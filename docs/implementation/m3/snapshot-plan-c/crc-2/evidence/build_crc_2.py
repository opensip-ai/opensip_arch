"""Build CRC-2, the identity successor of law M3-C r8's X-H3 (item 9, use 3), with PASSAGES.md, the
subject manifest and the lead's draft unit record.

Usage: build_crc_2.py [--product PATH] [--rev REV] [--check]
- PATH is the product checkout (default /Users/sb/code/opensip-ai/opensip), read only. REV (default
  21e428d, product main) names the commit whose design-lock.json is read with read-only `git show`.
- Without --check every generated file is written. With --check nothing is written: each generated
  file is rebuilt in memory and compared with the bytes on disk.

Deterministic: two runs give identical bytes. Run with python3 -I -B at nice -n 19. It needs the
hand-written README.md and evidence scripts to exist, because the record and the subject pin them.

Generated: crc-2/PASSAGES.md, crc-2/successor.json, ../crc-2-subject.json and ../crc-2-unit.json
(the unit record is not part of the subject).

The form (README LD-1, LD-2):
- IE:285 and IE:1377 carry CRC-1's bound overrides, so CRC-2 supersedes them in law VD2's form: same
  parent and selector, `before` equal to CRC-1's `after`, and `supersedes` naming CRC-1's record by
  exact pin.
- The identity-schema strings live, with CRC-1's meaning carried in place, in SYN-1F's complete copy,
  which is the selected IDS. No bound successor overrides them there, so CRC-2 overrides them plainly.
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
REV = opt('--rev', '21e428d')
CHECK = '--check' in args
M = 'docs/implementation/m3/snapshot-plan-c/'
D = M + 'crc-2/'
REVIEW = 'docs/implementation/m3/reviews/codex2-snapshot-plan-c-r8/crc-2/review.json'

IE = 'docs/v2/contracts/product-v1/identity-and-evidence.md'
CRC1 = M + 'crc-1/successor.json'
IDS_I1L = 'docs/implementation/m3/preview-pack-i1/i1-l/design/foundation/identity-schemas.v3.json'
IDS = 'docs/implementation/m3/syntax-e/syn-1f/design/foundation/identity-schemas.v3.json'
NOTE = '/x-opensip-digest-domains/closureKinds/note'
LAW = '/x-opensip-digest-domains/closureMembership/selectionLaw'


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


# --- The lock at REV: accepted paths, bound keys, and each key's current published entry. ------
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
                    if e['parent']['path'] not in inventory_paths)  # contract passage supersessions only (VD2)

# The selected identity schema bundle: the last complete identity-schemas.v3.json copy in the chain.
copies = [row['path'] for _, rec in records.values() for row in rec['candidates']
          if row['path'].endswith('/design/foundation/identity-schemas.v3.json')]
assert copies[-1] == IDS and IDS_I1L in copies, copies

# --- CRC-1's bound entries, which CRC-2 supersedes or whose meaning it carries. -----------------
crc1_pin, crc1 = records[CRC1]
crc1_by_key = {(e['parent']['path'], json.dumps(e['selector'], sort_keys=True)): e for e in crc1['passageOverrides']}

# --- The new text. ------------------------------------------------------------------------------
HEAD_OLD = '**Core role closures (contract successor CRC-1, 2026-10-04).**'
HEAD_NEW = '**Core role closures (contract successors CRC-1 and CRC-2, 2026-10-04).**'
PROVIDER_OLD = (
    '- **The core provider closure** has exactly two admitted uses under the one provider identity: (1) the'
    ' `import.producerClosure` of an import whose `kind` is `dependency` or `prepared`; (2) the producer of'
    ' syntax-universe work, only where the record\'s, stage\'s or binding\'s universe is a'
    ' `native.semantic-universe.syntax.v2` identity: `subject-scope.enumeratorClosure`, `view.producerClosure` and so'
    ' `fact.producerClosure`, `stage-spec.producerClosure`, an enumeration binding\'s `enumerator.closureId`, and'
    ' `CandidateProducerResultV1.producerClosure`. It is a `plan.semanticClosures` member exactly when the Plan selects'
    ' a syntax universe, and is never selected otherwise, not even explicitly. It is never the producer of a TypeScript'
    ' or Rust record. The grammar'
    ' closure keeps kind `grammar` and is never a producer, and a TypeScript or Rust provider closure is never the'
    ' producer of a syntax record. As every stage producer does, the core provider closure registers each syntax'
    ' stage\'s output schema as a core platform tree member at `opensip-interface/stage-output/<operation>.schema.json`'
    ' (below).')
PROVIDER_NEW = (
    '- **The core provider closure** has exactly three admitted uses under the one provider identity: (1) the'
    ' `import.producerClosure` of an import whose `kind` is `dependency` or `prepared`; (2) the producer of'
    ' syntax-universe work, only where the record\'s, stage\'s or binding\'s universe is a'
    ' `native.semantic-universe.syntax.v2` identity: `subject-scope.enumeratorClosure`, `view.producerClosure` and so'
    ' `fact.producerClosure`, `stage-spec.producerClosure`, an enumeration binding\'s `enumerator.closureId`, and'
    ' `CandidateProducerResultV1.producerClosure`; (3) (contract successor CRC-2) the producer and enumerator of host'
    ' inventory records in every universe. These are the records of the three `inventory` relations,'
    ' `file@enumerated`, `package@manifest-declared` and `vcs-change@vcs-reported`, that the host derives from retained'
    ' records and that no language provider produces. Use (3) has exactly four fields: the `enumerator.closureId` of'
    ' each enumeration binding of a requested `inventory` cell, available or not; the `stage-spec.producerClosure` of'
    ' each host inventory stage; and that stage\'s `view.producerClosure`, and so `fact.producerClosure`, and its'
    ' `subject-scope.enumeratorClosure`. Use (3) never admits a record of another relation, a record a language'
    ' provider returned, the enumerator of a binding that owes a symbol inventory, or'
    ' `CandidateProducerResultV1.producerClosure`. The core provider closure is a `plan.semanticClosures` member'
    ' exactly when the Plan selects a syntax universe or requests an `inventory` cell, and is never selected'
    ' otherwise, not even explicitly. Apart from use (3), it is never the producer of a TypeScript or Rust record.'
    ' The grammar closure keeps kind `grammar` and is never a producer, a TypeScript or Rust provider closure is never'
    ' the producer of a syntax record, and no language provider closure is the producer or enumerator of an'
    ' `inventory` relation\'s record. As every stage producer does, the core provider closure registers each syntax'
    ' stage\'s and each host inventory stage\'s output schema as a core platform tree member at'
    ' `opensip-interface/stage-output/<operation>.schema.json` (below).')
IE1377_PAIRS = [
    ('(contract successor CRC-1, above)', '(contract successors CRC-1 and CRC-2, above)'),
    ('exactly when the Plan selects a `native.semantic-universe.syntax.v2` universe,',
     'exactly when the Plan selects a `native.semantic-universe.syntax.v2` universe or requests an `inventory` cell,'),
]
NOTE_OLD = (
    'The core provider closure has exactly two uses under one identity: the import.producerClosure of a dependency or'
    ' prepared import, and the producer of syntax-universe work (subject-scope.enumeratorClosure, view.producerClosure'
    ' and so fact.producerClosure, stage-spec.producerClosure, the enumeration binding\'s enumerator.closureId and'
    ' CandidateProducerResultV1.producerClosure) only where the universe is a native.semantic-universe.syntax.v2'
    ' identity; it never produces a TypeScript or Rust record.')
NOTE_NEW = (
    'The core provider closure has exactly three uses under one identity: the import.producerClosure of a dependency'
    ' or prepared import; the producer of syntax-universe work (subject-scope.enumeratorClosure, view.producerClosure'
    ' and so fact.producerClosure, stage-spec.producerClosure, the enumeration binding\'s enumerator.closureId and'
    ' CandidateProducerResultV1.producerClosure) only where the universe is a native.semantic-universe.syntax.v2'
    ' identity; and (contract successor CRC-2) the producer and enumerator of the host-derived records of the three'
    ' inventory relations, file@enumerated, package@manifest-declared and vcs-change@vcs-reported, in every universe.'
    ' Its third use has four fields: the enumerator.closureId of a requested inventory cell\'s binding; the host'
    ' inventory stage\'s stage-spec.producerClosure; and that stage\'s view.producerClosure, so fact.producerClosure,'
    ' and subject-scope.enumeratorClosure. Apart from that third use it never produces a TypeScript or Rust record,'
    ' and no language provider closure produces or enumerates an inventory relation\'s record.')
LAW_PAIRS = [
    ('(contract successor CRC-1):', '(contract successors CRC-1 and CRC-2):'),
    ('exactly when the Plan selects a native.semantic-universe.syntax.v2 universe,',
     'exactly when the Plan selects a native.semantic-universe.syntax.v2 universe or requests an inventory cell,'),
]

SUPERSESSIONS_SPEC = [
    ({'line': 285}, [(HEAD_OLD, HEAD_NEW), (PROVIDER_OLD, PROVIDER_NEW)]),
    ({'line': 1377}, IE1377_PAIRS),
]
OVERRIDES_SPEC = [
    ({'jsonPointer': NOTE}, [(NOTE_OLD, NOTE_NEW)]),
    ({'jsonPointer': LAW}, LAW_PAIRS),
]

parents = {}
supersessions = []
for selector, pairs in SUPERSESSIONS_SPEC:
    key = (IE, json.dumps(selector, sort_keys=True))
    owner, target = bound[key]
    # The current meaning of the key is CRC-1's override: no later record supersedes it.
    assert owner == crc1_pin and target == crc1_by_key[key], (key, owner)
    assert 'supersedes' not in target
    parent = {k: target['parent'][k] for k in ('path', 'bytes', 'sha256')}
    assert {k: accepted[IE][k] for k in ('path', 'bytes', 'sha256')} == parent
    parents[IE] = parent
    before = target['after']
    after = edit(before, pairs)
    supersessions.append({'parent': parent, 'selector': selector, 'before': before, 'after': after,
                          'supersedes': {'record': crc1_pin, 'parent': parent, 'selector': selector}})

ids_row = accepted[IDS]
ids_pin = {k: ids_row[k] for k in ('path', 'bytes', 'sha256')}
ids_doc = json.loads(read_pinned(ids_pin))
parents[IDS] = ids_pin
overrides = []
for selector, pairs in OVERRIDES_SPEC:
    key = (IDS, json.dumps(selector, sort_keys=True))
    assert key not in bound, ('already overridden', key)
    before = resolve(ids_doc, selector['jsonPointer'])
    # SYN-1F carries CRC-1's I1-L override in place: the selected string is CRC-1's meaning.
    carried = crc1_by_key[(IDS_I1L, json.dumps(selector, sort_keys=True))]
    assert before == carried['after'], selector
    overrides.append({'parent': ids_pin, 'selector': selector, 'before': before, 'after': edit(before, pairs)})

for entry in supersessions + overrides:
    assert entry['after'].count('\u2014') == entry['before'].count('\u2014'), 'em dash in new text'


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


parts = ['# CRC-2 passages (generated)\n',
         'Generated by `evidence/build_crc_2.py` from the same data as `successor.json`; do not edit by hand. Each'
         ' entry gives the parent, the selector, the exact `before` and the candidate `after`, then the word-level'
         ' changes. Product lock: `%s`, %d contract successors, %d contract passage supersessions.\n'
         % (REV, CONTRACT_SUCCESSORS, SUPERSESSIONS),
         '## Passage supersessions (law VD2)\n',
         'Each `before` is CRC-1\'s bound `after` for the same parent and selector, and `supersedes` names CRC-1\'s'
         ' record `%s` (%d bytes, `%s`).\n' % (crc1_pin['path'], crc1_pin['bytes'], crc1_pin['sha256'])]
n = 0
for entry in supersessions:
    n += 1
    parts.append('### %d. `%s` %s (supersedes CRC-1)\n' % (n, entry['parent']['path'], selector_text(entry['selector'])))
    parts += ['Before:\n', fence(entry['before']), 'After:\n', fence(entry['after']), 'Changes:\n',
              changes(entry['before'], entry['after'])]
parts.append('## Passage overrides\n')
parts.append('The parent is SYN-1F\'s complete identity-schema copy, the selected IDS. Each `before` is the string'
             ' that copy carries in place, which equals CRC-1\'s `after` on I1-L\'s copy.\n')
for entry in overrides:
    n += 1
    parts.append('### %d. `%s` %s\n' % (n, entry['parent']['path'], selector_text(entry['selector'])))
    parts += ['Before:\n', fence(entry['before']), 'After:\n', fence(entry['after']), 'Changes:\n',
              changes(entry['before'], entry['after'])]
outputs = {D + 'PASSAGES.md': '\n'.join(parts).encode()}


def current(path):
    return outputs[path] if path in outputs else (A / path).read_bytes()


HAND = [D + 'README.md', D + 'evidence/build_crc_2.py', D + 'evidence/check_crc_2.py', D + 'evidence/verify_scratch.py']
GENERATED = [D + 'PASSAGES.md']
candidates = sorted([pin_bytes(p, current(p)) for p in HAND + GENERATED], key=lambda r: r['path'])
for row in candidates:
    assert row['path'] not in accepted, 'candidate reuses an accepted path: ' + row['path']
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED CRC-2 identity contract successor (law M3-C r8 item 9, use 3; M3-H r3 cross-law item X-H3),'
                ' in law VD2\'s form: the core provider closure gains a third admitted use, the producer and enumerator'
                ' of the host-derived records of the three inventory relations (file@enumerated,'
                ' package@manifest-declared, vcs-change@vcs-reported) in every universe, in exactly four fields (the'
                ' enumerator.closureId of a requested inventory cell\'s binding; the host inventory stage\'s'
                ' stage-spec.producerClosure; that stage\'s view.producerClosure, so fact.producerClosure, and'
                ' subject-scope.enumeratorClosure), and is a plan.semanticClosures member exactly when the Plan selects'
                ' a syntax universe or requests an inventory cell. Two contract passage supersessions of CRC-1\'s'
                ' identity-and-evidence overrides (lines 285 and 1377), naming CRC-1\'s record by exact pin; two'
                ' JSON Pointer overrides of SYN-1F\'s selected identity schema copy (closureKinds note,'
                ' closureMembership selectionLaw). No schema shape, kind, domain, recipe, registry, refusal code,'
                ' generated code, inventory or product change. Exact frozen candidate requires actual independent'
                ' review, listing supersededPassages, and root assent.',
    'parents': sorted(parents.values(), key=lambda r: r['path']),
    'passageOverrides': overrides,
    'passageSupersessions': supersessions,
    'candidates': candidates,
}
outputs[D + 'successor.json'] = (json.dumps(record, indent=2, ensure_ascii=False) + '\n').encode()
record_pin = pin_bytes(D + 'successor.json', outputs[D + 'successor.json'])
subject = {'schemaVersion': 1, 'files': sorted(candidates + [record_pin], key=lambda r: r['path'])}
outputs[M + 'crc-2-subject.json'] = (json.dumps(subject, indent=2) + '\n').encode()
subject_pin = pin_bytes(M + 'crc-2-subject.json', outputs[M + 'crc-2-subject.json'])
unit = {
    'schemaVersion': 1,
    'unit': 'snapshot-plan-c-crc-2',
    'status': 'DRAFT-PENDING-REVIEW',
    'subjectManifest': subject_pin,
    'independentReview': {'path': REVIEW, 'bytes': None, 'sha256': None},
    'rootSubstantiveAssent': False,
    'requiredUnitFindings': [],
    'acceptedSuccessor': record_pin,
    'rootAssessment': 'DRAFT (r1). Completed by the lead after CODEX2\'s review: status ACCEPTED-DESIGN-UNIT, the'
                      ' review pin, rootSubstantiveAssent true. CRC-2 carries M3-C r8\'s X-H3 (item 9, use 3): two'
                      ' VD2 contract passage supersessions of CRC-1\'s IE 285 and IE 1377 overrides, and two JSON'
                      ' Pointer overrides of SYN-1F\'s selected identity-schema copy. It binds on the verify_design at'
                      ' product %s on top of %d contract successors, and its review must carry supersededPassages.'
                      ' It binds only after M3-C r8 is accepted.' % (REV, CONTRACT_SUCCESSORS),
    'fullM2Complete': False,
    'productQualification': False,
}
outputs[M + 'crc-2-unit.json'] = (json.dumps(unit, indent=2) + '\n').encode()

if CHECK:
    stale = [p for p, b in outputs.items() if not (A / p).exists() or (A / p).read_bytes() != b]
    print(json.dumps({'check': 'identical' if not stale else 'DIFFERS', 'differs': stale}, indent=1))
    sys.exit(1 if stale else 0)
for path, raw in outputs.items():
    (A / path).write_bytes(raw)
print(json.dumps({'rev': REV, 'contractSuccessors': CONTRACT_SUCCESSORS, 'contractPassageSupersessionsBefore': SUPERSESSIONS,
                  'passageSupersessions': len(supersessions), 'passageOverrides': len(overrides),
                  'parents': len(parents), 'candidates': len(candidates), 'subject': subject_pin,
                  'successor': record_pin,
                  'supersededPassages': [e['supersedes'] for e in supersessions]}, indent=1))
