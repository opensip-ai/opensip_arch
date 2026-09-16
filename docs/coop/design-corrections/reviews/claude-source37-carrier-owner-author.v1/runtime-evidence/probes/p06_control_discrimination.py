"""Show the new source37 controls discriminate: run the EDITED validator over two hybrid trees that restore baseline
bytes for exactly one remedy area each, and record which checks fail.

  hybrid-ddl     edited tree, but baseline grant-journal.carrier.v3.sql and attempt-custody.schema.v1.json
                 (expect source37 grammar / publication / scenario failures; route rows still agree)
  hybrid-routes  edited tree, but baseline security-and-lifecycle.md and commit-recovery-readonly.v3.md
                 (expect source37 S12 / read-only row failures; DDL controls still pass)

Hybrids are new disposable directories; baseline and edited copies are only read.
"""
import hashlib, json, shutil, subprocess, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v1')
BL, ED = BASE / 'work/baseline', BASE / 'work/edited'
HYBRIDS = {
    'hybrid-ddl': ['docs/coop/design-corrections/security/grant-journal.carrier.v3.sql',
                   'docs/v2/architecture/attempt-custody.schema.v1.json'],
    'hybrid-routes': ['docs/v2/contracts/product-v1/security-and-lifecycle.md',
                      'docs/v2/architecture/commit-recovery-readonly.v3.md'],
}
result = {}
for name, restore in HYBRIDS.items():
    root = BASE / 'work' / name
    shutil.copytree(ED, root, symlinks=True, dirs_exist_ok=False)
    for rel in restore:
        shutil.copyfile(BL / rel, root / rel)
    report = BASE / 'receipts' / ('p06-integrated-carrier.' + name + '.json')
    if report.exists():
        raise SystemExit('preserve earlier report: ' + str(report))
    r = subprocess.run([sys.executable, '-I', '-B', str(root / 'docs/coop/design-corrections/security/check-integrated-carrier.v1.py'),
                        '--source', str(root), '--report', str(report)], capture_output=True, text=True, timeout=900)
    rep = json.loads(report.read_text()) if report.exists() else {'error': r.stderr[-2000:]}
    failures = [c['check'] for c in rep.get('checks', []) if not c['pass']]
    result[name] = {
        'restoredBaselineFiles': {rel: hashlib.sha256((root / rel).read_bytes()).hexdigest() for rel in restore},
        'childExit': r.returncode, 'passed': rep.get('passed'), 'failed': rep.get('failed'),
        'failures': failures, 'allFailuresAreSource37Controls': bool(failures) and all(f.startswith('source37') for f in failures),
        'error': rep.get('error'),
    }
ddl_fail = result['hybrid-ddl']['failures']
route_fail = result['hybrid-routes']['failures']
result['expectations'] = {
    'hybrid-ddl fails grammar controls': any('refuses an uppercase or non-hex' in f for f in ddl_fail),
    'hybrid-ddl fails publication controls': any('refuses every grant_journal_v3 append' in f for f in ddl_fail),
    'hybrid-ddl fails first_generation coupling': any('first_generation is exactly 1' in f for f in ddl_fail),
    'hybrid-ddl fails interrupted-state scenarios': any(f.startswith('source37 scenario') for f in ddl_fail),
    'hybrid-ddl keeps route rows agreeing': not any('S12 row' in f or 'section 1 row' in f for f in ddl_fail),
    'hybrid-routes fails S12 row controls': any('S12 row' in f for f in route_fail),
    'hybrid-routes fails read-only table controls': any('section 1 row' in f for f in route_fail),
    'hybrid-routes keeps DDL controls passing': not any('grant_journal_v3.' in f or 'attempt_custody' in f for f in route_fail),
    'only source37 controls fail': result['hybrid-ddl']['allFailuresAreSource37Controls'] and result['hybrid-routes']['allFailuresAreSource37Controls'],
}
(BASE / 'receipts' / 'p06-control-discrimination.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
if not all(result['expectations'].values()):
    raise SystemExit(1)
