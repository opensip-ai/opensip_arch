# M2 exit plan

2026-09-30. Claude Opus 5.5, implementation lead. Planning record, not law and not code. It follows [CREATOR-PLAN.md](CREATOR-PLAN.md) line 29: "The M2 exit … follows and is planned separately." Product baseline: `d4239a5`, with 458c complete and inventory v80 selected. 461a (law 461 r3) is under review and is not in that baseline.

## What M2 exit means

The build plan's milestone table (`docs/v2/architecture/implementation-boundaries-and-build-plan.md` line 886) defines M2 as follows:

- **Deliverable:** "pure replay plus live security guards, storage facade and selected carrier recovery join".
- **Owners:** "Evaluator replay; security commit_authority; storage commit/ledger/blob/recovery; host fact_admission/finalization".
- **Completion:** "Opaque API refusal tests and actual crash/lock/revocation matrix pass; synthetic fixtures remain labelled, not compiler qualification".

The detailed obligations are in the same document:

- **Publication sequence and lock discipline:** lines 153–209.
- **Private recovery record:** lines 230–419.
- **Witness-aware publication and read-only recovery:** lines 420–523.
- **The ordered failure matrix F00–F53:** lines 524–590.
- **Required API and fault-injection checks:** lines 591–613. That section names the test owners: `crates/host/tests/admission_tests.rs` for public-boundary scenarios and `crates/storage/tests/commit_tests.rs` for the real carrier crash matrix.
- **Read-only recovery and the settlement sweep:** `commit-recovery-readonly.v3.md` §§1–4.

The approach retrospective (`implementation-approach-retrospective-2026-09-22.md` line 9) restates M2 completion in the same terms.

The planning carry-ins to this plan are:

- **Project-root custody law:** required before any project admission (law 461 r3 item 9, lead decision 2026-09-30).
- **Writers that are not creators:** they have no durable write gate "until the ordinary platform owner exists (M2 exit)" (law 468 r5 item 2).
- **CLI enablement** (464 item 7). This includes:
  - the `RetentionDisclosure` backup-status field deferred by 468 item 7;
  - the doctor human label deferred by 458c r6 item 10.
- **Lineage budget:** one capture plus its full recheck costs about 3.4k of the 131,072-edge cap, so long lineage chains are bounded (458c-b2 follow-up).
- **Stale descriptions:** five stale inventory descriptions, taken by 461b.

## Product state at d4239a5, by M2 owner file

| Owner (build plan line 886 / gate routing lines 1011–1031) | Present? | What exists |
|---|---|---|
| `crates/evaluator/src/replay.rs` | yes, 335 lines | Independent replay of the fixed evaluator3 profile. Pure, with no host join. |
| `crates/security/src/commit_authority.rs` | yes, 268 lines | A private final-admission primitive, "not a CommitSession constructor". Custody, grants, generation, guards and replay evidence are all caller-supplied. |
| `crates/storage/src/ledger_store.rs` | yes, 2370 lines | Existing-carrier mechanisms under supplied path custody. No creation, migration or receipt constructor. |
| `crates/storage/src/blob_store.rs` | yes, 383 lines | Immutable-blob mechanism under a supplied directory. No custody and no commitment. |
| `crates/storage/src/recovery.rs` | yes, 504 lines | Inert recovery candidates and exact ledger joins over supplied same-snapshot observations. |
| `crates/storage/src/availability.rs` | yes, 248 lines | Inert current-evidence availability. |
| `crates/security/src/journal_store.rs` | yes, 3010 lines | Journal record shape and canonical body. "Neither a durable append, an authenticated journal prefix nor authority." |
| `crates/lifecycle/src/leases.rs` | yes | Lease composition over supplied handles; no authenticated namespace registry. |
| `crates/security/src/revocation.rs` | yes, 438 lines | Revocation records (463c embedded revocation). |
| `crates/storage/src/commit.rs` | **missing** | The storage commit facade. |
| `crates/lifecycle/src/journal_store.rs` | **missing** | Durable journal append and witness. |
| `crates/storage/src/index_store.rs` | **missing** | Disposable index (an M4 owner; listed under DR-G19). |
| `crates/security/src/grants.rs` | **missing** | Grants (DR-G09). |
| `crates/host/src/fact_admission.rs` | **missing** | Replay to admission join. |
| `crates/host/src/finalization.rs` | **missing** | Finalization and the not-sealed rule (DR-G27). |
| `crates/host/src/execution.rs`, `configuration.rs` | **missing** | Execution grants (DR-G09) and configuration (DR-G24). |
| `crates/host/tests/admission_tests.rs`, `crates/storage/tests/commit_tests.rs` | **missing** | The two M2 test owners. |
| Compile-fail harness | partial | Ad hoc rustdoc `compile_fail` doctests in `replay.rs`, `capabilities.rs`, `work_ledger.rs` and `installation_observation.rs`. No suite. |

Also in place, and not M2-exit owners: the complete creator path (459–468), the write gate, the charged read session, and the doctor report assembler (458c-c). All are library code; no CLI command reaches them (464 item 7).

## Units, in dependency order

Sizes: S is about one review round of a single file; M is several files with one inventory successor; L is a law plus two or three code units; XL is a law plus four or more units and a harness.

| Unit | Scope | Depends on | Law? | Size | Status / notes |
|---|---|---|---|---|---|
| 461a / 461b | Omitted ACL is unreadable at the choke point; refresh stale descriptions | 458c | 461 r3 accepted | S + S | In review / in draft |
| X1 | **Ordinary platform owner.** An `InitialPlatform`-equivalent receipt for writers that are not creators, so every writer (including commit) can enter the 468 gate. Shape after 458c-a: the same producers, no creator intent. | 461a | yes (new) | M | LAW ACCEPTED X1 r1; X1a INTEGRATED (inventory81); X1b (read_premise description) pending |
| X2 | **Project-root custody.** How a project root and its operational directories on H's filesystem are judged when their ACL is omitted. Then project admission and registration (`project-registry.v2` entry), and project leases (468 "Not claimed"). | 461a, X1 | yes (new; 461 item 9) | L | LAW ACCEPTED X2 r5; X2a INTEGRATED (inventory84); X2b-X2e pending |
| X3a | **Store admission under the write gate.** Open the selected store S through `DurableInstallation`: store-instance, marker, lineage endpoint, generation. The writer side of 458c's read session. | X1 | yes (new) | M | LAW ACCEPTED X3a r5; X3a-1 INTEGRATED (inventory83); X3a-2 (read-side switch, description fixes) pending |
| X3b | **Durable journal append and witness.** `crates/lifecycle/src/journal_store.rs`: PENDING to SEAL to COMMITTED witness over `security::journal_store` bodies, under S7 lock levels 3 and 4 (build plan lines 153–209). | X3a | yes (new) | L | Failure cases F06–F11 and F19. |
| X3c | **Evidence ledger transaction and blob publication.** Object temp write, file barrier, digest publication, directory barrier, then ledger receipt and association (lines 83–152 and 210–229). | X3a | yes (with X3b) | L | Failure cases F02–F05 and F11–F15. Reuses `blob_store` and `ledger_store`. |
| X3d | **`CommitSession` facade.** `crates/storage/src/commit.rs`, joining `commit_authority`. Covers the atomic admission and latch bit (F38–F41), duplicate ExecutionId routing (F34), and carrier capacity (F32). | X3b, X3c, X4 | yes (with X3b/c) | L | This is the storage facade of the M2 deliverable. |
| X4T-0 | **Signed accepted-store fixture generator (test only).** A real signed root, catalog and revocation; consistent admissions, history, events, clock and time evidence; roles in chosen states; a retained-phase capsule. It uses only the existing producers and binders. Added by X4T r4. | X3a-1 | INTEGRATED (inventory87) |
| X4T | **Native current-trust admission.** An authenticated reader of the trust current record, its records, root, revocation, policy, grants and time, rejecting floor rollback, all charged under the fence. It is X4's first timed read and its observer's reread. Added by X4 r2 (RF-1). | X1, X3a | LAW r1 PROPOSED (trust-admission-x4t); units X4T-a read-only admission, X4T-b floor publication, X4T-c contract successor adding CONTINUE-INDEX-NOT-TRUSTED and CONTINUE-COMPONENT-NOT-TRUSTED (lead decision) |
| X4B | **Trust bootstrap acceptance.** Accept the core's embedded bootstrap payload as a fresh installation's first trusted state. A creator-only installation is Unbootstrapped and never admitted (X4T r1). Not needed for the synthetic M2 exit tests. | X4T | NEW (X4T r1); before X11 |
| X4 | **Live security guards.** Grants (`crates/security/src/grants.rs`, `host/src/execution.rs`), live revocation and stale-guard checks at the handoff, and the observer latch and freshness rules (F18, F19, F26). | X1 | yes (new) | L | DR-G09. Grants are a design area the creator laws never touched. |
| X5 | **Pure replay join.** `crates/host/src/fact_admission.rs` hands evaluator `replay` evidence to `commit_authority` (F01; "an identity-valid but replay-invalid candidate never publishes authority", line 612). | X3d | yes (small) | M | Replay itself exists. |
| X12 | **Configuration and policy-pack admission (DR-G24).** `host/configuration.rs` and `evaluator/policy.rs`: admission refuses a pack that isn't bundled or declarative. Split out of X5 by X5 r1. | X1 | NEW; law to draft |
| X6 | **Carrier recovery join.** Read-only recovery (`commit-recovery-readonly.v3.md` steps 0–4) over `storage::recovery`, plus F20–F25, F27–F29, F33, F35–F37, F43–F49 and F52. The authorized settlement sweep (§4, F53) runs under store-gc. | X3d | yes (new) | L | The "selected carrier recovery join". Carrier-format migration (F46–F51) may stay outside M2 if no format-1/2 carrier exists for this product; the X6 law must state that explicitly. |
| X7 | **Finalization and outcomes.** `crates/host/src/finalization.rs`: no silent promotion of a preview result to a sealed Run (DR-G27). Covers committed-delivery-failed (F16, F17) and the D9 rows for durability-undetermined (F12, F40). | X3d, X5 | yes (small) | M | |
| X8 | **Opaque API refusal suite.** `crates/host/tests/admission_tests.rs`. Raw DTOs, a boolean `verified`, forged receipts, a cloned or reused session, a private constructor and a serialized previous session all fail to compile. Behavioral rejection of altered inputs at the handoff (lines 597–604). | X3d, X4, X5 | harness decision only | M | Tooling matrix line 1071 leaves trybuild versus isolated compile-fail fixtures to a trial. See "Choices". |
| X9 | **Crash, lock and revocation matrix.** `crates/storage/tests/commit_tests.rs` executes F00–F53 against the real carrier in fresh processes, with deterministic crash barriers before and after every durability step and no sleeps (lines 605–610, 1072). It also covers S7 contention (F30) and live revocation. | X3d, X4, X6, X7 | yes (harness law) | XL | Gates M2 completion. Needs a law fixing the injection mechanism (a child process killed at named barrier points) and the recorded evidence shape. |
| X10 | **CLI enablement, read-only first.** Wire `doctor` and the read-only surfaces (458c) to commands. Add the human doctor label. | 458c, 461a | no (464 item 7) | S | LAW ACCEPTED X10 r3 (Codex); X10a and X10b INTEGRATED: `opensip doctor` enabled (inventory82). Follow-ups: harden the source pin past the first test module; doctor_report.rs description |
| X11 | **CLI enablement, creator commands.** Wire `opensip`, `analyze`, `fit` and `audit` through the creator, the 468 gate and the `RetentionDisclosure` backup-status field (a contract successor for 468 item 7). | X10, X1, X2 | contract successor | M | These are analysis commands. Until M3 they can only create or admit the installation and then end on the existing not-implemented refusal; the X11 law must say whether that partial behavior ships before M3. |

**Recommended order:**

1. 461a and 461b (in flight).
2. X10 (small; every prerequisite exists).
3. X1.
4. X3a.
5. X4 and X3b/X3c in parallel.
6. X3d.
7. X5, X6 and X7.
8. X8.
9. X9 (M2 exit).

X3a's law (r1, 2026-09-30) decided that the store endpoint is admitted without a namespace, and that the full store binding needs a registered project (owner §8). So X2 now gates the real commit path of X3b and X3c, though not their scratch-installation tests. Run X2 alongside X3a and before X3b/X3c are integrated. X11 still runs in parallel with X3.

## Choices left open by the design

Each of the following has a technical basis for a recommendation, so under the owner's direction of 2026-09-30 the lead decides it in the unit's law and Grok reviews it:

- **Project-root evidence (X2).** Recommendation: a receipt-bound premise of its own, scoped to the project root and its operational directories, under the existing qualified profile member. The reason: a project root on H's qualified filesystem has the same mode-bits-govern semantics the 458 premise already authenticates. The alternative, separate evidence, adds a new trust path.
- **Compile-fail harness (X8).** Recommendation: isolated compile-fail fixtures built by the pinned toolchain inside the workspace's existing test lanes, extending the rustdoc `compile_fail` doctests already in the product. The reason: no new dependency outside the pinned closure, offline builds, and the reason for failure checked against rustc's error code. trybuild adds a dependency and normalizes rustc output. The tooling matrix (line 1071) asks only that misuse "fail for the intended reason".
- **Crash injection (X9).** Recommendation: named barrier points compiled only into a test feature, with a child process that the harness kills at a chosen point (line 1072: "deterministic synchronization and crash barriers against actual storage/processes").
- **Carrier-format migration in M2 (X6).** Recommendation: out of M2 unless a format-1 or format-2 carrier exists for this product. The X6 law states it.

**Owner actions, not decisions.** Two things only the owner can supply:

- **Signing keys** for a real embedded release and for a measured macOS 27 profile row. This host is BASELINE-ATTESTED under 469. Without them, CLI end-to-end runs on real machines stay at F0 or refuse at `/`.
- **M2 completion does not need them.** The matrix and suites run on scratch homes with synthetic signed profiles, labelled as synthetic per line 886.

No item in this plan is blocked on an owner policy choice.

## Release gates

The gate routing table is in `implementation-boundaries-and-build-plan.md` lines 997–1036; the gate definitions are in `08-decision-and-readiness-register.md` lines 352–372 and the rows around them. All 32 gates are unqualified, and executing them belongs to M6 (line 895). This plan prepares the six gates routed to M2:

| Gate | Routed milestone | Definition (register) | Prepared by |
|---|---|---|---|
| DR-G07 EXACT-BYTES | M2 | Verified bytes equal executed bytes | 463 (core identity), 461a, X3c |
| DR-G09 PERMISSIONS | M2 | Requested, granted and denied outcomes are truthful | X4 |
| DR-G11 STORAGE-CUSTODY | M2 | Authoritative closure needs verified durable storage | X3a–X3d, X6, X9 |
| DR-G19 STATE-CLASS-AUTHORITY | M2 | Every durable byte has one class, owner and writer | X3a–X3d, X6. `index_store` is M4 |
| DR-G24 PREVIEW-ANALYZE-WELL-FORMED-ADMISSION | M2 | Admission refuses a non-bundled or non-declarative pack | X12 (host configuration and policy-pack admission; moved out of X5 by X5 r1) |
| DR-G27 PREVIEW-ANALYZE-NOT-SEALED-RUN | M2 | No silent promotion to a sealed Run | X7 |

The other 26 gates are routed to M1 (G03, G15, G16, G31), M3 (G10, G13, G14, G21, G23, G25, G29), M4 (G17, G26), M5 (G08, G12, G18, G20, G28, G32) and M6 (G01, G02, G04, G05, G06, G22, G30). This plan does not touch them.

## Deferred tooling follow-up (lead decision, 2026-09-30)

**VD1: superseding override of an inherited description.** `verify_design` refuses every form of replacing a description whose meaning is already inherited by projection:
- a direct override on the final inventory;
- an override on the parent;
- an inventory successor that rewrites the row.

X1b, which refreshes `read_premise.rs` to mention the Write receipt, is therefore deferred. The proposed text and the probe are in `stale-descriptions-x1b/`.

VD1 is a reviewed change to `tools/verify_design.py`. It would accept a direct override on the final inventory whose `before` equals the inherited projection's `after`, recorded as superseding that projected row. It is batched with any other stale inherited rows, and lands before the X9 exit.

Rejected: changing the trust-anchor tool now for one sentence.

## Pending cross-law corrections (tracked 2026-09-30)

- **X2 (APPLIED to r4 before review):** record X3b r2's two steps inside the single fence hold: the floor step between R0/R2 and X2d's lease, and the carrier start inside X2e before the fence is released.
- **X4T (APPLIED to r1 before review):** item 7 must not say the carrier floor records the trust epoch. It compares against SC-TRUST's own floors (X3b r2 item 7).
- **F3 (flake): FIXED at product 8452ab9.** the native census tests in `trust/native_census.rs` (for example `native_profile_census_later_file_fence_and_missing_bucket_changes_refuse`, around line 888) fail intermittently at a setup `capture(...).unwrap()` under the parallel workspace. Isolate them as F1 did.
- **D1 (description batch):** a description-only contract successor for stale plain rows. It covers `installation_read.rs` (X2b-1 walks from `/`), `project_chain.rs`, `accepted_store_fixture_tests.rs` (named by X4T-a's tests), `doctor_report.rs` (now emitted), and X3a-1's rows (`carrier_floor.rs` (start and end now live in its child module), `installation_admission.rs`, `ordinary_writer.rs`, `installation_doctor.rs`, `native_current.rs`, the two `installation_termination.rs`), and X3c-2's `project_ledger.rs` and `recovery_material.rs`. Inherited rows wait for VD1.
- **X3b r7 (needed by X7b):** define opening a non-initial grant generation's carrier (generation g+1, after `TERMINAL`). X3b r6 item 3a covers only INIT. X7r1 item 6 depends on it.
- **X2 r7 (needed by X2b-2):** item 1's system Git config custody rule refuses every repository on a stock Mac: `/` is on the sealed system volume off H's volume with no ACL, `/etc` is a symlink, and the Homebrew prefix is user-owned and admin-writable. Planned lead decision: system sources are refusal-only evidence. They are read by path (following links, 64 KiB cap, closed parse) with no custody judgment, and an unreadable source is `vcs-unsupported`. Global and repository sources keep custody. X2b-2's review waits for r7.
- **F4, a possible flake (2026-10-01):** `installation_observation::tests::every_capture_phase_refuses_actual_mutations` failed once with `Capture … Changed` while four worktrees ran their suites at the same time. It didn't recur. Watch it; if it recurs, isolate it the way F3 did.
- **F5, a candidate flake (2026-10-02, found while fixing F4):** `installation_routing::tests::a_lost_race_enters_the_gate_and_admits_the_winner` failed once with `Custody { subject: "ancestor-acl" }` during concurrent suites. The likely cause is the same shared-ancestor churn, but its error has no component index, so F4's classifier can't cover it. Watch for it.
- **X9 cross-law gaps (2026-10-02, from the X9 r1 draft):** these are amended in one batch once X9 is accepted.
  - **G1:** the X3d r6 item 12, X6 r2 item 11 and X7 r3 item 10 composition tests depend on X9-1, since another crate's `cfg(test)` can't be seen.
  - **G2:** in X3c r7 item 11, X3b r10 item 11 and X4T r9 items 12–13, "only under `cfg(test)`" becomes "absent from every non-test build".
  - **G3:** X6a/b place the read-path hold points needed by F49.
  - **G4:** X4a places the observer-gate and checkpoint points.
  - **G5:** whether the sweep's X1 admission refuses when a closure subject is revoked. X1 or X6 decides this; until then the F18, F19 and F38 ladders stop at R2.
  - **G6:** X9-0 and X9-1 must land early (X9-0 before X3d-1).
- **F5 widened (2026-10-02):** `namespace_lease::the_target_holds_no_project_lock_for_the_floor_step` failed once while the x2e worktree's tests ran concurrently, and passed alone. It and `a_lost_race_enters_the_gate_and_admits_the_winner` are candidates for the same treatment as F4: classify churn above the scratch parent. Also add the `initial_core.rs` row (law 463 r3–r8, now r9) to the D1 batch.
- **X4T-a3, a reader successor needed before X4B-b (2026-10-03, from X4B-a judgment call 12):** X4T-a's reader treats the head root as both the accepted root and the signing root. A multi-root chain written by X4B-a therefore refuses on `FirstIdentity`. Fix: take the chain's first root as accepted and the head as signing. First check X4T r9's text to decide whether this is a code fix or needs a law amendment.
- **X4 F-1, observer reread expiry (2026-10-03, from X4a):** X4T r9 item 6 says observer rereads evaluate expiry at the handoff time, advanced by elapsed monotonic time. The accepted X4T-a reread evaluates no time, and X4 r7 does not assign this to X4a. Close it with either an X4T-a successor or an X4 amendment; decide which after the X4a review.
- **X9 clock dependence (2026-10-03, from X9-1):** since X4a, each fenced first read publishes a trust floor only when the wall clock has passed the stored evaluation floor. As a result, the `x4t.floor-publication` point counts and the trust-store bytes vary between lawful runs (34 vs 39 creates were observed). This conflicts with X9 item 5 (fixed kill set) and item 7 (repetition agreement). Before X9-2 and X9-6, X9 r2 needs either a scripted clock in the matrix child or a ruling that the trust store is compared per publisher run.
- **F5 widened again (2026-10-03):** X3d-1's `a_staging_io_error_rolls_back_then_appends_rev_and_cln` failed once in the X2c registration setup (operation_handoff_tests.rs:146) during a concurrent run, then passed 3 of 3 alone. Same suspected cause. Also add to the D1 batch the stale `trust_bootstrap.rs`, `live_observation.rs` and `operation_live_tests.rs` rows (from X4B-b) and the `commit_authority.rs` row (from X3d-1).
- **X3d-2 ordering and follow-ups (2026-10-03).**
  - **Lead decision:** X3d-2 integrates before X8b and X9-1. The first end-to-end composition test with a real session is X8c B0–B4. A record-only note goes into X3d r7.
  - **Known limits for X8c and X3c:**
    - (a) No corpus Run binds to a fresh scenario ProjectId, so X8c's B0 must produce its Run from the scenario project.
    - (b) Re-committing a Run already committed in the same store and namespace is refused at staging, because X3c-2 always stages a fresh availability record. That needs an X3c successor.
- **D2 and verify_design strictness (2026-10-03, from VD1).**
  - **D2:** a contract successor that supersedes the four inherited rows (`read_premise.rs`, `installation_session.rs`, `store_lineage.rs`, `initial_installation.rs`) through VD1's `passageSupersessions`. Bind it only after VD1 is in the product.
  - **Finding:** verify_design at main silently ignores unknown record fields. A later tooling unit should consider refusing unknown fields.
- **X7 follow-ups (2026-10-04, from X7a).**
  - X7's next revision is record-only. It covers three things:
    - item 3: the rollover already runs inside `finish`;
    - item 4: a security `SessionEnd` accessor, needed to disclose end-step and rollover outcomes (recommended for X7b);
    - the integration-test gap.
  - Session-level finalization tests need a `ProjectOperation` from a host test. That needs X9-1 or X8b, so those tests land with X8c, X9-5 or an X7a-2.
- **G5 decided in X6c (2026-10-04, pending review).** A revoked closure subject does not refuse the sweep. X1 item 4 gives no trust admission and X6 item 7 adds none. For F18, F19 and F38: R3 writes `refused`, and R4 is terminal-not-committed. Record this in X9's next record-only revision.
- **X11 (accepted r1, 2026-10-04, lead decision):** no creator command goes live in M2. The `opensip`, `analyze`, `fit` and `audit` refusals stay byte-identical. M2 carries only X11a (tests-only pins). The backup-status field, the analysis step order and the single-RequestId rule move to an M3 successor law.
- **X8 record note owed (2026-10-04, from the X3d r7 review):** X8 r3's unit list says X8b "lands before X3d-2", which the X3d-2-first ordering overtook. Fold a record-only X8 r4 into the X8b round.
- **RESOLVED (X3d-3, 2026-10-02): commit closure binding (2026-10-02, found by X9-2).** X3d step 1 requires `run.evaluator_closure() == session.core_closure()`. These are a `kind:evaluator` closure and a `kind:core` closure, so their ids can never be equal, and `prepare_commit` refuses every real ReplayedRun. X3d-2's tests masked this by building the session from the Run's closure. The fix is X3d r8 plus an X3d-3 code unit. This blocks X8c, X9-2..X9-6 and any production commit.
- **X8 B2 wording owed (2026-10-02).** In X8's next record note, the B2 row compares against the session's core evaluator closure (`CommitSession::core_evaluator_closure()`; X3d r8; EC1), and the owner column reads "X3d-2, binding X3d-3". B6 is unchanged.
- **M2 known limit: permanently refused crash states (2026-10-02, found by X9-2).** A crash at any of the following points leaves the project refused permanently until a repair/resume writer exists (M3):
  - inside first registration (RESERVED written, ACTIVE not): identity-recovery-required;
  - between creating a namespace, ledger, object directory or trust dependency and sampling it private: Custody, Incomplete or HostIo;
  - inside the ledger's WAL before the schema commit: LEDGER.CORRUPT.

  The owning laws (X2 item 8, X3c item 10) already fail closed here. X9 r8 records these outcomes and adds no product code.
- **X6c crash point fix (2026-10-02):** the sweep's `try_lock` took its lock outside any `x2.lease.*` scope. X9-2 carries the scope placement, which compiles to nothing without the feature.
- **X8 record notes owed after X8c (2026-10-02).** X8's next record-only revision should cover:
  - the B2 wording and owner;
  - the corpus path (host `replay-fixtures.json`);
  - the REV that B1, B2 and B4 append;
  - B7's drift and B6's gate, as shown at the public boundary;
  - B0's candidate route (`#[path]` include plus the schema-registry shim).
