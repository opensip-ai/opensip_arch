#!/usr/bin/env python
"""P5 - M-2: closed TypeScript native context.

Independent adversarial mutations of the REAL fixtures, including cases the
subject's own 18 TS-context cases do not run:
  - typescriptStdlibMerkleRoot actually exists and is reachable at the nested
    location the contract cites (A-1),
  - compiler change / stdlib change / config-input change each move
    nativeContextId AND universeId, and to DIFFERENT values,
  - a foreign closure tree, a foreign context and a Rust descriptor refuse,
  - the A-2 identity-spelling law: one digest, prefixed native form vs bare Plan
    form,
  - Plan digests deduplicate for a genuinely shared context but not for two
    different contexts.
"""
import copy, importlib.util, json, sys
from pathlib import Path

DC = Path("/tmp/opensip-design-corrections/candidate-subject.v6/docs/coop/design-corrections")
sys.path.insert(0, str(DC / "foundation"))


def load(n, p):
    s = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


N = load("nem", DC / "native/native_evidence_model.v2.py")
CASES = json.loads((DC / "native/native-cases.v2.json").read_text())
FX = CASES["fixtures"]

out = {"probe": "P5-M2-typescript-native-context"}

ctx = copy.deepcopy(FX["tsNativeContext"])
trees = copy.deepcopy(FX["tsClosureTrees"])
universe = copy.deepcopy(FX["tsUniverse"])

# --- A-1: the field exists at the cited nesting ------------------------------
schemas = json.loads((DC / "native/native-evidence.schemas.v2.json").read_text())
tsn = schemas["$defs"].get("TypeScriptNativeContextV2", {})
tstool = schemas["$defs"].get("TypeScriptToolchainIdentityV1", {})
rustool = schemas["$defs"].get("ToolchainIdentityV1", {})
out["A1_nesting"] = {
    "TypeScriptNativeContextV2_exists": bool(tsn),
    "toolchainProps": sorted(tstool.get("properties", {}).keys()),
    "typescriptStdlibMerkleRoot_at_toolchain":
        "typescriptStdlibMerkleRoot" in tstool.get("properties", {}),
    "rustcDevLlvmDigest_at_rust_toolchain":
        "rustcDevLlvmDigest" in rustool.get("properties", {}),
    "fixtureValue": ctx.get("toolchain", {}).get("typescriptStdlibMerkleRoot"),
    "mirroredNesting": ("typescriptStdlibMerkleRoot" in tstool.get("properties", {})
                        and "rustcDevLlvmDigest" in rustool.get("properties", {})),
}

# --- baseline admission -------------------------------------------------------
base = N.admit_native_context("typescript", ctx, trees)
out["baseline"] = {"refusals": base["refusals"], "domain": base["domain"],
                   "nativeContextId": base["nativeContextId"],
                   "planNativeContextDigest": base["planNativeContextDigest"]}

u_base = N.bind_typescript_universe(universe, base, ctx)
out["baselineUniverse"] = {"result": u_base["result"],
                           "universeId": u_base.get("universeId"),
                           "refusals": u_base.get("refusals")}

# --- A-2: one digest, two textual spellings ----------------------------------
out["A2_identitySpelling"] = {
    "nativeFormPrefixed": base["nativeContextId"],
    "planFormBareHex": base["planNativeContextDigest"],
    "sameDigestTwoForms": base["nativeContextId"]
        == "sha256:" + base["planNativeContextDigest"],
    "planFormHasNoPrefix": not base["planNativeContextDigest"].startswith("sha256:"),
}

# --- changing compiler / stdlib inputs ---------------------------------------
variants = {}
for label, cfix, tfix in [
        ("compilerChanged", "tsCompilerChangedContext", "tsCompilerChangedTrees"),
        ("stdlibChanged", "tsStdlibChangedContext", "tsStdlibChangedTrees")]:
    a = N.admit_native_context("typescript", copy.deepcopy(FX[cfix]),
                               copy.deepcopy(FX[tfix]))
    u = N.bind_typescript_universe(
        dict(universe, nativeContextId=a["nativeContextId"]), a,
        copy.deepcopy(FX[cfix])) if not a["refusals"] else {"universeId": None}
    variants[label] = {"refusals": a["refusals"],
                       "nativeContextId": a["nativeContextId"],
                       "universeId": u.get("universeId"),
                       "movesContext": a["nativeContextId"] != base["nativeContextId"]}
out["inputChanges"] = variants
out["inputChanges"]["compilerAndStdlibMoveToDifferentValues"] = (
    variants["compilerChanged"]["nativeContextId"]
    != variants["stdlibChanged"]["nativeContextId"])

# --- config-input change (compilerOptions projection) -------------------------
cfg_ctx = copy.deepcopy(ctx)
proj = cfg_ctx.get("configProjection", {})
out["configProjectionKeys"] = sorted(proj.keys())
mutated = False
ho = proj.get("honoredOptions")
if isinstance(ho, dict):
    for k, v in list(ho.items()):
        if isinstance(v, bool):
            ho[k] = not v
            out["configInputMutated"] = {"field": "honoredOptions." + k,
                                         "from": v, "to": ho[k]}
            mutated = True
            break
if mutated:
    a_cfg = N.admit_native_context("typescript", cfg_ctx, trees)
    out["configInputChange"] = {
        "refusals": a_cfg["refusals"],
        "nativeContextId": a_cfg["nativeContextId"],
        "movesContextOrRefuses": (bool(a_cfg["refusals"])
                                  or a_cfg["nativeContextId"] != base["nativeContextId"]),
    }

# --- foreign closure tree ------------------------------------------------------
foreign_trees = copy.deepcopy(FX["tsMacClosureTrees"])
a_ft = N.admit_native_context("typescript", ctx, foreign_trees)
out["foreignClosureTree"] = {"refusals": a_ft["refusals"],
                             "refused": bool(a_ft["refusals"])}

# --- Rust descriptor offered as TypeScript -------------------------------------
a_rust = N.admit_native_context("typescript",
                                copy.deepcopy(FX["rustContextOfferedAsTypescript"]),
                                trees)
out["rustDescriptorAsTypescript"] = {"refusals": a_rust["refusals"],
                                     "refused": bool(a_rust["refusals"])}

# --- universe bound to a foreign / unminted context ----------------------------
mac = N.admit_native_context("typescript", copy.deepcopy(FX["tsMacNativeContext"]),
                             copy.deepcopy(FX["tsMacClosureTrees"]))
u_foreign = N.bind_typescript_universe(universe, mac, copy.deepcopy(FX["tsMacNativeContext"]))
out["universeBoundToForeignContext"] = {"result": u_foreign["result"],
                                        "refusals": u_foreign.get("refusals")}

# context bytes that are not the admitted ones
u_wrongbytes = N.bind_typescript_universe(universe, base, copy.deepcopy(FX["tsMacNativeContext"]))
out["universeWithNonAdmittedContextBytes"] = {"result": u_wrongbytes["result"],
                                              "refusals": u_wrongbytes.get("refusals")}

# context omitted entirely (Codex note 7 bypass)
try:
    N.bind_typescript_universe(universe, base)
    out["universeWithoutContextArg"] = {"refused": False,
                                        "note": "context is optional - BYPASS"}
except TypeError as e:
    out["universeWithoutContextArg"] = {"refused": True,
                                        "error": "TypeError (required arg): " + str(e)[:90]}

# --- Plan digest set semantics --------------------------------------------------
out["planDigests"] = {
    "sharedContextDeduplicates": N.plan_native_context_digests([base, base]),
    "twoDifferentContexts": N.plan_native_context_digests([base, mac]),
}
out["planDigests"]["dedupToOne"] = len(out["planDigests"]["sharedContextDeduplicates"]) == 1
out["planDigests"]["distinctKeptSeparate"] = len(out["planDigests"]["twoDifferentContexts"]) == 2
out["planDigests"]["allBareHex"] = all(
    len(x) == 64 and not x.startswith("sha256:")
    for x in out["planDigests"]["twoDifferentContexts"])

# --- platform-specific identity through the signed tool closure -----------------
out["platformIdentity"] = {
    "macContextId": mac["nativeContextId"],
    "baseContextId": base["nativeContextId"],
    "identityIsPlatformSpecific": mac["nativeContextId"] != base["nativeContextId"],
}

print(json.dumps(out, indent=1))
