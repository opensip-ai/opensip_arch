"""Scratch-only feasibility proof for B-S9 with the product's real verify_design. Synthetic
reviews, assents and probe records are held in memory under SCRATCH-* paths; nothing is written
to either repository.

Usage: verify_scratch.py [PRODUCT_CHECKOUT] [--rev REV]
- Without --rev, the checkout's own tools/verify_design.py and design-lock.json are used, with
  the checkout as the implementation (generation and admission sources are checked).
- With --rev (for example e093e90), both files are read from that commit with read-only git
  plumbing and verify runs design-only.

Runs:
1. B-S9 appended: must PASS. This is the feasibility result. The copies are new accepted paths;
   no passage is overridden, so nothing can conflict.
2. The two rejected forms, as probes that each must REFUSE with the stated message:
   a. a second override of line 1158 on a parent: "conflicting contract passage overrides";
   b. VD1 supersessions of X12-0's two entries: "passage supersession must select an inventory row
      description".
3. Later successors after B-S9 is bound:
   a. an override of the B-S9 copy's line 1158 must PASS: the copy is a fresh key;
   b. an override of an old parent's line 1158 must REFUSE, exactly as it does today (X12-0);
   c. an override of an old parent's line 1157 PASSES. verify_design has no notion of which copy is
      selected, so a later unit that edits a superseded copy is caught only by review. That is the
      residual hazard of the copy form, and the same as capability-totality-reference-selection-v1's."""
import copy, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path

args = list(sys.argv[1:])
rev = None
if '--rev' in args:
    i = args.index('--rev')
    rev = args[i + 1]
    del args[i:i + 2]
W = Path(args[0] if args else '/Users/sb/code/opensip-ai/opensip')
A = Path('/Users/sb/code/opensip-ai/opensip_arch')
B = 'docs/implementation/m3/config-discovery-b/'
OLD = ['docs/coop/design-corrections/native/native_evidence_model.v2.py',
       'docs/implementation/m2/capability-totality-reference-selection-v1/reference/native_evidence_model.py']
X12_0 = 'docs/implementation/m2/config-remedy-x12-0/successor.json'


def git_show(path):
    return subprocess.run(['git', '-C', str(W), 'show', '%s:%s' % (rev, path)], check=True,
                          capture_output=True).stdout


if rev:
    spec = importlib.util.spec_from_loader('vd', loader=None)
    m = importlib.util.module_from_spec(spec)
    exec(compile(git_show('tools/verify_design.py'), 'verify_design.py@' + rev, 'exec'), m.__dict__)
    base_lock = json.loads(git_show('design-lock.json'))
    implementation = None
else:
    spec = importlib.util.spec_from_file_location('vd', W / 'tools/verify_design.py')
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    base_lock = json.loads((W / 'design-lock.json').read_text())
    implementation = W


def pin_bytes(path, b):
    return {'path': path, 'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}


def pin(p):
    return pin_bytes(p, (A / p).read_bytes())


synthetic = {}
real = m.pinned_bytes


def pinned_bytes(root, row):
    if isinstance(row, dict) and row.get('path') in synthetic:
        raw = synthetic[row['path']]
        assert hashlib.sha256(raw).hexdigest() == row['sha256']
        return raw
    return real(root, row)


m.pinned_bytes = pinned_bytes


def serve(path, raw):
    synthetic[path] = raw
    return pin_bytes(path, raw)


def binding(record_pin, subject_pin, tag):
    review = json.dumps({'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [],
                         'subjectManifestSha256': subject_pin['sha256']}).encode()
    rpin = serve('SCRATCH-%s/review.json' % tag, review)
    assent = json.dumps({'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [],
                         'subjectManifest': subject_pin, 'independentReview': rpin,
                         'acceptedSuccessor': record_pin}).encode()
    apin = serve('SCRATCH-%s/assent.json' % tag, assent)
    return {'record': record_pin, 'subjectManifest': subject_pin, 'review': rpin, 'assent': apin}


def probe(tag, parents, overrides=(), supersessions=None):
    note = serve('SCRATCH-%s/README.md' % tag, ('probe %s\n' % tag).encode())
    record = {'schemaVersion': 1, 'standing': 'scratch probe ' + tag, 'parents': sorted(parents, key=lambda r: r['path']),
              'passageOverrides': list(overrides), 'candidates': [note]}
    if supersessions is not None:
        record['passageSupersessions'] = supersessions
    rpin = serve('SCRATCH-%s/successor.json' % tag, (json.dumps(record, indent=2) + '\n').encode())
    spin = serve('SCRATCH-%s/subject.json' % tag, (json.dumps(
        {'schemaVersion': 1, 'files': sorted([note, rpin], key=lambda r: r['path'])}, indent=2) + '\n').encode())
    return binding(rpin, spin, tag)


def run(lock):
    try:
        return 'PASS', m.verify(A, lock, implementation)
    except m.DesignError as exc:
        return 'REFUSED: ' + str(exc), None


base_status, base = run(base_lock)
assert base_status == 'PASS'
out = {'mode': 'rev ' + rev if rev else 'checkout ' + str(W), 'baseContractSuccessors': len(base['contractSuccessors'])}

# 1. B-S9 appended.
bs9 = binding(pin(B + 'b-s9/successor.json'), pin(B + 'b-s9-subject.json'), 'B-S9')
with_bs9 = copy.deepcopy(base_lock)
with_bs9['contractSuccessors'].append(bs9)
status, result = run(with_bs9)
assert status == 'PASS', status
mine = result['contractSuccessors'][-1]
assert mine['passageOverrides'] == [] and mine['passageSupersessions'] == []
assert result['selectedInventory'] == base['selectedInventory']
assert result['inventoryPassageInheritance'] == base['inventoryPassageInheritance']
out['bs9'] = {'status': status, 'contractSuccessors': len(result['contractSuccessors']),
              'candidates': len(mine['inputs']), 'generationSources': result.get('generationSources')}

# 2. the rejected forms.
x12 = json.loads((A / X12_0).read_bytes())
copy_v = B + 'b-s9/reference/native_evidence_model.py'
s9_line = (A / copy_v).read_bytes().decode('utf-8').splitlines()[1157]
lock = copy.deepcopy(base_lock)
o = x12['passageOverrides'][0]
lock['contractSuccessors'].append(probe('SECOND-OVERRIDE', [o['parent']],
                                        [{'parent': o['parent'], 'selector': {'line': 1158}, 'before': o['before'],
                                          'after': s9_line}]))
out['rejected'] = {'secondOverride': run(lock)[0]}
assert out['rejected']['secondOverride'] == 'REFUSED: conflicting contract passage overrides'
lock = copy.deepcopy(base_lock)
x12_pin = [b['record'] for b in base_lock['contractSuccessors'] if b['record']['path'] == X12_0][0]
lock['contractSuccessors'].append(probe('SUPERSESSION', [t['parent'] for t in x12['passageOverrides']], [], [
    {'parent': t['parent'], 'selector': {'line': 1158}, 'before': t['after'], 'after': s9_line,
     'supersedes': {'record': x12_pin, 'parent': t['parent'], 'selector': {'line': 1158}}}
    for t in x12['passageOverrides']]))
out['rejected']['supersession'] = run(lock)[0]
assert out['rejected']['supersession'] == 'REFUSED: passage supersession must select an inventory row description'

# 3. later successors once B-S9 is bound.
later = {}
copy_pin = pin(copy_v)
lock = copy.deepcopy(with_bs9)
lock['contractSuccessors'].append(probe('LATER-COPY', [copy_pin], [
    {'parent': copy_pin, 'selector': {'line': 1158}, 'before': s9_line, 'after': s9_line[:-1] + ' ,'}]))
later['overrideOfCopyLine1158'] = run(lock)[0]
assert later['overrideOfCopyLine1158'] == 'PASS'
old = pin(OLD[1])
old_lines = (A / OLD[1]).read_bytes().decode('utf-8').splitlines()
lock = copy.deepcopy(with_bs9)
lock['contractSuccessors'].append(probe('LATER-OLD-1158', [old], [
    {'parent': old, 'selector': {'line': 1158}, 'before': old_lines[1157], 'after': s9_line}]))
later['overrideOfOldLine1158'] = run(lock)[0]
assert later['overrideOfOldLine1158'] == 'REFUSED: conflicting contract passage overrides'
lock = copy.deepcopy(with_bs9)
lock['contractSuccessors'].append(probe('LATER-OLD-1157', [old], [
    {'parent': old, 'selector': {'line': 1157}, 'before': old_lines[1156], 'after': old_lines[1156] + '  # probe'}]))
later['overrideOfOldOtherLine'] = run(lock)[0]
assert later['overrideOfOldOtherLine'] == 'PASS'
out['laterSuccessors'] = later
print(json.dumps(out, indent=1))
