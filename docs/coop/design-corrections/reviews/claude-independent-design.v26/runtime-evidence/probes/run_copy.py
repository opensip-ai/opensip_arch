"""Run report-writing checkers inside the verified disposable copy, never the frozen snapshot."""
import json, os, subprocess, sys, time

PY = '/tmp/opensip-architecture-review-env/bin/python'
KIT = '/tmp/opensip-design-corrections/claude-independent-design.v26/disposable/kit'
OUTDIR = '/tmp/opensip-design-corrections/claude-independent-design.v26/receipts'
os.makedirs(OUTDIR, exist_ok=True)
BASE = os.path.join(KIT, 'docs/coop/design-corrections')

JOBS = json.loads(sys.argv[1]) if len(sys.argv) > 1 else [
    ['native/check_native_evidence.v2.py'],
]
res = []
for job in JOBS:
    rel, args = job[0], job[1:]
    p = os.path.join(BASE, rel)
    t0 = time.time()
    r = subprocess.run([PY, '-I', '-B', p] + args, capture_output=True, text=True,
                       cwd=os.path.dirname(p), timeout=3600)
    dt = round(time.time() - t0, 1)
    res.append({'checker': rel, 'args': args, 'returncode': r.returncode, 'seconds': dt,
                'stdout_bytes': len(r.stdout), 'stderr_bytes': len(r.stderr),
                'stdout_tail': r.stdout[-2000:], 'stderr_tail': r.stderr[-3000:]})
    print('=== %s rc=%d %.1fs out=%d err=%d' % (rel, r.returncode, dt, len(r.stdout), len(r.stderr)))
    if r.returncode != 0:
        print(r.stderr[-2500:])
    else:
        print(r.stdout[-900:])
json.dump(res, open(os.path.join(OUTDIR, 'copy-run-%d.json' % int(time.time())), 'w'), indent=1)
