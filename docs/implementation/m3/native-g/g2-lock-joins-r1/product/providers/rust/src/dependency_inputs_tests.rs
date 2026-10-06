use super::*;
use opensip_identity::{
    IdentityCandidate, JsonInteger, ObjectInput, RegisteredSchemas, canonical_bytes, hash_preimage,
    raw_sha256,
};
use opensip_identity::{digest_hex, hash_canonical_value};
use std::path::Path;
use std::sync::OnceLock;

const WORK: usize = 10_000_000;
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
fn fixture() -> Fixture {
    let mut f = Fixture::new();
    f.blobs
        .insert(raw_sha256(b"owned lock"), b"owned lock".to_vec());
    f
}
fn files(f: &mut Fixture, rows: &[(&str, &[u8])]) -> JsonValue {
    JsonValue::Array(
        rows.iter()
            .map(|(path, bytes)| {
                let sha = raw_sha256(bytes);
                f.blobs.insert(sha, bytes.to_vec());
                object([
                    ("path", text(path)),
                    ("contentSha256", text(&digest_hex(&sha))),
                    ("byteLength", number(bytes.len())),
                ])
            })
            .collect(),
    )
}
fn package(f: &mut Fixture, name: &str, manifest: &JsonValue) -> JsonValue {
    let sha = f.frame("native.dependency-file-manifest.v1", manifest);
    let rows = array(manifest).unwrap();
    let count = rows.len();
    let total = rows
        .iter()
        .map(|r| super::number(field(map(r).unwrap(), "byteLength").unwrap()).unwrap())
        .sum::<u64>();
    object([
        ("name", text(name)),
        ("version", text("1.0.0")),
        ("sourceKind", text("git")),
        (
            "sourceId",
            text("git+https://example.invalid/dependency#owned"),
        ),
        ("lockChecksum", JsonValue::Null),
        ("fileManifestSha256", text(&digest_hex(&sha))),
        ("fileCount", number(count)),
        (
            "totalBytes",
            JsonValue::Integer(JsonInteger::new(total as i128).unwrap()),
        ),
        (
            "acquisition",
            object([
                ("mode", text("imported-descriptor")),
                ("descriptorId", text(&format!("import2:{}", "9".repeat(64)))),
                ("vendorPath", JsonValue::Null),
            ]),
        ),
        ("checksumVerification", text("not-applicable")),
        ("provenanceAssurance", text("declared")),
    ])
}
fn packages(f: &mut Fixture, rows: Vec<JsonValue>) {
    fields(&mut f.dependency).insert("packages".into(), JsonValue::Array(rows));
}
fn check(f: &Fixture, ids: &Ids) -> Result<DependencyInputChecks, DependencyInputError> {
    check_declared_dependency_inputs(
        &RetainedInputs::new(schemas(), &f.objects, &f.blobs),
        &UniverseInputRequest {
            universe_digest: ids.u,
            context_digest: ids.c,
            expected_host_digest: ids.c,
            snapshot_id: &ids.snapshot,
            prepared_digest: ids.prepared,
            ownership_digest: ids.ownership,
        },
        WORK,
    )
}

#[test]
fn every_manifest_and_raw_member_joins_counts_without_provenance_admission() {
    let mut f = fixture();
    let first = files(
        &mut f,
        &[
            ("Cargo.toml", b"owned manifest"),
            ("src/lib.rs", b"owned source"),
        ],
    );
    let second = files(
        &mut f,
        &[("a#member", b"same"), ("資料.bin", &[0, 255, 128])],
    );
    let a = package(&mut f, "a", &first);
    let b = package(&mut f, "b", &second);
    packages(&mut f, vec![a, b]);
    let ids = f.ids();
    let result = check(&f, &ids).unwrap();
    assert_eq!(result.package_count(), 2);
    assert_eq!(result.declared_files(), 4);
    assert_eq!(
        result.declared_bytes(),
        (b"owned manifest".len() + b"owned source".len() + 4 + 3) as u64
    );
    assert_eq!(result.universe_checks().snapshot_id(), ids.snapshot);
    assert_eq!(
        result.dependency_digest(),
        hash_canonical_value("native.dependency-source-set.v1", &f.dependency).unwrap()
    );
}
#[test]
fn empty_package_manifest_and_incomplete_set_are_representable_observations() {
    let mut f = fixture();
    let p = package(&mut f, "empty", &JsonValue::Array(vec![]));
    packages(&mut f, vec![p]);
    fields(&mut f.dependency).insert(
        "completeness".into(),
        object([
            ("state", text("incomplete")),
            (
                "missing",
                JsonValue::Array(vec![object([
                    ("name", text("missing")),
                    ("version", text("1")),
                    ("sourceId", text("git+missing")),
                ])]),
            ),
        ]),
    );
    let ids = f.ids();
    let result = check(&f, &ids).unwrap();
    assert_eq!(result.declared_files(), 0);
    assert_eq!(result.declared_bytes(), 0);
}
#[test]
fn missing_or_substituted_manifest_h_preimage_refuses() {
    for missing in [true, false] {
        let mut f = fixture();
        let rows = files(&mut f, &[("a", b"data")]);
        let sha = hash_canonical_value("native.dependency-file-manifest.v1", &rows).unwrap();
        let p = package(&mut f, "owned", &rows);
        packages(&mut f, vec![p]);
        let ids = f.ids();
        if missing {
            f.blobs.remove(&sha);
        } else {
            f.blobs.insert(sha, canonical_bytes(&rows).unwrap());
        }
        assert!(matches!(
            check(&f, &ids),
            Err(DependencyInputError::Frame(_))
        ));
    }
}
#[test]
fn registered_foreign_nested_domain_cannot_replace_file_manifest() {
    let mut f = fixture();
    let rows = files(&mut f, &[("a", b"data")]);
    let mut p = package(&mut f, "owned", &rows);
    let foreign = f.frame("native.unified-features.rust.v1", &f.features.clone());
    fields(&mut p).insert("fileManifestSha256".into(), text(&digest_hex(&foreign)));
    packages(&mut f, vec![p]);
    let ids = f.ids();
    assert!(matches!(
        check(&f, &ids),
        Err(DependencyInputError::Mismatch {
            field: "fileManifest.domain",
            ..
        })
    ));
}
#[test]
fn source_member_missing_substituted_or_wrong_length_refuses() {
    for mode in 0..3 {
        let mut f = fixture();
        let mut rows = files(&mut f, &[("a", b"data")]);
        if mode == 2 {
            let JsonValue::Array(ref mut values) = rows else {
                unreachable!()
            };
            fields(&mut values[0]).insert("byteLength".into(), number(5));
        }
        let p = package(&mut f, "owned", &rows);
        packages(&mut f, vec![p]);
        let ids = f.ids();
        if mode == 0 {
            f.blobs.remove(&raw_sha256(b"data"));
        }
        if mode == 1 {
            f.blobs.insert(raw_sha256(b"data"), b"substituted".to_vec());
        }
        assert!(matches!(
            check(&f, &ids),
            Err(DependencyInputError::Retained(_))
        ));
    }
}
#[test]
fn file_count_and_byte_total_must_equal_retained_manifest() {
    for member in ["fileCount", "totalBytes"] {
        let mut f = fixture();
        let rows = files(&mut f, &[("a", b"data")]);
        let mut p = package(&mut f, "owned", &rows);
        fields(&mut p).insert(member.into(), number(99));
        packages(&mut f, vec![p]);
        let ids = f.ids();
        assert!(
            matches!(check(&f, &ids), Err(DependencyInputError::Mismatch { field: actual, .. }) if actual == member)
        );
    }
}
#[test]
fn aggregate_manifest_overflow_refuses_before_payload_consumption() {
    let mut f = fixture();
    let mut rows = files(&mut f, &[("a", b"data"), ("b", b"other")]);
    let JsonValue::Array(ref mut values) = rows else {
        unreachable!()
    };
    fields(&mut values[0]).insert(
        "byteLength".into(),
        JsonValue::Integer(JsonInteger::new(u64::MAX as i128).unwrap()),
    );
    fields(&mut values[1]).insert("byteLength".into(), number(1));
    let normal = files(&mut f, &[("a", b"data")]);
    let mut p = package(&mut f, "owned", &normal);
    let sha = f.frame("native.dependency-file-manifest.v1", &rows);
    fields(&mut p).insert("fileManifestSha256".into(), text(&digest_hex(&sha)));
    fields(&mut p).insert("fileCount".into(), number(2));
    packages(&mut f, vec![p]);
    let ids = f.ids();
    assert!(matches!(
        check(&f, &ids),
        Err(DependencyInputError::CountOverflow)
    ));
}
#[test]
fn repeated_payloads_count_per_member_and_cannot_have_conflicting_lengths() {
    let mut f = fixture();
    let rows = files(&mut f, &[("a", b"same"), ("b", b"same")]);
    let p = package(&mut f, "owned", &rows);
    packages(&mut f, vec![p]);
    let ids = f.ids();
    assert_eq!(check(&f, &ids).unwrap().declared_bytes(), 8);
    let mut rows = rows;
    let JsonValue::Array(ref mut values) = rows else {
        unreachable!()
    };
    fields(&mut values[1]).insert("byteLength".into(), number(5));
    let p = package(&mut f, "owned", &rows);
    packages(&mut f, vec![p]);
    let ids = f.ids();
    assert!(matches!(
        check(&f, &ids),
        Err(DependencyInputError::Retained(_))
    ));
}
#[test]
fn lock_raw_bytes_missing_substituted_or_length_conflicting_refuse() {
    for mode in 0..3 {
        let mut f = fixture();
        if mode == 0 {
            f.blobs.remove(&raw_sha256(b"owned lock"));
        }
        if mode == 1 {
            f.blobs
                .insert(raw_sha256(b"owned lock"), b"foreign".to_vec());
        }
        if mode == 2 {
            let JsonValue::Array(rows) =
                fields(&mut f.snapshot).get_mut("sourceInventory").unwrap()
            else {
                unreachable!()
            };
            fields(&mut rows[0]).insert("bytes".into(), number(1));
        }
        let ids = f.ids();
        assert!(matches!(
            check(&f, &ids),
            Err(DependencyInputError::Retained(_))
        ));
    }
}
#[test]
fn declared_checksum_mismatch_refuses_the_whole_observation() {
    let mut f = fixture();
    let rows = files(&mut f, &[("a", b"data")]);
    let mut p = package(&mut f, "owned", &rows);
    fields(&mut p).insert("checksumVerification".into(), text("mismatch"));
    packages(&mut f, vec![p]);
    let ids = f.ids();
    assert!(matches!(
        check(&f, &ids),
        Err(DependencyInputError::Mismatch {
            field: "checksumVerification",
            ..
        })
    ));
}
#[test]
fn authenticated_looking_labels_remain_declarations_without_authentication_token() {
    let mut f = fixture();
    let rows = files(&mut f, &[("a", b"data")]);
    let mut p = package(&mut f, "owned", &rows);
    fields(&mut p).insert("checksumVerification".into(), text("tarball-matched"));
    fields(&mut p).insert("provenanceAssurance".into(), text("registry-authenticated"));
    packages(&mut f, vec![p]);
    let ids = f.ids();
    assert_eq!(check(&f, &ids).unwrap().declared_files(), 1);
}
#[test]
fn file_manifest_path_order_uniqueness_and_escapes_are_schema_first() {
    for mode in 0..3 {
        let mut f = fixture();
        let mut rows = files(&mut f, &[("a", b"data"), ("b", b"other")]);
        let JsonValue::Array(ref mut values) = rows else {
            unreachable!()
        };
        match mode {
            0 => values.reverse(),
            1 => {
                fields(&mut values[1]).insert("path".into(), text("a"));
            }
            _ => {
                fields(&mut values[0]).insert("path".into(), text("../outside"));
            }
        }
        let p = package(&mut f, "owned", &rows);
        packages(&mut f, vec![p]);
        let ids = f.ids();
        assert!(matches!(
            check(&f, &ids),
            Err(DependencyInputError::Frame(_))
        ));
    }
}
#[test]
fn mandatory_universe_checks_precede_dependency_byte_checks() {
    let mut f = fixture();
    let ids = f.ids();
    f.blobs.remove(&ids.c);
    assert!(matches!(
        check(&f, &ids),
        Err(DependencyInputError::Universe(_))
    ));
}

fn lock_bytes(f: &mut Fixture, bytes: &[u8], version: usize) {
    f.blobs.insert(raw_sha256(bytes), bytes.to_vec());
    for value in [&mut f.universe, &mut f.dependency] {
        let lock = fields(fields(value).get_mut("lockfileIdentity").unwrap());
        lock.insert("contentSha256".into(), hash_text(bytes));
        lock.insert("lockfileVersion".into(), number(version));
    }
    let JsonValue::Array(rows) = fields(&mut f.snapshot).get_mut("sourceInventory").unwrap() else {
        panic!("inventory");
    };
    rows[0] = row("Cargo.lock", bytes);
}
fn lock_check(f: &Fixture, ids: &Ids) -> Result<DependencyLockChecks, DependencyLockError> {
    check_declared_lockfile_joins(
        &RetainedInputs::new(schemas(), &f.objects, &f.blobs),
        &UniverseInputRequest {
            universe_digest: ids.u,
            context_digest: ids.c,
            expected_host_digest: ids.c,
            snapshot_id: &ids.snapshot,
            prepared_digest: ids.prepared,
            ownership_digest: ids.ownership,
        },
        WORK,
    )
}
fn lock_git_row(name: &str, version: &str, source: &str) -> String {
    format!("[[package]]\nname='{name}'\nversion='{version}'\nsource='{source}'\n")
}
fn one_locked_package() -> Fixture {
    let mut f = fixture();
    let manifest = files(&mut f, &[("src/lib.rs", b"member")]);
    let package = package(&mut f, "owned", &manifest);
    packages(&mut f, vec![package]);
    lock_bytes(
        &mut f,
        format!(
            "version=4\n{}",
            lock_git_row(
                "owned",
                "1.0.0",
                "git+https://example.invalid/dependency#owned"
            )
        )
        .as_bytes(),
        4,
    );
    f
}
#[test]
fn lock_exact_tuple_and_version_join_after_mandatory_retained_inputs() {
    let mut f = one_locked_package();
    let ids = f.ids();
    let checked = lock_check(&f, &ids).unwrap();
    assert_eq!(checked.lockfile_version(), 4);
    assert_eq!(checked.lock_package_rows(), 1);
    assert_eq!(checked.dependency_checks().package_count(), 1);
    assert_eq!(checked.dependency_checks().declared_files(), 1);
}
#[test]
fn lock_supported_versions_and_toml_integer_values_are_compared_exactly() {
    for (literal, v) in [
        ("3", 3),
        ("4", 4),
        ("+4", 4),
        ("0x4", 4),
        ("0o4", 4),
        ("0b100", 4),
    ] {
        let mut f = fixture();
        lock_bytes(&mut f, format!("version={literal}\n").as_bytes(), v);
        let ids = f.ids();
        assert_eq!(lock_check(&f, &ids).unwrap().lockfile_version(), v as u8);
    }
    for literal in ["2", "5", "-4", "340282366920938463463374607431768211456"] {
        let mut f = fixture();
        lock_bytes(&mut f, format!("version={literal}\n").as_bytes(), 4);
        let ids = f.ids();
        assert!(matches!(
            lock_check(&f, &ids),
            Err(DependencyLockError::Version)
        ));
    }
    let mut f = fixture();
    lock_bytes(&mut f, b"version=3\n", 4);
    let ids = f.ids();
    assert!(matches!(
        lock_check(&f, &ids),
        Err(DependencyLockError::Version)
    ));
}
#[test]
fn lock_all_tuple_coordinates_are_exact_and_never_package_name_only() {
    for (name, version, source) in [
        (
            "Owned",
            "1.0.0",
            "git+https://example.invalid/dependency#owned",
        ),
        (
            "owned",
            "1.0.1",
            "git+https://example.invalid/dependency#owned",
        ),
        (
            "owned",
            "1.0.0",
            "git+https://example.invalid/dependency#different",
        ),
    ] {
        let mut f = one_locked_package();
        lock_bytes(
            &mut f,
            format!("version=4\n{}", lock_git_row(name, version, source)).as_bytes(),
            4,
        );
        let ids = f.ids();
        assert!(matches!(
            lock_check(&f, &ids),
            Err(DependencyLockError::MissingTuple(0))
        ));
    }
}
#[test]
fn lock_selected_duplicate_tuples_are_not_resolved_by_first_or_last() {
    let mut f = one_locked_package();
    let row = lock_git_row(
        "owned",
        "1.0.0",
        "git+https://example.invalid/dependency#owned",
    );
    lock_bytes(&mut f, format!("version=4\n{row}{row}").as_bytes(), 4);
    let ids = f.ids();
    assert!(matches!(
        lock_check(&f, &ids),
        Err(DependencyLockError::AmbiguousTuple(0))
    ));
}
#[test]
fn lock_checksum_matches_value_and_absence_without_authentication_claim() {
    for actual in [None, Some("a"), Some("b")] {
        let mut f = one_locked_package();
        let JsonValue::Array(rows) = fields(&mut f.dependency).get_mut("packages").unwrap() else {
            panic!("packages");
        };
        let p = fields(&mut rows[0]);
        p.insert("sourceKind".into(), text("registry"));
        p.insert(
            "sourceId".into(),
            text("registry+https://example.invalid/index"),
        );
        p.insert("lockChecksum".into(), text(&"a".repeat(64)));
        p.insert("checksumVerification".into(), text("self-consistent"));
        let mut raw = String::from(
            "version=4\n[[package]]\nname='owned'\nversion='1.0.0'\nsource='registry+https://example.invalid/index'\n",
        );
        if let Some(letter) = actual {
            raw.push_str(&format!("checksum='{}'\n", letter.repeat(64)));
        }
        lock_bytes(&mut f, raw.as_bytes(), 4);
        let ids = f.ids();
        if actual == Some("a") {
            assert!(lock_check(&f, &ids).is_ok());
        } else {
            assert!(matches!(
                lock_check(&f, &ids),
                Err(DependencyLockError::Checksum(0))
            ));
        }
    }
    let mut f = one_locked_package();
    let raw = format!(
        "version=4\n{}checksum='{}'\n",
        lock_git_row(
            "owned",
            "1.0.0",
            "git+https://example.invalid/dependency#owned"
        ),
        "a".repeat(64)
    );
    lock_bytes(&mut f, raw.as_bytes(), 4);
    let ids = f.ids();
    assert!(matches!(
        lock_check(&f, &ids),
        Err(DependencyLockError::Checksum(0))
    ));
}
#[test]
fn lock_path_source_absence_stays_empty_and_null_checksum() {
    for source_line in ["", "source=''\n"] {
        let mut f = one_locked_package();
        let JsonValue::Array(rows) = fields(&mut f.dependency).get_mut("packages").unwrap() else {
            panic!("packages");
        };
        let p = fields(&mut rows[0]);
        p.insert("sourceKind".into(), text("path"));
        p.insert("sourceId".into(), text(""));
        lock_bytes(
            &mut f,
            format!("version=4\n[[package]]\nname='owned'\nversion='1.0.0'\n{source_line}")
                .as_bytes(),
            4,
        );
        let ids = f.ids();
        assert!(lock_check(&f, &ids).is_ok());
    }
}
#[test]
fn lock_full_toml_parse_and_field_types_precede_selected_tuple_lookup() {
    for raw in [
        b"version=4\npackage=[]\nbroken=[".as_slice(),
        b"version='4'",
        b"version=true",
        b"version=4\npackage='text'",
        b"version=4\npackage=[7]",
        b"version=4\n[[package]]\nname=7\nversion='1.0.0'",
        b"version=4\n[[package]]\nname='p'\nversion='1.0.0'\nsource=false",
        b"version=4\n[[package]]\nname='p'\nversion='1.0.0'\nchecksum=7",
    ] {
        let mut f = one_locked_package();
        lock_bytes(&mut f, raw, 4);
        let ids = f.ids();
        assert!(matches!(
            lock_check(&f, &ids),
            Err(DependencyLockError::Parse(_)) | Err(DependencyLockError::Shape(_))
        ));
    }
}
#[test]
fn lock_unselected_rows_are_not_an_implicit_activation_or_completeness_claim() {
    let mut f = fixture();
    let row = lock_git_row(
        "unselected",
        "7.0.0",
        "git+https://example.invalid/other#rev",
    );
    lock_bytes(&mut f, format!("version=4\n{row}{row}").as_bytes(), 4);
    let ids = f.ids();
    let checked = lock_check(&f, &ids).unwrap();
    assert_eq!(checked.lock_package_rows(), 2);
    assert_eq!(checked.dependency_checks().package_count(), 0);
    let mut f = fixture();
    lock_bytes(&mut f, b"version=4\npackage=[]\n", 4);
    let ids = f.ids();
    assert_eq!(lock_check(&f, &ids).unwrap().lock_package_rows(), 0);
}
#[test]
fn lock_missing_or_changed_retained_bytes_keep_upstream_errors() {
    for changed in [false, true] {
        let mut f = one_locked_package();
        let digest = super::digest(
            super::text(
                field(
                    map(&map(&f.dependency).unwrap()["lockfileIdentity"]).unwrap(),
                    "contentSha256",
                )
                .unwrap(),
            )
            .unwrap(),
        )
        .unwrap();
        let ids = f.ids();
        if changed {
            f.blobs.insert(digest, b"version=4".to_vec());
        } else {
            f.blobs.remove(&digest);
        }
        assert!(matches!(
            lock_check(&f, &ids),
            Err(DependencyLockError::Inputs(DependencyInputError::Retained(
                _
            )))
        ));
    }
}
