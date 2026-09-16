"""Independent executable counterexamples for joint10 combined admission/projection.

Compiles copy bytes; writes only under review/results. Not a product host.
"""
from __future__ import annotations

import copy
import hashlib
import json
import sys
import traceback
import types
from pathlib import Path

REVIEW = Path("/tmp/opensip-implementation/m1-grok-joint-review-10/review")
COPY = REVIEW / "copy"
RESULTS = REVIEW / "results"
RESULTS.mkdir(parents=True, exist_ok=True)


def load(path: Path, name: str):
    m = types.ModuleType(name)
    m.__file__ = str(path)
    exec(compile(path.read_bytes(), str(path), "exec"), m.__dict__)
    return m


class Cases:
    def __init__(self):
        self.rows = []

    def rec(self, name, passed, **detail):
        self.rows.append({"name": name, "passed": bool(passed), **detail})
        print(("PASS" if passed else "FAIL"), name)


def code_of(fn):
    try:
        fn()
        return "accepted"
    except Exception as exc:  # noqa: BLE001
        return getattr(exc, "code", None) or type(exc).__name__ + ":" + str(exc)[:180]


def main():
    C = Cases()
    D = load(COPY / "check_document.py", "document")
    B = load(COPY / "coverage_bindings.py", "binding")
    S = load(COPY / "coverage" / "coverage_source.py", "source")
    V, M, J = D.V, D.M, D.J
    P = load(COPY / "joint_placement.py", "placement")
    Out = load(COPY / "check_output_integration.py", "output")

    def refresh(doc):
        doc["disclosures"] = D.J.disclosures(
            doc["panels"], None, M, V.H, doc["envelope"]["run"]["runId"], lambda v: V.validate(V.history_schema["$id"], v)
        )
        D.refresh_static(doc)
        return doc

    def local(doc):
        return D.A.admit(M.canonical(doc), V, M, D.J, D.K, D.FJ.owner_summary(V.C))

    with D.R.world(V.read_unit, V.subjects) as w:
        rid, run, objects, blobs, owner = w["rid"], w["run"], w["objects"], w["blobs"], w["M"]
        doc, _, _ = D.make_document(w)
        panel = S.project(rid, run, objects, blobs, 3956, owner)
        panel["provenance"] = copy.deepcopy(B.PROVENANCE)
        doc["panels"]["evidence"] = {"state": "present", "data": panel}
        refresh(doc)
        admitted = local(doc)
        C.rec(
            "actual-retained-two-row-source-admits-and-host-joins",
            len(admitted["panels"]["evidence"]["data"]["entries"]) == 2
            and admitted["panels"]["evidence"]["data"]["source"]["evidenceId"] == run["evidenceId"],
            runId=rid,
            coverageIds=[r["coverageId"] for r in admitted["panels"]["evidence"]["data"]["entries"]],
        )

        def host(d):
            return B.verify_source_prefix(d["panels"]["evidence"]["data"], rid, run, objects, blobs, owner, 3956)

        # Item-cap omission is only lawful when the retained prefix hits the cap.
        # A 1-row panel claiming item-cap at the full 3956 cap is a count lie.
        fake_cap = copy.deepcopy(doc)
        data = fake_cap["panels"]["evidence"]["data"]
        data["entries"] = data["entries"][:1]
        data["entriesProjection"] = {"total": 2, "omitted": 1, "omissionCause": "item-cap"}
        refresh(fake_cap)
        C.rec(
            "one-row-item-cap-at-full-report-cap-fails-local-counts",
            code_of(lambda: local(fake_cap)) == "J-EVIDENCE-COUNTS",
            observed=code_of(lambda: local(fake_cap)),
        )
        one = S.project(rid, run, objects, blobs, 1, owner)
        expected_one = B.verify_source_prefix(one, rid, run, objects, blobs, owner, 1)
        C.rec(
            "standalone-item-cap-1-prefix-joins-host-at-cap-1",
            len(one["entries"]) == 1
            and expected_one["entriesProjection"]["omissionCause"] == "item-cap"
            and one["entriesProjection"]["total"] == 2,
        )
        cap1 = copy.deepcopy(doc)
        cap1["panels"]["evidence"] = {"state": "present", "data": {**one, "provenance": copy.deepcopy(B.PROVENANCE)}}
        refresh(cap1)
        C.rec(
            "standalone-item-cap-1-panel-refused-by-combined-report-item-cap",
            code_of(lambda: local(cap1)) == "J-EVIDENCE-COUNTS",
            observed=code_of(lambda: local(cap1)),
            note="Combined report check_projection requires item-cap prefixes to equal maxEvidenceEntries (3956), not the standalone hydration cap.",
        )

        # Forgery: identity-consistent rehash of row 0, keep row 1 and source.
        forged = copy.deepcopy(doc)
        row = forged["panels"]["evidence"]["data"]["entries"][0]
        row["result"]["entry"]["confidenceMillionths"] = 424242
        row["descriptor"]["payloadDigest"] = hashlib.sha256(V.C.canonical(row["result"])).hexdigest()
        row["coverageId"] = "coverage2:" + V.C.identity("coverage", row["descriptor"])
        forged["panels"]["evidence"]["data"]["entries"].sort(key=lambda r: r["coverageId"])
        refresh(forged)
        C.rec("forged-rehashed-row-passes-local-admission", code_of(lambda: local(forged)) == "accepted")
        C.rec(
            "forged-rehashed-row-fails-retained-source-join",
            code_of(lambda: host(forged)).endswith("J-EVIDENCE-SOURCE-PREFIX") or "J-EVIDENCE-SOURCE-PREFIX" in code_of(lambda: host(forged)),
            observed=code_of(lambda: host(forged)),
        )

        # Source substitution: well-formed other evidenceId.
        swapped = copy.deepcopy(doc)
        swapped["panels"]["evidence"]["data"]["source"]["evidenceId"] = "evidence3:" + "a" * 64
        refresh(swapped)
        C.rec("substituted-evidenceId-passes-local-admission", code_of(lambda: local(swapped)) == "accepted")
        C.rec(
            "substituted-evidenceId-fails-retained-source-join",
            "J-EVIDENCE-SOURCE-PREFIX" in code_of(lambda: host(swapped)),
            observed=code_of(lambda: host(swapped)),
        )

        # Run-id substitution is a local authority failure, not a silent empty panel.
        bad_run = copy.deepcopy(doc)
        bad_run["panels"]["evidence"]["data"]["source"]["runId"] = "run3:" + "f" * 64
        C.rec("substituted-runId-fails-local-source-run", code_of(lambda: local(bad_run)) == "J-EVIDENCE-SOURCE-RUN", observed=code_of(lambda: local(bad_run)))

        # Ephemeral shape on a retained Run document.
        eph = copy.deepcopy(doc)
        eph["panels"]["evidence"]["data"]["source"] = {"planId": "plan2:" + "b" * 64, "evidenceId": run["evidenceId"]}
        C.rec(
            "ephemeral-shape-on-retained-run-fails-local",
            code_of(lambda: local(eph)) in ("J-EVIDENCE-SOURCE-RUN", "J-EVIDENCE-SOURCE-EPHEMERAL"),
            observed=code_of(lambda: local(eph)),
        )

        # Missing evidence object is owner EvidenceUnavailable, not empty success.
        missing = copy.deepcopy(objects)
        del missing[run["evidenceId"]]
        C.rec(
            "lost-evidence-is-not-empty-panel",
            "EvidenceUnavailable" in code_of(lambda: B.verify_source_prefix(panel, rid, run, missing, blobs, owner, 3956)),
            observed=code_of(lambda: B.verify_source_prefix(panel, rid, run, missing, blobs, owner, 3956)),
        )

        extra = copy.deepcopy(objects)
        extra_blobs = copy.deepcopy(blobs)
        extra_row = copy.deepcopy(panel["entries"][0])
        extra_row["result"]["entry"]["confidenceMillionths"] = 7
        extra_row["descriptor"]["payloadDigest"] = hashlib.sha256(V.C.canonical(extra_row["result"])).hexdigest()
        extra_row["coverageId"] = "coverage2:" + V.C.identity("coverage", extra_row["descriptor"])
        extra[extra_row["coverageId"]] = ("coverage", extra_row["descriptor"])
        extra_blobs[extra_row["descriptor"]["payloadDigest"]] = V.C.canonical(extra_row["result"])
        projected = S.project(rid, run, extra, extra_blobs, 2, owner)
        C.rec(
            "unlinked-hash-valid-coverage-does-not-expand-retained-set",
            [r["coverageId"] for r in projected["entries"]] == [r["coverageId"] for r in panel["entries"]],
            extraId=extra_row["coverageId"],
        )

    # --- Shared budget reservation and order ---
    PRIORITY = list(V.report["$defs"]["BudgetProfileV1"]["properties"]["projectionPriority"]["const"])
    omitted = copy.deepcopy(P.OMITTED)
    present = lambda n: {"state": "present", "data": {"n": n}}
    existing = {"comparison": present("cmp"), "catalog": present("cat"), "evidence": present("ev")}
    # Later builder after catalog omitted must not run.
    called = []
    existing_stop = {"comparison": present("cmp"), "catalog": {"state": "omitted", "reason": "exploration-budget-exceeded"}}
    panels, _ = P.append(
        existing_stop,
        {"graph": lambda allowed: called.append(allowed) or {"ok": True}},
        {"history": {"state": "unavailable", "reason": "evidence-purged"}},
        PRIORITY,
        10**6,
        M,
    )
    C.rec(
        "budget-stop-skips-later-builder-after-catalog-omitted",
        called == [] and panels["graph"]["state"] == "omitted",
        called=called,
        graph=panels.get("graph"),
    )
    later_present = {"comparison": {"state": "omitted", "reason": "exploration-budget-exceeded"}, "catalog": present("late")}
    C.rec(
        "later-present-after-earlier-omission-refuses",
        "later existing panel violates priority" in code_of(
            lambda: P.append(later_present, {}, {}, ["comparison", "catalog"], 10**6, M)
        ),
        observed=code_of(lambda: P.append(later_present, {}, {}, ["comparison", "catalog"], 10**6, M)),
    )
    C.rec(
        "overlapping-builder-and-terminal-refuses",
        "one panel source state required" in code_of(lambda: P.append({}, {"catalog": lambda a: {}}, {"catalog": omitted}, ["catalog"], 100, M)),
        observed=code_of(lambda: P.append({}, {"catalog": lambda a: {}}, {"catalog": omitted}, ["catalog"], 100, M)),
    )
    C.rec(
        "reserved-states-exceeding-allowance-refuse",
        "reserved panel states exceed shared allowance" in code_of(
            lambda: P.append({"comparison": present("x" * 200)}, {}, {"catalog": omitted}, ["comparison", "catalog"], 20, M)
        ),
        observed=code_of(lambda: P.append({"comparison": present("x" * 200)}, {}, {"catalog": omitted}, ["comparison", "catalog"], 20, M)),
    )
    C.rec(
        "owner-exceeding-remaining-allowance-refuses",
        "owner exceeded its panel allowance" in code_of(
            lambda: P.append(
                {"comparison": present("c")},
                {"catalog": lambda allowed: {"pad": "y" * max(allowed, 1)}},
                {},
                ["comparison", "catalog"],
                len(M.canonical({"comparison": present("c"), "catalog": omitted})) + 8,
                M,
            )
        ),
        observed=code_of(
            lambda: P.append(
                {"comparison": present("c")},
                {"catalog": lambda allowed: {"pad": "y" * 400}},
                {},
                ["comparison", "catalog"],
                len(M.canonical({"comparison": present("c"), "catalog": omitted})) + 40,
                M,
            )
        ),
    )

    # --- Fit interruption / output precedence ---
    tests = Out.OutputIntegrationTests()
    record, envelope = tests.interrupted()
    before = copy.deepcopy(record)
    _, result, out, diag = tests.deliver(envelope)
    C.rec(
        "interrupted-composite-delivers-with-exit-130",
        result["exitCode"] == 130 and result["delivery"] == "complete" and envelope["advisoryReport"]["state"] == "unavailable-query-result",
        result=result,
    )
    f, result, out, diag = tests.deliver(envelope, Out.O.Writer(limit=19))
    C.rec(
        "output-failure-after-interruption-is-exit-4-not-130",
        result == {"termination": Out.O.FAULT, "exitCode": 4, "delivery": "failed"} and bytes(diag.data) == Out.F.DIAGNOSTIC,
        result=result,
        written=len(out.data),
    )
    C.rec(
        "after-commit-events-keep-output-fault-not-signal-130",
        all(f.after_commit(ev) == Out.O.FAULT for ev in ["user-signal", "transport-close", "optional-delivery-failure"]),
    )
    C.rec("second-deliver-after-commit-refuses", "already-committed" in code_of(lambda: f.deliver(envelope, Out.encode, out, diag)))
    C.rec("interruption-record-unmutated", record == before)

    encoder = Out.admitted_encoder(envelope)
    mutated = copy.deepcopy(envelope)
    mutated.pop("advisoryReport")
    Out.V.validate(Out.ENV, mutated)
    _, result, out, diag = tests.deliver(mutated, encoder=encoder)
    C.rec(
        "source-mutated-interrupted-envelope-writes-no-normal-bytes",
        result["delivery"] == "failed" and result["exitCode"] == 4 and out.calls == 0 and bytes(diag.data) == Out.F.DIAGNOSTIC,
        result=result,
        calls=out.calls,
    )
    # Independent: termination/aggregate mismatch at finalizer, not a 130 rewrite.
    f2 = Out.F.Finalizer(envelope["termination"], Out.O.FAULT, Out.O.EXITS)
    mismatched = copy.deepcopy(envelope)
    mismatched["termination"] = copy.deepcopy(Out.O.FAULT)
    result = f2.deliver(mismatched, Out.admitted_encoder(envelope), Out.O.Writer(max_write=257), Out.O.Writer())
    C.rec(
        "aggregate-envelope-mismatch-is-output-fault-exit-4",
        result["exitCode"] == 4 and result["delivery"] == "failed",
        result=result,
    )

    failed = [r for r in C.rows if not r["passed"]]
    out = {
        "standing": "Independent Grok executable combined-boundary probes; not product acceptance",
        "passed": not failed,
        "caseCount": len(C.rows),
        "failedCount": len(failed),
        "failed": [r["name"] for r in failed],
        "checks": C.rows,
    }
    (RESULTS / "independent-executable.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"passed": out["passed"], "caseCount": out["caseCount"], "failed": out["failed"]}))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    try:
        main()
    except SystemExit:
        raise
    except Exception:
        (RESULTS / "independent-executable.exc").write_text(traceback.format_exc())
        raise
