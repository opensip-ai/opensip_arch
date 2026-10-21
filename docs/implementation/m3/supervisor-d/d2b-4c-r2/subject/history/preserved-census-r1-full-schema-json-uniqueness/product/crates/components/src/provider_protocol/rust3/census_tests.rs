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
        assert_eq!(get(get(&last, "payload"), "symbolCensus"), &census);
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
