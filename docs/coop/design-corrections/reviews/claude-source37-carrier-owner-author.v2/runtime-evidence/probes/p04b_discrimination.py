"""p04 over the p02b tree. Executes p04's exact source with three asserted renames only: new hybrid directory names
(v2final-hybrid-*), new report names (p04b-*) and a new summary receipt, so every p04 artefact stays preserved.
Expectations are p04's, unchanged.
"""
from pathlib import Path

src = Path('/tmp/opensip-design-corrections/claude-source37-carrier-owner-author.v2/probes/p04_discrimination.py').read_text()
for old, new in (("root = W / name\n", "root = W / ('v2final-' + name)\n"),
                 ("('p04-integrated-carrier.' + name + '.json')", "('p04b-integrated-carrier.' + name + '.json')"),
                 ("'p04-discrimination.json'", "'p04b-discrimination.json'")):
    if src.count(old) != 1:
        raise SystemExit('rename anchor: ' + old)
    src = src.replace(old, new)
exec(compile(src, 'p04_discrimination.py (renamed outputs)', 'exec'), {'__name__': '__main__'})
