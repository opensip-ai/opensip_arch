"""Check the B2-a reference refresh (discovery-defaults.sx1-r1.py) against the accepted pruning copy.

1. All 49 pruning controls are rerun on both copies; every result is unchanged and equals its expectation.
2. SX-1 controls (B-S1 SX-1, LD-3; NE:714; SL:195).
3. Version-3 boundary inventory controls; every converter output validates as AdmittedBoundaryInventoryV3 in the
   SLS bundle merged with B-S1's additions under its merge rule.
4. AST: only the named functions and constants differ from the pruning copy; one helper is added.
Design evidence only: supplied paths, no filesystem, no product, no qualification."""
from pathlib import Path
import argparse, ast, copy, hashlib, importlib.util, json, sys

DESIGN = 'docs/coop/design-corrections/'
B_S1 = 'docs/implementation/m3/config-discovery-b/b-s1/schemas/security-lifecycle.schemas.v1.b-s1-additions.json'
PRUNING = 'docs/implementation/m3/config-discovery-b/discovery-pruning-reference-r2/reference/discovery-defaults.pruning-r1.py'
ARCH = ((PRUNING, None), (B_S1, None), (DESIGN + 'security/security-lifecycle.schemas.v1.json', 'f66d2c617084825e3cdb9a855a151c10aa66625968b40ef91fc6bb3be39423f4'),
        (DESIGN + 'foundation/canonical.py', 'd47f25db0fb09ceb84282a89fdf74055cb81ccb9de26f85a5a70b032b9a6b442'))
CHANGED_FUNCTIONS = ['boundary_inventory_from_provenance', 'cargo_roots_from_markers', 'classify_path', 'conventional_excluded_prefixes',
                     'enumerate_units', 'pruned_anchors_from_directories']
ADDED_FUNCTIONS = ['_custody_state']
CHANGED_CONSTANTS = ['BOUNDARY_INVENTORY_VERSION', 'CURRENT_PROVENANCE_VERSION', 'DISCOVERY_DEFAULTS_VERSION', 'PRUNED_TREE_ROW_VERSION', 'PRUNE_REASONS',
                     'SUPPORTED_BOUNDARY_INVENTORY_VERSIONS', 'SUPPORTED_PROVENANCE_VERSIONS']
ADDED_CONSTANTS = ['OPENSIP_CUSTODY_STATE']


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def plain(v):
    if isinstance(v, (set, frozenset)): return sorted(v)
    if isinstance(v, tuple): return list(v)
    if isinstance(v, dict) and any(isinstance(k, tuple) for k in v): return sorted([list(k) for k in v])
    return v


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--architecture', type=Path, required=True); ap.add_argument('--candidate', type=Path, required=True)
    ap.add_argument('--packages-root', type=Path, required=True); ap.add_argument('--out', type=Path, required=True); a = ap.parse_args()
    A = a.architecture
    pins = {}
    for rel, want in ARCH:
        raw = (A / rel).read_bytes(); got = hashlib.sha256(raw).hexdigest()
        assert want is None or got == want, rel
        pins[rel] = dict(bytes=len(raw), sha256=got)
    sys.path.insert(0, str(a.packages_root / 'tools/contracts/python-packages'))
    canonical = load('canonical_b2a', A / DESIGN / 'foundation/canonical.py')
    old = load('dd_pruning', A / PRUNING); new = load('dd_sx1', a.candidate)
    rows = []

    def add(group, label, call, args, expected, kwargs=None, both=True):
        kwargs = kwargs or {}
        after = plain(getattr(new, call)(*args, **kwargs))
        assert after == plain(expected), (label, after, expected)
        row = dict(group=group, label=label, function=call, args=args, kwargs=kwargs, result=after)
        if both:
            before = plain(getattr(old, call)(*args, **kwargs)); assert before == after, (label, before, after); row['pruningCopyEqual'] = True
        rows.append(row)

    # 1. The pruning controls (discovery-pruning-reference-r2/evidence/check.py), on both copies.
    for root in ['', 'workspace']:
        pre = root + '/' if root else ''
        for segment in ['node_modules', '.git', '.hg', '.svn', '.jj']:
            reason = 'dependency-tree' if segment == 'node_modules' else 'vcs-tree'
            add('pruning', pre + 'target-before-' + segment, 'classify_path', [pre + 'target/' + segment + '/pkg/file', [root]], (pre + 'target', 'cargo-build-output'))
            add('pruning', pre + segment + '-before-target', 'classify_path', [pre + segment + '/target/pkg/file', [root, pre + segment]], (pre + segment, reason))
            add('pruning', pre + 'ordinary-target-no-parent-marker-' + segment, 'classify_path', [pre + 'src/target/' + segment + '/file', [root]], (pre + 'src/target/' + segment, reason))
        add('pruning', pre + 'plain-target', 'classify_path', [pre + 'target/debug/file', [root]], (pre + 'target', 'cargo-build-output'))
        add('pruning', pre + 'unrooted-target', 'classify_path', [pre + 'packages/target/index.ts', [root]], None)
        add('pruning', pre + 'substring-target', 'classify_path', [pre + 'targetish/node_modulesish/file', [root]], None)
        markers = [pre + 'Cargo.toml', pre + 'target/dependency/Cargo.toml', pre + 'node_modules/pkg/Cargo.toml', pre + '.git/Cargo.toml', pre + 'src/Cargo.toml']
        for i, perm in enumerate([markers, list(reversed(markers)), markers[2:] + markers[:2]]):
            add('pruning', pre + 'cargo-root-pruned-marker-order-' + str(i), 'cargo_roots_from_markers', [perm], {root, pre + 'src'})
        add('pruning', pre + 'missing-parent-is-normal-source', 'cargo_roots_from_markers', [[pre + 'target/inner/Cargo.toml']], {pre + 'target/inner'})
    markers = ['Cargo.toml', 'target/Cargo.toml'] + ['target/node_modules/pkg' + str(i) + '/package.json' for i in range(4200)]
    add('pruning', '4200-nested-installed-markers-one-outer-cargo-anchor', 'enumerate_units', [markers],
        dict(unitDirs=[''], prunedTrees=[dict(path='target', reason='cargo-build-output', markerCount=None, markerCountBasis='not-enumerated')], refusal=None),
        dict(observed_directories=['target', 'target/node_modules'], marker_inventory_basis='not-enumerated'))
    add('pruning', '4200-nested-installed-markers-observed-inventory', 'enumerate_units', [markers],
        dict(unitDirs=[''], prunedTrees=[dict(path='target', reason='cargo-build-output', markerCount=4201, markerCountBasis='observed-inventory')], refusal=None))
    markers = ['package.json'] + ['node_modules/p' + str(i) + '/package.json' for i in range(4200)]
    add('pruning', '4200-installed-markers-remain-one-dependency-anchor', 'enumerate_units', [markers],
        dict(unitDirs=[''], prunedTrees=[dict(path='node_modules', reason='dependency-tree', markerCount=4200, markerCountBasis='observed-inventory')], refusal=None))
    for n in [4096, 4097]:
        ms = ['p' + str(i) + '/package.json' for i in range(n)]; r = new.enumerate_units(ms); assert r == old.enumerate_units(ms)
        assert (len(r['unitDirs']) == n and r['refusal'] is None) if n == 4096 else (r['unitDirs'] == [] and r['refusal'] == dict(detail='WORKSPACE_UNIT_LIMIT', unitCount=n, limit=4096))
        rows.append(dict(group='pruning', label='first-party-cap-' + str(n), pruningCopyEqual=True, unitCount=len(r['unitDirs']), refusal=r['refusal']))
    pruning_controls = len(rows); assert pruning_controls == 49, pruning_controls
    for value, wanted in [('.', ''), ('a/b/', 'a/b'), ('packages/target', 'packages/target')]:
        assert new.normalize_explicit_root(value) == old.normalize_explicit_root(value) == wanted

    # 2. SX-1.
    S = 'opensip-custody-state'
    add('sx1', 'root-anchor', 'classify_path', ['.opensip/local.json', ['']], ('.opensip', S), both=False)
    add('sx1', 'root-anchor-itself', 'classify_path', ['.opensip', []], ('.opensip', S), both=False)
    add('sx1', 'member-anchor', 'classify_path', ['m/.opensip/local.json', [], ['m']], ('m/.opensip', S), both=False)
    add('sx1', 'deep-member-anchor', 'classify_path', ['a/b/.opensip/x', [], ['a/b']], ('a/b/.opensip', S), both=False)
    add('sx1', 'elsewhere-is-source', 'classify_path', ['src/.opensip/x.ts', ['']], None)
    add('sx1', 'non-member-is-source', 'classify_path', ['m/.opensip/x.ts', []], None)
    add('sx1', 'below-member-is-source', 'classify_path', ['m/src/.opensip/x', [], ['m']], None, both=False)
    add('sx1', 'case-is-exact', 'classify_path', ['.OpenSIP/x', []], None)
    add('sx1', 'substring-is-source', 'classify_path', ['.opensipx/y', []], None)
    add('sx1', 'outermost-node-modules', 'classify_path', ['node_modules/.opensip/x', []], ('node_modules', 'dependency-tree'))
    add('sx1', 'outermost-anchor-over-node-modules', 'classify_path', ['.opensip/node_modules/x', []], ('.opensip', S), both=False)
    add('sx1', 'outermost-anchor-over-target', 'classify_path', ['.opensip/target/x', ['.opensip']], ('.opensip', S), both=False)
    add('sx1', 'outermost-target-over-member-anchor', 'classify_path', ['target/m/.opensip/x', [''], ['target/m']], ('target', 'cargo-build-output'), both=False)
    add('sx1', 'outermost-anchor-over-git', 'classify_path', ['.opensip/.git/x', []], ('.opensip', S), both=False)
    add('sx1', 'member-target-below-member', 'classify_path', ['m/target/x', ['m'], ['m']], ('m/target', 'cargo-build-output'), both=False)
    add('sx1', 'git-over-member-anchor', 'classify_path', ['.git/m/.opensip', [], ['.git/m']], ('.git', 'vcs-tree'), both=False)
    add('sx1', 'never-a-cargo-root', 'cargo_roots_from_markers', [['Cargo.toml', '.opensip/Cargo.toml', 'm/Cargo.toml', 'm/.opensip/Cargo.toml'], ['m']], {'', 'm'}, both=False)
    add('sx1', 'never-a-unit', 'enumerate_units', [['package.json', '.opensip/package.json', 'src/.opensip/package.json']],
        dict(unitDirs=['', 'src/.opensip'], prunedTrees=[dict(path='.opensip', reason=S, markerCount=None, markerCountBasis='not-enumerated')], refusal=None),
        dict(observed_directories=['.opensip', 'src/.opensip'], marker_inventory_basis='not-enumerated'), both=False)
    add('sx1', 'observed-directory-without-marker', 'enumerate_units', [['package.json']],
        dict(unitDirs=[''], prunedTrees=[dict(path='.opensip', reason=S, markerCount=0, markerCountBasis='observed-inventory')], refusal=None),
        dict(observed_directories=['.opensip']), both=False)
    add('sx1', 'unobserved-has-no-row', 'enumerate_units', [['package.json']], dict(unitDirs=[''], prunedTrees=[], refusal=None))
    add('sx1', 'member-row', 'pruned_anchors_from_directories', [['m', 'm/.opensip', 'src/.opensip'], [], ['m']], [['m/.opensip', S]], both=False)
    add('sx1', 'prefix-always', 'conventional_excluded_prefixes', [[''], []], ['.git', '.opensip', 'node_modules'], both=False)
    add('sx1', 'prefix-members', 'conventional_excluded_prefixes', [['', 'm/u'], [''], ['m']],
        ['.git', '.opensip', 'm/.opensip', 'm/u/.git', 'm/u/node_modules', 'node_modules', 'target'], both=False)
    # 2b. Codex B2AREF-1: a single-pass iterator gives exactly the list result at every entry point that forwards
    # member_roots (and pruned_anchors_from_directories' cargo_roots) repeatedly, including observed directories
    # processed after marker classification.
    def same(label, call, make):
        listed = plain(make(lambda xs: list(xs))); once = plain(make(lambda xs: iter(list(xs))))
        assert listed == once, (label, listed, once)
        rows.append(dict(group='iterator', label=label, function=call, result=listed, iteratorEqualsList=True))
        return listed
    got = same('cargo-roots-member-iterator', 'cargo_roots_from_markers', lambda f: new.cargo_roots_from_markers(['m/Cargo.toml', 'm/.opensip/Cargo.toml', 'n/.opensip/Cargo.toml'], f(['m', 'n'])))
    assert got == ['m']
    got = same('enumerate-member-iterator', 'enumerate_units', lambda f: new.enumerate_units(['m/Cargo.toml', 'm/.opensip/package.json', 'n/.opensip/Cargo.toml', 'n/package.json'],
                                                                                             observed_directories=['m/.opensip', 'n/.opensip', 'm/target'], member_roots=f(['m', 'n'])))
    assert got['unitDirs'] == ['m', 'n'] and [(t['path'], t['reason']) for t in got['prunedTrees']] == [('m/.opensip', S), ('m/target', 'cargo-build-output'), ('n/.opensip', S)], got
    got = same('directories-member-iterator', 'pruned_anchors_from_directories', lambda f: new.pruned_anchors_from_directories(['m', 'm/.opensip', 'n/.opensip'], [], f(['m', 'n'])))
    assert got == [['m/.opensip', S], ['n/.opensip', S]], got
    got = same('directories-cargo-iterator', 'pruned_anchors_from_directories', lambda f: new.pruned_anchors_from_directories(['target', 'a/target', 'b/target'], f(['', 'a']), []))
    assert got == [['a/target', 'cargo-build-output'], ['target', 'cargo-build-output']], got
    # 3. Version 3 boundary inventory.
    bundle = json.loads((A / DESIGN / 'security/security-lifecycle.schemas.v1.json').read_bytes()); add_ = json.loads((A / B_S1).read_bytes())
    for section in ('$defs', 'schemas'):
        for k, v in add_[section].items():
            assert k not in bundle[section], k; bundle[section][k] = v

    def valid(name, value):
        schema = copy.deepcopy(bundle); schema['$ref'] = '#/schemas/' + name; canonical.validate(schema, value)

    R = '/w'
    prov = dict(schemaVersion=3, selectedRoot=R, nestedRepositories=[R + '/vendor/x'], nestedProjects=[R + '/tools/p'],
                excludedUnits=[dict(path=R + '/deep', reason='DEPTH'), dict(path=R + '/vendor/x/u', reason='INSIDE_NESTED_REPOSITORY')],
                prunedTrees=[dict(path=R + '/node_modules', reason='dependency-tree', markerCount=None, markerCountBasis='not-enumerated'),
                             dict(path=R + '/.opensip', reason=S, markerCount=None, markerCountBasis='not-enumerated')],
                memberRepositories=[dict(path=R + '/repos/b', declaredBy=[]), dict(path=R + '/repos/a', declaredBy=[])])
    inv = new.boundary_inventory_from_provenance(prov); valid('AdmittedBoundaryInventoryV3', inv)
    assert inv == dict(schemaVersion=3, source='security.discovery', selectedRoot=R, nestedRepositories=['vendor/x'], nestedProjects=['tools/p'],
                       custodyExcludedUnits=[dict(path='deep', reason='DEPTH')],
                       prunedTrees=[dict(path='.opensip', reason=S, markerCount=None, markerCountBasis='not-enumerated'),
                                    dict(path='node_modules', reason='dependency-tree', markerCount=None, markerCountBasis='not-enumerated')],
                       memberRepositories=['repos/a', 'repos/b']), inv
    assert new.boundary_excluded_prefixes(inv) == ['deep', 'tools/p', 'vendor/x']
    rows.append(dict(group='v3', label='converter-members-sorted-relative-and-not-prefixes', result=inv, schemaValid=True))
    empty = dict(prov, memberRepositories=[]); inv0 = new.boundary_inventory_from_provenance(empty); valid('AdmittedBoundaryInventoryV3', inv0); assert inv0['memberRepositories'] == []
    rows.append(dict(group='v3', label='converter-no-members', result=inv0, schemaValid=True))
    for label, value, detail in [('v2-refused', dict(prov, schemaVersion=2), 'PROVENANCE_VERSION_UNSUPPORTED:2'), ('v1-refused', dict(prov, schemaVersion=1), 'PROVENANCE_VERSION_UNSUPPORTED:1'),
                                 ('v4-unknown', dict(prov, schemaVersion=4), 'PROVENANCE_VERSION_UNKNOWN:4'), ('bool-shape', dict(prov, schemaVersion=True), 'PROVENANCE_VERSION_SHAPE'),
                                 ('member-outside-root', dict(prov, memberRepositories=[dict(path='/elsewhere/r', declaredBy=[])]), 'LOCATOR_OUTSIDE_ROOT')]:
        try:
            new.boundary_inventory_from_provenance(value); raise AssertionError(label)
        except new.BoundaryError as e:
            assert str(e) == detail, (label, str(e)); rows.append(dict(group='v3', label=label, refusal=str(e)))
    try:
        old.boundary_inventory_from_provenance(prov); raise AssertionError('pruning copy admitted v3')
    except old.BoundaryError as e:
        assert str(e) == 'PROVENANCE_VERSION_UNKNOWN:3'
    # 4. AST.
    ot = ast.parse((A / PRUNING).read_text()); nt = ast.parse(a.candidate.read_text())
    fo = {x.name: ast.dump(x) for x in ot.body if isinstance(x, (ast.FunctionDef, ast.ClassDef))}
    fn = {x.name: ast.dump(x) for x in nt.body if isinstance(x, (ast.FunctionDef, ast.ClassDef))}
    assert sorted(set(fn) - set(fo)) == ADDED_FUNCTIONS and not set(fo) - set(fn)
    assert sorted(k for k in fo if fo[k] != fn[k]) == CHANGED_FUNCTIONS

    def consts(tree):
        out = {}
        for x in tree.body:
            if isinstance(x, ast.Assign) and len(x.targets) == 1 and isinstance(x.targets[0], ast.Name): out[x.targets[0].id] = ast.dump(x.value)
            elif not isinstance(x, (ast.FunctionDef, ast.ClassDef)): out.setdefault('<other>', []).append(ast.dump(x))
        return out
    co, cn = consts(ot), consts(nt)
    doc_o, doc_n = co.pop('<other>'), cn.pop('<other>')
    assert doc_o[1:] == doc_n[1:] and doc_o[0] != doc_n[0], 'only the module docstring differs among other statements'
    assert sorted(set(cn) - set(co)) == ADDED_CONSTANTS and not set(co) - set(cn)
    assert sorted(k for k in co if co[k] != cn[k]) == CHANGED_CONSTANTS
    assert new.DISCOVERY_DEFAULTS_VERSION == 3 and new.PRUNE_REASONS[-1] == S and new.CURRENT_PROVENANCE_VERSION == 3 and new.BOUNDARY_INVENTORY_VERSION == 3 and new.PRUNED_TREE_ROW_VERSION == 3 and old.PRUNED_TREE_ROW_VERSION == 2
    report = dict(passed=True, pins=pins, candidate=dict(bytes=len(a.candidate.read_bytes()), sha256=hashlib.sha256(a.candidate.read_bytes()).hexdigest()),
                  pruningControls=pruning_controls, pruningControlsUnchanged=True, sx1Controls=sum(r['group'] == 'sx1' for r in rows), v3Controls=sum(r['group'] == 'v3' for r in rows), iteratorControls=sum(r['group'] == 'iterator' for r in rows),
                  controls=len(rows), changedFunctions=CHANGED_FUNCTIONS, addedFunctions=ADDED_FUNCTIONS, changedConstants=CHANGED_CONSTANTS, addedConstants=ADDED_CONSTANTS,
                  moduleDocstringChanged=True, rows=rows, discoveryOverRealFilesystem=False, productEdited=False, qualification=False)
    a.out.write_text(json.dumps(report, indent=1) + '\n')
    print(json.dumps({k: v for k, v in report.items() if k not in ('rows', 'pins')}))


if __name__ == '__main__':
    main()
