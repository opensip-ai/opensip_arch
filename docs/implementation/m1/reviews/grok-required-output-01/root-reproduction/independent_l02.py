"""Independent L02 required-output01 probes. Not a restatement of check.py."""
from __future__ import annotations

import copy
import hashlib
import json
import types
from pathlib import Path

COPY = Path("/tmp/opensip-implementation/m1-root-required-output01-reproduction/copy")
RESULTS = Path("/tmp/opensip-implementation/m1-root-required-output01-reproduction/results")
FROZEN = Path("/tmp/opensip-implementation/m1-required-output-subject-01")
JOINT12 = Path("/tmp/opensip-implementation/m1-report-joint-candidate-12")
JOINT10_REVIEW = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/reviews/grok-report-joint-10/review.json")


def rec(rows, name, passed, **detail):
    rows.append({"name": name, "passed": bool(passed), **detail})
    print(("PASS" if passed else "FAIL"), name, detail.get("observed", ""))


def load(name, path):
    m = types.ModuleType(name)
    m.__file__ = str(path)
    exec(compile(Path(path).read_bytes(), str(path), "exec"), m.__dict__)
    return m


class Writer:
    def __init__(self, limit=None, flush_fault=False, max_write=None, progress=None):
        self.data = bytearray()
        self.limit = limit
        self.flush_fault = flush_fault
        self.max_write = max_write
        self.progress = progress
        self.calls = 0
        self.flushes = 0

    def write(self, raw):
        self.calls += 1
        if self.progress is not None:
            return self.progress
        count = len(raw) if self.max_write is None else min(len(raw), self.max_write)
        if self.limit is not None:
            if len(self.data) >= self.limit:
                raise OSError("/secret/path caller-token must never reach diagnostic")
            count = min(count, self.limit - len(self.data))
        self.data.extend(raw[:count])
        return count

    def flush(self):
        self.flushes += 1
        if self.flush_fault:
            raise OSError("private flush /tmp/secret")


def main():
    rows = []
    F = load("required_output_reference", COPY / "output_finalization.py")
    R = load("report08_reference", COPY / "owner/report_model.py")
    D = load("d9_required_output_owner", COPY / "owner/d9/check-d9-v1.14.py")
    CONTRACT = json.loads((COPY / "owner/d9/d9-exit-contract.v1.14.json").read_bytes())
    goldens = next(
        v
        for k, v in CONTRACT.items()
        if isinstance(v, list) and any(isinstance(r, dict) and r.get("id") == "machine-output-serialization-failed" for r in v)
    )
    GOLDEN = next(r for r in goldens if r.get("id") == "machine-output-serialization-failed")
    FAULT = dict({"class": D.derive_class(GOLDEN["scenarioAxes"])}, **D.derive_codes(GOLDEN["scenarioAxes"], CONTRACT["codeMaps"]))
    EXITS = CONTRACT["classToExitCode"]

    rec(
        rows,
        "d9-fault-derived-not-hand-copied",
        FAULT == GOLDEN["expectedTermination"] == {"class": "operational-failed", "errorCode": "OUTPUT.SERIALIZATION_FAILED"}
        and GOLDEN["scenarioAxes"]["interruption"] == "none"
        and GOLDEN["scenarioAxes"]["faultCause"] == "output-serialization"
        and GOLDEN["hostFinalizationProjection"]["preservesSettledRun"] is True
        and EXITS["operational-failed"] == 4
        and EXITS["interrupted"] == 130,
        observed=FAULT,
    )

    rec(
        rows,
        "v114-parity-invariant-still-success-only",
        next(i["text"] for i in CONTRACT["invariants"] if i["id"] == "invariant-envelope-parity")
        == "For finite CLI commands, CommandEnvelope.termination equals process termination when serialization succeeds.",
    )

    v15 = json.loads((JOINT12 / "composed-owners/d9-exit-contract.proposed.v1.15.json").read_bytes())
    rec(
        rows,
        "later-v115-clarification-is-not-this-freeze",
        "If required output fails" in next(i["text"] for i in v15["invariants"] if i["id"] == "invariant-envelope-parity")
        and not (COPY / "owner/d9/d9-exit-contract.proposed.v1.15.json").exists()
        and not any(p.name.endswith("v1.15.json") for p in (COPY / "owner/d9").glob("*.json")),
    )

    contract_text = (COPY / "contract.md").read_text()
    rec(
        rows,
        "this-freeze-does-not-claim-original-criterion-met",
        "stronger prevention/representation alternatives are\nnot claimed to have been implemented" in contract_text
        or "stronger prevention/representation alternatives are not claimed" in contract_text.replace("\n", " "),
    )

    sel = json.loads((JOINT12 / "L02-policy-selection.json").read_bytes())
    pin_raw = JOINT10_REVIEW.read_bytes()
    rec(
        rows,
        "later-root-selected-complete-output-or-operational-failure",
        sel["status"] == "ROOT-POLICY-SELECTED-SOURCE-INTEGRATION-PENDING"
        and sel["oldCriterionMet"] is False
        and sel["oldCriterionSuperseded"] is True
        and sel["sourcePromoted"] is False
        and sel["productImplemented"] is False
        and hashlib.sha256(pin_raw).hexdigest() == sel["review"]["sha256"]
        and len(pin_raw) == sel["review"]["bytes"],
        observed=sel["status"],
    )

    hist = json.loads(
        Path("/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m1/audits/envelope-capacity-01/issue.json").read_bytes()
    )
    rec(
        rows,
        "historical-l02-original-criterion-preserved",
        hist["id"] == "RP-OBL-L02"
        and any("prevent non-representable selections before they become retained" in x for x in hist["requiredResolution"]),
    )

    def envelope(aggregate):
        return {
            "termination": copy.deepcopy(aggregate),
            "exitCode": EXITS[aggregate["class"]],
            "availability": {"requiredSelection": ["never-remove-this"]},
        }

    def deliver(aggregate, encoder=None, writer=None, diag=None, env=None):
        f = F.Finalizer(aggregate, FAULT, EXITS)
        w = Writer() if writer is None else writer
        d = Writer() if diag is None else diag
        source = envelope(aggregate) if env is None else env
        before = copy.deepcopy((aggregate, source))
        result = f.deliver(source, encoder or R.canonical, w, d)
        assert before == (aggregate, source)
        return f, result, w, d

    interrupted = {"class": "interrupted", "signal": "SIGINT", "runId": "run3:" + "a" * 64}
    f, r, w, d = deliver(interrupted, writer=Writer(max_write=5))
    rec(
        rows,
        "interrupted-success-is-exit-130-and-keeps-run",
        r["exitCode"] == 130
        and r["termination"] == interrupted
        and r["delivery"] == "complete"
        and d.calls == 0
        and w.flushes == 1
        and json.loads(bytes(w.data))["termination"]["runId"] == interrupted["runId"],
        observed=r,
    )

    f, r, w, d = deliver(interrupted, encoder=lambda _: b"x" * (F.ENVELOPE_MAX_BYTES + 1))
    rec(
        rows,
        "interrupted-plus-capacity-fail-is-exit-4-not-130",
        r["exitCode"] == 4
        and r["termination"] == FAULT
        and r["delivery"] == "failed"
        and w.calls == 0
        and w.flushes == 0
        and bytes(d.data) == F.DIAGNOSTIC
        and interrupted["runId"] not in bytes(d.data).decode()
        and b"never-remove-this" not in w.data,
        observed=r,
    )

    rid = "run3:" + "c" * 64
    render = R.renderer_failure(rid)
    steps = [{"kind": "render", "requirement": "required", "recorded": True, "outcome": "failed", "termination": render}]
    aggregate = R.invocation_aggregate(steps, None)
    rec(rows, "renderer-aggregate-is-delivery-required-failed", aggregate["errorCode"] == "DELIVERY.REQUIRED_FAILED")
    _, r_ok, _, _ = deliver(aggregate)
    _, r_fail, _, _ = deliver(aggregate, writer=Writer(flush_fault=True))
    rec(
        rows,
        "renderer-code-preserved-until-later-output-fault",
        r_ok["termination"]["errorCode"] == "DELIVERY.REQUIRED_FAILED"
        and r_ok["exitCode"] == 4
        and r_fail["termination"]["errorCode"] == "OUTPUT.SERIALIZATION_FAILED"
        and r_fail["exitCode"] == 4,
        observed={"ok": r_ok["termination"]["errorCode"], "fail": r_fail["termination"]["errorCode"]},
    )

    raw = R.canonical(envelope({"class": "success"}))
    writer = Writer(limit=len(raw) // 2)
    _, r, w, d = deliver({"class": "success"}, writer=writer)
    rec(
        rows,
        "stream-prefix-no-second-envelope-and-fixed-diagnostic",
        r["exitCode"] == 4
        and bytes(w.data) == raw[: len(raw) // 2]
        and F.DIAGNOSTIC not in bytes(w.data)
        and bytes(d.data) == F.DIAGNOSTIC
        and b"/secret/path" not in bytes(d.data)
        and b"caller-token" not in bytes(d.data),
        observed={"prefix": len(w.data), "diag": bytes(d.data).decode()},
    )

    writer = Writer(limit=len(raw), flush_fault=True)
    _, r, w, d = deliver({"class": "success"}, writer=writer)
    rec(
        rows,
        "full-write-then-flush-fail-still-exit-4",
        r["exitCode"] == 4 and bytes(w.data) == raw and w.flushes == 1 and bytes(d.data) == F.DIAGNOSTIC,
    )

    _, r_hi, w_hi, _ = deliver({"class": "success"}, encoder=lambda _: b"x" * F.ENVELOPE_MAX_BYTES)
    _, r_over, w_over, _ = deliver({"class": "success"}, encoder=lambda _: b"x" * (F.ENVELOPE_MAX_BYTES + 1))
    rec(
        rows,
        "byte-preflight-allows-exact-4mib-refuses-plus-one-before-write",
        r_hi["delivery"] == "complete"
        and len(w_hi.data) == F.ENVELOPE_MAX_BYTES
        and r_over["delivery"] == "failed"
        and w_over.calls == 0
        and F.ENVELOPE_MAX_BYTES == 4 * 1024 * 1024,
    )

    f, r, w, _ = deliver({"class": "success"})
    after = f.after_commit("user-signal")
    second = None
    try:
        f.deliver(envelope({"class": "success"}), R.canonical, w, Writer())
    except RuntimeError as exc:
        second = str(exc)
    rec(
        rows,
        "one-commit-after-commit-events-cannot-reclassify",
        f.commit_count == 1
        and after == r["termination"] == {"class": "success"}
        and second == "finalization-already-committed",
        observed=second,
    )

    try:
        deliver({"class": "success"}, encoder=lambda _: (_ for _ in ()).throw(RuntimeError("unclassified programming error")))
        rec(rows, "unknown-exception-not-mapped-to-serialization-failed", False)
    except RuntimeError as exc:
        rec(rows, "unknown-exception-not-mapped-to-serialization-failed", str(exc) == "unclassified programming error")

    inter07 = (COPY / "owner/interruption07-contract.md").read_text()
    rec(
        rows,
        "interruption07-keeps-own-operational-fault-law",
        "Failure to record or deliver keeps its own existing operational fault law." in inter07,
    )

    rec(
        rows,
        "this-unit-source-bridge-not-complete",
        json.loads((COPY / "root-receipt.json").read_bytes())["sourceSuccession"].startswith("Exact D9 parity clarification")
        and json.loads((COPY / "result.json").read_bytes())["capacityPolicy"]
        == "proposed explicit operational failure; no prevention guarantee",
    )

    failed = [r for r in rows if not r["passed"]]
    out = {
        "standing": "independent Grok required-output01 probes; synthetic codec/writer; not store/CLI/live signals",
        "passed": not failed,
        "caseCount": len(rows),
        "failedCount": len(failed),
        "failed": [r["name"] for r in failed],
        "policyContext": {
            "thisFreeze": "unselected 43-file complete-output-or-operational-failure proposal; no accepted D9/source changed",
            "laterJoint10": "accepted the alternative as coherent replacement; original criterion not met; blocked promotion",
            "laterRootSelection": "complete-output-or-operational-failure selected; old criterion superseded not passed; source integration pending",
            "originalCriterionMet": False,
            "policyUndecided": False,
            "sourceBridgeComplete": False,
        },
        "checks": rows,
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "independent-l02.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"passed": out["passed"], "caseCount": out["caseCount"], "failed": out["failed"]}))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
