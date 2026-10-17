"""The snapshot ledger's lead-readable T2 census (M3-C r9 input; C1a plan r6, C1a4).

Developer tool only. It imports tools/security/discovery_census.py unchanged (its integrity-verified stores, its
workspace overlays and composition, its D15 decision path, its discovery walk model, its cost closure and its reference
rule) and tools/security/snapshot_ledger_model.py unchanged (the snapshot walk's and the capture session's charge
model), and prices each LEAD-READABLE T2 repository entry and workspace of the corpus manifest on the snapshot ledger:
the walk, then the session, then (given --term-a) sealing's and the leftover capture's upper bound.

Lead-readable only. Held-out entries are never opened: every store is reached through discovery_census.store_path,
which refuses a held-out entry before any filesystem call, and only `heldOut: false` entries and workspaces are visited.
The blind mode is neither called nor changed. Nothing of a tree is written: the output records ids and counts only.

Pricing and eligibility are separate (r2, Codex M3CR9-R1-RF-3).
  - Pricing is conservative: no admitted boundary is applied (boundaries only exclude, so the walk is charged for more,
    never less); every handed file takes the session's dearer branch (a new blob); the walk model charges every capture
    at its dearer branch. The D15 member roots are the ones discovery_census.d15_terms admits over the entry's tree or
    the composed workspace (r2, Codex M3CR9-R1-RF-2): `classify_cost` charges each of them on every classification.
    For a workspace, `allMountsAsMembers` also prices it as if every mount were an admitted member.
  - Eligibility is decided on the admitted extent: the boundaries the discovery walk model itself derives over the
    same tree (a child directory with VCS evidence or an `opensip.json`, not a member), and, as a lower bound on the
    rows, with every marker removed (a MARKER_CUSTODY row excludes only its marker) and every row below a directory
    deeper than discovery_scan.rs's MAX_UNIT_DEPTH removed (a DEPTH row excludes its unit and below). An entry is
    `over-item-5` only when that lower bound exceeds 100,000 rows, a 4 MiB canonical descriptor or 8 GiB; every other
    entry is measured at its conservative price, with its margins against each cap set given.

Usage: snapshot_ledger_census.py --architecture <arch> --packages-root <python-packages checkout> --t2-cache <cache>
       [--term-a <term_a_r2.output.json>] [--caps NAME:OBJECTS,EDGES,BYTES ...]  (a cap given as - is not tested)
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
VCS = ('.git', '.hg', '.svn', '.jj')


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def canonical(value):
    """The identity crate's canonical JSON for strings, integers, objects and arrays (sorted keys, no whitespace,
    non-ASCII raw, control characters escaped)."""
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def item5(handed, sizes, slm):
    """Rows, total bytes and the canonical descriptor's length (C1a3's record, with placeholder digests)."""
    rows = len(handed)
    total = sum(sizes)
    inventory = 2 + max(0, rows - 1)
    for path, size in zip(handed, sizes):
        inventory += len(canonical(dict(bytes=size, path=path, sha256='0' * 64)))
    envelope = canonical(dict(projectId='prj1-' + '0' * 64, resolvedConfigDigest='0' * 64, schemaVersion=2,
                              scopeDigest='0' * 64, sourceInventory=[], vcsDigest='0' * 64))
    descriptor = len(envelope) - 2 + inventory
    over = [f for f, v, limit in (('rows', rows, slm.MAX_ROWS), ('descriptor', descriptor, slm.MAX_DESCRIPTOR),
                                  ('totalBytes', total, None)) if limit is not None and v > limit]
    return dict(rows=rows, totalBytes=total, descriptorBytes=descriptor), over


def parse_caps(text):
    name, _, values = text.partition(':')
    return name, tuple(None if v == '-' else int(v) for v in values.split(','))


def main():
    ap = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    ap.add_argument('--architecture', type=Path, required=True)
    ap.add_argument('--packages-root', type=Path, required=True)
    ap.add_argument('--t2-cache', type=Path, required=True)
    ap.add_argument('--term-a', type=Path)
    ap.add_argument('--caps', action='append', type=parse_caps, default=[])
    a = ap.parse_args()
    arch = a.architecture.resolve(strict=True)
    dc = load('discovery_census', PRODUCT / 'tools/security/discovery_census.py')
    slm = load('snapshot_ledger_model', PRODUCT / 'tools/security/snapshot_ledger_model.py')
    dm = dc.load_member_model(PRODUCT)
    c, _ = slm.snapshot_costs(PRODUCT, dc)
    s = slm.session_costs(PRODUCT, c)
    _, _, _, rule = dc.load_reference(PRODUCT, arch, a.packages_root.resolve(strict=True))
    rpp = (arch / 'docs/coop/artifacts/rust-provider-protocol.v2.json').read_text()
    marker = '"maxSnapshotTotalFileBytes": '
    total_limit = int(rpp[rpp.index(marker) + len(marker):].split(',', 1)[0])
    unit_depth = re.findall(r'\nconst MAX_UNIT_DEPTH: usize = (\d+);', (PRODUCT / 'crates/security/src/custody/discovery_scan.rs').read_text())
    if len(unit_depth) != 1:
        raise SystemExit('MAX_UNIT_DEPTH anchor')
    unit_depth = int(unit_depth[0])
    caps = dict(a.caps) or {'r8': (slm.SNAPSHOT_OBJECTS, slm.SNAPSHOT_EDGES, None)}
    after = (0, 0, 0)
    after_basis = None
    if a.term_a is not None:
        raw = a.term_a.read_bytes()
        terms = json.loads(raw)['variants']['zeroMember']['terms']
        picked = [terms['sealing (C1a3, pinned)'], terms['leftover capture: one path copy']]
        after = tuple(sum(t[k] for t in picked) for k in ('objects', 'edges', 'bytes'))
        after_basis = dict(path=str(a.term_a.name), sha256=hashlib.sha256(raw).hexdigest(),
                           terms=['sealing (C1a3, pinned)', 'leftover capture: one path copy'])
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

    def per_chunk():
        one = slm.session_cost(c, s, [('a', b'\x01' * chunk)])
        two = slm.session_cost(c, s, [('a', b'\x01' * (2 * chunk))])
        return tuple(y - x for x, y in zip(one, two))

    step = per_chunk()

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
        bounds, _ = item5(paths, sizes, slm)
        # Eligibility, on the admitted extent and its lower bound.
        if found:
            _, _, a_paths, a_sizes = snapshot(tree, admitted, members)
        else:
            a_paths, a_sizes = paths, sizes
        keep = [(p, z) for p, z in zip(a_paths, a_sizes)
                if p.rsplit('/', 1)[-1] not in slm.SnapshotModel.MARKERS and p.count('/') <= unit_depth]
        lower, over = item5([p for p, _ in keep], [z for _, z in keep], slm)
        if lower['totalBytes'] > total_limit:
            over.append('totalBytes')
        row = dict(id=label, members=len(members), admittedBoundaries=len(found),
                   discoveryDepthLimitDirectories=disc.counts['depthLimitDirectories'],
                   item5Conservative=bounds,
                   eligibility=dict(admittedRows=len(a_paths), markerOrDeepRowsRemoved=len(a_paths) - len(keep), lowerBound=lower),
                   walk=dict(objects=walk[0], edges=walk[1], bytes=walk[2]),
                   session=dict(objects=session[0], edges=session[1], bytes=session[2]),
                   objects=cost[0], edges=cost[1], bytes=cost[2],
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

    manifest = json.loads((arch / dc.MANIFEST).read_bytes())
    cache = str(a.t2_cache.resolve(strict=True))
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
    out = dict(schemaVersion=2,
               standing='M3-C r9 input (round 2): the lead-readable T2 census on the snapshot ledger (walk, session, and '
                        'sealing\'s and the leftover capture\'s upper bound), from integrity-verified stores; held-out '
                        'entries never read. Priced with no boundary and every blob new (both conservative) and with the '
                        'D15 members discovery admits; over-item-5 decided on the admitted extent\'s lower bound. Counts '
                        'and ids only. Design evidence, not qualification.',
               manifest=dict(path=dc.MANIFEST, sha256=hashlib.sha256((arch / dc.MANIFEST).read_bytes()).hexdigest()),
               tools={p: hashlib.sha256((PRODUCT / p).read_bytes()).hexdigest() for p in
                      ('tools/security/snapshot_ledger_census.py', 'tools/security/snapshot_ledger_model.py',
                       'tools/security/discovery_census.py', 'tools/security/discovery_member_model.py')},
               afterWalk=dict(objects=after[0], edges=after[1], bytes=after[2], basis=after_basis),
               caps={n: dict(zip(keys, v)) for n, v in caps.items()}, maxUnitDepth=unit_depth,
               counts=dict(entries=len(entries), workspaces=len(workspaces), measured=len(measured),
                           overItem5=len(rows) - len(measured), withMembers=sum(1 for r in rows if r['members']),
                           withAdmittedBoundaries=sum(1 for r in rows if r['admittedBoundaries'])),
               maximaMeasured={k: max((r['fullLedger'][k] for r in measured), default=0) for k in keys},
               maximaAll={k: max((r['fullLedger'][k] for r in rows), default=0) for k in keys},
               maximaAllMountsAsMembers={k: max((r['allMountsAsMembers'][k] for r in workspaces if 'allMountsAsMembers' in r), default=0)
                                         for k in keys},
               failing2x={n: sorted(r['id'] for r in measured if not r['margins'][n]['passes2x']) for n in caps},
               entries=entries, workspaces=workspaces)
    print(json.dumps(out, indent=1, ensure_ascii=True))


if __name__ == '__main__':
    main()
