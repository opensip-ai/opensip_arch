"""p05 with one corrected wording-scan classification. Executes p05's exact source with asserted edits only.

p05 exited 1 on one hit: check-carrier-v3.py line "'encodingAssumption' not in _S37_G", which is the checker's own negative
control asserting the v2 key is ABSENT, not a current restriction claim. That receipt is retained. Here a hit is skipped only
when it is in check-carrier-v3.py and its line contains "'encodingAssumption' not in"; every other pattern, file and check is
unchanged. Output is p05b-routes-drift-wording.json.
"""
from pathlib import Path

src = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v3/probes/p05_routes_drift_wording.py').read_text()
old_loop = ("    for m in stale.finditer(text):\n"
            "        line = text.count('\\n', 0, m.start()) + 1\n"
            "        hits.append('%s:%d %s' % (rel, line, m.group(0)))\n")
new_loop = ("    lines_ = text.splitlines()\n"
            "    for m in stale.finditer(text):\n"
            "        line = text.count('\\n', 0, m.start()) + 1\n"
            "        if rel.endswith('check-carrier-v3.py') and \"'encodingAssumption' not in\" in lines_[line - 1]:\n"
            "            continue\n"
            "        hits.append('%s:%d %s' % (rel, line, m.group(0)))\n")
for old, new in ((old_loop, new_loop), ("'p05-routes-drift-wording.json'", "'p05b-routes-drift-wording.json'")):
    if src.count(old) != 1:
        raise SystemExit('edit anchor: ' + old[:60])
    src = src.replace(old, new)
exec(compile(src, 'p05_routes_drift_wording.py (negative-control classification)', 'exec'), {'__name__': '__main__'})
