"""Reviewer-05 probes from the 40-input copy (successor installed only on scoped instances by check_reference)."""
import sys, os, json, copy, ast, unicodedata
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); COPY = os.path.join(HERE, "copy")
sys.pycache_prefix = os.path.join(HERE, "tmp", "pycache")
sys.path.insert(0, os.path.join(COPY, "tools"))
from pathlib import Path
from jsonschema import Draft202012Validator
import common as CM, wirecodec as W, representability as REP, admission_ref as AR, sender_ref as SR, owner_successor as OS
from check_static import Static
from check_reference import Reference
arch = CM.arch_root(); st = Static(arch, Path(COPY))
try:
    R = Reference(arch, Path(COPY), st)
except Exception:
    st.run(Draft202012Validator); R = Reference(arch, Path(COPY), st)
NE, NE_S, IM3, IM3_S, fx, doc, K = R.NE, R.NE_S, R.IM3, R.IM3_S, R.fx, R.wire, R.K
LF = "\n"; out = {}
def res(fn):
    try:
        fn(); return "admitted"
    except Exception as e:
        return "refused:" + type(e).__name__ + ":" + str(e)[:70]
# ---- S sender
limits = R.limits("rust-semantic"); acc = AR.params(doc, "REQUEST-WIRE-ACCOUNTING")
vec = next(x for x in st.vectors["vectors"]["REQUEST-WIRE-ACCOUNTING"] if x["id"] == "frames-small-request")["input"]["plan"]
req = REP.build_plan(vec, fx, AR.prepared_entries); plan = REP.plan(doc, limits, vec, fx, AR.prepared_entries)
frames = SR.realize(req, "rust-semantic", limits)
def consume(tr, lim=limits):
    try:
        return "accepted:" + json.dumps(SR.consume(plan, "rust-semantic", acc, lim, tr))
    except W.Refuse as e:
        return "refused:" + str(e.code)
echo = plan["cancelEcho"]; n = len(frames)
full_echo = SR.expected_cancel(plan, n)
def cancel_at(k, payload): return frames[:k] + [SR.cancel_frame(k, payload)]
s = {"cancelEcho": echo, "expectedAtEnd": full_echo}
s["ordinalFalseInsteadOf0"] = consume(cancel_at(n, dict(full_echo, analysisOrdinal=False))) if full_echo["analysisOrdinal"] == 0 else "n/a planned ordinal %r" % full_echo["analysisOrdinal"]
s["ordinalFloat0"] = consume(cancel_at(n, dict(full_echo, analysisOrdinal=0.0))) if full_echo["analysisOrdinal"] == 0 else "n/a"
s["carrierOrdinalFalse"] = res(lambda: K.frame_payload("rust-semantic", "Cancel", dict(full_echo, analysisOrdinal=False)))
ou_idx = echo["openUniverseSlot"]
swapped = copy.deepcopy(frames); p = swapped[ou_idx]["payload"]; old = p["executionId"]; p["executionId"] = old[:-1] + ("0" if old[-1] != "0" else "1")
s["openUniverseExecutionIdSubstitutedSameLength_thenPlannedEchoCancel"] = consume(swapped[:ou_idx + 1] + [SR.cancel_frame(ou_idx + 1, SR.expected_cancel(plan, ou_idx + 1))])
s["openUniverseExecutionIdSubstituted_thenEchoOfWhatWasSent"] = consume(swapped[:ou_idx + 1] + [SR.cancel_frame(ou_idx + 1, dict(SR.expected_cancel(plan, ou_idx + 1), executionId=p["executionId"]))])
sm_idx = next(i for i, f in enumerate(frames) if f["frameType"] == "SnapshotManifest")
sw2 = copy.deepcopy(frames); sw2[sm_idx]["payload"]["manifestSha256"] = "f" * 64
s["snapshotManifestDigestSubstitutedSameLength"] = consume(sw2)
pos = {}
for k in range(0, n + 1):
    pos[k] = {"expected": SR.expected_cancel(plan, k), "accepted": consume(cancel_at(k, SR.expected_cancel(plan, k) or {"executionId": None, "analysisOrdinal": None, "reason": "user-interrupt"}))[:9]}
s["everyPosition"] = pos
out["S_sender"] = s
# ---- P prepared carried vs usable
def pcase(nrows, stale_idx=(), failed_idx=(), explicit=False, blob=None):
    prep, _ = R.prepared_case({"fixture": "prepInert", "rows": nrows})
    for i in stale_idx: prep["rows"][i]["inputBinding"]["toolchainDigest"] = "9" * 64
    for i in failed_idx: prep["rows"][i]["status"] = "failed"
    if blob: prep["rows"][blob[0]]["blob"]["byteLength"] = blob[1]
    try:
        owner = NE_S.prepared_output_set_admit(copy.deepcopy(prep), fx["ctx"], explicit)
    except Exception as e:
        owner = {"outcome": "EXC:" + type(e).__name__ + str(e)[:80]}
    succ = REP.prepared_output_set_admit_successor(NE_S, doc, prep, fx["ctx"], explicit)
    ident = NE_S.prepared_output_set_identity(prep)
    return {"owner": owner.get("outcome"), "ownerUsable": len(owner.get("usableRows", []) or []), "ownerStale": len(owner.get("staleRows", []) or []), "ownerFailed": len(owner.get("failedRows", []) or []),
            "succ": succ.get("outcome"), "succUsable": len(succ.get("usableRows", []) or []), "succStale": len(succ.get("staleRows", []) or []),
            "refusal": (succ.get("successorRefusal") or {}).get("raw"), "disclosure": succ.get("wireLimitDisclosure"), "basis": succ.get("wireLimitBasis"),
            "setIdentityOverAllRows": ident[:20]}
P = {}
P["defaulted_257_1stale"] = pcase(257, [0])
P["defaulted_256_1stale"] = pcase(256, [0])
P["defaulted_300_allStale"] = pcase(300, range(300))
P["explicit_257_1failed"] = pcase(257, (), [0], True)
P["defaulted_257_1failed"] = pcase(257, (), [0], False)
P["defaulted_10_staleRowBlobOver"] = pcase(10, [0], (), False, (0, 1073741825))
P["explicit_10_staleRowBlobOver"] = pcase(10, [0], (), True, (0, 1073741825))
# identity sensitivity: removing a stale row changes the set identity (so stale rows are identity-bearing)
prep, _ = R.prepared_case({"fixture": "prepInert", "rows": 3}); a = NE_S.prepared_output_set_identity(prep); prep2 = copy.deepcopy(prep); prep2["rows"] = prep2["rows"][1:]
P["identityChangesWhenRowDropped"] = a != NE_S.prepared_output_set_identity(prep2)
out["P_prepared"] = P
# ---- scope: actual consumers pinned vs scoped
sc = {}
def ne_found(mod, v):
    fn = next(getattr(mod, k) for k in dir(mod) if callable(getattr(mod, k)) and getattr(getattr(mod, k), "__code__", None) is not None and "_FOUNDATION_SCHEMAS" in getattr(mod, k).__code__.co_names)
    return fn.__name__, (lambda: fn("LogicalPath", v))
for v in ["a/b", "a/.." + LF, "x" + LF + "/../y", "0" * 64 + LF]:
    row = {}
    row["IM3.validate_registered_record identity v3 LogicalPath"] = [res(lambda m=m: m.validate_registered_record("foundation/identity-schemas.v3.json", "#/$defs/LogicalPath", v)) for m in (IM3, IM3_S)]
    row["IM3.validate_registered_record identity v2 LogicalPath"] = [res(lambda m=m: m.validate_registered_record("foundation/identity-schemas.v2.json", "#/$defs/LogicalPath", v)) for m in (IM3, IM3_S)]
    row["NE.validate_workflow common LogicalPath"] = [res(lambda m=m: m.validate_workflow("workflows/schemas/common.schema.json", "#/$defs/LogicalPath", v)) for m in (NE, NE_S)]
    try:
        name, f0 = ne_found(NE, v); _, f1 = ne_found(NE_S, v)
        row["NE." + name + " identity v2 LogicalPath"] = [res(f0), res(f1)]
    except StopIteration:
        pass
    row["NE.IM.validate_registered_record identity v2 LogicalPath"] = [res(lambda m=m: m.IM.validate_registered_record("foundation/identity-schemas.v2.json", "#/$defs/LogicalPath", v)) if hasattr(m.IM, "validate_registered_record") else "n/a" for m in (NE, NE_S)]
    sc[json.dumps(v)] = row
out["scopeNoChangeConsumers"] = sc
# relation sites via IM3 pinned/scoped, and whole FilePayloadV1 record
rel = {}
for v in ["src/a.rs", "a" + LF + "b.rs", "a/.." + LF, "x" + LF + "/../y.rs"]:
    rel[json.dumps(v)] = [res(lambda m=m: m.validate_registered_record("foundation/relation-payload-schemas.v2.json", "#/$defs/CanonicalPath", v)) for m in (IM3, IM3_S)]
out["relationCanonicalPath_pinned_scoped"] = rel
# fact-plane _is_path (ast-extracted, executed without importing the checker)
src = open(os.path.join(arch, CM.ARCH_PINS["checkFactPlane"][0])).read(); tree = ast.parse(src)
ns = {"unicodedata": unicodedata}
for node in tree.body:
    if isinstance(node, ast.FunctionDef) and node.name in ("_is_nfc_text", "_is_path"):
        exec(compile(ast.Module([node], []), "fp", "exec"), ns)
out["factPlane_is_path"] = {json.dumps(v): ns["_is_path"](v) for v in ["src/a.rs", "a" + LF + "b.rs", "a/.." + LF, "x" + LF + "/../y.rs", "a" + chr(0x7f) + "b"]}
out["carrierSnapshotPath_a_LF_b"] = res(lambda: W.lexical(doc["privateRepresentation"]["lexicalRules"], "canonical-path-segments", "a" + LF + "b.rs", "u"))
# ---- mark walk: NODE_MARK must be absent outside scoped documents
def count_marks(o, seen):
    if id(o) in seen: return 0
    seen.add(id(o)); c = 0
    if isinstance(o, dict):
        c += 1 if o.get(OS.NODE_MARK) is True else 0
        for v in o.values(): c += count_marks(v, seen)
    elif isinstance(o, list):
        for v in o: c += count_marks(v, seen)
    return c
mw = {}
for label, mod in (("NE_S", NE_S), ("ST_S", R.ST_S), ("WI_S", R.WI_S), ("IM3_S", IM3_S), ("NE_S.IM", NE_S.IM), ("NE_S.STARTUP", NE_S.STARTUP), ("NE_S.WIRE", NE_S.WIRE)):
    for k, v in vars(mod).items():
        if isinstance(v, (dict, tuple, list)) and not k.startswith("__"):
            c = count_marks(v, set())
            if c: mw[label + "." + k] = c
    mw[label + ".C_is_scoped"] = isinstance(getattr(mod, "C", None), OS.ScopedCanonical)
out["nodeMarks"] = mw
json.dump(out, open(os.path.join(HERE, "probe_05.out.json"), "w"), indent=1, ensure_ascii=True, default=str)
print(json.dumps(out, indent=1, ensure_ascii=True, default=str)[:14000])
