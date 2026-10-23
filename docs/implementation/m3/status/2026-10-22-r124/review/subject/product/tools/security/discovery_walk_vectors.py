"""Cross-implementation vectors for the S3 downward walker (M3-B r5 items 12 and 13; unit B2-b3b).

Developer tool only. Each case is a tree description under a selected root that the security test suite materializes
under a scratch directory, walks natively and hands to B2-b2's core (`discovery_walk_tests.rs`). This tool turns the
same description into SLM's synthetic `fs` and runs B2-b0, the current discovery reference (contract successor 164),
at its accepted architecture bytes: `current` selects the root (an explicit `--project`), restricts `fs` to the walker
population and runs `finish`. It writes or checks crates/security/src/custody/discovery_walk_vectors.json with, per
case, the reference's downward population (paths, kinds, custody fields, and VCS evidence on probed directories),
the version-3 result (workspaceDeclarations pending) and, when accepted, the boundary inventory (B2-b3 plan r2
section 3, the oracle cross-check).

The description-to-`fs` mapping is the observation adapter, and the only place this tool decides anything:
  * The selected root is `/h/w` under the account home `/h`. The invoking user is 1000; every entry is owned by
    1000, or by 1001 when the case is `foreign` (the native test then walks as another uid). Every entry's group is
    50, the scratch tree's own; `groups` authorizes 50 (`own`) or 60 (`other`).
  * An ACL write grant (`acl`) to another user is `uid:1001`; to another group, `group:70`.
  * A directory's `vcs` is the first present of `.git`, `.hg`, `.svn` and `.jj`: a directory is `true`; a regular
    `.git` file is an indirection whose target is its one `gitdir:` line when the bound model's `_file_custody`
    admits it (never waived), and null otherwise; any other marker is an indirection with a null target.
  * The production walker never enumerates inside a pruned tree, so the marker-count basis is `not-enumerated`.
No case needs an unreadable ACL, a foreign owner beside an owned one, or a mount: a scratch tree cannot hold them,
and they stay with B2-b2's pure-core vectors. SLM imports canonical.py, which imports jsonschema; the tool loads the
provisioned snapshot only after every file matches its generator-closure pin. No filesystem tree, network or
environment input.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import importlib.util
import json
import sys

OUTPUT = 'crates/security/src/custody/discovery_walk_vectors.json'
REF = 'docs/implementation/m3/config-discovery-b/b2-b-reference/'
# Architecture inputs (contract successor 164 and its parents): path, bytes, SHA-256.
ARCH = (
    (REF + 'reference/discovery_scan_reference.py', 12574, '6714575ccee1474e2d7c20c4e5e9b6c95b498ad155ec1e69fc9d6ba5f3e7e32b'),
)
UPWARD = ('mode', 'configPath', 'walked', 'stopReason', 'vcs', 'explicitPathWasSymlink')
HOME = '/h'
ROOT = '/h/w'
MARKERS = ('.git', '.hg', '.svn', '.jj')


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


def d(rel, mode='0755', **opts):
    return dict(kind='dir', path=rel, mode=mode, **opts)


def f(rel, mode='0644', text='{}', **opts):
    return dict(kind='file', path=rel, mode=mode, text=text, **opts)


def link(rel, target):
    return dict(kind='symlink', path=rel, target=target)


def fifo(rel):
    return dict(kind='fifo', path=rel, mode='0644')


def sock(rel):
    return dict(kind='socket', path=rel)


def dirs(rel):
    """Every directory on `rel`, parent-first."""
    parts = rel.split('/')
    return [d('/'.join(parts[:i])) for i in range(1, len(parts) + 1)]


def tree(dirs_=(), files=(), extra=()):
    """A description, parents first: `dirs_` and the parents of every file, the files, then `extra` entries, each
    replacing an implicit entry of the same path in place (so a parent stays before its children)."""
    out, index = [], {}

    def add(e):
        if e['path'] in index:
            out[index[e['path']]] = e
        else:
            index[e['path']] = len(out)
            out.append(e)

    def parents(rel):
        if '/' in rel:
            for p in dirs(rel.rsplit('/', 1)[0]):
                if p['path'] not in index:
                    add(p)

    for rel in dirs_:
        for p in dirs(rel):
            if p['path'] not in index:
                add(p)
    for x in files:
        parents(x)
        add(f(x))
    for e in extra:
        parents(e['path'])
        add(e)
    return out


def case(id_, entries, source='automatic', roots=(), waive=False, foreign=False, groups=None):
    return dict(id=id_, tree=entries, source=source, roots=list(roots), waive=waive, foreign=foreign, groups=groups)


def deep(n):
    return '/'.join('d' for _ in range(n))


def cases():
    out = [
        case('units-at-root-and-below', tree(files=['package.json', 'a/package.json', 'b/Cargo.toml', 'b/c/tsconfig.json', 'e/README'])),
        case('empty-root', []),
        case('pruned-anchors-all-four', tree(files=['Cargo.toml', 'node_modules/x/package.json', 'target/x/package.json', '.opensip/package.json', 'p/package.json'],
                                              extra=[d('.git'), f('.git/HEAD')])),
        case('pruned-anchor-hides-a-repository', tree(files=['package.json', 'node_modules/x/package.json', 'node_modules/x/.git/HEAD'])),
        case('target-without-cargo-is-ordinary', tree(files=['target/u/package.json'])),
        case('nested-repository-is-recorded-and-never-entered', tree(files=['r/package.json', 'r/sub/package.json', 'r/.git/HEAD', 'u/package.json'])),
        case('nested-gitdir-file-repository', tree(files=['u/package.json'], extra=[d('r'), f('r/.git', text='gitdir: /elsewhere/.git/worktrees/r\n'), f('r/package.json')])),
        case('nested-gitdir-file-under-acl-grant-has-no-target', tree(extra=[d('r'), f('r/.git', text='gitdir: /elsewhere\n', acl='user')])),
        case('nested-hg-file-repository', tree(extra=[d('r'), f('r/.hg', text='x')])),
        case('nested-project-is-recorded-and-never-entered', tree(files=['p/opensip.json', 'p/package.json', 'p/q/package.json', 'u/package.json'])),
        case('nested-project-config-directory-is-not-a-project', tree(files=['p/package.json'], extra=[d('p/opensip.json')])),
        case('opensip-directory-at-the-root', tree(files=['package.json', '.opensip/local.json', '.opensip/sub/package.json'])),
        case('opensip-file-at-the-root', tree(files=['package.json', '.opensip'])),
        case('depth-256-unit', tree(files=[deep(256) + '/package.json'])),
        case('depth-257-unit-and-hidden-repository', tree(files=[deep(256) + '/package.json', deep(257) + '/package.json', deep(257) + '/.git/HEAD', deep(257) + '/opensip.json'])),
        case('explicit-joins', tree(files=['a/u/package.json', 'b/package.json']), source='explicit-joins', roots=['a/u']),
        case('config-roots', tree(files=['a/u/package.json', 'b/package.json']), source='config-workspace-roots', roots=['a/u', '.']),
        case('explicit-join-without-marker', tree(dirs_=['a/u'], files=['b/package.json']), source='explicit-joins', roots=['a/u']),
        case('explicit-join-cargo-target', tree(files=['Cargo.toml', 'target/u/package.json']), source='explicit-joins', roots=['target/u']),
        case('config-root-cargo-target', tree(files=['Cargo.toml', 'target/u/package.json']), source='config-workspace-roots', roots=['target/u']),
        case('explicit-join-crosses-a-nested-repository', tree(files=['r/.git/HEAD', 'r/x/package.json']), source='explicit-joins', roots=['r/x']),
        case('explicit-join-crosses-a-nested-project', tree(files=['p/opensip.json', 'p/x/package.json']), source='explicit-joins', roots=['p/x']),
        case('explicit-join-absent', tree(files=['a/package.json']), source='explicit-joins', roots=['a/missing']),
        case('explicit-join-is-a-file', tree(files=['a/package.json']), source='explicit-joins', roots=['a/package.json']),
        case('explicit-join-grammar', tree(files=['a/package.json']), source='explicit-joins', roots=['../x']),
        case('explicit-join-inside-node-modules', tree(files=['node_modules/x/package.json']), source='explicit-joins', roots=['node_modules/x']),
        case('explicit-join-beside-a-large-sibling', tree(files=['a/u/package.json'] + ['big/s%d/package.json' % i for i in range(40)]), source='explicit-joins', roots=['a/u']),
        # r3 (Codex B2B3B-R2-RF-1): a pruned prefix that is a file, or absent, still refuses the join before custody.
        case('explicit-join-under-a-node-modules-file', tree(files=['a/node_modules']), source='explicit-joins', roots=['a/node_modules/x']),
        case('config-root-under-a-node-modules-file', tree(files=['a/node_modules']), source='config-workspace-roots', roots=['a/node_modules/x']),
        case('explicit-join-under-an-absent-node-modules', tree(dirs_=['a']), source='explicit-joins', roots=['a/node_modules/x']),
        case('config-root-under-an-absent-node-modules', tree(dirs_=['a']), source='config-workspace-roots', roots=['a/node_modules/x']),
        # r3 (Codex B2B3B-R2-RF-3): the depth policy applies to a named root itself.
        case('explicit-join-at-depth-256', tree(files=[deep(256) + '/package.json', deep(256) + '/unlisted.txt']), source='explicit-joins', roots=[deep(256)]),
        case('explicit-join-at-depth-257', tree(files=[deep(257) + '/package.json', deep(257) + '/unlisted.txt']), source='explicit-joins', roots=[deep(257)]),
        case('config-root-at-depth-257', tree(files=[deep(257) + '/package.json', deep(257) + '/unlisted.txt']), source='config-workspace-roots', roots=[deep(257)]),
        case('explicit-join-at-depth-260', tree(files=[deep(260) + '/package.json', deep(260) + '/unlisted.txt', deep(260) + '/sub/package.json']), source='explicit-joins', roots=[deep(260)]),
        # Metadata-only marker rejection (r2, B2B3PLAN-2): never opened.
        case('fifo-marker-alone', tree(dirs_=['u'], extra=[fifo('u/package.json')])),
        case('fifo-marker-beside-a-valid-marker', tree(files=['u/package.json'], extra=[fifo('u/Cargo.toml')])),
        case('socket-marker-beside-a-valid-marker', tree(files=['u/package.json'], extra=[sock('u/tsconfig.json')])),
        case('symlink-marker-beside-a-valid-marker', tree(files=['u/package.json'], extra=[link('u/jsconfig.json', '/etc/hosts')])),
        case('symlink-marker-alone', tree(dirs_=['u'], extra=[link('u/package.json', '/etc/hosts')])),
        case('fifo-marker-on-an-explicit-join', tree(files=['u/package.json'], extra=[fifo('u/Cargo.toml')]), source='explicit-joins', roots=['u']),
        # Custody failures on the tree.
        case('unit-directory-writable-by-others', tree(files=['u/package.json'], extra=[d('u', '0777')])),
        case('unit-chain-directory-writable-by-group', tree(files=['a/u/package.json'], extra=[d('a', '0775')])),
        case('unit-chain-group-write-authorized', tree(files=['a/u/package.json'], extra=[d('a', '0775')]), groups='own'),
        case('unit-chain-acl-grant', tree(files=['a/u/package.json'], extra=[d('a', acl='user')])),
        case('marker-writable-by-others', tree(files=['u/Cargo.toml'], extra=[f('u/package.json', '0666')])),
        case('marker-acl-grant-to-a-group', tree(files=['u/Cargo.toml'], extra=[f('u/package.json', acl='group')])),
        case('marker-hard-linked', tree(files=['u/Cargo.toml'], extra=[f('u/package.json', hardlink=True)])),
        case('marker-acl-before-hard-link', tree(extra=[d('u'), f('u/package.json', acl='user', hardlink=True)])),
        case('explicit-join-chain-writable-by-others', tree(files=['a/u/package.json'], extra=[d('a', '0777')]), source='explicit-joins', roots=['a/u']),
        case('root-as-an-explicit-unit', tree(files=['package.json', 'a/package.json']), source='explicit-joins', roots=['.']),
        # The typed owner waiver (plan r4 LD-B2B-9): the chain, never a marker.
        case('waiver-reaches-the-explicit-chain-and-never-a-marker', tree(files=['a/u/package.json']), source='explicit-joins', roots=['a/u'], waive=True, foreign=True),
    ]
    ids = [c['id'] for c in out]
    require(len(ids) == len(set(ids)), 'duplicate case id')
    return out


def gitdir_value(text):
    """One `gitdir:` line with an optional LF or CRLF end, else null (B2-b3a)."""
    if not text.startswith('gitdir: '):
        return None
    value = text[len('gitdir: '):]
    value = value[:-2] if value.endswith('\r\n') else value[:-1] if value.endswith('\n') else value
    return value if value and not any(c in value for c in '\n\r\0') else None


def slm_input(slm, c):
    owner = 1001 if c['foreign'] else 1000
    groups = [50 if c['groups'] == 'own' else 60] if c['groups'] else []
    kinds = {e['path']: e for e in c['tree']}
    fs = {'/': dict(kind='dir', uid=0, gid=0, mode='0755', dev=1), HOME: dict(kind='dir', uid=1000, gid=50, mode='0700', dev=1),
          ROOT: dict(kind='dir', uid=owner, gid=50, mode='0755', dev=1)}
    for e in c['tree']:
        row = dict(kind=e['kind'], uid=owner, gid=50, mode=e.get('mode', '0777'), dev=1)
        if e['kind'] == 'file':
            row['nlink'] = 2 if e.get('hardlink') else 1
            row['size'] = len(e['text'].encode())
        if e.get('acl'):
            row['aclWrite'] = ['uid:1001' if e['acl'] == 'user' else 'group:70']
        fs[ROOT + '/' + e['path']] = row
    for rel, e in [('', None)] + list(kinds.items()):
        if e is not None and e['kind'] != 'dir':
            continue
        for marker in MARKERS:
            m = kinds.get((rel + '/' if rel else '') + marker)
            if m is None:
                continue
            if m['kind'] == 'dir':
                vcs = True
            elif m['kind'] == 'file' and marker == '.git':
                admitted = slm._file_custody(fs[ROOT + '/' + m['path']], 1000, False, set(groups)) is None
                vcs = dict(kind='indirection', target=gitdir_value(m.get('text', '')) if admitted else None)
            else:
                vcs = dict(kind='indirection', target=None)
            fs[ROOT + ('/' + rel if rel else '')]['vcs'] = vcs
            break
    inp = dict(invokingUid=1000, accountHome=HOME, cwd=HOME, fs=fs, explicitProject=ROOT, prunedTreeMarkerInventory='not-enumerated')
    if c['waive']:
        inp['trustProjectOwner'] = True
    if groups:
        inp['authorizedGroupIds'] = groups
    if c['source'] == 'explicit-joins':
        inp['explicitJoins'] = c['roots']
    elif c['source'] == 'config-workspace-roots':
        inp['configWorkspaceRoots'] = c['roots']
    return inp


def population(downward):
    """The reference's downward population at or below the root, with the custody fields the native walk compares."""
    out = {}
    for p, e in sorted(downward['fs'].items()):
        if p != ROOT and not p.startswith(ROOT + '/'):
            continue
        row = {k: e[k] for k in ('kind', 'uid', 'mode', 'nlink', 'size', 'aclWrite') if k in e}
        if 'vcs' in e:
            v = e['vcs']
            row['vcs'] = dict(kind='directory', target=None) if v is True else dict(kind=v['kind'], target=v.get('target'))
        out[p] = row
    return out


def vector(ref, slm, rule, c):
    inp = slm_input(slm, c)
    cur, downward, _second = ref.current(slm, rule, copy.deepcopy(inp))
    require(downward is not None, 'selection refused: ' + c['id'])
    prov = cur['provenance']
    require(prov['selectedRoot'] == ROOT and prov['unitSource'] == c['source'], 'selection or source differs: ' + c['id'])
    partial = ref.project_v3(cur)
    expected = {k: v for k, v in partial.items() if k != 'pendingFields'}
    inventory = ref.boundary_inventory_v3(rule, partial) if partial['status'] == 'ACCEPT' else None
    return dict(id=c['id'], tree=c['tree'], source=c['source'], roots=c['roots'], waive=c['waive'], foreign=c['foreign'], groups=c['groups'],
                upward={k: prov[k] for k in UPWARD}, population=population(downward), expected=expected, inventory=inventory)


def vectors(arch, product, packages_root):
    packages(product, packages_root)
    for row in ARCH:
        pinned(arch, *row)
    ref = load('discovery_scan_reference', arch / ARCH[0][0])
    slm, rule = ref.load(arch)
    body = {'schemaVersion': 1,
            'standing': 'B2-b0 current-reference vectors for the S3 downward walker (M3-B r5 items 12 and 13; unit B2-b3b). Generated by '
                        'tools/security/discovery_walk_vectors.py at the reference\'s accepted bytes over tree descriptions the security tests '
                        'build natively; design reference results, not product qualification.',
            'sources': [dict(path=p, bytes=n, sha256=h) for p, n, h in ARCH],
            'cases': [vector(ref, slm, rule, c) for c in cases()]}
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
        print(f'Discovery walk vector generation failed: {error}', file=sys.stderr)
        raise SystemExit(1)
