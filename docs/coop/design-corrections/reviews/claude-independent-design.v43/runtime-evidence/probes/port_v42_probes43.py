"""Port this origin's source42 scope-preservation probes to the source43 runtime WITHOUT editing any expectation: only the runtime
root (claude-independent-design.v42 -> .v43), the probe copy (work/source42-pkg -> work/source43-pkg), the manifest index and
receipt file names change. Older comparison sides (this origin's retained source39 copy) are read-only history and unchanged.
Labels inside the ported probes that say "source40"/"source42" are historical text; the current side is the verified source43 copy.
Writes probes/ported43_*.py and receipts/probe-port43.json."""
import hashlib, json, re
from pathlib import Path

SRC = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v42/probes')
RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v43')
NAMES = ['ported42_probe_policy_v40.py', 'ported42_probe_native_v40.py', 'ported42_probe_runterm_adv_v40.py', 'ported42_probe_query_carriers.py',
         'ported42_probe_carrier_readonly.py', 'ported42_probe_comparison_knowledge.py', 'ported42_probe_repair2.py',
         'ported42_probe_run_termination_s7.py', 'ported42_probe_native_custody_fallback.py', 'probe_capture_joins_42.py']
SUBS = [('claude-independent-design.v42', 'claude-independent-design.v43'),
        ('work/source42-pkg', 'work/source43-pkg'),
        ('manifest42-index.json', 'manifest43-index.json'),
        ('-v40-on42.json', '-v40-on43.json'),
        ('receipts/probes/capture-joins-42.json', 'receipts/probes/capture-joins-on43.json')]
rows = []
for name in NAMES:
    raw = (SRC / name).read_text()
    new = raw
    counts = {}
    for a, b in SUBS:
        counts[a] = new.count(a)
        new = new.replace(a, b)
    dest = RT / 'probes' / ('ported43_' + name.replace('ported42_', '').replace('probe_capture_joins_42', 'probe_capture_joins'))
    dest.write_text(new)
    rows.append({'source': str(SRC / name), 'sourceSha256': hashlib.sha256(raw.encode()).hexdigest(), 'dest': str(dest),
                 'destSha256': hashlib.sha256(new.encode()).hexdigest(), 'substitutionCounts': counts,
                 'receiptNames': sorted(set(re.findall(r"receipts/probes/([A-Za-z0-9_.-]+\.json)", new))),
                 'residualV42RuntimeMentions': [l for l in new.splitlines() if 'claude-independent-design.v42' in l or 'source42-pkg' in l or 'manifest42-index' in l]})
(RT / 'receipts/probe-port43.json').write_text(json.dumps(rows, indent=1))
print(json.dumps(rows, indent=1))
