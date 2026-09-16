# Evidence workflows and product contracts

**Standing:** Acceptance, exact reviewed bytes, and reversibility are recorded
in [D-370](../../coop/COORDINATOR-DECISIONS.md#d-370--fallow-informed-product-design).
**Scope:** Design constraints settled before implementation; the D-369 preview
remains the selected implementation scope. This chapter adds no executable
capability, public command, wire field, identity recipe, or release qualification.

The [Fallow borrow register](../../coop/FALLOW-BORROW-REGISTER.md) maps the
original seven ideas and eight further observations to their sources and these
decisions. Fallow is design evidence, not a dependency or an authority over
OpenSIP semantics.

## 1. Scope and ownership

OpenSIP's product remains an evidence compiler with one host. Providers supply
declared facts and Coverage; rules declare predicates and evidence requirements;
the pure evaluator computes policy results; the host owns admission, identity,
configuration, supervision, and projections. Model-assisted exploration and
external review remain advisory under the [Map/Control boundary](../../MAP-VS-CONTROL.md).
No model call or external judgment becomes a required input to Control.

These commitments refine that architecture in two ways:

- **Preview implementation guidance** explains existing obligations: explicit
  insufficiency, consistent human/JSON meaning, deterministic declared inputs,
  host-owned common behavior, and refusal of unsupported operations. It changes
  no preview schema, threshold, supported platform, required gate, or row grade.
- **Future capability constraints** settle ownership, evidence handoffs, and
  failure semantics now. Before a future capability enters a supported slice,
  its owning register rows must accept the concrete schemas, identity and
  lifecycle joins, fixtures, resource limits, and product scope it needs.

The [reference handoff](../../coop/completion/reference-architecture.v2.md)
continues to own the exact preview: `analyze`, `doctor`, help/version, one
TypeScript provider, and the bundled import-cycle rule. This chapter does not
enable a baseline, repair, review, discovery command, additional rule pack,
runtime importer, semantic-similarity model, durable result cache, or Map.
Existing admission must continue to refuse excluded forms. A future feature is
not implemented by reserving an undocumented flag or accepting an open payload.

## 2. Discovery and zero-config behavior

For each supported conventional project shape, the product goal is useful
analysis without requiring a user-authored OpenSIP configuration. An installed,
compatible analysis closure is a prerequisite; zero-config is not permission to
download tools, execute repository configuration, or grant effects implicitly.

Discovery distinguishes three kinds of information:

| Information | Owner and treatment |
|---|---|
| Observed technical facts: language, manifest, workspace layout, recognized convention | Discovery producer reports the source and uncertainty; the host validates and resolves applicability. |
| Product defaults: supported ignore conventions and default profile selection | Host-owned, versioned, disclosed, and overridable through existing configuration precedence. |
| Project decisions: gate strictness, allowed dependencies, waivers, boundary intent | Explicit project policy; a detector or recommender cannot adopt these on the project's behalf. |

Any discovered value that affects analysis must enter the ordinary declared
input/resolution path with provenance. There is no seventh configuration layer,
provider-private override, or hidden environment input. An explicit supported
override wins according to the existing resolver; ambiguity is disclosed rather
than silently selecting a broader or weaker interpretation. Ignored and
unsupported regions are scope information, never evidence that those regions
are clean.

A future recommendation surface returns detected evidence, proposed settings,
default rationale, unresolved choices, and the effect of each choice. Reading a
recommendation does not write configuration. Applying it is a separate host
operation with the normal write authority. Proposed settings must be accepted
by the actual strict configuration resolver, not merely validate against a
JSON Schema; schema references must resolve from the supported offline closure.
The preview's read-only `doctor`
does not become a source analyzer or execute configuration to make detection
more convenient.

Qualification for newly supported project conventions should use pinned real
repository shapes and nearby negative cases, including generated sources,
monorepo consumers, and convention-loaded entry points. Record how many manual
corrections are needed for a useful result and which gaps remain. Repeated
workarounds are investigation inputs, not automatically confirmed bugs or
permission to collect private repositories. Exact corpus and numeric targets
belong to the capability's later qualification decision; no target is invented
here.

## 3. Evidence sufficiency and visible omissions

Preserve C-1: evidence is sufficient for a particular predicate over a declared
scope. Syntax, resolved symbols, tests, runtime observations, and repository
history do not form one global strength or confidence ranking. Independent
evidence may support different claims about the same subject without being
collapsed into a single score.

Every supported assessment projection must preserve the distinction between:

- completed analysis with no matches in the admitted scope;
- unsupported, disabled, or inapplicable analysis; and
- attempted analysis with missing, failed, truncated, or insufficient evidence.

These are semantic distinctions, not new wire-enum spellings. Existing typed
Coverage and diagnostics carry preview meaning. Future schemas must retain the
selected scope, applicable requirements, omissions and reasons, and truncation
or completion information needed to interpret the result. A count is meaningful
only together with that scope and sufficiency. Cancelling or exhausting a
budget cannot produce a clean result from a truncated subject set.

Optional evidence can be absent while independently sufficient predicates still
complete. A predicate whose required evidence is missing remains indeterminate;
reporting other completed predicates cannot make it pass. A syntactic fact may
satisfy a syntactic predicate, but cannot substitute for required semantic
resolution. A summary or renderer must not erase this distinction.

## 4. Candidate, inspection, and review handoffs

Future advisory discovery separates observations from judgments. A candidate
means that investigation is warranted; it is neither a proven finding nor a
policy outcome. Deterministic clone detection describes exact or normalized
structure under a named algorithm. Model-based similarity remains a separate
Map capability: a score is model-specific and does not prove behavioral
equivalence or refactor safety. This separation replaces the proposed single
progression from exact clones to supposedly stronger semantic confidence.

An inspection request selects an exact candidate from an explicit discovery
result. Its handoff binds the project, source subjects with their content
identity (the sealed Snapshot or per-subject content digests), scope,
producer/schema versions, relevant parameters, and completion information. Inspection either
uses retained source evidence or validates the currently opened source against
that handoff. Stale, missing, ambiguous, or outside-scope subjects are reported
explicitly. It cannot silently rerun retrieval and substitute a new candidate.

External reviews remain separate artifacts referencing the reviewed result and
subject binding. A later review-join operation validates supported versions,
membership, duplicate judgments, and source correspondence. Unreviewed
candidates remain visible; requiring every candidate to be reviewed is an
explicit workflow condition. Matching an identifier validates correlation, not
the truth of an agent's prose. Missing or contradictory evidence permits
abstention.

An advisory item claiming to cite Control must reference an actual host-emitted
item in its named view; unknown references are rejected. Map may also produce
its own labeled observations or hypotheses under its separate contract. Those
do not become Control citations merely because they mention the same file.

Keep three questions independent: whether the candidate merits investigation,
whether the compared behavior is equivalent, and whether a proposed refactor is
safe in context. A favorable similarity score answers none of them by itself.
No external verdict edits the original observations or directly changes a
Control result, waiver, baseline, or exit. Any supported future human policy
action must use its own host-owned policy path.

These are required binding dimensions, not new durable identifier recipes.
Candidate and review identities, retained source policy, and review storage must
be designed under the owning future contracts. Preview correlation identifiers
must not be advertised as stable finding identities or sealed Runs.

## 5. Remediation requires its own evidence

A future repair recipe declares the action, exact target binding, evidence
requirements, permitted edit scope, and verification obligations. Reporting a
candidate does not make its removal safe. "No references in the checked scope"
is distinct from "no possible consumers"; unresolved owning projects, dynamic
dispatch, external consumers, or incomplete runtime observation remain explicit
limitations relevant to the particular repair.

The repair lifecycle has separate preview and apply operations. A preview
describes edits and unmet preconditions without changing source. Apply checks
current source identity, current authorization, and evidence sufficiency at the
mutation boundary. A source change or evidence mismatch invalidates the plan;
the host refuses it and requires a new preview instead of relocating an edit
heuristically. A component cannot mutate source independently of the host.

Verification runs against the resulting source through ordinary analysis and
any declared, separately authorized tests. An applied edit and a verified
outcome are distinct results. Failed verification cannot be presented as a
successful repair. Multi-file atomicity, interruption, partial edits, rollback
ownership, and exact verification outcomes must be closed in the repair
contract before apply is supported. This chapter does not select a filesystem
transaction algorithm or authorize a test runner in the preview.

## 6. Delta attribution and policy changes

Preserve the existing versioned fingerprint and detector-pivot architecture.
A finding difference alone cannot establish a code regression when the
detector, rule selection, parameters, scope, required evidence, or policy also
changed. Baseline adoption remains an explicit host-owned policy operation.

A future comparison identifies both source snapshots and both analysis/policy
contexts. It separates code-introduced or code-fixed results from detector
changes, policy changes, scope changes, waivers, and changes in evidence
availability. Use controlled comparisons under compatible semantics to make an
attribution; otherwise report the affected comparison as indeterminate. Do not
rename an unclassifiable result "inherited" or count a vanished finding as fixed
merely because its rule was disabled or its file ignored.

The report/gate scope is distinct from the fact derivation scope. A PR may gate
only introduced findings while analysis still requires unchanged consumers,
entry points, dependencies, or test relationships. Restricting output to changed
lines does not establish a complete graph over just those lines. Supplied diff
scope and comparison base must agree or be reported incompatible; clone-group
reshaping alone does not prove new duplicated code was written.

Policy deltas should use schema-aware semantics: raising a maximum allowed
complexity weakens it, while lowering a minimum coverage weakens that policy.
String matching or the direction of a number alone is not an enforcement rule.
The host projects tracked policy changes; new/removed/skipped tests and removed
CI steps may also be advisory review observations with stated detection limits.

Metrics are reported with their population and unit. A smaller worst function,
more functions, and unchanged branching may describe decomposition, which can
improve readability without removing decisions. Do not claim behavioral
simplification from that metric alone. A suppression changes handling of a
finding, not the measured source property. Future waiver/suppression inventory
should expose rationale, scope, and staleness using the owning policy contract.

## 7. Runtime, test, and history evidence

Future evidence import is explicit, bounded, and local-first. Collection or
network retrieval is a separate capability and authority decision; analyzing a
repository does not implicitly execute tests or start production monitoring.

Runtime evidence must state source/build correspondence, capture provenance,
observation window, observed population, mapping gaps, and which subjects were
observable. Distinguish observed execution, observable-but-unhit code, and code
the capture could not observe. An unmatched build or missing source map cannot
be treated as an unhit function. A test coverage artifact does not establish
production traffic, and an absence of hits during one window does not prove
code is safe to delete.

Tests and history similarly retain source correspondence, collection scope,
tool/version provenance where relevant, and limitations. An impact-selected
test list is a bounded recommendation unless the evidence establishes the
claimed selection completeness. History or runtime importance may guide
advisory review priority; any future deterministic policy over these inputs
requires a separately admitted artifact and a declared predicate. Evidence
conflicts and gaps remain visible rather than being averaged into confidence.

Runtime execution coverage is distinct from OpenSIP Coverage, which describes
analysis sufficiency. Freshness, retention, artifact admission, data privacy,
and exact source-map/build binding require concrete future contracts. The
preview's SC-CACHE/SC-OPS/SC-TRUST state selection is unchanged; no runtime or
review evidence store is smuggled into an operational cache.

## 8. Common contracts and evidence reuse

Implement common behavior from one host-owned declaration registry or generated
contract source, with drift checks against the actual supported operations and
schemas. Public inventories should describe rules/capabilities, accepted input
and output schemas, applicability, supported projections, stable diagnostic
codes, and action availability from their owning contracts. The exact signed
component schema remains its existing owner; this registry neither adds an
unsigned capability claim nor creates a plugin ABI.

Rule/contribution updates cannot silently select project policy, introduce a
private configuration precedence, or change gate behavior through recommended
defaults. Host admission validates declarations even if a component uses the
SDK. Independent release compatibility remains per surface; generated artifacts
must not force all components onto one release version.

Generate or drift-check factual help/schema/adapter inventories from the same
source. Keep audience-specific explanation separate, but flag it for review when
its underlying contract changes. Tests must cover supported human/JSON
semantics in the preview and each additional adapter when advertised; a core
test alone does not demonstrate that an adapter preserves the result.

Report formatting consumes an explicit typed assessment; it does not crawl the
working tree, run an analyzer, read physical tables, or recompute findings.
Expensive facts can be shared within a valid analysis operation. Future saved
reports and inspection surfaces use the common typed query boundary and disclose
unavailable retained evidence instead of reconstructing it invisibly. Source
enrichment is an explicit inspection operation, not a renderer side effect.
Cross-run result reuse remains excluded from the preview. Exact acceleration
and semantic production retain the distinction in the Gortex borrow register.

## 9. Coherent workflows and bounded review

Preserve one host invocation containing typed steps. A named workflow is data
selecting existing host-owned operations, not a peer tool with private policy,
persistence, command hooks, or exits. Step requirements and dependencies must be
explicit; aggregation cannot hide a failed or indeterminate required step.
The existing Plan/workflow contracts own exact identity, cancellation, outcome,
and future parent/child links. No extra Invocation or Run identity is defined
here, and the preview is still the single supported analysis path.

A future review brief and target inspection compose existing evidence. The
brief may prioritize boundary crossings, public contract changes, dependency
changes, consumers outside the diff, and test/runtime/history context when
available. Deterministic selection records its version, inputs, reasons, scope,
limits, and omissions. A bounded top list is a view over findings, never a
policy truncation: omitted findings still participate in their ordinary gate.
Any agent framing remains separately identified and advisory. User research and
measurements should choose the list size; Fallow's three-to-five limit is not
adopted as an OpenSIP constant.

## 10. Declarative policy authoring

Future policy authoring should supply schema guidance, rule explanations,
positive and negative examples, and an explicit preview/test operation before
enforcement. Preview reports the effective policy and proposed change; it does
not rewrite tracked intent or promote a rule's severity implicitly. Test
overrides must be disclosed and scoped to that invocation.

Packs remain data-only contributions evaluated under host authority. A rule
such as "this layer does not perform network access" must distinguish a ban on
known direct calls from a transitive absence-of-effects claim. The latter needs
appropriate semantic relations and complete scope; an unknown callee is not
evidence of purity. No effect catalogue from another analyzer is accepted as
universal effect semantics.

The preview accepts only its bundled cycle pack. External packs, additional
rules, pack-test commands, and admission of user-authored policies retain their
existing scope re-entry requirements.

## 11. Integration and future acceptance

The architectural decisions in sections 2–10 are settled here; exact public
schemas and algorithms for excluded capabilities are not represented as
implementation-ready. Their scope admission must satisfy these constraints and
the owning rows in the [central readiness register](08-decision-and-readiness-register.md):

| Design area | Existing ownership to revisit when scope enters |
|---|---|
| Discovery, defaults, common declaration registry | DR-103, DR-117, DR-120, DR-123, DR-125; language applicability DR-118 |
| Sufficiency, native facts, richer evidence | DR-004, DR-005, DR-118, DR-133; runtime effects/security DR-105/117 |
| Candidates, review, runtime retention, repair | DR-002, DR-006–009, DR-105, DR-117; Map boundary and state ownership DR-109/124 |
| Baseline and policy attribution | DR-002, DR-006–008, DR-011, DR-111; policy provenance DR-103 |
| Workflow, projections, rule-authoring surfaces | DR-117, DR-122/123/125, DR-131; future pack admission under the product boundary |

This is an ownership map, not another readiness checklist. No row is closed or
regraded here. File 08 and its D-369 after-image remain unchanged because the
preview's accepted behavior and gates are unchanged. The decision register and
current reading path link this supplement now, before implementation begins.

Future qualification must exercise the actual capability input path, including
unknown/partial evidence, source changes between review and apply, invalid
review membership, policy-only changes, incompatible comparisons, and bounded
output. Those are acceptance obligations for the future capability, not claims
that newly authored product fixtures or passing runtime tests exist today.
