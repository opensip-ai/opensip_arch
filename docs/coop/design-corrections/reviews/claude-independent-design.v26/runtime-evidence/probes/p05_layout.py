"""Probe 05 — independent verification of the proposed layout's own stated laws.
Checks naming/suffix rules, generated-output coverage, pure-layer dependency direction
and acyclicity DIRECTLY from repository-file-inventory.v1.json, not from the checker."""
import json, os, re

ROOT = '/tmp/opensip-design-corrections/candidate-subject.v26'
inv = json.load(open(os.path.join(ROOT, 'docs/v2/architecture/repository-file-inventory.v1.json')))
files, pkgs = inv['files'], inv['packages']
OUT = {}

# --- package graph ---
edges = {p['id']: list(p.get('dependencies') or []) for p in pkgs}
OUT['packages'] = {'count': len(pkgs), 'ids': sorted(edges)}
unknown = sorted({d for ds in edges.values() for d in ds if d not in edges})
OUT['unknown_dependency_targets'] = unknown

# acyclicity (DFS)
WHITE, GREY, BLACK = 0, 1, 2
color = {k: WHITE for k in edges}
cycles = []
def dfs(n, stack):
    color[n] = GREY
    for d in edges.get(n, []):
        if d not in color:
            continue
        if color[d] == GREY:
            cycles.append(stack + [n, d])
        elif color[d] == WHITE:
            dfs(d, stack + [n])
    color[n] = BLACK
for n in list(edges):
    if color[n] == WHITE:
        dfs(n, [])
OUT['cycles'] = cycles

# pure-layer direction law (ch14: contracts none; identity->contracts; evaluator->identity,contracts)
PURE = {'opensip-contracts': set(), 'opensip-identity': {'opensip-contracts'},
        'opensip-evaluator': {'opensip-contracts', 'opensip-identity'},
        'opensip-syntax': {'opensip-contracts', 'opensip-identity'}}
OUT['pure_layer_violations'] = {
    k: sorted(set(edges.get(k, [])) - v) for k, v in PURE.items() if set(edges.get(k, [])) - v}
# nothing may depend INTO a pure crate from a pure crate in the wrong direction
OUT['reverse_pure_edges'] = {k: [d for d in edges.get(k, []) if d in PURE and d not in PURE[k]]
                             for k in PURE if [d for d in edges.get(k, []) if d in PURE and d not in PURE[k]]}
# storage/security stated edges
for k in ('opensip-storage', 'opensip-security', 'opensip-host', 'opensip-lifecycle'):
    OUT.setdefault('stated_edges', {})[k] = sorted(edges.get(k, []))

# --- naming law checks (ch14 "Naming rules") ---
RUST_STD = {'Cargo.toml', 'Cargo.lock', 'lib.rs', 'main.rs', 'mod.rs', 'rust-toolchain.toml'}
TS_STD = {'package.json', 'tsconfig.json', 'index.ts'}
viol = {'rust_module_case': [], 'ts_module_case': [], 'factory_suffix': [], 'renderer_suffix': [],
        'store_suffix': [], 'generated_location': [], 'generated_flag': [], 'test_name': [],
        'banned_catchall': []}
BANNED = {'utils', 'helpers', 'misc', 'manager', 'types'}
factories, renderers, stores, generated, tests = [], [], [], [], []
for f in files:
    p, role, gen = f['path'], f.get('role', ''), bool(f.get('generated'))
    base = p.rsplit('/', 1)[-1]
    stem = base.rsplit('.', 1)[0]
    ext = base.rsplit('.', 1)[-1] if '.' in base else ''
    if gen:
        generated.append(p)
        if '/generated/' not in p:
            viol['generated_location'].append(p)
    if '/generated/' in p and not gen:
        viol['generated_flag'].append(p)
    if ext == 'rs' and base not in RUST_STD:
        if not re.fullmatch(r'[a-z0-9]+(_[a-z0-9]+)*\.rs', base):
            viol['rust_module_case'].append(p)
    if ext == 'ts' and base not in TS_STD:
        core = base[:-3]
        if core.endswith('.test'):
            core = core[:-5]
        if not re.fullmatch(r'[a-z0-9]+(-[a-z0-9]+)*', core):
            viol['ts_module_case'].append(p)
    if stem in BANNED or stem.split('_')[-1] in BANNED or stem.split('-')[-1] in BANNED:
        viol['banned_catchall'].append(p)
    if 'factory' in stem:
        factories.append(p)
        if not (stem.endswith('_factory') or stem.endswith('-factory')):
            viol['factory_suffix'].append(p)
    if role == 'factory' and not (stem.endswith('_factory') or stem.endswith('-factory')):
        viol['factory_suffix'].append(p)
    if role == 'renderer' and not (stem.endswith('_renderer') or stem.endswith('-renderer')):
        viol['renderer_suffix'].append(p)
    if role == 'renderer':
        renderers.append(p)
    if role == 'store' and not (stem.endswith('_store') or stem.endswith('-store')):
        viol['store_suffix'].append(p)
    if role == 'store':
        stores.append(p)
    if role == 'test':
        tests.append(p)
        ok = base.endswith('_tests.rs') or base.endswith('.test.ts')
        if not ok:
            viol['test_name'].append(p)
OUT['naming_violations'] = {k: v for k, v in viol.items() if v}
OUT['factories'] = sorted(set(factories))
OUT['renderers'] = sorted(renderers)
OUT['stores'] = sorted(stores)
OUT['generated'] = sorted(generated)
OUT['generated_count'] = len(generated)
OUT['tests'] = sorted(tests)
OUT['roles'] = sorted({f.get('role', '') for f in files})

json.dump(OUT, open('/tmp/opensip-design-corrections/claude-independent-design.v26/probes/p05-result.json', 'w'), indent=1)
print(json.dumps(OUT, indent=1))
