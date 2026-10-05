"""Local binding check for HSR-1, in a throwaway detached worktree of product main.

Usage: verify_scratch.py WORKTREE [--out PATH]

Run it with python3 -I -B at nice -n 19, and with a private 0700 TMPDIR under
$(getconf DARWIN_USER_TEMP_DIR). It is Python only and runs no cargo. Never run it in the main
product checkout: it rewrites the worktree's design-lock.json.

The worktree's own tools/verify_design.py is loaded unchanged (it must equal HEAD's bytes).
SCRATCH-HSR1 review and assent pins are served from memory by an overlay of pinned_bytes, as CRC-2's,
SD-7's and REG v3's checks do; nothing is written to the architecture repository. The scratch review
carries supersededPassages equal to the record's supersedes list.

It reports:
- the baseline: the literal CLI on HEAD's lock, and the overlay run, both PASS;
- HSR-1 appended: PASS with the worktree as implementation and without it; one more contract
  successor and one more contract passage supersession; everything else equal to the baseline;
- refusals, each on HEAD's lock plus one or two entries:
  * the review omits supersededPassages;
  * the review lists [];
  * HSR-1 with IE:214 as a raw override instead of a supersession;
  * after HSR-1, a probe that supersedes I1-L's IE:214 again (no longer the current meaning);
  * after HSR-1, a probe that overrides IE:808 (the table) again with other text;
  * after HSR-1, a probe that overrides the payload-registry law pointer again with other text;
- the extension route: after HSR-1, a probe that supersedes HSR-1's IE:808 override, adding one
  table row, binds (PASS);
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
M = 'docs/implementation/m3/syntax-e/hsr/'
RECORD, SUBJECT = M + 'hsr-1/successor.json', M + 'hsr-1-subject.json'
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
out['hsr1'] = {'record': record_pin, 'subject': subject_pin, 'supersededPassages': superseded}

m = load(served)
out['baselineCli'] = cli()
st, base = run(m, head_lock, W)
assert st == 'PASS' and out['baselineCli']['status'] == 'PASS', (st, out['baselineCli'])
out['baseline'] = {'status': st, 'contractSuccessors': len(base['contractSuccessors']),
                   'contractPassageSupersessions': base['contractPassageSupersessions'],
                   'generationSources': base['generationSources']['sourcesVerified'],
                   'admissionSources': base['admissionSources']['sourcesVerified'],
                   'admissionAliases': base['admissionSources']['aliasesVerified']}

staged = copy.deepcopy(head_lock)
staged['contractSuccessors'].append(binding(record_pin, subject_pin, 'HSR1', superseded))
(W / 'design-lock.json').write_text(json.dumps(staged, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
staged = m.decode((W / 'design-lock.json').read_bytes())
st, res = run(m, staged, W)
st_noimpl, res_noimpl = run(m, staged)
out['withHsr1'] = {'status': st, 'statusWithoutImplementation': st_noimpl}
assert st == 'PASS' and st_noimpl == 'PASS', (st, st_noimpl)
mine = res['contractSuccessors'][-1]
out['withHsr1'].update({
    'contractSuccessors': len(res['contractSuccessors']),
    'contractPassageSupersessions': res['contractPassageSupersessions'],
    'selected': mine['selected'], 'inputs': [r['path'] for r in mine['inputs']],
    'passageOverrides': [(o['parent']['path'], o['selector']) for o in mine['passageOverrides']],
    'passageSupersessions': [(s['parent']['path'], s['selector']) for s in mine['passageSupersessions']]})
assert len(res['contractSuccessors']) == len(base['contractSuccessors']) + 1
assert res['contractPassageSupersessions'] == base['contractPassageSupersessions'] + 1
for k in ('inventorySuccessors', 'selectedInventory', 'inventoryPassageInheritance',
          'inventoryPassageSupersessions', 'generationSources', 'admissionSources', 'inputsVerified'):
    assert res.get(k) == base.get(k), k
out['withHsr1']['unchangedBesidesContractChain'] = True
out['appendedCli'] = cli()

# Refusal probes, each on HEAD's lock or on the staged lock.
refusals = {}
lock = copy.deepcopy(head_lock)
lock['contractSuccessors'].append(binding(record_pin, subject_pin, 'HSR1-NOLIST', superseded, omit_list=True))
refusals['reviewWithoutSupersededPassages'] = run(m, lock)[0]
lock = copy.deepcopy(head_lock)
lock['contractSuccessors'].append(binding(record_pin, subject_pin, 'HSR1-EMPTY', []))
refusals['reviewWithEmptyList'] = run(m, lock)[0]

# HSR-1 with IE:214 as a raw override: before is the raw parent line.
s0 = record['passageSupersessions'][0]
ie_lines = (A / s0['parent']['path']).read_text(encoding='utf-8').splitlines()
raw_override = {'parent': s0['parent'], 'selector': s0['selector'], 'before': ie_lines[s0['selector']['line'] - 1],
                'after': s0['after']}
body = {k: v for k, v in record.items() if k not in ('candidates', 'passageSupersessions')}
body['passageOverrides'] = [raw_override] + record['passageOverrides']
note = serve('SCRATCH-HSR1-RAW/note.md', b'raw-override probe\n')
rp, sp = probe_unit('HSR1-RAW', body, [note])
lock = copy.deepcopy(head_lock)
lock['contractSuccessors'].append(binding(rp, sp, 'HSR1-RAW', [], omit_list=True))
refusals['rawOverrideOfI1lLine214'] = run(m, lock)[0]

# After HSR-1: supersede I1-L's IE:214 again.
note = serve('SCRATCH-DOUBLE/note.md', b'double supersession probe\n')
body = {'schemaVersion': 1, 'standing': 'probe', 'parents': [s0['parent']], 'passageOverrides': [],
        'passageSupersessions': [dict(s0, after=s0['after'] + ' (probe)')]}
rp, sp = probe_unit('DOUBLE', body, [note])
lock = copy.deepcopy(staged)
lock['contractSuccessors'].append(binding(rp, sp, 'DOUBLE', [s0['supersedes']]))
refusals['secondSupersessionOfI1lAfterHsr1'] = run(m, lock)[0]

# After HSR-1: override the table line (IE:808) again with other text.
by_sel = {json.dumps(o['selector'], sort_keys=True): o for o in record['passageOverrides']}
o808 = by_sel[json.dumps({'line': 808}, sort_keys=True)]
note = serve('SCRATCH-AGAIN/note.md', b'second override probe\n')
body = {'schemaVersion': 1, 'standing': 'probe', 'parents': [o808['parent']],
        'passageOverrides': [dict(o808, after=o808['after'] + '\n\n(probe row)')]}
rp, sp = probe_unit('AGAIN', body, [note])
lock = copy.deepcopy(staged)
lock['contractSuccessors'].append(binding(rp, sp, 'AGAIN', [], omit_list=True))
refusals['secondOverrideOfTheTableLine'] = run(m, lock)[0]

# After HSR-1: override the payload-registry law pointer again with other text.
olaw = by_sel[json.dumps({'jsonPointer': '/x-opensip-payload-registry/law/payloadSchemaDigest'}, sort_keys=True)]
note = serve('SCRATCH-LAW/note.md', b'second pointer override probe\n')
body = {'schemaVersion': 1, 'standing': 'probe', 'parents': [olaw['parent']],
        'passageOverrides': [dict(olaw, after=olaw['after'] + ' (probe)')]}
rp, sp = probe_unit('LAW', body, [note])
lock = copy.deepcopy(staged)
lock['contractSuccessors'].append(binding(rp, sp, 'LAW', [], omit_list=True))
refusals['secondOverrideOfThePayloadLawPointer'] = run(m, lock)[0]

# The extension route: after HSR-1, a later successor supersedes HSR-1's IE:808 override and adds one
# row. The row here is synthetic; a real one names a retired digest and its accepted copy.
row_h2 = [l for l in o808['after'].split('\n') if l.startswith('| H2 |')][0]
row_h3 = ('| H3 | `native/native-evidence.schemas.v2.json` | `urn:opensip:product-v1:native:evidence-schemas:v2` | `'
          + '0' * 64 + '` | 1 | `SCRATCH-EXTEND/probe-copy.json` | PROBE |')
extended = o808['after'].replace(row_h2, row_h2 + '\n' + row_h3)
assert extended != o808['after']
target = {'record': record_pin, 'parent': o808['parent'], 'selector': o808['selector']}
note = serve('SCRATCH-EXTEND/note.md', b'extension probe\n')
body = {'schemaVersion': 1, 'standing': 'probe', 'parents': [o808['parent']], 'passageOverrides': [],
        'passageSupersessions': [{'parent': o808['parent'], 'selector': o808['selector'], 'before': o808['after'],
                                  'after': extended, 'supersedes': target}]}
rp, sp = probe_unit('EXTEND', body, [note])
lock = copy.deepcopy(staged)
lock['contractSuccessors'].append(binding(rp, sp, 'EXTEND', [target]))
st_ext, res_ext = run(m, lock)
out['extensionRoute'] = {'status': st_ext,
                         'contractSuccessors': len(res_ext['contractSuccessors']) if res_ext else None,
                         'contractPassageSupersessions': res_ext['contractPassageSupersessions'] if res_ext else None}
assert st_ext == 'PASS', st_ext

expected = {
    'reviewWithoutSupersededPassages': 'REFUSED: contract passage supersession is not listed by its review',
    'reviewWithEmptyList': 'REFUSED: contract review superseded passages differ from the record',
    'rawOverrideOfI1lLine214': 'REFUSED: conflicting contract passage overrides',
    'secondSupersessionOfI1lAfterHsr1': 'REFUSED: double supersession: the named passage is not the current meaning',
    'secondOverrideOfTheTableLine': 'REFUSED: conflicting contract passage overrides',
    'secondOverrideOfThePayloadLawPointer': 'REFUSED: conflicting contract passage overrides',
}
out['refusals'] = refusals
out['refusalsAsExpected'] = refusals == expected
text = json.dumps(out, indent=1) + '\n'
if out_path:
    out_path.write_text(text, encoding='utf-8')
print(text, end='')
assert out['refusalsAsExpected'], refusals
