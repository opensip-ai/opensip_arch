# Independent Grok review: history-selection02 original unit

**Reviewer:** Grok (explicitly authorized). Codex remains implementation lead. Not Claude agreement.
**Subject:** `/tmp/opensip-implementation/m1-history-selection-subject-02`
**Manifest SHA-256:** `39ddac40846fe240eea8352299d5059b7645cab9b0b0e7719f05a20d00d3d15e`
**Members:** 70
**Verdict:** **ACCEPT WITHIN STATED REFERENCE SCOPE**

This is not product history delivery, store custody, CLI grammar, report construction, browser qualification, or milestone/source promotion. Historical subject01 and its incorrect route remain under `prior/candidate01`. Joint10 later combined acceptance does **not** waive this unit.

## Custody

Verified before and after. Work used only `review/copy` and `review/probes`. Frozen subject not executed against and not written. No modes or symlinks listed.

| Check | Result |
| --- | --- |
| Manifest | `39ddac40…d15e` matches declared and adjacent copy |
| Files | 70 listed = 70 walk |
| Pins | **71/71** |
| After | frozen hash unchanged |

Private copy source and the seven generated outputs stayed byte-identical to the freeze. Query/mutant result JSON differ only by private scratch paths.

## Documented checker and controls

Private `fullcheck.py` (reference Python `-I -B`):

- `check.py`: **18/18** groups, 71 pins, `selected: false`
- `check_query.py`: **14/14** (actual pinned `close_run` over synthetic retained evidence)
- `check_budget.py`: exact documented sizes
- `mutants.py`: **12/12** killed
- `build_history.py`: **seven** generated outputs byte-identical

## HIS-F1–F6 (presentation review01 → this freeze)

Independently reproduced (**26/26**), not only author tests.

| Id | This freeze |
| --- | --- |
| **F1** | Format first (`REQUEST.UNKNOWN_OPTION` / `OUTPUT.FORMAT_NOT_APPLICABLE` / exit 2), including json + five valid IDs. Lexical/uniqueness before count (five IDs with one malformed → `REPORT.HISTORY_SELECTION_INVALID`, not the limit). Five distinct well-formed IDs → `EVALUATION.SELECTION_LIMIT`. Tokens never appear in the public route. One new detail registered in candidate common + shared registry. |
| **F2** | Malformed host `currentRunId` is `HistorySourceRefusal`, not a user request refusal. |
| **F3** | One retained read lease after non-render commits, released on failure. Current-run slot skips lookup and consumes a slot. Snapshot copy still sees this invocation’s own pivot after a later live purge. |
| **F4** | Explicit panel union; other-project present item refused; unavailable slots kept in request order; writer `evidence.pinned` detail refused. Independently recomputed canonical sizes: selection 896, four minimal unavailable 533, worst slot 12484, four maximal 49941, whole panel 51243. Never drop requested IDs to fit. |
| **F5** | Candidate `RunShowItemV1` / `RunShowResponseV1` refuses untyped items. Parent graph-query:3 still accepts the owner-audit arbitrary item. `run_show` invokes `identity_model.close_run` before a retained item; declared missing evidence → unavailable; unexpected `RuntimeError` is not relabelled corrupt. Consumer joins remain separate. |
| **F6** | Exact eight additive `{flag, owner, class, join}` records for default/analyze/fit/audit/candidates/inspect/review-brief/repair-preview. Identical `--history-run` join: 1..4 distinct full lowercase run3 IDs, HTML-only, no comma/prefix/latest/fallback. |

subject_run is an AST extraction of pinned report08: authoritative run carriers for default/analyze/fit/audit; candidates/inspect/review-brief query mappings; ephemeral/failure/invocation/repair-preview have no current Run.

## Query-schema versioning and legacy cache

**Decision.** Reuse of parent URI/major `urn:opensip:product-v1:workflows:evaluator3:graph-query:3` is the correct **selected successor identity**. This freeze is an unselected candidate file; silent in-place product overwrite is forbidden. After selection, an older untyped cached `run.show` item cannot become `RunShowItemV1` by relabeling (independently: parent accepts it, candidate refuses). A host with retained authority may project a new typed response from that exact retained Run, objects, blobs and admitted receipt via `close_run`. It must not reanalyze the current checkout or substitute latest. Unavailable authority stays unavailable.

A distinct candidate `$id` is **not** required in this freeze. Minting a parallel URI would not be a graph-query:3 successor. Common candidate follows the same pattern: parent `$id` plus one new `REPORT.HISTORY_SELECTION_INVALID` enum member.

## Joint10

`explicit-history.schema.json` is byte-identical (`3fc78bc5…9a94`, 1942 bytes). `explicit-history-panel.schema.json` is the same 4171 bytes but joint10 `694bc4c2…926e` vs this freeze `f96cba04…9ba9` — **not** identical. Joint10 combined acceptance does not rewrite or waive this 70-file unit.

## Must-fix / should-fix

**Must-fix:** none in the stated reference scope.

**S1 (should-fix).** `RunShowResponseV1` retained then-branch constrains `items` only when present (`minItems: 1`). A retained `run.show` object that **omits** `items` still passes the candidate schema. Producer always emits one item; consumer then `items[0]` would `KeyError` rather than admit an untyped payload. Not a false accept. Add `required: ["items"]` on the retained then-branch before product integration.

## Remaining duties

Select and compose query/common/registry/flag/report/inventory successors; bind admitted namespace snapshot and receipt handles; CLI parser append of the eight flag records; D9/command-envelope renderer goldens; HTML byte budget against remaining whole-document capacity; browser controls over embedded slots only. Actual store custody is absent. L02 global required-output delivery capacity remains a separate unresolved owner obligation. Automatic no-flag history is unchanged and out of this explicit-mode owner.
