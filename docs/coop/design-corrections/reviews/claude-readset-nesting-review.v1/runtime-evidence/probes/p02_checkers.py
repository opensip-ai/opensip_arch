"""p02 <variant>: focused checkers over the captured copy (never the live successor source).

  source-a4        check-native-consumer24-corrections.v1.py --only A4 over work/source
  source-all       the same checker, every section, over work/source
  before-model-a4  --only A4 over work/hybrid-p02: a regular copy of work/source with ONLY
                   foundation/identity-model.v3.py replaced by root's retained before-file
  semantic-source  check-semantic-replay.v3.py over work/source (retained run-termination goldens pin runIds)
Writes receipts/p02-<variant>.json (never overwritten).
"""
import hashlib, json, shutil, subprocess, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-readset-nesting-review.v1')
ROOT = Path('/tmp/opensip-design-corrections/root-source39-readset-nesting.v1')
PY = '/tmp/opensip-architecture-review-env/bin/python'
MODEL = 'docs/coop/design-corrections/foundation/identity-model.v3.py'
CHECK = 'docs/coop/design-corrections/foundation/check-native-consumer24-corrections.v1.py'
SEM = 'docs/coop/design-corrections/foundation/check-semantic-replay.v3.py'
NEW_CASES = {'listed-package-read-allowance-never-overrides-nested-vcs', 'nested-vcs-lookalike-segments-remain-lawful-package-reads',
             'real-run-package-vcs-lookalike-remains-lawful', 'real-run-refuses-listed-package-nested-git-metadata',
             'real-run-refuses-listed-package-nested-mercurial-metadata'}
EXPECT_FAIL_BEFORE = {'listed-package-read-allowance-never-overrides-nested-vcs', 'real-run-refuses-listed-package-nested-git-metadata',
                      'real-run-refuses-listed-package-nested-mercurial-metadata'}
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
variant = sys.argv[1]
out_path = BASE / 'receipts' / ('p02-%s.json' % variant)
if out_path.exists():
    raise SystemExit('refusing to overwrite ' + str(out_path))
tree = BASE / 'work' / 'source'
out = {'variant': variant}
if variant == 'before-model-a4':
    tree = BASE / 'work' / 'hybrid-p02'
    shutil.copytree(BASE / 'work' / 'source' / 'docs', tree / 'docs', copy_function=shutil.copy2)
    shutil.copy2(ROOT / 'before-files' / MODEL, tree / MODEL)
    out['hybridModelSha256'] = sha(tree / MODEL)
out['tree'] = str(tree)
out['modelSha256'] = sha(tree / MODEL)
out['checkerSha256'] = sha(tree / CHECK)
if variant == 'semantic-source':
    rdir = BASE / 'receipts' / 'p02-semantic-source-report'
    p = subprocess.run([PY, '-I', '-B', str(tree / SEM), '--output', str(rdir)], capture_output=True, text=True, timeout=3000, cwd=str(BASE))
    rep = json.loads((rdir / 'grok-native-replay.v1.json').read_text())
    out.update(exit=p.returncode, passed=rep['passed'], count=rep['count'], blocked=rep['blocked'],
               faults={c['case']: c.get('faults') for c in rep['checks'] if c.get('faults')},
               goldenRunIds={c['case']: c['termination'].get('runId') for c in rep['checks'] if isinstance(c.get('termination'), dict)},
               stderrTail=p.stderr[-1500:])
    ok = p.returncode == 0 and rep['passed']
else:
    args = [PY, '-I', '-B', str(tree / CHECK)] + (['--only', 'A4'] if variant.endswith('-a4') else [])
    p = subprocess.run(args, capture_output=True, text=True, timeout=3000, cwd=str(BASE))
    rep = json.loads(p.stdout)
    failed = {r['case'] for r in rep['failed']}
    out.update(exit=p.returncode, total=rep['total'], passed=rep['passed'], failedCases=sorted(failed),
               a4Rows=[{k: r.get(k) for k in ('case', 'ok', 'detail')} for r in rep['rows'] if r['item'] == 'A4'],
               newCasesPresent=sorted(NEW_CASES & {r['case'] for r in rep['rows']}), stderrTail=p.stderr[-1500:])
    if variant == 'before-model-a4':
        ok = failed == EXPECT_FAIL_BEFORE
    else:
        ok = p.returncode == 0 and not failed and NEW_CASES <= {r['case'] for r in rep['rows']}
out['expectationMet'] = ok
out_path.write_text(json.dumps(out, indent=1, default=str) + '\n')
print(json.dumps({k: v for k, v in out.items() if k not in ('a4Rows', 'goldenRunIds')}, indent=1, default=str)[:8000])
sys.exit(0 if ok else 1)
