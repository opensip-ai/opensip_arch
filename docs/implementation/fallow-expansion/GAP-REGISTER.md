# Expansion gap register

Status: proposed. The linked comparison report is the source investigation; this register turns its findings into implementation obligations. No Fallow performance or precision advantage is inferred.

| ID | Desired product behavior | Effective design owners to inspect | Implementation intersections | Priority and proposed acceptance evidence |
|---|---|---|---|
| FX-CAP | A full, explicit whole-workspace request fits the chosen supported unit envelope without silent narrowing | Native §1.4/§10 cardinality; identity scope/analysis-spec/Plan; provider protocol limits; snapshot representation; qualification budgets | M3-B discovery; C2 contexts and C4 Plan; D2 codecs; F/G providers; H Coverage; J request/termination; K/Q harness; existing S-R/S-B | Decide first. Exact-bound/+1 tests, mixed TS/Rust and distinct contexts, cross-unit consumers, serialized size, decode/replay cost, refusal order, resource stress and historical replay |
| FX-FR | Recognize additional frameworks' entry-point and configuration conventions without executing configs | Native §8; recognition schema, registry, reference; host-owned mappings and committed recognition | B registry/discovery and C4 recognition Plan; F consumes committed recognition; H completeness | Design now. Positive, ambiguous, dynamic-config, nested-workspace, framework-version and unresolved-origin controls per recognizer |
| FX-COMP | Analyze Vue/Svelte/Astro embedded code and templates with original-source correspondence | Native grammar/capability matrix; syntax tree, symbols and Coverage; closure manifests; source/span identity | E syntax/grammar; F semantic adapter; B/C inventory; H admission; I policy and report spans; historical readers | Shared model first. Embedded-language mapping, component imports, template consumers, malformed/unsupported constructs, source-map errors and independently adjudicated false-deletion controls |
| FX-STYLE | Explain CSS/CSS-in-JS design-token drift, class references and duplicate declaration candidates | Native capabilities/facts/Coverage; syntax input selection; policy atoms; imports; output | E extraction; F JS/TS embedded styles; H; I; future reporting | Advisory initial scope. Exact normalization and metric definitions; dynamic classes/variables and preprocessing remain explicit uncertainty; original spans and false-positive fixtures |
| FX-METRIC | Explain cyclomatic/cognitive and template complexity through individual contributions | Native fact vocabulary, Coverage and capability matrix; evaluator/policy atoms; quality catalog | E/F extraction; H; I; K/Q corpus and qualification | Define metric version and contribution accounting. Separate syntax-complete measurement from semantic safety claims; fixtures for nesting, short-circuit operators, closures, JSX/templates and unsupported syntax |
| FX-API | Identify public-signature type coupling and private-type exposure | TS native exported API/type relations and completeness; graph queries; policy predicates | F semantic provider; H; I; baseline detector identity | Advisory first. Re-exports, generic signatures, declaration emit, external consumers and ambiguous resolution controls; define each proposition rather than generic impact |
| FX-SEC | Surface source/sink pattern candidates and import separately verified results | Native candidate relations; external-observation admission; source correspondence; policy and output claims | E/F candidates; H imports; I review; K/Q | Candidate-only initially. Explicit source/sink catalogue, unresolved-callee blind spots, negative lookalikes, verifier provenance and source match; never infer a proved vulnerability from a pattern |
| FX-EDITOR | LSP diagnostics/navigation/explanations over admitted saved snapshots, with safe quick-fix handoff | Workflow query/projection; source identity and stale results; authorized preview/apply; lifecycle and scheduling | Query/agent surface; reporting; J repair; O operational events | Specify now, implement after interfaces stabilize. Version/staleness, cancellation/starvation, root change and concurrent disk changes; quick fixes carry exact existing repair authority |
| FX-QUEUE | Rank advisory maintenance opportunities using explained complexity/history/coupling evidence | Existing candidate/history/runtime imports and output; ranking identity | Query/reporting consumers of FX-METRIC and admitted observations | Later. Deterministic ties, missing evidence, formula/version and factor explanations; ranking confers no repair permission or gating qualification |

## Scope decisions and constraints

1. Framework recognition and component parsing are distinct. A recognizer alone does not claim complete template consumers or enable destructive fixes.
2. Public graph trace/path/reach, baselines, audit, agent access, retained evidence and review/repair already exist in the design; they are not expansion gaps.
3. Unknown framework/dynamic syntax keeps incomplete Coverage until a selected recognizer/extractor proves its stated population. Broad framework counts are not a quality metric.
4. New capability selection can change default request size. FX-CAP must account for the actual selected matrix, including new analyzer families; its arithmetic cannot permanently assume eleven TS capabilities.
5. Unsaved buffers are a separate future authority/source-state decision, not implicitly selected by FX-EDITOR.
6. All new qualified and exploratory analyses use the accepted analysis-quality plan's distinction; neither an advisory label nor user adoption supplies qualification evidence.

## Sources

- `docs/v2/contracts/product-v1/native-evidence.md`, §1.4, §8 and the bounded-selection law at line 4276.
- `docs/implementation/m3/config-discovery-b/PROPOSAL-r4.md`, items 8 and 17 (registry and recognition ownership).
- `docs/implementation/m3/snapshot-plan-c/PROPOSAL-r7.md`, items 5/20, S-R and S-B (snapshot capacity and request admission).
- `docs/implementation/m3/analysis-quality/PLAN-r6.md`, rule specifications, adjudication and qualification.
- `docs/implementation/m3/syntax-e/hsr/hsr-1/README.md` and the selected product lock (historical-reader compatibility).
- [Source comparison](../../../reports/Fallow%20and%20OpenSIP%20current%20comparison.md).
