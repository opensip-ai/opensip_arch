"""PROBE 17 (v31) — the separate property and mixed-universe probes, which the README says remain
outside verify-package. Executed against frozen source31 and assessed for what they do and do not
establish."""
import json, os, shutil, subprocess

SRC = '/tmp/opensip-design-corrections/candidate-subject.v31'
PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v7'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v31'
OUT = os.path.join(BASE, 'receipts')
WORK = os.path.join(BASE, 'disposable/propmixed')
PY = '/tmp/opensip-architecture-review-env/bin/python'
if os.path.isdir(WORK):
    shutil.rmtree(WORK)
os.makedirs(WORK)
R = {}

for name, args, tag in (
    ('check-author-properties.py', ['--source', SRC, '--package', PKG,
                                    '--out', os.path.join(WORK, 'props')], 'properties'),
    ('probe-mixed-universe-view.py', ['--source', SRC, '--package', PKG,
                                      '--out', os.path.join(WORK, 'mixed')], 'mixedUniverse'),
):
    r = subprocess.run([PY, '-I', '-B', os.path.join(PKG, name)] + args,
                       capture_output=True, text=True, timeout=3600)
    R[tag] = {'returncode': r.returncode, 'stdout': r.stdout[-2500:],
              'stderrTail': (r.stderr or '')[-800:]}
    print('\n=== %s rc=%d ===' % (name, r.returncode))
    print(r.stdout[-2500:])
    if r.returncode:
        print('--- stderr ---')
        print((r.stderr or '')[-900:])

try:
    p = json.loads(R['properties']['stdout'])
    R['propertiesPassed'] = p.get('passed')
    R['propertyChecks'] = p.get('checks')
except Exception:
    pass
try:
    m = json.loads(R['mixedUniverse']['stdout'])
    R['mixedRows'] = m
    R['unmergedAdmits'] = any(x.get('merged') is False and x.get('semantic') == 'ADMIT' for x in m)
    R['mergedRefuses'] = any(x.get('merged') is True and x.get('semantic') == 'REFUSE' for x in m)
    R['mergedRefusalCode'] = next((x.get('captureRefusals') for x in m if x.get('merged')), None)
except Exception:
    pass
print('\nproperties passed        :', R.get('propertiesPassed'))
print('unmerged view admits     :', R.get('unmergedAdmits'))
print('merged view refuses      :', R.get('mergedRefuses'), R.get('mergedRefusalCode'))

# compare the retained package copy of the mixed-universe probe result
ship = os.path.join(PKG, 'mixed-universe-view.probe.json')
if os.path.isfile(ship) and 'mixedRows' in R:
    shipped = json.load(open(ship))
    R['mixedMatchesRetainedCopy'] = shipped == R['mixedRows']
    print('mixed result equals the retained package copy:', R['mixedMatchesRetainedCopy'])

# confirm the README states these remain separate
rd = open(os.path.join(PKG, 'README.md'), encoding='utf-8').read()
R['readmeSaysProbesSeparate'] = bool(
    'separate' in rd.lower() and ('propert' in rd.lower() or 'mixed' in rd.lower()))
R['readmeRelevantLines'] = [l.strip() for l in rd.splitlines()
                            if any(t in l.lower() for t in ('propert', 'mixed', 'separate', 'query'))]
print('\nREADME lines on probe separation:')
for l in R['readmeRelevantLines'][:8]:
    print('   ', l[:190])

json.dump(R, open(os.path.join(OUT, 'p17-propmixed.json'), 'w'), indent=1, default=str)
print('\nwrote p17-propmixed.json')
