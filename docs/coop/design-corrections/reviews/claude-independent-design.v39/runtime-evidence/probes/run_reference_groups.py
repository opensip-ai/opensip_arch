"""Run the six pinned reference groups against this reviewer's verified disposable exact copy with
/tmp/opensip-architecture-review-env/bin/python -I -B. Preserve every exit/stdout/stderr and record exactly which copy
files the (writing) checkers changed, compared with the formal source39 manifest. Pins are never bypassed."""
import hashlib, json, os, subprocess, sys, time

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v39'
SRC = RT + '/work/source39'
PY = '/tmp/opensip-architecture-review-env/bin/python'
OUT = RT + '/receipts/reference'
IDX = json.load(open(RT + '/receipts/manifest39-index.json'))
os.makedirs(OUT, exist_ok=True)
DC = SRC + '/docs/coop/design-corrections'
GROUPS = [
    ('evaluator3', DC + '/foundation/run-evaluator3-checks.py', ['--out', OUT + '/evaluator3'], 9900),
    ('foundation', DC + '/foundation/run-reference-checks.py', ['--report', OUT + '/foundation.json', '--report-dir', OUT + '/foundation'], 3600),
    ('integration', DC + '/check-integration.py', ['--report', OUT + '/integration.json'], 900),
    ('native', DC + '/native/check_native_evidence.v2.py', [], 900),
    ('security', DC + '/security/check-security-lifecycle.v1.py', ['--report', OUT + '/security.json'], 900),
    ('workflows', DC + '/workflows/run-reference-checks.py', ['--report', OUT + '/workflows.json'], 900),
]
if len(sys.argv) > 1:
    GROUPS = [g for g in GROUPS if g[0] in sys.argv[1:]]


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()


def tree_check():
    changed, missing = [], []
    for rel, want in IDX.items():
        p = os.path.join(SRC, rel)
        if not os.path.isfile(p):
            missing.append(rel)
        elif sha(p) != want:
            changed.append(rel)
    extra = []
    for dp, ds, fs in os.walk(SRC):
        for f in fs:
            rel = os.path.relpath(os.path.join(dp, f), SRC)
            if rel not in IDX:
                extra.append(rel)
    return {'changed': sorted(changed), 'missing': sorted(missing), 'extra': sorted(extra)}


tag = '-'.join(g[0] for g in GROUPS) if len(sys.argv) > 1 else 'all'
report = {'standing': 'independent reviewer execution of the pinned reference groups on a verified disposable exact copy; reference evidence only',
          'copy': SRC, 'before': tree_check(), 'rows': []}
for name, script, args, timeout in GROUPS:
    rel = os.path.relpath(script, SRC)
    cmd = [PY, '-I', '-B', script] + args
    t = time.time()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, cwd=os.path.dirname(script), timeout=timeout)
        code, so, se, to = p.returncode, p.stdout, p.stderr, False
    except subprocess.TimeoutExpired as e:
        code, so, se, to = None, (e.stdout or b'').decode() if isinstance(e.stdout, bytes) else (e.stdout or ''), (e.stderr or b'').decode() if isinstance(e.stderr, bytes) else (e.stderr or ''), True
    open(OUT + '/' + name + '.stdout', 'w').write(so)
    open(OUT + '/' + name + '.stderr', 'w').write(se)
    row = {'name': name, 'script': rel, 'scriptSha256': sha(script), 'scriptMatchesManifest': sha(script) == IDX[rel], 'command': cmd,
           'exitCode': code, 'timedOut': to, 'seconds': round(time.time() - t, 1),
           'stdoutSha256': hashlib.sha256(so.encode()).hexdigest(), 'stderrSha256': hashlib.sha256(se.encode()).hexdigest(),
           'stdoutTail': so[-1500:], 'stderrTail': se[-1500:], 'copyAfter': tree_check()}
    report['rows'].append(row)
    print(name, code, row['seconds'], 'changedSoFar', len(row['copyAfter']['changed']), flush=True)
    json.dump(report, open(OUT + '/groups-report.' + tag + '.json', 'w'), indent=1)
report['passed'] = all(r['exitCode'] == 0 for r in report['rows'])
report['after'] = report['rows'][-1]['copyAfter']
json.dump(report, open(OUT + '/groups-report.' + tag + '.json', 'w'), indent=1)
print(json.dumps({'passed': report['passed'], 'before': report['before'], 'after': report['after']}, indent=1))
