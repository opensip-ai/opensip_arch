"""Copy the completed v1 author source into this v2 runtime and verify it byte for byte.

Usage: python -I -B copy_v1_source.py copy|verify DEST
The v1 runtime is read-only history. `copy` refuses an existing DEST. Verification checks DEST against
(a) the frozen37 manifest for every path v1 did not change, (b) v1's after-manifest for the eight v1 targets,
and (c) the v1 source tree itself file by file, so any drift in v1 is also reported.
"""
import hashlib
import json
import os
import shutil
import sys

MANIFEST = "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v37.json"
MANIFEST_SHA = "245ef613243aafeaac2dcdca7f0b398d5a770ec338abbf712039fdfd91676680"
V1 = "/tmp/opensip-design-corrections/claude-source37-host-finalizer-author.v1"
V1_SOURCE = V1 + "/source"
mode, dest = sys.argv[1], sys.argv[2]

raw = open(MANIFEST, "rb").read()
if hashlib.sha256(raw).hexdigest() != MANIFEST_SHA:
    raise SystemExit("manifest hash mismatch")
manifest = {f["path"]: f["sha256"] for f in json.loads(raw)["files"]}
v1_after = json.load(open(V1 + "/after-manifest.json"))
v1_targets = {r["path"]: r["sha256"] for r in v1_after["files"]}


def sha(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def tree(root):
    out = {}
    for d, _, fs in os.walk(root):
        for fn in fs:
            full = os.path.join(d, fn)
            rel = os.path.relpath(full, root)
            if "__pycache__" not in rel.split(os.sep):
                out[rel] = sha(full)
    return out


def verify(root):
    got = tree(root)
    expected = dict(manifest)
    expected.update(v1_targets)
    mismatch = sorted(p for p in expected if got.get(p) != expected[p])
    extra = sorted(set(got) - set(expected))
    return {"root": root, "files": len(got), "expectedFiles": len(expected), "mismatchOrMissing": mismatch,
            "extra": extra, "exact": not mismatch and not extra}


if mode == "copy":
    v1_check = verify(V1_SOURCE)
    if not v1_check["exact"]:
        print(json.dumps({"v1": v1_check}, indent=1))
        raise SystemExit("v1 source does not equal frozen37 + v1 after-manifest; refusing to copy")
    if os.path.exists(dest):
        raise SystemExit(f"{dest} exists; refusing to overwrite")
    shutil.copytree(V1_SOURCE, dest, symlinks=True, ignore=shutil.ignore_patterns("__pycache__"))
    result = {"v1SourceVerified": True, "v1AfterManifestSha256": sha(V1 + "/after-manifest.json"), "copy": verify(dest)}
    code = 0 if result["copy"]["exact"] else 1
elif mode == "verify":
    result = {"copy": verify(dest)}
    code = 0
else:
    raise SystemExit("mode must be copy or verify")
print(json.dumps(result, indent=1))
raise SystemExit(code)
