# Stale inventory descriptions after X1 to X4B-b: contract successor D1

2026-10-01. Claude Opus 5.5, implementation lead. This is unit D1 of EXIT-PLAN.md ("D1 (description batch)" and the later notes that add rows to it). It changes descriptions only. It makes no schema, registry, generated-code, product-file or inventory-successor change.

## Mechanism

This unit follows 461b's shape. It makes 39 JSON Pointer `/files/N/description` overrides on the inventory the product lock selects, `repository-file-inventory.v119.json`, and that inventory is the successor's only parent. verify_design's `contract_successor` accepts an override when:
- its parent is an accepted base or selected inventory;
- its `before` text equals the parent's passage;
- its `after` text is non-empty and different.

An inventory successor cannot do this, because `inventory_successor` requires every inherited row to be equal by value (X4T-a3 judgment call 1). A direct override on the final inventory is not projected, so `inventoryPassageInheritance` stays at its 16 rows.

**Plain rows only.** No row touched here is one of the 16 inherited projection rows. `build_d1.py` refuses any such row. A direct override on an inherited row conflicts with its projection, and verify_design refuses it ("inherited inventory meaning conflicts with direct override"; see `stale-descriptions-x1b/probe.py`). Those rows wait for VD1 (below).

**After selection.** Once D1 is selected, the next inventory successor must do two things:
- carry these 39 rows by value;
- add their meanings to the lock's `inventoryPassageInheritance`, which grows from 16 to 55 rows, sorted by verify_design's canonical order.

Its projection helper's row count changes the same way, as it did after 461b (8 to 16). If another inventory successor is selected before D1, `build_d1.py` rebuilds on it with no edit, because rows are found by path. That rebuild needs a new review, because the pins change.

## Rows (product main 8240856)

The exact before and after text is in `evidence/descriptions.json` and in `successor.json`. Every new description was written against the committed code at 8240856. Sentences that are still true are kept word for word.

| v119 | File | What was stale |
|---|---|---|
| 107 | crates/host/src/doctor_ingress.rs | Omitted the STATE.SCHEMA_UNSUPPORTED row's remedy (X3a-1) and the shared failure envelope's X12 policy rows (X12b). |
| 108 | crates/host/src/doctor_ingress_tests.rs | Did not say which rows it covers, or that it covers the core and current-store findings. |
| 109 | crates/host/src/doctor_report.rs | "Library only: nothing emits it yet" was false (X10a). It also omitted X3a's findings. |
| 118 | crates/host/src/installation_termination.rs | Named only 468's rows, and said "nothing emits it yet". It now describes the X3a-1, X4a and X3d-1 rows by kind. |
| 134 | crates/host/tests/admission_tests.rs | The planned sentence is kept. It adds X8a's compile-fail driver and the census rows from X4a and X3d-1. Its behavioural cases are X8c's. |
| 304 | crates/platform/src/work_ledger.rs | Omitted 467's `prepaid` and X3d-0's settlement reserve. |
| 309 | crates/platform/tests/settlement_reserve_tests.rs | "until X3d-1" was out of date. It now describes X3d-1's end-path-chain pin. |
| 327 | crates/security/src/commit_authority.rs | Described the plan's placement of CommitSession, JournalWriteTxn and JournalSealBinding, which now live in commit_session.rs. It now describes the gate primitive (FinalGate, X4a's OperationGate) and PreparedJournalSeal. |
| 334 | crates/security/src/custody/first_registration_tests.rs | Omitted X2e's footprint test (Exact and Started). |
| 338 | crates/security/src/custody/installation_admission.rs | Omitted the X3a-1 one-read rule, the gate's ledger, and the accessors and advances added by X2c, X4T-b, X2e and X4a. |
| 339 | crates/security/src/custody/installation_admission_tests.rs | Omitted the X3a-1, X4T-b and X4B-b cases. |
| 340 | crates/security/src/custody/installation_doctor.rs | "Library only" was false, because the doctor ingress calls it. It also omitted X3a's findings. |
| 347 | crates/security/src/custody/installation_read.rs | "Nothing walks from the root again" was false. The replacement is v93's proposed sentence, verified against the code. It also adds store_endpoint, observe_project_tracking and admit_namespace. |
| 348 | crates/security/src/custody/installation_read_fixture.rs | Omitted select_generation and unroot (X3a), and the trust writers and F4 retry (X4a). |
| 356 | crates/security/src/custody/namespace_lease.rs | Omitted X4a's post-release guard and X2e's seams. |
| 358 | crates/security/src/custody/operation_guard.rs | Omitted OperationGuard::stop (X3d-1). |
| 360 | crates/security/src/custody/operation_handoff.rs | "OperationGuard (X4a) is a seam not built here" and "ProjectOperation is private" were false. It now adds the X4a, X3d-1 and X4B-b additions. |
| 361 | crates/security/src/custody/operation_handoff_tests.rs | Omitted the accepted-store fixture, the begin_test adapter, and the included live and commit-session tests. |
| 362 | crates/security/src/custody/operation_live_tests.rs | The P0 refusal case is now X4B-b's P0 acceptance case. |
| 363 | crates/security/src/custody/ordinary_writer.rs | The claim that it grants no store, trust, project, id, grant or commit standing was false. It now lists the steps from X3a-1, X2c, X2d, X2e, X4a and X4B-b. |
| 367 | crates/security/src/custody/project_chain.rs | The S3 judgment now also covers .opensip, the config file and Git evidence. It also adds the accessors X2b-2 uses. |
| 382 | crates/security/src/installation_termination.rs | Named only 468's rows. It now describes the full closed table by kind, including the wider invariant row. |
| 383 | crates/security/src/journal_store.rs | Omitted grant-generation succession (X3b-4) and the operation and commit-session surface. |
| 386 | crates/security/src/journal_store/carrier_append.rs | The "TERMINAL only at the reserved slot" and reconcile_after_uncertain text predated law X3b r9. It now gives the capacity table and append_terminal. |
| 387 | crates/security/src/journal_store/carrier_append_tests.rs | Same r9 staleness: the reconciled-tail copy and the reserved-slot tests. |
| 389 | crates/security/src/journal_store/carrier_floor.rs | "...the end step and the append are later units" and "no production constructor until X3b-3" were out of date. It now names the four child modules and X3b-4's succession. |
| 395 | crates/security/src/journal_store/carrier_start.rs | Post-uncertainty reconciliation and the reconciled-tail copy were removed by r9. It now covers OPEN, NoSuccessor and the copy tail. |
| 396 | crates/security/src/journal_store/carrier_start_tests.rs | Same r9 staleness in its uncertain-outcome cases. |
| 408 | crates/security/src/revocation.rs | The planned text ("observe trust epochs and enforce effect/SEAL checkpoints under the required journal ordering") was never this file. It is the fail-stop FreshnessMonitor (X4a). |
| 411 | crates/security/src/trust/accepted_store_fixture.rs | "The only constructor of these kinds" was false since trust_bootstrap. It also omitted the rotation chain and the Spec fields. |
| 412 | crates/security/src/trust/accepted_store_fixture_tests.rs | The pin claim "named by no other source file" was false, because it admits the X4T-a and X4T-b tests under cfg(test). |
| 435 | crates/security/src/trust/current_trust_admission.rs | The accepted root is now the chain's first root, with heads.root signing (X4T-a3). "It writes nothing" now holds only for the admission itself. It also adds the child modules and the retained evidence. |
| 447 | crates/security/src/trust/initial_core.rs | "law 463 r3–r8" now reads r3–r9, and it adds the bootstrap documents and lending (X4B-a). |
| 452 | crates/security/src/trust/live_observation.rs | fenced_operation_read now bootstraps on F absent and returns every confirmed publication in order (X4B-b). |
| 497 | crates/security/src/trust/trust_bootstrap.rs | "Not wired to the fenced first read (X4B-b); grants nothing" was false. |
| 498 | crates/security/src/trust/trust_bootstrap_tests.rs | The FirstIdentity "stated gap" was false since X4T-a3. It also adds X4B-b's tests. |
| 457 | crates/security/src/trust/native_current.rs | Omitted decode_current_store and CURRENT_STATE_CAP (X3a-1), and parts_mut (X4T-a). |
| 665 | crates/storage/src/ledger_store/project_ledger.rs | "No object publication, staging, commit..." now says those operations live in the child commit module (X3c-2). |
| 668 | crates/storage/src/ledger_store/recovery_material.rs | Omitted stage_run_material (X3c-2). |

**Checked and kept.** These rows were named as candidates and are still true:
- `crates/security/src/clock_observation.rs`: X4a's project_monitor_sample is the existing projection.
- `crates/security/src/custody/operation_guard_tests.rs`: X4B-b's one new termination row is covered by "every fenced admission row's termination".

## Deferred to VD1 (inherited override rows)

These rows' effective descriptions are inherited projections (the 16 `inventoryPassageInheritance` rows), so no contract successor can supersede them until VD1 lands:
- `crates/security/src/custody/read_premise.rs`: X1b's text, then the X2e, X4a and X3d-1 additions.
- `crates/security/src/custody/installation_session.rs`: X3a-1.
- `crates/identity/src/store_lineage.rs`: X3a-1's `SuppliedChain::into_nodes`.
- `crates/security/src/initial_installation.rs`: X3d-1's settlement reserve.

## Evidence

- `evidence/descriptions.json` holds each row's path, its exact v119 before text and its after text.
- `evidence/build_d1.py` rebuilds `successor.json` and `description-batch-d1-subject.json` deterministically from the lock-selected inventory. It refuses on any of these: a before mismatch, an inherited row, a duplicate, or an empty or unchanged after.
- `evidence/verify_scratch.py` runs the product checkout's real verify_design over a scratch lock: the real lock with this binding appended, and the review and assent synthetic in memory. It asserts three things:
  - the scratch lock passes;
  - the selected inventory and the 16 inheritance rows are unchanged;
  - every override's parent is the selected inventory.
