"""The D15 workspace margins of the T2 census (M3-B r9 item 12; unit B3-b3c, B3-b plan r2 section 4.3).

Developer tool only. It writes or checks one generated file, crates/security/src/custody/discovery_workspace_ledger.json:
each lead-readable T2 workspace's full-ledger cost, the walker with its members entered plus the D15 reader, member and
descent terms, classified against the discovery profile's limits at the 2x margin. The security tests classify it again
(discovery_census_tests.rs).

The cost model is the bound census's, unchanged: this tool imports tools/security/discovery_census.py (its walker model,
its D15 composition `d15_terms` and `full_ledger`, its integrity-verified stores and overlays) and
tools/security/discovery_member_model.py, and adds no charge of its own. The census tool is kept byte for byte because
the blind held-out receipt binds it (B2-b4 plan r6 section 2.5): a change there would make the receipt stale and need
another blind run, which amendment A1 rejects.

The tree is each workspace as D15 discovers it (B3-b plan r2 section 3, control (b)): the verified overlay root with its
members mounted, each member a conventional Git repository (a `.git` directory: item 6b is charged at its ceilings
whatever the repository holds, and the walker prunes `.git`), W in no repository, and the reader carrier rendered from
the overlay's link map as the T2 link-map controls render it (tools/security/t2_link_controls.py: FETCH-SPEC section 6
for Cargo, equal to the cache's rendered file byte for byte; law item 20 for npm). Python has no D15 reader at M3, so
its W has no carrier. Each workspace is composed under both declaration branches:
  * automatic (branch B): the members the carrier's entries place, with the links before the walk;
  * config-workspace-roots (branch A): every member mount as a configured root, so item 6b is paid at the workspace's
    whole member count, with the links after the walk.
Every source at its envelope (the census's ENVIRONMENT_ENVELOPE and the system sources). A workspace holds only when
both branches hold; any failure returns the caps to the law (item 12). Held-out workspaces are never read (there are
none in the bound manifest).
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import os
import sys

TOOL = 'tools/security/discovery_workspace_ledger.py'
CENSUS_TOOL = 'tools/security/discovery_census.py'
LINK_TOOL = 'tools/security/t2_link_controls.py'
OUTPUT = 'crates/security/src/custody/discovery_workspace_ledger.json'
# (record key, census source): branch B, then branch A over every member mount.
BRANCHES = (('automatic', 'automatic'), ('configWorkspaceRoots', 'config-workspace-roots'))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def d15_shape(census, links, cache, ws, root_tree, members):
    """The workspace as D15 discovers it: the verified overlay root, each member mounted with a `.git` directory, and the
    reader carrier rendered from the overlay (none for Python). Returns the tree, the member mounts and the carrier's pin."""
    nodes = dict(census.compose(root_tree, members).nodes)
    mounts = [mount for mount, _ in members]
    for mount in mounts:
        require(mount + '/.git' not in nodes, 'a member store holds .git: ' + mount)
        nodes[mount + '/.git'] = dict(kind='dir')
    carrier = None
    ecosystem = ws['ecosystem']
    if ecosystem in links.RENDERED:
        path, raw = links.carrier(ecosystem, ws['overlay']['links'][ecosystem])
        if ecosystem == 'cargo':
            # FETCH-SPEC section 6's own rendering, as the cache wrote it at W.
            with open(os.path.join(cache, 'workspaces', ws['id'], '.cargo', 'config.toml'), 'rb') as fh:
                require(fh.read() == raw, 'the Cargo carrier differs from the cache rendering: ' + ws['id'])
            require(nodes.get(path, {}).get('size') == len(raw), 'the overlay carrier differs from its rendering: ' + ws['id'])
        else:
            require(path not in nodes, 'the overlay root holds a carrier already: ' + ws['id'])
        nodes[path] = dict(kind='file', size=len(raw), text=raw.decode())
        carrier = dict(path=path, bytes=len(raw), sha256=sha256(raw))
    return census.Tree(nodes), mounts, carrier


def branch_row(census, c, dm, rule, tree, mounts, source):
    """One declaration branch's composition: the admitted members, the walker with them entered, the three terms and
    the full ledger."""
    roots = list(mounts) if source == 'config-workspace-roots' else []
    member = dm.Member(c, census.ENVIRONMENT_ENVELOPE, c['SYSTEM_SOURCES'])
    terms, m, admitted = census.d15_terms(c, dm, rule, tree, member, source, roots)
    if source == 'config-workspace-roots':
        require(sorted(admitted) == sorted(mounts), 'branch A did not admit every member')
    return dict(admitted=sorted(admitted, key=lambda s: s.encode()),
                walker=dict(objects=m.objects, edges=m.edges, bytes=m.bytes, bytesPerRootByte=m.per_root_byte),
                **census.d15_row(terms, m, c['LIMITS']))


def workspace_row(census, links, c, dm, rule, cache, arch, store, manifest, ws, trees):
    root_tree, members, overlay_raw = census.verified_workspace(cache, arch, store, ws, manifest, trees)
    tree, mounts, carrier = d15_shape(census, links, cache, ws, root_tree, members)
    branches = {key: branch_row(census, c, dm, rule, tree, mounts, source) for key, source in BRANCHES}
    return dict(id=ws['id'], ecosystem=ws['ecosystem'], members=sorted(mounts, key=lambda s: s.encode()),
                overlayRecordSha256=sha256(overlay_raw), carrier=carrier, branches=branches,
                passes2x=all(b['fullLedger']['passes2x'] for b in branches.values()))


def ledger_output(product, arch, cache, c, census, links, dm, rule):
    manifest_raw = (arch / census.MANIFEST).read_bytes()
    manifest = json.loads(manifest_raw)
    store = os.path.join(cache, 'store')
    by_id = {e['id']: e for e in manifest['repositories']}
    rows = []
    for ws in manifest['workspaces']:
        if ws['heldOut'] is not False:
            rows.append(dict(id=ws['id'], status='outstanding: held-out'))
            continue
        trees = {}
        for entry_id in ws['memberIds']:
            entry = by_id[entry_id]
            trees[entry_id] = census.verified_tree(census.store_path(store, entry), entry)
        rows.append(workspace_row(census, links, c, dm, rule, cache, arch, store, manifest, ws, trees))
    failing = [r['id'] for r in rows if r.get('passes2x') is False]
    limits = c['LIMITS']
    body = {'schemaVersion': 1,
            'standing': 'The B3-b3c D15 workspace margins (M3-B r9 item 12; B3-b plan r2 section 4.3): each lead-readable T2 '
                        'workspace composed as D15 discovers it (members as conventional Git repositories, the reader carrier '
                        'rendered from the overlay), under both declaration branches, with its full ledger: the walker with '
                        'members entered plus the reader, member and descent terms of the bound census model. Generated by '
                        'tools/security/discovery_workspace_ledger.py from integrity-verified stores. Design evidence, not '
                        'product qualification.',
            'manifest': dict(path=census.MANIFEST, bytes=len(manifest_raw), sha256=sha256(manifest_raw)),
            'tools': [census.pin_row(product, p) for p in (TOOL, CENSUS_TOOL, census.MEMBER_MODEL, LINK_TOOL)],
            'closure': [census.pin_row(product, p) for p, _, _ in census.CLOSURE],
            'sizes': dict(c['SIZES']),
            'limits': dict(objects=limits[0], edges=limits[1], bytes=limits[2]),
            'margin': 2,
            'rootLengths': list(census.ROOT_LENGTHS),
            'environmentEnvelope': dict(entries=census.ENVIRONMENT_ENVELOPE[0], bytes=census.ENVIRONMENT_ENVELOPE[1]),
            'branches': [dict(key=key, source=source) for key, source in BRANCHES],
            'workspaces': rows,
            'failingWorkspaces': failing,
            'caps': 'returned-to-law' if failing else 'recorded-margin-holds'}
    return (json.dumps(body, indent=1, ensure_ascii=True) + '\n').encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true', help='compare the output without writing it')
    mode.add_argument('--write', action='store_true', help='regenerate the output')
    parser.add_argument('--architecture', type=Path, required=True, help='architecture checkout (manifest, reference)')
    parser.add_argument('--packages-root', type=Path, required=True, help='checkout holding the provisioned python-packages snapshot')
    parser.add_argument('--t2-cache', type=Path, required=True, help='the private durable T2 cache (store/ and workspaces/)')
    args = parser.parse_args()
    product = Path(__file__).resolve().parent.parent.parent
    arch = args.architecture.resolve(strict=True)
    census = load('discovery_census', product / CENSUS_TOOL)
    links = load('t2_link_controls', product / LINK_TOOL)
    c = census.costs(product)
    _, _, _, rule = census.load_reference(product, arch, args.packages_root.resolve(strict=True))
    raw = ledger_output(product, arch, str(args.t2_cache.resolve(strict=True)), c, census, links,
                        census.load_member_model(product), rule)
    target = product / OUTPUT
    if args.check:
        require(target.is_file() and target.read_bytes() == raw, 'output differs: ' + OUTPUT)
    else:
        target.write_bytes(raw)
    print(('Verified ' if args.check else 'Generated ') + OUTPUT)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f'Discovery workspace ledger failed: {error}', file=sys.stderr)
        raise SystemExit(1)
