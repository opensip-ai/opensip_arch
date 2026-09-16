"""Compare v3.admit_policy_rule vs walk_atoms+admit_atom(atom, rid). Not product code."""
from __future__ import annotations

import importlib.util
import json
import traceback
from pathlib import Path

V3 = Path(
    "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/workflows/workflows_model.v3.py"
)


def load_v3():
    spec = importlib.util.spec_from_file_location("wf_v3_probe", V3)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def catch(fn):
    try:
        fn()
        return {"ok": True}
    except Exception as e:
        return {
            "ok": False,
            "type": type(e).__name__,
            "msg": str(e)[:400],
            "detail": getattr(e, "detail", None),
        }


def rule(rel, rung, sk, evidence=None, evidence_use=None, endpoint="source"):
    atom = {
        "op": "exists",
        "relation": rel,
        "minResolution": rung,
        "filters": [],
        "endpoint": endpoint,
    }
    if evidence is not None:
        atom["evidence"] = evidence
    return {
        "ruleId": "r1",
        "ruleProgramRef": {
            "contributionId": "c" * 32 if False else "aaaaaaaa-bbbb-4ccc-8ddd-eeeeeeeeeeee",
            "ruleStableId": "stable-r1",
            "semanticsMajor": 1,
            "programDigest": "0" * 64,
        },
        "enabled": True,
        "severity": "error",
        "gate": True,
        "subjectEnumeration": {
            "universe": "native.semantic-universe.syntax.v2",
            "subjectKind": sk,
        },
        "emitWhen": atom,
        "evidenceUse": evidence_use or [],
    }


def main():
    W = load_v3()
    out = {
        "first_kind_file": None,
        "first_kind_runtime": None,
        "first_kind_test_execution": None,
    }
    # registry order
    reg = W.ATOM_REGISTRY["relations"]
    for name in ("file", "runtime-observation", "test-execution", "calls"):
        row = reg[name]
        kinds = row.get("sourceSubjectKinds", [row.get("sourceSubjectKind")])
        out[f"registry_{name}_kinds"] = kinds

    cases = [
        ("file_enumerated_sk_file", rule("file", "enumerated", "file")),
        ("file_enumerated_sk_symbol", rule("file", "enumerated", "symbol")),
        ("runtime_obs_sk_symbol", rule("runtime-observation", "observed", "symbol", "runtime", [{"kind": "runtime", "requirement": "required"}])),
        ("runtime_obs_sk_file", rule("runtime-observation", "observed", "file", "runtime", [{"kind": "runtime", "requirement": "required"}])),
        ("test_exec_sk_package", rule("test-execution", "observed", "package", "test", [{"kind": "test", "requirement": "optional"}])),
        ("calls_sk_symbol", rule("calls", "resolved-callee", "symbol")),
        ("calls_target_sk_symbol", rule("calls", "resolved-callee", "symbol", endpoint="target")),
    ]
    results = {}
    for name, r in cases:
        pol = catch(lambda r=r: W.admit_policy_rule(r))
        prog = catch(
            lambda r=r: W.walk_atoms(
                r["emitWhen"], lambda atom, rid=r["ruleId"]: W.admit_atom(atom, rid)
            )
        )
        results[name] = {
            "policy": pol,
            "program_subject_kind_none": prog,
            "policy_sk": r["subjectEnumeration"]["subjectKind"],
            "differ": pol != prog,
        }
    out["cases"] = results
    print(json.dumps(out, indent=2, default=str))


if __name__ == "__main__":
    main()
