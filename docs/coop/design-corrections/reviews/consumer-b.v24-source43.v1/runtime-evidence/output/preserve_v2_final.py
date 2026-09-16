"""source42.v3 setup: before any source42.v3 edit, copy the exact source42.v2 final bytes of every output file this runtime changes into
output/preserved/s42-v2-final/ with a sha256 manifest. The complete source42.v2 output also remains in place in the preserved
runtime /tmp/opensip-design-corrections/consumer-b.v24-source42.v2 (not written by this runtime). Refuses to run twice.
Usage: python3 output/preserve_v2_final.py
"""
import hashlib
import json
import os
import shutil
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source42.v3/output/"
DEST = OUT + "preserved/s42-v2-final/"
FILES = ["vectors/phase3_traces.py", "vectors/phase0_custody.py", "vectors/phase0-custody.json",
         "traces/complete.json", "traces/unavailable.json", "traces/cancel.json", "traces/fault.json", "traces/terminal.json", "traces/controls.json",
         "tools/checkpoint_p123.py", "tools/finalize_review.py", "tools/hc_source42.py",
         "requirement-status.json", "blind-review.md", "blind-review.json", "runs/final-custody.json",
         "notes/00-session-standing.md", "notes/10-gaps.md"] + [f"checkpoints/phase-{n}.json" for n in range(12)]


def main():
    if os.path.exists(DEST):
        print("already preserved; refusing to run twice")
        return 1
    rows = []
    for rel in FILES:
        src = OUT + rel
        b = open(src, "rb").read()
        os.makedirs(os.path.dirname(DEST + rel), exist_ok=True)
        shutil.copyfile(src, DEST + rel)
        rows.append({"path": rel, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
    v2 = "/private/tmp/opensip-design-corrections/consumer-b.v24-source42.v2/output/"
    equal_v2 = {r["path"]: os.path.exists(v2 + r["path"]) and hashlib.sha256(open(v2 + r["path"], "rb").read()).hexdigest() == r["sha256"] for r in rows}
    with open(DEST + "manifest.json", "w") as fh:
        json.dump({"standing": "exact source42.v2 final bytes (as copied by the root into source42.v3, before any source42.v3 edit) of files "
                               "changed in source42.v3; rebound executable copies are the post-rebind bytes (output/rebind-v3-manifest.json)",
                   "files": rows, "byteEqualToPreservedV2Runtime": equal_v2}, fh, indent=1)
    print(json.dumps({"preserved": len(rows), "notEqualToV2Runtime": [p for p, ok in equal_v2.items() if not ok]}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
