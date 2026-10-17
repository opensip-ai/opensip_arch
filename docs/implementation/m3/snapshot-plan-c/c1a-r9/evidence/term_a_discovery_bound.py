"""M3-C r9, Q1: is each cap-bounded snapshot term bounded by k times the discovery walk's charge for the same entries?

For each cap-bounded term of term (a) (listed names, link and special-file path copies, directories entered), this
prices one entry's MARGINAL charge under both models' own code, by walking synthetic trees with and without the entry:
the snapshot walk (tools/security/snapshot_ledger_model.py SnapshotModel) and the discovery walk
(tools/security/discovery_census.py Model, the automatic walk B2 runs first over the same root). k per component is the
largest ratio snapshot/discovery over every parent shape the envelopes admit (0 to the depth bound's `target`
segments, the parent at the row-path envelope). It also checks the extent: an entry the snapshot walk lists but the
discovery walk does not list has no discovery charge to bound it.

If the bound holds, term (a') is term (a)'s item-5-bounded terms plus k (the largest over the three terms, per
component) times the discovery ledger's caps, read through the census's anchors. Term (a) itself is read from
term_a.output.json, unchanged.

Usage: term_a_discovery_bound.py --product <worktree> --architecture <arch> --packages-root <python-packages checkout>
"""
import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def anchor(path, pattern):
    hits = re.findall(pattern, Path(path).read_text())
    if len(hits) != 1:
        raise SystemExit('anchor %r matched %d times' % (pattern, len(hits)))
    return hits[0]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--product', type=Path, required=True)
    ap.add_argument('--architecture', type=Path, required=True)
    ap.add_argument('--packages-root', type=Path, required=True)
    a = ap.parse_args()
    P = a.product.resolve()
    slm = load('snapshot_ledger_model', P / 'tools/security/snapshot_ledger_model.py')
    dc = load('discovery_census', P / 'tools/security/discovery_census.py')
    c, _ = slm.snapshot_costs(P, dc)
    _, _, _, rule = dc.load_reference(P, a.architecture.resolve(), a.packages_root.resolve())
    DEPTH = c['MAX_LISTED_DEPTH']
    SEGMENT = 4 * int(anchor(P / 'crates/identity/src/descriptors.rs', r'if part\.chars\(\)\.take\(\d+\)\.count\(\) > (\d+) \{'))
    ROW_PATH = 4 * int(anchor(P / 'crates/identity/src/descriptors.rs', r'if value\.chars\(\)\.take\(\d+\)\.count\(\) > (\d+) \{'))
    D_LIMITS = c['LIMITS']  # (objects, edges, bytes) of the discovery profile, by the census's anchors

    class Textless(dc.Tree):
        def node(self, rel):
            n = super().node(rel)
            if n is not None and n['kind'] == 'file' and 'text' not in n:
                return dict(n, text='')
            return n

    def parent_chain(t, depth_room):
        """A parent directory reached through `t` directories named `target`, then valid segments of the segment
        envelope up to the row-path envelope less one name, within `depth_room` segments."""
        parts = ['target'] * t
        while len(parts) < depth_room:
            used = len('/'.join(parts))
            room = ROW_PATH - SEGMENT - 1 - used - (1 if parts else 0)
            if room <= 0:
                break
            parts.append('p%d' % len(parts) + 'p' * (min(SEGMENT, room) - 1 - len(str(len(parts)))))
        return parts

    def tree_of(parts, extra):
        nodes = {'': dict(kind='dir')}
        rel = ''
        for part in parts:
            rel = slm.join_rel(rel, part)
            nodes[rel] = dict(kind='dir')
        for name, kind in extra:
            node = dict(kind=kind)
            if kind == 'file':
                node['size'] = 0
            nodes[slm.join_rel(rel, name)] = node
        return nodes

    def both(nodes):
        snap = slm.SnapshotModel(c, rule, Textless(nodes), slm.Boundaries({})).walk()
        disc = dc.Model(c, rule, dc.Tree(nodes), 'automatic', []).walk()
        return snap, (disc.objects, disc.edges, disc.bytes_at(0))

    def marginal(parts, entry):
        base = both(tree_of(parts, [('n0' + 'n' * (SEGMENT - 2), 'file')]))
        more = both(tree_of(parts, [('n0' + 'n' * (SEGMENT - 2), 'file'), entry]))
        return tuple(tuple(y - x for x, y in zip(b, m)) for b, m in zip(base, more))

    name = 'n1' + 'n' * (SEGMENT - 2)
    kinds = {'listed name (a link: listed, observed, classified)': (name, 'symlink'),
             'listed name (a special file)': (name, 'fifo'),
             'directory entered (empty)': (name, 'dir')}
    results = {}
    for label, entry in kinds.items():
        worst, rows = [0.0, 0.0, 0.0], []
        for t in range(0, DEPTH - 1):
            parts = parent_chain(t, DEPTH - 1)
            if len(parts) > DEPTH - 1:
                continue
            snap, disc = marginal(parts, entry)
            ratio = [s / d if d else (float('inf') if s else 0.0) for s, d in zip(snap, disc)]
            worst = [max(w, r) for w, r in zip(worst, ratio)]
            if t in (0, 1, 16, 64, 128, DEPTH - 2):
                rows.append(dict(targets=t, depth=len(parts) + 1, snapshot=snap, discovery=disc, ratio=[round(r, 3) for r in ratio]))
        results[label] = dict(k=[round(w, 3) for w in worst], samples=rows)
    # The extent: one level below the depth bound, discovery opens a directory and observes its markers, but never
    # lists it; the snapshot walk lists it.
    # The parent at depth DEPTH + 1: discovery opens it from its parent at the bound and observes its markers only.
    deep = ['d%03d' % i for i in range(DEPTH + 1)]
    snap0, disc0 = both(tree_of(deep, []))
    snap1, disc1 = both(tree_of(deep, [(name, 'symlink')]))
    beyond = dict(parentDepth=len(deep), snapshotMarginal=[y - x for x, y in zip(snap0, snap1)],
                  discoveryMarginal=[y - x for x, y in zip(disc0, disc1)])
    k = [max(r['k'][i] for r in results.values()) for i in range(3)]
    term_a = json.loads((HERE / 'term_a.output.json').read_text())
    bounded = {kk: v for kk, v in term_a['terms'].items() if 'by the caps' not in kk}
    item5 = [sum(v[f] for v in bounded.values()) for f in ('objects', 'edges', 'bytes')]
    a_prime = [item5[i] + int(k[i] * D_LIMITS[i] + 0.999999) for i in range(3)]
    # The bound needs every entry the snapshot walk lists to carry a discovery charge.
    holds = all(d > 0 for d in beyond['discoveryMarginal']) or beyond['snapshotMarginal'] == [0, 0, 0]
    rule2 = {}
    for i, f in enumerate(('objects', 'edges', 'bytes')):
        cap = 1
        while cap < 2 * a_prime[i]:
            cap *= 2
        rule2[f] = cap
    rule5 = {}
    for i, f in enumerate(('objects', 'edges', 'bytes')):
        cap = 1
        while cap < 2 * item5[i]:
            cap *= 2
        rule5[f] = cap
    out = dict(standing='M3-C r9 Q1: the snapshot walk\'s cap-bounded terms against the discovery walk\'s charge for the '
                        'same entries, by both models\' own code. Design evidence, not a cap.',
               discoveryLimits=dict(objects=D_LIMITS[0], edges=D_LIMITS[1], bytes=D_LIMITS[2]),
               perTerm=results, kLargest=k,
               extentBeyondDepthBound=beyond, boundHoldsOverTheWholeExtent=holds,
               item5BoundedTerms=dict(objects=item5[0], edges=item5[1], bytes=item5[2]),
               termAPrimeIfExtentClosed=dict(objects=a_prime[0], edges=a_prime[1], bytes=a_prime[2]),
               powerOfTwoAtTwiceTermAPrime=rule2,
               powerOfTwoAtTwiceItem5BoundedTerms=rule5,
               termA=term_a['total'])
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
