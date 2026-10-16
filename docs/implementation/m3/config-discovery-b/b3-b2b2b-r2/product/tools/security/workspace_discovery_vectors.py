"""Cross-implementation vectors for the D15 discovery composition (M3-B r9 items 19 to 24; unit B3-b2b2b, B3-b plan r2
amendment A3).

Developer tool only. Each case is a walk-vector tree description (tools/security/discovery_walk_vectors.py's format,
its builders and SLM adapter reused unchanged) with reader carriers and provider manifests as file texts, plus the
members the security test makes real Git repositories (`gitMembers`, by `git init`; `gitConfig` sets one key in one,
whose item-6b verdict the case states as `memberObservations`), whether W itself is a repository (`wRepository`), the
index gitlinks the test writes into a member's index at a populated directory with no VCS marker (`gitlinks`, r2, Codex
B3B2B2B-R1-RF-1; B3-b0 has no index, so its input states each as that directory's VCS evidence, the nested repository
item 21 makes it), and a file padded past its text (`padTo`, spaces after the JSON).
This tool runs B3-b0, the members-and-readers reference (contract successor 168), at its bound bytes: `discover` over
the adapter's SLM input with the texts as its `contents` side table. It writes or checks
crates/security/src/custody/workspace_discovery_vectors.json with each case's complete `DiscoveryResultV3` and its link
rows, which the security test compares with `discover_with_members` over the materialized tree, spelled under `/h/w`,
and the reference's access record (every W-relative path its reader code looked up, read or listed, recorded by
tools/security/workspace_member_vectors.py's recorder), which bounds the native observation's.
No filesystem tree, network or environment input.
"""
from pathlib import Path
import argparse
import copy
import hashlib
import importlib.util
import json
import sys

OUTPUT = 'crates/security/src/custody/workspace_discovery_vectors.json'
WALK_TOOL = 'tools/security/discovery_walk_vectors.py'
MEMBER_TOOL = 'tools/security/workspace_member_vectors.py'
REF = 'docs/implementation/m3/config-discovery-b/b3-b-reference/reference/member_reader_reference.py'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def cases(w):
    d, f, tree = w.d, w.f, w.tree
    out = []

    def case(id_, entries, members=(), config=None, w_repository=False, source='automatic', roots=(), gitlinks=()):
        c = w.case(id_, entries, source=source, roots=roots)
        c['gitMembers'] = sorted(members)
        c['gitConfig'] = config
        c['wRepository'] = w_repository
        c['gitlinks'] = [dict(member=m, path=g) for m, g in gitlinks]
        out.append(c)

    crate = lambda rel, name, version='1.0.0': f(rel + '/Cargo.toml', text='[package]\nname = "%s"\nversion = "%s"\n' % (name, version))
    npm = lambda rel, name, version='1.0.0': f(rel + '/package.json', text=json.dumps({'name': name, 'version': version}))
    cargo_config = lambda patches: f('.cargo/config.toml', text='[patch.crates-io]\n' + ''.join('%s = { path = "%s" }\n' % p for p in patches))
    workspaces = lambda entries: f('package.json', text=json.dumps({'private': True, 'workspaces': entries}))

    # Branch B, Cargo: two members declared by the patch carrier, linked; the members' units discovered inside them.
    case('b-cargo-two-members', tree(dirs_=['repos/a/.git', 'repos/b/.git'],
         extra=[crate('repos/a/crates/a', 'a'), crate('repos/b', 'b', '2.0.0'), cargo_config([('a', 'repos/a/crates/a'), ('b', 'repos/b')])]),
         members=['repos/a', 'repos/b'])
    # Branch B, npm: literal entries declare; a glob crossing a visible repository is disclosed; a W-own glob is not.
    case('b-npm-literal-and-globs', tree(dirs_=['repos/x/.git', 'repos/y/.git', 'packages/p'],
         extra=[npm('repos/x', 'x'), npm('repos/y/pkg', '@s/y', '3.1.0'), npm('packages/p', 'p'),
                workspaces(['repos/x', 'repos/y/pkg', 'repos/*', 'packages/*'])]),
         members=['repos/x', 'repos/y'])
    # Branch B: candidates excluded by placement (another VCS marker) and by item 6b (an include in its config).
    case('b-candidates-excluded', tree(dirs_=['repos/h/.git', 'repos/h/.hg', 'repos/s/.git'],
         extra=[npm('repos/h', 'h'), npm('repos/s', 's'), workspaces(['repos/h', 'repos/s'])]),
         members=['repos/h', 'repos/s'], config=dict(member='repos/s', key='include.path', value='/elsewhere', subject='member-vcs-unsupported:config-include'))
    # Branch B: one member's own opensip.json, its nested repository and SX-1 at its root.
    case('b-member-contents', tree(dirs_=['repos/a/.git', 'repos/a/vendor/sub/.git', 'repos/a/.opensip/cache'],
         extra=[npm('repos/a', 'a'), f('repos/a/opensip.json', text='{}'), npm('repos/a/vendor/sub', 'sub'), npm('repos/a/.opensip/cache', 'hidden'),
                workspaces(['repos/a', 'repos/a/vendor/sub'])]),
         members=['repos/a', 'repos/a/vendor/sub'])
    # The cap: 65 placed candidates refuse PROJECT.SCOPE_LIMIT before item 6b.
    many = ['m%02d' % i for i in range(65)]
    case('b-cap-65', tree(dirs_=[m + '/.git' for m in many], extra=[npm(m, 'p' + m) for m in many] + [workspaces(many)]), members=[])
    # Root in a repository: the readers declare nothing; a literal entry inside a nested repository is disclosed.
    case('w-in-repository', tree(dirs_=['.git', 'repos/x/.git'], extra=[npm('repos/x', 'x'), workspaces(['repos/x'])]),
         members=['repos/x'], w_repository=True)
    # Custody: a group-writable carrier and an ACL-granted carrier are refused as data; a world-writable member
    # directory is excluded with its directory custody.
    case('b-carrier-group-writable', tree(dirs_=['repos/x/.git'], extra=[npm('repos/x', 'x'), dict(workspaces(['repos/x']), mode='0664')]),
         members=['repos/x'])
    case('b-carrier-acl-grant', tree(dirs_=['repos/x/.git'], extra=[npm('repos/x', 'x'), dict(workspaces(['repos/x']), acl='user')]),
         members=['repos/x'])
    case('b-member-directory-custody', tree(dirs_=['repos/c/.git'], extra=[d('repos/c', mode='0777'), npm('repos/c', 'c'), workspaces(['repos/c'])]),
         members=['repos/c'])
    # r2 (Codex B3B2B2B-R1-RF-1): a member's index gitlink at a populated directory with no VCS marker is a nested
    # repository: never entered, no unit below it, an entry inside it declares and links nothing.
    case('b-member-index-gitlink', tree(dirs_=['repos/a/.git', 'repos/a/sub/src'],
         extra=[npm('repos/a', 'a'), npm('repos/a/sub', 'inner'), crate('repos/a/sub/src', 'deep'), workspaces(['repos/a', 'repos/a/sub'])]),
         members=['repos/a'], gitlinks=[('repos/a', 'sub')])
    # An oversize carrier: custody refuses it by its size, before any read; discovery completes.
    case('b-carrier-oversize', tree(dirs_=['repos/x/.git'], extra=[npm('repos/x', 'x'), dict(workspaces(['repos/x']), padTo=4 * 1024 * 1024 + 1)]),
         members=['repos/x'])
    # Branch A: the workspace-roots array decides; readers link only into its members.
    for source in ('config-workspace-roots', 'explicit-joins'):
        case('a-roots-' + source, tree(dirs_=['repos/a/.git', 'repos/b/.git'],
             extra=[crate('repos/a/crates/a', 'a'), crate('repos/b', 'b'), cargo_config([('a', 'repos/a/crates/a'), ('b', 'repos/b')])]),
             members=['repos/a', 'repos/b'], source=source, roots=['repos/a/crates/a'])
        # Branch A: placement refuses (a .git file), after the trial walk accepts.
        case('a-layout-refuses-' + source, tree(dirs_=['repos/f'], extra=[f('repos/f/.git', text='gitdir: /elsewhere\n'), crate('repos/f', 'f')]),
             source=source, roots=['repos/f'])
        # Branch A: item 6b refuses.
        case('a-6b-refuses-' + source, tree(dirs_=['repos/s/.git'], extra=[crate('repos/s', 's')]), members=['repos/s'],
             config=dict(member='repos/s', key='include.path', value='/elsewhere', subject='member-vcs-unsupported:config-include'),
             source=source, roots=['repos/s'])
        # Branch A: the trial walk refuses after it recorded the provisional member (a root inside the member's
        # nested repository): the refusal record carries no member.
        case('a-trial-refuses-crossing-' + source, tree(dirs_=['repos/a/.git', 'repos/a/inner/.git'], extra=[crate('repos/a/inner', 'i')]),
             members=['repos/a', 'repos/a/inner'], source=source, roots=['repos/a/inner'])
        # r2 (RF-1): branch A with a member's index gitlink. A root crossing it refuses as the trial would; a root
        # beside it is accepted, the walk never entering the gitlink.
        case('a-root-crosses-index-gitlink-' + source, tree(dirs_=['repos/a/.git', 'repos/a/sub/x'], extra=[crate('repos/a/sub/x', 'x')]),
             members=['repos/a'], gitlinks=[('repos/a', 'sub')], source=source, roots=['repos/a/sub/x'])
        case('a-root-beside-index-gitlink-' + source, tree(dirs_=['repos/a/.git', 'repos/a/vendor/lib'],
             extra=[crate('repos/a/crates/a', 'a'), crate('repos/a/vendor/lib', 'lib')]),
             members=['repos/a'], gitlinks=[('repos/a', 'vendor/lib')], source=source, roots=['repos/a/crates/a'])
        # Branch A: the trial walk refuses (an absent root).
        case('a-trial-refuses-' + source, tree(dirs_=['repos/a/.git'], extra=[crate('repos/a', 'a')]), members=['repos/a'],
             source=source, roots=['repos/a', 'missing'])
    ids = [c['id'] for c in out]
    require(len(ids) == len(set(ids)), 'duplicate case id')
    return out


def vector(w, ref, ctx, m, c):
    inp = w.slm_input(ctx.slm, c)
    padded = lambda e: e['text'] + ' ' * max(0, e.get('padTo', 0) - len(e['text'].encode()))
    inp['contents'] = {w.ROOT + '/' + e['path']: padded(e) for e in c['tree'] if e['kind'] == 'file'}
    for e in c['tree']:
        if e.get('padTo'):
            inp['fs'][w.ROOT + '/' + e['path']]['size'] = len(padded(e).encode())
    for g in c['gitlinks']:
        d = w.ROOT + '/' + g['member'] + '/' + g['path']
        require(inp['fs'].get(d, {}).get('kind') == 'dir', 'a gitlink names no directory: ' + c['id'])
        inp['fs'][d] = dict(inp['fs'][d], vcs=True)
    # Every VCS marker each directory holds, as B3-b0's `vcsMarkers` side table states it (one VCS representation, its
    # r2 RF-3): the adapter's SLM input records only the first.
    kinds = {e['path']: e['kind'] for e in c['tree']}
    held = {}
    for path in kinds:
        parent, _, name = path.rpartition('/')
        if name in w.MARKERS:
            held.setdefault(parent, []).append(name)
    inp['vcsMarkers'] = {w.ROOT + ('/' + d if d else ''): [m for m in w.MARKERS if m in names] for d, names in held.items()}
    if c['gitConfig']:
        inp['memberObservations'] = {w.ROOT + '/' + c['gitConfig']['member']: c['gitConfig']['subject']}
    spy = m.SpyContents(inp.get('contents', {}))
    ref.OBSERVED = []
    try:
        with m.Recorder(ref) as rec:
            result, links = ref.discover(ctx, dict(copy.deepcopy(inp), contents=spy))
        observed = list(ref.OBSERVED)
    finally:
        ref.OBSERVED = None
    prov = result['provenance']
    rel = lambda paths: sorted({r for p in paths if (r := m.rel(w.ROOT, p)) is not None}, key=lambda s: s.encode())
    require(prov['selectedRoot'] == w.ROOT, 'selection differs: ' + c['id'])
    return dict(id=c['id'], tree=c['tree'], source=c['source'], roots=c['roots'], gitMembers=c['gitMembers'], gitConfig=c['gitConfig'],
                wRepository=c['wRepository'], gitlinks=c['gitlinks'], upward={k: prov[k] for k in w.UPWARD}, expected=result, links=links,
                consulted=rel(observed), read=rel(spy.asked), listed=rel(rec.listed))


def vectors(arch, product, packages_root):
    w = load('discovery_walk_vectors', product / WALK_TOOL)
    w.packages(product, packages_root)
    m = load('workspace_member_vectors', product / MEMBER_TOOL)
    ref = load('member_reader_reference', arch / REF)
    ctx = ref.Context(arch)
    raw = (arch / REF).read_bytes()
    body = {'schemaVersion': 1,
            'standing': 'B3-b0 members-and-readers reference results for the D15 discovery composition (M3-B r9 items 19 to 24; unit '
                        'B3-b2b2b). Generated by tools/security/workspace_discovery_vectors.py over the walk-vector tree format; design '
                        'reference results, not product qualification.',
            'sources': [dict(path=REF, bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())],
            'cases': [vector(w, ref, ctx, m, c) for c in cases(w)]}
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
    print(('Verified ' if args.check else 'Generated ') + OUTPUT + ' from the B3-b0 reference at its bound bytes.')


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f'Workspace discovery vector generation failed: {error}', file=sys.stderr)
        raise SystemExit(1)
