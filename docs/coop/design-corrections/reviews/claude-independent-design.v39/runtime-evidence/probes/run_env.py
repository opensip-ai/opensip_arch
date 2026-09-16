"""Run one independent probe under /tmp/opensip-architecture-review-env/bin/python -I -B with cwd RT; preserve
exit/stdout/stderr and verify the probe copy still equals the formal source39 manifest afterwards.
usage: python3 run_env.py NAME SCRIPT [ARGS...]"""
import hashlib, json, os, subprocess, sys, time

RT = '/private/tmp/opensip-design-corrections/claude-independent-design.v39'
PY = '/tmp/opensip-architecture-review-env/bin/python'
COPY = RT + '/work/source39-pkg'
IDX = json.load(open(RT + '/receipts/manifest39-index.json'))


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for c in iter(lambda: f.read(1 << 20), b''):
            h.update(c)
    return h.hexdigest()


def check():
    changed = [r for r, s in IDX.items() if not os.path.isfile(os.path.join(COPY, r)) or sha(os.path.join(COPY, r)) != s]
    extra = [os.path.relpath(os.path.join(d, f), COPY) for d, _, fs in os.walk(COPY) for f in fs
             if os.path.relpath(os.path.join(d, f), COPY) not in IDX]
    return sorted(changed), sorted(extra)


name, script, args = sys.argv[1], sys.argv[2], sys.argv[3:]
t = time.time()
p = subprocess.run([PY, '-I', '-B', script] + args, capture_output=True, text=True, cwd=RT, timeout=7200)
secs = round(time.time() - t, 1)
changed, extra = check()
os.makedirs(RT + '/receipts/runs', exist_ok=True)
open(RT + '/receipts/runs/%s.stdout' % name, 'w').write(p.stdout)
open(RT + '/receipts/runs/%s.stderr' % name, 'w').write(p.stderr)
rec = {'name': name, 'command': [PY, '-I', '-B', script] + args, 'scriptSha256': sha(script), 'exitCode': p.returncode, 'seconds': secs,
       'copy': COPY, 'copyChangedVsManifest': changed, 'copyExtraVsManifest': extra,
       'stdoutSha256': hashlib.sha256(p.stdout.encode()).hexdigest(), 'stderrSha256': hashlib.sha256(p.stderr.encode()).hexdigest()}
json.dump(rec, open(RT + '/receipts/runs/%s.run.json' % name, 'w'), indent=1)
print(json.dumps({k: rec[k] for k in ('name', 'exitCode', 'seconds', 'copyChangedVsManifest', 'copyExtraVsManifest')}))
print(p.stdout[-7000:])
print(p.stderr[-4000:])
