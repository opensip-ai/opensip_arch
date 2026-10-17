"""SD-9's read-only checks and its edge and object model.

Usage: check_sd9.py [--product PATH] [--rev REV]
- PATH is the product checkout (default /Users/sb/code/opensip-ai/opensip), read only. REV (default 274dccc,
  product main with C2a-3k) names the commit whose sources are read with read-only `git show`.

It does three things, and writes nothing but its JSON report on standard output:
1. Pins every authority README.md cites (bytes and SHA-256), and checks each quoted anchor is present at its pin.
2. Reads, from the product sources at REV, every price constant the model uses: the three profiles' caps, C2a-3k's
   `digest_cost` and `COMPARISON_COST`, the snapshot session's `READ_CHUNK`, D3a-0's `descend_cost`, FS's
   `status_read_cost` and `descriptor_acl_capture_cost` edges (with `MAX_ENTRIES`). Nothing is typed in by hand: an
   anchor that does not match fails the run.
3. Evaluates README §3's edge and object terms over illustrative tree shapes, and reports, for each shape, the
   largest total file size whose R10a edge total fits each existing profile's edge cap. The shapes are
   illustrations of the model, not a census and not caps (README §5).

Deterministic. Run with python3 -I -B.
"""
import hashlib, json, math, re, subprocess, sys
from pathlib import Path

A = Path(__file__).resolve().parents[6]
args = list(sys.argv[1:])


def opt(name, default):
    if name in args:
        i = args.index(name)
        value = args[i + 1]
        del args[i:i + 2]
        return value
    return default


W = Path(opt('--product', '/Users/sb/code/opensip-ai/opensip'))
REV = opt('--rev', '274dccc')
M3 = 'docs/implementation/m3/'


def show(path):
    return subprocess.run(['git', '-C', str(W), 'show', '%s:%s' % (REV, path)], check=True, capture_output=True).stdout


def pin(path, raw):
    return {'path': path, 'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


# 1. Authorities and their quoted anchors.
ARCH = {
    M3 + 'supervisor-d/d4/PLAN-r2.md': ['**LD-D4-SD9. SD-9 is the lead\'s owed successor (Q6).**',
                                        '**LD-D4-8. The admission algorithm (RF-1, Q8).**',
                                        '**LD-D4-10. The prices (RF-1).**', '**LD-D4-13. The reserved list'],
    M3 + 'supervisor-d/d4/PLAN-r1.md': ['- **X-D4P-1. R10a\'s production work profile: the owner is unnamed.**',
                                        'One provider closure of 100 MB is about 1.6 M edges'],
    M3 + 'reviews/codex-d4-plan-r1/REVIEW.md': ['**Q6:** D4 may consume a borrowed scope without selecting a profile.',
                                                'R10\'s global profile cannot be silently reused for whole-tree R10a verification'],
    M3 + 'reviews/codex-d4-plan-r2/REVIEW.md': ['**Verdict: ACCEPT.**',
                                                'SD-9 still gates production R10a/ER10a, C2a-4 and J3d/J2c'],
    M3 + 'snapshot-plan-c/c2a/PLAN-r4.md': ['| **Q5 ruling** |', '- **LD-C2A-10. The ledger and the costs',
                                            '**C2a-3k,** per Blob one SHA-256 over its slice (edges ⌈len / 64⌉ + 1'],
    M3 + 'component-install/PROPOSAL-r5.md': ['- **`B_open`, opening the capability** (item 6).',
                                              '- **`B_transfer(f)`, one `transfer` of file `f`** (item 6)',
                                              'is an explicit **interim** finite installation policy under cross-law item **X-CI-1**',
                                              '**`Budget`** takes the caller\'s existing budget route',
                                              '**The work profile is the caller\'s:**'],
    M3 + 'component-install/PLAN-r3.md': ['- **LD-CIP-9. The X-CI-1 gate.**', '**So X-CI-1\'s resolution changes both receipts.**'],
    M3 + 'reviews/codex-component-install-r2/REVIEW.md': ['**Q9.** Accept snapshot_profile() as an explicit interim finite installation policy under X-CI-1'],
    M3 + 'host-pipeline-j/PROPOSAL-r7.md': ['| R10a | **(r4, SD-6) Pre-draw component admission.**',
                                            '| 11 | An attempt or admission ledger charge refused | operational-failed / 4 | `SYSTEM.OUTCOME.ILLEGAL_STATE` / host-invariant | `WORK.BUDGET_EXHAUSTED` | none | L468:49 |',
                                            '| 21 | Discovery or snapshot ledger exhausted |', '- **Control J-C10b (r4, SD-6).**',
                                            '    - **(r4, SD-6) ER10a,** R10a\'s ephemeral counterpart'],
    M3 + 'supervisor-d/PROPOSAL-r5.md': ['#### 29. Successor list', '| **SD-6** (r2) | **J1 r4, row R10a** | law amendment to accepted J1 r3'],
    M3 + 'snapshot-plan-c/c1a-r9/RECORD-r9.md': ['The caps are **2^21 objects, 2^24 edges and 2^33 bytes**'],
    'docs/coop/design-corrections/foundation/run-termination-contract.v1.md': ['No §7.5 detail is admitted for an\n  ephemeral attempt either (`RUN_TERMINATION_DETAIL_NOT_ADMITTED`)'],
}
PRODUCT = {
    'crates/platform/src/work_ledger.rs': ['const OBJECT_LIMIT: usize = 65_536;', 'const EDGE_LIMIT: usize = 131_072;',
                                           'const BYTE_LIMIT: usize = 268_435_456;', 'pub fn snapshot_profile() -> Self {',
                                           'A stricter policy may lower any limit, but never raise the global caps.'],
    'crates/security/src/component_closure.rs': ['pub(crate) fn verify_retained_tree(', 'pub(crate) const fn digest_cost(len: usize) -> WorkCost {'],
    'crates/security/src/trust/native_read_session.rs': ['// Law 458c item 6: the read session\'s one ledger.', 'budget: Budget::charged(fence.session()),'],
    'crates/security/src/trust/retained_metadata_index.rs': ['limits: (65536, 131072, 268435456),'],
    'crates/host/src/snapshot.rs': ['pub(crate) const READ_CHUNK: usize = 65_536;'],
    'crates/platform/src/process.rs': ['fn descend_cost(name: usize) -> WorkCost {'],
    'crates/platform/src/filesystem/path_binding.rs': ['pub(super) fn status_read_cost() -> crate::WorkCost {'],
    'crates/platform/src/filesystem/descriptor_acl_capture.rs': ['const MAX_ENTRIES: usize = 128;', 'pub fn descriptor_acl_capture_cost() -> WorkCost {'],
    'crates/host/src/installation_termination.rs': ['Some("WORK.BUDGET_EXHAUSTED")'],
}
report = {'productRev': subprocess.run(['git', '-C', str(W), 'rev-parse', REV], check=True, capture_output=True, text=True).stdout.strip(),
          'authorities': [], 'productSources': []}
for path, anchors in ARCH.items():
    raw = (A / path).read_bytes()
    text = raw.decode()
    missing = [a for a in anchors if a not in text]
    assert not missing, (path, missing)
    report['authorities'].append(pin(path, raw))
SRC = {}
for path, anchors in PRODUCT.items():
    raw = show(path)
    text = raw.decode()
    missing = [a for a in anchors if a not in text]
    assert not missing, (path, missing)
    SRC[path] = text
    report['productSources'].append(pin(path, raw))


# 2. Price constants, read from the sources.
def grab(path, pattern):
    m = re.search(pattern, SRC[path], re.S)
    assert m, (path, pattern)
    return m


def shift_or_int(s):
    s = s.strip().replace('_', '')
    m = re.fullmatch(r'1\s*<<\s*(\d+)', s)
    return 1 << int(m.group(1)) if m else int(s)


WL = 'crates/platform/src/work_ledger.rs'
caps = {}
for name, prefix in (('global', ''), ('discovery', 'DISCOVERY_'), ('snapshot', 'SNAPSHOT_')):
    caps[name] = {k: shift_or_int(grab(WL, r'const %s%s_LIMIT: usize = ([^;]+);' % (prefix, k.upper())).group(1))
                  for k in ('object', 'edge', 'byte')}
cc = SRC['crates/security/src/component_closure.rs']
assert re.search(r'pub\(crate\) const fn digest_cost\(len: usize\) -> WorkCost \{\s*WorkCost \{\s*objects: 0,\s*edges: len\.div_ceil\(64\)\.saturating_add\(1\),\s*bytes: 0,', cc)
assert re.search(r'pub\(crate\) const COMPARISON_COST: WorkCost = WorkCost \{\s*objects: 0,\s*edges: 1,\s*bytes: 0,', cc)
read_chunk = int(grab('crates/host/src/snapshot.rs', r'pub\(crate\) const READ_CHUNK: usize = ([\d_]+);').group(1).replace('_', ''))
desc = grab('crates/platform/src/process.rs', r'fn descend_cost\(name: usize\) -> WorkCost \{\s*WorkCost \{\s*objects: (\d+),\s*edges: (\d+),')
DESC_OBJECTS, DESC_EDGES = int(desc.group(1)), int(desc.group(2))
st = grab('crates/platform/src/filesystem/path_binding.rs', r'fn status_read_cost\(\) -> crate::WorkCost \{\s*crate::WorkCost \{\s*objects: (\d+),\s*edges: (\d+),')
ST_OBJECTS, ST_EDGES = int(st.group(1)), int(st.group(2))
acl = SRC['crates/platform/src/filesystem/descriptor_acl_capture.rs']
max_entries = int(re.search(r'const MAX_ENTRIES: usize = (\d+);', acl).group(1))
cust = re.search(r'pub fn descriptor_acl_capture_cost\(\) -> WorkCost \{\s*WorkCost \{\s*objects: (\d+),\s*edges: 3 \+ MAX_ENTRIES,', acl)
assert cust
CUST_OBJECTS, CUST_EDGES = int(cust.group(1)), 3 + max_entries
report['prices'] = {'caps': caps, 'digestCostEdges': 'ceil(len/64)+1', 'comparisonEdges': 1, 'readChunk': read_chunk,
                    'descend': {'objects': DESC_OBJECTS, 'edges': DESC_EDGES}, 'statusRead': {'objects': ST_OBJECTS, 'edges': ST_EDGES},
                    'custody': {'objects': CUST_OBJECTS, 'edges': CUST_EDGES}}


# 3. README §3's edge and object terms. Every count is CI r5's, C2a r4's or C2a-3k's. CI-A2-b/-c/-d, proposed in CI-2
# r1's SCOPE (in preparation, not pinned here), are included because they only add work, which is conservative.
def lg(x):
    return 0 if x < 2 else math.ceil(math.log2(x))


def env(x):
    return 2 * math.ceil(x / read_chunk) + 2


def digest(x):
    return math.ceil(x / 64) + 1


FOPEN_EDGES = 1 + ST_EDGES


def component(files, dirs, symlinks, depth, body, record):
    """One component: `files` is the list of file lengths, every file at `depth` components (k), `dirs` dir rows,
    `symlinks` symlink rows, the authenticated body's length and the generation record's length R."""
    F, D, S = len(files), dirs, symlinks
    n = F + D + S
    e = {}
    # C2a-1 (LD-C2A-10): two visits, the sort's comparisons at their reference bound, the duplicate pass and the
    # body's digest. Its allocations are objects only.
    e['C2a-1'] = (2 * n + F * lg(F) + max(F - 1, 0) + digest(body), 5)
    # CI-3's open (B_open, CI r5 item 4), with CI-A2-b's index and association and CI-A2-d's status read.
    edges = (CUST_EDGES + DESC_EDGES + CUST_EDGES + FOPEN_EDGES + 1 + FOPEN_EDGES + env(record) + DESC_EDGES + ST_EDGES
             + n * lg(n) + F * (lg(n) + 1) + DESC_EDGES * D + (n + 3 * (D + 1)) + ST_EDGES * n + S
             + sum(FOPEN_EDGES + env(x) for x in files))
    objects = (CUST_OBJECTS + 1 + DESC_OBJECTS + CUST_OBJECTS + 1 + 1 + DESC_OBJECTS + 2 + DESC_OBJECTS * D + S + 1)
    e['CI-3 open'] = (edges, objects)
    # C2a-3's transfers into memory (B_transfer per file, with CI-A2-c's lookup).
    e['CI-3 transfers'] = (sum((lg(n) + 1) + DESC_EDGES * (depth - 1) + FOPEN_EDGES + env(x) for x in files),
                           DESC_OBJECTS * (depth - 1) * F)
    # C2a-3k over a map holding exactly the Blobs: per Blob one presence comparison, one length comparison, its
    # digest and one digest comparison; then the body's digest and one comparison. No object.
    e['C2a-3k'] = (sum(3 + digest(x) for x in files) + digest(body) + 1, 0)
    return e


SHAPES = [
    # (label, file count, dir rows, symlinks, depth k, body bytes, record bytes R) - illustrations only.
    ('one file', 1, 0, 0, 1, 4096, 4096),
    ('1,000 files at depth 3', 1000, 100, 0, 3, 65536, 65536),
    ('10,000 files at depth 4', 10000, 1000, 100, 4, 1048576, 1048576),
    ('40,000 files at depth 6', 40000, 4000, 0, 6, 4194304, 4194304),
]


def total(shape, size):
    label, F, D, S, k, body, R = shape
    lengths = [size // F + (1 if i < size % F else 0) for i in range(F)]
    terms = component(lengths, D, S, k, body, R)
    return terms, sum(t[0] for t in terms.values()), sum(t[1] for t in terms.values())


rows = []
for shape in SHAPES:
    row = {'shape': shape[0], 'files': shape[1], 'dirs': shape[2], 'symlinks': shape[3], 'depth': shape[4],
           'bodyBytes': shape[5], 'recordBytes': shape[6], 'largestTotalBytesWithinEdgeCap': {}}
    for profile in ('global', 'discovery', 'snapshot'):
        cap = caps[profile]['edge']
        lo, hi = 0, 1 << 40
        if total(shape, 0)[1] > cap:
            row['largestTotalBytesWithinEdgeCap'][profile] = None
            continue
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if total(shape, mid)[1] <= cap:
                lo = mid
            else:
                hi = mid - 1
        row['largestTotalBytesWithinEdgeCap'][profile] = lo
    terms, edges, objects = total(shape, row['largestTotalBytesWithinEdgeCap']['snapshot'] or 0)
    row['atSnapshotBoundary'] = {'edges': edges, 'objects': objects, 'byTerm': {k: {'edges': v[0], 'objects': v[1]} for k, v in terms.items()},
                                 'hashingShareOfEdges': round((terms['C2a-3k'][0]) / edges, 4)}
    rows.append(row)
report['model'] = {'standing': 'illustrative shapes of README section 3; not a census, not caps',
                   'excluded': ['D4-1 and D4-2 (small per-manifest terms, owner-priced)', 'C2a-3\'s own map allocations (owed by C2a-3)',
                                'the identity admission internals (LD-C1A3-4 scoped exception)'],
                   'rows': rows}
print(json.dumps(report, indent=2))
