//! Law X9 r11 (unit X9-5): the crash matrix's host rows, run through host's
//! own commit coordinator and `store-gc` step in fresh processes. This
//! target exists only with `--features crash-matrix` (`required-features`,
//! law X9 r1 item 2); a plain `cargo test` skips it.
//!
//! Every process of a run is a matrix child: this test binary re-executed
//! by X9-0's driver (`matrix_child`), under X9 r2 item 3's scripted wall
//! clock, numbered in spawn order. The children:
//! - `fixture` (ordinal 0): a synthetic installation by the real creator
//!   path, X4T-0's accepted store and a project root (item 6);
//! - `candidate` (X9 r10's host order): its one entry is `operation`; it
//!   opens a `CommitSession`, writes X3d-3's run candidate to a file under
//!   the run's scratch root, and ends the session refused before
//!   `prepare_commit`;
//! - `finalize`: host's `finalize_commit` runner over that file, so host's
//!   own `finalize` replays before any custody (X5 r3 item 3), then admits
//!   through `operation`, commits, finishes and delivers;
//! - `store-gc`: host's `store_gc` runner (X6c's step through
//!   `maintenance::run`);
//! - `recover`: X9 r4 item 6's read entry, then `recover` (X6, read-only);
//! - `publisher`: the shared fenced revocation publisher, in a process that
//!   holds no operation (item 11).
//!
//! The parent transcribes nothing: every expected value comes from the
//! reviewed host `required-runs.v1.json` (X9 r10), written before any run.
//! It runs each row's script step by step, arms, awaits, resumes and kills
//! by blocking record reads, captures the post state between processes,
//! runs item 8's ladder, and writes one run record per run and the run
//! set's `matrix.json`. Nothing here sleeps, polls or waits on a timer;
//! X9-0's watchdog is the one timed wait, and it can only make a run a
//! `HARNESS-ERROR`.
#![cfg(all(feature = "crash-matrix", target_os = "macos"))]

use opensip_host::crash_matrix_support as support;
use opensip_identity::{JsonValue as V, canonical_bytes, digest_hex, parse_json, raw_sha256};
use opensip_platform::crash_barrier::driver::{
    Census, CensusPoint, ChildSpec, Exit, MatrixChild, Record, ScriptedClock,
};
use opensip_platform::crash_barrier::{child_role, report_outcome};
use opensip_security::{CommitSession, RecoveryRequest, SessionEnd};
use opensip_storage::{NamespaceSweep, RecoveredCommit, recover};
use std::collections::BTreeMap;
use std::fs;
use std::os::unix::fs::PermissionsExt;
use std::os::unix::process::ExitStatusExt;
use std::path::{Path, PathBuf};
use std::sync::Mutex;
use support::post_state::{PostState, capture, normalize, normalized_sha256};
use support::run_record::{
    ChildExit, ChildRecord, FilePin, Host, Product, RunRecord, TIMING_GUARD_LIMIT_MS, Verdict,
    census_json, trace_digest, write_run,
};
use support::{FinalizeOutcome, FinalizeReport, GcReport, RolloverReport};

/// The child entry `--exact` names.
const ENTRY: &str = "matrix_child";
/// The reviewed host required runs (law X9 r10: X9-5's rows only).
const REQUIRED: &str = "tests/fixtures/crash-matrix/required-runs.v1.json";
/// X9 r4 item 7: the cases item 12 gives X9-5.
const UNIT_CASES: &[&str] = &["F01", "F12", "F16", "F17", "F32", "F39", "F40", "F53"];
/// Rows whose scripted phase leaves no attempt to item 8's ladder: F01
/// ends before `prepare_commit` writes anything, and F53's scripted phase
/// is itself the sweeps that settle what it left.
const NO_LADDER: &[&str] = &["F01", "F53"];
/// Item 11's timing guard reads the parent's monotonic clock (X9 r12).
type GuardClock = std::time::Instant;
/// One run at a time.
static SERIAL: Mutex<()> = Mutex::new(());

/// The run candidate's registry. The included candidate source (below)
/// names storage's `crate::schema_sources::registry()`; host's
/// `embedded_schema_registry` compiles the same pinned sources (X8c's
/// `the_candidate_registry_is_storages_selected_registry`).
mod schema_sources {
    use opensip_identity::RegisteredSchemas;
    use std::sync::OnceLock;
    pub(crate) fn registry() -> Option<&'static RegisteredSchemas> {
        static REGISTRY: OnceLock<Option<RegisteredSchemas>> = OnceLock::new();
        REGISTRY
            .get_or_init(|| opensip_host::embedded_schema_registry().ok())
            .as_ref()
    }
}

// X3d-3's run candidate source, included by path as X8c includes it, for
// F01's substituted variants only: the parent writes them from the lawful
// candidate file before the `finalize` child starts (X9 r10). Inputs only;
// never a `ReplayedRun`.
#[allow(dead_code)]
#[path = "../../storage/src/crash_matrix_support/run_candidate.rs"]
mod run_candidate;

// =================================================================== child

/// The matrix child entry. In the parent's own run it returns at once.
#[test]
fn matrix_child() {
    let Some((role, input)) = child_role() else {
        return;
    };
    let input = Input::read(&input);
    let outcome = match role.as_str() {
        "fixture" => fixture(&input),
        "candidate" => candidate(&input),
        "finalize" => finalize(&input),
        "store-gc" => store_gc(&input),
        "recover" => recovery(&input),
        "publisher" => publisher(&input),
        "entries" => entries(&input),
        other => panic!("unknown matrix child role {other}"),
    };
    report_outcome(&outcome);
    println!("\nX9-OUTCOME {outcome}");
}

/// A child's input: `key=value` lines.
struct Input(BTreeMap<String, String>);
impl Input {
    fn read(path: &Path) -> Self {
        let text = fs::read_to_string(path).expect("child input");
        Self(
            text.lines()
                .filter_map(|l| l.split_once('='))
                .map(|(k, v)| (k.to_owned(), v.to_owned()))
                .collect(),
        )
    }
    fn get(&self, key: &str) -> &str {
        self.0
            .get(key)
            .unwrap_or_else(|| panic!("input {key}"))
            .as_str()
    }
    fn installation(&self) -> support::SyntheticInstallation {
        support::SyntheticInstallation::open(
            Path::new(self.get("home")),
            Path::new(self.get("installation")),
            self.get("store"),
        )
    }
}

/// `fixture` (ordinal 0): the synthetic installation under this process's
/// `TMPDIR`, X4T-0's accepted store at revocation version 1, and a project
/// root `H/code/project` (0755). Its paths and the core closure its P0
/// names go to `out`; the tree outlives this process.
fn fixture(input: &Input) -> String {
    let installation = support::SyntheticInstallation::create("x95");
    let closure = installation
        .install_accepted_trust(Vec::new(), 1)
        .expect("accepted store");
    let code = installation.home().join("code");
    let project = code.join("project");
    for dir in [&code, &project] {
        fs::create_dir(dir).expect("project root");
        fs::set_permissions(dir, fs::Permissions::from_mode(0o755)).expect("mode");
    }
    fs::write(
        input.get("out"),
        format!(
            "home={}\ninstallation={}\nstore={}\nproject={}\nclosure={closure}\n",
            installation.home().display(),
            installation.installation().display(),
            installation.store(),
            project.display()
        ),
    )
    .expect("fixture out");
    std::mem::forget(installation);
    "fixture".into()
}

fn end_text(end: &SessionEnd) -> String {
    format!(
        "end(rev={},cln={},settlement={:?},step={},stepFailure={:?})",
        end.revocation_appended(),
        end.cleanup_appended(),
        end.settlement_failure(),
        end.end_step_entered(),
        end.end_step_failure()
    )
}

/// `candidate` (X9 r10): the one entry `operation`, `CommitSession::open`,
/// X3d-3's candidate from that session written to `out` (and the session's
/// ProjectId beside it), then the session ended refused before
/// `prepare_commit`.
fn candidate(input: &Input) -> String {
    let installation = input.installation();
    let operation = match support::operation(&installation, Path::new(input.get("project"))) {
        Ok(operation) => operation,
        Err(row) => return format!("operation:{row:?}"),
    };
    let session = match CommitSession::open(operation) {
        Ok(session) => session,
        Err((refusal, stopped)) => {
            return format!(
                "open:{:?};{}",
                refusal.termination(),
                end_text(&stopped.finish())
            );
        }
    };
    let out = Path::new(input.get("out"));
    let candidate = support::synthetic_run_candidate(&session);
    support::write_run_candidate(
        out,
        candidate.run_id(),
        candidate.objects(),
        candidate.blobs(),
    )
    .expect("candidate file");
    fs::write(out.with_extension("project"), session.project_id()).expect("project id");
    // X9 r12 and r13: r12's distinct variant, for an R2 after a committed
    // Run, and the session's own core closure, the revoked subject.
    let distinct = support::synthetic_run_candidate_distinct(&session);
    support::write_run_candidate(
        &out.with_extension("distinct.json"),
        distinct.run_id(),
        distinct.objects(),
        distinct.blobs(),
    )
    .expect("distinct candidate file");
    fs::write(out.with_extension("closure"), session.core_closure()).expect("core closure");
    let end = session.reserve_end_path().map_or_else(
        |(_, stopped)| stopped.finish(),
        |session| session.refused().finish(),
    );
    format!("candidate;{}", end_text(&end))
}

/// The one registered namespace's id, if exactly one.
fn only_namespace(installation: &Path) -> Option<String> {
    let mut names: Vec<String> = fs::read_dir(installation.join("host/projects"))
        .ok()?
        .filter_map(|e| e.ok())
        .filter(|e| e.path().is_dir())
        .map(|e| e.file_name().into_string().unwrap())
        .collect();
    (names.len() == 1).then(|| names.pop().unwrap())
}

/// A row as `<errorCode>/<detail>`, public spellings.
fn row_text(row: &opensip_host::InstallationTerminationV1) -> String {
    format!(
        "{}/{}",
        row.error_code,
        row.detail.map_or("-".to_owned(), |d| d.to_string())
    )
}

/// A remedy by the route it names (the texts are finalization's and fact
/// admission's own constants).
fn remedy_text(remedy: Option<&str>) -> String {
    let Some(text) = remedy else {
        return "-".into();
    };
    for (prefix, name) in [
        (
            "the Run is committed; rerun the renderer",
            "renderer-failed-after-commit",
        ),
        (
            "The commit's outcome is undetermined.",
            "commit-undetermined",
        ),
        (
            "An attempt with this executionId already exists.",
            "existing-attempt",
        ),
        (
            "Restore the exact retained closure bytes",
            "evidence-missing",
        ),
        ("Retain the sealed Run", "regeneration-mismatch"),
        ("Correct the provider output", "input-refused"),
    ] {
        if text.starts_with(prefix) {
            return name.into();
        }
    }
    "other".into()
}

/// `finalize`: host's `finalize_commit` over the candidate file. The
/// report, as `key=value` fields; a subject is named by what it is.
fn finalize(input: &Input) -> String {
    let installation = input.installation();
    let candidate = Path::new(input.get("candidate"));
    let run_id = support::read_run_candidate(candidate)
        .map(|c| c.run_id)
        .unwrap_or_default();
    let report =
        support::finalize_commit(&installation, Path::new(input.get("project")), candidate);
    let namespace = only_namespace(installation.installation());
    finalize_text(&report, &run_id, namespace.as_deref())
}

fn finalize_text(report: &FinalizeReport, run_id: &str, namespace: Option<&str>) -> String {
    let subject = |s: &Option<String>| match s {
        None => "-".to_owned(),
        Some(s) if s.starts_with("exec1_") => "executionId".into(),
        Some(s) if s == run_id => "runId".into(),
        Some(s) if Some(s.as_str()) == namespace => "namespace".into(),
        Some(s) => s.clone(),
    };
    let head = match &report.outcome {
        FinalizeOutcome::Authoritative { run_id: r, exit } => format!(
            "kind=authoritative;exit={exit};runId={}",
            if r == run_id { "claimed" } else { "other" }
        ),
        FinalizeOutcome::Interrupted { signal, run_id: retained } => format!(
            "kind=interrupted;exit=130;signal={};runId={}", signal.as_str(),
            match retained { Some(id) if id == run_id => "claimed", Some(_) => "other", None => "no" }
        ),
        FinalizeOutcome::Terminated {
            row,
            run_id: retained,
            remedy,
            namespace: disclosed,
            requested_binding,
        } => format!(
            "kind=terminated;row={};exit={};subject={};runId={};remedy={};namespace={};requested={}",
            row_text(row),
            row.exit,
            subject(&row.subject),
            if retained.is_some() { "yes" } else { "no" },
            remedy_text(*remedy),
            if disclosed.is_some() { "yes" } else { "no" },
            if *requested_binding { "yes" } else { "no" }
        ),
    };
    let rollover = match &report.rollover {
        None => "-".to_owned(),
        Some(RolloverReport::Rolled { opened_generation }) => format!("rolled:{opened_generation}"),
        Some(RolloverReport::AlreadyRolled) => "already-rolled".into(),
        Some(RolloverReport::Skipped) => "skipped".into(),
        Some(RolloverReport::Refused(row)) => format!("refused:{}", row_text(row)),
        Some(RolloverReport::Undetermined(row)) => format!("undetermined:{}", row_text(row)),
    };
    format!(
        "{head};delivered={};optional={};end={};endStep={};rollover={rollover};arrivalPhases={}",
        report.delivered.len(),
        if report.optional_failed {
            "failed"
        } else {
            "ok"
        },
        report.end_failure.as_ref().map_or("-".into(), row_text),
        report
            .end_step_failure
            .as_ref()
            .map_or("-".into(), row_text),
        if report.arrival_phases.is_empty() { "-".to_owned() } else { report.arrival_phases.join(",") },
    )
}

/// `store-gc`: host's `store_gc`. Per namespace, its sweep (settled pairs
/// ordered by outcome, so repetitions report alike) and row, then the
/// ending row.
fn store_gc(input: &Input) -> String {
    let installation = input.installation();
    gc_text(&support::store_gc(&installation))
}

fn gc_text(report: &GcReport) -> String {
    let mut out = Vec::new();
    for n in &report.namespaces {
        let swept = match &n.swept {
            None => "skipped".to_owned(),
            Some(NamespaceSweep::Swept {
                settled,
                left,
                more,
                stopped,
            }) => {
                let mut settled: Vec<(&str, String)> = settled
                    .iter()
                    .map(|(e, o)| (o.spelling(), format!("{e}={}", o.spelling())))
                    .collect();
                settled.sort_by_key(|(o, _)| *o);
                let mut left: Vec<(&str, String)> = left
                    .iter()
                    .map(|l| (l.reason(), format!("{}={}", l.execution_id(), l.reason())))
                    .collect();
                left.sort_by_key(|(r, _)| *r);
                format!(
                    "swept[settled={};left={};more={more};stopped={}]",
                    settled
                        .into_iter()
                        .map(|(_, s)| s)
                        .collect::<Vec<_>>()
                        .join(","),
                    left.into_iter()
                        .map(|(_, s)| s)
                        .collect::<Vec<_>>()
                        .join(","),
                    stopped
                        .as_ref()
                        .map_or("-".to_owned(), |(_, stop)| format!("{stop:?}"))
                )
            }
            Some(other) => format!("{other:?}"),
        };
        out.push(format!(
            "{swept}:row={}",
            n.row.as_ref().map_or("-".into(), row_text)
        ));
    }
    format!(
        "{};ended={}",
        out.join("|"),
        report.ended.as_ref().map_or("-".into(), row_text)
    )
}

/// An observed standing: the owner's spelling, then its typed member.
fn standing_text(recovered: &RecoveredCommit) -> String {
    let standing = recovered.standing();
    match recovered {
        RecoveredCommit::CommittedHistorically {
            pending_settlement,
            diagnosis,
            ..
        }
        | RecoveredCommit::CommittedAvailabilityDegraded {
            pending_settlement,
            diagnosis,
            ..
        } => format!(
            "{standing}{}{}",
            if *pending_settlement {
                ":pendingSettlement"
            } else {
                ""
            },
            diagnosis.map_or(String::new(), |d| format!(":{d}"))
        ),
        RecoveredCommit::UnknownCustody { reason, .. } => format!("{standing}:{reason}"),
        RecoveredCommit::UnknownQuarantineCondition { reason, .. } => {
            format!("{standing}:{reason}")
        }
        RecoveredCommit::BindingUnusable { subject, .. } => format!("{standing}:{subject}"),
        _ => standing.to_owned(),
    }
}

/// `recover`: X9 r4 item 6's read entry, then `recover`.
fn recovery(input: &Input) -> String {
    let installation = input.installation();
    let request = RecoveryRequest::plain(input.get("execution"), input.get("namespace"))
        .expect("request shape");
    match support::recovery_admission(&installation, request) {
        Err(refusal) => format!("admission:{refusal:?}"),
        Ok(admission) => match recover(admission) {
            Ok(recovered) => standing_text(&recovered),
            Err(failure) => format!("failure:{failure:?}"),
        },
    }
}

/// `publisher`: the shared fenced publisher revokes the core closure P0
/// names (item 11), at revocation version 2, in a process that made no
/// entry and holds no operation. The subject is the `candidate` session's
/// own core closure (X9 r12 and r13), read from the file that child wrote.
fn publisher(input: &Input) -> String {
    let installation = input.installation();
    let closure = fs::read_to_string(input.get("core-closure")).expect("core closure");
    match installation.publish_revocation(vec![("release", closure)], 2) {
        Ok(versions) => format!("published:{}->{}", versions.before, versions.after),
        Err(error) => format!("refused:{error}"),
    }
}

/// `entries`: X9 r10's one entry per process for the runners. A first
/// `finalize_commit` over a missing candidate file ends before any entry,
/// on the host I/O row; a second runner call of either kind then refuses on
/// the invariant row without effect.
fn entries(input: &Input) -> String {
    let installation = input.installation();
    let project = Path::new(input.get("project"));
    let missing = Path::new(input.get("missing"));
    let first = support::finalize_commit(&installation, project, missing);
    let again = support::finalize_commit(&installation, project, missing);
    let gc = support::store_gc(&installation);
    format!(
        "first={};again={};gc={}",
        finalize_text(&first, "", None),
        finalize_text(&again, "", None),
        gc_text(&gc)
    )
}

// ================================================================== parent

/// The paths the fixture child published.
#[derive(Clone)]
struct Paths {
    home: PathBuf,
    installation: PathBuf,
    store: String,
    project: PathBuf,
    closure: String,
}
impl Paths {
    fn lines(&self) -> String {
        format!(
            "home={}\ninstallation={}\nstore={}\nproject={}\nclosure={}\n",
            self.home.display(),
            self.installation.display(),
            self.store,
            self.project.display(),
            self.closure
        )
    }
    /// N and its directory under I, when exactly one namespace is
    /// registered.
    fn namespace(&self) -> Option<(String, PathBuf)> {
        let n = only_namespace(&self.installation)?;
        let dir = self.installation.join("host/projects").join(&n);
        Some((n, dir))
    }
    /// N's ledger directory under `I/stores/S`.
    fn ledger_dir(&self, namespace: &str) -> PathBuf {
        self.installation
            .join("stores")
            .join(&self.store)
            .join("projects")
            .join(namespace)
    }
}

/// A harness failure: the run is a `HARNESS-ERROR`, never a pass.
#[derive(Debug)]
struct Harness(String);
fn harness<E: std::fmt::Debug>(what: &str) -> impl FnOnce(E) -> Harness + '_ {
    move |e| Harness(format!("{what}: {e:?}"))
}

/// One run's processes, under its own private scratch parent.
struct Run {
    scratch: PathBuf,
    next: u32,
    epoch: i64,
    children: Vec<ChildRecord>,
    paths: Option<Paths>,
}
impl Run {
    fn new(epoch: i64) -> Self {
        let nonce: String = opensip_platform::request_entropy()
            .unwrap()
            .iter()
            .map(|b| format!("{b:02x}"))
            .collect();
        let scratch = std::env::temp_dir().join(format!("opensip-x95-{nonce}"));
        fs::create_dir(&scratch).unwrap();
        fs::set_permissions(&scratch, fs::Permissions::from_mode(0o700)).unwrap();
        Self {
            scratch: fs::canonicalize(&scratch).unwrap(),
            next: 0,
            epoch,
            children: Vec::new(),
            paths: None,
        }
    }
    /// The lawful candidate file the `candidate` child writes.
    fn candidate_file(&self) -> PathBuf {
        self.scratch.join("candidate.json")
    }
    fn spawn(
        &mut self,
        role: &str,
        arms: Option<&str>,
        extra: &str,
    ) -> Result<MatrixChild, Harness> {
        let ordinal = self.next;
        self.next += 1;
        let input = self.scratch.join(format!("input-{ordinal}"));
        let base = self.paths.as_ref().map(Paths::lines).unwrap_or_default();
        fs::write(&input, format!("{base}{extra}")).map_err(harness("input"))?;
        MatrixChild::spawn(&ChildSpec {
            entry: ENTRY,
            role,
            input: &input,
            arms,
            clock: Some(ScriptedClock {
                epoch: self.epoch,
                ordinal,
            }),
            scratch_parent: &self.scratch,
        })
        .map_err(harness("spawn"))
    }
    /// Record a child under the ordinal it was spawned with.
    fn record_at(&mut self, role: &str, ordinal: u32, exit: &Exit) {
        let held = exit.records.iter().rev().find(|held| {
            held.event == "held"
                && !exit
                    .records
                    .iter()
                    .any(|r| r.point == held.point && r.event == "resumed")
        });
        let (records, sha) = normalized_trace(&exit.records);
        self.children.push(ChildRecord {
            role: role.to_owned(),
            ordinal,
            exit: match (exit.status.signal(), exit.status.code()) {
                (Some(signal), _) => ChildExit::Signal(signal),
                (None, Some(code)) => ChildExit::Code(code),
                (None, None) => ChildExit::Code(-1),
            },
            last_held: held.map(|r| r.point.clone()),
            trace_records: records,
            trace_sha256: sha,
            outcome: exit.outcome().map(normalized_text),
        });
        self.children.sort_by_key(|c| c.ordinal);
        if exit
            .outcome()
            .is_some_and(|o| o.starts_with("kind=authoritative"))
        {
            let misses = release_order_misses(&format!("{role}#{ordinal}"), &exit.records);
            RELEASE_ORDER.with(|r| r.borrow_mut().extend(misses));
        }
    }
    fn record(&mut self, role: &str, exit: &Exit) {
        let ordinal = self.next - 1;
        self.record_at(role, ordinal, exit);
    }
    /// Ordinal 0: the fixture child.
    fn fixture(&mut self) -> Result<(), Harness> {
        let out = self.scratch.join("fixture.out");
        let child = self.spawn("fixture", None, &format!("out={}\n", out.display()))?;
        let exit = child.finish().map_err(harness("fixture"))?;
        if !exit.status.success() {
            return Err(Harness(format!(
                "fixture child {:?}: {}",
                exit.status,
                exit.diagnostics.join("\n")
            )));
        }
        self.record("fixture", &exit);
        let text = fs::read_to_string(&out).map_err(harness("fixture out"))?;
        let map: BTreeMap<&str, &str> = text.lines().filter_map(|l| l.split_once('=')).collect();
        self.paths = Some(Paths {
            home: PathBuf::from(map["home"]),
            installation: PathBuf::from(map["installation"]),
            store: map["store"].to_owned(),
            project: PathBuf::from(map["project"]),
            closure: map["closure"].to_owned(),
        });
        Ok(())
    }
    /// The `candidate` child (X9 r10): it must end with the candidate file
    /// written, and leave no ledger or attempt row.
    fn candidate(&mut self) -> Result<(), Harness> {
        let out = self.candidate_file();
        let exit = self.finished("candidate", "", &format!("out={}\n", out.display()))?;
        if !exit.outcome().is_some_and(|o| o.starts_with("candidate;")) || !out.exists() {
            return Err(Harness(format!("candidate child: {:?}", exit.outcome())));
        }
        let state = self.capture()?;
        if count_rows(&state.logical, "attempt_custody") != 0 || ledger_present(&state) {
            return Err(Harness(
                "the candidate child left a ledger or an attempt row (X9 r10: stop and report)"
                    .into(),
            ));
        }
        Ok(())
    }
    fn paths(&self) -> &Paths {
        self.paths.as_ref().expect("fixture ran")
    }
    /// A child run to its end: exit 0, every armed point reached.
    fn finished(&mut self, role: &str, arms: &str, extra: &str) -> Result<Exit, Harness> {
        let child = self.spawn(role, Some(arms), extra)?;
        let exit = child.finish().map_err(harness(role))?;
        exit.verify_finished()
            .map_err(|e| Harness(format!("{role}: {e:?}\n{}", exit.diagnostics.join("\n"))))?;
        self.record(role, &exit);
        Ok(exit)
    }
    fn capture(&self) -> Result<PostState, Harness> {
        capture(&self.paths().home).map_err(harness("capture"))
    }
    fn finalize_input(&self, candidate: &Path) -> String {
        format!("candidate={}\n", candidate.display())
    }
}
impl Drop for Run {
    fn drop(&mut self) {
        let _ = std::process::Command::new("/bin/chmod")
            .args(["-R", "-N"])
            .arg(&self.scratch)
            .stderr(std::process::Stdio::null())
            .status();
        let _ = std::process::Command::new("/bin/chmod")
            .args(["-R", "u+rwX"])
            .arg(&self.scratch)
            .stderr(std::process::Stdio::null())
            .status();
        let _ = fs::remove_dir_all(&self.scratch);
    }
}

/// A string with every drawn value numbered by first appearance.
fn normalized_text(text: &str) -> String {
    match normalize(&V::String(text.to_owned())) {
        V::String(s) => s,
        _ => unreachable!(),
    }
}

/// Item 7's trace digest, comparable between repetitions (X9 r8 item 7).
fn normalized_trace(records: &[Record]) -> (u64, String) {
    trace_digest(&normalized_lines(records))
}

/// The lines `normalized_trace` digests: each thread's records in its own
/// order (threads by index), without the pid and the process-wide sequence
/// number, every drawn value numbered by first appearance.
fn normalized_lines(records: &[Record]) -> Vec<String> {
    let mut threads: BTreeMap<u64, Vec<&Record>> = BTreeMap::new();
    for r in records {
        threads.entry(r.thread).or_default().push(r);
    }
    let lines: Vec<V> = threads
        .into_values()
        .flat_map(object_groups_ordered)
        .map(|r| {
            V::String(format!(
                "{}|{}|{}|{}",
                r.thread, r.point, r.event, r.payload
            ))
        })
        .collect();
    let V::Array(lines) = normalize(&V::Array(lines)) else {
        unreachable!()
    };
    lines
        .into_iter()
        .map(|v| match v {
            V::String(s) => s,
            _ => unreachable!(),
        })
        .collect()
}

/// Law X9 r14 (r8's trace rule): one thread's records with each object
/// publication's per-object groups in a fixed order. A maximal run of
/// consecutive `x3c.object/` records is split at each `create.before`; the
/// groups are ordered by their records without occurrence numbers (stably),
/// then each name's occurrence numbers are reassigned ascending in that
/// order. Where every group is alike nothing moves. The same rule as
/// storage's matrix target.
fn object_groups_ordered(records: Vec<&Record>) -> Vec<Record> {
    let object = |r: &Record| r.name().starts_with("x3c.object/");
    let mut out: Vec<Record> = Vec::new();
    let mut at = 0;
    while at < records.len() {
        if !object(records[at]) {
            out.push(records[at].clone());
            at += 1;
            continue;
        }
        let end = (at..records.len())
            .find(|&i| !object(records[i]))
            .unwrap_or(records.len());
        let run = &records[at..end];
        let mut groups: Vec<Vec<&Record>> = Vec::new();
        for r in run {
            if r.name() == "x3c.object/create.before" || groups.is_empty() {
                groups.push(Vec::new());
            }
            groups.last_mut().expect("a group").push(r);
        }
        let key = |g: &Vec<&Record>| {
            g.iter()
                .map(|r| format!("{}|{}|{}", r.name(), r.event, r.payload))
                .collect::<Vec<_>>()
        };
        groups.sort_by_cached_key(key);
        let mut free: BTreeMap<String, Vec<u32>> = BTreeMap::new();
        for r in run {
            free.entry(r.name().to_owned())
                .or_default()
                .push(r.occurrence().unwrap_or(0));
        }
        for list in free.values_mut() {
            list.sort_unstable();
            list.reverse();
        }
        for r in groups.into_iter().flatten() {
            let mut moved = r.clone();
            if let Some(k) = free.get_mut(r.name()).and_then(Vec::pop) {
                moved.point = format!("{}#{k}", r.name());
            }
            out.push(moved);
        }
        at = end;
    }
    out
}

/// The draw point's ExecutionId (its `pass` payload), if the child drew.
fn drawn_execution(exit: &Exit) -> Option<String> {
    exit.records
        .iter()
        .find(|r| r.name() == "x3d.session.execution-draw" && r.event == "pass")
        .map(|r| r.payload.clone())
        .filter(|p| p.starts_with("exec1_"))
}

/// A writer's start witness action, from its trace.
fn witness_action(exit: &Exit) -> String {
    for (step, action) in [
        ("revert", "REVERT"),
        ("advance", "ADVANCE"),
        ("init", "INIT"),
        ("open", "OPEN"),
    ] {
        let prefix = format!("x3b.start.witness.{step}");
        if exit.records.iter().any(|r| r.name().starts_with(&prefix)) {
            return action.into();
        }
    }
    "OK".into()
}

/// A writer's floor step decision, from its trace.
fn floor_decision(exit: &Exit) -> String {
    if exit
        .records
        .iter()
        .any(|r| r.name().starts_with("x3b.floor") && r.name().ends_with("/rename.after"))
    {
        "published".into()
    } else {
        "unchanged".into()
    }
}

/// A `finalize` child's report fields.
fn fields(exit: &Exit) -> BTreeMap<String, String> {
    exit.outcome()
        .unwrap_or("")
        .split(';')
        .filter_map(|f| f.split_once('='))
        .map(|(k, v)| (k.to_owned(), v.to_owned()))
        .collect()
}

/// A finalize outcome's head: `authoritative:<exit>` or
/// `terminated:<row>`.
fn outcome_head(exit: &Exit) -> String {
    let f = fields(exit);
    match f.get("kind").map(String::as_str) {
        Some("authoritative") => format!("authoritative:{}", f["exit"]),
        Some("interrupted") => format!("interrupted:{}", f["exit"]),
        Some("terminated") => format!("terminated:{}", f["row"]),
        _ => format!("none:{}", exit.outcome().unwrap_or("")),
    }
}

/// A `store-gc` report without the ExecutionIds: what each namespace's
/// sweep did and its row.
fn gc_value(outcome: &str) -> String {
    let mut out = String::new();
    let mut rest = outcome;
    // `settled=e=o,e=o` and `left=e=r,…` lists, by their outcomes only.
    while let Some(at) = rest.find("exec1_") {
        out.push_str(&rest[..at]);
        let tail = &rest[at..];
        let end = tail.find('=').unwrap_or(tail.len());
        rest = &tail[(end + 1).min(tail.len())..];
    }
    out.push_str(rest);
    out
}

/// The (ExecutionId, outcome) pairs a `store-gc` report settled.
fn gc_settled(outcome: &str) -> Vec<(String, String)> {
    outcome
        .split("settled=")
        .skip(1)
        .flat_map(|rest| {
            rest.split(';')
                .next()
                .unwrap_or("")
                .split(',')
                .filter(|e| !e.is_empty())
                .filter_map(|e| e.split_once('='))
                .map(|(e, o)| (e.to_owned(), o.to_owned()))
                .collect::<Vec<_>>()
        })
        .collect()
}

// ------------------------------------------------- the census (X9 r11)

/// The three unarmed census runs of X9 r11 item 5, each after its own
/// fixture and `candidate` child: (a) a lawful `finalize` commit, (b) an
/// exhausted-carrier `finalize` after F32's reserved-slot setup at `…988`,
/// whose `finish` runs the rollover, (c) a `store-gc` after an unarmed (a)
/// on the same root. Only the named child's trace is the run's.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum CensusRun {
    Lawful,
    Exhausted,
    StoreGc,
}

/// The exhausted tail: no `SEAL` fits (X3b item 5a).
const EXHAUSTED_TAIL: i64 = 9_007_199_254_740_988;
/// The last tail at which a `SEAL` fits (X3b item 5a).
const LAST_SEAL_TAIL: i64 = 9_007_199_254_740_987;

fn census_run(epoch: i64, which: CensusRun) -> Result<(Census, Vec<Record>), Harness> {
    let mut run = Run::new(epoch);
    run.fixture()?;
    run.candidate()?;
    if which == CensusRun::Exhausted {
        plant(&run, EXHAUSTED_TAIL)?;
    }
    let input = run.finalize_input(&run.candidate_file());
    let exit = run.finished("finalize", "", &input)?;
    let head = outcome_head(&exit);
    let exit = match which {
        CensusRun::Lawful => {
            if head != "authoritative:0" {
                return Err(Harness(format!("census (a): {:?}", exit.outcome())));
            }
            exit
        }
        CensusRun::Exhausted => {
            if !exit.outcome().unwrap_or("").contains("rollover=rolled:2") {
                return Err(Harness(format!("census (b): {:?}", exit.outcome())));
            }
            exit
        }
        CensusRun::StoreGc => {
            if head != "authoritative:0" {
                return Err(Harness(format!("census (c) commit: {:?}", exit.outcome())));
            }
            let gc = run.finished("store-gc", "", "")?;
            if !gc
                .records
                .iter()
                .any(|r| r.name().starts_with("x6.sweep.settle.commit"))
            {
                return Err(Harness(format!(
                    "census (c): no x6.sweep.settle.commit point: {:?}",
                    gc.outcome()
                )));
            }
            gc
        }
    };
    let census = Census::from_exit(&exit).map_err(harness("census"))?;
    Ok((census, exit.records.clone()))
}

/// X9 r11's union: a point reached in more than one run takes the largest
/// occurrence count.
fn union(parts: &[&Census]) -> Census {
    let mut points: BTreeMap<String, CensusPoint> = BTreeMap::new();
    for part in parts {
        for p in &part.points {
            points
                .entry(p.name.clone())
                .and_modify(|q| q.occurrences = q.occurrences.max(p.occurrences))
                .or_insert_with(|| p.clone());
        }
    }
    Census {
        points: points.into_values().collect(),
    }
}

/// Each of (a), (b) and (c) twice, equal point for point; their union; the
/// trace lines of (a), then (b), then (c); and each run's raw trace.
#[allow(clippy::type_complexity)]
fn host_census(
    epoch: i64,
) -> Result<(Census, Vec<String>, Vec<(CensusRun, Vec<Record>)>), Harness> {
    let mut parts = Vec::new();
    let mut lines = Vec::new();
    let mut traces = Vec::new();
    for which in [CensusRun::Lawful, CensusRun::Exhausted, CensusRun::StoreGc] {
        let (first, records) = census_run(epoch, which)?;
        let (second, _) = census_run(epoch, which)?;
        if first != second {
            return Err(Harness(format!(
                "HARNESS-ERROR: the two census runs of {which:?} differ"
            )));
        }
        lines.extend(normalized_lines(&records));
        traces.push((which, records));
        parts.push(first);
    }
    let refs: Vec<&Census> = parts.iter().collect();
    Ok((union(&refs), lines, traces))
}

// --------------------------------------------------------------- run sets

fn repository() -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR")).join("../..")
}
fn command(program: &str, args: &[&str]) -> String {
    // The pinned macOS build PATH contains Rust and Homebrew, not /usr/bin.
    let executable = if cfg!(target_os = "macos") && program == "git" {
        "/usr/bin/git"
    } else {
        program
    };
    let mut command = std::process::Command::new(executable);
    command.args(args).current_dir(repository());
    if program == "git" {
        command
            .env_remove("GIT_CONFIG_COUNT")
            .env_remove("GIT_DIR")
            .env_remove("GIT_WORK_TREE")
            .env("GIT_CONFIG_NOSYSTEM", "1")
            .env("GIT_CONFIG_GLOBAL", "/dev/null");
    }
    let out = command
        .output()
        .unwrap_or_else(|e| panic!("{executable}: {e}"));
    assert!(out.status.success(), "{executable} metadata command failed");
    String::from_utf8_lossy(&out.stdout).trim().to_owned()
}

#[test]
fn x9_metadata_product_uses_host_git_with_pinned_path() {
    let record = product();
    assert_eq!(record.commit.len(), 40);
    assert!(
        record
            .commit
            .bytes()
            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
    );
    assert!(record.toolchain.starts_with("rustc "));
    let expected = std::process::Command::new(if cfg!(target_os = "macos") {
        "/usr/bin/git"
    } else {
        "git"
    })
    .args(["status", "--porcelain"])
    .current_dir(repository())
    .env_remove("GIT_CONFIG_COUNT")
    .env_remove("GIT_DIR")
    .env_remove("GIT_WORK_TREE")
    .env("GIT_CONFIG_NOSYSTEM", "1")
    .env("GIT_CONFIG_GLOBAL", "/dev/null")
    .output()
    .unwrap();
    assert!(expected.status.success());
    assert_eq!(record.worktree_clean, expected.stdout.is_empty());
}
#[test]
#[should_panic(expected = "metadata command failed")]
fn x9_metadata_command_failure_refuses() {
    command(
        "git",
        &[
            "rev-parse",
            "--verify",
            "refs/opensip-x9-metadata-missing-control",
        ],
    );
}

fn product() -> Product {
    Product {
        commit: command("git", &["rev-parse", "HEAD"]),
        worktree_clean: command("git", &["status", "--porcelain"]).is_empty(),
        toolchain: command("rustc", &["-vV"]),
    }
}
fn host() -> Host {
    let os = format!(
        "{} {} ({})",
        command("/usr/bin/sw_vers", &["-productName"]),
        command("/usr/bin/sw_vers", &["-productVersion"]),
        command("/usr/bin/sw_vers", &["-buildVersion"])
    );
    Host {
        os,
        arch: std::env::consts::ARCH.replace("aarch64", "arm64"),
        filesystem: "apfs".into(),
    }
}

fn member<'a>(v: &'a V, key: &str) -> Option<&'a V> {
    match v {
        V::Object(o) => o.get(key),
        _ => None,
    }
}
fn text(v: &V) -> &str {
    match v {
        V::String(s) => s,
        _ => panic!("string"),
    }
}

/// Whether `observed` meets `expected`: a string (a trailing `:*` admits
/// any typed member after the standing), or any of a list.
fn meets(expected: &V, observed: &str) -> bool {
    match expected {
        V::String(s) => match s.strip_suffix(":*") {
            Some(standing) => observed
                .strip_prefix(standing)
                .is_some_and(|rest| rest.is_empty() || rest.starts_with(':')),
            None => s == observed,
        },
        V::Array(items) => items.iter().any(|i| meets(i, observed)),
        _ => false,
    }
}

/// The reviewed host required runs X9-5 runs: every row without a `unit`
/// member (law X9 r16: the `"X9-6"` rows are X9-6's).
fn required() -> (i64, Vec<V>) {
    let (epoch, runs) = required_all();
    (
        epoch,
        runs.into_iter()
            .filter(|r| member(r, "unit").is_none())
            .collect(),
    )
}

/// Every reviewed host required run (X9-6's run set).
fn required_all() -> (i64, Vec<V>) {
    let raw =
        fs::read(Path::new(env!("CARGO_MANIFEST_DIR")).join(REQUIRED)).expect("required runs");
    let value = parse_json(&raw).expect("required runs JSON");
    let epoch = match member(&value, "clockEpoch") {
        Some(V::Integer(n)) => n.get() as i64,
        _ => panic!("clockEpoch"),
    };
    let Some(V::Array(runs)) = member(&value, "runs") else {
        panic!("runs")
    };
    let runs = runs
        .iter()
        .filter(|r| {
            UNIT_CASES.contains(&text(member(r, "case").unwrap())) ||
            member(r, "unit").is_some_and(|unit| matches!(text(unit), "J3b" | "J3d"))
        })
        .cloned()
        .collect();
    (epoch, runs)
}

fn strings(v: &V) -> Vec<String> {
    match v {
        V::Array(items) => items.iter().map(|i| text(i).to_owned()).collect(),
        _ => panic!("array"),
    }
}

fn object<const N: usize>(pairs: [(&str, V); N]) -> V {
    V::Object(pairs.into_iter().map(|(k, v)| (k.to_owned(), v)).collect())
}
fn s(text: &str) -> V {
    V::String(text.to_owned())
}

// ------------------------------------------------------ state helpers

/// Rows of `table` in the post state's logical dump, 0 when absent.
fn count_rows(logical: &V, table: &str) -> usize {
    fn walk(v: &V, table: &str) -> usize {
        match v {
            V::Object(o) => o
                .iter()
                .map(|(k, v)| match (k.as_str(), v) {
                    (k, V::Array(rows)) if k == table => rows.len(),
                    _ => walk(v, table),
                })
                .sum(),
            V::Array(items) => items.iter().map(|i| walk(i, table)).sum(),
            _ => 0,
        }
    }
    walk(logical, table)
}

/// Journal rows of `record_type` in every carrier of the post state.
fn journal_rows(logical: &V, record_type: &str) -> usize {
    let Some(V::Object(databases)) = member(logical, "databases") else {
        return 0;
    };
    databases
        .iter()
        .filter(|(path, _)| path.ends_with("grant-journal.sqlite"))
        .filter_map(|(_, db)| member(member(db, "tables")?, "grant_journal_v3"))
        .map(|rows| match rows {
            V::Array(rows) => rows
                .iter()
                .filter(|row| match row {
                    V::Array(cells) => cells.iter().any(|c| *c == s(record_type)),
                    _ => false,
                })
                .count(),
            _ => 0,
        })
        .sum()
}

/// Exact REV bodies in carrier row order. The scripted phase's additions
/// are selected by body multiplicity across the before/after snapshots, so
/// a carrier rename neither invents a REV nor discards one.
fn rev_bodies(logical: &V) -> Result<Vec<(String, String)>, Harness> {
    let mut bodies = Vec::new();
    let Some(V::Object(databases)) = member(logical, "databases") else { return Ok(bodies); };
    for (path, db) in databases {
        if !path.ends_with("grant-journal.sqlite") { continue; }
        let Some(V::Array(rows)) = member(db, "tables").and_then(|tables| member(tables, "grant_journal_v3")) else { continue; };
        for row in rows {
            let V::Array(cells) = row else { return Err(Harness("journal row is not an array".into())); };
            // The selected grant_journal_v3 DDL fixes record_type at column
            // 3 and the canonical TEXT body at column 11.
            if cells.get(3) != Some(&s("REV")) { continue; }
            let body = cells.get(11).ok_or_else(|| Harness("REV body is absent".into()))?;
            let V::String(body) = body else { return Err(Harness("REV body is not text".into())); };
            let decoded = parse_json(body.as_bytes()).map_err(|e| Harness(format!("REV body: {e:?}")))?;
            let reason = member(&decoded, "reason").ok_or_else(|| Harness("REV reason is absent".into()))?;
            let V::String(reason) = reason else { return Err(Harness("REV reason is not text".into())); };
            bodies.push((body.to_owned(), reason.to_owned()));
        }
    }
    Ok(bodies)
}
fn added_rev_reasons(before: &V, after: &V) -> Result<String, Harness> {
    let mut retained: BTreeMap<String, usize> = BTreeMap::new();
    for (body, _) in rev_bodies(before)? { *retained.entry(body).or_default() += 1; }
    let mut added = Vec::new();
    for (body, reason) in rev_bodies(after)? {
        if let Some(count) = retained.get_mut(&body).filter(|count| **count != 0) { *count -= 1; }
        else { added.push(reason); }
    }
    Ok(added.join(","))
}

/// Whether the post state holds any project ledger.
fn ledger_present(state: &PostState) -> bool {
    state.raw.iter().any(|e| e.path.ends_with("ledger.sqlite"))
}

/// The ledger and carrier logical state: every ledger and carrier database
/// and every witness, normalized (F01's "ledger and carrier logical state
/// unchanged").
fn ledger_and_carrier(state: &PostState) -> Result<String, Harness> {
    let pick = |key: &str, keep: &dyn Fn(&str) -> bool| -> V {
        match member(&state.logical, key) {
            Some(V::Object(o)) => V::Object(
                o.iter()
                    .filter(|(p, _)| keep(p))
                    .map(|(p, v)| (p.clone(), v.clone()))
                    .collect(),
            ),
            _ => V::Object(BTreeMap::new()),
        }
    };
    let databases = pick("databases", &|p| {
        p.ends_with("ledger.sqlite") || p.ends_with("grant-journal.sqlite")
    });
    let witnesses = pick("operational", &|p| p.ends_with(".witness.json"));
    normalized_sha256(&object([
        ("databases", databases),
        ("witnesses", witnesses),
    ]))
    .map_err(harness("ledger and carrier"))
}

/// X3b-2's reserved-slot technique at `tail` in N's carrier (F32's setup).
fn plant(run: &Run, tail: i64) -> Result<(), Harness> {
    let (namespace, dir) = run
        .paths()
        .namespace()
        .ok_or_else(|| Harness("no namespace to plant".into()))?;
    support::plant_committed_tail(&dir, &namespace, tail);
    Ok(())
}

// ------------------------------------------------- F01's candidate files

/// The lawful candidate file, as JSON.
fn candidate_json(path: &Path) -> Result<V, Harness> {
    parse_json(&fs::read(path).map_err(harness("candidate"))?).map_err(harness("candidate JSON"))
}

/// F01's variant candidates (X9 r10: written by the parent from the lawful
/// file before the `finalize` child starts; inputs, not stored custody
/// bytes). Returns the variant file's path.
fn candidate_variant(run: &Run, variant: &str) -> Result<PathBuf, Harness> {
    let lawful = run.candidate_file();
    let out = run.scratch.join(format!("candidate-{variant}.json"));
    let file = support::read_run_candidate(&lawful).map_err(Harness)?;
    let (run_id, mut objects, blobs) = (file.run_id, file.objects, file.blobs);
    match variant {
        // The claimed Run object removed: a lost retained byte of the
        // claimed closure (X5 r3 item 5, step 1: `evidence.missing`).
        "replay-run-object-missing" => {
            objects
                .remove(&run_id)
                .ok_or_else(|| Harness("no Run object".into()))?;
        }
        // The Run's descriptor altered so it no longer has its claimed
        // identity (X5 r3 item 5: `EVALUATION.INPUT_REFUSED`).
        "replay-run-descriptor-altered" => {
            let run_object = objects
                .get_mut(&run_id)
                .ok_or_else(|| Harness("no Run object".into()))?;
            let V::Object(fields) = &mut run_object.descriptor else {
                return Err(Harness("Run descriptor".into()));
            };
            fields.insert("planId".into(), s("plan3:altered"));
        }
        // The corpus Run rebound to the session's project, with the
        // corpus's own evaluator closure: a substituted inventory (X3d item
        // 3 step 1's invariant row).
        "substituted-inventory" => {
            let project = fs::read_to_string(lawful.with_extension("project"))
                .map_err(harness("project id"))?;
            let c = run_candidate::project_rebound_corpus(&project);
            return write_variant(&out, c.run_id(), c.objects(), c.blobs());
        }
        // The session's core evaluator closure, bound to another project: a
        // substituted target (X3d item 3 step 1's invariant row).
        "substituted-target" => {
            let document = candidate_json(&lawful)?;
            let descriptor = evaluator_descriptor(&document)?;
            // Another well-formed ProjectId: the session's own with its last
            // hex digit changed.
            let project = fs::read_to_string(lawful.with_extension("project"))
                .map_err(harness("project id"))?;
            let (head, last) = project.split_at(project.len() - 1);
            let other = format!("{head}{}", if last == "0" { "1" } else { "0" });
            let other = run_candidate::project_rebound_corpus(&other);
            let c = run_candidate::renaming_the_evaluator_closure(&other, descriptor);
            // The closure's manifest and tree blobs are retained as the
            // lawful candidate retains them (X9 r7).
            let mut merged = c.blobs().clone();
            merged.extend(blobs);
            return write_variant(&out, c.run_id(), c.objects(), &merged);
        }
        other => return Err(Harness(format!("unknown candidate variant {other}"))),
    }
    write_variant(&out, &run_id, &objects, &blobs)
}

fn write_variant(
    out: &Path,
    run_id: &str,
    objects: &BTreeMap<String, opensip_identity::ObjectInput>,
    blobs: &BTreeMap<[u8; 32], Vec<u8>>,
) -> Result<PathBuf, Harness> {
    support::write_run_candidate(out, run_id, objects, blobs).map_err(Harness)?;
    Ok(out.to_owned())
}

/// The lawful candidate's evaluator closure descriptor: the closure its
/// seal names.
fn evaluator_descriptor(document: &V) -> Result<V, Harness> {
    let Some(V::Object(objects)) = member(document, "objects") else {
        return Err(Harness("candidate objects".into()));
    };
    let seal = objects
        .values()
        .find(|o| member(o, "domain") == Some(&s("evaluation-seal")))
        .ok_or_else(|| Harness("no seal".into()))?;
    let closure = member(member(seal, "descriptor").unwrap(), "evaluatorClosure")
        .map(text)
        .ok_or_else(|| Harness("evaluatorClosure".into()))?;
    member(&objects[closure], "descriptor")
        .cloned()
        .ok_or_else(|| Harness("closure descriptor".into()))
}

// ----------------------------------------------------------- one run

/// What a run observed.
struct Observed {
    timing_guard_ms: Option<u64>,
    ladder: Vec<V>,
    values: BTreeMap<String, String>,
    not_applicable: Option<String>,
    post: PostState,
}

/// Item 8's ladder over the run's scripted phase, through host: R1
/// `recover`, R2 a `finalize` over the lawful candidate, R3 `store-gc`, R4
/// `recover`. `crashed` is the scripted `finalize` child's ExecutionId.
fn ladder(
    run: &mut Run,
    crashed: Option<&str>,
    distinct: bool,
    values: &mut BTreeMap<String, String>,
) -> Result<Vec<V>, Harness> {
    let mut ladder = Vec::new();
    let recover_input = |exec: &str, n: &str| format!("execution={exec}\nnamespace={n}\n");
    let namespace = run.paths().namespace().map(|(n, _)| n);
    // R1.
    if let (Some(exec), Some(n)) = (crashed, namespace.as_deref()) {
        let before = run.capture()?;
        let exit = run.finished("recover", "", &recover_input(exec, n))?;
        let after = run.capture()?;
        let standing = normalized_text(exit.outcome().unwrap_or("none"));
        let unchanged = before.normalized_sha256 == after.normalized_sha256;
        values.insert("R1".into(), standing.clone());
        values.insert("R1.stateUnchanged".into(), unchanged.to_string());
        ladder.push(object([
            ("step", s("R1-recover")),
            ("standing", s(&standing)),
            ("stateUnchanged", V::Bool(unchanged)),
        ]));
    }
    // R2: the candidate, or (X9 r12 and r13, after a committed Run) r12's
    // distinct variant.
    let r2 = if distinct {
        run.candidate_file().with_extension("distinct.json")
    } else {
        run.candidate_file()
    };
    let input = run.finalize_input(&r2);
    let exit = run.finished("finalize", "", &input)?;
    let action = witness_action(&exit);
    let outcome = outcome_head(&exit);
    let rollover = fields(&exit).get("rollover").cloned().unwrap_or_default();
    let r2_exec = drawn_execution(&exit);
    values.insert("R2.witnessAction".into(), action.clone());
    values.insert("R2.outcome".into(), outcome.clone());
    values.insert("R2.rollover".into(), rollover.clone());
    ladder.push(object([
        ("step", s("R2-next-writer")),
        ("floor", s(&floor_decision(&exit))),
        ("witnessAction", s(&action)),
        ("outcome", s(&outcome)),
        ("rollover", s(&rollover)),
    ]));
    // R3.
    let exit = run.finished("store-gc", "", "")?;
    let report = exit.outcome().unwrap_or("none").to_owned();
    let mut wrote = "nothing".to_owned();
    let mut others = Vec::new();
    for (exec, outcome) in gc_settled(&report) {
        if Some(exec.as_str()) == crashed {
            wrote = outcome;
        } else if Some(&exec) == r2_exec.as_ref() {
            others.push(format!("next-writer={outcome}"));
        } else {
            others.push(format!("other={outcome}"));
        }
    }
    values.insert("R3".into(), wrote.clone());
    values.insert("R3.others".into(), others.join(","));
    ladder.push(object([
        ("step", s("R3-sweep")),
        ("wrote", s(&wrote)),
        ("nextWriter", s(&others.join(","))),
    ]));
    // R4.
    let namespace = run.paths().namespace().map(|(n, _)| n);
    if let (Some(exec), Some(n)) = (crashed, namespace.as_deref()) {
        let exit = run.finished("recover", "", &recover_input(exec, n))?;
        let standing = normalized_text(exit.outcome().unwrap_or("none"));
        values.insert("R4".into(), standing.clone());
        ladder.push(object([
            ("step", s("R4-recover")),
            ("standing", s(&standing)),
        ]));
    }
    Ok(ladder)
}

/// Record a scripted child's observation under `slot`.
fn observe(values: &mut BTreeMap<String, String>, slot: &str, exit: &Exit, killed: bool) {
    if killed {
        values.insert(slot.into(), "killed".into());
        return;
    }
    let outcome = exit.outcome().unwrap_or("none");
    if slot.starts_with("finalize") {
        for (k, v) in fields(exit) {
            values.insert(format!("{slot}.{k}"), v);
        }
        values.insert(slot.into(), outcome_head(exit));
        // X7 item 4: whether the delivery phase was started at all.
        let started = exit
            .records
            .iter()
            .any(|r| r.name().starts_with("x7.delivery"));
        values.insert(
            format!("{slot}.deliveryPhase"),
            if started { "started" } else { "not-started" }.into(),
        );
        let latched = exit
            .records
            .iter()
            .any(|r| r.name() == "x4.gate.latch.after");
        values.insert(format!("{slot}.gateLatched"), latched.to_string());
    } else {
        values.insert(slot.into(), gc_value(outcome));
    }
}

/// One required run, end to end: the fixture and `candidate` children,
/// then the row's script, step by step, then item 8's ladder where the row
/// leaves an attempt to it.
fn execute(row: &V, epoch: i64) -> Result<Observed, Harness> {
    let V::Array(script) = member(row, "script").unwrap().clone() else {
        panic!("script")
    };
    let ladder_wanted = !NO_LADDER.contains(&text(member(row, "case").unwrap()));
    let mut run = Run::new(epoch);
    run.fixture()?;
    run.candidate()?;
    let mut values = BTreeMap::new();
    let mut arms: Vec<String> = Vec::new();
    let mut candidate = run.candidate_file();
    let mut distinct = false;
    let mut timing_guard_ms: Option<u64> = None;
    let mut crashed: Option<String> = None;
    let mut before_finalize: Option<PostState> = None;
    let mut counts: BTreeMap<String, usize> = BTreeMap::new();
    let mut i = 0;
    while i < script.len() {
        let step = &script[i];
        i += 1;
        if let Some(tail) = member(step, "plant") {
            plant(
                &run,
                match text(tail) {
                    "tail-987" => LAST_SEAL_TAIL,
                    "tail-988" => EXHAUSTED_TAIL,
                    other => return Err(Harness(format!("plant {other}"))),
                },
            )?;
        } else if let Some(variant) = member(step, "candidate") {
            candidate = candidate_variant(&run, text(variant))?;
        } else if let Some(arm) = member(step, "arm") {
            arms.push(text(arm).to_owned());
        } else if let Some(r2) = member(step, "r2") {
            distinct = text(r2) == "distinct";
        } else if let Some(kind) = member(step, "mutate") {
            mutate(&run, text(kind))?;
        } else if let Some(role) = member(step, "run") {
            let role = text(role).to_owned();
            let n = counts.entry(role.clone()).or_default();
            *n += 1;
            let slot = format!(
                "{}{}",
                if role == "finalize" { "finalize" } else { "gc" },
                n
            );
            let extra = if role == "finalize" {
                if before_finalize.is_none() {
                    before_finalize = Some(run.capture()?);
                }
                run.finalize_input(&candidate)
            } else {
                String::new()
            };
            let armed = arms.join(",");
            arms.clear();
            // The next step, if it awaits this child.
            let awaited = script.get(i).and_then(|next| {
                Some((
                    text(member(next, "await")?).to_owned(),
                    text(member(next, "then")?).to_owned(),
                ))
            });
            let (exit, killed) = match awaited {
                None => (run.finished(&role, &armed, &extra)?, false),
                Some((point, then)) => {
                    i += 1;
                    let mut child = run.spawn(&role, Some(&armed), &extra)?;
                    let ordinal = run.next - 1;
                    if then == "revoke-latch-resume" {
                        // Item 11's timing guard (r12, r13, r15): from the
                        // parent's read of the writer's first observer-tick
                        // hold to its first hold at any other point.
                        child
                            .await_held("x4.observer.tick#1")
                            .map_err(harness("await tick"))?;
                        let start = GuardClock::now();
                        child.await_held(&point).map_err(harness("await held"))?;
                        let ms = u64::try_from(start.elapsed().as_millis()).unwrap_or(u64::MAX);
                        timing_guard_ms = Some(ms);
                        if ms > TIMING_GUARD_LIMIT_MS {
                            return Err(Harness(format!(
                                "timing guard: {ms} ms above {TIMING_GUARD_LIMIT_MS} ms"
                            )));
                        }
                    } else {
                        child.await_held(&point).map_err(harness("await held"))?;
                    }
                    match then.as_str() {
                        "kill" => {
                            let exit = child.kill().map_err(harness("kill"))?;
                            exit.verify_death_at(&point).map_err(|e| {
                                Harness(format!(
                                    "death at {point}: {e:?}\n{}",
                                    exit.diagnostics.join("\n")
                                ))
                            })?;
                            run.record_at(&role, ordinal, &exit);
                            (exit, true)
                        }
                        // Item 11: the parent publishes (here, a publisher
                        // child that holds no operation), resumes one
                        // observer tick, awaits the gate's latch, then
                        // resumes the held thread.
                        "signal-resume" => {
                            child.signal(opensip_platform::crash_barrier::SignalInput::Sigint).map_err(harness("signal"))?;
                            child.resume(&point).map_err(harness("resume"))?;
                            finish_child(&mut run, child, &role, ordinal)?
                        }
                        "revoke-latch-resume" => {
                            let closure = run.candidate_file().with_extension("closure");
                            let published = run.finished(
                                "publisher",
                                "",
                                &format!("core-closure={}\n", closure.display()),
                            )?;
                            if !published
                                .outcome()
                                .is_some_and(|o| o.starts_with("published:1->2"))
                            {
                                return Err(Harness(format!(
                                    "publisher: {:?}",
                                    published.outcome()
                                )));
                            }
                            let tick = "x4.observer.tick#1";
                            let latched = child
                                .resume(tick)
                                .and_then(|()| child.await_event("x4.gate.latch.after#1", "pass"));
                            if let Err(e) = latched {
                                return Err(Harness(format!(
                                    "await latch: {e:?}\n{}",
                                    stopped(child)
                                )));
                            }
                            child.resume(&point).map_err(harness("resume"))?;
                            finish_child(&mut run, child, &role, ordinal)?
                        }
                        // F53's live writer: a `store-gc` while the writer
                        // holds, then the writer resumed to its end.
                        "store-gc-resume" => {
                            let n = counts.entry("store-gc".into()).or_default();
                            *n += 1;
                            let gc_slot = format!("gc{n}");
                            let gc = run.finished("store-gc", "", "")?;
                            observe(&mut values, &gc_slot, &gc, false);
                            child.resume(&point).map_err(harness("resume"))?;
                            finish_child(&mut run, child, &role, ordinal)?
                        }
                        other => return Err(Harness(format!("unknown then {other}"))),
                    }
                }
            };
            if role == "finalize" && crashed.is_none() {
                crashed = drawn_execution(&exit);
            }
            observe(&mut values, &slot, &exit, killed);
        } else {
            return Err(Harness(format!("unknown script step {step:?}")));
        }
    }
    let post = run.capture()?;
    values.insert(
        "attemptRows".into(),
        count_rows(&post.logical, "attempt_custody").to_string(),
    );
    values.insert(
        "sealRows".into(),
        journal_rows(&post.logical, "SEAL").to_string(),
    );
    if let Some(before) = &before_finalize {
        values.insert(
            "ledgerCarrierUnchanged".into(),
            (ledger_and_carrier(before)? == ledger_and_carrier(&post)?).to_string(),
        );
        values.insert(
            "stateUnchanged".into(),
            (before.normalized_sha256 == post.normalized_sha256).to_string(),
        );
        // X9 r13 (F01): the journal records the scripted phase added, by
        // type, and whether a ledger exists.
        let mut added = Vec::new();
        for kind in ["RA", "SEAL", "REV", "CLN", "TERMINAL"] {
            let n = journal_rows(&post.logical, kind)
                .saturating_sub(journal_rows(&before.logical, kind));
            added.extend(std::iter::repeat_n(kind, n));
        }
        values.insert("carrierAdded".into(), added.join(","));
        values.insert("revReasons".into(), added_rev_reasons(&before.logical, &post.logical)?);
        values.insert("ledgerPresent".into(), ledger_present(&post).to_string());
    }
    let ladder = if ladder_wanted {
        ladder(&mut run, crashed.as_deref(), distinct, &mut values)?
    } else {
        Vec::new()
    };
    let not_applicable = crashed.is_none().then(|| "no-execution-id".to_owned());
    let children = std::mem::take(&mut run.children);
    CHILDREN.with(|c| *c.borrow_mut() = children);
    Ok(Observed {
        timing_guard_ms,
        ladder,
        values,
        not_applicable,
        post,
    })
}

/// A harness failure's diagnostics: the child stopped and its trace's last
/// records with its untagged stderr.
fn stopped(child: MatrixChild) -> String {
    match child.kill() {
        Ok(exit) => {
            let trace = exit.trace();
            let tail = trace[trace.len().saturating_sub(40)..].join("\n");
            format!("{tail}\n{}", exit.diagnostics.join("\n"))
        }
        Err(e) => format!("(no trace: {e})"),
    }
}

/// A held child resumed: it must run to its end with every arm reached.
fn finish_child(
    run: &mut Run,
    child: MatrixChild,
    role: &str,
    ordinal: u32,
) -> Result<(Exit, bool), Harness> {
    let exit = child.finish().map_err(harness("finish"))?;
    exit.verify_finished().map_err(|e| {
        Harness(format!(
            "held {role}: {e:?}\n{}",
            exit.diagnostics.join("\n")
        ))
    })?;
    run.record_at(role, ordinal, &exit);
    Ok((exit, false))
}

/// F53's inaccessible namespace: N's ledger made mode 000, and restored.
fn mutate(run: &Run, kind: &str) -> Result<(), Harness> {
    let (namespace, _) = run
        .paths()
        .namespace()
        .ok_or_else(|| Harness("no namespace".into()))?;
    let ledger = run.paths().ledger_dir(&namespace).join("ledger.sqlite");
    let saved = run.scratch.join("ledger-mode");
    let mode = match kind {
        "ledger-mode-000" => {
            let mode = fs::metadata(&ledger)
                .map_err(harness("ledger"))?
                .permissions()
                .mode();
            fs::write(&saved, format!("{:o}", mode & 0o7777)).map_err(harness("mode"))?;
            0o000
        }
        "ledger-mode-restore" => {
            let text = fs::read_to_string(&saved).map_err(harness("mode"))?;
            u32::from_str_radix(&text, 8).map_err(harness("mode"))?
        }
        other => return Err(Harness(format!("unknown mutation {other}"))),
    };
    fs::set_permissions(&ledger, fs::Permissions::from_mode(mode)).map_err(harness("chmod"))
}

// ------------------------------------------- the release order (X9 r16)

thread_local! {
    /// Law X9 r16 (item 8): release-order misses of the current run's
    /// commit children, read into the run's verdict.
    static RELEASE_ORDER: std::cell::RefCell<Vec<String>> = const { std::cell::RefCell::new(Vec::new()) };
}

/// Law X9 r16 (item 8; build plan lines 139-143, 168-172 and 608): the
/// guard order on a commit child's own trace. Acquisition: the journal's
/// level 3, then the ledger's level 3, then level 4. Release: the evidence
/// `COMMIT`, level 4, level 3, then the writer lease, then the end fence;
/// an owed `REV` or `CLN` append releases its level 4 and level 3 before
/// that lease. Each step is its point's first record (the process-wide
/// sequence); the lease and the fence are the first after the SEAL's
/// level-3 release.
fn release_order_misses(role: &str, records: &[Record]) -> Vec<String> {
    let first = |name: &str, after: u64| {
        records
            .iter()
            .filter(|r| r.name() == name && r.sequence > after)
            .map(|r| r.sequence)
            .min()
    };
    let mut misses = Vec::new();
    let mut chain = |names: &[&str], what: &str| {
        let mut at = 0;
        for name in names {
            match first(name, 0) {
                Some(n) if n > at => at = n,
                Some(_) => {
                    misses.push(format!("{role}: {what} order: {name} out of order"));
                    return None;
                }
                None => {
                    misses.push(format!("{role}: {what} order: no {name}"));
                    return None;
                }
            }
        }
        Some(at)
    };
    chain(
        &[
            "x3b.append.seal.begin",
            "x3c.evidence.begin",
            "x3b.append.seal.level-four",
        ],
        "acquisition",
    );
    let Some(level_three) = chain(
        &[
            "x3c.evidence.commit.after",
            "x3b.append.seal.release-level-four",
            "x3b.append.seal.release-level-three",
        ],
        "release",
    ) else {
        return misses;
    };
    let Some(lease) = first("x2.lease.writer/unlock.after", level_three) else {
        misses.push(format!(
            "{role}: release order: no writer lease release after level 3"
        ));
        return misses;
    };
    if first("x2.fence.end/unlock.after", lease).is_none() {
        misses.push(format!(
            "{role}: release order: no end fence release after the lease"
        ));
    }
    for append in ["x3b.append.rev", "x3b.append.cln"] {
        let four = first(&format!("{append}.release-level-four"), level_three);
        let three = first(&format!("{append}.release-level-three"), level_three);
        match (four, three) {
            (None, None) => {}
            (Some(four), Some(three)) if four < three && three < lease => {}
            _ => misses.push(format!(
                "{role}: release order: {append}'s level 4 and level 3 are not released before the lease"
            )),
        }
    }
    misses
}

thread_local! {
    static CHILDREN: std::cell::RefCell<Vec<ChildRecord>> = const { std::cell::RefCell::new(Vec::new()) };
}

// =============================================================== the matrix

/// The limits of item 10, each with its reason and later owner.
fn limits() -> V {
    let rows = [
        (
            "L1",
            "Power loss, kernel panic and drive-cache loss: process death keeps unbarriered page-cache data, so F03 and F05 exercise only the survived branch.",
            "M6 qualification",
        ),
        (
            "L2",
            "SQLite's interior commit is atomic under process death by its own contract; the matrix kills at commit.before and .after and injects fail-*.",
            "SQLite (no VFS shim)",
        ),
        (
            "L3",
            "Native stalls and S6 scheduling bounds need real elapsed time or kernel control; a hold emulates a stalled step, not a stalled syscall.",
            "S6, M6",
        ),
        (
            "L4",
            "Whole-file state.v1 restore (X4T r9 item 7) is neither asserted refused nor admitted.",
            "S9.3 or a future anchor outside I",
        ),
        (
            "L5",
            "Store and carrier migration and restore (F35, F47, F48, F50, F51): no migration or restore writer exists in M2.",
            "the migration law",
        ),
        (
            "L6",
            "Orphan collection: no reachability GC exists; orphans are recorded in postState.",
            "a reachability GC law",
        ),
        (
            "L7",
            "Measured platform profile: this host is BASELINE-ATTESTED under 469; every run is synthetic.",
            "owner signing keys",
        ),
        (
            "L8",
            "Host coverage: macOS 27 on APFS on this host only.",
            "M6 qualification",
        ),
        (
            "L9",
            "Native optional delivery: M2 has no browser launch or export, so F17 runs only as an injected failure.",
            "CLI enablement",
        ),
        (
            "L10",
            "Journal pruning: no pruning writer exists, so F28 runs only over X6a's fixture.",
            "a pruning law",
        ),
        (
            "L11",
            "Permanently refused crash states: an interrupted first registration, a created owner not yet sampled private, and a partial ledger WAL leave the project refused until a repair or resume writer exists; F00 records each outcome.",
            "M3 (a repair or resume writer)",
        ),
    ];
    V::Array(
        rows.iter()
            .map(|(id, reason, owner)| {
                object([("id", s(id)), ("reason", s(reason)), ("owner", s(owner))])
            })
            .collect(),
    )
}

/// Whether a run's observation meets its required row.
fn verdict(row: &V, observed: &Observed) -> (Verdict, Vec<String>) {
    let mut misses = Vec::new();
    if let Some(V::Object(expected)) = member(row, "expected") {
        for (key, want) in expected {
            let got = observed
                .values
                .get(key)
                .map(String::as_str)
                .unwrap_or("absent");
            if !meets(want, got) {
                misses.push(format!("{key}: expected {want:?}, observed {got}"));
            }
        }
    }
    if observed
        .values
        .get("R1.stateUnchanged")
        .is_some_and(|v| v != "true")
    {
        misses.push("R1 changed the state".into());
    }
    (
        if misses.is_empty() {
            Verdict::Pass
        } else {
            Verdict::Fail
        },
        misses,
    )
}

/// `OPENSIP_X9_ROWS`, when set, limits a development run to these
/// `<case>-<variant>` prefixes; a run set for review runs every row.
#[allow(clippy::disallowed_methods, reason = "M3-B r5 item 9: an X9 crash-matrix seam, test-only")]
fn selected(row: &V) -> bool {
    let name = format!(
        "{}-{}",
        text(member(row, "case").unwrap()),
        text(member(row, "variant").unwrap())
    );
    match std::env::var("OPENSIP_X9_ROWS") {
        Ok(filter) => filter.split(',').any(|p| name.starts_with(p)),
        Err(_) => true,
    }
}

/// The run set (law X9 r1 item 7): every X9-5 row once, under
/// `target/opensip-x9/<runSetId>/` (`OPENSIP_X9_RUN_SET`), with X9 r11's
/// host census (each of its three runs twice, equal), the release-absence
/// result the lane produced (`OPENSIP_X9_RELEASE_ABSENCE`) and the limits.
/// Without `OPENSIP_X9_RUN_SET` this test does nothing.
#[test]
fn x9_5_matrix() {
    run_host_matrix("X9-5", required);
}

/// X9-6's host run set (law X9 r16): every row of host's reviewed
/// `required-runs.v1.json`, X9-5's and the `"X9-6"` rows, with X9-5's host
/// census, as `x9_5_matrix` runs X9-5's.
#[test]
fn x9_6_matrix() {
    run_host_matrix("X9-6", required_all);
}

/// One host run set: the host census, then every selected row of `rows`,
/// each run record, and `matrix.json`.
#[allow(clippy::disallowed_methods, reason = "M3-B r5 item 9: the X9 crash-matrix seams, test-only")]
fn run_host_matrix(unit: &str, rows: fn() -> (i64, Vec<V>)) {
    let Ok(run_set) = std::env::var("OPENSIP_X9_RUN_SET") else {
        return;
    };
    let _serial = SERIAL.lock().unwrap_or_else(|p| p.into_inner());
    let (epoch, rows) = rows();
    let out = repository().join("target/opensip-x9").join(&run_set);
    fs::create_dir_all(&out).unwrap();
    let (census, lines, traces) = host_census(epoch).unwrap_or_else(|e| panic!("census: {e:?}"));
    let (census_value, kill_set) = census_json(&census, &lines);
    for (which, records) in &traces {
        let name = match which {
            CensusRun::Lawful => "a",
            CensusRun::Exhausted => "b",
            CensusRun::StoreGc => "c",
        };
        let trace: String = records
            .iter()
            .map(|r| {
                format!(
                    "{}|{}|{}|{}|{}\n",
                    r.thread, r.sequence, r.point, r.event, r.payload
                )
            })
            .collect();
        fs::write(out.join(format!("census-trace-{name}.txt")), trace).unwrap();
    }
    if std::env::var("OPENSIP_X9_CENSUS_ONLY").is_ok() {
        fs::write(
            out.join("census.json"),
            canonical_bytes(&census_value).unwrap(),
        )
        .unwrap();
        return;
    }
    let product = product();
    let host = host();
    let mut pins: Vec<FilePin> = Vec::new();
    let mut failures = Vec::new();
    for row in rows.iter().filter(|r| selected(r)) {
        let case = text(member(row, "case").unwrap()).to_owned();
        let variant = text(member(row, "variant").unwrap()).to_owned();
        let V::Array(script) = member(row, "script").unwrap().clone() else {
            panic!("script")
        };
        RELEASE_ORDER.with(|r| r.borrow_mut().clear());
        let (verdict, misses, observed) = match execute(row, epoch) {
            Ok(observed) => {
                let (verdict, mut misses) = verdict(row, &observed);
                // Law X9 r16 (item 8): a commit child out of the guard
                // order fails the run, as R1's `stateUnchanged` does.
                let order = RELEASE_ORDER.with(|r| std::mem::take(&mut *r.borrow_mut()));
                if order.is_empty() {
                    (verdict, misses, Some(observed))
                } else {
                    misses.extend(order);
                    (Verdict::Fail, misses, Some(observed))
                }
            }
            Err(Harness(reason)) => (Verdict::HarnessError, vec![reason], None),
        };
        let children = CHILDREN.with(|c| std::mem::take(&mut *c.borrow_mut()));
        let empty = PostState {
            raw: Vec::new(),
            logical: V::Object(BTreeMap::new()),
            normalized_sha256: digest_hex(&raw_sha256(b"")),
        };
        let record = RunRecord {
            case: case.clone(),
            variant: variant.clone(),
            units: strings(member(row, "units").unwrap()),
            labels: strings(member(row, "labels").unwrap()),
            product: product.clone(),
            host: host.clone(),
            clock_epoch: epoch,
            script: V::Array(script),
            children,
            post_state: observed.as_ref().map_or(empty, |o| o.post.clone()),
            ladder: V::Array(
                observed
                    .as_ref()
                    .map_or_else(Vec::new, |o| o.ladder.clone()),
            ),
            expected: member(row, "expected").unwrap().clone(),
            verdict,
            ladder_end: None,
            timing_guard_ms: observed.as_ref().and_then(|o| o.timing_guard_ms),
            not_applicable: observed.as_ref().and_then(|o| o.not_applicable.clone()),
        };
        let pin = write_run(&out, &record).unwrap_or_else(|e| panic!("{e}"));
        let observed_values = observed
            .as_ref()
            .map(|o| format!("{:?}", o.values))
            .unwrap_or_default();
        eprintln!("{unit} {case}-{variant}: {verdict:?} {misses:?} {observed_values}");
        if verdict != Verdict::Pass {
            failures.push(format!("{case}-{variant}: {verdict:?} {misses:?}"));
        }
        pins.push(pin);
    }
    pins.sort_by(|a, b| a.path.cmp(&b.path));
    let release = std::env::var("OPENSIP_X9_RELEASE_ABSENCE")
        .ok()
        .map(|path| parse_json(&fs::read(path).expect("release absence")).expect("JSON"))
        .unwrap_or(V::Null);
    let matrix = object([
        ("schema", s("opensip.x9.matrix.v1")),
        (
            "product",
            object([
                ("commit", s(&product.commit)),
                ("worktreeClean", V::Bool(product.worktree_clean)),
            ]),
        ),
        (
            "runs",
            V::Array(
                pins.iter()
                    .map(|p| {
                        object([
                            ("path", s(&p.path)),
                            (
                                "bytes",
                                V::Integer(
                                    opensip_identity::JsonInteger::new(i128::from(p.bytes))
                                        .unwrap(),
                                ),
                            ),
                            ("sha256", s(&p.sha256)),
                        ])
                    })
                    .collect(),
            ),
        ),
        ("census", census_value),
        ("killSet", kill_set),
        ("releaseAbsence", release),
        ("limits", limits()),
    ]);
    fs::write(out.join("matrix.json"), canonical_bytes(&matrix).unwrap()).unwrap();
    assert!(
        failures.is_empty(),
        "{unit} runs not PASS:\n{}",
        failures.join("\n")
    );
}

// ============================================================ lane tests

/// Law X9 r10: a runner makes its process's one entry. In a fresh child, a
/// first `finalize_commit` over a missing candidate file ends on the host
/// I/O row before any entry; a second `finalize_commit` and a `store_gc`
/// then each refuse on the invariant row without effect.
#[test]
fn a_process_makes_at_most_one_runner_call() {
    let _serial = SERIAL.lock().unwrap_or_else(|p| p.into_inner());
    let (epoch, _) = required();
    let mut run = Run::new(epoch);
    run.fixture().unwrap();
    let missing = run.scratch.join("no-candidate.json");
    let exit = run
        .finished("entries", "", &format!("missing={}\n", missing.display()))
        .unwrap();
    let tail = "delivered=0;optional=ok;end=-;endStep=-;rollover=-";
    assert_eq!(
        exit.outcome(),
        Some(
            format!(
                "first=kind=terminated;row=HOST.IO_FAILURE/-;exit=4;subject=-;runId=no;remedy=-;namespace=no;requested=no;{tail};\
                 again=kind=terminated;row=SYSTEM.OUTCOME.ILLEGAL_STATE/HOST.INVARIANT_VIOLATED;exit=4;subject=-;runId=no;remedy=-;namespace=no;requested=no;{tail};\
                 gc=;ended=SYSTEM.OUTCOME.ILLEGAL_STATE/HOST.INVARIANT_VIOLATED"
            )
            .as_str()
        )
    );
    // Nothing was registered: no runner call reached an entry.
    assert!(run.paths().namespace().is_none());
}

/// Law X9 r11 item 5: each of the host census's three runs, twice, is equal
/// point for point; (b) reaches the rollover and (c) the sweep's settle.
#[test]
fn the_host_census_runs_are_equal_across_two_runs() {
    let _serial = SERIAL.lock().unwrap_or_else(|p| p.into_inner());
    let (epoch, _) = required();
    let (census, _, _) = host_census(epoch).unwrap();
    for name in [
        "x3c.attempt.commit.after",
        "x7.delivery.required.before",
        "x3b.rollover",
        "x6.sweep.settle.commit.before",
    ] {
        assert!(
            census.points.iter().any(|p| p.name.starts_with(name)),
            "{name}"
        );
    }
}

#[test]
fn rev_reason_diff_preserves_multiplicity_across_carrier_renames() {
    fn snapshot(path: &str, bodies: &[&str]) -> V {
        let rows = bodies.iter().map(|body| {
            let mut cells = vec![V::Null; 12];
            cells[3] = s("REV"); cells[11] = s(body);
            V::Array(cells)
        }).collect();
        object([("databases", object([(path, object([("tables", object([("grant_journal_v3", V::Array(rows))]))]))]))])
    }
    let old = r#"{"reason":"stale-guard"}"#;
    let new = r#"{"reason":"operator"}"#;
    let before = snapshot("old/grant-journal.sqlite", &[old, old]);
    let after = snapshot("renamed/grant-journal.sqlite", &[old, old, new, old]);
    assert_eq!(added_rev_reasons(&before, &after).unwrap(), "operator,stale-guard");
    assert_eq!(added_rev_reasons(&before, &snapshot("renamed/grant-journal.sqlite", &[old, old])).unwrap(), "");
    for bad in ["invalid", r#"{}"#, r#"{"reason":null}"#] {
        assert!(added_rev_reasons(&before, &snapshot("new/grant-journal.sqlite", &[bad])).is_err());
    }
}
