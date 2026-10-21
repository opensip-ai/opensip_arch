//! Synthetic host projections, not descriptor/Plan/source qualification.
use super::super::super::super::cbor;
use super::*;
use opensip_identity::{JsonInteger, canonical_bytes};

fn wire(v: &J) -> Value {
    match v {
        J::Null => Value::Null,
        J::Bool(v) => Value::Bool(*v),
        J::Integer(v) => Value::Unsigned(u64::try_from(v.get()).unwrap()),
        J::String(v) => t(v),
        J::Array(v) => Value::Array(v.iter().map(wire).collect()),
        J::Object(v) => Value::Map(v.iter().map(|(k, v)| (k.clone(), wire(v))).collect()),
    }
}
fn tokens() -> Vec<String> {
    [
        "coverage-v3",
        "fact-identity-fact2",
        "plan-identity-plan2",
        "source-identity-snapshot2",
    ]
    .into_iter()
    .map(str::to_owned)
    .collect()
}
fn fixture() -> Value {
    let j = parse_json(include_bytes!(
        "../../../../tests/data/rust3-startup-shape.v1.json"
    ))
    .unwrap();
    wire(at(&j, &["universeAccepted"]).unwrap())
}
fn identity() -> Value {
    let f = fixture();
    let universe = member(&f, "universe").unwrap();
    map([
        "protocolMajor",
        "providerBuildId",
        "rustCommitHash",
        "sysrootDigest",
        "hostTriple",
        "targetTriple",
    ]
    .into_iter()
    .map(|k| (k, member(universe, k).unwrap().clone()))
    .collect())
}
fn open() -> Open {
    let f = fixture();
    let string = |k| {
        let Some(Value::Text(v)) = member(&f, k) else {
            panic!()
        };
        v.clone()
    };
    Open {
        execution_id: string("executionId"),
        snapshot_id: string("snapshotId"),
        plan_id: string("planId"),
        plan_intent_commitment: format!("sha256:{}", "2".repeat(64)),
        universe: member(&f, "universe").unwrap().clone(),
        repository_resolution: member(&f, "repositoryResolution").unwrap().clone(),
    }
}
fn replace(value: &mut Value, key: &str, new: Value) {
    let Value::Map(fields) = value else { panic!() };
    *fields.iter_mut().find(|(k, _)| k == key).unwrap() = (key.into(), new);
}
fn properties(value: &mut J) -> &mut BTreeMap<String, J> {
    let J::Object(v) = value else { panic!() };
    let J::Object(v) = v.get_mut("$defs").unwrap() else {
        panic!()
    };
    let J::Object(v) = v.get_mut("ProtocolLimitsV3").unwrap() else {
        panic!()
    };
    let J::Object(v) = v.get_mut("properties").unwrap() else {
        panic!()
    };
    v
}

#[test]
fn selected_32_member_policy_and_hello_are_exact_not_defaulted() {
    let policy = Policy::load().unwrap();
    let hello = policy.hello("host", identity(), &tokens()).unwrap();
    let h = parse_json(HANDSHAKE).unwrap();
    let expected = object(at(&h, &["$defs", "ProtocolLimitsV3", "properties"]).unwrap()).unwrap();
    assert_eq!(expected.len(), 32);
    let limits = Value::Map(
        expected
            .iter()
            .map(|(k, v)| (k.clone(), wire(at(v, &["const"]).unwrap())))
            .collect(),
    );
    assert_eq!(member(&hello, "limits"), Some(&limits));
    assert_eq!(
        cbor::encode(member(&hello, "limits").unwrap()),
        cbor::encode(&limits)
    );
    assert_eq!(policy.limit("maxFramePayloadBytes").unwrap(), 67_108_864);
    assert_eq!(
        policy.limit("maxRequestPayloadBytesTotal").unwrap(),
        9_663_676_416
    );
    assert!(policy.limit("guessedLimit").is_err());
    for (key, current) in &policy.limits {
        let mut mutated = parse_json(HANDSHAKE).unwrap();
        properties(&mut mutated)
            .get_mut(key)
            .unwrap()
            .clone_from(&J::Object(BTreeMap::from([(
                "const".into(),
                J::Integer(JsonInteger::new(i128::from(current + 1)).unwrap()),
            )])));
        assert!(
            Policy::from_sources(&canonical_bytes(&mutated).unwrap(), RPP).is_err(),
            "{key}"
        );
        let mut altered = Policy::load().unwrap();
        *altered.limits.get_mut(key).unwrap() += 1;
        assert!(
            altered.hello("host", identity(), &tokens()).is_err(),
            "{key}"
        );
    }
    let mut missing = parse_json(HANDSHAKE).unwrap();
    properties(&mut missing).remove("maxScratchBytes");
    assert!(Policy::from_sources(&canonical_bytes(&missing).unwrap(), RPP).is_err());
    let mut extra = parse_json(HANDSHAKE).unwrap();
    properties(&mut extra).insert("policyId".into(), J::Null);
    assert!(Policy::from_sources(&canonical_bytes(&extra).unwrap(), RPP).is_err());
    let mut boolean = parse_json(HANDSHAKE).unwrap();
    properties(&mut boolean).insert(
        "maxScratchBytes".into(),
        J::Object(BTreeMap::from([("const".into(), J::Bool(true))])),
    );
    assert!(Policy::from_sources(&canonical_bytes(&boolean).unwrap(), RPP).is_err());
}

#[test]
fn hello_keeps_exact_selection_and_rejects_bad_rows_without_negotiating_off() {
    let policy = Policy::load().unwrap();
    for mask in 0..8 {
        let mut caps = tokens();
        for (bit, token) in [
            "subject-scope-reference-v1",
            "symbol-census-v1",
            "target-attribution-v2",
        ]
        .into_iter()
        .enumerate()
        {
            if mask & (1 << bit) != 0 {
                caps.push(token.into());
            }
        }
        caps.sort();
        let hello = policy.hello("host", identity(), &caps).unwrap();
        assert_eq!(
            member(&hello, "expectedCapabilities"),
            Some(&Value::Array(caps.iter().map(|c| t(c)).collect()))
        );
    }
    let mut bad = tokens();
    bad.swap(0, 1);
    assert!(policy.hello("host", identity(), &bad).is_err());
    let mut bad = tokens();
    bad.push(bad.last().unwrap().clone());
    assert!(policy.hello("host", identity(), &bad).is_err());
    let mut bad = tokens();
    bad.remove(0);
    assert!(policy.hello("host", identity(), &bad).is_err());
    let mut bad = tokens();
    bad.push("unknown-token".into());
    assert!(policy.hello("host", identity(), &bad).is_err());
    assert!(policy.hello("", identity(), &tokens()).is_err());
    let mut id = identity();
    replace(&mut id, "rustCommitHash", t(&"a".repeat(64)));
    assert!(policy.hello("host", id, &tokens()).is_err());
}

#[test]
fn open_checks_literal_identity_and_resolution_joins_before_host_dispatch() {
    let policy = Policy::load().unwrap();
    let hello = policy.hello("host", identity(), &tokens()).unwrap();
    let accepted = policy.open(&hello, open()).unwrap();
    let f = fixture();
    for key in [
        "executionId",
        "snapshotId",
        "planId",
        "providerId",
        "universe",
        "repositoryResolution",
    ] {
        assert_eq!(member(&accepted, key), member(&f, key));
    }
    for (key, value) in [
        ("protocolMajor", Value::Unsigned(4)),
        ("providerBuildId", t("different")),
        ("rustCommitHash", t(&"b".repeat(40))),
        ("sysrootDigest", t(&"b".repeat(64))),
        ("hostTriple", t("x86_64-apple-darwin")),
        ("targetTriple", t("x86_64-apple-darwin")),
    ] {
        let mut input = open();
        replace(&mut input.universe, key, value);
        assert!(
            matches!(
                policy.open(&hello, input),
                Err(Refusal::Join("Hello/universe identity"))
            ),
            "{key}"
        );
    }
    for key in ["dependencySourceSetId", "preparedOutputSetId"] {
        let mut input = open();
        replace(
            &mut input.repository_resolution,
            key,
            t(&format!("sha256:{}", "b".repeat(64))),
        );
        assert!(policy.open(&hello, input).is_err());
    }
    let mut input = open();
    replace(
        &mut input.repository_resolution,
        "workerExecutesRepositoryCode",
        Value::Bool(true),
    );
    assert!(policy.open(&hello, input).is_err());
    let mut input = open();
    input.plan_id = "not-plan2".into();
    assert!(policy.open(&hello, input).is_err());
    let mut wrong = hello.clone();
    replace(
        &mut wrong,
        "expectedProtocolContractSha256",
        t(&"b".repeat(64)),
    );
    assert!(matches!(
        policy.open(&wrong, open()),
        Err(Refusal::Join("protocol contract pin"))
    ));
}
