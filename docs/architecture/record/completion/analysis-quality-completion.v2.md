# Preview analysis, quality and independent-release completion

Author: Codex. Status: PROPOSED. Scope: DR-118, DR-122, DR-127, DR-131,
DR-133; capability-registry join to DR-125 and required-now G13 addition.

### Superseded owner rulings

Under D-367 delegation, this successor explicitly replaces these adopted
owner sentences from COORDINATOR-DECISIONS.md:

- D-314 **Adopted text item 24, G3-HOSTILE** and D-315 **Adopted text
  item 4, G3-HOSTILE**: “leave the seven live v3 within-class universal sets
  including CC-6 named-open, and supply no per-class totals.” Section 7's
  finite generated coverage definition decides that reservation; D-300's
  already-authored citation-witness floor remains the minimum baseline.
- D-314 **Adopted text item 25, G3-SARIF-RUNID**: “Keep
  FC-OUTFAIL.committed-run-preserved parked and do not author an opaque literal
  RunId; trigger it only after the governing RunId recipe is bound.” Section 6
  permits an opaque object for non-mutation only. The RunId recipe stays
  unbound; a valid sealed-Run golden still rides re-entry under the separately
  reviewed scope-rides unit. The reference adapter establishes only unchanged
  pre-image/post-image, not the product D9/operability failure path.
- D-315 **Adopted text item 5, G21-SCHEMA**, superseding D-314 item 28:
  “Choose neither route and author no bytes here.” Section 5 chooses the
  envelope/schema route and allows authoring. Truncated bodies and invalid
  UTF-8 remain unconditionally RF-2 and are never treated as schema-blocked.

Reversibility: a reviewed successor may restore any named reservation; doing
so removes the dependent application/acceptance evidence and reopens the
affected row before the withdrawn choice can be relied on. Historical entries
remain unchanged. The scope-rides unit is an explicit application prerequisite,
not inferred authority from a label or a reference to future implementation.

## 1. Applied architecture and preserved boundaries

On application, incorporate preview-analyze-contract.v2 (D-138), provider-only-
output-contract.v3 (D-136), preview-product-boundary-successor.v10 (D-295/D-363),
language-quality-matrix-contract.v13 (D-113), sarif-projection-contract.v15
(D-115), and anti-lockstep-contract.v7 (D-111). Source selectors and digests are
listed in the application manifest. This contract updates the DR-131 product
boundary citation from the historical v5 to v10 and explicitly applies the
provider-only output law. It does not import historical candidate disclaimers
as current authority or revive the old generic component 'may return findings'
permission. Existing D9 and TypeScript wire semantics remain owned by V1.

D-367 delegates the Class A openings for DR-131 and DR-133. The integrated
application act must include fresh independent application-grade and per-row
SATISFIED-GRADE findings, the gate-2 interpretation, and the exact register
changes under the reviewed workflow. This document alone performs none of them.

## 2. What the preview evaluates

The single first-party host-owned pack is `opensip.preview.typescript.pack`
version 1. It contains one declarative rule, `module-import-cycle`: over
host-admitted `imports` facts at `resolved-target`, find directed strongly
connected components with at least two project files, or a self-edge. Emit one
transient finding per cyclic component. Sort member paths by UTF-8 bytes;
present paths and spans from admitted facts only. Multiple import edges do not
multiply findings. Ignore external library vertices only after the host's
explicit project-domain partition; they cannot be silently dropped from a
domain declared as project. Dynamic imports without a statically resolved
target yield unknown Coverage for the applicable requirement, not a guessed
edge or a falsely passing graph.

The pure core evaluates the rule and returns its `policyOutcome` in the
existing CoreCompletion. The pack's fail threshold is at least one cyclic
component; zero cyclic components passes only with sufficient Coverage. A
missing required rung or incomplete Coverage produces the existing typed
indeterminate result; the host never turns it into a policy pass. These are
product-chosen thresholds over a named rule and corpus, not observed quality
results. The host projects the existing D9 result and exit discipline; this
pack cannot mint a new code or reinterpret policyOutcome as HostTermination.

No user packs, third-party packs, imperative predicates, execution hooks or
provider-authored findings are admitted. The TypeScript provider supplies facts
and Coverage, never rule evaluation. The pack is part of the useful-install
closure and its identity belongs in the conceptual Plan membership already
specified by DR-131; this does not produce a parked PlanId digest recipe.

The first implementation may use a pure graph SCC algorithm, but the accepted
property is the cyclic-component set and deterministic projection. An algorithm
change with identical accepted behavior is an implementation substitution.

## 3. Capability registry and matrix (DR-125 → DR-118)

Freeze these host-owned capability IDs and their relation/rung bindings:

| Capability ID | Existing fact relation | Required rung |
|---|---|---|
| typescript.imports | imports | resolved-target |
| typescript.references | references | resolved-binding |
| typescript.calls | calls | resolved-callee |
| typescript.types | types | checked |
| typescript.reachability | reachability | from-resolved-calls |

The concrete manifest role remains the inherited `analyzer`; its selected
opaque control tuple is `{role: "analyzer", roleSubprotocol: "typescript",
subprotocolVersion: 1}`. Each capability declaration carries that same
roleSubprotocol/version plus a closed declarationData object `{relation, rung}`
matching this table. This names the initial host vocabulary; it does not add a
second analyzer role. Matrix rows record role `analyzer` and language
`typescript` separately. These are manifest declaration IDs over existing
semantics, not new provider wire relation tokens. The provider SDK declares them as data; the host validates
the list and the fixed dependency of reachability on resolved calls. An unknown
capability or a changed rung is refused, never treated as an extension. The
preview TypeScript release advertises all five. Host-owned finding and output
checks are mandatory integration dimensions, not provider-granted authority.

The matrix is five capabilities × four D-002 platforms, with one separately
identified host integration row per platform. Each row names its corpus file
set and digests, behavior target, measurement method, known limitation,
performance runner/workload and thresholds. Parse fidelity is checked by the
syntax and typed semantic examples for each applicable capability; graph,
finding and output checks cover the illustrative floor from the earlier
contract. No matrix cell disappears when metadata is missing or a test fails.

Full-product prototype baseline standing is **NOT MEASURED HERE**. The local
prototype checkout is available and its pinned Program service is exercised;
that does not establish equivalent full-product measurements. Under D-007's explicit alternative,
the delegated product authorities approve the retained language-native corpus
as the preview behavior baseline. The pinned prototype remains historical
reference; any later measured regression against it requires a recorded
disposition and cannot be silently accepted.

### Numeric acceptance thresholds and method

- Golden behavior: exact set equality for expected facts, Coverage and graph
  results; 100% expected members, zero extra members, zero duplicate members.
  Finite-corpus precision and recall must both equal 1.0; empty expected sets
  require zero actual members rather than division by zero.
- Authority/failure cases: 100% refusal/discard/preservation expectations.
  Zero provider findings or provider-selected verdicts are admitted.
- All advertised matrix cells must pass. No percentage permits silently
  dropping a capability or platform. Unsupported input is explicitly unknown
  with the existing deficiency, not a success or a missing result.
- Performance workload: the retained deterministic 1,000-module TypeScript
  import/call/type graph, generated from a pinned seed, plus the small correctness
  corpus. Run on a dedicated four-vCPU/eight-GiB worker for each target, using
  the signed full TypeScript closure and pinned compiler/runtime, no network,
  five warmups and 30 measured independent cold and warm invocations. Record
  CPU model, OS/build, filesystem, kernel, executable digests and concurrency 1.
- Whole analyze latency: cold p95 ≤ 10,000 ms, warm p95 ≤ 5,000 ms; peak RSS of
  the whole host-plus-worker process tree ≤ 1,073,741,824 bytes. Use nearest-rank
  p95 (rank 29 of 30), monotonic elapsed time, and high-water resident sum over
  the supervised process tree. A runner unable to measure descendants is
  NON-PASS. These budgets are design targets, not claimed measurements.
- No measured performance baseline exists at adoption. The first qualified
  release establishes it. Subsequent same-corpus p95 regression >10% or RSS
  regression >10% is NON-PASS even if within the absolute ceiling, unless a
  separately reviewed product threshold successor explicitly changes the rule.
  Both the fixed ceiling and regression checks apply.

This names the workload, runner and denominators the old THRESHOLDS-NOW
rejection lacked. Actual production measurements remain qualification work.

## 4. G13 becomes required-now

The application act is an explicit D-002/D-086 successor adding
`harness.DR-G13.typescript-quality.preview` to required-now, owned by Language
quality + product + release engineering. The affected-row set stays 23; the
required gate count becomes 29. G13 executes all matrix cells above and emits
one strict result manifest with subject digests, corpus digests, platform,
capability, expected/actual counts, differences, elapsed samples, RSS samples,
runner identity and PASS/FAIL/NON-PASS. Missing samples or matrix cells fail
qualification. The harness specification is authored here; a name alone is not
evidence of execution. G14 still owns bundled runtime closure and G15 adapter
conformance; neither substitutes for G13 quality.

## 5. Provider, preview and control failure evidence

Retain every NT-1..NT-7 provider and NT-1..NT-8 analyze requirement from the
incorporated contracts. Construct fixtures against the pinned TypeScript wire
where they are wire cases, and strict host admission records where they are
host-domain cases. NT-6 must use an actual unknown frame or extra closed-payload
member attempting host termination; a descriptive citation is insufficient.

For G21 OQ-G21-4 choose the envelope-level route: a complete `ping` envelope
whose outer seq is a float or negative integer, whose controlMajor exceeds
uint53, or whose outer object has a duplicate or unknown member, is RF-2 before per-type body
interpretation. The separate seq-overflow case remains RF-7 under control v2
transportAndFraming.framing.sequencing. No otherwise-valid-body requirement is added. Truncated input
and invalid UTF-8 remain unconditional RF-2. Freeze an ordinary conforming
ping body as a positive control and retain exact framed bytes for all seven
mutants. This is an explicit ruling on the previously reserved route.

The common protocol's schema completion must preserve all sixteen existing
message types, strict unknown-field refusal, the opaque provider channel,
one select per child and the teardown precedence law. Per-type bodies are
defined and reviewed in the control-schema artifact; no arbitrary object
extension point is permitted. Failure detection cannot depend on interpreting
provider fate or semantic contents on fd3/fd4.

## 6. SARIF preservation under parked identities (DR-122)

The preview does not advertise SARIF, manufacture a RunId or label a terminal
result as a sealed Run. The remaining committed-run-preserved design case uses
a PRE-EXISTING opaque retained byte string outside the preview write set, with
a pre-image path and SHA-256. Trigger an output serialization failure in the
abstract host output adapter; the post-image bytes and digest must equal the
pre-image, and no candidate result is committed. The opaque object has no
claimed valid RunId, identity recipe or semantic interpretation.

This is an explicit D-367 ruling: test non-mutation without inventing the parked
identity. It authorizes this design fixture, not a sealed-run producer or a new
typed exit. Actual serialized required-output failure follows the existing
D9/operability law. The no-committed-run sibling remains separately tested.
If a later authoritative product is admitted, its own owner must test a VALID
sealed Run under the then-applied recipes; this preview fixture cannot qualify
that future claim. Record that limitation at G17/DR-012 rather than silently
claiming authoritative preservation from an opaque model.

## 7. Independent release and finite hostile coverage (DR-127)

Preserve AL-1/AL-2/AL-5 requirements and assign their preview selection,
compatibility and independent release execution to G16/G15/G18 with exact
cross-references. Retain a positive component-only release on a fixed core and
a core-only compatible release with unchanged component versions; an aggregate
bundle is optional and never the only release path. A version-equality selector
fails these cases. Roleless packaging/build components in the test corpus do
not expand the product's supported analyzer roles.

AL-3 core release byte rollback rides DR-110 only upon acceptance of the
separately reviewed `scope-rides-completion.v1.md` Limb-D successor in the
same integrated application act. Re-entry is mandatory when DR-110 enters
a slice; this paragraph alone does not discharge D-056 gate 2. Generation rollback remains active under
DR-107/G18 and must obey current trust floors. These are different mechanisms;
neither is accepted as evidence for the other. No existing affected row is
removed by this disposition.

The hostile corpus obligation quantifies over the named behavioral classes,
not every byte string in an infinite language. Define coverage as: one positive
control; each distinct protocol state transition and refusal branch; integer
and byte-length boundaries at min/min-1/max/max+1 where representable; each
permitted terminal interleaving pair in J-1..J-5; and every CC-1..CC-11 class.
Within a class, generate the Cartesian product of applicable direction, channel
state and mutation class BEFORE executing mutations. Every generated member
has exact bytes or an explicit process event and a deterministic expected
refusal/discard/teardown observation. The coverage manifest carries the complete
member set and digest; a removed member fails the coverage check.

This explicitly supersedes the unenumerated within-class universal reading
that prevented any finite corpus from being complete. It does not assert that
sampling proves all behaviors: deterministic corpus coverage plus specified
property-based extension is the release test requirement. Four-platform runtime
fault injection and the absence of crashes remain unqualified until executed.

## 8. Closure evidence

The applied package must include actual source fixtures, expected fact/graph
records, exact malformed control frames, the preservation pre/post image,
the complete coverage manifest and independent review. Pure reference-model
execution establishes consistency of the design examples only. The per-row
record lists every remaining production execution at its owning gate; missing
design or undefined output schemas cannot be hidden in that remainder.

## 9. Concrete supplements and scoped interpretation

The quality matrix is `language-quality-matrix.completed.v2.json`: 20 explicit
provider capability/platform cells and four host integration cells. Corpus
`quality-corpus-manifest.v1.json` pins all 1,019 source/configuration files;
`native-corpus-report.v1.json` compares eight native examples through both the
TypeScript 6.0.3 compiler and the exact pinned prototype Program service.
`prototype-baseline-disposition.v1.json` records the available local prototype
and why every row uses the approved language-native corpus path instead of
claiming an equivalent full-product behavior/performance baseline. Performance definitions, runner
fields and conservative process-tree memory accounting are in the matrix.

The retained opaque preservation bytes and the no-preexisting-object sibling
are in `sarif-preservation-cases.v1.json`, checked by `check_quality_design_v2.py`.
They close the non-mutation authoring request only when independently accepted;
future authoritative qualification remains owed under §6. The current preview
output-failure execution belongs to G26/G28 and their Output/operability +
CLI/product owners; G17 remains dropped for preview and cannot carry a required
preview execution remainder. Its future valid-sealed-object re-entry is named
separately.

Incorporate the exact accepted `protocol-completion` package for its retained
NT/CC witnesses, finite corpus and shared-platform storage aliases. Its CC8
successor explicitly replaces control v2's requirement to identify provider
meaning in arbitrary `fault.detail` prose: the string is opaque diagnostic data,
never a provider event, finding, policy, D9 or exit input. Ordinary fault
supervision/teardown still occurs. Unknown structured fields/types are RF2;
unauthorized semantic actions are RF5 under the closed action grammar. The
provider stream and semantic view remain unchanged by such diagnostic text.
The full sixteen-message schema and security effect-state join must also be
authored and reviewed; the protocol package's thirteen-message matrix alone
is not claimed complete. Universal normative rules still govern arbitrary
inputs; finite vectors and generative stress are evidence, not a proof over
all possible byte strings.

G13's strict result grammar is `g13-result-schema.v2.json`. Its semantic
validator requires the exact 24 cell IDs and every fixture named by that cell,
unique IDs, exact expected/actual sets and no missing/extra/duplicate results.
Each cell points to the matching platform's performance observation; one
whole-analyze measurement may serve that platform's six cells. All four
platforms must have complete measurements. Null runner/measurements means
NON-PASS. PASS requires every behavior expectation, both latency ceilings, the
larger of observed tree peak and sum of individual high-water RSS ceilings,
and every applicable future-regression check to pass. A false claimed PASS is
a malformed gate result, not a waiver. Result/fixture/subject digest joins are
mandatory. This schema is a qualification reporting artifact, not product JSON
or a new semantic outcome vocabulary.

The release gate obtains baseline existence from the authenticated prior
qualification record for this matrix/corpus/profile, not the candidate's
self-declared `baselineStatus`. FIRST-BASELINE is permitted only when that
trusted lookup is empty; ESTABLISHED requires its exact artifact digest and
all three baseline quantities. Missing or mismatched baseline custody is
NON-PASS. The first successful qualification is retained as that baseline;
changing the matrix/corpus/profile requires an explicit threshold successor,
not a candidate claiming to be a new first baseline.
