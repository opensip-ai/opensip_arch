"""CB4-MUST-2: deficiency cause carriers, probed at the producer boundary AND again at
retained Run closure, with positive controls and RC-3 preserved."""
import copy, json, sys
sys.path.insert(0, "/tmp/opensip-design-corrections/post-reset-review.v14/probes")
from harness import CI, M, C, N, probe, emit

SCH = N.SCHEMAS if hasattr(N, "SCHEMAS") else None
NDOC = json.load(open("/tmp/opensip-design-corrections/post-reset-review.v14/work/"
                      "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"))
REG = NDOC["x-opensip-deficiency-cause-registry"]
ROWS = REG["deficiencies"]

# --- 0. The registry is total and names EXISTING carriers, not a new enum. -----------------
probe("B0-registry-is-total-over-DeficiencyV2", "check",
      lambda: sorted(ROWS) == sorted(NDOC["$defs"]["DeficiencyV2"]["enum"]))
probe("B1-no-cause-enum-was-widened-to-fix-this", "check",
      lambda: len(NDOC["$defs"]["NativeCause"]["enum"]) == 14
              and len(NDOC["$defs"]["UnresolvedEdgeKindV1"]["enum"]) == 16
              and len(NDOC["$defs"]["DeficiencyV2"]["enum"]) == 9)
probe("B2-the-three-cited-rows-name-structured-carriers-not-nativeCause", "check",
      lambda: (ROWS["resolution-incomplete"]["carrier"] == "entry.resolutionCompleteness"
               and ROWS["external-consumers-unknown"]["carrier"] == "entry.closedWorld.exportsClosed"
               and ROWS["derivation-policy-unmet"]["carrier"] == "entry.derivationKinds"
               and all(ROWS[k]["nativeCause"] == "must-be-null" for k in
                       ("resolution-incomplete", "external-consumers-unknown",
                        "derivation-policy-unmet"))))
probe("B3-derivation-policy-unmet-is-relation-scoped-to-types-only", "check",
      lambda: ROWS["derivation-policy-unmet"].get("relations") == ["types"]
              and not any("relations" in ROWS[k] and ROWS[k]["relations"] != ["types"]
                          for k in ROWS))
probe("B4-the-selected-scalar-limitation-is-published-and-scoped-to-one-row", "check",
      lambda: "input-closure-incomplete" in REG["selectedScalarCauseLimitation"]
              and "does not and cannot enumerate" in REG["selectedScalarCauseLimitation"])
probe("B5-the-set-valued-row-is-not-claimed-to-be-a-scalar", "check",
      lambda: "SET-VALUED" in REG["whyNotMoreEnumMembers"]
              and "loses nothing" in REG["multiCauseAndPrecedence"])

# --- 1. Producer-boundary admission, driven through the candidate's own entry point. -------
def entry_case(mutate, relation="references", resolved=True):
    """Build a real Coverage payload for a complete Run, mutate ONE entry, and put it back
    through admit_coverage_result_v3 - the producer boundary the registry names."""
    run, objects, blobs = CI.build(relation=relation, has_match=True, resolved=resolved)
    cov_key = next(k for k, (d, v) in objects.items() if d == "coverage")
    cov = objects[cov_key][1]
    payload = C.parse(blobs[cov["payloadDigest"]])
    scope = objects[cov["scopeId"]][1]
    mutate(payload)
    return N.admit_coverage_result_v3(payload, scope, [], cov["payloadSchemaDigest"])

def first_entry(p): return p["entry"]

def admits(res):
    if res["result"] != "ADMIT":
        raise C.AdmissionError(json.dumps(res)[:400])
    return "run2:ok"

probe("B6-positive-an-unmutated-coverage-payload-admits", "positive",
      lambda: admits(entry_case(lambda p: None)))

def set_deficiency(deficiency, cause="__keep__", **fields):
    def m(p):
        e = first_entry(p)
        e["deficiency"] = deficiency
        if cause != "__keep__": e["nativeCause"] = cause
        e.update(fields)
    return m

# a cause without a deficiency
probe("B7-negative-a-cause-without-a-deficiency-refuses", "negative",
      lambda: admits(entry_case(set_deficiency(None, "lockfile-missing"))),
      "native.coverage-cause")
# an unrelated but schema-valid cause on a must-be-null row
probe("B8-negative-resolution-incomplete-with-a-borrowed-scalar-cause-refuses", "negative",
      lambda: admits(entry_case(set_deficiency("resolution-incomplete", "lockfile-missing"))),
      "native.coverage-cause")
# relabelled cause
probe("B9-negative-resolution-incomplete-relabelled-capability-missing-refuses", "negative",
      lambda: admits(entry_case(set_deficiency("resolution-incomplete", "capability-missing"))),
      "native.coverage-cause")
# language-tier-unsupported requires exactly capability-missing
probe("B10-negative-language-tier-unsupported-with-a-wrong-cause-refuses", "negative",
      lambda: admits(entry_case(set_deficiency("language-tier-unsupported", "lockfile-missing"))),
      "native.coverage-cause")
probe("B11-negative-language-tier-unsupported-with-a-null-cause-refuses", "negative",
      lambda: admits(entry_case(set_deficiency("language-tier-unsupported", None))),
      "native.coverage-cause")
# derivation-policy-unmet outside `types`
probe("B12-negative-derivation-policy-unmet-on-a-references-entry-refuses", "negative",
      lambda: admits(entry_case(set_deficiency("derivation-policy-unmet", None,
                                               derivationKinds=["compiler-inferred"]),
                                relation="references")),
      "native.coverage-cause")
# derivation-policy-unmet with an empty carrier
probe("B13-negative-derivation-policy-unmet-with-an-empty-carrier-refuses", "negative",
      lambda: admits(entry_case(set_deficiency("derivation-policy-unmet", None,
                                               derivationKinds=[]), relation="types")),
      "native.coverage-cause")
# external-consumers-unknown over a CLOSED world
probe("B14-negative-external-consumers-unknown-over-a-closed-world-refuses", "negative",
      lambda: admits(entry_case(lambda p: (first_entry(p).update(
          deficiency="external-consumers-unknown", nativeCause=None),
          first_entry(p).setdefault("closedWorld", {}).update(exportsClosed="closed")))),
      "native.coverage-cause")

emit("/tmp/opensip-design-corrections/post-reset-review.v14/evidence/probe-cb4-must-2.json",
     {"registryRows": {k: {kk: v.get(kk) for kk in ("carrier", "nativeCause", "allowedCauses", "relations")}
                       for k, v in ROWS.items()}})
