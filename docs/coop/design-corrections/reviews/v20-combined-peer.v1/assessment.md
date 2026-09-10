# V20 Combined Source — Final Composition Peer Assessment

**Standing.** Bounded ACTUAL-Claude coauthor alignment on the exact composed root/stage/advisory/main
delta. Not a full independent design audit, not acceptance, not freeze, not readiness. Source20
closure is **not** claimed.

**Verdict: technical assent for all ten final source hashes. Required changes: none.**

## What I actually read

Manifest `proposal.json` hashes to `272a2e131c0c2288e9452e76215dc5d95c88af16cf2be575f16c700a00fa8fb5`
— exact match. All ten `beforeSha256` values match frozen19 `candidate-subject.v19`, all ten
`afterSha256` match `work/`, and `root-identity.v2.json` matches `573f338b…`.

I read every byte of the added root delta: all six non-empty `.root.diff` files in full
(identity-schemas 13811 B, identity-and-evidence.md 7224 B, check-identity 7171 B,
native-evidence.schemas 3458 B, identity-model 2526 B, native-cases 777 B), plus the augmentation
record, `main-capture.json`, both root identity logs, and the schema/model sites the delta depends
on. I did **not** re-review main's v19→main delta or the wider design; that is the charter, and
Codex has already read main's changed bytes.

To prove I read *all* of the root delta, I replayed the decomposition: frozen19 → `patch(main.diff)`
→ `mainSha256` → `patch(root.diff)` → `afterSha256`, for every file. Every patch applied at rc=0 and
every intermediate and final hash matched byte-exactly; the four empty root diffs sit on files whose
bytes already equal `mainSha256`. The delta I read is provably the entire delta.

## Independent execution

In a disposable 619 MB copy — never the source — `check-identity.py` gives **1548 passed / 0
failed**, reproducing `root-identity.v2` exactly, with all 18 new `v20-*` controls present.
`check_workflows.v1.py` gives **1803/1803**. Both report `productQualification: false`.

Reproducing a passing run only shows the controls do not *fail*. To test whether they are
load-bearing I ran four targeted mutations, each reverted afterwards:

| Mutation | Result |
|---|---|
| M1 — neutralise the `registered-schema-document` guard | 3 fail: `v20-schema-view-unregistered`, `…schema-ref-unregistered`, `…view-unregistered-only` |
| M2 — inject a bogus member into `#/$defs/Domain` | 1 fail: `v20-domain-vocabularies-and-registry-agree` |
| M3 — revert `stage-spec.outputDomains` items to `$ref Text` | 1 fail: `v20-stage-domains-refuse-spec-only-invalid` |
| M4 — rename `artifactClass` at `view.schemaDigests` only | 2 fail; the `schema-ref` control still passes |

Each mutation is caught by exactly its intended control and nothing else. M1 shows the guard bites at
both annotated sites while leaving the missing/registered-extra controls untouched — confirming the
retention-first ordering, since `blob(value)` precedes the membership test. M4 shows the two sites
are independently guarded. Afterwards, all ten source paths and all ten disposable paths re-hash to
`afterSha256`: I edited no source, live or history file.

## Substantive judgement on root's three corrections

**The stage peer's OPTIONAL paragraph was wrong, and root's fix was necessary.** `stage-spec`
requires `[schemaVersion, planId, producerClosure, operation, parameters, outputDomains,
outputSchemaDigest]`; the peer's "operation/parameters/outputSchemaDigest/producerClosure are the
WHOLE hash inputs" omits `planId`, `outputDomains` and `schemaVersion`. `cache-key` further requires
`stageSpecDigest`, `scopeIds` and `inputRefs`, and `regeneration-key` is `$ref cache-key` — matching
"share one schema and differ only by H domain". Root's replacement — the complete stage spec
including Plan and output domains determines `stageSpecDigest`, keys commit that digest alongside
their other declared inputs, and there is no uncommitted operation discriminator — is exactly right.
The collateral claim that `program-predicate.operation` is a closed seven is literally true. Crucially,
`stage-spec.operation` remains `$ref Text` with **no** enum: the new `x-opensip-vocabulary` block is
annotation only, so no global stage enum was introduced, as required.

**Main's "NOT schema-decidable" clause really was false.** Under draft 2020-12 a conditional
`if`/`then` at the containing object can express `coverage=complete → examinedExhaustive=true`. Root
changed only that clause, to "enforced by the cross-property admission check rather than encoded in
this shape schema" — accurate, and precise about *where* it is enforced without overclaiming. The
RC-6 implication, the unknown-direction prose, the totality claim and both enforcement boundaries are
byte-identical. No RC6 semantics changed.

**Main's CB8 controls were tautological and vacuous, and root's fix is real.** Beyond removing
`or True`, the important repair is the precedence input. `_CAP_A` and `_CAP_B` share the tuple
`(inventory, ts-tsconfig, .)` and differ only in `required`. Probing the real model: `[A,B]` alone
refuses with `native.requested-capability-duplicate-ownership-tuple:…`, so the tuple rule is a live
competing refusal — but the *old* input `[made-up, B]` contained no duplicate tuple at all, so its
"unregistered outranks the tuple rule" assertion proved nothing. Root's `[made-up, A, B]` contains
both and still yields the unregistered refusal, which genuinely demonstrates precedence. The same
third row was mirrored into the native fixture, keeping code and corpus in step.

Two further verifications matter. The `closureMembership` annotation is descriptive, not
aspirational: there are exactly six `semanticClosures` membership sites in `close_run` and they map
one-to-one onto the six `direct` entries (`UNSELECTED_EVALUATOR`, `STAGE_SPEC_UNSELECTED_PRODUCER`,
`FINDING_RULE_CLOSURE_UNSELECTED`, `UNSELECTED_PRODUCER`, `UNSELECTED_ENUMERATOR`,
`CACHE_UNSELECTED_PRODUCER`), with both `equalToDirect` entries backed by `FACT_SOURCE_PRODUCER_JOIN`
and `EVALUATOR_JOIN`. And the published `importIds` prose matches the model exactly, including its
least obvious claim: `HIDDEN_FINDING_EVIDENCE` builds its import roots from the *evaluated* set, not
from `plan.importIds`, so "selection alone lets no finding cite it" is literally what the code does.

Root's construction-outside-the-catch discipline is not cosmetic. `root-identity.v1.log` records the
exact `ValidationError` raised during *construction*; inside a refusal catch it would have let a
builder crash masquerade as an intended Run refusal.

## Non-blocking observations

`ProofInputRef.domain` (12) and `FindingEvidenceRef.domain` (5) are correct proper subsets of
`byDomain` but have no durable guard; root's new work makes `ProofInputRef`'s `schema` member
load-bearing. The gap predates the delta, so it is not a required change — I refer it to the fresh
review rather than bolting it onto this composition. Separately, `Domain` duplicates the `Ref.domain`
list rather than `Ref.domain` becoming a `$ref`; normally drift-prone, but M2 shows drift fails the
run, and the choice keeps the published `Ref` shape byte-stable. Acceptable as composed; recorded so
the fresh review inherits it deliberately.

## Limitations

`check_native_evidence.v2.py` **exits 2 and runs no case**: all ten source pins still carry the
frozen19 before-hashes. My assent for `native-cases.v2.json` and `native-evidence.schemas.v2.json`
therefore rests on hash verification, full reading of the delta, and digest arithmetic — the fixture's
new `b1fff36d…` is the exact SHA-256 of the final schemas document, correctly pinning root's
post-RC6 bytes rather than main's intermediate, and the old `5665e5dd…` matched none of the three
revisions — **not** on native-checker execution. The manifest declares pins and the full six checks
as pending, so this is disclosed, but it must be discharged before acceptance.

These are reference check calls over a design model: closure, schema, identity and vocabulary
agreement — not semantic proof replay, not compiler qualification, not product qualification.

**V20-ROOT3 and V20-ROOT4 remain REQUIRED and PENDING** with the separate route coauthor PID31260. I
did not duplicate or pre-empt that active work, and my assent is deliberately confined to the current
exact root stage/schema/publication delta so a later separately authored route overlay composes on
top transparently. Consequently I do not claim complete source20 closure, and I claim neither the
fresh full independent review nor the new blind9 — both follow this agreement.
