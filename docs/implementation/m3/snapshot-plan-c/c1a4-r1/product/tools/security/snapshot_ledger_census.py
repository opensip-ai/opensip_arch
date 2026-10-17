"""The snapshot ledger's lead-readable T2 census (M3-C r8 item 2, as M3-C r9 amends it; C1a plan r6, unit C1a4).

Developer tool only. It writes or checks one generated file, crates/security/src/snapshot_ledger_census.json: each
LEAD-READABLE T2 repository entry and workspace of the corpus manifest, priced on the snapshot ledger (the walk, the
session, and sealing's and the leftover capture's upper bound) and classified against `WorkLedger::snapshot_profile`'s
caps at the 2x margin. The security tests classify it again against the compiled profile
(`snapshot_walk_tests.rs`). This is B2-b's T2 census margin test extended to the snapshot ledger's object, edge and
byte caps (item 2).

It imports tools/security/discovery_census.py unchanged (its integrity-verified stores, its workspace overlays and
composition, its D15 decision path, its discovery walk model, its cost closure and its reference rule) and
tools/security/snapshot_ledger_model.py unchanged (the snapshot walk's and the capture session's charge model, and
the profile's caps read by anchor). Item 5's bounds and sealing's charges are read by anchor from
crates/host/src/snapshot_seal.rs and the identity crate.

Lead-readable only. Held-out entries are never opened: every store is reached through discovery_census.store_path,
which refuses a held-out entry before any filesystem call, and only `heldOut: false` entries and workspaces are visited.
Nothing of a tree is written: the output records ids and counts only. Held-out entries are covered by the reviewed
blind validation run (C1a plan r6, RF-3), not by this tool.

Pricing and eligibility are separate (M3-C r9, Codex M3CR9-R1-RF-3).
  - Pricing is conservative: no admitted boundary is applied (boundaries only exclude, so the walk is charged for more,
    never less); every handed file takes the session's dearer branch (a new blob); the walk model charges every capture
    at its dearer branch; sealing is charged at its 4 MiB envelope. The D15 member roots are the ones
    discovery_census.d15_terms admits over the entry's tree or the composed workspace.
  - Eligibility is decided on the admitted extent: the boundaries the discovery walk model itself derives over the
    same tree, and, as a lower bound on the rows, with every marker removed (a MARKER_CUSTODY row excludes only its
    marker) and every row below a directory deeper than discovery_scan.rs's MAX_UNIT_DEPTH removed (a DEPTH row
    excludes its unit and below). An entry is `over-item-5` only when that lower bound exceeds an item-5 bound; every
    other entry is measured at its conservative price.

Usage: snapshot_ledger_census.py (--check | --write | --report) --architecture <arch> --packages-root <checkout>
       --t2-cache <cache> [--caps NAME:OBJECTS,EDGES,BYTES ...]
  --report prints the record to standard output, with any further cap sets given (a cap given as - is not tested).
"""
import argparse
import hashlib
import importlib.util
import json
import os
import re
import sys
from pathlib import Path

PRODUCT = Path(__file__).resolve().parent.parent.parent
OUTPUT = 'crates/security/src/snapshot_ledger_census.json'
TOOL = 'tools/security/snapshot_ledger_census.py'
SEAL = 'crates/host/src/snapshot_seal.rs'
VCS = ('.git', '.hg', '.svn', '.jj')
# Sealing's charge sites (C1a3), each matched exactly once: the leftover's path copy, the inventory, the VCS record,
# the inventory blob's custody, the descriptor and the id.
SEAL_SITES = (r'work\.charge::<SealError>\(owned_record\(leftover\.len\(\)\)\)\?;',
              r'work\.charge::<SealError>\(owned_record\(inventory_len\)\)\?;',
              r'work\.charge::<SealError>\(owned_record\(160\)\)\?;',
              r'\.begin\(inventory\.len\(\) as u64, work\)', r'pending\.write\(chunk, work\)', r'pending\.commit\(work\)',
              r'work\.charge::<SealError>\(owned_record\(descriptor_bytes\)\)\?;',
              r'work\.charge::<SealError>\(owned_record\("snapshot2:"\.len\(\) \+ 64\)\)\?;')


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def anchor(path, pattern):
    hits = re.findall(pattern, (PRODUCT / path).read_text())
    if len(hits) != 1:
        raise ValueError('anchor %r matched %d times in %s' % (pattern, len(hits), path))
    return hits[0]


def canonical(value):
    """The identity crate's canonical JSON for strings, integers, objects and arrays (sorted keys, no whitespace,
    non-ASCII raw, control characters escaped)."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def bounds5():
    """Item 5's bounds, as sealing enforces them: rows, the canonical descriptor and total bytes."""
    rows = int(anchor(SEAL, r'\npub\(crate\) const MAX_ROWS: u64 = ([\d_]+);').replace('_', ''))
    total = int(anchor(SEAL, r'\npub\(crate\) const MAX_TOTAL_BYTES: u64 = ([\d_]+);').replace('_', ''))
    x, y, z = (int(v) for v in anchor('crates/identity/src/canonical.rs', r'\npub const MAX_BYTES: usize = (\d+) \* (\d+) \* (\d+);'))
    return rows, x * y * z, total


def item5(handed, sizes, limits):
    """Rows, total bytes and the canonical descriptor's length (C1a3's record, with placeholder digests)."""
    rows = len(handed)
    total = sum(sizes)
    inventory = 2 + max(0, rows - 1)
    for path, size in zip(handed, sizes):
        inventory += len(canonical(dict(bytes=size, path=path, sha256='0' * 64)))
    envelope = canonical(dict(projectId='prj1-' + '0' * 64, resolvedConfigDigest='0' * 64, schemaVersion=2,
                              scopeDigest='0' * 64, sourceInventory=[], vcsDigest='0' * 64))
    descriptor = len(envelope) - 2 + inventory
    over = [f for f, v, limit in zip(('rows', 'descriptor', 'totalBytes'), (rows, descriptor, total), limits) if v > limit]
    return dict(rows=rows, totalBytes=total, descriptorBytes=descriptor), over


def sealing_bound(c, s, limits):
    """Sealing's charge at its envelope, and the first leftover's path copy (C1a3's sites, each anchored): the
    inventory and the descriptor at 4 MiB each, the VCS record, the id, and the inventory blob's custody (its pending
    entry, its chunk writes, its commit's sample and the dearer of a new digest name and a duplicate's unlink)."""
    for pattern in SEAL_SITES:
        anchor(SEAL, pattern)
    vcs_record = int(anchor(SEAL, r'work\.charge::<SealError>\(owned_record\((\d+)\)\)\?;'))
    path_scalars = int(anchor('crates/identity/src/descriptors.rs', r'if value\.chars\(\)\.take\(\d+\)\.count\(\) > (\d+) \{'))
    row_path = path_scalars * 4  # bytes per Unicode scalar in UTF-8 at most (RFC 3629)
    rows, descriptor, _ = limits
    o, e = c['OWNED']
    owned = lambda n: (o, e, n + c['RECORD'])
    add = lambda *xs: tuple(sum(x[i] for x in xs) for i in range(3))
    name_len = len('pending-%d' % rows)
    unique = add(owned(64), (s['RENAME_COST'][0], s['RENAME_COST'][1], name_len + 64 + s['RENAME_COST'][2]), owned(s['SET_ENTRY_SIZE'][0]))
    dup = (s['UNLINK_COST'][0], s['UNLINK_COST'][1], name_len + s['UNLINK_COST'][2])
    chunks = -(-descriptor // s['READ_CHUNK'][0])
    writes = tuple(x * chunks for x in s['WRITE'])
    return add(owned(descriptor), owned(vcs_record), owned(descriptor), owned(len('snapshot2:') + 64), owned(name_len),
               (s['CREATE_COST'][0], s['CREATE_COST'][1], name_len + s['CREATE_COST'][2]), writes, c['STATUS'][:3],
               tuple(max(x, y) for x, y in zip(unique, dup)), owned(row_path))


def parse_caps(text):
    name, _, values = text.partition(':')
    return name, tuple(None if v == '-' else int(v) for v in values.split(','))


def census(arch, packages_root, cache, extra_caps):
    dc = load('discovery_census', PRODUCT / 'tools/security/discovery_census.py')
    slm = load('snapshot_ledger_model', PRODUCT / 'tools/security/snapshot_ledger_model.py')
    dm = dc.load_member_model(PRODUCT)
    c, _ = slm.snapshot_costs(PRODUCT, dc)
    s = slm.session_costs(PRODUCT, c)
    _, _, _, rule = dc.load_reference(PRODUCT, arch, packages_root)
    limits = bounds5()
    unit_depth = int(anchor('crates/security/src/custody/discovery_scan.rs', r'\nconst MAX_UNIT_DEPTH: usize = (\d+);'))
    caps = dict([('snapshotProfile', slm.snapshot_caps(PRODUCT))] + list(extra_caps))
    after = sealing_bound(c, s, limits)
    chunk = s['READ_CHUNK'][0]

    class Textless(dc.Tree):
        """A verified tree as the walk model reads it: a regular file's text is never needed, only its identity."""

        def node(self, rel):
            n = super().node(rel)
            if n is not None and n['kind'] == 'file' and 'text' not in n:
                return dict(n, text='')
            return n

    class Boundaried(dc.Model):
        """The discovery walk model, recording each child directory it makes a boundary: the boundary is counted just
        after the child's `opensip.json` observation (discovery_census.Model.subtree)."""

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.found, self.last = [], None
            outer = self

            class Counts(dict):
                def __setitem__(self, key, value):
                    if key == 'boundaries' and value > self.get(key, 0):
                        outer.found.append(outer.last.rsplit('/', 1)[0])
                    super().__setitem__(key, value)

            self.counts = Counts(self.counts)

        def observe(self, rel):
            self.last = rel
            super().observe(rel)

    one = slm.session_cost(c, s, [('a', b'\x01' * chunk)])
    two = slm.session_cost(c, s, [('a', b'\x01' * (2 * chunk))])
    step = tuple(y - x for x, y in zip(one, two))

    def snapshot(tree, boundaries, members):
        model = slm.SnapshotModel(c, rule, tree, boundaries, members=members)
        walk = model.walk()
        paths = [p for p, _ in model.handed]
        sizes = [tree.nodes[p]['size'] for p in paths]
        # The session at its dearer branch: every file a new blob of one chunk (distinct stand-ins), then each
        # file's chunks beyond one (or none, for an empty file) by the model's own per-chunk charge.
        session = list(slm.session_cost(c, s, [(p, b'%d' % i) for i, p in enumerate(paths)]))
        for size in sizes:
            for i in range(3):
                session[i] += step[i] * (-(-size // chunk) - 1)
        return walk, tuple(session), paths, sizes

    def margins(cost):
        out = {}
        for name, cap in caps.items():
            m = {}
            for k, v, limit in zip(('objects', 'edges', 'bytes'), cost, cap):
                if limit is not None:
                    m[k] = dict(cap=limit, marginPermille=limit * 1000 // max(v, 1), passes2x=2 * v <= limit)
            out[name] = dict(m, passes2x=all(x['passes2x'] for x in m.values()))
        return out

    def price(tree, label, mounts=()):
        tree = Textless(tree.nodes)
        member = dm.Member(c, dc.ENVIRONMENT_ENVELOPE, c['SYSTEM_SOURCES'])
        _, _, members = dc.d15_terms(c, dm, rule, tree, member)
        members = tuple(members)
        disc = Boundaried(c, rule, tree, 'automatic', [], members)
        disc.walk()
        found = sorted(set(disc.found))
        repos = [b for b in found if any(tree.kind(slm.join_rel(b, v)) is not None for v in VCS)]
        admitted = slm.Boundaries(dict(nestedRepositories=repos, nestedProjects=[b for b in found if b not in repos]))
        walk, session, paths, sizes = snapshot(tree, slm.Boundaries({}), members)
        cost = tuple(w + x for w, x in zip(walk, session))
        full = tuple(x + y for x, y in zip(cost, after))
        conservative, _ = item5(paths, sizes, limits)
        if found:
            _, _, a_paths, a_sizes = snapshot(tree, admitted, members)
        else:
            a_paths, a_sizes = paths, sizes
        keep = [(p, z) for p, z in zip(a_paths, a_sizes)
                if p.rsplit('/', 1)[-1] not in slm.SnapshotModel.MARKERS and p.count('/') <= unit_depth]
        lower, over = item5([p for p, _ in keep], [z for _, z in keep], limits)
        row = dict(id=label, members=len(members), admittedBoundaries=len(found),
                   discoveryDepthLimitDirectories=disc.counts['depthLimitDirectories'],
                   item5Conservative=conservative,
                   eligibility=dict(admittedRows=len(a_paths), markerOrDeepRowsRemoved=len(a_paths) - len(keep), lowerBound=lower),
                   walk=dict(objects=walk[0], edges=walk[1], bytes=walk[2]),
                   session=dict(objects=session[0], edges=session[1], bytes=session[2]),
                   fullLedger=dict(objects=full[0], edges=full[1], bytes=full[2]))
        if over:
            row.update(status='over-item-5', overFields=over)
        else:
            row.update(status='measured', margins=margins(full))
        if mounts:
            w2, s2, _, _ = snapshot(tree, slm.Boundaries({}), tuple(mounts))
            alt = tuple(x + y + z for x, y, z in zip(w2, s2, after))
            row['allMountsAsMembers'] = dict(members=len(mounts), objects=alt[0], edges=alt[1], bytes=alt[2],
                                             margins=margins(alt))
        return row

    manifest_raw = (arch / dc.MANIFEST).read_bytes()
    manifest = json.loads(manifest_raw)
    store = os.path.join(cache, 'store')
    entries, trees = [], {}
    for entry in manifest['repositories']:
        if entry['heldOut'] is not False:
            continue
        tree = dc.verified_tree(dc.store_path(store, entry), entry)
        trees[entry['id']] = tree
        entries.append(price(tree, entry['id']))
        print('priced', entry['id'], file=sys.stderr, flush=True)
    workspaces = []
    for ws in manifest['workspaces']:
        if ws['heldOut'] is not False:
            continue
        root_tree, members, _ = dc.verified_workspace(cache, arch, store, ws, manifest, trees)
        workspaces.append(price(dc.compose(root_tree, members), ws['id'], [mount for mount, _ in members]))
        print('priced', ws['id'], file=sys.stderr, flush=True)
    rows = entries + workspaces
    measured = [r for r in rows if r['status'] == 'measured']
    keys = ('objects', 'edges', 'bytes')
    pins = [dc.pin_row(PRODUCT, p) for p in (TOOL, 'tools/security/snapshot_ledger_model.py', 'tools/security/discovery_census.py',
                                            'tools/security/discovery_member_model.py', SEAL, slm.WORK_LEDGER)]
    body = dict(schemaVersion=1,
                standing='The lead-readable T2 census on the snapshot ledger (M3-C r8 item 2 as M3-C r9 amends it; unit C1a4). '
                         'Generated by tools/security/snapshot_ledger_census.py from integrity-verified stores; held-out '
                         'entries are never read here (they are the reviewed blind validation run\'s). Priced with no '
                         'boundary, every blob new and sealing at its envelope (all conservative), with the D15 members '
                         'discovery admits; over-item-5 decided on the admitted extent\'s lower bound. Counts and ids '
                         'only. Design evidence, not product qualification.',
                manifest=dict(path=dc.MANIFEST, bytes=len(manifest_raw), sha256=hashlib.sha256(manifest_raw).hexdigest()),
                pins=pins, item5=dict(zip(('rows', 'descriptorBytes', 'totalBytes'), limits)), maxUnitDepth=unit_depth,
                afterWalk=dict(zip(keys, after)), caps={n: dict(zip(keys, v)) for n, v in caps.items()}, margin=2,
                marginUnit='cap * 1000 // cost, floored (per mille); the margin holds at 2000 or more',
                counts=dict(entries=len(entries), workspaces=len(workspaces), measured=len(measured),
                            overItem5=len(rows) - len(measured), withMembers=sum(1 for r in rows if r['members']),
                            withAdmittedBoundaries=sum(1 for r in rows if r['admittedBoundaries'])),
                maximaMeasured={k: max((r['fullLedger'][k] for r in measured), default=0) for k in keys},
                failing2x={n: sorted(r['id'] for r in measured if not r['margins'][n]['passes2x']) for n in caps},
                entries=entries, workspaces=workspaces)
    return (json.dumps(body, indent=1, ensure_ascii=True) + '\n').encode()


def main():
    ap = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument('--check', action='store_true', help='compare the output without writing it')
    mode.add_argument('--write', action='store_true', help='regenerate the output')
    mode.add_argument('--report', action='store_true', help='print the record, with any further cap sets')
    ap.add_argument('--architecture', type=Path, required=True)
    ap.add_argument('--packages-root', type=Path, required=True)
    ap.add_argument('--t2-cache', type=Path, required=True)
    ap.add_argument('--caps', action='append', type=parse_caps, default=[])
    a = ap.parse_args()
    if a.caps and not a.report:
        raise ValueError('further cap sets are for --report only')
    raw = census(a.architecture.resolve(strict=True), a.packages_root.resolve(strict=True), str(a.t2_cache.resolve(strict=True)), a.caps)
    target = PRODUCT / OUTPUT
    if a.report:
        sys.stdout.write(raw.decode())
    elif a.check:
        if not (target.is_file() and target.read_bytes() == raw):
            raise ValueError('output differs: ' + OUTPUT)
        print('Verified ' + OUTPUT)
    else:
        target.write_bytes(raw)
        print('Generated ' + OUTPUT)


if __name__ == '__main__':
    try:
        main()
    except (ValueError, KeyError, OSError) as error:
        print('Snapshot ledger census failed: ' + str(error), file=sys.stderr)
        raise SystemExit(1)
