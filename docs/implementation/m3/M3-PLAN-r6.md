# M3 unit plan

Draft r5. Claude Opus 5.5, implementation lead. **Planning record: not law, not code, not a contract successor.** It is the M3 counterpart of [m2/EXIT-PLAN.md](../m2/EXIT-PLAN.md). It orders M3's obligations into reviewable units and changes no accepted contract, gate, threshold or register row.

**Product baseline:** main `3e64266`. M2's exit gate X9-6 is integrated as commit C = `3d2d5b5`, followed by D3 (`30c5db1`) and F8a (`3e64266`). The M2 crash matrix gave `matrixPass: true` on C. M2 completion still waits for Grok's independent rerun on C (M2C:5, "PENDING-RERUN"). X9-6 is in, so the r4 rule "no unit touches product crates before X9-6" is now met.

**History.** r1 (`M3-PLAN-r1.md`, sha256 `65bf6ac5…`) and r2 (`M3-PLAN-r2.md`, `add49e25…`) were reviewed by GROK2 (facts) and CODEX2 (method). r3 (`M3-PLAN-r3.md`, `7ef4f0d1…`) was accepted by GROK2. **r4 was accepted on 2026-10-03:** CODEX2 accepted r4 (`e50f75d3…`; method), and r4 differs from r3 only by CODEX2's exit-formula finding. r4's bytes are preserved in `M3-PLAN-r4.md` (43,947 bytes, sha256 `e50f75d3cb7fbbb4d44484585adf2b9899ef6e291a3c4d90fb619fcc9f3663c8`). r5 folds in the night of 2026-10-03 to 2026-10-04: the accepted M3-T2, M3-Q0, M3-I1 and M3-B records, M3-C r3, the M3-E1 and M3-L drafts, and the M2 completion draft.

**Short names.**
- **Contracts and architecture:**
  - **BP** `docs/v2/architecture/implementation-boundaries-and-build-plan.md`;
  - **COV** `docs/v2/architecture/implementation-coverage.v1.json`;
  - **CH14** `docs/v2/architecture/14-repository-and-module-layout.md`;
  - **F02** `docs/v2/architecture/02-distribution-and-components.md`;
  - **REG** `docs/v2/architecture/08-decision-and-readiness-register.md`;
  - **NE / IE / AQ / WS / SL** `docs/v2/contracts/product-v1/{native-evidence,identity-and-evidence,admission-and-qualification,workflows-and-surfaces,security-and-lifecycle}.md`;
  - **PTT** `docs/coop/artifacts/permission-truth-tables.v9.json`;
  - **TES** `docs/coop/design-corrections/workflows/schemas/test-execution.schema.json`;
  - **NEM** `docs/coop/design-corrections/native/native_evidence_model.v2.py`;
  - **RPP** `docs/coop/artifacts/rust-provider-protocol.v2.json`.
- **Accepted plans:**
  - **AQP** `docs/implementation/m3/analysis-quality/PLAN.md`, the live file: r6, accepted, sha256 `1611014d…` (r6 bytes plus its 2-line acceptance note). **r5 re-pins every AQP line to this file.** r4 cited the r4 live file, whose lines have since moved.
  - **OPP** `docs/implementation/m3/operability/PLAN-r3.md` (r3, sha256 `b49035f2…`, accepted by Codex). OPP is cited **by section**, so that a later revision doesn't silently move a citation.
- **M3 unit records:**
  - **T2R** `docs/implementation/m3/corpus/README.md` (T2a and T2b accepted by GROK2; sha256 `3d355e72…`).
  - **HD** `docs/implementation/m3/harness/DESIGN.md` (M3-Q0, r13 accepted by CODEX2; live sha256 `1f108399…`).
  - **MI / MIU** `docs/implementation/m3/preview-pack-i1/{PROPOSAL,UNITS}.md` (M3-I1 r2, accepted by CODEX2; live sha256 `8cb31152…` and `0c3c0f44…`).
  - **MB** `docs/implementation/m3/config-discovery-b/PROPOSAL.md` (M3-B r2, accepted by GROK2; r2 bytes `92e65825…`, live file with its note).
  - **MC** `docs/implementation/m3/snapshot-plan-c/PROPOSAL.md` (M3-C **r3, in review with CODEX2**, sha256 `2e455c70…`; r2 `bf44ffe2…` had 3 required findings). MC is cited by section.
  - **ML** `docs/implementation/m3/provider-protocol-l/PROPOSAL.md` (M3-L r1 draft, acceptance-gated, not sent; sha256 `5e858c05…`).
  - **ME** `docs/implementation/m3/syntax-e/PROPOSAL.md` (M3-E1 **r1, in review with Codex**, sha256 `90175f28…`). ME is cited by item.
  - **SOP2** `docs/implementation/m3/operability/s-op-2/PROPOSAL.md` (S-OP-2 r3, with Codex).
- **M2 records:**
  - **EXIT** `docs/implementation/m2/EXIT-PLAN.md`. Its status-column refresh of 2026-10-04 added 2 lines after the units table, so **r5 re-pins every EXIT line after line 61**.
  - **M2C** `docs/implementation/m2/M2-COMPLETE.md` (draft, PENDING-RERUN).
  - **F8B** `docs/implementation/m2/generator-closure-f8b/PROPOSAL.md` (r2, accepted by CODEX2; execution pending).
  - **X11** `docs/implementation/m2/cli-enablement-x11/PROPOSAL.md` (r1, accepted).
  - **X12** `docs/implementation/m2/policy-admission-x12/PROPOSAL-r3.md`: the accepted r3 bytes. The live `PROPOSAL.md` is now the X12 r4 draft (M3-B successor S2), so **r5 cites the r3 snapshot**, whose lines equal r4's citations.
  - **X2r9** `docs/implementation/m2/project-root-x2/PROPOSAL.md` (X2 r9 draft, M3-B successor S1).
- **The overnight log, ON:** `docs/implementation/OVERNIGHT-2026-10-03.md`, cited by entry.
- Product paths are under `opensip/`.

## r6 changes

r6 answers GROK2's r5 review and changes nothing else. r5 is preserved as `M3-PLAN-r5.md`.
- **RF-1:** B2 now cites HD §5.6, §5.8 and OI-3. It states the accepted gating floor (a 0.99 lower bound, k_min 299) and that 59 is the zero-error count for the lead's proposed 0.95 bound.
- **RF-2:** G7 now records that S-OP-2 r3 received required findings and that r4 is in review.

## r5 changes

| # | Change | Source |
|---|---|---|
| 1 | **Header.** The r4 ACCEPTED note is removed. The baseline is main `3e64266`; M2 completion waits for Grok's rerun on C. | ON ("X9-6 accepted and integrated", "M2 crash matrix"); M2C:5, §6 |
| 2 | **M3-T2 is complete.** T2a and T2b are accepted: 49 repositories, 33 families, 5 workspaces. Its two open items are carried into K1a and the gating bar. | ON ("M3-T2b sent", "accepted by GROK2"); T2R:24, T2R:296; `reviews/grok2-corpus-t2b-r1` |
| 3 | **M3-Q0 is accepted.** K2 is sized at **16 days**, with per-lane oracle freezes. K2b and K2c are frozen before day 0, and K2a on days 0–6. Every bound in Q0's OI-12 list is applied: the K2 row, the R and M3-M rows, the K2 condition, the unbounded list, the pre-day-0 list, F1's first T1 run, and the slip rule, recomputed for r5. | HD §13 (HD:1177-1237); OI-12 (HD:1256) |
| 4 | **M3-I1's law is accepted, and I1 is resized from M to L.** It splits into I1-L, I1-P, I1-a, I1-b1, I1-b2 and I1-c. New edges: **I1-c → C4a**, **I1-b2 → X12d and J2**, and **F8b → I1-a**, because the contract generator refuses until F8b. | MI (r2 ACCEPTED); MIU:28-40; ON ("M3-I1 r1 sent", "F8 split"); M2C §5 row 2 |
| 5 | **M3-B's law is accepted.** It has nine code and harness sub-units and two design units, with successors S1 (X2 r9) to S9. The discovery ledger profile raises the platform caps for discovery only. **B2-c, which C1a waits for, finishes on day 10.** MB's own estimate of "about day 8" omits B2-b's edge on B1-b. | MB items 12 and 25, F14 (MB:805), unit table (MB:843-851) |
| 6 | **M3-C r3's units are taken in.** C1, C2 and C3 each have three sub-units; C2b is a hard XL part (5 days). C3b gets the D1 edge, with O7 and the D law as day-0 assumptions. C4 splits into C4a and C4c (variant B), with C4b = X12d. **X12 r4 and SX-1 become gates.** F1 and G1a wait only for the interfaces they consume. | MC "r3 changes", "Successors", "Units", "Acceptance gate"; `reviews/codex2-snapshot-plan-c-r2` (C2-N1) |
| 7 | **The critical path is recomputed: 33 days** under variant B (34 unsplit). That is MC r3's b + 23 with b = 10. Its conditions are K2 by day 28, O2_selected by day 31, and X12d's lead set by day 22. The slip rule is now M3-X = 33 + max(0, *s* − 10). r4's 26 days and MC r2's 28 no longer hold. | "Critical path" below; MC "Units"; MB:843-851 |
| 8 | **M2 carry-ins without an owner now have one** (lead decisions P5-1 to P5-5). The **resume/repair writer** goes to J-RW (law) and J4 (code), and J4 no longer waits for J3. The **X3c successor** goes to X3c r8 (law) and X3c-3 (code) before J3. Also scheduled: X3a-2, X4T-c, X4-F1, X4-F2 and F9, with X4b deferred. M2C's "no M3 unit row names it" overstates the gap. r4's M3-J row did name J4 and an X3c successor (M3-PLAN-r4.md:168), but gave neither a law, an author nor a code unit. | M2C §3.3, §4.1 (L11), §5 rows 2, 10, 11, 13–16; EXIT:171, EXIT:186-191; ON ("X4-F1 written") |
| 9 | **M3-L's gate is updated.** T2b and S-OP-2 are now met. S-M, the D3 and D13 sign-offs, and O7 remain open. | ML "Acceptance gate"; ON; `reviews/codex-s-op-2-r3/status.json` |
| 10 | **M3-L's findings are recorded.** Changed-scope reuse needs an identity-contract successor (INC-1). The Rust3 stage-1 cancel grace is 5,000 ms. | ML item 4 (ML:180-188), item 16c (ML:453-455), X3 |
| 11 | **Owner decisions still pending:** O7 (B1), the gating precision bar (B2), the D3 and D13 sign-offs (B3), and OQ-1 (B4). Tonight's lead decisions are listed. | ON "Blockers for the owner"; MB item 27; MC "Open questions"; M2C §5 |
| 12 | **Citation re-pins:**<br>- **"AQP:537" is now AQP:556**, and every other AQP line moves with it (for example, INC-1 to INC-8 are now AQP:389-409);<br>- X12 is cited at its r3 snapshot;<br>- EXIT lines after 61 move +2;<br>- `package.json:7`, `:12` become `:8`, `:13` after L1's licence line;<br>- the stale "Draft r3" header is fixed. | MB:38 (F8); ML:553 (X8); `git diff 6f85fe717 HEAD -- EXIT-PLAN.md`; product `git diff eb0d503 3e64266` |
| 13 | **Non-blocking observations folded in:**<br>- the stale "operability r3 in review" risk is removed (GROK2 r3 NBO-2);<br>- G2-v is said not to be D1's enforcement claim (NBO-3);<br>- late branches are compared by their arrival at M3-X (CODEX2 r4 N01). | `reviews/grok2-m3-plan-r3/review.json`; `reviews/codex2-m3-plan-r4/review.json` |
| 14 | **Smaller updates:**<br>- the licence unit is done (L1, product `2967905`);<br>- T3 now waits only on OQ-1 for its multi-repo instance;<br>- the calibration count is 62 commits;<br>- the effort count and lanes are updated. | M2C §3.2 (rows 59 and 62); AQP:547, AQP:555; MB "Not claimed" |
| 15 | **The C law can be accepted only after L** (MC's gate), so it is accepted at or after day 0. The DAG tolerates acceptance by day 5, with SX-1 by day 2. | MC "Acceptance gate", "Units"; "Critical path" below |
| 16 | **M3-E's units come from E1 r1** (drafted, in review with Codex): E0 (a probe), E2a, E2b, E2c and E3. The backend decision is tree-sitter grammars compiled to Wasm, run in-host by `wasmi`, with native tree-sitter as the fallback if E0 fails. E3 lands on day 14, with 14 days of slack, so the host chain does not move. | ME items 2, 3, 19, 20; ON ("M3-E1 r1 drafted") |
| 17 | **The overnight log's "about 31 days"** (its "M3-C r3 sent" entry) is the b = 8 figure. r5 records **33** (b = 10) and shows 31 only as MB F14's estimate. | ON; row 7 |

## r4 changes and review responses

r4 changes one thing. GROK2 accepted r3 (`7ef4f0d1…`), and r3 is preserved as `M3-PLAN-r3.md`.

| Finding | Change |
|---|---|
| CODEX2 C2-M3-R3-01 | `O2_selected` is now in M3-X's dependencies and in its maximum. The 26-day condition now also needs every O2 part kept in M3 to finish by day 24. The note on which branch becomes critical when it runs late is qualified to match. |

## r3 changes and review responses

| Finding | Change |
|---|---|
| GROK2 RF-1, CODEX2 C2-M3-R2-01 (the DAG and critical path) | **Missing edges added:**<br>- K1 → M3-M;<br>- CF-P → D-law acceptance;<br>- CF-1 → D5 and D's enforcement claim;<br>- D1's confinement primitive → every provider launch.<br>**Authoring and launch are separate.** G2 is authored before day 0. Its lawful launch, G2-v, runs after O7 and D1.<br>**Every M3-M and M3-X prerequisite has a duration or a finish bound,** with three exceptions: K2, R and O2. Those are unbounded until Q0 sizes K2 and their successors are accepted.<br>**26 days is now only the conditional host-chain duration.** The whole-M3 total is left uncomputed. |
| GROK2 RF-2 | M3-M cites AQP:236 only for too few findings. Closing an exploratory report with gating or repair-eligible adjudication still pending is **this plan's rule**. Any later Q2 use still needs AQP:228 and AQP:246. |
| GROK2 RF-3 | OPP §10 is cited for its ten areas. The three escape cases are new D5 and S-OP-11 controls. |
| GROK2 RF-4, CODEX2 C2-M3-R2-02 | A gated **M5 successor package, M5-EX**, must be accepted before M5's `execution.rs` claims any enforcement:<br>- the native §5.2 admission and disclosure join (NE:2440-2444, NE:2480-2487; NEM:2170-2182);<br>- the WS §7 test-execution schema join (WS:1071-1081; TES:7-14);<br>- a measured truth-table profile succeeding PTT.<br>Repository-code execution stays out of M3. The worker prohibition (NE:2534-2535) and the closed DR-128 untrusted-code scope (AQ:344; REG:317) are preserved. |
| GROK2 NBO-1..6 | Adopted:<br>- the citations are now `policy.rs:1087`, `policy.rs:1401`, X12:134, NE:2534-2535 and COV:4772 with 8976;<br>- the r2 response wording for S-OP-4 is clarified below: S-OP-4 is law content, not a gate item;<br>- CF's gates add G09 and G30 (AQ:344);<br>- launch rules have one owner, the D law, and M3-L cites it. |
| CODEX2 N01..N03 | Adopted:<br>- S-P and S-M state their launch boundary;<br>- the escape controls are labelled as an extension;<br>- the NE:2534-2535 span. |

(The AQP lines in the r3 and r2 tables are r4-era lines, kept as reviewed. r2's table is in `M3-PLAN-r4.md`.)

## What M3 exit means

The build plan's milestone row (BP:887) defines M3:

- **Deliverable:** "M2 and provider build lanes; discovery/configuration, sealed snapshot/Plan, supervised TS/JS and Rust analysis and the guarded durable host pipeline".
- **Owners:** "Host discovery/snapshot/plan/analysis; components protocols; both providers and evaluator".
- **Completion:** "Selected native matrix/corpora, missing-role disclosures, cancellation, semantic admission and host-boundary durability checks; neither language silently dropped. Complete CLI analysis delivery follows at M4 with every advertised renderer".

**Routed to M3 by the coverage groups** (COV), with the gates in the qualification routing table (BP:999-1036). BP:933-945 is only the population census.

- **All 66 capability cells** (COV:2077-4425): 57 SUPPORTED-DESIGN, 6 UNSUPPORTED-TYPED and 3 NOT-SELECTED (AQP:113). That is 33 TS/JS, 22 Rust and 11 syntax-only cells.
- **Seven gates, to be prepared, not qualified:** DR-G10 (BP:1014), G13 (BP:1017), G14 (BP:1018), G21 (BP:1025), G23 (BP:1027), G25 (BP:1029) and G29 (BP:1033). Execution stays at M6 (BP:895, BP:999-1000).
- **All seven shared flags** (COV:5266-5407).
- **Twelve contract sections:**
  - security-and-lifecycle:3 (COV:6702);
  - native-evidence:2, :3, :4, :5, :7, :9, :10, :11, :14 and :15 (COV:7066, 7093, 7118, 7144, 7193, 7245, 7270, 7294, 7366, 7390);
  - workflows-and-surfaces:2 (COV:7438).
- **Five Fallow constraints:** FW-01 (COV:7852), FW-03 (7894), FW-08 (7999), FW-13 (8104) and FW-14 (8125).
- **No command.** Every analysis command is M4 or later (BP:949-995). Complete CLI delivery is M4 (BP:887-888).

**The accepted quality plan's M3 obligations.**

*Before the provider protocol is fixed* (AQP:499):
- INC-1 to INC-8 in the M3 law, plus the INC-7 spike;
- pinned T2 manifests, including the multi-repo approximation and Python (**done**: M3-T2);
- the harness design and the rule-catalog draft (**done**: M3-Q0).

*At M3* (AQP:500):
- T1 for all 57 supported cells per mode, typed refusal for 6 and non-advertisement for 3;
- Q1 and Q4 on T1;
- draft catalog rules run non-authoritatively, for exploratory Q2–Q4 on T2;
- the determinism suite and exploratory Q6 workloads;
- the multi-repo workspace shapes in discovery;
- the third-language readiness review;
- an internal-harness dogfood checkpoint, "not CLI `analyze`".

**The operability plan's provisional M3 items** (OPP r3 §8).

*Before the protocol law:*
- O1 decided, with S-OP-4's record join under (a). ML item 11 decides it, as a lead decision.
- O7 decided by the owner. **Still pending (B1).**
- The S-OP-2 vocabulary drafted. **Done:** r3 is with Codex.

*At M3:*
- `tracing` with nonpersistent sinks, the vocabulary and allowlists, the bounds and loss marker;
- phase spans and the operational record as harness instrumentation;
- the supervision primitive and liveness;
- the outcome matrix in tests;
- two-stage cancellation;
- the enforcement checks.

*Once their successors are accepted* (OPP §9): the file sink (S-OP-1), crash records (S-OP-7), capacity preflight (S-OP-8), public switches (S-OP-5 and S-OP-6), and the cancellation and commit join (S-OP-12). The G20/G21 controls are authored now (S-OP-11). DR-G20 itself is an M5 implementation row (BP:1024).

**M2 carry-ins.** Every one now has an owning unit; the table under "Units" gives the gates.
- **X11 successor law** → J1. No creator command went live in M2 (EXIT:182; X11:18). The successor must fix:
  - the order;
  - the creator's host entry;
  - the one-RequestId rule;
  - how the creator command ends;
  - the creator terminations;
  - the F0 binary restatement;
  - the backup-status successor (X11:64-81);
  - X11 r1 item 1a's conflict with X12 r4's first-use clause (ON, "X2 r9 and X12 r4 drafted").
- **X12c and X12d.** X12c, the DR-131 preview pack, is **M3-I1**. X12d, the Run-closure `check_plan_pack` join, is **C4b**. It must land before any producer reaches X5 (X12:191-192).
- **The resume/repair writer** for the crash states M2 leaves refused (EXIT:186-191; M2C §4.1, L11) → **J-RW and J4** (P5-1).
- **An X3c successor**, because re-commit is refused at staging (EXIT:171) → **X3c r8 and X3c-3** (P5-2).
- **New from the M2 completion draft:** F8b, X3a-2, X4b, X4T-c, X4-F1, X4-F2 and F9 (M2C §3.3, §5; ON).
- **The product licence unit is done:** L1 at product `2967905`, inventory v134 (AQP:555; M2C §3.2 row 59).

## Product state, by M3 owner module

The table was read at `eb0d503` for r4. For r5 every cited product file was rechecked with `git diff eb0d503 3e64266`. Only two changed: `providers/typescript/package.json` and `providers/rust/Cargo.toml`, each gaining L1's `license` line. The two `package.json` citations move by one line; the Rust `Cargo.toml` line is unchanged.

| Owner (BP:887; CH14) | State | What exists |
|---|---|---|
| `crates/host/src/discovery.rs` | **absent** | First milestone M3 (COV:8963). |
| `crates/host/src/configuration.rs` | partial | Only X12's pack admission. "Layer merge, discovery, profiles, capabilities, waiver IDs and `resolvedConfigDigest` arrive with M3" (`crates/host/src/configuration.rs:1-4`). The digest is defined at IE:518. |
| `crates/host/src/snapshot.rs`, `plan.rs`, `analysis.rs`, `invocation.rs`, `syntax.rs` | **absent** | Planned owners at CH14:495, 489, 475, 485 and 496. |
| `crates/host/src/fact_admission.rs` | partial | The replay join only. "The M3 syntax, context, occupancy and Coverage joins arrive in this module" (`fact_admission.rs:1-3`). |
| `crates/host/src/request.rs`, `outcomes.rs` | partial | A process-custody `RequestAuthority` for the nonpersistent metadata host (`request.rs:15-19`). |
| `crates/host/src/finalization.rs`, `crates/storage/src/commit.rs` | present (M2) | The finalization and commit library. No command reaches it (`crates/host/src/lib.rs:53-62`). |
| `crates/components/*`, `crates/syntax/*` | **absent** | Not workspace members (`Cargo.toml:3`). CH14:37 and CH14:41 mark them "proposed". |
| `crates/security/src/component_manifest.rs` | present | The structural manifest owner, "no runtime or artifact authority" (`component_manifest.rs:1-2`). `components/manifest.rs` (the DR-G29 owner, BP:1033) is absent. |
| `crates/security/src/grants.rs` | **absent** | Yet it owns four M3 flags (COV:5277, 5317, 5337, 5377). MB's B3-a creates it. X4b's `admit_repo_execution_grant` is deferred to M5-EX (M2C §5 row 14). |
| `crates/platform/src/process.rs` | **absent** | The only process module is a read-only translation query (`crates/platform/src/macos_process.rs:1-2`). |
| `crates/evaluator` | largely present | Inspectors (`crates/evaluator/src/lib.rs:9-38`), pack admission (`lib.rs:111`), derivation (`lib.rs:122`) and replay (`lib.rs:127`). The pack registry has **zero rows** (`pack-registry.json:3`). Named admission returns `NotBundled` (`policy.rs:1087`), and `check_plan_pack` refuses an unbundled Plan policy (`policy.rs:1401`, with the refusal at `:1402`). |
| `crates/identity`, `crates/contracts` | present | The `IdentityDomain` enum and its prefixes, `fact2` through `subject3` (`crates/identity/src/descriptors.rs:483-555`). Generated TS2 and Rust3 frame carriers (`crates/contracts/src/generated/protocol.rs:5422`, `:6111`) from a carrier input that is "not a production wire decoder" (`schemas/wire/native-carriers-v1.json:4`). The generator's drift check refuses until F8b (M2C §6, "Policy checks"). |
| `providers/typescript` | stub | Present: `package.json`, `tsconfig.json` and the inert generated types (`src/generated/protocol.ts:1`), pinning Node 24.16.0 and TypeScript 6.0.3 (`package.json:8`, `:13`). Absent: every implementation source in CH14:507-517 and CH14:519-524. |
| `providers/rust` | stub | `main.rs` exits failure before reading a request (`providers/rust/src/main.rs:1-14`). It has its own workspace (`Cargo.toml:1-2`) and `rust-version = "1.95"` (`Cargo.toml:8`). The 1.95.0 pin has only rustfmt and clippy, no `rustc-dev` (`rust-toolchain.toml:2-4`). |
| `crates/lifecycle/src/installation.rs` | **absent** | The DR-G14 owner (BP:1018; COV:4770-4772), whose first milestone is M5 (COV:8976). |
| Tests | partial | `crates/host/tests/admission_tests.rs` exists. These named owners are absent: `discovery_tests.rs` (COV:5280), `workflow_tests.rs` (COV:7865) and `tests/qualification/README.md` (COV:8138). |
| Operability | **absent** | No `tracing` in `Cargo.lock`. No `std::panic::set_hook`. No `--timings` in `apps/cli/src/arguments.rs`. Three coded stderr lines (`apps/cli/src/bootstrap.rs:19`, `:44`, `:65`). The default command refuses (`arguments.rs:104`). |

Also in place:
- the M1 provider lane checks (`tools/check_typescript.py`, `tools/typescript-lanes.json`). Both refuse until F8b re-pins `verify_design.py` (F8B, "Problem").
- the Rust provider, excluded from the host workspace (`Cargo.toml:4`), as BP:621-622 requires.

**Stale text that the M3 laws must not copy.** F02:220 still says TypeScript major 1, and F02:259 says Rust major 2. The current protocols are TS2 and Rust3 (BP:716-717).

## Units, in dependency order

Sizes follow EXIT:61:
- **S:** about one review round of a single file.
- **M:** several files with one inventory successor.
- **L:** a law plus two or three code units.
- **XL:** a law plus four or more units and a harness.

Each sub-unit (B1-a, C2b …) is reviewed on its own; the row is the planning unit. The dependency column gives integration edges. A unit may be **authored** earlier, against its predecessors' accepted interfaces (MC "Units").

| Unit | Scope | Depends on | Law / successor? | Size | Gates and quality items |
|---|---|---|---|---|---|
| M3-T2 | **Done.** T2 corpus manifests and a harness-only `corpus fetch` (AQP:215, AQP:219-227). T2a and T2b are accepted by GROK2: 49 repositories, 5 multi-repo workspaces, 33 independence families (T2R:24). It includes the FW-14 inputs (COV:8125-8145).<br>**Carried out of T2:**<br>- only 10 held-out families exist (T2R:296), which bears on the gating bar (B2);<br>- aws-cdk and aws-sdk-rust exceed the 4 MiB canonicalizer limit for the tree digest, so K1a may need a chunked digest (ON, "M3-T2b sent"). | — | none; **D3 sign-off pending** (AQP:543; B3) | M | O1, D3, D9, D15, FW-14 |
| M3-Q0 | **Accepted, r13** (HD:3): the case model (AQP:138-143), the label ledger (AQP:257-271), the confidence rule (AQP:241-245), the exploratory envelope (AQP:438-444), the D12 runner, and the rule-catalog draft specs (AQP:175-199). **K2 is sized at 16 days** (HD §13). | — | D13 and D2 sign-offs (AQP:542, AQP:554); D12 (AQP:553) | M | Q1–Q8 definitions |
| M3-S | **S-P, feasibility probe:** can the pinned toolchain host the `rustc_driver` sidecar? Can Node and TypeScript load from a closure path? It is labelled preliminary and makes no Q6 claim.<br>**S-M, the measured INC-7 spike:** one-shot startup, sealing and replay costs on medium T2 (AQP:408), from a throwaway harness outside the product. S-M is a lead run set, queued on the machine (P5-8).<br>**Launch boundary:** S-P and S-M are lead-run throwaway tooling over public, pinned T2 bytes. They are not the product supervisor. They execute no repository code: no build script, proc-macro or package script. Their samples are labelled preliminary, and they make no production or confinement claim.<br>**Status:** neither has started. | S-P: — . S-M: T2a (met), Q0 envelope (met), D13 sign-off. D12 for Q6-labelled samples (AQP:553-554). | none | M | INC-7, Q6 |
| M3-CF | **Confinement work for O7** (see "O7").<br>- **CF-P, the confinement-feasibility probe:** a lead trial with a trivial test child, with no provider and no repository bytes. It covers the programmatic Seatbelt trial on macOS 27 (network denial and write-outside-scratch denial) and a desk check of the Linux primitives. It runs before D-law acceptance and needs no O7 decision, because it launches nothing that analyzes.<br>- **CF-1 and CF-2,** the successors, start once O7 is decided. | CF-P: — . CF-1/CF-2: O7. | SL S10 and S6 successor; AQ §5 item 4 and DR-128 disposition; disclosure-carrier successor | L | G09, G21, G29, G30 (AQ:344); O7 |
| M3-L | **M3 provider-protocol and reuse law. Drafted as r1, not sent** (ML; its request is a draft, `reviews/grok-provider-protocol-l-r1/REQUEST.md`). It carries:<br>- INC-1 to INC-8 (AQP:389-409), with TS2/Rust3 unchanged (INC-5; BP:716-717) and one child per universe with no reuse (F02:222, F02:269);<br>- O1(a) and the S-OP-4 record join (OPP §3.6, §9);<br>- RequestId as correlator and phase-lawful identities (OPP §3.1);<br>- the provider-side two-stage cancel (OPP §5.5), with the commit-phase join referred to S-OP-12 and M3-J;<br>- a reference to the D law, which alone owns the launch rules under O7;<br>- a record correcting DR-G10's selector (REG:355 against COV:4671).<br>**Findings in the draft:**<br>- `cache2` binds the Plan, and any source edit changes `plan2`, so **changed-scope reuse needs an identity-contract (D5a IE) successor, the INC-1 successor,** before it can ship. Nothing ships at M3 (ML:180-188).<br>- **The Rust3 stage-1 cancel grace is 5,000 ms** (RPP:119), fixed by the protocol and checked by exact equality in Hello. TS2 has no grace member, so D3's provisional 2 s applies there (ML:453-455).<br>**Acceptance gate:** S-M, complete T2 (T2b), Q0, D3, D13 and the D2 draft, S-OP-2 drafted, O1 and **O7 decided**. The S-OP-4 join is the law's content, not a gate item. Gate status is in "M3-L gate status". | the gate | **law**; D5a successors only if an INC needs one (AQP:546); S-OP-4 | L | G10, G21; INC-1..8; O1, O7 |
| M3-P0 | **Package scaffolds:**<br>- `crates/components` and `crates/syntax` (CH14:284, CH14:288) as members;<br>- the provider source layout;<br>- dependency-policy rows, including MC item 12's inflater row.<br>One inventory successor, so that parallel lanes don't race the linear chain. **Unblocked:** X9-6 and the licence unit are integrated. Like every unit that touches `crates/contracts` or `crates/identity`, it runs both dependency checkers in its Python lanes (M2C §5 row 20). | X9-6 (met); licence unit (met) | inventory successor | S | — |
| M3-B | **Configuration and discovery. Law r2 accepted by GROK2** (MB). Units (MB:843-851):<br>- **B-S1** (design, M): successor S3, the SL S3 and NE §1.4 passages, with S9's remedy text and MC's SX-1 (`.opensip/` is never source). **B-S2** (design, S): successor S4, IE `vcs-observation` schema 3.<br>- **B1-a** (M) and then **B1-b** (M): the resolver, `resolvedConfigDigest` (IE:518), FW-13, and the carriers with X2 r9 item 3a.<br>- **B3-a** (S): `grants.rs` with the four authorization records. X4b's `admit_repo_execution_grant` is **not** built at M3: it goes to M5-EX (M2C §5 row 14).<br>- **B2-a** (M), **B2-b** (L), **B2-c** (L) and **B2-d** (M): the shared rule; the S3 downward instrument with the **discovery ledger profile**; the native unit instrument U-0..U-9; host-side recognition (NE:2750).<br>- **B3-b** (L): D15 members through X2 r9 item 6b. **B3-c** (M, harness): the FW-14 outputs.<br>**Discovery caps (MB item 12).** The platform caps of 65,536 objects and 131,072 edges cannot hold T2's large repositories. A discovery-only ledger profile raises them, provisionally to 2^20 objects, 2^21 edges and 2^30 bytes (MB:338). A T2 census margin test (≥ 2×) guards the caps, and a failure returns them to the law. Exhaustion is `WORK.BUDGET_EXHAUSTED`, never truncation.<br>**D15's value at M3 is bounded** (MB F2–F4). There is no cross-unit resolution, and links are honoured only after S5 and S6. | P0, L; X2 r9 (S1) and X12 r4 (S2) accepted; B-S1 before B1-a and B3-b; SX-1 before B2-a | **law** (accepted); successors S1 X2 r9, S2 X12 r4, S3/S9 (B-S1), S4 (B-S2), S5 (C3), S6 (C2), S8 (T2 record); S7 is S-OP-5's | XL | FW-01, FW-13, FW-14, D15; 6 `inventory/*` cells; 7 flags; SL:3, NE:2 (§1.4), NE:9 |
| M3-C | **Sealed snapshot and Plan. Law r3 in review with CODEX2** (MC, `2e455c70…`). Units (MC "Units"):<br>- **C1a** (M): `snapshot.rs`, the capture session, walk, custody, sealing and bounds (IE:179). **C1b** (S): the VCS observation. **C1c** (S): the `node_modules` read set.<br>- **C2a** (M): closure admission and the core role closures. **C2b** (hard XL part, 5 days): the TS context and universe resolver and the layout. **C2c** (M): the Rust context functions. C2 covers NE:1255-1645 and BP:699-713.<br>- **C3a** (L): `imports.rs`, DS-1..DS-6, CRATE-ARCHIVE-1 (NE:1646-1698). **C3b** (S): the unified-features adapter, a tool launch under the D law, after D1's primitive and O7. **C3c** (M): prepared import under PO-0..PO-4 (NE:1803-1870).<br>- **C4a** (L): `plan.rs`, with `plan2` (IE:182) and the prospective-Plan bounds (NE:4276). **C4c** (S): prepared-import wiring (variant B). **C4b = X12d** (M, plus one serialized X9 lead set; X12:192).<br>- H-DEP, H-NM, H-PREP (S each): harness recipes on the K lane.<br>**Large repositories (MC item 5; O-3).** `snapshot2`'s 4 MiB descriptor holds about 27,000 rows. **S-R**, inventory by reference, is likely needed after S-M. It is conditional and unsized (see "Unsized"). | B (C1a: B2-c; C4a: B1-a, B2-c, B2-d), L, I1 (C4a: I1-c; X12d: I1-c and I1-b2), D1 (C3b), X3a-2 (C1a). **Successor gates:** CRC-1 and CR-1 before C2a; SX-1 before C1a; VCS-1 before C1b; NIJ-1 before C3a; R3 before C3c; **X12 r4 before C4a.** | **law** (gate: L accepted, X12 r4 accepted); X12d; CRC-1, CR-1, NIJ-1, VCS-1, SX-1, S-B, T2-DEP, X12-A; S-R conditional | XL | NE:3, NE:4; L-RS1, L-RS4 |
| M3-D | **Supervisor and common control.**<br>- **D1, `platform/process.rs`:** spawn with an explicit environment, no PATH, a process group and fd channels. It also builds the O7 confinement primitive. This module is the M6 DR-G22 owner (BP:1026), built early.<br>- **D2, the codecs:** `control_protocol.rs` and `provider_protocol.rs`, which own NE:10's dispatch (NE:2781-3316) with no translation (F02:168-169).<br>- **D3, `supervisor.rs`:** deadline, health, resources, tree kill, single settlement, provider cancel and candidate discard (F02:199-214; OPP §5.1). The stage-1 grace is Rust3's protocol 5,000 ms (RPP:119) for Rust, and D3's provisional 2 s for TS2 (ML item 16c).<br>- **D4, `manifest.rs` and `session_factory.rs`:** DR-G29 refusals with no ExecutionId (REG:374).<br>- **D5, the G21 controls.** OPP §10's control areas (privacy, correlation, custody, bounds, outcomes, crash, capacity, cancellation, liveness and overhead), plus three **new** confinement escape controls that extend S-OP-11 and are not in OPP §10: a network attempt, a write outside scratch and an ambient environment read.<br>**D-law** acceptance needs CF-P. D1's enforcement claim and D5's escape controls need CF-1. The D law's launch rules also govern C3b's adapter, a tool launch (MC item 12). | P0, L, CF-P (law); CF-1 (D1 claim, D5) | **law** | XL | G10 (control), G21, G29; NE:10 |
| M3-E | **Syntax crate and grammar registry. Law E1 r1 drafted, in review with Codex** (ME).<br>- **E1, law:** the backend choice (CH14:614); the `SyntaxGrammarBundleV1` closure (BP:684-688); seven languages and fourteen suffixes (NE:260-263); NE:2's syntax-only part (NE:178, NE:218-306).<br>- **The backend, a lead decision (ME items 2–3):** tree-sitter grammars compiled to Wasm and run in-host by `wasmi`, with fuel-metered, typed parse failures. Native tree-sitter is the fallback if E0 fails.<br>- **Units (ME item 20):**<br>  - **E0** (S, 2 days): a lead-run probe outside the product with six predeclared criteria. It executes no repository code.<br>  - **E2a** (M): the grammar closure lane, SYN-LANE.<br>  - **E2b** (L): `grammar.rs`, `parser.rs`, SYN-REG and SYN-DEP.<br>  - **E2c** (L): `normalization.rs`, `candidates.rs` and SYN-NS.<br>  - **E3** (M): `host/syntax.rs` (CH14:496).<br>- E2b and E2c cover CH14:372-379 and NE:7's grammar-body clones (NE:2562-2647).<br>The crate is pure (BP:676-680). | E0: — . E2a: E0, P0. E2b: E2a, C2a, CR-1, SYN-1. E2c: E2b, SYN-NS. E3: E2c, C1a, B2-c, SYN-1. | **law**; SYN-1, SYN-NS (contract successors); SYN-REG, SYN-DEP and SYN-LANE inside E2a/E2b | XL | G13 (syntax); 11 `*/syntax-only` cells; NE:2 (syntax), NE:7 |
| M3-I1 | **The X12c preview pack. Law r2 accepted by CODEX2** (MI). It covers the frozen rule IR of `module-import-cycle`; the policy-language successor, which is **needed**: one atom, `cycle-representative`, gives exactly one finding per cyclic component; the identity-contract passages that authorize that one additive op value under the existing majors (IE:213-214; IDS:4978; LD-3); and the pack contract. **Resized from M to L.** Units (MIU:28-33):<br>- **I1-L** (design, M) and **I1-P** (design, S);<br>- **I1-a** (M): schemas and regenerated enums;<br>- **I1-b1** (S): admission;<br>- **I1-b2** (L): semantics;<br>- **I1-c** (S): the row and the bytes.<br>Edges: I1-L → I1-P; I1-L → I1-a → I1-b1 → I1-c; I1-b1 → I1-b2 (MIU:35-38); **F8b → I1-a**. Downstream: **I1-c → C4a; I1-c and I1-b2 → X12d; I1-b2 → J2** (MIU:40; MC "Units"). Forbidden substitutes apply (X12:196-202). | I1-a: I1-L, X9-6 (met), **F8b**; it shares the generator with X4T-c (P5-3) | X12c contract successors (I1-L, I1-P) | L | G25 path; X12c |
| M3-F | **TS/JS provider (TS2).**<br>- **F1, transport:** NE:2944-3002 and NE:3151-3316.<br>- **F2, facts:** imports, references, calls, unresolved edges, types (NE:2347), symbols and Coverage, across three modes.<br>- **F3:** reachability and framework recognition (L-FW1), syntax facts, and NE:7's clone modes including cross-tsjs (NE:2562-2647).<br>- **F4, runtime closure:** signed Node and TypeScript with no ambient Node (F02:252), running under the O7 profile.<br>Code can be authored earlier; a provider is **launched** only after O7 and D1's primitive. **F1's first run on TS T1 fixtures waits for K2a's oracle freeze** (HD §13, QD-26). | Authoring: C1, C2, D2. **F1 integration: C1a, C2b, D3** (MC r3, narrowed). Launch: D1 primitive, D3, O7. | none expected (BP:717) | XL | G10, G13, G14 preparation; 33 TS/JS cells; NE:7, NE:10 frames |
| M3-G | **Rust provider (Rust3).**<br>- **G1a:** snapshot transport and `context.rs`.<br>- **G1b:** dependency and prepared frames (NE:2872-2943).<br>- **G2:** `compiler_adapter.rs`, the `rustc_driver` sidecar (`12-architecture-completion-goal.md:145`) with the rust-dev-llvm closure (NE:1445). It is **authored** after S-P. **G2-v** is its lawful launch and validation under the O7 profile, after O7 and D1's primitive. It is not D1's enforcement claim, which needs CF-1.<br>- **G3:** inventory, facts and Coverage for L-RS1..L-RS3 (NE:1793).<br>- **G4:** prepared-mode consumption (L-RS4, PO-1..PO-4) and NE:7's clones. | **G1a: C1a, C2c, D3** (MC r3, narrowed). G1b: G1a, C3a–C3c. G2 authoring: S-P. G2-v: O7, D1. G4: G3, G1b, C4c. | none expected (BP:717) | XL | G10, G13, G14 preparation; 22 Rust cells; NE:7, NE:10 frames |
| M3-H | **Fact admission:** the syntax, context, occupancy and Coverage joins (`fact_admission.rs:1-3`); relation-registry and Coverage-domain refusals (REG:368); a missing rung is indeterminate (REG:370). Framing grants no fact authority (CH14:482). H admits what I1-b2 reads: `imports` and `unresolved-edge` facts, occupancy, the imports symbol inventories, and the exact scopes (MI item 8). The full `admit_enumeration`, over the **actual** inventories, runs after execution in J2's pipeline with H's admission (MC item 16, C2-R1). | C4a; E3 or F1 | **law** | L | G23, G25; NE:5 |
| M3-J | **Guarded durable host pipeline.**<br>- **J1, law:** the X11 successor (X11:64-81), including X11 r1 item 1a's first-use conflict; the invocation DAG (WS:76-256); the backup-status successor; and the commit-phase cancellation join S-OP-12 with the X3D and X7 owners (OPP §5.5, §9).<br>- **J2, `invocation.rs`, `analysis.rs` and the `outcomes.rs` NE:11 work:** the deficiency-cause carriers, precedence and D9 bridge (NE:3317-3858); the full enumeration admission (MC item 16); the ephemeral path end to end. No durable write.<br>- **J3, durable:** through X7 finalization and the commit; `workflow_tests.rs`. It lands after **X3c-3**, which lifts the re-commit refusal (EXIT:171).<br>- **J-RW, law** (P5-1): the resume/repair writer's successor to X2 item 8, X3c item 10 and the X4T dependency-publication rule, with its X9 coverage rows.<br>- **J4, the resume/repair writer** (EXIT:186-191; M2C §4.1, L11), plus one serialized lead set for its X9 rows. **J4 no longer waits for J3.**<br>- **X3c r8, law, and X3c-3, storage code** (P5-2): re-commit of a Run already committed in the same store and namespace, plus its X9 storage-row rerun. | J2: H, C4a, C4c, X12d and its lead set, D3, CF-2, I1-b2, X4-F1, X4-F2. J3: J2, F2, G3, X3c-3. J4: J-RW. X3c-3: X3c r8. | **law** (J1); backup-status successor; **X3c r8**; **J-RW**; S-OP-12 | XL | G25; NE:11, NE:14, NE:15; FW-03, FW-08; WS:2 |
| M3-I2 | **Draft catalog, non-authoritative.** `PolicyDocumentV2` rules (AQP:173-199), evaluated only in the harness over admitted facts (AQP:500). The product pack stays at M5 (D2, AQP:542). I1-L's reference model is the harness oracle for `module-import-cycle` (MI item 8). | H, Q0 | none at M3 | M | Q2–Q4 exploratory |
| M3-K | **Quality harness and T1** (HD §13).<br>- **K1:** K1a (M) is the case and ledger libraries, digests, the freeze, `corpus fetch` and the store. It may need a chunked tree digest. K1b (S) is the confidence module. K1c (M) is the run driver and determinism driver (AQP:324-327).<br>- **K2:** T1 in three lanes, 57, 6 and 3 cells (AQP:500; AQ:233-234), **16 days**. K2b (Rust, 5) and K2c (syntax, 3), each with its one-day review and freeze, run **before day 0**: 10 days after Q0. K2a (TS/JS, 5) and its freeze run on **days 0–6**. Each lane's oracle is frozen before any producer runs on that lane's T1 fixtures (QD-26). | Q0 (met), T2b (met) | D13 | XL | Q1, Q4, G13 |
| M3-M | **Exploratory measurement and the dogfood checkpoint:** Q1/Q4 on T1; Q2–Q4 through I2; the determinism suite; Q6 core analysis kept separate from first use and from preparation-invalidating edits (AQP:359-366); T3, now that the licence has landed (AQP:555; D6 at AQP:547). T3's multi-repo instance waits on OQ-1 (MB item 27). **This plan's rule, not AQP's:** the exploratory report may close while adjudication of gating and repair-eligible findings is still pending. Those strata are reported as not yet adjudicated. Strata with too few findings are INSUFFICIENT-EVIDENCE (AQP:244). Any later Q2 use still requires every such finding adjudicated (AQP:236), with unclear labels resolved by the human expert (AQP:254). Large T2 repositories that refuse at `snapshot2`'s bound before S-R are reported as refused (MC O-3). | J3, G4, F3, E3, I2, K1, K2, O1 | none | L | Q1–Q6 exploratory |
| M3-O | **Operability.**<br>- **O1:** `tracing`, the S-OP-2 vocabulary, nonpersistent sinks, the bounds, phase spans and the operational record with INC-8's reuse disclosure (OPP §3.1-§3.3, §4.1), plus the enforcement checks (OPP §7).<br>- **O2, each part gated:** S-OP-1, S-OP-7, S-OP-8, S-OP-5 and S-OP-6. **Lead rule:** M3-X requires each O2 part whose successor is accepted by then. A part whose successor is not yet accepted is recorded as carried to M4. M3-X is not held for it.<br>- **O3:** the G20/G21 controls (OPP §10, plus D5's escape extension).<br>S-OP-2 is at r3 with Codex (SOP2). | P0; S-OP-2 | S-OP-1, -2, -5, -6, -7, -8, -11 (OPP §9) | L | G21; G20 controls (M5 row, BP:1024) |
| M3-R | **Third-language readiness review** with Python, and the onboarding kit (AQP:467-489). | L, F2, G3, K2 | record only | M | O8, D9 |
| M3-X | **Exit gate.** BP:887's completion checks on this host's profile: the seven gates prepared, both languages present, and the O7 implementation in place. | M3-M, B3-c, D4, D5, E3, F4, CF-2, J4 (and its X9 rows), O1, O3, R; O2 parts per the O-row rule; X4-F1 and X4-F2 (through J2) | none | L | all M3 gates |

**M2 carry-ins: owners, sizes and gates (r5).**

| Item | Source | Owning unit | Size | Must land | Decision |
|---|---|---|---|---|---|
| **F8b**, the generator-closure and TS lane-registry re-pin | M2C §5 row 2; F8B | M2 follow-up (lead; CODEX2 reviews) | M, plus its machine steps (rebuild, drift gate, equivalence probe) | after Grok's rerun on C; before I1-a and X4T-c. The I1 bound below allows **day 10** at the latest | accepted r2; execution pending |
| **X4T-c**, two continuation codes | M2C §5 row 15 | contract successor plus regeneration | M | after F8b; not concurrently with I1-a | M2C row 15; order P5-3 |
| **X3a-2**, read-side adoption of the selected endpoint | M2C §5 row 13; X3a r5 items 4, 8 | post-M2 unit | M (inventory successor) | before C1a, so by **day 10** | M2C row 13 |
| **X4b**, `admit_repo_execution_grant` | M2C §5 row 14 | B3-a (`grants.rs` records only) and M5-EX | — at M3 | not an M3 code item | M2C row 14 |
| **X4-F1**, observer reread expiry (a real defect) | M2C §5 row 16; ON ("X4-F1 written") | X4T-a successor | M (written: 10 files), plus full lanes and one lead run set (the 43 tick-armed storage rows, X9-4's remaining rows, 13 checkpoint kills, 4 host rows, both censuses) | before J2, so by **day 22** | M2C row 16; gate P5-4 |
| **X4-F2**, the same expiry gap in the fenced read | ON ("X4-F1 written") | X4T successor | provisional M plus one lead set (no draft yet) | before J2 | P5-4 |
| **F9**, test fixture dates that expire on 2026-12-30 | ON ("X4-F1 written") | test-only unit | provisional S (no draft yet) | by **2026-12-01** (calendar) | P5-5 |
| **Resume/repair writer** (L11) | EXIT:186-191; M2C §4.1, §5 row 10 | **J-RW** (law) and **J4** (code) | law ≤ 5 days; J4 L plus one lead set | J-RW before day 0; J4 before M3-X | P5-1 |
| **X3c successor** (re-commit) | EXIT:171; M2C §5 row 11 | **X3c r8** (law) and **X3c-3** (storage code) | law ≤ 5 days; X3c-3 M plus one lead set | before J3, so by **day 25** | P5-2 |
| X11 successor | X11:64-81; M2C §5 row 7 | J1 | — | J law | r4 |
| X12c / X12d | X12:191-192 | I1 / C4b | L / M plus a lead set | — / before J2 | r4 |
| Licence unit | AQP:555 | **done**: L1, `2967905` (v134) | — | — | — |

**Why these splits.**

- **B and C:** discovery answers to SL S3 and D15's successor; the snapshot answers to identity.
- **C, split by its law (MC "Units"):** C1, C2 and C3 have three sub-units each, and C4 has C4a, C4c and C4b. C4a still binds every input of `plan2` (IE:182), and the host owns resolved inputs before the PlanId (NE:2497-2499). C4c only wires prepared imports, so non-prepared Plans need not wait for C3c.
- **C3 and G1b/G4:** the host admits dependency and prepared sets (NE:1704-1712); the provider consumes them.
- **G1a and G1b:** splitting the snapshot frames from the dependency frames lets the Rust transport start on C1a instead of waiting for C3.
- **I1's product units:** I1-c (the row) feeds C4a. I1-b2 (the semantics) feeds X12d and J2. Under LD-11, I1-c may land before I1-b2, because the op stays a structural refusal until then (MI §9).
- **I1 and I2:** I1 is a mandatory input of every real Plan (X12:125, X12:134; `policy.rs:1401`). I2 is exploratory only.
- **CF:** O7's successors have different owners from supervision (REG:317).
- **J-RW and J4 apart from J3:** L11's crash states are made by M2 code (first registration, owner creation, the ledger's WAL), not by J3. The writer needs those owners' successors, not the durable pipeline.

## Critical path and parallel lanes

**Day 0 is M3-L's acceptance.** Because O7 and S-M are in L's gate, both are done by then.

**Assumed done before day 0** (not sized here):
- **Laws and successors:**
  - the D, E, H and J laws, J-RW and X3c r8, with D-law acceptance after CF-P;
  - the B law (accepted) and its successors X2 r9, X12 r4, B-S1 (with SX-1) and B-S2.
  - X12 r4 lands with B1-a (MB item 25), which starts on day 0 on the host chain, so it is **needed by day 0**.
- **P0 landed.**
- **I1's product units,** or at least I1-c by day 16 and I1-b2 by day 19 (below).
- **G2 authored.**
- **K2b and K2c,** with their freezes.
- **X3a-2, X4-F1 and X4-F2,** or by their bounds in the carry-in table.

**The C law is the exception.** MC's acceptance gate requires M3-L accepted, so the C law is accepted at or after day 0. The DAG tolerates this:
- CRC-1, CR-1 and the C law by **day 5**, since C2a must start by day 5 for C2b to finish before C1c at day 12;
- SX-1 by **day 2**, B2-a's slack. SX-1 lands with B-S1, so in practice it is accepted with B's design units before day 0;
- VCS-1 and NIJ-1 by day 12;
- R3 by day 15.

**Durations are planning assumptions:**
- a code sub-unit takes 1 day for S, 2 for M, 3 for L and 4–5 for a hard XL part, including build, review and integration;
- a successor law takes about 3 rounds, bounded at 5 days;
- one lead run set at a time, 1 day each where a unit needs one;
- edges are **integration** edges (MC "Units").

**r5 timing (variant B, the recommended C4 split; MC "Units").**

| Sub-unit | Days | Integration after | Finishes (day) |
|---|---|---|---|
| B1-a → B1-b | 2 + 2 | — / B1-a | 2 / 4 |
| B3-a; B2-a | 1; 2 | —; — (SX-1) | 1; 2 |
| B2-b → **B2-c** → B2-d | 3 + 3 + 2 | B2-a, B1-b, B3-a / B2-b / B2-c | 7 / **10** / 12 |
| B3-b → B3-c | 3 + 2 | B2-c (B-S1) / B3-b, K1a, S8 | 13 / 15 |
| C2a → C2b; C2c | 2 + 5; 2 | — (CRC-1, CR-1) / C2a; C2a | 2 / 7; 4 |
| C1a | 2 | B2-c (SX-1, X3a-2) | 12 |
| C1b; C1c | 1; 1 | C1a (VCS-1); C1a, C2b | 13; 13 |
| C3a | 3 | C1a (NIJ-1) | 15 |
| C3b | 1 | C3a, D1 (O7 and the D law by day 0) | 16 |
| C3c | 2 | C3a (R3) | 17 |
| C4a | 3 | C1b, C1c, C2b, C2c, C3a, C3b, B1-a, B2-c, B2-d, I1-c (X12 r4) | 19 |
| C4c | 1 | C4a, C3c | 20 |
| X12d (C4b), then its X9 lead set | 2, then 1 | C4a, I1-b2 | 21, then **22** |
| CF-1 → CF-2 | ≤ 5 + 2 | O7 (≤ day 0) / CF-1 | ≤ 5 / ≤ 7 |
| D1 (with the primitive) → D2 → D3 | 2 + 2 + 3 | — | 2 / 4 / 7 |
| D4; D5 | 2; 3 | D3; D3 and CF-1 | 9; 10 |
| E0 → E2a | 2 + 2 | — / E0, P0 (both may finish before day 0) | ≤ 0 |
| E2b → E2c → E3 | 3 + 3 + 2 | E2a, C2a (CR-1, SYN-1) / E2b (SYN-NS) / E2c, C1a, B2-c | 5 / 8 / 14 |
| F1 → F2 → F3 | 3 + 4 + 3 | C1a, C2b, D3 (launch: D1, O7; first T1 run: K2a's freeze) | 15 / 19 / 22 |
| F4 | 2 | F1, D1 | 17 |
| G2-v (launch and validation under the profile) | 1 | D1 (O7 by day 0) | 3 |
| G1a → G1b | 3 + 2 | C1a, C2c, D3 / G1a, C3a–C3c | 15 / 19 |
| G3 → G4 | 5 + 3 | G1a, G2-v / G3, G1b, C4c | 20 / 23 |
| H | 3 | C4a, F1 | 22 |
| I2 | 2 | H, Q0 | 24 |
| J2 → J3 | 3 + 3 | H, X12d and its lead set, C4c, D3, CF-2, I1-b2 (X4-F1, X4-F2) / J2, F2, G3, X3c-3 and its rows | 25 / 28 |
| X3c-3, then its X9 rows | 2, then 1 | X3c r8 (≤ day 0) | 2, then 3 |
| J4, then its X9 rows | 3, then 1 | J-RW (≤ day 0) | 3, then 4 |
| K1a → K1b → K1c | 2 + 1 + 2 | Q0, T2b (both met; it may run before day 0) | 2 / 3 / 5 |
| **K2 (T1, three lanes; HD §13)** | 16: 10 before day 0 (K2b, K2c and their freezes), 6 on days 0–6 (K2a and its freeze) | Q0 | **6** |
| O1; O3 | 4; 3 | P0 and S-OP-2; O1 and D5 | 4; 13 |
| O2 parts | successor-gated | each S-OP | carried to M4 if unaccepted (O-row rule). **O2_selected** is the latest finish of the O2 parts the O-row rule keeps in M3, or 0 when none is kept. |
| R | 2 | F2, G3, K2 | max(20, K2) + 2 = 22 |
| M3-M | 3 | J3, G4, F3, E3, I2, K1, K2, O1 | max(28, K2) + 3 = 31 |
| M3-X | 2 | M3-M, B3-c, D4, D5, E3, F4, CF-2, J4 and its rows, O1, O3, R, O2_selected | max(M3-M, R, 17, O2_selected) + 2 = 33 |

**Conditional host-chain duration: 33 days.**

> B1-a → B1-b → B2-b → B2-c → C1a → C3a → C3b → C4a → H → J2 → J3 → M3-M → M3-X

That is 2 + 2 + 3 + 3 + 2 + 3 + 1 + 3 + 3 + 3 + 3 + 3 + 2 = 33. A second branch has zero slack: C4a → X12d → its X9 lead set → J2, reaching J2 on day 22, the same day as H.

It holds only if all of the following hold, in addition to the day-zero assumptions above:
- **K2** finishes by day 28. Q0 gives 6, so this holds by construction unless K2a's freeze slips (next item).
- **K2a's freeze** slips by at most 10 days. Q0's rule is recomputed for r5: M3-X = 33 + max(0, *s* − 10), for a freeze slip *s* past day 6. F1 starts on day 12, so the freeze has 6 days of margin. H then waits for C4a until day 19, which gives F1 4 days of slack. Q0's r4-era rule, 26 + max(0, *s* − 3), is superseded.
- **O2_selected** finishes by day 31. The late branches are compared by their **arrival at M3-X**: max(28, K2) + 3 against O2_selected.
- **X12d's X9 lead set** is complete by day 22, with no other lead run set holding the machine on days 21–22.

**Branch slack:**
- C4c finishes on day 20 and J2 starts on day 22: 2 days.
- F1 (15) has 4 days against H, which starts on day 19.
- I2 (24) has 4 days against M3-M, which starts on day 28.
- The Rust branch has 5 days: G3 (20) against J3, which starts on day 25, and G4 (23) against M3-M.
- F2 (19) and F3 (22) have 6 days.
- C2b (7) has 5 days against C1c.
- B2-a has 2 days and B3-a has 3 against B2-b.
- R (22) has 9 days. E3 (14) has 14. B3-c (15), O3 (13), F4 (17), J4's rows (4) and X3c-3's rows (3) have more.

**Why 33, and not 26, 28 or 31.**
- **r4's 26** used one-row C units and B2 finishing on day 5.
- **MC r2's 28** split C, but kept r4's B rows. Its figure reproduces under those rows: CODEX2 confirmed the 29/28-day figures (`reviews/codex2-snapshot-plan-c-r2`, C-R4 disposition).
- **MC r3** expresses the chain as **b + 23 days**, where b is the day B2-c finishes (MC "Units").
- **b = 10** from MB's accepted unit table at this plan's durations: B1-a (2) → B1-b (2) → B2-b (3) → B2-c (3). B2-b waits for B2-a, **B1-b** and B3-a (MB:847).
- **MB's F14 says "about day 8"** (MB:805). That counts B2-a → B2-b → B2-c (2 + 3 + 3) and omits B2-b's integration edge on B1-b, which MB's own table states. At b = 8 the chain would be 31.

**Variants and rejected alternatives:**
- **Variant A, C4 unsplit:** C4a also waits for C3c, so it finishes on day 20, and the chain runs through C3c: **34 days**. Rejected (MC's recommendation, adopted as P5-6).
- **Rust context minting inside C2c,** waiting for C3b: **30 days in both variants at b = 5** (MC r3, C2-N1), so 35 here. Rejected in MC.
- **Full C1/C2 rows as F1 and G1a edges:** F1 and G1a finish on day 16, F2 on 20, G3 on 21 and G4 on 24, all inside slack. 33 is unchanged.
- **J4 after J3,** as in r4, at J4's r5 size: J3 (28) → J4 (31) → its rows (32) → M3-X **34**. Rejected (P5-1).

**I1 and F8b bounds.** The I1 product chain does not wait for P0 or L, so it is expected before day 0. If it is late, it moves nothing as long as I1-c lands by day 16 and I1-b2 by day 19, X12d's start. From F8b's finish *f*:
- with X4T-c first, I1-c lands at *f* + 6 and I1-b2 at *f* + 8, so F8b must finish by day 10;
- with I1-a first, I1-c lands at *f* + 4 and I1-b2 at *f* + 6, so F8b must finish by day 12.

**The whole-M3 total is left uncomputed.** These are still unbounded:
- the O7 decision date, which is outside the lead's control;
- the parallel pre-day-0 law and successor rounds (L, D, E, H, J, J-RW, X3c r8, X2 r9, X12 r4, B-S1, B-S2), each bounded at 5 days, but contending for reviewers;
- the pre-day-0 machine queue (P5-8);
- the O2 parts;
- S-R, if S-M shows it is needed.

K2 is no longer on this list: Q0 bounds it.

**The bounded pre-day-0 work:**
- T2 and Q0: **done**;
- K2b and K2c with their freezes (10, from Q0's acceptance);
- S-M (2), a lead run set;
- S-P (1), then G2 authoring (4);
- CF-P (2);
- E0 (2), then E2a (2, after P0);
- F8b (2, plus machine), then X4T-c (2) and the I1 chain (I1-a 2, I1-b1 1, I1-c 1, I1-b2 3);
- X3a-2 (2);
- X4-F1 (2, plus its lanes and one lead set);
- L acceptance (about 2, once its gate is met).

Recompute the total when O7 is decided, when MC is accepted (if its units change), after S-M, if S-P or CF-P fails, and if S-R becomes needed.

**Calibration only:** M2's exit integrated 62 product commits from `d4239a5` to `3e64266`, 60 of them up to C (`git rev-list --count`; M2C §3.2). Those were mostly smaller mechanism units.

**Effort.**
- **About 39 law, successor or record units:**
  - **laws:** L, the B, C, D, E, H and J laws, J-RW and I1 (B and I1 are accepted);
  - **law amendments:** X2 r9, X12 r4 and X3c r8;
  - **other successors:** CF-1, CF-2, backup-status, S-OP-1/2/7/8/12 and D13;
  - **contract successors and records:** B-S1, B-S2, S5, S6, CRC-1, CR-1, NIJ-1, VCS-1, S-B, T2-DEP, X12-A, I1-L, I1-P, S8, SYN-1, SYN-NS, F8b and X4T-c.
  - S-R is conditional.
- **About 76 code, harness or probe sub-units:**
  - P0;
  - B: 9;
  - C: 12, plus 3 harness recipes;
  - D: 5;
  - E: 5 (E0, E2a, E2b, E2c, E3);
  - I1: 4;
  - F: 4;
  - G: 6;
  - H;
  - J2, J3, J4 and X3c-3;
  - I2;
  - K: 6 sub-units and 3 lane freezes;
  - M3-M, O1, O3, R and M3-X;
  - CF-P, S-P and S-M;
  - X3a-2, X4-F1, X4-F2 and F9.

That is roughly 115 reviewed units, against r4's 63. Most of the growth is the B, C, E and I1 laws' own unit breakdowns. M5-EX (below) is M5 work.

**Lanes:**

| Lane | Units | Reviewer (suggested; actual so far) |
|---|---|---|
| Host core (the critical path) | B → C → H → J | B: GROK2 (law accepted). C: CODEX2 (law r3 in review). H and J: Grok. |
| Components and confinement | D, CF, F1/G1 conformance | Codex |
| Rust compiler | S-P → G2 → G3 → G4 | CODEX2 |
| Syntax and TS analysis | E → F2/F3/F4 | E1 law: Codex (r1 in review). Code: GROK2. |
| Preview pack and M2 carry-ins | F8b → X4T-c and I1-a → I1-b1 → I1-c, I1-b2; X3a-2; X4-F1, X4-F2; X3c r8 → X3c-3; J-RW → J4; F9 | I1: CODEX2 (its law reviewer). M2 carry-ins: Grok (the M2 law reviewer). |
| Quality and operability | K1, K2 lanes, I2, O, R, M3-M | the next free reviewer. K2b and K2c come first, because they are pre-day-0. |

**Lead run sets stay serialized.** The crash matrix has a 5000 ms timing guard (the subject of product commit `eb0d503`), and measurement needs a quiet machine. The order before day 0 is P5-8. After day 0, the run sets fall on X3c-3's rows (day 3), J4's rows (day 4), X12d's lead set (day 22, zero slack) and M3-M's measurement (days 28–31).

**Next, in order.** Product crates are open now that X9-6 is in.
1. **On the machine:** Grok's rerun on C, then F8b's cargo steps, then X4-F1's lanes and reruns, then S-M (P5-8).
2. **Unblocked now:** P0; X3a-2; K1, with K2b and K2c's oracle work; S-P, CF-P and E0, between run sets; the I1 design units I1-L and I1-P.
3. **Drafting:** M3-L r2, which fills ⟨SM-n⟩ after S-M and updates its gate rows; the D, H and J laws; J-RW; X3c r8; X4T-c's successor; X4-F2.
4. **In review:** M3-C r3 (CODEX2), M3-E1 r1 and S-OP-2 r3 (Codex), X2 r9 and X12 r4 (queued for Grok after the rerun), and M2C (GROK2).

## M3-L gate status (2026-10-04)

ML's gate table was written on 2026-10-03, before T2b and S-OP-2 existed. Its next revision must refresh it (ML "Acceptance gate").

| # | Gate item (r4 M3-L row) | Status | Evidence |
|---|---|---|---|
| G1 | S-M measured | **open.** Not started. It is a lead run set behind Grok's rerun, F8b and X4-F1 (P5-8), and its report also waits for the D13 sign-off. | ML G1; ON |
| G2 | T2 complete (T2b) | **met.** GROK2 accepted T2b: 49 repositories. | `reviews/grok2-corpus-t2b-r1/status.json`; T2R:24 |
| G3 | Q0 | **met** (r13) | HD:3 |
| G4 | D3 sign-off | **open: owner (B3)** | AQP:543 |
| G5 | D13 sign-off | **open: owner (B3).** Its mechanisms were accepted in Q0 r13. | AQP:554; HD OI-1 |
| G6 | D2 draft | **met on the lead's reading** (Q0 §2). The sign-off is separate. | ML G6; AQP:542 |
| G7 | S-OP-2 drafted | **met.** The drafts exist. r1, r2 and r3 each received required findings from Codex (r3: `reviews/codex-s-op-2-r3/status.json`, REQUIRED-FINDINGS), and r4 is in review. | ON; `reviews/codex-s-op-2-r3/status.json` |
| G8 | O1 | **decided in ML item 11** (lead decision). It becomes final when L is accepted. | ML G8 |
| G9 | O7 decided | **open: owner (B1)** | ON B1 |

**Before L can be sent:** S-M, the two sign-offs and O7. Then ML r2 fills every ⟨SM-n⟩ and re-pins its citations (`reviews/grok-provider-protocol-l-r1/REQUEST.md`, "Before sending").

## Choices left open, with lead recommendations

**Already decided; cite, don't reopen:**

- **Owner decisions:** D4, D5, D6, D9 timing, D10, D11, D14, D15 and D16 (AQP:544-557).
- **Evaluation and dogfood:** catalog evaluation is non-authoritative at M3 (AQP:500), and CLI dogfood is at M4 (AQP:502; BP:887).
- **Protocols and crates:**
  - the protocols are TS2 and Rust3 (BP:717);
  - the Rust substrate is `rustc_driver` (`12-architecture-completion-goal.md:145`);
  - `crates/syntax` is pure (BP:676-678).
- **Carried in from M2:** no creator command in M2 (X11:18); X12c and X12d at M3 (X12:191-192).
- **Python:** the support decision comes after M3's review (AQP:465).
- **Decided in accepted unit laws tonight:** I1's IR and LD-3 (MI); B's D15 shape and discovery ledger (MB).

The lead decides each choice below in the named unit's law, and a reviewer checks it.

- **O1 (M3-L).** Decided in ML item 11: (a), existing admitted observations only (OPP §3.6). Rejected: a new frame, which needs S-OP-3 and both protocol joins.
- **Syntax backend (E1; CH14:614).** Decided in ME items 2 and 3 (r1, in review): tree-sitter grammars compiled to Wasm, run in-host by `wasmi` with fuel-metered, typed parse failures. E0 chooses by six predeclared criteria. If it fails, the grammars are linked natively under BP:680-682's TCB statement, and the lead re-decides placement before CLI `analyze` takes untrusted input at M4 (ME item 18).
- **Dependency sources at M3 (C3).** Decided in MC (r3, in review): a library-level import of user-named sources (NE:1681-1691), driven by the harness, with `.crate` archives decoded only under CRATE-ARCHIVE-1. The `import` command stays at M5 (BP:957).
- **Prepared mode at M3 (C3, G4).** Decided in MC (O-1): `imported-descriptor` sets from the harness recipe (NE:1806; NE:2533-2537). T2 measurement of the five `rust-cargo-prepared` cells waits for M5's authorized preparation. `native-prepare` stays at M5 (BP:992). No repository code runs at M3.
- **DR-G14 placement (M3-L).** The gate is M3 (COV:4770), but its owner module is M5 (owner string COV:4772; first milestone COV:8976). Recommendation: M3 prepares closure manifests and no-ambient-runtime refusals (F4, G2); installation stays at M5.
- **Public CLI (J1).** Recommendation: nothing is wired. J1 fixes the order and identity rules (BP:887-888).
- **Changed-scope (M3-L).** Recommendation: none ships. ML item 4 found that cross-edit reuse needs an IE successor (the INC-1 successor), because `cache2` binds the Plan. It is owned by the identity owner (AQP:546) and decided at M4 with S-M's data (AQP:502).
- **Stage-1 cancel grace (M3-L item 16c; D3).** Rust3 keeps its protocol's 5,000 ms (RPP:119). TS2 uses D3's provisional 2 s. OPP's cancellation goal (p95 ≤ 2 s) may be missed by Rust3 without a second signal; it is a goal, not a threshold.
- **Logging (O1).** Recommendation: `tracing` with one host-owned subscriber and no environment input (OPP §3.1, §3.5).
- **Platform scope (M3-X).** Recommendation: run and claim only this host's macOS family (NE:157-160). The Linux confinement code is built but exercised only on Linux lanes.

## O7: hostile-input confinement (owner decision, pending)

**Status.** O7 is an owner decision (OPP §5.6, §9) and is **pending** (ON blocker B1). It is a **hard prerequisite of M3-L and of provider launch**: no provider (F, G, G2-v) launches, and C3b's adapter does not run, until O7 is decided and D1's primitive exists. Authoring may start earlier. This keeps OPP §8's schedule.

**The lead's recommendation, as put to the owner:**

1. **Analysis never executes repository code by default.** Existing law already says this: "Repository execution is disabled by default" (SL:1059), and the Rust worker's `workerExecutesRepositoryCode` is the constant `false` (NE:2534-2535).
2. **Providers run under OS confinement:**
   - on Linux and AL2023: Landlock, seccomp and no network;
   - on macOS: a Seatbelt profile that denies network access and any write outside the provider's scratch space.
3. **Where confinement is unavailable,** the result discloses it, and the documentation requires containers for untrusted pull requests.
4. **Executing repository code** (Rust build scripts and proc-macros in prepared mode) requires the existing `RepoExecutionGrantV2` (SL:1071) and runs only inside confinement or a container.

**Why it needs successors.** Accepted law currently disclaims confinement:
- "confinement is never claimed" (SL:1113);
- "No confinement is claimed" for unconfined children (SL:497);
- "No process/WASM boundary is claimed as a sandbox" (AQ:344);
- "No sandbox is claimed" (NE:2554);
- G21 "does not claim security confinement" (REG:366);
- DR-128 holds the sandbox boundary (REG:317).

Items 2 to 4 add enforced hardening and a disclosure. They must stay distinct from a sandbox claim for untrusted code, which only DR-128 could open.

**Units and successors it needs (all in M3-CF unless noted):**

- **CF-P, the feasibility probe,** before D-law acceptance: a programmatic Seatbelt trial on macOS 27, plus a desk check of the Linux primitives.
- **CF-1, the confinement successor** (owners: product security and platform owners, the DR-128 row's owners, REG:317):
  - an SL S10 and S6 successor with the per-platform enforcement matrix and the honest wording;
  - an AQ §5 item 4 disposition;
  - a DR-128 record saying this opens no untrusted-code scope.
- **CF-2, the disclosure carrier:** a WS output successor, or an S-OP-6 join, for "provider ran unconfined: <reason>". It sits beside Coverage and never inside it.
- **D1, the confinement primitive:**
  - a macOS Seatbelt profile applied at spawn;
  - Landlock, seccomp and a network namespace on Linux, built at M3 and exercised on Linux lanes.
- **D-law:** the single owner of the launch rules under O7. M3-L and MC cite it.
- **D5 and S-OP-11:** three new escape controls (a network attempt, a write outside scratch and an ambient environment read). They extend OPP §10, which does not contain them.
- **F4 and G2:** the provider closures run inside the profile (Node, the `rustc` temporary directories).
- **M4:** the container guidance in the runbook (OPP §6).
- **M5-EX, a gated M5 successor package for item 4.** All three successors must be accepted before M5's `execution.rs` (`native-prepare`, `test-run`; BP:974, BP:992) claims any confinement or container enforcement. X4b's `admit_repo_execution_grant` lands with it (M2C §5 row 14).
  1. **The native §5.2 admission and disclosure join.** Today, `AuthorizedExecutionV2` effects are copied from PTT, and a record claiming more is refused: network, subprocess and filesystem write are `DISCLOSURE-ONLY` (NE:2440-2444; the reference admission is NEM:2170-2172). The mandatory human and JSON sentence says OpenSIP "does not prevent network access or other effects on this platform" (NE:2480-2487; NEM:2181-2182). The successor moves only the measured platform and effect cells and the sentence that depends on them.
  2. **The WS §7 test-execution schema join.** `ENFORCED-PLATFORM` is not in `EnforcementValue`, and admitting it "requires a successor truth-table profile and test-execution schema" (WS:1071-1081; TES:7-14). The test pre-spawn sentence also changes.
  3. **A measured permission truth-table profile succeeding PTT,** owned by the security owner (S10). Only cells measured on a platform move (NE:2480-2481).

  No new native carrier major is assumed where the existing vocabulary suffices. Until M5-EX is accepted, M5 execution keeps today's disclosure-only behaviour.

**Boundaries kept:**
- **No repository-code execution in M3.** Prepared sets are imported (C3).
- **The worker prohibition stands:** `workerExecutesRepositoryCode` is constant `false` (NE:2534-2535).
- **DR-128's untrusted-code scope stays closed.** Untrusted native or WASM components are not admitted, and no process boundary is claimed as a sandbox (AQ:344; REG:317). Items 2 to 4 are hardening and disclosure for first-party providers and trusted repository code, not an admission path.

**Risk.** Whether Seatbelt can be applied programmatically on macOS 27 is unverified. CF-P decides it before the D law is accepted. If it fails, item 3's disclosure path applies on macOS, and the D law records that.

## Owner decisions

**Pending: the overnight blockers (ON, "Blockers for the owner").**

| # | Decision | What it blocks | Lead recommendation |
|---|---|---|---|
| B1 | **O7**, hostile-input confinement | M3-L acceptance (G9), so day 0; provider launch; C3b's adapter; CF-1 and CF-2; M5-EX | As in "O7" above |
| B2 | **The gating precision bar** (the quality plan's D4 revisit; HD §5.6, HD §5.8 and OI-3) | Q2 acceptance for **gating** rules only. Nothing in M3's DAG, and not M3-X. | The accepted gating floor is a 95% cluster-aware lower bound ≥ 0.99, which needs k_min = 299 independent zero-error families (HD §5.6, §5.8). The lead recommends observed precision ≥ 0.99 plus a lower bound ≥ 0.95; with zero errors, 59 families meet that 0.95 bound. Rules graduate from advisory to gating as evidence from T2 and T3 accumulates. **Note:** T2 has 10 held-out families (T2R:296), so no rule can meet either bar on T2 alone (HD OI-3). |
| B3 | **The D3 sign-off** (the T2 selection) and the **D13 sign-off** (the exploratory envelope) | M3-L gate items G4 and G5, so day 0. D13 also gates S-M's report. | Approve as reviewed: T2a and T2b are accepted by GROK2; ENV was accepted inside Q0 r13. |
| B4 | **OQ-1:** the owner's real workspace on disk (MB item 27) | Nothing. It sharpens D15's admitted shape and T3's multi-repo instance. | MB r2 admits a non-repo root with 1–64 disjoint conventional Git member repositories. Members are declared by explicit roots or by the Cargo patch and npm `workspaces` readers. |

**Other owner items:**
- **Sign-offs D2 and D12** (AQP:542, AQP:553). D12 is on S-M's Q6-labelled samples.
- **FYI:** the Wasm syntax backend needs a pinned wasi-sdk build toolchain (ON, "M3-E1 r1 drafted"; ME).
- **O4, OTLP** (OPP §4.2, §9): an M5 matter.
- **O9, raw provider stderr capture** (OPP §9; owner sign-off). Recommendation: not at M3.
- **Lead decisions flagged for possible reversal** (none blocks):
  - MC O-1 to O-3;
  - MB's "no consent flag for D15" and "a launch inside a member selects that member";
  - M2C's four carry-in decisions;
  - this revision's P5-1 to P5-8.
- **Owner actions:**
  - adjudication expert time (AQP:254). It does not hold M3-X.
  - T3: the licence has landed and D6 allows it (AQP:547). Its multi-repo instance waits on OQ-1.
  - signing keys for real-machine runs (EXIT:112). They are not needed for M3 exit, where tests use labelled synthetic closures.

## Lead decisions

**Recorded tonight in other records** (cited, not re-decided here):

| Decision | Recorded in |
|---|---|
| **I1 LD-3:** the `cycle-representative` op value widens in place, under an identity-contract passage successor. Rejected: a major bump, with its cascade. | MI §9; ON ("M3-I1: CODEX2's r1") |
| **I1 LD-11:** I1-c may land before I1-b2. | MI §9 |
| **F8 split:** F8a, the policy rows, is integrated at `3e64266`. F8b is the generator and lane re-pin, and it comes before I1-a. | ON ("F8 split"); M2C §5 row 2 |
| **D15's shape:** a non-repo root with 1–64 conventional Git members, with no consent flag. A launch inside a member selects that member. Discovery runs after the fence, on its own ledger profile. | MB items 12, 19, 23, 27 |
| **The first-use clause:** "before any project-scoped effect". X11 r1 item 1a's conflict goes to J1. X2 orders the placement check and chain walk before item 3a's config reads. | ON ("X2 r9 and X12 r4 drafted"); X2r9; X12 r4 |
| **MC O-1 to O-4:** prepared-mode measurement waits for M5; every core release is a new detector closure; large repositories may refuse until S-R; the plan impact. **Also:** the C4 split, the source and operational read split, and CRATE-ARCHIVE-1. | MC "Open questions", "r3 changes" |
| **M3-L:** O1(a). The stage-1 grace is Rust3's 5,000 ms, and TS2 uses D3's 2 s. No D5a successor is needed to accept L. | ML items 4, 11, 16c |
| **M2 carry-ins:** X3a-2 comes before C1. X4b is deferred to B3-a and M5-EX. X4T-c comes right after F8b. X4-F1 is a defect, fixed before any M3 analysis ships. | M2C §5 rows 13–16 |
| **X4-F1 is written.** X4-F2 and F9 are recorded as follow-ups. | ON ("X4-F1 written") |
| **S-OP-2 r2 and r3** answer Codex's findings. | ON; SOP2 |
| **M3-E1:** the syntax backend is tree-sitter grammars compiled to Wasm, run in-host by `wasmi`; native tree-sitter is the fallback if E0 fails. | ME items 2, 3; ON ("M3-E1 r1 drafted") |

**Made in this revision (P5).** Each is dated 2026-10-04, made under the owner's standing direction to decide on the lead's recommendation. A reviewer checks each one, and the owner may reverse any of them.

- **P5-1. The resume/repair writer is owned by M3-J,** as a new successor law **J-RW** and code unit **J4**.
  - **J-RW** amends X2 item 8, X3c item 10 and the X4T dependency-publication rule for L11's three state families, and adds their X9 coverage rows.
  - **J4** is resized from M to L, plus one serialized lead set. It depends on J-RW, not on J3: the crash states come from M2 code, not from the durable pipeline.
  - **Rejected:** keeping J3 → J4, which puts J4 and its rows on the exit path at 34 days; folding the writer into J1's law, which already carries the X11 successor and whose owners differ (X2, X3c, X4T).
- **P5-2. The X3c successor is X3c r8 (law) plus X3c-3** (M, storage code, with its X9 storage-row rerun), and it lands before J3.
  - **Reason:** the determinism suite and the dogfood checkpoint re-run identical analyses, and so re-commit identical Runs (EXIT:171).
  - **Rejected:** keeping it inside J3, which is a host-pipeline unit while X3c is the storage owner's law; carrying re-commit as a known M3 limit, which would make durable repetitions refuse.
- **P5-3. Generator order.** X4T-c and I1-a both follow F8b, and both regenerate `crates/contracts/src/generated`, so they integrate one at a time and never concurrently.
  - X4T-c goes first if its successor is accepted when F8b integrates (M2C row 15's "immediately after F8b"). Otherwise I1-a goes first, and X4T-c follows.
  - Neither waits for the other's review.
  - **Rejected:** a fixed order that idles the generator while one successor is still in review.
- **P5-4. X4-F1 and X4-F2 must land before J2,** the first unit that runs an analysis through the host pipeline.
  - This reads M2C row 16's "before any M3 analysis ships" for M3, where nothing is shipped to users.
  - **Rejected:** "before M3-X" only, which would let J2, J3 and the determinism suite run on a known-defective observer.
- **P5-5. F9 integrates by 2026-12-01,** a month before the fixtures expire on 2026-12-30, whatever day 0 turns out to be.
  - **Rejected:** scheduling it by DAG day, which is not anchored to the calendar.
- **P5-6. The plan adopts MC's variant B** (the C4 split), MC r3's narrowed F1 and G1a edges, and b from MB's accepted unit table: b = 10, giving 33 days.
  - **Rejected:** MB F14's "about day 8", which omits a stated edge; variant A, at 34 days.
- **P5-7. S-R is not an M3-X prerequisite.**
  - Until it lands, large T2 repositories that refuse at `snapshot2`'s bound are reported as refused (MC O-3). It is sized and scheduled after S-M.
  - **Rejected:** holding M3-X for an unsized, conditional successor.
- **P5-8. The machine order before day 0:** Grok's rerun on C, then F8b's cargo steps, then X4-F1's lanes and reruns, then S-M. S-P, CF-P and E0 run between run sets, never during one.
  - **Reason:** while O7 is pending, S-M is not what holds day 0, so M2's known defect goes first. If O7 is decided while both are waiting, S-M moves ahead of X4-F1.
  - **Rejected:** interleaving lead sets, which the 5 s timing guard forbids.

## Unsized

These units could not be sized from the records:
- **The O2 parts** (S-OP-1, -5, -6, -7, -8). Their successors are not drafted. The O-row rule applies.
- **S-R.** It is conditional on S-M's SM-5 and SM-6, and has no draft (MC item 5).
- **X4-F2 and F9.** No draft exists. They are sized provisionally, as M plus a lead set and as S, and neither is on the host chain.
- **The INC-1 successor.** It is an M4 decision (ML item 4).
- **M3-L's acceptance date.** It depends on O7, S-M and the two sign-offs.

## Risks

- **The schedule moved from 26 to 33 days.** The cause is B's real units (b = 10) and C's sub-units. The X12d lead set has zero slack at day 22.
- **The Rust compiler integration.** It needs rustc-dev and rust-dev-llvm (NE:1445). The pin has neither (`providers/rust/rust-toolchain.toml:2-4`). Stable-toolchain hosting is unverified. S-P probes it first.
- **Imported dependency sources.** Real Rust repositories need them (NE:1688-1698), and the `import` command is M5 (BP:957). C3 covers this. CRATE-ARCHIVE-1 has been checked only against unpinned Cargo sources so far (MC R6).
- **Large repositories:**
  - discovery's provisional caps, with the census margin test (MB item 12);
  - `snapshot2`'s 4 MiB descriptor holds about 27,000 rows. Five T2 repositories, and TypeScript repositories with `node_modules`, are at risk (MC item 5; S-R);
  - the 4 MiB tree-digest limit for aws-cdk and aws-sdk-rust (K1a).
- **D15 at M3.** X2 r9 is drafted. There is no cross-unit resolution, and links are honoured only after S5 and S6 (MB F2–F4).
- **Missing owners.**
  - `security/grants.rs` owns four M3 flags (COV:5277, 5317, 5337, 5377). B3-a creates it; X4b's predicate is M5-EX's.
  - `lifecycle/installation.rs` owns DR-G14 (BP:1018), but its first milestone is M5.
  - `platform/process.rs` is the M6 DR-G22 owner (BP:1026); D1 builds it early.
- **Known M2 defects.** X4-F1 (observer reread expiry) and X4-F2 (the fenced read) are disclosed at M2 completion and gated before J2 (P5-4).
- **Calendar.** The test fixtures expire on 2026-12-30 (F9; P5-5).
- **Held-out scale.** There are 10 held-out families (T2R:296), so Q2 PASS on T2 is INSUFFICIENT-EVIDENCE by design (HD OI-3; B2).
- **Cancellation goal.** Rust3's 5,000 ms grace can miss OPP's p95 ≤ 2 s without a second signal (ML item 16c).
- **Record drift.**
  - DR-G10's register row is stale (REG:355).
  - NE §14 says "independent Claude review pending" (NE:4203).
  - F02:220 and F02:259 still state the old majors.
  - M3-L records all three.
  - This revision re-pins AQP, EXIT and X12.
  - M2C §4.1 and §5 rows 10–11 say no M3 row names the resume writer or the X3c successor. r4's M3-J row did name them; r5 gives them owners.
- **The syntax backend.** If E0 fails, the native C parser joins the host TCB, and placement is re-decided before M4 accepts untrusted input (ME item 18).
- **O7 sits outside the lead's control,** and it gates L. A late decision moves the whole schedule. The confinement successors also reverse existing "never claimed" wording, which needs careful review.
- **Contention.**
  - **Reviewers:** the pre-day-0 law and successor rounds listed under "Critical path" compete for four reviewers.
  - **Machine:** a single quiet machine (P5-8).
  - **Inventory chain:** one linear chain, which F8b, X4T-c, I1-a and I1-c also share.
  - P0 and the lanes reduce this; they don't remove it.
- **Budgets.** The one-shot design may miss the §5.2 budgets (AQP:376-378). S-M exists to find that out before L.
- **Adjudication capacity** (AQP:249-255) limits exploratory Q2 depth, not exit.

## Not claimed

- **No M3 product unit has started.** The accepted M3 design records are T2, Q0, the I1 law and the B law. C r3, E1 r1, S-OP-2 r3 and the L draft are not accepted.
- **Nothing was run for this record:** no measurement, spike, cargo command or test. The DAG figures are arithmetic over the stated durations and edges.
- **No change to contracts or gates.** No gate is prepared or qualified. No contract, schema, gate, register row or threshold is changed.
- **Durations and effort are assumptions.**
- M3 does not claim:
  - CLI analysis (M4);
  - changed-scope or resident analysis;
  - `import`, `native-prepare` or repository-code execution (M5), or any confinement or container enforcement of it before M5-EX;
  - Linux or AL2023 runs;
  - Q2–Q8 qualification (M6, via D13);
  - any O7 outcome before the owner decides.
- **Sources read.** Product facts were read at `eb0d503` for r4. For r5, every cited product file was rechecked against `3e64266` with `git diff`; no other product file was read.
