"""Scratch-only: run a product worktree's real verify_design over a lock that
selects inventory135, with a synthetic review and assent held in memory
(SCRATCH-P0/ paths). Nothing is written to either repository. It proves only
that everything except the missing independent review and root assent
passes.

The parent is inventory134 (unit L1), selected at product cd5958b with its
fifty-five inheritance rows. The re-projected inheritance has one hundred
rows: the fifty-five plus D3's forty-five direct overrides on inventory134,
with D3's seventeen supersessions folded.

Two modes, chosen by the worktree's lock (as F8b's verify_scratch_f8b.py):
- appended: the lock does not select inventory135, so the binding and the
  re-projected inheritance are applied in memory;
- staged: the lock's last inventory successor is inventory135 (the
  uncommitted opensip-p0 worktree, written by evidence/stage_lock_v135.py).
  The staged lock must equal HEAD's lock plus exactly that entry and that
  inheritance, in the lock's canonical formatting; its review and assent pins
  must be the SCRATCH-P0 placeholders, which only this overlay serves. Plain
  verify_design must refuse that lock at the review placeholder, and this
  script checks that it does.

In both modes the lock without inventory135 must pass, the lock with it must
pass, inventory135 must be selected with exactly one more inventory
successor, the contract successors and supersession count must be unchanged,
and verify_design's own projected inheritance must equal the record's.
Usage: verify_scratch.py [WORKTREE]."""
import copy, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
A = Path('/Users/sb/code/opensip-ai/opensip_arch')
M = 'docs/implementation/m2/'
U = M + 'm3-p0-scaffolds-inventory-v135'
CANDIDATE = M + 'repository-file-inventory.v135.json'

def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def binding_for(parent):
    """The inventory135 lock entry with SCRATCH-P0 review and assent pins, the
    synthetic bytes those pins name, and the re-projected inheritance."""
    candidate, record, subject = pin(CANDIDATE), pin(U + '/successor.json'), pin(U + '-subject.json')
    assert json.loads((A / record['path']).read_bytes())['parent'] == parent, 'inventory135 must be built on the selected inventory'
    review = json.dumps({'verdict': 'ACCEPT-UNIT', 'requiredFindings': [], 'subjectManifestSha256': subject['sha256'],
        'inventoryCandidateAssessment': {'verdict': 'ACCEPT', 'requiredFindings': [], **candidate, 'parent': parent, 'successorRecord': record}}).encode()
    rpin = {'path': 'SCRATCH-P0/review.json', 'bytes': len(review), 'sha256': hashlib.sha256(review).hexdigest()}
    assent = json.dumps({'status': 'ACCEPTED-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [], 'subjectManifest': subject,
        'independentReview': rpin, 'acceptedInventory': candidate}).encode()
    apin = {'path': 'SCRATCH-P0/assent.json', 'bytes': len(assent), 'sha256': hashlib.sha256(assent).hexdigest()}
    binding = {'parent': parent, 'candidate': candidate, 'record': record, 'review': rpin, 'assent': apin}
    rows = json.loads((A / record['path']).read_text())['descriptionOverrideProjection']
    inheritance = sorted(
        ({'parent': candidate, 'selector': r['candidateSelector'], 'before': r['before'], 'after': r['effectiveDescription']} for r in rows),
        key=lambda o: json.dumps(o['selector'], sort_keys=True))
    return binding, inheritance, {rpin['path']: review, apin['path']: assent}

def head_lock(worktree):
    return json.loads(subprocess.run(['git', '-C', str(worktree), 'show', 'HEAD:design-lock.json'],
                                     capture_output=True, check=True).stdout)

def staged(base):
    """HEAD's lock plus the inventory135 entry and the re-projected inheritance."""
    assert all(s['candidate']['path'] != CANDIDATE for s in base['inventorySuccessors']), 'HEAD already selects inventory135'
    binding, inheritance, _ = binding_for(base['inventorySuccessors'][-1]['candidate'])
    lock = copy.deepcopy(base)
    lock['inventorySuccessors'].append(binding)
    lock['inventoryPassageInheritance'] = inheritance
    return lock

def canonical(lock):
    return json.dumps(lock, indent=2, ensure_ascii=True) + '\n'

def main():
    W = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip-p0').resolve(strict=True)
    spec = importlib.util.spec_from_file_location('vd', W / 'tools/verify_design.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    base = head_lock(W)
    raw = (W / 'design-lock.json').read_text()
    current = json.loads(raw)
    if current['inventorySuccessors'][-1]['candidate']['path'] == CANDIDATE:
        mode = 'staged'
        lock = staged(base)
        assert current == lock, 'the staged lock is not HEAD plus exactly the inventory135 entry and inheritance'
        assert raw == canonical(lock), 'the staged lock is not in canonical formatting'
        # Plain verify_design refuses at the first SCRATCH placeholder.
        try:
            m.verify(A, current, W)
        except m.DesignError as exc:
            plain = str(exc)
        else:
            raise AssertionError('plain verify_design accepted SCRATCH placeholders')
        assert 'SCRATCH-P0/review.json' in plain, plain
    else:
        mode, plain = 'appended', None
        assert current == base, 'the worktree lock differs from HEAD without selecting inventory135'
        lock = staged(base)
    _, inheritance, synthetic = binding_for(base['inventorySuccessors'][-1]['candidate'])
    real = m.pinned_bytes
    def pinned_bytes(root, row):
        if isinstance(row, dict) and row.get('path') in synthetic:
            data = synthetic[row['path']]; assert hashlib.sha256(data).hexdigest() == row['sha256'] and len(data) == row['bytes']; return data
        return real(root, row)
    m.pinned_bytes = pinned_bytes
    before = m.verify(A, base, W)
    result = m.verify(A, lock, W)
    assert before['passed'] is True and result['passed'] is True
    assert len(result['inventorySuccessors']) == len(before['inventorySuccessors']) + 1
    assert result['selectedInventory']['path'] == CANDIDATE and before['selectedInventory'] == base['inventorySuccessors'][-1]['candidate']
    assert len(result['contractSuccessors']) == len(before['contractSuccessors'])
    assert result['inventoryPassageSupersessions'] == before['inventoryPassageSupersessions']
    assert result['inventoryPassageInheritance'] == inheritance == lock['inventoryPassageInheritance'], 'verify_design projects a different inheritance'
    print(json.dumps({'mode': mode, 'passed': result['passed'], 'plainVerifyDesignRefusal': plain,
                      'inventorySuccessors': [len(before['inventorySuccessors']), len(result['inventorySuccessors'])],
                      'contractSuccessors': len(result['contractSuccessors']),
                      'inventoryPassageInheritance': [len(before['inventoryPassageInheritance']), len(result['inventoryPassageInheritance'])],
                      'inventoryPassageSupersessions': result['inventoryPassageSupersessions'],
                      'selectedInventory': result['selectedInventory']['path']}, indent=1))

if __name__ == '__main__':
    main()
