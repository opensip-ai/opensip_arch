"""CB4-SHOULD-2 continued: release-declaration integrity, bounds and overflow honesty,
precedence for a compiler-free capability, all-surface parity, and closure over the
RETAINED analysis-spec."""
import copy, json, sys
sys.path.insert(0, "/tmp/opensip-design-corrections/post-reset-review.v14/probes")
from harness import CI, M, C, N, probe, emit

ROOT = "/tmp/opensip-design-corrections/post-reset-review.v14/work"
MX = N.CAPABILITY_MATRIX
IDS = [c["id"] for c in MX["capabilities"]]
MODES = MX["languageModes"]
CELL = {(c["capability"], c["mode"]): c["state"] for c in MX["cells"]}
INV = json.load(open(ROOT + "/docs/coop/design-corrections/workflows/command-inventory.v1.json"))

def reg(rows): return sorted(rows, key=C.canonical)

# --- 1. A release declaration cannot redefine the product's promises. ----------------------
probe("E0-negative-a-declaration-naming-an-unregistered-capability-refuses", "negative",
      lambda: N.admit_release_capability_registry(
          reg([{"capabilityId": "clones-magic", "languageModes": ["ts-tsconfig"]}])),
      "native.release-capability-unregistered")
probe("E1-negative-a-declaration-naming-an-unregistered-mode-refuses", "negative",
      lambda: N.admit_release_capability_registry(
          reg([{"capabilityId": "inventory", "languageModes": ["go-modules"]}])),
      "native.release-capability-mode-unregistered")
probe("E2-negative-a-declaration-over-a-NOT-SELECTED-cell-refuses", "negative",
      lambda: N.admit_release_capability_registry(
          reg([{"capabilityId": "clones-cross-tsjs", "languageModes": ["rust-cargo"]}])),
      "native.release-capability-mode-not-selected")
probe("E3-negative-a-duplicate-capabilityId-refuses-rather-than-merging", "negative",
      lambda: N.admit_release_capability_registry(
          reg([{"capabilityId": "inventory", "languageModes": ["ts-tsconfig"]},
               {"capabilityId": "inventory", "languageModes": ["syntax-only"]}])),
      "native.release-capability-duplicate")
# These two helpers ADMIT by returning the rows and REFUSE by raising; attempt 1 wrongly
# asserted an empty fault list.
probe("E4-positive-a-lawful-single-row-registry-admits", "check",
      lambda: N.admit_release_capability_registry(
          reg([{"capabilityId": "inventory", "languageModes": ["ts-tsconfig"]}]))
              == [{"capabilityId": "inventory", "languageModes": ["ts-tsconfig"]}])

# --- 2. The request layer is closed by SHAPE before membership. ----------------------------
probe("E5-negative-a-relation-at-rung-spelling-is-refused-by-shape", "negative",
      lambda: N.admit_requested_capabilities(
          [{"capabilityId": "clones@normalized-body-hash", "languageMode": "ts-tsconfig",
            "workspaceRoot": ".", "required": True}]),
      "native.requested-capability")
probe("E6-negative-an-unregistered-capability-request-refuses", "negative",
      lambda: N.admit_requested_capabilities(
          [{"capabilityId": "telepathy", "languageMode": "ts-tsconfig",
            "workspaceRoot": ".", "required": True}]),
      "native.requested-capability-unregistered")
probe("E7-negative-a-NOT-SELECTED-cell-request-is-UNSATISFIABLE-not-merely-invalid",
      "negative",
      lambda: N.admit_requested_capabilities(
          [{"capabilityId": "clones-cross-tsjs", "languageMode": "syntax-only",
            "workspaceRoot": ".", "required": True}]),
      "native.requested-capability-mode-not-selected")
probe("E8-positive-an-UNSUPPORTED-TYPED-cell-request-is-ADMISSIBLE-not-refused", "check",
      lambda: N.admit_requested_capabilities(
          [{"capabilityId": "references", "languageMode": "syntax-only",
            "workspaceRoot": ".", "required": True}])
              == [{"capabilityId": "references", "languageMode": "syntax-only",
                   "workspaceRoot": ".", "required": True}])

# --- 3. Precedence: a compiler-free capability under syntax-only keeps the more specific
#        deficiency, and is NOT rejected merely because the provider is missing.
def syntax_support(relation, rung):
    rows = N.selected_grammar_rows("syntax-only") if hasattr(N, "selected_grammar_rows") else None
    return N.syntax_capability_support(rows, relation, rung) if rows is not None else None
probe("E9-references-under-syntax-only-is-UNSUPPORTED-TYPED-with-a-named-deficiency", "check",
      lambda: CELL[("references", "syntax-only")] == "UNSUPPORTED-TYPED"
              and next(c for c in MX["cells"]
                       if c["capability"] == "references" and c["mode"] == "syntax-only"
                       )["deficiency"] == "language-tier-unsupported")
probe("E10-the-precedence-order-ranks-language-tier-unsupported-above-provider-unavailable",
      "check",
      lambda: N.PRECEDENCE_V2.index("language-tier-unsupported")
              < N.PRECEDENCE_V2.index("provider-unavailable"))
probe("E11-language-tier-unsupported-admits-exactly-capability-missing", "check",
      lambda: json.load(open(ROOT + "/docs/coop/design-corrections/native/"
                             "native-evidence.schemas.v2.json"))
              ["x-opensip-deficiency-cause-registry"]["deficiencies"]
              ["language-tier-unsupported"]["allowedCauses"] == ["capability-missing"])

# --- 4. An unsupported class must not claim a complete EMPTY result. -----------------------
# ATTEMPT 1 expected build(has_match=False) under a syntax universe to BE the false-complete
# graph. It is not: the fixture honestly emits coverage `unknown` /
# `language-tier-unsupported` / `capability-missing`, and that Run closing is the CORRECT
# outcome and is retained below as the positive control. The false claim has to be forged.
def syntax_entry(mutate):
    run, objects, blobs = CI.build(relation="references", has_match=False, resolved=True,
                                   universe_language="syntax", pure_syntax=True)
    view = next(v for d, v in objects.values() if d == "view")
    for cid in view["coverageIds"]:
        cov = copy.deepcopy(objects[cid][1])
        payload = C.parse(blobs[cov["payloadDigest"]])
        if payload["entry"]["relation"] != "references": continue
        mutate(payload["entry"])
        cov["payloadDigest"] = CI.put_blob(blobs, payload)
        CI.rekey(objects, cid, cov, run)
        break
    CI.resync_witness(objects, blobs, run); CI.resync_proof_refs(objects, blobs, run)
    return M.close_run(run, objects, blobs)

probe("E12a-positive-the-honest-unsupported-answer-closes-a-run", "check",
      lambda: (lambda e: e["coverage"] == "unknown"
                         and e["deficiency"] == "language-tier-unsupported"
                         and e["nativeCause"] == "capability-missing")(
          next(C.parse(blobs[objects[cid][1]["payloadDigest"]])["entry"]
               for (run, objects, blobs) in [CI.build(relation="references", has_match=False,
                                                      resolved=True, universe_language="syntax",
                                                      pure_syntax=True)]
               for cid in next(v for d, v in objects.values() if d == "view")["coverageIds"]
               if C.parse(blobs[objects[cid][1]["payloadDigest"]])["entry"]["relation"]
                  == "references")))

def falsely_complete(e):
    e["coverage"] = "complete"; e["deficiency"] = None; e["nativeCause"] = None
probe("E12-negative-an-unsupported-class-cannot-claim-a-complete-empty-result", "negative",
      lambda: syntax_entry(falsely_complete), "SYNTAX_CAPABILITY_UNSUPPORTED_SCOPE")

def relabelled_deficiency(e):
    e["deficiency"] = "provider-unavailable"; e["nativeCause"] = "capability-missing"
probe("E12b-negative-the-unsupported-scope-cannot-be-relabelled-to-a-weaker-deficiency",
      "negative", lambda: syntax_entry(relabelled_deficiency),
      "SYNTAX_CAPABILITY_DEFICIENCY_MISMATCH")

# --- 5. All-surface parity: the disclosure is a DECLARED parity field of every analysis
#        command, not merely present on the envelope.
def analysis_commands():
    cmds = INV["commands"] if isinstance(INV.get("commands"), list) else []
    return [c for c in cmds if c.get("requestClass") == "analysis"]
probe("E13-there-are-exactly-five-analysis-commands", "check",
      lambda: sorted(c["name"] if "name" in c else c["id"] for c in analysis_commands())
              == ["analyze", "audit", "default", "fit", "repair-verify"])
probe("E14-capability-availability-is-a-declared-parity-field-of-every-analysis-command",
      "check",
      lambda: all("capability-availability" in c.get("parityFields", [])
                  for c in analysis_commands()))

# --- 6. Closed again at Run closure over the RETAINED analysis-spec, not only in the helper.
def run_with_bad_capability(spelling):
    run, objects, blobs = CI.build(relation="references", has_match=True, resolved=True)
    plan = copy.deepcopy(objects[run["planId"]][1])
    spec = C.parse(blobs[plan["analysisSpecDigest"]])
    spec["requestedCapabilities"] = [dict(r, capabilityId=spelling)
                                     for r in spec["requestedCapabilities"]]
    plan["analysisSpecDigest"] = CI.put_blob(blobs, CI.sort_canonical_sets("analysis-spec", spec))
    CI.rekey_plan(objects, blobs, run, plan)
    CI.resync_witness(objects, blobs, run); CI.resync_proof_refs(objects, blobs, run)
    return M.close_run(run, objects, blobs)

probe("E15-negative-an-unregistered-capability-in-the-RETAINED-spec-refuses-at-closure",
      "negative", lambda: run_with_bad_capability("telepathy"),
      "ANALYSIS_SPEC_CAPABILITY")
# The `@` spelling is refused by SHAPE, before membership is consulted - which is exactly
# what the capabilityIdLaw says should happen. Attempt 1 expected the membership fault.
probe("E16-negative-a-relation-at-rung-spelling-in-the-RETAINED-spec-refuses-by-shape",
      "negative", lambda: run_with_bad_capability("clones@normalized-body-hash"),
      "does not match")
probe("E17-positive-a-matrix-spelled-capability-in-the-retained-spec-closes", "positive",
      lambda: run_with_bad_capability("inventory"))

emit("/tmp/opensip-design-corrections/post-reset-review.v14/evidence/probe-cb4-should-2b.json")
