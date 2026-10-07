// Law X8 r3 group E (unit J3b; X3d r9 S10.7): the cancellation latch cannot be cloned.
use opensip_security::CancellationLatch;

fn probe<T: Clone>() {}

pub fn case(_: &CancellationLatch) {
    #[cfg(x8_misuse)]
    probe::<CancellationLatch>(); //~ ERROR E0277 "the trait bound `CancellationLatch: Clone` is not satisfied"
    #[cfg(not(x8_misuse))]
    probe::<u8>();
}
