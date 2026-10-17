"""M3-C r9 round 2: the snapshot ledger's bounded subtotal, from the snapshot's own rules (Codex M3CR9-R1-RF-1, RF-2).

Round 1 (term_a.py, kept as history) bounded the `target` count and the per-byte coefficient by discovery's
MAX_LISTED_DEPTH, a limit the snapshot walk does not have. This derivation uses none of discovery's listing policy:
  - a row path is a LogicalPath: at most 4096 scalars, 255 per segment (identity descriptors.rs), at most four UTF-8
    bytes per scalar; so at most 585 `target` segments (6 scalars each, with their separators);
  - the rows' path bytes are bounded jointly by the 4 MiB full descriptor: every row's canonical frame
    `{"bytes":N,"path":"P","sha256":"H"}` plus its separator is at least 98 bytes plus the path's UTF-8 bytes (one size
    digit; escaping only lengthens it), so the frames of all rows sum to at most D = 4 MiB - (the empty-inventory
    envelope) + 1;
  - hence for each component k, the rows' charge is at most D * max over row shapes of c_k(row) / frame(row): for any
    rows, sum c = sum frame * (c / frame) <= D * max (c / frame). The 100,000-row bound cannot bind (100,000 minimal
    frames exceed D), which the script asserts;
  - each row is charged at its dearest branch: listed (visit, converted copies, observation, slot), classified (twice
    for a `.opensip` name, the custody-anchor question and the walk's), opened, sampled, captured as a marker, and the
    session's dearer branch (a new blob's digest name, rename and set entry, never a duplicate's unlink), with the read
    envelope's per-row attempts and write;
  - for a fixed `target` count t and leaf class, a row's charge is affine in its path bytes L, its segments S and its
    leaf bytes: the coefficients are taken from the model's own charging code by differences on concrete paths and
    checked on further paths with four-byte scalars. S <= (L + 1) / 2 and the leaf's bytes <= min(L, 1020) bound the
    other variables, so the ratio is maximized at an end of L's range or at 1020;
  - D15 member roots (RF-2): `classify_cost` adds one object and 16 bytes per member-root segment for every member on
    every classification. The variant `memberBounded` takes the owner's limits: at most MAX_MEMBERS (64) admitted
    members, each at most MAX_DEPTH (256) segments (crates/security/src/custody/workspace_declarations.rs: MAX_MEMBERS
    at :30, refused at :875 and :1024; MAX_DEPTH at :32, refused at :678), both read through the census's anchors. The
    variant `zeroMember` is a repository or workspace with no admitted member.

Sealing is C1a3's candidate `crates/host/src/snapshot_seal.rs`, pinned by length and SHA-256 (Codex M3CR9-R1-NBO-1);
the derivation must be redone if C1a3's review changes a charged site. Codex's counterexample (580 `target`
directories, 1,000 empty leaves n000..n999 of 4,064 scalars) is priced by the model's own walk and session as a
regression case. The cap-bounded terms (directories, names that are not rows, link and special-file copies) are
recomputed at the LogicalPath envelopes for reference: they are the typed-refusal regime, not part of the subtotal.

Usage: term_a_r2.py --product <worktree> --architecture <arch> --packages-root <checkout> --seal <snapshot_seal.rs>
"""
import argparse
import hashlib
import importlib.util
import json
import re
import sys
from fractions import Fraction
from pathlib import Path

SEAL_BYTES = 16400
SEAL_SHA256 = '7ad4593b5bc9632cce677e978ce1a385b8d0dbb7303bc391a5ad47fad5be71a0'  # C1a3 r2 (Codex C1A3-R1-RF-1)
WIDE = '\U00010000'  # one Unicode scalar of four UTF-8 bytes


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def anchor(path, pattern):
    hits = re.findall(pattern, Path(path).read_text())
    if len(hits) != 1:
        raise SystemExit('anchor %r matched %d times in %s' % (pattern, len(hits), path))
    return hits[0]


def add(*costs, times=1):
    return tuple(sum(c[i] for c in costs) * times for i in range(3))


def scale(cost, k):
    return tuple(x * k for x in cost)


def blen(text):
    return len(text.encode())


def canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--product', type=Path, required=True)
    ap.add_argument('--architecture', type=Path, required=True)
    ap.add_argument('--packages-root', type=Path, required=True)
    ap.add_argument('--seal', type=Path, required=True)
    a = ap.parse_args()
    P, A = a.product.resolve(), a.architecture.resolve()
    seal_raw = a.seal.read_bytes()
    if len(seal_raw) != SEAL_BYTES or hashlib.sha256(seal_raw).hexdigest() != SEAL_SHA256:
        raise SystemExit('the sealing source is not the pinned C1a3 candidate')
    slm = load('snapshot_ledger_model', P / 'tools/security/snapshot_ledger_model.py')
    dc = load('discovery_census', P / 'tools/security/discovery_census.py')
    # The census's descriptor recipe, from this record's byte copy of the C1a4 candidate (not on main).
    census = load('snapshot_ledger_census', Path(__file__).resolve().parent / 'snapshot_ledger_census.py')
    c, _ = slm.snapshot_costs(P, dc)
    s = slm.session_costs(P, c)
    _, _, _, rule = dc.load_reference(P, A, a.packages_root.resolve(strict=True))

    # --- the limits, read where they are enforced
    ROWS, DESCRIPTOR = slm.MAX_ROWS, slm.MAX_DESCRIPTOR
    OBJ_CAP, EDGE_CAP = slm.SNAPSHOT_OBJECTS, slm.SNAPSHOT_EDGES
    TOTAL = int(anchor(A / 'docs/coop/artifacts/rust-provider-protocol.v2.json', r'"maxSnapshotTotalFileBytes": (\d+)'))
    PATH_SCALARS = int(anchor(P / 'crates/identity/src/descriptors.rs', r'if value\.chars\(\)\.take\(\d+\)\.count\(\) > (\d+) \{'))
    SEGMENT_SCALARS = int(anchor(P / 'crates/identity/src/descriptors.rs', r'if part\.chars\(\)\.take\(\d+\)\.count\(\) > (\d+) \{'))
    UTF8_MAX = 4  # bytes per Unicode scalar in UTF-8 (RFC 3629)
    ROW_PATH, SEGMENT = PATH_SCALARS * UTF8_MAX, SEGMENT_SCALARS * UTF8_MAX
    MEMBERS, MEMBER_DEPTH = c['MAX_MEMBERS'], c['MAX_DEPTH']
    decl = P / 'crates/security/src/custody/workspace_declarations.rs'
    anchor(decl, r'(if parts\.len\(\) > MAX_DEPTH \{\n\s+return Ok\(Some\(\(false, "DEPTH"\)\)\);)')
    anchor(decl, r'(if provisional\.len\(\) > MAX_MEMBERS \{)')
    anchor(decl, r'(if placed_ok\.len\(\) > MAX_MEMBERS \{)')
    CHUNK = s['READ_CHUNK'][0]
    for pat in (r'work\.charge::<SealError>\(owned_record\(leftover\.len\(\)\)\)\?;',
                r'work\.charge::<SealError>\(owned_record\(inventory_len\)\)\?;', r'work\.charge::<SealError>\(owned_record\(160\)\)\?;',
                r'work\.charge::<SealError>\(owned_record\(descriptor_bytes\)\)\?;',
                r'work\.charge::<SealError>\(owned_record\("snapshot2:"\.len\(\) \+ 64\)\)\?;',
                r'\.begin\(inventory\.len\(\) as u64, work\)', r'pending\.write\(chunk, work\)', r'pending\.commit\(work\)'):
        anchor(a.seal, pat)
    VCS_RECORD = int(anchor(a.seal, r'work\.charge::<SealError>\(owned_record\((\d+)\)\)\?;'))
    # The row frame without its path, at one size digit, plus the separator; and the descriptor's room for row frames.
    FRAME = len(canonical(dict(bytes=0, path='', sha256='0' * 64))) + 1
    envelope = len(canonical(dict(projectId='prj1-' + '0' * 64, resolvedConfigDigest='0' * 64, schemaVersion=2,
                                  scopeDigest='0' * 64, sourceInventory=[], vcsDigest='0' * 64)))
    ROOM = DESCRIPTOR - envelope + 1
    # The descriptor recipe is the census's (C1a3's record): check this room against it at one row.
    assert census.item5(['a'], [0], slm)[0]['descriptorBytes'] == envelope + FRAME + 1 - 1
    assert ROWS * (FRAME + 1) > ROOM, 'the row-count bound could bind'
    MAX_T = (PATH_SCALARS + 1) // 7  # 6 scalars per `target`, a separator between segments

    o, e = c['OWNED']
    owned = lambda n: (o, e, n + c['RECORD'])
    name_len = len('pending-%d' % ROWS)
    unique = add(owned(64), (s['RENAME_COST'][0], s['RENAME_COST'][1], name_len + 64 + s['RENAME_COST'][2]), owned(s['SET_ENTRY_SIZE'][0]))
    dup = (s['UNLINK_COST'][0], s['UNLINK_COST'][1], name_len + s['UNLINK_COST'][2])
    session_row = add(scale(c['STATUS'][:3], 3), owned(name_len), (s['CREATE_COST'][0], s['CREATE_COST'][1], name_len + s['CREATE_COST'][2]),
                      tuple(max(x, y) for x, y in zip(unique, dup)), owned(s['CAPTURE_SIZE'][0]))
    # The read envelope 2*ceil(size/chunk)+2 attempts and ceil(size/chunk) writes: per row 4 attempts and one write,
    # and, over all rows, 2*TOTAL/chunk attempts and TOTAL/chunk writes.
    reads_row = add(scale(s['ATTEMPT'], 4), s['WRITE'])
    payload_chunks = -(-TOTAL // CHUNK)
    reads_payload = add(scale(s['ATTEMPT'], 2 * payload_chunks), scale(s['WRITE'], payload_chunks))

    def model(members):
        return slm.SnapshotModel(c, rule, None, None, members=members)

    def charge(m, f, *args):
        m.cost = [0, 0, 0]
        f(*args)
        return tuple(m.cost)

    def row_cost(m, path):
        """One handed regular file at `path`: listed in its parent (visit, converted copies, observation, slot),
        the `.opensip` anchor question, its classification, open, sample, a marker's capture; its session and reads."""
        parent, _, name = path.rpartition('/')
        vo, ve, vb = c['VISIT']
        co, ce, two, tworec = c['CONVERTED_NAME']
        oo, oe, ob = c['OBS']
        listed = add((vo, ve, vb), (co, ce, two * blen(path) + tworec * c['RECORD']), (oo, oe, ob + blen(name)), (0, 0, c['SLOT']))
        anchor_q = charge(m, m.custody_anchor, path, set())
        assert not (name == '.opensip' and rule.classify_path(path, set(), m.members)), 'a custody anchor is not a row'
        cls = charge(m, m.classify, path)
        oo2, oe2, ob2 = c['OPEN_REG_1']
        opened = add((oo2, oe2, ob2 + blen(name)), c['STATUS'][:3])
        cap = charge(m, m.capture, path) if name in m.MARKERS else (0, 0, 0)
        return add(listed, anchor_q, cls, opened, cap, session_row, reads_row)

    targets = lambda t: ['target'] * t
    # Leaf classes: a plain name (not `target`), a name `target` (counted among the t), `.opensip` (classified twice),
    # and each marker (captured).
    CLASSES = [('plain', None), ('target', 'target'), ('.opensip', '.opensip')] + [(mk, mk) for mk in slm.SnapshotModel.MARKERS]

    def shape(t, cls, filler, leaf_extra=''):
        """A concrete path with t `target` segments (the leaf among them for class `target`), the filler segments, and
        the class's leaf (a plain leaf `x` + leaf_extra)."""
        if cls == 'target':
            parts = targets(t - 1) + filler + ['target']
        elif cls == 'plain':
            parts = targets(t) + filler + ['x' + leaf_extra]
        else:
            parts = targets(t) + filler + [cls]
        return '/'.join(parts)

    def coefficients(m, t, cls):
        """c(L, S, lb) = base + bL*L + bS*S + bleaf*lb for this t and class, by differences of the model's charge."""
        p1 = shape(t, cls, ['y'])
        p2 = shape(t, cls, ['yy'])
        p3 = shape(t, cls, ['y', 'y'])
        c1, c2, c3 = row_cost(m, p1), row_cost(m, p2), row_cost(m, p3)
        bL = tuple(y - x for x, y in zip(c1, c2))
        bS = tuple(z - x - 2 * l for x, z, l in zip(c1, c3, bL))
        if cls == 'plain':
            c4 = row_cost(m, shape(t, cls, ['y'], 'x'))
            bleaf = tuple(w - x - l for x, w, l in zip(c1, c4, bL))
        else:
            bleaf = (0, 0, 0)
        leaf = lambda p: blen(p.rsplit('/', 1)[-1])
        base = tuple(x - l * blen(p1) - g * (p1.count('/') + 1) - h * leaf(p1) for x, l, g, h in zip(c1, bL, bS, bleaf))
        formula = lambda p: tuple(b + l * blen(p) + g * (p.count('/') + 1) + h * leaf(p) for b, l, g, h in zip(base, bL, bS, bleaf))
        # Checked on paths of four-byte scalars, many segments and a long leaf.
        checks = [shape(t, cls, [WIDE * 3, 'z', WIDE]), shape(t, cls, ['q'] * 7, WIDE * 9), shape(t, cls, [WIDE * SEGMENT_SCALARS], 'w' * 40)]
        if not (t == 0 and cls in ('plain', '.opensip')):
            checks.append(shape(t, cls, []))  # the spelling without filler (a root `.opensip` is an anchor, not a row)
        for p in checks:
            assert formula(p) == row_cost(m, p), 'a row charge is not affine in L, S and the leaf'
        return base, bL, bS, bleaf

    def length_range(t, cls):
        """The row path's UTF-8 bytes for this t and class: its shortest spelling, and the LogicalPath envelope
        4N - 18t - 3(S - 1) with S - 1 >= t - 1."""
        if cls == 'target':
            lo = 7 * t - 1
        elif cls == 'plain':
            lo = 7 * t + 1
        else:
            lo = 7 * t + blen(cls) + (2 if t == 0 and cls == '.opensip' else 0)  # a root `.opensip` is an anchor
        hi = UTF8_MAX * PATH_SCALARS - 18 * t - 3 * max(t - 1, 0)
        return lo, hi

    def best_ratios(members, classes=CLASSES):
        m = model(members)
        best = [None, None, None]
        for t in range(0, MAX_T + 1):
            for cls, _ in classes:
                if cls == 'target' and t == 0:
                    continue
                lo, hi = length_range(t, cls)
                if lo > min(hi, PATH_SCALARS):  # the shortest spelling is ASCII: its bytes are its scalars
                    continue
                base, bL, bS, bleaf = coefficients(m, t, cls)
                leaf_fixed = 0 if cls == 'plain' else blen(cls)
                for L in sorted({lo, hi} | ({SEGMENT} if lo < SEGMENT < hi else set())):
                    lb = min(L, SEGMENT) if cls == 'plain' else leaf_fixed
                    for k in range(3):
                        value = Fraction(base[k]) + bL[k] * L + bS[k] * Fraction(L + 1, 2) + bleaf[k] * lb
                        ratio = value / (FRAME + L)
                        if best[k] is None or ratio > best[k][0]:
                            best[k] = (ratio, dict(targets=t, leaf=cls, pathBytes=L))
        return best

    def member_roots(n, depth):
        return tuple('/'.join(['m%d' % i] + ['s'] * (depth - 1)) for i in range(n))

    variants = {'zeroMember': (), 'memberBounded': member_roots(MEMBERS, MEMBER_DEPTH)}
    m0 = model(())
    root = add(c['STATUS'][:3], charge(m0, m0.capture, ''), owned(0), c['LISTING'][:3], scale(c['VISIT'], 2), owned(0))
    once = add(s['BUFFER'], s['ACL_CAPTURE'], s['LISTING'], scale(s['VISIT'], 2))
    inv_chunks = -(-DESCRIPTOR // CHUNK)
    sealing = add(owned(DESCRIPTOR), owned(VCS_RECORD), owned(DESCRIPTOR), owned(len('snapshot2:') + 64), owned(name_len),
                  (s['CREATE_COST'][0], s['CREATE_COST'][1], name_len + s['CREATE_COST'][2]), scale(s['WRITE'], inv_chunks),
                  c['STATUS'][:3], tuple(max(x, y) for x, y in zip(unique, dup)))  # the commit's one sample
    leftover = owned(ROW_PATH)  # sealing's first leftover capture refuses after one copy of its path
    results, sensitivity = {}, {}
    for vname, members in variants.items():
        # Sensitivity only: the rows' term were a `.opensip` name classified once (a code change r9 does not propose).
        alt = best_ratios(members, [x for x in CLASSES if x[0] != '.opensip'])
        alt_rows = tuple(int(-(-(alt[k][0] * ROOM) // 1)) for k in range(3))
        best = best_ratios(members)
        rows = tuple(int(-(-(best[k][0] * ROOM) // 1)) for k in range(3))
        terms = {'rows (descriptor-bounded, dearest shape per component)': rows,
                 'reads: the payload part of the envelope at 8 GiB': reads_payload,
                 'session once (buffer, custody admission, listing)': once,
                 'sealing (C1a3, pinned)': sealing, 'root': root, 'leftover capture: one path copy': leftover}
        subtotal = add(*terms.values())
        results[vname] = dict(members=dict(count=len(members), segmentsEach=(members[0].count('/') + 1) if members else 0),
                              dearestShape={k: dict(best[i][1], perFrameByte=float(round(best[i][0], 4)))
                                            for i, k in enumerate(('objects', 'edges', 'bytes'))},
                              terms={k: dict(objects=v[0], edges=v[1], bytes=v[2]) for k, v in terms.items()},
                              subtotal=dict(objects=subtotal[0], edges=subtotal[1], bytes=subtotal[2]))
        alt_sub = add(alt_rows, *[v for k, v in terms.items() if not k.startswith('rows')])
        sensitivity[vname] = dict(dearestShape={k: dict(alt[i][1], perFrameByte=float(round(alt[i][0], 4)))
                                                for i, k in enumerate(('objects', 'edges', 'bytes'))},
                                  rows=dict(zip(('objects', 'edges', 'bytes'), alt_rows)),
                                  subtotal=dict(zip(('objects', 'edges', 'bytes'), alt_sub)))

    # --- the regression case (Codex M3CR9-R1-RF-1): 580 `target` directories, 1,000 empty leaves n000..n999
    def priced(nodes):
        tree = dc.Tree(nodes)
        m = slm.SnapshotModel(c, rule, tree, slm.Boundaries({}))
        walk = m.walk()
        session = slm.session_cost(c, s, [(p, b'%d' % i) for i, (p, _) in enumerate(m.handed)])
        return add(walk, session), [p for p, _ in m.handed]

    chain = {'': dict(kind='dir')}
    rel = ''
    for _ in range(580):
        rel = slm.join_rel(rel, 'target')
        chain[rel] = dict(kind='dir')
    leaves = dict(chain)
    for i in range(1000):
        leaves[rel + '/n%03d' % i] = dict(kind='file', size=0, text='')
    full, handed = priced(leaves)
    bare, _ = priced(chain)
    rows_part = tuple(x - y for x, y in zip(full, bare))
    bounds, over = census.item5(handed, [0] * len(handed), slm)
    case_m = model(())
    classify_alone = scale(charge(case_m, case_m.classify, handed[0]), len(handed))
    regression = dict(rows=len(handed), rowPathScalars=len(handed[0]), item5=bounds, overItem5=over,
                      classificationAlone=classify_alone, rowsPart=rows_part, directoriesPart=bare,
                      ledgerWithSealing=add(full, sealing, leftover),
                      rowsPartWithinRowTerm={v: all(x <= results[v]['terms']['rows (descriptor-bounded, dearest shape per component)'][k]
                                                    for x, k in zip(rows_part, ('objects', 'edges', 'bytes'))) for v in results})

    # --- the cap-bounded terms, for reference (the typed-refusal regime), at r8's caps and the LogicalPath envelopes
    def parent_at(t, room_scalars):
        """t `target` segments, then segments of 255 four-byte scalars, within room_scalars scalars."""
        parts, used = targets(t), 7 * t - (1 if t else 0)
        while True:
            free = room_scalars - used - (1 if parts else 0)
            if free <= 0:
                break
            parts.append(WIDE * min(SEGMENT_SCALARS, free))
            used += min(SEGMENT_SCALARS, free) + (1 if len(parts) > 1 else 0)
        return '/'.join(parts)

    def listed(m, parent, name):
        child = slm.join_rel(parent, name)
        vo, ve, vb = c['VISIT']
        co, ce, two, tworec = c['CONVERTED_NAME']
        oo, oe, ob = c['OBS']
        return add((vo, ve, vb), (co, ce, two * blen(child) + tworec * c['RECORD']), (oo, oe, ob + blen(name)), (0, 0, c['SLOT']),
                   charge(m, m.custody_anchor, child, set()), charge(m, m.classify, child))

    reference = {}
    for vname, members in variants.items():
        m = model(members)
        name = WIDE * SEGMENT_SCALARS
        best = None
        for t in range(0, MAX_T):
            if 7 * t - 1 > PATH_SCALARS - SEGMENT_SCALARS - 1:
                break
            parent = parent_at(t, PATH_SCALARS - SEGMENT_SCALARS - 1)
            cost = listed(m, parent, name)
            count = min(OBJ_CAP // max(cost[0], 1), EDGE_CAP // max(cost[1], 1))
            if best is None or cost[2] * count > best[2][2]:
                best = (t, cost, scale(cost, count), count)
        dparent = parent_at(0, PATH_SCALARS - SEGMENT_SCALARS - 1)
        dname = WIDE * SEGMENT_SCALARS
        od, ed, bd = c['OPEN_DIR']
        dchild = slm.join_rel(dparent, dname)
        frame = add((od, ed, bd + blen(dname)), c['STATUS'][:3], charge(m, m.capture, dchild), owned(0), c['LISTING'][:3],
                    scale(c['VISIT'], 2), owned(0), owned(blen(dchild) + 1))
        dirs = min(OBJ_CAP // frame[0], EDGE_CAP // frame[1])
        copy = owned(ROW_PATH)
        copies = min(OBJ_CAP // copy[0], EDGE_CAP // max(copy[1], 1))
        terms = {'directories': scale(frame, dirs), 'listed names that are not rows': best[2], 'link and special-file copies': scale(copy, copies)}
        reference[vname] = dict(counts=dict(directories=dirs, listedNames=best[3], listedNameTargets=best[0], copies=copies),
                                terms={k: dict(objects=v[0], edges=v[1], bytes=v[2]) for k, v in terms.items()},
                                sum=dict(zip(('objects', 'edges', 'bytes'), add(*terms.values()))))

    def rule2x(*bounds):
        out = {}
        for i, k in enumerate(('objects', 'edges', 'bytes')):
            need, cap = 2 * max(b[i] for b in bounds), 1
            while cap < need:
                cap *= 2
            out[k] = cap
        return out

    report = dict(standing='M3-C r9 round 2: the snapshot ledger\'s item-5-bounded subtotal from the snapshot\'s own rules '
                  '(LogicalPath and the 4 MiB descriptor; no discovery depth), at the dearest branch per row, without and '
                  'with the owner\'s member-root limits; Codex\'s counterexample as a regression case; the cap-bounded '
                  'terms for reference. Design evidence for review, not a cap.',
                  seal=dict(path='crates/host/src/snapshot_seal.rs (C1a3 candidate)', bytes=len(seal_raw), sha256=SEAL_SHA256),
                  limits=dict(rows=ROWS, descriptorBytes=DESCRIPTOR, totalBytes=TOTAL, pathScalars=PATH_SCALARS,
                              segmentScalars=SEGMENT_SCALARS, rowPathBytes=ROW_PATH, segmentBytes=SEGMENT, maxTargets=MAX_T,
                              rowFrameBytesWithoutPath=FRAME, envelopeBytes=envelope, rowFrameRoom=ROOM, readChunk=CHUNK,
                              maxMembers=MEMBERS, memberDepth=MEMBER_DEPTH, r8ObjectCap=OBJ_CAP, r8EdgeCap=EDGE_CAP),
                  perRow=dict(session=session_row, reads=reads_row), variants=results, regression=regression,
                  capBoundedReference=reference,
                  sensitivityOpensipClassifiedOnce=dict(standing='not a proposal: the subtotal were a `.opensip` name '
                                                        'classified once', **sensitivity),
                  powerOfTwoAtTwice={v: rule2x(tuple(results[v]['subtotal'][k] for k in ('objects', 'edges', 'bytes'))) for v in results})
    print(json.dumps(report, indent=1))


if __name__ == '__main__':
    main()
