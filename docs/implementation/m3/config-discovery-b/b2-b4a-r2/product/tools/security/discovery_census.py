"""The T2 discovery census and its cost model (M3-B r5 item 12; unit B2-b4a, B2-b4 plan r2).

Developer tool only. It writes or checks two generated files:
  * crates/security/src/custody/discovery_census_vectors.json: the cost model's objects-and-edges prediction for every
    accepted walk vector (tools/security/discovery_walk_vectors.py) and for the composed-workspace vectors below. The
    security test suite walks each natively on a fresh discovery ledger and asserts the walker used no more
    (discovery_census_tests.rs, the soundness control).
  * crates/security/src/custody/discovery_census.json: the census of every lead-readable T2 entry, and every workspace
    as a composed checkout, with the modeled objects and edges against the discovery profile's limits. The ten
    held-out entries are `outstanding: held-out` and are never opened.

The cost model is an abstract walk that mirrors custody/discovery_walk.rs step for step and adds each charge the walker
makes. Its constants are read from the code by anchored matches, and every file of the transitive cost closure is pinned
whole: any change to any of them refuses the census (plan r2, RF-3). Unknowns are charged at their dearer branch: every
judged directory and every present regular marker is captured, every capture takes the filesystem branch, every
listing returns `.` and `..`, every chain passes, and a regular `.git` file is read at its uninterrupted envelope.
Interrupted read retries are excluded: the margin is structural (plan r2, RF-2). Objects and edges only; bytes are
bounded by other means (item 12, r2 NBO-1).

The population is the bound B2-b0 reference's (contract successor 164): every walk this tool models is compared with
`walker_population` over the same tree, and a difference refuses (LD-B2B4-1).

Integrity (plan r2 section 1.1): each store is re-verified before counting. The Git tree object and the QD-22 tree
digest are recomputed from the stored bytes with no-follow traversal; any extra object, any mode other than the
store's, any non-regular object and any `.git` path component refuses. Held-out entries are read from the manifest by
id and flag only, and their digests are never joined to a store path. No network, repository code, subprocess or
environment input.
"""

from pathlib import Path
import argparse
import copy
import hashlib
import importlib.util
import json
import os
import re
import stat
import sys

OUTPUT_VECTORS = 'crates/security/src/custody/discovery_census_vectors.json'
OUTPUT_CENSUS = 'crates/security/src/custody/discovery_census.json'
WALK_VECTORS = 'crates/security/src/custody/discovery_walk_vectors.json'
WALK_TOOL = 'tools/security/discovery_walk_vectors.py'
MANIFEST = 'docs/implementation/m3/corpus/t2-corpus-manifest.draft.json'

# The transitive cost closure (plan r2 section 1.3): path, bytes, SHA-256. Any change refuses.
CLOSURE = (
    ('crates/security/src/custody/discovery_walk.rs', 43629, 'ffec30d0bafe2578d9b819422a86404065a84e28fd31f58e387f21b8d9cb4988'),
    ('crates/security/src/custody/project_admission.rs', 77277, 'd9856dbc56eabddb20b2468fccf3199f46ce28d80b4c46d838cbdecf25d140ce'),
    ('crates/security/src/custody/project_chain.rs', 32761, '3a824290da7697001871d20b7b0eb6339085d9cd7ef0ccab786cf54e3dd0b53c'),
    ('crates/security/src/trust/initial_platform.rs', 21613, '227d35a35b58b06002bcaa21c490ce8d5d28474000427c16adafe8e84616aa94'),
    ('crates/security/src/custody/discovery_scan.rs', 29699, '79c17dbfe1f0d28bcde24cdd418db6f3eec9d9cf3dfef628038088f3accd1c44'),
    ('crates/security/src/custody/discovery_rule.rs', 18080, 'e3e3ef60293c825befcc024cd0a21e60e2b25d71444d66ab18f30d5a92bc20c2'),
    ('crates/security/src/custody.rs', 75486, '60a1641e8270f7250f8f377d1aff3ef78ae40c2cd246b8c535fb73f0a6dfbf00'),
    ('crates/platform/src/filesystem/directory_open.rs', 25442, '71ca33594e1775d9e1bbe2deba15ba4a38bd9ad2c528772a0842c63e3d1cc62a'),
    ('crates/platform/src/filesystem/path_binding.rs', 33600, 'a005d378507857a2d9bc4e56affb5e04b7cbd989bc9b2d423a9834c92e6b8a93'),
    ('crates/platform/src/filesystem.rs', 103566, '1c3831111ff782dff6841867d08e7fbc890e42580201fd0ba44410a36ad19162'),
    ('crates/platform/src/filesystem/descriptor_acl_capture.rs', 37140, '4113175351bca052d9e8bde9cc3cfe80c21527ff5316cccf9942f0b5f1f8ee02'),
    ('crates/platform/src/filesystem/descriptor_filesystem.rs', 14405, 'b8366f529958eab65f4125bba5bb75212038d899d320536fb4107f60eab79460'),
    ('crates/platform/src/filesystem/directory_entries.rs', 21695, '72824def6fa0fa4432304442ee68307c3e380d03d5e9949fb3ae94a02770c255'),
    ('crates/platform/src/work_reader.rs', 8590, '099df8356d750e4452682e264223fc492985b34eed007091ce5c26dcf10ec3b6'),
    ('crates/platform/src/work_ledger.rs', 34563, 'd7bed3489dafef3c83efae9cd218cd9874f042884279c26f87e071381d8597ab'),
)
HOME = '/h'
ROOT = '/h/w'


def require(condition, message):
    if not condition:
        raise ValueError(message)


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def pin_row(root, path):
    raw = (root / path).read_bytes()
    return dict(path=path, bytes=len(raw), sha256=sha256(raw))


# ------------------------------------------------------------------ the pinned cost constants

# One anchor per constant: (name, file, pattern). The pattern must match exactly once; its groups are the values.
ANCHORS = (
    ('LISTING', 'crates/security/src/custody/discovery_walk.rs',
     r'const LISTING: WorkCost = WorkCost \{\n    objects: (\d+),\n    edges: (\d+),\n    bytes: 1024,\n\};'),
    ('STATUS', 'crates/security/src/custody/discovery_walk.rs',
     r'const STATUS: WorkCost = WorkCost \{\n    objects: (\d+),\n    edges: (\d+),\n    bytes: 512,\n\};'),
    ('OWNED', 'crates/security/src/custody/discovery_walk.rs',
     r'fn owned\(bytes: usize\) -> WorkCost \{\n    WorkCost \{\n        objects: (\d+),\n        edges: (\d+),\n'),
    ('CLASSIFY', 'crates/security/src/custody/discovery_walk.rs',
     r'fn classify_cost\(rel: &str\) -> WorkCost \{\n.*\n.*\n    WorkCost \{\n        objects: (\d+) \+ targets,\n        edges: (\d+),\n'),
    ('RAW_NAME', 'crates/security/src/custody/discovery_walk.rs',
     r'work\.charge::<WalkRefusal>\(WorkCost \{\n                objects: (\d+),\n                edges: (\d+),\n                bytes: name\.len\(\)\.saturating_add\(RECORD\),'),
    ('LISTED_NAME', 'crates/security/src/custody/discovery_walk.rs',
     r'work\.charge::<WalkRefusal>\(WorkCost \{\n                objects: (\d+),\n                edges: (\d+),\n                bytes: name\.len\(\) \+ 2 \* \(rel\.len\(\) \+ 1 \+ name\.len\(\)\) \+ 3 \* RECORD,'),
    ('MAX_LISTED_DEPTH', 'crates/security/src/custody/discovery_walk.rs', r'const MAX_LISTED_DEPTH: usize = (\d+);'),
    ('GITDIR_TARGET', 'crates/security/src/custody/project_admission.rs',
     r'work\.run\(\n        WorkCost \{\n            objects: (\d+),\n            edges: (\d+),\n            bytes: target\.len\(\),'),
    ('ADMISSION_STATUS', 'crates/security/src/custody/project_admission.rs',
     r'\nconst STATUS: WorkCost = WorkCost \{\n    objects: (\d+),\n    edges: (\d+),\n'),
    ('MAX_CONFIG_BYTES', 'crates/security/src/custody.rs', r'const MAX_CONFIG_BYTES: u64 = (\d+) \* (\d+) \* (\d+);'),
    ('MAX_WORKSPACE_UNITS', 'crates/security/src/custody/discovery_rule.rs', r'pub\(crate\) const MAX_WORKSPACE_UNITS: usize = (\d+);'),
    ('STATUS_READ', 'crates/platform/src/filesystem/path_binding.rs',
     r'pub\(super\) fn status_read_cost\(\) -> crate::WorkCost \{\n    crate::WorkCost \{\n        objects: (\d+),\n        edges: (\d+),\n'),
    ('OPEN_DIR', 'crates/platform/src/filesystem/directory_open.rs',
     r'pub fn open_child_directory_cost\(name: &OsStr\) -> crate::WorkCost \{\n    let status = super::path_binding::status_read_cost\(\);\n    crate::WorkCost \{\n        objects: (\d+),\n        edges: (\d+) \+ status\.edges,\n'),
    ('OBS', 'crates/platform/src/filesystem/directory_open.rs',
     r'pub fn child_absence_observation_cost\(name: &OsStr\) -> crate::WorkCost \{\n    crate::WorkCost \{\n        objects: (\d+),\n        edges: (\d+),\n'),
    ('OPEN_REG', 'crates/platform/src/filesystem.rs',
     r'    pub fn open_regular_cost\(relative: &str\) -> crate::WorkCost \{\n        let components = relative\.split\(./.\)\.count\(\);\n        let status = path_binding::status_read_cost\(\);\n        crate::WorkCost \{\n            objects: (\d+)usize\.saturating_add\(components\.saturating_mul\((\d+)\)\),\n            edges: (\d+)usize\.saturating_add\(components\.saturating_mul\((\d+)\)\),\n'),
    ('CAP', 'crates/platform/src/filesystem/descriptor_acl_capture.rs',
     r'pub fn descriptor_acl_capture_cost\(\) -> WorkCost \{\n    WorkCost \{\n        objects: (\d+),\n        edges: (\d+) \+ MAX_ENTRIES,\n'),
    ('MAX_ENTRIES', 'crates/platform/src/filesystem/descriptor_acl_capture.rs', r'\nconst MAX_ENTRIES: usize = (\d+);'),
    ('FS', 'crates/platform/src/filesystem/descriptor_filesystem.rs',
     r'pub fn descriptor_filesystem_observation_cost\(\) -> crate::WorkCost \{\n.*\n.*\n.*\n.*\n    crate::WorkCost \{\n        objects: (\d+),\n        edges: (\d+),\n'),
    ('READ_OBJECT', 'crates/platform/src/work_reader.rs',
     r'    let ceiling = max \+ 1;\n    charge\(WorkCost \{\n        objects: (\d+),\n        \.\.WorkCost::default\(\)\n    \}\)\?;'),
    ('READ_GROWTH_EDGE', 'crates/platform/src/work_reader.rs',
     r'            charge\(WorkCost \{\n                edges: (\d+),\n                bytes: next,\n'),
    ('READ_ATTEMPT_EDGE', 'crates/platform/src/work_reader.rs',
     r'        \} else \{\n            charge\(WorkCost \{\n                edges: (\d+),\n                \.\.WorkCost::default\(\)\n'),
    ('DISCOVERY_OBJECT_LIMIT', 'crates/platform/src/work_ledger.rs', r'const DISCOVERY_OBJECT_LIMIT: usize = 1 << (\d+);'),
    ('DISCOVERY_EDGE_LIMIT', 'crates/platform/src/work_ledger.rs', r'const DISCOVERY_EDGE_LIMIT: usize = 1 << (\d+);'),
)


def costs(product):
    """Verify the closure whole, then read every constant by its anchor."""
    for path, size, digest in CLOSURE:
        raw = (product / path).read_bytes()
        require(len(raw) == size and sha256(raw) == digest, 'cost closure changed: ' + path)
    out = {}
    for name, path, pattern in ANCHORS:
        text = (product / path).read_text()
        hits = list(re.finditer(pattern, text))
        require(len(hits) == 1, 'cost anchor %s matched %d times' % (name, len(hits)))
        out[name] = tuple(int(g) for g in hits[0].groups())
    c = {}
    c['LISTING'] = out['LISTING']
    c['STATUS'] = out['STATUS']
    c['OWNED'] = out['OWNED']
    c['CLASSIFY_BASE'] = out['CLASSIFY']  # (2 + t, 0)
    c['RAW_NAME'] = out['RAW_NAME']
    c['LISTED_NAME'] = out['LISTED_NAME']
    c['MAX_LISTED_DEPTH'] = out['MAX_LISTED_DEPTH'][0]
    c['GITDIR_TARGET'] = out['GITDIR_TARGET']
    c['ADMISSION_STATUS'] = out['ADMISSION_STATUS']
    a, b, d = out['MAX_CONFIG_BYTES']
    c['MAX_CONFIG_BYTES'] = a * b * d
    c['MAX_WORKSPACE_UNITS'] = out['MAX_WORKSPACE_UNITS'][0]
    status_read = out['STATUS_READ']
    c['OPEN_DIR'] = (out['OPEN_DIR'][0], out['OPEN_DIR'][1] + status_read[1])
    c['OBS'] = out['OBS']
    o1, o2, e1, e2 = out['OPEN_REG']
    c['OPEN_REG_1'] = (o1 + o2, e1 + e2)  # one component
    c['CAP'] = (out['CAP'][0], out['CAP'][1] + out['MAX_ENTRIES'][0])
    c['FS'] = out['FS']
    c['READ_OBJECT'] = out['READ_OBJECT'][0]
    require(out['READ_GROWTH_EDGE'][0] == out['READ_ATTEMPT_EDGE'][0], 'read attempts charge unequal edges')
    c['READ_ATTEMPT_EDGE'] = out['READ_ATTEMPT_EDGE'][0]
    c['LIMITS'] = (1 << out['DISCOVERY_OBJECT_LIMIT'][0], 1 << out['DISCOVERY_EDGE_LIMIT'][0])
    return c


def read_envelope(c, length):
    """`read_charged` without interruption: one object, and one edge per attempt. Each attempt either returns at least
    one byte or is the final EOF, and the ceiling (max + 1) ends the loop, so attempts <= min(L, ceiling) + 1."""
    ceiling = c['MAX_CONFIG_BYTES'] + 1
    return (c['READ_OBJECT'], c['READ_ATTEMPT_EDGE'] * (min(length, ceiling) + 1))


# ------------------------------------------------------------------ trees

class Tree:
    """A filesystem tree under the selected root: rel path -> node; '' is the root directory."""

    def __init__(self, nodes):
        self.nodes = nodes
        self.children = {}
        for rel in nodes:
            if rel:
                parent = rel.rsplit('/', 1)[0] if '/' in rel else ''
                require(parent in nodes and nodes[parent]['kind'] == 'dir', 'orphan entry: ' + rel)
                self.children.setdefault(parent, []).append(rel.rsplit('/', 1)[-1])
        for names in self.children.values():
            names.sort()

    def node(self, rel):
        return self.nodes.get(rel)

    def kind(self, rel):
        n = self.nodes.get(rel)
        return n['kind'] if n else None


def tree_of_vector(case):
    nodes = {'': dict(kind='dir')}
    for e in case['tree']:
        node = dict(kind=e['kind'])
        if e['kind'] == 'file':
            node['size'] = len(e['text'].encode())
            node['text'] = e['text']
        nodes[e['path']] = node
    return Tree(nodes)


def join_rel(parent, name):
    return parent + '/' + name if parent else name


# ------------------------------------------------------------------ the cost model (mirrors discovery_walk.rs)

class Model:
    """The abstract walk. `cost` is (objects, edges); `observed` is the scope (rel paths of present observed entries)."""

    def __init__(self, c, rule, tree, source, roots):
        self.c, self.rule, self.t = c, rule, tree
        self.automatic = source == 'automatic'
        self.source, self.roots = source, roots
        self.objects = 0
        self.edges = 0
        self.observed = {''}
        self.listed = set()
        self.verdicts = set()
        self.counts = dict(listedDirectories=0, listedNames=0, visitedChildDirectories=0, prunedAnchors=0, openedDirectories=0,
                           boundaries=0, cargoRoots=0, judgedDirectories=0, markerCaptures=0, captures=0, depthLimitDirectories=0,
                           gitdirReads=0)

    def add(self, cost, times=1):
        self.objects += cost[0] * times
        self.edges += cost[1] * times

    def owned(self):
        self.add(self.c['OWNED'])

    def capture(self):
        # CAP, then the dearer of `owned(count*K)` (1, 0) and the filesystem premise FS (1, 2): an upper bound.
        self.counts['captures'] += 1
        self.add(self.c['CAP'])
        self.add(max(self.c['OWNED'], self.c['FS']))

    def observe(self, rel):
        """`observe` (351-387): the charged by-name observation, and the scope entry when new and present."""
        self.add(self.c['OBS'])
        if self.t.node(rel) is not None and rel not in self.observed:
            self.owned()
            self.observed.add(rel)

    def is_file(self, rel):
        return self.t.kind(rel) == 'file'

    def gitdir(self, rel):
        """`gitdir_target` (project_admission.rs:555-635) at its dearer branch: open, status, capture with the premise,
        the uninterrupted read envelope, status, and a parsed target."""
        self.counts['gitdirReads'] += 1
        self.add(self.c['OPEN_REG_1'])
        self.add(self.c['ADMISSION_STATUS'])
        self.counts['captures'] += 1
        self.add(self.c['CAP'])
        self.add(self.c['FS'])
        self.add(read_envelope(self.c, self.t.node(rel)['size']))
        self.add(self.c['ADMISSION_STATUS'])
        self.add(self.c['GITDIR_TARGET'])

    def vcs_probe(self, rel):
        """`vcs_evidence` (project_admission.rs:518-540): observations without scope entries, to the first present."""
        for marker in ('.git', '.hg', '.svn', '.jj'):
            self.add(self.c['OBS'])
            m = join_rel(rel, marker)
            kind = self.t.kind(m)
            if kind is None:
                continue
            if kind == 'file' and marker == '.git':
                self.gitdir(m)
            return True
        return False

    def directory_passes(self, rel):
        """`directory_passes` (499-517), memoized; every judgment captures and passes (the dearer branch)."""
        if rel in self.verdicts:
            return True
        self.counts['judgedDirectories'] += 1
        self.capture()
        self.owned()
        self.verdicts.add(rel)
        return True

    def capture_markers(self, rel):
        """`capture_markers` (525-565): four spellings; each present regular marker opened, sampled and captured."""
        for marker in self.rule.WORKSPACE_MARKERS:
            self.owned()
            m = join_rel(rel, marker)
            if not self.is_file(m):
                continue
            self.counts['markerCaptures'] += 1
            self.add(self.c['OPEN_REG_1'])
            self.add(self.c['STATUS'])
            self.capture()

    def list(self, rel):
        """`list` (608-658): the listing, each raw name (with `.` and `..`), each listed name."""
        names = self.t.children.get(rel, [])
        self.counts['listedDirectories'] += 1
        self.counts['listedNames'] += len(names)
        self.add(self.c['LISTING'])
        self.add(self.c['RAW_NAME'], len(names) + 2)
        self.add(self.c['LISTED_NAME'], len(names))
        return names

    def enter(self, ancestors, rel, known):
        """`enter` (666-733). Returns the level or None when already listed."""
        if rel in self.listed:
            return None
        self.owned()
        self.listed.add(rel)
        names = self.list(rel)
        for name in names:
            self.owned()  # spell
            self.observe(join_rel(rel, name))
            self.owned()  # the (name, observation) slot
        if rel == '':
            # `listed_vcs` (570-601): only a regular `.git` file costs (the `gitdir` read).
            for marker in ('.git', '.hg', '.svn', '.jj'):
                m = join_rel(rel, marker)
                kind = self.t.kind(m)
                if kind is None:
                    continue
                if kind == 'file' and marker == '.git':
                    self.gitdir(m)
                break
        pushed = self.is_file(join_rel(rel, 'Cargo.toml')) and rel not in known
        if pushed:
            self.counts['cargoRoots'] += 1
            self.owned()
            known.add(rel)
        if self.automatic and any(self.is_file(join_rel(rel, m)) for m in self.rule.WORKSPACE_MARKERS):
            for level in ancestors[1:]:
                self.directory_passes(level['rel'])
            if rel != '':
                self.directory_passes(rel)
            self.capture_markers(rel)
        depth = 0 if rel == '' else len(rel.split('/'))
        return dict(rel=rel, depth=depth, names=names, next=0, pushed=pushed)

    def classify(self, rel):
        targets = sum(1 for part in rel.split('/') if part == 'target')
        base = self.c['CLASSIFY_BASE']
        self.add((base[0] + targets, base[1]))

    def subtree(self, start, known):
        """`subtree` (739-824), with the levels on an explicit stack."""
        maxd = self.c['MAX_LISTED_DEPTH']
        if start != '' and len(start.split('/')) > maxd:
            for marker in self.rule.WORKSPACE_MARKERS:
                self.owned()
                self.observe(join_rel(start, marker))
            return
        levels = []
        level = self.enter(levels, start, known)
        if level is not None:
            levels.append(level)
        while levels:
            top = levels[-1]
            if top['next'] == len(top['names']):
                done = levels.pop()
                if done['pushed']:
                    known.discard(done['rel'])
                continue
            name = top['names'][top['next']]
            top['next'] += 1
            child = join_rel(top['rel'], name)
            if self.t.kind(child) != 'dir':
                continue
            self.counts['visitedChildDirectories'] += 1
            self.classify(child)
            if self.rule.classify_path(child, set(known), ()) is not None:
                self.counts['prunedAnchors'] += 1
                continue
            self.owned()  # spell
            self.counts['openedDirectories'] += 1
            self.add(self.c['OPEN_DIR'])
            self.add(self.c['STATUS'])
            if top['depth'] + 1 > maxd:
                self.counts['depthLimitDirectories'] += 1
                for marker in self.rule.WORKSPACE_MARKERS:
                    self.owned()
                    self.observe(join_rel(child, marker))
                continue
            vcs = self.vcs_probe(child)
            self.owned()  # the config spelling
            config = join_rel(child, 'opensip.json')
            self.observe(config)
            if vcs or self.is_file(config):
                self.counts['boundaries'] += 1
                continue
            self.owned()
            level = self.enter(levels, child, known)
            if level is not None:
                levels.append(level)

    def named_root(self, rel, judge):
        """`named_root` (837-960)."""
        self.owned()
        known = set()
        self.owned()
        self.observe('Cargo.toml')
        self.owned()
        self.observe('opensip.json')
        if self.is_file('Cargo.toml'):
            self.owned()
            known.add('')
        chain = ['']
        ended = 'reached'
        if rel:
            for part in rel.split('/'):
                parent = chain[-1]
                self.owned()  # spell
                self.owned()  # the sub path
                sub = join_rel(parent, part)
                self.observe(sub)
                if self.t.kind(sub) != 'dir':
                    ended = 'not-directory'
                    break
                self.classify(sub)
                if self.rule.classify_path(sub, set(known), ()) is not None:
                    ended = 'refused'
                    break
                self.add(self.c['OPEN_DIR'])
                self.add(self.c['STATUS'])
                self.owned()
                self.observe(join_rel(sub, 'Cargo.toml'))
                self.owned()
                config = join_rel(sub, 'opensip.json')
                self.observe(config)
                vcs = self.vcs_probe(sub)
                if vcs or self.is_file(config):
                    ended = 'refused'
                    break
                if self.is_file(join_rel(sub, 'Cargo.toml')):
                    self.owned()
                    known.add(sub)
                chain.append(sub)
        if judge and rel and ended != 'refused':
            self.classify(rel)
            if self.rule.classify_path(rel, set(known), ()) is not None:
                ended = 'refused'
        continues = judge
        if judge:
            if ended == 'refused':
                continues = False
            else:
                judged = [0] if not rel else list(range(1, len(chain)))
                for index in judged:
                    self.directory_passes(chain[index])
                if ended == 'reached':
                    start = chain[-1]
                    for marker in self.rule.WORKSPACE_MARKERS:
                        self.owned()
                        self.observe(join_rel(start, marker))
                    self.capture_markers(start)
                continues = ended == 'reached'
        if ended == 'reached':
            self.subtree(chain[-1], set(known))
        return continues

    def walk(self):
        """`walk` (975-1053)."""
        self.owned()
        self.owned()
        self.add(self.c['STATUS'])
        self.owned()  # the root's scope entry
        if self.automatic:
            self.owned()
            self.subtree('', set())
        else:
            judge = len(self.roots) <= self.c['MAX_WORKSPACE_UNITS']
            seen = set()
            for spec in self.roots:
                self.owned()
                try:
                    rel = self.rule.normalize_explicit_root(spec)
                except (self.rule.RootGrammarError, TypeError):
                    judge = False
                    continue
                if rel in seen:
                    continue
                self.owned()
                seen.add(rel)
                judge = self.named_root(rel, judge)
        return self


def model(c, rule, tree, source='automatic', roots=()):
    return Model(c, rule, tree, source, list(roots)).walk()


# ------------------------------------------------------------------ the reference population (LD-B2B4-1)

def reference_population(wv, ref, slm, rule, tree, source='automatic', roots=()):
    fs = {'/': dict(kind='dir', uid=0, gid=0, mode='0755', dev=1), HOME: dict(kind='dir', uid=1000, gid=50, mode='0700', dev=1),
          ROOT: dict(kind='dir', uid=1000, gid=50, mode='0755', dev=1)}
    for rel, node in tree.nodes.items():
        if not rel:
            continue
        row = dict(kind=node['kind'], uid=1000, gid=50, mode='0755' if node['kind'] == 'dir' else '0644', dev=1)
        if node['kind'] == 'file':
            row['nlink'] = 1
            row['size'] = node['size']
        fs[ROOT + '/' + rel] = row
    for rel, node in tree.nodes.items():
        if node['kind'] != 'dir':
            continue
        for marker in wv.MARKERS:
            m = tree.node(join_rel(rel, marker))
            if m is None:
                continue
            fs[ROOT + ('/' + rel if rel else '')]['vcs'] = True if m['kind'] == 'dir' else dict(kind='indirection', target=None)
            break
    inp = dict(invokingUid=1000, accountHome=HOME, cwd=HOME, fs=fs, explicitProject=ROOT, prunedTreeMarkerInventory='not-enumerated')
    if source == 'explicit-joins':
        inp['explicitJoins'] = list(roots)
    elif source == 'config-workspace-roots':
        inp['configWorkspaceRoots'] = list(roots)
    population = ref.walker_population(rule, inp, ROOT, source)['fs']
    return {('' if p == ROOT else p[len(ROOT) + 1:]) for p in population if p == ROOT or p.startswith(ROOT + '/')}


def checked_model(c, wv, ref, slm, rule, tree, label, source='automatic', roots=()):
    m = model(c, rule, tree, source, roots)
    expected = reference_population(wv, ref, slm, rule, tree, source, roots)
    require(m.observed == expected, 'model population differs from the reference: %s (%d extra, %d missing)'
            % (label, len(m.observed - expected), len(expected - m.observed)))
    return m


# ------------------------------------------------------------------ integrity (plan r2 section 1.1)

STORE_DIR_MODE = 0o555
STORE_FILE_MODES = {0o444: '100644', 0o555: '100755'}


def git_blob(data):
    return hashlib.sha1(b'blob %d\0' % len(data) + data).digest()


def verified_tree(root, entry):
    """Re-verify a store against its pinned `gitTree` and QD-22 `treeDigest`, no-follow, and return its Tree."""
    gitlinks = {g['path']: g['commit'] for g in entry['submodulePolicy']['gitlinks']}
    nodes = {'': dict(kind='dir')}
    blobs = []  # QD-22 rows: [path, mode, sha256]

    def visit(rel):
        here = os.path.join(root, rel) if rel else root
        st = os.lstat(here)
        require(stat.S_ISDIR(st.st_mode) and stat.S_IMODE(st.st_mode) == STORE_DIR_MODE, 'store directory mode: ' + (rel or '.'))
        rows = []
        with os.scandir(here) as it:
            names = sorted(e.name for e in it)
        for name in names:
            child = join_rel(rel, name)
            require(name != '.git', 'a .git path component in a T2 tree: ' + child)
            path = os.path.join(here, name)
            st = os.lstat(path)
            if child in gitlinks:
                # r2 (Codex B2B4A-R1-RF-2): a placeholder is a store directory too, 0555, and empty.
                require(stat.S_ISDIR(st.st_mode) and stat.S_IMODE(st.st_mode) == STORE_DIR_MODE and not os.listdir(path),
                        'gitlink placeholder is not an empty 0555 directory: ' + child)
                nodes[child] = dict(kind='dir')
                rows.append((b'160000', name.encode(), bytes.fromhex(gitlinks[child]), False))
            elif stat.S_ISLNK(st.st_mode):
                data = os.fsencode(os.readlink(path))
                nodes[child] = dict(kind='symlink')
                rows.append((b'120000', name.encode(), git_blob(data), False))
                blobs.append([child, '120000', sha256(data)])
            elif stat.S_ISREG(st.st_mode):
                mode = STORE_FILE_MODES.get(stat.S_IMODE(st.st_mode))
                require(mode is not None and st.st_nlink == 1, 'store file mode or links: ' + child)
                with open(path, 'rb') as f:
                    data = f.read()
                nodes[child] = dict(kind='file', size=len(data))
                rows.append((mode.encode(), name.encode(), git_blob(data), False))
                blobs.append([child, mode, sha256(data)])
            elif stat.S_ISDIR(st.st_mode):
                nodes[child] = dict(kind='dir')
                rows.append((b'40000', name.encode(), bytes.fromhex(visit(child)), True))
            else:
                raise ValueError('non-regular object in a store: ' + child)
        rows.sort(key=lambda r: r[1] + (b'/' if r[3] else b''))
        body = b''.join(m + b' ' + n + b'\0' + h for m, n, h, _ in rows)
        return hashlib.sha1(b'tree %d\0' % len(body) + body).hexdigest()

    got_tree = visit('')
    require(got_tree == entry['gitTree'], 'gitTree mismatch: ' + entry['id'])
    blobs.sort(key=lambda r: r[0].encode())
    digest = sha256(json.dumps(blobs, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode())
    require(digest == entry['treeDigest']['value'] and len(blobs) == entry['treeDigest']['blobEntries'], 'treeDigest mismatch: ' + entry['id'])
    return Tree(nodes)


def store_path(store, entry):
    """The only join of a digest to the store: refuses a held-out entry before any filesystem call."""
    require(entry.get('heldOut') is False, 'held-out entries are never opened: ' + str(entry.get('id')))
    return os.path.join(store, entry['treeDigest']['value'])


# ------------------------------------------------------------------ workspaces (plan r2 section 1.5)

def compose(root_tree, members):
    """The composed checkout: the overlay root's own non-symlink entries, each member tree mounted as an ordinary
    directory at its mount name."""
    nodes = dict(root_tree.nodes)
    for mount, tree in members:
        require(mount not in nodes, 'a member mount collides with an overlay entry: ' + mount)
        for rel, node in tree.nodes.items():
            nodes[join_rel(mount, rel) if rel else mount] = node
    return Tree(nodes)


OVERLAYS = 'docs/implementation/m3/corpus/t2-acquisition-2026-10-06-r1/overlays'


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def verified_workspace(cache, arch, store, ws, manifest, trees):
    """r2 (Codex B2B4A-R1-RF-1): the overlay as FETCH-SPEC section 2 writes it. Its record is the manifest's canonical
    `overlay`, its SHA-256 is `overlayDigest`, and it equals the archived acquisition copy. Its mounts are exactly the
    record's, each linked to its own pinned lead-readable store through `store_path`. Returns the root tree and the
    members in mount order."""
    overlay = os.path.join(cache, 'workspaces', ws['id'])
    root_tree, mounts = overlay_root_tree(overlay)
    record = os.path.join(overlay, 'workspace-overlay.json')
    require(stat.S_ISREG(os.lstat(record).st_mode), 'the overlay record is not a regular file: ' + ws['id'])
    with open(record, 'rb') as fh:
        raw = fh.read()
    require(raw == canonical(ws['overlay']) and sha256(raw) == ws['overlayDigest'] and raw == (arch / OVERLAYS / ws['id'] / 'workspace-overlay.json').read_bytes(),
            'the overlay record differs from its pins: ' + ws['id'])
    pinned = {m['mount']: m for m in ws['overlay']['members']}
    require(sorted(mounts) == sorted(pinned), 'the overlay mounts differ from its record: ' + ws['id'])
    by_id = {e['id']: e for e in manifest['repositories']}
    members = []
    for mount in sorted(mounts):
        m = pinned[mount]
        entry = by_id[m['entry']]
        require(m['entry'] in ws['memberIds'] and entry['treeDigest']['value'] == m['treeDigest'], 'an overlay member differs from the manifest: ' + mount)
        require(os.readlink(os.path.join(overlay, mount)) == store_path(store, entry), 'an overlay mount links elsewhere: ' + mount)
        members.append((mount, trees[entry['id']]))
    require(sorted(pinned[x]['entry'] for x in mounts) == sorted(ws['memberIds']), 'workspace members differ from the manifest: ' + ws['id'])
    return root_tree, members, raw


def workspace_cost(c, wv, ref, slm, rule, root_tree, members, label):
    return checked_model(c, wv, ref, slm, rule, compose(root_tree, members), label)


def overlay_root_tree(path):
    """The overlay root's own entries, no-follow; member symlinks are skipped (they are mounted by `compose`)."""
    root = os.lstat(path)
    require(stat.S_ISDIR(root.st_mode), 'the overlay root is not a directory: ' + path)  # r2: never a symlink
    nodes = {'': dict(kind='dir')}
    mounts = []

    def visit(rel):
        here = os.path.join(path, rel) if rel else path
        with os.scandir(here) as it:
            names = sorted(e.name for e in it)
        for name in names:
            child = join_rel(rel, name)
            st = os.lstat(os.path.join(here, name))
            if stat.S_ISLNK(st.st_mode):
                require(rel == '', 'a symlink below the overlay root: ' + child)
                mounts.append(name)
            elif stat.S_ISDIR(st.st_mode):
                nodes[child] = dict(kind='dir')
                visit(child)
            elif stat.S_ISREG(st.st_mode):
                nodes[child] = dict(kind='file', size=st.st_size)
            else:
                raise ValueError('non-regular overlay object: ' + child)

    visit('')
    return Tree(nodes), mounts


# ------------------------------------------------------------------ composed-workspace vectors (native soundness)

def d(path):
    return dict(path=path, kind='dir', mode='0755')


def f(path, text='{}'):
    return dict(path=path, kind='file', mode='0644', text=text)


def composed_vectors():
    """Synthetic workspaces whose members are nested trees (plan r2, RF-1). Each is (id, overlay entries, members);
    a member is (mount, entries). The native test materializes the composed tree."""
    unit_a = [f('Cargo.toml', '[package]\n'), d('src'), f('src/lib.rs', '')]
    unit_b = [f('package.json'), d('lib'), f('lib/index.js', '')]
    nested = [f('Cargo.toml', '[workspace]\n'), d('crates'), d('crates/x'), f('crates/x/Cargo.toml', '[package]\n'), d('crates/x/src'),
              f('crates/x/src/lib.rs', '')]
    boundary = [f('opensip.json'), d('inner'), f('inner/Cargo.toml', '[package]\n')]
    vcs = [d('.git'), f('.git/HEAD', 'ref: refs/heads/main\n'), f('package.json')]
    pruned = [f('package.json'), d('node_modules'), d('node_modules/m'), f('node_modules/m/package.json'), d('target'), f('target/x', '')]
    deep = []
    path = ''
    for i in range(252):
        path = join_rel(path, 'd')
        deep.append(d(path))
    deep.append(f(path + '/Cargo.toml', '[package]\n'))
    return [
        ('ws-units', [f('Cargo.toml', '[workspace]\n')], [('a', unit_a), ('b', unit_b), ('n', nested)]),
        ('ws-boundary-and-vcs-members', [f('package.json')], [('a', unit_a), ('c', boundary), ('g', vcs)]),
        ('ws-pruned-member-segments', [d('.cargo'), f('.cargo/config.toml', '')], [('p', pruned), ('b', unit_b)]),
        ('ws-deep-member', [f('Cargo.toml', '[workspace]\n')], [('a', unit_a), ('z', deep)]),
    ]


def vector_tree(entries):
    return Tree({'': dict(kind='dir'), **{e['path']: (dict(kind='file', size=len(e['text'].encode()), text=e['text']) if e['kind'] == 'file'
                                                     else dict(kind=e['kind'])) for e in entries}})


def composed_entries(overlay, members):
    out = list(overlay)
    for mount, entries in members:
        out.append(d(mount))
        out.extend(dict(e, path=mount + '/' + e['path']) for e in entries)
    return out


# ------------------------------------------------------------------ outputs

def load_reference(product, arch, packages_root):
    spec = importlib.util.spec_from_file_location('discovery_walk_vectors', product / WALK_TOOL)
    wv = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(wv)
    wv.packages(product, packages_root)
    for row in wv.ARCH:
        wv.pinned(arch, *row)
    ref = wv.load('discovery_scan_reference', arch / wv.ARCH[0][0])
    slm, rule = ref.load(arch)
    return wv, ref, slm, rule


def prediction(m):
    return dict(objects=m.objects, edges=m.edges)


def vectors_output(product, c, wv, ref, slm, rule):
    walk = json.loads((product / WALK_VECTORS).read_bytes())
    rows = []
    for case in walk['cases']:
        tree = tree_of_vector(case)
        m = checked_model(c, wv, ref, slm, rule, tree, case['id'], case['source'], case['roots'])
        rows.append(dict(id=case['id'], **prediction(m)))
    composed = []
    for id_, overlay, members in composed_vectors():
        m = workspace_cost(c, wv, ref, slm, rule, vector_tree(overlay), [(mount, vector_tree(e)) for mount, e in members], id_)
        composed.append(dict(id=id_, source='automatic', roots=[], tree=composed_entries(overlay, members), **prediction(m)))
    body = {'schemaVersion': 1,
            'standing': 'The B2-b4a cost model\'s objects-and-edges predictions for the accepted walk vectors and the composed-workspace '
                        'vectors (B2-b4 plan r2 section 1.4). Generated by tools/security/discovery_census.py; the security tests assert '
                        'the native walker uses no more. Design evidence, not product qualification.',
            'walkVectors': pin_row(product, WALK_VECTORS),
            'closure': [pin_row(product, p) for p, _, _ in CLOSURE],
            'walkCases': rows,
            'composedCases': composed}
    return (json.dumps(body, separators=(',', ':'), ensure_ascii=True) + '\n').encode()


def census_output(product, arch, cache, c, wv, ref, slm, rule):
    manifest_raw = (arch / MANIFEST).read_bytes()
    manifest = json.loads(manifest_raw)
    store = os.path.join(cache, 'store')
    limits = c['LIMITS']
    entries, trees = [], {}
    for entry in manifest['repositories']:
        if entry['heldOut'] is not False:
            entries.append(dict(id=entry['id'], status='outstanding: held-out'))
            continue
        tree = verified_tree(store_path(store, entry), entry)
        trees[entry['id']] = tree
        m = checked_model(c, wv, ref, slm, rule, tree, entry['id'])
        entries.append(row(entry['id'], m, limits, gitTree=entry['gitTree'], treeDigest=entry['treeDigest']['value'], verified=True))
    workspaces = []
    for ws in manifest['workspaces']:
        if ws['heldOut'] is not False:
            workspaces.append(dict(id=ws['id'], status='outstanding: held-out'))
            continue
        root_tree, members, overlay_raw = verified_workspace(cache, arch, store, ws, manifest, trees)
        m = workspace_cost(c, wv, ref, slm, rule, root_tree, members, ws['id'])
        workspaces.append(row(ws['id'], m, limits, members=sorted(ws['memberIds']), overlayRecordSha256=sha256(overlay_raw)))
    failing = [e['id'] for e in entries + workspaces if e.get('passes2x') is False]
    body = {'schemaVersion': 1,
            'standing': 'The B2-b4a census of the T2 corpus against the discovery profile (M3-B r5 item 12; B2-b4 plan r2). Generated by '
                        'tools/security/discovery_census.py from integrity-verified stores; objects and edges are the cost model\'s upper '
                        'bound (the margin is structural: interrupted read retries are excluded). Held-out entries are outstanding and '
                        'never read. Design evidence, not product qualification.',
            'manifest': dict(path=MANIFEST, bytes=len(manifest_raw), sha256=sha256(manifest_raw)),
            'closure': [pin_row(product, p) for p, _, _ in CLOSURE],
            'limits': dict(objects=limits[0], edges=limits[1]),
            'margin': 2,
            'marginUnit': 'limit * 1000 // cost, floored (per mille); the margin holds at 2000 or more on both',
            'entries': entries,
            'workspaces': workspaces,
            'failingEntries': failing,
            'caps': 'returned-to-law' if failing else 'margin-holds-for-lead-readable-entries',
            'heldOutMargin': 'outstanding'}
    return (json.dumps(body, indent=1, ensure_ascii=True) + '\n').encode()


def row(id_, m, limits, **extra):
    return dict(id=id_, **extra, counts=m.counts, objects=m.objects, edges=m.edges,
                objectMarginPermille=limits[0] * 1000 // m.objects, edgeMarginPermille=limits[1] * 1000 // m.edges,
                passes2x=2 * m.objects <= limits[0] and 2 * m.edges <= limits[1])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true', help='compare the outputs without writing repository files')
    mode.add_argument('--write', action='store_true', help='regenerate the outputs')
    parser.add_argument('--architecture', type=Path, required=True, help='architecture checkout (manifest, reference)')
    parser.add_argument('--packages-root', type=Path, required=True, help='checkout holding the provisioned python-packages snapshot')
    parser.add_argument('--t2-cache', type=Path, help='the private durable T2 cache (store/ and workspaces/); omit for the vectors only')
    args = parser.parse_args()
    product = Path(__file__).resolve().parent.parent.parent
    arch = args.architecture.resolve(strict=True)
    c = costs(product)
    wv, ref, slm, rule = load_reference(product, arch, args.packages_root.resolve(strict=True))
    outputs = [(OUTPUT_VECTORS, vectors_output(product, c, wv, ref, slm, rule))]
    if args.t2_cache is not None:
        outputs.append((OUTPUT_CENSUS, census_output(product, arch, str(args.t2_cache.resolve(strict=True)), c, wv, ref, slm, rule)))
    for path, raw in outputs:
        target = product / path
        if args.check:
            require(target.is_file() and target.read_bytes() == raw, 'output differs: ' + path)
        else:
            target.write_bytes(raw)
        print(('Verified ' if args.check else 'Generated ') + path)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, TypeError, OSError) as error:
        print(f'Discovery census failed: {error}', file=sys.stderr)
        raise SystemExit(1)
