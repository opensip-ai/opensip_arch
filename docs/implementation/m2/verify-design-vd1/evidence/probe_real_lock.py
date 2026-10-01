"""Scratch-only VD1 probe over the real design lock. Writes nothing.

It runs the VD1 worktree's verify_design over the real lock plus one or two
synthetic D2-shaped contract successors whose records, subjects, reviews and
assents live in memory (SCRATCH-VD1/ paths). Each supersedes the inherited
read_premise.rs meaning (461b's override on inventory80, projected to the
selected inventory). PROBE text stands in for D2's real descriptions.

Run against product main 96ca141 instead, the four refusal cases other than the
silent override PASS: the pre-VD1 verify_design ignores the unknown record field,
which is why D2 may be bound only after VD1-a (PROPOSAL item 6).

Usage: python3.14 -I -B probe_real_lock.py [WORKTREE]
"""
import hashlib, importlib.util, json, sys
from pathlib import Path

W = Path(sys.argv[1] if len(sys.argv) > 1 else '/Users/sb/code/opensip-ai/opensip-vd1')
A = Path('/Users/sb/code/opensip-ai/opensip_arch')
spec = importlib.util.spec_from_file_location('vd', W / 'tools/verify_design.py')
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
ROW = 'crates/security/src/custody/read_premise.rs'
ORIGIN = 'docs/implementation/m2/stale-descriptions-461b/successor.json'


def pinb(path, raw):
    return {'path': path, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def pin(path):
    return pinb(path, (A / path).read_bytes())


real_lock = json.loads((W / 'design-lock.json').read_text())
final = real_lock['inventorySuccessors'][-1]['candidate']
inventory = json.loads((A / final['path']).read_text())
index = [i for i, row in enumerate(inventory['files']) if row['path'] == ROW][0]
selector = {'jsonPointer': f'/files/{index}/description'}
inherited = [r for r in real_lock['inventoryPassageInheritance'] if r['selector'] == selector][0]
origin_pin = [b['record'] for b in real_lock['contractSuccessors'] if b['record']['path'] == ORIGIN][0]
origin = json.loads((A / ORIGIN).read_text())
root = [o for o in origin['passageOverrides']
        if json.loads((A / o['parent']['path']).read_text())['files'][int(o['selector']['jsonPointer'].split('/')[2])]['path'] == ROW][0]
synthetic = {}


def unit(n, overrides=(), supersessions=()):
    member = pinb(f'SCRATCH-VD1/{n}/README.md', b'probe\n')
    synthetic[member['path']] = b'probe\n'
    rec = json.dumps({'schemaVersion': 1, 'standing': 'PROBE', 'parents': [final], 'candidates': [member],
                      'passageOverrides': list(overrides), 'passageSupersessions': list(supersessions)}).encode()
    rpin = pinb(f'SCRATCH-VD1/{n}/successor.json', rec)
    subj = json.dumps({'files': sorted([member, rpin], key=lambda r: r['path'])}).encode()
    spin = pinb(f'SCRATCH-VD1/{n}-subject.json', subj)
    review = json.dumps({'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [], 'subjectManifestSha256': spin['sha256']}).encode()
    vpin = pinb(f'SCRATCH-VD1/{n}/review.json', review)
    assent = json.dumps({'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [],
                         'subjectManifest': spin, 'independentReview': vpin, 'acceptedSuccessor': rpin}).encode()
    apin = pinb(f'SCRATCH-VD1/{n}/assent.json', assent)
    synthetic.update({rpin['path']: rec, spin['path']: subj, vpin['path']: review, apin['path']: assent})
    return {'record': rpin, 'subjectManifest': spin, 'review': vpin, 'assent': apin}


def supersede(before, after, record, parent, sel):
    return {'parent': final, 'selector': selector, 'before': before, 'after': after,
            'supersedes': {'record': record, 'parent': parent, 'selector': sel}}


real = m.pinned_bytes


def pinned_bytes(root_dir, row):
    if isinstance(row, dict) and row.get('path') in synthetic:
        raw = synthetic[row['path']]
        if hashlib.sha256(raw).hexdigest() != row['sha256']:
            raise m.DesignError('synthetic digest mismatch')
        return raw
    return real(root_dir, row)


m.pinned_bytes = pinned_bytes
FIRST, SECOND = 'PROBE read_premise r1', 'PROBE read_premise r2'


def run(name, *bindings, expect):
    lock = json.loads((W / 'design-lock.json').read_text())
    lock['contractSuccessors'] += list(bindings)
    try:
        result = m.verify(A, lock, W)
        outcome = ('PASSED', result.get('inventoryPassageSupersessions'), len(result['inventoryPassageInheritance']),
                   result['inventoryPassageInheritance'] == real_lock['inventoryPassageInheritance'])
    except m.DesignError as exc:
        outcome = ('REFUSED', str(exc))
    ok = outcome[0] == expect
    print(json.dumps({'case': name, 'expect': expect, 'outcome': outcome, 'ok': ok}))
    return ok


assert inherited['before'] == inventory['files'][index]['description'] == root['before']
assert inherited['after'] == root['after']
results = []
synthetic.clear()
d2 = unit('d2', supersessions=[supersede(inherited['after'], FIRST, origin_pin, root['parent'], root['selector'])])
results.append(run('D2-shaped supersession of the inherited row', d2, expect='PASSED'))
d2b = unit('d2b', supersessions=[supersede(FIRST, SECOND, d2['record'], final, selector)])
results.append(run('second link extends the tail', d2, d2b, expect='PASSED'))
stale = unit('stale', supersessions=[supersede(inherited['before'], FIRST, origin_pin, root['parent'], root['selector'])])
results.append(run('stale before (raw bytes)', stale, expect='REFUSED'))
again = unit('again', supersessions=[supersede(inherited['after'], SECOND, origin_pin, root['parent'], root['selector'])])
results.append(run('double supersession of 461b', d2, again, expect='REFUSED'))
rebind = unit('rebind', supersessions=[supersede(inherited['after'], SECOND, d2['record'], final, selector)])
results.append(run('stale rebind to the superseded text', d2, rebind, expect='REFUSED'))
missing = unit('missing', supersessions=[supersede(inherited['after'], FIRST, pin('docs/implementation/m2/description-batch-d1/successor.json'), root['parent'], root['selector'])])
results.append(run('missing chain (target not in named record)', missing, expect='REFUSED'))
silent = unit('silent', overrides=[{'parent': final, 'selector': selector, 'before': inherited['before'], 'after': FIRST}])
results.append(run('silent direct override (pre-VD1 route)', silent, expect='REFUSED'))
results.append(run('real lock unchanged', expect='PASSED'))
sys.exit(0 if all(results) else 1)
