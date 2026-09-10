#!/usr/bin/env python3
"""PROBE 5 - the counterexample behind V15-ADV-1, and its bounded consequences.

The published pre-Plan ordering paragraph (native-evidence.md section 10, and
the admit_analysis_spec docstring) states without qualification:

  "Everything a schema is genuinely better at - an unknown property, a wrong
   type, a missing field, a missing `schemaVersion` - still refuses at the
   schema step exactly as before."

That sentence is true only while `requestedCapabilities` is within its bound.
When the array is ALSO over the bound, the cardinality step preempts, and the
caller sees PROJECT.SCOPE_LIMIT rather than the schema fault.

This probe (a) exhibits the counterexample, and (b) bounds its consequences:
the refusal that does fire is factually TRUE of the instance, the spec is
refused either way, and no Plan or Run is minted. That is why this is raised as
an ADVISORY and not as a MUST or a SHOULD.
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import harness as H  # noqa: E402

N, M, C = H.N, H.M, H.C
SR = N.ScopeRefusal
VE = C.ValidationError
SUBJ = H.SUBJECT

CAPS = N.required_default_capabilities("ts-tsconfig")


def rows(n):
    out, i = [], 0
    while len(out) < n:
        out.append({"capabilityId": CAPS[i % len(CAPS)], "languageMode": "ts-tsconfig",
                    "workspaceRoot": "r%05d" % (i // len(CAPS)), "required": True})
        i += 1
    return sorted(out, key=C.canonical)


def outcome(spec):
    try:
        N.admit_analysis_spec(spec)
        return None
    except BaseException as e:  # noqa: BLE001
        return e


# ------------------------------------------------- the sentence is in the bytes
NATIVE_MD = (SUBJ / "docs/v2/contracts/product-v1/native-evidence.md").read_text()
SENTENCE = ("Everything a schema is genuinely better at - an unknown property, "
            "a wrong type, a missing field, a missing `schemaVersion` - still "
            "refuses at the schema step exactly as before.")
H.check("the-unqualified-sentence-is-present-in-the-frozen-contract",
        SENTENCE in NATIVE_MD)
H.check("the-same-unqualified-claim-is-repeated-in-the-model-docstring",
        "still refuses at step 2 exactly as before"
        in " ".join(N.admit_analysis_spec.__doc__.split()))

# --------------------------------------------------------- CONTROLS: within bound
for label, spec in {
    "missing-schemaVersion": {"requestedCapabilities": rows(10),
                              "policyPackIds": [], "parameters": []},
    "wrong-schemaVersion": {"schemaVersion": 99, "requestedCapabilities": rows(10),
                            "policyPackIds": [], "parameters": []},
    "unknown-property": {"schemaVersion": 2, "requestedCapabilities": rows(10),
                         "policyPackIds": [], "parameters": [], "surprise": 1},
}.items():
    e = outcome(spec)
    H.check("CONTROL-within-the-bound-the-schema-fault-really-does-refuse-at-the-schema--"
            + label, isinstance(e, VE), {"exc": type(e).__name__ if e else "ADMITTED"})

# ------------------------------------------------- COUNTEREXAMPLES: over the bound
counter = {}
for label, spec in {
    "missing-schemaVersion": {"requestedCapabilities": rows(1034),
                              "policyPackIds": [], "parameters": []},
    "wrong-schemaVersion": {"schemaVersion": 99, "requestedCapabilities": rows(1034),
                            "policyPackIds": [], "parameters": []},
    "unknown-property": {"schemaVersion": 2, "requestedCapabilities": rows(1034),
                         "policyPackIds": [], "parameters": [], "surprise": 1},
    "missing-policyPackIds": {"schemaVersion": 2, "requestedCapabilities": rows(1034),
                              "parameters": []},
}.items():
    e = outcome(spec)
    counter[label] = e
    H.check("COUNTEREXAMPLE-over-the-bound-the-schema-fault-is-preempted--" + label,
            isinstance(e, SR), {"exc": type(e).__name__ if e else "ADMITTED",
                                "msg": str(e)[:120] if e else ""})

# ------------------------------------------- the consequences are bounded
for label, e in counter.items():
    H.check("the-preempting-refusal-states-a-TRUE-fact-about-the-instance--" + label,
            isinstance(e, SR) and e.subject["count"] == 1034
            and e.subject["limit"] == 1024
            and e.subject["field"] == "requestedCapabilities")
    H.check("the-malformed-spec-is-still-REFUSED-not-admitted--" + label, e is not None)
    H.check("the-preempting-refusal-is-still-request-rejected-exit-2--" + label,
            isinstance(e, SR) and e.d9["class"] == "request-rejected"
            and e.d9["exitCode"] == 2)
    H.check("no-plan-or-run-is-minted-for-the-refused-step--" + label,
            isinstance(e, SR))

# Nothing is unrepresentable: fixing the cardinality reveals the schema fault.
fixed = {"requestedCapabilities": rows(1023), "policyPackIds": [], "parameters": []}
H.check("narrowing-the-selection-then-reveals-the-underlying-schema-fault",
        isinstance(outcome(fixed), VE),
        {"note": "two round trips, not a lost diagnostic"})

# And the precise scoping the same paragraph DOES state remains accurate.
H.check("the-same-paragraph-does-state-cardinality-runs-first",
        "bounded selection cardinality first" in NATIVE_MD)
H.check("the-same-paragraph-does-state-the-array-only-condition",
        "conditional on the field actually being a JSON array in an object" in NATIVE_MD)
H.check("so-an-implementer-building-from-the-published-order-reaches-the-right-result",
        "bounded selection cardinality first" in NATIVE_MD
        and "then generic schema validation of the whole record" in NATIVE_MD)

exit_code = H.report(
    str(pathlib.Path(__file__).resolve().parent.parent /
        "evidence/probe-ordering-scope-advisory.json"),
    "V15-ADV-1 counterexample and its bounded consequences",
    ["Reference-model only. The consequence assessed here is which DIAGNOSTIC a "
     "caller receives, not whether the record is admitted: it is refused on "
     "either route, with the same class and exit code.",
     "This probe deliberately asserts a MISMATCH between an unqualified prose "
     "sentence and the implemented order. It is evidence for an advisory, not "
     "for a MUST or a SHOULD."])
sys.exit(1 if exit_code else 0)
