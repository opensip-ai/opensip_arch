#!/usr/bin/env python3
"""Retained executable checker for the D9 termination contract.

History of what this checker itself got wrong, because that is the point:

  v1.3  claimed "39/39 executed" while the executable lived outside the artifact
        set, so the claim was not reproducible from the binding object.
  v1.4  compared derived class against expected class only, never validating the
        goldens against the artifact's OWN schema — so v1.3 shipped 38 forbidden
        exitCode fields, 2 explicit nulls, 3 undeclared axes and 5 out-of-vocab
        codes while reporting clean.
  v1.5  B-D9V15-01: the D10 proof path was OPTIONAL. `maps = c.get("codeMaps")`
        followed by `if maps and ax` meant deleting the entire codeMaps object
        left the checker green.
  v1.6 adjudication (agent-a / R2-D9-04..05): causeModel and crossAxisInvariants
        were prose-only — deleting them or reversing precedence left the checker
        green. Concurrent-condition reduction is now executable. Golden top-level
        commandKind must equal scenarioAxes.commandKind.

  D1  every golden has a falsifiable scenario sentence
  D2  axes conform to the declared schema (enums, additionalProperties, no nulls)
  D3  termination payloads conform to their union variant
  D4  no payload carries a forbidden field (exitCode is derived, never stored)
  D5  every reason/error code is in the declared closed vocabulary
  D6  the pure derivation reproduces every expected class
  D7  class -> exit code agrees with the class table
  D8  every termination class has at least one golden
  D9  the finalization transition table leaves settled terminations unchanged
  D10 axes determine the FULL ordered code payload, not just the class
  D11 codeMaps are present, total over their enums, injective, and in-vocabulary
  D12 cross-axis invariants X1..X10 hold AND are declared in the artifact
  D13 cause exclusivity holds and every cause enum value has a golden
  D14 causeModel is present with the binding fault>rejection>deficiency order
  D15 concurrent-condition goldens reduce via causeModel.precedence
  D16 golden commandKind equals scenarioAxes.commandKind

Usage: python3 artifacts/check-d9.py [contract]   ·   --selftest
Exit:  0 clean · 1 findings · 2 IO error
"""
from __future__ import annotations
import copy, json, sys, pathlib

BINDING = "d9-exit-contract.v1.6.json"
EXPECTED_VERSION = "v1.6"
TOTALITY_ROOT_CASES = (
    ("string", "hostile-root"),
    ("null", None),
    ("list", []),
    ("empty-object", {}),
)
TOTALITY_NESTED_CASES = TOTALITY_ROOT_CASES
MALFORMED_SHAPE_EXCEPTIONS = (
    AttributeError, IndexError, KeyError, StopIteration, TypeError, ValueError,
)
FORBIDDEN_PAYLOAD_FIELDS = {"exitCode"}
CAUSES = ("deficiency", "rejectionCause", "faultCause")
MAP_FOR = {"deficiency": "deficiencyToReasonCode",
           "rejectionCause": "rejectionCauseToErrorCode",
           "faultCause": "faultCauseToErrorCode"}
REQUIRED_PRECEDENCE = ["faultCause", "rejectionCause", "deficiency"]
REQUIRED_X_IDS = {f"X{i}" for i in range(1, 11)}


def derive_class(ax: dict) -> str:
    """Pure axes -> HostTermination class. Ordered; first match wins.
    Every predicate reads an input axis; none reads the derivation's own output."""
    ck = ax["commandKind"]

    if ck == "serve":
        return "success" if ax["domainCondition"] in (
            "clean-shutdown", "graceful-signal-stop") else "operational-failed"

    if ax["admission"] == "rejected":
        return "operational-failed" if ax["domainCondition"] == "host-fault" else "request-rejected"

    if ax["domainCondition"] == "host-fault":
        return "operational-failed"

    # A signal only reclassifies while the outcome is still unsettled.
    if ax["interruption"] == "signal-before-finalization":
        return "interrupted"

    if ck == "mutation":
        if ax["domainCondition"] == "precondition-failed":
            return "request-rejected"
        if ax["domainCondition"] == "verification-propagated":
            return _analysis(ax)
        return "success"

    if ck == "query":
        if ax["domainCondition"] == "addressed-identity-unresolved":
            return "request-rejected"
        if ax["requiredCoverage"] == "unsatisfied":
            return "indeterminate"
        return "success"

    return _analysis(ax)


def _analysis(ax: dict) -> str:
    if ax["lifecycle"] == "cannot-seal-coherent-run":
        return "operational-failed"
    if ax["durability"] == "failed":
        return "operational-failed"
    if ax["requiredPostconditions"] == "failed":
        return "operational-failed"
    if ax["requiredCoverage"] in ("unsatisfied", "unknown"):
        return "indeterminate"
    if ax["verdict"] == "indeterminate":
        return "indeterminate"
    if ax["verdict"] == "fail":
        return "policy-failed"
    if ax["verdict"] in ("pass", "advisory"):
        return "success"
    return "operational-failed"


def derive_codes(ax: dict, maps: dict) -> dict:
    """Pure axes -> the complete code payload. Raises KeyError on an unmapped cause,
    which is the point: an unmapped cause must not degrade to 'no expectation'."""
    cls = derive_class(ax)
    if ax["deficiency"] != "none":
        codes = [maps["deficiencyToReasonCode"][ax["deficiency"]]]
        codes += [maps["deficiencyToReasonCode"][d] for d in ax.get("secondaryDeficiencies", [])]
        return {"reasonCodes": codes}
    if ax["rejectionCause"] != "none":
        return {"errorCode": maps["rejectionCauseToErrorCode"][ax["rejectionCause"]]}
    if ax["faultCause"] != "none":
        return {"errorCode": maps["faultCauseToErrorCode"][ax["faultCause"]]}
    if cls in ("success", "policy-failed", "interrupted"):
        return {}
    return {}


def reduce_concurrent(conditions: dict, precedence: list[str]) -> dict:
    """Pre-reduction concurrent conditions -> exclusive cause axes (R2-D9-04)."""
    faults = list(conditions.get("faultCauses") or [])
    rejs = list(conditions.get("rejectionCauses") or [])
    defs = list(conditions.get("deficiencies") or [])
    secs = list(conditions.get("secondaryDeficiencies") or [])
    out = {"faultCause": "none", "rejectionCause": "none", "deficiency": "none",
           "secondaryDeficiencies": []}
    # Apply declared precedence order.
    for fam in precedence:
        if fam == "faultCause" and faults:
            out["faultCause"] = faults[0]
            return out
        if fam == "rejectionCause" and rejs:
            out["rejectionCause"] = rejs[0]
            return out
        if fam == "deficiency" and defs:
            out["deficiency"] = defs[0]
            rest = [d for d in defs[1:] + secs if d != defs[0]]
            # dedupe preserve order
            seen = set()
            dedup = []
            for d in rest:
                if d not in seen:
                    seen.add(d); dedup.append(d)
            out["secondaryDeficiencies"] = dedup
            return out
    return out


def _cross_axis(gid: str, ax: dict, cls: str, f: list[str]) -> None:
    """D12 — X1..X10. Each was verified true of every golden before adoption."""
    def bad(x, msg):
        if x:
            f.append(f"D12 {gid}: {msg}")
    bad((ax["deficiency"] != "none") != (cls == "indeterminate"),
        "X1 deficiency<->indeterminate violated")
    bad((ax["rejectionCause"] != "none") != (cls == "request-rejected"),
        "X2 rejectionCause<->request-rejected violated")
    bad((ax["faultCause"] != "none") != (cls == "operational-failed"),
        "X3 faultCause<->operational-failed violated")
    bad(sum(1 for k in CAUSES if ax[k] != "none") > 1,
        "X4 more than one cause family is non-none")
    bad(ax["rejectionCause"] in ("identity-unknown", "identity-expired")
        and ax["domainCondition"] != "addressed-identity-unresolved",
        "X5 identity rejection without addressed-identity-unresolved")
    bad(ax["admission"] == "rejected" and ax["lifecycle"] != "pre-run",
        "X6 rejected admission with non-pre-run lifecycle")
    bad(cls == "success" and ax["verdict"] not in ("pass", "advisory", "not-applicable"),
        f"X7 success with verdict '{ax['verdict']}'")
    bad(ax["durability"] == "failed" and cls != "operational-failed",
        "X8 durability failed but class is not operational-failed")
    bad(ax["commandKind"] == "serve" and cls not in ("success", "operational-failed"),
        f"X9 serve terminated as '{cls}'")
    sec = ax.get("secondaryDeficiencies", [])
    bad(sec and ax["deficiency"] == "none", "X10 secondary deficiencies without a primary")
    bad(len(sec) != len(set(sec)), "X10 duplicate secondary deficiencies")
    bad(ax["deficiency"] in sec, "X10 primary deficiency repeated in secondaries")


def _check(c: dict) -> list[str]:
    f: list[str] = []

    if c.get("version") != EXPECTED_VERSION:
        f.append(f"D0: contract version is '{c.get('version')}', checker expects "
                 f"'{EXPECTED_VERSION}' — the checker must never validate a superseded artifact")

    # ---- D14: causeModel is load-bearing (R2-D9-04) ----
    cm = c.get("causeModel")
    if not isinstance(cm, dict):
        f.append("D14: causeModel is absent or not an object — concurrent-cause precedence "
                 "is unexecutable prose (R2-D9-04)")
        precedence = list(REQUIRED_PRECEDENCE)
    else:
        precedence = list(cm.get("precedence") or [])
        if precedence != REQUIRED_PRECEDENCE:
            f.append(f"D14: causeModel.precedence is {precedence}, expected "
                     f"{REQUIRED_PRECEDENCE} (fault > rejection > deficiency)")
        if not cm.get("precedenceRule"):
            f.append("D14: causeModel.precedenceRule is missing")
        if cm.get("families") != REQUIRED_PRECEDENCE:
            # families may be listed; require all three present
            fams = set(cm.get("families") or [])
            if fams != set(REQUIRED_PRECEDENCE):
                f.append(f"D14: causeModel.families incomplete: {sorted(fams)}")

    # ---- D12 declaration presence (R2-D9-05) ----
    xinv = c.get("crossAxisInvariants")
    if not isinstance(xinv, list) or not xinv:
        f.append("D12: crossAxisInvariants is absent or empty — declared rules must be "
                 "present in the binding artifact, not only hard-coded in the checker")
    else:
        ids = {x.get("id") for x in xinv if isinstance(x, dict)}
        missing = REQUIRED_X_IDS - ids
        if missing:
            f.append(f"D12: crossAxisInvariants missing declared ids {sorted(missing)}")

    schema = c["scenarioAxesSchema"]["properties"]
    codes = {x["class"]: x["code"] for x in c["exitClasses"]}
    variants = {v["class"]: v for v in c["hostTerminationUnion"]["variants"]}
    reason_vocab = set(c["codeVocabulary"]["reasonCodes"])
    error_vocab = set(c["codeVocabulary"]["errorCodes"])
    vocab = reason_vocab | error_vocab
    seen_classes: set[str] = set()
    seen_causes: set[str] = set()
    seen_ids: set[str] = set()

    maps = c.get("codeMaps")
    if not isinstance(maps, dict):
        f.append("D11: codeMaps is absent or not an object — the derivation has no code source")
        maps = {}
    for axis, mapname in MAP_FOR.items():
        m = maps.get(mapname)
        if not isinstance(m, dict) or not m:
            f.append(f"D11: codeMaps.{mapname} is absent or empty")
            continue
        want = {e for e in schema[axis]["enum"] if e != "none"}
        if set(m) != want:
            for k in want - set(m):
                f.append(f"D11: {mapname} has no entry for '{k}' (enum value unmapped)")
            for k in set(m) - want:
                f.append(f"D11: {mapname} maps '{k}', which is not in the {axis} enum")
        target = reason_vocab if mapname.endswith("ReasonCode") else error_vocab
        for k, v in m.items():
            if v not in target:
                f.append(f"D11: {mapname}['{k}'] = '{v}' is outside the declared "
                         f"{'reason' if target is reason_vocab else 'error'} vocabulary")
        dupes = {v for v in m.values() if list(m.values()).count(v) > 1}
        for v in sorted(dupes):
            f.append(f"D11: {mapname} is not injective — '{v}' is the image of multiple causes")

    for g in c["goldenCases"]:
        gid = g["id"]
        if gid in seen_ids:
            f.append(f"D2 {gid}: duplicate golden id")
        seen_ids.add(gid)

        if not g.get("scenario"):
            f.append(f"D1 {gid}: missing scenario sentence")

        ax = g.get("scenarioAxes") or {}
        if not ax:
            f.append(f"D2 {gid}: no scenarioAxes — nothing to derive from")
            continue

        # ---- D16: top-level commandKind sync (R2-D9-05) ----
        top_ck = g.get("commandKind")
        ax_ck = ax.get("commandKind")
        if top_ck is None:
            f.append(f"D16 {gid}: missing top-level commandKind")
        elif top_ck != ax_ck:
            f.append(f"D16 {gid}: top-level commandKind '{top_ck}' != "
                     f"scenarioAxes.commandKind '{ax_ck}'")

        # host-finalization projection honesty (R2-D9-02)
        if ax.get("projectionScope") == "host-finalization-only":
            hfp = g.get("hostFinalizationProjection") or {}
            if not hfp.get("doesNotClaimUniversalLifecycle"):
                f.append(f"D2 {gid}: host-finalization-only projection lacks "
                         f"doesNotClaimUniversalLifecycle=true")
            if not hfp.get("preservesSettledRun"):
                f.append(f"D2 {gid}: host-finalization-only projection must preserve "
                         f"already-settled Run identity")

        for k, v in ax.items():
            if k not in schema:
                f.append(f"D2 {gid}: undeclared axis field '{k}'")
                continue
            if v is None:
                f.append(f"D2 {gid}: axis '{k}' is explicitly null (absence-only policy)")
            elif isinstance(v, list):
                allowed = schema[k].get("items", {}).get("enum", [])
                for item in v:
                    if item not in allowed:
                        f.append(f"D2 {gid}: axis '{k}' item '{item}' not in declared enum")
            elif "enum" in schema[k] and v not in schema[k]["enum"]:
                f.append(f"D2 {gid}: axis '{k}'='{v}' not in declared enum")
        for k in schema:
            if schema[k].get("required") and k not in ax:
                f.append(f"D2 {gid}: missing required axis '{k}'")

        t = g["expectedTermination"]
        cls = t.get("class")
        seen_classes.add(cls)
        for k in CAUSES:
            if ax.get(k, "none") != "none":
                seen_causes.add(ax[k])
        seen_causes.update(ax.get("secondaryDeficiencies", []))

        var = variants.get(cls)
        if var is None:
            f.append(f"D3 {gid}: class '{cls}' has no union variant")
            continue

        allowed = set(var["required"]) | set(var.get("optional", [])) | {"class"}
        for k, v in t.items():
            if k in FORBIDDEN_PAYLOAD_FIELDS:
                f.append(f"D4 {gid}: forbidden field '{k}' in payload (derived from class)")
            elif k not in allowed:
                f.append(f"D3 {gid}: field '{k}' not permitted on class '{cls}'")
            if v is None:
                f.append(f"D3 {gid}: payload field '{k}' is explicitly null")
        for k in var["required"]:
            if k not in t:
                f.append(f"D3 {gid}: class '{cls}' requires '{k}'")

        for code in list(t.get("reasonCodes", [])) + ([t["errorCode"]] if "errorCode" in t else []):
            if code not in vocab:
                f.append(f"D5 {gid}: code '{code}' outside declared vocabulary")

        try:
            got = derive_class(ax)
        except KeyError as e:
            f.append(f"D6 {gid}: derivation needs missing axis {e}")
            continue
        if got != cls:
            f.append(f"D6 {gid}: derived '{got}', expected '{cls}'")

        if codes.get(cls) is None:
            f.append(f"D7 {gid}: class '{cls}' absent from exitClasses")

        try:
            want = derive_codes(ax, maps)
        except KeyError as e:
            f.append(f"D10 {gid}: cause {e} has no mapping — cannot determine the code payload")
        else:
            for field in ("reasonCodes", "errorCode"):
                exp, act = want.get(field), t.get(field)
                if exp != act:
                    f.append(f"D10 {gid}: axes imply {field}={exp!r} but golden carries {act!r}")

        _cross_axis(gid, ax, cls, f)

    for cls in codes:
        if cls not in seen_classes:
            f.append(f"D8: class '{cls}' has no golden")

    for axis in CAUSES:
        for val in schema[axis]["enum"]:
            if val != "none" and val not in seen_causes:
                f.append(f"D13: {axis} value '{val}' has no golden — the contract is "
                         f"aspirational for that cause")

    for row in c.get("finalizationTransitions", []):
        if row["expectedTermination"] != row["settledTermination"]:
            f.append(f"D9 {row['settledTermination']}/{row['event']}: settled termination changed")
    settled = {r["settledTermination"] for r in c.get("finalizationTransitions", [])}
    for cls in codes:
        if cls not in settled:
            f.append(f"D9: no post-finalization transition row for class '{cls}'")

    # ---- D15 concurrent condition goldens (R2-D9-04) ----
    cg = c.get("concurrentConditionGoldens")
    if not isinstance(cg, list) or len(cg) < 3:
        f.append("D15: concurrentConditionGoldens missing or too few — cause precedence "
                 "is unexecuted (R2-D9-04)")
    else:
        for row in cg:
            rid = row.get("id", "?")
            reduced = reduce_concurrent(row.get("conditions") or {}, precedence)
            fam = row.get("expectFamily")
            cause = row.get("expectCause")
            if fam == "faultCause":
                if reduced["faultCause"] != cause:
                    f.append(f"D15 {rid}: reduced faultCause={reduced['faultCause']!r}, "
                             f"expected {cause!r}")
                if reduced["rejectionCause"] != "none" or reduced["deficiency"] != "none":
                    f.append(f"D15 {rid}: non-fault families not cleared after reduction")
            elif fam == "rejectionCause":
                if reduced["rejectionCause"] != cause:
                    f.append(f"D15 {rid}: reduced rejectionCause={reduced['rejectionCause']!r}, "
                             f"expected {cause!r}")
                if reduced["faultCause"] != "none" or reduced["deficiency"] != "none":
                    f.append(f"D15 {rid}: non-rejection families not cleared after reduction")
            elif fam == "deficiency":
                if reduced["deficiency"] != cause:
                    f.append(f"D15 {rid}: reduced deficiency={reduced['deficiency']!r}, "
                             f"expected {cause!r}")
                exp_sec = row.get("expectSecondaries")
                if exp_sec is not None and reduced["secondaryDeficiencies"] != exp_sec:
                    f.append(f"D15 {rid}: secondaries={reduced['secondaryDeficiencies']!r}, "
                             f"expected {exp_sec!r}")
            else:
                f.append(f"D15 {rid}: unknown expectFamily '{fam}'")
        if not c.get("concurrentConditionReducer"):
            f.append("D15: concurrentConditionReducer schema/algorithm is absent")

    return f


def check(c: object) -> list[str]:
    """Total D9 contract boundary for malformed parsed JSON shapes."""
    if not isinstance(c, dict) or not c:
        return ["D9-TOTALITY-ROOT: contract root must be a non-empty object"]
    axes = c.get("scenarioAxesSchema")
    if not isinstance(axes, dict) or not isinstance(axes.get("properties"), dict):
        return ["D9-TOTALITY-SHAPE: scenarioAxesSchema.properties must be an object"]
    try:
        return _check(c)
    except MALFORMED_SHAPE_EXCEPTIONS as exc:
        return [f"D9-TOTALITY-EXCEPTION: malformed contract shape "
                f"({type(exc).__name__})"]


def _mut_drop_codemaps(c):
    del c["codeMaps"]

def _mut_drop_used_mapping(c):
    del c["codeMaps"]["deficiencyToReasonCode"]["required-relation-missing"]

def _mut_append_reason_code(c):
    for g in c["goldenCases"]:
        if g["id"] == "analysis-required-coverage-missing":
            g["expectedTermination"]["reasonCodes"].append("COVERAGE.PROVIDER_UNAVAILABLE")

def _mut_second_cause(c):
    for g in c["goldenCases"]:
        if g["id"] == "analysis-required-coverage-missing":
            g["scenarioAxes"]["faultCause"] = "ledger-busy"

def _mut_out_of_vocab_map(c):
    c["codeMaps"]["faultCauseToErrorCode"]["cas-link"] = "CAS.LINK_MISSING"

def _mut_wrong_code(c):
    for g in c["goldenCases"]:
        if g["id"] == "query-addressed-run-expired":
            g["expectedTermination"]["errorCode"] = "IDENTITY.UNKNOWN"

def _mut_serve_interrupted(c):
    for g in c["goldenCases"]:
        if g["id"] == "serve-graceful-signal-stop":
            g["scenarioAxes"]["domainCondition"] = "none"

def _mut_stale_version(c):
    c["version"] = "v1.5"

def _mut_delete_cause_model(c):
    del c["causeModel"]

def _mut_reverse_precedence(c):
    c["causeModel"]["precedence"] = list(reversed(c["causeModel"]["precedence"]))

def _mut_delete_cross_axis(c):
    del c["crossAxisInvariants"]

def _mut_desync_command_kind(c):
    for g in c["goldenCases"]:
        if g["id"] == "analysis-pass":
            g["commandKind"] = "query"

def _mut_finalization_flip(c):
    c["finalizationTransitions"][0]["expectedTermination"] = "interrupted"

MUTATIONS = [
    ("delete codeMaps entirely (B-D9V15-01)", _mut_drop_codemaps),
    ("delete one USED mapping (B-D9V15-01)", _mut_drop_used_mapping),
    ("append an extra reasonCode (B-D9V15-03)", _mut_append_reason_code),
    ("add a second cause family (B-D9V15-03)", _mut_second_cause),
    ("map a cause outside the vocabulary (B-D9V15-02)", _mut_out_of_vocab_map),
    ("swap IDENTITY.EXPIRED for IDENTITY.UNKNOWN (control)", _mut_wrong_code),
    ("make serve terminate as interrupted (X9)", _mut_serve_interrupted),
    ("point the checker at a superseded version (B-D9V15-04)", _mut_stale_version),
    ("delete causeModel entirely (R2-D9-04)", _mut_delete_cause_model),
    ("reverse causeModel.precedence (R2-D9-04)", _mut_reverse_precedence),
    ("delete crossAxisInvariants (R2-D9-05)", _mut_delete_cross_axis),
    ("desync top-level commandKind (R2-D9-05)", _mut_desync_command_kind),
    ("flip a finalization transition (R2-D9-01)", _mut_finalization_flip),
]


def selftest(base: dict) -> int:
    pre = check(base)
    if pre:
        print(f"REFUSING to self-test: the base contract has {len(pre)} finding(s), so "
              f"every mutation would be masked by them.")
        for x in pre[:5]:
            print("  -", x)
        return 1
    print("mutation self-test — each row must be REJECTED\n")
    escaped = 0
    for name, root in TOTALITY_ROOT_CASES:
        findings = check(copy.deepcopy(root))
        if not findings:
            escaped += 1
        print(f"  {'reject' if findings else 'ESCAPE':>6}  parsed-JSON root {name}")
        print(f"          {findings[0] if findings else 'NO FINDING — root survived'}")
    for name, value in TOTALITY_NESTED_CASES:
        candidate = copy.deepcopy(base)
        candidate["scenarioAxesSchema"] = copy.deepcopy(value)
        findings = check(candidate)
        if not findings:
            escaped += 1
        print(f"  {'reject' if findings else 'ESCAPE':>6}  "
              f"scenarioAxesSchema nested {name}")
        print(f"          {findings[0] if findings else 'NO FINDING — nested shape survived'}")
    for name, mut in MUTATIONS:
        c = copy.deepcopy(base)
        mut(c)
        findings = check(c)
        ok = bool(findings)
        if not ok:
            escaped += 1
        first = findings[0] if findings else "NO FINDING — mutation survived"
        print(f"  {'reject' if ok else 'ESCAPE':>6}  {name}")
        print(f"          {first}")
    print()
    if escaped:
        total = len(MUTATIONS) + len(TOTALITY_ROOT_CASES) + len(TOTALITY_NESTED_CASES)
        print(f"{escaped}/{total} retained cases ESCAPED — the checker's proof path is optional")
        return 1
    print(f"all {len(MUTATIONS)} semantic mutations, {len(TOTALITY_ROOT_CASES)} root-shape "
          f"cases and {len(TOTALITY_NESTED_CASES)} nested-shape cases rejected — "
          "the proof path is load-bearing")
    return 0


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--selftest"]
    p = pathlib.Path(args[0]) if args else pathlib.Path(__file__).with_name(BINDING)
    if not p.exists():
        print(f"missing contract: {p}", file=sys.stderr)
        return 2
    c = json.loads(p.read_text())
    if "--selftest" in sys.argv:
        return selftest(c)
    f = check(c)
    if not f:
        n = len(c["goldenCases"])
        print(f"D9 contract OK — {p.name}, {n} goldens, D0..D16 clean")
        return 0
    n = len(c.get("goldenCases", [])) if isinstance(c, dict) else 0
    print(f"{len(f)} finding(s) across {n} goldens in {p.name}:")
    for x in f:
        print("  -", x)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
