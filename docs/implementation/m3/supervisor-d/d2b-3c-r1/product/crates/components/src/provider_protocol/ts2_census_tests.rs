// Unit D2b-3c's controls (section 4's RF-3 FA-2 controls and the successors'
// vectors, for TS2; D2b-T4 and D2b-T5):
// - FA-2's vectors, vendored and hash-pinned, and their recipes reproduced;
// - the census request: the token, the owed census, the symbol-kind keys and
//   their D∅ commitments against the Plan;
// - both payload mismatch directions, on Analyze and on Complete;
// - the census's admission: complete and over-bound, each bound one over and
//   at the bound, misordered, duplicate and off-extent rows, a wrongly null
//   census, and an over-bound census within every bound;
// - Coverage under a census, and the terminals;
// - the handoff to H: the spool carries exactly the received census and
//   entries;
// - D2b-T4: each HelloAck echo mismatch refused before any source byte;
// - D2b-T5: every TS2 commitmentMap row recomputed over received bytes;
// - the depth bound recomputed with FA-2's payloads.
use super::*;

const FA2_VECTORS: &[u8] = include_bytes!("../../tests/data/fa2-vectors.v1.json");
/// SHA-256 of `docs/implementation/m3/native-successors-fa/fa-2/evidence/vectors.json`.
const FA2_VECTORS_SHA256: &str = "6bc14639bef0d6095ceb6c57f317f17b239869f51204e50489ce2087fe9cf7d3";

fn vectors() -> J {
    assert_eq!(
        hex(&raw_sha256(FA2_VECTORS)),
        FA2_VECTORS_SHA256,
        "the vendored FA-2 vectors"
    );
    parse_json(FA2_VECTORS).unwrap()
}
fn js(v: &J, keys: &[&str]) -> String {
    match path(v, keys) {
        Some(J::String(s)) => s.clone(),
        other => panic!("{keys:?}: {other:?}"),
    }
}
/// The §4.1a commitment of a descriptor: `"sha256:"` + hex(H("subject-scope", D)).
fn scope_commitment(d: &J) -> String {
    format!(
        "sha256:{}",
        hex(&hash_canonical_value("subject-scope", d).unwrap())
    )
}

/// The TS example's values (FA-2 vectors `typescriptExample`).
fn example() -> J {
    path(&vectors(), &["typescriptExample"]).unwrap().clone()
}
fn census_key(relation: &str, resolution: &str, commitment: &str) -> RequestedKey {
    let u = format!("sha256:{}", js(&example(), &["universe"]));
    RequestedKey {
        relation: relation.to_owned(),
        resolution: resolution.to_owned(),
        source_universe_id: u.clone(),
        target_universe_id: u,
        subject_scope_commitment: commitment.to_owned(),
    }
}
/// A census session: FA-2's example snapshot, universe and enumerator; one
/// stage with its two symbol-kind keys (imports, references) at their D∅
/// commitments, and one with a source-path key.
fn census_plan() -> Ts2Plan {
    let x = example();
    let keys = match path(&x, &["keys"]) {
        Some(J::Array(k)) => k.clone(),
        _ => panic!("keys"),
    };
    let mut p = plan();
    p.capabilities.push("symbol-census-v1".to_owned());
    p.capabilities.sort();
    p.snapshot_id = js(&x, &["snapshotId"]);
    p.symbol_census = Some(js(&x, &["enumeratorClosure"]));
    p.stages[0].relations = vec!["imports".to_owned(), "references".to_owned()];
    p.stages[0].keys = keys
        .iter()
        .map(|k| {
            census_key(
                &js(k, &["relation"]),
                &js(k, &["resolution"]),
                &js(k, &["requestCommitment"]),
            )
        })
        .collect();
    p.stages[1].relations = vec!["file".to_owned()];
    p.stages[1].keys = vec![census_key("file", "enumerated", &sha('d'))];
    p
}
/// FA-2's example census, as the worker sends it.
fn example_census() -> Value {
    json_value(path(&example(), &["completeSymbolCensus"]).unwrap())
}
fn json_value(j: &J) -> Value {
    match j {
        J::Null => Value::Null,
        J::Bool(b) => Value::Bool(*b),
        J::Integer(i) => u(u64::try_from(i.get()).unwrap()),
        J::String(s) => t(s),
        J::Array(a) => Value::Array(a.iter().map(json_value).collect()),
        J::Object(o) => Value::Map(o.iter().map(|(k, v)| (k.clone(), json_value(v))).collect()),
    }
}
/// One stage's Coverage, its entries departing as `departure` says for the
/// symbol-kind keys: (subjectScopeCommitment, subjectCount).
fn entries_for(c: &DispatchContext, stage: usize, departure: Option<(&str, u64)>) -> Vec<Value> {
    c.stages[stage]
        .keys
        .iter()
        .map(|k| {
            let e = entry(k, "complete", Value::Null);
            let symbol = k.relation != "file";
            match departure {
                Some((commitment, count)) if symbol => {
                    let key = with(get(&e, "key"), "subjectScopeCommitment", t(commitment));
                    let inner = get(&e, "entry");
                    let examined = m(&[
                        ("subjectScopeCommitment", t(commitment)),
                        ("subjectCount", u(count)),
                    ]);
                    with(
                        &with(&e, "key", key),
                        "entry",
                        with(inner, "examinedUniverse", examined),
                    )
                }
                _ => e,
            }
        })
        .collect()
}
fn coverage_of(c: &DispatchContext, stage: usize, entries: &[Value]) -> Value {
    m(&[
        ("analysisOrdinal", u(0)),
        ("stageId", t(&c.stages[stage].expected_stage_id)),
        (
            "coverageCommitment",
            t(&built_commitment(
                "opensip.ts-provider.stage-coverage.v1",
                &a(entries.to_vec()),
            )),
        ),
        ("entries", a(entries.to_vec())),
    ])
}
/// Complete over no facts and these stages' entries, with `census` added
/// (TypeScriptCompleteV2) unless it is `None`.
fn complete_of(c: &DispatchContext, entries: &[Vec<Value>], census: Option<Value>) -> Value {
    let mut results = Vec::new();
    let mut all = Vec::new();
    for (s, e) in c.stages.iter().zip(entries) {
        results.push(m(&[
            ("stageId", t(&s.expected_stage_id)),
            ("stageOrdinal", u(s.stage_ordinal)),
            ("factBatchCount", u(0)),
            ("factCount", u(0)),
            ("coverageEntryCount", u(e.len() as u64)),
            (
                "factCommitment",
                t(&built_commitment(
                    "opensip.ts-provider.stage-facts.v1",
                    &a(vec![]),
                )),
            ),
            (
                "coverageCommitment",
                t(&built_commitment(
                    "opensip.ts-provider.stage-coverage.v1",
                    &a(e.clone()),
                )),
            ),
        ]));
        all.extend(e.clone());
    }
    let done = m(&[
        ("analysisOrdinal", u(0)),
        ("stageResults", a(results)),
        (
            "factStreamCommitment",
            t(&built_commitment(
                "opensip.ts-provider.fact-stream.v1",
                &a(vec![]),
            )),
        ),
        (
            "coverageStreamCommitment",
            t(&built_commitment(
                "opensip.ts-provider.coverage-stream.v1",
                &a(all),
            )),
        ),
    ]);
    match census {
        Some(v) => with(&done, "symbolCensus", v),
        None => done,
    }
}
/// The return commitment of the example's first key.
fn return_commitment() -> String {
    match path(&example(), &["keys"]) {
        Some(J::Array(k)) => js(&k[0], &["returnCommitment"]),
        _ => panic!("keys"),
    }
}
/// A receiver at ANALYZING under the census plan, and its context.
fn census_receiver<'s>(s: &'s Session, p: &Ts2Plan) -> (Ts2Receiver<'s>, DispatchContext, u64) {
    let c = context_of(p, &build(p));
    let mut r = s.receiver(c.clone());
    let seq = analyzing(&mut r, &c);
    (r, c, seq)
}
/// Drive Coverage for both stages (the symbol keys departing as the
/// example's census decides), then `complete`.
fn finish(
    r: &mut Ts2Receiver<'_>,
    c: &DispatchContext,
    seq: u64,
    census: Option<Value>,
) -> Result<Admitted, Ts2Refusal> {
    let rc = return_commitment();
    let e0 = entries_for(c, 0, Some((&rc, 3)));
    let e1 = entries_for(c, 1, None);
    r.receive(frame("Coverage", seq, coverage_of(c, 0, &e0)))
        .unwrap();
    r.receive(frame("Coverage", seq + 1, coverage_of(c, 1, &e1)))
        .unwrap();
    r.receive(frame(
        "Complete",
        seq + 2,
        complete_of(c, &[e0, e1], census),
    ))
}

// ------------------------------------------------------------------ the vectors

/// FA-2's vectors (vendored, hash-pinned): the oracle case and every key's
/// request and return commitment reproduce with the identity crate's H frame.
#[test]
fn fa2_vectors_reproduce() {
    let v = vectors();
    let oracle = parse_json(js(&v, &["oracle", "canonicalUtf8"]).as_bytes()).unwrap();
    let id = js(&v, &["oracle", "expectedScopeId"]);
    assert_eq!(
        scope_commitment(&oracle),
        format!("sha256:{}", id.strip_prefix("scope2:").unwrap())
    );
    assert_eq!(
        scope_commitment(&oracle),
        js(&v, &["oracle", "computed", "subjectScopeCommitment"])
    );
    let free = path(&v, &["censusFreeOfOracleDescriptor", "descriptor"]).unwrap();
    assert_eq!(
        scope_commitment(free),
        js(
            &v,
            &[
                "censusFreeOfOracleDescriptor",
                "computed",
                "subjectScopeCommitment"
            ]
        )
    );
    let x = example();
    let Some(J::Array(keys)) = path(&x, &["keys"]) else {
        panic!("keys")
    };
    for k in keys {
        let d = parse_json(js(k, &["canonicalDescriptorUtf8"]).as_bytes()).unwrap();
        assert_eq!(scope_commitment(&d), js(k, &["returnCommitment"]));
        // The request commitment is the same descriptor with no subjects.
        let J::Object(mut free) = d else {
            panic!("object")
        };
        free.insert("subjects".to_owned(), J::Array(Vec::new()));
        assert_eq!(
            scope_commitment(&J::Object(free)),
            js(k, &["requestCommitment"])
        );
    }
    assert_eq!(
        js(&x, &["terminalSymbolEntry", "subjectScopeCommitment"]),
        js(&keys[0], &["requestCommitment"])
    );
}

// ------------------------------------------------------------------ the request

/// The census request (NE §9.8 `request`, `requestCommitment` and
/// `planNeed`; LD-D2B3C-7): Analyze is TypeScriptAnalyzeV2 with the census
/// request, each symbol-kind key's D∅ commitment is recomputed against the
/// Plan's, and every other Plan is a host invariant.
#[test]
fn the_census_request_is_the_plans() {
    let p = census_plan();
    let r = build(&p);
    let census = get(r.analyze(), "symbolCensus");
    assert!(same(
        census,
        &m(&[(
            "enumeratorClosure",
            t(&js(&example(), &["enumeratorClosure"]))
        )])
    ));
    assert!(same(
        get(r.hello(), "expectedCapabilities"),
        &a(p.capabilities.iter().map(|s| t(s)).collect())
    ));
    // Without the token: the historical branch, AnalyzeV1, no census member.
    let r1 = build(&plan());
    let Value::Map(f) = r1.analyze() else {
        panic!("map")
    };
    assert!(field(f, "symbolCensus").is_none());
    // The token with no census owed and no symbol-kind key: a null request.
    let mut q = census_plan();
    q.symbol_census = None;
    q.stages[0].relations = vec!["file".to_owned()];
    q.stages[0].keys = vec![census_key("file", "enumerated", &sha('c'))];
    assert_eq!(get(build(&q).analyze(), "symbolCensus"), &Value::Null);
    for (what, change, key) in [
        (
            "a D∅ commitment that is not the Plan's",
            Box::new(|q: &mut Ts2Plan| q.stages[0].keys[1].subject_scope_commitment = sha('e'))
                as Box<dyn Fn(&mut Ts2Plan)>,
            "native.symbol-census-request-commitment-mismatch",
        ),
        (
            "another enumerator",
            Box::new(|q: &mut Ts2Plan| q.symbol_census = Some(format!("closure2:{}", h('4')))),
            "native.symbol-census-request-commitment-mismatch",
        ),
        (
            "a census owed without the token",
            Box::new(|q: &mut Ts2Plan| q.capabilities.retain(|c| c != "symbol-census-v1")),
            "native.symbol-census-payload-without-token",
        ),
        (
            "a symbol-kind key without an owed census",
            Box::new(|q: &mut Ts2Plan| q.symbol_census = None),
            "without an owed census",
        ),
        (
            "a census owed to a worker asked for no symbol-kind key",
            Box::new(|q: &mut Ts2Plan| {
                q.stages[0].relations = vec!["file".to_owned()];
                q.stages[0].keys = vec![census_key("file", "enumerated", &sha('c'))];
            }),
            "no symbol-kind key",
        ),
    ] {
        let mut q = census_plan();
        change(&mut q);
        let why = invariant(&q, what);
        assert!(why.contains(key), "{what}: {why}");
    }
}

/// Both payload mismatch directions, on Analyze (the sender, before writing)
/// and on Complete (the receiver, at the schema): a census-bearing payload
/// without the token, and an inherited one with it.
#[test]
fn a_census_payload_must_match_the_token() {
    // Analyze: the inherited payload under the token, and the census payload
    // without it, each refused before writing.
    for (p, analyze) in [
        (
            census_plan(),
            without(build(&census_plan()).analyze(), "symbolCensus"),
        ),
        (
            plan(),
            with(build(&plan()).analyze(), "symbolCensus", Value::Null),
        ),
    ] {
        let (mut s, mut source) = sender(&p);
        until(&mut s, &mut source, SlotFrame::Analyze);
        let seq = s.next_slot().unwrap().sequence;
        divergence(s.admit(SlotFrame::Analyze, seq, analyze), "payload-schema");
    }
    // Complete: CompleteV1 under the token is refused at the schema.
    let s = Session::new();
    let p = census_plan();
    let (mut r, c, seq) = census_receiver(&s, &p);
    let got = finish(&mut r, &c, seq, None);
    assert!(matches!(got, Err(Ts2Refusal::Schema(_))), "{got:?}");
    // TypeScriptCompleteV2 without the token is refused at Ts2CompleteV1.
    let c = context(&TOKENS);
    let mut r = s.receiver(c.clone());
    let mut seq = analyzing(&mut r, &c);
    for i in 0..2 {
        r.receive(frame("Coverage", seq, coverage(&c, i))).unwrap();
        seq += 1;
    }
    let v2 = with(
        &complete(&c, &[Vec::new(), Vec::new()], &[0, 0]),
        "symbolCensus",
        Value::Null,
    );
    assert!(matches!(
        r.receive(frame("Complete", seq, v2)),
        Err(Ts2Refusal::Schema(_))
    ));
}

// ------------------------------------------------------------------ the census

/// The example's complete census is admitted, with its symbol-kind entries
/// departing as the census decides (X-FA2-D), and reaches the consumer typed.
#[test]
fn a_complete_census_is_admitted() {
    let s = Session::new();
    let p = census_plan();
    let (mut r, c, seq) = census_receiver(&s, &p);
    let got = finish(&mut r, &c, seq, Some(example_census())).unwrap();
    assert_eq!(got.trace, "T2-17");
    let Some(SymbolCensus1SymbolCensusV1::CompleteSymbolCensusV1(census)) = got.census else {
        panic!("a complete census")
    };
    assert_eq!(census.rows.len(), 3);
    assert_eq!(census.examined_paths.len(), 3);
    // An over-bound census (the example's) is the typed event, with no fault.
    let (mut r, c, seq) = census_receiver(&s, &p);
    let over = json_value(path(&example(), &["overBound"]).unwrap());
    let got = finish(&mut r, &c, seq, Some(over)).unwrap();
    assert!(matches!(
        got.census,
        Some(SymbolCensus1SymbolCensusV1::OverBoundSymbolCensusV1(_))
    ));
    assert_eq!(r.phase(), "WAIT_ZERO_EXIT");
}

/// Each census refusal (LD-D2B-16), each before the table, under its law's
/// internal key or at the schema.
#[test]
fn a_malformed_census_is_refused() {
    let s = Session::new();
    let p = census_plan();
    let census = example_census();
    let rows = match get(&census, "rows") {
        Value::Array(r) => r.clone(),
        _ => unreachable!(),
    };
    let paths = match get(&census, "examinedPaths") {
        Value::Array(r) => r.clone(),
        _ => unreachable!(),
    };
    let over = |rows: u64, paths: u64| {
        m(&[
            ("state", t("over-bound")),
            ("rowCount", u(rows)),
            ("examinedPathCount", u(paths)),
        ])
    };
    let cases: Vec<(&str, Option<Value>, &str)> = vec![
        (
            "a wrongly null census",
            Some(Value::Null),
            "native.symbol-census-null-mismatch",
        ),
        (
            "rows misordered",
            Some(with(
                &census,
                "rows",
                a(vec![rows[1].clone(), rows[0].clone(), rows[2].clone()]),
            )),
            "schema",
        ),
        (
            "a duplicate row",
            Some(with(
                &census,
                "rows",
                a(vec![rows[0].clone(), rows[0].clone(), rows[2].clone()]),
            )),
            "schema",
        ),
        (
            "examined paths misordered",
            Some(with(
                &census,
                "examinedPaths",
                a(vec![paths[1].clone(), paths[0].clone(), paths[2].clone()]),
            )),
            "schema",
        ),
        (
            "a row off the examined extent",
            Some(with(
                &census,
                "examinedPaths",
                a(vec![paths[0].clone(), paths[1].clone()]),
            )),
            "native.symbol-census-path-not-examined",
        ),
        (
            "a partial census",
            Some(with(&census, "state", t("partial"))),
            "schema",
        ),
        (
            "an over-bound census within every bound",
            Some(over(0, 1)),
            "native.symbol-census-over-bound-within-bounds",
        ),
    ];
    for (what, bad, want) in cases {
        let (mut r, c, seq) = census_receiver(&s, &p);
        let got = finish(&mut r, &c, seq, bad);
        match (&got, want) {
            (Err(Ts2Refusal::Schema(_)), "schema") => {}
            (Err(Ts2Refusal::Admission(why)), key) if why.starts_with(key) => {}
            _ => panic!("{what}: {got:?}"),
        }
        assert_eq!(
            r.phase(),
            "READY_COMPLETE",
            "{what}: refused before the table"
        );
    }
    // A census where none was requested (the token, no census owed).
    let mut q = census_plan();
    q.symbol_census = None;
    q.stages[0].relations = vec!["file".to_owned()];
    q.stages[0].keys = vec![census_key("file", "enumerated", &sha('c'))];
    let (mut r, c, seq) = census_receiver(&s, &q);
    let e0 = entries_for(&c, 0, None);
    let e1 = entries_for(&c, 1, None);
    r.receive(frame("Coverage", seq, coverage_of(&c, 0, &e0)))
        .unwrap();
    r.receive(frame("Coverage", seq + 1, coverage_of(&c, 1, &e1)))
        .unwrap();
    let got = r.receive(frame(
        "Complete",
        seq + 2,
        complete_of(&c, &[e0, e1], Some(example_census())),
    ));
    assert!(
        matches!(&got, Err(Ts2Refusal::Admission(w)) if w.starts_with("native.symbol-census-null-mismatch")),
        "{got:?}"
    );
    // Over-bound censuses beyond a bound are admitted.
    for (rows, paths) in [(100_001, 0), (0, 100_001), (1, 1), (100_001, 2400)] {
        let (mut r, c, seq) = census_receiver(&s, &p);
        assert!(
            finish(&mut r, &c, seq, Some(over(rows, paths))).is_ok(),
            "{rows} {paths}"
        );
    }
}

/// The census's bounds, each one over and at the bound: the examined paths'
/// count (100,000) and the complete census's bytes (4,194,304). The rows'
/// count cannot be reached within the byte bound (each row is at least 70
/// bytes), so it is shown one over only.
#[test]
fn the_census_bounds_are_exact() {
    let s = Session::new();
    let p = census_plan();
    let paths = |n: usize| -> Vec<Value> {
        let mut v: Vec<String> = (0..n).map(|i| format!("p/{i:06}")).collect();
        v.push("src/a.ts".to_owned());
        v.push("src/view.tsx".to_owned());
        v.sort();
        v.into_iter().map(|s| t(&s)).collect()
    };
    let census = example_census();
    for (n, ok) in [(99_998, true), (99_999, false)] {
        let (mut r, c, seq) = census_receiver(&s, &p);
        let got = finish(
            &mut r,
            &c,
            seq,
            Some(with(&census, "examinedPaths", a(paths(n)))),
        );
        assert_eq!(got.is_ok(), ok, "{} paths: {got:?}", n + 2);
    }
    // 100,001 rows.
    let rows: Vec<Value> = (0..100_001u32)
        .map(|i| {
            m(&[
                ("nativeSubjectId", t(&format!("ts:src/a.ts#s{i:06}"))),
                ("path", t("src/a.ts")),
                ("qualifiedName", t("s")),
                ("exported", t("unknown")),
                ("signatureTokens", a(vec![])),
            ])
        })
        .collect();
    let (mut r, c, seq) = census_receiver(&s, &p);
    assert!(finish(&mut r, &c, seq, Some(with(&census, "rows", a(rows)))).is_err());
    // The byte bound: a census of exactly 4,194,304 bytes, then one more,
    // of rows within their schema (a qualifiedName of at most 4,096 scalars).
    let sized = |total: usize| -> Value {
        let row = |i: usize, len: usize| {
            m(&[
                ("nativeSubjectId", t(&format!("ts:src/a.ts#s{i:06}"))),
                ("path", t("src/a.ts")),
                ("qualifiedName", t(&"a".repeat(len))),
                ("exported", t("unknown")),
                ("signatureTokens", a(vec![])),
            ])
        };
        let of = |rows: &[Value]| with(&census, "rows", a(rows.to_vec()));
        let mut rows = Vec::new();
        while cbor::encode(&of(&[rows.clone(), vec![row(rows.len(), 4096)]].concat())).len() < total
        {
            rows.push(row(rows.len(), 4096));
        }
        // CBOR text-head transitions can skip an encoded byte length.
        // Search the final row exactly; if a head boundary leaves a gap,
        // shorten one earlier row by one byte and search again.
        for adjust in [false, true] {
            if adjust {
                rows[0] = row(0, 4095);
            }
            let (mut low, mut high) = (0usize, 4096usize);
            while low <= high {
                let len = low + (high - low) / 2;
                let v = of(&[rows.clone(), vec![row(rows.len(), len)]].concat());
                match cbor::encode(&v).len().cmp(&total) {
                    std::cmp::Ordering::Equal => return v,
                    std::cmp::Ordering::Less => low = len + 1,
                    std::cmp::Ordering::Greater if len > 0 => high = len - 1,
                    std::cmp::Ordering::Greater => break,
                }
            }
        }
        panic!("cannot size {total}");
    };
    for (total, ok) in [(4_194_304, true), (4_194_305, false)] {
        let (mut r, c, seq) = census_receiver(&s, &p);
        let got = finish(&mut r, &c, seq, Some(sized(total)));
        assert_eq!(got.is_ok(), ok, "{total} bytes: {got:?}");
        if !ok {
            assert!(
                matches!(&got, Err(Ts2Refusal::Admission(w)) if w.starts_with("native.symbol-census-bound"))
            );
        }
    }
}

/// Coverage under a requested census (X-FA2-D; LD-D2B3C-6): only a
/// symbol-kind key's two commitments may depart; a source-path key's, and
/// every other echo, still must equal the request.
#[test]
fn only_symbol_keys_depart_under_a_census() {
    let s = Session::new();
    let p = census_plan();
    let (mut r, c, seq) = census_receiver(&s, &p);
    // The source-path key departing is refused.
    let mut e1 = entries_for(&c, 1, None);
    let key = with(
        get(&e1[0], "key"),
        "subjectScopeCommitment",
        t(&return_commitment()),
    );
    e1[0] = with(&e1[0], "key", key);
    let e0 = entries_for(&c, 0, Some((&return_commitment(), 3)));
    r.receive(frame("Coverage", seq, coverage_of(&c, 0, &e0)))
        .unwrap();
    assert!(matches!(
        r.receive(frame("Coverage", seq + 1, coverage_of(&c, 1, &e1))),
        Err(Ts2Refusal::Admission(_))
    ));
    // A symbol key's relation still echoes.
    let (mut r, c, seq) = census_receiver(&s, &p);
    let mut e0 = entries_for(&c, 0, Some((&return_commitment(), 3)));
    let key = with(get(&e0[0], "key"), "resolution", t("syntactic-specifier"));
    e0[0] = with(&e0[0], "key", key);
    assert!(matches!(
        r.receive(frame("Coverage", seq, coverage_of(&c, 0, &e0))),
        Err(Ts2Refusal::Admission(_))
    ));
    // Without a census request, a symbol key may not depart.
    let s2 = Session::new();
    let c = context(&TOKENS);
    let mut r = s2.receiver(c.clone());
    let seq = analyzing(&mut r, &c);
    let e = entries_for(&c, 0, Some((&return_commitment(), 3)));
    assert!(matches!(
        r.receive(frame("Coverage", seq, coverage_of(&c, 0, &e))),
        Err(Ts2Refusal::Admission(_))
    ));
}

/// The handoff to H (LD-D2B-16; item 20; LD-D2B3C-1): the participant's spool
/// carries exactly the received Coverage and Complete payloads, the census
/// with them, in admission order.
#[test]
fn the_handoff_carries_the_received_census_and_entries() {
    let table = Table::load(Protocol::Ts2).unwrap();
    let p = census_plan();
    let (mut part, mut w) = session(&p, &table);
    let c = w.c.clone();
    let rc = return_commitment();
    let e0 = entries_for(&c, 0, Some((&rc, 3)));
    let e1 = entries_for(&c, 1, None);
    let frames = [
        wire("Coverage", 4, coverage_of(&c, 0, &e0)),
        wire("Coverage", 5, coverage_of(&c, 1, &e1)),
        wire(
            "Complete",
            6,
            complete_of(&c, &[e0, e1], Some(example_census())),
        ),
    ];
    w.answer = Some(("Analyze", frames.concat()));
    let (statuses, _, _) = drive_all(&mut part, &mut w);
    assert_eq!(
        statuses.last(),
        Some(&ParticipantStatus::Terminal(TerminalKind::Complete))
    );
    let spooled = part
        .take_terminal_output()
        .unwrap()
        .into_spool()
        .into_candidates();
    let want: Vec<Vec<u8>> = frames.iter().map(|f| f[40..].to_vec()).collect();
    assert_eq!(spooled, want);
}

/// The census token negotiated end to end, and the HelloAck's census token
/// omitted or added refused before OpenUniverse (LD-D2B-18; r3).
#[test]
fn the_census_token_is_negotiated_exactly() {
    let table = Table::load(Protocol::Ts2).unwrap();
    for (offered, acked, ok) in [
        (true, true, true),
        (true, false, false),
        (false, true, false),
    ] {
        let p = if offered { census_plan() } else { plan() };
        let (mut part, mut w) = session(&p, &table);
        let mut ack = w.c.clone();
        if acked {
            if !ack.capabilities.iter().any(|c| c == "symbol-census-v1") {
                ack.capabilities.push("symbol-census-v1".to_owned());
            }
        } else {
            ack.capabilities.retain(|c| c != "symbol-census-v1");
        }
        ack.capabilities.sort();
        w.answer = Some(("Hello", wire("HelloAck", 0, hello_ack(&ack))));
        let (statuses, _, _) = drive_all(&mut part, &mut w);
        if ok {
            assert!(
                w.seen.contains(&"OpenUniverse".to_owned()),
                "{offered} {acked}"
            );
        } else {
            assert_eq!(
                statuses.last(),
                Some(&ParticipantStatus::Fault),
                "{offered} {acked}"
            );
            assert_eq!(
                w.seen,
                ["Hello"],
                "{offered} {acked}: before any source byte"
            );
        }
    }
}

// ------------------------------------------------------------------ D2b-T4 and D2b-T5

/// D2b-T4 (M3-D r5 item 10; NE:2854-2856 and NE:2983): each HelloAck echo
/// mismatch is a protocol fault at the HelloAck, before OpenUniverse and any
/// source byte: an offered token omitted, an unoffered one added, an identity
/// version, either descriptor digest, and each of A2's eleven descriptor
/// fields.
#[test]
fn d2b_t4_every_hello_ack_mismatch_refuses_before_any_source_byte() {
    let table = Table::load(Protocol::Ts2).unwrap();
    // An optional token offered, so omitting it is lawful at the schema.
    let mut p = plan();
    p.capabilities.push("unresolved-edge-v1".to_owned());
    p.capabilities.sort();
    let base = context_of(&p, &build(&p));
    let ack = hello_ack(&base);
    let mut cases: Vec<(String, Value)> = Vec::new();
    let mut omitted = base.clone();
    omitted.capabilities.retain(|c| c != "unresolved-edge-v1");
    cases.push(("an offered token omitted".to_owned(), hello_ack(&omitted)));
    let mut added = base.clone();
    added.capabilities.push("sealed-vfs-v1".to_owned());
    added.capabilities.sort();
    cases.push(("an unoffered token added".to_owned(), hello_ack(&added)));
    cases.push((
        "an identity version".to_owned(),
        with(
            &ack,
            "identityVersions",
            m(&[
                ("coverage", u(3)),
                ("fact", u(2)),
                ("plan", u(2)),
                ("snapshot", u(1)),
            ]),
        ),
    ));
    for d in ["providerDescriptorSha256", "runtimeDescriptorSha256"] {
        cases.push((d.to_owned(), with(&ack, d, t(&h('f')))));
    }
    for (k, v) in base
        .provider_descriptor
        .iter()
        .chain(&base.runtime_descriptor)
    {
        let other = match v {
            Value::Text(s) if s.len() == 64 => t(&h('f')),
            Value::Text(s) => t(&format!("{s}x")),
            Value::Unsigned(n) => u(n + 1),
            _ => panic!("{k}"),
        };
        cases.push((k.clone(), with(&ack, k, other)));
    }
    assert_eq!(cases.len(), 5 + 11, "every echo member has a case");
    for (what, bad) in cases {
        let (mut part, mut w) = session(&p, &table);
        w.answer = Some(("Hello", wire("HelloAck", 0, bad)));
        let (statuses, _, _) = drive_all(&mut part, &mut w);
        assert_eq!(statuses.last(), Some(&ParticipantStatus::Fault), "{what}");
        assert_eq!(
            w.seen,
            ["Hello"],
            "{what}: no OpenUniverse and no source byte"
        );
    }
}

/// D2b-T5 (M3-D r5 item 10; LD-D2B-3; section 4's RF-1): every TS2
/// `commitmentMap` row a worker frame carries is recomputed over the received
/// bytes, and each refuses a swapped domain, a swapped value class (the other
/// class's preimage) and a reordered preimage. The table is checked complete
/// against the carriers' rows.
#[test]
fn d2b_t5_every_commitment_row_is_recomputed() {
    let carriers = parse_json(carrier::CARRIERS).unwrap();
    let J::Array(rows) = path(&carriers, &["commitmentMap", "rows"]).unwrap() else {
        panic!("rows")
    };
    let ts2: BTreeSet<String> = rows
        .iter()
        .filter(|r| path(r, &["protocol"]) == Some(&J::String("typescript-semantic".to_owned())))
        .filter(|r| !matches!(path(r, &["domain"]), Some(J::Null)))
        .map(|r| js(r, &["field"]))
        .collect();
    // The request-side rows are the builder's (D2b-3b's tests), and the
    // manifest digest has no domain.
    let request: BTreeSet<String> = [
        "Ts2RequestedCoverageDomainV1.domainCommitment",
        "Ts2SubjectScopeV1.subjectScopeCommitment",
    ]
    .map(str::to_owned)
    .into();
    let mut tested = BTreeSet::new();
    let s = Session::new();
    // A context whose stage one has two keys, so a reorder is visible.
    let mut c = context(&TOKENS);
    let mut k2 = c.stages[0].keys[0].clone();
    k2.target_universe_id = sha('7');
    c.stages[0].keys.push(k2);
    c.target_domain.insert(sha('7'));
    let b = batch_v1(&c, "stage-one", 0, 0, 2);
    let facts = candidates(&b);
    let rev = |v: &[Value]| -> Vec<Value> { v.iter().rev().cloned().collect() };
    let entries = |stage: usize| match get(&coverage(&c, stage), "entries") {
        Value::Array(e) => e.clone(),
        _ => unreachable!(),
    };
    let (e0, e1) = (entries(0), entries(1));
    let all: Vec<Value> = [e0.clone(), e1.clone()].concat();
    let cc = |d: &str, v: &[Value]| t(&built_commitment(d, &a(v.to_vec())));
    let (batch, stage_facts, stage_cov, fact_stream, cov_stream) = (
        "opensip.ts-provider.fact-batch.v1",
        "opensip.ts-provider.stage-facts.v1",
        "opensip.ts-provider.stage-coverage.v1",
        "opensip.ts-provider.fact-stream.v1",
        "opensip.ts-provider.coverage-stream.v1",
    );
    // FactBatch.
    tested.insert("Ts2FactBatchV1.batchCommitment".to_owned());
    for (what, bad) in [
        ("swapped domain", cc(stage_facts, &facts)),
        ("swapped class", cc(batch, &e0)),
        ("reordered", cc(batch, &rev(&facts))),
    ] {
        let mut r = s.receiver(c.clone());
        let seq = analyzing(&mut r, &c);
        let got = r.receive(frame("FactBatch", seq, with(&b, "batchCommitment", bad)));
        assert!(
            matches!(got, Err(Ts2Refusal::Admission(_))),
            "batch: {what}"
        );
    }
    // Coverage.
    tested.insert("Startup1TypeScriptCoverageV2.coverageCommitment".to_owned());
    for (what, bad) in [
        ("swapped domain", cc(cov_stream, &e0)),
        ("swapped class", cc(stage_cov, &facts)),
        ("reordered", cc(stage_cov, &rev(&e0))),
    ] {
        let mut r = s.receiver(c.clone());
        let seq = analyzing(&mut r, &c);
        let got = r.receive(frame(
            "Coverage",
            seq,
            with(&coverage(&c, 0), "coverageCommitment", bad),
        ));
        assert!(
            matches!(got, Err(Ts2Refusal::Admission(_))),
            "coverage: {what}"
        );
    }
    // Complete: its four rows, after a lawful stream.
    let done = complete(&c, &[facts.clone(), Vec::new()], &[1, 0]);
    let stage0 = |field: &str, v: Value| {
        let Value::Array(results) = get(&done, "stageResults") else {
            unreachable!()
        };
        with(
            &done,
            "stageResults",
            a(vec![with(&results[0], field, v), results[1].clone()]),
        )
    };
    let mut cases: Vec<(String, Value)> = Vec::new();
    for (field, own_domain, own, other_domain, other) in [
        (
            "factStreamCommitment",
            fact_stream,
            facts.clone(),
            stage_facts,
            all.clone(),
        ),
        (
            "coverageStreamCommitment",
            cov_stream,
            all.clone(),
            stage_cov,
            facts.clone(),
        ),
    ] {
        tested.insert(format!("Ts2CompleteV1.{field}"));
        cases.push((
            format!("{field}: swapped domain"),
            with(&done, field, cc(other_domain, &own)),
        ));
        cases.push((
            format!("{field}: swapped class"),
            with(&done, field, cc(own_domain, &other)),
        ));
        cases.push((
            format!("{field}: reordered"),
            with(&done, field, cc(own_domain, &rev(&own))),
        ));
    }
    for (field, own_domain, own, other_domain, other) in [
        (
            "factCommitment",
            stage_facts,
            facts.clone(),
            fact_stream,
            e0.clone(),
        ),
        (
            "coverageCommitment",
            stage_cov,
            e0.clone(),
            cov_stream,
            facts.clone(),
        ),
    ] {
        tested.insert(format!("Ts2StageResultV1.{field}"));
        cases.push((
            format!("stage {field}: swapped domain"),
            stage0(field, cc(other_domain, &own)),
        ));
        cases.push((
            format!("stage {field}: swapped class"),
            stage0(field, cc(own_domain, &other)),
        ));
        cases.push((
            format!("stage {field}: reordered"),
            stage0(field, cc(own_domain, &rev(&own))),
        ));
    }
    for (what, bad) in cases {
        let mut r = s.receiver(c.clone());
        let mut seq = analyzing(&mut r, &c);
        r.receive(frame("FactBatch", seq, b.clone())).unwrap();
        seq += 1;
        r.receive(frame("Coverage", seq, coverage(&c, 0))).unwrap();
        r.receive(frame("Coverage", seq + 1, coverage(&c, 1)))
            .unwrap();
        let got = r.receive(frame("Complete", seq + 2, bad));
        assert!(matches!(got, Err(Ts2Refusal::Admission(_))), "{what}");
    }
    // The terminals' coverage-stream rows, over stage-major entries.
    let unavailable = terminal_coverage(&c, "provider-unavailable");
    let spent = terminal_coverage(&c, "budget-exhausted");
    let post = |commitment: Value| {
        m(&[
            ("analysisOrdinal", u(0)),
            ("affectedStageIds", a(vec![t("stage-one"), t("stage-two")])),
            ("reason", t("semantic-universe-incomplete")),
            ("coverageCommitment", commitment),
            ("coverage", a(unavailable.clone())),
        ])
    };
    let budget = |commitment: Value| {
        m(&[
            ("analysisOrdinal", u(0)),
            ("triggerStageId", t("stage-two")),
            ("dimension", t("typeQueries")),
            ("limit", u(100)),
            ("observed", u(101)),
            ("coverageCommitment", commitment),
            ("coverage", a(spent.clone())),
        ])
    };
    for (row, kind, own, build) in [
        (
            "Startup1TypeScriptUnavailableV2.coverageCommitment",
            "Unavailable",
            unavailable.clone(),
            &post as &dyn Fn(Value) -> Value,
        ),
        (
            "Startup1TypeScriptBudgetExhaustedV2.coverageCommitment",
            "BudgetExhausted",
            spent.clone(),
            &budget,
        ),
    ] {
        tested.insert(row.to_owned());
        let mut r = s.receiver(c.clone());
        let seq = analyzing(&mut r, &c);
        assert!(
            r.receive(frame(kind, seq, build(cc(cov_stream, &own))))
                .is_ok(),
            "{row}: lawful"
        );
        for (what, bad) in [
            ("swapped domain", cc(stage_cov, &own)),
            ("swapped class", cc(cov_stream, &facts)),
            ("reordered", cc(cov_stream, &rev(&own))),
        ] {
            let mut r = s.receiver(c.clone());
            let seq = analyzing(&mut r, &c);
            assert!(
                matches!(
                    r.receive(frame(kind, seq, build(bad))),
                    Err(Ts2Refusal::Admission(_))
                ),
                "{row}: {what}"
            );
        }
    }
    assert_eq!(
        ts2,
        &tested | &request,
        "every TS2 commitmentMap row has its control"
    );
}

// ------------------------------------------------------------------ the depth bound

/// LD-D2B-2 recomputed with FA-2's payloads (D2b-3c): TypeScriptAnalyzeV2
/// (its stage requests are the carriers' `Ts2StageRequestV1`) and
/// TypeScriptCompleteV2 nest no deeper than the bound, so the bound stands.
#[test]
fn the_depth_bound_holds_with_the_census_payloads() {
    let docs = documents();
    let carriers = parse_json(carrier::CARRIERS).unwrap();
    let carriers = obj(&carriers).unwrap();
    let id = "opensip.product.symbol-census.1";
    let defs = obj(docs[id].get_defs()).unwrap();
    let complete = schema_depth(&docs, &defs["TypeScriptCompleteV2"], id, &BTreeSet::new());
    let stage = carrier_depth(
        &docs,
        carriers,
        &parse_json(br#"{"t":"ref","ref":"Ts2StageRequestV1"}"#).unwrap(),
        &BTreeSet::new(),
    );
    // Analyze V2: its map, the stageRequests array, then one stage request;
    // its census request is one map deep.
    let analyze = 2 + stage;
    for (what, depth) in [
        ("TypeScriptCompleteV2", complete),
        ("TypeScriptAnalyzeV2", analyze),
    ] {
        assert!(
            depth < TS2_FRAME_MAX_DEPTH,
            "{what}: {depth} under the envelope"
        );
    }
    // And the deepest lawful census Complete is read under the bound.
    let s = Session::new();
    let p = census_plan();
    let (mut r, c, seq) = census_receiver(&s, &p);
    assert!(finish(&mut r, &c, seq, Some(example_census())).is_ok());
}

/// A legal row's escaped token array can exceed the JSON profile's 4 MiB
/// limit while the complete received CBOR census remains below 4 MiB.
/// Every token still owes its original item schema, including late items.
#[test]
fn wide_signature_token_rows_are_admitted_without_weakening_item_or_count_bounds() {
    let s = Session::new();
    let p = census_plan();
    let original = example_census();
    let Value::Array(rows) = get(&original, "rows") else {
        unreachable!()
    };
    let replace_tokens = |tokens: Vec<Value>| {
        let mut rows = rows.clone();
        rows[0] = with(&rows[0], "signatureTokens", a(tokens));
        with(&original, "rows", a(rows))
    };
    for (unit, count) in [("x", 256usize), ("\0", 256), ("😀", 200)] {
        let token = unit.repeat(4096);
        let census = replace_tokens(vec![t(&token); count]);
        assert!(cbor::encode(&census).len() <= CENSUS_MAX_BYTES as usize);
        let json = opensip_identity::canonical_bytes(&carrier::to_json(&census).unwrap());
        if unit == "\0" {
            assert_eq!(json, Err(opensip_identity::CanonicalError::ByteLimit));
        } else {
            assert!(json.is_ok());
        }
        let (mut r, c, seq) = census_receiver(&s, &p);
        let got = finish(&mut r, &c, seq, Some(census));
        assert!(got.is_ok(), "wide signature tokens: {got:?}");
        let Some(SymbolCensus1SymbolCensusV1::CompleteSymbolCensusV1(typed)) = got.unwrap().census
        else {
            panic!("the full typed census")
        };
        assert_eq!(typed.rows[0].signature_tokens.len(), count);
        assert!(
            typed.rows[0]
                .signature_tokens
                .iter()
                .all(|value| value.as_str() == token.as_str())
        );
    }
    for (what, tokens) in [
        ("late signature token over maxLength", {
            let mut tokens = vec![t(&"\0".repeat(4096)); 256];
            tokens[255] = t(&"\0".repeat(4097));
            tokens
        }),
        ("late signature token of the wrong type", {
            let mut tokens = vec![t(&"\0".repeat(4096)); 256];
            tokens[255] = u(0);
            tokens
        }),
        (
            "signature token count above maxItems",
            vec![t(&"\0".repeat(4096)); 257],
        ),
    ] {
        let (mut r, c, seq) = census_receiver(&s, &p);
        let got = finish(&mut r, &c, seq, Some(replace_tokens(tokens)));
        assert!(
            matches!(&got, Err(Ts2Refusal::Schema(_))),
            "{what}: {got:?}"
        );
    }
}
