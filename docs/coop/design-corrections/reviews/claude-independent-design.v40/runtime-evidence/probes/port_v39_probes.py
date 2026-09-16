"""Port this origin's own source39 probes whose owner bytes are unchanged 39->40 into the source40 runtime.

Reads the retained source39 probe scripts (read-only history) and writes adapted copies under probes/ with the runtime,
copy and module-name prefixes rebound to source40. No expectation is edited; the port is recorded in
receipts/probe-port.json with source and destination hashes so the reuse is explicit."""
import hashlib, json
from pathlib import Path

OLD = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v39/probes')
NEW = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v40/probes')
PORT = ['probe_query_carriers.py', 'probe_carrier_readonly.py', 'probe_comparison_knowledge.py', 'probe_repair2.py',
        'probe_run_termination_s7.py', 'probe_native_custody_fallback.py']
rows = []
for name in PORT:
    src = (OLD / name).read_bytes()
    text = src.decode('utf-8')
    out = (text.replace('claude-independent-design.v39', 'claude-independent-design.v40')
               .replace('work/source39-pkg', 'work/source40-pkg')
               .replace("'p39_", "'p40_").replace('"p39_', '"p40_'))
    dest = NEW / ('ported_' + name)
    if dest.exists():
        raise SystemExit('refusing to overwrite ' + str(dest))
    dest.write_text(out, encoding='utf-8')
    rows.append({'source': str(OLD / name), 'sourceSha256': hashlib.sha256(src).hexdigest(), 'dest': str(dest),
                 'destSha256': hashlib.sha256(out.encode()).hexdigest(),
                 'residualV39Mentions': [l for l in out.splitlines() if 'v39' in l or 'source39' in l][:10]})
Path('/private/tmp/opensip-design-corrections/claude-independent-design.v40/receipts/probe-port.json').write_text(json.dumps(rows, indent=1))
print(json.dumps(rows, indent=1))
