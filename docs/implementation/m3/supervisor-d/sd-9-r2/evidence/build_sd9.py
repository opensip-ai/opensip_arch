"""Build SD-9's subject manifest and the lead's draft unit record, after re-running check_sd9.py and requiring its
output to equal the archived check_sd9.output.json byte for byte.

Usage: build_sd9.py [--product PATH] [--rev REV] [--check]
- PATH and REV are passed to check_sd9.py (defaults /Users/sb/code/opensip-ai/opensip and 274dccc), read only.
- Without --check the subject manifest and the unit draft are written. With --check nothing is written: each is
  rebuilt in memory and compared with the bytes on disk.

Deterministic. Run with python3 -I -B. Generated: ../sd-9-r2-subject.json and ../sd-9-r2-unit.json (the unit record is not
part of the subject).
"""
import hashlib, json, subprocess, sys
from pathlib import Path

A = Path(__file__).resolve().parents[6]
args = list(sys.argv[1:])
CHECK = '--check' in args
passthrough = [a for a in args if a != '--check']
B = 'docs/implementation/m3/supervisor-d/'
D = B + 'sd-9-r2/'
REVIEW = 'docs/implementation/m3/reviews/codex-sd-9-r2/review.json'
PRIOR = ['docs/implementation/m3/reviews/codex-sd-9-r1/REQUEST.md', 'docs/implementation/m3/reviews/codex-sd-9-r1/REVIEW.md',
         'docs/implementation/m3/reviews/codex-sd-9-r1/review.json', B + 'sd-9-subject.json']
# The architecture head the record was drafted against (it must exist; later heads add no SD-9 input).
ARCH_BASE = 'c6c7d4acf0d4836ef3bb72cb2bcb8950a75530a2'
subprocess.run(['git', '-C', str(A), 'cat-file', '-e', ARCH_BASE + '^{commit}'], check=True)


def pin(path):
    raw = (A / path).read_bytes()
    return {'path': path, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


fresh = subprocess.run([sys.executable, '-I', '-B', str(A / D / 'evidence/check_sd9.py'), *passthrough], check=True,
                       capture_output=True).stdout
assert fresh == (A / D / 'evidence/check_sd9.output.json').read_bytes(), 'check_sd9.output.json is stale'
report = json.loads(fresh)
members = [D + 'README.md', D + 'evidence/build_sd9.py', D + 'evidence/check_sd9.py', D + 'evidence/check_sd9.output.json']
on_disk = sorted(p.relative_to(A).as_posix() for p in (A / D).rglob('*') if p.is_file() and '__pycache__' not in p.parts)
assert on_disk == sorted(members), on_disk
subject = {'schemaVersion': 1, 'unit': 'SD-9-r2', 'productBase': report['productRev'],
           'architectureBase': ARCH_BASE,
           'files': [pin(m) for m in sorted(members)],
           'priorRound': [pin(m) for m in PRIOR]}
outputs = {B + 'sd-9-r2-subject.json': (json.dumps(subject, indent=2) + '\n').encode()}
subject_pin = {'path': B + 'sd-9-r2-subject.json', 'bytes': len(outputs[B + 'sd-9-r2-subject.json']),
               'sha256': hashlib.sha256(outputs[B + 'sd-9-r2-subject.json']).hexdigest()}
unit = {
    'schemaVersion': 1,
    'unit': 'supervisor-d-sd-9',
    'status': 'DRAFT-PENDING-REVIEW',
    'form': 'law record (M3-D item 29 successor; J1 law content); no contract successor, no lock binding',
    'subjectManifest': subject_pin,
    'independentReview': {'path': REVIEW},
    'rootSubstantiveAssent': False,
    'requiredUnitFindings': None,
    'interimCaps': {'constructor': 'WorkLedger::snapshot_profile()', 'objects': report['prices']['caps']['snapshot']['object'],
                    'edges': report['prices']['caps']['snapshot']['edge'], 'bytes': report['prices']['caps']['snapshot']['byte'],
                    'standing': 'explicit interim policy on the X-CI-1 precedent; gate X-SD9-1'},
    'gates': ['C2a-4', 'production R10a and ER10a composition', 'J3d R10a wiring', 'J2c ER10a wiring'],
    'carriedGates': {'X-SD9-1': 'interim standing ends in census outcome E, V or N (README section 5)',
                     'X-SD9-2': 'priced M, final accepted CI bounds and implemented D4 bounds before any complete census or fit claim'},
    'capSourceRule': 'E census-derived (equal); V census-validated reused policy (never recorded as census-derived); N new census-derived profile',
    'priorRounds': [{'review': 'docs/implementation/m3/reviews/codex-sd-9-r1/review.json', 'verdict': 'REQUIRED-FINDINGS',
                     'findings': ['SD9-R1-RF-1', 'SD9-R1-RF-2']}],
    'productCodeUnchanged': True,
    'productQualification': False,
}
outputs[B + 'sd-9-r2-unit.json'] = (json.dumps(unit, indent=2) + '\n').encode()
for path, raw in outputs.items():
    if CHECK:
        assert (A / path).read_bytes() == raw, path + ' differs'
    else:
        (A / path).write_bytes(raw)
print(json.dumps({'checked' if CHECK else 'written': sorted(outputs), 'subject': subject_pin}, indent=2))
