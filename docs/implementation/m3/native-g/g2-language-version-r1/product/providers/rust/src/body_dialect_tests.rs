use super::*;
use opensip_identity::digest_hex;
use opensip_identity::{
    IdentityCandidate, IdentityDomain, JsonInteger, ObjectInput, RegisteredSchemas,
    canonical_bytes, hash_canonical_value, hash_preimage, raw_sha256,
};
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
    fn check(&self, ids: &Ids, path: &str) -> Result<BodyDialectChecks, BodyDialectError> {
        check_declared_body_dialect(
            &RetainedInputs::new(schemas(), &self.objects, &self.blobs),
            &UniverseInputRequest {
                universe_digest: ids.u,
                context_digest: ids.c,
                expected_host_digest: ids.c,
                snapshot_id: &ids.snapshot,
                prepared_digest: ids.prepared,
                ownership_digest: ids.ownership,
            },
            path,
            WORK,
        )
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

fn target(name: &str, crate_name: &str, edition: Option<usize>) -> JsonValue {
    let projection = object([
        ("schemaVersion", number(1)),
        ("markerPath", text("Cargo.toml")),
        ("targetKind", text("lib")),
        ("targetName", text(name)),
    ]);
    let id = id_text(hash_canonical_value("native.compilation-unit.v1", &projection).unwrap());
    object([
        ("unitId", id),
        ("markerPath", text("Cargo.toml")),
        ("crateName", text(crate_name)),
        ("targetKind", text("lib")),
        ("targetName", text(name)),
        (
            "targetEdition",
            edition.map(number).unwrap_or(JsonValue::Null),
        ),
    ])
}
fn unit_id(unit: &JsonValue) -> JsonValue {
    map(unit).unwrap()["unitId"].clone()
}
fn install(
    f: &mut Fixture,
    mut units: Vec<JsonValue>,
    mut selected: Vec<JsonValue>,
    paths: &[(&str, usize)],
) {
    let mut rows: Vec<_> = paths
        .iter()
        .map(|(path, index)| object([("path", text(path)), ("unitId", unit_id(&units[*index]))]))
        .collect();
    units.sort_by_key(|u| text_of(&map(u).unwrap()["unitId"]));
    selected.sort_by_key(text_of);
    rows.sort_by_key(|r| {
        (
            text_of(&map(r).unwrap()["path"]),
            text_of(&map(r).unwrap()["unitId"]),
        )
    });
    f.ownership = Some(object([
        ("schemaVersion", number(1)),
        ("enumeration", text("complete")),
        ("units", JsonValue::Array(units)),
        ("selectedUnitIds", JsonValue::Array(selected)),
        ("ownership", JsonValue::Array(rows)),
    ]));
}
fn text_of(value: &JsonValue) -> String {
    super::text(value).unwrap().to_owned()
}
fn single() -> Fixture {
    let mut f = Fixture::new();
    let unit = target("library", "owned", None);
    install(
        &mut f,
        vec![unit.clone()],
        vec![unit_id(&unit)],
        &[("src/lib.rs", 0)],
    );
    f
}
fn two(a: Option<usize>, b: Option<usize>, selected: &[usize]) -> Fixture {
    let mut f = Fixture::new();
    let units = vec![target("library", "owned", a), target("tests", "owned", b)];
    let selection = selected.iter().map(|i| unit_id(&units[*i])).collect();
    install(
        &mut f,
        units,
        selection,
        &[("src/lib.rs", 0), ("src/lib.rs", 1)],
    );
    f
}
#[test]
fn exact_owner_default_is_a_diagnostic_with_mandatory_input_checks() {
    let mut f = single();
    let ids = f.ids();
    let result = f.check(&ids, "src/lib.rs").unwrap();
    assert_eq!(result.edition(), 2024);
    assert_eq!(result.selected_owner_count(), 1);
    assert_eq!(result.input_checks().snapshot_id(), ids.snapshot);
    assert_eq!(
        result.input_checks().field_checks().universe_digest(),
        ids.u
    );
}
#[test]
fn single_edition_map_still_requires_committed_ownership() {
    let mut f = Fixture::new();
    let ids = f.ids();
    assert!(matches!(
        f.check(&ids, "src/lib.rs"),
        Err(BodyDialectError::MissingOwnership)
    ));
}
#[test]
fn partial_refuses_before_no_path_or_unselected_or_ambiguous_decision() {
    for selected in [vec![0], vec![0, 1]] {
        let mut f = two(Some(2018), Some(2024), &selected);
        fields(f.ownership.as_mut().unwrap()).insert("enumeration".into(), text("partial"));
        let ids = f.ids();
        for path in ["src/lib.rs", "does/not/exist"] {
            assert!(matches!(
                f.check(&ids, path),
                Err(BodyDialectError::PartialEnumeration)
            ));
        }
    }
}
#[test]
fn path_matching_is_exact_without_prefix_nearest_case_or_normalization() {
    let mut f = single();
    let ids = f.ids();
    for path in [
        "src",
        "src/lib.rs/body",
        "SRC/lib.rs",
        "src/./lib.rs",
        "src/lib.rs/",
        "src/lib.rs\n",
        "",
    ] {
        assert!(
            matches!(f.check(&ids, path), Err(BodyDialectError::NotCompiled)),
            "{path:?}"
        );
    }
}
#[test]
fn unselected_only_owner_refuses_before_borrowing_an_edition() {
    let mut f = Fixture::new();
    let units = vec![
        target("library", "owned", Some(2018)),
        target("other", "owned", Some(2024)),
    ];
    let selected = vec![unit_id(&units[1])];
    install(&mut f, units, selected, &[("src/lib.rs", 0)]);
    let ids = f.ids();
    assert!(matches!(
        f.check(&ids, "src/lib.rs"),
        Err(BodyDialectError::NotSelected)
    ));
}
#[test]
fn target_override_wins_even_when_all_package_defaults_agree() {
    for edition in [2015, 2018, 2021, 2024] {
        let mut f = two(Some(edition), None, &[0]);
        let ids = f.ids();
        assert_eq!(
            f.check(&ids, "src/lib.rs").unwrap().edition(),
            edition as u16
        );
    }
}
#[test]
fn several_selected_owners_with_same_effective_edition_agree() {
    for overrides in [(None, None), (Some(2024), None), (Some(2018), Some(2018))] {
        let mut f = two(overrides.0, overrides.1, &[0, 1]);
        let ids = f.ids();
        let r = f.check(&ids, "src/lib.rs").unwrap();
        assert_eq!(r.selected_owner_count(), 2);
        assert_eq!(r.edition(), overrides.0.unwrap_or(2024) as u16);
    }
}
#[test]
fn selected_conflict_refuses_independently_of_order_and_package_map_size() {
    for pair in [(2018, 2024), (2024, 2018), (2015, 2021)] {
        let mut f = two(Some(pair.0), Some(pair.1), &[0, 1]);
        let ids = f.ids();
        assert!(matches!(
            f.check(&ids, "src/lib.rs"),
            Err(BodyDialectError::AmbiguousEdition)
        ));
    }
}
#[test]
fn different_committed_selections_change_universe_and_choose_same_path_differently() {
    let mut a = two(Some(2018), Some(2024), &[0]);
    let a_ids = a.ids();
    let mut b = two(Some(2018), Some(2024), &[1]);
    let b_ids = b.ids();
    assert_ne!(a_ids.ownership, b_ids.ownership);
    assert_ne!(a_ids.u, b_ids.u);
    assert_eq!(a.check(&a_ids, "src/lib.rs").unwrap().edition(), 2018);
    assert_eq!(b.check(&b_ids, "src/lib.rs").unwrap().edition(), 2024);
}
#[test]
fn mixed_default_map_uses_owning_crate_and_ignores_unrelated_crates() {
    let mut f = Fixture::new();
    fields(&mut f.universe).insert(
        "edition".into(),
        object([
            ("owned", number(2018)),
            ("other", number(2024)),
            ("unrelated", number(2015)),
        ]),
    );
    let units = vec![
        target("library", "owned", None),
        target("other", "other", None),
    ];
    let selection = units.iter().map(unit_id).collect();
    install(
        &mut f,
        units,
        selection,
        &[("src/lib.rs", 0), ("src/other.rs", 1)],
    );
    let JsonValue::Array(inventory) = fields(&mut f.snapshot).get_mut("sourceInventory").unwrap()
    else {
        panic!()
    };
    inventory.push(row("src/other.rs", b"other source"));
    let ids = f.ids();
    assert_eq!(f.check(&ids, "src/lib.rs").unwrap().edition(), 2018);
    assert_eq!(f.check(&ids, "src/other.rs").unwrap().edition(), 2024);
}
#[test]
fn hash_unicode_and_marker_paths_are_not_narrowed() {
    let mut f = single();
    let path = "dir#片/src.rs";
    let o = fields(f.ownership.as_mut().unwrap());
    let JsonValue::Array(rows) = o.get_mut("ownership").unwrap() else {
        panic!()
    };
    fields(&mut rows[0]).insert("path".into(), text(path));
    let JsonValue::Array(inventory) = fields(&mut f.snapshot).get_mut("sourceInventory").unwrap()
    else {
        panic!()
    };
    inventory.insert(2, row(path, b"unicode source"));
    let ids = f.ids();
    assert_eq!(f.check(&ids, path).unwrap().edition(), 2024);
    assert!(matches!(
        f.check(&ids, "dir#片"),
        Err(BodyDialectError::NotCompiled)
    ));
}
#[test]
fn malformed_ownership_and_unbound_inputs_keep_upstream_refusals() {
    let mut f = single();
    let mut ids = f.ids();
    ids.c = [0; 32];
    assert!(matches!(
        f.check(&ids, "src/lib.rs"),
        Err(BodyDialectError::Inputs(_))
    ));
    let mut f = single();
    let mut ids = f.ids();
    ids.ownership = Some([0; 32]);
    assert!(matches!(
        f.check(&ids, "src/lib.rs"),
        Err(BodyDialectError::Inputs(_))
    ));
    let mut f = single();
    let ids = f.ids();
    f.blobs.remove(&ids.ownership.unwrap());
    assert!(matches!(
        f.check(&ids, "src/lib.rs"),
        Err(BodyDialectError::Inputs(_))
    ));
}
#[test]
fn forged_unit_and_missing_default_are_not_dialect_selections() {
    let mut f = single();
    let JsonValue::Array(units) = fields(f.ownership.as_mut().unwrap())
        .get_mut("units")
        .unwrap()
    else {
        panic!()
    };
    fields(&mut units[0]).insert("unitId".into(), id_text([0; 32]));
    let ids = f.ids();
    assert!(matches!(
        f.check(&ids, "src/lib.rs"),
        Err(BodyDialectError::Inputs(_))
    ));
    let mut f = single();
    let JsonValue::Array(units) = fields(f.ownership.as_mut().unwrap())
        .get_mut("units")
        .unwrap()
    else {
        panic!()
    };
    fields(&mut units[0]).insert("crateName".into(), text("absent"));
    let ids = f.ids();
    assert!(matches!(
        f.check(&ids, "src/lib.rs"),
        Err(BodyDialectError::Inputs(_))
    ));
}

fn version_tools(f: &mut Fixture) {
    let version = super::text(
        field(
            map(&map(&f.context).unwrap()["toolchain"]).unwrap(),
            "rustcVersion",
        )
        .unwrap(),
    )
    .unwrap()
    .to_owned();
    let manifest = b"inert unadmitted manifest";
    f.blobs.insert(raw_sha256(manifest), manifest.to_vec());
    let tools: [(&str, &[u8]); 5] = [
        ("bin/ar", b"ar"),
        ("bin/cargo", b"cargo"),
        ("bin/linker", b"linker"),
        ("bin/proc", b"proc"),
        ("bin/rustc", b"rustc"),
    ];
    for (_, raw) in tools {
        f.blobs.insert(raw_sha256(raw), raw.to_vec());
    }
    f.blobs
        .insert(raw_sha256(b"dev-library"), b"dev-library".to_vec());
    let closure = |kind, tree| {
        object([
            ("schemaVersion", number(2)),
            ("kind", text(kind)),
            ("manifestDigest", hash_text(manifest)),
            ("tree", JsonValue::Array(tree)),
            ("semanticVersion", text(&version)),
            ("protocolMajor", number(3)),
            ("platform", text("macos-aarch64")),
        ])
    };
    for (kind, tree, dev) in [
        (
            "toolchain",
            tools.iter().map(|(path, raw)| row(path, raw)).collect(),
            false,
        ),
        ("rust-dev-llvm", vec![row("lib/dev", b"dev-library")], true),
    ] {
        let descriptor = closure(kind, tree);
        let id = IdentityCandidate::from_json(
            schemas(),
            IdentityDomain::Closure,
            &canonical_bytes(&descriptor).unwrap(),
            WORK,
        )
        .unwrap()
        .identifier()
        .to_owned();
        f.objects.insert(
            id.clone(),
            ObjectInput {
                domain: IdentityDomain::Closure,
                descriptor,
            },
        );
        if dev {
            fields(fields(&mut f.context).get_mut("toolchain").unwrap()).insert(
                "rustcDevLlvmDigest".into(),
                text(id.strip_prefix("closure2:").unwrap()),
            );
        } else {
            fields(fields(&mut f.context).get_mut("toolClosure").unwrap())
                .insert("closureId".into(), text(&id));
        }
    }
}
fn version_check(
    f: &Fixture,
    ids: &Ids,
    path: &str,
) -> Result<DeclaredBodyLanguageVersion, BodyLanguageVersionError> {
    derive_declared_body_language_version(
        &RetainedInputs::new(schemas(), &f.objects, &f.blobs),
        &UniverseInputRequest {
            universe_digest: ids.u,
            context_digest: ids.c,
            expected_host_digest: ids.c,
            snapshot_id: &ids.snapshot,
            prepared_digest: ids.prepared,
            ownership_digest: ids.ownership,
        },
        path,
        WORK,
    )
}
#[test]
fn language_version_closed_record_has_exact_canonical_bytes_and_raw_sha256() {
    let mut f = single();
    version_tools(&mut f);
    let ids = f.ids();
    let v = version_check(&f, &ids, "src/lib.rs").unwrap();
    let expected = format!(
        "{{\"compilerBuild\":\"{}\",\"compilerName\":\"rustc\",\"compilerVersion\":\"1.95.0\",\"dialect\":{{\"edition\":2024}},\"languageId\":\"rust\",\"schemaVersion\":1}}",
        "0".repeat(40)
    );
    assert_eq!(v.canonical_record(), expected.as_bytes());
    assert_eq!(v.record_sha256(), raw_sha256(expected.as_bytes()));
    assert_eq!(v.tool_checks().context_digest(), ids.c);
    assert_eq!(v.dialect_checks().edition(), 2024);
}
#[test]
fn language_version_changes_for_each_compiler_version_build_and_selected_edition() {
    let mut base = single();
    version_tools(&mut base);
    let ids = base.ids();
    let expected = version_check(&base, &ids, "src/lib.rs")
        .unwrap()
        .record_sha256();
    for field_name in ["rustcVersion", "rustCommitHash", "edition"] {
        let mut f = single();
        if field_name == "edition" {
            fields(&mut f.universe).insert("edition".into(), object([("owned", number(2021))]));
        } else {
            fields(fields(&mut f.context).get_mut("toolchain").unwrap()).insert(
                field_name.into(),
                if field_name == "rustcVersion" {
                    text("1.95.1")
                } else {
                    text(&"1".repeat(40))
                },
            );
        }
        version_tools(&mut f);
        let ids = f.ids();
        assert_ne!(
            version_check(&f, &ids, "src/lib.rs")
                .unwrap()
                .record_sha256(),
            expected,
            "{field_name}"
        );
    }
}
#[test]
fn language_version_excludes_declared_operational_and_resolution_inputs() {
    let mut base = single();
    version_tools(&mut base);
    let ids = base.ids();
    let expected = version_check(&base, &ids, "src/lib.rs")
        .unwrap()
        .record_sha256();
    for field_name in [
        "hostTriple",
        "targetTriple",
        "cargoVersion",
        "sysrootDigest",
    ] {
        let mut f = single();
        version_tools(&mut f);
        match field_name {
            "hostTriple" => {
                fields(&mut f.context).insert("hostTriple".into(), text("x86_64-apple-darwin"));
            }
            "targetTriple" => {
                fields(&mut f.context).insert("targetTriple".into(), text("x86_64-apple-darwin"));
                fields(fields(&mut f.context).get_mut("toolchain").unwrap())
                    .insert("targetTriple".into(), text("x86_64-apple-darwin"));
                fields(&mut f.features).insert("targetTriple".into(), text("x86_64-apple-darwin"));
            }
            "cargoVersion" => {
                fields(fields(&mut f.context).get_mut("toolchain").unwrap())
                    .insert("cargoVersion".into(), text("other-declared-cargo"));
            }
            _ => {
                fields(fields(&mut f.context).get_mut("toolchain").unwrap()).insert(
                    "sysrootDigest".into(),
                    hash_text(b"other-unadmitted-sysroot"),
                );
            }
        }
        let other = f.ids();
        assert_ne!(ids.c, other.c);
        assert_eq!(
            version_check(&f, &other, "src/lib.rs")
                .unwrap()
                .record_sha256(),
            expected,
            "{field_name}"
        );
    }
}
#[test]
fn language_version_excludes_unrelated_crates_and_agreeing_owner_count() {
    let mut base = single();
    version_tools(&mut base);
    let ids = base.ids();
    let expected = version_check(&base, &ids, "src/lib.rs")
        .unwrap()
        .record_sha256();
    let mut f = single();
    fields(&mut f.universe).insert(
        "edition".into(),
        object([("owned", number(2024)), ("unrelated", number(2015))]),
    );
    version_tools(&mut f);
    let ids = f.ids();
    assert_eq!(
        version_check(&f, &ids, "src/lib.rs")
            .unwrap()
            .record_sha256(),
        expected
    );
    let mut f = two(Some(2024), Some(2024), &[0, 1]);
    version_tools(&mut f);
    let ids = f.ids();
    let checked = version_check(&f, &ids, "src/lib.rs").unwrap();
    assert_eq!(checked.dialect_checks().selected_owner_count(), 2);
    assert_eq!(checked.record_sha256(), expected);
}
#[test]
fn language_version_never_uses_a_display_version_without_declared_closure_join() {
    let mut f = single();
    version_tools(&mut f);
    fields(fields(&mut f.context).get_mut("toolchain").unwrap())
        .insert("rustcVersion".into(), text("forged-display-version"));
    let ids = f.ids();
    assert!(matches!(
        version_check(&f, &ids, "src/lib.rs"),
        Err(BodyLanguageVersionError::Tools(
            crate::compiler_tools::CompilerToolError::CompilerVersion
        ))
    ));
}
#[test]
fn language_version_requires_retained_compiler_tools_and_dev_bytes() {
    let mut f = single();
    version_tools(&mut f);
    let ids = f.ids();
    f.blobs.remove(&raw_sha256(b"rustc"));
    assert!(matches!(
        version_check(&f, &ids, "src/lib.rs"),
        Err(BodyLanguageVersionError::Tools(
            crate::compiler_tools::CompilerToolError::Retained(_)
        ))
    ));
    let mut f = single();
    let ids = f.ids();
    assert!(matches!(
        version_check(&f, &ids, "src/lib.rs"),
        Err(BodyLanguageVersionError::Tools(
            crate::compiler_tools::CompilerToolError::Retained(_)
        ))
    ));
}
#[test]
fn language_version_keeps_ownership_refusals_before_tools_and_never_skips_uniform_maps() {
    let mut f = Fixture::new();
    let ids = f.ids();
    assert!(matches!(
        version_check(&f, &ids, "src/lib.rs"),
        Err(BodyLanguageVersionError::Dialect(
            BodyDialectError::MissingOwnership
        ))
    ));
    let mut f = two(Some(2018), Some(2024), &[0, 1]);
    fields(f.ownership.as_mut().unwrap()).insert("enumeration".into(), text("partial"));
    let ids = f.ids();
    assert!(matches!(
        version_check(&f, &ids, "src/lib.rs"),
        Err(BodyLanguageVersionError::Dialect(
            BodyDialectError::PartialEnumeration
        ))
    ));
    let mut f = two(Some(2018), Some(2024), &[0, 1]);
    version_tools(&mut f);
    let ids = f.ids();
    assert!(matches!(
        version_check(&f, &ids, "src/lib.rs"),
        Err(BodyLanguageVersionError::Dialect(
            BodyDialectError::AmbiguousEdition
        ))
    ));
}
#[test]
fn language_version_keeps_exact_selected_anchor_decision() {
    let mut f = two(Some(2018), Some(2024), &[1]);
    version_tools(&mut f);
    let ids = f.ids();
    let checked = version_check(&f, &ids, "src/lib.rs").unwrap();
    assert_eq!(checked.dialect_checks().edition(), 2024);
    assert!(matches!(
        version_check(&f, &ids, "src/lib.rs.more"),
        Err(BodyLanguageVersionError::Dialect(
            BodyDialectError::NotCompiled
        ))
    ));
}
