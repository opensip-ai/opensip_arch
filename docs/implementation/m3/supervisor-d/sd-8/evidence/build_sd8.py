"""Build SD-8, the native-evidence passage supersession of SD-7's NE:3540 override that the lead's ruling on
E-3's ephemeral detail owes, with PASSAGES.md, the subject manifest and the lead's draft unit record.

Usage: build_sd8.py [--product PATH] [--rev REV] [--check]
- PATH is the product checkout (default /Users/sb/code/opensip-ai/opensip), read only. REV (default
  1799d3d, product main) names the commit whose design-lock.json is read with read-only `git show`.
- Without --check every generated file is written. With --check nothing is written: each generated
  file is rebuilt in memory and compared with the bytes on disk.

Deterministic: two runs give identical bytes. Run with python3 -I -B at nice -n 19. It needs the
hand-written README.md and evidence scripts to exist, because the record and the subject pin them.

Generated: sd-8/PASSAGES.md, sd-8/successor.json, ../sd-8-subject.json and ../sd-8-unit.json (the unit
record is not part of the subject).

The form (README LD-S8-1): NE:3540 carries SD-5's bound override, which SD-7 supersedes, and no later
record supersedes SD-7's entry. So SD-8 is one law VD2 contract passage supersession: same parent and
selector, `before` equal to SD-7's `after`, and `supersedes` naming SD-7's record by exact pin. Its
`after` keeps every word of SD-7's text and changes only the not-installed sentence's detail clause.
"""
import difflib, hashlib, json, re, subprocess, sys
from pathlib import Path

A = Path(__file__).resolve().parents[6]
args = list(sys.argv[1:])


def opt(name, default):
    if name in args:
        i = args.index(name)
        value = args[i + 1]
        del args[i:i + 2]
        return value
    return default


W = Path(opt('--product', '/Users/sb/code/opensip-ai/opensip'))
REV = opt('--rev', '1799d3d')
CHECK = '--check' in args
B = 'docs/implementation/m3/supervisor-d/'
D = B + 'sd-8/'
REVIEW = 'docs/implementation/m3/reviews/codex2-enum-1-sd-8-r1/sd-8/review.json'
NE = 'docs/v2/contracts/product-v1/native-evidence.md'
SD5 = B + 'sd-5/successor.json'
SD7 = B + 'sd-7/successor.json'
SELECTOR = {'line': 3540}


def git_show(path):
    return subprocess.run(['git', '-C', str(W), 'show', '%s:%s' % (REV, path)], check=True,
                          capture_output=True).stdout


def pin_bytes(path, raw):
    return {'path': path, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def read_pinned(row):
    raw = (A / row['path']).read_bytes()
    assert pin_bytes(row['path'], raw) == {k: row[k] for k in ('path', 'bytes', 'sha256')}, row['path']
    return raw


def edit(before, pairs):
    """Apply exact, single-occurrence replacements, in order."""
    text = before
    for old, new in pairs:
        assert text.count(old) == 1, old[:100]
        text = text.replace(old, new)
    assert text != before
    return text


# --- The lock at REV: accepted paths and each key's current published entry. -----------------------
lock = json.loads(git_show('design-lock.json'))
accepted, bound, records = {}, {}, {}
for key in ('sourceManifest', 'applicationManifest'):
    for row in json.loads(read_pinned(lock['approvals'][key]))['files']:
        accepted[row['path']] = row
for binding in lock['contractSuccessors']:
    record = json.loads(read_pinned(binding['record']))
    records[binding['record']['path']] = (binding['record'], record)
    accepted[binding['record']['path']] = binding['record']
    for row in record['candidates']:
        accepted[row['path']] = row
    for entry in record.get('passageOverrides', []) + record.get('passageSupersessions', []):
        bound[(entry['parent']['path'], json.dumps(entry['selector'], sort_keys=True))] = (binding['record'], entry)
CONTRACT_SUCCESSORS = len(lock['contractSuccessors'])
inventory_paths = {b['candidate']['path'] for b in lock['inventorySuccessors']} | {lock['inventorySuccessors'][0]['parent']['path']}
SUPERSESSIONS = sum(1 for _, r in records.values() for e in r.get('passageSupersessions', [])
                    if e['parent']['path'] not in inventory_paths)
assert NE.rsplit('/', 1)[-1] not in {row['path'].rsplit('/', 1)[-1] for _, r in records.values()
                                      for row in r['candidates']}, 'a complete NE copy is selected'

# --- SD-7's entry is the current meaning of NE:3540. ------------------------------------------------
key = (NE, json.dumps(SELECTOR, sort_keys=True))
sd7_pin, sd7 = records[SD7]
owner, target = bound[key]
assert owner == sd7_pin, ('NE:3540 is no longer SD-7\'s', owner)
assert target in sd7['passageSupersessions'] and target['supersedes']['record'] == records[SD5][0]
ne_pin = {k: accepted[NE][k] for k in ('path', 'bytes', 'sha256')}
assert target['parent'] == ne_pin

# --- The new text. ------------------------------------------------------------------------------
OLD = ('is never an excluded form and keeps that golden: `indeterminate` (3), `COVERAGE.PROVIDER_UNAVAILABLE`,'
       ' `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED`.')
NEW = ('is never an excluded form and keeps that golden: `indeterminate` (3), `COVERAGE.PROVIDER_UNAVAILABLE`,'
       ' with `COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED` on a durable request. On an ephemeral request, the'
       ' no-trust form included, it is `indeterminate` (3), `COVERAGE.PROVIDER_UNAVAILABLE`, `authority: ephemeral`,'
       ' with no runId and no detail, because the run-termination contract\'s §7.4 admits no detail on an ephemeral'
       ' attempt (contract successor SD-8).')
before = target['after']
after = edit(before, [(OLD, NEW)])
assert after.count('—') == before.count('—'), 'em dash in new text'
supersession = {'parent': ne_pin, 'selector': SELECTOR, 'before': before, 'after': after,
                'supersedes': {'record': sd7_pin, 'parent': ne_pin, 'selector': SELECTOR}}


# --- PASSAGES.md. ------------------------------------------------------------------------------
def fence(text):
    return '~~~text\n' + text + '\n~~~\n'


def changes(before, after):
    """Word-level changes, so that each fragment reads as text."""
    a, b = re.findall(r'\S+|\s+', before), re.findall(r'\S+|\s+', after)
    out = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes():
        if tag != 'equal':
            out.append('- %s: `%s` to `%s`' % (tag, ''.join(a[i1:i2]).strip().replace('`', "'") or '(nothing)',
                                                ''.join(b[j1:j2]).strip().replace('`', "'") or '(nothing)'))
    return '\n'.join(out) + '\n'


parts = ['# SD-8 passages (generated)\n',
         'Generated by `evidence/build_sd8.py` from the same data as `successor.json`; do not edit by hand. Product'
         ' lock: `%s`, %d contract successors, %d contract passage supersessions.\n'
         % (REV, CONTRACT_SUCCESSORS, SUPERSESSIONS),
         '## Passage supersession (law VD2)\n',
         'The `before` is SD-7\'s bound `after` for NE:3540, and `supersedes` names SD-7\'s record `%s` (%d bytes,'
         ' `%s`). SD-7 itself superseded SD-5\'s override of the same line. The text is two table rows: the raw'
         ' release-declaration row, then the excluded-form row. SD-8 changes one sentence of the second row.\n'
         % (sd7_pin['path'], sd7_pin['bytes'], sd7_pin['sha256']),
         '### 1. `%s` line %d (supersedes SD-7)\n' % (NE, SELECTOR['line']),
         'Before:\n', fence(before), 'After:\n', fence(after), 'Changes:\n', changes(before, after)]
outputs = {D + 'PASSAGES.md': '\n'.join(parts).encode()}


def current(path):
    return outputs[path] if path in outputs else (A / path).read_bytes()


HAND = [D + 'README.md', D + 'evidence/build_sd8.py', D + 'evidence/check_sd8.py']
GENERATED = [D + 'PASSAGES.md']
candidates = sorted([pin_bytes(p, current(p)) for p in HAND + GENERATED], key=lambda r: r['path'])
for row in candidates:
    assert row['path'] not in accepted, 'candidate reuses an accepted path: ' + row['path']
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED SD-8 native-evidence contract successor (lead ruling 2026-10-04 on E-3\'s ephemeral'
                ' detail, recorded in reviews/grok-j2a-r1/REQUEST.md, "Lead rulings", item 3, and applied by M3-C r8'
                ' item 7), in law VD2\'s form: one contract passage supersession of SD-7\'s NE:3540 override, naming'
                ' SD-7\'s record by exact pin. It keeps every word of SD-7\'s two rows and changes one sentence of the'
                ' excluded-form row: a required closure that is not installed, or that current trust does not admit,'
                ' keeps the not-installed golden with COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED on a durable request;'
                ' on an ephemeral request, the no-trust form included, it is indeterminate (3),'
                ' COVERAGE.PROVIDER_UNAVAILABLE, authority ephemeral, no runId and no detail, under the'
                ' run-termination contract section 7.4. No new code, class, exit, route, detail, schema, WS, RTC or'
                ' product change. Exact frozen candidate requires actual independent review, listing'
                ' supersededPassages, and root assent.',
    'parents': [ne_pin],
    'passageOverrides': [],
    'passageSupersessions': [supersession],
    'candidates': candidates,
}
outputs[D + 'successor.json'] = (json.dumps(record, indent=2, ensure_ascii=False) + '\n').encode()
record_pin = pin_bytes(D + 'successor.json', outputs[D + 'successor.json'])
subject = {'schemaVersion': 1, 'files': sorted(candidates + [record_pin], key=lambda r: r['path'])}
outputs[B + 'sd-8-subject.json'] = (json.dumps(subject, indent=2) + '\n').encode()
subject_pin = pin_bytes(B + 'sd-8-subject.json', outputs[B + 'sd-8-subject.json'])
unit = {
    'schemaVersion': 1,
    'unit': 'supervisor-d-sd-8',
    'status': 'DRAFT-PENDING-REVIEW',
    'subjectManifest': subject_pin,
    'independentReview': {'path': REVIEW, 'bytes': None, 'sha256': None},
    'rootSubstantiveAssent': False,
    'requiredUnitFindings': [],
    'acceptedSuccessor': record_pin,
    'rootAssessment': 'DRAFT (r1). Completed by the lead after CODEX2\'s review: status ACCEPTED-DESIGN-UNIT, the'
                      ' review pin, rootSubstantiveAssent true. SD-8 is one VD2 contract passage supersession of'
                      ' SD-7\'s NE:3540 override: the durable not-installed case keeps'
                      ' COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED, and an ephemeral request, the no-trust form'
                      ' included, carries no detail under RTC section 7.4. It binds on the verify_design at product'
                      ' %s on top of %d contract successors, and its review must carry supersededPassages.'
                      % (REV, CONTRACT_SUCCESSORS),
    'fullM2Complete': False,
    'productQualification': False,
}
outputs[B + 'sd-8-unit.json'] = (json.dumps(unit, indent=2) + '\n').encode()

if CHECK:
    stale = [p for p, b in outputs.items() if not (A / p).exists() or (A / p).read_bytes() != b]
    print(json.dumps({'check': 'identical' if not stale else 'DIFFERS', 'differs': stale}, indent=1))
    sys.exit(1 if stale else 0)
for path, raw in outputs.items():
    (A / path).write_bytes(raw)
print(json.dumps({'rev': REV, 'contractSuccessors': CONTRACT_SUCCESSORS, 'contractPassageSupersessionsBefore': SUPERSESSIONS,
                  'passageSupersessions': 1, 'passageOverrides': 0, 'candidates': len(candidates),
                  'subject': subject_pin, 'successor': record_pin,
                  'supersededPassages': [supersession['supersedes']]}, indent=1))
