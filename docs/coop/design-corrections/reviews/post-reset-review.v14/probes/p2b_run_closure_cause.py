"""CB4-MUST-2, second half: the pairing must bind at RETAINED RUN CLOSURE, not only in the
producer helper, and RC-3 must survive."""
import copy, json, sys
sys.path.insert(0, "/tmp/opensip-design-corrections/post-reset-review.v14/probes")
from harness import CI, M, C, N, probe, emit

def run_with_entry(mutate, relation="references"):
    """Mutate the RETAINED coverage payload of a complete Run and re-close it. This is the
    path a verifier walks; a producer-only check would pass this and Run closure must not."""
    run, objects, blobs = CI.build(relation=relation, has_match=True, resolved=True)
    cov_key = next(k for k, (d, v) in objects.items() if d == "coverage")
    cov = copy.deepcopy(objects[cov_key][1])
    payload = C.parse(blobs[cov["payloadDigest"]])
    mutate(payload["entry"])
    cov["payloadDigest"] = CI.put_blob(blobs, payload)
    CI.rekey(objects, cov_key, cov, run)
    CI.resync_witness(objects, blobs, run); CI.resync_proof_refs(objects, blobs, run)
    return M.close_run(run, objects, blobs)

probe("B15-positive-an-untouched-run-still-closes", "positive",
      lambda: M.close_run(*CI.build(relation="references", has_match=True, resolved=True)))

# RC-3: `complete` coverage with an `incomplete` resolution state and NO deficiency is an
# honest entry and must remain admissible - the registry says forcing a deficiency out of
# entry evidence would refuse lawful Runs. ATTEMPT 1 hand-mutated the state and was refused
# by RC-2 ("incomplete needs >=1 edge"), which is RC-2 doing its job on MY malformed entry;
# the lawful shape carries a real admitted unresolved-edge fact, so it is built rather than
# forged.
def rc3_run():
    return M.close_run(*CI.build(relation="references", has_match=True, resolved=True,
                                 unresolved_edges=["computed-member-access"]))
probe("B16-positive-RC-3-complete-with-incomplete-state-and-no-deficiency-is-lawful",
      "positive", rc3_run)

def rc3_entry_state():
    run, objects, blobs = CI.build(relation="references", has_match=True, resolved=True,
                                   unresolved_edges=["computed-member-access"])
    view = next(v for d, v in objects.values() if d == "view")
    for cid in view["coverageIds"]:
        cov = objects[cid][1]; e = C.parse(blobs[cov["payloadDigest"]])["entry"]
        if e["relation"] == "references":
            return (e["coverage"] == "complete" and e["deficiency"] is None
                    and e["resolutionCompleteness"]["state"] == "incomplete"
                    and e["resolutionCompleteness"]["unresolvedEdgeCount"] == 1)
    return False
probe("B16b-the-RC-3-entry-really-is-complete-incomplete-and-deficiency-free", "check",
      rc3_entry_state)

# The set-valued carrier really is a SET: several classes at once, each backed by its own
# admitted unresolved-edge fact. This is the claim that justified naming a carrier instead
# of adding enum members, so it is exercised rather than accepted.
def multi_class_run():
    return M.close_run(*CI.build(relation="references", has_match=True, resolved=True,
                                 unresolved_edges=["computed-member-access",
                                                   "dynamic-import-nonliteral"]))
probe("B16c-positive-the-set-valued-carrier-holds-several-classes-at-once", "positive",
      multi_class_run)

def relabelled(e):
    e["deficiency"] = "resolution-incomplete"; e["nativeCause"] = "capability-missing"
probe("B17-negative-a-relabelled-cause-is-refused-at-retained-run-closure", "negative",
      lambda: run_with_entry(relabelled), "native.coverage-cause")

def borrowed_scalar(e):
    e["deficiency"] = "resolution-incomplete"; e["nativeCause"] = "lockfile-missing"
probe("B18-negative-a-borrowed-scalar-cause-is-refused-at-retained-run-closure", "negative",
      lambda: run_with_entry(borrowed_scalar), "native.coverage-cause")

def dpu_on_references(e):
    e["deficiency"] = "derivation-policy-unmet"; e["nativeCause"] = None
    e["derivationKinds"] = ["compiler-inferred"]
probe("B19-negative-derivation-policy-unmet-outside-types-refused-at-run-closure", "negative",
      lambda: run_with_entry(dpu_on_references, relation="references"),
      "native.coverage-cause-relation-not-in-scope")

def cause_without_deficiency(e):
    e["deficiency"] = None; e["nativeCause"] = "lockfile-missing"
probe("B20-negative-a-cause-without-a-deficiency-refused-at-run-closure", "negative",
      lambda: run_with_entry(cause_without_deficiency),
      "native.coverage-cause-without-deficiency")

# `null` is no longer an escape: a must-be-null row whose named carrier does NOT carry the
# cause is refused rather than silently passing on the null.
def null_but_carrier_says_complete(e):
    e["deficiency"] = "resolution-incomplete"; e["nativeCause"] = None
    e["resolutionCompleteness"]["state"] = "complete"
probe("B21-negative-null-cause-with-a-carrier-that-does-not-carry-it-refuses", "negative",
      lambda: run_with_entry(null_but_carrier_says_complete),
      "native.coverage-cause-carrier-unsupported")

emit("/tmp/opensip-design-corrections/post-reset-review.v14/evidence/probe-cb4-must-2-closure.json")
