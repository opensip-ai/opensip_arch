//! End-to-end request projection controls over synthetic C4 inputs. A schema
//! shaped universe/set does not establish their admission or source custody.
use super::super::super::super::{
    built_commitment,
    table::{Protocol, Table},
};
use super::*;
use opensip_identity::{JsonInteger, digest_hex, hash_canonical_value, parse_json, raw_sha256};
fn jmap(v: Vec<(&str, J)>) -> J {
    J::Object(v.into_iter().map(|(k, v)| (k.into(), v)).collect())
}
fn js(v: &str) -> J {
    J::String(v.into())
}
fn jn(v: u64) -> J {
    J::Integer(JsonInteger::new(i128::from(v)).unwrap())
}
fn jfield<'a>(v: &'a J, k: &str) -> &'a J {
    let J::Object(v) = v else { panic!() };
    v.get(k).unwrap()
}
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
fn replace(v: &mut Value, k: &str, new: Value) {
    let Value::Map(v) = v else { panic!() };
    *v.iter_mut().find(|(key, _)| key == k).unwrap() = (k.into(), new);
}
fn jreplace(v: &mut J, k: &str, new: J) {
    let J::Object(v) = v else { panic!() };
    v.insert(k.into(), new);
}
fn native_id(domain: &str, v: &J) -> String {
    format!(
        "sha256:{}",
        digest_hex(&hash_canonical_value(domain, v).unwrap())
    )
}
fn prepared_set() -> J {
    let row = jmap(vec![
        ("kind", js("macro-expansion")),
        ("ownerKey", js("fixture-owner")),
        ("configuration", J::Array(vec![])),
        ("site", J::Null),
        (
            "inputBinding",
            jmap(vec![
                ("cfgSetId", js("primary")),
                (
                    "dependencySourceSetId",
                    js(&format!("sha256:{}", "b".repeat(64))),
                ),
                ("ownerFileManifestSha256", js(&"c".repeat(64))),
                ("toolchainDigest", js(&"d".repeat(64))),
            ]),
        ),
        (
            "blob",
            jmap(vec![
                ("byteLength", jn(1_048_577)),
                ("sha256", js(&"a".repeat(64))),
                ("mediaType", js("application/octet-stream")),
            ]),
        ),
        ("status", js("failed")),
        ("failureDetail", js("fixture-failure")),
        ("generated", J::Null),
    ]);
    // Preparation is deliberately opaque; this is not native set admission.
    jmap(vec![
        ("schemaVersion", jn(3)),
        ("preparation", jmap(vec![("fixture", js("not-admitted"))])),
        ("rows", J::Array(vec![row])),
    ])
}
pub(in crate::provider_protocol::rust3::send) fn plan(deps: bool, prep: bool) -> Plan {
    let fixture = parse_json(include_bytes!(
        "../../../../tests/data/rust3-startup-shape.v1.json"
    ))
    .unwrap();
    let accepted = jfield(&fixture, "universeAccepted");
    let mut universe = wire(jfield(accepted, "universe"));
    let mut repo = wire(jfield(accepted, "repositoryResolution"));
    let mut packages = Vec::new();
    let mut manifests = BTreeMap::new();
    if deps {
        let files = J::Array(vec![jmap(vec![
            ("path", js("src/lib.rs")),
            ("byteLength", jn(3)),
            ("contentSha256", js(&"a".repeat(64))),
        ])]);
        let hash = digest_hex(
            &hash_canonical_value("native.dependency-file-manifest.v1", &files).unwrap(),
        );
        manifests.insert(hash.clone(), files);
        packages.push(jmap(vec![
            ("name", js("a")),
            ("version", js("1")),
            ("sourceId", js("source with spaces")),
            ("sourceKind", js("path")),
            ("lockChecksum", J::Null),
            ("fileManifestSha256", js(&hash)),
            ("fileCount", jn(1)),
            ("totalBytes", jn(3)),
            (
                "acquisition",
                jmap(vec![
                    ("mode", js("in-snapshot-path")),
                    ("descriptorId", J::Null),
                    ("vendorPath", J::Null),
                ]),
            ),
            ("checksumVerification", js("not-applicable")),
            ("provenanceAssurance", js("declared")),
        ]));
    }
    let dependency_set = jmap(vec![
        ("schemaVersion", jn(1)),
        ("language", js("rust")),
        (
            "lockfileIdentity",
            jmap(vec![
                ("path", js("Cargo.lock")),
                ("lockfileVersion", jn(3)),
                ("contentSha256", js(&"b".repeat(64))),
            ]),
        ),
        ("packages", J::Array(packages)),
        (
            "completeness",
            jmap(vec![
                ("state", js("complete")),
                ("missing", J::Array(vec![])),
            ]),
        ),
    ]);
    let dep_id = native_id("native.dependency-source-set.v1", &dependency_set);
    let mut resolved = member(&universe, "resolvedInputs").unwrap().clone();
    replace(&mut resolved, "dependencySourceSetId", t(&dep_id));
    replace(&mut repo, "dependencySourceSetId", t(&dep_id));
    let prepared_set = prep.then(|| {
        let mut set = prepared_set();
        let J::Object(v) = &mut set else { panic!() };
        let J::Array(rows) = v.get_mut("rows").unwrap() else {
            panic!()
        };
        let J::Object(row) = &mut rows[0] else {
            panic!()
        };
        jreplace(
            row.get_mut("inputBinding").unwrap(),
            "dependencySourceSetId",
            js(&dep_id),
        );
        set
    });
    if let Some(set) = &prepared_set {
        let id = native_id("native.prepared-output-set.v3", set);
        replace(&mut resolved, "preparedOutputSetId", t(&id));
        replace(&mut resolved, "preparedResolution", t("imported-inert"));
        replace(&mut repo, "preparedOutputSetId", t(&id));
    }
    replace(&mut universe, "resolvedInputs", resolved);
    let identity = map([
        "protocolMajor",
        "providerBuildId",
        "rustCommitHash",
        "sysrootDigest",
        "hostTriple",
        "targetTriple",
    ]
    .into_iter()
    .map(|k| (k, member(&universe, k).unwrap().clone()))
    .collect());
    let source = built_commitment("opensip.rust-provider.universe.v2", &universe);
    let stages = vec![domain::Stage {
        plan_stage: map(vec![
            ("kind", t("fact-derivation")),
            ("stageId", t("rust-stage")),
            ("operator", t("semantic-provider")),
            ("relations", Value::Array(vec![t("declares")])),
        ]),
        resolved_provider: Some("rust-semantic".into()),
        scopes: vec![domain::Scope {
            relation: "declares".into(),
            resolution: "syntactic".into(),
            source: source.clone(),
            target: source,
            commitment: format!("sha256:{}", "f".repeat(64)),
        }],
    }];
    Plan {
        host_build_id: "host".into(),
        expected_identity: identity,
        capabilities: [
            "coverage-v3",
            "fact-identity-fact2",
            "plan-identity-plan2",
            "source-identity-snapshot2",
        ]
        .into_iter()
        .map(str::to_owned)
        .collect(),
        open: policy::Open {
            execution_id: "execution".into(),
            snapshot_id: text(&wire(jfield(accepted, "snapshotId"))).unwrap().into(),
            plan_id: text(&wire(jfield(accepted, "planId"))).unwrap().into(),
            plan_intent_commitment: format!("sha256:{}", "2".repeat(64)),
            universe: universe.clone(),
            repository_resolution: repo,
        },
        snapshot: vec![
            snapshot::Entry::File {
                path: "src/a.rs".into(),
                byte_length: 1_048_577,
                content_sha256: "a".repeat(64),
                executable: false,
            },
            snapshot::Entry::File {
                path: "src/empty.rs".into(),
                byte_length: 0,
                content_sha256: "a".repeat(64),
                executable: false,
            },
            snapshot::Entry::Symlink {
                path: "zzz-link".into(),
                target_bytes: vec![0xff, 0],
            },
        ],
        universes: vec![domain::Universe {
            provider_id: "rust-semantic".into(),
            provider_version: "provider".into(),
            value: universe,
        }],
        selected_universe: 0,
        stages,
        dependency_set,
        dependency_manifests: manifests,
        prepared_set,
        analysis_ordinal: u64::MAX,
    }
}
fn analyze(r: &Request) -> Value {
    map(vec![
        ("analysisOrdinal", Value::Unsigned(r.plan.analysis_ordinal)),
        ("executionId", t(&r.plan.open.execution_id)),
        ("snapshotId", t(&r.plan.open.snapshot_id)),
        ("planId", t(&r.plan.open.plan_id)),
        (
            "stages",
            Value::Array(
                r.context
                    .stages
                    .iter()
                    .enumerate()
                    .map(|(i, s)| {
                        map(vec![
                            ("stageOrdinal", Value::Unsigned(i as u64)),
                            ("planStage", s.plan_stage.clone()),
                            ("analysisDomain", s.analysis_domain.clone()),
                        ])
                    })
                    .collect(),
            ),
        ),
    ])
}

#[test]
fn complete_request_schedule_matches_real_envelopes_and_one_maximal_cancel() {
    for (deps, prep) in [(false, false), (true, false), (true, true)] {
        let r = Request::build(plan(deps, prep)).unwrap();
        let p = &r.plan;
        let profile = &r.policy;
        let snap = snapshot::build(profile, &p.open.snapshot_id, &p.snapshot, 2).unwrap();
        let dep_id =
            text(member(&p.open.repository_resolution, "dependencySourceSetId").unwrap()).unwrap();
        let dep = dependency::build(
            profile,
            &dependency::Input {
                set: &p.dependency_set,
                manifests: &p.dependency_manifests,
                set_id: dep_id,
            },
            6,
        )
        .unwrap();
        let mut frames = vec![
            (Frame::Hello, r.context.hello.clone()),
            (Frame::OpenUniverse, r.context.open_universe.clone()),
            (Frame::SnapshotManifest, snap.manifest),
        ];
        for (index, offset, length) in [(0, 0, 1_048_576), (1, 1_048_576, 1)] {
            frames.push((
                Frame::SnapshotFileChunk,
                snapshot::chunk(
                    profile,
                    &p.open.snapshot_id,
                    &p.snapshot[0],
                    index,
                    offset,
                    vec![7; length],
                )
                .unwrap(),
            ));
        }
        frames.push((Frame::SnapshotSeal, snap.seal));
        frames.push((Frame::DependencySourceManifest, dep.manifest.clone()));
        for entry in array(member(&dep.manifest, "entries").unwrap()).unwrap() {
            frames.push((
                Frame::DependencySourceChunk,
                dependency::chunk(profile, dep_id, entry, 0, 0, vec![8; 3]).unwrap(),
            ));
        }
        frames.push((Frame::DependencySourceSeal, dep.seal));
        if let Some(set) = &p.prepared_set {
            let set_id =
                text(member(&p.open.repository_resolution, "preparedOutputSetId").unwrap())
                    .unwrap();
            let prep = prepared::build(
                profile,
                &prepared::Input {
                    set,
                    set_id,
                    plan_id: &p.open.plan_id,
                },
                9,
            )
            .unwrap();
            frames.push((Frame::PreparedOutputManifest, prep.manifest.clone()));
            let entry = &array(member(&prep.manifest, "entries").unwrap()).unwrap()[0];
            for (index, offset, length) in [(0, 0, 1_048_576), (1, 1_048_576, 1)] {
                frames.push((
                    Frame::PreparedOutputChunk,
                    prepared::chunk(
                        profile,
                        &p.open.plan_id,
                        entry,
                        index,
                        offset,
                        vec![9; length],
                    )
                    .unwrap(),
                ));
            }
            frames.push((Frame::PreparedOutputSeal, prep.seal));
        }
        frames.push((Frame::Analyze, analyze(&r)));
        assert_eq!(frames.len(), r.schedule.slots.len());
        let mut total = 0_u64;
        for (sequence, ((frame, payload), slot)) in frames.iter().zip(&r.schedule.slots).enumerate()
        {
            assert_eq!(slot.frame, *frame);
            assert_eq!(slot.sequence, sequence as u64);
            let full = schedule::envelope(sequence as u64, frame.name(), payload.clone());
            let bytes = cbor::encode(&full);
            cbor::decode(&bytes, cbor::Profile::Rust3, RUST3_FRAME_MAX_DEPTH).unwrap();
            assert_eq!(slot.payload_bytes, bytes.len() as u64);
            total += bytes.len() as u64;
            let mut hashed = payload.clone();
            if slot.chunk.is_some() {
                let Value::Map(v) = &mut hashed else { panic!() };
                v.retain(|(k, _)| k != "bytes");
            }
            assert_eq!(slot.payload_sha256, raw_sha256(&cbor::encode(&hashed)));
        }
        let cancel = map(vec![
            ("executionId", t(&p.open.execution_id)),
            ("analysisOrdinal", Value::Unsigned(p.analysis_ordinal)),
            ("reason", t("user-interrupt")),
        ]);
        let cancel_bytes =
            cbor::encode(&schedule::envelope(frames.len() as u64, "Cancel", cancel)).len() as u64;
        assert_eq!(r.schedule.cancel_reserve_bytes, cancel_bytes);
        assert_eq!(r.schedule.totals.payload_bytes, total + cancel_bytes);
        assert_eq!(r.schedule.totals.frames, frames.len() as u64 + 1);
        assert_eq!(r.context.manifest_files.len(), 2);
        assert!(!r.reference);
        super::super::super::Rust3Receiver::new(
            &Table::load(Protocol::Rust3).unwrap(),
            r.context.clone(),
        )
        .unwrap();
    }
}

#[test]
fn request_selection_canonical_values_and_complete_set_joins_refuse_forgery() {
    let mut p = plan(false, false);
    p.selected_universe = 1;
    assert!(Request::build(p).is_err());
    let mut p = plan(false, false);
    p.universes[0].provider_version = "other".into();
    assert!(Request::build(p).is_err());
    let mut p = plan(false, false);
    let Value::Map(v) = &mut p.stages[0].plan_stage else {
        panic!()
    };
    v.push(("stageId".into(), t("duplicate")));
    assert!(Request::build(p).is_err());
    let mut p = plan(false, false);
    let Value::Map(v) = &mut p.open.universe else {
        panic!()
    };
    v.push(("providerBuildId".into(), t("duplicate")));
    assert!(Request::build(p).is_err());
    let mut p = plan(false, false);
    p.capabilities.push("symbol-census-v1".into());
    p.capabilities.sort();
    assert!(Request::build(p).is_err());
    let mut p = plan(false, false);
    p.prepared_set = Some(prepared_set());
    assert!(Request::build(p).is_err());
    let mut p = plan(false, true);
    p.prepared_set = None;
    assert!(Request::build(p).is_err());
    let mut p = plan(false, false);
    replace(
        &mut p.open.repository_resolution,
        "dependencySourceSetId",
        t(&format!("sha256:{}", "0".repeat(64))),
    );
    assert!(Request::build(p).is_err());
}

#[test]
fn request_reference_variant_is_selected_for_every_count_and_inline_cap_stays_closed() {
    for count in [1, 256, 257] {
        let make = |reference| {
            let mut p = plan(false, false);
            p.snapshot = (0..count)
                .map(|i| snapshot::Entry::File {
                    path: format!("src/{i:05}.rs"),
                    byte_length: 1,
                    content_sha256: "a".repeat(64),
                    executable: false,
                })
                .collect();
            if reference {
                p.capabilities.push("subject-scope-reference-v1".into());
                p.capabilities.sort();
            }
            p
        };
        let r = Request::build(make(true)).unwrap();
        assert!(r.reference);
        assert!(member(&r.context.stages[0].analysis_domain, "subjectScope").is_ok());
        assert!(member(&r.context.stages[0].analysis_domain, "subjects").is_err());
        // Host construction does not silently grant 4c worker admission.
        assert!(
            super::super::super::Rust3Receiver::new(
                &Table::load(Protocol::Rust3).unwrap(),
                r.context
            )
            .is_err()
        );
        if count <= 256 {
            let r = Request::build(make(false)).unwrap();
            assert!(member(&r.context.stages[0].analysis_domain, "subjects").is_ok());
        } else {
            assert!(matches!(
                Request::build(make(false)),
                Err(Refusal::ProjectionLimit("inline subjects"))
            ));
        }
    }
}

#[test]
fn whole_request_aggregate_and_256_subject_oversized_inline_refuse_before_spawn() {
    // Individually legal eight-GiB snapshot/dependency declarations do not
    // jointly fit the nine-GiB request. No file content is materialized.
    let mut p = plan(true, false);
    let snapshot::Entry::File { byte_length, .. } = &mut p.snapshot[0] else {
        panic!()
    };
    *byte_length = 8_589_934_592;
    let (_, mut manifest) = p.dependency_manifests.pop_first().unwrap();
    let J::Array(rows) = &mut manifest else {
        panic!()
    };
    jreplace(&mut rows[0], "byteLength", jn(8_589_934_592));
    let hash =
        digest_hex(&hash_canonical_value("native.dependency-file-manifest.v1", &manifest).unwrap());
    p.dependency_manifests.insert(hash.clone(), manifest);
    let J::Object(set) = &mut p.dependency_set else {
        panic!()
    };
    let J::Array(packages) = set.get_mut("packages").unwrap() else {
        panic!()
    };
    jreplace(&mut packages[0], "fileManifestSha256", js(&hash));
    jreplace(&mut packages[0], "totalBytes", jn(8_589_934_592));
    let dep_id = native_id("native.dependency-source-set.v1", &p.dependency_set);
    replace(
        &mut p.open.repository_resolution,
        "dependencySourceSetId",
        t(&dep_id),
    );
    let mut resolved = member(&p.open.universe, "resolvedInputs").unwrap().clone();
    replace(&mut resolved, "dependencySourceSetId", t(&dep_id));
    replace(&mut p.open.universe, "resolvedInputs", resolved);
    p.universes[0].value = p.open.universe.clone();
    let source = built_commitment("opensip.rust-provider.universe.v2", &p.open.universe);
    p.stages[0].scopes[0].source = source.clone();
    p.stages[0].scopes[0].target = source;
    assert!(matches!(
        Request::build(p),
        Err(Refusal::WireLimit(schedule::Refusal::PayloadLimit))
    ));

    // RUST3-LIM F-1 is separate from the subject cap: 256 lawful subjects
    // repeated in 256 stages exceed the complete inline Analyze envelope.
    let mut p = plan(false, false);
    p.snapshot = (0..256)
        .map(|i| snapshot::Entry::File {
            path: format!("src/{i:05}-{}.rs", "a".repeat(1024)),
            byte_length: 1,
            content_sha256: "a".repeat(64),
            executable: false,
        })
        .collect();
    let source = p.stages[0].scopes[0].source.clone();
    p.stages = (0..256)
        .map(|i| domain::Stage {
            plan_stage: map(vec![
                ("kind", t("fact-derivation")),
                ("stageId", t(&format!("stage-{i}"))),
                ("operator", t("semantic-provider")),
                ("relations", Value::Array(vec![t("declares")])),
            ]),
            resolved_provider: Some("rust-semantic".into()),
            scopes: vec![domain::Scope {
                relation: "declares".into(),
                resolution: "syntactic".into(),
                source: source.clone(),
                target: source.clone(),
                commitment: format!("sha256:{}", "f".repeat(64)),
            }],
        })
        .collect();
    assert!(matches!(
        Request::build(p),
        Err(Refusal::ProjectionLimit("Analyze envelope bytes"))
    ));
}
