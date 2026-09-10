# v18-checker-coauthor.v1 — bounded reference-checker source review

**Role.** Source **coauthor** review of a root-authored reference-checker correction.
**Coauthor assent only** — not independent acceptance, not readiness, not promotion.
I did not read the independent reviewer's private reasoning.

**Verdict: ASSENT.** `changesRequired` is empty. I made **no source correction** —
the ten-line fix is adequate, complete and minimal. **Suggested severity: SHOULD**
(reasoning in §5).

## 1. Assurance, not contract

This repairs a **reference harness**. No product semantic, schema, model, law, enum,
field or authority changes. The workflows model, every contract document and every
case expectation are byte-unchanged; only comparison logic inside ten checker
exception handlers moves.

## 2. Custody — one identity from three sources

| Item | Value |
|---|---|
| v17 manifest | `8cfe6d20a7d49b819f7c2eb2578afcaa5037048ed290ff1867fdcd6789cf3a9c` (7671 files) |
| Frozen checker = manifest row = proposal `beforeSha256` | `2fe3143944ff256c84d6ef3f09be685868a22e7937e7f4bb21e4b717b523d17d` |
| Proposed checker (`afterSha256`, verified on disk) | `2ac26ab8194993358b529a764eb3f9f852f4f4385d2f31bff5a203da123e6392` |

`checker.before.py` is byte-identical to the frozen file. All writes are confined to
my output directory.

## 3. The defect, and why the guard is the checker's own law

Each handler compares a **defaulting `.get` on the expectation side**. A case
expecting success has no `refusal` key, so `exp.get('refusal')` is `None`; a refusal
raised with `detail is None` then satisfies `None == None` and the check **passes**
although an unexpected refusal occurred. Detail-free refusals are real — e.g.
`repair_preview` raises `Refusal('REQUEST.PRECONDITION_FAILED', None, …)`.

The decisive point in the proposal's favour: each of these handlers is *already*
paired with a post-`try` `if 'refusal' in exp: check(cid, False, 'no refusal')`. The
checker **already** uses key membership to mean "a refusal was expected". The guard
restores that same convention to the raised-refusal direction — a restoration of
existing meaning, not a new law.

## 4. Scope completeness — derived independently

I encoded the defect signature myself (expectation-side defaulting `.get` **and**
control-flow-selected by a raised exception) and scanned the whole checker: **25**
`.get(...)==` comparisons exist; **exactly 10** match, at exactly the ten proposed
lines. The other fifteen put the `.get` on the **observed** side with an **indexed**
expectation, so an absent key raises `KeyError` and fails loudly. The single near
miss is line 146 — `t.get('errorCode') == g.get('errorCode')` in the **D9 golden**
comparison, where absence-matching-absence is the intended semantics (the
neighbouring `(t.get('reasonCodes') or [None])[0]` normalises absence deliberately).
Correctly left alone. **Ten is the complete set; I found no missed equivalent.**

**AST delta:** 452 → 462 Compare nodes, **zero originals removed**, ten new
membership conjuncts, each keyed to its own `.get` key, each preserving the original
comparison as the second conjunct; statement count unchanged, line numbers aligned,
ten diff hunks.

## 5. Severity

**SHOULD.** It is a real assurance weakness that can silently convert an unexpected
refusal into a pass, and it should be fixed before promotion. It is not MUST as a
defect *of the subject*, because **no currently-masked failure exists**: the proposed
checker over the unchanged frozen corpus yields an identical **1787/1787** with an
identical (empty) failure set. The canonical PASS is not shown false. Root may
elevate on promotion-gate grounds; I record the evidential basis rather than the
label.

## 6. The ten handlers, individually

| Line | Guarded call | Key | Guard added | Real executions |
|---|---|---|---|---|
| 171 | `run_invocation` | `refusal` | 'refusal' in exp | 4 |
| 384 | `build_import` | `refusal` | 'refusal' in case['expect'] | 8 |
| 407 | `admit_source_mapping` | `refusal` | 'refusal' in case['expect'] | 1 |
| 1112 | `repair_preview` | `refusal` | 'refusal' in case['expect'] | 6 |
| 1158 | `repair_recover` | `recoverRefusal` | 'recoverRefusal' in exp | 1 |
| 1171 | `repair_apply` | `refusal` | 'refusal' in exp | 5 |
| 1203 | `repair_verify` | `refusal` | 'refusal' in exp | 1 |
| 1226 | `admit_test_execution` | `refusal` | 'refusal' in exp | 17 |
| 1320 | `render` | `refusal` | 'refusal' in case['expect'] | 1 |
| 1360 | `review_join` | `refusal` | 'refusal' in exp | 2 |

Three deserve specific note. **384** is the only compound handler: the `errorCode`
conjunct is preserved *outside* the new parentheses, so the guard binds only the
refusal comparison. **407** has reversed operands (`exc.detail == expect.get(...)`)
and is still correctly guarded. **1158** is the compact one-line form with a
trailing `continue`, preserved.

## 7. Executable evidence, with limits

* **Baseline** — frozen checker, unchanged frozen corpus: 1787 / 1787 / 0 failed.
* **Non-regression** — proposed checker, same corpus: **1787 / 1787 / 0**, identical
  failure set.
* **Discriminating injection (mine, not root's expected output)** — I took
  `preview-applicable`, which expects success and has no `refusal` key, and set
  `runOverride.findings = []` so `repair_preview` raises its **real** detail-free
  refusal. **Frozen: 1785 checks, 0 failures** — the unexpected refusal passes
  silently. **Proposed: 1785 checks, 1 failure, exactly `repair.preview-applicable`.**
* **Explicit-null non-regression** — all three deliberate `"refusal": null` cases
  still pass, each retaining its passing `.refusal-reason` discriminator. The guard
  does **not** disallow deliberate null-detail expectations: the key is *present*, so
  `None == None` still matches.
* **Reachability trace** — all **10 of 10** guarded handlers execute in the real
  canonical run (46 executions), so none is dead code, and every one of those real
  executions had its key present.

**Limits.** The injection is a harness-level corpus mutation forcing a real model
refusal; it is not evidence about any product Run, host, ledger or admission. Root's
100 handler-body executions are **synthetic**. Neither is a six-unit reproduction —
root runs the canonical six after final records and pins. Line-execution counts show
reachability, not that a guard discriminated at that site.

## 8. Non-blocking observation (V18-OBS-1)

When the guard fires, the third `check(...)` argument is still `r.detail`, which is
`None` in exactly the case the guard exists to catch — my injected failure row reads
`{'id': 'repair.preview-applicable', 'ok': False, 'detail': None}`. Not required: the
check ID identifies the case, the verdict is correct, and changing the diagnostic
would touch the same ten lines without altering any verdict. A future pass might pass
the error code or remedy instead. Out of bounded scope here.

## 9. Disposable copies and pins

`work/` is an rsync of frozen v17 (excluding `reviews/`, plus the three review files
the pin manifests name). I invoked `check_workflows.v1.py` **directly**, not through
`run-reference-checks.py`, so **no source pin needed refreshing and none was
refreshed**. Once the proposed checker is placed in them these copies are **not**
source-identical to frozen 17, and **no report produced here is a frozen-17
artifact**. `work-injected/{frozen,proposed}` carry a deliberately mutated corpus and
are throwaway injection trees, not candidate source. All probe sources and raw
outputs are retained; nothing was overwritten.

## 10. Standing

The two earlier independent non-blocking advisories — imported
`perKindApplicability.rule` metadata and the historical source pointer — are
separately accounted in the application and are **not** touched here; I edited no
accepted contract byte. A newly frozen 18, a fresh independent full review, a **new
blind consumer** and a full application review all remain required.
