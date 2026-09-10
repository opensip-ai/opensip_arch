# v20 stage proposal — bounded actual-Claude peer assessment (v1)

**Standing.** Bounded peer assessment of one root source proposal. Not the full independent
acceptance review. No grade, no readiness judgement, no qualification, no implementation
authorization. Advisory to root.

## Custody

Both declared before-hashes match frozen19 exactly; both after-hashes match the proposal work
tree exactly; the work tree contains exactly the two declared files and nothing else.
`parentManifestSha256` is **unverified** — `candidate-subject.v19/` holds only `docs/`, and I
could not find the artifact that digest names. I flag it rather than assume it.

## Verdict

I agree with all four of root's choices as **design**. I withhold technical assent from the
proposal's exact schema bytes, because the change as written **crashes core admission**.

## RC-1 — blocking

Both `outputDomains.items` now carry `"$ref": "#/$defs/Ref/properties/domain"`. This is the
**first deep JSON pointer in the document**. All 39 pre-existing `$ref`s are flat
`#/$defs/<Name>`, and three resolvers in the owning surroundings implement reference resolution
as `ref.split('/')[-1]` indexed into `$defs`:

| site | function | result on the proposal |
|---|---|---|
| identity-model.py:589 | `deref`, called by the admission `walk` at every node | `KeyError: 'domain'` |
| identity-model.py:605 | `carries_digest` | same shape |
| check-identity.py:887 | `sort_canonical_sets`, reached through `rekey` | `KeyError: 'domain'` |

That the flat shape is a *contract* and not an accident is visible one line above the break:
identity-model.py:588 refuses any non-`#/$defs/` reference with `EXTERNAL_SCHEMA_REF`. The
pointer passes that guard and then dies on the lookup.

I reproduced this by transcribing both functions verbatim into `probes.py` — the frozen
checkers were never executed — and driving them with the exact fixture record shapes from
`integration-fixtures.py:779-780`:

```
frozen19  walk(execution-plan)                    ok
proposal  walk(execution-plan)                    KeyError: 'domain'
proposal  walk(stage-spec)                        KeyError: 'domain'
proposal  walk(stage-spec, outputDomains=[])      ok
proposal  sort_canonical_sets(execution-plan)     KeyError: 'domain'
```

Two consequences worth naming. First, this is **not a refusal** — it is an uncaught `KeyError`
out of `payload()`, not an `AdmissionError`. Second, the *only* value that still admits is
`outputDomains: []`, because `walk` never descends into an empty list. Choice 3 survives by
accident. And in the identity suite the damage is two-sided: `check-identity.py:19` `rejects()`
catches `KeyError`, so `stage-spec-output-domains-must-join-the-stage` would report **PASS for
the wrong reason**, while `stage-spec-positive-run-closes` (line 1520, no `try`) aborts the run.

**Resolution A (recommended, supplied and verified).** Add a flat `$defs/Domain` holding the
same 32 members, placed with the other scalar forms between `ProjectId` and `Ref`, and point
both `items` at `#/$defs/Domain`. `Ref.properties.domain` **must keep its inline enum bytes** —
check-identity.py:1367 reads `SCHEMA['$defs']['Ref']['properties']['domain']['enum']` directly
and would `KeyError` on a `$ref` there, which is why the tidier "make Ref reference Domain"
version is wrong.

**Resolution B.** Give the three resolvers real JSON-pointer resolution. Systemically this is
the better fix — `split('/')[-1]` is a latent defect independent of this proposal — but it edits
identity-model.py and check-identity.py, i.e. three files and the checker owner's surface. Root's
call.

**Residual under A**, stated rather than papered over: the 32-member enum then exists literally
twice and nothing pins the copies equal. The one-line companion law
(`$defs/Domain.enum == Ref.domain.enum <= byDomain`) belongs beside check-identity.py:1367. It is
**not** in my overlay because that is a third file; I record it as a merge obligation.

## Choice 1 — outputDomains reuse the existing vocabulary

**Accept the design.** This is enforcement, not annotation, and that is what makes it a
completion rather than a referral. Measured with `Draft202012Validator`, the draft the document
declares:

| input | frozen19 | proposal | overlay |
|---|---|---|---|
| `['view']` | admitted | admitted | admitted |
| `['View']` | **admitted** | refused | refused |
| `['my-provider/output']` | **admitted** | refused | refused |
| `[]` | admitted | admitted | admitted |

The original blind control `G4-DOM-unregistered` — an unregistered spelling sealing a Run — is
now dead at both selectors.

Confirmations root asked for. **Typed boundary:** yes, live. stage-spec is a canonical-record
payload; identity-model.py:685 validates it under the Draft202012 validator inside `payload()`,
which :1404 calls for every stage. **Existing equality check:** unchanged —
identity-model.py:1407, `C.equal_typed`, `STAGE_SPEC_OUTPUT_DOMAIN_JOIN`, and I re-measured its
refusal. **No new producer or evidence permission:** zero code, zero new refusal names. Dropping
the original assessment's optional `STAGE_SPEC_OUTPUT_DOMAIN_UNREGISTERED` was right — it would
have been a weaker second guard on a condition the schema now decides first.

One honest note on the public surface: the refusal *class* is pre-existing, not new. frozen19
already refuses `operation=''` with the same `ValidationError`, and check-identity.py:19/29
already treat it as an admission outcome. What widens is the set of inputs reaching it. How that
projects publicly is governed by ownership, origin and event position, which I did not assess.

**Residual I decline to fix:** all 32 domains are now admissible, including `plan` and `run`;
nothing refuses `outputDomains: ['plan']`. That is not a regression (frozen19 admitted any text)
and narrowing it would need an owning law tying declared domains to produced records — new
design, not gap closure.

## Choice 2 — operation is provider-authored interface vocabulary

**Accept.** Ownership is now total: for every stage-spec the owner is the selected
`producerClosure`'s versioned semantic interface, with no residual branch. Removing the original
conditional was the right call — "where the protocol publishes…" made ownership contingent on a
publication event with no named owner, which is deferral wearing a decision's clothes. Host
respelling is closed by "the same selected producer interface and logical operation use the same
token bytes" plus the explicit exclusion of aliases, localized labels and physical-plan names.
Nothing is invented: no manifest member, no global registry, no platform enum; `$defs/closure` is
untouched; the annotation reuses the existing `x-opensip-vocabulary` pattern already on
`analysis-spec…languageMode`. No C2 vocabulary is imported — the one `c2-plan-stage-schema.v4.json`
mention is pre-existing at md:62.

**One concrete ambiguity remains, and it is closable in prose.** Distinctness is stated *across*
providers but not *within* one interface. The mechanism, from `$defs/cache-key`, which I read
directly: a cache or regeneration key is `{planId, producerClosure, stageSpecDigest, scopeIds,
inputRefs, outputSchemaDigest}`, and `stageSpecDigest` covers `operation` + `parameters` +
`outputSchemaDigest`. So respelling is safe by construction — it changes the digest and *splits*
the key, a miss, never a false reuse. The real hazard is the converse: one token standing for two
distinct logical operations of one interface, with the same parameters and output schema,
collapses two stages onto one key. RC-2 adds that in eight lines, with no new mechanism, and says
plainly that the host cannot check it.

RC-3 is smaller: md:1069 says `operation` "is one of the seven evaluator predicates", and 43 lines
later the new text says flatly "there is no platform-wide operation enum". Scoped by its opening
selector it is not wrong, but a new blind consumer reading forward meets an unqualified
contradiction of a sentence it just read.

I did **not** treat the original alias probes as evidence. Different stage-spec bytes minting
different RunIds is the identity function working, not proved nondeterminism.

## Choice 3 — empty outputDomains preserved

**Accept**, and this is an improvement on the original assessment, which left it "referred, not
decided" for want of text either way. Silence about a case the model *admits* is the gap. I
verified no existing obligation is contradicted: the only `outputDomains` law is the two-array
equality, and `[] == []` satisfies it; completeness, fact production, predicate value and
retention are each governed by their own records, none of which reads `outputDomains`. No
`minItems` was added and I do not propose one — `minItems: 1` would refuse a graph frozen19 seals,
a behaviour change smuggled in as documentation. No no-output-stage implementation is claimed.

## Choice 4 — publish closureMembership

**Accept.** Root's exact-15 assertion **verified by measurement**: `closureKinds.byField` has 15
keys; `direct` (6) + `equalToDirect` (2) + `selectedThroughOtherInput` (7) = 15, no duplicates,
set-equal. I re-verified every binding against the model rather than trusting the retained
matrix — all six direct codes (`UNSELECTED_ENUMERATOR` :1473, `UNSELECTED_PRODUCER` :1469,
`STAGE_SPEC_UNSELECTED_PRODUCER` :1406, `CACHE_UNSELECTED_PRODUCER` :1647,
`FINDING_RULE_CLOSURE_UNSELECTED` :1442, `UNSELECTED_EVALUATOR` :1297), both equality joins
(`FACT_SOURCE_PRODUCER_JOIN` :1508, `EVALUATOR_JOIN` :1288), the import selectors (:1290, :1428,
:1664) and the native path (`NATIVE_CONTEXT_SET_JOIN` :1311 plus the `closureJoins` traversal at
:1245-1252).

Three things it gets right that matter. Native and import closures are declared retained *through
other selected inputs* and explicitly need **not** be direct members — flattening them into
`semanticClosures` would have been a behaviour change dressed as documentation, and it is the part
the original blind claim had backwards. There is no exact-minimal-set rule, honouring the earlier
"do NOT add an exact-set or minimality constraint". And reachability is anchored to named Plan
selectors throughout, with "unreferenced CAS blobs are not evaluation inputs" stated in both files
— no all-store scan, no new traversal.

**RC-4 (accuracy).** The import strings invert the law. `evaluationInputRefs` membership is what
*defines* an evaluated import (identity-model.py:1427 derives the set from it), not an additional
obligation on it; the actual law at :1428 is the converse — such an import must be a
`plan.importIds` member, refusing `UNSELECTED_EVALUATION_IMPORT`. Corrected in the overlay.

## Qualifications on the retained assessment

**RunId.** No universal stability follows from editing raw schema-document bytes. For *this*
proposal nothing re-mints: identity-schemas.v2.json is the validator and registry
(identity-model.py:6) and is not among the six documents the payload registry digests. In general
root's warning holds — any document that *is* a registered artifact, including every registered
parameter and stage-output schema reached through `raw-artifact`, re-mints its digest on any byte
edit and re-mints every complete record selecting it, with no hash-recipe change. Recipe stability
is not identity stability.

**Public route.** The full-origin-independent framing was overbroad; ownership, origin and event
position still govern public failure. No new universal route is proposed here — zero code, zero
new refusal names, only wider inputs to a pre-existing schema-admission outcome.

**C2.** Historical status alone is not a current-authority grade, and the DO-NOT-SEAL note was a
reason not to *bind*, not a grade. Moot here: no C2 vocabulary is imported. Broad governance
grading stays with application review.

## Limits

Not an acceptance review. I did not run `close_run()` end-to-end — building the real graph needs
`integration-fixtures.py` and the wider tree, and executing it means running frozen-tree modules,
which the brief forbids; so RC-1 is proven at the function admission calls, with the call path
established by reading identity-model.py:685-692 and :1404 rather than by executing it. I consider
that decisive, but it is transcription plus reading, not an end-to-end run. I did not read all
108,707 bytes of the contract prose line-by-line (see `fullRead`). `parentManifestSha256` is
unverified. I did not inspect the other coauthors' work, so if any of them also edits
identity-schemas.v2.json the merge must be re-diffed and my overlay re-applied against the merged
bytes. RC-2's collision argument is structural; I did not construct a colliding graph. Every
changed byte still needs the full independent review and a new blind consumer, on the merged
source, after root decides RC-1.

## Bound hashes

| artifact | sha256 | assent |
|---|---|---|
| frozen19 identity-and-evidence.md | `3d7ca24e…f2735` | — |
| frozen19 identity-schemas.v2.json | `e58745a6…c86c0c` | — |
| proposal identity-and-evidence.md | `b604dd18…39b378` | **false** (dependent — names the selector that must change; substance sound) |
| proposal identity-schemas.v2.json | `88d87b5f…2b0aac3` | **false** (blocking — RC-1) |
| overlay identity-and-evidence.md | `ae47256e…44f8b9b` | **true** |
| overlay identity-schemas.v2.json | `c39e4e82…46a4c1aba7` | **true** |
