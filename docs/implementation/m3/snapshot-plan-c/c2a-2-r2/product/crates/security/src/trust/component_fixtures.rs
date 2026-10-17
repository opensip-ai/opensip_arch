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
/// A supplied tree whose paths JSON must escape (C2A2-R1-RF-1): the first
/// file, the entrypoint, sits under a quoted directory and holds a quote and
/// a control; the others hold a tab, a newline, DEL, U+001F and non-ASCII.
/// Every path is lawful for the body validator and for identity-v3's
/// `LogicalPath`.
pub(crate) const ESCAPABLE_FILES: &[(&str, &[u8])] = &[
    ("q\"dir/entry\"\u{1}.sh", b"#!/bin/sh\n# synthetic entry\n"),
    ("lib/tab\there\nline.js", b"// tab and newline\n"),
    ("lib/\u{7f}del\u{1f}.js", b"// DEL and U+001F\n"),
    ("\u{65e5}\u{672c}/\u{8a9e}.wasm", b"\0asm"),
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

/// A JSON object of `members`, keyed as given.
fn object<const N: usize>(members: [(&str, V); N]) -> V {
    V::Object(
        members
            .into_iter()
            .map(|(k, v)| (k.to_owned(), v))
            .collect(),
    )
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
    // Every value is built as a JSON value and encoded by the identity
    // crate's canonical encoder, so any lawful path, quotes, controls and
    // non-ASCII included, is escaped exactly as `canonical.rs` escapes it
    // (C2A2-R1-RF-1); no supplied string is interpolated into JSON text.
    let text = |t: &str| V::String(t.to_owned());
    let mut rows = BTreeMap::new();
    for (path, raw) in c.files {
        for (at, _) in path.match_indices('/') {
            rows.insert(
                path[..at].to_owned(),
                object([
                    ("mode", text("0755")),
                    ("path", text(&path[..at])),
                    ("type", text("dir")),
                ]),
            );
        }
        rows.insert(
            (*path).to_owned(),
            object([
                ("length", int(raw.len() as i64)),
                ("mode", text("0755")),
                ("path", text(path)),
                (
                    "sha256",
                    text(&opensip_identity::digest_hex(
                        &opensip_identity::raw_sha256(raw),
                    )),
                ),
                ("type", text("file")),
            ]),
        );
    }
    let platform = object([
        ("arch", text(c.arch)),
        ("entrypoint", text(c.files[0].0)),
        ("os", text(c.os)),
        (
            "tree",
            object([("entries", V::Array(rows.into_values().collect()))]),
        ),
    ]);
    m.insert("platforms".to_owned(), V::Array(vec![platform]));
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
    // Built as a value and canonically encoded, as `body` is: the
    // pre-existing literal was already canonical, so its bytes are unchanged.
    let value = opensip_identity::parse_json(body).unwrap();
    let text = |t: &str| V::String(t.to_owned());
    let hex = |raw: &[u8]| {
        text(&opensip_identity::digest_hex(
            &opensip_identity::raw_sha256(raw),
        ))
    };
    let z = "0".repeat(64);
    let artifacts = tokens
        .iter()
        .map(|t| {
            object([
                ("archiveDigest", text(&z)),
                ("archiveProfileId", text(profile)),
                ("platform", text(t)),
                ("sha256", text(&z)),
            ])
        })
        .collect();
    let row = object([
        ("artifacts", V::Array(artifacts)),
        ("envelopeDigest", hex(&env)),
        (
            "hostCoreConstraint",
            object([
                ("includeMax", V::Bool(false)),
                ("includeMin", V::Bool(true)),
                ("max", text("0.2.0")),
                ("min", text("0.1.0")),
            ]),
        ),
        ("manifestDigest", hex(body)),
        (
            "manifestPreimageSha256",
            text(&opensip_identity::digest_hex(&preimage)),
        ),
        ("publisher", text("opensip")),
        ("sourceClass", text("first-party")),
        ("stableId", o(&value)["stableId"].clone()),
        ("version", o(&value)["version"].clone()),
    ]);
    let release = String::from_utf8(opensip_identity::canonical_bytes(&row).unwrap()).unwrap();
    (env, release)
}

/// One synthetic component of each role, at versions 1.0.0 to 1.0.4, in
/// `ROLES` order: the bodies a `Spec`'s `components` lists.
pub(crate) fn every_role() -> Vec<Vec<u8>> {
    every_role_with(FILES)
}
/// `every_role` over the supplied `files`.
pub(crate) fn every_role_with(files: &'static [(&'static str, &'static [u8])]) -> Vec<Vec<u8>> {
    const VERSIONS: [&str; 5] = ["1.0.0", "1.0.1", "1.0.2", "1.0.3", "1.0.4"];
    ROLES
        .iter()
        .zip(VERSIONS)
        .map(|(role, version)| {
            body(&Synthetic {
                files,
                ..Synthetic::of(role, version)
            })
        })
        .collect()
}

#[cfg(test)]
mod tests {
    include!("component_fixtures_tests.rs");
}
