"""Integrate only the exact independently accepted existing CLI test path."""
from pathlib import Path
import os, json, hashlib, subprocess, shutil

assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK') == '1'
F = Path(__file__).parent
Q = Path('/tmp/opensip-implementation/reviews/codex-cli-doctor-guard-repair-r2')
P = Path('/Users/sb/code/opensip-ai/opensip')
A = P.parent / 'opensip_arch'
W = P.parent / 'opensip-doctor-gate-repair'
C = Path('/Users/sb/code/.opensip-implementation-cache/control-2026-10-06')
PRE = 'docs/implementation/m3/cli-doctor-guard-repair-r2'
RP = 'docs/implementation/m3/reviews/codex-cli-doctor-guard-repair-r2'
E = dict(os.environ, GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
for k in ['GIT_DIR', 'GIT_WORK_TREE', 'GIT_CONFIG_COUNT']:
    E.pop(k, None)

def git(root, *args):
    return subprocess.check_output(['/usr/bin/git', '-c', 'user.name=sfbreen', '-c', 'user.email=sfbreen@hotmail.com', *args], cwd=root, env=E, text=True).strip()

def pin(root, path):
    b = (root / path).read_bytes()
    return dict(path=path, bytes=len(b), sha256=hashlib.sha256(b).hexdigest())

def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + '\n')

s = json.loads((Q / 'subject.json').read_text())
v = json.loads((Q / 'review.json').read_text())
assent = json.loads((F / 'lead-assent-r2.json').read_text())
sha = pin(Q, 'subject.json')['sha256']
assert v['verdict'] == 'ACCEPT-UNIT' and not v['requiredFindings'] and not v['nonBlockingObservations']
assert v['subjectManifestSha256'] == sha == assent['subjectManifestSha256']
assert assent['rootSubstantiveAssent'] and assent['independentReview'] == pin(Q, 'review.json')
for row in s['members']:
    assert pin(Q / 'subject', row['path']) == row
assert git(P, 'rev-parse', 'HEAD') == s['productParent']
prepared = json.loads((F / 'product-code-r2.json').read_text())
assert prepared['parent'] == s['productParent'] and prepared['subjectManifestSha256'] == sha
assert git(W, 'rev-parse', 'HEAD') == prepared['code']
assert git(W, 'rev-parse', 'HEAD^') == s['productParent']
assert git(A, 'rev-parse', 'HEAD') == s['architectureParent']
assert not git(P, 'status', '--porcelain') and not git(A, 'diff', '--name-only', 'HEAD')
assert not git(A, 'diff', '--cached', '--name-only')
untracked = git(A, 'ls-files', '--others', '--exclude-standard')
lock = pin(P, 'design-lock.json')
m = json.loads((Q / 'subject/product-map.json').read_text())
assert m['newPaths'] == [] and not m['productionChanges'] and len(m['paths']) == 1
r = m['paths'][0]
path = r['path']
assert path == 'apps/cli/tests/doctor_tests.rs'
assert pin(W, path) == r == pin(Q / 'subject/product', path)
assert (P / path).read_bytes() == (Q / 'subject/parent/product' / path).read_bytes()
assert git(W, 'diff', '--name-only', 'HEAD^', 'HEAD') == path
assert not git(W, 'ls-files', '--others', '--exclude-standard')
own = json.loads((Q / 'subject/evidence/owning-r7/report.json').read_text())
assert own['allPassed'] and own['allRestored'] and len(own['mutants']) == 11 and own['source'] == r
# All current authority files, including the resolved Cargo manifests, stay exact.
for base, root in [('product', P), ('architecture', A)]:
    for file in (Q / 'subject/authority' / base).rglob('*'):
        if file.is_file():
            assert file.read_bytes() == (root / file.relative_to(Q / 'subject/authority' / base)).read_bytes()
code = git(W, 'rev-parse', 'HEAD')
assert not git(W, 'status', '--porcelain')
git(P, 'merge', '--ff-only', code)
assert not git(P, 'status', '--porcelain') and pin(P, path) == r and pin(P, 'design-lock.json') == lock
paths = []
for file in sorted((Q / 'subject').rglob('*')):
    if file.is_file():
        dest = PRE + '/subject/' + file.relative_to(Q / 'subject').as_posix()
        assert not (A / dest).exists()
        (A / dest).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(file, A / dest)
        paths.append(dest)
for name in ['REQUEST.md', 'subject.json', 'REVIEW.md', 'review.json']:
    dest = RP + '/' + name
    assert not (A / dest).exists()
    (A / dest).parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(Q / name, A / dest)
    paths.append(dest)
write(A / (RP + '/lead-assent.json'), assent)
paths.append(RP + '/lead-assent.json')
post=json.loads((Q/'subject/evidence/post-base-r2/report.json').read_text());assert post['allPassed'] and post['source']==r and post['parent']==s['productParent']
unit = dict(schemaVersion=1, unit=assent['unit'], status='ACCEPTED-UNIT', rootSubstantiveAssent=True,
    subjectManifest=pin(A, RP + '/subject.json'), subjectRoot=PRE + '/subject', subjectManifestSha256=sha,
    independentReview=pin(A, RP + '/review.json'), rootAssessment=assent['rootAssessment'],
    closedRequiredFindings=assent['closedRequiredFindings'], requiredFindings=[], nonBlockingObservations=[],
    productCode=code, changedPaths=[path], newPaths=[], productionChanges=False, newDependencies=False,
    inventoryUnchanged=236, inventorySuccessorsUnchanged=196, contractSuccessorsUnchanged=183,
    inheritedMeaningsUnchanged=138, currentDirectMeaningsUnchanged=0,
    owningValidation=dict(doctorTestsPassed=7,compiledRuntimeMutants=11,allRestored=True,postBaseUnchangedSourceTestsAndClippyPassed=True,workspaceTestsPassed=False), productQualification=False, entireProjectComplete=False)
write(A / (PRE + '-unit.json'), unit)
paths.append(PRE + '-unit.json')
check = subprocess.run(['/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14', '-I', '-B', 'tools/verify_design.py', '--architecture', str(A), '--implementation', str(P)], cwd=P, env=E, capture_output=True)
(F / 'verify-integration-r2.log').write_bytes(check.stdout + check.stderr)
assert check.returncode == 0 and json.loads(check.stdout)['passed']
git(A, 'add', '--', *paths)
assert set(git(A, 'diff', '--cached', '--name-only').splitlines()) == set(paths)
git(A, 'commit', '-m', 'Record independent acceptance of the doctor guard repair.')
arch = git(A, 'rev-parse', 'HEAD')
assert not git(A, 'diff', '--name-only', 'HEAD')
assert git(A, 'ls-files', '--others', '--exclude-standard') == untracked
report = dict(unit=assent['unit'], productCode=code, architecture=arch,
    subjectManifestSha256=sha, independentReview=pin(A, RP + '/review.json'),
    newPaths=[], changedPaths=[path], inventoryUnchanged=236, inventorySuccessorsUnchanged=196,
    contractSuccessorsUnchanged=183, currentMeaningProjection=138, verifyDesignPassed=True,
    productQualification=False, entireProjectComplete=False, pushed=False)
write(F / 'integration-r2.json', report)
state = json.loads((C / 'CURRENT-STATE.json').read_text())
state.update(productHead=code, architectureHead=arch, doctorSourceGuardRepair=report)
write(C / 'CURRENT-STATE.json', state)
print(json.dumps(report, indent=2))
