// C2a-1's controls (C2a plan r4, section 4): the candidate for every role,
// the platform join, C2PM-1's guards and origins, the hand encoder against
// the real canonical encoder, the charged merge sort, the published prices
// and the size boundary. Every ledger here is an explicitly identified test
// scope, never evidence for a production profile (Q5 ruling).
use super::*;
use crate::trust::TestComponent;
use opensip_identity::{
    JsonInteger, canonical_bytes, digest_hex, hash_canonical_value, parse_json,
};
use opensip_platform::{WorkBudgetError, WorkLedger};
use std::sync::OnceLock;

const ROLES: [&str; 5] = [
    "analyzer",
    "toolchain",
    "stdlib",
    "rust-dev-llvm",
    "grammar",
];
const MACOS_ARM64: SelectedPlatform<'static> = SelectedPlatform {
    os: "macos",
    arch: "arm64",
};
/// A stand-in for the verified envelope; C2a-2's signed fixtures carry real ones.
const ENVELOPE: &[u8] = br#"{"test":"envelope stand-in"}"#;

/// The registered schemas, read from the repository's sources once.
pub(crate) fn registry() -> &'static RegisteredSchemas {
    static REGISTRY: OnceLock<RegisteredSchemas> = OnceLock::new();
    REGISTRY.get_or_init(|| {
        let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("../..");
        let raw: Vec<Vec<u8>> = RegisteredSchemas::source_requirements()
            .iter()
            .map(|p| std::fs::read(root.join(p.source_path())).unwrap())
            .collect();
        let refs: Vec<&[u8]> = raw.iter().map(Vec::as_slice).collect();
        RegisteredSchemas::from_sources(&refs).unwrap()
    })
}
/// The platform ledger's default caps, as an explicitly identified test scope.
fn test_ledger() -> WorkLedger {
    WorkLedger::new()
}
fn int(n: i128) -> V {
    V::Integer(JsonInteger::new(n).unwrap())
}
fn obj(v: &mut V) -> &mut BTreeMap<String, V> {
    let V::Object(m) = v else { panic!("object") };
    m
}
fn get<'v>(v: &'v V, key: &str) -> &'v V {
    let V::Object(m) = v else { panic!("object") };
    &m[key]
}
fn list(v: &V) -> &[V] {
    let V::Array(a) = v else { panic!("array") };
    a
}
fn string(v: &V) -> &str {
    let V::String(s) = v else { panic!("string") };
    s
}
/// CR-1's baseline body (`manifest268-semantic.ndjson`, `POS/full-security`),
/// made role-valid as `component_manifest.rs`'s `cr1_body` makes it, with
/// C2PM-1's declaration when `major` is given.
fn body(role: &str, major: Option<i128>) -> V {
    let line = include_bytes!("../tests/fixtures/manifest268-semantic.ndjson")
        .split(|b| *b == b'\n')
        .find(|b| !b.is_empty())
        .unwrap();
    let q = parse_json(line).unwrap();
    assert_eq!(string(get(&q, "label")), "POS/full-security");
    let hex = string(get(&q, "raw"));
    let raw: Vec<u8> = (0..hex.len())
        .step_by(2)
        .map(|i| u8::from_str_radix(&hex[i..i + 2], 16).unwrap())
        .collect();
    let mut v = parse_json(&raw).unwrap();
    let m = obj(&mut v);
    m.insert("role".to_owned(), V::String(role.to_owned()));
    if role != "analyzer" {
        m.remove("commands");
        m.insert("capabilities".to_owned(), V::Array(vec![]));
        m.insert("permissions".to_owned(), V::Array(vec![]));
    }
    if let Some(major) = major {
        m.insert("closureProtocolMajor".to_owned(), int(major));
    }
    v
}
fn provider_protocol(body: &V) -> i128 {
    let V::Integer(n) = get(get(body, "compatibility"), "providerProtocol") else {
        panic!("integer")
    };
    n.get()
}
/// The selected `{macos, arm64}` row's entries.
fn entries(body: &mut V) -> &mut Vec<V> {
    let V::Array(platforms) = obj(body).get_mut("platforms").unwrap() else {
        panic!("platforms")
    };
    let tree = obj(&mut platforms[0]).get_mut("tree").unwrap();
    let V::Array(entries) = obj(tree).get_mut("entries").unwrap() else {
        panic!("entries")
    };
    entries
}
/// A catalog release row of the recovery catalog's shape, one artifact per
/// token, bound to the body's digest.
fn release(raw: &[u8], tokens: &[&str]) -> V {
    let z = "0".repeat(64);
    let artifacts: Vec<String> = tokens
        .iter()
        .map(|t| {
            format!(
                r#"{{"archiveDigest":"{z}","archiveProfileId":"p1","platform":"{t}","sha256":"{z}"}}"#
            )
        })
        .collect();
    parse_json(
        format!(
            r#"{{"artifacts":[{}],"envelopeDigest":"{}","hostCoreConstraint":{{"includeMax":false,"includeMin":true,"max":"0.2.0","min":"0.1.0"}},"manifestDigest":"{}","manifestPreimageSha256":"{z}","publisher":"opensip","sourceClass":"first-party","stableId":"6f1c2c3e-0b6a-4a1c-9c2d-1f0e2a3b4c5d","version":"1.0.0"}}"#,
            artifacts.join(","),
            digest_hex(&raw_sha256(ENVELOPE)),
            digest_hex(&raw_sha256(raw)),
        )
        .as_bytes(),
    )
    .unwrap()
}
fn component(body: &V, tokens: &[&str]) -> TestComponent {
    let raw = canonical_bytes(body).unwrap();
    let release = release(&raw, tokens);
    TestComponent::new(raw, ENVELOPE.to_vec(), release).expect("a valid body")
}
fn candidate<'a>(
    c: &'a TestComponent,
    platform: SelectedPlatform<'_>,
    analyzer: Option<&AnalyzerSubprotocol>,
    ledger: &mut WorkLedger,
) -> Result<ClosureCandidate<'a>, ClosureFailure> {
    let authenticated = c.authenticated();
    ledger.scope(|work| component_candidate(&authenticated, platform, analyzer, registry(), work))
}
fn refusal<T>(result: Result<T, ClosureFailure>) -> ClosureRefusal {
    match result {
        Err(WorkFailure::Operation(refusal)) => refusal,
        Err(WorkFailure::Budget(budget)) => panic!("budget {budget:?}"),
        Ok(_) => panic!("admitted"),
    }
}
fn subprotocol_for(body: &V) -> AnalyzerSubprotocol {
    AnalyzerSubprotocol::selected_for_tests(provider_protocol(body) as u64)
}
fn analyzer_for<'s>(
    role: &str,
    selected: &'s AnalyzerSubprotocol,
) -> Option<&'s AnalyzerSubprotocol> {
    (role == "analyzer").then_some(selected)
}
fn declared(role: &str, body: &V) -> i128 {
    if role == "analyzer" {
        provider_protocol(body)
    } else {
        1
    }
}
/// The expected descriptor, built as a value and encoded by the real
/// canonical encoder: the selected row's regular files, path-sorted.
fn expected(kind: &str, raw: &[u8], major: i128, version: &str, body: &V) -> V {
    let mut tree: Vec<(String, String, i128)> = list(get(
        get(&list(get(body, "platforms"))[0], "tree"),
        "entries",
    ))
    .iter()
    .filter(|e| string(get(e, "type")) == "file")
    .map(|e| {
        let V::Integer(n) = get(e, "length") else {
            panic!("length")
        };
        (
            string(get(e, "path")).to_owned(),
            string(get(e, "sha256")).to_owned(),
            n.get(),
        )
    })
    .collect();
    tree.sort();
    descriptor_value(
        kind,
        &digest_hex(&raw_sha256(raw)),
        "macos-arm64",
        major,
        version,
        &tree,
    )
}
fn descriptor_value(
    kind: &str,
    digest: &str,
    platform: &str,
    major: i128,
    version: &str,
    tree: &[(String, String, i128)],
) -> V {
    V::Object(BTreeMap::from_iter([
        ("kind".to_owned(), V::String(kind.to_owned())),
        ("manifestDigest".to_owned(), V::String(digest.to_owned())),
        ("platform".to_owned(), V::String(platform.to_owned())),
        ("protocolMajor".to_owned(), int(major)),
        ("schemaVersion".to_owned(), int(2)),
        ("semanticVersion".to_owned(), V::String(version.to_owned())),
        (
            "tree".to_owned(),
            V::Array(
                tree.iter()
                    .map(|(path, sha, bytes)| {
                        V::Object(BTreeMap::from_iter([
                            ("bytes".to_owned(), int(*bytes)),
                            ("path".to_owned(), V::String(path.clone())),
                            ("sha256".to_owned(), V::String(sha.clone())),
                        ]))
                    })
                    .collect(),
            ),
        ),
    ]))
}

/// C2-T6's C2a-1 leg and LD-C2A-2 to -4: every role's role-valid body, with
/// C2PM-1's declaration, yields a candidate whose descriptor is exactly the
/// canonical one and whose id is `closure2:` + H("closure", D). The body's
/// entries are reversed and a symlink row is added, so the order is the
/// projection's own and no `dir` or `symlink` row is a Blob (C2-T4).
#[test]
fn c2a1_every_role_projects_its_exact_candidate() {
    for role in ROLES {
        let mut b = body(role, None);
        let major = declared(role, &b);
        obj(&mut b).insert("closureProtocolMajor".to_owned(), int(major));
        entries(&mut b).reverse();
        entries(&mut b).push(
            parse_json(
                br#"{"mode":"0755","path":"lib/alias.js","target":"provider.js","type":"symlink"}"#,
            )
            .unwrap(),
        );
        let c = component(&b, &["linux-x86_64", "macos-arm64"]);
        let selected = subprotocol_for(&b);
        let mut ledger = test_ledger();
        let got = candidate(&c, MACOS_ARM64, analyzer_for(role, &selected), &mut ledger)
            .unwrap_or_else(|f| panic!("{role}: {f:?}"));
        let kind = match role {
            "analyzer" => "provider",
            other => other,
        };
        let raw = canonical_bytes(&b).unwrap();
        let want = expected(kind, &raw, major, string(get(&b, "version")), &b);
        assert_eq!(got.descriptor(), canonical_bytes(&want).unwrap(), "{role}");
        assert_eq!(
            got.closure(),
            format!(
                "closure2:{}",
                digest_hex(&hash_canonical_value("closure", &want).unwrap())
            ),
            "{role}"
        );
        assert_eq!(got.manifest_digest(), raw_sha256(&raw), "{role}");
        assert_ne!(got.manifest_digest(), raw_sha256(ENVELOPE), "{role}");
        let paths: Vec<&str> = got.blobs().map(BlobRef::path).collect();
        assert_eq!(
            paths,
            ["bin/entry", "lib/provider.js", "runtime/node"],
            "{role}"
        );
        assert!(
            got.blobs()
                .all(|blob| blob.sha256().len() == 64 && blob.bytes() > 0)
        );
    }
}

/// C2-T5: the same tree under a changed version is a new `closure2`.
#[test]
fn c2a1_changed_version_is_a_new_closure() {
    let mut ids = Vec::new();
    for version in ["1.0.0", "1.0.1"] {
        let mut b = body("toolchain", Some(1));
        obj(&mut b).insert("version".to_owned(), V::String(version.to_owned()));
        let c = component(&b, &["macos-arm64"]);
        let got = candidate(&c, MACOS_ARM64, None, &mut test_ledger()).unwrap();
        ids.push(got.closure().to_owned());
    }
    assert_ne!(ids[0], ids[1]);
}

/// C2-T1's platform legs and NBO-1: a missing `{os, arch}` row, a token the
/// catalog does not admit (a core-inventory spelling), and a release with no
/// artifact of the joined token each refuse `Platform`. The closure's
/// platform is the catalog token.
#[test]
fn c2a1_platform_join_is_closed() {
    let b = body("toolchain", Some(1));
    let c = component(&b, &["macos-arm64"]);
    let missing = SelectedPlatform {
        os: "linux",
        arch: "arm64",
    };
    assert_eq!(
        refusal(candidate(&c, missing, None, &mut test_ledger())),
        ClosureRefusal::Platform
    );
    let other = component(&b, &["linux-arm64", "macos-x86_64"]);
    assert_eq!(
        refusal(candidate(&other, MACOS_ARM64, None, &mut test_ledger())),
        ClosureRefusal::Platform
    );
    let none = component(&b, &[]);
    assert_eq!(
        refusal(candidate(&none, MACOS_ARM64, None, &mut test_ledger())),
        ClosureRefusal::Platform
    );
    // The core inventory's spelling (`core_authentication.rs`, "macos-aarch64")
    // is never a catalog token, even when a release row names it.
    let mut core = body("toolchain", Some(1));
    let V::Array(platforms) = obj(&mut core).get_mut("platforms").unwrap() else {
        panic!("platforms")
    };
    obj(&mut platforms[0]).insert("arch".to_owned(), V::String("aarch64".to_owned()));
    let spelled = component(&core, &["macos-aarch64", "macos-arm64"]);
    let aarch64 = SelectedPlatform {
        os: "macos",
        arch: "aarch64",
    };
    assert_eq!(
        refusal(candidate(&spelled, aarch64, None, &mut test_ledger())),
        ClosureRefusal::Platform
    );
    let got = candidate(&c, MACOS_ARM64, None, &mut test_ledger()).unwrap();
    let admitted = parse_json(got.descriptor()).unwrap();
    assert_eq!(string(get(&admitted, "platform")), "macos-arm64");
}

/// The four tokens are the catalog's own (`recovery_catalog.rs`, `artifact`).
#[test]
fn c2a1_platform_tokens_are_the_catalogs() {
    let catalog = include_str!("trust/recovery_catalog.rs");
    assert!(catalog.contains(
        r#"["macos-arm64", "macos-x86_64", "linux-arm64", "linux-x86_64"].contains(&s)"#
    ));
    assert_eq!(
        PLATFORMS,
        ["macos-arm64", "macos-x86_64", "linux-arm64", "linux-x86_64"]
    );
}

/// C2PM-1 through the whole path: an absent declaration on a body that
/// validated refuses at projection; a non-analyzer major other than 1, and
/// an analyzer with no selected subprotocol or a different one, are
/// unsupported; an analyzer major equal to its subprotocol admits; nothing
/// is inferred from `compatibility.providerProtocol`.
#[test]
fn c2a1_c2pm_guards_through_the_projection() {
    let external = ProtocolOrigin::AuthenticatedReleaseDeclaration;
    for role in ROLES {
        let absent = body(role, None);
        let selected = subprotocol_for(&absent);
        let c = component(&absent, &["macos-arm64"]);
        assert_eq!(
            refusal(candidate(
                &c,
                MACOS_ARM64,
                analyzer_for(role, &selected),
                &mut test_ledger()
            )),
            ClosureRefusal::Protocol {
                key: ProtocolKey::DeclarationMissing,
                origin: external
            },
            "{role}"
        );
    }
    for major in [2, 9_223_372_036_854_775_807] {
        let c = component(&body("grammar", Some(major)), &["macos-arm64"]);
        assert_eq!(
            refusal(candidate(&c, MACOS_ARM64, None, &mut test_ledger())),
            ClosureRefusal::Protocol {
                key: ProtocolKey::Unsupported,
                origin: external
            }
        );
    }
    let analyzer = body("analyzer", None);
    let major = provider_protocol(&analyzer);
    let declared = body("analyzer", Some(major));
    let c = component(&declared, &["macos-arm64"]);
    for selected in [
        None,
        Some(AnalyzerSubprotocol::selected_for_tests(major as u64 + 1)),
    ] {
        assert_eq!(
            refusal(candidate(
                &c,
                MACOS_ARM64,
                selected.as_ref(),
                &mut test_ledger()
            )),
            ClosureRefusal::Protocol {
                key: ProtocolKey::Unsupported,
                origin: external
            }
        );
    }
    let selected = AnalyzerSubprotocol::selected_for_tests(major as u64);
    assert!(candidate(&c, MACOS_ARM64, Some(&selected), &mut test_ledger()).is_ok());
    // A toolchain's providerProtocol is not its closure protocol.
    let mut b = body("toolchain", Some(1));
    let V::Object(compat) = obj(&mut b).get_mut("compatibility").unwrap() else {
        panic!("compatibility")
    };
    compat.insert("providerProtocol".to_owned(), int(7));
    let c = component(&b, &["macos-arm64"]);
    let got = candidate(&c, MACOS_ARM64, None, &mut test_ledger()).unwrap();
    let V::Integer(copied) = get(&parse_json(got.descriptor()).unwrap(), "protocolMajor").clone()
    else {
        panic!("integer")
    };
    assert_eq!(copied.get(), 1);
}

/// C2PM-1's guard order and origins (LD-C2A-11), over each guard's inputs:
/// each guard in order, combined failures pick the first, an unsupported
/// major on a mismatched descriptor is descriptor-mismatch, and only the
/// host's own descriptor is a host bug.
#[test]
fn c2a1_c2pm_guard_order_and_origins() {
    let external = ProtocolOrigin::AuthenticatedReleaseDeclaration;
    let host = ProtocolOrigin::HostGeneratedInternalLayer;
    let first = |r: Result<u64, ClosureFailure>| refusal(r);
    // Guard 1 precedes guard 2: an analyzer with no declaration is missing.
    assert_eq!(
        first(declared_major("analyzer", None, 1)),
        ClosureRefusal::Protocol {
            key: ProtocolKey::DeclarationMissing,
            origin: external
        }
    );
    // Guard 2, whatever the support table would say of the major.
    for major in [2, 1] {
        assert_eq!(
            first(declared_major("analyzer", Some(major), major + 1)),
            ClosureRefusal::Protocol {
                key: ProtocolKey::AnalyzerMismatch,
                origin: external
            }
        );
    }
    // Guard 2 is the analyzer's alone.
    assert_eq!(declared_major("toolchain", Some(1), 2).unwrap(), 1);
    assert_eq!(declared_major("analyzer", Some(3), 3).unwrap(), 3);
    // Guard 3 precedes guard 4, and is the host's, whether or not an
    // analyzer subprotocol is selected: an unsupported major on a mismatched
    // descriptor is descriptor-mismatch.
    let selected = AnalyzerSubprotocol::selected_for_tests(3);
    for (role, major, descriptor) in [
        ("toolchain", 2, Some(1)),
        ("toolchain", 1, Some(2)),
        ("toolchain", 1, None),
        ("grammar", 2, None),
        ("analyzer", 4, Some(3)),
        ("analyzer", 3, Some(4)),
    ] {
        for analyzer in [None, Some(&selected)] {
            assert_eq!(
                refusal(admitted_major(role, major, descriptor, analyzer)),
                ClosureRefusal::Protocol {
                    key: ProtocolKey::DescriptorMismatch,
                    origin: host
                },
                "{role} {major}"
            );
        }
    }
    // Guard 4: the role table, with no numeric union and no cross-role
    // equivalence.
    for role in ["toolchain", "stdlib", "rust-dev-llvm", "grammar"] {
        assert!(admitted_major(role, 1, Some(1), None).is_ok());
        assert_eq!(
            refusal(admitted_major(role, 3, Some(3), Some(&selected))),
            ClosureRefusal::Protocol {
                key: ProtocolKey::Unsupported,
                origin: external
            }
        );
    }
    assert!(admitted_major("analyzer", 3, Some(3), Some(&selected)).is_ok());
    for (major, analyzer) in [(1, None), (3, None), (1, Some(&selected))] {
        assert_eq!(
            refusal(admitted_major(
                "analyzer",
                major,
                Some(major as i128),
                analyzer
            )),
            ClosureRefusal::Protocol {
                key: ProtocolKey::Unsupported,
                origin: external
            }
        );
    }
}

/// R3-RF-1: the hand encoder equals `canonical_bytes` over every escape
/// class, non-ASCII, and the widest integers (`bytes` 2^64 − 1,
/// `protocolMajor` 2^63 − 1), at exactly the predicted length; and the size
/// vectors of LD-C2A-3's formula.
#[test]
fn c2a1_hand_encoder_equals_the_canonical_encoder() {
    let digest = [0x5au8; 32];
    let sha = "ab".repeat(32);
    type Case<'a> = (&'a str, u64, Vec<(&'a str, u64)>);
    let cases: Vec<Case<'_>> = vec![
        ("1.0.0", 1, vec![]),
        ("1.0.0", 1, vec![("p", 0)]),
        (
            "1.0.0-rc.1",
            9_223_372_036_854_775_807,
            vec![("日本/語.wasm", 123_456_789_012)],
        ),
        (
            "v\"\\\u{8}\u{c}\n\r\t\u{0}\u{1f}\u{7f}é",
            42,
            vec![
                ("a", 0),
                ("lib/é\"q\\\n\u{1f}.js", u64::MAX),
                ("z\u{8}\u{c}\r\t\u{1}", 7),
            ],
        ),
    ];
    for (version, major, tree) in cases {
        let blobs: Vec<BlobRef<'_>> = tree
            .iter()
            .map(|(path, bytes)| BlobRef {
                path,
                sha256: &sha,
                bytes: *bytes,
            })
            .collect();
        let order: Vec<u32> = (0..blobs.len() as u32).collect();
        let fields = Fields {
            kind: "provider",
            manifest_digest: hex_digits(&digest),
            platform: "macos-arm64",
            protocol_major: major,
            semantic_version: version,
        };
        let length = descriptor_len(&fields, &blobs);
        let mut out = Vec::with_capacity(length);
        push_descriptor(&mut out, &fields, &blobs, &order);
        let rows: Vec<(String, String, i128)> = tree
            .iter()
            .map(|(p, b)| ((*p).to_owned(), sha.clone(), *b as i128))
            .collect();
        let value = descriptor_value(
            "provider",
            &digest_hex(&digest),
            "macos-arm64",
            major as i128,
            version,
            &rows,
        );
        let canonical = canonical_bytes(&value).unwrap();
        assert_eq!(out, canonical, "{version}");
        assert_eq!((out.len(), out.capacity()), (length, length), "{version}");
    }
    // A Blob with `bytes` 0 and path `p` is 98 bytes: the one-Blob
    // descriptor less the empty one.
    let one = BlobRef {
        path: "p",
        sha256: &sha,
        bytes: 0,
    };
    let fields = Fields {
        kind: "provider",
        manifest_digest: hex_digits(&digest),
        platform: "macos-arm64",
        protocol_major: 1,
        semantic_version: "1.0.0",
    };
    assert_eq!(
        descriptor_len(&fields, std::slice::from_ref(&one)) - descriptor_len(&fields, &[]),
        98
    );
    assert_eq!(
        hex_digits(&digest).as_slice(),
        digest_hex(&digest).as_bytes()
    );
}

fn reference(n: usize, f: impl Fn(usize) -> usize) -> Vec<Vec<u8>> {
    (0..n)
        .map(|i| format!("p{:06}", f(i)).into_bytes())
        .collect()
}
fn orders(n: usize) -> Vec<(&'static str, Vec<Vec<u8>>)> {
    vec![
        ("reverse", reference(n, |i| n - i)),
        ("sorted", reference(n, |i| i)),
        (
            "interleaved",
            reference(n, |i| if i % 2 == 0 { i } else { n + i }),
        ),
        ("pseudo-random", reference(n, |i| (i * 7919 + 13) % (n * 3))),
    ]
}
/// Runs the production sort over `keys` with exactly `edges` edges, counting
/// the comparisons it actually makes.
fn sort_with(keys: &[Vec<u8>], edges: usize) -> (Result<Vec<u32>, WorkFailure<()>>, usize) {
    let n = keys.len();
    // One edge is spent first, so an allowance of zero comparisons is a
    // valid ledger.
    let mut ledger = WorkLedger::with_limits(WorkCost {
        objects: 2,
        edges: edges + 1,
        bytes: 2 * n * size_of::<u32>(),
    })
    .unwrap();
    let mut made = 0;
    let result = ledger.scope(|work| {
        work.charge(COMPARISON_COST)?;
        merge_sort(n as u32, work, |a, b| {
            made += 1;
            keys[a as usize] < keys[b as usize]
        })
    });
    (result, made)
}
/// R3-RF-2 and its NBO: each order sorts completely within n·⌈log₂ n⌉
/// comparisons; r3's old estimate, n·⌈log₂(n + 1)⌉, is sufficient and
/// succeeds; an allowance one comparison short stops with `Budget` before
/// the unfunded comparison and makes none past its funding.
#[test]
fn c2a1_merge_sort_is_charged_and_bounded() {
    for n in [2usize, 3, 7, 20, 21, 33, 64, 100, 1000, 4097] {
        for (name, keys) in orders(n) {
            let (sorted, made) = sort_with(&keys, sort_reference_comparisons(n));
            let order = sorted.unwrap();
            assert!(
                order
                    .windows(2)
                    .all(|w| keys[w[0] as usize] <= keys[w[1] as usize])
            );
            assert!(made <= sort_reference_comparisons(n), "{name} {n}: {made}");
            if n == 20 && name == "reverse" {
                assert_eq!((made, sort_reference_comparisons(20)), (40, 100));
            }
            let old = n * (usize::BITS - n.leading_zeros()) as usize;
            assert!(old >= made);
            let (sufficient, again) = sort_with(&keys, old);
            assert_eq!((sufficient.unwrap(), again), (order, made), "{name} {n}");
            let (short, partial) = sort_with(&keys, made - 1);
            assert_eq!(
                short,
                Err(WorkFailure::Budget(WorkBudgetError::Edges)),
                "{name} {n}"
            );
            assert_eq!(partial, made - 1, "{name} {n}");
        }
    }
}

/// The duplicate pass refuses `Tree` on constructed input (the body reader
/// already refuses duplicate paths, so a real body never reaches it).
#[test]
fn c2a1_duplicate_paths_refuse_tree() {
    let sha = "0".repeat(64);
    let blobs = [
        BlobRef {
            path: "b",
            sha256: &sha,
            bytes: 1,
        },
        BlobRef {
            path: "a",
            sha256: &sha,
            bytes: 1,
        },
        BlobRef {
            path: "b",
            sha256: &sha,
            bytes: 2,
        },
    ];
    let mut ledger = test_ledger();
    assert_eq!(
        refusal(ledger.scope(|work| ordered(&blobs, work))),
        ClosureRefusal::Tree
    );
    let mut ledger = test_ledger();
    let order = ledger.scope(|work| ordered(&blobs[..2], work)).unwrap();
    assert_eq!(order, [1, 0]);
    // An empty projection (a row of directories only) orders at no edge cost.
    let mut ledger = test_ledger();
    assert!(ledger.scope(|work| ordered(&[], work)).unwrap().is_empty());
    assert_eq!(ledger.used(), sort_buffers_cost(0));
    assert_eq!(sort_reference_comparisons(0), 0);
    assert_eq!(sort_reference_comparisons(1), 0);
}

/// The published price of one candidate: every charge, with the sort's
/// comparisons counted by running the production sort over the same paths.
fn price(c: &TestComponent, body: &V) -> (WorkCost, usize) {
    let all = list(get(
        get(&list(get(body, "platforms"))[0], "tree"),
        "entries",
    ));
    let files: Vec<Vec<u8>> = all
        .iter()
        .filter(|e| string(get(e, "type")) == "file")
        .map(|e| string(get(e, "path")).as_bytes().to_vec())
        .collect();
    let (_, comparisons) = sort_with(&files, sort_reference_comparisons(files.len()));
    let got = candidate(c, MACOS_ARM64, None, &mut test_ledger()).unwrap();
    let d = got.descriptor().len();
    let mut total = WorkCost::default();
    for cost in [
        visit_cost(all.len()),
        projection_cost(files.len()),
        visit_cost(all.len()),
        sort_buffers_cost(files.len()),
        WorkCost {
            edges: comparisons,
            ..WorkCost::default()
        },
        duplicate_pass_cost(files.len()),
        digest_cost(canonical_bytes(body).unwrap().len()),
        encoding_cost(d),
        ID_COST,
    ] {
        total = total.checked_add(cost).unwrap();
    }
    (total, d)
}

/// R3-RF-1's funding control and RF-4's ledger: the charge equals the
/// published prices; a scope funded with exactly that price succeeds; one
/// short by one byte or one object at the descriptor's buffer refuses
/// `Budget` before the buffer exists, with nothing more charged.
#[test]
fn c2a1_charge_is_the_published_price_and_exactly_funded() {
    let mut b = body("stdlib", Some(1));
    entries(&mut b).reverse();
    let c = component(&b, &["macos-arm64"]);
    let (total, d) = price(&c, &b);
    let mut ledger = test_ledger();
    candidate(&c, MACOS_ARM64, None, &mut ledger).unwrap();
    assert_eq!(ledger.used(), total);
    let mut exact = WorkLedger::with_limits(total).unwrap();
    assert!(candidate(&c, MACOS_ARM64, None, &mut exact).is_ok());
    assert_eq!(exact.used(), total);
    let before = WorkCost {
        objects: total.objects - encoding_cost(d).objects - ID_COST.objects,
        edges: total.edges,
        bytes: total.bytes - encoding_cost(d).bytes - ID_COST.bytes,
    };
    for (short, budget) in [
        (
            WorkCost {
                bytes: before.bytes + d - 1,
                ..total
            },
            WorkBudgetError::Bytes,
        ),
        (
            WorkCost {
                objects: before.objects,
                ..total
            },
            WorkBudgetError::Objects,
        ),
    ] {
        let mut ledger = WorkLedger::with_limits(short).unwrap();
        assert!(matches!(
            candidate(&c, MACOS_ARM64, None, &mut ledger),
            Err(WorkFailure::Budget(got)) if got == budget
        ));
        assert_eq!(ledger.used(), before, "{budget:?}");
    }
    // One object short at the id record, after the descriptor.
    let mut ledger = WorkLedger::with_limits(WorkCost {
        objects: total.objects - 1,
        ..total
    })
    .unwrap();
    assert!(matches!(
        candidate(&c, MACOS_ARM64, None, &mut ledger),
        Err(WorkFailure::Budget(WorkBudgetError::Objects))
    ));
    assert_eq!(ledger.used(), before.checked_add(encoding_cost(d)).unwrap());
}

/// RF-4: the prices add up across components in one scope, and exhaustion
/// partway through the second component is `Budget`, never truncation.
#[test]
fn c2a1_aggregate_exhaustion_in_the_second_component() {
    let first = body("toolchain", Some(1));
    let second = body("grammar", Some(1));
    let (a, b) = (
        component(&first, &["macos-arm64"]),
        component(&second, &["macos-arm64"]),
    );
    let (pa, _) = price(&a, &first);
    let (pb, _) = price(&b, &second);
    let mut ledger = WorkLedger::with_limits(pa.checked_add(pb).unwrap()).unwrap();
    assert!(candidate(&a, MACOS_ARM64, None, &mut ledger).is_ok());
    assert!(candidate(&b, MACOS_ARM64, None, &mut ledger).is_ok());
    assert_eq!(ledger.used(), pa.checked_add(pb).unwrap());
    let mut ledger = WorkLedger::with_limits(WorkCost {
        edges: pa.edges + pb.edges / 2,
        ..pa.checked_add(pb).unwrap()
    })
    .unwrap();
    assert!(candidate(&a, MACOS_ARM64, None, &mut ledger).is_ok());
    assert!(matches!(
        candidate(&b, MACOS_ARM64, None, &mut ledger),
        Err(WorkFailure::Budget(WorkBudgetError::Edges))
    ));
}

/// R2-RF-1's feasible boundary at the real encoder's edge: a real unique tree
/// of 20-byte paths at the largest row count that fits admits through
/// `$defs/closure`; the descriptor at exactly 4 MiB admits, and one byte
/// over refuses `Encoding` before any buffer is charged or allocated.
#[test]
fn c2a1_descriptor_boundary_at_the_encoder_edge() {
    let sha = "0".repeat(64);
    let fields = Fields {
        kind: "toolchain",
        manifest_digest: hex_digits(&[0x11; 32]),
        platform: "macos-arm64",
        protocol_major: 1,
        semantic_version: "1.0.0",
    };
    let paths: Vec<String> = (0..40_000).map(|i| format!("{i:020}")).collect();
    let blobs = |n: usize| -> Vec<BlobRef<'_>> {
        paths[..n]
            .iter()
            .map(|path| BlobRef {
                path,
                sha256: &sha,
                bytes: 0,
            })
            .collect()
    };
    // The largest row count that fits, by bisection over the real formula.
    let (mut n, mut over) = (0, paths.len());
    while over - n > 1 {
        let mid = (n + over) / 2;
        if descriptor_len(&fields, &blobs(mid)) <= MAX_BYTES {
            n = mid;
        } else {
            over = mid;
        }
    }
    assert!(descriptor_len(&fields, &blobs(over)) > MAX_BYTES && over == n + 1);
    let fit = blobs(n);
    let slack = MAX_BYTES - descriptor_len(&fields, &fit);
    assert!(slack < 118, "{n} {slack}");
    let order: Vec<u32> = (0..n as u32).collect();
    let admit = |blobs: &[BlobRef<'_>], order: &[u32]| {
        let mut ledger = test_ledger();
        let result = ledger.scope(|work| {
            admit_descriptor(&fields, blobs, order, registry(), work).map(|(d, _)| d.len())
        });
        (result, ledger.used())
    };
    assert!(admit(&fit, &order).0.is_ok(), "{n} rows");
    // The last path lengthened by the slack: exactly 4 MiB, then one over.
    let last = format!("{}{}", paths[n - 1], "x".repeat(slack));
    let over = format!("{}{}", paths[n - 1], "x".repeat(slack + 1));
    for (path, admits) in [(&last, true), (&over, false)] {
        let mut edge = blobs(n - 1);
        edge.push(BlobRef {
            path,
            sha256: &sha,
            bytes: 0,
        });
        let (result, used) = admit(&edge, &order);
        if admits {
            assert_eq!(result.unwrap(), MAX_BYTES);
            assert_eq!(used, encoding_cost(MAX_BYTES));
        } else {
            assert_eq!(refusal(result), ClosureRefusal::Encoding);
            assert_eq!(used, WorkCost::default());
        }
    }
    // One more row than fits refuses `Encoding`, uncharged.
    let more = blobs(n + 1);
    let more_order: Vec<u32> = (0..n as u32 + 1).collect();
    let (result, used) = admit(&more, &more_order);
    assert_eq!(refusal(result), ClosureRefusal::Encoding);
    assert_eq!(used, WorkCost::default());
}

/// RF-4's count legs, labelled: on constructed input, 100,000 and 100,001
/// minimal Blobs both exceed the 4 MiB descriptor, so the schema's
/// `maxItems` of 100,000 is never reached through identity admission and
/// `Encoding` refuses first; upstream, a signed body of 100,001 entries is
/// refused by the reader's body validation before any projection.
#[test]
fn c2a1_count_predicate_on_constructed_input() {
    let sha = "0".repeat(64);
    let fields = Fields {
        kind: "grammar",
        manifest_digest: hex_digits(&[0; 32]),
        platform: "linux-x86_64",
        protocol_major: 1,
        semantic_version: "1",
    };
    let paths: Vec<String> = (0..100_001).map(|i| format!("{i}")).collect();
    for n in [100_000, 100_001] {
        let blobs: Vec<BlobRef<'_>> = paths[..n]
            .iter()
            .map(|path| BlobRef {
                path,
                sha256: &sha,
                bytes: 0,
            })
            .collect();
        assert!(descriptor_len(&fields, &blobs) > MAX_BYTES, "{n}");
    }
    let b = body("toolchain", Some(1));
    let base = canonical_bytes(&b).unwrap();
    let at = base
        .windows(br#""entries":["#.len())
        .position(|w| w == br#""entries":["#)
        .unwrap()
        + br#""entries":["#.len();
    let mut raw = base[..at].to_vec();
    for i in 0..100_001 - list(get(get(&list(get(&b, "platforms"))[0], "tree"), "entries")).len() {
        raw.extend_from_slice(
            format!(
                r#"{{"length":0,"mode":"0644","path":"f{i}","sha256":"{sha}","type":"file"}},"#
            )
            .as_bytes(),
        );
    }
    raw.extend_from_slice(&base[at..]);
    assert!(raw.len() > MAX_BYTES);
    let release = release(&raw, &["macos-arm64"]);
    assert!(TestComponent::new(raw, ENVELOPE.to_vec(), release).is_none());
}

/// R3-RF-1's allocation pin, as C1a3's (`snapshot_seal_tests.rs`): the
/// production source makes no string, integer or digest temporary, never
/// encodes through `canonical_bytes`, never sorts uncharged, and charges
/// each of its five allocations immediately before it; every comparison of
/// the sort is charged immediately before it is made.
#[test]
fn c2a1_allocates_only_what_it_charges() {
    let source = include_str!("component_closure.rs");
    let production = &source[..source.find("#[cfg(test)]\n#[path").unwrap()];
    for forbidden in [
        "format!",
        "to_string",
        "write!",
        "String::",
        "canonical_bytes",
        "digest_hex",
        "sort_unstable",
        "sort_by",
        ".sort(",
        "vec!",
        ".collect",
        "to_vec",
        "clone()",
        "Box::",
        "concat",
        "join(",
    ] {
        assert!(!production.contains(forbidden), "{forbidden}");
    }
    let encoder = &production[production.find("fn payload_len").unwrap()
        ..production.find("// The validated manifest's").unwrap()];
    for forbidden in ["String", "with_capacity", "to_owned"] {
        assert!(!encoder.contains(forbidden), "{forbidden}");
    }
    // Code lines only: the price comments name the allocations they price.
    let lines: Vec<&str> = production
        .lines()
        .filter(|l| !l.trim_start().starts_with("//"))
        .collect();
    let sites: Vec<usize> = (0..lines.len())
        .filter(|&at| lines[at].contains("with_capacity(") || lines[at].contains("to_owned()"))
        .collect();
    assert_eq!(sites.len(), 5, "{sites:?}");
    for (allocation, charge) in [
        (
            "Vec::with_capacity(files)",
            "work.charge(projection_cost(files))?;",
        ),
        (
            "let mut from = Vec::with_capacity(len)",
            "work.charge(sort_buffers_cost(len))?;",
        ),
        (
            "let mut to = Vec::with_capacity(len)",
            "work.charge(sort_buffers_cost(len))?;",
        ),
        (
            "Vec::with_capacity(length)",
            "work.charge(encoding_cost(length))?;",
        ),
        (
            "candidate.identifier().to_owned()",
            "work.charge(ID_COST)?;",
        ),
    ] {
        let at = lines.iter().position(|l| l.contains(allocation)).unwrap();
        let charged = lines[..at]
            .iter()
            .rev()
            .find(|l| l.contains("work.charge"))
            .unwrap();
        assert_eq!(charged.trim(), charge, "{allocation}");
    }
    // Pushes stay within their exact reservations.
    for (reserved, fill) in [
        (
            "let mut from = Vec::with_capacity(len);",
            "from.extend(0..n);",
        ),
        ("let mut to = Vec::with_capacity(len);", "to.extend(0..n);"),
    ] {
        let at = lines.iter().position(|l| l.trim() == reserved).unwrap();
        assert_eq!(lines[at + 1].trim(), fill);
    }
    let compare = lines
        .iter()
        .position(|l| l.contains("if less(from[j], from[i])"))
        .unwrap();
    assert_eq!(lines[compare - 1].trim(), "work.charge(COMPARISON_COST)?;");
    assert_eq!(production.matches("less(").count(), 1);
}
