// X3d r9 S10.7 (J3b): only the session can mint the token.
use opensip_security::CancellationLatch;
#[cfg(x8_misuse)]
pub fn case() -> CancellationLatch {
    CancellationLatch(()) //~ ERROR E0423 "cannot initialize a tuple struct which contains private fields"
}
#[cfg(not(x8_misuse))]
pub fn case(token: CancellationLatch) -> CancellationLatch {
    fn is_send<T: Send>(value: T) -> T { value }
    is_send(token)
}
