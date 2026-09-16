"""Probe: establish the ACTUAL authoritative ordering for a cell row's cross-source primary pair.

Reads the real schema order annotations and the real capability-matrix relation arrays. Does not
guess lexical order. Writes nothing outside this runtime.
"""
import importlib.util
import json
import re
from pathlib import Path

SRC = Path("/tmp/opensip-design-corrections/execution-account-successor.v1/source/docs/coop/design-corrections")
F = SRC / "foundation"


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


M = load("q1_model", F / "execution_inputs_model.v1.py")
out = {}

# 1. Execution-inputs schema order annotations on the arrays that feed the row.
schema = json.loads((F / "execution-inputs.schema.v1.json").read_text())
top = schema["properties"]
cell = schema["$defs"]["CellProgramOutcomeV1"]["properties"]
out["schemaOrders"] = {
    "ExecutionInputsV1.cellOutcomes": top["cellOutcomes"].get("x-opensip-order"),
    "ExecutionInputsV1.nativeCoverageAccounts": top["nativeCoverageAccounts"].get("x-opensip-order"),
    "ExecutionInputsV1.candidateResultRefs": top["candidateResultRefs"].get("x-opensip-order"),
    "CellProgramOutcomeV1.inventoryDigests": cell["inventoryDigests"].get("x-opensip-order"),
    "CellProgramOutcomeV1.viewDigests": cell["viewDigests"].get("x-opensip-order"),
    "NativeCoverageAccountV1.coverageIds":
        schema["$defs"]["NativeCoverageAccountV1"]["properties"]["coverageIds"].get("x-opensip-order"),
}

# 2. Capability matrix: is `relations` array order authored or incidental? Is it lexical?
matrix = json.loads((SRC / "native/native-capability-matrix.v2.json").read_text())
rows = []
for cap in matrix["capabilities"]:
    rels = cap.get("relations") or []
    as_is = [tuple(r) for r in rels]
    lexical = sorted(as_is)
    rows.append({
        "capabilityId": cap["id"],
        "relationsAsAuthored": [list(r) for r in as_is],
        "equalsLexical": as_is == lexical,
        "hasOwnOrderAnnotation": any(k.startswith("x-opensip-order") for k in cap),
    })
out["matrixRelations"] = rows
out["anyMatrixRelationArrayIsNotLexical"] = any(not r["equalsLexical"] for r in rows)
out["matrixHasAnyXOpensipOrder"] = bool(re.search(r'"x-opensip-order"', json.dumps(matrix)))

# 3. Where does _matrix_pairs read from, and does the model's owed loop use it?
out["matrixPairsSource"] = "native-capability-matrix.v2.json#/capabilities[id==cap]/relations, array order as authored"
out["matrixPairsSample"] = {c: M._matrix_pairs(c) for c in
                            ("inventory", "syntax", "clones-fact", "references", "imports")}

# 4. Is there any published statement in the matrix about relation array order?
text = json.dumps(matrix)
hits = []
for kw in ("order", "ordinal", "sequence", "canonical-set", "sorted"):
    for m in re.finditer(kw, text, re.I):
        seg = text[max(0, m.start() - 160):m.start() + 160]
        hits.append({"keyword": kw, "context": seg})
out["matrixOrderKeywordHitCount"] = len(hits)
out["matrixOrderKeywordSample"] = hits[:6]

# 5. Relation registry: does it declare an order over relations?
rel_reg = json.loads((F / "relation-payload-schemas.v2.json").read_text())["x-opensip-relation-registry"]
out["relationRegistryKeys"] = sorted(rel_reg)
out["relationRegistryOrderLaw"] = {
    k: v for k, v in rel_reg.items() if "order" in k.lower() or "Law" in k
}
out["relationRegistryRelationKeysAreDict"] = isinstance(rel_reg.get("relations"), dict)

print(json.dumps(out, indent=2, default=str))
