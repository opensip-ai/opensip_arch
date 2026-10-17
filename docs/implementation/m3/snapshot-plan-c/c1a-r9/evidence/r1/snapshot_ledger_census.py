"""The snapshot ledger's lead-readable T2 census (M3-C r9 input; C1a plan r6, C1a4).

Developer tool only. It imports tools/security/discovery_census.py unchanged (its integrity-verified stores, its
workspace overlays, its cost closure and its reference rule) and tools/security/snapshot_ledger_model.py unchanged (the
snapshot walk's and the capture session's charge model), and prices each LEAD-READABLE T2 repository entry and workspace
of the corpus manifest on the snapshot ledger: the walk, then the session.

Lead-readable only. Held-out entries are never opened: every store is reached through discovery_census.store_path,
which refuses a held-out entry before any filesystem call, and only `heldOut: false` entries and workspaces are visited.
The blind mode is neither called nor changed. Nothing of a tree is written: the output records ids and counts only.

Conservative where the input is unknown:
  - no admitted boundary is applied (boundaries only exclude, so the walk is charged for more, never less);
  - every handed file takes the session's dearer branch (a new blob, never a duplicate's unlink);
  - the walk model already charges every capture at its dearer branch.

Each entry is classified against item 5 first: one over 100,000 rows, a 4 MiB canonical descriptor or 8 GiB is
`over-item-5` (it cannot seal), with no margin. Every other entry reports its objects, edges and bytes, and its 2x
margin against the caps given.

Usage: snapshot_ledger_census.py --architecture <arch> --packages-root <python-packages checkout> --t2-cache <cache>
       [--objects N --edges N --bytes N]
"""
import argparse
import hashlib
import importlib.util
import json
import os
import sys
from pathlib import Path

PRODUCT = Path(__file__).resolve().parent.parent.parent


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


def main():
    ap = argparse.ArgumentParser(description=__doc__, allow_abbrev=False)
    ap.add_argument('--architecture', type=Path, required=True)
    ap.add_argument('--packages-root', type=Path, required=True)
    ap.add_argument('--t2-cache', type=Path, required=True)
    ap.add_argument('--objects', type=int)
    ap.add_argument('--edges', type=int)
    ap.add_argument('--bytes', type=int)
    a = ap.parse_args()
    arch = a.architecture.resolve(strict=True)
    dc = load('discovery_census', PRODUCT / 'tools/security/discovery_census.py')
    slm = load('snapshot_ledger_model', PRODUCT / 'tools/security/snapshot_ledger_model.py')
    c, _ = slm.snapshot_costs(PRODUCT, dc)
    s = slm.session_costs(PRODUCT, c)
    _, _, _, rule = dc.load_reference(PRODUCT, arch, a.packages_root.resolve(strict=True))
    rpp = (arch / 'docs/coop/artifacts/rust-provider-protocol.v2.json').read_text()
    marker = '"maxSnapshotTotalFileBytes": '
    total_limit = int(rpp[rpp.index(marker) + len(marker):].split(',', 1)[0])
    caps = (a.objects or slm.SNAPSHOT_OBJECTS, a.edges or slm.SNAPSHOT_EDGES, a.bytes)
    chunk = s['READ_CHUNK'][0]

    class Textless(dc.Tree):
        """A verified tree as the walk model reads it: a regular file's text is never needed, only its identity."""

        def node(self, rel):
            n = super().node(rel)
            if n is not None and n['kind'] == 'file' and 'text' not in n:
                return dict(n, text='')
            return n

    def per_chunk():
        one = slm.session_cost(c, s, [('a', b'\x01' * chunk)])
        two = slm.session_cost(c, s, [('a', b'\x01' * (2 * chunk))])
        return tuple(y - x for x, y in zip(one, two))

    step = per_chunk()

    def price(tree, label):
        tree = Textless(tree.nodes)
        model = slm.SnapshotModel(c, rule, tree, slm.Boundaries({}))
        walk = model.walk()
        paths = [p for p, _ in model.handed]
        sizes = [tree.nodes[p]['size'] for p in paths]
        # The session at its dearer branch: every file a new blob of one chunk (distinct stand-ins), then each
        # file's chunks beyond one (or none, for an empty file) by the model's own per-chunk charge.
        stand_ins = [(p, b'%d' % i) for i, p in enumerate(paths)]
        session = list(slm.session_cost(c, s, stand_ins))
        for size in sizes:
            extra = -(-size // chunk) - 1
            for i in range(3):
                session[i] += step[i] * extra
        cost = tuple(w + x for w, x in zip(walk, session))
        bounds, over = item5(paths, sizes, slm)
        if bounds['totalBytes'] > total_limit:
            over.append('totalBytes')
        row = dict(id=label, item5=bounds, walk=dict(objects=walk[0], edges=walk[1], bytes=walk[2]),
                   session=dict(objects=session[0], edges=session[1], bytes=session[2]),
                   objects=cost[0], edges=cost[1], bytes=cost[2])
        if over:
            row.update(status='over-item-5', overFields=over)
        else:
            row.update(status='measured')
            margins = {}
            for name, v, cap in zip(('objects', 'edges', 'bytes'), cost, caps):
                if cap is not None:
                    margins[name] = dict(cap=cap, marginPermille=cap * 1000 // max(v, 1), passes2x=2 * v <= cap)
            row['margins'] = margins
            row['passes2x'] = all(m['passes2x'] for m in margins.values())
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
        workspaces.append(price(dc.compose(root_tree, members), ws['id']))
        print('priced', ws['id'], file=sys.stderr, flush=True)
    measured = [r for r in entries + workspaces if r['status'] == 'measured']
    maxima = {k: max((r[k] for r in measured), default=0) for k in ('objects', 'edges', 'bytes')}
    maxima_all = {k: max((r[k] for r in entries + workspaces), default=0) for k in ('objects', 'edges', 'bytes')}
    out = dict(schemaVersion=1,
               standing='M3-C r9 input: the lead-readable T2 census on the snapshot ledger (walk and session), from '
                        'integrity-verified stores; held-out entries never read; boundaries not applied and every blob new '
                        '(both conservative). Counts and ids only. Design evidence, not qualification.',
               manifest=dict(path=dc.MANIFEST, sha256=hashlib.sha256((arch / dc.MANIFEST).read_bytes()).hexdigest()),
               tools={p: hashlib.sha256((PRODUCT / p).read_bytes()).hexdigest() for p in
                      ('tools/security/snapshot_ledger_census.py', 'tools/security/snapshot_ledger_model.py', 'tools/security/discovery_census.py')},
               caps=dict(objects=caps[0], edges=caps[1], bytes=caps[2]),
               counts=dict(entries=len(entries), workspaces=len(workspaces), measured=len(measured),
                           overItem5=len(entries) + len(workspaces) - len(measured)),
               maximaMeasured=maxima, maximaAll=maxima_all, entries=entries, workspaces=workspaces)
    print(json.dumps(out, indent=1, ensure_ascii=True))


if __name__ == '__main__':
    main()
