# M3 analysis-quality plan — proposal r2

2026-10-03. Claude Opus 5.5, implementation lead. Written at the owner's request ("draft the M3 analysis-quality plan"). r1 (`PLAN-r1.md`, sha256 `4e1c0901…`) was reviewed by GROK2 (fact validation, 7 required findings) and CODEX2 (method, 10 required findings). r2 answers all 17 and records the owner's decisions of 2026-10-03.

## Standing

**This is a plan, not law and not a contract successor.** It changes no accepted contract, gate, threshold or register row. Where it needs one, it names the owning row and lists the change in §11. Each such change is made later, through its own reviewed successor. No measurement has been taken.

**Owner decisions recorded here.** On 2026-10-03 the owner decided D4, D5, D6, D9 (timing), D10, D11, the workspace shapes (D15) and the record-hygiene batch (D16). §11 marks each as decided. A decided target is an approved product target; it is still not a qualification threshold until the DR-G13 successor in D13 admits it (§7).

**What it plans.** How OpenSIP will define, measure and gate the quality of what a developer actually sees: facts, findings, Coverage, stability, speed and explanations. It covers TypeScript/JavaScript and Rust at M3, Python as the third language, and the method for adding more.

**Why now.** The owner intends to use OpenSIP daily on a Rust, TypeScript and Python team, and judges it by the quality of its analysis. M3 is where the analysis gets built (BP:887), and no executable product corpus exists yet (O1). The three-reviewer synthesis called the corpus "the largest shared unmeasured product risk" (SYN:290); that synthesis is steering advice, not register law (SYN:297-299), and its "does not exist" wording predates the preview corpus. The crash matrix plays this role for durability at M2; this plan does the same for analysis at M3.

**The authority this plan sits under.**
- **The product contracts** (`docs/v2/contracts/product-v1/`), applied under D-372.
- **DR-118** (language-native quality) and **DR-G13** (`harness.DR-G13.product-v1`; QG items[12], `qualification-gates.applied.v1.json:262-275`; owners "Language quality + Product + Release engineering", QG:264).
- **The 66-cell native capability matrix** (NCM `/cells`, 66 entries from `native-capability-matrix.v2.json:206`; NE §1.3, NE:584-617).
- **The build plan's milestone rows** (BP:882-890).

Short names used below:
- **AQ:** `docs/v2/contracts/product-v1/admission-and-qualification.md`
- **NE:** `docs/v2/contracts/product-v1/native-evidence.md`
- **WS:** `docs/v2/contracts/product-v1/workflows-and-surfaces.md`
- **IE:** `docs/v2/contracts/product-v1/identity-and-evidence.md`
- **AQC:** `docs/coop/completion/analysis-quality-completion.v2.md`
- **LQM:** `docs/coop/completion/language-quality-matrix.completed.v2.json`
- **QG:** `docs/coop/design-corrections/qualification-gates.applied.v1.json`
- **NCM:** `docs/coop/design-corrections/native/native-capability-matrix.v2.json`
- **RS3:** `docs/coop/design-corrections/foundation/product-quality-report.schema.v3.json`
- **CS:** `docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json`
- **SMAP:** `docs/coop/design-corrections/current-source-map.proposed.md`
- **CD:** `docs/coop/COORDINATOR-DECISIONS.md`
- **REG:** `docs/v2/architecture/08-decision-and-readiness-register.md`
- **BP:** `docs/v2/architecture/implementation-boundaries-and-build-plan.md`
- **SYN:** `docs/v2/architecture/11-three-reviewer-direction-synthesis.md`
- **CH13:** `docs/v2/architecture/13-evidence-workflows-and-product-contracts.md`

---

## r2 changes and review responses

**Required findings.**

| Finding | Section | Change |
|---|---|---|
| GROK2 RF-1 | §1, §5.1 | The product statistic is median elapsed time and the maximum of the seven per-run peak RSS samples (AQ:268-272; RS3:78-101). RSS is no longer called a median. |
| GROK2 RF-2 | §1 | Split into two decided rules: D-007 item 8's typed refusal (CD:885-888), and DR-G25's Coverage-indeterminate missing TypeScript rung plus no silent fallback for closure, resolution, external-world and Coverage deficiencies (QG:507-511). |
| GROK2 RF-3 | §1 O5 | The finding shape is cited at IE:190 and CS:1635-1648. O5 is now "no explanation fields", not "messageCode only". |
| GROK2 RF-4 | §5.2, §9, §11 D12 | D-102 removed. Budgets are held on G13's own trusted runner lanes (AQ:190-198, AQ:229-230, AQ:238-239), with a proposed reference shape taken from the preview worker (AQC:138-141). Choosing it is new decision D12. |
| GROK2 RF-5 | §7, §11 D13 | The claim that RS3 accepts `standing` is withdrawn; RS3 is closed (RS3:4-18). Exploratory results use a separate envelope that references unchanged RS3 observations (D13). |
| GROK2 RF-6 | §4.1 | Corpus acquisition is a separate, explicit, networked harness step. Exploratory and qualification runs read only pinned local bytes, offline (AQ:346; QG:117; AQC:139). No exception is needed. |
| GROK2 RF-7 | §4.4, §7 | Cross-tool differentials stay outside G13 (GROK2's first option). They only nominate candidate cases; a case counts only after adjudication turns it into a curated corpus case with a pinned expected answer. The "consistent with D-007/BP" claim now covers only "never a product fallback". |
| CODEX2 C2-AQ-R1-01 | §2 Q3/Q4, §4.4, §6 | The scoring unit is now (rule, subject, required relation@rung, universe, configuration). Answerability is pinned per case, independently of candidate output. Q3 is answerable recall, and an abstention on an answerable case counts against it. Q4 is zero unsupported determinate negatives; a sound positive may still fail. Misses are classified by cause. The §6 example is replaced. |
| CODEX2 C2-AQ-R1-02 | §2 Q2, §4.3 | Acceptance uses conservative precision (unclear counts as not true) and a one-sided 95% exact lower bound per rule × language × mode stratum. Too little evidence gives INSUFFICIENT-EVIDENCE, never pass. Rubrics are frozen, labels are blind, calibration items are planted, agreement and conflicts are recorded, a human expert decides high-impact cases, and correlated agent votes count once. |
| CODEX2 C2-AQ-R1-03 | §4.3 | A label is bound to a label key over its truth-relevant inputs. `finding-key2` only proposes correspondence. The section defines re-adjudication triggers, keeps superseded labels, and adds a blind drift audit. |
| CODEX2 C2-AQ-R1-04 | §4.4 | Mutants are validated, with eligibility and invalid-seed accounting. The suite adds fix reversals and hard negative lookalikes, held-out acceptance repositories and mutation families, per-tool proposition mappings, and a four-way disagreement adjudication. |
| CODEX2 C2-AQ-R1-05 | §4.5 | The refactor suite gets an independently reviewed mapping oracle and validation of its semantic invariants. It checks content, Coverage, CODE-NET-NEW and CODE-FIXED, and reports per rule × transformation with a minimum population. A separate determinism suite is added. |
| CODEX2 C2-AQ-R1-06 | §5.1-§5.4 | Pinned workload manifests, phase timings, first-use and preparation-invalidating workflows, an edit taxonomy, missing/stale/broken-build controls, yield beside time, tails as diagnostics only, reviewed stress bounds, and concurrent process-tree RSS. |
| CODEX2 C2-AQ-R1-07 | §5.3 | The owner decided D5 (c). The reuse requirements are now obligations INC-1 to INC-8 that the M3 law must meet before the provider protocol is fixed, plus a measurement spike. The unmeasured "one-shot cannot meet it" claim is removed. |
| CODEX2 C2-AQ-R1-08 | §3 | Each rule spec has a fixed set of fields. `rs-unused-pub-item` and `unused-export` are split into a workspace-unreferenced claim, a closed-world claim and per-finding repair eligibility. Cycles and clones gate only by declared policy. A dependency's scope comes from its target. The catalog draft is a prerequisite for scoring. |
| CODEX2 C2-AQ-R1-09 | §8, §9, §11 | The blanket "D1–D9 before M3" is replaced by a dependency table. T3 is gated on the licence (D6/D14), with a public T2 alternative. The M3 checkpoint is an internal-harness checkpoint; CLI dogfood moves to M4 (BP:887-888). Draft rules are evaluated non-authoritatively at M3. Q8 is in the M6 row. |
| CODEX2 C2-AQ-R1-10 | §7, §9, §11 D13 | New decision D13 covers the exploratory envelope now and a DR-G13/report/harness successor before any Q2–Q8 target qualifies. CI separates exact correctness checks from thresholded performance checks and gets a reviewed baseline-advance process. |

**Non-blocking items adopted.**

| Item | Where |
|---|---|
| CODEX2 N01, noise and usefulness metrics | §2: FP/KLOC and findings/KLOC (Q2), time to first trustworthy result (Q6), triage cost (Q7), answerable population and accepted/dismissed counts (Q8). Reported, no new target. §6 adds proof-join checks and bad-tail review. |
| CODEX2 N02 | §3: cross-crate use and re-export, feature/target fixtures, package-boundary rules and entry-point failures come first. No lint replacement. |
| CODEX2 N03 | §2, §5.1: evaluation criteria are frozen before acceptance measurement, and tails are reported. |
| CODEX2 N04, fuller Python concerns | §8: environment, import-path, stub, native-extension, monkey-patching and broken-input cases; an input/environment/mode matrix in the onboarding kit; `pyproject.toml` is not given Cargo semantics. |
| CODEX2 N05 | §10 reordered: trust, yield and triage cost come before transport breadth; time is reserved for maintaining oracles and ledgers. |
| CODEX2 N06 | §11 keeps the owner/lead split and names a successor owner per row. |
| GROK2 NBO-1, cell-count citation | Standing, §1: count from NCM `/cells`; limitations NE:584-617. |
| GROK2 NBO-2 | O6: correspondence states exist (IE:211-213; WS:383-389). The declaration mechanism and a churn metric are what is missing. |
| GROK2 NBO-3, graph-query bounds | O3 is limited to `analyze`; the existing graph bounds (WS:1163-1165) are cited and exercised by stress fixtures (§5.4). |
| GROK2 NBO-4 | O9 and §10: the second copy of the p95 regime (AQC:136-150) and the extra stale text are forwarded to the record-hygiene batch. "Why now" no longer treats SYN as authority. |
| GROK2 NBO-5 | §2: Q8's measurement is required (SMAP:67; CH13:77-84). Its target of 0 is this plan's proposal, now owner-approved, not a pre-existing gate. |
| GROK2 NBO-6, PolicyDocumentV2 placement | §3, D2: catalog rules are PolicyDocumentV2 rules (WS:593-610). A first-party pack is a successor against CH13:37-40. |

---

## 1. What the design already decides, and what it leaves open

This plan builds on the following. It does not reopen any of it.

**Decided.**
- **Fact correctness is exact.** Expected facts, Coverage and graph results must equal an independent oracle by set equality, so precision and recall are both 1.0 on a finite corpus (AQC:127-130; AQ:257-266). The gate computes counts and correctness itself, and reads no submitted PASS flag. A report cannot supply its own expected answers (AQ:197-198).
- **The 66 cells.** There are 11 capabilities × 6 modes: 57 SUPPORTED-DESIGN, 6 UNSUPPORTED-TYPED and 3 NOT-SELECTED (NCM `/cells`). The limitations are L-JS1–3, L-RS1–4, L-FW1 and L-CL1 (NE:584-617; the NE table omits the `inventory` row).
- **Refusal, not degradation.** Each capability needs a negative test class in which the role refuses, typed and loud, rather than degrading to a weaker parser, syntactic tier, semantic model, graph or finding model (D-007 item 8, CD:885-888).
- **A missing rung is indeterminate.** A missing required TypeScript semantic rung is typed Coverage-indeterminate, and a silent syntax fallback fails. No input-closure, resolution, external-world or Coverage deficiency falls back silently; stale input, provider-unavailable and operational fault stay distinct (DR-G25, QG:507-511; routed to M3 at BP:1029).
- **Honest Coverage.** Outputs separate "no matches", "unsupported" and "attempted but insufficient" (CH13:94-98). Zero findings never establish complete analysis (WS:467). Completeness is RC-2 (NE:2113). Dynamic edges propagate to every target they could reach (NE:2230). Sufficiency is relative to the requirement and the target (NE:2260).
- **Stable finding identity.** `finding-key2` excludes line offsets, messages and concrete evidence (IE:188, IE:199-202). Correspondence is syntactic, not semantic; renames require explicit subject correspondence; and a stable fingerprint is not proof that detector semantics are unchanged (IE:211-213).
- **Baseline deltas** follow the delta-class model (WS:350-358). A removed detector can't hide a new bug (WS:435-438). No fingerprint is minted for an unmatched occurrence (WS:383-389).
- **Performance statistics for product cells.** Each benchmark records 3 warmups and then 7 measured runs. The gate takes the **median elapsed time** and the **maximum of the seven peak-RSS samples**. A regression fails above 1.20× median time or 1.25× peak RSS against a reviewed baseline, and the fixture's reviewed absolute bounds also apply. A new cell needs a reviewed initial baseline and budget. Cold and retained-evidence workloads are separate fixtures (AQ:268-282; RS3:78-101).
- **Real repositories are required.** The corpus must include "public or consented exact repository/configuration shapes, confirmed workarounds and manual-correction counts", and synthetic cases alone cannot qualify discovery (QG:271; CH13:77-84; FW-14, SMAP:67).
- **Offline.** Ordinary analysis and discovery do no implicit download (AQ:346), and supported runs need no network (DR-G06, QG:117).

**Open or absent.** This plan exists to fill these gaps:
- **O1. No executable product corpus.** Only the TypeScript preview corpus is pinned (1,019 files, `quality-corpus-manifest.v1.json`). The 477 native cases are design-reference scenarios; executable fixtures must be admitted before a cell is QUALIFIED (QG:271; AQ:244-246). Ten capabilities share one `corpusCases` tuple across the TS/JS and Rust modes.
- **O2. No first-party rule catalog.** Dead code, unused exports and boundary rules appear only as workflow fixture IDs. The preview ships one rule, `module-import-cycle` (AQC:52-63). The design measures precision and recall on facts, never on findings.
- **O3. No `analyze` budgets outside the TypeScript preview.** There is no latency or RSS budget for any JS, Rust or syntax-only cell, and no real-repository latency target. DR-G05 caps are deferred (D-006). Graph *queries* are already bounded: page ≤ 1,000, produced items ≤ 100,000, depth ≤ 64, visited nodes ≤ 1,000,000 (WS:1163-1165). Whole-repository `analyze` has no work or termination bound.
- **O4. No incremental, changed-scope or resident-host obligation** (SYN:275-276).
- **O5. No explanation fields.** A finding (`finding3`, IE:190; `FindingSurface`, CS:1635-1648) carries a rule, subject, severity, message code and parameters, correspondence state and evidence references. It has no scope statement, suggested action or quality requirement. Remedies attach to terminations, not findings.
- **O6. No declared rename/move correspondence and no churn metric.** Matched and unmatched states exist (IE:1563-1567; WS:383-389). What is missing is a way to declare that a renamed or moved subject is the same, and any measurement of identity churn.
- **O7. The status of exploratory measurements is undefined.** AQ:212-214 covers synthetic reports only. Nothing covers real measurements taken before qualification.
- **O8. Python is absent.** `.py` is `unsupported-file`, `no-bundled-grammar` (NE:304-306).
- **O9. Two statistical regimes are cited inconsistently.** QG:268-269 names "cold/warm p95" and "thresholds DECIDED by D-369", while AQ §3 uses median time and maximum RSS. AQC:136-150 holds the preview regime, which is correct for the preview but reads as general method.

---

## 2. What "excellent" means: eight quality dimensions

**The scoring unit** for Q2–Q5 is a **case**: (rule, subject, required relation@rung, universe, configuration). Configuration means the mode, target, features, cfg and prepared-input set. Every corpus case pins its expected answer independently of any candidate run:
- **determinate-positive**: a finding is required;
- **determinate-negative**: a no-match is required;
- **must-abstain**: required evidence is insufficient under target-relative sufficiency (NE:2260), with propagation (NE:2230) applied.

The case's "answerable" and "abstain" labels come from the corpus oracle. Candidate Coverage never chooses which cases are scored.

| # | Dimension | Measured by | Target (owner-approved, D4) | Definition corrected in r2 |
|---|---|---|---|---|
| Q1 | Fact correctness | Oracle set equality per cell (existing) | Exactly 1.0 | none (existing law) |
| Q2 | Finding precision | Adjudicated findings on T2 (§4.3) | Gating and repair-eligible ≥ 0.99; advisory ≥ 0.90 | The target applies to the one-sided 95% exact lower bound of conservative precision (true ÷ all reported) per rule × language × mode. Too little evidence gives INSUFFICIENT-EVIDENCE. |
| Q3 | Finding recall | Validated seeds and curated cases (§4.4) | ≥ 0.95 | Answerable recall = found ÷ answerable positives. An abstention on an answerable case counts as a miss. |
| Q4 | Coverage honesty | Must-abstain and insufficient-evidence cases (§4.4) | Zero; any one is release-blocking | Zero unsupported determinate negatives: no clean verdict or no-match on a case whose required evidence is insufficient. A sound positive may still determine fail (WS:600-604). |
| Q5 | Stability | Refactor suite plus a determinism suite (§4.5) | ≥ 0.99 survival of unaffected findings; zero spurious CODE-NET-NEW | "Unaffected" comes from an independent mapping oracle. Zero spurious CODE-FIXED as well. Determinism must be exact. |
| Q6 | Speed | Product statistics on pinned workloads (§5) | §5.2 budgets; incremental ≤ 2 s (§5.3) | Held on the D12 runner, not D-102. Yield is reported beside time. |
| Q7 | Explanations | Field and proof-join check, plus a rubric (§6) | 100% fields; rubric average ≥ 4 of 5 | Every sample item scoring ≤ 2 is reviewed and dispositioned. |
| Q8 | Zero-config usefulness | Manual corrections per pinned repository (FW-14) | 0 for conventional shapes | none. The measurement is required (SMAP:67); the 0 is this plan's proposal, now approved. |

**The corrected definitions are part of D4's approval record.** The owner approved the numbers on 2026-10-03, and the reviewers corrected what Q2–Q6 measure. r2 keeps the numbers and applies the corrections. The change most visible to the owner is Q2: 0.99 now means "0.99 with 95% confidence", which needs about 299 independent error-free gating findings per stratum (§4.3). The D4 revisit after the first exploratory measurement is the point to confirm or change that.

**Reported beside the targets, with no target yet** (CODEX2 N01). These are set at the D4 revisit, not now:
- **Q2 noise:** false positives and total findings per 1,000 analyzed hand-written source lines, per rule and repository. Generated and vendored code is counted separately.
- **Q3/Q8 yield:** determinate yield on answerable cases (positive and negative), per rule and shape, and the answerable population size. Each expected-answerable abstention needs a disposition: a defect, or a reviewed corpus change. A candidate run can't change it.
- **Q6:** time to first trustworthy result. This is the wall time from a clean checkout with no OpenSIP state to the first committed result in which every gating rule is determinate on its answerable population. It includes OpenSIP-driven preparation, and reports the user's own build separately.
- **Q7 triage cost:** median time to triage a finding, measured during adjudication, and accepted versus dismissed counts.

**Principles.**
- **Abstention never earns recall.** Honest indeterminacy is required where evidence is insufficient (Q4). On an answerable case it is a miss (Q3), so it is also visible as lost yield.
- **Precision outranks recall for anything that gates or repairs.** Aggregate precision never authorizes a deletion. Repair stays per finding, gated by `deadCodeRepairEligible` (NE:2237-2242).
- **Freeze before measuring.** Metric definitions, denominators, rubrics and held-out sets are frozen and digest-pinned before any acceptance measurement. Targets are revisited only from exploratory evidence, never by tuning on held-out evidence.

---

## 3. The rule catalog (O2)

**Placement.** A catalog rule is a `PolicyDocumentV2` rule. It has a `ruleProgramRef`, a `subjectEnumeration`, an `emitWhen` predicate tree, `evidenceUse`, `severity` and `gate`, and it is evaluated under strong Kleene (WS:593-610). The preview enables no additional rule pack (CH13:37-40), so a first-party product pack is a reviewed successor against that boundary (D2).

**The catalog draft is a prerequisite for Q2/Q3 scoring.** Each rule spec records:
- **Subject population:** universe, subject kind and include/exclude.
- **Predicate:** the exact proposition, in words and as `emitWhen`.
- **Selected configurations:** mode, targets, features, cfg and dev/build/test scope.
- **Origin and external-consumer policy:** the `ClosedWorldV2` fields it needs (NE:2210).
- **Minimum sufficiency:** the relation@rung and Coverage that must be complete for a determinate negative.
- **Negative lookalikes:** the legitimate cases that must not fire.
- **Default:** gating by default, advisory, or gating only after declared policy.
- **Message, explanation template (§6) and limitations.**

**The initial catalog.** The highest-value differentiators come first (CODEX2 N02): cross-crate use and re-exports, feature/target-aware dependency use, package boundaries and entry-point recognition. M3 does not replace compiler, security or style lints.

| Rule | Proposition | Default |
|---|---|---|
| `ws-unreferenced-export` (TS/JS) | No reference to the export inside the examined workspace universe | advisory; the explanation says external consumers are possible |
| `unused-export` (TS/JS) | As above, plus `exportsClosed=closed` and `externalConsumers=none-declared` | gating. Existing fixture ID `no-unused-export`. |
| `unimported-file` (TS/JS) | No import or entry-point origin reaches the file; needs `entryPointsRecognized=all` | gating; otherwise indeterminate (L-FW1) |
| `rs-workspace-unreferenced-pub` | A `pub` item with no reference from any workspace crate in the selected targets and features | advisory. rustc's `dead_code` can't see this across crates, which is where OpenSIP adds value. |
| `rs-unused-pub-item` | As above, plus closed world: not reachable from the published API and `externalConsumers=none-declared` | gating. Existing fixture ID `rs-no-dead-fn`. |
| repair eligibility | Per finding, `deadCodeRepairEligible` (NE:2237-2242) | never inferred from aggregate precision |
| `unused-dependency` (TS/JS `package.json`, Rust `Cargo.toml`) | Not used by any selected target that declares it, counting build scripts, proc-macros, tests and features | gating per declared scope |
| `module-import-cycle` | A directed SCC over resolved imports (AQC:52-63) | product default: gating only by declared policy. Preview behaviour is unchanged. |
| `unresolved-import` | Disclosed unresolved specifier | advisory |
| `clone-exact` / `clone-normalized` / `clone-near` | Facts; near is a candidate only (L-CL1) | advisory; never gating by default |
| `boundary-violation` | A project-declared layering rule | gating once declared |

**Required truth fixtures for every dead-code rule:** consumers outside the workspace, re-exports, `pub(crate)`, multi-crate workspaces, feature and cfg variants, test and build dependencies, and framework or generated entry points.

---

## 4. Corpus and ground truth (O1)

### 4.1 Three tiers

| Tier | What | Where it lives | Pinned by |
|---|---|---|---|
| **T1, oracle fixtures** | Small, purpose-built projects per cell **and per mode**: positive, negative, must-abstain and typed-refusal cases | `tests/qualification/fixtures/` in the product repo | per-file SHA-256 and manifest digest, as the preview corpus is |
| **T2, public real repositories** | Real code at pinned commits (§4.2) | A content-addressed local corpus store on the runner. The manifest records URL, commit, tree digest and licence. No source is vendored into any repository. | commit plus tree digest |
| **T3, consented private repositories** | The owner's team code | Local only. Only aggregate metrics and adjudication labels leave the machine, never source. No telemetry (CH13:82-84; QG:271). | local manifest digest; results labelled `T3-local` |

**Acquisition is outside the run** (RF-6). An explicit, networked harness step, `corpus fetch`, materializes each pinned commit into the local store and verifies its tree digest. Exploratory and qualification runs take the store as a pinned, read-only input and run with no network, as AQ:346, QG:117 and AQC:139 require. A run whose bytes don't match the digest refuses. Fetching is harness tooling, never a product command, so no exception is needed.

**T3 is gated on the licence, not on a separate approval** (D6, decided). The owner has confirmed that running OpenSIP on internal Amazon code is acceptable as long as OpenSIP is open source. The owner chose Apache-2.0 (D14). T3 starts when the product licence unit lands. Until then, every T3 role is covered by T2 and the T2 dogfood (§9).

### 4.2 Selecting T2

The selection covers the shapes a heavy user meets:
- **Rust:** a single crate; a mid-size Cargo workspace; a large workspace with proc-macros and build scripts (L-RS3); a codebase heavy in `cfg` and features; trait-object and generic dispatch (L-RS2); generated code; a broken or partial build.
- **TypeScript/JavaScript:** a library with `tsconfig` project references; a pnpm, npm or yarn workspace monorepo; a framework application with convention-loaded entry points (L-FW1); mixed CJS/ESM JavaScript without a tsconfig (L-JS1); `allowJs`/`checkJs`.
- **Both:** a polyglot repository with Rust and TypeScript together. The `mixed-native-partial` case is the reference (NE:1233).
- **Amazon-style multi-repository workspaces** (D15, decided). A workspace is assembled from packages that live in separate repositories and refer to each other by path or by version. This is a required discovery shape under FW-01/FW-14 (SMAP:54, SMAP:67). T2 approximates it with a pinned multi-checkout workspace built from several public repositories with cross-repository package references. The candidate is the Rust and TS AWS SDK and runtime repositories, subject to D3. T3 supplies a real instance once D14 lands.
- **Size classes:** small (< 20k lines), medium (20k–200k), large (200k–1M) and very large (> 1M), with at least two repositories per language per class. Lines are classed as hand-written, generated or vendored. Each workload also records files, packages, import and reference edges and dependency count (§5.1), so that one class doesn't hide very different graph loads.
- **Held out** (C2-04). At least one repository per language per size class, small to large, is reserved for acceptance. Its findings and adjudications are not inspected during rule development.

**Candidates,** for review; selection is D3, and none has yet been checked for licence or size:
- **Rust:** `smithy-rs`, `aws-lambda-rust-runtime`, `ripgrep`, `tokio`, `serde`, `axum`, `rust-analyzer`.
- **TypeScript/JavaScript:** `aws-cdk`, `aws-sdk-js-v3`, `typescript-eslint`, `vite`, `express`, a Next.js application.
- **Python** (pinned during M3, D9): `boto3`/`botocore`, `fastapi`, a Django application.

### 4.3 Measuring precision (Q2)

**What is adjudicated.** Every gating and repair-eligible finding on T2 is adjudicated. Advisory rules use a stratified sample of at least 100 per rule per language, or all findings if there are fewer.

**Labels and scoring.**
- Labels are *true*, *false* or *unclear*, each with a written rationale citing code. The label is about the rule's exact proposition (§3), not about whether the code is "good".
- **Acceptance** uses conservative precision, p = true ÷ all reported. Unclear counts as not true, because a gating finding burdens the user either way. Resolved-label precision, true ÷ (true + false), is reported for description only.
- **Confidence rule.** The target is met when the one-sided 95% Clopper–Pearson lower bound on p reaches it. With zero errors that needs n ≥ 299 for 0.99 and n ≥ 29 for 0.90. The rule is applied per stratum: rule × language × mode. Strata are never pooled to hide a failing high-cost rule.
- **Insufficient evidence.** A stratum with too few findings for the bound, including zero findings, is INSUFFICIENT-EVIDENCE. It never passes. The remedy is more T2 repositories; until then the rule can ship only as advisory in that stratum.
- **Repository correlation.** Per-repository precision is reported. A stratum dominated by one repository is labelled concentrated. The harness design fixes a clustered confidence method, such as a repository-level bootstrap, before acceptance measurement.
- **Cost.** False-positive cost (triage time, and for repair-eligible rules, the consequence of a wrong deletion) is recorded beside the headline precision, never folded into it.

**Adjudication protocol** (C2-02):
1. **Frozen rubric.** One digest-pinned rubric revision per rule.
2. **Blind, independent labels.** Each finding gets two labels, each written before the adjudicator sees the other label or the detector's evidence path and rationale.
3. **Calibration.** Known-true and known-false items are planted blind in each queue. An adjudicator below the rubric's calibration bar is excluded for that round.
4. **Independence and conflicts.** The author of a rule doesn't adjudicate it. Agent adjudicators from the same model family, or sharing the implementation context, count as **one** vote. Agents assist; they are never independent ground truth on their own.
5. **Resolution.** A disagreement, and every *unclear* label on a gating or repair-eligible finding, goes to a designated human domain expert: the owner or a named delegate. A third procedural vote does not settle it.
6. **Agreement.** Raw agreement and Cohen's κ are recorded per rule and round. Low agreement sends the rule's definition back for review, as does unclear above 5%.

**The label ledger** (C2-03). This is a digest-pinned adjudication ledger.
- **Label key.** Each label is bound to:
  - the adjudicated proposition and rubric revision;
  - the rule definition, program digest and detector semantics major;
  - the repository tree digest and resolved configuration (mode, target, features, cfg);
  - the dependency source set and prepared-output set identities (NE:1261-1276);
  - the finding's evidence references (`finding3`, IE:190).
- **Correspondence only.** `finding-key2` proposes which earlier label might apply. It is never a reason to reuse one, because the fingerprint omits concrete evidence and doesn't prove semantics are unchanged (IE:199-213).
- **Reuse.** A label carries forward only when every label-key component is identical, or when the only changes are outside the label's recorded truth-relevant inputs: the subject, its incoming references and the proof's evidence references. The compatibility check is mechanical and recorded.
- **Re-adjudication triggers:**
  - any change to the rule, rubric, configuration, dependency set or prepared outputs;
  - any change to the subject or its incoming references;
  - any change in detector output that no input change explains.
- **History.** Superseded labels and the reasons for superseding them are kept.
- **Drift audit.** Each round, a random sample of carried labels, at least 5% and at least 20, is re-adjudicated blind. Drift in the sample triggers full re-adjudication for that rule.

### 4.4 Measuring recall (Q3) and honesty (Q4)

**Sources of answerable cases.**
- **T1 oracles** give exact cell-level answers, as the design already requires.
- **Validated seeds.** A mutation is a candidate case only. Each mutant records:
  - its subject;
  - the unmutated control;
  - the expected introduced difference;
  - the selected configuration;
  - its expected answer under the case model (§2).

  An independent check confirms the mutant against the rule's proposition. An added `pub fn` may be public API, cfg-excluded or outside the analyzed targets. A "dependency" may serve a build script, macro or test. Invalid, equivalent and not-enumerated mutants are counted and reported. They never silently become misses or vanish from the accounting.
- **Realistic cases.** These are fix reversals: documented dead-code, unused-dependency and cycle fixes taken from the pinned repositories' history and reverted. They also include hard negative lookalikes: used only by external consumers, re-exported, used only in `build.rs` or a proc-macro, or cfg-gated.
- **Held-out mutation families.** At least one per rule is reserved, with the held-out repositories, for acceptance.

**Cross-tool differential: discovery only** (RF-7, C2-04).
- **Tools:** Knip and ts-prune for TS/JS; rustc `dead_code`/`unused` and cargo-udeps/cargo-machete for Rust. Each is pinned with its executable closure, version, compiler, configuration and adapter.
- **Proposition mapping.** Each tool has a published mapping of which of its findings correspond to which catalog proposition, and where they do not overlap.
- **Adjudication.** Every normalized disagreement is adjudicated as one of:
  - a confirmed comparable defect;
  - an other-tool false positive;
  - semantic non-overlap;
  - unresolved.
- **Counting.** Only a confirmed comparable defect affects recall. It does so by becoming a curated T2 case with a pinned expected answer. A tool's output is never itself an oracle.
- **Standing.** These tools run only inside the harness, never as a product dependency and never as a fallback (BP:716-717 forbids implicit PATH or system-compiler fallback). Differentials are exploratory and are not G13 evidence.

**Q4 cases** are the must-abstain cases, each pinned with the deficiency it must surface:
- propagation from an unresolved referrer to every possible target: module, universe or external (NE:2230);
- partial examination (RC-2, NE:2113);
- missing inputs (L-RS1) and stale or absent preparation (L-RS3/L-RS4);
- a `mixed-native-partial` repository (NE:1233);
- zero-findings runs (WS:467).

A sound positive under incomplete Coverage is a correct determinate fail, not a Q4 failure (WS:600-604).

**Every miss is classified by cause.**
- A miss where the required evidence was complete but the detector or predicate erred is a **Q3 miss**, within the 5% allowance.
- A miss where Coverage claimed complete but the oracle shows required evidence was missing is a **false completeness claim**. That is a **Q4 failure**, and release-blocking.

### 4.5 Measuring stability (Q5) and determinism

**Refactor suite** (C2-05). Each transformation is pinned. Examples: formatting, reordering items, moving a module, renaming an unrelated symbol, adding unrelated code, splitting a file. Each also has an **independently reviewed mapping oracle**: which subjects are unchanged, changed, moved or renamed, and the expected differences in facts, findings and Coverage.
- **Validation.** The harness first checks that the transformation preserves the invariants in the selected configuration: import resolution, recognized entry points and prepared-output freshness. A transformation that fails is recorded and discarded, never scored.
- **Comparison.** Results are compared against the oracle, not against `finding-key2` alone:
  - finding content;
  - relevant proofs and Coverage;
  - no spurious CODE-NET-NEW or CODE-FIXED (WS:350-358, WS:360);
  - ambiguous and unmatched findings counted explicitly (IE:1563-1567).
- **Reporting.** Survival is reported per rule × transformation with counts. A pair with fewer than 20 unaffected findings is reported as insufficient, not as passing.
- **The design gap.** O6's missing declaration mechanism is D7.

**Determinism suite.** This is new.
- **Inputs.** Identical semantic input closures run repeatedly, under varied traversal order and concurrency, and across compatible runner lanes.
- **Comparison.** Canonical semantic results and correspondence must be exactly equal. Only the platform and context distinctions the contract permits may differ, and IDs are not expected to match across different Plans.
- **Basis.** This tests the existing obligation of independent replay across machines (IE:1804-1806).

---

## 5. Performance (Q6, O3, O4)

### 5.1 Statistics and workloads

**Statistics.** The product regime governs every new cell: 3 warmups, then 7 measured runs; median elapsed time and maximum peak RSS; 1.20× and 1.25× against a reviewed baseline; and reviewed absolute bounds (AQ:268-282).
- **Cold fixtures** reset to the cold definition before every measured run, so warmups never turn cold samples into warm ones (LQM:923-924; AQ:279-280).
- **RSS** is the high-water mark of the concurrent process tree's summed RSS, not a sum of separate peaks (AQC:142-146).
- **Tails.** The seven samples and their maximum are reported as diagnostics only. They don't replace the median.
- The preview's p95 regime stays the TypeScript preview's own. **D1** corrects QG:268-269.

**Workload manifests** (C2-06) are pinned per repository and record:
- source counts by class (hand-written, generated, vendored, excluded);
- shape: files, packages, edges and dependencies;
- the selected rules, cells and configuration;
- the exact cold and warm resets and priming;
- start and end events for each run.

**Phase timings.** Each run records discovery/sealing, provider work, admission/replay, commit and delivery. No OpenSIP work is excluded.

**Workflows measured:**
- **core `analyze`**, with inputs prepared;
- **first use**, from a clean checkout, including any OpenSIP-driven preparation;
- **a preparation-invalidating edit.**

The user's own `cargo build` is always reported separately, never hidden and never counted as OpenSIP work.

**Controls:** clean; missing input (L-RS1); stale prepared output (L-RS4); broken or partial build. Each control reports how far the unaffected units progressed (NE:1233). A fast result with low yield is reported as such: completeness and yield always appear beside time.

### 5.2 Absolute budgets, whole-repository `analyze`

These were approved by the owner under D4 on 2026-10-03, to be revisited after the first exploratory measurement. They are held on the **D12 reference runner**, not on D-102 (RF-4). D-102 adopts the hosted fleet class for G03/G04 and does not name G13 (CD:3980-3986). D-006 deliberately leaves `analyze` RSS out (CD:761-764).

| Size class | Cold, median | Warm (retained evidence), median | Peak process-tree RSS |
|---|---|---|---|
| small (< 20k lines) | ≤ 5 s | ≤ 2 s | ≤ 1 GiB |
| medium (20k–200k) | ≤ 30 s | ≤ 8 s | ≤ 2 GiB |
| large (200k–1M) | ≤ 120 s | ≤ 30 s | ≤ 4 GiB |
| very large (> 1M) | measured; budget set after first measurement | | |

**Rust.** Semantic cells need a sealed dependency set and, in prepared mode, build outputs (L-RS1, L-RS3, L-RS4). The budgets cover all of OpenSIP's work and exclude the user's own build. The first-use workflow shows the whole cost.

### 5.3 Incremental and changed-scope analysis (O4; D5 decided)

**Decision.** The owner decided D5 (c), staged: changed-scope analysis at M3–M4, and a resident host at M5 alongside `agent-serve`. The decision is to be made before the M3 provider protocol is fixed. The approved target is a single-file edit re-analyzed in ≤ 2 s median, warm, on a medium repository. r1's claim that one-shot analysis cannot meet an edit-loop target was not measured, so r2 drops it.

**The obligation the M3 law must meet** (C2-07). The schedule above is a plan. The obligations below are the condition that the M3 provider protocol and host law must be able to satisfy, whether or not changed-scope ships at M3. Any of them that needs a contract change goes through the successors named in D5a.

- **INC-1. Optimization versus authority.** Reusing producer work is allowed as an optimization: a cache hit admitted against the new Plan's closure (IE:1610-1626). Reusing an authoritative object is not. Facts, scopes and Coverage bind their snapshot and Plan (IE:177-182). New source makes a new snapshot, Plan and Run. Full replay of an old Run is not evidence for a new snapshot (IE:1586-1592).
- **INC-2. Current admission.** Every result the new Plan uses is reconstructed and admitted under the new snapshot and Plan, with no inherited standing.
- **INC-3. Invalidation.** Invalidation is defined over:
  - enumeration: added and deleted subjects;
  - incoming references: a new referrer to an unchanged subject;
  - negative dependencies: a universal negative depends on its whole universe;
  - configuration and native context, where any field change changes the PlanId (NE:1276);
  - tool and rule closures;
  - dependency source sets;
  - prepared outputs.

  When the host can't bound an invalidation, it falls back to full analysis and discloses that it did.
- **INC-4. Equivalence acceptance.** Paired full-versus-incremental sequences must give canonically equal findings, facts, Coverage and replay outcomes. The sequences cover body-only edits, exported-signature edits, import edits, feature/config edits, generated-input edits, insert/delete, missing inputs, and a dynamic edge introduced into scope that was previously complete.
- **INC-5. Wire contracts.** The current protocols are TS2 and Rust3 (BP:717). Changing an accepted wire contract needs a reviewed successor; the protocols are not unselected.
- **INC-6. Resident host (M5).**
  - Every response is bound to an immutable request snapshot.
  - The single writer and the current grant are preserved (IE:1657-1660).
  - Cancellation, crash and restart, and rejection of stale replies are exercised.
  - Persistent RSS and eviction are bounded and measured.
- **INC-7. Spike first.** Before the protocol is fixed, measure startup, sealing and replay costs for one-shot analysis on medium T2 workloads. Residency must earn its cost against that measurement.
- **INC-8. Disclosure.** A changed-scope result discloses in Coverage what it re-established and what it reused, so it is never presented as a full analysis it wasn't.

### 5.4 Stress and termination

The very-large class and the stress fixtures need independently reviewed work, RSS and termination bounds before qualification (AQ:242-244). The stress fixtures also drive graph queries to their existing bounds (WS:1163-1165) and check for typed, honest exhaustion.

---

## 6. Explanations (Q7, O5)

Each finding should let a developer act without opening the tool's documentation. The plan proposes these structured fields, rendered by every advertised renderer:
- **Reason:** the rule's `messageCode` and parameters, as now.
- **Evidence path:** the chain of admitted facts that produced the finding.
- **Scope statement:** what was examined and what was not, taken from the finding's retained target-relative sufficiency proof (NE:2260). Example: "References to `X` are complete. The 2 unresolved dynamic imports in `src/plugins` have targets bounded to module `src/plugins/registry` (`targetScope=module`), which does not contain `X`." If a dynamic edge's possible targets include `X`'s universe, no determinate negative is emitted at all (NE:2230). r1's "holds outside them" phrasing is withdrawn.
- **Suggested action:** fixed text per rule and situation. Repair-eligible findings point to `repair preview`, and only when `deadCodeRepairEligible` holds.
- **Limitations:** the cell limitation IDs that applied, such as L-RS2.

**Measurement.**
- **Field presence**, checked mechanically, at 100%.
- **Proof join.** Every cited path, span and limitation must join an actual proof input of that finding. Every suggested action must respect the scope statement. Both are mechanical, and both must hold at 100%.
- **Usefulness.** A rubric scores a stratified sample of 50 findings per rule from 1 to 5 on whether a developer could act without further investigation. The target is an average of 4 or more. Every item scoring 2 or less, and every gating or repair-eligible item in the sample, is reviewed and dispositioned.
- **Triage cost** (Q7 report): median triage time and accepted versus dismissed counts.

The finding shape and renderers need a contract successor (D8).

---

## 7. Evidence carriers and exploratory measurement (O7)

**Exploratory envelope** (D13, RF-5, C2-10). RS3 is closed and has no `standing` member (RS3:4-18), and r2 does not change it. Exploratory results go in a separate **exploratory quality envelope**. The envelope:
- references unchanged RS3-shaped observations by digest;
- records the product commit, corpus and ledger digests, the scoring-harness digest, the runner, and tool versions;
- pins every metric definition and denominator from §2–§6;
- declares itself non-qualifying.

It may inform design, budgets and rule definitions, and is cited as exploratory. It is never a G13 input, and it is never promoted. AQ:212-214 covers synthetic reports only, so this is a new class, defined by D13.

**Qualification of Q2–Q8** depends on a reviewed **DR-G13/report/harness successor** owned by DR-G13's owners: Language quality, Product and Release engineering (QG:264). That successor carries the adjudication ledger, case model, confidence rule, refactor and determinism oracles, and explanation scoring. It must keep:
- independent expected answers (AQ:197-198);
- authenticated runners (AQ:190-198).

Until it is accepted, Q2–Q8 are reported at M6 but are not qualification evidence. Q1 and Q4 on T1 fit the existing exact-observation model now. D1's record correction does not add any of this.

**Promotion is forbidden.** A G13 qualification run re-executes from scratch, on the D12 runner lanes, at a release candidate, against the held-out set.

---

## 8. Python and later languages (O8)

**Python is the third language.** Adding it needs:
- an explicit support decision (`10-mvp-and-future-scope.md:41`);
- a D-007-shaped capability matrix with its own corpus and thresholds;
- D-008/DR-G14 self-contained closure evidence;
- a grammar-registry successor (BP:696-697);
- platform closure under DR-126.

**Decided timing (D9, owner, 2026-10-03).** The support decision comes after M3's third-language readiness review. Python T2 repositories are pinned during M3. **The analyzer choice stays open**, to be decided by measuring the candidates on the same pinned propositions and closure costs over Python T2. DR-119's self-contained closure rule favours a native, bundleable analyzer over one that needs a runtime the user must manage.

**The readiness review at M3** checks that the provider protocol, cell vocabulary, Coverage and rule catalog make no TS- or Rust-only assumptions. Python is the test case. Its concerns, with representative cases for each (CODEX2 N04):
- interpreter version and platform-specific environments (venv, conda, system);
- import-path and package-root precedence, relative imports, and editable and namespace-package layouts;
- `__all__` and re-exports;
- installed-dependency and stub/type-information closure, including missing stubs;
- generated code and native-extension surfaces;
- dynamic attribute access, dynamic imports and reflective monkey-patching (like L-JS2);
- runtime versus typing-only references, including `TYPE_CHECKING` blocks;
- decorators and framework entry points (like L-FW1);
- broken syntax and unavailable generated inputs, with typed partial results.

A `pyproject.toml` must not be given Cargo-workspace semantics by default.

**A language-onboarding kit.** It holds:
- the matrix template, and an input/environment/mode matrix;
- the public-interface and entry-point model;
- syntax-only versus semantic advertisement rules;
- the typed partial/error result patterns;
- cross-language unresolved boundaries;
- the corpus tiers and the rule-catalog mapping;
- the readiness review.

It is written once, proven with Python, and reused for every later language.

---

## 9. Milestone mapping

Each row lists only what this plan adds. BP's command and renderer prerequisites and every existing required gate still apply (BP:887-895).

| When | Quality work | Depends on |
|---|---|---|
| **Before the M3 provider protocol is fixed** | INC-1 to INC-8 written into the M3 law, plus the INC-7 spike. T2 manifests pinned, including the multi-repo approximation and Python. Harness design: corpus fetch, case model, ledger, exploratory envelope. Rule-catalog draft (§3). | D5a, D3, D13 (envelope), D2 draft |
| **M3** | T1 for all 57 supported cells per mode, plus typed refusal for 6 and non-advertisement for 3. Q1 and Q4 on T1. Draft catalog rules run **non-authoritatively** through the evaluator's policy module in the harness over admitted M3 facts, giving exploratory Q2–Q4 on T2. Determinism suite. Exploratory Q6 workloads. Multi-repo workspace shapes in discovery. Third-language readiness review. **Internal-harness dogfood checkpoint** on public T2, and on T3 once D14 lands. This is not CLI `analyze`, which completes at M4 (BP:887-888). | D2, D14 for T3 |
| **After M3's review** | Python support decision. Analyzer selection by measurement. | D9 |
| **M4** | CLI dogfood on T2, and on T3 if D14 has landed. Explanation fields in every format, with the rubric (Q7). SARIF parity. Changed-scope analysis meets INC-2 to INC-4 and INC-8 if it ships here. | D8 |
| **M5** | Product catalog through the policy DSL. Baselines and deltas. Refactor suite (Q5) with the correspondence mechanism. Repair verify, re-measured for precision. `agent-serve` over MCP. Resident host under INC-6. | D2, D7, D10 |
| **After the resident host** | LSP projection: read-only, no new authority. | D10 |
| **M6** | G13 from scratch on the D12 lanes, including AL2023 if its DR-126 successor is accepted, against the held-out set. Q1 and Q4 exact. Q2, Q3, Q5, Q6, Q7 and **Q8** against the D4 targets, as qualification evidence only if D13's DR-G13 successor is accepted. No exploratory report is promoted. | D12, D13, D11 |

**Continuous integration.**
- **Exact checks.** Every change touching a provider, rule or evaluator reruns T1 fully, and a T2 smoke subset against pinned expected answers. Any correctness difference fails.
- **Performance.** Thresholded with the product ratios against the last accepted exploratory baseline. A failure is rerun once before it is reported. Noise is never a zero-tolerance gate.
- **Advancing a baseline.** An intentional semantic, rule, oracle or corpus change advances the baseline only through a reviewed baseline-advance record that names the change and its expected effects.

---

## 10. What else is missing from the project plan and the product

The owner asked for anything else missing. In order of importance for daily use:
1. **Trusted ground truth and its upkeep** (§4). Adjudication, answerable yield, broken-build usefulness and triage cost decide whether developers trust the output. Time has to be reserved for maintaining oracles and ledgers as compilers and dependencies change.
2. **Incremental analysis and a resident host** (§5.3; D5 decided).
3. **The rule catalog** (§3) and **explanations** (§6). Without these, OpenSIP produces correct facts but not findings a developer can act on.
4. **The effort model and critical path** (SYN:286-287), still absent. M3 is the largest milestone; the providers, corpus and adjudication should be on a visible critical path before transport breadth is added.
5. **Workspace topology.** `ProjectId` across clones and worktrees, and polyglot workspaces, are thin (SYN:279). Multi-repo workspaces are now a required shape (D15).
6. **Agent and editor surfaces** (D10 decided). MCP is the `agent-serve` transport at M5, under the same admission and no-mutation rules (`14-repository-and-module-layout.md:474`). An LSP projection follows the resident host. MCP appears nowhere in the product contracts, so a WS successor is lead work.
7. **The platform population** (D11 decided). AL2023, the owner team's development platform, joins the supported population. DR-126 is SATISFIED for the preview baseline (REG:315), and its production row binds four canonical machine IDs (REG:435). Adding AL2023 is a DR-126 successor plus a G13 runner lane; that is lead work.
8. **Code review integration.** SARIF covers GitHub-style hosts. Internal code-review tools need a projection from the JSON envelope, plus a recommended CI recipe for `audit --profile code-regression`.
9. **Record hygiene** (D16, approved). The correction batch is in progress separately at `docs/implementation/m3/record-hygiene/`. It covers:
   - the four "no corpus exists" denials;
   - chapter 10's open-roles text (lines 143 and 154 against line 41);
   - the DR-011 subledger.

   GROK2 NBO-4 found more for that batch: SYN:290's denial, `02-distribution-and-components.md:339-341` ("does not invent a support list", against chapter 10 line 41), and AQC:136-150's preview regime, which reads as general method. This plan doesn't edit any of them.
10. **Implementation authorization.** The register says D-372 condition 5 is NOT MET (REG:402), yet M1 and M2 are implemented under the owner's direction. The authorization that exists should be recorded, in the hygiene batch if its scope admits it.

---

## 11. Decisions

Authority: **owner** means product thresholds, scope, consent and licence; **lead** means technical mechanisms and record corrections (CODEX2 N06). Accepting this plan accepts no successor; each is reviewed on its own.

| ID | Decision | Authority | Status | Content | Successor and owner | Blocks |
|---|---|---|---|---|---|---|
| D1 | Correct QG items[12]'s evidence and threshold text to AQ §3 | lead | proposed | Record-only successor. It adds no new acceptance semantics. | QG record successor; lead | nothing in M3 |
| D2 | Where the rule catalog lives | lead, owner sign-off | proposed | First-party `PolicyDocumentV2` rule-program pack, as a successor against CH13:37-40 | WS/pack successor; lead plus evaluator owner | Q2/Q3 scoring (draft), M5 (product) |
| D3 | T2 selection | lead, owner sign-off | proposed | §4.2 candidates, licence and size checked, held-out set named | none (corpus manifest) | M3 harness |
| D4 | Q2–Q8 targets and §5.2 budgets | **owner** | **decided 2026-10-03** | Approved as proposed; revisit after the first exploratory measurement. The numbers are kept and r2's corrected definitions applied (§2), including Q2's confidence rule. | via D13 for qualification | — |
| D5 | Incremental and resident-host strategy | **owner** | **decided 2026-10-03** | (c) staged: changed-scope at M3–M4, resident host at M5; decided before the M3 provider protocol is fixed | — | — |
| D5a | Reuse law INC-1 to INC-8 | lead | proposed | §5.3 obligations, plus any IE/cache/native/TS2/Rust3 protocol successors they need | IE and protocol successors; lead plus identity and native owners | M3 provider protocol |
| D6 | T3 private corpus | **owner** | **decided 2026-10-03** | Running on internal Amazon code is acceptable as long as OpenSIP is open source. T3 is gated on D14, not a separate approval. | — | T3 |
| D7 | Rename and move correspondence declaration | lead | proposed | Declared correspondence in the baseline, checked by the refactor suite | IE successor; lead plus identity owner | Q5 at M5 |
| D8 | Finding explanation fields | lead | proposed | As in §6 | WS/IE successor; lead plus reporting owner | Q7 at M4 |
| D9 | Python | **owner** | **timing decided 2026-10-03**; analyzer open | Support decision after M3's readiness review; Python T2 pinned during M3; analyzer chosen by measurement | language-support decision; owner | Python work |
| D10 | Agent and editor surfaces | **owner** | **decided 2026-10-03** | MCP as the `agent-serve` transport at M5; LSP projection after the resident host | WS successor; lead | M5 `agent-serve` |
| D11 | Platform population | **owner** | **decided 2026-10-03** | AL2023 joins the supported population | DR-126 successor and G13 lane; lead | M6 on AL2023 |
| D12 | G13 `analyze` reference runner | lead, owner sign-off | proposed | §5.2 budgets held per selected signed platform profile lane (AQ:229-230, AQ:238-239) on a dedicated 4 vCPU / 8 GiB worker at concurrency 1, as the preview worker (AQC:138-141). Not D-102. | G13 runner inventory; release engineering | Q6 measurement |
| D13 | Evidence carriers | lead, owner sign-off | proposed | Exploratory envelope now (§7); DR-G13/report/harness successor before any Q2–Q8 target qualifies | DR-G13 successor; Language quality + Product + Release engineering (QG:264) | M3 exploratory reports; M6 Q2–Q8 |
| D14 | Adopt a licence for the product repository | **owner** | **decided 2026-10-03: Apache-2.0** | The owner chose Apache-2.0 and may revisit it while the repositories are private. The design repo has the canonical text (arch `eb439532`). The product unit (LICENSE plus `license` metadata in Cargo.toml and package.json) follows X9-5, because it adds a file to the linear inventory chain. | — | T3 (D6) |
| D15 | Multi-repo workspace shapes | **owner** | **decided 2026-10-03** | Amazon-style multi-repo workspaces join M3 discovery's required shapes (FW-01/FW-14), with a T2 approximation and a T3 instance | SMAP/discovery successor if needed; lead | M3 discovery |
| D16 | Record-hygiene batch | **owner** | **approved 2026-10-03**; in progress | `docs/implementation/m3/record-hygiene/` | that batch | — |

## Not claimed

- No measurement has been taken. Every number is an approved or proposed target, not a result.
- No gate is qualified, and no contract, schema, gate or register row is changed.
- The repository candidates are unchecked against licence and size.
- The product repository does not yet carry its licence. The licence unit is queued (D14).
