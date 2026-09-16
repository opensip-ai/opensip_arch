"""p03 <tree>: root's ACTUAL probe.py, byte-for-byte, against work/<tree> of this runtime.

work/rootprobe-<tree>/probe.py is a regular copy verified against the p00 hash of root probe.py; work/rootprobe-<tree>/source
is a symlink to work/<tree> (this runtime's own regular tree). The probe writes its checker stdout and report.json only
there. Nothing under the root probe directory is written. Output: receipts/p03-rootprobe-<tree>.json.
"""
import hashlib, json, os, shutil, subprocess, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-repair-join-author.v1-continuation.v1')
ROOT = Path('/tmp/opensip-design-corrections/root-repair-owner-probe.v2')
R = BASE / 'receipts'
tree = sys.argv[1]
D = BASE / 'work' / ('rootprobe-' + tree)
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()
p00 = json.loads((R / 'p00-copy.json').read_text())
if D.exists():
    print('target exists; refusing'); sys.exit(2)
D.mkdir(parents=True)
shutil.copyfile(ROOT / 'probe.py', D / 'probe.py')
assert sha(D / 'probe.py') == p00['rootInputs']['probe.py'] == sha(ROOT / 'probe.py')
os.symlink(BASE / 'work' / tree, D / 'source')
p = subprocess.run(['/tmp/opensip-architecture-review-env/bin/python', '-I', '-B', str(D / 'probe.py')], cwd=D, capture_output=True, timeout=3000)
(D / 'probe-stdout.txt').write_bytes(p.stdout)
(D / 'probe-stderr.txt').write_bytes(p.stderr)
out = {'dir': str(D), 'sourceSymlink': os.readlink(D / 'source'), 'probeSha256': sha(D / 'probe.py'), 'exit': p.returncode,
       'stdout': p.stdout.decode()[-4000:], 'stderrTail': p.stderr.decode()[-4000:]}
if (D / 'report.json').exists():
    rep = json.loads((D / 'report.json').read_text())
    chk = json.loads((D / 'checker-stdout.json').read_text())
    out['report'] = {k: rep[k] for k in ('checkerExit', 'actualRunId', 'calls', 'before', 'after')}
    out['reportSha256'] = sha(D / 'report.json')
    out['checker'] = {'count': chk['count'], 'passed': chk['passed'], 'failed': chk['failed'], 'stdoutSha256': sha(D / 'checker-stdout.json')}
(R / ('p03-rootprobe-%s.json' % tree)).write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps(out, indent=1)[:12000])
sys.exit(p.returncode)
