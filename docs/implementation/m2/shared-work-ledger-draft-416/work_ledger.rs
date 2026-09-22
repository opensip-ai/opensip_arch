//! Bounded bookkeeping shared by borrowed host/platform/security operations.
//! Counters are not native custody, admission, authorization or effect receipts.
//! One private operation owner must preserve this ledger across all sub-operations.
//! Creating a new ledger never licenses retrying a failed native operation.

const OBJECT_LIMIT: usize = 65_536;
const EDGE_LIMIT: usize = 131_072;
const BYTE_LIMIT: usize = 268_435_456;
const RECORD_LIMIT: usize = 4_194_304;

#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
pub struct Cost {
    pub objects: usize,
    pub edges: usize,
    pub bytes: usize,
}
impl Cost {
    fn checked_add(self, other: Self) -> Option<Self> {
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

// No Clone, Default, reset, refund or deserialization. Public construction is
// deliberately accounting only; native operation ownership is enforced elsewhere.
pub struct WorkLedger {
    limits: Cost,
    used: Cost,
    failed: bool,
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

    pub fn new() -> Self {
        Self {
            limits: Cost {
                objects: OBJECT_LIMIT,
                edges: EDGE_LIMIT,
                bytes: BYTE_LIMIT,
            },
            used: Cost::default(),
            failed: false,
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
        })
    }

    pub fn scope<T, E>(
        &mut self,
        action: impl FnOnce(&mut Self) -> Result<T, Failure<E>>,
    ) -> Result<T, Failure<E>> {
        if self.failed {
            return Err(Failure::Budget(BudgetFailure::Closed));
        }
        let mut guard = LedgerScope {
            ledger: self,
            completed: false,
        };
        let result = action(guard.ledger);
        match result {
            Ok(value) if !guard.ledger.failed => {
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
            if cost.objects > s.limits.objects - s.used.objects {
                return Err(Failure::Budget(BudgetFailure::Objects));
            }
            if cost.edges > s.limits.edges - s.used.edges {
                return Err(Failure::Budget(BudgetFailure::Edges));
            }
            if cost.bytes > s.limits.bytes - s.used.bytes {
                return Err(Failure::Budget(BudgetFailure::Bytes));
            }
            s.used = s
                .used
                .checked_add(cost)
                .ok_or(Failure::Budget(BudgetFailure::Arithmetic))?;
            Ok(())
        })
    }

    pub fn run<T, E>(
        &mut self,
        cost: Cost,
        action: impl FnOnce(&mut Self) -> Result<T, Failure<E>>,
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
        action: impl FnOnce(&mut Self) -> Result<T, Failure<E>>,
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
                ledger: s,
                remaining: postchecks,
            })
        })
    }
}
struct LedgerScope<'a> {
    ledger: &'a mut WorkLedger,
    completed: bool,
}
impl Drop for LedgerScope<'_> {
    fn drop(&mut self) {
        if !self.completed {
            self.ledger.failed = true;
        }
    }
}
pub struct ReservedPostchecks<'a> {
    ledger: &'a mut WorkLedger,
    remaining: Cost,
}
impl ReservedPostchecks<'_> {
    pub fn spend<E>(&mut self, cost: Cost) -> Result<(), Failure<E>> {
        self.ledger.scope(|_| {
            self.remaining = self
                .remaining
                .checked_sub(cost)
                .ok_or(Failure::Budget(BudgetFailure::ReservedPostcheck))?;
            Ok(())
        })
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
}
