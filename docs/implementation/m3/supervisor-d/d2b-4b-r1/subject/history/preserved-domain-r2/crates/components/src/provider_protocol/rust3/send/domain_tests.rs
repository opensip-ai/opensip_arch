//! Independent recipe controls over synthetic Plan projections. No fixture
//! here establishes Plan, universe, custody, provider or source admission.
use super::*;

fn reference_hash(domain: &str, value: &Value) -> String {
    let mut bytes = domain.as_bytes().to_vec();
    bytes.push(0);
    bytes.extend(cbor::encode(value));
    format!("sha256:{}", digest_hex(&raw_sha256(&bytes)))
}
fn bounds() -> Bounds {
    Bounds {
        snapshot_entries: 200_000,
        inline_subjects: 256,
        stages: 256,
        keys_per_stage: 256,
    }
}
fn snapshot() -> String {
    format!("snapshot2:{}", "4".repeat(64))
}
fn universes() -> Vec<Universe> {
    vec![
        Universe {
            provider_id: "rust-semantic".into(),
            provider_version: "provider".into(),
            value: map(vec![("marker", Value::Unsigned(1))]),
        },
        Universe {
            provider_id: "typescript-semantic".into(),
            provider_version: "other".into(),
            value: map(vec![("marker", Value::Unsigned(2))]),
        },
    ]
}
fn reference_ids(rows: &[Universe]) -> (String, Vec<String>) {
    let source = reference_hash("opensip.rust-provider.universe.v2", &rows[0].value);
    let other = reference_hash(
        "opensip.semantic-universe.v2",
        &map(vec![
            ("providerId", t(&rows[1].provider_id)),
            ("providerVersion", t(&rows[1].provider_version)),
            ("universe", rows[1].value.clone()),
        ]),
    );
    let mut targets = vec![source.clone(), other];
    targets.sort();
    targets.dedup();
    (source, targets)
}
// Frozen dependency rows, asserted against the selected registry below.
const ROWS: [(&str, &[&str], bool); 2] = [
    (
        "calls",
        &["syntactic-callee-name", "resolved-callee"],
        false,
    ),
    ("declares", &["syntactic"], true),
];
fn reference_keys(rows: &[Universe], stage: usize) -> Vec<Value> {
    let (source, targets) = reference_ids(rows);
    // Independently structured cartesian product over the frozen dependency
    // rows, then filter same-only targets. This does not use Law's traversal,
    // loaded relation records or the implementation's scope-binding lookup.
    let dimensions: Vec<_> = ROWS
        .iter()
        .flat_map(|row| row.1.iter().map(move |rung| (row.0, *rung, row.2)))
        .collect();
    let tuples: Vec<_> = dimensions
        .iter()
        .flat_map(|row| {
            targets
                .iter()
                .map(move |target| (row.0, row.1, row.2, target))
        })
        .filter(|(_, _, same, target)| !*same || **target == source)
        .collect();
    tuples
        .into_iter()
        .enumerate()
        .map(|(n, (relation, rung, _, target))| {
            map(vec![
                ("relation", t(relation)),
                ("resolution", t(rung)),
                ("sourceUniverseId", t(&source)),
                ("targetUniverseId", t(target)),
                (
                    "subjectScopeCommitment",
                    t(&format!("sha256:{:064x}", n + 10 + stage * 100)),
                ),
                ("producer", t("rust-semantic")),
                ("producerVersion", t("provider")),
                ("schemaVersion", Value::Unsigned(1)),
            ])
        })
        .collect()
}
fn stages(rows: &[Universe]) -> Vec<Stage> {
    (0..2)
        .map(|index| {
            let keys = reference_keys(rows, index);
            let mut scopes: Vec<_> = keys
                .iter()
                .map(|k| Scope {
                    relation: value_text(k, "relation").unwrap().into(),
                    resolution: value_text(k, "resolution").unwrap().into(),
                    source: value_text(k, "sourceUniverseId").unwrap().into(),
                    target: value_text(k, "targetUniverseId").unwrap().into(),
                    commitment: value_text(k, "subjectScopeCommitment").unwrap().into(),
                })
                .collect();
            scopes.reverse(); // scope storage order is not request key order.
            Stage {
                plan_stage: map(vec![
                    ("kind", t("fact-derivation")),
                    ("stageId", t(&format!("rust-{index}"))),
                    ("operator", t("semantic-provider")),
                    ("relations", Value::Array(vec![t("calls"), t("declares")])),
                ]),
                resolved_provider: Some("rust-semantic".into()),
                scopes,
            }
        })
        .collect()
}
fn files(count: usize) -> Vec<File> {
    (0..count)
        .rev()
        .map(|i| File {
            path: format!("src/unit{i:05}.rs"),
            byte_length: i as u64 + 1,
            content_sha256: "a".repeat(64),
        })
        .collect()
}
fn reference_subjects(snapshot: &str, files: &[File]) -> Value {
    let mut selected: Vec<_> = files
        .iter()
        .filter(|f| f.path.ends_with(".rs") && f.byte_length > 0)
        .collect();
    selected.sort_by_key(|f| &f.path);
    Value::Array(
        selected
            .iter()
            .enumerate()
            .map(|(n, f)| {
                let preimage = map(vec![
                    ("snapshotId", t(snapshot)),
                    ("path", t(&f.path)),
                    ("contentSha256", t(&f.content_sha256)),
                    ("byteLength", Value::Unsigned(f.byte_length)),
                ]);
                map(vec![
                    ("subjectOrdinal", Value::Unsigned(n as u64)),
                    (
                        "subjectId",
                        t(&format!(
                            "rust-file:{}",
                            reference_hash("opensip.rust-provider.subject.v2", &preimage)
                        )),
                    ),
                    ("path", t(&f.path)),
                    ("startByte", Value::Unsigned(0)),
                    ("endByte", Value::Unsigned(f.byte_length)),
                ])
            })
            .collect(),
    )
}

#[test]
fn fresh_domains_match_independent_cartesian_products_and_frozen_dependency_rows() {
    let registry = parse_json(REGISTRY).unwrap();
    for (name, rungs, same) in ROWS {
        let row = at(
            &registry,
            &["x-opensip-relation-registry", "relations", name],
        )
        .unwrap();
        assert_eq!(at(row, &["ladder"]).and_then(strings).unwrap(), rungs);
        assert_eq!(
            at(row, &["universeRule"]).and_then(text),
            Some(if same { "same-only" } else { "admitted-target" })
        );
        assert_eq!(
            at(row, &["schemaVersion"]),
            Some(&J::Integer(opensip_identity::JsonInteger::new(1).unwrap()))
        );
    }
    let law = Law::load().unwrap();
    let u = universes();
    let s = stages(&u);
    let mut f = files(2);
    f.push(File {
        path: "src/empty.rs".into(),
        byte_length: 0,
        content_sha256: "b".repeat(64),
    });
    f.push(File {
        path: "README.md".into(),
        byte_length: 10,
        content_sha256: "c".repeat(64),
    });
    let d = law
        .derive(Input {
            snapshot: &snapshot(),
            files: &f,
            universes: &u,
            selected: 0,
            provider_build_id: "provider",
            plan_stages: &s,
            bounds: bounds(),
            reference: false,
        })
        .unwrap();
    let expected = reference_subjects(&snapshot(), &f);
    assert_eq!(d.subjects, expected);
    let (source, targets) = reference_ids(&u);
    assert_eq!(d.source_universe_id, source);
    assert_eq!(d.target_domain.into_iter().collect::<Vec<_>>(), targets);
    for (index, stage) in d.stages.iter().enumerate() {
        let keys = Value::Array(reference_keys(&u, index));
        assert_eq!(stage.keys, keys);
        assert_eq!(stage.plan_stage, s[index].plan_stage);
        assert_eq!(
            stage.domain_commitment,
            reference_hash(
                "opensip.rust-provider.analysis-domain.v2",
                &map(vec![
                    ("subjects", expected.clone()),
                    ("requestedCoverageDomain", keys)
                ])
            )
        );
    }
    assert_eq!(
        value_text(&d.subject_scope, "subjectScopeCommitment"),
        Some(reference_hash("opensip.rust-provider.subject-scope.v2", &expected).as_str())
    );
}

#[test]
fn reference_scope_preserves_the_same_subject_and_domain_commitments_without_inline_cap() {
    let law = Law::load().unwrap();
    let u = universes();
    let s = stages(&u);
    for count in [1, 256, 257, 513] {
        let f = files(count);
        let referenced = law
            .derive(Input {
                snapshot: &snapshot(),
                files: &f,
                universes: &u,
                selected: 0,
                provider_build_id: "provider",
                plan_stages: &s,
                bounds: bounds(),
                reference: true,
            })
            .unwrap();
        assert_eq!(
            member(&referenced.subject_scope, "subjectCount"),
            Some(&Value::Unsigned(count as u64))
        );
        assert_eq!(referenced.subjects, reference_subjects(&snapshot(), &f));
        let inline = law.derive(Input {
            snapshot: &snapshot(),
            files: &f,
            universes: &u,
            selected: 0,
            provider_build_id: "provider",
            plan_stages: &s,
            bounds: bounds(),
            reference: false,
        });
        if count <= 256 {
            let inline = inline.unwrap();
            assert_eq!(inline.subject_scope, referenced.subject_scope);
            assert_eq!(inline.subjects, referenced.subjects);
            assert!(
                inline
                    .stages
                    .iter()
                    .zip(&referenced.stages)
                    .all(|(a, b)| a.domain_commitment == b.domain_commitment && a.keys == b.keys)
            );
        } else {
            assert!(matches!(inline, Err(Refusal::InlineSubjectLimit)));
        }
    }
}

#[test]
fn selected_plan_stage_bytes_and_c4_scope_bindings_cannot_be_substituted() {
    let law = Law::load().unwrap();
    let u = universes();
    let f = files(1);
    let mut s = stages(&u);
    let foreign = Stage {
        plan_stage: map(vec![
            ("kind", t("fact-derivation")),
            ("stageId", t("ts-stage")),
            ("operator", t("semantic-provider")),
            ("providerId", t("typescript-semantic")),
            ("relations", Value::Array(vec![t("calls")])),
        ]),
        resolved_provider: Some("typescript-semantic".into()),
        scopes: vec![],
    };
    s.insert(1, foreign);
    let d = law
        .derive(Input {
            snapshot: &snapshot(),
            files: &f,
            universes: &u,
            selected: 0,
            provider_build_id: "provider",
            plan_stages: &s,
            bounds: bounds(),
            reference: false,
        })
        .unwrap();
    assert_eq!(d.stages.len(), 2);
    assert_eq!(
        cbor::encode(&d.stages[0].plan_stage),
        cbor::encode(&s[0].plan_stage)
    );
    assert_eq!(
        cbor::encode(&d.stages[1].plan_stage),
        cbor::encode(&s[2].plan_stage)
    );
    assert!(member(&d.stages[0].plan_stage, "providerId").is_none());
    assert!(member(&d.stages[0].plan_stage, "dependsOn").is_none());
    for bad in [
        "missing",
        "extra",
        "duplicate",
        "literal-provider",
        "null-optional",
    ] {
        let mut s = stages(&u);
        match bad {
            "missing" => {
                s[0].scopes.pop();
            }
            "extra" => s[0].scopes.push(Scope {
                relation: "calls".into(),
                resolution: "resolved-callee".into(),
                source: "sha256:extra".into(),
                target: "sha256:extra".into(),
                commitment: "sha256:extra".into(),
            }),
            "duplicate" => {
                let k = &s[0].scopes[0];
                let copy = Scope {
                    relation: k.relation.clone(),
                    resolution: k.resolution.clone(),
                    source: k.source.clone(),
                    target: k.target.clone(),
                    commitment: k.commitment.clone(),
                };
                s[0].scopes.push(copy);
            }
            "literal-provider" => {
                let Value::Map(m) = &mut s[0].plan_stage else {
                    unreachable!()
                };
                m.push(("providerId".into(), t("typescript-semantic")));
            }
            "null-optional" => {
                let Value::Map(m) = &mut s[0].plan_stage else {
                    unreachable!()
                };
                m.push(("dependsOn".into(), Value::Null));
            }
            _ => unreachable!(),
        }
        assert!(
            law.derive(Input {
                snapshot: &snapshot(),
                files: &f,
                universes: &u,
                selected: 0,
                provider_build_id: "provider",
                plan_stages: &s,
                bounds: bounds(),
                reference: false
            })
            .is_err(),
            "{bad}"
        );
    }
}

#[test]
fn invalid_and_overbound_domains_refuse_instead_of_emitting_a_partial_projection() {
    let law = Law::load().unwrap();
    let u = universes();
    let s = stages(&u);
    assert!(
        law.derive(Input {
            snapshot: &snapshot(),
            files: &[],
            universes: &u,
            selected: 0,
            provider_build_id: "provider",
            plan_stages: &s,
            bounds: bounds(),
            reference: true
        })
        .is_err()
    );
    let mut f = files(2);
    f[1].path = f[0].path.clone();
    assert!(
        law.derive(Input {
            snapshot: &snapshot(),
            files: &f,
            universes: &u,
            selected: 0,
            provider_build_id: "provider",
            plan_stages: &s,
            bounds: bounds(),
            reference: true
        })
        .is_err()
    );
    let f = files(2);
    for b in [
        Bounds {
            snapshot_entries: 1,
            ..bounds()
        },
        Bounds {
            inline_subjects: 1,
            ..bounds()
        },
        Bounds {
            stages: 1,
            ..bounds()
        },
        Bounds {
            keys_per_stage: 4,
            ..bounds()
        },
    ] {
        assert!(
            law.derive(Input {
                snapshot: &snapshot(),
                files: &f,
                universes: &u,
                selected: 0,
                provider_build_id: "provider",
                plan_stages: &s,
                bounds: b,
                reference: false
            })
            .is_err()
        );
    }
    assert!(
        law.derive(Input {
            snapshot: "snapshot2:bad",
            files: &f,
            universes: &u,
            selected: 0,
            provider_build_id: "provider",
            plan_stages: &s,
            bounds: bounds(),
            reference: true
        })
        .is_err()
    );
    assert!(
        law.derive(Input {
            snapshot: &snapshot(),
            files: &f,
            universes: &u,
            selected: 0,
            provider_build_id: "other",
            plan_stages: &s,
            bounds: bounds(),
            reference: true
        })
        .is_err()
    );
}
