"""The T2 discovery census and its cost model (M3-B r5 item 12; unit B2-b4a, B2-b4 plan r2).

Developer tool only. It writes or checks two generated files, and in its blind mode writes a third:
  * crates/security/src/custody/discovery_census_vectors.json: the cost model's objects-and-edges prediction for every
    accepted walk vector (tools/security/discovery_walk_vectors.py) and for the composed-workspace vectors below. The
    security test suite walks each natively on a fresh discovery ledger and asserts the walker used no more
    (discovery_census_tests.rs, the soundness control).
  * crates/security/src/custody/discovery_census.json: the census of every lead-readable T2 entry, and every workspace
    as a composed checkout, with the modeled objects and edges against the discovery profile's limits. The ten
    held-out entries are never opened here: their rows are composed from the blind receipt below when it is valid and
    bound to the current inputs, are `outstanding: held-out (blind receipt stale)` when it is bound to other inputs,
    and are `outstanding: held-out` when there is none.
  * crates/security/src/custody/discovery_census_held_out.json (--held-out-blind only; unit B2-b4c, plan r6 section
    2.5): the blind receipt. Each held-out store is integrity-checked and measured with the same model, population
    check and caps, and the receipt holds per entry only its id, its verdicts and its per-mille margins, or one error
    class. No exception, path or name is printed or stored; stdout carries one line of counts.

The cost model is an abstract walk that mirrors custody/discovery_walk.rs step for step and adds each charge the walker
makes. Its constants are read from the code by anchored matches, and every file of the transitive cost closure is pinned
whole: any change to any of them refuses the census (plan r2, RF-3). Unknowns are charged at their dearer branch: every
judged directory and every present regular marker is captured, every capture takes the filesystem branch, every
listing returns `.` and `..`, every chain passes, and a regular `.git` file is read at its uninterrupted envelope.
Interrupted read retries are excluded: the margin is structural (plan r2, RF-2).

Bytes (unit B2-b4b1, plan r4 section 2.1): each charge's byte formula is modeled too, as an affine function of the
root spelling's length R (bytes = base + perRootByte * R), with every compile-time size the formulas name taken from a
closed inventory that the security and platform tests assert against the build. The census reports bytes at three root
lengths and claims no byte margin. The B2-b4a probe cross-check is retired (that probe walked the walker before its
storage redesign); a lead probe of the redesigned walker is archived separately as supporting evidence (unit B2-b3d).

The population is the bound B2-b0 reference's (contract successor 164): every walk this tool models is compared with
`walker_population` over the same tree, and a difference refuses (LD-B2B4-1).

Integrity (plan r2 section 1.1): each store is re-verified before counting. The Git tree object and the QD-22 tree
digest are recomputed from the stored bytes with no-follow traversal; any extra object, any mode other than the
store's, any non-regular object and any `.git` path component refuses. Outside the blind mode, held-out entries are
read from the manifest by id and flag only, and their digests are never joined to a store path. No network, repository code, subprocess or
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
    ('crates/security/src/custody/discovery_walk.rs', 48217, '7bc4ed36e4563747700e4395b421c7425ef9dba7519763942f73c89d5077bba0'),
    ('crates/security/src/custody/project_admission.rs', 77277, 'd9856dbc56eabddb20b2468fccf3199f46ce28d80b4c46d838cbdecf25d140ce'),
    ('crates/security/src/custody/project_chain.rs', 32761, '3a824290da7697001871d20b7b0eb6339085d9cd7ef0ccab786cf54e3dd0b53c'),
    ('crates/security/src/trust/initial_platform.rs', 21613, '227d35a35b58b06002bcaa21c490ce8d5d28474000427c16adafe8e84616aa94'),
    ('crates/security/src/custody/discovery_scan.rs', 30776, '2cf59bfa15ec67fd8df6a63d51b8f3ecfdb96582a9fff8d47943a72a38b5e69e'),
    ('crates/security/src/custody/discovery_rule.rs', 18080, 'e3e3ef60293c825befcc024cd0a21e60e2b25d71444d66ab18f30d5a92bc20c2'),
    ('crates/security/src/custody.rs', 75787, 'bc2bfe98ee588760c5cc4beace666b9c5f88e02d7a5a58b65a225cf320f8b58b'),
    ('crates/platform/src/filesystem/directory_open.rs', 25442, '71ca33594e1775d9e1bbe2deba15ba4a38bd9ad2c528772a0842c63e3d1cc62a'),
    ('crates/platform/src/filesystem/path_binding.rs', 33600, 'a005d378507857a2d9bc4e56affb5e04b7cbd989bc9b2d423a9834c92e6b8a93'),
    ('crates/platform/src/filesystem.rs', 103566, '1c3831111ff782dff6841867d08e7fbc890e42580201fd0ba44410a36ad19162'),
    ('crates/platform/src/filesystem/descriptor_acl_capture.rs', 37140, '4113175351bca052d9e8bde9cc3cfe80c21527ff5316cccf9942f0b5f1f8ee02'),
    ('crates/platform/src/filesystem/descriptor_filesystem.rs', 14405, 'b8366f529958eab65f4125bba5bb75212038d899d320536fb4107f60eab79460'),
    ('crates/platform/src/filesystem/directory_entries.rs', 21695, '72824def6fa0fa4432304442ee68307c3e380d03d5e9949fb3ae94a02770c255'),
    ('crates/platform/src/work_reader.rs', 8590, '099df8356d750e4452682e264223fc492985b34eed007091ce5c26dcf10ec3b6'),
    ('crates/platform/src/work_ledger.rs', 34709, '46b78d8aab58b1e8bf4984530e5ee054ca30d8c1fe74daf2478c1a33f6ea6b7e'),
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
     r'const LISTING: WorkCost = WorkCost \{\n    objects: (\d+),\n    edges: (\d+),\n    bytes: (\d+),\n\};'),
    ('STATUS', 'crates/security/src/custody/discovery_walk.rs',
     r'const STATUS: WorkCost = WorkCost \{\n    objects: (\d+),\n    edges: (\d+),\n    bytes: (\d+),\n\};'),
    ('RECORD', 'crates/security/src/custody/discovery_walk.rs', r'\nconst RECORD: usize = (\d+);'),
    ('OWNED', 'crates/security/src/custody/discovery_walk.rs',
     r'fn owned\(bytes: usize\) -> WorkCost \{\n    WorkCost \{\n        objects: (\d+),\n        edges: (\d+),\n        bytes: bytes\.saturating_add\(RECORD\),\n'),
    ('CLASSIFY', 'crates/security/src/custody/discovery_walk.rs',
     r'fn classify_cost\(rel: &str\) -> WorkCost \{\n.*\n.*\n    WorkCost \{\n        objects: (\d+) \+ targets,\n        edges: (\d+),\n        bytes: segments\n            \.saturating_mul\((\d+) \* std::mem::size_of::<usize>\(\)\)\n            \.saturating_add\(rel\.len\(\)\.saturating_mul\(1 \+ targets\)\)\n            \.saturating_add\(\((\d+) \+ targets\)\.saturating_mul\(RECORD\)\),\n'),
    ('VISIT', 'crates/security/src/custody/discovery_walk.rs',
     r'const VISIT: WorkCost = WorkCost \{\n    objects: (\d+),\n    edges: (\d+),\n    bytes: (\d+),\n\};'),
    ('CONVERTED_NAME', 'crates/security/src/custody/discovery_walk.rs',
     r'work\.charge::<WalkRefusal>\(WorkCost \{\n            objects: (\d+),\n            edges: (\d+),\n            bytes: (\d+) \* \(parent_rel\.len\(\) \+ 1 \+ raw\.len\(\)\) \+ (\d+) \* RECORD,'),
    ('SCOPE_ENTRY', 'crates/security/src/custody/discovery_walk.rs',
     r'work\.charge::<WalkRefusal>\(owned\(\n                    rel\.len\(\) \+ std::mem::size_of::<ObservedEntry>\(\),\n                \)\)\?;()'),
    ('ROOT_ENTRY', 'crates/security/src/custody/discovery_walk.rs',
     r'work\.charge::<WalkRefusal>\(owned\(std::mem::size_of::<ObservedEntry>\(\)\)\)\?;()'),
    ('SLOT', 'crates/security/src/custody/discovery_walk.rs',
     r'work\.charge::<WalkRefusal>\(owned\(\n            paths\n                \.len\(\)\n                \.saturating_mul\(std::mem::size_of::<ChildObservation>\(\)\),\n        \)\)\?;()'),
    ('ACL_ENTRIES', 'crates/security/src/custody/discovery_walk.rs',
     r'count\.saturating_mul\(std::mem::size_of::<opensip_platform::CapturedAclEntry>\(\)\),()'),
    ('MAX_LISTED_DEPTH', 'crates/security/src/custody/discovery_walk.rs', r'const MAX_LISTED_DEPTH: usize = (\d+);'),
    ('GITDIR_TARGET', 'crates/security/src/custody/project_admission.rs',
     r'work\.run\(\n        WorkCost \{\n            objects: (\d+),\n            edges: (\d+),\n            bytes: target\.len\(\),'),
    ('ADMISSION_STATUS', 'crates/security/src/custody/project_admission.rs',
     r'\nconst STATUS: WorkCost = WorkCost \{\n    objects: (\d+),\n    edges: (\d+),\n    bytes: (\d+),\n'),
    ('MAX_CONFIG_BYTES', 'crates/security/src/custody.rs', r'const MAX_CONFIG_BYTES: u64 = (\d+) \* (\d+) \* (\d+);'),
    ('MAX_WORKSPACE_UNITS', 'crates/security/src/custody/discovery_rule.rs', r'pub\(crate\) const MAX_WORKSPACE_UNITS: usize = (\d+);'),
    ('STATUS_READ', 'crates/platform/src/filesystem/path_binding.rs',
     r'pub\(super\) fn status_read_cost\(\) -> crate::WorkCost \{\n    crate::WorkCost \{\n        objects: (\d+),\n        edges: (\d+),\n        bytes: std::mem::size_of::<libc::stat>\(\)\.max\(std::mem::size_of::<std::fs::Metadata>\(\)\),\n'),
    ('OPEN_DIR', 'crates/platform/src/filesystem/directory_open.rs',
     r'pub fn open_child_directory_cost\(name: &OsStr\) -> crate::WorkCost \{\n    let status = super::path_binding::status_read_cost\(\);\n    crate::WorkCost \{\n        objects: (\d+),\n        edges: (\d+) \+ status\.edges,\n        bytes: name\n            \.as_bytes\(\)\n            \.len\(\)\n            \.saturating_add\((\d+)\)\n            \.saturating_add\(status\.bytes\),\n'),
    ('OBS', 'crates/platform/src/filesystem/directory_open.rs',
     r'pub fn child_absence_observation_cost\(name: &OsStr\) -> crate::WorkCost \{\n    crate::WorkCost \{\n        objects: (\d+),\n        edges: (\d+),\n        bytes: name\n            \.as_bytes\(\)\n            \.len\(\)\n            \.saturating_add\((\d+)\)\n            \.saturating_add\(std::mem::size_of::<libc::stat>\(\)\),\n'),
    ('OPEN_REG', 'crates/platform/src/filesystem.rs',
     r'    pub fn open_regular_cost\(relative: &str\) -> crate::WorkCost \{\n        let components = relative\.split\(./.\)\.count\(\);\n        let status = path_binding::status_read_cost\(\);\n        crate::WorkCost \{\n            objects: (\d+)usize\.saturating_add\(components\.saturating_mul\((\d+)\)\),\n            edges: (\d+)usize\.saturating_add\(components\.saturating_mul\((\d+)\)\),\n            bytes: relative\n                \.len\(\)\n                \.saturating_add\(components\)\n                \.saturating_add\(status\.bytes\.saturating_mul\(components\)\),\n'),
    ('CAP', 'crates/platform/src/filesystem/descriptor_acl_capture.rs',
     r'pub fn descriptor_acl_capture_cost\(\) -> WorkCost \{\n    WorkCost \{\n        objects: (\d+),\n        edges: (\d+) \+ MAX_ENTRIES,\n        bytes: std::mem::size_of::<DescriptorAclCapture>\(\)\n            \+ BUFFER_BYTES\n            \+ (\d+) \* std::mem::size_of::<libc::stat>\(\)\n            \+ request_bytes\(\),\n'),
    ('REQUEST_BYTES', 'crates/platform/src/filesystem/descriptor_acl_capture.rs',
     r'#\[cfg\(target_os = "macos"\)\]\nconst fn request_bytes\(\) -> usize \{\n    std::mem::size_of::<libc::attrlist>\(\)\n\}()'),
    ('BUFFER_BYTES', 'crates/platform/src/filesystem/descriptor_acl_capture.rs', r'\nconst BUFFER_BYTES: usize = (\d+);'),
    ('MAX_ENTRIES', 'crates/platform/src/filesystem/descriptor_acl_capture.rs', r'\nconst MAX_ENTRIES: usize = (\d+);'),
    ('FS', 'crates/platform/src/filesystem/descriptor_filesystem.rs',
     r'pub fn descriptor_filesystem_observation_cost\(\) -> crate::WorkCost \{\n    #\[cfg\(target_os = "macos"\)\]\n    let statfs = std::mem::size_of::<libc::statfs>\(\);\n    #\[cfg\(not\(target_os = "macos"\)\)\]\n    let statfs = 0;\n    crate::WorkCost \{\n        objects: (\d+),\n        edges: (\d+),\n        bytes: statfs\n            \.saturating_add\(super::path_binding::status_read_cost\(\)\.bytes\)\n            \.saturating_add\(std::mem::size_of::<DescriptorFilesystem>\(\)\),\n'),
    ('READ_OBJECT', 'crates/platform/src/work_reader.rs',
     r'    let ceiling = max \+ 1;\n    charge\(WorkCost \{\n        objects: (\d+),\n        \.\.WorkCost::default\(\)\n    \}\)\?;'),
    ('READ_GROWTH_EDGE', 'crates/platform/src/work_reader.rs',
     r'            charge\(WorkCost \{\n                edges: (\d+),\n                bytes: next,\n'),
    ('READ_ATTEMPT_EDGE', 'crates/platform/src/work_reader.rs',
     r'        \} else \{\n            charge\(WorkCost \{\n                edges: (\d+),\n                \.\.WorkCost::default\(\)\n'),
    ('CHUNK', 'crates/platform/src/work_reader.rs', r'\nconst CHUNK: usize = (\d+);'),
    ('NEXT_BUFFER', 'crates/platform/src/work_reader.rs',
     r'fn next_buffer\(current: usize, ceiling: usize\) -> usize \{\n    \(if current == 0 \{ CHUNK \} else \{ current \* (\d+) \}\)\.min\(ceiling\)\n\}'),
    ('DISCOVERY_OBJECT_LIMIT', 'crates/platform/src/work_ledger.rs', r'const DISCOVERY_OBJECT_LIMIT: usize = 1 << (\d+);'),
    ('DISCOVERY_EDGE_LIMIT', 'crates/platform/src/work_ledger.rs', r'const DISCOVERY_EDGE_LIMIT: usize = 1 << (\d+);'),
    ('DISCOVERY_BYTE_LIMIT', 'crates/platform/src/work_ledger.rs', r'const DISCOVERY_BYTE_LIMIT: usize = 1 << (\d+);'),
)
# The compile-time sizes (aarch64-apple-darwin), by the exact operand text the anchored formulas name. Every operand
# an anchor names must be here (plan r4, RF-1), and the security and platform tests assert each equals `size_of` in the
# build (discovery_census_tests.rs, crates/platform/tests/discovery_census_sizes_tests.rs).
SIZES = {
    'usize': 8,
    'libc::stat': 144,
    'std::fs::Metadata': 144,
    'ObservedEntry': 128,
    'ChildObservation': 88,
    'opensip_platform::CapturedAclEntry': 16,
    'DescriptorAclCapture': 4384,
    'libc::attrlist': 24,
    'libc::statfs': 2168,
    'DescriptorFilesystem': 56,
}
SIZE_OF = re.compile(r'size_of::<(.+?)>\(\)')
# The root spelling lengths the census reports bytes at (plan r4 section 2.1): the lead probe's root, macOS PATH_MAX,
# and the code's bound on a project root spelling (path_binding.rs `components`).
ROOT_LENGTHS = (134, 1024, 4096)


def costs(product, sizes=None):
    """Verify the closure whole, then read every constant by its anchor. Every `size_of` operand an anchor names must
    be in the size inventory, or the census refuses."""
    sizes = SIZES if sizes is None else sizes
    for path, size, digest in CLOSURE:
        raw = (product / path).read_bytes()
        require(len(raw) == size and sha256(raw) == digest, 'cost closure changed: ' + path)
    out = {}
    for name, path, pattern in ANCHORS:
        text = (product / path).read_text()
        hits = list(re.finditer(pattern, text))
        require(len(hits) == 1, 'cost anchor %s matched %d times' % (name, len(hits)))
        for operand in SIZE_OF.findall(hits[0].group(0)):
            require(operand in sizes, 'cost anchor %s names an unpinned size: %s' % (name, operand))
        out[name] = tuple(int(g) for g in hits[0].groups() if g)
    z = sizes
    record = out['RECORD'][0]
    status_read_bytes = max(z['libc::stat'], z['std::fs::Metadata'])
    c = dict(RECORD=record, SIZES=dict(sizes))
    c['LISTING'] = out['LISTING'] + (0,)
    c['STATUS'] = out['STATUS'] + (0,)
    c['OWNED'] = out['OWNED']
    o, e, two, base = out['CLASSIFY']
    c['CLASSIFY'] = (o, e, two * z['usize'], base, record)  # objects o + t; bytes segs*(2*usize) + len*(1+t) + (base+t)*RECORD
    c['VISIT'] = out['VISIT']
    c['CONVERTED_NAME'] = out['CONVERTED_NAME']  # (o, e, 2, 2): the path and the validator's copy
    c['ENTRY'] = z['ObservedEntry']
    c['SLOT'] = z['ChildObservation']
    c['ACL_ENTRY'] = z['opensip_platform::CapturedAclEntry']
    c['MAX_LISTED_DEPTH'] = out['MAX_LISTED_DEPTH'][0]
    c['GITDIR_TARGET'] = out['GITDIR_TARGET']
    c['ADMISSION_STATUS'] = out['ADMISSION_STATUS'] + (0,)
    a, b, d = out['MAX_CONFIG_BYTES']
    c['MAX_CONFIG_BYTES'] = a * b * d
    c['MAX_WORKSPACE_UNITS'] = out['MAX_WORKSPACE_UNITS'][0]
    status_read = out['STATUS_READ']
    o, e, one = out['OPEN_DIR']
    c['OPEN_DIR'] = (o, e + status_read[1], one + status_read_bytes)  # + |name|
    o, e, one = out['OBS']
    c['OBS'] = (o, e, one + z['libc::stat'])  # + |name|
    o1, o2, e1, e2 = out['OPEN_REG']
    c['OPEN_REG_1'] = (o1 + o2, e1 + e2, 1 + status_read_bytes)  # one component: + |relative|
    o, e, two = out['CAP']
    c['MAX_ENTRIES'] = out['MAX_ENTRIES'][0]
    c['CAP'] = (o, e + c['MAX_ENTRIES'], z['DescriptorAclCapture'] + out['BUFFER_BYTES'][0] + two * z['libc::stat'] + z['libc::attrlist'], 0)
    o, e = out['FS']
    c['FS'] = (o, e, z['libc::statfs'] + status_read_bytes + z['DescriptorFilesystem'], 0)
    c['READ_OBJECT'] = out['READ_OBJECT'][0]
    require(out['READ_GROWTH_EDGE'][0] == out['READ_ATTEMPT_EDGE'][0], 'read attempts charge unequal edges')
    c['READ_ATTEMPT_EDGE'] = out['READ_ATTEMPT_EDGE'][0]
    c['CHUNK'] = out['CHUNK'][0]
    c['GROWTH'] = out['NEXT_BUFFER'][0]
    c['LIMITS'] = (1 << out['DISCOVERY_OBJECT_LIMIT'][0], 1 << out['DISCOVERY_EDGE_LIMIT'][0], 1 << out['DISCOVERY_BYTE_LIMIT'][0])
    return c


def read_envelope(c, length):
    """`read_charged` without interruption: one object; one edge per attempt, each either returning at least one byte
    or the final EOF, with the ceiling (max + 1) ending the loop, so attempts <= min(L, ceiling) + 1; and every buffer
    growth's full requested size in bytes, grown whenever the buffer fills, as `next_buffer` sizes it."""
    ceiling = c['MAX_CONFIG_BYTES'] + 1
    used = cap = grown = 0
    while used != ceiling:
        if used == cap:
            cap = min(c['CHUNK'] if cap == 0 else cap * c['GROWTH'], ceiling)
            grown += cap
        if used == length:
            break
        used = min(length, cap)
    return (c['READ_OBJECT'], c['READ_ATTEMPT_EDGE'] * (min(length, ceiling) + 1), grown, 0)


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

def blen(text):
    return len(text.encode())


class Model:
    """The abstract walk of the redesigned walker (unit B2-b3d, M3-B r6 item 12). A cost is (objects, edges, bytes,
    perRootByte): bytes are affine in the root spelling's length R, which the walker now keeps once. `observed` is the
    scope (root-relative paths of present observed entries)."""

    def __init__(self, c, rule, tree, source, roots):
        self.c, self.rule, self.t = c, rule, tree
        self.automatic = source == 'automatic'
        self.source, self.roots = source, roots
        self.objects = 0
        self.edges = 0
        self.bytes = 0
        self.per_root_byte = 0
        self.observed = {''}
        self.listed = set()
        self.verdicts = set()
        self.counts = dict(listedDirectories=0, listedNames=0, visitedChildDirectories=0, prunedAnchors=0, openedDirectories=0,
                           boundaries=0, cargoRoots=0, judgedDirectories=0, markerCaptures=0, captures=0, depthLimitDirectories=0,
                           gitdirReads=0)

    def add(self, cost, times=1):
        cost = tuple(cost) + (0,) * (4 - len(cost))
        self.objects += cost[0] * times
        self.edges += cost[1] * times
        self.bytes += cost[2] * times
        self.per_root_byte += cost[3] * times

    def owned(self, length=(0, 0)):
        """`owned(b)`: one record of b bytes plus RECORD."""
        o, e = self.c['OWNED']
        b, k = length if isinstance(length, tuple) else (length, 0)
        self.add((o, e, b + self.c['RECORD'], k))

    def key(self, rel, name):
        """`key`: a child's root-relative key, rel + 1 + name, owned (unit B2-b3d: no absolute spelling)."""
        self.owned(blen(rel) + 1 + blen(name))

    def capture(self):
        # CAP, then the dearer of `owned(count*K)` at its largest (MAX_ENTRIES entries) and the filesystem premise FS:
        # an upper bound in every dimension.
        self.counts['captures'] += 1
        self.add(self.c['CAP'])
        o, e = self.c['OWNED']
        acl = (o, e, self.c['MAX_ENTRIES'] * self.c['ACL_ENTRY'] + self.c['RECORD'], 0)
        self.add(tuple(max(x, y) for x, y in zip(acl, self.c['FS'])))

    def obs(self, name):
        o, e, b = self.c['OBS']
        self.add((o, e, b + blen(name), 0))

    def observe(self, rel):
        """`observe`: the charged by-name observation, and the scope entry (keyed by `rel`) when new and present."""
        name = rel.rsplit('/', 1)[-1]
        self.obs(name)
        if self.t.node(rel) is not None and rel not in self.observed:
            self.owned(blen(rel) + self.c['ENTRY'])
            self.observed.add(rel)

    def is_file(self, rel):
        return self.t.kind(rel) == 'file'

    def open_regular(self, name):
        o, e, b = self.c['OPEN_REG_1']
        self.add((o, e, b + blen(name), 0))

    def gitdir(self, rel):
        """`gitdir_target` (project_admission.rs) at its dearer branch: open, status, capture with the premise, the
        uninterrupted read envelope, status, and a parsed target as long as the file."""
        self.counts['gitdirReads'] += 1
        size = self.t.node(rel)['size']
        self.open_regular('.git')
        self.add(self.c['ADMISSION_STATUS'])
        self.counts['captures'] += 1
        self.add(self.c['CAP'])
        self.add(self.c['FS'])
        self.add(read_envelope(self.c, size))
        self.add(self.c['ADMISSION_STATUS'])
        o, e = self.c['GITDIR_TARGET']
        self.add((o, e, size, 0))

    def vcs_probe(self, rel):
        """`vcs_evidence` (project_admission.rs): observations without scope entries, to the first present."""
        for marker in ('.git', '.hg', '.svn', '.jj'):
            self.obs(marker)
            m = join_rel(rel, marker)
            kind = self.t.kind(m)
            if kind is None:
                continue
            if kind == 'file' and marker == '.git':
                self.gitdir(m)
            return True
        return False

    def directory_passes(self, rel):
        """`directory_passes`, memoized by root-relative path; every judgment captures and passes (the dearer branch)."""
        if rel in self.verdicts:
            return True
        self.counts['judgedDirectories'] += 1
        self.capture()
        self.owned(blen(rel))
        self.verdicts.add(rel)
        return True

    def capture_markers(self, rel):
        """`capture_markers`: four keys; each present regular marker opened, sampled and captured."""
        for marker in self.rule.WORKSPACE_MARKERS:
            self.key(rel, marker)
            m = join_rel(rel, marker)
            if not self.is_file(m):
                continue
            self.counts['markerCaptures'] += 1
            self.open_regular(marker)
            self.add(self.c['STATUS'])
            self.capture()

    def list(self, rel):
        """`list` with `ListingConversion` (unit B2-b3d): the listing; each raw entry's visit (with `.` and `..`); each
        other name converted to its one root-relative path with the validator's copy."""
        names = self.t.children.get(rel, [])
        self.counts['listedDirectories'] += 1
        self.counts['listedNames'] += len(names)
        self.add(self.c['LISTING'])
        self.add(self.c['VISIT'], len(names) + 2)
        o, e, two, records = self.c['CONVERTED_NAME']
        for name in names:
            self.add((o, e, two * (blen(rel) + 1 + blen(name)) + records * self.c['RECORD'], 0))
        return names

    def enter(self, ancestors, rel, known):
        """`enter`. Returns the level or None when already listed."""
        if rel in self.listed:
            return None
        self.owned(blen(rel))
        self.listed.add(rel)
        names = self.list(rel)
        self.owned(len(names) * self.c['SLOT'])  # the observation array, charged whole before it is reserved
        for name in names:
            self.observe(join_rel(rel, name))
        if rel == '':
            # `listed_vcs`: only a regular `.git` file costs (the `gitdir` read).
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
            self.owned(blen(rel))
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
        o, e, seg, base, record = self.c['CLASSIFY']
        parts = rel.split('/')
        targets = sum(1 for part in parts if part == 'target')
        self.add((o + targets, e, len(parts) * seg + blen(rel) * (1 + targets) + (base + targets) * record, 0))

    def open_directory(self, name):
        o, e, b = self.c['OPEN_DIR']
        self.add((o, e, b + blen(name), 0))
        self.add(self.c['STATUS'])

    def observe_markers(self, rel):
        """`observe_markers`: the four marker names of a directory past the depth policy, by key and observation."""
        for marker in self.rule.WORKSPACE_MARKERS:
            self.key(rel, marker)
            self.observe(join_rel(rel, marker))

    def subtree(self, start, known):
        """`subtree`, with the levels on an explicit stack."""
        maxd = self.c['MAX_LISTED_DEPTH']
        if start != '' and len(start.split('/')) > maxd:
            self.observe_markers(start)
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
            self.counts['openedDirectories'] += 1
            self.open_directory(name)
            if top['depth'] + 1 > maxd:
                self.counts['depthLimitDirectories'] += 1
                self.observe_markers(child)
                continue
            vcs = self.vcs_probe(child)
            self.key(child, 'opensip.json')
            config = join_rel(child, 'opensip.json')
            self.observe(config)
            if vcs or self.is_file(config):
                self.counts['boundaries'] += 1
                continue
            self.owned(0)  # the frame's own slot; its path moved in
            level = self.enter(levels, child, known)
            if level is not None:
                levels.append(level)

    def named_root(self, rel, judge):
        """`named_root`."""
        self.owned(0)  # the root frame's own slot
        known = set()
        self.key('', 'Cargo.toml')
        self.observe('Cargo.toml')
        self.key('', 'opensip.json')
        self.observe('opensip.json')
        if self.is_file('Cargo.toml'):
            self.owned(0)
            known.add('')
        chain = ['']
        ended = 'reached'
        if rel:
            for part in rel.split('/'):
                parent = chain[-1]
                self.key(parent, part)
                sub = join_rel(parent, part)
                self.observe(sub)
                if self.t.kind(sub) != 'dir':
                    ended = 'not-directory'
                    break
                self.classify(sub)
                if self.rule.classify_path(sub, set(known), ()) is not None:
                    ended = 'refused'
                    break
                self.open_directory(part)
                self.key(sub, 'Cargo.toml')
                self.observe(join_rel(sub, 'Cargo.toml'))
                self.key(sub, 'opensip.json')
                config = join_rel(sub, 'opensip.json')
                self.observe(config)
                vcs = self.vcs_probe(sub)
                if vcs or self.is_file(config):
                    ended = 'refused'
                    break
                if self.is_file(join_rel(sub, 'Cargo.toml')):
                    self.owned(blen(sub))
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
                    self.observe_markers(start)
                    self.capture_markers(start)
                continues = ended == 'reached'
        if ended == 'reached':
            self.subtree(chain[-1], set(known))
        return continues

    def walk(self):
        """`walk`: the root's spelling kept once (the one per-root-byte term), its scope entry keyed by `""`."""
        self.owned((0, 1))
        self.add(self.c['STATUS'])
        self.owned(self.c['ENTRY'])  # the root's scope entry
        if self.automatic:
            self.owned(0)  # the root frame's own slot
            self.subtree('', set())
        else:
            judge = len(self.roots) <= self.c['MAX_WORKSPACE_UNITS']
            seen = set()
            for spec in self.roots:
                self.owned(blen(spec))
                try:
                    rel = self.rule.normalize_explicit_root(spec)
                except (self.rule.RootGrammarError, TypeError):
                    judge = False
                    continue
                if rel in seen:
                    continue
                self.owned(blen(rel))
                seen.add(rel)
                judge = self.named_root(rel, judge)
        return self

    def bytes_at(self, root_length):
        return self.bytes + self.per_root_byte * root_length


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


# ------------------------------------------------------------------ the blind held-out census (unit B2-b4c; plan r6 section 2.5)

# The owner's decision (2026-10-16, owner-decisions/2026-10-16/HELD-OUT-T2-MARGIN.md): a held-out mode the lead runs
# without seeing contents, reporting only pass/fail and per-mille margins per entry, reviewed before and after the run.
OUTPUT_RECEIPT = 'crates/security/src/custody/discovery_census_held_out.json'
TOOL = 'tools/security/discovery_census.py'
ERROR_CLASSES = ('INTEGRITY', 'POPULATION', 'MODEL', 'IO')
# r2 (Codex B2B4C1-R1-RF-3): the code the population check executes, bound to the receipt too. The product helper that
# loads the reference and the generator closure that pins its packages; the reference, the SLM and rule it pins, and
# the foundation canonicalizer SLM imports by path (load_reference checks this is exactly what was loaded).
REFERENCE_PRODUCT = (WALK_TOOL, 'tools/contracts/generator-closure.json')
REFERENCE_ARCH = ('docs/implementation/m3/config-discovery-b/b2-b-reference/reference/discovery_scan_reference.py',
                  'docs/coop/design-corrections/security/security_lifecycle_model_v1.py',
                  'docs/implementation/m3/config-discovery-b/b2-a-reference/reference/discovery-defaults.sx1-r1.py',
                  'docs/coop/design-corrections/foundation/canonical.py')
MEASURED_KEYS = {'id', 'status', 'integrity', 'population', 'marginPermille', 'passes2x'}
ERROR_KEYS = {'id', 'status', 'errorClass'}
RECEIPT_KEYS = {'schemaVersion', 'standing', 'bindings', 'rows', 'state'}
_BLIND = object()


def held_out_store_path(store, entry, token):
    """The blind mode's only join of a held-out digest to the store. It refuses outside the mode and for any entry that
    is not held out; the ordinary `store_path` still refuses every held-out entry."""
    require(token is _BLIND, 'the held-out join is for the blind mode only')
    require(entry.get('heldOut') is True, 'the held-out join takes held-out entries only')
    return os.path.join(store, entry['treeDigest']['value'])


def receipt_bindings(product, arch, c):
    """The public pins a blind receipt is bound to: the manifest, this tool, the cost closure, the sizes, the caps as the
    code holds them, the root lengths, and the reference-loading code. Any drift makes the receipt stale."""
    manifest = (arch / MANIFEST).read_bytes()
    limits = c['LIMITS']
    return dict(manifest=dict(path=MANIFEST, bytes=len(manifest), sha256=sha256(manifest)), tool=pin_row(product, TOOL),
                closure=[pin_row(product, p) for p, _, _ in CLOSURE], sizes=dict(c['SIZES']),
                limits=dict(objects=limits[0], edges=limits[1], bytes=limits[2]), rootLengths=list(ROOT_LENGTHS),
                reference=[pin_row(product, p) for p in REFERENCE_PRODUCT] + [pin_row(arch, p) for p in REFERENCE_ARCH])


def held_out_ids(manifest):
    entries = manifest['repositories']
    require(all(e['heldOut'] in (True, False) for e in entries), 'a heldOut flag is not a boolean')
    return [e['id'] for e in entries if e['heldOut'] is True]


def blind_row(entry, store, c, measure):
    """One held-out entry, measured blind: a measured row, or an error row with its class only. Every exception is
    discarded unprinted. `measure(tree)` gives the model and the reference population."""
    def error(kind):
        return dict(id=entry['id'], status='error', errorClass=kind)
    try:
        tree = verified_tree(held_out_store_path(store, entry, _BLIND), entry)
    except OSError:
        return error('IO')
    except (Exception, SystemExit):  # noqa: BLE001 (reduced to its class; r2, Codex B2B4C1-R1-RF-2: an exit too)
        return error('INTEGRITY')
    try:
        m, expected = measure(tree)
    except OSError:
        return error('IO')
    except (Exception, SystemExit):  # noqa: BLE001
        return error('MODEL')
    if m.observed != expected:
        return error('POPULATION')
    try:
        limits = c['LIMITS']
        margins = dict(objects=limits[0] * 1000 // m.objects, edges=limits[1] * 1000 // m.edges,
                       bytes=limits[2] * 1000 // m.bytes_at(ROOT_LENGTHS[-1]))
    except (Exception, SystemExit):  # noqa: BLE001
        return error('MODEL')
    return dict(id=entry['id'], status='measured', integrity=True, population=True, marginPermille=margins,
                passes2x=all(v >= 2000 for v in margins.values()))


def receipt_state(rows):
    if any(r['status'] == 'error' for r in rows):
        return 'incomplete (blind census)'
    return 'holds (blind census)' if all(r['passes2x'] for r in rows) else 'fails (blind census)'


def blind_census(product, arch, cache, c, measure):
    manifest = json.loads((arch / MANIFEST).read_bytes())
    require(all(ws['heldOut'] is False for ws in manifest['workspaces']), 'a held-out workspace is outside the blind mode')
    store = os.path.join(cache, 'store')
    ids = held_out_ids(manifest)
    by_id = {e['id']: e for e in manifest['repositories']}
    require(ids, 'no held-out entries')
    rows = [blind_row(by_id[i], store, c, measure) for i in ids]
    body = {'schemaVersion': 1,
            'standing': 'The B2-b4c blind held-out receipt (plan r6 section 2.5; the owner decision of 2026-10-16): per held-out T2 '
                        'entry only its id, its integrity and population verdicts and its per-mille margins, or an error class. '
                        'Generated by tools/security/discovery_census.py --held-out-blind; no held-out content is emitted. Bound to '
                        'its inputs; any drift makes it stale.',
            'bindings': receipt_bindings(product, arch, c),
            'rows': rows,
            'state': receipt_state(rows)}
    return (json.dumps(body, indent=1, ensure_ascii=True) + '\n').encode(), rows


def run_blind(product, arch, cache, c, measure):
    """The blind run's only effects: the receipt, and one line of counts on stdout."""
    raw, rows = blind_census(product, arch, cache, c, measure)
    (product / OUTPUT_RECEIPT).write_bytes(raw)
    measured = [r for r in rows if r['status'] == 'measured']
    print('Blind held-out census: %d entries, %d measured, %d passing, %d errors.'
          % (len(rows), len(measured), sum(1 for r in measured if r['passes2x']), len(rows) - len(measured)))


def is_count(value):
    return isinstance(value, int) and not isinstance(value, bool) and value >= 0


def validated_receipt(receipt):
    """A receipt in the closed format (plan r6 section 2.5), its ids unique; returns its state. Coverage of the
    held-out ids is checked against the manifest it is bound to, by `compose_held_out`."""
    require(isinstance(receipt, dict) and set(receipt) == RECEIPT_KEYS and receipt['schemaVersion'] == 1, 'receipt shape')
    require(isinstance(receipt['bindings'], dict) and isinstance(receipt['standing'], str), 'receipt shape')
    rows = receipt['rows']
    require(isinstance(rows, list) and rows and all(isinstance(r, dict) and isinstance(r.get('id'), str) for r in rows), 'receipt rows')
    require(len({r['id'] for r in rows}) == len(rows), 'a receipt id is duplicated')
    for r in rows:
        if r.get('status') == 'measured':
            require(set(r) == MEASURED_KEYS and r['integrity'] is True and r['population'] is True, 'measured row shape: ' + r['id'])
            mp = r['marginPermille']
            require(isinstance(mp, dict) and set(mp) == {'objects', 'edges', 'bytes'} and all(is_count(v) for v in mp.values()),
                    'margins: ' + r['id'])
            require(r['passes2x'] is all(v >= 2000 for v in mp.values()), 'passes2x disagrees with the margins: ' + r['id'])
        elif r.get('status') == 'error':
            require(set(r) == ERROR_KEYS and r['errorClass'] in ERROR_CLASSES, 'error row shape: ' + r['id'])
        else:
            raise ValueError('receipt row status: ' + r['id'])
    require(receipt['state'] == receipt_state(rows), 'receipt state differs from its rows')
    return receipt['state']


def compose_held_out(manifest, receipt, current):
    """The census record's held-out rows and `heldOutMargin`, from the receipt only (never a held-out store). No receipt
    leaves them outstanding; an invalid one refuses; a receipt bound to other inputs is stale; a current one must cover
    exactly the manifest's held-out ids."""
    ids = held_out_ids(manifest)
    if receipt is None:
        return [dict(id=i, status='outstanding: held-out') for i in ids], 'outstanding'
    state = validated_receipt(receipt)
    if receipt['bindings'] != current:
        return [dict(id=i, status='outstanding: held-out (blind receipt stale)') for i in ids], 'outstanding'
    got = [r['id'] for r in receipt['rows']]
    require(len(got) == len(set(got)) and sorted(got) == sorted(ids), 'receipt coverage differs from the held-out entries')
    rows = {r['id']: r for r in receipt['rows']}
    return [dict(id=i, status='blind-census', result={k: v for k, v in rows[i].items() if k != 'id'}) for i in ids], state


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
    loaded = (wv.ARCH[0][0], ref.SLM[0], ref.RULE[0], Path(slm._cs.origin).resolve().relative_to(arch).as_posix())
    require(len(wv.ARCH) == 1 and loaded == REFERENCE_ARCH, 'the reference loads other files than the receipt binds')
    return wv, ref, slm, rule


def prediction(m):
    return dict(objects=m.objects, edges=m.edges, bytes=m.bytes, bytesPerRootByte=m.per_root_byte)


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
            'standing': 'The cost model\'s predictions for the accepted walk vectors and the composed-workspace vectors: objects, edges, '
                        'and bytes as bytes + bytesPerRootByte * R for a root spelled in R bytes (B2-b4 plan r2 section 1.4; plan r4 '
                        'section 2.1). Generated by tools/security/discovery_census.py; the security tests assert the native walker uses no '
                        'more. Design evidence, not product qualification.',
            'sizes': dict(c['SIZES']),
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
    receipt_path = product / OUTPUT_RECEIPT
    receipt = json.loads(receipt_path.read_bytes()) if receipt_path.is_file() else None
    held_rows, held_state = compose_held_out(manifest, receipt, receipt_bindings(product, arch, c))
    held_rows = {r['id']: r for r in held_rows}
    for entry in manifest['repositories']:
        if entry['heldOut'] is not False:
            entries.append(held_rows[entry['id']])
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
    # A composed blind row fails on its measured margins (plan r6 section 2.5); an error row is incomplete, not failing.
    failing = [e['id'] for e in entries + workspaces
               if e.get('passes2x') is False or (e.get('status') == 'blind-census' and e['result'].get('passes2x') is False)]
    for ws in workspaces:
        if 'objects' in ws:
            ws['fullLedgerMargin'] = 'outstanding: walker only until the B3-b member-observation bound (M3-B r6 item 12)'
    body = {'schemaVersion': 1,
            'standing': 'The B2-b4a census of the T2 corpus against the discovery profile (M3-B r5 item 12; B2-b4 plan r2). Generated by '
                        'tools/security/discovery_census.py from integrity-verified stores; objects and edges are the cost model\'s upper '
                        'bound (the margin is structural: interrupted read retries are excluded). Held-out entries are outstanding and '
                        'never read. Design evidence, not product qualification.',
            'manifest': dict(path=MANIFEST, bytes=len(manifest_raw), sha256=sha256(manifest_raw)),
            'closure': [pin_row(product, p) for p, _, _ in CLOSURE],
            'sizes': dict(c['SIZES']),
            'limits': dict(objects=limits[0], edges=limits[1], bytes=limits[2]),
            'margin': 2,
            'marginUnit': 'limit * 1000 // cost, floored (per mille); the margin holds at 2000 or more',
            'bytesUnit': 'bytes = base + perRootByte * R for a discovery root spelled in R bytes; reported at R in rootLengths, with no margin claimed (plan r4 section 2.1)',
            'rootLengths': list(ROOT_LENGTHS),
            'probeCrossCheck': 'retired (unit B2-b3d): the B2-b4a lead probe walked the walker before its storage redesign; the B2-b3d evidence carries a new lead probe of the redesigned walker over the same four stores',
            'entries': entries,
            'workspaces': workspaces,
            'failingEntries': failing,
            'caps': 'returned-to-law' if failing else 'recorded-margin-holds',
            'capsRecordedBy': 'M3-B r7 item 12 (unit B2-b4b3 changes the platform constants)',
            'heldOutMargin': held_state}
    return (json.dumps(body, indent=1, ensure_ascii=True) + '\n').encode()


def row(id_, m, limits, **extra):
    at = {str(r): m.bytes_at(r) for r in ROOT_LENGTHS}
    return dict(id=id_, **extra, counts=m.counts, objects=m.objects, edges=m.edges,
                objectMarginPermille=limits[0] * 1000 // m.objects, edgeMarginPermille=limits[1] * 1000 // m.edges,
                passes2x=2 * m.objects <= limits[0] and 2 * m.edges <= limits[1] and 2 * m.bytes_at(ROOT_LENGTHS[-1]) <= limits[2],
                bytes=dict(base=m.bytes, perRootByte=m.per_root_byte, at=at, marginPermilleAt={r: limits[2] * 1000 // b for r, b in at.items()},
                           fitsTwiceAt={r: 2 * b <= limits[2] for r, b in at.items()}))


def main():
    # r2 (Codex B2B4C1-R1-RF-2): no abbreviated options, and the blind mode's redaction is chosen from the parsed
    # arguments. Parser exits (usage, help) come before any store is touched and echo only the command line.
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true', help='compare the outputs without writing repository files')
    mode.add_argument('--write', action='store_true', help='regenerate the outputs')
    mode.add_argument('--held-out-blind', action='store_true', help='the blind held-out census: write only the receipt (B2-b4c)')
    parser.add_argument('--architecture', type=Path, required=True, help='architecture checkout (manifest, reference)')
    parser.add_argument('--packages-root', type=Path, required=True, help='checkout holding the provisioned python-packages snapshot')
    parser.add_argument('--t2-cache', type=Path, help='the private durable T2 cache (store/ and workspaces/); omit for the vectors only')
    args = parser.parse_args()
    if not args.held_out_blind:
        return run(args)
    try:
        run(args)
    except BaseException:  # noqa: BLE001
        # Every failure of a blind run, an exit or an interrupt included, is this one line: any exception text could
        # name a held-out path (plan r6 section 2.5).
        print('Discovery census blind run failed.', file=sys.stderr)
        raise SystemExit(1) from None


def run(args):
    product = Path(__file__).resolve().parent.parent.parent
    arch = args.architecture.resolve(strict=True)
    c = costs(product)
    wv, ref, slm, rule = load_reference(product, arch, args.packages_root.resolve(strict=True))
    if args.held_out_blind:
        require(args.t2_cache is not None, 'the blind mode needs the T2 cache')
        run_blind(product, arch, str(args.t2_cache.resolve(strict=True)), c,
                  lambda tree: (model(c, rule, tree), reference_population(wv, ref, slm, rule, tree)))
        return
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
