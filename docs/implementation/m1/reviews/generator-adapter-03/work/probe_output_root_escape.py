"""(B) End-to-end: real parent, real Python/Node children, rebound generator stub.

The stub (generator step 3) empties its granted output root, removes it and
replaces it with a symlink to an outside victim directory. The parent then
renders the unmodified TypeScript step's write grant from Path(output).resolve().
"""
import hashlib, json, shutil, subprocess, sys
from pathlib import Path

WORK = Path(__file__).resolve().parent
case = WORK / 'e2e-escape'
victim = WORK / 'victim'
shutil.rmtree(case, ignore_errors=True)
shutil.copytree(WORK / 'base', case, symlinks=True)
shutil.rmtree(victim, ignore_errors=True); victim.mkdir()
(victim / 'canary.txt').write_text('victim canary\n')

def pin(raw): return {'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}
stub = WORK / 'bin/probe-escape'
closure_path = case / 'tools/contracts/generator-closure.json'
receipt_path = case / 'tools/contracts/build-receipt.json'
closure = json.loads(closure_path.read_text()); receipt = json.loads(receipt_path.read_text())
closure['toolchain']['generator'] = pin(stub.read_bytes())
receipt['executable'] = closure['toolchain']['generator']
receipt_path.write_text(json.dumps(receipt, indent=2) + '\n')
for row in closure['files']:
    row.update(pin((case / row['path']).read_bytes()))
closure_path.write_text(json.dumps(closure, indent=1) + '\n')
registry_path = case / 'schemas/registry.json'
registry = json.loads(registry_path.read_text())
registry['recipes'][0]['generatorClosureSha256'] = pin(closure_path.read_bytes())['sha256']
registry_path.write_text(json.dumps(registry, indent=2) + '\n')

before_outputs = {p: pin((case / p).read_bytes()) for p in [o['path'] for o in registry['recipes'][0]['outputs']]}
r = subprocess.run(['/opt/homebrew/bin/python3', '-I', '-B', str(case / 'tools/generate_contracts.py'), '--root', str(case),
                    '--generator', str(stub), '--node', '/Users/sb/.nvm/versions/node/v24.16.0/bin/node'],
                   capture_output=True, text=True, timeout=900)
victim_files = sorted(str(p.relative_to(victim)) for p in victim.rglob('*') if p.is_file())
report = {
    'exit': r.returncode, 'stdout': r.stdout, 'stderr': r.stderr[-2000:],
    'victimFilesAfter': victim_files,
    'victimFilePins': {name: pin((victim / name).read_bytes()) for name in victim_files},
    'caseOutputsUnchanged': all(pin((case / p).read_bytes()) == v for p, v in before_outputs.items()),
}
# Compare the out-of-confinement TS writes with the frozen subject's checked-in TS outputs.
subject = Path('/tmp/opensip-implementation/m1-generator-adapter-subject-03')
for rel in ('apps/report/src/generated/report.ts', 'providers/typescript/src/generated/protocol.ts'):
    if (victim / rel).exists():
        a, b = (victim / rel).read_bytes(), (subject / rel).read_bytes()
        report['victim:' + rel] = {'bytes': len(a), 'bodyEqualsSubjectExceptProvenanceHeader': a.split(b'\n', 3)[3] == b.split(b'\n', 3)[3]}
print(json.dumps(report, indent=1))
