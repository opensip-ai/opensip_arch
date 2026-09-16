"""Discrimination: run the v2 EDITED validator over hybrid trees that restore exactly one earlier remedy area each.

  hybrid-v1ddl      v2 tree + v1-final DDL and attempt-custody bytes   expect only v2 storage-class controls to fail
  hybrid-frozenddl  v2 tree + frozen37 DDL and attempt-custody bytes   expect storage, publication and scenario controls to fail
  hybrid-routes     v2 tree + frozen37 S12 and read-only table         expect only S12 / read-only route-row controls to fail
Hybrids are new directories in this runtime; frozen37, v1final and edited trees are only read.
"""
import hashlib, json, shutil, subprocess, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v2')
W = BASE / 'work'
DDL = 'docs/coop/design-corrections/security/grant-journal.carrier.v3.sql'
AC = 'docs/v2/architecture/attempt-custody.schema.v1.json'
S12 = 'docs/v2/contracts/product-v1/security-and-lifecycle.md'
RO = 'docs/v2/architecture/commit-recovery-readonly.v3.md'
HYBRIDS = {'hybrid-v1ddl': ('v1final', [DDL, AC]), 'hybrid-frozenddl': ('frozen37', [DDL, AC]), 'hybrid-routes': ('frozen37', [S12, RO])}
result = {}
for name, (src, restore) in HYBRIDS.items():
    root = W / name
    shutil.copytree(W / 'edited', root, symlinks=True, dirs_exist_ok=False)
    for rel in restore:
        shutil.copyfile(W / src / rel, root / rel)
    report = BASE / 'receipts' / ('p04-integrated-carrier.' + name + '.json')
    if report.exists():
        raise SystemExit('preserve earlier report: ' + str(report))
    r = subprocess.run([sys.executable, '-I', '-B', str(root / 'docs/coop/design-corrections/security/check-integrated-carrier.v1.py'),
                        '--source', str(root), '--report', str(report)], capture_output=True, text=True, timeout=900)
    rep = json.loads(report.read_text()) if report.exists() else {'error': r.stderr[-2000:]}
    failures = [c['check'] for c in rep.get('checks', []) if not c['pass']]
    result[name] = {'restoredFrom': src, 'restored': {rel: hashlib.sha256((root / rel).read_bytes()).hexdigest() for rel in restore},
                    'childExit': r.returncode, 'passed': rep.get('passed'), 'failed': rep.get('failed'), 'failures': failures,
                    'error': rep.get('error')}
v1f = result['hybrid-v1ddl']['failures']
fzf = result['hybrid-frozenddl']['failures']
rtf = result['hybrid-routes']['failures']
result['expectations'] = {
    'hybrid-v1ddl fails': bool(v1f),
    'hybrid-v1ddl fails only storage-class controls': bool(v1f) and all(f.startswith('source37 storage') for f in v1f),
    'hybrid-v1ddl fails the root counterexample control': any('root counterexamples' in f for f in v1f),
    'hybrid-v1ddl fails NUL/BLOB controls for every hex column': all(
        any(('%s never stores a hostile value' % col) in f for f in v1f)
        for col in ('carrier_format.project_key_digest', 'carrier_format.migration_op_ref', 'grant_journal_v3.operation_ref',
                    'grant_journal_v3.run_id', 'grant_journal_v3.manifest_digest', 'grant_journal_v3.body_sha256',
                    'grant_journal_v3.prev_sha256', 'attempt_custody.store_generation_digest', 'attempt_custody.execution_id',
                    'attempt_custody.operation_ref')),
    'hybrid-v1ddl fails REAL controls': any('first_generation never stores' in f for f in v1f) and any('grantGeneration never stores' in f for f in v1f),
    'hybrid-v1ddl fails free-text BLOB controls': any('grant_journal_v3.body never stores' in f for f in v1f) and any('namespace_id never stores' in f for f in v1f),
    'hybrid-v1ddl keeps publication, scenario and route controls': not any(f.startswith('source37 scenario') or f.startswith('source37 route') for f in v1f),
    'hybrid-frozenddl fails storage, publication and scenario controls': any(f.startswith('source37 storage') for f in fzf)
        and any('refuses every grant_journal_v3 append' in f for f in fzf) and any(f.startswith('source37 scenario') for f in fzf),
    'hybrid-frozenddl fails only source37 controls': bool(fzf) and all(f.startswith('source37') for f in fzf),
    'hybrid-routes fails only route-row controls': bool(rtf) and all(f.startswith('source37 route') for f in rtf),
    'hybrid-routes keeps storage controls': not any(f.startswith('source37 storage') for f in rtf),
}
(BASE / 'receipts' / 'p04-discrimination.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
if not all(result['expectations'].values()):
    raise SystemExit(1)
