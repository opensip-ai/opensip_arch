"""S10-TSC integration checks with the bound lock in the candidate worktree: plain verify_design (with the
implementation preflight), the standard generate_contracts check (no --write), and the report TypeScript lane
(pinned ignored lane inputs copied from the main checkout, exact bytes). One lane hold, nice 10, private TMPDIR."""
from pathlib import Path
import os, subprocess, tempfile, time, json, hashlib, stat
W = Path('/Users/sb/code/opensip-ai/opensip-s10tsc'); P = W.parent / 'opensip'; A = W.parent / 'opensip_arch'
B = Path('/tmp/opensip-implementation/s10-tsc/integration'); B.mkdir()
D = Path(subprocess.check_output(['/usr/bin/getconf', 'DARWIN_USER_TEMP_DIR']).decode().strip()); lane = D / 'opensip-lanes.lock'; owned = False
os.setpriority(os.PRIO_PROCESS, 0, 10)
PY = '/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14'
NODE = '/Users/sb/.nvm/versions/node/v24.16.0/bin/node'
CHILD = '/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python'
GEN = '/Users/sb/opensip-deps/contracts-generator-rebuild-02/opensip-contract-generator'
lanes = json.loads((W / 'tools/typescript-lanes.json').read_bytes()); copied = 0
for row in lanes['files']:
    t = W / row['path']
    if t.exists(): continue
    assert row['path'].startswith('tools/typescript-boundary/node_modules/'), row['path']
    src = P / row['path']; raw = src.read_bytes(); assert len(raw) == row['bytes'] and hashlib.sha256(raw).hexdigest() == row['sha256']
    t.parent.mkdir(parents=True, exist_ok=True); t.write_bytes(raw); t.chmod(stat.S_IMODE(src.lstat().st_mode)); copied += 1
while not owned:
    try: lane.mkdir(); owned = True
    except FileExistsError: print('waiting for lane', flush=True); time.sleep(5)
try:
    T = Path(tempfile.mkdtemp(prefix='opensip-s10tsc-integration-', dir=D)); T.chmod(0o700)
    E = dict(os.environ, PATH='/opt/homebrew/bin:/usr/bin:/bin', TMPDIR=str(T), GIT_CONFIG_NOSYSTEM='1', GIT_CONFIG_GLOBAL='/dev/null')
    for k in ('GIT_CONFIG_COUNT', 'GIT_DIR', 'GIT_WORK_TREE'): E.pop(k, None)
    steps = [('verify-design', [PY, '-I', '-B', 'tools/verify_design.py', '--architecture', str(A), '--implementation', str(W)]),
             ('generate-contracts-check', [PY, '-I', '-B', 'tools/generate_contracts.py', '--root', str(W), '--architecture', str(A), '--output', str(B / 'generate-work'), '--node', NODE, '--generator', GEN, '--python', CHILD]),
             ('report-lane', [PY, '-I', '-B', 'tools/check_typescript.py', '--root', str(W), '--architecture', str(A), '--node', NODE, '--lane', 'report'])]
    rows = []
    for name, args in steps:
        print(name, 'starting', flush=True)
        with (B / (name + '.log')).open('wb') as log:
            child = subprocess.Popen(args, cwd=W, env=E, stdout=log, stderr=subprocess.STDOUT); pr = os.getpriority(os.PRIO_PROCESS, child.pid); assert pr == 10; code = child.wait()
        rows.append(dict(name=name, args=args, exitCode=code, niceness=pr)); print(name, 'exit', code, flush=True)
    (B / 'checks.json').write_text(json.dumps(dict(rows=rows, allPassed=all(r['exitCode'] == 0 for r in rows), typescriptPinnedInputsCopied=copied, privateTMPDIR=str(T), TMPDIRMode='0700', laneOwnedByThisProcess=True,
        installationAbsent=not Path('/Users/sb/Library/Application Support/OpenSIP').exists(), standing='S10-TSC INTEGRATION CHECKS WITH THE BOUND LOCK'), indent=2) + '\n')
    print('allPassed', all(r['exitCode'] == 0 for r in rows), flush=True)
finally:
    if owned: lane.rmdir()
