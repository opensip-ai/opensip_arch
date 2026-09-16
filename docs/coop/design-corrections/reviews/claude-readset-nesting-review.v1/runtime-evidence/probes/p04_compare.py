"""p04: compare p03-source (corrected identity model) with p03-before-model (only the identity model reverted) and the
p02 checker results; state every expectation and whether it holds. Also re-hash the captured corrected files and
dependencies against p00, and root's live corrected files against the capture (drift report only; never read for
judgement). Output: receipts/p04-compare.json.
"""
import hashlib, json, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-readset-nesting-review.v1')
SRC = Path('/tmp/opensip-design-corrections/consumer24-corrections-successor.v1/source')
R = BASE / 'receipts'
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
after = json.loads((R / 'p03-source.json').read_text())
before = json.loads((R / 'p03-before-model.json').read_text())
p00 = json.loads((R / 'p00-capture.json').read_text())
VCS = ('.git', '.hg', '.svn', '.jj')
has_vcs = lambda p: any(s in VCS for s in p.split('/'))
LISTED = ('node_modules/left-pad/', 'node_modules/@scope/util/', 'node_modules/lib/', 'packages/lib/')
checks = {}


def ck(name, ok, detail=None):
    checks[name] = {'ok': bool(ok), **({'detail': detail} if detail is not None else {})}


A = {r['path']: r for r in after['matrix']}
B = {r['path']: r for r in before['matrix']}
ck('models-loaded-from-the-intended-trees', after['loadedModelFile'].startswith(str(BASE / 'work/source')) and
   before['loadedModelFile'].startswith(str(BASE / 'work/hybrid-p03')) and after['modelSha256'] != before['modelSha256'],
   [after['loadedModelFile'], before['loadedModelFile']])
ck('same-matrix', set(A) == set(B), len(A))
ck('after: every path with an exact VCS segment at any depth is a fault, with or without a read set',
   all(A[p]['faultWithLayout'] and A[p]['faultWithoutLayout'] for p in A if has_vcs(p)), [p for p in A if has_vcs(p) and not A[p]['faultWithLayout']])
ck('after: lookalikes and ordinary package reads stay lawful under the read set',
   all(not A[p]['faultWithLayout'] for p in A if A[p]['kind'] in ('lookalike-in-listed-package', 'first-party-lookalike', 'ordinary')),
   [p for p in A if A[p]['kind'] in ('lookalike-in-listed-package', 'first-party-lookalike', 'ordinary') and A[p]['faultWithLayout']])
ck('after: unlisted package and Cargo build output remain faults', all(A[p]['faultWithLayout'] for p in A if A[p]['kind'] in ('unlisted-package', 'cargo-build-output')))
newly = sorted(p for p in A if A[p]['faultWithLayout'] and not B[p]['faultWithLayout'])
relaxed = sorted(p for p in A if B[p]['faultWithLayout'] and not A[p]['faultWithLayout'])
expected_new = sorted(p for p in A if has_vcs(p) and p.startswith(LISTED) and B[p]['discovery'] is not None and B[p]['discovery'][1] == 'dependency-tree')
ck('no expansion: nothing lawful after that was a fault before', relaxed == [], relaxed)
ck('the only change with a read set is VCS-segment paths under a listed dependency package prefix', newly == expected_new,
   {'newly': newly, 'expected': expected_new})
ck('without any read set the two models agree on every path', all(A[p]['faultWithoutLayout'] == B[p]['faultWithoutLayout'] for p in A),
   [p for p in A if A[p]['faultWithoutLayout'] != B[p]['faultWithoutLayout']])
ck('discovery instrument unchanged and still reports the outermost pruned tree',
   all(A[p]['discovery'] == B[p]['discovery'] for p in A)
   and A['node_modules/left-pad/.git/HEAD']['discovery'] == ['node_modules', 'dependency-tree']
   and A['sub/.git/x']['discovery'] == ['sub/.git', 'vcs-tree'])
ck('observation: an unlisted nested dependency under a listed parent is lawful in both models (pre-existing, unchanged)',
   not A['node_modules/left-pad/node_modules/evil/index.js']['faultWithLayout'] and not B['node_modules/left-pad/node_modules/evil/index.js']['faultWithLayout'])
ck('lookalike case sensitivity: .GIT and .Git are not VCS segments in either model (exact-segment law)',
   not A['node_modules/left-pad/.GIT/HEAD']['faultWithLayout'] and not A['node_modules/left-pad/.Git/HEAD']['faultWithLayout'])

RA = {r['path']: r for r in after['realRuns']}
RB = {r['path']: r for r in before['realRuns']}
vcs_runs = [p for p in RA if has_vcs(p)]
lawful_runs = [p for p in RA if not has_vcs(p)]
ck('real Runs after: nested VCS rows refuse at the close_run join naming exactly that path',
   all(RA[p]['outcome'] == 'REFUSE' and RA[p]['reason'] == 'SNAPSHOT_PRUNED_TREE_NOT_A_READ:' + p for p in vcs_runs), {p: RA[p].get('reason') for p in vcs_runs})
ck('real Runs before: the same nested VCS rows were admitted (defect reproduced for .svn, .jj, scoped .git and a .git file)',
   all(RB[p]['outcome'] == 'RETURNED' and RB[p]['inventoryHasPath'] for p in vcs_runs), {p: RB[p]['outcome'] for p in vcs_runs})
ck('real Runs: lawful package reads close in both models with identical runIds (no current valid fixture ID change)',
   all(RA[p]['outcome'] == RB[p]['outcome'] == 'RETURNED' and RA[p]['runId'] == RB[p]['runId'] == RA[p]['closeRunId'] and RA[p]['inventoryHasPath']
       for p in lawful_runs), {p: (RA[p].get('runId'), RB[p].get('runId')) for p in lawful_runs})

for name in ('source-a4', 'before-model-a4', 'source-all', 'semantic-source'):
    p = R / ('p02-%s.json' % name)
    if p.exists():
        d = json.loads(p.read_text())
        ck('p02 %s expectation' % name, d['expectationMet'], {k: d.get(k) for k in ('exit', 'total', 'passed', 'failedCases', 'count', 'blocked', 'faults')})
    else:
        ck('p02 %s expectation' % name, False, 'missing')

captured = {r['path']: r['captured'] for r in p00['correctedFiles']}
ck('captured corrected files unchanged in this runtime', all(sha(BASE / 'work/source' / p) == h for p, h in captured.items()))
ck('captured dependencies unchanged in this runtime', all(sha(BASE / 'work/source' / p) == v['captured'] for p, v in p00['dependencies'].items()))
drift = {p: sha(SRC / p) != h for p, h in captured.items()}
drift.update({p: sha(SRC / p) != v['captured'] for p, v in p00['dependencies'].items()})
out = {'checks': checks, 'allOk': all(c['ok'] for c in checks.values()), 'liveSourceDriftSinceCapture': drift}
(R / 'p04-compare.json').write_text(json.dumps(out, indent=1, default=str) + '\n')
print(json.dumps(out, indent=1, default=str)[:15000])
sys.exit(0 if out['allOk'] else 1)
