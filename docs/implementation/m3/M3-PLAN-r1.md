# M3 unit plan

Draft r1. Claude Opus 5.5, implementation lead. **Planning record: not law, not code, not a contract successor.** It is the M3 counterpart of [m2/EXIT-PLAN.md](../m2/EXIT-PLAN.md). It orders M3's obligations into reviewable units and changes no accepted contract, gate, threshold or register row. Product baseline: main `eb0d503` (X9-3 integrated). M2's tail (X9-4, X9-5, X9-6 exit gate, D3, licence unit) is still in flight, so no unit below touches product crates before X9-6.

Short names: **BP** `docs/v2/architecture/implementation-boundaries-and-build-plan.md`; **COV** `docs/v2/architecture/implementation-coverage.v1.json`; **CH14** `docs/v2/architecture/14-repository-and-module-layout.md`; **F02** `docs/v2/architecture/02-distribution-and-components.md`; **REG** `docs/v2/architecture/08-decision-and-readiness-register.md`; **NE / IE / AQ / WS / SL** `docs/v2/contracts/product-v1/{native-evidence,identity-and-evidence,admission-and-qualification,workflows-and-surfaces,security-and-lifecycle}.md`; **AQP** `docs/implementation/m3/analysis-quality/PLAN.md` (r4, accepted); **OPP** `docs/implementation/m3/operability/PLAN.md` (r2, under review; provisional here); **EXIT** `docs/implementation/m2/EXIT-PLAN.md`; **X11 / X12** `docs/implementation/m2/{cli-enablement-x11,policy-admission-x12}/PROPOSAL.md`. Product paths are under `opensip/`.

## What M3 exit means

The build plan's milestone row (BP:887) defines M3:

- **Deliverable:** "M2 and provider build lanes; discovery/configuration, sealed snapshot/Plan, supervised TS/JS and Rust analysis and the guarded durable host pipeline".
- **Owners:** "Host discovery/snapshot/plan/analysis; components protocols; both providers and evaluator".
- **Completion:** "Selected native matrix/corpora, missing-role disclosures, cancellation, semantic admission and host-boundary durability checks; neither language silently dropped. Complete CLI analysis delivery follows at M4 with every advertised renderer".

**Routed to M3 by the coverage owner** (COV; generated table BP:933-945):

- all 66 capability cells (COV:2077-4425): 57 SUPPORTED-DESIGN, 6 UNSUPPORTED-TYPED, 3 NOT-SELECTED (AQP:105; NE:590-601);
- seven gates, each to be *prepared*, not qualified: DR-G10, G13, G14, G21, G23, G25, G29 (BP:1014-1033). Execution stays at M6 (BP:895, BP:999-1000);
- all seven shared flags (COV:5266-5407), twelve contract sections (COV:6506-7849) and Fallow constraints FW-01, -03, -08, -13, -14 (COV:7850-8166);
- **no command.** Every analysis command is M4 or later (BP:949-995). Complete CLI delivery is M4 (BP:887-888).

**The accepted quality plan's M3 obligations.** Before the provider protocol is fixed: INC-1 to INC-8 in the M3 law, the INC-7 spike, pinned T2 manifests (multi-repo approximation and Python included), the harness design and the rule-catalog draft (AQP:480). At M3 (AQP:481):

- T1 for all 57 supported cells per mode, typed refusal for 6 and non-advertisement for 3;
- Q1 and Q4 on T1;
- draft catalog rules run non-authoritatively through the evaluator's policy module, giving exploratory Q2–Q4 on T2;
- the determinism suite and exploratory Q6 workloads;
- multi-repo workspace shapes in discovery;
- the third-language readiness review;
- an internal-harness dogfood checkpoint, "not CLI `analyze`".

**The operability plan's provisional M3 items** (OPP:333-334): O1 and O7 decided and the S-OP-2 vocabulary drafted before the protocol law. Then `tracing` with nonpersistent sinks, the vocabulary and allowlists, the bounds and loss marker, phase spans and the operational record as harness instrumentation, the supervision primitive and liveness, the outcome matrix in tests, two-stage cancellation and the enforcement checks. Once their successors are accepted: the file sink (S-OP-1), crash records (S-OP-7), capacity preflight (S-OP-8), and public `-v`/`--log-level` (S-OP-5, S-OP-6). G20/G21 controls are authored now (S-OP-11).

**M2 carry-ins:**

- **X11 successor law.** No creator command went live in M2 (EXIT:180; X11:18). The M3 law must fix the request order, the creator's host entry, the one-RequestId rule, how the creator command ends, and the backup-status successor (X11:64-77).
- **X12c and X12d.** X12c is the DR-131 pack row (a contract successor). X12d is the Run-closure `check_plan_pack` join in replay, and it must land before any analysis producer reaches X5 (X12:191-192).
- **A resume/repair writer** for the crash states M2 leaves permanently refused (EXIT:184-189).
- **Re-commit refused at staging.** A Run already committed in the same store and namespace is refused when re-committed (EXIT:169). That needs an X3c successor before a determinism suite re-commits identical Runs.
- **The product licence unit** (AQP:536). It gates T3.

## Product state at eb0d503, by M3 owner module

| Owner (BP:887; CH14) | State | What exists |
|---|---|---|
| `crates/host/src/discovery.rs` | **absent** | First milestone M3 (COV:8963). |
| `crates/host/src/configuration.rs` | partial | Only X12's pack admission. "Layer merge, discovery, profiles, capabilities, waiver IDs and `resolvedConfigDigest` arrive with M3" (`crates/host/src/configuration.rs:1-4`). |
| `crates/host/src/snapshot.rs`, `plan.rs`, `analysis.rs`, `invocation.rs`, `syntax.rs` | **absent** | None in `crates/host/src`. The planned owners are at CH14:475, 485, 489, 495, 496. |
| `crates/host/src/fact_admission.rs` | partial | The replay join only. "The M3 syntax, context, occupancy and Coverage joins arrive in this module" (`fact_admission.rs:1-3`). |
| `crates/host/src/request.rs`, `outcomes.rs` | partial | A process-custody `RequestAuthority` for the nonpersistent metadata host (`request.rs:15-19`). |
| `crates/host/src/finalization.rs`, `crates/storage/src/commit.rs` | present (M2) | The finalization and commit library, not wired to any command (`crates/host/src/lib.rs:53-62`). |
| `crates/components/*` | **absent** | Not a workspace member (`Cargo.toml:3`). CH14:41 still marks it "proposed". |
| `crates/syntax/*` | **absent** | Not a member (`Cargo.toml:3`). CH14:37 marks it "proposed". No parser dependency in `Cargo.lock`. |
| `crates/security/src/component_manifest.rs` | present | Structural manifest owner over captured bytes, with "no runtime or artifact authority" (`component_manifest.rs:1-2`). `components/manifest.rs` (DR-G29 owner, BP:1033) is absent. |
| `crates/security/src/grants.rs` | **absent** | Yet four M3 shared flags name it as owner (COV:5266-5287 and the `--trust-*`/`--yes-policy` rows). |
| `crates/platform/src/process.rs` | **absent** | The only process module is a read-only translation query (`crates/platform/src/macos_process.rs:1-2`). No spawn or supervision primitive. |
| `crates/evaluator` | largely present | Universe, context and Coverage-producer inspectors (`crates/evaluator/src/lib.rs:9-38`), pack admission (`lib.rs:111`), derivation (`lib.rs:122`) and replay (`lib.rs:127`). The bundled pack registry has **zero rows** (`crates/evaluator/src/pack-registry.json:3`). |
| `crates/identity`, `crates/contracts` | present | Every identity domain, `snapshot2` through `run3` (`crates/identity/src/descriptors.rs:483-555`). Generated TS2 and Rust3 frame carriers (`crates/contracts/src/generated/protocol.rs:5422`, `:6111`) from a carrier input that is "not a production wire decoder" (`schemas/wire/native-carriers-v1.json:4`). |
| `providers/typescript` | stub | Inert generated types only (`src/generated/protocol.ts:1`). Pins Node 24.16.0 and TypeScript 6.0.3 (`package.json:7`, `:12`). None of the CH14:506-525 sources exist. |
| `providers/rust` | stub | `main.rs` exits failure before reading a request (`providers/rust/src/main.rs:1-14`). Its own workspace and 1.95.0 pin carry no `rustc-dev` component (`providers/rust/Cargo.toml:1-2`; `rust-toolchain.toml:2-4`). |
| `crates/lifecycle/src/installation.rs` | **absent** | The DR-G14 owner (BP:1018), whose first milestone is M5 (COV:8976). |
| Tests | partial | `crates/host/tests/admission_tests.rs` exists. `discovery_tests.rs`, `workflow_tests.rs` and `tests/qualification/` are absent, though COV names them as verification owners (e.g. COV:5280, 7865, 8138). |
| Operability | **absent** | No `tracing` in `Cargo.lock`, no `std::panic::set_hook`, and no `--timings` in `apps/cli/src/arguments.rs`. Three coded stderr lines (`apps/cli/src/bootstrap.rs:19`, `:44`, `:65`). The default command still refuses (`arguments.rs:104`). |

Also in place: the M1 provider lane checks (`tools/check_typescript.py`, `tools/typescript-lanes.json`), and the Rust provider excluded from the host workspace (`Cargo.toml:4`). That excluded workspace is the separate lane BP:621-622 requires.

## Units, in dependency order

Sizes follow EXIT:61: S is about one review round of a single file; M is several files with one inventory successor; L is a law plus two or three code units; XL is a law plus four or more units and a harness. Sub-units (B1, C2 …) are reviewed separately; the row is the planning unit.

| Unit | Scope | Depends on | Law / successor? | Size | Gates and quality items |
|---|---|---|---|---|---|
| M3-T2 | **T2 corpus manifests** and a harness-only `corpus fetch` (AQP:207). The shapes are those of AQP:211-219: Rust, TS/JS, polyglot, the multi-repo approximation (D15), size classes and a held-out set. Also Python T2 (D9) and licence and size checks. The medium repositories come first, for M3-S. No product code. | — | none; D3 owner sign-off (AQP:524) | M | O1, D3, D9, D15, FW-14 |
| M3-Q0 | **Harness design record:** the case model (AQP:130-135), the label ledger (AQP:249-263), the confidence rule (AQP:233-237), the exploratory envelope (AQP:419-425) and the D12 runner. Also the rule-catalog draft specs (AQP:167-191). | — | D13 envelope and D2 draft (AQP:523, 535) | M | Q1–Q8 definitions; D2, D12, D13 |
| M3-S | **INC-7 spike.** Measures one-shot startup, sealing and replay costs on medium T2 with a throwaway harness outside the product (AQP:389). Also probes whether the pinned toolchain can host the `rustc_driver` sidecar (see Risks). Results are recorded in an exploratory envelope. It is a lead run set. | M3-T2 (medium) | none | M | INC-7, Q6 |
| M3-L | **M3 provider-protocol and reuse law.** It carries:<br>- INC-1 to INC-8 (AQP:370-390), with TS2/Rust3 unchanged (INC-5; BP:716-717) and one child per universe with no reuse (F02:222, F02:269);<br>- O1(a), no new control message, with the S-OP-4 record join (OPP:208-214, OPP:363);<br>- RequestId as the universal correlator, with phase-lawful identities (OPP:124-135);<br>- the two-stage cancellation join (OPP:293-294);<br>- a record correcting DR-G10's selector: REG:355 still says "TS major 1 and Rust merged major 2" and "HARD-BLOCKED pending selector refresh", while COV:4671 expands it to TS2/Rust3. | M3-S | **law**; D5a successors only if an INC needs one (AQP:527) | L | G10, G21; INC-1..8; O1 |
| M3-P0 | **Package scaffolds.** `crates/components` and `crates/syntax` (CH14:284, CH14:288) as workspace members, the provider source layout, and dependency-policy rows. One inventory successor, so that parallel lanes don't race the linear inventory chain or `Cargo.toml`. | M2 exit (X9-6); licence unit | inventory successor | S | — |
| M3-B | **Configuration and discovery.**<br>- **B1, the resolver:** Config2 layers, provenance and `resolvedConfigDigest` (AQ:43-53; `configuration.rs:1-4`), and FW-13's registry.<br>- **B2, discovery:** the S3 boundary (SL:105-332); units and membership U-0..U-4 (NE:619-1240); zero-config FW-01; the host side of framework recognition (NE:2750).<br>- **B3, multi-repo workspaces (D15):** an X2 successor, because M2 "admits one closed, conventional Git layout and refuses every other layout as `vcs-unsupported`" (`crates/security/src/custody/git_tracking.rs:5-6`). Also the consent flags, with a new `security/grants.rs` (COV:5266-5287). | M3-P0 | **law** (discovery/config); X2 successor; SMAP successor if D15 needs one (AQP:537) | XL | FW-01, FW-13, FW-14, D15; 6 `inventory/*` cells; 7 shared flags; SL:3, NE:2, NE:9 |
| M3-C | **Sealed snapshot and Plan.**<br>- **C1, `snapshot.rs`:** exact read-set bytes under custody, and `snapshot2` (IE:179).<br>- **C2, native contexts and closure admission:** `NativeContextV2`, `TypeScriptNativeContextV2` and the syntax context (NE:1430-1645); `closure2` for toolchain, stdlib, rust-dev-llvm and grammar (BP:699-713). Tests use synthetic signed closures, as M2's did.<br>- **C3, dependency sources and prepared outputs:** DS-1..DS-6 (NE:1646-1702), a library-level import of user-named sources (DS-5, NE:1688), and PO-0 admission of imported prepared sets (NE:1803-1830).<br>- **C4, `plan.rs`:** `plan2` (IE:182), the prospective-Plan bounds (NE:4276), and X12d. | M3-B, M3-L | **law** (snapshot/Plan); X12d inventory successor (X12:192) | XL | NE:3, NE:4; L-RS1, L-RS4 |
| M3-D | **Supervisor and common control.**<br>- **D1, `platform/process.rs`** (also the DR-G22 owner, BP:1026): spawn with an explicit environment, no PATH, a process group and fd channels.<br>- **D2, `control_protocol.rs`:** the codec over control-v3, plus `provider_protocol.rs` dispatch with no translation (F02:168-169).<br>- **D3, `supervisor.rs`:** deadline, health, resources, a TERM→KILL tree kill, single settlement, cancellation and candidate discard (F02:199-214; OPP:247).<br>- **D4, `manifest.rs` and `session_factory.rs`** over `security::component_manifest`, with DR-G29 refusals and no ExecutionId (REG:374). | M3-P0, M3-L | **law** (supervision) | XL | G10 (control half), G21, G29 |
| M3-E | **Syntax crate and grammar registry.**<br>- **E1, law:** the backend choice that CH14:614 leaves to review, and the retained `SyntaxGrammarBundleV1` closure (BP:684-688). The registry has seven languages and fourteen suffixes (NE:260-263; BP:692-694).<br>- **E2:** `grammar.rs`, `parser.rs`, `normalization.rs` and `candidates.rs` (CH14:372-379).<br>- **E3:** `host/syntax.rs` dispatch (CH14:496).<br>It is split from the providers because the crate is pure: no discovery, compiler or process (BP:676-680). | M3-P0, M3-C2 | **law** (syntax) | L | G13 (syntax part); 11 `*/syntax-only` cells; per-grammar fixtures (AQ:233-234) |
| M3-F | **TS/JS provider (TS2).**<br>- **F1, transport:** `protocol.ts`, `session.ts`, `sealed-vfs.ts`, `program-factory.ts`, `NativeContextVerified`, `Unavailable` and `Cancel` (NE:2944-3002, NE:3151-3316).<br>- **F2, facts:** imports, references, calls, unresolved edges, types with provenance (NE:2347), symbols and `coverage.ts`, across the three modes.<br>- **F3:** reachability and framework recognition (L-FW1; NE:2750), `syntax.ts`, and `clones.ts` including cross-tsjs (NE:2604).<br>- **F4, runtime closure:** signed Node and TypeScript, with no ambient Node (F02:252). | M3-C, M3-D | none expected (TS2 is accepted; BP:717); G10 goldens | XL | G10, G13, G14 preparation; 33 TS/JS cells |
| M3-G | **Rust provider (Rust3).**<br>- **G1, transport:** `protocol.rs`, `session.rs`, `sealed_vfs.rs` (with the dependency and prepared frames, NE:2872-2943) and `context.rs`.<br>- **G2, `compiler_adapter.rs`:** the `rustc_driver` sidecar (`12-architecture-completion-goal.md:145`) with the rust-dev-llvm closure (NE:1445).<br>- **G3:** `inventory.rs`, `facts.rs` and `coverage.rs`, covering L-RS1..L-RS3 and `missing-external-crate` (NE:1793).<br>- **G4:** prepared-mode consumption (L-RS4) and `clones.rs`. | M3-C, M3-D; M3-S for G2 | none expected (Rust3 is accepted; BP:717) | XL | G10, G13, G14 preparation; 22 Rust cells |
| M3-H | **Fact admission** (DR-G23, DR-G25):<br>- the syntax, context, occupancy and Coverage joins (`fact_admission.rs:1-3`);<br>- relation-registry refusal before admission, and Coverage-domain mutation refusal (REG:368);<br>- a missing rung is Coverage-indeterminate, with no silent fallback (REG:370).<br>It is separate from the providers because "protocol framing alone grants no fact authority" (CH14:482). | M3-C4; first producer (E3 or F1) | **law** (admission) | L | G23, G25; NE:5 |
| M3-I | **Evaluator and draft catalog, non-authoritative.** X12c's pack row (X12:191). The draft catalog as `PolicyDocumentV2` rules (AQP:165-191), evaluated only in the harness over admitted M3 facts (AQP:481). | M3-H, M3-Q0 | X12c contract successor. The product pack stays at M5 (D2, AQP:523). | M | exploratory Q2–Q4 |
| M3-J | **Guarded durable host pipeline.**<br>- **J1, law:** the X11 successor (X11:64-77), the invocation DAG (WS:76-256), and the backup-status successor (X11:76).<br>- **J2, `invocation.rs` and `analysis.rs`, ephemeral:** request, configuration, discovery, snapshot, Plan, supervised providers, admission and evaluation, with cancellation and D9 outcomes. No durable write.<br>- **J3, durable:** through X7 finalization and the commit; `workflow_tests.rs`; the re-commit limit (EXIT:169).<br>- **J4, the resume/repair writer** (EXIT:184-189). | M3-B, M3-C, M3-D, M3-H; producers E/F/G | **law** (X11 successor); backup-status contract successor; X3c successor for re-commit | XL | G25; NE:14, NE:15; FW-03, FW-08; WS:2 |
| M3-K | **Quality harness and T1.**<br>- **K1, the harness core:** store reader, case model, scoring, envelope writer and determinism driver (AQP:316-319).<br>- **K2, T1 in three lanes (TS/JS, Rust, syntax-only per grammar):** 57 supported, 6 typed-refusal and 3 non-advertisement cells (AQP:481; AQ:233-234). K2 is authored ahead of the producers, because expected answers must be independent (AQP:104). | M3-Q0, M3-T2 | D13 (from Q0) | XL | Q1, Q4, G13 |
| M3-M | **Exploratory measurement and the dogfood checkpoint.** Q1 and Q4 on T1; exploratory Q2–Q4 through M3-I; the determinism suite; Q6 workloads with phase timings; T3 once the licence unit lands (AQP:536). Not CLI `analyze` (AQP:481). It is a lead run set. | M3-J2/J3, I, K, O1 | none | L | Q1–Q6 exploratory |
| M3-O | **Operability.**<br>- **O1:** `tracing` with the S-OP-2 vocabulary, nonpersistent sinks, the bounds and loss marker, phase spans, and the operational record that carries INC-8's reuse disclosure (OPP:222-224). Also the enforcement checks (OPP:316-325).<br>- **O2, each part gated on its own successor:** the file sink (S-OP-1), crash records (S-OP-7), capacity preflight (S-OP-8) and public switches (S-OP-5, S-OP-6).<br>- **O3:** the G20/G21 controls (OPP:374-388).<br>`--timings` goes public at M4 (OPP:335). | M3-P0; S-OP-2 before O1 | S-OP-1, -2, -5, -6, -7, -8, -11 (OPP:360-370) | L | G21; G20 preparation |
| M3-R | **Third-language readiness review**, with Python as the test case, and the onboarding kit (AQP:448-470). | M3-L, F2, G3, K2 | record only | M | O8, D9 |
| M3-X | **M3 exit gate.** BP:887's completion checks over the selected matrix and corpora on this host's profile, with the seven gates prepared and neither language dropped. | all | none | L | all M3 gates |

**Why these splits.**

- **B and C are separate units:** discovery answers to the security S3 boundary and D15's successor, while the snapshot answers to identity.
- **C keeps its four parts together:** `plan2` binds the snapshot, contexts, imports and configuration at once (IE:182). The host also owns resolved inputs before the PlanId (NE:2497-2499).
- **C3 and G4 are separate:** the host admits dependency and prepared sets (NE:1704-1712), and the provider consumes them.
- **D is one unit shared by both providers:** the control plane is common (F02:158-177).
- **J is split four ways:** an ephemeral path, a durable path, and the M2 resume debt all have different reviewers' failure surfaces.

## Critical path and parallel lanes

**Critical path:**

> M3-T2 (medium subset) → M3-S → M3-L → M3-P0 → C1 → C2 → G1 → G2 → G3 → M3-H → J2 → J3 → M3-M → M3-X

That is 14 serial sub-units, one of them a law. The Rust provider sits on the path because it has the most frames (26, against TS2's 17, in `schemas/wire/native-carriers-v1.json` `protocols`), it alone needs sealed dependencies and prepared data, and its compiler integration is the least proven. The rest of M3 can run beside it:

| Lane | Units | Reviewer (suggested) |
|---|---|---|
| Host core | B → C → H → J | Grok (fact validation) |
| Components | D, then F1/G1 transport conformance | Codex (method) |
| Rust compiler | S's probe → G2 → G3 → G4 | CODEX2 |
| Syntax and TS analysis | E → F2/F3/F4 | GROK2 |
| Quality and operability (fills gaps) | T2, Q0, K, I, O, R | whichever reviewer is free; records get one fact reviewer and one method reviewer, as AQP had (AQP:3) |

**Lead run sets stay serialized.** Every workspace test run, every spike or Q6 measurement, and every crash-matrix set runs alone. The crash matrix has a 5000 ms timing guard (product commit `eb0d503` subject), and performance samples are meaningless under load. M3-S and M3-M wait for X9's lead sets.

**Effort account (rough; the design reviews found none).** The plan has about 18 law, successor or record units (M3-L; the B, C, D, E, H and J1 laws; X2, X12c, X12d, backup-status, X3c, S-OP-1/2/7/8; D13) and about 39 code or harness sub-units: roughly 57 reviewed units.

For calibration, M2's exit run integrated 55 product commits from `d4239a5` (2026-09-29) to `eb0d503` (2026-10-02) (`git rev-list --count d4239a5..eb0d503`). Those were mostly mechanism units in an already-specified area. M3's code units are larger and newer: two compiler integrations, three parser families and a corpus.

**Planning assumption:**

- laws take about 3 rounds;
- code units take about 2 rounds and 1–3 days each on the critical path.

This gives about 130 review rounds in total and a critical path of roughly 3–6 weeks of wall clock. G2/G3 and the T1 authoring dominate. This is an estimate to steer by, not a commitment. M3-S re-estimates G2 before M3-L is accepted.

**Recommended start (now, with no product crate touched before X9-6):**

1. **M3-T2**, medium repositories first.
2. **M3-S**, once X9's lead sets finish.
3. **M3-L**, drafted while the spike runs and accepted only after it.

The E1 and D laws, and M3-Q0, start as soon as a reviewer is free.

## Choices left open, with lead recommendations

**Already decided; cite, don't reopen:**

- **Owner decisions:** D4, D5 (staged reuse), D6, D9 timing, D10, D11, D14 (Apache-2.0), D15 (multi-repo shapes) and D16 (AQP:525-538).
- **Evaluation at M3:** catalog rules are evaluated non-authoritatively at M3 (AQP:481), with CLI dogfood at M4 (AQP:483; BP:887).
- **Protocols and substrate:**
  - the protocols are TS2 and Rust3 (BP:717);
  - the Rust substrate is the `rustc_driver` sidecar (`12-architecture-completion-goal.md:145`);
  - `crates/syntax` is pure and depends only on contracts and identity (BP:676-678).
- **No creator command in M2** (X11:18).
- **X12c and X12d are M3 work** (X12:191-192).
- **The Python decision comes after M3's review** (AQP:446).

Each choice below has a technical basis, so under the owner's standing direction the lead decides it in the named unit's law, and a reviewer checks it.

- **Provider diagnostics channel (O1, M3-L).** Recommendation: (a), existing admitted observations only (OPP:208-212). Rejected: a new frame, which needs S-OP-3 and both protocol joins (OPP:214).
- **Syntax backend (M3-E1; CH14:614).** Recommendation: a trial between tree-sitter grammars and hand-written parsers. The lead leans to tree-sitter for Rust, TS and JS: one uniform `grammarVariant` and anchor model, and retained grammar bytes that map onto the `kind=grammar` closure (BP:684-688). Its C runtime joins the host TCB, which BP:680-682 already anticipates. Rejected: three bespoke parsers and normalizers.
- **Dependency-source acquisition at M3 (M3-C3).** Recommendation: a library-level import step for user-named sources (DS-2 tarballs, DS-1 vendored trees; NE:1681-1691), driven by the harness. The `import` command stays at M5 (BP:957). Without it, every T2 repository with registry dependencies is `input-closure-incomplete` (NE:1693-1698).
- **Prepared mode at M3 (M3-C3, G4).** Recommendation: consume `imported-descriptor` prepared sets built by harness tooling (NE:1806). The authorized producer, `native-prepare`, stays at M5 (BP:992).
- **DR-G14 placement (M3-L).** The gate is routed to M3 (COV:4764-4771), but its owner module is first an M5 module (COV:8976). Recommendation: M3 prepares the provider closure manifests and the no-ambient-runtime refusal tests (F4, G2). Component installation stays at M5. M3-L records the split.
- **Public CLI at M3 (M3-J1).** Recommendation: nothing public is wired. J1 fixes the order and identity rules now, so M4 only wires them (BP:887-888).
- **Changed-scope at M3 (M3-L).** Recommendation: none ships. The law carries the obligations, and M4 decides with M3-S data (AQP:483).
- **Logging dependency (M3-O1).** Recommendation: `tracing` with one host-owned subscriber and no environment filter (OPP:123, OPP:200). Its exact closure goes into the dependency policy.
- **Platform scope at M3 (M3-X).** Recommendation: build portable code, but run and claim only this host's macOS family. The four families (NE:157-160) are a qualification-lane matter.

## Owner decisions

- **O7, hostile-input confinement** (OPP:353; owner, threat posture). OPP:300 says it is "needed before M3 providers ship", and OPP:333 places it before the protocol law. Lead recommendation: as OPP proposes. It does not change the wire, so it does not block M3-L or the F/G units, but it blocks M3-X.
- **O4, OTLP export** (OPP:350). An M5 matter; it does not block M3.
- **O9, raw provider stderr capture** (OPP:354; lead with owner sign-off). Recommendation: not at M3.
- **Sign-offs on lead decisions:** D2, D3, D12 and D13 (AQP:523-535).
- **Owner actions, not decisions:**
  - human expert time to settle adjudication disagreements (AQP:246);
  - T3 access once the licence unit lands (AQP:536);
  - signing keys for real-machine runs (EXIT:110). M3 exit does not need them; tests use synthetic signed closures, labelled as such.

## Risks

- **The Rust compiler integration is unproven here.** `rustc_driver` needs the rustc-dev and rust-dev-llvm closure (NE:1445). The provider pin carries neither (`providers/rust/rust-toolchain.toml:4`). Whether a stable 1.95.0 toolchain can host it without an unstable-feature escape is unverified. M3-S probes it before M3-L is accepted.
- **Real Rust repositories need imported dependency sources** (NE:1688-1702), whose command owner is M5 (BP:957). The C3 recommendation covers this. Without it, Rust semantic cells on T2 measure only incompleteness.
- **D15 meets M2's single-layout VCS rule** (`git_tracking.rs:5-6`). Multi-repo workspaces and worktrees need the B3 X2 successor.
- **Owners that don't exist yet.** `security/grants.rs`, `platform/process.rs` and `lifecycle/installation.rs` are absent, but M3 rows name them as owners (COV:5266-5287; BP:1018, BP:1026).
- **Record drift.**
  - DR-G10's register row is stale and hard-blocked (REG:355).
  - NE §14, which is routed to M3, carries "independent Claude review pending" (NE:4203).
  - M3-L must record both rather than build on them silently.
- **Contention.**
  - Parallel lanes share one linear inventory chain, so every integration rebuilds the other candidates.
  - Measurement needs a quiet machine.
  - M3-P0 and the lane assignment reduce this; they don't remove it.
- **Budgets.** The one-shot design may miss the §5.2 budgets (AQP:357-359). INC-7 exists to find that out before the protocol law, not after.
- **The corpus is human-limited.** Q2 adjudication needs blind, independent labels and a human expert (AQP:241-247). M3 reports it only as exploratory. Unbudgeted adjudication time would slip M3-M, not M3-X.
- **The operability plan is still under review (r2).** S-OP labels and numbers may change, and M3-O follows the accepted revision.

## Not claimed

- No unit has started, and no measurement, spike or test was run for this record.
- No gate is prepared or qualified, and no contract, schema, gate, register row or threshold is changed.
- The effort numbers are planning assumptions, not data.
- M3 does not claim CLI analysis (M4), changed-scope or resident analysis, the `import` and `native-prepare` commands (M5), Linux or AL2023 runs, Q2–Q8 qualification (M6, via D13), or T3 before the licence unit.
- This record was written from code reading at `eb0d503` only; the product was not built.
