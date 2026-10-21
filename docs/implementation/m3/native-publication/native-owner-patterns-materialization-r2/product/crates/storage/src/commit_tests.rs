// Law X3d r6 (unit X3d-2), storage's half: these tests run the very
// functions `prepare_commit` and `publish` compose, on a scratch `I/stores/S`
// under the per-process scratch parent, with the evaluator's real replay: the
// plan and its binding, the store generation digest, the layout, the
// publication reserve, attempt admission and the objects, the evidence
// ledger's level 3, the adapter's staging and its one COMMIT, the receipt
// counter and the rows.
//
// Law X3d r8 item 13 (unit X3d-3): a test's binding values come from a real
// session, never from the Run under test. `bound()` takes the project and the
// core evaluator closure from a `CommitSession` opened over X8b's
// `scenario-fixtures` `ProjectOperation` (a synthetic installation under the
// scratch parent), and the Run replayed is the synthetic run candidate built
// for that session (X9 r7). `the_first_real_commit_*` composes
// `prepare_commit` and `publish` end to end with a real session. Nothing here
// opens a real home or installation.
use super::*;
use crate::recovery::{LedgerStanding, SuppliedBinding, join_ledger};
use opensip_identity::{IdentityDomain, ObjectInput, RetainedInputs, TraversalBudget, parse_json};
use opensip_platform::{RetainedDirectory, WorkLedger};
use opensip_security::scenario::ScenarioHome;
use std::collections::{BTreeMap, BTreeSet};
use std::fs;
use std::os::unix::fs::{MetadataExt, PermissionsExt};
use std::path::PathBuf;

const STORE: &str = "0123456789abcdef0123456789abcdef";
const N: &str = "6f1c2a4e-3b5d-4c7e-9f10-1a2b3c4d5e6f";
const EXEC: &str = "exec1_0123456789abcdef0123456789abcdef";
const EXEC2: &str = "exec1_fedcba9876543210fedcba9876543210";
const OP: &str = "op-0123456789abcdef0123456789abcdef";
const OP2: &str = "op-fedcba9876543210fedcba9876543210";

// ---------------------------------------------------------------- fixtures

fn object(v: &V) -> &BTreeMap<String, V> {
    match v {
        V::Object(o) => o,
        _ => panic!("object"),
    }
}
fn string(v: &V) -> &str {
    match v {
        V::String(s) => s,
        _ => panic!("string"),
    }
}
fn bytes(s: &str) -> Vec<u8> {
    s.as_bytes()
        .chunks_exact(2)
        .map(|p| u8::from_str_radix(std::str::from_utf8(p).unwrap(), 16).unwrap())
        .collect()
}
// Law X3d r8 item 13: the synthetic run candidate, the same source file
// storage's `crash_matrix_support` compiles under the feature. Storage's
// plain test build has no support module, so it is included here by path
// rather than gated anew; in a test build with the feature, both copies
// compile, which is all `duplicate_mod` reports.
#[allow(clippy::duplicate_mod)]
#[path = "crash_matrix_support/run_candidate.rs"]
mod run_candidate;
use run_candidate::{SyntheticRunCandidate, synthetic_replay_limits, synthetic_run_candidate};

/// A real session's binding values (law X3d r8 item 13), with the synthetic
/// candidate built for it. Taken once per process from a `CommitSession`
/// opened over X8b's `scenario-fixtures` operation; the session then ends
/// (`refused`, then `finish`) and its scratch home is removed.
struct SessionValues {
    project: String,
    evaluator_closure: String,
    core_closure: String,
    candidate: SyntheticRunCandidate,
}
fn session_values() -> &'static SessionValues {
    static VALUES: std::sync::OnceLock<SessionValues> = std::sync::OnceLock::new();
    VALUES.get_or_init(|| {
        let home = ScenarioHome::create(&crate::test_scratch::temp_dir());
        let root = home.project("x3d3-values");
        let session = CommitSession::open(home.operation(&root).unwrap()).unwrap();
        let values = SessionValues {
            project: session.project_id().into(),
            evaluator_closure: session.core_evaluator_closure().into(),
            core_closure: session.core_closure().into(),
            candidate: synthetic_run_candidate(&session),
        };
        let end = session.reserve_end_path().unwrap().refused().finish();
        assert!(end.end_step_entered());
        values
    })
}
/// The evaluator's full replay of the synthetic candidate built for the
/// session of `session_values` (`replay_run`, the only `ReplayedRun` mint).
fn replay() -> ReplayedRun {
    let candidate = &session_values().candidate;
    opensip_evaluator::replay_run(
        &candidate.retained_inputs(),
        candidate.run_id(),
        synthetic_replay_limits(),
    )
    .unwrap()
}
/// The evaluator's full replay of the pinned corpus Run that security's SEAL
/// tests replay (`crates/security/tests/fixtures/journal-seal-replay.native-owner-r1.json`).
/// It names neither the session's project nor its core evaluator closure.
fn corpus_replay() -> ReplayedRun {
    let raw = fs::read(
        std::path::Path::new(env!("CARGO_MANIFEST_DIR"))
            .join("../security/tests/fixtures/journal-seal-replay.native-owner-r1.json"),
    )
    .unwrap();
    let f = parse_json(&raw).unwrap();
    let f = object(&f);
    let c = object(&f["case"]);
    let V::Array(keys) = &c["objects"] else {
        panic!("objects")
    };
    let objects: BTreeMap<String, ObjectInput> = keys
        .iter()
        .map(|k| {
            let r = object(&object(&f["objectPool"])[string(k)]);
            (
                string(&r["id"]).into(),
                ObjectInput {
                    domain: IdentityDomain::parse(string(&r["domain"])).unwrap(),
                    descriptor: r["descriptor"].clone(),
                },
            )
        })
        .collect();
    let V::Array(keys) = &c["blobs"] else {
        panic!("blobs")
    };
    let blobs: BTreeMap<[u8; 32], Vec<u8>> = keys
        .iter()
        .map(|k| {
            let r = object(&object(&f["blobPool"])[string(k)]);
            (
                bytes(string(&r["digest"])).try_into().unwrap(),
                bytes(string(&r["hex"])),
            )
        })
        .collect();
    let bound = TraversalBudget {
        steps: 20_000_000,
        depth: 96,
        descriptor_work: 20_000_000,
    };
    let registry = crate::schema_sources::registry().unwrap();
    let inputs = RetainedInputs::new(registry, &objects, &blobs);
    opensip_evaluator::replay_run(
        &inputs,
        string(&c["runId"]),
        opensip_evaluator::ReplayLimits {
            retained: opensip_evaluator::RetainedWalkLimits {
                walk: bound,
                owner: bound,
                owner_invocations: 100_000,
            },
            capture_entries: 100_000,
            retained_bytes: 32 * 1024 * 1024,
        },
    )
    .unwrap()
}
/// A real session's binding values (law X3d r8 item 13): the project and the
/// core evaluator closure from `session_values`, never from a Run; the store
/// values name this file's scratch `I/stores/S`.
fn bound(execution: &str, operation: &str) -> Bound {
    let values = session_values();
    Bound {
        project: values.project.clone(),
        evaluator_closure: values.evaluator_closure.clone(),
        namespace: N.into(),
        store: STORE.into(),
        generation: 1,
        schema: 2,
        carrier: sha256_hex(N.as_bytes()),
        execution: execution.into(),
        operation: operation.into(),
    }
}
fn sealed<'a>(planned: &'a Planned, seq: i64) -> Sealed<'a> {
    Sealed {
        carrier: &planned.carrier,
        generation: 1,
        seq,
        body: "1111111111111111111111111111111111111111111111111111111111111111",
        operation: &planned.operation,
        run_id: &planned.run_id,
    }
}

/// A scratch `I/stores/S`, private, as the session's store root lends it.
struct Store {
    root: PathBuf,
    path: PathBuf,
    directory: RetainedDirectory,
    uid: u32,
}
impl Store {
    fn new() -> Self {
        let tag: String = opensip_platform::request_entropy()
            .unwrap()
            .iter()
            .map(|b| format!("{b:02x}"))
            .collect();
        let p = crate::test_scratch::temp_dir().join(format!("opensip-x3d2-{tag}"));
        fs::create_dir(&p).unwrap();
        let root = fs::canonicalize(&p).unwrap();
        let path = root.join("stores").join(STORE);
        fs::create_dir_all(&path).unwrap();
        fs::set_permissions(&path, fs::Permissions::from_mode(0o700)).unwrap();
        let directory =
            RetainedDirectory::from_retained_handle(fs::File::open(&path).unwrap()).unwrap();
        let uid = fs::metadata(&path).unwrap().uid();
        Self {
            root,
            path,
            directory,
            uid,
        }
    }
    fn location(&self) -> ProjectStoreLocation<'_> {
        self.location_in(N)
    }
    /// X3c r8 (unit X3c-3): the same store's location for another namespace.
    fn location_in(&self, namespace: &str) -> ProjectStoreLocation<'_> {
        ProjectStoreLocation::selected(
            &self.directory,
            self.path.clone(),
            ProjectStoreNames::new(STORE, namespace).unwrap(),
            self.uid,
        )
    }
    fn ledger(&self) -> rusqlite::Connection {
        self.ledger_in(N)
    }
    fn ledger_in(&self, namespace: &str) -> rusqlite::Connection {
        rusqlite::Connection::open_with_flags(
            self.path
                .join("projects")
                .join(namespace)
                .join("ledger.sqlite"),
            rusqlite::OpenFlags::SQLITE_OPEN_READ_ONLY | rusqlite::OpenFlags::SQLITE_OPEN_NO_MUTEX,
        )
        .unwrap()
    }
    fn count(&self, table: &str) -> i64 {
        self.count_in(N, table)
    }
    fn count_in(&self, namespace: &str, table: &str) -> i64 {
        self.ledger_in(namespace)
            .query_row(&format!("SELECT count(*) FROM {table}"), [], |r| r.get(0))
            .unwrap()
    }
    fn objects(&self) -> BTreeSet<String> {
        fs::read_dir(self.path.join("projects").join(N).join("objects/sha256"))
            .unwrap()
            .map(|e| e.unwrap().file_name().into_string().unwrap())
            .collect()
    }
}
impl Drop for Store {
    fn drop(&mut self) {
        let _ = fs::remove_dir_all(&self.root);
    }
}

/// `prepare_commit`'s storage steps after the session's: the plan, the
/// layout, then attempt admission and the objects under the reserve.
struct Prepared {
    planned: Planned,
    layout: Layout,
    attempt: AdmittedAttempt,
    objects: PublishedObjects,
}
fn prepare(store: &Store, work: &mut WorkLedger, run: &ReplayedRun, b: &Bound) -> Prepared {
    let (planned, declared) = plan(run, b).unwrap();
    let location = store.location_in(&b.namespace);
    let layout = work.scope(|w| admit_layout(&location, w)).unwrap();
    let (attempt, objects) = work
        .scope(|w| {
            admit_and_publish(
                &location,
                &layout,
                &attempt_record(&planned),
                declared,
                w,
                Box::new(|| {}),
            )
        })
        .unwrap();
    Prepared {
        planned,
        layout,
        attempt,
        objects,
    }
}
/// `publish`'s storage steps: the evidence ledger's level 3, then staging
/// after a SEAL at `seq`.
fn staged(work: &mut WorkLedger, p: Prepared, seq: i64) -> (Planned, Refused<Staged>) {
    let Prepared {
        planned,
        layout,
        attempt,
        objects,
    } = p;
    let prepared = work
        .scope(|w| begin_prepared_ledger(&layout.ledger, &attempt, objects, w))
        .unwrap();
    let result = work.scope(|w| stage(prepared, &planned, &sealed(&planned, seq), w));
    (planned, result)
}

// -------------------------------------------------------------------- plan

#[test]
fn the_plan_declares_exactly_the_retained_frames_and_blobs() {
    let run = replay();
    let (planned, declared) = plan(&run, &bound(EXEC, OP)).unwrap();
    let evidence = run.retained_evidence();
    // The inventory lists every retained typed object and raw blob, in order.
    let inventory = parse_json(&planned.inventory).unwrap();
    let inventory = object(&inventory);
    let listed = |key: &str| -> Vec<String> {
        let V::Array(values) = &inventory[key] else {
            panic!("{key}")
        };
        values.iter().map(|v| string(v).to_owned()).collect()
    };
    assert_eq!(
        listed("objects"),
        evidence.object_frames().keys().cloned().collect::<Vec<_>>()
    );
    assert_eq!(
        listed("blobDigests"),
        evidence.blobs().keys().map(digest_hex).collect::<Vec<_>>()
    );
    assert_eq!(string(&inventory["runId"]), run.run_id());
    assert_eq!(planned.inventory_digest, sha256_hex(&planned.inventory));
    assert!(!evidence.object_frames().is_empty() && !evidence.blobs().is_empty());
    // Every frame is its identity's H preimage, published under that digest;
    // every blob under its raw digest; nothing twice.
    let mut digests = BTreeSet::new();
    for (id, frame) in evidence.object_frames() {
        assert_eq!(h_digest(id), Some(sha256_hex(frame).as_str()));
        digests.insert(sha256_hex(frame));
    }
    for digest in evidence.blobs().keys() {
        digests.insert(digest_hex(digest));
    }
    assert_eq!(declared.len(), digests.len());
    assert_eq!(planned.manifest, canonical_bytes(run.run()).unwrap());
}

#[test]
fn a_run_of_another_project_or_closure_does_not_bind() {
    let run = replay();
    let b = bound(EXEC, OP);
    // The candidate binds to the real session's project and closure.
    assert!(plan(&run, &b).is_ok());
    let V::Object(descriptor) = run.run() else {
        panic!("run")
    };
    assert_eq!(string(&descriptor["projectId"]), b.project);
    assert_eq!(run.evaluator_closure(), b.evaluator_closure);
    let mut other = bound(EXEC, OP);
    other.project = format!("prj1-{}", "0".repeat(64));
    assert_eq!(plan(&run, &other).err(), Some(PlanRefusal::Project));
    let mut other = bound(EXEC, OP);
    other.evaluator_closure = format!("closure2:{}", "0".repeat(64));
    assert_eq!(plan(&run, &other).err(), Some(PlanRefusal::Closure));
}

/// Law X3d r8 item 13: the pinned corpus Run, whose evaluator closure is not
/// the session's, is refused `PlanRefusal::Closure` on the invariant row
/// (item 3 step 1). Its project is first rebound to the session's (only that
/// member, as the candidate rebinds it), so the closure is the one
/// difference; the raw corpus Run is refused on its project first. Then the
/// same refusal through `prepare_commit` on a real session: the invariant
/// row, nothing written, and the end path's `REV`.
#[test]
fn a_corpus_run_does_not_bind_to_a_real_session() {
    let b = bound(EXEC, OP);
    let corpus = corpus_replay();
    assert_ne!(corpus.evaluator_closure(), b.evaluator_closure);
    assert_eq!(plan(&corpus, &b).err(), Some(PlanRefusal::Project));
    let rebound = |project: &str| {
        let candidate = run_candidate::project_rebound_corpus(project);
        opensip_evaluator::replay_run(
            &candidate.retained_inputs(),
            candidate.run_id(),
            synthetic_replay_limits(),
        )
        .unwrap()
    };
    let run = rebound(&b.project);
    let V::Object(descriptor) = run.run() else {
        panic!("run")
    };
    assert_eq!(string(&descriptor["projectId"]), b.project);
    assert_eq!(run.evaluator_closure(), corpus.evaluator_closure());
    assert_eq!(plan(&run, &b).err(), Some(PlanRefusal::Closure));

    let home = ScenarioHome::create(&crate::test_scratch::temp_dir());
    let root = home.project("x3d3-mismatch");
    let session = CommitSession::open(home.operation(&root).unwrap()).unwrap();
    let (namespace, store) = (
        session.namespace_id().to_owned(),
        session.store_instance().to_owned(),
    );
    let run = rebound(session.project_id());
    assert_ne!(run.evaluator_closure(), session.core_evaluator_closure());
    let Err((NotPrepared::Refused(row), stopped)) = prepare_commit(run, session) else {
        panic!("prepared")
    };
    assert_eq!(row, T::Invariant);
    let end = stopped.finish();
    assert!(end.revocation_appended());
    let census = home.carrier_census(&namespace).unwrap();
    assert_eq!((census.seal, census.rev), (0, 1));
    assert!(
        !home
            .installation()
            .join("stores")
            .join(&store)
            .join("projects")
            .join(&namespace)
            .exists()
    );
}

/// Law X3d r8 item 13: a session's core evaluator closure is not its core
/// closure, and a Run naming the core closure cannot be replayed, because
/// replay admits only an evaluator closure of `kind: "evaluator"`. So no Run
/// passes step 1 by naming the core closure.
#[test]
fn the_core_closure_is_not_the_evaluator_closure() {
    let values = session_values();
    assert_ne!(values.core_closure, values.evaluator_closure);
    assert!(values.core_closure.starts_with("closure2:"));
    assert!(values.evaluator_closure.starts_with("closure2:"));
    // The candidate retains the session's closure as `kind: "evaluator"`.
    let retained = &values.candidate.objects()[&values.evaluator_closure];
    let V::Object(closure) = &retained.descriptor else {
        panic!("closure")
    };
    assert_eq!(closure["kind"], V::String("evaluator".into()));
    // The same descriptor with `kind: "core"` is the session's core closure.
    let mut core = closure.clone();
    core.insert("kind".into(), V::String("core".into()));
    let core_id = format!(
        "closure2:{}",
        digest_hex(
            &opensip_identity::hash_canonical_value("closure", &V::Object(core.clone())).unwrap()
        )
    );
    assert_eq!(core_id, values.core_closure);
    // A Run whose seal names the core closure is refused by replay: the
    // retained closure is not of the evaluator kind its field requires.
    let replay_of = |candidate: &SyntheticRunCandidate| {
        opensip_evaluator::replay_run(
            &candidate.retained_inputs(),
            candidate.run_id(),
            synthetic_replay_limits(),
        )
        .map(|run| run.evaluator_closure().to_owned())
    };
    let named = run_candidate::renaming_the_evaluator_closure(&values.candidate, V::Object(core));
    assert!(named.objects().contains_key(&values.core_closure));
    assert_eq!(
        replay_of(&named).err(),
        Some(opensip_evaluator::ReplayError::Structure(
            opensip_evaluator::RetainedWalkError::Graph(opensip_identity::GraphError::Input(
                opensip_identity::RetainedInputError::Candidate(
                    opensip_identity::CandidateError::Schema(
                        opensip_identity::SchemaAdmissionError::Mismatch
                    )
                )
            ))
        ))
    );
    // The control: the same rewrite to another closure of `kind:
    // "evaluator"` replays, so the refusal above is the kind.
    let mut other = closure.clone();
    other.insert("semanticVersion".into(), V::String("0.0.1-x3d3".into()));
    let renamed =
        run_candidate::renaming_the_evaluator_closure(&values.candidate, V::Object(other));
    let replayed = replay_of(&renamed).unwrap();
    assert_ne!(replayed, values.evaluator_closure);
    assert_ne!(replayed, values.core_closure);
}

#[test]
fn the_store_generation_digest_is_the_lineage_recipe() {
    // Raw SHA-256 over the canonical five-member binding: sorted keys,
    // compact separators, integers as integers, no domain framing.
    let canonical = format!(
        r#"{{"namespaceId":"{N}","schemaVersion":1,"stateSchema":2,"storeGeneration":7,"storeInstanceId":"{STORE}"}}"#
    );
    assert_eq!(
        store_generation_digest(N, STORE, 7, 2).unwrap(),
        sha256_hex(canonical.as_bytes())
    );
    assert_ne!(
        store_generation_digest(N, STORE, 7, 2),
        store_generation_digest(N, STORE, 8, 2)
    );
}

// ------------------------------------------------------------ the pipeline

#[test]
fn a_prepared_commit_stages_every_row_and_writes_them_only_at_its_commit() {
    let run = replay();
    let store = Store::new();
    let mut work = WorkLedger::new();
    let p = prepare(&store, &mut work, &run, &bound(EXEC, OP));
    let store_digest = p.planned.store_digest.clone();
    // The attempt row is durable and the objects are published before level 3.
    assert_eq!(store.count("attempt_custody"), 1);
    let (planned, _) = plan(&run, &bound(EXEC, OP)).unwrap();
    let evidence = run.retained_evidence();
    let expected: BTreeSet<String> = evidence
        .object_frames()
        .values()
        .map(|frame| sha256_hex(frame))
        .chain(evidence.blobs().keys().map(digest_hex))
        .collect();
    assert_eq!(store.objects(), expected);
    for (id, frame) in evidence.object_frames() {
        let name = h_digest(id).unwrap();
        assert_eq!(
            fs::read(
                store
                    .path
                    .join("projects")
                    .join(N)
                    .join("objects/sha256")
                    .join(name)
            )
            .unwrap(),
            *frame
        );
    }
    let (_, result) = staged(&mut work, p, 9);
    let staged = result.unwrap();
    // Staged, nothing committed: another connection sees no receipt.
    assert_eq!(store.count("commit_receipts"), 0);
    assert_eq!(staged.sequence, 1);
    let receipt = staged.receipt.clone();
    let EvidenceCommit::Committed(committed) = staged.commit() else {
        panic!("committed")
    };
    assert_eq!(committed.receipt, receipt);
    assert_eq!(committed.sequence, 1);
    // Every row, once.
    for table in [
        "commit_receipts",
        "commit_associations",
        "commit_run_material",
        "evidence_availability",
    ] {
        assert_eq!(store.count(table), 1, "{table}");
    }
    assert_eq!(store.count("active_run_pins"), 0);
    let c = store.ledger();
    let body: Vec<u8> = c
        .query_row("SELECT body FROM commit_receipts", [], |r| r.get(0))
        .unwrap();
    assert_eq!(body, receipt);
    let r = ReceiptCandidate::parse(&body).unwrap();
    assert_eq!(
        (
            r.run.as_str(),
            r.execution.as_str(),
            r.namespace.as_str(),
            r.sequence
        ),
        (run.run_id(), EXEC, N, 1)
    );
    assert_eq!(r.inventory, planned.inventory_digest);
    assert_eq!(
        (r.assurance.as_str(), r.signer.as_str()),
        (SEALED_ASSURANCE, RECEIPT_SIGNER)
    );
    let raw: Vec<u8> = c
        .query_row("SELECT body FROM commit_associations", [], |r| r.get(0))
        .unwrap();
    let a = AssociationCandidate::parse(&raw).unwrap();
    assert_eq!(a.store, store_digest);
    assert_eq!((a.generation, a.journal_seq), (1, 9));
    assert_eq!(a.sequence.text, "1");
    assert_eq!(a.operation, OP);
    assert_eq!(a.carrier, planned.carrier);
    // The pair joins the admitted attempt: committed, settlement pending.
    let binding = SuppliedBinding {
        store: &store_digest,
        namespace: N,
        carrier: &planned.carrier,
        execution: EXEC,
    };
    assert_eq!(
        join_ledger(
            &binding,
            Some(&r),
            Some(&a),
            Some(&attempt_record(&planned))
        ),
        LedgerStanding::ContinueCarrier {
            pending_settlement: true,
            legacy_custody_unknown: false,
        }
    );
    let (generation, state): (String, Vec<u8>) = c
        .query_row(
            "SELECT generation, body FROM evidence_availability",
            [],
            |r| Ok((r.get(0)?, r.get(1)?)),
        )
        .unwrap();
    assert_eq!(generation, "0");
    assert!(String::from_utf8(state).unwrap().contains("\"retained\""));
}

#[test]
fn the_counter_orders_by_length_then_bytes_and_starts_at_one() {
    let run = replay();
    let store = Store::new();
    let mut work = WorkLedger::new();
    let p = prepare(&store, &mut work, &run, &bound(EXEC, OP));
    let (_, result) = staged(&mut work, p, 9);
    assert!(matches!(
        result.unwrap().commit(),
        EvidenceCommit::Committed(Committed { sequence: 1, .. })
    ));
    // Earlier associations at 2, 9, 10 and 100: lexical order would pick 9.
    let path = store.path.join("projects").join(N).join("ledger.sqlite");
    let digest = store_generation_digest(N, STORE, 1, 2).unwrap();
    let plant = |sequence: &str, execution: char| {
        let c = rusqlite::Connection::open(&path).unwrap();
        c.execute(
            "INSERT INTO commit_associations VALUES(?1,?2,?3,?4,?5,1,?6,x'00')",
            rusqlite::params![
                digest,
                N,
                format!("exec1_{}", execution.to_string().repeat(32)),
                sequence,
                "a".repeat(64),
                sequence.len() as i64 * 100 + i64::from(execution as u8),
            ],
        )
        .unwrap();
    };
    for (sequence, execution) in [("2", 'a'), ("9", 'b'), ("10", 'c'), ("100", 'd')] {
        plant(sequence, execution);
    }
    let next = |work: &mut WorkLedger, execution: &str, operation: &str| {
        let p = prepare(&store, work, &run, &bound(execution, operation));
        let prepared = work
            .scope(|w| begin_prepared_ledger(&p.layout.ledger, &p.attempt, p.objects, w))
            .unwrap();
        work.scope(|w| prepared.next_commit_sequence(w))
    };
    assert_eq!(next(&mut work, EXEC2, OP2).unwrap(), 101);
    // A full u64 counter refuses on the invariant row; nothing wraps.
    plant("18446744073709551615", 'e');
    let mut fresh = WorkLedger::new();
    let exhausted = next(&mut fresh, "exec1_99999999999999999999999999999999", OP);
    assert!(matches!(
        exhausted,
        Err(WorkFailure::Operation(ref r)) if r.row() == ProjectLedgerRow::Invariant
    ));
}

#[test]
fn a_seal_binding_that_does_not_join_stages_nothing() {
    let run = replay();
    for case in 0..3 {
        let store = Store::new();
        let mut work = WorkLedger::new();
        let p = prepare(&store, &mut work, &run, &bound(EXEC, OP));
        let Prepared {
            planned,
            layout,
            attempt,
            objects,
        } = p;
        let prepared = work
            .scope(|w| begin_prepared_ledger(&layout.ledger, &attempt, objects, w))
            .unwrap();
        let other_run = format!("run3:{}", "0".repeat(64));
        let other = "f".repeat(64);
        let mut seal = sealed(&planned, 9);
        match case {
            0 => seal.run_id = &other_run,
            1 => seal.carrier = &other,
            _ => seal.operation = OP2,
        }
        let result = work.scope(|w| stage(prepared, &planned, &seal, w));
        assert!(matches!(
            result,
            Err(WorkFailure::Operation(
                ProjectLedgerRefusal::StagingMismatch
            ))
        ));
        assert_eq!(store.count("commit_receipts"), 0);
        assert_eq!(store.count("commit_associations"), 0);
    }
}

/// A deferred foreign-key violation in the connection's own temp schema makes
/// the real `COMMIT` statement fail inside the held transaction (X3c-2's).
fn break_commit(c: &rusqlite::Connection) {
    c.execute_batch(
        "CREATE TEMP TABLE parent(k INTEGER PRIMARY KEY);
         CREATE TEMP TABLE child(k INTEGER REFERENCES parent(k) DEFERRABLE INITIALLY DEFERRED);
         INSERT INTO child VALUES(1);",
    )
    .unwrap();
}

#[test]
fn an_error_from_the_evidence_commit_is_undetermined() {
    let run = replay();
    let store = Store::new();
    let mut work = WorkLedger::new();
    let p = prepare(&store, &mut work, &run, &bound(EXEC, OP));
    let (_, result) = staged(&mut work, p, 9);
    let mut staged = result.unwrap();
    staged.commit = staged.commit.with_commit_hook(break_commit);
    assert!(matches!(staged.commit(), EvidenceCommit::Undetermined));
    // Nothing is read back or retried: the attempt row stays admitted.
    assert_eq!(store.count("commit_receipts"), 0);
    let phase: String = store
        .ledger()
        .query_row("SELECT phase FROM attempt_custody", [], |r| r.get(0))
        .unwrap();
    assert_eq!(phase, "admitted");
}

// ------------------------------------------------------ the composition

/// Law X3d r8 item 13: the first real composition. A `CommitSession` opened
/// over X8b's `scenario-fixtures` operation (a first registration on a
/// synthetic installation), the synthetic candidate built for that session
/// and replayed by `replay_run` after `open` (the drawn ProjectId is only
/// known then; X9 r5's matrix order), then `prepare_commit` and `publish`
/// end to end: the evidence `COMMIT` returns success, the carrier holds one
/// `SEAL` and no `REV` or `CLN`, and the store holds exactly the receipt and
/// every retained frame and blob, the core evaluator closure's preimages
/// (the inventory body and the tree) included.
#[test]
fn the_first_real_commit_composes_prepare_commit_and_publish() {
    let home = ScenarioHome::create(&crate::test_scratch::temp_dir());
    let root = home.project("x3d3-commit");
    let session = CommitSession::open(home.operation(&root).unwrap()).unwrap();
    let candidate = synthetic_run_candidate(&session);
    assert_eq!(candidate.label(), run_candidate::SYNTHETIC_LABEL);
    let (namespace, store, execution, evaluator) = (
        session.namespace_id().to_owned(),
        session.store_instance().to_owned(),
        session.execution_id().to_owned(),
        session.core_evaluator_closure().to_owned(),
    );
    let run = opensip_evaluator::replay_run(
        &candidate.retained_inputs(),
        candidate.run_id(),
        synthetic_replay_limits(),
    )
    .unwrap();
    assert_eq!(run.evaluator_closure(), evaluator);
    let run_id = run.run_id().to_owned();
    let retained: BTreeSet<String> = run
        .retained_evidence()
        .object_frames()
        .values()
        .map(|frame| sha256_hex(frame))
        .chain(run.retained_evidence().blobs().keys().map(digest_hex))
        .collect();
    // The closure's preimages are retained: the inventory body and the tree.
    let V::Object(closure) = &candidate.objects()[&evaluator].descriptor else {
        panic!("closure")
    };
    assert!(retained.contains(string(&closure["manifestDigest"])));
    let V::Array(tree) = &closure["tree"] else {
        panic!("tree")
    };
    assert!(!tree.is_empty());
    for member in tree {
        let digest = string(&object(member)["sha256"]);
        assert!(retained.contains(digest), "{digest}");
        assert!(
            candidate
                .blobs()
                .contains_key(&<[u8; 32]>::try_from(bytes(digest)).unwrap())
        );
    }

    let prepared = match prepare_commit(run, session) {
        Ok(prepared) => prepared,
        Err((not, _)) => panic!("not prepared: {not:?}"),
    };
    let (outcome, stopped) = prepared.publish();
    let CommitOutcome::Committed(published) = outcome else {
        panic!("{outcome:?}")
    };
    assert_eq!(published.run_id(), run_id);
    assert_eq!(published.execution_id(), execution);
    assert_eq!(published.commit_sequence(), 1);
    assert!(!published.latched_after_admission());
    let end = stopped.finish();
    assert!(!end.revocation_appended());
    assert!(!end.cleanup_appended());
    assert!(end.settlement_failure().is_none());
    assert!(end.end_step_entered());

    // The carrier: the one SEAL, nothing owed.
    let census = home.carrier_census(&namespace).unwrap();
    assert_eq!((census.seal, census.rev, census.cln), (1, 0, 0));
    // The store: the exact receipt, once, and every retained frame and blob.
    let project = home
        .installation()
        .join("stores")
        .join(&store)
        .join("projects")
        .join(&namespace);
    let c = rusqlite::Connection::open_with_flags(
        project.join("ledger.sqlite"),
        rusqlite::OpenFlags::SQLITE_OPEN_READ_ONLY | rusqlite::OpenFlags::SQLITE_OPEN_NO_MUTEX,
    )
    .unwrap();
    let receipts: Vec<Vec<u8>> = c
        .prepare("SELECT body FROM commit_receipts")
        .unwrap()
        .query_map([], |r| r.get(0))
        .unwrap()
        .map(Result::unwrap)
        .collect();
    assert_eq!(receipts, vec![published.receipt().to_vec()]);
    let r = ReceiptCandidate::parse(&receipts[0]).unwrap();
    assert_eq!(
        (r.run.as_str(), r.execution.as_str(), r.namespace.as_str()),
        (run_id.as_str(), execution.as_str(), namespace.as_str())
    );
    let phase: String = c
        .query_row("SELECT phase FROM attempt_custody", [], |r| r.get(0))
        .unwrap();
    assert_eq!(phase, "admitted");
    let stored: BTreeSet<String> = fs::read_dir(project.join("objects/sha256"))
        .unwrap()
        .map(|e| e.unwrap().file_name().into_string().unwrap())
        .collect();
    assert_eq!(stored, retained);
}

// --------------------------------------------------------------- the reserve

#[test]
fn the_publication_reserve_is_exactly_what_admission_and_the_objects_charge() {
    let run = replay();
    let b = bound(EXEC, OP);
    let (planned, declared) = plan(&run, &b).unwrap();
    let reserve = attempt_and_objects_cost(&declared).unwrap();
    // On a fresh store the layout's cost, then exactly the reserve.
    let store = Store::new();
    let mut work = WorkLedger::new();
    let location = store.location();
    let layout = work.scope(|w| admit_layout(&location, w)).unwrap();
    let before = work.used();
    work.scope(|w| {
        admit_and_publish(
            &location,
            &layout,
            &attempt_record(&planned),
            declared,
            w,
            Box::new(|| {}),
        )
    })
    .unwrap();
    let used = work.used();
    assert_eq!(
        (
            used.objects - before.objects,
            used.edges - before.edges,
            used.bytes - before.bytes
        ),
        (reserve.objects, reserve.edges, reserve.bytes)
    );
    // One byte short: refused on the budget row before the attempt row.
    let store = Store::new();
    let mut probe = WorkLedger::new();
    let location = store.location();
    let measured = probe.scope(|w| admit_layout(&location, w)).unwrap();
    drop(measured);
    let layout_cost = probe.used();
    let store = Store::new();
    let mut short = WorkLedger::with_limits(WorkCost {
        objects: layout_cost.objects + reserve.objects,
        edges: layout_cost.edges + reserve.edges,
        bytes: layout_cost.bytes + reserve.bytes - 1,
    })
    .unwrap();
    let location = store.location();
    let layout = short.scope(|w| admit_layout(&location, w)).unwrap();
    let (planned, declared) = plan(&run, &b).unwrap();
    let refused = short.scope(|w| {
        admit_and_publish(
            &location,
            &layout,
            &attempt_record(&planned),
            declared,
            w,
            Box::new(|| {}),
        )
    });
    assert!(matches!(
        refused,
        Err(WorkFailure::Budget(WorkBudgetError::Bytes))
    ));
    assert_eq!(store.count("attempt_custody"), 0);
    assert!(store.objects().is_empty());
}

#[test]
fn a_reused_execution_id_is_refused_before_any_object() {
    let run = replay();
    let store = Store::new();
    let mut work = WorkLedger::new();
    let b = bound(EXEC, OP);
    let (planned, _) = plan(&run, &b).unwrap();
    let location = store.location();
    let layout = work.scope(|w| admit_layout(&location, w)).unwrap();
    // An earlier process's admitted row for this ExecutionId (F34).
    work.scope(|w| admit_attempt(&location, &layout.ledger, &attempt_record(&planned), w))
        .unwrap();
    let mut again = WorkLedger::new();
    let (planned, declared) = plan(&run, &b).unwrap();
    let refused = again.scope(|w| {
        admit_and_publish(
            &location,
            &layout,
            &attempt_record(&planned),
            declared,
            w,
            Box::new(|| {}),
        )
    });
    assert!(matches!(
        refused,
        Err(WorkFailure::Operation(
            ProjectLedgerRefusal::ReusedExecution
        ))
    ));
    assert_eq!(store.count("attempt_custody"), 1);
    assert!(store.objects().is_empty());
}

// --------------------------------------------------------------------- rows

#[test]
fn every_ledger_row_maps_to_its_existing_termination() {
    for (row, termination) in [
        (ProjectLedgerRow::Busy, T::Busy),
        (ProjectLedgerRow::LedgerCorrupt, T::LedgerCorrupt),
        (ProjectLedgerRow::HostIo, T::HostIo),
        (
            ProjectLedgerRow::DurabilityCommitFailed,
            T::CommitUndetermined,
        ),
        (ProjectLedgerRow::Invariant, T::Invariant),
        (
            ProjectLedgerRow::Custody("symlink"),
            T::Custody { subject: "symlink" },
        ),
    ] {
        assert_eq!(ledger_row(row), termination, "{row:?}");
    }
    assert_eq!(
        ledger_failure(&WorkFailure::Budget(WorkBudgetError::Closed)),
        T::BudgetExhausted
    );
}

/// Law X9 r1 item 5: `x3d.publish.published` is placed once, after the
/// `PublishedCommit` is built, which only the `Committed` arm does.
#[test]
fn the_published_point_follows_the_published_commit_once() {
    let source = include_str!("commit.rs");
    let point = r#"crash_barrier!("x3d.publish", "published", step)"#;
    assert_eq!(source.matches(point).count(), 1);
    let built = source.find("let published = PublishedCommit {").unwrap();
    assert!(source.find(point).unwrap() > built);
    // The one construction site.
    assert_eq!(source.matches("= PublishedCommit {").count(), 1);
}

// ------------------------------------------------- re-commit (X3c r8, X3c-3)

const EXEC3: &str = "exec1_00000000000000000000000000000003";
const OP3: &str = "op-00000000000000000000000000000003";
const N2: &str = "7c9e6679-7425-40de-944b-e07fc1f90ae7";

/// Every row of every table of a ledger, each as its columns' SQL `quote()`
/// text (a BLOB as its hex), by table: the raw dump X3c r8 item 12b compares.
fn dump(c: &rusqlite::Connection) -> BTreeMap<String, BTreeSet<String>> {
    let names = |sql: &str| -> Vec<String> {
        c.prepare(sql)
            .unwrap()
            .query_map([], |r| r.get(0))
            .unwrap()
            .map(Result::unwrap)
            .collect()
    };
    names("SELECT name FROM sqlite_schema WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name")
        .into_iter()
        .map(|table| {
            let select = names(&format!("SELECT name FROM pragma_table_info('{table}')"))
                .iter()
                .map(|column| format!("quote(\"{column}\")"))
                .collect::<Vec<_>>()
                .join("||'|'||");
            let rows = names(&format!("SELECT {select} FROM \"{table}\""));
            (table, rows.into_iter().collect())
        })
        .collect()
}
/// Every earlier row is in `after`, byte for byte.
fn kept(before: &BTreeMap<String, BTreeSet<String>>, after: &BTreeMap<String, BTreeSet<String>>) {
    for (table, rows) in before {
        assert!(
            rows.is_subset(&after[table]),
            "{table}: an earlier row changed"
        );
    }
}
/// `after` adds exactly the refused attempt's own `admitted` row to `before`:
/// staging inserted nothing.
fn only_the_attempt_row_added(
    before: &BTreeMap<String, BTreeSet<String>>,
    after: &BTreeMap<String, BTreeSet<String>>,
) {
    for (table, rows) in after {
        let added = rows.difference(&before[table]).count();
        let expected = usize::from(table == "attempt_custody");
        assert_eq!(added, expected, "{table}");
    }
    kept(before, after);
}
/// The facade's storage steps for `b` with a SEAL at `seq`, on a fresh
/// operation ledger: the staged adapter, not yet committed.
fn staged_at(store: &Store, run: &ReplayedRun, b: &Bound, seq: i64) -> (Planned, Refused<Staged>) {
    let mut work = WorkLedger::new();
    let p = prepare(store, &mut work, run, b);
    staged(&mut work, p, seq)
}
/// As `staged_at`, then the evidence `COMMIT`, which must succeed.
fn committed_at(store: &Store, run: &ReplayedRun, b: &Bound, seq: i64) -> Planned {
    let (planned, result) = staged_at(store, run, b, seq);
    assert!(matches!(
        result.unwrap().commit(),
        EvidenceCommit::Committed(_)
    ));
    planned
}
/// The fail-after hook: the transaction's own `COMMIT` lands inside the
/// hook, so the adapter's `COMMIT` errors and reports the undetermined
/// outcome over a commit that landed (X9's `fail-after`).
fn land_commit(c: &rusqlite::Connection) {
    c.execute_batch("COMMIT").unwrap();
}
/// This crate's test hook for a stored row no writer changes: `statement`
/// on N's ledger with `table`'s triggers lifted, then reinstalled from their
/// own stored SQL, which must be byte-identical afterwards (X9 item 6's
/// reserved-slot technique). Returns the rows changed.
fn lifted(store: &Store, table: &str, statement: &str) -> usize {
    let c = rusqlite::Connection::open(store.path.join("projects").join(N).join("ledger.sqlite"))
        .unwrap();
    let triggers = |c: &rusqlite::Connection| -> Vec<(String, String)> {
        c.prepare(
            "SELECT name,sql FROM sqlite_schema WHERE type='trigger' AND tbl_name=?1 ORDER BY name",
        )
        .unwrap()
        .query_map([table], |r| Ok((r.get(0)?, r.get(1)?)))
        .unwrap()
        .map(Result::unwrap)
        .collect()
    };
    let before = triggers(&c);
    assert!(!before.is_empty());
    for (name, _) in &before {
        c.execute_batch(&format!("DROP TRIGGER \"{name}\""))
            .unwrap();
    }
    let changed = c.execute(statement, []).unwrap();
    for (_, sql) in &before {
        c.execute_batch(sql).unwrap();
    }
    assert_eq!(triggers(&c), before, "reinstalled byte-identically");
    changed
}
/// The refused re-commit held no transaction: level 3 is free.
fn level_three_released(store: &Store) {
    rusqlite::Connection::open(store.path.join("projects").join(N).join("ledger.sqlite"))
        .unwrap()
        .execute_batch("BEGIN IMMEDIATE; ROLLBACK")
        .unwrap();
}

/// Law X3c r8 items 6a and 12b (unit X3c-3): the same candidate committed
/// twice through the facade, each by its own real session over X8b's
/// `scenario-fixtures` operation on one project root, ends `Committed` both
/// times. The second confirms every object, takes the next sequence and adds
/// exactly item 6a.6's rows: its own attempt row, receipt, association and
/// Run material (byte-identical to the first's), one more `SEAL`, and no
/// availability record or pin change. A raw dump of every earlier row is
/// byte-identical before and after.
#[test]
fn the_same_candidate_committed_twice_is_committed_both_times() {
    let home = ScenarioHome::create(&crate::test_scratch::temp_dir());
    let root = home.project("x3c3-recommit");
    let commit = || {
        let session = CommitSession::open(home.operation(&root).unwrap()).unwrap();
        let candidate = synthetic_run_candidate(&session);
        let (namespace, store) = (
            session.namespace_id().to_owned(),
            session.store_instance().to_owned(),
        );
        let run = opensip_evaluator::replay_run(
            &candidate.retained_inputs(),
            candidate.run_id(),
            synthetic_replay_limits(),
        )
        .unwrap();
        let prepared = match prepare_commit(run, session) {
            Ok(prepared) => prepared,
            Err((not, _)) => panic!("not prepared: {not:?}"),
        };
        let dispositions: BTreeSet<String> = prepared
            .objects
            .objects()
            .iter()
            .map(|o| format!("{:?}", o.disposition()))
            .collect();
        let (outcome, stopped) = prepared.publish();
        let CommitOutcome::Committed(published) = outcome else {
            panic!("{outcome:?}")
        };
        let end = stopped.finish();
        assert!(!end.revocation_appended() && !end.cleanup_appended());
        assert!(end.settlement_failure().is_none() && end.end_step_entered());
        (published, dispositions, namespace, store)
    };
    let (first, dispositions, namespace, store) = commit();
    assert_eq!(dispositions, BTreeSet::from(["PublishedNew".to_owned()]));
    let ledger = || {
        rusqlite::Connection::open_with_flags(
            home.installation()
                .join("stores")
                .join(&store)
                .join("projects")
                .join(&namespace)
                .join("ledger.sqlite"),
            rusqlite::OpenFlags::SQLITE_OPEN_READ_ONLY | rusqlite::OpenFlags::SQLITE_OPEN_NO_MUTEX,
        )
        .unwrap()
    };
    let before = dump(&ledger());
    let (second, dispositions, again, _) = commit();
    assert_eq!(again, namespace);
    assert_eq!(
        dispositions,
        BTreeSet::from(["ConfirmedExisting".to_owned()])
    );
    assert_eq!(second.run_id(), first.run_id());
    assert_ne!(second.execution_id(), first.execution_id());
    assert_eq!((first.commit_sequence(), second.commit_sequence()), (1, 2));
    assert!(!second.latched_after_admission());
    let after = dump(&ledger());
    kept(&before, &after);
    for (table, added) in [
        ("attempt_custody", 1),
        ("commit_receipts", 1),
        ("commit_associations", 1),
        ("commit_run_material", 1),
        ("evidence_availability", 0),
        ("active_run_pins", 0),
        ("pin_change_facts", 0),
    ] {
        assert_eq!(after[table].len() - before[table].len(), added, "{table}");
    }
    assert_eq!(after["evidence_availability"].len(), 1);
    assert_eq!(after["active_run_pins"].len(), 0);
    let c = ledger();
    let material: Vec<(Vec<u8>, Vec<u8>)> = c
        .prepare("SELECT manifest,inventory FROM commit_run_material")
        .unwrap()
        .query_map([], |r| Ok((r.get(0)?, r.get(1)?)))
        .unwrap()
        .map(Result::unwrap)
        .collect();
    assert_eq!(material.len(), 2);
    assert_eq!(material[0], material[1]);
    let receipt = ReceiptCandidate::parse(second.receipt()).unwrap();
    assert_eq!(
        (
            receipt.run.as_str(),
            receipt.execution.as_str(),
            receipt.sequence
        ),
        (first.run_id(), second.execution_id(), 2)
    );
    // Two SEALs, nothing owed.
    let census = home.carrier_census(&namespace).unwrap();
    assert_eq!((census.seal, census.rev, census.cln), (2, 0, 0));
}

/// Law X3c r8 items 6a.2 and 12b (unit X3c-3): standing is read from the
/// Run's committed per-Run rows only. (a) An earlier attempt that died after
/// its SEAL and before its `COMMIT` (staged, then dropped) leaves no per-Run
/// row, so the next commit is a first commit: it writes availability
/// generation 0. (b) An earlier `COMMIT` that landed and was reported
/// undetermined (the fail-after hook) makes the next commit a re-commit.
#[test]
fn standing_is_read_from_committed_per_run_rows_only() {
    let run = replay();
    // (a)
    let store = Store::new();
    let (_, died) = staged_at(&store, &run, &bound(EXEC, OP), 9);
    drop(died.unwrap());
    assert_eq!(store.count("attempt_custody"), 1);
    assert_eq!(store.count("evidence_availability"), 0);
    let (_, next) = staged_at(&store, &run, &bound(EXEC2, OP2), 10);
    let next = next.unwrap();
    assert_eq!(next.sequence, 1);
    assert!(matches!(next.commit(), EvidenceCommit::Committed(_)));
    let generation: String = store
        .ledger()
        .query_row("SELECT generation FROM evidence_availability", [], |r| {
            r.get(0)
        })
        .unwrap();
    assert_eq!(generation, "0");
    assert_eq!(store.count("commit_run_material"), 1);
    // (b)
    let store = Store::new();
    let (_, landed) = staged_at(&store, &run, &bound(EXEC, OP), 9);
    let mut landed = landed.unwrap();
    landed.commit = landed.commit.with_commit_hook(land_commit);
    assert!(matches!(landed.commit(), EvidenceCommit::Undetermined));
    assert_eq!(store.count("commit_receipts"), 1, "the COMMIT landed");
    let before = dump(&store.ledger());
    let (_, next) = staged_at(&store, &run, &bound(EXEC2, OP2), 10);
    let next = next.unwrap();
    assert_eq!(next.sequence, 2);
    assert!(matches!(next.commit(), EvidenceCommit::Committed(_)));
    let after = dump(&store.ledger());
    kept(&before, &after);
    assert_eq!(store.count("evidence_availability"), 1);
    assert_eq!(store.count("commit_run_material"), 2);
    assert_eq!(store.count("commit_receipts"), 2);
}

/// Law X3c r8 items 6a.3 and 12b (unit X3c-3): the regeneration mismatch.
/// R's stored inventory is changed through this crate's lifted-trigger hook,
/// once at the same length (a digest's last digit) and once longer (so the
/// lengths differ and the stored body is never read). The re-commit refuses
/// on the invariant row, inserts nothing and holds no transaction.
#[test]
fn a_regeneration_mismatch_is_refused_on_the_invariant_row() {
    let run = replay();
    type Edit = fn(&[u8]) -> Vec<u8>;
    let edits: [(&str, Edit); 2] = [
        ("same length", |inventory| {
            let text = std::str::from_utf8(inventory).unwrap();
            let at = text.find("\"blobDigests\":[\"").unwrap() + "\"blobDigests\":[\"".len() + 63;
            let mut bytes = inventory.to_vec();
            bytes[at] = if bytes[at] == b'0' { b'1' } else { b'0' };
            bytes
        }),
        ("longer", |inventory| [inventory, b" "].concat()),
    ];
    for (label, edit) in edits {
        let store = Store::new();
        committed_at(&store, &run, &bound(EXEC, OP), 9);
        let inventory: Vec<u8> = store
            .ledger()
            .query_row("SELECT inventory FROM commit_run_material", [], |r| {
                r.get(0)
            })
            .unwrap();
        let changed = edit(&inventory);
        assert_ne!(changed, inventory);
        let hex: String = changed.iter().map(|b| format!("{b:02x}")).collect();
        assert_eq!(
            lifted(
                &store,
                "commit_run_material",
                &format!("UPDATE commit_run_material SET inventory=X'{hex}'")
            ),
            1
        );
        let before = dump(&store.ledger());
        let (_, refused) = staged_at(&store, &run, &bound(EXEC2, OP2), 10);
        assert!(
            matches!(
                refused,
                Err(WorkFailure::Operation(
                    ProjectLedgerRefusal::StagingMismatch
                ))
            ),
            "{label}"
        );
        only_the_attempt_row_added(&before, &dump(&store.ledger()));
        level_three_released(&store);
    }
}

/// Law X3c r8 items 6a.2, 10 and 12b (unit X3c-3): a one-sided Run is
/// `LEDGER.CORRUPT`, inserting nothing: R's availability record without any
/// Run material of R, and R's material without its availability record (each
/// row removed through this crate's lifted-trigger hook).
#[test]
fn a_one_sided_run_is_ledger_corrupt() {
    let run = replay();
    for (label, table) in [
        ("availability without material", "commit_run_material"),
        ("material without availability", "evidence_availability"),
    ] {
        let store = Store::new();
        committed_at(&store, &run, &bound(EXEC, OP), 9);
        assert_eq!(lifted(&store, table, &format!("DELETE FROM {table}")), 1);
        let before = dump(&store.ledger());
        let (_, refused) = staged_at(&store, &run, &bound(EXEC2, OP2), 10);
        let Err(WorkFailure::Operation(refusal)) = refused else {
            panic!("{label}: not refused")
        };
        assert_eq!(refusal.row(), ProjectLedgerRow::LedgerCorrupt, "{label}");
        assert_eq!(ledger_row(refusal.row()), T::LedgerCorrupt);
        only_the_attempt_row_added(&before, &dump(&store.ledger()));
        level_three_released(&store);
    }
}

/// Law X3c r8 items 6a.4 and 12b (unit X3c-3): a non-retained record. After
/// R's first commit a test writes a generation-1 `purged` successor; the
/// re-commit commits, adds no availability row, and the record is unchanged
/// and still current.
#[test]
fn a_non_retained_record_stays_current_through_a_re_commit() {
    let run = replay();
    let store = Store::new();
    let planned = committed_at(&store, &run, &bound(EXEC, OP), 9);
    let (digest, body): (String, Vec<u8>) = store
        .ledger()
        .query_row(
            "SELECT store_digest,body FROM evidence_availability",
            [],
            |r| Ok((r.get(0)?, r.get(1)?)),
        )
        .unwrap();
    let purged = String::from_utf8(body)
        .unwrap()
        .replace("\"generation\":0", "\"generation\":1")
        .replace("\"state\":\"retained\"", "\"state\":\"purged\"");
    let schemas = crate::schema_sources::registry().unwrap();
    let record = AvailabilityRecord::parse(schemas, purged.as_bytes(), 1 << 20).unwrap();
    assert_eq!(record.generation(), 1);
    rusqlite::Connection::open(store.path.join("projects").join(N).join("ledger.sqlite"))
        .unwrap()
        .execute(
            "INSERT INTO evidence_availability VALUES(?1,?2,?3,'1',?4)",
            rusqlite::params![digest, N, planned.run_id, purged.as_bytes()],
        )
        .unwrap();
    let before = dump(&store.ledger());
    let (_, next) = staged_at(&store, &run, &bound(EXEC2, OP2), 10);
    let next = next.unwrap();
    assert_eq!(next.sequence, 2);
    assert!(matches!(next.commit(), EvidenceCommit::Committed(_)));
    let after = dump(&store.ledger());
    kept(&before, &after);
    assert_eq!(
        after["evidence_availability"],
        before["evidence_availability"]
    );
    let current: Vec<u8> = store
        .ledger()
        .query_row(
            "SELECT body FROM evidence_availability ORDER BY length(generation) DESC,generation DESC LIMIT 1",
            [],
            |r| r.get(0),
        )
        .unwrap();
    assert_eq!(current, purged.into_bytes());
    assert_eq!(store.count("commit_run_material"), 2);
}

/// Law X3c r8 items 6a.2 and 12b (unit X3c-3): "the same store and
/// namespace" is the per-Run rows' key. A commit of R in another namespace
/// of the same store is a first commit there (availability generation 0,
/// sequence 1), and N's ledger is untouched.
#[test]
fn a_commit_of_the_run_in_another_namespace_is_a_first_commit_there() {
    let run = replay();
    let store = Store::new();
    committed_at(&store, &run, &bound(EXEC, OP), 9);
    let before = dump(&store.ledger());
    let mut other = bound(EXEC2, OP2);
    other.namespace = N2.into();
    other.carrier = sha256_hex(N2.as_bytes());
    let (planned, staged) = staged_at(&store, &run, &other, 1);
    assert_eq!(planned.run_id, run.run_id());
    let staged = staged.unwrap();
    assert_eq!(staged.sequence, 1);
    assert!(matches!(staged.commit(), EvidenceCommit::Committed(_)));
    assert_eq!(dump(&store.ledger()), before);
    for table in [
        "commit_receipts",
        "commit_run_material",
        "evidence_availability",
    ] {
        assert_eq!(store.count_in(N2, table), 1, "{table}");
    }
    let generation: String = store
        .ledger_in(N2)
        .query_row("SELECT generation FROM evidence_availability", [], |r| {
            r.get(0)
        })
        .unwrap();
    assert_eq!(generation, "0");
}

// Law X6 r3 (unit X6b): `recover_from` over the stores these steps commit.
#[path = "recover_tests.rs"]
mod recover;

// Law X6 r3 item 7 (unit X6c): the settlement sweep over the stores these
// steps commit, read back by `recover_from`.
#[path = "sweep_tests.rs"]
mod settlement_sweep;

// J-C15/J-C15b: the real prepare result retains the window until publish.
#[test]
fn a_prepared_commit_keeps_the_window_and_publish_closes_it() {
    for cancel_before_publish in [true, false] {
        let home = ScenarioHome::create(&crate::test_scratch::temp_dir());
        let root = home.project("j3b-prepared-window");
        let mut session = CommitSession::open(home.operation(&root).unwrap()).unwrap();
        let namespace = session.namespace_id().to_owned();
        let token = session.take_cancellation_latch().unwrap();
        assert!(session.take_cancellation_latch().is_none());
        let candidate = synthetic_run_candidate(&session);
        let run = opensip_evaluator::replay_run(
            &candidate.retained_inputs(),
            candidate.run_id(),
            synthetic_replay_limits(),
        )
        .unwrap();
        let prepared = match prepare_commit(run, session) {
            Ok(p) => p,
            Err((not, _)) => panic!("not prepared: {not:?}"),
        };
        let token = if cancel_before_publish {
            assert_eq!(
                token.latch(opensip_security::D9Signal::Sigint),
                opensip_security::LatchOutcome::BeforeAdmission
            );
            None
        } else {
            Some(token)
        };
        let (outcome, stopped) = prepared.publish();
        assert_eq!(stopped.admitted_at_close(), !cancel_before_publish);
        if cancel_before_publish {
            assert!(matches!(
                outcome,
                CommitOutcome::Refused(T::Interrupted {
                    signal: opensip_security::D9Signal::Sigint
                })
            ));
        } else {
            assert!(matches!(outcome, CommitOutcome::Committed(_)));
            assert_eq!(
                token.unwrap().latch(opensip_security::D9Signal::Sigterm),
                opensip_security::LatchOutcome::OutsideWindow
            );
        }
        let end = stopped.finish();
        assert_eq!(end.revocation_appended(), cancel_before_publish);
        let census = home.carrier_census(&namespace).unwrap();
        assert_eq!(
            (census.seal, census.rev, census.cln),
            if cancel_before_publish {
                (0, 1, 0)
            } else {
                (1, 0, 0)
            }
        );
        let next = home.operation(&root).unwrap();
        drop(next);
    }
}
