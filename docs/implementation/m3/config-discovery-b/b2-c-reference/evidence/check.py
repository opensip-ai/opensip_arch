"""Check B2-c0, the current native unit reference (B2-c plan r2 section 1).

Stages:
  historical - the selected model as loaded (its own shared rule, version-2 inventories): every `units-*` case of
               native-cases.v2.json, recorded;
  current    - the same cases through `native_unit_reference.Current`, each case's version-2 inventory argument
               projected to version 3 with no member (the checker's projection of the case input, not part of the
               reference). Every expectation must hold, or differ only by the one explained difference: SX-1's
               `.opensip` anchor at the root, which the B2-a rule adds to `excludedPathPrefixes`. Any other
               difference fails.
Then the current-only controls: a version-2 inventory refuses on the current lane; the three B-S1 member cases of plan
r2 (RF-2); and the security/native join sweep, run with the current instruments on both sides (B2-b0's `current` and
this reference). Design evidence: supplied synthetic maps only; no filesystem tree, product code or qualification."""
from pathlib import Path
import argparse, copy, hashlib, importlib.util, json, subprocess, sys, tempfile

NATIVE = 'docs/coop/design-corrections/native/'
SECURITY = 'docs/coop/design-corrections/security/'
CASES = NATIVE + 'native-cases.v2.json'
RUNNER = NATIVE + 'check_native_evidence.v2.py'
SEC_CHECK = SECURITY + 'check-security-lifecycle.v1.py'
B2B0 = 'docs/implementation/m3/config-discovery-b/b2-b-reference/reference/discovery_scan_reference.py'
HERE = Path(__file__).resolve().parent
# Each mutation patches a copy of the reference; the checker must then fail.
MUTATIONS = [
    ('member-consistency-dropped', "            if parent not in members:", "            if False:"),
    ('ld1-filter-dropped', "        withheld = set(self._outside_markers(markers, boundaries))", "        withheld = set()"),
    ('members-unbound', "        self.model.DD = _BoundRule(self.rule, members)", "        self.model.DD = _BoundRule(self.rule, ())"),
    ('version-2-admitted', "boundaries.get('schemaVersion') != 3:", "boundaries.get('schemaVersion') not in (2, 3):"),
    ('boundary-predicate-narrowed', "        return hit if hit is not None else self.rule.classify_custody_exclusion(path, None, boundaries['custodyExcludedUnits'])", "        return hit"),
    ('historical-rule-kept', "    rule = _module('native_unit_rule_sx1', pinned(arch, RULE))", "    rule = _module('native_unit_rule_sx1', pinned(arch, CLOSURE[2]))"),
]


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


def pin(arch, path):
    raw = (arch / path).read_bytes(); return dict(path=path, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())


class Replay:
    """The current instrument with each case's version-2 inventory argument projected to version 3."""

    def __init__(self, current, v3_of):
        self.current, self.v3_of = current, v3_of

    def __getattr__(self, name):
        target = getattr(self.current, name)
        if name not in ('discover_units', 'assign_membership', 'unit_scope_descriptor'):
            return target

        def call(*args, **kwargs):
            if 'boundaries' in kwargs:
                kwargs['boundaries'] = self.v3_of(kwargs['boundaries'])
            return target(*args, **kwargs)
        return call


def with_sx1(case):
    """The case with SX-1's explained difference applied to its expectations: `.opensip` in every expected
    `excludedPathPrefixes`, in UTF-8 order (the root anchor; these cases admit no member)."""
    out = copy.deepcopy(case); changed = []
    for key, value in list(out.get('expect', {}).items()):
        if key.endswith('excludedPathPrefixes') and isinstance(value, list) and '.opensip' not in value:
            out['expect'][key] = sorted(value + ['.opensip'], key=lambda p: p.encode()); changed.append(key)
    return out, changed


LD1_CASE = 'units-boundary-inventory-whose-pruned-trees-disagree-with-the-marker-inventory-refuses'


def ld1_case(case, replay, runner, fixtures):
    """LD-B2C0-1's explained difference for the one case whose disagreeing anchor lies inside a nested repository
    (`vendor/lib/node_modules`): on the current lane that anchor is not compared (S3 never enters the repository), so the
    first step admits the root unit; the case's purpose, refusing an inventory not taken over this marker inventory, is
    kept by a current variant whose disagreeing anchor is outside every boundary, and its schema-invalid step is unchanged."""
    adjusted = copy.deepcopy(case)
    adjusted['expect'] = {'$u.refused': None, '$u.units.0.rootPath': '', '$u.boundaries.memberRepositories': []}
    first = runner.run_case(adjusted, replay, fixtures)
    variant = copy.deepcopy(case)
    variant['id'] = case['id'] + ' (current variant: disagreeing anchor outside every boundary)'
    for step in variant['steps']:
        step['args']['markers'] = {'$merge': '$fixtures.markersBoundaryRepo', '$with': {'["node_modules/y/package.json"]': {'sha256': '5' * 64}}}
    variant['expect'] = {'$u.units': [], '$u.refused.detail': 'native.boundary-inventory-mismatch', '$u.refused.d9.code': 'REQUEST.PRECONDITION_FAILED',
                         '$u.refused.missingAnchors': [{'path': 'node_modules', 'reason': 'dependency-tree'}]}
    second = runner.run_case(variant, replay, fixtures)
    return first['passed'] and second['passed'], first['faults'] + second['faults']


def member_cases(cur, nur):
    """B-S1's member rules (plan r2 RF-2), on the current lane only."""
    rows = []

    def inv(pruned=(), members=(), repos=(), projects=()):
        return {'schemaVersion': 3, 'source': 'security.discovery', 'selectedRoot': '/h/w', 'nestedRepositories': list(repos),
                'nestedProjects': list(projects), 'custodyExcludedUnits': [], 'prunedTrees': list(pruned), 'memberRepositories': list(members)}

    def tree(path, reason):
        return {'path': path, 'reason': reason, 'markerCount': None, 'markerCountBasis': 'not-enumerated'}
    sha = '1' * 64
    # (a) No member, a root .opensip anchor carried from security: admitted, V3-valid, `.opensip` excluded in scope.
    a_inv = inv([tree('.git', 'vcs-tree'), tree('.opensip', 'opensip-custody-state')])
    a = cur.discover_units({'package.json': {'sha256': sha}}, None, a_inv)
    s = cur.unit_scope_descriptor(a['units'], [], None, a['prunedTrees'], a_inv)
    ok = a['refused'] is None and a['boundaries']['memberRepositories'] == [] and '.opensip' in s['scopeDescriptor']['excludedPathPrefixes']
    rows.append(dict(name='empty-member-v3-with-root-opensip-anchor', holds=ok, units=[u['rootPath'] for u in a['units']], prunedTrees=a['prunedTrees']))
    # (b) Two admitted members: their .git anchors are accepted; their manifests are units; a member's own .opensip is pruned.
    b_inv = inv([tree('.opensip', 'opensip-custody-state'), tree('repo-a/.git', 'vcs-tree'), tree('repo-a/.opensip', 'opensip-custody-state'), tree('repo-b/.git', 'vcs-tree')], members=['repo-a', 'repo-b'])
    markers = {'repo-a/Cargo.toml': {'sha256': sha, 'isCargoWorkspace': False}, 'repo-b/package.json': {'sha256': sha},
               'repo-a/.opensip/package.json': {'sha256': sha}}
    b = cur.discover_units(markers, None, b_inv)
    bs = cur.unit_scope_descriptor(b['units'], [], None, b['prunedTrees'], b_inv)
    pruned = {(r['path'], r['reason']) for r in b['prunedTrees']}
    ok = (b['refused'] is None and sorted(u['rootPath'] for u in b['units']) == ['repo-a', 'repo-b'] and b['boundaries']['memberRepositories'] == ['repo-a', 'repo-b']
          and ('repo-a/.opensip', 'opensip-custody-state') in pruned and 'repo-a' not in bs['scopeDescriptor']['excludedPathPrefixes']
          and 'repo-a/.opensip' in bs['scopeDescriptor']['excludedPathPrefixes'])
    # ... and the member's .opensip anchor is required of the inventory, like any derived anchor.
    b2 = cur.discover_units(markers, None, inv([tree('.opensip', 'opensip-custody-state'), tree('repo-a/.git', 'vcs-tree'), tree('repo-b/.git', 'vcs-tree')], members=['repo-a', 'repo-b']))
    ok = ok and b2['refused'] is not None and b2['refused']['detail'] == 'native.boundary-inventory-mismatch'
    rows.append(dict(name='admitted-members-are-ordinary-directories', holds=ok, units=[u['rootPath'] for u in b['units']], prunedTrees=b['prunedTrees'],
                     excluded=bs['scopeDescriptor']['excludedPathPrefixes']))
    # (c) A nested vcs-tree anchor whose parent is no admitted member and no boundary refuses, carried or derived.
    c1 = cur.discover_units({'package.json': {'sha256': sha}}, None, inv([tree('lib/x/.git', 'vcs-tree')]))
    c2 = cur.discover_units({'package.json': {'sha256': sha}, 'lib/x/.git/package.json': {'sha256': sha}}, None, inv([tree('lib/x/.git', 'vcs-tree')]))
    c3 = cur.discover_units({'package.json': {'sha256': sha}}, None, inv([tree('lib/x/.git', 'vcs-tree')], members=['lib/x']))
    ok = (c1['refused'] is not None and c1['refused']['detail'] == 'native.boundary-inventory-mismatch'
          and c2['refused'] is not None and c2['refused']['detail'] == 'native.boundary-inventory-mismatch' and c3['refused'] is None)
    rows.append(dict(name='nested-vcs-anchor-outside-members-refuses', holds=ok, carried=c1['refused'], derived=c2['refused'], admitted=c3['refused']))
    # r1 (Codex B2C0REF-R1-RF-1): the full boundary predicate. A directory-custody or DEPTH exclusion is a boundary for
    # both LD-B2C0-1 and member consistency; a marker-custody row excludes only its marker file.
    for reason in ('DIRECTORY_CUSTODY:ACL_UNREADABLE', 'DEPTH'):
        cust = {'schemaVersion': 3, 'source': 'security.discovery', 'selectedRoot': '/h/w', 'nestedRepositories': [], 'nestedProjects': [],
                'custodyExcludedUnits': [{'path': 'blocked', 'reason': reason}], 'prunedTrees': [], 'memberRepositories': []}
        derived = cur.discover_units({'package.json': {'sha256': sha}, 'blocked/node_modules/x/package.json': {'sha256': sha}}, None, cust)
        carried = cur.discover_units({'package.json': {'sha256': sha}}, None, dict(cust, prunedTrees=[tree('blocked/.git', 'vcs-tree')]))
        outside = cur.discover_units({'package.json': {'sha256': sha}, 'node_modules/x/package.json': {'sha256': sha}}, None, cust)
        ok = (derived['refused'] is None and carried['refused'] is None
              and outside['refused'] is not None and outside['refused']['detail'] == 'native.boundary-inventory-mismatch')
        rows.append(dict(name='directory-exclusion-is-a-boundary:' + reason, holds=ok, derived=derived['refused'], carried=carried['refused'], outside=outside['refused']))
    mark = {'schemaVersion': 3, 'source': 'security.discovery', 'selectedRoot': '/h/w', 'nestedRepositories': [], 'nestedProjects': [],
            'custodyExcludedUnits': [{'path': 'pkg', 'reason': 'MARKER_CUSTODY:package.json:ACL_UNREADABLE'}], 'prunedTrees': [], 'memberRepositories': []}
    derived = cur.discover_units({'package.json': {'sha256': sha}, 'pkg/package.json': {'sha256': sha}, 'pkg/node_modules/y/package.json': {'sha256': sha}}, None, mark)
    carried = cur.discover_units({'package.json': {'sha256': sha}}, None, dict(mark, prunedTrees=[tree('pkg/.git', 'vcs-tree')]))
    ok = (derived['refused'] is not None and derived['refused']['detail'] == 'native.boundary-inventory-mismatch'
          and carried['refused'] is not None and carried['refused']['detail'] == 'native.boundary-inventory-mismatch')
    rows.append(dict(name='marker-custody-excludes-only-its-marker', holds=ok, derived=derived['refused'], carried=carried['refused']))
    # The current lane refuses a version-2 inventory.
    try:
        cur.discover_units({'package.json': {'sha256': sha}}, None, dict(a_inv, schemaVersion=2))
        ok = False
    except Exception as exc:  # noqa: BLE001
        ok = 'version-unsupported' in str(exc)
    rows.append(dict(name='current-lane-refuses-version-2', holds=ok))
    return rows


def join_sweep(arch, cur, packages):
    """The P3 sweep with current instruments: B2-b0 gives the V3 inventory, this reference consumes it."""
    sec = module('sec_check', arch / SEC_CHECK)
    ref = module('b2b0', arch / B2B0)
    slm, rule = ref.load(arch)
    R, fs = sec._p3_repo()
    inp = {'invokingUid': 1000, 'accountHome': '/home/alice', 'cwd': R, 'fs': fs}
    res, _, _ = ref.current(slm, rule, inp)
    inv = ref.boundary_inventory_v3(rule, ref.project_v3(res))
    markers = {p[len(R) + 1:]: {'sha256': '1' * 64} for p, e in fs.items() if p.startswith(R + '/') and e['kind'] == 'file' and p.rpartition('/')[2] in slm.WORKSPACE_MARKERS}
    nd = cur.discover_units(markers, None, inv)
    mem = cur.assign_membership(nd['units'], ['index.js', 'vendor/lib/src/x.js', 'apps/site/sub/src/lib.rs'], inv)
    scope = cur.unit_scope_descriptor(nd['units'], [], None, nd['prunedTrees'], inv)
    crosses = [cur.discover_units(markers, [j], inv)['refused'] for j in ('apps/site/sub', 'vendor/lib')]
    # The subset test still bites outside the boundaries: a derived root anchor the inventory lacks refuses, and carried, admits.
    extra = dict(markers, **{'node_modules/x/package.json': {'sha256': '1' * 64}})
    bad = cur.discover_units(extra, None, inv)
    good = cur.discover_units(extra, None, dict(inv, prunedTrees=sorted(inv['prunedTrees'] + [{'path': 'node_modules', 'reason': 'dependency-tree', 'markerCount': None, 'markerCountBasis': 'not-enumerated'}], key=lambda r: r['path'].encode())))
    holds = (nd['refused'] is None and sorted({u['rootPath'] for u in nd['units']}) == [''] and mem['outsideBoundaryFiles'] == ['apps/site/sub/src/lib.rs', 'vendor/lib/src/x.js']
             and {'apps/site', 'vendor/lib'} <= set(scope['scopeDescriptor']['excludedPathPrefixes'])
             and all(c is not None and c['detail'] == 'native.explicit-root-crosses-boundary' for c in crosses) and bad['refused'] is not None and bad['refused']['detail'] == 'native.boundary-inventory-mismatch' and good['refused'] is None)
    return dict(name='admitted-boundary-inventory-joins-security-discovery-and-native-unit-discovery (current)', holds=holds, inventory=inv,
                units=[u['rootPath'] for u in nd['units']], excludedUnits=nd['boundaries']['excludedUnits'], prunedTrees=nd['prunedTrees'])


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--architecture', type=Path, required=True); ap.add_argument('--packages', type=Path, required=True)
    ap.add_argument('--reference', type=Path, default=HERE.parent / 'reference' / 'native_unit_reference.py'); ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--no-mutations', action='store_true')
    a = ap.parse_args(); arch = a.architecture.resolve()
    nur = module('native_unit_reference', a.reference)
    hist, cur = nur.load(arch, a.packages)
    runner = module('native_runner', arch / RUNNER)
    doc = json.loads((arch / CASES).read_bytes()); fixtures = doc.get('fixtures', {})
    units = [c for c in doc['cases'] if c['id'].startswith('units-')]
    rows, explained = [], []
    replay = Replay(cur, nur.v3_of)
    for case in units:
        h = runner.run_case(case, hist, fixtures)
        c = runner.run_case(case, replay, fixtures)
        diff = []
        if not c['passed'] and case['id'] == LD1_CASE:
            passed, faults = ld1_case(case, replay, runner, fixtures)
            c = dict(passed=passed, faults=faults); diff = ['ld-b2c0-1-anchor-inside-boundary-not-compared']
        elif not c['passed']:
            adjusted, diff = with_sx1(case)
            c = runner.run_case(adjusted, replay, fixtures)
        rows.append(dict(id=case['id'], historical=h['passed'], current=c['passed'], explainedDifferences=[k if k.startswith('ld-') else 'sx1-root-opensip-anchor:' + k for k in diff], faults=h['faults'] + c['faults']))
        if diff:
            explained.append(case['id'])
    members = member_cases(cur, nur)
    sweep = join_sweep(arch, cur, a.packages)
    inputs = [pin(arch, p) for p, _, _ in (nur.MODEL, *nur.CLOSURE, nur.RULE, nur.B_S1)] + [pin(arch, p) for p in (CASES, RUNNER, SEC_CHECK, B2B0)]
    out = dict(standing='B2-c0 CHECK: design evidence only', inputs=inputs, reference=dict(name=a.reference.name, bytes=len(a.reference.read_bytes()), sha256=hashlib.sha256(a.reference.read_bytes()).hexdigest()),
               cases=rows, unitCases=len(units), historicalPassed=sum(r['historical'] for r in rows), currentPassed=sum(r['current'] for r in rows),
               casesWithExplainedDifference=explained, memberCases=members, joinSweep=sweep,
               passed=all(r['historical'] and r['current'] for r in rows) and len(units) == 26 and all(m['holds'] for m in members) and sweep['holds'])
    if not a.no_mutations:
        controls = []
        src = a.reference.read_text()
        with tempfile.TemporaryDirectory() as tmp:
            for name, before, after in MUTATIONS:
                assert src.count(before) == 1, name
                ref = Path(tmp) / (name + '.py'); ref.write_text(src.replace(before, after))
                r = subprocess.run([sys.executable, '-I', '-B', __file__, '--architecture', str(arch), '--packages', str(a.packages), '--reference', str(ref),
                                    '--out', str(Path(tmp) / (name + '.json')), '--no-mutations'], capture_output=True, text=True)
                controls.append(dict(name=name, exitCode=r.returncode, caught=r.returncode != 0))
        out['mutations'] = controls
        out['passed'] = out['passed'] and all(c['caught'] for c in controls)
    a.out.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps(dict(passed=out['passed'], historical=out['historicalPassed'], current=out['currentPassed'], explained=len(explained),
                          members=[(m['name'], m['holds']) for m in members], sweep=sweep['holds'], mutations=[(c['name'], c['caught']) for c in out.get('mutations', [])])))
    return 0 if out['passed'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
