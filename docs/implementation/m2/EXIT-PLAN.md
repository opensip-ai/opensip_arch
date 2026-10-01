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
| X2 | **Project-root custody.** How a project root and its operational directories on H's filesystem are judged when their ACL is omitted. Then project admission and registration (`project-registry.v2` entry), and project leases (468 "Not claimed"). | 461a, X1 | yes (new; 461 item 9) | L | Recommendation: a receipt-bound omission premise scoped to the project root, under the same qualified profile member (458 item 3). See "Choices" below. |
| X3a | **Store admission under the write gate.** Open the selected store S through `DurableInstallation`: store-instance, marker, lineage endpoint, generation. The writer side of 458c's read session. | X1 | yes (new) | M | Also settles the lineage-budget follow-up: charge the node chain once per session, not once per capture. |
| X3b | **Durable journal append and witness.** `crates/lifecycle/src/journal_store.rs`: PENDING to SEAL to COMMITTED witness over `security::journal_store` bodies, under S7 lock levels 3 and 4 (build plan lines 153–209). | X3a | yes (new) | L | Failure cases F06–F11 and F19. |
| X3c | **Evidence ledger transaction and blob publication.** Object temp write, file barrier, digest publication, directory barrier, then ledger receipt and association (lines 83–152 and 210–229). | X3a | yes (with X3b) | L | Failure cases F02–F05 and F11–F15. Reuses `blob_store` and `ledger_store`. |
| X3d | **`CommitSession` facade.** `crates/storage/src/commit.rs`, joining `commit_authority`. Covers the atomic admission and latch bit (F38–F41), duplicate ExecutionId routing (F34), and carrier capacity (F32). | X3b, X3c, X4 | yes (with X3b/c) | L | This is the storage facade of the M2 deliverable. |
| X4T | **Native current-trust admission.** An authenticated reader of the trust current record, its records, root, revocation, policy, grants and time, rejecting floor rollback, all charged under the fence. It is X4's first timed read and its observer's reread. Added by X4 r2 (RF-1). | X1, X3a | LAW r1 PROPOSED (trust-admission-x4t); units X4T-a read-only admission, X4T-b floor publication, X4T-c contract successor adding CONTINUE-INDEX-NOT-TRUSTED and CONTINUE-COMPONENT-NOT-TRUSTED (lead decision) |
| X4B | **Trust bootstrap acceptance.** Accept the core's embedded bootstrap payload as a fresh installation's first trusted state. A creator-only installation is Unbootstrapped and never admitted (X4T r1). Not needed for the synthetic M2 exit tests. | X4T | NEW (X4T r1); before X11 |
| X4 | **Live security guards.** Grants (`crates/security/src/grants.rs`, `host/src/execution.rs`), live revocation and stale-guard checks at the handoff, and the observer latch and freshness rules (F18, F19, F26). | X1 | yes (new) | L | DR-G09. Grants are a design area the creator laws never touched. |
| X5 | **Pure replay join.** `crates/host/src/fact_admission.rs` hands evaluator `replay` evidence to `commit_authority` (F01; "an identity-valid but replay-invalid candidate never publishes authority", line 612). | X3d | yes (small) | M | Replay itself exists. |
| X6 | **Carrier recovery join.** Read-only recovery (`commit-recovery-readonly.v3.md` steps 0–4) over `storage::recovery`, plus F20–F25, F27–F29, F33, F35–F37, F43–F49 and F52. The authorized settlement sweep (§4, F53) runs under store-gc. | X3d | yes (new) | L | The "selected carrier recovery join". Carrier-format migration (F46–F51) may stay outside M2 if no format-1/2 carrier exists for this product; the X6 law must state that explicitly. |
| X7 | **Finalization and outcomes.** `crates/host/src/finalization.rs`: no silent promotion of a preview result to a sealed Run (DR-G27). Covers committed-delivery-failed (F16, F17) and the D9 rows for durability-undetermined (F12, F40). | X3d, X5 | yes (small) | M | |
| X8 | **Opaque API refusal suite.** `crates/host/tests/admission_tests.rs`. Raw DTOs, a boolean `verified`, forged receipts, a cloned or reused session, a private constructor and a serialized previous session all fail to compile. Behavioral rejection of altered inputs at the handoff (lines 597–604). | X3d, X4, X5 | harness decision only | M | Tooling matrix line 1071 leaves trybuild versus isolated compile-fail fixtures to a trial. See "Choices". |
| X9 | **Crash, lock and revocation matrix.** `crates/storage/tests/commit_tests.rs` executes F00–F53 against the real carrier in fresh processes, with deterministic crash barriers before and after every durability step and no sleeps (lines 605–610, 1072). It also covers S7 contention (F30) and live revocation. | X3d, X4, X6, X7 | yes (harness law) | XL | Gates M2 completion. Needs a law fixing the injection mechanism (a child process killed at named barrier points) and the recorded evidence shape. |
| X10 | **CLI enablement, read-only first.** Wire `doctor` and the read-only surfaces (458c) to commands. Add the human doctor label. | 458c, 461a | no (464 item 7) | S | Every invocation in a development build ends at `CORE.NO_EMBEDDED_RELEASE` (463 F0). Real end-to-end use needs a signed release. |
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
| DR-G24 PREVIEW-ANALYZE-WELL-FORMED-ADMISSION | M2 | Admission refuses a non-bundled or non-declarative pack | X5 (host configuration admission) |
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
