"""Check B3-b0, the members-and-readers reference (B3-b plan r2 section 1).

Two stages:
  * No-member equality: every discovery case of security/discovery-cases.v1.json runs through the B3-b0 reference and
    through B2-b0 (contract successor 164). Status, refusal, path, detail and every provenance field other than the
    three D15 fields must be equal, and no case may admit a member (none declares one).
  * The D15 cases: synthetic trees with reader carriers, provider manifests and Git members, one or more per registry
    reason and per law item 19 to 24 rule, each with its outcome written here by hand from the law and the registry.
Every result validates as DiscoveryResultV3 and every ACCEPTed result's boundary inventory as
AdmittedBoundaryInventoryV3, in the SLS bundle merged with B-S1's additions. Any exception fails the checker.
Design evidence: supplied synthetic maps only; no filesystem tree, product code or qualification."""
from pathlib import Path
import argparse, copy, hashlib, importlib.util, json, sys

DESIGN = 'docs/coop/design-corrections/'
CASES = DESIGN + 'security/discovery-cases.v1.json'
BUNDLE = (DESIGN + 'security/security-lifecycle.schemas.v1.json', 'f66d2c617084825e3cdb9a855a151c10aa66625968b40ef91fc6bb3be39423f4')
B_S1 = 'docs/implementation/m3/config-discovery-b/b-s1/schemas/security-lifecycle.schemas.v1.b-s1-additions.json'
D15 = ('memberRepositories', 'memberConfigs', 'workspaceDeclarations')
UID = 1000
W = '/h/w'


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path); m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m


# ------------------------------------------------------------------ synthetic trees

class Tree:
    """W = /h/w, selected by its own opensip.json (config mode) unless told otherwise."""

    def __init__(self, w_vcs=False, config=True):
        self.fs = {'/': dict(kind='dir', uid=0, mode='0755', dev=1), '/h': dict(kind='dir', uid=UID, mode='0700', dev=1),
                   W: dict(kind='dir', uid=UID, mode='0755', dev=1)}
        self.contents, self.markers, self.observations = {}, {}, {}
        if w_vcs:
            self.fs[W]['vcs'] = True
            self.dir('.git')
        if config:
            self.file('opensip.json', '{}')

    def dir(self, rel, **kw):
        parts = rel.split('/')
        for i in range(1, len(parts) + 1):
            self.fs.setdefault(W + '/' + '/'.join(parts[:i]), dict(kind='dir', uid=UID, mode='0755', dev=1))
        self.fs[W + '/' + rel].update(kw)
        return self

    def file(self, rel, text=None, **kw):
        if '/' in rel:
            self.dir(rel.rsplit('/', 1)[0])
        self.fs[W + '/' + rel] = dict(dict(kind='file', uid=UID, mode='0644', nlink=1, size=len(text or '') or 10), **kw)
        if text is not None:
            self.contents[W + '/' + rel] = text
        return self

    def repo(self, rel, git_file=False, extra=(), **kw):
        """A Git repository at rel: `.git` as a directory (or a file), plus any extra VCS markers."""
        self.dir(rel, **kw)
        if git_file:
            self.fs[W + '/' + rel]['vcs'] = {'kind': 'indirection', 'target': '/elsewhere'}
            self.file(rel + '/.git', 'gitdir: /elsewhere')
        else:
            self.fs[W + '/' + rel]['vcs'] = True
            self.dir(rel + '/.git')
        for m in extra:
            self.dir(rel + '/' + m)
        if extra:
            self.markers[W + '/' + rel] = ['.git'] + list(extra)
        return self

    def crate(self, rel, name, version='1.0.0'):
        v = ('version = "%s"' % version) if isinstance(version, str) else 'version.workspace = true'
        return self.file(rel + '/Cargo.toml', '[package]\nname = "%s"\n%s\n' % (name, v))

    def npm(self, rel, name, version='1.0.0'):
        doc = {'name': name}
        if version is not None:
            doc['version'] = version
        return self.file(rel + '/package.json', json.dumps(doc))

    def cargo_config(self, patches, rel='.cargo/config.toml', registry='crates-io'):
        body = '[patch.%s]\n' % registry + ''.join('%s = %s\n' % (n, spec) for n, spec in patches)
        return self.file(rel, body)

    def workspaces(self, entries, extra=None):
        doc = {'private': True, 'workspaces': entries}
        doc.update(extra or {})
        return self.file('package.json', json.dumps(doc))

    def input(self, **kw):
        out = dict(invokingUid=UID, accountHome='/h', cwd=W, fs=copy.deepcopy(self.fs), prunedTreeMarkerInventory='not-enumerated',
                   contents=dict(self.contents), vcsMarkers=dict(self.markers), memberObservations=dict(self.observations))
        out.update(kw)
        return out


def path(rel):
    return W + '/' + rel


# ------------------------------------------------------------------ the D15 cases, with hand-written outcomes

def d15_cases():
    """(id, input, expect). expect keys (each optional): status, refusal, detail, members ([rel]), declaredBy ({rel: [source]}),
    unresolved ({reader: [(entry, reason, subject)]}), states ({reader: (state, subject)}), links ([(eco, name, dir)]),
    configs ([rel]), nested ([rel] that must be nestedRepositories), notNested ([rel]), units ([rel] subset), pruned ([(rel, reason)] subset)."""
    C = []

    def case(cid, tree, expect, **kw):
        C.append((cid, tree.input(**kw), expect))

    # --- Branch B, Cargo: two members, links, the member's .git pruned, its units discovered.
    t = Tree().repo('repos/a').crate('repos/a/crates/a', 'a').repo('repos/b').crate('repos/b', 'b', '2.0.0')
    t.cargo_config([('a', '{ path = "repos/a/crates/a" }'), ('b', '{ path = "repos/b" }')])
    case('b-cargo-two-members', t, dict(status='ACCEPT', members=['repos/a', 'repos/b'], declaredBy={'repos/a': ['reader'], 'repos/b': ['reader']},
         unresolved={'cargo-config-patch': [], 'npm-workspaces-members': []}, states={'cargo-config-patch': ('read', None), 'npm-workspaces-members': ('absent', None)},
         links=[('cargo', 'a', 'repos/a/crates/a'), ('cargo', 'b', 'repos/b')], notNested=['repos/a', 'repos/b'],
         units=['repos/a/crates/a', 'repos/b'], pruned=[('repos/a/.git', 'vcs-tree'), ('repos/b/.git', 'vcs-tree')]))
    # Legacy carrier name.
    t = Tree().repo('repos/a').crate('repos/a', 'a')
    t.cargo_config([('a', '{ path = "repos/a" }')], rel='.cargo/config')
    case('b-cargo-legacy-config', t, dict(status='ACCEPT', members=['repos/a'], links=[('cargo', 'a', 'repos/a')]))
    # Both carriers: ambiguous, nothing declared.
    t = Tree().repo('repos/a').crate('repos/a', 'a')
    t.cargo_config([('a', '{ path = "repos/a" }')]); t.cargo_config([('a', '{ path = "repos/a" }')], rel='.cargo/config')
    case('b-cargo-carrier-ambiguous', t, dict(status='ACCEPT', members=[], states={'cargo-config-patch': ('refused', 'carrier-ambiguous')}, nested=['repos/a']))
    # --- Branch B, npm: literal entries, a nested package directory.
    t = Tree().repo('repos/x').npm('repos/x', 'x').repo('repos/y').npm('repos/y/pkg', '@s/y', '3.1.0')
    t.workspaces(['repos/x', 'repos/y/pkg'])
    case('b-npm-literal-members', t, dict(status='ACCEPT', members=['repos/x', 'repos/y'], links=[('npm', '@s/y', 'repos/y/pkg'), ('npm', 'x', 'repos/x')],
         unresolved={'npm-workspaces-members': []}, states={'npm-workspaces-members': ('read', None)}, notNested=['repos/x', 'repos/y']))
    # Globs: one crossing a repository (recorded), one in W's own tree (not recorded); neither declares.
    t = Tree().repo('repos/x').npm('repos/x', 'x').dir('packages/p').npm('packages/p', 'p')
    t.workspaces(['repos/*', 'packages/*'])
    case('b-npm-globs', t, dict(status='ACCEPT', members=[], unresolved={'npm-workspaces-members': [('repos/*', 'workspace-glob-crosses-repository', None)]}, nested=['repos/x']))
    t = Tree().repo('repos/x').npm('repos/x', 'x')
    t.workspaces(['*'])
    case('b-npm-root-glob-crosses', t, dict(status='ACCEPT', members=[], unresolved={'npm-workspaces-members': [('*', 'workspace-glob-crosses-repository', None)]}))
    # Workspaces shape: the object form is refused.
    t = Tree().repo('repos/x').npm('repos/x', 'x')
    t.file('package.json', json.dumps({'workspaces': {'packages': ['repos/x']}}))
    case('b-npm-object-form', t, dict(status='ACCEPT', members=[], states={'npm-workspaces-members': ('refused', 'workspaces-shape-unsupported')}))
    # No workspaces key: read, no entry.
    t = Tree().file('package.json', json.dumps({'name': 'w'}))
    case('b-npm-no-workspaces', t, dict(status='ACCEPT', members=[], states={'npm-workspaces-members': ('read', None)}, unresolved={'npm-workspaces-members': []}))
    # Parse failures.
    t = Tree().file('package.json', '{"workspaces": [1.5]}')
    case('b-npm-parse-float', t, dict(status='ACCEPT', states={'npm-workspaces-members': ('refused', 'parse')}))
    t = Tree().file('package.json', '{"a": 1, "a": 2}')
    case('b-npm-parse-duplicate-key', t, dict(status='ACCEPT', states={'npm-workspaces-members': ('refused', 'parse')}))
    t = Tree().file('.cargo/config.toml', '[patch.crates-io\n')
    case('b-cargo-parse', t, dict(status='ACCEPT', states={'cargo-config-patch': ('refused', 'parse')}))
    t = Tree().file('.cargo/config.toml', 'patch = 3\n')
    case('b-cargo-patch-not-table', t, dict(status='ACCEPT', states={'cargo-config-patch': ('refused', 'parse')}))
    # Carrier custody.
    t = Tree().repo('repos/x').npm('repos/x', 'x'); t.workspaces(['repos/x']); t.fs[path('package.json')]['mode'] = '0666'
    case('b-carrier-custody', t, dict(status='ACCEPT', members=[], states={'npm-workspaces-members': ('refused', 'custody:WRITABLE_BY_OTHERS')}, nested=['repos/x']))
    t = Tree().repo('repos/a').crate('repos/a', 'a'); t.cargo_config([('a', '{ path = "repos/a" }')]); t.fs[path('.cargo')]['mode'] = '0777'
    case('b-carrier-directory-custody', t, dict(status='ACCEPT', members=[], states={'cargo-config-patch': ('refused', 'custody:WRITABLE_BY_OTHERS')}))
    # --- Every entry disposition.
    t = Tree().repo('repos/a').crate('repos/a', 'a').repo('repos/m').crate('repos/m', 'other').repo('repos/v').crate('repos/v', 'v', None)
    t.dir('repos/e')
    t.cargo_config([('a', '{ path = "repos/a" }'), ('g', '{ git = "https://example.invalid/g" }'), ('p', '{ path = "repos/a", package = "q" }'),
                    ('m', '{ path = "repos/m" }'), ('v', '{ path = "repos/v" }'), ('e', '{ path = "repos/e" }'), ('n', '{ path = "repos/none" }'),
                    ('abs', '{ path = "/etc" }'), ('up', '{ path = "../x" }'), ('dot', '{ path = "./repos/a" }')])
    case('b-cargo-dispositions', t, dict(status='ACCEPT', members=['repos/a', 'repos/m', 'repos/v'], links=[('cargo', 'a', 'repos/a')],
         unresolved={'cargo-config-patch': [('patch.crates-io.abs', 'entry-path-outside-root', None), ('patch.crates-io.dot', 'entry-path-grammar', None),
                                            ('patch.crates-io.e', 'entry-not-in-a-member', None), ('patch.crates-io.g', 'patch-entry-not-path', None),
                                            ('patch.crates-io.m', 'patch-target-name-mismatch', None), ('patch.crates-io.n', 'entry-path-absent', None),
                                            ('patch.crates-io.p', 'patch-entry-not-path', None), ('patch.crates-io.up', 'entry-path-outside-root', None),
                                            ('patch.crates-io.v', 'provided-version-unusable', None)]}))
    t = Tree().repo('repos/x').repo('repos/y').file('repos/y/package.json', '{"name": "y", "version": 1}').repo('repos/z').npm('repos/z', 'z', None)
    t.workspaces(['repos/x', 'repos/y', 'repos/z'])
    case('b-npm-link-failures', t, dict(status='ACCEPT', members=['repos/x', 'repos/y', 'repos/z'], links=[],
         unresolved={'npm-workspaces-members': [('repos/x', 'link-manifest-unusable', 'absent'), ('repos/y', 'provided-version-unusable', None),
                                                ('repos/z', 'provided-version-unusable', None)]}))
    t = Tree().repo('repos/x').file('repos/x/package.json', '{"version": "1.0.0"}').repo('repos/u').file('repos/u/package.json', '{bad')
    t.workspaces(['repos/x', 'repos/u'])
    case('b-npm-manifest-unusable', t, dict(status='ACCEPT', members=['repos/u', 'repos/x'], links=[],
         unresolved={'npm-workspaces-members': [('repos/u', 'link-manifest-unusable', 'parse'), ('repos/x', 'link-manifest-unusable', 'name-absent')]}))
    # Ambiguous providers: both entries give no link; their members are still declared.
    t = Tree().repo('repos/p').npm('repos/p/one', 'dup').npm('repos/p/two', 'dup').npm('repos/p/three', 'solo')
    t.workspaces(['repos/p/one', 'repos/p/two', 'repos/p/three'])
    case('b-npm-ambiguous-provider', t, dict(status='ACCEPT', members=['repos/p'], links=[('npm', 'solo', 'repos/p/three')],
         unresolved={'npm-workspaces-members': [('repos/p/one', 'ambiguous-provider', None), ('repos/p/two', 'ambiguous-provider', None)]}))
    # --- Candidates that fail placement or 6b: excluded, disclosed, still boundaries.
    t = Tree().repo('repos/f', git_file=True).npm('repos/f', 'f').repo('repos/h', extra=['.hg']).npm('repos/h', 'h').repo('repos/s').npm('repos/s', 's')
    t.dir('vol').repo('vol/r', dev=2).npm('vol/r', 'r').repo('repos/c', mode='0777').npm('repos/c', 'c').dir('proj').file('proj/opensip.json', '{}').repo('proj/r').npm('proj/r', 'pr')
    t.observations[path('repos/s')] = 'member-vcs-unsupported:config-include'
    t.workspaces(['repos/f', 'repos/h', 'repos/s', 'vol/r', 'repos/c', 'proj/r'])
    case('b-candidates-excluded', t, dict(status='ACCEPT', members=[], links=[],
         unresolved={'npm-workspaces-members': [('proj/r', 'member-excluded', 'JOIN_CROSSES_NESTED_PROJECT'), ('repos/c', 'member-excluded', 'DIRECTORY_CUSTODY:WRITABLE_BY_OTHERS'),
                                                ('repos/f', 'member-excluded', 'member-vcs-unsupported:git-not-directory'), ('repos/h', 'member-excluded', 'member-vcs-unsupported:vcs-other'),
                                                ('repos/s', 'member-excluded', 'member-vcs-unsupported:config-include'), ('vol/r', 'member-excluded', 'member-outside-volume')]},
         nested=['repos/h', 'repos/s', 'repos/c', 'repos/f']))
    t = Tree().repo('.opensip/r').npm('.opensip/r', 'o')
    t.workspaces(['.opensip/r'])
    # r2 (RF-1): W/.opensip is a pruned anchor the placement walk never enters, so the repository below it is never seen.
    case('b-entry-under-root-opensip', t, dict(status='ACCEPT', members=[], unresolved={'npm-workspaces-members': [('.opensip/r', 'entry-not-in-a-member', None)]},
         notRead=[path('.opensip/r/package.json')]))
    # Provider manifest custody; an entry inside a nested repository of a member; both readers declaring one member.
    t = Tree().repo('repos/a').npm('repos/a', 'a').repo('repos/a/vendor/sub').npm('repos/a/vendor/sub', 'sub').repo('repos/k').npm('repos/k', 'k')
    t.fs[path('repos/k/package.json')]['mode'] = '0666'
    t.crate('repos/a', 'a').cargo_config([('a', '{ path = "repos/a" }')])
    t.workspaces(['repos/a', 'repos/a/vendor/sub', 'repos/k'])
    case('b-inner-boundary-and-manifest-custody', t, dict(status='ACCEPT', members=['repos/a', 'repos/k'],
         declaredBy={'repos/a': ['reader', 'reader'], 'repos/k': ['reader']}, links=[('cargo', 'a', 'repos/a'), ('npm', 'a', 'repos/a')],
         unresolved={'npm-workspaces-members': [('repos/a/vendor/sub', 'entry-not-in-a-member', None), ('repos/k', 'link-manifest-unusable', 'custody:WRITABLE_BY_OTHERS')]},
         nested=['repos/a/vendor/sub']))
    # --- Member contents: its own opensip.json, a nested repository inside it, SX-1 at its root.
    t = Tree().repo('repos/a').npm('repos/a', 'a').file('repos/a/opensip.json', '{}').repo('repos/a/vendor/sub').npm('repos/a/vendor/sub', 'sub')
    t.dir('repos/a/.opensip/cache').npm('repos/a/.opensip/cache', 'hidden').dir('repos/a/inner').file('repos/a/inner/opensip.json', '{}')
    t.workspaces(['repos/a'])
    case('b-member-contents', t, dict(status='ACCEPT', members=['repos/a'], configs=['repos/a/opensip.json'], nested=['repos/a/vendor/sub'], notNested=['repos/a'],
         pruned=[('repos/a/.opensip', 'opensip-custody-state'), ('repos/a/.git', 'vcs-tree')], nestedProjects=['repos/a/inner'], notProjects=['repos/a'],
         links=[('npm', 'a', 'repos/a')]))
    # --- The cap: 64 admits, 65 refuses (counted after placement, before 6b).
    for n, ok in ((64, True), (65, False)):
        t = Tree()
        for i in range(n):
            t.repo('m%02d' % i).npm('m%02d' % i, 'p%02d' % i)
        t.workspaces(['m%02d' % i for i in range(n)])
        if ok:
            case('b-cap-%d' % n, t, dict(status='ACCEPT', membersCount=n))
        else:
            case('b-cap-%d' % n, t, dict(status='REFUSE', refusal='PROJECT.SCOPE_LIMIT', detail='members:65>64', membersCount=0))
    t = Tree()
    for i in range(65):
        t.repo('m%02d' % i, git_file=(i == 0)).npm('m%02d' % i, 'p%02d' % i)
    t.workspaces(['m%02d' % i for i in range(65)])
    case('b-cap-placement-failure-not-counted', t, dict(status='ACCEPT', membersCount=64))
    # --- W in a repository: readers declare nothing; literal entries inside nested repositories are disclosed.
    t = Tree(w_vcs=True).repo('repos/x').npm('repos/x', 'x').dir('packages/p').npm('packages/p', 'p')
    t.workspaces(['repos/x', 'packages/p', 'repos/*', '../out'])
    case('w-in-repository', t, dict(status='ACCEPT', members=[], links=[], nested=['repos/x'],
         unresolved={'npm-workspaces-members': [('repos/x', 'member-excluded', 'workspace-root-inside-repository')]}))
    # --- Branch A: the array decides; readers only link.
    t = Tree().repo('repos/a').crate('repos/a/crates/a', 'a').repo('repos/b').crate('repos/b', 'b').dir('own').crate('own', 'own')
    t.cargo_config([('a', '{ path = "repos/a/crates/a" }'), ('b', '{ path = "repos/b" }'), ('own', '{ path = "own" }')])
    case('a-config-roots', t, dict(status='ACCEPT', members=['repos/a'], declaredBy={'repos/a': ['config-workspace-roots']}, links=[('cargo', 'a', 'repos/a/crates/a')],
         unresolved={'cargo-config-patch': [('patch.crates-io.b', 'dropped-workspace-roots-present', None), ('patch.crates-io.own', 'entry-not-in-a-member', None)]},
         notNested=['repos/a', 'repos/b'], units=['repos/a/crates/a']), configWorkspaceRoots=['repos/a/crates/a'])
    case('a-explicit-joins', t, dict(status='ACCEPT', members=['repos/a'], declaredBy={'repos/a': ['explicit-joins']}), explicitJoins=['repos/a/crates/a'])
    t3 = Tree().repo('repos/a').crate('repos/a/crates/a', 'a').crate('repos/a/crates/other', 'other').crate('repos/a', 'top')
    case('a-exact-roots-inside-member', t3, dict(status='ACCEPT', members=['repos/a'], unitsExact=['repos/a/crates/a']), configWorkspaceRoots=['repos/a/crates/a'])
    t2 = Tree().repo('repos/a').crate('repos/a/x', 'x').crate('repos/a/y', 'y')
    case('a-two-roots-one-member', t2, dict(status='ACCEPT', members=['repos/a'], declaredBy={'repos/a': ['config-workspace-roots', 'config-workspace-roots']}),
         configWorkspaceRoots=['repos/a/x', 'repos/a/y'])
    t = Tree().repo('repos/f', git_file=True).crate('repos/f', 'f')
    case('a-layout-refuses', t, dict(status='REFUSE', refusal='PROJECT.ROOT_CUSTODY_REFUSED', detail='member-vcs-unsupported:git-not-directory'), configWorkspaceRoots=['repos/f'])
    t = Tree().repo('repos/s').crate('repos/s', 's'); t.observations[path('repos/s')] = 'member-vcs-unsupported:index-split-or-sparse'
    case('a-6b-refuses', t, dict(status='REFUSE', refusal='PROJECT.ROOT_CUSTODY_REFUSED', detail='member-vcs-unsupported:index-split-or-sparse'), configWorkspaceRoots=['repos/s'])
    t = Tree().repo('repos/c', mode='0777').crate('repos/c', 'c')
    case('a-custody-refuses', t, dict(status='REFUSE', refusal='PROJECT.ROOT_CUSTODY_REFUSED', detail='WRITABLE_BY_OTHERS', path=path('repos/c')), configWorkspaceRoots=['repos/c'])
    t = Tree().dir('vol').repo('vol/r', dev=2).crate('vol/r', 'r')
    case('a-outside-volume', t, dict(status='REFUSE', refusal='PROJECT.ROOT_CUSTODY_REFUSED', detail='member-outside-volume'), configWorkspaceRoots=['vol/r'])
    t = Tree(w_vcs=True).repo('repos/a').crate('repos/a', 'a')
    case('a-root-in-repository', t, dict(status='REFUSE', refusal='PROJECT.EXPLICIT_PATH_INVALID', detail='JOIN_CROSSES_NESTED_REPOSITORY'), configWorkspaceRoots=['repos/a'])
    t = Tree().repo('repos/a').repo('repos/a/inner').crate('repos/a/inner', 'i')
    case('a-root-in-nested-of-member', t, dict(status='REFUSE', refusal='PROJECT.EXPLICIT_PATH_INVALID', detail='JOIN_CROSSES_NESTED_REPOSITORY', path=path('repos/a/inner')),
         configWorkspaceRoots=['repos/a/inner'])
    t = Tree().dir('proj').file('proj/opensip.json', '{}').repo('proj/r').crate('proj/r', 'r')
    case('a-nested-project-between', t, dict(status='REFUSE', refusal='PROJECT.EXPLICIT_PATH_INVALID', detail='JOIN_CROSSES_NESTED_PROJECT'), configWorkspaceRoots=['proj/r'])
    t = Tree()
    for i in range(65):
        t.repo('m%02d' % i).crate('m%02d' % i, 'p%02d' % i)
    case('a-cap-65', t, dict(status='REFUSE', refusal='PROJECT.SCOPE_LIMIT', detail='members:65>64'), configWorkspaceRoots=['m%02d' % i for i in range(65)])
    # --- Selection never changes: a launch inside a member selects that member alone.
    t = Tree().repo('repos/a').crate('repos/a', 'a'); t.cargo_config([('a', '{ path = "repos/a" }')])
    case('launch-inside-member', t, dict(status='ACCEPT', selectedRoot=path('repos/a'), members=[]), cwd=path('repos/a'))
    # --- A selection refusal before any root: no W, so no carrier is observed (LD-B3B0-4).
    t = Tree(); t.fs[W]['mode'] = '0777'
    case('selection-refused', t, dict(status='REFUSE', refusal='PROJECT.ROOT_CUSTODY_REFUSED', states={'cargo-config-patch': ('absent', None), 'npm-workspaces-members': ('absent', None)}))
    # --- The owner waiver reaches member directories, never files or Git evidence.
    t = Tree(config=False).repo('repos/o', uid=2000).crate('repos/o', 'o')
    t.observations[path('repos/o')] = 'member-vcs-unsupported:global-custody'
    case('a-waiver-directories-not-git', t, dict(status='REFUSE', refusal='PROJECT.ROOT_CUSTODY_REFUSED', detail='member-vcs-unsupported:global-custody'),
         explicitProject=W, trustProjectOwner=True, configWorkspaceRoots=['repos/o'])
    t = Tree(config=False).repo('repos/o', uid=2000).crate('repos/o', 'o')
    case('a-waiver-admits-member-directory', t, dict(status='ACCEPT', members=['repos/o']), explicitProject=W, trustProjectOwner=True, configWorkspaceRoots=['repos/o'])
    # --- r2 (B3B0REF-R1-RF-1): no entry inside a member's pruned anchor is placed below the anchor or read.
    t = Tree().repo('a').npm('a', 'a').npm('a/.opensip/p', 'hidden').file('a/.git/package.json', json.dumps({'name': 'git-hidden', 'version': '1.0.0'}))
    t.npm('a/node_modules/dep', 'dep')
    t.workspaces(['a', 'a/.opensip/p', 'a/.git', 'a/node_modules/dep'])
    case('rf1-npm-anchors-never-read', t, dict(status='ACCEPT', members=['a'], links=[('npm', 'a', 'a')],
         unresolved={'npm-workspaces-members': [('a/.git', 'entry-not-in-a-member', None), ('a/.opensip/p', 'entry-not-in-a-member', None),
                                                ('a/node_modules/dep', 'entry-not-in-a-member', None)]},
         notRead=[path('a/.opensip/p/package.json'), path('a/.git/package.json'), path('a/node_modules/dep/package.json')],
         notObserved=[path('a/.opensip'), path('a/.opensip/p'), path('a/.opensip/p/package.json'), path('a/.git'), path('a/.git/package.json'),
                      path('a/node_modules'), path('a/node_modules/dep')],
         pruned=[('a/.opensip', 'opensip-custody-state'), ('a/.git', 'vcs-tree')]))
    t = Tree().repo('a').crate('a', 'a').crate('a/.opensip/c', 'c').crate('a/target/t', 't')
    t.cargo_config([('a', '{ path = "a" }'), ('c', '{ path = "a/.opensip/c" }'), ('t', '{ path = "a/target/t" }')])
    case('rf1-cargo-anchors-never-read', t, dict(status='ACCEPT', members=['a'], links=[('cargo', 'a', 'a')],
         unresolved={'cargo-config-patch': [('patch.crates-io.c', 'entry-not-in-a-member', None), ('patch.crates-io.t', 'entry-not-in-a-member', None)]},
         notRead=[path('a/.opensip/c/Cargo.toml'), path('a/target/t/Cargo.toml')]))
    # --- r3 (B3B0REF-R2-RF-1): globs see only lawfully visible repositories. Paired fixtures differ only by a repository
    # hidden below an anchor; the hidden addition changes nothing and is never consulted.
    for anchor in ('.opensip', 'node_modules'):
        for hidden in (False, True):
            t = Tree().dir(anchor)
            if hidden:
                t.repo(anchor + '/secret').npm(anchor + '/secret', 'secret')
            t.workspaces([anchor + '/*'])
            case('r3-glob-under-%s-%s' % (anchor.strip('.'), 'hidden-repo' if hidden else 'empty'), t,
                 dict(status='ACCEPT', members=[], unresolved={'npm-workspaces-members': []},
                      notObserved=[path(anchor + '/secret'), path(anchor + '/secret/.git'), path(anchor + '/secret/package.json')]))
    t = Tree().repo('repos/x').dir('repos/x/packages/p').npm('repos/x/packages/p', 'p')
    t.workspaces(['repos/x/packages/*'])
    case('r3-glob-crossing-by-visible-repository', t, dict(status='ACCEPT', members=[],
         unresolved={'npm-workspaces-members': [('repos/x/packages/*', 'workspace-glob-crosses-repository', None)]},
         notObserved=[path('repos/x/packages'), path('repos/x/packages/p')]))
    t = Tree().dir('proj').file('proj/opensip.json', '{}').repo('proj/r').npm('proj/r', 'r')
    t.workspaces(['proj/*'])
    case('r3-glob-repository-inside-nested-project-not-visible', t, dict(status='ACCEPT', members=[], unresolved={'npm-workspaces-members': []},
         notObserved=[path('proj/r')]))
    # --- r2 (B3B0REF-R1-RF-2): branch A settles the array's grammar, absence and crossings (SLM) before member decisions.
    for src in ('configWorkspaceRoots', 'explicitJoins'):
        t = Tree().repo('a', git_file=True).crate('a', 'a').repo('b').crate('b', 'b')
        case('rf2-%s-grammar-before-layout' % src, t, dict(status='REFUSE', refusal='PROJECT.EXPLICIT_PATH_INVALID', detail='JOIN_PATH_GRAMMAR'), **{src: ['../bad', 'a']})
        case('rf2-%s-grammar-after-layout' % src, t, dict(status='REFUSE', refusal='PROJECT.EXPLICIT_PATH_INVALID', detail='JOIN_PATH_GRAMMAR'), **{src: ['a', '../bad']})
        case('rf2-%s-absent-before-layout' % src, t, dict(status='REFUSE', refusal='PROJECT.EXPLICIT_PATH_INVALID', detail='ABSENT', path=path('missing')), **{src: ['missing', 'a']})
        case('rf2-%s-member-then-absent' % src, t, dict(status='REFUSE', refusal='PROJECT.EXPLICIT_PATH_INVALID', detail='ABSENT', path=path('b/missing')), **{src: ['b', 'b/missing']})
        t2 = Tree().repo('a').crate('a', 'a').repo('a/inner').crate('a/inner', 'i').repo('f', git_file=True).crate('f', 'f')
        case('rf2-%s-crossing-before-layout' % src, t2, dict(status='REFUSE', refusal='PROJECT.EXPLICIT_PATH_INVALID', detail='JOIN_CROSSES_NESTED_REPOSITORY', path=path('a/inner')),
             **{src: ['f', 'a/inner']})
        t3 = Tree().repo('a').crate('a', 'a').repo('b').crate('b', 'b'); t3.observations[path('b')] = 'member-vcs-unsupported:config-include'
        case('rf2-%s-member-decisions-in-path-order' % src, t3, dict(status='REFUSE', refusal='PROJECT.ROOT_CUSTODY_REFUSED', detail='member-vcs-unsupported:config-include'),
             **{src: ['b', 'a']})
    # --- r2 (B3B0REF-R1-RF-3): one VCS representation. Side-table markers are boundaries wherever they are observed.
    for marker in ('.hg', '.svn', '.jj'):
        t = Tree().dir('a').dir('a/' + marker).npm('a', 'a')
        t.markers[path('a')] = [marker]
        t.workspaces(['a'])
        case('rf3-side-table-%s-excluded-and-a-boundary' % marker.strip('.'), t, dict(status='ACCEPT', members=[],
             unresolved={'npm-workspaces-members': [('a', 'member-excluded', 'member-vcs-unsupported:vcs-other')]}, nested=['a'], notUnits=['a']))
    t = Tree().dir('a').file('a/.git', 'gitdir: /elsewhere').npm('a', 'a')
    t.markers[path('a')] = ['.git']
    t.workspaces(['a'])
    case('rf3-side-table-git-file', t, dict(status='ACCEPT', members=[], unresolved={'npm-workspaces-members': [('a', 'member-excluded', 'member-vcs-unsupported:git-not-directory')]},
         nested=['a'], notUnits=['a']))
    t = Tree().repo('m').npm('m', 'm').dir('m/sub').dir('m/sub/.jj').npm('m/sub', 'inner')
    t.markers[path('m/sub')] = ['.jj']
    t.workspaces(['m'])
    case('rf3-side-table-nested-in-member', t, dict(status='ACCEPT', members=['m'], nested=['m/sub'], notUnits=['m/sub'], units=['m']))
    t = Tree().repo('x').npm('x', 'x')
    t.fs['/h/.hg'] = dict(kind='dir', uid=UID, mode='0755', dev=1)
    t.markers['/h'] = ['.hg']
    t.workspaces(['x'])
    case('rf3-side-table-ancestor-of-w', t, dict(status='ACCEPT', selectedRoot=W, members=[],
         unresolved={'npm-workspaces-members': [('x', 'member-excluded', 'workspace-root-inside-repository')]}))
    t = Tree().dir('a').npm('a', 'a'); t.markers[path('a')] = ['.hg']
    t.workspaces(['a'])
    case('rf3-side-table-inconsistent-refuses-before-discovery', t, dict(raises='VCS_SIDE_TABLE_INCONSISTENT:' + path('a')))
    # --- r2 (B3B0REF-R1-RF-4): M1's depth bounds the candidate, never the declaring entry.
    for depth in (256, 257):
        t = Tree().repo('a').npm('a/' + '/'.join(['d'] * (depth - 1)), 'deep')
        rel = 'a/' + '/'.join(['d'] * (depth - 1))
        t.workspaces([rel])
        case('rf4-entry-depth-%d' % depth, t, dict(status='ACCEPT', members=['a'], links=[('npm', 'deep', rel)]))
    deep = '/'.join(['d'] * 256) + '/r'
    t = Tree().repo(deep).npm(deep, 'r')
    t.workspaces([deep])
    case('rf4-candidate-depth-257-excluded', t, dict(status='ACCEPT', members=[], unresolved={'npm-workspaces-members': [(deep, 'member-excluded', 'DEPTH')]}))
    t = Tree().repo(deep).crate(deep, 'r')
    case('rf4-candidate-depth-257-refuses', t, dict(status='REFUSE', refusal='PROJECT.ROOT_CUSTODY_REFUSED', detail='DEPTH'), configWorkspaceRoots=[deep])
    return C


class SpyContents(dict):
    """The `contents` side table, recording every path the reference asks it for."""

    def __init__(self, *a):
        super().__init__(*a)
        self.asked = []

    def get(self, key, default=None):
        self.asked.append(key)
        return super().get(key, default)


def check_case(ref, ctx, cid, inp, expect, failures):
    if 'raises' in expect:
        try:
            ref.discover(ctx, inp)
        except ValueError as e:
            ok = str(e) == expect['raises']
            if not ok:
                failures.append((cid, str(e), expect))
            return None, [], ok
        failures.append((cid, 'did not raise', expect))
        return None, [], False
    spy = SpyContents(inp.get('contents', {}))
    inp = dict(inp, contents=spy)
    ref.OBSERVED = []
    try:
        result, links = ref.discover(ctx, inp)
        observed = ref.OBSERVED
    finally:
        ref.OBSERVED = None
    prov = result['provenance']
    got = {}
    rel = lambda p: p[len(W) + 1:] if p.startswith(W + '/') else p
    if 'status' in expect:
        got['status'] = result['status']
    for k in ('refusal', 'detail', 'path'):
        if k in expect:
            got[k] = result.get(k)
    if 'selectedRoot' in expect:
        got['selectedRoot'] = prov['selectedRoot']
    if 'members' in expect:
        got['members'] = [rel(m['path']) for m in prov['memberRepositories']]
    if 'membersCount' in expect:
        got['membersCount'] = len(prov['memberRepositories'])
    if 'declaredBy' in expect:
        got['declaredBy'] = {rel(m['path']): [d['source'] for d in m['declaredBy']] for m in prov['memberRepositories'] if rel(m['path']) in expect['declaredBy']}
    rows = {r['readerId']: r for r in prov['workspaceDeclarations']}
    if 'unresolved' in expect:
        got['unresolved'] = {r: [(u['entry'], u['reason'], u['subject']) for u in rows[r]['unresolved']] for r in expect['unresolved']}
        expect = dict(expect, unresolved={r: [tuple(x) for x in v] for r, v in expect['unresolved'].items()})
    if 'states' in expect:
        got['states'] = {r: (rows[r]['state'], rows[r]['stateSubject']) for r in expect['states']}
    if 'links' in expect:
        got['links'] = sorted((l['ecosystem'], l['packageName'], l['packageDir']) for l in links)
        expect = dict(expect, links=sorted(expect['links']))
    if 'configs' in expect:
        got['configs'] = [rel(c) for c in prov['memberConfigs']]
    for k, field in (('nested', 'nestedRepositories'), ('nestedProjects', 'nestedProjects')):
        if k in expect:
            got[k] = [x for x in expect[k] if path(x) in prov[field]]
    for k, field in (('notNested', 'nestedRepositories'), ('notProjects', 'nestedProjects')):
        if k in expect:
            got[k] = [x for x in expect[k] if path(x) not in prov[field]]
    if 'unitsExact' in expect:
        got['unitsExact'] = sorted(rel(u['path']) for u in prov['units'])
    if 'notRead' in expect:
        got['notRead'] = [x for x in expect['notRead'] if x not in spy.asked]
    if 'notObserved' in expect:
        got['notObserved'] = [x for x in expect['notObserved'] if x not in observed]
    if 'notUnits' in expect:
        got['notUnits'] = [x for x in expect['notUnits'] if path(x) not in [u['path'] for u in prov['units']]]
    if 'units' in expect:
        got['units'] = [x for x in expect['units'] if path(x) in [u['path'] for u in prov['units']]]
    if 'pruned' in expect:
        have = {(rel(p['path']), p['reason']) for p in prov['prunedTrees']}
        got['pruned'] = [x for x in expect['pruned'] if tuple(x) in have]
        expect = dict(expect, pruned=[tuple(x) for x in expect['pruned']])
    want = {k: v for k, v in expect.items() if k in got}
    ok = got == want and set(got) == set(expect)
    if not ok:
        failures.append((cid, got, expect))
    return result, links, ok


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--architecture', type=Path, required=True); ap.add_argument('--reference', type=Path, required=True)
    ap.add_argument('--packages-root', type=Path, required=True); ap.add_argument('--out', type=Path, required=True)
    a = ap.parse_args()
    A = a.architecture
    sys.path.insert(0, str(a.packages_root / 'tools/contracts/python-packages'))
    ref = module('member_reader_reference', a.reference)
    ctx = ref.Context(A)
    canonical = ctx.C
    raw = (A / BUNDLE[0]).read_bytes(); assert hashlib.sha256(raw).hexdigest() == BUNDLE[1]
    bundle = json.loads(raw); add = json.loads((A / B_S1).read_bytes())
    for section in ('$defs', 'schemas'):
        for k, v in add[section].items():
            assert k not in bundle[section]; bundle[section][k] = v

    def valid(name, value):
        schema = copy.deepcopy(bundle); schema['$ref'] = '#/schemas/' + name; canonical.validate(schema, value)

    failures, rows = [], []
    summary = dict(discoveryCases=0, equal=0, d15Cases=0, d15Passed=0, v3Valid=0, inventoriesValid=0)
    # Stage 1: no-member equality with B2-b0.
    for c in json.loads((A / CASES).read_bytes())['cases']:
        if c.get('model', 'discovery') != 'discovery':
            continue
        summary['discoveryCases'] += 1
        try:
            mine, links = ref.discover(ctx, copy.deepcopy(c['input']))
            theirs, _, _ = ctx.b2b0.current(ctx.slm, ctx.rule, copy.deepcopy(c['input']))
            theirs = ctx.b2b0.project_v3(theirs); theirs.pop('pendingFields', None)
            strip = lambda r: dict({k: v for k, v in r.items() if k != 'provenance'}, provenance={k: v for k, v in r['provenance'].items() if k not in D15})
            same = strip(mine) == strip(theirs) and mine['provenance']['memberRepositories'] == [] and mine['provenance']['memberConfigs'] == [] and links == []
            valid('DiscoveryResultV3', mine); summary['v3Valid'] += 1
            if mine['status'] == 'ACCEPT':
                valid('AdmittedBoundaryInventoryV3', ref.boundary_inventory_v3(ctx, mine)); summary['inventoriesValid'] += 1
        except Exception as e:  # noqa: BLE001 (every exception fails)
            failures.append((c['id'], 'exception', repr(e))); continue
        if same:
            summary['equal'] += 1
        else:
            failures.append((c['id'], 'differs from B2-b0 with no declaration'))
        rows.append(dict(id=c['id'], stage='no-member-equality', equal=same))
    # Stage 2: the D15 cases.
    for cid, inp, expect in d15_cases():
        summary['d15Cases'] += 1
        try:
            result, links, ok = check_case(ref, ctx, cid, inp, expect, failures)
            if result is None:
                summary['d15Passed'] += ok
                rows.append(dict(id=cid, stage='d15', passed=ok, raises=expect['raises']))
                continue
            valid('DiscoveryResultV3', result); summary['v3Valid'] += 1
            if result['status'] == 'ACCEPT':
                valid('AdmittedBoundaryInventoryV3', ref.boundary_inventory_v3(ctx, result)); summary['inventoriesValid'] += 1
        except Exception as e:  # noqa: BLE001
            failures.append((cid, 'exception', repr(e))); continue
        summary['d15Passed'] += ok
        rows.append(dict(id=cid, stage='d15', passed=ok, status=result['status'], refusal=result.get('refusal'), detail=result.get('detail'),
                         members=[m['path'] for m in result['provenance']['memberRepositories']], links=len(links)))
    if summary['discoveryCases'] != 64:
        failures.append(('coverage', 'discoveryCases', summary['discoveryCases']))
    out = dict(standing='B3-b0 members-and-readers reference checks (design evidence)', summary=summary, rows=rows,
               failures=[[str(x) for x in f] for f in failures], passed=not failures)
    a.out.write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps(summary), 'passed' if not failures else 'FAILED')
    for f in failures[:40]:
        print('FAIL', f)
    raise SystemExit(0 if not failures else 1)


if __name__ == '__main__':
    main()
