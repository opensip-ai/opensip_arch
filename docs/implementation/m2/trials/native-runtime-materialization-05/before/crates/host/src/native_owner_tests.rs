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
    parse_json(include_bytes!(
        "../tests/fixtures/native-context-fixtures.json"
    ))
    .unwrap()
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
