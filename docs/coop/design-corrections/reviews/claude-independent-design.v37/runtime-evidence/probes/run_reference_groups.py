"""Run the six source-pinned reference groups from the verified disposable copy.

Pin-gate refusals and failures are recorded, never bypassed. Commands mirror the root runner's
argument shapes; outputs go under this review's receipts directory. After the runs the copy is
re-verified against the manifest so any checker writes relative to code are disclosed.
"""
import hashlib, json, os, subprocess, sys, time

PY = '/tmp/opensip-architecture-review-env/bin/python'
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v37'
SRC = BASE + '/work/source37'
OUT = BASE + '/receipts/reference'
DC = SRC + '/docs/coop/design-corrections'
MANIFEST = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v37.json'
os.makedirs(OUT, exist_ok=False)

def sha(b):
    return hashlib.sha256(b).hexdigest()

jobs = [
    ('evaluator3', DC + '/foundation/run-evaluator3-checks.py', ['--out', OUT + '/evaluator3'], 9900),
    ('foundation', DC + '/foundation/run-reference-checks.py', ['--report', OUT + '/foundation.json', '--report-dir', OUT + '/foundation'], 3600),
    ('integration', DC + '/check-integration.py', ['--report', OUT + '/integration.json'], 900),
    ('native', DC + '/native/check_native_evidence.v2.py', [], 900),
    ('security', DC + '/security/check-security-lifecycle.v1.py', ['--report', OUT + '/security.json'], 900),
    ('workflows', DC + '/workflows/run-reference-checks.py', ['--report', OUT + '/workflows.json'], 900),
]
only = sys.argv[1:]
rows = []
for name, script, args, tmo in jobs:
    if only and name not in only:
        continue
    cmd = [PY, '-I', '-B', script] + args
    t0 = time.time()
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=tmo, cwd=os.path.dirname(script))
        code, so, se, to = p.returncode, p.stdout, p.stderr, False
    except subprocess.TimeoutExpired as e:
        dec = lambda v: v.decode('utf-8', 'replace') if isinstance(v, bytes) else (v or '')
        code, so, se, to = None, dec(e.stdout), dec(e.stderr), True
    open(f'{OUT}/{name}.stdout', 'w').write(so)
    open(f'{OUT}/{name}.stderr', 'w').write(se)
    row = {'name': name, 'script': os.path.relpath(script, SRC), 'scriptSha256': sha(open(script, 'rb').read()),
           'command': cmd, 'exitCode': code, 'timedOut': to, 'seconds': round(time.time() - t0, 1),
           'stdoutSha256': sha(so.encode()), 'stderrSha256': sha(se.encode()), 'stdoutTail': so[-1500:], 'stderrTail': se[-1500:]}
    rows.append(row)
    print(name, code, 'timeout' if to else '', row['seconds'], flush=True)

m = json.load(open(MANIFEST))
changed = []
for f in m['files']:
    pth = os.path.join(SRC, f['path'])
    if not os.path.isfile(pth):
        changed.append({'path': f['path'], 'state': 'missing'}); continue
    b = open(pth, 'rb').read()
    if sha(b) != f['sha256'] or len(b) != f['bytes']:
        changed.append({'path': f['path'], 'state': 'changed'})
listed = {f['path'] for f in m['files']}
extra = []
for d, _, fs in os.walk(SRC):
    for fn in fs:
        rel = os.path.relpath(os.path.join(d, fn), SRC)
        if rel not in listed and '__pycache__' not in rel:
            extra.append(rel)
rep = {'standing': 'Independent reviewer execution of source-pinned reference groups from a verified disposable exact copy; reference evidence only, not product qualification.',
       'copyVerifiedBeforeRun': BASE + '/receipts/archive-verification.json',
       'rows': rows, 'passed': bool(rows) and all(r['exitCode'] == 0 and not r['timedOut'] for r in rows),
       'copyFilesChangedByCheckers': changed, 'copyExtraFilesAfterRun': extra[:200]}
json.dump(rep, open(f'{OUT}/groups-report{"-" + "-".join(only) if only else ""}.json', 'w'), indent=1)
print(json.dumps({'passed': rep['passed'], 'changed': changed, 'extraCount': len(extra)}, indent=1))
