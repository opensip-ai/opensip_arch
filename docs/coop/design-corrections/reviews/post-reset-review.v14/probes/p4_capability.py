"""CB4-SHOULD-2: capability vocabulary authority, the matrix-fixed default, and the public
availability disclosure in the ORIGINAL invocation."""
import json, sys
sys.path.insert(0, "/tmp/opensip-design-corrections/post-reset-review.v14/probes")
from harness import CI, M, C, N, probe, emit

MX = N.CAPABILITY_MATRIX
IDS = [c["id"] for c in MX["capabilities"]]
MODES = MX["languageModes"]
CELL = {(c["capability"], c["mode"]): c["state"] for c in MX["cells"]}

# --- 0. The matrix is the closed authority and the cell set is the complete product. -------
probe("D0-cells-are-exactly-the-product-of-capabilities-and-modes", "check",
      lambda: len(MX["cells"]) == len(IDS) * len(MODES) == 66
              and set(CELL) == {(i, m) for i in IDS for m in MODES})
probe("D1-capabilityIdLaw-names-this-document-as-the-authority", "check",
      lambda: MX["capabilityIdLaw"]["selector"].endswith("#/capabilities[].id")
              and MX["capabilityIdLaw"]["members"] == IDS and len(IDS) == 11)
probe("D2-capability-ids-are-not-relation-at-rung-and-carry-no-at-sign", "check",
      lambda: all("@" not in i for i in IDS)
              and "DIFFERENT CONCEPTS" in MX["capabilityIdLaw"]["relationToRelationAtRung"])

# --- 1. The default is fixed by the MATRIX, independent of what a release ships. ------------
UNITS2 = [{"rootPath": "pkg/a", "languageMode": "ts-tsconfig", "languageFamily": "typescript"},
          {"rootPath": "pkg/b", "languageMode": "syntax-only", "languageFamily": "syntax"}]
FULL = [{"capabilityId": i, "languageModes": list(MODES)} for i in IDS
        if any(CELL[(i, m)] != "NOT-SELECTED" for m in MODES)]
FULL = sorted(({"capabilityId": r["capabilityId"],
                "languageModes": sorted(m for m in MODES
                                        if CELL[(r["capabilityId"], m)] != "NOT-SELECTED")}
               for r in FULL), key=C.canonical)
STARVED = [{"capabilityId": "inventory", "languageModes": ["ts-tsconfig"]}]

def sel(units, registry): return N.default_capability_selection(units, registry)

def requested_ids(units, registry):
    return sorted({r["capabilityId"] for r in sel(units, registry)["analysisSpec"]["requestedCapabilities"]})

probe("D3-the-default-request-set-is-identical-under-a-full-and-a-starved-release", "check",
      lambda: requested_ids(UNITS2, FULL) == requested_ids(UNITS2, STARVED))
probe("D4-the-default-requests-every-non-NOT-SELECTED-cell-for-each-unit-mode", "check",
      lambda: all(sorted(N.required_default_capabilities(u["languageMode"]))
                  == sorted(i for i in IDS if CELL[(i, u["languageMode"])] != "NOT-SELECTED")
                  for u in UNITS2))
probe("D5-UNSUPPORTED-TYPED-cells-are-requested-not-silently-dropped", "check",
      lambda: "references" in N.required_default_capabilities("syntax-only")
              and CELL[("references", "syntax-only")] == "UNSUPPORTED-TYPED")
probe("D6-NOT-SELECTED-cells-are-the-only-ones-excluded-from-the-default", "check",
      lambda: "clones-cross-tsjs" not in N.required_default_capabilities("syntax-only")
              and CELL[("clones-cross-tsjs", "syntax-only")] == "NOT-SELECTED")

# --- 2. Absence is DISCLOSED in this invocation, with the complete ownership tuple. --------
def starved_notices():
    s = sel(UNITS2, STARVED)
    return s["undeclaredCapabilities"]

probe("D7-a-starved-release-produces-undeclared-records-not-a-shrunken-request", "check",
      lambda: len(starved_notices()) > 0
              and len(sel(UNITS2, STARVED)["analysisSpec"]["requestedCapabilities"])
                  == len(sel(UNITS2, FULL)["analysisSpec"]["requestedCapabilities"]))
probe("D8-every-notice-carries-the-complete-ownership-tuple-in-typed-fields", "check",
      lambda: all({"capabilityId", "languageMode", "workspaceRoot"} <= set(u)
                  and u["workspaceRoot"] in ("pkg/a", "pkg/b") for u in starved_notices()))
probe("D9-two-workspaces-requesting-one-capability-stay-distinguishable", "check",
      lambda: len({(u["capabilityId"], u["languageMode"], u["workspaceRoot"])
                   for u in starved_notices()})
              == len(starved_notices())
              and len({u["workspaceRoot"] for u in starved_notices()}) == 2)
probe("D10-candidate-only-capabilities-project-to-a-selection-account-not-coverage", "check",
      lambda: all(u["projection"] == "selection-account-only" and u["relations"] == []
                  for u in starved_notices() if u["capabilityId"] in ("clones-near", "clones-cross-tsjs"))
              and any(u["capabilityId"] == "clones-near" for u in starved_notices()))
probe("D11-fact-producing-capabilities-name-their-exact-relation-at-rung-coordinates", "check",
      lambda: all(u["projection"] == "coverage-entry" and u["relations"]
                  for u in starved_notices() if u["capabilityId"] == "inventory"))

# --- 3. The public carrier, composed per step and delivered on the envelope. ---------------
def availability():
    notices = N.release_absence_notices(starved_notices())
    return notices, N.invocation_availability([(0, starved_notices()), (1, [])])

probe("D12-a-step-that-selected-and-found-nothing-absent-contributes-an-EMPTY-array",
      "check", lambda: (lambda a: any(s["noticeCount"] == 0 and s["notices"] == []
                                      for s in a[1]["steps"]))(availability()))
probe("D13-counts-are-exact-and-total-is-the-sum-not-a-truncation-residue", "check",
      lambda: (lambda a: a[1]["totalNoticeCount"] == sum(s["noticeCount"] for s in a[1]["steps"])
                         and all(s["noticeCount"] == len(s["notices"]) for s in a[1]["steps"])
                         and a[1]["stepCount"] == len(a[1]["steps"]))(availability()))
probe("D14-every-notice-carries-the-single-registered-code-and-a-remedy", "check",
      lambda: (lambda a: all(n["code"] == "native.capability-unavailable" and n.get("remedy")
                             for n in a[0]["notices"]))(availability()))
probe("D15-the-ownership-tuple-is-never-concatenated-into-one-bounded-subject", "check",
      lambda: (lambda a: all("capabilityId" in n and "languageMode" in n
                             and "workspaceRoot" in n for n in a[0]["notices"]))(availability()))

emit("/tmp/opensip-design-corrections/post-reset-review.v14/evidence/probe-cb4-should-2.json",
     {"capabilityIds": IDS, "languageModes": MODES, "cellCount": len(MX["cells"]),
      "notSelectedCells": [(c["capability"], c["mode"]) for c in MX["cells"]
                           if c["state"] == "NOT-SELECTED"]})
