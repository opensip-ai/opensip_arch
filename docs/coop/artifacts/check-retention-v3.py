#!/usr/bin/env python3
"""Check the non-binding retention-v3 detailed-design exploration.

This runner deliberately proves a narrow claim: the exploration's structured axes
conform to its declared schema and deterministically produce the expected proof-
gate classification. It does NOT validate a cryptographic proof construction,
extractor correctness, storage-root detection, deletion, implementation code, or
the architectural merit of retention-tiers.v4.json.

Independent review found known semantic holes A1-RTV3-01/02: zero activated
evaluations and ignored indeterminate/error outcomes can still derive durable-pass.
They are preserved here as evidence that a green detailed-design checker is not an
architecture review. Do not use this runner as a release or architecture gate.

  RV1  candidate status, three assurance capabilities, and orthogonal axes exist
  RV2  golden axes and receipt items conform to the declared closed schema
  RV3  expected results conform to the declared closed schema
  RV4  the pure ordered derivation reproduces every expected result
  RV5  load-bearing negative reasons and both successful custody modes are covered
  RV6  proof graph requires evaluation + verdict receipts and host-owned verifiers

Usage: python3 artifacts/check-retention-v3.py [path-to-contract]
Exit:  0 clean · 1 findings · 2 IO/JSON error
"""
from __future__ import annotations

import json
import pathlib
import sys
from typing import Any


# ------------------------------------------------------ the parse primitive
#
# json.loads without an object_pairs_hook keeps the LAST of a duplicated key, so
# a document can say one thing to a human reader and another to every
# instrument, with the parsed object byte-identical to the honest one.  Every
# JSON byte this checker reads enters through jloads(), which RECORDS each
# repeated key against its own path and reports it as a named finding at that
# position rather than raising.  An operator who is told only that the file is
# bad does not learn which key was duplicated or where it sits; these findings
# name both.

# label -> findings, for every parse this process performed.  A duplicate key is
# a property of the BYTES, so it is recorded where the bytes were read and
# reported by check() rather than thrown from the parse.
_PARSES: dict[str, list[str]] = {}


def _duplicate_paths(node: Any, steps: list[Any], marks: dict[int, list[str]],
                     out: list[tuple[str, str]]) -> None:
    """Walk the parse and report every recorded duplicate under its OWN path."""
    if isinstance(node, dict):
        for key in marks.get(id(node), []):
            path = "".join(
                f"[{s}]" if isinstance(s, int) else (f".{s}" if steps else s)
                for s in (steps + [key]))
            out.append((path.lstrip("."), key))
        for key, item in node.items():
            _duplicate_paths(item, steps + [key], marks, out)
    elif isinstance(node, list):
        for index, item in enumerate(node):
            _duplicate_paths(item, steps + [index], marks, out)


def jloads(text: str, label: str) -> tuple[Any, list[str]]:
    """Parse JSON and report every key the BYTES publish more than once."""
    marks: dict[int, list[str]] = {}
    keep: list[Any] = []

    def pairs(items: list[tuple[str, Any]]) -> dict[str, Any]:
        out: dict[str, Any] = {}
        repeated: list[str] = []
        for key, value in items:
            if key in out:
                repeated.append(key)
            out[key] = value
        if repeated:
            # `keep` holds a live reference to every object that recorded a
            # duplicate, so no id() in `marks` can be reused by a collected
            # object while the paths are being resolved.
            keep.append(out)
            marks[id(out)] = repeated
        return out

    value = json.loads(text, object_pairs_hook=pairs)
    found: list[tuple[str, str]] = []
    if marks:
        _duplicate_paths(value, [], marks, found)
    problems = [
        f"RV-DUPKEY {label}: key '{key}' is published more than once at "
        f"{path or '<document root>'}; the host parser keeps the LAST "
        f"occurrence, so the parsed document cannot say what the bytes say"
        for path, key in found
    ]
    declared = sum(len(v) for v in marks.values())
    if len(found) < declared:
        problems.append(
            f"RV-DUPKEY {label}: {declared - len(found)} duplicate key(s) sit in "
            f"an object the parse itself discarded, so this run cannot resolve "
            f"their path; they are refused regardless")
    if len(keep) != len(marks):
        problems.append(
            f"RV-DUPKEY {label}: the duplicate-key record and the objects it "
            f"refers to disagree in cardinality")
    _PARSES[label] = problems
    return value, problems


def parse_findings() -> list[str]:
    """Every duplicate-key finding recorded by every parse this run performed."""
    out: list[str] = []
    for problems in _PARSES.values():
        out.extend(problems)
    return out


def load(path: pathlib.Path) -> Any:
    """Every JSON file this checker reads enters here, and there is no other
    door."""
    path = pathlib.Path(path)
    value, _problems = jloads(path.read_text(), path.name)
    return value


def derive(ax: dict[str, Any]) -> dict[str, str | None]:
    """Pure first-failure derivation declared by goldenDerivation."""
    capability = ax["requestedCapability"]

    if ax["authoritative"] and capability == "C0-recorded":
        return result("request-rejected", "PROOF.CAPABILITY_INSUFFICIENT")

    if ax["durable"] and ax["storagePolicy"] == "missing":
        return result("request-rejected", "STORAGE.POLICY_REQUIRED")
    if ax["durable"] and ax["storagePolicy"] == "unsafe-root":
        return result("request-rejected", "STORAGE.ROOT_UNSAFE")

    if capability == "C0-recorded" and not ax["authoritative"]:
        return result("durable-advisory-recorded" if ax["durable"] else "ephemeral-advisory")

    if capability in {"C1-verifiable", "C2-replayable"} and not ax["durable"]:
        return result("request-rejected", "PROOF.DURABILITY_REQUIRED")

    receipts = ax["evaluationReceipts"]
    if len(receipts) != ax["activatedEvaluations"]:
        return result("indeterminate", "PROOF.EVALUATION_RECEIPT_MISSING")

    for receipt in receipts:
        if receipt["obligation"] != "host-owned":
            return result("indeterminate", "PROOF.OBLIGATION_UNTRUSTED")
        if receipt["verifierAndRoot"] != "present":
            return result("indeterminate", "PROOF.VERIFIER_OR_ROOT_MISSING")
        if receipt["custody"] == "frozen" and receipt["frozenBody"] != "present":
            return result("indeterminate", "PROOF.FROZEN_BODY_MISSING")
        if receipt["claimMaterial"] != "complete":
            return result("indeterminate", "PROOF.WITNESS_INSUFFICIENT")
        if receipt["sourceWitness"] == "required-not-granted":
            return result("indeterminate", "PRIVACY.SOURCE_RETENTION_NOT_GRANTED")
        if receipt["truncated"]:
            return result("indeterminate", "PROOF.BUDGET_EXHAUSTED")
        if receipt["custody"] == "regenerable" and receipt["derivationClosure"] != "complete":
            return result("indeterminate", "PROOF.REGENERATION_CLOSURE_MISSING")

    if ax["verdictReceipt"] != "present":
        return result("indeterminate", "PROOF.VERDICT_RECEIPT_MISSING")
    if capability == "C2-replayable" and ax["executableReplayClosure"] != "complete":
        return result("indeterminate", "REPLAY.CLOSURE_MISSING")

    return result("durable-pass" if ax["policyVerdict"] == "pass" else "durable-policy-fail")


def result(classification: str, reason: str | None = None) -> dict[str, str | None]:
    return {"classification": classification, "reasonCode": reason}


def validate_value(value: Any, rule: dict[str, Any], where: str, findings: list[str]) -> None:
    if "enum" in rule:
        if value not in rule["enum"]:
            findings.append(f"RV2 {where}: {value!r} outside enum")
        return
    expected = rule.get("type")
    if expected == "boolean" and type(value) is not bool:
        findings.append(f"RV2 {where}: expected boolean")
    elif expected == "non-negative-integer" and (
        type(value) is not int or value < 0
    ):
        findings.append(f"RV2 {where}: expected non-negative integer")
    elif expected == "array" and not isinstance(value, list):
        findings.append(f"RV2 {where}: expected array")


def validate_closed_object(
    obj: Any,
    schema: dict[str, Any],
    where: str,
    findings: list[str],
    finding_prefix: str,
) -> None:
    if not isinstance(obj, dict):
        findings.append(f"{finding_prefix} {where}: expected object")
        return
    properties = schema["properties"]
    for key in obj:
        if key not in properties:
            findings.append(f"{finding_prefix} {where}: undeclared field {key!r}")
    for key in schema["required"]:
        if key not in obj:
            findings.append(f"{finding_prefix} {where}: missing required field {key!r}")
    for key, value in obj.items():
        if key in properties:
            validate_value(value, properties[key], f"{where}.{key}", findings)


def check(contract: dict[str, Any]) -> list[str]:
    # A duplicated key is a property of the bytes that were read, not of the
    # dict those bytes produced, so it is carried in from the parse record.  It
    # leads because no other finding can be trusted while the document the
    # instrument parsed differs from the document a reader sees.
    findings: list[str] = parse_findings()

    # RV1 — the artifact must not ratify itself, and all axes must be distinct.
    if contract.get("status") != "CANDIDATE-UNREVIEWED":
        findings.append("RV1: v3 must remain CANDIDATE-UNREVIEWED pending independent review")
    capabilities = {item["id"] for item in contract.get("capabilities", [])}
    if capabilities != {"C0-recorded", "C1-verifiable", "C2-replayable"}:
        findings.append(f"RV1: capability set is {sorted(capabilities)!r}")
    axes = {item["axis"] for item in contract.get("model", {}).get("orthogonalAxes", [])}
    if axes != {"sealedCapability", "custodyMode", "availability"}:
        findings.append(f"RV1: orthogonal axis set is {sorted(axes)!r}")

    schema = contract["goldenAxesSchema"]
    expected_schema = schema["expected"]
    seen_reasons: set[str] = set()
    seen_success_modes: set[str] = set()

    for golden in contract["goldenCases"]:
        gid = golden.get("id", "<missing-id>")
        if not golden.get("scenario"):
            findings.append(f"RV2 {gid}: missing falsifiable scenario")
        axes_value = golden.get("scenarioAxes")
        validate_closed_object(axes_value, schema, f"{gid}.scenarioAxes", findings, "RV2")

        if isinstance(axes_value, dict) and isinstance(axes_value.get("evaluationReceipts"), list):
            receipt_schema = schema["properties"]["evaluationReceipts"]
            item_schema = {
                "properties": receipt_schema["itemProperties"],
                "required": receipt_schema["itemRequired"],
            }
            for index, receipt in enumerate(axes_value["evaluationReceipts"]):
                validate_closed_object(
                    receipt,
                    item_schema,
                    f"{gid}.evaluationReceipts[{index}]",
                    findings,
                    "RV2",
                )

        expected = golden.get("expected")
        validate_closed_object(expected, expected_schema, f"{gid}.expected", findings, "RV3")

        if isinstance(axes_value, dict) and isinstance(expected, dict):
            try:
                actual = derive(axes_value)
            except (KeyError, TypeError) as exc:
                findings.append(f"RV4 {gid}: derivation failed: {exc}")
            else:
                if actual != expected:
                    findings.append(f"RV4 {gid}: derived {actual!r}, expected {expected!r}")
            reason = expected.get("reasonCode")
            if isinstance(reason, str):
                seen_reasons.add(reason)
            if expected.get("classification") == "durable-pass":
                for receipt in axes_value.get("evaluationReceipts", []):
                    seen_success_modes.add(receipt.get("custody"))

    # RV5 — exact counterexamples that motivated v3 cannot silently disappear.
    required_reasons = {
        "PROOF.CAPABILITY_INSUFFICIENT",
        "PROOF.DURABILITY_REQUIRED",
        "STORAGE.POLICY_REQUIRED",
        "STORAGE.ROOT_UNSAFE",
        "PROOF.EVALUATION_RECEIPT_MISSING",
        "PROOF.OBLIGATION_UNTRUSTED",
        "PROOF.VERIFIER_OR_ROOT_MISSING",
        "PROOF.FROZEN_BODY_MISSING",
        "PROOF.WITNESS_INSUFFICIENT",
        "PRIVACY.SOURCE_RETENTION_NOT_GRANTED",
        "PROOF.BUDGET_EXHAUSTED",
        "PROOF.REGENERATION_CLOSURE_MISSING",
        "PROOF.VERDICT_RECEIPT_MISSING",
        "REPLAY.CLOSURE_MISSING",
    }
    for missing in sorted(required_reasons - seen_reasons):
        findings.append(f"RV5: no golden covers {missing}")
    if not {"frozen", "regenerable"}.issubset(seen_success_modes):
        findings.append("RV5: durable-pass goldens do not cover both frozen and regenerable custody")

    # RV6 — prevent a later prose edit from restoring finding-only/self-attested proof.
    proof = contract.get("proofContract", {})
    manifest_required = set(proof.get("manifest", {}).get("required", []))
    evaluation_required = set(proof.get("evaluationReceipt", {}).get("required", []))
    verdict_required = set(proof.get("verdictReceipt", {}).get("required", []))
    if not {"evaluationReceiptRefs", "verdictReceiptRef", "evaluationSetRoot"}.issubset(manifest_required):
        findings.append("RV6: RunProofManifest no longer requires complete evaluation/verdict references")
    if not {
        "proofObligationId", "verifierId", "proofRoot", "coverageRefs",
        "subjectUniverseRef", "custody",
    }.issubset(evaluation_required):
        findings.append("RV6: EvaluationReceipt lost a host-verifiable proof dependency")
    if not {"evaluationReceiptRoot", "proofObligationId", "verifierId", "proofRoot"}.issubset(verdict_required):
        findings.append("RV6: VerdictReceipt lost a host-verifiable derivation dependency")
    custody_variants = {
        item.get("mode"): set(item.get("required", []))
        for item in proof.get("custodyUnion", {}).get("variants", [])
    }
    if "proofBodyRef" not in custody_variants.get("frozen", set()):
        findings.append("RV6: frozen custody no longer requires the committed proof body")
    if "regenerationClosureRef" not in custody_variants.get("regenerable", set()):
        findings.append("RV6: regenerable custody no longer requires its exact closure")
    payload_kinds = {
        item["kind"] for item in contract.get("hostOwnedProofObligations", {}).get("requiredPayloadKinds", [])
    }
    required_kinds = {
        "predicate-match", "no-match-closed-set", "path-membership",
        "complete-set-aggregate", "metric-derivation", "policy-baseline",
        "external-observation", "composite-derivation-dag",
    }
    if payload_kinds != required_kinds:
        findings.append(f"RV6: proof payload kinds differ: {sorted(payload_kinds)!r}")

    return findings


def main() -> int:
    path = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path(__file__).with_name(
        "retention-tiers.v3.json"
    )
    try:
        contract = load(path)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot read retention contract {path}: {exc}", file=sys.stderr)
        return 2
    findings = check(contract)
    count = len(contract.get("goldenCases", []))
    if not findings:
        print(f"retention v3 exploration internally consistent — {count} goldens, RV1..RV6 clean; known A1-RTV3-01/02 semantic defects remain")
        return 0
    print(f"{len(findings)} finding(s) across {count} goldens:")
    for finding in findings:
        print("  -", finding)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
