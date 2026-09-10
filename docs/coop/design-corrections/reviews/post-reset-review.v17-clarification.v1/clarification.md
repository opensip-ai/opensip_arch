# Clarification and correction of post-reset-review.v17

**Standing.** Additive report correction on the **same** frozen subject
`8cfe6d20a7d49b819f7c2eb2578afcaa5037048ed290ff1867fdcd6789cf3a9c`. It supersedes only
**reporting claims**. I edited no design or reference source, no prior review, no snapshot, no live
repo and no prior copy. No agents, no product implementation, no commits, no pushes.

**Original report, retained verbatim** at `reviews/post-reset-review.v17`:

| Artifact | SHA-256 | Bytes |
|---|---|---|
| `review.json` | `aa3cfd5e94ff29de9af45441b41ac746cad030cde8c1451341c7f7ec6956e4d8` | 75,877 |
| `review.md` | `1ec8a56fb7577cf866d6ae83083286439b5011b7707034ae583481503ff1c8c7` | 34,592 |

I re-hashed both in the repo copy: identical.

**Headline outcome.** Six of the eight points identify real errors in my reporting; I confirm all
six by independent measurement. One (point 7) is a genuine defect in reviewed reference source that
I had missed, and I raise it as **V17-ADV-3**. One (point 6) asks me to assess root's dispositions,
and I find both sufficient. **Source acceptance still holds**, on a corrected and materially
narrower evidential basis.

---

## 1. AR basis was factually wrong — confirmed, corrected

**Root is right, and my report contradicted itself.** My `arDispositions` basis asserted the
crosswalk was byte-identical to v16, while my own delta section listed
`correction-crosswalk.proposed.json` as changed (+10,464 bytes). Independently measured:

| | |
|---|---|
| v16 | `d2423ea249973bc6620b0624bd6b8043e090f46815aa32f21d665f310cb21438` |
| v17 | `9a52657622cdb0bf5268044635c94498af76fa9b0d456f5a8b7ae43407095aa3` |

I extracted the v16 file (verified against its manifest entry) and compared field by field. Root's
exact comparison reproduces: **16 items in both, identical ids, and every one of the 16 rows differs
in exactly two fields — `latestCompletedReview` and `historicalReviews`.** `rowsWithNoChange` is
empty. **Zero** substantive fields changed (obligation, selector, owner, unit, contract, evidence,
ownerRows, status).

**The distinction I failed to make:** the original *obligation and contract* are preserved; the
*review routing* moved. Those are different things. The corrected AR basis says so explicitly.

I also re-verified every other owner document against its **own** manifest entries rather than
against my earlier assertion:

| Document | v16 vs v17 |
|---|---|
| `architecture-depth-review/REVIEW.md` (AR owner) | **byte-identical** |
| `current-source-map.proposed.md` (FW owner) | **byte-identical** |
| `inherited-residuals.proposed.md` | **byte-identical** |
| `inherited-row-sources.proposed.json` | **byte-identical** |
| `evaluation-residual-dispositions.proposed.json` | **byte-identical** |
| `qualification-gates.proposed.json` | **byte-identical** |
| `08-decision-and-readiness-register.md` (owner rows) | **byte-identical** |
| `correction-crosswalk.proposed.json` | **CHANGED (routing fields only)** |

One further correction: `correction-crosswalk.proposed.md` is **not in the manifest at all**, so I
should never have implied a `.md` crosswalk was part of the reviewed set.

CARRIED-UNCHANGED stands for all 16 AR rows on the corrected basis. No grade is granted or inferred.
All four disposition families are re-issued as **ID-keyed objects** in the successor `review.json`,
retaining every original per-row field, with `appliedByThisReview=false` and
`finalApplicationOutcomeGranted=false` on every row.

## 2. "Zero structural pointers changed" was a narrow metric over-generalised — confirmed, corrected

**Root is right on both halves.**

**The metric.** p02 measured *leaf values at pointers present in both versions*, after stripping a
chosen prose key set; empty containers vanish under flattening. Restated honestly:

- intersection-leaf values changed: **0**
- structural pointers **removed**: **1**
- structural pointers **ADDED**: **321**

Additions **are** structural changes — a new presence conditional on `EvidenceRequirement`, two new
enum definitions, `coveragePartitionLaw`, and the new `x-opensip-*` law blocks. "Zero structural
schema change" was never what I measured, and I withdraw it. p08 is likewise a token/line
heuristic, not an AST or semantic proof; **the absence of a removed raise-line is not a proof** that
the refusal set is preserved.

**The admission claim was worse than imprecise — it was backwards.** I measured the field's actual
admitted domain by validating every candidate token against the v16 and v17 field schemas:

| | v16 (`$ref D9Deficiency`) | v17 (`oneOf` two planes) |
|---|---|---|
| tokens admitted | **10** | **16** |

- **11 newly admitted**, including all four the blind review named inexpressible
  (`derivation-policy-unmet`, `external-consumers-unknown`, `input-closure-incomplete`,
  `resolution-incomplete`) — each measurably **refused by the v16 field**.
- **5 no longer admitted**: `none`, `verdict-indeterminate`, `convergence-exhausted`,
  `baseline-recipe-unsupported`, `query-completeness-unmet` — whole-Run and comparison-step
  terminations that never belonged on a per-requirement field.

So the admitted value domain was **deliberately replaced**, in both directions. That replacement
*is* the CB6-MUST-1 correction. Calling it "no widening" or "additive strictness" misdescribes it,
and I withdraw both phrasings.

**Authority assessed separately, as root asks — and now measured, not inferred.** I byte-compared
the owning guard blocks v16 vs v17:

- the closed-world gate block (`if unsafe:` …): **byte-identical**
- the entire `repair_apply` body: **byte-identical** (`repairPlanId` ×14, `authorization` ×22 in both)

**Preservation of intended authority and change of the admitted domain are separate findings, and
both are true.** The successor report states them separately.

## 3. p03's scope was overstated — confirmed, corrected

Root's decomposition is exactly right; my own log confirms it:

| Group | Cases |
|---|---|
| 13 native relations × 9 native causes (ADMIT) | 117 |
| cross-plane, **first 4 native relations only** × 7 imported causes | 28 |
| 2 imported kinds × 7 imported causes (per-kind) | 14 |
| 2 imported × 9 native causes (cross-plane) | 18 |
| presence/typing law | 10 |
| carryability of a produced token | 4 |
| **total** | **191** |

A full cross-product would be **240**. Cross-plane negatives covered **4 of 13** native relations
(`calls`, `clones`, `control-flow`, `declares`). "Full cross-product" is withdrawn.

**Sufficiency inputs** were partial helper dicts — `view_entry` supplies
resolution/coverage/confidence/resolutionCompleteness/closedWorld only. They are **not**
schema-validated `ViewEntryV3` records and carry no full seven-member `ClosedWorldV2`.

**ROUNDTRIP** constructs from `pc.target` with the relation hard-coded to `references` for all four
— including `derivation-policy-unmet`, which was **produced from a `types` requirement**. It does
not forward the produced record. What it supports is **token preservation**: all four producers
independently did emit that same sole deficiency, and each token is carryable and admissible at both
boundaries. It is **not** an end-to-end native-to-authorized-repair proof.

**My cross-reference was wrong.** The `copiedBooleanAloneNote` pointed at p06 as the authorization
probe; p06 is the coverage-partition probe. **No executed authorization or target-projection control
was run in this review.** Every authorization statement I made is code and contract *inspection* —
now supplemented by the byte-identity measurement in §2, which is stronger evidence than the
inspection was, but still not an executed authorization control.

## 4. p04/p05/p06 qualifications — confirmed, corrected

- **p04** calls `typescript_config_graph_faults` with **filler content digests**
  (`sha256(path)`), never `admit_native_context`. **0 Runs constructed.** The two graph digests
  (`4ff62816…`, `0817c006…`) genuinely differ; the step to *two RunIds* is the **published derivation
  chain read from the law**, an identity-consequence inference, not two constructed Runs.
  `configOrigin=tsconfig` for a custom-named entry is **normative inspection**, not an output of
  those 13 controls.
- **p05** used the author's `M.mutation_replay_scope` / `M.mutation_replay_key`. I did **not**
  independently reimplement the H encoding. What stands: the preimage **field set** equals the
  published recipe, and the author's key function is deterministic and sensitive to operation and
  requestId. "The key I recomputed" is withdrawn.
- **p06 does execute 7 full Run controls** (5 positive closing with real `run2:` identities,
  2 typed refusals) — that claim stands. Qualifications I owed: the fixture is the author's own
  `check-identity build()`; the **different-relation branch never executed**
  (`otherRelationChosen: null`), so tuple-difference was exercised only by **rung**;
  totality-only-`file` is a **static registry read**; and with exactly one overlapping subject per
  control, the **UTF-8 byte-order tie-break is not discriminated**.

**"All corrected in the admission, not merely in prose" is withdrawn.** Classified honestly across
the 26 findings: **8** are enforced at an executable boundary, **5** publish law with partial
executable enforcement, and **13 are prose or evidence-record corrections** — and are correctly so.

## 5. Governance scanner scope and advisory lineage — confirmed, corrected

p10 scanned **10 records**, not the repository or the corpus. Its raw 522/22/304 figures are
scoped to those ten. Triage of the 304:

- **240** — my scanner mis-paired a review **path** with `subjectManifestSha256`, a *manifest*
  digest, not that file's digest.
- **18** — handoff before-version pins (`frozen16Sha256`, `finalV5Sha256`), self-labelling.
- **42** — 21 external live files named by the preservation report, each counted twice
  (`openingSha256` and `currentSha256`).
- **4** — advisory-account rows needing context; **only V14-ADV-2 lacks it**.

**Classifying a pin as as-of-then does not verify the old bytes** — it records only that it does not
match current bytes and sits under a historical key. Root independently verified all 31 live
protected files; that is root's verification, not mine, and I retain my stated limit (10 of 31 lie
inside the frozen slice; all 10 match). A phrase hit inside a preserved finding quotation is **not
live law**.

**Advisory lineage corrected — and I verified root's "52" rather than accepting it:**

- `advisory-application-account.v16.proposed.json` → **50** items (what I compared against)
- `design-assent.v16.json#/advisoryApplicationAccount` → **52** items — the *completed* v16 assent
- `review-assessment.v16.json#/newAdvisoryApplicationAccount` → 2 (`V16-ADV-1`, `V16-ADV-2`)
- `advisory-application-account.v17.proposed.json` → **55**

Added relative to the **completed v16 assent**: exactly **`CB6-ADV-1`, `CB6-ADV-2`, `CB6-ADV-3`**.
My "50 → 55, five added" measured against the *proposed* file and mislabelled it as the lineage.
Zero removed, zero severities changed — those stand.

**Qualification gates:** all **three** per-gate boolean flags are false on all 32 —
`demonstrated`, `qualified` **and `implementationHarnessAuthored`**. I named only the first two.

## 6. Root's proposed dispositions — assessed, both sufficient

**V17-ADV-1.** Root proposes retaining the accepted schema bytes and recording an application
disposition that consumers **enumerate admitted kinds from the imported relation registry and index
`perKindApplicability` by that validated key**; `rule` is documentation metadata, not a relation.

I tested it against the frozen bytes: the registry yields exactly `history-change` and
`runtime-observation`; both have well-typed 5-member rows; the map is **total** over the registry;
`rule` is **unreachable** under that rule. The disposition names the correct *derivation order* —
which is already what both model sites and the checker do — and removes the failure mode without
touching accepted bytes. **Sufficient at the original nonblocking severity.**

I'll add an independent reason to prefer it: editing that registered schema document would change
its committed digest and **move the retained-Run identities of every fixture committing it** — the
CB6-NEW-4 consequence. A silent patch would be worse than the defect. **No normative clarification
here requires a new subject:** no admission outcome changes, no identity moves, and no published law
is wrong — only an annotation is mistyped.

**V17-ADV-2.** Root will label item 44's `ef0c…` pin as historical as-of-v16 and bind current
`53380a24…` in the separately reviewed application/advisory record. I confirmed the target digest is
the current frozen digest of `relation-payload-schemas.v2.json`. This is precisely the remedy I
proposed and precisely the pattern item 43 already implements. Doing it in the application record
rather than by editing the account is **correct**, because the account is itself inside the frozen
subject. **Sufficient.**

## 7. The harness observation — confirmed, and I raise V17-ADV-3

**Root's observation is correct, and I missed it.** At `check_workflows.v1.py:1112`:

```python
except M.Refusal as r:
    check(cid, case['expect'].get('refusal') == r.detail, r.detail)
    ...
    continue
```

`Refusal.detail` defaults to `None`, and `.get('refusal')` is `None` for a case expecting success.
`None == None` passes, and `continue` then skips every later assertion for that case.

**Measured:**

- **83** Refusal raise sites in the model; **10** are detail-free.
- Critically, `refuse` is the **inner helper of `admit_evidence_requirement`** — so **every
  CB6-MUST-1 per-requirement refusal is detail-free**. `repair_preview` itself has one too. The
  masking surface sits directly on the finding this candidate exists to fix.
- Truth table: **exactly one row mis-passes** — expects success, refusal fires with `detail=None`.
  An expected-success case that refuses *with* a detail is correctly caught.
- **3** comparison sites: line 384 (import) **is** guarded by an `errorCode` conjunct; lines **1112
  and 1320 are unguarded**.

**Is it masking anything today? No — measured, not assumed.** I replicated the harness loop over all
37 repair cases: **0 of 25 positive cases raises at all.** The reported 1787 is not inflated.

**Mitigations that bound the severity:**

1. The three CB6-MUST-1 controls that *do* rely on the null comparison each additionally carry
   `expectRemedyContains` naming the exact decision key, so a *different* detail-free refusal fails
   their `.refusal-reason` check. The authors already mitigated the negative direction.
2. A masked positive would skip its downstream `check()` calls, **lowering `checkCount` below
   1787** and breaking the byte-identical report comparison the freeze discipline performs.
3. The pattern is known to the authors — line 384 is guarded.

**Severity: advisory (V17-ADV-3), not SHOULD.** On this chain's own scale, SHOULD has meant a real
underdetermination in *published law* (SHOULD-1, SHOULD-2). This is a latent robustness gap in the
evidence harness that changes no outcome today and is backstopped twice.

**I record the counter-argument explicitly so root can overrule me:** a control that can pass for
the wrong reason is not a valid control, and "it does not fire today" is exactly the contingency
argument I used to *raise* V17-ADV-2. I did not escalate because, unlike V14-ADV-2's pin, this one is
additionally backstopped by `expectRemedyContains` and by `checkCount` sensitivity — and because
inventing a blocking finding to appear rigorous would be its own failure of judgement. **No
unresolved MUST or SHOULD arises, so the verdict does not change.**

**I withdraw my "stricter harness" claim as stated.** It is true of the import site (line 384) and of
the added `expectRemedyContains` assertions; it is not a universal guarantee about the repair
harness.

*Suggested correction (no source fix made in this pass):* require opt-in before accepting a refusal —
`check(cid, 'refusal' in case['expect'] and case['expect']['refusal'] == r.detail, r.detail)` —
which preserves the three deliberate null-refusal cases while failing an unexpected detail-free
refusal on a positive.

## 8. Attribution and artifact scope — corrected

The 12 concurrent files were **root's work** (the advisory-record applier, the
monitor/reading-notes/prepared-assent recorders, and mutable NEXT updates). No frozen byte changed.
My conclusion happened to be right, but **file mtimes alone cannot attribute authorship** to or away
from any process, and I should not have used them as attribution evidence.

**Accurate scope:** review-authored artifacts are exactly the files I created under my own output
directories. Ordinary Claude runtime, session and shell metadata also exists outside those
directories and is not a review artifact.

**Failed-artifact preservation, stated accurately.** My original wording implied I preserved every
failed byte. I did not — **my successful p06 rerun overwrote my own p06 result log**. What I
preserved is the failed **source**:

| Retained failed source | SHA-256 | Bytes |
|---|---|---|
| `failed-attempt-01-p04-wrong-graph-key.py` | `480e1e74…c0644` | 11,049 |
| `failed-attempt-02-p04-unsorted-nodes-array.py` | `742b9cd2…3b45e5` | 11,413 |
| `failed-attempt-03-p06-wrong-ladder-module.py` | `cd1521d4…46c124` | 7,921 |
| `failed-attempt-04-p06-degenerate-identical-scope.py` | `f02b93c2…7bc05860` | 8,172 |

The failed **result** was captured by root at
`/tmp/opensip-design-corrections/codex-post-reset.v1/independent-v17-p06-attempt2-report.json`
(3,950 bytes, `83fb1ab13913ed7f2a05089b1c6c80272f4db48b7fec0b6487547bc915a50b68`) before my rerun
overwrote mine. **That capture is root's artifact, not mine.** Other failed attempts survive in tool
outputs.

Four categories kept distinct throughout: **case selection**; **corrected expectation** (my four
failed attempts); **static check** (reading bytes/schemas/code); and **actual product enforcement**
— of which this review contains **none**: no host, compiler, provider, repository, renderer, ledger
or OS executed at any point.

---

## Does source acceptance still hold?

**Yes.** Every correction above is to my *reporting*, to probe-scope characterisation, or to a
governance-record provenance claim. None reaches the reviewed design or reference source — except
V17-ADV-3, which is nonblocking and measured to mask nothing today.

The load-bearing conclusions survive on a corrected and narrower basis, and two of them are now
**better** evidenced than before: the admitted-domain change is measured token by token rather than
hand-waved as "no widening," and authority preservation is a byte-identity result rather than an
inference.

**Zero unresolved MUST. Zero unresolved SHOULD.** Three advisories across both passes.
**ACCEPT stands, for source and design only.**

**Independence.** Correcting my own report does not make this review dependent on the authored
source. Every point above was measured against the frozen bytes before being accepted — including
root's "52", which I verified at `design-assent.v16.json#/advisoryApplicationAccount` rather than
adopting. Points 1, 5 and 7 I confirmed independently rather than on assertion.

Nothing here infers blind, application, readiness or product acceptance. D-372 remains unapplied,
condition 5 NOT MET, all 32 gates unperformed, and **a new independent blind reconstruction remains
separately required.**
