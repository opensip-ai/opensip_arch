"""C1c-0's r9 fixed-cap and 2x evidence for the WalkEvidence retention (C1c plan r4, LD-C1C-13 and the R3-RF-1 row).

The retention adds no charge for the first-party Cargo roots, which move (the vector cases with Cargo roots are
unchanged, a lane check). It adds one owned record per admitted member root: objects 1 and bytes len + RECORD each. Its
worst case is the member cap (workspace_declarations.rs MAX_MEMBERS) of roots at the longest logical path
(descriptors.rs: 4,096 scalars, at most 4 UTF-8 bytes each, RFC 3629). This tool reads those bounds, RECORD and the
snapshot profile's caps by anchor from the product, and r9's adopted cumulative subtotal from the accepted law record
(RECORD-r9.md, the (a)+(b-prime) row), adds the worst-case retention, and checks r9's own 2x rule against the caps.
No network, process or environment input. Usage: retention_cap_evidence.py <product> <architecture> <out.json>."""
from pathlib import Path
import json, re, sys

product, arch, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])


def one(path, pattern, root=None):
    hits = re.findall(pattern, ((root or product) / path).read_text())
    if len(hits) != 1:
        raise SystemExit('%s matched %d times in %s' % (pattern, len(hits), path))
    return hits[0]


members = int(one('crates/security/src/custody/workspace_declarations.rs', r'\npub\(crate\) const MAX_MEMBERS: usize = (\d+);'))
scalars = int(one('crates/identity/src/descriptors.rs', r'if value\.chars\(\)\.take\(\d+\)\.count\(\) > (\d+) \{'))
record = int(one('crates/security/src/snapshot_walk.rs', r'\nconst RECORD: usize = (\d+);'))
caps = tuple(1 << int(one('crates/platform/src/work_ledger.rs', r'\nconst SNAPSHOT_%s_LIMIT: usize = 1 << (\d+);' % k)) for k in ('OBJECT', 'EDGE', 'BYTE'))
row = one('docs/implementation/m3/snapshot-plan-c/c1a-r9/RECORD-r9.md',
          r'\| \*\*\(a\)\+\(b′\), adopted\*\* \| \*\*([\d,]+) / ([\d,]+) / ([\d,]+)\*\* \|', root=arch)
subtotal = tuple(int(x.replace(',', '')) for x in row)
retention = (members, 0, members * (scalars * 4 + record))
total = tuple(s + r for s, r in zip(subtotal, retention))
passes = [2 * t <= c for t, c in zip(total, caps)]
doc = dict(standing='C1c-0 retention cap evidence: r9 adopted subtotal plus the worst-case WalkEvidence member copies, by r9 2x rule',
           memberCap=members, logicalPathScalars=scalars, recordOverhead=record, caps=dict(zip(('objects', 'edges', 'bytes'), caps)),
           r9Subtotal=dict(zip(('objects', 'edges', 'bytes'), subtotal)), retentionWorstCase=dict(zip(('objects', 'edges', 'bytes'), retention)),
           total=dict(zip(('objects', 'edges', 'bytes'), total)), passes2x=dict(zip(('objects', 'edges', 'bytes'), passes)), allPass=all(passes))
out.write_text(json.dumps(doc, indent=2) + '\n')
print(json.dumps(doc))
raise SystemExit(0 if all(passes) else 1)
