// X3d r9 S10.7 (J3b): latch consumes the operation's single token.
use opensip_security::{CancellationLatch, D9Signal, LatchOutcome};
pub fn case(token: CancellationLatch) -> LatchOutcome {
    #[cfg(x8_misuse)]
    { let _ = token.latch(D9Signal::Sigint);
      token.latch(D9Signal::Sigterm) //~ ERROR E0382 "use of moved value: `token`"
    }
    #[cfg(not(x8_misuse))]
    token.latch(D9Signal::Sigint)
}
