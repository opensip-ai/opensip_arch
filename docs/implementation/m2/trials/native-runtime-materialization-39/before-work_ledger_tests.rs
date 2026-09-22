//! Actual public API across a sibling cache and platform reborrow. Accounting
//! and lifetime checks only; not native evidence-capture or authority fixtures.
use opensip_platform::{
    WorkBudgetError as BudgetFailure, WorkCost as Cost, WorkFailure as Failure, WorkLedger,
    WorkScope,
};
struct HeldCache<'cache, 'op> {
    work: &'cache mut WorkScope<'op>,
    held: Vec<Vec<u8>>,
}
impl<'cache, 'op> HeldCache<'cache, 'op> {
    fn new(work: &'cache mut WorkScope<'op>) -> Self {
        Self {
            work,
            held: Vec::new(),
        }
    }
    fn capture(&mut self, bytes: &[u8]) -> Result<(), Failure<()>> {
        self.work.retained_record(bytes.len(), |_| {
            self.held.push(bytes.to_vec());
            Ok(())
        })
    }
    fn platform_work<T>(
        &mut self,
        f: impl FnOnce(&mut WorkScope<'_>) -> Result<T, Failure<()>>,
    ) -> Result<T, Failure<()>> {
        self.work.scope(f)
    }
}
#[test]
fn host_security_platform_reborrow_one_ledger_without_losing_evidence() {
    let mut original = WorkLedger::new();
    original
        .scope::<_, ()>(|host| {
            host.charge(Cost {
                edges: 2,
                bytes: 16,
                ..Cost::default()
            })?;
            {
                let mut cache = HeldCache::new(host);
                cache.capture(b"held")?;
                let ptr = cache.held[0].as_ptr();
                cache.platform_work(|platform| {
                    platform.charge(Cost {
                        edges: 3,
                        bytes: 8,
                        ..Cost::default()
                    })
                })?;
                assert_eq!(cache.held[0].as_ptr(), ptr);
                assert_eq!(cache.held[0], b"held");
                cache.capture(b"more")?;
            }
            assert_eq!(
                host.used(),
                Cost {
                    objects: 2,
                    edges: 5,
                    bytes: 32
                }
            );
            assert!(!host.is_failed());
            host.charge(Cost {
                edges: 1,
                ..Cost::default()
            })
        })
        .unwrap();
    assert_eq!(
        original.used(),
        Cost {
            objects: 2,
            edges: 6,
            bytes: 32
        }
    );
}
#[test]
fn nested_platform_failure_survives_cache_drop_and_host_catch() {
    let mut original = WorkLedger::new();
    let result = original.scope::<_, ()>(|host| {
        {
            let mut cache = HeldCache::new(host);
            cache.capture(b"held")?;
            assert_eq!(
                cache.platform_work(|platform| {
                    assert!(
                        platform
                            .charge::<()>(Cost {
                                bytes: usize::MAX,
                                ..Cost::default()
                            })
                            .is_err()
                    );
                    Ok(())
                }),
                Err(Failure::Budget(BudgetFailure::Closed))
            );
            assert_eq!(cache.held[0], b"held");
        }
        assert!(host.is_failed());
        Ok(())
    });
    assert_eq!(result, Err(Failure::Budget(BudgetFailure::Closed)));
    assert!(original.is_failed());
    assert_eq!(
        original.used(),
        Cost {
            objects: 1,
            bytes: 4,
            edges: 0
        }
    );
    assert_eq!(
        original.charge::<()>(Cost::default()),
        Err(Failure::Budget(BudgetFailure::Closed))
    );
}
#[test]
fn lower_policy_limits_refuse_work_before_callback_without_reset() {
    let cap = Cost {
        objects: 1,
        edges: 2,
        bytes: 4,
    };
    let mut ledger = WorkLedger::with_limits(cap).unwrap();
    ledger.retained_record::<_, ()>(4, |_| Ok(())).unwrap();
    assert_eq!(
        ledger.used(),
        Cost {
            objects: 1,
            edges: 0,
            bytes: 4
        }
    );
    assert_eq!(
        ledger.retained_record::<(), ()>(1, |_| panic!("allocation after refusal")),
        Err(Failure::Budget(BudgetFailure::Objects))
    );
    assert!(ledger.is_failed());
    assert_eq!(
        ledger.used(),
        Cost {
            objects: 1,
            edges: 0,
            bytes: 4
        }
    );
    assert!(matches!(
        WorkLedger::with_limits(Cost::default()),
        Err(BudgetFailure::Profile)
    ));
    assert!(matches!(
        WorkLedger::with_limits(Cost {
            bytes: usize::MAX,
            ..cap
        }),
        Err(BudgetFailure::Profile)
    ));
}
