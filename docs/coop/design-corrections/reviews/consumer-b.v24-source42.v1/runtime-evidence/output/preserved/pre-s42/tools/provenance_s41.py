"""Provenance of every re-executed JSON artifact of this runtime (source41).

For each JSON file under output/{vectors,envelopes,traces,runs} it compares, after removing volatile process fields:
  (a) against preserved/s41-original-state: the same file as produced by the UNCHANGED ported helpers over the same source41 kit.
      Shows what the source41 helper corrections changed. Result: equal | different (first differing JSON path) | current-only | original-only.
  (b) against preserved/source39-v3: my own completed source39 counterpart (non-store files only; stores are compared by file SHA-256 from
      that runtime's manifest). ORIENTATION ONLY; a source39 result never establishes source41 conformance.
Writes selfcheck/s41-provenance.json.  Usage: python3 tools/seq.py <label> tools/provenance_s41.py
"""
import glob
import hashlib
import json
import os
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source42.v1/output/preserved/pre-s42"
ORIG = OUT + "/preserved/s41-original-state"
S39 = OUT + "/preserved/source39-v3"
VOLATILE = {"pid", "seconds", "receipt", "storeFile", "freshProcess", "modulesLoadedFrom", "stderr", "stderrTail", "tail", "log", "buildLog",
            "replayLog", "command"}


def scrub(x):
    if isinstance(x, dict):
        return {k: scrub(v) for k, v in x.items() if k not in VOLATILE}
    if isinstance(x, list):
        return [scrub(v) for v in x]
    if isinstance(x, str):
        for name in ("consumer-b.v24-source41.v1", "consumer-b.v24-source39.v1", "consumer-b.v24-source39.v2", "consumer-b.v24-source39.v3"):
            x = x.replace(name, "<runtime>")
        return x
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


def compare(rel, base, cur_label, base_label):
    a, b = f"{base}/{rel}", f"{OUT}/{rel}"
    if not os.path.exists(b):
        return {"status": f"{base_label}-only"}
    if not os.path.exists(a):
        return {"status": f"{cur_label}-only"}
    if rel.endswith(".store.json"):
        ea, eb = json.load(open(a)), json.load(open(b))
        same = ea["blobs"] == eb["blobs"] and ea.get("runId") == eb.get("runId")
        return {"status": "equal" if same else "different", "runIdEqual": ea.get("runId") == eb.get("runId"),
                "blobsAdded": len(set(eb["blobs"]) - set(ea["blobs"])), "blobsRemoved": len(set(ea["blobs"]) - set(eb["blobs"]))}
    d = first_diff(scrub(json.load(open(a))), scrub(json.load(open(b))))
    return {"status": "equal" if d is None else "different", "firstDifference": d}


def main():
    s39_manifest = {r["path"]: r["sha256"] for r in json.load(open(S39 + "/manifest.json"))["files"]}
    rels = set()
    for sub in ("vectors", "envelopes", "traces", "runs"):
        for base in (OUT, ORIG, S39):
            rels |= {os.path.relpath(p, base) for p in glob.glob(f"{base}/{sub}/*.json")}
        rels |= {p for p in s39_manifest if p.startswith(f"{sub}/") and p.endswith(".json") and "/" not in p[len(sub) + 1:]}
    rows = []
    for rel in sorted(rels):
        kind = "store" if rel.endswith(".store.json") else "report"
        row = {"file": rel, "kind": kind, "vsUnchangedHelpersSource41": compare(rel, ORIG, "current", "original")}
        if kind == "store":
            cur = f"{OUT}/{rel}"
            if rel not in s39_manifest:
                row["vsSource39v3"] = {"status": "current-only" if os.path.exists(cur) else "absent"}
            elif not os.path.exists(cur):
                row["vsSource39v3"] = {"status": "source39-only"}
            else:
                row["vsSource39v3"] = {"status": "file-sha-equal" if hashlib.sha256(open(cur, "rb").read()).hexdigest() == s39_manifest[rel] else "file-sha-different"}
        else:
            row["vsSource39v3"] = compare(rel, S39, "current", "source39")
        rows.append(row)
    counts = {}
    for r in rows:
        for col in ("vsUnchangedHelpersSource41", "vsSource39v3"):
            k = f"{col}:{r['kind']}:{r[col]['status']}"
            counts[k] = counts.get(k, 0) + 1
    doc = {"standing": "structural provenance only; 'equal' reproduces a recorded document after removing process fields and asserts nothing "
                       "about correctness; the source39 column is orientation and never current-source conformance",
           "counts": counts, "rows": rows}
    os.makedirs(OUT + "/selfcheck", exist_ok=True)
    json.dump(doc, open(OUT + "/selfcheck/s41-provenance.json", "w"), indent=1, sort_keys=True)
    print(json.dumps(counts, indent=1, sort_keys=True))
    for r in rows:
        if r["vsUnchangedHelpersSource41"]["status"] == "different":
            print("changed-by-correction", r["file"], r["vsUnchangedHelpersSource41"].get("firstDifference") or r["vsUnchangedHelpersSource41"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
