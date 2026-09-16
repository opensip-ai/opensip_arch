"""Source39 Run-closure laws shared by closure admission and the synthetic host builders.

- stage output schema registration: identity-and-evidence s3 lines 1303-1325; identity-schemas.v3.json
  $defs/stage-spec/properties/outputSchemaDigest/x-opensip-digest/registeredBy (HC-15)
- normalization specification map: identity-and-evidence lines 1065-1089; x-opensip-digest-domains.normalizationSpecificationLaw (HC-16)
- body eligibility: x-opensip-digest-domains.bodyEligibilityLaw; execution-inputs-contract s5 (HC-14, HC-17)
- snapshot sourceInventory pruned-tree read join: identity-and-evidence lines 548-593; security-and-lifecycle S3 lines 266-279 (HC-21)
Published paths, patterns and declaration names are read from the kit documents rather than restated.
"""
from jsonschema import Draft202012Validator
from jsonschema.exceptions import SchemaError
import re

import canonical as K
import schemas

KIT = schemas.kit()
ID = "foundation/identity-schemas.v3.json"
DD = KIT.doc(ID)["x-opensip-digest-domains"]
REGISTERED_BY = KIT.doc(ID)["$defs"]["stage-spec"]["properties"]["outputSchemaDigest"]["x-opensip-digest"]["registeredBy"]
NSL = DD["normalizationSpecificationLaw"]
UNIVERSE_ROWS = DD["domainSets"]["native-semantic-universe"]
MODE_LANGUAGE = DD["languageModes"]["map"]
POLICY_UNIVERSE_MAP = KIT.doc(ID)["x-opensip-evaluator-profile"]["policyUniverseMap"]
JSON_SCHEMA_2020_12 = "https://json-schema.org/draft/2020-12/schema"  # identity-and-evidence line 1312
OPERATION_SEGMENT = re.compile(REGISTERED_BY["operationSegment"])
VCS_SEGMENTS = {".git", ".hg", ".svn", ".jj"}  # native U-4a


# ------------------------------------------------------------------ stage output schema registration
def stage_output_tree_path(operation):
    return REGISTERED_BY["treePath"].replace("{operation}", operation)


def stage_output_schema_bytes(operation, output_domains, title):
    decl = {"schemaVersion": REGISTERED_BY["declares"]["schemaVersion"], "operation": operation, "outputDomains": list(output_domains)}
    return K.C({"$schema": JSON_SCHEMA_2020_12, "title": title, "type": "object", REGISTERED_BY["declaration"]: decl})


def stage_output_faults(store, spec, producer):
    """spec: admitted stage-spec; producer: admitted closure descriptor named by spec.producerClosure."""
    op = spec["operation"]
    if not OPERATION_SEGMENT.search(op):
        return ["STAGE_OUTPUT_SCHEMA_OPERATION_NOT_A_PATH_SEGMENT"]
    row = next((r for r in producer["tree"] if r["path"] == stage_output_tree_path(op)), None)
    if row is None:
        return ["STAGE_OUTPUT_SCHEMA_UNREGISTERED"]
    if row["sha256"] != spec["outputSchemaDigest"]:
        return ["STAGE_OUTPUT_SCHEMA_REGISTRATION_MISMATCH"]
    raw = store.blobs.get(row["sha256"])
    if raw is None:
        return ["EVIDENCE_UNAVAILABLE:stage-output-schema"]
    try:
        doc = K.parse_raw(raw)
    except (K.AdmissionError, ValueError):
        return ["STAGE_OUTPUT_SCHEMA_DOCUMENT_INVALID"]
    if not isinstance(doc, dict) or doc.get("$schema") != JSON_SCHEMA_2020_12:
        return ["STAGE_OUTPUT_SCHEMA_DOCUMENT_INVALID"]
    try:
        Draft202012Validator.check_schema(doc)
    except SchemaError:
        return ["STAGE_OUTPUT_SCHEMA_DOCUMENT_INVALID"]
    want = {"schemaVersion": REGISTERED_BY["declares"]["schemaVersion"], "operation": op, "outputDomains": spec["outputDomains"]}
    decl = doc.get(REGISTERED_BY["declaration"])
    if decl is None or K.C(decl) != K.C(want):
        return ["STAGE_OUTPUT_SCHEMA_DECLARATION_MISMATCH"]
    return []


# ------------------------------------------------------------------ normalization specification map
def normalization_map_bytes(normalizer_id, level_digests):
    levels = [{"level": lvl, "specificationDigest": level_digests[lvl]} for lvl in sorted(level_digests, key=lambda s: s.encode())]
    return K.C({"schemaVersion": 1, "normalizerId": normalizer_id, "levels": levels})


def normalization_owner(bound):
    """The closure that interprets the body span: languageVersionBinding.normalizationClosure over the admitted context."""
    spec = bound["row"]["languageVersionBinding"].get("normalizationClosure")
    if spec is None:
        return None, "cb24.NORMALIZATION_CLOSURE_UNDECLARED"
    cur = bound["contextAdmission"]["context"]
    for step in spec["path"]:
        cur = cur[step]
    desc = bound["contextAdmission"]["detail"]["closures"].get(spec["kind"])
    if desc is None or desc["kind"] != spec["kind"] or "closure2:" + K.H("closure", desc) != cur:
        return None, "cb24.NORMALIZATION_CLOSURE_UNBOUND"
    return desc, None


def normalization_map_faults(store, payload, bound):
    """normalizationSpecificationLaw.joins, in their published order."""
    owner, refusal = normalization_owner(bound)
    if refusal:
        return [refusal]
    row = next((r for r in owner["tree"] if r["path"] == NSL["closureTreePath"]), None)
    if row is None:
        return ["BODY_NORMALIZATION_MAP_MISSING"]
    if row["sha256"] not in store.blobs:
        return ["EVIDENCE_UNAVAILABLE:normalization-specification-map"]
    try:
        rec = store.get_record(row["sha256"])
    except K.AdmissionError:
        return ["BODY_NORMALIZATION_MAP_INVALID"]
    if not KIT.admit(rec, NSL["record"]["bundle"] == "identity" and ID, NSL["record"]["selector"])["ok"]:
        return ["BODY_NORMALIZATION_MAP_INVALID"]
    keys = [lv["level"].encode() for lv in rec["levels"]]
    if any(a >= b for a, b in zip(keys, keys[1:])):
        return ["BODY_NORMALIZATION_MAP_INVALID"]
    mapped = {lv["level"]: lv["specificationDigest"] for lv in rec["levels"]}
    level = payload["normalisationLevel"]
    if level not in mapped:
        return ["BODY_NORMALIZATION_LEVEL_UNMAPPED"]
    if mapped[level] != payload["normalisationVersion"]:
        return ["BODY_NORMALIZATION_LEVEL_VERSION_MISMATCH"]
    if mapped[level] not in {r["sha256"] for r in owner["tree"]}:
        return ["BODY_NORMALIZATION_SPECIFICATION_NOT_IN_CLOSURE"]
    if mapped[level] not in store.blobs:
        return ["EVIDENCE_UNAVAILABLE:level-specification"]
    return []


# ------------------------------------------------------------------ body eligibility
def eligible_suffixes(domain):
    lvb = UNIVERSE_ROWS[domain].get("languageVersionBinding", {})
    be = lvb.get("bodyEligibility")
    if be is None:
        raise K.AdmissionError("BODY_ELIGIBILITY_UNDECLARED", domain)
    if be.get("form") == "dialect-table" and lvb.get("dialect", {}).get("form") == "closed-suffix-table":
        return tuple(lvb["dialect"]["table"])
    if be.get("form") == "closed-suffix-set":
        return tuple(be["suffixes"])
    raise K.AdmissionError("BODY_ELIGIBILITY_FORM", domain)


def body_eligible(domain, path):
    return any(path.endswith(s) for s in eligible_suffixes(domain))


def universe_domain_of_mode(mode):
    return POLICY_UNIVERSE_MAP[MODE_LANGUAGE[mode]]


# ------------------------------------------------------------------ pruned-tree read join
def pruned_read_faults(inventory_rows, cargo_roots, layouts):
    """layouts: the retained ResolvedNodeModulesLayoutV1 of every Plan-selected context that committed nodeModulesInReadSet.
    cargo_roots: every rust unit root and member package root of the retained UnitMembershipV1."""
    listed = [d.split("/") for layout in layouts for e in layout["entries"] for d in (e["installPath"], e["realPath"])]
    faults = []
    for row in inventory_rows:
        segs = row["path"].split("/")
        dirs = segs[:-1]
        if any(s in VCS_SEGMENTS for s in dirs) or any(s == "target" and "/".join(segs[:i]) in cargo_roots for i, s in enumerate(dirs)):
            faults.append(f"SNAPSHOT_PRUNED_TREE_NOT_A_READ:{row['path']}")
            continue
        if "node_modules" not in dirs:
            continue
        if not any(len(segs) > len(d) and segs[:len(d)] == d and "node_modules" not in segs[len(d):-1] for d in listed):
            faults.append(f"SNAPSHOT_PRUNED_TREE_NOT_A_READ:{row['path']}")
    return faults
