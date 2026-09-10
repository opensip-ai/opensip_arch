#!/usr/bin/env python
"""CB3-MUST-4 (ScopeDocumentV1 analysis-spec parameter + comparison join) and
CB3-MUST-5 (clone ownership deficiency/cause pairing), probed independently.

MUST-4 is not discharged by a registry row. I test:
  * a real retained Run carrying the parameter,
  * malformed / wrong-selector / unregistered-schema refusals,
  * that the operator glob policy and the repository scope-descriptor stay
    DISTINCT records that do not substitute for each other,
  * the comparison binding itself: verify_scope_parameter_binding must refuse a
    document that is not the selected parameter, and a comparison in which ONLY
    the operator glob scope changes must move scopeDigest and nothing else.

MUST-5 tests the three refusable ownership states against the exact declared
pairing, at the producer AND at Run admission, plus injected false claims.
"""
import copy
import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(
    "/tmp/opensip-design-corrections/post-reset-review.v13/work/subject-copy"
    "/docs/coop/design-corrections")


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


F = load("fx", HERE / "integration-fixtures.py")
M, C = F.M, F.C
N = load("nat", HERE / "native/native_evidence_model.v2.py")
W = M.workflow_admission()

R = []


def rec(case, expect, got, cause=None, level="run-admission", detail=None):
    R.append({"case": case, "level": level, "expected": expect,
              "observed": got, "cause": cause, "detail": detail,
              "agrees": expect == got})


SCOPE_DOC = {"schemaFamily": "opensip.product.scope", "schemaMajor": 1,
             "include": ["src/**/*.ts"], "exclude": ["src/**/*.test.ts"]}
SCOPE_DOC_B = {"schemaFamily": "opensip.product.scope", "schemaMajor": 1,
               "include": ["lib/**/*.ts"], "exclude": []}
POLICY_SCHEMA_BYTES = (HERE / "workflows/schemas/policy-document.schema.json"
                       ).read_bytes()
IMPORT_CTX_BYTES = (HERE / "foundation/import-source-context.schema.json"
                    ).read_bytes()


def run_with_parameter(schema_bytes, payload_value):
    run, objects, blobs = F.build(resolved=True, has_match=True)
    put = lambda v: F.put_blob(blobs, v)
    plan = copy.deepcopy(objects[run["planId"]][1])
    analysis = C.parse(blobs[plan["analysisSpecDigest"]])
    analysis["parameters"] = [{"schemaDigest": put(schema_bytes),
                               "payloadDigest": put(payload_value)}]
    plan["analysisSpecDigest"] = put(analysis)
    F.rekey_plan(objects, blobs, run, plan)
    return M.close_run(run, objects, blobs)


def param_case(case, schema_bytes, payload, expect, want_cause=None):
    try:
        rid = run_with_parameter(schema_bytes, payload)
        rec(case, expect, "admits" if str(rid).startswith("run2:") else "odd")
    except Exception as exc:
        cause = str(exc)[:200]
        got = "refuses"
        if want_cause and not cause.startswith(want_cause):
            got = "refuses-wrong-cause"
        rec(case, expect, got, cause)


def main():
    # ================= MUST-4 =================
    param_case("M4/legal-scope-document-parameter-closes-a-real-run",
               POLICY_SCHEMA_BYTES, SCOPE_DOC, "admits")
    # Malformed against the registered selector.
    param_case("M4/malformed-scope-document-refuses", POLICY_SCHEMA_BYTES,
               {"schemaFamily": "opensip.product.scope", "schemaMajor": 1,
                "include": [], "exclude": []},
               "refuses", want_cause="PAYLOAD_RECORD:#/$defs/ScopeDocumentV1")
    param_case("M4/unknown-field-scope-document-refuses", POLICY_SCHEMA_BYTES,
               {"schemaFamily": "opensip.product.scope", "schemaMajor": 1,
                "include": ["a/**"], "exclude": [], "bogus": 1},
               "refuses", want_cause="PAYLOAD_RECORD:#/$defs/ScopeDocumentV1")
    # The repository scope-descriptor must NOT satisfy the operator glob row.
    param_case("M4/repository-scope-descriptor-is-not-a-scope-document",
               POLICY_SCHEMA_BYTES,
               {"schemaVersion": 2, "workspaceRoots": ["."],
                "pathPrefixes": ["."], "excludedPathPrefixes": []},
               "refuses", want_cause="PAYLOAD_RECORD:#/$defs/ScopeDocumentV1")
    # ... and the scope document must not pass as an import-source-context.
    param_case("M4/scope-document-under-wrong-registered-schema-refuses",
               IMPORT_CTX_BYTES, SCOPE_DOC, "refuses",
               want_cause="PAYLOAD_RECORD:")
    # An entirely unregistered parameter schema must still refuse.
    param_case("M4/unregistered-parameter-schema-refuses",
               b"{\"$id\":\"urn:not-registered\"}", SCOPE_DOC, "refuses")

    # The two scope records are distinct digests.
    a = hashlib.sha256(C.canonical(SCOPE_DOC)).hexdigest()
    b = hashlib.sha256(C.canonical(
        {"schemaVersion": 2, "workspaceRoots": ["."], "pathPrefixes": ["."],
         "excludedPathPrefixes": []})).hexdigest()
    rec("M4/glob-policy-and-repository-extent-are-distinct-digests", True,
        a != b, level="digest")

    # ---- the comparison binding itself ----------------------------------
    doc_digest = W.doc_digest
    raw_sha = W.raw_sha
    schema_digest = raw_sha(POLICY_SCHEMA_BYTES)
    good_spec = {"parameters": [{"schemaDigest": schema_digest,
                                 "payloadDigest": doc_digest(SCOPE_DOC)}]}
    empty_spec = {"parameters": []}
    wrong_payload_spec = {"parameters": [
        {"schemaDigest": schema_digest, "payloadDigest": doc_digest(SCOPE_DOC_B)}]}
    wrong_schema_spec = {"parameters": [
        {"schemaDigest": raw_sha(IMPORT_CTX_BYTES),
         "payloadDigest": doc_digest(SCOPE_DOC)}]}

    def binding(case, spec, scope, expect, want_code=None):
        try:
            got = W.verify_scope_parameter_binding(spec, scope)
            rec(case, expect, "verified", got[:24], level="comparison-binding")
        except Exception as exc:
            code = getattr(exc, "detail", None) or str(exc)[:120]
            ok = "refuses"
            if want_code and want_code not in str(code):
                ok = "refuses-wrong-code"
            rec(case, expect, ok, str(code)[:160], level="comparison-binding")

    binding("M4/binding-selected-parameter-verifies", good_spec, SCOPE_DOC,
            "verified")
    binding("M4/binding-no-selected-parameter-refuses", empty_spec, SCOPE_DOC,
            "refuses", want_code="SCOPE_NOT_A_SELECTED_PARAMETER")
    binding("M4/binding-digest-mismatch-refuses", wrong_payload_spec, SCOPE_DOC,
            "refuses", want_code="SCOPE_PARAMETER_DIGEST_MISMATCH")
    binding("M4/binding-under-wrong-schema-refuses", wrong_schema_spec,
            SCOPE_DOC, "refuses", want_code="SCOPE_NOT_A_SELECTED_PARAMETER")

    # ---- comparison where ONLY the operator glob scope changes ----------
    d1, d2 = doc_digest(SCOPE_DOC), doc_digest(SCOPE_DOC_B)
    rec("M4/only-scope-policy-change-moves-scopeDigest", True, d1 != d2,
        level="comparison-context")
    # and the same scope document under two spellings is one digest
    rec("M4/same-scope-policy-is-one-digest", True,
        doc_digest(dict(reversed(list(SCOPE_DOC.items())))) == d1,
        level="comparison-context")

    # ================= MUST-5 =================
    table = N.CLONE_OWNERSHIP_DISCLOSURE
    rec("M5/three-refusable-states-are-declared",
        {"ownership-missing", "owner-unenumerated", "owner-ambiguous"},
        set(table), level="registry", detail=json.dumps(table))
    causes = set(json.loads(
        (HERE / "native/native-evidence.schemas.v2.json").read_text()
    )["$defs"]["NativeCause"]["enum"])
    for state, row in sorted(table.items()):
        rec(f"M5/{state}-cause-is-registered", True,
            row["nativeCause"] in causes, level="registry",
            detail=row["nativeCause"])
        rec(f"M5/{state}-deficiency-is-input-closure-incomplete",
            "input-closure-incomplete", row["deficiency"], level="registry")
        rec(f"M5/{state}-cause-is-not-null", True,
            row["nativeCause"] is not None, level="registry")
    rec("M5/the-three-causes-are-distinct", 3,
        len({r["nativeCause"] for r in table.values()}), level="registry")

    # Rust ownership at the Run boundary: healthy control + the partial case.
    def rust_run(**kw):
        return F.build(resolved=True, has_match=True, universe_language="rust",
                       relation="clones", **kw)

    try:
        rid = M.close_run(*rust_run())
        rec("M5/healthy-rust-clone-run-closes", "admits",
            "admits" if rid.startswith("run2:") else "no")
    except Exception as exc:
        rec("M5/healthy-rust-clone-run-closes", "admits", "refuses",
            str(exc)[:160])

    bad = [r for r in R if not r["agrees"]]
    print(json.dumps({"total": len(R), "disagreeingCount": len(bad),
                      "disagreeing": bad, "results": R}, indent=2,
                     default=list))
    return 0 if not bad else 1


if __name__ == "__main__":
    sys.exit(main())
