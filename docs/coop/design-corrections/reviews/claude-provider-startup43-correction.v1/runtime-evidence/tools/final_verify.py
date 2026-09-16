"""Final custody verification, read-only except for its receipt.

usage: final_verify.py <receipt-json>

Re-verifies frozen43 against its manifest, the five wire43 handoff hashes, the wire43 work copy against
frozen43 + wire43 delta-final, the prior TS assessment runtime hash index, and that every changed file in this
runtime's scratch-after copy equals the corrected work copy.
"""
import hashlib
import json
import os
import sys
from pathlib import Path

RUNTIME = Path(__file__).resolve().parents[1]
MANIFEST = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v43.json")
MANIFEST_SHA = "db43ee76f91b08dc5076d152761ddef795a3645fafa690a3974d693bedaf897d"
FROZEN = Path("/tmp/opensip-design-corrections/candidate-subject.v43")
WIRE = Path("/tmp/opensip-design-corrections/claude-provider-wire43-correction.v1")
ASSESS = Path("/tmp/opensip-design-corrections/claude-ts-protocol43-publication-assessment.v1")
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


manifest = {m["path"]: (m["sha256"], m["bytes"]) for m in json.loads(MANIFEST.read_bytes())["files"]}
receipt = {"manifestSha256Ok": sha(MANIFEST) == MANIFEST_SHA}
frozen_tree = tree(FROZEN)
receipt["frozen43"] = {"members": len(manifest), "bytes": sum(v[1] for v in frozen_tree.values()), "ok": frozen_tree == manifest}
receipt["wire43Handoff"] = {rel: sha(WIRE / rel) == want for rel, want in HANDOFF.items()}
expected = dict(manifest)
for row in json.loads((WIRE / "delta-final" / "files.json").read_text(encoding="utf-8"))["changed"]:
    expected[row["path"]] = (row["afterSha256"], row["afterBytes"])
receipt["wire43WorkCopyOk"] = tree(WIRE / "work" / "candidate") == expected
index = json.loads((ASSESS / "hash-index.json").read_text(encoding="utf-8"))
receipt["priorAssessmentRuntimeOk"] = all(sha(ASSESS / f["path"]) == f["sha256"] for f in index["files"])
changed = json.loads((RUNTIME / "delta" / "cumulative-vs-frozen43" / "files.json").read_text(encoding="utf-8"))["changed"]
receipt["scratchAfterEqualsWorkForChangedFiles"] = all(
    sha(RUNTIME / "scratch-after" / "candidate" / r["path"]) == sha(RUNTIME / "work" / "candidate" / r["path"]) == r["currentSha256"]
    for r in changed if r["status"] != "removed")
receipt["ok"] = (receipt["manifestSha256Ok"] and receipt["frozen43"]["ok"] and all(receipt["wire43Handoff"].values())
                 and receipt["wire43WorkCopyOk"] and receipt["priorAssessmentRuntimeOk"]
                 and receipt["scratchAfterEqualsWorkForChangedFiles"])
Path(sys.argv[1]).write_text(json.dumps(receipt, indent=1) + "\n", encoding="utf-8")
print(json.dumps(receipt, indent=1))
