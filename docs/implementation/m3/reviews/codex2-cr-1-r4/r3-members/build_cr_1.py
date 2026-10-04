"""Build CR-1, the component role-to-kind contract successor of law M3-C (item 7): the closed
host table in security-and-lifecycle S1, the widened DR-103 role vocabulary, the successor copy of
the completed structural manifest schema, the copies report, the materialization map,
PASSAGES.md, the subject manifest and the lead's draft unit record.

Usage: build_cr_1.py [--product PATH] [--rev REV] [--check]
- PATH is the product checkout (default /Users/sb/code/opensip-ai/opensip), read only. REV
  (default 392499e, product main for r3) names the product commit whose design-lock.json, manifest schema input and
  manifest fixtures are read with read-only `git show`.
- Without --check every generated file is written. With --check nothing is written: each
  generated file is rebuilt in memory and compared with the bytes on disk.

Deterministic: two runs give identical bytes. Run with python3 -I -B at nice -n 19. It needs
the hand-written README.md to exist, because the record and the subject pin it.

Generated: cr-1/PASSAGES.md, cr-1/successor.json, cr-1/completion/manifest-schema.completed.v1.json,
cr-1/materialization-map.json, cr-1/evidence/copies-report.json, ../cr-1-subject.json and
../cr-1-unit.json (the unit record is not part of the subject). evidence/schema-audit.json is written
by evidence/audit_schema.py (it needs jsonschema); this build pins it and checks that it audits
exactly the copy built here.
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
REV = opt('--rev', '392499e')
CHECK = '--check' in args
M = 'docs/implementation/m3/snapshot-plan-c/'
D = M + 'cr-1/'

SL = 'docs/v2/contracts/product-v1/security-and-lifecycle.md'
DR103 = 'docs/coop/artifacts/component-manifest-schemas.v11.json'
COMPLETED = 'docs/coop/completion/manifest-schema.completed.v1.json'
APPLICATION = 'docs/coop/completion/architecture-application.v1.json'
CASES = 'docs/coop/completion/manifest-cases.completed.v1.json'
LAW = M + 'PROPOSAL-r7.md'
PRODUCT_SCHEMA = 'tools/security/inputs/manifest-schema.json'
PRODUCT_SOURCES = 'tools/security/inputs/sources.json'
PRODUCT_SHAPE = 'crates/security/src/generated/component_manifest_shape.rs'
PRODUCT_OWNER = 'crates/security/src/component_manifest.rs'
SHAPE_FIXTURE = 'crates/security/tests/fixtures/manifest268-shape.ndjson'
SEMANTIC_FIXTURE = 'crates/security/tests/fixtures/manifest268-semantic.ndjson'
COPY = D + 'completion/manifest-schema.completed.v1.json'
TABLE = [('analyzer', 'provider'), ('toolchain', 'toolchain'), ('stdlib', 'stdlib'),
         ('rust-dev-llvm', 'rust-dev-llvm'), ('grammar', 'grammar')]
ROLES = [r for r, _ in TABLE]


def git_show(path):
    return subprocess.run(['git', '-C', str(W), 'show', '%s:%s' % (REV, path)], check=True,
                          capture_output=True).stdout


def pin_bytes(path, raw):
    return {'path': path, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def pin(path):
    return pin_bytes(path, (A / path).read_bytes())


def read_pinned(row):
    raw = (A / row['path']).read_bytes()
    assert pin_bytes(row['path'], raw) == {k: row[k] for k in ('path', 'bytes', 'sha256')}, row['path']
    return raw


def resolve(doc, pointer):
    for token in pointer[1:].split('/'):
        doc = doc[int(token)] if isinstance(doc, list) else doc[token.replace('~1', '/').replace('~0', '~')]
    return doc


def insert_only(before, after):
    ops = difflib.SequenceMatcher(None, before, after, autojunk=False).get_opcodes()
    return before != after and all(tag in ('equal', 'insert') for tag, *_ in ops)


# --- The lock at REV. ---------------------------------------------------------------------------
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
CONTRACT_SUCCESSORS = len(lock['contractSuccessors'])

# --- The law's table, read from the accepted snapshot, must be this table. -----------------------
law = (A / LAW).read_text(encoding='utf-8')
law_rows = re.findall(r'^    \| `([a-z-]+)` \| `([a-z-]+)` \|$', law, flags=re.M)
assert law_rows == TABLE, law_rows

# --- The overrides. ----------------------------------------------------------------------------
SL70_ADD = '\n\n' + (
    '**Component roles and closure kinds (contract successor CR-1, 2026-10-04).** The `closure2` `kind` of a'
    ' component-manifest closure is fixed by one closed host table keyed by the admitted manifest\'s `role`. DR-103'
    ' makes the role vocabulary host-owned and its extension a host decision, not a manifest right; this table is that'
    ' decision:\n'
    '\n'
    '| Manifest `role` | `closure2` `kind` | Command tree (`commands`) |\n'
    '|---|---|---|\n'
    + ''.join('| `%s` | `%s` | %s |\n' % (r, k, 'required, non-empty' if r == 'analyzer' else 'none: absent')
              for r, k in TABLE) +
    '\n'
    'The kind is never asserted by a caller, inferred from a path or file name, or taken from any other manifest'
    ' field. A closure whose role maps to a kind other than the one its selecting field requires (identity'
    ' `closureKinds.byField`) refuses. `evaluator`, `detector` and `adapter` are never manifest roles, and `core` is'
    ' never a role or an identity closure kind: the core evaluator, detector, provider and adapter closures are'
    ' projections of the authenticated core inventory (identity §3, contract successors EC1 and CRC-1), never'
    ' component-manifest closures. `analyzer` is the only role whose component the host launches, as a provider'
    ' session. The other four roles are **closure-only**: the host never launches such a component through its'
    ' manifest, and reads its tree only as retained closure bytes. A closure-only manifest therefore declares no'
    ' capability (`capabilities` is `[]`, since a capability declaration is an analyzer role subprotocol) and requests'
    ' no permission (`permissions` is `[]`); its platform `entrypoint` names a committed regular-file entry of that'
    ' platform\'s tree, never a directory or symlink, under RJ-3\'s path and presence rules, but need not be'
    ' executable, and the host never executes it; and it carries no command tree: `commands` is absent, so it asks for'
    ' no mount and claims no root command. **The D4 join.** D4\'s EE-5a root-command check at R10a (M3-D r3 item 24)'
    ' examines every manifest that declares a command tree. For a closure-only role any declared tree is such a claim:'
    ' it is refused by the closed manifest schema at admission (RJ-6), and at D4 as an EE-5a root-command claim by that'
    ' existing route. How EE-5a judges an `analyzer` manifest\'s required tree is M3-D\'s and is unchanged here. A tool'
    ' that the host launches from a closure-only'
    ' tree is launched under its own launch law, never as a component session. Every other DR-103 manifest rule'
    ' applies to every role alike. A violation refuses at manifest admission through the manifest owner\'s existing'
    ' schema, capability, permission and path refusals; no code is added.')
TYPE_ADD = ('; M3 vocabulary (contract successor CR-1, the host\'s decision): \'analyzer\', \'toolchain\', \'stdlib\','
            ' \'rust-dev-llvm\', \'grammar\', each fixing the closure2 kind through security-and-lifecycle S1\'s closed'
            ' role-to-kind table; \'evaluator\', \'detector\' and \'adapter\' are never manifest roles')
SEMANTICS_ADD = (' The four roles beyond analyzer (contract successor CR-1) are closure-only: such a component is never'
                 ' launched through its manifest and its tree is read only as retained closure bytes, so it declares'
                 ' no capability and requests no permission, its entrypoint need not be executable and is never'
                 ' executed, and it carries no command tree (security-and-lifecycle S1).')
COMMANDS_ADD = (' Under contract successor CR-1 this tree is role-scoped. Role analyzer keeps it as above: required,'
                ' non-empty, with its one parentless entry bound to manifest.name (RJ-2). The closure-only roles'
                ' (toolchain, stdlib, rust-dev-llvm, grammar) carry no command tree: commands is absent, so such a'
                ' manifest asks for no mount and claims no root command. A closure-only manifest that declares a command'
                ' tree is refused: by the closed manifest schema (RJ-6), and at D4/R10a as an EE-5a root-command claim'
                ' by its existing route (security-and-lifecycle S1).')
dr103 = json.loads((A / DR103).read_bytes())
fields = dr103['manifestSchema']['fields']
ROLE_INDEX = [i for i, f in enumerate(fields) if f.get('name') == 'role']
assert ROLE_INDEX == [7], ROLE_INDEX
SPEC = [
    (SL, {'line': 70}, lambda b: b + SL70_ADD),
    (DR103, {'jsonPointer': '/manifestSchema/fields/7/type'}, lambda b: b + TYPE_ADD),
    (DR103, {'jsonPointer': '/manifestSchema/fields/7/semantics'}, lambda b: b + SEMANTICS_ADD),
    (DR103, {'jsonPointer': '/manifestSchema/fields/8/semantics'}, lambda b: b + COMMANDS_ADD),
]
parents, overrides = {}, []
for path, selector, make in SPEC:
    parent = accepted.get(path)
    assert parent is not None, 'parent is not accepted at %s: %s' % (REV, path)
    parent = {k: parent[k] for k in ('path', 'bytes', 'sha256')}
    raw = read_pinned(parent)
    parents[path] = parent
    if 'line' in selector:
        try:
            json.loads(raw)
        except ValueError:
            pass
        else:
            raise AssertionError('line selector on a JSON parent: ' + path)
        before = raw.decode('utf-8').splitlines()[selector['line'] - 1]
    else:
        before = resolve(json.loads(raw), selector['jsonPointer'])
    assert isinstance(before, str) and before
    key = (path, json.dumps(selector, sort_keys=True))
    assert key not in bound, 'already overridden by %s: %s %s' % (bound[key], path, selector)
    after = make(before)
    assert insert_only(before, after) and 'CR-1' in after, (path, selector)
    overrides.append({'parent': parent, 'selector': selector, 'before': before, 'after': after})
assert resolve(dr103, '/manifestSchema/fields/7/name') == 'role'
assert resolve(dr103, '/manifestSchema/fields/8/name') == 'commands'

OWNER_CHANGE = (
    'The command-tree-specific checks run only when commands is present, which the schema makes exactly'
    ' role analyzer. Component-name and manifest-alias admission currently colocated at'
    ' component_manifest.rs:257-276 remains mandatory for every role: form the name/alias set without'
    ' reading commands for closure-only roles, reject duplicate keys and reserved-list collisions, and'
    ' check live-name collisions against a different (stableId, provenance); analyzer also includes its'
    ' mounted-root aliases as before. The executable-entrypoint check (line 337) applies to role analyzer'
    ' only, while a closure-only entrypoint must name a regular-file entry directly (no symlink'
    ' resolution); the closure-only roles require capabilities [] and permissions []. Line ranges (r3),'
    ' identical at product cd5958b and 392499e: command_checks spans lines 166-279; its command-tree'
    ' checks are lines 171-256 (line 171 indexes m["commands"] unconditionally today); its name and alias'
    ' admission is lines 257-276; validate_inner calls it at line 414, for both validate (395-397) and'
    ' validate_inventory (398-403), so the split applies to full host admission and to inventory-body'
    ' validation alike.')

# --- The completed manifest schema successor copy. --------------------------------------------------
parent_raw = (A / COMPLETED).read_bytes()
parent_pin = pin_bytes(COMPLETED, parent_raw)
application = json.loads(read_pinned(accepted[APPLICATION]))


def find_key(value, key):
    if isinstance(value, dict):
        if key in value:
            yield value[key]
        for x in value.values():
            yield from find_key(x, key)
    elif isinstance(value, list):
        for x in value:
            yield from find_key(x, key)


m_schema = list(find_key(application, 'M.SCHEMA'))
assert len(m_schema) == 1, 'architecture-application must hold exactly one M.SCHEMA clause'
assert {'path': COMPLETED, 'pin': parent_pin['sha256'], 'selector': ''} in m_schema[0]['sources']
product_raw = git_show(PRODUCT_SCHEMA)
assert product_raw == parent_raw, 'product manifest schema input differs from the completed schema'
product_sources = json.loads(git_show(PRODUCT_SOURCES))
assert {'path': PRODUCT_SCHEMA, 'bytes': len(parent_raw), 'sha256': parent_pin['sha256']} in product_sources['files']
schema = json.loads(parent_raw)
assert json.dumps(schema, indent=2).encode() + b'\n' == parent_raw, 'parent is not in its json.dumps(indent=2) form'
assert schema['properties']['role'] == {'const': 'analyzer'} and 'oneOf' not in schema
assert schema['properties']['commands'] == {'type': 'array', 'items': {'$ref': '#/$defs/command'}, 'minItems': 1,
                                            'maxItems': 4096}
CLOSURE_ONLY = ROLES[1:]
BRANCHES = [
    {'$comment': 'CR-1: role analyzer, the only launched role, requires a non-empty command tree, as before.',
     'properties': {'role': {'const': 'analyzer'}, 'commands': {'type': 'array', 'minItems': 1}},
     'required': ['role', 'commands']},
    {'$comment': 'CR-1: the closure-only roles carry no command tree. The root types commands as an array, so this'
                 ' null type admits no value: commands must be absent.',
     'properties': {'role': {'enum': CLOSURE_ONLY}, 'commands': {'type': 'null'}},
     'required': ['role']},
]
edited = {}
for key, value in schema.items():
    if key == 'properties':
        value = dict(value, role={'enum': ROLES})
    if key == 'required':
        assert 'commands' in value
        value = [k for k in value if k != 'commands']
    edited[key] = value
    if key == 'additionalProperties':
        edited['oneOf'] = BRANCHES
assert list(edited) == ['$schema', '$id', '$comment', 'type', 'properties', 'required', 'additionalProperties', 'oneOf',
                        '$defs']
schema = edited
GENERATOR_KEYWORDS = {'$schema', '$id', '$comment', '$defs', '$ref', 'type', 'properties', 'required',
                      'additionalProperties', 'oneOf', 'const', 'enum', 'pattern', 'minimum', 'maximum', 'minLength',
                      'maxLength', 'minItems', 'maxItems', 'uniqueItems', 'items', 'propertyNames', 'x-maxUtf8Bytes'}
for branch in BRANCHES:
    assert set(branch) <= GENERATOR_KEYWORDS and set(branch['required']) <= set(branch['properties'])
    for sub in branch['properties'].values():
        assert set(sub) <= GENERATOR_KEYWORDS
copy_raw = json.dumps(schema, indent=2).encode() + b'\n'
outputs = {COPY: copy_raw}
diff = list(difflib.unified_diff(parent_raw.decode().splitlines(), copy_raw.decode().splitlines(), lineterm='', n=0))
hunks = [line for line in diff if line.startswith(('-', '+')) and not line.startswith(('---', '+++'))]
assert hunks[:8] == ['-      "const": "analyzer"', '+      "enum": [', '+        "analyzer",', '+        "toolchain",',
                     '+        "stdlib",', '+        "rust-dev-llvm",', '+        "grammar"', '+      ]'], hunks
assert hunks[8] == '-    "commands",' and all(h.startswith('+') for h in hunks[9:]), hunks

# Audit: no existing negative role case becomes valid under the widened enum.
cases = json.loads((A / CASES).read_bytes())
arch_role_values = sorted({op['value'] for c in cases['cases'] for op in c['operations']
                           if op.get('op') == 'set' and op.get('path') == ['role']})
assert arch_role_values and not set(arch_role_values) & set(ROLES), arch_role_values
shape_values, shape_cases = [], 0
for line in git_show(SHAPE_FIXTURE).decode('utf-8').splitlines():
    q = json.loads(line)
    if "('role',)" in q['label'] or q['label'].endswith('/()/role'):
        shape_cases += 1
        assert q['valid'] is False
        value = q['value'].get('role', '<absent>')
        assert not (isinstance(value, str) and value in ROLES), q['label']
        shape_values.append(value)
semantic_role = [json.loads(line) for line in git_show(SEMANTIC_FIXTURE).decode('utf-8').splitlines()
                 if json.loads(line)['label'] in ('TYPE/role', 'REQUIRED/role')]
assert len(semantic_role) == 2 and all(q['valid'] is False for q in semantic_role)
report = {
    'schemaVersion': 1,
    'standing': 'CR-1 copies report (r2). The completed structural manifest schema is not a verify_design input: the'
                ' architecture application pins it (clause M.SCHEMA) and the product carries the same bytes as its'
                ' security generation input. The CR-1 copy is those bytes with exactly three edits, serialized in the'
                ' parent\'s own form: /properties/role widened from the constant analyzer to the closed enum of the'
                ' CR-1 table; commands removed from /required; and a root oneOf of two role-scoped branches, so that'
                ' analyzer requires a non-empty command tree, as before, and the closure-only roles carry none.',
    'productHead': subprocess.run(['git', '-C', str(W), 'rev-parse', REV], check=True, capture_output=True,
                                  text=True).stdout.strip(),
    'copies': [{
        'parent': parent_pin,
        'parentSelection': {'application': pin(APPLICATION), 'clause': 'M.SCHEMA',
                            'productInput': pin_bytes(PRODUCT_SCHEMA, product_raw)},
        'copy': pin_bytes(COPY, copy_raw),
        'edits': [{'jsonPointer': '/properties/role', 'before': {'const': 'analyzer'}, 'after': {'enum': ROLES}},
                  {'jsonPointer': '/required', 'change': 'commands removed (r2, RF-CR1-1)'},
                  {'jsonPointer': '/oneOf', 'change': 'added after additionalProperties: two role-scoped branches'
                                                     ' (r2, RF-CR1-1)', 'after': BRANCHES}],
        'serialization': 'json.dumps(indent=2) plus LF, byte-identical to the parent\'s own form',
        'diffLines': hunks,
    }],
    'roleCaseAudit': {
        'archCases': {'file': pin(CASES), 'roleValuesSet': arch_role_values},
        'productShapeFixture': {'file': pin_bytes(SHAPE_FIXTURE, git_show(SHAPE_FIXTURE)), 'roleCases': shape_cases,
                                'allInvalid': True, 'newRoleValuesUsed': 0},
        'productSemanticFixture': {'file': pin_bytes(SEMANTIC_FIXTURE, git_show(SEMANTIC_FIXTURE)),
                                   'labels': ['REQUIRED/role', 'TYPE/role'], 'allInvalid': True},
        'conclusion': 'Every existing negative role case stays negative: none sets a value of the CR-1 enum.',
    },
}
outputs[D + 'evidence/copies-report.json'] = (json.dumps(report, indent=2) + '\n').encode()
mat = {
    'schemaVersion': 1,
    'standing': 'Exact product bytes for unit C2a (law M3-C r7 item 7; C2a depends on CR-1): it copies the candidate to'
                ' its product path, re-pins tools/security/inputs/sources.json and regenerates'
                ' crates/security/src/generated/component_manifest_shape.rs through tools/generate_security_tables.py'
                ' (the role node becomes the five-way enum, the root node reads commands only when present and gains'
                ' a one-of term, and two branch nodes are added; every keyword is inside the generator\'s allowed set,'
                ' so the generator itself is unchanged). C2a also implements the table and the closure-only rules in'
                ' the manifest owner and closure admission, which this map does not fix. Independent review and root'
                ' assent are required before selection.',
    'baseProductHead': report['productHead'],
    'files': [{'productPath': PRODUCT_SCHEMA, 'candidatePath': COPY,
               'before': {'bytes': len(product_raw), 'sha256': hashlib.sha256(product_raw).hexdigest()},
               'after': {'bytes': len(copy_raw), 'sha256': hashlib.sha256(copy_raw).hexdigest()}}],
    'alsoChangedByC2a': [
        {'productPath': PRODUCT_SOURCES, 'base': pin_bytes(PRODUCT_SOURCES, git_show(PRODUCT_SOURCES)),
         'change': 'the manifest-schema.json row takes the candidate\'s bytes and sha256'},
        {'productPath': PRODUCT_SHAPE, 'base': pin_bytes(PRODUCT_SHAPE, git_show(PRODUCT_SHAPE)),
         'change': 'regenerated: header digest; the role node matches any of the five roles; the root node checks'
                   ' commands only when present (is_none_or) and gains the one-of term; two branch nodes, of which'
                   ' the closure-only branch types commands as null'},
        {'productPath': PRODUCT_OWNER, 'base': pin_bytes(PRODUCT_OWNER, git_show(PRODUCT_OWNER)),
         'change': OWNER_CHANGE},
        {'productPath': SHAPE_FIXTURE, 'base': pin_bytes(SHAPE_FIXTURE, git_show(SHAPE_FIXTURE)),
         'change': 'none required: evidence/schema-audit.json shows all 11010 cases keep their verdicts under the'
                   ' copy; C2a adds closure-only positive and negative cases (README CR-T1 to CR-T4)'},
        {'productPath': SEMANTIC_FIXTURE, 'base': pin_bytes(SEMANTIC_FIXTURE, git_show(SEMANTIC_FIXTURE)),
         'change': 'none required: every case is role analyzer; C2a adds closure-only semantic cases'},
    ],
}
outputs[D + 'materialization-map.json'] = (json.dumps(mat, indent=2) + '\n').encode()


# --- PASSAGES.md. ------------------------------------------------------------------------------
def selector_text(selector):
    return 'line %d' % selector['line'] if 'line' in selector else 'pointer `%s`' % selector['jsonPointer']


def fence(text):
    return '~~~text\n' + text + '\n~~~\n'


parts = ['# CR-1 passages (generated)\n',
         'Generated by `evidence/build_cr_1.py` from the same data as `successor.json`; do not edit by hand. Each'
         ' entry gives the parent, the selector, the exact accepted `before` and the candidate `after`. Every `after`'
         ' keeps its `before` and only inserts text. Product lock: `%s`, %d contract successors.\n' % (REV, CONTRACT_SUCCESSORS),
         '## Passage overrides\n']
for n, o in enumerate(overrides, 1):
    parts += ['### %d. `%s` %s\n' % (n, o['parent']['path'], selector_text(o['selector'])),
              'Before:\n', fence(o['before']), 'After:\n', fence(o['after'])]
parts += ['## The successor copy\n',
          '`completion/manifest-schema.completed.v1.json` is `%s` (%d bytes, `%s`) with three edits: `/properties/role`'
          ' widened, `commands` removed from `/required`, and the root `oneOf` added. The unified diff (no context) is:\n'
          % (COMPLETED, parent_pin['bytes'], parent_pin['sha256']),
          fence('\n'.join(hunks))]
outputs[D + 'PASSAGES.md'] = '\n'.join(parts).encode()


def current(path):
    return outputs[path] if path in outputs else (A / path).read_bytes()


HAND = [D + 'README.md', D + 'evidence/build_cr_1.py', D + 'evidence/check_cr_1.py', D + 'evidence/verify_scratch.py',
        D + 'evidence/audit_schema.py', D + 'evidence/schema-audit.json']
try:
    audit = json.loads((A / D / 'evidence/schema-audit.json').read_bytes())
    AUDIT_OK = audit['copy'] == pin_bytes(COPY, copy_raw) and audit['parent'] == parent_pin
except (OSError, ValueError, KeyError, TypeError):
    AUDIT_OK = False
GENERATED = [D + 'PASSAGES.md', COPY, D + 'materialization-map.json', D + 'evidence/copies-report.json']
candidates = sorted([pin_bytes(p, current(p)) for p in HAND + GENERATED], key=lambda r: r['path'])
for row in candidates:
    assert row['path'] not in accepted, 'candidate reuses an accepted path: ' + row['path']
record = {
    'schemaVersion': 1,
    'standing': 'PROPOSED CR-1 security and DR-103 host-vocabulary contract successor (law M3-C r7 item 7): the closed'
                ' role-to-kind table (analyzer to provider; toolchain, stdlib, rust-dev-llvm and grammar to the kind of'
                ' the same name) in security-and-lifecycle S1, the four non-analyzer roles as closure-only roles, and'
                ' the DR-103 role vocabulary widened to those five roles. Text-only overrides of security-and-lifecycle'
                ' and component-manifest-schemas.v11; a complete successor copy of the completed structural manifest'
                ' schema (not a verify_design input) whose role becomes the five-role enum, selected by this record as'
                ' the completed manifest schema, with docs/coop/completion/manifest-schema.completed.v1.json and its'
                ' completion contract\'s analyzer-only sentence historical. No code, class, exit, public code,'
                ' inventory or product change; unit C2a materializes the copy. Exact frozen candidate requires actual'
                ' independent review and root assent.',
    'parents': sorted(parents.values(), key=lambda r: r['path']),
    'passageOverrides': overrides,
    'candidates': candidates,
}
outputs[D + 'successor.json'] = (json.dumps(record, indent=2, ensure_ascii=False) + '\n').encode()
record_pin = pin_bytes(D + 'successor.json', outputs[D + 'successor.json'])
subject = {'schemaVersion': 1, 'files': sorted(candidates + [record_pin], key=lambda r: r['path'])}
outputs[M + 'cr-1-subject.json'] = (json.dumps(subject, indent=2) + '\n').encode()
subject_pin = pin_bytes(M + 'cr-1-subject.json', outputs[M + 'cr-1-subject.json'])
unit = {
    'schemaVersion': 1,
    'unit': 'snapshot-plan-c-cr-1',
    'status': 'DRAFT-PENDING-REVIEW',
    'subjectManifest': subject_pin,
    'independentReview': {'path': 'docs/implementation/m3/reviews/codex2-cr-1-r3/review.json', 'bytes': None,
                          'sha256': None},
    'rootSubstantiveAssent': False,
    'requiredUnitFindings': [],
    'acceptedSuccessor': record_pin,
    'rootAssessment': 'DRAFT (r3, after CODEX2\'s r2 REQUIRED-FINDINGS RF-CR1-2). Completed by the lead after CODEX2\'s'
                      ' r3 review: status ACCEPTED-DESIGN-UNIT, the review pin, rootSubstantiveAssent true. CR-1 is four'
                      ' insert-only passage overrides (SL 70: the role-to-kind table, the closure-only rules with no'
                      ' command tree, and the D4 join; the DR-103 v11 role field\'s type and semantics; the commands'
                      ' field\'s semantics) and a complete successor copy of the completed manifest schema with the'
                      ' five-role enum and role-scoped commands, for C2a. It binds on'
                      ' the verify_design at product %s on top of %d contract successors, CRC-1 among them.'
                      % (REV, CONTRACT_SUCCESSORS),
    'fullM2Complete': False,
    'productQualification': False,
}
outputs[M + 'cr-1-unit.json'] = (json.dumps(unit, indent=2) + '\n').encode()

if CHECK:
    stale = [p for p, b in outputs.items() if not (A / p).exists() or (A / p).read_bytes() != b]
    if not AUDIT_OK:
        stale.append(D + 'evidence/schema-audit.json (does not audit this copy)')
    print(json.dumps({'check': 'identical' if not stale else 'DIFFERS', 'differs': stale}, indent=1))
    sys.exit(1 if stale else 0)
for path, raw in outputs.items():
    (A / path).parent.mkdir(parents=True, exist_ok=True)
    (A / path).write_bytes(raw)
if not AUDIT_OK:
    print('schema-audit.json does not audit this copy: run evidence/audit_schema.py --deps DIR --write, then rebuild')
    sys.exit(1)
print(json.dumps({'rev': REV, 'contractSuccessors': CONTRACT_SUCCESSORS, 'overrides': len(overrides),
                  'parents': len(parents), 'candidates': len(candidates), 'subject': subject_pin,
                  'successor': record_pin, 'copy': pin_bytes(COPY, copy_raw),
                  'roleCaseAudit': {'arch': arch_role_values, 'productShapeCases': shape_cases}}, indent=1))
