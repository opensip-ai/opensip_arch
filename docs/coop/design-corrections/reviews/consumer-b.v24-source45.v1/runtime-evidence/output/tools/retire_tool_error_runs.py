"""Retire Run stores built by an own tool error so they cannot be read as measurements, keeping their bytes and outcomes.

The first version of tools/replay_all.py built the Rust designed-negative mutations ambiguous-fact-present and partial-fact-present
over rust-mixed, whose ownership is neither ambiguous nor partial, so the mutation changed nothing and the Runs admitted
(logs/s39-replay-all.0.replay_all.log). This origin's prior runtime built them over rust-ambiguous / rust-partial (HC-27). The files are
moved, never deleted, to preserved/s39-tool-error/ with a SHA-256 manifest.
Usage: python3 tools/seq.py <label> tools/retire_tool_error_runs.py
"""
import hashlib
import json
import os
import shutil
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source45.v1/output"
DST = OUT + "/preserved/s39-tool-error"
NAMES = ["rust-mixed~ambiguous-fact-present", "rust-mixed~partial-fact-present"]


def main():
    os.makedirs(DST, exist_ok=True)
    mpath = DST + "/manifest.json"
    manifest = json.load(open(mpath)) if os.path.exists(mpath) else {
        "standing": "Runs built over the wrong base variant by an own tool error (HC-27); outcomes are not measurements of the mutation.",
        "files": []}
    for name in NAMES:
        for suffix in (".store.json", ".build.json", ".replay.json"):
            src = f"{OUT}/runs/{name}{suffix}"
            if not os.path.exists(src):
                continue
            data = open(src, "rb").read()
            shutil.move(src, f"{DST}/{name}{suffix}")
            manifest["files"].append({"path": f"runs/{name}{suffix}", "sha256": hashlib.sha256(data).hexdigest(), "bytes": len(data)})
    with open(mpath, "w") as fh:
        json.dump(manifest, fh, indent=1)
    print(json.dumps({"retired": len(manifest["files"]), "destination": os.path.relpath(DST, OUT)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
