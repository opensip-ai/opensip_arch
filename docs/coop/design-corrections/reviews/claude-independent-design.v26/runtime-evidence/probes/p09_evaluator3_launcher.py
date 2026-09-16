"""Probe 09 — run the current SOURCE-PINNED evaluator3 launcher in place against the
frozen snapshot. It writes only into the --out directory I supply, so the snapshot is
not mutated. Its own pin gate is left exactly as authored."""
import hashlib, json, os, shutil, subprocess, time

SRC = '/tmp/opensip-design-corrections/candidate-subject.v26'
PY = '/tmp/opensip-architecture-review-env/bin/python'
LAUNCHER = os.path.join(SRC, 'docs/coop/design-corrections/foundation/run-evaluator3-checks.py')
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v26/receipts/evaluator3-launcher'
if os.path.isdir(OUT):
    shutil.rmtree(OUT)

# record the launcher and its pin ledger identity before running
led = os.path.join(SRC, 'docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json')
print('launcher sha256 =', hashlib.sha256(open(LAUNCHER, 'rb').read()).hexdigest())
print('pin ledger sha256 =', hashlib.sha256(open(led, 'rb').read()).hexdigest())
print('pin ledger entries =', len(json.load(open(led))['files']))

t0 = time.time()
r = subprocess.run([PY, '-I', '-B', LAUNCHER, '--out', OUT], capture_output=True, text=True, timeout=3600)
print('rc=%d  %.1fs' % (r.returncode, time.time() - t0))
print(r.stdout[-3000:])
if r.stderr:
    print('--- stderr ---')
    print(r.stderr[-2000:])
rep = os.path.join(OUT, 'report.json')
if os.path.isfile(rep):
    d = json.load(open(rep))
    print('sourcePinsValid=%s passed=%s changedOrMissing=%d checks=%d' %
          (d['sourcePinsValid'], d['passed'], len(d['changedOrMissing']), len(d['checks'])))
    for c in d['checks']:
        print('   %-28s exit=%s timedOut=%s' % (c['name'], c['exitCode'], c['timedOut']))
