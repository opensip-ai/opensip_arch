"""Discrimination: run the v3 EDITED validator over hybrid trees that restore exactly one earlier remedy area each.

  hybrid-v2ddl      v3 tree + v2-final DDL and attempt-custody bytes  expect only storage controls to fail, concentrated in
                    UTF-16 lawful admission, the UTF-16 migration scenario and the no-byte-length structural check
  hybrid-frozenddl  v3 tree + frozen37 DDL and attempt-custody bytes  expect storage, publication and scenario controls to fail
  hybrid-routes     v3 tree + frozen37 S12 and read-only table        expect only S12 / read-only route-row controls to fail
Hybrids are new directories in this runtime; frozen37, v2final and edited trees are only read.
"""
import hashlib, json, shutil, subprocess, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v3')
W = BASE / 'work'
DDL = 'docs/coop/design-corrections/security/grant-journal.carrier.v3.sql'
AC = 'docs/v2/architecture/attempt-custody.schema.v1.json'
S12 = 'docs/v2/contracts/product-v1/security-and-lifecycle.md'
RO = 'docs/v2/architecture/commit-recovery-readonly.v3.md'
HYBRIDS = {'hybrid-v2ddl': ('v2final', [DDL, AC]), 'hybrid-frozenddl': ('frozen37', [DDL, AC]), 'hybrid-routes': ('frozen37', [S12, RO])}
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
                        '--source', str(root), '--report', str(report)], capture_output=True, text=True, timeout=1200)
    rep = json.loads(report.read_text()) if report.exists() else {'error': r.stderr[-2000:]}
    failures = [c['check'] for c in rep.get('checks', []) if not c['pass']]
    result[name] = {'restoredFrom': src, 'restored': {rel: hashlib.sha256((root / rel).read_bytes()).hexdigest() for rel in restore},
                    'childExit': r.returncode, 'passed': rep.get('passed'), 'failed': rep.get('failed'), 'failures': failures,
                    'error': rep.get('error')}
v2f = result['hybrid-v2ddl']['failures']
fzf = result['hybrid-frozenddl']['failures']
rtf = result['hybrid-routes']['failures']
result['expectations'] = {
    'hybrid-v2ddl fails': bool(v2f),
    'hybrid-v2ddl fails only storage controls': bool(v2f) and all(f.startswith('source37 storage') for f in v2f),
    'hybrid-v2ddl fails UTF-16 lawful admission for every table': all(
        any(f.startswith('source37 storage: %s' % t) and '[%s] admits every canonical lawful value' % e in f for f in v2f)
        for t in ('carrier_format.', 'grant_journal_v3.', 'attempt_custody.') for e in ('UTF-16le', 'UTF-16be')),
    'hybrid-v2ddl fails the UTF-16 migration scenario': all(any(('a %s carrierFormat 2 carrier migrates' % e) in f for f in v2f) for e in ('UTF-16le', 'UTF-16be')),
    'hybrid-v2ddl fails the no-byte-length structural check': any('encoding-dependent byte-length' in f for f in v2f),
    'hybrid-v2ddl has no UTF-8 canonical or hostile failure': not any('[UTF-8]' in f for f in v2f),
    'hybrid-v2ddl keeps publication, scenario and route controls': not any(f.startswith('source37 scenario') or f.startswith('source37 route') for f in v2f),
    'hybrid-frozenddl fails storage, publication and scenario controls': any(f.startswith('source37 storage') for f in fzf)
        and any('refuses every grant_journal_v3 append' in f for f in fzf) and any(f.startswith('source37 scenario') for f in fzf),
    'hybrid-frozenddl fails NUL/BLOB controls in every encoding': all(any(('[%s] never stores a hostile value' % e) in f for f in fzf) for e in ('UTF-8', 'UTF-16le', 'UTF-16be')),
    'hybrid-frozenddl fails only source37 controls': bool(fzf) and all(f.startswith('source37') for f in fzf),
    'hybrid-routes fails only route-row controls': bool(rtf) and all(f.startswith('source37 route') for f in rtf),
    'hybrid-routes keeps storage controls': not any(f.startswith('source37 storage') for f in rtf),
}
(BASE / 'receipts' / 'p04-discrimination.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({k: ({kk: vv for kk, vv in v.items() if kk != 'failures'} | {'failuresFirst12': v['failures'][:12]} if k != 'expectations' else v)
                  for k, v in result.items()}, indent=2))
if not all(result['expectations'].values()):
    raise SystemExit(1)
