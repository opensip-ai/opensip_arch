"""Build HSR-1, the identity contract successor of law HSR r1 (historical schema readers), with
PASSAGES.md, the subject manifest and the lead's draft unit record.

Usage: build_hsr_1.py [--product PATH] [--rev REV] [--check]
- PATH is the product checkout (default /Users/sb/code/opensip-ai/opensip), read only. REV (default
  43ea32a, product main) names the commit whose design-lock.json is read with read-only `git show`.
- Without --check every generated file is written. With --check nothing is written: each generated
  file is rebuilt in memory and compared with the bytes on disk.

Deterministic: two runs give identical bytes. Run with python3 -I -B at nice -n 19. It needs the
hand-written README.md and evidence scripts to exist, because the record and the subject pin them.

Generated: hsr-1/PASSAGES.md, hsr-1/successor.json, ../hsr-1-subject.json and ../hsr-1-unit.json
(the unit record is not part of the subject).

The form (README LD-1 to LD-3):
- IE:214 carries I1-L's bound override, so HSR-1 supersedes it in law VD2's form: same parent and
  selector, `before` equal to I1-L's `after`, and `supersedes` naming I1-L's record by exact pin.
- IE:662, IE:678 and IE:808 carry no bound override, so HSR-1 overrides them plainly.
- The two identity-schema strings live in SYN-1F's complete copy, the selected IDS. No bound
  successor overrides them there, so HSR-1 overrides them plainly.
- The historical reader table (IE:808's after) names two rows. Each row's bytes are an accepted
  architecture copy, pinned here by exact digest.
"""
import difflib, hashlib, json, re, subprocess, sys
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
REV = opt('--rev', '43ea32a')
CHECK = '--check' in args
M = 'docs/implementation/m3/syntax-e/hsr/'
D = M + 'hsr-1/'
REVIEW = 'docs/implementation/m3/reviews/grok-hsr-r1/hsr-1/review.json'

IE = 'docs/v2/contracts/product-v1/identity-and-evidence.md'
I1L = 'docs/implementation/m3/preview-pack-i1/i1-l/successor.json'
IDS = 'docs/implementation/m3/syntax-e/syn-1f/design/foundation/identity-schemas.v3.json'
SYN1 = 'docs/implementation/m3/syntax-e/syn-1/successor.json'
SYN1F = 'docs/implementation/m3/syntax-e/syn-1f/successor.json'
LAW = '/x-opensip-payload-registry/law/payloadSchemaDigest'
MAJOR = '/x-opensip-evaluator-profile/majorLaw'

# The closed historical reader table: (row, payload-registry document, $id, accepted architecture
# copy, retiring successor record, that successor's product copy of the same document).
ROWS = [
    ('H1', 'native/native-evidence.schemas.v2.json', 'urn:opensip:product-v1:native:evidence-schemas:v2',
     'docs/implementation/m1/source-selection-v2/schemas/sources/native.v2.schema.json', 'SYN-1', SYN1,
     'docs/implementation/m3/syntax-e/syn-1/product/schemas/sources/native-v2.schema.json'),
    ('H2', 'foundation/enumeration-plan.schema.v1.json', 'opensip.product.enumeration-plan.1',
     'docs/implementation/m2/admission-runtime-selection-v1/schemas/sources/enumeration-plan-v1.schema.json',
     'SYN-1F', SYN1F,
     'docs/implementation/m3/syntax-e/syn-1f/product/schemas/sources/enumeration-plan-v1.schema.json'),
]


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


def refs(doc):
    out = set()
    if isinstance(doc, dict):
        for k, v in doc.items():
            if k == '$ref' and isinstance(v, str):
                out.add(v)
            out |= refs(v)
    elif isinstance(doc, list):
        for v in doc:
            out |= refs(v)
    return out


# --- The lock at REV: accepted paths, bound keys, and each key's current published entry. ------
lock = json.loads(git_show('design-lock.json'))
accepted, bound, records = {}, {}, {}
for key in ('sourceManifest', 'applicationManifest'):
    for row in json.loads(read_pinned(lock['approvals'][key]))['files']:
        accepted[row['path']] = {k: row[k] for k in ('path', 'bytes', 'sha256')}
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
assert copies[-1] == IDS, copies

ie_pin = {k: accepted[IE][k] for k in ('path', 'bytes', 'sha256')}
ie_lines = read_pinned(ie_pin).decode('utf-8').splitlines()
ids_pin = {k: accepted[IDS][k] for k in ('path', 'bytes', 'sha256')}
ids_doc = json.loads(read_pinned(ids_pin))

# --- The historical reader table, verified against accepted bytes. -----------------------------
registry_documents = set()
for body in ids_doc['x-opensip-payload-registry']['classes'].values():
    if 'document' in body:
        registry_documents.add(body['document'])
    for row in body.get('rows', {}).values():
        registry_documents.add(row['document'])
table = []
for name, document, schema_id, copy_path, retired_by, retiring_record, retiring_copy in ROWS:
    assert document in registry_documents, document
    copy_pin = {k: accepted[copy_path][k] for k in ('path', 'bytes', 'sha256')}
    raw = read_pinned(copy_pin)
    doc = json.loads(raw)
    assert doc['$id'] == schema_id, (name, doc.get('$id'))
    assert all(r.startswith('#') for r in refs(doc)), (name, 'external reference')
    # The retiring successor is bound, and its product copy of the same document has other bytes.
    assert retiring_record in records, retiring_record
    new_pin = {k: accepted[retiring_copy][k] for k in ('path', 'bytes', 'sha256')}
    new_doc = json.loads(read_pinned(new_pin))
    assert new_doc['$id'] == schema_id and new_pin['sha256'] != copy_pin['sha256'], name
    assert retiring_copy in [r['path'] for r in records[retiring_record][1]['candidates']], name
    table.append({'row': name, 'document': document, 'schemaId': schema_id, 'sha256': copy_pin['sha256'],
                  'bytes': copy_pin['bytes'], 'copy': copy_path, 'retiredBy': retired_by,
                  'retiringProductCopy': new_pin})

# --- The new text. ------------------------------------------------------------------------------
I1L_LAST = 'Every other schema or domain change keeps this rule.'
SECOND_EXCEPTION = (
    'A second reviewed exception (contract successor HSR-1): contract successors SYN-1 and SYN-1F of law M3-E1'
    ' append the single member `source-parse-error` to the closed `NativeCause` vocabulary of the native evidence'
    ' schemas and of its five foundation copies, under their existing majors and without migration. It adds no other'
    ' member and changes no field, bound, recipe or prefix of any record. The member takes its code-point place in'
    ' each list, and no record names a list position. No record admitted before those successors carries the member.'
    ' Unlike the first exception, this one changes the exact bytes of two documents that retained records name by'
    ' digest: `native/native-evidence.schemas.v2.json` and `foundation/enumeration-plan.schema.v1.json`. Their'
    ' earlier selected bytes stay readable as historical schema readers (HSR-1, at the end of the payload registry'
    ' section below). So here too every existing record keeps its bytes, identity, validity and replay result.'
    ' Every other schema or domain change keeps this rule. A later reviewed exception that changes the bytes of a'
    ' document a retained record names by digest adds exactly one historical schema reader for that document, by'
    ' its own successor.')
IE662_OLD = '  document the row names** — never a canonicalization of a selected `$def`;'
IE662_NEW = (
    '  document the row names** — never a canonicalization of a selected `$def`. Those bytes are the'
    ' document\'s selected current bytes or, for a retained record only, the bytes of one of its historical schema'
    ' readers (contract successor HSR-1, at the end of this section);')
IE678_PAIRS = [(
    'Each member is the raw SHA-256 of the exact full bytes of a document on the closed registry above; a member'
    ' naming anything else refuses (`SCHEMA_DOCUMENT_UNREGISTERED`).',
    'Each member is the raw SHA-256 of the exact full bytes of a document on the closed registry above. Those are'
    ' the document\'s selected current bytes or, in a retained view only, the bytes of one of its historical schema'
    ' readers (contract successor HSR-1, at the end of this section). A member naming anything else refuses'
    ' (`SCHEMA_DOCUMENT_UNREGISTERED`).')]
IE808_OLD = 'policy over that extent.'


def table_lines():
    out = ['| Row | Document | `$id` | sha256 | Bytes | Accepted architecture copy | Retired by |',
           '|---|---|---|---|---|---|---|']
    for t in table:
        out.append('| %s | `%s` | `%s` | `%s` | %d | `%s` | %s |' % (
            t['row'], t['document'], t['schemaId'], t['sha256'], t['bytes'], t['copy'], t['retiredBy']))
    return '\n'.join(out)


HSR_SECTION = '\n'.join([
    '### Historical schema readers (contract successor HSR-1, 2026-10-04)',
    '',
    'A retained record names the schema document it was admitted under by the raw SHA-256 of that document\'s'
    ' exact bytes. It does so through a `payloadSchemaDigest`, an analysis-spec or stage-spec parameter\'s'
    ' `schemaDigest`, a `view.schemaDigests` member or a `schema` proof-input-ref, and each such document is named by'
    ' a row of the payload registry above. A stage-spec\'s `outputSchemaDigest` names a member of its producer'
    ' closure\'s tree instead, and a new output schema is a new closure (below). A reviewed exception to the major'
    ' rule of section 3 may change a registry document\'s selected bytes under its existing major. A record admitted'
    ' before that change still names the earlier bytes. A **historical schema reader** reads it: the earlier'
    ' selected bytes of the same document, kept and named by their exact digest.',
    '',
    '**The closed table.** These are all the historical schema readers. Each row is one earlier selected version of'
    ' one registry document. Its reference closure is its own bytes, and its accepted architecture copy holds'
    ' exactly those bytes.',
    '',
    table_lines(),
    '',
    '**Minting.** A boundary that creates a record names the selected current bytes of each document, and only'
    ' those. The host chooses the digest: a caller may restate it but never choose it. This holds at'
    ' `admit_coverage_result_v3` (native-evidence section 4, step 6), at import admission, at pre-Plan'
    ' analysis-spec admission, at view production and at every other boundary that creates a record. A historical'
    ' digest there refuses with the boundary\'s existing refusal for an unregistered document.',
    '',
    '**Retained records.** Retained closure, replay, Run closure and every later check of a retained record admit'
    ' the record\'s carried digest when it is either the selected current digest of the document its payload'
    ' registry row names, or the digest of a table row for that document.',
    '- The record is validated against exactly the bytes its digest names, through the payload registry row\'s'
    ' selector. Every digest annotation and reference of that document is read from the same bytes. A reader never'
    ' mixes the bytes of two versions.',
    '- The store still retains those schema bytes under that digest. A compiled-in reader never stands in for'
    ' missing retained bytes: their absence stays retention loss.',
    '- A check that re-applies a producer\'s admission law to a retained record, such as the Coverage producer law'
    ' that Run closure re-runs over retained Coverage, is a retained check. There, "the registered document" is the'
    ' document version the record\'s own digest names.',
    '- A digest resolves to its document before any registry row, key or cardinality rule applies. A current and a'
    ' historical digest of one document therefore cite one row, and two parameters of one spec citing them refuse'
    ' under the one-per-row rule above.',
    '- No other digest is admitted. A schema `$id`, URI, major or version alone never selects a reader, and no'
    ' caller, store, environment or configuration adds one.',
    '',
    '**One reader per digest.** Every digest in the selected registry and in this table names exactly one document.'
    ' A row whose digest is still its document\'s selected current digest in an implementation, because that'
    ' implementation has not yet selected the retiring successor\'s bytes, is read there by the current reader. It'
    ' is never a second reader of the same bytes.',
    '',
    '**Identity.** Nothing is re-minted. A historical record keeps its stored identifiers: its `coverage2`,'
    ' `import2` and `fact2` identities, its Plan\'s `analysisSpecDigest` and PlanId, and every identity above'
    ' them. Their descriptors carry the historical digest, so recomputing them from retained bytes gives the stored'
    ' values. The same payload admitted now under the current bytes is a different record with a different'
    ' identity, and the two are never equated. `finding-key2` names no schema digest, so findings still'
    ' correspond across the change.',
    '',
    '**Mixed stores and Runs.** Each record is read by the digest it carries. One store may hold records of both'
    ' readers, and so may one Run: a Plan created after the change may select an import retained before it. Replay,'
    ' Run closure and comparison need no mode, flag or per-store setting.',
    '',
    '**Verification.** A record admitted by a historical reader is admitted, and no defect, field, code or class is'
    ' added for it. A record whose digest is neither current nor in this table refuses with its existing refusal.'
    ' Every verification surface reports replay\'s result.',
    '',
    '**Extension.** The table changes only by a reviewed contract successor that supersedes this passage in law'
    ' VD2\'s form. A successor that changes the selected bytes of a document named by the payload registry adds'
    ' exactly one row for that document: the digest it retires, its bytes, its accepted architecture copy and the'
    ' successor\'s name. No row is ever removed or edited, and nothing else adds one. This table keeps records that'
    ' name a document by digest readable. A record that names no schema digest is read against the current bytes,'
    ' so an exception that is not purely additive still needs a new major and a reviewed migration (section 3).',
])
IE808_NEW = IE808_OLD + '\n\n' + HSR_SECTION

LAW_OLD = 'raw SHA-256 of the EXACT FULL schema DOCUMENT file bytes named by the row'
LAW_NEW = (
    'raw SHA-256 of the EXACT FULL schema DOCUMENT file bytes named by the row: the document\'s selected current'
    ' bytes or, for a retained record only, the bytes of one of its historical schema readers in the closed table of'
    ' identity-and-evidence section 3 (contract successor HSR-1). A boundary that creates a record names the current'
    ' bytes only. A cited digest resolves to its document, through the current bytes and that table, before any'
    ' row, key or cardinality rule applies.')
MAJOR_ADD = (
    ' The single additive NativeCause member source-parse-error, authorized by identity-and-evidence section 3\'s'
    ' second reviewed exception (contract successors SYN-1, SYN-1F and HSR-1), keeps every identifier major as well.'
    ' Retained records that name the earlier native evidence or enumeration plan schema bytes by digest are read by'
    ' HSR-1\'s historical schema readers and keep their identifiers.')

# --- Entries. -----------------------------------------------------------------------------------
parents = {IE: ie_pin, IDS: ids_pin}
i1l_pin, i1l = records[I1L]
key214 = (IE, json.dumps({'line': 214}, sort_keys=True))
owner, target = bound[key214]
# The current meaning of IE:214 is I1-L's override: no later record supersedes it.
assert owner == i1l_pin and 'supersedes' not in target, owner
assert target in i1l['passageOverrides'] and target['parent'] == ie_pin
assert ie_lines[213] == target['before']
before214 = target['after']
assert before214.endswith(I1L_LAST) and before214.count(I1L_LAST) == 1
after214 = before214[:-len(I1L_LAST)] + SECOND_EXCEPTION
supersessions = [{'parent': ie_pin, 'selector': {'line': 214}, 'before': before214, 'after': after214,
                  'supersedes': {'record': i1l_pin, 'parent': ie_pin, 'selector': {'line': 214}}}]

overrides = []
for line, new in ((662, None), (678, None), (808, None)):
    key = (IE, json.dumps({'line': line}, sort_keys=True))
    assert key not in bound, ('already overridden', key)
    raw = ie_lines[line - 1]
    if line == 662:
        assert raw == IE662_OLD, raw
        after = IE662_NEW
    elif line == 678:
        after = edit(raw, IE678_PAIRS)
    else:
        assert raw == IE808_OLD and ie_lines[line] == '' and ie_lines[line + 1].startswith('### `fact2` payload encoding')
        after = IE808_NEW
    overrides.append({'parent': ie_pin, 'selector': {'line': line}, 'before': raw, 'after': after})
for pointer, make in ((LAW, lambda b: edit(b, [(LAW_OLD, LAW_NEW)])), (MAJOR, lambda b: b + MAJOR_ADD)):
    key = (IDS, json.dumps({'jsonPointer': pointer}, sort_keys=True))
    assert key not in bound, ('already overridden', key)
    before = resolve(ids_doc, pointer)
    assert isinstance(before, str)
    overrides.append({'parent': ids_pin, 'selector': {'jsonPointer': pointer}, 'before': before, 'after': make(before)})

for entry in supersessions + overrides:
    assert entry['after'].count('—') == entry['before'].count('—'), 'em dash in new text'
    assert entry['after'] != entry['before']


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


parts = ['# HSR-1 passages (generated)\n',
         'Generated by `evidence/build_hsr_1.py` from the same data as `successor.json`; do not edit by hand. Each'
         ' entry gives the parent, the selector, the exact `before` and the candidate `after`, then the word-level'
         ' changes. Product lock: `%s`, %d contract successors, %d contract passage supersessions.\n'
         % (REV, CONTRACT_SUCCESSORS, SUPERSESSIONS),
         '## Passage supersession (law VD2)\n',
         'The `before` is I1-L\'s bound `after` for the same parent and selector, and `supersedes` names I1-L\'s'
         ' record `%s` (%d bytes, `%s`).\n' % (i1l_pin['path'], i1l_pin['bytes'], i1l_pin['sha256'])]
n = 0
for entry in supersessions:
    n += 1
    parts.append('### %d. `%s` %s (supersedes I1-L)\n' % (n, entry['parent']['path'], selector_text(entry['selector'])))
    parts += ['Before:\n', fence(entry['before']), 'After:\n', fence(entry['after']), 'Changes:\n',
              changes(entry['before'], entry['after'])]
parts.append('## Passage overrides\n')
parts.append('IE\'s three lines carry no bound override. The identity-schema parent is SYN-1F\'s complete copy, the'
             ' selected IDS, and no bound record overrides either pointer there. Each `before` is the raw passage.\n')
for entry in overrides:
    n += 1
    parts.append('### %d. `%s` %s\n' % (n, entry['parent']['path'], selector_text(entry['selector'])))
    parts += ['Before:\n', fence(entry['before']), 'After:\n', fence(entry['after']), 'Changes:\n',
              changes(entry['before'], entry['after'])]
parts.append('## The historical reader table, verified\n')
parts.append('Each row\'s accepted architecture copy is in the product lock\'s accepted set with exactly these pins.'
             ' Its `$id` is the row\'s, it holds no external reference, and the retiring successor\'s product copy of'
             ' the same document has other bytes.\n')
parts.append('| Row | Document | Historical copy (bytes, sha256) | Retiring product copy (bytes, sha256) |\n|---|---|---|---|')
for t in table:
    parts.append('| %s | `%s` | %d, `%s` | %d, `%s` |' % (t['row'], t['document'], t['bytes'], t['sha256'],
                                                        t['retiringProductCopy']['bytes'],
                                                        t['retiringProductCopy']['sha256']))
parts.append('')
outputs = {D + 'PASSAGES.md': '\n'.join(parts).encode()}


def current(path):
    return outputs[path] if path in outputs else (A / path).read_bytes()


HAND = [D + 'README.md', D + 'evidence/build_hsr_1.py', D + 'evidence/check_hsr_1.py', D + 'evidence/verify_scratch.py']
GENERATED = [D + 'PASSAGES.md']
candidates = sorted([pin_bytes(p, current(p)) for p in HAND + GENERATED], key=lambda r: r['path'])
for row in candidates:
    assert row['path'] not in accepted, 'candidate reuses an accepted path: ' + row['path']
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED HSR-1 identity contract successor (law HSR r1, historical schema readers), in law VD2\'s'
                ' form: a retained record that names a payload-registry schema document by digest is admitted'
                ' against exactly the bytes that digest names, either the document\'s selected current bytes or one'
                ' row of a closed historical reader table in identity-and-evidence section 3 (H1: the native'
                ' evidence schemas at e5834d37..., retired by SYN-1; H2: the enumeration plan schema at'
                ' 10627cb6..., retired by SYN-1F); a boundary that creates a record names the current bytes only;'
                ' nothing is re-minted; the table is extended only by a successor that supersedes it, one row per'
                ' retired digest. One contract passage supersession of I1-L\'s identity-and-evidence line 214'
                ' override (the second reviewed exception to the major rule, for SYN-1 and SYN-1F), naming I1-L\'s'
                ' record by exact pin; three plain identity-and-evidence line overrides (662, 678, 808); two JSON'
                ' Pointer overrides of SYN-1F\'s selected identity schema copy (payload registry law, evaluator'
                ' profile major law). No schema shape, kind, domain, recipe, registry, refusal code, generated code,'
                ' inventory or product change. Exact frozen candidate requires actual independent review, listing'
                ' supersededPassages, and root assent.',
    'parents': sorted(parents.values(), key=lambda r: r['path']),
    'passageOverrides': overrides,
    'passageSupersessions': supersessions,
    'candidates': candidates,
}
outputs[D + 'successor.json'] = (json.dumps(record, indent=2, ensure_ascii=False) + '\n').encode()
record_pin = pin_bytes(D + 'successor.json', outputs[D + 'successor.json'])
subject = {'schemaVersion': 1, 'files': sorted(candidates + [record_pin], key=lambda r: r['path'])}
outputs[M + 'hsr-1-subject.json'] = (json.dumps(subject, indent=2) + '\n').encode()
subject_pin = pin_bytes(M + 'hsr-1-subject.json', outputs[M + 'hsr-1-subject.json'])
unit = {
    'schemaVersion': 1,
    'unit': 'syntax-e-hsr-1',
    'status': 'DRAFT-PENDING-REVIEW',
    'subjectManifest': subject_pin,
    'independentReview': {'path': REVIEW, 'bytes': None, 'sha256': None},
    'rootSubstantiveAssent': False,
    'requiredUnitFindings': [],
    'acceptedSuccessor': record_pin,
    'rootAssessment': 'DRAFT (r1). Completed by the lead after Grok\'s review: status ACCEPTED-DESIGN-UNIT, the'
                      ' review pin, rootSubstantiveAssent true. HSR-1 carries law HSR r1\'s historical schema'
                      ' readers: one VD2 contract passage supersession of I1-L\'s IE 214 override, three plain IE'
                      ' line overrides (662, 678, 808) and two JSON Pointer overrides of SYN-1F\'s selected'
                      ' identity-schema copy. It binds on the verify_design at product %s on top of %d contract'
                      ' successors, and its review must carry supersededPassages. It binds only after law HSR r1'
                      ' is accepted, in a binding-only product commit before unit HSR-a.' % (REV, CONTRACT_SUCCESSORS),
    'fullM2Complete': False,
    'productQualification': False,
}
outputs[M + 'hsr-1-unit.json'] = (json.dumps(unit, indent=2) + '\n').encode()

if CHECK:
    stale = [p for p, b in outputs.items() if not (A / p).exists() or (A / p).read_bytes() != b]
    print(json.dumps({'check': 'identical' if not stale else 'DIFFERS', 'differs': stale}, indent=1))
    sys.exit(1 if stale else 0)
for path, raw in outputs.items():
    (A / path).write_bytes(raw)
print(json.dumps({'rev': REV, 'contractSuccessors': CONTRACT_SUCCESSORS, 'contractPassageSupersessionsBefore': SUPERSESSIONS,
                  'passageSupersessions': len(supersessions), 'passageOverrides': len(overrides),
                  'parents': len(parents), 'candidates': len(candidates), 'subject': subject_pin,
                  'successor': record_pin, 'table': [{k: t[k] for k in ('row', 'document', 'sha256', 'bytes')} for t in table],
                  'supersededPassages': [e['supersedes'] for e in supersessions]}, indent=1))
