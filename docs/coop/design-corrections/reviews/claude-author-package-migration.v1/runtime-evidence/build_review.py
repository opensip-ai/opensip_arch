"""Assemble review.json at the runtime root from actual custody, manifests, reports and receipts (no hand-typed results).

Refuses unless the designated final rebuild passed, every expected group outcome is present, and the probe passed.
Usage: build_review.py FINAL_RUN_DIR
"""
import hashlib
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
FINAL = Path(sys.argv[1]).resolve()
load = lambda p: json.loads(Path(p).read_text())
fsha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()


def receipts(root):
    rows = []
    for d in sorted(p for p in Path(root).iterdir() if p.is_dir()):
        cmd = load(d / "command.json") if (d / "command.json").exists() else {}
        dig = load(d / "digests.json") if (d / "digests.json").exists() else {}
        exit_code = (d / "exit.txt").read_text().strip() if (d / "exit.txt").exists() else cmd.get("exit", "NO-EXIT")
        rows.append({"label": d.name, "argv": cmd.get("argv"), "cwd": cmd.get("cwd"), "exit": str(exit_code),
                     "seconds": dig.get("seconds", cmd.get("seconds")), "stdoutSha256": dig.get("stdoutSha256", cmd.get("stdoutSha256"))})
    return rows


final_report = load(FINAL / "rebuild-report.json")
verification = final_report["verification"]
probe = final_report["nativeV2Probe"]
if not (final_report["passed"] and verification["passed"] and probe["passed"]):
    raise SystemExit("final rebuild did not pass")
groups = {g["group"]: g for g in verification["groups"]}
expected = {"checkpoint3": 1, "normalized-examples6": 4, "rust-selection-examples1": 2, "semantic-controls1": 3,
            "binding-controls": 3, "normalization-map-controls1": 4, "query": 7}
for name, count in expected.items():
    if not groups[name]["passed"] or groups[name]["count"] != count:
        raise SystemExit("group outcome missing: " + name)
custody = load(HERE / "custody/captured-source.json")
package_manifest = FINAL / "package/artifact-manifest.json"
review = {
    "artifact": "author-package-migration.review", "version": 1,
    "standing": ("Provisional AUTHOR-constructor migration evidence against a CAPTURED mutable successor source. Not independent "
                 "review, not blind work, not frozen-candidate39 acceptance, not a whole-source review, not product "
                 "implementation. Author-derived self-consistency under owner replay is not an independent implementation."),
    "runtime": str(HERE),
    "capturedSource": {k: custody[k] for k in ("input", "capture", "fileCount", "totalBytes", "copyFaults", "inputDriftDuringCapture", "capturedFileListSha256")}
                      | {"source38": {k: custody["source38"][k] for k in ("manifest", "sha256", "fileCount", "unchanged")},
                         "source38Modified": custody["source38"]["modified"], "source38Added": custody["source38"]["added"],
                         "source38Missing": custody["source38"]["missing"],
                         "packageSourceManifestSha256": final_report["inputs"]["sourceManifestSha256"]},
    "package15Copy": load(HERE / "custody/package15-copy.json"),
    "overlay": load(HERE / "overlay/overlay-manifest.json") | {"overlayManifestSha256": fsha(HERE / "overlay/overlay-manifest.json"),
                                                             "diff": "output/overlay/overlay-vs-package15.diff",
                                                             "diffFileSha256": fsha(HERE / "output/overlay/overlay-vs-package15.diff")},
    "finalRebuild": {"dir": str(FINAL), "reportSha256": fsha(FINAL / "rebuild-report.json"), "inputs": final_report["inputs"],
                     "commands": final_report["commands"], "construction": final_report["construction"]["failed"],
                     "packageManifestSha256": fsha(package_manifest), "packageFiles": len(load(package_manifest)["files"])},
    "verification": verification,
    "nativeV2Probe": probe,
    "exportComparison": final_report["exportComparison"],
    "baseline": load(HERE / "work/baseline-summary.json"),
    "packageDiff": {k: v for k, v in load(HERE / "output/package-vs-package15.json").items() if k != "files"}
                   | {"files": load(HERE / "output/package-vs-package15.json")["files"]},
    "determinism": load(HERE / "output/attempt2-vs-attempt3.json"),
    "extraProbesOnFinalPackage": {"authorProperties": load(HERE / "work/probes-final/author-properties.json"),
                                  "mixedUniverseView": load(HERE / "work/probes-final/mixed-universe-view.probe.json")},
    "endOfTaskCustodyRecheck": load(HERE / "custody/end-of-task-recheck.json"),
    "receipts": {"runtime": receipts(HERE / "receipts")},
}
review["receipts"]["rebuilds"] = {}
for report_path in sorted((HERE / "runs").rglob("work/receipts")):
    review["receipts"]["rebuilds"][str(report_path.relative_to(HERE))] = receipts(report_path)
text = json.dumps(review, indent=1) + "\n"
(HERE / "review.json").write_text(text)
print(json.dumps({"review": str(HERE / "review.json"), "sha256": hashlib.sha256(text.encode()).hexdigest(),
                  "groups": {k: (groups[k]["passed"], groups[k]["count"]) for k in expected},
                  "packageManifestSha256": review["finalRebuild"]["packageManifestSha256"]}, indent=1))
