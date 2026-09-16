"""Independent CFG-F1–F4 probes against config-disclosure02. Not a restatement of check.py."""
from __future__ import annotations

import copy
import hashlib
import json
import types
from pathlib import Path

COPY = Path("/tmp/opensip-implementation/m1-root-config02-reproduction/copy")
RESULTS = Path("/tmp/opensip-implementation/m1-root-config02-reproduction/results")
SUBJ01 = Path("/tmp/opensip-implementation/m1-config-disclosure-subject-01")
JOINT13 = Path("/tmp/opensip-implementation/m1-report-joint-candidate-13/composed-sources/configuration-disclosure.schema.json")


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
    pins = json.loads((COPY / "input-pins.json").read_bytes())["files"]
    by_role = {}
    for pin in pins:
        raw = Path(pin["path"]).read_bytes()
        assert len(raw) == pin["bytes"] and hashlib.sha256(raw).hexdigest() == pin["sha256"]
        by_role[pin["role"]] = Path(pin["path"])
    C = load(by_role["canonical"], "canonical_reference")
    IM = load(by_role["identity-model"], "identity_model")
    identity = json.loads(by_role["identity"].read_bytes())
    schema = json.loads((COPY / "configuration-disclosure.schema.json").read_bytes())
    policy = json.loads((COPY / "field-policy.json").read_bytes())
    D = load(COPY / "disclosure.py", "disclosure")
    builder = load(COPY / "build_schema.py", "schema_builder")

    def source():
        return {
            "analysis": {
                "profileId": "secret-profile",
                "capabilities": ["secret-capability"],
                "budget": {"unit": "work-units", "limit": 7},
            },
            "components": {},
            "discovery": {},
            "policy": {},
            "evidence": {},
        }

    def plan_for(config):
        return {
            "schemaVersion": 2,
            "snapshotId": "snapshot2:" + "2" * 64,
            "capabilityManifestId": "3" * 64,
            "semanticClosures": [],
            "analysisSpecDigest": "4" * 64,
            "resolvedConfigDigest": hashlib.sha256(C.canonical(config)).hexdigest(),
            "nativeContextDigests": [],
            "importIds": [],
            "policyDigest": "5" * 64,
            "waiverDigest": "6" * 64,
            "scopeDigest": "7" * 64,
            "budget": copy.deepcopy(config["analysis"]["budget"]),
            "semanticGrantDigest": "8" * 64,
            "capabilityManifestBytesDigest": "9" * 64,
        }

    def project(config, plan=None, plan_id=None, selected_policy=None):
        if plan is None:
            plan = plan_for(config)
        pid = plan_id if plan_id is not None else "plan2:" + C.identity("plan", plan)
        return D.project(pid, plan, config, selected_policy or policy, C, identity, schema)

    regenerated, rules = builder.build(identity)
    rec(rows, "schema-regenerates-from-pinned-identity-owner", regenerated == schema and rules == policy["fields"])

    config = source()
    plan = plan_for(config)
    expected = IM.identifier("plan", plan)
    rec(
        rows,
        "cfg-f1-plan-id-equals-identity-model-identifier",
        expected == "plan2:" + C.identity("plan", plan) and project(config)["source"]["planId"] == expected,
        observed=expected[:20],
    )

    try:
        project(config, plan_id="plan2:" + "a" * 64)
        rec(rows, "cfg-f1-caller-plan-id-cannot-relabel-same-plan", False)
    except D.DisclosureRefusal as exc:
        rec(rows, "cfg-f1-caller-plan-id-cannot-relabel-same-plan", "PLAN-ID" in str(exc), observed=str(exc))

    try:
        D.project(expected, {"resolvedConfigDigest": plan["resolvedConfigDigest"]}, config, policy, C, identity, schema)
        rec(rows, "cfg-f1-incomplete-plan-shape-refused", False)
    except (C.ValidationError, C.AdmissionError):
        rec(rows, "cfg-f1-incomplete-plan-shape-refused", True)

    # Historical subject01 still accepts a mismatched planId for the same dict.
    D01 = load(SUBJ01 / "disclosure.py", "disclosure01")
    schema01 = json.loads((SUBJ01 / "configuration-disclosure.schema.json").read_bytes())
    policy01 = json.loads((SUBJ01 / "field-policy.json").read_bytes())
    mismatched = D01.project("plan2:" + "a" * 64, plan, config, policy01, C, identity, schema01)
    rec(
        rows,
        "historical-subject01-still-emits-caller-plan-id",
        mismatched["source"]["planId"] == "plan2:" + "a" * 64 and mismatched["source"]["planId"] != expected,
        note="original CFG-F1; not this freeze",
    )

    out = project(config)
    rec(
        rows,
        "cfg-f2-provenance-split-document-vs-host",
        out["provenance"]["verifiedInDocument"]
        == ["closed-public-value-types", "complete-fixed-field-slots", "no-undeclared-field-slots"]
        and "configuration-digest-equals-retained-plan" in out["provenance"]["hostAsserted"]
        and "plan-id-recomputed-from-retained-plan" in out["provenance"]["hostAsserted"]
        and "retained-plan-belongs-to-selected-run" in out["provenance"]["hostAsserted"]
        and "configuration-digest-equals-retained-plan" not in out["provenance"]["verifiedInDocument"],
    )

    request_min = schema["properties"]["fields"]["properties"]["components.request"]["oneOf"][0]["properties"]["itemCount"]["minimum"]
    rec(rows, "cfg-f3-request-itemcount-minimum-copies-owner-minitems-1", request_min == 1, observed=request_min)

    report = json.loads(by_role["report-schema"].read_bytes())
    panel = report["$defs"]["PanelNotPresentV1"]
    mapped = True
    for reason, expected_state in D.SOURCE_FAILURES.items():
        value = D.unavailable_source(reason)
        C.validate(panel, value)
        if value != expected_state or "detail" in value:
            mapped = False
    rec(
        rows,
        "cfg-f4-source-failures-are-owned-panel-states-without-raw-detail",
        mapped
        and D.unavailable_source("missing")["reason"] == "evidence-missing"
        and D.unavailable_source("digest-mismatch") == {"state": "corrupt", "reason": "retained-bytes-corrupt"}
        and D.unavailable_source("unsupported-schema")["state"] == "incompatible",
    )
    try:
        D.unavailable_source("secret source error")
        rec(rows, "cfg-f4-unknown-failure-not-empty-or-current-settings", False)
    except D.DisclosureRefusal:
        rec(rows, "cfg-f4-unknown-failure-not-empty-or-current-settings", True)

    first = source()
    first["discovery"]["entryPoints"] = ["private-a"]
    second = copy.deepcopy(first)
    second["analysis"]["profileId"] = "other-private-profile"
    second["discovery"]["entryPoints"] = ["a-much-longer-private-path"]
    a, b = project(first), project(second)
    rec(
        rows,
        "noninterference-excludes-planid-and-digest-only",
        a["source"]["planId"] != b["source"]["planId"]
        and a["source"]["resolvedConfigDigest"] != b["source"]["resolvedConfigDigest"]
        and {k: v for k, v in a.items() if k != "source"} == {k: v for k, v in b.items() if k != "source"}
        and a["fields"] == b["fields"],
    )

    raw = C.canonical(project(first))
    rec(
        rows,
        "redacted-secrets-absent-from-canonical-carrier",
        b"secret-profile" not in raw and b"private-a" not in raw and b"secret-capability" not in raw,
    )

    try:
        project(config, plan=dict(plan, resolvedConfigDigest="0" * 64))
        rec(rows, "current-or-other-digest-cannot-fill-older-plan", False)
    except D.DisclosureRefusal as exc:
        rec(rows, "current-or-other-digest-cannot-fill-older-plan", "SOURCE-DIGEST" in str(exc), observed=str(exc))

    rec(
        rows,
        "joint13-schema-byte-identical-is-not-a-waiver",
        JOINT13.is_file()
        and hashlib.sha256(JOINT13.read_bytes()).hexdigest()
        == "0584bf2fd6fd9eee8879a4dca44569b2b9628f55a342f837c313c183c69ef659"
        == hashlib.sha256((COPY / "configuration-disclosure.schema.json").read_bytes()).hexdigest(),
    )

    rec(
        rows,
        "synthetic-plan-is-not-run-custody",
        "not a full retained digest closure" in Path(COPY / "check.py").read_text()
        and "Full retained digest closure" in Path(COPY / "contract.md").read_text(),
    )

    failed = [r for r in rows if not r["passed"]]
    out = {
        "standing": "independent Grok config-disclosure02 probes; synthetic Plan shape; not Run/HTML/browser",
        "passed": not failed,
        "caseCount": len(rows),
        "failedCount": len(failed),
        "failed": [r["name"] for r in failed],
        "findingDispositions": {
            "CFG-F1": "corrected-in-this-freeze-shape-and-recomputed-plan2; not full Run custody",
            "CFG-F2": "corrected-in-this-freeze-closed-provenance",
            "CFG-F3": "corrected-in-this-freeze-request-itemCount-minimum-1",
            "CFG-F4": "corrected-in-this-freeze-PanelNotPresentV1-mapping",
        },
        "checks": rows,
    }
    RESULTS.mkdir(parents=True, exist_ok=True)
    (RESULTS / "independent-config.json").write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"passed": out["passed"], "caseCount": out["caseCount"], "failed": out["failed"]}))
    if failed:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
