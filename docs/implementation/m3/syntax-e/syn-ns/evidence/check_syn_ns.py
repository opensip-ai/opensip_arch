"""Read-only checks for contract successor SYN-NS, independent of build_syn_ns.py's encoder.

1. Grammar pins. Each grammar's parser.c and node-types.json under --grammars (E0's SCRATCH sources) must hash to
   its row in docs/implementation/m3/syntax-e/e0-probe/pins/<repo>.pins.tsv.
2. Symbol census. From each parser.c, the public symbols (ts_symbol_map[s] == s) with their name, named and
   visible flags, and the field names; from node-types.json, which fields each named kind declares.
3. Every reference. Every node kind, anonymous token and field that normalizer.v1.json and the four level
   specifications name, per row, must be a visible public symbol of that row's grammar with the stated namedness,
   and every (kind, field) pair must be declared by node-types.json. Every rule object's keys are from a closed set,
   so no reference escapes this walk. This is the design-time image of admission step A12.
4. Canonical bytes. Every closure member re-encodes to itself under foundation/canonical.py (the real module; with
   --deps its jsonschema import is satisfied, else stubbed for canonical() alone), within its size bound.
5. The map. specification-map.v1.json validates against identity-schemas.v3.json#/$defs/normalization-specification-
   map with the design's ExactValidator (needs --deps), names the normalizer, has exactly L0 to L3 strictly
   ascending, and each row's digest is its level file's sha256 at its fixed path.
6. Consistency. Every level file names the normalizer and its own level; L1, L2 and L3 share atomicKinds, L2 and
   L3 share the comment law; the parameters equal native-evidence.md section 6.2.
7. Fixtures (r2). reference_syn_ns.py, a small oracle that reads these documents' own tables, runs over the
   hand-written trees of evidence/fixtures.json; every computed token stream and control-flow graph must equal the
   hand-derived expectation, the stated distinct/equal/disjoint relations must hold, and, where a fixture says so,
   r1's rule must reproduce the finding's defect on the same input.
8. With --write, writes evidence/kinds-report.json; without it, compares with that file.

Usage: python3.14 -I -B evidence/check_syn_ns.py [--grammars DIR] [--deps DIR] [--write]
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import sys
import types
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCH = HERE.parents[5]
BASE = 'docs/implementation/m3/syntax-e'
UNIT = f'{BASE}/syn-ns'
CLOSURE = f'{UNIT}/closure'
PINS = f'{BASE}/e0-probe/pins'
SCRATCH_SRC = '/private/tmp/claude-501/-Users-sb-code/8baf40a9-970f-46bc-bd52-a3dde4a615a1/scratchpad/e0/src'
GRAMMARS = {'javascript': ('tree-sitter-javascript', 'src'), 'rust': ('tree-sitter-rust', 'src'),
            'tsx': ('tree-sitter-typescript', 'tsx/src'), 'typescript': ('tree-sitter-typescript', 'typescript/src')}
LEVELS = ['L0-verbatim', 'L1-lexical', 'L2-comment-insensitive', 'L3-identifier-insensitive']
NE = 'docs/v2/contracts/product-v1/native-evidence.md'
IDS = 'docs/implementation/m3/syntax-e/syn-1f/design/foundation/identity-schemas.v3.json'   # the selected copy (SYN-1F)


def read(path):
    return (ARCH / path).read_bytes()


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


# ---------------------------------------------------------------- grammar census (parser.c and node-types.json)
def c_string(body):
    out, i = bytearray(), 0
    while i < len(body):
        ch = body[i]
        if ch == '\\':
            nxt = body[i + 1]
            simple = {'n': '\n', 't': '\t', 'r': '\r', '\\': '\\', '"': '"', "'": "'", '0': '\0', 'a': '\a',
                      'b': '\b', 'f': '\f', 'v': '\v', '?': '?'}
            if nxt in simple:
                out += simple[nxt].encode()
                i += 2
                continue
            if nxt == 'x':
                j = i + 2
                while j < len(body) and body[j] in '0123456789abcdefABCDEF':
                    j += 1
                out.append(int(body[i + 2:j], 16))
                i = j
                continue
            raise ValueError(body)
        out += ch.encode('utf-8')
        i += 1
    return out.decode('utf-8')


def census(src):
    text = (src / 'parser.c').read_text(encoding='utf-8')
    enum = re.search(r'enum ts_symbol_identifiers \{(.*?)\n\};', text, re.S).group(1)
    ids = {m.group(1): int(m.group(2)) for m in re.finditer(r'^\s*(\w+) = (\d+),', enum, re.M)}
    ids['ts_builtin_sym_end'] = 0
    block = re.search(r'ts_symbol_names\[\] = \{(.*?)\n\};', text, re.S).group(1)
    names = {m.group(1): c_string(m.group(2)) for m in re.finditer(r'^\s*\[(\w+)\] = "((?:[^"\\]|\\.)*)",', block, re.M)}
    block = re.search(r'ts_symbol_metadata\[\] = \{(.*?)\n\};', text, re.S).group(1)
    meta = {m.group(1): ('.visible = true' in m.group(2), '.named = true' in m.group(2))
            for m in re.finditer(r'\[(\w+)\] = \{(.*?)\}', block, re.S)}
    block = re.search(r'ts_symbol_map\[\] = \{(.*?)\n\};', text, re.S).group(1)
    public = {m.group(1): m.group(2) for m in re.finditer(r'\[(\w+)\] = (\w+),', block)}
    fblock = re.search(r'ts_field_names\[\] = \{(.*?)\n\};', text, re.S).group(1)
    fields = {c_string(m.group(2)) for m in re.finditer(r'\[(\w+)\] = "((?:[^"\\]|\\.)*)",', fblock)}
    count = int(re.search(r'#define SYMBOL_COUNT (\d+)', text).group(1)) + \
        int(re.search(r'#define ALIAS_COUNT (\d+)', text).group(1))
    assert sorted(ids.values()) == list(range(count))
    named, anonymous = set(), set()
    for enum_name in ids:
        if public.get(enum_name, enum_name) != enum_name or not meta[enum_name][0]:
            continue
        (named if meta[enum_name][1] else anonymous).add(names[enum_name])
    node_types = json.loads((src / 'node-types.json').read_text(encoding='utf-8'))
    kind_fields = {t['type']: set(t.get('fields', {})) for t in node_types if t['named']}
    abi = int(re.search(r'#define LANGUAGE_VERSION (\d+)', text).group(1))
    return {'named': named, 'anonymous': anonymous, 'fields': fields, 'kindFields': kind_fields, 'abi': abi,
            'symbolCount': count}


def pinned(grammars):
    out = {}
    for row, (repo, sub) in GRAMMARS.items():
        rows = {}
        for line in read(f'{PINS}/{repo}.pins.tsv').decode('utf-8').splitlines():
            if line.startswith('#') or not line.strip():
                continue
            parts = line.split('\t')
            rows[parts[0]] = parts[1]
        src = Path(grammars) / repo / sub
        pins = {}
        for name in ('parser.c', 'node-types.json'):
            rel = f'{sub}/{name}'
            got = sha((src / name).read_bytes())
            assert rows.get(rel) == got, f'{repo}/{rel} is not the pinned file'
            pins[rel] = got
        out[row] = (src, repo, pins)
    return out


# ---------------------------------------------------------------- the reference walk
class Refs:
    def __init__(self, table):
        self.t = table
        self.items = []

    def named(self, kind, where):
        assert kind in self.t['named'], f'{where}: {kind!r} is not a visible public named symbol'
        self.items.append(('named', kind))

    def anon(self, token, where):
        assert token in self.t['anonymous'], f'{where}: {token!r} is not a visible public anonymous symbol'
        self.items.append(('anonymous', token))

    def field(self, kind, field, where):
        assert field in self.t['fields'], f'{where}: field {field!r} is not in the field list'
        assert field in self.t['kindFields'].get(kind, set()), f'{where}: {kind}.{field} is not declared'
        self.items.append(('field', f'{kind}.{field}'))


def keys_ok(obj, allowed, where):
    extra = set(obj) - set(allowed)
    assert not extra, f'{where}: unchecked keys {sorted(extra)}'


def walk_pattern_law(r, law, where):
    keys_ok(law, {'leaves', 'bindingForms', 'descend', 'law', 'statedLimit'}, where)
    for k in law.get('leaves', []):
        r.named(k, where)
    for b in law.get('bindingForms', []):
        keys_ok(b, {'kind', 'child', 'firstChild', 'field', 'whenChild', 'whenAnonymous'}, where)
        r.named(b['kind'], where)
        for key in ('child', 'firstChild', 'whenChild'):
            if key in b:
                r.named(b[key], where)
        if 'field' in b:
            r.field(b['kind'], b['field'], where)
        if 'whenAnonymous' in b:
            r.anon(b['whenAnonymous'], where)
    for d in law['descend']:
        keys_ok(d, {'kind', 'into', 'field'}, where)
        r.named(d['kind'], where)
        if 'field' in d:
            r.field(d['kind'], d['field'], where)


def walk_normalizer_row(r, row):
    w = 'normalizer/' + row['grammarId']
    keys_ok(row, {'grammarId', 'bodies', 'statementContainers', 'importOnly', 'declares', 'containers',
                  'patternLaw', 'parameterLaw', 'literals', 'controlFlow'}, w)
    for b in row['bodies']:
        keys_ok(b, {'kind', 'bodyKind', 'field', 'child', 'methodWhen'}, w + '/bodies')
        r.named(b['kind'], w)
        if 'field' in b:
            r.field(b['kind'], b['field'], w)
        if 'child' in b:
            r.named(b['child'], w)
        for k in b.get('methodWhen', {}).get('parentKinds', []) + b.get('methodWhen', {}).get('grandparentKinds', []):
            r.named(k, w)
    for k in row['statementContainers']:
        r.named(k, w)
    keys_ok(row['importOnly'], {'kinds', 'commentKinds'}, w)
    for k in row['importOnly']['kinds'] + row['importOnly']['commentKinds']:
        r.named(k, w)
    for d in row['declares']:
        keys_ok(d, {'kind', 'declarationKind', 'name', 'names', 'bindings', 'container', 'when'}, w + '/declares')
        assert d['declarationKind'] in ('module', 'namespace', 'type', 'function', 'method', 'field', 'variable',
                                        'parameter')
        r.named(d['kind'], w)
        for key in ('name', 'names', 'bindings'):
            if key in d and 'field' in d[key]:
                r.field(d['kind'], d[key]['field'], w)
    for c in row['containers']:
        keys_ok(c, {'kind', 'tag'}, w)
        r.named(c['kind'], w)
    walk_pattern_law(r, row['patternLaw'], w + '/patternLaw')
    for lit in row['literals']:
        keys_ok(lit, {'kind', 'literalKind'}, w)
        assert lit['literalKind'] in ('string', 'number', 'boolean', 'null', 'regex', 'template')
        r.named(lit['kind'], w)
    cf = row['controlFlow']
    keys_ok(cf, {'statementLists', 'nonStatements', 'roles', 'roleLaw', 'earlyReturn'}, w + '/controlFlow')
    for s in cf['statementLists']:
        keys_ok(s, {'kind', 'field'}, w)
        r.named(s['kind'], w)
        if 'field' in s:
            r.field(s['kind'], s['field'], w)
    for k in cf['nonStatements']:
        r.named(k, w)
    field_keys = {'consequence', 'alternative', 'body', 'condition', 'handler', 'finalizer', 'label'}
    kind_keys = {'alternativeChild', 'handlerBody', 'finalizerBody', 'default', 'arms', 'labelChild', 'child'}
    for role in cf['roles']:
        keys_ok(role, {'kind', 'role', 'cases', 'armValue'} | field_keys | kind_keys, w + '/roles')
        r.named(role['kind'], w)
        for key in field_keys & set(role):
            r.field(role['kind'], role[key], w)
        for key in kind_keys & set(role):
            r.named(role[key], w)
        for k in role.get('cases', []):
            r.named(k, w)
        if 'armValue' in role:
            r.field(role['arms'], role['armValue'], w)
    if 'earlyReturn' in cf:
        r.named(cf['earlyReturn']['kind'], w)
        for k in cf['earlyReturn']['opaque']:
            r.named(k, w)


def walk_level_row(r, row, level):
    w = f'{level}/{row["grammarId"]}'
    allowed = {'grammarId'}
    if level != 'L0-verbatim':
        allowed |= {'atomicKinds', 'lineTerminators'}
        for k in row['atomicKinds']:
            r.named(k, w)
        assert row['lineTerminators'] == ('insignificant' if row['grammarId'] == 'rust' else 'significant'), w
    if level in ('L2-comment-insensitive', 'L3-identifier-insensitive'):
        allowed |= {'commentKinds', 'docMarkerKinds', 'directivePatterns'}
        for k in row['commentKinds'] + row.get('docMarkerKinds', []):
            r.named(k, w)
        for pattern in row.get('directivePatterns', []):
            re.compile(pattern)
    if level == 'L3-identifier-insensitive':
        allowed |= {'identifierKinds', 'functionScopes', 'blockScopes', 'barriers', 'bindingRules', 'nonRenamable',
                    'notOccurrences', 'disqualifying', 'formatCapture', 'bodyDisqualifiers', 'patternLaw',
                    'parameterLaw'}
        for key in ('identifierKinds', 'functionScopes', 'blockScopes', 'barriers'):
            for k in row[key]:
                r.named(k, w)
        for b in row['bindingRules']:
            keys_ok(b, {'kind', 'child', 'field', 'scope', 'when', 'anonymous', 'position', 'alternativeField'}, w)
            r.named(b['kind'], w)
            if 'child' in b:
                r.named(b['child'], w)
            if 'field' in b:
                r.field(b.get('child', b['kind']), b['field'], w)
            if 'alternativeField' in b:
                r.field(b['kind'], b['alternativeField'], w)
            for token in b.get('anonymous', []):
                r.anon(token, w)
        for b in row['nonRenamable']:
            keys_ok(b, {'kind', 'field', 'scope', 'when', 'firstChild', 'names'}, w)
            r.named(b['kind'], w)
            if 'field' in b:
                r.field(b['kind'], b['field'], w)
            if 'firstChild' in b:
                r.named(b['firstChild'], w)
        for d in row['notOccurrences'] + row['disqualifying']:
            keys_ok(d, {'kind', 'within', 'field'}, w)
            if 'kind' in d:
                r.named(d['kind'], w)
            for k in d.get('within', []):
                r.named(k, w)
                if 'field' in d:
                    r.field(k, d['field'], w)
        if 'formatCapture' in row:
            for k in row['formatCapture']['kinds'] + row['formatCapture']['within']:
                r.named(k, w)
        for d in row['bodyDisqualifiers']:
            keys_ok(d, {'kind', 'field', 'identifierText', 'descendant'}, w)
            r.named(d['kind'], w)
            if 'field' in d:
                r.field(d['kind'], d['field'], w)
            if 'descendant' in d:
                r.named(d['descendant'], w)
        walk_pattern_law(r, row['patternLaw'], w + '/patternLaw')
    keys_ok(row, allowed, w)


# ---------------------------------------------------------------- the design encoder
def load_canonical(deps):
    if deps:
        sys.path.insert(0, deps)
    else:   # canonical() and typed() need nothing from jsonschema; stub it for those two only
        stub = types.ModuleType('jsonschema')

        class _V:
            TYPE_CHECKER = types.SimpleNamespace(redefine=lambda *a, **k: None)
        stub.Draft202012Validator, stub.ValidationError = _V, Exception
        stub.validators = types.SimpleNamespace(extend=lambda *a, **k: None)
        sys.modules['jsonschema'] = stub
    spec = importlib.util.spec_from_file_location('canonical',
                                                  ARCH / 'docs/coop/design-corrections/foundation/canonical.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def run_fixtures(docs):
    spec = importlib.util.spec_from_file_location('reference_syn_ns', HERE / 'reference_syn_ns.py')
    R = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(R)
    nrows = R.rows(docs['normalizer'])
    fx = json.loads(read(f'{UNIT}/evidence/fixtures.json'))
    out = []
    for f in fx['fixtures']:
        g, exp = f['grammarId'], f['expect']
        built = {}
        for name, case in f['cases'].items():
            src = case['source'].encode('utf-8')
            built[name] = (src, R.build(src, case['tree']))
        result = {'id': f['id'], 'finding': f['finding']}
        if 'tokens' in exp:
            got = {}
            for name, (src, root) in built.items():
                (owner, body), = R.bodies(root, nrows[g])
                got[name] = {}
                for lv in ('L1-lexical', 'L2-comment-insensitive'):
                    stream = [[k, v.decode('utf-8')] for k, v in R.tokens(src, body, R.rows(docs[lv])[g], lv)]
                    assert stream == exp['tokens'][name][lv], (f['id'], name, lv, stream)
                    got[name][lv] = stream
            for lv in exp.get('distinct', []):
                assert got['A'][lv] != got['B'][lv], (f['id'], lv)
            for lv in exp.get('equal', []):
                assert got['A'][lv] == got['B'][lv], (f['id'], lv)
            if 'r1Equal' in exp:
                for lv in exp['r1Equal']['levels']:
                    streams = []
                    for name, (src, root) in built.items():
                        (owner, body), = R.bodies(root, nrows[g])
                        row = dict(R.rows(docs[lv])[g])
                        ov = exp['r1Equal']['override']
                        if 'lineTerminators' in ov:
                            row['lineTerminators'] = ov['lineTerminators']
                        if 'atomicKindsRemove' in ov:
                            row['atomicKinds'] = [k for k in row['atomicKinds'] if k not in ov['atomicKindsRemove']]
                        streams.append(R.tokens(src, body, row, lv))
                    assert streams[0] == streams[1], ('r1 rule did not reproduce the defect', f['id'], lv)
                result['r1DefectReproduced'] = exp['r1Equal']['levels']
            result['levelsChecked'] = ['L1-lexical', 'L2-comment-insensitive']
        if 'graphs' in exp:
            for name, (src, root) in built.items():
                graphs = []
                for owner, body in R.bodies(root, nrows[g]):
                    cf = R.CF(src, root, owner, body, nrows[g])
                    gr = cf.graph(f['path'])
                    graphs.append({'owner': '/'.join(cf.prefix), **gr})
                assert graphs == exp['graphs'][name], (f['id'], name, graphs)
                if exp.get('disjointGraphs'):
                    seen = set()
                    for gr in graphs:
                        assert not (set(gr['nodes']) & seen), f['id']
                        seen |= set(gr['nodes'])
                if exp.get('r1Collide'):
                    sets = []
                    for owner, body in R.bodies(root, nrows[g]):
                        cf = R.CF(src, root, owner, body, nrows[g])
                        cf.prefix = []                       # r1's literal strict-ancestor reading
                        sets.append(set(cf.graph(f['path'])['nodes']))
                    assert sets[0] == sets[1], ('r1 reading did not collide', f['id'])
                    result['r1DefectReproduced'] = 'identities collide under the strict-ancestor prefix'
            result['graphsChecked'] = len(exp['graphs']['A'])
        out.append(result)
    return out


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--grammars', default=SCRATCH_SRC)
    parser.add_argument('--deps')
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    grammar = pinned(args.grammars)
    tables = {row: census(src) for row, (src, _repo, _pins) in grammar.items()}
    C = load_canonical(args.deps)

    members = {
        'normalizer': f'{CLOSURE}/opensip-interface/grammar/normalizer.v1.json',
        'map': f'{CLOSURE}/opensip-interface/normalization/specification-map.v1.json',
        **{lv: f'{CLOSURE}/opensip-interface/normalization/levels/{lv}.v1.json' for lv in LEVELS},
    }
    docs = {}
    for name, path in members.items():
        raw = read(path)
        value = C.parse(raw)
        assert C.canonical(value) == raw, f'{path} is not canonical'
        assert len(raw) <= (1 << 20 if name == 'map' else 4 << 20)
        docs[name] = value

    # 3. references
    per_doc = {}
    refs = {row: Refs(tables[row]) for row in tables}
    normalizer = docs['normalizer']
    assert [r['grammarId'] for r in normalizer['rows']] == sorted(GRAMMARS)
    for row in normalizer['rows']:
        walk_normalizer_row(refs[row['grammarId']], row)
    per_doc['normalizer'] = {g: len(refs[g].items) for g in refs}
    for lv in LEVELS:
        doc = docs[lv]
        assert doc['level'] == lv and doc['normalizerId'] == normalizer['normalizerId']
        assert [r['grammarId'] for r in doc['rows']] == sorted(GRAMMARS)
        before = {g: len(refs[g].items) for g in refs}
        for row in doc['rows']:
            walk_level_row(refs[row['grammarId']], row, lv)
        per_doc[lv] = {g: len(refs[g].items) - before[g] for g in refs}

    # 5. the map
    spec_map = docs['map']
    assert spec_map['normalizerId'] == normalizer['normalizerId'] == 'opensip.syntax.normalizer'
    assert [r['level'] for r in spec_map['levels']] == LEVELS
    for row in spec_map['levels']:
        assert row['specificationDigest'] == sha(read(members[row['level']])), row['level']
    validated = False
    if args.deps:
        ids = json.loads(read(IDS))
        schema = {'$schema': ids.get('$schema', 'https://json-schema.org/draft/2020-12/schema'),
                  '$defs': ids['$defs'], '$ref': '#/$defs/normalization-specification-map'}
        C.validate(schema, spec_map)
        validated = True

    # 6. consistency
    l1, l2, l3 = (docs[lv]['rows'] for lv in LEVELS[1:])
    for a, b, c in zip(l1, l2, l3):
        assert a['atomicKinds'] == b['atomicKinds'] == c['atomicKinds']
        for key in ('commentKinds', 'docMarkerKinds', 'directivePatterns'):
            assert b.get(key) == c.get(key)
    assert docs['L2-comment-insensitive']['commentLaw'] == docs['L3-identifier-insensitive']['commentLaw']
    for nrow, lrow in zip(normalizer['rows'], l3):   # one pattern law, stated in both self-contained documents
        assert nrow['patternLaw'] == lrow['patternLaw'] and nrow['parameterLaw'] == lrow['parameterLaw']
    assert docs['L1-lexical']['tokenLaw'] == docs['L2-comment-insensitive']['tokenLaw'] == \
        docs['L3-identifier-insensitive']['tokenLaw']
    ne = read(NE).decode('utf-8')
    section = ne[ne.index('### 6.2 Parameters (selected)'):ne.index('### 6.3 Bodies')]
    p = normalizer['parameters']
    expected = {'minOccurrences': r'`minOccurrences (\d+)`', 'minBodyBytes': r'`minBodyBytes (\d+)` \(exact\)',
                'minTokensLevels': r'`minTokens (\d+)` \(L1–L3', 'minTokensNear': r'`minTokens (\d+)` \(near\)',
                'nearThresholdMillionths': r'`nearThreshold (\d+)`',
                'maxCandidatesPerGroup': r'`maxCandidatesPerGroup (\d+)`',
                'maxGroupsPerUniverse': r'`maxGroupsPerUniverse (\d+)`'}
    for key, pattern in expected.items():
        assert int(re.search(pattern, section).group(1)) == p[key], key

    # 7. fixtures
    fixtures_result = run_fixtures(docs)

    report = {
        'schemaVersion': 1,
        'standing': ('Generated by check_syn_ns.py: the pinned grammar census and every node kind, anonymous token and '
                     'field that SYN-NS names, each verified against that census. Evidence, not law.'),
        'grammars': {row: {'repository': grammar[row][1], 'pins': grammar[row][2], 'languageAbi': tables[row]['abi'],
                           'symbols': tables[row]['symbolCount'],
                           'visibleNamed': len(tables[row]['named']),
                           'visibleAnonymous': len(tables[row]['anonymous']),
                           'fields': len(tables[row]['fields'])} for row in sorted(tables)},
        'referencesChecked': per_doc,
        'distinctReferences': {row: sorted({f'{a}:{b}' for a, b in refs[row].items}) for row in sorted(refs)},
        'closure': {name: {'path': members[name], 'bytes': len(read(members[name])),
                           'sha256': sha(read(members[name]))} for name in members},
        'mapValidatedWithExactValidator': validated,
        'fixtures': fixtures_result,
    }
    out = (json.dumps(report, indent=2, ensure_ascii=False) + '\n').encode('utf-8')
    target = ARCH / UNIT / 'evidence/kinds-report.json'
    if args.write:
        target.write_bytes(out)
    else:
        assert target.read_bytes() == out, 'kinds-report.json differs; rerun with --write and rebuild'
    subject_path = ARCH / BASE / 'syn-ns-subject.json'
    if subject_path.exists() and not args.write:
        subject = json.loads(subject_path.read_bytes())
        for row in subject['files']:
            assert sha(read(row['path'])) == row['sha256'] and len(read(row['path'])) == row['bytes'], row['path']
    print(json.dumps({'passed': True, 'referencesChecked': per_doc, 'fixtures': fixtures_result,
                      'distinct': {row: len(report['distinctReferences'][row]) for row in report['distinctReferences']},
                      'mapValidatedWithExactValidator': validated, 'wrote': args.write}, indent=1))


if __name__ == '__main__':
    main()
