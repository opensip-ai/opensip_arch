// Law 458c r5 items 1 to 4 (unit 458c-a): the read side's premise receipt.
// A read command that must open I produces the same receipts the creator
// produces, and only those: the process's one attempt, the actor,
// InitialCore and InitialPlatform. It mints no intent and makes no storage
// choice, disclosure, preparation, permit, stage or effect, and takes no
// fence. The receipt is private, not Clone and not serializable; it holds
// the attempt it was produced on and is dropped with the invocation. Its
// only lending is the sealed `ReadPremiseQualification`, which
// `InitialPlatform` alone implements: the check that a filesystem is H's and
// the omission premise with 465 item 4's scope. No barrier policy. Every
// refusal ends in its law 468 item 6 row through 468c's per-family maps; no
// row is added. The observation path is 458c-b's.
//
// Law X1 r1 items 1 and 2 (unit X1a): the same receipt, typed by purpose.
// One producer composition makes `PlatformReceipt<Read>` (the receipt
// above, unchanged) or `PlatformReceipt<Write>`, whose only lending is the
// durable write gate's sealed `DurableBarrierQualification`. Neither can be
// converted into the other, and the attempt stays private to both. Library
// only.
use super::installation_admission::DurableBarrierQualification;
use super::installation_routing::{
    actor_refusal, attempt_error, core_refusal, platform_refusal, work,
};
use crate::InstallationTermination as T;
use crate::initial_installation::{
    ActorRefusal, AttemptError, InitialActor, InitialInstallationAttempt,
};
use crate::trust::{
    AclOmissionPremise, InitialCore, InitialCoreRefusal, InitialPlatform, InitialPlatformRefusal,
    StateWriter, produce_initial_core, produce_initial_platform,
};
use opensip_platform::{DescriptorFilesystem, WorkFailure};

mod sealed {
    pub trait Sealed {}
}
/// Item 2: what the read side borrows from this invocation's
/// `InitialPlatform`. Sealed: only `InitialPlatform` implements it, so no
/// caller can build one. It lends exactly the check that a filesystem is
/// H's and the omission premise, and grants no standing. No read path takes
/// a barrier, so it lends no barrier policy.
pub(crate) trait ReadPremiseQualification: sealed::Sealed {
    fn is_home_filesystem(&self, sample: &DescriptorFilesystem) -> bool;
    /// Evidence B, with 465 item 4's scope (item 3): the root-to-H prefix,
    /// `Library` and `Application Support`, only through its own `fstatfs`.
    fn omission_premise(&self) -> Option<&AclOmissionPremise>;
}
impl sealed::Sealed for InitialPlatform {}
impl ReadPremiseQualification for InitialPlatform {
    fn is_home_filesystem(&self, sample: &DescriptorFilesystem) -> bool {
        self.qualifies_installation_filesystem(sample)
    }
    fn omission_premise(&self) -> Option<&AclOmissionPremise> {
        self.acl_omission_premise()
    }
}

mod purpose {
    pub trait Sealed {
        const NAME: &'static str;
    }
}
/// X1 item 1: the purpose a receipt was produced for, fixed by the entry
/// that produced it. Sealed: `Read` and `Write` are the only purposes.
pub(crate) trait Purpose: purpose::Sealed {}
/// The read side's purpose (458c): lends `ReadPremiseQualification`.
#[derive(Debug)]
pub(crate) enum Read {}
/// An ordinary writer's purpose (X1): lends `DurableBarrierQualification`.
#[derive(Debug)]
pub(crate) enum Write {}
impl purpose::Sealed for Read {
    const NAME: &'static str = "ReadPremiseReceipt";
}
impl purpose::Sealed for Write {
    const NAME: &'static str = "WritePlatformReceipt";
}
impl Purpose for Read {}
impl Purpose for Write {}

/// Item 1: the platform receipt. It holds the attempt it was produced on,
/// so its work stays on that attempt's one ledger and nothing outlives the
/// invocation. No intent can be minted through it: the attempt is private.
/// Not Clone, not serializable, and not convertible between purposes.
pub(crate) struct PlatformReceipt<P: Purpose> {
    attempt: InitialInstallationAttempt,
    actor: InitialActor,
    core: InitialCore,
    platform: InitialPlatform,
    purpose: std::marker::PhantomData<fn() -> P>,
}
/// 458c's read receipt.
pub(crate) type ReadPremiseReceipt = PlatformReceipt<Read>;
/// X1's write receipt.
pub(crate) type WritePlatformReceipt = PlatformReceipt<Write>;

impl<P: Purpose> std::fmt::Debug for PlatformReceipt<P> {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct(<P as purpose::Sealed>::NAME)
            .finish_non_exhaustive()
    }
}
impl<P: Purpose> PlatformReceipt<P> {
    /// The actor, core and platform rechecks on the receipt's own attempt.
    /// Any refusal latches the attempt and ends in its item 6 row.
    pub(crate) fn recheck(&mut self) -> Result<(), T> {
        ReceiptRecheck {
            attempt: &mut self.attempt,
            actor: &self.actor,
            core: &self.core,
            platform: &self.platform,
        }
        .recheck()
    }
    /// Law X3a item 1: the selected core's closure and state writer K, which
    /// the store endpoint's pair must name. Values only: no standing.
    pub(crate) fn selected_core(&self) -> (&str, StateWriter) {
        (self.core.closure(), self.core.state_writer())
    }
    /// Law X3d r8 item 13: the selected core's evaluator closure (contract
    /// successor EC1), derived from the same authenticated inventory as
    /// `selected_core`'s closure. A value only: no standing.
    pub(crate) fn core_evaluator_closure(&self) -> &str {
        self.core.evaluator_closure()
    }
    /// Law X3d r8 item 13: the shared test-support read of the core
    /// evaluator closure's preimages (`CommitSession`'s accessor), through
    /// this receipt's `InitialCore`. On X8 r3 item 4b's one site list.
    #[cfg(any(test, feature = "crash-matrix", feature = "scenario-fixtures"))]
    pub(crate) fn core_evaluator_closure_preimages(
        &self,
    ) -> (
        opensip_identity::JsonValue,
        Vec<u8>,
        std::collections::BTreeMap<String, Vec<u8>>,
    ) {
        self.core.evaluator_closure_preimages()
    }
}

/// Which purpose lends which sealed qualification. Each lending method below
/// exists only on the receipt type that carries its marker, so the markers
/// are the type-level record of X1 item 1, pinned by the tests.
pub(crate) trait LendsReadPremise {}
pub(crate) trait LendsBarrier {}
impl LendsReadPremise for PlatformReceipt<Read> {}
impl LendsBarrier for PlatformReceipt<Write> {}

impl PlatformReceipt<Read>
where
    Self: LendsReadPremise,
{
    /// The item 2 lending, and nothing else of the platform receipt.
    pub(crate) fn qualification(&self) -> &impl ReadPremiseQualification {
        &self.platform
    }
    /// The lending and the rechecks together, for an observation session
    /// (458c-b) that holds the lending across its steps and rechecks the
    /// receipt under its fence. Nothing else of the receipt is exposed.
    pub(crate) fn split(&mut self) -> (&impl ReadPremiseQualification, ReceiptRecheck<'_>) {
        (
            &self.platform,
            ReceiptRecheck {
                attempt: &mut self.attempt,
                actor: &self.actor,
                core: &self.core,
                platform: &self.platform,
            },
        )
    }
}

impl PlatformReceipt<Write>
where
    Self: LendsBarrier,
{
    /// X1 item 1: the write receipt's only lending, the durable write gate's
    /// sealed qualification (468 item 2's three things), through this
    /// invocation's `InitialPlatform`.
    pub(crate) fn qualification(&self) -> &impl DurableBarrierQualification {
        &self.platform
    }
    /// Law X4B r5 item 2 (unit X4B-b): the first trust acceptance's only
    /// payload source, the running core's embedded bootstrap through this
    /// receipt's `InitialCore`. Lent to the fenced first read alone; a read
    /// receipt has no such lending, so a read-only command never bootstraps.
    pub(crate) fn bootstrap_source(&self) -> crate::trust::BootstrapSource<'_> {
        crate::trust::BootstrapSource::running_core(&self.core)
    }
    /// Law X3b r10 item 9 (unit X2e with X3b-3): one charged step on this
    /// receipt's attempt ledger, the operation ledger of X3b, X3d and X4,
    /// with the same lending as `qualification` beside it. Refused `Closed`
    /// once the attempt is latched; any failure latches it for good (X1
    /// item 5's ledger, the platform's failure latch).
    pub(crate) fn charge<R, E>(
        &mut self,
        action: impl FnOnce(
            &dyn DurableBarrierQualification,
            &mut opensip_platform::WorkScope<'_>,
        ) -> Result<R, WorkFailure<E>>,
    ) -> Result<R, WorkFailure<E>> {
        let platform = &self.platform;
        self.attempt.run(|work| action(platform, work))
    }
    /// Law X4 r7 item 4 (unit X4a): `charge` with the receipt's own rechecks
    /// lent beside the lending, so that the checkpoint's write-receipt guard
    /// runs on this same attempt ledger inside the same charged step: the
    /// actor, the core and the platform, as `recheck` runs them. A refusal of
    /// either latches the attempt, as `recheck`'s does.
    pub(crate) fn charge_guarded<R, E>(
        &mut self,
        action: impl FnOnce(
            &dyn DurableBarrierQualification,
            &ReceiptGuard<'_>,
            &mut opensip_platform::WorkScope<'_>,
        ) -> Result<R, WorkFailure<E>>,
    ) -> Result<R, WorkFailure<E>> {
        let guard = ReceiptGuard {
            actor: &self.actor,
            core: &self.core,
            platform: &self.platform,
        };
        let platform = &self.platform;
        self.attempt.run(|work| action(platform, &guard, work))
    }
    /// Law X3d r6 item 8 (unit X3d-1): the attempt ledger's settlement
    /// reserve, on the commit session's end-path step's way only.
    pub(crate) fn reserve_end_path_settlement(
        &mut self,
        cost: opensip_platform::WorkCost,
    ) -> Result<opensip_platform::SettlementReserve, opensip_platform::WorkBudgetError> {
        self.attempt.reserve_end_path_settlement(cost)
    }
    /// Law X3d r6 item 8 (unit X3d-1): spend it once, on
    /// `StoppedSession::finish`'s way only, with the same lending as
    /// `charge` beside it.
    pub(crate) fn settle_end_path<R, E>(
        &mut self,
        reserve: opensip_platform::SettlementReserve,
        action: impl FnOnce(&mut opensip_platform::WorkScope<'_>) -> Result<R, WorkFailure<E>>,
    ) -> Result<R, WorkFailure<E>> {
        self.attempt.settle_end_path(reserve, action)
    }
    /// Whether the attempt ledger is closed: every later charge refuses.
    pub(crate) fn is_closed(&self) -> bool {
        self.attempt.is_latched()
    }
    /// The attempt ledger's use so far, for budget tests.
    #[cfg(test)]
    pub(crate) fn attempt_used(&self) -> opensip_platform::WorkCost {
        self.attempt.used()
    }
}
/// The write receipt's rechecks on a borrowed scope of its own attempt
/// ledger (law X4 r7 item 4, unit X4a). Not Clone; lent only by
/// `charge_guarded`.
pub(crate) struct ReceiptGuard<'a> {
    actor: &'a InitialActor,
    core: &'a InitialCore,
    platform: &'a InitialPlatform,
}
impl ReceiptGuard<'_> {
    /// The actor, core and platform rechecks, charged to `work`; a refusal
    /// is its law 468 item 6 row.
    pub(crate) fn recheck_in(
        &self,
        work: &mut opensip_platform::WorkScope<'_>,
    ) -> Result<(), WorkFailure<T>> {
        fn row<E>(failure: WorkFailure<E>, map: impl FnOnce(&E) -> T) -> WorkFailure<T> {
            match failure {
                WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
                WorkFailure::Operation(refusal) => WorkFailure::Operation(map(&refusal)),
            }
        }
        crate::initial_installation::recheck_actor_in(self.actor, work)
            .map_err(|f| row(f, actor_refusal))?;
        self.core
            .recheck_in(work)
            .map_err(|f| row(f, core_refusal))?;
        self.platform
            .recheck_in(work)
            .map_err(|f| row(f, platform_refusal))
    }
}
/// The receipt's rechecks, borrowed alongside its lending. Not Clone.
pub(crate) struct ReceiptRecheck<'a> {
    attempt: &'a mut InitialInstallationAttempt,
    actor: &'a InitialActor,
    core: &'a InitialCore,
    platform: &'a InitialPlatform,
}
impl ReceiptRecheck<'_> {
    pub(crate) fn recheck(&mut self) -> Result<(), T> {
        self.attempt
            .recheck_actor(self.actor)
            .map_err(|f| work(&f, actor_refusal))?;
        self.core
            .recheck(self.attempt)
            .map_err(|f| work(&f, core_refusal))?;
        self.platform
            .recheck(self.attempt)
            .map_err(|f| work(&f, platform_refusal))
    }
}

/// Items 1 and 4: allocate the process's one attempt, admit the actor, then
/// produce InitialCore and InitialPlatform on it. A development build ends
/// at InitialCore F0 (`CORE.NO_EMBEDDED_RELEASE`) before any path is
/// opened. An admitted receipt without a premise is not a refusal.
pub(crate) fn produce_read_platform() -> Result<ReadPremiseReceipt, T> {
    produce_for(
        InitialInstallationAttempt::begin(),
        InitialInstallationAttempt::observe_actor,
        produce_initial_core,
        produce_initial_platform,
    )
}

/// X1 items 1 and 2: the same composition for an ordinary writer. Only the
/// purpose differs; there is no second producer.
pub(crate) fn produce_write_platform() -> Result<WritePlatformReceipt, T> {
    produce_for(
        InitialInstallationAttempt::begin(),
        InitialInstallationAttempt::observe_actor,
        produce_initial_core,
        produce_initial_platform,
    )
}

/// The read composition over its producers (458c-a's seam, unchanged).
pub(super) fn produce_on(
    begun: Result<InitialInstallationAttempt, AttemptError>,
    actor: impl FnOnce(
        &mut InitialInstallationAttempt,
    ) -> Result<InitialActor, WorkFailure<ActorRefusal>>,
    core: impl FnOnce(
        &mut InitialInstallationAttempt,
    ) -> Result<InitialCore, WorkFailure<InitialCoreRefusal>>,
    platform: impl FnOnce(
        &mut InitialInstallationAttempt,
        &InitialActor,
        &InitialCore,
    ) -> Result<InitialPlatform, WorkFailure<InitialPlatformRefusal>>,
) -> Result<ReadPremiseReceipt, T> {
    produce_for(begun, actor, core, platform)
}

/// Law X1 r2 item 1 (J1 S3; unit J3a): the write receipt on the
/// creator-class sequence's attempt B, which `ended` allocates. The same
/// composition as `produce_write_platform`; only the attempt's slot differs.
pub(crate) fn produce_write_platform_after(
    ended: super::installation_routing::CreatorActEnded,
) -> Result<WritePlatformReceipt, T> {
    produce_for(
        InitialInstallationAttempt::begin_after(ended),
        InitialInstallationAttempt::observe_actor,
        produce_initial_core,
        produce_initial_platform,
    )
}

/// The one composition, over its producers, for either purpose. Production
/// passes exactly the creator's; tests pass the same producers over signed
/// test trees.
pub(crate) fn produce_for<P: Purpose>(
    begun: Result<InitialInstallationAttempt, AttemptError>,
    actor: impl FnOnce(
        &mut InitialInstallationAttempt,
    ) -> Result<InitialActor, WorkFailure<ActorRefusal>>,
    core: impl FnOnce(
        &mut InitialInstallationAttempt,
    ) -> Result<InitialCore, WorkFailure<InitialCoreRefusal>>,
    platform: impl FnOnce(
        &mut InitialInstallationAttempt,
        &InitialActor,
        &InitialCore,
    ) -> Result<InitialPlatform, WorkFailure<InitialPlatformRefusal>>,
) -> Result<PlatformReceipt<P>, T> {
    produce_unsealed(begun, actor, core, platform).map(Producers::seal)
}

/// Law X1 r2 item 1 (J1 S3; unit J3a): one attempt's producers before any
/// purpose is fixed, for J1 item 3's durable creator-class entry, which runs
/// the presence probe on them first. On `Present` they are sealed as the
/// write receipt; on `PositivelyAbsent` they serve the creator act unsealed
/// and are dropped with it, so they never become a receipt. Private fields,
/// not Clone and not serializable; no conversion but `seal`.
pub(crate) struct Producers {
    pub(super) attempt: InitialInstallationAttempt,
    pub(super) actor: InitialActor,
    pub(super) core: InitialCore,
    pub(super) platform: InitialPlatform,
}
impl std::fmt::Debug for Producers {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("Producers").finish_non_exhaustive()
    }
}
impl Producers {
    /// Fix the purpose: the receipt, which no later step converts.
    pub(crate) fn seal<P: Purpose>(self) -> PlatformReceipt<P> {
        let Self {
            attempt,
            actor,
            core,
            platform,
        } = self;
        PlatformReceipt {
            attempt,
            actor,
            core,
            platform,
            purpose: std::marker::PhantomData,
        }
    }
}

/// The one composition, unsealed: allocate the attempt, admit the actor,
/// then InitialCore and InitialPlatform on it, each bound to the attempt.
pub(crate) fn produce_unsealed(
    begun: Result<InitialInstallationAttempt, AttemptError>,
    actor: impl FnOnce(
        &mut InitialInstallationAttempt,
    ) -> Result<InitialActor, WorkFailure<ActorRefusal>>,
    core: impl FnOnce(
        &mut InitialInstallationAttempt,
    ) -> Result<InitialCore, WorkFailure<InitialCoreRefusal>>,
    platform: impl FnOnce(
        &mut InitialInstallationAttempt,
        &InitialActor,
        &InitialCore,
    ) -> Result<InitialPlatform, WorkFailure<InitialPlatformRefusal>>,
) -> Result<Producers, T> {
    let mut attempt = begun.map_err(|e| attempt_error(&e))?;
    let actor = actor(&mut attempt).map_err(|f| work(&f, actor_refusal))?;
    let core = core(&mut attempt).map_err(|f| work(&f, core_refusal))?;
    let platform = platform(&mut attempt, &actor, &core).map_err(|f| work(&f, platform_refusal))?;
    // Every receipt must be this attempt's; a foreign one is a broken caller.
    let lineages = [actor.lineage(), core.lineage(), platform.lineage()];
    if lineages.iter().any(|l| !attempt.require_lineage(*l)) {
        return Err(T::Invariant);
    }
    Ok(Producers {
        attempt,
        actor,
        core,
        platform,
    })
}

#[cfg(test)]
mod tests {
    include!("read_premise_tests.rs");
}
