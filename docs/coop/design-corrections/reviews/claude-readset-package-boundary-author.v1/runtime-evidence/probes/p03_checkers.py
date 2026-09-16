"""p03 <variant>: focused checkers over this runtime's trees (never the root successor or the prior review source).

  edited-a4           check-native-consumer24-corrections.v1.py --only A4 over work/source
  edited-all          the same checker, all sections, over work/source
  semantic-edited     check-semantic-replay.v3.py over work/source (retained goldens pin runIds)
  baseline-model-a4   --only A4 over work/hybrid-p03-baseline-model (ONLY identity-model.v3.py restored to baseline);
                      expected to fail exactly the new negative nested-custody controls
  substring-mutant-a4 --only A4 over work/hybrid-p03-substring (the edited model with the exact-segment test replaced
                      by a substring test); expected to fail exactly the lookalike controls
Writes receipts/p03-<variant>.json (never overwritten).
"""
import hashlib, json, shutil, subprocess, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-readset-package-boundary-author.v1')
PRIOR = Path('/tmp/opensip-design-corrections/claude-readset-nesting-review.v1/work/source')
PY = '/tmp/opensip-architecture-review-env/bin/python'
MODEL = 'docs/coop/design-corrections/foundation/identity-model.v3.py'
CHECK = 'docs/coop/design-corrections/foundation/check-native-consumer24-corrections.v1.py'
SEM = 'docs/coop/design-corrections/foundation/check-semantic-replay.v3.py'
NEW_NEGATIVE = {'an-enclosing-listed-package-never-authorizes-a-nested-installed-package',
                'a-nested-package-row-does-not-authorize-deeper-or-sibling-nested-packages',
                'a-nested-scoped-package-needs-its-own-row',
                'a-nested-package-below-a-listed-store-realpath-needs-its-own-row',
                'a-first-party-realpath-keeps-first-party-custody-and-its-nested-dependency-needs-a-row',
                'real-run-refuses-an-unlisted-nested-package-under-a-listed-package',
                'real-run-refuses-an-unlisted-nested-scoped-package-under-a-listed-scoped-package'}
LOOKALIKE = {'lookalike-and-case-variant-segments-are-no-nested-package-boundary', 'real-run-closes-with-a-nested-lookalike-segment'}
SUBSTRING_OLD = "    return not any(segment in dependency_segments for segment in path[len(package)+1:].split('/'))\n"
SUBSTRING_NEW = "    return not any(segment in path[len(package)+1:] for segment in dependency_segments)\n"
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
variant = sys.argv[1]
out_path = BASE / 'receipts' / ('p03-%s.json' % variant)
if out_path.exists():
    raise SystemExit('refusing to overwrite ' + str(out_path))
tree = BASE / 'work' / 'source'
out = {'variant': variant}
if variant == 'baseline-model-a4':
    tree = BASE / 'work' / 'hybrid-p03-baseline-model'
    shutil.copytree(BASE / 'work' / 'source' / 'docs', tree / 'docs', copy_function=shutil.copy2)
    shutil.copy2(PRIOR / MODEL, tree / MODEL)
elif variant == 'substring-mutant-a4':
    tree = BASE / 'work' / 'hybrid-p03-substring'
    shutil.copytree(BASE / 'work' / 'source' / 'docs', tree / 'docs', copy_function=shutil.copy2)
    text = (tree / MODEL).read_text()
    if text.count(SUBSTRING_OLD) != 1:
        raise SystemExit('mutation anchor count %d' % text.count(SUBSTRING_OLD))
    (tree / MODEL).write_text(text.replace(SUBSTRING_OLD, SUBSTRING_NEW))
out.update(tree=str(tree), modelSha256=sha(tree / MODEL), checkerSha256=sha(tree / CHECK))
if variant == 'semantic-edited':
    rdir = BASE / 'receipts' / 'p03-semantic-edited-report'
    p = subprocess.run([PY, '-I', '-B', str(tree / SEM), '--output', str(rdir)], capture_output=True, text=True, timeout=3000, cwd=str(BASE))
    rep = json.loads((rdir / 'grok-native-replay.v1.json').read_text())
    out.update(exit=p.returncode, passed=rep['passed'], count=rep['count'], blocked=rep['blocked'],
               faults={c['case']: c.get('faults') for c in rep['checks'] if c.get('faults')}, stderrTail=p.stderr[-1500:])
    ok = p.returncode == 0 and rep['passed']
else:
    args = [PY, '-I', '-B', str(tree / CHECK)] + (['--only', 'A4'] if variant.endswith('-a4') else [])
    p = subprocess.run(args, capture_output=True, text=True, timeout=3000, cwd=str(BASE))
    try:
        rep = json.loads(p.stdout)
    except ValueError:
        rep = {'total': None, 'passed': None, 'failed': [{'case': 'unparsable-output', 'detail': p.stdout[-2000:]}], 'rows': []}
    failed = {r['case'] for r in rep['failed']}
    out.update(exit=p.returncode, total=rep['total'], passed=rep['passed'], failedCases=sorted(failed),
               failedDetails={r['case']: str(r.get('detail'))[:600] for r in rep['failed']},
               a4Rows=[{k: r.get(k) for k in ('case', 'ok', 'detail')} for r in rep['rows'] if r['item'] == 'A4'],
               stderrTail=p.stderr[-2000:])
    if variant == 'baseline-model-a4':
        ok = failed == NEW_NEGATIVE
    elif variant == 'substring-mutant-a4':
        ok = failed == LOOKALIKE
    else:
        ok = p.returncode == 0 and not failed and (NEW_NEGATIVE | LOOKALIKE) <= {r['case'] for r in rep['rows']}
out['expectationMet'] = ok
out_path.write_text(json.dumps(out, indent=1, default=str) + '\n')
print(json.dumps({k: v for k, v in out.items() if k != 'a4Rows'}, indent=1, default=str)[:10000])
sys.exit(0 if ok else 1)
