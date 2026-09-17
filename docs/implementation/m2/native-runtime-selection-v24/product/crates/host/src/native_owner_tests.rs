use opensip_evaluator::{
    NativeContextError, PlanCapabilityError, admit_plan_capability, inspect_native_context,
};
use opensip_identity::{
    IdentityCandidate, IdentityDomain, JsonValue as V, ObjectInput, RetainedInputError,
    RetainedInputs, digest_hex, hash_preimage, parse_json, raw_sha256,
};
use std::collections::BTreeMap;

fn object(v: &V) -> &BTreeMap<String, V> {
    if let V::Object(o) = v {
        o
    } else {
        panic!("fixture object")
    }
}
fn object_mut(v: &mut V) -> &mut BTreeMap<String, V> {
    if let V::Object(o) = v {
        o
    } else {
        panic!("fixture object")
    }
}
fn array(v: &V) -> &[V] {
    if let V::Array(a) = v {
        a
    } else {
        panic!("fixture array")
    }
}
fn string(v: &V) -> &str {
    if let V::String(s) = v {
        s
    } else {
        panic!("fixture string")
    }
}
fn bytes(s: &str) -> Vec<u8> {
    (0..s.len())
        .step_by(2)
        .map(|i| u8::from_str_radix(&s[i..i + 2], 16).unwrap())
        .collect()
}
fn objects(fixture: &V) -> BTreeMap<String, ObjectInput> {
    array(&object(fixture)["objects"])
        .iter()
        .map(|r| {
            let r = object(r);
            (
                string(&r["id"]).into(),
                ObjectInput {
                    domain: IdentityDomain::parse(string(&r["domain"])).unwrap(),
                    descriptor: r["descriptor"].clone(),
                },
            )
        })
        .collect()
}
fn native_fixture() -> V {
    let mut fixture = parse_json(include_bytes!(
        "../tests/fixtures/native-context-fixtures.json"
    ))
    .unwrap();
    let pool = object(&object(&fixture)["bodyIdentityBlobs"]).clone();
    for packet in object_mut(object_mut(&mut fixture).get_mut("bodyIdentity").unwrap()).values_mut()
    {
        let p = object_mut(packet);
        let digests = p.remove("blobDigests").unwrap();
        let rows = array(&digests)
            .iter()
            .map(|d| {
                let key = string(d);
                V::Object(BTreeMap::from([
                    ("digest".into(), d.clone()),
                    ("hex".into(), pool[key].clone()),
                ]))
            })
            .collect();
        p.insert("blobs".into(), V::Array(rows));
    }
    fixture
}

fn context(fixture: &V, language: &str) -> V {
    object(&object(fixture)["contexts"])[language].clone()
}
fn frame(language: &str, descriptor: &V) -> ([u8; 32], BTreeMap<[u8; 32], Vec<u8>>) {
    let raw = hash_preimage(&format!("native.context.{language}.v2"), descriptor).unwrap();
    let id = raw_sha256(&raw);
    (id, BTreeMap::from([(id, raw)]))
}
const WORK: usize = 10_000_000;

#[test]
fn syntax_universe_rechecks_the_named_context_and_selected_grammars() {
    let registry = crate::embedded_schema_registry().unwrap();
    let fixture = native_fixture();
    let mut obs = objects(&fixture);
    let descriptor = context(&fixture, "syntax");
    let (context_id, mut bs) = frame("syntax", &descriptor);
    let make = |selected: &str| {
        parse_json(format!(
        "{{\"schemaVersion\":2,\"nativeContextId\":\"sha256:{}\",\"selectedGrammarIds\":[\"{}\"],\"resolutionAttempted\":false}}",
        digest_hex(&context_id),selected).as_bytes()).unwrap()
    };
    let raw = hash_preimage("native.semantic-universe.syntax.v2", &make("json.v1")).unwrap();
    let id = raw_sha256(&raw);
    bs.insert(id, raw);
    let check = opensip_evaluator::inspect_syntax_universe(
        &RetainedInputs::new(&registry, &obs, &bs),
        id,
        WORK,
    )
    .unwrap();
    assert!(check.refusals().is_empty());
    assert_eq!(check.context_digest(), context_id);
    // Same context and maps, different selected grammar: no successful binding
    // result can substitute for a fresh universe-specific check.
    let raw = hash_preimage(
        "native.semantic-universe.syntax.v2",
        &make("not-bundled.v1"),
    )
    .unwrap();
    let wrong_id = raw_sha256(&raw);
    bs.insert(wrong_id, raw);
    let check = opensip_evaluator::inspect_syntax_universe(
        &RetainedInputs::new(&registry, &obs, &bs),
        wrong_id,
        WORK,
    )
    .unwrap();
    assert_eq!(
        check.refusals(),
        ["native.syntax-grammar-not-in-bundle:not-bundled.v1"]
    );
    let key = string(&object(&object(&descriptor)["grammarBundle"])["closureId"]);
    obs.remove(key);
    let check = opensip_evaluator::inspect_syntax_universe(
        &RetainedInputs::new(&registry, &obs, &bs),
        id,
        WORK,
    )
    .unwrap();
    assert_eq!(
        check.refusals(),
        ["native.native-context-closure-unretained:grammarBundle.closureId"]
    );
    bs.remove(&context_id);
    assert!(matches!(
        opensip_evaluator::inspect_syntax_universe(
            &RetainedInputs::new(&registry, &obs, &bs),
            id,
            WORK
        ),
        Err(opensip_evaluator::NativeUniverseError::Frame(
            opensip_identity::GraphError::Input(RetainedInputError::MissingBlob(_))
        ))
    ));
}

#[test]
fn retained_rust_and_syntax_contexts_recompute_owner_checks() {
    let registry = crate::embedded_schema_registry().unwrap();
    let fixture = native_fixture();
    let obs = objects(&fixture);
    for lang in ["rust", "syntax", "typescript"] {
        let (id, bs) = frame(lang, &context(&fixture, lang));
        let inputs = RetainedInputs::new(&registry, &obs, &bs);
        let checked = inspect_native_context(&inputs, id, WORK).unwrap();
        assert!(checked.refusals().is_empty());
        assert_eq!(checked.digest(), id);
        // Just one retained frame is supplied: these owner checks deliberately
        // grant no proof that every closure member byte was retained.
        assert_eq!(bs.len(), 1);
        assert!(matches!(
            inspect_native_context(&inputs, id, 0),
            Err(NativeContextError::Frame(_))
        ));
    }
}

#[test]
fn a_reframed_context_cannot_promote_data_grammar_to_code() {
    let registry = crate::embedded_schema_registry().unwrap();
    let fixture = native_fixture();
    let obs = objects(&fixture);
    let mut descriptor = context(&fixture, "syntax");
    let V::Array(grammars) = object_mut(
        object_mut(&mut descriptor)
            .get_mut("grammarBundle")
            .unwrap(),
    )
    .get_mut("grammars")
    .unwrap() else {
        panic!()
    };
    let grammar = grammars
        .iter_mut()
        .find(|g| string(&object(g)["languageId"]) == "json")
        .unwrap();
    object_mut(grammar).insert("syntaxClass".into(), V::String("code".into()));
    let (id, bs) = frame("syntax", &descriptor);
    let inputs = RetainedInputs::new(&registry, &obs, &bs);
    let result = inspect_native_context(&inputs, id, WORK).unwrap();
    assert!(result.refusals().iter().any(|s|s=="native.syntax-grammar-class-not-the-registered-one:json:declared=code:registered=data-document"));
}

#[test]
fn missing_closure_and_changed_identity_do_not_pass_native_owner() {
    let registry = crate::embedded_schema_registry().unwrap();
    let fixture = native_fixture();
    let mut obs = objects(&fixture);
    let descriptor = context(&fixture, "syntax");
    let key = string(&object(&object(&descriptor)["grammarBundle"])["closureId"]).to_owned();
    let (id, bs) = frame("syntax", &descriptor);
    let mut removed = obs.remove(&key).unwrap();
    let result =
        inspect_native_context(&RetainedInputs::new(&registry, &obs, &bs), id, WORK).unwrap();
    assert_eq!(
        result.refusals(),
        ["native.native-context-closure-unretained:grammarBundle.closureId"]
    );
    object_mut(&mut removed.descriptor)
        .insert("semanticVersion".into(), V::String("changed".into()));
    obs.insert(key, removed);
    let result =
        inspect_native_context(&RetainedInputs::new(&registry, &obs, &bs), id, WORK).unwrap();
    assert_eq!(
        result.refusals(),
        ["native.native-context-closure-identity-mismatch:grammarBundle.closureId"]
    );
}

#[test]
fn plan_capability_join_is_per_plan_and_checks_bytes_before_gates() {
    let registry = crate::embedded_schema_registry().unwrap();
    let fixture = parse_json(include_bytes!(
        "../tests/fixtures/plan-capability-fixture.json"
    ))
    .unwrap();
    let mut obs = objects(&fixture);
    let plan_id = string(&object(&fixture)["planId"]).to_owned();
    let row = object(&array(&object(&fixture)["blobs"])[0]);
    let digest: [u8; 32] = bytes(string(&row["digest"])).try_into().unwrap();
    let raw = bytes(string(&row["hex"]));
    let mut bs = BTreeMap::from([(digest, raw)]);
    let admitted =
        admit_plan_capability(&RetainedInputs::new(&registry, &obs, &bs), &plan_id, WORK).unwrap();
    assert_eq!(
        digest_hex(&admitted.identity()),
        "508f24c718a0564c52fe18a1e6a5308d53bdd6012a50ad186ffbc208bb18881b"
    );
    let raw = bs.remove(&digest).unwrap();
    assert!(matches!(
        admit_plan_capability(&RetainedInputs::new(&registry, &obs, &bs), &plan_id, WORK),
        Err(PlanCapabilityError::Input(RetainedInputError::MissingBlob(
            _
        )))
    ));
    bs.insert(digest, raw);
    let mut other = obs[&plan_id].descriptor.clone();
    object_mut(&mut other).insert("capabilityManifestId".into(), V::String("0".repeat(64)));
    let raw = opensip_identity::canonical_bytes(&other).unwrap();
    let other_id = IdentityCandidate::from_json(&registry, IdentityDomain::Plan, &raw, WORK)
        .unwrap()
        .identifier()
        .to_owned();
    obs.insert(
        other_id.clone(),
        ObjectInput {
            domain: IdentityDomain::Plan,
            descriptor: other,
        },
    );
    assert!(matches!(
        admit_plan_capability(&RetainedInputs::new(&registry, &obs, &bs), &other_id, WORK),
        Err(PlanCapabilityError::BytesJoin)
    ));
    let bad = vec![255];
    let bad_digest = raw_sha256(&bad);
    bs.insert(bad_digest, bad);
    let mut other = obs[&other_id].descriptor.clone();
    object_mut(&mut other).insert(
        "capabilityManifestBytesDigest".into(),
        V::String(digest_hex(&bad_digest)),
    );
    let raw = opensip_identity::canonical_bytes(&other).unwrap();
    let id = IdentityCandidate::from_json(&registry, IdentityDomain::Plan, &raw, WORK)
        .unwrap()
        .identifier()
        .to_owned();
    obs.insert(
        id.clone(),
        ObjectInput {
            domain: IdentityDomain::Plan,
            descriptor: other,
        },
    );
    assert!(matches!(
        admit_plan_capability(&RetainedInputs::new(&registry, &obs, &bs), &id, WORK),
        Err(PlanCapabilityError::BytesJoin)
    ));
}

#[test]
fn typescript_universe_requires_selected_records_and_snapshot_on_every_call() {
    use opensip_evaluator::{NativeUniverseError, inspect_typescript_universe};
    let registry = crate::embedded_schema_registry().unwrap();
    let fixture = native_fixture();
    let fixture = &object(&fixture)["typescriptUniverse"];
    let mut obs = objects(fixture);
    let f = object(fixture);
    let id: [u8; 32] = bytes(string(&f["digest"])).try_into().unwrap();
    let snapshot = string(&f["snapshotId"]);
    let mut bs: BTreeMap<[u8; 32], Vec<u8>> = array(&f["blobs"])
        .iter()
        .map(|r| {
            let r = object(r);
            (
                bytes(string(&r["digest"])).try_into().unwrap(),
                bytes(string(&r["hex"])),
            )
        })
        .collect();
    assert!(matches!(
        opensip_evaluator::inspect_syntax_universe(
            &RetainedInputs::new(&registry, &obs, &bs),
            id,
            WORK
        ),
        Err(NativeUniverseError::Unsupported(_))
    ));
    let checked = inspect_typescript_universe(
        &RetainedInputs::new(&registry, &obs, &bs),
        id,
        snapshot,
        WORK,
    )
    .unwrap();
    assert!(checked.refusals().is_empty());
    assert!(matches!(
        inspect_typescript_universe(&RetainedInputs::new(&registry, &obs, &bs), id, snapshot, 0),
        Err(NativeUniverseError::Frame(
            opensip_identity::GraphError::Schema(opensip_identity::SchemaAdmissionError::Schema(
                opensip_identity::SchemaError::Limit
            ))
        ))
    ));
    let u =
        opensip_identity::parse_hash_preimage("native.semantic-universe.typescript.v2", &bs[&id])
            .unwrap();
    let graph: [u8; 32] = bytes(string(&object(&u)["tsconfigGraphHash"]))
        .try_into()
        .unwrap();
    let raw = bs.remove(&graph).unwrap();
    let checked = inspect_typescript_universe(
        &RetainedInputs::new(&registry, &obs, &bs),
        id,
        snapshot,
        WORK,
    )
    .unwrap();
    assert_eq!(
        checked.refusals(),
        ["native.universe-retained-input-missing:configGraph"]
    );
    bs.insert(graph, raw);
    let removed = obs.remove(snapshot).unwrap();
    assert!(matches!(
        inspect_typescript_universe(
            &RetainedInputs::new(&registry, &obs, &bs),
            id,
            snapshot,
            WORK
        ),
        Err(NativeUniverseError::Frame(
            opensip_identity::GraphError::Input(RetainedInputError::MissingObject(_))
        ))
    ));
    let mut changed = removed.descriptor;
    object_mut(&mut changed).insert("sourceInventory".into(), V::Array(vec![]));
    let raw = opensip_identity::canonical_bytes(&changed).unwrap();
    let other = IdentityCandidate::from_json(&registry, IdentityDomain::Snapshot, &raw, WORK)
        .unwrap()
        .identifier()
        .to_owned();
    obs.insert(
        other.clone(),
        ObjectInput {
            domain: IdentityDomain::Snapshot,
            descriptor: changed,
        },
    );
    let checked =
        inspect_typescript_universe(&RetainedInputs::new(&registry, &obs, &bs), id, &other, WORK)
            .unwrap();
    assert!(
        checked
            .refusals()
            .iter()
            .any(|x| x == "native.universe-source-mismatch:tsconfig.json")
    );
    assert!(
        checked
            .refusals()
            .iter()
            .any(|x| x == "native.universe-path-not-inventoried:a.ts")
    );
}

#[test]
fn rust_universe_rechecks_features_and_uses_the_projection_record_identity() {
    use opensip_evaluator::inspect_rust_universe;
    let registry = crate::embedded_schema_registry().unwrap();
    let fixture = native_fixture();
    let fixture = &object(&fixture)["rustUniverse"];
    let obs = objects(fixture);
    let f = object(fixture);
    let id: [u8; 32] = bytes(string(&f["digest"])).try_into().unwrap();
    let snapshot = string(&f["snapshotId"]);
    let mut bs: BTreeMap<[u8; 32], Vec<u8>> = array(&f["blobs"])
        .iter()
        .map(|r| {
            let r = object(r);
            (
                bytes(string(&r["digest"])).try_into().unwrap(),
                bytes(string(&r["hex"])),
            )
        })
        .collect();
    let check = inspect_rust_universe(
        &RetainedInputs::new(&registry, &obs, &bs),
        id,
        snapshot,
        WORK,
    )
    .unwrap();
    assert!(check.refusals().is_empty());
    let mut universe =
        opensip_identity::parse_hash_preimage("native.semantic-universe.rust.v2", &bs[&id])
            .unwrap();
    let features: [u8; 32] = bytes(
        string(&object(&universe)["unifiedFeaturesId"])
            .strip_prefix("sha256:")
            .unwrap(),
    )
    .try_into()
    .unwrap();
    let raw = bs.remove(&features).unwrap();
    let check = inspect_rust_universe(
        &RetainedInputs::new(&registry, &obs, &bs),
        id,
        snapshot,
        WORK,
    )
    .unwrap();
    assert_eq!(
        check.refusals(),
        ["native.universe-retained-input-missing:unifiedFeatures"]
    );
    bs.insert(features, raw);
    let context_id: [u8; 32] = bytes(
        string(&object(&universe)["nativeContextId"])
            .strip_prefix("sha256:")
            .unwrap(),
    )
    .try_into()
    .unwrap();
    let context =
        opensip_identity::parse_hash_preimage("native.context.rust.v2", &bs[&context_id]).unwrap();
    let file_digest = object(&object(&context)["configProjection"])["projectionSha256"].clone();
    assert_ne!(object(&universe)["configProjectionSha256"], file_digest);
    object_mut(&mut universe).insert("configProjectionSha256".into(), file_digest);
    let raw = hash_preimage("native.semantic-universe.rust.v2", &universe).unwrap();
    let changed = raw_sha256(&raw);
    bs.insert(changed, raw);
    let check = inspect_rust_universe(
        &RetainedInputs::new(&registry, &obs, &bs),
        changed,
        snapshot,
        WORK,
    )
    .unwrap();
    assert_eq!(
        check.refusals(),
        ["native.universe-context-field-mismatch:configProjectionSha256"]
    );
}

#[test]
fn native_retention_requires_member_bytes_beyond_context_descriptors() {
    use opensip_evaluator::{NativeRetentionError, NativeUniverseError, inspect_native_retention};
    use opensip_identity::{GraphError, NativeFrameSet, TraversalBudget};
    let registry = crate::embedded_schema_registry().unwrap();
    let fixture = native_fixture();
    let fixture = &object(&fixture)["nativeRetention"];
    let obs = objects(fixture);
    let f = object(fixture);
    let id: [u8; 32] = bytes(string(&f["digest"])).try_into().unwrap();
    let snapshot = string(&f["snapshotId"]);
    let mut bs: BTreeMap<[u8; 32], Vec<u8>> = array(&f["blobs"])
        .iter()
        .map(|r| {
            let r = object(r);
            (
                bytes(string(&r["digest"])).try_into().unwrap(),
                bytes(string(&r["hex"])),
            )
        })
        .collect();
    let limits = || TraversalBudget {
        steps: 100_000,
        depth: 96,
        descriptor_work: WORK,
    };
    let check = inspect_native_retention(
        &RetainedInputs::new(&registry, &obs, &bs),
        id,
        NativeFrameSet::SemanticUniverse,
        snapshot,
        limits(),
    )
    .unwrap();
    assert_eq!(check.frame_count(), 2);
    assert_eq!(check.closure_count(), 1);
    let u = opensip_identity::parse_hash_preimage("native.semantic-universe.syntax.v2", &bs[&id])
        .unwrap();
    let context_id: [u8; 32] = bytes(
        string(&object(&u)["nativeContextId"])
            .strip_prefix("sha256:")
            .unwrap(),
    )
    .try_into()
    .unwrap();
    let context =
        opensip_identity::parse_hash_preimage("native.context.syntax.v2", &bs[&context_id])
            .unwrap();
    let key = string(&object(&object(&context)["grammarBundle"])["closureId"]);
    let member = &array(&object(&obs[key].descriptor)["tree"])[0];
    let digest: [u8; 32] = bytes(string(&object(member)["sha256"])).try_into().unwrap();
    let original = bs.remove(&digest).unwrap();
    // Descriptor admission is intentionally weaker; the retained frame owner
    // must never reuse it as proof that every artifact byte is available.
    assert!(
        inspect_native_context(&RetainedInputs::new(&registry, &obs, &bs), context_id, WORK)
            .unwrap()
            .refusals()
            .is_empty()
    );
    assert!(matches!(
        inspect_native_retention(
            &RetainedInputs::new(&registry, &obs, &bs),
            id,
            NativeFrameSet::SemanticUniverse,
            snapshot,
            limits()
        ),
        Err(NativeRetentionError::Owner(NativeUniverseError::Frame(
            GraphError::Input(RetainedInputError::MissingBlob(_))
        )))
    ));
    bs.insert(digest, b"changed".to_vec());
    assert!(matches!(
        inspect_native_retention(
            &RetainedInputs::new(&registry, &obs, &bs),
            id,
            NativeFrameSet::SemanticUniverse,
            snapshot,
            limits()
        ),
        Err(NativeRetentionError::Owner(NativeUniverseError::Frame(
            GraphError::Input(RetainedInputError::BlobDigest)
        )))
    ));
    bs.insert(digest, original);
    assert!(matches!(
        inspect_native_retention(
            &RetainedInputs::new(&registry, &obs, &bs),
            id,
            NativeFrameSet::SemanticUniverse,
            snapshot,
            TraversalBudget {
                steps: 1,
                ..limits()
            }
        ),
        Err(NativeRetentionError::Limit)
    ));
}

#[test]
fn plan_native_preserves_selection_and_preparation_fault_order() {
    use opensip_evaluator::{PlanNativeError, inspect_plan_native};
    use opensip_identity::TraversalBudget;
    let registry = crate::embedded_schema_registry().unwrap();
    let fixture = native_fixture();
    let fixtures = object(&object(&fixture)["planNative"]);
    for (name, expected) in [
        ("golden-syntax", None),
        (
            "syntax-unselected-context",
            Some("UNIVERSE_CONTEXT_NOT_SELECTED"),
        ),
        (
            "syntax-unselected-context-language-first",
            Some("UNIVERSE_LANGUAGE_NOT_REQUESTED:syntax"),
        ),
        (
            "prepared-grant-missing",
            Some("PREPARED_RESOLUTION_GRANT_JOIN:read-import"),
        ),
        (
            "prepared-mode-before-context",
            Some("PREPARED_RESOLUTION_MODE_NOT_REQUESTED:rust-cargo-prepared"),
        ),
    ] {
        let f = &fixtures[name];
        let obs = objects(f);
        let f = object(f);
        let bs: BTreeMap<[u8; 32], Vec<u8>> = array(&f["blobs"])
            .iter()
            .map(|r| {
                let r = object(r);
                (
                    bytes(string(&r["digest"])).try_into().unwrap(),
                    bytes(string(&r["hex"])),
                )
            })
            .collect();
        let contexts: Vec<[u8; 32]> = array(&f["contexts"])
            .iter()
            .map(|v| bytes(string(v)).try_into().unwrap())
            .collect();
        let universes: Vec<[u8; 32]> = array(&f["universes"])
            .iter()
            .map(|v| bytes(string(v)).try_into().unwrap())
            .collect();
        let inputs = RetainedInputs::new(&registry, &obs, &bs);
        let result = inspect_plan_native(
            &inputs,
            string(&f["planId"]),
            &contexts,
            &universes,
            TraversalBudget {
                steps: 100000,
                depth: 96,
                descriptor_work: WORK,
            },
        );
        match expected {
            None => {
                let v = result.unwrap();
                assert_eq!(v.context_count(), 1);
                assert_eq!(v.universe_count(), 1);
            }
            Some(cause) => assert!(
                matches!(result,Err(PlanNativeError::Refused(ref actual)) if actual==cause),
                "{name}"
            ),
        }
        assert!(matches!(
            inspect_plan_native(
                &inputs,
                string(&f["planId"]),
                &contexts,
                &universes,
                TraversalBudget {
                    steps: 1,
                    depth: 96,
                    descriptor_work: WORK
                }
            ),
            Err(PlanNativeError::Limit)
        ));
    }
}

#[test]
fn body_identity_uses_integer_rust_editions_and_separates_normalized_custody() {
    use opensip_evaluator::{BodyIdentityError, inspect_body_identity};
    use opensip_identity::{GraphError, TraversalBudget};
    let registry = crate::embedded_schema_registry().unwrap();
    let fixture = native_fixture();
    let fixtures = object(&object(&fixture)["bodyIdentity"]);
    for (name, recomputed, tokens, trailing) in [
        ("golden-typescript", true, 0, false),
        ("golden-rust", true, 0, false),
        ("golden-syntax", true, 0, false),
        ("golden-typescript-L1-lexical-12", false, 1, false),
        ("typescript-L1-lexical-trailing-12", false, 0, true),
    ] {
        let packet = &fixtures[name];
        let obs = objects(packet);
        let p = object(packet);
        let bs: BTreeMap<[u8; 32], Vec<u8>> = array(&p["blobs"])
            .iter()
            .map(|r| {
                let r = object(r);
                (
                    bytes(string(&r["digest"])).try_into().unwrap(),
                    bytes(string(&r["hex"])),
                )
            })
            .collect();
        let inputs = RetainedInputs::new(&registry, &obs, &bs);
        let limits = || TraversalBudget {
            steps: 100000,
            depth: 96,
            descriptor_work: WORK,
        };
        let result = inspect_body_identity(&inputs, string(&p["factId"]), limits());
        if trailing {
            assert!(
                matches!(result,Err(BodyIdentityError::Refused(ref s)) if s=="BODY_TOKEN_STREAM_TRAILING")
            );
        } else {
            let value = result.unwrap();
            assert_eq!(value.source_recomputed(), recomputed, "{name}");
            assert_eq!(value.token_count(), tokens, "{name}");
        }
        // The identity-only boundary must not silently accept a native body
        // merely because the evaluator's separate local check now exists.
        let fact = &obs[string(&p["factId"])].descriptor;
        let f = object(fact);
        assert_eq!(
            inputs.inspect_relation_sources(
                bytes(string(&f["payloadDigest"])).try_into().unwrap(),
                bytes(string(&f["payloadSchemaDigest"])).try_into().unwrap(),
                fact,
                limits()
            ),
            Err(GraphError::Unsupported("relation body identity owner"))
        );
        assert!(matches!(
            inspect_body_identity(
                &inputs,
                string(&p["factId"]),
                TraversalBudget {
                    steps: 0,
                    depth: 96,
                    descriptor_work: WORK
                }
            ),
            Err(BodyIdentityError::Limit)
        ));
    }
}

#[test]
fn native_support_uses_selected_suffixes_and_derives_empty_view_disclosures() {
    use opensip_evaluator::{
        NativeSupportError, inspect_coverage_prerequisites, inspect_syntax_fact,
    };
    use opensip_identity::TraversalBudget;
    let registry = crate::embedded_schema_registry().unwrap();
    let fixture = native_fixture();
    for (name, case) in object(&object(&fixture)["capabilitySupport"]) {
        let case = object(case);
        let packet = &case["request"];
        let p = object(packet);
        let obs = objects(packet);
        // Reuse already-retained body fixture blobs; the per-request digest
        // list still determines exactly which bytes are supplied to this test.
        let mut pool: BTreeMap<&str, &V> = BTreeMap::new();
        for packet in object(&object(&fixture)["bodyIdentity"]).values() {
            for row in array(&object(packet)["blobs"]) {
                let row = object(row);
                pool.insert(string(&row["digest"]), &row["hex"]);
            }
        }
        for (digest, raw) in object(&object(&fixture)["capabilitySupportBlobs"]) {
            pool.insert(digest.as_str(), raw);
        }
        let bs: BTreeMap<[u8; 32], Vec<u8>> = array(&p["blobDigests"])
            .iter()
            .map(|d| {
                let d = string(d);
                (bytes(d).try_into().unwrap(), bytes(string(pool[d])))
            })
            .collect();
        let inputs = RetainedInputs::new(&registry, &obs, &bs);
        let run = |steps| {
            let budget = TraversalBudget {
                steps,
                depth: 96,
                descriptor_work: WORK,
            };
            if string(&p["mode"]) == "syntax-fact" {
                inspect_syntax_fact(&inputs, string(&p["factId"]), budget)
            } else {
                inspect_coverage_prerequisites(&inputs, string(&p["coverageId"]), budget)
            }
        };
        let expected = object(&case["expected"]);
        let result = run(100000);
        if string(&expected["result"]) == "checked" {
            let checks = result.unwrap();
            assert_eq!(
                checks.gates_checked(),
                if string(&p["mode"]) == "syntax-fact" {
                    1
                } else {
                    3
                },
                "{name}"
            );
        } else {
            assert!(
                matches!(result,Err(NativeSupportError::Refused(ref cause)) if cause==string(&expected["cause"])),
                "{name}"
            );
        }
        assert!(matches!(run(0), Err(NativeSupportError::Limit)), "{name}");
    }
}

#[test]
fn coverage_producer_recomputes_scope_and_preserves_rc3_rc4_rc6() {
    use opensip_evaluator::{
        CoverageProducerError, CoverageProducerInput, CoverageUnresolvedEdge,
        inspect_coverage_producer,
    };
    use opensip_identity::TraversalBudget;
    let registry = crate::embedded_schema_registry().unwrap();
    let fixture = native_fixture();
    let mut pool: BTreeMap<&str, &V> = BTreeMap::new();
    for packet in object(&object(&fixture)["bodyIdentity"]).values() {
        for row in array(&object(packet)["blobs"]) {
            let row = object(row);
            pool.insert(string(&row["digest"]), &row["hex"]);
        }
    }
    for group in ["capabilitySupportBlobs", "coverageProducerBlobs"] {
        for (d, raw) in object(&object(&fixture)[group]) {
            pool.insert(d.as_str(), raw);
        }
    }
    for (name, case) in object(&object(&fixture)["coverageProducer"]) {
        let case = object(case);
        let packet = &case["request"];
        let p = object(packet);
        let obs = objects(packet);
        let bs: BTreeMap<[u8; 32], Vec<u8>> = array(&p["blobDigests"])
            .iter()
            .map(|d| {
                let d = string(d);
                (bytes(d).try_into().unwrap(), bytes(string(pool[d])))
            })
            .collect();
        let inputs = RetainedInputs::new(&registry, &obs, &bs);
        let edges: Vec<_> = array(&p["unresolved"])
            .iter()
            .map(|v| {
                let v = object(v);
                CoverageUnresolvedEdge {
                    relation: string(&v["relation"]),
                    referrer: string(&v["referrer"]),
                    edge_kind: string(&v["edgeKind"]),
                }
            })
            .collect();
        let request = || CoverageProducerInput {
            scope_id: string(&p["scopeId"]),
            payload_digest: bytes(string(&p["payloadDigest"])).try_into().unwrap(),
            payload_schema_digest: if p["payloadSchemaDigest"] == V::Null {
                None
            } else {
                Some(bytes(string(&p["payloadSchemaDigest"])).try_into().unwrap())
            },
            unresolved: &edges,
            universe_dialect: if p["dialect"] == V::Null {
                None
            } else {
                Some(&p["dialect"])
            },
        };
        let result = inspect_coverage_producer(
            &inputs,
            request(),
            TraversalBudget {
                steps: 100000,
                depth: 96,
                descriptor_work: WORK,
            },
        )
        .unwrap();
        assert_eq!(result.value(), &case["expected"], "{name}");
        assert!(
            matches!(
                inspect_coverage_producer(
                    &inputs,
                    request(),
                    TraversalBudget {
                        steps: 0,
                        depth: 96,
                        descriptor_work: WORK
                    }
                ),
                Err(CoverageProducerError::Limit)
            ),
            "{name}"
        );
    }
}

#[test]
fn view_joins_keep_partition_totality_and_unresolved_census_local() {
    use opensip_evaluator::{NativeSupportError, ViewJoinError, inspect_view_joins};
    use opensip_identity::TraversalBudget;
    let registry = crate::embedded_schema_registry().unwrap();
    let fixture = native_fixture();
    let f = object(&fixture);
    let mut pool: BTreeMap<&str, &V> = BTreeMap::new();
    let mut opool: BTreeMap<&str, &V> = BTreeMap::new();
    for packet in object(&f["bodyIdentity"]).values() {
        let p = object(packet);
        for row in array(&p["blobs"]) {
            let row = object(row);
            pool.insert(string(&row["digest"]), &row["hex"]);
        }
        for row in array(&p["objects"]) {
            opool.insert(string(&object(row)["id"]), row);
        }
    }
    for group in [
        "capabilitySupportBlobs",
        "coverageProducerBlobs",
        "viewJoinBlobs",
    ] {
        for (d, raw) in object(&f[group]) {
            pool.insert(d.as_str(), raw);
        }
    }
    for group in ["capabilitySupport", "coverageProducer"] {
        for case in object(&f[group]).values() {
            for row in array(&object(&object(case)["request"])["objects"]) {
                opool.insert(string(&object(row)["id"]), row);
            }
        }
    }
    for (id, row) in object(&f["viewJoinObjects"]) {
        opool.insert(id.as_str(), row);
    }
    let orows: Vec<_> = opool.into_iter().collect();
    let brows: Vec<_> = pool.into_iter().collect();
    let index = |v: &V| {
        let V::Integer(n) = v else { panic!("index") };
        usize::try_from(n.get()).unwrap()
    };
    for (name, case) in object(&f["viewJoins"]) {
        let c = object(case);
        let p = object(&c["request"]);
        let expected = object(&c["expected"]);
        let obs: BTreeMap<String, ObjectInput> = array(&p["objectIndices"])
            .iter()
            .map(|i| {
                let (id, row) = orows[index(i)];
                let row = object(row);
                (
                    id.into(),
                    ObjectInput {
                        domain: IdentityDomain::parse(string(&row["domain"])).unwrap(),
                        descriptor: row["descriptor"].clone(),
                    },
                )
            })
            .collect();
        let bs: BTreeMap<[u8; 32], Vec<u8>> = array(&p["blobIndices"])
            .iter()
            .map(|i| {
                let (d, raw) = brows[index(i)];
                (bytes(d).try_into().unwrap(), bytes(string(raw)))
            })
            .collect();
        let inputs = RetainedInputs::new(&registry, &obs, &bs);
        let result = inspect_view_joins(
            &inputs,
            string(&p["runId"]),
            string(&p["viewId"]),
            TraversalBudget {
                steps: 100000,
                depth: 96,
                descriptor_work: WORK,
            },
        );
        match result {
            Ok(checks) => {
                assert_eq!(string(&expected["result"]), "checked", "{name}");
                for (key, count) in [
                    ("facts", checks.fact_count()),
                    ("scopes", checks.scope_count()),
                    ("coverage", checks.coverage_count()),
                ] {
                    let V::Integer(n) = &expected[key] else {
                        panic!("count")
                    };
                    assert_eq!(count as i128, n.get(), "{name}:{key}");
                }
            }
            Err(ViewJoinError::ViewNotSelected) => {
                assert_eq!(string(&expected["result"]), "not-selected", "{name}")
            }
            Err(ViewJoinError::Refused(cause))
            | Err(ViewJoinError::Support(NativeSupportError::Refused(cause))) => {
                assert_eq!(string(&expected["result"]), "refused", "{name}");
                assert_eq!(cause, string(&expected["cause"]), "{name}");
            }
            Err(error) => panic!("{name}: unexpected {error:?}"),
        }
        assert!(
            matches!(
                inspect_view_joins(
                    &inputs,
                    string(&p["runId"]),
                    string(&p["viewId"]),
                    TraversalBudget {
                        steps: 0,
                        depth: 96,
                        descriptor_work: WORK
                    }
                ),
                Err(ViewJoinError::Limit)
            ),
            "{name}"
        );
    }
}

#[test]
fn run_links_and_evidence_roots_rehash_their_selected_inputs() {
    use opensip_evaluator::{RunLinkError, inspect_evidence_roots, inspect_run_links};
    use opensip_identity::TraversalBudget;
    let registry = crate::embedded_schema_registry().unwrap();
    let fixture = native_fixture();
    let f = object(&fixture);
    let mut pool: BTreeMap<&str, &V> = BTreeMap::new();
    let mut opool: BTreeMap<&str, &V> = BTreeMap::new();
    for packet in object(&f["bodyIdentity"]).values() {
        let p = object(packet);
        for row in array(&p["blobs"]) {
            let row = object(row);
            pool.insert(string(&row["digest"]), &row["hex"]);
        }
        for row in array(&p["objects"]) {
            opool.insert(string(&object(row)["id"]), row);
        }
    }
    for group in [
        "capabilitySupportBlobs",
        "coverageProducerBlobs",
        "viewJoinBlobs",
        "runLinkBlobs",
    ] {
        for (d, raw) in object(&f[group]) {
            pool.insert(d.as_str(), raw);
        }
    }
    for group in ["capabilitySupport", "coverageProducer"] {
        for case in object(&f[group]).values() {
            for row in array(&object(&object(case)["request"])["objects"]) {
                opool.insert(string(&object(row)["id"]), row);
            }
        }
    }
    for group in ["viewJoinObjects", "runLinkObjects"] {
        for (id, row) in object(&f[group]) {
            opool.insert(id.as_str(), row);
        }
    }
    let orows: Vec<_> = opool.into_iter().collect();
    let brows: Vec<_> = pool.into_iter().collect();
    let index = |v: &V| {
        let V::Integer(n) = v else { panic!("index") };
        usize::try_from(n.get()).unwrap()
    };
    for (name, case) in object(&f["runLinks"]) {
        let c = object(case);
        let p = object(&c["request"]);
        let expected = object(&c["expected"]);
        let obs: BTreeMap<String, ObjectInput> = array(&p["objectIndices"])
            .iter()
            .map(|i| {
                let (id, row) = orows[index(i)];
                let row = object(row);
                (
                    id.into(),
                    ObjectInput {
                        domain: IdentityDomain::parse(string(&row["domain"])).unwrap(),
                        descriptor: row["descriptor"].clone(),
                    },
                )
            })
            .collect();
        let bs: BTreeMap<[u8; 32], Vec<u8>> = array(&p["blobIndices"])
            .iter()
            .map(|i| {
                let (d, raw) = brows[index(i)];
                (bytes(d).try_into().unwrap(), bytes(string(raw)))
            })
            .collect();
        let inputs = RetainedInputs::new(&registry, &obs, &bs);
        let run = |steps| {
            let budget = TraversalBudget {
                steps,
                depth: 96,
                descriptor_work: WORK,
            };
            if string(&p["mode"]) == "run-links" {
                inspect_run_links(&inputs, string(&p["runId"]), budget)
                    .map(|v| vec![("imports", v.import_count())])
            } else {
                inspect_evidence_roots(&inputs, string(&p["runId"]), budget).map(|v| {
                    vec![
                        ("views", v.view_count()),
                        ("coverage", v.coverage_count()),
                        ("findings", v.finding_count()),
                    ]
                })
            }
        };
        match run(100000) {
            Ok(counts) => {
                assert_eq!(string(&expected["result"]), "checked", "{name}");
                for (key, count) in counts {
                    assert_eq!(count, index(&expected[key]), "{name}:{key}");
                }
            }
            Err(RunLinkError::Refused(cause)) => {
                assert_eq!(string(&expected["result"]), "refused", "{name}");
                assert_eq!(cause, string(&expected["cause"]), "{name}");
            }
            Err(error) => panic!("{name}: unexpected {error:?}"),
        }
        assert!(matches!(run(0), Err(RunLinkError::Limit)), "{name}");
    }
}

#[test]
fn policy_program_rehashes_compilation_and_closes_rule_domains() {
    use opensip_evaluator::{PolicyAdmissionError, inspect_policy_program};
    use opensip_identity::{GraphError, RetainedInputError, TraversalBudget};
    let registry = crate::embedded_schema_registry().unwrap();
    let fixture = native_fixture();
    let f = object(&fixture);
    for (name, case) in object(&f["policyProgram"]) {
        let c = object(case);
        let p = object(&c["request"]);
        let expected = object(&c["expected"]);
        let obs: BTreeMap<String, ObjectInput> = array(&p["objects"])
            .iter()
            .map(|row| {
                let r = object(row);
                (
                    string(&r["id"]).into(),
                    ObjectInput {
                        domain: IdentityDomain::parse(string(&r["domain"])).unwrap(),
                        descriptor: r["descriptor"].clone(),
                    },
                )
            })
            .collect();
        let bs: BTreeMap<[u8; 32], Vec<u8>> = array(&p["blobs"])
            .iter()
            .map(|row| {
                let r = object(row);
                (
                    bytes(string(&r["digest"])).try_into().unwrap(),
                    bytes(string(&r["hex"])),
                )
            })
            .collect();
        let inputs = RetainedInputs::new(&registry, &obs, &bs);
        let run = |steps| {
            inspect_policy_program(
                &inputs,
                string(&p["runId"]),
                TraversalBudget {
                    steps,
                    depth: 96,
                    descriptor_work: WORK,
                },
            )
        };
        let result = match run(100000) {
            Ok(checked) => {
                let V::Integer(n) = &expected["rules"] else {
                    panic!("{name}: expected rule count")
                };
                assert_eq!(
                    checked.rule_count(),
                    usize::try_from(n.get()).unwrap(),
                    "{name}"
                );
                "checked"
            }
            Err(PolicyAdmissionError::Refused(cause)) => {
                assert_eq!(cause, string(&expected["cause"]), "{name}");
                "refused"
            }
            Err(PolicyAdmissionError::Limit) => "limit",
            Err(PolicyAdmissionError::Record(GraphError::Input(
                RetainedInputError::MissingObject(_) | RetainedInputError::MissingBlob(_),
            ))) => "unavailable",
            Err(_) => "invalid",
        };
        assert_eq!(result, string(&expected["result"]), "{name}");
        assert!(matches!(run(0), Err(PolicyAdmissionError::Limit)), "{name}");
    }
}

#[test]
fn predicate_witnesses_join_exact_nodes_children_and_evidence_roots() {
    use opensip_evaluator::{PredicateError, inspect_predicate_witnesses};
    use opensip_identity::{GraphError, RetainedInputError, TraversalBudget};
    let registry = crate::embedded_schema_registry().unwrap();
    let fixture = native_fixture();
    let f = object(&fixture);
    for (name, case) in object(&f["predicateWitnesses"]) {
        let c = object(case);
        let p = object(&c["request"]);
        let expected = object(&c["expected"]);
        let obs: BTreeMap<String, ObjectInput> = array(&p["objects"])
            .iter()
            .map(|row| {
                let r = object(row);
                (
                    string(&r["id"]).into(),
                    ObjectInput {
                        domain: IdentityDomain::parse(string(&r["domain"])).unwrap(),
                        descriptor: r["descriptor"].clone(),
                    },
                )
            })
            .collect();
        let bs: BTreeMap<[u8; 32], Vec<u8>> = array(&p["blobs"])
            .iter()
            .map(|row| {
                let r = object(row);
                (
                    bytes(string(&r["digest"])).try_into().unwrap(),
                    bytes(string(&r["hex"])),
                )
            })
            .collect();
        let inputs = RetainedInputs::new(&registry, &obs, &bs);
        let run = |steps| {
            inspect_predicate_witnesses(
                &inputs,
                string(&p["runId"]),
                TraversalBudget {
                    steps,
                    depth: 96,
                    descriptor_work: WORK,
                },
            )
        };
        let result = match run(100000) {
            Ok(checked) => {
                let V::Integer(n) = &expected["predicates"] else {
                    panic!("{name}: expected predicate count")
                };
                assert_eq!(
                    checked.predicate_count(),
                    usize::try_from(n.get()).unwrap(),
                    "{name}"
                );
                "checked"
            }
            Err(PredicateError::Refused(cause)) => {
                assert_eq!(cause, string(&expected["cause"]), "{name}");
                "refused"
            }
            Err(PredicateError::Limit) => "limit",
            Err(PredicateError::Record(GraphError::Input(
                RetainedInputError::MissingObject(_) | RetainedInputError::MissingBlob(_),
            ))) => "unavailable",
            Err(_) => "invalid",
        };
        assert_eq!(result, string(&expected["result"]), "{name}");
        assert!(matches!(run(0), Err(PredicateError::Limit)), "{name}");
    }
}

#[test]
fn stage_outputs_join_selected_provider_interface_and_declared_inputs() {
    use opensip_evaluator::{StageOutputError, inspect_stage_output_schema, inspect_stage_specs};
    use opensip_identity::{GraphError, RetainedInputError, TraversalBudget};
    let registry = crate::embedded_schema_registry().unwrap();
    let fixture = native_fixture();
    let f = object(&fixture);
    for (name, case) in object(&f["stageOutputs"]) {
        let c = object(case);
        let p = object(&c["request"]);
        let expected = object(&c["expected"]);
        let obs: BTreeMap<String, ObjectInput> = array(&p["objects"])
            .iter()
            .map(|row| {
                let r = object(row);
                (
                    string(&r["id"]).into(),
                    ObjectInput {
                        domain: IdentityDomain::parse(string(&r["domain"])).unwrap(),
                        descriptor: r["descriptor"].clone(),
                    },
                )
            })
            .collect();
        let bs: BTreeMap<[u8; 32], Vec<u8>> = array(&p["blobs"])
            .iter()
            .map(|row| {
                let r = object(row);
                (
                    bytes(string(&r["digest"])).try_into().unwrap(),
                    bytes(string(&r["hex"])),
                )
            })
            .collect();
        let inputs = RetainedInputs::new(&registry, &obs, &bs);
        let run = |steps| {
            let budget = TraversalBudget {
                steps,
                depth: 96,
                descriptor_work: WORK,
            };
            if string(&p["mode"]) == "stage-output" {
                inspect_stage_output_schema(
                    &inputs,
                    bytes(string(&p["specDigest"])).try_into().unwrap(),
                    budget,
                )
                .map(|_| None)
            } else {
                inspect_stage_specs(&inputs, string(&p["runId"]), budget)
                    .map(|v| Some(v.stage_count()))
            }
        };
        let result = match run(100000) {
            Ok(checked) => {
                if let Some(count) = checked {
                    let V::Integer(n) = &expected["stages"] else {
                        panic!("{name}: expected stage count")
                    };
                    assert_eq!(count, usize::try_from(n.get()).unwrap(), "{name}");
                }
                "checked"
            }
            Err(StageOutputError::Refused(cause)) => {
                assert_eq!(cause, string(&expected["cause"]), "{name}");
                "refused"
            }
            Err(StageOutputError::Limit) => "limit",
            Err(StageOutputError::Record(GraphError::Input(
                RetainedInputError::MissingObject(_) | RetainedInputError::MissingBlob(_),
            ))) => "unavailable",
            Err(_) => "invalid",
        };
        assert_eq!(result, string(&expected["result"]), "{name}");
        assert!(matches!(run(0), Err(StageOutputError::Limit)), "{name}");
    }
}

#[test]
fn imports_join_retained_source_revision_build_and_parameter_selection() {
    use opensip_evaluator::{ImportJoinError, inspect_import_joins, inspect_parameter_selection};
    use opensip_identity::{GraphError, RetainedInputError, TraversalBudget};
    let registry = crate::embedded_schema_registry().unwrap();
    let fixture = opensip_identity::parse_json(include_bytes!(
        "../tests/fixtures/import-joins-fixtures.json"
    ))
    .unwrap();
    let f = object(&fixture);
    for (name, case) in f {
        let c = object(case);
        let p = object(&c["request"]);
        let expected = object(&c["expected"]);
        let obs: BTreeMap<String, ObjectInput> = array(&p["objects"])
            .iter()
            .map(|row| {
                let r = object(row);
                (
                    string(&r["id"]).into(),
                    ObjectInput {
                        domain: IdentityDomain::parse(string(&r["domain"])).unwrap(),
                        descriptor: r["descriptor"].clone(),
                    },
                )
            })
            .collect();
        let bs: BTreeMap<[u8; 32], Vec<u8>> = array(&p["blobs"])
            .iter()
            .map(|row| {
                let r = object(row);
                (
                    bytes(string(&r["digest"])).try_into().unwrap(),
                    bytes(string(&r["hex"])),
                )
            })
            .collect();
        let inputs = RetainedInputs::new(&registry, &obs, &bs);
        let run = |steps| {
            let budget = TraversalBudget {
                steps,
                depth: 96,
                descriptor_work: WORK,
            };
            if string(&p["mode"]) == "parameter-selection" {
                inspect_parameter_selection(
                    &inputs,
                    bytes(string(&p["analysisDigest"])).try_into().unwrap(),
                    budget,
                )
                .map(|_| None)
            } else {
                inspect_import_joins(&inputs, string(&p["runId"]), budget)
                    .map(|v| Some(v.import_count()))
            }
        };
        let result = match run(100000) {
            Ok(checked) => {
                if let Some(count) = checked {
                    let V::Integer(n) = &expected["imports"] else {
                        panic!("{name}: expected import count")
                    };
                    assert_eq!(count, usize::try_from(n.get()).unwrap(), "{name}");
                }
                "checked"
            }
            Err(ImportJoinError::Refused(cause)) => {
                assert_eq!(cause, string(&expected["cause"]), "{name}");
                "refused"
            }
            Err(ImportJoinError::Limit) => "limit",
            Err(ImportJoinError::Record(GraphError::Input(
                RetainedInputError::MissingObject(_) | RetainedInputError::MissingBlob(_),
            ))) => "unavailable",
            Err(_) => "invalid",
        };
        assert_eq!(result, string(&expected["result"]), "{name}");
        assert!(matches!(run(0), Err(ImportJoinError::Limit)), "{name}");
    }
}

#[test]
fn import_payloads_require_exact_kind_domain_and_retained_schema() {
    use opensip_evaluator::{ImportPayloadError, inspect_import_payload};
    use opensip_identity::{GraphError, RetainedInputError, TraversalBudget};
    let registry = crate::embedded_schema_registry().unwrap();
    let fixture = opensip_identity::parse_json(include_bytes!(
        "../tests/fixtures/import-payload-fixtures.json"
    ))
    .unwrap();
    let f = object(&fixture);
    for (name, case) in object(&f["cases"]) {
        let c = object(case);
        let p = object(&c["request"]);
        let expected = object(&c["expected"]);
        let obs: BTreeMap<String, ObjectInput> = array(&p["objects"])
            .iter()
            .map(|row| {
                let r = object(row);
                (
                    string(&r["id"]).into(),
                    ObjectInput {
                        domain: IdentityDomain::parse(string(&r["domain"])).unwrap(),
                        descriptor: r["descriptor"].clone(),
                    },
                )
            })
            .collect();
        let bs: BTreeMap<[u8; 32], Vec<u8>> = array(&p["blobs"])
            .iter()
            .map(|row| {
                let r = object(&object(&f["blobPool"])[string(row)]);
                (
                    bytes(string(&r["digest"])).try_into().unwrap(),
                    bytes(string(&r["hex"])),
                )
            })
            .collect();
        let inputs = RetainedInputs::new(&registry, &obs, &bs);
        let run = |steps| {
            let budget = TraversalBudget {
                steps,
                depth: 96,
                descriptor_work: WORK,
            };
            inspect_import_payload(&inputs, string(&p["importId"]), budget)
        };
        let result = match run(20000000) {
            Ok(_) => "checked",
            Err(ImportPayloadError::Refused(cause)) => {
                assert_eq!(cause, string(&expected["cause"]), "{name}");
                "refused"
            }
            Err(ImportPayloadError::Limit) => "limit",
            Err(ImportPayloadError::Record(GraphError::Input(
                RetainedInputError::MissingObject(_) | RetainedInputError::MissingBlob(_),
            ))) => "unavailable",
            Err(_) => "invalid",
        };
        assert_eq!(result, string(&expected["result"]), "{name}");
        assert!(matches!(run(0), Err(ImportPayloadError::Limit)), "{name}");
    }
}

#[test]
fn full_retained_walk_checks_complete_inputs_faults_and_separate_limits() {
    use opensip_evaluator::{RetainedWalkLimits, inspect_retained_walk};
    use opensip_identity::TraversalBudget;
    let registry = crate::embedded_schema_registry().unwrap();
    let fixture = parse_json(include_bytes!("../tests/fixtures/full-walk-fixtures.json")).unwrap();
    let f = object(&fixture);
    for (name, case) in object(&f["cases"]) {
        let c = object(case);
        let p = object(&c["request"]);
        let expected = object(&c["expected"]);
        let obs: BTreeMap<String, ObjectInput> = array(&p["objects"])
            .iter()
            .map(|row| {
                let r = object(&object(&f["objectPool"])[string(row)]);
                (
                    string(&r["id"]).into(),
                    ObjectInput {
                        domain: IdentityDomain::parse(string(&r["domain"])).unwrap(),
                        descriptor: r["descriptor"].clone(),
                    },
                )
            })
            .collect();
        let bs: BTreeMap<[u8; 32], Vec<u8>> = array(&p["blobs"])
            .iter()
            .map(|row| {
                let r = object(&object(&f["blobPool"])[string(row)]);
                (
                    bytes(string(&r["digest"])).try_into().unwrap(),
                    bytes(string(&r["hex"])),
                )
            })
            .collect();
        let inputs = RetainedInputs::new(&registry, &obs, &bs);
        let bound = |key, default| {
            p.get(key)
                .map(|v| string(v).parse::<usize>().unwrap())
                .unwrap_or(default)
        };
        let walk = TraversalBudget {
            steps: bound("steps", 20_000_000),
            depth: bound("walkDepth", 96),
            descriptor_work: bound("walkWork", 20_000_000),
        };
        if string(&p["mode"]) == "default-walk" {
            assert!(matches!(
                inputs.inspect_local_structure(string(&p["runId"]), IdentityDomain::Run, walk),
                Err(opensip_identity::GraphError::Unsupported(
                    "capability derivation"
                ))
            ));
            continue;
        }
        let result = inspect_retained_walk(
            &inputs,
            string(&p["runId"]),
            RetainedWalkLimits {
                walk,
                owner: TraversalBudget {
                    steps: bound("ownerSteps", 20_000_000),
                    depth: bound("ownerDepth", 96),
                    descriptor_work: bound("ownerWork", 20_000_000),
                },
                owner_invocations: bound("ownerCalls", 100_000),
            },
        );
        match result {
            Ok(checked) => {
                assert_eq!(string(&expected["result"]), "checked", "{name}");
                assert!(checked.object_count() > 0 && checked.context_count() > 0);
                assert!(checked.universe_count() > 0 && checked.owner_invocations() > 0);
            }
            Err(error) => {
                // Test-only normalization across the existing typed owner errors.
                // Public results remain typed; this is not a production router.
                let detail = format!("{error:?}");
                let class = if detail.contains("MissingObject(") || detail.contains("MissingBlob(")
                {
                    "unavailable"
                } else if detail.contains("Limit") {
                    "limited"
                } else {
                    "invalid"
                };
                assert_eq!(class, string(&expected["result"]), "{name}: {detail}");
                if let Some(cause) = expected.get("cause") {
                    let cause = string(cause);
                    if [
                        "REFERENCE_SOURCE_JOIN",
                        "REFERENCE_PLAN_JOIN",
                        "CAPABILITY_JOIN",
                        "VERDICT_JOIN",
                        "HIDDEN_FINDING_EVIDENCE",
                        "EVALUATION_VIEW_ROOTS",
                        "EVALUATION_COVERAGE_ROOTS",
                    ]
                    .contains(&cause)
                    {
                        assert!(detail.contains(cause), "{name}: {detail}");
                    }
                }
            }
        }
    }
}

#[test]
fn enumeration_extents_follow_scope_program_ownership_and_canonical_order() {
    use opensip_evaluator::{
        EnumerationExtentError, EnumerationExtentInputs, EnumerationExtentKind,
        project_enumeration_extent,
    };
    let fixture = parse_json(include_bytes!(
        "../tests/fixtures/enumeration-fixtures.json"
    ))
    .unwrap();
    let f = object(&fixture);
    let pool = object(&f["values"]);
    for (name, case) in object(&f["cases"]) {
        let c = object(case);
        let p = object(&c["request"]);
        let expected = object(&c["expected"]);
        let value = |key| &pool[string(&p[key])];
        let paths = array(value("snapshotPaths"))
            .iter()
            .map(|v| string(v).to_owned())
            .collect::<Vec<_>>();
        let input = EnumerationExtentInputs {
            membership: value("membership"),
            snapshot_paths: &paths,
            scope: value("scope"),
            workspace_root: string(&p["workspaceRoot"]),
            language_mode: string(&p["languageMode"]),
            universe: Some(value("universe")),
            retained: Some(value("retained")),
        };
        let kind = match string(&p["kind"]) {
            "file" => EnumerationExtentKind::File,
            "symbol" => EnumerationExtentKind::Symbol,
            _ => panic!("{name}: kind"),
        };
        let steps = p
            .get("steps")
            .map(|v| string(v).parse::<usize>().unwrap())
            .unwrap_or(1_000_000);
        match project_enumeration_extent(&input, kind, steps) {
            Ok(actual) => {
                assert_eq!(string(&expected["result"]), "projected", "{name}");
                let expected_paths = array(&expected["paths"])
                    .iter()
                    .map(string)
                    .collect::<Vec<_>>();
                let expected_refusals = array(&expected["refusals"])
                    .iter()
                    .map(string)
                    .collect::<Vec<_>>();
                assert_eq!(actual.paths(), expected_paths, "{name}");
                assert_eq!(actual.refusals(), expected_refusals, "{name}");
            }
            Err(error) => {
                assert_eq!(string(&expected["result"]), "error", "{name}: {error:?}");
                assert_eq!(error, EnumerationExtentError::Limit, "{name}");
            }
        }
    }
}

#[test]
fn enumeration_membership_rederives_rows_order_roots_and_snapshot_coverage() {
    use opensip_evaluator::{EnumerationMembershipError, inspect_enumeration_membership};
    let registry = crate::embedded_schema_registry().unwrap();
    let fixture = parse_json(include_bytes!(
        "../tests/fixtures/enumeration-fixtures.json"
    ))
    .unwrap();
    let f = object(&fixture);
    let pool = object(&f["membershipValues"]);
    for (name, case) in object(&f["membershipCases"]) {
        let c = object(case);
        let q = object(&c["request"]);
        let expected = object(&c["expected"]);
        let mut membership = pool[string(&q["membership"])].clone();
        let V::Object(fields) = &mut membership else {
            panic!("{name}: membership")
        };
        for key in ["rows", "units"] {
            let members = array(&fields[key])
                .iter()
                .map(|id| pool[string(id)].clone())
                .collect();
            fields.insert(key.into(), V::Array(members));
        }
        let paths = array(&pool[string(&q["snapshotPaths"])])
            .iter()
            .map(|v| string(v).to_owned())
            .collect::<Vec<_>>();
        let steps = q
            .get("steps")
            .map(|v| string(v).parse::<usize>().unwrap())
            .unwrap_or(1_000_000);
        match inspect_enumeration_membership(&registry, &membership, &paths, steps) {
            Ok(actual) => {
                assert_eq!(string(&expected["result"]), "checked", "{name}");
                let refusals = array(&expected["refusals"])
                    .iter()
                    .map(string)
                    .collect::<Vec<_>>();
                assert_eq!(actual.refusals(), refusals, "{name}");
            }
            Err(error) => {
                assert_eq!(string(&expected["result"]), "error", "{name}: {error:?}");
                assert_eq!(error, EnumerationMembershipError::Limit, "{name}");
            }
        }
    }
}

#[test]
fn retained_package_projection_matches_selected_reference_and_local_limits() {
    use opensip_evaluator::{
        EnumerationExtentError, EnumerationExtentInputs, project_enumeration_packages,
    };
    let fixture = parse_json(include_bytes!("../tests/fixtures/package-fixtures.json")).unwrap();
    for (name, case) in object(&fixture) {
        let case = object(case);
        let input = object(&case["input"]);
        let expected = object(&case["expected"]);
        let paths = array(&input["snapshotPaths"])
            .iter()
            .map(|v| string(v).to_owned())
            .collect::<Vec<_>>();
        let request = EnumerationExtentInputs {
            membership: &input["membership"],
            snapshot_paths: &paths,
            scope: &input["scope"],
            workspace_root: string(&input["workspaceRoot"]),
            language_mode: "syntax-only",
            universe: None,
            retained: None,
        };
        let blobs = object(&input["blobs"])
            .iter()
            .map(|(k, v)| (k.clone(), bytes(string(v))))
            .collect();
        let index = input
            .get("index")
            .filter(|v| !matches!(v, V::Null))
            .map(object);
        let steps = input
            .get("steps")
            .map(|v| {
                if let V::Integer(n) = v {
                    usize::try_from(n.get()).unwrap()
                } else {
                    panic!("steps")
                }
            })
            .unwrap_or(1_000_000);
        match project_enumeration_packages(&request, &blobs, index, steps) {
            Ok(actual) => {
                assert_eq!(string(&expected["result"]), "projected", "{name}");
                assert_eq!(actual.value(), &expected["value"], "{name}");
                let refusals = array(&expected["refusals"])
                    .iter()
                    .map(string)
                    .collect::<Vec<_>>();
                assert_eq!(actual.refusals(), refusals, "{name}");
            }
            Err(error) => {
                assert_eq!(string(&expected["result"]), "error", "{name}: {error:?}");
                assert_eq!(error, EnumerationExtentError::Limit, "{name}");
            }
        }
    }
}

#[test]
fn toml_parser_and_drop_fit_selected_development_worker_stack() {
    // The host execution profile owns stack provisioning; the no_std parser
    // neither inspects ambient thread state nor creates threads itself.
    std::thread::Builder::new()
        .stack_size(2 * 1024 * 1024)
        .spawn(|| {
            for (open, close) in [("[", "]"), ("{a=", "}")] {
                let raw = format!("x={}0{}", open.repeat(80), close.repeat(80));
                drop(opensip_identity::parse_toml(raw.as_bytes()).unwrap());
                let raw = format!("x={}0{}", open.repeat(81), close.repeat(81));
                assert!(matches!(
                    opensip_identity::parse_toml(raw.as_bytes()),
                    Err(opensip_identity::TomlError::RecursionLimit)
                ));
            }
            let path = std::iter::repeat_n("a", 80).collect::<Vec<_>>().join(".");
            let raw = format!("[{path}]\nx={}0{}", "[".repeat(80), "]".repeat(80));
            drop(opensip_identity::parse_toml(raw.as_bytes()).unwrap());
            let raw = format!("x={}", "[".repeat(opensip_identity::MAX_BYTES - 2));
            assert!(matches!(
                opensip_identity::parse_toml(raw.as_bytes()),
                Err(opensip_identity::TomlError::RecursionLimit)
            ));
        })
        .unwrap()
        .join()
        .unwrap();
}

#[test]
fn enumeration_join_rederives_population_and_refuses_retained_input_faults() {
    use opensip_evaluator::inspect_enumeration_join;
    use opensip_identity::TraversalBudget;
    let registry = crate::embedded_schema_registry().unwrap();
    let fixture = parse_json(include_bytes!(
        "../tests/fixtures/enumeration-join-fixtures.json"
    ))
    .unwrap();
    let f = object(&fixture);
    for (name, case) in object(&f["cases"]) {
        let c = object(case);
        let p = object(&c["request"]);
        let expected = object(&c["expected"]);
        let obs: BTreeMap<String, ObjectInput> = array(&p["objects"])
            .iter()
            .map(|key| {
                let r = object(&object(&f["objectPool"])[string(key)]);
                (
                    string(&r["id"]).into(),
                    ObjectInput {
                        domain: IdentityDomain::parse(string(&r["domain"])).unwrap(),
                        descriptor: r["descriptor"].clone(),
                    },
                )
            })
            .collect();
        let bs: BTreeMap<[u8; 32], Vec<u8>> = array(&p["blobs"])
            .iter()
            .map(|key| {
                let r = object(&object(&f["blobPool"])[string(key)]);
                (
                    bytes(string(&r["digest"])).try_into().unwrap(),
                    bytes(string(&r["hex"])),
                )
            })
            .collect();
        let inputs = RetainedInputs::new(&registry, &obs, &bs);
        let bound = |key, default| {
            p.get(key)
                .map(|v| string(v).parse::<usize>().unwrap())
                .unwrap_or(default)
        };
        let result = inspect_enumeration_join(
            &inputs,
            string(&p["planId"]),
            array(&p["inputRefs"]),
            TraversalBudget {
                steps: bound("steps", 20_000_000),
                depth: bound("walkDepth", 96),
                descriptor_work: bound("walkWork", 20_000_000),
            },
        );
        match result {
            Ok(checked) => assert_eq!(checked.value(), &expected["value"], "{name}"),
            Err(error) => {
                // Test-only classification; production errors remain typed.
                let detail = format!("{error:?}");
                if let Some(wanted) = expected.get("errorDetail") {
                    assert_eq!(detail, string(wanted), "{name}");
                }
                let class = if detail.contains("MissingObject(") || detail.contains("MissingBlob(")
                {
                    "unavailable"
                } else if detail.contains("Limit") {
                    "limited"
                } else {
                    "invalid"
                };
                assert_eq!(class, string(&expected["errorClass"]), "{name}: {detail}");
            }
        }
    }
}

#[test]
fn evaluator_parameters_bind_retained_payloads_policy_and_detector_closures() {
    use opensip_evaluator::{PolicyAdmissionError, inspect_evaluator_parameters};
    use opensip_identity::TraversalBudget;
    let registry = crate::embedded_schema_registry().unwrap();
    let fixture = parse_json(include_bytes!(
        "../tests/fixtures/evaluator-parameter-fixtures.json"
    ))
    .unwrap();
    let f = object(&fixture);
    for (name, case) in object(&f["cases"]) {
        let c = object(case);
        let p = object(&c["request"]);
        let expected = object(&c["expected"]);
        let obs: BTreeMap<String, ObjectInput> = array(&p["objects"])
            .iter()
            .map(|key| {
                let r = object(&object(&f["objectPool"])[string(key)]);
                (
                    string(&r["id"]).into(),
                    ObjectInput {
                        domain: IdentityDomain::parse(string(&r["domain"])).unwrap(),
                        descriptor: r["descriptor"].clone(),
                    },
                )
            })
            .collect();
        let bs: BTreeMap<[u8; 32], Vec<u8>> = array(&p["blobs"])
            .iter()
            .map(|key| {
                let r = object(&object(&f["blobPool"])[string(key)]);
                (
                    bytes(string(&r["digest"])).try_into().unwrap(),
                    bytes(string(&r["hex"])),
                )
            })
            .collect();
        let inputs = RetainedInputs::new(&registry, &obs, &bs);
        let bound = |key, default| {
            p.get(key)
                .map(|v| string(v).parse::<usize>().unwrap())
                .unwrap_or(default)
        };
        let result = inspect_evaluator_parameters(
            &inputs,
            string(&p["planId"]),
            TraversalBudget {
                steps: bound("steps", 20_000_000),
                depth: bound("walkDepth", 96),
                descriptor_work: bound("walkWork", 20_000_000),
            },
        );
        match result {
            Ok(value) => {
                let expected = object(&expected["value"]);
                assert_eq!(value.selected(), object(&expected["selected"]), "{name}");
                assert_eq!(value.policy(), &expected["policy"], "{name}");
                assert_eq!(value.emission(), &expected["emission"], "{name}");
            }
            Err(PolicyAdmissionError::Refused(cause)) if expected.contains_key("cause") => {
                assert_eq!(cause, string(&expected["cause"]), "{name}")
            }
            Err(error) => {
                let detail = format!("{error:?}");
                let class = if detail.contains("MissingObject(") || detail.contains("MissingBlob(")
                {
                    "unavailable"
                } else if detail.contains("Limit") {
                    "limited"
                } else {
                    "invalid"
                };
                assert_eq!(class, string(&expected["errorClass"]), "{name}: {detail}");
            }
        }
    }
}

#[test]
fn plan_input_owners_require_no_run_or_proof_output() {
    use opensip_evaluator::{
        inspect_plan_import_joins, inspect_plan_stage_specs, inspect_plan_view_joins,
    };
    use opensip_identity::TraversalBudget;
    let registry = crate::embedded_schema_registry().unwrap();
    let fixture = parse_json(include_bytes!("../tests/fixtures/plan-input-fixtures.json")).unwrap();
    let f = object(&fixture);
    for (name, case) in object(&f["cases"]) {
        let c = object(case);
        let p = object(&c["request"]);
        let expected = object(&c["expected"]);
        let obs: BTreeMap<String, ObjectInput> = array(&p["objects"])
            .iter()
            .map(|key| {
                let r = object(&object(&f["objectPool"])[string(key)]);
                assert!(
                    ![
                        "run",
                        "evaluation-seal",
                        "proof-bundle",
                        "finding",
                        "semantic-evidence",
                        "evaluation-subject",
                        "predicate-evidence"
                    ]
                    .contains(&string(&r["domain"])),
                    "{name}: output dependency"
                );
                (
                    string(&r["id"]).into(),
                    ObjectInput {
                        domain: IdentityDomain::parse(string(&r["domain"])).unwrap(),
                        descriptor: r["descriptor"].clone(),
                    },
                )
            })
            .collect();
        let bs: BTreeMap<[u8; 32], Vec<u8>> = array(&p["blobs"])
            .iter()
            .map(|key| {
                let r = object(&object(&f["blobPool"])[string(key)]);
                (
                    bytes(string(&r["digest"])).try_into().unwrap(),
                    bytes(string(&r["hex"])),
                )
            })
            .collect();
        let inputs = RetainedInputs::new(&registry, &obs, &bs);
        let bound = |key, default| {
            p.get(key)
                .map(|v| string(v).parse::<usize>().unwrap())
                .unwrap_or(default)
        };
        let budget = TraversalBudget {
            steps: bound("steps", 20_000_000),
            depth: bound("walkDepth", 96),
            descriptor_work: bound("walkWork", 20_000_000),
        };
        let count = |n| V::Integer(opensip_identity::JsonInteger::new(n as i128).unwrap());
        let result = match string(&p["mode"]) {
            "plan-imports" => inspect_plan_import_joins(&inputs, string(&p["planId"]), budget)
                .map(|v| BTreeMap::from([("imports".into(), count(v.import_count()))]))
                .map_err(|e| format!("{e:?}")),
            "plan-stages" => inspect_plan_stage_specs(
                &inputs,
                string(&p["planId"]),
                string(&p["executionId"]),
                budget,
            )
            .map(|v| BTreeMap::from([("stages".into(), count(v.stage_count()))]))
            .map_err(|e| format!("{e:?}")),
            "plan-view" => inspect_plan_view_joins(
                &inputs,
                string(&p["planId"]),
                string(&p["viewId"]),
                array(&p["inputRefs"]),
                budget,
            )
            .map(|v| {
                BTreeMap::from([
                    ("scopes".into(), count(v.scope_count())),
                    ("facts".into(), count(v.fact_count())),
                    ("coverage".into(), count(v.coverage_count())),
                ])
            })
            .map_err(|e| format!("{e:?}")),
            _ => panic!("unknown fixture owner"),
        };
        match result {
            Ok(mut value) => {
                value.insert("result".into(), V::String("checked".into()));
                assert_eq!(&V::Object(value), &expected["value"], "{name}");
            }
            Err(error) if expected.contains_key("error") => {
                assert_eq!(error, string(&expected["error"]), "{name}")
            }
            Err(error) => {
                let class = if error.contains("MissingObject(") || error.contains("MissingBlob(") {
                    "unavailable"
                } else if error.contains("Limit") {
                    "limited"
                } else {
                    "invalid"
                };
                assert_eq!(class, string(&expected["errorClass"]), "{name}: {error}");
            }
        }
    }
}

#[test]
fn execution_inputs_recheck_retained_selection_and_capture_without_outputs() {
    let f = parse_json(include_bytes!(
        "../tests/fixtures/execution-input-fixtures.json"
    ))
    .unwrap();
    let f = object(&f);
    let registry = crate::embedded_schema_registry().unwrap();
    for cv in array(&f["cases"]) {
        let c = object(cv);
        let name = string(&c["label"]);
        let obs = array(&c["objects"])
            .iter()
            .map(|k| {
                let r = object(&object(&f["objectPool"])[string(k)]);
                let dom = IdentityDomain::parse(string(&r["domain"])).unwrap();
                assert!(
                    ![
                        IdentityDomain::Run,
                        IdentityDomain::EvaluationSeal,
                        IdentityDomain::ProofBundle,
                        IdentityDomain::Finding,
                        IdentityDomain::SemanticEvidence,
                        IdentityDomain::EvaluationSubject
                    ]
                    .contains(&dom)
                );
                (
                    string(&r["id"]).into(),
                    ObjectInput {
                        domain: dom,
                        descriptor: r["descriptor"].clone(),
                    },
                )
            })
            .collect();
        let bs = array(&c["blobs"])
            .iter()
            .map(|k| {
                let r = object(&object(&f["blobPool"])[string(k)]);
                (
                    bytes(string(&r["digest"])).try_into().unwrap(),
                    bytes(string(&r["hex"])),
                )
            })
            .collect();
        let inputs = RetainedInputs::new(&registry, &obs, &bs);
        let bound = |k, default| {
            c.get(k)
                .map(|v| {
                    if let V::Integer(n) = v {
                        usize::try_from(n.get()).unwrap()
                    } else {
                        panic!("bound")
                    }
                })
                .unwrap_or(default)
        };
        let actual = opensip_evaluator::inspect_execution_input_join(
            &inputs,
            string(&c["planId"]),
            string(&c["executionId"]),
            string(&c["evaluatorClosure"]),
            array(&c["inputRefs"]),
            opensip_identity::TraversalBudget {
                steps: bound("steps", 20_000_000),
                depth: bound("depth", 96),
                descriptor_work: bound("descriptorWork", 20_000_000),
            },
        );
        let expected = object(&c["expected"]);
        match actual {
            Ok(v) => {
                assert_eq!(Some(v.value()), expected.get("value"), "{name}");
                let capture = array(&c["inputRefs"])
                    .iter()
                    .find(|rf| string(&object(rf)["domain"]) == "execution-inputs")
                    .unwrap();
                assert_eq!(
                    digest_hex(&v.input_digest()),
                    string(&object(capture)["digest"]),
                    "{name}: retained capture identity"
                );
            }
            Err(e) => {
                let message = format!("{e:?}");
                let want = string(&expected["error"]);
                assert_eq!(message, want, "{name}")
            }
        }
    }
}

#[test]
fn plan_policy_compilation_needs_no_claimed_program_or_run() {
    use opensip_evaluator::{PolicyAdmissionError, compile_plan_policy};
    use opensip_identity::{GraphError, TraversalBudget};
    let registry = crate::embedded_schema_registry().unwrap();
    let fixture = parse_json(include_bytes!(
        "../tests/fixtures/plan-policy-fixtures.json"
    ))
    .unwrap();
    let fixture = object(&fixture);
    let mut n = 0;
    for cv in array(&fixture["cases"]) {
        let c = object(cv);
        let q = object(&c["request"]);
        let expected = object(&c["expected"]);
        let name = string(&q["label"]);
        let obs = array(&q["objects"])
            .iter()
            .map(|k| {
                let r = object(&object(&fixture["objectPool"])[string(k)]);
                (
                    string(&r["id"]).into(),
                    ObjectInput {
                        domain: IdentityDomain::parse(string(&r["domain"])).unwrap(),
                        descriptor: r["descriptor"].clone(),
                    },
                )
            })
            .collect::<BTreeMap<_, _>>();
        assert!(obs.values().all(|v| {
            ![
                IdentityDomain::Run,
                IdentityDomain::EvaluationSeal,
                IdentityDomain::ProofBundle,
            ]
            .contains(&v.domain)
        }));
        let bs = array(&q["blobs"])
            .iter()
            .map(|r| {
                let r = object(&object(&fixture["blobPool"])[string(r)]);
                (
                    bytes(string(&r["digest"])).try_into().unwrap(),
                    bytes(string(&r["hex"])),
                )
            })
            .collect();
        let inputs = RetainedInputs::new(&registry, &obs, &bs);
        let steps = q
            .get("steps")
            .map(|v| string(v).parse().unwrap())
            .unwrap_or(10_000_000);
        let result = compile_plan_policy(
            &inputs,
            string(&q["planId"]),
            TraversalBudget {
                steps,
                depth: 96,
                descriptor_work: 10_000_000,
            },
        );
        let actual = match result {
            Ok(v) => {
                assert_eq!(v.policy(), &expected["policy"], "{name}");
                assert_eq!(v.waiver(), &expected["waiver"], "{name}");
                assert_eq!(v.program(), &expected["program"], "{name}");
                assert_eq!(
                    digest_hex(&v.program_digest()),
                    string(&expected["digest"]),
                    "{name}"
                );
                "checked"
            }
            Err(PolicyAdmissionError::Refused(cause)) => {
                assert_eq!(cause, string(&expected["cause"]), "{name}");
                "refused"
            }
            Err(PolicyAdmissionError::Limit) => "limit",
            Err(PolicyAdmissionError::Record(GraphError::Input(
                RetainedInputError::MissingObject(_) | RetainedInputError::MissingBlob(_),
            ))) => "unavailable",
            Err(_) => "invalid",
        };
        assert_eq!(actual, string(&expected["result"]), "{name}");
        n += 1;
    }
    std::println!("Plan policy no-output reference cases {n}");
}

#[test]
fn first_evaluation_structure_uses_only_retained_inputs() {
    let f = parse_json(include_bytes!(
        "../tests/fixtures/execution-input-fixtures.json"
    ))
    .unwrap();
    let f = object(&f);
    let registry = crate::embedded_schema_registry().unwrap();
    let mut n = 0;
    let mut results: BTreeMap<String, V> = BTreeMap::new();
    for cv in array(&f["cases"]) {
        let c = object(cv);
        let expected = object(&c["expected"]);
        if !expected.contains_key("value") {
            continue;
        }
        let name = string(&c["label"]);
        let obs = array(&c["objects"])
            .iter()
            .map(|k| {
                let r = object(&object(&f["objectPool"])[string(k)]);
                let dom = IdentityDomain::parse(string(&r["domain"])).unwrap();
                assert!(
                    ![
                        IdentityDomain::Run,
                        IdentityDomain::EvaluationSeal,
                        IdentityDomain::ProofBundle,
                        IdentityDomain::Finding,
                        IdentityDomain::SemanticEvidence,
                        IdentityDomain::EvaluationSubject
                    ]
                    .contains(&dom)
                );
                (
                    string(&r["id"]).into(),
                    ObjectInput {
                        domain: dom,
                        descriptor: r["descriptor"].clone(),
                    },
                )
            })
            .collect();
        let bs = array(&c["blobs"])
            .iter()
            .map(|k| {
                let r = object(&object(&f["blobPool"])[string(k)]);
                (
                    bytes(string(&r["digest"])).try_into().unwrap(),
                    bytes(string(&r["hex"])),
                )
            })
            .collect();
        let inputs = RetainedInputs::new(&registry, &obs, &bs);
        let budget = opensip_identity::TraversalBudget {
            steps: 20_000_000,
            depth: 96,
            descriptor_work: 20_000_000,
        };
        let result = opensip_evaluator::inspect_first_evaluation_structure(
            &inputs,
            string(&c["planId"]),
            string(&c["executionId"]),
            string(&c["evaluatorClosure"]),
            array(&c["inputRefs"]),
            opensip_evaluator::RetainedWalkLimits {
                walk: budget,
                owner: budget,
                owner_invocations: 100_000,
            },
        );
        match result {
            Ok(v) => {
                assert_eq!(
                    string(&object(&expected["value"])["result"]),
                    "ADMIT",
                    "{name}"
                );
                assert_eq!(v.execution_inputs().value(), &expected["value"], "{name}");
                assert!(v.object_count() > 0 && v.context_count() > 0 && v.universe_count() > 0);
                results.insert(
                    name.into(),
                    V::String(format!(
                        "objects {} contexts {} universes {} owners {}",
                        v.object_count(),
                        v.context_count(),
                        v.universe_count(),
                        v.owner_invocations()
                    )),
                );
            }
            Err(opensip_evaluator::RetainedWalkError::ExecutionRefused(v)) => {
                assert_eq!(v, expected["value"], "{name}")
            }
            Err(e) => {
                results.insert(name.into(), V::String(format!("ERROR {e:?}")));
            }
        }
        n += 1;
    }
    assert!(
        results.values().all(|v| !string(v).starts_with("ERROR")),
        "new input owner failures: {results:?}"
    );
    std::println!("first evaluation no-output cases {n}");
}

#[test]
fn first_evaluation_structure_controls() {
    let registry = crate::embedded_schema_registry().unwrap();
    let fixture = parse_json(include_bytes!(
        "../tests/fixtures/input-structure-fixtures.json"
    ))
    .unwrap();
    let fixture = object(&fixture);
    for cv in array(&fixture["cases"]) {
        let q = object(cv);
        let name = string(&q["label"]);
        let obs = array(&q["objects"])
            .iter()
            .map(|k| {
                let r = object(&object(&fixture["objectPool"])[string(k)]);
                (
                    string(&r["id"]).into(),
                    ObjectInput {
                        domain: IdentityDomain::parse(string(&r["domain"])).unwrap(),
                        descriptor: r["descriptor"].clone(),
                    },
                )
            })
            .collect::<BTreeMap<_, _>>();
        let bs = array(&q["blobs"])
            .iter()
            .map(|r| {
                let r = object(&object(&fixture["blobPool"])[string(r)]);
                (
                    bytes(string(&r["digest"])).try_into().unwrap(),
                    bytes(string(&r["hex"])),
                )
            })
            .collect();
        let inputs = RetainedInputs::new(&registry, &obs, &bs);
        let budget = opensip_identity::TraversalBudget {
            steps: 20_000_000,
            depth: 96,
            descriptor_work: 20_000_000,
        };
        let bound = |k, default| {
            q.get(k)
                .map(|v| {
                    if let V::Integer(n) = v {
                        usize::try_from(n.get()).unwrap()
                    } else {
                        panic!("bound")
                    }
                })
                .unwrap_or(default)
        };
        let x = opensip_evaluator::inspect_execution_input_join(
            &inputs,
            string(&q["planId"]),
            string(&q["executionId"]),
            string(&q["evaluatorClosure"]),
            array(&q["inputRefs"]),
            budget,
        );
        let x_status = match x {
            Ok(v) => string(&object(v.value())["result"]).to_owned(),
            Err(e) => format!("{e:?}"),
        };
        let limits = opensip_evaluator::RetainedWalkLimits {
            walk: opensip_identity::TraversalBudget {
                steps: bound("walkSteps", budget.steps),
                depth: bound("walkDepth", budget.depth),
                ..budget
            },
            owner: opensip_identity::TraversalBudget {
                steps: bound("ownerSteps", budget.steps),
                depth: bound("ownerDepth", budget.depth),
                ..budget
            },
            owner_invocations: bound("ownerInvocations", 100_000),
        };
        let result = opensip_evaluator::inspect_first_evaluation_structure(
            &inputs,
            string(&q["planId"]),
            string(&q["executionId"]),
            string(&q["evaluatorClosure"]),
            array(&q["inputRefs"]),
            limits,
        );
        let status = match result {
            Ok(_) => {
                assert_eq!(string(&q["expect"]), "admit", "{name}");
                "ADMIT".into()
            }
            Err(e) => {
                assert_eq!(string(&q["expect"]), "refuse", "{name}: {e:?}");
                format!("{e:?}")
            }
        };
        let expected = object(&q["expected"]);
        assert_eq!(
            x_status,
            string(&expected["executionJoin"]),
            "{name}: execution boundary"
        );
        assert_eq!(
            status,
            string(&expected["structure"]),
            "{name}: structural boundary"
        );
    }
}

#[test]
fn reconstructs_retained_evaluator_inputs_without_run_outputs() {
    let registry = crate::embedded_schema_registry().unwrap();
    let fixture = parse_json(include_bytes!(
        "../tests/fixtures/reconstruction-fixtures.json"
    ))
    .unwrap();
    let fixture = object(&fixture);
    let cases = array(&fixture["cases"]);
    assert_eq!(cases.len(), 87);
    for cv in cases {
        let q = object(cv);
        let name = string(&q["label"]);
        let obs = array(&q["objects"])
            .iter()
            .map(|key| {
                let r = object(&object(&fixture["objectPool"])[string(key)]);
                (
                    string(&r["id"]).into(),
                    ObjectInput {
                        domain: IdentityDomain::parse(string(&r["domain"])).unwrap(),
                        descriptor: r["descriptor"].clone(),
                    },
                )
            })
            .collect::<BTreeMap<_, _>>();
        assert!(obs.values().all(|v| {
            ![
                IdentityDomain::Run,
                IdentityDomain::EvaluationSeal,
                IdentityDomain::ProofBundle,
                IdentityDomain::Finding,
                IdentityDomain::SemanticEvidence,
                IdentityDomain::EvaluationSubject,
            ]
            .contains(&v.domain)
        }));
        let bs = array(&q["blobs"])
            .iter()
            .map(|key| {
                let r = object(&object(&fixture["blobPool"])[string(key)]);
                (
                    bytes(string(&r["digest"])).try_into().unwrap(),
                    bytes(string(&r["hex"])),
                )
            })
            .collect();
        let inputs = RetainedInputs::new(&registry, &obs, &bs);
        let bound = |key, default| {
            q.get(key)
                .map(|v| match v {
                    V::Integer(n) => usize::try_from(n.get()).unwrap(),
                    _ => panic!("invalid bound"),
                })
                .unwrap_or(default)
        };
        let b = opensip_identity::TraversalBudget {
            steps: 20_000_000,
            depth: 96,
            descriptor_work: 20_000_000,
        };
        let actual = opensip_evaluator::reconstruct_evaluator_inputs(
            &inputs,
            string(&q["planId"]),
            string(&q["executionId"]),
            string(&q["evaluatorClosure"]),
            array(&q["inputRefs"]),
            opensip_evaluator::RetainedWalkLimits {
                walk: opensip_identity::TraversalBudget {
                    steps: bound("walkSteps", b.steps),
                    ..b
                },
                owner: opensip_identity::TraversalBudget {
                    steps: bound("ownerSteps", b.steps),
                    ..b
                },
                owner_invocations: bound("ownerInvocations", 100_000),
            },
        );
        let expected = object(&object(&fixture["expectedPool"])[string(&q["expected"])]);
        if let Some(e) = expected.get("typedError") {
            assert_eq!(
                format!(
                    "{:?}",
                    actual.err().expect("expected reconstruction refusal")
                ),
                string(e),
                "{name}"
            );
            continue;
        }
        match actual {
            Ok(v) => {
                assert_eq!(
                    v.normalized(),
                    &expected["normalized"],
                    "{name}: normalized"
                );
                assert_eq!(v.evidence(), &expected["evidence"], "{name}: evidence");
            }
            Err(opensip_evaluator::ReconstructionError::Structure(
                opensip_evaluator::RetainedWalkError::ExecutionRefused(v),
            )) => {
                let refs = array(&object(&v)["refusals"])
                    .iter()
                    .map(string)
                    .collect::<Vec<_>>()
                    .join(",");
                assert_eq!(
                    format!("EVALUATOR_EXECUTION_INPUTS_JOIN:{refs}"),
                    string(&expected["refused"]),
                    "{name}"
                );
            }
            Err(opensip_evaluator::ReconstructionError::Structure(
                opensip_evaluator::RetainedWalkError::Execution(
                    opensip_evaluator::ExecutionInputError::Refused(cause),
                ),
            )) => {
                assert_eq!(cause, "EVALUATOR_ENUMERATION_JOIN", "{name}");
                assert!(
                    string(&expected["refused"]).starts_with("EVALUATOR_ENUMERATION_JOIN:"),
                    "{name}"
                );
            }
            Err(opensip_evaluator::ReconstructionError::Refused(cause)) => {
                assert_eq!(cause, string(&expected["refused"]), "{name}")
            }
            Err(e) => panic!("{name}: {e:?}"),
        }
    }
}
