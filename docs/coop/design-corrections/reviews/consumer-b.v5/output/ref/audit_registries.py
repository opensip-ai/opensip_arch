"""Mechanical cross-registry audits the contracts assert about themselves."""

from __future__ import annotations

import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_ref as R
import closure as CL

OUT = "/tmp/opensip-design-corrections/consumer-b.v5/output/vectors"


def arrays_without_order(path):
    d = R.doc_json(path)
    bad = []

    def walk(node, p):
        if isinstance(node, dict):
            if node.get("type") == "array" and "x-opensip-order" not in node:
                bad.append(p)
            for k, v in node.items():
                if k in ("description", "x-opensip-digest", "x-opensip-order"):
                    continue
                walk(v, p + "/" + k)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, p + "/%d" % i)

    walk(d.get("$defs", {}), "#/$defs")
    return bad


def logical_path_usage():
    d = R.doc_json(R._PATHS["identity"])
    uses, plain = [], []

    def walk(node, p):
        if isinstance(node, dict):
            if node.get("$ref") == "#/$defs/LogicalPath":
                uses.append(p)
            if (node.get("type") == "string" and node.get("maxLength") == 4096
                    and "pattern" not in node and node.get("minLength") == 1
                    and p.endswith(("path", "Path", "logicalPath"))):
                plain.append(p)
            for k, v in node.items():
                if k == "description":
                    continue
                walk(v, p + "/" + k)
        elif isinstance(node, list):
            for i, v in enumerate(node):
                walk(v, p + "/%d" % i)

    walk(d.get("$defs", {}), "#/$defs")
    return sorted(set(uses)), sorted(set(plain))


def ladder_mirrors():
    reg = R.RELATION_REGISTRY
    caps = R.doc_json("docs/coop/design-corrections/native/capability-manifest-domains.v2.json")
    mirror = None
    for k, v in caps.items():
        if isinstance(v, dict) and "ladders" in v:
            mirror = v["ladders"]
    drift = {}
    if mirror is not None:
        for rel, lad in mirror.items():
            authority = reg.get(rel, {}).get("ladder")
            if authority is None:
                drift[rel] = {"mirrorOnly": lad}
            elif list(lad) != list(authority):
                drift[rel] = {"authority": authority, "mirror": lad}
        for rel in reg:
            if rel not in mirror:
                drift.setdefault(rel, {})["authorityOnly"] = reg[rel]["ladder"]
    return {"mirrorFound": mirror is not None, "drift": drift}


def rung_vocabulary_union():
    union = sorted({r for row in R.RELATION_REGISTRY.values() for r in row["ladder"]})
    policy_enum = sorted(R.doc_json(R._PATHS["policy-document"])["$defs"]["Rung"]["enum"])
    native_enum = sorted(R.NATIVE["$defs"]["Rung"]["enum"])
    return {"ladderUnion": union, "policyRungEnum": policy_enum,
            "nativeRungEnum": native_enum,
            "policyMatchesUnion": union == policy_enum,
            "nativeMatchesUnion": union == native_enum}


def relation_law_consumption():
    """relation-payload-schemas.v2's own x-opensip-digest-law: every annotated field is
    joined or declares retention: not-joined, and every named join field exists."""
    d = R.doc_json(R._PATHS["relation"])
    reg = d["x-opensip-relation-registry"]["relations"]
    problems = []
    for rel, row in reg.items():
        sel = row["selector"]
        node = d
        for part in sel[2:].split("/"):
            node = node[part]
        props = node.get("properties", {})
        for join in row.get("snapshotJoins", []):
            for k, v in join.items():
                if k.endswith("Field") and v not in props:
                    problems.append(f"{rel}: join field {v} not in selector")
        for name, sub in props.items():
            ann = sub.get("x-opensip-digest")
            if ann is None:
                continue
            joined = any(v == name for join in row.get("snapshotJoins", [])
                         for k, v in join.items() if k.endswith("Field"))
            if rel == "clones" and name in ("bodyIdentity", "normalisationLevel",
                                            "normalisationVersion"):
                joined = True
            if not joined and ann.get("retention") != "not-joined":
                problems.append(f"{rel}.{name}: annotated, not joined, "
                                f"retention={ann.get('retention')}")
    return problems


def capability_manifest_domain_conflict():
    delivery = R.doc_json("docs/coop/artifacts/delivery.v4.json")
    op = delivery["derivedFrom"]["operations"][17]["value"]
    regs = op["valueDomains"]["registries"]
    fp = R.doc_json("docs/coop/artifacts/fact-plane.v1.json")
    live_relations = sorted(fp["relationRegistry"]["relations"])
    live_def = fp.get("deficiencyVocabulary", {})
    live_def_values = live_def.get("values", live_def) if isinstance(live_def, dict) else live_def
    return {
        "capabilityManifestRelationDomain":
            regs["fact-plane.v1#relationRegistry.relations"]["members"],
        "capabilityManifestRelationDomainSource":
            regs["fact-plane.v1#relationRegistry.relations"]["source"],
        "liveFactPlaneRelations": live_relations,
        "capabilityManifestDeficiencyDomain":
            regs["fact-plane.v1#deficiencyVocabulary"]["members"],
        "liveFactPlaneDeficiencyVocabulary": live_def_values,
        "productRelations": sorted(R.RELATION_REGISTRY),
        "productDeficiencies": R.NATIVE["$defs"]["DeficiencyV2"]["enum"],
        "relationsUnexpressible": sorted(
            set(R.RELATION_REGISTRY)
            - set(regs["fact-plane.v1#relationRegistry.relations"]["members"])),
        "deficienciesUnexpressible": sorted(
            set(R.NATIVE["$defs"]["DeficiencyV2"]["enum"])
            - set(regs["fact-plane.v1#deficiencyVocabulary"]["members"])),
        "platformDomainMembers":
            regs["PLATFORM-ID-DOMAIN-V1"]["members"],
        "securitySelectedPlatformIds": R.MATRIX["platformFamilies"],
        "platformIdsInTheManifestDomainOutsideTheSelectedProduct": sorted(
            set(regs["PLATFORM-ID-DOMAIN-V1"]["members"])
            - set(R.MATRIX["platformFamilies"]) - {"all-supported"}),
        "admDomainGate": op["admission"]["ADM-DOMAIN"]["statement"],
    }


def scope_limit_arithmetic():
    per_mode = {}
    for mode in R.MATRIX["languageModes"]:
        per_mode[mode] = sum(1 for c in R.CAPABILITY_IDS
                             if R.CELLS[(c, mode)]["state"] != "NOT-SELECTED")
    ts = per_mode["ts-tsconfig"]
    return {
        "capabilitiesRequestedPerUnitByMode": per_mode,
        "analysisSpecBound": 1024,
        "typeScriptUnitsThatFit": 1024 // ts,
        "rowsAt93Units": 93 * ts,
        "rowsAt94Units": 94 * ts,
        "contractClaim": "11 per TypeScript unit and 10 per Rust unit; 93 units fit at "
                         "1023 rows and 94 do not, at 1034",
        "verified": ts == 11 and per_mode["rust-cargo"] == 10
        and 93 * ts == 1023 and 94 * ts == 1034,
        "scopeDescriptorWorkspaceRootBound": 1024,
        "discoveryFirstPartyUnitCap": 4096,
        "effectiveScopeLimit": "1024 distinct workspace roots; 1025..4096 valid "
                               "discovered roots refuse PROJECT.SCOPE_LIMIT without "
                               "truncation",
    }


def public_detail_registry_parity():
    reg = R.doc_json("docs/coop/design-corrections/public-detail-registry.v1.json")
    codes = {r["code"] for r in reg["records"]}
    enum = set(R.COMMON["$defs"]["DomainDetailCode"]["enum"])
    aliases = {a["internalCode"] for a in reg["internalAliases"]}
    route_keys = set(R.ROUTE_REGISTRY["keys"])
    context_free = set()
    for k, row in R.ROUTE_REGISTRY["keys"].items():
        if not row.get("originDependent"):
            d = row.get("route", {}).get("domainDetail")
            if d:
                context_free.add(k)
    return {
        "registryCodeCount": len(codes),
        "commonEnumCount": len(enum),
        "identical": codes == enum,
        "onlyInRegistry": sorted(codes - enum),
        "onlyInEnum": sorted(enum - codes),
        "internalAliases": sorted(aliases),
        "aliasesThatAreNotRouteKeys": sorted(aliases - route_keys),
        "contextFreeRouteKeysWithAPublicDetail": sorted(context_free),
        "contextFreeKeysMissingAnAlias": sorted(context_free - aliases),
        "deficienciesThatArePublicDetailCodes": sorted(
            set(R.NATIVE["$defs"]["DeficiencyV2"]["enum"]) & enum),
        "deficienciesThatAreNot": sorted(
            set(R.NATIVE["$defs"]["DeficiencyV2"]["enum"]) - enum),
    }


def main():
    out = {
        "arraysWithoutDeclaredOrder": {
            name: arrays_without_order(path)
            for name, path in R._PATHS.items()
            if name in ("identity", "relation", "native", "common", "policy-document",
                        "imported-evidence", "invocation-record", "comparison-result",
                        "repair", "review", "test-execution", "graph-query",
                        "policy-test", "baseline-artifact", "command-envelope",
                        "command-inventory-schema", "product-configuration")
        },
        "logicalPathUsageInIdentitySchemas": dict(
            zip(("fieldsReferencingLogicalPath", "pathLikeFieldsWithoutIt"),
                logical_path_usage())),
        "ladderMirrorDriftCheck": ladder_mirrors(),
        "rungVocabularyUnion": rung_vocabulary_union(),
        "relationDigestLawConsumption": relation_law_consumption(),
        "capabilityManifestDomainConflict": capability_manifest_domain_conflict(),
        "scopeLimitArithmetic": scope_limit_arithmetic(),
        "publicDetailRegistryParity": public_detail_registry_parity(),
        "unannotated64HexFields": {
            b: CL.unannotated_hex64_fields(b) for b in ("identity", "native")},
    }
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, "registry-audits.json"), "w") as fh:
        json.dump(out, fh, indent=1, sort_keys=True, ensure_ascii=False)
    print(json.dumps(out, indent=1)[:12000])


if __name__ == "__main__":
    main()
