"""VD2 fixture controls: contract passage supersession on the product's own test fixture. Writes nothing to either repository.

It loads the design-binding test module from product commit 6190e66 (read-only `git show`) for its fixture
builder (Fx, ov, sup, proj), and the VD2 prototype tool from ../reference/verify_design.prototype.py. Every case builds
a fresh fixture in a private temporary directory and runs the tool's verify on it. It mirrors VD1's
PassageSupersessionTests, for a contract passage instead of an inventory row description.

Fixture: inventory inv0 (b.py, d.py) and inv1 (adds c.py); c1 introduces the members doc.md (three text lines) and
doc.json ({"text": "T0", "other": "O0"}); c2 is the root, an ordinary override of doc.md line 2, L2 to L2a.

With --base-tool, the REV tool itself (read with `git show`) runs the same cases. It has no contract passage
supersession, so every case that carries one must refuse ("must select an inventory row description"): the binding
order fails closed. N11e, which carries no supersession, passes there, because that tool ignores the review field.

Usage: python3.14 -I -B fixture_controls.py [--tool PATH | --base-tool] [--product CHECKOUT] [--rev REV] [--json OUT]
Exit 0 only if every case gives its expected outcome for the tool run.
"""
import argparse, copy, hashlib, importlib.util, json, subprocess, sys, tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument('--tool', type=Path, default=HERE.parent / 'reference/verify_design.prototype.py')
ap.add_argument('--product', type=Path, default=Path('/Users/sb/code/opensip-ai/opensip'))
ap.add_argument('--rev', default='6190e66')
ap.add_argument('--json', type=Path)
ap.add_argument('--base-tool', action='store_true')
args = ap.parse_args()

if args.base_tool:
    tool_raw = subprocess.run(['git', '-C', str(args.product), 'show', f'{args.rev}:tools/verify_design.py'],
                              check=True, capture_output=True).stdout
    tool_origin = f'{args.rev}:tools/verify_design.py'
    TOOL = importlib.util.module_from_spec(importlib.util.spec_from_loader('base_tool', loader=None))
    exec(compile(tool_raw, tool_origin, 'exec'), TOOL.__dict__)
else:
    tool_raw, tool_origin = args.tool.read_bytes(), str(args.tool)
    spec = importlib.util.spec_from_file_location('vd2_tool', args.tool)
    TOOL = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(TOOL)
source = subprocess.run(['git', '-C', str(args.product), 'show', f'{args.rev}:tools/tests/test_design_binding.py'],
                        check=True, capture_output=True).stdout
fixture = {'__name__': 'design_binding_fixture',
           '__file__': str(args.product / 'tools/tests/test_design_binding.py')}
exec(compile(source, f'test_design_binding.py@{args.rev}', 'exec'), fixture)
Fx, ov, sup, proj, by_path = fixture['Fx'], fixture['ov'], fixture['sup'], fixture['proj'], fixture['by_path']


def text(fx, path, lines):
    raw = ('\n'.join(lines) + '\n').encode()
    (fx.root / path).write_bytes(raw)
    return {'path': path, 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}


def line(parent, n, before, after):
    return {'parent': parent, 'selector': {'line': n}, 'before': before, 'after': after}


def ptr(parent, pointer, before, after):
    return {'parent': parent, 'selector': {'jsonPointer': pointer}, 'before': before, 'after': after}


def csup(entry_parent, selector, before, after, record, target_parent=None, target_selector=None):
    """A contract passage supersession of the entry at (record, target_parent, target_selector)."""
    return {'parent': entry_parent, 'selector': selector, 'before': before, 'after': after,
            'supersedes': {'record': record, 'parent': target_parent or entry_parent,
                           'selector': target_selector or selector}}


L2 = {'line': 2}
AUTO = object()


def contract(fx, parents, overrides=(), members=None, supersessions=None, listed=AUTO):
    """Fx.contract, with the review's supersededPassages: AUTO lists the record's, None omits it."""
    n = len(fx.lock['contractSuccessors']) + 1
    if members is None:
        members = [fx.write(f'c{n}/member.json', {'unit': n})]
    record = {'schemaVersion': 1, 'parents': by_path(copy.deepcopy(parents)),
              'candidates': by_path(copy.deepcopy(members)), 'passageOverrides': copy.deepcopy(list(overrides))}
    if supersessions is not None:
        record['passageSupersessions'] = copy.deepcopy(supersessions)
    rec = fx.write(f'c{n}/record.json', record)
    man = fx.write(f'c{n}/manifest.json', {'files': by_path([rec, *members])})
    review = {'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [], 'subjectManifestSha256': man['sha256']}
    if listed is AUTO:
        if supersessions:
            review['supersededPassages'] = [entry['supersedes'] for entry in supersessions]
    elif listed is not None:
        review['supersededPassages'] = listed
    rev = fx.write(f'c{n}/review.json', review)
    ass = fx.write(f'c{n}/assent.json', {'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True,
                                         'requiredUnitFindings': [], 'independentReview': rev,
                                         'subjectManifest': man, 'acceptedSuccessor': rec})
    fx.lock['contractSuccessors'].append(dict(record=rec, subjectManifest=man, review=rev, assent=ass))
    return rec


class World:
    def __init__(self, root):
        fx = self.fx = Fx(root)
        self.base = fx.base({'b.py': 'B0', 'd.py': 'D0'})
        self.final = fx.hop({'c.py': 'C0'})
        self.doc = text(fx, 'doc.md', ['L1', 'L2', 'L3'])
        self.js = fx.write('doc.json', {'text': 'T0', 'other': 'O0'})
        fx.contract([self.base], members=[self.doc, self.js])
        self.root = contract(fx, [self.doc], [line(self.doc, 2, 'L2', 'L2a')])


results = []


def case(name, expect, build):
    with tempfile.TemporaryDirectory() as tmp:
        w = World(tmp)
        try:
            build(w)
            out = TOOL.verify(w.fx.root, w.fx.lock)
            # .get: the REV tool has no contractPassageSupersessions field (--base-tool).
            outcome = ['PASSED', out.get('contractPassageSupersessions'), out['inventoryPassageSupersessions'],
                       len(out['inventoryPassageInheritance'])]
        except TOOL.DesignError as exc:
            outcome = ['REFUSED', str(exc)]
    if args.base_tool:
        # Cases refused before the chain (N10, N14, N15) or by unchanged rules (N12b, N13) keep their VD2 message.
        # N11e carries no supersession and passes. Every other case carries a contract passage supersession,
        # which the REV tool refuses as a whole.
        if name.startswith('N11e'):
            expect = ('PASSED',)
        elif not name.startswith(('N10', 'N12b', 'N13', 'N14', 'N15')):
            expect = ('REFUSED', 'must select an inventory row description')
    if expect[0] == 'PASSED':
        ok = outcome[:len(expect)] == list(expect)
    else:
        ok = outcome[0] == 'REFUSED' and expect[1] in outcome[1]
    results.append({'case': name, 'expect': list(expect), 'outcome': outcome, 'ok': ok})


# ---- Positive controls.
case('P1 line supersession of a contract override', ('PASSED', 1, 0, 0), lambda w: contract(
    w.fx, [w.doc], supersessions=[csup(w.doc, L2, 'L2a', 'L2b', w.root)]))
def p2(w):
    root = contract(w.fx, [w.js], [ptr(w.js, '/text', 'T0', 'T1')])
    contract(w.fx, [w.js], supersessions=[csup(w.js, {'jsonPointer': '/text'}, 'T1', 'T2', root)])
case('P2 JSON Pointer supersession of a contract override', ('PASSED', 1), p2)
def p3(w):
    first = contract(w.fx, [w.doc], supersessions=[csup(w.doc, L2, 'L2a', 'L2b', w.root)])
    contract(w.fx, [w.doc], supersessions=[csup(w.doc, L2, 'L2b', 'L2c', first)])
case('P3 chain of two extends the tail', ('PASSED', 2), p3)
def p4(w):
    copy_ = contract(w.fx, [w.doc], [line(w.doc, 2, 'L2', 'L2a')])
    contract(w.fx, [w.doc], supersessions=[csup(w.doc, L2, 'L2a', 'L2b', copy_)])
case('P4 first link may name an identical root copy', ('PASSED', 1), p4)
def p5(w):
    inv_root = contract(w.fx, [w.final], [ov(w.final, 2, 'D0', 'D1')])
    contract(w.fx, [w.doc, w.final], supersessions=[sup(w.final, 2, 'D1', 'D2', inv_root, w.final, 2),
                                                     csup(w.doc, L2, 'L2a', 'L2b', w.root)])
case('P5 mixed record: inventory (VD1) and contract (VD2) links, review lists both', ('PASSED', 1, 1, 0), p5)
case('P6 a link may restore the raw parent text', ('PASSED', 1), lambda w: contract(
    w.fx, [w.doc], supersessions=[csup(w.doc, L2, 'L2a', 'L2', w.root)]))
def p7(w):
    root = contract(w.fx, [w.doc], [line(w.doc, 3, 'L3', 'L3\nL3-inserted')])
    contract(w.fx, [w.doc], supersessions=[csup(w.doc, {'line': 3}, 'L3\nL3-inserted', 'L3\nL3-conformed', root)])
case('P7 a multi-line meaning is superseded whole', ('PASSED', 1), p7)
def p8(w):
    other = contract(w.fx, [w.doc], [line(w.doc, 1, 'L1', 'L1a')])
    contract(w.fx, [w.doc], supersessions=[csup(w.doc, L2, 'L2a', 'L2b', w.root),
                                           csup(w.doc, {'line': 1}, 'L1a', 'L1b', other)])
case('P8 two passages superseded in one record', ('PASSED', 2), p8)

# ---- Negative controls.
case('N1 stale before (raw parent text)', ('REFUSED', 'before text differs from the superseded meaning'),
     lambda w: contract(w.fx, [w.doc], supersessions=[csup(w.doc, L2, 'L2', 'L2b', w.root)]))
def n2(w):
    first = contract(w.fx, [w.doc], supersessions=[csup(w.doc, L2, 'L2a', 'L2b', w.root)])
    contract(w.fx, [w.doc], supersessions=[csup(w.doc, L2, 'L2a', 'L2c', first)])
case('N2 stale rebind to the superseded text', ('REFUSED', 'before text differs from the superseded meaning'), n2)
def n3(w):
    contract(w.fx, [w.doc], supersessions=[csup(w.doc, L2, 'L2a', 'L2b', w.root)])
    contract(w.fx, [w.doc], supersessions=[csup(w.doc, L2, 'L2a', 'L2c', w.root)])
case('N3 double supersession of the root', ('REFUSED', 'double supersession'), n3)
def n4(w):
    copy_ = contract(w.fx, [w.doc], [line(w.doc, 2, 'L2', 'L2a')])
    contract(w.fx, [w.doc], supersessions=[csup(w.doc, L2, 'L2a', 'L2b', w.root)])
    contract(w.fx, [w.doc], supersessions=[csup(w.doc, L2, 'L2a', 'L2c', copy_)])
case('N4 double supersession through an identical root copy', ('REFUSED', 'double supersession'), n4)
def n5(w):
    first = contract(w.fx, [w.doc], supersessions=[csup(w.doc, L2, 'L2a', 'L2b', w.root)])
    contract(w.fx, [w.doc], supersessions=[csup(w.doc, L2, 'L2b', 'L2c', first)])
    contract(w.fx, [w.doc], supersessions=[csup(w.doc, L2, 'L2b', 'L2d', first)])
case('N5 fork from a link that is no longer the tail', ('REFUSED', 'double supersession'), n5)
def n6a(w):
    unbound = w.fx.write('elsewhere/record.json', {'passageOverrides': [line(w.doc, 2, 'L2', 'L2a')]})
    contract(w.fx, [w.doc], supersessions=[csup(w.doc, L2, 'L2a', 'L2b', unbound)])
case('N6a unbound target record', ('REFUSED', 'superseded record is not an earlier contract successor'), n6a)
case('N6b wrong record pin (sha)', ('REFUSED', 'superseded record is not an earlier contract successor'),
     lambda w: contract(w.fx, [w.doc], supersessions=[csup(w.doc, L2, 'L2a', 'L2b', {**w.root, 'sha256': '0' * 64})]))
case('N6c named entry not in the record (selector)', ('REFUSED', 'superseded passage is not in the named record'),
     lambda w: contract(w.fx, [w.doc], supersessions=[csup(w.doc, L2, 'L2a', 'L2b', w.root, w.doc, {'line': 1})]))
case('N6d named entry parent pin wrong', ('REFUSED', 'superseded passage is not in the named record'),
     lambda w: contract(w.fx, [w.doc], supersessions=[csup(w.doc, L2, 'L2a', 'L2b', w.root, {**w.doc, 'bytes': 1})]))
def n7(w):
    contract(w.fx, [w.doc], supersessions=[csup(w.doc, L2, 'L2a', 'L2b', w.root)])
    cs = w.fx.lock['contractSuccessors']
    cs[1], cs[2] = cs[2], cs[1]
case('N7 named record not strictly earlier', ('REFUSED', 'superseded record is not an earlier contract successor'), n7)
def n8a(w):
    other = contract(w.fx, [w.doc], [line(w.doc, 1, 'L1', 'L2a')])
    contract(w.fx, [w.doc], supersessions=[csup(w.doc, L2, 'L2a', 'L2b', other, w.doc, {'line': 1})])
case('N8a link selects another passage of the same parent', ('REFUSED', 'selects a different passage'), n8a)
def n8b(w):
    twin = text(w.fx, 'twin.md', ['L1', 'L2', 'L3'])
    w.fx.contract([w.base], members=[twin])
    contract(w.fx, [twin], supersessions=[csup(twin, L2, 'L2a', 'L2b', w.root, w.doc, L2)])
case('N8b link on another parent naming an identical passage', ('REFUSED', 'selects a different passage'), n8b)
def n8c(w):
    inv_root = contract(w.fx, [w.final], [ov(w.final, 2, 'D0', 'D1')])
    contract(w.fx, [w.doc], supersessions=[csup(w.doc, L2, 'D1', 'L2b', inv_root, w.final,
                                                {'jsonPointer': '/files/2/description'})])
case('N8c contract link naming an inventory meaning', ('REFUSED', 'selects a different passage'), n8c)
def n9a(w):
    contract(w.fx, [w.doc], supersessions=[csup(w.doc, L2, 'L2a', 'L2b', w.root)])
    contract(w.fx, [w.doc], [line(w.doc, 2, 'L2', 'L2a')])
case('N9a restatement of the superseded root', ('REFUSED', 'restates a superseded contract meaning'), n9a)
def n9b(w):
    contract(w.fx, [w.doc], supersessions=[csup(w.doc, L2, 'L2a', 'L2b', w.root)])
    contract(w.fx, [w.doc], [line(w.doc, 2, 'L2', 'L2b')])
case('N9b override restating the current tail text', ('REFUSED', 'conflicting contract passage overrides'), n9b)
case('N10 override and supersession of one passage in one record', ('REFUSED', 'duplicate passage override'),
     lambda w: contract(w.fx, [w.doc], [line(w.doc, 2, 'L2', 'L2a')],
                        supersessions=[csup(w.doc, L2, 'L2a', 'L2b', w.root)]))
case('N11a review does not list the supersession', ('REFUSED', 'not listed by its review'),
     lambda w: contract(w.fx, [w.doc], supersessions=[csup(w.doc, L2, 'L2a', 'L2b', w.root)], listed=None))
case('N11b review lists a different passage', ('REFUSED', 'superseded passages differ from the record'),
     lambda w: contract(w.fx, [w.doc], supersessions=[csup(w.doc, L2, 'L2a', 'L2b', w.root)],
                        listed=[{'record': w.root, 'parent': w.doc, 'selector': {'line': 1}}]))
def n11c(w):
    other = contract(w.fx, [w.doc], [line(w.doc, 1, 'L1', 'L1a')])
    entries = [csup(w.doc, L2, 'L2a', 'L2b', w.root), csup(w.doc, {'line': 1}, 'L1a', 'L1b', other)]
    contract(w.fx, [w.doc], supersessions=entries, listed=[entries[1]['supersedes'], entries[0]['supersedes']])
case('N11c review lists the record out of order', ('REFUSED', 'superseded passages differ from the record'), n11c)
def n11d(w):
    inv_root = contract(w.fx, [w.final], [ov(w.final, 2, 'D0', 'D1')])
    entries = [sup(w.final, 2, 'D1', 'D2', inv_root, w.final, 2), csup(w.doc, L2, 'L2a', 'L2b', w.root)]
    contract(w.fx, [w.doc, w.final], supersessions=entries, listed=[entries[1]['supersedes']])
case('N11d mixed record: review omits the inventory link', ('REFUSED', 'superseded passages differ from the record'), n11d)
case('N11e review lists a supersession the record lacks', ('REFUSED', 'superseded passages differ from the record'),
     lambda w: contract(w.fx, [w.doc], [line(w.doc, 1, 'L1', 'L1a')],
                        listed=[{'record': w.root, 'parent': w.doc, 'selector': L2}]))
def n12a(w):
    inv_root = contract(w.fx, [w.final], [ov(w.final, 2, 'D0', 'D1')])
    contract(w.fx, [w.final], supersessions=[{**sup(w.final, 2, 'D1', 'D2', inv_root, w.final, 2),
                                              'selector': {'jsonPointer': '/files/2/role'}}])
case('N12a inventory parent, non-description selector (VD1 unchanged)',
     ('REFUSED', 'must select an inventory row description'), n12a)
case('N12b inventory link naming a contract meaning (VD1 unchanged)',
     ('REFUSED', 'superseded passage is not an inventory row description'),
     lambda w: contract(w.fx, [w.final], supersessions=[{**sup(w.final, 2, 'L2a', 'D2', w.root, w.doc, 0),
                                                         'supersedes': {'record': w.root, 'parent': w.doc, 'selector': L2}}]))
case('N13a silent change: override whose before is the effective text', ('REFUSED', 'before text differs from accepted parent'),
     lambda w: contract(w.fx, [w.doc], [line(w.doc, 2, 'L2a', 'L2b')]))
case('N13b silent change: a second, different override', ('REFUSED', 'conflicting contract passage overrides'),
     lambda w: contract(w.fx, [w.doc], [line(w.doc, 2, 'L2', 'L2b')]))
for label, entry, pattern in (
        ('unknown field', lambda w: {**csup(w.doc, L2, 'L2a', 'L2b', w.root), 'note': 'x'}, 'unknown or missing fields'),
        ('supersedes unknown field', lambda w: {**csup(w.doc, L2, 'L2a', 'L2b', w.root),
                                                'supersedes': {'record': w.root, 'parent': w.doc, 'selector': L2, 'note': 'x'}},
         'superseded passage has unknown or missing fields'),
        ('empty after', lambda w: csup(w.doc, L2, 'L2a', '', w.root), 'must change one text value'),
        ('after equals before', lambda w: csup(w.doc, L2, 'L2a', 'L2a', w.root), 'must change one text value'),
        ('parent outside the record parents', lambda w: csup(w.js, {'jsonPointer': '/text'}, 'T1', 'T2', w.root),
         'parent is outside the accepted parent set'),
        ('selector outside the document', lambda w: csup(w.doc, {'line': 9}, 'L2a', 'L2b', w.root), 'passage line outside document')):
    case(f'N14 malformed: {label}', ('REFUSED', pattern),
         lambda w, entry=entry: contract(w.fx, [w.doc], supersessions=[entry(w)]))
def n15(w):
    fx = w.fx
    lock = fx.lock
    lock['schemaVersion'] = 3
    lock['inventorySuccessor'] = lock.pop('inventorySuccessors')[0]
    first = lock['contractSuccessors'][0]
    lock['contractSuccessors'] = []
    contract(fx, [w.base], members=[fx.write('v3/member.json', {'v': 3})],
             supersessions=[csup(w.base, {'jsonPointer': '/files/0/description'}, 'B0', 'B1', first['record'])])
    lock['contractSuccessor'] = lock.pop('contractSuccessors')[0]
    del lock['inventoryPassageInheritance']
case('N15 a version 3 lock refuses any supersession', ('REFUSED', 'require a v4 successor chain'), n15)

for row in results:
    print(json.dumps(row))
summary = {'tool': {'origin': tool_origin, 'sha256': hashlib.sha256(tool_raw).hexdigest(), 'bytes': len(tool_raw)},
           'fixtureSource': f'{args.rev}:tools/tests/test_design_binding.py',
           'cases': len(results), 'ok': sum(r['ok'] for r in results), 'results': results}
if args.json:
    args.json.write_text(json.dumps(summary, indent=1) + '\n')
print(json.dumps({'cases': summary['cases'], 'ok': summary['ok']}))
sys.exit(0 if summary['ok'] == summary['cases'] else 1)
