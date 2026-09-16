"""PROBE G (v27) — run the current source-pinned evaluator3 launcher and all 16 children
against snapshot27, preserving source pins and raw failures."""
import hashlib, json, os, shutil, subprocess, time

SRC = '/tmp/opensip-design-corrections/candidate-subject.v27'
PY = '/tmp/opensip-architecture-review-env/bin/python'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v27/receipts/evaluator3-launcher27'
if os.path.isdir(OUT):
    shutil.rmtree(OUT)

L = os.path.join(SRC, 'docs/coop/design-corrections/foundation/run-evaluator3-checks.py')
LED = os.path.join(SRC, 'docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json')
print('launcher sha256  :', hashlib.sha256(open(L, 'rb').read()).hexdigest())
print('pin ledger sha256:', hashlib.sha256(open(LED, 'rb').read()).hexdigest())
print('pin ledger rows  :', len(json.load(open(LED))['files']))

t0 = time.time()
r = subprocess.run([PY, '-I', '-B', L, '--out', OUT], capture_output=True, text=True, timeout=5400)
print('rc=%d  %.1fs' % (r.returncode, time.time() - t0))
print(r.stdout[-2500:])
if r.stderr:
    print('--- stderr ---')
    print(r.stderr[-2500:])

rep = os.path.join(OUT, 'report.json')
if os.path.isfile(rep):
    d = json.load(open(rep))
    print('sourcePinsValid=%s passed=%s changedOrMissing=%d checks=%d'
          % (d['sourcePinsValid'], d['passed'], len(d['changedOrMissing']), len(d['checks'])))
    for c in d['checks']:
        print('   %-30s exit=%-5s timedOut=%s' % (c['name'], c['exitCode'], c['timedOut']))
    if d['changedOrMissing']:
        print('CHANGED OR MISSING PINS:', d['changedOrMissing'][:10])
