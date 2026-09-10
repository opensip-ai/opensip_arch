"""Required-output failure after a committed Run: the strict parity access the delta
introduced must FAIL rather than silently render a partial result."""
import json, sys
sys.path.insert(0, "/tmp/opensip-design-corrections/post-reset-review.v14/probes")
from harness import CI, M, C, N, W, probe, emit

ROOT = "/tmp/opensip-design-corrections/post-reset-review.v14/work"
COMMON = json.load(open(ROOT + "/docs/coop/design-corrections/workflows/schemas/common.schema.json"))
INV = json.load(open(ROOT + "/docs/coop/design-corrections/workflows/command-inventory.v1.json"))

probe("H0-the-fault-cause-mapper-carries-the-successor-member", "check",
      lambda: W.D9_FAULT_CODES["host-invariant"] == "SYSTEM.OUTCOME.ILLEGAL_STATE"
      if hasattr(W, "D9_FAULT_CODES") else
      "host-invariant" in open(ROOT + "/docs/coop/design-corrections/workflows/"
                               "workflows_model.v1.py").read())
def _codes(root):
    import re
    src = open(root + "/docs/coop/design-corrections/workflows/workflows_model.v1.py").read()
    return dict(re.findall(r"'([a-z-]+)':\s*'([A-Z][A-Z0-9._]+)'", src))

NEWC = _codes(ROOT)
OLDC = _codes("/tmp/opensip-design-corrections/candidate-subject.v13")
probe("H1-every-inherited-fault-cause-mapping-is-preserved", "check",
      lambda: all(OLDC[k] == NEWC.get(k) for k in OLDC))
probe("H1b-the-vocabulary-grew-by-exactly-the-one-successor-member", "check",
      lambda: set(NEWC) - set(OLDC) == {"host-invariant"}
              and NEWC["host-invariant"] == "SYSTEM.OUTCOME.ILLEGAL_STATE")

# Strict parity access: a declared field missing from the envelope must RAISE.
def render_missing_field():
    cmds = INV["commands"]
    cmd = next(c for c in cmds if c.get("requestClass") == "analysis")
    fields = cmd["parityFields"]
    envelope = {"parity": {f: "x" for f in fields if f != fields[0]}}
    return W.render(cmd, envelope) if hasattr(W, "render") else None
probe("H2-negative-a-missing-declared-parity-field-fails-rather-than-rendering-partial",
      "negative", render_missing_field, "")

probe("H3-capability-availability-is-declared-parity-on-all-five-analysis-commands", "check",
      lambda: len([c for c in INV["commands"] if c.get("requestClass") == "analysis"]) == 5
              and all("capability-availability" in c["parityFields"]
                      for c in INV["commands"] if c.get("requestClass") == "analysis"))
probe("H4-the-delivery-fault-route-is-named-and-retains-a-committed-run", "check",
      lambda: "DELIVERY.REQUIRED_FAILED" in open(
          ROOT + "/docs/coop/design-corrections/workflows/workflows_model.v1.py").read()
          and "delivery-required" in COMMON["$defs"]["D9FaultCause"]["enum"])

emit("/tmp/opensip-design-corrections/post-reset-review.v14/evidence/probe-delivery.json")
