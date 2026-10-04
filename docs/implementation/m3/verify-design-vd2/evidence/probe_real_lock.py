"""VD2 probe over the real design lock: SD-7 r2's clean form and its refusals. Writes nothing to either repository.

It runs a verify_design (by default the VD2 prototype, ../reference/verify_design.prototype.py) over the product lock at
REV (read with `git show`), plus synthetic contract successors whose records, subjects, reviews and assents live in
memory under SCRATCH-VD2/ paths. It also runs the REV tool itself on the same cases, to show how it behaves today.

The SD-7 r2 form (law VD2 item 6, "SD-7 r2"):
- a passage supersession of SD-5's NE:3540 override, naming SD-5's record pin, with SD-7 r1's conformed row;
- an ordinary override of NE:3539, which no bound successor overrides, inserting item 25's row after it;
- SD-7 r1's two line-1159 overrides of B-S9's native-model copies, unchanged.
The row texts are read from SD-7 r1's draft copy NE7 (lines 3822 and 3824); NE7 is not a parent and is not selected.

The probe also folds every bound passage entry on native-evidence.md in lock order (law VD2 item 4) independently of
the tool, and compares the result with NE7: r2's effective NE should equal r1's complete copy byte for byte.

Usage: python3.14 -I -B probe_real_lock.py [--tool PATH] [--product CHECKOUT] [--rev REV] [--json OUT]
Exit 0 only if every case gives its expected outcome under both tools.
"""
import argparse, copy, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ap = argparse.ArgumentParser()
ap.add_argument('--tool', type=Path, default=HERE.parent / 'reference/verify_design.prototype.py')
ap.add_argument('--product', type=Path, default=Path('/Users/sb/code/opensip-ai/opensip'))
ap.add_argument('--architecture', type=Path, default=Path('/Users/sb/code/opensip-ai/opensip_arch'))
ap.add_argument('--rev', default='6190e66')
ap.add_argument('--json', type=Path)
args = ap.parse_args()
A = args.architecture


def git_show(path):
    return subprocess.run(['git', '-C', str(args.product), 'show', f'{args.rev}:{path}'], check=True,
                          capture_output=True).stdout


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def pin_bytes(path, raw):
    return {'path': path, 'bytes': len(raw), 'sha256': sha(raw)}


def pin(path):
    return pin_bytes(path, (A / path).read_bytes())


synthetic = {}


def load_tool(label, raw, origin):
    module = importlib.util.module_from_spec(importlib.util.spec_from_loader(label, loader=None))
    exec(compile(raw, origin, 'exec'), module.__dict__)
    real = module.pinned_bytes

    def pinned_bytes(root, row):
        if isinstance(row, dict) and row.get('path') in synthetic:
            data = synthetic[row['path']]
            if sha(data) != row.get('sha256'):
                raise module.DesignError('synthetic digest mismatch')
            return data
        return real(root, row)
    module.pinned_bytes = pinned_bytes
    return module


tool_raw = args.tool.read_bytes()
base_raw = git_show('tools/verify_design.py')
TOOLS = {'vd2': load_tool('vd2', tool_raw, str(args.tool)), args.rev: load_tool('base', base_raw, f'verify_design.py@{args.rev}')}
lock_raw = git_show('design-lock.json')
BASE_LOCK = json.loads(lock_raw)

NE = 'docs/v2/contracts/product-v1/native-evidence.md'
NE7 = 'docs/implementation/m3/supervisor-d/sd-7/contracts/native-evidence.md'
SD5 = 'docs/implementation/m3/supervisor-d/sd-5/successor.json'
SD7R1 = 'docs/implementation/m3/supervisor-d/sd-7/successor.json'
NEM = 'docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.py'
X120 = 'docs/implementation/m2/config-remedy-x12-0/successor.json'
CT = 'docs/implementation/m2/capability-totality-reference-selection-v1/reference/native_evidence_model.py'
CR1 = 'docs/implementation/m3/snapshot-plan-c/cr-1/successor.json'
SYN1 = 'docs/implementation/m3/syntax-e/syn-1/successor.json'


def bound(path):
    return next(b['record'] for b in BASE_LOCK['contractSuccessors'] if b['record']['path'] == path)


def entry_of(path, parent_path, selector):
    record = json.loads((A / path).read_bytes())
    return next(o for o in record['passageOverrides']
                if o['parent']['path'] == parent_path and o['selector'] == selector)


ne_pin = pin(NE)
ne_raw = (A / NE).read_bytes()
assert b'\r' not in ne_raw and ne_raw.endswith(b'\n')
ne_lines = ne_raw.decode('utf-8').splitlines()
ne7_raw = (A / NE7).read_bytes()
ne7_lines = ne7_raw.decode('utf-8').splitlines()
# NE7: the NOT-SELECTED row (raw 3539), item 25's row, the release declaration row (raw 3540), SD-5's row conformed.
assert ne7_lines[3820] == ne_lines[3538] and ne7_lines[3822] == ne_lines[3539]
item25, conformed = ne7_lines[3821], ne7_lines[3823]
sd5_pin = bound(SD5)
sd5_entry = entry_of(SD5, NE, {'line': 3540})
assert sd5_entry['before'] == ne_lines[3539] and sd5_entry['after'].split('\n')[0] == ne_lines[3539]
sd7r1 = json.loads((A / SD7R1).read_bytes())
remedy_overrides = sd7r1['passageOverrides']
assert [o['parent']['path'] for o in remedy_overrides] == [NEM, NEM.replace('.py', '.v2.py')]

SUPERSEDE_3540 = {'parent': ne_pin, 'selector': {'line': 3540}, 'before': sd5_entry['after'],
                  'after': ne_lines[3539] + '\n' + conformed,
                  'supersedes': {'record': sd5_pin, 'parent': ne_pin, 'selector': {'line': 3540}}}
OVERRIDE_3539 = {'parent': ne_pin, 'selector': {'line': 3539}, 'before': ne_lines[3538],
                 'after': ne_lines[3538] + '\n' + item25}


def unit(tag, parents, overrides=(), supersessions=(), listed='auto'):
    note = pin_bytes(f'SCRATCH-VD2/{tag}/README.md', f'probe {tag}\n'.encode())
    synthetic[note['path']] = f'probe {tag}\n'.encode()
    record = {'schemaVersion': 1, 'standing': f'SCRATCH VD2 probe {tag}',
              'parents': sorted(copy.deepcopy(parents), key=lambda r: r['path']),
              'passageOverrides': list(overrides), 'candidates': [note]}
    if supersessions:
        record['passageSupersessions'] = list(supersessions)
    rec_raw = (json.dumps(record, indent=2) + '\n').encode()
    rpin = pin_bytes(f'SCRATCH-VD2/{tag}/successor.json', rec_raw)
    subj_raw = (json.dumps({'schemaVersion': 1, 'files': sorted([note, rpin], key=lambda r: r['path'])}, indent=2) + '\n').encode()
    spin = pin_bytes(f'SCRATCH-VD2/{tag}-subject.json', subj_raw)
    review = {'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [], 'subjectManifestSha256': spin['sha256']}
    if listed == 'auto' and supersessions:
        review['supersededPassages'] = [entry['supersedes'] for entry in supersessions]
    elif listed not in ('auto', None):
        review['supersededPassages'] = listed
    rev_raw = json.dumps(review).encode()
    vpin = pin_bytes(f'SCRATCH-VD2/{tag}/review.json', rev_raw)
    ass_raw = json.dumps({'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [],
                          'subjectManifest': spin, 'independentReview': vpin, 'acceptedSuccessor': rpin}).encode()
    apin = pin_bytes(f'SCRATCH-VD2/{tag}/assent.json', ass_raw)
    synthetic.update({rpin['path']: rec_raw, spin['path']: subj_raw, vpin['path']: rev_raw, apin['path']: ass_raw})
    return {'record': rpin, 'subjectManifest': spin, 'review': vpin, 'assent': apin}


def sd7r2(tag='SD-7-r2', **kw):
    return unit(tag, [ne_pin, remedy_overrides[0]['parent'], remedy_overrides[1]['parent']],
                [OVERRIDE_3539, *remedy_overrides], [SUPERSEDE_3540], **kw)


def record_of(row):
    raw = synthetic.get(row['path'])
    return json.loads(raw if raw is not None else (A / row['path']).read_bytes())


def effective(path, lock):
    """Law VD2 item 4's consumer fold: every bound entry on path, in lock order; each sets its passage's text."""
    lines = (A / path).read_bytes().decode('utf-8').splitlines()
    texts, applied = {}, 0
    for binding in lock['contractSuccessors']:
        record = record_of(binding['record'])
        for entry in [*record.get('passageOverrides', []), *record.get('passageSupersessions', [])]:
            if entry['parent']['path'] == path:
                texts[entry['selector']['line']] = entry['after']
                applied += 1
    out = [texts.get(i + 1, text) for i, text in enumerate(lines)]
    return ('\n'.join(out) + '\n').encode('utf-8'), applied, len(texts)


results = []


def run(name, bindings, expect, extra=None):
    lock = copy.deepcopy(BASE_LOCK)
    lock['contractSuccessors'] += bindings
    row = {'case': name, 'expect': expect}
    for label, tool in TOOLS.items():
        try:
            out = tool.verify(A, lock)
            outcome = ['PASSED', len(out['contractSuccessors']), out.get('contractPassageSupersessions'),
                       out['inventoryPassageSupersessions'], len(out['inventoryPassageInheritance'])]
            row.setdefault('outputs', {})[label] = out
        except tool.DesignError as exc:
            outcome = ['REFUSED', str(exc)]
        row[label] = outcome
    want = expect['vd2']
    row['ok'] = (row['vd2'][0] == want[0] and (want[0] == 'PASSED' and row['vd2'][2] == want[1]
                                                or want[0] == 'REFUSED' and want[1] in row['vd2'][1]))
    if want[0] == 'PASSED':
        row['ok'] = row['ok'] and row['vd2'][3:] == [21, 100]
    base_want = expect.get('base')
    if base_want:
        row['ok'] = row['ok'] and row[args.rev][0] == base_want[0] and (base_want[0] == 'PASSED' or base_want[1] in row[args.rev][1])
    if extra:
        row.update(extra(lock))
        row['ok'] = row['ok'] and row.get('extraOk', True)
    outputs = row.pop('outputs', {})
    results.append(row)
    return outputs, lock


FAIL_CLOSED = ('REFUSED', 'passage supersession must select an inventory row description')

# R0. The real lock: the two tools agree on every field; VD2 adds only its count.
outputs, _ = run('R0 real lock at REV, unchanged', [], {'vd2': ('PASSED', 0), 'base': ('PASSED',)})
vd2_out, base_out = outputs['vd2'], outputs[args.rev]
results[-1]['sameOutputExceptCount'] = (set(vd2_out) - set(base_out) == {'contractPassageSupersessions'}
                                        and all(vd2_out[k] == base_out[k] for k in base_out))
results[-1]['ok'] = results[-1]['ok'] and results[-1]['sameOutputExceptCount']


def ne7_equal(lock):
    raw, applied, keys = effective(NE, lock)
    base_raw_, base_applied, base_keys = effective(NE, BASE_LOCK)
    return {'effectiveNE': {'bytes': len(raw), 'sha256': sha(raw), 'entriesApplied': applied, 'passages': keys},
            'effectiveNEAtRev': {'bytes': len(base_raw_), 'sha256': sha(base_raw_), 'entriesApplied': base_applied},
            'ne7': {'path': NE7, 'bytes': len(ne7_raw), 'sha256': sha(ne7_raw)},
            'equalsNE7': raw == ne7_raw, 'extraOk': raw == ne7_raw}


R1 = sd7r2()
run('R1 SD-7 r2 clean form: supersede SD-5 NE:3540, override NE:3539, two NEM line-1159 overrides', [R1],
    {'vd2': ('PASSED', 1), 'base': FAIL_CLOSED}, ne7_equal)
link2 = unit('second-link', [ne_pin], supersessions=[{
    **SUPERSEDE_3540, 'before': SUPERSEDE_3540['after'], 'after': SUPERSEDE_3540['after'] + ' (probe r3)',
    'supersedes': {'record': R1['record'], 'parent': ne_pin, 'selector': {'line': 3540}}}])
run('R2 a second link names SD-7 r2 (the tail)', [R1, link2], {'vd2': ('PASSED', 2), 'base': FAIL_CLOSED})
wrong = unit('wrong-pin', [ne_pin], supersessions=[{**SUPERSEDE_3540, 'supersedes': {
    **SUPERSEDE_3540['supersedes'], 'record': {**sd5_pin, 'sha256': '0' * 64}}}])
run('R3 wrong record pin for SD-5', [wrong], {'vd2': ('REFUSED', 'superseded record is not an earlier contract successor'), 'base': FAIL_CLOSED})
shadow_raw = (A / SD5).read_bytes()
shadow = pin_bytes('SCRATCH-VD2/unbound/successor.json', shadow_raw)
synthetic[shadow['path']] = shadow_raw
unbound = unit('unbound', [ne_pin], supersessions=[{**SUPERSEDE_3540, 'supersedes': {
    **SUPERSEDE_3540['supersedes'], 'record': shadow}}])
run('R4 unbound target: a byte-identical copy of SD-5\'s record that the lock does not bind', [unbound],
    {'vd2': ('REFUSED', 'superseded record is not an earlier contract successor'), 'base': FAIL_CLOSED})
r1_record = unit('names-sd7-r1', [ne_pin], supersessions=[{**SUPERSEDE_3540, 'supersedes': {
    **SUPERSEDE_3540['supersedes'], 'record': pin(SD7R1)}}])
run('R5 unbound target: SD-7 r1\'s draft record (in arch, not bound)', [r1_record],
    {'vd2': ('REFUSED', 'superseded record is not an earlier contract successor'), 'base': FAIL_CLOSED})
absent = unit('absent-entry', [ne_pin], supersessions=[{**SUPERSEDE_3540, 'supersedes': {
    **SUPERSEDE_3540['supersedes'], 'selector': {'line': 3541}}}])
run('R6 SD-5 has no NE:3541 entry', [absent], {'vd2': ('REFUSED', 'superseded passage is not in the named record'), 'base': FAIL_CLOSED})
syn1_entry = entry_of(SYN1, NE, {'line': 3541})
other = unit('other-passage', [ne_pin], supersessions=[{**SUPERSEDE_3540, 'before': syn1_entry['after'], 'supersedes': {
    'record': bound(SYN1), 'parent': ne_pin, 'selector': {'line': 3541}}}])
run('R7 names SYN-1\'s NE:3541 meaning from an NE:3540 link', [other], {'vd2': ('REFUSED', 'selects a different passage'), 'base': FAIL_CLOSED})
stale = unit('stale', [ne_pin], supersessions=[{**SUPERSEDE_3540, 'before': ne_lines[3539]}])
run('R8 stale before: raw NE:3540', [stale], {'vd2': ('REFUSED', 'before text differs from the superseded meaning'), 'base': FAIL_CLOSED})
again = unit('again', [ne_pin], supersessions=[{**SUPERSEDE_3540, 'after': SUPERSEDE_3540['after'] + ' (again)'}])
run('R9 double supersession of SD-5', [R1, again], {'vd2': ('REFUSED', 'double supersession'), 'base': FAIL_CLOSED})
restate = unit('restate', [ne_pin], [sd5_entry])
run('R10 restating SD-5\'s superseded row as an override', [R1, restate], {'vd2': ('REFUSED', 'restates a superseded contract meaning'), 'base': FAIL_CLOSED})
second = unit('second-override', [ne_pin], [{**sd5_entry, 'after': SUPERSEDE_3540['after']}])
run('R11 a second override of NE:3540 (SD-7 r1 probe 2a)', [second],
    {'vd2': ('REFUSED', 'conflicting contract passage overrides'), 'base': ('REFUSED', 'conflicting contract passage overrides')})
run('R12 the review does not list the supersession', [sd7r2('unlisted', listed=None)],
    {'vd2': ('REFUSED', 'not listed by its review'), 'base': FAIL_CLOSED})
run('R13 the review lists a different passage', [sd7r2('mislisted', listed=[{**SUPERSEDE_3540['supersedes'], 'selector': {'line': 3539}}])],
    {'vd2': ('REFUSED', 'superseded passages differ from the record'), 'base': FAIL_CLOSED})
lock14 = copy.deepcopy(BASE_LOCK)
sd5_binding = next(b for b in lock14['contractSuccessors'] if b['record']['path'] == SD5)
lock14['contractSuccessors'] = [b for b in lock14['contractSuccessors'] if b is not sd5_binding] + [R1, sd5_binding]
try:
    TOOLS['vd2'].verify(A, lock14)
    outcome14 = ['PASSED']
except TOOLS['vd2'].DesignError as exc:
    outcome14 = ['REFUSED', str(exc)]
results.append({'case': 'R14 SD-7 r2 ordered before SD-5 (SD-5 moved after it)', 'note': 'vd2 tool only',
                'expect': {'vd2': ['REFUSED', 'superseded record is not an earlier contract successor']}, 'vd2': outcome14,
                'ok': outcome14 == ['REFUSED', 'superseded record is not an earlier contract successor']})
# Generality: the B-S9 and CR-1 shapes.
x120 = entry_of(X120, CT, {'line': 1158})
bs9_line = (A / NEM).read_bytes().decode('utf-8').splitlines()[1157]
bs9 = unit('b-s9-shape', [x120['parent']], supersessions=[{'parent': x120['parent'], 'selector': {'line': 1158},
    'before': x120['after'], 'after': bs9_line, 'supersedes': {'record': bound(X120), 'parent': x120['parent'], 'selector': {'line': 1158}}}])
run('R15 B-S9 shape: supersede X12-0\'s line 1158 on the capability-totality copy (illustration only)', [bs9],
    {'vd2': ('PASSED', 1), 'base': FAIL_CLOSED})
cr1 = entry_of(CR1, 'docs/coop/artifacts/component-manifest-schemas.v11.json', {'jsonPointer': '/manifestSchema/fields/7/semantics'})
json_link = unit('json-pointer', [cr1['parent']], supersessions=[{'parent': cr1['parent'], 'selector': cr1['selector'],
    'before': cr1['after'], 'after': cr1['after'] + ' (probe)', 'supersedes': {'record': bound(CR1), 'parent': cr1['parent'], 'selector': cr1['selector']}}])
run('R16 JSON Pointer: supersede CR-1\'s DR-103 fields/7 semantics', [json_link], {'vd2': ('PASSED', 1), 'base': FAIL_CLOSED})

for row in results:
    print(json.dumps({k: v for k, v in row.items() if k not in ('effectiveNEAtRev',)}))
summary = {'standing': 'VD2 law evidence: prototype feasibility over the real lock; not the VD2-a subject, not a binding',
           'tool': {'path': str(args.tool), 'bytes': len(tool_raw), 'sha256': sha(tool_raw)},
           'baseTool': {'rev': args.rev, 'bytes': len(base_raw), 'sha256': sha(base_raw)},
           'lock': {'rev': args.rev, 'bytes': len(lock_raw), 'sha256': sha(lock_raw),
                    'contractSuccessors': len(BASE_LOCK['contractSuccessors'])},
           'cases': len(results), 'ok': sum(r['ok'] for r in results), 'results': results}
if args.json:
    args.json.write_text(json.dumps(summary, indent=1) + '\n')
print(json.dumps({'cases': summary['cases'], 'ok': summary['ok']}))
sys.exit(0 if summary['ok'] == summary['cases'] else 1)
