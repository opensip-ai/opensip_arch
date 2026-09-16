"""p01 <tree>: the two focused owner validators over one working tree (baseline or edited), never the global groups.

1. foundation/check-semantic-replay.v3.py (run-termination goldens and the host composition controls live here).
2. security/check-integrated-carrier.v1.py --source work/<tree> (carrier v3 checker incl. section 9 dispatch scenarios).
Reports go to receipts/p01-<tree>[.rN]/ and are never overwritten. Output summary: stdout.
"""
import json, subprocess, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source38-advisory-author.v1')
PY = '/tmp/opensip-architecture-review-env/bin/python'
tree = sys.argv[1]
T = BASE / 'work' / tree
n, out = 1, BASE / 'receipts' / ('p01-' + tree)
while out.exists():
    n += 1
    out = BASE / 'receipts' / ('p01-%s.r%d' % (tree, n))
out.mkdir(parents=True)
summary = {'tree': str(T), 'reportDir': str(out)}
sem = subprocess.run([PY, '-I', '-B', str(T / 'docs/coop/design-corrections/foundation/check-semantic-replay.v3.py'), '--output', str(out)],
                     capture_output=True, text=True, timeout=3000, cwd=str(out))
(out / 'semantic.stderr').write_text(sem.stderr)
rep = json.loads((out / 'grok-native-replay.v1.json').read_text()) if (out / 'grok-native-replay.v1.json').exists() else {}
rt = [c for c in rep.get('checks', []) if c.get('case', '').startswith('run-termination')]
summary['semanticReplay'] = {'exit': sem.returncode, 'passed': rep.get('passed'), 'count': rep.get('count'), 'blocked': rep.get('blocked'),
                             'runTerminationRows': len(rt), 'runTerminationFaults': {c['case']: c['faults'] for c in rt if c.get('faults')},
                             'stderrTail': sem.stderr[-1500:]}
car = subprocess.run([PY, '-I', '-B', str(T / 'docs/coop/design-corrections/security/check-integrated-carrier.v1.py'),
                      '--source', str(T), '--report', str(out / 'carrier.json')], capture_output=True, text=True, timeout=3000, cwd=str(out))
(out / 'carrier.stderr').write_text(car.stderr)
crep = json.loads((out / 'carrier.json').read_text()) if (out / 'carrier.json').exists() else {}
summary['carrier'] = {'exit': car.returncode, 'passed': crep.get('passed'), 'failed': crep.get('failed'),
                      'failedChecks': [c for c in crep.get('checks', []) if not c.get('ok', c.get('passed', True))][:40],
                      'stderrTail': car.stderr[-1500:]}
(out / 'summary.json').write_text(json.dumps(summary, indent=1) + '\n')
print(json.dumps(summary, indent=1)[:15000])
sys.exit(0 if sem.returncode == 0 and car.returncode == 0 else 1)
