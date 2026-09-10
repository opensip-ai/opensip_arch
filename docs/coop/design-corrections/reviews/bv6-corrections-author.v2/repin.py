"""Refresh the four unit source-pins files IN A DISPOSABLE COPY ONLY.
Usage: python -I -B repin.py <disposable-root>   (never run against `work`)"""
import hashlib, json, pathlib, sys
ROOT = pathlib.Path(sys.argv[1]).resolve()
assert 'disposable' in str(ROOT), 'refuse: repin only ever runs in a disposable copy'
DC = ROOT / 'docs/coop/design-corrections'
changed = []
for pin, key in [('foundation/source-pins.v1.json', 'files'), ('workflows/source-pins.v1.json', 'files'),
                 ('native/source-pins.v2.json', 'pins'), ('security/source-pins.v1.json', 'pins')]:
    p = DC / pin
    d = json.loads(p.read_text(encoding='utf-8'))
    rows = d[key]
    items = rows.items() if isinstance(rows, dict) else [(r['path'], r) for r in rows]
    for path, row in items:
        cur = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
        if isinstance(row, dict) and 'sha256' in row and row['sha256'] != cur:
            row['sha256'] = cur; changed.append((pin, path))
        elif isinstance(row, str) and row != cur:
            rows[path] = cur; changed.append((pin, path))
    p.write_text(json.dumps(d, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print(json.dumps({'repinnedIn': str(ROOT), 'rows': len(changed)}, indent=1))
