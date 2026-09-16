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
