"""Mechanical port of this origin's source44 startup discriminator (probe_startup44.py) for RE-EXECUTION on the verified source45
probe copy, expectations unedited: runtime root, probe copy and receipt name only. The source45 native model changed only the
pre-analysis conversion closedWorld construction, which this probe exercises, so the re-execution is corroboration of unchanged
startup behaviour; it is not labelled fresh source45 assessment. Writes probes/reexec45_probe_startup.py and
receipts/startup-reexec-port45.json."""
import hashlib, json
from pathlib import Path

SRC = Path('/tmp/opensip-design-corrections/claude-independent-design.v44/probes/probe_startup44.py')
RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v45')
SUBS = [('claude-independent-design.v44', 'claude-independent-design.v45'), ('work/source44-pkg', 'work/source45-pkg'),
        ("receipts/probes/startup44.json", "receipts/probes/startup44-reexec-on45.json")]
raw = SRC.read_text()
new = raw
counts = {}
for a, b in SUBS:
    counts[a] = new.count(a)
    new = new.replace(a, b)
dest = RT / 'probes/reexec45_probe_startup.py'
dest.write_text(new)
rec = {'source': str(SRC), 'sourceSha256': hashlib.sha256(raw.encode()).hexdigest(), 'dest': str(dest), 'destSha256': hashlib.sha256(new.encode()).hexdigest(),
       'substitutionCounts': counts, 'residualV44Mentions': [l for l in new.splitlines() if 'design.v44' in l or 'source44-pkg' in l]}
(RT / 'receipts/startup-reexec-port45.json').write_text(json.dumps(rec, indent=1))
print(json.dumps(rec, indent=1))
