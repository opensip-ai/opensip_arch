"""The snapshot walk's charge model (M3-C r8 item 2; unit C1a1, C1a plan r5 section 2).

Developer tool only. It writes or checks crates/security/src/snapshot_ledger_vectors.json: for each tree, its description
(the discovery walk vectors' format), its admitted boundaries, and the model's predicted charge of the snapshot extent
walk (`crates/security/src/snapshot_walk.rs`, with its opener helpers in `snapshot_source.rs`) as (objects, edges,
bytes). The security tests walk each tree natively on a fresh ledger and assert the walk used no more
(`snapshot_walk_tests.rs`, the soundness control).

The cost constants are the bound census's: this tool imports tools/security/discovery_census.py unchanged (its `costs`,
which verifies the census's whole cost closure and reads every constant by anchor, its `Tree` and its tree reading of
the walk vectors), so a change to any shared charge refuses here too. The snapshot modules' own shapes are pinned by
anchors below, and both files are pinned whole: any change to them refuses until this model is revised. Unknowns are
charged at their dearer branch: every judged object captures its ACL and takes the larger of a full entry list and the
filesystem premise.

It also reports, for the cap derivation that follows in C1a4, the model's charge for item 5's maximum row population
(100,000 rows whose canonical inventory is at most 4 MiB). No network, process or environment input.
"""
from pathlib import Path
import argparse
import hashlib
import importlib.util
import json
import re
import sys

OUTPUT = 'crates/security/src/snapshot_ledger_vectors.json'
CENSUS = 'tools/security/discovery_census.py'
WALK_VECTORS = 'crates/security/src/custody/discovery_walk_vectors.json'
SNAPSHOT_FILES = ('crates/security/src/snapshot_walk.rs', 'crates/security/src/snapshot_source.rs')
# The snapshot modules' own charge shapes (each must match exactly once).
SNAPSHOT_ANCHORS = (
    ('RECORD', 'crates/security/src/snapshot_walk.rs', r'\nconst RECORD: usize = (\d+);'),
    # r2 (Codex C1A1-R1-RF-4): the classification's own form, counted from the shared rule's source.
    ('CLASSIFY', 'crates/security/src/snapshot_walk.rs',
     r'fn classify_cost\(rel: &str, members: &BTreeSet<String>\) -> WorkCost \{\n'
     r'    let segments = rel\.split\(\'/\'\)\.count\(\);\n'
     r'    let targets = rel\.split\(\'/\'\)\.filter\(\|part\| \*part == "target"\)\.count\(\);\n'
     r'    let \(lists, member_segments\) = members\n        \.iter\(\)\n        \.filter\(\|member\| !member\.is_empty\(\)\)\n'
     r'        \.fold\(\(0usize, 0usize\), \|\(lists, total\), member\| \{\n'
     r'            \(lists \+ 1, total \+ member\.split\(\'/\'\)\.count\(\)\)\n        \}\);\n'
     r'    let objects = (\d+) \+ targets \+ lists;\n    WorkCost \{\n        objects,\n        edges: (\d+),\n'
     r'        bytes: segments\n            \.saturating_add\(member_segments\)\n'
     r'            \.saturating_mul\((\d+) \* std::mem::size_of::<usize>\(\)\)\n'
     r'            \.saturating_add\(rel\.len\(\)\.saturating_mul\((\d+) \+ targets\)\)\n'
     r'            \.saturating_add\(objects\.saturating_mul\(RECORD\)\),\n'),
    ('ANCHOR_CLASSIFY', 'crates/security/src/snapshot_walk.rs',
     r'    if last_segment\(path\) != rule::OPENSIP_CUSTODY_STATE \{\n        return Ok\(false\);\n    \}\n'
     r'    work\.charge::<SnapshotStop<E>>\(classify_cost\(path, members\)\)\?;()'),
    ('ANCHOR_DROP', 'crates/security/src/snapshot_walk.rs',
     r'    if let Some\(index\) = anchor \{\n        drop\(paths\.remove\(index\)\);\n    \}\n    work\.charge::<SnapshotStop<E>>\(owned\(\n()'),
    ('KIND_FREE_BOUNDARY', 'crates/security/src/snapshot_walk.rs',
     r'        if extent\.boundaries\.is_boundary\(&rel\) \{\n            continue;\n        \}\n        let parent_dir = levels\n()'),
    ('ROOT_STATUS', 'crates/security/src/snapshot_source.rs',
     r'    let sample = work\.run\(STATUS, \|_\| \{\n        opensip_platform::observe_descriptor_metadata\(lent\.as_file\(\)\)()'),
    ('ROOT_FRAME', 'crates/security/src/snapshot_walk.rs',
     r'    // The root frame\'s own slot\.\n    work\.charge::<SnapshotStop<E>>\(owned\(0\)\)\?;()'),
    ('FRAME', 'crates/security/src/snapshot_walk.rs', r'                work\.charge::<SnapshotStop<E>>\(owned\(0\)\)\?;()'),
    ('LISTING', 'crates/security/src/snapshot_walk.rs', r'    work\.charge::<SnapshotStop<E>>\(LISTING\)\?;()'),
    ('SLOTS', 'crates/security/src/snapshot_walk.rs',
     r'    work\.charge::<SnapshotStop<E>>\(owned\(\n        paths\n            \.len\(\)\n            \.saturating_mul\(std::mem::size_of::<ChildObservation>\(\)\),\n    \)\)\?;()'),
    ('CARGO_KEY', 'crates/security/src/snapshot_walk.rs', r'        work\.charge::<SnapshotStop<E>>\(key_cost\(&rel, ""\)\)\?;()'),
    ('SYMLINK', 'crates/security/src/snapshot_walk.rs',
     r'                work\.charge::<SnapshotStop<E>>\(owned\(rel\.len\(\)\)\)\?;\n                report\.symlinks\.push\(rel\);()'),
    ('SPECIAL', 'crates/security/src/snapshot_walk.rs',
     r'                work\.charge::<SnapshotStop<E>>\(owned\(rel\.len\(\)\)\)\?;\n                report\.special\.push\(rel\);()'),
    ('ACL_ENTRIES', 'crates/security/src/snapshot_source.rs',
     r'count\.saturating_mul\(std::mem::size_of::<opensip_platform::CapturedAclEntry>\(\)\),()'),
    ('OPEN_DIR_SAMPLE', 'crates/security/src/snapshot_source.rs',
     r'    let sample = work\.run\(STATUS, \|_\| \{\n        opensip_platform::observe_descriptor_metadata\(directory\.as_file\(\)\)()'),
    ('OPEN_REG_SAMPLE', 'crates/security/src/snapshot_source.rs',
     r'    let sample = work\.run\(STATUS, \|_\| \{\n        opensip_platform::observe_descriptor_metadata\(&file\)()'),
    # r3 (Codex C1A1-R2-RF-1): the pre-walk opener's charges, in its order.
    ('OPENER_VALIDATE', 'crates/security/src/snapshot_source.rs',
     r'        work\.charge::<SnapshotRefusal>\(owned\(path\.len\(\)\)\)\?;\n        let Ok\(validated\) = opensip_identity::LogicalPath::parse\(path\) else \{()'),
    ('OPENER_ROOT', 'crates/security/src/snapshot_source.rs', r'        judge_root\(self, custody, work\)\?;()'),
    ('OPENER_KEY', 'crates/security/src/snapshot_source.rs', r'            work\.charge::<SnapshotRefusal>\(key_cost\(&rel, part\)\)\?;()'),
    ('OPENER_PATH_KEPT', 'crates/security/src/snapshot_source.rs', r'            path: validated\.into_string\(\),()'),
    ('KEY_COST', 'crates/security/src/snapshot_source.rs',
     r'pub\(crate\) fn key_cost\(dir: &str, name: &str\) -> WorkCost \{\n    owned\(dir\.len\(\) \+ 1 \+ name\.len\(\)\)\n\}()'),
)
# Item 5's bounds, and item 2's object allowance for rows.
MAX_ROWS = 100_000
MAX_DESCRIPTOR = 4 * 1024 * 1024
# The snapshot ledger's caps fixed by item 2 (objects, edges); bytes are C1a4's.
SNAPSHOT_OBJECTS = 1 << 20
SNAPSHOT_EDGES = 1 << 21


def require(condition, message):
    if not condition:
        raise ValueError(message)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def snapshot_costs(product, dc):
    c = dc.costs(product)
    shapes = {}
    for name, path, pattern in SNAPSHOT_ANCHORS:
        hits = list(re.finditer(pattern, (product / path).read_text()))
        require(len(hits) == 1, 'snapshot anchor %s matched %d times' % (name, len(hits)))
        shapes[name] = tuple(int(g) for g in hits[0].groups() if g)
    require(shapes['RECORD'] == (c['RECORD'],), 'the snapshot walk prices records unlike the census')
    o, e, two, anchors = shapes['CLASSIFY']
    c = dict(c, SNAPSHOT_CLASSIFY=(o, e, two * c['SIZES']['usize'], anchors))
    pins = [dc.pin_row(product, p) for p in SNAPSHOT_FILES]
    return c, pins


def blen(text):
    return len(text.encode())


def join_rel(parent, name):
    return parent + '/' + name if parent else name


class Boundaries:
    """`AdmittedBoundaries`, as the walk asks it: nested repositories and projects, and custody rows (a marker-custody
    row excludes its marker only; any other row its directory and below)."""

    def __init__(self, inventory):
        self.repos = list(inventory.get('nestedRepositories', []))
        self.projects = list(inventory.get('nestedProjects', []))
        self.rows = [(r['path'], r['reason']) for r in inventory.get('custodyExcludedUnits', [])]

    @staticmethod
    def at_or_below(rel, anchor):
        """The shared rule's `at_or_below` exactly: the root anchor `''` covers only the root."""
        stem = anchor.rstrip('/')
        return rel == anchor or (rel.startswith(stem) and rel[len(stem):].startswith('/'))

    def anchor(self, rel, marker=None):
        """`AdmittedBoundaries::boundary_anchor`: repositories, then projects, then the first covering custody row."""
        for b in self.repos + self.projects:
            if self.at_or_below(rel, b):
                return b
        for p, reason in self.rows:
            if reason.startswith('MARKER_CUSTODY:'):
                if p == rel and marker is not None and reason[len('MARKER_CUSTODY:'):].split(':')[0] == marker:
                    return p
            elif self.at_or_below(rel, p):
                return p
        return None

    def is_boundary(self, rel):
        return self.anchor(rel) is not None

    def marker_row(self, parent, name):
        return self.anchor(parent, name) == parent


class SnapshotModel:
    """The abstract walk of `walk_snapshot`: one charge per charge the code makes, in its order."""
    MARKERS = ('Cargo.toml', 'package.json', 'tsconfig.json', 'jsconfig.json')

    def __init__(self, c, rule, tree, boundaries, ignore=(), members=(), acl_paths=()):
        self.c, self.rule, self.t, self.b = c, rule, tree, boundaries
        self.ignore, self.members, self.acl_paths = tuple(ignore), tuple(members), frozenset(acl_paths)
        self.cost = [0, 0, 0]
        # Exact (r2, Codex C1A1-R1-NBO-2) while every capture takes the branch charged: on the APFS scratch an object
        # with no ACL entry returns none, so its capture takes the premise, which must be the dearer branch.
        o, e = self.c['OWNED']
        full = (o, e, self.c['MAX_ENTRIES'] * self.c['ACL_ENTRY'] + self.c['RECORD'])
        self.exact = all(f >= a for f, a in zip(self.c['FS'][:3], full))

    def add(self, cost, times=1):
        for i in range(3):
            self.cost[i] += cost[i] * times

    def owned(self, nbytes):
        o, e = self.c['OWNED']
        self.add((o, e, nbytes + self.c['RECORD']))

    def capture(self, rel):
        """`judge_opened` past its metadata-only rejection: CAP, then the dearer of a full entry list and the premise."""
        if rel in self.acl_paths:
            self.exact = False
        self.add(self.c['CAP'])
        o, e = self.c['OWNED']
        acl = (o, e, self.c['MAX_ENTRIES'] * self.c['ACL_ENTRY'] + self.c['RECORD'])
        self.add(tuple(max(x, y) for x, y in zip(acl, self.c['FS'][:3])))

    def classify(self, rel):
        """`classify_cost`: the segment list, a prefix per `target`, the anchors, and each member root's list."""
        o, e, two_usize, anchors = self.c['SNAPSHOT_CLASSIFY']
        segments = rel.count('/') + 1
        targets = rel.split('/').count('target')
        lists = [m for m in self.members if m]
        objects = o + targets + len(lists)
        member_segments = sum(m.count('/') + 1 for m in lists)
        self.add((objects, e, (segments + member_segments) * two_usize + blen(rel) * (anchors + targets)
                  + objects * self.c['RECORD']))

    def custody_anchor(self, rel, known):
        """An exact `.opensip` anchor, asked of `.opensip` names only, and charged as a classification."""
        if rel.split('/')[-1] != '.opensip':
            return False
        self.classify(rel)
        hit = self.rule.classify_path(rel, set(known), self.members)
        return hit is not None and hit[1] == 'opensip-custody-state'

    def ignored(self, rel):
        return any(rel == p or rel.startswith(p + '/') for p in self.ignore)

    def enter(self, rel, known):
        self.add(self.c['LISTING'][:3])
        names = self.t.children.get(rel, [])
        vo, ve, vb = self.c['VISIT']
        self.add((vo, ve, vb), len(names) + 2)  # `.` and `..` are visited too
        co, ce, two, tworec = self.c['CONVERTED_NAME']
        for name in names:
            self.add((co, ce, two * (blen(rel) + 1 + blen(name)) + tworec * self.c['RECORD']))
        # The exact `.opensip` anchors leave the listing before any observation (Codex C1A1-R1-RF-1).
        names = [n for n in names if not self.custody_anchor(join_rel(rel, n), known)]
        self.owned(len(names) * self.c['SLOT'])
        oo, oe, ob = self.c['OBS']
        for name in names:
            self.add((oo, oe, ob + blen(name)))
        pushed = False
        if 'Cargo.toml' in names and self.t.kind(join_rel(rel, 'Cargo.toml')) == 'file' and rel not in known:
            self.owned(blen(rel) + 1)
            known.add(rel)
            pushed = True
        return names, pushed

    def walk(self):
        """The predicted (objects, edges, bytes); `self.exact` after it says whether the native walk must equal it."""
        self.add(self.c['STATUS'][:3])  # the root's sample
        self.capture('')                # the root's custody
        known = set()
        stack = []
        self.owned(0)                   # the root frame
        names, pushed = self.enter('', known)
        stack.append(['', names, 0, pushed])
        while stack:
            top = stack[-1]
            rel, names, index, pushed = top
            if index == len(names):
                stack.pop()
                if pushed:
                    known.discard(rel)
                continue
            top[2] += 1
            name = names[index]
            child = join_rel(rel, name)
            self.classify(child)
            if self.rule.classify_path(child, set(known), self.members) is not None or self.ignored(child):
                continue
            if self.b.is_boundary(child):  # whatever the entry now is (Codex C1A1-R1-RF-2)
                continue
            kind = self.t.kind(child)
            if kind == 'dir':
                o, e, b = self.c['OPEN_DIR']
                self.add((o, e, b + blen(name)))
                self.add(self.c['STATUS'][:3])
                self.capture(child)
                self.owned(0)
                child_names, child_pushed = self.enter(child, known)
                stack.append([child, child_names, 0, child_pushed])
            elif kind == 'file':
                if name in self.MARKERS and self.b.marker_row(rel, name):
                    continue
                o, e, b = self.c['OPEN_REG_1']
                self.add((o, e, b + blen(name)))
                self.add(self.c['STATUS'][:3])
                if name in self.MARKERS:
                    self.capture(child)
            else:
                self.owned(blen(child))
        return tuple(self.cost)


def opener_cost(c, tree, path, acl):
    """`SnapshotRoot::open(path)`: the validator's copy (kept as the source file's path), the root's sample and
    custody, then per directory component its key, observation, open, sample and custody, then the leaf's observation,
    open and sample, and a marker's custody."""
    m = SnapshotModel(c, None, tree, None, acl_paths=acl)
    m.owned(blen(path))
    m.add(c['STATUS'][:3])
    m.capture('')
    parts, rel = path.split('/'), ''
    oo, oe, ob = c['OBS']
    for part in parts[:-1]:
        m.owned(blen(rel) + 1 + blen(part))
        sub = join_rel(rel, part)
        m.add((oo, oe, ob + blen(part)))
        o, e, b = c['OPEN_DIR']
        m.add((o, e, b + blen(part)))
        m.add(c['STATUS'][:3])
        m.capture(sub)
        rel = sub
    leaf = parts[-1]
    m.add((oo, oe, ob + blen(leaf)))
    o, e, b = c['OPEN_REG_1']
    m.add((o, e, b + blen(leaf)))
    m.add(c['STATUS'][:3])
    if leaf in SnapshotModel.MARKERS:
        m.capture(path)
    return tuple(m.cost), m.exact


def opener_cases():
    """r3 (Codex C1A1-R2-RF-1): a root-level file, a nested one and a nested marker, each opened before any walk."""
    tree = [dict(kind='file', path='a.txt', mode='0644', text='a'),
            dict(kind='dir', path='src', mode='0755'), dict(kind='dir', path='src/lib', mode='0755'),
            dict(kind='file', path='src/lib/main.rs', mode='0644', text='fn main() {}'),
            dict(kind='dir', path='pkg', mode='0755'), dict(kind='file', path='pkg/package.json', mode='0644', text='{}')]
    return [('opener-' + p.replace('/', '-'), tree, p) for p in ('a.txt', 'src/lib/main.rs', 'pkg/package.json')]


def generated_cases():
    """Trees that maximize single charge types: long names, a wide listing of excluded entries, a deep chain."""
    out = []
    long = 'n' * 200
    tree = [dict(kind='file', path='%s%03d' % (long, k), mode='0644', text='x') for k in range(40)]
    out.append(('wide-long-names', tree, {}))
    tree = [dict(kind='dir', path='node_modules', mode='0755')]
    tree += [dict(kind='dir', path='node_modules/%s%03d' % (long, k), mode='0755') for k in range(30)]
    tree += [dict(kind='file', path='kept.txt', mode='0644', text='k')]
    out.append(('wide-pruned-listing', tree, {}))
    tree, rel = [], ''
    for k in range(64):
        rel = join_rel(rel, 'd%02d' % k)
        tree.append(dict(kind='dir', path=rel, mode='0755'))
    tree.append(dict(kind='file', path=join_rel(rel, 'leaf.txt'), mode='0644', text='leaf'))
    out.append(('deep-chain', tree, {}))
    tree = [dict(kind='file', path='Cargo.toml', mode='0644', text='[package]\n'),
            dict(kind='dir', path='target', mode='0755'), dict(kind='file', path='target/x', mode='0644', text='x'),
            dict(kind='dir', path='src', mode='0755'), dict(kind='file', path='src/main.rs', mode='0644', text='fn main() {}'),
            dict(kind='file', path='package.json', mode='0644', text='{}'),
            dict(kind='symlink', path='link', mode='0755', target='src'),
            dict(kind='dir', path='r', mode='0755'), dict(kind='file', path='r/f', mode='0644', text='f')]
    out.append(('markers-pruned-boundary-and-link', tree, dict(nestedRepositories=['r'])))
    # r2 (Codex C1A1-R1-RF-1): the exact `.opensip` anchors at the root and a D15 member, never observed, beside an
    # ordinary nested `.opensip` that is walked.
    tree = [dict(kind='dir', path='.opensip', mode='0755'), dict(kind='file', path='.opensip/project-id.v1', mode='0644', text='p'),
            dict(kind='dir', path='m', mode='0755'), dict(kind='file', path='m/package.json', mode='0644', text='{}'),
            dict(kind='dir', path='m/.opensip', mode='0755'), dict(kind='file', path='m/.opensip/x', mode='0644', text='x'),
            dict(kind='dir', path='a', mode='0755'), dict(kind='dir', path='a/.opensip', mode='0755'),
            dict(kind='file', path='a/.opensip/kept.txt', mode='0644', text='k')]
    out.append(('opensip-anchors-root-and-member', tree, {}, ['m']))
    # r2 (Codex C1A1-R1-RF-2): boundaries that are now a file, a link and a FIFO, and a custody row that is now a file.
    tree = [dict(kind='file', path='r1', mode='0644', text='was a repository'),
            dict(kind='symlink', path='r2', mode='0755', target='r1'),
            dict(kind='fifo', path='r3', mode='0644'),
            dict(kind='file', path='c', mode='0644', text='was a custody-excluded directory'),
            dict(kind='file', path='kept.txt', mode='0644', text='k')]
    out.append(('boundaries-replaced-by-non-directories', tree,
                dict(nestedRepositories=['r1', 'r2', 'r3'],
                     custodyExcludedUnits=[dict(path='c', reason='DIRECTORY_CUSTODY:WRITABLE_BY_OTHERS')])))
    # r2 (Codex C1A1-R1-RF-4): long names three deep (about 640 bytes of path, within macOS's 1,024-byte path limit
    # under a lane's private TMPDIR), and 24 custody rows consulted for every entry.
    tree, rel = [], ''
    for k in range(3):
        rel = join_rel(rel, ('L%d' % k) + 'l' * 198)
        tree.append(dict(kind='dir', path=rel, mode='0755'))
    tree.append(dict(kind='file', path=join_rel(rel, 'package.json'), mode='0644', text='{}'))
    tree.append(dict(kind='file', path=join_rel(rel, 'f' * 40), mode='0644', text='f'))
    rows = []
    for k in range(12):
        tree.append(dict(kind='dir', path='p%02d' % k, mode='0755'))
        tree.append(dict(kind='file', path='p%02d/package.json' % k, mode='0644', text='{}'))
        tree.append(dict(kind='file', path='p%02d/s.ts' % k, mode='0644', text='s'))
        rows.append(dict(path='p%02d' % k, reason='MARKER_CUSTODY:package.json:HARD_LINKED'))
        tree.append(dict(kind='dir', path='c%02d' % k, mode='0755'))
        tree.append(dict(kind='file', path='c%02d/x' % k, mode='0644', text='x'))
        rows.append(dict(path='c%02d' % k, reason='DIRECTORY_CUSTODY:WRITABLE_BY_GROUP'))
    out.append(('long-deep-and-many-custody-rows', tree, dict(custodyExcludedUnits=rows)))
    return out


def acl_paths(rows):
    """The tree's entries given an ACL entry: a capture of one may take the entry-list branch."""
    return {r['path'] for r in rows if r.get('acl')}


def vectors(product, arch, packages_root):
    dc = load('discovery_census', product / CENSUS)
    c, pins = snapshot_costs(product, dc)
    wv, ref, slm, rule = dc.load_reference(product, arch, packages_root)
    body = json.loads((product / WALK_VECTORS).read_bytes())
    cases = []
    for case in body['cases']:
        if case['source'] != 'automatic' or case['expected']['status'] != 'ACCEPT':
            continue
        tree = dc.tree_of_vector(case)
        model = SnapshotModel(c, rule, tree, Boundaries(case['inventory']), acl_paths=acl_paths(case['tree']))
        predicted = model.walk()
        cases.append(dict(id=case['id'], origin='discovery-walk-vector', tree=case['tree'], inventory=case['inventory'],
                          groups=case['groups'], waive=case['waive'], foreign=case['foreign'], exact=model.exact,
                          predicted=dict(objects=predicted[0], edges=predicted[1], bytes=predicted[2])))
    for cid, tree_rows, inventory, *rest in generated_cases():
        members = rest[0] if rest else []
        tree = dc.tree_of_vector(dict(tree=tree_rows))
        model = SnapshotModel(c, rule, tree, Boundaries(inventory), members=members, acl_paths=acl_paths(tree_rows))
        predicted = model.walk()
        cases.append(dict(id=cid, origin='generated', tree=tree_rows, inventory=inventory, members=members, exact=model.exact,
                          predicted=dict(objects=predicted[0], edges=predicted[1], bytes=predicted[2])))
    require(len({x['id'] for x in cases}) == len(cases), 'duplicate case ids')
    openers = []
    for oid, tree_rows, path in opener_cases():
        predicted, exact = opener_cost(c, dc.tree_of_vector(dict(tree=tree_rows)), path, acl_paths(tree_rows))
        openers.append(dict(id=oid, tree=tree_rows, path=path, exact=exact,
                            predicted=dict(objects=predicted[0], edges=predicted[1], bytes=predicted[2])))
    doc = dict(schemaVersion=1, standing='C1a1 snapshot walk charge predictions (tools/security/snapshot_ledger_model.py): '
               'the model of snapshot_walk.rs over the accepted automatic discovery walk vectors and generated trees, '
               'each to be an upper bound on the native walk, and equal to it where `exact` (every capture there takes '
               'the branch the model charges). Design evidence, not qualification.',
               pins=pins, cases=cases, openers=openers)
    return (json.dumps(doc, indent=1, sort_keys=True) + '\n').encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true')
    mode.add_argument('--write', action='store_true')
    parser.add_argument('--architecture', type=Path, required=True)
    parser.add_argument('--packages-root', type=Path, required=True)
    args = parser.parse_args()
    product = Path(__file__).resolve().parent.parent.parent
    raw = vectors(product, args.architecture.resolve(strict=True), args.packages_root.resolve(strict=True))
    target = product / OUTPUT
    if args.check:
        require(target.is_file() and target.read_bytes() == raw, 'snapshot ledger vectors differ: ' + OUTPUT)
    else:
        target.write_bytes(raw)
    print(('Verified ' if args.check else 'Generated ') + OUTPUT)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError) as error:
        print('Snapshot ledger model failed: ' + str(error), file=sys.stderr)
        raise SystemExit(1)
