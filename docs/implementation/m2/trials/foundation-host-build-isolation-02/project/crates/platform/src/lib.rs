#![deny(unsafe_code)]

// Only the audited OS adapter may use unsafe FFI; all other platform modules
// keep the crate-wide denial. This does not add policy or trust to the handles.
#[cfg(any(target_os = "macos", target_os = "linux"))]
#[allow(unsafe_code)]
mod filesystem;
#[cfg(any(target_os = "macos", target_os = "linux"))]
pub use filesystem::RetainedDirectory;

/// Failure to obtain a complete independent OS CSPRNG draw.
#[derive(Debug)]
pub struct EntropyError;

/// Operational correlation only; never an input to semantic identity.
pub fn request_entropy() -> Result<[u8; 16], EntropyError> {
    let mut value = [0; 16];
    getrandom::fill(&mut value).map_err(|_| EntropyError)?;
    Ok(value)
}
