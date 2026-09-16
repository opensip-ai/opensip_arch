"""Read composed metadata only after checking its recorded bytes."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent

def read(name):
    allowed={'inventory':'composed-owners/command-inventory.proposed.json','details':'composed-owners/public-detail-registry.proposed.json'}
    path=allowed[name]
    rows=json.loads((HERE/'metadata-composition-result.json').read_bytes())['outputs']
    row=next(r for r in rows if r['path']==path)
    raw=(HERE/path).read_bytes()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
    return json.loads(raw)
