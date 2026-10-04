"""Local binding check for CRC-2, in a throwaway detached worktree of product main.

Usage: verify_scratch.py WORKTREE [--out PATH]

Run it with python3 -I -B at nice -n 19, and with a private 0700 TMPDIR under
$(getconf DARWIN_USER_TEMP_DIR). It is Python only and runs no cargo. Never run it in the main
product checkout: it rewrites the worktree's design-lock.json.

The worktree's own tools/verify_design.py is loaded unchanged (it must equal HEAD's bytes).
SCRATCH-CRC2 review and assent pins are served from memory by an overlay of pinned_bytes, as REG
v3's verify_reg_v3_r2.py, F8c's and SD-7's checks do; nothing is written to the architecture
repository. The scratch review carries supersededPassages equal to the record's supersedes list.

It reports:
- the baseline: the literal CLI on HEAD's lock, and the overlay run, both PASS;
- CRC-2 appended: PASS with the worktree as implementation and without it; one more contract
  successor and two more contract passage supersessions; everything else equal to the baseline;
- refusals, each on HEAD's lock plus one or two entries:
  * the review omits supersededPassages;
  * the review lists [];
  * CRC-2 with IE:285 and IE:1377 as raw overrides instead of supersessions;
  * after CRC-2, a probe that supersedes CRC-1's IE:285 again (no longer the current meaning);
  * after CRC-2, a probe that overrides one of CRC-2's identity-schema pointers again;
- the literal CLI on the appended lock, which stops at the SCRATCH placeholder (fail closed).
"""
import copy, hashlib, importlib.util, json, os, subprocess, sys
from pathlib import Path

args = list(sys.argv[1:])
out_path = None
if '--out' in args:
    i = args.index('--out')
    out_path = Path(args[i + 1])
    del args[i:i + 2]
W = Path(args[0])
A = Path('/Users/sb/code/opensip-ai/opensip_arch')
M = 'docs/implementation/m3/snapshot-plan-c/'
RECORD, SUBJECT = M + 'crc-2/successor.json', M + 'crc-2-subject.json'
assert W.resolve() != Path('/Users/sb/code/opensip-ai/opensip').resolve(), 'not in the main checkout'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def pin_bytes(path, b):
    return {'path': path, 'bytes': len(b), 'sha256': sha(b)}


def pin(p):
    return pin_bytes(p, (A / p).read_bytes())


def git(*a):
    return subprocess.run(['git', '-C', str(W), *a], check=True, capture_output=True).stdout


tool_raw = (W / 'tools/verify_design.py').read_bytes()
assert tool_raw == git('show', 'HEAD:tools/verify_design.py')
head_lock_raw = git('show', 'HEAD:design-lock.json')
head_lock = json.loads(head_lock_raw)
assert json.loads((W / 'design-lock.json').read_bytes()) == head_lock, 'worktree lock already edited'


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


served = {}


def serve(path, raw):
    served[(path, sha(raw))] = raw
    return pin_bytes(path, raw)


def binding(record_pin, subject_pin, tag, superseded, omit_list=False):
    review = {'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [], 'subjectManifestSha256': subject_pin['sha256']}
    if not omit_list:
        review['supersededPassages'] = superseded
    rpin = serve('SCRATCH-%s/review.json' % tag, json.dumps(review).encode())
    apin = serve('SCRATCH-%s/assent.json' % tag, json.dumps(
        {'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [],
         'subjectManifest': subject_pin, 'independentReview': rpin, 'acceptedSuccessor': record_pin}).encode())
    return {'record': record_pin, 'subjectManifest': subject_pin, 'review': rpin, 'assent': apin}


def probe_unit(tag, record_body, candidates):
    """A synthetic unit whose record, subject and candidates are all served from memory."""
    rec_pin = serve('SCRATCH-%s/successor.json' % tag, json.dumps(dict(record_body, candidates=candidates)).encode())
    subj_pin = serve('SCRATCH-%s/subject.json' % tag, json.dumps(
        {'schemaVersion': 1, 'files': sorted(candidates + [rec_pin], key=lambda r: r['path'])}).encode())
    return rec_pin, subj_pin


def run(m, lock, implementation=None):
    try:
        return 'PASS', m.verify(A, lock, implementation)
    except m.DesignError as exc:
        return 'REFUSED: ' + str(exc), None


def cli(lock_path=None):
    cmd = [sys.executable, '-I', '-B', 'tools/verify_design.py', '--architecture', str(A)]
    if lock_path:
        cmd += ['--lock', str(lock_path)]
    r = subprocess.run(cmd, cwd=W, capture_output=True, text=True)
    if r.returncode == 0:
        res = json.loads(r.stdout)
        return {'status': 'PASS', 'contractSuccessors': len(res['contractSuccessors']),
                'contractPassageSupersessions': res['contractPassageSupersessions']}
    return {'status': 'FAILED', 'stderr': r.stderr.strip()}


out = {'worktreeHead': git('rev-parse', 'HEAD').decode().strip(),
       'tmpdir': os.environ.get('TMPDIR'),
       'tool': pin_bytes('tools/verify_design.py@HEAD', tool_raw),
       'headLock': pin_bytes('design-lock.json@HEAD', head_lock_raw)}
record_pin, subject_pin = pin(RECORD), pin(SUBJECT)
record = json.loads((A / RECORD).read_bytes())
superseded = [e['supersedes'] for e in record['passageSupersessions']]
out['crc2'] = {'record': record_pin, 'subject': subject_pin, 'supersededPassages': superseded}

m = load(served)
out['baselineCli'] = cli()
st, base = run(m, head_lock, W)
assert st == 'PASS' and out['baselineCli']['status'] == 'PASS', (st, out['baselineCli'])
out['baseline'] = {'status': st, 'contractSuccessors': len(base['contractSuccessors']),
                   'contractPassageSupersessions': base['contractPassageSupersessions']}

staged = copy.deepcopy(head_lock)
staged['contractSuccessors'].append(binding(record_pin, subject_pin, 'CRC2', superseded))
(W / 'design-lock.json').write_text(json.dumps(staged, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
staged = m.decode((W / 'design-lock.json').read_bytes())
st, res = run(m, staged, W)
st_noimpl, res_noimpl = run(m, staged)
out['withCrc2'] = {'status': st, 'statusWithoutImplementation': st_noimpl}
assert st == 'PASS' and st_noimpl == 'PASS', (st, st_noimpl)
mine = res['contractSuccessors'][-1]
out['withCrc2'].update({
    'contractSuccessors': len(res['contractSuccessors']),
    'contractPassageSupersessions': res['contractPassageSupersessions'],
    'selected': mine['selected'], 'inputs': [r['path'] for r in mine['inputs']],
    'passageOverrides': [(o['parent']['path'], o['selector']) for o in mine['passageOverrides']],
    'passageSupersessions': [(s['parent']['path'], s['selector']) for s in mine['passageSupersessions']]})
assert len(res['contractSuccessors']) == len(base['contractSuccessors']) + 1
assert res['contractPassageSupersessions'] == base['contractPassageSupersessions'] + 2
for k in ('inventorySuccessors', 'selectedInventory', 'inventoryPassageInheritance',
          'inventoryPassageSupersessions', 'generationSources', 'admissionSources', 'inputsVerified'):
    assert res.get(k) == base.get(k), k
out['withCrc2']['unchangedBesidesContractChain'] = True
out['appendedCli'] = cli()

# Refusal probes, each on HEAD's lock.
refusals = {}
lock = copy.deepcopy(head_lock)
lock['contractSuccessors'].append(binding(record_pin, subject_pin, 'CRC2-NOLIST', superseded, omit_list=True))
refusals['reviewWithoutSupersededPassages'] = run(m, lock)[0]
lock = copy.deepcopy(head_lock)
lock['contractSuccessors'].append(binding(record_pin, subject_pin, 'CRC2-EMPTY', []))
refusals['reviewWithEmptyList'] = run(m, lock)[0]

# CRC-2 with its two IE entries as raw overrides: before is the raw parent line.
ie_parent = record['passageSupersessions'][0]['parent']
ie_lines = (A / ie_parent['path']).read_text(encoding='utf-8').splitlines()
raw_overrides = [{'parent': s['parent'], 'selector': s['selector'], 'before': ie_lines[s['selector']['line'] - 1],
                  'after': s['after']} for s in record['passageSupersessions']]
body = {k: v for k, v in record.items() if k not in ('candidates', 'passageSupersessions')}
body['passageOverrides'] = raw_overrides + record['passageOverrides']
note = serve('SCRATCH-CRC2-RAW/note.md', b'raw-override probe\n')
rp, sp = probe_unit('CRC2-RAW', body, [note])
lock = copy.deepcopy(head_lock)
lock['contractSuccessors'].append(binding(rp, sp, 'CRC2-RAW', [], omit_list=True))
refusals['rawOverridesOfCrc1Lines'] = run(m, lock)[0]

# After CRC-2: supersede CRC-1's IE:285 again.
s0 = record['passageSupersessions'][0]
note = serve('SCRATCH-DOUBLE/note.md', b'double supersession probe\n')
body = {'schemaVersion': 1, 'standing': 'probe', 'parents': [s0['parent']], 'passageOverrides': [],
        'passageSupersessions': [dict(s0, after=s0['after'] + ' (probe)')]}
rp, sp = probe_unit('DOUBLE', body, [note])
lock = copy.deepcopy(staged)
lock['contractSuccessors'].append(binding(rp, sp, 'DOUBLE', [s0['supersedes']]))
refusals['secondSupersessionOfCrc1AfterCrc2'] = run(m, lock)[0]

# After CRC-2: override one of its identity-schema pointers again.
o0 = record['passageOverrides'][0]
note = serve('SCRATCH-AGAIN/note.md', b'second override probe\n')
body = {'schemaVersion': 1, 'standing': 'probe', 'parents': [o0['parent']],
        'passageOverrides': [dict(o0, after=o0['after'] + ' (probe)')]}
rp, sp = probe_unit('AGAIN', body, [note])
lock = copy.deepcopy(staged)
lock['contractSuccessors'].append(binding(rp, sp, 'AGAIN', [], omit_list=True))
refusals['secondOverrideOfCrc2Pointer'] = run(m, lock)[0]

expected = {
    'reviewWithoutSupersededPassages': 'REFUSED: contract passage supersession is not listed by its review',
    'reviewWithEmptyList': 'REFUSED: contract review superseded passages differ from the record',
    'rawOverridesOfCrc1Lines': 'REFUSED: conflicting contract passage overrides',
    'secondSupersessionOfCrc1AfterCrc2': 'REFUSED: double supersession: the named passage is not the current meaning',
    'secondOverrideOfCrc2Pointer': 'REFUSED: conflicting contract passage overrides',
}
out['refusals'] = refusals
out['refusalsAsExpected'] = refusals == expected
text = json.dumps(out, indent=1) + '\n'
if out_path:
    out_path.write_text(text, encoding='utf-8')
print(text, end='')
assert out['refusalsAsExpected'], refusals
