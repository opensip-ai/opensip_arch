"""Cross-implementation vectors for the pure discovery core (M3-B r5 item 13; unit B2-b2).

Developer tool only. It runs B2-b0, the current discovery reference (contract successor 164), at its accepted
architecture bytes over every case of security/discovery-cases.v1.json and over the reference checker's own
synthetic controls, and writes or checks crates/security/src/custody/discovery_scan_vectors.json. Each vector is
what the walker hands the core (the observed scope, the selected root, the upward provenance, the unit source and
the invocation facts) and the reference's version-3 result: the partial provenance (workspaceDeclarations pending
B3-b) and, for an accepted result, the complete boundary inventory. A case that refuses before `finish` is upward
selection, not the core's, and is listed by id only.

SLM imports canonical.py, which imports jsonschema; the tool loads the provisioned snapshot only after every file
matches its generator-closure pin. No filesystem tree, network or environment input.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import importlib.util
import json
import sys

OUTPUT = 'crates/security/src/custody/discovery_scan_vectors.json'
REF = 'docs/implementation/m3/config-discovery-b/b2-b-reference/'
# Architecture inputs (contract successor 164 and its parents): path, bytes, SHA-256.
ARCH = (
    (REF + 'reference/discovery_scan_reference.py', 12574, '6714575ccee1474e2d7c20c4e5e9b6c95b498ad155ec1e69fc9d6ba5f3e7e32b'),
    (REF + 'evidence/check.py', 19556, 'be618884e783c90ef7ff5dd33a1c2052ac2ee5ac54cfa5b3316e48c8065785cb'),
    ('docs/coop/design-corrections/security/discovery-cases.v1.json', 152804, '2b3f9fdbe99313f75b8545b53c62011a4533bcef4593149aa70b84bddf5303b3'),
)
UPWARD = ('mode', 'configPath', 'walked', 'stopReason', 'vcs', 'explicitPathWasSymlink')


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


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def controls(chk):
    """The reference checker's synthetic control inputs (B2-b0 evidence/check.py), named."""
    tree, inp = chk.tree, chk.inp
    out = []
    for label, anchor, files in [('dependency-tree', 'node_modules', ['package.json']), ('vcs-tree', '.git', ['package.json']),
                                 ('cargo-build-output', 'target', ['Cargo.toml']), ('opensip-custody-state', '.opensip', ['package.json'])]:
        fs = tree(dirs=[anchor + '/sub', anchor + '/repo'], files=files + [anchor + '/.git/HEAD', anchor + '/opensip.json', anchor + '/package.json',
                                                                           anchor + '/Cargo.toml', anchor + '/sub/package.json'], vcs=[anchor + '/repo'])
        out.append(('anchor-' + label, inp(fs)))
        out.append(('anchor-vcs-' + label, inp(tree(dirs=[anchor + '/.git'], files=files, vcs=[anchor]), explicitProject='/h/w')))
    fs = tree(dirs=['target/u'], files=['Cargo.toml', 'target/u/package.json'])
    out.append(('cargo-target-join-explicit', inp(fs, explicitProject='/h/w', explicitJoins=['target/u'])))
    out.append(('cargo-target-join-config', inp(fs, explicitProject='/h/w', configWorkspaceRoots=['target/u'])))
    out.append(('ordinary-target-join', inp(tree(dirs=['target/u'], files=['target/u/package.json']), explicitProject='/h/w', explicitJoins=['target/u'])))
    out.append(('crossing-above-prune', inp(tree(dirs=['r/node_modules/x'], files=['r/node_modules/x/package.json'], vcs=['r']), explicitProject='/h/w', explicitJoins=['r/node_modules/x'])))
    out.append(('repository-below-prune', inp(tree(dirs=['node_modules/x/sub'], files=['node_modules/x/sub/package.json'], vcs=['node_modules/x']), explicitProject='/h/w', explicitJoins=['node_modules/x/sub'])))
    out.append(('nested-in-nested', inp(tree(dirs=['a/b', 'p/q'], files=['package.json', 'p/opensip.json', 'p/q/opensip.json'], vcs=['a', 'a/b']))))
    sibling = tree(dirs=['a/u', 'b/repo', 'b/proj', 'b/c'], files=['a/u/package.json', 'b/proj/opensip.json', 'b/c/package.json'], vcs=['b/repo'])
    out.append(('explicit-sibling', inp(sibling, explicitProject='/h/w', explicitJoins=['a/u'])))
    out.append(('config-sibling', inp(copy.deepcopy(sibling), explicitProject='/h/w', configWorkspaceRoots=['a/u'])))
    out.append(('markers-below-anchor', inp(tree(dirs=['node_modules/p/target/q'], files=['package.json', 'node_modules/p/Cargo.toml', 'node_modules/p/target/q/package.json']))))
    # r2 (Codex B2B2-1): a marker failing both its ACL and its links or size reports the ACL first (SLM _file_custody).
    def marker(label, waive=False, foreign=False, **fields):
        fs = tree(dirs=['u'], files=['u/package.json', 'u/Cargo.toml'])
        fs['/h/w/u/package.json'].update(fields)
        if foreign:
            for d in ('/h/w', '/h/w/u'):
                fs[d]['uid'] = 1001
            fs['/h/w/u/package.json']['uid'] = 1001
        extra = dict(trustProjectOwner=True) if waive else {}
        out.append(('marker-order-' + label, inp(fs, explicitProject='/h/w', explicitJoins=['u'], **extra)))
    marker('acl-write-hard-linked', nlink=2, aclWrite=['uid:4242'])
    marker('acl-unreadable-hard-linked', nlink=2, aclUnreadable=True)
    marker('acl-write-oversize', size=4194305, aclWrite=['uid:4242'])
    marker('acl-unreadable-oversize', size=4194305, aclUnreadable=True)
    marker('hard-linked-only', nlink=2)
    marker('oversize-only', size=4194305)
    marker('waived-chain-foreign-marker-hard-linked', waive=True, foreign=True, nlink=2)
    marker('waived-chain-foreign-marker-acl-write', waive=True, foreign=True, aclWrite=['uid:4242'])
    for n in (256, 257, 258):
        rel = '/'.join('d' for _ in range(n))
        out.append(('depth-unit-%d' % n, inp(tree(dirs=[rel], files=['package.json', rel + '/package.json']))))
        out.append(('depth-config-%d' % n, inp(tree(dirs=[rel], files=['package.json', rel + '/opensip.json']), explicitProject='/h/w')))
        out.append(('depth-vcs-%d' % n, inp(tree(dirs=[rel], files=['package.json'], vcs=[rel]), explicitProject='/h/w')))
    return out


def vector(ref, slm, rule, case_id, case_input):
    cur, downward, second = ref.current(slm, rule, case_input)
    if downward is None:
        return None
    prov = cur['provenance']
    source = prov['unitSource']
    roots = case_input.get('explicitJoins') if source == 'explicit-joins' else case_input.get('configWorkspaceRoots') if source == 'config-workspace-roots' else []
    partial = ref.project_v3(cur)
    expected = {k: v for k, v in partial.items() if k != 'pendingFields'}
    inventory = ref.boundary_inventory_v3(rule, partial) if partial['status'] == 'ACCEPT' else None
    return dict(id=case_id,
                input=dict(uid=case_input['invokingUid'], ci=bool(case_input.get('ci', False)), groups=sorted(case_input.get('authorizedGroupIds', [])),
                           waive=bool(case_input.get('trustProjectOwner', False)), explicitProject=case_input.get('explicitProject'),
                           basis=case_input.get('prunedTreeMarkerInventory', 'observed-inventory'), source=source, roots=roots or [],
                           root=prov['selectedRoot'], upward={k: prov[k] for k in UPWARD}, scope=second['fs']),
                expected=expected, inventory=inventory)


def vectors(arch, product, packages_root):
    packages(product, packages_root)
    for row in ARCH:
        pinned(arch, *row)
    ref = load('discovery_scan_reference', arch / ARCH[0][0])
    chk = load('discovery_scan_reference_check', arch / ARCH[1][0])
    slm, rule = ref.load(arch)
    cases, upward_only = [], []
    for case in json.loads((arch / ARCH[2][0]).read_bytes())['cases']:
        if case.get('model', 'discovery') != 'discovery':
            continue
        v = vector(ref, slm, rule, case['id'], case['input'])
        (upward_only.append(case['id']) if v is None else cases.append(v))
    for label, i in controls(chk):
        v = vector(ref, slm, rule, 'control:' + label, i)
        require(v is not None, 'control refused before finish: ' + label)
        cases.append(v)
    body = {'schemaVersion': 1,
            'standing': 'B2-b0 current-reference vectors for the pure discovery core (M3-B r5 item 13). Generated by '
                        'tools/security/discovery_scan_vectors.py at the reference\'s accepted bytes; design reference results over '
                        'synthetic observed scopes, not product qualification.',
            'sources': [dict(path=p, bytes=n, sha256=d) for p, n, d in ARCH],
            'upwardOnly': upward_only,
            'cases': cases}
    return (json.dumps(body, separators=(',', ':'), ensure_ascii=True) + '\n').encode()


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
    print(('Verified ' if args.check else 'Generated ') + OUTPUT + ' from the B2-b0 reference at its accepted bytes.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f'Discovery scan vector generation failed: {error}', file=sys.stderr)
        raise SystemExit(1)
