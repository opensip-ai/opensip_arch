//! Independent native-owners-08 negatives. Not part of the frozen subject.
use opensip_evaluator::{
    NativeContextError, PlanCapabilityError, admit_plan_capability, inspect_native_context,
};
use opensip_identity::{
    GraphError, IdentityCandidate, IdentityDomain, JsonValue as V, ObjectInput, RetainedInputError,
    RetainedInputs, digest_hex, hash_preimage, parse_json, raw_sha256,
};
use std::collections::BTreeMap;

fn object(v: &V) -> &BTreeMap<String, V> {
    let V::Object(o) = v else { panic!("object") };
    o
}
fn object_mut(v: &mut V) -> &mut BTreeMap<String, V> {
    let V::Object(o) = v else { panic!("object") };
    o
}
fn array(v: &V) -> &[V] {
    let V::Array(a) = v else { panic!("array") };
    a
}
fn string(v: &V) -> &str {
    let V::String(s) = v else { panic!("string") };
    s
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
        "../../../subject/product/crates/host/tests/fixtures/native-context-fixtures.json"
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

fn main() {
    let mut failures = Vec::new();
    let check = |failures: &mut Vec<String>, name: &str, ok: bool, detail: String| {
        println!("{} {} {}", if ok { "PASS" } else { "FAIL" }, name, detail);
        if !ok {
            failures.push(format!("{name}: {detail}"));
        }
    };
    let registry = opensip_host::embedded_schema_registry().unwrap();
    let fixture = native_fixture();
    let obs = objects(&fixture);

    let (id, bs) = frame("syntax", &context(&fixture, "syntax"));
    let inputs = RetainedInputs::new(&registry, &obs, &bs);
    let checked = inspect_native_context(&inputs, id, WORK).unwrap();
    check(
        &mut failures,
        "syntax-positive-without-member-blobs",
        checked.refusals().is_empty() && bs.len() == 1,
        format!("refusals={} blobs={}", checked.refusals().len(), bs.len()),
    );
    check(
        &mut failures,
        "budget-zero-is-limit-not-unretained",
        matches!(
            inspect_native_context(&inputs, id, 0),
            Err(NativeContextError::Frame(GraphError::Limit))
                | Err(NativeContextError::Frame(GraphError::Schema(
                    opensip_identity::SchemaAdmissionError::Schema(
                        opensip_identity::SchemaError::Limit
                    )
                )))
        ),
        "Limit".into(),
    );

    let mut missing = objects(&fixture);
    let key = string(&object(&object(&context(&fixture, "syntax"))["grammarBundle"])["closureId"])
        .to_owned();
    let mut removed = missing.remove(&key).unwrap();
    let result = inspect_native_context(&RetainedInputs::new(&registry, &missing, &bs), id, WORK)
        .unwrap();
    check(
        &mut failures,
        "missing-closure-is-unretained",
        result.refusals() == ["native.native-context-closure-unretained:grammarBundle.closureId"],
        result.refusals().join(","),
    );
    object_mut(&mut removed.descriptor)
        .insert("semanticVersion".into(), V::String("changed".into()));
    missing.insert(key.clone(), removed);
    let result = inspect_native_context(&RetainedInputs::new(&registry, &missing, &bs), id, WORK)
        .unwrap();
    check(
        &mut failures,
        "changed-descriptor-is-identity-mismatch",
        result.refusals()
            == ["native.native-context-closure-identity-mismatch:grammarBundle.closureId"],
        result.refusals().join(","),
    );

    let mut kinded = objects(&fixture);
    let mut rec = kinded.get(&key).unwrap().descriptor.clone();
    object_mut(&mut rec).insert("kind".into(), V::String("provider".into()));
    let raw = opensip_identity::canonical_bytes(&rec).unwrap();
    let new_id = IdentityCandidate::from_json(&registry, IdentityDomain::Closure, &raw, WORK)
        .unwrap()
        .identifier()
        .to_owned();
    kinded.insert(
        new_id.clone(),
        ObjectInput {
            domain: IdentityDomain::Closure,
            descriptor: rec,
        },
    );
    let mut desc = context(&fixture, "syntax");
    object_mut(object_mut(&mut desc).get_mut("grammarBundle").unwrap())
        .insert("closureId".into(), V::String(new_id));
    let (id2, bs2) = frame("syntax", &desc);
    let result =
        inspect_native_context(&RetainedInputs::new(&registry, &kinded, &bs2), id2, WORK).unwrap();
    check(
        &mut failures,
        "rekeyed-wrong-kind-is-kind-mismatch-not-unretained",
        result
            .refusals()
            .iter()
            .any(|s| s == "native.native-context-closure-kind-mismatch:grammarBundle.closureId")
            && !result.refusals().iter().any(|s| s.contains("unretained")),
        result.refusals().join(","),
    );

    let mut descriptor = context(&fixture, "syntax");
    let V::Array(grammars) = object_mut(
        object_mut(&mut descriptor)
            .get_mut("grammarBundle")
            .unwrap(),
    )
    .get_mut("grammars")
    .unwrap() else {
        panic!("grammars")
    };
    let grammar = grammars
        .iter_mut()
        .find(|g| string(&object(g)["languageId"]) == "json")
        .unwrap();
    object_mut(grammar).insert("syntaxClass".into(), V::String("code".into()));
    let (id, bs) = frame("syntax", &descriptor);
    let result = inspect_native_context(&RetainedInputs::new(&registry, &obs, &bs), id, WORK).unwrap();
    check(
        &mut failures,
        "reframed-json-cannot-promote-to-code",
        result.refusals().iter().any(|s| {
            s == "native.syntax-grammar-class-not-the-registered-one:json:declared=code:registered=data-document"
        }),
        result.refusals().join(","),
    );

    let plan_fix = parse_json(include_bytes!(
        "../../../subject/product/crates/host/tests/fixtures/plan-capability-fixture.json"
    ))
    .unwrap();
    let mut pobs = objects(&plan_fix);
    let plan_id = string(&object(&plan_fix)["planId"]).to_owned();
    let row = object(&array(&object(&plan_fix)["blobs"])[0]);
    let digest: [u8; 32] = bytes(string(&row["digest"])).try_into().unwrap();
    let raw = bytes(string(&row["hex"]));
    let mut pbs = BTreeMap::from([(digest, raw.clone())]);
    let admitted =
        admit_plan_capability(&RetainedInputs::new(&registry, &pobs, &pbs), &plan_id, WORK).unwrap();
    check(
        &mut failures,
        "plan-golden-bytes-join-then-gates",
        digest_hex(&admitted.identity())
            == "508f24c718a0564c52fe18a1e6a5308d53bdd6012a50ad186ffbc208bb18881b",
        digest_hex(&admitted.identity()),
    );

    let bad = vec![255];
    let bad_digest = raw_sha256(&bad);
    pbs.insert(bad_digest, bad.clone());
    let mut other = pobs[&plan_id].descriptor.clone();
    object_mut(&mut other).insert(
        "capabilityManifestBytesDigest".into(),
        V::String(digest_hex(&bad_digest)),
    );
    object_mut(&mut other).insert("capabilityManifestId".into(), V::String("0".repeat(64)));
    let rawp = opensip_identity::canonical_bytes(&other).unwrap();
    let id = IdentityCandidate::from_json(&registry, IdentityDomain::Plan, &rawp, WORK)
        .unwrap()
        .identifier()
        .to_owned();
    pobs.insert(
        id.clone(),
        ObjectInput {
            domain: IdentityDomain::Plan,
            descriptor: other,
        },
    );
    check(
        &mut failures,
        "malformed-bytes-wrong-id-is-bytes-join-not-codec",
        matches!(
            admit_plan_capability(&RetainedInputs::new(&registry, &pobs, &pbs), &id, WORK),
            Err(PlanCapabilityError::BytesJoin)
        ),
        "BytesJoin".into(),
    );

    let identity = digest_hex(&raw_sha256(
        &[b"opensip.capability-manifest.v1\0".as_slice(), bad.as_slice()].concat(),
    ));
    let mut other = pobs[&id].descriptor.clone();
    object_mut(&mut other).insert("capabilityManifestId".into(), V::String(identity));
    let rawp = opensip_identity::canonical_bytes(&other).unwrap();
    let id2 = IdentityCandidate::from_json(&registry, IdentityDomain::Plan, &rawp, WORK)
        .unwrap()
        .identifier()
        .to_owned();
    pobs.insert(
        id2.clone(),
        ObjectInput {
            domain: IdentityDomain::Plan,
            descriptor: other,
        },
    );
    check(
        &mut failures,
        "malformed-bytes-matching-id-reaches-manifest-after-join",
        matches!(
            admit_plan_capability(&RetainedInputs::new(&registry, &pobs, &pbs), &id2, WORK),
            Err(PlanCapabilityError::Manifest(_))
        ),
        "Manifest".into(),
    );

    let mut objects = BTreeMap::new();
    let blobs = BTreeMap::new();
    let producer = {
        let value = parse_json(
            format!(
                r#"{{"schemaVersion":2,"kind":"provider","manifestDigest":"{}","tree":[],"semanticVersion":"1.0.0","protocolMajor":3,"platform":"macos-aarch64"}}"#,
                "0".repeat(64)
            )
            .as_bytes(),
        )
        .unwrap();
        let raw = opensip_identity::canonical_bytes(&value).unwrap();
        let key = IdentityCandidate::from_json(&registry, IdentityDomain::Closure, &raw, WORK)
            .unwrap()
            .identifier()
            .to_owned();
        objects.insert(
            key.clone(),
            ObjectInput {
                domain: IdentityDomain::Closure,
                descriptor: value,
            },
        );
        key
    };
    let z = "0".repeat(64);
    let fact = parse_json(
        format!(
            r#"{{"schemaVersion":2,"snapshotId":"snapshot2:{z}","relation":"file","resolution":"enumerated","sourceUniverse":"{z}","targetUniverse":"{z}","producerClosure":"{producer}","payloadSchemaDigest":"{z}","payloadDigest":"{z}","anchors":[],"confidenceMillionths":0}}"#
        )
        .as_bytes(),
    )
    .unwrap();
    let raw = opensip_identity::canonical_bytes(&fact).unwrap();
    let fkey = IdentityCandidate::from_json(&registry, IdentityDomain::Fact, &raw, WORK)
        .unwrap()
        .identifier()
        .to_owned();
    objects.insert(
        fkey.clone(),
        ObjectInput {
            domain: IdentityDomain::Fact,
            descriptor: fact,
        },
    );
    let walked = RetainedInputs::new(&registry, &objects, &blobs).inspect_local_structure(
        &fkey,
        IdentityDomain::Fact,
        opensip_identity::TraversalBudget {
            steps: 10_000,
            depth: 64,
            descriptor_work: WORK,
        },
    );
    check(
        &mut failures,
        "graph-relation-still-unsupported",
        matches!(
            walked,
            Err(GraphError::Unsupported("payload-class owner joins"))
        ),
        "unsupported".into(),
    );

    let _ = RetainedInputError::MissingBlob([0; 32]);
    println!("failures={}", failures.len());
    if !failures.is_empty() {
        std::process::exit(1);
    }
    println!("ALL_PASS");
}
