"""Port this origin's source44 scope-preservation probes to the source45 runtime WITHOUT editing any expectation: only the runtime
root (claude-independent-design.v44 -> .v45), the probe copy (work/source44-pkg -> work/source45-pkg), the manifest index and
receipt file names change. Older comparison sides (this origin's retained source39 copy) are read-only history and unchanged.
Labels inside the ported probes that say "source40"/"source42"/"source43"/"source44" are historical text; the current side is the
verified source45 copy. The source44 wire and startup discriminators are NOT ported as fresh probes here; they are re-executed
separately and labelled as re-execution on source45. Writes probes/ported45_*.py and receipts/probe-port45.json."""
import hashlib, json, re
from pathlib import Path

SRC = Path('/tmp/opensip-design-corrections/claude-independent-design.v44/probes')
RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v45')
NAMES = ['ported44_probe_policy_v40.py', 'ported44_probe_native_v40.py', 'ported44_probe_runterm_adv_v40.py', 'ported44_probe_query_carriers.py',
         'ported44_probe_carrier_readonly.py', 'ported44_probe_comparison_knowledge.py', 'ported44_probe_repair2.py',
         'ported44_probe_run_termination_s7.py', 'ported44_probe_native_custody_fallback.py', 'ported44_probe_capture_joins.py']
SUBS = [('claude-independent-design.v44', 'claude-independent-design.v45'),
        ('work/source44-pkg', 'work/source45-pkg'),
        ('manifest44-index.json', 'manifest45-index.json'),
        ('-v40-on44.json', '-v40-on45.json'),
        ('receipts/probes/capture-joins-on44.json', 'receipts/probes/capture-joins-on45.json')]
rows = []
for name in NAMES:
    raw = (SRC / name).read_text()
    new = raw
    counts = {}
    for a, b in SUBS:
        counts[a] = new.count(a)
        new = new.replace(a, b)
    dest = RT / 'probes' / name.replace('ported44_', 'ported45_')
    dest.write_text(new)
    rows.append({'source': str(SRC / name), 'sourceSha256': hashlib.sha256(raw.encode()).hexdigest(), 'dest': str(dest),
                 'destSha256': hashlib.sha256(new.encode()).hexdigest(), 'substitutionCounts': counts,
                 'receiptNames': sorted(set(re.findall(r"receipts/probes/([A-Za-z0-9_.-]+\.json)", new))),
                 'residualV44RuntimeMentions': [l for l in new.splitlines() if 'claude-independent-design.v44' in l or 'source44-pkg' in l or 'manifest44-index' in l]})
(RT / 'receipts/probe-port45.json').write_text(json.dumps(rows, indent=1))
print(json.dumps(rows, indent=1))
