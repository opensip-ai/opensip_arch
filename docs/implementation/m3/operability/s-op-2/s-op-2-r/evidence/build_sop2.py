"""Build the S-OP-2 recording (S-OP-2 r6 item 24) as two design units, with PASSAGES.md, both subject
manifests and the lead's two draft unit records.

Usage: build_sop2.py [--product PATH] [--rev REV] [--check]
- PATH is the product checkout (default /Users/sb/code/opensip-ai/opensip), read only. REV (default
  b7b87b7, product main) names the commit whose design-lock.json is read with read-only `git show`.
- Without --check every generated file is written. With --check nothing is written: each generated
  file is rebuilt in memory and compared with the bytes on disk.

Deterministic: two runs give identical bytes. Run with python3 -I -B at nice -n 19. It needs the
hand-written README.md and both evidence scripts to exist, because the record and the subject pin them.

Why two units (README, LD-R1). Item 24's two overrides name SDK4 and DRC as parents. Neither file is in
the selected design at REV: not in the source manifest, not in the application manifest, and not a
candidate of any bound contract successor. verify_design refuses a parent outside that set ("contract
parent is not an accepted base or selected inventory"), and a unit cannot override its own candidate.
So unit S-OP-2-P first selects the exact SDK4 and DRC bytes that the accepted D-369 application pins
(APP /rows/12/inheritedContract and /evidenceTargets/D.SDK/sources/0), with no override, as
control-source-v1 selected control-completion.schema.v3.json. Unit S-OP-2-R then pins S-OP-2 r6's
accepted bytes and makes item 24's two insertion-only overrides.

Generated:
- s-op-2-p/successor.json, ../s-op-2-p-subject.json, ../s-op-2-p-unit.json;
- s-op-2-r/PASSAGES.md, s-op-2-r/successor.json, ../s-op-2-r-subject.json, ../s-op-2-r-unit.json.
The unit records are not subject members.
"""
import hashlib, json, subprocess, sys
from pathlib import Path

A = Path(__file__).resolve().parents[7]
args = list(sys.argv[1:])


def opt(name, default):
    if name in args:
        i = args.index(name)
        value = args[i + 1]
        del args[i:i + 2]
        return value
    return default


W = Path(opt('--product', '/Users/sb/code/opensip-ai/opensip'))
REV = opt('--rev', 'b7b87b7')
CHECK = '--check' in args
B = 'docs/implementation/m3/operability/s-op-2/'
P = B + 's-op-2-p/'
R = B + 's-op-2-r/'
REVIEWS = 'docs/implementation/m3/reviews/codex-o1-law-r1/'
SOP2 = B + 'PROPOSAL-r6.md'
SOP2_SHA = 'ce8d3a4b783328915f0bf550dd111f227aa9901d5efddbcd9ccc8707cd4cb11d'
SOP2_REVIEW = 'docs/implementation/m3/reviews/codex-s-op-2-r6/review.json'
APP = 'docs/coop/completion/architecture-application.v1.json'
SDK4 = 'docs/coop/artifacts/component-sdk-contract.v4.json'
DRC = 'docs/coop/completion/distribution-runtime-completion.v2.md'
SDK4_POINTER = '/standardizedFamilies/1/rule'
DRC_LINE = 576


def git_show(path):
    return subprocess.run(['git', '-C', str(W), 'show', '%s:%s' % (REV, path)], check=True,
                          capture_output=True).stdout


def pin_bytes(path, raw):
    return {'path': path, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def read_pinned(row):
    raw = (A / row['path']).read_bytes()
    assert pin_bytes(row['path'], raw) == {k: row[k] for k in ('path', 'bytes', 'sha256')}, row['path']
    return raw


def pointer(document, ptr):
    value = document
    for token in ptr[1:].split('/'):
        key = token.replace('~1', '/').replace('~0', '~')
        value = value[int(key)] if isinstance(value, list) else value[key]
    return value


# --- The lock at REV: accepted paths and every bound passage key. ---------------------------------
lock = json.loads(git_show('design-lock.json'))
accepted, bound = {}, {}
for key in ('sourceManifest', 'applicationManifest'):
    for row in json.loads(read_pinned(lock['approvals'][key]))['files']:
        accepted[row['path']] = row
for binding in lock['contractSuccessors']:
    record = json.loads(read_pinned(binding['record']))
    accepted[binding['record']['path']] = binding['record']
    for row in record['candidates']:
        accepted[row['path']] = row
    for entry in record.get('passageOverrides', []) + record.get('passageSupersessions', []):
        bound[(entry['parent']['path'], json.dumps(entry['selector'], sort_keys=True))] = binding['record']['path']
for binding in lock['inventorySuccessors']:
    accepted[binding['candidate']['path']] = binding['candidate']
CONTRACT_SUCCESSORS = len(lock['contractSuccessors'])

# --- The parent finding. ------------------------------------------------------------------------
assert SDK4 not in accepted and DRC not in accepted, 'a parent is already selected; drop S-OP-2-P'
assert not any(path in (SDK4, DRC) for path, _ in bound), 'a bound passage already names SDK4 or DRC'
app_pin = {k: accepted[APP][k] for k in ('path', 'bytes', 'sha256')}
app = json.loads(read_pinned(app_pin))
sdk4_raw, drc_raw = (A / SDK4).read_bytes(), (A / DRC).read_bytes()
sdk4_pin, drc_pin = pin_bytes(SDK4, sdk4_raw), pin_bytes(DRC, drc_raw)
APP_SDK4 = '/rows/12/inheritedContract'
APP_DRC = '/evidenceTargets/D.SDK/sources/0'
assert pointer(app, APP_SDK4) == {'path': SDK4, 'pin': sdk4_pin['sha256']}
assert pointer(app, APP_DRC + '/path') == DRC and pointer(app, APP_DRC + '/pin') == drc_pin['sha256']
assert pointer(app, APP_DRC + '/selector') == '## 8. SDK contract (DR-125)'
assert pointer(app, '/rows/12/row') == 'DR-125'
for path in (P + 'successor.json', R + 'successor.json'):
    assert path not in accepted, path

# --- Item 24's text, read from the accepted S-OP-2 r6 bytes. ---------------------------------------
sop2_raw = (A / SOP2).read_bytes()
assert hashlib.sha256(sop2_raw).hexdigest() == SOP2_SHA, 'S-OP-2 r6 bytes changed'
lines = sop2_raw.decode('utf-8').splitlines()
assert lines[918] == '**24. Recording on acceptance (LD; r2, SOP2-R1-NB-05).**'
APPEND_HEAD = '  - **SDK4 `/standardizedFamilies/1/rule`.** Append: "'
assert lines[920].startswith(APPEND_HEAD) and lines[920].endswith('"')
APPEND = lines[920][len(APPEND_HEAD):-1]
assert lines[921] == '  - **DRC line 576.**'
DRC_BEFORE = lines[922][len('    - Before: "'):-len('".')]
DRC_AFTER = lines[923][len('    - After: "'):-len('".')]
assert lines[922] == '    - Before: "%s".' % DRC_BEFORE and lines[923] == '    - After: "%s".' % DRC_AFTER

sdk4_before = pointer(json.loads(sdk4_raw), SDK4_POINTER)
assert sdk4_before == 'Bounded structured diagnostics only. No unstructured host logs. Redaction is host-owned.'
sdk4_after = sdk4_before + APPEND
drc_line = drc_raw.decode('utf-8').splitlines()[DRC_LINE - 1]
assert drc_line == DRC_BEFORE, (drc_line, DRC_BEFORE)
INSERTED_DRC = ' The host reduces that channel to its byte count and truncation flag before any operational sink (contract successor S-OP-2).'
assert DRC_AFTER == 'meaning.' + INSERTED_DRC + DRC_BEFORE[len('meaning.'):]
for before, after, inserted in ((sdk4_before, sdk4_after, APPEND), (DRC_BEFORE, DRC_AFTER, INSERTED_DRC)):
    assert after.count(inserted) == 1 and after.replace(inserted, '', 1) == before, 'not insertion-only'
    assert '\u2014' not in inserted, 'em dash in new text'
overrides = [
    {'parent': sdk4_pin, 'selector': {'jsonPointer': SDK4_POINTER}, 'before': sdk4_before, 'after': sdk4_after},
    {'parent': drc_pin, 'selector': {'line': DRC_LINE}, 'before': DRC_BEFORE, 'after': DRC_AFTER},
]
for o in overrides:
    assert (o['parent']['path'], json.dumps(o['selector'], sort_keys=True)) not in bound

outputs = {}

# --- Unit S-OP-2-P: select the two parents, exactly as APP pins them. -------------------------------
record_p = {
    'schemaVersion': 1,
    'standing': 'PROPOSED S-OP-2-P, the parent selection of the S-OP-2 recording (S-OP-2 r6 item 24, accepted'
                ' by Codex as ACCEPT-DESIGN-UNIT; law M3-O1 r1 item 22): direct v4 contract-successor selection of'
                ' the exact existing SDK4 and DRC bytes that the accepted D-369 application pins, so that item 24\'s'
                ' two passage overrides have selected parents. No override, no text change, no schema, application,'
                ' register, gate or product change. Exact frozen candidate requires actual independent review and'
                ' root assent.',
    'scope': 'Selects component-sdk-contract.v4.json (APP /rows/12/inheritedContract, the DR-125 row\'s inherited'
             ' contract) and distribution-runtime-completion.v2.md (APP /evidenceTargets/D.SDK/sources/0, the'
             ' D.SDK selection of section 8) at their own paths with their APP-pinned bytes. Selection binds bytes'
             ' only: SDK4 keeps its own CANDIDATE-NOT-APPLIED header, and it and DRC mean exactly what the D-369'
             ' application already inherits from them.',
    'parents': [app_pin],
    'passageOverrides': [],
    'candidates': sorted([sdk4_pin, drc_pin], key=lambda r: r['path']),
    'acceptanceDoesNotQualifyProduct': True,
    'selection': {
        'kind': 'EXISTING-UNSELECTED-ARCHITECTURE-FILE',
        'precedent': 'docs/implementation/m1/control-source-v1/successor.json',
        'baseApproval': {key: lock['approvals'][key] for key in ('sourceManifest', 'applicationManifest')},
        'parentSelectedBy': 'sourceManifest',
        'files': [
            {'candidate': sdk4_pin, 'parentSelector': {'parent': app_pin, 'jsonPointer': APP_SDK4},
             'parentPin': sdk4_pin['sha256']},
            {'candidate': drc_pin, 'parentSelector': {'parent': app_pin, 'jsonPointer': APP_DRC},
             'parentPin': drc_pin['sha256']},
        ],
    },
    'carriedLimits': [
        'Selecting SDK4 does not apply it: its header still says CANDIDATE-NOT-APPLIED and binds NOTHING; the'
        ' DR-125 application row inherits it, and only that inheritance is carried.',
        'DRC is selected whole for byte provenance; only its section 8 is the D.SDK selection.',
        'No product, M3 or release qualification.',
    ],
}
outputs[P + 'successor.json'] = (json.dumps(record_p, indent=2, ensure_ascii=False) + '\n').encode()
record_p_pin = pin_bytes(P + 'successor.json', outputs[P + 'successor.json'])
subject_p = {'schemaVersion': 1, 'files': sorted(record_p['candidates'] + [record_p_pin], key=lambda r: r['path'])}
outputs[B + 's-op-2-p-subject.json'] = (json.dumps(subject_p, indent=2) + '\n').encode()
subject_p_pin = pin_bytes(B + 's-op-2-p-subject.json', outputs[B + 's-op-2-p-subject.json'])


# --- Unit S-OP-2-R: the recording. --------------------------------------------------------------
def fence(text):
    return '~~~text\n' + text + '\n~~~\n'


parts = ['# S-OP-2 recording passages (generated)\n',
         'Generated by `evidence/build_sop2.py` from the same data as `successor.json`; do not edit by hand.'
         ' Product lock: `%s`, %d contract successors. Both overrides are plain, insertion-only overrides: no'
         ' bound record overrides either passage, so there is nothing to supersede.\n' % (REV, CONTRACT_SUCCESSORS),
         'The text is S-OP-2 r6 item 24\'s (`%s`, %d bytes, `%s`), read from its lines 921, 923 and 924.\n'
         % (SOP2, len(sop2_raw), SOP2_SHA)]
for n, (o, inserted) in enumerate(zip(overrides, (APPEND, INSERTED_DRC)), 1):
    sel = o['selector'].get('jsonPointer') or 'line %d' % o['selector']['line']
    parts += ['## %d. `%s` %s\n' % (n, o['parent']['path'], sel),
              'Parent: %d bytes, `%s` (selected by S-OP-2-P).\n' % (o['parent']['bytes'], o['parent']['sha256']),
              'Before:\n', fence(o['before']), 'After:\n', fence(o['after']),
              'Inserted (the only change):\n', fence(inserted)]
outputs[R + 'PASSAGES.md'] = '\n'.join(parts).encode()


def current(path):
    return outputs[path] if path in outputs else (A / path).read_bytes()


HAND = [R + 'README.md', R + 'evidence/build_sop2.py', R + 'evidence/check_sop2.py']
candidates_r = sorted([pin_bytes(p, current(p)) for p in HAND + [R + 'PASSAGES.md']] + [pin_bytes(SOP2, sop2_raw)],
                      key=lambda r: r['path'])
for row in candidates_r:
    assert row['path'] not in accepted, 'candidate reuses an accepted path: ' + row['path']
record_r = {
    'schemaVersion': 1,
    'standing': 'PROPOSED S-OP-2-R, the recording of contract successor S-OP-2 r6 (the safe event vocabulary'
                ' and sink law, accepted by Codex as ACCEPT-DESIGN-UNIT, reviews/codex-s-op-2-r6), as its item 24'
                ' requires: the accepted PROPOSAL bytes are the successor text, pinned here as a candidate, and two'
                ' insertion-only passage overrides record its meaning in the DR-125 texts. SDK4'
                ' /standardizedFamilies/1/rule (SF-2) gains one sentence: host operational records are S-OP-2'
                ' registry events of SafeField kinds, free text reaches no operational sink, and the doctor report'
                ' keeps DR-114\'s tiers. DRC line 576 gains one sentence: the host reduces the bounded stderr'
                ' channel to its byte count and truncation flag before any operational sink. F02:193-197 is not'
                ' overridden. Binds after S-OP-2-P, which selects both parents. No new code, class, exit, route,'
                ' schema, register row, gate or product change. Exact frozen candidate requires actual independent'
                ' review and root assent.',
    'parents': sorted([sdk4_pin, drc_pin], key=lambda r: r['path']),
    'passageOverrides': overrides,
    'candidates': candidates_r,
}
outputs[R + 'successor.json'] = (json.dumps(record_r, indent=2, ensure_ascii=False) + '\n').encode()
record_r_pin = pin_bytes(R + 'successor.json', outputs[R + 'successor.json'])
subject_r = {'schemaVersion': 1, 'files': sorted(candidates_r + [record_r_pin], key=lambda r: r['path'])}
outputs[B + 's-op-2-r-subject.json'] = (json.dumps(subject_r, indent=2) + '\n').encode()
subject_r_pin = pin_bytes(B + 's-op-2-r-subject.json', outputs[B + 's-op-2-r-subject.json'])


def unit(name, subject_pin, record_pin, review, assessment):
    return {
        'schemaVersion': 1,
        'unit': name,
        'status': 'DRAFT-PENDING-REVIEW',
        'subjectManifest': subject_pin,
        'independentReview': {'path': review, 'bytes': None, 'sha256': None},
        'rootSubstantiveAssent': False,
        'requiredUnitFindings': [],
        'acceptedSuccessor': record_pin,
        'rootAssessment': assessment,
        'fullM2Complete': False,
        'productQualification': False,
    }


outputs[B + 's-op-2-p-unit.json'] = (json.dumps(unit(
    'operability-s-op-2-p', subject_p_pin, record_p_pin, REVIEWS + 's-op-2-p/review.json',
    'DRAFT (r1). Completed by the lead after Codex\'s review: status ACCEPTED-DESIGN-UNIT, the review pin,'
    ' rootSubstantiveAssent true. S-OP-2-P selects the exact SDK4 and DRC bytes the D-369 application pins, so'
    ' that S-OP-2 r6 item 24\'s overrides have selected parents; it overrides nothing. It binds on the'
    ' verify_design at product %s on top of %d contract successors, immediately before S-OP-2-R.'
    % (REV, CONTRACT_SUCCESSORS)), indent=2) + '\n').encode()
outputs[B + 's-op-2-r-unit.json'] = (json.dumps(unit(
    'operability-s-op-2-r', subject_r_pin, record_r_pin, REVIEWS + 's-op-2-r/review.json',
    'DRAFT (r1). Completed by the lead after Codex\'s review: status ACCEPTED-DESIGN-UNIT, the review pin,'
    ' rootSubstantiveAssent true. S-OP-2-R records contract successor S-OP-2 r6 (Codex ACCEPT-DESIGN-UNIT,'
    ' ce8d3a4b): it pins the accepted PROPOSAL bytes and makes item 24\'s two insertion-only overrides, SDK4'
    ' /standardizedFamilies/1/rule and DRC line 576. It binds after S-OP-2-P, on product %s, and its review'
    ' lists supersededPassages [].' % REV), indent=2) + '\n').encode()

if CHECK:
    stale = [p for p, b in outputs.items() if not (A / p).exists() or (A / p).read_bytes() != b]
    print(json.dumps({'check': 'identical' if not stale else 'DIFFERS', 'differs': stale}, indent=1))
    sys.exit(1 if stale else 0)
for path, raw in outputs.items():
    (A / path).write_bytes(raw)
print(json.dumps({'rev': REV, 'contractSuccessors': CONTRACT_SUCCESSORS,
                  'selection': {'subject': subject_p_pin, 'successor': record_p_pin},
                  'recording': {'subject': subject_r_pin, 'successor': record_r_pin,
                                'passageOverrides': len(overrides), 'candidates': len(candidates_r)},
                  'supersededPassages': []}, indent=1))
