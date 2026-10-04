"""Build ENUM-1, the enumeration contract successor that M3-C r8's cross-law finding X-8 owes, with
PASSAGES.md, the subject manifest and the lead's draft unit record.

Usage: build_enum_1.py [--product PATH] [--rev REV] [--check]
- PATH is the product checkout (default /Users/sb/code/opensip-ai/opensip), read only. REV (default
  1799d3d, product main) names the commit whose design-lock.json is read with read-only `git show`.
- Without --check every generated file is written. With --check nothing is written: each generated
  file is rebuilt in memory and compared with the bytes on disk.

Deterministic: two runs give identical bytes. Run with python3 -I -B at nice -n 19. It needs the
hand-written README.md and evidence scripts to exist, because the record and the subject pin them.

Generated: enum-1/PASSAGES.md, enum-1/successor.json, ../enum-1-subject.json and ../enum-1-unit.json
(the unit record is not part of the subject).

The form (README LD-1 to LD-3): no target key carries a bound override at REV, so every entry is a
plain override; none is a VD2 passage supersession. The markdown parents are the frozen foundation
contracts, of which no complete copy is selected. The two schema parents are SYN-1F's complete
copies, the last complete copy of each schema in the chain.
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
M = 'docs/implementation/m3/snapshot-plan-c/'
D = M + 'enum-1/'
REVIEW = 'docs/implementation/m3/reviews/codex2-enum-1-sd-8-r1/enum-1/review.json'

F = 'docs/coop/design-corrections/foundation/'
ENC = F + 'enumeration-contract.v1.md'
EXC = F + 'execution-inputs-contract.v1.md'
COMP = F + 'evaluator-composition-contract.v3.md'
S = 'docs/implementation/m3/syntax-e/syn-1f/design/foundation/'
EPS = S + 'enumeration-plan.schema.v1.json'
EXS = S + 'execution-inputs.schema.v1.json'


def git_show(path):
    return subprocess.run(['git', '-C', str(W), 'show', '%s:%s' % (REV, path)], check=True,
                          capture_output=True).stdout


def pin_bytes(path, raw):
    return {'path': path, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def read_pinned(row):
    raw = (A / row['path']).read_bytes()
    assert pin_bytes(row['path'], raw) == {k: row[k] for k in ('path', 'bytes', 'sha256')}, row['path']
    return raw


def resolve(doc, pointer):
    for token in pointer[1:].split('/'):
        doc = doc[token.replace('~1', '/').replace('~0', '~')]
    return doc


def edit(before, pairs):
    """Apply exact, single-occurrence replacements, in order."""
    text = before
    for old, new in pairs:
        assert text.count(old) == 1, old[:100]
        text = text.replace(old, new)
    assert text != before
    return text


# --- The lock at REV: accepted paths, bound keys, and the complete copies in the chain. ---------
lock = json.loads(git_show('design-lock.json'))
accepted, bound, records = {}, {}, {}
for key in ('sourceManifest', 'applicationManifest'):
    for row in json.loads(read_pinned(lock['approvals'][key]))['files']:
        accepted[row['path']] = row
copies = {}
for binding in lock['contractSuccessors']:
    record = json.loads(read_pinned(binding['record']))
    records[binding['record']['path']] = (binding['record'], record)
    accepted[binding['record']['path']] = binding['record']
    for row in record['candidates']:
        accepted[row['path']] = row
        copies.setdefault(row['path'].rsplit('/', 1)[-1], []).append(row['path'])
    for entry in record.get('passageOverrides', []) + record.get('passageSupersessions', []):
        bound[(entry['parent']['path'], json.dumps(entry['selector'], sort_keys=True))] = (binding['record'], entry)
CONTRACT_SUCCESSORS = len(lock['contractSuccessors'])
inventory_paths = {b['candidate']['path'] for b in lock['inventorySuccessors']} | {lock['inventorySuccessors'][0]['parent']['path']}
SUPERSESSIONS = sum(1 for _, r in records.values() for e in r.get('passageSupersessions', [])
                    if e['parent']['path'] not in inventory_paths)

# The markdown parents have no complete copy in the chain; each schema parent is its last copy.
for path in (ENC, EXC, COMP):
    assert path.rsplit('/', 1)[-1] not in copies, ('a complete copy exists', path)
for path in (EPS, EXS):
    assert copies[path.rsplit('/', 1)[-1]][-1] == path, copies[path.rsplit('/', 1)[-1]]

# --- The new text. ------------------------------------------------------------------------------
CASE = ('no admitted closure can lawfully be the binding\'s selected enumerator, because a closure the cell\'s mode'
        ' needs is not admitted for the request')

ENC53_OLD = '`required=true` plus unselected refuses (`ENUMERATION_PLAN_REQUIRED_UNSELECTED_ENUMERATOR`).'
ENC53_NEW = (
    '`required=true` plus unselected refuses (`ENUMERATION_PLAN_REQUIRED_UNSELECTED_ENUMERATOR`), except in one'
    ' case (contract successor ENUM-1, 2026-10-04): **a required cell whose closure is not admitted.** When '
    + CASE + ' (for a TypeScript or Rust mode, its provider closure; for `syntax-only`, a grammar closure,'
    ' without which no syntax universe exists for the core provider closure to enumerate), the binding of a'
    ' `required=true` cell takes the same unselected shape, `{status:"unselected", reason:"optional-unselected"}`,'
    ' and the `reason` token keeps its spelling. Its pair is exactly deficiency `provider-unavailable` with'
    ' `nativeCause` null. Its `universe` is null, its host extents are still populated, and its inventories are'
    ' empty `unavailable` with that pair. It covers a required provider closure that is not installed, or that'
    ' current trust does not admit (workflows-and-surfaces §9, "required provider closure not installed"), and an'
    ' ephemeral request with no admitted trust view, which admits no component closure. The cell stays required. Its unavailable work holds'
    ' the Run at `indeterminate` through `requiredCellDeficiencies` (`execution-inputs-contract.v1.md` §4 and §5),'
    ' and required-cell totality is unchanged. A required cell whose closure is admitted never takes this shape:'
    ' its binding names that closure, available or not. An `inventory` cell never meets the case, because its'
    ' enumerator is the core provider closure (`identity-and-evidence.md` §3, core role closures). Closure'
    ' admission is not an input of this admission, so the host establishes the case when it builds the Plan, and'
    ' admission checks the shape. A required unselected binding with any other pair still refuses.')
ENC75_OLD = 'A `required=true` cell still may not be unselected'
ENC75_NEW = 'Outside ENUM-1\'s one case (**Enumerator**, above), a `required=true` cell still may not be unselected'
ENC145_OLD = 'required+unselected enumerator;'
ENC145_NEW = 'required+unselected enumerator outside ENUM-1\'s one case (§1, **Enumerator**);'

SEL_OLD = 'Missing capability/provider selection for a required cell refuses pre-Plan (no fictional closure).'
SEL_NEW = ('Missing capability/provider selection for a required cell refuses pre-Plan (no fictional closure),'
           ' except in contract successor ENUM-1\'s one case: when ' + CASE + ', the binding is'
           ' UnavailableProgramBindingV1 with UnselectedEnumeratorRef and deficiency provider-unavailable with'
           ' nativeCause null, never a fictional closure.')
UNSEL_OLD = 'Optional-cell enumerator not selected. Lawful only on UnavailableProgramBindingV1 when the cell required=false.'
UNSEL_NEW = ('Enumerator not selected. Lawful only on UnavailableProgramBindingV1, in two cases: the cell required=false;'
             ' or contract successor ENUM-1\'s one case, where the cell required=true and ' + CASE + ', with'
             ' deficiency provider-unavailable and nativeCause null. The reason token is optional-unselected in both'
             ' cases.')
EREF_OLD = 'or unselected optional-unselected when required=false.'
EREF_NEW = ('or unselected optional-unselected when required=false or in contract successor ENUM-1\'s one case'
            ' (required=true, ' + CASE + ', provider-unavailable with nativeCause null).')

EXC103_OLD = '`EXECUTION_INPUTS_CANDIDATE_REQUIRED` first.'
EXC103_NEW = ('`EXECUTION_INPUTS_CANDIDATE_REQUIRED` first, except in the enumeration contract\'s ENUM-1 case'
              ' (`enumeration-contract.v1.md` §1, **Enumerator**). There the cell\'s closure is not admitted, its'
              ' enumerator is unselected and no producer can return an envelope, so its row is `unavailable` with'
              ' the binding carrier (cross-source row 1, above) and emits its `requiredCellDeficiencies` row.')
EXC110_OLD = 'it refuses an unselected enumerator on an available binding or a required cell, and'
EXC110_NEW = ('it refuses an unselected enumerator on an available binding, and on a required cell except in its'
              ' ENUM-1 case, which carries exactly `provider-unavailable` with `nativeCause` null; and it')
EXC131_OLD = '**the enumerator was not selected** (an optional'
EXC131_NEW = ('**the enumerator was not selected** (an optional, or in the enumeration contract\'s ENUM-1 case a'
              ' required,')
COMP235_OLD = ('A required cell with **no** retained envelope refuses `EXECUTION_INPUTS_CANDIDATE_REQUIRED` before'
               ' reaching this bridge.')
COMP235_NEW = ('A required cell with **no** retained envelope refuses `EXECUTION_INPUTS_CANDIDATE_REQUIRED` before'
               ' reaching this bridge, except in the enumeration contract\'s ENUM-1 case, whose unselected binding'
               ' takes the row above.')
CAND_OLD = 'a required one refuses EXECUTION_INPUTS_CANDIDATE_REQUIRED first.'
CAND_NEW = ('a required one refuses EXECUTION_INPUTS_CANDIDATE_REQUIRED first, except in the enumeration contract\'s'
            ' ENUM-1 case, where the cell\'s closure is not admitted and its unselected binding\'s row is'
            ' unavailable with the binding carrier.')

# (parent, selector, pairs, role). Order: the enumeration contract, its schema, then its two consumers.
SPEC = [
    (ENC, {'line': 53}, [(ENC53_OLD, ENC53_NEW)], 'the rule and its one exception'),
    (ENC, {'line': 75}, [(ENC75_OLD, ENC75_NEW)], 'the restatement in the enumerator-status note'),
    (ENC, {'line': 145}, [(ENC145_OLD, ENC145_NEW)], 'the class table, invalid row'),
    (EPS, {'jsonPointer': '/$defs/SelectedEnumeratorRef/description'}, [(SEL_OLD, SEL_NEW)],
     'the schema: "refuses pre-Plan"'),
    (EPS, {'jsonPointer': '/$defs/UnselectedEnumeratorRef/description'}, [(UNSEL_OLD, UNSEL_NEW)],
     'the schema: "lawful only when required=false"'),
    (EPS, {'jsonPointer': '/$defs/EnumeratorRef/description'}, [(EREF_OLD, EREF_NEW)],
     'the schema: the union\'s note'),
    (EXC, {'line': 103}, [(EXC103_OLD, EXC103_NEW)], 'the candidate-required refusal'),
    (EXC, {'line': 110}, [(EXC110_OLD, EXC110_NEW)], 'its restatement of the enumeration owner\'s refusal'),
    (EXC, {'line': 131}, [(EXC131_OLD, EXC131_NEW)], 'the meaning of an unselected binding'),
    (EXS, {'jsonPointer': '/x-opensip-derived-carrier-law/candidateCarrier'}, [(CAND_OLD, CAND_NEW)],
     'the schema copy of the candidate-required refusal'),
    (COMP, {'line': 235}, [(COMP235_OLD, COMP235_NEW)], 'the proof bridge\'s restatement of that refusal'),
]

parents, overrides, raw_by_path = {}, [], {}
for path, selector, pairs, _ in SPEC:
    key = (path, json.dumps(selector, sort_keys=True))
    assert key not in bound, ('already overridden at %s' % REV, key)
    pin = {k: accepted[path][k] for k in ('path', 'bytes', 'sha256')}
    raw = raw_by_path.setdefault(path, read_pinned(pin))
    parents[path] = pin
    if 'line' in selector:
        before = raw.decode('utf-8').splitlines()[selector['line'] - 1]
    else:
        before = resolve(json.loads(raw), selector['jsonPointer'])
    assert isinstance(before, str)
    after = edit(before, pairs)
    assert after.count('—') == before.count('—'), 'em dash in new text'
    overrides.append({'parent': pin, 'selector': selector, 'before': before, 'after': after})


# --- PASSAGES.md. ------------------------------------------------------------------------------
def selector_text(selector):
    return 'line %d' % selector['line'] if 'line' in selector else 'pointer `%s`' % selector['jsonPointer']


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


parts = ['# ENUM-1 passages (generated)\n',
         'Generated by `evidence/build_enum_1.py` from the same data as `successor.json`; do not edit by hand. Each'
         ' entry gives the parent, the selector, the exact `before` and the candidate `after`, then the word-level'
         ' changes. Product lock: `%s`, %d contract successors, %d contract passage supersessions. No target key'
         ' carries a bound override there, so every entry is a plain override.\n'
         % (REV, CONTRACT_SUCCESSORS, SUPERSESSIONS),
         '## Passage overrides\n']
for n, (entry, (_, _, _, role)) in enumerate(zip(overrides, SPEC), 1):
    parts.append('### %d. `%s` %s (%s)\n' % (n, entry['parent']['path'], selector_text(entry['selector']), role))
    parts += ['Before:\n', fence(entry['before']), 'After:\n', fence(entry['after']), 'Changes:\n',
              changes(entry['before'], entry['after'])]
outputs = {D + 'PASSAGES.md': '\n'.join(parts).encode()}


def current(path):
    return outputs[path] if path in outputs else (A / path).read_bytes()


HAND = [D + 'README.md', D + 'evidence/build_enum_1.py', D + 'evidence/check_enum_1.py']
GENERATED = [D + 'PASSAGES.md']
candidates = sorted([pin_bytes(p, current(p)) for p in HAND + GENERATED], key=lambda r: r['path'])
for row in candidates:
    assert row['path'] not in accepted, 'candidate reuses an accepted path: ' + row['path']
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED ENUM-1 enumeration contract successor (law M3-C r8 cross-law finding X-8; lead decision'
                ' 2026-10-04): the enumeration contract admits an unselected enumerator on a required cell in exactly'
                ' one case, a required cell whose closure is not admitted (no admitted closure can lawfully be the'
                ' binding\'s selected enumerator, because a closure the cell\'s mode needs is not admitted for the'
                ' request), with the existing UnselectedEnumeratorRef shape, deficiency provider-unavailable and'
                ' nativeCause null, a null universe, populated host extents and empty unavailable inventories. The'
                ' cell stays required and holds the Run at indeterminate. Every other required unselected binding'
                ' still refuses ENUMERATION_PLAN_REQUIRED_UNSELECTED_ENUMERATOR. Eleven plain passage overrides:'
                ' enumeration-contract lines 53, 75 and 145; three descriptions of SYN-1F\'s selected'
                ' enumeration-plan schema copy; execution-inputs-contract lines 103, 110 and 131 and the'
                ' candidateCarrier law of SYN-1F\'s selected execution-inputs schema copy, so that the case is not'
                ' refused downstream as a required candidate cell with no envelope; and evaluator-composition line'
                ' 235. No passage supersession, schema shape, token, refusal code, class, exit, route, registry,'
                ' generated code, reference model, inventory or product change. Exact frozen candidate requires'
                ' actual independent review and root assent.',
    'parents': sorted(parents.values(), key=lambda r: r['path']),
    'passageOverrides': overrides,
    'passageSupersessions': [],
    'candidates': candidates,
}
outputs[D + 'successor.json'] = (json.dumps(record, indent=2, ensure_ascii=False) + '\n').encode()
record_pin = pin_bytes(D + 'successor.json', outputs[D + 'successor.json'])
subject = {'schemaVersion': 1, 'files': sorted(candidates + [record_pin], key=lambda r: r['path'])}
outputs[M + 'enum-1-subject.json'] = (json.dumps(subject, indent=2) + '\n').encode()
subject_pin = pin_bytes(M + 'enum-1-subject.json', outputs[M + 'enum-1-subject.json'])
unit = {
    'schemaVersion': 1,
    'unit': 'snapshot-plan-c-enum-1',
    'status': 'DRAFT-PENDING-REVIEW',
    'subjectManifest': subject_pin,
    'independentReview': {'path': REVIEW, 'bytes': None, 'sha256': None},
    'rootSubstantiveAssent': False,
    'requiredUnitFindings': [],
    'acceptedSuccessor': record_pin,
    'rootAssessment': 'DRAFT (r1). Completed by the lead after CODEX2\'s review: status ACCEPTED-DESIGN-UNIT, the'
                      ' review pin, rootSubstantiveAssent true. ENUM-1 carries M3-C r8\'s X-8: the enumeration'
                      ' contract admits an unselected enumerator on a required cell exactly when the cell\'s closure'
                      ' is not admitted, with deficiency provider-unavailable and nativeCause null. Eleven plain'
                      ' overrides (ENC 53, 75, 145; three SYN-1F enumeration-plan schema descriptions; EXC 103, 110,'
                      ' 131; SYN-1F execution-inputs candidateCarrier; COMP 235), no supersession. It binds on the'
                      ' verify_design at product %s on top of %d contract successors.' % (REV, CONTRACT_SUCCESSORS),
    'fullM2Complete': False,
    'productQualification': False,
}
outputs[M + 'enum-1-unit.json'] = (json.dumps(unit, indent=2) + '\n').encode()

if CHECK:
    stale = [p for p, b in outputs.items() if not (A / p).exists() or (A / p).read_bytes() != b]
    print(json.dumps({'check': 'identical' if not stale else 'DIFFERS', 'differs': stale}, indent=1))
    sys.exit(1 if stale else 0)
for path, raw in outputs.items():
    (A / path).write_bytes(raw)
print(json.dumps({'rev': REV, 'contractSuccessors': CONTRACT_SUCCESSORS, 'contractPassageSupersessionsBefore': SUPERSESSIONS,
                  'passageOverrides': len(overrides), 'passageSupersessions': 0,
                  'parents': len(parents), 'candidates': len(candidates), 'subject': subject_pin,
                  'successor': record_pin, 'supersededPassages': []}, indent=1))
