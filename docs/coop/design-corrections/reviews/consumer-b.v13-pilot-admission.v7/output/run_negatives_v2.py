#!/usr/bin/env python3
"""Bounded isolated negatives for law families added this checkpoint.

Each control mutates retained operands, remints identities that include the
mutated field, and records the actual checker refusal. Not product qualification.
"""
from __future__ import annotations

import copy
import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v7/output")
sys.path.insert(0, str(OUT))

from helpers import law_admit, store, h, canonical, builder, pilot_checks  # noqa: E402
from helpers.store import load_export  # noqa: E402


def load_st():
    return load_export(json.loads((OUT / "runs" / "ts.store.json").read_text()))


def remint_canonical(st, domain, obj, old_ident=None):
    ident = st.put_canonical_record(domain, obj)
    return ident


def main():
    results = []

    def rec(fid, law, checker, mutation, refused, first, reminted):
        results.append(
            {
                "id": fid,
                "lawFamily": law,
                "checker": checker,
                "mutation": mutation,
                "refused": bool(refused),
                "firstRefusal": first,
                "identitiesReminted": reminted,
            }
        )
        print(("REFUSED" if refused else "UNEXPECTED_PASS"), fid, first)

    st0 = load_st()
    plan = next(o for i, o in st0.objects.items() if i.startswith("plan2:"))
    spec = law_admit._c(st0, plan["analysisSpecDigest"])
    proof = next(o for i, o in st0.objects.items() if i.startswith("proof3:"))
    ei = law_admit._c(st0, proof["executionInputsDigest"])
    enum_plan = law_admit._c(
        st0, next(p["payloadDigest"] for p in spec["parameters"] if p["schemaDigest"] == builder.ENUM_PLAN_DIGEST)
    )

    # 1 uniqueness
    spec2 = copy.deepcopy(spec)
    spec2["requestedCapabilities"].append(copy.deepcopy(spec2["requestedCapabilities"][0]))
    err = law_admit.check_uniqueness_requested_caps(spec2)
    rec("NEG-UNIQ-CAPS", "x-opensip-uniqueness ownershipTuple",
        "law_admit.check_uniqueness_requested_caps",
        "duplicate first requestedCapabilities row", err, err[0] if err else None, [])

    # 2 vocabulary
    spec3 = copy.deepcopy(spec)
    spec3["requestedCapabilities"][0]["capabilityId"] = "not-a-matrix-id"
    err = law_admit.check_vocabulary_requested_caps(spec3)
    rec("NEG-VOCAB-CAP", "x-opensip-vocabulary capabilityId matrix",
        "law_admit.check_vocabulary_requested_caps",
        "capabilityId=not-a-matrix-id", err, err[0] if err else None, [])

    # 3 default caps
    spec4 = copy.deepcopy(spec)
    spec4["requestedCapabilities"] = [r for r in spec4["requestedCapabilities"] if r["capabilityId"] != "types"]
    err = law_admit.check_default_caps_required(spec4, "ts-tsconfig")
    rec("NEG-DEFAULT-CAPS", "matrix requiredDefault",
        "law_admit.check_default_caps_required",
        "drop types from requestedCapabilities", err, err[0] if err else None, [])

    # 4 subject language
    invs = [law_admit._c(st0, r["digest"]) for r in ei["selectedRefs"] if r["domain"] == "subject-inventory"]
    invs2 = copy.deepcopy(invs)
    for inv in invs2:
        if inv.get("kind") == "file" and inv.get("rows"):
            inv["rows"][0]["subjectLanguage"] = "rust"
            break
    err = law_admit.check_subject_language(invs2)
    rec("NEG-SUBJECT-LANGUAGE", "x-opensip-subject-language-table",
        "law_admit.check_subject_language",
        "file row subjectLanguage=rust", err, err[0] if err else None, [])

    # 5 coverage cause: nativeCause without deficiency
    st = load_st()
    cov_id = next(i for i, o in st.objects.items() if i.startswith("coverage2:"))
    cov = dict(st.objects[cov_id])
    payload = law_admit._c(st, cov["payloadDigest"])
    payload = copy.deepcopy(payload)
    payload["entry"]["deficiency"] = None
    payload["entry"]["nativeCause"] = "capability-missing"
    pd = hashlib_sha(payload)
    st.put_raw_digest_record(payload)
    cov["payloadDigest"] = pd
    new_cov = remint_canonical(st, "coverage", {k: v for k, v in cov.items() if not str(k).startswith("_")})
    err = law_admit.check_coverage_cause_registry(st)
    rec("NEG-COVERAGE-CAUSE", "x-opensip-deficiency-cause-registry noDeficiencyNoCause",
        "law_admit.check_coverage_cause_registry",
        "coverage entry nativeCause set while deficiency null; reminted coverage2",
        err, err[0] if err else None, [new_cov])

    # 6 scope capability mixed complete — checker on v1 preserved store
    st_old = load_export(json.loads((OUT / "inventory" / "ts-before-scope-capability-correction.store.json").read_text()))
    uni = next(o for i, o in st_old.objects.items() if isinstance(o, dict) and o.get("tsconfigGraphHash"))
    err = law_admit.check_scope_capability_law(st_old, uni)
    rec("NEG-SCOPE-CAPABILITY", "x-opensip-digest-domains.scopeCapabilityLaw",
        "law_admit.check_scope_capability_law",
        "v1 export complete clones Coverage over json+ts subjects (preserved bytes)",
        err, err[0] if err else None, [])

    # 7 target attribution external evaluationNativeId
    st = load_st()
    ei2 = copy.deepcopy(ei)
    attr_ref = next(r for r in ei2["selectedRefs"] if r["domain"] == "target-attribution")
    attr = copy.deepcopy(law_admit._c(st, attr_ref["digest"]))
    attr["evaluationNativeId"] = "left-pad"
    ad = hashlib_sha(attr)
    st.put_raw_digest_record(attr)
    attr_ref["digest"] = ad
    err = law_admit.check_target_attribution(st, plan, ei2)
    rec("NEG-ATTRIBUTION-EXTERNAL-ID", "x-opensip-join-law packagePathCases.external-package",
        "law_admit.check_target_attribution",
        "occupancy=external evaluationNativeId=left-pad (must be null)",
        err, err[0] if err else None, [ad])

    # 8 selectedRefs drop coverage
    ei3 = copy.deepcopy(ei)
    ei3["selectedRefs"] = [r for r in ei3["selectedRefs"] if r["domain"] != "coverage"]
    err = law_admit.check_selected_refs_totality(st0, plan, ei3)
    rec("NEG-SELECTED-REFS", "execution-inputs-contract §1 selectedRefs totality",
        "law_admit.check_selected_refs_totality",
        "drop all coverage selectedRefs", err, err[0] if err else None, [])

    # 9 candidate source paths omitted
    ep = copy.deepcopy(enum_plan)
    for cell in ep["cells"]:
        if cell["capabilityId"] == "clones-near":
            cell["programBindings"][0].pop("candidateSourcePaths", None)
    err = law_admit.check_extent_law(ep, law_admit._c(st0, ep["membershipDigest"]),
                                     next(o for i, o in st0.objects.items() if i.startswith("snapshot2:")))
    rec("NEG-CANDIDATE-PATHS", "x-opensip-kind-derivation note + enumeration candidateSourcePaths",
        "law_admit.check_extent_law",
        "omit candidateSourcePaths on clones-near binding", err, err[0] if err else None, [])

    # 10 vcs fabricated coverage
    ei4 = copy.deepcopy(ei)
    for acc in ei4["nativeCoverageAccounts"]:
        if acc["relation"] == "vcs-change":
            acc["applicability"] = "supported-available"
            acc["coverageIds"] = ["0" * 64]
    err = law_admit.check_vcs_inapplicable(st0, ei4)
    rec("NEG-VCS-FABRICATED", "execution-inputs §5 inapplicable-vcs",
        "law_admit.check_vcs_inapplicable",
        "vcs-change applicability=supported-available with fabricated coverageId",
        err, err[0] if err else None, [])

    # 11 kind derivation
    ep2 = copy.deepcopy(enum_plan)
    for cell in ep2["cells"]:
        if cell["capabilityId"] == "inventory":
            cell["kinds"] = ["file"]
    err = law_admit.check_kind_derivation(ep2)
    rec("NEG-KIND-DERIVATION", "x-opensip-kind-derivation",
        "law_admit.check_kind_derivation",
        "inventory cell kinds=[file] omitting package", err, err[0] if err else None, [])

    # 12 payload schema digest
    st = load_st()
    fid = next(i for i, o in st.objects.items() if i.startswith("fact2:") and o.get("relation") == "file")
    fact = dict(st.objects[fid])
    fact["payloadSchemaDigest"] = "0" * 64
    newf = remint_canonical(st, "fact", fact)
    err = law_admit.check_payload_schema_digests(st)
    rec("NEG-PAYLOAD-SCHEMA", "x-opensip-payload-registry law.payloadSchemaDigest",
        "law_admit.check_payload_schema_digests",
        "file fact payloadSchemaDigest zeroed; reminted fact2",
        err, err[0] if err else None, [newf])

    # 13 native atom with evidence
    pol = law_admit._c(st0, plan["policyDigest"])
    pol2 = copy.deepcopy(pol)
    pol2["rules"][0]["emitWhen"]["evidence"] = "runtime"
    err = law_admit.check_policy_evidence_declaration(pol2)
    rec("NEG-NATIVE-ATOM-EVIDENCE", "x-opensip-evidence-relation-registry evidenceDeclarationRule",
        "law_admit.check_policy_evidence_declaration",
        "file.exists atom carries evidence=runtime", err, err[0] if err else None, [])

    # 14 H-frame C(X) under H
    st = load_st()
    snap_id = next(i for i in st.objects if i.startswith("snapshot2:"))
    snap = st.objects[snap_id]
    hx = snap_id.split(":")[1]
    st.blobs[hx] = canonical.encode(snap)
    err = pilot_checks.verify_h_frame_for_object(st, snap_id, "snapshot", snap)
    rec("NEG-H-FRAME-C-UNDER-H", "identity-and-evidence §3 framed preimage",
        "pilot_checks.verify_h_frame_for_object",
        "replace blobs[H] with C(X)", err, err[0] if err else None, [])

    unexpected = [r for r in results if not r["refused"]]
    dest = OUT / "inventory" / "negatives.json"
    dest.write_text(json.dumps({"controls": results, "unexpectedPass": [u["id"] for u in unexpected]}, indent=2) + "\n")
    print("wrote", dest, "n", len(results), "unexpectedPass", len(unexpected))
    return 0 if not unexpected else 1


def hashlib_sha(obj):
    from helpers import h as _h, canonical as _c
    return _h.raw_sha256(_c.encode(obj))


if __name__ == "__main__":
    sys.exit(main())
