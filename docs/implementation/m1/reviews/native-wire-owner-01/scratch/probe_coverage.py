"""Independent comparison of field-coverage.json against the prior TS2/Rust3 translation inventories and gap lists,
and of every coverage target against the actual carrier input."""
import json, re, sys
B = "/tmp/opensip-implementation/"
fc = json.load(open(B + "m1-native-wire-owner-subject-01/field-coverage.json"))
idl = json.load(open(B + "m1-native-wire-owner-subject-01/wire-carriers.v1.json"))
ts = json.load(open(B + "m1-typescript-wire-translation-01/fields.json"))
rs = json.load(open(B + "m1-rust-wire-translation-01/fields.json"))
out = {}


def ids_of(coll):
    if isinstance(coll, dict):
        return list(coll.keys())
    res = []
    for r in coll:
        res.append(r.get("id") or r.get("rowId") or r.get("key") or json.dumps(r, sort_keys=True)[:80])
    return res


out["fcCounts"] = fc["counts"]
out["fcTotals"] = fc["totals"]
sample = {p: fc["rows"][p][:1] if isinstance(fc["rows"][p], list) else list(fc["rows"][p].items())[:1] for p in fc["rows"]}
out["fcSample"] = sample
out["tsRowSample"] = ts["rows"][:1]
out["tsNewRowSample"] = ts["newRows"][:1]
out["tsGaps"] = list(ts["gaps"].keys())
out["rsGaps"] = list(rs["gaps"].keys())
out["rsRowSample"] = list(rs["rows"].items())[:1]
out["rsFramesSample"] = list(rs["frames"].items())[:1]
out["rsEnvelope"] = rs["envelope"]
json.dump(out, sys.stdout, indent=1, ensure_ascii=False, default=str)
