"""Port this origin's source40 scope probes to the source42 runtime WITHOUT editing any expectation: only the runtime root,
the probe copy (work/source40-pkg -> work/source42-pkg), the manifest index and the receipt file names change. The older
comparison sides (this origin's retained source39 copy, frozen source38/39 snapshots) are read-only history and unchanged.
Labels inside the ported probes that say "source40" are historical text; the current side is the verified source42 copy.
Writes probes/ported42_*.py and receipts/probe-port.json."""
import hashlib, json, re
from pathlib import Path

SRC = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v40/probes')
RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v42')
NAMES = ['probe_policy_v40.py', 'probe_native_v40.py', 'probe_runterm_adv_v40.py', 'ported_probe_query_carriers.py',
         'ported_probe_carrier_readonly.py', 'ported_probe_comparison_knowledge.py', 'ported_probe_repair2.py',
         'ported_probe_run_termination_s7.py', 'ported_probe_native_custody_fallback.py']
SUBS = [('claude-independent-design.v40', 'claude-independent-design.v42'),
        ('work/source40-pkg', 'work/source42-pkg'),
        ('manifest40-index.json', 'manifest42-index.json')]
rows = []
for name in NAMES:
    raw = (SRC / name).read_text()
    new = raw
    counts = {}
    for a, b in SUBS:
        counts[a] = new.count(a)
        new = new.replace(a, b)
    receipt_names = re.findall(r"receipts/probes/([A-Za-z0-9_.-]+\.json)", new)
    for rn in set(receipt_names):
        if rn.endswith('-v40.json'):
            new = new.replace('receipts/probes/' + rn, 'receipts/probes/' + rn[:-5] + '-on42.json')
    dest = RT / 'probes' / ('ported42_' + name.replace('ported_', ''))
    dest.write_text(new)
    rows.append({'source': str(SRC / name), 'sourceSha256': hashlib.sha256(raw.encode()).hexdigest(), 'dest': str(dest),
                 'destSha256': hashlib.sha256(new.encode()).hexdigest(), 'substitutionCounts': counts,
                 'receiptNames': sorted(set(re.findall(r"receipts/probes/([A-Za-z0-9_.-]+\.json)", new))),
                 'residualV40RuntimeMentions': [l for l in new.splitlines() if 'claude-independent-design.v40' in l or 'source40-pkg' in l]})
(RT / 'receipts/probe-port.json').write_text(json.dumps(rows, indent=1))
print(json.dumps(rows, indent=1))
