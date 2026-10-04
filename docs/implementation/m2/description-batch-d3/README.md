# Stale inventory descriptions after X3d-2 to X9-6: contract successor D3

2026-10-04. Claude Opus 5.5, implementation lead. This is unit D3, the third description batch, which follows D1 and D2. It covers the rows that X3d-2, X5a, X6a, X7a, X6b, X6c, X4B-c, X7b, X9-1, X8b, X3d-3, X9-2, X9-3, X9-5 and X9-6 left stale. It also covers X1b's `read_premise.rs` and the stale rows a full sweep found.

D3 changes descriptions only. It makes no schema, registry, generated-code, product-file or inventory-successor change.

## Mechanism

D3 is one record, and its only parent is `repository-file-inventory.v134.json`, the inventory the product lock selects at product 3d2d5b5. It uses both of verify_design's forms, as `build_d3.py` decides per row from the lock:

- **45 `passageOverrides` on plain rows (D1's form).** A plain row has no `inventoryPassageInheritance` entry and no supersession chain. Its `before` is the row's raw description.
- **17 `passageSupersessions` on inherited rows (law VD1 r1, D2's form).** An inherited row has exactly one inheritance entry. Its `before` is that entry's `after`, which is the row's current meaning, and its `supersedes` names the row's chain tail:
  - D1's override on v119, for 15 rows;
  - D2's supersession on v122, for `read_premise.rs` and `installation_session.rs`.

  No row whose tail is an older root override (461b, 468a, bootstrap-selection-v1 and the others) is stale at 3d2d5b5.

A direct override of an inherited row would conflict with its projection, and an override of a superseded row would restate a superseded meaning. verify_design refuses both, and `build_d3.py` asserts neither occurs. Every entry is on the final selected inventory, so verify_design checks it and projects nothing:
- `inventoryPassageInheritance` stays at its 55 rows;
- `inventoryPassageSupersessions` goes from 4 (D2's, now folded) to 21.

## After selection

Once D3 is selected, the next inventory successor must do four things:
- carry all rows by value;
- project D3's 45 overrides into `inventoryPassageInheritance`, which grows from 55 to 100 rows in verify_design's canonical order, as D1's 39 did at inventory122;
- fold each of D3's 17 supersessions into its row's one inheritance entry (law VD1 item 3): `before` stays the raw text and `after` becomes D3's, as D2's four were folded at inventory123;
- extend its projection helper to read both forms from D3's record.

If another inventory is selected before D3, `build_d3.py` rebuilds D3 on it with no edit, because it finds rows by path. That rebuild needs a new review, because the pins change.

## How the rows were found

1. Each v134 row's effective description was taken from the lock: the raw text, or the inheritance entry's `after`. Each row was also matched to the lock commit at which that text last changed. That is the inventory successor that wrote it, D1 (text written against 8240856) or D2 (text written against 96dd114).
2. 121 rows name a file that changed after that point within 8240856..3d2d5b5. 8240856 is D1's basis, and D1's review covered earlier changes. Every one of the 121 was judged against the file at 3d2d5b5, together with:
   - one further row, `recovery_route.rs`, found by scanning all effective texts for time-bound wording ("until X…", "before X11", "vacuous", "Library only", "joins it with", later unit names);
   - every row that an inventory README or review since D1 left for "the next description-only successor". These come from X3d-2, X5a, X6a, X7a, X6b, X6c, X9-1, X8b, X3d-3, X9-2 and X9-5, and from X4B-c's and X7b's review requests.
3. A second, independent pass checked every drafted claim against the code (functions, counts, units by `git log -S`, law items, and "only" or "never" claims). Its corrections are in the text.

Rows marked "Pre-D1" were already stale by omissions that D1's sweep missed. They were found because F5 or F6 touched their files.

## Rows (product main 3d2d5b5)

The exact before and after text is in `evidence/descriptions.json` and in `successor.json`. Every new description was written against the committed code at 3d2d5b5. Sentences that are still true are kept word for word. Only false text is replaced, and clauses are added for what the file now does.

| v134 | File | Form | What was stale |
|---|---|---|---|
| 12 | `apps/cli/tests/doctor_tests.rs` | override | "refuse a features table on the crates of that path" was false since X9-1. The pin refuses a features table only on apps/cli and reporting. On host, security and storage it admits only crash-matrix and scenario-fixtures (law X10 r4 item 5). |
| 108 | `crates/host/src/crash_matrix_support.rs` | override | "the synthetic run candidate ... joins it with X9-5" was superseded: the candidate is storage's, forwarded. It omitted X9-5's finalize_commit and store_gc runners, the run-candidate file and the fixed delivery phase. "Nothing here returns an authority type" ignored the forwarded driver entries. |
| 111 | `crates/host/src/doctor_ingress.rs` | supersession (D1) | Omitted X5a's three replay-join details and their fact_admission remedies. |
| 116 | `crates/host/src/fact_admission.rs` | override | The planned M3 sentence is kept. It omitted the M2 replay join the file holds (X5a). |
| 117 | `crates/host/src/fact_admission_tests.rs` | override | "(vacuous until X7a)" was false: the pin requires exactly one caller, in finalization.rs. |
| 118 | `crates/host/src/finalization.rs` | override | The planned text routed exhaustion "to lifecycle rollover" and used outcomes.rs for the analysis projection; neither is this file. It now describes X7a's coordinator, X6b's requested binding and X7b's disclosure. |
| 119 | `crates/host/src/finalization_tests.rs` | override | It said "Check X7a" only. It omitted X7b's disclosure tests and SessionEnd pin, and X6b's requested-binding checks. |
| 128 | `crates/host/src/maintenance.rs` | override | The planned sentence is kept. It omitted the file's only content, store-gc's settlement sweep step (X6c), and its crash-matrix caller. |
| 143 | `crates/host/tests/admission_tests.rs` | supersession (D1) | The census list stopped at X3d-1: it was missing the X3d-2, X5a, X7a and X8b rows. It omitted X3d-2's adapter source pin. B0 to B8 (X8c) are in this file. |
| 144 | `crates/host/tests/commit_matrix_tests.rs` | override | Omitted X9-6's x9_6_matrix run set and the r16 release-order verdict condition. |
| 147 | `crates/host/tests/fixtures/crash-matrix/required-runs.v1.json` | override | "X9-5's rows only" was false: X9-6 appended four delivery-point kill rows, for 98. |
| 318 | `crates/platform/src/clock.rs` | override | Omitted the scripted wall reading under the crash-matrix feature (X9-1). |
| 319 | `crates/platform/src/crash_barrier.rs` | override | Omitted the scripted wall clock (OPENSIP_X9_CLOCK, scripted_wall) and its harness errors (X9-1). |
| 320 | `crates/platform/src/crash_barrier/driver.rs` | override | "a cleared environment holding only ..." was false: the child also gets OPENSIP_X9_CLOCK (X9-1). |
| 321 | `crates/platform/src/crash_barrier/self_tests.rs` | override | Omitted X9-1's clock self-tests and F7's bracketed OS-clock check. |
| 373 | `crates/security/src/crash_matrix_sites.rs` | override | Omitted gate 5 (X3d-3), the scenario modules (X8b), the storage and host matrix targets' guards (X9-2, X9-5) and the widened no-sleep pin (X9-3, X9-5). |
| 374 | `crates/security/src/crash_matrix_support.rs` | override | "never an authority type" was false since X9-2's three driver entries. |
| 375 | `crates/security/src/crash_matrix_support/post_state.rs` | override | "every regular file" no longer held: X9-3 records unreadable files instead. It omitted undumpable databases and the ordering of rows without rowid (X9-3), and blobText and the object set by shape (X9-2). The kept capture sentence was narrowed to what the code claims. |
| 376 | `crates/security/src/crash_matrix_support/run_record.rs` | override | Omitted X9-3's timingGuard member. |
| 378 | `crates/security/src/custody/commit_session.rs` | override | Omitted X3d-2's project_id and store_root hooks, X3d-3's core evaluator closure and X7b's SessionEnd accessors. Its list of points omitted X9-1's x3b.append scopes. |
| 379 | `crates/security/src/custody/commit_session_tests.rs` | override | Omitted X3d-2's hook test and X7b's eight disclosure tests. |
| 381 | `crates/security/src/custody/first_registration.rs` | override | Pre-D1. Omitted what X2d, X2e and X4a added: the Lease step and busy row, the Exact and Started footprints with the Handoff step, and recheck_registered_owners. |
| 389 | `crates/security/src/custody/installation_doctor_tests.rs` | override | Pre-D1. Omitted the X10 and X3a-1 cases: the chain finding; the account, omitted-ACL, budget and not-initialized rows; and the current-store finding. |
| 396 | `crates/security/src/custody/installation_read_fixture.rs` | supersession (D1) | Omitted F5's churned retry, X9-1's joint predicate and shared producers, and X8b's new_in, admitted_writer, publish_trust_fenced and InstallationAt::operation. |
| 398 | `crates/security/src/custody/installation_root.rs` | override | Pre-D1. The plan-era sentence is kept. It omitted the creator's law 460 parent observation, and the shared ancestor walk and judgment that the parent preparation, the write gate and the project chain use. |
| 401 | `crates/security/src/custody/installation_session.rs` | supersession (D2) | D2's text stays. It omitted X6b's read_recovery_members, the member reads that recovery's admission takes with no fence. |
| 402 | `crates/security/src/custody/installation_session_tests.rs` | override | Pre-D1. Omitted X3a-1's five cases, and one older failed-capture case. |
| 404 | `crates/security/src/custody/namespace_lease.rs` | supersession (D1) | Omitted what X6 builds from it: the lent primitives, shared_reader (X6b), and exclusive and try_lock (X6c). |
| 408 | `crates/security/src/custody/operation_handoff.rs` | supersession (D1) | Omitted open_store_root and store_root_in (X3d-2, X6b), core_evaluator_closure (X3d-3) and the x2.fence.end scope. "the carrier location's production constructor" was no longer unique. |
| 409 | `crates/security/src/custody/operation_handoff_tests.rs` | supersession (D1) | "the carrier location's only production constructor" was false since X6b's CarrierLocation::recovered. |
| 412 | `crates/security/src/custody/ordinary_writer_tests.rs` | override | Pre-D1. Omitted X3a-1's two store-endpoint cases. |
| 417 | `crates/security/src/custody/read_premise.rs` | supersession (D2) | D2's text (X1b's refresh) stays word for word. It omitted X3d-3's core_evaluator_closure. |
| 435 | `crates/security/src/journal_store.rs` | supersession (D1) | Omitted X6b's recovery re-exports and the public CarrierObservation and CarrierKind, and X9-1's carrier fixtures. |
| 438 | `crates/security/src/journal_store/carrier_append.rs` | supersession (D1) | "Crash and fault hooks exist only under cfg(test)" was false since X9-1's barrier points. |
| 440 | `crates/security/src/journal_store/carrier_dispatch.rs` | override | Omitted X6a's inherited_present. |
| 441 | `crates/security/src/journal_store/carrier_floor.rs` | supersession (D1) | "is CarrierLocation's only production constructor" was false since X6b's recovered. It omitted the recovery_capture and recovery_location children. |
| 443 | `crates/security/src/journal_store/carrier_operation.rs` | override | "A cfg(test) helper" was false since X9-1. "the production constructor" was no longer unique. It omitted later re-exports (X4a, X3d-1). |
| 445 | `crates/security/src/journal_store/carrier_rollover.rs` | override | "Crash and fault hooks ... exist only under cfg(test)" was false since X9-1. |
| 466 | `crates/security/src/store_custody.rs` | override | Omitted X6b's admit_existing_store_directory. "under the caller's namespace writer lease" did not cover recovery's reads. |
| 468 | `crates/security/src/trust/accepted_store_fixture.rs` | supersession (D1) | "declared solely under cfg(test)" was false (X9-1). Since X4B-c, reachable requests are X4B's producer's records, not the module's own construction. |
| 469 | `crates/security/src/trust/accepted_store_fixture_tests.rs` | supersession (D1) | The pin requires the joint predicate (X9-1). It omitted X4B-c's three tests. |
| 488 | `crates/security/src/trust/core_inventory.rs` | override | Omitted X3d-3's core evaluator closure (EC1), derived in bind. |
| 493 | `crates/security/src/trust/current_trust_admission_tests.rs` | override | Pre-D1. Omitted X4T-a3's five recorded-chain tests. |
| 500 | `crates/security/src/trust/floor_publication.rs` | override | Omitted X9-1's shared fenced publisher publish_store_fenced, and X4B-b's ordered confirmations. |
| 501 | `crates/security/src/trust/floor_publication_tests.rs` | override | Pre-D1. Omitted X4T-a3's rotated-store test. |
| 504 | `crates/security/src/trust/initial_core.rs` | supersession (D1) | Omitted X3d-3's evaluator_closure. |
| 505 | `crates/security/src/trust/initial_core_tests.rs` | override | "Compiled only for tests" was false (X9-1). It omitted X3d-3's evaluator_closure_preimages. |
| 507 | `crates/security/src/trust/initial_platform_tests.rs` | override | "Compiled only for tests" was false (X9-1). Its receipt producers serve both support surfaces. |
| 554 | `crates/security/src/trust/trust_bootstrap.rs` | supersession (D1) | Omitted X4B-c's build_over_p0. |
| 715 | `crates/storage/src/commit_tests.rs` | override | "without a session" and the corpus Run's replay were false since X3d-3. It omitted the first real commit, the closure tests, and the recover and settlement_sweep children. |
| 716 | `crates/storage/src/crash_matrix_support.rs` | override | Omitted run_candidate and its re-exports. "nothing here returns an authority type" ignored the forwarded driver entries. |
| 717 | `crates/storage/src/crash_matrix_support/run_candidate.rs` | override | Omitted X9-3's distinct variant, and the by-path includes from host's admission_tests.rs (X8c) and commit_matrix_tests.rs (X9-5). |
| 723 | `crates/storage/src/ledger_store/project_commit.rs` | override | "blob digests must equal the published objects" was out of date: the typed objects' H digests also count (X3d-2). "Only tests construct a location" and "crash points only under cfg(test)" were false. It omitted X3d-2's helpers. |
| 725 | `crates/storage/src/ledger_store/project_commit_tests.rs` | override | Omitted X9-1's census child module. |
| 726 | `crates/storage/src/ledger_store/project_ledger.rs` | supersession (D1) | "Only tests construct a location." was false since X3d-2. It omitted the recovery_read and sweep_settle children. |
| 729 | `crates/storage/src/ledger_store/recovery_material.rs` | supersession (D1) | "returning the inventory's blob digests" was out of date: it also returns the typed object identities (X3d-2). |
| 738 | `crates/storage/src/recover_tests.rs` | override | "storage cannot build security's RecoveryAdmission" was false since X9-2's support surface. It omitted X3d-3's fixture. |
| 747 | `crates/storage/src/sweep_tests.rs` | override | Same for SweepLease (X9-2), and X3d-3's fixture. |
| 748 | `crates/storage/tests/commit_tests.rs` | override | The planned clause "API compile-fail fixtures require the selected harness" named nothing in the file. The file is storage's crash-matrix target (X9-2 to X9-6). |
| 749 | `crates/storage/tests/fixtures/crash-matrix/required-runs.v1.json` | override | "Later X9 units append their rows" has happened (381 rows). It did not name the script forms or the unit member. |
| 863 | `tools/check_crash_matrix.py` | override | "limits L1 to L10" was false (L11). check is the two-target gate. It omitted the clock, the timing guard, check-unit, the unit member and coverage. |
| 916 | `tools/tests/test_check_crash_matrix.py` | override | Omitted the tests added by later units (X9-1, X9-2, X9-3, X9-4, X9-6). |

## Checked and kept

These 60 rows were judged true at 3d2d5b5 (122 judged, 62 changed).

**Lead decisions on rows the first pass drafted as stale:**
- **`crates/host/src/recovery_route.rs`** keeps "Library only: no CLI command calls it before X11." Law X11 r1 item 4 rules that this wording "stays true".
- **`crates/storage/src/commit.rs`** keeps its planned text. That text already describes the facade: bind, publish verified objects, the SEAL and ledger barriers, and PublishedCommit. X3d-2 and X3d-3 judged it true.
- **`crates/storage/src/ledger_store.rs`** keeps its text. `next_commit_sequence` and `settle_admitted_attempt` are private ledger transactions used only by the guarded commit and authorized maintenance paths, which is what the text says.
- **`crates/storage/src/recovery.rs`** keeps its text. Its parsers, counter and `join_ledger` are the inert reconciliation pieces the planned sentence describes, and the read path's files have their own rows.
- **`crates/security/src/custody/installation_parent.rs`** keeps its text. `recheck_names_in` is the preparation's own chain and name recheck, lent on a borrowed scope, and the cfg widening is not material.

**Kinds of change that leave a row true:**
- **Generic manifest and lib rows.** The changes are L1's `license` field, X9-1's and X8b's test-only feature tables and dev-dependencies, the matrix `[[test]]` targets, module declarations and re-exports, and the crash-matrix compile guards. Rows: the eleven `Cargo.toml`, the three `package.json` (two inherited), `README.md`, `Cargo.lock`, `design-lock.json`, the two dependency policies, and the `lib.rs`, `custody.rs` and `trust.rs` rows of evaluator, host, security and storage.
- **Files changed only by F5's or F6's churn retry.** None of these texts describes the harness: `first_registration_tests.rs`, `git_tracking_tests.rs`, `installation_admission_tests.rs`, `installation_parent_tests.rs`, `installation_publication_tests.rs`, `installation_read_tests.rs`, `installation_routing_tests.rs`, `namespace_lease_tests.rs`, `operation_live_tests.rs`, `project_admission_tests.rs`, `project_chain_tests.rs`, `store_endpoint_tests.rs`, `installation_observation_tests.rs` and `native_read_session.rs`.
- **X9-1 barrier points and scopes, and cfg or visibility widening.** These rows' texts neither list the file's points nor claim "only cfg(test)": `carrier_start.rs`, `installation_admission.rs` (its `FenceLock` only names the unlock), `installation_publication.rs`, `initial_installation.rs`, `recovery_admission.rs`, `settlement_sweep.rs`, `current_trust_admission.rs`, `core_authentication.rs`, `initial_platform.rs`, `ordinary_targets.rs`, `root_payload.rs`, `recovery_read.rs` and `availability.rs` (X6b's `state_text`).
- **Small changes inside a still-true text:**
  - `crash_matrix_census.rs` (X9-3: one record literal);
  - `tools/verify_design.py` and `tools/tests/test_design_binding.py` (VD1's request judged both true).

## X1b

X1b deferred a refresh of `read_premise.rs` so that it mentions the Write receipt (`stale-descriptions-x1b/`). D2 made that refresh. At 3d2d5b5 every sentence of D2's text is still true, including the Write receipt's lendings and the single wired CLI path, `opensip doctor`. D3 supersedes D2's link only to add X3d-3's `core_evaluator_closure`. D2's text stays word for word. X1b is closed.

## Found but not changed (product code comments)

D3 changes no product byte. These stale doc comments are left for a code follow-up:
- `carrier_floor.rs:9-10, 115-116` and `carrier_operation.rs:52-54` say there is no other production constructor (X6b's `recovered`). `operation_handoff_tests.rs:890` has the same claim in a test name.
- `fact_admission.rs:17`: "nothing calls it before X7a".
- `first_registration.rs:24-26`: "X2e is a later unit".
- `accepted_store_fixture.rs:1-13`: "no product producer" and "compiled only under cfg(test)".
- `driver.rs:3-6`: the child environment, which is missing `OPENSIP_X9_CLOCK`.
- `security/src/crash_matrix_support.rs:7-12` and `storage/src/crash_matrix_support.rs:12-13`: "never an authority type".
- `post_state.rs:4-9`, `commit_matrix_tests.rs:1-31, 58`, `storage/tests/commit_tests.rs:1-2, 22`, and `recover_tests.rs:2-4` / `sweep_tests.rs:1-3`.
- `project_commit.rs:422-424`, `project_ledger.rs:128` and `store_custody.rs:4-5`.
- `read_premise.rs:14-19`: the Write receipt's "only lending".
- `commit_session.rs:1225, 1239, 1250` and `commit_session_tests.rs:508` cite X7 r5 item 6. X7 r6 item 6 records the accessors.
- Security `lib.rs:1` and storage `lib.rs:1` say "no ... commit authority" and "groundwork".
- `journal_store.rs:3043`: a fixture comment is above the wrong block.

## Evidence

- **`evidence/descriptions.json`** holds each row's path, its exact current effective text (`before`) and its new text (`after`).
- **`evidence/build_d3.py`** rebuilds `successor.json` and `description-batch-d3-subject.json` deterministically from the lock-selected inventory and the lock's contract successors. It chooses the form per row, and it refuses on any of these:
  - more than one inheritance entry;
  - a `before` that is not the row's current text;
  - an override of a superseded row;
  - an ambiguous root;
  - an empty, unchanged or multi-line `after`;
  - a duplicate path.
- **`evidence/verify_scratch.py`** runs the checkout's real verify_design with a synthetic review and assent held in memory (SCRATCH-D3/ paths). Given a checkout whose lock does not bind D3, it appends the binding in memory, as D1's and D2's scripts did. Given the lead's worktree, whose lock already binds D3 with the two SCRATCH-D3 placeholders, it checks that entry against this tree. It asserts:
  - the lock passes;
  - the selected inventory and the 55 inheritance rows equal those of the same lock without D3;
  - supersessions grow by exactly D3's count;
  - every entry's parent is v134;
  - every `before` is the row's current text.
