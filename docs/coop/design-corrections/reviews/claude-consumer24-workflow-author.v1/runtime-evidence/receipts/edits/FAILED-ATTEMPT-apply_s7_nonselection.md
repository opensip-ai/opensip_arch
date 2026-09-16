# Failed attempt preserved: tools/apply_s7_nonselection.py

- Exit code 1: `S7 non-selection prose projection contract: ... workflow-projection-contract.v3.md replacement 1 expected exactly one match, found 0`.
- Cause: the §13 anchor was written as `whose subjectPath is` but the contract text is ``whose `subjectPath` is`` (backticks).
- Effect: `textedit.apply` writes a file only after all of its replacements match. Files written before the refusal:
  `workflow_projection_model.v3.py` (8 replacements) and `workflows-and-surfaces.md` (1 replacement); both rows are in `text-edits.jsonl`.
  Not written by that attempt: `workflow-projection-contract.v3.md`, `check-workflow-projection.v3.py`, and the
  `comparison-result.schema.json` PivotPresence description.
- Resumed by `tools/apply_s7_nonselection_resume.py` with the corrected anchor; nothing already applied is re-applied.
