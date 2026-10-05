"""Local binding check for the S-OP-2 recording units, in a throwaway detached worktree of product main.

Usage: verify_scratch.py WORKTREE [--out PATH]

Run it with python3 -I -B at nice -n 19, and with a private 0700 TMPDIR under
$(getconf DARWIN_USER_TEMP_DIR). It is Python only and runs no cargo. Never run it in the main
product checkout: it rewrites the worktree's design-lock.json.

The worktree's own tools/verify_design.py is loaded unchanged (it must equal HEAD's bytes).
SCRATCH review and assent pins are served from memory by an overlay of pinned_bytes, as CRC-2's,
SD-8's and ENUM-1's checks did; nothing is written to the architecture repository. Both scratch
reviews carry "supersededPassages": [].

It reports:
- the baseline: the literal CLI on HEAD's lock, and the overlay run, both PASS;
- S-OP-2-R alone: REFUSED, because its parents (SDK4, DRC) are not selected (the finding);
- S-OP-2-P alone, and S-OP-2-P then S-OP-2-R: PASS with the worktree as implementation and
  without it; everything outside the contract chain equal to the baseline;
- refusal probes, each on HEAD's lock plus the named entries;
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
B = 'docs/implementation/m3/operability/s-op-2/'
P_RECORD, P_SUBJECT = B + 's-op-2-p/successor.json', B + 's-op-2-p-subject.json'
R_RECORD, R_SUBJECT = B + 's-op-2-r/successor.json', B + 's-op-2-r-subject.json'
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
served = {}


def load():
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


def serve(path, raw):
    served[(path, sha(raw))] = raw
    return pin_bytes(path, raw)


def binding(record_pin, subject_pin, tag, superseded=(), review_subject=None):
    review = {'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [],
              'subjectManifestSha256': (review_subject or subject_pin)['sha256'],
              'supersededPassages': list(superseded)}
    rpin = serve('SCRATCH-%s/review.json' % tag, json.dumps(review).encode())
    apin = serve('SCRATCH-%s/assent.json' % tag, json.dumps(
        {'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [],
         'subjectManifest': subject_pin, 'independentReview': rpin, 'acceptedSuccessor': record_pin}).encode())
    return {'record': record_pin, 'subjectManifest': subject_pin, 'review': rpin, 'assent': apin}


def probe_unit(tag, record_body, candidates, extra_members=()):
    """A synthetic unit whose record and subject are served from memory."""
    rec_pin = serve('SCRATCH-%s/successor.json' % tag, json.dumps(dict(record_body, candidates=candidates)).encode())
    subj_pin = serve('SCRATCH-%s/subject.json' % tag, json.dumps(
        {'schemaVersion': 1, 'files': sorted(list(candidates) + list(extra_members) + [rec_pin],
                                             key=lambda r: r['path'])}).encode())
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


def counts(res):
    return {'contractSuccessors': len(res['contractSuccessors']),
            'contractPassageSupersessions': res['contractPassageSupersessions']}


SAME = ('inventorySuccessors', 'selectedInventory', 'inventoryPassageInheritance',
        'inventoryPassageSupersessions', 'generationSources', 'admissionSources', 'inputsVerified')

out = {'worktreeHead': git('rev-parse', 'HEAD').decode().strip(), 'tmpdir': os.environ.get('TMPDIR'),
       'tool': pin_bytes('tools/verify_design.py@HEAD', tool_raw),
       'headLock': pin_bytes('design-lock.json@HEAD', head_lock_raw)}
p_record, p_subject, r_record, r_subject = pin(P_RECORD), pin(P_SUBJECT), pin(R_RECORD), pin(R_SUBJECT)
out['units'] = {'S-OP-2-P': {'record': p_record, 'subject': p_subject},
                'S-OP-2-R': {'record': r_record, 'subject': r_subject}}
P = binding(p_record, p_subject, 'SOP2P')
R = binding(r_record, r_subject, 'SOP2R')
m = load()

out['baselineCli'] = cli()
st, base = run(m, head_lock, W)
assert st == 'PASS' and out['baselineCli']['status'] == 'PASS', (st, out['baselineCli'])
out['baseline'] = dict(status=st, **counts(base))

configs = {}
for name, entries in (('S-OP-2-R alone', [R]), ('S-OP-2-P alone', [P]), ('S-OP-2-P then S-OP-2-R', [P, R])):
    lock = copy.deepcopy(head_lock)
    lock['contractSuccessors'].extend(entries)
    st, res = run(m, lock, W)
    st2, _ = run(m, lock)
    row = {'status': st, 'statusWithoutImplementation': st2}
    if res is not None:
        row.update(counts(res))
        row['unchangedBesidesContractChain'] = all(res.get(k) == base.get(k) for k in SAME)
        if name == 'S-OP-2-P then S-OP-2-R':
            p_res, r_res = res['contractSuccessors'][-2], res['contractSuccessors'][-1]
            row['S-OP-2-P'] = {'selected': p_res['selected'], 'inputs': [r['path'] for r in p_res['inputs']],
                               'passageOverrides': len(p_res['passageOverrides'])}
            row['S-OP-2-R'] = {'selected': r_res['selected'], 'inputs': [r['path'] for r in r_res['inputs']],
                               'passageOverrides': [(o['parent']['path'], o['selector']) for o in r_res['passageOverrides']]}
    configs[name] = row
out['configurations'] = configs
assert configs['S-OP-2-R alone']['status'] == 'REFUSED: contract parent is not an accepted base or selected inventory'
for name in ('S-OP-2-P alone', 'S-OP-2-P then S-OP-2-R'):
    assert configs[name]['status'] == 'PASS' and configs[name]['statusWithoutImplementation'] == 'PASS', name
    assert configs[name]['unchangedBesidesContractChain'], name
    assert configs[name]['contractPassageSupersessions'] == out['baseline']['contractPassageSupersessions']
assert configs['S-OP-2-P alone']['contractSuccessors'] == out['baseline']['contractSuccessors'] + 1
assert configs['S-OP-2-P then S-OP-2-R']['contractSuccessors'] == out['baseline']['contractSuccessors'] + 2

# The appended lock, written to the worktree, and the literal CLI on it (fails closed at SCRATCH).
staged = copy.deepcopy(head_lock)
staged['contractSuccessors'].extend([P, R])
(W / 'design-lock.json').write_text(json.dumps(staged, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
staged = m.decode((W / 'design-lock.json').read_bytes())
assert run(m, staged, W)[0] == 'PASS'
out['appendedCli'] = cli()

# Refusal probes.
record_r = json.loads((A / R_RECORD).read_bytes())
sdk4, drc = record_r['passageOverrides'][0], record_r['passageOverrides'][1]
note = serve('SCRATCH-NOTE/note.md', b'probe\n')
refusals = {}


def with_entries(*entries, base_lock=None):
    lock = copy.deepcopy(base_lock if base_lock is not None else head_lock)
    lock['contractSuccessors'].extend(entries)
    return run(m, lock)[0]


refusals['recordingAloneParentsUnselected'] = with_entries(R)
refusals['recordingReviewNamesSelectionSubject'] = with_entries(P, binding(r_record, r_subject, 'R-WRONG', review_subject=p_subject))
fake = {'record': p_record, 'parent': sdk4['parent'], 'selector': sdk4['selector']}
refusals['recordingReviewListsAPassage'] = with_entries(P, binding(r_record, r_subject, 'R-LIST', superseded=[fake]))
body = {'schemaVersion': 1, 'standing': 'probe', 'parents': [sdk4['parent']],
        'passageOverrides': [dict(sdk4, before=sdk4['before'] + ' ')]}
rp, sp = probe_unit('BEFORE', body, [note])
refusals['sdk4BeforeAltered'] = with_entries(P, binding(rp, sp, 'BEFORE'))
sdk4_lines = (A / sdk4['parent']['path']).read_text(encoding='utf-8').splitlines()
rule_line = next(i for i, text in enumerate(sdk4_lines, 1) if 'No unstructured host logs.' in text)
body = {'schemaVersion': 1, 'standing': 'probe', 'parents': [sdk4['parent']],
        'passageOverrides': [{'parent': sdk4['parent'], 'selector': {'line': rule_line},
                              'before': sdk4_lines[rule_line - 1], 'after': sdk4_lines[rule_line - 1] + ' probe'}]}
rp, sp = probe_unit('LINE', body, [note])
refusals['sdk4ByLineSelector'] = with_entries(P, binding(rp, sp, 'LINE'))
body = {'schemaVersion': 1, 'standing': 'probe', 'parents': [drc['parent']],
        'passageOverrides': [dict(drc, after=drc['after'] + ' (probe)')]}
rp, sp = probe_unit('AGAIN', body, [note])
refusals['secondOverrideOfDrc576AfterRecording'] = with_entries(binding(rp, sp, 'AGAIN'), base_lock=staged)
body = {'schemaVersion': 1, 'standing': 'probe', 'parents': [drc['parent']], 'passageOverrides': [],
        'passageSupersessions': [{'parent': drc['parent'], 'selector': drc['selector'], 'before': drc['after'],
                                  'after': drc['after'] + ' (probe)',
                                  'supersedes': {'record': r_record, 'parent': drc['parent'], 'selector': drc['selector']}}]}
rp, sp = probe_unit('VD2', body, [note])
refusals['vd2SupersessionOfDrc576AfterRecording'] = with_entries(
    binding(rp, sp, 'VD2', superseded=[{'record': r_record, 'parent': drc['parent'], 'selector': drc['selector']}]),
    base_lock=staged)
record_p = json.loads((A / P_RECORD).read_bytes())
body = {k: v for k, v in record_p.items() if k != 'candidates'}
rp, sp = probe_unit('SELECT-AGAIN', body, record_p['candidates'])
refusals['secondSelectionOfSdk4AndDrc'] = with_entries(P, binding(rp, sp, 'SELECT-AGAIN'))
subject_r = json.loads((A / R_SUBJECT).read_bytes())
short = serve('SCRATCH-SHORT/subject.json', json.dumps(
    {'schemaVersion': 1, 'files': [r for r in subject_r['files'] if not r['path'].endswith('PROPOSAL-r6.md')]}).encode())
refusals['recordingSubjectWithoutProposal'] = with_entries(P, binding(r_record, short, 'SHORT'))

expected = {
    'recordingAloneParentsUnselected': 'REFUSED: contract parent is not an accepted base or selected inventory',
    'recordingReviewNamesSelectionSubject': 'REFUSED: contract review names a different manifest',
    'recordingReviewListsAPassage': 'REFUSED: contract review superseded passages differ from the record',
    'sdk4BeforeAltered': 'REFUSED: passage override before text differs from accepted parent',
    'sdk4ByLineSelector': 'REFUSED: v4 JSON parent passages require JSON Pointer selectors',
    'secondOverrideOfDrc576AfterRecording': 'REFUSED: conflicting contract passage overrides',
    'vd2SupersessionOfDrc576AfterRecording': 'PASS',
    'secondSelectionOfSdk4AndDrc': 'REFUSED: contract candidate reuses an accepted path',
    'recordingSubjectWithoutProposal': 'REFUSED: contract candidates do not cover the reviewed subject',
}
out['refusals'] = refusals
out['refusalsAsExpected'] = refusals == expected
text = json.dumps(out, indent=1) + '\n'
if out_path:
    out_path.write_text(text, encoding='utf-8')
print(text, end='')
assert out['refusalsAsExpected'], {k: v for k, v in refusals.items() if expected.get(k) != v}
