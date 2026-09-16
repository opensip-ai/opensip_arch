"""Preserve the ORIGINAL (pre-correction) ported helper sources and every Run store/build/replay produced by them under the
source39 kit, before any helper correction is applied. Copies are byte-exact; a manifest records each SHA-256.

Destination: output/preserved/s39-original/{ref,builders,tools,runs}/... plus manifest.json. Refuses to overwrite an existing
preserved set, so the original bytes can never be replaced by corrected ones.
Usage: python3 tools/seq.py <label> tools/preserve_original.py
"""
import glob
import hashlib
import json
import os
import shutil
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source39.v2/output"
DST = OUT + "/preserved/s39-original"


def main():
    if os.path.exists(DST + "/manifest.json"):
        print("preserved set already exists; not overwritten")
        return 0
    rows = []
    patterns = ["ref/*.py", "builders/*.py", "tools/*.py", "vectors/*.py", "runs/*.json"]
    for pat in patterns:
        for src in sorted(glob.glob(f"{OUT}/{pat}")):
            rel = os.path.relpath(src, OUT)
            dst = f"{DST}/{rel}"
            os.makedirs(os.path.dirname(dst), exist_ok=True)
            shutil.copyfile(src, dst)
            b = open(dst, "rb").read()
            rows.append({"path": rel, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
    manifest = {"standing": ("Original ported helpers and the Runs they built under the source39 kit, before any source39 helper "
                             "correction. Original closure outcome: every one of 26 Runs refused at owning-schema admission "
                             "(execution-inputs /nativeCoverageAccounts/0/targetUniverse not null); logs/s39-original*.log."),
                "files": rows}
    with open(DST + "/manifest.json", "w") as fh:
        json.dump(manifest, fh, indent=1)
    print(json.dumps({"preserved": len(rows), "destination": os.path.relpath(DST, OUT)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
