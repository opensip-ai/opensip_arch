"""Apply the COMPLETE reviewed v1 delta to the fresh frozen39 capture, with provenance and before-images.

1. The v1 delta manifest's patch file must hash to 8fe83cd1...2a9f28 and the manifest must list exactly six modified files.
2. For each change: the capture's current bytes must equal beforeSha256/beforeBytes (these bytes are saved as the
   before-image under work/before-images-v39); the after bytes are read from the completed v1 corrected copy and must equal
   afterSha256/afterBytes.
3. The unified diff regenerated from those exact before/after bytes (same generator as v1 make_delta.py) must reproduce the
   v1 patch text byte for byte, so the applied bytes ARE the reviewed patch.
4. The after bytes are written into the capture (fresh file replace) and re-hashed.
Writes OUT_JSON; non-zero exit on any fault. Usage: apply_v1_delta.py CAPTURE OUT_JSON
"""
import difflib
import hashlib
import json
import sys
from pathlib import Path

V1 = Path("/private/tmp/opensip-design-corrections/claude-policy-test-known-hit-author.v1")
PATCH_SHA = "8fe83cd122eefeec384f4d48aebc2c2eaa505a5c1a1bac5958c6fe74672a9f28"
R = Path(__file__).resolve().parent
capture, out_json = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve()
sha = lambda b: hashlib.sha256(b).hexdigest()
manifest_raw = (V1 / "custody/delta-manifest.json").read_bytes()
manifest = json.loads(manifest_raw)
patch = (V1 / manifest["patch"]).read_bytes()
faults = []
if sha(patch) != PATCH_SHA or manifest["patchSha256"] != PATCH_SHA:
    faults.append("patch sha mismatch")
if len(manifest["changes"]) != 6 or {c["status"] for c in manifest["changes"]} != {"modified"}:
    faults.append("manifest is not exactly six modified files")
rows, parts, pending = [], [], []
for c in manifest["changes"]:
    rel = c["path"]
    before = (capture / rel).read_bytes()
    after = (V1 / "work/source39" / rel).read_bytes()
    ok_before = sha(before) == c["beforeSha256"] and len(before) == c["beforeBytes"]
    ok_after = sha(after) == c["afterSha256"] and len(after) == c["afterBytes"]
    if not (ok_before and ok_after):
        faults.append("hash mismatch for " + rel)
    image = R / "work/before-images-v39" / rel
    image.parent.mkdir(parents=True, exist_ok=True)
    with open(image, "xb") as fh:
        fh.write(before)
    parts.extend(difflib.unified_diff(before.decode().splitlines(keepends=True), after.decode().splitlines(keepends=True),
                                      fromfile="a/" + rel, tofile="b/" + rel, n=3))
    rows.append({"path": rel, "beforeSha256": sha(before), "beforeVerified": ok_before, "afterSha256": sha(after), "afterVerified": ok_after,
                 "beforeImage": str(image.relative_to(R))})
    pending.append((rel, after))
regenerated = "".join(parts).encode()
if regenerated != patch:
    faults.append("regenerated diff does not reproduce the v1 patch")
if not faults:
    for rel, after in pending:
        target = capture / rel
        target.unlink()
        with open(target, "xb") as fh:
            fh.write(after)
        if sha(target.read_bytes()) != sha(after):
            faults.append("write verify failed for " + rel)
report = {"artifact": "policy-test-imported-universe-author.v1-delta-application", "version": 1,
          "v1DeltaManifest": str(V1 / "custody/delta-manifest.json"), "v1DeltaManifestSha256": sha(manifest_raw),
          "v1Patch": str(V1 / manifest["patch"]), "v1PatchSha256": sha(patch), "regeneratedPatchEqualsV1Patch": regenerated == patch,
          "afterBytesSource": str(V1 / "work/source39"), "changes": rows, "applied": not faults, "faults": faults}
out_json.parent.mkdir(parents=True, exist_ok=True)
out_json.write_text(json.dumps(report, indent=1) + "\n")
print(json.dumps(report, indent=1))
raise SystemExit(1 if faults else 0)
