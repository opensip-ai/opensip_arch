//! Synthetic wire/context controls. Returned symbol scopes remain pending H;
//! neither a Plan capability nor a native subject inventory is admitted here.
use super::*;
use opensip_contracts::generated::protocol::SymbolCensus1SymbolCensusV1 as Census;
fn closure() -> String {
    format!("closure2:{}", h('1'))
}
fn census_context() -> Rust3DispatchContext {
    let mut c = context(false);
    c.symbol_census = Some(closure());
    let mut tokens = Vec::from(TOKENS);
    tokens.push("symbol-census-v1");
    tokens.sort();
    c.hello = with(
        &c.hello,
        "expectedCapabilities",
        a(tokens.into_iter().map(t).collect()),
    );
    for stage in &mut c.stages {
        let Value::Array(mut keys) = get(&stage.analysis_domain, "requestedCoverageDomain").clone()
        else {
            panic!()
        };
        for key in &mut keys {
            let suffix = |name| {
                text_of(map_of(key).unwrap(), name)
                    .unwrap()
                    .strip_prefix("sha256:")
                    .unwrap()
                    .to_owned()
            };
            let descriptor = m(&[
                ("schemaVersion", u(2)),
                ("snapshotId", t(&snapshot())),
                ("sourceUniverse", t(&suffix("sourceUniverseId"))),
                ("targetUniverse", t(&suffix("targetUniverseId"))),
                ("relation", get(key, "relation").clone()),
                ("resolution", get(key, "resolution").clone()),
                ("enumeratorClosure", t(&closure())),
                ("subjects", a(vec![])),
            ]);
            let id = opensip_identity::hash_canonical_value(
                "subject-scope",
                &carrier::to_json(&descriptor).unwrap(),
            )
            .unwrap();
            *key = with(
                key,
                "subjectScopeCommitment",
                t(&format!("sha256:{}", digest_hex(&id))),
            );
        }
        stage.analysis_domain = with(&stage.analysis_domain, "requestedCoverageDomain", a(keys));
    }
    c
}
fn row(index: u64) -> Value {
    m(&[
        ("nativeSubjectId", t(&format!("rust-symbol:{index:05}"))),
        ("path", t("src/a.rs")),
        ("qualifiedName", t("item")),
        ("exported", t("unknown")),
        ("signatureTokens", a(vec![])),
    ])
}
fn full(rows: Vec<Value>) -> Value {
    m(&[
        ("state", t("complete")),
        ("examinedPaths", a(vec![t("src/a.rs")])),
        ("rows", a(rows)),
    ])
}
fn over(rows: u64, paths: u64) -> Value {
    m(&[
        ("state", t("over-bound")),
        ("rowCount", u(rows)),
        ("examinedPathCount", u(paths)),
    ])
}
fn ready(r: &mut Rust3Receiver<'_>, c: &Rust3DispatchContext) -> u64 {
    let seq = analyzing(r, c);
    // These unchanged symbol entries deliberately retain their arbitrary
    // fixture scopes. D2b must preserve them for H, not decide their truth.
    worker(r, "CoverageV3", coverage(0), seq).unwrap();
    worker(r, "CoverageV3", coverage(1), seq + 1).unwrap();
    seq + 2
}
#[test]
fn census_complete_and_over_bound_are_typed_and_move_original_complete_to_h_once() {
    let table = Table::load(Protocol::Rust3).unwrap();
    for census in [
        full(vec![]),
        full(vec![row(1)]),
        over(100_001, 0),
        over(0, 100_001),
    ] {
        let c = census_context();
        let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
        let seq = ready(&mut r, &c);
        let frame = received(
            "Complete",
            with(&complete(&[vec![], vec![]]), "symbolCensus", census.clone()),
            seq,
        );
        let ptr = frame.payload().as_ptr();
        let got = r.receive(frame).unwrap();
        assert!(matches!(
            got.payload,
            Rust3ProviderFrameV3Payload::Complete(_)
        ));
        assert!(matches!(
            got.census,
            Some(Census::CompleteSymbolCensusV1(_)) | Some(Census::OverBoundSymbolCensusV1(_))
        ));
        assert!(r.take_candidate_spool().is_none());
        r.process(ProcessEvent::ZeroExit).unwrap();
        r.process(ProcessEvent::Eof).unwrap();
        let frames: Vec<_> = r.take_candidate_spool().unwrap().collect();
        assert_eq!(frames.len(), 3);
        assert_eq!(frames.last().unwrap().as_ptr(), ptr);
        let last = cbor::decode(
            frames.last().unwrap(),
            cbor::Profile::Rust3,
            RUST3_FRAME_MAX_DEPTH,
        )
        .unwrap();
        assert_eq!(
            cbor::encode(get(get(&last, "payload"), "symbolCensus")),
            cbor::encode(&census)
        );
        assert!(r.take_candidate_spool().is_none());
    }
}
#[test]
fn census_return_null_order_uniqueness_membership_and_impossible_over_bound_refuse() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let outside = with(&row(1), "path", t("src/other.rs"));
    let cases = [
        Value::Null,
        full(vec![row(2), row(1)]),
        full(vec![row(1), row(1)]),
        full(vec![outside]),
        with(
            &full(vec![]),
            "examinedPaths",
            a(vec![t("b.rs"), t("a.rs")]),
        ),
        with(
            &full(vec![]),
            "examinedPaths",
            a(vec![t("src/a.rs"), t("src/a.rs")]),
        ),
        over(0, 0),
    ];
    for census in cases {
        let c = census_context();
        let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
        let seq = ready(&mut r, &c);
        assert!(
            worker(
                &mut r,
                "Complete",
                with(&complete(&[vec![], vec![]]), "symbolCensus", census),
                seq
            )
            .is_err()
        );
        assert!(r.take_candidate_spool().is_none());
    }
}
#[test]
fn census_selected_token_requires_complete_v3_and_unoffered_census_is_not_accepted() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let c = census_context();
    let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
    let seq = ready(&mut r, &c);
    assert!(matches!(
        worker(&mut r, "Complete", complete(&[vec![], vec![]]), seq),
        Err(Rust3Refusal::Schema(_))
    ));
    let c = context(false);
    let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
    let seq = analyzing(&mut r, &c);
    worker(&mut r, "CoverageV3", coverage(0), seq).unwrap();
    worker(&mut r, "CoverageV3", coverage(1), seq + 1).unwrap();
    assert!(matches!(
        worker(
            &mut r,
            "Complete",
            with(&complete(&[vec![], vec![]]), "symbolCensus", full(vec![])),
            seq + 2
        ),
        Err(Rust3Refusal::Schema(_))
    ));
}
#[test]
fn census_complete_raw_byte_bound_is_checked_without_borrowed_json_limit() {
    let table = Table::load(Protocol::Rust3).unwrap();
    // One legal row has about1MiB CBOR but over6MiB JSON escaping. It must
    // use the existing structured evaluator rather than a JSON-byte cap.
    let dense = |index| {
        with(
            &row(index),
            "signatureTokens",
            a(vec![t(&"\0".repeat(4096)); 256]),
        )
    };
    for (rows, allowed) in [
        (vec![dense(1)], true),
        ((1..=5).map(dense).collect(), false),
    ] {
        let census = full(rows);
        let size = cbor::encode(&census).len();
        assert_eq!(size <= 4_194_304, allowed);
        let c = census_context();
        let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
        let seq = ready(&mut r, &c);
        let result = worker(
            &mut r,
            "Complete",
            with(&complete(&[vec![], vec![]]), "symbolCensus", census),
            seq,
        );
        if allowed {
            assert!(
                result.is_ok(),
                "legal received census rejected: {:?}",
                result.err()
            );
        } else {
            assert!(
                matches!(result, Err(Rust3Refusal::Admission(_))),
                "over-bound complete must fail received-byte admission"
            );
        }
    }
}

#[test]
fn census_each_optional_token_mismatch_refuses_at_hello_before_open_or_source() {
    let table = Table::load(Protocol::Rust3).unwrap();
    for (bit, token) in [
        (1, "symbol-census-v1"),
        (2, "subject-scope-reference-v1"),
        (4, "target-attribution-v2"),
    ] {
        for offered in [false, true] {
            let mask = if bit == 1 {
                u8::from(offered)
            } else {
                1 | if offered { bit } else { 0 }
            };
            let c = super::super::super::send::census_context_for_test(mask);
            let Value::Array(expected) = get(&c.hello, "expectedCapabilities").clone() else {
                panic!()
            };
            let mut actual = expected;
            actual.retain(|v| v != &t(token));
            if !offered {
                actual.push(t(token));
            }
            actual.sort_by(|a, b| match (a, b) {
                (Value::Text(a), Value::Text(b)) => a.as_bytes().cmp(b.as_bytes()),
                _ => panic!(),
            });
            let wrong = with(&ack(&c), "capabilities", a(actual));
            let mut r = Rust3Receiver::new(&table, c).unwrap();
            r.sent(Rust3HostFrame::Hello).unwrap();
            assert!(matches!(
                worker(&mut r, "HelloAck", wrong, 0),
                Err(Rust3Refusal::Admission(_))
            ));
            assert!(!r.admits(&Rust3HostFrame::OpenUniverse));
            assert_eq!(r.totals().frames, 0);
        }
    }
}
fn census_terminal_entries(c: &Rust3DispatchContext, deficiency: &str, count: u64) -> Value {
    a(c.stages
        .iter()
        .map(|s| {
            let key = get(&s.analysis_domain, "requestedCoverageDomain");
            let Value::Array(keys) = key else { panic!() };
            let k = &keys[0];
            let key = Key {
                relation: text_of(map_of(k).unwrap(), "relation").unwrap().into(),
                resolution: text_of(map_of(k).unwrap(), "resolution").unwrap().into(),
                source_universe_id: text_of(map_of(k).unwrap(), "sourceUniverseId")
                    .unwrap()
                    .into(),
                target_universe_id: text_of(map_of(k).unwrap(), "targetUniverseId")
                    .unwrap()
                    .into(),
                subject_scope_commitment: text_of(map_of(k).unwrap(), "subjectScopeCommitment")
                    .unwrap()
                    .into(),
            };
            let entry = entry(&key, "unknown", t(deficiency));
            let view = get(&entry, "entry");
            let examined = with(get(view, "examinedUniverse"), "subjectCount", u(count));
            with(&entry, "entry", with(view, "examinedUniverse", examined))
        })
        .collect())
}
#[test]
fn census_clean_budget_and_unavailable_keep_requested_d_empty_and_zero_count() {
    let table = Table::load(Protocol::Rust3).unwrap();
    for budget_case in [false, true] {
        for count in [0, 1] {
            let c = census_context();
            let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
            let seq = analyzing(&mut r, &c);
            let deficiency = if budget_case {
                "budget-exhausted"
            } else {
                "provider-unavailable"
            };
            let entries = census_terminal_entries(&c, deficiency, count);
            let payload = if budget_case {
                with(&budget(), "coverage", entries.clone())
            } else {
                m(&[
                    ("analysisOrdinal", u(7)),
                    ("affectedStageIds", a(vec![t("stage-one"), t("stage-two")])),
                    ("reason", t("dependency-source-incomplete")),
                    ("coverage", entries.clone()),
                ])
            };
            let payload = with(
                &payload,
                "coverageCommitment",
                t(&built("opensip.rust-provider.coverage-stream.v2", &entries)),
            );
            let result = worker(
                &mut r,
                if budget_case {
                    "BudgetExhausted"
                } else {
                    "Unavailable"
                },
                payload,
                seq,
            );
            if count == 0 {
                assert!(
                    result.is_ok(),
                    "clean symbol D-empty refusal: {:?}",
                    result.err()
                );
            } else {
                assert!(matches!(result, Err(Rust3Refusal::Admission(_))));
            }
        }
    }
}

#[test]
fn census_exact_received_four_mib_boundary_and_one_byte_over() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let maximum = 4_194_304_u64;
    let dense = |index| {
        with(
            &row(index),
            "signatureTokens",
            a(vec![t(&"\0".repeat(4096)); 256]),
        )
    };
    let mut rows = (1..=3).map(dense).collect::<Vec<_>>();
    let mut tokens = vec![t(&"\0".repeat(4096)); 255];
    tokens.push(t(""));
    rows.push(with(&row(4), "signatureTokens", a(tokens.clone())));
    let base = full(rows.clone());
    let length = cbor::encoded_length(&base).unwrap();
    let needed = maximum.checked_sub(length).unwrap();
    let padding = (0..=4096)
        .find(|n| cbor::encoded_length(&t(&"\0".repeat(*n))).unwrap() - 1 == needed)
        .expect("exact bound can be represented without changing any other field");
    for extra in [0, 1] {
        let mut tokens = tokens.clone();
        *tokens.last_mut().unwrap() = t(&"\0".repeat(padding + extra));
        let mut rows = rows.clone();
        rows[3] = with(&row(4), "signatureTokens", a(tokens));
        let census = full(rows);
        assert_eq!(cbor::encoded_length(&census), Some(maximum + extra as u64));
        let c = census_context();
        let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
        let seq = ready(&mut r, &c);
        let before = r.totals();
        let got = worker(
            &mut r,
            "Complete",
            with(&complete(&[vec![], vec![]]), "symbolCensus", census),
            seq,
        );
        if extra == 0 {
            assert!(got.is_ok(), "exact received4MiB census: {got:?}");
        } else {
            assert!(matches!(got, Err(Rust3Refusal::Admission(_))));
            assert_eq!(r.totals(), before);
            assert!(r.take_candidate_spool().is_none());
        }
    }
}
#[test]
fn census_examined_path_count_at_100000_and_one_over_at_actual_receive() {
    let table = Table::load(Protocol::Rust3).unwrap();
    for count in [100_000, 100_001] {
        let census = with(
            &full(vec![]),
            "examinedPaths",
            a((0..count).map(|i| t(&format!("p{i:06}"))).collect()),
        );
        assert!(cbor::encoded_length(&census).unwrap() < 4_194_304);
        let c = census_context();
        let mut r = Rust3Receiver::new(&table, c.clone()).unwrap();
        let seq = ready(&mut r, &c);
        let before = r.totals();
        let got = worker(
            &mut r,
            "Complete",
            with(&complete(&[vec![], vec![]]), "symbolCensus", census),
            seq,
        );
        if count == 100_000 {
            assert!(got.is_ok(), "path count at source bound: {got:?}");
        } else {
            assert!(matches!(got, Err(Rust3Refusal::Schema(_))));
            assert_eq!(r.totals(), before);
            assert!(r.take_candidate_spool().is_none());
        }
    }
}
#[test]
fn census_row_count_shape_boundary_is_separate_from_the_received_byte_bound() {
    let law = Law::load().unwrap();
    for count in [100_000, 100_001] {
        let census = full((0..count).map(row).collect());
        // This legal row cardinality exceeds4MiB even with these compact
        // values. Test the owning schema predicate directly, without
        // claiming that the complete received census would be admissible.
        assert!(cbor::encoded_length(&census).unwrap() > 4_194_304);
        let payload = with(&complete(&[vec![], vec![]]), "symbolCensus", census);
        let got = law.census.shape(&payload);
        assert_eq!(got.is_ok(), count == 100_000, "rows={count}: {got:?}");
        if let Err(e) = got {
            assert_eq!(e, "native.symbol-census-bound: rows");
        }
    }
}
