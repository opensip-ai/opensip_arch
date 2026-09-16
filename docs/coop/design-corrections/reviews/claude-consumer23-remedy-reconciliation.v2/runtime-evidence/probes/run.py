"""Receipt runner: executes one probe with the pinned interpreter and retains command, stdout, stderr, exit code, timing
and sha256 of the probe and both streams under receipts/<label>[.n]/ (never overwritten). Foreground only."""
import hashlib, json, os, subprocess, sys, time

BASE = '/tmp/opensip-design-corrections/claude-consumer23-remedy-reconciliation.v2'
PY = '/tmp/opensip-architecture-review-env/bin/python'
probe = sys.argv[1]
label = os.path.splitext(probe)[0]
path = os.path.join(BASE, 'probes', probe)
d = os.path.join(BASE, 'receipts', label)
n = 1
while os.path.isdir(d):
    n += 1
    d = os.path.join(BASE, 'receipts', '%s.%d' % (label, n))
os.makedirs(d)
cmd = [PY, '-I', '-B', path] + sys.argv[2:]
t0 = time.time()
r = subprocess.run(cmd, capture_output=True, text=True, cwd=BASE, timeout=540)
rec = {'command': cmd, 'cwd': BASE, 'exit': r.returncode, 'seconds': round(time.time() - t0, 1),
       'probeSha256': hashlib.sha256(open(path, 'rb').read()).hexdigest(),
       'stdoutSha256': hashlib.sha256(r.stdout.encode()).hexdigest(), 'stderrSha256': hashlib.sha256(r.stderr.encode()).hexdigest(),
       'startedUtc': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(t0))}
open(os.path.join(d, 'stdout.txt'), 'w').write(r.stdout)
open(os.path.join(d, 'stderr.txt'), 'w').write(r.stderr)
json.dump(rec, open(os.path.join(d, 'command.json'), 'w'), indent=1)
print(r.stdout[-9000:])
if r.stderr:
    print('--- stderr tail ---')
    print(r.stderr[-3000:])
print('receipt dir:', d, '| exit', r.returncode, '| %.1fs' % rec['seconds'])
sys.exit(0)
