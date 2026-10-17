"""M3-C r9 term (a): the explicitly conservative componentwise bound of C1a plan r6 (RF-2 row).

Every operation count is bounded separately, by the bound that limits it, each at its worst branch; (a) is the sum of
the terms, per component (objects, edges, bytes). Every per-operation charge is computed by calling the charge model's
own charging code (tools/security/snapshot_ledger_model.py's SnapshotModel methods and session_costs, over
tools/security/discovery_census.py's verified cost closure), never restated. Every limit is read from the code or the
artifact that enforces it, by anchor:
  - rows 100,000 and the 4 MiB descriptor: the model's MAX_ROWS and MAX_DESCRIPTOR (item 5);
  - 8 GiB: rust-provider-protocol.v2.json maxSnapshotTotalFileBytes (RPP:100; item 5);
  - the object and edge caps 2^20 and 2^21: the model's SNAPSHOT_OBJECTS and SNAPSHOT_EDGES (item 2);
  - a raw listed name's envelope: discovery_walk.rs MAX_COMPONENT_BYTES; a valid segment's and a row path's: the
    LogicalPath scalar limits in identity's descriptors.rs, at four UTF-8 bytes per scalar; the walk depth:
    MAX_LISTED_DEPTH (the census's anchor);
  - the read chunk and the custody, session and row shapes: the model's session anchors;
  - sealing's charges: C1a3's snapshot_seal.rs, read by anchor from --seal (C1a3 is not yet on main).

Usage: term_a.py --product <worktree> --architecture <arch> --seal <path to C1a3's crates/host/src/snapshot_seal.rs>
"""
import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path


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


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--product', type=Path, required=True)
    ap.add_argument('--architecture', type=Path, required=True)
    ap.add_argument('--seal', type=Path, required=True)
    a = ap.parse_args()
    P, A = a.product.resolve(), a.architecture.resolve()
    slm = load('snapshot_ledger_model', P / 'tools/security/snapshot_ledger_model.py')
    dc = load('discovery_census', P / 'tools/security/discovery_census.py')
    c, _ = slm.snapshot_costs(P, dc)
    s = slm.session_costs(P, c)

    # --- the limits, read where they are enforced
    ROWS, DESCRIPTOR = slm.MAX_ROWS, slm.MAX_DESCRIPTOR
    OBJ_CAP, EDGE_CAP = slm.SNAPSHOT_OBJECTS, slm.SNAPSHOT_EDGES
    TOTAL = int(anchor(A / 'docs/coop/artifacts/rust-provider-protocol.v2.json', r'"maxSnapshotTotalFileBytes": (\d+)'))
    RAW_NAME = int(anchor(P / 'crates/security/src/custody/discovery_walk.rs', r'const MAX_COMPONENT_BYTES: usize = (\d+);'))
    PATH_SCALARS = int(anchor(P / 'crates/identity/src/descriptors.rs', r'if value\.chars\(\)\.take\(\d+\)\.count\(\) > (\d+) \{'))
    SEGMENT_SCALARS = int(anchor(P / 'crates/identity/src/descriptors.rs', r'if part\.chars\(\)\.take\(\d+\)\.count\(\) > (\d+) \{'))
    UTF8_MAX = 4  # bytes per Unicode scalar in UTF-8 (RFC 3629)
    ROW_PATH, SEGMENT = PATH_SCALARS * UTF8_MAX, SEGMENT_SCALARS * UTF8_MAX
    DEPTH = c['MAX_LISTED_DEPTH']
    CHUNK = s['READ_CHUNK'][0]
    seal_src = a.seal.read_text()
    for pat in (r'work\.charge::<SealError>\(owned_record\(inventory_len\)\)\?;', r'work\.charge::<SealError>\(owned_record\(160\)\)\?;',
                r'work\.charge::<SealError>\(owned_record\(descriptor_bytes\)\)\?;',
                r'work\.charge::<SealError>\(owned_record\("snapshot2:"\.len\(\) \+ 64\)\)\?;',
                r'\.begin\(inventory\.len\(\) as u64, work\)', r'pending\.write\(chunk, work\)', r'pending\.commit\(work\)'):
        anchor(a.seal, pat)
    VCS_RECORD = int(anchor(a.seal, r'work\.charge::<SealError>\(owned_record\((\d+)\)\)\?;'))

    # --- per-operation charges, by the model's own code
    m = slm.SnapshotModel(c, None, None, None)

    def charge(f, *args):
        m.cost = [0, 0, 0]
        f(*args)
        return tuple(m.cost)

    def listed(rel, name):
        """One listed name in `enter`, then its classification in the walk loop: its visit, converted copies,
        observation, slot bytes, and `classify_cost` (as SnapshotModel.enter and .walk charge them)."""
        vo, ve, vb = c['VISIT']
        co, ce, two, tworec = c['CONVERTED_NAME']
        oo, oe, ob = c['OBS']
        child = slm.join_rel(rel, name)
        return add((vo, ve, vb), (co, ce, two * (len(rel) + 1 + len(name)) + tworec * c['RECORD']),
                   (oo, oe, ob + len(name)), (0, 0, c['SLOT']), charge(m.classify, child))

    def directory_frame(rel, name):
        """Entering one directory: its open, sample, custody capture, frame slot, listing (with `.` and `..`), the
        slots record and a Cargo key at the parent's envelope."""
        o, e, b = c['OPEN_DIR']
        return add((o, e, b + len(name)), c['STATUS'][:3], charge(m.capture, slm.join_rel(rel, name)), charge(m.owned, 0),
                   c['LISTING'][:3], scale(c['VISIT'], 2), charge(m.owned, 0), charge(m.owned, len(slm.join_rel(rel, name)) + 1))

    def row_open(name):
        """A handed regular file: its open, sample and (a marker's) custody capture, at its dearer branch."""
        o, e, b = c['OPEN_REG_1']
        return add((o, e, b + len(name)), c['STATUS'][:3], charge(m.capture, name))

    def parent_at(t):
        """A parent path at the row-path envelope less one valid name: `t` segments named `target`, then valid
        segments of the segment envelope, within the depth bound; None when that cannot be formed."""
        parts, length = ['target'] * t, 7 * t
        room = ROW_PATH - SEGMENT - 1
        while length < room and len(parts) < DEPTH - 1:
            seg = 'p' * min(SEGMENT, room - length - (1 if parts else 0))
            if not seg:
                break
            parts.append(seg)
            length += len(seg) + (1 if len(parts) > 1 else 0)
        rel = '/'.join(parts)
        return rel if len(rel) <= room and len(parts) < DEPTH else None

    # The worst listed name: a valid name at the segment envelope, under the dearest parent over every `target`
    # count, its count bounded by the object and edge caps through its own coefficients.
    def worst_name():
        best = None
        for t in range(0, DEPTH):
            parent = parent_at(t)
            if parent is None:
                continue
            cost = listed(parent, 'n' * SEGMENT)
            count = min(OBJ_CAP // max(cost[0], 1), EDGE_CAP // max(cost[1], 1))
            total = scale(cost, count)
            if best is None or total[2] > best[2][2]:
                best = (t, cost, total, count)
        return best

    terms = {}
    # 1. Rows: 100,000 handed regular files, each listed, opened, sampled and (as a marker) captured. Their path bytes
    # are bounded jointly by the 4 MiB full descriptor. The per-row fixed charge is taken at a one-byte name, and every
    # path byte at its dearest coefficient (a name byte, a `target` segment at the depth bound, or a new segment).
    minimal = listed('', 'a')
    per_byte = tuple(x - y for x, y in zip(listed('', 'aa'), minimal))
    deep = '/'.join(['target'] * (DEPTH - 2))
    per_byte_targets = tuple(x - y for x, y in zip(listed(deep, 'aa'), listed(deep, 'a')))
    # A new segment costs two path bytes (`/` and one byte), so its coefficient is per two bytes, rounded up.
    per_segment = tuple(-(-(x - y) // 2) for x, y in zip(listed(deep + '/a', 'b'), listed(deep, 'b')))
    dearest = tuple(max(x, y, z) for x, y, z in zip(per_byte, per_byte_targets, per_segment))
    # The canonical row frame `{"bytes":N,"path":"P","sha256":"H"}` without its path is at least 94 bytes plus one
    # digit and the separator; C1a3's row_len counts it, read here from the sealing source's literals.
    frame = (len('{"bytes":') + 1 + len(',"path":') + 2 + len(',"sha256":') + 66 + 1) + 1
    # 100,000 minimal frames alone exceed 4 MiB, so the rows' framing cannot be subtracted for every row: bounded
    # separately and conservatively, the rows' path bytes are at most the descriptor's own bytes.
    path_budget = DESCRIPTOR
    terms['rows: listed, opened, sampled and captured'] = add(scale(add(minimal, row_open('a')), ROWS), scale(dearest, path_budget))
    # 2. Read attempts and writes: the envelope 2*ceil(size/chunk)+2 per row, summed at the total bound (at least one
    # EOF attempt per row); one write per chunk.
    chunks = -(-TOTAL // CHUNK) + ROWS
    terms['reads: attempts within the envelope'] = scale(s['ATTEMPT'], 2 * chunks + 2 * ROWS)
    terms['reads: chunk writes into custody'] = scale(s['WRITE'], chunks)
    # 3. The session per row (C1a2's anchors): two samples and the commit's, the pending name and creation, the dearer
    # of a duplicate's unlink and a new blob's digest name, rename and set entry, and the capture record.
    o, e = c['OWNED']
    owned = lambda n: (o, e, n + c['RECORD'])
    name_len = len('pending-%d' % ROWS)
    unique = add(owned(64), (s['RENAME_COST'][0], s['RENAME_COST'][1], name_len + 64 + s['RENAME_COST'][2]), owned(s['SET_ENTRY_SIZE'][0]))
    dup = (s['UNLINK_COST'][0], s['UNLINK_COST'][1], name_len + s['UNLINK_COST'][2])
    per_row = add(scale(c['STATUS'][:3], 3), owned(name_len), (s['CREATE_COST'][0], s['CREATE_COST'][1], name_len + s['CREATE_COST'][2]),
                  tuple(max(x, y) for x, y in zip(unique, dup)), owned(s['CAPTURE_SIZE'][0]))
    terms['session: per row'] = scale(per_row, ROWS)
    terms['session: once (buffer, custody admission, listing)'] = add(s['BUFFER'], s['ACL_CAPTURE'], s['LISTING'], scale(s['VISIT'], 2))
    # 4. Sealing (C1a3): the inventory and descriptor at 4 MiB each, the VCS record, the id, and the inventory blob's
    # custody (one pending entry, its chunk writes, the commit).
    inv_chunks = -(-DESCRIPTOR // CHUNK)
    terms['sealing (C1a3)'] = add(owned(DESCRIPTOR), owned(VCS_RECORD), owned(DESCRIPTOR), owned(len('snapshot2:') + 64),
                                  owned(name_len), (s['CREATE_COST'][0], s['CREATE_COST'][1], name_len + s['CREATE_COST'][2]),
                                  scale(s['WRITE'], inv_chunks), c['STATUS'][:3], unique)
    # 5. The root: its sample, custody and frame, and its listing.
    terms['root'] = add(c['STATUS'][:3], charge(m.capture, ''), charge(m.owned, 0), c['LISTING'][:3], scale(c['VISIT'], 2), charge(m.owned, 0))
    # 6. Directories entered, bounded by the object and edge caps through the frame's own coefficients, at the
    # envelopes (a valid segment under a parent at the row-path envelope).
    frame_cost = directory_frame('p' * (ROW_PATH - SEGMENT - 1), 'd' * SEGMENT)
    dirs = min(OBJ_CAP // frame_cost[0], EDGE_CAP // frame_cost[1])
    terms['directories (by the caps, at the envelopes)'] = scale(frame_cost, dirs)
    # 7. Listed names that are not rows (excluded, pruned, links, specials, directories' own entries), bounded by the
    # caps through the listed name's coefficients, at the worst `target` count and the raw-name envelope.
    t, name_cost, name_total, names = worst_name()
    terms['listed names (by the caps, at the envelopes)'] = name_total
    # 8. Copies: a link's or special file's path record, per listed name, at the row-path envelope.
    copy = charge(m.owned, ROW_PATH)
    copies = min(OBJ_CAP // copy[0], EDGE_CAP // max(copy[1], 1))
    terms['copies: link and special paths (by the caps)'] = scale(copy, copies)
    total = add(*terms.values())
    # Rows alone against item 2's object and edge caps: the cheapest row (a non-marker one-byte name at the root,
    # empty, no capture) and the charged session.
    o_, e_, b_ = c['OPEN_REG_1']
    cheapest = add(minimal, (o_, e_, b_ + 1), c['STATUS'][:3], per_row, s['ATTEMPT'])
    rows_need = scale(cheapest, ROWS)
    rule = {}
    for i, k in enumerate(('objects', 'edges', 'bytes')):
        need, cap = 2 * total[i], 1
        while cap < need:
            cap *= 2
        rule[k] = cap
    report = dict(standing='M3-C r9 term (a): the conservative componentwise bound (C1a plan r6, RF-2). Each term is its '
                  'count at its bound times its worst-branch charge; (a) is their sum. Design evidence for review, not a cap.',
                  limits=dict(rows=ROWS, descriptorBytes=DESCRIPTOR, totalBytes=TOTAL, objectCap=OBJ_CAP, edgeCap=EDGE_CAP,
                              rawNameBytes=RAW_NAME, segmentBytes=SEGMENT, rowPathBytes=ROW_PATH, depth=DEPTH, readChunk=CHUNK,
                              rowFrameBytes=frame, rowPathBudgetBytes=path_budget),
                  counts=dict(directories=dirs, listedNames=names, listedNameTargets=t, copies=copies, chunks=chunks),
                  perOperation=dict(listedNameWorst=name_cost, directoryFrame=frame_cost, rowMinimal=add(minimal, row_open('a')),
                                    rowPathByteDearest=dearest, sessionPerRow=per_row),
                  terms={k: dict(objects=v[0], edges=v[1], bytes=v[2]) for k, v in terms.items()},
                  total=dict(objects=total[0], edges=total[1], bytes=total[2]),
                  rowsAloneAtTheCheapestRow=dict(perRow=cheapest, objects=rows_need[0], edges=rows_need[1], bytes=rows_need[2],
                                                 objectCap=OBJ_CAP, edgeCap=EDGE_CAP),
                  powerOfTwoAtTwiceTermA=rule)
    print(json.dumps(report, indent=1))


if __name__ == '__main__':
    main()
