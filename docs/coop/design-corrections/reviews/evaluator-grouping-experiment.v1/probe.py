"""Bounded design experiment: aggregation and enumeration outcome composition.

Not an OpenSIP evaluator, schema admission, complete Run replay, or qualification.
Inputs below are explicit hypothetical observations, never admitted product facts.
Effective gating and emitted findings are preconditions supplied by other pending
evaluator work. Native population/extraction, selectors, imports and waivers are
not implemented here. Only the proposed composition laws are exercised.
"""
import copy
import itertools
import json


class Refusal(ValueError):
    pass


def stable(value):
    # ASCII experiment fixtures only; NOT the product canonicalizer.
    return json.dumps(value, sort_keys=True, separators=(",", ":"))


BASELINE_FIELDS = (
    "fingerprint", "ruleId", "detectorId", "stabilityClass", "subjectPath", "waived"
)


def project_baseline(occurrences):
    """Keep original findings intact; collapse only identical baseline projections."""
    by_fingerprint = {}
    occurrence_keys = set()
    for occurrence in occurrences:
        key = (occurrence["ruleId"], occurrence["universe"], occurrence["nativeSubjectId"])
        if key in occurrence_keys:
            raise Refusal("duplicate evaluation occurrence")
        occurrence_keys.add(key)
        projection = {k: occurrence[k] for k in BASELINE_FIELDS}
        if "legacyFingerprint" in occurrence:
            if type(occurrence["legacyFingerprint"]) is not str or not occurrence["legacyFingerprint"]:
                raise Refusal("invalid legacy fingerprint")
            projection["legacyFingerprint"] = occurrence["legacyFingerprint"]
        if type(projection["waived"]) is not bool:
            raise Refusal("waived must be boolean")
        fp = projection["fingerprint"]
        if fp in by_fingerprint and by_fingerprint[fp] != projection:
            raise Refusal("conflicting logical baseline projection")
        by_fingerprint[fp] = projection
    return [by_fingerprint[k] for k in sorted(by_fingerprint)]


def compose(rule_rows, occurrences, required_execution_incomplete=False):
    """Compose observed enumeration uncertainty with already evaluated findings.

    Each rule is present even for zero known candidates. A disabled rule has no
    execution obligation. Unavailable population and unresolved export membership
    are uncertainty. Missing promised bytes are an admission error, not this input.
    """
    rules = {}
    disclosures = []
    for row in rule_rows:
        rid = row["ruleId"]
        if rid in rules:
            raise Refusal("duplicate rule result")
        if any(type(row[k]) is not bool for k in ("enabled", "effectiveGating")):
            raise Refusal("rule flags must be boolean")
        if type(row["unresolvedExportCount"]) is not int or row["unresolvedExportCount"] < 0:
            raise Refusal("invalid unresolved export count")
        if row["population"] not in ("complete", "unavailable"):
            raise Refusal("invalid population status")
        rules[rid] = row
        if row["enabled"]:
            if row["population"] == "unavailable":
                disclosures.append((rid, "population-unavailable"))
            if row["unresolvedExportCount"]:
                disclosures.append((rid, "export-membership-unknown"))
    for occurrence in occurrences:
        row = rules.get(occurrence["ruleId"])
        if row is None or not row["enabled"]:
            raise Refusal("finding outside enabled rule set")
    baseline = project_baseline(occurrences)
    failing = any(rules[f["ruleId"]]["effectiveGating"] and not f["waived"] for f in occurrences)
    uncertain = required_execution_incomplete or any(rules[r]["effectiveGating"] for r, _ in disclosures)
    return {
        "verdict": "fail" if failing else "indeterminate" if uncertain else "pass",
        "disclosures": sorted(disclosures),
        "baseline": baseline,
        # Full occurrence payload remains present; neither parameters nor citations
        # are flattened to a representative or compared by count.
        "occurrences": sorted(copy.deepcopy(occurrences), key=stable),
    }


def run():
    cases = []

    def check(name, fn):
        fn()
        cases.append({"case": name, "result": "PASS"})

    def equal(actual, expected):
        assert actual == expected, (actual, expected)

    def refused(fn):
        try:
            fn()
        except Refusal:
            return
        raise AssertionError("expected refusal")

    rule = {"ruleId": "rule-a", "enabled": True, "effectiveGating": True,
            "population": "complete", "unresolvedExportCount": 0}
    finding = {"fingerprint": "logical-a", "ruleId": "rule-a", "detectorId": "detector-a",
               "stabilityClass": "path-stable", "subjectPath": "src/a.ts", "waived": False,
               "universe": "config-a", "nativeSubjectId": "symbol-a",
               "messageCode": "example", "parameters": {"count": 1}, "evidenceRefs": ["evidence-a"]}
    second = dict(finding, universe="config-b", parameters={"count": 2}, evidenceRefs=["evidence-b"])
    unknown = dict(rule, unresolvedExportCount=3)
    check("two-config-findings-one-baseline-full-parameters-retained", lambda: (
        equal(len(compose([rule], [finding, second])["baseline"]), 1),
        equal(len(compose([rule], [finding, second])["occurrences"]), 2),
        equal({f["parameters"]["count"] for f in compose([rule], [finding, second])["occurrences"]}, {1, 2})))
    check("all-occurrence-permutations-identical", lambda: [
        equal(compose([rule], list(order)), compose([rule], [finding, second]))
        for order in itertools.permutations([finding, second])])
    check("universe-input-churn-does-not-create-baseline-entry", lambda:
          equal(project_baseline([finding]), project_baseline([dict(finding, universe="changed-inputs")])) )
    check("same-fingerprint-conflicting-path-refused", lambda:
          refused(lambda: project_baseline([finding, dict(second, subjectPath="src/b.ts")])))
    check("same-fingerprint-conflicting-waiver-refused", lambda:
          refused(lambda: project_baseline([finding, dict(second, waived=True)])))
    check("same-fingerprint-conflicting-legacy-migration-refused", lambda:
          refused(lambda: project_baseline([finding, dict(second, legacyFingerprint="legacy-a")])) )
    check("agreed-legacy-fingerprint-preserved", lambda:
          equal(project_baseline([dict(finding, legacyFingerprint="legacy-a"),
                                  dict(second, legacyFingerprint="legacy-a")])[0]["legacyFingerprint"], "legacy-a"))
    check("duplicate-evaluation-occurrence-refused", lambda:
          refused(lambda: project_baseline([finding, copy.deepcopy(finding)])))
    check("zero-findings-unresolved-export-is-indeterminate", lambda:
          equal(compose([unknown], [])["verdict"], "indeterminate"))
    check("complete-empty-population-is-distinct", lambda:
          equal(compose([rule], [])["verdict"], "pass"))
    check("unavailable-population-is-not-complete-empty", lambda:
          equal(compose([dict(rule, population="unavailable")], [])["verdict"], "indeterminate"))
    check("known-gating-finding-dominates-other-export-uncertainty", lambda:
          equal(compose([unknown], [finding])["verdict"], "fail"))
    check("waiver-does-not-cure-export-uncertainty", lambda:
          equal(compose([unknown], [dict(finding, waived=True)])["verdict"], "indeterminate"))
    check("advisory-uncertainty-remains-disclosed", lambda: (
        equal(compose([dict(unknown, effectiveGating=False)], [])["verdict"], "pass"),
        equal(compose([dict(unknown, effectiveGating=False)], [])["disclosures"], [("rule-a", "export-membership-unknown")]) ))
    check("required-execution-deficiency-survives-advisory-policy", lambda:
          equal(compose([dict(unknown, effectiveGating=False)], [], True)["verdict"], "indeterminate"))
    check("disabled-rule-has-no-enumeration-deficiency", lambda:
          equal(compose([dict(unknown, enabled=False)], [])["disclosures"], []))
    check("disabled-rule-finding-refused", lambda:
          refused(lambda: compose([dict(rule, enabled=False)], [finding])))
    # Discriminating counterexample: count-only replay would accept each mutation;
    # complete comparison of this LIMITED projected result detects every mutation.
    original = compose([rule], [finding])
    mutants = [dict(finding, parameters={"count": 9}), dict(finding, evidenceRefs=["wrong"]),
               dict(finding, messageCode="changed"), dict(finding, universe="different")]
    def compare_mutants():
        for mutant in mutants:
            changed = compose([rule], [mutant])
            equal(len(original["occurrences"]), len(changed["occurrences"]))
            assert original != changed
    check("same-count-parameter-citation-message-universe-mutations-detected", compare_mutants)
    return {"standing": "Bounded Codex design experiment; NOT complete retained-Run replay, schema admission or product qualification",
            "caseCount": len(cases), "cases": cases,
            "assumptions": ["ASCII fixtures are hypothetical observations, not admitted facts",
                            "effectiveGating and findings already decided by pending G3-G9 laws",
                            "GR3 population completeness is an input, not proved by this experiment",
                            "legacyFingerprint value/presence must agree; actual recipe migration is not implemented",
                            "operational errors handled outside sealed verdict composition"]}


if __name__ == "__main__":
    print(json.dumps(run(), indent=2))
