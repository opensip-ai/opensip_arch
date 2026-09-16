//! Refuse ambient selection of a different entropy backend in host builds.
//! The compiler/toolchain itself remains a separately trusted build input.
use std::env;

fn main() {
    println!("cargo:rerun-if-env-changed=CARGO_CFG_GETRANDOM_BACKEND");
    println!("cargo:rerun-if-env-changed=CARGO_ENCODED_RUSTFLAGS");
    // Cargo exposes effective --cfg values after applying environment and
    // .cargo/config flags. No explicit getrandom backend is selected for this
    // platform crate: the pinned dependency must choose its target default.
    if env::var_os("CARGO_CFG_GETRANDOM_BACKEND").is_some() {
        panic!(
            "OpenSIP refuses an explicit getrandom_backend override; use the selected platform default"
        );
    }
}
