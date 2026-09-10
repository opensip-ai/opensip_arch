# v20 coauthor handoff — CB-GAP-1, CB-GAP-2, CB-GAP-3

**Role.** Actual Claude source coauthor. I am not the independent reviewer of these
changes and not the blind consumer. Everything below is a **proposed source delta**:
no grade, no acceptance, no application authority, and no claim of host, compiler,
grammar, provider, OS or platform qualification. A fresh freeze, a fresh independent
source review and a **new** blind consumer over the corrected bytes all remain owed.

**Custody.** All 8653 paths declared by `candidate-subject.v19.json`
(`312db9d9…`) were re-hashed before any edit: 0 missing, 0 mismatched, 0 undeclared.
Afterwards: still 8653 files, **10 changed**, 0 added, 0 removed. Pin ledgers,
generated canonical reports, `reviews/`, README/current-design/readiness/governance/
crosswalk and application records are all delivered at their accepted19 bytes. The
live repository and the `candidate-subject.v19` snapshot were read only.

**How I measured the gaps.** I did not read, run or rely on the blind consumer's own
reconstruction or its session. I took root's independently captured probe inputs and
root's captured object graphs from `blind8-gap-reproduction.v1` and replayed them
through *my* copy of the accepted19 reference models. All three reproduced, and
CB-GAP-1 came back with root's exact `runId` and both binding digests.

---

## CB-GAP-1 (MUST) — at most one selected parameter per registered row

**Reproduced.** The Run closed; `verify_scope_parameter_binding` returned a *verified*
digest for **both** candidate scope documents; the pre-Plan boundary admitted the spec.

**Assessment — the blind's diagnosis of *why* is exact.** The payload registry closes
which documents a parameter may cite, and refuses two **registry rows** resolving to one
document digest (`PAYLOAD_PARAMETER_AMBIGUOUS_ROW`). Nothing constrained how many
**spec entries** may cite one row. The registry's own prose reasons carefully about the
first question and never reaches the second. The consequence is not cosmetic: the
verifier is *existential* over the selected rows, so whichever document a caller
happened to hold came back verified while another was equally selected — and both
entries enter `analysisSpecDigest` and therefore the `PlanId`, so two conforming hosts
bind different scope policies from **one admitted Plan** and attribute the E2→E3
comparison scope axis differently for the same Plan.

**Root's preferred semantics is right, and I adopted it.** *At most one* is the only
answer that invents no authority. A default, a first/last winner or a merge would each
be the registry making the arbitrary selection its own law declines to make one level
up, and the digest recipes give no basis for preferring either payload. Zero stays
legal — most analyses need no scope-policy input — and the caller that *does* need it
still meets the explicit missing-selection refusal, so nothing is silently substituted.
I asserted rather than assumed that the foundation `scope-descriptor` does not become a
fallback.

**One generalisation I judged necessary.** I published the law for the parameter
**class**, not for the `ScopeDocumentV1` row alone. Both registered rows are Plan
inputs and the ambiguity argument is identical for either; a rule written for one row
would have left the sibling to be rediscovered — exactly the failure mode being
corrected. `ImportSourceContextV1`'s zero/one/multiple rule is unchanged and is now
*total* rather than reachable only from the import derivation.

**Precedence, named exactly.** At retained closure, most-specific-first: the retained
analysis-spec is schema-validated first, so a **whole-item duplicate** refuses on
`uniqueItems` and never reports the selection key (measured — the observed text is
jsonschema's `uniqueItems`, not the ambiguity key); `IMPORT_SOURCE_CONTEXT_MULTIPLE`
keeps its name inside the derivation that consumes its row; `admit_parameter_selection`
runs after that as the total backstop and names the offending row. At the pre-Plan
boundary the published cardinality → schema → vocabulary order is preserved *verbatim*
and the foundation law is **appended** as step 4, so no existing route is reclassified.
At the verifier: zero → the existing `BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER`; more
than one → the ambiguity refusal, **before** any payload comparison; one-and-mismatched
→ the existing `BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH`. That order is the point —
checking the digest first would let a caller holding one of two candidates obtain a
"verified" digest, which is the existential proof that made the entries
indistinguishable in the first place.

**No new vocabulary.** The two foundation refusals are internal closure
`AdmissionError`s in the same class as their existing sibling
`IMPORT_SOURCE_CONTEXT_MULTIPLE`. The verifier reuses `CONFIG.INVALID`, a member of
both the closed `D9ErrorCode` enum and the closed `DomainDetailCode` registry; a
control validates the composed termination against the real `StepTermination` carrier,
and a second proves that carrier would have **refused** an invented
`BASELINE.SCOPE_PARAMETER_AMBIGUOUS` spelling.

**After.** Captured *before* the CB-GAP-2/3 schema edits, so it is like-for-like on the
identical frozen bytes: retained closure and the pre-Plan boundary both refuse with
`ANALYSIS_SPEC_PARAMETER_SELECTION_AMBIGUOUS:workflows/schemas/policy-document.schema.json#/$defs/ScopeDocumentV1`,
and **both** bindings now refuse with `CONFIG.INVALID`.

---

## CB-GAP-2 (SHOULD) — the requestedCapabilities ownership tuple

**Reproduced.** Schema, `admit_requested_capabilities` and `admit_analysis_spec` all
admitted two rows for one `(inventory, ts-tsconfig, .)` differing only in `required`.

**I looked for the law that would have invalidated the gap, and there is none.**
`uniqueItems` admits the pair because two rows differing in `required` are *distinct*
items; `x-opensip-order: canonical-set` **orders** them rather than refusing them; the
vocabulary helper judges each row alone against the matrix and never compares rows; and
retained closure re-runs that same helper. No document states a requiredness precedence
and no selector could be substantiated. Both rows enter `analysisSpecDigest` and
therefore the `PlanId`, so the contradiction is **committed** — and `required` decides
whether a missing Coverage entry contributes `indeterminate`.

**Architectural refinement.** I placed the rule in `admit_requested_capabilities`, the
helper **both** the pre-Plan boundary and retained closure call, so they agree by
construction rather than by review. That required distinguishing it from the published
sentence *"IT DOES NOT GUARD CARDINALITY, deliberately"*, which is about population
**size** — a pre-Plan selection bound with no meaning for a retained record. Uniqueness
of the ownership tuple is a **determinacy** property of what the record *means* and
must hold wherever the record is read. The docstring now states that distinction
rather than leaving the two rules looking contradictory.

**Precedence.** Schema-first for malformed within-bound records (a byte-identical row
refuses on `uniqueItems` at `validate_foundation`, measured); the cardinality-first
special route for an actually oversized request is untouched (measured —
`PROJECT.SCOPE_LIMIT` still wins over a duplicate tuple in the same spec); inside the
helper the vocabulary loop runs first, so an unregistered capability, an unregistered
mode and a `NOT-SELECTED` cell each keep their own more specific refusal. Two rows
cannot contend for ownership of a cell that is not a registered cell at all.

**Public routing.** New **internal** key
`native.requested-capability-duplicate-ownership-tuple`, registered in
`x-opensip-public-route-registry` as origin-dependent over the three **existing**
routes — `CONFIG.INVALID` / `REQUEST.PRECONDITION_FAILED` +
`native.capability-spec-invalid` / `SYSTEM.OUTCOME.ILLEGAL_STATE` with `host-invariant`
+ `HOST.INVARIANT_VIOLATED`. **No public `DomainDetailCode` member is added**, asserted
by a control against the registry and independently by the security unit's own
closed-set sweep. Per the registry's own `aliasMapIsContextFree` rule an
origin-*dependent* key must **not** appear in `internalAliases`, so
`public-detail-registry.v1.json` is untouched and a control asserts that absence is
correct rather than an omission. Complete failure envelopes are composed for all three
origins.

**An adjacent copy that would have shipped a wrong answer.** `PUBLIC_ROUTE_REMEDIES` is
keyed by **public code**, not by internal key, so the new key silently inherited *"name
a registered capability id from the native capability matrix"* — the wrong next step for
a duplicate tuple. Two strings were widened to state both conditions honestly; no code,
class, exit code or route changed. The structural fix (keying by code *and* key) was not
taken — see `V20-ROOT-5`.

**Default construction.** The matrix-fixed default emits `required: True` for every row,
so it can never produce a tuple duplicate that is not *also* byte-identical — which the
existing `DUPLICATE_REQUESTED_CAPABILITY` guard already refuses rather than
deduplicating, so no requested analysis is silently lost. Measured on both branches: two
co-located units in one mode refuse; in different modes both are still selected.

---

## CB-GAP-3 (MUST) — RC-6, and why it is an implication

**Reproduced.** The Run closed, and the producer helper returned **no** fault for the
entry either — the gap was open at both boundaries, not only at closure.

**Assessment.** Section 4.1 commits the examined-partition question in two places and
nothing joined them. RC-2 reads `examinedExhaustive` for a **resolved** rung only, so on
the twelve non-resolved pairs nothing read it at all — and `file@enumerated` is one of
them, which is why the vector chose it. That entry is not harmless there:
`coverage=complete` on `file@enumerated` carries the inventory-totality obligation,
which keys on `coverage` alone. RC-1's sentence *"`examinedExhaustive` stays the
independent examined-partition claim of §4.1"* is an accurate **half-truth** —
independent of the *resolution state* — and reading it as unconstrained is what left the
join unstated. I corrected that sentence to say what it meant.

**Where I disagree with the blind, on the substance.** Its title calls these *"two
committed encodings of one claim"* and asks for *"an equality the closure decides"*. An
equality would be **wrong** and would refuse lawful evidence. `examinedExhaustive` is
about the *examination*; `coverage` is the *answer* over what was examined. A host may
examine the committed partition exhaustively and still answer `unknown` because the
evidence it needs is **missing rather than unexamined** — ambiguous or missing Rust
compilation ownership, an undeclared or unservable capability, an unlisted source
variant. An equality would force a host to understate its own examination in order to
report an honest unknown, and would refuse exactly the disclosures §10 requires. So the
published rule is one-directional: `coverage=complete` **requires**
`examinedExhaustive=true`; `coverage=unknown` constrains it in **neither** direction.
Both `unknown` positives are pinned by controls *and* by reference cases so a later
reader cannot quietly tighten it.

**Totality and scope.** RC-6 runs before the rung branch and without a `continue`, so it
is total over every registered `(relation, rung)` pair — all 17, asserted by a loop —
and independent of RC-1/RC-2, which still report on the same entry. It needs no fact:
asserted equal for an empty and for a non-matching fact set, which is the fact-free
shape a fact-admission guard cannot protect. RC-0 still runs first. It reads `coverage`
only when the entry carries it: `coverage` is required by `ViewEntryV3` and the producer
schema-validates first, but the three pre-existing *direct* `coverage_bijection` cases
pass a bare completeness fragment, and inventing a claim for them would be the checker
asserting something the caller never made. **No new key and no new public detail** — an
RC-6 disagreement is an ordinary bijection fault on the existing
`native.coverage-bijection-mismatch` carrier (operational-failed 4,
`PROVIDER.PROTOCOL_VIOLATION`).

**Masking, reported rather than worked around.** After the CB-GAP-2/3 edits,
`native-evidence.schemas.v2.json` is a changed source and its raw SHA-256 *is*
`coverage2.payloadSchemaDigest`. Every frozen `coverage2` identity in root's captured
graph therefore refuses at `PAYLOAD_SCHEMA_NOT_THE_REGISTERED_DOCUMENT` — **one guard
before RC-6**. Calling that an RC-6 refusal would be false. What is still like-for-like:
the producer helper run on the **exact retained payload bytes** from the frozen graph
now reports the RC-6 fault. For retained closure I rebuilt the same vector shape under
the changed bytes — `file@enumerated`, `coverage=complete`, `state=not-applicable`,
`examinedExhaustive=false` — in **two** universes, each with its own positive control:
both close honestly when consistent, and both refuse with **RC-6 as the only reported
fault** when contradictory.

**Masking in the other direction, caught by a failure.** The first run after RC-6
landed was 1425/6. All six were existing controls that inject `coverage='complete'` onto
an entry the producer had built as an honest `unknown`; RC-6 refused them at the
producer boundary, one layer before the capability/dialect guards they exist to
exercise. That is a real boundary move that would have **masked** those guards. It was
resolved without changing a single assertion token: a shared helper makes the injected
lie internally coherent (it now also asserts `examinedExhaustive=true`), which is a
strictly more adversarial provider and leaves the guard under test as the only thing
that can refuse it.

---

## What was executed

Nine checks, all passing. The six with no pin gate ran in `work`; the three pin-gated
ones ran in a **disposable repinned copy outside `work`** — no pin in `work` was edited
and **no pin match is claimed**.

| check | before | after |
|---|---|---|
| `foundation/check-identity.py` | 1431 / 0 | **1530 / 0** (+99) |
| `check-integration.py` | 412 / 0 | 412 / 0 |
| `foundation/check-foundation.py` | 231 / 231 | 231 / 231 |
| `foundation/check-array-orders.py` | 65 / 65 | 65 / 65 |
| `foundation/check-product-configuration.py` | 28 / 0 | 28 / 0 |
| `foundation/check-product-quality.py` | 24 / 0 | 24 / 0 |
| `native/check_native_evidence.v2.py` † | 355 / 355 | **375 / 375** (+20 cases) |
| `security/check-security-lifecycle.v1.py` † | 456 / 456 | 456 / 456 |
| `workflows/run-reference-checks.py` † | 1795 / 0 | **1803 / 0** (+8) |

† run in the disposable repinned copy.

**Failures encountered are preserved in `handoff.json`, not smoothed over.** Besides the
six-control boundary move above: I ran the native checker inside `work` after the
sources had changed — it failed the pin gate as expected, but had **already rewritten**
`native-evidence-report.v2.json`, a generated report I was told not to edit. I caught it
by re-verifying every path against the manifest, restored it byte-for-byte from the
snapshot (`5f31c119…` confirmed), and moved every pin-gated run to the disposable copy.
Three new controls asserted wrong literals and failed honestly (jsonschema's actual
`uniqueItems` text; `CONFIG.INVALID` reaching `StepTermination` through a `$ref` rather
than literally) — the last was replaced by a *stronger* control that validates the real
carrier and proves the validator is not vacuous. One near-neighbour used an unregistered
language mode; one release-declaration fixture violated the strict-unique order law.

**`native-cases.v2.json` is proven purely additive:** removing the 20 `cb8-*` cases and
the three `feedbackMap` rows and re-serialising reproduces `07d990e2…` byte for byte.

---

## What root must decide

1. **`V20-ROOT-1`** — five pin ledgers now disagree with the changed sources by
   construction. No pin edited, no pin match claimed.
2. **`V20-ROOT-2`** — the two generated canonical reports are delivered at accepted19
   bytes and are now stale (375 native cases, 1803 workflow checks). Root regenerates.
3. **`V20-ROOT-3` — an independent contradiction I found and deliberately did *not*
   correct.** Exactly two of the 36 DomainDetail codes emitted by
   `workflows_model.v1.py` — `BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER` and
   `BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH` — are in **neither** the closed
   `DomainDetailCode` enum, the public detail registry records, nor `internalAliases`,
   and the real public carrier **refuses both** (measured). Both are emitted by
   `verify_scope_parameter_binding`, the very function CB-GAP-1 touches. I left them
   alone because changing the code of an existing reachable refusal changes accepted
   behaviour outside the corrected input, and that is root's call. It is precisely why
   the new ambiguity refusal reuses `CONFIG.INVALID`.
4. **`V20-ROOT-4`** — `DUPLICATE_REQUESTED_CAPABILITY` has no route-registry row, so no
   public termination can be derived for it. Pre-existing; now exercised by a control.
5. **`V20-ROOT-5`** — `PUBLIC_ROUTE_REMEDIES` is keyed by public code, so any new key
   reusing a code inherits its remedy. Widened two strings; the structural fix is a
   separate decision.

**On the separate root finding.** I changed no accepted contract to bless the blind
reconstruction's own-code mistakes (the jsconfig flag, the literal false/pass proofs with
no matching Coverage), and I found no independent contradiction in the published §4
answers to them. The one contradiction I did find is `V20-ROOT-3`, which is unrelated to
that exercise.

## Source versions

No version was changed. Every edit is an added law, an added guard, an added control or
a corrected sentence inside the current `v1`/`v2` documents, so no digest recipe, record
shape, enum, bound, order law or parameter payload encoding moved. The only identity
consequence is the unavoidable one: `native-evidence.schemas.v2.json` changed, and its
raw digest is `coverage2.payloadSchemaDigest`, so `coverage2` identities move — which is
why the CB-GAP-3 frozen-graph replay is reported the way it is above.
