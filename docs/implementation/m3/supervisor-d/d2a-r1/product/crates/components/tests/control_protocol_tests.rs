// Unit D2a's controls (M3-D r5 item 9; D2a plan r1): CC v5's retained
// reference corpus, replayed byte for byte (D2a-T1, T2), the framing and
// resource probes (D2a-T3, T4), and the lead's supplementary controls.
use opensip_components::control_protocol::*;
use opensip_identity::{JsonInteger, JsonValue as V, RawSha256, parse_json};
use std::collections::BTreeMap;
use std::num::NonZeroU64;

/// The vendored corpus and RF5 proof, byte copies of the architecture's
/// `docs/coop/completion/control-completion.cases.v5.json` and
/// `.rf5-proof.v2.json`, pinned as the v5 freeze pins them.
const CASES: &[u8] = include_bytes!("data/control-completion.cases.v5.json");
const PROOF: &[u8] = include_bytes!("data/control-completion.rf5-proof.v2.json");
const CASES_SHA256: &str = "683d66988b169e5e90b648fbe6b8ffcd66dacf86aba23a58f29cfe8583cfddca";
const PROOF_SHA256: &str = "21d7fb2a4d5a6dfb93e69f174e1498350ad2f2768e733d1cf875f09c1b28e3e8";

fn hex(bytes: &[u8]) -> String {
    bytes.iter().map(|b| format!("{b:02x}")).collect()
}
fn unhex(text: &str) -> Vec<u8> {
    (0..text.len())
        .step_by(2)
        .map(|i| u8::from_str_radix(&text[i..i + 2], 16).unwrap())
        .collect()
}
fn sha256(bytes: &[u8]) -> String {
    hex(&RawSha256::new().update(bytes).unwrap().finish())
}
fn get<'v>(v: &'v V, k: &str) -> Option<&'v V> {
    match v {
        V::Object(m) => m.get(k),
        _ => None,
    }
}
fn at<'v>(v: &'v V, k: &str) -> &'v V {
    get(v, k).unwrap_or_else(|| panic!("missing {k}"))
}
fn text(v: &V) -> String {
    match v {
        V::String(s) => s.clone(),
        other => panic!("not a string: {other:?}"),
    }
}
fn opt_text(v: &V) -> Option<String> {
    match v {
        V::Null => None,
        other => Some(text(other)),
    }
}
fn int(v: &V) -> i64 {
    match v {
        V::Integer(i) => i64::try_from(i.get()).unwrap(),
        other => panic!("not an integer: {other:?}"),
    }
}
fn items(v: &V) -> &[V] {
    match v {
        V::Array(a) => a,
        _ => panic!("not an array"),
    }
}
fn tuple(v: &V) -> SubprotocolTuple {
    let V::Object(m) = v else { panic!("tuple") };
    assert_eq!(m.len(), 3);
    SubprotocolTuple {
        role: text(at(v, "role")),
        role_subprotocol: text(at(v, "roleSubprotocol")),
        subprotocol_version: int(at(v, "subprotocolVersion")),
    }
}

/// A corpus case's context, exactly its sixteen members (and the one case's
/// offered refusal major).
fn context(c: &V) -> ControlContext {
    let V::Object(m) = c else { panic!("context") };
    for key in m.keys() {
        assert!(
            [
                "state",
                "direction",
                "helloSeen",
                "frameBound",
                "frameOffer",
                "nextSeq",
                "stableId",
                "manifestDigest",
                "platform",
                "manifestTuples",
                "offeredTuples",
                "confirmedTuples",
                "selectedTuple",
                "pendingNonce",
                "authorizationEvidence",
                "effectOutcomeEvidence",
                "offeredControlMajor",
            ]
            .contains(&key.as_str()),
            "{key}"
        );
    }
    let platform = at(c, "platform");
    let auth = at(c, "authorizationEvidence");
    let outcome = at(c, "effectOutcomeEvidence");
    let nonce = at(c, "pendingNonce");
    ControlContext {
        state: ControlState::parse(&text(at(c, "state"))).unwrap(),
        direction: Direction::parse(&text(at(c, "direction"))).unwrap(),
        hello_seen: matches!(at(c, "helloSeen"), V::Bool(true)),
        frame_bound: u32::try_from(int(at(c, "frameBound"))).unwrap(),
        frame_offer: int(at(c, "frameOffer")),
        next_seq: int(at(c, "nextSeq")),
        stable_id: text(at(c, "stableId")),
        manifest_digest: text(at(c, "manifestDigest")),
        platform: Platform {
            os: text(at(platform, "os")),
            arch: text(at(platform, "arch")),
        },
        manifest_tuples: items(at(c, "manifestTuples")).iter().map(tuple).collect(),
        offered_tuples: items(at(c, "offeredTuples")).iter().map(tuple).collect(),
        confirmed_tuples: items(at(c, "confirmedTuples")).iter().map(tuple).collect(),
        selected_tuple: match at(c, "selectedTuple") {
            V::Null => None,
            t => Some(tuple(t)),
        },
        pending_pong: get(nonce, "pong").and_then(opt_text),
        pending_health_report: get(nonce, "healthReport").and_then(opt_text),
        authorization: AuthorizationEvidence {
            authorized: matches!(at(auth, "authorized"), V::Bool(true)),
            effect_class: text(at(auth, "effectClass")),
            authorization_ref: text(at(auth, "authorizationRef")),
            operation_ref: text(at(auth, "operationRef")),
            decision_class: opt_text(at(auth, "decisionClass")),
            binding_mismatch_decision_class: opt_text(at(auth, "bindingMismatchDecisionClass")),
        },
        effect_outcome: EffectOutcomeEvidence {
            request_seq: int(at(outcome, "requestSeq")),
            decision_seq: int(at(outcome, "decisionSeq")),
            outcome_seq: int(at(outcome, "outcomeSeq")),
            commit_class: text(at(outcome, "commitClass")),
            effect_outcome: text(at(outcome, "effectOutcome")),
            effect_class: text(at(outcome, "effectClass")),
        },
        offered_control_major: get(c, "offeredControlMajor").map_or(1, int),
    }
}

fn s(v: &str) -> V {
    V::String(v.to_owned())
}
fn b(v: bool) -> V {
    V::Bool(v)
}
fn n(v: i64) -> V {
    V::Integer(JsonInteger::new(v as i128).unwrap())
}
fn object(members: Vec<(&str, V)>) -> V {
    V::Object(
        members
            .into_iter()
            .map(|(k, v)| (k.to_owned(), v))
            .collect::<BTreeMap<_, _>>(),
    )
}

/// A verdict as the reference reports it.
fn outcome(verdict: &ControlVerdict) -> V {
    match verdict {
        ControlVerdict::Accepted(a) => {
            let mut m = vec![
                ("verdict", s("ACCEPT")),
                ("type", s(a.message_type)),
                ("nextState", s(a.next_state.as_str())),
                ("bodyBuffered", b(true)),
            ];
            if let Some(family) = &a.terminal_family {
                m.push(("terminalFamily", s(family)));
            }
            object(m)
        }
        ControlVerdict::Refused(r) => {
            let mut m = vec![
                ("verdict", s(r.family.as_str())),
                ("nextState", s("FAULTED")),
                ("bodyBuffered", b(r.body_buffered)),
            ];
            if let Some(d) = &r.decision_class {
                m.push(("decisionClass", s(d)));
            }
            object(m)
        }
    }
}

fn frame_of(case: &V) -> Vec<u8> {
    if let Some(recipe) = get(case, "frameRecipe") {
        let length = int(at(recipe, "length")) as usize;
        let base = unhex(&text(at(recipe, "baseHex")));
        let mut raw = (length as u32).to_be_bytes().to_vec();
        raw.extend_from_slice(&base);
        raw.resize(4 + length, b' ');
        return raw;
    }
    unhex(&text(at(case, "frameHex")))
}

/// The reference's `run_session`, through `ControlSession`.
fn trace(case: &V) -> V {
    let mut session = ControlSession::new(context(at(case, "context")));
    let steps = items(at(case, "sessionFrames"))
        .iter()
        .map(|step| {
            let direction = Direction::parse(&text(at(step, "direction"))).unwrap();
            let raw = unhex(&text(at(step, "frameHex")));
            let out = session.receive(direction, &raw);
            let (verdict, buffered) = match &out.verdict {
                ControlVerdict::Accepted(_) => ("ACCEPT", true),
                ControlVerdict::Refused(r) => (r.family.as_str(), r.body_buffered),
            };
            object(vec![
                ("verdict", s(verdict)),
                ("bodyBuffered", b(buffered)),
                ("state", s(out.state.as_str())),
                (
                    "stoppedDirections",
                    V::Array(out.stopped.iter().map(|d| s(d.as_str())).collect()),
                ),
                (
                    "nextSeq",
                    object(vec![
                        ("host-to-component", n(out.next_seq[0])),
                        ("component-to-host", n(out.next_seq[1])),
                    ]),
                ),
            ])
        })
        .collect();
    object(vec![("verdict", s("TRACE")), ("steps", V::Array(steps))])
}

#[test]
fn d2a_t1_the_cc_v5_corpus_replays_byte_for_byte() {
    assert_eq!(sha256(CASES), CASES_SHA256);
    assert_eq!(sha256(PROOF), PROOF_SHA256);
    let corpus = parse_json(CASES).unwrap();
    let cases = items(at(&corpus, "cases"));
    assert_eq!(cases.len(), 480);
    let mut failures = Vec::new();
    for case in cases {
        let id = text(at(case, "id"));
        let actual = if get(case, "sessionFrames").is_some() {
            trace(case)
        } else {
            outcome(&classify(&frame_of(case), &context(at(case, "context"))))
        };
        if &actual != at(case, "expected") {
            failures.push(format!(
                "{id}: expected {:?}, got {actual:?}",
                at(case, "expected")
            ));
        }
    }
    assert!(
        failures.is_empty(),
        "{} of 480 differ:\n{}",
        failures.len(),
        failures.join("\n")
    );
    // coverage/RF5-unreachable-preview, as the reference states it.
    let proof = parse_json(PROOF).unwrap();
    let V::Object(functions) = at(&proof, "messageFunctions") else {
        panic!("messageFunctions")
    };
    let mut types: Vec<&str> = functions.keys().map(String::as_str).collect();
    types.sort();
    let mut expected_types = vec![
        "hello",
        "helloAck",
        "select",
        "selectAck",
        "refusal",
        "ping",
        "pong",
        "cancel",
        "health",
        "healthReport",
        "resourceReport",
        "fault",
        "effectRequest",
        "effectResult",
        "shutdown",
        "shutdownAck",
    ];
    expected_types.sort();
    assert_eq!(types, expected_types);
    assert_eq!(
        items(at(&proof, "effectClasses"))
            .iter()
            .map(text)
            .collect::<Vec<_>>(),
        ["HE-1", "HE-2"]
    );
    assert!(
        cases
            .iter()
            .all(|c| get(at(c, "expected"), "verdict") != Some(&s("RF-5")))
    );
}

#[test]
fn d2a_t2_every_cell_of_the_full_sixteen_by_eight_by_two_matrix_is_covered() {
    // The reference counts distinct triples; this asserts the whole product.
    let corpus = parse_json(CASES).unwrap();
    let mut cells = std::collections::BTreeSet::new();
    for case in items(at(&corpus, "cases")) {
        if text(at(case, "id")).starts_with("MATRIX/") {
            let c = at(case, "context");
            assert!(cells.insert((
                text(at(c, "state")),
                text(at(c, "direction")),
                text(at(case, "messageType"))
            )));
        }
    }
    assert_eq!(cells.len(), 256);
    for state in ControlState::ALL {
        for direction in [Direction::HostToComponent, Direction::ComponentToHost] {
            let count = cells
                .iter()
                .filter(|(s, d, _)| s == state.as_str() && d == direction.as_str())
                .count();
            assert_eq!(count, 16, "{} {}", state.as_str(), direction.as_str());
        }
    }
}

fn base_context() -> ControlContext {
    let corpus = parse_json(CASES).unwrap();
    context(at(&items(at(&corpus, "cases"))[0], "context"))
}
fn framed(body: &str) -> Vec<u8> {
    let mut raw = (body.len() as u32).to_be_bytes().to_vec();
    raw.extend_from_slice(body.as_bytes());
    raw
}
fn verdict_of(raw: &[u8], context: &ControlContext) -> String {
    match classify(raw, context) {
        ControlVerdict::Accepted(_) => "ACCEPT".to_owned(),
        ControlVerdict::Refused(r) => format!("{} buffered={}", r.family.as_str(), r.body_buffered),
    }
}

#[test]
fn d2a_t3_an_oversized_or_zero_prefix_refuses_from_the_prefix_alone() {
    let context = base_context();
    for prefix in [0u32, 65_537, 131_073, u32::MAX] {
        let raw = prefix.to_be_bytes();
        assert_eq!(
            verdict_of(&raw, &context),
            "RF-2 buffered=false",
            "{prefix}"
        );
    }
    // Fewer than four bytes, and a body one short of its prefix.
    assert_eq!(verdict_of(&[0, 0, 1], &context), "RF-2 buffered=false");
    let mut short = framed("{}");
    short.pop();
    assert_eq!(verdict_of(&short, &context), "RF-2 buffered=true");
}

#[test]
fn d2a_t4_deep_nesting_and_long_integers_never_recurse() {
    // On a thread with a 64 KiB stack: a recursive reader, drop or compare
    // would overflow it.
    let handle = std::thread::Builder::new()
        .stack_size(64 * 1024)
        .spawn(|| {
            let mut context = base_context();
            context.state = ControlState::Steady;
            context.direction = Direction::HostToComponent;
            let deep = format!("{}{}", "[".repeat(65_000), "]".repeat(65_000));
            let body =
                format!(r#"{{"type":"ping","seq":1,"controlMajor":1,"body":{{"nonce":{deep}}}}}"#);
            let mut bound = context.clone();
            bound.frame_bound = 16_777_216;
            let deep_ping = verdict_of(&framed(&body), &bound);
            let digits = "9".repeat(5_000);
            let long_seq = verdict_of(
                &framed(&format!(
                    r#"{{"type":"ping","seq":{digits},"controlMajor":1,"body":{{"nonce":"n"}}}}"#
                )),
                &context,
            );
            (deep_ping, long_seq)
        })
        .unwrap();
    let (deep_ping, long_seq) = handle.join().unwrap();
    assert_eq!(deep_ping, "RF-2 buffered=true");
    assert_eq!(long_seq, "RF-7 buffered=true");
}

#[test]
fn negative_zero_is_zero_and_an_unpaired_surrogate_in_an_opaque_body_reaches_rf1() {
    let mut context = base_context();
    // seq -0 is the integer 0: a sequence fault.
    context.state = ControlState::Steady;
    context.direction = Direction::HostToComponent;
    let raw = framed(r#"{"type":"ping","seq":-0,"controlMajor":1,"body":{"nonce":"n"}}"#);
    assert_eq!(verdict_of(&raw, &context), "RF-7 buffered=true");
    // -0 in a body integer is 0, accepted.
    context.direction = Direction::ComponentToHost;
    let raw = framed(
        r#"{"type":"resourceReport","seq":1,"controlMajor":1,"body":{"residentBytes":-0,"cpuNanoseconds":0,"openHandles":0}}"#,
    );
    assert_eq!(verdict_of(&raw, &context), "ACCEPT");
    // A future-major hello's body is opaque: an unpaired surrogate there is
    // never walked, so the frozen envelope selects RF1.
    let mut context = base_context();
    context.state = ControlState::AwaitHello;
    context.direction = Direction::HostToComponent;
    context.hello_seen = false;
    let raw = framed(r#"{"type":"hello","seq":1,"controlMajor":2,"body":{"x":"\ud800"}}"#);
    assert_eq!(verdict_of(&raw, &context), "RF-1 buffered=true");
    // The same string in a known body is refused by the UTF-8 walk.
    context.state = ControlState::Steady;
    let raw = framed(r#"{"type":"ping","seq":1,"controlMajor":1,"body":{"nonce":"\ud800"}}"#);
    assert_eq!(verdict_of(&raw, &context), "RF-2 buffered=true");
}

/// A duplicate member is RF2 at every depth, compared on the decoded key
/// (`check.v5.py`:75, in the parser, before the envelope): a body's duplicate
/// is refused although the envelope's four members are exact.
#[test]
fn a_duplicate_member_in_a_body_is_rf2_on_the_decoded_key() {
    let mut context = base_context();
    context.state = ControlState::Steady;
    context.direction = Direction::HostToComponent;
    let raw =
        framed(r#"{"type":"ping","seq":1,"controlMajor":1,"body":{"nonce":"n","nonce":"n"}}"#);
    assert_eq!(verdict_of(&raw, &context), "RF-2 buffered=true");
    let raw =
        framed(r#"{"type":"ping","seq":1,"controlMajor":1,"body":{"nonce":"n","\u006eonce":"m"}}"#);
    assert_eq!(verdict_of(&raw, &context), "RF-2 buffered=true");
    // The same body without the duplicate is accepted.
    let raw = framed(r#"{"type":"ping","seq":1,"controlMajor":1,"body":{"nonce":"n"}}"#);
    assert_eq!(verdict_of(&raw, &context), "ACCEPT");
}

fn selection() -> AdmittedSelection {
    AdmittedSelection {
        stable_id: "00000000-0000-4000-8000-000000000001".to_owned(),
        manifest_digest: "1".repeat(64),
        platform: Platform {
            os: "macos".to_owned(),
            arch: "arm64".to_owned(),
        },
        tuple: SubprotocolTuple {
            role: "analyzer".to_owned(),
            role_subprotocol: "typescript-semantic".to_owned(),
            subprotocol_version: 2,
        },
    }
}

#[test]
fn the_production_context_is_the_65536_bound_and_the_one_admitted_tuple() {
    let context = ControlContext::for_session(&selection());
    assert_eq!(context.frame_bound, HOST_FRAME_BOUND);
    assert_eq!(context.frame_bound, 65_536);
    assert_eq!(context.frame_offer, 65_536);
    assert_eq!(context.offered_tuples, [selection().tuple]);
    assert_eq!(context.manifest_tuples, [selection().tuple]);
    assert_eq!(context.state, ControlState::AwaitHello);
}

#[test]
fn the_hosts_own_frames_classify_as_accepted_and_a_multi_tuple_hello_is_refused() {
    let selection = selection();
    let one = NonZeroU64::MIN;
    let mut context = ControlContext::for_session(&selection);
    context.direction = Direction::HostToComponent;
    // hello in AWAIT-HELLO.
    let hello = host_hello(&selection, one).unwrap();
    let raw = encode(&hello).unwrap();
    assert_eq!(verdict_of(&raw, &context), "ACCEPT");
    let ControlVerdict::Accepted(accepted) = classify(&raw, &context) else {
        unreachable!()
    };
    assert_eq!(encode(&accepted.message).unwrap(), raw);
    // select in AWAIT-SELECT, once the tuple is confirmed.
    context.state = ControlState::AwaitSelect;
    context.confirmed_tuples = vec![selection.tuple.clone()];
    let select = host_select(&selection, one).unwrap();
    let raw = encode(&select).unwrap();
    assert_eq!(verdict_of(&raw, &context), "ACCEPT");
    // A hello with two offers is never written (item 9's one tuple).
    let mut two = hello;
    if let Control3Root::Hello { body, .. } = &mut two {
        let extra = body.subprotocol_offers[0].clone();
        body.subprotocol_offers.push(extra);
    }
    assert_eq!(encode(&two), Err(EncodeRefusal::HelloOffers(2)));
}

#[test]
fn the_schema_interpreter_takes_the_product_schema_and_refuses_any_other_keyword() {
    const PRODUCT: &str = include_str!("../../../schemas/sources/control-v3.schema.json");
    let loaded = schema().expect("the embedded product schema loads");
    let mut types: Vec<&str> = loaded.message_types().collect();
    assert_eq!(types.len(), 16);
    types.sort();
    types.dedup();
    assert_eq!(types.len(), 16);
    assert!(Schema::load(PRODUCT).is_ok());
    // An uninterpreted keyword, or a pattern other than the two, refuses the
    // whole schema rather than being ignored.
    let with_format = PRODUCT.replacen(r#""minLength""#, r#""format": "uri", "minLength""#, 1);
    assert!(matches!(
        Schema::load(&with_format),
        Err(SchemaRefusal::UnknownKeyword(k)) if k == "format"
    ));
    let with_pattern = PRODUCT.replacen("^[0-9a-f]{64}", "^[0-9A-F]{64}", 1);
    assert!(matches!(
        Schema::load(&with_pattern),
        Err(SchemaRefusal::UnknownPattern(_))
    ));
}
