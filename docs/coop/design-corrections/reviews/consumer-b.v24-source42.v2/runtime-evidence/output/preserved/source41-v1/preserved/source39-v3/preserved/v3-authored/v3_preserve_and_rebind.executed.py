"""source39.v3 completion continuation, step 1: preserve the copied v2 output, then rebind own helper paths to this runtime.

1. Hash manifest of EVERY file of output/ as copied at v3 start, each compared byte-for-byte (SHA-256) with the same path in the
   read-only v2 runtime -> output/preserved/v2-copied-output.manifest.json. Nothing in the v2 runtime is written.
2. Copy of every non-store file outside preserved/ (reports, logs, checkpoints, notes, helper code, negatives reports, selfcheck)
   -> output/preserved/v2-copied-state/<rel>, so any v3 step that rewrites a report leaves the v2-measured bytes in place. Store
   files (*.store.json) are not rewritten by any v3 step and stay covered by the manifest hashes.
3. Rebind the v2 runtime root to the v3 runtime root in every helper *.py under output/{ref,tools,builders,vectors} and
   output/preserved/pre-hc33/{ref,tools} (the pre-correction code copy that negatives run under). Runtime LABELS inside helper text
   are not touched here; they are edited deliberately afterwards. -> output/port-manifest-v3.json (before/after SHA-256, count).
Refuses to run twice.  Usage: python3 tools/v3_preserve_and_rebind.py
"""
import hashlib
import json
import os
import shutil
import sys

V2 = "/private/tmp/opensip-design-corrections/consumer-b.v24-source39.v2"
V2_ALT = "/tmp/opensip-design-corrections/consumer-b.v24-source39.v2"
V3 = "/private/tmp/opensip-design-corrections/consumer-b.v24-source39.v3"
OUT = V3 + "/output"


def sha(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    if os.path.exists(OUT + "/port-manifest-v3.json"):
        print("already rebound; refusing to run twice")
        return 1
    rows, mismatched = [], []
    for d, _, fs in sorted(os.walk(OUT)):
        for f in sorted(fs):
            p = os.path.join(d, f)
            rel = os.path.relpath(p, OUT)
            a = sha(p)
            v2p = f"{V2}/output/{rel}"
            b = sha(v2p) if os.path.exists(v2p) else None
            rows.append({"path": rel, "bytes": os.path.getsize(p), "sha256": a, "equalToV2Runtime": a == b})
            if a != b:
                mismatched.append(rel)
    json.dump({"standing": "output/ as copied into runtime source39.v3 at start, compared with the v2 runtime (read-only); v2-measured work, not v3 execution",
               "files": len(rows), "allEqualToV2Runtime": not mismatched, "mismatched": mismatched, "rows": rows},
              open(OUT + "/preserved/v2-copied-output.manifest.json", "w"), indent=1)
    copied = 0
    for r in rows:
        rel = r["path"]
        if rel.startswith("preserved/") or rel.endswith(".store.json"):
            continue
        dst = f"{OUT}/preserved/v2-copied-state/{rel}"
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(f"{OUT}/{rel}", dst)
        copied += 1
    ported = []
    targets = []
    for sub in ("ref", "tools", "builders", "vectors", "preserved/pre-hc33/ref", "preserved/pre-hc33/tools"):
        for name in sorted(os.listdir(f"{OUT}/{sub}")):
            if name.endswith(".py"):
                targets.append(f"{sub}/{name}")
    for rel in targets:
        p = f"{OUT}/{rel}"
        raw = open(p, "rb").read()
        text = raw.decode("utf-8")
        n = text.count(V2) + text.count(V2_ALT)
        if not n:
            continue
        new = text.replace(V2, V3).replace(V2_ALT, V3)
        open(p, "w").write(new)
        ported.append({"file": rel, "beforeSha256": hashlib.sha256(raw).hexdigest(), "afterSha256": hashlib.sha256(new.encode()).hexdigest(),
                       "rebound": n, "beforeCopy": f"preserved/v2-copied-state/{rel}" if not rel.startswith("preserved/") else "v2 runtime (read-only) + manifest"})
    json.dump({"standing": "own helper code rebound from runtime source39.v2 to source39.v3 by root path only; label edits are separate and listed in notes/12-v3-completion.md",
               "files": ported}, open(OUT + "/port-manifest-v3.json", "w"), indent=1)
    print(json.dumps({"manifestFiles": len(rows), "mismatched": len(mismatched), "copiedReports": copied, "rebound": len(ported)}))
    return 0 if not mismatched else 1


if __name__ == "__main__":
    sys.exit(main())
