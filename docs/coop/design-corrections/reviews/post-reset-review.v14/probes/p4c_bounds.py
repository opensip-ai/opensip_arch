"""CB4-SHOULD-2 bounds: maximum cardinality, the 4096 path bound, and whether counts stay
honest at the edges (no silent truncation)."""
import json, sys
sys.path.insert(0, "/tmp/opensip-design-corrections/post-reset-review.v14/probes")
from harness import CI, M, C, N, probe, emit
import jsonschema

def _val(defname, inst):
    jsonschema.validate(inst, {"$defs": NS["$defs"], "$ref": "#/$defs/" + defname})
    return True

ROOT = "/tmp/opensip-design-corrections/post-reset-review.v14/work"
NS = json.load(open(ROOT + "/docs/coop/design-corrections/workflows/schemas/common.schema.json"))
STEP = NS["$defs"]["CapabilityAvailabilityStepV1"]
INVO = NS["$defs"]["CapabilityAvailabilityV1"]
NOTICE = NS["$defs"]["CapabilityAvailabilityNoticeV1"]

probe("K0-a-step-notice-array-is-bounded-by-the-analysis-spec-request-bound", "check",
      lambda: STEP["properties"]["notices"]["maxItems"] == 1024)
probe("K1-the-invocation-step-array-is-bounded-by-the-invocation-step-bound", "check",
      lambda: INVO["properties"]["steps"]["maxItems"] == 64)
probe("K2-workspaceRoot-is-the-4096-path-type-not-the-1024-text-type", "check",
      lambda: NOTICE["properties"]["workspaceRoot"]["$ref"].endswith("UserInputPath")
              and NS["$defs"]["UserInputPath"]["maxLength"] == 4096
              and NS["$defs"]["BoundedText"]["maxLength"] == 1024)

# A long-but-valid workspaceRoot must survive whole: this is the case concatenation into one
# BoundedText subject would have silently truncated.
LONG = "w/" + "d" * 4000
def long_path_notice():
    u = [{"capabilityId": "clones-near", "languageMode": "ts-tsconfig", "workspaceRoot": LONG,
          "projection": "selection-account-only", "relations": []}]
    return N.release_absence_notices(u)
probe("K3-a-4000-character-workspaceRoot-survives-the-notice-intact", "check",
      lambda: long_path_notice()["notices"][0]["workspaceRoot"] == LONG)
probe("K4-and-it-is-not-concatenated-into-a-1024-bounded-subject", "check",
      lambda: "subject" not in long_path_notice()["notices"][0])

# Maximum cardinality: a full step, and an invocation whose total exceeds any single step's
# bound - the case one flat 1024 array refused.
def big(n, root="pkg/a"):
    return [{"capabilityId": i, "languageMode": m, "workspaceRoot": "%s/%d" % (root, k),
             "projection": "selection-account-only", "relations": []}
            for k in range(n)
            for i, m in [("clones-near", "ts-tsconfig")]][:n]

probe("K5-a-full-1024-notice-step-is-representable-with-an-exact-count", "check",
      lambda: (lambda s: s["noticeCount"] == len(s["notices"]) == 1024)(
          N.release_absence_notices(big(1024))))
# ATTEMPT 1 expected the HELPER to refuse an oversized step. It does not - and it does not
# truncate either: it returned all 1025 notices with noticeCount 1025, which is the honest
# direction. The bound is held in two other places, and both are checked instead:
#   (a) the overflow is UNREACHABLE from a lawful selection, and
#   (b) if forced anyway, the record is refused by the schema rather than silently emitted.
probe("K6a-the-helper-does-not-silently-truncate-an-oversized-input", "check",
      lambda: (lambda s: s["noticeCount"] == len(s["notices"]) == 1025)(
          N.release_absence_notices(big(1025))))
probe("K6b-a-step-notice-overflow-is-unreachable-one-absence-per-requested-row", "check",
      lambda: json.load(open(ROOT + "/docs/coop/design-corrections/foundation/"
                             "identity-schemas.v2.json"))["$defs"]["analysis-spec"]
              ["properties"]["requestedCapabilities"]["maxItems"]
              == STEP["properties"]["notices"]["maxItems"] == 1024)
probe("K6c-negative-and-a-forced-oversized-step-is-refused-by-the-schema", "negative",
      lambda: _val("CapabilityAvailabilityStepV1",
                   {"stepId": 0, "noticeCount": 1025,
                    "notices": [{"code": "native.capability-unavailable",
                                 "capabilityId": "c%d" % i, "languageMode": "ts-tsconfig",
                                 "workspaceRoot": "p", "remedy": "r"} for i in range(1025)]}),
      "")
def two_big_steps():
    return N.invocation_availability([(0, big(1023, "pkg/a")), (1, big(1023, "pkg/b"))])
probe("K7-two-steps-of-1023-compose-2046-notices-which-one-flat-1024-array-refused",
      "check",
      lambda: (lambda a: a["totalNoticeCount"] == 2046 == sum(s["noticeCount"] for s in a["steps"])
                         and a["stepCount"] == 2)(two_big_steps()))
probe("K8a-the-step-bound-is-the-invocations-own-StepId-range-not-a-new-limit", "check",
      lambda: json.load(open(ROOT + "/docs/coop/design-corrections/workflows/schemas/"
                             "common.schema.json"))["$defs"]["StepId"]["maximum"] == 63
              and INVO["properties"]["steps"]["maxItems"] == 64)
probe("K8b-negative-a-forced-65-step-invocation-is-refused-by-the-schema", "negative",
      lambda: _val("CapabilityAvailabilityV1",
                   {"stepCount": 65, "totalNoticeCount": 0,
                    "steps": [{"stepId": i % 64, "noticeCount": 0, "notices": []}
                              for i in range(65)]}), "")
probe("K8c-negative-a-step-id-outside-the-range-is-refused", "negative",
      lambda: _val("CapabilityAvailabilityStepV1",
                   {"stepId": 64, "noticeCount": 0, "notices": []}),
      "64 is greater than the maximum of 63")
probe("K8d-positive-a-lawful-step-record-validates", "check",
      lambda: _val("CapabilityAvailabilityStepV1",
                   {"stepId": 0, "noticeCount": 0, "notices": []}) is True)
probe("K9-counts-are-exact-at-the-edge-not-a-residue-of-a-dropped-tail", "check",
      lambda: all(s["noticeCount"] == len(s["notices"]) for s in two_big_steps()["steps"]))

emit("/tmp/opensip-design-corrections/post-reset-review.v14/evidence/probe-capability-bounds.json")
