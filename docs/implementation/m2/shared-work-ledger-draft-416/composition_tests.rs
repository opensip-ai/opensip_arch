//! Compile/run experiment: a sibling cache borrows the one ledger and reborrows
//! it for platform work without losing held evidence. Not native qualification.
#[path = "work_ledger.rs"]
mod work_ledger;
use work_ledger::{BudgetFailure, Cost, Failure, WorkLedger};

struct HeldCache<'a> {
    ledger: &'a mut WorkLedger,
    held: Vec<Vec<u8>>,
}
impl<'a> HeldCache<'a> {
    fn new(ledger: &'a mut WorkLedger) -> Self {
        Self {
            ledger,
            held: Vec::new(),
        }
    }
    fn capture(&mut self, bytes: &[u8]) -> Result<(), Failure<()>> {
        self.ledger.retained_record(bytes.len(), |_| {
            self.held.push(bytes.to_vec());
            Ok(())
        })
    }
    fn platform_work<T>(
        &mut self,
        work: impl FnOnce(&mut WorkLedger) -> Result<T, Failure<()>>,
    ) -> Result<T, Failure<()>> {
        self.ledger.scope(work)
    }
}

#[test]
fn host_security_platform_reborrow_one_ledger_without_losing_evidence() {
    let mut original = WorkLedger::new();
    original
        .charge::<()>(Cost {
            edges: 2,
            bytes: 16,
            ..Cost::default()
        })
        .unwrap();
    {
        let mut security = HeldCache::new(&mut original);
        security.capture(b"held").unwrap();
        let ptr = security.held[0].as_ptr();
        security
            .platform_work(|same| {
                same.charge(Cost {
                    edges: 3,
                    bytes: 8,
                    ..Cost::default()
                })
            })
            .unwrap();
        assert_eq!(security.held[0].as_ptr(), ptr);
        assert_eq!(security.held[0], b"held");
        security.capture(b"more").unwrap();
    }
    assert_eq!(
        original.used(),
        Cost {
            objects: 2,
            edges: 5,
            bytes: 32
        }
    );
    original
        .charge::<()>(Cost {
            edges: 1,
            ..Cost::default()
        })
        .unwrap();
    assert_eq!(original.used().edges, 6);
}

#[test]
fn nested_platform_failure_survives_cache_drop_and_host_catch() {
    let mut original = WorkLedger::new();
    {
        let mut security = HeldCache::new(&mut original);
        security.capture(b"held").unwrap();
        let result = security.platform_work(|same| {
            assert!(
                same.charge::<()>(Cost {
                    bytes: usize::MAX,
                    ..Cost::default()
                })
                .is_err()
            );
            Ok(())
        });
        assert_eq!(result, Err(Failure::Budget(BudgetFailure::Closed)));
        assert_eq!(security.held[0], b"held");
    }
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
