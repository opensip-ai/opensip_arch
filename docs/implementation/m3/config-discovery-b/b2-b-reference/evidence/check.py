"""Check B2-b0, the current discovery reference (B2-b plan r4 section 1.0).

For every case of security/discovery-cases.v1.json, three stages are run and compared:
  historical   - SLM as accepted (original DD), recorded only;
  rule-swapped - SLM with the bound B2-a reference, on the full input (pass one);
  current      - the same over the walker population (pass two): the oracle.
A difference between rule-swapped and current must be caused by the population, and fails otherwise: every
path the current result lacks must be outside the population; a changed outcome must stem from a refusing path
outside the population. Every current result validates as DiscoveryResultV3 (its pending field shape-filled,
labelled, never emitted), and every ACCEPTed result's boundary inventory validates as AdmittedBoundaryInventoryV3,
in the SLS bundle merged with B-S1's additions. The adapter controls of plan r4 run on synthetic trees.
Design evidence: supplied synthetic maps only; no filesystem tree, product code or qualification."""
from pathlib import Path
import argparse, copy, hashlib, importlib.util, json, subprocess, sys, tempfile

DESIGN = 'docs/coop/design-corrections/'
CASES = (DESIGN + 'security/discovery-cases.v1.json', None)
BUNDLE = (DESIGN + 'security/security-lifecycle.schemas.v1.json', 'f66d2c617084825e3cdb9a855a151c10aa66625968b40ef91fc6bb3be39423f4')
B_S1 = ('docs/implementation/m3/config-discovery-b/b-s1/schemas/security-lifecycle.schemas.v1.b-s1-additions.json', None)
CANONICAL = (DESIGN + 'foundation/canonical.py', 'd47f25db0fb09ceb84282a89fdf74055cb81ccb9de26f85a5a70b032b9a6b442')
LISTS = ('nestedRepositories', 'nestedProjects')


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def pinned(A, row):
    raw = (A / row[0]).read_bytes(); d = hashlib.sha256(raw).hexdigest()
    assert row[1] is None or d == row[1], row[0]
    return raw, dict(path=row[0], bytes=len(raw), sha256=d)


def paths_of(prov):
    out = set(prov.get(k, []) or []) if False else set()
    for k in LISTS:
        out |= set(prov.get(k) or [])
    for k in ('units', 'excludedUnits', 'prunedTrees'):
        out |= {r['path'] for r in prov.get(k) or []}
    return out


# Synthetic trees for the adapter controls -----------------------------------------------------------------
UID = 1000


def tree(dirs=(), files=(), vcs=(), extra=None):
    fs = {'/': dict(kind='dir', uid=0, mode='0755', dev=1), '/h': dict(kind='dir', uid=UID, mode='0700', dev=1),
          '/h/w': dict(kind='dir', uid=UID, mode='0755', dev=1)}
    for d in dirs:
        parts = d.split('/')
        for i in range(1, len(parts) + 1):
            fs.setdefault('/h/w/' + '/'.join(parts[:i]), dict(kind='dir', uid=UID, mode='0755', dev=1))
    for f in files:
        parent = f.rsplit('/', 1)[0] if '/' in f else ''
        if parent:
            parts = parent.split('/')
            for i in range(1, len(parts) + 1):
                fs.setdefault('/h/w/' + '/'.join(parts[:i]), dict(kind='dir', uid=UID, mode='0755', dev=1))
        fs['/h/w/' + f] = dict(kind='file', uid=UID, mode='0644', nlink=1, size=10)
    for v in vcs:
        fs['/h/w/' + v]['vcs'] = True
    fs.update(extra or {})
    return fs


def inp(fs, **kw):
    base = dict(invokingUid=UID, accountHome='/h', cwd='/h/w', fs=fs, prunedTreeMarkerInventory='not-enumerated')
    base.update(kw)
    return base


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--architecture', type=Path, required=True); ap.add_argument('--reference', type=Path, required=True)
    ap.add_argument('--packages-root', type=Path, required=True); ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--inject-current-fault', action='store_true', help='negative control only: the first discovery case\'s current replay raises')
    a = ap.parse_args()
    A = a.architecture
    sys.path.insert(0, str(a.packages_root / 'tools/contracts/python-packages'))
    pins = {}
    for row in (CASES, BUNDLE, B_S1, CANONICAL):
        pins[row[0]] = pinned(A, row)[1]
    canonical = module('canonical_b2b0', A / CANONICAL[0])
    ref = module('discovery_scan_reference', a.reference)
    slm_h, _ = ref.load(A, historical=True)
    slm, rule = ref.load(A)
    bundle = json.loads((A / BUNDLE[0]).read_bytes()); add = json.loads((A / B_S1[0]).read_bytes())
    for section in ('$defs', 'schemas'):
        for k, v in add[section].items():
            assert k not in bundle[section]; bundle[section][k] = v

    def valid(name, value):
        schema = copy.deepcopy(bundle); schema['$ref'] = '#/schemas/' + name; canonical.validate(schema, value)

    rows, failures = [], []

    def validate_current(result, label):
        partial = ref.project_v3(result)
        filled = dict({k: v for k, v in partial.items() if k != 'pendingFields'}, provenance=ref.shape_fill(partial))
        valid('DiscoveryResultV3', filled)
        inventory = None
        if partial['status'] == 'ACCEPT':
            inventory = ref.boundary_inventory_v3(rule, partial)
            valid('AdmittedBoundaryInventoryV3', inventory)
        return partial, inventory

    cases = json.loads((A / CASES[0]).read_bytes())['cases']
    summary = dict(cases=len(cases), discoveryCases=0, nonDiscoveryCases=0, replayed=0, v3Valid=0, inventoriesValid=0,
                   outcomeChangedByRule=0, outcomeChangedByPopulation=0, pathsRemovedByPopulation=0)
    injected = [a.inject_current_fault]

    def current_or_fault(i):
        if injected[0]:
            injected[0] = False
            raise ValueError('pass two changed the selected root or unit source (injected negative control)')
        return ref.current(slm, rule, i)

    for case in cases:
        if case.get('model', 'discovery') != 'discovery':
            summary['nonDiscoveryCases'] += 1
            rows.append(dict(id=case['id'], model=case.get('model'), classified='not a discovery-model case (boundary inventory over a supplied provenance)'))
            continue
        summary['discoveryCases'] += 1
        # r2 (B2B0REF-2): no case expects an instrument exception, so every exception fails the checker.
        try:
            hist = slm_h.discovery(copy.deepcopy(case['input']))
            swapped = slm.discovery(copy.deepcopy(case['input']))
            cur, downward, second_input = current_or_fault(case['input'])
            partial, inventory = validate_current(cur, case['id'])
        except Exception as e:
            failures.append((case['id'], 'unexpected exception', repr(e)))
            rows.append(dict(id=case['id'], exception=repr(e)))
            continue
        summary['replayed'] += 1
        summary['v3Valid'] += 1
        if inventory is not None:
            summary['inventoriesValid'] += 1
        key = lambda r: (r.get('status'), r.get('refusal'), r.get('detail'))
        row = dict(id=case['id'], historical=key(hist), ruleSwapped=key(swapped), current=key(cur), v3Valid=True, inventoryValid=inventory is not None)
        if key(hist) != key(swapped):
            summary['outcomeChangedByRule'] += 1; row['ruleCause'] = 'B2-a reference (pruning correction / SX-1)'
        if downward is not None:
            down = set(downward['fs'])
            seen = set(second_input['fs'])
            root = cur['provenance']['selectedRoot']
            # Population property: every reported downward path was observed by the downward walk.
            for path in paths_of(cur['provenance']):
                if path != root and path not in down:
                    failures.append((case['id'], 'reported path outside the downward population', path))
            if key(swapped) != key(cur):
                summary['outcomeChangedByPopulation'] += 1
                if swapped.get('path') in seen:
                    failures.append((case['id'], 'outcome changed but the refusing path was observed', swapped.get('path')))
                row['populationCause'] = 'refusing path not observed by the walker: %s' % swapped.get('path')
            elif cur['status'] == 'ACCEPT':
                removed = paths_of(swapped['provenance']) - paths_of(cur['provenance'])
                added = paths_of(cur['provenance']) - paths_of(swapped['provenance'])
                bad = [x for x in removed if x in down] + sorted(added)
                if bad:
                    failures.append((case['id'], 'path difference not explained by the population', bad))
                summary['pathsRemovedByPopulation'] += len(removed)
                if removed:
                    row['removedUnobserved'] = sorted(removed)
        rows.append(row)
    # r2 (B2B0REF-2): exact coverage.
    if not a.inject_current_fault:
        for name, want in [('discoveryCases', 64), ('nonDiscoveryCases', 4), ('replayed', 64), ('v3Valid', 64)]:
            if summary[name] != want:
                failures.append(('coverage', name, summary[name], want))

    # Adapter controls (plan r4) -----------------------------------------------------------------------------
    controls = []

    def control(label, value, expect):
        ok = value == expect
        controls.append(dict(label=label, ok=ok, got=value, expected=expect))
        if not ok:
            failures.append((label, value, expect))

    def run(i):
        cur, population, _ = ref.current(slm, rule, i)
        validate_current(cur, 'control')
        return cur, population

    def refusal(r):
        return None if r['status'] == 'ACCEPT' else (r['refusal'], r['detail'])

    # 1. Direct population assertions: a pruned anchor of each reason contributes only itself.
    for label, anchor, fs_extra_files, vcs_ in [
            ('dependency-tree', 'node_modules', ['package.json'], []),
            ('vcs-tree', '.git', ['package.json'], []),
            ('cargo-build-output', 'target', ['Cargo.toml'], []),
            ('opensip-custody-state', '.opensip', ['package.json'], [])]:
        fs = tree(dirs=[anchor + '/sub', anchor + '/repo'], files=fs_extra_files + [anchor + '/.git/HEAD', anchor + '/opensip.json', anchor + '/package.json', anchor + '/Cargo.toml', anchor + '/sub/package.json'],
                  vcs=[anchor + '/repo'])
        cur, pop = run(inp(fs))
        below = sorted(p for p in pop['fs'] if p.startswith('/h/w/' + anchor + '/'))
        control('population: %s anchor contributes only itself' % label, ('/h/w/' + anchor in pop['fs'], below), (True, []))
        control('reported: %s hidden repository never reported' % label, '/h/w/' + anchor + '/repo' in cur['provenance']['nestedRepositories'], False)
    # Codex's B2BPLAN-1 reproduction: an explicit root with a repository hidden under .opensip.
    fs = tree(dirs=['.opensip/hidden-repo'], files=['package.json'], vcs=['.opensip/hidden-repo'])
    cur, pop = run(inp(fs, explicitProject='/h/w'))
    control('codex-b2bplan-r2: hidden repository under .opensip', (cur['status'], cur['provenance']['nestedRepositories']), ('ACCEPT', []))
    # 2. Joins inside a Cargo target through both explicit sources; an ordinary target admitted.
    fs = tree(dirs=['target/u'], files=['Cargo.toml', 'target/u/package.json'])
    for source in ('explicitJoins', 'configWorkspaceRoots'):
        cur, _ = run(inp(fs, explicitProject='/h/w', **{source: ['target/u']}))
        control('cargo-target join via %s' % source, refusal(cur), ('PROJECT.EXPLICIT_PATH_INVALID', 'JOIN_INSIDE_PRUNED_TREE:cargo-build-output:target'))
    fs = tree(dirs=['target/u'], files=['target/u/package.json'])
    cur, _ = run(inp(fs, explicitProject='/h/w', explicitJoins=['target/u']))
    control('ordinary target without Cargo.toml is admitted', (cur['status'], [u['path'] for u in cur['provenance']['units']]), ('ACCEPT', ['/h/w/target/u']))
    # 3. A crossing above a pruned prefix refuses as the crossing; a repository below a prune is never reported.
    fs = tree(dirs=['r/node_modules/x'], files=['r/node_modules/x/package.json'], vcs=['r'])
    cur, _ = run(inp(fs, explicitProject='/h/w', explicitJoins=['r/node_modules/x']))
    control('crossing above a pruned prefix', refusal(cur), ('PROJECT.EXPLICIT_PATH_INVALID', 'JOIN_CROSSES_NESTED_REPOSITORY'))
    fs = tree(dirs=['node_modules/x/sub'], files=['node_modules/x/sub/package.json'], vcs=['node_modules/x'])
    cur, _ = run(inp(fs, explicitProject='/h/w', explicitJoins=['node_modules/x/sub']))
    control('repository below a pruned prefix', (refusal(cur), cur['provenance']['nestedRepositories']),
            (('PROJECT.EXPLICIT_PATH_INVALID', 'JOIN_INSIDE_PRUNED_TREE:dependency-tree:node_modules'), []))
    # 4. Nested-in-nested repositories and projects are not reported.
    fs = tree(dirs=['a/b', 'p/q'], files=['package.json', 'p/opensip.json', 'p/q/opensip.json'], vcs=['a', 'a/b'])
    cur, _ = run(inp(fs))
    control('nested in nested', (cur['provenance']['nestedRepositories'], cur['provenance']['nestedProjects']), (['/h/w/a'], ['/h/w/p']))
    # 5. An explicit root beside an unrelated sibling: nothing in the sibling is observed or reported.
    fs = tree(dirs=['a/u', 'b/repo', 'b/proj', 'b/c'], files=['a/u/package.json', 'b/proj/opensip.json', 'b/c/package.json'], vcs=['b/repo'])
    cur, pop = run(inp(fs, explicitProject='/h/w', explicitJoins=['a/u']))
    control('explicit sibling not observed', (sorted(p for p in pop['fs'] if p.startswith('/h/w/b')), cur['provenance']['nestedRepositories'], cur['provenance']['nestedProjects']), ([], [], []))
    fs2 = copy.deepcopy(fs)
    cur2, _ = run(inp(fs2, explicitProject='/h/w', configWorkspaceRoots=['a/u']))
    control('config array does not fall through', (cur2['provenance']['unitSource'], [u['path'] for u in cur2['provenance']['units']]), ('config-workspace-roots', ['/h/w/a/u']))
    # 6. Markers below an anchor never yield a unit, an exclusion or a Cargo root.
    fs = tree(dirs=['node_modules/p/target/q'], files=['package.json', 'node_modules/p/Cargo.toml', 'node_modules/p/target/q/package.json'])
    cur, _ = run(inp(fs))
    control('markers below an anchor', ([u['path'] for u in cur['provenance']['units']], cur['provenance']['excludedUnits']), (['/h/w'], []))
    # 8. r2 (B2B0REF-1): upward evidence never enters the downward population.
    fs = tree(dirs=['.opensip/hidden-repo'], files=['package.json', '.opensip/opensip.json'], vcs=['.opensip/hidden-repo'])
    cur, pop = run(inp(fs, explicitProject='/h/w', cwd='/h/w/.opensip/hidden-repo'))
    control('B2B0REF-1 repro 1: cwd below .opensip', (cur['status'], cur['provenance']['nestedRepositories'], sorted(x for x in pop['fs'] if x.startswith('/h/w/.opensip/'))), ('ACCEPT', [], []))
    fs = tree(dirs=['a/u', 'b/repo'], files=['a/u/package.json'], vcs=['b/repo'])
    cur, pop = run(inp(fs, explicitProject='/h/w', explicitJoins=['a/u'], cwd='/h/w/b/repo'))
    control('B2B0REF-1 repro 2: cwd in an unrelated sibling', (cur['status'], cur['provenance']['nestedRepositories'], sorted(x for x in pop['fs'] if x.startswith('/h/w/b'))), ('ACCEPT', [], []))
    rel = '/'.join('d' for _ in range(258))
    fs = tree(dirs=[rel], files=['package.json', rel + '/package.json'])
    cur, pop = run(inp(fs, explicitProject='/h/w', cwd='/h/w/' + rel))
    control('B2B0REF-1 depth overlap: a deep cwd adds nothing beyond the depth stop',
            ('/h/w/' + rel in pop['fs'], '/h/w/' + rel + '/package.json' in pop['fs'], [u['path'] for u in cur['provenance']['units']], cur['provenance']['excludedUnits']),
            (False, False, ['/h/w'], []))
    # 10. r3 (B2B0REF-3): a pruned anchor never carries VCS evidence from inside it.
    for label, anchor, extra_files in [('dependency-tree', 'node_modules', ['package.json']), ('vcs-tree', '.git', ['package.json']),
                                       ('cargo-build-output', 'target', ['Cargo.toml']), ('opensip-custody-state', '.opensip', ['package.json'])]:
        fs = tree(dirs=[anchor + '/.git'], files=extra_files, vcs=[anchor])
        cur, pop = run(inp(fs, explicitProject='/h/w'))
        entry = pop['fs'].get('/h/w/' + anchor, {})
        control('B2B0REF-3 %s anchor with vcs: entry projected, not a repository' % label,
                ('vcs' in entry, entry.get('kind'), cur['provenance']['nestedRepositories'], ['/h/w/' + anchor] == [t['path'] for t in cur['provenance']['prunedTrees'] if t['path'] == '/h/w/' + anchor]),
                (False, 'dir', [], True))
    # 11. r3 (B2B0REF-4): the depth policy precedes boundary evidence, for config and VCS boundaries at 256/257/258.
    for n in (256, 257, 258):
        rel = '/'.join('d' for _ in range(n))
        deep = '/h/w/' + rel
        fs = tree(dirs=[rel], files=['package.json', rel + '/opensip.json'])
        cur, pop = run(inp(fs, explicitProject='/h/w'))
        want = ([deep], True) if n == 256 else ([], False)
        control('B2B0REF-4 config boundary at depth %d' % n, (cur['provenance']['nestedProjects'], deep + '/opensip.json' in pop['fs']), want)
        fs = tree(dirs=[rel], files=['package.json'], vcs=[rel])
        cur, pop = run(inp(fs, explicitProject='/h/w'))
        entry = pop['fs'].get(deep)
        want = ([deep], True) if n == 256 else (([], False) if n == 257 else ([], None))
        control('B2B0REF-4 vcs boundary at depth %d' % n, (cur['provenance']['nestedRepositories'], None if entry is None else 'vcs' in entry), want)
    # 7. Depth (Codex NBO-1 on plan r4): 256 is a unit, 257 is DEPTH, 258 is unseen.
    for n, expect in [(256, ('unit', None)), (257, ('excluded', 'DEPTH')), (258, ('unseen', None))]:
        rel = '/'.join('d' for _ in range(n))
        fs = tree(dirs=[rel], files=['package.json', rel + '/package.json'])
        cur, pop = run(inp(fs))
        unit_paths = [u['path'] for u in cur['provenance']['units']]
        ex = [r for r in cur['provenance']['excludedUnits'] if r['path'] == '/h/w/' + rel]
        got = ('unit', None) if '/h/w/' + rel in unit_paths else (('excluded', ex[0]['reason']) if ex else ('unseen', None))
        control('depth %d' % n, got, expect)
        if n == 258:
            control('depth 258 marker not observed', '/h/w/' + rel + '/package.json' in pop['fs'], False)
    # 9. r2 (B2B0REF-2): an injected current-replay consistency fault fails the checker (passed false, nonzero exit).
    if not a.inject_current_fault:
        with tempfile.TemporaryDirectory() as tmp:
            out = Path(tmp) / 'fault.json'
            r = subprocess.run([sys.executable, '-I', '-B', __file__, '--architecture', str(A), '--reference', str(a.reference), '--packages-root', str(a.packages_root),
                                '--out', str(out), '--inject-current-fault'], capture_output=True)
            fault = json.loads(out.read_text())
            control('negative: injected consistency fault fails the checker', (r.returncode != 0, fault['passed'], any('unexpected exception' in f[1] for f in fault['failures'])), (True, False, True))
    report = dict(passed=not failures, failures=[list(map(str, f)) for f in failures], pins=pins, summary=summary,
                  controls=controls, controlCount=len(controls), cases=rows, shapeFillLabel='SHAPE-ONLY workspaceDeclarations absent rows; never emitted',
                  filesystemRead=False, productEdited=False, qualification=False)
    a.out.write_text(json.dumps(report, indent=1) + '\n')
    print(json.dumps(dict(passed=report['passed'], failures=len(failures), summary=summary, controls=len(controls))))
    sys.exit(0 if report['passed'] else 1)


if __name__ == '__main__':
    main()
