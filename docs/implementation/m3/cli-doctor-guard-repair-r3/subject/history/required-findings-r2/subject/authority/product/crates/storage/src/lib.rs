//! Private storage groundwork under supplied custody; no public write authority.
#![forbid(unsafe_code)]

// Law X9 r1 item 2, guard 1: the crash barrier never reaches a build without
// debug assertions, so a release-profile build with the feature fails here.
#[cfg(all(feature = "crash-matrix", not(debug_assertions)))]
compile_error!(
    "the crash-matrix feature is test-only (law X9 r1 item 2) and refuses every build without debug assertions"
);
// Law X9 r1 item 6 (unit X9-1): the crash matrix's synthetic support
// surface, only under the test-only feature.
#[allow(dead_code)]
mod availability;
#[allow(dead_code)]
mod blob_store;
#[cfg(all(feature = "crash-matrix", target_os = "macos"))]
#[doc(hidden)]
pub mod crash_matrix_support;
#[allow(dead_code)]
mod ledger_store;
#[allow(dead_code)]
mod recovery;
// Law X8 r3 item 4d (unit X8b): the refusal suite's ledger seam, only under
// the test-only feature that host's `[dev-dependencies]` enable.
#[cfg(all(feature = "scenario-fixtures", target_os = "macos"))]
#[doc(hidden)]
pub mod scenario;

#[allow(dead_code)]
mod pin_inventory;

#[allow(dead_code)]
mod store_root;

#[cfg(target_os = "macos")]
pub use store_root::native_marker::{Error as StoreMarkerObservationError, ProvisionalStoreMarker};

// Law X3d r6 (unit X3d-2): the commit facade. `prepare_commit` takes the
// evaluator's opaque `ReplayedRun` and security's live `CommitSession`; its
// types have no public constructor and are not Clone, Default or
// serializable (law X8 r3 groups A to H).
#[cfg(target_os = "macos")]
mod commit;
#[cfg(target_os = "macos")]
pub use commit::{CommitOutcome, NotPrepared, PreparedCommit, PublishedCommit, prepare_commit};
// Law X6 r3 (unit X6b): read-only recovery's `recover` and its closed
// result, over security's `RecoveryAdmission`. Nothing here writes.
#[cfg(target_os = "macos")]
mod recover;
#[cfg(target_os = "macos")]
pub use recover::{
    INTERIOR_BODIES_NOT_AUTHENTICATED, RecoveredCommit, RecoveryFailure, Unavailable,
    UnavailableObject, recover,
};
// Law X6 r3 item 7 (unit X6c): the authorized settlement sweep's storage
// step, over security's `SweepLease`. Its one write is the settle
// transition in `ledger_store`.
#[cfg(target_os = "macos")]
mod sweep;
#[cfg(target_os = "macos")]
pub use sweep::{LeftAttempt, NamespaceSweep, SettledOutcome, SweepStop, sweep_namespace};
#[cfg(target_os = "macos")]
mod schema_sources;

/// F3's per-process scratch parent for storage fixtures that need a real
/// directory tree: `<temp>/opensip-test/<pid>-<draw>`, created once with mode
/// 0700. Fixtures below it never add or remove entries in the shared system
/// temporary directory, so other processes' walkers see no churn from them.
#[cfg(test)]
mod test_scratch {
    static PRIVATE: std::sync::OnceLock<std::path::PathBuf> = std::sync::OnceLock::new();
    pub(crate) fn temp_dir() -> std::path::PathBuf {
        PRIVATE
            .get_or_init(|| {
                use std::os::unix::fs::DirBuilderExt;
                let shared = std::env::temp_dir().join("opensip-test");
                match std::fs::DirBuilder::new().mode(0o700).create(&shared) {
                    Ok(()) => {}
                    Err(e) if e.kind() == std::io::ErrorKind::AlreadyExists => {}
                    Err(e) => panic!("opensip-test scratch parent: {e}"),
                }
                // Law X9 r2 item 3: no wall reading names it (a matrix
                // child takes none from the OS); a fresh draw does.
                let draw: String = opensip_platform::request_entropy()
                    .expect("entropy")
                    .iter()
                    .map(|b| format!("{b:02x}"))
                    .collect();
                let private = shared.join(format!("{}-{draw}", std::process::id()));
                std::fs::DirBuilder::new()
                    .mode(0o700)
                    .create(&private)
                    .unwrap_or_else(|e| panic!("private scratch parent: {e}"));
                private
            })
            .clone()
    }
}
