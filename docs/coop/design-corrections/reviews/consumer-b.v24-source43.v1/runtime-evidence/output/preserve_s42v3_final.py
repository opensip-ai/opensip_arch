"""source43.v1 setup: before any source43 edit or execution that rewrites them, copy the exact source42.v3 final bytes of every output file this
runtime may change into output/preserved/s42-v3-final/ with a sha256 manifest. The complete source42.v3 output also remains in place in the
preserved runtime (not read or written by this runtime). Executable copies are recorded as their post-rebind bytes; their pre-rebind hashes are
in output/rebind-s43-manifest.json. Refuses to run twice.
Usage: python3 output/preserve_s42v3_final.py
"""
import hashlib
import json
import os
import shutil
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source43.v1/output/"
DEST = OUT + "preserved/s42-v3-final/"
FILES = (["tools/phase9_graph_query.py", "vectors/graph-query.json", "tools/checkpoint_p9.py", "tools/finalize_review.py", "tools/hc_source42.py",
          "tools/final_custody.py", "vectors/phase0_custody.py", "vectors/phase0-custody.json", "requirement-status.json", "blind-review.md",
          "blind-review.json", "runs/final-custody.json", "notes/00-session-standing.md", "notes/10-gaps.md"]
         + [f"checkpoints/phase-{n}.json" for n in range(12)])


def main():
    if os.path.exists(DEST):
        print("already preserved; refusing to run twice")
        return 1
    rows = []
    for rel in FILES:
        b = open(OUT + rel, "rb").read()
        os.makedirs(os.path.dirname(DEST + rel), exist_ok=True)
        shutil.copyfile(OUT + rel, DEST + rel)
        rows.append({"path": rel, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
    rebind = json.load(open(OUT + "rebind-s43-manifest.json"))
    pre = {r["file"]: r["beforeSha256"] for r in rebind["files"]}
    for r in rows:
        if r["path"] in pre:
            r["preRebindSha256"] = pre[r["path"]]
    with open(DEST + "manifest.json", "w") as fh:
        json.dump({"standing": "exact source42.v3 final bytes (as copied by the root into source43.v1) of files that source43.v1 may change; "
                               "executable files after the runtime-root rebind only (preRebindSha256 recorded)", "files": rows}, fh, indent=1)
    print(json.dumps({"preserved": len(rows)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
