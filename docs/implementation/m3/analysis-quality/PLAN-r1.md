# M3 analysis-quality plan — proposal r1

2026-10-03. Claude Opus 5.5, implementation lead. Written at the owner's request ("draft the M3 analysis-quality plan"), and reviewed by GROK2 (fact validation) and CODEX2 (method review).

## Standing

**This is a plan, not law and not a contract successor.** It changes no accepted contract, gate, threshold or register row. Where it needs one, it names the owning row and lists the change under "Decisions this plan asks for" (§11). Each such change is made later, through its own reviewed successor. Every number in this plan is a **proposed target**. None is a measurement or a qualification claim.

**What it plans.** How OpenSIP will define, measure and gate the quality of what a developer actually sees: facts, findings, Coverage, stability, speed and explanations. It covers TypeScript/JavaScript and Rust at M3, Python as the third language, and the method for adding more.

**Why now.** The design calls the language-quality corpus "the largest shared unmeasured product risk" (`docs/v2/architecture/11-three-reviewer-direction-synthesis.md:290`). The owner intends to use OpenSIP daily on a Rust, TypeScript and Python team, and judges it by the quality of its analysis. M3 is where the analysis gets built, so its quality has to be defined before then. The crash matrix plays that role for durability at M2; this plan does the same for analysis at M3.

**The authority this plan sits under.**
- **The product contracts** (`docs/v2/contracts/product-v1/`), applied under D-372.
- **DR-118** (language-native quality) and **DR-G13** (`harness.DR-G13.product-v1`, `docs/coop/design-corrections/qualification-gates.applied.v1.json` items[12]).
- **The 66-cell native capability matrix** (`docs/coop/design-corrections/native/native-capability-matrix.v2.json`; `docs/v2/contracts/product-v1/native-evidence.md` §1.3).
- **The build plan's milestone rows** (`docs/v2/architecture/implementation-boundaries-and-build-plan.md:884-890`).

Short names used below:
- **AQ:** `docs/v2/contracts/product-v1/admission-and-qualification.md`
- **NE:** `docs/v2/contracts/product-v1/native-evidence.md`
- **WS:** `docs/v2/contracts/product-v1/workflows-and-surfaces.md`
- **IE:** `docs/v2/contracts/product-v1/identity-and-evidence.md`
- **AQC:** `docs/coop/completion/analysis-quality-completion.v2.md`
- **QG:** `docs/coop/design-corrections/qualification-gates.applied.v1.json`
- **BP:** the build plan
- **CH13:** `docs/v2/architecture/13-evidence-workflows-and-product-contracts.md`

---

## 1. What the design already decides, and what it leaves open

This plan builds on the following. It does not reopen any of it.

**Decided.**
- **Fact correctness is exact.** Expected facts, Coverage and graph results must equal an independent oracle by set equality, so precision and recall are both 1.0 on a finite corpus (AQC:127-130; AQ:257-266). The gate computes counts and correctness itself; a submitted PASS flag is refused.
- **The 66 cells.** There are 11 capabilities × 6 modes: 57 SUPPORTED-DESIGN, 6 UNSUPPORTED-TYPED and 3 NOT-SELECTED, each with named limitations L-JS1–3, L-RS1–4, L-FW1 and L-CL1 (NE:584-616).
- **No silent fallback.** A missing semantic rung is typed and indeterminate, never a weaker answer (D-007 item 8; DR-G25, routed to M3 at BP:1029).
- **Honest Coverage.** Outputs separate "no matches", "unsupported" and "attempted but insufficient" (CH13:94-98). Zero findings never establish complete analysis (WS:466-467).
- **Stable finding identity.** `finding-key2` excludes line offsets and messages, and renames require explicit correspondence (IE:188-213).
- **Baseline deltas** follow the delta-class model, and a removed detector can't hide a new bug (WS:352-358, WS:437-438).
- **Performance statistics for product cells.** Each benchmark takes the median of 7 runs after 3 warmups. A regression fails above ×1.20 time or ×1.25 RSS against a reviewed baseline, plus per-fixture absolute bounds. A new cell needs a reviewed initial baseline and budget (AQ:273-287).
- **Real repositories are required.** The corpus must include "public or consented exact repository/configuration shapes, confirmed workarounds and manual-correction counts", and synthetic cases alone cannot qualify discovery (QG items[12]; CH13:77-84).

**Open or absent.** This plan exists to fill these gaps:
- **O1. No executable product corpus.** Only the TypeScript preview corpus is pinned (1,019 files, `quality-corpus-manifest.v1.json`). The 477 native cases are design-reference scenarios (QG items[12]; AQ:244-249). Several cells share case lists across TypeScript and Rust modes instead of having mode-specific ones.
- **O2. No first-party rule catalog.** Dead code, unused exports and boundary rules appear only as workflow fixture IDs. The design measures precision and recall on facts, never on the findings a developer reads.
- **O3. No budgets outside the TypeScript preview.** There is no latency or RSS budget for any JS, Rust or syntax-only cell, no real-repository latency target, and no worst-case graph bound. DR-G05 component caps are still undecided.
- **O4. No incremental, changed-scope or resident-host obligation** (`11-three-reviewer-direction-synthesis.md:275-276`).
- **O5. No requirement on explanation quality.** Remedies attach to terminations, not findings. Findings carry `messageCode` and parameters only (IE:1282-1286).
- **O6. No fingerprint-stability measurement.** There is no rename or move correspondence mechanism and no churn metric.
- **O7. The status of exploratory measurements is undefined.** Nothing says how a pre-qualification measurement may inform design without becoming G13 evidence.
- **O8. Python is absent.** `.py` is `unsupported-file`, `no-bundled-grammar` (NE:304-306).
- **O9. Two statistical regimes are cited inconsistently.** QG items[12] still names "cold/warm p95" and "thresholds DECIDED by D-369", while AQ §3 specifies median and ratio.

---

## 2. What "excellent" means: eight measurable quality dimensions

Each dimension has a definition, a measurement and a proposed target. Q1 and Q8 already exist in the design. Q2 to Q7 are this plan's additions.

| # | Dimension | What a developer experiences | Measured by | Proposed target |
|---|---|---|---|---|
| Q1 | Fact correctness | The graph, references and types are right | Oracle set equality per cell (existing) | Exactly 1.0, as now |
| Q2 | Finding precision | Every reported finding is real | Adjudicated findings on pinned real repositories (§4.3) | Gating and repair-eligible rules ≥ 0.99; advisory rules ≥ 0.90 |
| Q3 | Finding recall | Real problems aren't missed where analysis claims completeness | Seeded defects plus a cross-tool differential (§4.4) | ≥ 0.95 within complete-resolution scope |
| Q4 | Coverage honesty | "Clean" means clean; unknown means unknown | Every known defect in an unresolved region must surface as indeterminate, never as clean | **Zero** false-clean results; any one is a release-blocking defect |
| Q5 | Stability | Findings keep their identity through refactors | A refactor suite over pinned repositories (§4.5) | ≥ 0.99 identity survival for unaffected findings; zero spurious CODE-NET-NEW from formatting or reordering |
| Q6 | Speed | Fast enough to run on every change | Product-regime statistics on real repositories by size class (§5) | Size-class budgets in §5.2; incremental budgets once O4 is decided |
| Q7 | Explanations | Each finding says why, shows the evidence, and suggests what to do | A structured-field check, plus a rubric on a sample (§6) | 100% have an evidence path and a reason code; rubric ≥ 4 of 5 on a sample |
| Q8 | Zero-config usefulness | Useful on the first run, with no setup | Manual corrections per pinned repository (FW-14) | 0 for conventional shapes; every correction recorded with its cause |

Three principles govern all eight:
- **Honesty outranks coverage.** An indeterminate answer is never scored as a recall miss, and a false-clean answer is never tolerated (Q4). Indeterminate rates are reported per repository so they can't hide. Reducing them is engineering work, not a reason to guess.
- **Precision outranks recall for anything that gates or repairs.** A developer stops trusting a tool after a few false positives. This matters most for dead-code deletion, which is gated by `deadCodeRepairEligible` (NE:2237-2242).
- **Targets are product decisions.** §11 asks the owner to approve them. Until then they are the targets M3 engineering works toward and measures against, with the measurements labeled exploratory (§7).

---

## 3. The rule catalog (O2)

Precision and recall need something to measure. The plan proposes a first-party catalog, defined at M3 and evaluated through the closed declarative policy DSL (FW-15; WS:621-649). Each rule records:
- its ID and definition;
- the capability cells it requires, with their sufficiency;
- its behavior under incomplete Coverage (strong Kleene, WS:600-604);
- its `messageCode` and parameters;
- an explanation template (§6);
- its class: gating, advisory or repair-eligible;
- its precision target and known limitations.

**The initial catalog** draws on the IDs the workflow fixtures already use, plus the gaps that matter most for daily work:

| Rule | Languages | Why it matters | Class |
|---|---|---|---|
| `unused-export` | TS/JS | The most common TS dead code; existing fixture ID `no-unused-export` | gating |
| `unimported-file` | TS/JS | Whole files nothing reaches (existing fixture ID) | gating |
| `unused-dependency` | TS/JS (package.json), Rust (Cargo.toml) | Supply-chain and build-time cost | gating |
| `module-import-cycle` | TS/JS, Rust (module graph) | The preview's one shipped rule (AQC:53-63) | gating |
| `rs-unused-pub-item` | Rust | `pub` items unused anywhere in the workspace. rustc's `dead_code` lint can't see across crates, so OpenSIP adds real value here; existing fixture ID `rs-no-dead-fn` | gating; repair-eligible only under closed-world |
| `unresolved-import` | TS/JS, Rust | Disclosed, never guessed | advisory |
| `clone-exact` / `clone-normalized` | all | Duplicate code, as facts | advisory |
| `clone-near` | all | Candidate only; never equivalence (L-CL1) | advisory |
| `boundary-violation` | all | Architecture layering, declared by the project (CH13 §2: project decisions are explicit policy) | gating once declared |

**Contract placement.** This plan doesn't decide where the catalog lives. Options include a first-party pack under the existing pack identity rules, or a contract successor naming a product rule set. That is decision D2 in §11.

---

## 4. Corpus and ground truth (O1)

### 4.1 Three tiers

| Tier | What | Where it lives | Pinned by |
|---|---|---|---|
| **T1, oracle fixtures** | Small, purpose-built projects per cell **and per mode**, with an independent oracle: positive cases, negative cases and typed-refusal cases | `tests/qualification/fixtures/` in product, the owner already planned in COV | per-file SHA-256 and manifest digest, as the preview corpus is |
| **T2, public real repositories** | Real code at pinned commits, chosen by the criteria in §4.2 | Fetched by the harness at the pinned commit. The corpus manifest records the URL, commit, tree digest and licence. No source is vendored into the repositories | the commit plus a tree digest |
| **T3, consented private repositories** | The owner's team code | Run locally only. Only aggregate metrics and adjudication labels leave the machine, never source. No telemetry, consistent with CH13:82-84 | local manifest digest; results labelled `T3-local` |

**T3 needs owner confirmation first** (D6): running OpenSIP on internal code may need an internal security or open-source review.

### 4.2 Selecting T2

Selection criteria cover the shapes a heavy user meets:
- **Rust:**
  - a single crate;
  - a mid-size Cargo workspace;
  - a large workspace with proc-macros and build scripts (L-RS3);
  - a codebase heavy in `cfg` and features;
  - trait-object and generic dispatch (L-RS2);
  - generated code.
- **TypeScript/JavaScript:**
  - a library with `tsconfig` project references;
  - a pnpm, npm or yarn workspace monorepo;
  - a framework application with convention-loaded entry points (L-FW1);
  - mixed CJS/ESM JavaScript without a tsconfig (L-JS1);
  - `allowJs`/`checkJs`.
- **Both:** a polyglot repository with Rust and TypeScript together.
- **Size classes:** small (under 20k lines), medium (20k–200k), large (200k–1M) and very large (over 1M). That's at least two repositories per language per class.

**Candidates.** These are for review; selection is D3.
- **Rust:**
  - **AWS-shaped:** `smithy-rs` (codegen, large workspace) and `aws-lambda-rust-runtime`.
  - **Community:** `ripgrep` (mid workspace), `tokio` (large workspace, heavy `cfg`), `serde` (proc-macro), `axum` (generics, traits), and `rust-analyzer` (very large).
- **TypeScript/JavaScript:**
  - **AWS-shaped:** `aws-cdk` (very large monorepo) and `aws-sdk-js-v3` (generated code).
  - **Community:** `typescript-eslint` (project references), `vite` (mixed), `express` (CommonJS JS), and a Next.js application (framework entry points).
- **Python, for §8:** `boto3`/`botocore`, `fastapi`, and a Django application.

### 4.3 Measuring precision (Q2)

Real repositories have no answer key, so precision is measured by **adjudication**:
1. **What gets adjudicated.** Every finding a gating or repair-eligible rule reports on T2 is adjudicated. Advisory rules use a stratified sample of at least 100 per rule per language, or all findings if there are fewer.
2. **How.** Each finding gets two independent adjudications, *true*, *false* or *unclear*, each with a written rationale citing code. Disagreements go to a third adjudicator. Adjudicators can be the owner, a reviewer agent or the lead; the label records who.
3. **Where labels live.** In a digest-pinned **adjudication ledger**, keyed by `finding-key2` and repository commit. Labels carry forward across runs while the key matches, so later runs only need adjudication for findings they haven't seen before.
4. **Scoring.** Precision is true ÷ (true + false). *Unclear* is reported separately, and if it rises above 5% the rule's definition is reviewed.

### 4.4 Measuring recall (Q3) and honesty (Q4)

Recall uses **known answers**:
- **Seeded defects.** A mutation tool injects known problems at recorded locations into copies of T2 repositories: an unused export, an unused `pub fn`, an unused dependency, a cycle, a clone. Recall is the share found. A seeded defect inside an unresolved region (a dynamic import, `dyn` dispatch, a missing proc-macro output) must come out **indeterminate**. If it comes out clean, that is a Q4 failure.
- **Cross-tool differential.** The same pinned repository is run through established tools: Knip and ts-prune for TS/JS, rustc's `dead_code`/`unused` lints and cargo-udeps/cargo-machete for Rust. Every disagreement is adjudicated. A finding another tool reports and OpenSIP misses, inside OpenSIP's claimed-complete scope, is a recall miss. A finding OpenSIP reports and others miss is adjudicated for precision.
  - These tools run only inside the harness, at pinned versions. They are never a product dependency and never a fallback, consistent with D-007 and BP:716-717.
- **T1 oracles** give exact recall at cell level, as the design already requires.

### 4.5 Measuring stability (Q5)

A **refactor suite** applies semantics-preserving edits to pinned T2 repositories:
- formatting;
- reordering items;
- moving a module;
- renaming an unrelated symbol;
- adding unrelated code;
- splitting a file.

After each edit, it compares findings by `finding-key2`. Findings the edit doesn't touch must survive. A moved or renamed subject must either match through declared correspondence or come out explicitly unmatched (IE:1564-1567). It must never be silently treated as a new finding plus a fixed one. **O6 is a design gap:** no mechanism yet exists for declaring correspondence for a rename or move. This plan asks for one (D7).

---

## 5. Performance (Q6, O3, O4)

### 5.1 Statistics

The product regime (AQ:273-287) governs every new cell: median of 7 runs after 3 warmups, ×1.20 time and ×1.25 RSS against a reviewed baseline, plus reviewed absolute bounds. The preview's p95 regime stays a historical TypeScript floor. **D1** asks for QG items[12]'s evidence text to be corrected to the product statistics (O9).

### 5.2 Proposed absolute budgets, whole-repository `analyze`

These are measured on the slowest D-102 runner class that each class is held to. They need owner approval (D4) and are exploratory until then.

| Size class | Cold, median | Warm (retained evidence), median | Peak process-tree RSS |
|---|---|---|---|
| small (< 20k lines) | ≤ 5 s | ≤ 2 s | ≤ 1 GiB |
| medium (20k–200k) | ≤ 30 s | ≤ 8 s | ≤ 2 GiB |
| large (200k–1M) | ≤ 120 s | ≤ 30 s | ≤ 4 GiB |
| very large (> 1M) | measured and reported; budget set after first measurement | | |

**Rust caveat.** Rust semantic cells need a sealed dependency set and, in prepared mode, build outputs (L-RS1, L-RS3, L-RS4). Budgets exclude the user's own `cargo build` but include everything OpenSIP does itself. The harness reports the two separately.

### 5.3 Incremental and changed-scope analysis (O4): the most important open product decision

Daily use means re-running after small edits, from the shell, in CI on a pull request, and from coding agents in a loop. The design today is one-shot. Warm runs use a "new process … retained declared cache; no reused provider process". An authoritative cache hit needs full replay admission. A one-shot design can meet the medium-class budget, but not an edit-loop expectation of about 1–2 s on a medium repository.

This plan recommends deciding **before the M3 provider protocol is fixed**, because retrofitting incremental analysis into a fixed protocol is expensive. Options, for D5:
- **(a) Changed-scope analysis.** Re-analyze only the subjects whose inputs changed, with an exact dependency closure, and reuse admitted evidence for the rest under replay rules. Coverage stays honest: anything not re-established is disclosed.
- **(b) A resident host**, a daemon per project, for editor and agent loops. It keeps the provider warm under the same admission rules (SYN:275, "measure, then park or promote").
- **(c) Both, staged:** (a) at M3–M4 and (b) at M5 alongside `agent-serve`.

The lead recommends **(c)**. The proposed target for (a): a single-file edit on a medium repository re-analyzes in ≤ 2 s median, warm.

---

## 6. Explanations (Q7, O5)

Each finding should let a developer act without opening the tool's documentation. The plan proposes these structured fields, rendered by every advertised renderer:
- **Reason:** the rule's `messageCode` plus parameters, as now.
- **Evidence path:** the chain of facts that produced the finding. For example: export `X` in `a.ts` → no resolved reference in the examined universe → universe complete for `references@resolved-binding` in mode `ts-tsconfig`.
- **Scope statement:** what was examined and what was not, taken from Coverage. For example: "2 dynamic imports in `src/plugins` are unresolved; this finding holds outside them."
- **Suggested action:** a fixed text per rule and situation. Repair-eligible findings point to `repair preview`.
- **Limitations:** the cell limitation IDs that applied, such as L-RS2.

**Measurement.**
- **Field presence.** Every finding must carry the reason, evidence path and scope statement. This is checked mechanically, and the target is 100%.
- **Usefulness.** A rubric scores a stratified sample of 50 findings per rule from 1 to 5 on whether a developer could act without further investigation. The target is ≥ 4 average.

This needs a contract successor for the finding shape and the renderers (D8).

---

## 7. Exploratory measurement (O7)

M3 needs measurements well before M6 qualification. This plan proposes a labelled class of evidence, consistent with AQ:212-214 ("synthetic reports are tagged reference-only and cannot be promoted"):
- **What it is.** An **exploratory quality report** uses the product-quality report schema with `standing: "exploratory"`, records the product commit, corpus digests, runner and tool versions, and is never a G13 input.
- **How it's used.** It may inform design decisions, budgets and rule definitions, and it is cited as such.
- **Promotion is forbidden.** A G13 qualification run re-executes from scratch, on qualified runners, at a release candidate.

---

## 8. Python and later languages (O8)

**Python is the third language.** Adding it needs:
- an explicit support decision (`10-mvp-and-future-scope.md:41`);
- a D-007-shaped capability matrix with its own corpus and thresholds;
- D-008/DR-G14 self-contained closure evidence;
- a grammar-registry successor (BP:696-697);
- platform closure under DR-126.

**The plan's proposal:**
1. **Now, at M3: third-language readiness.** M3's provider protocol, cell vocabulary, Coverage and rule catalog get a review that checks for no TS- or Rust-only assumptions. Python is the test case. Its concerns include:
   - dynamic attribute access and imports, which are like L-JS2;
   - `__all__` and re-exports;
   - namespace packages;
   - type-hint-only versus runtime references;
   - `TYPE_CHECKING` blocks;
   - decorators and framework entry points, which are like L-FW1;
   - `pyproject.toml` workspaces.
2. **The Python support decision follows M3,** with this plan's eight dimensions as its acceptance structure.
3. **The analyzer is a decision (D9).** DR-119's self-contained closure rule favours a native, bundleable analyzer over one that needs a Python or Node runtime the user must manage. The candidates differ in maturity and in how much semantic depth they offer, and the choice should come from measuring them on the Python T2 corpus.
4. **The corpus starts now.** Pinning Python T2 repositories costs little and lets the third-language review use real code.

**A language-onboarding kit.** It holds the matrix template, mode and limitation patterns, the corpus tiers, the rule-catalog mapping and the readiness review. It is written once, proven with Python, and reused for every later language.

---

## 9. Milestone mapping

| Milestone | Quality work |
|---|---|
| **Before M3 code** | Owner decisions D1–D9. Pin the T2 manifests. Write the harness design. Write the rule catalog draft. |
| **M3** | T1 fixtures for all 57 supported cells, mode-specific, plus typed refusal for 6 and non-advertisement for 3. Q1 and Q4 on T1. Exploratory Q2–Q6 on T2 for the catalog's facts. Changed-scope analysis (D5a), if decided. The third-language readiness review. **A dogfood checkpoint:** the owner runs `analyze` on T3 and the findings are adjudicated. |
| **M4** | Explanations rendered in every format (Q7). SARIF parity (G17). The rubric on the sample. |
| **M5** | Baselines and deltas: the refactor suite (Q5) and the rename correspondence mechanism. Policy rules through the DSL. Repair verify, re-measured for precision. `agent-serve` and the resident host (D5b). |
| **M6** | G13 qualification on D-102 runners from scratch: Q1 and Q4 exact, Q2/Q3/Q5/Q6/Q7 against the approved targets. No exploratory report is promoted. |

**Continuous.** Every product change that touches a provider, rule or evaluator reruns T1 fully and a T2 smoke subset in CI, and fails on any regression against the last accepted exploratory baseline.

---

## 10. What else is missing from the project plan and the product

The owner asked for anything else missing. In order of importance for daily use:
1. **Incremental analysis and a resident host** (§5.3). This is the biggest gap between the design and an edit-loop tool.
2. **An agent protocol.**
   - `agent-serve` is selected for M5, but its wire protocol and transport are unspecified, and MCP appears nowhere in the product contracts.
   - Coding agents are a primary consumer for a team that writes code with them.
   - Recommendation: select MCP as the `agent-serve` transport, under the same admission and no-mutation rules (`14-repository-and-module-layout.md:474`).
3. **Editor integration.**
   - Nothing covers in-editor diagnostics; the TUI is excluded, and the LSP is not mentioned.
   - Recommendation: once the resident host exists, an LSP projection of findings, read-only and with no new authority.
4. **The rule catalog** (§3) and **explanations** (§6). Without these, OpenSIP produces correct facts but not findings a developer can act on.
5. **Workspace topology.** `ProjectId` across clones and worktrees, and polyglot workspaces, are thin (SYN:279). Amazon-style multi-package workspaces, built from packages in separate repositories, need an explicit shape in discovery (FW-01/FW-14) and a T2/T3 representative.
6. **The platform population.**
   - The qualified runner classes are macOS and Ubuntu (D-102).
   - If the team develops on Amazon Linux (AL2023) cloud desktops, that platform should join the supported population under DR-126. Otherwise the tool is unqualified where it is used most.
7. **Code review integration.** SARIF covers GitHub-style hosts. Internal code-review tools need a projection from the JSON envelope, plus a recommended CI recipe for `audit --profile code-regression`.
8. **The effort model and critical path** (SYN:286-287), still absent. M3 is the largest milestone, and its critical path, the providers and the corpus, should be visible.
9. **Record hygiene.** Stale text contradicts current authority:
   - four places say no quality corpus exists (`02-…:334-338`, `prototype-evidence-reference.md:26-30`, `05-…:102`, register DR-203), against DR-118's SATISFIED row;
   - chapter 10 lines 143 and 154 call the roles open, against line 41;
   - the register's DR-011 subledger reads OPEN against D-372 condition 1.

   A record-only correction batch would stop these confusing future readers and reviewers.
10. **Implementation authorization.**
    - The register says D-372 condition 5, implementation authorization, is NOT MET (register:402), yet M1 and M2 are implemented under the owner's direction.
    - The authorization that actually exists should be recorded in the register, so the record matches reality.

---

## 11. Decisions this plan asks for

| ID | Decision | Owner | Lead recommendation |
|---|---|---|---|
| D1 | Correct QG items[12]'s evidence and threshold text to the product statistics (AQ §3) | lead (record correction) | Do it, as a record-only successor |
| D2 | Where the first-party rule catalog lives | lead, with owner sign-off | A first-party pack with a reviewed rule-set successor |
| D3 | T2 repository selection | lead, with owner sign-off | The §4.2 candidates, at least 2 per language per size class |
| D4 | Q2–Q8 targets and the §5.2 budgets | **owner** (product thresholds) | As proposed; revisit after the first exploratory measurement |
| D5 | Incremental and resident-host strategy | **owner** (product scope) | (c) staged: changed-scope at M3–M4, resident host at M5 |
| D6 | T3 private corpus and internal approval | **owner** | Confirm internal approval first, then run local-only |
| D7 | The rename and move correspondence mechanism | lead (IE successor) | Declared correspondence in the baseline, plus a refactor suite |
| D8 | The finding explanation fields | lead (WS/IE successor) | As in §6 |
| D9 | The Python support decision and analyzer choice | **owner** | Decide after M3's third-language review, by measurement on Python T2 |
| D10 | MCP as the `agent-serve` transport; an LSP projection | **owner** (product scope) | Yes to both, at M5 |
| D11 | Amazon Linux in the platform population | **owner** | Yes, if it is the team's development platform |

## Not claimed

- No measurement has been taken.
- No target is approved.
- No gate is qualified.
- No contract is changed.
- The repository candidates are unchecked against licence and size.
