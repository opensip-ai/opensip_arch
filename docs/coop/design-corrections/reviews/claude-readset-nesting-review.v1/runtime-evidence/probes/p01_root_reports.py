"""p01: inspect root's before/after probe reports by content (not by whole-file hash claims).

For each case: path, outcome, refusal reason; for RETURNED cases the returned tuple's Run: runId, the snapshot's
sourceInventory row for the probed path, the Plan-selected TypeScript context's nodeModulesLayoutDigest and the
retained layout entries (installPath/realPath) when present, and the replay verdict. Reports whether each report
parsed completely. Output: receipts/p01-root-reports.json.
"""
import json, sys
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-readset-nesting-review.v1')
ROOT = Path('/tmp/opensip-design-corrections/root-source39-readset-nesting.v1')
out = {'standing': 'content inspection of root probe reports'}


def find_layouts(value, acc):
    if isinstance(value, dict):
        if value.get('schemaVersion') == 1 and isinstance(value.get('entries'), list) and all(
                isinstance(e, dict) and 'installPath' in e for e in value['entries']) and value['entries']:
            acc.append([(e['installPath'], e['realPath']) for e in value['entries']])
        for v in value.values():
            find_layouts(v, acc)
    elif isinstance(value, list):
        for v in value:
            find_layouts(v, acc)


for tag in ('before', 'after'):
    p = ROOT / tag / 'report.json'
    try:
        rep = json.loads(p.read_text())
    except Exception as exc:
        out[tag] = {'parsed': False, 'error': repr(exc)[:200]}
        continue
    rows = []
    for c in rep['cases']:
        row = {'path': c['path'], 'outcome': c['outcome'], 'reason': c.get('reason'), 'exceptionType': c.get('exceptionType')}
        if c['outcome'] == 'RETURNED':
            run, objects, blobs, actual = c['result']
            row['runId'] = actual.get('runId') if isinstance(actual, dict) else None
            row['verdict'] = actual.get('verdict') if isinstance(actual, dict) else None
            snap = objects[run['snapshotId']][1]
            inv = [r for r in snap['sourceInventory'] if r['path'] == c['path']]
            row['inventoryRowForPath'] = inv
            row['inventoryPathsInPrunedTrees'] = [r['path'] for r in snap['sourceInventory'] if r['path'].startswith('node_modules/') or '/.' in '/' + r['path']]
            ctx = [v[1] for v in objects.values() if isinstance(v, list) and v and v[0] in ('closure',) and False]
            layouts = []
            find_layouts(blobs if isinstance(blobs, dict) else {}, layouts)
            find_layouts(objects, layouts)
            row['layoutEntriesFound'] = layouts[:3]
            row['blobCount'] = len(blobs) if isinstance(blobs, dict) else None
        rows.append(row)
    out[tag] = {'parsed': True, 'source': rep['source'], 'modelSha256': rep['modelSha256'], 'cases': rows}
(BASE / 'receipts').mkdir(exist_ok=True)
(BASE / 'receipts' / 'p01-root-reports.json').write_text(json.dumps(out, indent=1, default=str) + '\n')
print(json.dumps(out, indent=1, default=str)[:12000])
