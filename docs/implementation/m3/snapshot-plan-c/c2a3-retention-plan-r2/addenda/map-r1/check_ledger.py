"""Pure checker for the C2a-3 map/local/slot price addendum r1. No Rust is executed.

Recomputes every call-tree total, checks each selected allowance is the next
power of two at or above its counted visits, recounts the proposed
fund_representation's helpers against funding-r3's fixed and scan rows, checks the
proposed source's literals, and reports the M consequence for SD-9 r2's four
illustrative shapes against the current snapshot interim and the accepted C2b
successor caps. It claims no fit, census or native result.
"""
from pathlib import Path
import hashlib, json, re

B = Path(__file__).parent
T = json.loads((B / 'CALL-TREE.json').read_text())
D = T['definitions']
L = json.loads((B / 'LEDGER.json').read_text())
assert hashlib.sha256((B / 'FUNDING-R3-CALL-TREE.json').read_bytes()).hexdigest() == T['importedFundingR3CallTreeSha256']
F3 = json.loads((B / 'FUNDING-R3-CALL-TREE.json').read_text())['definitions']
for name in T['importedDefinitions']:
    assert D[name] == F3[name], name


def cost(node, stack=()):
    if node['kind'] == 'primitive':
        return node['visits']
    if node['kind'] == 'ref':
        assert node['name'] not in stack
        return cost(D[node['name']], stack + (node['name'],))
    return sum((2 * node[k] + 63) // 64 for k in ('argumentBytes', 'resultBytes')) + sum(cost(x, stack) for x in node['body'])


def p2(x):
    return 1 << (x - 1).bit_length()


def walk(node, out, stack=()):
    if node['kind'] == 'ref':
        walk(D[node['name']], out, stack + (node['name'],))
    elif node['kind'] == 'call':
        for x in node['body']:
            walk(x, out, stack)
    else:
        out.append(node)


# Every move primitive is ceil(2w/64); every inherited count names its audited subject.
for name, node in D.items():
    prims = []
    walk(node, prims)
    for x in prims:
        if 'moveBytes' in x:
            assert x['visits'] == (2 * x['moveBytes'] + 63) // 64, x
        if 'inheritedFrom' in x:
            assert 'SOURCE-AUDIT' in x['inheritedFrom'], x

rows = {}
for key, row in L.items():
    names = [row['node']] if 'node' in row else row['nodes']
    visits = sum(cost(D[n]) for n in names)
    assert visits == row['visits'], key
    if 'accepted' in row:
        assert row['selected'] >= visits, key
    else:
        assert row['selected'] == p2(visits) >= visits, key
    rows[key] = (visits, row['selected'])
assert rows['perBlobLocal'][1] == 1024 and rows['componentFixedLocal'][1] == 1024
assert rows['slotPerComponent'][1] == 256 and rows['prepareFixed'][1] == 1024
assert rows['admitPerComponent'][1] == 1024 and rows['admitFixed'][1] == 2048
# Funding keeps its accepted literals; its explicit roots must fit them (RF-3).
assert rows['fundFixed'][0] <= 1024 and rows['fundScanPerBlob'][0] <= 256

# ---- the proposed source: literals, debit order and funding helper recount ----
src = (B / 'proposed/component_admission.rs').read_text()
for literal in ['const FIXED: usize = 1024;', 'const SCAN: usize = 256;', 'const LOCAL: usize = 1024;',
                'const COMPONENT: usize = 1024;', 'const PREPARE_FIXED: usize = 1024;', 'const PREPARE_SLOT: usize = 256;',
                'const ADMIT_FIXED: usize = 2048;', 'const ADMIT_COMPONENT: usize = 1024;']:
    assert src.count(literal) == 1, literal
for gone in ['BTreeMap', 'HEX', 'sha256: &', '10_368', 'height', 'comparisons', 'resize_with', 'let mut slots = Vec::new();']:
    assert gone not in src, gone
inner = src.split('fn admit_component_inner<', 1)[1]
assert inner.index('edges: COMPONENT') < inner.index('open_retained_tree(') < inner.index('fund_representation(')
fund = src.split('fn fund_representation(', 1)[1].split('\n}\n', 1)[0]
loop = fund.split('    for blob in candidate.blobs() {', 1)[1].split('\n    }', 1)[0]
helpers = len(re.findall(r'\b(?:add|mul)\(', fund))
scan_helpers = len(re.findall(r'\b(?:add|mul)\(', loop))
subs = fund.count('.checked_sub(')
assert scan_helpers == 5 and helpers - scan_helpers == 18 and subs == 2

# The funding roots must use exactly the proposed source's helper calls.
def count_refs(node_name, target):
    return sum(1 for x in D[node_name]['body'] if x.get('kind') == 'ref' and x['name'] == target)
assert count_refs('fund_fixed', 'helper_try') == helpers - scan_helpers
assert count_refs('fund_fixed', 'sub_try') == subs
assert count_refs('fund_scan_blob', 'helper_try') == scan_helpers
fixed_new, scan_new = rows['fundFixed'][0], rows['fundScanPerBlob'][0]


# ---- prices ----
def env(b):
    return 2 * ((b + 65535) // 65536) + 2


def m_new(sizes):
    f = len(sizes)
    e = sum(env(b) for b in sizes)
    bsum = sum(sizes)
    edges = 1024 + 1024 + f * (256 + 1024) + 128 * e          # COMPONENT + FIXED + F(SCAN+LOCAL) + 128E
    objects = (1 if f else 0) + f
    byts = 64 * edges + ((40 * f + 128) if f else 0) + bsum + 128 * f + 2 * bsum
    return objects, edges, byts


def m_r3(sizes):
    """The accepted (undercharging) funding-r3 price, for comparison only."""
    f = len(sizes)
    e = sum(env(b) for b in sizes)
    bsum = sum(sizes)
    pmax = 64
    h = 1 + f.bit_length()
    q = 11 * f * h
    edges = 1024 + f * (481 + 23 * h) + 128 * e
    objects = (1 if f else 0) + 3 * f
    byts = ((24 * f + 128) if f else 0) + bsum + 128 * f + 2 * f * 640 + 2 * bsum + 48 * f + 2 * pmax * q + 64 * (edges - q) + 10368 * f
    return objects, edges, byts


def map_audited_edges(f):
    """Order of the audited map construction plus destruction, lower terms dropped: F(870 + 571H)."""
    h = 1 + f.bit_length()
    return f * (870 + 571 * h)


def frame(n):
    if n == 0:
        return 0, 0, 0
    edges = 1024 + 256 * n + 2048 + 1024 * n
    return 2, edges, 64 * edges + (128 * n + 128) + (264 * n + 128)


CAPS = {'snapshotInterim': (1 << 21, 1 << 24, 1 << 33), 'c2bSuccessor': (1 << 25, 1 << 34, 1 << 41)}
SHAPES = [('one file', 1, 1069536384), ('1,000 files', 1000, 1064704785),
          ('10,000 files', 10000, 1010568235), ('40,000 files', 40000, 796181735)]
shapes = []
for label, files, total in SHAPES:
    base, extra = divmod(total, files)
    sizes = [base + (1 if i < extra else 0) for i in range(files)]
    new, old = m_new(sizes), m_r3(sizes)
    fr = frame(1)
    m_plus_frame = tuple(a + b for a, b in zip(new, fr))
    shapes.append({
        'shape': label, 'files': files, 'totalBytes': total,
        'newM': dict(zip(['objects', 'edges', 'bytes'], new)),
        'frameOneComponent': dict(zip(['objects', 'edges', 'bytes'], fr)),
        'acceptedR3M': dict(zip(['objects', 'edges', 'bytes'], old)),
        'auditedMapEdgesOrderEstimate': map_audited_edges(files),
        'newMEdgesPerFile': round(new[1] / files, 1),
        'fractionOfCap': {k: [round(a / c, 4) for a, c in zip(m_plus_frame, caps)] for k, caps in CAPS.items()},
        'mAndFrameAloneWithinCap': {k: all(a <= c for a, c in zip(m_plus_frame, caps)) for k, caps in CAPS.items()},
    })
assert m_new([])[1] == 2048 and m_new([]) == (0, 2048, 64 * 2048)

report = {
    'passed': True,
    'rows': {k: {'visits': v, 'selected': s} for k, (v, s) in rows.items()},
    'fundingFixed': {'acceptedR3Count': 775, 'explicitRoot': fixed_new, 'selected': 1024},
    'fundingScanPerBlob': {'acceptedR3Count': 163, 'explicitRoot': scan_new, 'selected': 256},
    'proposedHelperCalls': {'fixed': helpers - scan_helpers, 'perBlob': scan_helpers, 'checkedSub': subs},
    'perComponentEdges': '2048 + 1280F + 128E',
    'frameEdges': 'n>0: 3072 + 1280n (n=0 charges nothing)',
    'sd9Shapes': shapes,
    'definitionVisits': {k: cost(v) for k, v in D.items()},
    'actualRustExecuted': False, 'nativeExecution': False, 'primitiveContractsEstablished': False,
    'completeMBoundEstablished': False, 'fitClaimed': False, 'censusRun': False,
    'unitAcceptance': False, 'productQualification': False,
}
(B / 'ledger-report.json').write_text(json.dumps(report, indent=1) + '\n')
print(json.dumps({k: v for k, v in report.items() if k not in ('definitionVisits', 'sd9Shapes')}, indent=1))
for s in shapes:
    print(s['shape'], s['newMEdgesPerFile'], s['newM']['edges'], s['acceptedR3M']['edges'], s['auditedMapEdgesOrderEstimate'],
          s['fractionOfCap'], s['mAndFrameAloneWithinCap'])
