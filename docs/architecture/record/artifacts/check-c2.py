#!/usr/bin/env python3
"""Retained executable checker for the C-2 plan/stage contract.

v2 was rejected with two criticals. The two that shaped this checker:

  B-C2V2-01  the admission boundary CONTRADICTED D9. v2 said any failure during
             snapshot capture is pre-admission and never a Run verdict; D9's
             analysis-snapshot-invalidated golden carries admission=admitted,
             a RunId, and class=indeterminate. Two artifacts, incompatible
             identity semantics for one failure. Prose review caught it; nothing
             mechanical could have.
  B-C2V2-02  PS-09 claimed runtime capability denial while the artifact's own
             knownLimitations recorded that no such mechanism is designed — a
             sealed property discharged by an unimplemented test.

So this checker does not only validate C-2 against itself. It reads the LIVE D9
and fact-plane artifacts and fails when the three disagree, and it mechanically
refuses paper seals.

  C1X  the admission-level model agrees with D9's live admission/lifecycle axes
  C2X  Coverage keys agree with the live fact-plane relation registry and ladders
  C3X  implementable test declarations specify properties but never discharge
       them; DISCHARGED/DEMONSTRATED requires retained execution evidence
  C2DL the named v1 full-profile provider oracle uses DELIVERY's exact canonical
       contributionId/providerId namespace
  I1   closed PlanIntent validates every authority-bearing field before attempt
  I2   domain-tagged canonical commitment has exact positive vectors
  I3   AttemptRecord / ExecutionPlan / PlanId-input equality rejects substitution
  P1   every plan fixture validates exactly as its `valid` flag says, AND every
       negative fixture is rejected by the SPECIFIC conformance id it names
  P2   stage kinds are closed; unknown kinds rejected, not ignored
  P3   private operator names never appear in a serialised plan
  P4   forbidden fields per kind are rejected at schema level
  P5   declared relations exist in the fact-plane registry
  C4   coverage fixtures validate exactly as their `valid` flag says

Usage: python3 artifacts/check-c2.py [contract]   ·   --selftest
Exit:  0 clean · 1 findings · 2 IO error
"""
from __future__ import annotations
import copy, hashlib, json, pathlib, re, sys, unicodedata

BINDING = "c2-plan-stage-schema.v3.json"
D9 = "d9-exit-contract.v1.6.json"
FP = "fact-plane.v1.json"
TM = "threat-model.v3.json"
OP = "operability.v2.json"
DELIVERY = "delivery.v2.json"
HERE = pathlib.Path(__file__).resolve().parent

TOTALITY_ROOT_CASES = (
    ("string", "hostile-root"),
    ("null", None),
    ("list", []),
    ("empty-object", {}),
)
MALFORMED_SHAPE_EXCEPTIONS = (
    AttributeError, IndexError, KeyError, StopIteration, TypeError, ValueError,
)


def load(name: str):
    p = HERE / name
    return json.loads(p.read_text()) if p.exists() else None


def _normalise_json(value):
    """The restricted opensip-canonical-json-v1 data model.

    PlanIntent deliberately forbids floats. Python's serializer is used only
    after recursively enforcing that smaller data model and NFC-normalising all
    strings/keys. ensure_ascii=False, sort_keys and compact separators then
    implement the artifact's exact UTF-8 JSON spelling for this domain.
    """
    if value is None or isinstance(value, bool):
        return value
    if isinstance(value, int):
        return value
    if isinstance(value, float):
        raise ValueError("floating-point values are forbidden")
    if isinstance(value, str):
        return unicodedata.normalize("NFC", value)
    if isinstance(value, list):
        return [_normalise_json(x) for x in value]
    if isinstance(value, dict):
        out = {}
        for key, item in value.items():
            if not isinstance(key, str):
                raise ValueError("object key is not a string")
            canonical_key = unicodedata.normalize("NFC", key)
            if canonical_key in out:
                raise ValueError("keys collide after NFC normalisation")
            out[canonical_key] = _normalise_json(item)
        return out
    raise ValueError(f"unsupported JSON value {type(value).__name__}")


def canonical_plan_intent(intent: dict, c: dict) -> bytes:
    spec = c["planIntent"]["canonicalCommitment"]
    if spec.get("domainTagUtf8") != "opensip.plan-intent.v1":
        raise ValueError("unknown PlanIntent commitment domain")
    if spec.get("digest") != "SHA-256" or \
            spec.get("encoding", {}).get("name") != "opensip-canonical-json-v1":
        raise ValueError("unknown PlanIntent commitment algorithm/encoding")
    normal = _normalise_json(intent)
    body = json.dumps(normal, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")
    return spec["domainTagUtf8"].encode("utf-8") + b"\0" + body


def plan_intent_commitment(intent: dict, c: dict) -> str:
    return "sha256:" + hashlib.sha256(canonical_plan_intent(intent, c)).hexdigest()


def _pointer_mutate(value, operation: dict):
    """Apply the tiny set/remove fixture mutation language, returning a copy."""
    out = copy.deepcopy(value)
    parts = [p.replace("~1", "/").replace("~0", "~")
             for p in operation["path"].split("/")[1:]]
    parent = out
    for part in parts[:-1]:
        parent = parent[int(part)] if isinstance(parent, list) else parent[part]
    leaf = parts[-1]
    if operation["op"] == "set":
        if isinstance(parent, list):
            parent[int(leaf)] = copy.deepcopy(operation["value"])
        else:
            parent[leaf] = copy.deepcopy(operation["value"])
    elif operation["op"] == "remove":
        if isinstance(parent, list):
            del parent[int(leaf)]
        else:
            parent.pop(leaf, None)
    else:
        raise ValueError(f"unknown fixture mutation op {operation['op']}")
    return out


IDENTIFIER_RE = re.compile(r"^[a-z][a-z0-9]*(?:[._:-][a-z0-9]+)*$")
SEMVER_RE = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
SHA256_HEX_RE = re.compile(r"^[0-9a-f]{64}$")
SHA256_ID_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
PROJECT_ID_RE = re.compile(r"^prj1-[0-9a-f]{64}$")
RUN_ID_RE = re.compile(r"^run1:[0-9a-f]{64}$")
ARTIFACT_ID_RE = re.compile(
    r"^artifact1:[a-z][a-z0-9]*(?:[._:-][a-z0-9]+)*:sha256:[0-9a-f]{64}$"
)
FACT_VIEW_ID_RE = re.compile(r"^factview1:sha256:[0-9a-f]{64}$")
REQUEST_ID_RE = re.compile(r"^req1_[0-9a-f]{32}$")
BUDGET_KEY_RE = re.compile(
    r"^[a-z][a-z0-9]*(?:[._:-][a-z0-9]+)*\."
    r"(?:work-units|milliseconds|bytes|items)$"
)
INT64_MIN, INT64_MAX = -(2**63), 2**63 - 1


def _exact_object(value, fields: set[str]) -> bool:
    return isinstance(value, dict) and set(value) == fields


def _is_identifier(value, max_bytes: int = 128) -> bool:
    return isinstance(value, str) and len(value.encode("utf-8")) <= max_bytes and \
        IDENTIFIER_RE.fullmatch(value) is not None


def _is_semver(value) -> bool:
    return isinstance(value, str) and len(value.encode("utf-8")) <= 96 and \
        SEMVER_RE.fullmatch(value) is not None


def _is_sorted_unique_strings(value, *, nonempty=False, max_items=None,
                              validator=_is_identifier) -> bool:
    return isinstance(value, list) and (not nonempty or bool(value)) and \
        (max_items is None or len(value) <= max_items) and \
        all(validator(x) for x in value) and value == sorted(value) and \
        len(value) == len(set(value))


def _is_relative_path(value) -> bool:
    if not isinstance(value, str) or value != unicodedata.normalize("NFC", value):
        return False
    if not 1 <= len(value.encode("utf-8")) <= 4096 or value.startswith("/") or \
            "\\" in value or "\0" in value:
        return False
    if re.match(r"^[A-Za-z]:", value):
        return False
    return all(part not in {"", ".", ".."} for part in value.split("/"))


def _bounded_parameter(value, *, depth=0) -> bool:
    if depth > 8:
        return False
    if value is None or isinstance(value, bool):
        return True
    if isinstance(value, int) and not isinstance(value, bool):
        return INT64_MIN <= value <= INT64_MAX
    if isinstance(value, float):
        return False
    if isinstance(value, str):
        return value == unicodedata.normalize("NFC", value) and \
            len(value.encode("utf-8")) <= 4096
    if isinstance(value, list):
        return len(value) <= 256 and \
            all(_bounded_parameter(item, depth=depth + 1) for item in value)
    if isinstance(value, dict):
        if len(value) > 64 or not all(isinstance(key, str) for key in value):
            return False
        return list(value) == sorted(value) and \
            all(_is_identifier(key) and _bounded_parameter(item, depth=depth + 1)
                for key, item in value.items())
    return False


def _bounded_parameter_root(value, *, require_map=False) -> bool:
    if require_map and not isinstance(value, dict):
        return False
    if not _bounded_parameter(value):
        return False
    try:
        size = len(json.dumps(_normalise_json(value), ensure_ascii=False,
                              sort_keys=True, separators=(",", ":")).encode("utf-8"))
    except ValueError:
        return False
    return size <= 65536


def _validate_budget(value, sid: str) -> list[tuple[str, str]]:
    if not _exact_object(value, {"unit", "limit"}):
        return [("PS-01", f"stage '{sid}': budget is not the exact StageBudgetV1 shape")]
    if value["unit"] not in {"work-units", "milliseconds", "bytes", "items"}:
        return [("PS-01", f"stage '{sid}': budget unit is unknown")]
    limit = value["limit"]
    if not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= INT64_MAX:
        return [("PS-01", f"stage '{sid}': budget limit is outside 1..INT64_MAX")]
    return []


def validate_plan(plan: dict, c: dict, relations: set[str],
                  grant_ids: set[str] | None = None) -> list[tuple[str, str]]:
    """Pure logical stage-plan validation with closed value grammar."""
    errs: list[tuple[str, str]] = []
    ss = c["stageSchemas"]
    kinds = set(c["executionPlan"]["stageKinds"])
    private = set(ss["privateOperators"]["names"])
    common = ss["common"]
    stages = plan.get("stages") if isinstance(plan, dict) else None
    if not isinstance(stages, list) or not stages:
        return [("PS-01", "stages must be a non-empty array")]

    stage_ids = [st.get("stageId") if isinstance(st, dict) else None for st in stages]
    if any(not _is_identifier(sid) for sid in stage_ids):
        errs.append(("PS-01", "stageId values must be non-null canonical identifiers"))
    if stage_ids != sorted(stage_ids, key=lambda x: x if isinstance(x, str) else "") or \
            len(stage_ids) != len(set(map(str, stage_ids))):
        errs.append(("PS-01", "stages must be uniquely sorted by stageId"))

    prior: set[str] = set()
    for st in stages:
        if not isinstance(st, dict):
            errs.append(("PS-01", "stage is not an object"))
            continue
        sid = st.get("stageId", "?")
        kind = st.get("kind")
        if kind not in kinds:
            vid = "PS-11" if kind == "snapshot" else "PS-01"
            errs.append((vid, f"stage '{sid}': unknown kind '{kind}' — the kind set is closed"))
            continue
        spec = ss["kinds"][kind]
        for fld in common["required"] + spec["required"]:
            if fld not in st:
                vid = ("PS-10" if fld == "requiredness"
                       else "PS-12b" if kind == "probe" and fld == "capabilityGrants"
                       else "PS-01")
                errs.append((vid, f"stage '{sid}': missing required field '{fld}'"))
        allowed = set(common["required"]) | set(common["optional"]) | \
            set(spec["required"]) | set(spec.get("optional", []))
        for fld in st:
            if fld in private:
                errs.append(("PS-02", f"stage '{sid}': private operator '{fld}' in a serialised plan"))
            elif fld in spec.get("forbidden", []):
                errs.append(("PS-12a", f"stage '{sid}': field '{fld}' is forbidden on kind '{kind}'"))
            elif fld not in allowed:
                errs.append(("PS-01", f"stage '{sid}': field '{fld}' not permitted on kind '{kind}'"))

        depends = st.get("dependsOn", [])
        if "dependsOn" in st and not _is_sorted_unique_strings(depends, nonempty=True):
            errs.append(("PS-01", f"stage '{sid}': dependsOn is not a non-empty sorted identifier set"))
        elif any(dep not in prior for dep in depends):
            errs.append(("PS-01", f"stage '{sid}': dependsOn names self, forward or unknown stage"))
        if "budget" in st:
            errs.extend(_validate_budget(st["budget"], str(sid)))

        if kind == "fact-derivation":
            rels = st.get("relations")
            if not _is_sorted_unique_strings(rels, nonempty=True):
                errs.append(("PS-01", f"stage '{sid}': relations is not a non-empty sorted identifier set"))
            else:
                for rel in rels:
                    if rel not in relations:
                        errs.append(("C2X", f"stage '{sid}': relation '{rel}' is not in the fact-plane registry"))
            operator = st.get("operator")
            if operator not in spec["operatorAuthority"]:
                errs.append(("PS-01", f"stage '{sid}': operator '{operator}' is not a declared authority"))
            provider = st.get("providerId")
            if operator in {"semantic-provider", "external-scanner"} and not _is_identifier(provider):
                errs.append(("PS-01", f"stage '{sid}': {operator} requires canonical providerId"))
            if operator == "builtin-extractor" and "providerId" in st:
                errs.append(("PS-01", f"stage '{sid}': builtin-extractor forbids providerId"))
        elif kind == "rule-evaluation":
            if not _is_sorted_unique_strings(st.get("ruleIds"), nonempty=True):
                errs.append(("PS-10", f"stage '{sid}': ruleIds is not a non-empty sorted identifier set"))
            if st.get("requiredness") not in {"required", "optional"}:
                errs.append(("PS-10", f"stage '{sid}': requiredness must be required or optional"))
        elif kind == "policy-evaluation":
            if not _is_identifier(st.get("policyId")):
                errs.append(("PS-01", f"stage '{sid}': policyId is not a canonical identifier"))
        elif kind == "probe" and not _is_identifier(st.get("probeId")):
            errs.append(("PS-01", f"stage '{sid}': probeId is not a canonical identifier"))

        if "capabilityGrants" in st:
            refs = st["capabilityGrants"]
            if not _is_sorted_unique_strings(refs, nonempty=True):
                errs.append(("PS-12b" if kind == "probe" else "PS-01",
                             f"stage '{sid}': capabilityGrants is not a non-empty sorted identifier set"))
            elif grant_ids is not None and any(ref not in grant_ids for ref in refs):
                errs.append(("PS-01", f"stage '{sid}': capabilityGrants names an unadmitted grantId"))
        if isinstance(sid, str):
            prior.add(sid)
    return errs


def _validate_admission_descriptor(value, c: dict,
                                   relations: set[str]) -> list[tuple[str, str]]:
    errs: list[tuple[str, str]] = []
    spec = c["planIntent"]["admissionDescriptorV1"]
    required = set(spec["required"])
    if not _exact_object(value, required):
        return [("C2I-01", "admissionDescriptor is not the exact closed AdmissionDescriptorV1 shape")]
    if value["schemaVersion"] != 1:
        errs.append(("C2I-02", "AdmissionDescriptor schemaVersion must be 1"))

    release = value["release"]
    if not _exact_object(release, {"manifestId", "capabilityManifestId", "profileId"}):
        errs.append(("C2I-01", "release is not the exact closed shape"))
    elif not SHA256_HEX_RE.fullmatch(str(release["manifestId"])) or \
            not SHA256_HEX_RE.fullmatch(str(release["capabilityManifestId"])) or \
            not _is_identifier(release["profileId"]):
        errs.append(("C2I-02", "release contains a malformed manifest/profile identifier"))
    if value["invocationProfile"] not in spec["invocationProfile"]:
        errs.append(("C2I-02", "invocationProfile is not declared"))

    config = value["resolvedConfiguration"]
    config_paths = []
    if not isinstance(config, list):
        errs.append(("C2I-01", "resolvedConfiguration is not an array"))
        config = []
    for index, entry in enumerate(config):
        fields = {"path", "value", "decidingLayer", "analysisAffecting"}
        if not _exact_object(entry, fields):
            errs.append(("C2I-01", f"resolvedConfiguration[{index}] is not the exact closed shape"))
            continue
        path = entry["path"]
        if not _is_identifier(path, 256):
            errs.append(("C2I-02", f"resolvedConfiguration[{index}].path is malformed"))
        if isinstance(path, str):
            config_paths.append(path)
        layer = entry["decidingLayer"]
        if not isinstance(layer, int) or isinstance(layer, bool) or not 1 <= layer <= 6:
            errs.append(("C2I-02", f"resolvedConfiguration[{index}].decidingLayer is outside 1..6"))
        if entry["analysisAffecting"] is not True or not _bounded_parameter_root(entry["value"]):
            errs.append(("C2I-02", f"resolvedConfiguration[{index}] value/analysisAffecting is invalid"))
    if config_paths != sorted(config_paths) or len(config_paths) != len(set(config_paths)):
        errs.append(("C2I-02", "resolvedConfiguration is not uniquely sorted by path"))

    scope = value["scope"]
    if not _exact_object(scope, {"projectId", "workspaceUnitIds", "requestedPaths", "impactExpansion"}):
        errs.append(("C2I-01", "scope is not the exact closed shape"))
        project_id = None
    else:
        project_id = scope["projectId"]
        if not isinstance(project_id, str) or not PROJECT_ID_RE.fullmatch(project_id):
            errs.append(("C2I-02", "scope.projectId is not PROJECT-ID-V1 text"))
        if not _is_sorted_unique_strings(scope["workspaceUnitIds"], nonempty=True, max_items=4096):
            errs.append(("C2I-02", "workspaceUnitIds is not a non-empty sorted identifier set"))
        if not _is_sorted_unique_strings(scope["requestedPaths"], max_items=100000,
                                         validator=_is_relative_path):
            errs.append(("C2I-02", "requestedPaths is not a sorted canonical-relative-path set"))
        if scope["impactExpansion"] not in spec["scope"]["impactExpansion"]:
            errs.append(("C2I-02", "scope.impactExpansion is not declared"))

    change = value["changeSpec"]
    change_fields = {"mode", "baseCommitId", "dirtyOverlayPolicy", "untrackedPolicy", "vcsAdapterId"}
    if not _exact_object(change, change_fields):
        errs.append(("C2I-01", "changeSpec is not the exact closed shape"))
    else:
        if change["mode"] not in spec["changeSpec"]["mode"] or \
                change["dirtyOverlayPolicy"] not in spec["changeSpec"]["dirtyOverlayPolicy"] or \
                change["untrackedPolicy"] not in spec["changeSpec"]["untrackedPolicy"]:
            errs.append(("C2I-02", "changeSpec contains an undeclared enum value"))
        base = change["baseCommitId"]
        if base is not None and (not isinstance(base, str) or not SHA256_HEX_RE.fullmatch(base)):
            errs.append(("C2I-02", "changeSpec.baseCommitId is neither null nor sha256Hex"))
        if not _is_identifier(change["vcsAdapterId"]):
            errs.append(("C2I-02", "changeSpec.vcsAdapterId is malformed"))

    contributions = value["contributions"]
    activation_ids, contribution_authorities = [], set()
    contribution_fields = set(spec["contribution"]["required"])
    if not isinstance(contributions, list):
        errs.append(("C2I-01", "contributions is not an array"))
        contributions = []
    for index, item in enumerate(contributions):
        if not _exact_object(item, contribution_fields):
            errs.append(("C2I-01", f"contribution {index} is not the exact closed shape"))
            continue
        if isinstance(item["activationId"], str):
            activation_ids.append(item["activationId"])
        for field in ("activationId", "contributionId", "bundleId"):
            if not _is_identifier(item[field]):
                errs.append(("C2I-02", f"contribution {index}.{field} is malformed"))
        if not _is_semver(item["contributionVersion"]) or \
                not SHA256_HEX_RE.fullmatch(str(item["artifactDigest"])):
            errs.append(("C2I-02", f"contribution {index} version/digest is malformed"))
        if item["admissionGrant"] not in spec["contribution"]["admissionGrant"] or \
                item["role"] not in spec["contribution"]["role"] or \
                item["verificationState"] not in spec["contribution"]["verificationState"] or \
                item["origin"] not in spec["contribution"]["origin"] or \
                item["authority"] not in spec["contribution"]["authority"]:
            errs.append(("C2I-02", f"contribution {index} contains an undeclared enum value"))
        evidence = item["verificationEvidenceId"]
        if item["verificationState"] == "VERIFIED":
            if not _is_identifier(evidence):
                errs.append(("C2I-02", f"contribution {index} VERIFIED requires verificationEvidenceId"))
        elif evidence is not None:
            errs.append(("C2I-02", f"contribution {index} non-VERIFIED forbids verificationEvidenceId"))
        if not _bounded_parameter_root(item["parameters"], require_map=True):
            errs.append(("C2I-02", f"contribution {index}.parameters violates boundedParameterValue"))
        if isinstance(item["contributionId"], str) and isinstance(item["authority"], str):
            contribution_authorities.add((item["contributionId"], item["authority"]))
    if activation_ids != sorted(activation_ids) or len(activation_ids) != len(set(activation_ids)):
        errs.append(("C2I-02", "contributions are not uniquely sorted by activationId"))

    grants = value["capabilityGrants"]
    grant_fields = set(spec["capabilityGrant"]["required"])
    grant_tuples, grant_ids = [], set()
    if not isinstance(grants, list):
        errs.append(("C2I-01", "capabilityGrants is not an array"))
        grants = []
    for index, item in enumerate(grants):
        if not _exact_object(item, grant_fields):
            errs.append(("C2I-01", f"capabilityGrant {index} is not the exact closed shape"))
            continue
        if not _is_identifier(item["grantId"]) or not _is_semver(item["grantVersion"]) or \
                not isinstance(item["projectId"], str) or not PROJECT_ID_RE.fullmatch(item["projectId"]):
            errs.append(("C2I-02", f"capabilityGrant {index} identifier/version/project is malformed"))
        if item["projectId"] != project_id:
            errs.append(("C2I-02", f"capabilityGrant {index} crosses descriptor projectId"))
        if item["capability"] not in spec["capabilityGrant"]["capability"] or \
                not _bounded_parameter_root(item["parameters"], require_map=True):
            errs.append(("C2I-02", f"capabilityGrant {index} capability/parameters is invalid"))
        if all(isinstance(item[field], str)
               for field in ("grantId", "grantVersion", "projectId")):
            grant_tuples.append((item["grantId"], item["grantVersion"], item["projectId"]))
        if isinstance(item["grantId"], str):
            grant_ids.add(item["grantId"])
    if grant_tuples != sorted(grant_tuples) or len(grant_tuples) != len(set(grant_tuples)) or \
            len(grant_ids) != len(grant_tuples):
        errs.append(("C2I-02", "capabilityGrants are not uniquely sorted by grant tuple/id"))

    workflow = value["workflow"]
    if not _exact_object(workflow, {"stages"}):
        errs.append(("C2I-01", "workflow is not the exact closed shape"))
    else:
        for _, message in validate_plan(workflow, c, relations, grant_ids):
            errs.append(("C2I-03", message))
        for stage in workflow.get("stages", []):
            if not isinstance(stage, dict):
                continue
            operator = stage.get("operator")
            provider = stage.get("providerId")
            if operator in {"semantic-provider", "external-scanner"} and \
                    (not isinstance(provider, str) or
                     (provider, operator) not in contribution_authorities):
                errs.append(("C2I-03", f"stage {stage.get('stageId')} has no matching admitted contribution"))

    budgets = value["budgets"]
    if not isinstance(budgets, dict) or len(budgets) > 64:
        errs.append(("C2I-01", "budgets is not a closed map with at most 64 entries"))
    else:
        for key, limit in budgets.items():
            if not isinstance(key, str) or not BUDGET_KEY_RE.fullmatch(key) or \
                    not isinstance(limit, int) or isinstance(limit, bool) or not 1 <= limit <= INT64_MAX:
                errs.append(("C2I-02", f"budget {key!r} has malformed unit-bearing key or limit"))
    return errs


def _validate_stored_view(value, c: dict) -> list[tuple[str, str]]:
    errs: list[tuple[str, str]] = []
    spec = c["planIntent"]["storedViewIntentV1"]
    if not _exact_object(value, set(spec["required"])):
        return [("C2I-07", "storedView is not the exact closed StoredViewIntentV1 shape")]
    if not isinstance(value["projectId"], str) or not PROJECT_ID_RE.fullmatch(value["projectId"]):
        errs.append(("C2I-07", "storedView.projectId is not PROJECT-ID-V1 text"))
    target = value["target"]
    if not _exact_object(target, {"kind", "runId", "sealedManifestDigest"}):
        errs.append(("C2I-07", "storedView.target is not the exact closed shape"))
    elif target["kind"] != "sealed-run" or \
            not isinstance(target["runId"], str) or not RUN_ID_RE.fullmatch(target["runId"]) or \
            not isinstance(target["sealedManifestDigest"], str) or \
            not SHA256_ID_RE.fullmatch(target["sealedManifestDigest"]):
        errs.append(("C2I-07", "storedView.target contains a malformed kind/RunId/manifest digest"))
    query = value["query"]
    union = spec["query"]["closedTaggedUnion"]
    operation = query.get("operation") if isinstance(query, dict) else None
    branch = union.get(operation)
    if branch is None or not _exact_object(query, set(branch["exactFields"])):
        errs.append(("C2I-07", "storedView.query is not one exact declared tagged-union branch"))
    elif operation == "read-artifact" and \
            (not isinstance(query["artifactId"], str) or not ARTIFACT_ID_RE.fullmatch(query["artifactId"])):
        errs.append(("C2I-07", "storedView.query artifactId is malformed"))
    elif operation == "read-fact-view" and \
            (not isinstance(query["factViewId"], str) or not FACT_VIEW_ID_RE.fullmatch(query["factViewId"])):
        errs.append(("C2I-07", "storedView.query factViewId is malformed"))
    allowed_results = spec["resultSelectorByOperation"].get(operation, [])
    if value["resultSelector"] not in allowed_results:
        errs.append(("C2I-07", "storedView.resultSelector is incompatible with query.operation"))
    retention = value["retentionSelector"]
    if not _exact_object(retention, {"requiredState", "onUnavailable"}) or \
            retention.get("requiredState") not in spec["retentionSelector"]["requiredState"] or \
            retention.get("onUnavailable") != spec["retentionSelector"]["onUnavailable"]:
        errs.append(("C2I-07", "storedView.retentionSelector is not the exact declared selector"))
    return errs


def _validate_plan_intent(intent: object, c: dict,
                          relations: set[str]) -> list[tuple[str, str]]:
    errs: list[tuple[str, str]] = []
    intent_spec = c.get("planIntent", {})
    schema = intent_spec.get("schema", {})
    if schema.get("closed") is not True or schema.get("required") != ["schemaVersion", "intentKind"] or \
            set(schema.get("taggedUnion", {})) != {"analysis", "stored-view"}:
        errs.append(("C2I-01", "PlanIntent binding is not the declared closed tagged union"))
    if not isinstance(intent, dict):
        return errs + [("C2I-01", "PlanIntent is not an object")]
    kind = intent.get("intentKind")
    branch = schema.get("taggedUnion", {}).get(kind)
    if branch is None:
        return errs + [("C2I-02", "PlanIntent intentKind is not declared")]
    expected = set(branch["exactTopLevelFields"])
    if set(intent) != expected:
        errs.append(("C2I-01", f"PlanIntent {kind} branch is not exact; fields={sorted(intent)}"))
    if intent.get("schemaVersion") != 1:
        errs.append(("C2I-02", "PlanIntent schemaVersion must be 1"))
    if kind == "stored-view":
        return errs + _validate_stored_view(intent.get("storedView"), c)

    analysis = intent.get("analysis")
    analysis_spec = intent_spec["analysisIntentV1"]
    if not _exact_object(analysis, set(analysis_spec["required"])):
        return errs + [("C2I-01", "analysis is not the exact closed AnalysisIntentV1 shape")]
    for field in ("executionTopology", "workflowIntent", "networkIntent", "remoteComputation"):
        if analysis[field] not in analysis_spec[field]:
            errs.append(("C2I-02", f"analysis.{field} has undeclared value {analysis[field]!r}"))
    repo = analysis["repositoryExecution"]
    repo_spec = analysis_spec["repositoryExecution"]
    if not _exact_object(repo, set(repo_spec["required"])):
        errs.append(("C2I-01", "repositoryExecution is not the exact closed shape"))
    else:
        for field in repo_spec["required"]:
            if repo[field] not in repo_spec["values"]:
                errs.append(("C2I-02", f"repositoryExecution.{field} has undeclared value"))
    errs.extend(_validate_admission_descriptor(analysis["admissionDescriptor"], c, relations))
    return errs


def validate_plan_intent(intent: object, c: dict,
                         relations: set[str]) -> list[tuple[str, str]]:
    """Total parsed-JSON validator: malformed input is data, never an exception.

    The explicit guards in the validators produce the precise C2I-* findings.
    This final boundary converts any missed wrong-type traversal into the same
    deterministic pre-attempt rejection instead of leaking a Python/host fault.
    """
    try:
        return _validate_plan_intent(intent, c, relations)
    except (TypeError, KeyError, IndexError, AttributeError, ValueError) as exc:
        return [("C2I-02", f"malformed parsed JSON rejected at validation boundary: {type(exc).__name__}")]

def validate_coverage(entry: dict, c: dict, fp: dict | None) -> list[str]:
    """Pure Coverage entry -> violations, checked against the live fact-plane."""
    errs: list[str] = []
    key = {f["field"]: f for f in c["coverageKey"]["key"]}
    for fld in key:
        if fld == "targetUniverseId":
            continue
        if fld not in entry:
            errs.append(f"C2X: Coverage entry missing '{fld}'")
    rel = entry.get("relation")
    if fp and rel:
        rels = fp["relationRegistry"]["relations"]
        if rel not in rels:
            errs.append(f"C2X: relation '{rel}' is not in the fact-plane registry")
        elif entry.get("resolution") not in rels[rel]["ladder"]:
            errs.append(f"C2X: resolution '{entry.get('resolution')}' is not a rung of "
                        f"'{rel}' — ladders are per-relation")
    if rel in c["coverageKey"]["crossUniverseRelations"] and "targetUniverseId" not in entry:
        errs.append(f"C2X: cross-universe relation '{rel}' has no targetUniverseId — "
                    f"source-complete would masquerade as target-complete")
    return errs


def _intent_fixture_values(c: dict) -> tuple[dict[str, dict], list[str]]:
    """Expand concrete/base+mutation PlanIntent fixtures."""
    values: dict[str, dict] = {}
    findings: list[str] = []
    for fx in c.get("planIntentFixtures", []):
        if "intent" in fx:
            values[fx["id"]] = copy.deepcopy(fx["intent"])
            continue
        base_id = fx.get("baseFixtureId")
        if base_id not in values:
            findings.append(f"I1 {fx.get('id')}: base fixture {base_id!r} is unavailable or forward-referenced")
            continue
        try:
            values[fx["id"]] = _pointer_mutate(values[base_id], fx["mutation"])
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            findings.append(f"I1 {fx.get('id')}: fixture mutation failed: {exc}")
    return values, findings


def _analysis_descriptor(intent: dict) -> dict:
    return intent["analysis"]["admissionDescriptor"]


def _stored_payload(intent: dict) -> dict:
    return intent["storedView"]


def _replace_binding_sentinels(value, intent: dict, commitment: str):
    descriptor = _analysis_descriptor(intent) if intent.get("intentKind") == "analysis" else None
    stored = _stored_payload(intent) if intent.get("intentKind") == "stored-view" else None
    sentinels = {
        "$BASE_COMMITMENT": commitment,
        "$BASE_INTENT": intent,
        "$BASE_ADMISSION_DESCRIPTOR": descriptor,
        "$BASE_PROJECT_ID": descriptor["scope"]["projectId"] if descriptor else stored["projectId"],
        "$BASE_RELEASE": descriptor["release"] if descriptor else None,
        "$BASE_INVOCATION_PROFILE": descriptor["invocationProfile"] if descriptor else None,
        "$BASE_RESOLVED_CONFIGURATION": descriptor["resolvedConfiguration"] if descriptor else None,
        "$BASE_SCOPE": descriptor["scope"] if descriptor else None,
        "$BASE_CHANGE_SPEC": descriptor["changeSpec"] if descriptor else None,
        "$BASE_CONTRIBUTIONS": descriptor["contributions"] if descriptor else None,
        "$BASE_CAPABILITY_GRANTS": descriptor["capabilityGrants"] if descriptor else None,
        "$BASE_WORKFLOW": descriptor["workflow"] if descriptor else None,
        "$BASE_BUDGETS": descriptor["budgets"] if descriptor else None,
        "$BASE_STAGE_INTENTS": descriptor["workflow"]["stages"] if descriptor else None,
        "$BASE_STORED_TARGET": stored["target"] if stored else None,
        "$BASE_STORED_QUERY": stored["query"] if stored else None,
        "$BASE_RESULT_SELECTOR": stored["resultSelector"] if stored else None,
        "$BASE_RETENTION_SELECTOR": stored["retentionSelector"] if stored else None,
    }
    if isinstance(value, str) and value in sentinels:
        return copy.deepcopy(sentinels[value])
    if isinstance(value, list):
        return [_replace_binding_sentinels(x, intent, commitment) for x in value]
    if isinstance(value, dict):
        return {k: _replace_binding_sentinels(v, intent, commitment)
                for k, v in value.items()}
    return value


def _default_attempt(intent: dict, commitment: str) -> dict:
    descriptor = _analysis_descriptor(intent)
    return {
        "executionId": "exec-1",
        "admittedPlanIntent": copy.deepcopy(intent),
        "admissionDescriptor": copy.deepcopy(descriptor),
        "planIntentCommitment": commitment,
    }


def _default_execution_plan(intent: dict, commitment: str) -> dict:
    descriptor = _analysis_descriptor(intent)
    inputs = {
        "snapshotId": "snap-1",
        "planSchemaMajor": 1,
        "release": copy.deepcopy(descriptor["release"]),
        "invocationProfile": descriptor["invocationProfile"],
        "resolvedConfiguration": copy.deepcopy(descriptor["resolvedConfiguration"]),
        "scope": copy.deepcopy(descriptor["scope"]),
        "changeSpec": copy.deepcopy(descriptor["changeSpec"]),
        "contributions": copy.deepcopy(descriptor["contributions"]),
        "semanticUniverses": [],
        "capabilityGrants": copy.deepcopy(descriptor["capabilityGrants"]),
        "workflow": copy.deepcopy(descriptor["workflow"]),
        "budgets": copy.deepcopy(descriptor["budgets"]),
        "planIntentCommitment": commitment,
    }
    return {
        "snapshotId": "snap-1",
        "planId": "plan-1",
        "projectId": descriptor["scope"]["projectId"],
        "planIntentCommitment": commitment,
        "planIdentityInputs": inputs,
        "stages": copy.deepcopy(descriptor["workflow"]["stages"]),
    }


def validate_intent_binding(fx: dict, base_intent: dict, c: dict,
                            relations: set[str]) -> list[tuple[str, str]]:
    if base_intent.get("intentKind") != "analysis":
        return [("C2I-06", "analysis binding fixture does not use an analysis PlanIntent")]
    commitment = plan_intent_commitment(base_intent, c)
    attempt = _replace_binding_sentinels(
        copy.deepcopy(fx.get("attemptRecord", _default_attempt(base_intent, commitment))),
        base_intent, commitment)
    plan = _replace_binding_sentinels(
        copy.deepcopy(fx.get("executionPlan", _default_execution_plan(base_intent, commitment))),
        base_intent, commitment)
    candidate_intent = copy.deepcopy(base_intent)
    try:
        if fx.get("candidateIntentMutation"):
            candidate_intent = _pointer_mutate(candidate_intent, fx["candidateIntentMutation"])
        if fx.get("attemptRecordMutation"):
            attempt = _pointer_mutate(attempt, fx["attemptRecordMutation"])
        if fx.get("executionPlanMutation"):
            plan = _pointer_mutate(plan, fx["executionPlanMutation"])
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        return [("C2I-06", f"binding fixture mutation failed: {exc}")]

    errs: list[tuple[str, str]] = []
    attempt_required = set(c["planIntent"]["attemptAndExecutionJoin"]["attemptRecordRequired"])
    if not isinstance(attempt, dict) or set(attempt) != attempt_required:
        if not isinstance(attempt, dict) or "planIntentCommitment" not in attempt:
            errs.append(("C2I-05", "AttemptRecord lacks planIntentCommitment"))
        errs.append(("C2I-06", "AttemptRecord is not the exact closed intent-bound envelope"))
    required_plan = set(c["executionPlan"].get("requiredFields", []))
    if not isinstance(plan, dict) or c["executionPlan"].get("closedTopLevel") is not True or \
            set(plan) != required_plan:
        return errs + [("C2I-06", "ExecutionPlan is not the exact closed intent-bound envelope")]

    descriptor = _analysis_descriptor(base_intent)
    candidate_commitment = plan_intent_commitment(candidate_intent, c)
    inputs = plan.get("planIdentityInputs")
    inputs_required = set(c["planIntent"]["attemptAndExecutionJoin"]["planIdentityInputsRequired"])
    if not isinstance(inputs, dict) or set(inputs) != inputs_required:
        errs.append(("C2I-06", "planIdentityInputs is not the exact 13-field PlanDescriptor"))
        inputs = {}

    commitment_values = [
        attempt.get("planIntentCommitment") if isinstance(attempt, dict) else None,
        plan.get("planIntentCommitment"),
        inputs.get("planIntentCommitment"),
    ]
    if any(value != commitment for value in commitment_values) or candidate_commitment != commitment:
        errs.append(("C2I-06", "PlanIntent commitment differs across candidate, AttemptRecord, ExecutionPlan or PlanId input"))
    if not isinstance(attempt, dict) or attempt.get("admittedPlanIntent") != base_intent:
        errs.append(("C2I-06", "AttemptRecord.admittedPlanIntent differs from frozen admitted PlanIntent"))
    if not isinstance(attempt, dict) or attempt.get("admissionDescriptor") != descriptor:
        errs.append(("C2I-06", "AttemptRecord.admissionDescriptor differs from admitted subobject"))

    mapping = {
        "release": "release",
        "invocationProfile": "invocationProfile",
        "resolvedConfiguration": "resolvedConfiguration",
        "scope": "scope",
        "changeSpec": "changeSpec",
        "contributions": "contributions",
        "capabilityGrants": "capabilityGrants",
        "workflow": "workflow",
        "budgets": "budgets",
    }
    for plan_field, descriptor_field in mapping.items():
        if inputs.get(plan_field) != descriptor[descriptor_field]:
            errs.append(("C2I-06", f"planIdentityInputs.{plan_field} differs from admitted descriptor"))
    if inputs.get("snapshotId") != plan.get("snapshotId") or \
            inputs.get("planSchemaMajor") != 1 or not isinstance(inputs.get("semanticUniverses"), list):
        errs.append(("C2I-06", "post-admission PlanDescriptor fields are malformed or inconsistent"))
    if plan.get("projectId") != descriptor["scope"]["projectId"]:
        errs.append(("C2I-06", "ExecutionPlan.projectId differs from admitted scope.projectId"))
    if plan.get("stages") != descriptor["workflow"]["stages"]:
        errs.append(("C2I-06", "ExecutionPlan.stages differs from admitted workflow.stages"))
    grant_ids = {grant["grantId"] for grant in descriptor["capabilityGrants"]}
    for _, message in validate_plan({"stages": plan.get("stages")}, c, relations, grant_ids):
        errs.append(("C2I-03", message))
    return errs


def _default_stored_binding(intent: dict, commitment: str) -> tuple[dict, dict]:
    stored = _stored_payload(intent)
    request_id = "req1_00000000000000000000000000000001"
    request = {
        "requestId": request_id,
        "admittedPlanIntent": copy.deepcopy(intent),
        "planIntentCommitment": commitment,
    }
    prepared = {
        "requestId": request_id,
        "planIntentCommitment": commitment,
        "projectId": stored["projectId"],
        "target": copy.deepcopy(stored["target"]),
        "query": copy.deepcopy(stored["query"]),
        "resultSelector": stored["resultSelector"],
        "retentionSelector": copy.deepcopy(stored["retentionSelector"]),
    }
    return request, prepared


def validate_stored_view_binding(fx: dict, base_intent: dict,
                                 c: dict) -> list[tuple[str, str]]:
    if base_intent.get("intentKind") != "stored-view":
        return [("C2I-08", "stored binding fixture does not use a stored-view PlanIntent")]
    commitment = plan_intent_commitment(base_intent, c)
    default_request, default_prepared = _default_stored_binding(base_intent, commitment)
    request = _replace_binding_sentinels(
        copy.deepcopy(fx.get("requestContext", default_request)), base_intent, commitment)
    prepared = _replace_binding_sentinels(
        copy.deepcopy(fx.get("preparedStoredRead", default_prepared)), base_intent, commitment)
    try:
        if fx.get("requestContextMutation"):
            request = _pointer_mutate(request, fx["requestContextMutation"])
        if fx.get("preparedStoredReadMutation"):
            prepared = _pointer_mutate(prepared, fx["preparedStoredReadMutation"])
    except (KeyError, IndexError, TypeError, ValueError) as exc:
        return [("C2I-08", f"stored binding fixture mutation failed: {exc}")]

    errs: list[tuple[str, str]] = []
    request_fields = set(c["planIntent"]["storedViewJoin"]["requestContextRequired"])
    prepared_fields = set(c["planIntent"]["storedViewJoin"]["preparedStoredReadRequired"])
    if not _exact_object(request, request_fields):
        errs.append(("C2I-08", "RequestContext is not the exact closed stored-read envelope"))
    if not _exact_object(prepared, prepared_fields):
        errs.append(("C2I-08", "PreparedStoredRead is not the exact closed stored-read envelope"))
    request_id = request.get("requestId") if isinstance(request, dict) else None
    prepared_request_id = prepared.get("requestId") if isinstance(prepared, dict) else None
    if not isinstance(request_id, str) or not REQUEST_ID_RE.fullmatch(request_id) or \
            not isinstance(prepared_request_id, str) or \
            not REQUEST_ID_RE.fullmatch(prepared_request_id):
        errs.append(("C2I-09", "stored-read envelopes require canonical REQUEST-ID-V1 text"))
    if fx.get("requestIdAuthority", "host-minted-reserved") != "host-minted-reserved":
        errs.append(("C2I-09", "stored-read RequestId was not host-minted and reserved at ingress"))
    stored = _stored_payload(base_intent)
    if not isinstance(request, dict) or request.get("admittedPlanIntent") != base_intent or \
            request.get("planIntentCommitment") != commitment:
        errs.append(("C2I-08", "RequestContext differs from frozen stored-view intent/commitment"))
    if not isinstance(prepared, dict) or prepared_request_id != request_id or \
            prepared.get("planIntentCommitment") != commitment:
        errs.append(("C2I-08", "PreparedStoredRead request/commitment differs from RequestContext"))
    for field in ("projectId", "target", "query", "resultSelector", "retentionSelector"):
        if not isinstance(prepared, dict) or prepared.get(field) != stored[field]:
            errs.append(("C2I-08", f"PreparedStoredRead.{field} differs from admitted stored-view request"))
    return errs

def _check(c: dict, d9: dict | None, fp: dict | None, tm: dict | None = None,
           operability: dict | None = None,
           delivery: dict | None = None) -> list[str]:
    f: list[str] = []
    relations = set(fp["relationRegistry"]["relations"]) if fp else set()
    if fp is None:
        f.append(f"C2X: could not load {FP} — relation constraints unverified")
    if d9 is None:
        f.append(f"C1X: could not load {D9} — the admission boundary is unverified")

    # ---- C1X: the admission model must agree with the LIVE D9 axes ----
    if d9:
        goldens = d9["goldenCases"]
        levels = {lv["level"]: lv for lv in c["theAdmissionBoundary"]["levels"]}

        # every level's declared D9 correspondence must actually occur in D9
        for name, lv in levels.items():
            corr = lv.get("d9Correspondence", "")
            pairs = [p.strip() for p in corr.split(",") if "=" in p]
            want = dict(p.split("=", 1) for p in pairs)
            if want and not any(all(g["scenarioAxes"].get(k) == v for k, v in want.items())
                                for g in goldens):
                f.append(f"C1X: level '{name}' declares D9 correspondence '{corr}' but no "
                         f"D9 golden matches it")

        # the specific contradiction B-C2V2-01 named
        snap = [g for g in goldens
                if g["scenarioAxes"].get("deficiency") == "convergence-exhausted"]
        if not snap:
            f.append("C1X: D9 has no convergence-exhausted golden — the snapshot boundary "
                     "claim cannot be cross-checked")
        for g in snap:
            ax = g["scenarioAxes"]
            if ax["admission"] != "admitted":
                f.append(f"C1X: D9 golden '{g['id']}' treats snapshot exhaustion as "
                         f"admission={ax['admission']}, but C-2 places snapshot-binding "
                         f"AFTER admission (B-C2V2-01)")
            if ax["lifecycle"] != "coherent-terminal-run":
                f.append(f"C1X: D9 golden '{g['id']}' has lifecycle={ax['lifecycle']}; C-2 "
                         f"claims snapshot exhaustion seals a coherent terminal Run")
        sb = levels.get("snapshot-binding", {})
        if "POST-ADMISSION" not in sb.get("onFailure", "").upper():
            f.append("C1X: snapshot-binding does not declare post-admission failure semantics")
        if "ExecutionId" not in levels.get("attempt-admission", {}).get("allocates", []):
            f.append("C1X: ExecutionId is not allocated at attempt-admission — a crash "
                     "before snapshot work could not name the orphan (EC-6)")

    # ---- I1..I4: pre-admission requests and immutable joins ----
    intent_spec = c.get("planIntent", {})
    lifecycle = intent_spec.get("lifecycle", {})
    if "No ExecutionId" not in lifecycle.get("onInvalidOrExcluded", "") or \
            "AttemptRecord" not in lifecycle.get("onInvalidOrExcluded", ""):
        f.append("I1: invalid/excluded PlanIntent does not bind zero attempt allocation")
    if tm is None:
        f.append(f"C2I-TM: could not load {TM} — ProjectId path encoding join unverified")
    else:
        c2_pattern = intent_spec.get("wireTypes", {}).get("projectId", {}).get("pattern")
        tm_pattern = tm.get("storageNamespace", {}).get("projectId", {}).get("canonicalTextPattern")
        if c2_pattern != tm_pattern:
            f.append("C2I-TM: PlanIntent and storage namespace disagree on ProjectId encoding")
    request_join = intent_spec.get("storedViewJoin", {}).get("requestIdContract", {})
    if operability is None:
        f.append(f"C2I-OP: could not load {OP} — stored-read REQUEST-ID-V1 join unverified")
    else:
        live_request = operability.get("requestIdContract", {})
        live_pattern = live_request.get("representation", {}).get("regex")
        if request_join.get("id") != "REQUEST-ID-V1" or \
                request_join.get("source") != "operability.v2.json#requestIdContract" or \
                request_join.get("pattern") != live_pattern or \
                live_pattern != r"^req1_[0-9a-f]{32}$":
            f.append("C2I-OP: stored-view envelopes drift from live REQUEST-ID-V1")
        owner_blob = json.dumps(request_join)
        live_owner_blob = json.dumps(live_request.get("authority", {}))
        if "host-minted-reserved" not in owner_blob or \
                "MUST NOT supply requestId" not in live_owner_blob:
            f.append("C2I-OP: stored-view RequestId ownership/caller exclusion is incomplete")

    intent_values, fixture_findings = _intent_fixture_values(c)
    f.extend(fixture_findings)

    # The generic C-2 grammar deliberately permits future provider identifiers,
    # but this named fixture is the shipping v1 full-profile oracle consumed by
    # RI and DELIVERY. Its two identifier surfaces must therefore join the live
    # DELIVERY allow-list exactly; a coordinated provider.* rename is not merely
    # a valid new commitment, it is a different and non-v1 plan.
    full_profile = next((fx for fx in c.get("planIntentFixtures", [])
                         if fx.get("id") == "valid-full-profile-semantic-providers"), None)
    canonical_provider_ids = {"rust-semantic", "typescript-semantic"}
    if full_profile is None or full_profile.get("productScope") != "V1 FULL PROFILE" or \
            full_profile.get("id") not in intent_values:
        f.append("C2DL: named V1 FULL PROFILE PlanIntent oracle is absent")
    elif delivery is None:
        f.append(f"C2DL: could not load {DELIVERY} — v1 provider namespace join unverified")
    else:
        descriptor = _analysis_descriptor(intent_values[full_profile["id"]])
        contribution_ids = {
            item.get("contributionId") for item in descriptor.get("contributions", [])
            if isinstance(item, dict) and item.get("authority") == "semantic-provider"
        }
        provider_ids = {
            stage.get("providerId") for stage in descriptor.get("workflow", {}).get("stages", [])
            if isinstance(stage, dict) and stage.get("operator") == "semantic-provider"
        }
        conditions = delivery.get("initialProductScope", {}).get(
            "v1PlanIntentOverlay", {}).get("conditions", {})
        delivery_contribution_ids = conditions.get(
            "bundled-semantic-provider", {}).get("allowedContributionIds")
        delivery_provider_ids = conditions.get(
            "bundled-semantic-provider-stage", {}).get("allowedProviderIds")
        canonical_list = ["rust-semantic", "typescript-semantic"]
        if contribution_ids != canonical_provider_ids or \
                provider_ids != canonical_provider_ids or \
                delivery_contribution_ids != canonical_list or \
                delivery_provider_ids != canonical_list:
            f.append("C2DL: v1 full-profile contributionId/providerId surfaces drift "
                     "from DELIVERY's exact rust-semantic/typescript-semantic namespace")
    totality_matrix = c.get("planIntentTotalityMatrix", {})
    matrix_keys = totality_matrix.get("scalarCollectionKeys", [])
    matrix_values = totality_matrix.get("hostileValues", [])
    if {item.get("id") for item in matrix_keys} != {
            "resolved-configuration-path", "contribution-activation-id",
            "contribution-id", "capability-grant-id"} or \
            {item.get("jsonType") for item in matrix_values} != {
                "object", "array", "boolean", "null"} or \
            totality_matrix.get("caseCount") != 16 or \
            totality_matrix.get("expectedViolation") != "C2I-02" or \
            totality_matrix.get("expectedCreatesAttempt") is not False:
        f.append("I1: hostile parsed-JSON totality matrix is not the exact 4x4 corpus")
    else:
        for key_case in matrix_keys:
            base = intent_values.get(key_case.get("baseFixtureId"))
            if base is None:
                f.append(f"I1 totality {key_case.get('id')}: base fixture missing")
                continue
            for value_case in matrix_values:
                candidate = _pointer_mutate(base, {
                    "op": "set", "path": key_case["path"], "value": value_case["value"]})
                errors = validate_plan_intent(candidate, c, relations)
                codes = {code for code, _ in errors}
                if "C2I-02" not in codes:
                    f.append(f"I1 totality {key_case['id']}/{value_case['jsonType']}: "
                             f"expected typed C2I-02 rejection, got {sorted(codes)}")
    seen_intent_codes: set[str] = set()
    valid_operations: set[str] = set()
    for fx in c.get("planIntentFixtures", []):
        intent = intent_values.get(fx.get("id"))
        if intent is None:
            continue
        errs = validate_plan_intent(intent, c, relations)
        codes = {code for code, _ in errs}
        seen_intent_codes.update(codes)
        try:
            commitment = plan_intent_commitment(intent, c)
        except ValueError as exc:
            errs.append(("C2I-04", str(exc)))
            codes.add("C2I-04")
            commitment = None
        if fx.get("valid"):
            expected = fx.get("expectedCommitment")
            if errs:
                f.append(f"I1 {fx['id']}: expected valid but got — {errs[0][1]}")
            if expected != commitment:
                f.append(f"I2 {fx['id']}: commitment vector is {expected!r}; recomputed {commitment!r}")
            if intent.get("intentKind") == "stored-view":
                valid_operations.add(intent["storedView"]["query"]["operation"])
                if fx.get("expectedCreatesAttempt") is not False or \
                        fx.get("expectedCreatesExecutionPlan") is not False:
                    f.append(f"I1 {fx['id']}: stored-view fixture does not assert zero attempt/ExecutionPlan")
                stored_rule = lifecycle.get("onValidatedStoredRead", "")
                if "No ExecutionId" not in stored_rule or "AttemptRecord" not in stored_rule or \
                        "ExecutionPlan" not in stored_rule:
                    f.append("I1: stored-view lifecycle does not preserve the zero-attempt boundary")
        else:
            want = fx.get("violates")
            if not errs:
                f.append(f"I1 {fx['id']}: expected pre-attempt rejection by {want} but intent validated")
            elif want not in codes:
                f.append(f"I1 {fx['id']}: expected {want}, got {sorted(codes)}")
    for required_code in {"C2I-01", "C2I-02", "C2I-03", "C2I-07"} - seen_intent_codes:
        f.append(f"I1: no negative PlanIntent fixture proves {required_code}")
    totality = intent_spec.get("validationTotality", {})
    totality_classes = {fx.get("totalityClass") for fx in c.get("planIntentFixtures", [])
                        if fx.get("totalityClass")}
    expected_totality_classes = {
        "object-in-scalar-collection-key", "array-in-scalar-collection-key",
        "boolean-in-scalar-collection-key", "null-in-scalar-collection-key",
    }
    if totality_classes != expected_totality_classes or \
            "Every successfully parsed JSON value" not in totality.get("domain", "") or \
            "never raises" not in totality.get("result", ""):
        f.append("I1: PlanIntent parsed-JSON totality contract/corpus is incomplete")
    expected_operations = set(intent_spec.get("storedViewIntentV1", {})
                              .get("query", {}).get("closedTaggedUnion", {}))
    if valid_operations != expected_operations:
        f.append(f"I1: stored-view positive vectors cover {sorted(valid_operations)}, "
                 f"expected every query branch {sorted(expected_operations)}")

    valid_intents = [intent_values[fx["id"]] for fx in c.get("planIntentFixtures", [])
                     if fx.get("valid") and fx.get("id") in intent_values]
    external_scanner_visible = any(
        intent.get("intentKind") == "analysis" and
        any(stage.get("kind") == "fact-derivation" and
            stage.get("operator") == "external-scanner" and stage.get("providerId")
            for stage in intent["analysis"]["admissionDescriptor"]["workflow"]["stages"]) and
        any(item.get("authority") == "external-scanner"
            for item in intent["analysis"]["admissionDescriptor"]["contributions"])
        for intent in valid_intents
    )
    if not external_scanner_visible:
        f.append("I1: no valid general-schema PlanIntent exposes external-scanner at both stage and contribution surfaces")

    seen_binding_codes: set[str] = set()
    for fx in c.get("intentBindingFixtures", []):
        base = intent_values.get(fx.get("baseFixtureId"))
        if base is None:
            f.append(f"I3 {fx.get('id')}: unknown base PlanIntent fixture")
            continue
        try:
            errs = validate_intent_binding(fx, base, c, relations)
        except ValueError as exc:
            errs = [("C2I-04", str(exc))]
        codes = {code for code, _ in errs}
        seen_binding_codes.update(codes)
        if fx.get("valid") and errs:
            f.append(f"I3 {fx['id']}: expected valid but got — {errs[0][1]}")
        elif not fx.get("valid"):
            want = fx.get("violates")
            if not errs:
                f.append(f"I3 {fx['id']}: expected binding rejection by {want} but it validated")
            elif want not in codes:
                f.append(f"I3 {fx['id']}: expected {want}, got {sorted(codes)}")
    for required_code in {"C2I-05", "C2I-06"} - seen_binding_codes:
        f.append(f"I3: no negative analysis intent-binding fixture proves {required_code}")

    seen_stored_binding_codes: set[str] = set()
    for fx in c.get("storedViewBindingFixtures", []):
        base = intent_values.get(fx.get("baseFixtureId"))
        if base is None:
            f.append(f"I4 {fx.get('id')}: unknown base stored-view fixture")
            continue
        try:
            errs = validate_stored_view_binding(fx, base, c)
        except ValueError as exc:
            errs = [("C2I-04", str(exc))]
        codes = {code for code, _ in errs}
        seen_stored_binding_codes.update(codes)
        if fx.get("valid") and errs:
            f.append(f"I4 {fx['id']}: expected valid but got — {errs[0][1]}")
        elif fx.get("valid") and fx.get("requestIdAuthority") != "host-minted-reserved":
            f.append(f"I4 {fx['id']}: positive stored read does not declare host-minted-reserved REQUEST-ID-V1")
        elif not fx.get("valid"):
            want = fx.get("violates")
            if not errs:
                f.append(f"I4 {fx['id']}: expected stored-read rejection by {want} but it validated")
            elif want not in codes:
                f.append(f"I4 {fx['id']}: expected {want}, got {sorted(codes)}")
        if fx.get("valid") and (fx.get("expectedCreatesAttempt") is not False or
                                fx.get("expectedCreatesExecutionPlan") is not False):
            f.append(f"I4 {fx['id']}: stored binding does not assert zero attempt/ExecutionPlan")
    for required_code in {"C2I-08", "C2I-09"} - seen_stored_binding_codes:
        f.append(f"I4: no negative stored-view binding fixture proves {required_code}")

    # ---- C3X: no paper seals ----
    # ``implementable`` is feasibility metadata.  It says a test can be built;
    # it is not evidence that the test ran.  R2-FINAL-02 found the previous
    # checker accepted exactly that inference for every implementable:true row.
    impl = {t["id"]: t.get("implementable", False) for t in c["conformanceTests"]}
    for prop in c["dischargeStatus"]["properties"]:
        for tid in prop["dischargedBy"]:
            if tid not in impl:
                f.append(f"C3X: '{prop['property']}' names unknown test '{tid}'")
            elif not impl[tid]:
                f.append(f"C3X: '{prop['property']}' is discharged by '{tid}', which is "
                         f"not implementable — that is a paper seal")
        if prop["status"] == "SPECIFIED" and prop["dischargedBy"] and \
                prop.get("evidenceGrade") != "IMPLEMENTABLE_UNEXECUTED":
            f.append(f"C3X: '{prop['property']}' is SPECIFIED by unexecuted tests but "
                     "does not say IMPLEMENTABLE_UNEXECUTED")
        if prop["status"] in {"DISCHARGED", "DEMONSTRATED"}:
            if not prop["dischargedBy"]:
                f.append(f"C3X: '{prop['property']}' claims {prop['status']} with no tests")
            if prop.get("evidenceGrade") != "DEMONSTRATED" or not \
                    prop.get("demonstrationEvidenceIds"):
                f.append(f"C3X: '{prop['property']}' claims {prop['status']} without "
                         "evidenceGrade DEMONSTRATED and retained demonstrationEvidenceIds "
                         "— implementable:true is not execution evidence")

    # ---- P1..P5 plan fixtures ----
    # The generic grammar remains open to future provider identifiers. This
    # specifically named positive vector is the shipping TypeScript provider
    # vector, so it must not double as an alias/future-provider example.
    provider_fixture = next((fx for fx in c.get("planFixtures", [])
                             if isinstance(fx, dict) and
                             fx.get("id") == "valid-provider-plan"), None)
    provider_stages = ((provider_fixture or {}).get("plan") or {}).get("stages")
    semantic_stages = [stage for stage in provider_stages
                       if isinstance(stage, dict) and
                       stage.get("operator") == "semantic-provider"] \
        if isinstance(provider_stages, list) else []
    if provider_fixture is None or provider_fixture.get("valid") is not True or \
            len(semantic_stages) != 1 or \
            semantic_stages[0].get("providerId") != "typescript-semantic":
        f.append("C2PV: valid-provider-plan must use the exact shipping providerId "
                 "'typescript-semantic'")
    for fx in c["planFixtures"]:
        errs = validate_plan(fx["plan"], c, relations)
        codes = {code for code, _ in errs}
        if fx["valid"] and errs:
            f.append(f"P1 {fx['id']}: expected valid but got — {errs[0][1]}")
        elif not fx["valid"]:
            want = fx.get("violates")
            if not errs:
                f.append(f"P1 {fx['id']}: expected REJECTION (violates {want}) but the "
                         f"plan validated")
            elif want not in codes:
                # rejected, but not for the stated reason — evidence by coincidence
                f.append(f"P1 {fx['id']}: expected rejection by {want} but was rejected "
                         f"by {sorted(codes)} — the fixture proves a different property "
                         f"than it claims")

    # ---- C4 coverage fixtures ----
    for fx in c["coverageFixtures"]:
        errs = validate_coverage(fx["entry"], c, fp)
        if fx["valid"] and errs:
            f.append(f"C4 {fx['id']}: expected valid but got — {errs[0]}")
        elif not fx["valid"] and not errs:
            f.append(f"C4 {fx['id']}: expected REJECTION (violates {fx.get('violates')}) "
                     f"but the entry validated")

    # ---- coverage of the fixture set itself ----
    kinds = set(c["executionPlan"]["stageKinds"])
    seen = {st.get("kind") for fx in c["planFixtures"] if fx["valid"]
            for st in fx["plan"]["stages"]}
    for k in kinds - seen:
        f.append(f"P2: stage kind '{k}' has no positive fixture — unexercised schema")
    return f


def check(c: object, d9: dict | None, fp: dict | None, tm: dict | None = None,
          operability: dict | None = None,
          delivery: dict | None = None) -> list[str]:
    """Total contract boundary: malformed parsed JSON becomes a named finding."""
    if not isinstance(c, dict) or not c:
        return ["C2-TOTALITY-ROOT: contract root must be a non-empty object"]
    admission = c.get("theAdmissionBoundary")
    if not isinstance(admission, dict) or not isinstance(admission.get("levels"), list):
        return ["C2-TOTALITY-SHAPE: theAdmissionBoundary.levels must be an array"]
    try:
        return _check(c, d9, fp, tm, operability, delivery)
    except MALFORMED_SHAPE_EXCEPTIONS as exc:
        return [f"C2-TOTALITY-EXCEPTION: malformed contract shape "
                f"({type(exc).__name__})"]


# --------------------------------------------------------------------------
def _m_snapshot_preadmission(c):
    for lv in c["theAdmissionBoundary"]["levels"]:
        if lv["level"] == "snapshot-binding":
            lv["onFailure"] = "pre-admission: request-rejected, never a Run verdict"

def _m_execid_after_snapshot(c):
    for lv in c["theAdmissionBoundary"]["levels"]:
        if lv["level"] == "attempt-admission":
            lv["allocates"] = []

def _m_paper_seal(c):
    for p in c["dischargeStatus"]["properties"]:
        if p["property"] == "effectful work is unrepresentable as a Rule":
            p["dischargedBy"] = ["PS-09", "PS-12c"]
            p["status"] = "DISCHARGED"

def _m_ps07_discharges_privacy(c):
    for p in c["dischargeStatus"]["properties"]:
        if p["property"] == "physical storage schema stays private":
            p["dischargedBy"] = ["PS-02", "PS-07"]

def _m_implementable_boolean_discharges(c):
    for p in c["dischargeStatus"]["properties"]:
        if p["property"] == "fact sufficiency is predicate-relative":
            p["status"] = "DISCHARGED"
            p.pop("evidenceGrade", None)

def _m_allow_private_operator(c):
    c["stageSchemas"]["privateOperators"]["names"].remove("shardAssignment")

def _m_rule_may_have_grants(c):
    c["stageSchemas"]["kinds"]["rule-evaluation"]["forbidden"] = []
    c["stageSchemas"]["kinds"]["rule-evaluation"]["optional"] = ["capabilityGrants", "operator"]

def _m_open_stage_kinds(c):
    c["executionPlan"]["stageKinds"].append("snapshot")
    c["stageSchemas"]["kinds"]["snapshot"] = {"required": [], "optional": [], "effectClass": "no-effect"}

def _m_drop_target_universe(c):
    c["coverageKey"]["crossUniverseRelations"] = []

def _m_unknown_relation_ok(c):
    for fx in c["planFixtures"]:
        if fx["id"] == "reject-unknown-relation":
            fx["valid"] = True

def _m_probe_without_grants_ok(c):
    c["stageSchemas"]["kinds"]["probe"]["required"] = ["probeId"]

def _m_open_plan_intent(c):
    c["planIntent"]["schema"]["closed"] = False

def _m_change_intent_domain(c):
    c["planIntent"]["canonicalCommitment"]["domainTagUtf8"] = "opensip.plan-intent.v2"

def _m_drop_attempt_intent_commitment(c):
    fixture = next(x for x in c["intentBindingFixtures"]
                   if x["id"] == "valid-frozen-intent-execution-plan")
    fixture["attemptRecord"].pop("planIntentCommitment")

def _m_accept_stage_substitution(c):
    fixture = next(x for x in c["intentBindingFixtures"]
                   if x["id"] == "reject-post-admission-stage-substitution")
    fixture["valid"] = True

def _m_hide_external_scanner_intent(c):
    fixture = next(x for x in c["planIntentFixtures"]
                   if x["id"] == "valid-explicit-general-authority-forms")
    stage = fixture["intent"]["analysis"]["admissionDescriptor"]["workflow"]["stages"][0]
    stage["operator"] = "builtin-extractor"
    stage.pop("providerId")

def _m_accept_null_contribution_id(c):
    fixture = next(x for x in c["planIntentFixtures"]
                   if x["id"] == "reject-null-contribution-id-before-attempt")
    fixture["valid"] = True

def _m_accept_stored_target_substitution(c):
    fixture = next(x for x in c["storedViewBindingFixtures"]
                   if x["id"] == "reject-stored-read-target-substitution")
    fixture["valid"] = True

def _m_shrink_plan_descriptor_join(c):
    c["planIntent"]["attemptAndExecutionJoin"]["planIdentityInputsRequired"].remove("contributions")

def _mark_plan_intent_fixture_valid(c, fixture_id):
    next(x for x in c["planIntentFixtures"] if x["id"] == fixture_id)["valid"] = True

def _m_accept_object_config_path(c):
    _mark_plan_intent_fixture_valid(c, "reject-object-resolved-configuration-path-before-attempt")

def _m_accept_array_activation_id(c):
    _mark_plan_intent_fixture_valid(c, "reject-array-contribution-activation-id-before-attempt")

def _m_accept_boolean_contribution_id(c):
    _mark_plan_intent_fixture_valid(c, "reject-boolean-contribution-id-before-attempt")

def _m_accept_null_grant_id(c):
    _mark_plan_intent_fixture_valid(c, "reject-null-capability-grant-id-before-attempt")

def _m_accept_malformed_stored_request_id(c):
    next(x for x in c["storedViewBindingFixtures"]
         if x["id"] == "reject-stored-read-malformed-request-id")["valid"] = True

def _m_accept_caller_stored_request_id(c):
    next(x for x in c["storedViewBindingFixtures"]
         if x["id"] == "reject-stored-read-caller-supplied-request-id")["valid"] = True

def _m_drift_request_id_join(c):
    c["planIntent"]["storedViewJoin"]["requestIdContract"]["pattern"] = \
        "^request-[0-9]+$"

def _m_drop_totality_collection_key(c):
    c["planIntentTotalityMatrix"]["scalarCollectionKeys"].pop()

def _m_drop_totality_hostile_type(c):
    c["planIntentTotalityMatrix"]["hostileValues"].pop()

def _m_prefix_full_profile_provider_ids(c):
    fixture = next(x for x in c["planIntentFixtures"]
                   if x["id"] == "valid-full-profile-semantic-providers")
    descriptor = fixture["intent"]["analysis"]["admissionDescriptor"]
    prefixed = {
        "rust-semantic": "provider.rust-semantic",
        "typescript-semantic": "provider.typescript-semantic",
    }
    for item in descriptor["contributions"]:
        if item.get("contributionId") in prefixed:
            item["contributionId"] = prefixed[item["contributionId"]]
    for stage in descriptor["workflow"]["stages"]:
        if stage.get("providerId") in prefixed:
            stage["providerId"] = prefixed[stage["providerId"]]
    # Keep the commitment vector internally exact so only the v1 cross-contract
    # provider namespace join can reject this otherwise-valid coordinated drift.
    fixture["expectedCommitment"] = plan_intent_commitment(fixture["intent"], c)


def _set_valid_provider_plan_id(c, provider_id):
    fixture = next(x for x in c["planFixtures"]
                   if x["id"] == "valid-provider-plan")
    fixture["plan"]["stages"][0]["providerId"] = provider_id


def _m_alias_valid_provider_plan(c):
    _set_valid_provider_plan_id(c, "provider.typescript-semantic")


def _m_legacy_valid_provider_plan(c):
    _set_valid_provider_plan_id(c, "typescript")


def _m_arbitrary_valid_provider_plan(c):
    _set_valid_provider_plan_id(c, "arbitrary-semantic-provider")

MUTATIONS = [
    ("make snapshot failure pre-admission again (B-C2V2-01)", _m_snapshot_preadmission),
    ("allocate ExecutionId after snapshot work (EC-6)", _m_execid_after_snapshot),
    ("discharge a sealed property with an unbuilt test (B-C2V2-02)", _m_paper_seal),
    ("treat implementable:true as retained discharge evidence (R2-FINAL-02)",
     _m_implementable_boolean_discharges),
    ("let PS-07 discharge private-operator privacy (A1-C2V2-05)", _m_ps07_discharges_privacy),
    ("permit a private operator in a plan (PS-02)", _m_allow_private_operator),
    ("let a rule stage hold capability grants (PS-12a)", _m_rule_may_have_grants),
    ("reopen the stage-kind set (PS-01/PS-11)", _m_open_stage_kinds),
    ("stop requiring targetUniverseId (B-C2V2-05)", _m_drop_target_universe),
    ("accept a relation outside the fact-plane registry (P5)", _m_unknown_relation_ok),
    ("let a probe run without capability grants (PS-12b)", _m_probe_without_grants_ok),
    ("make the pre-admission PlanIntent schema open (IP-R4-04)", _m_open_plan_intent),
    ("change the PlanIntent commitment domain without new vectors", _m_change_intent_domain),
    ("allocate an attempt without its admitted-intent commitment", _m_drop_attempt_intent_commitment),
    ("accept post-admission stage substitution", _m_accept_stage_substitution),
    ("hide external-scanner from the pre-admission operator surface", _m_hide_external_scanner_intent),
    ("accept null contribution identity in admitted input", _m_accept_null_contribution_id),
    ("accept stored-read target substitution", _m_accept_stored_target_substitution),
    ("shrink the exact PlanDescriptor equality join", _m_shrink_plan_descriptor_join),
    ("accept object-valued resolved-configuration path", _m_accept_object_config_path),
    ("accept array-valued contribution activationId", _m_accept_array_activation_id),
    ("accept boolean-valued contributionId", _m_accept_boolean_contribution_id),
    ("accept null capability grantId", _m_accept_null_grant_id),
    ("accept malformed matching stored-read RequestId", _m_accept_malformed_stored_request_id),
    ("accept caller-supplied stored-read RequestId", _m_accept_caller_stored_request_id),
    ("drift stored-read RequestId from live REQUEST-ID-V1", _m_drift_request_id_join),
    ("drop one exception-prone scalar key from totality matrix", _m_drop_totality_collection_key),
    ("drop one hostile JSON type from totality matrix", _m_drop_totality_hostile_type),
    ("drift the joined v1 full-profile provider namespace to provider.*",
     _m_prefix_full_profile_provider_ids),
    ("alias valid-provider-plan as provider.typescript-semantic (R9-PROVIDER-VECTOR-01)",
     _m_alias_valid_provider_plan),
    ("alias valid-provider-plan as legacy typescript (R9-PROVIDER-VECTOR-01)",
     _m_legacy_valid_provider_plan),
    ("replace valid-provider-plan with an arbitrary canonical identifier "
     "(R9-PROVIDER-VECTOR-01)", _m_arbitrary_valid_provider_plan),
]


def selftest(base: dict, d9, fp, tm, operability, delivery) -> int:
    # A mutation suite only means anything against a clean base. Otherwise every row
    # echoes the pre-existing failure and reports "all rejected" — a false assurance
    # that actually occurred on the first run of check-evidence.py.
    pre = check(base, d9, fp, tm, operability, delivery)
    if pre:
        print(f"REFUSING to self-test: the base contract has {len(pre)} finding(s), so "
              f"every mutation would be masked by them.")
        for x in pre[:5]:
            print("  -", x)
        return 1
    print("mutation self-test — each row must be REJECTED\n")
    escaped = 0
    for name, root in TOTALITY_ROOT_CASES:
        findings = check(copy.deepcopy(root), d9, fp, tm, operability, delivery)
        if not findings:
            escaped += 1
        print(f"  {'reject' if findings else 'ESCAPE':>6}  parsed-JSON root {name}")
        print(f"          {findings[0] if findings else 'NO FINDING — root survived'}")
    for name, mut in MUTATIONS:
        c = copy.deepcopy(base)
        mut(c)
        findings = check(c, d9, fp, tm, operability, delivery)
        if not findings:
            escaped += 1
        print(f"  {'reject' if findings else 'ESCAPE':>6}  {name}")
        print(f"          {findings[0] if findings else 'NO FINDING — mutation survived'}")
    print()
    if escaped:
        print(f"{escaped}/{len(MUTATIONS) + len(TOTALITY_ROOT_CASES)} retained cases "
              "ESCAPED — the proof path is optional")
        return 1
    print(f"all {len(MUTATIONS)} semantic mutations and {len(TOTALITY_ROOT_CASES)} "
          "root-shape cases rejected — the proof path is load-bearing")
    return 0


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--selftest"]
    p = pathlib.Path(args[0]) if args else HERE / BINDING
    if not p.exists():
        print(f"missing contract: {p}", file=sys.stderr)
        return 2
    c = json.loads(p.read_text())
    d9, fp, tm, operability, delivery = \
        load(D9), load(FP), load(TM), load(OP), load(DELIVERY)
    if "--selftest" in sys.argv:
        return selftest(c, d9, fp, tm, operability, delivery)
    f = check(c, d9, fp, tm, operability, delivery)
    if not f:
        ni, nb = len(c["planIntentFixtures"]), len(c["intentBindingFixtures"])
        ns = len(c.get("storedViewBindingFixtures", []))
        np_, nc = len(c["planFixtures"]), len(c["coverageFixtures"])
        impl = sum(1 for t in c["conformanceTests"] if t.get("implementable"))
        tot = len(c["conformanceTests"])
        print(f"C-2 contract OK — {p.name}, {ni} PlanIntent + {nb} analysis binding + "
              f"{ns} stored binding + {np_} stage-plan + {nc} coverage fixtures, "
              f"I1..I4/C1X/C2X/C3X/P1..P5 clean")
        print(f"  cross-checked against {D9}, {FP}, {TM}, {OP} and {DELIVERY}")
        print(f"  {impl}/{tot} conformance tests implementable; "
              f"{tot - impl} blocked on ARCH.PROBE-CONTRACT or an unbuilt harness")
        return 0
    print(f"{len(f)} finding(s) in {p.name}:")
    for x in f:
        print("  -", x)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
