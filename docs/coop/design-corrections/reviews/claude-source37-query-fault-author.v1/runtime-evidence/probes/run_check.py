"""Run one focused checker/probe under the pinned review interpreter (-I -B) against one tree of this runtime.

usage: python3 run_check.py NAME TREE CWD_REL -- ARGV...
TREE is a directory name under work/ (source37-pristine | source37-coauthor). '{TREE}' and '{RT}' in CWD_REL/ARGV
expand to absolute paths. Preserves exit code, stdout/stderr and proves which tree files changed (full SHA-256 walk).
"""
import hashlib, json, os, subprocess, sys, time

RT = '/private/tmp/opensip-design-corrections/claude-source37-query-fault-author.v1'
PY = '/tmp/opensip-architecture-review-env/bin/python'


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
cwd = expand(cwd_rel)
cmd = [PY, '-I', '-B'] + argv
before = tree(root)
t = time.time()
p = subprocess.run(cmd, capture_output=True, text=True, cwd=cwd, timeout=3600)
secs = round(time.time() - t, 1)
after = tree(root)
base = RT + '/receipts/runs/' + name + '.' + label
os.makedirs(RT + '/receipts/runs', exist_ok=True)
open(base + '.stdout', 'w').write(p.stdout)
open(base + '.stderr', 'w').write(p.stderr)
rec = {'name': name, 'tree': label, 'command': cmd, 'cwd': cwd,
       'scriptSha256': hashlib.sha256(open(argv[0], 'rb').read()).hexdigest(),
       'exitCode': p.returncode, 'seconds': secs, 'treeFileCount': len(before),
       'treeChanged': sorted(k for k in before if after.get(k) != before[k]),
       'treeExtra': sorted(k for k in after if k not in before), 'treeRemoved': sorted(k for k in before if k not in after),
       'stdoutSha256': hashlib.sha256(p.stdout.encode()).hexdigest(), 'stderrSha256': hashlib.sha256(p.stderr.encode()).hexdigest(),
       'stdoutBytes': len(p.stdout.encode()), 'stderrBytes': len(p.stderr.encode())}
json.dump(rec, open(base + '.run.json', 'w'), indent=1)
print(json.dumps({k: rec[k] for k in ('name', 'tree', 'exitCode', 'seconds', 'treeChanged', 'treeExtra', 'treeRemoved')}))
print('--- stdout tail ---')
print(p.stdout[-2500:])
print('--- stderr tail ---')
print(p.stderr[-2500:])
