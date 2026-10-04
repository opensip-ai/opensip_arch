"""Scratch-only feasibility proof for SD-7 with the product's real verify_design. Synthetic reviews, assents and
probe records are held in memory under SCRATCH-* paths; nothing is written to either repository.

Usage: verify_scratch.py [PRODUCT_CHECKOUT] [--rev REV]
- Without --rev, the checkout's own tools/verify_design.py and design-lock.json are used, with the checkout as the
  implementation (generation and admission sources are checked).
- With --rev (for example 6190e66), both files are read from that commit with read-only git plumbing and verify
  runs design-only.

Runs:
1. SD-7 appended: must PASS, with exactly the two line-1159 overrides of B-S9's model copies and no supersession,
   the selected inventory and the inheritance projection unchanged, and one more contract successor.
2. The rejected forms, as probes that must REFUSE with the stated message:
   a. conforming SD-5's row by a second override of NE:3540: "conflicting contract passage overrides";
   b. a VD1 supersession of SD-5's NE:3540 entry: "passage supersession must select an inventory row description".
3. Later successors once SD-7 is bound:
   a. an override of a line of the NE copy PASSES: the copy is a fresh key;
   b. a second override of a B-S9 copy's line 1159 REFUSES: "conflicting contract passage overrides";
   c. an override of an unoverridden raw NE line (NE:3539) PASSES. verify_design has no notion of which NE text is
      selected, so a later unit that edits the superseded raw NE is caught only by review: the copy form's residual
      hazard, the same as B-S9's and capability-totality-reference-selection-v1's."""
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
B = 'docs/implementation/m3/supervisor-d/'
NE = 'docs/v2/contracts/product-v1/native-evidence.md'
COPY = B + 'sd-7/contracts/native-evidence.md'
SD5 = B + 'sd-5/successor.json'
NEM = 'docs/implementation/m3/config-discovery-b/b-s9/reference/native_evidence_model.py'


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
    record = {'schemaVersion': 1, 'standing': 'scratch probe ' + tag,
              'parents': sorted(parents, key=lambda r: r['path']), 'passageOverrides': list(overrides),
              'candidates': [note]}
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
assert base_status == 'PASS', base_status
out = {'mode': 'rev ' + rev if rev else 'checkout ' + str(W), 'baseContractSuccessors': len(base['contractSuccessors'])}

# 1. SD-7 appended.
sd7 = binding(pin(B + 'sd-7/successor.json'), pin(B + 'sd-7-subject.json'), 'SD-7')
with_sd7 = copy.deepcopy(base_lock)
with_sd7['contractSuccessors'].append(sd7)
status, result = run(with_sd7)
assert status == 'PASS', status
mine = result['contractSuccessors'][-1]
assert mine['passageSupersessions'] == [] and len(mine['passageOverrides']) == 2
assert {(o['parent']['path'], o['selector']['line']) for o in mine['passageOverrides']} == {
    (NEM, 1159), (NEM.replace('.py', '.v2.py'), 1159)}
assert result['selectedInventory'] == base['selectedInventory']
assert result['inventoryPassageInheritance'] == base['inventoryPassageInheritance']
out['sd-7'] = {'status': status, 'contractSuccessors': len(result['contractSuccessors']),
               'passageOverrides': len(mine['passageOverrides']), 'passageSupersessions': 0,
               'candidates': len(mine['inputs']), 'generationSources': result.get('generationSources')}

# 2. the rejected forms.
ne = pin(NE)
ne_lines = (A / NE).read_bytes().decode('utf-8').splitlines()
sd5_pin = next(b['record'] for b in base_lock['contractSuccessors'] if b['record']['path'] == SD5)
sd5_entry = json.loads((A / SD5).read_bytes())['passageOverrides'][0]
copy_lines = (A / COPY).read_bytes().decode('utf-8').splitlines()
conformed = next(l for l in copy_lines if l.startswith('| **component manifest that is an excluded form**'))
lock = copy.deepcopy(base_lock)
lock['contractSuccessors'].append(probe('SECOND-OVERRIDE', [ne], [
    {'parent': ne, 'selector': {'line': 3540}, 'before': ne_lines[3539], 'after': ne_lines[3539] + '\n' + conformed}]))
rejected = {'secondOverrideOfNE3540': run(lock)[0]}
assert rejected['secondOverrideOfNE3540'] == 'REFUSED: conflicting contract passage overrides'
lock = copy.deepcopy(base_lock)
lock['contractSuccessors'].append(probe('SUPERSESSION', [ne], [], [
    {'parent': ne, 'selector': {'line': 3540}, 'before': sd5_entry['after'],
     'after': ne_lines[3539] + '\n' + conformed,
     'supersedes': {'record': sd5_pin, 'parent': ne, 'selector': {'line': 3540}}}]))
rejected['vd1SupersessionOfSD5'] = run(lock)[0]
assert rejected['vd1SupersessionOfSD5'] == 'REFUSED: passage supersession must select an inventory row description'
out['rejectedForms'] = rejected

# 3. later successors once SD-7 is bound.
later = {}
cpin = pin(COPY)
n = copy_lines.index(conformed) + 1
lock = copy.deepcopy(with_sd7)
lock['contractSuccessors'].append(probe('LATER-COPY', [cpin], [
    {'parent': cpin, 'selector': {'line': n}, 'before': conformed, 'after': conformed + ' '}]))
later['overrideOfCopyLine'] = run(lock)[0]
assert later['overrideOfCopyLine'] == 'PASS'
npin = pin(NEM)
nem_line = (A / NEM).read_bytes().decode('utf-8').splitlines()[1158]
lock = copy.deepcopy(with_sd7)
lock['contractSuccessors'].append(probe('LATER-1159', [npin], [
    {'parent': npin, 'selector': {'line': 1159}, 'before': nem_line, 'after': nem_line + '  # probe'}]))
later['secondOverrideOfModelLine1159'] = run(lock)[0]
assert later['secondOverrideOfModelLine1159'] == 'REFUSED: conflicting contract passage overrides'
lock = copy.deepcopy(with_sd7)
lock['contractSuccessors'].append(probe('LATER-RAW-NE', [ne], [
    {'parent': ne, 'selector': {'line': 3539}, 'before': ne_lines[3538], 'after': ne_lines[3538] + ' '}]))
later['overrideOfRawNE3539'] = run(lock)[0]
assert later['overrideOfRawNE3539'] == 'PASS'
out['laterSuccessors'] = later
print(json.dumps(out, indent=1))
