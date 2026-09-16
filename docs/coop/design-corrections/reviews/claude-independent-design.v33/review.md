# Independent design review — consolidated product **source33**

Same reviewer origin `ce3dec3b-0620-44ec-86e6-129b0e25cb1b`. I have authored no source in this
lineage and am none of the six excluded source-author origins. My source32 ACCEPT and the two record
reconciliations are historical and unchanged; **none of them accepts these bytes.**

**Verdict: ACCEPT.** Zero new MUST, zero new SHOULD, three advisories (one raised and resolved
within this review).

Design and reference scope only. **No application grade, no activation, no blind acceptance, no
package acceptance, no implementation authorization, no commit or push.** No consumer output,
runtime, report or blind replay file was opened; no blind oracle is an input here.

---

## 0. Custody

| Binding | Expected | Measured |
|---|---|---|
| `candidate-subject.v33.json` | `1cf3db70…9299` | ✅ |
| `candidate-source.v33.tar.gz` | `a3707693…14c7` | ✅ |
| Snapshot | 12,899 files / 736,764,309 B | ✅ every row by hash **and** size; 0 missing, 0 mismatched, **0 extras** |
| Archive ↔ manifest | — | ✅ **all 12,899 members** byte-compared; 0 mismatches, none extra, none absent |
| Parent | source32 | ✅ `3897e8d1…` — exactly the subject I graded |
| Baseline record | `7336c04d…65af` | ✅ the corrected 107-row reconciliation.v2 review |

Frozen33 re-measured **unchanged** after every run (0 deviations). Report writers ran only in a
disposable copy of 1,357 files verified byte-equal first.

**My delta: 1 added, 0 removed, 17 changed (18 touched), +98,195 bytes** — agreeing with root's
inventory on all 18 paths. Root's listing is inventory, never approval.

## 1. The changed execution law — correct, and controlled in both directions

### First-match applicability
The five-token order is published as normative with an `x-opensip-applicability-precedence`
annotation. My exhaustive **108-cell grid** reaches all five tokens, and the contract's own
reachability argument holds under measurement: **unselected + null U → `unavailable-unselected`** in
all 16 cases, **selected + null U → `unavailable-null-universe`** in all 16. So the two advertised
states stay distinct rather than collapsing — which is exactly why row 3 must precede row 4.
`UNSUPPORTED-TYPED` outranks both (32/32) and `vcs-change`+`kind=none` outranks everything (12/12).
The checker carries a 10-case precedence control where every `want` equals `got`.

### External `sourceUniverse` → binding join
`sourceUniverse` equals the binding's universe for **every** applicability; a null binding U stays
null; carrying no Coverage does not erase the coordinate; `targetUniverse` is deliberately **not**
joined. It is published as `x-opensip-external-joins` precisely because JSON Schema cannot compare a
different document — an honest statement of what admission compares rather than a pretended
per-record check. Four negative controls refuse `EXECUTION_INPUTS_COVERAGE_DERIVE`
(`inapplicable-vcs`/`unsupported-typed` null source universe, `null-binding-universe-must-stay-null`,
`foreign-universe`) and two positive controls admit.

### Request vs selection vs disclosure
Kept distinct and each separately controlled: a capability **request** may be `UNSUPPORTED-TYPED` and
still requestable; the **enumerator** selection is independently unselected or selected-with-null-U;
and optional retained **disclosure** is a third thing —
`optional-unselected-account-retained-typed-disclosure` admits while
`optional-unsupported-cell-owes-no-required-cell-row` shows an optional unsupported cell is not
forced to execute a provider to close.

### Selected-U unsupported Coverage, and the required bridge
A selected-U `UNSUPPORTED-TYPED` cell may lawfully have returned Coverage while its account names
none of it: `coverageIds` stays empty because only `supported-available` names envelopes, and the
Coverage remains in its returned view, the stage capture, `selectedRefs` and native disclosure.
Disclosure runs through `derivedAccounts` carrying the **matrix** pair, and a **required** such cell
additionally bridges to proof and holds the Run at **indeterminate** —
`full-run-required-unsupported-matrix-pair-bridge` is an admitted Run, verdict `indeterminate`,
carrying `["language-tier-unsupported","capability-missing"]`.

### `(null, null)` for pure missing work
Where no retained source carries a pair, the derived pair is explicitly `(null, null)` and **not**
`provider-unavailable` — 18 measured cases. Four controls refuse any attempt to claim otherwise, and
the typed carrier survives alongside a census failure
(`[["budget-exhausted", null], [null, null]]`), so real native causes are never suppressed and
inventory budget failures are never rewritten. The pair is taken **whole** from the first record that
*actually carries one*, never the first source record and never re-paired across records.

### The two-owner contradiction, corrected together
Composition §9.6 now records on the record that its own table had **explicitly prescribed** the
`provider-unavailable` fallback that execution-inputs §4/§5 forbade — a genuine **contradiction
between two normative owners**, since a host obeying §4 and a host obeying the old table could not
both admit — and that the earlier diagnosis calling it a reference-side invention was **too narrow**.
I agree with both the correction and with recording it rather than quietly fixing it. Measured on 33
the owners agree, and `provider-unavailable` remains lawful exactly where a record genuinely carries
it (an unavailable binding's own declared deficiency, a typed unavailable receipt) — a distinction my
own keyword scan initially blurred and reading resolved.

**Control set: 75 cases, 0 mismatches, 41 admitting / 34 refusing, including five full-Run rows** with
real `run3:` ids that assert exact proof ExecutionInputs digest equality
(`executionInputsDigest == digest0`). These are reference fixture self-consistency controls — not
blind reconstruction, not provider qualification.

## 2. Bounded scopes, verified on final33

- **Candidate envelope, schema only.** I reproduced it with root's own two instances against the
  frozen33 schema: the `execution2` prefix **REFUSES** on the published pattern and the corrected
  `exec-plan2` prefix **ADMITS** the unavailable/null envelope. This is schema admission **only** — not
  a retained join, not a full Run, and **not** a retroactive success for the original author q2
  command, whose refusal stands. I infer no schema admission from that probe.
- **Optional candidate carrier reachability.** Root's assessment is bound to source32 and an author
  draft, so I verified on **final33**: `optional-candidate-absent-envelope-derives-null-pair` admits,
  and `full-run-optional-unselected-and-optional-unsupported-…` is an admitted Run with verdict
  **pass** and **empty** cause pairs. The required side still refuses
  (`required-candidate-absent-envelope-still-refuses`), so candidate refs exist only when an envelope
  exists.

## 3. Suites and planning

All six changed-input suites exit 0 — including `check-execution-inputs.v1.py`,
`check-identity.py` (1596/1596) and `check_native_evidence.v2.py` (375/375). The pinned launcher
validates **1,244 pins, 0 changed or missing, 16/16 children**. Both planning groups pass (198 unique
paths; 320 mappings, 54 planned cases).

Planning: **layer4 binds 29 inputs, all resolving against frozen33**, differing from layer3 by exactly
one repin (`native-evidence.md`, which is in my delta) with nothing added or removed; layer3, layer2
and the original source25 layer are preserved; **zero `.py` files are normative inputs**; and
**198 / 20 / 320 / 54** are unchanged. Report/module layout and M0–M6 stand.

## 4. Author package — verified, after a status change mid-review

The root-owned `author-package-update.json` was **PENDING** when I began. My final pre-finalization
re-read caught it at **READY_FOR_INDEPENDENT_REVIEW**, so I performed the verification rather than
finalizing an incomplete package review. Both exact versions are recorded.

**Package10 verifies:** artifact manifest matches the root-named digest `88c38b16…`, **305/305**
members hash-verified, `source-manifest.json` byte-equal to the frozen33 manifest, and **all 13**
Run/control cases replay as expected through **both** `open_run_closure` and `close_run` under my own
decoder — 7 positives ADMIT/ADMIT, 3 false-result controls ADMIT then REFUSE
`EVALUATOR_COMPLETE_PROOF_REPLAY`, invalid-default ADMIT then REFUSE `ENUMERATION_BINDING_PROGRAM_ENTRY`,
both lawful binding controls ADMIT. `verify-package.py` exits 0 over 12,899 source files with **7/7**
query checks. My group outcomes match root's retained verification — corroboration only; my basis is
my own execution.

**Package9 remains preserved and was NOT rerun.** It was rebound from package8 rather than constructed
on 33, and three positives refused complete proof replay. That is the *correct* outcome for a rebound
package under changed law — a historical source30 construction does not become a new execution by
rebinding. Root's explanation that its negative-group expectation was **masked** (the base proof had
already refused) rather than independent tamper evidence matches my own reading of the receipts.

Limits retained exactly: **A-10** — TS checkpoint is helper-versus-owner only, six owner-derived
self-consistency, `exists`/`none` with other operator limitations, incomplete two-binding construction
with a single explicit binding, no compiler/provider/OS qualification. **A-9** — repair controls keep
their admitted-versus-unit limitations. **All 30 author residual proposals remain PENDING** independent
grading.

## 5. Advisories

- **A-9**, **A-10** — carried unchanged; nothing in this delta touches their subjects.
- **A-11** *(raised and resolved within this review)* — no source33-bound package existed when I began,
  leaving nine F rows unevidenced. Resolved when the root input named package10 and I verified it.

## 6. Standing

All **107** rows carry `appliedByThisReview=false` and `finalApplicationOutcomeGranted=false`.
**TCB-SCOPE-01** assessed once over its **13** dependent rows with the joint-reopening consequence
intact. **28** condition-2 obligations retained; **32** product qualification gates unperformed with
**condition 5 NOT MET**; **54** recovery cases unexecuted; the **D9** implementation obligation on
DR-007 / DR-011-R08 persists. Blind reconstruction and final application review/activation remain
separate.

---

*All 107 individually reasoned rows, with current33 owner paths, manifest-derived changed/unchanged
arrays and inherited-reading standing, are in `review.json`. Receipts are in `receipts/` and probe
sources in `probes/`. Five probes that were wrong or imprecise are preserved and labelled: a
document-wide table-order index, a metric that read False only because a clean PASS row has no refs, a
keyword scan that mistook the lawful provider-unavailable carrier for the forbidden one, an invented
envelope record shape, and an initial misreading of a negative group's `passed` field.*
