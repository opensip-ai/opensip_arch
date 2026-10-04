"""Scratch-only: run a product worktree's real verify_design over a lock that
binds I1-a's contract successor, with a synthetic review and assent held in
memory (SCRATCH-I1A/ paths). Nothing is written to either repository. It proves
only that everything except the missing independent review and root assent
passes.

Two modes, chosen by the worktree's lock (as P0's verify_scratch.py and F8b's
verify_scratch_f8b.py):
- appended: the lock does not bind I1-a, so the binding is appended in memory;
- staged: the lock's last contract successor is I1-a (the uncommitted
  opensip-i1a worktree, written by stage_lock_i1a.py). The staged lock must
  equal HEAD's lock plus exactly that entry, in the lock's canonical
  formatting; its review and assent pins must be the SCRATCH-I1A placeholders,
  which only this overlay serves. Plain verify_design must refuse that lock at
  the review placeholder, and this script checks that it does.

In both modes:
- HEAD's lock (without I1-a) passes on its own, and refuses this worktree's
  product sources at the admission registry, because the admission source map
  now names I1-a's architecture copy;
- the lock with I1-a passes with the implementation check: one more contract
  successor, no passage overrides or supersessions, and the inventory chain,
  selected inventory, inheritance projection and supersession count unchanged;
- the worktree's two schema sources equal I1-L's accepted copies, and both
  source maps pin those copies;
- the worktree's generator closure and admission registry bytes are selected
  only by I1-a: the closure by its one product/ copy, the admission registry
  by its architecture copy and its product/ copy.
Usage: verify_scratch_i1a.py [WORKTREE]"""
import copy, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path
A = Path('/Users/sb/code/opensip-ai/opensip_arch')
M = 'docs/implementation/m3/preview-pack-i1'
D = M + '/i1-a'; L = M + '/i1-l'
RECORD = D + '/successor.json'

def pin(p):
    b = (A / p).read_bytes(); return {'path': p, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def binding():
    """The I1-a contractSuccessors entry with SCRATCH-I1A review and assent pins,
    and the synthetic bytes those pins name."""
    subject, record = pin(D + '-subject.json'), pin(RECORD)
    review = json.dumps({'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [], 'subjectManifestSha256': subject['sha256']}).encode()
    rpin = {'path': 'SCRATCH-I1A/review.json', 'bytes': len(review), 'sha256': hashlib.sha256(review).hexdigest()}
    assent = json.dumps({'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [],
                         'subjectManifest': subject, 'independentReview': rpin, 'acceptedSuccessor': record}).encode()
    apin = {'path': 'SCRATCH-I1A/assent.json', 'bytes': len(assent), 'sha256': hashlib.sha256(assent).hexdigest()}
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
    """HEAD's lock plus the I1-a contract-successor entry."""
    assert all(b['record']['path'] != RECORD for b in base['contractSuccessors']), 'HEAD already binds I1-a'
    lock = copy.deepcopy(base)
    lock['contractSuccessors'].append(binding()[0])
    return lock

def canonical(lock):
    return json.dumps(lock, indent=2, ensure_ascii=True) + '\n'

def main():
    W = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip-i1a').resolve(strict=True)
    spec = importlib.util.spec_from_file_location('vd', W / 'tools/verify_design.py'); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    base = head_lock(W)
    raw = (W / 'design-lock.json').read_text(); current = json.loads(raw)
    if current['contractSuccessors'][-1]['record']['path'] == RECORD:
        mode = 'staged'; lock = staged(base)
        assert current == lock, 'the staged lock is not HEAD plus exactly the I1-a entry'
        assert raw == canonical(lock), 'the staged lock is not in canonical formatting'
        try:
            m.verify(A, current, W)
        except m.DesignError as exc:
            plain = str(exc)
        else:
            raise AssertionError('plain verify_design accepted SCRATCH placeholders')
        assert 'SCRATCH-I1A/review.json' in plain, plain
    else:
        mode, plain = 'appended', None
        assert current == base, 'the worktree lock differs from HEAD without binding I1-a'
        lock = staged(base)
    # HEAD's lock alone: passes without the implementation, refuses this tree with it.
    alone = m.verify(A, base, None)
    try:
        m.verify(A, base, W)
    except m.DesignError as exc:
        without = str(exc)
    else:
        raise AssertionError('HEAD lock accepted the I1-a product sources without I1-a')
    assert without == 'admission source is not selected by accepted design', without
    overlay(m)
    result = m.verify(A, lock, W)
    mine = result['contractSuccessors'][-1]
    assert alone['passed'] is True and result['passed'] is True
    assert len(result['contractSuccessors']) == len(alone['contractSuccessors']) + 1 and mine['selected'] == RECORD
    assert mine['passageOverrides'] == [] and mine['passageSupersessions'] == []
    assert result['inventorySuccessors'] == alone['inventorySuccessors'] and result['selectedInventory'] == alone['selectedInventory']
    assert result['inventoryPassageInheritance'] == alone['inventoryPassageInheritance']
    assert result['inventoryPassageSupersessions'] == alone['inventoryPassageSupersessions']
    # The schema sources are I1-L's copies and both source maps pin them.
    copies = {'schemas/sources/identity-v3.schema.json': pin(L + '/product/schemas/sources/identity-v3.schema.json'),
              'schemas/sources/policy-v2.schema.json': pin(L + '/product/schemas/sources/policy-v2.schema.json')}
    for product, copy_pin in copies.items():
        assert (W / product).read_bytes() == (A / copy_pin['path']).read_bytes(), product
    for name in ('schemas/source-map.json', 'schemas/admission-source-map.json'):
        rows = {r['implementationPath']: r['architectureSource'] for r in json.loads((W / name).read_bytes())['sources']}
        for product, copy_pin in copies.items():
            assert rows[product] == {'path': copy_pin['path'], 'sha256': copy_pin['sha256'], 'bytes': copy_pin['bytes']}, (name, product)
    inputs = [row for unit in result['contractSuccessors'] for row in unit['inputs']]
    def selected(raw):
        d = hashlib.sha256(raw).hexdigest()
        return (sum(1 for row in inputs if row['sha256'] == d and row['bytes'] == len(raw)),
                sum(1 for row in mine['inputs'] if row['sha256'] == d and row['bytes'] == len(raw)))
    closure = selected((W / 'tools/contracts/generator-closure.json').read_bytes())
    registry_raw = (W / 'schemas/admission-registry.json').read_bytes()
    admission = selected(registry_raw)
    # The closure has one copy (product/); the admission registry has the architecture
    # copy the map names and its product/ copy, both I1-a inputs.
    assert closure == (1, 1) and admission == (2, 2), (closure, admission)
    assert json.loads((W / 'schemas/admission-source-map.json').read_bytes())['registryArchitectureSource']['path'] == D + '/schemas/admission-registry.json'
    print(json.dumps({'mode': mode, 'passed': result['passed'], 'plainVerifyDesignRefusal': plain,
                      'headLockOnThisTree': without,
                      'contractSuccessors': [len(alone['contractSuccessors']), len(result['contractSuccessors'])],
                      'inventorySuccessors': len(result['inventorySuccessors']), 'selectedInventory': result['selectedInventory']['path'],
                      'inventoryPassageInheritance': len(result['inventoryPassageInheritance']),
                      'inventoryPassageSupersessions': result['inventoryPassageSupersessions'],
                      'i1a': {'selected': mine['selected'], 'inputs': len(mine['inputs']), 'passageOverrides': 0, 'passageSupersessions': 0},
                      'generatorClosureSelected': {'byAll': closure[0], 'byI1a': closure[1]},
                      'admissionRegistrySelected': {'byAll': admission[0], 'byI1a': admission[1]},
                      'generationSources': result.get('generationSources'), 'admissionSources': result.get('admissionSources'),
                      'inputsVerified': result.get('inputsVerified')}, indent=1))

if __name__ == '__main__':
    main()
