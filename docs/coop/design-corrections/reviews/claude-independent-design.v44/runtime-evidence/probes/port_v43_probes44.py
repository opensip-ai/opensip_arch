"""Port this origin's source43 scope-preservation probes to the source44 runtime WITHOUT editing any expectation: only the runtime
root (claude-independent-design.v43 -> .v44), the probe copy (work/source43-pkg -> work/source44-pkg), the manifest index and
receipt file names change. Older comparison sides (this origin's retained source39 copy) are read-only history and unchanged.
Labels inside the ported probes that say "source40"/"source42"/"source43" are historical text; the current side is the verified
source44 copy. Writes probes/ported44_*.py and receipts/probe-port44.json."""
import hashlib, json, re
from pathlib import Path

SRC = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v43/probes')
RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v44')
NAMES = ['ported43_probe_policy_v40.py', 'ported43_probe_native_v40.py', 'ported43_probe_runterm_adv_v40.py', 'ported43_probe_query_carriers.py',
         'ported43_probe_carrier_readonly.py', 'ported43_probe_comparison_knowledge.py', 'ported43_probe_repair2.py',
         'ported43_probe_run_termination_s7.py', 'ported43_probe_native_custody_fallback.py', 'ported43_probe_capture_joins.py']
SUBS = [('claude-independent-design.v43', 'claude-independent-design.v44'),
        ('work/source43-pkg', 'work/source44-pkg'),
        ('manifest43-index.json', 'manifest44-index.json'),
        ('-v40-on43.json', '-v40-on44.json'),
        ('receipts/probes/capture-joins-on43.json', 'receipts/probes/capture-joins-on44.json')]
rows = []
for name in NAMES:
    raw = (SRC / name).read_text()
    new = raw
    counts = {}
    for a, b in SUBS:
        counts[a] = new.count(a)
        new = new.replace(a, b)
    dest = RT / 'probes' / name.replace('ported43_', 'ported44_')
    dest.write_text(new)
    rows.append({'source': str(SRC / name), 'sourceSha256': hashlib.sha256(raw.encode()).hexdigest(), 'dest': str(dest),
                 'destSha256': hashlib.sha256(new.encode()).hexdigest(), 'substitutionCounts': counts,
                 'receiptNames': sorted(set(re.findall(r"receipts/probes/([A-Za-z0-9_.-]+\.json)", new))),
                 'residualV43RuntimeMentions': [l for l in new.splitlines() if 'claude-independent-design.v43' in l or 'source43-pkg' in l or 'manifest43-index' in l]})
(RT / 'receipts/probe-port44.json').write_text(json.dumps(rows, indent=1))
print(json.dumps(rows, indent=1))
