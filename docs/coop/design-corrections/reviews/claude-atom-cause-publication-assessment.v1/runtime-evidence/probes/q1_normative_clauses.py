"""Where, in the NORMATIVE-ONLY kit, is each atom cause's emission condition published?

Normative-only kit = published contracts (.md) + schemas/registries (.json). ALL reference Python
(.py) is EXCLUDED, per root: a consumer must derive proof causes from published clauses alone.
Historical review folders are excluded as non-current.

READ-ONLY.
"""
import json
import re
from pathlib import Path

S = Path("/tmp/opensip-design-corrections/candidate-subject.v33")
ROOTS = [S / "docs/v2/contracts", S / "docs/coop/design-corrections"]
EXCLUDE_DIR = re.compile(r"/(reviews|__pycache__|disposable|before-image|quarantine)/")

CAUSES = [
    "missing-relation-coverage", "selector-unbound", "coverage-unknown",
    "uncovered-expected-source-subject", "scope-without-coverage",
    "unavailable-program-binding", "population-unknown", "required-relation-missing",
]

files = []
for root in ROOTS:
    for p in sorted(root.rglob("*")):
        if not p.is_file() or p.suffix.lower() not in (".md", ".json"):
            continue
        if EXCLUDE_DIR.search(str(p) + "/"):
            continue
        files.append(p)

out = {
    "standing": "READ-ONLY clause census over the NORMATIVE-ONLY kit. All .py excluded.",
    "kitFileCount": len(files),
    "kitRoots": [str(r) for r in ROOTS],
    "excluded": "every *.py (reference model), reviews/, __pycache__/, disposable/, "
                "before-image*/, quarantine*/",
}

hits = {c: [] for c in CAUSES}
for p in files:
    try:
        text = p.read_text(encoding="utf-8", errors="replace")
    except Exception:  # noqa: BLE001
        continue
    lines = text.splitlines()
    for c in CAUSES:
        for i, line in enumerate(lines, 1):
            if c in line:
                hits[c].append({
                    "file": str(p.relative_to(S)), "line": i,
                    "text": line.strip()[:400],
                })
out["hits"] = hits
out["hitCounts"] = {c: len(v) for c, v in hits.items()}

# Which files carry any of them?
byfile = {}
for c, rows in hits.items():
    for r in rows:
        byfile.setdefault(r["file"], set()).add(c)
out["filesCarryingAnyCause"] = {k: sorted(v) for k, v in sorted(byfile.items())}
print(json.dumps(out, indent=2, default=str))
