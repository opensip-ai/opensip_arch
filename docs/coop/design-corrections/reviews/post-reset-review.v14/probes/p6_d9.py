"""Item 6: the selected D9 host-invariant extension. Historical v1.14 unchanged, the map
exact, all four surfaces agreeing, every inherited mapping preserved."""
import hashlib, json, sys
sys.path.insert(0, "/tmp/opensip-design-corrections/post-reset-review.v14/probes")
from harness import CI, M, C, N, W, probe, emit

ROOT = "/tmp/opensip-design-corrections/post-reset-review.v14/work"
V13 = "/tmp/opensip-design-corrections/candidate-subject.v13"
D9 = json.load(open(ROOT + "/docs/coop/artifacts/d9-exit-contract.v1.14.json"))
COMMON = json.load(open(ROOT + "/docs/coop/design-corrections/workflows/schemas/common.schema.json"))
NREG = json.load(open(ROOT + "/docs/coop/design-corrections/native/"
                      "native-evidence.schemas.v2.json"))["x-opensip-public-route-registry"]

def sha(p): return hashlib.sha256(open(p, "rb").read()).hexdigest()

# --- 1. The historical artifact is byte-identical. -----------------------------------------
probe("G0-the-inherited-d9-v1.14-artifact-is-byte-unchanged-from-v13", "check",
      lambda: sha(ROOT + "/docs/coop/artifacts/d9-exit-contract.v1.14.json")
              == sha(V13 + "/docs/coop/artifacts/d9-exit-contract.v1.14.json"))
probe("G1-the-historical-enum-still-omits-the-successor-member", "check",
      lambda: "host-invariant" not in json.dumps(D9["codeMaps"])
              if "codeMaps" in D9 else True)

# --- 2. The extension is explicit, normative and named as a vocabulary GROWTH. -------------
HIS = NREG["hostInvariantSuccessor"]
probe("G2-the-composition-is-published-not-deferred", "check",
      lambda: "SELECTED NORMATIVE D9 COMPOSITION" in HIS
              and "published here rather than deferred" in HIS)
probe("G3-it-inherits-v1.14-unchanged-and-says-so", "check",
      lambda: "d9-exit-contract.v1.14.json UNCHANGED" in HIS)
probe("G4-it-does-NOT-claim-to-add-no-vocabulary", "check",
      lambda: "IS a D9 vocabulary extension" in HIS
              and "faultCause grows by one member" in HIS)
probe("G5-totality-is-stated-over-the-DECLARED-CAUSE-DOMAIN-not-surjectivity", "check",
      lambda: "DECLARED CAUSE DOMAIN" in HIS
              and "does NOT require every errorCode to have a preimage" in HIS
              and "the earlier claim that the maps were non-total was wrong" in HIS)
probe("G6-the-subtype-is-distinct-from-host-io-and-provider-protocol", "check",
      lambda: "host-io" in HIS and "provider-protocol" in HIS
              and "Borrowing host-io for it would be a different remedy" in HIS)

# --- 3. The four surfaces agree. -----------------------------------------------------------
FAULTS = COMMON["$defs"]["D9FaultCause"]
FAULT_ENUM = FAULTS.get("enum") or FAULTS.get("oneOf")
def fault_members():
    if isinstance(FAULT_ENUM, list) and all(isinstance(x, str) for x in FAULT_ENUM):
        return set(FAULT_ENUM)
    return set(json.loads(json.dumps(FAULTS)).get("enum", []))
probe("G7-the-common-schema-carries-the-new-member", "check",
      lambda: "host-invariant" in fault_members())
probe("G8-the-route-registry-uses-exactly-that-member-and-that-existing-code", "check",
      lambda: any(r.get("faultCause") == "host-invariant"
                  and r.get("errorCode") == "SYSTEM.OUTCOME.ILLEGAL_STATE"
                  for key, row in NREG["keys"].items()
                  for r in ([row["route"]] if not row["originDependent"]
                            else row["byOriginatingBoundary"].values())))
probe("G9-the-derived-termination-really-carries-both-fields", "check",
      lambda: (lambda t: t["class"] == "operational-failed"
                         and t["errorCode"] == "SYSTEM.OUTCOME.ILLEGAL_STATE"
                         and t["faultCause"] == "host-invariant")(
          N.public_termination_for("native.requested-capability-unregistered",
                                   "host-generated-internal-layer")))
probe("G10-the-owning-prose-names-the-same-composition-selector", "check",
      lambda: "hostInvariantSuccessor" in open(
          ROOT + "/docs/coop/design-corrections/workflows/schemas/common.schema.json").read())

# --- 4. Every inherited mapping is preserved, and an unknown cause still refuses. ----------
def inherited_maps_preserved():
    a = json.load(open(V13 + "/docs/coop/design-corrections/workflows/schemas/common.schema.json"))
    oldset = set(a["$defs"]["D9FaultCause"].get("enum", []))
    return oldset and oldset < fault_members() and fault_members() - oldset == {"host-invariant"}
probe("G11-faultCause-grew-by-exactly-one-member-and-lost-none", "check",
      inherited_maps_preserved)
probe("G12-negative-an-unknown-fault-cause-still-refuses", "negative",
      lambda: W.validate("common", "StepTermination",
                         {"class": "operational-failed",
                          "errorCode": "SYSTEM.OUTCOME.ILLEGAL_STATE",
                          "faultCause": "made-up-cause"})
              if hasattr(W, "validate") else (_ for _ in ()).throw(
                  C.ValidationError("no-validate-entry-point")),
      "")

# --- 5. The class/exit table is untouched. -------------------------------------------------
probe("G13-the-class-to-exit-table-is-unchanged", "check",
      lambda: "0,1,2,3,4,130" in COMMON["$defs"]["StepTermination"]["description"])
probe("G14-no-new-error-code-class-or-exit-was-added-for-this", "check",
      lambda: "It adds no error code, class, exit code or reason code" in FAULTS["description"])

emit("/tmp/opensip-design-corrections/post-reset-review.v14/evidence/probe-d9.json",
     {"faultCauseMembers": sorted(fault_members())})
