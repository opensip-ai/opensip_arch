"""F8c step 9 (scratch only): run a product worktree's real verify_design (VD2-a's bytes) over
a lock that binds F8c's contract successor, with a synthetic review and assent held in memory
(SCRATCH-F8C/ paths). Nothing is written to either repository. It proves only that everything
except the missing independent review and root assent passes.

Two modes, chosen by the worktree's lock (as F8b's verify_scratch_f8b.py and I1-a's
verify_scratch_i1a.py):
- appended: the lock does not bind F8c, so the binding is appended in memory;
- staged: the lock's last contract successor is F8c (the uncommitted opensip-vd2a worktree,
  written by stage_lock_f8c.py). The staged lock must equal HEAD's lock plus exactly that
  entry, in the lock's canonical formatting; its review and assent pins must be the
  SCRATCH-F8C placeholders, which only this overlay serves. Plain verify_design must refuse
  that lock at the review placeholder, and this script checks that it does.

In both modes:
- the worktree's verify_design.py is VD2-a's (not c13d231e, F8b's reference bytes);
- HEAD's lock (without F8c) passes on this tree with the implementation check, with
  contractPassageSupersessions 0 (verify_design.py is not a generation or admission source);
- the lock with F8c passes with the implementation check: one more contract successor, no
  passage overrides or supersessions, contractPassageSupersessions still 0, and the inventory
  chain, selected inventory, inheritance projection, inventory supersession count, generation
  sources and admission sources unchanged;
- the worktree's closure, registry, report.ts, lane registry and verify_design.py bytes are
  each selected exactly once, by F8c (check_typescript.py's rule for the lane registry;
  generate_contracts.py needs the closure selected at least once).
Usage: verify_scratch_f8c.py [WORKTREE]"""
import copy, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
A = Path('/Users/sb/code/opensip-ai/opensip_arch')
D = 'docs/implementation/m3/verify-design-vd2/f8c'
RECORD = D + '/successor.json'
OLD_VD = 'c13d231eb755a08a33fae674426861145758c5ec136ba2cd6dd4b0f1020f8f08'
SELECTED = ('tools/contracts/generator-closure.json', 'schemas/registry.json', 'apps/report/src/generated/report.ts',
            'tools/typescript-lanes.json', 'tools/verify_design.py')

def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def binding():
    """The F8c contractSuccessors entry with SCRATCH-F8C review and assent pins, and the
    synthetic bytes those pins name."""
    subject, record = pin(D + '-subject.json'), pin(RECORD)
    review = json.dumps({'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [], 'subjectManifestSha256': subject['sha256']}).encode()
    rpin = {'path': 'SCRATCH-F8C/review.json', 'bytes': len(review), 'sha256': hashlib.sha256(review).hexdigest()}
    assent = json.dumps({'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [],
                         'subjectManifest': subject, 'independentReview': rpin, 'acceptedSuccessor': record}).encode()
    apin = {'path': 'SCRATCH-F8C/assent.json', 'bytes': len(assent), 'sha256': hashlib.sha256(assent).hexdigest()}
    return {'record': record, 'subjectManifest': subject, 'review': rpin, 'assent': apin}, {rpin['path']: review, apin['path']: assent}

def overlay(m):
    """Serve the two synthetic placeholders to a loaded verify_design module."""
    _, synthetic = binding(); real = m.pinned_bytes
    def pinned_bytes(root, row):
        if isinstance(row, dict) and row.get('path') in synthetic:
            data = synthetic[row['path']]
            assert hashlib.sha256(data).hexdigest() == row['sha256'] and len(data) == row['bytes']
            return data
        return real(root, row)
    m.pinned_bytes = pinned_bytes
    return m

def head_lock(worktree):
    return json.loads(subprocess.run(['git', '-C', str(worktree), 'show', 'HEAD:design-lock.json'], capture_output=True, check=True).stdout)

def staged(base):
    """HEAD's lock plus the F8c contract-successor entry."""
    assert all(b['record']['path'] != RECORD for b in base['contractSuccessors']), 'HEAD already binds F8c'
    lock = copy.deepcopy(base)
    lock['contractSuccessors'].append(binding()[0])
    return lock

def canonical(lock):
    return json.dumps(lock, indent=2, ensure_ascii=True) + '\n'

def main():
    W = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip-vd2a').resolve(strict=True)
    tool = (W / 'tools/verify_design.py').read_bytes()
    assert hashlib.sha256(tool).hexdigest() != OLD_VD, 'the worktree does not carry VD2-a'
    spec = importlib.util.spec_from_file_location('vd', W / 'tools/verify_design.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    base = head_lock(W)
    raw = (W / 'design-lock.json').read_text(); current = json.loads(raw)
    if current['contractSuccessors'][-1]['record']['path'] == RECORD:
        mode = 'staged'; lock = staged(base)
        assert current == lock, 'the staged lock is not HEAD plus exactly the F8c entry'
        assert raw == canonical(lock), 'the staged lock is not in canonical formatting'
        try:
            m.verify(A, current, W)
        except m.DesignError as exc:
            plain = str(exc)
        else:
            raise AssertionError('plain verify_design accepted SCRATCH placeholders')
        assert 'SCRATCH-F8C/review.json' in plain, plain
    else:
        mode, plain = 'appended', None
        assert current == base, 'the worktree lock differs from HEAD without binding F8c'
        lock = staged(base)
    alone = m.verify(A, base, W)
    overlay(m)
    result = m.verify(A, lock, W)
    mine = result['contractSuccessors'][-1]
    assert alone['passed'] is True and result['passed'] is True
    assert len(result['contractSuccessors']) == len(alone['contractSuccessors']) + 1 and mine['selected'] == RECORD
    assert mine['passageOverrides'] == [] and mine['passageSupersessions'] == []
    assert alone['contractPassageSupersessions'] == 0 and result['contractPassageSupersessions'] == 0
    for key in ('inventorySuccessors', 'selectedInventory', 'inventoryPassageInheritance', 'inventoryPassageSupersessions',
                'generationSources', 'admissionSources', 'inputsVerified'):
        assert result[key] == alone[key], key
    inputs = [row for unit in result['contractSuccessors'] for row in unit['inputs']]
    def selected(raw):
        d = hashlib.sha256(raw).hexdigest()
        return (sum(1 for row in inputs if row['sha256'] == d and row['bytes'] == len(raw)),
                sum(1 for row in mine['inputs'] if row['sha256'] == d and row['bytes'] == len(raw)))
    selection = {name: selected((W / name).read_bytes()) for name in SELECTED}
    assert all(value == (1, 1) for value in selection.values()), selection
    print(json.dumps({'mode': mode, 'passed': result['passed'], 'plainVerifyDesignRefusal': plain,
                      'tool': {'bytes': len(tool), 'sha256': hashlib.sha256(tool).hexdigest()},
                      'contractSuccessors': [len(alone['contractSuccessors']), len(result['contractSuccessors'])],
                      'inventorySuccessors': len(result['inventorySuccessors']), 'selectedInventory': result['selectedInventory']['path'],
                      'inventoryPassageInheritance': len(result['inventoryPassageInheritance']),
                      'inventoryPassageSupersessions': result['inventoryPassageSupersessions'],
                      'contractPassageSupersessions': result['contractPassageSupersessions'],
                      'f8c': {'selected': mine['selected'], 'inputs': len(mine['inputs']), 'passageOverrides': 0, 'passageSupersessions': 0},
                      'selectedExactlyOnceByF8c': {name: {'byAll': value[0], 'byF8c': value[1]} for name, value in selection.items()},
                      'generationSources': result.get('generationSources'), 'admissionSources': result.get('admissionSources'),
                      'inputsVerified': result.get('inputsVerified')}, indent=1))

if __name__ == '__main__':
    main()
