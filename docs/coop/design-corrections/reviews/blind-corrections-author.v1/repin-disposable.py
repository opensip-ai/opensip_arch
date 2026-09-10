"""Disposable: rewrite security/native source pins inside the /tmp verification mirror only.
Never run against the repository working tree; Codex refreshes the real pins after integration."""
import hashlib, json, sys
from pathlib import Path
ROOT = Path(sys.argv[1]).resolve()
assert '/tmp/' in str(ROOT), 'refusing to repin outside the disposable mirror'
for rel in ('docs/coop/design-corrections/security/source-pins.v1.json',):
    p = ROOT / rel
    doc = json.loads(p.read_text())
    for item in doc['pins']:
        item['sha256'] = hashlib.sha256((ROOT / item['path']).read_bytes()).hexdigest()
    p.write_text(json.dumps(doc, indent=1) + '\n')
    print('repinned', rel, len(doc['pins']))
