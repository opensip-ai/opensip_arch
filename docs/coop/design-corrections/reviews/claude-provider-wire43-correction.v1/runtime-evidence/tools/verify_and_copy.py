"""Verify frozen43 against its manifest and make an exact mutable copy.

Writes only inside this runtime. Frozen43 is opened read-only.
usage: verify_and_copy.py verify <root> <receipt>
       verify_and_copy.py copy <root> <dest> <receipt>
"""
import hashlib
import json
import os
import shutil
import sys

MANIFEST = "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v43.json"
MANIFEST_SHA = "db43ee76f91b08dc5076d152761ddef795a3645fafa690a3974d693bedaf897d"


def load_manifest():
    raw = open(MANIFEST, "rb").read()
    got = hashlib.sha256(raw).hexdigest()
    return json.loads(raw), got


def listing(root):
    out = set()
    for d, dirs, files in os.walk(root):
        for f in files:
            out.add(os.path.relpath(os.path.join(d, f), root))
    return out


def verify(root):
    man, got = load_manifest()
    missing, mismatched, size_mismatch = [], [], []
    bytes_read = 0
    for m in man["files"]:
        p = os.path.join(root, m["path"])
        if not os.path.isfile(p):
            missing.append(m["path"])
            continue
        b = open(p, "rb").read()
        bytes_read += len(b)
        if len(b) != m["bytes"]:
            size_mismatch.append(m["path"])
        if hashlib.sha256(b).hexdigest() != m["sha256"]:
            mismatched.append(m["path"])
    extra = sorted(listing(root) - {m["path"] for m in man["files"]})
    return {
        "root": root,
        "manifest": MANIFEST,
        "manifestSha256": got,
        "shaOk": got == MANIFEST_SHA,
        "members": len(man["files"]),
        "fileCount": man["fileCount"],
        "bytesRead": bytes_read,
        "totalBytes": man["totalBytes"],
        "missing": len(missing),
        "mismatched": len(mismatched),
        "sizeMismatch": len(size_mismatch),
        "extra": len(extra),
        "missingPaths": missing[:50],
        "mismatchedPaths": mismatched[:50],
        "extraPaths": extra[:50],
        "ok": got == MANIFEST_SHA and not (missing or mismatched or size_mismatch or extra),
    }


def main():
    mode = sys.argv[1]
    if mode == "verify":
        res = verify(sys.argv[2])
        receipt = sys.argv[3]
    elif mode == "copy":
        src, dest, receipt = sys.argv[2], sys.argv[3], sys.argv[4]
        if os.path.exists(dest):
            raise SystemExit("destination exists: " + dest)
        man, _ = load_manifest()
        for m in man["files"]:
            s = os.path.join(src, m["path"])
            t = os.path.join(dest, m["path"])
            os.makedirs(os.path.dirname(t), exist_ok=True)
            shutil.copyfile(s, t)
        res = verify(dest)
    else:
        raise SystemExit("mode")
    os.makedirs(os.path.dirname(receipt), exist_ok=True)
    with open(receipt, "w", encoding="utf-8") as fh:
        json.dump(res, fh, indent=1, sort_keys=True)
        fh.write("\n")
    print(json.dumps({k: v for k, v in res.items() if not k.endswith("Paths")}, sort_keys=True))


if __name__ == "__main__":
    main()
