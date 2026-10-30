//! C2a-3: whole retained closure admission. Library only; no native entrypoint.
use crate::installation::ComponentStore;
use crate::retained_tree::{
    PinRequest, RetainedTree, TreeReadFailure, VerifiedSink, open_retained_tree,
};
use opensip_identity::RegisteredSchemas;
use opensip_platform::{WorkBudgetError, WorkCost, WorkFailure, WorkScope};
use opensip_security::{
    AnalyzerSubprotocol, AuthenticatedComponent, AuthenticatedCoreRole, AuthenticatedCoreRoles,
    ClosureCandidate, ClosureFailure, ClosureRefusal, CoreRole, SelectedPlatform,
    component_candidate, verify_retained_tree,
};

// The selected LP64 representation; other ABIs need a reviewed price first.
const _: () = assert!(std::mem::size_of::<usize>() == 8);
const _: () = assert!(std::mem::size_of::<Vec<u8>>() == 24);
const _: () = assert!(std::mem::size_of::<&str>() == 16);
const _: () = assert!(std::mem::size_of::<&[u8]>() == 16);

/// The only component payload: candidate identity plus actual pinned custody.
/// Its private constructor runs the full open/transfer/kernel chain.
pub struct AdmittedComponent<'store, 'borrow, 'manifest: 'borrow> {
    candidate: &'borrow ClosureCandidate<'manifest>,
    retained: RetainedTree<'store, 'borrow>,
}
impl<'store, 'borrow, 'manifest: 'borrow> AdmittedComponent<'store, 'borrow, 'manifest> {
    pub fn closure(&self) -> &str {
        self.candidate.closure()
    }
    pub fn descriptor(&self) -> &[u8] {
        self.candidate.descriptor()
    }
    /// The admitted owner's existing capability, never a reconstructed path.
    pub fn retained(&mut self) -> &mut RetainedTree<'store, 'borrow> {
        &mut self.retained
    }
}

/// Borrowed views duplicate neither custody nor authenticated core evidence.
pub enum AdmittedClosure<'owner, 'store, 'borrow, 'manifest: 'borrow> {
    Component(&'owner AdmittedComponent<'store, 'borrow, 'manifest>),
    Core(AuthenticatedCoreRole<'owner>),
}

/// Stable operation-owned candidate storage, funded only by prepare_slots.
/// No raw slice, resizing, prepopulation, cloning or extraction is public.
pub struct PreparedCandidateSlots<'input, 'manifest: 'input> {
    components: &'input [AuthenticatedComponent<'manifest>],
    slots: Vec<Option<ClosureCandidate<'manifest>>>,
    available: bool,
}

/// A single-use borrow of the privately paired component and slot slices.
/// Only its prepared owner mints it, and admission consumes it by value.
pub struct CandidateSlotClaim<'borrow, 'input: 'borrow, 'manifest: 'input> {
    components: &'input [AuthenticatedComponent<'manifest>],
    slots: &'borrow mut [Option<ClosureCandidate<'manifest>>],
}
impl<'input, 'manifest: 'input> PreparedCandidateSlots<'input, 'manifest> {
    pub fn claim<'borrow>(
        &'borrow mut self,
    ) -> Option<CandidateSlotClaim<'borrow, 'input, 'manifest>> {
        if !self.available {
            return None;
        }
        self.available = false;
        Some(CandidateSlotClaim {
            components: self.components,
            slots: &mut self.slots,
        })
    }
}

/// One operation's private admitted owners. Construction is all-or-nothing.
pub struct AdmittedSet<'store, 'borrow, 'manifest: 'borrow> {
    components: Vec<AdmittedComponent<'store, 'borrow, 'manifest>>,
    core: AuthenticatedCoreRoles,
}
impl<'store, 'borrow, 'manifest: 'borrow> AdmittedSet<'store, 'borrow, 'manifest> {
    /// The operation frame owns this storage outside the admitted set. It is
    /// initialized and funded once, before any candidate/capability borrow.
    pub fn prepare_slots<'input>(
        components: &'input [AuthenticatedComponent<'manifest>],
        work: &mut WorkScope<'_>,
    ) -> Result<PreparedCandidateSlots<'input, 'manifest>, ComponentAdmissionFailure>
    where
        'manifest: 'input,
    {
        work.scope(|scope| {
            let count = components.len();
            // Addendum map-r1: constructed once (no replaced live Vec). A
            // constant frame debit comes first, then the slot array and its
            // per-slot work; zero components charge and allocate nothing.
            let slots = if count == 0 {
                Vec::new()
            } else {
                scope.charge(WorkCost {
                    objects: 0,
                    edges: PREPARE_FIXED,
                    bytes: 64 * PREPARE_FIXED,
                })?;
                let bytes = mul(
                    count,
                    std::mem::size_of::<Option<ClosureCandidate<'manifest>>>(),
                )?;
                let edges = mul(PREPARE_SLOT, count)?;
                scope.charge(WorkCost {
                    objects: 1,
                    edges,
                    bytes: add(add(bytes, 128)?, mul(64, edges)?)?,
                })?;
                let mut slots = Vec::with_capacity(count);
                while slots.len() < count {
                    slots.push(None);
                }
                slots
            };
            Ok(PreparedCandidateSlots {
                components,
                slots,
                available: true,
            })
        })
        .map_err(public_failure)
    }

    /// Consume the only claim to the owner's privately paired slices.
    /// No completed capability escapes if any later component refuses.
    #[allow(
        clippy::too_many_arguments,
        reason = "the C2a-3 owning composition keeps its custody, authenticated inputs and borrowed scope explicit"
    )]
    pub fn admit<'input>(
        store: &'store ComponentStore,
        claim: CandidateSlotClaim<'borrow, 'input, 'manifest>,
        core: AuthenticatedCoreRoles,
        platform: SelectedPlatform<'_>,
        analyzer: Option<&AnalyzerSubprotocol>,
        registry: &RegisteredSchemas,
        pin: PinRequest,
        work: &mut WorkScope<'_>,
    ) -> Result<Self, ComponentAdmissionFailure>
    where
        'manifest: 'input,
        'input: 'borrow,
    {
        work.scope(|scope| {
            let CandidateSlotClaim { components, slots } = claim;
            let count = components.len();
            if count != 0 {
                scope.charge(WorkCost {
                    objects: 0,
                    edges: ADMIT_FIXED,
                    bytes: 64 * ADMIT_FIXED,
                })?;
                let bytes = mul(
                    count,
                    std::mem::size_of::<AdmittedComponent<'store, 'borrow, 'manifest>>(),
                )?;
                let edges = mul(ADMIT_COMPONENT, count)?;
                scope.charge(WorkCost {
                    objects: 1,
                    edges,
                    bytes: add(add(bytes, 128)?, mul(64, edges)?)?,
                })?;
            }
            let mut admitted = Vec::with_capacity(count);
            for (component, slot) in components.iter().zip(slots) {
                let candidate = slot.insert(
                    component_candidate(component, platform, analyzer, registry, scope)
                        .map_err(closure_input)?,
                );
                let payload =
                    admit_component_inner(store, component, candidate, platform, pin, scope)?;
                admitted.push(payload);
            }
            Ok(Self {
                components: admitted,
                core,
            })
        })
        .map_err(public_failure)
    }

    pub fn components(&self) -> &[AdmittedComponent<'store, 'borrow, 'manifest>] {
        &self.components
    }
    pub fn core(&self, role: CoreRole) -> AdmittedClosure<'_, 'store, 'borrow, 'manifest> {
        AdmittedClosure::Core(self.core.role(role))
    }
}

/// The operation frame's fixed and per-component work (addendum map-r1).
const PREPARE_FIXED: usize = 1024;
const PREPARE_SLOT: usize = 256;
const ADMIT_FIXED: usize = 2048;
const ADMIT_COMPONENT: usize = 1024;

/// Internal Rust failures, not serialized routes or caller-selected details.
#[derive(Debug)]
pub enum ComponentAdmissionFailure {
    Closure(ClosureRefusal),
    Tree(TreeReadFailure),
    Budget(WorkBudgetError),
    Invariant,
}
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
enum CollectorFault {
    Begin,
    Chunk,
    Length,
    Completion,
}
enum Fault {
    Closure(ClosureRefusal),
    Tree(TreeReadFailure),
    Collector(CollectorFault),
}
type Failure = WorkFailure<Fault>;

fn closure_input(error: ClosureFailure) -> Failure {
    match error {
        WorkFailure::Budget(budget) => WorkFailure::Budget(budget),
        WorkFailure::Operation(refusal) => WorkFailure::Operation(Fault::Closure(refusal)),
    }
}
fn tree_input(error: TreeReadFailure) -> Failure {
    match error {
        TreeReadFailure::Budget(budget) => WorkFailure::Budget(budget),
        cause @ (TreeReadFailure::NotInstalled
        | TreeReadFailure::Absent { .. }
        | TreeReadFailure::Length { .. }
        | TreeReadFailure::Digest { .. }
        | TreeReadFailure::Type { .. }
        | TreeReadFailure::Mode { .. }
        | TreeReadFailure::LinkTarget { .. }
        | TreeReadFailure::Extra { .. }
        | TreeReadFailure::Association
        | TreeReadFailure::Pin
        | TreeReadFailure::Custody(_)
        | TreeReadFailure::Binding
        | TreeReadFailure::Io { .. }) => WorkFailure::Operation(Fault::Tree(cause)),
    }
}
fn public_failure(error: Failure) -> ComponentAdmissionFailure {
    match error {
        WorkFailure::Budget(budget) => ComponentAdmissionFailure::Budget(budget),
        WorkFailure::Operation(Fault::Closure(refusal)) => {
            ComponentAdmissionFailure::Closure(refusal)
        }
        WorkFailure::Operation(Fault::Tree(cause)) => ComponentAdmissionFailure::Tree(cause),
        WorkFailure::Operation(Fault::Collector(_)) => ComponentAdmissionFailure::Invariant,
    }
}
fn arithmetic() -> Failure {
    WorkFailure::Budget(WorkBudgetError::Arithmetic)
}
fn add(left: usize, right: usize) -> Result<usize, Failure> {
    left.checked_add(right).ok_or_else(arithmetic)
}
fn mul(left: usize, right: usize) -> Result<usize, Failure> {
    left.checked_mul(right).ok_or_else(arithmetic)
}

/// Fund the representation block before retaining any bytes (addendum
/// map-r1): fixed, scan, then the checked remainder. CI open, transfer and
/// the kernel continue charging their own work independently.
fn fund_representation(
    candidate: &ClosureCandidate<'_>,
    work: &mut WorkScope<'_>,
) -> Result<usize, Failure> {
    const FIXED: usize = 1024;
    const SCAN: usize = 256;
    const LOCAL: usize = 1024;
    const ENTRY: usize = std::mem::size_of::<(&str, Vec<u8>)>();
    work.charge(WorkCost {
        objects: 0,
        edges: FIXED,
        bytes: 64 * FIXED,
    })?;
    let count = candidate.blob_count();
    let scan = mul(SCAN, count)?;
    work.charge(WorkCost {
        objects: 0,
        edges: scan,
        bytes: mul(64, scan)?,
    })?;
    let mut bytes = 0usize;
    let mut envelopes = 0usize;
    for blob in candidate.blobs() {
        let length = usize::try_from(blob.bytes()).map_err(|_| arithmetic())?;
        bytes = add(bytes, length)?;
        let chunks = add(length / 65_536, usize::from(length % 65_536 != 0))?;
        envelopes = add(envelopes, add(mul(2, chunks)?, 2)?)?;
    }
    let edges = add(add(FIXED, mul(count, SCAN + LOCAL)?)?, mul(128, envelopes)?)?;
    let index = if count == 0 {
        0
    } else {
        add(mul(ENTRY, count)?, 128)?
    };
    let payload = add(bytes, mul(128, count)?)?;
    let mut total_bytes = add(index, payload)?;
    total_bytes = add(total_bytes, mul(2, bytes)?)?;
    total_bytes = add(total_bytes, mul(64, edges)?)?;
    let objects = add(usize::from(count != 0), count)?;
    let prepaid = add(FIXED, scan)?;
    work.charge(WorkCost {
        objects,
        edges: edges.checked_sub(prepaid).ok_or_else(arithmetic)?,
        bytes: total_bytes
            .checked_sub(mul(64, prepaid)?)
            .ok_or_else(arithmetic)?,
    })?;
    Ok(count)
}

/// A bounded, private transfer collector. It holds no work scope, publishes no
/// bytes, and cannot grow beyond its already-funded expected length.
struct Collector {
    expected: usize,
    bytes: Vec<u8>,
    begun: bool,
    finished: bool,
    fault: Option<CollectorFault>,
}
impl Collector {
    fn fail(&mut self, fault: CollectorFault) {
        if self.fault.is_none() {
            self.fault = Some(fault);
        }
    }
    fn into_verified(self) -> Result<Vec<u8>, CollectorFault> {
        if let Some(fault) = self.fault {
            return Err(fault);
        }
        if !self.begun || !self.finished || self.bytes.len() != self.expected {
            return Err(CollectorFault::Completion);
        }
        Ok(self.bytes)
    }
}
impl VerifiedSink for Collector {
    /// The announced digest is not compared here: C2a-3k re-hashes every
    /// retained byte against the candidate's own `sha256` (addendum map-r1).
    fn begin(&mut self, _sha256: [u8; 32], length: u64) {
        if self.fault.is_some() {
            return;
        }
        if self.begun || self.finished || length != self.expected as u64 {
            self.fail(CollectorFault::Begin);
            return;
        }
        self.begun = true;
    }
    fn chunk(&mut self, bytes: &[u8]) {
        if self.fault.is_some() {
            return;
        }
        if !self.begun || self.finished {
            self.fail(CollectorFault::Chunk);
        } else if bytes.len() > self.expected - self.bytes.len() {
            self.fail(CollectorFault::Length);
        } else {
            self.bytes.extend_from_slice(bytes);
        }
    }
    fn finish(&mut self, verified: bool) {
        if self.fault.is_some() {
            return;
        }
        if !self.begun || self.finished || !verified || self.bytes.len() != self.expected {
            self.fail(CollectorFault::Completion);
        }
        self.finished = true;
    }
}

/// Retain and verify one complete component on the caller's original scope.
/// Neither a candidate nor a digest-only success can construct this payload.
pub fn admit_component<'store, 'borrow, 'manifest: 'borrow>(
    store: &'store ComponentStore,
    component: &AuthenticatedComponent<'manifest>,
    candidate: &'borrow ClosureCandidate<'manifest>,
    platform: SelectedPlatform<'_>,
    pin: PinRequest,
    work: &mut WorkScope<'_>,
) -> Result<AdmittedComponent<'store, 'borrow, 'manifest>, ComponentAdmissionFailure> {
    work.scope(|scope| admit_component_inner(store, component, candidate, platform, pin, scope))
        .map_err(public_failure)
}

fn admit_component_inner<'store, 'borrow, 'manifest: 'borrow>(
    store: &'store ComponentStore,
    component: &AuthenticatedComponent<'manifest>,
    candidate: &'borrow ClosureCandidate<'manifest>,
    platform: SelectedPlatform<'_>,
    pin: PinRequest,
    scope: &mut WorkScope<'_>,
) -> Result<AdmittedComponent<'store, 'borrow, 'manifest>, Failure> {
    /// The component's fixed local work: the open boundary, funding entry,
    /// buffer vector, loop, kernel boundary, drop and return (addendum map-r1).
    const COMPONENT: usize = 1024;
    scope.charge(WorkCost {
        objects: 0,
        edges: COMPONENT,
        bytes: 64 * COMPONENT,
    })?;
    let mut retained = open_retained_tree(store, component, candidate, platform, pin, scope)
        .map_err(tree_input)?;
    #[cfg(test)]
    test_faults::after_open();
    let count = fund_representation(candidate, scope)?;
    let mut retained_bytes = Vec::with_capacity(count);
    for blob in candidate.blobs() {
        let length = usize::try_from(blob.bytes()).map_err(|_| arithmetic())?;
        let mut collector = Collector {
            expected: length,
            bytes: Vec::with_capacity(length),
            begun: false,
            finished: false,
            fault: None,
        };
        let path = blob.path();
        // The transfer's actual error wins over finish(false)/sticky state.
        let transfer = retained.transfer(path, &mut collector, scope);
        #[cfg(test)]
        if transfer.is_err() {
            test_faults::observe_failure(&collector);
        }
        transfer.map_err(tree_input)?;
        let bytes = collector
            .into_verified()
            .map_err(|fault| WorkFailure::Operation(Fault::Collector(fault)))?;
        retained_bytes.push((path, bytes));
    }
    #[cfg(test)]
    let test_body = test_faults::kernel_inputs(&mut retained_bytes, component.body());
    #[cfg(test)]
    let body = test_body.as_ref();
    #[cfg(not(test))]
    let body = component.body();
    verify_retained_tree(candidate, &retained_bytes, body, scope).map_err(closure_input)?;
    drop(retained_bytes);
    Ok(AdmittedComponent {
        candidate,
        retained,
    })
}

#[cfg(test)]
mod test_faults {
    include!("component_admission_faults.rs");
}

#[cfg(test)]
mod tests {
    include!("component_admission_tests.rs");
}
