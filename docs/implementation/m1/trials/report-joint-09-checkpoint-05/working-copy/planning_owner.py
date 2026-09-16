"""Load the proposed planning owner only after checking its recorded bytes."""
from pathlib import Path
import hashlib,json
HERE=Path(__file__).resolve().parent

def read():
    row=json.loads((HERE/'planning-composition-result.json').read_bytes())['output']
    assert row['path']=='composed-owners/builtin-step-planning.proposed.json'
    raw=(HERE/row['path']).read_bytes()
    assert len(raw)==row['bytes'] and hashlib.sha256(raw).hexdigest()==row['sha256']
    return json.loads(raw)
