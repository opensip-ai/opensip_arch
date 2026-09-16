#![forbid(unsafe_code)]
mod arguments;
mod bootstrap;
mod terminal;
fn main() -> std::process::ExitCode {
    std::process::ExitCode::from(bootstrap::run(std::env::args_os().skip(1)))
}
