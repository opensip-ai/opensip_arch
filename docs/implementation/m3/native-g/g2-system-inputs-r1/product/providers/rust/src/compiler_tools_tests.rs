use super::*;
use opensip_identity::{
    IdentityCandidate, JsonInteger, ObjectInput, RegisteredSchemas, canonical_bytes, digest_hex,
    hash_preimage, raw_sha256,
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
fn row(path: &str, bytes: &[u8]) -> JsonValue {
    object([
        ("path", text(path)),
        ("sha256", hash_text(bytes)),
        ("bytes", number(bytes.len())),
    ])
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
    tools_id: String,
    dev_id: String,
}
impl Fixture {
    fn insert_closure(&mut self, descriptor: JsonValue) -> String {
        let raw = canonical_bytes(&descriptor).unwrap();
        let id = IdentityCandidate::from_json(schemas(), IdentityDomain::Closure, &raw, WORK)
            .unwrap()
            .identifier()
            .to_owned();
        self.objects.insert(
            id.clone(),
            ObjectInput {
                domain: IdentityDomain::Closure,
                descriptor,
            },
        );
        id
    }
    fn new() -> Self {
        let mut fixture = Self {
            objects: BTreeMap::new(),
            blobs: BTreeMap::new(),
            context: JsonValue::Null,
            tools_id: String::new(),
            dev_id: String::new(),
        };
        let tools: [(&str, &[u8]); 5] = [
            ("bin/ar", b"ar"),
            ("bin/cargo", b"cargo"),
            ("bin/linker", b"linker"),
            ("bin/proc", b"proc"),
            ("bin/rustc", b"rustc"),
        ];
        for (_, bytes) in tools {
            fixture.blobs.insert(raw_sha256(bytes), bytes.to_vec());
        }
        fixture
            .blobs
            .insert(raw_sha256(b"dev-library"), b"dev-library".to_vec());
        fixture
            .blobs
            .insert(raw_sha256(b"owned-manifest"), b"owned-manifest".to_vec());
        let closure = |kind, rows| {
            object([
                ("schemaVersion", number(2)),
                ("kind", text(kind)),
                ("manifestDigest", hash_text(b"owned-manifest")),
                ("tree", JsonValue::Array(rows)),
                ("semanticVersion", text("1.95.0")),
                ("protocolMajor", number(3)),
                ("platform", text("macos-aarch64")),
            ])
        };
        fixture.tools_id = fixture.insert_closure(closure(
            "toolchain",
            tools.iter().map(|(path, bytes)| row(path, bytes)).collect(),
        ));
        fixture.dev_id = fixture.insert_closure(closure(
            "rust-dev-llvm",
            vec![row("lib/dev", b"dev-library")],
        ));
        fixture.context = object([
            ("schemaVersion", number(2)),
            ("targetTriple", text("aarch64-apple-darwin")),
            ("hostTriple", text("aarch64-apple-darwin")),
            (
                "toolchain",
                object([
                    ("cargoVersion", text("1.95.0")),
                    ("rustCommitHash", text(&"0".repeat(40))),
                    (
                        "rustcDevLlvmDigest",
                        text(fixture.dev_id.strip_prefix("closure2:").unwrap()),
                    ),
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
                    ("closureId", text(&fixture.tools_id)),
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
        fixture
    }
    fn frame(&mut self) -> [u8; 32] {
        let raw = hash_preimage("native.context.rust.v2", &self.context).unwrap();
        let digest = raw_sha256(&raw);
        self.blobs.insert(digest, raw);
        digest
    }
    fn check(
        &self,
        sha: [u8; 32],
        expected: [u8; 32],
    ) -> Result<CompilerToolChecks, CompilerToolError> {
        check_declared_tools(
            &RetainedInputs::new(schemas(), &self.objects, &self.blobs),
            sha,
            expected,
            WORK,
        )
    }
    fn context_field(&mut self, parent: &str, name: &str, value: JsonValue) {
        fields(fields(&mut self.context).get_mut(parent).unwrap()).insert(name.into(), value);
    }
    fn replace_closure(&mut self, dev: bool, change: impl FnOnce(&mut JsonValue)) {
        let id = if dev { &self.dev_id } else { &self.tools_id };
        let mut descriptor = self.objects.get(id).unwrap().descriptor.clone();
        change(&mut descriptor);
        let new_id = self.insert_closure(descriptor);
        if dev {
            self.dev_id = new_id.clone();
            self.context_field(
                "toolchain",
                "rustcDevLlvmDigest",
                text(new_id.strip_prefix("closure2:").unwrap()),
            );
        } else {
            self.tools_id = new_id.clone();
            self.context_field("toolClosure", "closureId", text(&new_id));
        }
    }
}

#[test]
fn retained_declared_tool_joins_and_whole_context_digest_match() {
    let mut fixture = Fixture::new();
    let sha = fixture.frame();
    let checked = fixture.check(sha, sha).unwrap();
    assert_eq!(checked.context_digest(), sha);
    assert!(checked.linker_present());
    // Sysroot/config/dependency admissions are intentionally not established.
    assert!(
        !fixture
            .blobs
            .contains_key(&raw_sha256(b"unadmitted sysroot fixture"))
    );
}

#[test]
fn every_named_tool_must_belong_to_the_declared_tree() {
    for role in ["rustc", "cargo", "procMacroServer", "linker", "ar"] {
        let mut fixture = Fixture::new();
        fixture.context_field("toolClosure", role, hash_text(b"unselected outsider"));
        let sha = fixture.frame();
        assert!(
            matches!(fixture.check(sha, sha), Err(CompilerToolError::ToolNotInClosure(actual)) if actual == role),
            "{role}"
        );
    }
}

#[test]
fn absent_optional_tools_stay_absent_without_fallback() {
    let mut fixture = Fixture::new();
    fixture.context_field("toolClosure", "ar", JsonValue::Null);
    fixture.context_field("toolClosure", "linker", JsonValue::Null);
    let sha = fixture.frame();
    assert!(!fixture.check(sha, sha).unwrap().linker_present());
}

#[test]
fn unknown_dev_closure_is_not_a_digest_only_admission() {
    let mut fixture = Fixture::new();
    fixture.context_field("toolchain", "rustcDevLlvmDigest", text(&"a".repeat(64)));
    let sha = fixture.frame();
    assert!(matches!(
        fixture.check(sha, sha),
        Err(CompilerToolError::Retained(
            RetainedInputError::MissingObject(_)
        ))
    ));
}

#[test]
fn both_closure_kinds_are_checked_after_identity_recomputation() {
    for dev in [true, false] {
        let mut fixture = Fixture::new();
        fixture.replace_closure(dev, |descriptor| {
            fields(descriptor).insert("kind".into(), text("stdlib"));
        });
        let sha = fixture.frame();
        let expected = if dev { "rust-dev-llvm" } else { "toolchain" };
        assert!(
            matches!(fixture.check(sha, sha), Err(CompilerToolError::ClosureKind(actual)) if actual == expected)
        );
    }
}

#[test]
fn closure_descriptor_substitution_under_id_refuses() {
    let mut fixture = Fixture::new();
    fields(
        &mut fixture
            .objects
            .get_mut(&fixture.tools_id)
            .unwrap()
            .descriptor,
    )
    .insert("semanticVersion".into(), text("1.96.0"));
    let sha = fixture.frame();
    assert!(matches!(
        fixture.check(sha, sha),
        Err(CompilerToolError::Retained(
            RetainedInputError::ObjectIdentity
        ))
    ));
}

#[test]
fn all_declared_tree_and_manifest_bytes_are_required() {
    for bytes in [
        &b"owned-manifest"[..],
        &b"dev-library"[..],
        &b"ar"[..],
        &b"cargo"[..],
        &b"linker"[..],
        &b"proc"[..],
        &b"rustc"[..],
    ] {
        let mut fixture = Fixture::new();
        fixture.blobs.remove(&raw_sha256(bytes));
        let sha = fixture.frame();
        assert!(matches!(
            fixture.check(sha, sha),
            Err(CompilerToolError::Retained(
                RetainedInputError::MissingBlob(_)
            ))
        ));
    }
}

#[test]
fn retained_member_substitution_and_wrong_length_refuse() {
    let mut fixture = Fixture::new();
    fixture
        .blobs
        .insert(raw_sha256(b"dev-library"), b"changed".to_vec());
    let sha = fixture.frame();
    assert!(matches!(
        fixture.check(sha, sha),
        Err(CompilerToolError::Retained(RetainedInputError::BlobDigest))
    ));
    let mut fixture = Fixture::new();
    fixture.replace_closure(true, |descriptor| {
        let JsonValue::Array(rows) = fields(descriptor).get_mut("tree").unwrap() else {
            unreachable!()
        };
        fields(&mut rows[0]).insert("bytes".into(), number(1));
    });
    let sha = fixture.frame();
    assert!(matches!(
        fixture.check(sha, sha),
        Err(CompilerToolError::Retained(RetainedInputError::BlobLength))
    ));
}

#[test]
fn compiler_version_and_target_agreement_are_required() {
    let mut fixture = Fixture::new();
    fixture.context_field("toolchain", "rustcVersion", text("1.96.0"));
    let sha = fixture.frame();
    assert!(matches!(
        fixture.check(sha, sha),
        Err(CompilerToolError::CompilerVersion)
    ));
    let mut fixture = Fixture::new();
    fixture.context_field(
        "toolchain",
        "targetTriple",
        text("x86_64-unknown-linux-gnu"),
    );
    let sha = fixture.frame();
    assert!(matches!(
        fixture.check(sha, sha),
        Err(CompilerToolError::TargetTriple)
    ));
}

#[test]
fn host_comparison_covers_fields_beyond_the_tool_projection() {
    let mut fixture = Fixture::new();
    let old = fixture.frame();
    fields(&mut fixture.context).insert("baseCfg".into(), JsonValue::Array(vec![text("changed")]));
    let changed = fixture.frame();
    assert!(matches!(
        fixture.check(changed, old),
        Err(CompilerToolError::HostContextMismatch)
    ));
    assert_eq!(
        fixture.check(changed, changed).unwrap().context_digest(),
        changed
    );
}

#[test]
fn bad_context_shape_or_raw_frame_cannot_acquire_tool_checks() {
    let mut fixture = Fixture::new();
    fixture.context_field("toolClosure", "rustc", JsonValue::Null);
    let sha = fixture.frame();
    assert!(matches!(
        fixture.check(sha, sha),
        Err(CompilerToolError::Frame(_))
    ));
    let mut fixture = Fixture::new();
    let sha = fixture.frame();
    fixture.blobs.insert(sha, b"changed".to_vec());
    assert!(matches!(
        fixture.check(sha, sha),
        Err(CompilerToolError::Frame(_))
    ));
}

fn system_fixture(rows: &[(&str, &[u8])]) -> Fixture {
    let mut fixture = Fixture::new();
    let manifest = b"unadmitted sysroot fixture";
    fixture
        .blobs
        .insert(raw_sha256(manifest), manifest.to_vec());
    let mut components = Vec::new();
    for (name, bytes) in rows {
        fixture.blobs.insert(raw_sha256(bytes), bytes.to_vec());
        components.push(object([
            ("component", text(name)),
            ("sha256", hash_text(bytes)),
        ]));
    }
    fixture.context_field(
        "toolchain",
        "standardLibraryComponentDigests",
        JsonValue::Array(components),
    );
    fixture
}
fn system_check(
    fixture: &Fixture,
    sha: [u8; 32],
    host: [u8; 32],
) -> Result<SystemInputChecks, SystemInputError> {
    check_declared_system_inputs(
        &RetainedInputs::new(schemas(), &fixture.objects, &fixture.blobs),
        sha,
        host,
        WORK,
    )
}
#[test]
fn system_declared_preimages_and_order_are_observed_without_manifest_admission() {
    let mut f = system_fixture(&[
        ("core", b"binary\0\xff"),
        ("std", b"std"),
        ("é", b"unicode-name"),
    ]);
    let sha = f.frame();
    let checked = system_check(&f, sha, sha).unwrap();
    assert_eq!(checked.tool_checks().context_digest(), sha);
    assert_eq!(
        checked.sysroot_digest(),
        raw_sha256(b"unadmitted sysroot fixture")
    );
    assert_eq!(checked.declared_components(), 3);
    // Opaque synthetic sysroot bytes have no manifest grammar/admission here.
}
#[test]
fn system_empty_components_remain_only_an_empty_observation() {
    let mut f = system_fixture(&[]);
    let sha = f.frame();
    assert_eq!(system_check(&f, sha, sha).unwrap().declared_components(), 0);
}
#[test]
fn system_missing_and_substituted_sysroot_are_distinct_retained_errors() {
    for changed in [false, true] {
        let mut f = system_fixture(&[]);
        let key = raw_sha256(b"unadmitted sysroot fixture");
        if changed {
            f.blobs.insert(key, b"changed".to_vec());
        } else {
            f.blobs.remove(&key);
        }
        let sha = f.frame();
        let error = system_check(&f, sha, sha).unwrap_err();
        if changed {
            assert!(matches!(
                error,
                SystemInputError::Tools(CompilerToolError::Retained(
                    RetainedInputError::BlobDigest
                ))
            ));
        } else {
            assert!(
                matches!(error,SystemInputError::Tools(CompilerToolError::Retained(RetainedInputError::MissingBlob(d))) if d==key)
            );
        }
    }
}
#[test]
fn system_each_component_raw_preimage_is_required() {
    for name in ["core", "std"] {
        let mut f = system_fixture(&[("core", b"core"), ("std", b"std")]);
        let key = raw_sha256(name.as_bytes());
        f.blobs.remove(&key);
        let sha = f.frame();
        assert!(
            matches!(system_check(&f,sha,sha),Err(SystemInputError::Tools(CompilerToolError::Retained(RetainedInputError::MissingBlob(d)))) if d==key)
        );
    }
}
#[test]
fn system_substituted_component_does_not_satisfy_a_retained_digest() {
    let mut f = system_fixture(&[("core", b"core")]);
    f.blobs.insert(raw_sha256(b"core"), b"substitute".to_vec());
    let sha = f.frame();
    assert!(matches!(
        system_check(&f, sha, sha),
        Err(SystemInputError::Tools(CompilerToolError::Retained(
            RetainedInputError::BlobDigest
        )))
    ));
}
#[test]
fn system_component_order_and_duplicate_names_are_never_rewritten() {
    for rows in [
        vec![("std", b"a".as_slice()), ("core", b"b".as_slice())],
        vec![("core", b"a".as_slice()), ("core", b"b".as_slice())],
        vec![("é", b"a".as_slice()), ("z", b"b".as_slice())],
    ] {
        let mut f = system_fixture(&rows);
        let sha = f.frame();
        assert!(matches!(
            system_check(&f, sha, sha),
            Err(SystemInputError::ComponentOrder)
        ));
    }
}
#[test]
fn system_shared_digests_do_not_merge_component_declarations() {
    let mut f = system_fixture(&[("core", b"shared"), ("std", b"shared")]);
    let sha = f.frame();
    assert_eq!(system_check(&f, sha, sha).unwrap().declared_components(), 2);
}
#[test]
fn system_selected_host_context_and_tools_are_mandatory_before_byte_observation() {
    let mut f = Fixture::new();
    let sha = f.frame();
    assert!(matches!(
        system_check(&f, sha, [0; 32]),
        Err(SystemInputError::Tools(
            CompilerToolError::HostContextMismatch
        ))
    ));
    f.context_field("toolClosure", "rustc", hash_text(b"outsider"));
    let sha = f.frame();
    assert!(matches!(
        system_check(&f, sha, sha),
        Err(SystemInputError::Tools(
            CompilerToolError::ToolNotInClosure("rustc")
        ))
    ));
}
#[test]
fn system_full_context_frame_digest_shape_and_component_ceiling_still_refuse() {
    let mut f = system_fixture(&[]);
    let sha = f.frame();
    f.blobs.get_mut(&sha).unwrap().push(b' ');
    assert!(matches!(
        system_check(&f, sha, sha),
        Err(SystemInputError::Tools(CompilerToolError::Frame(_)))
    ));
    let mut f = system_fixture(&[]);
    f.context_field(
        "toolchain",
        "standardLibraryComponentDigests",
        JsonValue::Bool(false),
    );
    let sha = f.frame();
    assert!(matches!(
        system_check(&f, sha, sha),
        Err(SystemInputError::Tools(CompilerToolError::Frame(_)))
    ));
    let mut f = system_fixture(&[]);
    f.context_field(
        "toolchain",
        "standardLibraryComponentDigests",
        JsonValue::Array(
            (0..65)
                .map(|i| {
                    object([
                        ("component", text(&format!("c{i:02}"))),
                        ("sha256", hash_text(b"member")),
                    ])
                })
                .collect(),
        ),
    );
    let sha = f.frame();
    assert!(matches!(
        system_check(&f, sha, sha),
        Err(SystemInputError::Tools(CompilerToolError::Frame(_)))
    ));
}
