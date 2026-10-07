// Law X8 r3 group G (unit J3b; X3d r9 S10.7): the cancellation latch cannot be serialized as a
// previous session.
use opensip_security::CancellationLatch;

pub fn case(session: &CancellationLatch) -> Option<String> {
    #[cfg(x8_misuse)]
    return serde_json::to_string(session).ok(); //~ ERROR E0277 "the trait bound `CancellationLatch: serde::Serialize` is not satisfied"
    #[cfg(not(x8_misuse))]
    {
        let _ = session;
        serde_json::to_string(&0u8).ok()
    }
}
