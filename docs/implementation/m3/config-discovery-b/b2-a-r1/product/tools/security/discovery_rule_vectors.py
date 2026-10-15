"""Cross-implementation vectors for the shared discovery rule (M3-B r5 items 13 and 14; unit B2-a).

Developer tool only. It runs the B2-a reference refresh (contract successor 163) at its accepted architecture bytes
over a fixture set and writes or checks crates/security/src/custody/discovery_rule_vectors.json: each case's function,
arguments and the reference's result. The product test reproduces every case. The reference imports only the
standard library. No filesystem tree, network or environment input.

Large supplied inventories are stored as {"range": [prefix, suffix, count]} and expanded identically by the
product test."""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import itertools
import json
import sys

OUTPUT = 'crates/security/src/custody/discovery_rule_vectors.json'
# Architecture input (contract successor 163): path, bytes, SHA-256.
REFERENCE = ('docs/implementation/m3/config-discovery-b/b2-a-reference/reference/discovery-defaults.sx1-r1.py', 25293,
             '4a104209af0ba89c76826ba7f6be4c4085f1eb7db90410f6bb731041562fdcc8')
SWEEP_SEGMENTS = ('a', 'node_modules', '.git', 'target', '.opensip', 'src', 'Cargo.toml')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def model(arch):
    path, size, digest = REFERENCE
    raw = (arch / path).read_bytes()
    require(len(raw) == size and hashlib.sha256(raw).hexdigest() == digest, 'input pin mismatch: ' + path)
    spec = importlib.util.spec_from_file_location('discovery_rule_reference', arch / path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def expand(value):
    if isinstance(value, dict) and set(value) == {'range'}:
        prefix, suffix, count = value['range']
        return [prefix + str(i) + suffix for i in range(count)]
    return value


def expand_list(values):
    out = []
    for value in values:
        if isinstance(value, dict) and set(value) == {'range'}:
            out.extend(expand(value))
        else:
            out.append(value)
    return out


def plain(value):
    if isinstance(value, (set, frozenset)):
        return sorted(value, key=lambda s: s.encode('utf-8'))
    if isinstance(value, tuple):
        return list(value)
    if isinstance(value, dict) and any(isinstance(k, tuple) for k in value):
        return sorted([list(k) for k in value], key=lambda k: (k[0].encode('utf-8'), k[1]))
    return value


def fixtures():
    cases = []

    def case(function, *args, **kwargs):
        cases.append(dict(function=function, args=list(args), kwargs=kwargs))

    # Explicit roots (SL:224-232).
    for spec in ['.', '', 'a', 'a/b', 'a/b/', 'a//', 'a//b', '/a', 'a\\b', 'a\x00b', '..', 'a/../b', './a', 'a/.', '.opensip', 'packages/target', '/']:
        case('normalize_explicit_root', spec)
    for root in ['', 'a/b']:
        case('spell_root', root)
    # The pruning controls and SX-1 controls (the refresh checker's fixtures).
    for root in ['', 'workspace']:
        pre = root + '/' if root else ''
        for segment in ['node_modules', '.git', '.hg', '.svn', '.jj']:
            case('classify_path', pre + 'target/' + segment + '/pkg/file', [root], [])
            case('classify_path', pre + segment + '/target/pkg/file', [root, pre + segment], [])
            case('classify_path', pre + 'src/target/' + segment + '/file', [root], [])
        case('classify_path', pre + 'target/debug/file', [root], [])
        case('classify_path', pre + 'packages/target/index.ts', [root], [])
        case('classify_path', pre + 'targetish/node_modulesish/file', [root], [])
        markers = [pre + 'Cargo.toml', pre + 'target/dependency/Cargo.toml', pre + 'node_modules/pkg/Cargo.toml', pre + '.git/Cargo.toml', pre + 'src/Cargo.toml']
        for perm in [markers, list(reversed(markers)), markers[2:] + markers[:2]]:
            case('cargo_roots_from_markers', perm, [])
        case('cargo_roots_from_markers', [pre + 'target/inner/Cargo.toml'], [])
    for path, cargo, members in [('.opensip/local.json', [''], []), ('.opensip', [], []), ('m/.opensip/local.json', [], ['m']), ('a/b/.opensip/x', [], ['a/b']),
                                 ('src/.opensip/x.ts', [''], []), ('m/.opensip/x.ts', [], []), ('m/src/.opensip/x', [], ['m']), ('.OpenSIP/x', [], []),
                                 ('.opensipx/y', [], []), ('node_modules/.opensip/x', [], []), ('.opensip/node_modules/x', [], []), ('.opensip/target/x', ['.opensip'], []),
                                 ('m/target/x', ['m'], ['m']), ('.git/m/.opensip', [], ['.git/m']), ('', [], []), ('Node_Modules/x', [], [])]:
        case('classify_path', path, cargo, members)
    case('cargo_roots_from_markers', ['Cargo.toml', '.opensip/Cargo.toml', 'm/Cargo.toml', 'm/.opensip/Cargo.toml'], ['m'])
    case('pruned_anchors_from_directories', ['m', 'm/.opensip', 'src/.opensip', '', '/abs/node_modules', 'node_modules', 'node_modules/x', 'target'], [''], ['m'])
    # The sweep: every path of up to three segments over a small alphabet, under three Cargo and two member settings.
    for depth in (1, 2, 3):
        for parts in itertools.product(SWEEP_SEGMENTS, repeat=depth):
            for cargo in ([], [''], ['', 'a']):
                for members in ([], ['a']):
                    case('classify_path', '/'.join(parts), cargo, members)
    # Enumeration (U-4a; U-7).
    E = 'enumerate_units'
    case(E, ['package.json', '.opensip/package.json', 'src/.opensip/package.json'], observed_directories=['.opensip', 'src/.opensip'], marker_inventory_basis='not-enumerated')
    case(E, ['package.json'], observed_directories=['.opensip'])
    case(E, ['package.json'])
    case(E, ['Cargo.toml', 'target/Cargo.toml', {'range': ['target/node_modules/pkg', '/package.json', 4200]}], observed_directories=['target', 'target/node_modules'], marker_inventory_basis='not-enumerated')
    case(E, ['Cargo.toml', 'target/Cargo.toml', {'range': ['target/node_modules/pkg', '/package.json', 4200]}])
    case(E, ['package.json', {'range': ['node_modules/p', '/package.json', 4200]}])
    case(E, [{'range': ['p', '/package.json', 4096]}])
    case(E, [{'range': ['p', '/package.json', 4097]}])
    case(E, [{'range': ['p', '/package.json', 4097]}], enforce_limit=False)
    case(E, ['package.json', 'node_modules/a/package.json', '.hg/x/Cargo.toml'], observed_directories=['node_modules', '.hg', '.svn'], unreadable_anchors=['.hg'])
    case(E, ['/abs/package.json', 'README.md', 'a/tsconfig.json', 'a/jsconfig.json', 'b/package.json', 'b/package.json'])
    case(E, ['m/package.json', 'm/.opensip/package.json'], observed_directories=['m/.opensip'], member_roots=['m'])
    # Locators and boundaries.
    for root, absolute in [('/w', '/w'), ('/w', '/w/a/b'), ('/w/', '/w/a'), ('/w', '/wx/a'), ('/w', '/w/'), ('/w', '/w/a//b'), ('/w', '/w/./a'), ('/w', '/w/a\\b'), ('', '/w'), ('/', '/a')]:
        case('relative_locator', root, absolute)
    for path in ['vendor/x', 'vendor/x/y', 'vendor/xy', 'tools/p/q', 'vendor/x/tools/p', 'src', '']:
        case('classify_boundary', path, ['vendor/x'], ['tools/p', 'vendor/x/tools/p'])
    rows = [dict(path='deep', reason='DEPTH'), dict(path='a', reason='MARKER_CUSTODY:package.json:mode'), dict(path='b', reason='DIRECTORY_CUSTODY:owner'), dict(path='', reason='DIRECTORY_CUSTODY:acl')]
    for unit, marker in [('deep/x', None), ('a', 'package.json'), ('a', 'Cargo.toml'), ('a', None), ('b', 'Cargo.toml'), ('c', 'package.json')]:
        case('classify_custody_exclusion', unit, marker, rows[:3])
    case('classify_custody_exclusion', 'anything', None, rows)
    case('boundary_excluded_prefixes', dict(nestedRepositories=['vendor/x', 'a'], nestedProjects=['tools/p', 'a'], custodyExcludedUnits=rows, memberRepositories=['repos/m']))
    for units, cargo, members in [([''], [''], []), (['', 'm/u'], [''], ['m']), ([], [], []), (['b', 'a'], ['b'], ['z', 'y'])]:
        case('conventional_excluded_prefixes', units, cargo, members)
    return cases


def run(module, cases):
    out = []
    for c in cases:
        args = [expand_list(a) if isinstance(a, list) else a for a in c['args']]
        kwargs = {k: (expand_list(v) if isinstance(v, list) else v) for k, v in c['kwargs'].items()}
        fn = getattr(module, c['function'])
        try:
            if c['function'] in ('classify_path', 'cargo_roots_from_markers', 'pruned_anchors_from_directories', 'conventional_excluded_prefixes'):
                result = {'ok': plain(fn(*args))}
            elif c['function'] == 'classify_boundary':
                result = {'ok': plain(fn(*args))}
            else:
                result = {'ok': plain(fn(*args, **kwargs))}
        except module.RootGrammarError as e:
            result = {'refusal': str(e)}
        except module.BoundaryError as e:
            result = {'refusal': str(e)}
        out.append({**c, 'reference': result})
    return out


def vectors(arch):
    module = model(arch)
    body = {'schemaVersion': 1,
            'standing': 'Reference vectors for the product shared discovery rule (M3-B r5 items 13 and 14). Generated by '
                        'tools/security/discovery_rule_vectors.py from the B2-a reference refresh at its accepted bytes; '
                        'design reference results over supplied paths, not product qualification.',
            'sources': [dict(path=REFERENCE[0], bytes=REFERENCE[1], sha256=REFERENCE[2])],
            'cases': run(module, fixtures())}
    return (json.dumps(body, indent=None, separators=(',', ':'), ensure_ascii=True) + '\n').encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true', help='compare the output without writing repository files')
    mode.add_argument('--write', action='store_true', help='regenerate the output')
    parser.add_argument('--architecture', type=Path, required=True, help='architecture checkout holding the reference')
    args = parser.parse_args()
    product = Path(__file__).resolve().parent.parent.parent
    raw = vectors(args.architecture.resolve(strict=True))
    target = product / OUTPUT
    if args.check:
        require(target.is_file() and target.read_bytes() == raw, 'vectors differ: ' + OUTPUT)
    else:
        target.write_bytes(raw)
    print(('Verified ' if args.check else 'Generated ') + OUTPUT + ' from the B2-a reference at its accepted bytes.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f'Discovery rule vector generation failed: {error}', file=sys.stderr)
        raise SystemExit(1)
