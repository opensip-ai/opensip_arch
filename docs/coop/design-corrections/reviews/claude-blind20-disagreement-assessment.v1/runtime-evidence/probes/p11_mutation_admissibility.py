"""Validate final20's retained mutation preimages against the PUBLISHED owning schema.

Two retained final20 artifacts publish a generic mutation-intent key. This admits each preimage
against MutationReplayScopeV1 with the frozen canonical keyword layer. READ-ONLY.
"""
import hashlib
import importlib.util
import json
from pathlib import Path

B = Path("/tmp/opensip-design-corrections")
S = B / "candidate-subject.v33"
DC = S / "docs/coop/design-corrections"
C20 = B / "consumer-b.v20"


def load(n, p):
    s = importlib.util.spec_from_file_location(n, p)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


C = load("canon11", DC / "foundation/canonical.py")


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


common = json.loads((DC / "workflows/schemas/common.schema.json").read_text())
inv = json.loads((DC / "workflows/schemas/invocation-record.schema.json").read_text())
scope_def = inv["$defs"]["MutationReplayScopeV1"]
# Inline the two referenced common defs so the schema is self-contained for validation.
defs = {"RequestId": common["$defs"]["RequestId"], "StepId": common["$defs"]["StepId"],
        "ProjectId": common["$defs"]["ProjectId"]}
inlined = json.loads(json.dumps(scope_def)
                     .replace("urn:opensip:product-v1:workflows:common#/$defs/", "#/$defs/"))
# `operation` $refs the repair schema; replace with a permissive string so the ID fields are what
# is being measured, not the operation vocabulary.
inlined["properties"]["operation"] = {"type": "string"}
schema = {"$defs": defs, "allOf": [{"$ref": "#/$defs/Scope"}]}
schema["$defs"]["Scope"] = inlined

out = {"standing": "READ-ONLY admissibility of final20's retained mutation preimages against the "
                   "published MutationReplayScopeV1. No mutation performed or authorized.",
       "publishedRequestId": defs["RequestId"], "publishedStepId": defs["StepId"],
       "commonSchemaSha256": sha(DC / "workflows/schemas/common.schema.json"),
       "invocationRecordSha256": sha(DC / "workflows/schemas/invocation-record.schema.json")}

cases = []
mk_path = C20 / "output/vectors/mutation-keys.json"
mk = json.loads(mk_path.read_text())
for name in ("genericMutation", "importStep", "nativePreparationStep"):
    row = mk.get(name) or {}
    pre = row.get("preimage")
    if not isinstance(pre, dict):
        continue
    try:
        C.validate(schema, pre)
        verdict, err = "ADMIT", None
    except Exception as exc:  # noqa: BLE001
        verdict, err = "REFUSE", str(exc).splitlines()[0][:200]
    cases.append({"artifact": "output/vectors/mutation-keys.json", "artifactSha256": sha(mk_path),
                  "entry": name, "requestId": pre.get("requestId"), "stepId": pre.get("stepId"),
                  "declaredKey": row.get("key"), "schemaVerdict": verdict, "firstError": err})

ims_path = C20 / "output/vectors/indep-mutation-surface.json"
ims = json.loads(ims_path.read_text())
raws = ims.get("rawRecords") or {}
found = []


def walk(node, path=""):
    if isinstance(node, dict):
        if {"requestId", "stepId", "projectId", "operation"} <= set(node):
            found.append((path, node))
        for k, v in node.items():
            walk(v, path + "/" + k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, path + "/" + str(i))


walk(raws, "rawRecords")
for path, pre in found:
    probe = {k: pre[k] for k in ("schemaVersion", "requestId", "stepId", "projectId", "operation")
             if k in pre}
    try:
        C.validate(schema, probe)
        verdict, err = "ADMIT", None
    except Exception as exc:  # noqa: BLE001
        verdict, err = "REFUSE", str(exc).splitlines()[0][:200]
    cases.append({"artifact": "output/vectors/indep-mutation-surface.json",
                  "artifactSha256": sha(ims_path), "entry": path,
                  "requestId": probe.get("requestId"), "stepId": probe.get("stepId"),
                  "schemaVerdict": verdict, "firstError": err})

out["cases"] = cases
out["admitCount"] = sum(1 for c in cases if c["schemaVerdict"] == "ADMIT")
out["refuseCount"] = sum(1 for c in cases if c["schemaVerdict"] == "REFUSE")
out["measuredKeysInNewProbe"] = ims.get("measuredKeys")
out["declaredKeyInOlderVector"] = (mk.get("genericMutation") or {}).get("key")
out["twoRetainedArtifactsPublishDifferentGenericKeys"] = (
    (ims.get("measuredKeys") or {}).get("genericMutationIntent")
    != (mk.get("genericMutation") or {}).get("key"))
print(json.dumps(out, indent=2, default=str))
