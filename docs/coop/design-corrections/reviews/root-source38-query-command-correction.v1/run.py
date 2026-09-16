from pathlib import Path
import subprocess, json, time, hashlib, shutil
OUT = Path(__file__).parent
COMMAND = ['/tmp/opensip-architecture-review-env/bin/python', '-I', '-B', '/tmp/opensip-design-corrections/termination-exclusivity-successor.v1/source/docs/coop/design-corrections/workflows/check-query-projection.v3.py', '--report', '/tmp/opensip-design-corrections/root-source38-query-command-correction.v1/query-report.json']
start = time.time()
r = subprocess.run(COMMAND, capture_output=True, timeout=600)
(OUT / 'stdout.txt').write_bytes(r.stdout)
(OUT / 'stderr.txt').write_bytes(r.stderr)
(OUT / 'command.json').write_text(json.dumps({'command':COMMAND, 'exitCode':r.returncode, 'elapsedSeconds':time.time()-start, 'stdoutSha256':hashlib.sha256(r.stdout).hexdigest(), 'stderrSha256':hashlib.sha256(r.stderr).hexdigest()},indent=2)+'\n')
shutil.copytree(OUT, Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews') / OUT.name)
print('Corrected query invocation exit',r.returncode)
raise SystemExit(r.returncode)
