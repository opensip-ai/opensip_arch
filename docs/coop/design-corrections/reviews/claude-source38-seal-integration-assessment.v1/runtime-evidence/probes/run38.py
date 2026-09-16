"""Run one focused checker/probe under /tmp/opensip-architecture-review-env/bin/python -I -B against a copied tree.

usage: python3 run38.py NAME TREE CWD -- ARGV...   ('{TREE}' and '{RT}' expand). Foreground; records exit code,
stdout/stderr, a timeout (as unfinished, never a pass) and a full SHA-256 walk of the tree before/after.
"""
import hashlib, json, os, subprocess, sys, time

RT = '/private/tmp/opensip-design-corrections/claude-source38-seal-integration-assessment.v1'
PY = '/tmp/opensip-architecture-review-env/bin/python'
LIMIT = 560


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


name, label, cwd_rel = sys.argv[1], sys.argv[2], sys.argv[3]
assert sys.argv[4] == '--'
root = RT + '/work/' + label
expand = lambda s: s.replace('{TREE}', root).replace('{RT}', RT)
argv = [expand(a) for a in sys.argv[5:]]
cmd = [PY, '-I', '-B'] + argv
before = tree(root)
t = time.time()
try:
    p = subprocess.run(cmd, capture_output=True, text=True, cwd=expand(cwd_rel), timeout=LIMIT)
    code, out, err = p.returncode, p.stdout, p.stderr
except subprocess.TimeoutExpired as exc:
    code = 'TIMEOUT-unfinished-not-a-pass'
    out = (exc.stdout or b'').decode(errors='replace') if isinstance(exc.stdout, bytes) else (exc.stdout or '')
    err = (exc.stderr or b'').decode(errors='replace') if isinstance(exc.stderr, bytes) else (exc.stderr or '')
secs = round(time.time() - t, 1)
after = tree(root)
base = RT + '/receipts/runs/' + name + '.' + label
os.makedirs(RT + '/receipts/runs', exist_ok=True)
open(base + '.stdout', 'w').write(out)
open(base + '.stderr', 'w').write(err)
rec = {'name': name, 'tree': label, 'command': cmd, 'cwd': expand(cwd_rel), 'scriptSha256': hashlib.sha256(open(argv[0], 'rb').read()).hexdigest(),
       'exitCode': code, 'seconds': secs, 'treeFileCount': len(before),
       'treeUnchanged': before == after, 'treeChanged': sorted(k for k in before if after.get(k) != before[k])[:20],
       'treeExtra': sorted(k for k in after if k not in before)[:20],
       'stdoutSha256': hashlib.sha256(out.encode()).hexdigest(), 'stderrSha256': hashlib.sha256(err.encode()).hexdigest()}
json.dump(rec, open(base + '.run.json', 'w'), indent=1)
print(json.dumps({k: rec[k] for k in ('name', 'tree', 'exitCode', 'seconds', 'treeUnchanged')}))
print('--- stdout tail ---')
print(out[-3000:])
print('--- stderr tail ---')
print(err[-3000:])
