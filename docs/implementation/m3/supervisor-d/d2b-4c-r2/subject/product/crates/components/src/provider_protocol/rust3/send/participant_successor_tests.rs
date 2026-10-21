//! Full nonblocking participant composition over admitted-wire-shaped inert
//! projections. Original response buffers cross the DONE boundary once.
//! Native selection and returned census settlement still belong to C4/H.
use super::*;
fn plan(mask: u8) -> super::super::super::request::Plan {
    super::super::super::request::tests::census_plan(mask)
}
fn make<'t>(
    table: &'t Table,
    plan: super::super::super::request::Plan,
) -> (Rust3Participant<'t>, Rc<Cell<usize>>, Rust3DispatchContext) {
    let request = Request::build(plan).unwrap();
    let context = request.context.clone();
    let reads = Rc::new(Cell::new(0));
    let p = Rust3Participant::new(
        table,
        request,
        Box::new(Custody {
            reads: reads.clone(),
            fail: false,
        }),
    )
    .unwrap();
    (p, reads, context)
}
fn census(variant: u8) -> Value {
    match variant {
        0 | 1 => map(vec![
            ("state", t("complete")),
            ("examinedPaths", Value::Array(vec![t("src/a.rs")])),
            (
                "rows",
                Value::Array(if variant == 0 {
                    vec![]
                } else {
                    vec![map(vec![
                        ("nativeSubjectId", t("rust-symbol:item")),
                        ("path", t("src/a.rs")),
                        ("qualifiedName", t("item")),
                        ("exported", t("unknown")),
                        ("signatureTokens", Value::Array(vec![])),
                    ])]
                }),
            ),
        ]),
        2 | 3 => map(vec![
            ("state", t("over-bound")),
            ("rowCount", u(if variant == 2 { 100_001 } else { 0 })),
            (
                "examinedPathCount",
                u(if variant == 3 { 100_001 } else { 0 }),
            ),
        ]),
        _ => panic!(),
    }
}
fn responses(
    p: &mut Rust3Participant<'_>,
    c: &Rust3DispatchContext,
    mut seq: u64,
    mask: u8,
    census: Value,
    fact: bool,
) -> Vec<Vec<u8>> {
    let stage = get(&c.stages[0].plan_stage, "stageId").clone();
    let facts = Value::Array(if fact { vec![candidate(c)] } else { vec![] });
    let entries = coverage_entries(c, "complete", Value::Null);
    let mut raw = vec![];
    if fact {
        let mut fields = vec![
            ("analysisOrdinal", u(c.analysis_ordinal)),
            ("stageId", stage.clone()),
            ("batchIndex", u(0)),
            ("candidates", facts.clone()),
        ];
        if mask & 4 != 0 {
            fields.push(("schemaVersion", u(3)));
            fields.push(("occupancyCompanions", Value::Array(vec![])));
        }
        raw.push(feed(p, "FactBatch", map(fields), seq));
        seq += 1;
    }
    raw.push(feed(
        p,
        "CoverageV3",
        map(vec![
            ("analysisOrdinal", u(c.analysis_ordinal)),
            ("stageId", stage.clone()),
            ("entries", entries.clone()),
            (
                "coverageCommitment",
                t(&commitment(
                    "opensip.rust-provider.stage-coverage.v2",
                    &entries,
                )),
            ),
        ]),
        seq,
    ));
    seq += 1;
    let result = map(vec![
        ("stageId", stage),
        ("factCount", u(u64::from(fact))),
        ("coverageEntryCount", u(1)),
        (
            "factCommitment",
            t(&commitment("opensip.rust-provider.stage-facts.v2", &facts)),
        ),
        (
            "coverageCommitment",
            t(&commitment(
                "opensip.rust-provider.stage-coverage.v2",
                &entries,
            )),
        ),
    ]);
    let mut fields = vec![
        ("analysisOrdinal", u(c.analysis_ordinal)),
        ("stageResults", Value::Array(vec![result])),
        (
            "factStreamCommitment",
            t(&commitment("opensip.rust-provider.fact-stream.v2", &facts)),
        ),
        (
            "coverageStreamCommitment",
            t(&commitment(
                "opensip.rust-provider.coverage-stream.v2",
                &entries,
            )),
        ),
    ];
    if mask & 1 != 0 {
        fields.push(("symbolCensus", census));
    }
    raw.push(feed(p, "Complete", map(fields), seq));
    raw
}
fn take(p: &mut Rust3Participant<'_>, kind: TerminalKind, raw: Vec<Vec<u8>>) -> Vec<Vec<u8>> {
    assert!(p.take_terminal_output().is_none());
    let pointers = worker::original_buffer_addresses(&p.receiver);
    assert_eq!(pointers.len(), raw.len());
    assert_eq!(
        p.process(ProcessEvent::ZeroExit).status,
        ParticipantStatus::Terminal(kind)
    );
    assert!(p.take_terminal_output().is_none());
    let eof = p.readable(&mut io::empty());
    assert!(eof.eof);
    assert!(p.take_terminal_output().is_none());
    assert_eq!(p.process(ProcessEvent::Eof).status, ParticipantStatus::Done);
    let output = p.take_terminal_output().unwrap();
    assert_eq!(output.kind(), kind);
    let frames = output.into_spool().into_candidates();
    assert_eq!(
        frames
            .iter()
            .map(|b| (b.as_ptr() as usize, b.len()))
            .collect::<Vec<_>>(),
        pointers
    );
    assert_eq!(
        frames,
        raw.into_iter()
            .map(|v| v[FRAME_PREFIX_BYTES..].to_vec())
            .collect::<Vec<_>>()
    );
    assert!(p.take_terminal_output().is_none());
    frames
}
#[test]
fn successor_participant_all_eight_tokens_complete_and_over_bound_move_original_census_to_h() {
    let table = Table::load(Protocol::Rust3).unwrap();
    for mask in 0..8 {
        for variant in 0..if mask & 1 != 0 { 4 } else { 1 } {
            let (mut p, reads, c) = make(&table, plan(mask));
            assert_eq!(reads.get(), 0);
            let seq = analyzing(&mut p, &c, &reads);
            let census = census(variant);
            let raw = responses(&mut p, &c, seq, mask, census.clone(), true);
            let frames = take(&mut p, TerminalKind::Complete, raw);
            let complete = cbor::decode(
                frames.last().unwrap(),
                cbor::Profile::Rust3,
                super::super::super::super::RUST3_FRAME_MAX_DEPTH,
            )
            .unwrap();
            let payload = get(&complete, "payload");
            if mask & 1 != 0 {
                assert_eq!(
                    cbor::encode(get(payload, "symbolCensus")),
                    cbor::encode(&census)
                );
            } else {
                let Value::Map(fields) = payload else {
                    panic!()
                };
                assert!(!fields.iter().any(|(k, _)| k == "symbolCensus"));
            }
            assert_eq!(reads.get(), 3);
        }
    }
}
#[test]
fn successor_participant_unowed_census_stays_null_for_each_other_token_pair() {
    let table = Table::load(Protocol::Rust3).unwrap();
    for mask in [1, 3, 5, 7] {
        let (mut p, reads, c) = make(&table, unowed_plan(mask));
        let seq = analyzing(&mut p, &c, &reads);
        let raw = responses(&mut p, &c, seq, mask, Value::Null, false);
        let frames = take(&mut p, TerminalKind::Complete, raw);
        let complete = cbor::decode(
            frames.last().unwrap(),
            cbor::Profile::Rust3,
            super::super::super::super::RUST3_FRAME_MAX_DEPTH,
        )
        .unwrap();
        assert_eq!(get(get(&complete, "payload"), "symbolCensus"), &Value::Null);
    }
}
#[test]
fn successor_participant_clean_budget_and_unavailable_keep_d_empty_zero_counts() {
    let table = Table::load(Protocol::Rust3).unwrap();
    for mask in [1, 3, 5, 7] {
        for budget in [false, true] {
            for count in [0, 1] {
                let mut plan = plan(mask);
                if budget {
                    let Value::Map(stage) = &mut plan.stages[0].plan_stage else {
                        panic!()
                    };
                    stage.push((
                        "budget".into(),
                        map(vec![("unit", t("items")), ("limit", u(10))]),
                    ));
                }
                let (mut p, reads, c) = make(&table, plan);
                let seq = analyzing(&mut p, &c, &reads);
                let deficiency = if budget {
                    "budget-exhausted"
                } else {
                    "provider-unavailable"
                };
                let mut entries = coverage_entries(&c, "unknown", t(deficiency));
                let Value::Array(rows) = &mut entries else {
                    panic!()
                };
                for row in rows {
                    let mut inner = get(row, "entry").clone();
                    let mut examined = get(&inner, "examinedUniverse").clone();
                    replace(&mut examined, "subjectCount", u(count));
                    replace(&mut inner, "examinedUniverse", examined);
                    replace(row, "entry", inner);
                }
                let mut fields = vec![
                    ("analysisOrdinal", u(c.analysis_ordinal)),
                    ("coverage", entries.clone()),
                    (
                        "coverageCommitment",
                        t(&commitment(
                            "opensip.rust-provider.coverage-stream.v2",
                            &entries,
                        )),
                    ),
                ];
                let (name, kind) = if budget {
                    fields.extend([
                        (
                            "triggerStageId",
                            get(&c.stages[0].plan_stage, "stageId").clone(),
                        ),
                        ("unit", t("items")),
                        ("limit", u(10)),
                        ("observed", u(11)),
                    ]);
                    ("BudgetExhausted", TerminalKind::BudgetExhausted)
                } else {
                    fields.extend([
                        (
                            "affectedStageIds",
                            Value::Array(vec![get(&c.stages[0].plan_stage, "stageId").clone()]),
                        ),
                        ("reason", t("semantic-universe-incomplete")),
                    ]);
                    ("Unavailable", TerminalKind::Unavailable)
                };
                if count == 0 {
                    let raw = feed(&mut p, name, map(fields), seq);
                    take(&mut p, kind, vec![raw]);
                } else {
                    let bytes = wire(name, map(fields), seq);
                    assert_eq!(
                        p.readable(&mut bytes.as_slice()).status,
                        ParticipantStatus::Fault
                    );
                    assert!(p.take_terminal_output().is_none());
                    assert!(worker::original_buffer_addresses(&p.receiver).is_empty());
                }
            }
        }
    }
}
#[test]
fn successor_participant_cancel_finishes_pending_analyze_before_one_exact_echo() {
    let table = Table::load(Protocol::Rust3).unwrap();
    for mask in 0..8 {
        let (mut p, reads, c) = make(&table, plan(mask));
        let seq = before_context(&mut p, &c, &reads);
        feed(&mut p, "NativeContextVerified", worker::native(&c), seq);
        assert_eq!(
            p.pending_frame,
            Some(super::super::super::super::Rust3HostFrame::Analyze)
        );
        let mut writer = Writer {
            bytes: vec![],
            calls: 0,
            maximum: 5,
        };
        p.writable(&mut writer);
        assert_eq!(p.at, 5);
        assert!(p.cancel());
        assert!(!p.cancel());
        let mut written = 0;
        while p.wants_write() {
            let step = p.writable(&mut writer);
            assert!(!matches!(
                step.status,
                ParticipantStatus::Fault | ParticipantStatus::HostFault
            ));
            written += usize::from(step.cancel.written);
        }
        assert_eq!(written, 1);
        assert!(p.closed);
        assert_eq!(reads.get(), 3);
        let mut bytes = writer.bytes.as_slice();
        let mut names = vec![];
        while let Some(frame) = super::super::super::super::super::read_frame(
            &mut bytes,
            Profile::Rust3,
            super::super::super::super::RUST3_FRAME_MAX_DEPTH,
            None,
        )
        .unwrap()
        {
            let envelope = frame.value();
            let name = get(envelope, "frameType");
            names.push(name.clone());
            if name == &t("Cancel") {
                let payload = get(envelope, "payload");
                assert_eq!(
                    get(payload, "executionId"),
                    get(&c.open_universe, "executionId")
                );
                assert_eq!(get(payload, "analysisOrdinal"), &u(c.analysis_ordinal));
            }
        }
        assert_eq!(names, [t("Analyze"), t("Cancel")]);
        assert!(!p.cancel());
        assert!(p.take_terminal_output().is_none());
    }
}
#[test]
fn successor_participant_input_rejected_fault_is_admitted_in_all_eight_variants() {
    let table = Table::load(Protocol::Rust3).unwrap();
    for mask in 0..8 {
        let (mut p, reads, c) = make(&table, plan(mask));
        let seq = analyzing(&mut p, &c, &reads);
        let payload = map(vec![
            ("executionId", get(&c.open_universe, "executionId").clone()),
            ("analysisOrdinal", u(c.analysis_ordinal)),
            ("phase", t("ANALYZING")),
            ("faultKind", t("input-rejected")),
            ("detailCode", t("diagnostic-only")),
        ]);
        let raw = wire("ProviderFault", payload, seq);
        // A successfully admitted typed fault normalizes to the supervisor's
        // provider-protocol outcome; it is not a malformed-frame refusal.
        assert_eq!(
            p.readable(&mut raw.as_slice()).status,
            ParticipantStatus::Fault
        );
        assert!(!p.protocol_fault && !p.host_fault);
        assert_eq!(p.receiver.terminal_kind(), Some("provider-fault"));
        assert_eq!(p.phase(), "WAIT_ZERO_EXIT");
        assert!(p.take_terminal_output().is_none());
        let before = p.receiver.totals();
        assert_eq!(before.frames, seq + 1);
        assert!(!raw.is_empty());
    }
}

fn unowed_plan(mask: u8) -> super::super::super::request::Plan {
    let mut p = plan(mask);
    p.symbol_census = None;
    replace(
        &mut p.stages[0].plan_stage,
        "relations",
        Value::Array(vec![t("file")]),
    );
    let cell = &mut p.stages[0].scopes[0];
    cell.relation = "file".into();
    cell.resolution = "enumerated".into();
    cell.target = cell.source.clone();
    cell.commitment = format!("sha256:{}", "f".repeat(64));
    p
}
#[test]
fn successor_participant_census_token_never_defers_nonsymbol_counts_or_scope() {
    let table = Table::load(Protocol::Rust3).unwrap();
    for mask in [1, 3, 5, 7] {
        for fault in ["count", "scope"] {
            let (mut p, reads, c) = make(&table, unowed_plan(mask));
            let seq = analyzing(&mut p, &c, &reads);
            let mut entries = coverage_entries(&c, "complete", Value::Null);
            let Value::Array(rows) = &mut entries else {
                panic!()
            };
            let mut inner = get(&rows[0], "entry").clone();
            let mut examined = get(&inner, "examinedUniverse").clone();
            if fault == "count" {
                replace(&mut examined, "subjectCount", u(0));
            } else {
                replace(
                    &mut examined,
                    "subjectScopeCommitment",
                    t(&format!("sha256:{}", "e".repeat(64))),
                );
            }
            replace(&mut inner, "examinedUniverse", examined);
            replace(&mut rows[0], "entry", inner);
            let payload = map(vec![
                ("analysisOrdinal", u(c.analysis_ordinal)),
                ("stageId", get(&c.stages[0].plan_stage, "stageId").clone()),
                ("entries", entries.clone()),
                (
                    "coverageCommitment",
                    t(&commitment(
                        "opensip.rust-provider.stage-coverage.v2",
                        &entries,
                    )),
                ),
            ]);
            let before = p.receiver.totals();
            let bytes = wire("CoverageV3", payload, seq);
            assert_eq!(
                p.readable(&mut bytes.as_slice()).status,
                ParticipantStatus::Fault,
                "mask={mask} {fault}"
            );
            assert_eq!(p.receiver.totals(), before);
            assert!(p.take_terminal_output().is_none());
            assert!(worker::original_buffer_addresses(&p.receiver).is_empty());
        }
    }
}
