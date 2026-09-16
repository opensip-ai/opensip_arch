"""p05 over the p02b tree. Executes p05's exact source with two asserted renames only: it reads the p02b receipt
instead of p02's and writes p05b-routes-drift-wording.json, so the p05 receipt stays preserved.
"""
from pathlib import Path

src = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v2/probes/p05_routes_drift_wording.py').read_text()
for old, new in (("'receipts/p02-apply-v2.json'", "'receipts/p02b-apply-v2-final.json'"),
                 ("'p05-routes-drift-wording.json'", "'p05b-routes-drift-wording.json'")):
    if src.count(old) != 1:
        raise SystemExit('rename anchor: ' + old)
    src = src.replace(old, new)
exec(compile(src, 'p05_routes_drift_wording.py (renamed inputs/outputs)', 'exec'), {'__name__': '__main__'})
