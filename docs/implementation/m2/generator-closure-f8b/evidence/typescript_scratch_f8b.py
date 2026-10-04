"""F8b step 8 (scratch only): replay check_typescript.py's selection and pin checks with F8b's
review and assent served in memory (SCRATCH-F8B/ paths), as verify_scratch_f8b.py does.

Part 1 runs the checkout's real check_typescript.check(). The only change is that the
design_preflight module it loads gets the in-memory overlay. Expected outcome on this Mac:
- verify_design passes;
- the lane registry is selected exactly once by an accepted design unit;
- the registry closes and is sorted;
- check() then refuses at the first tools/typescript-boundary/node_modules pin. That tree
  needs esbuild 0.28.2, which is not in the offline npm cache, so no lane child starts.
  This is unchanged from base and is disclosed, not claimed.
Part 2 checks the registry's 12 tracked rows with check_typescript's own pinned() helper,
plus its two trusted-entry-point comparisons (check_typescript.py and verify_design.py).
Usage: typescript_scratch_f8b.py CHECKOUT"""
import argparse, hashlib, importlib.util, json, sys, types
from pathlib import Path
W = Path(sys.argv[1]).resolve(strict=True); A = Path('/Users/sb/code/opensip-ai/opensip_arch')
NODE = Path('/Users/sb/.nvm/versions/node/v24.16.0/bin/node')
D = 'docs/implementation/m2/generator-closure-f8b'
def pin(p): b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
subject, record = pin(D + '-subject.json'), pin(D + '/successor.json')
review = json.dumps({'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [], 'subjectManifestSha256': subject['sha256']}).encode()
rpin = {'path': 'SCRATCH-F8B/review.json', 'bytes': len(review), 'sha256': hashlib.sha256(review).hexdigest()}
assent = json.dumps({'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [], 'subjectManifest': subject, 'independentReview': rpin, 'acceptedSuccessor': record}).encode()
apin = {'path': 'SCRATCH-F8B/assent.json', 'bytes': len(assent), 'sha256': hashlib.sha256(assent).hexdigest()}
synthetic = {rpin['path']: review, apin['path']: assent}
binding = {'record': record, 'subjectManifest': subject, 'review': rpin, 'assent': apin}
spec = importlib.util.spec_from_file_location('ct', W / 'tools/check_typescript.py'); ct = importlib.util.module_from_spec(spec); spec.loader.exec_module(ct)
state = {'approval': None}
def overlay(m):
    real, real_verify = m.pinned_bytes, m.verify
    def pinned_bytes(root, row):
        if isinstance(row, dict) and row.get('path') in synthetic: return synthetic[row['path']]
        return real(root, row)
    def verify(architecture, lock, implementation=None):
        lock = dict(lock)
        if lock['contractSuccessors'][-1]['record']['path'] == record['path']:
            assert lock['contractSuccessors'][-1] == binding, 'bound F8b entry differs'; state['mode'] = 'bound'
        else:
            lock['contractSuccessors'] = [*lock['contractSuccessors'], binding]; state['mode'] = 'appended'
        state['approval'] = real_verify(architecture, lock, implementation)
        return state['approval']
    m.pinned_bytes, m.verify = pinned_bytes, verify
def sffl(name, path, *a, **k):
    s = importlib.util.spec_from_file_location(name, path, *a, **k)
    if name == 'design_preflight':
        real_exec = s.loader.exec_module
        def exec_module(module): real_exec(module); overlay(module)
        s.loader.exec_module = exec_module
    return s
ct.importlib = types.SimpleNamespace(util=types.SimpleNamespace(spec_from_file_location=sffl, module_from_spec=importlib.util.module_from_spec))
out = {'standing': 'F8b step 8 scratch replay; lane children not run (esbuild 0.28.2 unavailable offline); not a passing lane check'}
try:
    ct.check(argparse.Namespace(root=W, architecture=A, node=NODE, lane=None))
    out['check'] = {'completed': True}
except (ValueError, OSError) as exc:
    out['check'] = {'completed': False, 'refusal': str(exc)}
out['scratchMode'] = state.get('mode')
approval = state['approval']
raw = (W / 'tools/typescript-lanes.json').read_bytes(); digest = hashlib.sha256(raw).hexdigest()
out['verifyDesignPassed'] = bool(approval and approval.get('passed'))
out['laneRegistry'] = {'bytes': len(raw), 'sha256': digest,
                       'selectedTimes': sum(1 for u in approval['contractSuccessors'] for r in u['inputs'] if r['sha256'] == digest and r['bytes'] == len(raw)) if approval else None}
registry = json.loads(raw)
tracked = [r for r in registry['files'] if '/node_modules/' not in r['path']]
results = {}
for row in tracked:
    try: ct.pinned(W, row); results[row['path']] = 'match'
    except (ValueError, OSError) as exc: results[row['path']] = 'refused: ' + str(exc)
out['trackedRows'] = {'count': len(tracked), 'allMatch': all(v == 'match' for v in results.values()), 'rows': results}
out['trustedEntryPoints'] = {rel: ct.pinned(W, next(r for r in registry['files'] if r['path'] == rel)) == (W / rel).read_bytes()
                             for rel in ('tools/check_typescript.py', 'tools/verify_design.py')}
nm = [r for r in registry['files'] if '/node_modules/' in r['path']]
out['nodeModulesRows'] = {'count': len(nm), 'present': sum(1 for r in nm if (W / r['path']).is_file())}
expected_refusal = out['check'].get('refusal', '')
out['refusedAtNodeModulesBeforeAnyChild'] = (not out['check']['completed']) and 'tools/typescript-boundary/node_modules/' in expected_refusal
out['passed'] = (out['verifyDesignPassed'] and out['laneRegistry']['selectedTimes'] == 1 and out['trackedRows']['allMatch']
                 and all(out['trustedEntryPoints'].values()) and out['refusedAtNodeModulesBeforeAnyChild'])
print(json.dumps(out, indent=1))
sys.exit(0 if out['passed'] else 1)
