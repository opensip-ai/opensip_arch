"""Reviewer probes (candidate 04), run from the 39-input copy with the owner pattern successor installed:
S  reference sender: Cancel position/payload law vs HOST-SEND-SCHEDULE and P3 START;
P  prepared: defaulted-mode stale + over-limit set (owner fallback bypasses the wire-limit selector?), planner/carrier
   consequence for >256 prepared entries; precedence of phase A path refusal;
R  relation-payload CanonicalPath (not in the successor rows) under the installed ECMA evaluator."""
import sys, os, json, copy
sys.dont_write_bytecode = True
HERE = os.path.dirname(os.path.abspath(__file__)); COPY = os.path.join(HERE, "copy")
sys.pycache_prefix = os.path.join(HERE, "tmp", "pycache")
sys.path.insert(0, os.path.join(COPY, "tools"))
from pathlib import Path
from jsonschema import Draft202012Validator
import common as CM, wirecodec as W, representability as REP, admission_ref as AR, sender_ref as SR, owner_successor as OS
from check_static import Static
from check_reference import Reference

arch = CM.arch_root()
st = Static(arch, Path(COPY))
try:
    R = Reference(arch, Path(COPY), st)
except Exception:  # noqa: BLE001
    st.run(Draft202012Validator)
    R = Reference(arch, Path(COPY), st)
NE, K, fx, doc = R.NE_S, R.K, R.fx, R.wire
NE_PINNED = R.NE
out = {"successorInstalledOnNE_S": bool(getattr(NE, OS.MARK, False)), "pinnedNEInstalled": bool(getattr(NE_PINNED, OS.MARK, False))}
LF = "\n"


def carrier(ft, payload):
    try:
        K.frame_payload("rust-semantic", ft, payload)
        return "admitted"
    except W.Refuse as e:
        return "refused:" + str(e.code)
    except Exception as e:  # noqa: BLE001
        return "EXC:" + type(e).__name__ + ":" + str(e)[:120]


# ---------------- S: sender Cancel law
limits = R.limits("rust-semantic")
acc_p = AR.params(doc, "REQUEST-WIRE-ACCOUNTING")
vec = next(x for x in st.vectors["vectors"]["REQUEST-WIRE-ACCOUNTING"] if x["id"] == "frames-small-request")["input"]["plan"]
req = REP.build_plan(vec, fx, AR.prepared_entries)
plan = REP.plan(doc, limits, vec, fx, AR.prepared_entries)
frames = SR.realize(req, "rust-semantic", limits)


def consume(tr):
    try:
        r = SR.consume(plan, "rust-semantic", acc_p, limits, tr)
        return "accepted:" + json.dumps(r)
    except W.Refuse as e:
        return "refused:" + str(e.code)


def cancel(seq, **over):
    f = SR.cancel_frame(req, seq)
    f["payload"].update(over)
    return f


exec_id = req["openUniverse"]["executionId"]
wrong_exec = exec_id[:-1] + ("0" if exec_id[-1] != "0" else "1")
s = {"planFrames": len(plan["schedule"]), "cancelReserve": plan["cancelReserve"],
     "full": consume(frames),
     "fullThenCancel": consume(frames + [cancel(len(frames))]),
     "cancelAsFirstFrameBeforeHello": consume([cancel(0)]),
     "helloThenCancel": consume(frames[:1] + [cancel(1)]),
     "cancelWrongExecutionIdSameLength": consume(frames[:3] + [cancel(3, executionId=wrong_exec)]),
     "cancelWrongReasonSameLengthOrShorter": consume(frames[:3] + [cancel(3, reason="user-interrup")]),
     "cancelWrongAnalysisOrdinal": consume(frames[:3] + [cancel(3, analysisOrdinal=7)]),
     "carrierCancelWrongReason": carrier("Cancel", cancel(3, reason="user-interrup")["payload"]),
     "executionIdUsed": exec_id, "wrongExecutionId": wrong_exec}
out["S_sender"] = s

# ---------------- P: prepared defaulted stale + over-limit
p = {}
for explicit in (False, True):
    prep, _ = R.prepared_case({"fixture": "prepInert", "rows": 300})
    prep["rows"][0]["inputBinding"]["toolchainDigest"] = "9" * 64
    owner = NE.prepared_output_set_admit(copy.deepcopy(prep), fx["ctx"], explicit)
    succ = REP.prepared_output_set_admit_successor(NE, doc, prep, fx["ctx"], explicit)
    p["explicit" if explicit else "defaulted"] = {"rows": 300, "staleRows": len(owner.get("staleRows", [])), "ownerOutcome": owner["outcome"],
                                                  "ownerUsableRows": len(owner.get("usableRows", [])), "successorOutcome": succ["outcome"],
                                                  "successorUsableRows": len(succ.get("usableRows", [])), "successorRefusal": (succ.get("successorRefusal") or {}).get("raw"),
                                                  "wireLimitDisclosure": succ.get("wireLimitDisclosure")}
# all fresh 300 defaulted, for contrast
prep, _ = R.prepared_case({"fixture": "prepInert", "rows": 300})
succ = REP.prepared_output_set_admit_successor(NE, doc, prep, fx["ctx"], False)
p["defaultedAllFresh300"] = {"successorOutcome": succ["outcome"], "usableRows": len(succ.get("usableRows", [])), "wireLimitDisclosure": succ.get("wireLimitDisclosure")}
# what a 299-entry prepared plan would do at planner and carrier
pl = {"protocol": "rust-semantic", "snapshot": [{"n": 1, "pathScalars": 8, "byteLength": 3}],
      "dependency": [{"n": 1, "packageKey": "serde 1.0.200 registry+https://github.com/rust-lang/crates.io-index", "pathScalars": 10, "byteLength": 3}],
      "prepared": {"n": 299, "configurationCount": 0, "blobByteLength": 3}}
res = REP.plan(doc, limits, pl, fx, AR.prepared_entries)
p["planner299PreparedEntries"] = {"refusal": (res.get("refusal") or {}).get("raw"), "largestPreparedManifest": res["largestFrame"].get("PreparedOutputManifest")}
r299 = REP.build_plan(pl, fx, AR.prepared_entries)
p["carrier299PreparedManifest"] = carrier("PreparedOutputManifest", r299["preparedManifest"])
# phase A precedence: non-inert dylib row plus a bad generated path
dy = copy.deepcopy(fx["prepDylib"])
gen = copy.deepcopy(fx["prepGenerated"])
rows = dy["rows"] + [r for r in gen["rows"] if r["kind"] == "generated-file"]
rows[-1] = copy.deepcopy(rows[-1]); rows[-1]["generated"]["logicalPath"] = "x" + LF + "/../y"
dy["rows"] = rows
try:
    succ = REP.prepared_output_set_admit_successor(NE, doc, dy, fx["ctx"], True)
    p["dylibPlusBadPath"] = {"outcome": succ["outcome"], "refusal": (succ.get("successorRefusal") or {}).get("raw"), "ownerRan": succ.get("ownerRan"), "ownerD9": succ.get("d9")}
except Exception as e:  # noqa: BLE001
    p["dylibPlusBadPath"] = "EXC:" + type(e).__name__ + ":" + str(e)[:200]
out["P_prepared"] = p

# ---------------- R: relation payload CanonicalPath
rel = json.load(open(os.path.join(arch, CM.ARCH_PINS["relationRegistry2"][0])))
r = {"relationCanonicalPathPattern": rel["$defs"]["CanonicalPath"]["pattern"],
     "inSuccessorRows": any(x["document"] == rel["$id"] for x in json.load(open(os.path.join(COPY, "owner-pattern-successor.v1.json")))["schemaPatternRows"])}
for v in ["src/a.rs", "x" + LF + "/../y.rs", "../y.rs", "a/.." + LF]:
    sch = json.loads(json.dumps(rel)); sch["$ref"] = "#/$defs/CanonicalPath"
    try:
        NE.C.validate(sch, v); rr = "admitted"
    except Exception as e:  # noqa: BLE001
        rr = "refused:" + type(e).__name__
    r[json.dumps(v)] = {"installedCanonicalValidate_relationRegistry": rr, "evidenceCorrectedSchema": REP.owner_schema_ok(NE, "#/$defs/CanonicalPath", v)}
out["R_relationPayloadPath"] = r
# ---------------- I: identity-model LogicalPath through IM.C, pinned vs successor-installed (outside declared parents)
ids3 = json.load(open(os.path.join(arch, CM.ARCH_PINS["identitySchemas3"][0])))
im = {}
for label, mod in (("pinned", NE_PINNED), ("successorInstalled", NE)):
    for v in ["a/b", "a/.." + LF, "a/..", "x" + LF + "/../y"]:
        sch = json.loads(json.dumps(ids3)); sch["$ref"] = "#/$defs/LogicalPath"
        try:
            mod.IM.C.validate(sch, v); rr = "admitted"
        except Exception as e:  # noqa: BLE001
            rr = "refused:" + type(e).__name__
        im.setdefault(label, {})[json.dumps(v)] = rr
    im[label + "_IM_C_patched"] = bool(getattr(mod.IM.C, OS.MARK, False))
out["I_identityLogicalPathViaIM"] = im
json.dump(out, open(os.path.join(HERE, "probe_sender_prepared.out.json"), "w"), indent=1, ensure_ascii=True)
print(json.dumps(out, indent=1, ensure_ascii=True))
