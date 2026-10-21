//! Synthetic pre-C4 wire inputs, using the same pinned public startup
//! fixture as D2b's request controls. No native Plan/source admission is
//! inferred. Authority identity is read independently of the built sender.
use super::*;
use opensip_components::provider_protocol::{built_commitment, cbor::Value as C, rust3::*};
use std::collections::BTreeMap;
const STARTUP: &[u8] = include_bytes!("../../components/tests/data/rust3-startup-shape.v1.json");
fn wire(value: &serde_json::Value) -> C {
    match value {
        serde_json::Value::Null => C::Null,
        serde_json::Value::Bool(value) => C::Bool(*value),
        serde_json::Value::String(value) => C::Text(value.clone()),
        serde_json::Value::Number(value) => {
            C::Unsigned(value.as_u64().expect("literal unsigned fixture integer"))
        }
        serde_json::Value::Array(values) => C::Array(values.iter().map(wire).collect()),
        serde_json::Value::Object(values) => C::Map(
            values
                .iter()
                .map(|(key, value)| (key.clone(), wire(value)))
                .collect(),
        ),
    }
}
fn identity(universe: &serde_json::Value) -> C {
    C::Map(
        [
            "protocolMajor",
            "providerBuildId",
            "rustCommitHash",
            "sysrootDigest",
            "hostTriple",
            "targetTriple",
        ]
        .into_iter()
        .map(|key| (key.to_owned(), wire(&universe[key])))
        .collect(),
    )
}
fn caps() -> Vec<String> {
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
pub(super) fn rust() -> (Provider, C, Vec<String>) {
    let fixture: serde_json::Value = serde_json::from_slice(STARTUP).unwrap();
    let accepted = &fixture["universeAccepted"];
    let mut universe = accepted["universe"].clone();
    let mut repository = accepted["repositoryResolution"].clone();
    let dependency = serde_json::json!({"schemaVersion":1,"language":"rust","lockfileIdentity":{"path":"Cargo.lock","lockfileVersion":3,"contentSha256":"b".repeat(64)},"packages":[],"completeness":{"state":"complete","missing":[]}});
    let dependency = parse_json(&serde_json::to_vec(&dependency).unwrap()).unwrap();
    let dependency_id = format!(
        "sha256:{}",
        digest_hex(
            &opensip_identity::hash_canonical_value("native.dependency-source-set.v1", &dependency)
                .unwrap()
        )
    );
    universe["resolvedInputs"]["dependencySourceSetId"] = serde_json::json!(dependency_id);
    repository["dependencySourceSetId"] = serde_json::json!(dependency_id);
    let expected = identity(&universe);
    let universe = wire(&universe);
    let source = built_commitment("opensip.rust-provider.universe.v2", &universe);
    let stage = Rust3StagePlan {
        plan_stage: C::Map(vec![
            ("kind".into(), C::Text("fact-derivation".into())),
            ("stageId".into(), C::Text("rust-stage".into())),
            ("operator".into(), C::Text("semantic-provider".into())),
            (
                "relations".into(),
                C::Array(vec![C::Text("declares".into())]),
            ),
        ]),
        resolved_provider: Some("rust-semantic".into()),
        scopes: vec![Rust3ScopeBinding {
            relation: "declares".into(),
            resolution: "syntactic".into(),
            source: source.clone(),
            target: source,
            commitment: format!("sha256:{}", "f".repeat(64)),
        }],
    };
    let plan = Rust3Plan {
        symbol_census: None,
        host_build_id: "host".into(),
        expected_identity: expected,
        capabilities: caps(),
        open: Rust3OpenPlan {
            execution_id: "execution".into(),
            snapshot_id: accepted["snapshotId"].as_str().unwrap().into(),
            plan_id: accepted["planId"].as_str().unwrap().into(),
            plan_intent_commitment: format!("sha256:{}", "2".repeat(64)),
            universe: universe.clone(),
            repository_resolution: wire(&repository),
        },
        snapshot: vec![
            Rust3SnapshotEntry::File {
                path: "src/a.rs".into(),
                byte_length: 1_048_577,
                content_sha256: "a".repeat(64),
                executable: false,
            },
            Rust3SnapshotEntry::File {
                path: "src/empty.rs".into(),
                byte_length: 0,
                content_sha256: "a".repeat(64),
                executable: false,
            },
            Rust3SnapshotEntry::Symlink {
                path: "zzz-link".into(),
                target_bytes: vec![0xff, 0],
            },
        ],
        universes: vec![Rust3UniversePlan {
            provider_id: "rust-semantic".into(),
            provider_version: "provider".into(),
            value: universe,
        }],
        selected_universe: 0,
        stages: vec![stage],
        dependency_set: dependency,
        dependency_manifests: BTreeMap::new(),
        prepared_set: None,
        analysis_ordinal: u64::MAX,
    };
    let sender = Rust3Sender::new(Rust3Request::build(plan).unwrap()).unwrap();
    let independent: serde_json::Value = serde_json::from_slice(STARTUP).unwrap();
    (
        Provider::Rust { sender },
        identity(&independent["universeAccepted"]["universe"]),
        caps(),
    )
}
