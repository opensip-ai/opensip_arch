// Unit D2b-3a's controls: a lawful TS2 session end to end, then each step's
// refusals, each before the table is matched and before any payload is
// published, the commitments over received bytes and their provenance, and
// the depth bounds recomputed from the documents.
use super::super::{built_commitment, read_frame, write_frame};
use super::*;
use opensip_contracts::generated::protocol::Ts2FrameV2Payload as P;

fn h(c: char) -> String {
    std::iter::repeat_n(c, 64).collect()
}
fn sha(c: char) -> String {
    format!("sha256:{}", h(c))
}
fn t(s: &str) -> Value {
    Value::Text(s.to_owned())
}
fn u(n: u64) -> Value {
    Value::Unsigned(n)
}
fn m(pairs: &[(&str, Value)]) -> Value {
    Value::Map(
        pairs
            .iter()
            .map(|(k, v)| ((*k).to_owned(), v.clone()))
            .collect(),
    )
}
fn a(items: Vec<Value>) -> Value {
    Value::Array(items)
}
/// Replace (or add) member `k` of map `v`.
fn with(v: &Value, k: &str, x: Value) -> Value {
    let Value::Map(f) = v else { panic!("map") };
    let mut f: Vec<(String, Value)> = f.iter().filter(|(n, _)| n != k).cloned().collect();
    f.push((k.to_owned(), x));
    Value::Map(f)
}
fn without(v: &Value, k: &str) -> Value {
    let Value::Map(f) = v else { panic!("map") };
    Value::Map(f.iter().filter(|(n, _)| n != k).cloned().collect())
}
fn get<'v>(v: &'v Value, k: &str) -> &'v Value {
    let Value::Map(f) = v else { panic!("map") };
    field(f, k).unwrap()
}

const TOKENS: [&str; 4] = [
    "coverage-v3",
    "fact-identity-fact2",
    "plan-identity-plan2",
    "source-identity-snapshot2",
];
const EXEC: &str = "exec1_0123456789abcdef0123456789abcdef";
const BUILD: &str = "typescript-provider 1.0.0";
const PATH: &str = "src/a.ts";

fn context(tokens: &[&str]) -> DispatchContext {
    let text = |s: &str| t(s);
    let provider = BTreeMap::from_iter([
        ("providerBuildId".to_owned(), text(BUILD)),
        ("protocolMajor".to_owned(), u(2)),
        ("typescriptVersion".to_owned(), text("5.9.2")),
        ("typescriptCompilerSha256".to_owned(), text(&h('1'))),
        ("typescriptStdlibMerkleRoot".to_owned(), text(&h('2'))),
        (
            "defaultWorkBudgetProfileId".to_owned(),
            text("typescript-provider-default-work-budget-v1"),
        ),
        (
            "defaultWorkBudgetProfileSha256".to_owned(),
            text("bf7305a12d26a1938b615c861f995d66eac494915e6140c4942a2ea6f0846da6"),
        ),
    ]);
    let runtime = BTreeMap::from_iter([
        ("nodeVersion".to_owned(), text("24.16.0")),
        ("v8Version".to_owned(), text("13.6")),
        ("modulesAbi".to_owned(), text("137")),
        ("platformId".to_owned(), text("darwin-arm64")),
    ]);
    let budget = BTreeMap::from_iter(
        [
            "sourceFilesVisited",
            "astNodesVisited",
            "moduleResolutionQueries",
            "typeQueries",
            "factsEmitted",
            "factBytesEmitted",
        ]
        .iter()
        .map(|k| ((*k).to_owned(), 100u64)),
    );
    let key = |c: char| RequestedKey {
        relation: "calls".to_owned(),
        resolution: "syntactic-callee-name".to_owned(),
        source_universe_id: sha('5'),
        target_universe_id: sha('6'),
        subject_scope_commitment: sha(c),
    };
    let stage = |id: &str, ordinal: u64, c: char| StageBinding {
        expected_stage_id: id.to_owned(),
        stage_ordinal: ordinal,
        relations: vec!["calls".to_owned()],
        budget: budget.clone(),
        keys: vec![key(c)],
    };
    DispatchContext {
        capabilities: tokens.iter().map(|s| (*s).to_owned()).collect(),
        identity_versions: BTreeMap::from_iter([
            ("coverage".to_owned(), 3),
            ("fact".to_owned(), 2),
            ("plan".to_owned(), 2),
            ("snapshot".to_owned(), 2),
        ]),
        expected_provider_descriptor_sha256: h('3'),
        expected_runtime_descriptor_sha256: h('4'),
        provider_descriptor: provider,
        runtime_descriptor: runtime,
        execution_id: EXEC.to_owned(),
        snapshot_id: format!("snapshot2:{}", h('7')),
        plan_id: format!("plan2:{}", h('8')),
        universe_key: sha('5'),
        native_context_id: sha('9'),
        manifest_files: BTreeMap::from_iter([(PATH.to_owned(), (h('a'), 100))]),
        manifest_sha256: h('b'),
        entry_count: 1,
        total_file_bytes: 100,
        total_chunk_count: 1,
        stages: vec![stage("stage-one", 0, 'c'), stage("stage-two", 1, 'd')],
        target_domain: BTreeSet::from_iter([sha('6')]),
        symbol_census: None,
    }
}

fn hello_ack(c: &DispatchContext) -> Value {
    let mut f: Vec<(String, Value)> = c
        .provider_descriptor
        .iter()
        .chain(&c.runtime_descriptor)
        .map(|(k, v)| (k.clone(), v.clone()))
        .collect();
    f.push((
        "capabilities".to_owned(),
        a(c.capabilities.iter().map(|s| t(s)).collect()),
    ));
    f.push((
        "identityVersions".to_owned(),
        Value::Map(
            c.identity_versions
                .iter()
                .map(|(k, v)| (k.clone(), u(*v)))
                .collect(),
        ),
    ));
    f.push((
        "providerDescriptorSha256".to_owned(),
        t(&c.expected_provider_descriptor_sha256),
    ));
    f.push((
        "runtimeDescriptorSha256".to_owned(),
        t(&c.expected_runtime_descriptor_sha256),
    ));
    Value::Map(f)
}
fn universe_accepted(c: &DispatchContext) -> Value {
    m(&[
        ("executionId", t(&c.execution_id)),
        ("snapshotId", t(&c.snapshot_id)),
        ("planId", t(&c.plan_id)),
        ("universeKey", t(&c.universe_key)),
    ])
}
fn snapshot_accepted(c: &DispatchContext) -> Value {
    m(&[
        ("snapshotId", t(&c.snapshot_id)),
        ("manifestSha256", t(&c.manifest_sha256)),
        ("entryCount", u(c.entry_count)),
        ("totalFileBytes", u(c.total_file_bytes)),
        ("totalChunkCount", u(c.total_chunk_count)),
    ])
}
fn native_context_verified(c: &DispatchContext) -> Value {
    m(&[
        ("nativeContextId", t(&c.native_context_id)),
        ("recomputedNativeContextId", t(&c.native_context_id)),
        ("equal", Value::Bool(true)),
    ])
}
fn anchor(c: &DispatchContext, start: u64, end: u64) -> Value {
    m(&[
        ("kind", t("source-span")),
        ("snapshotId", t(&c.snapshot_id)),
        ("path", t(PATH)),
        ("contentSha256", t(&h('a'))),
        ("startByte", u(start)),
        ("endByte", u(end)),
        ("factId", Value::Null),
    ])
}
fn candidate(c: &DispatchContext, ordinal: u64) -> Value {
    m(&[
        ("candidateOrdinal", u(ordinal)),
        ("relation", t("calls")),
        ("resolution", t("syntactic-callee-name")),
        ("layer", t("semantic")),
        ("producer", t("typescript-semantic")),
        ("producerVersion", t(BUILD)),
        ("schemaVersion", u(1)),
        ("language", t("typescript")),
        ("sourceUniverseId", t(&c.universe_key)),
        ("targetUniverseId", t(&sha('6'))),
        ("confidenceMillionths", u(1_000_000)),
        ("relationSchemaId", t("opensip.relation.calls.v1")),
        (
            "canonicalRelationPayload",
            Value::Bytes(cbor::encode(&m(&[
                ("calleeText", t("g")),
                ("caller", t("f")),
            ]))),
        ),
        ("anchors", a(vec![anchor(c, 0, 10)])),
    ])
}
fn batch_v1(c: &DispatchContext, stage: &str, index: u64, first: u64, n: u64) -> Value {
    let facts: Vec<Value> = (first..first + n).map(|o| candidate(c, o)).collect();
    m(&[
        ("analysisOrdinal", u(0)),
        ("stageId", t(stage)),
        ("batchIndex", u(index)),
        (
            "batchCommitment",
            t(&built_commitment(
                "opensip.ts-provider.fact-batch.v1",
                &a(facts.clone()),
            )),
        ),
        ("facts", a(facts)),
    ])
}
fn entry(key: &RequestedKey, coverage: &str, deficiency: Value) -> Value {
    m(&[
        ("schemaVersion", u(3)),
        (
            "key",
            m(&[
                ("relation", t(&key.relation)),
                ("resolution", t(&key.resolution)),
                (
                    "sourceUniverse",
                    t(suffix(&key.source_universe_id).unwrap()),
                ),
                (
                    "targetUniverse",
                    t(suffix(&key.target_universe_id).unwrap()),
                ),
                ("subjectScopeCommitment", t(&key.subject_scope_commitment)),
            ]),
        ),
        (
            "entry",
            m(&[
                ("relation", t(&key.relation)),
                ("resolution", t(&key.resolution)),
                ("coverage", t(coverage)),
                (
                    "examinedUniverse",
                    m(&[
                        ("subjectScopeCommitment", t(&key.subject_scope_commitment)),
                        ("subjectCount", u(1)),
                    ]),
                ),
                (
                    "resolutionCompleteness",
                    m(&[
                        ("state", t("complete")),
                        ("attempted", Value::Bool(true)),
                        ("examinedExhaustive", Value::Bool(true)),
                        ("stageTerminal", Value::Null),
                        ("unresolvedEdgeCount", u(0)),
                        ("unresolvedEdgeClasses", a(vec![])),
                    ]),
                ),
                (
                    "closedWorld",
                    m(&[
                        ("exportsClosed", t("closed")),
                        ("entryPointsRecognized", t("all")),
                        ("nonliteralLoading", t("none")),
                        ("externalConsumers", t("none-declared")),
                        ("dynamicDispatch", t("resolved")),
                        ("reasons", a(vec![])),
                        ("deadCodeRepairEligible", Value::Bool(false)),
                    ]),
                ),
                ("derivationKinds", a(vec![])),
                ("confidenceMillionths", u(1_000_000)),
                ("deficiency", deficiency),
                ("nativeCause", Value::Null),
            ]),
        ),
    ])
}
fn coverage(c: &DispatchContext, stage: usize) -> Value {
    let entries: Vec<Value> = c.stages[stage]
        .keys
        .iter()
        .map(|k| entry(k, "complete", Value::Null))
        .collect();
    m(&[
        ("analysisOrdinal", u(0)),
        ("stageId", t(&c.stages[stage].expected_stage_id)),
        (
            "coverageCommitment",
            t(&built_commitment(
                "opensip.ts-provider.stage-coverage.v1",
                &a(entries.clone()),
            )),
        ),
        ("entries", a(entries)),
    ])
}
/// Complete over what `facts[i]` and coverage(i) sent, stage by stage.
fn complete(c: &DispatchContext, facts: &[Vec<Value>], batches: &[u64]) -> Value {
    let mut results = Vec::new();
    let (mut all_facts, mut all_cov) = (Vec::new(), Vec::new());
    for (i, s) in c.stages.iter().enumerate() {
        let cov = match get(&coverage(c, i), "entries") {
            Value::Array(e) => e.clone(),
            _ => unreachable!(),
        };
        results.push(m(&[
            ("stageId", t(&s.expected_stage_id)),
            ("stageOrdinal", u(s.stage_ordinal)),
            ("factBatchCount", u(batches[i])),
            ("factCount", u(facts[i].len() as u64)),
            ("coverageEntryCount", u(cov.len() as u64)),
            (
                "factCommitment",
                t(&built_commitment(
                    "opensip.ts-provider.stage-facts.v1",
                    &a(facts[i].clone()),
                )),
            ),
            (
                "coverageCommitment",
                t(&built_commitment(
                    "opensip.ts-provider.stage-coverage.v1",
                    &a(cov.clone()),
                )),
            ),
        ]));
        all_facts.extend(facts[i].clone());
        all_cov.extend(cov);
    }
    m(&[
        ("analysisOrdinal", u(0)),
        ("stageResults", a(results)),
        (
            "factStreamCommitment",
            t(&built_commitment(
                "opensip.ts-provider.fact-stream.v1",
                &a(all_facts),
            )),
        ),
        (
            "coverageStreamCommitment",
            t(&built_commitment(
                "opensip.ts-provider.coverage-stream.v1",
                &a(all_cov),
            )),
        ),
    ])
}
fn terminal_coverage(c: &DispatchContext, deficiency: &str) -> Vec<Value> {
    c.stages
        .iter()
        .flat_map(|s| &s.keys)
        .map(|k| entry(k, "unknown", t(deficiency)))
        .collect()
}

/// One worker frame, written and read back as the reader would.
fn frame(kind: &str, sequence: u64, payload: Value) -> ReceivedFrame {
    let envelope = m(&[
        ("protocolMajor", u(2)),
        ("frameType", t(kind)),
        ("sequence", u(sequence)),
        ("payload", payload),
    ]);
    let bytes = write_frame(&envelope).unwrap();
    read_frame(
        &mut bytes.as_slice(),
        cbor::Profile::Ts2,
        TS2_FRAME_MAX_DEPTH,
        None,
    )
    .unwrap()
    .unwrap()
}

/// A session driven to `phase` with the lawful host and worker frames.
struct Session {
    table: Table,
}
impl Session {
    fn new() -> Self {
        Self {
            table: Table::load(Protocol::Ts2).unwrap(),
        }
    }
    fn receiver(&self, c: DispatchContext) -> Ts2Receiver<'_> {
        Ts2Receiver::new(&self.table, c).unwrap()
    }
}
/// Drive `r` through the startup to READY_ANALYZE; returns the next worker
/// sequence.
fn startup(r: &mut Ts2Receiver<'_>, c: &DispatchContext) -> u64 {
    r.sent(HostFrame::Hello).unwrap();
    r.receive(frame("HelloAck", 0, hello_ack(c))).unwrap();
    r.sent(HostFrame::OpenUniverse).unwrap();
    r.receive(frame("UniverseAccepted", 1, universe_accepted(c)))
        .unwrap();
    r.sent(HostFrame::SnapshotManifest).unwrap();
    r.sent(HostFrame::SnapshotFileChunk).unwrap();
    r.sent(HostFrame::SnapshotSeal).unwrap();
    r.receive(frame("SnapshotAccepted", 2, snapshot_accepted(c)))
        .unwrap();
    r.receive(frame(
        "NativeContextVerified",
        3,
        native_context_verified(c),
    ))
    .unwrap();
    assert_eq!(r.phase(), "READY_ANALYZE");
    4
}
fn analyzing(r: &mut Ts2Receiver<'_>, c: &DispatchContext) -> u64 {
    let seq = startup(r, c);
    r.sent(HostFrame::Analyze).unwrap();
    assert_eq!(r.phase(), "ANALYZING");
    seq
}
fn candidates(v: &Value) -> Vec<Value> {
    match get(v, "facts") {
        Value::Array(f) => f.clone(),
        _ => unreachable!(),
    }
}

/// The lawful session, Hello to DONE: every frame is admitted with its row,
/// and every payload reaches its generated carrier.
#[test]
fn a_lawful_session_is_admitted_end_to_end() {
    let s = Session::new();
    let c = context(&TOKENS);
    let mut r = s.receiver(c.clone());
    let mut seq = analyzing(&mut r, &c);
    let b0 = batch_v1(&c, "stage-one", 0, 0, 2);
    let b1 = batch_v1(&c, "stage-one", 1, 2, 1);
    for b in [&b0, &b1] {
        let got = r.receive(frame("FactBatch", seq, b.clone())).unwrap();
        assert_eq!(got.trace, "T2-12");
        assert!(matches!(got.payload, P::FactBatch0(_)));
        seq += 1;
    }
    let got = r.receive(frame("Coverage", seq, coverage(&c, 0))).unwrap();
    assert_eq!(got.trace, "T2-13");
    seq += 1;
    r.receive(frame("Coverage", seq, coverage(&c, 1))).unwrap();
    seq += 1;
    assert_eq!(r.phase(), "READY_COMPLETE");
    let facts = vec![[candidates(&b0), candidates(&b1)].concat(), Vec::new()];
    let got = r
        .receive(frame("Complete", seq, complete(&c, &facts, &[2, 0])))
        .unwrap();
    assert_eq!(got.trace, "T2-17");
    let P::Complete(done) = got.payload else {
        panic!("Complete")
    };
    assert_eq!(done.stage_results.len(), 2);
    assert_eq!(r.process(ProcessEvent::ZeroExit).unwrap(), "T2-20");
    assert_eq!(r.process(ProcessEvent::Eof).unwrap(), "T2-21");
    assert_eq!(r.phase(), "DONE");
}

/// Step 7: the envelope's major, the frame's direction and the sequence.
#[test]
fn the_envelope_refuses_major_direction_and_sequence() {
    let s = Session::new();
    let c = context(&TOKENS);
    let bad_major = |r: &mut Ts2Receiver<'_>| {
        let envelope = m(&[
            ("protocolMajor", u(1)),
            ("frameType", t("HelloAck")),
            ("sequence", u(0)),
            ("payload", hello_ack(&c)),
        ]);
        let bytes = write_frame(&envelope).unwrap();
        r.receive(
            read_frame(
                &mut bytes.as_slice(),
                cbor::Profile::Ts2,
                TS2_FRAME_MAX_DEPTH,
                None,
            )
            .unwrap()
            .unwrap(),
        )
    };
    let mut r = s.receiver(c.clone());
    r.sent(HostFrame::Hello).unwrap();
    assert!(matches!(bad_major(&mut r), Err(Ts2Refusal::Envelope(_))));
    assert_eq!(
        r.receive(frame("HelloAck", 0, hello_ack(&c))).unwrap_err(),
        Ts2Refusal::AfterRefusal
    );
    for (kind, sequence) in [("Hello", 0), ("HelloAck", 1)] {
        let mut r = s.receiver(c.clone());
        r.sent(HostFrame::Hello).unwrap();
        assert!(
            matches!(
                r.receive(frame(kind, sequence, hello_ack(&c))),
                Err(Ts2Refusal::Envelope(_))
            ),
            "{kind} {sequence}"
        );
    }
    // A duplicate sequence.
    let mut r = s.receiver(c.clone());
    r.sent(HostFrame::Hello).unwrap();
    r.receive(frame("HelloAck", 0, hello_ack(&c))).unwrap();
    r.sent(HostFrame::OpenUniverse).unwrap();
    assert!(matches!(
        r.receive(frame("UniverseAccepted", 0, universe_accepted(&c))),
        Err(Ts2Refusal::Envelope(_))
    ));
}

/// LD-D2B-18 and A2: HelloAck's token array, identity versions, descriptor
/// digests and every descriptor field are exact; each mismatch refuses
/// before OpenUniverse, and the session does not continue.
#[test]
fn the_hello_ack_echo_is_exact() {
    let s = Session::new();
    let mut offered = TOKENS.to_vec();
    offered.push("unresolved-edge-v1");
    let c = context(&offered);
    let mut cases = vec![
        (
            "omitted token",
            with(
                &hello_ack(&c),
                "capabilities",
                a(TOKENS.iter().map(|x| t(x)).collect()),
            ),
        ),
        (
            "added token",
            with(
                &hello_ack(&c),
                "capabilities",
                a([
                    "coverage-v3",
                    "fact-identity-fact2",
                    "plan-identity-plan2",
                    "sealed-vfs-v1",
                    "source-identity-snapshot2",
                    "unresolved-edge-v1",
                ]
                .iter()
                .map(|x| t(x))
                .collect()),
            ),
        ),
        (
            "provider digest",
            with(&hello_ack(&c), "providerDescriptorSha256", t(&h('e'))),
        ),
        (
            "runtime digest",
            with(&hello_ack(&c), "runtimeDescriptorSha256", t(&h('e'))),
        ),
    ];
    for k in c
        .provider_descriptor
        .keys()
        .chain(c.runtime_descriptor.keys())
    {
        if matches!(
            k.as_str(),
            "protocolMajor" | "defaultWorkBudgetProfileId" | "defaultWorkBudgetProfileSha256"
        ) {
            continue; // schema constants: their change refuses at step 8 (below)
        }
        let changed = if k.ends_with("Sha256") || k.ends_with("Root") {
            t(&h('f'))
        } else {
            t("changed")
        };
        cases.push((k.as_str(), with(&hello_ack(&c), k, changed)));
    }
    for (what, ack) in cases {
        let mut r = s.receiver(c.clone());
        r.sent(HostFrame::Hello).unwrap();
        let got = r.receive(frame("HelloAck", 0, ack));
        assert!(
            matches!(got, Err(Ts2Refusal::Admission(_))),
            "{what}: {got:?}"
        );
        assert_eq!(
            r.sent(HostFrame::OpenUniverse),
            Err(Ts2Refusal::AfterRefusal),
            "{what}"
        );
    }
    // A schema constant, and identityVersions' constant members, refuse at step 8.
    for ack in [
        with(&hello_ack(&c), "protocolMajor", u(1)),
        with(
            &hello_ack(&c),
            "identityVersions",
            m(&[
                ("coverage", u(2)),
                ("fact", u(2)),
                ("plan", u(2)),
                ("snapshot", u(2)),
            ]),
        ),
        without(&hello_ack(&c), "platformId"),
    ] {
        let mut r = s.receiver(c.clone());
        r.sent(HostFrame::Hello).unwrap();
        assert!(matches!(
            r.receive(frame("HelloAck", 0, ack)),
            Err(Ts2Refusal::Schema(_))
        ));
    }
    // The identity-negotiated guard follows the admitted array.
    let mut r = s.receiver(c.clone());
    r.sent(HostFrame::Hello).unwrap();
    r.receive(frame("HelloAck", 0, hello_ack(&c))).unwrap();
    assert_eq!(r.sent(HostFrame::OpenUniverse).unwrap(), "T2-03");
}

/// UniverseAccepted, SnapshotAccepted and NativeContextVerified echo
/// OpenUniverse and the Seal member by member.
#[test]
fn the_startup_echoes_are_exact() {
    let s = Session::new();
    let c = context(&TOKENS);
    for k in ["executionId", "snapshotId", "planId", "universeKey"] {
        let mut r = s.receiver(c.clone());
        r.sent(HostFrame::Hello).unwrap();
        r.receive(frame("HelloAck", 0, hello_ack(&c))).unwrap();
        r.sent(HostFrame::OpenUniverse).unwrap();
        let other = match k {
            "executionId" => t("exec1_ffffffffffffffffffffffffffffffff"),
            "snapshotId" => t(&format!("snapshot2:{}", h('e'))),
            "planId" => t(&format!("plan2:{}", h('e'))),
            _ => t(&sha('e')),
        };
        assert!(
            matches!(
                r.receive(frame(
                    "UniverseAccepted",
                    1,
                    with(&universe_accepted(&c), k, other)
                )),
                Err(Ts2Refusal::Admission(_))
            ),
            "{k}"
        );
    }
    let to_seal = |r: &mut Ts2Receiver<'_>| {
        r.sent(HostFrame::Hello).unwrap();
        r.receive(frame("HelloAck", 0, hello_ack(&c))).unwrap();
        r.sent(HostFrame::OpenUniverse).unwrap();
        r.receive(frame("UniverseAccepted", 1, universe_accepted(&c)))
            .unwrap();
        r.sent(HostFrame::SnapshotManifest).unwrap();
        r.sent(HostFrame::SnapshotSeal).unwrap();
    };
    for (k, v) in [
        ("manifestSha256", t(&h('e'))),
        ("entryCount", u(2)),
        ("totalFileBytes", u(99)),
        ("totalChunkCount", u(0)),
        ("snapshotId", t(&format!("snapshot2:{}", h('e')))),
    ] {
        let mut r = s.receiver(c.clone());
        to_seal(&mut r);
        assert!(
            matches!(
                r.receive(frame(
                    "SnapshotAccepted",
                    2,
                    with(&snapshot_accepted(&c), k, v)
                )),
                Err(Ts2Refusal::Admission(_))
            ),
            "{k}"
        );
    }
    for k in ["nativeContextId", "recomputedNativeContextId"] {
        let mut r = s.receiver(c.clone());
        to_seal(&mut r);
        r.receive(frame("SnapshotAccepted", 2, snapshot_accepted(&c)))
            .unwrap();
        assert!(
            matches!(
                r.receive(frame(
                    "NativeContextVerified",
                    3,
                    with(&native_context_verified(&c), k, t(&sha('e')))
                )),
                Err(Ts2Refusal::Admission(_))
            ),
            "{k}"
        );
    }
}

/// Step 9 for FactBatch (DISPATCH-STAGE-CORRELATION): another stage, a
/// duplicate, skipped or decreasing batchIndex, and a wrong first
/// candidateOrdinal each refuse before the table, on a frame that passes
/// its closed schema.
#[test]
fn fact_batch_stage_correlation_and_counters() {
    let s = Session::new();
    let c = context(&TOKENS);
    let cases: Vec<(&str, Vec<Value>)> = vec![
        ("another stage", vec![batch_v1(&c, "stage-two", 0, 0, 1)]),
        (
            "an unrequested stage",
            vec![batch_v1(&c, "stage-nine", 0, 0, 1)],
        ),
        (
            "a skipped batchIndex",
            vec![batch_v1(&c, "stage-one", 1, 0, 1)],
        ),
        (
            "a duplicate batchIndex",
            vec![
                batch_v1(&c, "stage-one", 0, 0, 1),
                batch_v1(&c, "stage-one", 0, 1, 1),
            ],
        ),
        (
            "a decreasing batchIndex",
            vec![
                batch_v1(&c, "stage-one", 0, 0, 1),
                batch_v1(&c, "stage-one", 1, 1, 1),
                batch_v1(&c, "stage-one", 0, 2, 1),
            ],
        ),
        (
            "a wrong first candidateOrdinal",
            vec![batch_v1(&c, "stage-one", 0, 1, 1)],
        ),
        (
            "a repeated candidateOrdinal",
            vec![
                batch_v1(&c, "stage-one", 0, 0, 2),
                batch_v1(&c, "stage-one", 1, 1, 1),
            ],
        ),
    ];
    for (what, batches) in cases {
        let mut r = s.receiver(c.clone());
        let first = analyzing(&mut r, &c);
        let last = batches.len() - 1;
        for (seq, (i, b)) in (first..).zip(batches.into_iter().enumerate()) {
            let got = r.receive(frame("FactBatch", seq, b));
            if i < last {
                got.unwrap();
            } else {
                assert!(
                    matches!(got, Err(Ts2Refusal::Admission(_))),
                    "{what}: {got:?}"
                );
                assert_eq!(r.phase(), "ANALYZING", "{what}: refused before the table");
            }
        }
    }
}

/// Step 8: the carriers' own bounds, before any contextual check.
#[test]
fn schema_bounds_refuse_at_step_8() {
    let s = Session::new();
    let c = context(&TOKENS);
    let empty = with(&batch_v1(&c, "stage-one", 0, 0, 1), "facts", a(vec![]));
    let over = batch_v1(&c, "stage-one", 0, 0, 4097);
    let negative = with(
        &batch_v1(&c, "stage-one", 0, 0, 1),
        "batchIndex",
        Value::Negative(-1),
    );
    let unknown = with(&batch_v1(&c, "stage-one", 0, 0, 1), "extra", u(1));
    for (what, b) in [
        ("0 facts", empty),
        ("4,097 facts", over),
        ("a negative integer", negative),
        ("an unknown member", unknown),
    ] {
        let mut r = s.receiver(c.clone());
        let seq = analyzing(&mut r, &c);
        assert!(
            matches!(
                r.receive(frame("FactBatch", seq, b)),
                Err(Ts2Refusal::Schema(_))
            ),
            "{what}"
        );
    }
}

/// FP-CANDIDATE, RELATION-PAYLOAD-CBOR, ANCHOR-WIRE-SPAN and
/// ANCHOR-FACT-REF-REFUSED, each on a schema-valid candidate.
#[test]
fn the_candidate_law() {
    let s = Session::new();
    let c = context(&TOKENS);
    let base = candidate(&c, 0);
    let fact_ref = m(&[
        ("kind", t("fact-ref")),
        ("snapshotId", Value::Null),
        ("path", Value::Null),
        ("contentSha256", Value::Null),
        ("startByte", Value::Null),
        ("endByte", Value::Null),
        ("factId", t("fact2:x")),
    ]);
    let nested = Value::Bytes(cbor::encode(&m(&[("a", a(vec![u(1)]))])));
    let with_bytes = Value::Bytes(cbor::encode(&m(&[("a", Value::Bytes(vec![1]))])));
    let cases = vec![
        (
            "an unrequested relation",
            with(&base, "relation", t("imports")),
        ),
        (
            "a rung outside the ladder",
            with(&base, "resolution", t("resolved-import")),
        ),
        ("another layer", with(&base, "layer", t("syntax"))),
        (
            "another producerVersion",
            with(&base, "producerVersion", t("other")),
        ),
        ("another schemaVersion", with(&base, "schemaVersion", u(2))),
        (
            "another relationSchemaId",
            with(&base, "relationSchemaId", t("opensip.relation.imports.v1")),
        ),
        (
            "another source universe",
            with(&base, "sourceUniverseId", t(&sha('e'))),
        ),
        (
            "a target outside the domain",
            with(&base, "targetUniverseId", t(&sha('e'))),
        ),
        (
            "a payload past its depth bound",
            with(&base, "canonicalRelationPayload", nested),
        ),
        (
            "a payload holding bytes",
            with(&base, "canonicalRelationPayload", with_bytes),
        ),
        (
            "a non-canonical payload",
            with(
                &base,
                "canonicalRelationPayload",
                Value::Bytes(vec![0x18, 0x01]),
            ),
        ),
        (
            "a fact-ref anchor",
            with(&base, "anchors", a(vec![fact_ref])),
        ),
        (
            "an anchor outside the manifest",
            with(
                &base,
                "anchors",
                a(vec![with(&anchor(&c, 0, 10), "path", t("src/b.ts"))]),
            ),
        ),
        (
            "an anchor digest",
            with(
                &base,
                "anchors",
                a(vec![with(&anchor(&c, 0, 10), "contentSha256", t(&h('e')))]),
            ),
        ),
        (
            "an anchor snapshot",
            with(
                &base,
                "anchors",
                a(vec![with(
                    &anchor(&c, 0, 10),
                    "snapshotId",
                    t(&format!("snapshot2:{}", h('e'))),
                )]),
            ),
        ),
        (
            "an empty span",
            with(&base, "anchors", a(vec![anchor(&c, 5, 5)])),
        ),
        (
            "a span past the file",
            with(&base, "anchors", a(vec![anchor(&c, 0, 101)])),
        ),
    ];
    for (what, cand) in cases {
        let mut r = s.receiver(c.clone());
        let seq = analyzing(&mut r, &c);
        let b = batch_v1(&c, "stage-one", 0, 0, 1);
        let b = with(
            &with(&b, "facts", a(vec![cand.clone()])),
            "batchCommitment",
            t(&built_commitment(
                "opensip.ts-provider.fact-batch.v1",
                &a(vec![cand]),
            )),
        );
        let got = r.receive(frame("FactBatch", seq, b));
        assert!(
            matches!(got, Err(Ts2Refusal::Admission(_) | Ts2Refusal::Schema(_))),
            "{what}: {got:?}"
        );
    }
    // The anchors' cbor-bytes-strict order is the carrier's (step 8).
    let mut r = s.receiver(c.clone());
    let seq = analyzing(&mut r, &c);
    let two = with(
        &base,
        "anchors",
        a(vec![anchor(&c, 2, 9), anchor(&c, 1, 9)]),
    );
    let b = with(
        &with(
            &batch_v1(&c, "stage-one", 0, 0, 1),
            "facts",
            a(vec![two.clone()]),
        ),
        "batchCommitment",
        t(&built_commitment(
            "opensip.ts-provider.fact-batch.v1",
            &a(vec![two]),
        )),
    );
    assert!(matches!(
        r.receive(frame("FactBatch", seq, b)),
        Err(Ts2Refusal::Schema(_))
    ));
}

/// COMMIT-MAP and COMMIT-TS2-FACT-BATCH: each commitment is recomputed over
/// the received bytes under exactly its row's domain; a swapped domain, a
/// swapped value class and a reordered preimage each refuse.
#[test]
fn commitments_are_recomputed_over_received_bytes() {
    let s = Session::new();
    let c = context(&TOKENS);
    let b = batch_v1(&c, "stage-one", 0, 0, 2);
    let facts = candidates(&b);
    let swapped_domain = with(
        &b,
        "batchCommitment",
        t(&built_commitment(
            "opensip.ts-provider.stage-facts.v1",
            &a(facts.clone()),
        )),
    );
    let reordered = with(
        &b,
        "batchCommitment",
        t(&built_commitment(
            "opensip.ts-provider.fact-batch.v1",
            &a(vec![facts[1].clone(), facts[0].clone()]),
        )),
    );
    for (what, bad) in [
        ("a swapped domain", swapped_domain),
        ("a reordered preimage", reordered),
    ] {
        let mut r = s.receiver(c.clone());
        let seq = analyzing(&mut r, &c);
        assert!(
            matches!(
                r.receive(frame("FactBatch", seq, bad)),
                Err(Ts2Refusal::Admission(_))
            ),
            "{what}"
        );
    }
    // A coverage commitment under the fact class's domain.
    let mut r = s.receiver(c.clone());
    let seq = analyzing(&mut r, &c);
    let cov = coverage(&c, 0);
    let entries = match get(&cov, "entries") {
        Value::Array(e) => e.clone(),
        _ => unreachable!(),
    };
    let bad = with(
        &cov,
        "coverageCommitment",
        t(&built_commitment(
            "opensip.ts-provider.stage-facts.v1",
            &a(entries),
        )),
    );
    assert!(matches!(
        r.receive(frame("Coverage", seq, bad)),
        Err(Ts2Refusal::Admission(_))
    ));
    // Complete: each of the four commitments, swapped for another row's.
    for (k, domain) in [
        ("factStreamCommitment", "opensip.ts-provider.stage-facts.v1"),
        (
            "coverageStreamCommitment",
            "opensip.ts-provider.stage-coverage.v1",
        ),
    ] {
        let mut r = s.receiver(c.clone());
        let mut seq = analyzing(&mut r, &c);
        r.receive(frame("FactBatch", seq, b.clone())).unwrap();
        seq += 1;
        r.receive(frame("Coverage", seq, coverage(&c, 0))).unwrap();
        r.receive(frame("Coverage", seq + 1, coverage(&c, 1)))
            .unwrap();
        let done = complete(&c, &[facts.clone(), Vec::new()], &[1, 0]);
        let preimage = if k == "factStreamCommitment" {
            a(facts.clone())
        } else {
            a(vec![])
        };
        let bad = with(&done, k, t(&built_commitment(domain, &preimage)));
        assert!(
            matches!(
                r.receive(frame("Complete", seq + 2, bad)),
                Err(Ts2Refusal::Admission(_))
            ),
            "{k}"
        );
    }
    // A stage result's count not as observed.
    let mut r = s.receiver(c.clone());
    let mut seq = analyzing(&mut r, &c);
    r.receive(frame("Coverage", seq, coverage(&c, 0))).unwrap();
    seq += 1;
    r.receive(frame("Coverage", seq, coverage(&c, 1))).unwrap();
    let done = complete(&c, &[Vec::new(), Vec::new()], &[1, 0]);
    assert!(matches!(
        r.receive(frame("Complete", seq + 1, done)),
        Err(Ts2Refusal::Admission(_))
    ));
}

/// LD-D2B-3 item 5: every commitment's preimage parts are slices of a
/// received payload, never a re-encoding.
#[test]
fn every_commitment_preimage_is_a_received_slice() {
    PROVENANCE.with_borrow_mut(Vec::clear);
    let s = Session::new();
    let c = context(&TOKENS);
    let mut r = s.receiver(c.clone());
    let mut seq = analyzing(&mut r, &c);
    let b = batch_v1(&c, "stage-one", 0, 0, 2);
    r.receive(frame("FactBatch", seq, b.clone())).unwrap();
    seq += 1;
    r.receive(frame("Coverage", seq, coverage(&c, 0))).unwrap();
    r.receive(frame("Coverage", seq + 1, coverage(&c, 1)))
        .unwrap();
    r.receive(frame(
        "Complete",
        seq + 2,
        complete(&c, &[candidates(&b), Vec::new()], &[1, 0]),
    ))
    .unwrap();
    let ranges: Vec<(usize, usize)> = r
        .retained
        .iter()
        .map(|f| (f.payload().as_ptr() as usize, f.payload().len()))
        .collect();
    let log = PROVENANCE.with_borrow(Clone::clone);
    // One batch, two coverage frames, and Complete's four per stage-pair
    // commitments plus its two streams.
    assert_eq!(log.len(), 1 + 2 + 2 * 2 + 2, "{log:?}");
    for (domain, parts) in &log {
        for (at, len) in parts {
            assert!(
                ranges.iter().any(|(p, n)| *at >= *p && at + len <= p + n),
                "{domain}: a part outside every received payload"
            );
        }
    }
}

/// PER-KEY-SCOPE2 and UNIVERSE-NATIVE-IDENTITY: each entry echoes its key.
#[test]
fn coverage_entries_echo_their_keys() {
    let s = Session::new();
    let c = context(&TOKENS);
    let key = &c.stages[0].keys[0];
    let changed = |path: &[&str], v: Value| {
        let e = entry(key, "complete", Value::Null);
        let e = match path {
            [k] => with(&e, k, v),
            [outer, k] => with(&e, outer, with(get(&e, outer), k, v)),
            [outer, mid, k] => with(
                &e,
                outer,
                with(get(&e, outer), mid, with(get(get(&e, outer), mid), k, v)),
            ),
            _ => unreachable!(),
        };
        let entries = vec![e];
        m(&[
            ("analysisOrdinal", u(0)),
            ("stageId", t("stage-one")),
            (
                "coverageCommitment",
                t(&built_commitment(
                    "opensip.ts-provider.stage-coverage.v1",
                    &a(entries.clone()),
                )),
            ),
            ("entries", a(entries)),
        ])
    };
    let cases = vec![
        ("key relation", changed(&["key", "relation"], t("imports"))),
        (
            "key resolution",
            changed(&["key", "resolution"], t("resolved-callee")),
        ),
        (
            "key scope",
            changed(&["key", "subjectScopeCommitment"], t(&sha('e'))),
        ),
        (
            "key source suffix",
            changed(&["key", "sourceUniverse"], t(&h('e'))),
        ),
        (
            "key target suffix",
            changed(&["key", "targetUniverse"], t(&h('e'))),
        ),
        (
            "examined scope",
            changed(
                &["entry", "examinedUniverse", "subjectScopeCommitment"],
                t(&sha('e')),
            ),
        ),
        (
            "another stage",
            with(&coverage(&c, 1), "stageId", t("stage-two")),
        ),
    ];
    for (what, cov) in cases {
        let mut r = s.receiver(c.clone());
        let seq = analyzing(&mut r, &c);
        assert!(
            matches!(
                r.receive(frame("Coverage", seq, cov)),
                Err(Ts2Refusal::Admission(_))
            ),
            "{what}"
        );
    }
}

/// The terminals: pre-Analyze Unavailable in WAIT_NATIVE_CONTEXT_VERIFIED,
/// post-Analyze Unavailable before any output, BudgetExhausted's budget
/// join, each with stage-major coverage under the coverage-stream domain.
#[test]
fn the_terminals() {
    let s = Session::new();
    let c = context(&TOKENS);
    let pre = m(&[
        ("executionId", t(EXEC)),
        ("snapshotId", t(&c.snapshot_id)),
        ("planId", t(&c.plan_id)),
        ("reason", t("native-context-mismatch")),
        ("nativeContextId", t(&c.native_context_id)),
        ("recomputedNativeContextId", t(&sha('e'))),
    ]);
    let to_ncv = |r: &mut Ts2Receiver<'_>| {
        r.sent(HostFrame::Hello).unwrap();
        r.receive(frame("HelloAck", 0, hello_ack(&c))).unwrap();
        r.sent(HostFrame::OpenUniverse).unwrap();
        r.receive(frame("UniverseAccepted", 1, universe_accepted(&c)))
            .unwrap();
        r.sent(HostFrame::SnapshotManifest).unwrap();
        r.sent(HostFrame::SnapshotSeal).unwrap();
        r.receive(frame("SnapshotAccepted", 2, snapshot_accepted(&c)))
            .unwrap();
    };
    let mut r = s.receiver(c.clone());
    to_ncv(&mut r);
    let got = r.receive(frame("Unavailable", 3, pre.clone())).unwrap();
    assert_eq!(got.trace, "T2-10");
    assert!(matches!(got.payload, P::Unavailable0(_)));
    let mut r = s.receiver(c.clone());
    to_ncv(&mut r);
    assert!(matches!(
        r.receive(frame(
            "Unavailable",
            3,
            with(&pre, "recomputedNativeContextId", t(&c.native_context_id))
        )),
        Err(Ts2Refusal::Admission(_))
    ));
    // The pre-Analyze payload in READY_ANALYZE has no selection: the table refuses.
    let mut r = s.receiver(c.clone());
    let seq = startup(&mut r, &c);
    assert!(matches!(
        r.receive(frame("Unavailable", seq, pre.clone())),
        Err(Ts2Refusal::Table(_))
    ));

    let cov = terminal_coverage(&c, "provider-unavailable");
    let post = |cov: Vec<Value>, domain: &str| {
        m(&[
            ("analysisOrdinal", u(0)),
            ("affectedStageIds", a(vec![t("stage-one"), t("stage-two")])),
            ("reason", t("semantic-universe-incomplete")),
            (
                "coverageCommitment",
                t(&built_commitment(domain, &a(cov.clone()))),
            ),
            ("coverage", a(cov)),
        ])
    };
    let mut r = s.receiver(c.clone());
    let seq = analyzing(&mut r, &c);
    let got = r
        .receive(frame(
            "Unavailable",
            seq,
            post(cov.clone(), "opensip.ts-provider.coverage-stream.v1"),
        ))
        .unwrap();
    assert_eq!(got.trace, "T2-14");
    for (what, bad) in [
        (
            "the stage domain",
            post(cov.clone(), "opensip.ts-provider.stage-coverage.v1"),
        ),
        (
            "another deficiency",
            post(
                terminal_coverage(&c, "budget-exhausted"),
                "opensip.ts-provider.coverage-stream.v1",
            ),
        ),
        (
            "one stage only",
            post(cov[..1].to_vec(), "opensip.ts-provider.coverage-stream.v1"),
        ),
        (
            "affected stages",
            with(
                &post(cov.clone(), "opensip.ts-provider.coverage-stream.v1"),
                "affectedStageIds",
                a(vec![t("stage-one")]),
            ),
        ),
    ] {
        let mut r = s.receiver(c.clone());
        let seq = analyzing(&mut r, &c);
        assert!(
            matches!(
                r.receive(frame("Unavailable", seq, bad)),
                Err(Ts2Refusal::Admission(_))
            ),
            "{what}"
        );
    }

    // LD-D2B3-2: every item of a piecewise-admitted array is admitted by its
    // own schema, not only the first.
    let mut items = cov.clone();
    items[1] = with(&items[1], "schemaVersion", u(4));
    let mut r = s.receiver(c.clone());
    let seq = analyzing(&mut r, &c);
    assert!(matches!(
        r.receive(frame(
            "Unavailable",
            seq,
            post(items, "opensip.ts-provider.coverage-stream.v1")
        )),
        Err(Ts2Refusal::Schema(_))
    ));

    let spent = terminal_coverage(&c, "budget-exhausted");
    let budget = |trigger: &str, limit: u64, observed: u64| {
        m(&[
            ("analysisOrdinal", u(0)),
            ("triggerStageId", t(trigger)),
            ("dimension", t("typeQueries")),
            ("limit", u(limit)),
            ("observed", u(observed)),
            (
                "coverageCommitment",
                t(&built_commitment(
                    "opensip.ts-provider.coverage-stream.v1",
                    &a(spent.clone()),
                )),
            ),
            ("coverage", a(spent.clone())),
        ])
    };
    let mut r = s.receiver(c.clone());
    let seq = analyzing(&mut r, &c);
    assert_eq!(
        r.receive(frame("BudgetExhausted", seq, budget("stage-two", 100, 101)))
            .unwrap()
            .trace,
        "T2-15"
    );
    for (what, bad) in [
        ("an unrequested stage", budget("stage-nine", 100, 101)),
        ("another limit", budget("stage-one", 99, 100)),
        ("observed not limit + 1", budget("stage-one", 100, 102)),
    ] {
        let mut r = s.receiver(c.clone());
        let seq = analyzing(&mut r, &c);
        assert!(
            matches!(
                r.receive(frame("BudgetExhausted", seq, bad)),
                Err(Ts2Refusal::Admission(_))
            ),
            "{what}"
        );
    }
}

/// CANCELLED-ECHO and TS2-OBSERVED-PHASE.
#[test]
fn cancelled_echoes_the_cancel() {
    let s = Session::new();
    let c = context(&TOKENS);
    let cancelled = |phase: &str, execution: Value| {
        m(&[
            ("executionId", execution),
            ("analysisOrdinal", Value::Null),
            ("observedPhase", t(phase)),
        ])
    };
    let in_ncv = |r: &mut Ts2Receiver<'_>| {
        r.sent(HostFrame::Hello).unwrap();
        r.receive(frame("HelloAck", 0, hello_ack(&c))).unwrap();
        r.sent(HostFrame::OpenUniverse).unwrap();
        r.receive(frame("UniverseAccepted", 1, universe_accepted(&c)))
            .unwrap();
        r.sent(HostFrame::SnapshotManifest).unwrap();
        r.sent(HostFrame::SnapshotSeal).unwrap();
        r.receive(frame("SnapshotAccepted", 2, snapshot_accepted(&c)))
            .unwrap();
        r.sent(HostFrame::Cancel {
            execution_id: Some(EXEC.to_owned()),
            analysis_ordinal: None,
        })
        .unwrap();
    };
    let mut r = s.receiver(c.clone());
    in_ncv(&mut r);
    assert_eq!(
        r.receive(frame("Cancelled", 3, cancelled("snapshot", t(EXEC))))
            .unwrap()
            .trace,
        "T2-19"
    );
    for (what, bad) in [
        ("another phase", cancelled("analysis", t(EXEC))),
        ("another execution", cancelled("snapshot", Value::Null)),
    ] {
        let mut r = s.receiver(c.clone());
        in_ncv(&mut r);
        assert!(
            matches!(
                r.receive(frame("Cancelled", 3, bad)),
                Err(Ts2Refusal::Admission(_))
            ),
            "{what}"
        );
    }
}

/// OCCUPANCY-JOIN, under target-attribution-v2 (FactBatchV3).
#[test]
fn fact_batch_v3_joins_its_companions() {
    let s = Session::new();
    let mut tokens = TOKENS.to_vec();
    tokens.push("target-attribution-v2");
    tokens.sort();
    let c = context(&tokens);
    let companion = |ordinal: u64, target: &str| {
        m(&[
            ("schemaVersion", u(1)),
            ("candidateOrdinal", u(ordinal)),
            ("targetUniverseId", t(target)),
            ("targetNativeId", t("ts:f")),
            ("kind", t("file")),
            ("occupancy", t("external")),
            ("exported", Value::Null),
            ("logicalPath", Value::Null),
            ("packageManifestPath", Value::Null),
            ("evaluationNativeId", Value::Null),
        ])
    };
    let v3 = |companions: Vec<Value>| {
        m(&[
            ("schemaVersion", u(3)),
            ("analysisOrdinal", u(0)),
            ("stageId", t("stage-one")),
            ("batchIndex", u(0)),
            ("candidates", a(vec![candidate(&c, 0)])),
            ("occupancyCompanions", a(companions)),
        ])
    };
    let mut r = s.receiver(c.clone());
    let seq = analyzing(&mut r, &c);
    let got = r
        .receive(frame("FactBatch", seq, v3(vec![companion(0, &sha('6'))])))
        .unwrap();
    assert!(matches!(got.payload, P::FactBatch1(_)));
    for (what, bad) in [
        (
            "more companions than candidates",
            v3(vec![companion(0, &sha('6')), companion(0, &sha('6'))]),
        ),
        (
            "a companion of no candidate",
            v3(vec![companion(1, &sha('6'))]),
        ),
        ("another target", v3(vec![companion(0, &sha('e'))])),
    ] {
        let mut r = s.receiver(c.clone());
        let seq = analyzing(&mut r, &c);
        assert!(
            matches!(
                r.receive(frame("FactBatch", seq, bad)),
                Err(Ts2Refusal::Admission(_) | Ts2Refusal::Schema(_))
            ),
            "{what}"
        );
    }
}

/// A negotiated FA-2 context constructs; an owed census without its token,
/// or descriptor fields other than A2's, refuses before reading a frame.
#[test]
fn the_context_is_checked_at_construction() {
    let s = Session::new();
    let mut tokens = TOKENS.to_vec();
    tokens.push("symbol-census-v1");
    assert!(Ts2Receiver::new(&s.table, context(&tokens)).is_ok());
    let mut without_token = context(&TOKENS);
    without_token.symbol_census = Some(sha('a'));
    assert!(matches!(
        Ts2Receiver::new(&s.table, without_token),
        Err(Ts2Refusal::Context(_))
    ));
    let mut c = context(&TOKENS);
    c.runtime_descriptor.remove("platformId");
    assert!(matches!(
        Ts2Receiver::new(&s.table, c),
        Err(Ts2Refusal::Context(_))
    ));
    let rust = Table::load(Protocol::Rust3).unwrap();
    assert!(matches!(
        Ts2Receiver::new(&rust, context(&TOKENS)),
        Err(Ts2Refusal::Context(_))
    ));
}

/// The carrier interpreter fails closed: a form, order, pattern or lexical
/// rule it does not implement refuses to load.
#[test]
fn the_carrier_interpreter_fails_closed() {
    assert!(Carriers::load("Ts2").is_ok());
    let c = Carriers::load("Ts2").unwrap();
    let ty = |s: &str| parse_json(s.as_bytes()).unwrap();
    for bad in [
        r#"{"t":"text","pattern":"^[a-z]+$"}"#,
        r#"{"t":"array","items":{"t":"uint64"},"order":"newest-first"}"#,
        r#"{"t":"float"}"#,
        r#"{"t":"uint64","min":"1"}"#,
    ] {
        assert!(c.validate_type("test", &ty(bad)).is_err(), "{bad}");
    }
}

// The depth bounds (LD-D2B-2), recomputed: containers count, scalars do not;
// a `$ref` is followed across the embedded documents; `oneOf`/`anyOf`/
// `allOf` and `if`/`then`/`else`/`not` take their deepest branch.
fn documents() -> BTreeMap<String, J> {
    crate::schema_sources::sources()
        .iter()
        .map(|raw| {
            let d = parse_json(raw).unwrap();
            (
                txt(obj(&d).unwrap().get("$id").unwrap())
                    .unwrap()
                    .to_owned(),
                d,
            )
        })
        .collect()
}
fn resolve<'d>(docs: &'d BTreeMap<String, J>, r: &str, current: &str) -> (&'d J, String) {
    let (base, pointer) = r.split_once('#').unwrap();
    let id = if base.is_empty() { current } else { base };
    let node = pointer
        .split('/')
        .filter(|p| !p.is_empty())
        .fold(&docs[id], |n, p| {
            obj(n)
                .unwrap()
                .get(&p.replace("~1", "/").replace("~0", "~"))
                .unwrap()
        });
    (node, id.to_owned())
}
fn value_depth(v: &J) -> usize {
    match v {
        J::Object(o) => 1 + o.values().map(value_depth).max().unwrap_or(0),
        J::Array(a) => 1 + a.iter().map(value_depth).max().unwrap_or(0),
        _ => 0,
    }
}
fn schema_depth(
    docs: &BTreeMap<String, J>,
    s: &J,
    current: &str,
    seen: &BTreeSet<String>,
) -> usize {
    let Some(s) = obj(s) else { return 0 };
    let mut best = 0;
    if let Some(r) = s.get("$ref").and_then(txt) {
        let key = if r.starts_with('#') {
            format!("{current}{r}")
        } else {
            r.to_owned()
        };
        assert!(
            !seen.contains(&key),
            "a recursive schema has no depth bound: {key}"
        );
        let (node, id) = resolve(docs, r, current);
        let mut seen = seen.clone();
        seen.insert(key);
        best = schema_depth(docs, node, &id, &seen);
    }
    for k in ["oneOf", "anyOf", "allOf"] {
        if let Some(J::Array(xs)) = s.get(k) {
            best = best.max(
                xs.iter()
                    .map(|x| schema_depth(docs, x, current, seen))
                    .max()
                    .unwrap_or(0),
            );
        }
    }
    for k in ["if", "then", "else", "not"] {
        if let Some(x) = s.get(k) {
            best = best.max(schema_depth(docs, x, current, seen));
        }
    }
    let types: Vec<&str> = match s.get("type") {
        Some(J::String(t)) => vec![t],
        Some(J::Array(ts)) => ts.iter().filter_map(txt).collect(),
        _ => vec![],
    };
    let mut container = false;
    let mut inner = 0;
    if s.contains_key("properties")
        || types.contains(&"object")
        || s.contains_key("additionalProperties")
        || s.contains_key("patternProperties")
    {
        container = true;
        for k in ["properties", "patternProperties"] {
            if let Some(J::Object(ps)) = s.get(k) {
                inner = inner.max(
                    ps.values()
                        .map(|x| schema_depth(docs, x, current, seen))
                        .max()
                        .unwrap_or(0),
                );
            }
        }
        if let Some(x @ J::Object(_)) = s.get("additionalProperties") {
            inner = inner.max(schema_depth(docs, x, current, seen));
        }
    }
    if s.contains_key("items") || types.contains(&"array") || s.contains_key("prefixItems") {
        container = true;
        if let Some(x @ J::Object(_)) = s.get("items") {
            inner = inner.max(schema_depth(docs, x, current, seen));
        }
        if let Some(J::Array(xs)) = s.get("prefixItems") {
            inner = inner.max(
                xs.iter()
                    .map(|x| schema_depth(docs, x, current, seen))
                    .max()
                    .unwrap_or(0),
            );
        }
    }
    let literals: Vec<&J> = s
        .get("const")
        .into_iter()
        .chain(match s.get("enum") {
            Some(J::Array(e)) => e.iter().collect(),
            _ => vec![],
        })
        .collect();
    for l in literals {
        if matches!(l, J::Object(_) | J::Array(_)) {
            container = true;
            inner = inner.max(value_depth(l) - 1);
        }
    }
    best.max(if container { 1 + inner } else { 0 })
}
fn carrier_depth(
    docs: &BTreeMap<String, J>,
    carriers: &BTreeMap<String, J>,
    ty: &J,
    seen: &BTreeSet<String>,
) -> usize {
    let t = obj(ty).unwrap();
    let records = obj(carriers.get("records").unwrap()).unwrap();
    let scalars = obj(carriers.get("scalars").unwrap()).unwrap();
    match txt(t.get("t").unwrap()).unwrap() {
        "uint64" | "text" | "bytes" | "null" => 0,
        "nullable" => carrier_depth(docs, carriers, t.get("of").unwrap(), seen),
        "array" => 1 + carrier_depth(docs, carriers, t.get("items").unwrap(), seen),
        "ref" => {
            let name = txt(t.get("ref").unwrap()).unwrap();
            if let Some(s) = scalars.get(name) {
                return carrier_depth(docs, carriers, obj(s).unwrap().get("type").unwrap(), seen);
            }
            assert!(!seen.contains(name));
            let mut seen = seen.clone();
            seen.insert(name.to_owned());
            let r = obj(records.get(name).unwrap()).unwrap();
            let types: Vec<&J> = match txt(r.get("kind").unwrap()).unwrap() {
                "record" => match r.get("members").unwrap() {
                    J::Array(ms) => ms
                        .iter()
                        .map(|m| obj(m).unwrap().get("type").unwrap())
                        .collect(),
                    _ => unreachable!(),
                },
                _ => obj(r.get("variants").unwrap())
                    .unwrap()
                    .values()
                    .flat_map(|v| obj(v).unwrap().values())
                    .collect(),
            };
            1 + types
                .into_iter()
                .map(|x| carrier_depth(docs, carriers, x, &seen))
                .max()
                .unwrap_or(0)
        }
        "extern" => {
            let (node, id) = resolve(docs, txt(t.get("schemaRef").unwrap()).unwrap(), "");
            schema_depth(docs, node, &id, &BTreeSet::new())
        }
        "frame-payload" => {
            let protocol = txt(t.get("protocol").unwrap()).unwrap();
            let frames = path(carriers.get("protocols").unwrap(), &[protocol, "frames"]).unwrap();
            let J::Array(frames) = frames else {
                unreachable!()
            };
            frames
                .iter()
                .flat_map(|f| {
                    let p = obj(f).unwrap().get("payload").unwrap();
                    match obj(p).unwrap().get("alternatives") {
                        Some(J::Object(alts)) => alts.values().collect::<Vec<_>>(),
                        _ => vec![p],
                    }
                })
                .map(|p| carrier_depth(docs, carriers, p, seen))
                .max()
                .unwrap_or(0)
        }
        other => panic!("form {other}"),
    }
}

#[test]
fn the_depth_bounds_are_recomputed_from_the_documents() {
    let docs = documents();
    let carriers = parse_json(carrier::CARRIERS).unwrap();
    let carriers = obj(&carriers).unwrap();
    let envelope = parse_json(br#"{"t":"ref","ref":"Ts2FrameV2"}"#).unwrap();
    assert_eq!(
        carrier_depth(&docs, carriers, &envelope, &BTreeSet::new()),
        TS2_FRAME_MAX_DEPTH
    );
    let id = "opensip.product.relation-payload.2";
    let rel = obj(docs[id].get_defs()).unwrap();
    let deepest = rel
        .values()
        .map(|s| schema_depth(&docs, s, id, &BTreeSet::new()))
        .max()
        .unwrap();
    assert_eq!(deepest, RELATION_PAYLOAD_MAX_DEPTH);
    // The deepest lawful frame (D2b-3a r1 NBO-2): a Coverage frame whose
    // `entries[i].entry.resolutionCompleteness.unresolvedEdgeClasses` array
    // is the seventh container, admitted at the bound by the reader and in a
    // session by the receiver. One level more, an array inside that array,
    // refuses at the reader.
    let s = Session::new();
    let c = context(&TOKENS);
    let mut r = s.receiver(c.clone());
    let seq = analyzing(&mut r, &c);
    let witness = coverage(&c, 0);
    let envelope = |payload: Value| {
        m(&[
            ("protocolMajor", u(2)),
            ("frameType", t("Coverage")),
            ("sequence", u(seq)),
            ("payload", payload),
        ])
    };
    assert_eq!(cbor_depth(&envelope(witness.clone())), TS2_FRAME_MAX_DEPTH);
    let bytes = write_frame(&envelope(witness.clone())).unwrap();
    let read = read_frame(
        &mut bytes.as_slice(),
        cbor::Profile::Ts2,
        TS2_FRAME_MAX_DEPTH,
        None,
    )
    .unwrap()
    .unwrap();
    assert_eq!(r.receive(read).unwrap().trace, "T2-13");
    let deeper = {
        let Value::Array(entries) = get(&witness, "entries") else {
            unreachable!()
        };
        let e = &entries[0];
        let inner = get(e, "entry");
        let rc = get(inner, "resolutionCompleteness");
        let rc = with(rc, "unresolvedEdgeClasses", a(vec![a(vec![])]));
        let inner = with(inner, "resolutionCompleteness", rc);
        with(&witness, "entries", a(vec![with(e, "entry", inner)]))
    };
    assert_eq!(
        cbor_depth(&envelope(deeper.clone())),
        TS2_FRAME_MAX_DEPTH + 1
    );
    let bytes = write_frame(&envelope(deeper)).unwrap();
    assert!(matches!(
        read_frame(
            &mut bytes.as_slice(),
            cbor::Profile::Ts2,
            TS2_FRAME_MAX_DEPTH,
            None
        ),
        Err(super::super::FrameRefusal::Cbor(cbor::CborRefusal::Depth))
    ));
}

/// A value's container depth: arrays and maps count, scalars do not
/// (LD-D2B-2).
fn cbor_depth(v: &Value) -> usize {
    match v {
        Value::Array(items) => 1 + items.iter().map(cbor_depth).max().unwrap_or(0),
        Value::Map(members) => {
            1 + members
                .iter()
                .map(|(_, x)| cbor_depth(x))
                .max()
                .unwrap_or(0)
        }
        _ => 0,
    }
}

trait Defs {
    fn get_defs(&self) -> &J;
}
impl Defs for J {
    fn get_defs(&self) -> &J {
        obj(self).unwrap().get("$defs").unwrap()
    }
}

#[path = "ts2_send_tests.rs"]
mod send;
