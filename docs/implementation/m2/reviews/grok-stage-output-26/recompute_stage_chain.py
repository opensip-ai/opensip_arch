"""Replay check_stage26.py oracle setup against frozen requests. Read-only."""
from pathlib import Path
import ast
import json

T = Path("/tmp/opensip-implementation")
s = (T / "check_run_links19.py").read_text()
exec(s[: s.index("cases=[]")])  # noqa: S102 — same bootstrap as frozen generator
A = Path("/Users/sb/code/opensip-ai/opensip_arch")
R = A / "docs/implementation/m2/stage-meta-reference-selection-v1/reference"
IP = R / "identity_model.py"
tree = ast.parse(IP.read_bytes())
names = ["stage_output_schema_member_path", "admit_stage_output_schema"]
stage_env = {**I.__dict__, "HERE": R}
exec(
    compile(
        ast.Module(
            body=[n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name in names],
            type_ignores=[],
        ),
        str(IP),
        "exec",
    ),
    stage_env,
)
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
    env = {
        **I.__dict__,
        "objects": obs,
        "blobs": bs,
        "parsed": {},
        "admit_stage_output_schema": stage_env["admit_stage_output_schema"],
    }
    exec(code, env)
    env["walk"] = lambda *args: None
    get = env["get"]
    payload = env["payload"]
    if q["mode"] == "stage-output":
        spec = payload(q["specDigest"], "stage-spec")
        env["admit_stage_output_schema"](
            spec, get(spec["producerClosure"], "closure"), env["blob"](spec["outputSchemaDigest"])
        )
        return {"result": "checked"}
    run = get(q["runId"], "run")
    plan = get(run["planId"], "plan")
    seal = get(run["evaluationSealId"], "evaluation-seal")
    execution = get(seal["executionPlanId"], "execution-plan")
    analysis = payload(plan["analysisSpecDigest"], "analysis-spec")
    env.update(run=run, plan=plan, execution=execution, analysis_spec=analysis)
    exec(phase, env)
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


EXPORT = Path("/tmp/opensip-implementation/m2-stage-output-subject-26")
OUT = Path("/tmp/opensip-implementation/m2-grok-stage-output-review-26/review/results")
reqs = [json.loads(l) for l in (EXPORT / "stage-requests.ndjson").read_bytes().splitlines()]
frozen_exp = [json.loads(l) for l in (EXPORT / "stage-expected.ndjson").read_bytes().splitlines()]
frozen_act = [json.loads(l) for l in (EXPORT / "stage-actual.ndjson").read_bytes().splitlines()]
miss_exp = []
miss_act = []
checked = 0
for i, q in enumerate(reqs):
    got = mapped(q)
    if got.get("result") == "checked":
        checked += 1
    if got != frozen_exp[i]:
        miss_exp.append({"index": i, "label": q.get("label"), "got": got, "expected": frozen_exp[i]})
    if got != frozen_act[i]:
        miss_act.append({"index": i, "label": q.get("label"), "got": got, "actual": frozen_act[i]})
result = {
    "cases": len(reqs),
    "checked": checked,
    "vsFrozenExpectedMismatches": len(miss_exp),
    "vsFrozenActualMismatches": len(miss_act),
    "frozenActualVsExpected": sum(a != e for a, e in zip(frozen_act, frozen_exp)),
    "missExpSample": miss_exp[:8],
    "missActSample": miss_act[:8],
}
OUT.mkdir(parents=True, exist_ok=True)
(OUT / "stage-recompute.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result))
assert result["vsFrozenExpectedMismatches"] == 0
assert result["vsFrozenActualMismatches"] == 0
