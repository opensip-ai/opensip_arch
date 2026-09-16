"""Prepare the v1 regression probes inside THIS runtime (reads v1/root files; writes only under this runtime's probes/).

1. Copy the completed v1 known-hit/universe comparison probe byte for byte (it is parameterised by --source/--out).
2. Make a new path-only adaptation of the retained original independent probe: only RT (output root) and SRC (source) change,
   and the standing text is relabelled; RT is this runtime's work/repro-original, never a root or old-author directory.
Writes probes/regression-probes.json with source/copy hashes and the adaptation diff. Usage: make_regression_probes.py
"""
import difflib
import hashlib
import json
from pathlib import Path

R = Path(__file__).resolve().parent.parent
V1 = Path("/private/tmp/opensip-design-corrections/claude-policy-test-known-hit-author.v1")
ORIGINAL = Path("/tmp/opensip-design-corrections/root-source39-policy-test-counterexample.v1/claude-original-probe.py")
ORIGINAL_SHA = "23d4f7dda532bff496add04af7e162207a516f5f03591a75f97962dcdb31ab58"
sha = lambda b: hashlib.sha256(b).hexdigest()

comparison = (V1 / "probes/known_hit_universe_probe.py").read_bytes()
comparison_copy = R / "probes/known_hit_universe_probe.v1-copy.py"
comparison_copy.write_bytes(comparison)

original = ORIGINAL.read_text()
if sha(original.encode()) != ORIGINAL_SHA:
    raise SystemExit("retained original probe digest mismatch")
replacements = [
    ("RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v39')", "RT = Path('%s/work/repro-original')" % R),
    ("SRC = RT / 'work/source39-pkg'", "SRC = Path('%s/work/source')" % R),
    ("'standing': 'independent reviewer probe; reference evidence over the verified copy; not product qualification'",
     "'standing': 'author path-only rerun of the retained independent probe against the v1-plus-imported-universe corrected copy; not an independent probe'"),
]
adapted = original
for old, new in replacements:
    if adapted.count(old) != 1:
        raise SystemExit("adaptation anchor not unique: " + old)
    adapted = adapted.replace(old, new)
adapted_path = R / "probes/original-probe.path-only.py"
adapted_path.write_text(adapted)
diff = "".join(difflib.unified_diff(original.splitlines(keepends=True), adapted.splitlines(keepends=True), "claude-original", "author-rerun"))
(R / "probes/original-probe.path-only.diff").write_text(diff)
report = {"comparisonProbeSource": str(V1 / "probes/known_hit_universe_probe.py"), "comparisonProbeSha256": sha(comparison),
          "comparisonProbeCopy": str(comparison_copy), "comparisonCopyIdentical": comparison_copy.read_bytes() == comparison,
          "originalProbe": str(ORIGINAL), "originalProbeSha256": ORIGINAL_SHA, "adaptedProbe": str(adapted_path),
          "adaptedProbeSha256": sha(adapted.encode()), "adaptationDiffLines": diff.count("\n")}
(R / "probes/regression-probes.json").write_text(json.dumps(report, indent=1) + "\n")
print(json.dumps(report, indent=1))
