"""Scoped receipt binding controls; never assembles or grants acceptance."""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'bind-review-receipts.v1.py'
ROOT = Path('/Users/sb/code/opensip-ai/opensip_arch')
ASSENT = ROOT / 'docs/coop/design-corrections/reviews/codex-post-reset.v1/design-assent.v25.json'
REPORT = HERE / 'root-design-assent-guard.v1.json'
assert not REPORT.exists()
spec = importlib.util.spec_from_file_location('actual_binder', SOURCE)
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
original = json.loads(ASSENT.read_text())
review_spec = {'reviewPath': original['independentReview']['path'], 'reviewSha256': original['independentReview']['sha256']}
cases = [
    ('actual-assent', None, None),
    ('explicit-refusal', 'rootDesignAssent', False),
    ('missing-assent', 'rootDesignAssent', None),
    ('other-subject', 'subjectManifestSha256', '0' * 64),
    ('other-session', 'actualSessionId', 'other'),
    ('other-review', 'independentReview', {'path': 'other', 'sha256': '0' * 64}),
    ('unresolved-must', 'unresolvedRootMustIssues', ['REQUIRED']),
    ('unresolved-should', 'unresolvedRootShouldIssues', ['REQUIRED']),
    ('missing-must-account', 'unresolvedRootMustIssues', None),
    ('missing-should-account', 'unresolvedRootShouldIssues', None),
]
rows = []
for name, key, value in cases:
    assent = copy.deepcopy(original)
    if key is not None:
        if value is None:
            assent.pop(key)
        else:
            assent[key] = value
    try:
        M.require_root_design_assent(assent, original['subjectManifestSha256'], review_spec, original['actualSessionId'])
        observed, detail = 'ADMIT', None
    except AssertionError as error:
        observed, detail = 'REFUSE', str(error)
    expected = 'ADMIT' if key is None else 'REFUSE'
    rows.append(dict(name=name, observed=observed, expected=expected, detail=detail, passed=observed == expected))
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
report = {'standing': 'Scoped root design receipt binding controls only; no blind or application assent.', 'sourceSha256': sha(SOURCE), 'controlSha256': sha(Path(__file__)), 'actualAssentSha256': sha(ASSENT), 'checks': rows, 'passed': all(row['passed'] for row in rows)}
REPORT.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
raise SystemExit(not report['passed'])
