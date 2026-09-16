"""Confirm the native lane's non-zero exit is PIN-ONLY, not semantic."""
import json, os, subprocess

REF = '/tmp/opensip-architecture-review-env/bin/python'
SRC = '/tmp/opensip-design-corrections/repair-selection-successor.v1/source'
HERE = os.path.dirname(os.path.abspath(__file__))
cwd = os.path.join(SRC, 'docs/coop/design-corrections/native')
p = subprocess.run([REF, '-I', '-B', os.path.join(cwd, 'check_native_evidence.v2.py')],
                   capture_output=True, text=True, cwd=cwd, timeout=1800)
print('exit', p.returncode)
raw = p.stdout.strip()
try:
    doc = json.loads(raw)
except Exception:
    print(raw[-2500:])
    raise SystemExit(1)

faults = doc if isinstance(doc, list) else doc.get('faults', doc)
kinds = sorted({f.get('fault') for f in faults}) if isinstance(faults, list) else ['<not a list>']
print('fault records:', len(faults) if isinstance(faults, list) else '?')
print('distinct fault kinds:', kinds)
print('paths:')
for f in (faults if isinstance(faults, list) else []):
    print('  ', f.get('fault'), '|', f.get('path'))
json.dump({'exitCode': p.returncode, 'faults': faults, 'distinctFaultKinds': kinds,
           'pinOnly': kinds == ['sha256 mismatch']},
          open(os.path.join(HERE, 'native-lane-detail.json'), 'w'), indent=2)
print('\npinOnly:', kinds == ['sha256 mismatch'])
