# Fallow-derived design borrow register

**Status:** Source and gap map. The accepted design constraints live in
[chapter 13](../v2/architecture/13-evidence-workflows-and-product-contracts.md)
under [D-370](COORDINATOR-DECISIONS.md#d-370--fallow-informed-product-design).
This register is not a second readiness checklist or an implementation claim.

**Reviewed upstream:**
[`fallow-rs/fallow@23bb9a7eceb6467336422db710ee0f5d92258c30`](https://github.com/fallow-rs/fallow/tree/23bb9a7eceb6467336422db710ee0f5d92258c30),
2026-09-05; workspace version 3.22.0 with unreleased changes.
**Method:** Codex read source, contracts, authoring guides, and the changelog;
Claude independently examined both projects and reviewed the concrete update.
The retained [review record](fallow-review/README.md) identifies the actual
reviewer, fixed subjects, disagreements, and final disposition.

No upstream code is copied and Fallow is not an OpenSIP dependency. This was not
a build, execution validation, performance comparison, or comprehensive audit
of Fallow. The previous review's commit is unavailable: an addition to the
user's list is not necessarily a feature added since that review. The changelog
dates semantic similar-code discovery to 3.19.0 (2026-08-26) and the branching
brief and explicit visualization availability to 3.22.0 (2026-09-01).

## Source catalogue

All links pin the same upstream revision rather than tracking `main`.

| Key | Upstream evidence |
|---|---|
| S1 | [README and command inventory](https://github.com/fallow-rs/fallow/blob/23bb9a7eceb6467336422db710ee0f5d92258c30/README.md) |
| S2 | [Onboarding decision catalogue](https://github.com/fallow-rs/fallow/blob/23bb9a7eceb6467336422db710ee0f5d92258c30/crates/cli/src/onboarding.rs) |
| S3 | [Semantic similar-code contract](https://github.com/fallow-rs/fallow/blob/23bb9a7eceb6467336422db710ee0f5d92258c30/docs/similar-code-analysis.md) |
| S4 | [Type-aware analysis contract](https://github.com/fallow-rs/fallow/blob/23bb9a7eceb6467336422db710ee0f5d92258c30/docs/type-aware-analysis.md) |
| S5 | [Runtime coverage output contract](https://github.com/fallow-rs/fallow/blob/23bb9a7eceb6467336422db710ee0f5d92258c30/crates/output/src/health_runtime_coverage.rs) |
| S6 | [Audit comparison ledger](https://github.com/fallow-rs/fallow/blob/23bb9a7eceb6467336422db710ee0f5d92258c30/crates/api/src/audit_keys.rs) |
| S7 | [Architecture invariants](https://github.com/fallow-rs/fallow/blob/23bb9a7eceb6467336422db710ee0f5d92258c30/docs/architecture-invariants.md) and [issue metadata](https://github.com/fallow-rs/fallow/blob/23bb9a7eceb6467336422db710ee0f5d92258c30/crates/types/src/issue_meta.rs) |
| S8 | [Analyzer authoring and fixture matrix](https://github.com/fallow-rs/fallow/blob/23bb9a7eceb6467336422db710ee0f5d92258c30/docs/analyzer-authoring.md) |
| S9 | [Public configuration and smoke corpus](https://github.com/fallow-rs/fallow/blob/23bb9a7eceb6467336422db710ee0f5d92258c30/docs/public-config-corpus.md) |
| S10 | [Weakening heuristics](https://github.com/fallow-rs/fallow/blob/23bb9a7eceb6467336422db710ee0f5d92258c30/crates/cli/src/audit_weakening.rs) and [branching observations](https://github.com/fallow-rs/fallow/blob/23bb9a7eceb6467336422db710ee0f5d92258c30/crates/output/src/audit_branching.rs) |
| S11 | [Decision extraction and anchoring](https://github.com/fallow-rs/fallow/blob/23bb9a7eceb6467336422db710ee0f5d92258c30/crates/api/src/decision_surface.rs) |
| S12 | [Rule-pack model](https://github.com/fallow-rs/fallow/blob/23bb9a7eceb6467336422db710ee0f5d92258c30/crates/config/src/rule_pack.rs) and [pack-test operation](https://github.com/fallow-rs/fallow/blob/23bb9a7eceb6467336422db710ee0f5d92258c30/crates/cli/src/rule_pack/test.rs) |
| S13 | [Changelog](https://github.com/fallow-rs/fallow/blob/23bb9a7eceb6467336422db710ee0f5d92258c30/CHANGELOG.md) |

## Original seven ideas

`PRESERVE` means existing architecture already covers the principle. `ADAPT`
identifies a clarification or addition adopted in chapter 13. `FUTURE` means
its design constraints are settled now but implementation remains outside the
preview. None of these labels applies a V1 recipe or changes a register grade.

| ID | Idea and finding | Disposition and concrete design consequence | Source / design home |
|---|---|---|---|
| FW-01 | Zero-config and recommendation | ADAPT. Separate technical evidence, product defaults, and project policy; analysis-affecting discovery uses ordinary input provenance. A proposal must pass the strict resolver and cannot write intent or grant effects. FUTURE recommendation surface; preview commands unchanged. | S1/S2; [chapter 13 §2](../v2/architecture/13-evidence-workflows-and-product-contracts.md#2-discovery-and-zero-config-behavior); configuration chapter 03 |
| FW-02 | More sophisticated clones | PRESERVE existing body normalization and predicate-specific facts. ADAPT the suggested progression: structural/near-clone detection and model-based similarity are different claims. FUTURE similarity is advisory Map work; algorithm choice and tuning remain later. | S1/S3; [§4](../v2/architecture/13-evidence-workflows-and-product-contracts.md#4-candidate-inspection-and-review-handoffs); fact-plane body identity |
| FW-03 | Rich native TypeScript/JavaScript analysis | PRESERVE language-native providers and C-1. FUTURE additional predicates consume native facts and explicit Coverage. Adapt useful framework abstention cases into later native corpora; never import a provider's verdict authority or syntactic fallback. | S4; [§3](../v2/architecture/13-evidence-workflows-and-product-contracts.md#3-evidence-sufficiency-and-visible-omissions); DR-118/133 |
| FW-04 | Static + test + runtime + history evidence | ADAPT binding dimensions and observation limits now. FUTURE admitted relation/artifact families and lifecycle contracts. Observable-but-unhit differs from unobservable; no global combined-confidence score or implicit collection. | S5; [§7](../v2/architecture/13-evidence-workflows-and-product-contracts.md#7-runtime-test-and-history-evidence) |
| FW-05 | Baseline, delta gate, debt reduction | PRESERVE stronger versioned fingerprint/detector-pivot design. ADAPT explicit policy/scope/evidence attribution and fact-scope versus gate-scope distinction. FUTURE baseline operations remain gated on their owning contracts. | S6; [§6](../v2/architecture/13-evidence-workflows-and-product-contracts.md#6-delta-attribution-and-policy-changes); evidence chapter 06 |
| FW-06 | Determinism, typed output, stable fingerprints | PRESERVE. Fallow confirms the product value; it supplies no replacement identity recipe. Same declared semantic inputs produce the same assessment; preview identifiers remain expressly unstable. | S1/S7; [§8](../v2/architecture/13-evidence-workflows-and-product-contracts.md#8-common-contracts-and-evidence-reuse); domain model 02 |
| FW-07 | One coherent invocation with steps | PRESERVE host-owned data-only workflows and shared evidence. FUTURE named workflows cannot own private exits, stores, hooks, or policy; required-step failures remain visible. | S1/S7; [§9](../v2/architecture/13-evidence-workflows-and-product-contracts.md#9-coherent-workflows-and-bounded-review); surfaces chapter 08 |

## Eight further observations

| ID | Idea and actual gap | Disposition and concrete design consequence | Source / design home |
|---|---|---|---|
| FW-08 | Visible completeness and omissions | PRESERVE Coverage semantics; ADAPT explanation requirements for future assessments. Completed-zero differs from unrun, unsupported, partial, or unavailable. Existing preview Coverage/D9 remains exact; no new output field or qualification fixture added by this review. | S3/S5/S13; [§3](../v2/architecture/13-evidence-workflows-and-product-contracts.md#3-evidence-sufficiency-and-visible-omissions) |
| FW-09 | Discovery → inspection → judgment | ADAPT explicit advisory handoff and review-membership constraints around existing snapshot/query architecture. FUTURE separate review artifacts; stale or unknown Control references refuse; correlation is not verification of prose. | S3/S11; [§4](../v2/architecture/13-evidence-workflows-and-product-contracts.md#4-candidate-inspection-and-review-handoffs) |
| FW-10 | Evidence requirements specific to repair | ADAPT reporting/apply distinction, mutation-boundary source guard, current authorization, and separate post-edit verification. FUTURE repair requires exact schemas and interruption/partial-write semantics before support. | S4; [§5](../v2/architecture/13-evidence-workflows-and-product-contracts.md#5-remediation-requires-its-own-evidence) |
| FW-11 | Weakened safeguards and metric redistribution | ADAPT policy-aware attribution and metric honesty. FUTURE advisory observations for tests/CI and decomposition; raw token counts and branching redistribution do not establish regressions or behavioral simplification. | S10; [§6](../v2/architecture/13-evidence-workflows-and-product-contracts.md#6-delta-attribution-and-policy-changes) |
| FW-12 | Bounded decision-focused review | ADAPT Control-reference validation and explicit limits. FUTURE advisory brief composes evidence on boundaries, contracts, dependencies and affected consumers. Ranking and cap size are not preview architecture constants. | S11; [§9](../v2/architecture/13-evidence-workflows-and-product-contracts.md#9-coherent-workflows-and-bounded-review) |
| FW-13 | Common declaration registry and generated contracts | ADAPT an implementation discipline for existing host-owned common behavior: generate or drift-check factual public inventories against owning contracts and real adapters. PRESERVE one typed assessment with multiple projections and independently versioned releases. | S7/S8; [§8](../v2/architecture/13-evidence-workflows-and-product-contracts.md#8-common-contracts-and-evidence-reuse) |
| FW-14 | Learn from real-world configuration workarounds | ADAPT as a qualification method: pinned project shapes, confirmed reproductions, explicit manual-correction counts and privacy boundaries. Not a telemetry feature, architecture subsystem, or change to the accepted G13 corpus. | S9; [§2](../v2/architecture/13-evidence-workflows-and-product-contracts.md#2-discovery-and-zero-config-behavior) |
| FW-15 | Declarative policy authoring and testing | ADAPT future authoring requirements around existing data-only packs: strict schemas, explanations, positive/negative examples, effective-policy preview. A direct-call ban is not a complete transitive effect proof. Preview remains bundled-pack-only. | S8/S12; [§10](../v2/architecture/13-evidence-workflows-and-product-contracts.md#10-declarative-policy-authoring) |

## Explicit non-borrows

- No syntax substitution for missing required semantic evidence; no
  unclassifiable comparison relabeled inherited to keep a gate green.
- No global ordering of syntax, semantic, runtime, or model confidence; no
  similarity score promoted to behavioral equivalence or repair safety.
- No model call or externally authored verdict in the Control product path.
- No producer- or adapter-owned policy outcome, finding identity, public exit,
  or authoritative persistence.
- No Fallow fingerprint/hash algorithm substituted for OpenSIP's versioned
  host-owned identity contracts.
- No implicit model/tool download, repository configuration execution, test
  run, permission grant, or production monitoring in a default analysis.
- No cloud subscription, license watermark, telemetry system, or external
  runtime dependency selected by this exercise.
- No copied command roster, arbitrary review cap, confidence threshold,
  weakening-token list, framework-count target, or effect taxonomy.
- No algorithm or performance claim adopted from README benchmarks without
  OpenSIP-specific measurement and a sufficient correctness corpus.

## Implementation and maintenance

The selected implementation remains the D-369 preview. Implementers should read
chapter 13 before choosing private abstractions, especially the ownership and
no-hidden-input boundaries. This does not require speculative public APIs or
empty implementations of future capabilities.

When a future capability is proposed for support, use chapter 13's ownership map
to revisit the existing central register rows and accepted contracts. Supply
concrete schemas, source/state binding, negative cases, resource measurements,
and required scope successors then; this source register cannot waive them.
Do not mark a row implemented on the basis of prose or peer agreement.

Update the upstream revision explicitly on another review and retain what
changed. If source code is later copied, conduct the separate license/notice
review required by that copying; this decision adopts ideas only.
