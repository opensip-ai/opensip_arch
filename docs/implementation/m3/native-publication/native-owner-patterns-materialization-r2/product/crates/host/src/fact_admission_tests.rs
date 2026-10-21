// Law X5 r3 item 8 (unit X5a), host side. Replay is pure, so every test runs
// on the evaluator's existing synthetic replay corpus
// (`tests/fixtures/replay-fixtures.native-owner-r1.json`, 101 labelled cases) with no scratch
// installation, home or lock. Synthetic fixtures; no compiler
// qualification is claimed.
use super::*;
use crate::doctor_ingress::failure_envelope;
use opensip_evaluator::{EvaluationError, RetainedWalkError, UnavailableEvidence};
use opensip_identity::{
    CaptureError, GraphError, IdentityDomain, JsonValue as V, RetainedInputError, digest_hex,
    parse_json,
};
use serde_json::Value;
use std::sync::OnceLock;

const REQUEST: &str = "req1_0123456789abcdef0123456789abcdef";
const ENVELOPE: &str = "urn:opensip:product-v1:workflows:evaluator3:command-envelope:7";
/// The corpus's lawful case that the removal, input and bounds tests use.
const LAWFUL: &str = "packet-0-original";
/// The corpus's missing-evidence case.
const MISSING_BLOB: &str =
    "missing-blob-03cc96a8548e6d391a1b12c3bcf491ab13ef50f355e809819b2a1d7e53117bd0";

// ---------------------------------------------------------------- corpus

struct Case {
    label: String,
    run_id: String,
    objects: BTreeMap<String, ObjectInput>,
    blobs: BTreeMap<[u8; 32], Vec<u8>>,
    expected: BTreeMap<String, V>,
}

fn object(v: &V) -> &BTreeMap<String, V> {
    match v {
        V::Object(o) => o,
        _ => panic!("fixture object"),
    }
}
fn array(v: &V) -> &[V] {
    match v {
        V::Array(a) => a,
        _ => panic!("fixture array"),
    }
}
fn string(v: &V) -> &str {
    match v {
        V::String(s) => s,
        _ => panic!("fixture string"),
    }
}
fn bytes(hex: &str) -> Vec<u8> {
    hex.as_bytes()
        .chunks_exact(2)
        .map(|p| u8::from_str_radix(std::str::from_utf8(p).unwrap(), 16).unwrap())
        .collect()
}
fn copy(objects: &BTreeMap<String, ObjectInput>) -> BTreeMap<String, ObjectInput> {
    objects
        .iter()
        .map(|(k, v)| {
            (
                k.clone(),
                ObjectInput {
                    domain: v.domain,
                    descriptor: v.descriptor.clone(),
                },
            )
        })
        .collect()
}

fn corpus() -> &'static [Case] {
    static CORPUS: OnceLock<Vec<Case>> = OnceLock::new();
    CORPUS.get_or_init(|| {
        let f = parse_json(include_bytes!(
            "../tests/fixtures/replay-fixtures.native-owner-r1.json"
        ))
        .unwrap();
        let f = object(&f);
        array(&f["cases"])
            .iter()
            .map(|c| {
                let q = object(c);
                let objects = array(&q["objects"])
                    .iter()
                    .map(|k| {
                        let r = object(&object(&f["objectPool"])[string(k)]);
                        (
                            string(&r["id"]).to_owned(),
                            ObjectInput {
                                domain: IdentityDomain::parse(string(&r["domain"])).unwrap(),
                                descriptor: r["descriptor"].clone(),
                            },
                        )
                    })
                    .collect();
                let blobs = array(&q["blobs"])
                    .iter()
                    .map(|k| {
                        let r = object(&object(&f["blobPool"])[string(k)]);
                        (
                            bytes(string(&r["digest"])).try_into().unwrap(),
                            bytes(string(&r["hex"])),
                        )
                    })
                    .collect();
                Case {
                    label: string(&q["label"]).to_owned(),
                    run_id: string(&q["runId"]).to_owned(),
                    objects,
                    blobs,
                    expected: object(&q["expected"]).clone(),
                }
            })
            .collect()
    })
}
fn case(label: &str) -> &'static Case {
    corpus().iter().find(|c| c.label == label).unwrap()
}
fn registry() -> &'static RegisteredSchemas {
    static REGISTRY: OnceLock<RegisteredSchemas> = OnceLock::new();
    REGISTRY.get_or_init(|| crate::embedded_schema_registry().unwrap())
}

/// One replay through the join, over the given maps.
fn replay(
    run_id: &str,
    objects: &BTreeMap<String, ObjectInput>,
    blobs: &BTreeMap<[u8; 32], Vec<u8>>,
    limits: ReplayLimits,
) -> Result<ReplayedRun, ReplayRefusal> {
    replay_candidate(
        &RunCandidateInputs {
            registry: registry(),
            objects,
            blobs,
            run_id,
        },
        limits,
    )
}

/// Run `work` over `items` on every core. Replay is pure, so the order of
/// the probes does not matter; results come back in input order.
fn parallel<T: Sync, R: Send>(items: &[T], work: impl Fn(&T) -> R + Sync) -> Vec<R> {
    let threads = std::thread::available_parallelism().map_or(4, |n| n.get());
    let chunk = items.len().div_ceil(threads).max(1);
    std::thread::scope(|scope| {
        let handles: Vec<_> = items
            .chunks(chunk)
            .map(|part| scope.spawn(|| part.iter().map(&work).collect::<Vec<_>>()))
            .collect();
        handles
            .into_iter()
            .flat_map(|h| h.join().unwrap())
            .collect()
    })
}

// ---------------------------------------------------------------- the rows

/// The public members of each item 5 route, spelled as the fault schema's
/// `x-opensip-routes` and identity's carriers spell them:
/// (class, exit, errorCode, faultCause, detail, remedy).
const EVIDENCE_MISSING: (&str, u8, &str, &str, &str, &str) = (
    "operational-failed",
    4,
    "HOST.IO_FAILURE",
    "host-io",
    "evidence.missing",
    "Restore the exact retained closure bytes or report their unavailability.",
);
const INPUT_REFUSED: (&str, u8, &str, &str, &str, &str) = (
    "operational-failed",
    4,
    "PROVIDER.PROTOCOL_VIOLATION",
    "provider-protocol",
    "EVALUATION.INPUT_REFUSED",
    "Correct the provider output and rerun the stage; retain its admission diagnostic.",
);
const REGENERATION_MISMATCH: (&str, u8, &str, &str, &str, &str) = (
    "operational-failed",
    4,
    "HOST.IO_FAILURE",
    "host-io",
    "evidence.regeneration-mismatch",
    "Retain the sealed Run and investigate the differing regeneration result.",
);

/// Assert that `refusal` projects to `route` with `subject`, and that the
/// shared failure envelope carries it, valid against command-envelope v7.
fn assert_row(
    refusal: &ReplayRefusal,
    route: (&str, u8, &str, &str, &str, &str),
    subject: Option<&str>,
) {
    let (class, exit, code, fault, detail, remedy) = route;
    let t = replay_termination(refusal);
    let context = format!("{refusal:?}");
    assert_eq!(t.class, class.parse::<Class>().unwrap(), "{context}");
    assert_eq!(t.exit, exit, "{context}");
    assert_eq!(t.error_code, code.parse::<Code>().unwrap(), "{context}");
    assert_eq!(t.fault_cause, fault.parse::<Fault>().unwrap(), "{context}");
    assert_eq!(
        t.detail,
        Some(detail.parse::<Detail>().unwrap()),
        "{context}"
    );
    assert_eq!(t.subject.as_deref(), subject, "{context}");
    assert_eq!(replay_remedy(refusal), remedy, "{context}");

    let (envelope, exit_code) = failure_envelope(REQUEST, None, &t).unwrap();
    assert_eq!(exit_code, exit);
    let raw = opensip_reporting::render_json(&envelope).unwrap();
    assert!(
        registry()
            .schema(ENVELOPE, "")
            .unwrap()
            .admit_json(&raw, 64 * 1024 * 1024)
            .is_ok(),
        "{}",
        String::from_utf8_lossy(&raw)
    );
    let value: Value = serde_json::from_slice(&raw).unwrap();
    let termination = &value["termination"];
    assert_eq!(termination["class"], class);
    assert_eq!(termination["errorCode"], code);
    assert_eq!(termination["faultCause"], fault);
    assert_eq!(termination["domainDetail"]["code"], detail);
    assert_eq!(termination["domainDetail"]["remedy"], remedy);
    match subject {
        Some(subject) => assert_eq!(termination["domainDetail"]["subject"], subject),
        None => assert!(termination["domainDetail"].get("subject").is_none()),
    }
    assert_eq!(value["exitCode"], exit);
    // No failure envelope substitutes an empty success or names a Run as
    // authoritative.
    assert_eq!(value["kind"], "failure");
    assert!(value.get("run").is_none());
}

/// The refusal of a replay that must not succeed (`ReplayedRun` has no
/// `Debug`, by design).
fn refused<T>(outcome: Result<T, ReplayRefusal>) -> ReplayRefusal {
    match outcome {
        Ok(_) => panic!("the candidate replayed"),
        Err(refusal) => refusal,
    }
}

fn refusal(diagnostic: ReplayError) -> ReplayRefusal {
    ReplayRefusal {
        run_id: "run3:claimed".into(),
        diagnostic,
    }
}

#[test]
fn each_replay_error_maps_to_its_row_and_remedy() {
    const KEY: &str = "plan3:0000000000000000000000000000000000000000000000000000000000000000";
    let digest = [0x5a; 32];
    // Step 1: missing evidence, wherever it sits, before the variant table.
    for (diagnostic, reference) in [
        (
            ReplayError::Input(RetainedInputError::MissingObject(KEY.into())),
            KEY.to_owned(),
        ),
        (
            ReplayError::Input(RetainedInputError::MissingBlob(digest)),
            digest_hex(&digest),
        ),
        (
            ReplayError::Structure(RetainedWalkError::Graph(GraphError::Input(
                RetainedInputError::MissingObject(KEY.into()),
            ))),
            KEY.to_owned(),
        ),
        (
            ReplayError::Evaluation(EvaluationError::Reconstruction(
                opensip_evaluator::ReconstructionError::Record(GraphError::Input(
                    RetainedInputError::MissingBlob(digest),
                )),
            )),
            digest_hex(&digest),
        ),
    ] {
        assert_row(&refusal(diagnostic), EVIDENCE_MISSING, Some(&reference));
    }
    // Step 2: every variant of the table.
    for diagnostic in [
        ReplayError::Structure(RetainedWalkError::Limit),
        ReplayError::Structure(RetainedWalkError::Graph(GraphError::Law)),
        ReplayError::Capture(CaptureError::Limit),
        ReplayError::Capture(CaptureError::NotCapturing),
        ReplayError::Law,
        ReplayError::Input(RetainedInputError::ObjectIdentity),
        ReplayError::Input(RetainedInputError::ObjectDomain),
        ReplayError::Input(RetainedInputError::BlobDigest),
        ReplayError::Input(RetainedInputError::BlobLength),
        ReplayError::Input(RetainedInputError::NoncanonicalRecord),
        ReplayError::Input(RetainedInputError::InvalidRoleField),
        ReplayError::Evaluation(EvaluationError::Limit),
        ReplayError::Evaluation(EvaluationError::Law),
        ReplayError::Evaluation(EvaluationError::AtomRefused("atom")),
        ReplayError::Evaluation(EvaluationError::CompositionRefused("composition")),
    ] {
        assert_row(&refusal(diagnostic), INPUT_REFUSED, None);
    }
    for target in [None, Some(KEY.to_owned())] {
        assert_row(
            &refusal(ReplayError::Mismatch {
                key: "EVALUATOR_COMPLETE_PROOF_REPLAY",
                target,
            }),
            REGENERATION_MISMATCH,
            Some("run3:claimed"),
        );
    }
}

#[test]
fn the_remedies_are_the_route_and_carrier_text_byte_for_byte() {
    assert_eq!(REMEDY_EVIDENCE_MISSING, EVIDENCE_MISSING.5);
    assert_eq!(REMEDY_INPUT_REFUSED, INPUT_REFUSED.5);
    assert_eq!(REMEDY_REGENERATION_MISMATCH, REGENERATION_MISMATCH.5);
}

// ---------------------------------------------------------------- the corpus

#[test]
fn the_replay_corpus_replays_through_the_join_or_takes_its_row() {
    let cases = corpus();
    assert_eq!(cases.len(), 101);
    let outcomes = parallel(cases, |c| {
        replay(&c.run_id, &c.objects, &c.blobs, REPLAY_LIMITS).map(|r| r.run_id().to_owned())
    });
    let (mut lawful, mut forged, mut missing) = (0, 0, 0);
    for (c, outcome) in cases.iter().zip(outcomes) {
        if c.expected.contains_key("mismatch") {
            // A forged output: the corpus's one-byte or member alterations of
            // a claimed output, each re-identified, so only complete replay
            // can see them.
            let refusal = outcome.expect_err(&c.label);
            assert!(
                matches!(refusal.diagnostic(), ReplayError::Mismatch { .. }),
                "{}",
                c.label
            );
            assert_eq!(refusal.run_id(), c.run_id);
            assert_row(&refusal, REGENERATION_MISMATCH, Some(&c.run_id));
            forged += 1;
        } else if c.expected.contains_key("unavailable") {
            let refusal = outcome.expect_err(&c.label);
            let reference = string(&c.expected["unavailable"])
                .strip_prefix("EVIDENCE_UNAVAILABLE:")
                .unwrap();
            assert_row(&refusal, EVIDENCE_MISSING, Some(reference));
            missing += 1;
        } else {
            let run_id = outcome.unwrap_or_else(|e| panic!("{}: {e:?}", c.label));
            assert_eq!(run_id, c.run_id, "{}", c.label);
            let value = object(&c.expected["value"]);
            assert_eq!(run_id, string(&value["runId"]), "{}", c.label);
            lawful += 1;
        }
    }
    assert_eq!(missing, 1);
    assert!(forged >= 1 && lawful >= 1);
    assert_eq!(lawful + forged + missing, 101);
}

#[test]
fn the_corpus_missing_blob_case_is_evidence_missing_with_its_digest() {
    let c = case(MISSING_BLOB);
    let refusal = refused(replay(&c.run_id, &c.objects, &c.blobs, REPLAY_LIMITS));
    // The evaluator reports it under the walk, not as a top-level Input.
    assert!(matches!(refusal.diagnostic(), ReplayError::Structure(..)));
    let reference = MISSING_BLOB.strip_prefix("missing-blob-").unwrap();
    assert_eq!(
        refusal.diagnostic().unavailable_evidence(),
        Some(UnavailableEvidence::Blob(
            bytes(reference).try_into().unwrap()
        ))
    );
    assert_row(&refusal, EVIDENCE_MISSING, Some(reference));
}

#[test]
fn removing_any_member_of_the_claimed_closure_is_evidence_missing_naming_it() {
    let c = case(LAWFUL);
    let replayed = replay(&c.run_id, &c.objects, &c.blobs, REPLAY_LIMITS).unwrap();
    let read = replayed.retained_evidence();
    enum Removed {
        Object(String),
        Blob([u8; 32]),
    }
    let removals: Vec<Removed> = c
        .objects
        .keys()
        .cloned()
        .map(Removed::Object)
        .chain(c.blobs.keys().copied().map(Removed::Blob))
        .collect();
    let outcomes = parallel(&removals, |removed| {
        let (mut objects, mut blobs) = (copy(&c.objects), c.blobs.clone());
        let (reference, in_closure) = match removed {
            Removed::Object(key) => {
                objects.remove(key);
                (key.clone(), read.objects().contains_key(key))
            }
            Removed::Blob(digest) => {
                blobs.remove(digest);
                (digest_hex(digest), read.blobs().contains_key(digest))
            }
        };
        (
            reference,
            in_closure,
            replay(&c.run_id, &objects, &blobs, REPLAY_LIMITS).map(|r| r.run_id().to_owned()),
        )
    });
    let mut reached = 0;
    for (reference, in_closure, outcome) in outcomes {
        if in_closure {
            let refusal = outcome.expect_err(&reference);
            assert_row(&refusal, EVIDENCE_MISSING, Some(&reference));
            reached += 1;
        } else {
            // An ambient member the walk never reads.
            assert_eq!(outcome.expect(&reference), c.run_id);
        }
    }
    assert_eq!(reached, read.objects().len() + read.blobs().len());
    assert!(!read.objects().is_empty() && !read.blobs().is_empty());
}

#[test]
fn a_schema_or_identity_failure_is_input_refused_on_the_provider_return_route() {
    let c = case(LAWFUL);
    // An object whose descriptor no longer has its claimed identity.
    let mut objects = copy(&c.objects);
    let run = objects.get_mut(&c.run_id).unwrap();
    let V::Object(fields) = &mut run.descriptor else {
        panic!("run")
    };
    fields.insert("planId".into(), V::String("plan3:altered".into()));
    let refusal = refused(replay(&c.run_id, &objects, &c.blobs, REPLAY_LIMITS));
    assert_eq!(refusal.diagnostic().unavailable_evidence(), None);
    assert_row(&refusal, INPUT_REFUSED, None);
    // A read blob whose bytes are not its digest.
    let replayed = replay(&c.run_id, &c.objects, &c.blobs, REPLAY_LIMITS).unwrap();
    let digest = *replayed.retained_evidence().blobs().keys().next().unwrap();
    let mut blobs = c.blobs.clone();
    blobs.get_mut(&digest).unwrap().push(b'!');
    let refusal = refused(replay(&c.run_id, &c.objects, &blobs, REPLAY_LIMITS));
    assert_eq!(refusal.diagnostic().unavailable_evidence(), None);
    assert_row(&refusal, INPUT_REFUSED, None);
    // A domain the closure did not claim for the Run.
    let mut objects = copy(&c.objects);
    objects.get_mut(&c.run_id).unwrap().domain = IdentityDomain::Plan;
    let refusal = refused(replay(&c.run_id, &objects, &c.blobs, REPLAY_LIMITS));
    assert_row(&refusal, INPUT_REFUSED, None);
}

// ---------------------------------------------------------------- the bounds

/// One dimension of `ReplayLimits`: its name, its `REPLAY_LIMITS` value, and
/// `REPLAY_LIMITS` with only that dimension set.
struct Dimension {
    name: &'static str,
    constant: usize,
    with: fn(usize) -> ReplayLimits,
}
fn dimensions() -> Vec<Dimension> {
    let l = REPLAY_LIMITS;
    vec![
        Dimension {
            name: "walk.steps",
            constant: l.retained.walk.steps,
            with: |n| {
                let mut l = REPLAY_LIMITS;
                l.retained.walk.steps = n;
                l
            },
        },
        Dimension {
            name: "walk.depth",
            constant: l.retained.walk.depth,
            with: |n| {
                let mut l = REPLAY_LIMITS;
                l.retained.walk.depth = n;
                l
            },
        },
        Dimension {
            name: "walk.descriptor_work",
            constant: l.retained.walk.descriptor_work,
            with: |n| {
                let mut l = REPLAY_LIMITS;
                l.retained.walk.descriptor_work = n;
                l
            },
        },
        Dimension {
            name: "owner.steps",
            constant: l.retained.owner.steps,
            with: |n| {
                let mut l = REPLAY_LIMITS;
                l.retained.owner.steps = n;
                l
            },
        },
        Dimension {
            name: "owner.depth",
            constant: l.retained.owner.depth,
            with: |n| {
                let mut l = REPLAY_LIMITS;
                l.retained.owner.depth = n;
                l
            },
        },
        Dimension {
            name: "owner.descriptor_work",
            constant: l.retained.owner.descriptor_work,
            with: |n| {
                let mut l = REPLAY_LIMITS;
                l.retained.owner.descriptor_work = n;
                l
            },
        },
        Dimension {
            name: "owner_invocations",
            constant: l.retained.owner_invocations,
            with: |n| {
                let mut l = REPLAY_LIMITS;
                l.retained.owner_invocations = n;
                l
            },
        },
        Dimension {
            name: "capture_entries",
            constant: l.capture_entries,
            with: |n| ReplayLimits {
                capture_entries: n,
                ..REPLAY_LIMITS
            },
        },
        Dimension {
            name: "retained_bytes",
            constant: l.retained_bytes,
            with: |n| ReplayLimits {
                retained_bytes: n,
                ..REPLAY_LIMITS
            },
        },
    ]
}

#[test]
fn the_replay_limits_are_the_item_5e_values() {
    let budget = |b: TraversalBudget| (b.steps, b.depth, b.descriptor_work);
    let l = REPLAY_LIMITS;
    assert_eq!(budget(l.retained.walk), (20_000_000, 96, 20_000_000));
    assert_eq!(budget(l.retained.owner), (20_000_000, 96, 20_000_000));
    assert_eq!(l.retained.owner_invocations, 100_000);
    assert_eq!(l.capture_entries, 100_000);
    assert_eq!(l.retained_bytes, 33_554_432);
}

#[test]
fn each_bound_admits_the_corpus_at_its_exact_need_and_refuses_one_below() {
    let c = case(LAWFUL);
    let replayed = replay(&c.run_id, &c.objects, &c.blobs, REPLAY_LIMITS).unwrap();
    let passes = |limits: ReplayLimits| replay(&c.run_id, &c.objects, &c.blobs, limits).is_ok();
    let needs = parallel(&dimensions(), |d| {
        // The least value that replays, by bisection over [0, constant]:
        // every bound is a count that only ever refuses when exceeded.
        assert!(passes((d.with)(d.constant)), "{}", d.name);
        let (mut low, mut high) = (0usize, d.constant);
        while low < high {
            let mid = low + (high - low) / 2;
            if passes((d.with)(mid)) {
                high = mid;
            } else {
                low = mid + 1;
            }
        }
        (d.name, d.constant, low, d.with)
    });
    for (name, constant, need, with) in needs {
        assert!(need >= 1 && need <= constant, "{name}: {need}");
        let at = replay(&c.run_id, &c.objects, &c.blobs, with(need)).expect(name);
        assert_eq!(at.run_id(), c.run_id, "{name}");
        let below = refused(replay(&c.run_id, &c.objects, &c.blobs, with(need - 1)));
        assert_eq!(below.diagnostic().unavailable_evidence(), None, "{name}");
        assert_row(&below, INPUT_REFUSED, None);
        // The two capture bounds are exact counts of this corpus.
        match name {
            "capture_entries" => assert_eq!(need, c.objects.len() + c.blobs.len()),
            "retained_bytes" => assert_eq!(need, replayed.retained_evidence().byte_length()),
            _ => {}
        }
    }
}

#[test]
fn the_capture_entry_bound_holds_at_the_constant_itself() {
    let c = case(LAWFUL);
    // Ambient entries, never read, pad the inputs to exactly the bound.
    let mut blobs = c.blobs.clone();
    let mut n: u64 = 0;
    while c.objects.len() + blobs.len() < REPLAY_LIMITS.capture_entries {
        let mut key = [0xee; 32];
        key[..8].copy_from_slice(&n.to_be_bytes());
        n += 1;
        assert!(blobs.insert(key, Vec::new()).is_none());
    }
    let at = replay(&c.run_id, &c.objects, &blobs, REPLAY_LIMITS).unwrap();
    assert_eq!(at.run_id(), c.run_id);
    let mut key = [0xee; 32];
    key[..8].copy_from_slice(&n.to_be_bytes());
    blobs.insert(key, Vec::new());
    let above = refused(replay(&c.run_id, &c.objects, &blobs, REPLAY_LIMITS));
    assert_eq!(
        above.diagnostic(),
        &ReplayError::Capture(CaptureError::Limit)
    );
    assert_row(&above, INPUT_REFUSED, None);
}

// ---------------------------------------------------------------- source pins

/// fact_admission.rs without its test module.
fn production_source() -> &'static str {
    let text = include_str!("fact_admission.rs");
    let (production, tests) = text.split_once("#[cfg(test)]").unwrap();
    assert_eq!(
        tests.trim(),
        "mod tests {\n    include!(\"fact_admission_tests.rs\");\n}"
    );
    production
}
fn code_only(source: &str) -> String {
    source
        .lines()
        .filter(|line| !line.trim_start().starts_with("//"))
        .collect::<Vec<_>>()
        .join("\n")
}

#[test]
fn the_join_calls_replay_run_once_and_mints_nothing_itself() {
    let source = code_only(production_source());
    // The only evaluator names are the boundary types and replay_run.
    assert_eq!(source.matches("opensip_evaluator").count(), 1);
    assert!(source.contains(
        "use opensip_evaluator::{ReplayError, ReplayLimits, ReplayedRun, RetainedWalkLimits, replay_run};"
    ));
    assert_eq!(source.matches("replay_run(").count(), 1);
    // The only evaluator method used on a refusal is its own classification.
    assert_eq!(source.matches(".unavailable_evidence()").count(), 1);
    // No ReplayedRun, RunId or verdict is built here, and no other join is
    // wired into replay (X12 r3 item 9 leaves check_plan_pack unwired).
    for forbidden in [
        "ReplayedRun {",
        "ReplayedRun::",
        "run3:",
        "verdict",
        "check_plan_pack",
        "admit_pack",
        "derive_evaluation",
        "inspect_",
        "policy_derivation",
        "retained_evidence",
        "Default",
        "Clone",
        "Serialize",
        "Deserialize",
    ] {
        assert!(!source.contains(forbidden), "{forbidden}");
    }
    // Pure: no custody, storage, lock, ledger, I/O, environment or process.
    for forbidden in [
        "opensip_security",
        "opensip_storage",
        "opensip_platform",
        "opensip_lifecycle",
        "WorkLedger",
        "fs::",
        "env::",
        "Command",
        "Mutex",
        "OnceLock",
        "static mut",
        "unsafe",
    ] {
        assert!(!source.contains(forbidden), "{forbidden}");
    }
    // Step 2 has no wildcard arm.
    assert!(!source.contains("_ =>"));
}

/// Item 5d: every production call of `replay_candidate(` under
/// `crates/host/src` passes `REPLAY_LIMITS` as written. Returns the calls.
fn limits_pin(sources: &[(String, String)]) -> Result<usize, String> {
    let mut calls = 0;
    for (name, text) in sources {
        let text = code_only(text);
        for (at, _) in text.match_indices("replay_candidate(") {
            if text[..at].ends_with("fn ") {
                continue;
            }
            let rest = &text[at + "replay_candidate(".len()..];
            let mut depth = 1usize;
            let end = rest
                .char_indices()
                .find(|&(_, ch)| {
                    match ch {
                        '(' => depth += 1,
                        ')' => depth -= 1,
                        _ => {}
                    }
                    depth == 0
                })
                .map(|(i, _)| i)
                .ok_or_else(|| format!("{name}: unclosed call"))?;
            let args = &rest[..end];
            // The last top-level argument, exactly the host constant.
            let mut nesting = 0usize;
            let mut last = 0usize;
            for (i, ch) in args.char_indices() {
                match ch {
                    '(' | '[' | '{' => nesting += 1,
                    ')' | ']' | '}' => nesting = nesting.saturating_sub(1),
                    ',' if nesting == 0 && !args[i + 1..].trim().is_empty() => last = i + 1,
                    _ => {}
                }
            }
            let limits = args[last..].trim().trim_end_matches(',').trim();
            if !matches!(
                limits,
                "REPLAY_LIMITS"
                    | "fact_admission::REPLAY_LIMITS"
                    | "crate::fact_admission::REPLAY_LIMITS"
            ) {
                return Err(format!("{name}: replay_candidate({args})"));
            }
            calls += 1;
        }
    }
    Ok(calls)
}
fn host_production_sources() -> Vec<(String, String)> {
    let root = std::path::Path::new(env!("CARGO_MANIFEST_DIR")).join("src");
    let mut out = Vec::new();
    let mut stack = vec![root];
    while let Some(dir) = stack.pop() {
        for entry in std::fs::read_dir(&dir).unwrap() {
            let path = entry.unwrap().path();
            let name = path.file_name().unwrap().to_string_lossy().into_owned();
            if path.is_dir() {
                stack.push(path);
            } else if name.ends_with(".rs") && !name.ends_with("_tests.rs") && name != "tests.rs" {
                let text = std::fs::read_to_string(&path).unwrap();
                // A module's own `#[cfg(test)]` tail is not production.
                let text = text
                    .split("#[cfg(test)]\nmod tests")
                    .next()
                    .unwrap()
                    .to_owned();
                out.push((name, text));
            }
        }
    }
    out
}

#[test]
fn every_production_caller_passes_the_host_replay_limits() {
    let sources = host_production_sources();
    assert!(sources.iter().any(|(name, _)| name == "fact_admission.rs"));
    // X7a's `finalize` is the one production caller; never a caller-chosen
    // value.
    assert!(sources.iter().any(|(name, _)| name == "finalization.rs"));
    assert_eq!(limits_pin(&sources).unwrap(), 1);
}

#[test]
fn the_limits_pin_refuses_a_caller_chosen_value() {
    let lawful = |body: &str| vec![("finalization.rs".to_owned(), body.to_owned())];
    assert_eq!(
        limits_pin(&lawful(
            "let r = replay_candidate(&candidate, REPLAY_LIMITS);"
        )),
        Ok(1)
    );
    assert_eq!(
        limits_pin(&lawful(
            "let r = replay_candidate(\n    &candidate,\n    crate::fact_admission::REPLAY_LIMITS,\n);"
        )),
        Ok(1)
    );
    assert_eq!(
        limits_pin(&lawful(
            "pub(crate) fn replay_candidate(c: &C, limits: L) {}"
        )),
        Ok(0)
    );
    for chosen in [
        "replay_candidate(&candidate, limits)",
        "replay_candidate(&candidate, ReplayLimits { capture_entries: 1, ..REPLAY_LIMITS })",
        "replay_candidate(&candidate, REPLAY_LIMITS_FOR_TESTS)",
        "replay_candidate(&candidate, my_REPLAY_LIMITS)",
        "replay_candidate(&candidate)",
        "replay_candidate(&c, mine(REPLAY_LIMITS, 2))",
    ] {
        assert!(limits_pin(&lawful(chosen)).is_err(), "{chosen}");
    }
}
