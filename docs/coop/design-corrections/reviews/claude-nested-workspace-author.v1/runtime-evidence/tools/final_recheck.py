"""End-of-work custody recheck.

Usage: final_recheck.py DELTA_MANIFEST OUT_JSON

1. LIVE manifest39 still hashes to the expected sha256; all members of its snapshot root still match (regular files,
   sha256, bytes); unlisted files and __pycache__ directories are reported.
2. The edited capture work/source differs from the manifest in exactly the delta files, each at its after-bytes.
3. Root's probe directory is listed with hashes, and root's report rows equal this runtime's pre-fix path-only
   adaptation rows (same cases, same observed outcomes), i.e. the reproduction reproduced root's observation.
"""
import hashlib
import json
import os
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
MANIFEST = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v39.json")
EXPECTED = "f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009"
ROOT_PROBE = Path("/tmp/opensip-design-corrections/root-nested-workspace-probe.v1")
delta_path, out_json = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()
raw = MANIFEST.read_bytes()
manifest = json.loads(raw)
listed = {f["path"]: f for f in manifest["files"]}


def verify_tree(root, overrides):
    faults, unlisted, pycache = [], [], []
    for path, f in listed.items():
        p = root / path
        want = overrides.get(path, f)
        if p.is_symlink() or not p.is_file():
            faults.append({"path": path, "fault": "missing-or-not-regular"})
            continue
        data = p.read_bytes()
        if sha(data) != want["sha256"] or len(data) != want["bytes"]:
            faults.append({"path": path, "fault": "digest-or-size"})
    for d, dirs, names in os.walk(root):
        pycache += [str((Path(d) / x).relative_to(root)) for x in dirs if x == "__pycache__"]
        dirs[:] = [x for x in dirs if x != "__pycache__"]
        unlisted += [(Path(d) / n).relative_to(root).as_posix() for n in names if (Path(d) / n).relative_to(root).as_posix() not in listed]
    return {"faults": faults, "unlisted": sorted(unlisted), "pycacheDirs": sorted(pycache)}


delta = json.loads(delta_path.read_text())
after = {f["path"]: f["after"] for f in delta["files"]}
frozen = verify_tree(Path(manifest["snapshotRoot"]), {})
capture = verify_tree(HERE / "work/source", after)
root_files = [{"path": p.name, "sha256": sha(p.read_bytes()), "bytes": p.stat().st_size} for p in sorted(ROOT_PROBE.iterdir()) if p.is_file()]
root_rows = json.loads((ROOT_PROBE / "report.json").read_text())["rows"]
adapted_rows = json.loads((HERE / "results/prefix/root-adapted.json").read_text())["rows"]
out = {"artifact": "nested-workspace-author.final-recheck", "version": 1,
       "manifest": {"path": str(MANIFEST), "sha256": sha(raw), "holds": sha(raw) == EXPECTED, "memberCount": len(listed)},
       "frozen39Snapshot": frozen, "editedCaptureAgainstDelta": capture,
       "rootProbeDirectory": {"path": str(ROOT_PROBE), "files": root_files},
       "rootReportRowsEqualAdaptedPrefixRows": root_rows == adapted_rows}
out["holds"] = (out["manifest"]["holds"] and not frozen["faults"] and not frozen["unlisted"] and not capture["faults"]
                and not capture["unlisted"] and not capture["pycacheDirs"] and out["rootReportRowsEqualAdaptedPrefixRows"])
out_json.parent.mkdir(parents=True, exist_ok=True)
out_json.write_text(json.dumps(out, indent=1) + "\n")
print(json.dumps({"manifestHolds": out["manifest"]["holds"], "frozen39Faults": len(frozen["faults"]), "frozen39Unlisted": frozen["unlisted"][:10],
                  "frozen39Pycache": frozen["pycacheDirs"][:10], "captureFaults": capture["faults"][:10], "captureUnlisted": capture["unlisted"][:10],
                  "capturePycache": capture["pycacheDirs"][:10], "rootFiles": root_files,
                  "rootReportRowsEqualAdaptedPrefixRows": out["rootReportRowsEqualAdaptedPrefixRows"], "holds": out["holds"]}, indent=1))
raise SystemExit(0 if out["holds"] else 1)
