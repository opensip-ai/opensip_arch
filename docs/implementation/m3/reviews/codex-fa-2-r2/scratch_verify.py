"""Scratch selection check for FA-2 r2 with the product's own verify_design.py. Lead evidence, not the subject.

It reads tools/verify_design.py and design-lock.json from the product at LOCK_COMMIT with `git show` (read-only),
appends FA-2 r2 as one more contractSuccessors entry, and runs verify() against the real arch tree. FA-2 is not
accepted, so its review and assent are LABELLED SYNTHETIC ACCEPT records written only under the scratch directory.
The one change to the tool is a wrapper on relative_file that redirects exactly those two repo-relative paths to the
scratch copies. Every other read, and all of verify()'s logic, is the tool's. Nothing in arch or the product is
written. A pass shows the record is selectable once accepted; it is not acceptance.

Usage: python3.14 -I -B scratch_verify.py --product /path/to/opensip --scratch DIR
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import subprocess
from pathlib import Path

ARCH = Path(__file__).resolve().parents[5]
LOCK_COMMIT = 'cd5958b3608f44a0035566c9d4500e5005c62e91'
BASE = 'docs/implementation/m3/native-successors-fa'
SUBJECT = f'{BASE}/fa-2-subject.json'
RECORD = f'{BASE}/fa-2/successor.json'
REVIEW = 'docs/implementation/m3/reviews/codex-fa-2-r2/review.json'   # synthetic, scratch only
ASSENT = f'{BASE}/fa-2-unit.json'                                    # synthetic accepted form, scratch only


def pin(path, raw):
    return {'path': path, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--product', required=True)
    ap.add_argument('--scratch', required=True)
    args = ap.parse_args()
    scratch = Path(args.scratch)
    scratch.mkdir(parents=True, exist_ok=True)
    show = lambda p: subprocess.run(['git', '-C', args.product, 'show', f'{LOCK_COMMIT}:{p}'], check=True,
                                    capture_output=True).stdout
    (scratch / 'verify_design.py').write_bytes(show('tools/verify_design.py'))
    lock = json.loads(show('design-lock.json'))
    before = len(lock['contractSuccessors'])
    subject_raw, record_raw = (ARCH / SUBJECT).read_bytes(), (ARCH / RECORD).read_bytes()
    review = {'standing': 'SYNTHETIC scratch-only review for a selection check; not a review.',
              'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [],
              'subjectManifestSha256': hashlib.sha256(subject_raw).hexdigest(), 'successor': pin(RECORD, record_raw)}
    review_raw = (json.dumps(review, indent=2) + '\n').encode()
    assent = {'schemaVersion': 1, 'unit': 'native-successor-fa-2', 'status': 'ACCEPTED-DESIGN-UNIT',
              'standing': 'SYNTHETIC scratch-only assent for a selection check; not assent.',
              'subjectManifest': pin(SUBJECT, subject_raw), 'independentReview': pin(REVIEW, review_raw),
              'rootSubstantiveAssent': True, 'requiredUnitFindings': [], 'acceptedSuccessor': pin(RECORD, record_raw),
              'fullM2Complete': False, 'productQualification': False}
    assent_raw = (json.dumps(assent, indent=2) + '\n').encode()
    synthetic = {REVIEW: scratch / 'synthetic-review.json', ASSENT: scratch / 'synthetic-assent.json'}
    synthetic[REVIEW].write_bytes(review_raw)
    synthetic[ASSENT].write_bytes(assent_raw)
    lock['contractSuccessors'].append({'record': pin(RECORD, record_raw), 'subjectManifest': pin(SUBJECT, subject_raw),
                                       'review': pin(REVIEW, review_raw), 'assent': pin(ASSENT, assent_raw)})
    spec = importlib.util.spec_from_file_location('verify_design_scratch', scratch / 'verify_design.py')
    tool = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(tool)
    original = tool.relative_file

    def relative_file(root, value):
        if value in synthetic:
            return synthetic[value]
        return original(root, value)
    tool.relative_file = relative_file
    result = tool.verify(ARCH, lock)
    fa2 = next(r for r in result['contractSuccessors'] if r['selected'] == RECORD)
    print(json.dumps({'tool': f'tools/verify_design.py@{LOCK_COMMIT[:7]}', 'lock': f'design-lock.json@{LOCK_COMMIT[:7]}',
                      'contractSuccessorsBefore': before, 'contractSuccessorsAfter': len(lock['contractSuccessors']),
                      'passed': result['passed'], 'inputsVerified': result['inputsVerified'],
                      'fa2': {'selected': fa2['selected'], 'sha256': fa2['sha256'],
                              'candidates': len(fa2['inputs']), 'passageOverrides': len(fa2['passageOverrides']),
                              'passageSupersessions': len(fa2['passageSupersessions'])},
                      'subjectManifestSha256': review['subjectManifestSha256'],
                      'synthetic': {'review': review['standing'], 'assent': assent['standing']},
                      'writes': 'scratch directory only'}, indent=2))


if __name__ == '__main__':
    main()
