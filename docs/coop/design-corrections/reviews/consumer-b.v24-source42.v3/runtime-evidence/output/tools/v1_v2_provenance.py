"""Provenance of every re-executed JSON artifact against its preserved source39.v1 counterpart (source39.v2).

For each JSON file under output/{vectors,envelopes,traces,runs} that exists both here and in preserved/source39-v1/, compare the parsed
documents after removing volatile process fields (pid, seconds, receipt, storeFile, freshProcess, modulesLoadedFrom, stderr tails, log
paths). Result per file: equal | different (first differing JSON path) | v2-only | v1-only. Equality is claimed only for files compared
here against the same kit (identical manifest rows, vectors/phase0-custody.json); it asserts nothing about correctness by itself.
Writes selfcheck/v1-v2-provenance.json.  Usage: python3 tools/v1_v2_provenance.py
"""
import glob
import json
import os
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source42.v3/output"
V1 = OUT + "/preserved/source39-v1"
VOLATILE = {"pid", "seconds", "receipt", "storeFile", "freshProcess", "modulesLoadedFrom", "stderr", "stderrTail", "tail", "log", "buildLog",
            "replayLog", "command"}


def scrub(x):
    if isinstance(x, dict):
        return {k: scrub(v) for k, v in x.items() if k not in VOLATILE}
    if isinstance(x, list):
        return [scrub(v) for v in x]
    if isinstance(x, str):
        return x.replace("consumer-b.v24-source39.v1", "<runtime>").replace("consumer-b.v24-source39.v2", "<runtime>").replace("consumer-b.v24-source39.v3", "<runtime>")
    return x


def first_diff(a, b, path="$"):
    if type(a) is not type(b):
        return path
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                return f"{path}.{k}"
            d = first_diff(a[k], b[k], f"{path}.{k}")
            if d:
                return d
        return None
    if isinstance(a, list):
        if len(a) != len(b):
            return f"{path}[len {len(a)}!={len(b)}]"
        for i, (x, y) in enumerate(zip(a, b)):
            d = first_diff(x, y, f"{path}[{i}]")
            if d:
                return d
        return None
    return None if a == b else path


def main():
    rows = []
    rels = set()
    for sub in ("vectors", "envelopes", "traces", "runs"):
        for base in (OUT, V1):
            for p in glob.glob(f"{base}/{sub}/*.json"):
                rels.add(os.path.relpath(p, base))
    for rel in sorted(rels):
        a, b = f"{V1}/{rel}", f"{OUT}/{rel}"
        if rel.endswith(".store.json"):
            kind = "store"
        else:
            kind = "report"
        if not os.path.exists(b):
            rows.append({"file": rel, "kind": kind, "status": "v1-only"})
            continue
        if not os.path.exists(a):
            rows.append({"file": rel, "kind": kind, "status": "v2-only"})
            continue
        if kind == "store":
            ea, eb = json.load(open(a)), json.load(open(b))
            same = ea["blobs"] == eb["blobs"] and ea.get("runId") == eb.get("runId")
            rows.append({"file": rel, "kind": kind, "status": "equal" if same else "different", "runIdEqual": ea.get("runId") == eb.get("runId"),
                         "blobsAdded": len(set(eb["blobs"]) - set(ea["blobs"])), "blobsRemoved": len(set(ea["blobs"]) - set(eb["blobs"]))})
            continue
        da, db = scrub(json.load(open(a))), scrub(json.load(open(b)))
        d = first_diff(da, db)
        rows.append({"file": rel, "kind": kind, "status": "equal" if d is None else "different", "firstDifference": d})
    counts = {}
    for r in rows:
        counts[f"{r['kind']}:{r['status']}"] = counts.get(f"{r['kind']}:{r['status']}", 0) + 1
    doc = {"standing": "structural provenance only; equal means the re-executed v2 bytes reproduce v1's recorded document after removing process fields",
           "counts": counts, "rows": rows}
    os.makedirs(OUT + "/selfcheck", exist_ok=True)
    json.dump(doc, open(OUT + "/selfcheck/v1-v2-provenance.json", "w"), indent=1, sort_keys=True)
    print(json.dumps(counts, indent=1))
    for r in rows:
        if r["status"] == "different":
            print(r["file"], r.get("firstDifference") or (r.get("runIdEqual"), r.get("blobsAdded"), r.get("blobsRemoved")))
    return 0


if __name__ == "__main__":
    sys.exit(main())
