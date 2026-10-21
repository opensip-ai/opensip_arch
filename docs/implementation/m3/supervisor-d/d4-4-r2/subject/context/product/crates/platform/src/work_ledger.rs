//! Bounded bookkeeping shared by borrowed host/platform/security operations.
//! Counters are not native custody, admission, authorization or effect receipts.
//! One private operation owner must preserve this ledger across all sub-operations.
//! Creating a new ledger never licenses retrying a failed native operation.
//! The one exception to the failure latch is a settlement reserve (law X3d r6
//! item 8): an allowance charged before any effect, taken at most once per
//! instance, and spendable once through `WorkLedger::settle` even after the
//! instance has failed. Outside `settle` a failed ledger refuses everything.

use core::sync::atomic::{AtomicU64, Ordering};

const OBJECT_LIMIT: usize = 65_536;
const EDGE_LIMIT: usize = 131_072;
const BYTE_LIMIT: usize = 268_435_456;
const RECORD_LIMIT: usize = 4_194_304;
// M3-B r7 item 12 (units B2-b1 and B2-b4b3): the discovery ledger profile's
// caps, 2^22 objects, 2^21 edges and 2^30 bytes, recorded from the redesigned
// walker's T2 census by r6's rule (the smallest power of two at least twice
// the largest censused entry; bytes at a 4,096-byte root spelling).
const DISCOVERY_OBJECT_LIMIT: usize = 1 << 22;
const DISCOVERY_EDGE_LIMIT: usize = 1 << 21;
const DISCOVERY_BYTE_LIMIT: usize = 1 << 30;
// M3-C r9 item 2 (unit C1a4): the snapshot ledger profile's caps, 2^21
// objects, 2^24 edges and 2^33 bytes, by r5's rule (the smallest power of two
// at least twice the larger of the item-5-bounded subtotal and the
// lead-readable T2 census maximum), with the walk's classification remedies
// (a) and (b-prime) landed.
const SNAPSHOT_OBJECT_LIMIT: usize = 1 << 21;
const SNAPSHOT_EDGE_LIMIT: usize = 1 << 24;
const SNAPSHOT_BYTE_LIMIT: usize = 1 << 33;

#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
pub struct Cost {
    pub objects: usize,
    pub edges: usize,
    pub bytes: usize,
}
impl Cost {
    /// Add requested work component by component without overflow. This only
    /// computes a cost; it reserves no work and grants no operation authority.
    pub fn checked_add(self, other: Self) -> Option<Self> {
        Some(Self {
            objects: self.objects.checked_add(other.objects)?,
            edges: self.edges.checked_add(other.edges)?,
            bytes: self.bytes.checked_add(other.bytes)?,
        })
    }
    fn checked_sub(self, other: Self) -> Option<Self> {
        Some(Self {
            objects: self.objects.checked_sub(other.objects)?,
            edges: self.edges.checked_sub(other.edges)?,
            bytes: self.bytes.checked_sub(other.bytes)?,
        })
    }
}

#[derive(Debug, PartialEq, Eq)]
pub enum BudgetFailure {
    Closed,
    Objects,
    Edges,
    Bytes,
    Record,
    Arithmetic,
    ReservedPostcheck,
    Profile,
}
#[derive(Debug, PartialEq, Eq)]
pub enum Failure<E> {
    Budget(BudgetFailure),
    Operation(E),
}

// Issue numbers that bind a settlement reserve to the one instance that took
// it. Each is drawn once and never reused; exhaustion refuses the reservation.
static SETTLEMENT_ISSUE: AtomicU64 = AtomicU64::new(1);

// The instance's one settlement reserve (law X3d r6 item 8).
#[derive(Clone, Copy, PartialEq, Eq)]
enum Settlement {
    Untaken,
    // Charged to `used`; the reserve with this issue number is outstanding.
    Reserved(u64),
    // `settle` is running. Scopes inside it are checked against this latch,
    // not against `failed`; any failure inside sets both.
    Active { latched: bool },
    // Consumed by `settle`, or refused there. Never taken again.
    Spent,
}

// No Clone, Default, reset, refund or deserialization. Public construction is
// deliberately accounting only; native operation ownership is enforced elsewhere.
pub struct WorkLedger {
    limits: Cost,
    used: Cost,
    failed: bool,
    // While `ReservedPostchecks::prepaid` or `settle` runs, charges draw from
    // this carved, already-charged allowance instead of the limits; `used`
    // does not move.
    prepaid: Option<Cost>,
    settlement: Settlement,
}

/// The one settlement allowance of the [`WorkLedger`] that issued it (law X3d
/// r6 item 8). Its cost was charged to that ledger's `used` when it was taken
/// and is never refunded. It can be spent once, only through
/// [`WorkLedger::settle`] on the issuing instance, and nothing adds to it.
/// It is not `Clone`, `Copy`, `Default` or serializable, and
/// [`WorkLedger::reserve_settlement`] is its only constructor. Dropping it
/// unspent forfeits it.
///
/// ```
/// use opensip_platform::{WorkCost, WorkLedger};
/// let mut owner = WorkLedger::new();
/// let two = WorkCost { edges: 2, ..WorkCost::default() };
/// let reserve = owner.reserve_settlement(two).unwrap();
/// owner.settle::<_, ()>(reserve, |work| work.charge(two)).unwrap();
/// ```
///
/// It cannot be cloned or copied, so it is spent at most once:
///
/// ```compile_fail
/// use opensip_platform::{WorkCost, WorkLedger};
/// let mut owner = WorkLedger::new();
/// let reserve = owner.reserve_settlement(WorkCost::default()).unwrap();
/// let _copy = reserve.clone();
/// ```
///
/// ```compile_fail
/// use opensip_platform::{WorkCost, WorkLedger};
/// let mut owner = WorkLedger::new();
/// let reserve = owner.reserve_settlement(WorkCost::default()).unwrap();
/// owner.settle::<(), ()>(reserve, |_| Ok(())).unwrap();
/// owner.settle::<(), ()>(reserve, |_| Ok(())).unwrap();
/// ```
///
/// It cannot be defaulted or constructed:
///
/// ```compile_fail
/// use opensip_platform::SettlementReserve;
/// let _reserve = SettlementReserve::default();
/// ```
///
/// ```compile_fail
/// use opensip_platform::{SettlementReserve, WorkCost};
/// let _reserve = SettlementReserve { issuer: 1, allowance: WorkCost::default() };
/// ```
///
/// It cannot be taken or spent from a helper's `WorkScope`:
///
/// ```compile_fail
/// use opensip_platform::{WorkCost, WorkLedger};
/// let mut owner = WorkLedger::new();
/// owner.scope::<(), ()>(|helper| {
///     let _ = helper.reserve_settlement(WorkCost::default());
///     Ok(())
/// }).unwrap();
/// ```
///
/// ```compile_fail
/// use opensip_platform::{WorkCost, WorkLedger};
/// let mut owner = WorkLedger::new();
/// let reserve = owner.reserve_settlement(WorkCost::default()).unwrap();
/// owner.scope::<(), ()>(|helper| helper.settle(reserve, |_| Ok(()))).unwrap();
/// ```
///
/// or from `ReservedPostchecks`:
///
/// ```compile_fail
/// use opensip_platform::{WorkCost, WorkLedger};
/// let mut owner = WorkLedger::new();
/// owner.effect::<(), ()>(WorkCost::default(), WorkCost::default(), |post| {
///     let _ = post.reserve_settlement(WorkCost::default());
///     Ok(())
/// }).unwrap();
/// ```
///
/// ```compile_fail
/// use opensip_platform::{WorkCost, WorkLedger};
/// let mut owner = WorkLedger::new();
/// let reserve = owner.reserve_settlement(WorkCost::default()).unwrap();
/// owner.effect::<(), ()>(WorkCost::default(), WorkCost::default(), |post| {
///     post.settle(reserve, |_| Ok(()))
/// }).unwrap();
/// ```
pub struct SettlementReserve {
    issuer: u64,
    allowance: Cost,
}

impl WorkLedger {
    /// Charged work, including unused reservations; never decremented.
    pub fn used(&self) -> Cost {
        self.used
    }
    /// Failure is permanent for this instance, including nested errors/unwind.
    pub fn is_failed(&self) -> bool {
        self.failed
    }

    /// No `Default`: `std::mem::take` would swap a failed ledger for a fresh
    /// one in place, which is the retry this ledger must never allow.
    #[allow(clippy::new_without_default)]
    pub fn new() -> Self {
        Self {
            limits: Cost {
                objects: OBJECT_LIMIT,
                edges: EDGE_LIMIT,
                bytes: BYTE_LIMIT,
            },
            used: Cost::default(),
            failed: false,
            prepaid: None,
            settlement: Settlement::Untaken,
        }
    }

    /// M3-B r5 item 12: the one discovery ledger an invocation creates, once,
    /// after X2's handoff releases the installation fence. Its caps are the
    /// only ones above the global caps; `with_limits` still cannot raise any.
    /// Like every ledger it has no `Default` and no `Clone`: a failed discovery
    /// ledger is never replaced, and exhaustion is never truncation.
    pub fn discovery_profile() -> Self {
        Self {
            limits: Cost {
                objects: DISCOVERY_OBJECT_LIMIT,
                edges: DISCOVERY_EDGE_LIMIT,
                bytes: DISCOVERY_BYTE_LIMIT,
            },
            used: Cost::default(),
            failed: false,
            prepaid: None,
            settlement: Settlement::Untaken,
        }
    }

    /// M3-C r8 item 2, as M3-C r9 amends it: the one snapshot ledger an
    /// invocation creates, once, after discovery. Its caps are its own, above
    /// the global caps; `with_limits` still cannot raise any. Like every
    /// ledger it has no `Default` and no `Clone`: a failed snapshot ledger is
    /// never replaced, and exhaustion is never truncation.
    pub fn snapshot_profile() -> Self {
        Self {
            limits: Cost {
                objects: SNAPSHOT_OBJECT_LIMIT,
                edges: SNAPSHOT_EDGE_LIMIT,
                bytes: SNAPSHOT_BYTE_LIMIT,
            },
            used: Cost::default(),
            failed: false,
            prepaid: None,
            settlement: Settlement::Untaken,
        }
    }

    /// A stricter policy may lower any limit, but never raise the global caps.
    /// A new instance is independent accounting, never a retry permission.
    pub fn with_limits(limits: Cost) -> Result<Self, BudgetFailure> {
        if limits.objects == 0
            || limits.objects > OBJECT_LIMIT
            || limits.edges == 0
            || limits.edges > EDGE_LIMIT
            || limits.bytes == 0
            || limits.bytes > BYTE_LIMIT
        {
            return Err(BudgetFailure::Profile);
        }
        Ok(Self {
            limits,
            used: Cost::default(),
            failed: false,
            prepaid: None,
            settlement: Settlement::Untaken,
        })
    }

    /// Helpers receive a non-constructible borrowed scope, not the replaceable ledger.
    ///
    /// ```compile_fail
    /// use opensip_platform::WorkLedger;
    /// let mut owner = WorkLedger::new();
    /// owner.scope::<(), ()>(|helper| {
    ///     *helper = WorkLedger::new();
    ///     Ok(())
    /// }).unwrap();
    /// ```
    ///
    /// A second ledger cannot donate a scope which escapes its nested borrow:
    ///
    /// ```compile_fail
    /// use opensip_platform::WorkLedger;
    /// let mut owner = WorkLedger::new();
    /// let mut replacement = WorkLedger::new();
    /// owner.scope::<(), ()>(|original| {
    ///     replacement.scope::<(), ()>(|other| {
    ///         core::mem::swap(original, other);
    ///         Ok(())
    ///     })
    /// }).unwrap();
    /// ```
    pub fn scope<T, E>(
        &mut self,
        action: impl FnOnce(&mut WorkScope<'_>) -> Result<T, Failure<E>>,
    ) -> Result<T, Failure<E>> {
        if self.closed() {
            return Err(Failure::Budget(BudgetFailure::Closed));
        }
        let mut guard = LedgerScope {
            ledger: self,
            completed: false,
        };
        let result = action(&mut WorkScope {
            ledger: guard.ledger,
        });
        match result {
            Ok(value) if !guard.ledger.closed() => {
                guard.completed = true;
                Ok(value)
            }
            // A caller catching a nested failure cannot reopen the outer scope.
            Ok(_) => Err(Failure::Budget(BudgetFailure::Closed)),
            Err(error) => Err(error),
        }
    }

    pub fn charge<E>(&mut self, cost: Cost) -> Result<(), Failure<E>> {
        self.scope(|s| {
            if let Some(credit) = s.ledger.prepaid {
                s.ledger.prepaid = Some(
                    credit
                        .checked_sub(cost)
                        .ok_or(Failure::Budget(BudgetFailure::ReservedPostcheck))?,
                );
                return Ok(());
            }
            if cost.objects > s.ledger.limits.objects - s.ledger.used.objects {
                return Err(Failure::Budget(BudgetFailure::Objects));
            }
            if cost.edges > s.ledger.limits.edges - s.ledger.used.edges {
                return Err(Failure::Budget(BudgetFailure::Edges));
            }
            if cost.bytes > s.ledger.limits.bytes - s.ledger.used.bytes {
                return Err(Failure::Budget(BudgetFailure::Bytes));
            }
            s.ledger.used = s
                .ledger
                .used
                .checked_add(cost)
                .ok_or(Failure::Budget(BudgetFailure::Arithmetic))?;
            Ok(())
        })
    }

    pub fn run<T, E>(
        &mut self,
        cost: Cost,
        action: impl FnOnce(&mut WorkScope<'_>) -> Result<T, Failure<E>>,
    ) -> Result<T, Failure<E>> {
        self.scope(|s| {
            s.charge(cost)?;
            action(s)
        })
    }

    /// Account one newly retained record and its bytes before the callback.
    /// Identity deduplication belongs to the caller's retained cache. Temporary
    /// reads/copies and repeated observations require separate charges.
    pub fn retained_record<T, E>(
        &mut self,
        bytes: usize,
        action: impl FnOnce(&mut WorkScope<'_>) -> Result<T, Failure<E>>,
    ) -> Result<T, Failure<E>> {
        self.scope(|s| {
            if bytes > RECORD_LIMIT {
                return Err(Failure::Budget(BudgetFailure::Record));
            }
            s.run(
                Cost {
                    objects: 1,
                    bytes,
                    ..Cost::default()
                },
                action,
            )
        })
    }

    // Reserve the effect AND all known required follow-up work before the action.
    // This is bookkeeping only; real native producers must derive sufficient
    // costs and supply their actual admission/retained-owner receipts separately.
    pub fn effect<T, E>(
        &mut self,
        effect: Cost,
        postchecks: Cost,
        action: impl FnOnce(&mut ReservedPostchecks<'_>) -> Result<T, Failure<E>>,
    ) -> Result<T, Failure<E>> {
        self.scope(|s| {
            let total = effect
                .checked_add(postchecks)
                .ok_or(Failure::Budget(BudgetFailure::Arithmetic))?;
            s.charge(total)?;
            action(&mut ReservedPostchecks {
                ledger: s.ledger,
                remaining: postchecks,
            })
        })
    }

    /// Take this instance's one settlement reserve (law X3d r6 item 8). It is
    /// on the owner's ledger only: `WorkScope` and `ReservedPostchecks` have
    /// no such method. `cost` is charged to `used` at once, exactly as any
    /// charge is, and is never refunded. A closed ledger refuses `Closed`;
    /// a cost beyond the remaining limits refuses `Objects`, `Edges`, `Bytes`
    /// or `Arithmetic`. Each refusal takes nothing and latches the ledger, as
    /// any failed charge does. A second reservation on the same instance,
    /// whether or not the first was spent, is refused `Closed` and latches.
    pub fn reserve_settlement(&mut self, cost: Cost) -> Result<SettlementReserve, BudgetFailure> {
        if self.settlement != Settlement::Untaken {
            self.failed = true;
            return Err(BudgetFailure::Closed);
        }
        if self.failed {
            return Err(BudgetFailure::Closed);
        }
        let Ok(issuer) = SETTLEMENT_ISSUE
            .fetch_update(Ordering::Relaxed, Ordering::Relaxed, |n| n.checked_add(1))
        else {
            self.failed = true;
            return Err(BudgetFailure::Arithmetic);
        };
        match self.charge::<core::convert::Infallible>(cost) {
            Ok(()) => {}
            Err(Failure::Budget(failure)) => return Err(failure),
            Err(Failure::Operation(never)) => match never {},
        }
        self.settlement = Settlement::Reserved(issuer);
        Ok(SettlementReserve {
            issuer,
            allowance: cost,
        })
    }

    /// Spend this instance's settlement reserve once (law X3d r6 item 8).
    /// It is admitted whether or not the ledger has failed. `action` receives
    /// a `WorkScope` on this ledger. Every charge inside it, including nested
    /// `run`, `effect`, `ReservedPostchecks` and `prepaid`, draws only from the
    /// reserve's allowance, never from the limits, and `used` does not move.
    /// Scopes inside are checked against the settlement's own latch, not the
    /// ledger's. Any `Err`, an overrun (refused `ReservedPostcheck` before the
    /// work it covers) or an unwind latches both the settlement and the
    /// ledger; the reserve is consumed, so nothing more can be drawn. A
    /// reserve this instance did not issue is refused `Closed` before
    /// `action` runs, and latches this ledger. Unused allowance is never
    /// refunded, and nothing adds to it. Outside `settle` nothing changes: a
    /// failed ledger still refuses every `scope`, `charge`, `run` and `effect`.
    pub fn settle<T, E>(
        &mut self,
        reserve: SettlementReserve,
        action: impl FnOnce(&mut WorkScope<'_>) -> Result<T, Failure<E>>,
    ) -> Result<T, Failure<E>> {
        let SettlementReserve { issuer, allowance } = reserve;
        if self.settlement != Settlement::Reserved(issuer) {
            self.failed = true;
            return Err(Failure::Budget(BudgetFailure::Closed));
        }
        let guard = Settling {
            saved: self.prepaid.replace(allowance),
            ledger: self,
        };
        guard.ledger.settlement = Settlement::Active { latched: false };
        guard.ledger.scope(action)
    }

    // Inside `settle` scopes answer to the settlement's latch; elsewhere,
    // and on every ledger that never settles, to `failed` exactly as before.
    fn closed(&self) -> bool {
        match self.settlement {
            Settlement::Active { latched } => latched,
            _ => self.failed,
        }
    }

    // A failed or unwound scope latches the ledger and, inside `settle`, the
    // settlement too.
    fn latch(&mut self) {
        self.failed = true;
        if let Settlement::Active { latched } = &mut self.settlement {
            *latched = true;
        }
    }
}
/// A borrowed view for helpers. It cannot replace, clone or obtain the owner's
/// ledger. Only the private operation owner keeps the replaceable WorkLedger.
/// Native scope/receipt ownership is still an independent composition obligation.
pub struct WorkScope<'a> {
    ledger: &'a mut WorkLedger,
}
impl WorkScope<'_> {
    pub fn used(&self) -> Cost {
        self.ledger.used()
    }
    pub fn is_failed(&self) -> bool {
        self.ledger.is_failed()
    }
    pub fn scope<T, E>(
        &mut self,
        action: impl FnOnce(&mut WorkScope<'_>) -> Result<T, Failure<E>>,
    ) -> Result<T, Failure<E>> {
        self.ledger.scope(action)
    }
    pub fn charge<E>(&mut self, cost: Cost) -> Result<(), Failure<E>> {
        self.ledger.charge(cost)
    }
    pub fn run<T, E>(
        &mut self,
        cost: Cost,
        action: impl FnOnce(&mut WorkScope<'_>) -> Result<T, Failure<E>>,
    ) -> Result<T, Failure<E>> {
        self.ledger.run(cost, action)
    }
    pub fn retained_record<T, E>(
        &mut self,
        bytes: usize,
        action: impl FnOnce(&mut WorkScope<'_>) -> Result<T, Failure<E>>,
    ) -> Result<T, Failure<E>> {
        self.ledger.retained_record(bytes, action)
    }
    pub fn effect<T, E>(
        &mut self,
        effect: Cost,
        postchecks: Cost,
        action: impl FnOnce(&mut ReservedPostchecks<'_>) -> Result<T, Failure<E>>,
    ) -> Result<T, Failure<E>> {
        self.ledger.effect(effect, postchecks, action)
    }
}

struct LedgerScope<'a> {
    ledger: &'a mut WorkLedger,
    completed: bool,
}
impl Drop for LedgerScope<'_> {
    fn drop(&mut self) {
        if !self.completed {
            self.ledger.latch();
        }
    }
}
// Ends a settlement however `settle` returns or unwinds: the reserve is spent
// and the enclosing credit (none, at the owner) is restored.
struct Settling<'a> {
    ledger: &'a mut WorkLedger,
    saved: Option<Cost>,
}
impl Drop for Settling<'_> {
    fn drop(&mut self) {
        self.ledger.prepaid = self.saved;
        self.ledger.settlement = Settlement::Spent;
    }
}
pub struct ReservedPostchecks<'a> {
    ledger: &'a mut WorkLedger,
    remaining: Cost,
}
impl ReservedPostchecks<'_> {
    /// Run fallible follow-up work within the original reserved allowance.
    /// Returning an error or unwinding permanently closes the original ledger,
    /// even when an outer callback catches the failure. No allowance is refunded.
    /// This guard does not prove that native checks happened or costs suffice.
    pub fn scope<T, E>(
        &mut self,
        action: impl FnOnce(&mut ReservedPostchecks<'_>) -> Result<T, Failure<E>>,
    ) -> Result<T, Failure<E>> {
        if self.ledger.closed() {
            return Err(Failure::Budget(BudgetFailure::Closed));
        }
        let mut guard = ReservedScope {
            postchecks: self,
            completed: false,
        };
        let result = action(guard.postchecks);
        match result {
            Ok(value) if !guard.postchecks.ledger.closed() => {
                guard.completed = true;
                Ok(value)
            }
            Ok(_) => Err(Failure::Budget(BudgetFailure::Closed)),
            Err(error) => Err(error),
        }
    }
    /// Carve out a child allowance from this reservation before invoking its helper.
    /// The child borrows the SAME original ledger but can spend only its own share.
    /// Unused child allowance is not returned to the parent; no outer work is
    /// charged again. Failure/unwind closes the original operation everywhere.
    /// Costs and native checks still belong to the trusted operation owner.
    pub fn with_allowance<T, E>(
        &mut self,
        cost: Cost,
        action: impl FnOnce(&mut ReservedPostchecks<'_>) -> Result<T, Failure<E>>,
    ) -> Result<T, Failure<E>> {
        self.scope(|parent| {
            parent.spend(cost)?;
            let mut child = ReservedPostchecks {
                ledger: parent.ledger,
                remaining: cost,
            };
            child.scope(action)
        })
    }
    /// Run ordinary charged work inside this reservation (law 467 item 6: the
    /// owner rechecks after the rename run inside the rename's reservation).
    /// `cost` is first spent from this allowance, as `spend` would; the action
    /// then receives a [`WorkScope`] on the SAME ledger whose charges draw from
    /// that carved allowance, not from the ledger's limits, so nothing is charged
    /// twice and `used()` does not move inside it. A charge beyond the allowance
    /// fails closed with `ReservedPostcheck` before the work it covers, and
    /// closes the original ledger. Unused allowance is not refunded. Nested
    /// effects and prepaid runs inside the action draw from this allowance too.
    pub fn prepaid<T, E>(
        &mut self,
        cost: Cost,
        action: impl FnOnce(&mut WorkScope<'_>) -> Result<T, Failure<E>>,
    ) -> Result<T, Failure<E>> {
        self.scope(|post| {
            post.spend(cost)?;
            let credit = PrepaidCredit {
                saved: post.ledger.prepaid.replace(cost),
                ledger: post.ledger,
            };
            credit.ledger.scope(action)
        })
    }
    pub fn spend<E>(&mut self, cost: Cost) -> Result<(), Failure<E>> {
        self.scope(|s| {
            s.remaining = s
                .remaining
                .checked_sub(cost)
                .ok_or(Failure::Budget(BudgetFailure::ReservedPostcheck))?;
            Ok(())
        })
    }
}
// Restores the enclosing credit (or none) when a prepaid run ends or unwinds.
struct PrepaidCredit<'a> {
    ledger: &'a mut WorkLedger,
    saved: Option<Cost>,
}
impl Drop for PrepaidCredit<'_> {
    fn drop(&mut self) {
        self.ledger.prepaid = self.saved;
    }
}
struct ReservedScope<'borrow, 'owner> {
    postchecks: &'borrow mut ReservedPostchecks<'owner>,
    completed: bool,
}
impl Drop for ReservedScope<'_, '_> {
    fn drop(&mut self) {
        if !self.completed {
            self.postchecks.ledger.latch();
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    use std::cell::Cell;
    use std::panic::{AssertUnwindSafe, catch_unwind};

    #[test]
    fn exhausted_dimensions_and_record_limit_prevent_action() {
        for (cost, expected) in [
            (
                Cost {
                    objects: OBJECT_LIMIT + 1,
                    ..Cost::default()
                },
                BudgetFailure::Objects,
            ),
            (
                Cost {
                    edges: EDGE_LIMIT + 1,
                    ..Cost::default()
                },
                BudgetFailure::Edges,
            ),
            (
                Cost {
                    bytes: usize::MAX,
                    ..Cost::default()
                },
                BudgetFailure::Bytes,
            ),
        ] {
            let mut ledger = WorkLedger::new();
            let result = ledger.run::<(), ()>(cost, |_| panic!("action before reservation"));
            assert_eq!(result, Err(Failure::Budget(expected)));
            assert_eq!(
                ledger.charge::<()>(Cost::default()),
                Err(Failure::Budget(BudgetFailure::Closed))
            );
        }
        let mut ledger = WorkLedger::new();
        assert_eq!(
            ledger.retained_record::<(), ()>(RECORD_LIMIT + 1, |_| panic!(
                "oversized record allocation"
            )),
            Err(Failure::Budget(BudgetFailure::Record))
        );
    }

    /// C1-T27 (M3-C r8 item 2, with M3-C r9's caps; unit C1a4): the snapshot
    /// ledger at exactly 2^21 objects, 2^24 edges and 2^33 bytes admits, and
    /// one unit over in any dimension refuses as budget exhaustion, charging
    /// nothing and closing the ledger, never truncating the work.
    #[test]
    fn the_snapshot_profile_admits_exactly_its_caps_and_refuses_one_unit_over() {
        let caps = Cost {
            objects: 2_097_152,
            edges: 16_777_216,
            bytes: 8_589_934_592,
        };
        let mut exact = WorkLedger::snapshot_profile();
        assert_eq!(exact.charge::<()>(caps), Ok(()));
        assert_eq!(exact.used(), caps);
        assert!(!exact.is_failed());
        for (over, expected) in [
            (
                Cost {
                    objects: caps.objects + 1,
                    ..Cost::default()
                },
                BudgetFailure::Objects,
            ),
            (
                Cost {
                    edges: caps.edges + 1,
                    ..Cost::default()
                },
                BudgetFailure::Edges,
            ),
            (
                Cost {
                    bytes: caps.bytes + 1,
                    ..Cost::default()
                },
                BudgetFailure::Bytes,
            ),
        ] {
            let mut ledger = WorkLedger::snapshot_profile();
            assert_eq!(
                ledger.run::<(), ()>(over, |_| panic!("action before reservation")),
                Err(Failure::Budget(expected))
            );
            assert_eq!(ledger.used(), Cost::default());
            assert!(ledger.is_failed());
            assert_eq!(
                ledger.charge::<()>(Cost::default()),
                Err(Failure::Budget(BudgetFailure::Closed))
            );
        }
        // Cumulatively too: a ledger at its caps refuses the next unit.
        assert_eq!(
            exact.charge::<()>(Cost {
                edges: 1,
                ..Cost::default()
            }),
            Err(Failure::Budget(BudgetFailure::Edges))
        );
        assert_eq!(exact.used(), caps);
    }

    #[test]
    fn exact_limits_are_inclusive_and_repeated_work_is_not_free() {
        let mut ledger = WorkLedger::new();
        let cap = Cost {
            objects: OBJECT_LIMIT,
            edges: EDGE_LIMIT,
            bytes: BYTE_LIMIT,
        };
        ledger.charge::<()>(cap).unwrap();
        assert_eq!(ledger.used, cap);
        assert_eq!(
            ledger.charge::<()>(Cost {
                edges: 1,
                ..Cost::default()
            }),
            Err(Failure::Budget(BudgetFailure::Edges))
        );
        let mut ledger = WorkLedger::new();
        ledger
            .retained_record::<_, ()>(RECORD_LIMIT, |_| Ok(()))
            .unwrap();
        ledger
            .retained_record::<_, ()>(RECORD_LIMIT, |_| Ok(()))
            .unwrap();
        assert_eq!(ledger.used.bytes, RECORD_LIMIT * 2);
    }

    #[test]
    fn failed_ledger_keeps_reservation_and_cannot_retry() {
        let mut ledger = WorkLedger::new();
        let cost = Cost {
            objects: 1,
            edges: 3,
            bytes: 4096,
        };
        assert_eq!(
            ledger.run(cost, |_| Err::<(), _>(Failure::Operation("read failure"))),
            Err(Failure::Operation("read failure"))
        );
        assert_eq!(ledger.used, cost);
        assert_eq!(
            ledger.run::<(), ()>(Cost::default(), |_| panic!("retry")),
            Err(Failure::Budget(BudgetFailure::Closed))
        );
    }

    #[test]
    fn swallowed_nested_failure_and_unwind_cannot_reopen_ledger() {
        let mut ledger = WorkLedger::new();
        assert_eq!(
            ledger.scope(|s| {
                let _ = s.run::<(), ()>(Cost::default(), |_| Err(Failure::Operation(())));
                Ok::<_, Failure<()>>(())
            }),
            Err(Failure::Budget(BudgetFailure::Closed))
        );
        let mut ledger = WorkLedger::new();
        assert!(
            catch_unwind(AssertUnwindSafe(|| {
                let _ = ledger.run::<(), ()>(
                    Cost {
                        edges: 1,
                        ..Cost::default()
                    },
                    |_| panic!("native adapter unwound"),
                );
            }))
            .is_err()
        );
        assert_eq!(ledger.used.edges, 1);
        assert_eq!(
            ledger.charge::<()>(Cost::default()),
            Err(Failure::Budget(BudgetFailure::Closed))
        );
    }

    #[test]
    fn postcheck_cost_is_precharged_and_never_refunded() {
        let mut ledger = WorkLedger::new();
        ledger
            .charge::<()>(Cost {
                edges: EDGE_LIMIT - 1,
                ..Cost::default()
            })
            .unwrap();
        assert_eq!(
            ledger.effect::<(), ()>(
                Cost {
                    edges: 1,
                    ..Cost::default()
                },
                Cost {
                    edges: 1,
                    ..Cost::default()
                },
                |_| panic!("effect without postcheck budget")
            ),
            Err(Failure::Budget(BudgetFailure::Edges))
        );
        let mut ledger = WorkLedger::new();
        let called = Cell::new(false);
        ledger
            .effect::<_, ()>(
                Cost {
                    edges: 1,
                    ..Cost::default()
                },
                Cost {
                    edges: 3,
                    ..Cost::default()
                },
                |post| {
                    called.set(true);
                    post.spend(Cost {
                        edges: 1,
                        ..Cost::default()
                    })?;
                    Ok(())
                },
            )
            .unwrap();
        assert!(called.get());
        assert_eq!(ledger.used.edges, 4); // Unused postchecks are not refunded.
        assert_eq!(
            ledger.effect::<(), ()>(
                Cost {
                    bytes: usize::MAX,
                    ..Cost::default()
                },
                Cost {
                    bytes: 1,
                    ..Cost::default()
                },
                |_| panic!("overflowing reservation")
            ),
            Err(Failure::Budget(BudgetFailure::Arithmetic))
        );
    }

    #[test]
    fn caught_postcheck_overrun_still_closes_the_ledger() {
        let mut ledger = WorkLedger::new();
        assert_eq!(
            ledger.effect::<(), ()>(Cost::default(), Cost::default(), |post| {
                let _ = post.spend::<()>(Cost {
                    edges: 1,
                    ..Cost::default()
                });
                Ok(())
            }),
            Err(Failure::Budget(BudgetFailure::Closed))
        );
    }

    fn edges(n: usize) -> Cost {
        Cost {
            edges: n,
            ..Cost::default()
        }
    }

    #[test]
    fn prepaid_work_draws_from_the_carved_allowance_without_charging_twice() {
        let mut ledger = WorkLedger::new();
        let seen = ledger
            .effect::<_, ()>(edges(1), edges(10), |post| {
                let inside = post.prepaid(edges(6), |work| {
                    let before = work.used();
                    work.charge(edges(2))?;
                    work.run(edges(1), |_| Ok(()))?;
                    // A nested effect is charged from the same allowance.
                    work.effect(edges(1), edges(2), |nested| nested.spend(edges(2)))?;
                    assert_eq!(work.used(), before); // Already charged; not again.
                    Ok(before)
                })?;
                // The rest of the reservation remains for later postchecks.
                post.spend(edges(4))?;
                Ok(inside)
            })
            .unwrap();
        assert_eq!(seen, edges(11));
        assert_eq!(ledger.used(), edges(11));
        assert!(!ledger.is_failed());
        // Ordinary charging resumes against the limits afterwards.
        ledger.charge::<()>(edges(1)).unwrap();
        assert_eq!(ledger.used(), edges(12));
    }

    #[test]
    fn prepaid_overrun_fails_closed_before_the_work_it_covers() {
        let mut ledger = WorkLedger::new();
        let ran = Cell::new(false);
        let result = ledger.effect::<(), ()>(Cost::default(), edges(5), |post| {
            post.prepaid(edges(3), |work| {
                work.charge(edges(2))?;
                work.run(edges(2), |_| {
                    ran.set(true);
                    Ok(())
                })
            })
        });
        assert_eq!(
            result,
            Err(Failure::Budget(BudgetFailure::ReservedPostcheck))
        );
        assert!(!ran.get());
        assert!(ledger.is_failed());
        assert_eq!(ledger.used(), edges(5));
        assert_eq!(
            ledger.charge::<()>(Cost::default()),
            Err(Failure::Budget(BudgetFailure::Closed))
        );
        // An allowance larger than the reservation is refused before the action.
        let mut ledger = WorkLedger::new();
        let result = ledger.effect::<(), ()>(Cost::default(), edges(2), |post| {
            post.prepaid(edges(3), |_| panic!("action beyond the reservation"))
        });
        assert_eq!(
            result,
            Err(Failure::Budget(BudgetFailure::ReservedPostcheck))
        );
        assert!(ledger.is_failed());
    }

    #[test]
    fn prepaid_swallowed_overrun_or_unwind_still_closes_the_ledger() {
        let mut ledger = WorkLedger::new();
        let result = ledger.effect::<(), ()>(Cost::default(), edges(2), |post| {
            post.prepaid(edges(2), |work| {
                let _ = work.charge::<()>(edges(3));
                Ok(())
            })
        });
        assert_eq!(result, Err(Failure::Budget(BudgetFailure::Closed)));
        assert!(ledger.is_failed());
        let mut ledger = WorkLedger::new();
        assert!(
            catch_unwind(AssertUnwindSafe(|| {
                let _ = ledger.effect::<(), ()>(Cost::default(), edges(2), |post| {
                    post.prepaid(edges(2), |_| panic!("recheck unwound"))
                });
            }))
            .is_err()
        );
        assert!(ledger.is_failed());
        assert_eq!(ledger.prepaid, None);
    }

    #[test]
    fn settlement_ends_spent_with_no_credit_however_it_returns() {
        // Success, Err and unwind each leave the reserve spent, no credit
        // installed, and ordinary charging back on the limits and `failed`.
        let mut ledger = WorkLedger::new();
        let reserve = ledger.reserve_settlement(edges(3)).unwrap();
        assert!(ledger.settlement == Settlement::Reserved(reserve.issuer));
        ledger
            .settle::<_, ()>(reserve, |work| work.charge(edges(1)))
            .unwrap();
        assert!(ledger.settlement == Settlement::Spent);
        assert_eq!(ledger.prepaid, None);
        assert!(!ledger.is_failed());
        ledger.charge::<()>(edges(1)).unwrap();
        assert_eq!(ledger.used(), edges(4));

        let mut ledger = WorkLedger::new();
        let reserve = ledger.reserve_settlement(edges(3)).unwrap();
        assert_eq!(
            ledger.settle::<(), _>(reserve, |_| Err(Failure::Operation(()))),
            Err(Failure::Operation(()))
        );
        assert!(ledger.settlement == Settlement::Spent);
        assert_eq!(ledger.prepaid, None);
        assert!(ledger.is_failed() && ledger.closed());

        let mut ledger = WorkLedger::new();
        let reserve = ledger.reserve_settlement(edges(3)).unwrap();
        assert!(
            catch_unwind(AssertUnwindSafe(|| {
                let _ = ledger.settle::<(), ()>(reserve, |_| panic!("append unwound"));
            }))
            .is_err()
        );
        assert!(ledger.settlement == Settlement::Spent);
        assert_eq!(ledger.prepaid, None);
        assert!(ledger.is_failed() && ledger.closed());
    }
}
