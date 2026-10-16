// M3-B r9 item 18 (unit B2-d3): the recommendation evidence against the
// actual resolver. The resolver input is the configuration vectors' `base`
// case (tools/host/configuration_vectors.py), with its project carrier
// replaced per control; the recognitions come from `framework_recognition`.
use super::configuration::{
    CapturedCarrierV1, CompiledDefaultsV1, ComponentRequestV1, ComponentVersionV1, FlagLayerV1,
    ResolverInputV1, resolve,
};
use super::discovery::recommendation_evidence;
use super::framework_recognition::{RecognitionInputs, recognize};
use super::invocation::InvocationModeV1;
use super::recommendation::{RecognizedUnit, apply_setting};
use opensip_identity::{JsonValue as V, parse_json};
use serde_json::Value;
use std::collections::{BTreeMap, BTreeSet};

const VECTORS: &str = include_str!("configuration_vectors.json");

fn strs(value: &Value) -> Vec<String> {
    value
        .as_array()
        .unwrap()
        .iter()
        .map(|v| v.as_str().unwrap().to_owned())
        .collect()
}
fn version(value: &Value) -> ComponentVersionV1 {
    ComponentVersionV1 {
        stable_id: value["stableId"].as_str().unwrap().to_owned(),
        version: value["version"].as_str().unwrap().to_owned(),
    }
}
/// The `base` case's defaults layer (exact versions only, as it holds).
fn base_defaults() -> CompiledDefaultsV1 {
    let vectors: Value = serde_json::from_str(VECTORS).unwrap();
    let case = vectors["cases"]
        .as_array()
        .unwrap()
        .iter()
        .find(|c| c["id"] == "base")
        .unwrap();
    let d = &case["layers"]["defaults"];
    CompiledDefaultsV1 {
        profile_id: d["analysis"]["profileId"].as_str().map(str::to_owned),
        capabilities: Some(strs(&d["analysis"]["capabilities"])),
        budget_limit: d["analysis"]["budget"]["limit"].as_u64(),
        request: Some(
            d["components"]["request"]
                .as_array()
                .unwrap()
                .iter()
                .map(|r| ComponentRequestV1::Version(version(r)))
                .collect(),
        ),
        pins: Some(Vec::new()),
        holds: Some(Vec::new()),
        allowed_scopes: Some(strs(&d["components"]["allowedScopes"])),
        pack_ids: Some(strs(&d["policy"]["packIds"])),
    }
}
fn input(project: Option<&str>, local: Option<&str>) -> ResolverInputV1 {
    ResolverInputV1 {
        defaults: base_defaults(),
        global: None,
        project: project.map(|t| CapturedCarrierV1 {
            path: "opensip.json".to_owned(),
            bytes: t.as_bytes().to_vec(),
        }),
        local: local.map(|t| CapturedCarrierV1 {
            path: "opensip.local.json".to_owned(),
            bytes: t.as_bytes().to_vec(),
        }),
        flags: FlagLayerV1::default(),
        mode: InvocationModeV1 {
            interactive: local.is_some(),
        },
    }
}
fn recognition(files: &[(&str, &[u8])]) -> V {
    let bytes: BTreeMap<String, Vec<u8>> = files
        .iter()
        .map(|(p, b)| ((*p).to_owned(), b.to_vec()))
        .collect();
    let paths: BTreeSet<String> = bytes.keys().cloned().collect();
    recognize(&RecognitionInputs {
        paths: &paths,
        bytes: &bytes,
        explicit_entry_points: None,
    })
    .unwrap()
}
fn cargo_unit() -> V {
    recognition(&[
        ("Cargo.toml", b"[package]\nname = \"a\"\n"),
        ("src/main.rs", b""),
    ])
}
fn resolved_field(input: &ResolverInputV1, name: &str) -> Option<Vec<String>> {
    let resolved = resolve(input).unwrap();
    let V::Object(semantic) = &resolved.semantic else {
        panic!()
    };
    let Some(V::Object(discovery)) = semantic.get("discovery") else {
        return None;
    };
    discovery.get(name).map(|v| match v {
        V::Array(items) => items
            .iter()
            .map(|i| match i {
                V::String(s) => s.clone(),
                other => panic!("{other:?}"),
            })
            .collect(),
        other => panic!("{other:?}"),
    })
}

#[test]
fn every_proposal_round_trips_through_the_actual_resolver() {
    let root = cargo_unit();
    let nested = cargo_unit();
    let units = [
        RecognizedUnit {
            unit_ordinal: 0,
            root_path: "",
            recognition: &root,
        },
        RecognizedUnit {
            unit_ordinal: 1,
            root_path: "crates/a",
            recognition: &nested,
        },
    ];
    let base = input(None, None);
    let evidence = recommendation_evidence(&units, &base).unwrap();
    // Applying none changes nothing: the base is the input as resolved.
    assert_eq!(
        evidence.base_digest,
        resolve(&base).unwrap().resolved_config_digest
    );
    let by_field = |f: &str| evidence.proposed.iter().find(|p| p.field == f).unwrap();
    let entries = by_field("discovery.entryPoints");
    let paths: Vec<&str> = entries.paths.iter().map(|p| p.path.as_str()).collect();
    // Unit-root projection: colliding relative names, distinct project paths,
    // in the resolver's order.
    assert_eq!(paths, ["crates/a/src/main.rs", "src/main.rs"]);
    assert_eq!(entries.paths[0].sources[0].unit_ordinal, 1);
    assert_eq!(entries.paths[0].sources[0].recognizer_id, "cargo-package");
    let ignores = by_field("discovery.ignorePaths");
    let ignore_paths: Vec<&str> = ignores.paths.iter().map(|p| p.path.as_str()).collect();
    assert_eq!(ignore_paths, ["crates/a/target", "target"]);
    for setting in &evidence.proposed {
        let name = setting.field.trim_start_matches("discovery.");
        let values: Vec<String> = setting.paths.iter().map(|p| p.path.clone()).collect();
        let applied = apply_setting(&base, name, &values).unwrap();
        let resolved = resolve(&applied).unwrap();
        assert_eq!(resolved.resolved_config_digest, setting.digest_with);
        assert_eq!(setting.digest_without, evidence.base_digest);
        assert_ne!(setting.digest_with, setting.digest_without);
        assert_eq!(resolved_field(&applied, name), Some(values));
    }
    // FR-2 provenance on the detected evidence; no unresolved choice.
    assert!(
        evidence
            .detected
            .iter()
            .all(|d| d.provenance == "DISCOVERED:cargo-package@1")
    );
    assert!(evidence.unresolved.is_empty());
    assert!(
        evidence
            .defaults
            .iter()
            .any(|d| d.field == "discovery.workspaceRoots")
    );
}

#[test]
fn equal_project_paths_from_two_units_are_one_setting_citing_both() {
    // Synthetic recognitions: `b/x` in the unit at `a` and `x` in the unit at
    // `a/b` are both the project path `a/b/x`.
    let make = |entry: &str| {
        parse_json(
            format!(
                r#"{{"schemaVersion":1,"recognized":[{{"recognizerId":"vite","recognizerVersion":1,"evidence":[{{"path":"vite.config.ts","contentSha256":"{}","field":"presence"}}],"assurance":"inferred","effects":{{"entryPoints":["{entry}"],"testGlobs":[],"ignoreConventions":[]}},"unresolvedChoices":[]}}],"observedHints":[],"entryPoints":{{"state":"all","source":"recognized"}}}}"#,
                "0".repeat(64)
            )
            .as_bytes(),
        )
        .unwrap()
    };
    let (one, two) = (make("b/x"), make("x"));
    let units = [
        RecognizedUnit {
            unit_ordinal: 3,
            root_path: "a",
            recognition: &one,
        },
        RecognizedUnit {
            unit_ordinal: 4,
            root_path: "a/b",
            recognition: &two,
        },
    ];
    let evidence = recommendation_evidence(&units, &input(None, None)).unwrap();
    let entries = evidence
        .proposed
        .iter()
        .find(|p| p.field == "discovery.entryPoints")
        .unwrap();
    assert_eq!(entries.paths.len(), 1);
    assert_eq!(entries.paths[0].path, "a/b/x");
    let ordinals: Vec<u64> = entries.paths[0]
        .sources
        .iter()
        .map(|s| s.unit_ordinal)
        .collect();
    assert_eq!(ordinals, [3, 4]);
}

#[test]
fn explicit_entry_points_are_never_proposed_over() {
    let unit = cargo_unit();
    let units = [RecognizedUnit {
        unit_ordinal: 0,
        root_path: "",
        recognition: &unit,
    }];
    // Absent: proposed. Explicit `[]`, and project ["a"] overridden by local
    // []: explicit, so not proposed.
    for (project, local, proposed) in [
        (None, None, true),
        (
            Some(r#"{"schemaVersion":2,"discovery":{"entryPoints":[]}}"#),
            None,
            false,
        ),
        (
            Some(r#"{"schemaVersion":2,"discovery":{"entryPoints":["a"]}}"#),
            Some(r#"{"schemaVersion":2,"discovery":{"entryPoints":[]}}"#),
            false,
        ),
    ] {
        let base = input(project, local);
        let evidence = recommendation_evidence(&units, &base).unwrap();
        let entry = evidence
            .proposed
            .iter()
            .any(|p| p.field == "discovery.entryPoints");
        assert_eq!(entry, proposed, "{project:?} {local:?}");
        if !proposed {
            assert!(evidence.defaults.iter().any(
                |d| d.field == "discovery.entryPoints" && d.reason == "explicit-configuration"
            ));
            assert_eq!(resolved_field(&base, "entryPoints"), Some(Vec::new()));
        }
    }
}

#[test]
fn incomplete_recognition_proposes_no_entry_points() {
    // A Vite unit needs its configuration evaluated: `partial`.
    let vite = recognition(&[("vite.config.ts", b"x"), ("index.html", b"")]);
    let units = [RecognizedUnit {
        unit_ordinal: 0,
        root_path: "web",
        recognition: &vite,
    }];
    let evidence = recommendation_evidence(&units, &input(None, None)).unwrap();
    assert!(
        !evidence
            .proposed
            .iter()
            .any(|p| p.field == "discovery.entryPoints")
    );
    assert!(
        evidence
            .defaults
            .iter()
            .any(|d| d.field == "discovery.entryPoints" && d.reason == "recognition-incomplete")
    );
    // Its disclosure is carried; its ignore convention is still proposed.
    assert!(
        evidence
            .unresolved
            .iter()
            .any(|u| u.choice == "config-requires-evaluation")
    );
    let ignores = evidence
        .proposed
        .iter()
        .find(|p| p.field == "discovery.ignorePaths")
        .unwrap();
    assert_eq!(ignores.paths[0].path, "web/dist");
}

#[test]
fn a_path_the_resolver_refuses_is_recorded_not_proposed() {
    let synthetic = parse_json(
        format!(
            r#"{{"schemaVersion":1,"recognized":[{{"recognizerId":"node-package","recognizerVersion":1,"evidence":[{{"path":"package.json","contentSha256":"{}","field":"type/private/exports/main"}}],"assurance":"declared","effects":{{"entryPoints":[],"testGlobs":[],"ignoreConventions":["../escape/","node_modules/"]}},"unresolvedChoices":[]}}],"observedHints":[{{"dependencyName":"vue"}}],"entryPoints":{{"state":"none","source":"none"}}}}"#,
            "0".repeat(64)
        )
        .as_bytes(),
    )
    .unwrap();
    let units = [RecognizedUnit {
        unit_ordinal: 0,
        root_path: "",
        recognition: &synthetic,
    }];
    let evidence = recommendation_evidence(&units, &input(None, None)).unwrap();
    assert!(
        evidence
            .unresolved
            .iter()
            .any(|u| u.choice == "resolver-refused:discovery.ignorePaths:../escape")
    );
    let ignores = evidence
        .proposed
        .iter()
        .find(|p| p.field == "discovery.ignorePaths")
        .unwrap();
    let paths: Vec<&str> = ignores.paths.iter().map(|p| p.path.as_str()).collect();
    assert_eq!(paths, ["node_modules"]);
    assert_eq!(evidence.observed_hints, [(0, "vue".to_owned())]);
}

#[test]
fn applying_a_proposal_keeps_the_rest_of_the_carrier() {
    let unit = cargo_unit();
    let units = [RecognizedUnit {
        unit_ordinal: 0,
        root_path: "",
        recognition: &unit,
    }];
    let carrier =
        r#"{"schemaVersion":2,"ui":{"color":"never"},"discovery":{"workspaceRoots":["src"]}}"#;
    let base = input(Some(carrier), None);
    let evidence = recommendation_evidence(&units, &base).unwrap();
    let entries = evidence
        .proposed
        .iter()
        .find(|p| p.field == "discovery.entryPoints")
        .unwrap();
    let applied = apply_setting(&base, "entryPoints", &["src/main.rs".to_owned()]).unwrap();
    let before = resolve(&base).unwrap();
    let after = resolve(&applied).unwrap();
    assert_eq!(after.resolved_config_digest, entries.digest_with);
    assert_eq!(after.operational, before.operational);
    assert_eq!(
        resolved_field(&applied, "workspaceRoots"),
        Some(vec!["src".to_owned()])
    );
    // A refused input is the resolver's refusal, unchanged.
    let refused = input(Some("{"), None);
    assert_eq!(
        recommendation_evidence(&units, &refused).err(),
        resolve(&refused).err()
    );
}
