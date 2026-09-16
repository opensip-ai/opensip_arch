use opensip_contracts::generated::output::{
    Metadata1BuildMetadataV1, Metadata1BuildMetadataV1BuildChannel,
};

// Sole build-channel selection. No environment or caller-controlled release path.
const BUILD_CHANNEL: Metadata1BuildMetadataV1BuildChannel =
    Metadata1BuildMetadataV1BuildChannel::Development;

// Private build input, not a wire type or a caller-supplied runtime record.
// A present pin identifies real, explicitly assembled asset-manifest bytes.
// No pin is selected in the metadata-only development build below.
#[derive(Clone, Copy)]
struct HostAssetPinV1 {
    schema_version: u8,
    asset_root: &'static str,
    asset_manifest_path: &'static str,
    asset_manifest_sha256: &'static str,
    asset_manifest_bytes: u64,
    build_channel: Metadata1BuildMetadataV1BuildChannel,
}

#[derive(Clone, Copy)]
struct CompiledBuildSelection {
    channel: Metadata1BuildMetadataV1BuildChannel,
    asset_pin: Option<HostAssetPinV1>,
}
impl CompiledBuildSelection {
    // Used in a const initializer: invalid explicit build inputs fail compilation.
    // This validates the private pin's shape and channel join only. Assembly must
    // separately prove the real manifest/member bytes and complete inventory;
    // the selected asset renderer later rechecks bounded reads and raw digests.
    const fn new(
        channel: Metadata1BuildMetadataV1BuildChannel,
        asset_pin: Option<HostAssetPinV1>,
    ) -> Self {
        if let Some(pin) = asset_pin {
            assert!(pin.schema_version == 1, "asset pin schema version differs");
            assert!(build_path(pin.asset_root), "invalid asset root");
            assert!(build_path(pin.asset_manifest_path), "invalid manifest path");
            let root = pin.asset_root.as_bytes();
            let path = pin.asset_manifest_path.as_bytes();
            assert!(
                path.len() > root.len() + 1,
                "manifest must be under asset root"
            );
            let mut i = 0;
            while i < root.len() {
                assert!(path[i] == root[i], "manifest must be under asset root");
                i += 1;
            }
            assert!(path[i] == b'/', "manifest must be under asset root");
            let digest = pin.asset_manifest_sha256.as_bytes();
            assert!(digest.len() == 64, "invalid raw manifest digest");
            let mut i = 0;
            while i < digest.len() {
                assert!(
                    matches!(digest[i], b'0'..=b'9' | b'a'..=b'f'),
                    "invalid raw manifest digest"
                );
                i += 1;
            }
            assert!(
                pin.asset_manifest_bytes >= 1 && pin.asset_manifest_bytes <= 9_007_199_254_740_990,
                "invalid manifest byte length"
            );
            let agrees = matches!(
                (channel, pin.build_channel),
                (
                    Metadata1BuildMetadataV1BuildChannel::Development,
                    Metadata1BuildMetadataV1BuildChannel::Development
                ) | (
                    Metadata1BuildMetadataV1BuildChannel::Release,
                    Metadata1BuildMetadataV1BuildChannel::Release
                )
            );
            assert!(
                agrees,
                "asset pin build channel differs from compiled metadata"
            );
        }
        Self { channel, asset_pin }
    }
    const fn channel(self) -> Metadata1BuildMetadataV1BuildChannel {
        match self.asset_pin {
            Some(pin) => pin.build_channel,
            None => self.channel,
        }
    }
}

// Canonical private release-relative POSIX path. Unicode bounds count scalars,
// not bytes; these private pin paths have no additional per-component255 rule.
const fn build_path(value: &str) -> bool {
    let bytes = value.as_bytes();
    if bytes.is_empty() {
        return false;
    }
    let mut scalars = 0;
    let mut start = 0;
    let mut i = 0;
    while i <= bytes.len() {
        if i == bytes.len() || bytes[i] == b'/' {
            let length = i - start;
            if length == 0
                || (length == 1 && bytes[start] == b'.')
                || (length == 2 && bytes[start] == b'.' && bytes[start + 1] == b'.')
            {
                return false;
            }
            start = i + 1;
        }
        if i < bytes.len() {
            if bytes[i] == b'\\' || bytes[i] == 0 {
                return false;
            }
            if bytes[i] & 0xc0 != 0x80 {
                scalars += 1;
            }
            if scalars > 4096 {
                return false;
            }
        }
        i += 1;
    }
    true
}

// Explicit absence of an asset selection: no dummy manifest path or digest.
// Selecting an assembled bundle must replace None with its admitted actual pin
// here, so the same const admission governs metadata and the future loader.
const BUILD_SELECTION: CompiledBuildSelection = CompiledBuildSelection::new(BUILD_CHANNEL, None);

pub fn development_metadata(
    host_release: &'static str,
) -> Result<Metadata1BuildMetadataV1, &'static str> {
    if !semver(host_release) {
        return Err("invalid compiled host version");
    }
    Ok(Metadata1BuildMetadataV1 {
        schema_version: 1_u64.into(),
        host_release: host_release
            .parse()
            .map_err(|_| "invalid compiled host version")?,
        build_channel: BUILD_SELECTION.channel(),
        closure_ids: Vec::new(),
    })
}
fn numeric(s: &str) -> bool {
    !s.is_empty() && s.bytes().all(|x| x.is_ascii_digit()) && (s == "0" || !s.starts_with('0'))
}
fn identifiers(s: &str, prerelease: bool) -> bool {
    s.split('.').all(|part| {
        !part.is_empty()
            && part.bytes().all(|b| b.is_ascii_alphanumeric() || b == b'-')
            && (!prerelease || !part.bytes().all(|b| b.is_ascii_digit()) || numeric(part))
    })
}
fn semver(s: &str) -> bool {
    if s.len() > 128 || !s.is_ascii() {
        return false;
    }
    let (version, build) = s.split_once('+').map_or((s, None), |(a, b)| (a, Some(b)));
    if build.is_some_and(|x| !identifiers(x, false)) {
        return false;
    }
    let (core, pre) = version
        .split_once('-')
        .map_or((version, None), |(a, b)| (a, Some(b)));
    if pre.is_some_and(|x| !identifiers(x, true)) {
        return false;
    }
    let parts: Vec<_> = core.split('.').collect();
    parts.len() == 3 && parts.iter().all(|s| numeric(s))
}
#[cfg(test)]
mod tests {
    use super::*;
    #[test]
    fn compiled_metadata_stays_development_and_semver_exact() {
        for value in ["0.1.0", "1.2.3-rc.1+test.01", "100000000000000000000.0.0"] {
            let m = development_metadata(value).unwrap();
            assert_eq!(m.build_channel, BUILD_CHANNEL);
            assert!(m.closure_ids.is_empty());
        }
        for value in [
            "01.2.3",
            "1.2",
            "1.2.3\n",
            "1.2.3-01",
            "1.2.3+",
            "1.2.3-a..b",
            "1.2.3+foo+bar",
            "1.2.3-α",
        ] {
            assert!(development_metadata(value).is_err(), "{value}");
        }
    }
}
