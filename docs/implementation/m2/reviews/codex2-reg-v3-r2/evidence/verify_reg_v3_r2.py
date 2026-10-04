"""Local binding check for registry owner selection v3 r2, in a throwaway product worktree.

The worktree's own tools/verify_design.py is loaded unchanged. SCRATCH-REGV3 review and assent pins are
served from memory by an overlay of pinned_bytes, as F8c's and SD-7's verify_scratch scripts do; nothing is
written to the architecture repository. The worktree's design-lock.json gets the candidate entry appended.
"""
import copy, hashlib, importlib.util, json, subprocess, sys
from pathlib import Path

W = Path(sys.argv[1])
A = Path('/Users/sb/code/opensip-ai/opensip_arch')
M2 = 'docs/implementation/m2/'
V3 = M2 + 'project-registry-owner-selection-v3/'
RECORD, SUBJECT = V3 + 'successor.json', M2 + 'project-registry-owner-selection-v3-subject.json'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def pin_bytes(path, b):
    return {'path': path, 'bytes': len(b), 'sha256': sha(b)}


def pin(p):
    return pin_bytes(p, (A / p).read_bytes())


tool_raw = (W / 'tools/verify_design.py').read_bytes()
main_tool = subprocess.run(['git', '-C', str(W), 'show', 'HEAD:tools/verify_design.py'], check=True,
                           capture_output=True).stdout
assert tool_raw == main_tool


def load(served):
    m = importlib.util.module_from_spec(importlib.util.spec_from_loader('vd', loader=None))
    exec(compile(tool_raw, str(W / 'tools/verify_design.py'), 'exec'), m.__dict__)
    real = m.pinned_bytes

    def pinned_bytes(root, row):
        if isinstance(row, dict) and (row.get('path'), row.get('sha256')) in served:
            data = served[(row['path'], row['sha256'])]
            assert sha(data) == row['sha256'] and len(data) == row['bytes']
            return data
        return real(root, row)
    m.pinned_bytes = pinned_bytes
    return m


def binding(record_pin, subject_pin, tag, superseded, served, omit_list=False):
    review = {'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [], 'subjectManifestSha256': subject_pin['sha256']}
    if not omit_list:
        review['supersededPassages'] = superseded
    rraw = json.dumps(review).encode()
    rpin = pin_bytes('SCRATCH-%s/review.json' % tag, rraw)
    araw = json.dumps({'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [],
                       'subjectManifest': subject_pin, 'independentReview': rpin,
                       'acceptedSuccessor': record_pin}).encode()
    apin = pin_bytes('SCRATCH-%s/assent.json' % tag, araw)
    served[(rpin['path'], rpin['sha256'])] = rraw
    served[(apin['path'], apin['sha256'])] = araw
    return {'record': record_pin, 'subjectManifest': subject_pin, 'review': rpin, 'assent': apin}


def run(m, lock, implementation=None):
    try:
        return 'PASS', m.verify(A, lock, implementation)
    except m.DesignError as exc:
        return 'REFUSED: ' + str(exc), None


out = {'worktreeHead': subprocess.run(['git', '-C', str(W), 'rev-parse', 'HEAD'], check=True,
                                      capture_output=True, text=True).stdout.strip(),
       'tool': pin_bytes('tools/verify_design.py@HEAD', tool_raw)}
head_lock = json.loads(subprocess.run(['git', '-C', str(W), 'show', 'HEAD:design-lock.json'], check=True,
                                      capture_output=True).stdout)
assert json.loads((W / 'design-lock.json').read_bytes()) == head_lock

record_pin, subject_pin = pin(RECORD), pin(SUBJECT)
record = json.loads((A / RECORD).read_bytes())
superseded = [e['supersedes'] for e in record['passageSupersessions']]

served = {}
m = load(served)
st, base = run(m, head_lock, W)
assert st == 'PASS', st
staged = copy.deepcopy(head_lock)
staged['contractSuccessors'].append(binding(record_pin, subject_pin, 'REGV3', superseded, served))
(W / 'design-lock.json').write_text(json.dumps(staged, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
staged = m.decode((W / 'design-lock.json').read_bytes())
st, res = run(m, staged, W)
st_noimpl, _ = run(m, staged)
mine = res['contractSuccessors'][-1] if res else None
out['base'] = {'status': 'PASS', 'contractSuccessors': len(base['contractSuccessors']),
               'contractPassageSupersessions': base['contractPassageSupersessions']}
out['withV3r2'] = {'status': st, 'statusWithoutImplementation': st_noimpl}
if res:
    out['withV3r2'].update({'contractSuccessors': len(res['contractSuccessors']),
                            'contractPassageSupersessions': res['contractPassageSupersessions'],
                            'selected': mine['selected'], 'inputs': [r['path'] for r in mine['inputs']],
                            'passageOverrides': [o['selector']['line'] for o in mine['passageOverrides']],
                            'passageSupersessions': [s['selector']['line'] for s in mine['passageSupersessions']]})
    for k in ('inventorySuccessors', 'selectedInventory', 'inventoryPassageInheritance',
              'inventoryPassageSupersessions', 'generationSources', 'admissionSources', 'inputsVerified'):
        assert res.get(k) == base.get(k), k
    out['withV3r2']['unchangedBesidesContractChain'] = True

# Refusal probes, each on head's lock plus one entry.
refusals = {}
lock = copy.deepcopy(head_lock)
lock['contractSuccessors'].append(binding(record_pin, subject_pin, 'REGV3-NOLIST', superseded, served, omit_list=True))
refusals['reviewWithoutSupersededPassages'] = run(m, lock)[0]
lock = copy.deepcopy(head_lock)
lock['contractSuccessors'].append(binding(record_pin, subject_pin, 'REGV3-WRONGLIST', [], served))
refusals['reviewWithEmptyList'] = run(m, lock)[0]
# r1, as CODEX2 reviewed it: its exact bytes, served at their original paths.
r1 = {}
snap = A / V3 / 'r1-snapshot'
for name, path in (('README.md', V3 + 'README.md'), ('successor.json', RECORD),
                   ('project-registry-owner-selection-v3-subject.json', SUBJECT)):
    raw = (snap / name).read_bytes()
    r1[name] = pin_bytes(path, raw)
    served[(path, sha(raw))] = raw
assert r1['project-registry-owner-selection-v3-subject.json']['sha256'].startswith('0bd640d3')
lock = copy.deepcopy(head_lock)
lock['contractSuccessors'].append(binding(r1['successor.json'], r1['project-registry-owner-selection-v3-subject.json'],
                                          'REGV3-R1', [], served, omit_list=True))
refusals['r1RawOverrideOfREG9'] = run(m, lock)[0]
out['refusals'] = refusals
expected = {'reviewWithoutSupersededPassages': 'REFUSED: contract passage supersession is not listed by its review',
            'reviewWithEmptyList': 'REFUSED: contract review superseded passages differ from the record',
            'r1RawOverrideOfREG9': 'REFUSED: conflicting contract passage overrides'}
out['refusalsAsExpected'] = refusals == expected
print(json.dumps(out, indent=1))
