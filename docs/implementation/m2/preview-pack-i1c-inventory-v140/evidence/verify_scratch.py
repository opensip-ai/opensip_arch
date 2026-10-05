"""Scratch-only: run a product worktree's real verify_design over a lock that
selects inventory140 (unit I1-c), with synthetic reviews and assents held in
memory. Nothing is written to either repository. It proves only that
everything except the missing independent reviews and root assents passes.

The parent is inventory139 (unit J3a), which is not yet integrated. While
HEAD's lock selects inventory138, J3a's staged entry (its own
evidence/verify_scratch.py, with SCRATCH-J3A placeholders) comes first, then
I1-c's entry (SCRATCH-I1C placeholders); once J3a is integrated, HEAD's lock
selects inventory139 and only I1-c's entry is added. Either way the
re-projected inheritance has one hundred and three rows on inventory140.
I1-c has no contract successor.

Two modes, chosen by the worktree's lock (as E2a's verify_scratch.py):
- appended: the lock is HEAD's, so the entries and the re-projected
  inheritance are applied in memory;
- staged: the lock's last inventory successor is inventory140 (the
  uncommitted opensip-i1c worktree, written by evidence/stage_lock_i1c.py).
  The staged lock must equal HEAD's plus exactly those entries and that
  inheritance, in the lock's canonical formatting. Plain verify_design must
  refuse it at the first review placeholder, which this overlay alone serves.

In both modes HEAD's lock, the lock with inventory139 and the lock with
inventory140 must pass. inventory140 must be selected with exactly one more
inventory successor than the inventory139 lock and the same contract
successors; both supersession counts must be unchanged; and verify_design's
own projected inheritance must equal the record's.
Usage: verify_scratch.py [WORKTREE]."""
import copy, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
A = Path('/Users/sb/code/opensip-ai/opensip_arch')
M = 'docs/implementation/m2/'
U = M + 'preview-pack-i1c-inventory-v140'
CANDIDATE = M + 'repository-file-inventory.v140.json'
PARENT = M + 'repository-file-inventory.v139.json'
J3A = M + 'durable-entry-j3a-inventory-v139'

def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def synthetic_pin(path, data):
    return {'path': path, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def j3a_module():
    spec = importlib.util.spec_from_file_location('j3a_scratch', A / J3A / 'evidence/verify_scratch.py')
    module = importlib.util.module_from_spec(spec); spec.loader.exec_module(module)
    return module

def with_parent(base):
    """The lock selecting inventory139 and the synthetic bytes it needs: HEAD's
    once J3a is integrated, else HEAD's plus J3a's staged entry."""
    if base['inventorySuccessors'][-1]['candidate']['path'] == PARENT:
        return copy.deepcopy(base), {}, 'integrated'
    _, lock, synthetic, _ = j3a_module().scenario(base)
    return lock, synthetic, 'staged-in-memory'

def bindings_for(parent):
    """The inventory140 lock entry with SCRATCH-I1C review and assent pins;
    the synthetic bytes those pins name; and the re-projected inheritance."""
    candidate, record, subject = pin(CANDIDATE), pin(U + '/successor.json'), pin(U + '-subject.json')
    assert json.loads((A / record['path']).read_bytes())['parent'] == parent, 'inventory140 must be built on inventory139'
    review = json.dumps({'verdict': 'ACCEPT-UNIT', 'requiredFindings': [], 'subjectManifestSha256': subject['sha256'],
        'inventoryCandidateAssessment': {'verdict': 'ACCEPT', 'requiredFindings': [], **candidate, 'parent': parent, 'successorRecord': record}}).encode()
    rpin = synthetic_pin('SCRATCH-I1C/review.json', review)
    assent = json.dumps({'status': 'ACCEPTED-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [], 'subjectManifest': subject,
        'independentReview': rpin, 'acceptedInventory': candidate}).encode()
    apin = synthetic_pin('SCRATCH-I1C/assent.json', assent)
    inventory = {'parent': parent, 'candidate': candidate, 'record': record, 'review': rpin, 'assent': apin}
    rows = json.loads((A / record['path']).read_text())['descriptionOverrideProjection']
    inheritance = sorted(
        ({'parent': candidate, 'selector': r['candidateSelector'], 'before': r['before'], 'after': r['effectiveDescription']} for r in rows),
        key=lambda o: json.dumps(o['selector'], sort_keys=True))
    synthetic = {rpin['path']: review, apin['path']: assent}
    return inventory, inheritance, synthetic

def head_lock(worktree):
    return json.loads(subprocess.run(['git', '-C', str(worktree), 'show', 'HEAD:design-lock.json'],
                                     capture_output=True, check=True).stdout)

def scenario(base):
    """(the inventory139 lock, the inventory140 lock, every synthetic byte, J3a's mode)."""
    assert all(s['candidate']['path'] != CANDIDATE for s in base['inventorySuccessors']), 'HEAD already selects inventory140'
    parent_lock, synthetic, mode = with_parent(base)
    assert parent_lock['inventorySuccessors'][-1]['candidate']['path'] == PARENT
    inventory, inheritance, mine = bindings_for(parent_lock['inventorySuccessors'][-1]['candidate'])
    lock = copy.deepcopy(parent_lock)
    lock['inventorySuccessors'].append(inventory)
    lock['inventoryPassageInheritance'] = inheritance
    return parent_lock, lock, {**synthetic, **mine}, mode

def staged(base):
    """HEAD's lock plus (J3a's entry, while unintegrated, and) the inventory140
    entry, with the re-projected inheritance."""
    return scenario(base)[1]

def canonical(lock):
    return json.dumps(lock, indent=2, ensure_ascii=True) + '\n'

def main():
    W = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip-i1c').resolve(strict=True)
    spec = importlib.util.spec_from_file_location('vd', W / 'tools/verify_design.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    base = head_lock(W)
    parent_lock, lock, synthetic, j3a_mode = scenario(base)
    raw = (W / 'design-lock.json').read_text()
    current = json.loads(raw)
    first_placeholder = next(e['review']['path'] for e in lock['inventorySuccessors'] if e['review']['path'].startswith('SCRATCH-'))
    if current['inventorySuccessors'][-1]['candidate']['path'] == CANDIDATE:
        mode = 'staged'
        assert current == lock, 'the staged lock is not HEAD plus exactly the I1-c (and J3a) entries and inheritance'
        assert raw == canonical(lock), 'the staged lock is not in canonical formatting'
        # Plain verify_design refuses at the first SCRATCH placeholder.
        try:
            m.verify(A, current, W)
        except m.DesignError as exc:
            plain = str(exc)
        else:
            raise AssertionError('plain verify_design accepted SCRATCH placeholders')
        assert first_placeholder in plain, plain
    else:
        mode, plain = 'appended', None
        assert current == base, 'the worktree lock differs from HEAD without selecting inventory140'
    real = m.pinned_bytes
    def pinned_bytes(root, row):
        if isinstance(row, dict) and row.get('path') in synthetic:
            data = synthetic[row['path']]; assert hashlib.sha256(data).hexdigest() == row['sha256'] and len(data) == row['bytes']; return data
        return real(root, row)
    m.pinned_bytes = pinned_bytes
    before = m.verify(A, base, W)
    parent = m.verify(A, parent_lock, W)
    result = m.verify(A, lock, W)
    assert before['passed'] is True and parent['passed'] is True and result['passed'] is True
    assert len(result['inventorySuccessors']) == len(parent['inventorySuccessors']) + 1
    assert len(result['contractSuccessors']) == len(parent['contractSuccessors']) == len(before['contractSuccessors'])
    assert result['selectedInventory']['path'] == CANDIDATE and parent['selectedInventory']['path'] == PARENT
    assert result['inventoryPassageSupersessions'] == parent['inventoryPassageSupersessions'] == before['inventoryPassageSupersessions']
    assert result.get('contractPassageSupersessions') == before.get('contractPassageSupersessions')
    assert result['inventoryPassageInheritance'] == lock['inventoryPassageInheritance'], 'verify_design projects a different inheritance'
    assert len(result['inventoryPassageInheritance']) == len(parent['inventoryPassageInheritance']) == 103
    print(json.dumps({'mode': mode, 'j3a': j3a_mode, 'passed': result['passed'], 'plainVerifyDesignRefusal': plain,
                      'inventorySuccessors': [len(before['inventorySuccessors']), len(parent['inventorySuccessors']), len(result['inventorySuccessors'])],
                      'contractSuccessors': len(result['contractSuccessors']),
                      'inventoryPassageInheritance': [len(before['inventoryPassageInheritance']), len(parent['inventoryPassageInheritance']), len(result['inventoryPassageInheritance'])],
                      'inventoryPassageSupersessions': result['inventoryPassageSupersessions'],
                      'contractPassageSupersessions': result.get('contractPassageSupersessions'),
                      'selectedInventory': result['selectedInventory']['path'],
                      'generationSources': result.get('generationSources'), 'admissionSources': result.get('admissionSources')}, indent=1))

if __name__ == '__main__':
    main()
