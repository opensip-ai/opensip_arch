use opensip_contracts::generated::output::{
    Metadata1BuildMetadataV1, Metadata1BuildMetadataV1BuildChannel,
};

// Sole build-channel selection. No environment or caller-controlled release path.
const BUILD_CHANNEL: Metadata1BuildMetadataV1BuildChannel =
    Metadata1BuildMetadataV1BuildChannel::Development;

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
        build_channel: BUILD_CHANNEL,
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
