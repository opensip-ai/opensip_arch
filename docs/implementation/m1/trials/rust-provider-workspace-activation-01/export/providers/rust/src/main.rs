//! Development workspace entry point. No native-analysis provider is advertised.
//!
//! Protocol negotiation and compiler integration are implemented at M3. Until
//! those exist this binary exits before reading a request or acknowledging any
//! capabilities. A development build cannot substitute synthetic analysis.
use std::io::{self, Write};
use std::process::ExitCode;

fn main() -> ExitCode {
    let _ = writeln!(
        io::stderr().lock(),
        "opensip Rust provider: native analysis is not implemented in this development build"
    );
    ExitCode::FAILURE
}
