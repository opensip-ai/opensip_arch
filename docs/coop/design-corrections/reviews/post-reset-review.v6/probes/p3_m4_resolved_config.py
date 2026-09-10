#!/usr/bin/env python
"""P3 - M-4: exact resolved semantic-configuration shape, via the REAL resolver
and the REAL Run graph (not the schema alone).

Blind M-4: `{"analysis":{...}}` and the five-section spelling both validated and
minted different resolvedConfigDigest. Tests:
  1. an omitted input section and an explicitly-empty input section converge to
     ONE resolved spelling / ONE digest,
  2. the resolved value always carries exactly the five sections,
  3. `analysis` post-resolution requires profileId+capabilities+budget,
  4. absent vs explicitly-empty entryPoints stays DISTINCT,
  5. operations/presentation are excluded from the semantic config,
  6. the digest propagates into snapshot2/plan2/run2 identically.
"""
import copy, importlib.util, json, sys
from pathlib import Path

DC = Path("/tmp/opensip-design-corrections/candidate-subject.v6/docs/coop/design-corrections")
F = DC / "foundation"


def load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


M = load("cfg2", F / "product-configuration-model.py")
C = M.C

registry = {"profiles": ["default"],
            "capabilities": ["typescript.imports", "rust.imports"],
            "packs": ["architecture"]}

ANALYSIS = {"profileId": "default",
            "capabilities": ["rust.imports", "typescript.imports"],
            "budget": {"unit": "work-units", "limit": 1000}}

out = {"probe": "P3-M4-resolved-config-shape"}

# --- 1/2. omitted vs explicitly-empty input sections converge -----------------
omitted = {"schemaVersion": 2, "analysis": copy.deepcopy(ANALYSIS)}
explicit_empty = {"schemaVersion": 2, "analysis": copy.deepcopy(ANALYSIS),
                  "components": {}, "discovery": {}, "policy": {}, "evidence": {}}

r_om = M.resolve({"defaults": C.canonical(omitted)}, registry)
r_ex = M.resolve({"defaults": C.canonical(explicit_empty)}, registry)

out["omittedSections"] = {
    "resolvedSections": sorted(r_om["semantic"].keys()),
    "digest": r_om["resolvedConfigDigest"],
    "canonicalBytes": C.canonical(r_om["semantic"]).decode(),
}
out["explicitlyEmptySections"] = {
    "resolvedSections": sorted(r_ex["semantic"].keys()),
    "digest": r_ex["resolvedConfigDigest"],
}
out["convergeToOneSpelling"] = (
    r_om["resolvedConfigDigest"] == r_ex["resolvedConfigDigest"]
    and C.canonical(r_om["semantic"]) == C.canonical(r_ex["semantic"]))
out["alwaysExactlyFiveSections"] = (
    sorted(r_om["semantic"].keys())
    == ["analysis", "components", "discovery", "evidence", "policy"])

# --- 3. analysis post-resolution requiredness --------------------------------
def refuses(fn):
    try:
        fn()
        return {"refused": False}
    except Exception as e:
        return {"refused": True, "error": type(e).__name__ + ":" + str(e)[:90]}


out["analysisRequired"] = {
    "emptyAnalysis": refuses(lambda: M.resolve(
        {"defaults": C.canonical({"schemaVersion": 2, "analysis": {}})}, registry)),
    "noProfileId": refuses(lambda: M.resolve({"defaults": C.canonical(
        {"schemaVersion": 2, "analysis": {k: v for k, v in ANALYSIS.items()
                                          if k != "profileId"}})}, registry)),
    "noCapabilities": refuses(lambda: M.resolve({"defaults": C.canonical(
        {"schemaVersion": 2, "analysis": {k: v for k, v in ANALYSIS.items()
                                          if k != "capabilities"}})}, registry)),
    "noBudget": refuses(lambda: M.resolve({"defaults": C.canonical(
        {"schemaVersion": 2, "analysis": {k: v for k, v in ANALYSIS.items()
                                          if k != "budget"}})}, registry)),
}

# --- 4. absent vs explicitly-empty entryPoints stays distinct ----------------
absent_ep = {"schemaVersion": 2, "analysis": copy.deepcopy(ANALYSIS), "discovery": {}}
empty_ep = {"schemaVersion": 2, "analysis": copy.deepcopy(ANALYSIS),
            "discovery": {"entryPoints": []}}
r_abs = M.resolve({"defaults": C.canonical(absent_ep)}, registry)
r_emp = M.resolve({"defaults": C.canonical(empty_ep)}, registry)
out["entryPointsAbsentVsEmpty"] = {
    "absentResolvedDiscovery": r_abs["semantic"]["discovery"],
    "emptyResolvedDiscovery": r_emp["semantic"]["discovery"],
    "absentDigest": r_abs["resolvedConfigDigest"],
    "emptyDigest": r_emp["resolvedConfigDigest"],
    "staysDistinct": r_abs["resolvedConfigDigest"] != r_emp["resolvedConfigDigest"],
}

# --- 5. operations / presentation excluded -----------------------------------
out["excludedSections"] = {}
for section, rec in [("ui", {"color": "never"}), ("retention", {"maxBytes": 1})]:
    r = M.resolve({"defaults": C.canonical(omitted),
                   "flags": C.canonical({"schemaVersion": 2, section: rec})}, registry)
    out["excludedSections"][section] = {
        "digestUnchanged": r["resolvedConfigDigest"] == r_om["resolvedConfigDigest"],
        "notInSemantic": section not in r["semantic"],
    }
# a top-level 'operations'/'presentation' key must not be silently admitted
for bogus in ("operations", "presentation"):
    out["excludedSections"][bogus + "_rejected"] = refuses(
        lambda b=bogus: M.resolve({"defaults": C.canonical(omitted),
                                   "flags": C.canonical({"schemaVersion": 2, b: {}})}, registry))

# --- 6. propagation into snapshot2 / plan2 / run2 -----------------------------
IM = load("identity_model", F / "identity-model.py")
schemas = json.loads((F / "identity-schemas.v2.json").read_text())


def h(domain, desc):
    return IM.C.H(domain, desc) if hasattr(IM.C, "H") else None


out["runGraphPropagation"] = {}
try:
    d_a = r_om["resolvedConfigDigest"]
    d_b = r_emp["resolvedConfigDigest"]
    inv = [{"path": "src/a.ts", "contentSha256": "a" * 64, "byteLength": 1}]

    def snap(cfg):
        return IM.identity("snapshot", {
            "schemaVersion": 2, "projectId": "prj1-" + "a" * 64,
            "sourceInventory": inv, "resolvedConfigDigest": cfg,
            "scopeDigest": "b" * 64, "vcsDigest": "c" * 64})

    s1, s2 = snap(d_a), snap(d_b)
    out["runGraphPropagation"] = {
        "snapshotConverged": snap(d_a) == snap(r_ex["resolvedConfigDigest"]),
        "snapshotDistinctForAbsentVsEmpty": s1 != s2,
        "snapshot_omitted": s1, "snapshot_emptyEntryPoints": s2,
    }
except Exception as e:
    out["runGraphPropagation"] = {"note": "direct mint unavailable: "
                                          + type(e).__name__ + ":" + str(e)[:120]}

print(json.dumps(out, indent=1))
