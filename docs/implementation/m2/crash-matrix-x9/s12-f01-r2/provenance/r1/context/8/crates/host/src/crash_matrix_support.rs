//! Law X9 r1 item 6 (unit X9-1): host's synthetic test-support surface for
//! the crash matrix, only under the test-only `crash-matrix` feature (law
//! X9 r1 item 2), `#[doc(hidden)]`.
//!
//! Host's matrix target (`crates/host/tests/commit_matrix_tests.rs`, X9-5)
//! reaches the whole surface here: storage's, which forwards security's,
//! unchanged, and (law X9 r11, unit X9-5) host's own items:
//! - the two runners, [`finalize_commit`] and [`store_gc`]. Each is a route
//!   into host's one commit coordinator (`finalization::finalize`) or host's
//!   one `store-gc` step (`maintenance::run`), and nothing else. Each makes
//!   its process's one driver entry, through `operation` or
//!   `settlement_sweep` (X9 r4 item 6), and returns a value report only;
//! - the on-disk run candidate's writer and reader (X9 r10's host order: a
//!   prior child writes the candidate, the `finalize` child reads it, so
//!   `finalize` replays before any custody, X5 r3 item 3), inputs only;
//! - the fixed delivery phase `finalize_commit` hands `finalize`.
//!
//! A process makes at most one call to the three entries and the two
//! runners together; a second runner call refuses on the invariant row
//! without effect, including after a first call that ended at replay,
//! before its entry. Nothing here returns or lends an authority type, takes
//! a receipt, gate, guard, monitor, clock, session, permit,
//! `ProjectOperation`, `ReplayedRun`, delivery phase or callback from its
//! caller, or sleeps, polls or waits on a timer.
pub use opensip_storage::crash_matrix_support::*;

use crate::fact_admission::RunCandidateInputs;
use crate::finalization::cancellation::CommitCancellationSource;
use crate::finalization::{
    DeliveryPhase, DecidedEnvelope, Finalization, OptionalFailed, Outcome, RendererFailed, Rollover, finalize, open_finalization,
};
use crate::maintenance::{NamespaceOutcome, SweepReport, run as sweep_run};
use crate::{InstallationTerminationV1, RenderedResponse, installation_termination};
use opensip_identity::{
    IdentityDomain, JsonValue as V, ObjectInput, RegisteredSchemas, canonical_bytes, digest_hex,
    parse_json,
};
use opensip_security::InstallationTermination as Row;
use opensip_storage::{NamespaceSweep, PublishedCommit};
use std::collections::BTreeMap;
use std::io::Write;
use std::path::Path;
use std::sync::atomic::{AtomicBool, Ordering};

/// Set by this process's first runner call, never cleared (X9 r10: a
/// runner makes the process's one entry, even when it ends at replay).
static RAN: AtomicBool = AtomicBool::new(false);
fn run_once() -> bool {
    !RAN.swap(true, Ordering::SeqCst)
}

// ------------------------------------------------- the candidate file

/// The schema of the on-disk run candidate.
pub const CANDIDATE_SCHEMA: &str = "opensip.x9.run-candidate.v1";

fn hex(bytes: &[u8]) -> String {
    bytes.iter().map(|b| format!("{b:02x}")).collect()
}
fn unhex(text: &str) -> Result<Vec<u8>, String> {
    if !text.len().is_multiple_of(2) {
        return Err("odd hex".into());
    }
    (0..text.len())
        .step_by(2)
        .map(|i| u8::from_str_radix(&text[i..i + 2], 16).map_err(|e| format!("hex: {e}")))
        .collect()
}

/// Write a run candidate (its retained objects, blobs and claimed RunId) as
/// canonical JSON at `path`. Inputs only: it reads nothing but its
/// arguments and writes only `path`.
pub fn write_run_candidate(
    path: &Path,
    run_id: &str,
    objects: &BTreeMap<String, ObjectInput>,
    blobs: &BTreeMap<[u8; 32], Vec<u8>>,
) -> Result<(), String> {
    let objects = objects
        .iter()
        .map(|(id, input)| {
            (
                id.clone(),
                V::Object(BTreeMap::from([
                    (
                        "domain".to_owned(),
                        V::String(input.domain.name().to_owned()),
                    ),
                    ("descriptor".to_owned(), input.descriptor.clone()),
                ])),
            )
        })
        .collect();
    let blobs = blobs
        .iter()
        .map(|(digest, bytes)| (digest_hex(digest), V::String(hex(bytes))))
        .collect();
    let document = V::Object(BTreeMap::from([
        ("schema".to_owned(), V::String(CANDIDATE_SCHEMA.to_owned())),
        ("runId".to_owned(), V::String(run_id.to_owned())),
        ("objects".to_owned(), V::Object(objects)),
        ("blobs".to_owned(), V::Object(blobs)),
    ]));
    let bytes = canonical_bytes(&document).map_err(|e| format!("candidate: {e:?}"))?;
    std::fs::write(path, bytes).map_err(|e| format!("candidate: {e}"))
}

/// A run candidate read back from its file: inert values.
pub struct CandidateFile {
    pub run_id: String,
    pub objects: BTreeMap<String, ObjectInput>,
    pub blobs: BTreeMap<[u8; 32], Vec<u8>>,
}

/// Read the run candidate at `path`. Each blob is keyed by the digest the
/// file names, so a parent's alteration of a blob's bytes stays visible to
/// replay as the altered input it is.
pub fn read_run_candidate(path: &Path) -> Result<CandidateFile, String> {
    let raw = std::fs::read(path).map_err(|e| format!("candidate: {e}"))?;
    let document = parse_json(&raw).map_err(|e| format!("candidate: {e:?}"))?;
    let V::Object(fields) = document else {
        return Err("candidate: not an object".into());
    };
    let text = |key: &str| match fields.get(key) {
        Some(V::String(s)) => Ok(s.clone()),
        _ => Err(format!("candidate: {key}")),
    };
    if text("schema")? != CANDIDATE_SCHEMA {
        return Err("candidate: schema".into());
    }
    let run_id = text("runId")?;
    let (Some(V::Object(objects)), Some(V::Object(blobs))) =
        (fields.get("objects"), fields.get("blobs"))
    else {
        return Err("candidate: objects or blobs".into());
    };
    let mut read_objects = BTreeMap::new();
    for (id, value) in objects {
        let V::Object(member) = value else {
            return Err(format!("candidate object {id}"));
        };
        let (Some(V::String(domain)), Some(descriptor)) =
            (member.get("domain"), member.get("descriptor"))
        else {
            return Err(format!("candidate object {id}"));
        };
        let domain =
            IdentityDomain::parse(domain).map_err(|e| format!("candidate domain: {e:?}"))?;
        read_objects.insert(
            id.clone(),
            ObjectInput {
                domain,
                descriptor: descriptor.clone(),
            },
        );
    }
    let mut read_blobs = BTreeMap::new();
    for (digest, value) in blobs {
        let V::String(bytes) = value else {
            return Err(format!("candidate blob {digest}"));
        };
        let key: [u8; 32] = unhex(digest)?
            .try_into()
            .map_err(|_| format!("candidate digest {digest}"))?;
        read_blobs.insert(key, unhex(bytes)?);
    }
    Ok(CandidateFile {
        run_id,
        objects: read_objects,
        blobs: read_blobs,
    })
}

// ------------------------------------------------- the delivery phase

/// The fixed response the matrix's delivery phase renders.
pub const FIXED_RESPONSE: &[u8] = b"{\"x9\":\"delivered\"}\n";

/// X9 r10's fixed delivery phase: it renders one fixed response with exit 0
/// into a buffer the runner owns, and its optional effect succeeds. A
/// delivery failure comes only from an armed `x7.delivery` point. It reads
/// nothing from the store and takes no lease, receipt or read session.
struct FixedPhase {
    output: Vec<u8>,
}
impl DeliveryPhase for FixedPhase {
    type Projection = ();
    fn project(&mut self, _: &PublishedCommit) -> Result<((), u8), RendererFailed> { Ok(((), 0)) }
    fn finalize_operational(&mut self, _: &Finalization) {}
    fn error_output(&mut self) -> &mut dyn Write { &mut self.output }
    fn render(&mut self, envelope: DecidedEnvelope<'_, ()>) -> Result<RenderedResponse, RendererFailed> {
        Ok(RenderedResponse {
            bytes: match envelope.outcome { Outcome::Authoritative { .. } => FIXED_RESPONSE.to_vec(), Outcome::Terminated(_) | Outcome::Interrupted { .. } => Vec::new() },
            exit_code: match envelope.outcome { Outcome::Authoritative { exit, .. } => *exit, Outcome::Terminated(t) => t.row.exit, Outcome::Interrupted { .. } => 130 },
        })
    }
    fn output(&mut self) -> &mut dyn Write {
        &mut self.output
    }
    fn optional(&mut self, _commit: &PublishedCommit) -> Result<(), OptionalFailed> {
        Ok(())
    }
}

// ------------------------------------------------- the finalize runner

/// The envelope `finalize` projected, as values.
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum FinalizeOutcome {
    /// Required delivery succeeded: the committed RunId and the exit.
    Authoritative { run_id: String, exit: u8 },
    /// Every other end, on its one row, with what finalization disclosed
    /// beside it: the retained RunId, the remedy, the namespace, and
    /// whether a requested binding was disclosed.
    Interrupted { signal: opensip_security::D9Signal, run_id: Option<String> },
    Terminated {
        row: InstallationTerminationV1,
        run_id: Option<String>,
        remedy: Option<&'static str>,
        namespace: Option<String>,
        requested_binding: bool,
    },
}

/// The capacity rollover's disclosure, as values (X7 r6 item 6).
#[derive(Debug, Clone, PartialEq, Eq)]
pub enum RolloverReport {
    Rolled { opened_generation: i64 },
    AlreadyRolled,
    Skipped,
    Refused(InstallationTerminationV1),
    Undetermined(InstallationTerminationV1),
}

/// What one `finalize_commit` call reports: values only.
#[derive(Debug, Clone, PartialEq, Eq)]
pub struct FinalizeReport {
    pub arrival_phases: Vec<String>,
    pub outcome: FinalizeOutcome,
    pub end_failure: Option<InstallationTerminationV1>,
    pub end_step_failure: Option<InstallationTerminationV1>,
    pub rollover: Option<RolloverReport>,
    pub optional_failed: bool,
    /// The bytes the fixed phase delivered.
    pub delivered: Vec<u8>,
}

fn report(finalization: Finalization, delivered: Vec<u8>) -> FinalizeReport {
    let outcome = match finalization.outcome {
        Outcome::Authoritative { run, exit } => FinalizeOutcome::Authoritative {
            run_id: run.run_id().to_owned(),
            exit,
        },
        Outcome::Interrupted { signal, run } => FinalizeOutcome::Interrupted { signal, run_id: run.map(|r| r.run_id().to_owned()) },
        Outcome::Terminated(t) => FinalizeOutcome::Terminated {
            row: t.row,
            run_id: t.run_id,
            remedy: t.remedy,
            namespace: t.namespace,
            requested_binding: t.requested.is_some(),
        },
    };
    let rollover = finalization.rollover.map(|r| match r {
        Rollover::Rolled { opened_generation } => RolloverReport::Rolled { opened_generation },
        Rollover::AlreadyRolled => RolloverReport::AlreadyRolled,
        Rollover::Skipped => RolloverReport::Skipped,
        Rollover::Refused(row) => RolloverReport::Refused(row),
        Rollover::Undetermined(row) => RolloverReport::Undetermined(row),
    });
    FinalizeReport {
        arrival_phases: Vec::new(),
        outcome,
        end_failure: finalization.end_failure,
        end_step_failure: finalization.end_step_failure,
        rollover,
        optional_failed: finalization.optional_failure.is_some(),
        delivered,
    }
}

fn invariant() -> FinalizeReport {
    FinalizeReport {
        arrival_phases: Vec::new(),
        outcome: FinalizeOutcome::Terminated {
            row: installation_termination(&Row::Invariant),
            run_id: None,
            remedy: None,
            namespace: None,
            requested_binding: false,
        },
        end_failure: None,
        end_step_failure: None,
        rollover: None,
        optional_failed: false,
        delivered: Vec::new(),
    }
}

/// Law X9 r10 (unit X9-5): host's commit coordinator over the synthetic
/// installation `at`, the project root `root`, and the run candidate the
/// prior `candidate` child wrote at `candidate`. It calls host's own
/// `finalize` with `admit` set to the `operation` entry and the fixed
/// delivery phase, so `finalize` replays before any custody and `operation`
/// runs only after the replay succeeded. A candidate file that cannot be
/// read is reported on the host I/O row, with no entry made.
pub fn finalize_commit(
    at: &SyntheticInstallation,
    root: &Path,
    candidate: &Path,
) -> FinalizeReport {
    if !run_once() {
        return invariant();
    }
    let file = match read_run_candidate(candidate) {
        Ok(file) => file,
        Err(_) => {
            return FinalizeReport {
                outcome: FinalizeOutcome::Terminated {
                    row: installation_termination(&Row::HostIo),
                    run_id: None,
                    remedy: None,
                    namespace: None,
                    requested_binding: false,
                },
                ..invariant()
            };
        }
    };
    let registry: RegisteredSchemas = match crate::embedded_schema_registry() {
        Ok(registry) => registry,
        Err(_) => return invariant(),
    };
    let inputs = RunCandidateInputs {
        registry: &registry,
        objects: &file.objects,
        blobs: &file.blobs,
        run_id: &file.run_id,
    };
    let mut phase = FixedPhase { output: Vec::new() };
    let arrivals = std::sync::Arc::new(std::sync::Mutex::new(Vec::new()));
    let records = arrivals.clone();
    let mut port = CommitCancellationSource::new(move |record| {
        records.lock().unwrap().push(format!("{:?}", record.phase));
    });
    let source = port.clone();
    let _signal_input = opensip_platform::crash_barrier::register_signal_input(move |signal| {
        let signal = match signal {
            opensip_platform::crash_barrier::SignalInput::Sigint => opensip_security::D9Signal::Sigint,
            opensip_platform::crash_barrier::SignalInput::Sigterm => opensip_security::D9Signal::Sigterm,
            opensip_platform::crash_barrier::SignalInput::Sighup => opensip_security::D9Signal::Sighup,
        };
        let _ = source.receive(signal);
    });
    let finalization = match operation(at, root) {
        Ok(operation) => match open_finalization(operation, &mut phase, &mut port) {
            Ok(opened) => finalize(opened, &inputs, &mut phase, &mut port),
            Err(finalization) => finalization,
        },
        Err(row) => return FinalizeReport { outcome: FinalizeOutcome::Terminated { row: installation_termination(&row), run_id: None, remedy: None, namespace: None, requested_binding: false }, ..invariant() },
    };
    let mut report = report(finalization, phase.output);
    report.arrival_phases = arrivals.lock().unwrap().clone();
    report
}

// ------------------------------------------------- the store-gc runner

/// One namespace `store_gc` reached, as values: `swept` is `None` when its
/// lease was busy (skipped and retained).
#[derive(Debug, PartialEq, Eq)]
pub struct GcNamespace {
    pub namespace: String,
    pub swept: Option<NamespaceSweep>,
    pub row: Option<InstallationTerminationV1>,
}

/// What one `store_gc` call reports: each namespace reached, in order, and
/// the row that ended the sweep or failed its release.
#[derive(Debug, PartialEq, Eq)]
pub struct GcReport {
    pub namespaces: Vec<GcNamespace>,
    pub ended: Option<InstallationTerminationV1>,
}

/// Law X9 r10 (unit X9-5): host's `store-gc` settlement step over the
/// synthetic installation `at`: host's own `maintenance::run` over the
/// `settlement_sweep` entry. An admission refusal ends it as `sweep_store`
/// reports one.
pub fn store_gc(at: &SyntheticInstallation) -> GcReport {
    if !run_once() {
        return GcReport {
            namespaces: Vec::new(),
            ended: Some(installation_termination(&Row::Invariant)),
        };
    }
    let report: SweepReport = match settlement_sweep(at) {
        Ok(sweep) => sweep_run(sweep),
        Err(row) => SweepReport {
            namespaces: Vec::new(),
            ended: Some(installation_termination(&row)),
        },
    };
    GcReport {
        namespaces: report
            .namespaces
            .into_iter()
            .map(|n| GcNamespace {
                namespace: n.namespace,
                swept: match n.outcome {
                    NamespaceOutcome::Skipped => None,
                    NamespaceOutcome::Swept(swept) => Some(swept),
                },
                row: n.row,
            })
            .collect(),
        ended: report.ended,
    }
}
