from pathlib import Path
import os, json, hashlib, subprocess
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK') == '1'
F = Path(__file__).parent
Q = Path('/tmp/opensip-implementation/reviews/codex-cli-doctor-guard-repair-r2')
W = Path('/Users/sb/code/opensip-ai/opensip-doctor-gate-repair')
s = json.loads((Q / 'subject.json').read_text())
v = json.loads((Q / 'review.json').read_text())
a = json.loads((F / 'lead-assent-r2.json').read_text())
sha = hashlib.sha256((Q / 'subject.json').read_bytes()).hexdigest()
assert v['verdict'] == 'ACCEPT-UNIT' and not v['requiredFindings']
assert v['subjectManifestSha256'] == sha == a['subjectManifestSha256'] and a['rootSubstantiveAssent']
def git(*args):
    return subprocess.check_output(['/usr/bin/git', '-c', 'user.name=sfbreen', '-c', 'user.email=sfbreen@hotmail.com', *args], cwd=W, text=True).strip()
path = 'apps/cli/tests/doctor_tests.rs'
assert git('rev-parse', 'HEAD') == s['productParent']
assert git('diff', '--name-only', 'HEAD') == path and not git('ls-files', '--others', '--exclude-standard')
assert (W / path).read_bytes() == (Q / 'subject/product' / path).read_bytes()
git('add', '--', path)
assert git('diff', '--cached', '--name-only') == path
git('commit', '-m', 'Bind the doctor source guard to accepted feature resolution and lawful source sites.')
code = git('rev-parse', 'HEAD')
assert git('rev-parse', 'HEAD^') == s['productParent'] and not git('status', '--porcelain')
report = dict(unit=a['unit'], code=code, parent=s['productParent'], subjectManifestSha256=sha,
    changedPaths=[path], newPaths=[], rootSubstantiveAssent=True, mainIntegrated=False, pushed=False,
    productQualification=False)
(F / 'product-code-r2.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
