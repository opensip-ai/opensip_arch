"""Run one focused probe/checker under the pinned review interpreter (-I -B) against the verified overlay copy.
Preserves exit code, stdout/stderr and proves no copy file changed (full-tree SHA-256 before/after).
usage: python3 run_env.py NAME CWD -- ARGV..."""
import hashlib, json, os, subprocess, sys, time

RT = '/private/tmp/opensip-design-corrections/claude-source37-root-corrections-review.v1'
PY = '/tmp/opensip-architecture-review-env/bin/python'
COPY = RT + '/work/source37-overlay'


def tree(root):
    out = {}
    for d, ds, fs in os.walk(root):
        for f in fs:
            p = os.path.join(d, f)
            h = hashlib.sha256()
            with open(p, 'rb') as fh:
                for c in iter(lambda: fh.read(1 << 20), b''):
                    h.update(c)
            out[os.path.relpath(p, root)] = h.hexdigest()
    return out


name, cwd = sys.argv[1], sys.argv[2]
assert sys.argv[3] == '--'
argv = sys.argv[4:]
cmd = [PY, '-I', '-B'] + argv
before = tree(COPY)
t = time.time()
p = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=3600)
secs = round(time.time() - t, 1)
after = tree(COPY)
os.makedirs(RT + '/receipts/runs', exist_ok=True)
open(RT + '/receipts/runs/' + name + '.stdout', 'w').write(p.stdout)
open(RT + '/receipts/runs/' + name + '.stderr', 'w').write(p.stderr)
script = argv[0]
rec = {'name': name, 'command': cmd, 'cwd': cwd, 'scriptSha256': hashlib.sha256(open(script, 'rb').read()).hexdigest(),
       'exitCode': p.returncode, 'seconds': secs, 'copyFileCount': len(before),
       'copyChanged': sorted(k for k in before if after.get(k) != before[k]), 'copyExtra': sorted(k for k in after if k not in before),
       'stdoutSha256': hashlib.sha256(p.stdout.encode()).hexdigest(), 'stderrSha256': hashlib.sha256(p.stderr.encode()).hexdigest()}
json.dump(rec, open(RT + '/receipts/runs/' + name + '.run.json', 'w'), indent=1)
print(json.dumps({k: rec[k] for k in ('name', 'exitCode', 'seconds', 'copyChanged', 'copyExtra')}))
print('--- stdout tail ---')
print(p.stdout[-5000:])
print('--- stderr tail ---')
print(p.stderr[-3000:])
