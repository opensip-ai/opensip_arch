use super::*;
use opensip_identity::JsonValue as J;

const RUST3_VECTORS: &[u8] = include_bytes!("../../tests/data/table-vectors.rust3.v1.json");
const TS2_VECTORS: &[u8] = include_bytes!("../../tests/data/table-vectors.ts2.v1.json");

fn member<'v>(v: &'v J, k: &str) -> &'v J {
    match v {
        J::Object(m) => m.get(k).unwrap_or(&J::Null),
        _ => panic!("not an object"),
    }
}
fn items(v: &J) -> &[J] {
    match v {
        J::Array(a) => a,
        _ => panic!("not an array"),
    }
}
fn as_text(v: &J) -> &str {
    match v {
        J::String(s) => s,
        other => panic!("not text: {other:?}"),
    }
}
fn as_int(v: &J) -> i64 {
    match v {
        J::Integer(i) => i64::try_from(i.get()).unwrap(),
        other => panic!("not an integer: {other:?}"),
    }
}
fn as_scalar(v: &J) -> Scalar {
    match v {
        J::Null => Scalar::Null,
        J::Bool(b) => Scalar::Bool(*b),
        J::Integer(_) => Scalar::Int(as_int(v)),
        J::String(s) => Scalar::Text(s.clone()),
        other => panic!("not a scalar: {other:?}"),
    }
}

/// A vector token as the event the codec would derive (the builder's
/// `token`): `HelloAck+` carries every identity token, `HelloAck-` does not;
/// `OpenUniverse:XY` its two modes; `Unavailable:pre|post` its payload.
fn event(token: &str, stages: i64) -> Event {
    let (frame, arg) = token.split_once(':').unwrap_or((token, ""));
    let (frame, negotiated) = match frame.strip_suffix('+') {
        Some(f) => (f, true),
        None => (frame.strip_suffix('-').unwrap_or(frame), false),
    };
    let mut e = Event::frame(frame);
    e.identity_negotiated = negotiated;
    e.stage_count = stages;
    if frame == "OpenUniverse" && !arg.is_empty() {
        e.dependency_mode = &arg[..1] == "T";
        e.prepared_mode = &arg[1..] == "T";
    }
    if frame == "Unavailable" && !arg.is_empty() {
        e.observations = vec![(
            "unavailablePayload".to_owned(),
            Scalar::Text(format!("{arg}-analyze")),
        )];
    }
    e
}

fn check(run: &Run<'_>, node: &J, protocol: Protocol, at: usize) {
    let want = |k: &str| as_scalar(member(node, k));
    assert_eq!(
        Scalar::Text(run.phase().to_owned()),
        want("phase"),
        "node {at}"
    );
    for (field, key) in [
        ("terminalKind", "terminal"),
        ("sourceBytesSent", "source"),
        ("stagesCompleted", "stages"),
        ("identityNegotiated", "identity"),
    ] {
        assert_eq!(run.field(field), Some(&want(key)), "node {at} {field}");
    }
    if protocol == Protocol::Ts2 {
        assert_eq!(run.field("cancelPhase"), Some(&want("cancel")), "node {at}");
    }
}

/// D2b-T1: every node of the reference's exploration (every row, both
/// catch-alls, the post-terminal law, absorption and the total fallback over
/// every reachable state and event) steps to the reference's trace entry and
/// state; P3T with the carriers' overlay is the major-3 table.
fn replay(protocol: Protocol, raw: &[u8]) -> usize {
    let table = Table::load(protocol).unwrap();
    let vectors = parse_json(raw).unwrap();
    let nodes = items(member(&vectors, "nodes"));
    let mut runs: Vec<Run<'_>> = Vec::with_capacity(nodes.len());
    let mut seen = std::collections::BTreeSet::new();
    for (at, node) in nodes.iter().enumerate() {
        let stages = as_int(member(node, "n"));
        let parent = as_int(member(node, "p"));
        let run = if parent < 0 {
            table.start()
        } else {
            let mut run = runs[parent as usize].clone();
            let entry = run.step(&event(as_text(member(node, "e")), stages));
            assert_eq!(entry, as_text(member(node, "t")), "node {at}");
            seen.insert(entry);
            run
        };
        check(&run, node, protocol, at);
        runs.push(run);
    }
    // Every row's id is reached, including both catch-alls.
    for id in table.rule_ids() {
        assert!(seen.contains(id), "{id} never replayed");
    }
    nodes.len()
}

#[test]
fn d2b_t1_every_p3t_row_with_the_overlay_replays_the_reference() {
    assert_eq!(replay(Protocol::Rust3, RUST3_VECTORS), 18_367);
}

#[test]
fn d2b_t1_every_t2o_row_replays_the_reference() {
    assert_eq!(replay(Protocol::Ts2, TS2_VECTORS), 2_810);
}

/// native-cases.v2's six protocol3_run cases, whose own expectations the
/// builder asserted for the base table; under the overlay each trace is the
/// overlay runner's.
#[test]
fn the_native_cases_replay_under_the_overlay() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let vectors = parse_json(RUST3_VECTORS).unwrap();
    let cases = items(member(&vectors, "nativeCases"));
    assert_eq!(cases.len(), 6);
    for case in cases {
        let stages = as_int(member(case, "n"));
        let mut run = table.start();
        let trace: Vec<String> = items(member(case, "events"))
            .iter()
            .map(|t| run.step(&event(as_text(t), stages)))
            .collect();
        let want: Vec<&str> = items(member(case, "overlayTrace"))
            .iter()
            .map(as_text)
            .collect();
        assert_eq!(trace, want, "{}", as_text(member(case, "id")));
    }
}

/// The overlay's one guard addition is P3-25's: Unavailable after output
/// faults under the production table, though the base table admits it.
#[test]
fn the_overlay_guards_unavailable_after_output() {
    let table = Table::load(Protocol::Rust3).unwrap();
    let mut run = table.start();
    let mut negotiated = Event::frame("HelloAck");
    negotiated.identity_negotiated = true;
    let mut universe = Event::frame("OpenUniverse");
    universe.dependency_mode = true;
    let mut analyze = Event::frame("Analyze");
    analyze.stage_count = 1;
    let head = [
        Event::frame("Hello"),
        negotiated,
        universe,
        Event::frame("UniverseAccepted"),
        Event::frame("SnapshotManifest"),
        Event::frame("SnapshotSeal"),
        Event::frame("SnapshotAccepted"),
        Event::frame("DependencySourceManifest"),
        Event::frame("DependencySourceSeal"),
        Event::frame("DependencySourceAccepted"),
        Event::frame("NativeContextVerified"),
        analyze,
    ];
    for e in &head {
        run.step(e);
    }
    let mut before = run.clone();
    assert_eq!(before.step(&Event::frame("Unavailable")), "P3-25");
    run.step(&Event::frame("FactBatch"));
    assert_eq!(run.step(&Event::frame("Unavailable")), "P3-34");
    assert_eq!(run.phase(), "FAULT");
    // No Cancel in START under major 3; TS2 permits it (T2-18).
    assert_eq!(table.start().step(&Event::frame("Cancel")), "P3-34");
    let ts2 = Table::load(Protocol::Ts2).unwrap();
    assert_eq!(ts2.start().step(&Event::frame("Cancel")), "T2-18");
}

/// The published rows are pairwise disjoint: rows sharing a phase and a
/// frame are separated by a guard key with different values, so first
/// match resolves no ambiguity (both tables' match law).
#[test]
fn rows_sharing_a_phase_and_frame_have_exclusive_guards() {
    for protocol in [Protocol::Rust3, Protocol::Ts2] {
        let table = Table::load(protocol).unwrap();
        for (i, a) in table.rules.iter().enumerate() {
            for b in &table.rules[i + 1..] {
                let shares = a.frame == b.frame
                    && (a.phase == b.phase
                        || (a.phase == table.set_wildcard.0
                            && table.set_wildcard.1.contains(&b.phase))
                        || (b.phase == table.set_wildcard.0
                            && table.set_wildcard.1.contains(&a.phase)));
                if shares && a.phase != "*ANY" {
                    let exclusive = a
                        .guard
                        .iter()
                        .any(|(k, v)| b.guard.iter().any(|(k2, v2)| k == k2 && v != v2));
                    assert!(exclusive, "{} and {} overlap", a.id, b.id);
                }
            }
        }
    }
}

/// Loading is closed: a base table that is not the carriers' pin, a prose
/// law the engine does not implement, and an unknown overlay member each
/// refuse.
#[test]
fn loading_refuses_an_unpinned_table_an_unknown_law_and_an_unknown_overlay_member() {
    assert_eq!(Table::load(Protocol::Rust3).unwrap().rule_ids().count(), 34);
    assert_eq!(Table::load(Protocol::Ts2).unwrap().rule_ids().count(), 23);
    let mut altered = P3T.to_vec();
    let at = altered.windows(5).position(|w| w == b"P3-01").unwrap();
    altered[at + 4] = b'9';
    assert_eq!(
        Table::load_from(Protocol::Rust3, &altered, CARRIERS).err(),
        Some(TableRefusal::Pin("p3"))
    );
    // The pin is the carriers': rewrite the pin to the altered bytes and the
    // engine judges the content instead.
    let text = std::str::from_utf8(T2O).unwrap();
    let law = text.replacen(
        "cancelPhase = the phase in which Cancel was sent",
        "cancelPhase = START",
        1,
    );
    let carriers = std::str::from_utf8(CARRIERS)
        .unwrap()
        .replacen(
            &digest_hex(&raw_sha256(T2O)),
            &digest_hex(&raw_sha256(law.as_bytes())),
            1,
        )
        .replacen(
            &format!("\"bytes\": {}", T2O.len()),
            &format!("\"bytes\": {}", law.len()),
            1,
        );
    assert_eq!(
        Table::load_from(Protocol::Ts2, law.as_bytes(), carriers.as_bytes()).err(),
        Some(TableRefusal::Law("cancelPhase = START".to_owned()))
    );
    let overlay = std::str::from_utf8(CARRIERS).unwrap().replacen(
        "\"guardAdditions\": {",
        "\"rowAdditions\": {}, \"guardAdditions\": {",
        1,
    );
    assert_eq!(
        Table::load_from(Protocol::Rust3, P3T, overlay.as_bytes()).err(),
        Some(TableRefusal::Law("overlay rowAdditions".to_owned()))
    );
}
