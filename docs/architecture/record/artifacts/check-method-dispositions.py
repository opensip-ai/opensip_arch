#!/usr/bin/env python3
"""Validate terminal dispositions for non-product method claims.

The three subjects are intentionally removed from the live claim lattice.  This
does not call them SEALED: it records why the broad claim was abandoned or what
narrow process guidance survived, and prevents an unanswered meta-question from
silently remaining OPEN at architecture freeze.

Usage: python3 artifacts/check-method-dispositions.py [contract] [--selftest]
"""
from __future__ import annotations

import copy
import json
import pathlib
import sys


HERE = pathlib.Path(__file__).resolve().parent
ROOT = HERE.parent
BINDING = "method-claim-dispositions.v1.json"
REGISTER = "claim-register.v1.json"
EXPECTED = {
    "METHOD.CLAIM-STATUS-INTEGRITY": "ABANDONED-BROAD-CLAIM",
    "METHOD.ALTITUDE": "NARROWED-TO-PROCESS-GUIDANCE",
    "CLEANSHEET.VERDICT": "ABANDONED-NON-GATING",
}
FACTORS = {
    "blast-radius", "external-custody", "ownership-boundary",
    "reversibility", "change-cost",
}


# ------------------------------------------------------ the parse primitive
#
# json.loads without an object_pairs_hook keeps the LAST of a duplicated key, so
# a document can say one thing to a human reader and another to every
# instrument, with the parsed object byte-identical to the honest one.  Every
# JSON byte this checker reads — the contract AND the claim register, because a
# defence applied to the candidate and not to its siblings is only half a
# defence — enters through jloads(), which RECORDS each repeated key against its
# own path and reports it as a named finding at that position rather than
# raising.  An operator who is told only that the file is bad does not learn
# which key was duplicated or where it sits; these findings name both.

# label -> findings, for every parse this process performed.  A duplicate key is
# a property of the BYTES, so it is recorded where the bytes were read and
# reported by check() rather than thrown from the parse.
_PARSES: dict[str, list[str]] = {}


def _duplicate_paths(node, steps: list, marks: dict, out: list) -> None:
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


def jloads(text: str, label: str) -> tuple[object, list[str]]:
    """Parse JSON and report every key the BYTES publish more than once."""
    marks: dict = {}
    keep: list = []

    def pairs(items: list[tuple[str, object]]) -> dict:
        out: dict = {}
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
    found: list = []
    if marks:
        _duplicate_paths(value, [], marks, found)
    problems = [
        f"MD-DUPKEY {label}: key '{key}' is published more than once at "
        f"{path or '<document root>'}; the host parser keeps the LAST "
        f"occurrence, so the parsed document cannot say what the bytes say"
        for path, key in found
    ]
    declared = sum(len(v) for v in marks.values())
    if len(found) < declared:
        problems.append(
            f"MD-DUPKEY {label}: {declared - len(found)} duplicate key(s) sit in "
            f"an object the parse itself discarded, so this run cannot resolve "
            f"their path; they are refused regardless")
    if len(keep) != len(marks):
        problems.append(
            f"MD-DUPKEY {label}: the duplicate-key record and the objects it "
            f"refers to disagree in cardinality")
    _PARSES[label] = problems
    return value, problems


def parse_findings() -> list[str]:
    """Every duplicate-key finding recorded by every parse this run performed."""
    out: list[str] = []
    for problems in _PARSES.values():
        out.extend(problems)
    return out


def load(path: pathlib.Path) -> dict:
    """Every JSON file this checker reads enters here, and there is no other
    door."""
    path = pathlib.Path(path)
    value, _problems = jloads(path.read_text(), path.name)
    return value


def evidence_file(ref: str) -> pathlib.Path:
    return ROOT / ref.split("#", 1)[0]


def fixture_errors(fixture: dict) -> list[str]:
    errors: list[str] = []
    ids = fixture.get("dispositionIds")
    if ids is not None and set(ids) != set(EXPECTED):
        errors.append("disposition denominator is not exact")
    if fixture.get("liveClaimId") in EXPECTED:
        errors.append("terminally dispositioned ID remains a live claim")
    if fixture.get("rerunRequired") is True:
        errors.append("abandoned clean-sheet verdict was turned back into required work")
    if fixture.get("assuranceEffect") not in (None, "NONE"):
        errors.append("process guidance was promoted into assurance")
    if fixture.get("replacementKind") not in (None, "DIAGNOSTIC-ONLY"):
        errors.append("bounded checker was promoted into complete proof")
    return errors


def check(contract: dict, register: dict, check_narrative: bool = True) -> list[str]:
    # A duplicated key is a property of the bytes that were read, not of the
    # dict those bytes produced, so it is carried in from the parse record.  It
    # leads because no other finding can be trusted while the document the
    # instrument parsed differs from the document a reader sees.
    errors: list[str] = parse_findings()
    dispositions_list = contract.get("dispositions", [])
    dispositions = {item.get("id"): item for item in dispositions_list}
    if len(dispositions) != len(dispositions_list) or set(dispositions) != set(EXPECTED):
        errors.append("MD-SET: disposition set is not the exact three non-product claims")

    required = contract.get("registerRule", {}).get("requiredEntries", [])
    wanted_entries = [
        {
            "id": claim_id,
            "disposition": disposition,
            "artifact": "artifacts/method-claim-dispositions.v1.json",
        }
        for claim_id, disposition in EXPECTED.items()
    ]
    if required != wanted_entries:
        errors.append("MD-REGISTER: contract register entries are not exact")

    live_ids = {item.get("id") for item in register.get("claims", [])}
    still_live = sorted(set(EXPECTED) & live_ids)
    if still_live:
        errors.append(f"MD-REGISTER: terminal dispositions remain live claims: {still_live}")
    if register.get("nonProductClaimDispositions") != wanted_entries:
        errors.append("MD-REGISTER: claim register has not indexed the terminal dispositions")
    narrative = contract.get("registerRule", {}).get("requiredNarrative", {})
    validator = register.get("validator", {})
    if register.get("purpose") != narrative.get("purpose") or \
            validator.get("selfTestProves") != narrative.get("validatorSelfTestProves") or \
            validator.get("liveStatus") != narrative.get("validatorLiveStatus") or \
            register.get("knownLimitations") != narrative.get("knownLimitations"):
        errors.append("MD-REGISTER: claim-register narrative still promotes or describes the abandoned broad claim")

    for claim_id, expected_disposition in EXPECTED.items():
        item = dispositions.get(claim_id, {})
        if item.get("disposition") != expected_disposition:
            errors.append(f"MD-SET {claim_id}: wrong terminal disposition")
        for key in ("priorClaim", "priorStatus", "decision", "reason",
                    "retainedValue", "forbiddenUse", "evidence"):
            if not item.get(key):
                errors.append(f"MD-SET {claim_id}: missing {key}")
        if item.get("doesNotGateArchitectureFreeze") is not True:
            errors.append(f"MD-SET {claim_id}: still gates architecture freeze")
        for ref in item.get("evidence", []):
            if not evidence_file(ref).exists():
                errors.append(f"MD-EVIDENCE {claim_id}: missing {ref}")

    csi = dispositions.get("METHOD.CLAIM-STATUS-INTEGRITY", {})
    if csi.get("replacementScope", {}).get("kind") != "DIAGNOSTIC-ONLY" or \
            "complete" not in csi.get("priorClaim", "").lower():
        errors.append("MD-CSI: broad completeness claim was not abandoned for bounded diagnostics")

    altitude = dispositions.get("METHOD.ALTITUDE", {})
    guidance = altitude.get("processGuidance", {})
    if set(guidance.get("classificationFactors", [])) != FACTORS or \
            guidance.get("assuranceEffect") != "NONE" or \
            "invariant" not in guidance.get("implementationHandoff", "").lower() or \
            "binding" not in guidance.get("implementationHandoff", "").lower():
        errors.append("MD-ALT: consequence guidance is incomplete or promoted to assurance")

    clean = dispositions.get("CLEANSHEET.VERDICT", {})
    if clean.get("wholeDesignVerdict") != "NOT-AUTHORIZED" or \
            clean.get("rerunRequired") is not False:
        errors.append("MD-CLEAN: abandoned verdict was authorized or made required again")

    for fixture in contract.get("fixtures", []):
        got = fixture_errors(fixture)
        if fixture.get("valid") and got:
            errors.append(f"MD-FX {fixture.get('id')}: expected valid — {got[0]}")
        elif not fixture.get("valid") and not got:
            errors.append(f"MD-FX {fixture.get('id')}: expected rejection")

    if check_narrative:
        method = (ROOT / "architecture" / "10-method.md").read_text()
        trace = (ROOT / "architecture" / "11-traceability.md").read_text()
        for claim_id in EXPECTED:
            marker = f"<!-- disposition:{claim_id} -->"
            if marker not in method and marker not in trace:
                errors.append(f"MD-NARRATIVE {claim_id}: disposition marker absent")
    return errors


def integrated_register(register: dict, contract: dict) -> dict:
    candidate = copy.deepcopy(register)
    candidate["claims"] = [
        claim for claim in candidate.get("claims", []) if claim.get("id") not in EXPECTED
    ]
    candidate["nonProductClaimDispositions"] = copy.deepcopy(
        contract["registerRule"]["requiredEntries"]
    )
    narrative = contract["registerRule"]["requiredNarrative"]
    candidate["purpose"] = narrative["purpose"]
    candidate["knownLimitations"] = copy.deepcopy(narrative["knownLimitations"])
    candidate.setdefault("validator", {})["selfTestProves"] = narrative[
        "validatorSelfTestProves"
    ]
    candidate["validator"]["liveStatus"] = narrative["validatorLiveStatus"]
    return candidate


def selftest(contract: dict, register: dict) -> int:
    base_register = integrated_register(register, contract)
    base = check(contract, base_register)
    if base:
        print(f"REFUSING to self-test: integrated base has {len(base)} finding(s)")
        for item in base[:10]:
            print("  -", item)
        return 1

    def drop_disposition(c: dict, _: dict) -> None:
        c["dispositions"].pop()

    def restore_live_clean(_: dict, r: dict) -> None:
        r["claims"].append({"id": "CLEANSHEET.VERDICT", "status": "OPEN"})

    def require_rerun(c: dict, _: dict) -> None:
        for item in c["dispositions"]:
            if item["id"] == "CLEANSHEET.VERDICT":
                item["rerunRequired"] = True

    def promote_altitude(c: dict, _: dict) -> None:
        for item in c["dispositions"]:
            if item["id"] == "METHOD.ALTITUDE":
                item["processGuidance"]["assuranceEffect"] = "SEALED"

    def promote_diagnostic(c: dict, _: dict) -> None:
        for item in c["dispositions"]:
            if item["id"] == "METHOD.CLAIM-STATUS-INTEGRITY":
                item["replacementScope"]["kind"] = "COMPLETE-PROOF"

    def drop_evidence(c: dict, _: dict) -> None:
        c["dispositions"][0]["evidence"] = []

    def drift_register(_: dict, r: dict) -> None:
        r["nonProductClaimDispositions"][0]["disposition"] = "SEALED"

    def restore_candidate_narrative(_: dict, r: dict) -> None:
        r["validator"]["liveStatus"] = "METHOD.CLAIM-STATUS-INTEGRITY remains CANDIDATE"

    mutations = [
        ("drop one terminal disposition", drop_disposition),
        ("leave CLEANSHEET.VERDICT silently OPEN", restore_live_clean),
        ("make the 138-row rerun required", require_rerun),
        ("promote altitude guidance into assurance", promote_altitude),
        ("promote bounded diagnostics into complete proof", promote_diagnostic),
        ("remove evidence for a disposition", drop_evidence),
        ("let register disposition drift", drift_register),
        ("leave stale CANDIDATE narrative in the register", restore_candidate_narrative),
    ]
    print("method-disposition mutation self-test — each row must be REJECTED\n")
    escaped = 0
    for name, mutation in mutations:
        candidate = copy.deepcopy(contract)
        candidate_register = copy.deepcopy(base_register)
        mutation(candidate, candidate_register)
        findings = check(candidate, candidate_register)
        if not findings:
            escaped += 1
        print(f"  {'reject' if findings else 'ESCAPE':>6}  {name}")
        print(f"          {findings[0] if findings else 'NO FINDING — mutation survived'}")

    # Duplicate-key rows.  A duplicated key is a property of the BYTES, so these
    # rows drive jloads() on crafted text rather than mutating a parsed dict —
    # the dict a mutation produces cannot express "this key appeared twice".
    # The last row is a CONTROL: a guard that fires on every document proves
    # nothing, so an honest document must produce no finding.
    parse_rows = [
        ("duplicate key at the document root",
         '{"status": "PLANTED", "status": "REAL"}', "status", "status"),
        ("duplicate key nested inside an array element",
         '{"dispositions": [{"disposition": "PLANTED", "disposition": "REAL"}]}',
         "disposition", "dispositions[0].disposition"),
        ("duplicate key that repeats three times",
         '{"id": "A", "id": "B", "id": "C"}', "id", "id"),
        ("CONTROL: honest document, no duplicate", '{"status": "REAL"}',
         None, None),
    ]
    print("\n  duplicate-key rows — the parse must NAME the key and its position\n")
    for name, text, key, path in parse_rows:
        _value, problems = jloads(text, "selftest")
        _PARSES.pop("selftest", None)
        if key is None:
            ok = not problems
            detail = problems[0] if problems else "no finding, as required"
        else:
            ok = bool(problems) and f"key '{key}'" in problems[0] and \
                f"at {path};" in problems[0]
            detail = problems[0] if problems else \
                "NO FINDING — duplicate key survived"
        if not ok:
            escaped += 1
        print(f"  {'reject' if ok else 'ESCAPE':>6}  {name}")
        print(f"          {detail}")

    total = len(mutations) + len(parse_rows)
    print()
    if escaped:
        print(f"{escaped}/{total} rows ESCAPED")
        return 1
    print(f"all {total} rows rejected — no silent OPEN meta-claim remains, and "
          f"no duplicated key can reach a verdict unnamed")
    return 0


def main() -> int:
    args = [arg for arg in sys.argv[1:] if arg != "--selftest"]
    path = pathlib.Path(args[0]) if args else HERE / BINDING
    if not path.exists():
        print(f"missing contract: {path}", file=sys.stderr)
        return 2
    try:
        contract = load(path)
        register = load(HERE / REGISTER)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"cannot load disposition inputs: {exc}", file=sys.stderr)
        return 2
    if "--selftest" in sys.argv:
        return selftest(contract, register)
    findings = check(contract, register)
    if findings:
        print(f"{len(findings)} method-disposition finding(s):")
        for item in findings:
            print("  -", item)
        return 1
    print("method dispositions OK — 3/3 terminal, evidence-backed, non-gating")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
