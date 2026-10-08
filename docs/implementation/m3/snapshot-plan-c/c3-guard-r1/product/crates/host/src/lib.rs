#![forbid(unsafe_code)]

// Law X9 r1 item 2, guard 1: the crash barrier never reaches a build without
// debug assertions, so a release-profile build with the feature fails here.
#[cfg(all(feature = "crash-matrix", not(debug_assertions)))]
compile_error!(
    "the crash-matrix feature is test-only (law X9 r1 item 2) and refuses every build without debug assertions"
);
// Law X9 r1 item 6 (unit X9-1): the crash matrix's synthetic support
// surface, only under the test-only feature.
#[cfg(all(feature = "crash-matrix", target_os = "macos"))]
#[doc(hidden)]
pub mod crash_matrix_support;
mod delivery;
// Law M3-J1 r5 (unit J2a): beside the metadata ingress, this module holds
// item 10's M3 outcome matrix, and `invocation` the pure request, step-list,
// join, cancellation and settlement model. Library only: no analysis
// request reaches either before J2c and J3d, and no analysis word is wired
// in the binary (item 1).
#[allow(dead_code)]
mod invocation;
#[allow(dead_code)]
mod outcomes;
mod request;
pub use delivery::deliver_required;

/// One finalization of optional logging. A later call does nothing once the summary is frozen.
/// Metadata paths pass `cancelled = false`. The allocation-failure return does not call this.
pub fn finalize_invocation(cancelled: bool) {
    opensip_operability::finalize(cancelled);
}
pub use outcomes::{Format, MetadataError, MetadataHost, MetadataRequest, RenderedResponse};
pub use request::{
    InstallationEntry, InstallationEntryError, RequestAllocationError, RequestContext,
    installation_entry, installation_precondition,
};

mod schema_sources;
pub use schema_sources::embedded_schema_registry;

mod installation_termination;
pub use installation_termination::{InstallationTerminationV1, installation_termination};

mod doctor_ingress;

// Law X6 r3 items 6 and 8 (unit X6b): read-only recovery's read-entry route.
// Library only; no CLI command calls it before X11.
#[cfg(target_os = "macos")]
#[allow(dead_code)]
mod recovery_route;

// Law X6 r3 item 7 (unit X6c): `store-gc`'s per-namespace settlement sweep
// step. Library only; no CLI command calls it before X11.
#[cfg(target_os = "macos")]
#[allow(dead_code)]
mod maintenance;

// Law X5 r3 (unit X5a): the replay join. Library only; host finalization
// (X7a) is its one caller.
#[allow(dead_code)]
mod fact_admission;

// Law X12 r3 (unit X12b): policy-pack admission. Library only; no analysis
// request calls it before M3.
#[allow(dead_code)]
mod configuration;

// Law X7 r5 (unit X7a): host finalization, the one commit coordinator.
// Library only; no CLI command calls it (X11). The authoritative projection
// is exported so that its signature is pinned from outside (law X8 r3 item
// 3c); it takes only storage's `PublishedCommit`.
#[cfg(target_os = "macos")]
#[allow(dead_code)]
mod finalization;
#[cfg(target_os = "macos")]
pub use finalization::{AuthoritativeRun, authoritative_run};
mod doctor_report;
pub use doctor_report::{
    DURABILITY_NOT_CHECKED_LABEL, DURABILITY_NOT_CHECKED_REMEDY, DoctorOutcome,
    DoctorReportSession, DoctorReportV1, DoctorTerminationV1, REMEDY_CHAIN, REMEDY_MARKER,
    REMEDY_MISSING, REMEDY_NODE, REMEDY_PAIR, REMEDY_STORE, ReportUnavailable,
};
#[cfg(target_os = "macos")]
pub use doctor_report::{doctor_installation, installation_defect};

#[cfg(test)]
mod native_owner_tests;

#[cfg(target_os = "macos")]
pub mod installation_selection;

#[cfg(target_os = "macos")]
pub mod installation_records;

#[cfg(target_os = "macos")]
pub mod installation_trust;

#[cfg(target_os = "macos")]
pub mod installation_lineage;

// C3a supporting decoder library only; no source/import/owner admission or CLI route.
#[allow(dead_code)]
mod archive_decoder;

// Library-only arithmetic; the importer owns observation and admission.
#[allow(dead_code)]
mod dependency_counters;

// Library-only logical acquisition guard; custody and admission stay with imports.
#[allow(dead_code)]
mod acquisition_guard;
