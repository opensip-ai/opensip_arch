from pathlib import Path
import importlib.util, json, hashlib, copy, ast
from referencing import Registry, Resource
from jsonschema import Draft202012Validator, validators

B = Path("/tmp/opensip-implementation/m2-grok-exact-schema-profile-selection-v1-review/review/subject")
A = Path("/Users/sb/code/opensip-ai/opensip_arch")
PROD = Path("/tmp/opensip-implementation/m1-combined-corrections-subject-01/product")
OUT = Path("/tmp/opensip-implementation/m2-grok-exact-schema-profile-selection-v1-review/review/evidence")
OUT.mkdir(parents=True, exist_ok=True)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


N = load("new_exact", B / "canonical.py")
O = load("old_exact", A / "docs/coop/design-corrections/foundation/canonical.py")
results = []


def add(name, passed):
    results.append({"id": name, "passed": bool(passed)})
    assert passed, name


D = N.DIALECT
root = {"$id": "urn:probe", "$schema": D, "x-opensip-order": "numeric"}
mid = {"$id": "urn:mid", "$schema": D, "$ref": "urn:probe#"}
defs = {"$id": "urn:defs", "$schema": D, "$defs": {"nums": {"x-opensip-order": "numeric"}}}
docs = [root, mid, defs]
before = copy.deepcopy(docs)
raws = [json.dumps(d).encode() for d in docs]
stock = Registry().with_resources((d["$id"], Resource.from_contents(d)) for d in docs)
helper = N.exact_registry(docs)
for mode, registry in [("full-resources", stock), ("helper-resources", helper)]:
    for route, schema in [
        ("direct", root),
        ("wrapped", {"$ref": "urn:probe#"}),
        ("nested", {"$ref": "urn:mid#"}),
        ("fragment", {"$ref": "urn:defs#/$defs/nums"}),
    ]:
        for label, value, expected in [("valid", [0, 1], True), ("bool", [1, True], False), ("order", [2, 1], False)]:
            add(
                mode + "-" + route + "-" + label,
                N.ExactValidator(schema, registry=registry).is_valid(value) == expected,
            )
add("old-wrapper-gap-observed", O.ExactValidator({"$ref": "urn:probe#"}, registry=stock).is_valid([1, True]))
add("exact-registry-input-unchanged", docs == before and raws == [json.dumps(d).encode() for d in docs])
add("stock-global-dispatch-unchanged", validators.validator_for({"$schema": D}) is Draft202012Validator)
add("direct-xmax-annotation-stays-ignored", N.ExactValidator({"type": "string", "x-maxUtf8Bytes": 1}).is_valid("😀"))
for law in [{"const": 1}, {"enum": [1]}, {"type": "integer"}]:
    doc = {"$schema": D, "$id": "urn:exact", **law}
    reg = Registry().with_resource(doc["$id"], Resource.from_contents(doc))
    v = N.ExactValidator({"$ref": "urn:exact#"}, registry=reg)
    add("custom-" + next(iter(law)) + "-preserved", not v.is_valid(True) and v.is_valid(1) and not v.is_valid(1.0))
for schema in [
    {"$schema": "https://example.invalid/dialect"},
    {"not": {"$schema": "https://example.invalid/dialect"}},
    {"anyOf": [{"$schema": "https://example.invalid/dialect"}, True]},
]:
    try:
        N.ExactValidator(schema).is_valid(0)
    except N.AdmissionError as e:
        add("dialect-fault-not-instance-false-" + str(len(results)), str(e) == "UNREGISTERED_SCHEMA_DIALECT")
    else:
        add("dialect-fault-not-instance-false", False)
for docs in [
    [root, root],
    [{"$id": "", "type": "integer"}],
    [{"$id": "urn:bad#x"}],
    [{"$id": "urn:bad", "$schema": "https://example.invalid/dialect"}],
]:
    try:
        N.exact_registry(docs)
    except N.AdmissionError:
        add("registry-invalid-" + str(len(results)), True)
    else:
        add("registry-invalid", False)
try:
    N.ExactValidator({"$ref": "https://example.invalid/missing"}, registry=helper).validate(0)
except Exception as e:
    add("closed-registry-missing-no-fetch", type(e).__name__ == "_WrappedReferencingError")
else:
    add("closed-registry-missing-no-fetch", False)
oldtree = ast.parse((A / "docs/coop/design-corrections/foundation/canonical.py").read_text())
newtree = ast.parse((B / "canonical.py").read_text())
functions = {n.name: n for n in newtree.body if isinstance(n, ast.FunctionDef)}
for f in oldtree.body:
    if isinstance(f, ast.FunctionDef) and f.name != "validate":
        add(
            "unchanged-function-" + f.name,
            ast.dump(f, include_attributes=False) == ast.dump(functions[f.name], include_attributes=False),
        )
sourcepins = json.loads(Path("/tmp/opensip-implementation/m2-schema-engine-trial-01/schema-source-pins.json").read_bytes())
for row in sourcepins:
    p = PROD / row["path"]
    add(
        "unchanged-raw-" + p.name,
        hashlib.sha256(p.read_bytes()).hexdigest() == row["sha256"] and json.loads(p.read_bytes())["$schema"] == D,
    )
record = {
    "standing": "private retarget of unit helper; not product integration",
    "tests": len(results),
    "passed": sum(r["passed"] for r in results),
    "results": results,
    "frozenCanonicalUnchanged": hashlib.sha256(
        (A / "docs/coop/design-corrections/foundation/canonical.py").read_bytes()
    ).hexdigest()
    == "d47f25db0fb09ceb84282a89fdf74055cb81ccb9de26f85a5a70b032b9a6b442",
}
(OUT / "retargeted-result.json").write_text(json.dumps(record, indent=2) + "\n")
print(record["tests"], "checks passed", record["passed"])
