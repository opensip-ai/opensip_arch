# Independent Grok design-unit review: source-selection v2

**Reviewer:** Grok (explicitly authorized). Codex remains lead. Not Claude agreement.
**Subject:** `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/source-selection-v2/`
**Manifest:** `/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/source-selection-v2-subject.json`
**Manifest SHA-256:** `1c4366eb3909433f5e5a790ced4a6d35a28c7b76322840e96297225943d135ff`
**Members:** 137
**Verdict:** **ACCEPT-DESIGN-UNIT**

This is exact source and semantic-owner selection for the implementation. It is not generator execution, bootstrap, product qualification, milestone close, or the fresh blind consumer. Original-unit verdicts are not rewritten.

## Custody

Verified before and after. Frozen architecture files were not executed against. Private copy only.

| Check | Result |
| --- | --- |
| Manifest | `1c4366eb…35ff` matches declared |
| Files | 137 listed = 137 walk; extra/missing/mismatch 0 |
| After | frozen hash unchanged |
| Archive | `docs/implementation/m1/trials/source-selection-v2-01/` status `sourceAccepted: false` |

## Reproduction

Private `python -I -B copy/check_selection.py --architecture opensip_arch --product opensip`: exit 0, stdout byte-identical to frozen `source-selection-v2-check08.stdout`. 46 base inputs, 40 proposed sources, 14 current, 323 planning rows, unapproved selection refused against accepted map, materialized drift refused, `selectionApproved: false`, `productModified: false`. Historical root-production scripts were not run.

Closed generator adapter accepts 40 mappings and 857 entry points. Generation03 `prepared04/options.json` had 26 mappings + 14 pending; those 14 pending IDs are exactly this unit’s current-dispatch set and are now closed `sourceMappings`. Generation03 entryPoints are byte-identical (857). Adapter refuses the incomplete 26-row options (`source major/profile/semantic owner differs`). The four generation03 prepared blobs (`owners.json`, `rust-projection.json`, `targets.json`, `ts-projection.json`) hash to the pinned checkpoint; they are not members of this 137-file subject. README’s “587 predecessor roots” is a prior-lineage coverage figure; this unit preserves generation03’s entire 857-root set.

## Original-unit duties

| Unit | Archived verdict | This source unit |
| --- | --- | --- |
| report-projection08 | **CHANGES REQUIRED** Q-FIT-1 | Unchanged. README keeps the fixture as defective historical evidence. Current envelope7 `FitAdvisoryReportV1` / `unavailable-query-result` and invocation5 `FitQueryFromAnalysisParams` are the selected composition, not retrospective acceptance of the 21-file freeze. |
| fit-interruption01 | ACCEPT reference; Q-FIT-1 not closed on report08 | Laws are now in the selected schemas/owners. Dictionary custody and exact decoder remain product duties. |
| history-native-delta01 | ACCEPT delta; history02 S1 closed in query4 | graph-query:4 retained `run.show` `required:["items"]`. Historical graph-query:3 (`graph.v3.schema.json`) is a distinct digest and is not relabeled. Envelope7 `queryResponse` `$ref`s query4. |
| native07 | ACCEPT delta; native06 RF-1 closed | Wire `patternDialect.standing` carries the promotion condition; “selected final owner” absent. Four-pair owner-pattern scope, 35 pattern rows, public-route and P3 successors present. Relation-path gap and native03 frame-payload slot remain named duties. |
| required-output01 / L02 | ACCEPT reference; old criterion superseded not passed | D9 v1.15 changes only invariant[1]; after-text equals `successor.json` passageOverrides[0]. L02 record: `oldCriterionMet: false`, `oldCriterionSuperseded: true`, `sourcePromoted: false`. |
| native-integration03 | ACCEPT delta; S1 closed | Guard duty preserved in README. |

## Scoped interruption (C01/C02)

Three span overrides under `owners/interruption/passage-overrides.json` match the exact parent paragraphs of `workflows-and-surfaces.md`. The one-line workflow-model correction is the generic line-380 override of `workflows_model.v1.py` (`required` → `results`) and matches `model-successor.json`. Generic `verify_design.selected_passage` refuses `{startLine,endLine}`. Those spans are authenticated candidate data checked by `check_selection.py`, not generic lock selectors. Report line passages’ before-images match chapter 14; `scoped-owner-succession.json` states current encoder names are envelope7/invocation5. Adoption is explicit and coherent.

## New-Plan, codecs, coverage

Recognition-plan1, identity3, common4, public-detail registry, native public-route successor and `new_plan_admission.py` are selected together. Retained `close_run` / historical Plans stay compatible. Report profile6 is 27,829,365 B / depth 39; generic envelope remains 4 MiB. Identity/native current URIs keep historical coop digests distinct (`native` `2d37b810…` vs current `e5834d37…`). Policy v1 and v2 use different `$id`s and digests.

Planning coverage is 323 not-executed rows. **RP-OBL-R11-LOCATION** stays open before M4 (graph endpoints are not source spans). **P01/X01** stay open before M5. These are honest remaining product duties, not placeholders that block this source-unit selection.

## `contract_successor`

Product `tools/verify_design.py` is byte-identical to the freeze snapshot. Vocabulary is `ACCEPT-DESIGN-UNIT` / `ACCEPTED-DESIGN-UNIT`. This unit’s 11 parents are accepted-base pins. Binding this record with the archived report08 CHANGES REQUIRED review and canonical inventory assent refuses: `independent contract acceptance missing or findings remain`. Captured base lock `c5a1e568…4314` still selects inventory3. Live product lock has since grown an inventory4 successor (`58d499e6…e636`); neither lock binds this source-selection record. No assent or lock data was written.

## Must-fix / should-fix

None in this source-unit scope.

## Remaining (do not block this unit)

Complete generation tooling/bootstrap; fresh blind consumer/integration; private host admission, retained source custody, query execution and delivery; R11 locations before M4; P01/X01 before M5; relation-path fact admission; prepared-read authority and production sender; bounded encoding/stream tests; all selected implementation milestones. Envelope7/invocation5 description genealogy still says “graph-query:3 operations” while structural `$ref`s are query4 — succession narrative, not current dispatch.
