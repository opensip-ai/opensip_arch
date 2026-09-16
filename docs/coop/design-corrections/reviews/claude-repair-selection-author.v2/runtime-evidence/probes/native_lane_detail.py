"""Record PRECISELY what the native lane did: it stopped at PIN ADMISSION.

It reported sha256 pin mismatches and did NOT proceed to its semantic checks. The absence of
reported semantic faults is therefore NOT evidence that those checks passed. Root assesses the
sealed integrated run.
"""
import json, os

HERE = os.path.dirname(os.path.abspath(__file__))
r = json.load(open(os.path.join(HERE, 'receipts', 'check_native_evidence.v2.receipt.json')))
out = r['stdout'].strip()
try:
    faults = json.loads(out)
except Exception:
    faults = None

kinds = sorted({f.get('fault') for f in faults}) if isinstance(faults, list) else None
doc = {
    'lane': 'native/check_native_evidence.v2.py',
    'exitCode': r['exitCode'],
    'stoppedAt': 'pin admission',
    'reported': 'sha256 pin mismatches only',
    'distinctFaultKinds': kinds,
    'faultPaths': [f.get('path') for f in faults] if isinstance(faults, list) else None,
    'semanticChecksExecuted': False,
    'precision': ('The lane stopped at pin admission and did not execute its subsequent '
                  'semantic checks. Absence of reported semantic faults is NOT evidence that '
                  'those checks passed.'),
    'fullStdout': out,
    'stderr': r['stderr'],
}
json.dump(doc, open(os.path.join(HERE, 'native-lane-detail.json'), 'w'), indent=2)
print('exit', doc['exitCode'], '| kinds', kinds)
print('paths:')
for p in (doc['faultPaths'] or []):
    print('  ', p)
print('semanticChecksExecuted:', doc['semanticChecksExecuted'])
