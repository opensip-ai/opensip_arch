"""Runner for the pinned reference launchers under the required interpreter.
Runs each checker IN PLACE under the frozen snapshot (read-only) with
/tmp/opensip-architecture-review-env/bin/python -I -B. Never bypasses a pin gate."""
import json, os, subprocess, sys, time

PY = '/tmp/opensip-architecture-review-env/bin/python'
ROOT = '/tmp/opensip-design-corrections/candidate-subject.v26'
OUTDIR = '/tmp/opensip-design-corrections/claude-independent-design.v26/receipts'
os.makedirs(OUTDIR, exist_ok=True)

TARGETS = sys.argv[1:] or [
    'docs/coop/design-corrections/foundation/check-current-profile.v3.py',
    'docs/coop/design-corrections/foundation/check-candidate-replay.v3.py',
    'docs/coop/design-corrections/foundation/check-composition.v3.py',
    'docs/coop/design-corrections/foundation/check-execution-replay.v3.py',
    'docs/coop/design-corrections/foundation/check-policy-derivation.v3.py',
    'docs/coop/design-corrections/foundation/check-evaluator-faults.v3.py',
    'docs/coop/design-corrections/workflows/check-comparison-knowledge.v3.py',
]

results = []
for rel in TARGETS:
    p = os.path.join(ROOT, rel)
    t0 = time.time()
    r = subprocess.run([PY, '-I', '-B', p], capture_output=True, text=True, cwd=os.path.dirname(p), timeout=1800)
    dt = round(time.time() - t0, 1)
    tail_out = r.stdout[-1500:]
    tail_err = r.stderr[-2500:]
    results.append({'checker': rel, 'returncode': r.returncode, 'seconds': dt,
                    'stdout_bytes': len(r.stdout), 'stderr_bytes': len(r.stderr),
                    'stdout_tail': tail_out, 'stderr_tail': tail_err})
    print('=== %s rc=%d %.1fs out=%d err=%d' % (rel.rsplit('/', 1)[-1], r.returncode, dt, len(r.stdout), len(r.stderr)))
    if r.returncode != 0:
        print('--- stderr tail ---')
        print(tail_err[-1800:])

json.dump(results, open(os.path.join(OUTDIR, 'pinned-run-%d.json' % int(time.time())), 'w'), indent=1)
