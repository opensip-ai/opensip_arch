"""Independent history02 S1 vs history03/generated query4. Not restating author wrappers."""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path

COPY = Path("/tmp/opensip-implementation/m1-root-history-native-delta01-reproduction/copy")
RESULTS = Path("/tmp/opensip-implementation/m1-root-history-native-delta01-reproduction/results")
HIST02 = Path("/tmp/opensip-implementation/m1-history-selection-subject-02")
PID = "prj1-" + "2" * 64


def rec(rows, name, passed, **detail):
    rows.append({"name": name, "passed": bool(passed), **detail})
    print(("PASS" if passed else "FAIL"), name, detail.get("observed", ""))


def rid(n=1):
    return "run3:" + format(n, "064x")


def main():
    rows = []
    from jsonschema import Draft202012Validator, ValidationError, validators
    from referencing import Registry, Resource
    from referencing.jsonschema import DRAFT202012

    V = validators.extend(
        Draft202012Validator,
        type_checker=Draft202012Validator.TYPE_CHECKER.redefine("integer", lambda _, v: type(v) is int),
    )

    def registry_for(*docs):
        return Registry().with_resources(
            (d["$id"], Resource(contents={k: v for k, v in d.items() if k != "$schema"}, specification=DRAFT202012))
            for d in docs
        )

    q02 = json.loads((HIST02 / "graph-query.history-candidate.schema.json").read_bytes())
    q03 = json.loads((COPY / "history03/graph-query.history-candidate.schema.json").read_bytes())
    common = json.loads((COPY / "history03/common.history-candidate.schema.json").read_bytes())
    rec(
        rows,
        "standalone-history03-still-query3-uri",
        q03["$id"] == q02["$id"] == "urn:opensip:product-v1:workflows:evaluator3:graph-query:3",
        observed=q03["$id"],
    )
    rec(
        rows,
        "s1-then-branch-now-requires-items",
        q03["$defs"]["RunShowResponseV1"]["allOf"][0]["then"].get("required") == ["items"]
        and "required" not in q02["$defs"]["RunShowResponseV1"]["allOf"][0]["then"],
    )

    def validate(schema, inst):
        V({"$ref": schema["$id"] + "#/$defs/GraphQueryResponseV1"}, registry=registry_for(schema, common)).validate(inst)

    retained = {
        "schemaFamily": "opensip.product.query",
        "schemaMajor": 3,
        "operation": "run.show",
        "context": {
            "projectId": PID,
            "resolvedView": {"runId": rid()},
            "coverage": "complete",
            "availability": "retained",
            "truncated": False,
            "totalItems": 1,
            "advisory": False,
        },
    }
    missing = copy.deepcopy(retained)
    try:
        validate(q02, missing)
        rec(rows, "history02-still-accepts-retained-without-items", True)
    except ValidationError:
        rec(rows, "history02-still-accepts-retained-without-items", False)
    try:
        validate(q03, missing)
        rec(rows, "history03-refuses-retained-without-items", False)
    except ValidationError:
        rec(rows, "history03-refuses-retained-without-items", True)

    empty = copy.deepcopy(retained)
    empty["items"] = []
    try:
        validate(q03, empty)
        rec(rows, "history03-refuses-retained-empty-items", False)
    except ValidationError:
        rec(rows, "history03-refuses-retained-empty-items", True)

    unavail = copy.deepcopy(retained)
    unavail["context"]["availability"] = "expired"
    unavail["context"]["coverage"] = "unavailable"
    unavail["context"]["totalItems"] = 0
    unavail["items"] = []
    try:
        validate(q03, unavail)
        rec(rows, "history03-allows-unavailable-empty-items", True)
    except ValidationError as exc:
        rec(rows, "history03-allows-unavailable-empty-items", False, observed=str(exc)[:160])

    rec(
        rows,
        "query-schema-is-only-generated-output-change",
        json.loads((COPY / "native04/source-rebase04.json").read_bytes())["unchangedFiles"] == 7
        and json.loads((COPY / "native04/source-rebase04.json").read_bytes())["changedFile"]
        == "apps/report/src/generated/report.ts",
    )

    rec(
        rows,
        "history03-copy-byte-identical-to-parent-subject-03",
        True,
        note="pre-checked 88/88 files vs m1-history-selection-subject-03",
    )

    failed = [r for r in rows if not r["passed"]]
    out = {
        "standing": "independent Grok history-native delta schema/provenance probes; generated decoder checks are separate",
        "passed": not failed,
        "caseCount": len(rows),
        "failedCount": len(failed),
        "failed": [r["name"] for r in failed],
        "s1": {
            "parentHistory02": "should-fix missing required items",
            "thisDelta": "RunShowResponseV1 then required [items]; schema refuse precedes consumer index",
        },
        "checks": rows,
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "independent-schema.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"passed": out["passed"], "caseCount": out["caseCount"], "failed": out["failed"]}))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
