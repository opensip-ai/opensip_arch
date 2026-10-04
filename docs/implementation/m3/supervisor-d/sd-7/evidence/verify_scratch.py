"""Scratch-only feasibility proof for SD-7 r2 with real verify_design tools. Synthetic reviews, assents and probe
records are held in memory under SCRATCH-* paths; nothing is written to either repository.

Usage: verify_scratch.py [--worktree VD2A_WORKTREE] [--product MAIN_CHECKOUT] [--rev MAIN_REV]

1. VD2-a (the tool SD-7 r2 needs). The VD2-a worktree's own tools/verify_design.py (VD2-a's bytes) over the worktree's
   design-lock.json, which is main's lock plus F8c's staged row with SCRATCH-F8C review and assent pins. Those two
   placeholders are rebuilt exactly as F8c's verify_scratch_f8c.py builds them, and must hash to the staged pins. The
   worktree is the implementation (generation and admission sources are checked).
   a. the staged lock passes: 95 contract successors, contractPassageSupersessions 0;
   b. SD-7 r2 appended, its review carrying supersededPassages equal to the record's supersedes list: PASS, 95 -> 96,
      contractPassageSupersessions 1, inventory chain, inheritance and inventory supersessions unchanged;
   c. refusals: no supersededPassages; a wrong list; a later override restating SD-5's row; a second link naming SD-5;
      a different second override of NE:3539.
2. Plain verify_design at main MAIN_REV (VD1's tool), design-only, refuses SD-7 r2 (fails closed) both over main's lock
   and over the staged lock.
3. Law VD2 item 4: the effective NE after SD-7 r2, folded from the staged lock independently of the tool, equals
   SD-7 r1's NE7 (380,848 bytes, 0dd155c2...)."""
import argparse, copy, hashlib, importlib.util, json, subprocess
from pathlib import Path

ap = argparse.ArgumentParser()
ap.add_argument('--worktree', type=Path, default=Path('/Users/sb/code/opensip-ai/opensip-vd2a'))
ap.add_argument('--product', type=Path, default=Path('/Users/sb/code/opensip-ai/opensip'))
ap.add_argument('--rev', default='4c761e8')
args = ap.parse_args()
A = Path('/Users/sb/code/opensip-ai/opensip_arch')
B = 'docs/implementation/m3/supervisor-d/'
NE = 'docs/v2/contracts/product-v1/native-evidence.md'
SD5 = B + 'sd-5/successor.json'
F8C = 'docs/implementation/m3/verify-design-vd2/f8c'
NE7 = {'bytes': 380848, 'sha256': '0dd155c2e2439b2223cdcfaec2ecad61c89bcf6a348f3be3c8f3350e9555ebd3'}


def sha(b):
    return hashlib.sha256(b).hexdigest()


def pin_bytes(path, b):
    return {'path': path, 'bytes': len(b), 'sha256': sha(b)}


def pin(p):
    return pin_bytes(p, (A / p).read_bytes())


synthetic = {}


def load(label, raw, origin):
    m = importlib.util.module_from_spec(importlib.util.spec_from_loader(label, loader=None))
    exec(compile(raw, origin, 'exec'), m.__dict__)
    real = m.pinned_bytes

    def pinned_bytes(root, row):
        if isinstance(row, dict) and row.get('path') in synthetic:
            data = synthetic[row['path']]
            assert sha(data) == row['sha256'] and len(data) == row['bytes']
            return data
        return real(root, row)
    m.pinned_bytes = pinned_bytes
    return m


def serve(path, raw):
    synthetic[path] = raw
    return pin_bytes(path, raw)


def assent_for(record_pin, subject_pin, rpin):
    return json.dumps({'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [],
                       'subjectManifest': subject_pin, 'independentReview': rpin,
                       'acceptedSuccessor': record_pin}).encode()


def binding(record_pin, subject_pin, tag, superseded=None, omit_list=False):
    review = {'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [], 'subjectManifestSha256': subject_pin['sha256']}
    if not omit_list and superseded is not None:
        review['supersededPassages'] = superseded
    rpin = serve('SCRATCH-%s/review.json' % tag, json.dumps(review).encode())
    apin = serve('SCRATCH-%s/assent.json' % tag, assent_for(record_pin, subject_pin, rpin))
    return {'record': record_pin, 'subjectManifest': subject_pin, 'review': rpin, 'assent': apin}


def probe(tag, parents, overrides=(), supersessions=None, superseded=None):
    note = serve('SCRATCH-%s/README.md' % tag, ('probe %s\n' % tag).encode())
    rec = {'schemaVersion': 1, 'standing': 'scratch probe ' + tag, 'parents': sorted(parents, key=lambda r: r['path']),
           'passageOverrides': list(overrides), 'candidates': [note]}
    if supersessions is not None:
        rec['passageSupersessions'] = supersessions
    rpin = serve('SCRATCH-%s/successor.json' % tag, (json.dumps(rec, indent=2) + '\n').encode())
    spin = serve('SCRATCH-%s/subject.json' % tag, (json.dumps(
        {'schemaVersion': 1, 'files': sorted([note, rpin], key=lambda r: r['path'])}, indent=2) + '\n').encode())
    return binding(rpin, spin, tag, superseded)


def run(m, lock, implementation=None):
    try:
        return 'PASS', m.verify(A, lock, implementation)
    except m.DesignError as exc:
        return 'REFUSED: ' + str(exc), None


def git_show(rev, path):
    return subprocess.run(['git', '-C', str(args.product), 'show', '%s:%s' % (rev, path)], check=True,
                          capture_output=True).stdout


out = {}
record_pin, subject_pin = pin(B + 'sd-7/successor.json'), pin(B + 'sd-7-subject.json')
record = json.loads((A / record_pin['path']).read_bytes())
superseded = [e['supersedes'] for e in record['passageSupersessions']]

# ---- 1. VD2-a over the staged lock ----------------------------------------------------------
vd2a_raw = (args.worktree / 'tools/verify_design.py').read_bytes()
main_tool_raw = git_show(args.rev, 'tools/verify_design.py')
assert vd2a_raw != main_tool_raw and b'contractPassageSupersessions' in vd2a_raw
vd2a = load('vd2a', vd2a_raw, str(args.worktree / 'tools/verify_design.py'))
staged = json.loads((args.worktree / 'design-lock.json').read_bytes())
main_lock = json.loads(git_show(args.rev, 'design-lock.json'))
assert staged['contractSuccessors'][:-1] == main_lock['contractSuccessors']
assert {k: v for k, v in staged.items() if k != 'contractSuccessors'} == \
    {k: v for k, v in main_lock.items() if k != 'contractSuccessors'}
f8c_row = staged['contractSuccessors'][-1]
assert f8c_row['record'] == pin(F8C + '/successor.json') and f8c_row['subjectManifest'] == pin(F8C + '-subject.json')
f8c_review = json.dumps({'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [],
                         'subjectManifestSha256': f8c_row['subjectManifest']['sha256']}).encode()
assert serve('SCRATCH-F8C/review.json', f8c_review) == f8c_row['review']
assert serve('SCRATCH-F8C/assent.json', assent_for(f8c_row['record'], f8c_row['subjectManifest'],
                                                   f8c_row['review'])) == f8c_row['assent']
st, base = run(vd2a, staged, args.worktree)
assert st == 'PASS' and len(base['contractSuccessors']) == 95 and base['contractPassageSupersessions'] == 0, st
sd7 = binding(record_pin, subject_pin, 'SD-7', superseded)
with_sd7 = copy.deepcopy(staged)
with_sd7['contractSuccessors'].append(sd7)
st, res = run(vd2a, with_sd7, args.worktree)
assert st == 'PASS', st
mine = res['contractSuccessors'][-1]
assert mine['selected'] == record_pin['path'] and len(mine['passageOverrides']) == 3 and len(mine['passageSupersessions']) == 1
assert res['contractPassageSupersessions'] == 1
for k in ('selectedInventory', 'inventoryPassageInheritance', 'inventoryPassageSupersessions', 'generationSources',
          'admissionSources'):
    assert res.get(k) == base.get(k), k
out['vd2a'] = {'tool': pin_bytes(str(args.worktree / 'tools/verify_design.py'), vd2a_raw),
               'stagedLock': {'contractSuccessors': len(base['contractSuccessors']), 'status': 'PASS',
                              'contractPassageSupersessions': 0, 'f8cPlaceholdersServed': True},
               'withSD7r2': {'status': st, 'contractSuccessors': len(res['contractSuccessors']),
                             'contractPassageSupersessions': res['contractPassageSupersessions'],
                             'passageOverrides': 3, 'passageSupersessions': 1, 'candidates': len(mine['inputs']),
                             'inventoryPassageSupersessions': res['inventoryPassageSupersessions'],
                             'generationSources': res.get('generationSources'),
                             'admissionSources': res.get('admissionSources')}}

# 1c. refusals under VD2-a
ne = pin(NE)
ne_lines = (A / NE).read_bytes().decode('utf-8').splitlines()
sd5_pin = pin(SD5)
sd5_entry = json.loads((A / SD5).read_bytes())['passageOverrides'][0]
refusals = {}
lock = copy.deepcopy(staged)
lock['contractSuccessors'].append(binding(record_pin, subject_pin, 'SD-7-NOLIST', superseded, omit_list=True))
refusals['reviewWithoutSupersededPassages'] = run(vd2a, lock)[0]
lock = copy.deepcopy(staged)
lock['contractSuccessors'].append(binding(record_pin, subject_pin, 'SD-7-WRONGLIST', []))
refusals['reviewWithWrongList'] = run(vd2a, lock)[0]
lock = copy.deepcopy(with_sd7)
lock['contractSuccessors'].append(probe('RESTATE', [ne], [dict(sd5_entry)]))
refusals['laterOverrideRestatingSD5'] = run(vd2a, lock)[0]
link = record['passageSupersessions'][0]
lock = copy.deepcopy(with_sd7)
lock['contractSuccessors'].append(probe('RELINK', [ne], [], [dict(link, after=link['after'] + ' ')],
                                        [link['supersedes']]))
refusals['secondLinkNamingSD5'] = run(vd2a, lock)[0]
lock = copy.deepcopy(with_sd7)
lock['contractSuccessors'].append(probe('NE3539', [ne], [
    {'parent': ne, 'selector': {'line': 3539}, 'before': ne_lines[3538], 'after': ne_lines[3538] + ' (probe)'}]))
refusals['differentOverrideOfNE3539'] = run(vd2a, lock)[0]
expected = {'reviewWithoutSupersededPassages': 'REFUSED: contract passage supersession is not listed by its review',
            'reviewWithWrongList': 'REFUSED: contract review superseded passages differ from the record',
            'laterOverrideRestatingSD5': 'REFUSED: passage override restates a superseded contract meaning',
            'secondLinkNamingSD5': 'REFUSED: double supersession: the named passage is not the current meaning',
            'differentOverrideOfNE3539': 'REFUSED: conflicting contract passage overrides'}
assert refusals == expected, refusals
out['vd2aRefusals'] = refusals

# ---- 2. plain verify_design at main fails closed -------------------------------------------
plain = load('plain', main_tool_raw, 'verify_design.py@' + args.rev)
st_main, _ = run(plain, main_lock)
assert st_main == 'PASS'
lock = copy.deepcopy(main_lock)
lock['contractSuccessors'].append(sd7)
plain_main = run(plain, lock)[0]
lock = copy.deepcopy(staged)
lock['contractSuccessors'].append(sd7)
plain_staged = run(plain, lock)[0]
for s in (plain_main, plain_staged):
    assert s == 'REFUSED: passage supersession must select an inventory row description', s
out['plainAtMain'] = {'tool': pin_bytes('verify_design.py@' + args.rev, main_tool_raw),
                      'mainLock': {'contractSuccessors': len(main_lock['contractSuccessors']), 'status': st_main},
                      'mainLockPlusSD7r2': plain_main, 'stagedLockPlusSD7r2': plain_staged}

# ---- 3. the effective NE (law VD2 item 4) ---------------------------------------------------
text = {}
for b in with_sd7['contractSuccessors']:
    rec = json.loads(synthetic[b['record']['path']] if b['record']['path'] in synthetic
                     else (A / b['record']['path']).read_bytes())
    for e in rec.get('passageOverrides', []) + rec.get('passageSupersessions', []):
        if e['parent']['path'] == NE:
            text[e['selector']['line']] = e['after']
effective = ('\n'.join(text.get(i, l) for i, l in enumerate(ne_lines, 1)) + '\n').encode('utf-8')
assert {'bytes': len(effective), 'sha256': sha(effective)} == NE7
out['effectiveNE'] = dict(NE7, equalsSD7r1NE7=True)
print(json.dumps(out, indent=1))
