# Bounded assessment of CB-GAP-4 and CB-GAP-5

**Standing.** Independent bounded design assessment of TWO limited blind claims. This is **not**
a fresh full acceptance review, not a blind substitute, and not authorization to implement.
No source byte was edited. No grade is issued. Any changed bytes still require a fresh full
independent review and a NEW blind consumer.

**Inputs, verified by hash before use.**

| Input | Expected | Measured | Status |
|---|---|---|---|
| Blind claim capture `original-blind-gaps2.py` | `d18839cb…c17b3b` | `d18839cb4b340f2841ac509f504d7bca9eeee87d5f93730ba695f50ba0c17b3b` | match |
| v19 manifest `candidate-subject.v19.json` | `312db9d9…f24b` | `312db9d904d0ec1f9c91d84137feb3277490b79b07bf3a6d5efc0380caa0f24b` | match |

Manifest standing: `FROZEN CORRECTED CANDIDATE FOR FRESH INDEPENDENT REVIEW; NO ACCEPTANCE`,
`reviewPending: true`, `applicationPending: true`, 8653 files.

I did not inspect the concurrent corrections author's directory, and did not access the original
blind reviewer's active directory or log. The only blind input used is the captured file above.

**Reference environment.** The frozen model pins Unicode case data 15.0.0 and raises
`ReferenceEnvironmentError` under any other; CPython 3.12.13 (Unicode 15.0.0) was used.
Baseline control before any probe: `check-identity.py` → **1431 passed, 0 failed**. Every probe
below re-ran that same baseline in-process, so each measured result is stated against a green tree.

---

## 1. CB-GAP-4 — stage-spec `operation` and both `outputDomains` carry no named vocabulary

### Disposition: **ACCEPTED**, premise upheld; basis materially sharpened. Remaining obligation: **SHOULD**.

The blind claim's factual assertions are all independently reproduced, and the underlying
defect is more extensive than the claim measured. The claim was established by schema inspection
only; I closed real Runs.

### 1.1 What the owning normative text actually says

`outputDomains` appears in exactly **two** normative places in the whole corpus
(exhaustive sweep of `docs/v2` and the foundation schemas):

- `docs/v2/contracts/product-v1/identity-and-evidence.md:1092` — the §3 field list.
- `identity-and-evidence.md:1097` — the one rule: *"its `outputDomains` equal the stage's"*.

`stage-spec.operation` is named at `:1092` and **never defined anywhere**. The contrast is
inside the same paragraph block: §3 defines `program-predicate.operation` precisely at
`identity-and-evidence.md:1069` — *"`operation` is one of the seven evaluator predicates and
equals both the addressed node's `op` and the predicate proof's `operation`"*. So §3 bounds one
`operation` field and leaves the sibling one open. The schema carries `$ref: #/$defs/Text`
(`{type:string, minLength:1, maxLength:4096}`) for `stage-spec.operation`, `Text` for
`stage-spec.outputDomains[]`, and an inline equivalent for
`execution-plan.stages[].outputDomains[]`. No `x-opensip-vocabulary` on any of the three;
the bundle carries exactly two such annotations, both on `analysis-spec.requestedCapabilities[]`.

### 1.2 Independently measured controls (not inspection)

Each probe re-mints the exact dependent chain — stage-spec bytes → `execution-plan` →
`proof-bundle` → `semantic-evidence` → `evaluation-seal` → `run` — and calls the real
`close_run`. The Plan is *not* re-minted, because no Plan field names the execution plan;
that is why an `operation` edit moves RunId but not PlanId.

| Probe | Value written | `close_run` | RunId ≠ baseline |
|---|---|---|---|
| `G4-OP-native.analyze` | `native.analyze` | **ACCEPT** | yes |
| `G4-OP-analyze` | `analyze` | **ACCEPT** | yes |
| `G4-OP-derive` | `derive` | **ACCEPT** | yes |
| `G4-OP-emoji` | `😀 not an operation at all` | **ACCEPT** | yes |
| `G4-OP-empty` | `""` | REFUSE (`minLength`) | — |
| `G4-DOM-view2` | `["view2"]` both sides | **ACCEPT** | yes |
| `G4-DOM-scope2` | `["scope2"]` both sides | **ACCEPT** | yes |
| `G4-DOM-subject-scope` | `["subject-scope"]` both sides | **ACCEPT** | yes |
| `G4-DOM-unregistered` | `["totally-unregistered-domain-xyz"]` | **ACCEPT** | yes |
| `G4-DOM-empty-array` | `[]` both sides | **ACCEPT** | yes |
| `G4-DOM-mismatch-control` | spec `["fact"]` vs stage `["view"]` | REFUSE `STAGE_SPEC_OUTPUT_DOMAIN_JOIN` | — |

Baseline RunId `run2:5e215948…`; every accepting probe minted a distinct RunId. The control row
confirms the blind's `notMitigatedBy` verbatim: the **only** enforced rule is the internal
spec↔stage equality, which is satisfied when both sides are spelled the same wrong way.

Two findings the blind did **not** measure:

- `outputDomains: []` closes. A stage may declare **no output domain at all** and still seal a Run.
- The frozen source itself already spells the field two ways: `check-identity.py:824` writes
  `operation: 'derive-references-view'`, while `VECTOR_STAGE_SPEC` at `check-identity.py:1397`
  writes `operation: 'derive'`. The drift the claim predicts is already present in the reference
  fixture.

### 1.3 The decisive argument the blind did not make

The blind argued from a *missing annotation*. The stronger and more precise argument is from
**an established closed vocabulary in the same bundle**. Every other field in
`identity-schemas.v2.json` that names a *domain* is a closed enum drawn from the
`x-opensip-digest-domains` registry keys:

| Selector | Form | Members |
|---|---|---|
| `#/$defs/Ref/properties/domain` | `enum` | 32 |
| `#/$defs/ProofInputRef/properties/domain` | `enum` | 12 |
| `#/$defs/FindingEvidenceRef/properties/domain` | `enum` | 5 |
| `#/$defs/stage-spec/properties/outputDomains/items` | **free `Text`** | unbounded |
| `#/$defs/execution-plan/…/outputDomains/items` | **free `string`** | unbounded |

And real usage already conforms to that registry: the frozen fixture writes `["view"]`
(`check-identity.py:824-825`), the rejection control writes `["fact"]` (`:1521`), and
`consumer-b.v7/output/work/build.py:279` writes `["coverage","fact"]`. Every value in live use
is a `Ref.domain` enum member.

So for `outputDomains` the vocabulary is **already determined by construction and merely
unstated**. This is not implementation freedom; it is an omitted enum. The bundle's own stated
stance is `x-opensip-payload-registry.law.unregistered`: *"a key with no row refuses; there is no
default row and no caller-selected schema."*

`operation` is a **different question** and must not be conflated. There is no existing authority:
`#/$defs/closure` carries only `kind`, `manifestDigest`, `tree`, `semanticVersion`,
`protocolMajor`, `platform` — no declared operation set — and no schema in the corpus declares
provider operations. The nearest owner is `docs/coop/artifacts/c2-plan-stage-schema.v4.json`,
which defines closed `stageSchemas.kinds` (`fact-derivation`, `rule-evaluation`,
`policy-evaluation`, `probe`) and an `operatorAuthority` enum — but its own `status` reads
`CANDIDATE-NOT-APPLIED / AWAITING-INDEPENDENT-REVIEW … DO-NOT-SEAL`, and its `reviewStatus`
records a REJECT verdict against v3. **It is not authority in v19 and must not be cited as one.**

### 1.4 Answering the architectural question directly

*Is a stage operation fixed platform vocabulary, a provider-closure-defined semantic token, or a
versioned declared operation?* On the evidence it cannot be the first — stages are provider acts
(`closureKinds.byField` binds `stage-spec.producerClosure: provider`) and a fixed identity-level
enum would freeze third-party provider capability. It is properly a **declared operation owned by
the producer closure's protocol**, and the c2 artifact's own `privateOperators.plannerFreedom`
states the governing principle: physical planning may *"insert, reorder, fuse or elide freely,
provided the logical stage contract and the resulting EvidenceDigest are unchanged"*. That is the
test. Because `operation` enters `stageSpecDigest` → `exec-plan2` → `proof2` → `seal2` → RunId, it
is being treated as **logical stage identity**. A field with that role must come from a named
vocabulary; if it were instead a producer-private physical label it should not enter identity at
all. Today it is neither — it is an unbounded free string inside a canonical identity input.

### 1.5 Proposed minimal correction (for the source coauthor; not applied here)

Two separable changes, deliberately different in strength.

**(a) `outputDomains` — closable now, byte-compatible.** Add to both selectors the annotation
already used for `capabilityId`, and state the rule in §3 beside the existing equality sentence.

Schema, at `#/$defs/stage-spec/properties/outputDomains/items` and
`#/$defs/execution-plan/properties/stages/items/properties/outputDomains/items`:

```json
"x-opensip-vocabulary": {
  "authority": "foundation/identity-schemas.v2.json#/x-opensip-digest-domains/byDomain",
  "admittedBy": "foundation close_run (STAGE_SPEC_OUTPUT_DOMAIN_UNREGISTERED)",
  "note": "The domain a stage declares it produces, named from the SAME registry Ref.domain, ProofInputRef.domain and FindingEvidenceRef.domain already draw on. This field enters stageSpecDigest and therefore RunId, so an unregistered spelling mints a different RunId for one analysis."
}
```

Proposed §3 sentence, appended to the existing clause at `identity-and-evidence.md:1097`
(*"its `outputDomains` equal the stage's"*):

> Each member of `outputDomains` MUST be a domain name registered in
> `x-opensip-digest-domains.byDomain`; a stage declares which registered domains it produces,
> in the same vocabulary every `domain` field in this bundle uses. The equality between the stage
> spec and the stage is necessary and not sufficient: two records agreeing on an unregistered
> spelling are both refused.

**(b) `operation` — state the owner, do not invent an enum.** Do not bind identity to an
unaccepted artifact and do not create a new registry inside the identity bundle. The minimal
honest step is a §3 sentence that fixes the semantic owner and the determinism obligation:

> `operation` names the logical act the stage's `producerClosure` performed. It is a token of
> that closure's declared protocol vocabulary, not a free label and not a physical plan detail:
> it enters `stageSpecDigest` and therefore RunId, so two conforming hosts running one analysis
> with one selected producer closure MUST write one spelling. Where the producer protocol
> publishes a closed operation vocabulary, admission refuses a token outside it.

Whether to go further — a declared-operation list on the component manifest, or applying the
c2 stage vocabulary — is a decision for the source coauthor and the c2 lane, **out of scope for
this assessment** and dependent on that artifact's own independent review.

**Open judgment call flagged, not decided:** `outputDomains: []` currently closes. If no
legitimate stage produces nothing, `minItems: 1` belongs on both selectors. If a no-output stage
is lawful (a pure precondition or ordering stage), it should be stated rather than left silent.
I did not find text either way, so I do not assert which is intended.

### 1.6 Compatibility, routing, before/after

- **Compatibility of (a): zero byte change to any lawful graph.** Every value in live use
  (`view`, `fact`, `coverage`) is already a `byDomain` key. No identity recipe changes, no digest
  changes, no RunId changes. Expected after: `check-identity.py` still **1431 passed, 0 failed**.
  Only previously-admissible malformed inputs newly refuse — precisely the "explicit admission
  guard only for previously ambiguous malformed inputs" shape root prefers.
- **Compatibility of (b): prose only**, no schema constraint, no behavioural change, until the
  producer protocol publishes a vocabulary.
- **Owning selectors affected:** the two `outputDomains` items selectors, plus
  `identity-and-evidence.md` §3 at `:1097`. `cache-key`/`regeneration-key` are *not* affected —
  they carry `stageSpecDigest` and `outputSchemaDigest`, not `outputDomains`.
- **Routing.** A refusal here is an identity Run-closure admission fault, an internal closed code
  in the `AdmissionError` family alongside the existing `STAGE_SPEC_OUTPUT_DOMAIN_JOIN`,
  `STAGE_SPEC_UNSELECTED_PRODUCER` and `STAGE_SPEC_HIDDEN_PARAMETER`. It is **origin-independent**
  — a malformed retained record is malformed whoever produced it — and it takes the existing
  structural-evidence route (`request-rejected` / `REQUEST.PRECONDITION_FAILED`, exit 2, per
  `identity-and-evidence.md:1393-1395`). It needs **no new public `DomainDetailCode`**: no
  identity closure-join fault is in `public-detail-registry.v1.json` today (its 6 identity/
  foundation records are all `evidence.*` availability/retention details), and that registry's
  `aliasRule` states that absence of an alias "is a positive statement about a key, not an
  omission." Adding one would be a scope increase, not a completion.

### 1.7 CB-GAP-4 verdict

- **Premise:** accepted as written.
- **Severity:** the blind's `SHOULD` is right for `outputDomains` and right for `operation`.
  Neither is a MUST: no lawful graph is currently mis-admitted and no accepted Run is wrong.
  The defect is that two conforming hosts are not *compelled* to agree.
- **Source correction required:** yes for (a) — schema annotation plus one §3 sentence.
  Prose-only for (b).
- **technicalAssent:** true. **changesRequired:** true.

---

## 2. CB-GAP-5 — `plan.semanticClosures` membership "published for exactly one field"

### Disposition: **REJECTED as stated**; narrowed to a genuine but much smaller residual. Remaining obligation: **SHOULD, reporting/normative clarification only — no schema guard, no behaviour change.**

Root's prior finding is confirmed and can be strengthened: the headline is false, the stated
consequence mis-describes the mechanism, and the claim's own stated reason for not closing its
graph is factually wrong. A real residual survives, but it is a documentation gap, not a
determinism defect.

### 2.1 The headline is false

The claim says membership is stated "for EXACTLY ONE field and for no other closure the graph
names". Measured across the corpus:

- **Schema descriptions: the claim's count is correct.** An exhaustive walk of
  `identity-schemas.v2.json` finds exactly one description mentioning Plan selection —
  `#/$defs/subject-scope/properties/enumeratorClosure`.
- **Normative prose: the claim is wrong.** `identity-and-evidence.md:1096-1097` states the stage
  spec's *"`producerClosure` is a **Plan-selected** semantic closure"*, and `:1287` states, for
  cache admission, *"the producing closure retained and **Plan-selected**"*. Membership is
  published for at least three fields, in the contract that owns them. A schema `description` is
  not the only place a rule may live, and §3 is the owning normative text.

### 2.2 The enforcement matrix the claim omits

Measured in the frozen `identity-model.py`. Of the ten identity fields the claim lists as carrying
"NO such statement", **eight are closed**:

| Field | How bound | Closed code / mechanism |
|---|---|---|
| `subject-scope.enumeratorClosure` | direct member | `UNSELECTED_ENUMERATOR` (`:1473`) |
| `view.producerClosure` | direct member | `UNSELECTED_PRODUCER` (`:1469`) |
| `stage-spec.producerClosure` | direct member | `STAGE_SPEC_UNSELECTED_PRODUCER` (`:1406`) |
| `cache-key.producerClosure` | direct member | `CACHE_UNSELECTED_PRODUCER` (`:1647`) |
| `finding.ruleClosure` | direct member | `FINDING_RULE_CLOSURE_UNSELECTED` (`:1442`) |
| `evaluation-seal.evaluatorClosure` | direct member | `UNSELECTED_EVALUATOR` (`:1297`) |
| `fact.producerClosure` | **transitive** — must equal `view.producerClosure` | `FACT_SOURCE_PRODUCER_JOIN` (`:1508`) |
| `proof-bundle.evaluatorClosure` | **transitive** — must equal `seal.evaluatorClosure` | `EVALUATOR_JOIN` (`:1288`) |
| `import.producerClosure` / `adapterClosure` | bound by a **different Plan selector**, `plan.importIds` | `IMPORT_JOIN` (`:1290`), `UNSELECTED_EVALUATION_IMPORT` (`:1428`), `CACHE_INPUT_IMPORT_NOT_SELECTED` (`:1664`) |
| native `toolchain` / `stdlib` / `rust-dev-llvm` / `grammar` | bound by `plan.nativeContextDigests` + `domainSets[].closureJoins` | `UNIVERSE_CONTEXT_NOT_SELECTED` (`:1343`), `NATIVE_CONTEXT_SET_JOIN` (`:1311`) |

The last two rows are exactly the transitive retention the assessment brief warned against
flattening. Native contexts already bind their toolchain, stdlib, LLVM and grammar closures
through `x-opensip-digest-domains.domainSets[].closureJoins`, and imports carry their own
producer/adapter closures inside a Plan-selected `import2`. **Requiring these to be direct
`plan.semanticClosures` members would be wrong**, and the claim's own reconstruction choice —
"I chose to include the toolchain and stdlib closures" — flattened a dependency the design
deliberately retains transitively.

### 2.3 The claim's stated reason for not closing its graph is wrong

The claim declines to build the discriminating control because *"every retained view, scope and
fact names the original plan2 and re-minting all of them would be a second complete graph."*
Measured against the schema:

| Record | carries `planId` |
|---|---|
| `subject-scope` | **no** — binds `snapshotId`, `sourceUniverse` |
| `fact` | **no** — binds `snapshotId`, `sourceUniverse` |
| `coverage` | **no** — binds `scopeId` |
| `view`, `stage-spec`, `execution-plan`, `proof-bundle`, `semantic-evidence`, `evaluation-seal`, `run`, `cache-key` | yes |

Scopes and facts do **not** name a Plan. The re-mint is eight records, not a second complete
graph — so the control was available and was not taken. I took it.

### 2.4 The control the claim did not run

Re-minting `plan → view → stage-spec → execution-plan → proof-bundle (including the view digest
its `evaluationInputRefs` and `predicateProofs[].inputRefs` carry) → semantic-evidence →
evaluation-seal → run`, leaving scopes, facts and coverage untouched:

| Probe | Plan `semanticClosures` | `close_run` |
|---|---|---|
| `BASE` | `{provider, evaluator}` (fixture default) | ACCEPT `run2:5e215948…` |
| `G5-SUPERSET` | `+ toolchain` | **ACCEPT** `run2:99a27df3…`, new PlanId |
| `G5-SUPERSET-ALL` | `+ toolchain ×2, stdlib, rust-dev-llvm, grammar` (all 5 retained) | **ACCEPT** `run2:71c30d44…` |
| `G5-PHANTOM` | `+ closure2:eeee…` (not retained) | REFUSE `EVIDENCE_UNAVAILABLE` |
| `G5-NARROW` | drop the used enumerator | REFUSE `UNSELECTED_ENUMERATOR` |

So the mechanism is precisely: **an enforced lower bound and no upper bound.** Every closure the
graph actually uses must be a direct member (six distinct closed codes enforce it); any additional
**retained and admissible** closure may also be selected; a closure that does not exist cannot be.

### 2.5 Why the superset tolerance is design, not defect

This is the decisive measurement, and it disposes of the claim's consequence.

The v19 fixture's own Plan declares **three** `nativeContextDigests`. Dropping them one at a time:

```
drop 1aa71d2e5be1 -> ACCEPT   (not load-bearing)
drop b12a5d2f1d7e -> REFUSE   UNIVERSE_CONTEXT_NOT_SELECTED
drop d91e9cb39f65 -> ACCEPT   (not load-bearing)
MINIMAL closing context set size 1: ['b12a5d2f1d7e']
```

**The accepted reference fixture ships a Plan that selects two native contexts it does not use,
and the 1431-check suite passes.** Over-selection is therefore an exercised, in-source property of
Plan selection generally — not an anomaly of `semanticClosures`. `plan.nativeContextDigests` shows
the identical lower-bound/open-upper-bound shape, and `NATIVE_CONTEXT_SET_JOIN` at `:1311` is
equality against *the set the walk reached*, which the Plan's own declaration feeds.

This is coherent: **a Plan is a declaration of selection, and a deliberately larger selection is a
different analysis request with a different identity.** That is exactly the distinction the brief
draws — different deliberately selected extra closures are different semantic inputs, not
nondeterminism. The claim's consequence, *"two conforming hosts analysing one repository with one
toolchain can list {provider, evaluator} or {provider, evaluator, toolchain, stdlib} and mint
different PlanIds and RunIds for the same analysis"*, mis-describes this: those are two different
Plans, and the design intends a Plan's identity to include what it selected. Nothing forces one
analysis to a single Plan, and §2 already separates operational from semantic identity
(`identity-and-evidence.md:82`: *"Identical semantic inputs can…"*).

Note the contrast with CB-GAP-4, which is a genuine defect for the opposite reason: there, two
hosts describing the **same** stage with the **same** closure are free to spell one field
differently. Here, two hosts choosing different closure sets have made different choices.

### 2.6 The genuine residual

Stripped of the false headline and the mistaken consequence, one real gap survives:

> The **lower bound is enforced in six places by six distinct closed codes and stated in the
> contract for only two of them** (`stage-spec` at `:1096-1097`, cache at `:1287`) — and never as
> a general rule. There is no sentence anywhere telling an implementer *which* closures a Plan
> must select. An implementer constructing a Plan discovers the rule only by refusal.

That is a real obligation under the brief's own standard — an implementer must not have to invent
a required authoritative record's meaning — but it is a **documentation** obligation. The
behaviour is already correct, complete and total; only its statement is missing.

The upper bound needs no change and should not get one. Constraining `semanticClosures` to an
exact minimal set would refuse the fixture's own over-selecting Plan shape, break lawful positive
graphs, and contradict `nativeContextDigests`.

### 2.7 Proposed minimal correction (for the source coauthor; not applied here)

**Reporting/normative clarification only. No schema constraint, no new refusal code, no
behavioural change.**

Proposed §3 sentence, to sit beside the existing closure list at `identity-and-evidence.md:1126`:

> `plan.semanticClosures` is the set of semantic closures this Plan selects. Every closure the
> retained graph names directly — a scope's `enumeratorClosure`, a view's, fact's, stage spec's
> or cache key's `producerClosure`, a finding's `ruleClosure`, and the proof bundle's and seal's
> `evaluatorClosure` — MUST be a member, and Run closure refuses each by its own name. Closures
> reached *through* another selected input are NOT direct members and MUST NOT be required to be:
> a native context's `toolchain`, `stdlib`, `rust-dev-llvm` and `grammar` closures are retained
> through `plan.nativeContextDigests` and the `domainSets` closure joins, and an import's
> `producerClosure` and `adapterClosure` through `plan.importIds`. The set is a lower bound, not
> an exact one: a Plan MAY select a further retained closure, and doing so is a different
> selection with its own PlanId, not a variant spelling of the same one.

Optionally, a machine-readable `closureMembership` block beside the existing
`x-opensip-digest-domains.closureKinds.byField` — which already states *kind* per field and would
then state *binding* per field, using the same field keys:

```json
"closureMembership": {
  "standing": "Which Plan selector binds each closure-bearing field. Stated so no field is left to guess. Companion to closureKinds.byField, which states KIND.",
  "direct": {
    "subject-scope.enumeratorClosure": "plan.semanticClosures (UNSELECTED_ENUMERATOR)",
    "view.producerClosure": "plan.semanticClosures (UNSELECTED_PRODUCER)",
    "stage-spec.producerClosure": "plan.semanticClosures (STAGE_SPEC_UNSELECTED_PRODUCER)",
    "cache-key.producerClosure": "plan.semanticClosures (CACHE_UNSELECTED_PRODUCER)",
    "finding.ruleClosure": "plan.semanticClosures (FINDING_RULE_CLOSURE_UNSELECTED)",
    "evaluation-seal.evaluatorClosure": "plan.semanticClosures (UNSELECTED_EVALUATOR)"
  },
  "transitive": {
    "fact.producerClosure": "equals view.producerClosure (FACT_SOURCE_PRODUCER_JOIN)",
    "proof-bundle.evaluatorClosure": "equals evaluation-seal.evaluatorClosure (EVALUATOR_JOIN)",
    "import.producerClosure": "retained through plan.importIds",
    "import.adapterClosure": "retained through plan.importIds",
    "TypeScriptToolClosureV1.closureId": "retained through plan.nativeContextDigests closureJoins",
    "ToolClosureV1.closureId": "retained through plan.nativeContextDigests closureJoins",
    "toolchain.typescriptStdlibMerkleRoot": "retained through plan.nativeContextDigests closureJoins",
    "toolchain.rustcDevLlvmDigest": "retained through plan.nativeContextDigests closureJoins",
    "SyntaxGrammarBundleV1.closureId": "retained through plan.nativeContextDigests closureJoins"
  },
  "cardinality": "lower bound only; a Plan MAY select a further retained closure and that is a different PlanId"
}
```

This is **descriptive of behaviour I measured**, not a promise of unspecified behaviour: every
`direct` row was reproduced by a refusing probe or read at its enforcing line, and every
`transitive` row at its enforcing join. It adds no rule.

### 2.8 Compatibility, routing, before/after

- **No behavioural change whatsoever.** Expected after: `check-identity.py` still
  **1431 passed, 0 failed**, byte-identical identity recipes, no digest or RunId movement.
- **Owning selectors affected:** `identity-and-evidence.md` §3 (prose), and optionally
  `identity-schemas.v2.json#/x-opensip-digest-domains` (a new sibling annotation key; it does not
  touch `$defs` and so cannot affect validation).
- **Routing:** none. No new refusal, no new public code, no origin-dependence. The six existing
  internal `AdmissionError` codes keep their names and their absence from
  `public-detail-registry.v1.json`.

### 2.9 CB-GAP-5 verdict

- **Premise:** rejected as stated (headline false; consequence mis-describes the mechanism;
  the stated reason for not closing the graph is factually wrong). **Narrowed** to: the
  selection rule is enforced but never stated as a rule.
- **Severity:** **SHOULD**, reporting/clarification only. Not a MUST — no lawful graph is
  mis-admitted, and the claim's `SHOULD` label happens to land right for the wrong reason.
- **Source correction required:** documentation only. No schema guard. **Explicitly do not**
  add an exact-set or minimality constraint on `plan.semanticClosures`.
- **technicalAssent:** false as claimed; true for the narrowed residual.
  **changesRequired:** true (prose), false (behaviour).

---

## 3. Concrete disposition

| ID | Premise | Remaining obligation | Correction type | technicalAssent | changesRequired |
|---|---|---|---|---|---|
| CB-GAP-4 | **accepted** | **SHOULD** — name the vocabulary for `outputDomains`; state the semantic owner for `operation` | source: schema annotation ×2 + §3 prose | true | true |
| CB-GAP-5 | **rejected as stated → narrowed** | **SHOULD** — state the selection rule that is already enforced | reporting/normative clarification only; **no** schema guard | false as claimed / true as narrowed | true (prose only) |

**Recommended sequencing.** CB-GAP-4(a) and CB-GAP-5 are independent and both byte-compatible with
every lawful graph; either may proceed. CB-GAP-4(b) should be drafted as prose only and must not
be bound to `c2-plan-stage-schema.v4.json` while that artifact remains
`CANDIDATE-NOT-APPLIED / DO-NOT-SEAL` with an unresolved REJECT on its predecessor.

**Two items referred, not decided by me.** (i) Whether `outputDomains: []` is lawful — I found no
text either way and did not assert one. (ii) Whether the producer protocol should publish a closed
operation vocabulary — that belongs to the c2 lane and its own independent review.

**Limits of this assessment.** Two claims only. Everything asserted as measured was produced by
`probes.py` / `probes2.py` against the frozen v19 model on a green 1431-check baseline; everything
else is cited to a file and line and labelled as inspection. I did not review the rest of v19, did
not evaluate the concurrent three-gap correction, and issue no grade and no acceptance. Changed
bytes still require a fresh full independent review and a NEW blind consumer.

## 4. Artifacts in this directory

| File | What it is |
|---|---|
| `assessment.md` | this report |
| `assessment.json` | machine-readable form of §3 and the per-ID findings |
| `probes.py` | CB-GAP-4 and CB-GAP-5 discriminating probes |
| `probe-results.json` | measured output of `probes.py` |
| `probes2.py` | Plan-selector comparator probes |
| `probe2-results.json` | measured output of `probes2.py` |
| `_remint.py` | shared complete Plan re-mint helper |
| `original-blind-gaps2.py` | the captured blind input (unmodified) |
