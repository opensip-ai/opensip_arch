"""Independent TIM-F1–F4 probes against workflow-timing02. Not a restatement of check.py."""
from __future__ import annotations

import hashlib
import json
import types
from pathlib import Path

COPY = Path("/tmp/opensip-implementation/m1-grok-workflow-timing-review-02/review/copy")
RESULTS = Path("/tmp/opensip-implementation/m1-grok-workflow-timing-review-02/review/results")
SUBJ01 = Path("/tmp/opensip-implementation/m1-workflow-timing-subject-01")
JOINT13 = Path("/tmp/opensip-implementation/m1-report-joint-candidate-13/composed-sources/invocation-record.proposed.schema.json")


def rec(rows, name, passed, **detail):
    rows.append({"name": name, "passed": bool(passed), **detail})
    print(("PASS" if passed else "FAIL"), name, detail.get("observed", ""))


def load(path, name):
    m = types.ModuleType(name)
    m.__file__ = str(path)
    exec(compile(Path(path).read_bytes(), str(path), "exec"), m.__dict__)
    return m


def main():
    rows = []
    T = load(COPY / "timing.py", "timing")
    T01 = load(SUBJ01 / "timing.py", "timing01")
    schema = json.loads((COPY / "invocation-record.v4.schema.json").read_bytes())
    pins = json.loads((COPY / "input-pins.json").read_bytes())["files"]
    common = json.loads(Path(pins[3]["path"]).read_bytes())
    report = json.loads(Path(pins[4]["path"]).read_bytes())
    from jsonschema import Draft202012Validator, validators
    from referencing import Registry, Resource

    V = validators.extend(
        Draft202012Validator,
        type_checker=Draft202012Validator.TYPE_CHECKER.redefine("integer", lambda _, v: type(v) is int),
    )
    registry = Registry().with_resources([(x["$id"], Resource.from_contents(x)) for x in (schema, common)])
    attempt_v = V({"$ref": schema["$id"] + "#/$defs/Attempt"}, registry=registry)

    def attempt(outcome, duration):
        return {"executionId": "exec1_" + "1" * 32, "outcome": outcome, "observedDuration": duration}

    measured = {"state": "measured", "milliseconds": 0}
    lost = T.unavailable("supervisor-lost")
    clock = T.unavailable("clock-unavailable")
    rec(
        rows,
        "tim-f1-abandoned-measured-invalid",
        attempt_v.is_valid(attempt("abandoned", measured)) is False,
    )
    rec(
        rows,
        "tim-f1-completed-supervisor-lost-invalid",
        attempt_v.is_valid(attempt("completed", lost)) is False,
    )
    rec(
        rows,
        "tim-f1-abandoned-clock-unavailable-invalid",
        attempt_v.is_valid(attempt("abandoned", clock)) is False,
    )
    rec(
        rows,
        "tim-f1-abandoned-supervisor-lost-and-completed-measured-valid",
        attempt_v.is_valid(attempt("abandoned", lost)) and attempt_v.is_valid(attempt("completed", measured)),
    )

    def refused(fn):
        try:
            fn()
            return False
        except T.TimingRefusal:
            return True

    rec(
        rows,
        "tim-f2-malformed-none-pairs-are-admission-errors",
        refused(lambda: T.observe_terminal("completed", None, 4.0))
        and refused(lambda: T.observe_terminal("completed", "0", None))
        and refused(lambda: T.observe_terminal("completed", True, None)),
    )
    rec(
        rows,
        "historical-subject01-none-float-was-clock-unavailable",
        T01.observe_terminal("completed", None, 4.0) == T.unavailable("clock-unavailable"),
        note="original TIM-F2; not this freeze",
    )
    rec(
        rows,
        "tim-f2-true-missing-samples-are-clock-unavailable",
        T.observe_terminal("failed", None, 10) == T.unavailable("clock-unavailable")
        and T.observe_terminal("failed", 10, None) == T.unavailable("clock-unavailable"),
    )

    bogus = [{"state": "bogus"}]
    rec(rows, "tim-f3-bogus-projection-is-timing-refusal-not-keyerror", refused(lambda: T.summarize_attempts(bogus)))
    value = {
        "executionId": "exec1_" + "1" * 32,
        "sourceSchemaMajor": 4,
        "outcome": "completed",
        "duration": {"state": "measured", "milliseconds": 1},
    }
    rec(rows, "tim-f3-duplicate-execution-ids-refused", refused(lambda: T.summarize_attempts([value, value])))
    rec(
        rows,
        "tim-f3-negative-milliseconds-refused",
        refused(lambda: T.summarize_attempts([dict(value, duration={"state": "measured", "milliseconds": -1})])),
    )
    rec(
        rows,
        "tim-f3-unique-bounded-sum",
        T.summarize_attempts(
            [
                dict(value, executionId="exec1_" + format(1, "032x"), duration={"state": "measured", "milliseconds": 3}),
                dict(value, executionId="exec1_" + format(2, "032x"), duration={"state": "measured", "milliseconds": 8}),
            ]
        )
        == {"state": "measured", "attemptCount": 2, "milliseconds": 11},
    )

    rec(
        rows,
        "tim-f4-major-1-is-owned-incompatible-before-decode",
        T.source_support(1) == {"state": "incompatible", "reason": "retained-schema-major-unsupported"}
        and V(report["$defs"]["PanelNotPresentV1"]["oneOf"][3]).is_valid(T.source_support(1)),
    )
    rec(
        rows,
        "tim-f4-project-attempt-does-not-decode-unsupported-major",
        refused(lambda: T.project_attempt(1, {"executionId": "exec1_" + "1" * 32, "outcome": "completed"})),
    )
    try:
        T01.project_attempt(1, {"executionId": "exec1_" + "1" * 32, "outcome": "completed"})
        rec(rows, "historical-subject01-major-1-was-unowned-refusal", False)
    except T01.TimingRefusal:
        rec(rows, "historical-subject01-major-1-was-unowned-refusal", "source_support" not in Path(SUBJ01 / "timing.py").read_text())

    rec(
        rows,
        "render-in-progress-named-in-pinned-report-ledger",
        "render-in-progress" in json.dumps(report["$defs"])
        and "render-in-progress" in Path(COPY / "contract.md").read_text(),
    )

    rec(
        rows,
        "zero-is-measured-not-fallback",
        T.observe_terminal("completed", 0, 999999) == {"state": "measured", "milliseconds": 0},
    )

    freeze_hash = hashlib.sha256((COPY / "invocation-record.v4.schema.json").read_bytes()).hexdigest()
    joint_hash = hashlib.sha256(JOINT13.read_bytes()).hexdigest() if JOINT13.is_file() else None
    rec(
        rows,
        "joint13-invocation5-is-later-composition-not-this-freeze",
        freeze_hash == "814b61bd0c25045f6a3625eea136f9e55ac1968e2176007149b4b2ac789a1c89"
        and joint_hash is not None
        and joint_hash != freeze_hash,
        observed={"freeze": freeze_hash, "joint13": joint_hash},
    )

    failed = [r for r in rows if not r["passed"]]
    out = {
        "standing": "independent Grok workflow-timing02 probes; no clocks/journal/report ledger custody",
        "passed": not failed,
        "caseCount": len(rows),
        "failedCount": len(failed),
        "failed": [r["name"] for r in failed],
        "findingDispositions": {
            "TIM-F1": "corrected-in-this-freeze-Attempt-allOf",
            "TIM-F2": "corrected-in-this-freeze-type-before-none",
            "TIM-F3": "corrected-in-this-freeze-admit-unique-nonnegative",
            "TIM-F4": "corrected-in-this-freeze-source_support-before-decode",
        },
        "checks": rows,
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "independent-timing.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"passed": out["passed"], "caseCount": out["caseCount"], "failed": out["failed"]}))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
