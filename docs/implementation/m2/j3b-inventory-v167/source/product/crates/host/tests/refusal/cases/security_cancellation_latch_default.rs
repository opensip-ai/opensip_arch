// Law X8 r3 group D (unit J3b; X3d r9 S10.7): the cancellation latch has no `Default`.
use opensip_security::CancellationLatch;

fn probe<T: Default>() {}

pub fn case(_: &CancellationLatch) {
    #[cfg(x8_misuse)]
    probe::<CancellationLatch>(); //~ ERROR E0277 "the trait bound `CancellationLatch: Default` is not satisfied"
    #[cfg(not(x8_misuse))]
    probe::<u8>();
}
