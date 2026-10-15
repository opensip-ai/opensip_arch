//! M3-B r5 item 3 (unit B1-b): the invocation mode, computed once. An
//! invocation is interactive exactly when standard input and standard error
//! are both terminals; every other invocation is CI. No environment variable
//! (`CI`, `TERM` or any other) is consulted. J1 wires the call at the host
//! entry; the resolver and the carrier capture consume the result.
use crate::invocation::InvocationModeV1;
use std::io::IsTerminal;

/// The rule itself, over the two observations.
pub(crate) fn invocation_mode(stdin_terminal: bool, stderr_terminal: bool) -> InvocationModeV1 {
    InvocationModeV1 {
        interactive: stdin_terminal && stderr_terminal,
    }
}

/// The host entry's one observation of this process's standard input and
/// standard error.
pub(crate) fn observe_invocation_mode() -> InvocationModeV1 {
    invocation_mode(
        std::io::stdin().is_terminal(),
        std::io::stderr().is_terminal(),
    )
}

#[cfg(test)]
mod tests {
    include!("invocation_mode_tests.rs");
}
