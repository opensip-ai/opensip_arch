//! Draft bookkeeping for one host-owned initial installation attempt.
//! No ingress, native admission receipt, filesystem action or creation authority.

const OBJECT_LIMIT: usize = 65_536;
const EDGE_LIMIT: usize = 131_072;
const BYTE_LIMIT: usize = 268_435_456;
const RECORD_LIMIT: usize = 4_194_304;

#[derive(Clone, Copy, Debug, Default, PartialEq, Eq)]
struct Cost {
    objects: usize,
    edges: usize,
    bytes: usize,
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
enum BudgetFailure {
    Closed,
    Objects,
    Edges,
    Bytes,
    Record,
    Arithmetic,
    ReservedPostcheck,
}
#[derive(Debug, PartialEq, Eq)]
enum Failure<E> {
    Budget(BudgetFailure),
    Operation(E),
}

// The attempt cannot be cloned, deserialized or reset. Its eventual constructor
// call belongs only to admitted durable ingress, before account/path observation.
// Merely allocating counters grants no native authority.
struct InitialInstallationAttempt {
    used: Cost,
    failed: bool,
}
impl InitialInstallationAttempt {
    fn new() -> Self {
        Self {
            used: Cost::default(),
            failed: false,
        }
    }

    fn scope<T, E>(
        &mut self,
        action: impl FnOnce(&mut Self) -> Result<T, Failure<E>>,
    ) -> Result<T, Failure<E>> {
        if self.failed {
            return Err(Failure::Budget(BudgetFailure::Closed));
        }
        let mut guard = AttemptScope {
            attempt: self,
            completed: false,
        };
        let result = action(guard.attempt);
        match result {
            Ok(value) if !guard.attempt.failed => {
                guard.completed = true;
                Ok(value)
            }
            // A caller catching a nested failure cannot reopen the outer scope.
            Ok(_) => Err(Failure::Budget(BudgetFailure::Closed)),
            Err(error) => Err(error),
        }
    }

    fn charge<E>(&mut self, cost: Cost) -> Result<(), Failure<E>> {
        self.scope(|s| {
            if cost.objects > OBJECT_LIMIT - s.used.objects {
                return Err(Failure::Budget(BudgetFailure::Objects));
            }
            if cost.edges > EDGE_LIMIT - s.used.edges {
                return Err(Failure::Budget(BudgetFailure::Edges));
            }
            if cost.bytes > BYTE_LIMIT - s.used.bytes {
                return Err(Failure::Budget(BudgetFailure::Bytes));
            }
            s.used = s
                .used
                .checked_add(cost)
                .ok_or(Failure::Budget(BudgetFailure::Arithmetic))?;
            Ok(())
        })
    }

    fn run<T, E>(
        &mut self,
        cost: Cost,
        action: impl FnOnce(&mut Self) -> Result<T, Failure<E>>,
    ) -> Result<T, Failure<E>> {
        self.scope(|s| {
            s.charge(cost)?;
            action(s)
        })
    }

    fn record<T, E>(
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
    fn effect<T, E>(
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
                attempt: s,
                remaining: postchecks,
            })
        })
    }
}
struct AttemptScope<'a> {
    attempt: &'a mut InitialInstallationAttempt,
    completed: bool,
}
impl Drop for AttemptScope<'_> {
    fn drop(&mut self) {
        if !self.completed {
            self.attempt.failed = true;
        }
    }
}
struct ReservedPostchecks<'a> {
    attempt: &'a mut InitialInstallationAttempt,
    remaining: Cost,
}
impl ReservedPostchecks<'_> {
    fn spend<E>(&mut self, cost: Cost) -> Result<(), Failure<E>> {
        self.attempt.scope(|_| {
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
            let mut attempt = InitialInstallationAttempt::new();
            let result = attempt.run::<(), ()>(cost, |_| panic!("action before reservation"));
            assert_eq!(result, Err(Failure::Budget(expected)));
            assert_eq!(
                attempt.charge::<()>(Cost::default()),
                Err(Failure::Budget(BudgetFailure::Closed))
            );
        }
        let mut attempt = InitialInstallationAttempt::new();
        assert_eq!(
            attempt.record::<(), ()>(RECORD_LIMIT + 1, |_| panic!("oversized record allocation")),
            Err(Failure::Budget(BudgetFailure::Record))
        );
    }

    #[test]
    fn exact_limits_are_inclusive_and_repeated_work_is_not_free() {
        let mut attempt = InitialInstallationAttempt::new();
        let cap = Cost {
            objects: OBJECT_LIMIT,
            edges: EDGE_LIMIT,
            bytes: BYTE_LIMIT,
        };
        attempt.charge::<()>(cap).unwrap();
        assert_eq!(attempt.used, cap);
        assert_eq!(
            attempt.charge::<()>(Cost {
                edges: 1,
                ..Cost::default()
            }),
            Err(Failure::Budget(BudgetFailure::Edges))
        );
        let mut attempt = InitialInstallationAttempt::new();
        attempt.record::<_, ()>(RECORD_LIMIT, |_| Ok(())).unwrap();
        attempt.record::<_, ()>(RECORD_LIMIT, |_| Ok(())).unwrap();
        assert_eq!(attempt.used.bytes, RECORD_LIMIT * 2);
    }

    #[test]
    fn failed_attempt_keeps_reservation_and_cannot_retry() {
        let mut attempt = InitialInstallationAttempt::new();
        let cost = Cost {
            objects: 1,
            edges: 3,
            bytes: 4096,
        };
        assert_eq!(
            attempt.run(cost, |_| Err::<(), _>(Failure::Operation("read failure"))),
            Err(Failure::Operation("read failure"))
        );
        assert_eq!(attempt.used, cost);
        assert_eq!(
            attempt.run::<(), ()>(Cost::default(), |_| panic!("retry")),
            Err(Failure::Budget(BudgetFailure::Closed))
        );
    }

    #[test]
    fn swallowed_nested_failure_and_unwind_cannot_reopen_attempt() {
        let mut attempt = InitialInstallationAttempt::new();
        assert_eq!(
            attempt.scope(|s| {
                let _ = s.run::<(), ()>(Cost::default(), |_| Err(Failure::Operation(())));
                Ok::<_, Failure<()>>(())
            }),
            Err(Failure::Budget(BudgetFailure::Closed))
        );
        let mut attempt = InitialInstallationAttempt::new();
        assert!(
            catch_unwind(AssertUnwindSafe(|| {
                let _ = attempt.run::<(), ()>(
                    Cost {
                        edges: 1,
                        ..Cost::default()
                    },
                    |_| panic!("native adapter unwound"),
                );
            }))
            .is_err()
        );
        assert_eq!(attempt.used.edges, 1);
        assert_eq!(
            attempt.charge::<()>(Cost::default()),
            Err(Failure::Budget(BudgetFailure::Closed))
        );
    }

    #[test]
    fn postcheck_cost_is_precharged_and_never_refunded() {
        let mut attempt = InitialInstallationAttempt::new();
        attempt
            .charge::<()>(Cost {
                edges: EDGE_LIMIT - 1,
                ..Cost::default()
            })
            .unwrap();
        assert_eq!(
            attempt.effect::<(), ()>(
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
        let mut attempt = InitialInstallationAttempt::new();
        let called = Cell::new(false);
        attempt
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
        assert_eq!(attempt.used.edges, 4); // Unused postchecks are not refunded.
        assert_eq!(
            attempt.effect::<(), ()>(
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
    fn caught_postcheck_overrun_still_closes_the_attempt() {
        let mut attempt = InitialInstallationAttempt::new();
        assert_eq!(
            attempt.effect::<(), ()>(Cost::default(), Cost::default(), |post| {
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
