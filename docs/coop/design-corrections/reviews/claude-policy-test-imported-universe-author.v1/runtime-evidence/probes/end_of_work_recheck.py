"""End-of-work read-only recheck that no frozen, root or completed-author artifact was altered.

1. Every frozen39 manifest member at the snapshot root still matches, with no unlisted file or __pycache__.
2. Root's imported-universe probe: probe.py matches command.json probeSha256; the four suite inputs and report.json match the
   hashes recorded when this runtime first read them (below).
3. The completed v1 author delta: delta-manifest.json and correction.patch digests, and the six v1 corrected files' after hashes.
Writes custody/end-of-work-recheck.json and exits non-zero on any mismatch. Usage: end_of_work_recheck.py
"""
import hashlib
import json
import os
from pathlib import Path

R = Path(__file__).resolve().parent.parent
sha = lambda p: hashlib.sha256(Path(p).read_bytes()).hexdigest()
MANIFEST = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v39.json")
ROOT = Path("/tmp/opensip-design-corrections/root-policy-test-imported-universe-probe.v1")
V1 = Path("/private/tmp/opensip-design-corrections/claude-policy-test-known-hit-author.v1")
RECORDED_SUITES = {
    "frozen39-typescript-suite.json": "f4a17c69bd4a3eb2e08be52f4b95f4ec84219891876ffbc30212e974602f8114",
    "frozen39-rust-suite.json": "3c20d4abcf7f2fa5c7188cc7003f739150540843f502cb3a254587dfd898d36d",
    "author-correction-typescript-suite.json": "f4a17c69bd4a3eb2e08be52f4b95f4ec84219891876ffbc30212e974602f8114",
    "author-correction-rust-suite.json": "3c20d4abcf7f2fa5c7188cc7003f739150540843f502cb3a254587dfd898d36d",
}
faults = []
raw = MANIFEST.read_bytes()
manifest_sha = hashlib.sha256(raw).hexdigest()
if manifest_sha != "f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009":
    faults.append("frozen39 manifest digest")
members = json.loads(raw)["files"]
snapshot = Path(json.loads(raw)["snapshotRoot"])
mismatch = [f["path"] for f in members if sha(snapshot / f["path"]) != f["sha256"]]
listed = {f["path"] for f in members}
unlisted, pycache = [], []
for d, dirs, files in os.walk(snapshot):
    pycache += [str((Path(d) / x).relative_to(snapshot)) for x in dirs if x == "__pycache__"]
    dirs[:] = [x for x in dirs if x != "__pycache__"]
    unlisted += [(Path(d) / n).relative_to(snapshot).as_posix() for n in files if (Path(d) / n).relative_to(snapshot).as_posix() not in listed]
faults += ["frozen39 member " + p for p in mismatch] + ["frozen39 unlisted " + p for p in unlisted] + ["frozen39 pycache " + p for p in pycache]
command = json.loads((ROOT / "command.json").read_text())
root_rows = {"probe.py": {"sha256": sha(ROOT / "probe.py"), "recorded": command["probeSha256"]}}
root_rows |= {name: {"sha256": sha(ROOT / name), "recorded": want} for name, want in RECORDED_SUITES.items()}
root_rows["report.json"] = {"sha256": sha(ROOT / "report.json"), "rowsEqualAdaptedPreFix": json.loads((ROOT / "report.json").read_text())["rows"]
                            == json.loads((R / "probes/root-adapted/pre-fix/report.json").read_text())["rows"]}
faults += ["root " + n for n, row in root_rows.items() if row.get("recorded") not in (None, row["sha256"]) or row.get("rowsEqualAdaptedPreFix") is False]
v1_manifest = json.loads((V1 / "custody/delta-manifest.json").read_text())
v1_rows = {"deltaManifestSha256": sha(V1 / "custody/delta-manifest.json"), "patchSha256": sha(V1 / "output/correction.patch"),
           "patchMatchesRecorded": sha(V1 / "output/correction.patch") == "8fe83cd122eefeec384f4d48aebc2c2eaa505a5c1a1bac5958c6fe74672a9f28",
           "afterFilesMatch": {c["path"]: sha(V1 / "work/source39" / c["path"]) == c["afterSha256"] for c in v1_manifest["changes"]}}
if not v1_rows["patchMatchesRecorded"] or not all(v1_rows["afterFilesMatch"].values()):
    faults.append("v1 author delta changed")
report = {"frozen39": {"manifestSha256": manifest_sha, "members": len(members), "mismatch": mismatch, "unlisted": unlisted, "pycache": pycache},
          "rootImportedUniverseProbe": root_rows, "v1AuthorDelta": v1_rows, "faults": faults}
(R / "custody/end-of-work-recheck.json").write_text(json.dumps(report, indent=1) + "\n")
print(json.dumps({"faults": faults, "frozen39Members": len(members), "v1": {k: v for k, v in v1_rows.items() if k != "afterFilesMatch"}}, indent=1))
raise SystemExit(1 if faults else 0)
