"""source42.v1 setup: preserve own history (read-only), then port own helper code from source41.v1.

1. Hash manifest of EVERY file of the completed source41.v1 output tree (read-only) and a copy of every non-store file (reports, logs,
   checkpoints, notes, helper code, review, preserved sub-histories) into output/preserved/source41-v1/, so source41 and earlier failures and
   final claims stay available here. *.store.json files are covered by the manifest hashes only (exact bytes remain in that runtime).
2. Port every *.py of source41.v1 output/{ref,builders,tools,vectors} into this runtime, rebinding only the source41.v1 runtime root to this
   runtime root (output/port-manifest.json).
No Run store is seeded: every current-source claim is rebuilt and re-executed against the source42 kit.
Refuses to run twice.  Usage: python3 output/port_and_preserve.py
"""
import hashlib
import json
import os
import shutil
import sys

S41 = "/private/tmp/opensip-design-corrections/consumer-b.v24-source41.v1"
S41_ALT = "/tmp/opensip-design-corrections/consumer-b.v24-source41.v1"
S42 = "/private/tmp/opensip-design-corrections/consumer-b.v24-source42.v1"
OUT = S42 + "/output"


def sha(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if os.path.exists(OUT + "/port-manifest.json"):
        print("already ported; refusing to run twice")
        return 1
    dst = OUT + "/preserved/source41-v1"
    rows, copied = [], 0
    for d, _, fs in sorted(os.walk(S41 + "/output")):
        for f in sorted(fs):
            p = os.path.join(d, f)
            rel = os.path.relpath(p, S41 + "/output")
            digest = sha(p)
            rows.append({"path": rel, "bytes": os.path.getsize(p), "sha256": digest})
            if rel.endswith(".store.json"):
                continue
            t = f"{dst}/{rel}"
            os.makedirs(os.path.dirname(t), exist_ok=True)
            shutil.copyfile(p, t)
            if sha(t) != digest:
                raise SystemExit(f"copy mismatch {rel}")
            copied += 1
    with open(dst + "/manifest.json", "w") as fh:
        json.dump({"standing": "completed source41.v1 output of origin 9d3dfb70-b2d3-498c-a3c1-f8de9e488514 (verdict ACCEPT-RECONSTRUCTABLE on the "
                               "source41 kit, root admission unobserved); read-only own history, not source42 conformance. Non-store files copied "
                               "here; stores hashed only.", "source": S41 + "/output", "files": rows, "copiedNonStoreFiles": copied}, fh, indent=1)
    ported = []
    for sub in ("ref", "builders", "tools", "vectors"):
        for name in sorted(os.listdir(f"{S41}/output/{sub}")):
            if not name.endswith(".py"):
                continue
            rel = f"{sub}/{name}"
            raw = open(f"{S41}/output/{rel}", "rb").read()
            text = raw.decode("utf-8")
            n = text.count(S41) + text.count(S41_ALT)
            new = text.replace(S41, S42).replace(S41_ALT, S42)
            os.makedirs(f"{OUT}/{sub}", exist_ok=True)
            with open(f"{OUT}/{rel}", "w") as fh:
                fh.write(new)
            ported.append({"file": rel, "sourceSha256": hashlib.sha256(raw).hexdigest(), "portedSha256": hashlib.sha256(new.encode()).hexdigest(),
                           "rebound": n})
    with open(OUT + "/port-manifest.json", "w") as fh:
        json.dump({"standing": "own source41.v1 helper code rebound to source42.v1 by root path only; a starting point checked against the source42 "
                               "kit; any later change is a numbered helper correction with the original failure preserved", "files": ported}, fh, indent=1)
    print(json.dumps({"source41Files": len(rows), "copiedNonStore": copied, "ported": len(ported)}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
