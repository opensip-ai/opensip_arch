//! D2b-4c pinned public synthetic replays. Cases exercise their actual
//! owning wire predicates; illustrative successor Plan values are not C4
//! admission proofs. Trial07's remaining rules are tracked separately until
//! their Rust3 replay/classification is complete.
use super::*;
use crate::provider_protocol::{FrameRefusal, manifest_digest};
const TRIAL: &[u8] = include_bytes!("../../../tests/data/trial07-admission-vectors.v1.json");
const SELECTION: &[u8] = include_bytes!("../../../tests/data/trial07-integer-replay.v1.json");
const LIM: &[u8] = include_bytes!("../../../tests/data/rust3-lim-vectors.v1.json");
const FA2: &[u8] = include_bytes!("../../../tests/data/fa2-vectors.v1.json");
fn corpus() -> J {
    assert_eq!(
        digest_hex(&raw_sha256(TRIAL)),
        "e93c69e57f24c8309544c5773b2394d2c8973d2dcb67da604afb2bb1edc06290"
    );
    assert_eq!(
        digest_hex(&raw_sha256(SELECTION)),
        "79d0ee27533f3c4a5ac2c3f90db9423412304a7148aeaec41582c892f56dc9ae"
    );
    parse_json(SELECTION).unwrap()
}
fn cases(rule: &str) -> Vec<J> {
    let d = corpus();
    let J::Array(v) = path(&d, &["vectors", rule]).unwrap() else {
        panic!()
    };
    v.clone()
}
fn js<'a>(v: &'a J, keys: &[&str]) -> &'a str {
    txt(path(v, keys).unwrap()).unwrap()
}
fn expect(v: &J) -> bool {
    match js(v, &["kind"]) {
        "accept" => true,
        "refuse" => false,
        _ => panic!(),
    }
}
fn optional_string(v: &Value, key: &str) -> Option<String> {
    match get(v, key) {
        Value::Null => None,
        Value::Text(s) => Some(s.clone()),
        _ => panic!(),
    }
}
fn optional_uint(v: &Value, key: &str) -> Option<u64> {
    match get(v, key) {
        Value::Null => None,
        Value::Unsigned(n) => Some(*n),
        _ => panic!(),
    }
}
fn context_for_events(events: &[J]) -> Rust3DispatchContext {
    let mut c = context(false);
    c.analysis_ordinal = 0;
    for e in events {
        match js(e, &["frame"]) {
            "OpenUniverse" => {
                if let Some(J::String(id)) = path(e, &["payload", "executionId"]) {
                    c.open_universe = with(&c.open_universe, "executionId", t(id));
                }
            }
            "Analyze" => {
                if let Some(J::Integer(n)) = path(e, &["payload", "analysisOrdinal"]) {
                    c.analysis_ordinal = u64::try_from(n.get()).unwrap();
                }
            }
            _ => {}
        }
    }
    c
}
/// Only fixed control values omitted by the abstract reference events are
/// supplied by the exact synthetic codec context. Every named event remains
/// in its original order; no fault observation is rewritten.
fn drive(
    r: &mut Rust3Receiver<'_>,
    c: &Rust3DispatchContext,
    events: &[J],
) -> Result<u64, Rust3Refusal> {
    let mut seq = 0;
    for e in events {
        let name = js(e, &["frame"]);
        let host = match name {
            "Hello" => Some(Rust3HostFrame::Hello),
            "OpenUniverse" => Some(Rust3HostFrame::OpenUniverse),
            "SnapshotManifest" => Some(Rust3HostFrame::SnapshotManifest),
            "SnapshotSeal" => Some(Rust3HostFrame::SnapshotSeal),
            "DependencySourceManifest" => Some(Rust3HostFrame::DependencySourceManifest),
            "DependencySourceSeal" => Some(Rust3HostFrame::DependencySourceSeal),
            "Analyze" => Some(Rust3HostFrame::Analyze),
            "Cancel" => Some(Rust3HostFrame::Cancel {
                execution_id: None,
                analysis_ordinal: None,
            }),
            _ => None,
        };
        if let Some(frame) = host {
            r.sent(frame)?;
            continue;
        }
        match name {
            "zero-exit" => {
                r.process(ProcessEvent::ZeroExit)?;
            }
            "eof" => {
                r.process(ProcessEvent::Eof)?;
            }
            _ => {
                let payload = match name {
                    "HelloAck" => {
                        let mut a = ack(c);
                        if let Some(v) = path(e, &["capabilities"]) {
                            a = with(&a, "capabilities", wire(v));
                        }
                        a
                    }
                    "UniverseAccepted" => accepted(c),
                    "SnapshotAccepted" => c.snapshot_seal.clone(),
                    "DependencySourceAccepted" => c.dependency_seal.clone(),
                    "NativeContextVerified" => native(c),
                    "FactBatch" => with(
                        &batch("stage-one", 0, 0),
                        "analysisOrdinal",
                        u(c.analysis_ordinal),
                    ),
                    "CoverageV3" => with(&coverage(0), "analysisOrdinal", u(c.analysis_ordinal)),
                    "Unavailable" => {
                        let entries = a((0..c.stages.len())
                            .map(|i| entry(&key(i), "unknown", t("provider-unavailable")))
                            .collect());
                        m(&[
                            ("analysisOrdinal", u(c.analysis_ordinal)),
                            (
                                "affectedStageIds",
                                a(c.stages
                                    .iter()
                                    .map(|s| get(&s.plan_stage, "stageId").clone())
                                    .collect()),
                            ),
                            ("reason", t("dependency-source-incomplete")),
                            (
                                "coverageCommitment",
                                t(&built("opensip.rust-provider.coverage-stream.v2", &entries)),
                            ),
                            ("coverage", entries),
                        ])
                    }
                    _ => panic!("unimplemented replay event {name}"),
                };
                worker(r, name, payload, seq)?;
                seq += 1;
            }
        }
    }
    Ok(seq)
}
#[test]
fn replay_trial07_canonical_paths_and_raw_manifest_digest() {
    let carriers = Carriers::load("Rust3").unwrap();
    let shape = parse_json(br#"{"t":"ref","ref":"Rust3CanonicalPath"}"#).unwrap();
    let paths = cases("CANONICAL-PATH-ADMISSION");
    assert_eq!(paths.len(), 25);
    for v in paths {
        assert_eq!(
            carriers
                .check(&shape, &t(js(&v, &["input", "path"])), "path")
                .is_ok(),
            expect(&v),
            "{}",
            js(&v, &["id"])
        );
    }
    let shape = parse_json(br#"{"t":"ref","ref":"Rust3DigestHex"}"#).unwrap();
    for v in cases("RAW-MANIFEST-DIGEST") {
        let entries = wire(path(&v, &["input", "manifest", "entries"]).unwrap());
        let claimed = js(&v, &["input", "manifest", "manifestSha256"]);
        // RAW-MANIFEST-DIGEST is the digest of supplied raw entries. These
        // historical illustrative rows do not establish current row shape.
        let ok = carriers
            .check(&shape, &t(claimed), "manifestSha256")
            .is_ok()
            && manifest_digest(&entries) == claimed;
        assert_eq!(ok, expect(&v), "{}", js(&v, &["id"]));
    }
}
#[test]
fn replay_trial07_provider_fault_all_joint_observations() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let rows = cases("RUST3-PROVIDER-FAULT");
    assert_eq!(rows.len(), 13);
    for v in rows {
        let J::Array(events) = path(&v, &["input", "events"]).unwrap() else {
            panic!()
        };
        let c = context_for_events(events);
        let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
        let seq = drive(&mut r, &c, events).unwrap();
        let result = worker(
            &mut r,
            "ProviderFault",
            wire(path(&v, &["input", "fault"]).unwrap()),
            seq,
        );
        assert_eq!(
            result.is_ok(),
            expect(&v),
            "{}: {:?}",
            js(&v, &["id"]),
            result.err()
        );
    }
}
#[test]
fn replay_trial07_budget_payload_and_plan_correlation() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let rows = cases("RUST3-BUDGET-EXHAUSTED");
    assert_eq!(rows.len(), 4);
    for v in rows {
        let mut c = context(false);
        let b = wire(path(&v, &["input", "planBudget"]).unwrap());
        if b == Value::Null {
            let Value::Map(p) = &mut c.stages[0].plan_stage else {
                panic!()
            };
            p.retain(|(k, _)| k != "budget");
        } else {
            c.stages[0].plan_stage = with(&c.stages[0].plan_stage, "budget", b);
        }
        let receiver = Rust3Receiver::new(&table, c.clone());
        if let Err(e) = receiver {
            assert!(!expect(&v), "{}: {e:?}", js(&v, &["id"]));
            assert_eq!(js(&v, &["id"]), "budget-milliseconds");
            continue;
        }
        let mut r = receiver.unwrap();
        let seq = analyzing(&mut r, &c);
        let fields = wire(path(&v, &["input", "payload"]).unwrap());
        let mut payload = budget();
        for name in ["unit", "limit", "observed"] {
            payload = with(&payload, name, get(&fields, name).clone());
        }
        let result = worker(&mut r, "BudgetExhausted", payload, seq);
        assert_eq!(
            result.is_ok(),
            expect(&v),
            "{}: {:?}",
            js(&v, &["id"]),
            result.err()
        );
    }
}
#[test]
fn replay_trial07_deferred_float_zero_is_preserved_and_unencodable_in_real_rust3_framing() {
    let d = corpus();
    let J::Array(deferred) = path(&d, &["deferredVectors"]).unwrap() else {
        panic!()
    };
    assert_eq!(deferred.len(), 1);
    let raw = js(&deferred[0], &["originalVectorJson"]);
    assert_eq!(
        digest_hex(&raw_sha256(raw.as_bytes())),
        "3587eda94e92a75717fd24a4970c55764a43be3c9452b5c554f170d384fc4c97"
    );
    assert!(raw.contains("\"analysisOrdinal\":0.0"));
    assert!(matches!(
        parse_json(raw.as_bytes()),
        Err(opensip_identity::CanonicalError::FloatForbidden)
    ));
    let value = m(&[
        ("protocolMajor", u(3)),
        ("direction", t("host-to-worker")),
        ("sequence", u(1)),
        ("frameType", t("Cancel")),
        (
            "payload",
            m(&[
                ("executionId", Value::Null),
                ("analysisOrdinal", Value::Null),
                ("reason", t("user-interrupt")),
            ]),
        ),
    ]);
    let mut encoded = cbor::encode(&value);
    let key = cbor::encode(&t("analysisOrdinal"));
    let positions: Vec<_> = encoded
        .windows(key.len())
        .enumerate()
        .filter_map(|(i, v)| (v == key).then_some(i + key.len()))
        .collect();
    assert_eq!(positions.len(), 1);
    let at = positions[0];
    assert_eq!(encoded[at], 0xf6);
    encoded.splice(at..at + 1, [0xf9, 0, 0]);
    let mut framed = (encoded.len() as u64).to_be_bytes().to_vec();
    framed.extend(raw_sha256(&encoded));
    framed.extend(encoded);
    assert!(matches!(
        read_frame(
            &mut framed.as_slice(),
            cbor::Profile::Rust3,
            RUST3_FRAME_MAX_DEPTH,
            None
        ),
        Err(FrameRefusal::Cbor(cbor::CborRefusal::FloatOrSimple))
    ));
}
#[test]
fn replay_successor_lim_exact_subjects_commitments_sizes_and_reference_tampering() {
    assert_eq!(
        digest_hex(&raw_sha256(LIM)),
        "d9a09c9e53aef9648e26f7f9016fe968b58222d24176edd82329047bbb5f981c"
    );
    let d = parse_json(LIM).unwrap();
    let snapshot = js(&d, &["snapshotId"]);
    let J::Array(entries) = path(&d, &["manifestEntries"]).unwrap() else {
        panic!()
    };
    let files: Vec<_> = entries
        .iter()
        .filter(|e| js(e, &["kind"]) == "file")
        .map(|e| {
            let J::Integer(n) = path(e, &["byteLength"]).unwrap() else {
                panic!()
            };
            super::super::super::send::domain::File {
                path: js(e, &["path"]).into(),
                byte_length: u64::try_from(n.get()).unwrap(),
                content_sha256: js(e, &["contentSha256"]).into(),
            }
        })
        .collect();
    let law = super::super::super::send::domain::Law::load().unwrap();
    let (subjects, encoded, scope) = law.subjects(snapshot, &files, 200_000, None).unwrap();
    assert_eq!(
        cbor::encode(&subjects),
        cbor::encode(&wire(path(&d, &["subjects"]).unwrap()))
    );
    assert_eq!(
        get(&scope, "subjectScopeCommitment"),
        &t(js(&d, &["subjectScopeCommitment"]))
    );
    assert_eq!(encoded.len(), 447);
    let inline = wire(path(&d, &["stageRequestV2Inline"]).unwrap());
    let reference = wire(path(&d, &["stageRequestV3ByReference"]).unwrap());
    let keys = get(get(&inline, "analysisDomain"), "requestedCoverageDomain");
    assert_eq!(
        super::super::super::send::domain::analysis_commitment(&encoded, keys).unwrap(),
        js(&d, &["domainCommitment"])
    );
    assert_eq!(cbor::encode(&inline).len(), 1137);
    assert_eq!(cbor::encode(&reference).len(), 833);
    // The vectors label their stage/key illustrative. Use an independently
    // valid synthetic host context for the production refusal predicate,
    // retaining the vector's exact snapshot, manifest and reference scope.
    for fault in ["none", "count", "reversed"] {
        let mut c = super::super::super::send::census_context_for_test(2);
        c.open_universe = with(&c.open_universe, "snapshotId", t(snapshot));
        c.snapshot_seal = with(&c.snapshot_seal, "snapshotId", t(snapshot));
        c.manifest_files = files
            .iter()
            .map(|e| (e.path.clone(), (e.content_sha256.clone(), e.byte_length)))
            .collect();
        let mut actual_scope = scope.clone();
        if fault == "count" {
            actual_scope = with(&actual_scope, "subjectCount", u(4));
        } else if fault == "reversed" {
            let J::Array(refusals) = path(&d, &["refusals"]).unwrap() else {
                panic!()
            };
            actual_scope = with(
                &actual_scope,
                "subjectScopeCommitment",
                t(js(&refusals[1], &["value"])),
            );
        }
        let domain = &c.stages[0].analysis_domain;
        let actual_keys = get(domain, "requestedCoverageDomain");
        let commitment =
            super::super::super::send::domain::analysis_commitment(&encoded, actual_keys).unwrap();
        c.stages[0].analysis_domain = with(
            &with(domain, "subjectScope", actual_scope),
            "domainCommitment",
            t(&commitment),
        );
        let table = Table::load(Protocol::Rust3).unwrap();
        assert_eq!(
            Rust3Receiver::new(&table, c).is_ok(),
            fault == "none",
            "{fault}"
        );
    }
}
#[test]
fn replay_successor_fa2_native_h_oracle_and_real_d_empty_request_check() {
    assert_eq!(
        digest_hex(&raw_sha256(FA2)),
        "6bc14639bef0d6095ceb6c57f317f17b239869f51204e50489ce2087fe9cf7d3"
    );
    let d = parse_json(FA2).unwrap();
    let original = parse_json(js(&d, &["oracle", "canonicalUtf8"]).as_bytes()).unwrap();
    let hash = opensip_identity::hash_canonical_value("subject-scope", &original).unwrap();
    assert_eq!(
        format!("scope2:{}", digest_hex(&hash)),
        js(&d, &["oracle", "expectedScopeId"])
    );
    let descriptor = wire(path(&d, &["censusFreeOfOracleDescriptor", "descriptor"]).unwrap());
    let law = super::super::super::census::Law::load().unwrap();
    let key = m(&[
        (
            "sourceUniverseId",
            t(&format!(
                "sha256:{}",
                text_of(map_of(&descriptor).unwrap(), "sourceUniverse").unwrap()
            )),
        ),
        (
            "targetUniverseId",
            t(&format!(
                "sha256:{}",
                text_of(map_of(&descriptor).unwrap(), "targetUniverse").unwrap()
            )),
        ),
        ("relation", get(&descriptor, "relation").clone()),
        ("resolution", get(&descriptor, "resolution").clone()),
    ]);
    let got = law
        .empty_scope(
            text_of(map_of(&descriptor).unwrap(), "snapshotId").unwrap(),
            &key,
            text_of(map_of(&descriptor).unwrap(), "enumeratorClosure").unwrap(),
        )
        .unwrap();
    assert_eq!(
        got,
        js(
            &d,
            &[
                "censusFreeOfOracleDescriptor",
                "computed",
                "subjectScopeCommitment"
            ]
        )
    );
}

fn observation_prefix(id: &str, omit_analyze: bool) -> Vec<J> {
    let v = cases("RUST3-PROVIDER-FAULT")
        .into_iter()
        .find(|v| js(v, &["id"]) == id)
        .unwrap();
    let J::Array(mut events) = path(&v, &["input", "events"]).unwrap().clone() else {
        panic!()
    };
    if omit_analyze {
        assert_eq!(js(events.last().unwrap(), &["frame"]), "Analyze");
        events.pop();
    }
    events
}
#[test]
fn replay_trial07_cancel_nullability_and_cancelled_exact_send_phase() {
    let table = Table::load(Protocol::Rust3).unwrap();
    for v in cases("CANCEL-NULLABILITY") {
        let J::Array(sent) = path(&v, &["input", "sent"]).unwrap() else {
            panic!()
        };
        let mut c = context_for_events(sent);
        c.analysis_ordinal = 0;
        let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
        if sent.iter().any(|e| js(e, &["frame"]) == "Analyze") {
            analyzing(&mut r, &c);
        } else if sent.iter().any(|e| js(e, &["frame"]) == "OpenUniverse") {
            r.sent(Rust3HostFrame::Hello).unwrap();
            worker(&mut r, "HelloAck", ack(&c), 0).unwrap();
            r.sent(Rust3HostFrame::OpenUniverse).unwrap();
        } else {
            r.sent(Rust3HostFrame::Hello).unwrap();
        }
        let cancel = wire(path(&v, &["input", "cancel"]).unwrap());
        let result = r.sent(Rust3HostFrame::Cancel {
            execution_id: optional_string(&cancel, "executionId"),
            analysis_ordinal: optional_uint(&cancel, "analysisOrdinal"),
        });
        assert_eq!(
            result.is_ok(),
            expect(&v),
            "{}: {:?}",
            js(&v, &["id"]),
            result.err()
        );
    }
    for (rule, prefix, omit) in [
        ("CANCELLED-ECHO", "fault-inflight-analyze-read", true),
        (
            "RUST3-CANCEL-TYPES",
            "fault-inflight-snapshot-manifest-unread",
            false,
        ),
    ] {
        for v in cases(rule) {
            let events = observation_prefix(prefix, omit);
            let c = context_for_events(&events);
            let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
            let seq = drive(&mut r, &c, &events).unwrap();
            let cancel = wire(path(&v, &["input", "cancel"]).unwrap());
            r.sent(Rust3HostFrame::Cancel {
                execution_id: optional_string(&cancel, "executionId"),
                analysis_ordinal: optional_uint(&cancel, "analysisOrdinal"),
            })
            .unwrap();
            let result = worker(
                &mut r,
                "Cancelled",
                wire(path(&v, &["input", "cancelled"]).unwrap()),
                seq,
            );
            assert_eq!(
                result.is_ok(),
                expect(&v),
                "{}: {:?}",
                js(&v, &["id"]),
                result.err()
            );
        }
    }
}
#[test]
fn replay_trial07_rust3_p3_overlay_through_the_actual_codec() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let rows = cases("P3-OVERLAY");
    assert_eq!(rows.len(), 5);
    for v in rows {
        let J::Array(events) = path(&v, &["input", "events"]).unwrap() else {
            panic!()
        };
        let mut c = context_for_events(events);
        let J::Integer(stages) = path(&v, &["input", "stageCount"]).unwrap() else {
            panic!()
        };
        c.stages.truncate(usize::try_from(stages.get()).unwrap());
        let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
        let result = drive(&mut r, &c, events);
        if !expect(&v) {
            assert!(
                matches!(&result,Err(Rust3Refusal::Table(trace))if trace=="P3-34"),
                "{}: {result:?}",
                js(&v, &["id"])
            );
        } else {
            assert!(result.is_ok(), "{}: {result:?}", js(&v, &["id"]));
        }
    }
}

#[test]
fn replay_trial07_accepted_equals_actual_sent_snapshot_seal() {
    let table = Table::load(Protocol::Rust3).unwrap();
    for v in cases("ACCEPTED-EQUALS-SEAL") {
        let mut c = context(false);
        c.snapshot_seal = wire(path(&v, &["input", "seal"]).unwrap());
        c.open_universe = with(
            &c.open_universe,
            "snapshotId",
            get(&c.snapshot_seal, "snapshotId").clone(),
        );
        let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
        r.sent(Rust3HostFrame::Hello).unwrap();
        worker(&mut r, "HelloAck", ack(&c), 0).unwrap();
        r.sent(Rust3HostFrame::OpenUniverse).unwrap();
        worker(&mut r, "UniverseAccepted", accepted(&c), 1).unwrap();
        r.sent(Rust3HostFrame::SnapshotManifest).unwrap();
        r.sent(Rust3HostFrame::SnapshotSeal).unwrap();
        let result = worker(
            &mut r,
            "SnapshotAccepted",
            wire(path(&v, &["input", "accepted"]).unwrap()),
            2,
        );
        assert_eq!(
            result.is_ok(),
            expect(&v),
            "{}: {:?}",
            js(&v, &["id"]),
            result.err()
        );
    }
}
#[test]
fn replay_trial07_rust_commit_map_uses_selected_domains_and_received_preimage_classes() {
    let law = Law::load().unwrap();
    let doc = parse_json(carrier::CARRIERS).unwrap();
    let J::Array(rows) = path(&doc, &["commitmentMap", "rows"]).unwrap() else {
        panic!()
    };
    let rpp = parse_json(RPP).unwrap();
    let mut count = 0;
    for v in cases("COMMIT-MAP") {
        // The four delivery2 fields belong to TS2's separate accepted replay.
        if js(&v, &["input", "commitment", "$ownerCommit", "doc"]) != "rust2" {
            continue;
        }
        let field = js(&v, &["input", "field"]);
        let row = rows.iter().find(|r| js(r, &["field"]) == field).unwrap();
        let actual_domain = law.domain(field).unwrap();
        let recipe = js(&v, &["input", "commitment", "$ownerCommit", "recipe"]);
        let text = txt(path(&rpp, &["commitments", recipe]).unwrap()).unwrap();
        let reference_domain = text
            .split("UTF8(")
            .nth(1)
            .unwrap()
            .split(')')
            .next()
            .unwrap();
        let stages = wire(path(&v, &["input", "stages"]).unwrap());
        let original = received("RawPreimages", m(&[("stages", stages.clone())]), 0);
        let env = map_of(original.value()).unwrap();
        let payload = child(&original, 0, env, "payload").unwrap();
        let pf = map_of(get(original.value(), "payload")).unwrap();
        let list = child(&original, payload, pf, "stages").unwrap();
        let stage_nodes: Vec<_> = original.children(list).collect();
        let actual_nodes: Vec<_> = match js(row, &["valueClass"]) {
            "stage-major-entries" => stage_nodes
                .iter()
                .flat_map(|&n| original.children(n))
                .collect(),
            "stage-entries" => original.children(stage_nodes[0]).collect(),
            other => panic!("{other}"),
        };
        let actual: Vec<_> = actual_nodes
            .iter()
            .map(|&n| original.node(n).unwrap())
            .collect();
        let Value::Array(stages) = stages else {
            panic!()
        };
        let claimed = match js(&v, &["input", "commitment", "$ownerCommit", "value"]) {
            "stage-major" => a(stages
                .into_iter()
                .flat_map(|s| if let Value::Array(a) = s { a } else { panic!() })
                .collect()),
            "stage" => stages[0].clone(),
            other => panic!("{other}"),
        };
        assert_eq!(
            commit(actual_domain, &actual) == built(reference_domain, &claimed),
            expect(&v),
            "{}",
            js(&v, &["id"])
        );
        count += 1;
    }
    assert_eq!(count, 10);
}

#[test]
fn replay_trial07_rust_anchor_wire_values_and_the_actual_100001_count() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let mut count = 0;
    for v in cases("ANCHOR-WIRE-SPAN") {
        if js(&v, &["input", "language"]) != "rust-semantic" {
            continue;
        }
        let J::Object(manifest) = path(&v, &["input", "manifest"]).unwrap() else {
            panic!()
        };
        let mut c = context(false);
        c.manifest_files = manifest
            .iter()
            .map(|(p, e)| {
                let J::Integer(n) = path(e, &["byteLength"]).unwrap() else {
                    panic!()
                };
                (
                    p.clone(),
                    (
                        js(e, &["contentSha256"]).into(),
                        u64::try_from(n.get()).unwrap(),
                    ),
                )
            })
            .collect();
        let input = path(&v, &["input", "anchors"]).unwrap();
        let anchors = if let Some(repeated) = path(input, &["$repeat"]) {
            let J::Integer(n) = path(repeated, &["n"]).unwrap() else {
                panic!()
            };
            assert_eq!(n.get(), 100_001);
            a(vec![wire(path(repeated, &["item"]).unwrap()); 100_001])
        } else {
            wire(input)
        };
        let Value::Array(rows) = &anchors else {
            panic!()
        };
        let snapshot = get(&rows[0], "snapshotId");
        c.open_universe = with(&c.open_universe, "snapshotId", snapshot.clone());
        c.snapshot_seal = with(&c.snapshot_seal, "snapshotId", snapshot.clone());
        let candidate = with(&candidate(0), "anchors", anchors);
        let payload = with(&batch("stage-one", 0, 0), "candidates", a(vec![candidate]));
        let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
        let seq = analyzing(&mut r, &c);
        let result = worker(&mut r, "FactBatch", payload, seq);
        assert_eq!(
            result.is_ok(),
            expect(&v),
            "{}: {:?}",
            js(&v, &["id"]),
            result.err()
        );
        count += 1;
    }
    assert_eq!(count, 5);
}
#[test]
fn replay_trial07_occupancy_joins_actual_rust_candidates_and_companions() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let rows = cases("OCCUPANCY-JOIN");
    assert_eq!(rows.len(), 3);
    for v in rows {
        let J::Array(candidates) = path(&v, &["input", "batch", "candidates"]).unwrap() else {
            panic!()
        };
        let J::Array(companions) = path(&v, &["input", "batch", "occupancyCompanions"]).unwrap()
        else {
            panic!()
        };
        let mut c = context(true);
        for row in candidates.iter().chain(companions) {
            c.target_domain
                .insert(js(row, &["targetUniverseId"]).into());
        }
        let values = candidates
            .iter()
            .map(|row| {
                let J::Integer(ordinal) = path(row, &["candidateOrdinal"]).unwrap() else {
                    panic!()
                };
                with(
                    &candidate(u64::try_from(ordinal.get()).unwrap()),
                    "targetUniverseId",
                    t(js(row, &["targetUniverseId"])),
                )
            })
            .collect();
        let companions = companions
            .iter()
            .map(|row| {
                let J::Integer(ordinal) = path(row, &["candidateOrdinal"]).unwrap() else {
                    panic!()
                };
                with(
                    &with(
                        &companion(),
                        "candidateOrdinal",
                        u(u64::try_from(ordinal.get()).unwrap()),
                    ),
                    "targetUniverseId",
                    t(js(row, &["targetUniverseId"])),
                )
            })
            .collect();
        let payload = with(
            &with(
                &with(&batch("stage-one", 0, 0), "schemaVersion", u(3)),
                "candidates",
                a(values),
            ),
            "occupancyCompanions",
            a(companions),
        );
        let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
        let seq = analyzing(&mut r, &c);
        let result = worker(&mut r, "FactBatch", payload, seq);
        assert_eq!(
            result.is_ok(),
            expect(&v),
            "{}: {:?}",
            js(&v, &["id"]),
            result.err()
        );
    }
}

/// Historical path checks through selected enclosing schemas, never copied
/// regular expressions. Native identity, C4 admission, ownership and source
/// custody remain separate obligations.
#[test]
fn replay_trial07_rust_path_sites_against_exact_selected_schema_predicates() {
    let registry = crate::schema_sources::registry().unwrap();
    let native = "urn:opensip:product-v1:native:evidence-schemas:v2";
    let mut count = 0;
    for v in cases("PATH-SITE-SEGMENT-LAW") {
        let text = t(js(&v, &["input", "value"]));
        let (schema, selector, value) = match js(&v, &["input", "site"]) {
            "generated-logicalPath" => (
                native,
                "/$defs/GeneratedFileV1",
                m(&[
                    ("logicalPath", text),
                    (
                        "blob",
                        m(&[
                            ("byteLength", u(0)),
                            ("sha256", t(&h('a'))),
                            ("mediaType", t("application/octet-stream")),
                        ]),
                    ),
                ]),
            ),
            "expansion-site-path" => (
                native,
                "/$defs/ExpansionSiteV1",
                m(&[
                    ("path", text),
                    ("startByte", u(0)),
                    ("endByte", u(0)),
                    ("inputTokenDigest", t(&h('a'))),
                ]),
            ),
            "crateRootPaths" => {
                let c = context(false);
                let inputs = get(get(&c.open_universe, "universe"), "resolvedInputs");
                (
                    native,
                    "/$defs/RustUniverseV2ResolvedInputs",
                    with(inputs, "crateRootPaths", a(vec![text])),
                )
            }
            "dependency-manifest-path" => (
                native,
                "/$defs/DependencySourceManifestV3",
                m(&[
                    ("dependencySourceSetId", t(&format!("sha256:{}", h('a')))),
                    ("manifestSha256", t(&h('b'))),
                    (
                        "entries",
                        a(vec![m(&[
                            ("packageKey", t("a 1 source")),
                            ("path", text),
                            ("byteLength", u(0)),
                            ("contentSha256", t(&h('c'))),
                        ])]),
                    ),
                ]),
            ),
            "occupancy-LogicalPath" => (
                "opensip.product.occupancy-companion.1",
                "/$defs/LogicalPath",
                text,
            ),
            "jsRootFiles" | "programRootFiles" => continue, // TS2's ten sites.
            site => panic!("unclassified path site {site}"),
        };
        let value = crate::provider_protocol::ts2::carrier::to_json(&value).unwrap();
        let handle = registry.schema(schema, selector).unwrap();
        let result = handle.admit_value(
            &value,
            crate::provider_protocol::ts2::carrier::SCHEMA_BUDGET,
        );
        assert_eq!(
            result.is_ok(),
            expect(&v),
            "{} at {selector}: {:?}",
            js(&v, &["id"]),
            result.err()
        );
        count += 1;
    }
    assert_eq!(count, 25);
    let mut logical = 0;
    for v in cases("OWNER-PATTERN-EVALUATION") {
        if js(&v, &["input", "owner", "call"]) != "logical-re" {
            continue;
        }
        let value = J::String(js(&v, &["input", "owner", "value"]).into());
        for schema in [
            "opensip.product.occupancy-companion.1",
            "opensip.product.symbol-census.1",
        ] {
            let handle = registry.schema(schema, "/$defs/LogicalPath").unwrap();
            assert_eq!(
                handle
                    .admit_value(
                        &value,
                        crate::provider_protocol::ts2::carrier::SCHEMA_BUDGET
                    )
                    .is_ok(),
                expect(&v),
                "{} at {schema}",
                js(&v, &["id"])
            );
        }
        logical += 1;
    }
    assert_eq!(logical, 2);
}

#[test]
fn replay_trial07_rust_fact_ref_anchor_is_refused_at_actual_batch_admission() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let mut count = 0;
    for v in cases("ANCHOR-FACT-REF-REFUSED") {
        if js(&v, &["input", "language"]) != "rust-semantic" {
            continue;
        }
        let c = context(false);
        let mut receiver = Rust3Receiver::new(&table, c.clone()).unwrap();
        let seq = analyzing(&mut receiver, &c);
        let anchors = wire(path(&v, &["input", "anchors"]).unwrap());
        let payload = with(
            &batch("stage-one", 0, 0),
            "candidates",
            a(vec![with(&candidate(0), "anchors", anchors)]),
        );
        let got = worker(&mut receiver, "FactBatch", payload, seq);
        assert!(!expect(&v));
        assert!(
            matches!(got, Err(Rust3Refusal::Admission(_))),
            "{}: {got:?}",
            js(&v, &["id"])
        );
        count += 1;
    }
    assert_eq!(count, 1);
}

/// The four additional OWNER-PATTERN cases reached by startup wire or
/// prepared-output wire. Native file-manifest/set admission stays with C4.
#[test]
fn replay_trial07_owner_patterns_reached_by_rust_startup_and_generated_wire() {
    const ACCOUNT: &[u8] =
        include_bytes!("../../../tests/data/trial07-accounting-fixtures.v1.json");
    const PREP: &[u8] = include_bytes!("../../../tests/data/trial07-prepared-fixture.v1.json");
    assert_eq!(
        digest_hex(&raw_sha256(ACCOUNT)),
        "cb582ebec92077800b288e39092b8e5205c3de54bc13cc736165c44761e0bd15"
    );
    assert_eq!(
        digest_hex(&raw_sha256(PREP)),
        "b6ccb101133a573230a94afaebf12ab3716074ea511f5a7844f835ba6024115b"
    );
    let prep = parse_json(PREP).unwrap();
    let registry = crate::schema_sources::registry().unwrap();
    let schemas = super::super::super::schemas::Rust3PayloadSchemas::load().unwrap();
    let mut count = 0;
    for v in cases("OWNER-PATTERN-EVALUATION") {
        let call = js(&v, &["input", "owner", "call"]);
        let text = t(js(&v, &["input", "owner", "value"]));
        let got = match call {
            "startup-open-universe" => {
                // The original startup fixture predates the selected closed
                // carrier. Preserve the original tested path in a current
                // schema-shaped context; no historical whole-frame or C4
                // admission is inferred from this scoped path check.
                let open = context(false).open_universe;
                let universe = get(&open, "universe");
                let resolved = get(universe, "resolvedInputs");
                let resolved = with(resolved, "crateRootPaths", a(vec![text]));
                let open = with(
                    &open,
                    "universe",
                    with(universe, "resolvedInputs", resolved),
                );
                schemas.check_payload("OpenUniverse", &open, "WAIT_UNIVERSE_ACCEPTED", false)
            }
            "validate" if js(&v, &["input", "owner", "def"]) == "GeneratedFileV1" => {
                let J::Array(rows) = path(&prep, &["fixture", "rows"]).unwrap() else {
                    panic!()
                };
                let row = rows
                    .iter()
                    .find(|r| js(r, &["kind"]) == "generated-file")
                    .unwrap();
                let generated = with(
                    &wire(path(row, &["generated"]).unwrap()),
                    "logicalPath",
                    text,
                );
                let model = crate::provider_protocol::ts2::carrier::to_json(&generated).unwrap();
                registry
                    .schema(
                        "urn:opensip:product-v1:native:evidence-schemas:v2",
                        "/$defs/GeneratedFileV1",
                    )
                    .unwrap()
                    .admit_value(
                        &model,
                        crate::provider_protocol::ts2::carrier::SCHEMA_BUDGET,
                    )
                    .map(|_| ())
                    .map_err(|e| format!("{e:?}"))
            }
            _ => continue,
        };
        assert_eq!(got.is_ok(), expect(&v), "{}: {got:?}", js(&v, &["id"]));
        count += 1;
    }
    assert_eq!(count, 4);
}

/// The complete rule/case partition is reviewed beside the implementation.
/// Every original integer case must occur once; owner-external cases cannot
/// silently become Rust3 passes. The deferred rawfloat remains separate.
#[test]
fn replay_trial07_scope_covers_all_31_rules_and_all_353_original_cases() {
    const SCOPE: &[u8] = include_bytes!("../../../tests/data/rust3-trial07-replay-scope.v1.json");
    assert_eq!(
        digest_hex(&raw_sha256(SCOPE)),
        "448caaefa3b519d55f06fa18ae02dcd6e1f1359c5076272d40af5a1651d3ca08"
    );
    let scope = parse_json(SCOPE).unwrap();
    let corpus = corpus();
    assert_eq!(
        js(&scope, &["sources", "originalAdmissionSha256"]),
        digest_hex(&raw_sha256(TRIAL))
    );
    assert_eq!(
        js(&scope, &["sources", "integerSelectionSha256"]),
        digest_hex(&raw_sha256(SELECTION))
    );
    let J::Object(vectors) = path(&corpus, &["vectors"]).unwrap() else {
        panic!()
    };
    let J::Array(rules) = path(&scope, &["rules"]).unwrap() else {
        panic!()
    };
    assert_eq!(rules.len(), 31);
    assert_eq!(vectors.len(), 31);
    let mut seen_rules = std::collections::BTreeSet::new();
    let mut seen = std::collections::BTreeSet::new();
    let mut counts = std::collections::BTreeMap::<String, usize>::new();
    for rule in rules {
        let name = js(rule, &["rule"]);
        assert!(seen_rules.insert(name));
        let J::Array(originals) = &vectors[name] else {
            panic!()
        };
        let J::Array(rows) = path(rule, &["cases"]).unwrap() else {
            panic!()
        };
        assert_eq!(rows.len(), originals.len());
        let expected = originals
            .iter()
            .map(|v| js(v, &["id"]))
            .collect::<std::collections::BTreeSet<_>>();
        let mut found = std::collections::BTreeSet::new();
        for row in rows {
            let id = js(row, &["id"]);
            assert!(expected.contains(id));
            assert!(found.insert(id));
            assert!(seen.insert((name, id)));
            let disposition = js(row, &["disposition"]);
            assert!(
                ["rust3-scoped-predicate", "ts2-separate", "upstream-owner"].contains(&disposition)
            );
            *counts.entry(disposition.into()).or_default() += 1;
            assert!(!js(row, &["reason"]).is_empty());
        }
        assert_eq!(expected, found);
    }
    assert_eq!(seen.len(), 352);
    assert_eq!(counts["rust3-scoped-predicate"], 194);
    assert_eq!(counts["ts2-separate"], 48);
    assert_eq!(counts["upstream-owner"], 110);
    assert_eq!(js(&scope, &["rawFloat", "rule"]), "HOST-SEND-SCHEDULE");
    assert_eq!(
        js(&scope, &["rawFloat", "rawVectorSha256"]),
        "3587eda94e92a75717fd24a4970c55764a43be3c9452b5c554f170d384fc4c97"
    );
}

/// Native-cases LD14 supplement: exact Rust limit values through the actual
/// host builder, and original empty dependency payloads through their current
/// selected schema predicates. The shared TS2 limit branch stays separate.
#[test]
fn replay_native_cases_rust_limits_and_empty_dependency_shapes() {
    const DATA: &[u8] = include_bytes!("../../../tests/data/native-wire-public-fixtures.v1.json");
    assert_eq!(
        digest_hex(&raw_sha256(DATA)),
        "04b041d2db1f4ec3a495dae41bfc5088b62ecc9d3b8738aa18fc22531a80ba23"
    );
    let doc = parse_json(DATA).unwrap();
    let J::Array(cases) = path(&doc, &["cases"]).unwrap() else {
        panic!()
    };
    assert_eq!(cases.len(), 2);
    let limits = wire(path(&doc, &["fixtures", "wireRustProtocolLimitsV3"]).unwrap());
    let context = super::super::super::send::census_context_for_test(0);
    assert_eq!(
        cbor::encode(get(&context.hello, "limits")),
        cbor::encode(&limits)
    );
    let schemas = super::super::super::schemas::Rust3PayloadSchemas::load().unwrap();
    for (name, key) in [
        (
            "DependencySourceManifest",
            "startupRustEmptyDependencyManifest",
        ),
        ("DependencySourceSeal", "startupRustEmptyDependencySeal"),
    ] {
        let payload = wire(path(&doc, &["fixtures", key]).unwrap());
        assert!(
            schemas
                .check_payload(name, &payload, "WAIT_DEPENDENCY_SOURCE_ACCEPTED", false)
                .is_ok(),
            "{name}"
        );
    }
}

/// LD14's old literal inputs are not silently relabeled to fit RCA-1, nor
/// are a first-frame shape refusal and a historical later-stage diagnostic
/// treated as equivalent. This records current profile differences only.
#[test]
fn replay_native_rust_literal_profile_differences_without_commit_relabeling() {
    const DATA: &[u8] = include_bytes!("../../../tests/data/native-rust3-profile-cases.v1.json");
    const HANDSHAKE: &[u8] =
        include_bytes!("../../../../../schemas/sources/handshake-v1.schema.json");
    assert_eq!(
        digest_hex(&raw_sha256(DATA)),
        "de0ddb7fcca9b85a28432ca97089a92eeaf9d86638761add21a0149c34f821c0"
    );
    let doc = parse_json(DATA).unwrap();
    assert_eq!(
        js(&doc, &["currentAuthority", "sha256"]),
        digest_hex(&raw_sha256(HANDSHAKE))
    );
    let handshake = parse_json(HANDSHAKE).unwrap();
    assert_eq!(
        js(
            &handshake,
            &[
                "$defs",
                "ExpectedRustIdentityV3",
                "properties",
                "rustCommitHash",
                "pattern"
            ]
        ),
        "^[0-9a-f]{40}(?![\\s\\S])"
    );
    let schemas = super::super::super::schemas::Rust3PayloadSchemas::load().unwrap();
    let J::Array(rows) = path(&doc, &["legacyLiteralViews"]).unwrap() else {
        panic!()
    };
    assert_eq!(rows.len(), 34);
    for row in rows {
        let name = js(row, &["frameType"]);
        let payload = wire(path(row, &["payload"]).unwrap());
        let J::Bool(attribution) = path(row, &["targetAttribution"]).unwrap() else {
            panic!()
        };
        let got = schemas.check_payload(name, &payload, "ANALYZING", *attribution);
        assert!(
            got.is_err(),
            "{} literal current-profile {name} unexpectedly admitted",
            js(row, &["caseId"])
        );
    }
}
#[test]
fn replay_native_shared_schema_bool_values_are_not_integer_values() {
    const DATA: &[u8] = include_bytes!("../../../tests/data/native-rust3-profile-cases.v1.json");
    assert_eq!(
        digest_hex(&raw_sha256(DATA)),
        "de0ddb7fcca9b85a28432ca97089a92eeaf9d86638761add21a0149c34f821c0"
    );
    let doc = parse_json(DATA).unwrap();
    let J::Array(rows) = path(&doc, &["sharedSchemaRefusals"]).unwrap() else {
        panic!()
    };
    assert_eq!(rows.len(), 2);
    let registry = crate::schema_sources::registry().unwrap();
    for row in rows {
        let name = js(row, &["definition"]);
        let handle = registry
            .schema(
                "urn:opensip:product-v1:native:evidence-schemas:v2",
                &format!("/$defs/{name}"),
            )
            .unwrap();
        assert!(
            handle
                .admit_value(
                    path(row, &["value"]).unwrap(),
                    crate::provider_protocol::ts2::carrier::SCHEMA_BUDGET
                )
                .is_err(),
            "{} {name}",
            js(row, &["caseId"])
        );
    }
}
