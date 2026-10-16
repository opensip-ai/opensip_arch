"""Cross-implementation vectors for the S3 downward walk and core with admitted D15 members (M3-B r9 item 22; unit B3-b2a).

Developer tool only. Each case is a walk-vector tree description (tools/security/discovery_walk_vectors.py's format and
its observation adapter, reused unchanged) plus a supplied set of admitted member roots. The security test suite
materializes the tree under a scratch directory, walks it natively with those member roots and hands the scope to the
core (`discovery_walk_tests.rs`). This tool runs B3-b0, the members-and-readers reference (contract successor 168), at
its accepted architecture bytes: its pass two (`_finish`) with the same members, which withholds each member's VCS
evidence and its own `opensip.json` from SLM, binds SX-1 to the member roots and enters members as ordinary directories.
It writes or checks crates/security/src/custody/discovery_member_vectors.json with, per case, the downward population
(the reference's, with each member's own VCS evidence and root `opensip.json` restored, because the native walk observes
both before entering it), the version-3 records without `workspaceDeclarations` (B3-b2b's readers write them; member
roots are listed by path) and, when accepted, the boundary inventory. `scanCases` (LD-B3B2A-6) are the same records
over synthetic observed scopes in the scan-vector format (`discovery_scan_tests.rs`), built with B2-b0's checker
helpers, for what a scratch tree cannot hold (an unreadable ACL). The readers, placement and item 6b are not
exercised here: the member set is supplied, as B3-b2a's core receives it. No filesystem tree, network or environment
input.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import importlib.util
import json
import sys

OUTPUT = 'crates/security/src/custody/discovery_member_vectors.json'
WALK_TOOL = 'tools/security/discovery_walk_vectors.py'
REF = 'docs/implementation/m3/config-discovery-b/b3-b-reference/reference/member_reader_reference.py'
B2B0 = 'docs/implementation/m3/config-discovery-b/b2-b-reference/reference/discovery_scan_reference.py'
CHECK = 'docs/implementation/m3/config-discovery-b/b2-b-reference/evidence/check.py'
SCAN_UPWARD = ('mode', 'configPath', 'walked', 'stopReason', 'vcs', 'explicitPathWasSymlink')
READERS = ('cargo-config-patch', 'npm-workspaces-members')


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def cases(w):
    """Tree descriptions (the walk tool's builders) with their admitted members."""
    d, f, tree = w.d, w.f, w.tree
    out = []

    def case(id_, entries, members, source='automatic', roots=()):
        c = w.case(id_, entries, source=source, roots=roots)
        c['members'] = sorted(members)
        out.append(c)

    # Two members entered as ordinary directories: units inside them, each `.git` a vcs-tree row, a member's own
    # opensip.json in memberConfigs (not a nested project), SX-1 at a member root, a nested repository and a nested
    # project inside a member kept as boundaries, Cargo `target` under a member's Cargo root, and a sibling non-member
    # repository as a boundary.
    case('members-automatic', tree(
        dirs_=['m1/.git', 'm1/sub/.git', 'm2/.git', 'other/.git', 'm1/.opensip/cache'],
        files=['package.json', 'm1/package.json', 'm1/opensip.json', 'm1/sub/package.json', 'm1/.opensip/cache/package.json',
               'm1/inner/opensip.json', 'm1/inner/package.json', 'm1/pkg/tsconfig.json', 'm2/Cargo.toml', 'm2/target/t/Cargo.toml',
               'm2/crates/c/Cargo.toml', 'other/package.json']), ['m1', 'm2'])
    # A member below an intermediate directory, and one at depth two.
    case('member-nested-path', tree(dirs_=['repos/a/.git', 'repos/b/.git'], files=['repos/a/package.json', 'repos/b/Cargo.toml', 'repos/README']),
         ['repos/a', 'repos/b'])
    # Exact roots inside members (config roots and --workspace-root): only the named roots are units; a sibling
    # repository is never observed.
    for source in ('config-workspace-roots', 'explicit-joins'):
        case('members-exact-roots-' + source, tree(dirs_=['m1/.git', 'm2/.git', 'other/.git'],
             files=['m1/pkg/package.json', 'm1/other/package.json', 'm2/package.json', 'other/package.json']),
             ['m1', 'm2'], source=source, roots=['m1/pkg', 'm2'])
        # A root inside a nested repository of a member is still a crossing.
        case('member-root-in-nested-repository-' + source, tree(dirs_=['m1/.git', 'm1/inner/.git'], files=['m1/inner/package.json']),
             ['m1'], source=source, roots=['m1/inner'])
        # A root at the member itself.
        case('member-root-at-member-' + source, tree(dirs_=['m1/.git'], files=['m1/Cargo.toml', 'm1/opensip.json']),
             ['m1'], source=source, roots=['m1'])
    # An exact root below a member's SX-1 anchor: the probe chain refuses at `m1/.opensip`, never opening it.
    for source in ('config-workspace-roots', 'explicit-joins'):
        case('member-root-below-member-anchor-' + source, tree(dirs_=['m1/.git', 'm1/.opensip/p'], files=['m1/.opensip/p/package.json']),
             ['m1'], source=source, roots=['m1/.opensip/p'])
    # A member whose directory fails custody: the core excludes the units below it (the member is still not a boundary).
    case('member-directory-custody', tree(dirs_=['m3/.git'], files=['m3/package.json'], extra=[d('m3', mode='0777')]), ['m3'])
    # No member among repositories: identical to B2-b0's walk (the control for the member plumbing).
    case('no-member-control', tree(dirs_=['r/.git'], files=['package.json', 'r/package.json']), [])
    ids = [c['id'] for c in out]
    require(len(ids) == len(set(ids)), 'duplicate case id')
    return out


def member_records(ctx, ref, inp, members):
    """B3-b0's pass two with `members` over SLM input `inp`: pass one's provenance, the population the native walk
    observes, and the expected records and inventory."""
    first = ctx.slm.discovery(copy.deepcopy(inp))
    prov = first['provenance']
    root, source = prov['selectedRoot'], prov['unitSource']
    rows = {r: dict(readerId=r, readerVersion=1, state='absent', path=None, contentSha256=None, stateSubject=None, unresolved=[]) for r in READERS}
    result, _links = ref._finish(ctx, inp, inp, first, members, {}, rows, {r: [] for r in READERS}, [])
    # The population the native walk observes: B3-b0's member-aware population, plus what the walker observes of each
    # member before entering it (its own VCS evidence and its root opensip.json).
    hidden = copy.deepcopy(inp)
    for m in members:
        R = root + '/' + m
        hidden['fs'][R] = {k: v for k, v in hidden['fs'][R].items() if k != 'vcs'}
        hidden['fs'].pop(R + '/opensip.json', None)
    downward = ctx.b2b0.walker_population(ref._PopulationRule(ctx.rule, members), hidden, root, source)
    for m in members:
        R = root + '/' + m
        if R in downward['fs'] and 'vcs' in inp['fs'][R]:
            downward['fs'][R] = dict(downward['fs'][R], vcs=inp['fs'][R]['vcs'])
        if R in downward['fs'] and (R + '/opensip.json') in inp['fs']:
            downward['fs'][R + '/opensip.json'] = inp['fs'][R + '/opensip.json']
    expected = copy.deepcopy(result)
    eprov = expected['provenance']
    eprov['memberRepositories'] = [row['path'] for row in eprov['memberRepositories']]
    del eprov['workspaceDeclarations']
    inventory = ref.boundary_inventory_v3(ctx, result) if result['status'] == 'ACCEPT' else None
    return prov, downward, expected, inventory


def vector(ctx, ref, w, c):
    inp = w.slm_input(ctx.slm, c)
    prov, downward, expected, inventory = member_records(ctx, ref, inp, c['members'])
    require(prov['selectedRoot'] == w.ROOT and prov['unitSource'] == c['source'], 'selection or source differs: ' + c['id'])
    return dict(id=c['id'], tree=c['tree'], source=c['source'], roots=c['roots'], waive=c['waive'], foreign=c['foreign'], groups=c['groups'],
                members=c['members'], upward={k: prov[k] for k in w.UPWARD}, population=w.population(downward), expected=expected, inventory=inventory)


def scan_cases(chk):
    """Synthetic SLM inputs (B2-b0's checker helpers) with admitted members, for observations a scratch tree cannot hold."""
    tree, inp = chk.tree, chk.inp
    out = []
    for basis in ('observed-inventory', 'not-enumerated'):
        # An unreadable SX-1 anchor at a member root: the core counts no markers below it (`unreadable_anchors`).
        fs = tree(dirs=['m1/.opensip/x'], files=['m1/package.json', 'm1/.opensip/x/package.json'], vcs=['m1'])
        fs['/h/w/m1/.opensip']['aclUnreadable'] = True
        out.append(('scan-member-anchor-unreadable-' + basis, inp(fs, prunedTreeMarkerInventory=basis), ['m1']))
        # The same anchor readable: its markers are counted under the observed inventory.
        fs = tree(dirs=['m1/.opensip/x'], files=['m1/package.json', 'm1/.opensip/x/package.json'], vcs=['m1'])
        out.append(('scan-member-anchor-readable-' + basis, inp(fs, prunedTreeMarkerInventory=basis), ['m1']))
    return out


def scan_vector(ctx, ref, id_, inp, members):
    prov, downward, expected, inventory = member_records(ctx, ref, inp, members)
    source = prov['unitSource']
    roots = inp.get('explicitJoins') if source == 'explicit-joins' else inp.get('configWorkspaceRoots') if source == 'config-workspace-roots' else []
    return dict(id=id_,
                input=dict(uid=inp['invokingUid'], ci=bool(inp.get('ci', False)), groups=sorted(inp.get('authorizedGroupIds', [])),
                           waive=bool(inp.get('trustProjectOwner', False)), explicitProject=inp.get('explicitProject'),
                           basis=inp.get('prunedTreeMarkerInventory', 'observed-inventory'), source=source, roots=roots or [],
                           root=prov['selectedRoot'], upward={k: prov[k] for k in SCAN_UPWARD}, scope=downward['fs'], members=members),
                expected=expected, inventory=inventory)


def vectors(arch, product, packages_root):
    w = load('discovery_walk_vectors', product / WALK_TOOL)
    w.packages(product, packages_root)
    ref = load('member_reader_reference', arch / REF)
    ctx = ref.Context(arch)
    chk = load('discovery_scan_reference_check', arch / CHECK)
    pins = [dict(path=p, bytes=len((arch / p).read_bytes()), sha256=hashlib.sha256((arch / p).read_bytes()).hexdigest()) for p in (REF, B2B0, CHECK)]
    body = {'schemaVersion': 1,
            'standing': 'B3-b0 members-and-readers reference vectors for the S3 downward walk and core with supplied D15 members (M3-B r9 '
                        'item 22; unit B3-b2a). Generated by tools/security/discovery_member_vectors.py over the walk-vector tree format; '
                        'design reference results, not product qualification.',
            'sources': pins,
            'cases': [vector(ctx, ref, w, c) for c in cases(w)],
            'scanCases': [scan_vector(ctx, ref, i, inp, m) for i, inp, m in scan_cases(chk)]}
    return (json.dumps(body, separators=(',', ':'), ensure_ascii=True) + '\n').encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true', help='compare the output without writing repository files')
    mode.add_argument('--write', action='store_true', help='regenerate the output')
    parser.add_argument('--architecture', type=Path, required=True)
    parser.add_argument('--packages-root', type=Path, required=True)
    args = parser.parse_args()
    product = Path(__file__).resolve().parent.parent.parent
    raw = vectors(args.architecture.resolve(strict=True), product, args.packages_root.resolve(strict=True))
    target = product / OUTPUT
    if args.check:
        require(target.is_file() and target.read_bytes() == raw, 'vectors differ: ' + OUTPUT)
    else:
        target.write_bytes(raw)
    print(('Verified ' if args.check else 'Generated ') + OUTPUT + ' from the B3-b0 reference at its accepted bytes.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f'Discovery member vector generation failed: {error}', file=sys.stderr)
        raise SystemExit(1)
