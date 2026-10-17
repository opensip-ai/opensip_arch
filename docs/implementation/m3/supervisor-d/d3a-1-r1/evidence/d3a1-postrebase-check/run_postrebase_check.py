"""D3a-1's post-rebase focused check (LD-D3A1-7): on the moved worktree, the components suite and platform's
process_tests (serial), with the fixture record written from this build's compiler-artifact record and deleted after.
Usage: run_postrebase_check.py <worktree> <evidence dir>. Run under the lane lock (locked_run.py)."""
import hashlib, json, subprocess, sys
from pathlib import Path
W, EV = Path(sys.argv[1]), Path(sys.argv[2]); R = '/opt/homebrew/Cellar/rust/1.95.0/bin/'
git = lambda *a: subprocess.check_output(['/usr/bin/git', *a], cwd=W).decode().strip()
for old in (W / 'target/debug/deps').glob('supervisor_fixture.path'): old.unlink()
r = subprocess.run([R + 'cargo', 'test', '--locked', '--offline', '--no-run', '--message-format=json', '-p', 'opensip-components'], cwd=W, capture_output=True)
(EV / 'fixture-build.log').write_bytes(r.stderr)
fixture = lib = None
for raw in r.stdout.splitlines():
    try: m = json.loads(raw)
    except ValueError: continue
    if m.get('reason') != 'compiler-artifact' or not m.get('executable'): continue
    if m['target']['name'] == 'supervisor_fixture': fixture = Path(m['executable'])
    elif m['target']['name'] == 'opensip_components' and 'lib' in m['target']['kind'] and m['profile']['test']: lib = Path(m['executable'])
record = lib.parent / 'supervisor_fixture.path'
record.write_text(f'{fixture}\n{hashlib.sha256(fixture.read_bytes()).hexdigest()}\n')
try:
    with (EV / 'components.log').open('wb') as out:
        c = subprocess.run([R + 'cargo', 'test', '--locked', '--offline', '--no-fail-fast', '-p', 'opensip-components'], cwd=W, stdout=out, stderr=subprocess.STDOUT).returncode
    with (EV / 'platform-process-tests.log').open('wb') as out:
        p = subprocess.run([R + 'cargo', 'test', '--locked', '--offline', '-p', 'opensip-platform', '--lib', '--', 'process_tests', '--test-threads=1'], cwd=W, stdout=out, stderr=subprocess.STDOUT).returncode
finally:
    record.unlink()
import re
def counts(log):
    t = (EV / log).read_text(errors='replace')
    res = re.findall(r'test result: (ok|FAILED)\. (\d+) passed; (\d+) failed', t)
    return dict(passed=sum(int(a) for _, a, _ in res), failed=sum(int(b) for _, _, b in res), failedNames=sorted(set(re.findall(r'^test (\S+) \.\.\. FAILED$', t, re.M))))
summary = dict(head=git('rev-parse', 'HEAD'), components=dict(exitCode=c, **counts('components.log')), platformProcessTests=dict(exitCode=p, **counts('platform-process-tests.log')))
(EV / 'summary.json').write_text(json.dumps(summary, indent=2) + '\n'); print(json.dumps(summary))
