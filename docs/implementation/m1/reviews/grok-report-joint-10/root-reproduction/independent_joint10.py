"""Independent Grok probes for joint10 combined reference. Writes only under review/results."""
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

REVIEW = Path("/tmp/opensip-implementation/m1-grok-joint-review-10/root-reproduction")
COPY = REVIEW / "copy"
RESULTS = REVIEW / "results"
RESULTS.mkdir(parents=True, exist_ok=True)


class Cases:
    def __init__(self):
        self.rows = []

    def rec(self, name, passed, **detail):
        self.rows.append({"name": name, "passed": bool(passed), **detail})
        print(("PASS" if passed else "FAIL"), name)


def main():
    C = Cases()
    guide = (COPY / "REVIEW-GUIDE.md").read_text()
    readme = (COPY / "README.md").read_text()
    succession = (COPY / "coverage-succession.md").read_text()
    status = json.loads((COPY / "integration-status.json").read_bytes())
    obligations = json.loads((COPY / "joint-obligations.json").read_bytes())
    verify = (COPY / "verify_candidate.py").read_text()

    C.rec(
        "review-guide-is-stale-joint09-replacement-count",
        "Joint report09" in guide
        and "186 unchanged outcomes and8 replacements" in guide.replace(" ", "")
        or ("186 unchanged" in guide and "8 replacements" in guide),
        note="Detection: True means the guide still states joint09 8-replacement arithmetic, not joint10's 11.",
        guideTitle=guide.splitlines()[0],
    )
    C.rec(
        "current-docs-state-eleven-replacement-witnesses",
        "11 explicit replacement witnesses" in readme
        and "11 explicit replacement witnesses" in succession
        and status["latestChecks"]["parentReconciliation"]["unchangedOutcomes"] == 183
        and len(status["latestChecks"]["parentReconciliation"]["rebasedWitnesses"]) == 11
        and status["latestChecks"]["parentReconciliation"]["totalExecuted"] == 205
        and "eleven explicit predecessor-witness differences" in verify,
        unchanged=status["latestChecks"]["parentReconciliation"]["unchangedOutcomes"],
        witnesses=len(status["latestChecks"]["parentReconciliation"]["rebasedWitnesses"]),
        totalExecuted=status["latestChecks"]["parentReconciliation"]["totalExecuted"],
    )
    C.rec(
        "parent-inventory-is-not-collapsed-to-194-unchanged",
        status["latestChecks"]["parentReconciliation"]["parentCases"] == 194
        and status["latestChecks"]["parentReconciliation"]["totalExecuted"] == 205,
    )

    schema_path = COPY / "coverage" / "coverage-budget.experimental.schema.json"
    schema = json.loads(schema_path.read_bytes())
    src = schema["properties"]["source"]
    C.rec(
        "standalone-experimental-schema-is-run-evidence-only",
        src.get("required") == ["runId", "evidenceId"] and "oneOf" not in src,
        sourceKeys=list(src),
    )
    composed = None
    for p in [
        COPY / "composed-sources" / "report-projection.proposed.schema.json",
        COPY / "composed-sources" / "report-projection.schema.json",
    ]:
        if p.exists():
            composed = json.loads(p.read_bytes())
            break
    # Evidence panel in composed report after schema_into
    evidence = None
    if composed:
        evidence = composed.get("$defs", {}).get("EvidencePanelV1")
    C.rec("composed-report-schema-present", composed is not None, path=str(composed and "found"))
    if evidence:
        source = evidence["properties"]["source"]
        C.rec(
            "composed-evidence-source-is-oneof-retained-or-ephemeral",
            "oneOf" in source and len(source["oneOf"]) == 2,
            source=source,
        )
        C.rec(
            "composed-profile-is-development-caps-6",
            composed["$defs"]["BudgetProfileV1"]["properties"]["profileId"]["const"]
            == "opensip.report-projection.development-caps.6",
            profile=composed["$defs"]["BudgetProfileV1"]["properties"]["profileId"]["const"],
        )
        item = composed.get("$defs", {}).get("ItemProjectionV1", {})
        C.rec(
            "composed-omission-includes-byte-budget",
            "byte-budget" in json.dumps(item),
            itemProjection=item.get("properties", {}).get("omissionCause"),
        )
    else:
        C.rec("composed-evidence-source-is-oneof-retained-or-ephemeral", False, reason="EvidencePanelV1 missing")
        C.rec("composed-profile-is-development-caps-6", False)
        C.rec("composed-omission-includes-byte-budget", False)

    frozen_report08 = json.loads((COPY / "parent-report08" / "report-projection.schema.json").read_bytes())
    C.rec(
        "frozen-report08-still-single-coverageId-stream",
        frozen_report08["$defs"]["EvidencePanelV1"]["required"] == ["coverageId", "entries", "entriesProjection", "provenance"],
        required=frozen_report08["$defs"]["EvidencePanelV1"]["required"],
    )
    frozen_profile = frozen_report08["$defs"]["BudgetProfileV1"]["properties"]["profileId"]["const"]
    C.rec(
        "frozen-report08-profile-is-historical-caps-4",
        frozen_profile == "opensip.report-projection.development-caps.4",
        frozenProfile=frozen_profile,
        note="report_carriers then sets 5; coverage schema_into sets 6 as the unreleased combined carrier",
    )

    pool = [r for r in obligations.get("obligations", []) + obligations.get("integrationObligations", []) if isinstance(r, dict)]
    ids = [r.get("id") for r in pool]
    l02 = next((r for r in pool if r.get("id") == "RP-OBL-L02"), None)
    if l02 is None:
        C.rec("l02-original-criterion-not-claimed-met", False, obligationIds=ids)
        C.rec("l02-output-policy-standing-unresolved", False)
    else:
        C.rec(
            "l02-original-criterion-not-claimed-met",
            l02["status"] == "open-owner-decision"
            and l02.get("blocksM1FinalIntegration") is True
            and "not met by this proposal" in l02.get("jointEvidence", {}).get("standing", ""),
            standing=l02.get("jointEvidence", {}).get("standing"),
            closure=l02.get("closureCriterion"),
        )
        policy = json.loads((COPY / "output-policy-result.json").read_bytes()) if (COPY / "output-policy-result.json").exists() else {}
        blob = json.dumps(policy)
        C.rec(
            "l02-output-policy-standing-unresolved",
            "L02" in blob and ("unresolved" in blob.lower() or "no L02" in blob or "does not close L02" in blob),
            standing=policy.get("standing"),
        )

    C.rec(
        "coverage-source-py-matches-standalone-experiment",
        hashlib.sha256((COPY / "coverage" / "coverage_source.py").read_bytes()).hexdigest()
        == "e2f4e9a283144aef896efb23a7b7814a191c06ac79fd2cf57323a13b7e368a32",
    )
    C.rec(
        "verify_source_prefix-docstring-denies-maximal-byte-and-lease",
        "does not establish the maximal byte-budget prefix" in (COPY / "coverage_bindings.py").read_text()
        and "storage lease" in (COPY / "coverage_bindings.py").read_text(),
    )
    C.rec(
        "ephemeral-native-replay-declared-host-duty",
        "native source custody/replay remains a host implementation" in succession,
    )
    C.rec(
        "readiness-still-blocks-promotion",
        obligations["readiness"]["projectCompletion"].startswith("not complete")
        and "RP-OBL-L02" in obligations["readiness"]["m1FinalIntegrationBlockers"],
    )
    C.rec(
        "inventory-provenance-is-inventory6",
        "inventory6" in (COPY / "REVIEW-GUIDE.md").read_text()
        or "inventory6" in (COPY / "README.md").read_text()
        or "inventory6" in (COPY / "coverage-succession.md").read_text(),
    )
    # envelope7 / invocation5 from generate_models asserts
    gen = json.loads((COPY / "model-generation-result.json").read_bytes()) if (COPY / "model-generation-result.json").exists() else {}
    C.rec(
        "invocation5-and-query4-generation-recorded",
        gen.get("timingCompatibility", "").startswith("Invocation5") or "schemaMajor" in json.dumps(gen),
        standing=gen.get("standing"),
        timing=gen.get("timingCompatibility"),
    )

    failed = [r for r in C.rows if not r["passed"]]
    out = {
        "standing": "Independent Grok joint10 probes; not product acceptance",
        "passed": not failed,
        "caseCount": len(C.rows),
        "failedCount": len(failed),
        "failed": [r["name"] for r in failed],
        "checks": C.rows,
    }
    (RESULTS / "independent-joint10.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"passed": out["passed"], "caseCount": out["caseCount"], "failed": out["failed"]}))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
