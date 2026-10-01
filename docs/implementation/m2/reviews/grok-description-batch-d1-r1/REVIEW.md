# D1 r1 — description-batch contract successor

**Verdict: ACCEPT-DESIGN-UNIT**

Thirty-nine `/files/N/description` overrides on inventory v119. Each new description is true of the product at `8240856a635d3fffb44f869465f87341cac399d0`. Each edit keeps every sentence that is still true word for word, replaces text that is false, and inserts short clauses for what the file now does. No true sentence is dropped. No plain v119 row whose description is now false is missing from the batch. The successor is well-formed for selection. `requiredFindings` is empty.

## Subject

| Pin | Bytes | SHA-256 |
| --- | ---: | --- |
| `docs/implementation/m2/description-batch-d1-subject.json` | 1037 | `44ec70cd2179022e36158acd23c481942194861728a3abb9d7aa077e897ef982` |
| `docs/implementation/m2/description-batch-d1/successor.json` | 124472 | `2a2f94a61515c175efb3e88eb619626b0c0709682a8724a7fa119576f95a27c9` |

All eight `hashes.txt` rows match, including the README, `evidence/build_d1.py`, `evidence/descriptions.json`, `evidence/verify_scratch.py`, this review's `REQUEST.md`, and the convenience `rationales.json`. `rationales.json` is not part of the subject. The parent is `docs/implementation/m2/repository-file-inventory.v119.json` (469771 bytes, `34443e615d5c30f64e7f93c56d3b6e60b6afa06712d3489c127ecc858e4e21c6`). Product main is `8240856a635d3fffb44f869465f87341cac399d0` and its working tree is clean. `~/Library/Application Support/OpenSIP` is absent. No product cargo was run. There is no inventory candidate.

`successor.json` is schemaVersion 1, one parent (the v119 pin above), 39 `passageOverrides`, and candidates for the README and the three evidence files. `descriptions.json` before/after text is identical to those overrides. Every `before` equals the v119 row. No override selector is one of the 16 inherited pointers. Paths are unique. Every `after` is non-empty, different from `before`, and contains no newline. Overrides are sorted by inventory index.

`evidence/build_d1.py` was not executed: it writes `successor.json` and the subject manifest into the architecture tree. A read-only reconstruction of its record equals both pinned files byte for byte. The script refuses a before mismatch, an inherited row, a duplicate path, and an empty or unchanged `after`.

## Verifier

`python3.14 -I -B verify_scratch.py`, run from `description-batch-d1/evidence` with `PATH=/opt/homebrew/bin:/usr/bin:/bin`, exited 0:

- `passed`: true
- `selectedInventory`: `docs/implementation/m2/repository-file-inventory.v119.json`
- `contractSuccessors`: 73
- `inventoryPassageInheritance`: 16
- `d1.selected`: `docs/implementation/m2/description-batch-d1/successor.json`, `passageOverrides`: 39
- generation sources verified: 40; `executedGeneratorCode`: false
- admission sources verified: 48; aliases verified: 15; `executedRuntimeCode`: false

The scratch lock is the real lock with D1 appended. Review and assent records are synthetic and stay in memory. The architecture tree was not written. Live `verify_design` at 8240856 was left as the lead reported it; the scratch run exercises the same generators and admission sources against that lock plus D1.

## Judgment calls

### 1. ACCEPT

VD1 stays deferred. The four stale rows are inherited projection pointers, and a direct override on any of them conflicts with that projection. The indexes are `read_premise.rs` 369, `installation_session.rs` 353, `store_lineage.rs` 254, and `initial_installation.rs` 379. Their current sentences are stale: `read_premise.rs` still says no read path uses it, `installation_session.rs` still says no consumer uses it, `store_lineage.rs` omits `SuppliedChain::into_nodes`, and `initial_installation.rs` omits the X3d-1 settlement reserve. Changing the trust anchor inside this description unit is rejected. These four rows wait for VD1, a separately reviewed `tools/verify_design.py` change.

### 2. ACCEPT

The batch includes every description a README or review deferred to the description-only successor through X4B-b, including rows the EXIT-PLAN D1 entry did not copy (the X3b-4 carrier rows, the X4a rows, `admission_tests.rs`, and `work_ledger.rs`). That is the batch that closes those deferrals in one successor.

### 3. ACCEPT

Index 408 `revocation.rs` is rewritten to the file. The module is a private fail-stop `FreshnessMonitor`: no polling thread, no journal append, no cancellation, and no operational authority. X4 r7 shares one monitor per operation. `OBSERVATION_BOUND` is `Duration::from_secs(10)`. `Sample` carries before, after, boot, wall_seconds, and wall_nanos. `StopReason::subject` maps to clock-unavailable, clock, unreadable, stalled, and latched (`OBSERVER.FAIL_STOP`). `read_sampled_with` latches on any failure and replaces history only on success. `boundary_with` is one clock sample and no I/O: boot must match, the sample may not precede the last read's end, elapsed time stays within the bound, history is not refreshed, and failure latches. A boot change or regression is `MalformedClock`. Unwind latches through `StopOnUnwind`. Epoch observation is `root_payload`'s `observe_revocation`. The checkpoint is `operation_guard`'s. The planned "observe trust epochs" text was never this file.

### 4. ACCEPT

Index 327 `commit_authority.rs` is `FinalGate`, `OperationGate`, and `PreparedJournalSeal`. `FinalGate::admit` is `compare_exchange(0, ADMITTED, SeqCst, SeqCst)`. `latch` is `fetch_or(LATCHED, SeqCst)`. The barrier comments are `x4.gate.latch.after` after the fetch-OR and `x4.gate.admit.after` after a successful exchange. `OperationGate::admit` returns `Err((prepared, state))` and hands the value back; a second call is refused by the gate's own state. `PreparedAttempt` is that same `FinalGate` created with its prepared value. `CommitSession`, `JournalWriteTxn`, and `JournalSealBinding` live in `custody/commit_session.rs`. The S6 checkpoint is `operation_guard`'s. `PreparedJournalSeal::bind` refuses another record type, a missing or fixture run id, a mismatched run, and the absence of live custody. Those types are not constructed here.

### 5. ACCEPT

Index 134 `admission_tests.rs` keeps the planned first sentence. The behavioural cases that sentence names are X8c's. The header is the X8a compile-fail driver: census and self-test, groups I/K/L, X4a group D unnameable rows for `AdmissionPermit`, `FinalGate`, and `OperationGuard`, X3d-1 session types in groups D/E/F/G, rustc 1.95.0, and the scenario-fixtures pin. The `CASES` array holds 23 `case()` entries and 53 `owned()` entries (50 from unit X3d-1, 3 from unit X4a). `SELFTESTS` lists 8 files. `census()` checks the table before compile. The file contains `opaque_api_misuse_fails_for_the_intended_reason` and `annotations_are_parsed_exactly`.

### 6. ACCEPT

Rows 118 (host) and 382 (security) describe terminations by kind and say "existing codes". `LedgerCorrupt` and `CommitUndetermined` publish no domain detail (`failed(..., None)`). `MigrationCorrupt` publishes `Detail::MigrationCorrupt`. Host `StateSchemaUnsupported` is request-rejected, exit 2, `RequestSchemaMajorUnsupported`. `TrustRoot` `SchemaUnsupported` uses that same request code; every other `RootDetail` uses `ExtensionAdmissionRejected`. All nine `RootDetail` variants exist (`ChainGap`, `ChainBackdated`, `ChainOldThreshold`, `ChainNewThreshold`, `FinalExpired`, `FinalFuture`, `ExpiredNoChain`, `StateInconsistent`, `SchemaUnsupported`). The sentence that each `ROOT.*` chain detail projects to its own code, and that only `ROOT.SCHEMA_UNSUPPORTED` leaves the admission class, holds when "code" is the distinct detail and "admission class" is `ExtensionAdmissionRejected`. `Invariant` is operational-failed, exit 4, `SYSTEM.OUTCOME.ILLEGAL_STATE`, detail `HOST.INVARIANT_VIOLATED`.

The host header at `crates/host/src/installation_termination.rs` lines 11–12 still says nothing emits the table yet. That product comment is disclosed with call 8.

### 7. ACCEPT

The `operation_handoff.rs` override (index 360) is 3989 characters. The longest existing v119 description is 3232. True sentences stay as verbatim prefixes, with short clauses inserted. Rewording true text to save space is rejected.

### 8. ACCEPT

These stay in product code and are disclosed for the lead's code follow-up:

- `crates/security/src/journal_store/carrier_floor.rs` lines 114–116 still say there is no production constructor until X3b-3. The description says `CarrierLocation::admitted`, built from X2e's confirmed `CarrierPlace`, is the only production constructor.
- `crates/security/src/custody/installation_doctor.rs` line 11 still says "Library only." The ingress calls `observe_installation_for_doctor` (`doctor_ingress.rs`).
- The security `InstallationTermination::Invariant` doc still says only a broken caller reaches it. X4B-b's second F absent also reaches it, and the security termination description says so.
- `crates/host/src/installation_termination.rs` lines 11–12 still say nothing emits the table yet.

Doctor path, confirmed. `row_remedy` maps `StateSchemaUnsupported`, `ConfigInvalid`, `PolicyImperativeKeyRefused`, and `HostInvariantViolated`. Every other detail is `MetadataError::Projection`. The map does not list Trust*, Root*, `PayloadNotAdmissible`, `ClockExcursionForward`, `TrustComponentRevokedDuringOperation`, `ObserverFailStop`, or `MigrationCorrupt`. `observe_installation_for_doctor` goes through `doctor_observation`, `session_refusal`, and `gate_refusal`, which produce only the 468 rows, `StateSchemaUnsupported`, `Incomplete` (core and current-store collapse to Incomplete for the session; `findings()` maps those two to findings), and `Invariant` (latched, or a missing Home, Installation, or Parent finding). Doctor runs no trust admission and no operation, so the X4a and X3d-1 termination rows are not constructed on this path. A detail with no remedy would be a projection error if one of those rows were passed to `row_remedy`. `doctor_ingress_tests::rows()` lists the 468 rows plus `StateSchemaUnsupported` and `Invariant`, which is the coverage the new description claims.

Envelope kinds match the description. A report envelope is kind `doctor`. A refused envelope is kind `failure`. The host I/O row names no domain detail, so `refused_envelope` puts `Detail::HostIoFailure` into `errors` to satisfy the schema's non-empty `errors`. Exit codes come from the class only (success 0, request-rejected 2, operational-failed 4). `doctor_report` matches its added sentences: an unreachable installation returns the 468 row and no report; each structural finding, including X3a core and current-store, is one `CONFIG.CUSTODY_REFUSED` with an `installation-incomplete` subject; `DOCTOR.DEFECTS_FOUND` carries the selected-golden remedy constant; the ingress emits the report through `doctor_installation`, passing an empty other-checks vector.

### 9. ACCEPT

`tools/verify_design.py` projects a passage override only when the parent path is an ancestor of the final selected inventory. A direct override whose parent is the selected inventory leaves `inventoryPassageInheritance` at 16. The scratch run records that: 16 rows, v119 selected, 39 overrides, all parented on v119. The 39 file paths are disjoint from the 16 inherited paths. Once D1 is selected, the next inventory successor carries these 39 description rows by value. The projection then grows from 16 to 55, in verify_design's canonical order (parent path, then lexicographic selector JSON, so `/files/10` sorts before `/files/2`), and the projection helper's count becomes 55. The same step took the lock from 8 to 16. `inventory_successor` requires inherited rows to be equal by value, so an inventory successor cannot carry these description edits. `build_d1.py` finds rows by path, so a parent-only rebuild after another inventory is selected needs no script edit and needs a new review.

## Descriptions against 8240856

Confirmed in the committed tree: the doctor ingress, report, and tests; both termination tables and the nine `RootDetail` variants; `seal_fits` and the capacity-window test (`SEAL_CEILING` is 9007199254740987; a SEAL takes 9007199254740988 and is refused above the ceiling; RA, REV, and CLN take 9007199254740990 and are refused there as `GenerationFull` on the busy row; TERMINAL is refused below its window and on an empty tail and admitted after tails 9007199254740988 through 9007199254740990; only `carrier_rollover.rs` calls `append_terminal`; `RecordDraft` contains no TERMINAL); the six-file pin in `only_the_commit_sessions_end_path_reserves_or_settles` (`work_ledger.rs`, platform `lib.rs`, `initial_installation.rs`, `read_premise.rs`, `operation_handoff.rs`, `commit_session.rs`); `OperationGuard::stop` as `gate.latch()` with no recorded cause; `namespace_lease`'s `lease_free`, `into_parts`, `recheck_namespace_at`, and `recheck_held` (a granted exclusive probe is dropped and refused as `NamespaceRefusal::Busy`); `BootstrapDocuments` (`catalog`, `manifests`, `revocation`) and `bootstrap_release`; `native_current`'s `parts_mut` (capsule, descriptor, bindings, and the capture's native store) and `CURRENT_STATE_CAP`; `WriteTransaction::stage_run_material` (inserts `commit_run_material`, returns `material.blobs`, commits nothing); `project_ledger` mapping `ObjectDeclaration` and `StagingMismatch` to `ProjectLedgerRow::Invariant`; `admit_project_root` as the walk from launch or explicit; the FreshnessMonitor body; and the FinalGate body.

The three X4B-b sentences this series had marked stale are in the batch and match the accepted wiring: `trust_bootstrap.rs` (497) names `bootstrapping_first_read`, maps a second F absent to `TrustRow::Invariant`, and says the confirming admission is X4T's own; `live_observation.rs` (452) narrows the "never takes the fence" claim to the observation, because `fenced_operation_read` writes when F is absent; `operation_live_tests.rs` (362) replaces the P0 refusal-before-any-lease clause with the X4B-b acceptance inside the first read. `trust_bootstrap_tests` (498) and `current_trust_admission` (435) replace the FirstIdentity stated-gap wording with the two-root reader: `heads.root` is the signing root, and the accepted root is the closure's first rootChain document.

Kept outside the batch, and still true: `clock_observation.rs` (the X4a projection remains `project_monitor_sample`) and `operation_guard_tests.rs` (the fenced-admission termination sentence still covers the X4B-b `Invariant` row). `floor_publication.rs` still says it mints `ConfirmedCurrent` for `advance_current`; `confirmations()` returns `&[ConfirmedCurrent]`, so that sentence is understated and still true. `live_observation_tests.rs` still classifies every other reread row as a fail-stop. `current_trust_admission_tests.rs` still says `accepted.by` must name a loaded event of that role; an event opened by reference is loaded. The short re-export descriptions on `trust.rs`, `ordinary_targets.rs`, and `root_payload.rs` stay true. `commit_session.rs` keeps its v119 description; that file is unchanged since the inventory that wrote it.

Files X4B-b changed and that this batch does not override are one of the four VD1 rows, one of the kept rows above, or a generic re-export.

## requiredFindings

Empty. No description's bytes should change.
