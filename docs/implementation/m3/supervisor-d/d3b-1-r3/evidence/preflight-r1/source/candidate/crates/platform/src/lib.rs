#![deny(unsafe_code)]

// M3-D r5 item 1 (unit D3a-0, LD-D3A-9): `LaunchSpec::fixture` reaches a
// dependent only as a dev-dependency feature, never a build without debug
// assertions.
#[cfg(all(feature = "test-fixture", not(debug_assertions)))]
compile_error!(
    "the test-fixture feature is test-only (law M3-D r5 item 1) and refuses every build without debug assertions"
);

// Law X9 r1 item 2, guard 1: the crash barrier never reaches a build without
// debug assertions, so a release-profile build with the feature fails here.
#[cfg(all(feature = "crash-matrix", not(debug_assertions)))]
compile_error!(
    "the crash-matrix feature is test-only (law X9 r1 item 2) and refuses every build without debug assertions"
);

// `crash_barrier!` and `crash_scope!`. Without the feature both expand to
// their wrapped effect or to nothing: no call, no string, no branch.
mod crash_macros;
// The barrier module (registry, kinds, arming parser, child rendezvous and
// parent driver) exists only under the test-only feature.
#[cfg(all(
    feature = "crash-matrix",
    any(target_os = "macos", target_os = "linux")
))]
#[doc(hidden)]
pub mod crash_barrier;
// Source and manifest pins for the feature and the self-test workload; they
// run in every test build, with or without the feature.
#[cfg(all(test, any(target_os = "macos", target_os = "linux")))]
mod crash_matrix_tests;

// Unsafe FFI is confined to the selected OS adapters; other platform modules
// keep the crate-wide denial. These handles do not establish policy or trust.
#[cfg(any(target_os = "macos", target_os = "linux"))]
#[allow(unsafe_code)]
mod filesystem;
#[cfg(any(target_os = "macos", target_os = "linux"))]
pub use filesystem::{
    DirectoryBarrier, DirectoryBarrierReceipt, DirectoryRenameFailure, DirectoryVisitError,
    DirectoryVisitSummary, ExistingFileReceipt, NamedDirectoryPublication, NewFileReceipt,
    PrivateDirectoryStage, PublicationFailure, PublicationStage, ReplacementReceipt,
    RetainedChildDirectory, RetainedDirectory, RetainedDirectoryPath, TargetVisibility,
};
#[cfg(any(target_os = "macos", target_os = "linux"))]
pub use filesystem::{
    DirectoryRenameClass, ExclusiveRegularError, ExclusiveRegularOutcome, FileBarrierReceipt,
    NewRegularWriteError, RenameReplaceError, classify_directory_rename,
    create_exclusive_regular_cost, exclusive_publication_cost, private_directory_stage_cost,
    rename_replace_cost, write_new_regular_accounted, write_new_regular_cost,
    write_new_regular_reserved,
};
#[cfg(any(target_os = "macos", target_os = "linux"))]
pub use filesystem::{
    ExclusiveDirectoryError, ExclusiveDirectoryOutcome, create_exclusive_directory_cost,
    directory_barrier_cost,
};
// M3-C r8 item 1 (unit C1a2): the candidate blob custody's exclusive rename
// and unlink inside one retained directory.
#[cfg(any(target_os = "macos", target_os = "linux"))]
#[allow(unsafe_code)]
mod custody_entry;
#[cfg(any(target_os = "macos", target_os = "linux"))]
pub use custody_entry::{ExclusiveRenameOutcome, rename_exclusive_cost, unlink_entry_cost};

/// Failure to obtain a complete independent OS CSPRNG draw.
#[derive(Debug)]
pub struct EntropyError;

/// Operational correlation only; never an input to semantic identity.
pub fn request_entropy() -> Result<[u8; 16], EntropyError> {
    let mut value = [0; 16];
    getrandom::fill(&mut value).map_err(|_| EntropyError)?;
    Ok(value)
}

/// Lowercase hex of 16 bytes behind `prefix`: identity §2's `req1_` and
/// `exec1_` grammars.
fn render_id(prefix: &str, bytes: &[u8; 16]) -> String {
    use std::fmt::Write as _;
    let mut text = String::with_capacity(prefix.len() + 32);
    text.push_str(prefix);
    for byte in bytes {
        write!(&mut text, "{byte:02x}").expect("String writes cannot fail");
    }
    text
}

/// Law M3-J1 r6 item 2 (unit J3a): one invocation's RequestId. Its only
/// constructor is the CSPRNG draw (`request_entropy`). The host's
/// process-custody registry reserves it at ingress and lends
/// `&RequestIdentity` to the durable entry (J1 item 3), and the creation
/// intent records it and draws no RequestId of its own (law 464 r3 item 1).
/// Sealed: no constructor from bytes or text, and not `Clone`, `Default`,
/// serializable or deserializable. It is a correlation identity only: no
/// custody, grant or authority.
pub struct RequestIdentity {
    bytes: [u8; 16],
}
impl std::fmt::Debug for RequestIdentity {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_tuple("RequestIdentity")
            .field(&render_id("req1_", &self.bytes))
            .finish()
    }
}
impl RequestIdentity {
    /// One complete, independent 128-bit OS CSPRNG draw. Failure returns no
    /// identity and no partial bytes. The draw is not a reservation: the
    /// host's registry checks its uniqueness before any use (IE:77-79).
    pub fn draw() -> Result<Self, EntropyError> {
        request_entropy().map(|bytes| Self { bytes })
    }
    /// The read-only projection: the drawn bytes, which every carrier
    /// renders as `req1_` and 32 lowercase hex.
    pub fn bytes(&self) -> [u8; 16] {
        self.bytes
    }
}

/// Law M3-J1 r6 item 2 (J1-R4; unit J3a): an ExecutionId reserved, with its
/// uniqueness checked, in this process's `ExecutionIdReservations` before any
/// use (IE:77-81). The registry is its only constructor: there is none from
/// bytes or text, and it is not `Clone`, `Default`, serializable or
/// deserializable. P0's writer, `CommitSession`, the attempt row and the
/// operational record take this type or its read-only projection, so a bare
/// draw reaches none of them.
#[derive(PartialEq, Eq)]
pub struct ReservedExecutionId {
    bytes: [u8; 16],
    rendered: String,
}
impl std::fmt::Debug for ReservedExecutionId {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        std::fmt::Debug::fmt(&self.rendered, f)
    }
}
impl ReservedExecutionId {
    /// The read-only projection: identity §2's `exec1_` and 32 lowercase
    /// hex.
    pub fn as_str(&self) -> &str {
        &self.rendered
    }
    /// The reserved bytes. Read-only; they reserve and admit nothing.
    pub fn bytes(&self) -> [u8; 16] {
        self.bytes
    }
}

/// Why no ExecutionId was reserved. Each is the drawing owner's existing
/// host-I/O row (J1 item 2; no code is added).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum ExecutionIdUnavailable {
    /// The CSPRNG draw failed.
    Entropy,
    /// Eight draws in a row were already reserved in this process.
    CollisionExhausted,
}

/// Law M3-J1 r6 item 2 (J1-R4; unit J3a): the process-custody ExecutionId
/// reservation registry, IE:77-81's "corresponding operational ledger" for
/// ExecutionIds before any use. It lives here, beside `request_entropy`,
/// because security and the host both draw ExecutionIds. One set per
/// process: each draw is checked against every ExecutionId already reserved
/// in the process, a collision redraws (at most eight draws in all, as the
/// host's `RequestAuthority` does), and a reservation is never released or
/// reused. It is not durable: across processes, uniqueness rests on the
/// 128-bit draw, and an authoritative attempt is reserved a second time,
/// durably, by its attempt row (X3c item 3). No owner holds it: only
/// `reserve_execution_id` reserves, and only `execution_id_reserved` reads.
struct ExecutionIdReservations {
    reserved: std::collections::BTreeSet<[u8; 16]>,
}
static EXECUTION_IDS: std::sync::Mutex<ExecutionIdReservations> =
    std::sync::Mutex::new(ExecutionIdReservations {
        reserved: std::collections::BTreeSet::new(),
    });
impl ExecutionIdReservations {
    /// The process's one registry. A panic can never leave it half-written
    /// (`allocate` inserts in one step), so a poisoned lock is still sound.
    fn process() -> std::sync::MutexGuard<'static, Self> {
        EXECUTION_IDS
            .lock()
            .unwrap_or_else(std::sync::PoisonError::into_inner)
    }
    /// Up to eight draws, each reserved only if no ExecutionId in this
    /// registry has its bytes. A failed draw or exhaustion reserves nothing.
    fn allocate(
        &mut self,
        mut draw: impl FnMut() -> Result<[u8; 16], EntropyError>,
    ) -> Result<ReservedExecutionId, ExecutionIdUnavailable> {
        for _ in 0..8 {
            let bytes = draw().map_err(|_| ExecutionIdUnavailable::Entropy)?;
            if self.reserved.insert(bytes) {
                // Constructed only after the uniqueness insert. There is no
                // inherent constructor (X8 r3 item 3, group F).
                return Ok(ReservedExecutionId {
                    bytes,
                    rendered: render_id("exec1_", &bytes),
                });
            }
        }
        Err(ExecutionIdUnavailable::CollisionExhausted)
    }
}

/// Identity §2's ExecutionId grammar, `exec1_` and 32 lowercase hex, as
/// bytes.
fn parse_execution_id(text: &str) -> Option<[u8; 16]> {
    let hex = text.strip_prefix("exec1_")?;
    if hex.len() != 32
        || !hex
            .bytes()
            .all(|b| b.is_ascii_digit() || (b'a'..=b'f').contains(&b))
    {
        return None;
    }
    let mut bytes = [0; 16];
    for (byte, pair) in bytes.iter_mut().zip(hex.as_bytes().chunks(2)) {
        *byte = u8::from_str_radix(std::str::from_utf8(pair).ok()?, 16).ok()?;
    }
    Some(bytes)
}

/// Draw one ExecutionId from the OS CSPRNG and reserve it in this process's
/// registry (J1 item 2): the only way to obtain a `ReservedExecutionId`.
/// The creation intent's prelude reserves through it in `mint_intent`,
/// `CommitSession::open` at its draw point, and the host at each ephemeral
/// and render attempt's start.
pub fn reserve_execution_id() -> Result<ReservedExecutionId, ExecutionIdUnavailable> {
    ExecutionIdReservations::process().allocate(request_entropy)
}

/// Whether `id` names an ExecutionId reserved in this process. Read-only:
/// it reserves, releases and grants nothing.
pub fn execution_id_reserved(id: &str) -> bool {
    parse_execution_id(id)
        .is_some_and(|bytes| ExecutionIdReservations::process().reserved.contains(&bytes))
}

/// One complete, independent 256-bit OS CSPRNG draw for one ProjectId
/// candidate (the registry owner's PROJECT-ID-V1 allocation: up to eight such
/// draws). Failure returns no bytes and no partial guess. The draw is
/// randomness only, never a registration, custody or authorization token.
pub fn project_id_draw() -> Result<[u8; 32], EntropyError> {
    let mut value = [0; 32];
    getrandom::fill(&mut value).map_err(|_| EntropyError)?;
    Ok(value)
}

/// A complete 256-bit OS CSPRNG draw for a host recovery challenge.
/// Failure returns no nonce. Entropy is not a custody or authorization token.
pub fn recovery_nonce() -> Result<[u8; 32], EntropyError> {
    let mut value = [0; 32];
    getrandom::fill(&mut value).map_err(|_| EntropyError)?;
    Ok(value)
}

#[cfg(any(target_os = "macos", target_os = "linux"))]
#[allow(unsafe_code)]
mod locks;
#[cfg(any(target_os = "macos", target_os = "linux"))]
pub use locks::{FileLock, LockMode};

#[cfg(any(target_os = "macos", target_os = "linux"))]
mod clock;
#[cfg(target_os = "linux")]
#[allow(unsafe_code)]
mod linux;
#[cfg(target_os = "macos")]
#[allow(unsafe_code)]
mod macos;
#[cfg(any(target_os = "macos", target_os = "linux"))]
pub use clock::{ClockError, ClockObservation, observe_clock, process_cpu_time};
#[cfg(any(target_os = "macos", target_os = "linux"))]
#[allow(unsafe_code)]
mod harness_descriptor;
#[cfg(any(target_os = "macos", target_os = "linux"))]
pub use harness_descriptor::{HarnessDescriptorError, admit_harness_descriptor};
mod disposition;
pub use disposition::{Disposition, dispose};
#[cfg(test)]
mod disposition_tests;

#[cfg(any(target_os = "macos", target_os = "linux"))]
pub use filesystem::{
    AclWriter, DescriptorAcl, DescriptorFilesystem, DescriptorMetadata, DescriptorObservation,
    DescriptorObservationError, descriptor_name_matches, descriptor_name_matches_accounted,
    descriptor_name_matches_reserved, descriptor_name_observation_cost, observe_descriptor,
    observe_filesystem,
};
#[cfg(any(target_os = "macos", target_os = "linux"))]
pub use filesystem::{
    child_absence_observation_cost, descriptor_filesystem_observation_cost,
    observe_filesystem_accounted, observe_filesystem_reserved, open_child_directory_cost,
    retained_path_open_cost,
};
#[cfg(target_os = "macos")]
pub use filesystem::{
    observe_descriptor_metadata, open_fixed_regular_following, open_fixed_regular_following_cost,
};
// M3-B r5 items 12 and 13 (unit B2-b1): the by-name child observation.
#[cfg(target_os = "macos")]
pub use filesystem::{ChildKind, ChildObservation};

/// Obtain the macOS per-account temporary location, independent of HOME/TMPDIR.
/// The OS may create the directory as a side effect. Never call on a write-free
/// admission or report-only path; current callers are test fixtures only.
/// The returned path may contain symlinked components or a trailing separator.
/// It is not canonical or admitted custody, storage selection or creation consent.
/// Resolve its location, then separately admit every retained directory component.
#[cfg(target_os = "macos")]
pub fn account_temporary_directory() -> std::io::Result<std::path::PathBuf> {
    macos::account_temporary_directory()
}

#[cfg(any(target_os = "macos", target_os = "linux"))]
#[allow(unsafe_code)]
mod account;
#[cfg(any(target_os = "macos", target_os = "linux"))]
pub use account::{
    AccountObservation, AccountObservationError, account_observation_cost, observe_account,
    observe_account_accounted, observe_account_reserved,
};

// Read-only native macOS identity samples; no profile or execution authority.
#[cfg(any(target_os = "macos", target_os = "linux"))]
#[cfg_attr(target_os = "macos", allow(unsafe_code))]
mod macos_boot;
#[cfg(any(target_os = "macos", target_os = "linux"))]
pub use macos_boot::{
    MacosBootError, MacosBootObservation, macos_boot_observation_cost, observe_macos_boot,
    observe_macos_boot_accounted,
};

#[cfg(target_os = "macos")]
#[allow(unsafe_code)]
mod macos_loader;
#[cfg(target_os = "macos")]
pub use macos_loader::{
    MacosLoaderError, MacosLoaderObservation, capture_system_loader,
    capture_system_loader_accounted, system_loader_capture_cost, system_loader_recheck_cost,
};

#[cfg(target_os = "macos")]
#[allow(unsafe_code)]
mod macos_image;
#[cfg(target_os = "macos")]
pub use macos_image::{RunningImageError, RunningImageObservation, observe_running_image};

#[cfg(target_os = "macos")]
#[allow(unsafe_code)]
mod macos_process;
#[cfg(target_os = "macos")]
pub use macos_process::{
    MacosProcessError, MacosProcessObservation, macos_process_observation_cost,
    observe_macos_process, observe_macos_process_accounted,
};

#[cfg(any(target_os = "macos", target_os = "linux"))]
pub use filesystem::{DirectoryBirthObservation, observe_directory_birth};

#[cfg(unix)]
pub use filesystem::{
    DirectoryVolumeObservation, directory_volume_observation_cost, observe_directory_volume,
};

// M3-D r5 items 1 to 8 (unit D1a): the only production spawner. Its FFI is
// confined here; it holds no supervision policy (D3) and accepts only a
// `VerifiedLaunch` (D4's closure recheck).
#[allow(unsafe_code)]
mod process;
pub use process::{
    Child as ProcessChild, ChildEnvironment, ChildScratch, ClosureRecheck, DescriptorSet,
    ExitStatus as ProcessExitStatus, KillOutcome, LaunchClass, LaunchError, LaunchSpec, Listing,
    ProcessIdentity, Protected, Readiness, Reaped, ScratchRoot, SpecError as LaunchSpecError,
    TerminatingSignal, Unreaped, VerifiedLaunch, child_processes, group_members_bounded,
    process_identity, resident_bytes, spawn, wait_ready,
};
#[cfg(all(test, target_os = "macos"))]
#[allow(unsafe_code)]
mod process_tests;

// Accounting shared by one operation owner. These are not custody or permission.
mod work_ledger;
pub use work_ledger::{
    BudgetFailure as WorkBudgetError, Cost as WorkCost, Failure as WorkFailure, ReservedPostchecks,
    SettlementReserve, WorkLedger, WorkScope,
};

mod work_reader;
pub use work_reader::{
    ReadFailure as WorkReadFailure, read_bounded_accounted, read_bounded_cost,
    read_bounded_observed, read_bounded_reserved, read_bounded_reserved_with_postchecks,
};

#[cfg(any(target_os = "macos", target_os = "linux"))]
pub use filesystem::{
    CapturedAclEntry, CapturedAclPrincipal, CapturedAclState, DescriptorAclCapture,
    DescriptorAclCaptureError, capture_descriptor_acl_accounted, capture_descriptor_acl_observed,
    capture_descriptor_acl_reserved, descriptor_acl_capture_cost,
};

#[cfg(target_os = "macos")]
pub use macos::{
    append_owner_zero_allow_accounted, append_owner_zero_allow_cost,
    append_owner_zero_allow_reserved,
};

// Law M3-J1 r6 item 2 (unit J3a), control J-C4b's registry bullets: forced
// draw sequences on a local registry, as the host's `RequestAuthority` tests
// force theirs, and the process registry itself.
#[cfg(test)]
mod reservation_tests {
    use super::*;
    use std::collections::BTreeSet;

    fn local() -> ExecutionIdReservations {
        ExecutionIdReservations {
            reserved: BTreeSet::new(),
        }
    }

    #[test]
    fn a_repeated_draw_is_redrawn_and_the_redraw_is_reserved() {
        let mut registry = local();
        let first = registry.allocate(|| Ok([7; 16])).unwrap();
        let mut draws = 0;
        let second = registry
            .allocate(|| {
                draws += 1;
                Ok(if draws < 3 { [7; 16] } else { [8; 16] })
            })
            .unwrap();
        assert_eq!(draws, 3);
        assert_eq!(first.bytes(), [7; 16]);
        assert_eq!(second.bytes(), [8; 16]);
        assert_ne!(first, second);
        assert_eq!(registry.reserved, BTreeSet::from([[7; 16], [8; 16]]));
    }

    #[test]
    fn eight_collisions_or_a_failed_draw_refuse_and_reserve_nothing() {
        let mut registry = local();
        let _first = registry.allocate(|| Ok([0; 16])).unwrap();
        let mut draws = 0;
        assert_eq!(
            registry
                .allocate(|| {
                    draws += 1;
                    Ok([0; 16])
                })
                .unwrap_err(),
            ExecutionIdUnavailable::CollisionExhausted
        );
        assert_eq!(draws, 8);
        assert_eq!(
            registry.allocate(|| Err(EntropyError)).unwrap_err(),
            ExecutionIdUnavailable::Entropy
        );
        // A refusal after a collision reserves neither draw.
        let mut calls = 0;
        assert_eq!(
            registry
                .allocate(|| {
                    calls += 1;
                    if calls == 1 {
                        Ok([0; 16])
                    } else {
                        Err(EntropyError)
                    }
                })
                .unwrap_err(),
            ExecutionIdUnavailable::Entropy
        );
        assert_eq!(registry.reserved, BTreeSet::from([[0; 16]]));
    }

    #[test]
    fn the_process_registry_reserves_distinct_ids_and_never_releases_one() {
        let a = reserve_execution_id().unwrap();
        let b = reserve_execution_id().unwrap();
        assert_ne!(a, b);
        assert!(execution_id_reserved(a.as_str()) && execution_id_reserved(b.as_str()));
        let held = a.as_str().to_owned();
        drop(a);
        // Dropping the value releases nothing: its bytes stay reserved.
        assert!(execution_id_reserved(&held));
        assert!(!execution_id_reserved("exec1_not-an-id"));
    }

    #[test]
    fn the_projections_are_identity_section_2s_grammars() {
        let reserved = local().allocate(|| Ok([0xab; 16])).unwrap();
        assert_eq!(reserved.as_str(), format!("exec1_{}", "ab".repeat(16)));
        assert_eq!(
            format!("{reserved:?}"),
            format!("\"exec1_{}\"", "ab".repeat(16))
        );
        assert_eq!(parse_execution_id(reserved.as_str()), Some([0xab; 16]));
        for unlawful in [
            "exec1_",
            "exec1_injected",
            &format!("exec1_{}", "AB".repeat(16)),
            &format!("exec1_{}", "ab".repeat(15)),
            &format!("exec2_{}", "ab".repeat(16)),
            &format!("exec1_{}a", "ab".repeat(16)),
        ] {
            assert_eq!(parse_execution_id(unlawful), None, "{unlawful}");
        }
        let identity = RequestIdentity::draw().unwrap();
        let rendered = render_id("req1_", &identity.bytes());
        assert_eq!(rendered.len(), 37);
        assert_eq!(
            format!("{identity:?}"),
            format!("RequestIdentity({rendered:?})")
        );
        assert_ne!(RequestIdentity::draw().unwrap().bytes(), identity.bytes());
    }
}

// Law CI r5 item 4 (unit CI-2): the component store's charged native
// primitives, P-1 to P-7. Implemented on macOS only; every other target
// refuses before any native call.
#[cfg(any(target_os = "macos", target_os = "linux"))]
#[allow(unsafe_code)]
pub mod component_tree;
