"""Reviewer probe: dependency-source representability on the Rust3 wire.

(1) Owner DependencyFileManifestV1 / DependencySourceManifestV3 path schema vs candidate canonical-path-segments.
(2) Owner file_manifest_identity accepts such paths (no segment check).
(3) Encoded DependencySourceManifest length vs maxFramePayloadBytes at owner-admissible entry counts.
(4) packageKey/set constraints behaviour incl. empty sourceId, spaces in sourceId, DEL/C1 in name, NFC.
"""
import importlib.util, json, sys, unicodedata
from pathlib import Path

COPY = Path(__file__).resolve().parent / "copy"
ARCH = Path("/Users/sb/code/opensip-ai/opensip_arch")
sys.path.insert(0, str(COPY / "tools"))
import wirecodec as W  # noqa: E402
import admission_ref as AR  # noqa: E402
from jsonschema import Draft202012Validator  # noqa: E402

doc = json.loads((COPY / "wire-carriers.v1.json").read_text())
ev = json.loads((ARCH / "docs/coop/design-corrections/native/native-evidence.schemas.v2.json").read_text())
spec = importlib.util.spec_from_file_location("ne", ARCH / "docs/coop/design-corrections/native/native_evidence_model.v2.py")
NE = importlib.util.module_from_spec(spec); spec.loader.exec_module(NE)
out = {}

fm = dict(ev); fm = {"$schema": ev.get("$schema"), "$defs": ev["$defs"], "$ref": "#/$defs/DependencyFileManifestV1"}
V = Draft202012Validator(fm)
paths = ["C:x", "c:/lib.rs", "a//b", "a/", "src/lib.rs", "a:b/c", "Z:"]
rows = {}
for p in paths:
    owner_ok = V.is_valid([{"path": p, "contentSha256": "0" * 64, "byteLength": 0}])
    try:
        W.lexical("canonical-path-segments", p); wire_ok = True
    except W.Refuse:
        wire_ok = False
    try:
        NE.file_manifest_identity({p: {"sha256": "0" * 64, "byteLength": 0}}); ident_ok = True
    except Exception as e:  # noqa: BLE001
        ident_ok = repr(e)[:80]
    rows[p] = {"ownerSchemaAdmits": owner_ok, "ownerIdentityMints": ident_ok, "candidateWireAdmits": wire_ok}
out["pathDomain"] = rows

limits = {"maxFramePayloadBytes": 67108864, "maxDependencySourceEntries": 1000000}
def manifest(n, key, path_len):
    e = {"packageKey": key, "path": "p" * path_len, "byteLength": 0, "contentSha256": "0" * 64}
    per = W.encoded_length(e)
    head = W.encoded_length({"dependencySourceSetId": "sha256:" + "0" * 64, "manifestSha256": "0" * 64, "entries": []}) + 4
    return head + per * n, per
realistic_key = "serde 1.0.200 registry+https://github.com/rust-lang/crates.io-index"
for label, key, pl in [("minimal", "a 1 ", 1), ("realistic", realistic_key, 24)]:
    total, per = manifest(1000000, key, pl)
    out.setdefault("frameCapacity", {})[label] = {"entryBytes": per, "bytesAt1e6Entries": total,
                                                  "exceedsFrame": total > limits["maxFramePayloadBytes"],
                                                  "maxEntriesThatFit": (limits["maxFramePayloadBytes"] - 100) // per}
# does any candidate rule refuse the oversized dependency manifest before spawn?
out["candidateDepsrcRefusalRules"] = [r["id"] for r in doc["admission"] if "DEPSRC" in r["id"] or "DEPENDENCY" in r["id"]]
out["depsrcRulesMentionFramePayload"] = [r["id"] for r in doc["admission"] if ("DEPSRC" in r["id"]) and "maxFramePayloadBytes" in json.dumps(r)]
out["anyRuleMentionsRequestTotals"] = [r["id"] for r in doc["admission"] if "maxRequestPayloadBytesTotal" in json.dumps(r) or "maxRequestFrames" in json.dumps(r)]

def pk(name, version, source):
    return {"name": name, "version": version, "sourceId": source}
cases = {"emptySource": pk("a", "1", ""), "spaceInSource": pk("my-proj", "0.1.0", "path+file:///my proj"),
         "spaceInName": pk("a b", "1", ""), "tabInVersion": pk("a", "1\t", ""), "delInName": pk("a\x7f", "1", ""),
         "c1InName": pk("a\x85", "1", ""), "key4096": pk("a" * 256, "1" * 256, "s" * (4096 - 514)),
         "key4097": pk("a" * 256, "1" * 256, "s" * (4097 - 514)), "nonNfcSource": pk("a", "1", "e\u0301")}
res = {}
for n, row in cases.items():
    try:
        AR.depsrc_set_key_constraints(doc, [row]); c = "admitted"
    except AR.Refuse as e:
        c = str(e)
    key = AR.constructed_key(doc, row)
    try:
        W.Carriers(doc, lambda *a: None).check(doc["scalars"]["Rust3PackageKey"]["type"], key, "k"); wire = True
    except W.Refuse as e:
        wire = str(e)
    res[n] = {"setConstraint": c, "wireKey": wire, "keyScalars": len(key)}
out["packageKey"] = res
# order equivalence (tuple vs key bytes) under constraint, randomized
import random
random.seed(7)
alpha = ["a", "b", "-", "!", "\x7f", "é", "0", "~"]
bad = 0
for _ in range(20000):
    rs = [pk("".join(random.choices(alpha, k=random.randint(1, 3))), "".join(random.choices(alpha, k=random.randint(1, 2))),
             "".join(random.choices(alpha + [" ", ""], k=random.randint(0, 3)))) for _ in range(2)]
    t = [tuple(x[k].encode() for k in ("name", "version", "sourceId")) for x in rs]
    kk = [AR.constructed_key(doc, x).encode() for x in rs]
    if (t[0] < t[1]) != (kk[0] < kk[1]) or (t[0] == t[1]) != (kk[0] == kk[1]):
        bad += 1
out["tupleVsKeyOrderDisagreements"] = bad
print(json.dumps(out, indent=1, ensure_ascii=True))
