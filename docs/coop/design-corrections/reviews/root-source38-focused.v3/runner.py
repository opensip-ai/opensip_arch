from pathlib import Path
import json, hashlib, subprocess, time, concurrent.futures, shutil
BASE = Path('/tmp/opensip-design-corrections')
SOURCE = BASE / 'termination-exclusivity-successor.v1/source'
OUT = BASE / 'root-source38-focused.v3'
REPO = Path('/Users/sb/code/opensip-ai/opensip_arch')
assert not OUT.exists()
OUT.mkdir()
PYTHON = '/tmp/opensip-architecture-review-env/bin/python'
DC = SOURCE / 'docs/coop/design-corrections'
commands = {
    'semantic': [PYTHON, '-I', '-B', str(DC / 'foundation/check-semantic-replay.v3.py')],
    'query': [PYTHON, '-I', '-B', str(DC / 'workflows/check-query-projection.v3.py'), '--output', str(OUT / 'query-report.json')],
    'workflow': [PYTHON, '-I', '-B', str(DC / 'workflows/check-workflow-projection.v3.py')],
}
def execute(item):
    name, command = item
    started = time.time()
    result = subprocess.run(command, cwd=SOURCE, capture_output=True, timeout=600)
    (OUT / (name + '.stdout')).write_bytes(result.stdout)
    (OUT / (name + '.stderr')).write_bytes(result.stderr)
    row = {'name': name, 'command': command, 'exitCode': result.returncode, 'elapsedSeconds': time.time()-started, 'stdoutSha256': hashlib.sha256(result.stdout).hexdigest(), 'stderrSha256': hashlib.sha256(result.stderr).hexdigest()}
    print(name, 'exit', result.returncode, flush=True)
    return row
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:
    rows = list(pool.map(execute, commands.items()))
report = {'standing': 'Focused checks after exact host-finalizer integration. Not global validation, independent acceptance or product qualification.', 'commands': rows, 'passed': all(row['exitCode']==0 for row in rows)}
(OUT / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
shutil.copyfile(Path(__file__), OUT / 'runner.py')
shutil.copytree(OUT, REPO / 'docs/coop/design-corrections/reviews' / OUT.name)
raise SystemExit(0 if report['passed'] else 1)
