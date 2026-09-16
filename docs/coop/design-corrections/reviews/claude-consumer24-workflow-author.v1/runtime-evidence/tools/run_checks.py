"""Run one focused owner checker against the work tree and capture its receipt outside the tree.

usage: python -I -B run_checks.py LABEL CHECK [CHECK ...]
Each CHECK is a key of CHECKS. stdout/stderr/report go to receipts/checks/LABEL/. The checker's own file hash and the
work-tree hashes of the files it is known to exercise are recorded. Nothing is written into the work tree.
"""
import hashlib, json, os, subprocess, sys, time

RT = '/private/tmp/opensip-design-corrections/claude-consumer24-workflow-author.v1'
DC = RT + '/work/source38-work/docs/coop/design-corrections'
PY = '/tmp/opensip-architecture-review-env/bin/python'
LABEL = sys.argv[1]
OUT = RT + '/receipts/checks/' + LABEL
CHECKS = {
    'workflow-projection': ('workflows/check-workflow-projection.v3.py', []),
    'query-projection': ('workflows/check-query-projection.v3.py', ['--report', '{OUT}/query-projection.report.json']),
    'comparison-knowledge': ('workflows/check-comparison-knowledge.v3.py', []),
    'workflows-v1': ('workflows/check_workflows.v1.py', ['--report', '{OUT}/workflows-v1.report.json']),
    'composition': ('foundation/check-composition.v3.py', []),
    'semantic-replay': ('foundation/check-semantic-replay.v3.py', []),
    'evaluator-faults': ('foundation/check-evaluator-faults.v3.py', []),
    'integration': ('check-integration.py', ['--report', '{OUT}/integration.report.json']),
    'security-lifecycle': ('security/check-security-lifecycle.v1.py', ['--report', '{OUT}/security-lifecycle.report.json']),
    'carrier-v3': ('security/check-carrier-v3.py', []),
    'current-profile': ('foundation/check-current-profile.v3.py', []),
    'replay': ('foundation/check-replay.v3.py', []),
}
if len(sys.argv) > 2 and sys.argv[1] == '--root':
    DC = sys.argv[2] + '/docs/coop/design-corrections'
    del sys.argv[1:3]
    LABEL = sys.argv[1]
    OUT = RT + '/receipts/checks/' + LABEL


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


os.makedirs(OUT, exist_ok=True)
summary = {}
for name in sys.argv[2:]:
    rel, args = CHECKS[name]
    script = os.path.join(DC, rel)
    cmd = [PY, '-I', '-B', script] + [a.replace('{OUT}', OUT) for a in args]
    t0 = time.time()
    try:
        run = subprocess.run(cmd, cwd=os.path.dirname(script), capture_output=True, text=True, timeout=3000)
        code, so, se = run.returncode, run.stdout, run.stderr
    except subprocess.TimeoutExpired as exc:
        code, so, se = 'timeout', exc.stdout or '', exc.stderr or ''
        so = so.decode() if isinstance(so, bytes) else so
        se = se.decode() if isinstance(se, bytes) else se
    dt = round(time.time() - t0, 1)
    open(os.path.join(OUT, name + '.stdout'), 'w').write(so)
    open(os.path.join(OUT, name + '.stderr'), 'w').write(se)
    parsed = None
    try:
        doc = json.loads(so)
        parsed = {k: doc.get(k) for k in ('passed', 'count', 'total', 'failedCount', 'status') if k in doc}
        failed = doc.get('failed')
        if isinstance(failed, list):
            parsed['failedIds'] = [f.get('id') or f.get('case') or f if isinstance(f, dict) else f for f in failed][:40]
    except Exception:
        tail = [l for l in so.strip().splitlines()[-3:]]
        parsed = {'stdoutTail': tail}
    row = {'command': ' '.join(cmd), 'cwd': os.path.dirname(script), 'exitCode': code, 'seconds': dt,
           'checkerSha256': sha(script), 'stdoutSha256': hashlib.sha256(so.encode()).hexdigest(),
           'stderrTail': se.strip().splitlines()[-5:], 'parsed': parsed}
    summary[name] = row
    json.dump(row, open(os.path.join(OUT, name + '.receipt.json'), 'w'), indent=1)
print(json.dumps(summary, indent=1))
