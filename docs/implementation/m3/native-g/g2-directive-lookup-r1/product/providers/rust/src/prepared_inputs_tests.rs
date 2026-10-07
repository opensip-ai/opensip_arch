use super::*;
use opensip_identity::{
    IdentityCandidate, IdentityDomain, JsonInteger, ObjectInput, RegisteredSchemas,
    canonical_bytes, hash_preimage, raw_sha256,
};
use opensip_identity::{digest_hex, hash_canonical_value};
use std::path::Path;
use std::sync::OnceLock;

const WORK: usize = 100_000_000;
fn schemas() -> &'static RegisteredSchemas {
    static REGISTRY: OnceLock<RegisteredSchemas> = OnceLock::new();
    REGISTRY.get_or_init(|| {
        let root = Path::new(env!("CARGO_MANIFEST_DIR")).join("../..");
        let raw: Vec<_> = RegisteredSchemas::source_requirements()
            .iter()
            .map(|pin| std::fs::read(root.join(pin.source_path())).unwrap())
            .collect();
        RegisteredSchemas::from_sources(&raw.iter().map(Vec::as_slice).collect::<Vec<_>>()).unwrap()
    })
}
fn object(entries: impl IntoIterator<Item = (&'static str, JsonValue)>) -> JsonValue {
    JsonValue::Object(
        entries
            .into_iter()
            .map(|(key, value)| (key.into(), value))
            .collect(),
    )
}
fn text(value: &str) -> JsonValue {
    JsonValue::String(value.into())
}
fn number(value: usize) -> JsonValue {
    JsonValue::Integer(JsonInteger::new(value as i128).unwrap())
}
fn hash_text(bytes: &[u8]) -> JsonValue {
    text(&digest_hex(&raw_sha256(bytes)))
}
fn fields(value: &mut JsonValue) -> &mut BTreeMap<String, JsonValue> {
    let JsonValue::Object(value) = value else {
        panic!("owned object fixture")
    };
    value
}
struct Fixture {
    objects: BTreeMap<String, ObjectInput>,
    blobs: BTreeMap<[u8; 32], Vec<u8>>,
    context: JsonValue,
    universe: JsonValue,
    dependency: JsonValue,
    features: JsonValue,
    snapshot: JsonValue,
    prepared: Option<JsonValue>,
    ownership: Option<JsonValue>,
}
impl Fixture {
    fn new() -> Self {
        let context = object([
            ("schemaVersion", number(2)),
            ("targetTriple", text("aarch64-apple-darwin")),
            ("hostTriple", text("aarch64-apple-darwin")),
            (
                "toolchain",
                object([
                    ("cargoVersion", text("1.95.0")),
                    ("rustCommitHash", text(&"0".repeat(40))),
                    ("rustcDevLlvmDigest", text(&"1".repeat(64))),
                    ("rustcVersion", text("1.95.0")),
                    ("standardLibraryComponentDigests", JsonValue::Array(vec![])),
                    ("sysrootDigest", hash_text(b"unadmitted sysroot fixture")),
                    ("targetTriple", text("aarch64-apple-darwin")),
                ]),
            ),
            (
                "toolClosure",
                object([
                    ("ar", hash_text(b"ar")),
                    ("cargo", hash_text(b"cargo")),
                    ("closureId", text(&format!("closure2:{}", "0".repeat(64)))),
                    ("linker", hash_text(b"linker")),
                    ("procMacroServer", hash_text(b"proc")),
                    ("rustc", hash_text(b"rustc")),
                ]),
            ),
            ("baseCfg", JsonValue::Array(vec![text("unix")])),
            ("resolverVersion", number(3)),
            (
                "dependencySourceSetId",
                text(&format!("sha256:{}", "a".repeat(64))),
            ),
            (
                "unifiedFeaturesId",
                text(&format!("sha256:{}", "b".repeat(64))),
            ),
            ("preparedOutputSetId", JsonValue::Null),
            (
                "configProjection",
                object([
                    ("schemaVersion", number(2)),
                    ("ancestorCarrierVerified", JsonValue::Bool(true)),
                    ("cargoHome", text("private-empty")),
                    ("claimsCargoSwitch", JsonValue::Bool(false)),
                    ("environmentProjection", text("none")),
                    ("honoredKeys", JsonValue::Array(vec![])),
                    ("projectionSha256", hash_text(b"unadmitted config fixture")),
                    ("replacedSnapshotConfigs", JsonValue::Array(vec![])),
                    (
                        "rustflags",
                        object([
                            ("executableSelected", JsonValue::Bool(false)),
                            ("honored", JsonValue::Array(vec![])),
                            ("stripped", JsonValue::Array(vec![])),
                        ]),
                    ),
                    ("strippedKeys", JsonValue::Array(vec![])),
                ]),
            ),
        ]);
        let universe = object([
            ("schemaVersion", number(2)),
            ("edition", object([("owned", number(2024))])),
            (
                "lockfileIdentity",
                object([
                    ("path", text("Cargo.lock")),
                    ("contentSha256", hash_text(b"owned lock")),
                    ("lockfileVersion", number(4)),
                ]),
            ),
            (
                "dependencySourceSetId",
                map(&context).unwrap()["dependencySourceSetId"].clone(),
            ),
            (
                "unifiedFeaturesId",
                map(&context).unwrap()["unifiedFeaturesId"].clone(),
            ),
            ("nativeContextId", JsonValue::Null),
            (
                "cfgSets",
                JsonValue::Array(vec![
                    cfg("primary", &["unix"]),
                    cfg("test", &["test", "unix"]),
                ]),
            ),
            (
                "rustflags",
                map(&map(&context).unwrap()["configProjection"]).unwrap()["rustflags"].clone(),
            ),
            ("crateRootPaths", JsonValue::Array(vec![text("src/lib.rs")])),
            (
                "configProjectionSha256",
                text(&digest_hex(
                    &hash_canonical_value(
                        "native.cargo-config-projection.v2",
                        &map(&context).unwrap()["configProjection"],
                    )
                    .unwrap(),
                )),
            ),
            ("preparedResolution", text("none")),
            ("executionCapableResolution", JsonValue::Bool(false)),
            ("preparedOutputSetId", JsonValue::Null),
            ("sourceUnitOwnershipId", JsonValue::Null),
        ]);

        let dependency = object([
            ("schemaVersion", number(1)),
            ("language", text("rust")),
            (
                "lockfileIdentity",
                map(&universe).unwrap()["lockfileIdentity"].clone(),
            ),
            ("packages", JsonValue::Array(vec![])),
            (
                "completeness",
                object([
                    ("state", text("complete")),
                    ("missing", JsonValue::Array(vec![])),
                ]),
            ),
        ]);
        let features = object([
            ("schemaVersion", number(1)),
            ("resolverVersion", number(3)),
            ("targetTriple", text("aarch64-apple-darwin")),
            ("activated", JsonValue::Array(vec![])),
            (
                "computedBy",
                object([
                    ("producer", text("opensip-cargo-adapter")),
                    ("producerBuildId", text("owned fixture")),
                ]),
            ),
        ]);
        let snapshot = object([
            ("schemaVersion", number(2)),
            ("projectId", text(&format!("prj1-{}", "0".repeat(64)))),
            (
                "sourceInventory",
                JsonValue::Array(vec![
                    row("Cargo.lock", b"owned lock"),
                    row("Cargo.toml", b"owned manifest"),
                    row("src/lib.rs", b"owned source"),
                ]),
            ),
            ("resolvedConfigDigest", hash_text(b"owned config")),
            ("scopeDigest", hash_text(b"owned scope")),
            ("vcsDigest", hash_text(b"owned vcs")),
        ]);
        Self {
            objects: BTreeMap::new(),
            blobs: BTreeMap::new(),
            context,
            universe,
            dependency,
            features,
            snapshot,
            prepared: None,
            ownership: None,
        }
    }
    fn frame(&mut self, domain: &str, value: &JsonValue) -> [u8; 32] {
        let bytes = hash_preimage(domain, value).unwrap();
        let sha = raw_sha256(&bytes);
        self.blobs.insert(sha, bytes);
        sha
    }
    fn ids(&mut self) -> Ids {
        let dependency = self.frame("native.dependency-source-set.v1", &self.dependency.clone());
        let features = self.frame("native.unified-features.rust.v1", &self.features.clone());
        for (name, sha) in [
            ("dependencySourceSetId", dependency),
            ("unifiedFeaturesId", features),
        ] {
            for record in [&mut self.context, &mut self.universe] {
                fields(record).insert(name.into(), id_text(sha));
            }
        }
        let prepared = self
            .prepared
            .clone()
            .map(|p| self.frame("native.prepared-output-set.v3", &p));
        for record in [&mut self.context, &mut self.universe] {
            fields(record).insert(
                "preparedOutputSetId".into(),
                prepared.map(id_text).unwrap_or(JsonValue::Null),
            );
        }
        let ownership = self
            .ownership
            .clone()
            .map(|o| self.frame("native.source-unit-ownership.v1", &o));
        fields(&mut self.universe).insert(
            "sourceUnitOwnershipId".into(),
            ownership.map(id_text).unwrap_or(JsonValue::Null),
        );
        let projection = &map(&self.context).unwrap()["configProjection"];
        fields(&mut self.universe).insert(
            "configProjectionSha256".into(),
            text(&digest_hex(
                &hash_canonical_value("native.cargo-config-projection.v2", projection).unwrap(),
            )),
        );
        let c = self.frame("native.context.rust.v2", &self.context.clone());
        fields(&mut self.universe).insert("nativeContextId".into(), id_text(c));
        let u = self.frame("native.semantic-universe.rust.v2", &self.universe.clone());
        let snapshot = IdentityCandidate::from_json(
            schemas(),
            IdentityDomain::Snapshot,
            &canonical_bytes(&self.snapshot).unwrap(),
            WORK,
        )
        .unwrap()
        .identifier()
        .to_owned();
        self.objects.insert(
            snapshot.clone(),
            ObjectInput {
                domain: IdentityDomain::Snapshot,
                descriptor: self.snapshot.clone(),
            },
        );
        Ids {
            u,
            c,
            snapshot,
            prepared,
            ownership,
        }
    }
    fn prepare(&mut self, kind: &str) {
        let dep =
            hash_canonical_value("native.dependency-source-set.v1", &self.dependency).unwrap();
        let imported = kind == "imported-descriptor";
        self.prepared = Some(object([
            ("schemaVersion", number(3)),
            ("rows", JsonValue::Array(vec![])),
            (
                "preparation",
                object([
                    ("kind", text(kind)),
                    (
                        "authorizationId",
                        if imported {
                            JsonValue::Null
                        } else {
                            id_text([3; 32])
                        },
                    ),
                    (
                        "importId",
                        if imported {
                            text(&format!("import2:{}", "3".repeat(64)))
                        } else {
                            JsonValue::Null
                        },
                    ),
                    (
                        "toolchain",
                        map(&self.context).unwrap()["toolchain"].clone(),
                    ),
                    ("dependencySourceSetId", id_text(dep)),
                    ("cfgSetId", text("primary")),
                    (
                        "producer",
                        object([("id", text("external")), ("version", text("owned"))]),
                    ),
                ]),
            ),
        ]));
        fields(&mut self.universe).insert(
            "preparedResolution".into(),
            text(if imported {
                "imported-inert"
            } else {
                "host-prepared"
            }),
        );
        fields(&mut self.universe)
            .insert("executionCapableResolution".into(), JsonValue::Bool(true));
    }
}
fn cfg(id: &str, values: &[&str]) -> JsonValue {
    object([
        ("cfgSetId", text(id)),
        (
            "cfg",
            JsonValue::Array(values.iter().map(|s| text(s)).collect()),
        ),
    ])
}

struct Ids {
    u: [u8; 32],
    c: [u8; 32],
    snapshot: String,
    prepared: Option<[u8; 32]>,
    ownership: Option<[u8; 32]>,
}
fn id_text(sha: [u8; 32]) -> JsonValue {
    text(&format!("sha256:{}", digest_hex(&sha)))
}
fn row(path: &str, bytes: &[u8]) -> JsonValue {
    object([
        ("path", text(path)),
        ("sha256", hash_text(bytes)),
        ("bytes", number(bytes.len())),
    ])
}

fn retained(f: &mut Fixture, bytes: &[u8]) -> JsonValue {
    let sha = raw_sha256(bytes);
    f.blobs.insert(sha, bytes.to_vec());
    text(&digest_hex(&sha))
}
fn blob(f: &mut Fixture, bytes: &[u8], media: &str) -> JsonValue {
    object([
        ("sha256", retained(f, bytes)),
        ("byteLength", number(bytes.len())),
        ("mediaType", text(media)),
    ])
}
fn prepared() -> Fixture {
    let mut f = Fixture::new();
    f.prepare("imported-descriptor");
    retained(&mut f, b"owner manifest");
    let toolchain = canonical_bytes(&map(&f.context).unwrap()["toolchain"]).unwrap();
    retained(&mut f, &toolchain);
    f
}
fn output(f: &mut Fixture, kind: &str, media: &str, bytes: &[u8]) -> JsonValue {
    let preparation = map(&map(f.prepared.as_ref().unwrap()).unwrap()["preparation"]).unwrap();
    let dep = preparation["dependencySourceSetId"].clone();
    let toolchain = canonical_bytes(&preparation["toolchain"]).unwrap();
    let binding = object([
        ("ownerFileManifestSha256", hash_text(b"owner manifest")),
        ("dependencySourceSetId", dep),
        ("toolchainDigest", hash_text(&toolchain)),
        ("cfgSetId", text("primary")),
    ]);
    object([
        ("kind", text(kind)),
        ("ownerKey", text("owned")),
        ("configuration", JsonValue::Array(vec![])),
        ("site", JsonValue::Null),
        ("generated", JsonValue::Null),
        ("inputBinding", binding),
        ("blob", blob(f, bytes, media)),
        ("status", text("ok")),
        ("failureDetail", JsonValue::Null),
    ])
}
fn generated(f: &mut Fixture, path: &str, bytes: &[u8]) -> JsonValue {
    let mut row = output(f, "generated-file", "application/octet-stream", bytes);
    let body = map(&row).unwrap()["blob"].clone();
    fields(&mut row).insert(
        "generated".into(),
        object([("logicalPath", text(path)), ("blob", body)]),
    );
    row
}
fn set_rows(f: &mut Fixture, rows: Vec<JsonValue>) {
    fields(f.prepared.as_mut().unwrap()).insert("rows".into(), JsonValue::Array(rows));
}
fn check(
    f: &Fixture,
    ids: &Ids,
    owners: &BTreeMap<String, [u8; 32]>,
) -> Result<PreparedInputChecks, PreparedInputError> {
    check_declared_prepared_inputs(
        &RetainedInputs::new(schemas(), &f.objects, &f.blobs),
        &PreparedInputRequest {
            universe: UniverseInputRequest {
                universe_digest: ids.u,
                context_digest: ids.c,
                expected_host_digest: ids.c,
                snapshot_id: &ids.snapshot,
                prepared_digest: ids.prepared,
                ownership_digest: ids.ownership,
            },
            owner_manifests: owners,
        },
        WORK,
    )
}
fn owners() -> BTreeMap<String, [u8; 32]> {
    BTreeMap::from([("owned".into(), raw_sha256(b"owner manifest"))])
}

#[test]
fn all_three_inert_kinds_retain_bytes_and_failed_rows_without_admission() {
    let mut f = prepared();
    let directives = output(
        &mut f,
        "build-script-directives",
        "text/x-cargo-directives",
        b"cargo:rustc-cfg=owned",
    );
    let mut expansion = output(
        &mut f,
        "macro-expansion",
        "text/x-rust-expansion",
        b"fn expanded() {}",
    );
    let token = retained(&mut f, b"owned!()");
    fields(&mut expansion).insert(
        "site".into(),
        object([
            ("path", text("src/lib.rs")),
            ("startByte", number(0)),
            ("endByte", number(8)),
            ("inputTokenDigest", token),
        ]),
    );
    let mut data = generated(&mut f, "資料.bin", &[0, 255, 128]);
    fields(&mut data).insert("status".into(), text("failed"));
    fields(&mut data).insert("failureDetail".into(), text("owned failed capture"));
    set_rows(&mut f, vec![directives, expansion, data]);
    let ids = f.ids();
    let result = check(&f, &ids, &owners()).unwrap();
    assert_eq!(result.prepared_digest(), ids.prepared);
    assert_eq!(result.row_count(), 3);
    assert_eq!(result.failed_rows(), 1);
    assert_eq!(result.generated_rows(), 1);
    assert_eq!(result.universe_checks().snapshot_id(), ids.snapshot);
}
#[test]
fn absent_selection_remains_absent_despite_other_custodied_blobs() {
    let mut f = Fixture::new();
    retained(&mut f, b"unselected bytes");
    let ids = f.ids();
    let result = check(&f, &ids, &owners()).unwrap();
    assert_eq!(result.prepared_digest(), None);
    assert_eq!(result.row_count(), 0);
}
#[test]
fn selected_set_still_requires_mandatory_universe_input_checks() {
    let mut f = prepared();
    let ids = f.ids();
    f.blobs.remove(&ids.c);
    assert!(matches!(
        check(&f, &ids, &owners()),
        Err(PreparedInputError::Universe(_))
    ));
}
#[test]
fn row_blob_missing_tampered_or_wrong_length_refuses() {
    for mode in 0..3 {
        let mut f = prepared();
        let mut row = output(
            &mut f,
            "build-script-directives",
            "text/x-cargo-directives",
            b"owned data",
        );
        let sha = raw_sha256(b"owned data");
        match mode {
            0 => {
                f.blobs.remove(&sha);
            }
            1 => {
                f.blobs.insert(sha, b"tampered".to_vec());
            }
            _ => {
                fields(fields(&mut row).get_mut("blob").unwrap())
                    .insert("byteLength".into(), number(99));
            }
        }
        set_rows(&mut f, vec![row]);
        let ids = f.ids();
        assert!(matches!(
            check(&f, &ids, &owners()),
            Err(PreparedInputError::Retained(_))
        ));
    }
}
#[test]
fn generated_outer_and_inner_references_are_independently_retained() {
    let mut f = prepared();
    let mut row = generated(&mut f, "generated.rs", b"inner");
    let outer = blob(&mut f, b"outer", "text/plain");
    fields(&mut row).insert("blob".into(), outer);
    set_rows(&mut f, vec![row]);
    let ids = f.ids();
    assert!(check(&f, &ids, &owners()).is_ok());
    for sha in [raw_sha256(b"inner"), raw_sha256(b"outer")] {
        let bytes = f.blobs.remove(&sha).unwrap();
        assert!(matches!(
            check(&f, &ids, &owners()),
            Err(PreparedInputError::Retained(_))
        ));
        f.blobs.insert(sha, bytes);
    }
}
#[test]
fn expansion_token_preimage_is_retained_without_claiming_site_verification() {
    let mut f = prepared();
    let mut row = output(
        &mut f,
        "macro-expansion",
        "text/x-rust-expansion",
        b"expanded",
    );
    let token = retained(&mut f, b"tokens");
    fields(&mut row).insert(
        "site".into(),
        object([
            ("path", text("src/lib.rs")),
            ("startByte", number(0)),
            ("endByte", number(6)),
            ("inputTokenDigest", token),
        ]),
    );
    set_rows(&mut f, vec![row]);
    let ids = f.ids();
    assert!(check(&f, &ids, &owners()).is_ok());
    f.blobs.remove(&raw_sha256(b"tokens"));
    assert!(matches!(
        check(&f, &ids, &owners()),
        Err(PreparedInputError::Retained(_))
    ));
}
#[test]
fn owner_selection_and_owner_manifest_retention_are_both_required() {
    let mut f = prepared();
    let row = output(
        &mut f,
        "build-script-directives",
        "text/x-cargo-directives",
        b"data",
    );
    set_rows(&mut f, vec![row]);
    let ids = f.ids();
    for selected in [
        BTreeMap::new(),
        BTreeMap::from([("owned".into(), raw_sha256(b"foreign owner"))]),
    ] {
        assert!(matches!(
            check(&f, &ids, &selected),
            Err(PreparedInputError::Binding {
                field: "ownerFileManifestSha256",
                ..
            })
        ));
    }
    f.blobs.remove(&raw_sha256(b"owner manifest"));
    assert!(matches!(
        check(&f, &ids, &owners()),
        Err(PreparedInputError::Retained(_))
    ));
}
#[test]
fn toolchain_canonical_preimage_is_required_and_tampering_refuses() {
    for missing in [true, false] {
        let mut f = prepared();
        let toolchain = canonical_bytes(&map(&f.context).unwrap()["toolchain"]).unwrap();
        let sha = raw_sha256(&toolchain);
        if missing {
            f.blobs.remove(&sha);
        } else {
            f.blobs.insert(sha, b"foreign toolchain".to_vec());
        }
        let ids = f.ids();
        assert!(matches!(
            check(&f, &ids, &owners()),
            Err(PreparedInputError::Retained(_))
        ));
    }
}
#[test]
fn stale_row_bindings_are_diagnostics_including_failed_rows() {
    for field in [
        "toolchainDigest",
        "cfgSetId",
        "dependencySourceSetId",
        "ownerFileManifestSha256",
    ] {
        let mut f = prepared();
        let mut row = output(
            &mut f,
            "build-script-directives",
            "text/x-cargo-directives",
            b"data",
        );
        let value = match field {
            "cfgSetId" => text("test"),
            "dependencySourceSetId" => id_text([9; 32]),
            _ => text(&"9".repeat(64)),
        };
        fields(fields(&mut row).get_mut("inputBinding").unwrap()).insert(field.into(), value);
        fields(&mut row).insert("status".into(), text("failed"));
        set_rows(&mut f, vec![row]);
        let ids = f.ids();
        assert!(
            matches!(check(&f, &ids, &owners()), Err(PreparedInputError::Binding { field: actual, .. }) if actual == field)
        );
    }
}
#[test]
fn executable_kind_refuses_despite_inert_looking_media() {
    for kind in ["proc-macro-dylib", "build-script-binary"] {
        for media in [
            "text/x-rust-expansion",
            "text/plain",
            "application/octet-stream",
        ] {
            let mut f = prepared();
            let row = output(&mut f, kind, media, b"executable-shaped bytes");
            set_rows(&mut f, vec![row]);
            let ids = f.ids();
            assert!(matches!(
                check(&f, &ids, &owners()),
                Err(PreparedInputError::NonInert { row: 0 })
            ));
        }
    }
}
#[test]
fn each_inert_kind_refuses_a_foreign_media_type() {
    for kind in [
        "build-script-directives",
        "macro-expansion",
        "generated-file",
    ] {
        let mut f = prepared();
        let row = output(&mut f, kind, "application/x-sharedlib", b"data");
        set_rows(&mut f, vec![row]);
        let ids = f.ids();
        assert!(matches!(
            check(&f, &ids, &owners()),
            Err(PreparedInputError::NonInert { row: 0 })
        ));
    }
}
#[test]
fn generated_binding_requires_generated_kind_and_present_generated_reference() {
    for generated_kind in [true, false] {
        let mut f = prepared();
        let mut row = generated(&mut f, "data", b"data");
        if generated_kind {
            fields(&mut row).insert("generated".into(), JsonValue::Null);
        } else {
            fields(&mut row).insert("kind".into(), text("macro-expansion"));
            fields(fields(&mut row).get_mut("blob").unwrap())
                .insert("mediaType".into(), text("text/x-rust-expansion"));
        }
        set_rows(&mut f, vec![row]);
        let ids = f.ids();
        assert!(matches!(
            check(&f, &ids, &owners()),
            Err(PreparedInputError::NonInert { row: 0 })
        ));
    }
}
#[test]
fn generated_reference_media_and_exact_length_are_checked() {
    for foreign_media in [true, false] {
        let mut f = prepared();
        let mut row = generated(&mut f, "data", b"data");
        let inner = fields(
            fields(fields(&mut row).get_mut("generated").unwrap())
                .get_mut("blob")
                .unwrap(),
        );
        if foreign_media {
            inner.insert("mediaType".into(), text("application/x-sharedlib"));
        } else {
            inner.insert("byteLength".into(), number(5));
        }
        set_rows(&mut f, vec![row]);
        let ids = f.ids();
        if foreign_media {
            assert!(matches!(
                check(&f, &ids, &owners()),
                Err(PreparedInputError::NonInert { row: 0 })
            ));
        } else {
            assert!(matches!(
                check(&f, &ids, &owners()),
                Err(PreparedInputError::Retained(_))
            ));
        }
    }
}
#[test]
fn generated_logical_path_limit_counts_utf8_bytes() {
    let mut f = prepared();
    let row = generated(&mut f, &"é".repeat(513), b"data");
    set_rows(&mut f, vec![row]);
    let ids = f.ids();
    assert!(matches!(
        check(&f, &ids, &owners()),
        Err(PreparedInputError::GeneratedBound {
            field: "maxLogicalPathBytes",
            ..
        })
    ));
}
#[test]
fn oversized_generated_length_refuses_before_consuming_blob() {
    let mut f = prepared();
    let mut row = generated(&mut f, "data", b"data");
    fields(
        fields(fields(&mut row).get_mut("generated").unwrap())
            .get_mut("blob")
            .unwrap(),
    )
    .insert("byteLength".into(), number(67_108_865));
    set_rows(&mut f, vec![row]);
    let ids = f.ids();
    assert!(matches!(
        check(&f, &ids, &owners()),
        Err(PreparedInputError::GeneratedBound {
            field: "maxGeneratedFileBytes",
            ..
        })
    ));
}
#[test]
fn published_per_owner_generated_count_boundary_is_exact() {
    let mut f = prepared();
    let mut rows = Vec::new();
    for i in 0..4096 {
        rows.push(generated(&mut f, &format!("data/{i}"), b""));
    }
    set_rows(&mut f, rows.clone());
    let ids = f.ids();
    assert_eq!(check(&f, &ids, &owners()).unwrap().generated_rows(), 4096);
    rows.push(generated(&mut f, "data/4096", b""));
    set_rows(&mut f, rows);
    let ids = f.ids();
    assert!(matches!(
        check(&f, &ids, &owners()),
        Err(PreparedInputError::GeneratedBound {
            row: 4096,
            field: "maxGeneratedFilesPerOwner"
        })
    ));
}
#[test]
fn path_escape_is_schema_first_before_blob_consumption() {
    for path in [
        "../outside",
        "/absolute",
        "data/./file",
        "data\\file",
        "data\0file",
    ] {
        let mut f = prepared();
        let row = generated(&mut f, path, b"data");
        set_rows(&mut f, vec![row]);
        let ids = f.ids();
        assert!(matches!(
            check(&f, &ids, &owners()),
            Err(PreparedInputError::Universe(_))
        ));
    }
}

#[test]
fn published_total_generated_bytes_boundary_counts_every_row() {
    let mut f = prepared();
    let bytes = vec![b'x'; 1_048_576];
    let prototype = generated(&mut f, "data/0", &bytes);
    let mut rows = Vec::new();
    for i in 0..1024 {
        let mut row = prototype.clone();
        fields(fields(&mut row).get_mut("generated").unwrap())
            .insert("logicalPath".into(), text(&format!("data/{i}")));
        rows.push(row);
    }
    set_rows(&mut f, rows.clone());
    let ids = f.ids();
    assert_eq!(check(&f, &ids, &owners()).unwrap().generated_rows(), 1024);
    let mut over = prototype;
    fields(fields(&mut over).get_mut("generated").unwrap())
        .insert("logicalPath".into(), text("data/1024"));
    rows.push(over);
    set_rows(&mut f, rows);
    let ids = f.ids();
    assert!(matches!(
        check(&f, &ids, &owners()),
        Err(PreparedInputError::GeneratedBound {
            row: 1024,
            field: "maxGeneratedTotalBytes"
        })
    ));
}

#[test]
fn repeated_blob_reference_cannot_contradict_its_verified_length() {
    let mut f = prepared();
    let first = generated(&mut f, "data/first", b"shared");
    let mut second = generated(&mut f, "data/second", b"shared");
    fields(
        fields(fields(&mut second).get_mut("generated").unwrap())
            .get_mut("blob")
            .unwrap(),
    )
    .insert("byteLength".into(), number(7));
    set_rows(&mut f, vec![first, second]);
    let ids = f.ids();
    assert!(matches!(
        check(&f, &ids, &owners()),
        Err(PreparedInputError::Retained(_))
    ));
}

fn lookup(
    f: &Fixture,
    ids: &Ids,
    selected: &BTreeMap<String, [u8; 32]>,
    owner: &str,
    path: &str,
) -> Result<DeclaredGeneratedFile, GeneratedLookupError> {
    lookup_declared_generated_file(
        &RetainedInputs::new(schemas(), &f.objects, &f.blobs),
        &PreparedInputRequest {
            universe: UniverseInputRequest {
                universe_digest: ids.u,
                context_digest: ids.c,
                expected_host_digest: ids.c,
                snapshot_id: &ids.snapshot,
                prepared_digest: ids.prepared,
                ownership_digest: ids.ownership,
            },
            owner_manifests: selected,
        },
        owner,
        path,
        WORK,
    )
}
#[test]
fn generated_lookup_uses_exact_inner_bytes_and_owns_them() {
    let mut f = prepared();
    let mut row = generated(&mut f, "generated.rs", b"inner source");
    let outer = blob(&mut f, b"outer observation", "text/plain");
    fields(&mut row).insert("blob".into(), outer);
    set_rows(&mut f, vec![row]);
    let ids = f.ids();
    let DeclaredGeneratedFile::Bytes(bytes) =
        lookup(&f, &ids, &owners(), "owned", "generated.rs").unwrap()
    else {
        panic!("exact match");
    };
    f.blobs
        .insert(raw_sha256(b"inner source"), b"replacement".to_vec());
    drop(f);
    assert_eq!(&*bytes, b"inner source");
}
#[test]
fn generated_lookup_does_not_find_prefix_other_owner_or_unreferenced_blob() {
    let mut f = prepared();
    let row = generated(&mut f, "generated.rs", b"source");
    retained(&mut f, b"ambient extra");
    set_rows(&mut f, vec![row]);
    let ids = f.ids();
    for (owner, path) in [
        ("owned", "generated.rs.more"),
        ("other", "generated.rs"),
        ("owned", "extra"),
    ] {
        assert!(matches!(
            lookup(&f, &ids, &owners(), owner, path).unwrap(),
            DeclaredGeneratedFile::Missing
        ));
    }
    let mut f = prepared();
    let ids = f.ids();
    assert!(matches!(
        lookup(&f, &ids, &owners(), "owned", "generated.rs").unwrap(),
        DeclaredGeneratedFile::Missing
    ));
    let mut f = Fixture::new();
    let ids = f.ids();
    assert!(matches!(
        lookup(&f, &ids, &owners(), "owned", "generated.rs").unwrap(),
        DeclaredGeneratedFile::Missing
    ));
}
#[test]
fn failed_script_owner_cannot_be_hidden_by_generated_row_order() {
    for reverse in [false, true] {
        let mut f = prepared();
        let row = generated(&mut f, "generated.rs", b"source");
        let mut failed = output(
            &mut f,
            "build-script-directives",
            "text/x-cargo-directives",
            b"failed capture",
        );
        fields(&mut failed).insert("status".into(), text("failed"));
        fields(&mut failed).insert("failureDetail".into(), text("failed"));
        let mut rows = vec![row, failed];
        if reverse {
            rows.reverse();
        }
        set_rows(&mut f, rows);
        let ids = f.ids();
        assert!(matches!(
            lookup(&f, &ids, &owners(), "owned", "generated.rs").unwrap(),
            DeclaredGeneratedFile::Missing
        ));
    }
    let mut f = prepared();
    let mut row = generated(&mut f, "generated.rs", b"failed source");
    fields(&mut row).insert("status".into(), text("failed"));
    fields(&mut row).insert("failureDetail".into(), text("failed"));
    set_rows(&mut f, vec![row]);
    let ids = f.ids();
    assert!(matches!(
        lookup(&f, &ids, &owners(), "owned", "generated.rs").unwrap(),
        DeclaredGeneratedFile::Missing
    ));
}
#[test]
fn other_owner_failure_does_not_hide_selected_generated_file() {
    let mut f = prepared();
    let row = generated(&mut f, "generated.rs", b"source");
    let mut failed = output(
        &mut f,
        "build-script-directives",
        "text/x-cargo-directives",
        b"other failure",
    );
    fields(&mut failed).insert("ownerKey".into(), text("other"));
    fields(&mut failed).insert("status".into(), text("failed"));
    fields(&mut failed).insert("failureDetail".into(), text("failed"));
    set_rows(&mut f, vec![row, failed]);
    let ids = f.ids();
    let mut selected = owners();
    selected.insert("other".into(), raw_sha256(b"owner manifest"));
    assert!(matches!(
        lookup(&f, &ids, &selected, "owned", "generated.rs").unwrap(),
        DeclaredGeneratedFile::Bytes(_)
    ));
}
#[test]
fn generated_lookup_ambiguity_never_selects_first_or_last_bytes() {
    for reverse in [false, true] {
        let mut f = prepared();
        let a = generated(&mut f, "generated.rs", b"a");
        let b = generated(&mut f, "generated.rs", b"b");
        let mut rows = vec![a, b];
        if reverse {
            rows.reverse();
        }
        set_rows(&mut f, rows);
        let ids = f.ids();
        assert!(matches!(
            lookup(&f, &ids, &owners(), "owned", "generated.rs"),
            Err(GeneratedLookupError::Ambiguous)
        ));
    }
}
#[test]
fn generated_lookup_path_bounds_and_prerequisite_failures_are_independent() {
    let mut f = prepared();
    let row = generated(&mut f, "generated.rs", b"source");
    set_rows(&mut f, vec![row]);
    let ids = f.ids();
    for path in [
        "",
        "/escape",
        "../escape",
        "a/./b",
        "a/../b",
        "a\\b",
        "a\0b",
        &"x".repeat(1025),
    ] {
        assert!(matches!(
            lookup(&f, &ids, &owners(), "owned", path).unwrap(),
            DeclaredGeneratedFile::OutOfBounds
        ));
    }
    assert!(matches!(
        lookup(&f, &ids, &owners(), "owned", &"x".repeat(1024)).unwrap(),
        DeclaredGeneratedFile::Missing
    ));
    f.blobs.remove(&raw_sha256(b"source"));
    assert!(matches!(
        lookup(&f, &ids, &owners(), "owned", "../escape"),
        Err(GeneratedLookupError::Prepared(
            PreparedInputError::Retained(_)
        ))
    ));
}

fn expansion_row(f: &mut Fixture, bytes: &[u8]) -> JsonValue {
    let mut row = output(f, "macro-expansion", "text/x-rust-expansion", bytes);
    let token = retained(f, b"tokens");
    fields(&mut row).insert(
        "site".into(),
        object([
            ("path", text("src/lib.rs")),
            ("startByte", number(2)),
            ("endByte", number(8)),
            ("inputTokenDigest", token),
        ]),
    );
    row
}
fn expansion_site() -> DeclaredExpansionSite<'static> {
    DeclaredExpansionSite {
        path: "src/lib.rs",
        start_byte: 2,
        end_byte: 8,
        input_token_digest: raw_sha256(b"tokens"),
        macro_crate_manifest_sha256: raw_sha256(b"owner manifest"),
    }
}
fn expansion_lookup(
    f: &Fixture,
    ids: &Ids,
    site: &DeclaredExpansionSite<'_>,
) -> Result<DeclaredMacroExpansion, MacroLookupError> {
    lookup_declared_macro_expansion(
        &RetainedInputs::new(schemas(), &f.objects, &f.blobs),
        &PreparedInputRequest {
            universe: UniverseInputRequest {
                universe_digest: ids.u,
                context_digest: ids.c,
                expected_host_digest: ids.c,
                snapshot_id: &ids.snapshot,
                prepared_digest: ids.prepared,
                ownership_digest: ids.ownership,
            },
            owner_manifests: &owners(),
        },
        site,
        WORK,
    )
}
#[test]
fn expansion_lookup_exact_tuple_owns_retained_bytes() {
    let mut f = prepared();
    let row = expansion_row(&mut f, b"expanded");
    set_rows(&mut f, vec![row]);
    let ids = f.ids();
    let DeclaredMacroExpansion::Bytes(bytes) =
        expansion_lookup(&f, &ids, &expansion_site()).unwrap()
    else {
        panic!("exact tuple");
    };
    f.blobs
        .insert(raw_sha256(b"expanded"), b"replacement".to_vec());
    drop(f);
    assert_eq!(&*bytes, b"expanded");
}
#[test]
fn expansion_lookup_each_tuple_coordinate_is_mandatory() {
    let mut f = prepared();
    let row = expansion_row(&mut f, b"expanded");
    set_rows(&mut f, vec![row]);
    let ids = f.ids();
    for change in 0..5 {
        let mut site = expansion_site();
        match change {
            0 => site.path = "src/lib.rs.more",
            1 => site.start_byte = 3,
            2 => site.end_byte = 9,
            3 => site.input_token_digest = raw_sha256(b"different tokens"),
            _ => site.macro_crate_manifest_sha256 = raw_sha256(b"different manifest"),
        };
        assert!(matches!(
            expansion_lookup(&f, &ids, &site).unwrap(),
            DeclaredMacroExpansion::Missing
        ));
    }
}
#[test]
fn expansion_lookup_failed_null_empty_and_absent_rows_supply_no_bytes() {
    for status in ["failed", "null"] {
        let mut f = prepared();
        let mut row = expansion_row(&mut f, b"expanded");
        if status == "failed" {
            fields(&mut row).insert("status".into(), text("failed"));
            fields(&mut row).insert("failureDetail".into(), text("failed"));
        } else {
            fields(&mut row).insert("site".into(), JsonValue::Null);
        }
        set_rows(&mut f, vec![row]);
        let ids = f.ids();
        assert!(matches!(
            expansion_lookup(&f, &ids, &expansion_site()).unwrap(),
            DeclaredMacroExpansion::Missing
        ));
    }
    let mut f = prepared();
    let ids = f.ids();
    assert!(matches!(
        expansion_lookup(&f, &ids, &expansion_site()).unwrap(),
        DeclaredMacroExpansion::Missing
    ));
    let mut f = Fixture::new();
    let ids = f.ids();
    assert!(matches!(
        expansion_lookup(&f, &ids, &expansion_site()).unwrap(),
        DeclaredMacroExpansion::Missing
    ));
}
#[test]
fn expansion_lookup_ambiguity_has_no_row_order_priority() {
    for reverse in [false, true] {
        let mut f = prepared();
        let a = expansion_row(&mut f, b"first");
        let b = expansion_row(&mut f, b"second");
        let mut rows = vec![a, b];
        if reverse {
            rows.reverse();
        }
        set_rows(&mut f, rows);
        let ids = f.ids();
        assert!(matches!(
            expansion_lookup(&f, &ids, &expansion_site()),
            Err(MacroLookupError::Ambiguous)
        ));
    }
}
#[test]
fn expansion_lookup_miss_cannot_bypass_retention_or_stale_binding() {
    let mut f = prepared();
    let mut row = expansion_row(&mut f, b"expanded");
    fields(fields(&mut row).get_mut("inputBinding").unwrap())
        .insert("cfgSetId".into(), text("other"));
    set_rows(&mut f, vec![row]);
    let ids = f.ids();
    let mut site = expansion_site();
    site.path = "absent.rs";
    assert!(matches!(
        expansion_lookup(&f, &ids, &site),
        Err(MacroLookupError::Prepared(PreparedInputError::Binding {
            field: "cfgSetId",
            ..
        }))
    ));
    let mut f = prepared();
    let row = expansion_row(&mut f, b"expanded");
    set_rows(&mut f, vec![row]);
    let ids = f.ids();
    f.blobs.remove(&raw_sha256(b"tokens"));
    assert!(matches!(
        expansion_lookup(&f, &ids, &site),
        Err(MacroLookupError::Prepared(PreparedInputError::Retained(_)))
    ));
}

fn directive_lookup(
    f: &Fixture,
    ids: &Ids,
    owner: &str,
) -> Result<DeclaredBuildScriptDirectives, DirectiveLookupError> {
    lookup_declared_build_script_directives(
        &RetainedInputs::new(schemas(), &f.objects, &f.blobs),
        &PreparedInputRequest {
            universe: UniverseInputRequest {
                universe_digest: ids.u,
                context_digest: ids.c,
                expected_host_digest: ids.c,
                snapshot_id: &ids.snapshot,
                prepared_digest: ids.prepared,
                ownership_digest: ids.ownership,
            },
            owner_manifests: &owners(),
        },
        owner,
        WORK,
    )
}
#[test]
fn directive_lookup_retains_exact_uninterpreted_owned_bytes() {
    let mut f = prepared();
    let raw = b"cargo:rustc-cfg=custom\ncargo:rustc-env=KEY=value\n\xff\0";
    let row = output(
        &mut f,
        "build-script-directives",
        "text/x-cargo-directives",
        raw,
    );
    set_rows(&mut f, vec![row]);
    let ids = f.ids();
    let DeclaredBuildScriptDirectives::Bytes(bytes) = directive_lookup(&f, &ids, "owned").unwrap()
    else {
        panic!("directives");
    };
    f.blobs.insert(raw_sha256(raw), b"replacement".to_vec());
    drop(f);
    assert_eq!(&*bytes, raw);
}
#[test]
fn directive_lookup_owner_and_kind_are_exact() {
    let mut f = prepared();
    let row = output(
        &mut f,
        "build-script-directives",
        "text/x-cargo-directives",
        b"captured",
    );
    let other = expansion_row(&mut f, b"expansion");
    set_rows(&mut f, vec![row, other]);
    let ids = f.ids();
    for owner in ["", "own", "owned-more", "Owned"] {
        assert!(matches!(
            directive_lookup(&f, &ids, owner).unwrap(),
            DeclaredBuildScriptDirectives::Missing
        ));
    }
    let mut f = prepared();
    let row = expansion_row(&mut f, b"expansion");
    set_rows(&mut f, vec![row]);
    let ids = f.ids();
    assert!(matches!(
        directive_lookup(&f, &ids, "owned").unwrap(),
        DeclaredBuildScriptDirectives::Missing
    ));
}
#[test]
fn directive_lookup_failed_owner_dominates_ok_rows_in_either_order() {
    for reverse in [false, true] {
        let mut f = prepared();
        let ok = output(
            &mut f,
            "build-script-directives",
            "text/x-cargo-directives",
            b"captured",
        );
        let mut failed = output(
            &mut f,
            "build-script-directives",
            "text/x-cargo-directives",
            b"partial",
        );
        fields(&mut failed).insert("status".into(), text("failed"));
        fields(&mut failed).insert("failureDetail".into(), text("build failed"));
        let mut rows = vec![ok, failed];
        if reverse {
            rows.reverse();
        }
        set_rows(&mut f, rows);
        let ids = f.ids();
        assert!(matches!(
            directive_lookup(&f, &ids, "owned").unwrap(),
            DeclaredBuildScriptDirectives::Missing
        ));
    }
}
#[test]
fn directive_lookup_duplicate_ok_rows_never_merge_or_choose_by_order() {
    for reverse in [false, true] {
        let mut f = prepared();
        let a = output(
            &mut f,
            "build-script-directives",
            "text/x-cargo-directives",
            b"one",
        );
        let b = output(
            &mut f,
            "build-script-directives",
            "text/x-cargo-directives",
            b"two",
        );
        let mut rows = vec![a, b];
        if reverse {
            rows.reverse();
        }
        set_rows(&mut f, rows);
        let ids = f.ids();
        assert!(matches!(
            directive_lookup(&f, &ids, "owned"),
            Err(DirectiveLookupError::Ambiguous)
        ));
    }
}
#[test]
fn directive_lookup_empty_and_absent_sets_are_missing() {
    for mut f in [prepared(), Fixture::new()] {
        let ids = f.ids();
        assert!(matches!(
            directive_lookup(&f, &ids, "owned").unwrap(),
            DeclaredBuildScriptDirectives::Missing
        ));
    }
}
#[test]
fn directive_lookup_miss_and_failed_owner_cannot_bypass_whole_set_checks() {
    let mut f = prepared();
    let mut row = output(
        &mut f,
        "build-script-directives",
        "text/x-cargo-directives",
        b"captured",
    );
    fields(fields(&mut row).get_mut("inputBinding").unwrap())
        .insert("cfgSetId".into(), text("stale"));
    set_rows(&mut f, vec![row]);
    let ids = f.ids();
    assert!(matches!(
        directive_lookup(&f, &ids, "missing"),
        Err(DirectiveLookupError::Prepared(
            PreparedInputError::Binding {
                field: "cfgSetId",
                ..
            }
        ))
    ));
    let mut f = prepared();
    let mut row = output(
        &mut f,
        "build-script-directives",
        "text/x-cargo-directives",
        b"partial",
    );
    fields(&mut row).insert("status".into(), text("failed"));
    fields(&mut row).insert("failureDetail".into(), text("failed"));
    set_rows(&mut f, vec![row]);
    let ids = f.ids();
    f.blobs.remove(&raw_sha256(b"partial"));
    assert!(matches!(
        directive_lookup(&f, &ids, "owned"),
        Err(DirectiveLookupError::Prepared(
            PreparedInputError::Retained(_)
        ))
    ));
}
