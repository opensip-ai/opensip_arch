"""M3-C r9 round 2, option 3 (the lead's question): the bounded subtotal under three classification remedies.

Not a proposal and no product change: each remedy is modelled on tools/security/snapshot_ledger_model.py's
SnapshotModel by a subclass, and term_a_r2.py's bound (D * the largest charge per frame byte over every row shape,
checked affine form, the same relaxations) is re-run under it, without and with the owner's member limits.
  (a) a `.opensip` name that is not an anchor is classified once: the walk loop reuses the anchor question's result;
  (b) the admitted members' segment lists are charged once per walk (objects = lists, bytes = member segments * 16 +
      lists * RECORD), not on every classification;
  (b') the shared rule's `custody_state` compares each member root with the path's prefix without allocating, so no
      member charge remains, per classification or per walk (the lead's adopted form, with (a));
  (c) the per-`target` Cargo-root prefix copies are not made (the prefix tested as a slice of the path).
For each combination it reports both subtotals and the 2x power-of-two caps (with the round-2 census maxima, an upper
bound on the census under any remedy, since each remedy only removes charges), and which of the accepted snapshot
walk vectors (crates/security/src/snapshot_ledger_vectors.json) would change their predicted charge.

Usage: option3_r2.py --product <worktree> --architecture <arch> --packages-root <checkout> --seal <snapshot_seal.rs>
       --census <census-r2.json>
"""
import argparse
import hashlib
import importlib.util
import json
import sys
from fractions import Fraction
from pathlib import Path

HERE = Path(__file__).resolve().parent
SEAL_BYTES = 16400
SEAL_SHA256 = '7ad4593b5bc9632cce677e978ce1a385b8d0dbb7303bc391a5ad47fad5be71a0'
WIDE = '\U00010000'
COMBINATIONS = {'none': '', 'a': 'a', 'a+b': 'ab', "a+b'": 'ap', 'a+b+c': 'abc'}


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def add(*costs):
    return tuple(sum(c[i] for c in costs) for i in range(3))


def scale(cost, k):
    return tuple(x * k for x in cost)


def blen(text):
    return len(text.encode())


def main():
    ap = argparse.ArgumentParser()
    for flag in ('--product', '--architecture', '--packages-root', '--seal', '--census'):
        ap.add_argument(flag, type=Path, required=True)
    a = ap.parse_args()
    P, A = a.product.resolve(), a.architecture.resolve()
    raw = a.seal.read_bytes()
    if len(raw) != SEAL_BYTES or hashlib.sha256(raw).hexdigest() != SEAL_SHA256:
        raise SystemExit('the sealing source is not the pinned C1a3 candidate')
    slm = load('snapshot_ledger_model', P / 'tools/security/snapshot_ledger_model.py')
    dc = load('discovery_census', P / 'tools/security/discovery_census.py')
    c, _ = slm.snapshot_costs(P, dc)
    s = slm.session_costs(P, c)
    _, _, _, rule = dc.load_reference(P, A, a.packages_root.resolve(strict=True))
    base = json.loads((HERE / 'term_a_r2.output.json').read_bytes())
    lim = base['limits']
    census_raw = a.census.read_bytes()
    census_max = json.loads(census_raw)['maximaMeasured']
    PATH_SCALARS, SEGMENT_SCALARS, SEGMENT = lim['pathScalars'], lim['segmentScalars'], lim['segmentBytes']
    FRAME, ROOM, MAX_T = lim['rowFrameBytesWithoutPath'], lim['rowFrameRoom'], lim['maxTargets']
    MEMBERS, MEMBER_DEPTH = c['MAX_MEMBERS'], c['MAX_DEPTH']
    assert (MEMBERS, MEMBER_DEPTH) == (lim['maxMembers'], lim['memberDepth'])

    class Remedied(slm.SnapshotModel):
        remedies = ''

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.reused = set()

        def member_lists(self):
            lists = [m for m in self.members if m]
            return len(lists), sum(m.count('/') + 1 for m in lists)

        def classify(self, rel):
            if rel in self.reused:  # (a): the anchor question's classification, reused
                self.reused.discard(rel)
                return
            o, e, two, anchors = self.c['SNAPSHOT_CLASSIFY']
            segments = rel.count('/') + 1
            targets = 0 if 'c' in self.remedies else rel.split('/').count('target')
            lists, member_segments = (0, 0) if ('b' in self.remedies or 'p' in self.remedies) else self.member_lists()
            objects = o + targets + lists
            self.add((objects, e, (segments + member_segments) * two + blen(rel) * (anchors + targets) + objects * self.c['RECORD']))

        def custody_anchor(self, rel, known):
            hit = super().custody_anchor(rel, known)
            if not hit and 'a' in self.remedies and rel.split('/')[-1] == '.opensip':
                self.reused.add(rel)
            return hit

        def members_once(self):
            if 'b' not in self.remedies:
                return (0, 0, 0)
            lists, member_segments = self.member_lists()
            two = self.c['SNAPSHOT_CLASSIFY'][2]
            return (lists, 0, member_segments * two + lists * self.c['RECORD'])

        def walk(self):
            self.add(self.members_once())
            return super().walk()

    def model(remedies, members):
        cls = type('M', (Remedied,), dict(remedies=remedies))
        return cls(c, rule, None, None, members=members)

    # The row charge, exactly as term_a_r2.py prices it, under the remedied model.
    o, e = c['OWNED']
    owned = lambda n: (o, e, n + c['RECORD'])
    session_row, reads_row = tuple(base['perRow']['session']), tuple(base['perRow']['reads'])

    def charge(m, f, *args):
        m.cost = [0, 0, 0]
        f(*args)
        return tuple(m.cost)

    def row_cost(m, path):
        _, _, name = path.rpartition('/')
        vo, ve, vb = c['VISIT']
        co, ce, two, tworec = c['CONVERTED_NAME']
        oo, oe, ob = c['OBS']
        listed = add((vo, ve, vb), (co, ce, two * blen(path) + tworec * c['RECORD']), (oo, oe, ob + blen(name)), (0, 0, c['SLOT']))
        anchor_q = charge(m, m.custody_anchor, path, set())
        cls = charge(m, m.classify, path)
        oo2, oe2, ob2 = c['OPEN_REG_1']
        opened = add((oo2, oe2, ob2 + blen(name)), c['STATUS'][:3])
        cap = charge(m, m.capture, path) if name in m.MARKERS else (0, 0, 0)
        return add(listed, anchor_q, cls, opened, cap, session_row, reads_row)

    CLASSES = ['plain', 'target', '.opensip'] + list(slm.SnapshotModel.MARKERS)

    def shape(t, cls, filler, leaf_extra=''):
        if cls == 'target':
            parts = ['target'] * (t - 1) + filler + ['target']
        elif cls == 'plain':
            parts = ['target'] * t + filler + ['x' + leaf_extra]
        else:
            parts = ['target'] * t + filler + [cls]
        return '/'.join(parts)

    def coefficients(m, t, cls):
        p1, p2, p3 = shape(t, cls, ['y']), shape(t, cls, ['yy']), shape(t, cls, ['y', 'y'])
        c1, c2, c3 = row_cost(m, p1), row_cost(m, p2), row_cost(m, p3)
        bL = tuple(y - x for x, y in zip(c1, c2))
        bS = tuple(z - x - 2 * l for x, z, l in zip(c1, c3, bL))
        bleaf = tuple(w - x - l for x, w, l in zip(c1, row_cost(m, shape(t, cls, ['y'], 'x')), bL)) if cls == 'plain' else (0, 0, 0)
        leaf = lambda p: blen(p.rsplit('/', 1)[-1])
        b0 = tuple(x - l * blen(p1) - g * (p1.count('/') + 1) - h * leaf(p1) for x, l, g, h in zip(c1, bL, bS, bleaf))
        formula = lambda p: tuple(b + l * blen(p) + g * (p.count('/') + 1) + h * leaf(p) for b, l, g, h in zip(b0, bL, bS, bleaf))
        checks = [shape(t, cls, [WIDE * 3, 'z', WIDE]), shape(t, cls, ['q'] * 7, WIDE * 9), shape(t, cls, [WIDE * SEGMENT_SCALARS], 'w' * 40)]
        if not (t == 0 and cls in ('plain', '.opensip')):
            checks.append(shape(t, cls, []))
        for p in checks:
            assert formula(p) == row_cost(m, p), 'a row charge is not affine in L, S and the leaf'
        return b0, bL, bS, bleaf

    def length_range(t, cls):
        if cls == 'target':
            lo = 7 * t - 1
        elif cls == 'plain':
            lo = 7 * t + 1
        else:
            lo = 7 * t + blen(cls) + (2 if t == 0 and cls == '.opensip' else 0)
        return lo, 4 * PATH_SCALARS - 18 * t - 3 * max(t - 1, 0)

    def best_ratios(m):
        best = [None, None, None]
        for t in range(0, MAX_T + 1):
            for cls in CLASSES:
                if cls == 'target' and t == 0:
                    continue
                lo, hi = length_range(t, cls)
                if lo > min(hi, PATH_SCALARS):
                    continue
                b0, bL, bS, bleaf = coefficients(m, t, cls)
                for L in sorted({lo, hi} | ({SEGMENT} if lo < SEGMENT < hi else set())):
                    lb = min(L, SEGMENT) if cls == 'plain' else blen(cls)
                    for k in range(3):
                        ratio = (Fraction(b0[k]) + bL[k] * L + bS[k] * Fraction(L + 1, 2) + bleaf[k] * lb) / (FRAME + L)
                        if best[k] is None or ratio > best[k][0]:
                            best[k] = (ratio, dict(targets=t, leaf=cls, pathBytes=L))
        return best

    def member_roots(n, depth):
        return tuple('/'.join(['m%d' % i] + ['s'] * (depth - 1)) for i in range(n))

    variants = {'zeroMember': (), 'memberBounded': member_roots(MEMBERS, MEMBER_DEPTH)}
    fixed_names = ('reads: the payload part of the envelope at 8 GiB', 'session once (buffer, custody admission, listing)',
                   'sealing (C1a3, pinned)', 'root', 'leftover capture: one path copy')
    keys = ('objects', 'edges', 'bytes')

    def caps(subtotal):
        out = {}
        for i, k in enumerate(keys):
            need, cap = 2 * max(subtotal[i], census_max[k]), 1
            while cap < need:
                cap *= 2
            out[k] = cap
        return out

    combos = {}
    for label, remedies in COMBINATIONS.items():
        row = {}
        for vname, members in variants.items():
            m = model(remedies, members)
            best = best_ratios(m)
            rows = tuple(int(-(-(best[k][0] * ROOM) // 1)) for k in range(3))
            fixed = add(*[tuple(base['variants'][vname]['terms'][n][k] for k in keys) for n in fixed_names])
            once = m.members_once()
            subtotal = add(rows, fixed, once)
            row[vname] = dict(dearestShape={k: dict(best[i][1], perFrameByte=float(round(best[i][0], 4))) for i, k in enumerate(keys)},
                              rows=dict(zip(keys, rows)), membersOnce=dict(zip(keys, once)), subtotal=dict(zip(keys, subtotal)),
                              caps=caps(subtotal))
        combos[label] = row
    # The baseline must be term_a_r2.py's own result.
    for vname in variants:
        assert combos['none'][vname]['subtotal'] == base['variants'][vname]['subtotal'], 'the baseline differs from term_a_r2'

    # Which accepted snapshot walk vectors would change their predicted charge.
    vectors = json.loads((P / slm.OUTPUT).read_bytes())
    changed = {label: [] for label in COMBINATIONS if label != 'none'}
    for case in vectors['cases']:
        tree = dc.tree_of_vector(dict(tree=case['tree']))
        members = case.get('members', [])
        acl = slm.acl_paths(case['tree'])
        now = model('', members)
        now.t, now.b, now.acl_paths = tree, slm.Boundaries(case['inventory']), frozenset(acl)
        predicted = now.walk()
        assert predicted == tuple(case['predicted'][k] for k in keys), 'the model no longer reproduces ' + case['id']
        for label, remedies in COMBINATIONS.items():
            if label == 'none':
                continue
            m = model(remedies, members)
            m.t, m.b, m.acl_paths = tree, slm.Boundaries(case['inventory']), frozenset(acl)
            after = m.walk()
            if after != predicted:
                changed[label].append(dict(id=case['id'], delta=dict(zip(keys, (y - x for x, y in zip(predicted, after))))))
    report = dict(standing='M3-C r9 round 2, option 3: the bounded subtotal under three modelled classification remedies '
                  '(not proposals), with the 2x power-of-two caps and the snapshot walk vectors each would change. Design '
                  'evidence, not a cap.',
                  inputs=dict(termA=dict(path='term_a_r2.output.json', sha256=hashlib.sha256((HERE / 'term_a_r2.output.json').read_bytes()).hexdigest()),
                              census=dict(path=a.census.name, sha256=hashlib.sha256(census_raw).hexdigest(), maximaMeasured=census_max),
                              seal=dict(bytes=len(raw), sha256=SEAL_SHA256)),
                  combinations=combos, vectorsChanged=dict(total=len(vectors['cases']), byCombination=changed))
    print(json.dumps(report, indent=1))


if __name__ == '__main__':
    main()
