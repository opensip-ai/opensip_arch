"""M3-C r9, Q2: the pre-walk captures' term.

From the code (crates/host/src/snapshot.rs CaptureSession::capture and its walk visitor):
  - a capture charges SnapshotRoot::open (the opener: its validated path, the root's sample and custody, then per
    directory component its key, observation, open, sample and custody, then the leaf's observation, open, sample and
    a marker's custody), then read_once (the session's per-file charges and the file's read attempts and writes), then
    the capture record;
  - when the walk later reaches the captured path, it charges that row's walk terms in full (listing, open, sample,
    marker custody) but neither a second read nor a second record: the session's per-file charge is paid once, at the
    capture. So a REACHED capture adds only its opener beyond term (a)'s row;
  - a capture the walk never reaches is a LEFTOVER: it refuses at sealing (LeftoverCapture, after charging a copy of
    its path), and costs its opener, its read, its record and that copy.

Which ledger. The law charges B2's marker and manifest reads to the DISCOVERY ledger (snapshot-plan-c/PROPOSAL.md:206),
the snapshot ledger is created only after discovery (:249), and C1a plan r6 says B2's and C2's pre-walk captures use the
discovery ledger (c1a/PLAN-r6.md:119). So on the SNAPSHOT ledger a capture adds nothing (a reached one is the walk's
row, already in term (a), whose per-row session term then over-counts, conservatively), and a leftover adds only the
sealing refusal's path copy, once. The opener, read and record below are DISCOVERY-ledger charges: they are reported
for M3-B, whose census must carry them once J1 routes B2's reads through the session.

The count. B2's captures are of markers B2's discovery walk itself listed and captured (the discovery model's
`capture_markers`: each a regular-file open, a sample and a custody capture on the DISCOVERY ledger). So their number
is at most the discovery ledger's caps over that per-marker charge, read from the census's coefficients. C2's layout
reads have no law bound here (C2 is not yet planned against the snapshot ledger), so they are reported as open.

Usage: captures_term.py --product <worktree> --architecture <arch> --packages-root <python-packages checkout>
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


def add(*costs):
    return tuple(sum(c[i] for c in costs) for i in range(3))


def scale(cost, k):
    return tuple(x * k for x in cost)


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
    s = slm.session_costs(P, c)
    _, _, _, rule = dc.load_reference(P, a.architecture.resolve(), a.packages_root.resolve())
    DEPTH = c['MAX_LISTED_DEPTH']
    ROW_PATH = 4 * int(re.findall(r'if value\.chars\(\)\.take\(\d+\)\.count\(\) > (\d+) \{',
                                  (P / 'crates/identity/src/descriptors.rs').read_text())[0])
    CHUNK = s['READ_CHUNK'][0]
    MARKER_BYTES = c['MAX_CONFIG_BYTES']  # config-file custody: a marker is at most this (SL:126-128)
    D_OBJ, D_EDGE, _ = c['LIMITS']

    # The worst opener: a marker at the discovery depth bound, its path at the row-path envelope.
    marker = 'package.json'
    seg = (ROW_PATH - len(marker)) // DEPTH - 1
    parts = ['d' * seg for _ in range(DEPTH - 1)]
    path = '/'.join(parts + [marker])
    rows = []
    rel = ''
    for part in parts:
        rel = slm.join_rel(rel, part)
        rows.append(dict(kind='dir', path=rel, mode='0755'))
    rows.append(dict(kind='file', path=path, mode='0644', text='{}'))
    opener, _ = slm.opener_cost(c, dc.tree_of_vector(dict(tree=rows)), path, set())
    # A leftover's read, record and refusal copy, at the marker bound.
    o, e = c['OWNED']
    owned = lambda n: (o, e, n + c['RECORD'])
    session_one = slm.session_cost(c, s, [('a', b'\x01')])
    session_none = slm.session_cost(c, s, [])
    per_file = tuple(y - x for x, y in zip(session_none, session_one))
    chunks = -(-MARKER_BYTES // CHUNK)
    leftover = add(opener, per_file, scale(s['ATTEMPT'], 2 * chunks + 2), scale(s['WRITE'], chunks - 1), owned(len(path)))
    # B2's count: one discovery marker capture each (open, sample, custody capture), on the discovery ledger.
    ob, eb, _ = c['OPEN_REG_1']
    d_marker = add((ob, eb, 0), c['STATUS'][:3], c['CAP'][:3], c['FS'][:3])
    b2_count = min(D_OBJ // d_marker[0], D_EDGE // d_marker[1])
    worst = tuple(max(x, y) for x, y in zip(opener, leftover))
    out = dict(standing='M3-C r9 Q2: the pre-walk captures\' term on the snapshot ledger. Design evidence, not a cap.',
               openerWorst=dict(path='%d components, %d bytes' % (len(parts) + 1, len(path)), cost=opener),
               reachedCaptureAddsOnly='the opener (the row and the session are term (a)\'s)',
               leftoverWorst=leftover,
               discoveryPerMarkerCapture=d_marker, b2CaptureCountBound=b2_count,
               snapshotLedgerTerm=dict(zip(('objects', 'edges', 'bytes'), owned(ROW_PATH)),
                                       basis='the leftover refusal\'s path copy at the row-path envelope, once (sealing refuses at the first)'),
               discoveryLedgerTermIfB2ReadsThroughTheSession=dict(zip(('objects', 'edges', 'bytes'), scale(worst, b2_count))),
               c2='open: C2\'s layout reads have no count bound against the snapshot ledger yet')
    print(json.dumps(out, indent=1))


if __name__ == '__main__':
    main()
