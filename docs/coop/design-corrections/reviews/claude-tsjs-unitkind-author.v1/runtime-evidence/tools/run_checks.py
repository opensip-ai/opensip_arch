"""Run affected reference checkers against this runtime's capture; receipts go to receipts/checks/LABEL (never the tree).

usage: python -I -B run_checks.py LABEL CHECK [CHECK ...]   (CHECK 'evaluator3-children' expands to all 17 current children)
The 17 children and their arguments are those of foundation/run-evaluator3-checks.py; they are run directly because
that launcher's source-pin gate is invalid for an edited tree (pins are root-owned and not regenerated here).
"""
import hashlib, json, os, subprocess, sys, time

RT = '/private/tmp/opensip-design-corrections/claude-tsjs-unitkind-author.v1'
DC = RT + '/work/source/docs/coop/design-corrections'
PY = '/tmp/opensip-architecture-review-env/bin/python'
LABEL = sys.argv[1]
OUT = RT + '/receipts/checks/' + LABEL
EVALUATOR3 = [
    ('current-profile', 'foundation/check-current-profile.v3.py', []),
    ('enumeration', 'foundation/check-enumeration.v1.py', ['--receipt', '{OUT}/enumeration.receipt.json', '--hashes', '{OUT}/enumeration.hashes.json', '--stdout']),
    ('atoms', 'foundation/check-atoms.v1.py', []),
    ('execution-inputs', 'foundation/check-execution-inputs.v1.py', []),
    ('composition', 'foundation/check-composition.v3.py', []),
    ('full-replay', 'foundation/check-replay.v3.py', []),
    ('native-replay', 'foundation/check-semantic-replay.v3.py', []),
    ('execution-replay', 'foundation/check-execution-replay.v3.py', []),
    ('candidate-replay', 'foundation/check-candidate-replay.v3.py', []),
    ('policy-derivation', 'foundation/check-policy-derivation.v3.py', []),
    ('faults', 'foundation/check-evaluator-faults.v3.py', []),
    ('provider-attribution-return', 'foundation/check-provider-attribution-return.v2.py', []),
    ('workflow-projection', 'workflows/check-workflow-projection.v3.py', []),
    ('query-projection', 'workflows/check-query-projection.v3.py', ['--report', '{OUT}/query-projection.receipt.json']),
    ('comparison-knowledge', 'workflows/check-comparison-knowledge.v3.py', []),
    ('analysis-seal', 'security/check-analysis-seal-adapter.v1.py', []),
    ('native-consumer24-corrections', 'foundation/check-native-consumer24-corrections.v1.py', []),
]
CHECKS = {name: (script, args) for name, script, args in EVALUATOR3}
CHECKS['native-driver'] = (RT + '/tools/run_native_checker.py', ['{OUT}/native-evidence-report.json'])
CHECKS['native-driver-unpinned'] = (RT + '/tools/run_native_checker.py', ['{OUT}/native-evidence-report.json', '--bypass-pins-labelled'])


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


names = []
for n in sys.argv[2:]:
    names.extend([e[0] for e in EVALUATOR3] if n == 'evaluator3-children' else [n])
os.makedirs(OUT, exist_ok=True)
summary = {}
for name in names:
    rel, args = CHECKS[name]
    script = rel if rel.startswith('/') else os.path.join(DC, rel)
    cmd = [PY, '-I', '-B', script] + [a.replace('{OUT}', OUT) for a in args]
    cwd = DC + '/native' if rel.startswith('/') else os.path.dirname(script)
    t0 = time.time()
    try:
        run = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True, timeout=1800)
        code, so, se = run.returncode, run.stdout, run.stderr
    except subprocess.TimeoutExpired as exc:
        code, so, se = 'timeout', exc.stdout or '', exc.stderr or ''
        so = so.decode() if isinstance(so, bytes) else so
        se = se.decode() if isinstance(se, bytes) else se
    open(os.path.join(OUT, name + '.stdout'), 'w').write(so)
    open(os.path.join(OUT, name + '.stderr'), 'w').write(se)
    parsed = {}
    try:
        doc = json.loads(so)
        for k in ('passed', 'total', 'count', 'result', 'failedCount', 'mismatches', 'n'):
            if k in doc:
                parsed[k] = doc[k] if not isinstance(doc[k], list) else doc[k][:40]
        if isinstance(doc.get('failed'), list):
            parsed['failed'] = [{kk: f.get(kk) for kk in ('item', 'case', 'id', 'name', 'detail') if kk in f} if isinstance(f, dict) else f for f in doc['failed']][:60]
        elif 'failed' in doc:
            parsed['failed'] = doc['failed']
        if name.startswith('native-driver'):
            rep = json.load(open(OUT + '/native-evidence-report.json'))
            parsed['native'] = {k: rep.get(k) for k in ('result', 'cases', 'pins', 'driverStanding')}
            if isinstance(parsed['native'].get('cases'), dict):
                parsed['native']['cases'] = {k: v for k, v in parsed['native']['cases'].items() if k in ('total', 'passed', 'failed', 'failures')}
    except Exception:
        parsed = {'stdoutTail': so.strip().splitlines()[-5:]}
    row = {'command': cmd, 'cwd': cwd, 'exitCode': code, 'seconds': round(time.time() - t0, 1), 'scriptSha256': sha(script),
           'stdoutSha256': hashlib.sha256(so.encode()).hexdigest(), 'stderrTail': se.strip().splitlines()[-6:], 'parsed': parsed}
    summary[name] = row
    json.dump(row, open(os.path.join(OUT, name + '.receipt.json'), 'w'), indent=1, default=str)
print(json.dumps({n: {'exitCode': r['exitCode'], 'seconds': r['seconds'], 'parsed': r['parsed']} for n, r in summary.items()}, indent=1, default=str)[:20000])
