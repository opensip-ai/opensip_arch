"""P3 (CLOSURE + INVOCATION counterfactual). Prove the new item-1 controls are NOT vacuous.

Kind: a DISPOSABLE clone of the corrected tree has ONLY the registration reverted - the two codes
are removed from public-detail-registry records and from the mirrored DomainDetailCode enum, and
nothing else. The identity checker is then run there. If the new controls were register-string
theatre they would still pass; the correction is only real if they FAIL, and by name.

Reported as measured, including the failures. Nothing is swallowed.
"""
import json, shutil, subprocess, sys
from pathlib import Path

SRC = Path(sys.argv[1])            # corrected .../work
DEST = Path(sys.argv[2])           # disposable clone root
PY = sys.argv[3]

NEW = ['BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER', 'BASELINE.SCOPE_PARAMETER_DIGEST_MISMATCH']

if DEST.exists():
    shutil.rmtree(DEST)
DEST.mkdir(parents=True)
subprocess.run(['cp', '-Rc', str(SRC / 'docs'), str(DEST / 'docs')], check=True)

D = DEST / 'docs/coop/design-corrections'
reg_p = D / 'public-detail-registry.v1.json'
com_p = D / 'workflows/schemas/common.schema.json'
reg = json.loads(reg_p.read_text())
com = json.loads(com_p.read_text())
assert all(c in {r['code'] for r in reg['records']} for c in NEW), 'clone was not the corrected tree'
reg['records'] = [r for r in reg['records'] if r['code'] not in NEW]
com['$defs']['DomainDetailCode']['enum'] = [c for c in com['$defs']['DomainDetailCode']['enum']
                                            if c not in NEW]
reg_p.write_text(json.dumps(reg, indent=2) + '\n')
com_p.write_text(json.dumps(com, indent=2) + '\n')

report = DEST / 'counterfactual-identity.json'
run = subprocess.run([PY, '-I', '-B', str(D / 'foundation/check-identity.py'),
                      '--report', str(report)], capture_output=True, text=True, timeout=1800)

out = {'kind': 'closure+invocation counterfactual (registration reverted, nothing else)',
       'revertedCodes': NEW, 'exitCode': run.returncode, 'stdout': run.stdout.strip(),
       'stderr': run.stderr.strip()[-1500:]}
if report.exists():
    rep = json.loads(report.read_text())
    out['reportKeys'] = sorted(rep)
    for key in ('results', 'checks', 'cases'):
        if isinstance(rep.get(key), list):
            out['failedIds'] = sorted(r['id'] for r in rep[key] if not r.get('passed', True))
            out['failedCount'] = len(out['failedIds'])
            break
print(json.dumps(out, indent=1))
