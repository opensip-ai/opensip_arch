"""Scratch-only: run a product worktree's real verify_design over a lock that
selects inventory136 and binds unit X3a-2's description successor, with
synthetic reviews and assents held in memory (SCRATCH-X3A2/ paths). Nothing
is written to either repository. It proves only that everything except the
missing independent reviews and root assents passes.

The parent is inventory135 (unit M3-P0), selected at product 3f6f9a5 with its
one hundred inheritance rows. The re-projected inheritance has the same one
hundred rows on inventory136; the forty-six sorted after the two inserted
paths move by two. The description successor
(read-endpoint-x3a2-descriptions) has inventory136 as its only parent, so
its three overrides are on the final inventory and are checked, not
projected.

Two modes, chosen by the worktree's lock (as P0's verify_scratch.py):
- appended: the lock does not select inventory136, so both bindings and the
  re-projected inheritance are applied in memory;
- staged: the lock's last inventory successor is inventory136 (the
  uncommitted opensip-x3a2 worktree, written by evidence/stage_lock_x3a2.py).
  The staged lock must equal HEAD's lock plus exactly the inventory136 entry,
  that inheritance and the description binding as the last contract
  successor, in the lock's canonical formatting; its review and assent pins
  must be the SCRATCH-X3A2 placeholders, which only this overlay serves.
  Plain verify_design must refuse that lock at the first placeholder, the
  inventory review, and this script checks that it does.

In both modes the lock without X3a-2, the lock with inventory136 alone and
the lock with both must pass. inventory136 must be selected with exactly one
more inventory successor and the descriptions with exactly one more contract
successor; the supersession count must be unchanged; verify_design's own
projected inheritance must equal the record's; and each description override
must be on inventory136 with its raw text as before, on a row with no
inherited meaning.
Usage: verify_scratch.py [WORKTREE]."""
import copy, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
A = Path('/Users/sb/code/opensip-ai/opensip_arch')
M = 'docs/implementation/m2/'
U = M + 'read-endpoint-x3a2-inventory-v136'
DESC = M + 'read-endpoint-x3a2-descriptions'
CANDIDATE = M + 'repository-file-inventory.v136.json'

def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def synthetic_pin(path, data):
    return {'path': path, 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def bindings_for(parent):
    """The inventory136 lock entry and the description binding, each with
    SCRATCH-X3A2 review and assent pins; the synthetic bytes those pins name;
    and the re-projected inheritance."""
    candidate, record, subject = pin(CANDIDATE), pin(U + '/successor.json'), pin(U + '-subject.json')
    assert json.loads((A / record['path']).read_bytes())['parent'] == parent, 'inventory136 must be built on the selected inventory'
    review = json.dumps({'verdict': 'ACCEPT-UNIT', 'requiredFindings': [], 'subjectManifestSha256': subject['sha256'],
        'inventoryCandidateAssessment': {'verdict': 'ACCEPT', 'requiredFindings': [], **candidate, 'parent': parent, 'successorRecord': record}}).encode()
    rpin = synthetic_pin('SCRATCH-X3A2/review.json', review)
    assent = json.dumps({'status': 'ACCEPTED-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [], 'subjectManifest': subject,
        'independentReview': rpin, 'acceptedInventory': candidate}).encode()
    apin = synthetic_pin('SCRATCH-X3A2/assent.json', assent)
    inventory = {'parent': parent, 'candidate': candidate, 'record': record, 'review': rpin, 'assent': apin}
    dsubject, drecord = pin(DESC + '-subject.json'), pin(DESC + '/successor.json')
    dreview = json.dumps({'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [], 'subjectManifestSha256': dsubject['sha256']}).encode()
    drpin = synthetic_pin('SCRATCH-X3A2/descriptions-review.json', dreview)
    dassent = json.dumps({'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [], 'subjectManifest': dsubject,
        'independentReview': drpin, 'acceptedSuccessor': drecord}).encode()
    dapin = synthetic_pin('SCRATCH-X3A2/descriptions-assent.json', dassent)
    descriptions = {'record': drecord, 'subjectManifest': dsubject, 'review': drpin, 'assent': dapin}
    rows = json.loads((A / record['path']).read_text())['descriptionOverrideProjection']
    inheritance = sorted(
        ({'parent': candidate, 'selector': r['candidateSelector'], 'before': r['before'], 'after': r['effectiveDescription']} for r in rows),
        key=lambda o: json.dumps(o['selector'], sort_keys=True))
    synthetic = {rpin['path']: review, apin['path']: assent, drpin['path']: dreview, dapin['path']: dassent}
    return inventory, descriptions, inheritance, synthetic

def head_lock(worktree):
    return json.loads(subprocess.run(['git', '-C', str(worktree), 'show', 'HEAD:design-lock.json'],
                                     capture_output=True, check=True).stdout)

def staged(base, with_descriptions=True):
    """HEAD's lock plus the inventory136 entry, the re-projected inheritance
    and, last among the contract successors, the description binding."""
    assert all(s['candidate']['path'] != CANDIDATE for s in base['inventorySuccessors']), 'HEAD already selects inventory136'
    inventory, descriptions, inheritance, _ = bindings_for(base['inventorySuccessors'][-1]['candidate'])
    lock = copy.deepcopy(base)
    lock['inventorySuccessors'].append(inventory)
    lock['inventoryPassageInheritance'] = inheritance
    if with_descriptions:
        lock['contractSuccessors'].append(descriptions)
    return lock

def canonical(lock):
    return json.dumps(lock, indent=2, ensure_ascii=True) + '\n'

def main():
    W = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip-x3a2').resolve(strict=True)
    spec = importlib.util.spec_from_file_location('vd', W / 'tools/verify_design.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    base = head_lock(W)
    raw = (W / 'design-lock.json').read_text()
    current = json.loads(raw)
    if current['inventorySuccessors'][-1]['candidate']['path'] == CANDIDATE:
        mode = 'staged'
        lock = staged(base)
        assert current == lock, 'the staged lock is not HEAD plus exactly the X3a-2 entries and inheritance'
        assert raw == canonical(lock), 'the staged lock is not in canonical formatting'
        # Plain verify_design refuses at the first SCRATCH placeholder.
        try:
            m.verify(A, current, W)
        except m.DesignError as exc:
            plain = str(exc)
        else:
            raise AssertionError('plain verify_design accepted SCRATCH placeholders')
        assert 'SCRATCH-X3A2/review.json' in plain, plain
    else:
        mode, plain = 'appended', None
        assert current == base, 'the worktree lock differs from HEAD without selecting inventory136'
        lock = staged(base)
    inventory_only = staged(base, with_descriptions=False)
    _, _, inheritance, synthetic = bindings_for(base['inventorySuccessors'][-1]['candidate'])
    real = m.pinned_bytes
    def pinned_bytes(root, row):
        if isinstance(row, dict) and row.get('path') in synthetic:
            data = synthetic[row['path']]; assert hashlib.sha256(data).hexdigest() == row['sha256'] and len(data) == row['bytes']; return data
        return real(root, row)
    m.pinned_bytes = pinned_bytes
    before = m.verify(A, base, W)
    alone = m.verify(A, inventory_only, W)
    result = m.verify(A, lock, W)
    assert before['passed'] is True and alone['passed'] is True and result['passed'] is True
    assert len(result['inventorySuccessors']) == len(alone['inventorySuccessors']) == len(before['inventorySuccessors']) + 1
    assert len(result['contractSuccessors']) == len(alone['contractSuccessors']) + 1 == len(before['contractSuccessors']) + 1
    assert result['selectedInventory']['path'] == CANDIDATE and before['selectedInventory'] == base['inventorySuccessors'][-1]['candidate']
    assert result['inventoryPassageSupersessions'] == alone['inventoryPassageSupersessions'] == before['inventoryPassageSupersessions']
    assert result['inventoryPassageInheritance'] == alone['inventoryPassageInheritance'] == inheritance == lock['inventoryPassageInheritance'], 'verify_design projects a different inheritance'
    mine = result['contractSuccessors'][-1]
    assert mine['selected'] == DESC + '/successor.json' and not mine['passageSupersessions']
    v136 = json.loads((A / CANDIDATE).read_bytes())
    inherited = {o['selector']['jsonPointer'] for o in inheritance}
    for o in mine['passageOverrides']:
        pointer = o['selector']['jsonPointer']
        assert o['parent'] == result['selectedInventory'] and pointer not in inherited
        assert o['before'] == v136['files'][int(pointer.split('/')[2])]['description']
    print(json.dumps({'mode': mode, 'passed': result['passed'], 'plainVerifyDesignRefusal': plain,
                      'inventorySuccessors': [len(before['inventorySuccessors']), len(result['inventorySuccessors'])],
                      'contractSuccessors': [len(before['contractSuccessors']), len(result['contractSuccessors'])],
                      'inventoryPassageInheritance': [len(before['inventoryPassageInheritance']), len(result['inventoryPassageInheritance'])],
                      'inventoryPassageSupersessions': result['inventoryPassageSupersessions'],
                      'descriptionOverrides': {o['selector']['jsonPointer']: v136['files'][int(o['selector']['jsonPointer'].split('/')[2])]['path'] for o in mine['passageOverrides']},
                      'selectedInventory': result['selectedInventory']['path'],
                      'generationSources': result.get('generationSources'), 'admissionSources': result.get('admissionSources')}, indent=1))

if __name__ == '__main__':
    main()
