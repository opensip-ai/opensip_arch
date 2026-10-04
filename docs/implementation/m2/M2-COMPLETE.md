# M2 completion record — COMPLETE (2026-10-04)

2026-10-04. Drafted for Claude Opus 5.5, implementation lead, by a lead-dispatched drafting agent during the overnight autonomous run. This is a record. It is not law, code or a contract successor, and it changes no accepted contract, gate, threshold or register row. Drafted against arch HEAD `28e46fec5` and product main `3e64266`.

**Status: COMPLETE (2026-10-04).** The rerun was accepted (`reviews/grok-crash-matrix-x96-r2`, arch `50047b7ed`). M2 completes when Grok's independent rerun of the crash matrix on product commit C (`3d2d5b5`) is accepted. That rerun is review `reviews/grok-crash-matrix-x96-r2/`, assigned at arch `af703414d`. Until then, this record claims nothing beyond the lead's own evidence and the accepted reviews it cites.

When the lead finalizes:
- every `RERUN` token below (a name in double square brackets) is filled from that review's `review.json` and `REVIEW.md`;
- the status line becomes **COMPLETE (date)**;
- §9's checklist is worked through.

If the rerun's verdict is REQUIRED-FINDINGS, M2 is not complete. The status stays PENDING-RERUN, and the findings go into §5.

## Finalization tokens

| Token | Filled from (`grok-crash-matrix-x96-r2`) | Expected value |
|---|---|---|
| (filled) `[[RERUN:verdict]]` | `review.json` `"verdict"` | `ACCEPT` |
| `[[RERUN:requiredFindings]]` | `"requiredFindings"` | `[]` |
| `[[RERUN:matrixPass-reviewer-pair]]` | `"matrixPass"`, the reviewer's two sets | `true` |
| `[[RERUN:matrixPass-mixed-pair]]` | `"matrixPass"`, the pair (lead-1, reviewer set 1) | `true` |
| `[[RERUN:normalized-equal]]` | `"normalizedAgreement"`: equal runs | every compared run |
| `[[RERUN:normalized-differing]]` | `"normalizedAgreement"`: differing runs | `0` |
| `[[RERUN:evidenceRecordSha256]]` | `"evidenceRecordSha256"` | `97f8367e46c07fddc627bb0661896b228e39348460af70cf29f1d535ed57da69` |
| `[[RERUN:release-absence]]` | the reviewer's release-absence record (`REVIEW.md`) | `opensip` 6315264 bytes, `b32604fe…`; both feature builds refused |
| `[[RERUN:date]]` | the date of Grok's review | — |
| `[[RERUN:arch-record]]` | the arch commit that copies the review in | — |

## 1. The claim

### What the build plan asks

The M2 row of the build plan (`docs/v2/architecture/implementation-boundaries-and-build-plan.md:886`, "BP" below) reads:
- **Milestone:** "M2 — admission and durable publication".
- **Prerequisites and deliverable:** "M1; pure replay plus live security guards, storage facade and selected carrier recovery join".
- **Main files and boundaries:** "Evaluator replay; security commit_authority; storage commit/ledger/blob/recovery; host fact_admission/finalization".
- **Demonstration of completion:** "Opaque API refusal tests and actual crash/lock/revocation matrix pass; synthetic fixtures remain labelled, not compiler qualification".

The detailed checks are BP:591–613 ("Required API and fault-injection checks"). [EXIT-PLAN.md](EXIT-PLAN.md) broke M2 into units X1 to X12.

### What this record claims, once the rerun is accepted

1. **Opaque API refusal tests pass.** These are the X8 suite: compile-fail fixtures and the behavioural cases B0–B8 (§2.1).
2. **The actual crash/lock/revocation matrix passes.** The real two-target `check` gave `matrixPass: true` on the clean commit C, and an independent rerun on C agrees (§2.2).
3. **Synthetic fixtures stay labelled.** Every matrix run carries `synthetic`, and no record claims qualification (§2.3).
4. **The deliverable exists.** Its four parts exist as reviewed, integrated library code at main `3e64266` (§2.4).
5. **The exit plan is accounted for.** Every EXIT-PLAN unit is integrated, or carried with a recorded owner (§3, §5). There are four exceptions: three units that accepted laws declare were never built (X3a-2, X4b and X4T-c), and the open gap X4 F-1. None of the four lies on BP:886's completion criteria. Each now has a lead decision (2026-10-04), recorded in §5 rows 13–16. X3a-2 is a post-M2 unit due before M3-C1. X4b is deferred to M3-B3's `grants.rs` and M5-EX, under O7. X4T-c follows F8b. X4 F-1 is a disclosed known defect: its fix, unit X4-F1, is written and lands before any M3 analysis ships. M3-PLAN r6 schedules all four.

### What this record does not claim

- **Product qualification.** `productQualification: false` in the matrix `check.json` and in `verify_design`'s output.
- **Compiler qualification.** BP:886 says so. The compile-fail suite is pinned to rustc 1.95.0 on `aarch64-apple-darwin` (X8 r5, "Not claimed").
- **Any QUALIFIED gate.** All 32 release gates (DR-G01–G32) stay unqualified. The six gates routed to M2 are prepared only (§2.5), and gate execution belongs to M6 (BP:895). D-372 condition 4 still stands: "Harness implementation/execution and real supported-platform qualification remain required; none is claimed QUALIFIED or DEMONSTRATED here" (`docs/v2/architecture/08-decision-and-readiness-register.md`, condition table, row 4). The implementation authorization record does not authorize "Treating any gate as QUALIFIED … without its gate's actual execution" (`docs/implementation/IMPLEMENTATION-AUTHORIZATION.md`, "What is not authorized").
- **Real-machine use.**
  - This macOS 27 host is BASELINE-ATTESTED under law 469. Every test uses scratch homes with synthetic signed profiles, and real sessions refuse at `/` (X3a r5, "Not claimed").
  - A development build has no embedded release, so it refuses at InitialCore F0 (CREATOR-PLAN, 463).
  - Real use needs the owner's signing keys, for a real embedded release and for a measured macOS 27 profile row (EXIT-PLAN, "Owner actions"; L7).
- **A CLI product.** `opensip doctor` is the only enabled command. `opensip`, `analyze`, `fit` and `audit` keep their byte-identical refusals (X11 r1; X11a).
- **Other platforms.** Only macOS 27 on APFS on this host is covered (L8). AL2023 joins the supported population by owner decision D11 (2026-10-03). That needs a DR-126 successor and a G13 lane (`m3/analysis-quality/PLAN.md` §11, D11).
- **M3 work.** Discovery, the snapshot and Plan, providers, analysis and the durable host pipeline are all M3.

## 2. Evidence for each completion criterion

### 2.1 Opaque API refusal tests (X8)

**The law.** X8 r5 is accepted (`refusal-suite-x8/PROPOSAL-r5.md`, sha256 `ba6915b9…`, `reviews/grok-refusal-suite-x8-r5`).
- **The harness (item 1, a lead decision).** It settles BP:1071's trial: isolated compile-fail fixtures, compiled by the pinned rustc inside `cargo test -p opensip-host --test admission_tests`, with each failure's reason checked against the rustc error code. trybuild is a forbidden substitute.
- **Behavioural cases (item 5).** Each case drives the public facade on its own `ScenarioHome`, through `scenario-fixtures`, a test-only feature enabled from dev-dependencies only.

**Integration.**

| Part | Unit | Product commit | Inventory | Review |
|---|---|---|---|---|
| Driver, annotation parser, toolchain check, census and self-test; groups I, K and L, including the 17 ported doctests | X8a | `c2352ae` | v117 | `grok-refusal-suite-x8a-r1` |
| Owner rows (groups A–H, per X8 item 3) | X4a, X3d-1, X3d-2, X5a, X7a | `a34dc6b`, `5f4395d`, `adc9081`, `54e6166`, `f097c5b` | (each unit's own) | each unit's review (§3.2) |
| The `scenario-fixtures` feature, both `scenario` modules and group J | X8b | `4faf729` | v129 | `grok-scenario-fixtures-x8b-r1` |
| Behavioural cases B0–B8 | X8c | `cdd4589` | none | `grok-refusal-cases-x8c-r1` |

The commits that add fixture files are, from `git log -- crates/host/tests/refusal/cases`: `c2352ae`, `a34dc6b`, `5f4395d`, `adc9081`, `54e6166`, `f097c5b` and `4faf729`.

**At main `3e64266`:**
- `crates/host/tests/refusal/cases/` holds 108 fixture files: security 58, storage 21, host 10, platform 10 and evaluator 9. `refusal/selftest/` holds 8 more. These are file counts, not a count of the driver's reported cases.
- `admission_tests.rs` holds B0–B8, named `synthetic_b0_…` to `synthetic_b8_…`.

**What the suite covers.**
- **BP:597–604.** Raw DTOs, a boolean `verified`, structural-only validation and a serialized previous session cannot enter the facade. An admitted input (B1), inventory (B2), namespace (B3), execution (B4) or generation (B5) altered at the handoff yields no acknowledged authority. Live revocation is covered by B6 and B7, and stale guards by B3 and B5.
- **F01 (BP:609).** This is B8: a replay-invalid candidate never yields a `ReplayedRun`.
- **What it does not cover.** X8 item 6: it "covers no F-case alone and qualifies no gate".

**Lanes.**
- X8c's own lanes: workspace 1726 passed twice, crash-matrix lane 1611, `scenario-fixtures` lane 1139 (`reviews/grok-refusal-cases-x8c-r1/REQUEST.md:131-133`).
- The latest lanes are in §6.

### 2.2 The actual crash/lock/revocation matrix (X9)

**The law.** X9 r16 is accepted (`crash-matrix-x9/PROPOSAL-r16.md`, sha256 `f08efe95deba681f2940a043c80c91b4faae4e4c804ca5865c024e0e083c0a85`, arch `ab193f89a`, `reviews/grok-crash-matrix-x9-r16`; r15 was accepted by Codex). The units X9-0 to X9-6 are listed in §3.2.

**The run set.**

| Target | Runs | Made up of |
|---|---|---|
| storage (`crates/storage/tests/commit_tests.rs`) | 381 | X9-2 231 + X9-3 57 + X9-4 47 + X9-6 46 |
| host (`crates/host/tests/commit_matrix_tests.rs`) | 98 | X9-5 94 + X9-6 4 |

**The lead's evidence on clean commit C.**
- **Location:** `crash-matrix-x9/evidence/3d2d5b5a5e5cabd1768b02e29eb3c0928264fb4f/`, committed at arch `5c703071d`. It holds 490 files, 23 MB, in r16's item 7 layout.
- **`hashes.txt`:** 66611 bytes, sha256 `97f8367e46c07fddc627bb0661896b228e39348460af70cf29f1d535ed57da69`. It pins 489 evidence files plus both `required-runs.v1.json` files at C. This record's drafter re-hashed all 489 files, and all match.
- **`check.json`:** 56813 bytes, sha256 `cee0aaa1d6cde6715bb5e57b3a1f5650679aa022376fda93899cb931e9b299ab`. It is the real two-target `check`:

| Member | Value |
|---|---|
| `commit` | `3d2d5b5a5e5cabd1768b02e29eb3c0928264fb4f` |
| `matrixPass` / `passed` | `true` / `true` |
| `runs` | 479 |
| `killSet` / `killedPoints` | 383 / 383 |
| `killedOutsideKillSet` | `[]` |
| `repetitionsAgree` | `true` |
| `unionCensusPoints` | 321 |
| `limits` | L1 … L11 |
| `productQualification` | `false` |
| storage | census 259 points (trace 1379 records, `e9add21e…`); kill set 321; killed 305; runs 381 |
| host | census 218 points (trace 1195 records, `93d0922a…`); kill set 271; killed 81; runs 98 |

**The runs.**
- All 479 lead-1 run records have verdict `PASS`.
- Every one is labelled `synthetic` and `scripted-clock`. 401 are also `process-death` (320 storage, 81 host), 117 `mutation` (40, 77) and 19 `injected` (12, 7).
- Each record states its host and build: macOS 27.0 (26A428), arm64, APFS, fixture `synthetic-signed-v2`, profile standing `BASELINE-ATTESTED`, rustc 1.95.0, features `crash-matrix`, and `worktreeClean: true`.
- Lead set durations: storage 1959 s and 1921 s, host 811 s and 801 s (`OVERNIGHT-2026-10-03.md`).

**Release absence.** `release-absence.json` (sha256 `538a10c4…`) records:
- the release `opensip` binary: 6315264 bytes, sha256 `b32604fe8c83343a93e7e38f023abc330afda2fa0f7cb255c842ab2b52aa5e49`;
- no scanned string found: `OPENSIP_X9_` and 25 scope names;
- `featureBuildRefused: true`.

The same binary bytes appear in X9-2's to X9-5's records.

**Independent runs before C.** The reviewers of X9-2 to X9-5 each ran two sets of their own:
- **X9-2:** Grok's two sets, 231 PASS each, agree with the lead on every `normalizedSha256` and child trace (`grok-crash-matrix-x92-r1/review.json`).
- **X9-3, X9-4 and X9-5:** the reviewer sets agree with both lead sets on every `normalizedSha256` and child trace (their `review.json` scopes).
- **X9-6 r1 (ACCEPT-UNIT):** Grok reproduced the census, the transcription, the coverage and release absence. Grok deferred its two full sets to a single rerun on C (`grok-crash-matrix-x96-r1/REVIEW.md`, "Rerun timing").

**Grok's rerun on C (the third execution, X9 r16 item 7). PENDING.**
- **Verdict:** `ACCEPT`. Required findings: `none`.
- **`matrixPass`:** reviewer pair `true`; mixed pair (lead-1, reviewer set 1) `true (the lead pair is also true)`.
- **`normalizedSha256` agreement with the lead:** `479 of 479, in every pairing of Grok's two sets with the lead's two sets and with each other` equal, `0` differing.
- **The evidence record's `hashes.txt`, as Grok hashed it:** ``97f8367e46c07fddc627bb0661896b228e39348460af70cf29f1d535ed57da69``.
- **The reviewer's release absence:** ``opensip` 6315264 bytes, `b32604fe…`, with no barrier strings found; both feature builds refused`.
- **Review date and record:** `2026-10-04`, arch ``50047b7ed``.

**Result:** M2's crash/lock/revocation matrix gate is MET when `ACCEPT` is ACCEPT.

### 2.3 "Synthetic fixtures remain labelled, not compiler qualification"

- **The matrix.** Every run is labelled `synthetic` (§2.2), and `check.json` carries `productQualification: false` and the limits L1–L11. X9's forbidden substitutes bar dropping `synthetic`, `injected` or `mutation` from a run's labels, and reporting a limit row as executed.
- **X8.** The behavioural cases are named `synthetic_…`, as BP:886's label requires (X8 item 5). X8's "Not claimed" excludes compiler qualification, process isolation, native scheduling, and every toolchain other than rustc 1.95.0.
- **The design lock.** `verify_design` at `3e64266` reports `productQualification: false` (§6).

### 2.4 The deliverable (BP:886, second and third columns)

| Part | BP owner | At main `3e64266` | Units |
|---|---|---|---|
| Pure replay | evaluator replay | `crates/evaluator/src/replay.rs` (335 lines; present before the exit plan), joined to commit admission by `crates/host/src/fact_admission.rs` (180 lines) | X5a |
| Live security guards | security commit_authority | `crates/security/src/commit_authority.rs` (`FinalGate`, `AdmissionPermit`); the operation guard, freshness monitor, observer and checkpoint; native current-trust admission and trust bootstrap | X4T-a/a2/a3/b, X4B-a/b/c, X4a, X3d-1 |
| Storage facade | storage commit/ledger/blob | `crates/storage/src/commit.rs` (808 lines: `prepare_commit`, `publish`); the project ledger, object publication and the journal carrier with its witness and rollover | X3a-1, X3b-1a…X3b-4, X3c-1/2, X3d-0…X3d-3 |
| Selected carrier recovery join | storage recovery | `crates/storage/src/recover.rs` (482 lines); recovery capture and admission; the authorized settlement sweep (`store-gc`) | X6a, X6b, X6c |
| Host admission and finalization | host fact_admission/finalization | `fact_admission.rs`; `crates/host/src/finalization.rs` (571 lines) | X5a, X7a, X7b |

**Prerequisites built for these parts:**
- X1: the ordinary platform owner;
- X2: project-root custody, admission, registration and the operation handoff;
- X12: policy-pack admission, DR-G24;
- X10 and X11: CLI scope.

**Owner files still absent at main.** Each is absent by an accepted decision or carried as open:
- `crates/lifecycle/src/journal_store.rs` is a different owner: lifecycle transition records, M5 (X3b r10). The grant journal's read side is `security/src/journal_store*`.
- `crates/host/src/execution.rs` stays with the M5 commands (X4 r7 item 1).
- `crates/security/src/grants.rs` belongs to X4b, which was never built (§3.3, §5).
- `crates/storage/src/index_store.rs` is an M4 owner (EXIT-PLAN, DR-G19).

### 2.5 Release gates routed to M2: prepared, not qualified

| Gate | Prepared by (integrated) | Not prepared in M2 |
|---|---|---|
| DR-G07 EXACT-BYTES | 463 (core identity), 461a `d1b5eda`, X3c-1/2 `859089a`/`920941b` | — |
| DR-G09 PERMISSIONS | X4a `a34dc6b` (the operation guard, S6) | X4b's S10 repository-execution predicate (`grants.rs`) is unbuilt. The spawn composition is M5 (X4 r7 item 1). |
| DR-G11 STORAGE-CUSTODY | X3a-1 … X3d-3, X6a–c, X9-0 … X9-6 | — |
| DR-G19 STATE-CLASS-AUTHORITY | X3a-1 … X3d-3, X6a–c | `index_store` (M4) |
| DR-G24 PREVIEW-ANALYZE-WELL-FORMED-ADMISSION | X12-0 `b880e83`, X12a `b642c45`, X12b `6dd7363` | The release registry has no pack rows in M2 (X12a). X12c → M3-I1; X12d → M3-C (C4). |
| DR-G27 PREVIEW-ANALYZE-NOT-SEALED-RUN | X7a `f097c5b`, X7b `099de03` | — |

The other 26 gates are routed to M1 and M3–M6 (EXIT-PLAN, "Release gates"). None is touched here.

## 3. Units

### 3.1 Laws

| Law | Accepted revision | Accepting review | Accepted at arch | Earlier rounds |
|---|---|---|---|---|
| 461 (omitted ACL unreadable) | r3 | `grok-acl-unreadable461-r3` | `82ed44598` (2026-09-30) | Grok r1 (findings), r2 (accept) |
| X1 (ordinary platform owner) | r1 | `grok-ordinary-platform-x1-r1` | `34153a802` (2026-09-30) | — |
| X2 (project-root custody, admission, registration) | r8 | `grok-project-root-x2-r8` | `bf3007f0f` (2026-10-01) | Codex r1–r2 (findings); Grok r3–r4 (findings), r5 and r6 (accept, r6 in `grok-x5r2-x6r2-x2r6`); r7 superseded by r8 |
| X3a (store admission) | r5 | `grok-store-admission-x3a-r5` | `349c575a8` (2026-09-30) | Grok r1–r4 |
| X3b (journal append, witness, rollover) | r10 | `grok-journal-x3b-r10-commit-session-x3d-r6` | `21a7eaba7` (2026-10-01) | Grok r1–r9 |
| X3c (ledger and blob publication) | r7 | `grok-ledger-blob-x3c-r7` | `925c9c3ca` (2026-10-01) | Grok r1–r6 |
| X3d (CommitSession facade) | r8, with EC1 | `grok-evaluator-closure-x3d-r8` | `8293ab89e` (2026-10-02) | Grok r1–r7 (r7 record-only) |
| X4 (live guards) | r7 | `grok-live-guards-x4-r7` | `22c969a0f` (2026-10-01) | Codex r1 (findings); Grok r2–r6 |
| X4T (native current-trust admission) | r11 | `grok-trust-admission-x4t-r11` | `846071458` (2026-10-01) | Grok r1–r10 |
| X4B (trust bootstrap), with 463 r9 | r5 | `grok-initial-core-463-r9-trust-bootstrap-x4b-r5` | `3eb0a4fe4` (2026-10-01) | Grok r1–r4 |
| X5 (replay join) | r3 | `grok-replay-join-x5-r3` | `3e02f71b2` (2026-10-01) | Grok r1 (findings), r2 (accept) |
| X6 (read-only recovery and sweep) | r4 (record-only) | `grok-crash-matrix-x9-r4-x6-r4` | `5733fc9fd` (2026-10-02) | Grok r1–r3 |
| X7 (finalization) | r6 (record-only) | `grok-record-x3d-r7-x7-r6-x9-r3` | `6e16b026d` (2026-10-01) | Grok r1–r5 |
| X8 (opaque API refusal suite) | r5 (record-only) | `grok-refusal-suite-x8-r5` | `e1bca5583` (2026-10-02) | Grok r1–r4 |
| X9 (crash, lock and revocation matrix) | r16 | `grok-crash-matrix-x9-r16` | `ab193f89a` (2026-10-03) | Grok r1–r14; Codex r15 (`codex-crash-matrix-x9-r15`) |
| X10 (read-only CLI) | r4 | `grok-read-cli-x10-r4` | `69583023b` (2026-10-01) | Codex r1–r3 (r3 accepted) |
| X11 (creator commands, M2 scope) | r1 | `grok-cli-enablement-x11-r1` | `8c4aad02e` (2026-10-01) | — |
| X12 (configuration and policy-pack admission) | r3 | `grok-policy-admission-x12-r3` | `0f69f15fc` (2026-10-01) | Grok r1–r2 |
| VD1 (verify_design supersession) | r1, with tooling | `grok-verify-design-vd1-r1` | `eafe9c273` (2026-10-01) | — |

**Dating.** The "accepted at" dates are git commit dates. Several law headers carry later dates (§8).

### 3.2 Code and contract units, in integration order

Sources:
- **Product commit:** `git log` on product main.
- **Inventory:** the selected inventory, read from `design-lock.json` at each commit.
- **Review:** the review directory that the design lock binds, or for units without an inventory, the unit's own review directory.

Every code review below is Grok's (w2:p1), except where another reviewer is named.

| # | Unit | What it delivered | Law at integration | Product commit | Inventory | Review |
|---|---|---|---|---|---|---|
| 1 | 461a | An omitted ACL is unreadable at the custody choke point | 461 r3 (review) | `d1b5eda` | none (v80) | `grok-acl-unreadable461a-r2` |
| 2 | 461b | Eight stale descriptions refreshed | 461 r3 | `fdbedf4` | contract successor `stale-descriptions-461b` | `grok-stale-descriptions461b-r1` |
| 3 | X1a | Purpose-sealed platform receipt; ordinary writer admission | X1 r1 (review) | `f7acb6d` | v81 | `grok-ordinary-writer-x1a-r1` |
| 4 | X10a + X10b | `opensip doctor`, the first read-only command; golden successor | X10 r3 (review) | `84a8bfd` | v82; contract successor `read-cli-x10b` | `grok-read-cli-x10a-r1` |
| 5 | X3a-1 | Selected store endpoint admission | X3a r5 (review) | `99f1c35` | v83 | `grok-store-endpoint-x3a1-r2` |
| 6 | X2a | The chain from root to a project root | X2 r5 (review) | `8bfc78a` | v84 | `grok-project-chain-x2a-r2` |
| 7 | X4T-0 | Signed accepted trust store generator (tests only) | X4T r5 (review) | `5b5f04c` | v87 | `grok-signed-store-x4t0-r1` |
| 8 | X3b-1a | Journal floor and carrier creation | X3b r6 (review) | `7e676a9` | v91 | `grok-journal-carrier-x3b1a-r2` |
| 9 | X2b-1 | Project root selection and admission | X2 r5 (review) | `451838d` | v93 | `grok-project-admission-x2b1-r3` |
| 10 | F3 | Test scratch isolation (test only) | — | `8452ab9` | none | `grok-scratch-isolation-f3-r1` |
| 11 | X3c-1 | Project ledger creation; attempt admission | X3c r6 (review) | `859089a` | v94 | `grok-ledger-creation-x3c1-r3` |
| 12 | X4T-a | Current trust admitted read-only | X4T r5 (review r1) | `fc7dce7` | v96 | `grok-current-trust-x4ta-r3` |
| 13 | X3b-1b | Journal start, uncertain-outcome reconciliation, end floor step | X3b r6 | `46b1d60` | v97 | `grok-journal-start-x3b1b-r2` |
| 14 | X2b-2 | Git tracking observation; system sources as refusal-only evidence | X2 r8 | `66bdd05` | v99 | `grok-git-tracking-x2b2-r2` |
| 15 | X3c-2 | Object publication, prepared ledger, staging, durability classification | X3c r7 | `920941b` | v102 | `grok-ledger-blob-x3c2-r2` |
| 16 | X3b-2 | Journal append under `JournalAppendLock`; witness; uncertain-outcome latch | X3b r6 | `9dbefb9` | v101 | `grok-journal-append-x3b2-r1` |
| 17 | X12a | Evaluator-side pack admission (bundled registry, declarativeness) | X12 r3 | `b642c45` | v104 | `grok-policy-pack-x12a-r1` |
| 18 | X12-0 | `CONFIG.INVALID` remedy widened for pack rows | X12 r3 item 7 | `b880e83` | contract successor `config-remedy-x12-0` | `grok-config-remedy-x12-0-r1` |
| 19 | X2c | First registration | X2 r8 | `0206ce8` | v105 | `grok-first-registration-x2c-r1` |
| 20 | X12b | Host-side pack selection admission and routing | X12 r3 | `6dd7363` | v109 | `grok-policy-pack-x12b-r1` |
| 21 | X2d | Namespace admission and S7 leases | X2 r8 | `9d51f33` | v110 | `grok-namespace-lease-x2d-r2` |
| 22 | F4 | Capture churn isolation (test only) | — | `8bd0283` | none | `grok-flake-f4-r1` |
| 23 | X3d-0 | WorkLedger settlement reserve | X3d r6 | `f1b8321` | v112 | `grok-settlement-reserve-x3d0-r1` |
| 24 | X4T-a2 + X4T-b | `accepted.by` by reference; trust floor publication | X4T r9 | `704251e` | v106 | `grok-trust-floor-x4tb-r2` |
| 25 | X3b-4 | Grant-generation rollover | X3b r10 | `97f630a` | v108 | `grok-journal-rollover-x3b4-r4` |
| 26 | X2e + X3b-3 | Operation handoff from fence to lease; floor step, carrier start, end path | X2 r8; X3b r10 | `abf2a48` | v111 | `grok-operation-handoff-x2e-r3` |
| 27 | 463h | Bootstrap catalog and component-manifest envelopes retained in InitialCore | 463 r9 | `19e3e5b` | none | `grok-initial-core-463h-r1` |
| 28 | X9-0 | Barrier mechanism (feature, macros, child protocol, platform points, checker) | X9 r1 | `daa7b01` | v114 | `grok-crash-matrix-x90-r2` |
| 29 | X8a | Compile-fail driver; groups I, K, L | X8 r3 | `c2352ae` | v117 | `grok-refusal-suite-x8a-r1` |
| 30 | X4a | Live guards: monitor, observer, checkpoint, single admission permit | X4 r7 | `a34dc6b` | v116 | `grok-live-guards-x4a-r1` |
| 31 | X4B-a | First trust acceptance from the embedded bootstrap payload | X4B r5 | `0fc8ea2` | v113 | `grok-trust-bootstrap-x4ba-r2` |
| 32 | X4T-a3 | Trust view from the chain's first root; `heads.root` signs | X4T r11 | `d884ed0` | none | `grok-trust-roots-x4ta3-r1` |
| 33 | X3d-1 | `CommitSession` open, seal under the append lock, finish | X3d r6 | `5f4395d` | v119 | `grok-commit-session-x3d1-r1` |
| 34 | X4B-b | Bootstrap wired into the monitor's first read | X4B r5 item 1 | `8240856` | none | `grok-trust-bootstrap-x4bb-r1` |
| 35 | D1 | 39 stale descriptions refreshed | — | `7be09a7` | contract successor `description-batch-d1` | `grok-description-batch-d1-r1` |
| 36 | F5 | Ancestor-walk churn retry (test only) | — | `96ca141` | none | `grok-flake-f5-r1` |
| 37 | X3d-2 | `prepare_commit` and `publish` through the storage facade | X3d r6 | `adc9081` | v122 | `grok-commit-facade-x3d2-r1` |
| 38 | VD1 | `verify_design` `passageSupersessions` | VD1 r1 | `96dd114` | none (tooling) | `grok-verify-design-vd1-r1` |
| 39 | D2 | Four inherited descriptions superseded (X1b's refresh among them) | — (VD1 r1's form) | `933e78b` | contract successor `description-batch-d2` | `grok-description-batch-d2-r1` |
| 40 | X5a | Replay joined to commit admission | X5 r3 | `54e6166` | v123 | `grok-replay-join-x5a-r1` |
| 41 | X6a | Read-only journal carrier capture for recovery | X6 r2 | `81214cb` | v124 | `grok-recovery-capture-x6a-r2` |
| 42 | X7a | Finalize: replay, admit, publish, finish, deliver; every outcome projected | X7 r5 | `f097c5b` | v125 | `grok-finalization-x7a-r1` |
| 43 | X6b | Recovery admission, `recover`, `RecoveredCommit`, host routing | X6 r3 | `f880145` | v126 | `grok-recovery-admission-x6b-r1` |
| 44 | X4B-c | X4T-0's fixture built through X4B's producer | X4B r5 item 9 | `3237afc` | none | `grok-trust-fixture-x4bc-r1` |
| 45 | X6c | Authorized settlement sweep (`store-gc`) | X6 r3 | `bccb6b4` | v127 | `grok-settlement-sweep-x6c-r1` |
| 46 | X11a | Creator commands' M2 refusals pinned (tests only) | X11 r1 | `d64ef7b` | v128 | `grok-cli-pins-x11a-r1` |
| 47 | F6 | Every ancestor-walking security test retried on churn (test only) | — | `5067a27` | none | `grok-flake-f6-r1` |
| 48 | X7b | `SessionEnd` accessors; end-step and rollover disclosure | X7 r5 items 6, 6a | `099de03` | none | `grok-finalization-x7b-r1` |
| 49 | X9-1 | Support surface, barrier points, scripted clock, census | X9 r3 | `a36da7c` | v118 | `grok-crash-matrix-x91-r1` |
| 50 | X8b | `scenario-fixtures` test surface | X8 r4 | `4faf729` | v129 | `grok-scenario-fixtures-x8b-r1` |
| 51 | EC1 | The core release's evaluator closure (identity text overrides) | with X3d r8 | `9d3b84b` | contract successor `core-evaluator-closure-ec1` | `grok-evaluator-closure-x3d-r8` (`ec1/`) |
| 52 | X3d-3 | Run bound to the core evaluator closure; first end-to-end commit | X3d r8 | `a2c5e8b` | v130 | `grok-evaluator-closure-x3d3-r1` |
| 53 | X8c | Behavioural cases B0–B8 | X8 r4 | `cdd4589` | none | `grok-refusal-cases-x8c-r1` |
| 54 | X9-2 | Carrier and object rows, 231 runs | X9 r9 | `b999ae3` | v131 | `grok-crash-matrix-x92-r1` |
| 55 | X9-3 | Commit and recovery rows, 57 | X9 r14 | `eb0d503` | none | `grok-crash-matrix-x93-r1` |
| 56 | X9-5 | Host rows, 94 runs | X9 r15 | `8dcfe37` | v133 | `grok-crash-matrix-x95-r1` |
| 57 | F7 | X9-1 clock self-test independent of the wall-clock date | — | `9c5f145` | none | GROK2 (w6:p1) `grok2-clock-selftest-f7-r2` |
| 58 | X9-4 | Locks and live-revocation rows, 47 runs | X9 r15 | `91cb45a` | none | `grok-crash-matrix-x94-r1` |
| 59 | L1 | Apache-2.0 licence (owner decision D14) | — | `2967905` | v134 | Codex (w3:p1) `codex-licence-l1-r1` |
| 60 | X9-6 = **C** | M2 exit: two-target check and coverage, 50 rows, release-order condition | X9 r16 | `3d2d5b5` | none | `grok-crash-matrix-x96-r1`; rerun `grok-crash-matrix-x96-r2` PENDING |
| 61 | D3 | 45 overrides, 17 supersessions on v134; closes X1b | — | `30c5db1` | contract successor `description-batch-d3` | `grok-description-batch-d3-r1` |
| 62 | F8a | Contracts and identity dependency-policy rows refreshed | — | `3e64266` | none | Codex (w3:p1) `codex-policy-refresh-f8a-r1` |

**Notes on the table.**
- **The law column** gives the revision that the commit message names, or, marked "(review)", the revision that the unit's review request names. It is not today's revision. Each law's accepted revision is in §3.1.
- **Inventory order.** The chain is linear but not numerically monotone, because units were rebuilt in acceptance order: v101 follows v102, v106 follows v112, v116 follows v117, v113 follows v116, and v118 follows v128 (`verify_design`'s `inventorySuccessors`).
- **Commit count.** 62 product commits lie in `d4239a5..3e64266`, and every one appears above.

### 3.3 Units that accepted laws declare, but that are not built

| Unit | Declared by | What it is | Record of deferral |
|---|---|---|---|
| X3a-2 | X3a r5 items 4 and 8 ("The read side adopts it now") | The host provisional readers take the pair, marker and chain from the session's `SelectedStoreEndpoint`, with the extended source pin | **None.** X3a-1's review says "Item 4's host-reader adoption is X3a-2" (`grok-store-endpoint-x3a1-r1/REVIEW.md:7`). At main, `crates/host/src/installation_lineage.rs:68` still re-captures through `capture_descendant`, and the file was last changed at `b230250`. The description half is already true through an inherited override. |
| X4b | X4 r7 item 11 ("No M2 dependency") | `grants.rs` `admit_repo_execution_grant`, the pure S10 admission predicate with its `GRANT.*` refusals | **None.** `crates/security/src/grants.rs` is absent at main. |
| X4T-c | X4T r11 (lead decision on two new codes) | A contract successor adding `CONTINUE-INDEX-NOT-TRUSTED` and `CONTINUE-COMPONENT-NOT-TRUSTED` | **None.** The interim stands: `CONTINUE-CORE-NOT-TRUSTED` with a role-naming subject (X4T item 10). |
| X12c, X12d | X12 r3 ("(M3)") | The DR-131 pack row and bundled bytes; the Run-closure `check_plan_pack` join | By law: M3. Now M3-I1 and M3-C (C4). |

## 4. Known limits carried forward

### 4.1 The matrix limits L1–L11

Each limit's "recorded owner" is verbatim from the `limits` member of both targets' `matrix.json` in the evidence record. The law text is X9 r16 item 10. Where the "When" column says *inference*, it is this record's reading, not a recorded assignment.

| Limit | What is not executed | Recorded owner | When |
|---|---|---|---|
| L1 | Power loss, kernel panic, drive-cache loss. Process death keeps unbarriered page-cache data, so F03 and F05 run the "survived" branch only. | M6 qualification | M6 (BP:1072 "M2/M6") |
| L2 | SQLite's interior commit. The matrix kills at `commit.before` and `.after` and injects `fail-*`, with no VFS shim. | SQLite (no VFS shim) | None: SQLite's own atomicity contract |
| L3 | Native stalls and S6 scheduling bounds: the 10 s freshness stall, a stalled syscall, the residual admission window | S6, M6 | M6 |
| L4 | Whole-file `state.v1` restore, asserted neither refused nor admitted (X4T r9 item 7) | S9.3 or a future anchor outside I | Not scheduled |
| L5 | Store and carrier migration and restore (F35, F47, F48, F50, F51). No migration or restore writer exists, and F46's read side is executed. | the migration law | Not scheduled. *Inference:* storage maintenance is an M5 owner (BP:889). |
| L6 | Orphan collection. No reachability GC exists, and orphans are recorded in `postState`. | a reachability GC law | Not scheduled. *Inference:* M5 (BP:889). |
| L7 | A measured platform profile. This host is BASELINE-ATTESTED, so every run is synthetic. | owner signing keys | An owner action; qualification at M6 |
| L8 | Host coverage: macOS 27 on APFS on this host only | M6 qualification | M6. AL2023 joins the population by owner decision D11, through a DR-126 successor. |
| L9 | Native optional delivery. F17 runs only as an injected failure. | CLI enablement | M3-J, the X11 successor. *Inference:* browser and export renderers arrive at M4 (BP:888). |
| L10 | Journal pruning. F28 runs only over X6a's fixture. | a pruning law | Not scheduled |
| **L11** | **Permanently refused crash states** (below) | M3 (a repair or resume writer) | An M3 carry-in (`m3/M3-PLAN.md:112`). **No M3 unit row names it** (M3-PLAN:156–173). |

**L11 in full** (X9 r8/r9; EXIT-PLAN, "M2 known limit: permanently refused crash states"). Until a repair or resume writer exists, a crash at any of these points leaves the project refused permanently:
- **Inside first registration** (RESERVED written, ACTIVE not): X2 item 8's identity rows (identity-recovery-required).
- **Between creating an owner and sampling it private** (a namespace, ledger, object directory or trust dependency): custody, host I/O, or `CONFIG.CUSTODY_REFUSED` with subject `installation-incomplete` for an X4T dependency that the next publication writes.
- **Inside the ledger's WAL before the schema commit:** `LEDGER.CORRUPT` (X3c item 10).

F00 records each outcome. The owning laws fail closed here, and X9 added no product code for them.

### 4.2 Other limits M2 carries

- **Lineage chain bound.** At most 64 nodes (`MAX_LINEAGE_NODES`, X3a r5 item 3). A longer chain is the budget row. Later owner: "A later compaction or retention law may revisit it". This answers EXIT-PLAN's "Lineage budget" carry-in.
- **Backup classification.** It is constant `UNKNOWN` (law 464; owner decision 2026-09-26), so Time Machine users see "unknown". The `RetentionDisclosure` backup-status field moves to the X11 successor (M3-J1).
- **No pack rows.** The release pack registry is empty in M2 (X12a), so X12c ships the first row (M3-I1).
- **Interim continuation code.** `CONTINUE-CORE-NOT-TRUSTED` with a role subject stands in for two unregistered codes until X4T-c.
- **No signed release.** Development builds refuse at InitialCore F0. There is no measured profile row (L7).
- **Gates.** All 32 release gates are unqualified (§1).

## 5. Open follow-ups: owner and when

Status values:
- **open:** not done, and no owner or date is recorded.
- **owned:** a recorded owner exists.
- **closed:** done, and the source is cited.

| # | Follow-up | Source | Status | Owner | When |
|---|---|---|---|---|---|
| 1 | Grok's X9-6 rerun on C | X9 r16 item 7; `grok-crash-matrix-x96-r2` | owned, in progress | Grok (w2:p1) | Now. M2 completes on its acceptance. |
| 2 | **F8b**, the generator-closure and TypeScript lane-registry re-pin. It covers: the contract generator's drift check and `check_typescript.py`, which still refuse because they pin the `verify_design.py` from before VD1; the L1 follow-up (`license` fields on three tooling manifests); and the rest of EXIT-PLAN's "Stale dependency-policy rows". | `generator-closure-f8b/PROPOSAL.md`; `codex2-generator-closure-f8b-r2` (ACCEPTED); arch `1648ceb7e` | owned | lead; CODEX2 reviews | After Grok's rerun, because it needs the machine: rebuild, equivalence probe, re-pins, then an ACCEPT-DESIGN-UNIT review. Any contract regeneration waits for it, including M3-I1's product units and X4T-c. |
| 3 | **Stale product doc comments** listed by D3: `carrier_floor.rs:9-10, 115-116`, `carrier_operation.rs:52-54`, `operation_handoff_tests.rs:890`, `fact_admission.rs:17`, `first_registration.rs:24-26`, `accepted_store_fixture.rs:1-13`, `driver.rs:3-6`, both `crash_matrix_support.rs` headers, `post_state.rs:4-9`, `commit_matrix_tests.rs:1-31, 58`, `commit_tests.rs:1-2, 22`, `recover_tests.rs:2-4`, `sweep_tests.rs:1-3`, `project_commit.rs:422-424`, `project_ledger.rs:128`, `store_custody.rs:4-5`, `read_premise.rs:14-19`, `commit_session.rs:1225, 1239, 1250`, `commit_session_tests.rs:508`, security and storage `lib.rs:1`, `journal_store.rs:3043` | `description-batch-d3/README.md`, "Found but not changed"; `grok-description-batch-d3-r1/REVIEW.md` item 11 | open | none recorded ("a code follow-up") | None. One comment-only code unit, or each file's next code unit. |
| 4 | **Record-hygiene staged notes.** 11 notes in `staged-notes.patch` (README, chapters 02, 05, 08 (×5), 10 (×2) and 12). The staged condition-5 note must now point to `IMPLEMENTATION-AUTHORIZATION.md`, not read "pending owner record". | `m3/record-hygiene/PROPOSAL.md`, lead decision 2026-10-03 items 2 and 6 | owned | "the next successor that re-pins their files": the next D-372 application-manifest successor, or the next design-lock change that touches the register | Not scheduled. D3 changed `design-lock.json` without re-pinning the register (an `inputs` entry). As proposed, F8b adds one contract-successor row and does not re-pin it either. |
| 5 | **X9 record notes.** The r14 overstatement and the X9-1 clock-window flake are recorded in r16's "Records" section. The flake was fixed by F7 `9c5f145`. | X9 r16, "Records (no rule changes)" | closed | — | — |
| 6 | **G2 restatements.** The literal "`cfg(test)` only" sentences in X3c r7 item 11, X3b r10 item 11 and X4T items 12–13 should read "absent from every non-test build". | X9 r1 "Cross-law corrections" G2; X9 r3 | owned | each law's next revision | Not scheduled (record only) |
| 7 | **X11 successor law**: the order, the creator's host entry, the one-RequestId rule, how the creator command ends, the creator terminations, the F0 binary restatement, and the backup-status successor | X11 r1; EXIT-PLAN "X11"; `m3/M3-PLAN.md:103-110` | owned | M3-J1 (M3-PLAN:170) | M3 |
| 8 | **X12c**, the DR-131 preview pack row and bundled bytes | X12 r3 | owned | M3-I1. Law r2 accepted by CODEX2 (`m3/reviews/codex2-preview-pack-i1-r2`). Product units I1-a, I1-b1, I1-b2 and I1-c. | M3, after F8b |
| 9 | **X12d**, the Run-closure `check_plan_pack` join in replay, with the corpus moved to the test pack | X12 r3 | owned | M3-C, unit C4 (M3-PLAN:208). `m3/snapshot-plan-c/PROPOSAL.md` item 19 is r1. CODEX2 returned 4 required findings on r1 (`codex2-snapshot-plan-c-r1`, arch `7615a496b`). | M3. It must land before any producer reaches X5. |
| 10 | **Resume/repair writer** for L11's states | EXIT-PLAN:184-189; X9 L11 | owned at milestone level | M3 carry-in (M3-PLAN:112) | M3. **No unit row yet.** The lead should assign it to a unit. |
| 11 | **X3c successor.** Re-committing a Run already committed in the same store and namespace is refused at staging, because X3c-2 always stages a fresh availability record. | EXIT-PLAN, "X3d-2 ordering and follow-ups" (b) | owned at milestone level | M3 carry-in (M3-PLAN:113), counted among M3's law and successor units (M3-PLAN:255) | M3. No unit row yet. |
| 12 | **L1 follow-up**: `license` on `tools/contracts/Cargo.toml`, `tools/contracts/package.json` and `tools/typescript-boundary/package.json` | EXIT-PLAN, "L1 follow-up" | owned | F8b (row 2) | With F8b |
| 13 | **X3a-2**, the read-side adoption of the selected endpoint by the host provisional readers | X3a r5 items 4 and 8 | **open** | none recorded | **Lead decision (2026-10-04): deferred to a scheduled post-M2 unit, X3a-2.** It is due before M3-C1, whose snapshot reads go through the selected endpoint. No CLI path reaches these readers at M2. **Rejected:** building it inside M2's close, which would delay the gate for a path nothing calls. |
| 14 | **X4b**, `grants.rs` `admit_repo_execution_grant` (S10) | X4 r7 item 11 | **open** | none recorded | **Lead decision (2026-10-04): deferred to M3-B3 and M5.** M3-B r1 creates `security/grants.rs` for the M3 authorization flags. `admit_repo_execution_grant` lands with M5's authorized-execution package (M5-EX), under O7. **Rejected:** building it now, ahead of O7, which would fix an execution path before its confinement law exists. |
| 15 | **X4T-c**, the two continuation codes | X4T r11 | **open** | none recorded | **Lead decision (2026-10-04): scheduled immediately after F8b,** because it regenerates contracts. The interim `CONTINUE-CORE-NOT-TRUSTED` stands until then. |
| 16 | **X4 F-1**, observer reread expiry. X4T r9 item 6 says rereads evaluate expiry at the handoff time advanced by elapsed monotonic time. X4T-a's reread evaluates no time, and X4 r7 does not assign the check. | EXIT-PLAN, "X4 F-1"; `grok-live-guards-x4a-r1/REVIEW.md` ("F-1 stays open as an X4T-a successor or an X4 amendment") | **open** | none recorded. The choice is an X4T-a successor or an X4 amendment. | **Lead decision (2026-10-04): a defect, fixed by an X4T-a successor unit, X4-F1, before any M3 analysis ships.** The fix makes observer rereads evaluate expiry at the handoff time advanced by elapsed monotonic time, per X4T r9 item 6. It is disclosed here as a known defect at M2 completion. **Rejected:** an X4 amendment that weakens the requirement. |
| 17 | **The X10 source pin** cuts at the first `#[cfg(test)]\nmod tests`. X11a's pin uses the same cut. | EXIT-PLAN X10 row; Codex's partial X10a notes, as quoted in `grok-read-cli-x10a-r1/REQUEST.md:71`; `apps/cli/tests/doctor_tests.rs:111`, `apps/cli/tests/creator_commands_tests.rs:464` | open | none recorded | None. It is harmless today: the X10a review found that the cut drops no production code (`grok-read-cli-x10a-r1/REVIEW.md:19`). |
| 18 | **X7 item 10's session-level finalization tests**: a committed Run delivered, a renderer failure after commit, a latch after admission, `CommitUndetermined` with the namespace, `ExistingAttempt` with its binding, capacity exhaustion through `finalize`, and the gate-ledger balance assertion | X7 r6, "Session-level finalization tests wait on G1" | **unverified** | X8c, X9-5 or an X7a-2 | X9-5's host rows run F12, F16, F17, F32 and F40 through `finalize`. No record maps the seven tests to landed tests. The lead should record the mapping, or schedule X7a-2. |
| 19 | **`verify_design` silently ignores unknown record fields** | EXIT-PLAN, "D2 and verify_design strictness" | open | "a later tooling unit" | None |
| 20 | **Process:** add both dependency checkers and their suites to the Python lanes of any unit that touches `crates/contracts/src` or `crates/identity/src` | `codex-policy-refresh-f8a-r1/REQUEST.md` item 5; `OVERNIGHT-2026-10-03.md` | owned | lead (process) | From now. F8b and M3-I1 are the first such units. |
| 21 | **EXIT-PLAN record pass.** Several dated follow-up bullets are done but carry no status, and some dates are wrong (§8). | this record | open | lead (record only) | Before or with finalization |
| 22 | **Review-record hygiene.** Missing or stale `status.json` files, and one truncated subject (§8) | this record | open | lead (record only) | Any time |

**Owner blockers.** No M2 item is blocked on the owner. Items 13–16 are lead decisions. The owner blockers B1–B4 in `OVERNIGHT-2026-10-03.md` are M3 items. B4 (OQ-1) is informational only.

**Closed EXIT-PLAN follow-ups** (for the record pass, row 21):

| Follow-up | Closed by |
|---|---|
| VD1 | `96dd114` |
| D1 | `7be09a7` |
| D2 | `933e78b` |
| X1b | D2's refresh; D3 records it closed |
| X3b r7 | X3b r7–r10; X3b-4 `97f630a` |
| X2 r7 | superseded by r8, accepted |
| F3 | `8452ab9` |
| F4 | `8bd0283` |
| F5 | `96ca141` |
| F6 | `5067a27` |
| F7 | `9c5f145` |
| X4T-a3 | `d884ed0` |
| X9 clock dependence | X9 r2: scripted clock |
| X3d-2 ordering | X3d r7; X8 r4 |
| X3d-2 limit (a): no corpus Run binds a fresh ProjectId | X3d-3's synthetic run candidate |
| X8 record notes | X8 r4, r5 |
| X3d-3 closure blocker | `a2c5e8b` |
| G1 | X9-1, X8b; X3d r7, X6 r4, X7 r6 |
| G3, G4 | X6a/b, X4a |
| G5 | X6c; X9 r3 |
| G6 | the X9 row's status cell |
| X6c crash-point fix | X9-2 |
| F8a's half of the stale policy rows | `3e64266` |
| The doctor human label (458c r6 item 10) | X10a |
| The `doctor_report.rs` description | D1 |

## 6. Product state at completion

**Commits.**
- **The matrix commit:** C = `3d2d5b5a5e5cabd1768b02e29eb3c0928264fb4f` (2026-10-03 23:46 -0700).
- **Main:** `3e64266aa8729160cd22509dcfff95a3bb09fcea` (2026-10-04 01:09 -0700). It lies two commits past C: D3 (`30c5db1`) and F8a (`3e64266`).
- **What changed after C:** `git diff --stat 3d2d5b5 3e64266` shows `design-lock.json`, `tools/contracts/dependency-policy.json` and `tools/identity/dependency-policy.json` only. No Rust source and no matrix file changed after C.

**Inventory.** `repository-file-inventory.v134.json` is selected: 552176 bytes, sha256 `626cd71996d79de5c0efd914438dd65b3123e701e774ccdad1f8f9681466c58a`. It plans 968 files; 861 files are tracked at main.

**`verify_design` at `3e64266`.** Command, run in the product checkout:

```
nice -n 19 /opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14 -I -B tools/verify_design.py --architecture /Users/sb/code/opensip-ai/opensip_arch --implementation .
```

| Output member | Value |
|---|---|
| `passed` | `true` |
| `productQualification` | `false` |
| `contractSuccessors` | **76**. That is 69 at `d4239a5` plus seven in the exit period: 461b, X10b, X12-0, D1, D2, EC1, D3. The count is the same as the 76 reported at `30c5db1`, since F8a adds none. |
| `inventorySuccessors` | 94 (55 at `d4239a5`) |
| `inventoryPassageInheritance` | 55 rows |
| `inventoryPassageSupersessions` | 21 (D2's 4 + D3's 17) |
| `inputsVerified` | 46 |
| `applicationManifestSha256` | `dab6e00fc3ccf82f015941bc767a10b18be9e6ca5f1c8598fa1fe9a4d05743f7` |
| selected inventory | v134, as above |

**Test lanes.** These are the last recorded lanes. They ran on X9-6's pre-integration worktree, whose diff `d68bcdf9` is the reviewed subject that became C (`reviews/grok-crash-matrix-x96-r1/REQUEST.md`, "Lanes"):

| Lane | Result |
|---|---|
| Workspace, without the feature, run 1 | 1744 passed, 0 failed, 3 ignored |
| Workspace, without the feature, run 2 | 1744 passed, 0 failed, 3 ignored |
| Crash-matrix lane: `cargo test -p opensip-platform -p opensip-security -p opensip-storage -p opensip-host --features crash-matrix --all-targets` | 1624 passed, 0 failed, 3 ignored |
| `cargo fmt --all --check` | clean |
| Clippy `-D warnings`: the workspace; four crates with `crash-matrix`; three with `scenario-fixtures` | clean |
| `check_package_edges.py --lane host` against v134 | passed |
| Checker unit tests | 26 OK |

No cargo lane is recorded at `3e64266`. D3 and F8a change no byte that Rust reads; F8a's request deferred the workspace lanes to "integration, after those sets". The lead ran the lanes on product main `3e64266` on 2026-10-04, after Grok's rerun. Workspace: 1744 passed, 0 failed, 3 ignored. Crash-matrix feature lane (platform, security, storage, host): 1624 passed, 0 failed, 3 ignored. Workspace clippy `-D warnings`: clean. fmt: clean. `verify_design`: passed, v134 selected. The real home stayed absent.

**Policy checks.**
- After F8a, `check_dependencies.py` and `check_identity_dependencies.py` pass, and so do their suites, 9 and 5 tests (`codex-policy-refresh-f8a-r1`).
- `generate_contracts.py`'s drift check and `check_typescript.py` still refuse until F8b (row 2). `check_typescript.py` refuses first on the absent esbuild archive.

**Surfaces.**
- `opensip doctor` is enabled.
- `opensip`, `analyze`, `fit` and `audit` end on their existing refusals.
- Every M2 writer path is library code, reached only from tests: the commit facade, recovery and the sweep.
- Development builds refuse at InitialCore F0.

**Safety.** No test or run touched the real home (`~/Library/Application Support/OpenSIP`). The reviews record `realOpenSipAbsent: true`.

## 7. EXIT-PLAN status refresh

The "Status / notes" column of [EXIT-PLAN.md](EXIT-PLAN.md)'s units table is refreshed to match §3 and §5, in the same change as this record.
- **Not pinned.** `EXIT-PLAN.md` appears neither in product `design-lock.json` nor in the D-372 application manifest (`docs/coop/design-corrections/reviews/application-subject.v46.json`). Only historical review `hashes.txt` files name it, and they pin earlier bytes as context.
- **Padded rows.** Four rows (X4T-0, X4T, X4B and X12) had only four cells, so their status sat in the "Law?" column. They are padded to six columns, with "—" for Size.
- **Unchanged.** No other column or section of EXIT-PLAN changed. The dated follow-up bullets are left as they were, for the record pass (§5 row 21).

## 8. Record discrepancies found while compiling this record

None of these changes a completion criterion. They are listed so that the reviewer, and the record pass, can check them.

1. **Date drift.** Records written between about 2026-10-01 11:00 and 2026-10-02 10:00 (git commit times) carry dates of 2026-10-03 or 2026-10-04.
   - **EXIT-PLAN follow-up bullets:**
     - "X4T-a3 … (2026-10-03)" is really `01626ee9a`, 2026-10-01;
     - "X4 F-1 (2026-10-03)" is `f04cc8527`, 2026-10-01;
     - "X9 clock dependence (2026-10-03)" is `d2f70dbe9`, 2026-10-01;
     - "F5 widened again (2026-10-03)" is `4048ef406`, 2026-10-01;
     - "X3d-2 ordering … (2026-10-03)" is `aa3537a5d`, 2026-10-01;
     - "D2 and verify_design strictness (2026-10-03)" is `6b8c1f1ba`, 2026-10-01;
     - "X7 follow-ups (2026-10-04)" is `8e3c60c75`, 2026-10-01;
     - "G5 decided in X6c (2026-10-04)" is `778c63866`, 2026-10-01;
     - "X11 (accepted r1, 2026-10-04)" is `8c4aad02e`, 2026-10-01;
     - "X8 record note owed (2026-10-04)" is `6e16b026d`, 2026-10-01.
   - **Law headers:**
     - X9 "r2 ACCEPTED by Grok on 2026-10-04" (accepted at `aa24a2d35`, 2026-10-01) and "r3 (2026-10-04)" (`6e16b026d`, 2026-10-01);
     - X3d "r7 ACCEPTED … 2026-10-04" (`6e16b026d`);
     - X7 "r5 … 2026-10-04" (`75c607314`, 2026-10-01) and "r6 … 2026-10-04" (`6e16b026d`);
     - X11 "r1 ACCEPTED … 2026-10-04" (`8c4aad02e`);
     - X5 "r3 ACCEPTED … 2026-10-03" (`3e02f71b2`, 2026-10-01);
     - X10 "r4 ACCEPTED … 2026-10-03" (`69583023b`, 2026-10-01);
     - VD1 "r1 ACCEPTED … 2026-10-03" (`eafe9c273`, 2026-10-01);
     - X8 "r4 (2026-10-04) … r4 ACCEPTED by Grok on 2026-10-02" (`d8166e48e`, 2026-10-02), which contradicts itself.
2. **EXIT-PLAN corrections that laws asked for and nobody applied.** All three are now noted in the refreshed status cells:
   - X8 r5: the X8 row gains "law X8 r2; units X8a–X8c", and the "Choices" doctest recommendation is superseded by X8 item 1;
   - X12 r3: X12 depends on nothing, and its row should read "…units X12-0, X12a, X12b; X12c and X12d at M3";
   - X9 G6: the X9 row's "Depends on" omits X2e and X5.
3. **EXIT-PLAN bullets now stale.** "X9 follow-ups (from X9-3)" says to fold the r14 overstatement into X9's next record note, but X9 r16 has already recorded it, and F7 has fixed the clock flake. Most other dated bullets are done, without a status marker (§5, "Closed EXIT-PLAN follow-ups").
4. **Units declared by accepted laws, never built, with no deferral record:** X3a-2, X4b and X4T-c (§3.3).
5. **Review-record hygiene.**
   - **No `status.json`:**
     - `grok-journal-start-x3b1b-r2`, which is the review the design lock binds for v97;
     - `grok-git-tracking-x2b2-r1`;
     - `grok-journal-rollover-x3b4-r1`, `-r2` and `-r3`;
     - `grok-ledger-blob-x3c2-r1`;
     - `grok-namespace-lease-x2d-r1`;
     - `grok-operation-handoff-x2e-r1` and `-r2`;
     - `grok-recovery-capture-x6a-r1`;
     - `grok-trust-bootstrap-x4ba-r1`;
     - `grok-trust-floor-x4tb-r1`.
   - **Stale `status.json`** (the round was answered, superseded or accepted):
     - `grok-finalization-x7-r1` (SENT) and `-r2` (PENDING);
     - `grok-policy-admission-x12-r1` and `-r2` (PENDING; r2 has a REQUIRED-FINDINGS review);
     - `grok-trust-admission-x4t-r8` and `-r10` (PENDING; both have REQUIRED-FINDINGS reviews);
     - `grok-trust-bootstrap-x4b-r1` (SENT), `-r2` (PENDING) and `-r3` (PENDING, with a REQUIRED-FINDINGS review);
     - `grok-crash-matrix-x90-r1` (DRAFTED, while its review is ACCEPT-UNIT);
     - `grok-project-root-x2-r7` (QUEUED, superseded by r8);
     - `codex-read-cli-x10a-r1` (SENT; never completed, and Grok's X10a review is the one bound).
   - **Other:**
     - `grok-crash-matrix-x9-r16/status.json` records a 12-character subject prefix, `f08efe95deba`. Its `review.json` has the full value.
     - `grok-crash-matrix-x96-r1/status.json`'s `"pending"` member still lists the final lead sets and the evidence record, which are now done.
6. **Record hygiene count.** The lead decision says "The 12 staged notes land with the next successor". `staged-notes.patch` holds 11 hunks. The batch has 12 notes in all, but one is already applied, in `prototype-evidence-reference.md`.
7. **F8b's status line.** `generator-closure-f8b/PROPOSAL.md` still reads "Status: **DRAFT r2 for review**", although CODEX2 accepted r2 (`codex2-generator-closure-f8b-r2/status.json`: ACCEPTED; arch `1648ceb7e`).

## 9. Finalization checklist for the lead

1. **When Grok's rerun returns,** copy `REVIEW.md` and `review.json` into `reviews/grok-crash-matrix-x96-r2/` and set its `status.json`.
2. **Fill the tokens.** Fill every `RERUN` token in §2.2, and the `LEAD` token in §6. The "Finalization tokens" table keeps its token names: delete it, or mark it filled. Then `grep -n '\[\[' M2-COMPLETE.md` should find nothing outside that table.
3. **Decide items 13–16 of §5** (X3a-2, X4b, X4T-c, X4 F-1). Record each decision, with its rejected alternative, in the owning law or here. Then update §1 claim 5, §3.3 and §5.
4. **Change the status line** to "**COMPLETE (date)**", or keep PENDING-RERUN if the rerun had required findings.
5. **Commit this record and the EXIT-PLAN refresh.**
6. **Rehash for GROK2.** Recompute `hashes.txt` in `reviews/grok2-m2-complete-r1/` over the finalized bytes, commit, and send the request to GROK2 (w6:p1).
7. **On GROK2's acceptance,** record it here and in EXIT-PLAN's X9 row.
