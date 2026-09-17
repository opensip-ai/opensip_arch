"""Independent stage AST oracle over frozen requests using the selected identity_model."""
from pathlib import Path
import ast
import json
import importlib.util

EXPORT = Path("/tmp/opensip-implementation/m2-stage-output-subject-26")
REF = Path(
    "/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/stage-meta-reference-selection-v1/reference"
)
OUT = Path("/tmp/opensip-implementation/m2-grok-stage-output-review-26/review/results")
IP = REF / "identity_model.py"


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


I = load(IP, "selected_identity_model")
C = I.C
tree = ast.parse(IP.read_bytes())
body = next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == "open_run_closure").body
helpers = [
    n
    for n in body
    if isinstance(n, ast.FunctionDef) and n.name in ["get", "blob", "canonical_bytes", "payload"]
]
assert len(helpers) == 4
code = compile(ast.Module(body=helpers, type_ignores=[]), str(IP), "exec")
stages = [n for n in body if isinstance(n, ast.For) and ast.unparse(n.iter) == "execution['stages']"]
assert len(stages) == 1
phase = compile(ast.Module(body=stages, type_ignores=[]), str(IP), "exec")


def oracle(q):
    obs = {r["id"]: (r["domain"], r["descriptor"]) for r in q["objects"]}
    bs = {r["digest"]: bytes.fromhex(r["hex"]) for r in q["blobs"]}
    local = {**I.__dict__, "objects": obs, "blobs": bs, "parsed": {}, "HERE": REF}
    exec(code, local)
    local["walk"] = lambda *args: None  # local payload shim; not full walk
    get = local["get"]
    payload = local["payload"]
    if q["mode"] == "stage-output":
        spec = payload(q["specDigest"], "stage-spec")
        local["admit_stage_output_schema"](
            spec, get(spec["producerClosure"], "closure"), local["blob"](spec["outputSchemaDigest"])
        )
        return {"result": "checked"}
    run = get(q["runId"], "run")
    plan = get(run["planId"], "plan")
    seal = get(run["evaluationSealId"], "evaluation-seal")
    execution = get(seal["executionPlanId"], "execution-plan")
    analysis = payload(plan["analysisSpecDigest"], "analysis-spec")
    local.update(run=run, plan=plan, execution=execution, analysis_spec=analysis)
    exec(phase, local)
    return {"result": "checked", "stages": len(execution["stages"])}


def mapped(q):
    steps = q.get("steps")
    try:
        if steps == "0" or steps == 0:
            return {"result": "limit"}
        return oracle(q)
    except I.EvidenceUnavailable:
        return {"result": "unavailable"}
    except C.AdmissionError as exc:
        cause = str(exc)
        if cause.startswith("STAGE_OUTPUT_SCHEMA_OPERATION_NOT_A_PATH_SEGMENT"):
            cause = "STAGE_OUTPUT_SCHEMA_OPERATION_NOT_A_PATH_SEGMENT"
        if cause.startswith(("STAGE_", "CLOSURE_FIELD_KIND:stage-spec.")):
            return {"result": "refused", "cause": cause}
        return {"result": "invalid"}
    except (C.ValidationError, ValueError):
        return {"result": "invalid"}


reqs = [json.loads(l) for l in (EXPORT / "stage-requests.ndjson").read_bytes().splitlines()]
frozen_exp = [json.loads(l) for l in (EXPORT / "stage-expected.ndjson").read_bytes().splitlines()]
frozen_act = [json.loads(l) for l in (EXPORT / "stage-actual.ndjson").read_bytes().splitlines()]
miss_exp = []
miss_act = []
checked = 0
named_ops = 0
for i, q in enumerate(reqs):
    got = mapped(q)
    if got.get("result") == "checked":
        checked += 1
    if got != frozen_exp[i]:
        miss_exp.append({"index": i, "label": q.get("label"), "got": got, "expected": frozen_exp[i]})
    if got != frozen_act[i]:
        miss_act.append({"index": i, "label": q.get("label"), "got": got, "actual": frozen_act[i]})
    if frozen_act[i].get("cause") == "STAGE_OUTPUT_SCHEMA_OPERATION_NOT_A_PATH_SEGMENT":
        named_ops += 1
        assert ":" not in frozen_act[i]["cause"]
result = {
    "cases": len(reqs),
    "checked": checked,
    "vsFrozenExpectedMismatches": len(miss_exp),
    "vsFrozenActualMismatches": len(miss_act),
    "frozenActualVsExpected": sum(a != e for a, e in zip(frozen_act, frozen_exp)),
    "operationNamedCauseRows": named_ops,
    "missExpSample": miss_exp[:8],
    "missActSample": miss_act[:8],
}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "stage-recompute.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result))
assert result["vsFrozenExpectedMismatches"] == 0 and result["vsFrozenActualMismatches"] == 0
