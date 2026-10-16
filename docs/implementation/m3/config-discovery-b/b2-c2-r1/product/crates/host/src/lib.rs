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

// Law X12 r3 (unit X12b): policy-pack admission; law M3-B r4 (unit B1-a): the
// configuration resolver and the X12 r4 order. Library only; no analysis
// request calls it yet (B1-b captures the carriers).
#[allow(dead_code)]
mod configuration;

// M3-B r5 item 3 (unit B1-b): the one computation of the invocation mode.
// Library only; J1 wires the host entry's call.
#[allow(dead_code)]
mod invocation_mode;

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

// M3-B r7 item 14 (unit B2-c1): the native unit instrument, pure. Library
// only; J1 composes it with the walker, C1's inventory and the resolver.
#[allow(dead_code)]
mod discovery;
// Its vectors build admitted inventories through security's scenario seam.
#[cfg(all(test, target_os = "macos"))]
mod discovery_tests;

// M3-B r8 item 14a (unit B2-c2): the first-party JSONC reader and the
// pre-Plan TypeScript configuration graph with effective `allowJs`. Pure and
// library only; J1 composes it with C1's snapshot custody.
#[allow(dead_code)]
mod jsonc;
#[allow(dead_code)]
mod typescript_config;
#[cfg(all(test, target_os = "macos"))]
mod typescript_config_tests;

#[cfg(test)]
mod native_owner_tests;
// M3-B unit B2-b3c: the COV:5288 and COV:5388 rows through security's
// scenario seam, beside the resolver they use (its own module: the
// configuration module's test pin holds that module's includes exactly).
#[cfg(all(test, target_os = "macos"))]
mod discovery_flag_tests;

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

// Plain supplied-stream data only; owning custody and source admission remain external.
#[allow(dead_code)]
mod raw_stream_copy;

// Complete native manifest array/frame recipes over supplied observations, data only.
#[allow(dead_code)]
mod native_file_manifest;

// Bound NKC-1 exact key data recipes only; original observation and owner admission remain external.
#[allow(dead_code)]
mod native_key_data;

// MWS-1 supplied opaque-id source-class data only; actual metadata/activation remain external.
#[allow(dead_code)]
mod workspace_source_data;

// Raw tuple ordering data only; no source census, duplicate resolution or admission.
#[allow(dead_code)]
mod native_candidate_order;

// RSD-1: private RUST3-LIM scope recipe data; no manifest/provider admission.
#[allow(dead_code)]
mod rust_scope_data;

// DT-MD1 is an inert entries-array recipe; transport and source admission remain owed.
#[allow(dead_code)]
mod dependency_transport_digest;

// NCA-1 supplied key-path/set data only; actual config classification and custody stay external.
#[allow(dead_code)]
mod native_config_key_record_data;
