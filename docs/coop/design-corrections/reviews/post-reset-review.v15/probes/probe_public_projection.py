#!/usr/bin/env python3
"""PROBE 2 - the public projection of the pre-Plan refusal, and the retained-payload boundary.

Independently authored expectations. The shared fixture is imported only to
CONSTRUCT a lawful Run; every verdict below is my own assertion about what the
candidate's admission actually does.

Claims under test:
  * a ScopeRefusal projects to a schema-admitted StepTermination and a complete
    schema-admitted kind=failure CommandEnvelope with a nonempty errors array
  * class request-rejected, exit 2, errorCode REQUEST.UNSATISFIABLE, detail
    PROJECT.SCOPE_LIMIT, subject `field:count>limit`
  * the refusal is NOT a host fault (never SYSTEM.OUTCOME.ILLEGAL_STATE and
    never faultCause host-invariant)
  * ALL FOUR bounded fields across TWO record families use the one law, each
    with its own remedy, and none introduces a new public code
  * the scope refusal does NOT launder through the native internal-key
    normalizer, and a generic schema exception has no public route
  * a CORRUPT RETAINED analysis-spec payload is a DIFFERENT question: it refuses
    at retained Run closure through raw payload schema validation, before any
    capability vocabulary admission - not as an ordinary request refusal
  * positive control: an unmutated Run closes
"""
import copy
import importlib.util
import json
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import harness as H  # noqa: E402

N, M, C, W = H.N, H.M, H.C, H.W
SR = N.ScopeRefusal
VE = C.ValidationError

COMMON = "workflows/schemas/common.schema.json"
ENVELOPE = "workflows/schemas/command-envelope.schema.json"

PUBLIC = json.loads((H.DC / "public-detail-registry.v1.json").read_text())
PUBLIC_CODES = {r["code"] for r in PUBLIC["records"]}

# Shared fixture: CONSTRUCTION ONLY. Not a verdict oracle.
_s = importlib.util.spec_from_file_location("intfix", H.DC / "integration-fixtures.py")
FIX = importlib.util.module_from_spec(_s)
sys.modules["intfix"] = FIX
_s.loader.exec_module(FIX)


def admits(document, selector, value):
    try:
        W.validate_import_record(document, selector, value)
        return True
    except Exception:  # noqa: BLE001
        return False


def overflow(field="requestedCapabilities", count=1034, limit=1024):
    return N.ScopeRefusal(field, count, limit)


def envelope_for(refusal):
    """The complete public failure envelope a refusal composes."""
    t = N.scope_refusal_termination(refusal)
    return t, {"schemaFamily": "opensip.product.envelope", "schemaMajor": 2,
               "kind": "failure", "requestId": "req1_" + "a" * 32,
               "termination": t, "exitCode": W.EXIT[t["class"]],
               "errors": [t["domainDetail"]]}


# ===================================================== the projected termination
ref = overflow()
term, env = envelope_for(ref)

H.check("the-termination-admits-through-the-real-StepTermination-schema",
        admits(COMMON, "#/$defs/StepTermination", term), {"termination": term})
H.check("the-full-failure-envelope-admits-through-the-real-envelope-schema",
        admits(ENVELOPE, "", env))
H.check("the-failure-envelope-errors-array-is-nonempty",
        len(env["errors"]) >= 1)
H.check("the-envelope-errors-are-exactly-the-termination-detail-so-the-two-surfaces-agree",
        env["errors"] == [term["domainDetail"]])
H.check("the-class-is-request-rejected", term["class"] == "request-rejected")
H.check("the-exit-code-is-2", env["exitCode"] == 2, {"exit": env["exitCode"]})
H.check("the-error-code-is-REQUEST-UNSATISFIABLE",
        term["errorCode"] == "REQUEST.UNSATISFIABLE")
H.check("the-detail-code-is-PROJECT-SCOPE-LIMIT",
        term["domainDetail"]["code"] == "PROJECT.SCOPE_LIMIT")
H.check("the-subject-states-the-observed-bound-exactly",
        term["domainDetail"]["subject"] == "requestedCapabilities:1034>1024",
        {"subject": term["domainDetail"]["subject"]})

# -------------------------------------------------------- never a host fault
H.check("the-refusal-is-never-a-host-invariant-error-code",
        term["errorCode"] != "SYSTEM.OUTCOME.ILLEGAL_STATE")
H.check("the-refusal-carries-no-host-invariant-fault-cause",
        "host-invariant" not in json.dumps(term))
H.check("the-refusal-class-is-not-an-operational-failure",
        term["class"] != "operational-failed")

# --------------------------------------------- no new public code at this boundary
H.check("PROJECT-SCOPE-LIMIT-is-an-existing-registered-public-code",
        "PROJECT.SCOPE_LIMIT" in PUBLIC_CODES)
H.check("the-public-detail-registry-still-carries-exactly-287-codes",
        len(PUBLIC_CODES) == 287, {"codes": len(PUBLIC_CODES)})
H.check("this-boundary-introduces-no-new-public-detail-code",
        "PROJECT.SCOPE_LIMIT" not in
        json.dumps(PUBLIC.get("newInThisCorrection", "")))

# ===================== all FOUR bounded fields, across TWO record families
FIELDS = ["workspaceRoots", "pathPrefixes", "excludedPathPrefixes",
          "requestedCapabilities"]
H.check("the-one-remedy-table-names-exactly-the-four-bounded-fields",
        sorted(N.SCOPE_LIMIT_REMEDY) == sorted(FIELDS),
        {"fields": sorted(N.SCOPE_LIMIT_REMEDY)})

SCOPE_DESCRIPTOR_BOUNDS = {"workspaceRoots": 1024, "pathPrefixes": 65536,
                           "excludedPathPrefixes": 65536}
sd = M.SCHEMA["$defs"]["scope-descriptor"]["properties"]
for f, want in SCOPE_DESCRIPTOR_BOUNDS.items():
    H.check("the-scope-descriptor-family-publishes-its-own-bound--" + f,
            sd[f]["maxItems"] == want, {"maxItems": sd[f]["maxItems"]})
H.check("the-analysis-spec-family-publishes-its-own-bound--requestedCapabilities",
        M.SCHEMA["$defs"]["analysis-spec"]["properties"]
        ["requestedCapabilities"]["maxItems"] == 1024)
H.check("the-two-record-families-are-distinct-schema-definitions",
        "requestedCapabilities" not in sd)

for f in FIELDS:
    r = overflow(f, 70000, 65536) if "Prefix" in f else overflow(f, 1034, 1024)
    t, e = envelope_for(r)
    H.check("every-bounded-field-uses-the-one-law-and-one-code--" + f,
            t["domainDetail"]["code"] == "PROJECT.SCOPE_LIMIT"
            and t["errorCode"] == "REQUEST.UNSATISFIABLE"
            and t["class"] == "request-rejected")
    H.check("every-bounded-field-names-itself-in-the-subject--" + f,
            t["domainDetail"]["subject"].startswith(f + ":"),
            {"subject": t["domainDetail"]["subject"]})
    H.check("every-bounded-field-composes-a-schema-admitted-envelope--" + f,
            admits(COMMON, "#/$defs/StepTermination", t) and admits(ENVELOPE, "", e))
    rem = t["domainDetail"]["remedy"]
    H.check("every-remedy-names-narrowing-and-denies-truncation--" + f,
            "narrow" in rem.lower() and "truncat" in rem.lower(), {"remedy": rem})

# The previously served scope-descriptor remedies must be PRESERVED, not replaced.
for f in SCOPE_DESCRIPTOR_BOUNDS:
    H.check("the-inherited-scope-descriptor-remedy-is-preserved--" + f,
            "no " in N.SCOPE_LIMIT_REMEDY[f] and "truncated" in N.SCOPE_LIMIT_REMEDY[f],
            {"remedy": N.SCOPE_LIMIT_REMEDY[f]})

# ================ the scope refusal does not launder through the internal-key route
H.raises("a-generic-schema-exception-has-no-public-route-through-the-key-normalizer",
         lambda: N.public_termination_for(
             "jsonschema.exceptions.ValidationError: 1034 is too long", "user-config"),
         (Exception,))
H.raises("an-unregistered-internal-key-refuses-rather-than-passing-through",
         lambda: N.public_termination_for("totally.unregistered-key", "user-config"),
         (Exception,))

# ============================== POSITIVE CONTROL: a lawful Run closes unmutated
run, objects, blobs = FIX.build()
try:
    rid = M.close_run(run, copy.deepcopy(objects), copy.deepcopy(blobs))
    H.check("POSITIVE-CONTROL-an-unmutated-lawful-run-closes", bool(rid),
            {"runId": str(rid)[:40]})
    closed_ok = True
except BaseException as e:  # noqa: BLE001
    H.check("POSITIVE-CONTROL-an-unmutated-lawful-run-closes", False,
            {"exc": type(e).__name__, "msg": str(e)[:300]})
    closed_ok = False

# ================== a CORRUPT RETAINED analysis-spec is a DIFFERENT question
# Authored expectation: mutating the RETAINED analysis-spec payload to carry an
# oversized requestedCapabilities array must refuse at retained Run closure
# through raw payload SCHEMA validation - the existing corruption route - and
# must NOT be reported as an ordinary pre-Plan request refusal.
if closed_ok:
    obj2 = copy.deepcopy(objects)
    blob2 = copy.deepcopy(blobs)
    run2 = copy.deepcopy(run)
    # locate the retained analysis-spec blob
    spec_digest = None
    for d, raw in blob2.items():
        try:
            v = json.loads(raw)
        except Exception:  # noqa: BLE001
            continue
        if isinstance(v, dict) and "requestedCapabilities" in v and v.get("schemaVersion") == 2:
            spec_digest = d
            break
    H.check("the-retained-analysis-spec-payload-was-located-in-the-run-closure",
            spec_digest is not None)
    if spec_digest:
        # ATTEMPT 1 of this case only mutated the blob bytes, so the retained
        # CONTENT DIGEST join refused first with BLOB_DIGEST - a correct and
        # stronger outcome, but it never reached the schema route the claim is
        # about. Retained in probe-attempts.md. The case below forges a
        # SELF-CONSISTENT corrupt payload: the oversized spec is stored under
        # its own digest and the Plan is re-minted to name it, so the digest
        # joins all hold and the payload's own schema validation is reached.
        plan_domain, plan = obj2[run2["planId"]]
        spec_v = json.loads(blob2[plan["analysisSpecDigest"]])
        row0 = spec_v["requestedCapabilities"][0]
        big = sorted(({**row0, "workspaceRoot": "r%05d" % i} for i in range(1034)),
                     key=C.canonical)
        new_digest = FIX.put_blob(blob2, dict(spec_v, requestedCapabilities=big))
        FIX.rekey_plan(obj2, blob2, run2, dict(plan, analysisSpecDigest=new_digest))

        try:
            M.close_run(run2, obj2, blob2)
            corrupt_exc = None
        except BaseException as e:  # noqa: BLE001
            corrupt_exc = e
        H.check("a-self-consistent-oversized-retained-analysis-spec-refuses-at-run-closure",
                corrupt_exc is not None,
                {"exc": type(corrupt_exc).__name__ if corrupt_exc else "CLOSED"})
        H.check("the-corrupt-retained-payload-refuses-on-RAW-PAYLOAD-SCHEMA-validation",
                isinstance(corrupt_exc, VE),
                {"exc": type(corrupt_exc).__name__})
        H.check("the-corrupt-retained-payload-is-NOT-an-ordinary-pre-Plan-scope-refusal",
                corrupt_exc is not None and not isinstance(corrupt_exc, SR),
                {"exc": type(corrupt_exc).__name__ if corrupt_exc else "CLOSED"})
        H.check("the-corrupt-retained-payload-does-not-publish-PROJECT-SCOPE-LIMIT",
                corrupt_exc is not None and "PROJECT.SCOPE_LIMIT" not in str(corrupt_exc))
        H.check("the-corrupt-retained-payload-is-not-reported-as-a-vocabulary-fault",
                corrupt_exc is not None
                and "ANALYSIS_SPEC_CAPABILITY" not in str(corrupt_exc))
        H.check("preflight-indexing-does-not-bypass-retained-schema-validation",
                isinstance(corrupt_exc, VE) and "1034" not in str(corrupt_exc)[:60])
        # The generic exception's shape is exactly why the pre-Plan typed refusal
        # exists: it restates the whole instance and names no field/count/limit.
        gl = len(str(corrupt_exc))
        H.check("the-generic-retained-schema-error-restates-the-whole-instance",
                gl > 100000, {"genericErrorChars": gl})
        H.check("the-generic-retained-schema-error-names-no-field-count-and-limit-subject",
                "requestedCapabilities:1034>1024" not in str(corrupt_exc),
                {"genericErrorChars": gl})

        # A digest-inconsistent mutation is a DIFFERENT and earlier route, and it
        # must not be confused with either of the above.
        obj3 = copy.deepcopy(objects)
        blob3 = copy.deepcopy(blobs)
        for d, raw in list(blob3.items()):
            try:
                vv = json.loads(raw)
            except Exception:  # noqa: BLE001
                continue
            if isinstance(vv, dict) and vv.get("schemaVersion") == 2 \
                    and "requestedCapabilities" in vv:
                blob3[d] = C.canonical(dict(vv, requestedCapabilities=big))
                break
        try:
            M.close_run(copy.deepcopy(run), obj3, blob3)
            tampered = None
        except BaseException as e:  # noqa: BLE001
            tampered = e
        H.check("a-digest-inconsistent-retained-mutation-refuses-earlier-on-the-blob-digest-join",
                tampered is not None and "BLOB_DIGEST" in str(tampered),
                {"exc": type(tampered).__name__, "msg": str(tampered)[:120]})
        H.check("the-digest-route-and-the-schema-route-are-distinct-refusals",
                tampered is not None and corrupt_exc is not None
                and type(tampered) is not type(corrupt_exc))

exit_code = H.report(
    str(pathlib.Path(__file__).resolve().parent.parent /
        "evidence/probe-public-projection.json"),
    "public projection of the pre-Plan refusal and the retained-payload boundary",
    ["Reference-model only: no host, CLI, renderer or D9 interpreter executes. "
     "The termination and envelope are composed and schema-validated here, not "
     "delivered by a real surface.",
     "The shared fixture is used for CONSTRUCTION only. Every expected outcome "
     "in this file is authored here and none is read from the candidate's own "
     "check list.",
     "The corrupt-retained-payload case mutates a committed blob and re-closes; "
     "it demonstrates the reference verifier's path, not a real storage fault."])
sys.exit(1 if exit_code else 0)
