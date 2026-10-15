// Law X1 r1 items 2 to 7 (unit X1a): the ordinary writer's admission. A
// writer that is not a creator produces the write receipt (item 1), the
// same composition as the read side's with only its purpose differing,
// rechecks it, enters the law 468 durable write gate with the receipt's
// sealed `DurableBarrierQualification` as the gate's only input, and
// rechecks the receipt again while the gate's fence is still held. A
// failed second recheck releases the fence: the writer never receives the
// installation. The admission grants exactly what `DurableInstallation`
// grants and nothing else: no store, trust, project, id, grant or commit
// standing. An absent I is `INSTALLATION.NOT_INITIALIZED` through the gate's
// positive absence; nothing is ever created on this path. Every refusal is
// its law 468 item 6 row through 468c's maps. Library only: no command is
// wired.
use super::first_registration::{
    self, ProjectInputs, ProjectWriteRefusal, RegisteredProject, Seam,
};
use super::git_tracking::TrackingObservation;
use super::installation_admission::{
    DurableBarrierQualification, DurableInstallation, DurableWriteGate, GateRefusal,
};
use super::project_admission::ProjectRootAdmission;
use super::installation_routing::gate_refusal;
use super::read_premise::{WritePlatformReceipt, produce_write_platform};
use super::store_endpoint::{SelectedStoreEndpoint, validate_endpoint};
use super::namespace_lease::{
    self, Failure as NamespaceFailure, FenceHolder, Held, NamespaceRefusal, NamespaceSubject,
    NamespaceTarget, WriterLease,
};
use super::operation_handoff::{OperationRefusal, ProjectOperation};
use super::project_admission::judged_registry;
use super::project_chain::ProjectChainPolicy;
use crate::InstallationTermination as T;
use crate::journal_store::CarrierRefusal;
use opensip_platform::{DescriptorFilesystem, WorkFailure, WorkScope};

/// Item 4: an admitted ordinary writer. Private, not Clone, no serialized
/// form, and no conversion into a read session. Dropped with the invocation.
pub(crate) struct OrdinaryWriteAdmission {
    installation: DurableInstallation,
    receipt: WritePlatformReceipt,
    /// The gate that admitted it, kept for its own ledger (law X3a item 7).
    gate: DurableWriteGate,
}
impl std::fmt::Debug for OrdinaryWriteAdmission {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("OrdinaryWriteAdmission")
            .field("installation", &self.installation)
            .finish_non_exhaustive()
    }
}
impl OrdinaryWriteAdmission {
    /// The held fence and the confirmed durability of I's and the
    /// I-parent's names, for the writer's own owner (X3a onwards).
    pub(crate) fn installation(&self) -> &DurableInstallation {
        &self.installation
    }
    /// The write receipt's actor, core and platform rechecks, for the
    /// writer's own owner. Charged to the attempt's ledger (item 5).
    pub(crate) fn recheck(&mut self) -> Result<(), T> {
        self.receipt.recheck()
    }
    /// Unlock the fence and close the retained handles. A failed unlock is
    /// the host I/O row, as the lock step's failures are.
    pub(crate) fn release(self) -> Result<(), T> {
        let Self { installation, .. } = self;
        installation.release().map_err(|error| {
            gate_refusal(&GateRefusal::Io(
                super::installation_admission::IoFailure::Lock(error),
            ))
        })
    }

    /// Spend the gate on a refusal; then, on success, the receipt's recheck
    /// while the fence is still held (a refusal of it spends the gate too).
    fn settle<R>(
        &mut self,
        result: Result<R, ProjectWriteRefusal>,
    ) -> Result<R, ProjectWriteRefusal> {
        let value = match result {
            Ok(value) => value,
            Err(refusal) => {
                self.gate.spend();
                return Err(refusal);
            }
        };
        if let Err(row) = self.receipt.recheck() {
            self.gate.spend();
            return Err(ProjectWriteRefusal::Receipt(row));
        }
        Ok(value)
    }
    /// Law X2 items 2 to 5 on this writer's gate (unit X2c): select and
    /// admit the project root with its registry classification, under the
    /// held fence, with the write receipt's premise. Grants nothing alone.
    pub(crate) fn admit_project_root(
        &mut self,
        launch: &std::path::Path,
        explicit: Option<&std::path::Path>,
        trust_groups: &std::collections::BTreeSet<u32>,
    ) -> Result<ProjectRootAdmission, ProjectWriteRefusal> {
        let result = first_registration::admit_on_gate(
            &mut self.gate,
            &self.installation,
            self.receipt.qualification(),
            launch,
            explicit,
            trust_groups,
        );
        self.settle(result)
    }
    /// M3-B unit B1-b on this writer's gate, the analysis path's first
    /// phase: the carriers before any registry read (X2 r9 item 3a).
    pub(crate) fn admit_project_carriers(
        &mut self,
        launch: &std::path::Path,
        explicit: Option<&std::path::Path>,
        trust_groups: &std::collections::BTreeSet<u32>,
        local: super::project_admission::LocalCarrierPolicy,
    ) -> Result<super::project_admission::CarrierAdmission, ProjectWriteRefusal> {
        let result = first_registration::admit_carriers_on_gate(
            &mut self.gate,
            &self.installation,
            self.receipt.qualification(),
            launch,
            explicit,
            trust_groups,
            local,
        );
        self.settle(result)
    }
    /// The analysis path's second phase on this writer's gate (X2 item 5).
    pub(crate) fn complete_project_admission(
        &mut self,
        carriers: super::project_admission::CarrierAdmission,
        trust_groups: &std::collections::BTreeSet<u32>,
    ) -> Result<ProjectRootAdmission, ProjectWriteRefusal> {
        let result = first_registration::complete_on_gate(
            &mut self.gate,
            &self.installation,
            self.receipt.qualification(),
            carriers,
            trust_groups,
        );
        self.settle(result)
    }
    /// Law X2 item 6a on this writer's gate, over the process environment
    /// and the fixed system sources.
    pub(crate) fn observe_project_tracking(
        &mut self,
        admission: &ProjectRootAdmission,
        trust_groups: &std::collections::BTreeSet<u32>,
    ) -> Result<TrackingObservation, ProjectWriteRefusal> {
        let (environment, sources) = first_registration::production_sources();
        let sources: Vec<&std::path::Path> = sources.iter().map(|p| p.as_path()).collect();
        let inputs = ProjectInputs {
            trust_groups,
            environment: &environment,
            system_sources: &sources,
        };
        self.observe_project_tracking_with(admission, &inputs)
    }
    /// `observe_project_tracking` over given inputs (the crate seam).
    pub(crate) fn observe_project_tracking_with(
        &mut self,
        admission: &ProjectRootAdmission,
        inputs: &ProjectInputs<'_>,
    ) -> Result<TrackingObservation, ProjectWriteRefusal> {
        let result = first_registration::observe_tracking_on_gate(
            &mut self.gate,
            &self.installation,
            self.receipt.qualification(),
            admission,
            inputs,
        );
        self.settle(result)
    }
    /// Law X2 item 6 (unit X2c): first registration of a FirstUseCandidate
    /// with its untracked observation, under this writer's held fence, over
    /// the process environment and the fixed system sources.
    pub(crate) fn register_first_use(
        &mut self,
        admission: ProjectRootAdmission,
        tracking: TrackingObservation,
        trust_groups: &std::collections::BTreeSet<u32>,
    ) -> Result<RegisteredProject, ProjectWriteRefusal> {
        let (environment, sources) = first_registration::production_sources();
        let sources: Vec<&std::path::Path> = sources.iter().map(|p| p.as_path()).collect();
        let inputs = ProjectInputs {
            trust_groups,
            environment: &environment,
            system_sources: &sources,
        };
        self.register_first_use_with(admission, tracking, &inputs, &Seam::live())
    }
    /// `register_first_use` over given inputs and seam (the crate seam;
    /// production passes `Seam::live()`).
    pub(crate) fn register_first_use_with(
        &mut self,
        admission: ProjectRootAdmission,
        tracking: TrackingObservation,
        inputs: &ProjectInputs<'_>,
        seam: &Seam<'_>,
    ) -> Result<RegisteredProject, ProjectWriteRefusal> {
        let result = first_registration::register_on_gate(
            &mut self.gate,
            &mut self.installation,
            self.receipt.qualification(),
            admission,
            tracking,
            inputs,
            seam,
        );
        self.settle(result)
    }
    /// A registered project's recheck set on this writer's gate.
    pub(crate) fn recheck_registered(
        &mut self,
        registered: &RegisteredProject,
        inputs: &ProjectInputs<'_>,
    ) -> Result<(), ProjectWriteRefusal> {
        let result = first_registration::recheck_registered_on_gate(
            &mut self.gate,
            &self.installation,
            self.receipt.qualification(),
            registered,
            inputs,
        );
        self.settle(result)
    }

    /// Law X2 item 7 (unit X2d): admit the namespace of an Eligible root
    /// (with its tracking observation) or of a project this writer has just
    /// registered, under this writer's held fence and on its gate's ledger.
    /// N is R's ACTIVE row's. No lock is taken: the target borrows this
    /// writer, and `NamespaceTarget::lease_writer` takes APPEND-WRITE or
    /// EXCLUSIVE. Any refusal spends the gate; the fence stays held.
    pub(crate) fn admit_namespace(
        &mut self,
        subject: NamespaceSubject,
        inputs: &ProjectInputs<'_>,
    ) -> Result<NamespaceTarget<&mut Self>, ProjectWriteRefusal> {
        namespace_lease::admit(self, subject, inputs)
    }

    /// Law X2 r8 item 7a (unit X2e, with X3b-3): the checked operation
    /// handoff. The selected store endpoint is joined from this gate's one
    /// read; the subject's namespace is admitted (X2d); X3b's floor step
    /// runs at the lease-free point; the lease is taken in `lease`; then,
    /// with the same fence held, the owners move into `ProjectOperation`,
    /// X3b's carrier start runs, and only then is the fence released. Any
    /// refusal spends the gate and releases every project lock, then the
    /// fence. One operation per writer: this consumes it.
    /// Law X4 r7 (unit X4a): `invocation` is the floor publication's
    /// invocation identity, and the operation carries X4's live guard.
    pub(crate) fn begin_operation(
        self,
        subject: NamespaceSubject,
        lease: WriterLease,
        inputs: &ProjectInputs<'_>,
        invocation: &crate::trust::TrustInvocation,
    ) -> Result<ProjectOperation, OperationRefusal> {
        super::operation_handoff::begin(
            self,
            subject,
            lease,
            inputs,
            invocation,
            super::operation_guard::GuardSeam::live(),
        )
    }
    /// `begin_operation` over a scripted guard seam (clock and cadence).
    #[cfg(test)]
    pub(crate) fn begin_operation_with(
        self,
        subject: NamespaceSubject,
        lease: WriterLease,
        inputs: &ProjectInputs<'_>,
        invocation: &crate::trust::TrustInvocation,
        seam: super::operation_guard::GuardSeam,
    ) -> Result<ProjectOperation, OperationRefusal> {
        super::operation_handoff::begin(self, subject, lease, inputs, invocation, seam)
    }
    /// Item 7a step 1's endpoint half (law X3a r5 items 1 and 2, unit X2e):
    /// the selected store endpoint validated from the gate's one read on its
    /// own ledger, then the gate's recheck and the receipt's, with the
    /// fence held. Unlike `admit_store_endpoint` this keeps the writer for
    /// the namespace steps; a refusal spends the gate, and dropping the
    /// writer releases the fence.
    pub(super) fn join_store_endpoint(&mut self) -> Result<(), T> {
        if self.gate.is_spent() {
            return Err(T::Invariant);
        }
        let (closure, writer) = {
            let (closure, writer) = self.receipt.selected_core();
            (closure.to_owned(), writer)
        };
        let checked = self
            .gate
            .charged(|work| validate_endpoint(self.installation.endpoint(), &closure, writer, work))
            .and_then(|()| {
                self.gate
                    .recheck(&self.installation, self.receipt.qualification())
            })
            .map_err(|refusal| gate_refusal(&refusal))
            .and_then(|()| self.receipt.recheck());
        if checked.is_err() {
            self.gate.spend();
        }
        checked
    }
    /// Unit X2e with X3b-3: one X3b step under this writer's held fence,
    /// charged to the write receipt's attempt ledger (X3b r10 item 9's
    /// operation ledger), then the gate's full recheck and the receipt's,
    /// still under the fence. Any refusal spends the gate too.
    pub(super) fn attempt_step<R>(
        &mut self,
        action: impl FnOnce(
            &DurableInstallation,
            &mut WorkScope<'_>,
        ) -> Result<R, WorkFailure<CarrierRefusal>>,
    ) -> Result<R, OperationRefusal> {
        if self.gate.is_spent() {
            return Err(OperationRefusal::Project(ProjectWriteRefusal::Latched));
        }
        let installation = &self.installation;
        let value = match self.receipt.charge(|_, work| action(installation, work)) {
            Ok(value) => value,
            Err(failure) => {
                self.gate.spend();
                return Err(OperationRefusal::Carrier(failure));
            }
        };
        let rechecked = self
            .gate
            .recheck(&self.installation, self.receipt.qualification())
            .map_err(ProjectWriteRefusal::Gate);
        self.settle(rechecked).map_err(OperationRefusal::Project)?;
        Ok(value)
    }
    /// Law X4 r7 items 2 and 9 (unit X4a): one step at the lease-free point
    /// on the gate's own ledger with the fence held (the fenced trust
    /// admission is charged there, never to a lease-held ledger). The
    /// installation is lent mutably so that a confirmed trust publication can
    /// advance its retained `state.v1` owner; then the gate's full recheck
    /// and the receipt's run, still under the fence. Any refusal spends the
    /// gate; a step refusal is returned as the step's own. X4B r5 item 2
    /// (unit X4B-b): the receipt's bootstrap source is lent beside the
    /// qualification, for the fenced first read's F-absent branch only.
    pub(super) fn gate_step<R, E>(
        &mut self,
        action: impl FnOnce(
            &mut DurableInstallation,
            &dyn super::installation_admission::DurableBarrierQualification,
            &crate::trust::BootstrapSource<'_>,
            &mut WorkScope<'_>,
        ) -> Result<R, WorkFailure<E>>,
    ) -> Result<R, GateStep<E>> {
        if self.gate.is_spent() {
            return Err(GateStep::Gate(ProjectWriteRefusal::Latched));
        }
        let Self {
            installation,
            receipt,
            gate,
        } = self;
        let qualification = receipt.qualification();
        let bootstrap = receipt.bootstrap_source();
        let value = match gate.scope(|work| action(installation, qualification, &bootstrap, work)) {
            Ok(value) => value,
            Err(failure) => {
                gate.spend();
                return Err(GateStep::Step(failure));
            }
        };
        let rechecked = gate
            .recheck(installation, qualification)
            .map_err(ProjectWriteRefusal::Gate);
        self.settle(rechecked).map_err(GateStep::Gate)?;
        Ok(value)
    }
    /// The write receipt's selected core closure (law X4T r9 item 4: the
    /// closure's release subject). Values only.
    pub(super) fn selected_closure(&self) -> String {
        self.receipt.selected_core().0.to_owned()
    }
    /// Item 7a step 2 (unit X2e): the writer's owners moved apart. The
    /// installation still holds the fence.
    pub(super) fn into_parts(
        self,
    ) -> (DurableInstallation, WritePlatformReceipt, DurableWriteGate) {
        let Self {
            installation,
            receipt,
            gate,
        } = self;
        (installation, receipt, gate)
    }

    /// Law X3a r3 items 1 and 2: admit the selected store endpoint from the
    /// gate's one read. The retained values are validated in memory on the
    /// gate's own ledger against the write receipt's selected core, then the
    /// gate's full recheck and the receipt's recheck run, still under the
    /// held fence. No file is read. A refusal releases the fence; the
    /// refusal's row stays the cause.
    pub(crate) fn admit_store_endpoint(self) -> Result<StoreAdmittedWriter, T> {
        let Self {
            installation,
            mut receipt,
            mut gate,
        } = self;
        let (closure, writer) = {
            let (closure, writer) = receipt.selected_core();
            (closure.to_owned(), writer)
        };
        let checked = gate
            .charged(|work| validate_endpoint(installation.endpoint(), &closure, writer, work))
            .and_then(|()| gate.recheck(&installation, receipt.qualification()))
            .map_err(|refusal| gate_refusal(&refusal))
            .and_then(|()| receipt.recheck());
        if let Err(row) = checked {
            let _ = installation.release();
            return Err(row);
        }
        Ok(StoreAdmittedWriter {
            admission: Self {
                installation,
                receipt,
                gate,
            },
        })
    }
}

/// A `gate_step` refusal: the step's own, or the gate's or the receipt's
/// recheck after it.
#[derive(Debug)]
pub(super) enum GateStep<E> {
    Step(WorkFailure<E>),
    Gate(ProjectWriteRefusal),
}

/// Law X2 item 7 (unit X2d): the writer's gate holds the fence for its
/// namespace steps. Each step runs on the gate's one ledger with the write
/// receipt's premise, then the gate's full recheck, then the receipt's
/// recheck (`settle`), all while the fence is held. Any refusal spends the
/// gate and drops what the step returned, so no project lock outlives it.
impl FenceHolder for &mut OrdinaryWriteAdmission {
    type Refusal = ProjectWriteRefusal;
    fn fenced<R>(
        &mut self,
        inputs: &ProjectInputs<'_>,
        action: impl FnOnce(&Held<'_, '_>, &mut WorkScope<'_>) -> Result<R, NamespaceFailure>,
    ) -> Result<R, ProjectWriteRefusal> {
        let writer: &mut OrdinaryWriteAdmission = self;
        if writer.gate.is_spent() {
            return Err(ProjectWriteRefusal::Latched);
        }
        let result = {
            let OrdinaryWriteAdmission {
                installation,
                receipt,
                gate,
            } = &mut *writer;
            let qualification = receipt.qualification();
            let home_filesystem =
                |sample: &DescriptorFilesystem| qualification.is_home_filesystem(sample);
            let policy = ProjectChainPolicy::new(
                qualification.omission_premise(),
                &home_filesystem,
                inputs.trust_groups,
            );
            match judged_registry(installation.required()) {
                None => Err(ProjectWriteRefusal::Namespace(WorkFailure::Operation(
                    NamespaceRefusal::Invariant("no-registry"),
                ))),
                Some(judged) => {
                    let held = Held {
                        installation: installation.installation_directory(),
                        uid: installation.uid(),
                        home: installation.home_spelling(),
                        judged,
                        policy: &policy,
                        inputs,
                        durable: Some(installation),
                    };
                    gate.scope(|work| action(&held, work))
                        .map_err(ProjectWriteRefusal::Namespace)
                        .and_then(|value| {
                            gate.recheck(installation, qualification)
                                .map_err(ProjectWriteRefusal::Gate)?;
                            Ok(value)
                        })
                }
            }
        };
        writer.settle(result)
    }
}

/// An ordinary writer whose selected store endpoint is admitted (law X3a
/// item 1). Private, not Clone. It grants only the endpoint: no namespace,
/// lease, journal, ledger, blob or commit authority.
pub(crate) struct StoreAdmittedWriter {
    admission: OrdinaryWriteAdmission,
}
impl std::fmt::Debug for StoreAdmittedWriter {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        f.debug_struct("StoreAdmittedWriter")
            .field("endpoint", &self.endpoint())
            .finish_non_exhaustive()
    }
}
impl StoreAdmittedWriter {
    pub(crate) fn endpoint(&self) -> SelectedStoreEndpoint<'_> {
        SelectedStoreEndpoint::new(self.admission.installation.endpoint())
    }
    pub(crate) fn installation(&self) -> &DurableInstallation {
        &self.admission.installation
    }
    pub(crate) fn release(self) -> Result<(), T> {
        self.admission.release()
    }
}

/// Item 2 on the native account's I: the write receipt, its recheck, the
/// gate, and the receipt's recheck again under the held fence. One entry
/// per process (item 7): the process's one attempt and one gate.
pub(crate) fn admit_ordinary_writer() -> Result<OrdinaryWriteAdmission, T> {
    let receipt = produce_write_platform()?;
    admit_receipt(receipt)
}

/// Law X1 r2 item 7 (J1 S3, item 3 step 3b.4; unit J3a): the creator-class
/// sequence's one ordinary admission, on attempt B. Item 2's steps 1 to 4
/// exactly as `admit_ordinary_writer`'s, with fresh producers, except that
/// step 1's attempt is the second slot, allocated by consuming the creator
/// act's `CreatorActEnded`. The gate is the process's one gate, which the
/// creator act never entered (468 r6 item 1).
pub(crate) fn admit_ordinary_writer_after(
    ended: super::installation_routing::CreatorActEnded,
) -> Result<OrdinaryWriteAdmission, T> {
    let receipt = super::read_premise::produce_write_platform_after(ended)?;
    admit_receipt(receipt)
}

/// Item 2's steps 2 to 4 on the native account's I, for a write receipt:
/// its recheck, the process's one gate, and its recheck again under the
/// held fence. J1 item 3's steady-state route (3a) runs exactly these on
/// attempt A's sealed receipt (X1 r2 item 1).
pub(super) fn admit_receipt(receipt: WritePlatformReceipt) -> Result<OrdinaryWriteAdmission, T> {
    admit_with(
        receipt,
        WritePlatformReceipt::recheck,
        DurableWriteGate::begin,
        |gate, receipt| gate.admit(receipt.qualification()),
    )
}

/// The composition over its seams. Production passes the receipt's own
/// recheck, the process's one gate and the native admission; tests pass the
/// same over scratch homes, or a scripted recheck refusal.
pub(super) fn admit_with(
    mut receipt: WritePlatformReceipt,
    mut recheck: impl FnMut(&mut WritePlatformReceipt) -> Result<(), T>,
    begin: impl FnOnce() -> Result<DurableWriteGate, GateRefusal>,
    admit: impl FnOnce(
        &mut DurableWriteGate,
        &WritePlatformReceipt,
    ) -> Result<DurableInstallation, GateRefusal>,
) -> Result<OrdinaryWriteAdmission, T> {
    // Step 2: the standing that lends the qualification holds before it.
    recheck(&mut receipt)?;
    // Step 3: 468 item 3 steps 0 to 5, unchanged; the gate's own ledger.
    let mut gate = begin().map_err(|r| gate_refusal(&r))?;
    let installation = admit(&mut gate, &receipt).map_err(|r| gate_refusal(&r))?;
    // Step 4: and still holds while the fence is held. A refusal releases
    // the fence before returning; the recheck's row stays the cause.
    if let Err(row) = recheck(&mut receipt) {
        let _ = installation.release();
        return Err(row);
    }
    Ok(OrdinaryWriteAdmission {
        installation,
        receipt,
        gate,
    })
}

#[cfg(test)]
mod tests {
    include!("ordinary_writer_tests.rs");
}
