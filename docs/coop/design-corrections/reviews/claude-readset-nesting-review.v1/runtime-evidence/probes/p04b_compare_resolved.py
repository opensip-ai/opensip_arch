"""p04b: p04_compare with one corrected harness comparison. Executes p04's exact source with asserted edits only.

p04_compare exited 1 (receipt retained) on `models-loaded-from-the-intended-trees` alone: the loaded module paths are
reported resolved (/private/tmp/...) while the check compared them to the unresolved /tmp/... prefix. The reported
paths were in fact the intended trees. This rerun compares resolved paths; every other check is unchanged. Output is
receipts/p04b-compare.json.
"""
from pathlib import Path

src = Path('/tmp/opensip-design-corrections/claude-readset-nesting-review.v1/probes/p04_compare.py').read_text()
edits = [
    ("after['loadedModelFile'].startswith(str(BASE / 'work/source'))", "after['loadedModelFile'].startswith(str((BASE / 'work/source').resolve()))"),
    ("before['loadedModelFile'].startswith(str(BASE / 'work/hybrid-p03'))", "before['loadedModelFile'].startswith(str((BASE / 'work/hybrid-p03').resolve()))"),
    ("(R / 'p04-compare.json')", "(R / 'p04b-compare.json')"),
]
for old, new in edits:
    if src.count(old) != 1:
        raise SystemExit('edit anchor count %d: %r' % (src.count(old), old))
    src = src.replace(old, new)
exec(compile(src, 'p04_compare.py (resolved-path comparison)', 'exec'), {'__name__': '__main__'})
