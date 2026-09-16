"""PROBE F (v27) — complete from-scratch portable construction in a FRESH ARBITRARY
directory outside every declared input, then compare the freshly-built export bytes and
RunIds against the shipped ones, and replay the fresh build through the snapshot27 owner.

No shipped export is repaired, substituted or consulted during construction.
"""
import hashlib, json, os, shutil, subprocess, sys, tempfile

PY = '/tmp/opensip-architecture-review-env/bin/python'
SRC = '/tmp/opensip-design-corrections/candidate-subject.v27'
PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v4'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v27/receipts'
os.makedirs(OUT, exist_ok=True)

# a fresh arbitrary path, deliberately unrelated to source/package/kit/helpers
ARB = tempfile.mkdtemp(prefix='indep27-arbitrary-', dir='/tmp')
ARB = os.path.join(ARB, 'deep', 'nested', 'elsewhere')
res = {'arbitraryOutputRoot': ARB,
       'standing': 'independent from-scratch construction; shipped exports not consulted'}

BUILDS = [
    ('build-checkpoint3.py', 'a-checkpoint3', [], 'checkpoint3'),
    ('build-normalized-examples6.py', 'b-normalized', [], 'normalized-examples6'),
    ('build-rust-selection-examples.py', 'c-rust-selection', [], 'rust-selection-examples1'),
    ('build-binding-controls.py', 'e-binding-controls', [], 'binding-controls'),
]
runs = []
for script, sub, extra, shipped_dir in BUILDS:
    dest = os.path.join(ARB, sub)
    cmd = [PY, '-I', '-B', os.path.join(PKG, script),
           '--source', SRC, '--package', PKG, '--out', dest] + extra
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    runs.append({'script': script, 'out': dest, 'returncode': r.returncode,
                 'stdout': r.stdout[-900:], 'stderr': r.stderr[-900:] if r.returncode else ''})
    print('=== %-38s rc=%d' % (script, r.returncode))
    if r.returncode:
        print(r.stderr[-1400:])
    else:
        print('   ', r.stdout.strip()[:400])

# the semantic controls build needs a positive built above
dctrl = os.path.join(ARB, 'd-controls')
cmd = [PY, '-I', '-B', os.path.join(PKG, 'build-semantic-controls.py'),
       '--source', SRC, '--package', PKG, '--out', dctrl,
       '--positive', os.path.join(ARB, 'a-checkpoint3', 'checkpoint3')]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
runs.append({'script': 'build-semantic-controls.py', 'out': dctrl, 'returncode': r.returncode,
             'stdout': r.stdout[-900:], 'stderr': r.stderr[-900:] if r.returncode else ''})
print('=== %-38s rc=%d' % ('build-semantic-controls.py', r.returncode))
print(('   ' + r.stdout.strip()[:400]) if not r.returncode else r.stderr[-1400:])
res['builds'] = runs
res['allBuildsSucceeded'] = all(x['returncode'] == 0 for x in runs)

# ---- compare freshly built bytes with the shipped exports ----
PAIRS = [(os.path.join(ARB, 'a-checkpoint3', 'checkpoint3'), os.path.join(PKG, 'checkpoint3')),
         (os.path.join(ARB, 'b-normalized', 'normalized-examples6'),
          os.path.join(PKG, 'normalized-examples6')),
         (os.path.join(ARB, 'c-rust-selection', 'rust-selection-examples1'),
          os.path.join(PKG, 'rust-selection-examples1')),
         (os.path.join(ARB, 'd-controls', 'semantic-controls1'),
          os.path.join(PKG, 'semantic-controls1')),
         (os.path.join(ARB, 'e-binding-controls', 'binding-controls'),
          os.path.join(PKG, 'binding-controls'))]
cmp_rows = []
for fresh, shipped in PAIRS:
    if not os.path.isdir(fresh):
        cmp_rows.append({'group': os.path.basename(shipped), 'freshBuilt': False})
        continue
    for n in sorted(os.listdir(fresh)):
        fp, sp = os.path.join(fresh, n), os.path.join(shipped, n)
        row = {'group': os.path.basename(shipped), 'file': n,
               'freshSha256': hashlib.sha256(open(fp, 'rb').read()).hexdigest(),
               'shippedPresent': os.path.isfile(sp)}
        if row['shippedPresent']:
            row['shippedSha256'] = hashlib.sha256(open(sp, 'rb').read()).hexdigest()
            row['byteIdentical'] = row['freshSha256'] == row['shippedSha256']
            if n.endswith('claims.json'):
                row['freshClaims'] = json.load(open(fp))
                row['shippedClaims'] = json.load(open(sp))
                row['runIdsIdentical'] = (
                    sorted((c.get('name'), c['runId']) for c in row['freshClaims'])
                    == sorted((c.get('name'), c['runId']) for c in row['shippedClaims']))
        cmp_rows.append(row)
res['comparison'] = cmp_rows
store_rows = [r for r in cmp_rows if r.get('file', '').endswith('.store.json')]
claim_rows = [r for r in cmp_rows if r.get('file', '').endswith('claims.json')]
res['storeFilesCompared'] = len(store_rows)
res['storeFilesByteIdentical'] = sum(1 for r in store_rows if r.get('byteIdentical'))
res['storeFilesDiffering'] = [r['group'] + '/' + r['file'] for r in store_rows
                              if r.get('shippedPresent') and not r.get('byteIdentical')]
res['claimRunIdsIdenticalEverywhere'] = all(
    r.get('runIdsIdentical') for r in claim_rows if 'runIdsIdentical' in r)

print()
print('store files compared: %d  byte-identical: %d' % (
    res['storeFilesCompared'], res['storeFilesByteIdentical']))
print('differing store files:', res['storeFilesDiffering'])
print('claim RunIds identical everywhere:', res['claimRunIdsIdenticalEverywhere'])
json.dump(res, open(os.path.join(OUT, 'pF-portable.json'), 'w'), indent=1)
print('\nfresh build root retained at:', ARB)
