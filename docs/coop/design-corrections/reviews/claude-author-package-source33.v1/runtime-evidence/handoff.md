# Handoff — author reference package v10, source33 remint

**Author standing.** Actual-Claude source author, session `823bf66b-e92a-4789-ab81-63a1a9dc371d`.
Author-assisted reference evidence only. **No independent assent is given or implied.** I cannot
accept the design, the blind work or the final application. Source33 independent acceptance,
whole-design review and blind acceptance all remain required and outstanding. **This package must
never be supplied to the blind consumer.**

## What to take

| Item | Path |
|---|---|
| **The package** | `/tmp/opensip-design-corrections/claude-author-package-successor.v10` |
| Package artifact manifest | `…/v10/artifact-manifest.json`, SHA `88c38b160e8b3af2702c0975271e10a765cd551b7245e8ac6f963887ef3551d2` (lists 305 files; **does not list itself**) |
| Remint account | `…/v10/source33-remint.v1.json` |
| Current binding | `…/v10/source-binding.v33.json` |
| Superseded v9 bytes | `…/v10/historical-source33-before-remint/` + `before-image-index.json` |
| Public report | `<runtime>/author-review.md`, `author-review.json` |
| Verification evidence | `<runtime>/verification/final/` (`verification.json`, per-group stdout/stderr) |
| Receipts | `<runtime>/probes/receipts/<label>/` — argv, stdout, stderr, exit for every command |

Runtime = `/tmp/opensip-design-corrections/claude-author-package-source33.v1`.

`author-review.md/json` deliberately live in the runtime, **not** inside package10, so that no
package artifact states the package manifest hash. There is no circular claim.

## To re-verify

```
/tmp/opensip-architecture-review-env/bin/python -I -B \
  /tmp/opensip-design-corrections/claude-author-package-successor.v10/verify-package.py \
  --source /tmp/opensip-design-corrections/candidate-subject.v33 \
  --out <a fresh directory outside both trees>
```

Expect exit 0 and `verification.json` with `passed: true`, `sourceFilesVerified: 12899`,
`packageFilesVerified: 305`, six groups covering **13 Run/control cases and 7 queries**.

If it ever fails, it now **still writes** `verification.json` with `passed: false` and the failing
stage recorded. That was the defect behind root's "no verification.json" — corrected without
weakening a single expectation.

## What changed, in one page

1. **Diagnosis.** The TS positive and both positive binding controls refused with
   `EVALUATOR_COMPLETE_PROOF_REPLAY`. Exactly one proof field differed: `executionDeficiencies`.
   A Coverage record retaining `(null, null)` had been given the sibling record's
   `language-tier-unsupported` while keeping its own null `nativeCause`. Source33 derives
   `required-cell-unsatisfied` for it.
2. **Not a source defect.** Frozen source33 refused correctly under its published no-invention and
   exact-per-record-pair law. **No frozen byte was edited and no fixture was adjusted to make an
   old artifact pass.**
3. **Helper corrected** — `author-helpers/evaluator.py` only: each record now contributes its own
   exact pair, `(null, null)` when it carries none; the manufactured `provider-unavailable`
   fallback is gone; the deterministic carrier order is recorded.
4. **Reminted on source33**: `checkpoint3`, `binding-controls`, `semantic-controls1` — new
   constructions, new proofs, new retained bytes, new run ids (except `collapsed-deficiencies`,
   whose run id is unchanged while its store bytes differ; both facts recorded).
5. **Reused exact source30 bytes**, re-verified against frozen33 in the same pass:
   `normalized-examples6`, `rust-selection-examples1`.
6. **Reproduced byte-identically**: `author-properties.json`, `mixed-universe-view.probe.json`.
7. **Second defect repaired.** In v9 the semantic negative group passed while having *no*
   discriminating power — its base proof was stale, so all three refused regardless of their
   mutation. In v10 the base admits, so each refusal isolates its own tamper. Measured both ways.

## Preservation

v9: **0 files removed**, every `historical-*` directory, `source-rebuild.v1.json`,
`evaluation-residual-author-assessment.json` (30 items, all PENDING),
`original-requirement-handoff.json` and `author-workspace-history.tar.gz` byte-identical. v9's own
manifest still hashes to `55066ece…`, matching root's `MF55066ece…`. 24 files changed in v10, 21
added, none removed.

## Open, and not addressed here

* Source33 independent acceptance; whole-design review; blind consumer acceptance.
* Thirty residual proposals, individually **PENDING**.
* The TS helper remains **partial**: execution deficiencies only for required
  `supported-available` accounts; no census, inventory, binding or candidate deficiencies; no
  `unsupported-typed` matrix rows. Complete frozen-owner replay remains the authority.
* `and`/`or`/`not` unexercised; `count-at-most`/`all-covered` unimplemented; two-binding
  construction incomplete with a single explicit selection.
* All native/compiler/OS records synthetic and unqualified; host TCB assumed for all thirteen.
* The remint changed which execution deficiency is cited, **not** the verdict (`fail` before and
  after).

Package10 is my owned work and is complete as handed off. Root edits nothing while I am active;
from here it is root's.
