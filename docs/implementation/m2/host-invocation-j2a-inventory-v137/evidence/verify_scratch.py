"""Scratch-only: run a product worktree's real verify_design over a lock that
selects inventory137, with a synthetic review and assent held in memory
(SCRATCH-J2A/ paths). Nothing is written to either repository. It proves
only that everything except the missing independent review and root assent
passes.

The parent is inventory136 (unit X3a-2), selected at product cca4fe4 and
still at d2c00a9, with its one hundred inheritance rows and the three direct
overrides of the bound description successor read-endpoint-x3a2-descriptions.
The re-projected inheritance has one hundred and three rows on inventory137.
Unit J2a binds no contract successor.

Two modes, chosen by the worktree's lock (as P0's verify_scratch.py):
- appended: the lock does not select inventory137, so the binding and the
  re-projected inheritance are applied in memory;
- staged: the lock's last inventory successor is inventory137 (the
  uncommitted opensip-j2a worktree, written by evidence/stage_lock_j2a.py).
  The staged lock must equal HEAD's lock plus exactly that entry and that
  inheritance, in the lock's canonical formatting; its review and assent pins
  must be the SCRATCH-J2A placeholders, which only this overlay serves. Plain
  verify_design must refuse that lock at the review placeholder, and this
  script checks that it does.

In both modes the lock without inventory137 must pass, the lock with it must
pass, inventory137 must be selected with exactly one more inventory
successor, the contract successors, the contract passage supersessions and
the inventory supersession count must be unchanged, and verify_design's own
projected inheritance must equal the record's.
Usage: verify_scratch.py [WORKTREE]."""
import copy, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
A = Path('/Users/sb/code/opensip-ai/opensip_arch')
M = 'docs/implementation/m2/'
U = M + 'host-invocation-j2a-inventory-v137'
CANDIDATE = M + 'repository-file-inventory.v137.json'

def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def binding_for(parent):
    """The inventory137 lock entry with SCRATCH-J2A review and assent pins, the
    synthetic bytes those pins name, and the re-projected inheritance."""
    candidate, record, subject = pin(CANDIDATE), pin(U + '/successor.json'), pin(U + '-subject.json')
    assert json.loads((A / record['path']).read_bytes())['parent'] == parent, 'inventory137 must be built on the selected inventory'
    review = json.dumps({'verdict': 'ACCEPT-UNIT', 'requiredFindings': [], 'subjectManifestSha256': subject['sha256'],
        'inventoryCandidateAssessment': {'verdict': 'ACCEPT', 'requiredFindings': [], **candidate, 'parent': parent, 'successorRecord': record}}).encode()
    rpin = {'path': 'SCRATCH-J2A/review.json', 'bytes': len(review), 'sha256': hashlib.sha256(review).hexdigest()}
    assent = json.dumps({'status': 'ACCEPTED-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [], 'subjectManifest': subject,
        'independentReview': rpin, 'acceptedInventory': candidate}).encode()
    apin = {'path': 'SCRATCH-J2A/assent.json', 'bytes': len(assent), 'sha256': hashlib.sha256(assent).hexdigest()}
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
    """HEAD's lock plus the inventory137 entry and the re-projected inheritance."""
    assert all(s['candidate']['path'] != CANDIDATE for s in base['inventorySuccessors']), 'HEAD already selects inventory137'
    binding, inheritance, _ = binding_for(base['inventorySuccessors'][-1]['candidate'])
    lock = copy.deepcopy(base)
    lock['inventorySuccessors'].append(binding)
    lock['inventoryPassageInheritance'] = inheritance
    return lock

def canonical(lock):
    return json.dumps(lock, indent=2, ensure_ascii=True) + '\n'

def main():
    W = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip-j2a').resolve(strict=True)
    spec = importlib.util.spec_from_file_location('vd', W / 'tools/verify_design.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    base = head_lock(W)
    raw = (W / 'design-lock.json').read_text()
    current = json.loads(raw)
    if current['inventorySuccessors'][-1]['candidate']['path'] == CANDIDATE:
        mode = 'staged'
        lock = staged(base)
        assert current == lock, 'the staged lock is not HEAD plus exactly the inventory137 entry and inheritance'
        assert raw == canonical(lock), 'the staged lock is not in canonical formatting'
        # Plain verify_design refuses at the first SCRATCH placeholder.
        try:
            m.verify(A, current, W)
        except m.DesignError as exc:
            plain = str(exc)
        else:
            raise AssertionError('plain verify_design accepted SCRATCH placeholders')
        assert 'SCRATCH-J2A/review.json' in plain, plain
    else:
        mode, plain = 'appended', None
        assert current == base, 'the worktree lock differs from HEAD without selecting inventory137'
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
    assert result.get('contractPassageSupersessions') == before.get('contractPassageSupersessions')
    assert result['inventoryPassageInheritance'] == inheritance == lock['inventoryPassageInheritance'], 'verify_design projects a different inheritance'
    print(json.dumps({'mode': mode, 'passed': result['passed'], 'plainVerifyDesignRefusal': plain,
                      'inventorySuccessors': [len(before['inventorySuccessors']), len(result['inventorySuccessors'])],
                      'contractSuccessors': len(result['contractSuccessors']),
                      'inventoryPassageInheritance': [len(before['inventoryPassageInheritance']), len(result['inventoryPassageInheritance'])],
                      'inventoryPassageSupersessions': result['inventoryPassageSupersessions'],
                      'contractPassageSupersessions': result.get('contractPassageSupersessions'),
                      'selectedInventory': result['selectedInventory']['path'],
                      'generationSources': result.get('generationSources'), 'admissionSources': result.get('admissionSources')}, indent=1))

if __name__ == '__main__':
    main()
