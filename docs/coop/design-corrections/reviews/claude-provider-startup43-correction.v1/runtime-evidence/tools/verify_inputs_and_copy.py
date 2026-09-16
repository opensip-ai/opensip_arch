"""Verify the handoff hashes, frozen43 and the wire43 work copy, then make an exact copy into this runtime.

usage: verify_inputs_and_copy.py <receipt-json>

The wire43 work copy must equal frozen43's manifest except exactly the files named by the wire43
delta-final/files.json, which must carry their recorded after-hashes. The copy in this runtime is then
verified against the same expectation. Nothing outside this runtime is written.
"""
import hashlib
import json
import os
import shutil
import sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parents[1]
MANIFEST = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v43.json")
MANIFEST_SHA = "db43ee76f91b08dc5076d152761ddef795a3645fafa690a3974d693bedaf897d"
FROZEN = Path("/tmp/opensip-design-corrections/candidate-subject.v43")
WIRE = Path("/tmp/opensip-design-corrections/claude-provider-wire43-correction.v1")
HANDOFF = {
    "review.md": "8ce242fdf8f9f7524030ede6596419b371975c10a575b8f76536df608dd8cc0c",
    "review.json": "6625215cb979d64e8b12b474cc736548b2541d1ae364a7551b29d45e04fff06e",
    "delta-final/files.json": "afa1548dd4fa0e79408202dc6a183102c98a348482f7d0766857fdcccc73ed8d",
    "delta-final/unified.patch": "19f60c60576c469ddc84d79fed0af0ffd8d324f240450c4acd3cabd793f6beed",
    "hash-index.json": "506a69c7202171fcb6ba3acea7800eb16e8e74fec324ee02f8467e1b19b90371",
}


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def tree(root):
    out = {}
    for d, _, files in os.walk(root):
        for f in files:
            p = Path(d) / f
            b = p.read_bytes()
            out[str(p.relative_to(root))] = (hashlib.sha256(b).hexdigest(), len(b))
    return out


receipt = {"handoff": {}, "manifestSha256": sha(MANIFEST)}
for rel, want in HANDOFF.items():
    receipt["handoff"][rel] = {"sha256": sha(WIRE / rel), "expected": want, "ok": sha(WIRE / rel) == want}
manifest = {m["path"]: (m["sha256"], m["bytes"]) for m in json.loads(MANIFEST.read_bytes())["files"]}
frozen = tree(FROZEN)
receipt["frozen43"] = {"members": len(manifest), "ok": frozen == manifest}
delta = json.loads((WIRE / "delta-final" / "files.json").read_text(encoding="utf-8"))["changed"]
expected = dict(manifest)
for row in delta:
    if row["status"] == "removed":
        expected.pop(row["path"])
    else:
        expected[row["path"]] = (row["afterSha256"], row["afterBytes"])
wire_tree = tree(WIRE / "work" / "candidate")
receipt["wire43WorkCopy"] = {"files": len(wire_tree), "ok": wire_tree == expected,
                             "differences": sorted(set(wire_tree.items()) ^ set(expected.items()))[:20]}
ok = receipt["manifestSha256"] == MANIFEST_SHA and all(v["ok"] for v in receipt["handoff"].values()) \
    and receipt["frozen43"]["ok"] and receipt["wire43WorkCopy"]["ok"]
dest = RUNTIME / "work" / "candidate"
if ok:
    if dest.exists():
        raise SystemExit("destination exists")
    shutil.copytree(WIRE / "work" / "candidate", dest, symlinks=True)
    copy_tree = tree(dest)
    receipt["copy"] = {"root": str(dest), "files": len(copy_tree), "ok": copy_tree == expected}
    ok = receipt["copy"]["ok"]
receipt["ok"] = ok
Path(sys.argv[1]).parent.mkdir(parents=True, exist_ok=True)
Path(sys.argv[1]).write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
print(json.dumps({k: (v if k != "wire43WorkCopy" else {"files": v["files"], "ok": v["ok"]}) for k, v in receipt.items()}, indent=1))
