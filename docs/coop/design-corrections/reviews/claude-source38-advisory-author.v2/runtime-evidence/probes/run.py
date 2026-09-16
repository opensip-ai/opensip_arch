"""Receipt runner: run one probe with the reference interpreter and retain its output. A rerun never overwrites."""
import hashlib, json, subprocess, sys, time
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source38-advisory-author.v2')
PY = '/tmp/opensip-architecture-review-env/bin/python'
name, args = sys.argv[1], sys.argv[2:]
probe = BASE / 'probes' / (name + '.py')
R = BASE / 'receipts'
R.mkdir(exist_ok=True)
stem = name + ('.' + '.'.join(args) if args else '')
n = 1
while (R / (stem + ('' if n == 1 else '.r%d' % n) + '.receipt.json')).exists():
    n += 1
stem = stem + ('' if n == 1 else '.r%d' % n)
started = time.strftime('%Y-%m-%dT%H:%M:%S')
p = subprocess.run([PY, '-I', '-B', str(probe), *args], cwd=BASE / 'probes', capture_output=True, timeout=3000)
(R / (stem + '.stdout')).write_bytes(p.stdout)
(R / (stem + '.stderr')).write_bytes(p.stderr)
sha = lambda b: hashlib.sha256(b).hexdigest()
rec = {'probe': str(probe), 'probeSha256': sha(probe.read_bytes()), 'args': args, 'interpreter': PY + ' -I -B',
       'started': started, 'finished': time.strftime('%Y-%m-%dT%H:%M:%S'), 'exit': p.returncode,
       'stdoutSha256': sha(p.stdout), 'stderrSha256': sha(p.stderr)}
(R / (stem + '.receipt.json')).write_text(json.dumps(rec, indent=1) + '\n')
sys.stdout.write(p.stdout.decode('utf-8', 'replace')[-20000:])
sys.stderr.write(p.stderr.decode('utf-8', 'replace')[-6000:])
print('\n[receipt %s exit %d]' % (stem, p.returncode))
sys.exit(p.returncode)
