# CODEX2 review: M3 analysis-quality plan r2

**Verdict: REQUIRED-FINDINGS.**

Eight r1 findings are resolved at plan level. R2 addresses most of the remaining two, but Q2 still needs a single coherent confidence/qualification rule, and INC-4/INC-8 need compatible semantics for Coverage equality and reuse provenance. Two required plan revisions remain. This review accepts the owner decisions supplied by REQUEST.md and does not reconsider their merits or require implementation/measurement before plan acceptance.

Subject: [PLAN.md](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/analysis-quality/PLAN.md:1), 58201 bytes; SHA-256 `dd351ffe79b59f920b91da6372c7f132c1e9e69ea20bf1fd280b942f1d1936ed`. Both r2 and the r1 snapshot hashes were verified.

## Resolution of every r1 finding

Resolved here means resolved for the purpose of this plan. It does not claim implementation, measurement or acceptance of any future successor.

| R1 finding | Status | R2 locations | Assessment |
|---|---|---|---|
| C2-AQ-R1-01 | RESOLVED | PLAN.md:115-144,247-284,385 | Answerability now comes from an independent case oracle; an answerable-positive abstention reduces Q3 recall. Yield includes positive and negative answerable cases, and each unexpected abstention needs a disposition. Q4 distinguishes unjustified negatives/false completeness from a detector miss with sufficient evidence and permits a sound positive under incomplete Coverage. The explanation now requires a bounded possible-target scope. |
| C2-AQ-R1-02 | PARTIALLY-RESOLVED | PLAN.md:125,133,213-229 | Conservative scoring, unclear-label handling, blind calibration, conflict controls, human resolution, per-rule/language/mode strata, insufficient-evidence outcomes and cost accounting are all present. The independent-binomial zero-error counts are correct. The primary confidence rule remains inconsistent with the deferred clustered method, and the unconditional advisory fallback does not specify how the advisory threshold or unqualified standing applies. Remaining: C2-AQ-R2-01. |
| C2-AQ-R1-03 | RESOLVED | PLAN.md:231-245 | The ledger now binds proposition/rubric, rule/program, source/configuration, dependencies/preparation and evidence. The fingerprint proposes correspondence only. A recorded compatibility check, re-adjudication triggers, superseded-label history and blind drift audit address the original method defect. Implementation of that check remains future harness work, as appropriate for this plan. |
| C2-AQ-R1-04 | RESOLVED | PLAN.md:192,204,249-284 | Mutations are candidate cases until independently validated against the proposition and configuration, with invalid/equivalent/not-enumerated accounting. Fix reversals, difficult negatives and held-out mutation families/repositories are specified. Differential outputs are pinned and mapped, adjudicated into four categories, and contribute only through independently curated expected answers; the differential itself stays exploratory. |
| C2-AQ-R1-05 | RESOLVED | PLAN.md:128,286-301 | Transformations have an independent mapping oracle and invariant checks. Content, proofs/Coverage, both spurious delta directions and unmatched occurrences are covered, with non-vacuous populations. The separate determinism suite compares canonical semantic results under compatible inputs and permits only the contract's platform/context distinctions. |
| C2-AQ-R1-06 | RESOLVED | PLAN.md:138,199-204,307-376 | Pinned workload shapes, per-run cold resets, concurrent process-tree RSS, phase boundaries, prepared/first-use/preparation-invalidating workflows and missing/stale/broken-build controls are now explicit. The edit taxonomy and full fallback are in INC-3/4, tails remain diagnostic, and stress/very-large bounds must be reviewed before qualification. D12 explicitly owns the new runner choice instead of treating D-102 as its authority. |
| C2-AQ-R1-07 | PARTIALLY-RESOLVED | PLAN.md:346-372,462,509 | INC-1/2 correctly reject old-snapshot authority and require current reconstruction/admission. INC-3 covers incoming/negative dependencies and non-file inputs; INC-5 names accepted wire protocols and successors; INC-6 covers request snapshots, grants, writer ordering, failure behavior and persistent memory; INC-7 supplies the spike. INC-4 and INC-8 still require mutually incompatible canonical Coverage equality and reuse-specific Coverage content. Remaining: C2-AQ-R2-02. |
| C2-AQ-R1-08 | RESOLVED | PLAN.md:148-178 | Rule propositions, subject populations, configurations, sufficiency, origin/external-consumer policies, negative lookalikes and defaults are prerequisites for scoring. Workspace-only export/pub information is advisory, closed-world findings are distinguished, repair remains per finding, dependency targets are explicit, and cycles gate only by declared policy while the preview is preserved. |
| C2-AQ-R1-09 | RESOLVED | PLAN.md:194,428,456-468,502-520 | The blanket pre-M3 approval list is gone. Python support follows readiness with analyzer selection open; T3 uses the owner's decided license condition and has a public alternative. M3 dogfood is explicitly internal/non-authoritative, complete CLI dogfood is at M4, draft rule evaluation supplies early finding metrics, and Q8 is included at M6. Owner decisions are treated as supplied authority, not reopened. |
| C2-AQ-R1-10 | RESOLVED | PLAN.md:399-415,468-473,517 | A separate exploratory envelope references unchanged RS3-shaped observations. D13 owns the new metric/report/harness successor with language/product/release owners, independent expectations and authenticated runner inputs. Exploratory reports are not promoted, qualification re-executes, and CI separates exact checks, ratio-based performance and reviewed baseline advancement. |

## Required findings

### C2-AQ-R2-01 (P1) — Make Q2's primary confidence rule and advisory fallback consistent

**Location:** [PLAN.md](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/analysis-quality/PLAN.md:213) — docs/implementation/m3/analysis-quality/PLAN.md:125,133,213-220 (§2 Q2; §4.3)

**R1 relation:** C2-AQ-R1-02.

**Problem.** Q2's normative target and §4.3 specify an exact Clopper-Pearson lower bound per finding stratum, while line 220 says the harness will fix a clustered method such as a repository-level bootstrap. The binomial finding-level bound requires independent sampling units; a concentration label and per-repository descriptive scores do not establish that condition. The plan does not say which bound governs acceptance when findings are correlated, or when the clustered result is insufficient. An ordinary empirical bootstrap also cannot establish the stated confidence at the all-success boundary merely by resampling identical successful repository outcomes. Separately, line 219 permits an insufficient stratum, explicitly including zero findings, to ship as advisory without stating whether it must meet the approved advisory 0.90 confidence threshold or remain explicitly unqualified. Ten independent true findings, for example, have lower bound about 0.741, satisfying neither target.

**Recommended fix.** Keep the approved 0.99/0.90 targets. State a single primary acceptance obligation: use finding-level exact binomial bounds only where the sampling/independence assumptions are established; correlated strata require a preregistered defensible cluster-aware bound and minimum independent evidence, otherwise INSUFFICIENT-EVIDENCE. Label 299/29 as independent-zero-error examples, not sufficient counts for clustered corpora, and require the harness design to resolve the zero-error boundary without a degenerate-bootstrap pass. This can remain a named pre-measurement harness task; no implementation is required now. Make the downgrade rule explicit: a qualified advisory rule must meet its own 0.90 criterion; an interim advisory experiment may instead remain declared unqualified/exploratory, with no Q2 pass or automatic qualification waiver. Specify that standing in D13 and the selected qualification inventory.

**Analytic illustration.** For independent all-success Bernoulli observations, L(n)=0.05^(1/n). L(299)=0.9900308532 and L(29)=0.9018553723. If 300 findings are 100 perfectly correlated findings in each of three independent equal-size repositories, treating n=300 invents independent evidence; in this illustrative cluster-Bernoulli model the same exact calculation over three independent outcomes gives L(3)=0.3684031499. Resampling only observed all-success clusters produces all-success bootstrap replicates. This is a mathematical counterexample, not a product measurement.

**Source anchors:**

- [PLAN.md](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/analysis-quality/PLAN.md:125): The target names an exact per-stratum lower bound.
- [PLAN.md](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/analysis-quality/PLAN.md:218): The independent-zero-error counts are correct; the acceptance rule remains binomial.
- [PLAN.md](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/analysis-quality/PLAN.md:219): Insufficient and zero-finding strata may ship as advisory without a stated advisory qualification condition.
- [PLAN.md](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/analysis-quality/PLAN.md:220): A separate clustered method is deferred without resolving its relation to the primary bound.

### C2-AQ-R2-02 (P1) — Separate reuse provenance from canonical semantic Coverage

**Location:** [PLAN.md](/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/analysis-quality/PLAN.md:364) — docs/implementation/m3/analysis-quality/PLAN.md:352-372 (§5.3 INC-1/2/4/8)

**R1 relation:** C2-AQ-R1-07.

**Problem.** INC-4 requires canonically equal findings, facts, Coverage and replay outcomes between a full run and an incremental run. INC-8 simultaneously requires Coverage to distinguish what was reused from what was re-established. For the same new snapshot, those execution histories differ; encoding that difference in canonical Coverage makes INC-4 fail by construction and changes coverage2 identities. Current CoverageResultV3 has no reuse/provenance field, and identity/replay admit its exact retained payload rather than silently ignoring such data. INC-8 also risks describing a complete current-admitted result as less than full merely because extraction work was reused: under INC-2, every consumed result must already be valid for the current Plan. Actual incomplete obligations need genuine semantic deficiencies, not a cache-history distinction.

**Recommended fix.** Keep the semantic equivalence obligation. Put reuse/recomputation provenance in a separately owned operational measurement or delivery record, with any required reviewed successor, and keep canonical semantic Coverage about the current Plan's examined/resolved sufficiency. Fully re-admitted reusable work may support a complete result; obligations not re-established remain typed incomplete and must never be hidden as a reuse success. Amend INC-8 and D5a accordingly. If a semantic Coverage successor is deliberately chosen instead, explicitly define the contract-approved comparison projection and changed identity/replay obligations; do not claim byte/canonical Coverage equality or silently strip unrecognized fields. Keep the full-vs-incremental comparison tied to the same current semantic input closure and check operational provenance separately.

**Source anchors:**

- [native-evidence.md](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/native-evidence.md:2014): ViewEntryV3/CoverageResultV3 describe semantic examination, resolution and sufficiency, with no reused-work field.
- [identity-and-evidence.md](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/identity-and-evidence.md:183): Scope, fact, Coverage and view identities bind the semantic payload and current inputs.
- [identity-and-evidence.md](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/identity-and-evidence.md:1580): Complete replay checks canonical proofs and referenced output preimages and identities.
- [identity-and-evidence.md](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/identity-and-evidence.md:1610): A hit must join the current Plan/snapshot; reusable producer output is not inherited authority.

## Statistics and citation checks

The one-sided 95% zero-error lower bound is L(n) = 0.05^(1/n). The minimum independent sample sizes are correctly stated: 299 for 0.99 and 29 for 0.90. At 298 the bound is 0.9899975676; at 299 it is 0.9900308532. At 28 it is 0.8985342644; at 29 it is 0.9018553723. These are analytic calculations, not product observations.

The revised median-time/maximum-RSS description matches AQ:268-282 and the seven-sample RS3 arrays. The separate exploratory envelope correctly avoids adding standing to the closed schema. D-102 does not itself name G13 in CD:3980-3986; D12 is explicitly a new runner decision, and qualification must still cover each selected trusted profile lane. The corrected typed-refusal, G25, graph-bound, finding-surface and baseline-correspondence citations are supported by the cited passages.

INC-1/2 agree with new-source/new-Plan admission and the existing cache/replay joins; INC-3/5/6/7 provide the required design obligations. The remaining INC-4/8 conflict is C2-AQ-R2-02. The owner-approved staged strategy is not reopened.

## Recording of owner decisions

The recorded decisions are consistent with the scope supplied by REQUEST.md. No owner decision's merits were re-reviewed.

- **D4:** Approved numeric Q2-Q8 targets/budgets are retained; confidence-method consistency is reviewed as method, not a proposal to change the targets.
- **D5:** Changed-scope at M3-M4 and residency at M5 are recorded as decided; D5a names technical law/successor work.
- **D6:** The owner's open-source condition is recorded; T3 waits for the license unit and uses a public alternative meanwhile. No separate approval requirement is reintroduced.
- **D9:** Only timing is decided: support decision after M3 readiness, Python corpus during M3; analyzer remains open.
- **D10:** MCP at M5 and LSP after residency are recorded without adding analysis authority.
- **D11:** AL2023 is a decided platform addition, routed to a DR-126 successor and a G13 lane.
- **D14:** Apache-2.0 is recorded as the chosen license, with the product unit still queued. The cited architecture commit eb439532 has an Apache License Version 2.0 LICENSE header.
- **D15:** Multi-repository workspaces are recorded as a required discovery shape with public/private representatives.
- **D16:** The approved record-hygiene batch remains separate from this plan.

REQUEST.md supplies the owner decisions as authoritative; this is not an audit of an unprovided owner conversation or a claim that successors/license/platform qualification have completed.

## Non-blocking observations

### C2-AQ-R2-N01 — PLAN.md:202,463,519 (§4.2; §9; D15)

D15 accurately records the decided multi-repository workspace requirement. Its implementation/harness design must still choose how separately checked-out repositories join a project and native program without bypassing existing custody boundaries. Native discovery excludes nested repositories, and explicit roots cannot cross those boundaries; a multi-checkout fixture cannot simply be flattened or scanned as one ordinary project and claim representative discovery.

**Follow-up.** As part of the already named discovery successor task, include security/native/identity owners, pin each checkout and cross-package edge, and specify lawful admission or typed external/unsupported handling before scoring the fixture. This is implementation design work for the accepted shape, not a request to reconsider D15.

- [native-evidence.md](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/native-evidence.md:818): Nested custody boundaries exclude units/files and reject explicit crossing roots.
- [identity-and-evidence.md](/Users/sb/code/opensip-ai/opensip_arch/docs/v2/contracts/product-v1/identity-and-evidence.md:1841): Snapshot capture and native discovery consume one admitted boundary inventory.

### C2-AQ-R2-N02 — PLAN.md:213-229,392,470-473

The remaining sampling and retry details are appropriate harness-design tasks, but should be written before measurement: advisory sample selection and denominator/weights, exclusion of calibration items and duplicate carried labels from evidence counts, fewer-than-50 explanation samples, and the treatment of a second CI performance batch.

**Follow-up.** Distinguish corpus population, adjudicated sample and independent evidence units. Retain both performance batches and preregister the retry decision rather than keeping the better result. These follow from the existing freeze-before-measuring and evidence-carrier work and do not require a new product decision.

### C2-AQ-R2-N03 — PLAN.md:352,385,413,468

The new authority citations are generally accurate. INC-1's IE:177-182 citation stops before the actual scope/fact/Coverage rows at IE:183-185; the intended binding is supported by the immediately following text. The revised dynamic-import explanation also needs its reference partition and dependency requirements to satisfy RC-2/§4.6, beyond proving that X is outside a possible target module.

**Follow-up.** Extend INC-1's citation through IE:195. Encode the explanation example as a truth fixture in D8's work. Keep D13 and the AL2023 successor as explicit blockers for completing the corresponding approved qualification scope; descriptive reporting must not be presented as that scope being qualified.

## Review boundary

No repository writes, product code, product tests, benchmarks, delegation or commits. No access to the runtime OpenSIP home or the private 413 UUID fixture. Only REVIEW.md and review.json were written under the requested /tmp directory.

This is a plan-method review. No proposed experiment, qualification gate or successor implementation was executed or accepted.

Read-only inputs:

- All 527 lines of the pinned r2 PLAN.md, the r2 REQUEST.md and the repository copy of CODEX2's r1 review
- The r1 snapshot hash and r2 subject hash/byte count
- Product-v1 identity/cache/replay, native Coverage/sufficiency/boundaries, qualification statistics and workflows
- New cited coordinator decision, source-map, report-schema, finding-surface, register, build-plan and preview-method passages
- The architecture eb439532 LICENSE header through read-only git show
