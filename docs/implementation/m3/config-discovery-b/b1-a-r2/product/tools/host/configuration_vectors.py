"""Cross-implementation byte vectors for the host configuration resolver (M3-B r4 item 4 controls; unit B1-a).

Developer tool only. It runs PCM, the accepted reference resolver, at its accepted architecture bytes over a
fixture set and writes or checks crates/host/src/configuration_vectors.json: each fixture's layers, mode and
PCM's expected resolvedConfigDigest or refusal class. The product test pins those results.

PCM imports jsonschema through its canonical reference; the tool imports the product's provisioned snapshot
only after every file matches its generator-closure pin. No network or environment input.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import importlib.util
import json
import sys

OUTPUT = 'crates/host/src/configuration_vectors.json'
FOUNDATION = 'docs/coop/design-corrections/foundation/'
# Architecture inputs (each a member of candidate-subject.v45.json): path, bytes, SHA-256.
ARCH = (
    (FOUNDATION + 'product-configuration-model.py', 3674, '055ab34c76f3d241633dd8e0d0a0b017c29747056a9d8de75b29bf57bd79fa8b'),
    (FOUNDATION + 'canonical.py', 6465, 'd47f25db0fb09ceb84282a89fdf74055cb81ccb9de26f85a5a70b032b9a6b442'),
    (FOUNDATION + 'product-configuration.schema.v2.json', 10262, '591a66e5dc35c4be516eaf68bacc62f9a82260b0c1698665dd85f7613b78e14d'),
    (FOUNDATION + 'identity-schemas.v2.json', 148414, 'c56679857b83e0ff71f8eca9345e29433617030945429d524bb5645669d267d5'),
    (FOUNDATION + 'check-product-configuration.py', 5378, 'a6f90facef164c12ae8db95053070372baf3aea63c47cdd096e8b17306c70a36'),
    ('docs/coop/design-corrections/native/native-capability-matrix.v2.json', 36595,
     '4b1c19b03a34a271718b1e7e79335aa6f0735affd7cd36018035eeb4e7b18a14'),
)
PACK = 'opensip.preview.typescript.pack:1'
A = '0f0e0d0c-0b0a-4908-8706-050403020100'
B = '1f1e1d1c-1b1a-4918-9716-151413121110'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def pinned(root, path, size, digest):
    raw = (root / path).read_bytes()
    require(len(raw) == size and hashlib.sha256(raw).hexdigest() == digest, 'input pin mismatch: ' + path)
    return raw


def packages(product, packages_root):
    closure = json.loads((product / 'tools/contracts/generator-closure.json').read_bytes())
    rows = [r for r in closure['files'] if r['path'].startswith('tools/contracts/python-packages/')]
    require(rows, 'no pinned python packages')
    for row in rows:
        pinned(packages_root, row['path'], row['bytes'], row['sha256'])
    sys.path.insert(0, str(packages_root / 'tools/contracts/python-packages'))


def model(arch):
    for row in ARCH:
        pinned(arch, *row)
    spec = importlib.util.spec_from_file_location('pcm', arch / ARCH[0][0])
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def fixtures(capabilities):
    """The fixture set. Every layer respects M3-B item 2's allowlist, so PCM and the product agree on
    admission; the AQ:183-187 / check-product-configuration.py cases are re-expressed on that basis."""
    defaults = {'schemaVersion': 2,
                'analysis': {'profileId': 'default', 'capabilities': capabilities, 'budget': {'unit': 'work-units', 'limit': 1000}},
                'components': {'request': [{'stableId': A, 'version': '1.2.3'}], 'pins': [], 'holds': [], 'allowedScopes': ['project', 'global']},
                'policy': {'packIds': [PACK]}}
    project = {'schemaVersion': 2,
               'discovery': {'entryPoints': ['src/main.rs'], 'workspaceRoots': ['src'], 'ignorePaths': ['target']},
               'policy': {'waiverIds': []}, 'evidence': {'importIds': []},
               'retention': {'maxBytes': None, 'maxRuns': None, 'maxAgeSeconds': None}, 'ui': {'color': 'auto'}}

    def doc(**sections):
        return {'schemaVersion': 2, **sections}

    def raw(value):
        return value if isinstance(value, str) else json.dumps(value, separators=(',', ':'), sort_keys=True)

    def without(value, *path):
        value = copy.deepcopy(value)
        node = value
        for key in path[:-1]:
            node = node[key]
        node.pop(path[-1])
        return value

    minimal = doc(analysis=defaults['analysis'])
    cases = []

    def case(id, layers, interactive=False, pcm=None, note=None):
        layers = {k: (v if k in ('defaults', 'flags') else raw(v)) for k, v in layers.items()}
        row = {'id': id, 'interactive': interactive, 'layers': layers}
        if pcm is not None:
            row['pcmLayers'] = {k: raw(v) for k, v in pcm.items()}
        if note:
            row['note'] = note
        cases.append(row)

    base = {'defaults': defaults, 'project': project}
    case('zero-project-config-mixed-native-default', {'defaults': defaults})
    case('base', base)
    case('explicit-entry-points-override-discovery', {**base, 'local': doc(discovery={'entryPoints': ['app/main.rs']})}, interactive=True)
    case('workspace-project-root-sentinel', {'defaults': defaults, 'project': doc(discovery={'workspaceRoots': ['.']})})
    case('ignore-paths-root-sentinel', {'defaults': defaults, 'project': doc(discovery={'ignorePaths': ['.']})})
    case('entry-point-root-sentinel-is-not-a-source', {'defaults': defaults, 'project': doc(discovery={'entryPoints': ['.']})})
    case('explicit-empty-workspace-roots-refused', {'defaults': defaults, 'project': doc(discovery={'workspaceRoots': []})})
    for id, text in [('fractional', '{"schemaVersion":2.0}'), ('exponent', '{"schemaVersion":2e0}'),
                     ('boolean', '{"schemaVersion":true}'), ('unknown-key', '{"schemaVersion":2,"shell":"run"}'),
                     ('unknown-capability', '{"schemaVersion":2,"analysis":{"capabilities":["other.magic"]}}'),
                     ('path-escape', '{"schemaVersion":2,"discovery":{"entryPoints":["../a.ts"]}}'),
                     ('absolute-path', '{"schemaVersion":2,"discovery":{"workspaceRoots":["/src"]}}'),
                     ('backslash-path', '{"schemaVersion":2,"discovery":{"ignorePaths":["a\\\\b"]}}'),
                     ('empty-segment-path', '{"schemaVersion":2,"discovery":{"entryPoints":["a//b.rs"]}}'),
                     ('duplicate-key', '{"schemaVersion":2,"schemaVersion":2}'),
                     ('trailing-data', '{"schemaVersion":2} {}'),
                     ('negative-zero-budget', '{"schemaVersion":2,"analysis":{"budget":{"unit":"work-units","limit":-0}}}'),
                     ('budget-over-uint53', '{"schemaVersion":2,"analysis":{"budget":{"unit":"work-units","limit":9007199254740992}}}'),
                     ('newline-suffixed-profile', '{"schemaVersion":2,"analysis":{"profileId":"default\\n"}}'),
                     ('schema-major-three', '{"schemaVersion":3}')]:
        case(id, {'defaults': defaults, 'project': text})
    case('ci-does-not-consume-invalid-local', {**base, 'local': 'invalid'}, interactive=False)
    case('interactive-consumes-invalid-local', {**base, 'local': 'invalid'}, interactive=True)
    case('ui-excluded-from-semantic-config', {**base, 'global': doc(ui={'color': 'never'})})
    case('retention-excluded-from-semantic-config', {**base, 'global': doc(retention={'maxBytes': 1, 'maxRuns': 2, 'maxAgeSeconds': 3})})
    case('semantic-budget-changes-config', {**base, 'global': doc(analysis={'budget': {'unit': 'work-units', 'limit': 999}})})
    case('set-order-not-semantic', {'defaults': defaults, 'project': {**project, 'analysis': {'capabilities': list(reversed(capabilities))}}})
    case('entry-point-permutation-not-semantic', {'defaults': defaults, 'project': {**project, 'discovery': {**project['discovery'], 'entryPoints': ['src/z.rs', 'src/a.rs']}}})
    case('entry-point-permutation-other-order', {'defaults': defaults, 'project': {**project, 'discovery': {**project['discovery'], 'entryPoints': ['src/a.rs', 'src/z.rs']}}})
    case('allowed-scopes-global-only-changes-config', {**base, 'local': doc(components={'allowedScopes': ['global']})}, interactive=True)
    case('waiver-unregistered', {'defaults': defaults, 'project': doc(policy={'waiverIds': ['unknown']})})
    case('profile-unregistered', {'defaults': defaults, 'project': doc(analysis={'profileId': 'other'})})
    case('capability-subset-is-semantic', {'defaults': defaults, 'project': doc(analysis={'capabilities': ['imports', 'syntax']})})
    case('duplicate-component-request', {'defaults': defaults, 'project': doc(components={'request': [{'stableId': B, 'version': '1.0.0'}, {'stableId': B, 'versionConstraint': '1.0.0'}]})})
    case('component-pins-and-holds', {'defaults': defaults, 'project': doc(components={'pins': [{'stableId': B, 'version': '2.0.0'}], 'holds': [{'stableId': A, 'version': '1.2.3'}]})})
    case('component-range-request', {'defaults': defaults, 'project': doc(components={'request': [{'stableId': B, 'versionConstraint': {'min': '1.0.0', 'max': '2.0.0', 'includeMin': True, 'includeMax': False}}]})})
    case('resolved-empty-sections-always-present', {'defaults': minimal})
    case('explicit-empty-input-sections-same-digest', {'defaults': minimal, 'project': doc(components={}, discovery={}, policy={}, evidence={})})
    for missing in ['profileId', 'capabilities', 'budget']:
        case('resolved-required-' + missing, {'defaults': without(minimal, 'analysis', missing)})
    # Item 1 controls: each layer's win at every adjacent pair (the loss is the pair's lower value).
    budget = lambda n: {'analysis': {'budget': {'unit': 'work-units', 'limit': n}}}
    case('defaults-loses-to-global', {**base, 'global': doc(**budget(999))})
    case('global-loses-to-project', {'defaults': defaults, 'global': doc(**budget(999)), 'project': {**project, **budget(777)}})
    case('project-loses-to-local', {**base, 'local': doc(discovery={'workspaceRoots': ['lib']})}, interactive=True)
    case('local-loses-to-flags', {**base, 'local': doc(discovery={'workspaceRoots': ['lib']}), 'flags': doc(discovery={'workspaceRoots': ['app']})}, interactive=True)
    case('higher-array-replaces-lower-whole', {**base, 'local': doc(discovery={'ignorePaths': ['dist']})}, interactive=True)
    # Item 6 controls: provenance-only moves keep the digest; --workspace-root's winning set is semantic.
    case('workspace-root-from-flags-same-roots', {'defaults': defaults, 'project': without(project, 'discovery', 'workspaceRoots'), 'flags': doc(discovery={'workspaceRoots': ['src']})})
    case('workspace-root-from-flags-other-roots', {'defaults': defaults, 'project': without(project, 'discovery', 'workspaceRoots'), 'flags': doc(discovery={'workspaceRoots': ['lib']})})
    case('budget-moved-to-project-same-value', {'defaults': defaults, 'project': {**project, **budget(1000)}})
    # Item 11: a schema-one project file. PCM reads version 2 only, so its input is the in-memory projection.
    one = {'schemaVersion': 1, 'analysis': {'budget': {'unit': 'work-units', 'limit': 555}},
           'components': {'pins': [{'stableId': B, 'version': '3.0.0'}], 'allowedScopes': ['global']}}
    case('schema-one-project-projection', {'defaults': defaults, 'project': one},
         pcm={'defaults': defaults, 'project': {**one, 'schemaVersion': 2}},
         note='PCM input is the version-2 projection; the product reads the version-1 bytes through the preview carrier schema')
    case('schema-one-global-projection', {**base, 'global': {'schemaVersion': 1, 'ui': {'color': 'always'}, 'analysis': {'budget': {'unit': 'work-units', 'limit': 444}}}},
         pcm={**base, 'global': {'schemaVersion': 2, 'ui': {'color': 'always'}, 'analysis': {'budget': {'unit': 'work-units', 'limit': 444}}}},
         note='PCM input is the version-2 projection')
    return cases


def run(module, cases, registry):
    C = module.C
    out = []
    for case in cases:
        layers = case.get('pcmLayers') or case['layers']
        pcm = {k: (C.canonical(v) if isinstance(v, dict) else v.encode('utf-8')) for k, v in layers.items()}
        try:
            result = module.resolve(pcm, registry, ci=not case['interactive'])
            expected = {'digest': result['resolvedConfigDigest'], 'semantic': result['semantic'],
                        'provenance': dict(sorted(result['provenance'].items()))}
        except C.AdmissionError as error:
            code = str(error)
            expected = {'refusal': code if code.startswith('CONFIG_') else 'LEXICAL'}
        except C.ValidationError:
            expected = {'refusal': 'SCHEMA'}
        out.append({**case, 'pcm': expected})
    return out


def vectors(arch, product, packages_root):
    packages(product, packages_root)
    module = model(arch)
    matrix = json.loads((arch / ARCH[5][0]).read_bytes())
    capabilities = [c['id'] for c in matrix['capabilities']]
    registry = {'profiles': ['default'], 'capabilities': capabilities, 'packs': [PACK], 'waivers': []}
    body = {'schemaVersion': 1,
            'standing': 'PCM byte vectors for the product resolver (M3-B r4 item 4). Generated by tools/host/configuration_vectors.py '
                        'from PCM at its accepted bytes; design reference results, not product qualification.',
            'sources': [{'path': p, 'bytes': n, 'sha256': d} for p, n, d in ARCH],
            'registry': registry,
            'cases': run(module, fixtures(capabilities), registry)}
    return (json.dumps(body, indent=1, ensure_ascii=True) + '\n').encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true', help='compare the output without writing repository files')
    mode.add_argument('--write', action='store_true', help='regenerate the output')
    parser.add_argument('--architecture', type=Path, required=True, help='architecture checkout holding PCM')
    parser.add_argument('--packages-root', type=Path, required=True,
                        help='checkout holding the provisioned tools/contracts/python-packages snapshot')
    args = parser.parse_args()
    product = Path(__file__).resolve().parent.parent.parent
    raw = vectors(args.architecture.resolve(strict=True), product, args.packages_root.resolve(strict=True))
    target = product / OUTPUT
    if args.check:
        require(target.is_file() and target.read_bytes() == raw, 'vectors differ: ' + OUTPUT)
    else:
        target.write_bytes(raw)
    print(('Verified ' if args.check else 'Generated ') + OUTPUT + ' from PCM at its accepted bytes.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f'Configuration vector generation failed: {error}', file=sys.stderr)
        raise SystemExit(1)
