#!/usr/bin/env python3
"""P4: prove the guards the correction was NOT allowed to weaken still hold.

Runs the candidate's own checkers and asserts that every named guard case is
still present AND still passing. A guard that was silently deleted would show up
as `missing`; one that was inverted would show up as `failing`. Both are
failures of this probe, which is the point: the delta is large enough that
"the suite is green" is not by itself evidence that these specific laws survived.
"""
import json
import os
import subprocess
import sys

B = "/tmp/opensip-design-corrections/bv3-corrections-author.v1"
PY = "/tmp/opensip-architecture-review-env/bin/python"
SRC = os.environ.get("OPENSIP_SRC", B + "/devtest")
DC = SRC + "/docs/coop/design-corrections"

# Substrings that must each match at least one PASSING check id.
REQUIRED = {
    # The conflict limb's check ids say "conflict"/"conflicts", not "annotation-conflict";
    # the first needle here was wrong, the guard was always present.
    "typed annotation conflict guard": ["conflict"],
    "typed annotation alias guard": ["alias"],
    "typed annotation cycle guard": ["cycle"],
    "typed annotation missingness guard": ["unannotated", "missing"],
    "digest law limb 1 (every governed field annotated)": ["every-closure-bearing-field-declares-its-kind"],
    "digest law limb 2 (annotated field reachable from joins)": ["not-joined", "residue"],
    "digest law limb 3 (join names an existing field)": ["digest-law", "relation-digest"],
    "clone version join": ["body-language", "language-version"],
    "clone dialect join": ["dialect"],
    "source inventory join": ["inventor"],
    "early annotation comparison": ["annotation"],
    "relation rung ladder": ["rung"],
    "universe rule": ["same-only", "universe"],
    "coverage sufficiency": ["coverage"],
}


def run(script, report, extra=()):
    out = os.path.join(B, "logs", "guards-" + os.path.basename(script) + ".json")
    proc = subprocess.run([PY, "-I", "-B", os.path.join(DC, script), "--report", out] + list(extra),
                          capture_output=True, text=True, timeout=600)
    data = json.load(open(out)) if os.path.exists(out) else {}
    return proc.returncode, data


def collect():
    """Return {check_id: passed} across the checkers that publish per-check ids."""
    ids = {}
    for script in ("foundation/check-identity.py", "foundation/check-foundation.py"):
        _, data = run(script, None)
        for entry in data.get("checks", []):
            key = entry.get("id") or entry.get("name")
            if key is not None:
                ids[key] = bool(entry.get("passed", entry.get("ok", False)))
    _, wf = run("workflows/check_workflows.v1.py", None)
    for entry in wf.get("checks", []):
        ids[entry["id"]] = bool(entry["ok"])
    return ids


def main():
    ids = collect()
    report = {"checkIdsSeen": len(ids), "guards": {}}
    bad = []
    for label, needles in REQUIRED.items():
        matched = sorted(k for k in ids if any(n in k for n in needles))
        failing = sorted(k for k in matched if not ids[k])
        report["guards"][label] = {"matchedChecks": len(matched), "failing": failing,
                                   "examples": matched[:4]}
        if not matched:
            bad.append(label + ": NO CHECK MATCHES (guard may have been removed)")
        if failing:
            bad.append(label + ": FAILING " + ", ".join(failing))
    report["verdict"] = "ALL GUARDS PRESENT AND PASSING" if not bad else "PROBLEMS"
    report["problems"] = bad
    print(json.dumps(report, indent=2))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
