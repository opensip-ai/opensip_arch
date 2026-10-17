"""C1b-0 r2's stale-receipt record (Codex C1B0-R1-RF-1; C1b plan r3 LD-C1B-7 and its R2-RF-1 rule), separate from the
census output checks: regenerate_c1b0_census.py --verify, which writes nothing and opens no held-out material. From
the accepted batch-entry baseline on main (C1a4's refresh: both receipts current, every held-out row rendered
'blind-census'), it records both receipts' public binding deltas (the discovery receipt's exactly the generator-closure
digest; the companion's exactly that digest nested in its discovery binding), both receipts byte-equal main's
(historical baseline evidence for the stale interval), and the candidate's two records rendering every held-out row
stale, with every other record field unchanged but those derived from the held-out results. Usage: <out json>."""
import subprocess, sys
from pathlib import Path
here = Path(__file__).resolve().parent
r = subprocess.run([sys.executable, '-I', '-B', str(here / 'regenerate_c1b0_census.py'), sys.argv[1], '--verify'])
sys.exit(r.returncode)
