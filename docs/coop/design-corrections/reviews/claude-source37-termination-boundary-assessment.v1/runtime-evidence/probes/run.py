"""Receipt runner: execute one probe with the pinned interpreter and retain its exact outcome.

A nonzero exit is retained, never retried over: an existing receipt gets a new numbered suffix.
"""
import hashlib, json, subprocess, sys, time
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source37-termination-boundary-assessment.v1')
PY = '/tmp/opensip-architecture-review-env/bin/python'


def sha(b):
    return hashlib.sha256(b).hexdigest()


name = sys.argv[1]
probe = BASE / 'probes' / (name + '.py')
out = BASE / 'receipts'
out.mkdir(exist_ok=True)
stem, n = name, 1
while (out / (stem + '.receipt.json')).exists():
    n += 1
    stem = name + '.r' + str(n)
started = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
proc = subprocess.run([PY, '-I', '-B', str(probe)], capture_output=True, cwd=str(BASE / 'probes'), timeout=900)
(out / (stem + '.stdout')).write_bytes(proc.stdout)
(out / (stem + '.stderr')).write_bytes(proc.stderr)
receipt = {
    'probe': probe.name, 'probeSha256': sha(probe.read_bytes()), 'interpreter': PY + ' -I -B',
    'started': started, 'finished': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
    'exit': proc.returncode, 'stdoutSha256': sha(proc.stdout), 'stderrSha256': sha(proc.stderr),
}
(out / (stem + '.receipt.json')).write_text(json.dumps(receipt, indent=2) + '\n')
print(json.dumps(receipt, indent=2))
sys.stdout.write(proc.stdout.decode(errors='replace')[-6000:])
sys.stderr.write(proc.stderr.decode(errors='replace')[-4000:])
