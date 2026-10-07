// Law X8 r3 group D (unit J3b; X3d r9 S10.7): the cancellation latch cannot be read back from
// serialized bytes; it has no `Deserialize`.
use opensip_security::CancellationLatch;

#[cfg(x8_misuse)]
pub fn case(text: &str) -> Option<CancellationLatch> {
    serde_json::from_str::<CancellationLatch>(text).ok() //~ ERROR E0277 "the trait bound `CancellationLatch: serde::Deserialize<'de>` is not satisfied"
}

#[cfg(not(x8_misuse))]
pub fn case(text: &str) -> Option<serde_json::Value> {
    serde_json::from_str::<serde_json::Value>(text).ok()
}
