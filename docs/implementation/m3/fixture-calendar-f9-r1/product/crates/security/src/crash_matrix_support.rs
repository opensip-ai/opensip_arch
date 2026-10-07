//! Law X9 r1 item 6 (unit X9-1): security's synthetic test-support surface
//! for the crash, lock and revocation matrix. It exists only under the
//! test-only `crash-matrix` feature (law X9 r1 item 2: no manifest enables
//! it, and a build without debug assertions refuses it), and it is
//! `#[doc(hidden)]`.
//!
//! It produces inputs on disk under a scratch root and returns paths,
//! values and outcomes only, never an authority type (`PlatformReceipt`,
//! `ProjectOperation`, `CommitSession`, `ReplayedRun`, `PreparedCommit`,
//! `PublishedCommit`, `RecoveredCommit`, `AdmissionPermit`). Those come from
//! the production paths over these inputs. Every item here is a thin caller
//! of a shared fixture site that X9-1 pins (`crash_matrix_sites.rs`):
//! - a synthetic installation through the real creator path, with
//!   InitialCore's injected loaded image and the synthetic V2 profile set
//!   (the shared installation fixture);
//! - X4T-0's signed accepted store, built from the public test-only quorum
//!   seeds, written in place;
//! - the revocation publication helper: the shared fenced `state.v1`
//!   publisher, which takes the installation fence by the write gate's walk
//!   and replaces `state.v1` by the trust owner's protocol;
//! - the inherited format-1 and format-2 carrier fixture;
//! - X3b-2's reserved-slot technique;
//! - (law X9 r4 item 6, unit X9-2) exactly three driver entries,
//!   [`operation`], [`recovery_admission`] and [`settlement_sweep`]: the one
//!   exception to "no authority type". Each returns only what an existing
//!   crate-private production composition returns over the fixture home,
//!   accepts no receipt, gate, guard, monitor, clock, session, permit or
//!   `ReplayedRun`, and constructs nothing itself. A process makes at most
//!   one call to any of the three (X1 items 1 and 7); a second refuses on
//!   the invariant row without effect, and `publish_revocation` refuses in a
//!   process that made one.
//!
//! Every run that uses it is labelled with `FIXTURE` and `PROFILE_STANDING`
//! (law X9 r1 item 6; build plan line 886: "synthetic fixtures remain
//! labelled, not compiler qualification"). Nothing here sleeps, polls or
//! waits on a timer.
use crate::InstallationTermination as T;
use crate::custody::installation_read_fixture::{InstallationAt, ReadFixture};
use crate::custody::operation_handoff::ProjectOperation;
use crate::custody::recovery_admission::{RecoveryAdmission, RecoveryRefusal, RecoveryRequest};
use crate::custody::settlement_sweep::SettlementSweep;
use crate::trust::ReadProducers;
use std::cell::RefCell;
use std::path::Path;
use std::sync::atomic::{AtomicBool, Ordering};

pub mod post_state;
pub mod run_record;

/// The fixture label every matrix run records.
pub const FIXTURE: &str = "synthetic-signed-v2";
/// The platform profile standing every matrix run records (law 469: this
/// host has no measured row).
pub const PROFILE_STANDING: &str = "BASELINE-ATTESTED";

/// A synthetic installation: a published P0 under a scratch H, made by the
/// real creator path over 462's signed test tree with the injected loaded
/// image and the synthetic V2 profile set with the ACL-omission premise.
/// The one `create` made owns its scratch tree and removes it on drop; one
/// `open`ed by its paths (in a matrix child) owns nothing. It holds paths
/// only.
pub struct SyntheticInstallation {
    at: InstallationAt,
    // The signed test trees of the entry this process made; they outlive
    // what the entry returned for as long as the installation value lives.
    trees: RefCell<Vec<ReadProducers>>,
    _owned: Option<ReadFixture>,
}
impl SyntheticInstallation {
    /// Publish a new installation; `tag` names its scratch tree.
    pub fn create(tag: &str) -> Self {
        let fixture = ReadFixture::new(tag);
        Self {
            at: fixture.at(),
            trees: RefCell::new(Vec::new()),
            _owned: Some(fixture),
        }
    }
    /// An installation another process published, by its paths.
    pub fn open(home: &Path, installation: &Path, store: &str) -> Self {
        Self {
            at: InstallationAt {
                home: home.to_owned(),
                installation: installation.to_owned(),
                store: store.to_owned(),
            },
            trees: RefCell::new(Vec::new()),
            _owned: None,
        }
    }
    /// The scratch H.
    pub fn home(&self) -> &Path {
        &self.at.home
    }
    /// I, under the scratch H.
    pub fn installation(&self) -> &Path {
        &self.at.installation
    }
    /// The store S the creator drew.
    pub fn store(&self) -> &str {
        &self.at.store
    }
    /// The revocation version of `trust/stores/S/state.v1`, read by name
    /// (0 for P0). Read-only.
    pub fn revocation_version(&self) -> Result<i128, String> {
        self.at.current_trust_values().map(|(_, version)| version)
    }
    /// X4T-0's signed accepted store for S, its roles Trusted, with these
    /// revocation entries (`(subjectKind, subject)`) and list version,
    /// written in place with no fence. Returns the core closure its P0
    /// names.
    pub fn install_accepted_trust(
        &self,
        revocations: Vec<(&'static str, String)>,
        revocation_version: i128,
    ) -> Result<&'static str, String> {
        self.at
            .install_accepted_trust(revocations, revocation_version, None)
    }
    /// The revocation publication helper (law X9 r1 items 6 and 11): the
    /// shared fenced publisher publishes X4T-0's store for S with these
    /// entries at `revocation_version` under the installation fence, then
    /// releases it. The calling process must hold no operation lease.
    pub fn publish_revocation(
        &self,
        revocations: Vec<(&'static str, String)>,
        revocation_version: i128,
    ) -> Result<RevocationVersions, String> {
        // Law X9 r4 item 6: never in a process that made a driver entry.
        if ENTERED.load(Ordering::SeqCst) {
            return Err("publish_revocation in a process that made a driver entry".into());
        }
        let (before, after) = self
            .at
            .publish_accepted_trust_fenced(revocations, revocation_version)?;
        Ok(RevocationVersions { before, after })
    }
}

/// The revocation version of `state.v1` before and after a publication.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct RevocationVersions {
    pub before: i128,
    pub after: i128,
}

/// The inherited carrier formats.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum InheritedFormat {
    One,
    Two,
}

/// Plant the inherited format-1 or format-2 carrier fixture as the carrier
/// of the namespace directory at `namespace` (X3b item 3a's F46 class;
/// matrix rows F31 and F46).
pub fn plant_inherited_carrier(namespace: &Path, format: InheritedFormat) {
    use crate::journal_store::InheritedFormat as F;
    crate::journal_store::plant_inherited_carrier_for_tests(
        namespace,
        match format {
            InheritedFormat::One => F::One,
            InheritedFormat::Two => F::Two,
        },
    );
}

/// X3b-2's reserved-slot technique: plant a committed `RA` at (1, `seq`)
/// in the carrier of the namespace directory at `namespace` (the append
/// trigger lifted and reinstalled byte-identically from its own stored
/// SQL), and the witness `COMMITTED` at it (matrix rows F32 and F43).
pub fn plant_committed_tail(namespace: &Path, namespace_id: &str, seq: i64) {
    crate::journal_store::plant_committed_tail_for_tests(namespace, namespace_id, seq);
}

// ------------------------------------------------- the three driver entries

/// Law X9 r4 item 6: set by the first driver entry of this process, never
/// cleared. The fixture seams each entry runs take a fresh attempt flag per
/// call, so this flag is what keeps X1 items 1 and 7's one entry.
static ENTERED: AtomicBool = AtomicBool::new(false);

/// Take this process's one entry, or refuse on the invariant row.
fn enter() -> bool {
    !ENTERED.swap(true, Ordering::SeqCst)
}

/// Law X9 r4 item 6: the production chain to `root`'s `ProjectOperation`
/// under an APPEND-WRITE lease, over the synthetic installation `at`: X1's
/// ordinary writer (`ordinary_writer::admit_with`, the write receipt over a
/// signed test tree, the gate over `HomeSource::Fixture`), X2's root
/// admission and tracking, the first registration when the root is
/// unregistered, then `begin_operation` (X2d, X3a, X4, X3b's floor step and
/// start, X2e's handoff). It is the one composition X8b's
/// `scenario::operation` also calls (`InstallationAt::operation`), and it
/// returns that composition's `ProjectOperation` or its row. A second entry
/// in this process refuses on the invariant row without effect.
pub fn operation(at: &SyntheticInstallation, root: &Path) -> Result<ProjectOperation, T> {
    if !enter() {
        return Err(T::Invariant);
    }
    let (operation, trees) = at.at.operation(
        root,
        crate::custody::namespace_lease::WriterLease::AppendWrite,
    )?;
    at.trees.borrow_mut().push(trees);
    Ok(operation)
}

/// Law X9 r4 item 6 (X6 r4 item 2): recovery's read entry over the
/// synthetic installation `at`. A read receipt over a signed test tree for
/// `at`'s H, recovery's one ledger allocated as `RecoveryAdmission::admit`
/// allocates it, then `recovery_admission::admit_on` over
/// `HomeSource::Fixture`. It returns that function's admission or refusal.
/// A second entry in this process refuses on the invariant row without
/// effect.
pub fn recovery_admission(
    at: &SyntheticInstallation,
    request: RecoveryRequest,
) -> Result<RecoveryAdmission, RecoveryRefusal> {
    use crate::custody::installation_admission::HomeSource;
    use crate::custody::read_premise::{Read, produce_for};
    use crate::custody::recovery_admission::{RECOVERY_ALLOCATED, admit_on, allocate};
    use crate::initial_installation::InitialInstallationAttempt;
    if !enter() {
        return Err(RecoveryRefusal::Row(T::Invariant));
    }
    let producers = crate::trust::read_producers(
        &format!("x9-recover-{}", at.at.store),
        true,
        Some(&at.at.home),
    );
    let mut receipt = produce_for::<Read>(
        InitialInstallationAttempt::for_tests(&AtomicBool::new(false), None),
        InitialInstallationAttempt::observe_actor,
        |attempt| producers.core(attempt),
        |attempt, actor, core| producers.platform(attempt, actor, core),
    )
    .map_err(RecoveryRefusal::Row)?;
    at.trees.borrow_mut().push(producers);
    let ledger = allocate(&RECOVERY_ALLOCATED, None)?;
    admit_on(
        &mut receipt,
        request,
        ledger,
        HomeSource::Fixture(&at.at.home),
        &mut || {},
    )
}

/// Law X9 r4 item 6 (X6 r4 item 7): the sweep's entry over the synthetic
/// installation `at`: X1's ordinary writer as `operation` admits it, then
/// `settlement_sweep::admit_on`. It returns that function's sweep or row.
/// A second entry in this process refuses on the invariant row without
/// effect.
pub fn settlement_sweep(at: &SyntheticInstallation) -> Result<SettlementSweep, T> {
    if !enter() {
        return Err(T::Invariant);
    }
    let (writer, trees) = at.at.admitted_writer().map_err(|(_, row)| row)?;
    at.trees.borrow_mut().push(trees);
    crate::custody::settlement_sweep::admit_on(writer)
}
