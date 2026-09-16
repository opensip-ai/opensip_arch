"""Determinism/portability comparison of two rebuilt packages (e.g. attempt2 in-runtime vs attempt3 from another cwd).

Compares every file of the two package trees by digest; classifies export stores and claims separately from
provenance/manifest files, which legitimately embed absolute --out paths. Writes OUT_JSON and prints a summary.
Usage: compare_attempts.py PACKAGE_A PACKAGE_B OUT_JSON
"""
import hashlib
import json
import os
import sys
from pathlib import Path

a_root, b_root, out = Path(sys.argv[1]), Path(sys.argv[2]), Path(sys.argv[3])


def walk(root):
    rows = {}
    for d, dirs, files in os.walk(root):
        dirs[:] = [x for x in dirs if x != "__pycache__"]
        for name in files:
            p = Path(d) / name
            rows[p.relative_to(root).as_posix()] = hashlib.sha256(p.read_bytes()).hexdigest()
    return rows


a, b = walk(a_root), walk(b_root)
differ = sorted(r for r in set(a) & set(b) if a[r] != b[r])
only_a, only_b = sorted(set(a) - set(b)), sorted(set(b) - set(a))
exports = sorted(r for r in set(a) | set(b) if r.endswith(".store.json") or r.endswith("claims.json") or r.endswith("variants.json"))
export_differ = [r for r in exports if a.get(r) != b.get(r)]
report = {"packageA": str(a_root), "packageB": str(b_root), "filesA": len(a), "filesB": len(b),
          "exportFilesCompared": len(exports), "exportFilesDiffering": export_differ,
          "allFilesDiffering": differ, "onlyInA": only_a, "onlyInB": only_b,
          "exportsByteIdentical": not export_differ and not only_a and not only_b}
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(report, indent=1) + "\n")
print(json.dumps({k: report[k] for k in ("filesA", "filesB", "exportFilesCompared", "exportFilesDiffering", "exportsByteIdentical")}
                 | {"nonExportFilesDiffering": [r for r in differ if r not in exports]}, indent=1))
