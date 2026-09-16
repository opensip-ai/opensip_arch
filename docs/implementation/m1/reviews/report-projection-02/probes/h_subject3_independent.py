"""Independent subject3 frame: stdlib hashlib + json only (no subject or reference module)."""
import hashlib, json, struct
SUBJ = "/tmp/opensip-implementation/m1-report-projection-review-02/work/augmented-copy/fixtures.json"
fx = json.load(open(SUBJ))
def C(x): return json.dumps(x, ensure_ascii=False, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()
def sid(endpoint):
    X = C(dict({"schemaVersion": 3}, **endpoint)); D = b"evaluation-subject"
    return "subject3:" + hashlib.sha256(b"opensip.product.v1\x00" + D + b"\x00" + struct.pack(">Q", len(X)) + X).hexdigest()
out = {"goldens": [sid(r["endpoint"]) == r["subjectId"] for r in fx["subjectGoldens"]["positive"]]}
audit = fx["bases"]["audit-full"]
rows = audit["panels"]["graph"]["data"]["subjectIndex"]
out["indexRowsRecomputed"] = sum(sid(r["endpoint"]) == r["subjectId"] for r in rows)
out["indexRows"] = len(rows)
out["indexSortedStrict"] = all(rows[i]["subjectId"].encode() < rows[i + 1]["subjectId"].encode() for i in range(len(rows) - 1))
fids = {f["subjectId"]: (f["subjectKind"], f["subjectPath"]) for f in audit["envelope"]["findings"]}
out["findingSubjectsJoinedByIndex"] = {s: v for s, v in fids.items() if s in {r["subjectId"] for r in rows}}
out["findingSubjectsNotInIndex"] = {s: v for s, v in fids.items() if s not in {r["subjectId"] for r in rows}}
# path-guess counterexample: a file finding whose subjectPath equals an indexed file nativeSubjectId must NOT join unless subjectIds equal
out["indexedFileNativeIds"] = [r["endpoint"]["nativeSubjectId"] for r in rows if r["endpoint"]["kind"] == "file"]
print(json.dumps(out, indent=1)); json.dump(out, open("h_subject3_independent.json", "w"), indent=1)
