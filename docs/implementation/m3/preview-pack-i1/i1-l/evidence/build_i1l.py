"""Build contract successor I1-L deterministically, and check it without the product's tools.

Writes, under docs/implementation/m3/preview-pack-i1/:
  i1-l/design/foundation/identity-schemas.v3.json          (IDS successor copy)
  i1-l/design/workflows/schemas/policy-document.v2.schema.json  (PDS successor copy)
  i1-l/product/schemas/sources/identity-v3.schema.json     (product IDS source copy)
  i1-l/product/schemas/sources/policy-v2.schema.json       (product PDS source copy)
  i1-l/atom-section-4a.md, i1-l/materialization-map.json, i1-l/evidence/copies-report.json,
  i1-l/successor.json and i1-l-subject.json.

Each JSON copy is its parent's raw bytes with (1) every passage override the product lock binds
to that parent applied in place, so the copy carries the parent's accepted meaning, and (2) I1's
edits: "cycle-representative" appended at the end of each closed operation enum (no existing
member moves), the IDS majorLaw sentence, and the PDS description's predicate list.

The checks restate tools/verify_design.py's contract_successor and successor_chain rules for this
record: accepted parents, exact before texts, JSON Pointer selectors on JSON parents, no selector
already overridden, candidates equal to the subject minus the record, and fresh candidate paths.

Usage (read-only on the product; git is used only to read the base blobs):
    python3.14 -I -B evidence/build_i1l.py --product /path/to/opensip [--check]
--check rebuilds in memory and compares with the files on disk instead of writing.
"""
from __future__ import annotations

import argparse
import difflib
import hashlib
import json
import subprocess
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCH = HERE.parents[5]
BASE = 'docs/implementation/m3/preview-pack-i1'
UNIT = f'{BASE}/i1-l'
PRODUCT_HEAD = '3e64266aa8729160cd22509dcfff95a3bb09fcea'
LAW = f'{BASE}/PROPOSAL-r2.md'
LAW_SHA256 = '1eb47d1e292660b15cb0016a280899a384364f2c3d99ab61d18f12b133eba2c7'
UNITS_LAW = f'{BASE}/UNITS-r2.md'
UNITS_SHA256 = '0c3c0f44d61a64813b2e1156e8ecb0b97adeeecbd48149a00bf77a8c8950e785'

WS = 'docs/v2/contracts/product-v1/workflows-and-surfaces.md'
WSE = 'docs/implementation/m1/source-selection-v2/reference/effective-workflows-and-surfaces.md'
IE = 'docs/v2/contracts/product-v1/identity-and-evidence.md'
COMP = 'docs/coop/design-corrections/foundation/evaluator-composition-contract.v3.md'
ATOM = 'docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md'
IDS = 'docs/coop/design-corrections/foundation/identity-schemas.v3.json'
PDS = 'docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json'
PIDS = 'docs/implementation/m1/source-selection-v2/schemas/sources/identity.v3.schema.json'
PPDS = 'docs/implementation/m1/source-selection-v2/schemas/sources/policy.v2.schema.json'

COPIES = {  # parent -> (copy path, product path or None)
    IDS: (f'{UNIT}/design/foundation/identity-schemas.v3.json', None),
    PDS: (f'{UNIT}/design/workflows/schemas/policy-document.v2.schema.json', None),
    PIDS: (f'{UNIT}/product/schemas/sources/identity-v3.schema.json', 'schemas/sources/identity-v3.schema.json'),
    PPDS: (f'{UNIT}/product/schemas/sources/policy-v2.schema.json', 'schemas/sources/policy-v2.schema.json'),
}
# The bound overrides each JSON parent carries in the product lock at PRODUCT_HEAD (asserted).
BOUND = {
    IDS: {'/$defs/program-predicate/description': 'predicate-matching-reference-selection-v2',
          '/$defs/stage-spec/properties/outputSchemaDigest/x-opensip-digest/registeredBy/law':
              'stage-meta-reference-selection-v1',
          '/$defs/closure/properties/manifestDigest/x-opensip-digest/artifact': 'core-evaluator-closure-ec1',
          '/x-opensip-digest-domains/closureKinds/note': 'core-evaluator-closure-ec1'},
    PIDS: {'/$defs/program-predicate/description': 'predicate-matching-reference-selection-v2',
           '/$defs/stage-spec/properties/outputSchemaDigest/x-opensip-digest/registeredBy/law':
               'stage-meta-reference-selection-v1'},
    PDS: {}, PPDS: {},
}
ENUMS = {IDS: ['/$defs/proof-bundle/properties/predicateProofs/items/properties/operation/enum',
               '/$defs/program-predicate/properties/operation/enum'],
         PIDS: ['/$defs/proof-bundle/properties/predicateProofs/items/properties/operation/enum',
                '/$defs/program-predicate/properties/operation/enum'],
         PDS: ['/$defs/Atom/properties/op/enum', '/$defs/AtomSuccessorV1/properties/op/enum'],
         PPDS: ['/$defs/Atom/properties/op/enum']}
MEMBER = 'cycle-representative'
MAJOR_LAW = '/x-opensip-evaluator-profile/majorLaw'
MAJOR_LAW_APPEND = (" The single additive operation member authorized by identity-and-evidence §3's "
                    "reviewed M3-I1 exception keeps proof3 and the program-predicate schemaVersion; "
                    "it is not a permissive mixed-version parse.")
DESCRIPTION_OLD = '(exists, none, count-at-most, all-covered, and, or, not)'
DESCRIPTION_NEW = ('(exists, none, count-at-most, all-covered, and, or, not; the graph atom '
                   'cycle-representative of atom contract §4a is admitted only as a rule\'s whole emitWhen)')

# Text passages: (parent, line, anchor, insertion). The insertion goes right after the anchor,
# which must occur exactly once in the line; None as anchor appends to the line.
WS598 = (", the graph atom `cycle-representative` (only as a rule's whole `emitWhen`, only over "
         "`imports` at `resolved-target` with no filters, only for subject kind `file`)")
WS603 = ("; `cycle-representative` is true for the least-path file of a cyclic component of the "
         "admitted resolved project import graph, false for its other files, and otherwise false "
         "only under complete graph Coverage, else indeterminate (atom contract §4a)")
IE214 = (" One reviewed exception: the M3-I1 successor appends the single member "
         "`cycle-representative` to the closed `operation` vocabularies of proof-bundle "
         "`predicateProofs[]` and of `program-predicate`, under their existing majors and without "
         "migration. It changes no other field, member, bound, order, recipe or prefix. No record "
         "admitted before that successor can carry the member, because the member becomes "
         "admissible in a policy only through the same successor. So every existing record keeps "
         "its bytes, identity, validity and replay result, and `finding-key2`, whose descriptor "
         "names no operation, is unaffected. A reader that selects the successor's schema bytes "
         "admits records with or without the member under the same majors. A reader that does not "
         "refuses the member as a schema mismatch and never coerces, ignores or drops it. Every "
         "other schema or domain change keeps this rule.")
IE1266 = " (or `cycle-representative`, under the reviewed M3-I1 exception above)"
IE1334 = " (eight, with the reviewed M3-I1 exception's `cycle-representative`)"
IE1544 = ("\n| cycle-representative | true at the representative (least path) of a known cyclic "
          "component of the admitted resolved import graph; false at the component's other members; "
          "elsewhere false only under complete graph Coverage with no uncertain edge (atom contract "
          "§4a) | indeterminate |")
COMP34 = (" `cycle-representative` with a known cyclic component is true at its representative and "
          "false at the component's other members (atom contract §4a).")
COMP109 = " / `cycle-representative`"
TEXT = [
    (WS, 598, '`exists|none|count-at-most|all-covered`', WS598, 'law item 4'),
    (WS, 603, '`all-covered` indeterminate', WS603, 'law item 4 (603-604: only 603 changes)'),
    (WSE, 602, '`exists|none|count-at-most|all-covered`', WS598, 'effective copy of WS:598'),
    (WSE, 607, '`all-covered` indeterminate', WS603, 'effective copy of WS:603'),
    (IE, 214, 'not a permissive parser.', IE214, 'law item 4 (213-214: only 214 changes)'),
    (IE, 1266, 'one of the seven evaluator predicates', IE1266, 'consequential (seven no longer closes it)'),
    (IE, 1334, 'whose seven evaluator', IE1334, 'consequential (seven no longer closes it)'),
    (IE, 1544, None, IE1544, 'consequential (the section 4 predicate table gains its row)'),
    (COMP, 34, None, COMP34, 'law item 4'),
    (COMP, 109, '`all-covered`', COMP109, 'consequential (the atomic-node list of section 9.2)'),
    (ATOM, 366, None, None, 'law item 4: new section 4a'),
]

SECTION_HEADER = '## 4a. `cycle-representative`, the graph atom (contract successor M3-I1-L)'
SECTION_PREAMBLE = (
    'This section is added by contract successor I1-L (`docs/implementation/m3/preview-pack-i1/i1-l/`). '
    'Its body is items 2.1 to 2.9 of law M3-I1 r2 (`docs/implementation/m3/preview-pack-i1/PROPOSAL-r2.md`, '
    f'sha256 `{LAW_SHA256}`, accepted by CODEX2 on 2026-10-04), verbatim. In that text, "item N" names an '
    'item of that law; "r2", "I1-RF-n" and "I1-NB-n" name its review history; the short names (AQC, ATOM, '
    'COMP, ENUM, EPLAN, EXI, FAULT, IE, NE, PAC, PDS, QP, RA, REG, RPS, SIS, WS, X12) are those of its '
    'Short names table, and ATOM is this contract; line citations are to the files, and product paths to '
    'product main 2967905, as that law checked them. The precisions P0 to P7 after the verbatim text are the successor\'s own: they fix choices the '
    'verbatim text leaves open, and change none of it. The reference model is '
    '`docs/implementation/m3/preview-pack-i1/i1-l/evidence/cycle_representative_model.py`; '
    '`evidence/check_cycle_representative.py` beside it runs the discriminating cases.')
SECTION_PRECISIONS = '\n'.join([
    '**Successor precisions (I1-L).**',
    '- **P0. Where it is evaluated.** This atom is evaluated once per rule, over the rule\'s whole selected '
    'population (item 2.3), never by \u00a78\'s per-subject `evaluate_atom`. \u00a7\u00a75 to 9 do not apply '
    'to it, except \u00a77\'s cause registry and its retention of uncertain ids.',
    '- **P1. Cause universes on uncertain edges.** `target-kind-unknown` carries the fact\'s '
    '`targetUniverse`. An unplaceable target carries `population-unknown` with the fact\'s `targetUniverse`; '
    'an importer with no unique row carries `population-unknown` with the fact\'s `sourceUniverse`. An '
    'uncertain edge carries every cause that applies to it, its importer\'s and its target\'s.',
    '- **P2. Order and accumulation of 2.5.** The shared prelude runs once, and its P2 return '
    '(`missing-relation-coverage`) is the only return of the whole computation. The universes of V are '
    'then accounted in ascending UTF-8 order of their identifiers, each in full, with no return across '
    'universes. In a universe with no available owed binding, outgoing step 1\'s `selector-unbound` ends '
    'that universe\'s account. Within a universe, every exact scope is cited in `scopeIds`, every unpaired '
    'scope emits `scope-without-coverage`, and every paired Coverage is evaluated: outgoing step 3\'s '
    'return is not taken. `scopeIds` and `coverageIds` follow \u00a74\'s selection order.',
    '- **P3. Unique rows.** The exact-id lookup of item 2.3 reads every retained `symbol` inventory of the '
    'universe. Byte-identical `(nativeSubjectId, path)` observations count once; one `nativeSubjectId` at '
    'two paths has no unique row.',
    '- **P4. Unplaced unresolved edges.** An `imports` unresolved-edge fact whose referrer maps to no '
    'selected vertex is in no witness. It bears on the value only through 2.5(c), whose Coverage RC-2 '
    'already counts it (NE:2113-2117).',
    '- **P5. Census carriers.** The census\'s `population-unknown` and `uncovered-expected-source-subject` '
    'carry `nativeCause` null, as incoming\'s do. An incomplete inventory\'s own typed carrier stays on that '
    'retained inventory, which every atomic node cites through `inputRefs` = EI (composition \u00a79.2).',
    '- **P6. Member order.** The finding\'s member list is sorted by item 2.3\'s representative order: path '
    'bytes, then universe bytes.',
    '- **P7. The sufficiency answer.** 2.5(c)\'s view is the native owner\'s `sufficiency_v2` answer under '
    'the fixed requirement stated there. The atom neither recomputes it nor accepts an answer computed '
    'under another requirement. An unsatisfied answer\'s `DeficiencyV2` values are the result\'s '
    '`nativeDeficiencies`.',
])


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def pin(path, raw):
    return {'path': path, 'bytes': len(raw), 'sha256': sha(raw)}


def read(path):
    return (ARCH / path).read_bytes()


def dumps(value):
    return (json.dumps(value, indent=2, ensure_ascii=True) + '\n').encode('ascii')


def pointer_get(doc, pointer):
    for token in pointer[1:].split('/'):
        token = token.replace('~1', '/').replace('~0', '~')
        doc = doc[int(token)] if isinstance(doc, list) else doc[token]
    return doc


def pointer_set(doc, pointer, value):
    parts = pointer[1:].split('/')
    parent = pointer_get(doc, '/' + '/'.join(parts[:-1])) if len(parts) > 1 else doc
    parent[parts[-1].replace('~1', '/').replace('~0', '~')] = value


def lock_state(product):
    lock = json.loads((product / 'design-lock.json').read_bytes())
    accepted = {}
    for name in ('sourceManifest', 'applicationManifest'):
        for row in json.loads(read(lock['approvals'][name]['path']))['files']:
            accepted[row['path']] = row
    for binding in lock['inventorySuccessors']:
        accepted[binding['parent']['path']] = binding['parent']
        accepted[binding['candidate']['path']] = binding['candidate']
    bound = {}
    for binding in lock['contractSuccessors']:
        record = json.loads(read(binding['record']['path']))
        accepted[binding['record']['path']] = binding['record']
        for row in record['candidates']:
            accepted[row['path']] = row
        name = binding['record']['path'].split('/')[-2]
        for entry in record.get('passageOverrides', []) + record.get('passageSupersessions', []):
            bound.setdefault(entry['parent']['path'], []).append((name, entry))
    return lock, accepted, bound


def json_copy(parent, bound):
    """Return (copy bytes, report) for one JSON parent."""
    raw = read(parent)
    text = raw.decode('ascii')
    expected = json.loads(raw)
    applied = []
    have = {entry['selector'].get('jsonPointer'): (name, entry) for name, entry in bound.get(parent, [])}
    if {k: v[0] for k, v in have.items()} != BOUND[parent]:
        raise SystemExit(f'bound overrides on {parent} differ from the reviewed set: {sorted(have)}')
    for pointer, (name, entry) in sorted(have.items()):
        old, new = json.dumps(entry['before']), json.dumps(entry['after'])
        if text.count(old) != 1 or pointer_get(expected, pointer) != entry['before']:
            raise SystemExit(f'cannot place bound override {pointer} in {parent}')
        text = text.replace(old, new)
        pointer_set(expected, pointer, entry['after'])
        applied.append({'record': name, 'jsonPointer': pointer})
    lines = text.split('\n')
    edits = []
    for pointer in ENUMS[parent]:
        # Enums are written one member per line after '"enum": ['. The pointers are listed in
        # document order, and an edited enum no longer matches, so the first match is this one.
        # The structural comparison below proves the edit landed at the pointer.
        members = pointer_get(expected, pointer)
        want = [json.dumps(m) for m in members]
        hits = [i for i, line in enumerate(lines) if line.strip() == '"enum": ['
                and [l.strip().rstrip(',') for l in lines[i + 1:i + 1 + len(members)]] == want
                and lines[i + 1 + len(members)].strip().startswith(']')]
        if not hits:
            raise SystemExit(f'cannot place {pointer} in {parent}')
        last = hits[0] + len(members)
        indent = lines[last][:len(lines[last]) - len(lines[last].lstrip())]
        lines[last] = lines[last] + ','
        lines.insert(last + 1, indent + json.dumps(MEMBER))
        members.append(MEMBER)
        edits.append({'jsonPointer': pointer, 'newMemberLine': last + 2})
    text = '\n'.join(lines)
    if parent in (IDS, PIDS):
        old = pointer_get(expected, MAJOR_LAW)
        new = old + MAJOR_LAW_APPEND
        if text.count(json.dumps(old)) != 1:
            raise SystemExit('cannot place majorLaw')
        text = text.replace(json.dumps(old), json.dumps(new))
        pointer_set(expected, MAJOR_LAW, new)
        edits.append({'jsonPointer': MAJOR_LAW,
                      'line': next(n for n, l in enumerate(text.split('\n'), 1) if l.lstrip().startswith('"majorLaw"'))})
    else:
        old = expected['description']
        if old.count(DESCRIPTION_OLD) != 1:
            raise SystemExit('cannot place the description edit')
        new = old.replace(DESCRIPTION_OLD, DESCRIPTION_NEW)
        if text.count(json.dumps(old)) != 1:
            raise SystemExit('cannot place the description')
        text = text.replace(json.dumps(old), json.dumps(new))
        expected['description'] = new
        edits.append({'jsonPointer': '/description', 'line': 5})
    out = text.encode('ascii')
    if json.loads(out) != expected:
        raise SystemExit(f'{parent}: copy does not parse to the expected document')
    hunks = [{'parentLines': [i1 + 1, i2], 'copyLines': [j1 + 1, j2]} for tag, i1, i2, j1, j2 in
             difflib.SequenceMatcher(None, raw.decode().split('\n'), text.split('\n'), autojunk=False).get_opcodes()
             if tag != 'equal']
    return out, {'parent': pin(parent, raw), 'copy': pin(COPIES[parent][0], out),
                 'boundOverridesCarried': applied, 'i1Edits': edits, 'hunks': hunks}


def section_4a():
    law = read(LAW)
    if sha(law) != LAW_SHA256:
        raise SystemExit('law bytes changed')
    lines = law.decode('utf-8').split('\n')
    if not lines[87].startswith('**2.1 Syntax.**') or not lines[220].startswith('**2.9 The algorithm is free.**'):
        raise SystemExit('items 2.1 to 2.9 are not at law lines 88 to 221')
    verbatim = '\n'.join(lines[87:221])
    return '\n\n'.join([SECTION_HEADER, SECTION_PREAMBLE, verbatim, SECTION_PRECISIONS]), verbatim


def overrides(section):
    out = []
    for parent, line, anchor, insertion, _why in TEXT:
        raw = read(parent)
        before = raw.decode('utf-8').splitlines()[line - 1]
        if parent == ATOM:
            after = before + '\n\n---\n\n' + section
        elif anchor is None:
            after = before + insertion
        else:
            if before.count(anchor) != 1:
                raise SystemExit(f'anchor not unique at {parent}:{line}')
            cut = before.index(anchor) + len(anchor)
            after = before[:cut] + insertion + before[cut:]
        out.append({'parent': pin(parent, raw), 'selector': {'line': line}, 'before': before, 'after': after})
    return out


def check(record, subject, files, accepted, bound, lock):
    """verify_design's contract_successor / successor_chain rules for this one record."""
    members = subject['files']
    paths = [row['path'] for row in members]
    assert paths == sorted(set(paths)), 'subject paths must be sorted and unique'
    record_path = f'{UNIT}/successor.json'
    assert {r['path'] for r in record['candidates']} == set(paths) - {record_path}
    for row in members:
        assert pin(row['path'], files[row['path']]) == row
        assert row['path'] not in accepted, f'candidate reuses an accepted path: {row["path"]}'
    parents = record['parents']
    assert [p['path'] for p in parents] == sorted({p['path'] for p in parents}) and parents
    for row in parents:
        assert accepted.get(row['path'], {}).get('sha256') == row['sha256'], row['path']
        assert accepted[row['path']]['bytes'] == row['bytes']
        assert pin(row['path'], read(row['path'])) == row
        assert row['path'] not in paths
    parent_map = {p['path']: p for p in parents}
    seen = set()
    for entry in record['passageOverrides']:
        assert set(entry) == {'parent', 'selector', 'before', 'after'}
        assert parent_map.get(entry['parent']['path']) == entry['parent']
        key = (entry['parent']['path'], json.dumps(entry['selector'], sort_keys=True))
        assert key not in seen
        seen.add(key)
        assert isinstance(entry['after'], str) and entry['after'] and entry['before'] != entry['after']
        raw = read(entry['parent']['path'])
        assert set(entry['selector']) == {'line'}
        assert raw.decode('utf-8').splitlines()[entry['selector']['line'] - 1] == entry['before']
        try:
            json.loads(raw)
        except ValueError:
            pass
        else:
            raise AssertionError('v4 JSON parent passages require JSON Pointer selectors')
        for name, other in bound.get(entry['parent']['path'], []):
            assert json.dumps(other['selector'], sort_keys=True) != key[1], f'selector already bound by {name}'
    for binding in lock['contractSuccessors']:
        assert binding['record']['path'] != record_path


def build(product):
    lock, accepted, bound = lock_state(product)
    files, reports = {}, []
    for parent, (path, product_path) in COPIES.items():
        out, report = json_copy(parent, bound)
        files[path] = out
        if product_path:
            base = subprocess.run(['git', '-C', str(product), 'show', f'{PRODUCT_HEAD}:{product_path}'],
                                  check=True, capture_output=True).stdout
            if base != read(parent):
                raise SystemExit(f'product {product_path} differs from its accepted parent')
            report['productPath'] = product_path
        reports.append(report)
    # The design copy and the product copy keep their parents' relation.
    def body(raw):
        return raw.decode().split('\n')
    pds, ppds = body(files[COPIES[PDS][0]]), body(files[COPIES[PPDS][0]])
    start = pds.index('    "AtomSuccessorV1": {') - 1
    end = pds.index('  "$ref": "#/$defs/PolicyDocumentV2",') - 2
    assert pds[:start] + pds[end:] == ppds, 'PDS copies lost their parents\' relation'
    section, verbatim = section_4a()
    files[f'{UNIT}/atom-section-4a.md'] = (section + '\n').encode('utf-8')
    passage_overrides = overrides(section)
    materialization = {
        'schemaVersion': 1,
        'standing': ('Exact schema source bytes for unit I1-a: it copies each candidate to its product path. '
                     'I1-a also re-pins the registries, source maps, atom-registry pins and generated code, '
                     'which this map does not fix. Independent review and root assent are required before selection.'),
        'baseProductHead': PRODUCT_HEAD,
        'files': [{'productPath': r['productPath'], 'candidatePath': r['copy']['path'],
                   'before': {'bytes': r['parent']['bytes'], 'sha256': r['parent']['sha256']},
                   'after': {'bytes': r['copy']['bytes'], 'sha256': r['copy']['sha256']}}
                  for r in sorted(reports, key=lambda r: r.get('productPath', '')) if 'productPath' in r]}
    files[f'{UNIT}/materialization-map.json'] = dumps(materialization)
    files[f'{UNIT}/evidence/copies-report.json'] = dumps({
        'schemaVersion': 1, 'productHead': PRODUCT_HEAD, 'member': MEMBER, 'copies': reports,
        'section4a': {'verbatimLawLines': [88, 221], 'verbatimSha256': sha(verbatim.encode('utf-8')),
                      'insertedAfter': f'{ATOM}:366'}})
    static = [LAW, UNITS_LAW, f'{UNIT}/README.md', f'{UNIT}/evidence/build_i1l.py',
              f'{UNIT}/evidence/cases-report.json', f'{UNIT}/evidence/check_cycle_representative.py',
              f'{UNIT}/evidence/cycle_representative_model.py']
    for path in static:
        files[path] = read(path)
    assert sha(files[LAW]) == LAW_SHA256 and sha(files[UNITS_LAW]) == UNITS_SHA256
    parents = sorted({e['parent']['path'] for e in passage_overrides} | set(COPIES), key=str)
    record = {
        'schemaVersion': 1,
        'standing': ('PROPOSED I1-L policy-language contract successor (law M3-I1 r2 items 2 to 4): the '
                     'cycle-representative graph atom. Text passage overrides of workflows-and-surfaces (and its '
                     'selected effective copy), identity-and-evidence, the composition contract and the atom '
                     'contract (new section 4a); complete successor copies of the policy-document v2 and '
                     'identity v3 schemas, design and product source, each its parent with the lock\'s bound '
                     'overrides carried and the one operation member appended; a reference model with its '
                     'discriminating cases. Exact frozen candidate requires actual independent review and root assent.'),
        'parents': [pin(p, read(p)) for p in parents],
        'passageOverrides': passage_overrides,
        'candidates': None,
    }
    candidate_paths = sorted(files)
    record['candidates'] = [pin(p, files[p]) for p in candidate_paths]
    files[f'{UNIT}/successor.json'] = dumps(record)
    subject = {'schemaVersion': 1, 'files': [pin(p, files[p]) for p in sorted(files)]}
    files[f'{BASE}/i1-l-subject.json'] = dumps(subject)
    check(record, subject, files, accepted, bound, lock)
    return files


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--product', required=True, type=Path)
    parser.add_argument('--check', action='store_true')
    args = parser.parse_args()
    files = build(args.product.resolve())
    written = [p for p in files if p.startswith(UNIT + '/') and not p.endswith(('README.md', '.py', 'cases-report.json'))]
    written.append(f'{BASE}/i1-l-subject.json')
    for path in sorted(set(written)):
        target = ARCH / path
        if args.check:
            if target.read_bytes() != files[path]:
                raise SystemExit(f'differs: {path}')
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(files[path])
    subject = files[f'{BASE}/i1-l-subject.json']
    record = files[f'{UNIT}/successor.json']
    print(json.dumps({'subject': pin(f'{BASE}/i1-l-subject.json', subject),
                      'successor': pin(f'{UNIT}/successor.json', record),
                      'overrides': len(json.loads(record)['passageOverrides']),
                      'candidates': len(json.loads(record)['candidates']), 'checked': args.check}))


if __name__ == '__main__':
    main()
