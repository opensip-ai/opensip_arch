"""S10c checks: TSR-1's successor of S10's registry and S10b's native-model copies (unit C2b-1b, LD-Q-160).

Run from the architecture checkout root:

    python3 -I -B docs/implementation/m3/config-discovery-b/s10c-tsr1/evidence/check.py

It reads S10's public detail registry and S10b's two native-model copies (the parents), TSR-1's erratum E3 r3,
and this unit's three successor files, as text, JSON and Python syntax trees; it executes neither model. It checks
that each model copy is its S10b parent with exactly E3's 290-byte clause appended to the remedy keyed by
`native.typescript-config-unresolved`, and nothing else; that the registry is S10's with exactly R-10.1's eight
profile alias rows added in sorted position (as one inserted block), and nothing else; and that each new row's selector names a
present file. Then it plants negative controls (mutants), each of which must fail. It writes `checks.json` beside
itself.
"""
from pathlib import Path
import ast
import difflib
import hashlib
import json
import sys

UNIT = Path('docs/implementation/m3/config-discovery-b')
HERE = UNIT / 's10c-tsr1'
COPIES = ('native_evidence_model.py', 'native_evidence_model.v2.py')
# The parents, pinned: S10b's selected model copies (contract successor 172) and S10's registry (contract successor 167).
PARENT_PINS = {
    UNIT / 's10b-remedy/reference/native_evidence_model.py': (322096, 'bdfd8373355e82c99057fa3235284acd64f28a03efcebf94b9c540c16e515b2b'),
    UNIT / 's10b-remedy/reference/native_evidence_model.v2.py': (321976, 'd645540782a6291ae6416f882bee5c6216c785ffb8f83c24099ade7b3e13b4bf'),
    UNIT / 's10-tsc/registry/public-detail-registry.v1.json': (67246, '1cf1269298d056d07aa846ad8efe2af9a2859c10302dc8e726ded13c9c149c48'),
}
# TSR-1 erratum E3 r3 (adopted, LD-COORD-E3), the source of the clause.
TSR1 = Path('docs/implementation/m3/snapshot-plan-c/tsr1')
E3 = (TSR1 / 'ERRATUM-E3-r3.md', 6246, '1c7901a6814391cd5f83fd524c87137680b93809b9f5ddda5da042022719a0af')
# The successors, pinned as the product's vector generator pins them (tools/host/typescript_config_vectors.py).
SUCCESSOR_PINS = {
    HERE / 'reference/native_evidence_model.py': (322386, '193fb6d961b13a1f15c50bcb7d34c1c8a3e1c8aac0b5e9d528c2a29cf0c3e78f'),
    HERE / 'reference/native_evidence_model.v2.py': (322266, '49ee8dd9befc6f350adcb632f36d23732c10e6acaf4d329b32f55cb74d349dea'),
    HERE / 'registry/public-detail-registry.v1.json': (69037, 'a25db186e03803d518ba223e40e7c974cedcd3962e38045bca5158906a51c7ab'),
}
KEY = 'native.typescript-config-unresolved'
CLAUSE_BYTES = 290
REMEDY_MAX = 1024  # DomainDetail.remedy is BoundedText, maxLength 1024 (TSR-1 R-10.3, E3)
# R-10.1's eight profile internal codes, each aliased to the existing public code.
PROFILE_CODES = (
    'native.typescript-profile-bound',
    'native.typescript-profile-option-malformed',
    'native.typescript-profile-option-unsupported',
    'native.typescript-profile-option-value-unsupported',
    'native.typescript-profile-package-json-malformed',
    'native.typescript-profile-path-outside-project',
    'native.typescript-profile-root-unsupported',
    'native.typescript-profile-spec-malformed',
)
SELECTOR = 'docs/implementation/m3/snapshot-plan-c/tsr1/TSR-1-r4.md R-10.1'


class Fail(Exception):
    pass


def require(condition, message):
    if not condition:
        raise Fail(message)


def pinned(path, size, sha):
    data = path.read_bytes()
    require(len(data) == size and hashlib.sha256(data).hexdigest() == sha,
            f'{path}: {len(data)} bytes, sha256 {hashlib.sha256(data).hexdigest()}; pinned {size} {sha}')
    return data


def clause_of(erratum):
    """E3 r3's replacement clause: the one block-quoted backtick span that begins `; or, for an option`."""
    spans = [line[3:-1] for line in erratum.split('\n') if line.startswith('> `; or, for an option') and line.endswith('`')]
    require(len(spans) == 1, 'E3 r3 holds exactly one quoted replacement clause')
    clause = spans[0]
    require(len(clause.encode('ascii')) == CLAUSE_BYTES, f'the E3 clause is {CLAUSE_BYTES} ASCII bytes')
    return clause


def remedies(text, name):
    """The literal `PUBLIC_ROUTE_REMEDIES` dict of one model copy, from its syntax tree."""
    tree = ast.parse(text, name)
    found = [n for n in tree.body if isinstance(n, ast.Assign)
             and any(isinstance(t, ast.Name) and t.id == 'PUBLIC_ROUTE_REMEDIES' for t in n.targets)]
    require(len(found) == 1 and isinstance(found[0].value, ast.Dict), name + ': one literal PUBLIC_ROUTE_REMEDIES')
    return ast.literal_eval(found[0].value)


def check_model(parent, successor, clause, name):
    p_lines, s_lines = parent.split('\n'), successor.split('\n')
    require(len(p_lines) == len(s_lines), name + ': same line count as the parent')
    changed = [i for i, (a, b) in enumerate(zip(p_lines, s_lines)) if a != b]
    require(len(changed) == 1, f'{name}: exactly one line differs from the parent ({len(changed)})')
    old, new = remedies(parent, name + ' parent'), remedies(successor, name)
    require(set(old) == set(new), name + ': the same remedy keys')
    require(all(old[k] == new[k] for k in old if k != KEY), name + ': every other remedy unchanged')
    require(new[KEY] == old[KEY] + clause, name + ": the remedy is S10b's followed, with no other change, by E3's clause")
    require(len(new[KEY]) <= REMEDY_MAX, f'{name}: the remedy is {len(new[KEY])} characters, within {REMEDY_MAX}')
    return new[KEY]


def check_registry(parent, successor):
    p, s = json.loads(parent), json.loads(successor)
    require(set(p) == set(s), 'registry: the same top-level members')
    require(all(p[k] == s[k] for k in p if k != 'internalAliases'), 'registry: every member but internalAliases unchanged')
    pa, sa = p['internalAliases'], s['internalAliases']
    require([r for r in sa if r in pa] == pa, "registry: every S10 alias row kept, in its order")
    added = [r for r in sa if r not in pa]
    require([r.get('internalCode') for r in added] == list(PROFILE_CODES),
            'registry: exactly the eight R-10.1 profile codes added')
    require(len(sa) == len(pa) + len(PROFILE_CODES), 'registry: no row removed or duplicated')
    codes = [r.get('internalCode') for r in sa]
    require(codes == sorted(codes), "registry: the alias rows stay sorted by internalCode, as S10's are")
    require(all(r == {'internalCode': r['internalCode'], 'publicCode': KEY, 'selector': SELECTOR} for r in added),
            'registry: each added row aliases to native.typescript-config-unresolved with the TSR-1 R-10.1 selector')
    ops = [op for op in difflib.SequenceMatcher(None, parent.split('\n'), successor.split('\n'), autojunk=False).get_opcodes()
           if op[0] != 'equal']
    require(len(ops) == 1 and ops[0][0] == 'insert', 'registry: the bytes are the parent with one inserted block')
    require(Path(SELECTOR.split(' ')[0]).is_file(), 'registry: the selector names a present file')


def run(models, registry, parents, clause):
    remedy = [check_model(parents[c], models[c], clause, c) for c in COPIES]
    require(remedy[0] == remedy[1], 'both copies register the same remedy')
    check_registry(parents['registry'], registry)
    return remedy[0]


def main():
    out = {'unit': 'S10c (TSR-1, C2b-1b)', 'checks': [], 'mutants': []}
    try:
        parents = {}
        for path, (size, sha) in PARENT_PINS.items():
            data = pinned(path, size, sha).decode('utf-8')
            parents['registry' if path.suffix == '.json' else path.name] = data
        clause = clause_of(pinned(*E3).decode('utf-8'))
        succ = {path: pinned(path, size, sha).decode('utf-8') for path, (size, sha) in SUCCESSOR_PINS.items()}
        models = {c: succ[HERE / 'reference' / c] for c in COPIES}
        registry = succ[HERE / 'registry/public-detail-registry.v1.json']
        remedy = run(models, registry, parents, clause)
        out['checks'] = ['parents, E3 r3 and successors at their pinned bytes', 'each model copy: one line, E3 clause appended',
                         'every other remedy unchanged; both copies agree', f'remedy {len(remedy)} characters <= {REMEDY_MAX}',
                         'registry: S10 plus exactly the eight R-10.1 rows; one inserted block', 'selector file present']
    except Fail as e:
        out['result'] = 'FAIL'; out['failure'] = str(e)
        print(json.dumps(out, indent=1)); (HERE / 'evidence/checks.json').write_text(json.dumps(out, indent=1) + '\n'); sys.exit(1)

    key_line = f'    "{KEY}": "'
    mutants = {
        'clause altered by one character': lambda m, r: ({**m, COPIES[0]: m[COPIES[0]].replace('package.json or toolchain', 'package.json or toolchian', 1)}, r),
        'v2 copy left at its parent': lambda m, r: ({**m, COPIES[1]: parents[COPIES[1]]}, r),
        'another remedy altered': lambda m, r: ({**m, COPIES[0]: m[COPIES[0]].replace('break any extends cycle', 'break every extends cycle', 1)}, r),
        'a second line changed (comment added)': lambda m, r: ({**m, COPIES[0]: m[COPIES[0]].replace(key_line, '    # S10c\n' + key_line, 1)}, r),
        'the two copies disagreeing': lambda m, r: ({**m, COPIES[1]: m[COPIES[1]].replace(clause, clause[:-1] + 'S', 1)}, r),
        'registry: one profile row dropped': lambda m, r: (m, _drop_row(r)),
        'registry: a row aliased to another public code': lambda m, r: (m, r.replace(f'"publicCode": "{KEY}",\n      "selector": "{SELECTOR}"', f'"publicCode": "native.typescript-config-malformed",\n      "selector": "{SELECTOR}"', 1)),
        'registry: a selector naming another path': lambda m, r: (m, r.replace(SELECTOR, SELECTOR.replace('snapshot-plan-c/tsr1', 'tsr1'), 1)),
        "registry: one of S10's rows altered": lambda m, r: (m, r.replace('"internalCode": "native.typescript-config-bound"', '"internalCode": "native.typescript-config-boundX"', 1)),
        'registry: the profile rows appended out of sorted order': lambda m, r: (m, _append_unsorted(r)),
    }
    for name, plant in mutants.items():
        m, r = plant(models, registry)
        try:
            run(m, r, parents, clause)
            out['mutants'].append({'mutant': name, 'result': 'SURVIVED'})
        except (Fail, SyntaxError, ValueError, KeyError) as e:
            out['mutants'].append({'mutant': name, 'result': 'KILLED', 'by': str(e)})
    survived = [m['mutant'] for m in out['mutants'] if m['result'] != 'KILLED']
    out['result'] = 'PASS' if not survived else 'FAIL'
    if survived:
        out['failure'] = 'mutants survived: ' + ', '.join(survived)
    (HERE / 'evidence/checks.json').write_text(json.dumps(out, indent=1) + '\n')
    print(json.dumps(out, indent=1))
    sys.exit(0 if not survived else 1)


def _drop_row(registry):
    s = json.loads(registry)
    s['internalAliases'] = [r for r in s['internalAliases'] if r['internalCode'] != PROFILE_CODES[-1]]
    return json.dumps(s, indent=2)


def _append_unsorted(registry):
    s = json.loads(registry)
    rows = s['internalAliases']
    s['internalAliases'] = [r for r in rows if r['internalCode'] not in PROFILE_CODES] + [r for r in rows if r['internalCode'] in PROFILE_CODES]
    return json.dumps(s, indent=2)


if __name__ == '__main__':
    main()
