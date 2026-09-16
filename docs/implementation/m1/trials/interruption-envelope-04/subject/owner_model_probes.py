"""Run pinned owner functions with exactly the declared cancellation successor.

Extracts the existing pure functions and constants, rather than executing its
filesystem import shim. The owner supplies synthetic already-admitted results;
this is workflow behavior evidence, not retained Run admission or host custody.
"""
import ast
import copy
import hashlib
import json
import types


def load_model(source, canonical):
    wanted = {"Refusal", "terminate", "dd", "analysis_termination", "comparison_termination", "exit_code", "validate_dag",
              "raw_sha", "synthetic_execution_id", "_exec_id", "run_invocation"}
    tree = ast.parse(source)
    nodes = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)) and node.name in wanted:
            nodes.append(node)
        elif isinstance(node, ast.Assign):
            names = {t.id for t in node.targets if isinstance(t, ast.Name)}
            if names & wanted or (names and all(n.isupper() for n in names)
                                   and not any(isinstance(n, ast.Call) for n in ast.walk(node.value))):
                nodes.append(node)
    model = types.ModuleType("scoped_workflow_owner")
    model.__dict__.update(hashlib=hashlib, json=json, canonical=canonical)
    exec(compile(ast.Module(body=nodes, type_ignores=[]), "pinned-workflow-owner#pure-extract", "exec"), model.__dict__)
    return model


def run(source, successor, ref, registry, schema, fixtures, join):
    assert hashlib.sha256(source).hexdigest() == successor["ownerSha256"]
    text = source.decode()
    span = successor["selector"]
    assert "\n".join(text.splitlines()[span["startLine"]-1:span["endLine"]]) == successor["before"]
    assert text.count(successor["before"]) == 1
    revised = text.replace(successor["before"], successor["after"])
    assert revised.replace(successor["after"], successor["before"]) == text
    original, current = load_model(text, ref), load_model(revised, ref)
    g = fixtures["deliveryGoldens"][24]["envelope"]
    rid, pid = g["requestId"], g["projectId"]
    invocation_id = "urn:opensip:product-v1:workflows:evaluator3:invocation:3"
    scenarios = [("default", ["analysis", "render"], ["required"] * 2),
                 ("fit", ["analysis", "query", "render"], ["required"] * 3),
                 ("candidates", ["query", "render"], ["required"] * 2),
                 ("two-analysis", ["analysis", "analysis", "render"], ["required"] * 3),
                 ("optional-analysis", ["analysis", "render"], ["optional", "required"]),
                 ("later-optional-analysis", ["analysis", "analysis", "render"], ["required", "optional", "required"]),
                 ("optional-after-settled-required", ["query", "analysis"], ["required", "optional"])]
    rows = []
    changed = 0
    for label, kinds, requirements in scenarios:
        for cut in range(len(kinds) + 1):
            for signal in ("SIGINT", "SIGTERM", "SIGHUP"):
                steps, script = [], {"cancelAt": {"stepId": cut, "signal": signal}}
                for i, (kind, requirement) in enumerate(zip(kinds, requirements)):
                    depends = [j for j in range(i) if requirements[j] == "required" or requirement == "optional"]
                    if kind == "analysis":
                        params = {"kind": kind, "profile": "fit" if label == "fit" else "default", "role": "primary",
                                  "durability": "authoritative", "snapshotSource": "live-worktree"}
                        result = copy.deepcopy(g["run"])
                        if i:
                            result["runId"] = "run3:" + "b" * 64
                    elif kind == "query":
                        request = copy.deepcopy(g["advisoryReport"]["request"])
                        params = {"kind": kind, "operation": request["operation"], "request": request,
                                  "completeness": request["completeness"], "page": request["page"]}
                        result = {"kind": "query", "items": 1, "truncated": False, "completenessMet": True, "advisory": True}
                    else:
                        params = {"kind": kind, "format": "json", "destination": "stdout", "sourceSteps": depends, "required": True}
                        result = {"kind": kind, "format": "json", "rendererVersion": 1, "bytes": 100, "truncation": False, "written": True}
                    steps.append({"stepId": i, "kind": kind, "requirement": requirement, "dependsOn": depends,
                                  "dependencyGate": "terminal" if kind == "render" else "completed", "retryPolicy": "none", "params": params})
                    script[str(i)] = [{"event": "completed", "result": result}]
                workflow = ({"kind": "builtin", "name": label} if label in ("default", "fit", "candidates")
                            else {"kind": "profile", "contributionId": "org.example.workflow", "activationId": "review", "profileVersion": "1.0.0"})
                base = {"schemaFamily": "opensip.product.invocation", "schemaMajor": 3, "requestId": rid, "projectId": pid,
                        "workflow": workflow, "mode": {"interactive": False, "ci": True, "ephemeral": False}, "orderedSteps": steps}
                before, old_exit = original.run_invocation(copy.deepcopy(base), copy.deepcopy(script))
                record, code = current.run_invocation(copy.deepcopy(base), copy.deepcopy(script))
                ref.validate({"$ref": invocation_id}, record, registry)
                assert before["stepResults"] == record["stepResults"] and old_exit == code
                difference = before["termination"] != record["termination"]
                if difference:
                    assert label in ("optional-analysis", "later-optional-analysis")
                    assert record["termination"]["class"] == "interrupted"
                    assert record["termination"]["signal"] == before["termination"]["signal"]
                    changed += 1
                envelope = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 6, "kind": "invocation",
                            "requestId": rid, "projectId": pid, "termination": copy.deepcopy(record["termination"]),
                            "exitCode": code, "invocation": copy.deepcopy(record)}
                # Exercise the new minimal form whenever lawful; otherwise keep
                # the complete admitted invocation without fabricating results.
                if code == 130 and "runId" not in record["termination"]:
                    envelope["kind"] = "failure"
                    envelope["errors"] = []
                    del envelope["invocation"]
                ref.validate({"$ref": schema["$id"]}, envelope, registry)
                assert join.validate_interruption_join(record, envelope)
                rows.append({"scenario": label, "cut": cut, "signal": signal, "exitCode": code,
                             "phase": record["cancellation"]["phase"], "runId": record["termination"].get("runId"),
                             "changedFromParent": difference, "accepted": True})
    assert changed == 6, ("expected only two optional-commit cuts times three signals", changed)
    return {"cases": rows, "changedOptionalCommitCases": changed, "stepResultsAndExitCodesUnchanged": True,
            "extraction": "pinned pure owner functions/constants; full model import shim not executed"}
