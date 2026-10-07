// Public-boundary scenarios (build plan, "Required API and fault-injection
// checks"). Unit X8a of law X8 r3 (the opaque API refusal suite): the
// compile-fail fixture driver, its census and self-test, groups I, K and L,
// and the `scenario-fixtures` manifest pin. Unit X4a adds group D's
// unnameable rows for `AdmissionPermit`, `FinalGate` and `OperationGuard`.
// Unit X3d-1 adds the session types' rows of groups D, E, F and G. Unit
// X3d-2 adds storage's facade rows of groups A to E, G and H for
// `prepare_commit`, `PreparedCommit` and `PublishedCommit`, and item 3b's
// adapter source pin. Unit X5a adds group C's unnameable `RunCandidateInputs`
// and group E's `ReplayedRun` reuse. Unit X7a adds the authoritative
// projection's rows A and B and, for its exported `AuthoritativeRun`, the
// capability rows D, E and G. Unit X8b adds group J's unresolved
// `scenario` modules; `scenario-fixtures` reaches this crate's tests only
// through its `[dev-dependencies]`. Unit X8c adds item 5's behavioural cases
// B0 to B8 (the `synthetic_…` tests at the end of this file), item 5a's
// revocation helper entry, and the run candidate's registry pin.
//
// Each case under `tests/refusal/cases/` is compiled by the pinned rustc
// against the `.rmeta` files of a plain `cargo check -p opensip-host` (the
// release public surface: no `cfg(test)`, no dev-dependencies, no features),
// twice: once as the lawful control, which must compile, and once with
// `--cfg x8_misuse`, which must fail with exactly one error carrying the
// annotated code, message fragment and line. Message fragments are rustc
// 1.95.0's English text; a re-pin re-checks every one in the same unit.
// Synthetic fixtures; no compiler qualification is claimed.
use serde_json::Value;
use std::collections::{BTreeMap, BTreeSet};
use std::path::{Path, PathBuf};
use std::process::Command;
use std::time::Instant;

/// The `rust-toolchain.toml` pin, as `rustc -vV` reports it.
const PINNED_RELEASE: &str = "release: 1.95.0";
/// The annotation marker. Exactly one per case.
const MARKER: &str = "//~";

/// Law X8 r3 item 1f: the categories of build-plan lines 597–598 and 1071,
/// each of which must have a case, and the two further categories of
/// groups I and L.
#[derive(Clone, Copy, Debug, PartialEq, Eq, PartialOrd, Ord)]
enum Category {
    RawDto,
    BooleanVerified,
    StructuralOnly,
    SerializedPreviousSession,
    ForgedReceipt,
    ClonedOrReused,
    PrivateConstructor,
    /// Group I: storage's ledger internals are unnameable.
    StorageInternals,
    /// Group J: the test-only `scenario` seams are absent from the plain
    /// surface.
    TestSeam,
    /// Group L: a borrowed scope, fence or session confined to its owner.
    ScopeConfinement,
}

const REQUIRED_CATEGORIES: [Category; 7] = [
    Category::RawDto,
    Category::BooleanVerified,
    Category::StructuralOnly,
    Category::SerializedPreviousSession,
    Category::ForgedReceipt,
    Category::ClonedOrReused,
    Category::PrivateConstructor,
];

/// One census row: law X8 r3 item 1f's `(file, owning crate, type, unit,
/// category)`, with the item 3 group it belongs to.
struct Case {
    file: &'static str,
    krate: &'static str,
    ty: &'static str,
    unit: &'static str,
    group: char,
    category: Category,
}

const fn case(
    file: &'static str,
    krate: &'static str,
    ty: &'static str,
    group: char,
    category: Category,
) -> Case {
    Case {
        file,
        krate,
        ty,
        unit: "X8a",
        group,
        category,
    }
}

/// An owner unit's row (law X8 r3 item 3's "Owner rows, added by their
/// units").
const fn owned(
    file: &'static str,
    krate: &'static str,
    ty: &'static str,
    unit: &'static str,
    group: char,
    category: Category,
) -> Case {
    Case {
        file,
        krate,
        ty,
        unit,
        group,
        category,
    }
}

/// The case table (law X8 r3 item 3). Owner units add their rows here.
const CASES: &[Case] = &[
    owned(
        "security_cancellation_latch_literal.rs",
        "opensip_security",
        "CancellationLatch",
        "J3b",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "security_cancellation_latch_default.rs",
        "opensip_security",
        "CancellationLatch",
        "J3b",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "security_cancellation_latch_deserialize.rs",
        "opensip_security",
        "CancellationLatch",
        "J3b",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "security_cancellation_latch_clone.rs",
        "opensip_security",
        "CancellationLatch",
        "J3b",
        'E',
        Category::ClonedOrReused,
    ),
    owned(
        "security_cancellation_latch_serialize.rs",
        "opensip_security",
        "CancellationLatch",
        "J3b",
        'G',
        Category::SerializedPreviousSession,
    ),
    owned(
        "security_cancellation_latch_reuse.rs",
        "opensip_security",
        "CancellationLatch",
        "J3b",
        'E',
        Category::ClonedOrReused,
    ),
    // Group D (unit X4a): the operation's commit permit, its one gate and
    // its live guard are crate-private, so each is unnameable (E0603).
    owned(
        "security_admission_permit_unnameable.rs",
        "opensip_security",
        "AdmissionPermit",
        "X4a",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "security_final_gate_unnameable.rs",
        "opensip_security",
        "FinalGate",
        "X4a",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "security_operation_guard_unnameable.rs",
        "opensip_security",
        "OperationGuard",
        "X4a",
        'D',
        Category::ForgedReceipt,
    ),
    // Unit X3d-1 (law X8 r3 item 3, owner rows): the session types
    // `CommitSession`, `JournalWriteTxn`, `JournalSealBinding` and
    // `StoppedSession`, and `ProjectOperation`, which X3d-1 exports because
    // the public `CommitSession::open` takes it, are exported, so each has
    // the full capability set: a literal, `Default` and `Deserialize`
    // (group D), `Clone` and reuse (group E), `Serialize` (group G); the
    // `open` arity case and item 3a's census of every non-public inherent
    // function and cfg(test) producer (group F).
    owned(
        "security_commit_session_literal.rs",
        "opensip_security",
        "CommitSession",
        "X3d-1",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "security_commit_session_default.rs",
        "opensip_security",
        "CommitSession",
        "X3d-1",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "security_commit_session_deserialize.rs",
        "opensip_security",
        "CommitSession",
        "X3d-1",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "security_commit_session_clone.rs",
        "opensip_security",
        "CommitSession",
        "X3d-1",
        'E',
        Category::ClonedOrReused,
    ),
    owned(
        "security_commit_session_serialize.rs",
        "opensip_security",
        "CommitSession",
        "X3d-1",
        'G',
        Category::SerializedPreviousSession,
    ),
    owned(
        "security_journal_write_txn_literal.rs",
        "opensip_security",
        "JournalWriteTxn",
        "X3d-1",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "security_journal_write_txn_default.rs",
        "opensip_security",
        "JournalWriteTxn",
        "X3d-1",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "security_journal_write_txn_deserialize.rs",
        "opensip_security",
        "JournalWriteTxn",
        "X3d-1",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "security_journal_write_txn_clone.rs",
        "opensip_security",
        "JournalWriteTxn",
        "X3d-1",
        'E',
        Category::ClonedOrReused,
    ),
    owned(
        "security_journal_write_txn_serialize.rs",
        "opensip_security",
        "JournalWriteTxn",
        "X3d-1",
        'G',
        Category::SerializedPreviousSession,
    ),
    owned(
        "security_journal_seal_binding_literal.rs",
        "opensip_security",
        "JournalSealBinding",
        "X3d-1",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "security_journal_seal_binding_default.rs",
        "opensip_security",
        "JournalSealBinding",
        "X3d-1",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "security_journal_seal_binding_deserialize.rs",
        "opensip_security",
        "JournalSealBinding",
        "X3d-1",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "security_journal_seal_binding_clone.rs",
        "opensip_security",
        "JournalSealBinding",
        "X3d-1",
        'E',
        Category::ClonedOrReused,
    ),
    owned(
        "security_journal_seal_binding_serialize.rs",
        "opensip_security",
        "JournalSealBinding",
        "X3d-1",
        'G',
        Category::SerializedPreviousSession,
    ),
    owned(
        "security_stopped_session_literal.rs",
        "opensip_security",
        "StoppedSession",
        "X3d-1",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "security_stopped_session_default.rs",
        "opensip_security",
        "StoppedSession",
        "X3d-1",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "security_stopped_session_deserialize.rs",
        "opensip_security",
        "StoppedSession",
        "X3d-1",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "security_stopped_session_clone.rs",
        "opensip_security",
        "StoppedSession",
        "X3d-1",
        'E',
        Category::ClonedOrReused,
    ),
    owned(
        "security_stopped_session_serialize.rs",
        "opensip_security",
        "StoppedSession",
        "X3d-1",
        'G',
        Category::SerializedPreviousSession,
    ),
    owned(
        "security_project_operation_literal.rs",
        "opensip_security",
        "ProjectOperation",
        "X3d-1",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "security_project_operation_default.rs",
        "opensip_security",
        "ProjectOperation",
        "X3d-1",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "security_project_operation_deserialize.rs",
        "opensip_security",
        "ProjectOperation",
        "X3d-1",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "security_project_operation_clone.rs",
        "opensip_security",
        "ProjectOperation",
        "X3d-1",
        'E',
        Category::ClonedOrReused,
    ),
    owned(
        "security_project_operation_serialize.rs",
        "opensip_security",
        "ProjectOperation",
        "X3d-1",
        'G',
        Category::SerializedPreviousSession,
    ),
    owned(
        "security_project_operation_open_twice.rs",
        "opensip_security",
        "ProjectOperation",
        "X3d-1",
        'E',
        Category::ClonedOrReused,
    ),
    owned(
        "security_commit_session_reused.rs",
        "opensip_security",
        "CommitSession",
        "X3d-1",
        'E',
        Category::ClonedOrReused,
    ),
    owned(
        "security_journal_write_txn_reused.rs",
        "opensip_security",
        "JournalWriteTxn",
        "X3d-1",
        'E',
        Category::ClonedOrReused,
    ),
    owned(
        "security_stopped_session_finish_twice.rs",
        "opensip_security",
        "StoppedSession",
        "X3d-1",
        'E',
        Category::ClonedOrReused,
    ),
    owned(
        "security_commit_session_open_arity.rs",
        "opensip_security",
        "CommitSession",
        "X3d-1",
        'F',
        Category::PrivateConstructor,
    ),
    owned(
        "security_ordinary_writer_unnameable.rs",
        "opensip_security",
        "OrdinaryWriteAdmission",
        "X3d-1",
        'F',
        Category::PrivateConstructor,
    ),
    owned(
        "security_project_operation_binding_private.rs",
        "opensip_security",
        "ProjectOperation",
        "X3d-1",
        'F',
        Category::PrivateConstructor,
    ),
    owned(
        "security_project_operation_row_private.rs",
        "opensip_security",
        "ProjectOperation",
        "X3d-1",
        'F',
        Category::PrivateConstructor,
    ),
    owned(
        "security_project_operation_mode_private.rs",
        "opensip_security",
        "ProjectOperation",
        "X3d-1",
        'F',
        Category::PrivateConstructor,
    ),
    owned(
        "security_project_operation_subject_private.rs",
        "opensip_security",
        "ProjectOperation",
        "X3d-1",
        'F',
        Category::PrivateConstructor,
    ),
    owned(
        "security_project_operation_endpoint_private.rs",
        "opensip_security",
        "ProjectOperation",
        "X3d-1",
        'F',
        Category::PrivateConstructor,
    ),
    owned(
        "security_project_operation_required_private.rs",
        "opensip_security",
        "ProjectOperation",
        "X3d-1",
        'F',
        Category::PrivateConstructor,
    ),
    owned(
        "security_project_operation_selected_core_private.rs",
        "opensip_security",
        "ProjectOperation",
        "X3d-1",
        'F',
        Category::PrivateConstructor,
    ),
    owned(
        "security_project_operation_carrier_private.rs",
        "opensip_security",
        "ProjectOperation",
        "X3d-1",
        'F',
        Category::PrivateConstructor,
    ),
    owned(
        "security_project_operation_guard_private.rs",
        "opensip_security",
        "ProjectOperation",
        "X3d-1",
        'F',
        Category::PrivateConstructor,
    ),
    owned(
        "security_project_operation_attempt_closed_private.rs",
        "opensip_security",
        "ProjectOperation",
        "X3d-1",
        'F',
        Category::PrivateConstructor,
    ),
    owned(
        "security_project_operation_charge_private.rs",
        "opensip_security",
        "ProjectOperation",
        "X3d-1",
        'F',
        Category::PrivateConstructor,
    ),
    owned(
        "security_project_operation_reserve_end_path_settlement_private.rs",
        "opensip_security",
        "ProjectOperation",
        "X3d-1",
        'F',
        Category::PrivateConstructor,
    ),
    owned(
        "security_project_operation_settle_end_path_private.rs",
        "opensip_security",
        "ProjectOperation",
        "X3d-1",
        'F',
        Category::PrivateConstructor,
    ),
    owned(
        "security_project_operation_journal_private.rs",
        "opensip_security",
        "ProjectOperation",
        "X3d-1",
        'F',
        Category::PrivateConstructor,
    ),
    owned(
        "security_project_operation_end_private.rs",
        "opensip_security",
        "ProjectOperation",
        "X3d-1",
        'F',
        Category::PrivateConstructor,
    ),
    owned(
        "security_project_operation_end_with_private.rs",
        "opensip_security",
        "ProjectOperation",
        "X3d-1",
        'F',
        Category::PrivateConstructor,
    ),
    owned(
        "security_project_operation_lease_mut_private.rs",
        "opensip_security",
        "ProjectOperation",
        "X3d-1",
        'F',
        Category::PrivateConstructor,
    ),
    owned(
        "security_project_operation_carrier_mut_private.rs",
        "opensip_security",
        "ProjectOperation",
        "X3d-1",
        'F',
        Category::PrivateConstructor,
    ),
    owned(
        "security_project_operation_attempt_used_private.rs",
        "opensip_security",
        "ProjectOperation",
        "X3d-1",
        'F',
        Category::PrivateConstructor,
    ),
    // Unit X3d-2 (law X8 r3 item 3, owner rows): storage's facade. Rows A,
    // B and C hold `prepare_commit` to the evaluator's `ReplayedRun`; the
    // exported `PreparedCommit` and `PublishedCommit` have the full
    // capability set (D, E, G), with the reuse of a consumed session and a
    // second `publish` (E); group H pins that the facade takes no external
    // adapter or `SealOutcome` (E0061). Neither type has a non-public inherent
    // function or a cfg(test) producer, so item 3a's census adds no F row.
    owned(
        "storage_prepare_commit_raw_json.rs",
        "opensip_storage",
        "ReplayedRun",
        "X3d-2",
        'A',
        Category::RawDto,
    ),
    owned(
        "storage_prepare_commit_contracts_run.rs",
        "opensip_storage",
        "ReplayedRun",
        "X3d-2",
        'A',
        Category::RawDto,
    ),
    owned(
        "storage_prepare_commit_bool.rs",
        "opensip_storage",
        "ReplayedRun",
        "X3d-2",
        'B',
        Category::BooleanVerified,
    ),
    owned(
        "storage_published_commit_verified.rs",
        "opensip_storage",
        "PublishedCommit",
        "X3d-2",
        'B',
        Category::BooleanVerified,
    ),
    owned(
        "storage_prepare_commit_retained_inputs.rs",
        "opensip_storage",
        "ReplayedRun",
        "X3d-2",
        'C',
        Category::StructuralOnly,
    ),
    owned(
        "storage_prepared_commit_literal.rs",
        "opensip_storage",
        "PreparedCommit",
        "X3d-2",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "storage_prepared_commit_default.rs",
        "opensip_storage",
        "PreparedCommit",
        "X3d-2",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "storage_prepared_commit_deserialize.rs",
        "opensip_storage",
        "PreparedCommit",
        "X3d-2",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "storage_prepared_commit_clone.rs",
        "opensip_storage",
        "PreparedCommit",
        "X3d-2",
        'E',
        Category::ClonedOrReused,
    ),
    owned(
        "storage_prepared_commit_serialize.rs",
        "opensip_storage",
        "PreparedCommit",
        "X3d-2",
        'G',
        Category::SerializedPreviousSession,
    ),
    owned(
        "storage_published_commit_literal.rs",
        "opensip_storage",
        "PublishedCommit",
        "X3d-2",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "storage_published_commit_default.rs",
        "opensip_storage",
        "PublishedCommit",
        "X3d-2",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "storage_published_commit_deserialize.rs",
        "opensip_storage",
        "PublishedCommit",
        "X3d-2",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "storage_published_commit_clone.rs",
        "opensip_storage",
        "PublishedCommit",
        "X3d-2",
        'E',
        Category::ClonedOrReused,
    ),
    owned(
        "storage_published_commit_serialize.rs",
        "opensip_storage",
        "PublishedCommit",
        "X3d-2",
        'G',
        Category::SerializedPreviousSession,
    ),
    owned(
        "storage_prepare_commit_consumed_session.rs",
        "opensip_storage",
        "CommitSession",
        "X3d-2",
        'E',
        Category::ClonedOrReused,
    ),
    owned(
        "storage_prepared_commit_publish_twice.rs",
        "opensip_storage",
        "PreparedCommit",
        "X3d-2",
        'E',
        Category::ClonedOrReused,
    ),
    owned(
        "storage_prepared_commit_publish_adapter.rs",
        "opensip_storage",
        "PreparedCommit",
        "X3d-2",
        'H',
        Category::ForgedReceipt,
    ),
    owned(
        "storage_prepare_commit_seal_outcome.rs",
        "opensip_storage",
        "SealOutcome",
        "X3d-2",
        'H',
        Category::ForgedReceipt,
    ),
    // Group C (unit X5a): the build plan's inert `RunCandidate` is
    // crate-private to the host, so it is unnameable (E0603) and cannot stand
    // in for a `ReplayedRun` (X3d r6 item 11; X5 r3 item 5f).
    owned(
        "host_run_candidate_unnameable.rs",
        "opensip_host",
        "RunCandidateInputs",
        "X5a",
        'C',
        Category::StructuralOnly,
    ),
    // Group E (unit X5a): a `ReplayedRun` reaches one `prepare_commit` only.
    owned(
        "evaluator_replayed_second_prepare_commit.rs",
        "opensip_evaluator",
        "ReplayedRun",
        "X5a",
        'E',
        Category::ClonedOrReused,
    ),
    // Unit X7a (law X7 r3 items 2 and 10; law X8 r3 items 3 and 3c): the
    // exported authoritative projection takes `&PublishedCommit` and nothing
    // else: not a raw JSON Run (A), nor `true`, a RunId string or a replayed
    // but uncommitted Run (B). Its exported `AuthoritativeRun` has the full
    // capability set (D, E, G). It has no non-public inherent function and
    // no cfg(test) producer, so item 3a's census adds no F row.
    owned(
        "host_authoritative_run_raw_json.rs",
        "opensip_host",
        "authoritative_run",
        "X7a",
        'A',
        Category::RawDto,
    ),
    owned(
        "host_authoritative_run_bool.rs",
        "opensip_host",
        "authoritative_run",
        "X7a",
        'B',
        Category::BooleanVerified,
    ),
    owned(
        "host_authoritative_run_run_id.rs",
        "opensip_host",
        "authoritative_run",
        "X7a",
        'B',
        Category::BooleanVerified,
    ),
    owned(
        "host_authoritative_run_replayed.rs",
        "opensip_host",
        "authoritative_run",
        "X7a",
        'B',
        Category::BooleanVerified,
    ),
    owned(
        "host_authoritative_run_literal.rs",
        "opensip_host",
        "AuthoritativeRun",
        "X7a",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "host_authoritative_run_default.rs",
        "opensip_host",
        "AuthoritativeRun",
        "X7a",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "host_authoritative_run_deserialize.rs",
        "opensip_host",
        "AuthoritativeRun",
        "X7a",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "host_authoritative_run_clone.rs",
        "opensip_host",
        "AuthoritativeRun",
        "X7a",
        'E',
        Category::ClonedOrReused,
    ),
    owned(
        "host_authoritative_run_serialize.rs",
        "opensip_host",
        "AuthoritativeRun",
        "X7a",
        'G',
        Category::SerializedPreviousSession,
    ),
    // Unit J3a (law M3-J1 r6 item 2, controls J-C4 and J-C4b; X3d r9 S10.7):
    // the exported `RequestIdentity` and `ReservedExecutionId` have the full
    // capability set: a literal from bytes, `Default`, `Deserialize` and
    // conversions from bytes and from text (D), `Clone` (E) and `Serialize`
    // (G). Neither has a non-public inherent constructor; item 3a's census
    // finds one feature-only constructor of `ReservedExecutionId`, the crash
    // matrix's `inject-id` reservation, absent from the plain surface (F).
    // `CommitSession` is given no other ExecutionId, not even a reserved one
    // (F, beside X3d-1's arity case).
    owned(
        "platform_request_identity_literal.rs",
        "opensip_platform",
        "RequestIdentity",
        "J3a",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "platform_request_identity_default.rs",
        "opensip_platform",
        "RequestIdentity",
        "J3a",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "platform_request_identity_deserialize.rs",
        "opensip_platform",
        "RequestIdentity",
        "J3a",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "platform_request_identity_from_bytes.rs",
        "opensip_platform",
        "RequestIdentity",
        "J3a",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "platform_request_identity_from_text.rs",
        "opensip_platform",
        "RequestIdentity",
        "J3a",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "platform_request_identity_clone.rs",
        "opensip_platform",
        "RequestIdentity",
        "J3a",
        'E',
        Category::ClonedOrReused,
    ),
    owned(
        "platform_request_identity_serialize.rs",
        "opensip_platform",
        "RequestIdentity",
        "J3a",
        'G',
        Category::SerializedPreviousSession,
    ),
    owned(
        "platform_reserved_execution_id_literal.rs",
        "opensip_platform",
        "ReservedExecutionId",
        "J3a",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "platform_reserved_execution_id_default.rs",
        "opensip_platform",
        "ReservedExecutionId",
        "J3a",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "platform_reserved_execution_id_deserialize.rs",
        "opensip_platform",
        "ReservedExecutionId",
        "J3a",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "platform_reserved_execution_id_from_bytes.rs",
        "opensip_platform",
        "ReservedExecutionId",
        "J3a",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "platform_reserved_execution_id_from_text.rs",
        "opensip_platform",
        "ReservedExecutionId",
        "J3a",
        'D',
        Category::ForgedReceipt,
    ),
    owned(
        "platform_reserved_execution_id_clone.rs",
        "opensip_platform",
        "ReservedExecutionId",
        "J3a",
        'E',
        Category::ClonedOrReused,
    ),
    owned(
        "platform_reserved_execution_id_serialize.rs",
        "opensip_platform",
        "ReservedExecutionId",
        "J3a",
        'G',
        Category::SerializedPreviousSession,
    ),
    owned(
        "platform_reserved_execution_id_injected_absent.rs",
        "opensip_platform",
        "ReservedExecutionId",
        "J3a",
        'F',
        Category::PrivateConstructor,
    ),
    owned(
        "security_commit_session_open_reserved.rs",
        "opensip_security",
        "CommitSession",
        "J3a",
        'F',
        Category::PrivateConstructor,
    ),
    // Group I: storage internals.
    case(
        "storage_ledger_store_private.rs",
        "opensip_storage",
        "ledger_store",
        'I',
        Category::StorageInternals,
    ),
    // Group J (unit X8b; law X8 r3 item 4f): security's and storage's
    // `scenario` modules exist only under the test-only `scenario-fixtures`
    // feature, so the plain host surface cannot resolve either (E0432).
    owned(
        "security_scenario_unnameable.rs",
        "opensip_security",
        "scenario",
        "X8b",
        'J',
        Category::TestSeam,
    ),
    owned(
        "storage_scenario_unnameable.rs",
        "opensip_storage",
        "scenario",
        "X8b",
        'J',
        Category::TestSeam,
    ),
    // Group K: replay.
    case(
        "evaluator_replayed_empty_literal.rs",
        "opensip_evaluator",
        "ReplayedRun",
        'K',
        Category::ForgedReceipt,
    ),
    case(
        "evaluator_replayed_deserialize.rs",
        "opensip_evaluator",
        "ReplayedRun",
        'K',
        Category::SerializedPreviousSession,
    ),
    case(
        "evaluator_replayed_raw_json.rs",
        "opensip_evaluator",
        "ReplayedRun",
        'K',
        Category::RawDto,
    ),
    case(
        "evaluator_replayed_bool.rs",
        "opensip_evaluator",
        "ReplayedRun",
        'K',
        Category::BooleanVerified,
    ),
    case(
        "evaluator_replayed_retained_inputs.rs",
        "opensip_evaluator",
        "ReplayedRun",
        'K',
        Category::StructuralOnly,
    ),
    // Group L: the 17 ported compile_fail doctests.
    case(
        "platform_settlement_clone.rs",
        "opensip_platform",
        "SettlementReserve",
        'L',
        Category::ClonedOrReused,
    ),
    case(
        "platform_settlement_settle_twice.rs",
        "opensip_platform",
        "SettlementReserve",
        'L',
        Category::ClonedOrReused,
    ),
    case(
        "platform_settlement_default.rs",
        "opensip_platform",
        "SettlementReserve",
        'L',
        Category::PrivateConstructor,
    ),
    case(
        "platform_settlement_literal.rs",
        "opensip_platform",
        "SettlementReserve",
        'L',
        Category::ForgedReceipt,
    ),
    case(
        "platform_settlement_reserve_in_scope.rs",
        "opensip_platform",
        "SettlementReserve",
        'L',
        Category::PrivateConstructor,
    ),
    case(
        "platform_settlement_settle_in_scope.rs",
        "opensip_platform",
        "SettlementReserve",
        'L',
        Category::ScopeConfinement,
    ),
    case(
        "platform_settlement_reserve_in_postchecks.rs",
        "opensip_platform",
        "SettlementReserve",
        'L',
        Category::PrivateConstructor,
    ),
    case(
        "platform_settlement_settle_in_postchecks.rs",
        "opensip_platform",
        "SettlementReserve",
        'L',
        Category::ScopeConfinement,
    ),
    case(
        "platform_scope_replace.rs",
        "opensip_platform",
        "WorkLedger",
        'L',
        Category::ScopeConfinement,
    ),
    case(
        "platform_scope_swap.rs",
        "opensip_platform",
        "WorkLedger",
        'L',
        Category::ScopeConfinement,
    ),
    case(
        "evaluator_replayed_literal.rs",
        "opensip_evaluator",
        "ReplayedRun",
        'L',
        Category::ForgedReceipt,
    ),
    case(
        "evaluator_admitted_pack_literal.rs",
        "opensip_evaluator",
        "AdmittedPack",
        'L',
        Category::ForgedReceipt,
    ),
    case(
        "evaluator_capability_manifest_literal.rs",
        "opensip_evaluator",
        "CapabilityManifest",
        'L',
        Category::ForgedReceipt,
    ),
    case(
        "security_fence_capture_after_drop.rs",
        "opensip_security",
        "ProvisionalHeldFile",
        'L',
        Category::ScopeConfinement,
    ),
    case(
        "security_fence_capture_escape.rs",
        "opensip_security",
        "ProvisionalHeldFile",
        'L',
        Category::ScopeConfinement,
    ),
    case(
        "security_trust_session_after_drop.rs",
        "opensip_security",
        "NativeTrustReadSession",
        'L',
        Category::ScopeConfinement,
    ),
    case(
        "security_trust_session_escape.rs",
        "opensip_security",
        "NativeTrustReadSession",
        'L',
        Category::ScopeConfinement,
    ),
];

/// Why the driver rejected a case. Each self-test names the one it expects.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum Rejection {
    Annotation,
    BrokenControl,
    ErrorCount,
    WrongReason,
    WrongLine,
}

/// Law X8 r3 item 1e: must-reject shapes. The driver fails if any passes, or
/// is rejected for another reason than the one named here.
const SELFTESTS: &[(&str, Rejection)] = &[
    ("wrong_reason_typo.rs", Rejection::WrongReason),
    ("wrong_extra_error.rs", Rejection::ErrorCount),
    ("wrong_line.rs", Rejection::WrongLine),
    ("wrong_vacuous_reference_clone.rs", Rejection::ErrorCount),
    ("wrong_broken_control.rs", Rejection::BrokenControl),
    ("wrong_fragment.rs", Rejection::WrongReason),
    ("wrong_none_for_coded.rs", Rejection::WrongReason),
    ("wrong_two_annotations.rs", Rejection::Annotation),
];

#[derive(Debug, PartialEq, Eq)]
struct Expect {
    line: u64,
    code: Option<String>,
    fragment: String,
}

/// Parse the one `//~ ERROR <code|none> "<fragment>"` annotation of a case.
fn annotation(source: &str) -> Result<Expect, String> {
    let mut found = None;
    for (index, line) in source.lines().enumerate() {
        let Some(at) = line.find(MARKER) else {
            continue;
        };
        if found.is_some() || line[at + MARKER.len()..].contains(MARKER) {
            return Err("more than one annotation".into());
        }
        let rest = line[at + MARKER.len()..]
            .strip_prefix(" ERROR ")
            .ok_or("annotation is not `//~ ERROR`")?;
        let (code, fragment) = rest.split_once(' ').ok_or("annotation has no fragment")?;
        let fragment = fragment
            .trim_end()
            .strip_prefix('"')
            .and_then(|f| f.strip_suffix('"'))
            .filter(|f| !f.is_empty() && !f.contains('"'))
            .ok_or("fragment is not one non-empty quoted string")?;
        let code = match code {
            "none" => None,
            c if c.len() == 5
                && c.starts_with('E')
                && c[1..].bytes().all(|b| b.is_ascii_digit()) =>
            {
                Some(c.to_owned())
            }
            other => return Err(format!("code `{other}` is neither E#### nor none")),
        };
        found = Some(Expect {
            line: index as u64 + 1,
            code,
            fragment: fragment.to_owned(),
        });
    }
    found.ok_or_else(|| "no annotation".into())
}

/// The pinned compiler and the surface it was used to build.
struct Surface {
    rustc: PathBuf,
    deps: PathBuf,
    externs: BTreeMap<String, PathBuf>,
    scratch: PathBuf,
}

fn rustc_path() -> PathBuf {
    std::env::var_os("RUSTC").map_or_else(|| PathBuf::from("rustc"), PathBuf::from)
}

/// Law X8 r3 item 1d: the pinned release, or the test fails. It never skips.
fn require_pinned(rustc: &Path) {
    let out = Command::new(rustc)
        .arg("-vV")
        .output()
        .unwrap_or_else(|e| panic!("the pinned rustc {}: {e}", rustc.display()));
    assert!(out.status.success(), "rustc -vV failed");
    let text = String::from_utf8(out.stdout).unwrap();
    assert!(
        text.lines().any(|l| l == PINNED_RELEASE),
        "rustc is not the rust-toolchain.toml pin ({PINNED_RELEASE}):\n{text}"
    );
}

fn workspace_manifest() -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("../../Cargo.toml")
        .canonicalize()
        .unwrap()
}

/// Nested cargo inherits nothing that could change the surface it builds.
fn nested_cargo(rustc: &Path) -> Command {
    let cargo = std::env::var_os("CARGO").expect("CARGO is set by cargo test");
    let mut command = Command::new(cargo);
    command.env("RUSTC", rustc);
    for name in [
        "RUSTFLAGS",
        "CARGO_ENCODED_RUSTFLAGS",
        "CARGO_BUILD_RUSTFLAGS",
        "RUSTC_WRAPPER",
        "RUSTC_WORKSPACE_WRAPPER",
        "CARGO_BUILD_RUSTC_WRAPPER",
        "CARGO_TARGET_DIR",
        "CARGO_BUILD_TARGET",
    ] {
        command.env_remove(name);
    }
    command
}

/// Law X8 r3 item 1b: a plain `cargo check -p opensip-host` into its own
/// target directory, and the `.rmeta` of every `opensip_*` library and of
/// `serde_json` from cargo's own artifact messages.
fn surface() -> Surface {
    let rustc = rustc_path();
    require_pinned(&rustc);
    let scratch = PathBuf::from(env!("CARGO_TARGET_TMPDIR")).join("x8-surface");
    let out = nested_cargo(&rustc)
        .args(["check", "--locked", "--offline", "-p", "opensip-host"])
        .arg("--message-format=json")
        .arg("--manifest-path")
        .arg(workspace_manifest())
        .arg("--target-dir")
        .arg(&scratch)
        .output()
        .unwrap();
    assert!(
        out.status.success(),
        "surface check failed:\n{}",
        String::from_utf8_lossy(&out.stderr)
    );
    let mut externs = BTreeMap::new();
    for line in out.stdout.split(|b| *b == b'\n').filter(|l| !l.is_empty()) {
        let message: Value = serde_json::from_slice(line).unwrap();
        if message["reason"] != "compiler-artifact" {
            continue;
        }
        let kinds = message["target"]["kind"].as_array().unwrap();
        if !kinds.iter().any(|k| k == "lib") {
            continue;
        }
        let name = message["target"]["name"]
            .as_str()
            .unwrap()
            .replace('-', "_");
        if !(name.starts_with("opensip_") || name == "serde_json") {
            continue;
        }
        let rmeta: Vec<_> = message["filenames"]
            .as_array()
            .unwrap()
            .iter()
            .map(|f| f.as_str().unwrap())
            .filter(|f| f.ends_with(".rmeta"))
            .collect();
        assert_eq!(rmeta.len(), 1, "{name}: one .rmeta, got {rmeta:?}");
        let previous = externs.insert(name.clone(), PathBuf::from(rmeta[0]));
        assert!(previous.is_none(), "duplicate surface library {name}");
    }
    for required in ["opensip_host", "serde_json"] {
        assert!(externs.contains_key(required), "surface lacks {required}");
    }
    let parents: BTreeSet<_> = externs.values().map(|p| p.parent().unwrap()).collect();
    assert_eq!(parents.len(), 1, "surface libraries in several directories");
    let deps = parents.into_iter().next().unwrap().to_owned();
    Surface {
        rustc,
        deps,
        externs,
        scratch,
    }
}

struct Compiled {
    success: bool,
    errors: Vec<Value>,
}

/// Law X8 r3 item 1c: one compilation of a case by the pinned rustc.
fn compile(surface: &Surface, file: &Path, misuse: bool) -> Result<Compiled, String> {
    let mut command = Command::new(&surface.rustc);
    command
        .args(["--edition", "2024", "--crate-type", "lib"])
        .args(["--crate-name", "x8_case", "--emit=metadata"])
        .args(["--error-format=json", "--cap-lints", "allow"])
        .arg("-o")
        .arg(surface.scratch.join("x8-case.rmeta"))
        .arg("-L")
        .arg(format!("dependency={}", surface.deps.display()));
    for (name, path) in &surface.externs {
        command
            .arg("--extern")
            .arg(format!("{name}={}", path.display()));
    }
    if misuse {
        command.args(["--cfg", "x8_misuse"]);
    }
    let out = command.arg(file).output().map_err(|e| e.to_string())?;
    let mut errors = Vec::new();
    for line in String::from_utf8_lossy(&out.stderr).lines() {
        let diagnostic: Value = serde_json::from_str(line)
            .map_err(|_| format!("rustc emitted a non-JSON line: {line}"))?;
        let level = diagnostic["level"].as_str().unwrap_or_default();
        let message = diagnostic["message"].as_str().unwrap_or_default();
        if level.starts_with("error") && !message.starts_with("aborting due to") {
            errors.push(diagnostic);
        }
    }
    Ok(Compiled {
        success: out.status.success(),
        errors,
    })
}

fn render(errors: &[Value]) -> Vec<String> {
    errors
        .iter()
        .map(|d| format!("{}: {}", d["code"]["code"], d["message"]))
        .collect()
}

/// Law X8 r3 item 1c: the four independent checks, after a compiling control.
fn verdict(surface: &Surface, file: &Path) -> Result<(), (Rejection, String)> {
    let source = std::fs::read_to_string(file).unwrap();
    let expect = annotation(&source).map_err(|e| (Rejection::Annotation, e))?;
    let control = compile(surface, file, false).map_err(|e| (Rejection::BrokenControl, e))?;
    if !control.success || !control.errors.is_empty() {
        let detail = format!("control does not compile: {:?}", render(&control.errors));
        return Err((Rejection::BrokenControl, detail));
    }
    let misuse = compile(surface, file, true).map_err(|e| (Rejection::ErrorCount, e))?;
    let [error] = misuse.errors.as_slice() else {
        let detail = format!("want one error, got {:?}", render(&misuse.errors));
        return Err((Rejection::ErrorCount, detail));
    };
    assert!(!misuse.success, "rustc reported an error and success");
    let code = error["code"]["code"].as_str().map(str::to_owned);
    let message = error["message"].as_str().unwrap_or_default();
    if code != expect.code || !message.contains(&expect.fragment) {
        let detail = format!("got {code:?} {message:?}, want {expect:?}");
        return Err((Rejection::WrongReason, detail));
    }
    let name = file.to_str().unwrap();
    let lines: Vec<u64> = error["spans"]
        .as_array()
        .unwrap()
        .iter()
        .filter(|s| s["is_primary"] == true && s["file_name"] == name)
        .filter_map(|s| s["line_start"].as_u64())
        .collect();
    if !lines.contains(&expect.line) {
        let detail = format!("primary lines {lines:?}, annotated {}", expect.line);
        return Err((Rejection::WrongLine, detail));
    }
    Ok(())
}

fn refusal_dir(child: &str) -> PathBuf {
    Path::new(env!("CARGO_MANIFEST_DIR"))
        .join("tests/refusal")
        .join(child)
}

fn listing(child: &str) -> BTreeSet<String> {
    std::fs::read_dir(refusal_dir(child))
        .unwrap()
        .map(|e| e.unwrap().file_name().into_string().unwrap())
        .collect()
}

/// Law X8 r3 item 1f: the census, checked before anything is compiled.
fn census() {
    let mut files = BTreeSet::new();
    for row in CASES {
        assert!(files.insert(row.file), "duplicate census row {}", row.file);
        assert!(row.file.ends_with(".rs") && row.file != "main.rs");
        assert!(row.krate.starts_with("opensip_") && !row.ty.is_empty());
        assert!(!row.unit.is_empty() && row.group.is_ascii_uppercase());
        let source = std::fs::read_to_string(refusal_dir("cases").join(row.file)).unwrap();
        assert!(
            source.contains(row.krate) && source.contains(row.ty),
            "{} names neither its crate nor its type",
            row.file
        );
    }
    let listed = listing("cases");
    let table: BTreeSet<String> = files.iter().map(|f| f.to_string()).collect();
    assert_eq!(listed, table, "tests/refusal/cases differs from the census");
    let present: BTreeSet<Category> = CASES.iter().map(|c| c.category).collect();
    for category in REQUIRED_CATEGORIES {
        assert!(present.contains(&category), "no case for {category:?}");
    }
    let selftests: BTreeSet<String> = SELFTESTS.iter().map(|(f, _)| f.to_string()).collect();
    assert_eq!(selftests.len(), SELFTESTS.len(), "duplicate self-test row");
    assert_eq!(
        listing("selftest"),
        selftests,
        "tests/refusal/selftest differs"
    );
}

/// Law X8 r3 item 1: every case fails for its intended reason, and every
/// must-reject self-test is rejected for the reason it names. One test, so no
/// two nested builds share the surface target directory.
#[test]
fn opaque_api_misuse_fails_for_the_intended_reason() {
    census();
    let started = Instant::now();
    let surface = surface();
    eprintln!(
        "x8 surface check {:?}; externs {:?}",
        started.elapsed(),
        surface.externs.keys().collect::<Vec<_>>()
    );
    let started = Instant::now();
    let mut failures = Vec::new();
    for row in CASES {
        if let Err((rejection, detail)) = verdict(&surface, &refusal_dir("cases").join(row.file)) {
            failures.push(format!("{}: {rejection:?}: {detail}", row.file));
        }
    }
    for (file, expected) in SELFTESTS {
        match verdict(&surface, &refusal_dir("selftest").join(file)) {
            Ok(()) => failures.push(format!("self-test {file} passed")),
            Err((rejection, _)) if rejection == *expected => {}
            Err((rejection, detail)) => failures.push(format!(
                "self-test {file}: rejected as {rejection:?}, not {expected:?}: {detail}"
            )),
        }
    }
    eprintln!(
        "x8 {} cases and {} self-tests {:?}",
        CASES.len(),
        SELFTESTS.len(),
        started.elapsed()
    );
    assert!(failures.is_empty(), "{failures:#?}");
}

#[test]
fn annotations_are_parsed_exactly() {
    let ok = "a\nb(); //~ ERROR E0308 \"mismatched types\"\n";
    assert_eq!(
        annotation(ok),
        Ok(Expect {
            line: 2,
            code: Some("E0308".into()),
            fragment: "mismatched types".into(),
        })
    );
    let none = "x //~ ERROR none \"private fields\"";
    assert_eq!(annotation(none).unwrap().code, None);
    for bad in [
        "",
        "x //~ ERROR E0308",
        "x //~ ERROR E0308 \"\"",
        "x //~ ERROR E0308 mismatched",
        "x //~ ERROR E308 \"m\"",
        "x //~ ERROR e0308 \"m\"",
        "x //~ WARN E0308 \"m\"",
        "x //~ERROR E0308 \"m\"",
        "x //~ ERROR E0308 \"m\" //~ ERROR E0308 \"m\"",
        "x //~ ERROR E0308 \"m\"\ny //~ ERROR E0308 \"m\"",
        "x //~ ERROR E0308 \"m\" trailing",
    ] {
        assert!(annotation(bad).is_err(), "accepted {bad:?}");
    }
}

/// Law X8 r3 item 4f: where `scenario-fixtures` may appear in a manifest.
#[derive(Clone, Copy, Debug, PartialEq, Eq)]
enum Table {
    Features,
    DevDependencies,
    Other,
}

/// Split a dotted TOML key or table name, keeping quoted segments whole.
fn segments(name: &str) -> Vec<String> {
    let mut out = vec![String::new()];
    let mut quote = None;
    for ch in name.chars() {
        match (quote, ch) {
            (None, '"' | '\'') => quote = Some(ch),
            (Some(q), c) if c == q => quote = None,
            (None, '.') => out.push(String::new()),
            (None, c) if c.is_whitespace() => {}
            (_, c) => out.last_mut().unwrap().push(c),
        }
    }
    out
}

fn table(header: &str) -> Table {
    let parts = segments(header);
    let kind = match parts.as_slice() {
        [target, _, kind, ..] if target == "target" => kind.as_str(),
        [kind, ..] => kind.as_str(),
        [] => "",
    };
    match (parts.len(), kind) {
        (1, "features") => Table::Features,
        (_, "dev-dependencies" | "dev_dependencies") => Table::DevDependencies,
        _ => Table::Other,
    }
}

/// The text of a line before any comment. `depth` carries the bracket depth
/// of open arrays and inline tables from one line to the next.
fn scan(line: &str, depth: &mut usize) -> String {
    let mut out = String::new();
    let mut quote = None;
    for ch in line.chars() {
        match (quote, ch) {
            (None, '#') => break,
            (None, '"' | '\'') => quote = Some(ch),
            (Some(q), c) if c == q => quote = None,
            (None, '[' | '{') => *depth += 1,
            (None, ']' | '}') => *depth = depth.saturating_sub(1),
            _ => {}
        }
        out.push(ch);
    }
    out
}

/// Law X8 r3 item 4f's source pin for one manifest: `scenario-fixtures` only
/// in `[features]` of security and storage (never `default`) and in
/// `[dev-dependencies]`; never in `[dependencies]` or any other table.
fn feature_pin(manifest: &str, features_allowed: bool) -> Result<(), String> {
    const FEATURE: &str = "scenario-fixtures";
    let mut current = Table::Other;
    let mut depth = 0;
    let mut key = String::new();
    for (index, raw) in manifest.lines().enumerate() {
        let start = depth;
        let line = scan(raw, &mut depth);
        let trimmed = line.trim();
        if start == 0 && trimmed.starts_with('[') {
            let header = trimmed.trim_start_matches('[').trim_end_matches(']');
            current = table(header);
            key.clear();
            depth = 0;
            if header.contains(FEATURE) {
                return Err(format!("line {}: feature in a table name", index + 1));
            }
            continue;
        }
        if start == 0
            && let Some((name, _)) = trimmed.split_once('=')
        {
            key = segments(name).join(".");
        }
        if !line.contains(FEATURE) {
            continue;
        }
        let at = index + 1;
        match current {
            Table::DevDependencies => {}
            Table::Features if !features_allowed => {
                return Err(format!(
                    "line {at}: [features] outside security and storage"
                ));
            }
            Table::Features if key == "default" => {
                return Err(format!("line {at}: a default feature"));
            }
            Table::Features => {}
            Table::Other => {
                return Err(format!(
                    "line {at}: outside [features] and dev-dependencies"
                ));
            }
        }
    }
    Ok(())
}

/// Law X8 r3 item 4f: every `Cargo.toml` of the workspace keeps
/// `scenario-fixtures` out of release builds. Since unit X8b it is declared
/// by security and storage and enabled from storage's and host's
/// `[dev-dependencies]`.
#[test]
fn scenario_fixtures_stays_out_of_release_manifests() {
    let out = nested_cargo(&rustc_path())
        .args(["metadata", "--locked", "--offline", "--no-deps"])
        .args(["--format-version", "1", "--manifest-path"])
        .arg(workspace_manifest())
        .output()
        .unwrap();
    assert!(
        out.status.success(),
        "{}",
        String::from_utf8_lossy(&out.stderr)
    );
    let metadata: Value = serde_json::from_slice(&out.stdout).unwrap();
    let members: BTreeSet<&str> = metadata["workspace_members"]
        .as_array()
        .unwrap()
        .iter()
        .map(|m| m.as_str().unwrap())
        .collect();
    let mut manifests = vec![(workspace_manifest(), false)];
    for package in metadata["packages"].as_array().unwrap() {
        if !members.contains(package["id"].as_str().unwrap()) {
            continue;
        }
        let name = package["name"].as_str().unwrap();
        let path = PathBuf::from(package["manifest_path"].as_str().unwrap());
        manifests.push((path, matches!(name, "opensip-security" | "opensip-storage")));
    }
    assert_eq!(
        manifests.len(),
        members.len() + 1,
        "a member without a manifest"
    );
    for name in ["opensip-host", "opensip-security", "opensip-storage"] {
        let found = metadata["packages"]
            .as_array()
            .unwrap()
            .iter()
            .any(|p| p["name"] == name);
        assert!(found, "workspace lacks {name}");
    }
    for (path, features_allowed) in manifests {
        let text = std::fs::read_to_string(&path).unwrap();
        if let Err(e) = feature_pin(&text, features_allowed) {
            panic!("{}: {e}", path.display());
        }
    }
}

#[test]
fn the_feature_pin_refuses_every_release_route() {
    let allowed = [
        "[features]\nscenario-fixtures = []\n",
        "[features]\nscenario-fixtures = [\"opensip-security/scenario-fixtures\"]\n",
        "[features]\nscenario-fixtures = [\n  \"opensip-security/scenario-fixtures\",\n]\n",
        "[dev-dependencies]\nopensip-storage = { path = \"../storage\", features = [\"scenario-fixtures\"] }\n",
        "[dev-dependencies.opensip-storage]\npath = \"../storage\"\nfeatures = [\"scenario-fixtures\"]\n",
        "[target.'cfg(unix)'.dev-dependencies]\nopensip-storage = { path = \"x\", features = [\"scenario-fixtures\"] }\n",
        "[dependencies]\n# scenario-fixtures is never named here\nserde_json = \"=1.0.151\"\n",
    ];
    for manifest in allowed {
        assert_eq!(feature_pin(manifest, true), Ok(()), "{manifest}");
    }
    let refused_everywhere = [
        "[dependencies]\nopensip-storage = { path = \"x\", features = [\"scenario-fixtures\"] }\n",
        "[dependencies.opensip-storage]\npath = \"x\"\nfeatures = [\"scenario-fixtures\"]\n",
        "[target.'cfg(unix)'.dependencies]\nopensip-storage = { path = \"x\", features = [\"scenario-fixtures\"] }\n",
        "[build-dependencies]\nopensip-storage = { path = \"x\", features = [\"scenario-fixtures\"] }\n",
        "[workspace.dependencies]\nopensip-storage = { path = \"x\", features = [\"scenario-fixtures\"] }\n",
        "[features]\ndefault = [\"scenario-fixtures\"]\nscenario-fixtures = []\n",
        "[features]\ndefault = [\n  \"std\",\n  \"scenario-fixtures\",\n]\nscenario-fixtures = []\n",
        "[package]\nname = \"scenario-fixtures\"\n",
        "[dependencies]\nopensip-storage = { path = \"x\", features = [\n  \"scenario-fixtures\",\n] }\n",
    ];
    for manifest in refused_everywhere {
        assert!(feature_pin(manifest, true).is_err(), "{manifest}");
        assert!(feature_pin(manifest, false).is_err(), "{manifest}");
    }
    assert!(feature_pin("[features]\nscenario-fixtures = []\n", false).is_err());
    // X9's `crash-matrix` (platform's `[features]`, law X9 r1 item 2) is not
    // this pin's feature: its own manifest pin governs it.
    let platform = "[features]\ncrash-matrix = []\n\n[[test]]\nname = \"m\"\nrequired-features = [\"crash-matrix\"]\n";
    assert_eq!(feature_pin(platform, false), Ok(()));
}

// ------------------------------------------------- law X8 r3 item 3b's pin

/// The names law X8 r3 item 3b confines: security's two-phase adapter traits
/// and the two session functions storage's facade composes.
const CONFINED: [&str; 4] = [
    "CommitAdapter",
    "StagedCommit",
    "begin_journal_txn",
    "seal_under_append_lock",
];
/// Where they may appear in production code: security's defining module and
/// its root re-export, and storage's `commit.rs`.
const CONFINED_TO: [&str; 3] = [
    "crates/security/src/custody/commit_session.rs",
    "crates/security/src/lib.rs",
    "crates/storage/src/commit.rs",
];

/// The confined names `source` uses as identifiers outside comments.
fn confined_uses(source: &str) -> BTreeSet<&'static str> {
    let mut used = BTreeSet::new();
    for line in source.lines() {
        let code = line.split_once("//").map_or(line, |(code, _)| code);
        for word in code.split(|c: char| !(c.is_ascii_alphanumeric() || c == '_')) {
            if let Some(name) = CONFINED.iter().find(|name| **name == word) {
                used.insert(*name);
            }
        }
    }
    used
}
/// Every production `.rs` file under `crates/*/src` (test files, named
/// `*_tests.rs` or `tests.rs`, are not production code), relative to the
/// workspace root.
fn production_sources(root: &Path) -> Vec<(String, String)> {
    fn walk(dir: &Path, root: &Path, out: &mut Vec<(String, String)>) {
        for entry in std::fs::read_dir(dir).unwrap() {
            let path = entry.unwrap().path();
            if path.is_dir() {
                walk(&path, root, out);
                continue;
            }
            let name = path.file_name().unwrap().to_str().unwrap();
            if !name.ends_with(".rs") || name.ends_with("_tests.rs") || name == "tests.rs" {
                continue;
            }
            let relative = path
                .strip_prefix(root)
                .unwrap()
                .to_str()
                .unwrap()
                .to_owned();
            out.push((relative, std::fs::read_to_string(&path).unwrap()));
        }
    }
    let mut out = Vec::new();
    for krate in std::fs::read_dir(root.join("crates")).unwrap() {
        let src = krate.unwrap().path().join("src");
        if src.is_dir() {
            walk(&src, root, &mut out);
        }
    }
    out.sort();
    out
}
fn confinement(sources: &[(String, String)]) -> Result<(), String> {
    for (path, source) in sources {
        let used = confined_uses(source);
        if !used.is_empty() && !CONFINED_TO.contains(&path.as_str()) {
            return Err(format!("{path} uses {used:?}"));
        }
    }
    Ok(())
}

/// Law X8 r3 item 3b (unit X3d-2): Rust visibility cannot confine a public
/// trait's implementations or a public function's callers to one sibling
/// crate, so a source pin does. In production code under `crates/*/src`,
/// security's adapter traits, `begin_journal_txn` and
/// `seal_under_append_lock` appear only in security's defining module (with
/// its root re-export) and in storage's `commit.rs`, which uses all four.
#[test]
fn the_commit_adapter_and_session_functions_are_confined_to_storage_commit() {
    let root = workspace_manifest().parent().unwrap().to_owned();
    let sources = production_sources(&root);
    assert!(
        sources.len() > 100,
        "the walk found {} files",
        sources.len()
    );
    assert_eq!(confinement(&sources), Ok(()));
    let commit = sources
        .iter()
        .find(|(path, _)| path == "crates/storage/src/commit.rs")
        .expect("storage's commit facade");
    assert_eq!(confined_uses(&commit.1), CONFINED.into_iter().collect());
}

#[test]
fn the_adapter_pin_refuses_a_use_outside_its_files() {
    let planted = |path: &str, source: &str| vec![(path.to_owned(), source.to_owned())];
    for name in CONFINED {
        let source = format!("use opensip_security::{name};\n");
        assert!(confinement(&planted("crates/host/src/lib.rs", &source)).is_err());
        assert!(confinement(&planted("crates/storage/src/ledger_store.rs", &source)).is_err());
        assert_eq!(
            confinement(&planted("crates/storage/src/commit.rs", &source)),
            Ok(())
        );
    }
    // A comment or a longer identifier is not a use.
    let source = "// seal_under_append_lock binds the replay\nfn begin_journal_txn_cost() {}\n";
    assert_eq!(
        confinement(&planted("crates/host/src/lib.rs", source)),
        Ok(())
    );
}

// ------------------------------------- law X8 r4 item 5: B0 to B8 (unit X8c)
//
// The behavioural refusal cases, each an ordinary `#[test]` named
// `synthetic_…` (build plan line 886's label) on its own `ScenarioHome`,
// driving the public facade: `scenario::operation`, `CommitSession::open`,
// `replay_run`, `prepare_commit`, `publish` and `finish`. B0 is the lawful
// control that makes B1 to B8 non-vacuous. Each refusal asserts its outcome
// variant, its exact `InstallationTermination` row and that row's public
// projection, that no `PublishedCommit` exists (the outcome type shows it),
// and the durable census after `finish`: N's carrier records and (S, N)'s
// evidence ledger.
//
// Synchronization (item 5): every alteration happens on the test thread
// between two public calls, after the handoff (`operation`) and `open`, and
// before `prepare_commit`; no case sleeps or reads a clock. B6 and B7's trust
// publication runs in a helper process that holds no operation lease (item
// 5a). Replay is pure and takes no custody; B0 to B7 replay after `open`,
// because a first registration draws the ProjectId inside the operation
// (X9 r5's order); B8 replays before any fence (X5 r3 item 3, F01).
// Synthetic fixtures; no compiler qualification is claimed.

/// The run candidate's registry. The candidate's source (below) names
/// storage's `crate::schema_sources::registry()`, which host's tests cannot
/// reach; host's `embedded_schema_registry` compiles the same 48 pinned
/// sources from the same files (pinned by
/// `the_candidate_registry_is_storages_selected_registry`).
#[cfg(target_os = "macos")]
mod schema_sources {
    use opensip_identity::RegisteredSchemas;
    use std::sync::OnceLock;
    pub(crate) fn registry() -> Option<&'static RegisteredSchemas> {
        static REGISTRY: OnceLock<Option<RegisteredSchemas>> = OnceLock::new();
        REGISTRY
            .get_or_init(|| opensip_host::embedded_schema_registry().ok())
            .as_ref()
    }
}

// Law X3d r8 item 13 (unit X3d-3): the synthetic run candidate, inputs only,
// never a `ReplayedRun`. Storage compiles it only under `crash-matrix`, which
// no manifest enables (X9 r1 item 2), so it is included here by path, as
// storage's own unit tests include it. This copy is a test-crate module, not
// a `crash_matrix_support` item. The core evaluator closure's preimages it
// reads come from `CommitSession::core_evaluator_closure_preimages`, on X8 r3
// item 4b's shared site list, which `scenario-fixtures` reaches.
#[cfg(target_os = "macos")]
#[allow(dead_code)]
#[path = "../../storage/src/crash_matrix_support/run_candidate.rs"]
mod run_candidate;

#[cfg(target_os = "macos")]
mod x8c {
    use opensip_evaluator::{ReplayError, ReplayedRun, replay_run};
    use opensip_identity::{
        IdentityDomain, JsonValue as V, ObjectInput, RetainedInputs, digest_hex,
        hash_canonical_value, parse_json,
    };
    use opensip_security::scenario::{
        CarrierCensus, RevocationVersions, ScenarioHome, revocation_version,
    };
    use opensip_security::{CommitSession, InstallationTermination as T, SessionEnd};
    use opensip_storage::scenario::{LedgerCensus, ledger_census};
    use std::collections::BTreeMap;
    use std::fs;
    use std::os::unix::fs::{DirBuilderExt, MetadataExt, PermissionsExt};
    use std::path::{Path, PathBuf};
    use std::process::Command;
    use std::sync::OnceLock;

    /// Every case's scratch directory, made before any case runs.
    const CASES: [&str; 10] = [
        "b0",
        "b1",
        "b2",
        "b3-marker",
        "b3-lease",
        "b4",
        "b5",
        "b6",
        "b7",
        "b8",
    ];

    fn private_dir(path: &Path) {
        match fs::DirBuilder::new().mode(0o700).create(path) {
            Ok(()) => {}
            Err(e) if e.kind() == std::io::ErrorKind::AlreadyExists => {}
            Err(e) => panic!("{}: {e}", path.display()),
        }
    }
    /// This process's scratch root, `<temp>/opensip-test/x8c-<pid>-<draw>`,
    /// below F3's long-lived shared parent, with every case's directories
    /// made once, before any case's walk: no case adds an entry above another
    /// case's home. (Security's fixture lock then runs the cases one at a
    /// time, from each case's `ScenarioHome::create` to its thread's end.)
    fn process_root() -> &'static Path {
        static ROOT: OnceLock<PathBuf> = OnceLock::new();
        ROOT.get_or_init(|| {
            let shared = std::env::temp_dir().join("opensip-test");
            private_dir(&shared);
            let draw: String = opensip_platform::request_entropy()
                .expect("entropy")
                .iter()
                .map(|b| format!("{b:02x}"))
                .collect();
            let root = shared.join(format!("x8c-{}-{draw}", std::process::id()));
            fs::DirBuilder::new().mode(0o700).create(&root).unwrap();
            for name in CASES {
                let case = root.join(name);
                fs::DirBuilder::new().mode(0o700).create(&case).unwrap();
                for child in ["homes", "helper"] {
                    fs::DirBuilder::new()
                        .mode(0o700)
                        .create(case.join(child))
                        .unwrap();
                }
            }
            fs::canonicalize(&root).unwrap()
        })
    }

    /// One case's scratch: `homes`, the scenario home's parent, and beside it
    /// (never above the home) `helper`, item 5a's helper process's scratch
    /// parent, which holds its input file and is its `TMPDIR`.
    pub(crate) struct Case {
        pub(crate) homes: PathBuf,
        pub(crate) helper: PathBuf,
    }
    pub(crate) fn case(name: &str) -> Case {
        assert!(CASES.contains(&name), "unknown case {name}");
        let case = process_root().join(name);
        Case {
            homes: case.join("homes"),
            helper: case.join("helper"),
        }
    }

    /// The values a case keeps from its session before handing it on.
    #[derive(Debug, Clone)]
    pub(crate) struct Bound {
        pub(crate) execution: String,
        pub(crate) namespace: String,
        pub(crate) store: String,
        pub(crate) project: String,
        pub(crate) core_closure: String,
        pub(crate) evaluator_closure: String,
    }
    impl Bound {
        pub(crate) fn of(session: &CommitSession) -> Self {
            Self {
                execution: session.execution_id().to_owned(),
                namespace: session.namespace_id().to_owned(),
                store: session.store_instance().to_owned(),
                project: session.project_id().to_owned(),
                core_closure: session.core_closure().to_owned(),
                evaluator_closure: session.core_evaluator_closure().to_owned(),
            }
        }
    }

    /// A scenario home, its root `H/code/<name>`, and the session opened on
    /// the production chain's `ProjectOperation`, with its values.
    pub(crate) fn open(case: &Case, name: &str) -> (ScenarioHome, PathBuf, CommitSession, Bound) {
        let home = ScenarioHome::create(&case.homes);
        let root = home.project(name);
        let operation = home
            .operation(&root)
            .unwrap_or_else(|row| panic!("the scenario chain refused: {row:?}"));
        let session = CommitSession::open(operation).expect("the session opens");
        let bound = Bound::of(&session);
        // A fresh namespace: no carrier record but the start's, no ledger.
        let carrier = home.carrier_census(&bound.namespace).unwrap();
        assert_eq!((carrier.seal, carrier.rev, carrier.cln), (0, 0, 0));
        assert_eq!(
            ledger_census(&home, &bound.store, &bound.namespace).unwrap(),
            LedgerCensus::default()
        );
        (home, root, session, bound)
    }

    /// The durable census after `finish`: N's carrier records by kind and
    /// (S, N)'s evidence ledger.
    pub(crate) fn census(home: &ScenarioHome, bound: &Bound) -> (CarrierCensus, LedgerCensus) {
        (
            home.carrier_census(&bound.namespace).unwrap(),
            ledger_census(home, &bound.store, &bound.namespace).unwrap(),
        )
    }
    /// N's SEAL, REV and CLN counts.
    pub(crate) fn records(carrier: &CarrierCensus) -> (u64, u64, u64) {
        (carrier.seal, carrier.rev, carrier.cln)
    }

    /// The end path that every certain refusal before admission owes (X3d
    /// r6 item 7): the gate latched, so one `REV` and no `CLN` (no `SEAL` is
    /// durable), settled without failure; the refusal closed the attempt
    /// ledger, so X3b's end step is not entered (not a failure).
    pub(crate) fn refused_end(end: &SessionEnd) {
        assert!(end.revocation_appended(), "{end:?}");
        assert!(!end.cleanup_appended(), "{end:?}");
        assert_eq!(end.settlement_failure(), None);
        assert!(!end.end_step_entered(), "{end:?}");
        assert_eq!(end.end_step_failure(), None);
        assert_eq!(end.rollover(), None);
    }

    /// The row's public projection (468c's map): code, detail and subject.
    pub(crate) fn public(row: &T) -> (String, Option<String>, Option<String>) {
        let v1 = opensip_host::installation_termination(row);
        (
            v1.error_code.to_string(),
            v1.detail.map(|d| d.to_string()),
            v1.subject,
        )
    }

    /// The evaluator's full replay of the synthetic candidate built for
    /// `session` (law X3d r8 item 13): `replay_run`, the only `ReplayedRun`
    /// mint, over the candidate's inputs.
    pub(crate) fn candidate_replay(session: &CommitSession) -> (ReplayedRun, String) {
        let candidate = super::run_candidate::synthetic_run_candidate(session);
        assert_eq!(candidate.label(), "synthetic");
        let run = replay_run(
            &candidate.retained_inputs(),
            candidate.run_id(),
            super::run_candidate::synthetic_replay_limits(),
        )
        .expect("the synthetic candidate replays");
        (run, candidate.run_id().to_owned())
    }

    // ------------------------------------------------------------ corpus

    fn object(v: &V) -> &BTreeMap<String, V> {
        match v {
            V::Object(o) => o,
            _ => panic!("corpus: object"),
        }
    }
    fn string(v: &V) -> &str {
        match v {
            V::String(s) => s,
            _ => panic!("corpus: string"),
        }
    }
    fn array(v: &V) -> &[V] {
        match v {
            V::Array(a) => a,
            _ => panic!("corpus: array"),
        }
    }
    fn hex(s: &str) -> Vec<u8> {
        s.as_bytes()
            .chunks_exact(2)
            .map(|p| u8::from_str_radix(std::str::from_utf8(p).unwrap(), 16).unwrap())
            .collect()
    }
    /// `prefix:hex(H(domain, descriptor))`, the object identity recipe.
    fn identity(domain: IdentityDomain, descriptor: &V) -> String {
        let h = hash_canonical_value(domain.name(), descriptor).unwrap();
        format!("{}:{}", domain.prefix(), digest_hex(&h))
    }

    /// One pinned corpus Run of host's selected replay reference
    /// (`tests/fixtures/replay-fixtures.json`, the corpus
    /// `independent_run_replay_matches_selected_reference_and_owns_its_closure`
    /// pins): its retained objects and blobs and its RunId.
    pub(crate) struct Corpus {
        pub(crate) objects: BTreeMap<String, ObjectInput>,
        pub(crate) blobs: BTreeMap<[u8; 32], Vec<u8>>,
        pub(crate) run_id: String,
    }
    impl Corpus {
        pub(crate) fn case(label: &str) -> Self {
            let raw = fs::read(
                Path::new(env!("CARGO_MANIFEST_DIR")).join("tests/fixtures/replay-fixtures.json"),
            )
            .unwrap();
            let f = parse_json(&raw).unwrap();
            let f = object(&f);
            let c = array(&f["cases"])
                .iter()
                .map(object)
                .find(|c| string(&c["label"]) == label)
                .unwrap_or_else(|| panic!("corpus case {label}"));
            let objects = array(&c["objects"])
                .iter()
                .map(|k| {
                    let r = object(&object(&f["objectPool"])[string(k)]);
                    (
                        string(&r["id"]).to_owned(),
                        ObjectInput {
                            domain: IdentityDomain::parse(string(&r["domain"])).unwrap(),
                            descriptor: r["descriptor"].clone(),
                        },
                    )
                })
                .collect();
            let blobs = array(&c["blobs"])
                .iter()
                .map(|k| {
                    let r = object(&object(&f["blobPool"])[string(k)]);
                    (
                        hex(string(&r["digest"])).try_into().unwrap(),
                        hex(string(&r["hex"])),
                    )
                })
                .collect();
            Self {
                objects,
                blobs,
                run_id: string(&c["runId"]).to_owned(),
            }
        }
        pub(crate) fn replay(&self) -> Result<ReplayedRun, ReplayError> {
            let registry = super::schema_sources::registry().unwrap();
            replay_run(
                &RetainedInputs::new(registry, &self.objects, &self.blobs),
                &self.run_id,
                super::run_candidate::synthetic_replay_limits(),
            )
        }
        /// B8's alteration: one byte of a claimed output, the last byte of a
        /// finding's message code. The derived finding carries it twice, as
        /// its `messageCode` and inside its parameter blob, so the same byte
        /// changes in both: the blob is retained under its new raw digest,
        /// the finding names it, and every retained object that names the
        /// finding is recomputed to a fixpoint (the proof bundle, the
        /// evidence, the seal and the Run), so the claim is a well-formed
        /// retained closure. The original objects and blob stay retained, as
        /// unread ambient inputs would. Returns the altered and the original
        /// byte.
        pub(crate) fn alter_one_claimed_byte(&mut self) -> (u8, u8) {
            let (finding, mut descriptor) = self
                .objects
                .iter()
                .find(|(_, o)| o.domain == IdentityDomain::Finding)
                .map(|(id, o)| (id.clone(), object(&o.descriptor).clone()))
                .expect("a corpus Run with a finding");
            let message = string(&descriptor["messageCode"]).to_owned();
            let original = *message.as_bytes().last().unwrap();
            let altered = if original == b'a' { b'b' } else { b'a' };
            let mut bytes = message.clone().into_bytes();
            *bytes.last_mut().unwrap() = altered;
            let changed = String::from_utf8(bytes).unwrap();
            let parameters: [u8; 32] = hex(string(&descriptor["parameterDigest"]))
                .try_into()
                .unwrap();
            let blob = String::from_utf8(self.blobs[&parameters].clone()).unwrap();
            let field = |m: &str| format!("\"messageCode\":\"{m}\"");
            assert_eq!(blob.matches(&field(&message)).count(), 1);
            let blob = blob
                .replace(&field(&message), &field(&changed))
                .into_bytes();
            assert_eq!(
                blob.iter()
                    .zip(&self.blobs[&parameters])
                    .filter(|(a, b)| a != b)
                    .count(),
                1
            );
            let digest = opensip_identity::raw_sha256(&blob);
            self.blobs.insert(digest, blob);
            descriptor.insert("messageCode".into(), V::String(changed));
            descriptor.insert("parameterDigest".into(), V::String(digest_hex(&digest)));
            let descriptor = V::Object(descriptor);
            let renamed = identity(IdentityDomain::Finding, &descriptor);
            self.objects.insert(
                renamed.clone(),
                ObjectInput {
                    domain: IdentityDomain::Finding,
                    descriptor,
                },
            );
            let mut map = vec![(hex_of(&finding).to_owned(), hex_of(&renamed).to_owned())];
            loop {
                let mut added = Vec::new();
                let current: Vec<(String, IdentityDomain, V)> = self
                    .objects
                    .iter()
                    .map(|(id, o)| (id.clone(), o.domain, o.descriptor.clone()))
                    .collect();
                for (id, domain, descriptor) in current {
                    let rewritten = substitute(&descriptor, &map);
                    if rewritten == descriptor {
                        continue;
                    }
                    let new = identity(domain, &rewritten);
                    let pair = (hex_of(&id).to_owned(), hex_of(&new).to_owned());
                    self.objects.entry(new).or_insert(ObjectInput {
                        domain,
                        descriptor: rewritten,
                    });
                    if !map.contains(&pair) && !added.contains(&pair) {
                        added.push(pair);
                    }
                }
                if added.is_empty() {
                    break;
                }
                map.extend(added);
            }
            self.run_id = substitute_text(&self.run_id, &map);
            assert!(self.objects.contains_key(&self.run_id));
            (altered, original)
        }
    }
    fn hex_of(id: &str) -> &str {
        id.rsplit(':').next().unwrap()
    }
    fn substitute_text(text: &str, map: &[(String, String)]) -> String {
        map.iter().fold(text.to_owned(), |text, (old, new)| {
            text.replace(old.as_str(), new)
        })
    }
    /// One reference rewrite of a value. An array of texts that was in
    /// ascending order (an id set) is kept in ascending order.
    fn substitute(v: &V, map: &[(String, String)]) -> V {
        match v {
            V::String(s) => V::String(substitute_text(s, map)),
            V::Array(a) => {
                let mut out: Vec<V> = a.iter().map(|c| substitute(c, map)).collect();
                let texts = |a: &[V]| -> Option<Vec<String>> {
                    a.iter()
                        .map(|c| match c {
                            V::String(s) => Some(s.clone()),
                            _ => None,
                        })
                        .collect()
                };
                if let Some(before) = texts(a)
                    && before.is_sorted()
                {
                    let mut after = texts(&out).unwrap();
                    after.sort();
                    out = after.into_iter().map(V::String).collect();
                }
                V::Array(out)
            }
            V::Object(o) => V::Object(
                o.iter()
                    .map(|(k, c)| (k.clone(), substitute(c, map)))
                    .collect(),
            ),
            other => other.clone(),
        }
    }

    // ------------------------------------------------- item 5a's helper

    /// The helper entry's variable, its one lawful value, and its input.
    pub(crate) const HELPER: &str = "OPENSIP_X8_HELPER";
    const HELPER_MODE: &str = "publish-revocation";
    const HELPER_INPUT: &str = "OPENSIP_X8_INPUT";
    /// The tagged record the helper writes once on success.
    const PUBLISHED: &str = "X8|published|";

    /// Item 5a, the helper process's body: with the variable set, read the
    /// input file, publish through `scenario::publish_revocation_fenced`
    /// (the shared fenced publisher, under I's fence by its production
    /// walk), write one tagged record and return. Any error panics.
    pub(crate) fn helper_publish(mode: std::ffi::OsString) {
        assert_eq!(mode, HELPER_MODE, "unknown helper mode");
        let input = std::env::var_os(HELPER_INPUT).expect("the helper's input file");
        let input = parse_json(&fs::read(input).unwrap()).unwrap();
        let input = object(&input);
        let home = ScenarioHome::open(
            Path::new(string(&input["home"])),
            Path::new(string(&input["installation"])),
            string(&input["store"]),
        );
        let subjects: Vec<(&str, &str)> = array(&input["subjects"])
            .iter()
            .map(|pair| (string(&array(pair)[0]), string(&array(pair)[1])))
            .collect();
        let versions = opensip_security::scenario::publish_revocation_fenced(&home, &subjects)
            .unwrap_or_else(|row| panic!("the fenced publication refused: {row:?}"));
        eprintln!("{PUBLISHED}{}|{}", versions.before, versions.after);
    }

    /// Item 5a, the test thread's side: read the revocation version, run
    /// the helper process (this binary, the entry alone, the environment
    /// cleared but for the helper's variable, its input and `TMPDIR`), wait
    /// for it to exit, then require its success, its one `published` record
    /// from one test run, an advanced version, and that version in
    /// `state.v1`. Only then does the case go on. No sleep.
    pub(crate) fn publish_through_helper(
        case: &Case,
        home: &ScenarioHome,
        subjects: &[(&str, &str)],
    ) -> RevocationVersions {
        let before = revocation_version(home);
        let pairs = subjects
            .iter()
            .map(|(kind, subject)| {
                V::Array(vec![
                    V::String((*kind).into()),
                    V::String((*subject).into()),
                ])
            })
            .collect();
        let text = |p: &Path| V::String(p.to_str().unwrap().to_owned());
        let input = V::Object(BTreeMap::from([
            ("home".to_owned(), text(home.home())),
            ("installation".to_owned(), text(home.installation())),
            ("store".to_owned(), V::String(home.store().to_owned())),
            ("subjects".to_owned(), V::Array(pairs)),
        ]));
        let path = case.helper.join("input.json");
        fs::write(&path, opensip_identity::canonical_bytes(&input).unwrap()).unwrap();
        let out = Command::new(std::env::current_exe().unwrap())
            .args([
                "--exact",
                "x8_helper_publish_revocation",
                "--nocapture",
                "--test-threads=1",
            ])
            .env_clear()
            .env(HELPER, HELPER_MODE)
            .env(HELPER_INPUT, &path)
            .env("TMPDIR", &case.helper)
            .output()
            .unwrap();
        let stdout = String::from_utf8_lossy(&out.stdout);
        let stderr = String::from_utf8_lossy(&out.stderr);
        assert!(out.status.success(), "helper failed:\n{stdout}\n{stderr}");
        assert!(
            stdout.contains("running 1 test\n")
                && stdout.contains("test x8_helper_publish_revocation ... ok")
                && stdout.contains("test result: ok. 1 passed; 0 failed; 0 ignored;"),
            "the helper entry did not run once:\n{stdout}"
        );
        let records: Vec<&str> = stderr
            .lines()
            .filter_map(|line| line.strip_prefix(PUBLISHED))
            .collect();
        assert_eq!(records.len(), 1, "published records:\n{stderr}");
        let (b, a) = records[0].split_once('|').expect("before|after");
        let versions = RevocationVersions {
            before: b.parse().unwrap(),
            after: a.parse().unwrap(),
        };
        assert!(versions.after > versions.before, "{versions:?}");
        assert_eq!(versions.before, before);
        assert_eq!(revocation_version(home), versions.after);
        versions
    }

    // ------------------------------------------------ project files

    /// Replace `path` with a new file of `bytes`: a copy made beside it with
    /// `cp -p` (its mode, owner, flags and ACL kept), rewritten, then renamed
    /// over it. Its identity always changes; nothing else that custody
    /// checks does, except the bytes when `bytes` differ.
    pub(crate) fn replace(path: &Path, bytes: &[u8]) {
        let before = fs::metadata(path).unwrap();
        let name = path.file_name().unwrap().to_str().unwrap();
        let fresh = path.with_file_name(format!(".x8c-{name}"));
        let copied = Command::new("/bin/cp")
            .arg("-p")
            .arg(path)
            .arg(&fresh)
            .status()
            .unwrap();
        assert!(copied.success(), "cp -p {}", path.display());
        let mut writable = before.permissions();
        writable.set_mode(before.permissions().mode() | 0o200);
        fs::set_permissions(&fresh, writable).unwrap();
        fs::write(&fresh, bytes).unwrap();
        fs::set_permissions(&fresh, before.permissions()).unwrap();
        fs::rename(&fresh, path).unwrap();
        let after = fs::metadata(path).unwrap();
        assert_ne!(
            (before.dev(), before.ino()),
            (after.dev(), after.ino()),
            "{} was not replaced",
            path.display()
        );
        assert_eq!(after.mode(), before.mode());
        assert_eq!(fs::read(path).unwrap(), bytes);
    }
    /// A lineage node naming another generation: the same canonical node
    /// with its `storeGeneration` one higher.
    pub(crate) fn another_generation(node: &[u8]) -> Vec<u8> {
        let mut value = object(&parse_json(node).unwrap()).clone();
        let V::Integer(generation) = &value["storeGeneration"] else {
            panic!("lineage node: storeGeneration")
        };
        let next = generation.get().checked_add(1).unwrap();
        value.insert(
            "storeGeneration".into(),
            V::Integer(opensip_identity::JsonInteger::new(next).unwrap()),
        );
        opensip_identity::canonical_bytes(&V::Object(value)).unwrap()
    }
}

/// Item 5a's helper entry, in X9 item 3's shape: an ordinary `#[test]`
/// (never `#[ignore]`d, so no harness flag decides whether its body runs)
/// that returns at once unless `OPENSIP_X8_HELPER` is set. In the lane's own
/// run it passes trivially and publishes nothing.
#[cfg(target_os = "macos")]
#[test]
fn x8_helper_publish_revocation() {
    if let Some(mode) = std::env::var_os(x8c::HELPER) {
        x8c::helper_publish(mode);
    }
}

/// The run candidate's registry shim names exactly storage's selected
/// sources: host's and storage's `SOURCES` list the same 48 files, in order.
#[cfg(target_os = "macos")]
#[test]
fn the_candidate_registry_is_storages_selected_registry() {
    let crates = workspace_manifest().parent().unwrap().join("crates");
    let sources = |krate: &str| -> Vec<String> {
        let text =
            std::fs::read_to_string(crates.join(krate).join("src/schema_sources.rs")).unwrap();
        let start = text.find("const SOURCES: &[&[u8]] = &[").expect("SOURCES");
        let end = start + text[start..].find("\n];").expect("SOURCES end");
        text[start..end]
            .split('"')
            .filter(|s| s.starts_with("/../../schemas/sources/") && s.ends_with(".schema.json"))
            .map(str::to_owned)
            .collect()
    };
    let storage = sources("storage");
    assert_eq!(storage.len(), 48);
    assert_eq!(sources("host"), storage);
    assert!(schema_sources::registry().is_some());
}

/// B0, the lawful control (X3d): the same harness, home and corpus reach a
/// commit. The synthetic candidate bound to the session's project and core
/// evaluator closure replays, prepares and publishes: `Committed`, not
/// latched; after `finish`, one SEAL, no REV or CLN, one receipt.
#[cfg(target_os = "macos")]
#[test]
fn synthetic_b0_the_lawful_control_commits() {
    use opensip_storage::{CommitOutcome, prepare_commit};
    let case = x8c::case("b0");
    let (home, _root, session, bound) = x8c::open(&case, "b0");
    let (run, run_id) = x8c::candidate_replay(&session);
    assert_eq!(run.evaluator_closure(), bound.evaluator_closure);
    assert_ne!(bound.evaluator_closure, bound.core_closure);
    let prepared = prepare_commit(run, session).expect("B0 prepares");
    let (outcome, stopped) = prepared.publish();
    let CommitOutcome::Committed(published) = outcome else {
        panic!("B0 did not commit: {outcome:?}")
    };
    assert!(!published.latched_after_admission());
    assert_eq!(published.run_id(), run_id);
    assert_eq!(published.execution_id(), bound.execution);
    assert_eq!(published.commit_sequence(), 1);
    assert_eq!(opensip_host::authoritative_run(&published).run_id(), run_id);
    let end = stopped.finish();
    assert!(
        !end.revocation_appended() && !end.cleanup_appended(),
        "{end:?}"
    );
    assert_eq!(end.settlement_failure(), None);
    assert!(end.end_step_entered());
    assert_eq!(end.end_step_failure(), None);
    let (carrier, ledger) = x8c::census(&home, &bound);
    assert_eq!(x8c::records(&carrier), (1, 0, 0), "{carrier:?}");
    assert_eq!(ledger.receipts, 1, "{ledger:?}");
    assert_eq!(ledger.attempts.len(), 1, "{ledger:?}");
    assert_eq!(ledger.attempts[0].0, bound.execution);
}

/// B1, admitted input (X3d-2, item 3 step 1): a `ReplayedRun` of another
/// corpus Run (host's pinned replay reference, `packet-1-original`), which
/// names another project. `Refused` on the invariant row; after `finish`,
/// no attempt row, no SEAL, no receipt, and the latched gate's REV.
#[cfg(target_os = "macos")]
#[test]
fn synthetic_b1_another_runs_replay_does_not_bind() {
    use opensip_storage::{NotPrepared, prepare_commit};
    let case = x8c::case("b1");
    let (home, _root, session, bound) = x8c::open(&case, "b1");
    let run = x8c::Corpus::case("packet-1-original")
        .replay()
        .expect("the corpus Run replays");
    let opensip_identity::JsonValue::Object(descriptor) = run.run() else {
        panic!("run")
    };
    assert_ne!(
        descriptor["projectId"],
        opensip_identity::JsonValue::String(bound.project.clone())
    );
    let Err((NotPrepared::Refused(row), stopped)) = prepare_commit(run, session) else {
        panic!("B1 was not refused")
    };
    assert_eq!(row, opensip_security::InstallationTermination::Invariant);
    assert_eq!(
        x8c::public(&row),
        (
            "SYSTEM.OUTCOME.ILLEGAL_STATE".into(),
            Some("HOST.INVARIANT_VIOLATED".into()),
            None
        )
    );
    assert_eq!(stopped.execution_id(), Some(bound.execution.as_str()));
    x8c::refused_end(&stopped.finish());
    let (carrier, ledger) = x8c::census(&home, &bound);
    assert_eq!(x8c::records(&carrier), (0, 1, 0), "{carrier:?}");
    assert_eq!(
        ledger,
        opensip_storage::scenario::LedgerCensus::default(),
        "no attempt row"
    );
}

/// B2, inventory (X3d-2, binding X3d-3; X3d r8 item 3 step 1, EC1): a
/// `ReplayedRun` that names the session's project but whose evaluator
/// closure is not the session's core evaluator closure (the pinned corpus
/// Run with only its `projectId` rebound). The same invariant row and
/// census as B1.
#[cfg(target_os = "macos")]
#[test]
fn synthetic_b2_another_evaluator_closure_does_not_bind() {
    use opensip_storage::{NotPrepared, prepare_commit};
    let case = x8c::case("b2");
    let (home, _root, session, bound) = x8c::open(&case, "b2");
    let candidate = run_candidate::project_rebound_corpus(&bound.project);
    let run = opensip_evaluator::replay_run(
        &candidate.retained_inputs(),
        candidate.run_id(),
        run_candidate::synthetic_replay_limits(),
    )
    .expect("the rebound corpus Run replays");
    let opensip_identity::JsonValue::Object(descriptor) = run.run() else {
        panic!("run")
    };
    assert_eq!(
        descriptor["projectId"],
        opensip_identity::JsonValue::String(bound.project.clone())
    );
    assert_ne!(run.evaluator_closure(), bound.evaluator_closure);
    assert_ne!(run.evaluator_closure(), bound.core_closure);
    let Err((NotPrepared::Refused(row), stopped)) = prepare_commit(run, session) else {
        panic!("B2 was not refused")
    };
    assert_eq!(row, opensip_security::InstallationTermination::Invariant);
    assert_eq!(
        x8c::public(&row),
        (
            "SYSTEM.OUTCOME.ILLEGAL_STATE".into(),
            Some("HOST.INVARIANT_VIOLATED".into()),
            None
        )
    );
    x8c::refused_end(&stopped.finish());
    let (carrier, ledger) = x8c::census(&home, &bound);
    assert_eq!(x8c::records(&carrier), (0, 1, 0), "{carrier:?}");
    assert_eq!(
        ledger,
        opensip_storage::scenario::LedgerCensus::default(),
        "no attempt row"
    );
}

/// B3 and B5's shared shape (X4a with X3d; X4 r7 items 4 and 8): after the
/// handoff and `open`, `alter` replaces a file the guard holds; the
/// synthetic candidate then prepares (its attempt row is admitted) and
/// `publish`'s first checkpoint refuses on the custody row, latching the
/// gate before admission. After `finish`: the attempt row `admitted`, no
/// SEAL, one REV, no CLN (no SEAL is durable, so X3d item 7 owes none), no
/// receipt.
#[cfg(target_os = "macos")]
fn custody_case(name: &str, alter: impl FnOnce(&opensip_security::scenario::ScenarioPaths)) {
    use opensip_storage::{CommitOutcome, prepare_commit};
    let case = x8c::case(name);
    let (home, root, session, bound) = x8c::open(&case, name);
    alter(&home.paths(&root, &bound.namespace));
    let (run, _) = x8c::candidate_replay(&session);
    let prepared = prepare_commit(run, session).expect("the attempt is admitted");
    let (outcome, stopped) = prepared.publish();
    let CommitOutcome::Refused(row) = outcome else {
        panic!("{name} was not refused: {outcome:?}")
    };
    assert_eq!(
        row,
        opensip_security::InstallationTermination::Custody {
            subject: "required-files-changed"
        }
    );
    assert_eq!(
        x8c::public(&row),
        (
            "CONFIG.INVALID".into(),
            Some("CONFIG.CUSTODY_REFUSED".into()),
            Some("required-files-changed".into())
        )
    );
    x8c::refused_end(&stopped.finish());
    let (carrier, ledger) = x8c::census(&home, &bound);
    assert_eq!(x8c::records(&carrier), (0, 1, 0), "{carrier:?}");
    assert_eq!(
        ledger.attempts,
        vec![(bound.execution.clone(), "admitted".to_owned())]
    );
    assert_eq!(ledger.receipts, 0);
}

/// B3, namespace: the project marker replaced (same bytes, new file).
#[cfg(target_os = "macos")]
#[test]
fn synthetic_b3_a_replaced_marker_is_refused_at_the_checkpoint() {
    custody_case("b3-marker", |paths| {
        let bytes = std::fs::read(&paths.marker).unwrap();
        x8c::replace(&paths.marker, &bytes);
    });
}

/// B3, namespace, separately: N's writer lease file replaced (same bytes,
/// new file) under the session's held lease.
#[cfg(target_os = "macos")]
#[test]
fn synthetic_b3_a_replaced_lease_file_is_refused_at_the_checkpoint() {
    custody_case("b3-lease", |paths| {
        let bytes = std::fs::read(&paths.writer_lease).unwrap();
        x8c::replace(&paths.writer_lease, &bytes);
    });
}

/// B4, execution (X3d-2 / X3c; F34): an `admitted` attempt row for the
/// session's own ExecutionId, planted through the ledger's ordinary insert
/// before `prepare_commit`. `ExistingAttempt` with that ExecutionId and the
/// requested binding disclosed; it stays on the invariant row until X6
/// routes it (X6 r3 item 6, X7 r6). After `finish`: the planted row
/// unchanged and alone, no SEAL, no receipt, and the latched gate's REV.
#[cfg(target_os = "macos")]
#[test]
fn synthetic_b4_an_existing_attempt_is_not_overwritten() {
    use opensip_storage::scenario::{StoreBinding, plant_attempt};
    use opensip_storage::{NotPrepared, prepare_commit};
    let case = x8c::case("b4");
    let (home, _root, session, bound) = x8c::open(&case, "b4");
    let (carrier_digest, operation_ref) = (
        session.carrier_digest().to_owned(),
        session.operation_ref().to_owned(),
    );
    let binding = StoreBinding {
        namespace: &bound.namespace,
        store: &bound.store,
        generation: session.store_generation(),
        schema: session.state_schema(),
    };
    plant_attempt(&home, binding, &bound.execution).expect("the row is planted");
    let planted =
        opensip_storage::scenario::ledger_census(&home, &bound.store, &bound.namespace).unwrap();
    assert_eq!(
        planted.attempts,
        vec![(bound.execution.clone(), "admitted".to_owned())]
    );
    let (run, _) = x8c::candidate_replay(&session);
    let Err((
        NotPrepared::ExistingAttempt {
            execution_id,
            requested,
        },
        stopped,
    )) = prepare_commit(run, session)
    else {
        panic!("B4 was not ExistingAttempt")
    };
    assert_eq!(execution_id, bound.execution);
    assert_eq!(requested.namespace_id(), bound.namespace);
    assert_eq!(requested.journal_carrier_digest(), carrier_digest);
    assert_eq!(requested.operation_ref(), operation_ref);
    let digest = requested.store_generation_digest();
    assert!(digest.len() == 64 && digest.bytes().all(|b| b.is_ascii_hexdigit()));
    // The invariant row (X7a projects it with the ExecutionId as subject).
    let row = opensip_security::InstallationTermination::Invariant;
    assert_eq!(
        x8c::public(&row),
        (
            "SYSTEM.OUTCOME.ILLEGAL_STATE".into(),
            Some("HOST.INVARIANT_VIOLATED".into()),
            None
        )
    );
    x8c::refused_end(&stopped.finish());
    let (carrier, ledger) = x8c::census(&home, &bound);
    assert_eq!(x8c::records(&carrier), (0, 1, 0), "{carrier:?}");
    assert_eq!(ledger, planted, "the planted row, unchanged and alone");
    assert_eq!(ledger.receipts, 0);
}

/// B5, generation (X4a / X3a): the selected endpoint's lineage node
/// replaced by one naming another generation. The custody row; as B3.
#[cfg(target_os = "macos")]
#[test]
fn synthetic_b5_a_lineage_node_naming_another_generation_is_refused() {
    custody_case("b5", |paths| {
        let node = paths.lineage.as_ref().expect("the selected lineage node");
        let bytes = std::fs::read(node).unwrap();
        let other = x8c::another_generation(&bytes);
        assert_ne!(other, bytes);
        x8c::replace(node, &other);
    });
}

/// B6, live revocation (X4a; F18): after the handoff, item 5a's helper
/// process publishes a revocation naming the session's core closure (the
/// closure's `release` subject), and the test thread waits for it to exit.
/// The first checkpoint's monitored observation reads it: `Refused` on
/// `TRUST.COMPONENT_REVOKED_DURING_OPERATION`, the gate latched before
/// admission. The census as B3.
#[cfg(target_os = "macos")]
#[test]
fn synthetic_b6_a_live_revocation_of_the_core_closure_is_refused() {
    use opensip_storage::{CommitOutcome, prepare_commit};
    let case = x8c::case("b6");
    let (home, _root, session, bound) = x8c::open(&case, "b6");
    x8c::publish_through_helper(&case, &home, &[("release", &bound.core_closure)]);
    let (run, _) = x8c::candidate_replay(&session);
    let prepared = prepare_commit(run, session).expect("the attempt is admitted");
    let (outcome, stopped) = prepared.publish();
    let CommitOutcome::Refused(row) = outcome else {
        panic!("B6 was not refused: {outcome:?}")
    };
    assert_eq!(
        row,
        opensip_security::InstallationTermination::RevokedDuringOperation {
            subject: "trust-revoked"
        }
    );
    assert_eq!(
        x8c::public(&row),
        (
            "EXTENSION.ADMISSION_REJECTED".into(),
            Some("TRUST.COMPONENT_REVOKED_DURING_OPERATION".into()),
            Some("trust-revoked".into())
        )
    );
    x8c::refused_end(&stopped.finish());
    let (carrier, ledger) = x8c::census(&home, &bound);
    assert_eq!(x8c::records(&carrier), (0, 1, 0), "{carrier:?}");
    assert_eq!(
        ledger.attempts,
        vec![(bound.execution.clone(), "admitted".to_owned())]
    );
    assert_eq!(ledger.receipts, 0);
}

/// B7, unrelated revocation (X4a): the same helper publishes a revocation
/// naming nothing in any closure. `Committed`, not latched; the census as
/// B0.
#[cfg(target_os = "macos")]
#[test]
fn synthetic_b7_an_unrelated_revocation_still_commits() {
    use opensip_storage::{CommitOutcome, prepare_commit};
    let case = x8c::case("b7");
    let (home, _root, session, bound) = x8c::open(&case, "b7");
    x8c::publish_through_helper(&case, &home, &[]);
    let (run, run_id) = x8c::candidate_replay(&session);
    let prepared = prepare_commit(run, session).expect("B7 prepares");
    let (outcome, stopped) = prepared.publish();
    let CommitOutcome::Committed(published) = outcome else {
        panic!("B7 did not commit: {outcome:?}")
    };
    assert!(!published.latched_after_admission());
    assert_eq!(published.run_id(), run_id);
    let end = stopped.finish();
    assert!(
        !end.revocation_appended() && !end.cleanup_appended(),
        "{end:?}"
    );
    assert_eq!(end.settlement_failure(), None);
    assert!(end.end_step_entered());
    let (carrier, ledger) = x8c::census(&home, &bound);
    assert_eq!(x8c::records(&carrier), (1, 0, 0), "{carrier:?}");
    assert_eq!(ledger.receipts, 1, "{ledger:?}");
    assert_eq!(ledger.attempts.len(), 1, "{ledger:?}");
    assert_eq!(ledger.attempts[0].0, bound.execution);
}

/// B8, replay-invalid (X5a; F01, build plan line 609): one byte of a claimed
/// output altered. `replay_run` returns `Mismatch`, so no `ReplayedRun`
/// exists to pass on (group K pins that nothing else can stand in); the
/// refusal comes before any fence, so the scratch home holds no namespace,
/// carrier, lease, ledger or marker for the project.
#[cfg(target_os = "macos")]
#[test]
fn synthetic_b8_an_altered_claimed_output_never_replays() {
    let case = x8c::case("b8");
    let home = opensip_security::scenario::ScenarioHome::create(&case.homes);
    let root = home.project("b8");
    let mut corpus = x8c::Corpus::case("selected-complete-file-positive");
    corpus.replay().expect("the unaltered corpus Run replays");
    let (altered, original) = corpus.alter_one_claimed_byte();
    assert_ne!(altered, original);
    let refusal = corpus
        .replay()
        .err()
        .expect("an altered output never replays");
    assert_eq!(
        refusal,
        opensip_evaluator::ReplayError::Mismatch {
            key: "EVALUATOR_COMPLETE_PROOF_REPLAY",
            target: None
        }
    );
    // Before any fence: no registration, namespace, carrier, lease or ledger.
    assert!(!root.join(".opensip").exists());
    let projects = home.installation().join("host/projects");
    let namespaces: Vec<_> = match std::fs::read_dir(&projects) {
        Ok(entries) => entries.map(|e| e.unwrap().file_name()).collect(),
        Err(e) if e.kind() == std::io::ErrorKind::NotFound => Vec::new(),
        Err(e) => panic!("{}: {e}", projects.display()),
    };
    assert!(namespaces.is_empty(), "{namespaces:?}");
    let ledgers = home
        .installation()
        .join("stores")
        .join(home.store())
        .join("projects");
    assert!(!ledgers.exists(), "{}", ledgers.display());
}
