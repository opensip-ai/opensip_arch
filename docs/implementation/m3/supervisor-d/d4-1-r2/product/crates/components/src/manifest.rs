//! M3-D r5 item 24 (unit D4-1; D4 plan r2, LD-D4-2 to LD-D4-10): the
//! manifest-class excluded forms of DR-G29, judged at R10a and ER10a before
//! any analysis-attempt ExecutionId is drawn.
//!
//! The judge reads a pure, borrowed projection of the security owner's
//! validated manifest (`ManifestClaims`), which the host builds from the
//! trust view; components has no security dependency (CH14:288) and parses
//! no manifest bytes. It refuses EE-1, EE-3b and EE-5a; EE-4's manifest part
//! has no carrier in the closed manifest schema (LD-D4-5). Every refusal is
//! returned, in SD-5's order: by manifest digest, then class. Every
//! allocation, comparison and probe is charged on the caller's borrowed
//! `WorkScope` before it is made; no profile is selected here (LD-D4-SD9).
//! `Cleared` names the judged digests and authorizes nothing by itself.
use opensip_platform::{WorkBudgetError, WorkCost, WorkFailure, WorkScope};

/// A manifest's role (DR103:891-897, as the product's generated shape
/// admits it since CR-1's materialization).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Role {
    Analyzer,
    Toolchain,
    Stdlib,
    RustDevLlvm,
    Grammar,
}

/// `provenance.sourceClass`, the closed slice-1 vocabulary (DR103:1023).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum SourceClass {
    FirstParty,
    ExplicitlyTrusted,
}

/// The publisher and source class of the catalog release row the ordinary
/// reader joined to the manifest (LD-D4-3): the root-authenticated
/// association, never a caller's assertion.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ReleaseProvenance<'a> {
    pub publisher: &'a str,
    pub source_class: SourceClass,
}

/// One `commands[]` entry: its name, its parent, and its aliases.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct CommandClaim<'a> {
    pub name: &'a str,
    pub parent: Option<&'a str>,
    pub aliases: &'a [&'a str],
}

/// One `capabilities[]` entry: its id and its `declarationData` relation and
/// rung, which the validated value already ties to the id.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct CapabilityClaim<'a> {
    pub capability_id: &'a str,
    pub relation: &'a str,
    pub rung: &'a str,
}

/// The borrowed projection D4 judges (LD-D4-2).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ManifestClaims<'a> {
    pub manifest_digest: [u8; 32],
    pub role: Role,
    pub name: &'a str,
    pub aliases: &'a [&'a str],
    /// `None` when the manifest declares no `commands` member at all.
    pub commands: Option<&'a [CommandClaim<'a>]>,
    pub capabilities: &'a [CapabilityClaim<'a>],
    pub provenance: ReleaseProvenance<'a>,
}

/// Which policy slice is out of order (LD-D4-2).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum PolicySlice {
    ReservedRoots,
    ProviderRelations,
    ExplicitlyTrusted,
}

/// Why a policy was not built.
#[derive(Debug, PartialEq, Eq)]
pub enum PolicyRefusal {
    /// A slice is not strictly ascending: a host-invariant fault.
    Unordered(PolicySlice),
    Budget(WorkBudgetError),
}

/// The host's admission policy: three sorted, unique borrowed slices
/// (LD-D4-2). Only `AdmissionPolicy::new` builds one, after checking the
/// order at one charged comparison per adjacent pair.
#[derive(Debug)]
pub struct AdmissionPolicy<'a> {
    reserved_roots: &'a [&'a str],
    provider_relations: &'a [(&'a str, &'a str)],
    explicitly_trusted: &'a [&'a str],
}

impl<'a> AdmissionPolicy<'a> {
    /// `reserved_roots` is the list the security owner validated against;
    /// `provider_relations` the native capability matrix's pinned
    /// projection; `explicitly_trusted` the explicit-trust list, empty at
    /// M3 (LD-D4-3).
    pub fn new(
        reserved_roots: &'a [&'a str],
        provider_relations: &'a [(&'a str, &'a str)],
        explicitly_trusted: &'a [&'a str],
        work: &mut WorkScope<'_>,
    ) -> Result<Self, PolicyRefusal> {
        ascending(reserved_roots, PolicySlice::ReservedRoots, work)?;
        ascending(provider_relations, PolicySlice::ProviderRelations, work)?;
        ascending(explicitly_trusted, PolicySlice::ExplicitlyTrusted, work)?;
        Ok(Self {
            reserved_roots,
            provider_relations,
            explicitly_trusted,
        })
    }
}

fn ascending<T: Ord>(
    slice: &[T],
    which: PolicySlice,
    work: &mut WorkScope<'_>,
) -> Result<(), PolicyRefusal> {
    for pair in slice.windows(2) {
        compare(work).map_err(policy_budget)?;
        if ordered(&pair[0], &pair[1]) != core::cmp::Ordering::Less {
            return Err(PolicyRefusal::Unordered(which));
        }
    }
    Ok(())
}

fn policy_budget(failure: WorkFailure<()>) -> PolicyRefusal {
    match failure {
        WorkFailure::Budget(b) => PolicyRefusal::Budget(b),
        WorkFailure::Operation(()) => unreachable!("a charge has no operation failure"),
    }
}

/// The excluded-form classes D4 represents (items 24 and 25), in the one
/// order both projections use: SD-5's EE-1, EE-3b, EE-4, EE-5a for manifests
/// and item 25's EE-2, EE-4, EE-6a for requests (LD-D4-9).
#[derive(Debug, Clone, Copy, PartialEq, Eq, PartialOrd, Ord)]
pub enum ExcludedFormClass {
    Ee1,
    Ee2,
    Ee3b,
    Ee4,
    Ee5a,
    Ee6a,
}

/// Which arm of its class refused the manifest: internal only, for the
/// operational record's key (LD-D4-9).
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum Arm {
    /// EE-1: an `explicitly-trusted` publisher not on the explicit-trust list.
    UnlistedPublisher,
    /// EE-3b: a capability whose relation and rung no provider capability of
    /// the matrix has.
    UnmatchedCapability,
    /// EE-5a (a): a closure-only role that declares `commands` at all.
    ClosureOnlyCommands,
    /// EE-5a (b): an analyzer tree outside the mounted-root model.
    RootModel,
    /// EE-5a (c): a root-namespace key on the reserved list.
    ReservedRoot,
}

/// One internal refusal, `ExcludedForm {class, subject}` (item 24), the
/// subject being the manifest's digest.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub struct ExcludedForm {
    pub class: ExcludedFormClass,
    pub arm: Arm,
    pub manifest_digest: [u8; 32],
}

/// A host-built input the judge refuses as a host invariant.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
pub enum InvariantFault {
    /// Two claims with one digest: R10a's set has one per manifest.
    DuplicateDigest,
    /// More claims than a `u32` index can name.
    TooManyClaims,
}

/// Why `admit` did not clear the set.
#[derive(Debug, PartialEq, Eq)]
pub enum Refusal {
    /// Every excluded form, by digest then class; the first is SD-5's
    /// projected pair (LD-D4-8).
    Excluded(Vec<ExcludedForm>),
    Invariant(InvariantFault),
    Budget(WorkBudgetError),
}

/// The judged digests, in ascending order. Opaque and not `Clone`: only
/// `admit` builds one, and it authorizes nothing (LD-D4-8).
#[derive(Debug, PartialEq, Eq)]
pub struct Cleared {
    digests: Vec<[u8; 32]>,
}
impl Cleared {
    pub fn digests(&self) -> &[[u8; 32]] {
        &self.digests
    }
}

/// One comparison or membership test, charged immediately before it.
pub const COMPARISON_COST: WorkCost = WorkCost {
    objects: 0,
    edges: 1,
    bytes: 0,
};

/// The digest sort's two `u32` index buffers (CI-A1-b's recipe).
pub const fn index_buffers_cost(n: usize) -> WorkCost {
    WorkCost {
        objects: 2,
        edges: 0,
        bytes: n.saturating_mul(2 * size_of::<u32>()),
    }
}

/// The refusal vector, reserved for exactly `k` forms.
pub const fn refusal_vector_cost(k: usize) -> WorkCost {
    WorkCost {
        objects: 1,
        edges: 0,
        bytes: k.saturating_mul(size_of::<ExcludedForm>()),
    }
}

/// `Cleared`'s digest list, reserved for exactly `n` digests.
pub const fn cleared_cost(n: usize) -> WorkCost {
    WorkCost {
        objects: 1,
        edges: 0,
        bytes: n.saturating_mul(size_of::<[u8; 32]>()),
    }
}

/// The published reference bounds: a sort of `n` makes at most
/// n·⌈log₂ n⌉ comparisons, and a probe into `m` at most ⌈log₂ m⌉ + 1 (one
/// for an empty slice, its empty check). Actual charges are made as they
/// occur, never above these.
pub const fn sort_reference_comparisons(n: usize) -> usize {
    if n < 2 {
        0
    } else {
        n.saturating_mul(ceil_log2(n))
    }
}
pub const fn probe_reference_comparisons(m: usize) -> usize {
    if m == 0 { 1 } else { ceil_log2(m) + 1 }
}
const fn ceil_log2(n: usize) -> usize {
    if n < 2 {
        0
    } else {
        (usize::BITS - (n - 1).leading_zeros()) as usize
    }
}

type Charge = Result<(), WorkFailure<()>>;

/// The work sites, as the operation-order oracle records them (unit D4-1
/// r2; `codex-d4-1-r1` RF-1). Each charge funds exactly the operations that
/// follow it before the next charge: an index-buffer charge two allocations,
/// a result charge one, and a comparison charge one comparison or one push.
#[derive(Debug, Clone, Copy, PartialEq, Eq)]
#[cfg_attr(not(test), allow(dead_code))]
enum Operation {
    Charged(WorkCost),
    Allocated,
    Compared,
    Pushed,
}

#[cfg(test)]
thread_local! {
    /// The oracle's log, recording only while a test has armed it.
    static OPERATIONS: core::cell::RefCell<Option<Vec<Operation>>> =
        const { core::cell::RefCell::new(None) };
}

/// Record one work site (tests only).
#[cfg(test)]
fn note(operation: Operation) {
    OPERATIONS.with(|log| {
        if let Some(log) = log.borrow_mut().as_mut() {
            log.push(operation);
        }
    });
}
/// Nothing is recorded in any other build.
#[cfg(not(test))]
#[inline(always)]
fn note(_: Operation) {}

/// Every charge goes through here: the ledger first, then the record.
fn charge(work: &mut WorkScope<'_>, cost: WorkCost) -> Charge {
    work.charge::<()>(cost)?;
    note(Operation::Charged(cost));
    Ok(())
}

fn compare(work: &mut WorkScope<'_>) -> Charge {
    charge(work, COMPARISON_COST)
}

/// Every judged comparison goes through here, so its site is recorded where
/// it is made.
fn ordered<T: Ord + ?Sized>(a: &T, b: &T) -> core::cmp::Ordering {
    note(Operation::Compared);
    a.cmp(b)
}
/// A judged boolean test, recorded where it is made.
fn tested(outcome: bool) -> bool {
    note(Operation::Compared);
    outcome
}
/// Every allocation goes through here.
fn reserve<T>(capacity: usize) -> Vec<T> {
    note(Operation::Allocated);
    Vec::with_capacity(capacity)
}

/// A charged binary search of a sorted, unique slice: one edge before each
/// comparison, or one for an empty slice's empty check.
fn probe<T: Ord + ?Sized, U: core::borrow::Borrow<T>>(
    slice: &[U],
    key: &T,
    work: &mut WorkScope<'_>,
) -> Result<bool, WorkFailure<()>> {
    if slice.is_empty() {
        compare(work)?;
        tested(true);
        return Ok(false);
    }
    let (mut low, mut high) = (0, slice.len());
    while low < high {
        let mid = low + (high - low) / 2;
        compare(work)?;
        match ordered(slice[mid].borrow(), key) {
            core::cmp::Ordering::Less => low = mid + 1,
            core::cmp::Ordering::Greater => high = mid,
            core::cmp::Ordering::Equal => return Ok(true),
        }
    }
    Ok(false)
}

/// The bottom-up merge sort over `u32` indices, one edge charged before each
/// comparison (CI-A1-b; C2a-1's recipe). Its second buffer is dropped here.
fn sort_indices(
    claims: &[ManifestClaims<'_>],
    n: u32,
    work: &mut WorkScope<'_>,
) -> Result<Vec<u32>, WorkFailure<()>> {
    let len = n as usize;
    charge(work, index_buffers_cost(len))?;
    let mut from = reserve(len);
    from.extend(0..n);
    let mut to = reserve(len);
    to.extend(0..n);
    let mut width = 1;
    while width < len {
        let mut low = 0;
        while low < len {
            let mid = (low + width).min(len);
            let high = (low + 2 * width).min(len);
            let (mut i, mut j, mut k) = (low, mid, low);
            while i < mid && j < high {
                compare(work)?;
                if ordered(
                    &claims[from[j] as usize].manifest_digest,
                    &claims[from[i] as usize].manifest_digest,
                ) == core::cmp::Ordering::Less
                {
                    to[k] = from[j];
                    j += 1;
                } else {
                    to[k] = from[i];
                    i += 1;
                }
                k += 1;
            }
            to[k..k + mid - i].copy_from_slice(&from[i..mid]);
            k += mid - i;
            to[k..high].copy_from_slice(&from[j..high]);
            low = high;
        }
        core::mem::swap(&mut from, &mut to);
        width *= 2;
    }
    Ok(from)
}

/// One manifest's predicates, in class order, each form handed to `found`
/// (LD-D4-10's per-manifest prices). The count and fill passes both call it,
/// so both are charged identically.
fn judge(
    claim: &ManifestClaims<'_>,
    policy: &AdmissionPolicy<'_>,
    work: &mut WorkScope<'_>,
    found: &mut impl FnMut(ExcludedForm),
) -> Charge {
    let form = |class, arm| ExcludedForm {
        class,
        arm,
        manifest_digest: claim.manifest_digest,
    };
    // EE-1: the release association's class, then the explicit-trust list.
    compare(work)?;
    if tested(claim.provenance.source_class == SourceClass::ExplicitlyTrusted)
        && !probe(policy.explicitly_trusted, claim.provenance.publisher, work)?
    {
        found(form(ExcludedFormClass::Ee1, Arm::UnlistedPublisher));
    }
    // EE-3b: each capability's relation and rung, until one is unmatched.
    for capability in claim.capabilities {
        if !probe(
            policy.provider_relations,
            &(capability.relation, capability.rung),
            work,
        )? {
            found(form(ExcludedFormClass::Ee3b, Arm::UnmatchedCapability));
            break;
        }
    }
    // EE-4's manifest part has no carrier (LD-D4-5). EE-5a: (a), (b), (c).
    if let Some(arm) = root_claim(claim, policy, work)? {
        found(form(ExcludedFormClass::Ee5a, arm));
    }
    Ok(())
}

/// EE-5a's root-command predicate (item 24, LD-R4-1): the first arm that
/// holds, in the order (a), (b), (c).
fn root_claim(
    claim: &ManifestClaims<'_>,
    policy: &AdmissionPolicy<'_>,
    work: &mut WorkScope<'_>,
) -> Result<Option<Arm>, WorkFailure<()>> {
    // (a) A closure-only role that declares `commands` at all.
    compare(work)?;
    if tested(claim.role != Role::Analyzer && claim.commands.is_some()) {
        return Ok(Some(Arm::ClosureOnlyCommands));
    }
    // (b) Exactly one parentless entry, named for the manifest.
    let mut root = None;
    if claim.role == Role::Analyzer {
        let commands = claim.commands.unwrap_or(&[]);
        let mut roots = 0usize;
        for command in commands {
            compare(work)?;
            if tested(command.parent.is_none()) {
                roots += 1;
                root = Some(command);
            }
        }
        if roots != 1 {
            return Ok(Some(Arm::RootModel));
        }
        compare(work)?;
        if tested(root.is_some_and(|r| r.name != claim.name)) {
            return Ok(Some(Arm::RootModel));
        }
    }
    // (c) The root-namespace keys: the name, each alias, and the analyzer
    // root's aliases.
    let root_aliases = root.map_or(&[][..], |r| r.aliases);
    for key in core::iter::once(&claim.name)
        .chain(claim.aliases)
        .chain(root_aliases)
    {
        if probe(policy.reserved_roots, *key, work)? {
            return Ok(Some(Arm::ReservedRoot));
        }
    }
    Ok(None)
}

/// Judge every claim (LD-D4-8): sort by digest, refuse duplicates, count
/// the forms, then either fill the exact refusal vector or the `Cleared`
/// list. Exhaustion at any step is `Budget`, never a partial result.
pub fn admit(
    claims: &[ManifestClaims<'_>],
    policy: &AdmissionPolicy<'_>,
    work: &mut WorkScope<'_>,
) -> Result<Cleared, Refusal> {
    let n = u32::try_from(claims.len())
        .map_err(|_| Refusal::Invariant(InvariantFault::TooManyClaims))?;
    let order = sort_indices(claims, n, work).map_err(refusal_budget)?;
    for pair in order.windows(2) {
        compare(work).map_err(refusal_budget)?;
        if ordered(
            &claims[pair[0] as usize].manifest_digest,
            &claims[pair[1] as usize].manifest_digest,
        ) == core::cmp::Ordering::Equal
        {
            return Err(Refusal::Invariant(InvariantFault::DuplicateDigest));
        }
    }
    let mut k = 0usize;
    for &i in &order {
        judge(&claims[i as usize], policy, work, &mut |_| k += 1).map_err(refusal_budget)?;
    }
    if k > 0 {
        charge(work, refusal_vector_cost(k)).map_err(refusal_budget)?;
        let mut forms = reserve(k);
        for &i in &order {
            judge(&claims[i as usize], policy, work, &mut |f| forms.push(f))
                .map_err(refusal_budget)?;
        }
        return Err(Refusal::Excluded(forms));
    }
    charge(work, cleared_cost(order.len())).map_err(refusal_budget)?;
    let mut digests = reserve(order.len());
    for &i in &order {
        compare(work).map_err(refusal_budget)?;
        note(Operation::Pushed);
        digests.push(claims[i as usize].manifest_digest);
    }
    Ok(Cleared { digests })
}

fn refusal_budget(failure: WorkFailure<()>) -> Refusal {
    match failure {
        WorkFailure::Budget(b) => Refusal::Budget(b),
        WorkFailure::Operation(()) => unreachable!("a charge has no operation failure"),
    }
}

#[cfg(test)]
#[path = "manifest_tests.rs"]
mod tests;
