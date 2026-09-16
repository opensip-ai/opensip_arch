"""p04 <tree>: the two affected focused owner validators over one v2 tree (edited), never the global groups.

1. foundation/check-semantic-replay.v3.py (run-termination goldens incl. host-composition-boundary).
2. security/check-integrated-carrier.v1.py --source <tree> (carrier v3 checker incl. section 9 read-only scenarios).
Reports: receipts/p04-<tree>[.rN]/ (never overwritten). Summary on stdout and in summary.json.
"""
import json, subprocess, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source38-advisory-author.v2')
PY = '/tmp/opensip-architecture-review-env/bin/python'
tree = sys.argv[1]
T = BASE / 'work' / tree
n, out = 1, BASE / 'receipts' / ('p04-' + tree)
while out.exists():
    n += 1
    out = BASE / 'receipts' / ('p04-%s.r%d' % (tree, n))
out.mkdir(parents=True)
summary = {'tree': str(T), 'reportDir': str(out)}
sem = subprocess.run([PY, '-I', '-B', str(T / 'docs/coop/design-corrections/foundation/check-semantic-replay.v3.py'), '--output', str(out)],
                     capture_output=True, text=True, timeout=3000, cwd=str(out))
(out / 'semantic.stderr').write_text(sem.stderr)
rep = json.loads((out / 'grok-native-replay.v1.json').read_text()) if (out / 'grok-native-replay.v1.json').exists() else {}
rows = rep.get('checks', [])
comp = [c for c in rows if c.get('case') == 'run-termination:host-composition-boundary']
summary['semanticReplay'] = {'exit': sem.returncode, 'passed': rep.get('passed'), 'count': rep.get('count'), 'blocked': rep.get('blocked'),
                             'runTerminationFaults': {c['case']: c['faults'] for c in rows if c.get('case', '').startswith('run-termination') and c.get('faults')},
                             'compositionCases': [(c['label'], c.get('composition'), c.get('pureProjection'), c.get('error')) for c in (comp[0]['composition'] if comp else [])],
                             'stderrTail': sem.stderr[-2000:]}
car = subprocess.run([PY, '-I', '-B', str(T / 'docs/coop/design-corrections/security/check-integrated-carrier.v1.py'),
                      '--source', str(T), '--report', str(out / 'carrier.json')], capture_output=True, text=True, timeout=3000, cwd=str(out))
(out / 'carrier.stderr').write_text(car.stderr)
crep = json.loads((out / 'carrier.json').read_text()) if (out / 'carrier.json').exists() else {}
checks = crep.get('checks', [])
summary['carrier'] = {'exit': car.returncode, 'passed': crep.get('passed'), 'failed': crep.get('failed'),
                      'failedChecks': [(c['check'], str(c.get('detail'))[:300]) for c in checks if not c['pass']],
                      'followUpChecks': [(c['check'], c['pass']) for c in checks if 'absent' in c['check'] or 'unknown-custody' in c['check']],
                      'stderrTail': (car.stderr or car.stdout)[-2000:]}
(out / 'summary.json').write_text(json.dumps(summary, indent=1) + '\n')
print(json.dumps(summary, indent=1)[:20000])
sys.exit(0 if sem.returncode == 0 and car.returncode == 0 else 1)
