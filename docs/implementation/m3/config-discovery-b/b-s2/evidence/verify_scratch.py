"""Scratch-only: run the product's real verify_design over a lock that appends B-S2, with a
synthetic review and assent held in memory (SCRATCH-B-S2/ paths). Nothing is written to either
repository. It proves only that everything except the missing independent review and root
assent passes.

Usage: verify_scratch.py [PRODUCT_CHECKOUT] [--rev REV]
- Without --rev, the checkout's own tools/verify_design.py and design-lock.json are used, with
  the checkout as the implementation (generation and admission sources are checked).
- With --rev (for example e093e90), both files are read from that commit with read-only git
  plumbing and verify runs design-only.

It asserts that the lock passes, that the selected inventory and the inheritance projection are
unchanged, and that no bound successor already overrides IE lines 542 or 547."""
import copy, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path

args = list(sys.argv[1:])
rev = None
if '--rev' in args:
    i = args.index('--rev')
    rev = args[i + 1]
    del args[i:i + 2]
W = Path(args[0] if args else '/Users/sb/code/opensip-ai/opensip')
A = Path('/Users/sb/code/opensip-ai/opensip_arch')
B = 'docs/implementation/m3/config-discovery-b/'


def git_show(path):
    return subprocess.run(['git', '-C', str(W), 'show', '%s:%s' % (rev, path)], check=True,
                          capture_output=True).stdout


if rev:
    spec = importlib.util.spec_from_loader('vd', loader=None)
    m = importlib.util.module_from_spec(spec)
    exec(compile(git_show('tools/verify_design.py'), 'verify_design.py@' + rev, 'exec'), m.__dict__)
    base_lock = json.loads(git_show('design-lock.json'))
    implementation = None
else:
    spec = importlib.util.spec_from_file_location('vd', W / 'tools/verify_design.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    base_lock = json.loads((W / 'design-lock.json').read_text())
    implementation = W


def pin_bytes(path, b):
    return {'path': path, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def pin(p):
    return pin_bytes(p, (A / p).read_bytes())


subject, record = pin(B + 'b-s2-subject.json'), pin(B + 'b-s2/successor.json')
review = json.dumps({'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [],
                     'subjectManifestSha256': subject['sha256']}).encode()
rpin = pin_bytes('SCRATCH-B-S2/review.json', review)
assent = json.dumps({'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [],
                     'subjectManifest': subject, 'independentReview': rpin, 'acceptedSuccessor': record}).encode()
apin = pin_bytes('SCRATCH-B-S2/assent.json', assent)
synthetic = {rpin['path']: review, apin['path']: assent}
real = m.pinned_bytes


def pinned_bytes(root, row):
    if isinstance(row, dict) and row.get('path') in synthetic:
        raw = synthetic[row['path']]
        assert hashlib.sha256(raw).hexdigest() == row['sha256']
        return raw
    return real(root, row)


m.pinned_bytes = pinned_bytes
IE = 'docs/v2/contracts/product-v1/identity-and-evidence.md'
for other in base_lock['contractSuccessors']:
    rec = json.loads(m.pinned_bytes(A, other['record']))
    for entry in rec.get('passageOverrides', []) + rec.get('passageSupersessions', []):
        assert not (entry['parent']['path'] == IE and entry['selector'] in ({'line': 542}, {'line': 547})), \
            other['record']['path']
base = m.verify(A, base_lock, implementation)
lock = copy.deepcopy(base_lock)
lock['contractSuccessors'].append({'record': record, 'subjectManifest': subject, 'review': rpin, 'assent': apin})
result = m.verify(A, lock, implementation)
mine = result['contractSuccessors'][-1]
assert base['passed'] is True and result['passed'] is True and mine['selected'] == record['path']
assert result['selectedInventory'] == base['selectedInventory']
assert result['inventoryPassageInheritance'] == base['inventoryPassageInheritance']
print(json.dumps({'mode': 'rev ' + rev if rev else 'checkout ' + str(W), 'passed': True,
                  'contractSuccessors': len(result['contractSuccessors']),
                  'b-s2': {'selected': mine['selected'], 'passageOverrides': len(mine['passageOverrides']),
                           'candidates': len(mine['inputs'])},
                  'generationSources': result.get('generationSources')}, indent=1))
