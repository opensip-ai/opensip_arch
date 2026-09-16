"""Follow-up after the first workflow-projection run crashed at art_extra (preserved in receipts/checks/after-edits-2).

The historical fixture reminted a baseline with a detectorClosure row that no policy rule contributes and expected
baseline admission to pass so the bound E0 join could refuse it. Under the corrected detector identity law that
artifact is not a lawful baseline, so admission now refuses first. The control records the new admission boundary
explicitly (by refusal message, not code alone) and keeps the bound E0 comparison refusal; the E0 exact-map subset
refusal remains covered directly by e0-extra-detector-id-refused.
"""
import json, sys
sys.path.insert(0, '/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v1/tools')
from textedit import apply  # noqa: E402

CWP = 'docs/coop/design-corrections/workflows/check-workflow-projection.v3.py'
row = apply('fix art_extra admission boundary', CWP, [
    ('''art_extra["baselineId"] = P.wid("baseline2", "workflow.baseline", art_extra["descriptor"])
P.verify_baseline_artifact_v3(art_extra)
''', '''art_extra["baselineId"] = P.wid("baseline2", "workflow.baseline", art_extra["descriptor"])
try:
    P.verify_baseline_artifact_v3(art_extra)
    check("m4-extra-noncontributing-detector-refused-at-baseline-admission", False, "admitted")
except P.Refusal as _extra_exc:
    check(
        "m4-extra-noncontributing-detector-refused-at-baseline-admission",
        _extra_exc.error_code == "CONFIG.INVALID" and _extra_exc.detail == "EVALUATION.FINDING_JOIN_REFUSED"
        and "embedded policy rule contributions" in str(_extra_exc.remedy),
        repr((_extra_exc.error_code, _extra_exc.detail, _extra_exc.remedy)),
    )
'''),
])
print(json.dumps(row, indent=1))
