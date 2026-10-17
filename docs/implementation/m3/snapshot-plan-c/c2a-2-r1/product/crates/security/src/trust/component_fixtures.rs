// M3-C r8 item 8 (unit C2a-2; C2a plan r4, LD-C2A-6 and the Q4 ruling): the
// shared synthetic signed component fixtures. Included in
// `core_authentication.rs`'s `tests` module, so it is compiled under exactly
// that module's joint test-and-fixture predicate and adds no predicate site
// of its own (the crash-matrix site census is unchanged).
//
// It generalizes that module's component builders to role-valid manifests of
// every role, each with C2PM-1's `closureProtocolMajor` and a tree built from
// supplied file bytes, and signs them only with the public test-only signers
// `INDEX_SIGNER` and `COMPONENT_SIGNER` under the existing synthetic root
// that module already uses. It introduces no root, key source or feature. Its
// outputs carry no authority: they enter through the ordinary reader and
// C2a-1's candidate like any signed release. Every artifact row it writes
// carries `LABEL` as its `archiveProfileId` (C2-T8's label half).
use super::*;

/// The label every synthetic artifact carries (`scenario.rs`'s `LABEL`).
pub(crate) const LABEL: &str = "synthetic";
/// CR-1's five manifest roles (`component_manifest.rs`, `closure_kind`).
pub(crate) const ROLES: [&str; 5] = [
    "analyzer",
    "toolchain",
    "stdlib",
    "rust-dev-llvm",
    "grammar",
];

/// One synthetic component: its role, its version (the catalog identity's
/// last member), C2PM-1's declaration when given, the `{os, arch}` row it
/// declares, and its tree's regular files by path, with their bytes.
#[derive(Clone, Copy)]
pub(crate) struct Synthetic<'a> {
    pub(crate) role: &'a str,
    pub(crate) version: &'a str,
    pub(crate) major: Option<i64>,
    pub(crate) os: &'a str,
    pub(crate) arch: &'a str,
    pub(crate) files: &'a [(&'a str, &'a [u8])],
}
/// A default tree: an executable entry and one library file.
pub(crate) const FILES: &[(&str, &[u8])] = &[
    ("bin/entry", b"#!/bin/sh\n# synthetic entry\n"),
    ("lib/provider.js", b"// synthetic library\n"),
];
impl Synthetic<'static> {
    /// `role` at `version` 1.0.`i`, declaring major 1 (its role's supported
    /// major, and the analyzer's `providerProtocol`) for `macos-arm64`.
    pub(crate) fn of(role: &'static str, version: &'static str) -> Self {
        Self {
            role,
            version,
            major: Some(1),
            os: "macos",
            arch: "arm64",
            files: FILES,
        }
    }
}

/// The role-valid canonical body: `COMPONENT_MANIFEST` with the role, the
/// version, the declaration and the tree, and, for every role but the
/// analyzer, no commands and empty capabilities and permissions (CR-1, as
/// `component_manifest.rs`'s `cr1_body`). Directory rows cover every proper
/// prefix; every file is `0755`, and the entrypoint is the first file.
pub(crate) fn body(c: &Synthetic<'_>) -> Vec<u8> {
    let int = |n: i64| V::Integer(opensip_identity::JsonInteger::new(n as i128).unwrap());
    let mut v = opensip_identity::parse_json(COMPONENT_MANIFEST.as_bytes()).unwrap();
    let V::Object(m) = &mut v else { unreachable!() };
    m.insert("role".to_owned(), V::String(c.role.to_owned()));
    m.insert("version".to_owned(), V::String(c.version.to_owned()));
    if c.role != "analyzer" {
        m.remove("commands");
        m.insert("capabilities".to_owned(), V::Array(Vec::new()));
        m.insert("permissions".to_owned(), V::Array(Vec::new()));
    }
    if let Some(major) = c.major {
        m.insert("closureProtocolMajor".to_owned(), int(major));
    }
    let mut rows = BTreeMap::new();
    for (path, raw) in c.files {
        for (at, _) in path.match_indices('/') {
            rows.insert(
                path[..at].to_owned(),
                format!(r#"{{"mode":"0755","path":"{}","type":"dir"}}"#, &path[..at]),
            );
        }
        rows.insert(
            (*path).to_owned(),
            format!(
                r#"{{"length":{},"mode":"0755","path":"{path}","sha256":"{}","type":"file"}}"#,
                raw.len(),
                opensip_identity::digest_hex(&opensip_identity::raw_sha256(raw))
            ),
        );
    }
    let entries: Vec<&str> = rows.values().map(String::as_str).collect();
    let platform = format!(
        r#"{{"arch":"{}","entrypoint":"{}","os":"{}","tree":{{"entries":[{}]}}}}"#,
        c.arch,
        c.files[0].0,
        c.os,
        entries.join(",")
    );
    m.insert(
        "platforms".to_owned(),
        V::Array(vec![
            opensip_identity::parse_json(platform.as_bytes()).unwrap(),
        ]),
    );
    opensip_identity::canonical_bytes(&v).unwrap()
}

/// The body's envelope, signed by `signer` with the keys `root` lists, and
/// the catalog release row that joins it: its identity read from the body,
/// one artifact per platform token, each carrying `LABEL`.
pub(crate) fn release(
    body: &[u8],
    signer: Signer<'_>,
    root: &V,
    tokens: &[&str],
) -> (Vec<u8>, String) {
    release_row(body, signer, root, tokens, LABEL)
}
/// `release` with the artifacts' `archiveProfileId`: `LABEL` for every
/// synthetic row, and `p1` only for the pre-existing rows, whose bytes stay
/// unchanged (`component_release`).
pub(crate) fn release_row(
    body: &[u8],
    (role, by): Signer<'_>,
    root: &V,
    tokens: &[&str],
    profile: &str,
) -> (Vec<u8>, String) {
    let env = sign(
        body,
        "manifest",
        "opensip.metadata.manifest.1",
        role,
        root,
        by,
    );
    let carrier = crate::trust::metadata::parse(&env).unwrap();
    let preimage = super::super::verified_envelopes::parse_carrier(&carrier)
        .unwrap()
        .preimage_digest();
    let value = opensip_identity::parse_json(body).unwrap();
    let z = "0".repeat(64);
    let artifacts: Vec<String> = tokens
        .iter()
        .map(|t| {
            format!(
                r#"{{"archiveDigest":"{z}","archiveProfileId":"{profile}","platform":"{t}","sha256":"{z}"}}"#
            )
        })
        .collect();
    let release = format!(
        r#"{{"artifacts":[{}],"envelopeDigest":"{}","hostCoreConstraint":{{"includeMax":false,"includeMin":true,"max":"0.2.0","min":"0.1.0"}},"manifestDigest":"{}","manifestPreimageSha256":"{}","publisher":"opensip","sourceClass":"first-party","stableId":"{}","version":"{}"}}"#,
        artifacts.join(","),
        opensip_identity::digest_hex(&opensip_identity::raw_sha256(&env)),
        opensip_identity::digest_hex(&opensip_identity::raw_sha256(body)),
        opensip_identity::digest_hex(&preimage),
        s(&o(&value)["stableId"]),
        s(&o(&value)["version"]),
    );
    (env, release)
}

/// One synthetic component of each role, at versions 1.0.0 to 1.0.4, in
/// `ROLES` order: the bodies a `Spec`'s `components` lists.
pub(crate) fn every_role() -> Vec<Vec<u8>> {
    const VERSIONS: [&str; 5] = ["1.0.0", "1.0.1", "1.0.2", "1.0.3", "1.0.4"];
    ROLES
        .iter()
        .zip(VERSIONS)
        .map(|(role, version)| body(&Synthetic::of(role, version)))
        .collect()
}

#[cfg(test)]
mod tests {
    include!("component_fixtures_tests.rs");
}
