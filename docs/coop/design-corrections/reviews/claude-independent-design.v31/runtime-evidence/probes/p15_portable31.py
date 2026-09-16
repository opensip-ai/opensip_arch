"""PROBE 15 (v31) — reproduce the portable constructors against frozen SOURCE31 in a fresh
arbitrary directory outside every input tree, and MEASURE whether the freshly built exports equal
the preserved package7 bytes. The v27 'one differing unreferenced blob' result is historical; this
measures the current state rather than assuming it."""
import hashlib, json, os, subprocess, tempfile

SRC = '/tmp/opensip-design-corrections/candidate-subject.v31'
PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v7'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v31/receipts'
PY = '/tmp/opensip-architecture-review-env/bin/python'
ARB = tempfile.mkdtemp(prefix='indep31-arbitrary-')
DEST = os.path.join(ARB, 'deep', 'nested', 'elsewhere')
os.makedirs(DEST)
R = {'arbitraryOutputRoot': DEST,
     'standing': 'independent from-scratch construction against frozen source31; shipped exports not consulted'}
print('arbitrary output root:', DEST)

BUILDS = [
    ('build-checkpoint3.py', 'a-checkpoint3', [], 'checkpoint3'),
    ('build-normalized-examples6.py', 'b-normalized', [], 'normalized-examples6'),
    ('build-rust-selection-examples.py', 'c-rust-selection', [], 'rust-selection-examples1'),
    ('build-binding-controls.py', 'e-binding-controls', [], 'binding-controls'),
]
builds = []
for script, sub, extra, shipped in BUILDS:
    dest = os.path.join(DEST, sub)
    cmd = [PY, '-I', '-B', os.path.join(PKG, script),
           '--source', SRC, '--package', PKG, '--out', dest] + extra
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
    builds.append({'script': script, 'returncode': r.returncode,
                   'stdoutTail': (r.stdout or '')[-500:], 'stderrTail': (r.stderr or '')[-700:]})
    print('%-36s rc=%d %s' % (script, r.returncode, (r.stdout or '').strip().splitlines()[-1:][:1]))
    if r.returncode:
        print('   stderr:', (r.stderr or '')[-600:])

# semantic controls need the freshly built positive
dctrl = os.path.join(DEST, 'd-controls')
cmd = [PY, '-I', '-B', os.path.join(PKG, 'build-semantic-controls.py'),
       '--source', SRC, '--package', PKG, '--out', dctrl,
       '--positive', os.path.join(DEST, 'a-checkpoint3', 'checkpoint3')]
r = subprocess.run(cmd, capture_output=True, text=True, timeout=3600)
builds.append({'script': 'build-semantic-controls.py', 'returncode': r.returncode,
               'stdoutTail': (r.stdout or '')[-500:], 'stderrTail': (r.stderr or '')[-700:]})
print('%-36s rc=%d' % ('build-semantic-controls.py', r.returncode))
if r.returncode:
    print('   stderr:', (r.stderr or '')[-700:])
R['builds'] = builds
R['allBuildsSucceeded'] = all(b['returncode'] == 0 for b in builds)
print('\nall builds succeeded:', R['allBuildsSucceeded'])

# ---- compare every produced store against the preserved package bytes ----
PAIRS = [('a-checkpoint3/checkpoint3', 'checkpoint3'),
         ('b-normalized/normalized-examples6', 'normalized-examples6'),
         ('c-rust-selection/rust-selection-examples1', 'rust-selection-examples1'),
         ('d-controls/semantic-controls1', 'semantic-controls1'),
         ('e-binding-controls', 'binding-controls')]
comp = []
for freshsub, shipsub in PAIRS:
    fdir = os.path.join(DEST, freshsub)
    sdir = os.path.join(PKG, shipsub)
    if not os.path.isdir(fdir):
        comp.append({'group': shipsub, 'error': 'fresh dir missing'})
        continue
    for n in sorted(os.listdir(fdir)):
        if not n.endswith('.json'):
            continue
        fp, sp = os.path.join(fdir, n), os.path.join(sdir, n)
        row = {'group': shipsub, 'file': n,
               'freshSha256': hashlib.sha256(open(fp, 'rb').read()).hexdigest(),
               'shippedPresent': os.path.isfile(sp)}
        if row['shippedPresent']:
            row['shippedSha256'] = hashlib.sha256(open(sp, 'rb').read()).hexdigest()
            row['byteIdentical'] = row['freshSha256'] == row['shippedSha256']
            row['freshBytes'] = os.path.getsize(fp)
            row['shippedBytes'] = os.path.getsize(sp)
        comp.append(row)
R['comparison'] = comp
stores = [c for c in comp if c.get('file', '').endswith('.store.json') and c.get('shippedPresent')]
R['storeFilesCompared'] = len(stores)
R['storeFilesByteIdentical'] = sum(1 for c in stores if c.get('byteIdentical'))
print('\nstore files compared: %d | byte-identical: %d' % (R['storeFilesCompared'],
                                                           R['storeFilesByteIdentical']))
for c in comp:
    if c.get('shippedPresent') and not c.get('byteIdentical'):
        print('   DIFFERS %-28s %-34s fresh=%d shipped=%d' % (c['group'], c['file'],
                                                              c['freshBytes'], c['shippedBytes']))
# claims/runIds
same_ids = True
for freshsub, shipsub in PAIRS:
    fc = os.path.join(DEST, freshsub, 'claims.json')
    sc = os.path.join(PKG, shipsub, 'claims.json')
    if os.path.isfile(fc) and os.path.isfile(sc):
        a = {x['name']: x['runId'] for x in json.load(open(fc))}
        b = {x['name']: x['runId'] for x in json.load(open(sc))}
        if a != b:
            same_ids = False
            R.setdefault('runIdDifferences', []).append({'group': shipsub, 'fresh': a, 'shipped': b})
R['claimRunIdsIdenticalEverywhere'] = same_ids
print('claimed runIds identical to the preserved package everywhere:', same_ids)
R['allStoresByteIdentical'] = R['storeFilesCompared'] == R['storeFilesByteIdentical']
print('ALL stores byte-identical (v27 blob-difference no longer present):',
      R['allStoresByteIdentical'])
json.dump(R, open(os.path.join(OUT, 'p15-portable31.json'), 'w'), indent=1)
print('\nwrote p15-portable31.json')
