"""Local binding check for ENUM-1 and SD-8, alone and together, in a throwaway detached worktree of product main.

Usage: verify_scratch.py WORKTREE [--out PATH]

Run it with python3 -I -B at nice -n 19, and with a private 0700 TMPDIR under
$(getconf DARWIN_USER_TEMP_DIR). It is Python only and runs no cargo. Never run it in the main
product checkout: it rewrites the worktree's design-lock.json.

The worktree's own tools/verify_design.py is loaded unchanged (it must equal HEAD's bytes, and HEAD
must be 1799d3d). SCRATCH review and assent pins are served from memory by an overlay of
pinned_bytes, as CRC-2's, SD-7's and REG v3's checks do; nothing is written to the architecture
repository. ENUM-1's scratch review lists supersededPassages as []; SD-8's lists its record's
supersedes list.

It reports:
- the baseline: the literal CLI on HEAD's lock, and the overlay run, both PASS;
- ENUM-1 alone, SD-8 alone, and both in each order: PASS with the worktree as implementation and
  without it; the contract successor and contract passage supersession counts move by exactly the
  units' own; everything else equals the baseline;
- refusals and two positive probes, each on HEAD's lock plus the named entries:
  * ENUM-1 whose review lists SD-8's superseded passage;
  * after ENUM-1, a second plain override of ENC:53;
  * ENUM-1 with ENC:53's `before` altered;
  * ENC:53 posed as a supersession naming SD-7's record, which publishes no ENC passage;
  * after ENUM-1, a VD2 supersession of ENUM-1's ENC:53 (positive: the passage stays editable);
  * SD-8 whose review omits supersededPassages, and one that lists [];
  * SD-8 as a raw override of NE:3540;
  * SD-8 superseding SD-5's override, which SD-7 already superseded;
  * after SD-8, a second supersession of SD-7's NE:3540;
  * after SD-8, a VD2 supersession of SD-8's NE:3540 (positive: the chain stays linear);
- the literal CLI on the lock with both units appended, which stops at the SCRATCH placeholder.
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
HEAD = '1799d3d4e8107611636f6dda2d27b2586e4f550f'
UNITS = {
    'ENUM-1': ('docs/implementation/m3/snapshot-plan-c/enum-1/successor.json',
               'docs/implementation/m3/snapshot-plan-c/enum-1-subject.json'),
    'SD-8': ('docs/implementation/m3/supervisor-d/sd-8/successor.json',
             'docs/implementation/m3/supervisor-d/sd-8-subject.json'),
}
assert W.resolve() != Path('/Users/sb/code/opensip-ai/opensip').resolve(), 'not in the main checkout'


def sha(b):
    return hashlib.sha256(b).hexdigest()


def pin_bytes(path, b):
    return {'path': path, 'bytes': len(b), 'sha256': sha(b)}


def pin(p):
    return pin_bytes(p, (A / p).read_bytes())


def git(*a):
    return subprocess.run(['git', '-C', str(W), *a], check=True, capture_output=True).stdout


assert git('rev-parse', 'HEAD').decode().strip() == HEAD
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


def binding(record_pin, subject_pin, tag, superseded, omit_list=False):
    review = {'verdict': 'ACCEPT-DESIGN-UNIT', 'requiredFindings': [], 'subjectManifestSha256': subject_pin['sha256']}
    if not omit_list:
        review['supersededPassages'] = superseded
    rpin = serve('SCRATCH-%s/review.json' % tag, json.dumps(review).encode())
    apin = serve('SCRATCH-%s/assent.json' % tag, json.dumps(
        {'status': 'ACCEPTED-DESIGN-UNIT', 'rootSubstantiveAssent': True, 'requiredUnitFindings': [],
         'subjectManifest': subject_pin, 'independentReview': rpin, 'acceptedSuccessor': record_pin}).encode())
    return {'record': record_pin, 'subjectManifest': subject_pin, 'review': rpin, 'assent': apin}


def probe_unit(tag, body):
    """A synthetic unit whose record, subject and one candidate are all served from memory."""
    note = serve('SCRATCH-%s/note.md' % tag, ('%s probe\n' % tag).encode())
    rec_pin = serve('SCRATCH-%s/successor.json' % tag, json.dumps(dict(body, candidates=[note])).encode())
    subj_pin = serve('SCRATCH-%s/subject.json' % tag, json.dumps(
        {'schemaVersion': 1, 'files': sorted([note, rec_pin], key=lambda r: r['path'])}).encode())
    return rec_pin, subj_pin


def run(m, lock, implementation=None):
    try:
        return 'PASS', m.verify(A, lock, implementation)
    except m.DesignError as exc:
        return 'REFUSED: ' + str(exc), None


def cli():
    r = subprocess.run([sys.executable, '-I', '-B', 'tools/verify_design.py', '--architecture', str(A)],
                       cwd=W, capture_output=True, text=True)
    if r.returncode == 0:
        res = json.loads(r.stdout)
        return {'status': 'PASS', 'contractSuccessors': len(res['contractSuccessors']),
                'contractPassageSupersessions': res['contractPassageSupersessions']}
    return {'status': 'FAILED', 'stderr': r.stderr.strip()}


m = load()
out = {'worktreeHead': HEAD, 'tmpdir': os.environ.get('TMPDIR'),
       'tool': pin_bytes('tools/verify_design.py@HEAD', tool_raw),
       'headLock': pin_bytes('design-lock.json@HEAD', head_lock_raw), 'units': {}}
bindings, records = {}, {}
for name, (rec_path, subj_path) in UNITS.items():
    rp, sp = pin(rec_path), pin(subj_path)
    records[name] = json.loads((A / rec_path).read_bytes())
    superseded = [e['supersedes'] for e in records[name]['passageSupersessions']]
    bindings[name] = binding(rp, sp, name, superseded)
    out['units'][name] = {'record': rp, 'subject': sp, 'supersededPassages': superseded}

out['baselineCli'] = cli()
st, base = run(m, head_lock, W)
assert st == 'PASS' and out['baselineCli']['status'] == 'PASS', (st, out['baselineCli'])
out['baseline'] = {'status': st, 'contractSuccessors': len(base['contractSuccessors']),
                   'contractPassageSupersessions': base['contractPassageSupersessions']}
OWN_LINKS = {'ENUM-1': 0, 'SD-8': 1}
UNCHANGED = ('inventorySuccessors', 'selectedInventory', 'inventoryPassageInheritance', 'inventoryPassageSupersessions',
             'generationSources', 'admissionSources', 'inputsVerified')


def staged(names):
    lock = copy.deepcopy(head_lock)
    lock['contractSuccessors'] += [bindings[n] for n in names]
    (W / 'design-lock.json').write_text(json.dumps(lock, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    return m.decode((W / 'design-lock.json').read_bytes())


out['configurations'] = {}
for names in (['ENUM-1'], ['SD-8'], ['ENUM-1', 'SD-8'], ['SD-8', 'ENUM-1']):
    lock = staged(names)
    st, res = run(m, lock, W)
    st_noimpl, _ = run(m, lock)
    assert st == 'PASS' and st_noimpl == 'PASS', (names, st, st_noimpl)
    assert len(res['contractSuccessors']) == len(base['contractSuccessors']) + len(names)
    assert res['contractPassageSupersessions'] == base['contractPassageSupersessions'] + sum(OWN_LINKS[n] for n in names)
    for k in UNCHANGED:
        assert res.get(k) == base.get(k), (names, k)
    tail = res['contractSuccessors'][-len(names):]
    out['configurations'][' then '.join(names)] = {
        'status': st, 'statusWithoutImplementation': st_noimpl,
        'contractSuccessors': len(res['contractSuccessors']),
        'contractPassageSupersessions': res['contractPassageSupersessions'],
        'selected': [t['selected'] for t in tail],
        'passageOverrides': [len(t['passageOverrides']) for t in tail],
        'passageSupersessions': [len(t['passageSupersessions']) for t in tail],
        'unchangedBesidesContractChain': True}
both = staged(['ENUM-1', 'SD-8'])
out['appendedCli'] = cli()

# Probes.
probes = {}
enum1, sd8 = records['ENUM-1'], records['SD-8']
e53 = enum1['passageOverrides'][0]
assert e53['selector'] == {'line': 53}
s3540 = sd8['passageSupersessions'][0]
sd8_list = [s3540['supersedes']]
lock_enum1 = copy.deepcopy(head_lock)
lock_enum1['contractSuccessors'].append(bindings['ENUM-1'])
lock_sd8 = copy.deepcopy(head_lock)
lock_sd8['contractSuccessors'].append(bindings['SD-8'])


def with_probe(base_lock, tag, body, superseded, omit_list=False):
    rp, sp = probe_unit(tag, body)
    lock = copy.deepcopy(base_lock)
    lock['contractSuccessors'].append(binding(rp, sp, tag, superseded, omit_list))
    return run(m, lock)[0]


def with_unit(name, tag, superseded, omit_list=False):
    lock = copy.deepcopy(head_lock)
    u = out['units'][name]
    lock['contractSuccessors'].append(binding(u['record'], u['subject'], tag, superseded, omit_list))
    return run(m, lock)[0]


probes['enum1ReviewListsForeignPassage'] = with_unit('ENUM-1', 'E-FOREIGN', sd8_list)
enc_lines = (A / e53['parent']['path']).read_text(encoding='utf-8').splitlines()
probes['enum1SecondOverrideOfEnc53'] = with_probe(lock_enum1, 'E-AGAIN', {
    'schemaVersion': 1, 'standing': 'probe', 'parents': [e53['parent']], 'passageSupersessions': [],
    'passageOverrides': [dict(e53, before=enc_lines[52], after=e53['after'] + ' (probe)')]}, [], omit_list=True)
body = {k: v for k, v in enum1.items() if k != 'candidates'}
body['passageOverrides'] = [dict(e53, before=e53['before'] + ' ')] + enum1['passageOverrides'][1:]
probes['enum1TamperedBefore'] = with_probe(head_lock, 'E-TAMPER', body, [], omit_list=True)
sd7_pin = s3540['supersedes']['record']
fake = {'record': sd7_pin, 'parent': e53['parent'], 'selector': e53['selector']}
probes['enc53SupersessionNamingSd7'] = with_probe(head_lock, 'E-UNPUB', {
    'schemaVersion': 1, 'standing': 'probe', 'parents': [e53['parent']], 'passageOverrides': [],
    'passageSupersessions': [dict(e53, supersedes=fake)]}, [fake])
link = {'record': out['units']['ENUM-1']['record'], 'parent': e53['parent'], 'selector': e53['selector']}
probes['positiveSupersessionOfEnum1Enc53'] = with_probe(lock_enum1, 'E-NEXT', {
    'schemaVersion': 1, 'standing': 'probe', 'parents': [e53['parent']], 'passageOverrides': [],
    'passageSupersessions': [{'parent': e53['parent'], 'selector': e53['selector'], 'before': e53['after'],
                              'after': e53['after'] + ' (probe)', 'supersedes': link}]}, [link])

probes['sd8ReviewWithoutList'] = with_unit('SD-8', 'S-NOLIST', [], omit_list=True)
probes['sd8ReviewWithEmptyList'] = with_unit('SD-8', 'S-EMPTY', [])
ne_lines = (A / s3540['parent']['path']).read_text(encoding='utf-8').splitlines()
probes['sd8AsRawOverride'] = with_probe(head_lock, 'S-RAW', {
    'schemaVersion': 1, 'standing': 'probe', 'parents': [s3540['parent']], 'passageSupersessions': [],
    'passageOverrides': [{'parent': s3540['parent'], 'selector': s3540['selector'], 'before': ne_lines[3539],
                          'after': s3540['after']}]}, [], omit_list=True)
sd7_record = json.loads((A / sd7_pin['path']).read_bytes())
sd5_link = sd7_record['passageSupersessions'][0]['supersedes']
sd5_record = json.loads((A / sd5_link['record']['path']).read_bytes())
sd5_entry = [e for e in sd5_record['passageOverrides'] if e['selector'] == {'line': 3540}][0]
stale = {'record': sd5_link['record'], 'parent': s3540['parent'], 'selector': s3540['selector']}
probes['sd8SupersedingSd5'] = with_probe(head_lock, 'S-STALE', {
    'schemaVersion': 1, 'standing': 'probe', 'parents': [s3540['parent']], 'passageOverrides': [],
    'passageSupersessions': [dict(s3540, before=sd5_entry['after'], supersedes=stale)]}, [stale])
probes['secondSupersessionOfSd7AfterSd8'] = with_probe(lock_sd8, 'S-DOUBLE', {
    'schemaVersion': 1, 'standing': 'probe', 'parents': [s3540['parent']], 'passageOverrides': [],
    'passageSupersessions': [dict(s3540, after=s3540['after'] + ' (probe)')]}, sd8_list)
link8 = {'record': out['units']['SD-8']['record'], 'parent': s3540['parent'], 'selector': s3540['selector']}
probes['positiveSupersessionOfSd8'] = with_probe(lock_sd8, 'S-NEXT', {
    'schemaVersion': 1, 'standing': 'probe', 'parents': [s3540['parent']], 'passageOverrides': [],
    'passageSupersessions': [{'parent': s3540['parent'], 'selector': s3540['selector'], 'before': s3540['after'],
                              'after': s3540['after'] + ' (probe)', 'supersedes': link8}]}, [link8])

expected = {
    'enum1ReviewListsForeignPassage': 'REFUSED: contract review superseded passages differ from the record',
    'enum1SecondOverrideOfEnc53': 'REFUSED: conflicting contract passage overrides',
    'enum1TamperedBefore': 'REFUSED: passage override before text differs from accepted parent',
    'enc53SupersessionNamingSd7': 'REFUSED: superseded passage is not in the named record',
    'positiveSupersessionOfEnum1Enc53': 'PASS',
    'sd8ReviewWithoutList': 'REFUSED: contract passage supersession is not listed by its review',
    'sd8ReviewWithEmptyList': 'REFUSED: contract review superseded passages differ from the record',
    'sd8AsRawOverride': 'REFUSED: conflicting contract passage overrides',
    'sd8SupersedingSd5': 'REFUSED: double supersession: the named passage is not the current meaning',
    'secondSupersessionOfSd7AfterSd8': 'REFUSED: double supersession: the named passage is not the current meaning',
    'positiveSupersessionOfSd8': 'PASS',
}
out['probes'] = probes
out['probesAsExpected'] = probes == expected
text = json.dumps(out, indent=1) + '\n'
if out_path:
    out_path.write_text(text, encoding='utf-8')
print(text, end='')
assert out['probesAsExpected'], {k: v for k, v in probes.items() if expected[k] != v}
