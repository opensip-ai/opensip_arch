"""B-S10 addendum: re-pin crates/identity/src/schema_registry.rs in tools/identity/dependency-policy.json (the policy pins every identity source)."""
from pathlib import Path
import json, hashlib
W = Path('/Users/sb/code/opensip-ai/opensip-b-s10'); p = W / 'tools/identity/dependency-policy.json'; raw = p.read_text(); d = json.loads(raw)
b = (W / 'crates/identity/src/schema_registry.rs').read_bytes(); hits = []
def walk(o):
    if isinstance(o, dict):
        if o.get('path') == 'src/schema_registry.rs': hits.append(o)
        for v in o.values(): walk(v)
    elif isinstance(o, list):
        for v in o: walk(v)
walk(d); assert len(hits) == 1; old = dict(hits[0]); hits[0].update(bytes=len(b), sha256=hashlib.sha256(b).hexdigest())
out = json.dumps(d, indent=2) + '\n'; assert raw == json.dumps(json.loads(raw), indent=2) + '\n', 'policy formatting differs from indent-2'
p.write_text(out); print(old, '->', hits[0])
