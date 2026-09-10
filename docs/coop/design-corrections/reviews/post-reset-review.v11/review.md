# Fresh independent design/reference review — frozen candidate v11

**Verdict: CHANGES_REQUIRED** — one unresolved MUST (`v11-M1`), one unresolved SHOULD (`v11-S1`),
three non-blocking advisories (`v11-A1`, `v11-A2`, `v11-A3`).

**Subject** `subject.manifestSha256 = a03b7fe987ee886101a6d5b85bf4b0760f59b06a5a9e9c5f627accb9a7263bdf`,
2,786 files, 70,148,210 bytes, snapshot `/tmp/opensip-design-corrections/candidate-subject.v11`.

**Reviewer** actual Claude, fresh independent session. I authored none of these bytes. I am neither
coauthor `5dec928a-6357-4726-9ea8-49a3079fb726` nor prior reviewer
`4628c693-7a5e-4567-a1c8-e2f7ae322651`. No subagents were used. Every write I made is confined to
`/tmp/opensip-design-corrections/post-reset-review.v11`, including all disposable copies and probes.
I made no source edit, no commit, no push and no reset or clean.

This is **independent design and reference acceptance only**. It is not reconstructability, not
readiness, not application acceptance, and not product qualification.

---

## 1. Why the verdict is CHANGES_REQUIRED, and what it is not

The primary delta is sound. The `v10-S1` same-path aggregation defect is genuinely closed, and closed
in the right way. I reproduced both original order arrangements, confirmed the intended refusal cause,
and — more importantly — confirmed that the twelve new checks are **discriminating** rather than merely
numerous: seven of them fail when run against the pre-fix model.

The verdict turns on something else entirely. **The frozen candidate cannot reproduce its own declared
reference evidence.** Two of the six declared commands exit 1 on the frozen bytes, because the last
recording step rewrote a file that two pin ledgers still pin at its previous digest. That is a
reproducibility defect in the evidence pipeline, not a defect in the corrected law — but a candidate
offered for independent acceptance has to reproduce its own claims from its own bytes.

Under the strict gate, any unresolved MUST or SHOULD is CHANGES_REQUIRED, and ACCEPT is never granted
with a non-blocking SHOULD outstanding. Both top-level arrays are non-empty, so ACCEPT is unavailable.

---

## 2. Custody, verified before and after

| | before | after |
|---|---|---|
| declared files verified | 2786 / 2786 | 2786 / 2786 |
| digest mismatches | 0 | 0 |
| length mismatches | 0 | 0 |
| missing files | 0 | 0 |
| **undeclared files** | 0 | 0 |
| symlinks | 0 | 0 |
| total bytes | 70,148,210 ✓ | 70,148,210 ✓ |

Byte-identical before and after all probe work. Manifest SHA matches the declared value; the declared
predecessor matches frozen v10 `82c1be11…`; the prior review JSON hashes to the declared
`64e15aff…`. The original repository is unmodified — I re-hashed the five report files the six
commands would have written and all are unchanged.

All 184 prior-review artifacts are preserved **verbatim** against the repository, including
`p05_enforcement_absent.py`, the `instr/` harness-instrumentation directory, `tamper/`, and the failed
initial attempts. Prior enforcement-removal and instrumentation evidence retains its actual scope.

---

## 3. The exact delta, treated as assertions to test

16 changed, 284 added, **0 removed**, 2486 unchanged.

The 284 added files are review and custody artifacts only. Of the 16 changed, nine have a **+0 byte
delta** — same length, different content — which I confirmed are pure hex-digest pin updates. The
substantive changes are four files:

| file | delta | what it is |
|---|---|---|
| `foundation/identity-model.py` | +1289 | the monotonic `missing` fact |
| `foundation/check-identity.py` | +6246 | 12 new annotation checks |
| `foundation/identity-report.json` | +1328 | 12 added, **0 removed, 0 changed results** |
| `contracts/product-v1/identity-and-evidence.md` | +2826 | the assessed normative insert |

**Exactly one normative file changed** — the contract insertion. **Zero registered schema or registry
bytes changed**, so registered identity preimages are preserved; the registered relation document is
canonically byte-identical across the delta.

---

## 4. The primary delta: the same-path aggregation defect

### What was wrong

v10's `record()` read:

```python
annotations = previous['annotations'] + [a for a in annotations if a not in previous['annotations']]
if not previous['annotations'] or not annotations: annotations = []
```

`annotations` is rebound to the merged list on the first line **before** it is tested on the second, so
`not annotations` could only be true when both sides were empty. The rule collapsed to "poison iff the
*first-recorded* sighting was unannotated" — a visit-order dependence, and the exact opposite of what
the docstring above it claimed.

### What v11 does

`missing = not annotations` is computed from the **incoming** annotations before any rebinding, then
merged monotonically with `missing = previous['missing'] or missing`. The merged annotation list is
kept as a separate fact, so "no new annotation" stays distinguishable from "already merged" and a
conflict remains diagnosable. Every consumer — the coverage counts, the `byRelation` account, and the
law's `uncovered` set — now reads the monotonic fact.

Order independence now follows from `or` being commutative and idempotent, rather than from careful
sequencing. That is the durable form of the fix.

### What I verified independently

I built my probes from the law text, not from the candidate's helpers. Both columns below are my own
measurements:

| case | v11 | v10 (pre-fix) |
|---|---|---|
| container, unannotated-first | REFUSE | REFUSE |
| **container, annotated-first** | **REFUSE** | **ADMIT ← the defect** |
| keyorder, unannotated-first | REFUSE | REFUSE |
| **keyorder, annotated-first** | **REFUSE** | **ADMIT ← the defect** |
| third sighting, missing at 0 | REFUSE | REFUSE |
| **third sighting, missing at 1** | **REFUSE** | **ADMIT** |
| **third sighting, missing at 2** | **REFUSE** | **ADMIT** |
| three sightings all annotated (control) | ADMIT | ADMIT |
| registered document (control) | ADMIT | ADMIT |

Every refusal carries the intended cause `RELATION_DIGEST_UNANNOTATED` at the expected path. I also ran
12 randomised whole-document key permutations across all 13 relations: verdicts invariant.

### Discrimination, not counts

Counts and source greps prove nothing, so I ran three arms:

| arm | result |
|---|---|
| v11 checker + v11 model | 673/673 pass |
| **v11 checker + v10 model** | **7 of the 12 new checks FAIL** |
| v10 checker + v10 model | 661/661 pass — v10's own suite could not see the defect |

No pre-existing check fails under the pre-fix model, so the seven failures are attributable to the new
law alone.

The five new checks that do *not* discriminate are exactly the intended controls, and must pass in both
arms by construction: the missing-at-0 case and the two unannotated-first cases are the arrangements
v10 already refused; the three-all-annotated case is the positive control; and the canonical-equality
case is a property of the fixtures, not the model. Their passing in both arms is correct design, not
weak testing.

### v10-A3 closed on its own terms

v10-A3 measured that the merge branch executed **zero** times across all 661 checks. I re-measured with
a counter injected into a disposable copy (frozen source untouched; suite results unchanged, which is
the lawfulness guard):

- v10: merge branch executed **0** times across 661 checks — v10-A3 reproduced exactly.
- v11: merge branch executed **16** times across 1,355 `record()` calls, suite still 673/673.

Reachability is now accompanied by discrimination, which is strictly stronger than what A3 asked for.

### Preserved corpus

I reproduced the injection corpus independently rather than trusting the suite: **39 injections**
(13 relations × 3 governed forms) all refuse with the intended cause, and all 39 positive controls
admit. All **8 traversal shapes** (ref, inline, nullable, aliased, nested, array, container-ref,
cyclic-container-ref) refuse when unannotated and admit when annotated. The removal corpus holds: 7
governed fields refuse with their per-field cause, while `file.byteLength` — annotated but **not
governed**, since it refs `UInt64` — correctly **admits**. That distinction between removing a
non-governed annotation and removing a governed digest/path annotation is preserved exactly.
`vcs-change.previousPath` retains its `not-joined` exemption with its explanation under the existing
`join` key.

I also probed a risk the parameterised-document API introduces: whether a hypothetical document can
contaminate the registered-law memo. It cannot — hypothetical calls never write the memo, and
registered verdicts are unaffected in both orders.

---

## 5. The normative prose

40 lines, 4 paragraphs, 2,825 bytes, **0 lines removed**. I checked every claim against the
implementation rather than against the narrative:

Governed-occurrence definition, traversal surface, annotation inheritance, **terminal scalar
exclusion** (annotating `$defs/DigestHex` does *not* exempt an unannotated field of that form),
intermediate-alias coverage, branch/occurrence isolation, monotonic missingness, order independence,
conflict refusal, retention vocabulary, one effective-annotation account across all limbs, and
top-level join addressing — all verified against behaviour.

Two details matter and are stated correctly:

- **Direct non-governed annotations refer explicitly to top-level selector properties.** Verified: a
  top-level annotated `UInt64` with `retention: preimage` and no join refuses with
  `RELATION_DIGEST_LAW_RESIDUE`; the same annotation nested produces **no sighting at all** and admits.
  The unqualified phrase would have overstated the reference.
- **Exemption reasons remain an authoring disclosure obligation.** Verified: a nested `not-joined`
  occurrence admits with a reason, without a reason, and with an empty reason. Admission validates the
  declared retention, not the presence or content of the prose, and **no new `reason` key is invented**.

The six named refusal conditions map one-to-one onto the six implemented causes, all of which I reached
independently. No arbitrary future schema feature is added.

**Blind-input completeness.** A blind implementer can build the law from this prose plus the existing
canonical section without reading the author Python. "Typed canonical equality" is grounded by §3's
existing statement that booleans are distinct from integers. The `items`/`additionalProperties`
collapse to one location is not spelled out, but I verified it cannot change any verdict — an
unannotated governed occurrence refuses either way, so only the diagnostic path text would differ. The
one genuine omission is cycle termination (`v11-A3`), which also cannot change a verdict.

### Insertion custody

The inserted bytes are **verbatim** `CODEX-AGREED-NORMATIVE-INSERT.md` (sha `32db3495…`), and differ
from Codex's original proposal in exactly the two places the assessment asked for. The assessment
document records reading the 3,908-byte proposal at `a3705e7e…`, proposing the reason-clause
replacement, and then — in a final section — reading the **exact final 2,825 bytes in full** and
confirming both changes against the reference.

So actual Claude did assess the exact inserted bytes. **No agreement about an unread version is
inferred anywhere in this chain.** I re-hashed every digest the assessment cites; all match. I also
re-measured both of its load-bearing empirical claims rather than taking them at face value; both hold,
and my control confirms the admissions are caused by the `not-joined` declaration rather than by nesting.

Root applied only the released delta: for both source files the before-digest equals frozen v10, and
the applied v11 file equals the coauthor's retained author-source **byte for byte**. The insert's
before/after images equal the frozen v10/v11 contract documents.

---

## 6. Finding v11-M1 (MUST) — the candidate cannot reproduce its own six commands

`correction-crosswalk.proposed.json` in frozen v11 hashes to `ae78c7e6…`. Both
`security/source-pins.v1.json` and `workflows/source-pins.v1.json` pin it at `9560a51e…` — **exactly
its frozen v10 digest**.

Re-executing the six declared commands in a disposable full-subject copy:

| command | exit | report |
|---|---|---|
| foundation | 0 | byte-identical |
| **security** | **1** | `sourcePinsValid: false`, `checksExecuted: false` |
| native | 0 | — |
| **workflows** | **1** | `sourcePinsValid: false`, `checksExecuted: false` |
| workflow-surface | 0 | byte-identical |
| integration | 0 | byte-identical |

Both failures refuse *before running a single check*.

**Root cause — an ordering defect, not a typo.** `finish-v11-records.py` runs after
`run-final-v11.py` (step 1) and after `refresh-pins-v6.py` (step 3) in its own declared sequence, and
at lines 13–15 it **rewrites** `correction-crosswalk.proposed.json` to append `historicalReviews` and
reset `latestCompletedReview` on every row. Nothing re-refreshes the pins or re-runs the commands after
that final mutation. The guard at line 5, `assert report['passed']`, reads the `reference-checks.json`
recorded **before** the mutation it is about to make — a self-satisfying guard that can never catch
this. The pipeline has no post-mutation fixpoint.

**Why it matters.** `README.md`, `NEXT-REVIEW.md`, `validation-summary.v1.json`,
`reference-checks.json` (`"passed": true`, `exitCode 0` for both) and `technical-review.v11.md` ("All
four consuming pin sets are refreshed against their current inputs"; "The six final executed commands
pass") all assert six passing commands. On the frozen bytes that is false for two of them.

**Bounded scope.** I audited all **1,308 pins** across the four ledgers independently: exactly **2
stale, 0 missing**, both the same file, both equal to the v10 value. Neutralising only those two hex
strings in a separate disposable copy makes all six pass and reproduces every declared count exactly —
foundation 1021 = 231+673+24+28+65 over 1099 pins, security 456 cases + 10 sweeps, native 151 / 60
cells / 0 qualified, workflows 1290, integration 363. So the underlying evidence is sound; this is
bookkeeping. The declared pin counts 1099/73/71/65 are correct — it is the *content* of two pins that
is not.

I propose no patch text and made no source edit. The direction: refresh pins and re-run the six
commands **after** the final record-writing mutation, and replace the self-satisfying assert with one
that binds to the post-mutation tree.

---

## 7. Finding v11-S1 (SHOULD) — stale pending-review label

`validation-summary.v1.json` still records `"claudeFinalReview": "PENDING-FROZEN-V10"` inside the
frozen **v11** candidate. The convention is `PENDING-FROZEN-<current frozen version>` (v7→V7, v9→V9,
v10→V10). In the same edit, the sibling `claudePriorReview` *was* correctly advanced to the v10 review
and `priorReviewLimitation` *was* rewritten to the v10 outcome — only this field was left behind.

A downstream consumer would conclude the outstanding independent review is against manifest
`82c1be11` rather than `a03b7fe9`. The same slip occurred once before (frozen v8 carried
`PENDING-FROZEN-V7`), so it is recurring rather than a one-off, and it shares v11-M1's root cause:
post-hoc edits without re-reconciliation.

---

## 8. Non-blocking advisories

**v11-A1 — the two annotation-dedup sites use different equality notions.** This delta correctly
upgraded `record()`'s merge to `C.equal_typed`, and the new prose promises that only annotations "equal
under typed canonical equality" fail to conflict. But `walk()` still filters the `$ref`-chain
contribution with Python `not in` (i.e. `==`). Since `1 == True` in Python while `equal_typed` correctly
reports them distinct, a typed-distinct annotation can be dropped before `record()` sees it. Measured:
two annotations differing only by `ordinal: 1` vs `ordinal: true` are canonically distinct documents,
yet both placements ADMIT instead of raising `RELATION_DIGEST_ANNOTATION_CONFLICT`.

Non-blocking on three independent bounds: it is **unreachable** in the registered documents (every
annotation value there is a string or nested object — no numeric or boolean scalar exists); it does
**not** affect the order-independence property under repair (both placements give the same verdict, so
only the retained annotation differs); and reaching it requires a future schema edit introducing a
numeric- or boolean-valued annotation key, which is beyond declared support and is not something this
review demands. Worth aligning when the traversal is next edited.

**v11-A2 — reported check count includes duplicate ids.** 673 reported, 663 distinct: `closed-closure`
and `exact-version-closure` each appear 6 times from parameterised loops. Identical in frozen v10
(661/651), so this delta neither introduced nor worsened it, and all instances of each id agree so no
failure is masked. Noted because it sits directly in the spirit of the project's own standing caution
that check-count growth is not coverage growth.

**v11-A3 — prose does not state cycle termination.** The insert says to follow local references but
does not mention terminating on a cyclic `$defs` reference. The implementation has a chain guard and
the suite exercises a self-referential container, which I reproduced. No admission outcome depends on
it — any terminating guard reaches the same verdict — so this is a robustness note, not a semantic gap.

---

## 9. Preservation of previously confirmed behaviour

`identity-report.json`: 12 added, **0 removed, 0 changed results**; limits and standing unchanged. A
purely additive delta — no previously passing check was removed, weakened or flipped, so no prior
enforcement was withdrawn.

**Identity stability.** Rather than synthesise values, I harvested every identity the complete suite
actually computes, under both models, via a logging wrapper in a disposable copy: **18,431 identities
across 17 domains, 5,370 distinct — set-identical, with identical per-domain counts and identical set
SHA.** Zero identity drift across Run, plan, closure, snapshot, view, coverage, fact, subject-scope,
execution-plan, proof-bundle, semantic-evidence, evaluation-seal, finding, finding-fingerprint, import,
cache-key and regeneration-key.

The registered relation document is canonically byte-identical: 8 literal annotation injections, 7
governed sightings, 7 annotated, 0 unannotated, none missing, across clones / file / package /
vcs-change. All 13 selectors admit at base and under 12 key permutations.

The earlier Codex counterexamples are retained and re-run at v11 — traversal (4 cases), alias (3
cases), inherited limbs (9 cases: field / alias / branch × preimage / invented-retention / not-joined).
I independently reproduced equivalents of each, and confirmed all three law limbs read the same
effective annotations, with invalid retention refusing.

**What I did not re-derive.** The long list of previously confirmed behaviours — owning-snapshot joins
and memo owner context, `file@enumerated` Coverage, the 13 registered full-schema-document relations
and typed arrays, CVE1's four gates, native Coverage producer admission, Plan enumerator membership,
complete TypeScript+Rust Run closure, the TS config/layout/extends family, raw32 compiler/dialect clone
body version, JS body language via the TS engine, L0 recomputation vs L1–L3 custody, the Rust
target/edition/marker/bounds family, stable body IDs under unrelated ownership, partial vs complete
empty clone Coverage, cache lookup vs validated hit, mutation vs repair replay, public purge
disclosure, required-output failure and committed Run preservation, and complete leased pin ledger
comparison vs pure projection — was **not** individually re-derived. Preservation rests on the
exact-diff basis: 0 changed results across the 661 shared checks, 0 removed checks, set-identical
identities, and a delta touching only the schema-law functions plus additive prose.

---

## 10. Registers

- **16 AR rows** individually disposed. ACCEPT for the foundation, native and integration units whose
  reference commands pass and whose reports reproduce byte-identically. **CHANGES_REQUIRED for the
  nine security and workflows rows** (AR-03/04/05/06/14, AR-08/10/11/16) whose declared evidence cannot
  be regenerated from the frozen bytes — linked to v11-M1, with no substantive defect asserted in the
  obligations themselves. AR-15 is ACCEPT_SCOPED to routing only.
- **15 FW rows** ACCEPT_SCOPED. `current-source-map.proposed.md` is byte-identical across the delta, so
  no FW statement changed; the one normative change is additive prose adding no forward capability. No
  FW obligation is demonstrated or closed.
- **27 inherited residuals** (DR-001…011 and DR-011-R01…R16) individually keyed, all ACCEPT, all
  unchanged by this delta, no SATISFIED grade granted. (`DR-012` appears in prose but is the
  release-qualification row routed to the DR-G gates, not an inherited residual — my initial regex
  over-captured it.)
- **DR-201…205** ACCEPT_SCOPED, each independently confirmed as an `ownerRows` entry of AR-15, whose
  status is `PROPOSED-SOURCE-MAP-PENDING-REVIEW-AND-APPLICATION`. Routing only; no historical
  acceptance re-opened or graded.
- **32 qualification gates** DR-G01…DR-G32: all `demonstrated: false`, `qualified: false`,
  `implementationHarnessAuthored: false` over the four platform families. This review demonstrates and
  grants none.
- **30 evaluation subresiduals** unchanged and individually dispositioned; not closed here.
- **28 carried v5–v10 advisories** all present with original severities and explicitly preserved. None
  discharged. The three new advisories are additional and also undischarged.
- **31 protected historical files** verified unchanged.

---

## 11. Harness errors I made, corrected honestly

These are my mistakes, not subject defects, and none is counted as one:

1. **p08** — my "nullable oneOf single-branch" case used a `{"type": "null"}` sibling. A null branch is
   not a governed form, so it is never a sighting and ADMIT was the *correct* verdict; my probe tested
   nothing. Re-tested in p09 with both branches governed, in both orders — branch isolation holds.
2. **p17** — I passed synthetic values to `identifier()`, which rejected them: the model validates each
   domain payload against its schema before hashing. Replaced with p17b (real identity harvest). The
   rejection was the model behaving correctly.
3. **p12** — whole-suite `sys.settrace` reachability exceeded 600s; I terminated it with `pkill` and it
   exited 144 with no result. Superseded by p12b. The abandoned attempt is retained.
4. **p16** — my regex captured `DR-012` from a prose sentence, suggesting 28 inherited rows. The
   register is 27, as declared.

---

## 12. Limitations and claims explicitly not made

Independent design/reference acceptance only — **not** reconstructability, readiness, application or
product qualification. No implementation, commit, push, source edit, reset or clean. Reports were
regenerated only in disposable copies, never in the frozen subject and never in the original
repository, which I re-verified as unmodified. All native, OS, compiler, crypto and storage
observations remain synthetic TCB assumptions; nothing was measured on real toolchains and no platform
is qualified. The integration fixture's synthetic shared construction is **not** an independent oracle;
I verified only its declared provenance. No Codex assent, no blind pass and no application review is
performed or implied. No self-hash review cycle is invented — a review cannot be embedded in its own
frozen subject. Root's prospective application tooling is outside this frozen design and was not
assessed. No historical preview grade is extended.

## 13. Required next acts

1. Correct **v11-M1**: refresh the pin ledgers and re-run the six commands *after* the final
   record-writing mutation, with a guard that binds to the post-mutation tree.
2. Correct **v11-S1**: advance `claudeFinalReview` with its siblings.
3. Re-freeze as a successor and obtain a fresh independent review at zero unresolved MUST/SHOULD.
4. Then actual Codex assent to those exact bytes with all carried plus new advisories.
5. Then a **new** fresh blind consumer pass on the accepted normative bytes.
6. Then a complete, independently reviewed application and readiness reconciliation.

---

*Probes: `probes/p01`–`p19`. Results: `logs/`. Disposable copies: `copies/`. Builder:
`build_review.py`. Machine-readable verdict: `review.json`.*
