//! Synthetic codec-context controls only; no source/toolchain, Plan, H,
//! whole-host or release qualification is claimed by these fixtures.
use super::super::super::{ProcessEvent, write_frame};
use super::*;
fn t(s: &str) -> Value {
    Value::Text(s.to_owned())
}
fn u(n: u64) -> Value {
    Value::Unsigned(n)
}
fn a(xs: Vec<Value>) -> Value {
    Value::Array(xs)
}
fn m(xs: &[(&str, Value)]) -> Value {
    Value::Map(
        xs.iter()
            .map(|(k, v)| ((*k).to_owned(), v.clone()))
            .collect(),
    )
}
fn get<'a>(v: &'a Value, key: &str) -> &'a Value {
    field(map_of(v).unwrap(), key).unwrap()
}
fn with(v: &Value, key: &str, new: Value) -> Value {
    let Value::Map(fields) = v else { panic!("map") };
    let mut fields = fields.clone();
    if let Some((_, v)) = fields.iter_mut().find(|(k, _)| k == key) {
        *v = new
    } else {
        fields.push((key.to_owned(), new))
    };
    Value::Map(fields)
}
fn h(c: char) -> String {
    c.to_string().repeat(64)
}
fn sha(c: char) -> String {
    format!("sha256:{}", h(c))
}
fn wire(j: &J) -> Value {
    match j {
        J::Null => Value::Null,
        J::Bool(x) => Value::Bool(*x),
        J::Integer(x) => u(u64::try_from(x.get()).unwrap()),
        J::String(s) => t(s),
        J::Array(xs) => a(xs.iter().map(wire).collect()),
        J::Object(xs) => Value::Map(xs.iter().map(|(k, v)| (k.clone(), wire(v))).collect()),
    }
}
fn fixture() -> Value {
    let d = parse_json(include_bytes!(
        "../../../tests/data/rust3-startup-shape.v1.json"
    ))
    .unwrap();
    wire(path(&d, &["universeAccepted"]).unwrap())
}
fn snapshot() -> String {
    let v = fixture();
    text_of(map_of(&v).unwrap(), "snapshotId")
        .unwrap()
        .to_owned()
}
const TOKENS: [&str; 4] = [
    "coverage-v3",
    "fact-identity-fact2",
    "plan-identity-plan2",
    "source-identity-snapshot2",
];
struct Key {
    relation: String,
    resolution: String,
    source_universe_id: String,
    target_universe_id: String,
    subject_scope_commitment: String,
}
fn key(index: usize) -> Key {
    Key {
        relation: "calls".to_owned(),
        resolution: "syntactic-callee-name".to_owned(),
        source_universe_id: sha('5'),
        target_universe_id: sha('6'),
        subject_scope_commitment: sha(if index == 0 { 'c' } else { 'd' }),
    }
}
fn context(target: bool) -> Rust3DispatchContext {
    let accepted = fixture();
    let universe = get(&accepted, "universe");
    let inputs = get(universe, "resolvedInputs");
    let identity = m(&[
        ("protocolMajor", u(3)),
        ("providerBuildId", t("provider")),
        ("rustCommitHash", t(&"a".repeat(40))),
        ("sysrootDigest", t(&h('a'))),
        ("hostTriple", t("aarch64-apple-darwin")),
        ("targetTriple", t("aarch64-apple-darwin")),
    ]);
    let hs = parse_json(include_bytes!(
        "../../../../../schemas/sources/handshake-v1.schema.json"
    ))
    .unwrap();
    let properties = obj(path(&hs, &["$defs", "ProtocolLimitsV3", "properties"]).unwrap()).unwrap();
    let limits = Value::Map(
        properties
            .iter()
            .map(|(key, v)| (key.clone(), wire(path(v, &["const"]).unwrap())))
            .collect(),
    );
    let mut tokens = TOKENS.iter().map(|x| t(x)).collect::<Vec<_>>();
    if target {
        tokens.push(t("target-attribution-v2"));
    }
    let hello = m(&[
        ("protocolMajor", u(3)),
        ("hostBuildId", t("host")),
        (
            "expectedProtocolContractSha256",
            t(&digest_hex(&raw_sha256(RPP))),
        ),
        ("expectedIdentity", identity),
        ("expectedCapabilities", a(tokens)),
        (
            "identityVersions",
            m(&[
                ("snapshot", u(2)),
                ("plan", u(2)),
                ("fact", u(2)),
                ("coverage", u(3)),
            ]),
        ),
        ("limits", limits),
    ]);
    let open = with(&accepted, "planIntentCommitment", t(&sha('2')));
    let snapshot_seal = m(&[
        ("snapshotId", get(&accepted, "snapshotId").clone()),
        ("manifestSha256", t(&h('b'))),
        ("entryCount", u(1)),
        ("totalFileBytes", u(100)),
        ("totalChunkCount", u(1)),
    ]);
    let dependency_seal = m(&[
        (
            "dependencySourceSetId",
            get(inputs, "dependencySourceSetId").clone(),
        ),
        ("manifestSha256", t(&h('b'))),
        ("entryCount", u(0)),
        ("totalBytes", u(0)),
        ("totalChunkCount", u(0)),
    ]);
    let stages = (0..2)
        .map(|i| {
            let k = key(i);
            let plan_stage = m(&[
                ("kind", t("fact-derivation")),
                ("stageId", t(if i == 0 { "stage-one" } else { "stage-two" })),
                ("relations", a(vec![t("calls")])),
                ("operator", t("semantic-provider")),
                ("budget", m(&[("unit", t("items")), ("limit", u(10))])),
            ]);
            let request = m(&[
                ("relation", t(&k.relation)),
                ("resolution", t(&k.resolution)),
                ("sourceUniverseId", t(&k.source_universe_id)),
                ("targetUniverseId", t(&k.target_universe_id)),
                ("subjectScopeCommitment", t(&k.subject_scope_commitment)),
                ("producer", t("rust-semantic")),
                ("producerVersion", t("provider")),
                ("schemaVersion", u(1)),
            ]);
            let analysis_domain = m(&[
                (
                    "subjects",
                    a(vec![m(&[
                        ("subjectOrdinal", u(0)),
                        ("subjectId", t(&format!("rust-file:{}", sha('4')))),
                        ("path", t("src/lib.rs")),
                        ("startByte", u(0)),
                        ("endByte", u(100)),
                    ])]),
                ),
                ("requestedCoverageDomain", a(vec![request])),
                ("domainCommitment", t(&sha('3'))),
            ]);
            Rust3StageBinding {
                plan_stage,
                analysis_domain,
            }
        })
        .collect();
    Rust3DispatchContext {
        hello,
        open_universe: open,
        snapshot_seal,
        dependency_seal,
        prepared_seal: None,
        manifest_files: BTreeMap::from_iter([("src/lib.rs".to_owned(), (h('a'), 100))]),
        universe_key: sha('5'),
        target_domain: BTreeSet::from_iter([sha('6')]),
        analysis_ordinal: 7,
        stages,
    }
}
fn ack(c: &Rust3DispatchContext) -> Value {
    let Value::Map(mut f) = get(&c.hello, "expectedIdentity").clone() else {
        panic!("identity")
    };
    f.push((
        "capabilities".to_owned(),
        get(&c.hello, "expectedCapabilities").clone(),
    ));
    f.push((
        "identityVersions".to_owned(),
        get(&c.hello, "identityVersions").clone(),
    ));
    Value::Map(f)
}
fn accepted(c: &Rust3DispatchContext) -> Value {
    let Value::Map(mut f) = c.open_universe.clone() else {
        panic!("open")
    };
    f.retain(|(k, _)| k != "planIntentCommitment");
    Value::Map(f)
}
fn received(name: &str, payload: Value, seq: u64) -> ReceivedFrame {
    let env = m(&[
        ("protocolMajor", u(3)),
        ("direction", t("worker-to-host")),
        ("sequence", u(seq)),
        ("frameType", t(name)),
        ("payload", payload),
    ]);
    let bytes = write_frame(&env).unwrap();
    read_frame(
        &mut bytes.as_slice(),
        cbor::Profile::Rust3,
        RUST3_FRAME_MAX_DEPTH,
        None,
    )
    .unwrap()
    .unwrap()
}
fn worker(
    r: &mut Rust3Receiver<'_>,
    name: &str,
    v: Value,
    seq: u64,
) -> Result<Rust3Admitted, Rust3Refusal> {
    r.receive(received(name, v, seq))
}
fn native(c: &Rust3DispatchContext) -> Value {
    let id = get(
        get(get(&c.open_universe, "universe"), "resolvedInputs"),
        "nativeContextId",
    )
    .clone();
    m(&[
        ("nativeContextId", id.clone()),
        ("recomputedNativeContextId", id),
        ("equal", Value::Bool(true)),
    ])
}
fn analyzing(r: &mut Rust3Receiver<'_>, c: &Rust3DispatchContext) -> u64 {
    assert!(r.admits(&Rust3HostFrame::Hello));
    r.sent(Rust3HostFrame::Hello).unwrap();
    worker(r, "HelloAck", ack(c), 0).unwrap();
    r.sent(Rust3HostFrame::OpenUniverse).unwrap();
    worker(r, "UniverseAccepted", accepted(c), 1).unwrap();
    r.sent(Rust3HostFrame::SnapshotManifest).unwrap();
    r.sent(Rust3HostFrame::SnapshotSeal).unwrap();
    worker(r, "SnapshotAccepted", c.snapshot_seal.clone(), 2).unwrap();
    assert_eq!(r.phase(), "READY_DEPENDENCY_MANIFEST");
    r.sent(Rust3HostFrame::DependencySourceManifest).unwrap();
    r.sent(Rust3HostFrame::DependencySourceSeal).unwrap();
    worker(r, "DependencySourceAccepted", c.dependency_seal.clone(), 3).unwrap();
    worker(r, "NativeContextVerified", native(c), 4).unwrap();
    r.sent(Rust3HostFrame::Analyze).unwrap();
    assert_eq!(r.phase(), "ANALYZING");
    5
}
fn candidate(ordinal: u64) -> Value {
    m(&[
        ("candidateOrdinal", u(ordinal)),
        ("relation", t("calls")),
        ("resolution", t("syntactic-callee-name")),
        ("layer", t("semantic")),
        ("producer", t("rust-semantic")),
        ("producerVersion", t("provider")),
        ("schemaVersion", u(1)),
        ("language", t("rust")),
        ("sourceUniverseId", t(&sha('5'))),
        ("targetUniverseId", t(&sha('6'))),
        ("confidenceMillionths", u(1000000)),
        ("relationSchemaId", t("opensip.relation.calls.v1")),
        (
            "canonicalRelationPayload",
            Value::Bytes(cbor::encode(&m(&[
                ("calleeText", t("g")),
                ("caller", t("f")),
            ]))),
        ),
        (
            "anchors",
            a(vec![m(&[
                ("kind", t("source-span")),
                ("snapshotId", t(&snapshot())),
                ("path", t("src/lib.rs")),
                ("contentSha256", t(&h('a'))),
                ("startByte", u(0)),
                ("endByte", u(10)),
                ("factId", Value::Null),
            ])]),
        ),
    ])
}
fn batch(stage: &str, index: u64, ordinal: u64) -> Value {
    m(&[
        ("analysisOrdinal", u(7)),
        ("stageId", t(stage)),
        ("batchIndex", u(index)),
        ("candidates", a(vec![candidate(ordinal)])),
    ])
}
fn built(domain: &str, value: &Value) -> String {
    let mut preimage = domain.as_bytes().to_vec();
    preimage.push(0);
    preimage.extend(cbor::encode(value));
    format!("sha256:{}", digest_hex(&raw_sha256(&preimage)))
}
fn entry(key: &Key, coverage: &str, deficiency: Value) -> Value {
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
fn coverage(index: usize) -> Value {
    let entries = a(vec![entry(&key(index), "complete", Value::Null)]);
    m(&[
        ("analysisOrdinal", u(7)),
        (
            "stageId",
            t(if index == 0 { "stage-one" } else { "stage-two" }),
        ),
        (
            "coverageCommitment",
            t(&built("opensip.rust-provider.stage-coverage.v2", &entries)),
        ),
        ("entries", entries),
    ])
}
fn complete(facts: &[Vec<Value>]) -> Value {
    let mut allfacts = Vec::new();
    let mut allcoverage = Vec::new();
    let mut results = Vec::new();
    for (i, facts) in facts.iter().enumerate() {
        let Value::Array(entries) = get(&coverage(i), "entries").clone() else {
            panic!("entries")
        };
        results.push(m(&[
            ("stageId", t(if i == 0 { "stage-one" } else { "stage-two" })),
            ("factCount", u(facts.len() as u64)),
            ("coverageEntryCount", u(entries.len() as u64)),
            (
                "factCommitment",
                t(&built(
                    "opensip.rust-provider.stage-facts.v2",
                    &a(facts.clone()),
                )),
            ),
            (
                "coverageCommitment",
                t(&built(
                    "opensip.rust-provider.stage-coverage.v2",
                    &a(entries.clone()),
                )),
            ),
        ]));
        allfacts.extend(facts.clone());
        allcoverage.extend(entries);
    }
    m(&[
        ("analysisOrdinal", u(7)),
        ("stageResults", a(results)),
        (
            "factStreamCommitment",
            t(&built("opensip.rust-provider.fact-stream.v2", &a(allfacts))),
        ),
        (
            "coverageStreamCommitment",
            t(&built(
                "opensip.rust-provider.coverage-stream.v2",
                &a(allcoverage),
            )),
        ),
    ])
}
#[test]
fn rust3_receive_two_stages_publishes_generated_types_and_full_spool_entries() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let c = context(false);
    let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
    let seq = analyzing(&mut r, &c);
    let got = worker(&mut r, "FactBatch", batch("stage-one", 0, 0), seq).unwrap();
    assert!(matches!(
        got.payload,
        Rust3ProviderFrameV3Payload::FactBatch0(_)
    ));
    assert_eq!(
        got.spool_entries,
        vec![cbor::encode(&m(&[
            ("analysisOrdinal", u(7)),
            ("stageId", t("stage-one")),
            ("candidate", candidate(0))
        ]))]
    );
    assert_eq!(
        worker(&mut r, "CoverageV3", coverage(0), seq + 1)
            .unwrap()
            .trace,
        "P3-24"
    );
    assert_eq!(r.phase(), "ANALYZING");
    worker(&mut r, "CoverageV3", coverage(1), seq + 2).unwrap();
    assert_eq!(r.phase(), "READY_COMPLETE");
    let got = worker(
        &mut r,
        "Complete",
        complete(&[vec![candidate(0)], vec![]]),
        seq + 3,
    )
    .unwrap();
    let Rust3ProviderFrameV3Payload::Complete(v) = got.payload else {
        panic!("complete type")
    };
    assert_eq!(v.stage_results.len(), 2);
    assert_eq!(v.stage_results[0].fact_count, 1);
    assert_eq!(r.terminal_kind(), Some("complete"));
    r.process(ProcessEvent::ZeroExit).unwrap();
    r.process(ProcessEvent::Eof).unwrap();
    assert_eq!(r.phase(), "DONE");
    assert_eq!(r.totals().frames, 9);
    assert_eq!(r.totals().candidates, 1);
}
#[test]
fn rust3_receive_hello_exact_echo_refuses_before_source_disclosure() {
    let table = Table::load(Protocol::Rust3).unwrap();
    for target in [false, true] {
        let c = context(target);
        for key in [
            "rustCommitHash",
            "sysrootDigest",
            "hostTriple",
            "targetTriple",
            "providerBuildId",
        ] {
            let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
            r.sent(Rust3HostFrame::Hello).unwrap();
            let replacement = match key {
                "rustCommitHash" => t(&"b".repeat(40)),
                "sysrootDigest" => t(&h('b')),
                _ => t("other"),
            };
            let bad = with(&ack(&c), key, replacement);
            assert!(
                matches!(
                    worker(&mut r, "HelloAck", bad, 0),
                    Err(Rust3Refusal::Admission(_))
                ),
                "{key}"
            );
            assert_eq!(r.phase(), "WAIT_HELLO_ACK");
            assert!(!r.admits(&Rust3HostFrame::OpenUniverse));
            assert_eq!(r.totals().frames, 0);
        }
        let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
        r.sent(Rust3HostFrame::Hello).unwrap();
        let mut caps = if let Value::Array(v) = get(&c.hello, "expectedCapabilities").clone() {
            v
        } else {
            panic!("caps")
        };
        caps.remove(0);
        assert!(
            worker(
                &mut r,
                "HelloAck",
                with(&ack(&c), "capabilities", a(caps)),
                0
            )
            .is_err()
        );
        assert!(!r.admits(&Rust3HostFrame::OpenUniverse));
    }
}
#[test]
fn rust3_receive_all_32_hello_limits_are_required_and_exact() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let base = context(false);
    let Value::Map(limits) = get(&base.hello, "limits") else {
        panic!("limits")
    };
    assert_eq!(limits.len(), 32);
    for (key, value) in limits {
        let Value::Unsigned(n) = value else {
            panic!("limit")
        };
        let mut c = base.clone();
        c.hello = with(
            &base.hello,
            "limits",
            with(get(&base.hello, "limits"), key, u(n + 1)),
        );
        assert!(
            matches!(Rust3Receiver::new(&table, c), Err(Rust3Refusal::Context(_))),
            "{key}"
        );
    }
}
#[test]
fn rust3_receive_misordered_stages_ordinals_and_batches_never_publish() {
    let table = Table::load(Protocol::Rust3).unwrap();
    for bad in [
        with(&batch("stage-one", 0, 0), "stageId", t("stage-two")),
        with(&batch("stage-one", 0, 0), "analysisOrdinal", u(8)),
        batch("stage-one", 1, 0),
        batch("stage-one", 0, 1),
    ] {
        let c = context(false);
        let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
        let seq = analyzing(&mut r, &c);
        let before = r.totals();
        assert!(matches!(
            worker(&mut r, "FactBatch", bad, seq),
            Err(Rust3Refusal::Admission(_))
        ));
        assert_eq!(r.totals(), before);
        assert_eq!(r.retained.len(), 0);
        assert!(matches!(
            worker(&mut r, "FactBatch", batch("stage-one", 0, 0), seq),
            Err(Rust3Refusal::AfterRefusal)
        ));
    }
}
#[test]
fn rust3_receive_raw_commitment_mismatch_and_wrong_profile_refuse() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let c = context(false);
    let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
    let seq = analyzing(&mut r, &c);
    let before = r.totals();
    assert!(matches!(
        worker(
            &mut r,
            "CoverageV3",
            with(&coverage(0), "coverageCommitment", t(&sha('0'))),
            seq
        ),
        Err(Rust3Refusal::Admission(_))
    ));
    assert_eq!(r.totals(), before);
    let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
    r.sent(Rust3HostFrame::Hello).unwrap();
    let env = m(&[
        ("protocolMajor", u(3)),
        ("direction", t("worker-to-host")),
        ("sequence", u(0)),
        ("frameType", t("HelloAck")),
        ("payload", ack(&c)),
    ]);
    let raw = write_frame(&env).unwrap();
    let read = read_frame(&mut raw.as_slice(), cbor::Profile::Ts2, 7, None)
        .unwrap()
        .unwrap();
    assert!(matches!(r.receive(read), Err(Rust3Refusal::Envelope(_))));
}
fn fault(phase: &str, execution: Option<&str>, ordinal: Option<u64>) -> Value {
    m(&[
        ("executionId", execution.map(t).unwrap_or(Value::Null)),
        ("analysisOrdinal", ordinal.map(u).unwrap_or(Value::Null)),
        ("phase", t(phase)),
        ("faultKind", t("input-rejected")),
        ("detailCode", t("diagnostic-only")),
    ])
}
#[test]
fn rust3_receive_provider_fault_joint_window_is_wired_before_p3t() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let c = context(false);
    for bad in [false, true] {
        let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
        r.sent(Rust3HostFrame::Hello).unwrap();
        let got = worker(
            &mut r,
            "ProviderFault",
            fault(if bad { "START" } else { "WAIT_HELLO_ACK" }, None, None),
            0,
        );
        if bad {
            assert!(got.is_err())
        } else {
            assert!(matches!(
                got.unwrap().payload,
                Rust3ProviderFrameV3Payload::ProviderFault(_)
            ));
            assert_eq!(r.terminal_kind(), Some("provider-fault"));
        }
    }
    for (phase, execution, expected) in [
        ("READY_OPEN_UNIVERSE", None, true),
        ("WAIT_UNIVERSE_ACCEPTED", Some("execution"), true),
        ("READY_OPEN_UNIVERSE", Some("execution"), false),
        ("WAIT_UNIVERSE_ACCEPTED", None, false),
        ("WAIT_HELLO_ACK", None, false),
    ] {
        let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
        r.sent(Rust3HostFrame::Hello).unwrap();
        worker(&mut r, "HelloAck", ack(&c), 0).unwrap();
        r.sent(Rust3HostFrame::OpenUniverse).unwrap();
        let got = worker(&mut r, "ProviderFault", fault(phase, execution, None), 1);
        if expected {
            assert!(got.is_ok(), "{phase} {execution:?}")
        } else {
            assert!(
                matches!(got, Err(Rust3Refusal::Admission(_))),
                "joint worker observation must refuse {phase} {execution:?}"
            )
        }
    }
}
#[test]
fn rust3_receive_cancelled_echoes_exact_cancel_and_the_send_phase() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let c = context(false);
    for observed in ["ANALYZING", "READY_ANALYZE"] {
        let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
        let seq = analyzing(&mut r, &c);
        r.sent(Rust3HostFrame::Cancel {
            execution_id: Some("execution".to_owned()),
            analysis_ordinal: Some(7),
        })
        .unwrap();
        let got = worker(
            &mut r,
            "Cancelled",
            m(&[
                ("executionId", t("execution")),
                ("analysisOrdinal", u(7)),
                ("observedPhase", t(observed)),
            ]),
            seq,
        );
        if observed == "ANALYZING" {
            assert!(matches!(
                got.unwrap().payload,
                Rust3ProviderFrameV3Payload::Cancelled(_)
            ));
            assert_eq!(r.terminal_kind(), Some("cancelled"));
        } else {
            assert!(matches!(got, Err(Rust3Refusal::Admission(_))))
        }
    }
    let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
    r.sent(Rust3HostFrame::Hello).unwrap();
    r.sent(Rust3HostFrame::Cancel {
        execution_id: None,
        analysis_ordinal: None,
    })
    .unwrap();
    worker(
        &mut r,
        "Cancelled",
        m(&[
            ("executionId", Value::Null),
            ("analysisOrdinal", Value::Null),
            ("observedPhase", t("WAIT_HELLO_ACK")),
        ]),
        0,
    )
    .unwrap();
    let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
    let seq = analyzing(&mut r, &c);
    r.sent(Rust3HostFrame::Cancel {
        execution_id: Some("execution".to_owned()),
        analysis_ordinal: Some(7),
    })
    .unwrap();
    assert!(
        matches!(
            worker(&mut r, "FactBatch", batch("stage-one", 0, 0), seq),
            Err(Rust3Refusal::Table(_))
        ),
        "in-flight frame must not bypass the actual post-Cancel table"
    );
}
fn terminal_coverage(deficiency: &str) -> Value {
    a((0..2)
        .map(|i| entry(&key(i), "unknown", t(deficiency)))
        .collect())
}
fn budget() -> Value {
    let entries = terminal_coverage("budget-exhausted");
    m(&[
        ("analysisOrdinal", u(7)),
        ("triggerStageId", t("stage-one")),
        ("unit", t("items")),
        ("limit", u(10)),
        ("observed", u(11)),
        (
            "coverageCommitment",
            t(&built("opensip.rust-provider.coverage-stream.v2", &entries)),
        ),
        ("coverage", entries),
    ])
}
#[test]
fn rust3_receive_budget_exhausted_matches_only_the_current_stage_and_exact_units() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let c = context(false);
    let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
    let seq = analyzing(&mut r, &c);
    let got = worker(&mut r, "BudgetExhausted", budget(), seq).unwrap();
    assert!(matches!(
        got.payload,
        Rust3ProviderFrameV3Payload::BudgetExhausted(_)
    ));
    assert_eq!(r.terminal_kind(), Some("budget-exhausted"));
    for bad in [
        with(&budget(), "triggerStageId", t("stage-two")),
        with(&budget(), "unit", t("bytes")),
        with(&budget(), "limit", u(9)),
        with(&budget(), "observed", u(12)),
    ] {
        let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
        let seq = analyzing(&mut r, &c);
        let before = r.totals();
        assert!(
            matches!(
                worker(&mut r, "BudgetExhausted", bad, seq),
                Err(Rust3Refusal::Admission(_))
            ),
            "T020 current-stage guard must refuse"
        );
        assert_eq!(r.totals(), before);
    }
}
#[test]
fn rust3_receive_optional_token_omission_is_an_exact_echo_failure() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let c = context(true);
    let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
    r.sent(Rust3HostFrame::Hello).unwrap();
    let bad = with(
        &ack(&c),
        "capabilities",
        a(TOKENS.iter().map(|s| t(s)).collect()),
    );
    assert!(
        matches!(
            worker(&mut r, "HelloAck", bad, 0),
            Err(Rust3Refusal::Admission(_))
        ),
        "offered optional token omission must refuse before disclosure"
    );
    assert_eq!(r.totals().frames, 0);
    assert!(!r.admits(&Rust3HostFrame::OpenUniverse));
}
#[test]
fn rust3_receive_deepest_coverage_is_admitted_and_one_more_container_refuses() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let c = context(false);
    let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
    let seq = analyzing(&mut r, &c);
    let value = coverage(0);
    let frame = received("CoverageV3", value.clone(), seq);
    assert_eq!(depth(frame.value()), 7);
    assert_eq!(r.receive(frame).unwrap().trace, "P3-24");
    let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
    let seq = analyzing(&mut r, &c);
    let Value::Array(entries) = get(&value, "entries") else {
        panic!("entries")
    };
    let e = &entries[0];
    let inner = get(e, "entry");
    let rc = get(inner, "resolutionCompleteness");
    let rc = with(rc, "unresolvedEdgeClasses", a(vec![a(vec![])]));
    let e = with(e, "entry", with(inner, "resolutionCompleteness", rc));
    let deep = with(&value, "entries", a(vec![e]));
    let env = m(&[
        ("protocolMajor", u(3)),
        ("direction", t("worker-to-host")),
        ("sequence", u(seq)),
        ("frameType", t("CoverageV3")),
        ("payload", deep),
    ]);
    assert_eq!(depth(&env), 8);
    let raw = write_frame(&env).unwrap();
    let before = r.totals();
    assert!(
        matches!(r.read(&mut raw.as_slice()),Err(Rust3Refusal::Transport(s))if s.contains("Depth"))
    );
    assert_eq!(r.totals(), before);
}
fn depth(v: &Value) -> usize {
    match v {
        Value::Array(xs) => 1 + xs.iter().map(depth).max().unwrap_or(0),
        Value::Map(xs) => 1 + xs.iter().map(|(_, v)| depth(v)).max().unwrap_or(0),
        _ => 0,
    }
}
#[test]
fn rust3_receive_commitments_use_only_retained_received_value_slices() {
    PROVENANCE.with_borrow_mut(Vec::clear);
    let table = Table::load(Protocol::Rust3).unwrap();
    let c = context(false);
    let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
    let seq = analyzing(&mut r, &c);
    worker(&mut r, "FactBatch", batch("stage-one", 0, 0), seq).unwrap();
    worker(&mut r, "CoverageV3", coverage(0), seq + 1).unwrap();
    worker(&mut r, "CoverageV3", coverage(1), seq + 2).unwrap();
    worker(
        &mut r,
        "Complete",
        complete(&[vec![candidate(0)], vec![]]),
        seq + 3,
    )
    .unwrap();
    let log = PROVENANCE.with_borrow(Clone::clone);
    assert_eq!(log.len(), 8);
    let buffers = r
        .retained
        .iter()
        .map(|f| {
            let p = f.payload();
            (p.as_ptr() as usize, p.len())
        })
        .collect::<Vec<_>>();
    let mut parts = 0;
    for (_, slices) in log {
        for (address, length) in slices {
            parts += 1;
            assert!(
                buffers
                    .iter()
                    .any(|(start, size)| address >= *start && address + length <= start + size),
                "commitment input must belong to a retained received buffer"
            );
        }
    }
    assert_eq!(parts, 8);
}
fn prepared_context() -> Rust3DispatchContext {
    let mut c = context(false);
    let universe = get(&c.open_universe, "universe");
    let inputs = get(universe, "resolvedInputs");
    let flags = with(
        get(inputs, "rustflags"),
        "stripped",
        a(vec![m(&[
            ("flag", t("-Ctarget-cpu=native")),
            ("reason", t("codegen-option-not-allowlisted")),
        ])]),
    );
    let inputs = with(
        &with(
            &with(
                &with(inputs, "preparedOutputSetId", t(&sha('9'))),
                "preparedResolution",
                t("imported-inert"),
            ),
            "executionCapableResolution",
            Value::Bool(true),
        ),
        "rustflags",
        flags,
    );
    let effect = m(&[
        ("requested", t("none")),
        ("enforcement", t("DISCLOSURE-ONLY")),
    ]);
    let effects = m(&[
        ("environment", effect.clone()),
        ("filesystemWrite", effect.clone()),
        ("network", effect.clone()),
        ("subprocess", effect),
    ]);
    let repo = with(
        &with(
            get(&c.open_universe, "repositoryResolution"),
            "preparedOutputSetId",
            t(&sha('9')),
        ),
        "effects",
        effects,
    );
    c.open_universe = with(
        &with(
            &c.open_universe,
            "universe",
            with(universe, "resolvedInputs", inputs),
        ),
        "repositoryResolution",
        repo,
    );
    c.prepared_seal = Some(m(&[
        ("planId", get(&c.open_universe, "planId").clone()),
        ("manifestSha256", t(&h('b'))),
        ("entryCount", u(0)),
        ("totalBlobBytes", u(0)),
        ("totalChunkCount", u(0)),
    ]));
    c
}
#[test]
fn rust3_receive_prepared_mode_recursively_converts_resolved_inputs_and_effects() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let c = prepared_context();
    let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
    r.sent(Rust3HostFrame::Hello).unwrap();
    worker(&mut r, "HelloAck", ack(&c), 0).unwrap();
    r.sent(Rust3HostFrame::OpenUniverse).unwrap();
    let got = worker(&mut r, "UniverseAccepted", accepted(&c), 1).unwrap();
    let Rust3ProviderFrameV3Payload::UniverseAccepted(v) = got.payload else {
        panic!("universe type")
    };
    assert_eq!(v.universe.resolved_inputs.cfg_sets.len(), 2);
    assert_eq!(v.universe.resolved_inputs.edition.len(), 1);
    assert_eq!(v.universe.resolved_inputs.rustflags.stripped.len(), 1);
    assert!(v.repository_resolution.effects.is_some());
    assert!(v.universe.resolved_inputs.execution_capable_resolution);
    r.sent(Rust3HostFrame::SnapshotManifest).unwrap();
    r.sent(Rust3HostFrame::SnapshotSeal).unwrap();
    worker(&mut r, "SnapshotAccepted", c.snapshot_seal.clone(), 2).unwrap();
    r.sent(Rust3HostFrame::DependencySourceManifest).unwrap();
    r.sent(Rust3HostFrame::DependencySourceSeal).unwrap();
    worker(
        &mut r,
        "DependencySourceAccepted",
        c.dependency_seal.clone(),
        3,
    )
    .unwrap();
    assert_eq!(r.phase(), "READY_PREPARED_MANIFEST");
    r.sent(Rust3HostFrame::PreparedOutputManifest).unwrap();
    r.sent(Rust3HostFrame::PreparedOutputSeal).unwrap();
    let got = worker(
        &mut r,
        "PreparedOutputAccepted",
        c.prepared_seal.clone().unwrap(),
        4,
    )
    .unwrap();
    assert!(matches!(
        got.payload,
        Rust3ProviderFrameV3Payload::PreparedOutputAccepted(_)
    ));
    worker(&mut r, "NativeContextVerified", native(&c), 5).unwrap();
    assert_eq!(r.phase(), "READY_ANALYZE");
}
fn companion() -> Value {
    m(&[
        ("schemaVersion", u(1)),
        ("candidateOrdinal", u(0)),
        ("targetUniverseId", t(&sha('6'))),
        ("targetNativeId", t("native-target")),
        ("kind", t("unknown")),
        ("occupancy", t("unknown")),
        ("exported", Value::Null),
        ("logicalPath", Value::Null),
        ("packageManifestPath", Value::Null),
        ("evaluationNativeId", Value::Null),
    ])
}
#[test]
fn rust3_receive_target_attribution_checks_the_original_companion_schema_and_batch_join() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let c = context(true);
    let v3 = with(
        &with(&batch("stage-one", 0, 0), "schemaVersion", u(3)),
        "occupancyCompanions",
        a(vec![companion()]),
    );
    let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
    let seq = analyzing(&mut r, &c);
    let got = worker(&mut r, "FactBatch", v3.clone(), seq).unwrap();
    let Rust3ProviderFrameV3Payload::FactBatch1(v) = got.payload else {
        panic!("target-attribution variant")
    };
    assert_eq!(v.occupancy_companions.len(), 1);
    for comp in [
        with(&companion(), "candidateOrdinal", u(1)),
        with(&companion(), "targetUniverseId", t(&sha('7'))),
    ] {
        let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
        let seq = analyzing(&mut r, &c);
        assert!(matches!(
            worker(
                &mut r,
                "FactBatch",
                with(&v3, "occupancyCompanions", a(vec![comp])),
                seq
            ),
            Err(Rust3Refusal::Admission(_))
        ))
    }
    let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
    let seq = analyzing(&mut r, &c);
    assert!(matches!(
        worker(
            &mut r,
            "FactBatch",
            with(
                &v3,
                "occupancyCompanions",
                a(vec![with(&companion(), "logicalPath", t("unowned-hint"))])
            ),
            seq
        ),
        Err(Rust3Refusal::Schema(_))
    ));
}
#[test]
fn rust3_receive_unavailable_keeps_its_phase_specific_shape_and_stage_major_coverage() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let c = context(false);
    let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
    r.sent(Rust3HostFrame::Hello).unwrap();
    worker(&mut r, "HelloAck", ack(&c), 0).unwrap();
    r.sent(Rust3HostFrame::OpenUniverse).unwrap();
    worker(&mut r, "UniverseAccepted", accepted(&c), 1).unwrap();
    r.sent(Rust3HostFrame::SnapshotManifest).unwrap();
    r.sent(Rust3HostFrame::SnapshotSeal).unwrap();
    worker(&mut r, "SnapshotAccepted", c.snapshot_seal.clone(), 2).unwrap();
    r.sent(Rust3HostFrame::DependencySourceManifest).unwrap();
    r.sent(Rust3HostFrame::DependencySourceSeal).unwrap();
    worker(
        &mut r,
        "DependencySourceAccepted",
        c.dependency_seal.clone(),
        3,
    )
    .unwrap();
    let pre = m(&[
        ("executionId", get(&c.open_universe, "executionId").clone()),
        ("snapshotId", get(&c.open_universe, "snapshotId").clone()),
        ("planId", get(&c.open_universe, "planId").clone()),
        ("reason", t("native-context-mismatch")),
        (
            "nativeContextId",
            get(
                get(get(&c.open_universe, "universe"), "resolvedInputs"),
                "nativeContextId",
            )
            .clone(),
        ),
        ("recomputedNativeContextId", t(&sha('e'))),
    ]);
    let got = worker(&mut r, "Unavailable", pre, 4).unwrap();
    assert!(matches!(
        got.payload,
        Rust3ProviderFrameV3Payload::Unavailable0(_)
    ));
    let entries = terminal_coverage("provider-unavailable");
    let post = m(&[
        ("analysisOrdinal", u(7)),
        ("affectedStageIds", a(vec![t("stage-one"), t("stage-two")])),
        ("reason", t("dependency-source-incomplete")),
        (
            "coverageCommitment",
            t(&built("opensip.rust-provider.coverage-stream.v2", &entries)),
        ),
        ("coverage", entries),
    ]);
    let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
    let seq = analyzing(&mut r, &c);
    let got = worker(&mut r, "Unavailable", post.clone(), seq).unwrap();
    assert!(matches!(
        got.payload,
        Rust3ProviderFrameV3Payload::Unavailable1(_)
    ));
    let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
    let seq = analyzing(&mut r, &c);
    assert!(matches!(
        worker(
            &mut r,
            "Unavailable",
            with(
                &post,
                "affectedStageIds",
                a(vec![t("stage-two"), t("stage-one")])
            ),
            seq
        ),
        Err(Rust3Refusal::Admission(_))
    ));
}
#[test]
fn rust3_receive_context_and_recursive_echo_never_substitute_a_different_identity() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let base = context(false);
    let mut wrong = base.clone();
    wrong.open_universe = with(
        &wrong.open_universe,
        "universe",
        with(
            get(&wrong.open_universe, "universe"),
            "rustCommitHash",
            t(&"b".repeat(40)),
        ),
    );
    assert!(
        matches!(
            Rust3Receiver::new(&table, wrong),
            Err(Rust3Refusal::Context(_))
        ),
        "trusted projections must agree on the Rust identity"
    );
    let mut r = Rust3Receiver::new(&table, base.clone()).unwrap();
    r.sent(Rust3HostFrame::Hello).unwrap();
    worker(&mut r, "HelloAck", ack(&base), 0).unwrap();
    r.sent(Rust3HostFrame::OpenUniverse).unwrap();
    let value = accepted(&base);
    let inputs = get(get(&value, "universe"), "resolvedInputs");
    let inputs = with(inputs, "unifiedFeaturesId", t(&sha('e')));
    let bad = with(
        &value,
        "universe",
        with(get(&value, "universe"), "resolvedInputs", inputs),
    );
    assert!(
        matches!(
            worker(&mut r, "UniverseAccepted", bad, 1),
            Err(Rust3Refusal::Admission(_))
        ),
        "recursive echo must compare the original resolved input value"
    );
    assert_eq!(r.totals().frames, 1);
}
#[test]
fn rust3_receive_sequence_exhaustion_and_transport_allowance_fail_before_publication() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let c = context(false);
    let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
    r.sent(Rust3HostFrame::Hello).unwrap();
    r.sequence.next = u64::MAX;
    assert!(matches!(
        worker(&mut r, "HelloAck", ack(&c), u64::MAX),
        Err(Rust3Refusal::Envelope(_))
    ));
    assert_eq!(r.totals().frames, 0);
    let mut r = Rust3Receiver::new(&table, c).unwrap();
    let prefix = (super::super::super::MAX_FRAME_PAYLOAD_BYTES + 1)
        .to_be_bytes()
        .to_vec();
    assert!(
        matches!(r.read(&mut prefix.as_slice()),Err(Rust3Refusal::Transport(s))if s.contains("Oversize"))
    );
    assert_eq!(r.totals(), ResponseTotals::default());
}

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
        "uint64" | "text" | "bytes" | "null" | "bool" => 0,
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
            if r.get("kind").and_then(txt) == Some("alias") {
                return carrier_depth(docs, carriers, r.get("target").unwrap(), &seen);
            }
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
fn rust3_receive_depth_bound_is_recomputed_over_base_and_both_successors() {
    crate::schema_sources::registry().unwrap();
    let docs = documents();
    let c = parse_json(carrier::CARRIERS).unwrap();
    let c = obj(&c).unwrap();
    let named = |name: &str| {
        let ty = parse_json(format!("{{\"t\":\"ref\",\"ref\":\"{name}\"}}").as_bytes()).unwrap();
        carrier_depth(&docs, c, &ty, &BTreeSet::new())
    };
    let base = named("Rust3ProviderFrameV3");
    let stage2 = named("Rust3StageRequestV2");
    let plan = named("Rust3C2PlanStageV3");
    let scope = "opensip.product.rust-subject-scope.1";
    let stage3 = resolve(&docs, "#/$defs/StageRequestV3", scope).0;
    // The successor deliberately does not restate the selected C2 stage.
    // Its annotation retains that exact carrier, not an arbitrary object.
    let ps = obj(path(stage3, &["properties", "planStage"]).unwrap()).unwrap();
    assert_eq!(ps.get("type").and_then(txt), Some("object"));
    assert_eq!(ps.len(), 2);
    assert_eq!(
        ps.get("description").and_then(txt),
        Some(
            "StageRequestV2.planStage, unchanged: the exact nested C-2 stage value (planStageByteRule). Not restated here."
        )
    );
    let domain3 = schema_depth(
        &docs,
        resolve(&docs, "#/$defs/StageAnalysisDomainV3", scope).0,
        scope,
        &BTreeSet::new(),
    );
    let stage3 = 1 + plan.max(domain3);
    let census = "opensip.product.symbol-census.1";
    let analyze3 = resolve(&docs, "#/$defs/AnalyzeV3", census).0;
    let item = obj(path(analyze3, &["properties", "stages", "items"]).unwrap()).unwrap();
    assert_eq!(item.len(), 1);
    assert_eq!(item.get("type").and_then(txt), Some("object"));
    assert_eq!(
        path(analyze3, &["properties", "stages", "description"]).and_then(txt),
        Some(
            "rust-provider-protocol.v2 wireSchema.definitions.StageRequestV2, unchanged in members and law; its analysisDomain keys' subjectScopeCommitment values follow native-evidence 4.1a and 9.8. Not restated here."
        )
    );
    let complete3 = 1 + schema_depth(
        &docs,
        resolve(&docs, "#/$defs/CompleteV3", census).0,
        census,
        &BTreeSet::new(),
    );
    // Both target-attribution alternatives are already in the base carrier
    // frame graph. All eight independent token combinations are included.
    for _attribution in [false, true] {
        for census in [false, true] {
            for scope in [false, true] {
                let analyze = 3 + if scope { stage3 } else { stage2 };
                let complete = if census {
                    complete3
                } else {
                    1 + named("Rust3CompleteV2")
                };
                assert_eq!(base.max(analyze).max(complete), RUST3_FRAME_MAX_DEPTH);
            }
        }
    }
    let relation = "opensip.product.relation-payload.2";
    let defs = obj(path(&docs[relation], &["$defs"]).unwrap()).unwrap();
    assert_eq!(
        defs.values()
            .map(|s| schema_depth(&docs, s, relation, &BTreeSet::new()))
            .max(),
        Some(RELATION_PAYLOAD_MAX_DEPTH)
    );
}
fn with_candidate(value: Value) -> Value {
    with(&batch("stage-one", 0, 0), "candidates", a(vec![value]))
}
#[test]
fn rust3_receive_candidate_registry_and_embedded_payload_guards_run_before_publication() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let c = context(false);
    let mut cases = vec![
        with(&candidate(0), "relation", t("file")),
        with(&candidate(0), "resolution", t("enumerated")),
        with(&candidate(0), "layer", t("syntax")),
        with(&candidate(0), "producerVersion", t("different-build")),
        with(&candidate(0), "schemaVersion", u(2)),
        with(&candidate(0), "relationSchemaId", t("other-schema")),
        with(&candidate(0), "sourceUniverseId", t(&sha('7'))),
        with(&candidate(0), "targetUniverseId", t(&sha('7'))),
    ];
    for raw in [
        vec![0x20],
        vec![0xf9, 0, 0],
        vec![0x18, 0],
        vec![0xa0, 0xa0],
        vec![0xa1, 0x61, b'a', 0x40],
        cbor::encode(&m(&[("nested", m(&[]))])),
    ] {
        cases.push(with(
            &candidate(0),
            "canonicalRelationPayload",
            Value::Bytes(raw),
        ));
    }
    for bad in cases {
        let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
        let seq = analyzing(&mut r, &c);
        let before = r.totals();
        assert!(
            matches!(
                worker(&mut r, "FactBatch", with_candidate(bad), seq),
                Err(Rust3Refusal::Admission(_))
            ),
            "wire candidate contextual/embedded refusal"
        );
        assert_eq!(r.totals(), before);
        assert!(r.retained.is_empty());
    }
    for bad in [
        with(&candidate(0), "producer", t("typescript-semantic")),
        with(&candidate(0), "language", t("typescript")),
        with(&candidate(0), "confidenceMillionths", u(1000001)),
    ] {
        let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
        let seq = analyzing(&mut r, &c);
        assert!(matches!(
            worker(&mut r, "FactBatch", with_candidate(bad), seq),
            Err(Rust3Refusal::Schema(_))
        ));
    }
}
#[test]
fn rust3_receive_anchor_manifest_join_nonempty_spans_and_fact_ref_are_enforced() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let c = context(false);
    let Value::Array(anchors) = get(&candidate(0), "anchors").clone() else {
        panic!("anchors")
    };
    let anchor = &anchors[0];
    let mut fact_ref = with(anchor, "kind", t("fact-ref"));
    for key in [
        "snapshotId",
        "path",
        "contentSha256",
        "startByte",
        "endByte",
    ] {
        fact_ref = with(&fact_ref, key, Value::Null);
    }
    fact_ref = with(&fact_ref, "factId", t(&format!("fact2:{}", h('a'))));
    for bad in [
        with(anchor, "snapshotId", t(&format!("snapshot2:{}", h('e')))),
        with(anchor, "path", t("src/absent.rs")),
        with(anchor, "contentSha256", t(&h('b'))),
        with(anchor, "startByte", u(10)),
        with(anchor, "endByte", u(101)),
        fact_ref,
    ] {
        let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
        let seq = analyzing(&mut r, &c);
        let bad = with(&candidate(0), "anchors", a(vec![bad]));
        assert!(
            matches!(
                worker(&mut r, "FactBatch", with_candidate(bad), seq),
                Err(Rust3Refusal::Admission(_))
            ),
            "anchor contextual refusal"
        );
        assert!(r.retained.is_empty());
    }
    let mut c = c;
    c.manifest_files.insert("a.rs".to_owned(), (h('b'), 100));
    c.snapshot_seal = with(
        &with(
            &with(&c.snapshot_seal, "entryCount", u(2)),
            "totalFileBytes",
            u(200),
        ),
        "totalChunkCount",
        u(2),
    );
    let second = with(
        &with(anchor, "path", t("a.rs")),
        "contentSha256",
        t(&h('b')),
    );
    let good = with(
        &candidate(0),
        "anchors",
        a(vec![anchor.clone(), second.clone()]),
    );
    let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
    let seq = analyzing(&mut r, &c);
    worker(&mut r, "FactBatch", with_candidate(good), seq).unwrap();
    let bad = with(&candidate(0), "anchors", a(vec![second, anchor.clone()]));
    let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
    let seq = analyzing(&mut r, &c);
    assert!(
        matches!(
            worker(&mut r, "FactBatch", with_candidate(bad), seq),
            Err(Rust3Refusal::Schema(_))
        ),
        "Rust3 anchors use CVE1 order, including when CBOR order differs"
    );
}
#[test]
fn rust3_receive_coverage_key_suffix_scope_and_stage_bijections_are_exact() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let c = context(false);
    let original = entry(&key(0), "complete", Value::Null);
    let mut bad_entries = Vec::new();
    for (name, value) in [
        ("relation", t("file")),
        ("resolution", t("enumerated")),
        ("sourceUniverse", t(&h('e'))),
        ("targetUniverse", t(&h('e'))),
        ("subjectScopeCommitment", t(&sha('e'))),
    ] {
        bad_entries.push(with(
            &original,
            "key",
            with(get(&original, "key"), name, value),
        ));
    }
    let inner = get(&original, "entry");
    bad_entries.push(with(
        &original,
        "entry",
        with(
            inner,
            "examinedUniverse",
            with(
                get(inner, "examinedUniverse"),
                "subjectScopeCommitment",
                t(&sha('e')),
            ),
        ),
    ));
    for bad in bad_entries {
        let entries = a(vec![bad]);
        let bad = with(
            &with(&coverage(0), "entries", entries.clone()),
            "coverageCommitment",
            t(&built("opensip.rust-provider.stage-coverage.v2", &entries)),
        );
        let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
        let seq = analyzing(&mut r, &c);
        let before = r.totals();
        assert!(matches!(
            worker(&mut r, "CoverageV3", bad, seq),
            Err(Rust3Refusal::Admission(_))
        ));
        assert_eq!(r.totals(), before);
    }
    let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
    let seq = analyzing(&mut r, &c);
    assert!(
        matches!(
            worker(&mut r, "CoverageV3", coverage(1), seq),
            Err(Rust3Refusal::Admission(_))
        ),
        "another requested stage is not the current stage"
    );
}
#[test]
fn rust3_receive_complete_checks_all_counts_domains_and_stage_order() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let c = context(false);
    let all = complete(&[vec![candidate(0)], vec![]]);
    let Value::Array(results) = get(&all, "stageResults") else {
        panic!("stage results")
    };
    let mut bad = vec![
        with(&all, "factStreamCommitment", t(&sha('0'))),
        with(&all, "coverageStreamCommitment", t(&sha('0'))),
        with(
            &all,
            "stageResults",
            a(vec![results[1].clone(), results[0].clone()]),
        ),
    ];
    for (name, value) in [
        ("factCount", u(0)),
        ("coverageEntryCount", u(0)),
        ("factCommitment", t(&sha('0'))),
        ("coverageCommitment", t(&sha('0'))),
    ] {
        bad.push(with(
            &all,
            "stageResults",
            a(vec![with(&results[0], name, value), results[1].clone()]),
        ));
    }
    for value in bad {
        let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
        let seq = analyzing(&mut r, &c);
        worker(&mut r, "FactBatch", batch("stage-one", 0, 0), seq).unwrap();
        worker(&mut r, "CoverageV3", coverage(0), seq + 1).unwrap();
        worker(&mut r, "CoverageV3", coverage(1), seq + 2).unwrap();
        let before = r.totals();
        assert!(matches!(
            worker(&mut r, "Complete", value, seq + 3),
            Err(Rust3Refusal::Admission(_))
        ));
        assert_eq!(r.totals(), before);
    }
}
#[test]
fn rust3_receive_full_published_response_boundaries_refuse_atomically_and_latch() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let c = context(false);
    assert_eq!(
        get(get(&c.hello, "limits"), "maxCandidateSpoolBytes"),
        &u(1_073_741_824)
    );
    assert_eq!(
        get(get(&c.hello, "limits"), "maxResponseFrames"),
        &u(1_000_000)
    );
    assert_eq!(
        get(get(&c.hello, "limits"), "maxFactCandidatesTotal"),
        &u(1_000_000)
    );
    let spool = cbor::encode(&m(&[
        ("analysisOrdinal", u(7)),
        ("stageId", t("stage-one")),
        ("candidate", candidate(0)),
    ]))
    .len() as u64;
    for cause in ["frames", "candidates", "spool", "payload"] {
        let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
        let seq = analyzing(&mut r, &c);
        let frame = received("FactBatch", batch("stage-one", 0, 0), seq);
        let mut totals = r.totals();
        match cause {
            "frames" => totals.frames = 1_000_000,
            "candidates" => totals.candidates = 1_000_000,
            "spool" => totals.spool_bytes = 1_073_741_824 - spool + 1,
            "payload" => totals.payload_bytes = 1_073_741_824 - frame.payload().len() as u64 + 1,
            _ => unreachable!(),
        };
        r.accounting.seed_totals_for_test(totals);
        let error = r.receive(frame).unwrap_err();
        assert!(
            matches!(error,Rust3Refusal::Admission(ref s)if s.starts_with("response safety:")),
            "{cause}: {error:?}"
        );
        assert_eq!(r.totals(), totals);
        assert!(r.retained.is_empty());
        assert!(matches!(
            worker(&mut r, "FactBatch", batch("stage-one", 0, 0), seq),
            Err(Rust3Refusal::AfterRefusal)
        ));
    }
    for last in ["frames", "candidates", "spool"] {
        let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
        let seq = analyzing(&mut r, &c);
        let mut totals = r.totals();
        match last {
            "frames" => totals.frames = 999_999,
            "candidates" => totals.candidates = 999_999,
            "spool" => totals.spool_bytes = 1_073_741_824 - spool,
            _ => unreachable!(),
        };
        r.accounting.seed_totals_for_test(totals);
        worker(&mut r, "FactBatch", batch("stage-one", 0, 0), seq).unwrap();
        let after = r.totals();
        assert!(
            after.frames == 1_000_000
                || after.candidates == 1_000_000
                || after.spool_bytes == 1_073_741_824
        );
    }
    let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
    let mut totals = r.totals();
    totals.payload_bytes = 1_073_741_824 - 8;
    r.accounting.seed_totals_for_test(totals);
    let prefix = 9u64.to_be_bytes();
    assert!(
        matches!(r.read(&mut prefix.as_slice()),Err(Rust3Refusal::Transport(s))if s.contains("Oversize(9)")),
        "remaining aggregate must be judged at the 8-byte prefix before digest/payload allocation"
    );
    assert_eq!(r.totals(), totals);
}
#[test]
fn rust3_receive_stage_batch_and_candidate_arithmetic_is_checked_without_partial_update() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let c = context(false);
    for counter in ["batch", "candidate"] {
        let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
        let seq = analyzing(&mut r, &c);
        let value = if counter == "batch" {
            r.live[0].batches = u64::MAX;
            batch("stage-one", u64::MAX, 0)
        } else {
            r.live[0].next_candidate = u64::MAX;
            batch("stage-one", 0, u64::MAX)
        };
        let before = (r.live[0].batches, r.live[0].next_candidate);
        let error = worker(&mut r, "FactBatch", value, seq).unwrap_err();
        assert!(matches!(error,Rust3Refusal::Admission(s)if s.contains("overflow")));
        assert_eq!((r.live[0].batches, r.live[0].next_candidate), before);
        assert_eq!(r.totals().candidates, 0);
    }
    let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
    let seq = analyzing(&mut r, &c);
    worker(&mut r, "FactBatch", batch("stage-one", 0, 0), seq).unwrap();
    assert!(
        matches!(
            worker(&mut r, "FactBatch", batch("stage-one", 0, 0), seq + 1),
            Err(Rust3Refusal::Admission(_))
        ),
        "a second frame cannot repeat an admitted batch"
    );
}
#[test]
fn rust3_receive_full_fact_batch_count_boundary_and_outer_schema_refusals() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let c = context(false);
    for count in [0, 4096, 4097] {
        let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
        let seq = analyzing(&mut r, &c);
        let value = with(
            &batch("stage-one", 0, 0),
            "candidates",
            a((0..count).map(candidate).collect()),
        );
        let got = worker(&mut r, "FactBatch", value, seq);
        if count == 4096 {
            let got = got.unwrap();
            assert_eq!(got.spool_entries.len(), 4096);
            assert_eq!(r.totals().candidates, 4096);
        } else {
            assert!(matches!(got, Err(Rust3Refusal::Schema(_))));
            assert_eq!(r.totals().candidates, 0);
        }
    }
}
#[test]
fn rust3_receive_legal_wire_above_escaped_json_cap_reaches_the_generated_universe() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let mut c = context(false);
    let universe = get(&c.open_universe, "universe");
    let wide = with(
        universe,
        "standardLibraryComponentDigests",
        Value::Map(vec![("\0".repeat(700000), t(&h('a')))]),
    );
    c.open_universe = with(&c.open_universe, "universe", wide);
    let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
    r.sent(Rust3HostFrame::Hello).unwrap();
    worker(&mut r, "HelloAck", ack(&c), 0).unwrap();
    r.sent(Rust3HostFrame::OpenUniverse).unwrap();
    let got = worker(&mut r, "UniverseAccepted", accepted(&c), 1).unwrap();
    let Rust3ProviderFrameV3Payload::UniverseAccepted(value) = got.payload else {
        panic!("universe carrier")
    };
    assert_eq!(value.universe.standard_library_component_digests.len(), 1);
    assert_eq!(
        value
            .universe
            .standard_library_component_digests
            .keys()
            .next()
            .unwrap()
            .len(),
        700000
    );
}
fn two_key_context() -> Rust3DispatchContext {
    let mut c = context(false);
    c.target_domain.insert(sha('7'));
    let domain = &c.stages[0].analysis_domain;
    let Value::Array(mut keys) = get(domain, "requestedCoverageDomain").clone() else {
        panic!("keys")
    };
    keys.push(with(
        &with(&keys[0], "targetUniverseId", t(&sha('7'))),
        "subjectScopeCommitment",
        t(&sha('e')),
    ));
    c.stages[0].analysis_domain = with(domain, "requestedCoverageDomain", a(keys));
    c
}
fn two_key_entries(deficiency: Option<&str>) -> Vec<Vec<Value>> {
    let mut second = key(0);
    second.target_universe_id = sha('7');
    second.subject_scope_commitment = sha('e');
    let coverage = if deficiency.is_some() {
        "unknown"
    } else {
        "complete"
    };
    let d = deficiency.map(t).unwrap_or(Value::Null);
    vec![
        vec![
            entry(&key(0), coverage, d.clone()),
            entry(&second, coverage, d.clone()),
        ],
        vec![entry(&key(1), coverage, d)],
    ]
}
fn two_key_coverage() -> Value {
    let entries = a(two_key_entries(None).remove(0));
    with(
        &with(&coverage(0), "entries", entries.clone()),
        "coverageCommitment",
        t(&built("opensip.rust-provider.stage-coverage.v2", &entries)),
    )
}
fn two_key_complete() -> Value {
    let value = complete(&[vec![candidate(0), candidate(1)], vec![]]);
    let Value::Array(mut results) = get(&value, "stageResults").clone() else {
        panic!("results")
    };
    let entries = two_key_entries(None);
    results[0] = with(
        &with(&results[0], "coverageEntryCount", u(2)),
        "coverageCommitment",
        t(&built(
            "opensip.rust-provider.stage-coverage.v2",
            &a(entries[0].clone()),
        )),
    );
    let all = a(entries.into_iter().flatten().collect());
    with(
        &with(&value, "stageResults", a(results)),
        "coverageStreamCommitment",
        t(&built("opensip.rust-provider.coverage-stream.v2", &all)),
    )
}
fn two_key_ready(r: &mut Rust3Receiver<'_>, c: &Rust3DispatchContext) -> u64 {
    let seq = analyzing(r, c);
    worker(
        r,
        "FactBatch",
        with(
            &batch("stage-one", 0, 0),
            "candidates",
            a(vec![candidate(0), candidate(1)]),
        ),
        seq,
    )
    .unwrap();
    worker(r, "CoverageV3", two_key_coverage(), seq + 1).unwrap();
    worker(r, "CoverageV3", coverage(1), seq + 2).unwrap();
    seq + 3
}
fn reversed(values: &Value) -> Value {
    let Value::Array(mut values) = values.clone() else {
        panic!("array")
    };
    assert!(values.len() > 1);
    values.reverse();
    a(values)
}
#[test]
fn rust3_receive_every_commitment_row_refuses_domain_class_and_preimage_order_swaps() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let c = two_key_context();
    let facts = a(vec![candidate(0), candidate(1)]);
    let coverage_entries = two_key_entries(None);
    let stage_entries = a(coverage_entries[0].clone());
    let all_entries = a(coverage_entries.into_iter().flatten().collect());
    let valid_complete = two_key_complete();
    let Value::Array(results) = get(&valid_complete, "stageResults").clone() else {
        panic!("results")
    };
    let mut positive = Rust3Receiver::new(&table, c.clone()).unwrap();
    let seq = two_key_ready(&mut positive, &c);
    worker(&mut positive, "Complete", valid_complete.clone(), seq).unwrap();
    for (stage, field_name, domain, wrong_domain, values, wrong_class) in [
        (
            true,
            "factCommitment",
            "opensip.rust-provider.stage-facts.v2",
            "opensip.rust-provider.stage-coverage.v2",
            facts.clone(),
            stage_entries.clone(),
        ),
        (
            true,
            "coverageCommitment",
            "opensip.rust-provider.stage-coverage.v2",
            "opensip.rust-provider.stage-facts.v2",
            stage_entries.clone(),
            facts.clone(),
        ),
        (
            false,
            "factStreamCommitment",
            "opensip.rust-provider.fact-stream.v2",
            "opensip.rust-provider.coverage-stream.v2",
            facts.clone(),
            all_entries.clone(),
        ),
        (
            false,
            "coverageStreamCommitment",
            "opensip.rust-provider.coverage-stream.v2",
            "opensip.rust-provider.fact-stream.v2",
            all_entries.clone(),
            facts.clone(),
        ),
    ] {
        for bad_hash in [
            built(wrong_domain, &values),
            built(domain, &wrong_class),
            built(domain, &reversed(&values)),
        ] {
            let bad = if stage {
                let mut changed = results.clone();
                changed[0] = with(&changed[0], field_name, t(&bad_hash));
                with(&valid_complete, "stageResults", a(changed))
            } else {
                with(&valid_complete, field_name, t(&bad_hash))
            };
            let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
            let seq = two_key_ready(&mut r, &c);
            let before = r.totals();
            assert!(
                matches!(
                    worker(&mut r, "Complete", bad, seq),
                    Err(Rust3Refusal::Admission(_))
                ),
                "{field_name}: domain/value-class/order swap must refuse"
            );
            assert_eq!(r.totals(), before);
        }
    }
    for (frame, valid, domain, values) in {
        let unavailable_entries = a(two_key_entries(Some("provider-unavailable"))
            .into_iter()
            .flatten()
            .collect());
        let unavailable = m(&[
            ("analysisOrdinal", u(7)),
            ("affectedStageIds", a(vec![t("stage-one"), t("stage-two")])),
            ("reason", t("dependency-source-incomplete")),
            (
                "coverageCommitment",
                t(&built(
                    "opensip.rust-provider.coverage-stream.v2",
                    &unavailable_entries,
                )),
            ),
            ("coverage", unavailable_entries.clone()),
        ]);
        let budget_entries = a(two_key_entries(Some("budget-exhausted"))
            .into_iter()
            .flatten()
            .collect());
        let spent = with(
            &with(&budget(), "coverage", budget_entries.clone()),
            "coverageCommitment",
            t(&built(
                "opensip.rust-provider.coverage-stream.v2",
                &budget_entries,
            )),
        );
        [
            (
                "CoverageV3",
                two_key_coverage(),
                "opensip.rust-provider.stage-coverage.v2",
                stage_entries,
            ),
            (
                "Unavailable",
                unavailable,
                "opensip.rust-provider.coverage-stream.v2",
                unavailable_entries,
            ),
            (
                "BudgetExhausted",
                spent,
                "opensip.rust-provider.coverage-stream.v2",
                budget_entries,
            ),
        ]
    } {
        // Each terminal's untouched positive has the same multi-key cardinality.
        let mut positive = Rust3Receiver::new(&table, c.clone()).unwrap();
        let seq = analyzing(&mut positive, &c);
        worker(&mut positive, frame, valid.clone(), seq).unwrap();
        for bad_hash in [
            built("opensip.rust-provider.stage-facts.v2", &values),
            built(domain, &facts),
            built(domain, &reversed(&values)),
        ] {
            let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
            let seq = analyzing(&mut r, &c);
            let before = r.totals();
            assert!(
                matches!(
                    worker(
                        &mut r,
                        frame,
                        with(&valid, "coverageCommitment", t(&bad_hash)),
                        seq
                    ),
                    Err(Rust3Refusal::Admission(_))
                ),
                "{frame}: domain/value-class/order swap must refuse"
            );
            assert_eq!(r.totals(), before);
        }
    }
}
