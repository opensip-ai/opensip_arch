#![deny(unsafe_code)]

// Unsafe FFI is confined to the selected OS adapters; other platform modules
// keep the crate-wide denial. These handles do not establish policy or trust.
#[cfg(any(target_os = "macos", target_os = "linux"))]
#[allow(unsafe_code)]
mod filesystem;
#[cfg(any(target_os = "macos", target_os = "linux"))]
pub use filesystem::{
    DirectoryBarrier, DirectoryVisitError, DirectoryVisitSummary, ExistingFileReceipt,
    NewFileReceipt, PublicationFailure, PublicationStage, ReplacementReceipt,
    RetainedChildDirectory, RetainedDirectory, RetainedDirectoryPath, TargetVisibility,
};

/// Failure to obtain a complete independent OS CSPRNG draw.
#[derive(Debug)]
pub struct EntropyError;

/// Operational correlation only; never an input to semantic identity.
pub fn request_entropy() -> Result<[u8; 16], EntropyError> {
    let mut value = [0; 16];
    getrandom::fill(&mut value).map_err(|_| EntropyError)?;
    Ok(value)
}

/// A complete 256-bit OS CSPRNG draw for a host recovery challenge.
/// Failure returns no nonce. Entropy is not a custody or authorization token.
pub fn recovery_nonce() -> Result<[u8; 32], EntropyError> {
    let mut value = [0; 32];
    getrandom::fill(&mut value).map_err(|_| EntropyError)?;
    Ok(value)
}

#[cfg(any(target_os = "macos", target_os = "linux"))]
#[allow(unsafe_code)]
mod locks;
#[cfg(any(target_os = "macos", target_os = "linux"))]
pub use locks::{FileLock, LockMode};

#[cfg(any(target_os = "macos", target_os = "linux"))]
mod clock;
#[cfg(target_os = "linux")]
#[allow(unsafe_code)]
mod linux;
#[cfg(target_os = "macos")]
#[allow(unsafe_code)]
mod macos;
#[cfg(any(target_os = "macos", target_os = "linux"))]
pub use clock::{ClockError, ClockObservation, observe_clock};

#[cfg(any(target_os = "macos", target_os = "linux"))]
pub use filesystem::{
    AclWriter, DescriptorFilesystem, DescriptorMetadata, DescriptorObservation,
    DescriptorObservationError, descriptor_name_matches, observe_descriptor, observe_filesystem,
};

/// Obtain the macOS per-account temporary location, independent of HOME/TMPDIR.
/// The OS may create the directory as a side effect. Never call on a write-free
/// admission or report-only path; current callers are test fixtures only.
/// The returned path may contain symlinked components or a trailing separator.
/// It is not canonical or admitted custody, storage selection or creation consent.
/// Resolve its location, then separately admit every retained directory component.
#[cfg(target_os = "macos")]
pub fn account_temporary_directory() -> std::io::Result<std::path::PathBuf> {
    macos::account_temporary_directory()
}

#[cfg(any(target_os = "macos", target_os = "linux"))]
#[allow(unsafe_code)]
mod account;
#[cfg(any(target_os = "macos", target_os = "linux"))]
pub use account::{AccountObservation, AccountObservationError, observe_account};

// Read-only native macOS identity samples; no profile or execution authority.
#[cfg(any(target_os = "macos", target_os = "linux"))]
#[cfg_attr(target_os = "macos", allow(unsafe_code))]
mod macos_boot;
#[cfg(any(target_os = "macos", target_os = "linux"))]
pub use macos_boot::{MacosBootError, MacosBootObservation, observe_macos_boot};

#[cfg(target_os = "macos")]
#[allow(unsafe_code)]
mod macos_loader;
#[cfg(target_os = "macos")]
pub use macos_loader::{MacosLoaderError, MacosLoaderObservation, capture_system_loader};

#[cfg(target_os = "macos")]
#[allow(unsafe_code)]
mod macos_process;
#[cfg(target_os = "macos")]
pub use macos_process::{MacosProcessError, MacosProcessObservation, observe_macos_process};
