#!/usr/bin/env python
"""Exact v16 -> v17 manifest delta, plus verification of the six declared
reference-check source pins against the frozen v17 bytes.

Pins are verified BEFORE any execution. No repinning is ever performed.
"""
import hashlib
import json
import os
import sys

REV = "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews"
V16 = os.path.join(REV, "candidate-subject.v16.json")
V17 = os.path.join(REV, "candidate-subject.v17.json")


def load(p):
    with open(p, "rb") as fh:
        raw = fh.read()
    return hashlib.sha256(raw).hexdigest(), json.loads(raw)


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


def main():
    out = sys.argv[1]
    s16, m16 = load(V16)
    s17, m17 = load(V17)
    root17 = m17["snapshotRoot"]

    a = {f["path"]: f for f in m16["files"]}
    b = {f["path"]: f for f in m17["files"]}

    added = sorted(set(b) - set(a))
    removed = sorted(set(a) - set(b))
    changed = sorted(
        p for p in (set(a) & set(b)) if a[p]["sha256"] != b[p]["sha256"]
    )

    rep = {
        "v16ManifestSha256": s16,
        "v17ManifestSha256": s17,
        "v17DeclaredPredecessor": m17.get("predecessorManifestSha256"),
        "predecessorChainOk": m17.get("predecessorManifestSha256") == s16,
        "v16FileCount": m16["fileCount"],
        "v17FileCount": m17["fileCount"],
        "v16TotalBytes": m16["totalBytes"],
        "v17TotalBytes": m17["totalBytes"],
        "addedCount": len(added),
        "removedCount": len(removed),
        "changedCount": len(changed),
        "removed": removed,
        "changed": [
            {
                "path": p,
                "v16Sha256": a[p]["sha256"],
                "v17Sha256": b[p]["sha256"],
                "v16Bytes": a[p]["bytes"],
                "v17Bytes": b[p]["bytes"],
                "byteDelta": b[p]["bytes"] - a[p]["bytes"],
            }
            for p in changed
        ],
        "added": [{"path": p, "bytes": b[p]["bytes"]} for p in added],
    }

    # Non-review-scaffolding delta: changes outside reviews/ transcripts
    def is_scaffold(p):
        return "/reviews/" in p or p.endswith("tool-calls.json")

    rep["changedNonScaffold"] = [c for c in rep["changed"] if not is_scaffold(c["path"])]
    rep["addedNonScaffold"] = [c for c in rep["added"] if not is_scaffold(c["path"])]
    rep["changedNonScaffoldCount"] = len(rep["changedNonScaffold"])
    rep["addedNonScaffoldCount"] = len(rep["addedNonScaffold"])

    # --- Source pin verification for the six reference-check commands ---
    rc_rel = ("docs/coop/design-corrections/reviews/codex-post-reset.v1/"
              "final-reference.v17/reference-checks.json")
    with open(os.path.join(root17, rc_rel), "rb") as fh:
        rc = json.loads(fh.read())

    pins = []
    for cmd in rc["commands"]:
        src = cmd["source"]
        full = os.path.join(root17, src)
        exists = os.path.isfile(full)
        actual = sha_file(full) if exists else None
        manifest_sha = b.get(src, {}).get("sha256")
        pins.append(
            {
                "name": cmd["name"],
                "source": src,
                "declaredPinSha256": cmd["sourceSha256"],
                "actualFrozenSha256": actual,
                "manifestSha256": manifest_sha,
                "existsInSubject": exists,
                "pinMatchesFrozenBytes": actual == cmd["sourceSha256"],
                "pinMatchesManifest": manifest_sha == cmd["sourceSha256"],
                "declaredExitCode": cmd["exitCode"],
                "changedSinceV16": src in set(changed),
                "addedSinceV16": src in set(added),
            }
        )
    rep["referenceCheckPins"] = pins
    rep["allPinsVerifiedBeforeExecution"] = all(
        p["pinMatchesFrozenBytes"] and p["pinMatchesManifest"] for p in pins
    )
    rep["commandCount"] = len(pins)

    with open(out, "w") as fh:
        json.dump(rep, fh, indent=1, sort_keys=True)

    summary = {k: v for k, v in rep.items()
               if k not in ("changed", "added", "removed",
                            "changedNonScaffold", "addedNonScaffold",
                            "referenceCheckPins")}
    print(json.dumps(summary, indent=1, sort_keys=True))
    print("\n--- PINS ---")
    for p in pins:
        print(p["name"], p["pinMatchesFrozenBytes"], p["pinMatchesManifest"],
              "changed16to17=" + str(p["changedSinceV16"]),
              "added=" + str(p["addedSinceV16"]))
    print("\n--- NON-SCAFFOLD CHANGED (%d) ---" % rep["changedNonScaffoldCount"])
    for c in rep["changedNonScaffold"]:
        print(" %+7d  %s" % (c["byteDelta"], c["path"]))
    print("\n--- NON-SCAFFOLD ADDED (%d) ---" % rep["addedNonScaffoldCount"])
    for c in rep["addedNonScaffold"][:80]:
        print(" %8d  %s" % (c["bytes"], c["path"]))
    print("\n--- REMOVED (%d) ---" % len(removed))
    for p in removed[:80]:
        print("  " + p)


if __name__ == "__main__":
    main()
