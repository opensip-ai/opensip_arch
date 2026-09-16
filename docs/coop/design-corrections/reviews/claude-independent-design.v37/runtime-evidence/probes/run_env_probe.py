"""Run one independent probe under the pinned review interpreter (-I -B) against the verified exact copy,
and prove the probe changed no copy file (full tree SHA-256 before/after)."""
import hashlib, json, os, subprocess, sys, time
BASE = '/tmp/opensip-design-corrections/claude-independent-design.v37'
PY = '/tmp/opensip-architecture-review-env/bin/python'
COPY = BASE + '/work/source37'


def tree(root):
    out = {}
    for d, ds, fs in os.walk(root):
        ds.sort()
        for f in sorted(fs):
            p = os.path.join(d, f)
            h = hashlib.sha256()
            with open(p, 'rb') as fh:
                for chunk in iter(lambda: fh.read(1 << 20), b''):
                    h.update(chunk)
            out[os.path.relpath(p, root)] = h.hexdigest()
    return out


script = sys.argv[1]
name = os.path.splitext(os.path.basename(script))[0]
before = tree(COPY)
t = time.time()
p = subprocess.run([PY, '-I', '-B', script], capture_output=True, text=True, timeout=5400)
secs = round(time.time() - t, 1)
after = tree(COPY)
receipt = {
    'probe': script, 'probeSha256': hashlib.sha256(open(script, 'rb').read()).hexdigest(),
    'command': [PY, '-I', '-B', script], 'exitCode': p.returncode, 'seconds': secs,
    'copy': COPY, 'copyFileCount': len(before),
    'copyChanged': sorted(k for k in before if after.get(k) != before[k]),
    'copyExtra': sorted(k for k in after if k not in before),
    'stdoutSha256': hashlib.sha256(p.stdout.encode()).hexdigest(),
    'stderrTail': p.stderr[-4000:],
}
os.makedirs(BASE + '/receipts/probes', exist_ok=True)
json.dump(receipt, open(BASE + '/receipts/probes/' + name + '.run.json', 'w'), indent=1)
print(json.dumps({k: receipt[k] for k in ('exitCode', 'seconds', 'copyFileCount', 'copyChanged', 'copyExtra')}))
print(p.stdout[-6000:])
print(p.stderr[-3000:])
