#!/usr/bin/env python3
"""PROBE 1 - Pre-Plan analysis-spec selection cardinality.

Independently authored expectations. Nothing here imports the candidate's own
check ids or expected outcomes; every expectation is authored from the published
law and asserted against the real admission entry points.

Attempt 1 of this probe used invented languageMode names ('typescript'/'rust')
and an invented row shape; the candidate correctly refused them. The real
vocabulary is read from the matrix and the real row shape from the schema. That
first failure is retained in evidence/probe-attempts.md.

Claims under test:
  * the analysis-spec `requestedCapabilities` bound is 1024, read from the schema
  * the matrix-fixed default requests 11 capabilities for each TS/JS unit and 10
    for each Rust/syntax unit, so 93 TS units = 1023 rows (ADMIT, one row of
    headroom) and 94 TS units = 1034 rows (REFUSE)
  * the refusal is typed: PROJECT.SCOPE_LIMIT, subject `field:count>limit`,
    request-rejected / exit 2 / REQUEST.UNSATISFIABLE
  * the complete DEFAULT and a complete EXPLICITLY SUPPLIED spec both reach the
    same owning size check before generic maxItems validation
  * a non-array `requestedCapabilities` is neither counted nor coerced
  * nothing is truncated, no bound is raised, no sharding occurs
"""
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import harness as H  # noqa: E402

N, M, C = H.N, H.M, H.C
SR = N.ScopeRefusal
VE = C.ValidationError
AE = N.AdmissionError

TS_MODE = "ts-tsconfig"
RUST_MODE = "rust-cargo"

# ---------------------------------------------------------------- the bound
LIMIT = N.requested_capability_bound()
H.check("bound-is-1024", LIMIT == 1024, {"limit": LIMIT})
H.check("bound-is-read-from-the-foundation-schema-not-a-native-constant",
        LIMIT == M.SCHEMA["$defs"]["analysis-spec"]["properties"]
        ["requestedCapabilities"]["maxItems"])

# ------------------------------------------- per-unit request cardinality, recomputed
per_mode = {m: len(N.required_default_capabilities(m))
            for m in N.CAPABILITY_MATRIX["languageModes"]}
H.check("recomputed-per-unit-counts-are-11-for-ts-js-and-10-for-rust-syntax",
        per_mode == {"ts-tsconfig": 11, "js-allowjs": 11, "js-synthesized": 11,
                     "rust-cargo": 10, "rust-cargo-prepared": 10,
                     "syntax-only": 10},
        {"perMode": per_mode})
H.check("93-ts-units-produce-1023-rows-one-under-the-bound",
        93 * per_mode[TS_MODE] == 1023 and 1023 < LIMIT)
H.check("94-ts-units-produce-1034-rows-over-the-bound",
        94 * per_mode[TS_MODE] == 1034 and 1034 > LIMIT)
H.check("the-fitting-count-leaves-exactly-one-row-of-headroom",
        LIMIT - 1023 == 1)

# ----------------------------------------------------------- fixture builders
CAPS_TS = N.required_default_capabilities(TS_MODE)


def units(n, mode=TS_MODE, family="typescript"):
    return [{"languageMode": mode, "rootPath": "unit%04d" % i,
             "languageFamily": family} for i in range(n)]


def full_registry():
    """A release registry declaring EVERY capability for every mode, so the
    default's availability account is empty and only cardinality is in play."""
    # languageModes is x-opensip-order: utf8 and requestedCapabilities is
    # canonical-set; my first fixture ignored both and the candidate's
    # array-order law correctly refused it (retained in probe-attempts.md).
    # A release may only declare cells the matrix actually selects. My third
    # fixture declared every capability for every mode, including the
    # NOT-SELECTED (clones-cross-tsjs, rust-cargo) cell, and the candidate
    # refused with native.release-capability-mode-not-selected - the v14
    # CB4-SHOULD-2 law firing on MY input. Retained in probe-attempts.md.
    not_selected = {(c["capability"], c["mode"]) for c in N.CAPABILITY_MATRIX["cells"]
                    if c["state"] == "NOT-SELECTED"}
    rows = []
    for c in N.CAPABILITY_MATRIX["capabilities"]:
        modes = sorted((m for m in N.CAPABILITY_MATRIX["languageModes"]
                        if (c["id"], m) not in not_selected),
                       key=lambda m: m.encode("utf-8"))
        if modes:
            rows.append({"capabilityId": c["id"], "languageModes": modes})
    # The registry array is ALSO x-opensip-order: canonical-set. My second
    # fixture sorted the inner modes but not the outer rows, and the same law
    # refused it again - retained in probe-attempts.md.
    return sorted(rows, key=C.canonical)


def explicit_spec(rows):
    return {"schemaVersion": 2, "requestedCapabilities": rows,
            "policyPackIds": [], "parameters": []}


def rows_for(n):
    """n structurally valid, DISTINCT requested-capability rows."""
    out = []
    i = 0
    while len(out) < n:
        cap = CAPS_TS[i % len(CAPS_TS)]
        root = "r%05d" % (i // len(CAPS_TS))
        out.append({"capabilityId": cap, "languageMode": TS_MODE,
                    "workspaceRoot": root, "required": True})
        i += 1
    # canonical-set order is a law of the field, not a convenience.
    return sorted(out, key=C.canonical)


H.check("my-fixture-rows-are-distinct", len({C.canonical(r) for r in rows_for(1034)}) == 1034)

# =========================================================== THE DEFAULT PATH
# 93 TS units: the largest fitting default. Authored expectation: ADMITS, and
# the emitted spec carries exactly 1023 rows.
res93 = None
try:
    res93 = N.default_capability_selection(units(93), full_registry())
    H.check("the-complete-default-for-93-ts-units-admits", True)
except BaseException as e:  # noqa: BLE001
    H.check("the-complete-default-for-93-ts-units-admits", False,
            {"exc": type(e).__name__, "msg": str(e)[:300]})
if res93:
    n = len(res93["analysisSpec"]["requestedCapabilities"])
    H.check("the-admitted-default-carries-exactly-1023-rows", n == 1023, {"rows": n})
    H.check("the-admitted-default-declares-itself-the-complete-selected-product",
            res93.get("defaultIsCompleteSelectedProduct") is True)
    H.check("the-admitted-default-carries-DEFAULTED-provenance",
            res93.get("provenance") == "DEFAULTED")

# 94 TS units: the first overflowing default. Authored expectation: the COMPLETE
# DEFAULT reaches its owning size check and refuses TYPED with exact numbers.
H.raises("the-complete-default-for-94-ts-units-refuses-typed-with-exact-count-and-limit",
         lambda: N.default_capability_selection(units(94), full_registry()),
         SR, must_contain="requestedCapabilities:1034>1024")
H.raises("the-overflowing-default-names-PROJECT-SCOPE-LIMIT",
         lambda: N.default_capability_selection(units(94), full_registry()),
         SR, must_contain="PROJECT.SCOPE_LIMIT")

# The overflow must NOT be a generic schema exception.
try:
    N.default_capability_selection(units(94), full_registry())
    got = None
except BaseException as e:  # noqa: BLE001
    got = e
H.check("the-overflowing-default-is-not-a-generic-schema-validation-error",
        isinstance(got, SR) and not isinstance(got, VE),
        {"exc": type(got).__name__ if got else "ADMITTED"})

# The matrix-fixed default is UNCHANGED: a starved registry must not shrink it.
starved = [{"capabilityId": CAPS_TS[0], "languageModes": [TS_MODE]}]
try:
    r_starved = N.default_capability_selection(units(93), starved)
    same = (r_starved["analysisSpec"]["requestedCapabilities"]
            == res93["analysisSpec"]["requestedCapabilities"]) if res93 else False
    H.check("the-fixed-matrix-default-is-identical-under-a-starved-release-registry",
            same, {"rows": len(r_starved["analysisSpec"]["requestedCapabilities"])})
    H.check("a-starved-registry-discloses-absences-rather-than-dropping-requests",
            len(r_starved["undeclaredCapabilities"]) > 0,
            {"undeclared": len(r_starved["undeclaredCapabilities"])})
except BaseException as e:  # noqa: BLE001
    H.check("the-fixed-matrix-default-is-identical-under-a-starved-release-registry",
            False, {"exc": type(e).__name__, "msg": str(e)[:200]})

# And it still overflows at 94 under a starved registry - the bound is on the
# REQUEST, not on availability.
H.raises("the-default-still-overflows-at-94-units-under-a-starved-registry",
         lambda: N.default_capability_selection(units(94), starved),
         SR, must_contain="requestedCapabilities:1034>1024")

# ================================================ THE EXPLICITLY SUPPLIED PATH
H.admits("an-explicit-spec-at-exactly-the-1024-bound-admits",
         lambda: N.admit_analysis_spec(explicit_spec(rows_for(1024))))
H.raises("an-explicit-spec-at-1025-refuses-typed-with-exact-count-and-limit",
         lambda: N.admit_analysis_spec(explicit_spec(rows_for(1025))),
         SR, must_contain="requestedCapabilities:1025>1024")
H.admits("an-explicit-spec-at-1023-admits",
         lambda: N.admit_analysis_spec(explicit_spec(rows_for(1023))))
H.raises("an-explicit-spec-at-1034-refuses-typed",
         lambda: N.admit_analysis_spec(explicit_spec(rows_for(1034))),
         SR, must_contain="requestedCapabilities:1034>1024")

# ordinary small and empty explicit selections
H.admits("an-ordinary-one-row-explicit-selection-admits",
         lambda: N.admit_analysis_spec(explicit_spec(rows_for(1))))
H.admits("an-ordinary-small-explicit-selection-of-11-rows-admits",
         lambda: N.admit_analysis_spec(explicit_spec(rows_for(11))))
H.admits("an-empty-explicit-selection-admits-and-is-not-a-scope-limit",
         lambda: N.admit_analysis_spec(explicit_spec([])))

# ================================= wrong shape / type / missingness must NOT count
WRONG = {
    "missing-field": {"schemaVersion": 2, "policyPackIds": [], "parameters": []},
    "null": explicit_spec(None),
    "boolean-true": explicit_spec(True),
    "integer-1034": explicit_spec(1034),
    "short-string": explicit_spec("x"),
    "oversized-string-1025-chars": explicit_spec("x" * 1025),
    "oversized-string-1034-chars": explicit_spec("x" * 1034),
    "oversized-dict-1034-keys": explicit_spec({str(i): i for i in range(1034)}),
    "oversized-tuple-like-nested-list": explicit_spec({"rows": rows_for(1034)}),
    "missing-schemaVersion": {"requestedCapabilities": [], "policyPackIds": [],
                              "parameters": []},
    "wrong-schemaVersion": {"schemaVersion": 1, "requestedCapabilities": [],
                            "policyPackIds": [], "parameters": []},
    "unknown-property": {"schemaVersion": 2, "requestedCapabilities": [],
                         "policyPackIds": [], "parameters": [], "surprise": 1},
}
for label, bad in WRONG.items():
    try:
        N.admit_analysis_spec(bad)
        raised = None
    except BaseException as e:  # noqa: BLE001
        raised = e
    H.check("wrong-shape-refuses--" + label, raised is not None,
            {"exc": type(raised).__name__ if raised else "ADMITTED"})
    H.check("wrong-shape-is-never-a-ScopeRefusal--" + label,
            raised is not None and not isinstance(raised, SR),
            {"exc": type(raised).__name__ if raised else "ADMITTED"})
    H.check("wrong-shape-never-publishes-PROJECT-SCOPE-LIMIT--" + label,
            raised is not None and "PROJECT.SCOPE_LIMIT" not in str(raised))
    H.check("wrong-shape-is-not-silently-coerced-or-repaired--" + label,
            raised is not None)

# The decisive misclassification case, stated on its own: a 1025-character
# string must never be reported as 1025 requested capabilities.
try:
    N.admit_analysis_spec(explicit_spec("x" * 1025))
    s_exc = None
except BaseException as e:  # noqa: BLE001
    s_exc = e
H.check("a-1025-character-string-is-never-published-as-1025-capabilities",
        s_exc is not None and "1025>1024" not in str(s_exc),
        {"msg": str(s_exc)[:200] if s_exc else "ADMITTED"})

# ================== cardinality precedes generic schema validation for real arrays
H.raises("an-oversized-array-of-malformed-items-still-refuses-typed-first",
         lambda: N.admit_analysis_spec(
             explicit_spec([{"nope": i} for i in range(1034)])),
         SR, must_contain="requestedCapabilities:1034>1024")
H.raises("the-same-malformed-items-within-the-bound-refuse-on-the-schema",
         lambda: N.admit_analysis_spec(
             explicit_spec([{"nope": i} for i in range(10)])),
         (VE, KeyError, TypeError, ValueError),
         must_not_contain="PROJECT.SCOPE_LIMIT")

# ===================================== vocabulary still runs after the schema
bad_id = dict(rows_for(1)[0], capabilityId="not-a-real-capability")
H.raises("an-unregistered-capability-id-at-an-admitted-size-refuses-on-vocabulary",
         lambda: N.admit_analysis_spec(explicit_spec([bad_id])),
         (AE, VE, ValueError), must_not_contain="PROJECT.SCOPE_LIMIT")
bad_mode = dict(rows_for(1)[0], languageMode="klingon")
H.raises("an-unregistered-language-mode-at-an-admitted-size-refuses-on-vocabulary",
         lambda: N.admit_analysis_spec(explicit_spec([bad_mode])),
         (AE, VE, ValueError), must_not_contain="PROJECT.SCOPE_LIMIT")
rel_spelling = dict(rows_for(1)[0], capabilityId="file@enumerated")
H.raises("a-relation-at-rung-spelling-is-refused-by-shape",
         lambda: N.admit_analysis_spec(explicit_spec([rel_spelling])),
         (AE, VE, ValueError), must_not_contain="PROJECT.SCOPE_LIMIT")

# ============== the shared vocabulary helper deliberately does NOT guard size
try:
    N.admit_requested_capabilities(rows_for(2048))
    helper_exc = None
except BaseException as e:  # noqa: BLE001
    helper_exc = e
H.check("the-shared-vocabulary-helper-raises-no-scope-refusal-on-an-oversized-array",
        not isinstance(helper_exc, SR),
        {"exc": type(helper_exc).__name__ if helper_exc else "admitted"})

# ===================== no truncation, no raised bound, no sharding, no host fault
H.check("the-published-bound-is-not-raised-by-this-correction", LIMIT == 1024)
try:
    N.admit_analysis_spec(explicit_spec(rows_for(1034)))
    trunc = "ADMITTED"
except SR as e:
    trunc = str(e)
H.check("the-refusal-reports-the-full-1034-count-rather-than-a-truncated-one",
        "1034" in trunc and "1024>" not in trunc, {"msg": trunc})

exit_code = H.report(
    str(pathlib.Path(__file__).resolve().parent.parent /
        "evidence/probe-preplan-cardinality.json"),
    "pre-Plan analysis-spec selection cardinality",
    ["Reference-model only. No host, CLI, renderer or real analysis execution "
     "exists to observe; these are admission-boundary outcomes in the "
     "candidate's own Python reference model.",
     "The 93/94-unit fixtures are synthetic discovered units, not measured "
     "repositories; the arithmetic is recomputed from the matrix but the unit "
     "discovery itself is assumed.",
     "Attempt 1 of this probe used invented languageMode and row-shape "
     "vocabulary and was correctly refused by the candidate; retained in "
     "probe-attempts.md."])
sys.exit(1 if exit_code else 0)
