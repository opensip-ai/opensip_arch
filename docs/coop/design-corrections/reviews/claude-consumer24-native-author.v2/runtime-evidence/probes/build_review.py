"""Assemble output/review.json from this runtime's actual receipts and manifests (no hand-typed results).

Reads: dispatch.json; output/changed-files.v1.json; output/v1-to-v2.changed-files.json; receipts/registered-documents-v2;
receipts/goldens-rewrite-apply; work/goldens-ids-corrected.json; every receipts/*/ of v2 and v1 (all attempts);
receipts/corrections-v2-final (corrections checker rows). Findings dispositions are declared in FINDINGS below and
each names the controls that exercise it; the builder refuses if a named control row is absent or failed.
Usage: build_review.py
"""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
V1 = Path("/private/tmp/opensip-design-corrections/claude-consumer24-native-author.v1")
OUT = HERE / "output"


def load(path):
    return json.loads(Path(path).read_text())


def receipts(root):
    rows = []
    for d in sorted(p for p in (root / "receipts").iterdir() if p.is_dir()):
        cmd = load(d / "command.json") if (d / "command.json").exists() else {}
        dig = load(d / "digests.json") if (d / "digests.json").exists() else {}
        rows.append({"label": d.name, "argv": cmd.get("argv"), "cwd": cmd.get("cwd"),
                     "exit": (d / "exit.txt").read_text().strip() if (d / "exit.txt").exists() else "NO-EXIT",
                     "seconds": dig.get("seconds"), "stdoutSha256": dig.get("stdoutSha256")})
    return rows


corrections = load(HERE / "receipts/corrections-v2-final/stdout.txt")
by_case = {(r["item"], r["case"]): r for r in corrections["rows"]}

FINDINGS = {
    "M1": {"disposition": "corrected", "controlPrefix": "M1"},
    "M2": {"disposition": "corrected", "controlPrefix": "M2"},
    "M3": {"disposition": "corrected", "controlPrefix": "M3"},
    "S1": {"disposition": "corrected", "controlPrefix": "S1"},
    "S2": {"disposition": "corrected", "controlPrefix": "S2"},
    "S3": {"disposition": "corrected", "controlPrefix": "S3"},
    "S4": {"disposition": "corrected", "controlPrefix": "S4"},
    "A1": {"disposition": "corrected", "controlPrefix": "A1"},
    "A2": {"disposition": "corrected", "controlPrefix": "A2"},
    "A4": {"disposition": "corrected", "controlPrefix": "A4"},
    "A5": {"disposition": "corrected-by-merge", "controlPrefix": None},
}
findings = {}
for item, spec in FINDINGS.items():
    rows = [r for (i, _), r in by_case.items() if i == item] if spec["controlPrefix"] else []
    if spec["controlPrefix"] and (not rows or not all(r["ok"] for r in rows)):
        raise SystemExit("control rows missing or failing for " + item)
    findings[item] = {"disposition": spec["disposition"], "controls": len(rows),
                      "controlsPassed": sum(r["ok"] for r in rows),
                      "realRunControls": sorted(r["case"] for r in rows if "real-run" in r["case"])}

native_report = load(HERE / "work/native-evidence-report.v2-final.json")
a5_cases = [r for r in native_report["cases"]["results"] if r["id"] in (
    "ts-tsconfig-explicit-allowjs-false-excludes-js", "tsconfig-checkjs-only-admits-js",
    "tsconfig-checkjs-only-without-js-roots", "jsconfig-explicit-allowjs-false-excludes-js",
    "js-allowjs-checkjs-not-completeness")]
findings["A5"].update({"nativeCases": [{"id": r["id"], "passed": r["passed"]} for r in a5_cases]})
if len(a5_cases) != 5 or not all(r["passed"] for r in a5_cases):
    raise SystemExit("A5 native cases missing or failing")

goldens = load(HERE / "work/goldens-ids-corrected.json")
v2_receipts = receipts(HERE)
final = [r for r in v2_receipts if r["label"].endswith("-v2-final")]
review = {
    "artifact": "consumer24-native-author.review", "version": 2,
    "standing": ("Actual same Claude coauthor correction evidence (continuation of partial v1). Architecture/design/reference "
                 "only. No product implementation, commit, push, pin, planning or acceptance/readiness claim."),
    "dispatch": load(HERE / "dispatch.json"),
    "sourceParent": {"manifest": "docs/coop/design-corrections/reviews/candidate-subject.v38.json",
                     "sha256": "2ddfa0dbfc101b264c24d2a1f63de1e4e70908ac2a7346eaf0dab09d37f7e5c5"},
    "v1Continuation": {"partialManifestSha256": "14f29c964f2e578b8f6283635239bdc42000677a332417d675d1afda0e22b91c",
                       "copyVerification": load(HERE / "receipts/copy-v1/stdout.txt") | {"copiedTools": "see receipt"}},
    "findings": findings,
    "registeredDocumentConsequences": load(HERE / "receipts/registered-documents-v2/stdout.txt"),
    "goldens": {"file": "docs/coop/design-corrections/foundation/run-termination-goldens.v1.json",
                "rewrite": load(HERE / "receipts/goldens-rewrite-apply/stdout.txt"),
                "currentDerivedTerminations": {k: v["derivedTermination"] for k, v in goldens.items()},
                "checkerChildCommands": [
                    "python -I -B docs/coop/design-corrections/foundation/check-semantic-replay.v3.py",
                    "python -I -B docs/coop/design-corrections/foundation/check-native-consumer24-corrections.v1.py"]},
    "diffs": {"vsSource38": {k: v for k, v in load(OUT / "changed-files.v1.json").items() if k != "files"}
              | {"files": load(OUT / "changed-files.v1.json")["files"], "diffPath": "output/source38-to-corrected.diff"},
              "incrementalVsV1": load(OUT / "v1-to-v2.changed-files.json") | {"diffPath": "output/v1-to-v2.diff"}},
    "checks": {"final": final, "finalNonZero": [r for r in final if r["exit"] != "0"],
               "corrections": {"total": corrections["total"], "passed": corrections["passed"], "failed": corrections["failed"]},
               "nativeReport": {"result": native_report["result"], "cases": {k: native_report["cases"][k] for k in ("total", "passed", "failed")}}},
    "attempts": {"v2": v2_receipts, "v1NonZero": [r for r in receipts(V1) if r["exit"] != "0"]},
}
OUT.mkdir(exist_ok=True)
text = json.dumps(review, indent=1) + "\n"
(OUT / "review.json").write_text(text)
print(json.dumps({"review": str(OUT / "review.json"), "sha256": hashlib.sha256(text.encode()).hexdigest(),
                  "findings": {k: (v["disposition"], v.get("controlsPassed"), v.get("controls")) for k, v in findings.items()},
                  "finalNonZero": [(r["label"], r["exit"]) for r in review["checks"]["finalNonZero"]]}, indent=1))
