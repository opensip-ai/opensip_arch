"""Cross-implementation vectors for the native unit instrument (M3-B r7 item 14; unit B2-c1, B2-c plan r2 section 2.1).

Developer tool only. It runs B2-c0, the current native unit reference (contract successor 166), at its accepted
architecture bytes, and writes or checks crates/host/src/discovery_vectors.json: every reference call the host's
`discovery.rs` must reproduce, with its exact JSON inputs and its exact JSON result or refusal.

  * Every step of the 26 `units-*` cases of native-cases.v2.json that calls an instrument function (`discover_units`,
    `assign_membership`, `unit_scope_descriptor`, `default_capability_selection`), its arguments resolved as the
    case runner resolves them and each version-2 boundary inventory projected to version 3 with no member (B2-c0's
    checker projection). `typescript_mode` is C2's and is recorded as skipped.
  * The B2-c0 member, custody and depth controls, the cap sweeps (4096 and 4097 first-party directories, 4200
    installed manifests), the scope sweep (1024 and 1025 unit roots), the explicit-root grammar sweep and the internal
    detail keys of the public alias map.

Large marker maps are written in their generator form (`$synthetic`: first-party count, installed count, root marker),
which the host test expands exactly as the reference's `synthetic_marker_set` does. A refusal is recorded by its
internal key: the exception text when it is an internal key (`native.`, `PROJECT.`, `NATIVE_`), otherwise
`schema-invalid`. No filesystem tree, network or environment input.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import importlib.util
import json
import sys

OUTPUT = 'crates/host/src/discovery_vectors.json'
REF = 'docs/implementation/m3/config-discovery-b/b2-c-reference/'
NATIVE = 'docs/coop/design-corrections/native/'
# Architecture inputs (contract successor 166 and the cases it replays): path, bytes, SHA-256.
ARCH = (
    (REF + 'reference/native_unit_reference.py', None, None),
    (NATIVE + 'native-cases.v2.json', None, None),
    (NATIVE + 'check_native_evidence.v2.py', None, None),
    (NATIVE + 'native-capability-matrix.v2.json', None, None),
    ('docs/coop/design-corrections/public-detail-registry.v1.json', None, None),
)
# The instrument's internal decision keys and the public records it passes unchanged (plan r2 section 2.3).
ALIASED = ('native.boundary-inventory-mismatch', 'native.explicit-root-crosses-boundary', 'native.explicit-root-grammar', 'native.too-many-units')
PUBLIC = ('native.explicit-root-without-marker', 'PROJECT.SCOPE_LIMIT')
INSTRUMENT = ('discover_units', 'assign_membership', 'unit_scope_descriptor', 'default_capability_selection')
SHA = '1' * 64


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pinned(root, path, size, digest):
    raw = (root / path).read_bytes()
    require((size is None or len(raw) == size) and (digest is None or hashlib.sha256(raw).hexdigest() == digest), 'input pin mismatch: ' + path)
    return raw


def packages(product, packages_root):
    closure = json.loads((product / 'tools/contracts/generator-closure.json').read_bytes())
    rows = [r for r in closure['files'] if r['path'].startswith('tools/contracts/python-packages/')]
    require(rows, 'no pinned python packages')
    for row in rows:
        pinned(packages_root, row['path'], row['bytes'], row['sha256'])
    return packages_root / 'tools/contracts/python-packages'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def marker_digest(markers):
    return hashlib.sha256(json.dumps(markers, sort_keys=True).encode()).hexdigest()


def error_key(exc):
    text = getattr(exc, 'message', None) or str(exc)
    if text.startswith('NATIVE_UNIT_ROOT_REPRESENTATION:'):
        # B2-c1 r3 (a lead decision): a grammar refusal's key names the field, the selector and the class; the value's
        # Python `repr` spelling is not reproduced (its printability follows Python's Unicode database).
        fault, at, selector, rest = text.split(':', 3)
        if not rest.startswith('length='):
            return ':'.join((fault, at, selector, 'grammar'))
    return text if text.startswith(('native.', 'PROJECT.', 'NATIVE_')) else 'schema-invalid'


class Recorder:
    """Calls the current instrument and records each call; the B2-c0 checker's projection of version-2 inventories."""

    def __init__(self, current, v3_of):
        self.current, self.v3_of, self.steps, self.case = current, v3_of, [], None
        self.markers_form = {}

    def __getattr__(self, name):
        target = getattr(self.current, name)
        if name not in INSTRUMENT:
            return target

        def call(**kwargs):
            if 'boundaries' in kwargs:
                kwargs['boundaries'] = self.v3_of(kwargs['boundaries'])
            args = copy.deepcopy(kwargs)
            if name == 'discover_units' and len(kwargs['markers']) > 64 and marker_digest(kwargs['markers']) in self.markers_form:
                args['markers'] = self.markers_form[marker_digest(kwargs['markers'])]
            row = dict(case=self.case, fn=name, args=args)
            try:
                result = target(**kwargs)
            except Exception as exc:  # noqa: BLE001 (recorded by its internal key)
                row.update(outcome='refused', key=error_key(exc))
                self.steps.append(row)
                raise
            row.update(outcome='result', result=copy.deepcopy(result))
            self.steps.append(row)
            return result
        return call


def synthetic(cur, first_party, installed, root_marker=True):
    return cur.synthetic_marker_set(first_party, installed, root_marker), {'$synthetic': dict(firstParty=first_party, installed=installed, rootMarker=root_marker)}


def extra(rec, cur):
    """The vectors beyond the cases."""
    def tree(path, reason):
        return {'path': path, 'reason': reason, 'markerCount': None, 'markerCountBasis': 'not-enumerated'}

    def inv(pruned=(), members=(), repos=(), projects=(), custody=()):
        return {'schemaVersion': 3, 'source': 'security.discovery', 'selectedRoot': '/h/w', 'nestedRepositories': list(repos), 'nestedProjects': list(projects),
                'custodyExcludedUnits': list(custody), 'prunedTrees': list(pruned), 'memberRepositories': list(members)}

    def run(case, fn, **kwargs):
        rec.case = case
        try:
            return getattr(rec, fn)(**kwargs)
        except Exception:  # noqa: BLE001 (recorded)
            return None
    pkg = {'package.json': {'sha256': SHA}}
    # The B2-c0 member, custody and depth controls.
    a = run('b2c0-empty-member-root-opensip', 'discover_units', markers=pkg, explicit_workspace_roots=None, boundaries=inv([tree('.git', 'vcs-tree'), tree('.opensip', 'opensip-custody-state')]))
    run('b2c0-empty-member-root-opensip', 'unit_scope_descriptor', units=a['units'], ignore_paths=[], explicit_path_prefixes=None, pruned_trees=a['prunedTrees'],
        boundaries=inv([tree('.git', 'vcs-tree'), tree('.opensip', 'opensip-custody-state')]))
    members = inv([tree('.opensip', 'opensip-custody-state'), tree('repo-a/.git', 'vcs-tree'), tree('repo-a/.opensip', 'opensip-custody-state'), tree('repo-b/.git', 'vcs-tree')], members=['repo-a', 'repo-b'])
    mk = {'repo-a/Cargo.toml': {'sha256': SHA, 'isCargoWorkspace': False}, 'repo-b/package.json': {'sha256': SHA}, 'repo-a/.opensip/package.json': {'sha256': SHA}}
    b = run('b2c0-admitted-members', 'discover_units', markers=mk, explicit_workspace_roots=None, boundaries=members)
    run('b2c0-admitted-members', 'assign_membership', units=b['units'], files=['repo-a/src/lib.rs', 'repo-b/index.ts', 'repo-a/.opensip/x.json', 'repo-b/.git/HEAD', 'README.md'], boundaries=members)
    run('b2c0-admitted-members', 'unit_scope_descriptor', units=b['units'], ignore_paths=['vendor/'], explicit_path_prefixes=None, pruned_trees=b['prunedTrees'], boundaries=members)
    run('b2c0-member-opensip-required', 'discover_units', markers=mk, explicit_workspace_roots=None, boundaries=inv([tree('.opensip', 'opensip-custody-state'), tree('repo-a/.git', 'vcs-tree'), tree('repo-b/.git', 'vcs-tree')], members=['repo-a', 'repo-b']))
    for name, markers, boundaries in (('carried', pkg, inv([tree('lib/x/.git', 'vcs-tree')])),
                                      ('derived', dict(pkg, **{'lib/x/.git/package.json': {'sha256': SHA}}), inv([tree('lib/x/.git', 'vcs-tree')])),
                                      ('admitted', pkg, inv([tree('lib/x/.git', 'vcs-tree')], members=['lib/x']))):
        run('b2c0-nested-vcs-' + name, 'discover_units', markers=markers, explicit_workspace_roots=None, boundaries=boundaries)
    for reason in ('DIRECTORY_CUSTODY:ACL_UNREADABLE', 'DEPTH'):
        cust = inv(custody=[{'path': 'blocked', 'reason': reason}])
        run('b2c0-custody-derived:' + reason, 'discover_units', markers=dict(pkg, **{'blocked/node_modules/x/package.json': {'sha256': SHA}}), explicit_workspace_roots=None, boundaries=cust)
        run('b2c0-custody-carried:' + reason, 'discover_units', markers=pkg, explicit_workspace_roots=None, boundaries=dict(cust, prunedTrees=[tree('blocked/.git', 'vcs-tree')]))
        u = run('b2c0-custody-outside:' + reason, 'discover_units', markers=dict(pkg, **{'blocked/package.json': {'sha256': SHA}}), explicit_workspace_roots=None, boundaries=cust)
        run('b2c0-custody-outside:' + reason, 'assign_membership', units=u['units'], files=['index.js', 'blocked/x.js', 'blocked/deep/y.rs'], boundaries=cust)
    mark = inv(custody=[{'path': 'pkg', 'reason': 'MARKER_CUSTODY:package.json:ACL_UNREADABLE'}])
    run('b2c0-marker-custody-derived', 'discover_units', markers=dict(pkg, **{'pkg/package.json': {'sha256': SHA}, 'pkg/node_modules/y/package.json': {'sha256': SHA}}), explicit_workspace_roots=None, boundaries=mark)
    u = run('b2c0-marker-custody', 'discover_units', markers=dict(pkg, **{'pkg/package.json': {'sha256': SHA}, 'pkg/tsconfig.json': {'sha256': SHA, 'allowJs': True}}), explicit_workspace_roots=None, boundaries=mark)
    run('b2c0-marker-custody', 'assign_membership', units=u['units'], files=['pkg/a.js', 'index.ts'], boundaries=mark)
    run('b2c0-version-2-refused', 'discover_units', markers=pkg, explicit_workspace_roots=None, boundaries=dict(inv(), schemaVersion=2))
    # U-3: the deepest unit of the file's own family wins, at every depth.
    nested = {'package.json': {'sha256': SHA}, 'packages/web/tsconfig.json': {'sha256': SHA}, 'packages/web/app/package.json': {'sha256': SHA},
              'Cargo.toml': {'sha256': SHA, 'isCargoWorkspace': False}, 'tools/gen/Cargo.toml': {'sha256': SHA, 'isCargoWorkspace': False}}
    u = run('deepest-unit-in-language', 'discover_units', markers=nested, explicit_workspace_roots=None, boundaries=None)
    run('deepest-unit-in-language', 'assign_membership', units=u['units'],
        files=['index.ts', 'packages/web/a.ts', 'packages/web/app/b.js', 'packages/web/app/deep/c.tsx', 'src/lib.rs', 'tools/gen/src/main.rs', 'packages/web/x.rs'], boundaries=None)
    # r2 (Codex B2C1-R1-RF-2): the schema bounds count characters. A 2049-character root (4098 UTF-8 bytes) admits
    # throughout; a 4097-character exclusion prefix or unit root refuses; 4096 characters admit.
    wide = 'é' * 2049
    u = run('multibyte-root', 'discover_units', markers={wide + '/package.json': {'sha256': SHA}}, explicit_workspace_roots=None, boundaries=None)
    run('multibyte-root', 'assign_membership', units=u['units'], files=[wide + '/a.js', 'b.js'], boundaries=None)
    run('multibyte-root', 'unit_scope_descriptor', units=u['units'], ignore_paths=['é' * 4096], explicit_path_prefixes=None, pruned_trees=u['prunedTrees'], boundaries=None)
    run('multibyte-prefix-over-bound', 'unit_scope_descriptor', units=u['units'], ignore_paths=['é' * 4097], explicit_path_prefixes=None, pruned_trees=u['prunedTrees'], boundaries=None)
    run('multibyte-root-over-bound', 'assign_membership', units=[dict(u['units'][0], rootPath='é' * 4097)], files=['x.js'], boundaries=None)
    run('multibyte-member-root-over-bound', 'assign_membership', units=[dict(u['units'][0], memberPackageRoots=['é' * 4097])], files=['x.js'], boundaries=None)
    # r3 (Codex B2C1-R2-RF-1): malformed roots with non-printable Unicode (U+0085, U+2028), and ASCII ones.
    for name, root in (('u0085', '/\u0085'), ('u2028', '/\u2028'), ('dot-segment', 'a/./b'), ('trailing-slash', 'a/')):
        run('malformed-root:' + name, 'assign_membership', units=[dict(u['units'][0], rootPath=root)], files=['x.js'], boundaries=None)
        run('malformed-member-root:' + name, 'assign_membership', units=[dict(u['units'][0], memberPackageRoots=[root])], files=['x.js'], boundaries=None)
    # r2 (Codex B2C1-R1-RF-3): a unit mode outside the matrix refuses in default selection.
    run('default-selection:unknown-mode', 'default_capability_selection', units=[dict(u['units'][0], languageMode='unknown-mode')], registry=[])
    # The cap sweeps (U-7): first-party directories at the cap and one beyond; installed manifests never count.
    for first, installed in ((4095, 0), (4096, 0), (4200, 0), (0, 4200)):
        markers, form = synthetic(cur, first, installed)
        rec.markers_form[marker_digest(markers)] = form
        run('cap:%d-first-party:%d-installed' % (first, installed), 'discover_units', markers=markers, explicit_workspace_roots=None, boundaries=None)
    # The scope sweep (1024 roots admit; 1025 refuse PROJECT.SCOPE_LIMIT, never truncated).
    for n in (1024, 1025):
        markers, _ = synthetic(cur, n, 0, False)
        rec.markers_form[marker_digest(markers)] = {'$synthetic': dict(firstParty=n, installed=0, rootMarker=False)}
        u = run('scope:%d-roots' % n, 'discover_units', markers=markers, explicit_workspace_roots=None, boundaries=None)
        run('scope:%d-roots' % n, 'unit_scope_descriptor', units=u['units'], ignore_paths=[], explicit_path_prefixes=None, pruned_trees=u['prunedTrees'], boundaries=None)
    # The explicit-root grammar sweep and exact explicit roots.
    tree_markers = {'package.json': {'sha256': SHA}, 'apps/web/package.json': {'sha256': SHA}, 'crates/core/Cargo.toml': {'sha256': SHA, 'isCargoWorkspace': False}}
    for spec in ('.', 'apps/web', 'apps/web/', '', '..', '/abs', 'a//b', 'a\\b', 'apps/./web', 'crates', 'docs'):
        run('explicit-root:' + repr(spec), 'discover_units', markers=tree_markers, explicit_workspace_roots=[spec], boundaries=None)
    run('explicit-roots:two', 'discover_units', markers=tree_markers, explicit_workspace_roots=['apps/web', 'crates/core'], boundaries=None)
    # Default selection over a syntax-only fallback and a mixed repository, and zero units.
    for name, markers in (('fallback', {}), ('mixed', tree_markers)):
        u = run('default-selection:' + name, 'discover_units', markers=markers, explicit_workspace_roots=None, boundaries=None)
        run('default-selection:' + name, 'default_capability_selection', units=u['units'], registry=[])
    run('default-selection:zero-units', 'default_capability_selection', units=[], registry=[])
    # The analysis-spec cardinality bound: 100 js-synthesized units request more than 1024 capabilities.
    many = {'p%03d/package.json' % i: {'sha256': SHA} for i in range(100)}
    u = run('default-selection:cardinality', 'discover_units', markers=many, explicit_workspace_roots=None, boundaries=None)
    run('default-selection:cardinality', 'default_capability_selection', units=u['units'], registry=[])
    u = run('default-selection:registry', 'discover_units', markers=tree_markers, explicit_workspace_roots=None, boundaries=None)
    for name, registry in (('declared', [{'capabilityId': 'syntax', 'languageModes': ['js-synthesized', 'rust-cargo']}]),
                           ('unregistered', [{'capabilityId': 'nope', 'languageModes': ['rust-cargo']}]),
                           ('duplicate', [{'capabilityId': 'syntax', 'languageModes': ['rust-cargo']}, {'capabilityId': 'syntax', 'languageModes': ['ts-tsconfig']}]),
                           ('mode-unregistered', [{'capabilityId': 'syntax', 'languageModes': ['cobol']}])):
        rec.case = 'default-selection:registry:' + name
        try:
            rec.default_capability_selection(units=u['units'], registry=registry)
        except Exception:  # noqa: BLE001 (recorded)
            pass


def vectors(arch, product, packages_root):
    pins = []
    for row in ARCH:
        raw = pinned(arch, *row)
        pins.append(dict(path=row[0], bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest()))
    nur = load('native_unit_reference', arch / ARCH[0][0])
    _, cur = nur.load(arch, packages(product, packages_root))
    runner = load('native_runner', arch / ARCH[2][0])
    doc = json.loads((arch / ARCH[1][0]).read_bytes())
    fixtures = doc.get('fixtures', {})
    rec = Recorder(cur, nur.v3_of)
    skipped = []
    for case in [c for c in doc['cases'] if c['id'].startswith('units-')]:
        rec.case = case['id']
        env = {'fixtures': fixtures}
        for step in case['steps']:
            fn = step['fn']
            if fn not in INSTRUMENT and fn != 'synthetic_marker_set':
                skipped.append(dict(case=case['id'], fn=fn))
                if step.get('bind'):
                    env[step['bind']] = None
                continue
            args = runner.resolve(step.get('args', {}), env)
            if fn == 'synthetic_marker_set':
                result = cur.synthetic_marker_set(**args)
                rec.markers_form[marker_digest(result)] = {'$synthetic': dict(firstParty=args['first_party'], installed=args['installed'], rootMarker=args.get('root_marker', True))}
            else:
                try:
                    result = getattr(rec, fn)(**args)
                except Exception:  # noqa: BLE001 (recorded)
                    result = None
            if step.get('bind'):
                env[step['bind']] = result
    extra(rec, cur)
    registry = json.loads((arch / ARCH[4][0]).read_bytes())
    aliases = sorted(([r['internalCode'], r['publicCode']] for r in registry['internalAliases'] if r['internalCode'] in ALIASED), key=lambda r: r[0])
    require([a[0] for a in aliases] == sorted(ALIASED) and all('selector' not in r for r in registry['internalAliases'] if r['internalCode'] in ALIASED), 'alias rows differ')
    records = {r['code'] for r in registry['records']}
    require(all(code in records for code in PUBLIC) and not any(key in records for key in ALIASED), 'public records differ')
    body = {'schemaVersion': 1,
            'aliases': aliases,
            'standing': 'B2-c1 native unit instrument vectors, generated by tools/host/discovery_unit_vectors.py from the bound B2-c0 reference (contract successor 166). Design evidence, not qualification.',
            'reference': pins, 'skipped': skipped, 'steps': rec.steps}
    return (json.dumps(body, separators=(',', ':'), ensure_ascii=True, sort_keys=True) + '\n').encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true', help='compare the output without writing repository files')
    mode.add_argument('--write', action='store_true', help='regenerate the output')
    parser.add_argument('--architecture', type=Path, required=True, help='architecture checkout holding the reference')
    parser.add_argument('--packages-root', type=Path, required=True, help='checkout holding the provisioned python-packages snapshot')
    args = parser.parse_args()
    product = Path(__file__).resolve().parent.parent.parent
    raw = vectors(args.architecture.resolve(strict=True), product, args.packages_root.resolve(strict=True))
    target = product / OUTPUT
    if args.check:
        require(target.is_file() and target.read_bytes() == raw, 'vectors differ: ' + OUTPUT)
    else:
        target.write_bytes(raw)
    print(('Verified ' if args.check else 'Generated ') + OUTPUT + ' from the B2-c0 reference at its accepted bytes.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f'Discovery unit vector generation failed: {error}', file=sys.stderr)
        raise SystemExit(1)
