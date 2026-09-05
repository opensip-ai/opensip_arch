#!/usr/bin/env python3
"""Validate a completed clean-sheet comparison against the pre-registered rule.

Rule: artifacts/cleansheet-adjudication-rule.v1.md

This exists because the rule's mechanisms are skippable by a motivated adjudicator.
The checker makes the skips visible:

  A1  every decision has exactly one class and a recorded disposition
  A2  every INCUMBENT-affecting disposition records a Justification Test result
  A3  every ONLY-INCUMBENT retention names a forcing requirement
  A4  no justification cites the existing implementation (rule: that is a failure)
  A5  MATCH where incumbent=FORCED and cleansheet=PREFERRED is downgraded
  A6  DIVERGE resolved for the incumbent only if the test passed
  A7  every disposition records the evidence used
  A8  no adjudicator adjudicates a decision they authored
  A9  the pre-committed metrics are present

Usage: python3 artifacts/check-adjudication.py <comparison.json>
Exit:  0 conforms · 1 findings · 2 IO error
"""
from __future__ import annotations
import json, re, sys, pathlib

CLASSES = {"MATCH", "DIVERGE", "ONLY-INCUMBENT", "ONLY-CLEANSHEET"}
# Phrases that mean a justification is leaning on the existing implementation.
CONTAMINATED = re.compile(
    r"current (system|implementation|code|design|package)|existing (system|implementation|corpus|code)"
    r"|today'?s|shipping product|the repo\b|as (built|shipped)|legacy|would require rewrit"
    r"|migration cost|porting cost|inverts?\b|pain point|too expensive to change",
    re.I)
REQUIRED_METRICS = {
    "incumbentPassedJustification", "incumbentFailedJustification",
    "forcedDowngradedToPreferred", "onlyIncumbentCount",
    "onlyIncumbentRemoved", "onlyCleansheetCount", "unresolvedCount",
}


# ------------------------------------------------------ the parse primitive
#
# json.loads without an object_pairs_hook keeps the LAST of a duplicated key, so
# a comparison can say one thing to a human reader and another to this checker,
# with the parsed object byte-identical to the honest one — a decision could
# read "RETAINED" on the page while A1..A9 score the "DOWNGRADED" the parser
# kept.  Every JSON byte this checker reads enters through jloads(), which
# RECORDS each repeated key against its own path and reports it as a named
# finding at that position rather than raising.  An operator who is told only
# that the file is bad does not learn which key was duplicated or where it sits;
# these findings name both.

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


def jloads(text: str, label: str) -> tuple:
    """Parse JSON and report every key the BYTES publish more than once."""
    marks: dict = {}
    keep: list = []

    def pairs(items: list) -> dict:
        out: dict = {}
        repeated: list = []
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
        f"A0-DUPKEY {label}: key '{key}' is published more than once at "
        f"{path or '<document root>'}; the host parser keeps the LAST "
        f"occurrence, so the parsed comparison cannot say what the bytes say"
        for path, key in found
    ]
    declared = sum(len(v) for v in marks.values())
    if len(found) < declared:
        problems.append(
            f"A0-DUPKEY {label}: {declared - len(found)} duplicate key(s) sit in "
            f"an object the parse itself discarded, so this run cannot resolve "
            f"their path; they are refused regardless")
    if len(keep) != len(marks):
        problems.append(
            f"A0-DUPKEY {label}: the duplicate-key record and the objects it "
            f"refers to disagree in cardinality")
    _PARSES[label] = problems
    return value, problems


def parse_findings() -> list[str]:
    """Every duplicate-key finding recorded by every parse this run performed."""
    out: list[str] = []
    for problems in _PARSES.values():
        out.extend(problems)
    return out


def load(p: pathlib.Path) -> dict:
    """Every JSON file this checker reads enters here, and there is no other
    door."""
    p = pathlib.Path(p)
    value, _problems = jloads(p.read_text(), p.name)
    return value


def check(c: dict) -> list[str]:
    # A duplicated key is a property of the bytes that were read, not of the
    # dict those bytes produced, so it is carried in from the parse record.  It
    # leads because no A1..A9 result can be trusted while the comparison this
    # checker parsed differs from the comparison an adjudicator reads.
    f: list[str] = parse_findings()
    for d in c.get("decisions", []):
        did = d.get("id", "<no-id>")
        cls = d.get("class")

        # A1
        if cls not in CLASSES:
            f.append(f"A1 {did}: class '{cls}' invalid")
        if not d.get("disposition"):
            f.append(f"A1 {did}: no disposition recorded")

        jt = d.get("justificationTest")
        # A MATCH whose FORCED claim is already DOWNGRADED has surrendered the
        # necessity claim, so there is nothing left to justify.
        affects_incumbent = cls in ("DIVERGE", "ONLY-INCUMBENT") or (
            cls == "MATCH" and d.get("incumbentForcing") == "FORCED"
            and d.get("disposition") != "DOWNGRADED")

        # A2
        if affects_incumbent and not isinstance(jt, dict):
            f.append(f"A2 {did}: {cls} requires a justificationTest result")
        elif isinstance(jt, dict):
            if jt.get("result") not in ("PASS", "FAIL"):
                f.append(f"A2 {did}: justificationTest.result must be PASS or FAIL")
            stated = str(jt.get("statedRequirement", ""))
            # A4 — a justification that cites the incumbent is a FAIL by rule
            if jt.get("result") == "PASS":
                if not stated.strip():
                    f.append(f"A4 {did}: PASS with no stated requirement")
                elif CONTAMINATED.search(stated):
                    f.append(f"A4 {did}: PASS cites the existing implementation "
                             f"— rule says this is a FAIL")

        # A3
        if cls == "ONLY-INCUMBENT" and d.get("disposition") == "RETAINED":
            if not d.get("forcingRequirement"):
                f.append(f"A3 {did}: RETAINED without a forcing requirement")
            if not (isinstance(jt, dict) and jt.get("result") == "PASS"):
                f.append(f"A3 {did}: RETAINED but justification test did not pass")

        # A5
        if cls == "MATCH" and d.get("incumbentForcing") == "FORCED" \
           and d.get("cleansheetForcing") == "PREFERRED":
            if d.get("disposition") != "DOWNGRADED":
                f.append(f"A5 {did}: FORCED vs PREFERRED must be DOWNGRADED, "
                         f"got '{d.get('disposition')}'")

        # A6
        if cls == "DIVERGE" and d.get("disposition") == "INCUMBENT-WINS":
            if not (isinstance(jt, dict) and jt.get("result") == "PASS"):
                f.append(f"A6 {did}: INCUMBENT-WINS requires a passing justification test")
            if not d.get("tieBreakerApplied"):
                f.append(f"A6 {did}: INCUMBENT-WINS requires a recorded tie-breaker "
                         f"(contracts / moving parts / reversibility)")

        # A7
        if not d.get("evidence"):
            f.append(f"A7 {did}: no evidence recorded — disposition is void")

        # A8
        a, auth = d.get("adjudicator"), d.get("incumbentAuthor")
        if a and auth and a == auth:
            f.append(f"A8 {did}: adjudicator '{a}' authored the incumbent decision")
        # A8b — rule disqualifies Agent 3 from adjudicating incumbent decisions it
        # authored. Setting incumbentAuthor to a decorative alias (e.g.
        # "agent-3-AUTHOR-CONFLICT") previously green-washed a disqualified run.
        if a == "agent-3" and d.get("class") in (
            "MATCH", "DIVERGE", "ONLY-INCUMBENT"
        ):
            f.append(
                f"A8 {did}: adjudicator agent-3 is disqualified for incumbent "
                f"decisions (cleansheet-adjudication-rule.v1 Who adjudicates)"
            )

    # A9
    m = c.get("metrics") or {}
    for k in sorted(REQUIRED_METRICS - set(m)):
        f.append(f"A9: pre-committed metric '{k}' missing")

    if not c.get("ruleVersion"):
        f.append("A9: comparison does not state which rule version governs it")
    return f


def main() -> int:
    if len(sys.argv) < 2:
        print(__doc__.strip().splitlines()[-3], file=sys.stderr)
        return 2
    p = pathlib.Path(sys.argv[1])
    if not p.exists():
        print(f"missing comparison: {p}", file=sys.stderr)
        return 2
    c = load(p)
    f = check(c)
    n = len(c.get("decisions", []))
    if not f:
        print(f"comparison conforms to the rule — {n} decisions, A1..A9 clean")
        return 0
    print(f"{len(f)} conformance finding(s) across {n} decisions:")
    for x in f:
        print("  -", x)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
