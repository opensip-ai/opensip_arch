//! Law X9 r1 items 5 and 12 (unit X9-1): the census of the integrated path
//! on security's side, and verified kills at its points. Compiled only in
//! security's own test build with the test-only `crash-matrix` feature.
//!
//! Every process of a run is a matrix child (this test binary re-executed by
//! X9-0's driver) under law X9 r2 item 3's scripted wall clock, numbered in
//! spawn order: the `fixture` child (ordinal 0) publishes the synthetic
//! installation, X4T-0's accepted store and a project root; the next child
//! drives the integrated write path in a fresh process:
//! 1. a first operation: X1's writer, X2b's root admission, X2c's first
//!    registration, X2d's namespace and lease, X3b's floor step (INIT floor),
//!    X3b-3's carrier creation and start, then X2e's handoff; one `SEAL`;
//!    the end path (the fence retaken, the floor copied);
//! 2. a second operation on the registered root: a `SEAL`, then the end
//!    path's `REV` and `CLN`, then the end path;
//! 3. an exhausted generation (X3b-2's reserved-slot technique) and a third
//!    operation whose end path runs X3b-4's rollover, then the copy;
//! 4. an `EXCLUSIVE` operation (both lease carriers) with no record;
//! 5. the shared fenced `state.v1` publisher (X4T-b's publication protocol
//!    under the write gate's fence).
//!
//! Traced with nothing armed, that child's records are the census (item 5);
//! two census runs on one product agree point for point (X9 r2). The parent
//! takes no wall reading.
//! No durability primitive may be reached outside a scope: the child would
//! report a harness error. Nothing here sleeps, polls or waits on a timer;
//! every synchronization is X9-0's blocking record read.
use crate::custody::installation_read_fixture::{InstallationAt, ReadFixture};
use crate::custody::namespace_lease::{NamespaceSubject, WriterLease};
use crate::custody::operation_handoff::{JournalOutcome, OperationEnd, ProjectOperation};
use crate::custody::ordinary_writer::OrdinaryWriteAdmission;
use crate::journal_store::{AppendError, CapacityExhaustion, RecordDraft};
use opensip_platform::crash_barrier::driver::{
    Census, ChildSpec, Exit, MatrixChild, ScriptedClock,
};
use opensip_platform::crash_barrier::{child_role, report_outcome};
use std::collections::BTreeSet;
use std::fs;
use std::os::unix::fs::PermissionsExt;
use std::path::{Path, PathBuf};

const ENTRY: &str = "crash_matrix_census::matrix_child";
const OP: &str = "op-0123456789abcdef0123456789abcdef";
const RELEASED: &str = "op-dddddddddddddddddddddddddddddddd";
/// X3b r10 item 5a: no `SEAL` fits after 9007199254740987.
const EXHAUSTED: i64 = 9_007_199_254_740_990;

fn run_id() -> String {
    format!("run3:{}", "5".repeat(64))
}
fn field(input: &str, key: &str) -> String {
    input
        .lines()
        .find_map(|line| line.strip_prefix(&format!("{key}=")))
        .unwrap_or_default()
        .to_owned()
}
fn project_inputs() -> crate::custody::first_registration::ProjectInputs<'static> {
    static NO_GROUPS: BTreeSet<u32> = BTreeSet::new();
    crate::custody::first_registration::ProjectInputs {
        trust_groups: &NO_GROUPS,
        environment: &[],
        system_sources: &[],
    }
}

/// The writer's subject for `project`: a first registration, or the
/// registered root's admission.
fn subject(
    writer: &mut OrdinaryWriteAdmission,
    project: &Path,
    first: bool,
) -> Result<NamespaceSubject, String> {
    let inputs = project_inputs();
    let admission = writer
        .admit_project_root(project, None, inputs.trust_groups)
        .map_err(|e| format!("admission: {e:?}"))?;
    let tracking = writer
        .observe_project_tracking_with(&admission, &inputs)
        .map_err(|e| format!("tracking: {e:?}"))?;
    if !first {
        return Ok(NamespaceSubject::Eligible {
            admission,
            tracking,
        });
    }
    let registered = writer
        .register_first_use_with(
            admission,
            tracking,
            &inputs,
            &crate::custody::first_registration::Seam::live(),
        )
        .map_err(|e| format!("registration: {e:?}"))?;
    Ok(NamespaceSubject::Registered(registered))
}

/// One operation through X2e's handoff on a fresh writer.
fn operation(at: &InstallationAt, project: &Path, first: bool) -> Result<ProjectOperation, String> {
    operation_with(at, project, first, WriterLease::AppendWrite)
}
fn operation_with(
    at: &InstallationAt,
    project: &Path,
    first: bool,
    lease: WriterLease,
) -> Result<ProjectOperation, String> {
    let (mut writer, _trees) = at.writer()?;
    let subject = subject(&mut writer, project, first)?;
    let invocation = crate::trust::TrustInvocation::new(
        "req1_0123456789abcdef0123456789abcdef",
        "exec1_0123456789abcdef0123456789abcdef",
        0,
    )
    .ok_or("invocation")?;
    writer
        .begin_operation(subject, lease, &project_inputs(), &invocation)
        .map_err(|e| format!("handoff: {:?}", e.row()))
}

/// One record through the operation's carrier, in the append scope its
/// composition owner enters (`x3b.append.<kind>`), as X3d will.
fn append(operation: &mut ProjectOperation, draft: Option<RecordDraft>) -> Result<String, String> {
    let kind = match &draft {
        None => "seal",
        Some(RecordDraft::Rev { .. }) => "rev",
        Some(RecordDraft::Cln { .. }) => "cln",
        Some(RecordDraft::Ra { .. }) => "ra",
    };
    let appended = operation.journal(|location, carrier, _checkpoint, work| {
        opensip_platform::crash_scope!(
            match kind {
                "seal" => "x3b.append.seal",
                "rev" => "x3b.append.rev",
                _ => "x3b.append.cln",
            },
            {
                let mut held = carrier.lock().begin(location, work)?.acquire()?;
                let appended = match &draft {
                    None => held.append_seal(OP, &run_id(), work),
                    Some(draft) => {
                        let result = held.append(OP, draft, work);
                        return Ok(result);
                    }
                };
                drop(held);
                Ok(appended)
            }
        )
    });
    // Any failure ends the workload: an undetermined append is X3d's
    // uncertain outcome, after which the composition runs nothing more.
    match appended {
        Ok(Ok(record)) => Ok(format!("{kind}:{}", record.seq())),
        Ok(Err(AppendError::Refused(f))) => Err(format!("{kind}:refused:{f:?}")),
        Ok(Err(AppendError::Undetermined(f))) => Err(format!("{kind}:undetermined:{f:?}")),
        Err(f) => Err(format!("{kind}:{f:?}")),
    }
}

fn ended(end: OperationEnd) -> String {
    match end {
        OperationEnd::Ended(outcome) => format!("ended:{outcome:?}"),
        OperationEnd::RolledOver { rollover, end } => {
            format!("rolled:{rollover:?}:{:?}", end.map_err(|e| e.row()))
        }
        OperationEnd::NotEntered => "not-entered".to_owned(),
        OperationEnd::Failed(failure) => format!("failed:{:?}", failure.row()),
    }
}

/// The census workload: the integrated path, steps 1 to 4 of the module
/// comment. Every step's outcome is reported; the first refusal ends it.
fn integrated(at: &InstallationAt, project: &Path) -> Result<String, String> {
    let mut out = Vec::new();
    // 1. First use: registration, INIT, creation, one SEAL, the end path.
    let mut first = operation(at, project, true)?;
    let namespace = first.binding().namespace_id().to_owned();
    out.push(format!("a.start={:?}", first.carrier().reconciliation()));
    out.push(append(&mut first, None)?);
    out.push(ended(first.end(JournalOutcome::Certain)));
    // 2. The registered root: SEAL, then the end path's REV and CLN.
    let mut second = operation(at, project, false)?;
    out.push(format!("b.start={:?}", second.carrier().reconciliation()));
    out.push(append(&mut second, None)?);
    let epoch = crate::trust::metadata::parse(br#"{"revocationVersion":1}"#)
        .map_err(|e| format!("{e:?}"))?;
    out.push(append(
        &mut second,
        Some(RecordDraft::Rev {
            reason: "observer-fail-stop".into(),
            trust_epoch_observed: Some(epoch),
        }),
    )?);
    out.push(append(
        &mut second,
        Some(RecordDraft::Cln {
            residuals: vec!["seal-without-commit".into()],
        }),
    )?);
    out.push(ended(second.end(JournalOutcome::Certain)));
    // 3. An exhausted generation, then the rollover in the end path.
    let namespace_path = at.installation.join("host/projects").join(&namespace);
    crate::journal_store::plant_committed_tail_for_tests(&namespace_path, &namespace, EXHAUSTED);
    let third = operation(at, project, false)?;
    out.push(format!("c.start={:?}", third.carrier().start_tail().1));
    out.push(ended(third.end(JournalOutcome::Exhausted {
        exhaustion: CapacityExhaustion::new(1, EXHAUSTED),
        operation_ref: RELEASED.into(),
    })));
    // 4. An EXCLUSIVE operation (both lease carriers), with no record.
    let fourth = operation_with(at, project, false, WriterLease::Exclusive)?;
    out.push(format!("d.start={:?}", fourth.carrier().start_tail()));
    out.push(ended(fourth.end(JournalOutcome::Certain)));
    // 5. The shared fenced publisher.
    let (before, after) = at.publish_accepted_trust_fenced(Vec::new(), 2)?;
    out.push(format!("trust={before}->{after}"));
    Ok(out.join(";"))
}

/// The `fixture` child (law X9 r2 item 3, ordinal 0): a synthetic
/// installation under this process's `TMPDIR` (the run's scratch parent),
/// X4T-0's accepted store at revocation version 1, and a project root under
/// H (0755, no ACL, as on a stock Mac). The paths are written to `out`; the
/// tree outlives this process, and the parent removes it.
fn fixture(out: &Path) -> Result<String, String> {
    let fixture = ReadFixture::new("x91");
    let at = fixture.at();
    at.install_accepted_trust(Vec::new(), 1, None)?;
    let code = fixture.home.join("code");
    let project = code.join("project");
    for dir in [&code, &project] {
        fs::create_dir(dir).map_err(|e| format!("{e}"))?;
        fs::set_permissions(dir, fs::Permissions::from_mode(0o755)).map_err(|e| format!("{e}"))?;
    }
    fs::write(
        out,
        format!(
            "home={}\ninstallation={}\nstore={}\nproject={}\n",
            fixture.home.display(),
            fixture.installation.display(),
            fixture.store,
            project.display()
        ),
    )
    .map_err(|e| format!("{e}"))?;
    std::mem::forget(fixture);
    Ok("fixture".into())
}

/// A later writer on the registered root: its start's reconciliation, then
/// the end path.
fn next_writer(at: &InstallationAt, project: &Path) -> Result<String, String> {
    let next = operation(at, project, false)?;
    let reconciliation = format!("{:?}", next.carrier().reconciliation());
    Ok(format!(
        "next={reconciliation};{}",
        ended(next.end(JournalOutcome::Certain))
    ))
}

/// The matrix child entry. In the parent's own run it returns at once.
#[test]
fn matrix_child() {
    let Some((role, input)) = child_role() else {
        return;
    };
    let input = fs::read_to_string(input).unwrap();
    let at = InstallationAt {
        home: PathBuf::from(field(&input, "home")),
        installation: PathBuf::from(field(&input, "installation")),
        store: field(&input, "store"),
    };
    let project = PathBuf::from(field(&input, "project"));
    let outcome = match role.as_str() {
        "fixture" => fixture(Path::new(&field(&input, "out"))),
        "integrated" => integrated(&at, &project),
        "next" => next_writer(&at, &project),
        "publish" => at
            .publish_accepted_trust_fenced(Vec::new(), field(&input, "version").parse().unwrap())
            .map(|(before, after)| format!("trust={before}->{after}")),
        other => panic!("unknown matrix child role {other}"),
    }
    .unwrap_or_else(|e| format!("refused:{e}"));
    report_outcome(&outcome);
    println!("\nOUTCOME {outcome}");
}

/// The run set's clock epoch (law X9 r2 item 3): 2026-10-03T00:00:00Z, a
/// whole second after X4T-0's evaluation floor (2026-10-02) and inside every
/// validity window of the synthetic fixture.
pub(crate) const CLOCK_EPOCH: i64 = 1_791_072_000;

/// One run: a private scratch parent (every child's `TMPDIR`), the fixture
/// its `fixture` child published at ordinal 0, and the next ordinal.
struct Setup {
    fixture: InstallationAt,
    input: PathBuf,
    parent: PathBuf,
    ordinal: std::cell::Cell<u32>,
}
impl Drop for Setup {
    fn drop(&mut self) {
        // The fixture's zero-rights owner entries and private modes, as the
        // shared fixture's own scratch removes them.
        let _ = std::process::Command::new("/bin/chmod")
            .args(["-R", "-N"])
            .arg(&self.parent)
            .stderr(std::process::Stdio::null())
            .status();
        let _ = std::process::Command::new("/bin/chmod")
            .args(["-R", "u+rwX"])
            .arg(&self.parent)
            .stderr(std::process::Stdio::null())
            .status();
        let _ = fs::remove_dir_all(&self.parent);
    }
}
impl Setup {
    fn new() -> Self {
        let nonce: String = opensip_platform::request_entropy()
            .unwrap()
            .iter()
            .map(|b| format!("{b:02x}"))
            .collect();
        let parent = std::env::temp_dir().join(format!("opensip-x91-{nonce}"));
        fs::create_dir(&parent).unwrap();
        fs::set_permissions(&parent, fs::Permissions::from_mode(0o700)).unwrap();
        let parent = fs::canonicalize(parent).unwrap();
        let out = parent.join("fixture.out");
        let fixture_input = parent.join("fixture.in");
        fs::write(&fixture_input, format!("out={}\n", out.display())).unwrap();
        let exit = MatrixChild::spawn(&ChildSpec {
            entry: ENTRY,
            role: "fixture",
            input: &fixture_input,
            arms: None,
            clock: Some(ScriptedClock {
                epoch: CLOCK_EPOCH,
                ordinal: 0,
            }),
            scratch_parent: &parent,
        })
        .unwrap()
        .finish()
        .unwrap();
        exit.verify_finished()
            .unwrap_or_else(|e| panic!("fixture child: {e:?}\n{}", exit.stdout));
        let written = fs::read_to_string(&out).unwrap();
        let fixture = InstallationAt {
            home: PathBuf::from(field(&written, "home")),
            installation: PathBuf::from(field(&written, "installation")),
            store: field(&written, "store"),
        };
        let input = parent.join("x9-input");
        fs::write(&input, &written).unwrap();
        Self {
            fixture,
            input,
            parent,
            ordinal: std::cell::Cell::new(1),
        }
    }
    /// The next child of this run, at the next ordinal.
    fn child(&self, role: &str, input: &Path, arms: Option<&str>) -> MatrixChild {
        let ordinal = self.ordinal.get();
        self.ordinal.set(ordinal + 1);
        MatrixChild::spawn(&ChildSpec {
            entry: ENTRY,
            role,
            input,
            arms,
            clock: Some(ScriptedClock {
                epoch: CLOCK_EPOCH,
                ordinal,
            }),
            scratch_parent: &self.parent,
        })
        .unwrap()
    }
    fn spawn(&self, arms: Option<&str>) -> MatrixChild {
        self.child("integrated", &self.input, arms)
    }
}

/// The expected outcome of the census workload.
const OUTCOME: &str = "a.start=Consistent;seal:1;ended:CopiedForward;\
b.start=Consistent;seal:2;rev:3;cln:4;ended:CopiedForward;\
c.start=9007199254740990;\
rolled:Rolled { closed: (1, 9007199254740991), opened: 2 }:Ok(CopiedForward);\
d.start=(2, 0, None);ended:Unchanged;trust=1->2";

/// The census of security's integrated path (law X9 r1 item 5, r2): every
/// point the unarmed workload reaches under the scripted clock, with its
/// occurrences and whether it is a durability point, sorted by name. A
/// product change that removes a point, or adds an unscoped or unlisted
/// one, fails this pin.
pub(crate) const CENSUS: &[(&str, u32, bool)] = &[
    ("x2.fence.end/lock.after", 4, true),
    ("x2.fence.end/lock.before", 4, true),
    ("x2.fence.end/unlock.after", 4, true),
    ("x2.fence.end/unlock.before", 4, true),
    ("x2.fence.gate/directory-barrier.after", 10, true),
    ("x2.fence.gate/directory-barrier.before", 10, true),
    ("x2.fence.gate/lock.after", 5, true),
    ("x2.fence.gate/lock.before", 5, true),
    ("x2.fence.register.active/create.after", 1, true),
    ("x2.fence.register.active/create.before", 1, true),
    ("x2.fence.register.active/directory-barrier.after", 1, true),
    ("x2.fence.register.active/directory-barrier.before", 1, true),
    ("x2.fence.register.active/file-barrier.after", 1, true),
    ("x2.fence.register.active/file-barrier.before", 1, true),
    ("x2.fence.register.active/rename.after", 1, true),
    ("x2.fence.register.active/rename.before", 1, true),
    ("x2.fence.register.active/write.after", 1, true),
    ("x2.fence.register.active/write.before", 1, true),
    ("x2.fence.register.marker-directory/create.after", 1, true),
    ("x2.fence.register.marker-directory/create.before", 1, true),
    (
        "x2.fence.register.marker-directory/directory-barrier.after",
        2,
        true,
    ),
    (
        "x2.fence.register.marker-directory/directory-barrier.before",
        2,
        true,
    ),
    ("x2.fence.register.marker/create.after", 1, true),
    ("x2.fence.register.marker/create.before", 1, true),
    ("x2.fence.register.marker/directory-barrier.after", 1, true),
    ("x2.fence.register.marker/directory-barrier.before", 1, true),
    ("x2.fence.register.marker/file-barrier.after", 1, true),
    ("x2.fence.register.marker/file-barrier.before", 1, true),
    ("x2.fence.register.marker/write.after", 1, true),
    ("x2.fence.register.marker/write.before", 1, true),
    ("x2.fence.register.namespace/create.after", 4, true),
    ("x2.fence.register.namespace/create.before", 4, true),
    (
        "x2.fence.register.namespace/directory-barrier.after",
        6,
        true,
    ),
    (
        "x2.fence.register.namespace/directory-barrier.before",
        6,
        true,
    ),
    ("x2.fence.register.namespace/file-barrier.after", 2, true),
    ("x2.fence.register.namespace/file-barrier.before", 2, true),
    ("x2.fence.register.namespace/link.after", 1, true),
    ("x2.fence.register.namespace/link.before", 1, true),
    ("x2.fence.register.namespace/write.after", 2, true),
    ("x2.fence.register.namespace/write.before", 2, true),
    ("x2.fence.register.reserved/create.after", 1, true),
    ("x2.fence.register.reserved/create.before", 1, true),
    (
        "x2.fence.register.reserved/directory-barrier.after",
        1,
        true,
    ),
    (
        "x2.fence.register.reserved/directory-barrier.before",
        1,
        true,
    ),
    ("x2.fence.register.reserved/file-barrier.after", 1, true),
    ("x2.fence.register.reserved/file-barrier.before", 1, true),
    ("x2.fence.register.reserved/rename.after", 1, true),
    ("x2.fence.register.reserved/rename.before", 1, true),
    ("x2.fence.register.reserved/write.after", 1, true),
    ("x2.fence.register.reserved/write.before", 1, true),
    ("x2.fence.release/unlock.after", 5, true),
    ("x2.fence.release/unlock.before", 5, true),
    ("x2.lease.readers/lock.after", 1, true),
    ("x2.lease.readers/lock.before", 1, true),
    ("x2.lease.readers/unlock.after", 1, true),
    ("x2.lease.readers/unlock.before", 1, true),
    ("x2.lease.writer/lock.after", 4, true),
    ("x2.lease.writer/lock.before", 4, true),
    ("x2.lease.writer/unlock.after", 4, true),
    ("x2.lease.writer/unlock.before", 4, true),
    ("x3b.append.cln.begin", 1, true),
    ("x3b.append.cln.built", 1, true),
    ("x3b.append.cln.commit.after", 1, true),
    ("x3b.append.cln.commit.before", 1, true),
    ("x3b.append.cln.insert.after", 1, true),
    ("x3b.append.cln.insert.before", 1, true),
    ("x3b.append.cln.level-four", 1, true),
    ("x3b.append.cln.release-level-four", 1, true),
    ("x3b.append.cln.release-level-three", 1, true),
    ("x3b.append.cln.witness-committed/create.after", 1, true),
    ("x3b.append.cln.witness-committed/create.before", 1, true),
    (
        "x3b.append.cln.witness-committed/directory-barrier.after",
        1,
        true,
    ),
    (
        "x3b.append.cln.witness-committed/directory-barrier.before",
        1,
        true,
    ),
    (
        "x3b.append.cln.witness-committed/file-barrier.after",
        1,
        true,
    ),
    (
        "x3b.append.cln.witness-committed/file-barrier.before",
        1,
        true,
    ),
    ("x3b.append.cln.witness-committed/rename.after", 1, true),
    ("x3b.append.cln.witness-committed/rename.before", 1, true),
    ("x3b.append.cln.witness-committed/write.after", 1, true),
    ("x3b.append.cln.witness-committed/write.before", 1, true),
    ("x3b.append.cln.witness-pending/create.after", 1, true),
    ("x3b.append.cln.witness-pending/create.before", 1, true),
    (
        "x3b.append.cln.witness-pending/directory-barrier.after",
        1,
        true,
    ),
    (
        "x3b.append.cln.witness-pending/directory-barrier.before",
        1,
        true,
    ),
    ("x3b.append.cln.witness-pending/file-barrier.after", 1, true),
    (
        "x3b.append.cln.witness-pending/file-barrier.before",
        1,
        true,
    ),
    ("x3b.append.cln.witness-pending/rename.after", 1, true),
    ("x3b.append.cln.witness-pending/rename.before", 1, true),
    ("x3b.append.cln.witness-pending/write.after", 1, true),
    ("x3b.append.cln.witness-pending/write.before", 1, true),
    ("x3b.append.rev.begin", 1, true),
    ("x3b.append.rev.built", 1, true),
    ("x3b.append.rev.commit.after", 1, true),
    ("x3b.append.rev.commit.before", 1, true),
    ("x3b.append.rev.insert.after", 1, true),
    ("x3b.append.rev.insert.before", 1, true),
    ("x3b.append.rev.level-four", 1, true),
    ("x3b.append.rev.release-level-four", 1, true),
    ("x3b.append.rev.release-level-three", 1, true),
    ("x3b.append.rev.witness-committed/create.after", 1, true),
    ("x3b.append.rev.witness-committed/create.before", 1, true),
    (
        "x3b.append.rev.witness-committed/directory-barrier.after",
        1,
        true,
    ),
    (
        "x3b.append.rev.witness-committed/directory-barrier.before",
        1,
        true,
    ),
    (
        "x3b.append.rev.witness-committed/file-barrier.after",
        1,
        true,
    ),
    (
        "x3b.append.rev.witness-committed/file-barrier.before",
        1,
        true,
    ),
    ("x3b.append.rev.witness-committed/rename.after", 1, true),
    ("x3b.append.rev.witness-committed/rename.before", 1, true),
    ("x3b.append.rev.witness-committed/write.after", 1, true),
    ("x3b.append.rev.witness-committed/write.before", 1, true),
    ("x3b.append.rev.witness-pending/create.after", 1, true),
    ("x3b.append.rev.witness-pending/create.before", 1, true),
    (
        "x3b.append.rev.witness-pending/directory-barrier.after",
        1,
        true,
    ),
    (
        "x3b.append.rev.witness-pending/directory-barrier.before",
        1,
        true,
    ),
    ("x3b.append.rev.witness-pending/file-barrier.after", 1, true),
    (
        "x3b.append.rev.witness-pending/file-barrier.before",
        1,
        true,
    ),
    ("x3b.append.rev.witness-pending/rename.after", 1, true),
    ("x3b.append.rev.witness-pending/rename.before", 1, true),
    ("x3b.append.rev.witness-pending/write.after", 1, true),
    ("x3b.append.rev.witness-pending/write.before", 1, true),
    ("x3b.append.seal.begin", 2, true),
    ("x3b.append.seal.built", 2, true),
    ("x3b.append.seal.commit.after", 2, true),
    ("x3b.append.seal.commit.before", 2, true),
    ("x3b.append.seal.insert.after", 2, true),
    ("x3b.append.seal.insert.before", 2, true),
    ("x3b.append.seal.level-four", 2, true),
    ("x3b.append.seal.release-level-four", 2, true),
    ("x3b.append.seal.release-level-three", 2, true),
    ("x3b.append.seal.witness-committed/create.after", 2, true),
    ("x3b.append.seal.witness-committed/create.before", 2, true),
    (
        "x3b.append.seal.witness-committed/directory-barrier.after",
        2,
        true,
    ),
    (
        "x3b.append.seal.witness-committed/directory-barrier.before",
        2,
        true,
    ),
    (
        "x3b.append.seal.witness-committed/file-barrier.after",
        2,
        true,
    ),
    (
        "x3b.append.seal.witness-committed/file-barrier.before",
        2,
        true,
    ),
    ("x3b.append.seal.witness-committed/rename.after", 2, true),
    ("x3b.append.seal.witness-committed/rename.before", 2, true),
    ("x3b.append.seal.witness-committed/write.after", 2, true),
    ("x3b.append.seal.witness-committed/write.before", 2, true),
    ("x3b.append.seal.witness-pending/create.after", 2, true),
    ("x3b.append.seal.witness-pending/create.before", 2, true),
    (
        "x3b.append.seal.witness-pending/directory-barrier.after",
        2,
        true,
    ),
    (
        "x3b.append.seal.witness-pending/directory-barrier.before",
        2,
        true,
    ),
    (
        "x3b.append.seal.witness-pending/file-barrier.after",
        2,
        true,
    ),
    (
        "x3b.append.seal.witness-pending/file-barrier.before",
        2,
        true,
    ),
    ("x3b.append.seal.witness-pending/rename.after", 2, true),
    ("x3b.append.seal.witness-pending/rename.before", 2, true),
    ("x3b.append.seal.witness-pending/write.after", 2, true),
    ("x3b.append.seal.witness-pending/write.before", 2, true),
    ("x3b.append.terminal.begin", 1, true),
    ("x3b.append.terminal.built", 1, true),
    ("x3b.append.terminal.commit.after", 1, true),
    ("x3b.append.terminal.commit.before", 1, true),
    ("x3b.append.terminal.insert.after", 1, true),
    ("x3b.append.terminal.insert.before", 1, true),
    ("x3b.append.terminal.level-four", 1, true),
    ("x3b.append.terminal.release-level-four", 1, true),
    ("x3b.append.terminal.release-level-three", 1, true),
    (
        "x3b.append.terminal.witness-committed/create.after",
        1,
        true,
    ),
    (
        "x3b.append.terminal.witness-committed/create.before",
        1,
        true,
    ),
    (
        "x3b.append.terminal.witness-committed/directory-barrier.after",
        1,
        true,
    ),
    (
        "x3b.append.terminal.witness-committed/directory-barrier.before",
        1,
        true,
    ),
    (
        "x3b.append.terminal.witness-committed/file-barrier.after",
        1,
        true,
    ),
    (
        "x3b.append.terminal.witness-committed/file-barrier.before",
        1,
        true,
    ),
    (
        "x3b.append.terminal.witness-committed/rename.after",
        1,
        true,
    ),
    (
        "x3b.append.terminal.witness-committed/rename.before",
        1,
        true,
    ),
    ("x3b.append.terminal.witness-committed/write.after", 1, true),
    (
        "x3b.append.terminal.witness-committed/write.before",
        1,
        true,
    ),
    ("x3b.append.terminal.witness-pending/create.after", 1, true),
    ("x3b.append.terminal.witness-pending/create.before", 1, true),
    (
        "x3b.append.terminal.witness-pending/directory-barrier.after",
        1,
        true,
    ),
    (
        "x3b.append.terminal.witness-pending/directory-barrier.before",
        1,
        true,
    ),
    (
        "x3b.append.terminal.witness-pending/file-barrier.after",
        1,
        true,
    ),
    (
        "x3b.append.terminal.witness-pending/file-barrier.before",
        1,
        true,
    ),
    ("x3b.append.terminal.witness-pending/rename.after", 1, true),
    ("x3b.append.terminal.witness-pending/rename.before", 1, true),
    ("x3b.append.terminal.witness-pending/write.after", 1, true),
    ("x3b.append.terminal.witness-pending/write.before", 1, true),
    ("x3b.end.floor.probe/lock.after", 4, true),
    ("x3b.end.floor.probe/lock.before", 4, true),
    ("x3b.end.floor.probe/unlock.after", 4, true),
    ("x3b.end.floor.probe/unlock.before", 4, true),
    ("x3b.end.floor.write/create.after", 3, true),
    ("x3b.end.floor.write/create.before", 3, true),
    ("x3b.end.floor.write/directory-barrier.after", 3, true),
    ("x3b.end.floor.write/directory-barrier.before", 3, true),
    ("x3b.end.floor.write/file-barrier.after", 3, true),
    ("x3b.end.floor.write/file-barrier.before", 3, true),
    ("x3b.end.floor.write/rename.after", 3, true),
    ("x3b.end.floor.write/rename.before", 3, true),
    ("x3b.end.floor.write/write.after", 3, true),
    ("x3b.end.floor.write/write.before", 3, true),
    ("x3b.floor.directory/create.after", 1, true),
    ("x3b.floor.directory/create.before", 1, true),
    ("x3b.floor.directory/directory-barrier.after", 2, true),
    ("x3b.floor.directory/directory-barrier.before", 2, true),
    ("x3b.floor.probe/lock.after", 4, true),
    ("x3b.floor.probe/lock.before", 4, true),
    ("x3b.floor.probe/unlock.after", 4, true),
    ("x3b.floor.probe/unlock.before", 4, true),
    ("x3b.floor.write/create.after", 2, true),
    ("x3b.floor.write/create.before", 2, true),
    ("x3b.floor.write/directory-barrier.after", 2, true),
    ("x3b.floor.write/directory-barrier.before", 2, true),
    ("x3b.floor.write/file-barrier.after", 2, true),
    ("x3b.floor.write/file-barrier.before", 2, true),
    ("x3b.floor.write/rename.after", 2, true),
    ("x3b.floor.write/rename.before", 2, true),
    ("x3b.floor.write/write.after", 2, true),
    ("x3b.floor.write/write.before", 2, true),
    ("x3b.init.ddl.commit.after", 1, true),
    ("x3b.init.ddl.commit.before", 1, true),
    ("x3b.init.file-barrier.after", 1, true),
    ("x3b.init.file-barrier.before", 1, true),
    ("x3b.init.witness/create.after", 1, true),
    ("x3b.init.witness/create.before", 1, true),
    ("x3b.init.witness/directory-barrier.after", 1, true),
    ("x3b.init.witness/directory-barrier.before", 1, true),
    ("x3b.init.witness/file-barrier.after", 1, true),
    ("x3b.init.witness/file-barrier.before", 1, true),
    ("x3b.init.witness/rename.after", 1, true),
    ("x3b.init.witness/rename.before", 1, true),
    ("x3b.init.witness/write.after", 1, true),
    ("x3b.init.witness/write.before", 1, true),
    ("x3b.init/create.after", 1, true),
    ("x3b.init/create.before", 1, true),
    ("x3b.init/directory-barrier.after", 1, true),
    ("x3b.init/directory-barrier.before", 1, true),
    ("x3b.rollover.before-open", 1, true),
    ("x3b.rollover.exclusive.readers/lock.after", 1, true),
    ("x3b.rollover.exclusive.readers/lock.before", 1, true),
    ("x3b.rollover.exclusive.writer/lock.after", 1, true),
    ("x3b.rollover.exclusive.writer/lock.before", 1, true),
    ("x3b.rollover.lock-dropped", 1, true),
    ("x3b.rollover.minted", 1, true),
    ("x3b.rollover.observed", 1, true),
    ("x3b.rollover.open.witness/create.after", 1, true),
    ("x3b.rollover.open.witness/create.before", 1, true),
    ("x3b.rollover.open.witness/directory-barrier.after", 1, true),
    (
        "x3b.rollover.open.witness/directory-barrier.before",
        1,
        true,
    ),
    ("x3b.rollover.open.witness/file-barrier.after", 1, true),
    ("x3b.rollover.open.witness/file-barrier.before", 1, true),
    ("x3b.rollover.open.witness/rename.after", 1, true),
    ("x3b.rollover.open.witness/rename.before", 1, true),
    ("x3b.rollover.open.witness/write.after", 1, true),
    ("x3b.rollover.open.witness/write.before", 1, true),
    ("x3b.rollover.opened", 1, true),
    ("x3b.rollover.readers-released", 1, true),
    ("x3b.rollover.readers-taken", 1, true),
    ("x3b.rollover.release.readers/unlock.after", 1, true),
    ("x3b.rollover.release.readers/unlock.before", 1, true),
    ("x3b.rollover.release.writer/unlock.after", 1, true),
    ("x3b.rollover.release.writer/unlock.before", 1, true),
    ("x3b.rollover.reserved", 1, true),
    ("x3b.rollover.terminal-appended", 1, true),
    ("x3b.rollover.writer-released", 1, true),
    ("x3b.rollover.writer-taken", 1, true),
    ("x3d.finish.end-step.after", 4, true),
    ("x3d.finish.end-step.before", 4, true),
    ("x3d.finish.lease-release", 4, true),
    ("x4.observer.tick", 4, false),
    ("x4t.floor-publication.dependency/create.after", 39, true),
    ("x4t.floor-publication.dependency/create.before", 39, true),
    (
        "x4t.floor-publication.dependency/directory-barrier.after",
        43,
        true,
    ),
    (
        "x4t.floor-publication.dependency/directory-barrier.before",
        43,
        true,
    ),
    (
        "x4t.floor-publication.dependency/file-barrier.after",
        35,
        true,
    ),
    (
        "x4t.floor-publication.dependency/file-barrier.before",
        35,
        true,
    ),
    ("x4t.floor-publication.dependency/write.after", 35, true),
    ("x4t.floor-publication.dependency/write.before", 35, true),
    ("x4t.floor-publication.pointer/create.after", 5, true),
    ("x4t.floor-publication.pointer/create.before", 5, true),
    (
        "x4t.floor-publication.pointer/directory-barrier.after",
        5,
        true,
    ),
    (
        "x4t.floor-publication.pointer/directory-barrier.before",
        5,
        true,
    ),
    ("x4t.floor-publication.pointer/file-barrier.after", 5, true),
    ("x4t.floor-publication.pointer/file-barrier.before", 5, true),
    ("x4t.floor-publication.pointer/rename.after", 5, true),
    ("x4t.floor-publication.pointer/rename.before", 5, true),
    ("x4t.floor-publication.pointer/write.after", 5, true),
    ("x4t.floor-publication.pointer/write.before", 5, true),
];
/// Its kill set (X9-0's `Census::kill_set`).
pub(crate) const KILL_SET: usize = 437;

fn census_table(exit: &Exit) -> Vec<(String, u32, bool)> {
    Census::from_exit(exit)
        .unwrap()
        .points
        .into_iter()
        .map(|p| (p.name, p.occurrences, p.durability))
        .collect()
}

#[test]
fn the_integrated_path_reaches_only_scoped_points_and_its_census_is_pinned() {
    let census = |setup: &Setup| {
        let exit = setup.spawn(Some("")).finish().unwrap();
        exit.verify_finished()
            .unwrap_or_else(|e| panic!("{e:?}\n{}", exit.diagnostics.join("\n")));
        assert_eq!(exit.outcome(), Some(OUTCOME));
        (census_table(&exit), exit.trace())
    };
    let (table, _) = census(&Setup::new());
    let pinned: Vec<(String, u32, bool)> = CENSUS
        .iter()
        .map(|(name, n, d)| ((*name).to_owned(), *n, *d))
        .collect();
    assert_eq!(table, pinned);
    // X9 r2: a second census run on this product is equal point for point.
    let (again, _) = census(&Setup::new());
    assert_eq!(again, table);
    let kills: usize = CENSUS
        .iter()
        .filter(|(_, _, durable)| *durable)
        .map(|(_, n, _)| [1, n.div_ceil(2), *n].iter().collect::<BTreeSet<_>>().len())
        .sum();
    assert_eq!(kills, KILL_SET);
    // Every registered scope this unit places is reached, and on the way
    // X4a's read-only observer tick and X3d-1's end-path points (the
    // operation's `end` runs through X3d's `finish` steps).
    let scopes: BTreeSet<&str> = CENSUS
        .iter()
        .map(|(name, _, _)| {
            opensip_platform::crash_barrier::SCOPES
                .iter()
                .map(|(scope, _)| *scope)
                .filter(|scope| {
                    name.starts_with(&format!("{scope}.")) || name.starts_with(&format!("{scope}/"))
                })
                .max_by_key(|scope| scope.len())
                .unwrap()
        })
        .collect();
    assert_eq!(
        scopes.into_iter().collect::<Vec<_>>(),
        [
            "x2.fence",
            "x2.lease",
            "x3b.append.cln",
            "x3b.append.rev",
            "x3b.append.seal",
            "x3b.append.terminal",
            "x3b.end.floor",
            "x3b.floor",
            "x3b.init",
            "x3b.rollover",
            "x3d.finish",
            "x4.observer",
            "x4t.floor-publication",
        ]
    );
}

// ------------------------------------------------- verified process deaths

impl Setup {
    /// The one registered namespace N under I.
    fn namespace(&self) -> PathBuf {
        let projects = self.fixture.installation.join("host/projects");
        let mut entries: Vec<PathBuf> = fs::read_dir(&projects)
            .unwrap()
            .map(|e| e.unwrap().path())
            .filter(|p| p.is_dir())
            .collect();
        assert_eq!(entries.len(), 1, "{entries:?}");
        entries.pop().unwrap()
    }
    /// The carrier's journal rows and the witness's state and sequence.
    fn journal(&self) -> (i64, String, i64) {
        let n = self.namespace();
        let c = rusqlite::Connection::open(n.join("grant-journal.sqlite")).unwrap();
        let rows: i64 = c
            .query_row("SELECT count(*) FROM grant_journal_v3", [], |r| r.get(0))
            .unwrap();
        drop(c);
        let witness = fs::read(n.join("grant-journal.witness.json")).unwrap();
        let text = String::from_utf8(witness).unwrap();
        let value = |key: &str| {
            let at = text.find(&format!("\"{key}\":")).unwrap() + key.len() + 3;
            text[at..]
                .split([',', '}'])
                .next()
                .unwrap()
                .trim_matches('"')
                .to_owned()
        };
        (rows, value("state"), value("seq").parse().unwrap())
    }
    /// Kill the traced child where it holds at `point`, and verify the death.
    fn kill_at(&self, point: &str) -> Exit {
        let mut child = self.spawn(Some(&format!("{point}=hold")));
        child.await_held(point).unwrap();
        let exit = child.kill().unwrap();
        exit.verify_death_at(point).unwrap();
        assert!(exit.outcome().is_none());
        exit
    }
    /// One finished, untraced child's outcome.
    fn run(&self, role: &str, input: &Path) -> String {
        let exit = self.child(role, input, None).finish().unwrap();
        exit.verify_finished().unwrap();
        exit.outcome()
            .map(str::to_owned)
            .or_else(|| {
                exit.stdout
                    .lines()
                    .find_map(|l| l.strip_prefix("OUTCOME ").map(str::to_owned))
            })
            .unwrap()
    }
    /// The next writer's start, in its own process.
    fn next_start(&self) -> String {
        let outcome = self.run("next", &self.input);
        let (start, end) = outcome.split_once(';').unwrap();
        assert!(end.starts_with("ended:"), "{outcome}");
        start.trim_start_matches("next=").to_owned()
    }
    /// The trust revocation version, read by name in this process (no clock).
    fn revocation_version(&self) -> i128 {
        self.fixture.current_trust_values().unwrap().1
    }
}

#[test]
fn a_kill_after_the_pending_witness_rename_is_reverted_by_the_next_writer() {
    // F07's shape: the PENDING witness is durable, the SEAL is not.
    let setup = Setup::new();
    setup.kill_at("x3b.append.seal.witness-pending/rename.after#1");
    assert_eq!(setup.journal(), (0, "PENDING".into(), 1));
    assert_eq!(setup.next_start(), "Reverted");
    assert_eq!(setup.journal(), (0, "COMMITTED".into(), 0));
}

#[test]
fn a_kill_after_the_seal_commit_is_advanced_by_the_next_writer() {
    // F09's death branch: the SEAL landed, its witness still PENDING.
    let setup = Setup::new();
    setup.kill_at("x3b.append.seal.commit.after#1");
    assert_eq!(setup.journal(), (1, "PENDING".into(), 1));
    assert_eq!(setup.next_start(), "Advanced");
    assert_eq!(setup.journal(), (1, "COMMITTED".into(), 1));
}

#[test]
fn an_injected_landed_commit_failure_is_undetermined_and_advanced_next() {
    // F09's injected branch: `fail-after` reports a COMMIT that landed.
    // The undetermined append latched the attempt ledger, so the
    // operation's journal step returns the closed budget and the workload
    // stops (nothing follows an uncertain outcome).
    let setup = Setup::new();
    let exit = setup
        .spawn(Some("x3b.append.seal.commit.after#1=fail-after"))
        .finish()
        .unwrap();
    exit.verify_finished().unwrap();
    assert_eq!(exit.outcome(), Some("refused:seal:Budget(Closed)"));
    assert_eq!(setup.journal(), (1, "PENDING".into(), 1));
    assert_eq!(setup.next_start(), "Advanced");
    // `fail-before`: the COMMIT does not land; the next writer reverts.
    let setup = Setup::new();
    let exit = setup
        .spawn(Some("x3b.append.seal.commit.before#1=fail-before"))
        .finish()
        .unwrap();
    exit.verify_finished().unwrap();
    assert_eq!(exit.outcome(), Some("refused:seal:Budget(Closed)"));
    assert_eq!(setup.journal(), (0, "PENDING".into(), 1));
    assert_eq!(setup.next_start(), "Reverted");
}

#[test]
fn the_kernel_releases_the_fence_and_the_lease_of_a_killed_writer() {
    use opensip_platform::{FileLock, LockMode};
    let busy = |path: &Path| {
        FileLock::try_acquire(fs::File::open(path).unwrap(), LockMode::Exclusive)
            .unwrap()
            .is_none()
    };
    // Held at the gate's lock: the fence is the child's until it dies.
    let setup = Setup::new();
    let fence = setup.fixture.installation.join("lifecycle.fence");
    let mut child = setup.spawn(Some("x2.fence.gate/lock.after#1=hold"));
    child.await_held("x2.fence.gate/lock.after#1").unwrap();
    assert!(busy(&fence));
    let exit = child.kill().unwrap();
    exit.verify_death_at("x2.fence.gate/lock.after#1").unwrap();
    assert!(!busy(&fence));
    // A pause, not a death: held at the second operation's lease, then
    // resumed, the run completes exactly as the unarmed census run.
    let setup = Setup::new();
    let point = "x2.lease.writer/lock.after#2";
    let mut child = setup.spawn(Some(&format!("{point}=hold")));
    child.await_held(point).unwrap();
    let lease = setup.namespace().join("writer.lease");
    assert!(busy(&lease) && busy(&setup.fixture.installation.join("lifecycle.fence")));
    child.resume(point).unwrap();
    let exit = child.finish().unwrap();
    exit.verify_finished().unwrap();
    assert_eq!(exit.outcome(), Some(OUTCOME));
    assert!(!busy(&lease));
}

#[test]
fn a_kill_after_the_trust_pointer_rename_leaves_the_new_state_v1() {
    // The first operation's fenced first read (X4T-b) wrote its floor
    // publication and died after `state.v1`'s rename, before its directory
    // barrier: the new capsule is visible (process death keeps the page
    // cache; L1), with the revocation version unchanged, and the fence is
    // free again.
    let setup = Setup::new();
    let current = setup
        .fixture
        .installation
        .join(format!("trust/stores/{}/state.v1", setup.fixture.store));
    let before = fs::read(&current).unwrap();
    setup.kill_at("x4t.floor-publication.pointer/rename.after#1");
    assert_ne!(fs::read(&current).unwrap(), before);
    assert_eq!(setup.revocation_version(), 1);
    // The shared fenced publication, in its own process, takes the fence
    // and advances.
    let input = setup.parent.join("publish.in");
    fs::write(
        &input,
        format!("{}version=2\n", fs::read_to_string(&setup.input).unwrap()),
    )
    .unwrap();
    assert_eq!(setup.run("publish", &input), "trust=1->2");
    assert_eq!(setup.revocation_version(), 2);
}

// ------------------------------------------------------ the post-state

#[test]
fn two_census_runs_differ_in_raw_bytes_and_agree_when_normalized() {
    use crate::crash_matrix_support::post_state::{capture, normalize};
    use opensip_identity::JsonValue as V;
    let run = || {
        let setup = Setup::new();
        let exit = setup.spawn(None).finish().unwrap();
        exit.verify_finished().unwrap();
        // An untraced child records nothing and reaches the same outcome.
        assert!(exit.records.is_empty());
        assert!(exit.stdout.contains(&format!("OUTCOME {OUTCOME}")));
        let state = capture(&setup.fixture.home).unwrap();
        // Capturing writes nothing: a second capture is identical.
        assert_eq!(capture(&setup.fixture.home).unwrap(), state);
        state
    };
    let (a, b) = (run(), run());
    // Not vacuous: the carrier's six rows (two SEALs, REV, CLN, the planted
    // RA and the TERMINAL), the OPEN witness and the floor are in `logical`.
    let member = |v: &V, k: &str| match v {
        V::Object(o) => o.get(k).cloned(),
        _ => None,
    };
    for state in [&a, &b] {
        let V::Object(databases) = member(&state.logical, "databases").unwrap() else {
            panic!()
        };
        let carrier = databases
            .iter()
            .find(|(path, _)| path.ends_with("/grant-journal.sqlite"))
            .map(|(_, dump)| dump.clone())
            .unwrap();
        let rows = member(&member(&carrier, "tables").unwrap(), "grant_journal_v3").unwrap();
        assert!(matches!(rows, V::Array(r) if r.len() == 6));
        let V::Object(operational) = member(&state.logical, "operational").unwrap() else {
            panic!()
        };
        let witness = operational
            .iter()
            .find(|(path, _)| path.ends_with("grant-journal.witness.json"))
            .map(|(_, v)| v.clone())
            .unwrap();
        assert_eq!(
            member(&witness, "state"),
            Some(V::String("COMMITTED".into()))
        );
        assert!(
            operational
                .keys()
                .any(|path| path.contains("trust/carrier-floors/"))
        );
    }
    assert_ne!(a.raw, b.raw);
    assert_ne!(a.logical, b.logical);
    // X9 r2 item 7: under the scripted clock the repetitions agree, the
    // trust store (`trustState`) included.
    if a.normalized_sha256 != b.normalized_sha256 {
        let (na, nb) = (normalize(&a.logical), normalize(&b.logical));
        let text = |v| String::from_utf8(opensip_identity::canonical_bytes(v).unwrap()).unwrap();
        let (ta, tb) = (text(&na), text(&nb));
        let at = ta
            .bytes()
            .zip(tb.bytes())
            .position(|(x, y)| x != y)
            .unwrap_or(0);
        panic!(
            "normalized states differ at {at}:\n{}\n{}",
            &ta[at.saturating_sub(300)..(at + 300).min(ta.len())],
            &tb[at.saturating_sub(300)..(at + 300).min(tb.len())]
        );
    }
    assert_eq!(
        member(&a.logical, "trustState"),
        member(&b.logical, "trustState")
    );
}

#[test]
fn a_killed_run_is_recorded_in_the_checkers_run_shape() {
    use crate::crash_matrix_support::post_state::capture;
    use crate::crash_matrix_support::run_record::{
        ChildExit, ChildRecord, Host, Product, RunRecord, Verdict, census_json, write_run,
    };
    use opensip_identity::JsonValue as V;
    let setup = Setup::new();
    let point = "x3b.append.seal.witness-pending/rename.after#1";
    let exit = setup.kill_at(point);
    let child = ChildRecord::from_exit("commit", 1, &exit);
    assert_eq!(child.exit, ChildExit::Signal(9));
    assert_eq!(child.last_held.as_deref(), Some(point));
    assert_eq!(child.trace_records, exit.records.len() as u64);
    assert_eq!(child.outcome, None);
    let s = |text: &str| V::String(text.into());
    let record = RunRecord {
        case: "F07".into(),
        variant: "kill-witness-pending-rename-after".into(),
        units: vec!["X3b".into()],
        labels: vec![
            "process-death".into(),
            "scripted-clock".into(),
            "synthetic".into(),
        ],
        product: Product {
            commit: "0".repeat(40),
            worktree_clean: true,
            toolchain: "rustc 1.95.0".into(),
        },
        host: Host {
            os: "macOS".into(),
            arch: "arm64".into(),
            filesystem: "apfs".into(),
        },
        clock_epoch: CLOCK_EPOCH,
        script: V::Array(vec![V::Object(
            [
                ("await".to_owned(), s(point)),
                ("then".to_owned(), s("kill")),
            ]
            .into(),
        )]),
        children: vec![child],
        post_state: capture(&setup.fixture.home).unwrap(),
        ladder: V::Array(Vec::new()),
        expected: V::Object(Default::default()),
        verdict: Verdict::Pass,
        ladder_end: None,
        not_applicable: None,
        timing_guard_ms: None,
    };
    let pin = write_run(&setup.parent, &record).unwrap();
    assert_eq!(pin.path, "runs/F07-kill-witness-pending-rename-after.json");
    let raw = fs::read(setup.parent.join(&pin.path)).unwrap();
    assert_eq!(pin.bytes, raw.len() as u64);
    let value = opensip_identity::parse_json(&raw).unwrap();
    // Canonical bytes, and exactly the checker's run keys.
    assert_eq!(opensip_identity::canonical_bytes(&value).unwrap(), raw);
    let V::Object(members) = &value else { panic!() };
    assert_eq!(
        members.keys().map(String::as_str).collect::<Vec<_>>(),
        [
            "case",
            "children",
            "clock",
            "expected",
            "host",
            "labels",
            "ladder",
            "postState",
            "product",
            "schema",
            "script",
            "units",
            "variant",
            "verdict"
        ]
    );
    // An existing run file is never replaced.
    assert!(write_run(&setup.parent, &record).is_err());
    // A refusal path's implicit fence release is scoped too: the census
    // workload on this already-registered root refuses at registration and
    // drops its writer, and the child still reports no harness error.
    let refused = setup.spawn(Some("")).finish().unwrap();
    refused.verify_finished().unwrap();
    assert!(
        refused
            .outcome()
            .unwrap()
            .starts_with("refused:registration:")
    );
    assert!(
        refused
            .records
            .iter()
            .any(|r| r.point == "x2.fence.release/unlock.after#1")
    );
    // The census as `matrix.json` carries it.
    let census_exit = Setup::new().spawn(Some("")).finish().unwrap();
    let census = Census::from_exit(&census_exit).unwrap();
    let (census_value, kill_set) = census_json(&census, &census_exit.trace());
    let V::Array(kills) = kill_set else { panic!() };
    assert_eq!(kills.len(), KILL_SET);
    let V::Object(c) = census_value else { panic!() };
    assert!(matches!(&c["points"], V::Array(points) if points.len() == CENSUS.len()));
    eprintln!("X91-RUN-RECORD {}", String::from_utf8(raw).unwrap());
}
