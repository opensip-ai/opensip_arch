"""p04 <tree>: the complete semantic golden replay checker (foundation/check-semantic-replay.v3.py) of work/<tree>.

Run unmodified as a subprocess with no arguments; stdout retained in full. Output: receipts/p04-semantic-<tree>.json.
"""
import hashlib, json, subprocess, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-repair-join-author.v1')
R = BASE / 'receipts'
tree = sys.argv[1]
F = BASE / 'work' / tree / 'docs/coop/design-corrections/foundation'
sha = lambda b: hashlib.sha256(b).hexdigest()
p = subprocess.run(['/tmp/opensip-architecture-review-env/bin/python', '-I', '-B', str(F / 'check-semantic-replay.v3.py')], cwd=F, capture_output=True, timeout=3000)
(R / ('p04-semantic-%s.stdout' % tree)).write_bytes(p.stdout)
out = {'checker': str(F / 'check-semantic-replay.v3.py'), 'checkerSha256': sha((F / 'check-semantic-replay.v3.py').read_bytes()),
       'exit': p.returncode, 'stdoutSha256': sha(p.stdout), 'stderrTail': p.stderr.decode()[-3000:]}
try:
    doc = json.loads(p.stdout)
    out.update({k: doc.get(k) for k in ('passed', 'count', 'blocked', 'faults')})
except ValueError as exc:
    out['parseError'] = str(exc)
(R / ('p04-semantic-%s.json' % tree)).write_text(json.dumps(out, indent=1) + '\n')
print(json.dumps(out, indent=1)[:6000])
sys.exit(p.returncode)
