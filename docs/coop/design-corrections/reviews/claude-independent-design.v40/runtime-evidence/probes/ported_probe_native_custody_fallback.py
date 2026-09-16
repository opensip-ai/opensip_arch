"""Independent helper-level probe of identity section 3 pruned-tree read custody and native U-9 fallback boundaries.

Calls the owner functions directly (identity-model.v3 snapshot_pruned_tree_faults; native discover_units,
default_capability_selection, unit_scope_descriptor). Rows marked `observation` characterise a stated TCB or grammar
limit rather than assert a contract outcome. Real complete Run controls for the same laws are the author's
check-native-consumer24-corrections (reference group evidence). Writes only receipts/probes/native-custody-fallback.json."""
import importlib.util, json, sys, traceback
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v40')
DC = RT / 'work/source40-pkg/docs/coop/design-corrections'
spec = importlib.util.spec_from_file_location('p40_identity_custody', DC / 'foundation/identity-model.v3.py')
M = importlib.util.module_from_spec(spec)
sys.modules['p40_identity_custody'] = M
spec.loader.exec_module(M)
N = M.native_admission()
FIX = json.loads((DC / 'native/native-cases.v2.json').read_text())['fixtures']
ROWS = []


def row(case, ok, observed=None, expected=None, observation=False):
    r = {'case': case, 'ok': bool(ok), 'observed': observed}
    if expected is not None:
        r['expected'] = expected
    if observation:
        r['kind'] = 'observation'
    ROWS.append(r)


def faults(paths, *layouts):
    return M.snapshot_pruned_tree_faults([{'path': p} for p in paths], list(layouts))


def layout(*rows):
    return {'schemaVersion': 1, 'entries': sorted(({'packageName': n, 'packageVersion': '1.0.0', 'installPath': i, 'realPath': r, 'contentSha256': '1' * 64}
                                                  for n, i, r in rows), key=lambda e: e['installPath'].encode())}


def custody():
    A = layout(('a', 'node_modules/a', 'node_modules/a'))
    row('control-listed-package-read-lawful', faults(['node_modules/a/index.js'], A) == [], faults(['node_modules/a/index.js'], A), [])
    broad = layout(('everything', 'node_modules', 'node_modules'))
    got = faults(['node_modules/a/index.js', 'node_modules/b/lib/x.js'], broad)
    row('observation-a-single-broad-installPath-row-authorizes-every-top-level-package', True, got,
        'identity section 3: listed directories are arbitrary admitted CanonicalPaths; which files a context read is a host TCB observation', True)
    got = faults(['node_modules/a/node_modules/b/x.js'], broad)
    row('broad-row-still-never-authorizes-a-nested-installed-package', got == ['node_modules/a/node_modules/b/x.js'], got)
    got = faults(['node_modules/a/index.js'], layout(('a', 'node_modules/a/', 'node_modules/a/')))
    row('trailing-slash-row-is-the-same-directory', got == [], got, [])
    got = faults(['node_modules/a'], A)
    row('observation-a-file-at-the-listed-directory-path-itself-is-not-authorized', True, got, None, True)
    got = faults(['.git/modules/a/index.js'], layout(('a', 'node_modules/a', '.git/modules/a')))
    row('a-realPath-inside-a-vcs-tree-never-authorizes-a-read', got == ['.git/modules/a/index.js'], got)
    got = faults(['node_modules/a/Cargo.toml', 'node_modules/a/target/debug/x.d'], A)
    row('cargo-marker-inside-a-pruned-tree-creates-no-cargo-root-so-its-target-is-a-package-read', got == [], got,
        'security S3: a Cargo.toml inside a pruned tree does not create a Cargo root')
    got = faults(['packages/lib/Cargo.toml', 'packages/lib/target/debug/x.d'], layout(('lib', 'node_modules/lib', 'packages/lib')))
    row('first-party-cargo-build-output-is-never-a-read-even-below-a-listed-realPath', got == ['packages/lib/target/debug/x.d'], got)
    got = faults(['Node_Modules/a/index.js'], A)
    row('observation-exact-case-segment-rule-leaves-a-case-variant-directory-in-first-party-custody', True, got, None, True)
    got = faults(['node_modules/a/.svn/entries', 'node_modules/a/sub/.jj/x'], A)
    row('vcs-at-any-depth-inside-a-listed-package-refuses', got == ['node_modules/a/.svn/entries', 'node_modules/a/sub/.jj/x'], got)
    store = 'node_modules/.pnpm/a@1.0.0/node_modules/a'
    got = faults([store + '/index.js'], layout(('a', 'node_modules/a', store)))
    row('store-layout-realPath-with-internal-node_modules-segments-authorizes-its-own-files', got == [], got, [])
    got = faults([store + '/index.js'], layout(('a', 'node_modules/a', 'node_modules/a')))
    row('store-layout-without-the-realPath-row-refuses-the-store-read', got == [store + '/index.js'], got)


def fallback():
    fb = dict(N.SYNTAX_ONLY_FALLBACK_UNIT, unitOrdinal=0)
    bare = N.discover_units({})
    row('control-marker-free-discovery-yields-the-fallback', bare['units'] == [fb], bare['units'])
    inv = {'schemaVersion': 2, 'source': 'security.discovery', 'selectedRoot': '/home/u/repo', 'nestedRepositories': [], 'nestedProjects': [],
           'custodyExcludedUnits': [{'path': 'pkg', 'reason': 'DIRECTORY_CUSTODY:WRITABLE_BY_OTHERS'}], 'prunedTrees': []}
    got = N.discover_units({'pkg/package.json': {'sha256': '1' * 64}}, None, inv)
    row('observation-only-marker-in-a-custody-excluded-directory-yields-the-fallback', True,
        {'refused': got.get('refused'), 'units': got.get('units'), 'excludedUnits': (got.get('boundaries') or {}).get('excludedUnits')}, None, True)
    if got.get('units') == [fb]:
        scope = N.unit_scope_descriptor([fb], [], None, got.get('prunedTrees', []), inv)['scopeDescriptor']
        row('fallback-scope-excludes-the-custody-excluded-directory', 'pkg' in scope['excludedPathPrefixes'], scope['excludedPathPrefixes'])
    for label, value in (('empty-explicit-root-list', []), ('explicit-dot-root', ['.'])):
        try:
            g = N.discover_units({}, value)
            row('observation-explicit-roots-' + label, True, {'refused': g.get('refused'), 'units': g.get('units')}, None, True)
        except Exception as exc:  # noqa: BLE001
            row('observation-explicit-roots-' + label, True, type(exc).__name__ + ':' + str(exc)[:200], None, True)
    rs = N.discover_units({'Cargo.toml': {'sha256': '1' * 64}})
    row('any-surviving-language-unit-suppresses-the-fallback', all(u['languageFamily'] != 'none' for u in rs['units']) and rs['units'], rs['units'])
    sel = N.default_capability_selection([fb], FIX['registry'])['analysisSpec']['requestedCapabilities']
    row('fallback-default-selection-is-the-complete-syntax-only-product-at-root',
        sorted(r['capabilityId'] for r in sel) == N.required_default_capabilities('syntax-only') and all(r['workspaceRoot'] == '.' for r in sel), len(sel))
    try:
        N.default_capability_selection([], FIX['registry'])
        row('zero-units-default-selection-refuses', False, 'admitted')
    except Exception as exc:  # noqa: BLE001
        row('zero-units-default-selection-refuses', 'NATIVE_DEFAULT_SELECTION_WITHOUT_UNIT' in str(exc), str(exc)[:200])


for fn in (custody, fallback):
    try:
        fn()
    except Exception:  # noqa: BLE001
        row(fn.__name__ + '-crashed', False, traceback.format_exc()[-1500:])
out = RT / 'receipts/probes/native-custody-fallback.json'
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps({'standing': 'independent reviewer helper-level probe; owner functions; not a full Run', 'rows': ROWS,
                           'failed': [r for r in ROWS if not r['ok']]}, indent=1, default=str))
print(json.dumps({'total': len(ROWS), 'failed': [(r['case'], r['observed']) for r in ROWS if not r['ok']],
                  'observations': [(r['case'], r['observed']) for r in ROWS if r.get('kind') == 'observation']}, indent=1, default=str)[:6000])
