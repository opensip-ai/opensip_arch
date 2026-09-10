#!/usr/bin/env python
"""CB6-MUST-1: per-requirement producer/consumer vocabulary.

Independent structural assessment of the repair, over the frozen bytes:
  A. Does the native per-requirement vocabulary preserve EVERY native
     sufficiency cause, including the four blind v6 named inexpressible?
  B. Is the imported vocabulary SEPARATELY defined (not merged into the native
     one), with its own outcomes?
  C. Did the global D9 / public termination vocabulary silently grow?
  D. Are the schema/reference/prose joins consistent (authorities named in the
     schema actually resolve, and the enums they name actually match)?
"""
import json
import os
import sys

ROOT = "/tmp/opensip-design-corrections/candidate-subject.v17"
DC = os.path.join(ROOT, "docs/coop/design-corrections")
REV = "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews"


def L(p):
    with open(os.path.join(DC, p)) as fh:
        return json.load(fh)


def main():
    out = sys.argv[1]
    rep = {}

    common = L("workflows/schemas/common.schema.json")
    native = L("native/native-evidence.schemas.v2.json")
    imported = L("workflows/schemas/imported-evidence.schema.json")
    repair = L("workflows/schemas/repair.schema.json")

    cd = common["$defs"]
    nd = native["$defs"]

    # --- A. native plane vocabulary vs DeficiencyV2 ---
    nsd = cd.get("NativeSufficiencyDeficiency")
    dv2 = nd.get("DeficiencyV2")
    nsd_enum = nsd.get("enum") if nsd else None
    dv2_enum = dv2.get("enum") if dv2 else None
    rep["nativeSufficiencyDeficiencyEnum"] = nsd_enum
    rep["deficiencyV2Enum"] = dv2_enum
    rep["nativeVocabEqualsDeficiencyV2"] = (
        nsd_enum is not None and dv2_enum is not None
        and set(nsd_enum) == set(dv2_enum)
    )
    rep["nativeVocabOrderEqual"] = nsd_enum == dv2_enum

    formerly_inexpressible = [
        "derivation-policy-unmet",
        "external-consumers-unknown",
        "input-closure-incomplete",
        "resolution-incomplete",
    ]
    rep["blindV6InexpressibleValues"] = formerly_inexpressible
    rep["nowExpressibleOnNativePlane"] = {
        v: (nsd_enum is not None and v in nsd_enum)
        for v in formerly_inexpressible
    }
    rep["allFourFormerlyInexpressibleNowExpressible"] = all(
        rep["nowExpressibleOnNativePlane"].values())

    # --- B. imported plane separately defined ---
    ird = cd.get("ImportedRequirementDeficiency")
    ird_enum = ird.get("enum") if ird else None
    rep["importedRequirementDeficiencyEnum"] = ird_enum
    rep["importedVocabExists"] = ird_enum is not None
    rep["importedDisjointFromNative"] = (
        ird_enum is not None and nsd_enum is not None
        and not (set(ird_enum) & set(nsd_enum))
    )
    law = imported.get("x-opensip-imported-requirement-law")
    rep["importedLawPresent"] = law is not None
    if law:
        outcomes = law.get("outcomes")
        rep["importedLawOutcomeKeys"] = (
            sorted(outcomes) if isinstance(outcomes, dict)
            else [o.get("value") or o.get("outcome") for o in outcomes]
            if isinstance(outcomes, list) else outcomes)
        rep["importedLawOutcomeCount"] = (
            len(outcomes) if hasattr(outcomes, "__len__") else None)
        rep["importedLawEnumMatchesCommonDef"] = (
            set(rep["importedLawOutcomeKeys"] or []) == set(ird_enum or []))
        rep["perKindApplicabilityPresent"] = "perKindApplicability" in law
        rep["perKindApplicability"] = law.get("perKindApplicability")

    # --- C. D9 / public termination vocabulary growth ---
    d9 = cd.get("D9Deficiency")
    rep["d9DeficiencyEnum"] = d9.get("enum") if d9 else None
    # compare against the v16 bytes of common.schema.json
    import hashlib
    import tarfile
    rep["d9EnumMemberCount"] = len(d9["enum"]) if d9 and "enum" in d9 else None

    # inherited D9 contract, must be byte-untouched
    d9c = os.path.join(ROOT, "docs/coop/artifacts/d9-exit-contract.v1.14.json")
    h = hashlib.sha256(open(d9c, "rb").read()).hexdigest()
    rep["inheritedD9ContractSha256"] = h
    rep["inheritedD9ContractDeclaredPin"] = \
        "8dd3303855f49bfdbb2751ee65f54a906405f0654159ebe815472f73cdf7da31"
    rep["inheritedD9ContractUnchanged"] = (
        h == "8dd3303855f49bfdbb2751ee65f54a906405f0654159ebe815472f73cdf7da31")

    # --- D. joins: the authorities the repair schema names must resolve ---
    ervoc = (repair["$defs"]["EvidenceRequirement"]["properties"]["deficiency"]
             ["x-opensip-vocabulary"])
    rep["repairNamedNativeAuthority"] = ervoc["nativePlaneAuthority"]
    rep["repairNamedImportedAuthority"] = ervoc["importedPlaneAuthority"]
    rep["namedNativeAuthorityResolves"] = "DeficiencyV2" in nd
    rep["namedImportedAuthorityResolves"] = (
        law is not None and "outcomes" in law)
    rep["repairDeficiencyOneOfRefs"] = [
        r["$ref"] for r in
        repair["$defs"]["EvidenceRequirement"]["properties"]["deficiency"]["oneOf"]
    ]
    rep["repairRequired"] = repair["$defs"]["EvidenceRequirement"]["required"]
    rep["repairAdditionalProperties"] = \
        repair["$defs"]["EvidenceRequirement"]["additionalProperties"]
    rep["satisfiedIsBooleanTyped"] = (
        repair["$defs"]["EvidenceRequirement"]["properties"]["satisfied"]
        == {"type": "boolean"})
    rep["presenceLawAllOf"] = repair["$defs"]["EvidenceRequirement"]["allOf"]

    with open(out, "w") as fh:
        json.dump(rep, fh, indent=1, sort_keys=True)
    for k in sorted(rep):
        v = rep[k]
        print("%-46s %s" % (k, json.dumps(v)[:230]))


if __name__ == "__main__":
    main()
