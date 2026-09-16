"""PROBE L (v27) — run the package's four portable probes MYSELF against snapshot27, and
independently audit their outputs against the shipped retained copies.

This tests F-03 (queries regenerable, blind13 dependency gone), F-08 (effective-edition fields
asserted), F-09 (mixed-universe refusal code) by execution, not by reading retained JSON.
Outputs go to my own tree; the frozen package and snapshot are never written to.
"""
import hashlib, json, os, shutil, subprocess, time

SRC = '/tmp/opensip-design-corrections/candidate-subject.v27'
PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v4'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v27'
OUT = os.path.join(BASE, 'receipts')
WORK = os.path.join(BASE, 'disposable/pkgprobes')
PY = '/tmp/opensip-architecture-review-env/bin/python'
os.makedirs(OUT, exist_ok=True)
if os.path.isdir(WORK):
    shutil.rmtree(WORK)
os.makedirs(WORK)

JOBS = [
    ('check-author-query.py', ['--source', SRC, '--package', PKG, '--out', os.path.join(WORK, 'query')]),
    ('check-author-properties.py', ['--source', SRC, '--package', PKG, '--out', os.path.join(WORK, 'props')]),
    # assess-author-query.py consumes the query probe's OUTPUT: --input/--out. My first run
    # passed --source/--package and exited 2 on argparse; that was my probe defect, preserved.
    ('assess-author-query.py', ['--input', os.path.join(WORK, 'query'), '--out', os.path.join(WORK, 'assess')]),
    ('probe-mixed-universe-view.py', ['--source', SRC, '--package', PKG, '--out', os.path.join(WORK, 'mixed')]),
]
rows = []
for name, args in JOBS:
    p = os.path.join(PKG, name)
    t0 = time.time()
    r = subprocess.run([PY, '-I', '-B', p] + args, capture_output=True, text=True, timeout=3600)
    rows.append({'probe': name, 'returncode': r.returncode, 'seconds': round(time.time() - t0, 1),
                 'stdoutTail': (r.stdout or '')[-3000:], 'stderrTail': (r.stderr or '')[-1200:]})
    print('\n' + '=' * 92)
    print('%s  rc=%d  %.1fs' % (name, r.returncode, time.time() - t0))
    print('=' * 92)
    print((r.stdout or '')[-3000:])
    if r.returncode:
        print('--- stderr ---')
        print((r.stderr or '')[-1500:])

# --- compare my regenerated query outputs with the shipped retained copies ---
cmp_rows = []
qdir = os.path.join(WORK, 'query')
if os.path.isdir(qdir):
    for n in sorted(os.listdir(qdir)):
        mine = os.path.join(qdir, n)
        shipped = os.path.join(PKG, 'query-checks1', n)
        row = {'file': n, 'shippedExists': os.path.isfile(shipped)}
        if row['shippedExists']:
            a = hashlib.sha256(open(mine, 'rb').read()).hexdigest()
            b = hashlib.sha256(open(shipped, 'rb').read()).hexdigest()
            row['sameBytes'] = a == b
            if not row['sameBytes']:
                ja, jb = json.load(open(mine)), json.load(open(shipped))
                row['sameSemantics'] = ja == jb
                if not row.get('sameSemantics'):
                    ka = ja if isinstance(ja, dict) else {}
                    kb = jb if isinstance(jb, dict) else {}
                    row['keysDiffering'] = sorted(k for k in set(ka) | set(kb) if ka.get(k) != kb.get(k))
                    row['mineResult'] = ka.get('result')
                    row['shippedResult'] = kb.get('result')
                    row['mineCode'] = ka.get('code')
                    row['shippedCode'] = kb.get('code')
        cmp_rows.append(row)
        print('%-22s shipped=%-5s sameBytes=%-5s sameSemantics=%s %s' % (
            n, row['shippedExists'], row.get('sameBytes'), row.get('sameSemantics', ''),
            row.get('keysDiffering', '')))

res = {'standing': 'I executed the package probes; outputs written only under my own tree',
       'jobs': rows, 'queryComparison': cmp_rows,
       'allProbesExitZero': all(x['returncode'] == 0 for x in rows)}
json.dump(res, open(os.path.join(OUT, 'pL-pkgprobes.json'), 'w'), indent=1)
print('\nall four probes exit 0:', res['allProbesExitZero'])
