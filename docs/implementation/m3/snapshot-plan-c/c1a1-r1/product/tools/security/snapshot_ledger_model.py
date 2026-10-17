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
    ('CLASSIFY', 'crates/security/src/snapshot_walk.rs',
     r'fn classify_cost\(rel: &str\) -> WorkCost \{\n.*\n.*\n    WorkCost \{\n        objects: (\d+) \+ targets,\n        edges: (\d+),\n'
     r'        bytes: segments\n            \.saturating_mul\((\d+) \* std::mem::size_of::<usize>\(\)\)\n'
     r'            \.saturating_add\(rel\.len\(\)\.saturating_mul\(1 \+ targets\)\)\n            \.saturating_add\(\((\d+) \+ targets\)\.saturating_mul\(RECORD\)\),\n'),
    ('ROOT_STATUS', 'crates/security/src/snapshot_walk.rs', r'        \.run\(crate::custody::discovery_walk::STATUS, \|_\| \{()'),
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
    o, e, two, base = shapes['CLASSIFY']
    require((o, e, two * c['SIZES']['usize'], base) == c['CLASSIFY'][:4], 'the snapshot classify cost differs in shape')
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
        return anchor == '' or rel == anchor or rel.startswith(anchor + '/')

    def is_boundary(self, rel):
        if any(self.at_or_below(rel, b) for b in self.repos + self.projects):
            return True
        return any(not reason.startswith('MARKER_CUSTODY:') and self.at_or_below(rel, p) for p, reason in self.rows)

    def marker_row(self, parent, name):
        return any(reason.startswith('MARKER_CUSTODY:') and p == parent and reason[len('MARKER_CUSTODY:'):].split(':')[0] == name
                   for p, reason in self.rows)


class SnapshotModel:
    """The abstract walk of `walk_snapshot`: one charge per charge the code makes, in its order."""
    MARKERS = ('Cargo.toml', 'package.json', 'tsconfig.json', 'jsconfig.json')

    def __init__(self, c, rule, tree, boundaries, ignore=(), members=()):
        self.c, self.rule, self.t, self.b = c, rule, tree, boundaries
        self.ignore, self.members = tuple(ignore), tuple(members)
        self.cost = [0, 0, 0]

    def add(self, cost, times=1):
        for i in range(3):
            self.cost[i] += cost[i] * times

    def owned(self, nbytes):
        o, e = self.c['OWNED']
        self.add((o, e, nbytes + self.c['RECORD']))

    def capture(self):
        """`judge_opened` past its metadata-only rejection: CAP, then the dearer of a full entry list and the premise."""
        self.add(self.c['CAP'])
        o, e = self.c['OWNED']
        acl = (o, e, self.c['MAX_ENTRIES'] * self.c['ACL_ENTRY'] + self.c['RECORD'])
        self.add(tuple(max(x, y) for x, y in zip(acl, self.c['FS'][:3])))

    def classify(self, rel):
        o, e, two_usize, base, record = self.c['CLASSIFY']
        segments = rel.count('/') + 1
        targets = rel.split('/').count('target')
        self.add((o + targets, e, segments * two_usize + blen(rel) * (1 + targets) + (base + targets) * record))

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
        self.add(self.c['STATUS'][:3])  # the root's sample
        self.capture()                  # the root's custody
        known = set()
        stack = []
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
            kind = self.t.kind(child)
            if kind == 'dir':
                if self.b.is_boundary(child):
                    continue
                o, e, b = self.c['OPEN_DIR']
                self.add((o, e, b + blen(name)))
                self.add(self.c['STATUS'][:3])
                self.capture()
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
                    self.capture()
            else:
                self.owned(blen(child))
        return tuple(self.cost)


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
    return out


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
        predicted = SnapshotModel(c, rule, tree, Boundaries(case['inventory'])).walk()
        cases.append(dict(id=case['id'], origin='discovery-walk-vector', tree=case['tree'], inventory=case['inventory'],
                          groups=case['groups'], waive=case['waive'], foreign=case['foreign'],
                          predicted=dict(objects=predicted[0], edges=predicted[1], bytes=predicted[2])))
    for cid, tree_rows, inventory in generated_cases():
        tree = dc.tree_of_vector(dict(tree=tree_rows))
        predicted = SnapshotModel(c, rule, tree, Boundaries(inventory)).walk()
        cases.append(dict(id=cid, origin='generated', tree=tree_rows, inventory=inventory,
                          predicted=dict(objects=predicted[0], edges=predicted[1], bytes=predicted[2])))
    require(len({x['id'] for x in cases}) == len(cases), 'duplicate case ids')
    doc = dict(schemaVersion=1, standing='C1a1 snapshot walk charge predictions (tools/security/snapshot_ledger_model.py): '
               'the model of snapshot_walk.rs over the accepted automatic discovery walk vectors and generated trees, '
               'each to be an upper bound on the native walk. Design evidence, not qualification.',
               pins=pins, cases=cases)
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
