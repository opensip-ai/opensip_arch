"""Independent native probe: U-4b.2 unitKind projection (full Run closure), U-1/section 1.2 effective allowJs and nested Cargo
workspace folding, on source39 bytes versus source40 bytes in separate processes.

Parent (no arguments) writes only receipts/probes/native-v40-on43.json. Child: --side ROOT -> JSON on stdout.
Full Runs are built by the maintained execution-inputs fixture (the same path check-native-consumer24-corrections uses):
the fixture's own native copy builds a membership from the reviewer's units, the reviewer mutates it BEFORE membershipDigest is
computed (so the whole Plan is digest-consistent), and identity-model.v3.close_run (complete semantic replay) decides.
Expected values are this reviewer's reading of native-evidence.md section 1.2, U-1, U-2 and U-4b (source40 text)."""
import contextlib, copy, hashlib, importlib.util, io, json, subprocess, sys, traceback
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v43')
NEW = RT / 'work/source43-pkg'
OLD = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v39/work/source39-pkg')
OUT = RT / 'receipts/probes/native-v40-on43.json'
SHA = 'd' * 64


def C(x):
    return json.dumps(x, sort_keys=True, separators=(',', ':'), ensure_ascii=False).encode('utf-8')


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def summary(units):
    return [(u['rootPath'], u['languageFamily'], u['languageMode'], u['unitKind'], u['markerPath'], u['memberPackageRoots']) for u in units]


def cargo(ws):
    return {'sha256': SHA, 'isCargoWorkspace': ws}


def child(root):
    DC = Path(root) / 'docs/coop/design-corrections'
    ENUM = load('nv40_enum', DC / 'foundation/enumeration_model.v1.py')
    NV = ENUM.NV
    out = {'root': root, 'discovery': {}, 'cargo': {}, 'mode': {}, 'fullRun': {}}

    def disc(markers, explicit=None, boundaries=None):
        try:
            d = NV.discover_units(markers, explicit, boundaries)
            return {'refused': (d.get('refused') or {}).get('detail') if d.get('refused') else None, 'units': summary(d.get('units', [])),
                    'excluded': [(x['path'], x['reason']) for x in (d.get('boundaries') or {}).get('excludedUnits', [])], 'raw': d.get('units', [])}
        except Exception as exc:  # noqa: BLE001
            return {'exception': type(exc).__name__ + ':' + str(exc)[:200]}

    # U-1 / section 1.2 marker observations
    for name, markers in {
            'jsconfig-omitted': {'jsconfig.json': {'sha256': SHA}},
            'jsconfig-false': {'jsconfig.json': {'sha256': SHA, 'allowJs': False}},
            'jsconfig-true': {'jsconfig.json': {'sha256': SHA, 'allowJs': True}},
            'tsconfig-omitted': {'tsconfig.json': {'sha256': SHA}},
            'tsconfig-true': {'tsconfig.json': {'sha256': SHA, 'allowJs': True}},
            'tsconfig-false-beside-jsconfig-true': {'tsconfig.json': {'sha256': SHA, 'allowJs': False}, 'jsconfig.json': {'sha256': SHA, 'allowJs': True}},
            'package-only': {'package.json': {'sha256': SHA}},
            'tsconfig-beside-package': {'tsconfig.json': {'sha256': SHA}, 'package.json': {'sha256': SHA}}}.items():
        r = disc(markers)
        r.pop('raw', None)
        out['discovery'][name] = r
    d = NV.discover_units({'jsconfig.json': {'sha256': SHA, 'allowJs': False}})
    m = NV.assign_membership(d['units'], ['index.ts', 'lib.js', 'README.md'])
    out['jsconfigFalseMembershipDigest'] = hashlib.sha256(C(m)).hexdigest()
    # typescript_mode over config dictionaries (the effective-option derivation the marker observation must carry)
    for name, (ts, js) in {'tsconfig-checkJs-true-no-allowJs': ({'compilerOptions': {'checkJs': True}}, None),
                           'tsconfig-allowJs-false-checkJs-true': ({'compilerOptions': {'allowJs': False, 'checkJs': True}}, None),
                           'jsconfig-no-options': (None, {'compilerOptions': {}}),
                           'jsconfig-allowJs-false': (None, {'compilerOptions': {'allowJs': False}})}.items():
        try:
            t = NV.typescript_mode(['index.ts', 'lib.js'], '', None, ts, js, [], False)
            out['mode'][name] = {'languageMode': t['languageMode'], 'allowJs': t['allowJs'], 'checkJs': t['checkJs'], 'configOrigin': t['configOrigin']}
        except Exception as exc:  # noqa: BLE001
            out['mode'][name] = {'exception': type(exc).__name__ + ':' + str(exc)[:200]}
    # nested Cargo
    inventory = lambda projects: {'schemaVersion': 2, 'source': 'security.discovery', 'selectedRoot': '/home/u/repo', 'nestedRepositories': [],  # noqa: E731
                                  'nestedProjects': projects, 'custodyExcludedUnits': [], 'prunedTrees': []}
    TRIPLE = {'Cargo.toml': cargo(True), 'a/Cargo.toml': cargo(True), 'a/b/Cargo.toml': cargo(True), 'a/b/c/Cargo.toml': cargo(False)}
    cases = {
        'C1-triple-nesting-auto': (TRIPLE, None, None),
        'C2-explicit-a': (TRIPLE, ['a'], None),
        'C3-explicit-root-and-a-b': (TRIPLE, ['.', 'a/b'], None),
        'C4-explicit-a-b': (TRIPLE, ['a/b'], None),
        'C5-nested-project-a': (TRIPLE, None, inventory(['a'])),
        'C6-root-package-over-nested-workspace': ({'Cargo.toml': cargo(False), 'a/Cargo.toml': cargo(True), 'a/b/Cargo.toml': cargo(False)}, None, None),
        'C7-package-between-workspaces': ({'Cargo.toml': cargo(True), 'a/Cargo.toml': cargo(False), 'a/b/Cargo.toml': cargo(True), 'a/b/c/Cargo.toml': cargo(False)}, None, None),
        'C8-explicit-a-and-its-member-a-b-c': (TRIPLE, ['a', 'a/b/c'], None),
        'C9-utf8-member-order': ({'Cargo.toml': cargo(True), 'x/Cargo.toml': cargo(True), 'x/p/Cargo.toml': cargo(False), 'x-y/Cargo.toml': cargo(False)}, None, None),
    }
    law_faults = {}
    for name, (markers, explicit, bounds) in cases.items():
        r = disc(markers, explicit, bounds)
        raw = r.pop('raw', None)
        out['cargo'][name] = r
        if raw and not r.get('refused') and name in ('C1-triple-nesting-auto', 'C9-utf8-member-order'):
            files = ['a/b/c/src/lib.rs', 'a/b/target/debug/x.rs', 'a/target/debug/y.rs', 'a/src/target/z.rs', 'target/w.rs', 'src/main.rs'] if name.startswith('C1') \
                else ['x/p/src/lib.rs', 'x-y/src/lib.rs', 'x/target/q.rs', 'x-y/target/q.rs']
            mem = NV.assign_membership(raw, files, bounds)
            out['cargo'][name]['rows'] = [(row['path'], row['membership'], row['reason'], row['unitOrdinal']) for row in mem['rows']]
            faults = []
            ENUM._membership_order_law(mem, faults)
            law_faults[name] = faults
            if name.startswith('C1') and raw[0]['memberPackageRoots']:
                dropped = copy.deepcopy(mem)
                dropped['units'][0]['memberPackageRoots'] = [x for x in dropped['units'][0]['memberPackageRoots'] if x != 'a/b']
                f2 = []
                ENUM._membership_order_law(dropped, f2)
                law_faults[name + '-folded-member-a-b-dropped'] = f2
    out['cargoLaw'] = law_faults
    # full Runs
    EI = load('nv40_execution_inputs_checker', DC / 'foundation/check-execution-inputs.v1.py')
    real = EI.F.fixture_helpers
    helpers = real()
    original = helpers.N.assign_membership

    def run_with(units, mutate):
        def patched(units_, files, boundaries=None):
            membership = original([dict(u) for u in units], files)
            mutate(membership)
            return membership
        helpers.N.assign_membership = patched
        EI.F.fixture_helpers = lambda: helpers
        try:
            graph = EI.F.build_file_inputs()
        finally:
            EI.F.fixture_helpers = real
            helpers.N.assign_membership = original
        try:
            result, _ = EI.full_run(graph)
            return {'closed': True, 'runId': result.get('runId'), 'units': summary(graph['membership']['units'])}
        except Exception as exc:  # noqa: BLE001
            return {'closed': False, 'refusal': type(exc).__name__ + ':' + str(exc)[:300], 'units': summary(graph['membership']['units'])}

    def setu(**kw):
        return lambda m: m['units'][0].update(**kw)
    js_false = NV.discover_units({'jsconfig.json': {'sha256': SHA, 'allowJs': False}})['units']
    ts_true = NV.discover_units({'tsconfig.json': {'sha256': SHA, 'allowJs': True}})['units']
    rust = NV.discover_units({'Cargo.toml': cargo(False)})['units']
    tsc = NV.discover_units({'tsconfig.json': {'sha256': SHA}})['units']
    out['fullRun'] = {
        'N1-jsconfig-false-published': run_with(js_false, lambda m: None),
        'N2-jsconfig-false-kind-reminted': run_with(js_false, setu(unitKind='js-program' if js_false[0]['unitKind'] == 'ts-program' else 'ts-program')),
        'N3-jsconfig-false-mode-and-kind-consistently-reminted': run_with(js_false, setu(languageMode='js-allowjs', unitKind='js-program')
                                                                          if js_false[0]['languageMode'] == 'ts-tsconfig' else setu(languageMode='ts-tsconfig', unitKind='ts-program')),
        'N4-rust-unit-carrying-js-program': run_with(rust, setu(unitKind='js-program')),
        'N5-tsjs-unit-carrying-cargo-package': run_with(tsc, setu(unitKind='cargo-package')),
        'N6-tsconfig-allowjs-true-published': run_with(ts_true, lambda m: None),
    }
    return out


def side(root):
    p = subprocess.run([sys.executable, '-I', '-B', str(Path(__file__).resolve()), '--side', str(root)], capture_output=True, text=True, timeout=5400)
    if p.returncode != 0:
        return {'error': p.stderr[-3000:]}
    return json.loads(p.stdout.strip().splitlines()[-1])


def parent():
    rows = []

    def row(case, ok, observed, expected=None, kind=None):
        r = {'case': case, 'ok': bool(ok), 'observed': observed}
        if expected is not None:
            r['expected'] = expected
        if kind:
            r['kind'] = kind
        rows.append(r)
    old, new = side(OLD), side(NEW)
    if 'error' in old or 'error' in new or 'crash' in old or 'crash' in new:
        row('sides-completed', False, {'old': old.get('error') or old.get('crash'), 'new': new.get('error') or new.get('crash')})
        return rows, old, new
    D, DO = new['discovery'], old['discovery']
    mk = lambda r: [(u[2], u[3], u[4]) for u in r.get('units', [])]  # noqa: E731
    expect_modes = {'jsconfig-omitted': [('js-allowjs', 'js-program', 'jsconfig.json')], 'jsconfig-false': [('ts-tsconfig', 'ts-program', 'jsconfig.json')],
                    'jsconfig-true': [('js-allowjs', 'js-program', 'jsconfig.json')], 'tsconfig-omitted': [('ts-tsconfig', 'ts-program', 'tsconfig.json')],
                    'tsconfig-true': [('js-allowjs', 'js-program', 'tsconfig.json')],
                    'tsconfig-false-beside-jsconfig-true': [('ts-tsconfig', 'ts-program', 'tsconfig.json')],
                    'package-only': [('js-synthesized', 'js-program', 'package.json')], 'tsconfig-beside-package': [('ts-tsconfig', 'ts-program', 'tsconfig.json')]}
    for name, want in expect_modes.items():
        row('U-1-source40-' + name, mk(D[name]) == want, mk(D[name]), want)
    row('U-1-source39-jsconfig-false-was-js-allowjs (discriminating baseline)', mk(DO['jsconfig-false']) == [('js-allowjs', 'js-program', 'jsconfig.json')], mk(DO['jsconfig-false']))
    row('identity-consequence-jsconfig-false-membershipDigest-differs-39-to-40', new['jsconfigFalseMembershipDigest'] != old['jsconfigFalseMembershipDigest'],
        {'source39': old['jsconfigFalseMembershipDigest'], 'source40': new['jsconfigFalseMembershipDigest']})
    M = new['mode']
    row('section-1.2-typescript_mode-tsconfig-without-allowJs-inherits-checkJs', M['tsconfig-checkJs-true-no-allowJs'].get('languageMode') == 'js-allowjs', M)
    row('section-1.2-typescript_mode-explicit-allowJs-false-wins-over-checkJs', M['tsconfig-allowJs-false-checkJs-true'].get('languageMode') == 'ts-tsconfig', M)
    row('section-1.2-typescript_mode-jsconfig-default-true-and-explicit-false', M['jsconfig-no-options'].get('languageMode') == 'js-allowjs'
        and M['jsconfig-allowJs-false'].get('languageMode') == 'ts-tsconfig', M)
    row('observation-marker-observation-must-carry-the-effective-value (omitted tsconfig allowJs reads false even where checkJs derives true)', True,
        {'discoverUnitsTsconfigOmitted': mk(D['tsconfig-omitted']), 'typescriptModeCheckJsDerived': M['tsconfig-checkJs-true-no-allowJs']},
        'section 1.2: the pre-Plan marker observation named allowJs means the effective value', 'observation')
    CG = new['cargo']
    exp = {
        'C1-triple-nesting-auto': [('', 'cargo-workspace', ['a', 'a/b', 'a/b/c'])],
        'C2-explicit-a': [('a', 'cargo-workspace', ['a/b', 'a/b/c'])],
        'C3-explicit-root-and-a-b': [('', 'cargo-workspace', ['a', 'a/b', 'a/b/c'])],
        'C4-explicit-a-b': [('a/b', 'cargo-workspace', ['a/b/c'])],
        'C5-nested-project-a': [('', 'cargo-workspace', [])],
        'C6-root-package-over-nested-workspace': [('', 'cargo-package', []), ('a', 'cargo-workspace', ['a/b'])],
        'C7-package-between-workspaces': [('', 'cargo-workspace', ['a', 'a/b', 'a/b/c'])],
        'C8-explicit-a-and-its-member-a-b-c': [('a', 'cargo-workspace', ['a/b', 'a/b/c'])],
        'C9-utf8-member-order': [('', 'cargo-workspace', ['x', 'x-y', 'x/p'])],
    }
    for name, want in exp.items():
        got = [(u[0], u[3], u[5]) for u in CG[name].get('units', [])]
        row('U-4b.2-source40-' + name, got == want and not CG[name].get('refused'), {'units': got, 'excluded': CG[name].get('excluded'), 'refused': CG[name].get('refused'),
                                                                                  'exception': CG[name].get('exception')}, want)
        if name in ('C1-triple-nesting-auto', 'C4-explicit-a-b', 'C7-package-between-workspaces'):
            row('source39-baseline-' + name, True, {k: old['cargo'][name].get(k) for k in ('units', 'refused', 'exception')}, None, 'observation')
    row('U-4b.2-C5-nested-project-excludes-all-three-marker-directories', sorted(p for p, _ in CG['C5-nested-project-a'].get('excluded', []))
        == ['a', 'a/b', 'a/b/c'], CG['C5-nested-project-a'].get('excluded'))
    rows1 = {r[0]: r for r in CG['C1-triple-nesting-auto'].get('rows', [])}
    row('U-4a-target-pruned-under-every-folded-member-root-and-src-target-stays-source',
        rows1.get('a/b/target/debug/x.rs', [None, None])[2] == 'host-ignore-convention' and rows1.get('a/target/debug/y.rs', [None, None])[2] == 'host-ignore-convention'
        and rows1.get('target/w.rs', [None, None])[2] == 'host-ignore-convention' and rows1.get('a/src/target/z.rs', [None, None])[1] == 'program-member', rows1)
    law = new['cargoLaw']
    row('U-4b.5-law-admits-the-derived-nested-memberships', law.get('C1-triple-nesting-auto') == [] and law.get('C9-utf8-member-order') == [], law)
    row('U-4b.5-dropping-a-folded-member-root-refuses-row-derivation', law.get('C1-triple-nesting-auto-folded-member-a-b-dropped') == ['ENUMERATION_MEMBERSHIP_ROW_DERIVATION'], law)
    F, FO = new['fullRun'], old['fullRun']
    row('full-run-source40-N1-jsconfig-false-published-closes', F['N1-jsconfig-false-published'].get('closed') is True, F['N1-jsconfig-false-published'])
    row('full-run-source40-N6-tsconfig-allowjs-true-published-closes', F['N6-tsconfig-allowjs-true-published'].get('closed') is True, F['N6-tsconfig-allowjs-true-published'])
    for name in ('N2-jsconfig-false-kind-reminted', 'N4-rust-unit-carrying-js-program', 'N5-tsjs-unit-carrying-cargo-package'):
        row('full-run-source40-' + name + '-refuses-ENUMERATION_MEMBERSHIP_ORDER', F[name].get('closed') is False and 'ENUMERATION_MEMBERSHIP_ORDER' in str(F[name].get('refusal')), F[name])
        row('full-run-source39-baseline-' + name, True, FO[name], None, 'observation')
    row('observation-full-run-N3-consistent-mode-and-kind-remint-over-a-jsconfig-false-marker', True, {'source40': F['N3-jsconfig-false-mode-and-kind-consistently-reminted'],
        'source39': FO['N3-jsconfig-false-mode-and-kind-consistently-reminted']},
        'closure can check kind against mode; whether the mode matches the marker bytes is the trusted pre-Plan marker observation', 'observation')
    return rows, old, new


if __name__ == '__main__':
    if '--side' in sys.argv:
        try:
            result = child(sys.argv[sys.argv.index('--side') + 1])
        except Exception:  # noqa: BLE001
            result = {'crash': traceback.format_exc()[-3000:]}
        print(json.dumps(result, default=str))
    else:
        try:
            rows, old, new = parent()
        except Exception:  # noqa: BLE001
            rows, old, new = [{'case': 'probe-crashed', 'ok': False, 'observed': traceback.format_exc()[-3000:]}], None, None
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps({'standing': 'independent reviewer probe; owner functions and full Run closure over the maintained fixture on source39 and source40 bytes in separate processes',
                                   'rows': rows, 'failed': [r for r in rows if not r['ok']], 'sides': {'source39': old, 'source40': new}}, indent=1, default=str))
        print(json.dumps({'total': len(rows), 'failed': [(r['case'], r['observed']) for r in rows if not r['ok']],
                          'observations': [r['case'] for r in rows if r.get('kind') == 'observation']}, indent=1, default=str)[:9000])
