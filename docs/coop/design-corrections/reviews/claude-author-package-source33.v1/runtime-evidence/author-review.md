# Author reference package v10 — source33 remint

**Standing.** Same actual-Claude source author (session `823bf66b-…`), acting as **author of the
reference package only**. This is **not** independent review, **not** blind reconstruction, **not**
product qualification, and **not** any form of acceptance. I cannot accept the design, the blind
work or the final application. Source33 is frozen and immutable: **no architecture, source, pin,
planning or live file was edited.** No commit, no push, no other agents. This package must never
be supplied to the blind consumer.

Owned outputs: the new package at `claude-author-package-successor.v10` and this runtime. Package
v9 and every historical preparation directory are read-only here and verified unchanged.

---

## 1. Frozen source33 verified

| | |
|---|---|
| Manifest | `candidate-subject.v33.json`, SHA `1cf3db70d4b73b0c42f1393331e6a874ee26f7ddf67aa05c6ac15a5753069299` — **matches** the declared value |
| Parent | `3897e8d1…10bf2` (frozen32) |
| Tree | 12 899 files, 736 764 309 bytes — **every byte re-hashed against the manifest**: 0 mismatched, 0 missing, 0 extra |

Receipt: `probes/receipts/verify-frozen33/`, report `reports/frozen33-verification.json`.

## 2. Diagnosis — one proof field, one stale helper rule

Root's verifier failed with `EVALUATOR_COMPLETE_PROOF_REPLAY` on the TypeScript positive and the
two positive binding controls. I replayed the retained export through the frozen owner and
compared the retained proof to what source33 derives.

**Exactly one field differed: `executionDeficiencies`.** One of its two items:

| | cause | nativeCause | originating Coverage |
|---|---|---|---|
| retained (source30) | `language-tier-unsupported` | `null` | `acc2c1c5…` |
| derived (source33) | `required-cell-unsatisfied` | `null` | `acc2c1c5…` |

That Coverage record **retains `coverage: complete`, `deficiency: null`, `nativeCause: null`**. The
sibling record `30616b96…` retains `unknown` / `language-tier-unsupported` / `capability-missing`.

The cause was in the **bundled author helper**, `author-helpers/evaluator.py`:

```python
fallback = (records[0][1]["deficiency"] if records else None) or "provider-unavailable"
carriers = [(hx, e["deficiency"] or fallback, e["nativeCause"]) for hx, e in records]
if not carriers:
    carriers = [(None, fallback, None)]
```

This did both of the things source33 forbids. A record carrying no pair **borrowed
`records[0]`'s deficiency while keeping its own null `nativeCause`** — an unzipped, re-paired
carrier — and a missing-work account would have been handed a manufactured `provider-unavailable`.

**This is not a source defect, and I did not edit the source.** Frozen source33 refused
correctly: `execution-inputs-contract.v1.md` §4/§5 and `evaluator-composition-contract.v3.md` §9.6
require each retained record to contribute its own exact pair, with `(null, null)` bridging to
`required-cell-unsatisfied` and nothing manufactured. The published law did its job against a
stale author artifact.

**Minimal correction**, to the helper only:

```python
carriers = [(hx, e["deficiency"], e["nativeCause"]) for hx, e in records]
if not carriers:
    carriers = [(None, None, None)]
```

A null deficiency then reaches `required-cell-unsatisfied` through the helper's existing registry
branch. I also recorded the deterministic carrier order in the helper: records are walked in the
account's `coverageIds` order (`x-opensip-order: canonical-set`), accounts in the retained array
order, and the emitted list is a `cset`, so the proof bytes do not depend on either walk while the
owner re-derives its own §4 owed order independently.

Receipts: `probes/receipts/d1b-proof-difference/`, `probes/receipts/d2-new-proof/`.

## 3. Reconstruction — what is new, what is reused, what is unchanged

**Reminted on frozen source33** (new constructions, new retained bytes):

| Group | Case | source30 runId | source33 runId |
|---|---|---|---|
| checkpoint3 | author-ts | `run3:0ef285d5…` | `run3:0f6b13af…` |
| binding-controls | ts-lawful-default | `run3:0ef285d5…` | `run3:0f6b13af…` |
| binding-controls | ts-invalid-default-entry | `run3:bd000aa6…` | `run3:9f433416…` |
| binding-controls | ts-lawful-explicit-selection | `run3:93412a24…` | `run3:80c4ab7d…` |
| semantic-controls1 | severity | `run3:fb0455f3…` | `run3:803bfad3…` |
| semantic-controls1 | unrelated-scope | `run3:99494158…` | `run3:4021c30a…` |
| semantic-controls1 | collapsed-deficiencies | `run3:d785ab9b…` | `run3:d785ab9b…` **(same id, different store bytes)** |

`collapsed-deficiencies` keeps the same runId because its mutation discards the second deficiency
item and unions the refs, and the first item did not change; its **store bytes still differ**
because the retained base blobs did. Both facts are recorded rather than glossed.

**Reused EXACT source30 construction bytes**: `normalized-examples6` (rust, rust-partial,
syntax-code, syntax-data) and `rust-selection-examples1` (rust-bin, rust-lib-only). Their bytes are
byte-identical to v9 and they were **re-verified against frozen source33 in this same pass**, so
their standing is measured here, not inherited.

**Reproduced byte-identically** on source33: `author-properties.json` and
`mixed-universe-view.probe.json` — re-executed, same bytes, limitations unchanged.

**Regenerated** because they are derived from the TS Run: all seven `query-checks1/*` observation
files (`wrong-run.json` alone is unchanged, since it never binds the real Run) and
`query-assessment.json` (unchanged content — the same seven checks still pass).

The superseded source30 bytes are preserved verbatim in
`package10/historical-source33-before-remint/` with an index, under a name that collides with none
of the existing `historical-source25/26/27/28/30/31/32`, `historical-consumer-custody` or
`historical-intermediate-preparation` directories.

## 4. A second, quieter defect this repaired

In package9 the semantic negative group reported **pass** while having **no discriminating power**.
Its three controls are tampered variants of the TS proof; because that base proof was itself stale,
each of them refused with `EVALUATOR_COMPLETE_PROOF_REPLAY` **whether or not its mutation was
present**. The group's expectation was met by an artifact that established nothing.

Measured both ways (`probes/receipts/d3-control-discrimination/`):

| Package | untampered base | three tampered controls | refusal attributable to its own tamper |
|---|---|---|---|
| v9 (source30) | **REFUSE** `EVALUATOR_COMPLETE_PROOF_REPLAY` | all REFUSE | **no** |
| v10 (source33) | **ADMIT** | all REFUSE | **yes** |

## 5. Verifier reporting corrected

Root reported "no verification.json due to the query assertion failure". That is a real defect in
my own `verify-package.py`: it asserted mid-flight, so a failing run left no report at all. It now
**records** a group crash or a query failure and still writes `verification.json` with
`passed: false` before exiting non-zero.

**No expectation was weakened.** Every group's admission/refusal condition, the
`ENUMERATION_BINDING_PROGRAM_ENTRY` clause, the `EVALUATOR_COMPLETE_PROOF_REPLAY` clause for the
negatives, the seven-check query condition and the final `assert result['passed']` are unchanged.
The report now additionally carries each case's observed owner/semantic admission and reason.

Demonstrated with a disposable copy whose query step was deliberately broken
(`reports/honest-failure-demo.json`): exit 1, `verification.json` written, `passed: false`,
`{"stage": "query", "error": "AssertionError", "detail": "query step 1 exited 3"}`. The throwaway
was deleted; package10 and v9 were never written by it.

## 6. Actual fresh verification of package10 on frozen33

`verify-package.py --source <frozen33> --out <fresh>` — receipt
`probes/receipts/verify-package10-final/`, exit **0**.

| Group | Cases | Passed | Observed |
|---|---|---|---|
| checkpoint3 | 1 | yes | author-ts ADMIT/ADMIT |
| normalized-examples6 | 4 | yes | all ADMIT/ADMIT |
| rust-selection-examples1 | 2 | yes | all ADMIT/ADMIT |
| semantic-controls1 | 3 | yes | all ADMIT then REFUSE `EVALUATOR_COMPLETE_PROOF_REPLAY` |
| binding-controls | 3 | yes | lawful ×2 ADMIT; invalid-entry REFUSE `ENUMERATION_BINDING_PROGRAM_ENTRY` |
| query | 7 | yes | all seven checks pass |

**13 Run/control cases and 7 queries**, `sourceFilesVerified: 12899`, `packageFilesVerified: 305`,
source manifest `1cf3db70…`, package manifest `88c38b16…`.

The required negative still refuses **first** at the enumeration boundary with
`ENUMERATION_BINDING_PROGRAM_ENTRY` — it is not masked by any later stage.

## 7. Package hashes

| | |
|---|---|
| source manifest | `1cf3db70d4b73b0c42f1393331e6a874ee26f7ddf67aa05c6ac15a5753069299` |
| package10 artifact manifest | `88c38b160e8b3af2702c0975271e10a765cd551b7245e8ac6f963887ef3551d2` |
| package9 artifact manifest (unchanged) | `55066ece33a25ccb1f5b2984227196863a168ea9814049a4285f275ad905b028` — matches root's `MF55066ece…` |
| package10 files | 306 on disk; the manifest lists 305 and **does not list itself**, so it makes no circular claim about its own bytes |

Versus v9: 24 files changed, 21 added, **0 removed**. Every `historical-*` directory,
`source-rebuild.v1.json`, `evaluation-residual-author-assessment.json` (30 items, all PENDING),
`original-requirement-handoff.json` and `author-workspace-history.tar.gz` are byte-identical
(`reports/preservation.json`).

## 8. Limits — unchanged, and none of them repaired by this pass

* Only the TypeScript checkpoint compares a **partial** consumer helper against the owner. The six
  other positives are owner-derived / replayed **self-consistency**.
* The helper exercises `exists` and `none`. `and`/`or`/`not` are **unexercised**;
  `count-at-most` and `all-covered` are **unimplemented**.
* The two-binding construction remains **incomplete**, retaining a single explicit selection.
* All native, compiler and OS records are **synthetic and unqualified**; the thirteen cases assume
  a trusted host TCB.
* Thirty independent residual proposals remain individually **PENDING**; nothing here grades them.
* Source33 independent acceptance, whole-design review and blind acceptance all remain **required
  and outstanding**. This pass establishes none of them.
* `verification.json` is package **revalidation by its own author**, not independent
  reconstruction. Its standing line says so and I do not claim otherwise.
* I have no access to any consumer runtime, output or root blind file, and read none.

## 9. Honest residue

1. The reminted TS Run's **verdict is unchanged (`fail`)** — the corrected carrier changed which
   execution deficiency is cited, not the finding-driven verdict. Anyone comparing old and new
   should not read the remint as a verdict change.
2. The corrected helper still emits execution deficiencies **only for required
   `supported-available` accounts**. It does not establish census completeness, inventory, binding
   or candidate deficiencies, and does not emit the `unsupported-typed` matrix rows the owner does.
   Complete frozen-owner replay remains the authority; this pass narrowed the helper's error, it
   did not complete the helper.
3. `collapsed-deficiencies` does not exercise the corrected law at all — its mutation discards the
   second item either way. It tests ref-collapsing, and that is all it tests.
4. `source-rebuild.v1.json` remains the **source30** construction receipt at package root. It is
   preserved deliberately; `source-binding.v33.json` and `source33-remint.v1.json` are the current
   records and name which groups each account covers.
5. Three receipts in this runtime exit non-zero and are kept: the first `d1` probe (wrong
   `decode_store` arity) and the two reminted-control verifications, which exit 1 because
   `check-export.v4.py` reports "some check refused" — the expected outcome for a negative group,
   as `verify-package.py` encodes per group.
