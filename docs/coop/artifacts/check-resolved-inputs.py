#!/usr/bin/env python3
"""Retained executable checker for the resolved-inputs contract.

Two findings shaped this file:

  B-CSG-01  the ambient-environment closure was ABSENT. v1 recorded an environment
            identity and stopped, which is not the same as neutralising locale,
            clock, entropy, enumeration order or path form. Recording buys
            reproducibility-by-identity at the cost of portability, and recording
            the inputs you did not think of buys nothing.
  A1-RI-02  the artifact cited threat-model.v1 finding ids that v2 renumbered or
            dropped, while claiming to discharge them — paper compliance. Prose
            review caught it. RI-TM now reads the LIVE threat model, so a stale
            citation is a diff rather than a discovery.

  RI-CL-1  the ambient-input closure is TOTAL over its declared inventory
  RI-CL-2  no input is classified twice
  RI-CL-3  a NEUTRALISED input never enters PlanId  (keying a constant is churn)
  RI-CL-4  a KEYED input always enters PlanId       (else two analyses share an id)
  RI-CL-5  a FORBIDDEN input enters neither         (recording != permitting)
  RI-TM    every threatModelRef resolves in the live threat model
  RI-PR    config precedence is a total order with declared PlanId participation
  RI-SU    both P-4 providers have a semantic universe key, with the dimensions
           whose omission is unsound
  RI-CT    conformance tests marked implementable:false name their blocker
  RI-PID   PLAN-ID-V1 has one closed byte recipe, exact vectors and mandatory
           supplied-vs-recomputed verification
  RI-JOIN  Snapshot/PlanIntent lifecycle, DELIVERY release identities, and the
           binding CI layer-4 product disposition join the recipe without drift

Usage: python3 artifacts/check-resolved-inputs.py [contract]   ·   --selftest
Exit:  0 clean · 1 findings · 2 IO error
"""
from __future__ import annotations
import copy, hashlib, json, pathlib, re, struct, sys, unicodedata

BINDING = "resolved-inputs.v2.json"
TM = "threat-model.v3.json"
C2 = "c2-plan-stage-schema.v3.json"
DELIVERY = "delivery.v2.json"
PRODUCT = "product-dispositions.v1.json"
D9 = "d9-exit-contract.v1.6.json"
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

PLAN_DOMAIN_DESCRIPTION = (
    "UTF-8 bytes 6f70656e7369702e706c616e2d696400 (the ASCII string "
    "opensip.plan-id followed by one NUL byte)"
)
PLAN_DOMAIN_BYTES = b"opensip.plan-id\0"
PLAN_FIELDS = [
    (1, "snapshotId"),
    (2, "planSchemaMajor"),
    (3, "release"),
    (4, "invocationProfile"),
    (5, "resolvedConfiguration"),
    (6, "scope"),
    (7, "changeSpec"),
    (8, "contributions"),
    (9, "semanticUniverses"),
    (10, "capabilityGrants"),
    (11, "workflow"),
    (12, "budgets"),
    (13, "planIntentCommitment"),
]
PLAN_ID_RE = re.compile(r"^plan1:sha256:[0-9a-f]{64}$")
SNAPSHOT_ID_RE = re.compile(r"^snap1:sha256:[0-9a-f]{64}$")
PROJECT_ID_RE = re.compile(r"^prj1-[0-9a-f]{64}$")
COMMITMENT_RE = re.compile(r"^sha256:[0-9a-f]{64}$")
DIGEST_RE = re.compile(r"^[0-9a-f]{64}$")
IDENT_RE = re.compile(r"^[a-z][a-z0-9]*(?:[._:-][a-z0-9]+)*$")
VERSION_RE = re.compile(
    r"^(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)\.(0|[1-9][0-9]*)"
    r"(?:-[0-9A-Za-z-]+(?:\.[0-9A-Za-z-]+)*)?$"
)
SNAPSHOT_DOMAIN_DESCRIPTION = (
    "UTF-8 bytes 6f70656e7369702e736e617073686f742d696400 (the ASCII string "
    "opensip.snapshot-id followed by one NUL byte)"
)
SNAPSHOT_DOMAIN_BYTES = b"opensip.snapshot-id\0"
PROJECT_MARKER_PREFIX = b"opensip-project-id-v1\n"
PROJECT_MARKER_PATH = ".opensip/project-id.v1"
REQUIRED_PLAN_NEGATIVES = {
    "reject-supplied-planid-mismatch": "PLAN_ID_MISMATCH",
    "reject-uppercase-planid": "PLAN_ID_INVALID_REPRESENTATION",
    "reject-correlation-field": "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION",
    "reject-ci-layer4-record": "PLAN_ID_PROFILE_VIOLATION",
    "reject-neutralised-input": "PLAN_ID_INPUT_CLASS_VIOLATION",
    "reject-unknown-field": "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION",
    "reject-plan-intent-substitution": "PLAN_INTENT_COMMITMENT_MISMATCH",
    "reject-unsorted-scope": "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION",
    "reject-duplicate-requested-path": "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION",
    "reject-contribution-unknown-field": "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION",
    "reject-unsorted-contributions": "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION",
    "reject-rust-universe-unknown-field": "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION",
    "reject-provider-substitution": "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION",
    "reject-universe-order": "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION",
    "reject-grant-unknown-field": "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION",
    "reject-grant-order": "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION",
    "reject-workflow-set-order": "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION",
    "reject-workflow-unknown-field": "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION",
    "reject-invalid-budget-unit": "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION",
    "reject-admitted-artifact-substitution": "PLAN_INTENT_COMMITMENT_MISMATCH",
    "reject-admitted-grant-substitution": "PLAN_INTENT_COMMITMENT_MISMATCH",
    "reject-admitted-parameter-substitution": "PLAN_INTENT_COMMITMENT_MISMATCH",
}
TS_PLAN_UNIVERSE_REQUIRED = {
    "schemaVersion", "manifestId", "capabilityManifestId", "runtimeArtifactId",
    "runtimeArtifactSha256", "providerArtifactId", "providerArtifactSha256",
    "runtimeDescriptorSha256", "providerDescriptorSha256", "protocolMajor",
    "providerBuildId", "nodeVersion", "v8Version", "modulesAbi",
    "typescriptVersion", "typescriptCompilerSha256", "typescriptStdlibMerkleRoot",
    "platformId", "resolvedInputs",
}
TS_RESOLVED_UNIVERSE_REQUIRED = {
    "tsconfigGraphHash", "compilerOptions", "programRootFiles", "packageLockIdentity",
    "resolvedNodeModulesLayout", "executionCapableResolution",
}
TS_DELIVERY_HANDSHAKE_REQUIRED = {
    "protocolMajor", "providerBuildId", "providerDescriptorSha256",
    "defaultWorkBudgetProfileId", "defaultWorkBudgetProfileSha256",
    "runtimeDescriptorSha256", "nodeVersion", "v8Version", "modulesAbi",
    "typescriptVersion", "typescriptCompilerSha256", "typescriptStdlibMerkleRoot",
    "platformId", "capabilities",
}
RUST_PLAN_UNIVERSE_REQUIRED = {
    "schemaVersion", "manifestId", "capabilityManifestId",
    "providerArtifactId", "providerArtifactSha256", "toolchainArtifactId",
    "toolchainArtifactSha256", "protocolMajor", "providerBuildId",
    "rustCommitHash", "rustcVersion", "cargoVersion", "hostTriple",
    "targetTriple", "sysrootDigest", "rustcDevLlvmDigest",
    "standardLibraryComponentDigests", "providerBinarySha256",
    "licenseNoticeBundleSha256", "platformId", "resolvedInputs",
}
RUST_RESOLVED_UNIVERSE_REQUIRED = {
    "edition", "cfg", "packageLockIdentity", "resolvedPackages", "rustflags",
    "crateRootPaths", "executionCapableResolution", "buildScriptOutputs",
    "procMacroOutputs",
}
RUST_DELIVERY_HANDSHAKE_REQUIRED = {
    "protocolMajor", "providerBuildId", "rustCommitHash", "hostTriple",
    "targetTriple", "sysrootDigest", "capabilities",
}
CONTRIBUTION_FIELDS = {
    "activationId", "contributionId", "contributionVersion", "bundleId",
    "artifactDigest", "admissionGrant", "role", "verificationState",
    "verificationEvidenceId", "parameters", "origin", "authority",
}
CAPABILITY_GRANT_FIELDS = {
    "grantId", "grantVersion", "projectId", "capability", "parameters",
}
CHANGE_MODES = {"worktree", "staged-index", "explicit-files", "merge-base", "since-ref"}
IMPACT_EXPANSIONS = {"none", "direct", "transitive"}
GRANT_CAPABILITIES = {
    "read-snapshot", "write-private-scratch", "spawn-process",
    "repository-execution", "network",
}
PLAN_OUTCOMES = {
    "PLAN_ID_INVALID_REPRESENTATION",
    "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION",
    "PLAN_ID_MISMATCH",
    "PLAN_ID_PROFILE_VIOLATION",
    "PLAN_INTENT_COMMITMENT_MISMATCH",
    "PLAN_ID_INPUT_CLASS_VIOLATION",
}
PROJECT_OUTCOMES = {
    "PROJECT_ID_INVALID_REPRESENTATION",
    "PROJECT_ID_CALLER_SUPPLIED",
    "PROJECT_ID_COLLISION",
    "PROJECT_ID_MARKER_TRACKED",
    "PROJECT_ID_MARKER_UNSAFE",
    "PROJECT_ID_ALLOCATION_FAILED",
}
SNAPSHOT_OUTCOMES = {
    "SNAPSHOT_ID_INVALID_REPRESENTATION",
    "SNAPSHOT_ID_PREIMAGE_SCHEMA_VIOLATION",
    "SNAPSHOT_ID_MISMATCH",
}
PROJECT_D9_OUTCOME_CONTEXTS = {
    "PROJECT_ID_INVALID_REPRESENTATION": {
        "callerOrConfig": "request-invalid",
        "persistedMarkerOrRegistry": "persisted-corruption",
    },
    "PROJECT_ID_CALLER_SUPPLIED": {"callerOrConfig": "request-invalid"},
    "PROJECT_ID_COLLISION": {"persistedMarkerOrRegistry": "persisted-corruption"},
    "PROJECT_ID_MARKER_TRACKED": {"callerOrConfig": "request-invalid"},
    "PROJECT_ID_MARKER_UNSAFE": {"persistedMarkerOrRegistry": "persisted-corruption"},
    "PROJECT_ID_ALLOCATION_FAILED": {"allocationInfrastructure": "host-io"},
}
SNAPSHOT_D9_OUTCOME_CONTEXTS = {
    "SNAPSHOT_ID_INVALID_REPRESENTATION": {
        "requestOrMutationInput": "request-invalid",
        "persistedLedgerCasOrCache": "persisted-corruption",
        "providerEcho": "provider-echo",
    },
    "SNAPSHOT_ID_PREIMAGE_SCHEMA_VIOLATION": {
        "requestOrMutationInput": "request-invalid",
        "persistedLedgerCasOrCache": "persisted-corruption",
        "providerEcho": "provider-echo",
    },
    "SNAPSHOT_ID_MISMATCH": {
        "requestOrMutationInput": "request-mismatch",
        "persistedLedgerCasOrCache": "persisted-corruption",
        "providerEcho": "provider-echo",
    },
}
BUDGET_ID_RE = re.compile(
    r"^[a-z][a-z0-9]*(?:[._:-][a-z0-9]+)*\.(?:work-units|milliseconds|bytes|items)$"
)

# Dimensions whose omission from a universe key is unsound, per provider.
# Sourced from A1-RI-01 and A1-RI-05; each is a way two semantically different
# fact sets could otherwise share one identity.
REQUIRED_UNIVERSE_DIMS = {
    "rust": ["target triple", "sysroot", "cfg", "package set", "RUSTFLAGS", "edition",
             "execution-capable"],
    "typescript": ["tsconfig", "compilerOptions", "program root", "execution-capable"],
}


def load(name: str) -> dict | None:
    path = HERE / name
    return json.loads(path.read_text()) if path.exists() else None


def _cve1(value) -> bytes:
    """Independent executable oracle for the closed CVE1 value grammar."""
    if value is None:
        return b"\x00"
    if value is False:
        return b"\x01"
    if value is True:
        return b"\x02"
    if isinstance(value, int):
        if 0 <= value <= 0xffff_ffff_ffff_ffff:
            return b"\x03" + struct.pack(">Q", value)
        if -(1 << 63) <= value < 0:
            return b"\x07" + struct.pack(">q", value)
        raise ValueError("integer outside CVE1 signed/unsigned 64-bit range")
    if isinstance(value, str):
        if unicodedata.normalize("NFC", value) != value:
            raise ValueError("non-NFC string")
        encoded = value.encode("utf-8")
        if len(encoded) > 0xffff_ffff:
            raise ValueError("string too long")
        return b"\x04" + struct.pack(">I", len(encoded)) + encoded
    if isinstance(value, list):
        if len(value) > 0xffff_ffff:
            raise ValueError("array too long")
        return b"\x05" + struct.pack(">I", len(value)) + b"".join(
            _cve1(item) for item in value
        )
    if isinstance(value, dict):
        if not all(isinstance(key, str) for key in value):
            raise ValueError("non-string map key")
        keys = sorted(value, key=lambda key: key.encode("utf-8"))
        if len(keys) > 0xffff_ffff:
            raise ValueError("map too large")
        return b"\x06" + struct.pack(">I", len(keys)) + b"".join(
            _cve1(key) + _cve1(value[key]) for key in keys
        )
    raise ValueError(f"unsupported CVE1 type {type(value).__name__}")


def _is_uint(value, maximum=0xffff_ffff_ffff_ffff) -> bool:
    return isinstance(value, int) and not isinstance(value, bool) and 0 <= value <= maximum


def _is_nfc_text(value, *, nonempty=True) -> bool:
    return isinstance(value, str) and (bool(value) or not nonempty) and \
        unicodedata.normalize("NFC", value) == value and "\x00" not in value


def _closed(value, fields: set[str]) -> bool:
    return isinstance(value, dict) and set(value) == fields


def _path_error(value) -> str | None:
    if not _is_nfc_text(value):
        return "is not a non-empty NFC string"
    if value.startswith("/") or value.endswith("/") or "\\" in value:
        return "is not a forward-slash project-relative path"
    parts = value.split("/")
    if any(part in {"", ".", ".."} for part in parts):
        return "contains an empty, dot, or dot-dot segment"
    return None


def _sorted_unique_text(values, *, nonempty=False, path_values=False) -> bool:
    if not isinstance(values, list) or (nonempty and not values):
        return False
    if not all(_is_nfc_text(value) for value in values):
        return False
    if path_values and any(_path_error(value) for value in values):
        return False
    return values == sorted(values, key=lambda value: value.encode("utf-8")) and \
        len(values) == len(set(values))


def _release_errors(value, delivery: dict | None) -> list[str]:
    errors: list[str] = []
    if not _closed(value, {"manifestId", "capabilityManifestId", "profileId"}):
        return ["release is not the exact closed identity map"]
    for field in ("manifestId", "capabilityManifestId"):
        if not isinstance(value[field], str) or not DIGEST_RE.fullmatch(value[field]):
            errors.append(f"release.{field} is not 64 lowercase SHA-256 hex")
    profiles = {
        item.get("profile") for item in ((delivery or {}).get("installProfiles") or {})
        .get("profiles", [])
    }
    if not _is_nfc_text(value["profileId"]) or (profiles and value["profileId"] not in profiles):
        errors.append("release.profileId is not a live DELIVERY profile")
    return errors


def _configuration_errors(value, profile: str) -> list[str]:
    errors: list[str] = []
    if not isinstance(value, list):
        return ["resolvedConfiguration is not an array"]
    paths: list[str] = []
    for item in value:
        if not _closed(item, {"path", "value", "decidingLayer", "analysisAffecting"}):
            errors.append("resolvedConfiguration entry is not the exact closed record")
            continue
        if not _is_nfc_text(item["path"]):
            errors.append("resolvedConfiguration.path is not canonical text")
        else:
            paths.append(item["path"])
        if item["analysisAffecting"] is not True:
            errors.append("resolvedConfiguration includes a non-analysis field")
        if not _is_uint(item["decidingLayer"], 6) or item["decidingLayer"] == 0:
            errors.append("resolvedConfiguration decidingLayer is outside 1..6")
        if profile == "ci" and item["decidingLayer"] == 4:
            errors.append("CI record contains layer 4")
        try:
            _cve1(item["value"])
        except ValueError as exc:
            errors.append(f"resolvedConfiguration.value is not CVE1: {exc}")
    if paths != sorted(paths, key=lambda item: item.encode("utf-8")) or \
            len(paths) != len(set(paths)):
        errors.append("resolvedConfiguration is not sorted unique by path")
    return errors


def _change_spec_errors(value) -> list[str]:
    fields = {"mode", "baseCommitId", "dirtyOverlayPolicy", "untrackedPolicy", "vcsAdapterId"}
    if not _closed(value, fields):
        return ["changeSpec is not the exact closed record"]
    errors: list[str] = []
    if value["mode"] not in CHANGE_MODES:
        errors.append("changeSpec.mode is outside the closed token enum")
    base = value["baseCommitId"]
    if base is not None and (not _is_nfc_text(base) or len(base.encode("utf-8")) > 256):
        errors.append("changeSpec.baseCommitId is neither null nor bounded canonical text")
    if value["dirtyOverlayPolicy"] not in {"include", "exclude"}:
        errors.append("changeSpec.dirtyOverlayPolicy is outside the closed enum")
    if value["untrackedPolicy"] not in {"include", "exclude"}:
        errors.append("changeSpec.untrackedPolicy is outside the closed enum")
    if not _is_nfc_text(value["vcsAdapterId"]) or not IDENT_RE.fullmatch(value["vcsAdapterId"]):
        errors.append("changeSpec.vcsAdapterId is not a canonical identifier")
    return errors


def _scope_errors(value) -> list[str]:
    fields = {"projectId", "workspaceUnitIds", "requestedPaths", "impactExpansion"}
    if not _closed(value, fields):
        return ["scope is not the exact closed record"]
    errors: list[str] = []
    if not PROJECT_ID_RE.fullmatch(value["projectId"] if isinstance(value["projectId"], str) else ""):
        errors.append("scope.projectId is not canonical PROJECT-ID-V1")
    if not _sorted_unique_text(value["workspaceUnitIds"], nonempty=True):
        errors.append("scope.workspaceUnitIds is not non-empty sorted unique canonical text")
    if not _sorted_unique_text(value["requestedPaths"], path_values=True):
        errors.append("scope.requestedPaths is not sorted unique canonical paths")
    if value["impactExpansion"] not in IMPACT_EXPANSIONS:
        errors.append("scope.impactExpansion is outside the closed enum")
    return errors


def _budget_errors(value, where="budgets") -> list[str]:
    if not isinstance(value, dict):
        return [f"{where} is not a map"]
    errors: list[str] = []
    if len(value) > 64:
        errors.append(f"{where} has more than 64 entries")
    for key, amount in value.items():
        if not isinstance(key, str) or not BUDGET_ID_RE.fullmatch(key):
            errors.append(f"{where} has unknown or unitless budget id {key!r}")
        if not _is_uint(amount, (1 << 63) - 1) or amount == 0:
            errors.append(f"{where}.{key} is not integer 1..i64::MAX")
    return errors


def _bounded_parameter_errors(value, where="parameters", depth=0) -> list[str]:
    if depth > 8:
        return [f"{where} exceeds maximum depth 8"]
    if value is None or isinstance(value, bool):
        return []
    if isinstance(value, int) and not isinstance(value, bool):
        return [] if -(1 << 63) <= value < (1 << 63) else [f"{where} integer outside signed-64"]
    if isinstance(value, str):
        return [] if unicodedata.normalize("NFC", value) == value and \
            len(value.encode("utf-8")) <= 4096 else [f"{where} string is non-NFC or too long"]
    if isinstance(value, list):
        if len(value) > 256:
            return [f"{where} array exceeds 256 items"]
        return [error for index, item in enumerate(value)
                for error in _bounded_parameter_errors(item, f"{where}[{index}]", depth + 1)]
    if isinstance(value, dict):
        if len(value) > 64 or any(not isinstance(key, str) or not IDENT_RE.fullmatch(key)
                                  for key in value):
            return [f"{where} map keys/count violate boundedParameterValue"]
        if list(value) != sorted(value, key=lambda key: key.encode("utf-8")):
            return [f"{where} map keys are not sorted by UTF-8 bytes"]
        errors: list[str] = []
        for key, item in value.items():
            errors += _bounded_parameter_errors(item, f"{where}.{key}", depth + 1)
        try:
            if len(_canonical_json(value)) > 65536:
                errors.append(f"{where} exceeds 65536 canonical bytes")
        except ValueError as exc:
            errors.append(f"{where} is not canonical JSON: {exc}")
        return errors
    return [f"{where} has forbidden JSON type"]


def _contribution_errors(values, c2: dict | None, delivery: dict | None) -> list[str]:
    if not isinstance(values, list):
        return ["contributions is not an array"]
    errors: list[str] = []
    activation_ids: list[str] = []
    c2_contribution = ((((c2 or {}).get("planIntent") or {})
                        .get("admissionDescriptorV1") or {}).get("contribution") or {})
    if c2_contribution.get("closed") is not True or \
            set(c2_contribution.get("required", [])) != CONTRIBUTION_FIELDS:
        errors.append("live C-2 contribution schema is not the exact closed Plan record")
    origins = set(c2_contribution.get("origin", []))
    authorities = set(c2_contribution.get("authority", []))
    roles = set(c2_contribution.get("role", []))
    verification_states = set(c2_contribution.get("verificationState", []))
    delivery_grants = {
        row.get("grant") for row in ((delivery or {}).get("provenancePolicy") or {}).get("grants", [])
    } or {"published", "local-development"}
    for item in values:
        if not _closed(item, CONTRIBUTION_FIELDS):
            errors.append("contribution is not the exact closed AdmissionDescriptor record")
            continue
        for field in ("activationId", "contributionId", "bundleId"):
            if not _is_nfc_text(item[field]) or not IDENT_RE.fullmatch(item[field]):
                errors.append(f"contribution.{field} is not a canonical identifier")
        if _is_nfc_text(item["activationId"]):
            activation_ids.append(item["activationId"])
        if not isinstance(item["contributionVersion"], str) or \
                not VERSION_RE.fullmatch(item["contributionVersion"]):
            errors.append("contribution.contributionVersion is not canonical semver")
        if not isinstance(item["artifactDigest"], str) or not DIGEST_RE.fullmatch(item["artifactDigest"]):
            errors.append("contribution.artifactDigest is not 64 lowercase SHA-256 hex")
        if item["admissionGrant"] not in delivery_grants:
            errors.append("contribution.admissionGrant is not a live DELIVERY grant")
        if item["role"] not in roles:
            errors.append("contribution.role is outside the closed enum")
        if item["verificationState"] not in verification_states:
            errors.append("contribution.verificationState is outside the closed enum")
        evidence = item["verificationEvidenceId"]
        if evidence is not None and not _is_nfc_text(evidence):
            errors.append("contribution.verificationEvidenceId is neither null nor canonical text")
        if item["verificationState"] == "VERIFIED" and evidence is None:
            errors.append("VERIFIED contribution lacks verificationEvidenceId")
        if item["admissionGrant"] == "local-development" and item["role"] != "advisory":
            errors.append("local-development contribution is not advisory")
        if item["origin"] not in origins or item["authority"] not in authorities:
            errors.append("contribution origin/authority is outside live C-2")
        if not isinstance(item["parameters"], dict):
            errors.append("contribution.parameters is not a schema-validated closed map")
        else:
            errors += _bounded_parameter_errors(item["parameters"], "contribution.parameters")
    if activation_ids != sorted(activation_ids, key=lambda item: item.encode("utf-8")) or \
            len(activation_ids) != len(set(activation_ids)):
        errors.append("contributions is not sorted unique by activationId")
    return errors


def _grant_parameter_errors(capability, parameters) -> list[str]:
    if not isinstance(parameters, dict):
        return ["capability grant parameters is not a closed map"]
    return _bounded_parameter_errors(parameters, f"{capability}.parameters")


def _capability_grant_errors(values, project_id, c2: dict | None) -> list[str]:
    if not isinstance(values, list):
        return ["capabilityGrants is not an array"]
    errors: list[str] = []
    c2_grant = ((((c2 or {}).get("planIntent") or {})
                 .get("admissionDescriptorV1") or {}).get("capabilityGrant") or {})
    if c2_grant.get("closed") is not True or \
            set(c2_grant.get("required", [])) != CAPABILITY_GRANT_FIELDS or \
            set(c2_grant.get("capability", [])) != GRANT_CAPABILITIES:
        errors.append("live C-2 capability-grant schema is not the exact closed Plan record")
    keys: list[tuple[bytes, int, bytes]] = []
    for item in values:
        if not _closed(item, CAPABILITY_GRANT_FIELDS):
            errors.append("capability grant is not the exact closed AdmissionDescriptor record")
            continue
        if not _is_nfc_text(item["grantId"]) or not IDENT_RE.fullmatch(item["grantId"]):
            errors.append("capability grant grantId is not canonical")
            continue
        if not isinstance(item["grantVersion"], str) or not VERSION_RE.fullmatch(item["grantVersion"]):
            errors.append("capability grant grantVersion is not canonical semanticVersion")
        if item["projectId"] != project_id:
            errors.append("capability grant projectId differs from scope.projectId")
        if item["capability"] not in GRANT_CAPABILITIES:
            errors.append("capability grant capability is outside the closed C-2 vocabulary")
        errors += _grant_parameter_errors(item["capability"], item["parameters"])
        keys.append((item["grantId"].encode("utf-8"), item["grantVersion"].encode("utf-8"),
                     str(item["projectId"]).encode("utf-8")))
    if keys != sorted(keys) or len(keys) != len(set(keys)):
        errors.append("capabilityGrants is not sorted unique by grantId/version/projectId")
    return errors


def _stage_errors(values, c2: dict | None, grant_ids: set[str]) -> list[str]:
    if not isinstance(values, list) or not values:
        return ["workflow.stages is not a non-empty array"]
    errors: list[str] = []
    schemas = (c2 or {}).get("stageSchemas") or {}
    common = schemas.get("common") or {"required": ["kind", "stageId"],
                                       "optional": ["dependsOn", "budget"]}
    kinds = schemas.get("kinds") or {}
    stage_ids: list[str] = []
    for stage in values:
        if not isinstance(stage, dict):
            errors.append("workflow stage is not a map")
            continue
        kind = stage.get("kind")
        spec = kinds.get(kind)
        if not spec:
            errors.append("workflow stage kind is outside live C-2")
            continue
        required = set(common.get("required", [])) | set(spec.get("required", []))
        optional = set(common.get("optional", [])) | set(spec.get("optional", []))
        allowed = required | optional
        if set(stage) - allowed or not required <= set(stage):
            errors.append(f"workflow {kind} stage has unknown or missing fields")
            continue
        sid = stage.get("stageId")
        if not _is_nfc_text(sid) or not IDENT_RE.fullmatch(sid):
            errors.append("workflow.stageId is not a canonical identifier")
        else:
            stage_ids.append(sid)
        if "dependsOn" in stage and not _sorted_unique_text(stage["dependsOn"], nonempty=True):
            errors.append("workflow.dependsOn is not non-empty sorted unique")
        if "budget" in stage:
            budget = stage["budget"]
            if not _closed(budget, {"unit", "limit"}) or \
                    budget.get("unit") not in {"work-units", "milliseconds", "bytes", "items"} or \
                    not _is_uint(budget.get("limit"), (1 << 63) - 1) or budget.get("limit") == 0:
                errors.append(f"workflow.{sid}.budget is not exact StageBudgetV1")
        if kind == "fact-derivation":
            if not _sorted_unique_text(stage.get("relations"), nonempty=True):
                errors.append("fact-derivation relations is not non-empty sorted unique")
            if stage.get("operator") not in set(spec.get("operatorAuthority", [])):
                errors.append("fact-derivation operator is outside live C-2")
            provider = stage.get("providerId")
            if stage.get("operator") in {"semantic-provider", "external-scanner"}:
                if not _is_nfc_text(provider) or not IDENT_RE.fullmatch(provider):
                    errors.append("provider fact-derivation lacks canonical providerId")
            elif provider is not None:
                errors.append("builtin fact-derivation carries providerId")
            if "capabilityGrants" in stage:
                if not _sorted_unique_text(stage["capabilityGrants"], nonempty=True):
                    errors.append("stage capabilityGrants is not sorted unique")
                elif not set(stage["capabilityGrants"]) <= grant_ids:
                    errors.append("stage references a capability grant absent from PlanDescriptor")
        elif kind == "rule-evaluation":
            if not _sorted_unique_text(stage.get("ruleIds"), nonempty=True):
                errors.append("rule-evaluation ruleIds is not non-empty sorted unique")
            if stage.get("requiredness") not in {"required", "optional"}:
                errors.append("rule-evaluation requiredness is outside the closed wire enum")
        elif kind == "policy-evaluation":
            if not _is_nfc_text(stage.get("policyId")) or not IDENT_RE.fullmatch(stage["policyId"]):
                errors.append("policy-evaluation policyId is not canonical")
        elif kind == "probe":
            if not _is_nfc_text(stage.get("probeId")) or not IDENT_RE.fullmatch(stage["probeId"]):
                errors.append("probeId is not canonical")
            if not _sorted_unique_text(stage.get("capabilityGrants"), nonempty=True) or \
                    not set(stage.get("capabilityGrants", [])) <= grant_ids:
                errors.append("probe capabilityGrants is absent, unordered, or unresolved")
    if stage_ids != sorted(stage_ids, key=lambda item: item.encode("utf-8")) or \
            len(stage_ids) != len(set(stage_ids)):
        errors.append("workflow stages is not sorted unique by stageId")
    known = set(stage_ids)
    order = {sid: index for index, sid in enumerate(stage_ids)}
    graph = {stage.get("stageId"): stage.get("dependsOn", [])
             for stage in values if isinstance(stage, dict) and stage.get("stageId") in known}
    if any(dep not in known or dep == sid for sid, deps in graph.items() for dep in deps):
        errors.append("workflow dependency is unknown or self-referential")
    if any(dep in order and order[dep] >= order[sid]
           for sid, deps in graph.items() for dep in deps):
        errors.append("workflow dependency does not reference an earlier stage")
    visiting: set[str] = set()
    visited: set[str] = set()
    def visit(sid):
        if sid in visiting:
            return False
        if sid in visited:
            return True
        visiting.add(sid)
        ok = all(visit(dep) for dep in graph.get(sid, []))
        visiting.remove(sid)
        visited.add(sid)
        return ok
    if not all(visit(sid) for sid in graph):
        errors.append("workflow dependencies contain a cycle")
    return errors


def _typescript_universe_errors(value) -> list[str]:
    errors: list[str] = []
    if not _closed(value, TS_PLAN_UNIVERSE_REQUIRED):
        return ["TypeScript universe is not the exact closed typescript-v1 record"]
    constants = {"schemaVersion": 1, "runtimeArtifactId": "typescript-runtime",
                 "providerArtifactId": "typescript-provider"}
    if any(value[name] != expected for name, expected in constants.items()):
        errors.append("TypeScript universe constant drift")
    digests = {
        "manifestId", "capabilityManifestId", "runtimeArtifactSha256",
        "providerArtifactSha256", "runtimeDescriptorSha256", "providerDescriptorSha256",
        "typescriptCompilerSha256", "typescriptStdlibMerkleRoot",
    }
    if any(not isinstance(value[name], str) or not DIGEST_RE.fullmatch(value[name])
           for name in digests):
        errors.append("TypeScript universe has a noncanonical digest")
    for name in (TS_PLAN_UNIVERSE_REQUIRED - digests - set(constants)):
        if name == "resolvedInputs" or name == "protocolMajor":
            continue
        if not _is_nfc_text(value[name]):
            errors.append(f"TypeScript universe {name} is not canonical text")
    if not _is_uint(value["protocolMajor"], 0xffff) or value["protocolMajor"] == 0:
        errors.append("TypeScript protocolMajor is not positive unsigned-16")
    resolved = value["resolvedInputs"]
    if not _closed(resolved, TS_RESOLVED_UNIVERSE_REQUIRED):
        return errors + ["TypeScript resolvedInputs is not the exact closed record"]
    if not isinstance(resolved["tsconfigGraphHash"], str) or \
            not DIGEST_RE.fullmatch(resolved["tsconfigGraphHash"]):
        errors.append("TypeScript tsconfigGraphHash is not canonical")
    allowed_options = {
        "allowJs", "baseUrl", "exactOptionalPropertyTypes", "jsx", "lib", "module",
        "moduleResolution", "paths", "rootDirs", "skipLibCheck", "strict",
        "strictBindCallApply", "strictFunctionTypes", "strictNullChecks",
        "strictPropertyInitialization", "target", "typeRoots", "types",
        "useUnknownInCatchVariables",
    }
    options = resolved["compilerOptions"]
    if not isinstance(options, dict) or not set(options) <= allowed_options:
        errors.append("TypeScript compilerOptions contains an unknown option")
    else:
        bool_options = {"allowJs", "exactOptionalPropertyTypes", "skipLibCheck", "strict",
                        "strictBindCallApply", "strictFunctionTypes", "strictNullChecks",
                        "strictPropertyInitialization", "useUnknownInCatchVariables"}
        list_options = {"lib", "rootDirs", "typeRoots", "types"}
        text_options = {"baseUrl", "jsx", "module", "moduleResolution", "target"}
        for name, option in options.items():
            if name in bool_options and not isinstance(option, bool):
                errors.append(f"TypeScript compiler option {name} is not boolean")
            elif name in list_options and not _sorted_unique_text(option):
                errors.append(f"TypeScript compiler option {name} is not sorted unique text")
            elif name in text_options and not _is_nfc_text(option):
                errors.append(f"TypeScript compiler option {name} is not canonical text")
            elif name == "paths":
                if not isinstance(option, dict) or any(
                        not _is_nfc_text(key) or not _sorted_unique_text(targets, nonempty=True)
                        for key, targets in option.items()):
                    errors.append("TypeScript compiler option paths is not a canonical map")
    for name in ("programRootFiles", "resolvedNodeModulesLayout"):
        if not _sorted_unique_text(resolved[name], path_values=True):
            errors.append(f"TypeScript {name} is not sorted unique canonical paths")
    if not isinstance(resolved["packageLockIdentity"], str) or \
            not DIGEST_RE.fullmatch(resolved["packageLockIdentity"]):
        errors.append("TypeScript packageLockIdentity is not canonical")
    if not isinstance(resolved["executionCapableResolution"], bool):
        errors.append("TypeScript executionCapableResolution is not boolean")
    return errors


def _rust_universe_errors(value, grants: list[dict]) -> list[str]:
    errors: list[str] = []
    if not _closed(value, RUST_PLAN_UNIVERSE_REQUIRED):
        return ["Rust universe is not the exact closed rust-v1 record"]
    constants = {"schemaVersion": 1, "providerArtifactId": "rust-provider",
                 "toolchainArtifactId": "rust-toolchain-bundle"}
    if any(value[name] != expected for name, expected in constants.items()):
        errors.append("Rust universe constant drift")
    digests = {
        "manifestId", "capabilityManifestId", "providerArtifactSha256",
        "toolchainArtifactSha256", "rustCommitHash", "sysrootDigest",
        "rustcDevLlvmDigest", "providerBinarySha256", "licenseNoticeBundleSha256",
    }
    if any(not isinstance(value[name], str) or not DIGEST_RE.fullmatch(value[name])
           for name in digests):
        errors.append("Rust universe has a noncanonical digest")
    for name in ("providerBuildId", "rustcVersion", "cargoVersion", "hostTriple",
                 "targetTriple", "platformId"):
        if not _is_nfc_text(value[name]):
            errors.append(f"Rust universe {name} is not canonical text")
    if not _is_uint(value["protocolMajor"], 0xffff) or value["protocolMajor"] == 0:
        errors.append("Rust protocolMajor is not positive unsigned-16")
    stdlib = value["standardLibraryComponentDigests"]
    if not isinstance(stdlib, dict) or not stdlib or any(
            not IDENT_RE.fullmatch(key) or not isinstance(digest, str) or not DIGEST_RE.fullmatch(digest)
            for key, digest in stdlib.items()):
        errors.append("Rust standardLibraryComponentDigests is not a non-empty canonical digest map")
    resolved = value["resolvedInputs"]
    if not _closed(resolved, RUST_RESOLVED_UNIVERSE_REQUIRED):
        return errors + ["Rust resolvedInputs is not the exact closed record"]
    if resolved["edition"] not in {"2015", "2018", "2021", "2024"}:
        errors.append("Rust edition is outside the closed enum")
    if not _sorted_unique_text(resolved["cfg"]):
        errors.append("Rust cfg is not sorted unique canonical text")
    if not isinstance(resolved["packageLockIdentity"], str) or \
            not DIGEST_RE.fullmatch(resolved["packageLockIdentity"]):
        errors.append("Rust packageLockIdentity is not canonical")
    packages = resolved["resolvedPackages"]
    package_ids: list[str] = []
    if not isinstance(packages, list):
        errors.append("Rust resolvedPackages is not an array")
    else:
        for package in packages:
            if not _closed(package, {"packageId", "version", "sourceDigest", "features"}):
                errors.append("Rust resolved package is not the exact closed record")
                continue
            if not _is_nfc_text(package["packageId"]) or not IDENT_RE.fullmatch(package["packageId"]):
                errors.append("Rust packageId is not canonical")
            else:
                package_ids.append(package["packageId"])
            if not isinstance(package["version"], str) or not VERSION_RE.fullmatch(package["version"]):
                errors.append("Rust package version is not canonical semver")
            if not isinstance(package["sourceDigest"], str) or not DIGEST_RE.fullmatch(package["sourceDigest"]):
                errors.append("Rust package sourceDigest is not canonical")
            if not _sorted_unique_text(package["features"]):
                errors.append("Rust package features is not sorted unique")
        if package_ids != sorted(package_ids, key=lambda item: item.encode("utf-8")) or \
                len(package_ids) != len(set(package_ids)):
            errors.append("Rust resolvedPackages is not sorted unique by packageId")
    if not isinstance(resolved["rustflags"], list) or \
            not all(_is_nfc_text(item, nonempty=False) for item in resolved["rustflags"]):
        errors.append("Rust rustflags is not an ordered canonical string array")
    if not _sorted_unique_text(resolved["crateRootPaths"], nonempty=True, path_values=True):
        errors.append("Rust crateRootPaths is not sorted unique canonical paths")
    if not isinstance(resolved["executionCapableResolution"], bool):
        errors.append("Rust executionCapableResolution is not boolean")
    build_outputs = resolved["buildScriptOutputs"]
    build_keys: list[tuple[str, str]] = []
    if not isinstance(build_outputs, list):
        errors.append("Rust buildScriptOutputs is not an array")
    else:
        for item in build_outputs:
            if not _closed(item, {"packageId", "cfg", "outputDigest"}):
                errors.append("Rust build-script output is not closed")
                continue
            if not _is_nfc_text(item["packageId"]) or not _is_nfc_text(item["cfg"]) or \
                    not isinstance(item["outputDigest"], str) or not DIGEST_RE.fullmatch(item["outputDigest"]):
                errors.append("Rust build-script output has noncanonical values")
            build_keys.append((item["packageId"], item["cfg"]))
        if build_keys != sorted(build_keys) or len(build_keys) != len(set(build_keys)):
            errors.append("Rust buildScriptOutputs is not sorted unique")
    proc_outputs = resolved["procMacroOutputs"]
    proc_ids: list[str] = []
    if not isinstance(proc_outputs, list):
        errors.append("Rust procMacroOutputs is not an array")
    else:
        for item in proc_outputs:
            if not _closed(item, {"crateId", "outputDigest"}) or \
                    not _is_nfc_text(item.get("crateId")) or \
                    not isinstance(item.get("outputDigest"), str) or \
                    not DIGEST_RE.fullmatch(item["outputDigest"]):
                errors.append("Rust proc-macro output is not the exact canonical record")
                continue
            proc_ids.append(item["crateId"])
        if proc_ids != sorted(proc_ids) or len(proc_ids) != len(set(proc_ids)):
            errors.append("Rust procMacroOutputs is not sorted unique")
    if resolved.get("executionCapableResolution") is False and (build_outputs or proc_outputs):
        errors.append("Rust execution-disabled universe contains repository execution outputs")
    if resolved.get("executionCapableResolution") is True and not any(
            item.get("capability") == "repository-execution" for item in grants):
        errors.append("Rust execution-capable universe lacks repository-execution grant")
    return errors


def _semantic_universe_errors(values, grants: list[dict]) -> list[str]:
    if not isinstance(values, list):
        return ["semanticUniverses is not an array"]
    errors: list[str] = []
    providers: list[str] = []
    for item in values:
        if not _closed(item, {"providerId", "providerVersion", "universe"}):
            errors.append("semantic universe wrapper is not the exact closed record")
            continue
        provider = item["providerId"]
        if provider not in {"rust-semantic", "typescript-semantic"}:
            errors.append("semantic universe providerId is outside the closed P-4 set")
            continue
        providers.append(provider)
        if not isinstance(item["providerVersion"], str) or not VERSION_RE.fullmatch(item["providerVersion"]):
            errors.append("semantic universe providerVersion is not canonical semver")
        if provider == "typescript-semantic":
            errors += _typescript_universe_errors(item["universe"])
        else:
            errors += _rust_universe_errors(item["universe"], grants)
    if providers != sorted(providers, key=lambda item: item.encode("utf-8")) or \
            len(providers) != len(set(providers)):
        errors.append("semanticUniverses is not sorted unique by providerId")
    return errors


def _plan_record_errors(record: dict, c2: dict | None = None,
                        delivery: dict | None = None) -> list[str]:
    errors: list[str] = []
    expected = {name for _, name in PLAN_FIELDS}
    actual = set(record) if isinstance(record, dict) else set()
    if actual != expected:
        errors.append(f"top-level fields are {sorted(actual)}, expected {sorted(expected)}")
        return errors
    if not isinstance(record["snapshotId"], str) or not SNAPSHOT_ID_RE.fullmatch(record["snapshotId"]):
        errors.append("snapshotId is not canonical SNAPSHOT-ID-V1")
    if record["planSchemaMajor"] != 1 or isinstance(record["planSchemaMajor"], bool):
        errors.append("planSchemaMajor is not exactly unsigned integer 1")
    errors += _release_errors(record["release"], delivery)
    if record["invocationProfile"] not in {"ci", "local-interactive"}:
        errors.append("invocationProfile is outside the closed enum")
    errors += _configuration_errors(record["resolvedConfiguration"], record["invocationProfile"])
    errors += _scope_errors(record["scope"])
    errors += _change_spec_errors(record["changeSpec"])
    errors += _contribution_errors(record["contributions"], c2, delivery)
    project_id = record["scope"].get("projectId") if isinstance(record["scope"], dict) else None
    errors += _capability_grant_errors(record["capabilityGrants"], project_id, c2)
    grants = record["capabilityGrants"] if isinstance(record["capabilityGrants"], list) else []
    errors += _semantic_universe_errors(record["semanticUniverses"], grants)
    workflow = record["workflow"]
    if not _closed(workflow, {"stages"}):
        errors.append("workflow is not the exact closed record")
    else:
        grant_ids = {item.get("grantId") for item in grants if isinstance(item, dict)}
        errors += _stage_errors(workflow["stages"], c2, grant_ids)
        universe_ids = {item.get("providerId") for item in record["semanticUniverses"]
                        if isinstance(item, dict)}
        stage_provider_ids = {
            stage.get("providerId")
            for stage in workflow["stages"] if isinstance(stage, dict) and
            stage.get("operator") == "semantic-provider"
        }
        if stage_provider_ids != universe_ids:
            errors.append("semantic-provider stages and semanticUniverses are not an exact set join")
    errors += _budget_errors(record["budgets"])
    if not isinstance(record["planIntentCommitment"], str) or \
            not COMMITMENT_RE.fullmatch(record["planIntentCommitment"]):
        errors.append("planIntentCommitment is not canonical sha256 lowercase hex")
    profiles = {item.get("profile"): set(item.get("semanticProviders", []))
                for item in (((delivery or {}).get("installProfiles") or {}).get("profiles", []))}
    selected = profiles.get(record["release"].get("profileId")
                            if isinstance(record["release"], dict) else None)
    if selected is not None:
        plan_providers = {
            {"rust-semantic": "rust", "typescript-semantic": "typescript"}.get(item.get("providerId"))
            for item in record["semanticUniverses"] if isinstance(item, dict)
        }
        if plan_providers != selected:
            errors.append("semanticUniverses does not exactly match selected DELIVERY profile")
    try:
        _cve1(record)
    except ValueError as exc:
        errors.append(f"CVE1-invalid value: {exc}")
    return errors


def _snapshot_record_errors(record: dict) -> list[str]:
    fields = {"schemaVersion", "projectId", "entries", "vcsState",
              "resolvedConfiguration", "scope", "capture"}
    if not _closed(record, fields):
        return ["SnapshotDescriptorV1 is not the exact closed record"]
    errors: list[str] = []
    if record["schemaVersion"] != 1 or isinstance(record["schemaVersion"], bool):
        errors.append("SnapshotDescriptor schemaVersion is not exactly 1")
    if not PROJECT_ID_RE.fullmatch(record["projectId"] if isinstance(record["projectId"], str) else ""):
        errors.append("SnapshotDescriptor projectId is not canonical PROJECT-ID-V1")
    entries = record["entries"]
    paths: list[str] = []
    if not isinstance(entries, list) or not entries:
        errors.append("SnapshotDescriptor entries is not a non-empty array")
    else:
        for entry in entries:
            if not isinstance(entry, dict):
                errors.append("snapshot entry is not a record")
                continue
            path = entry.get("path")
            if _path_error(path):
                errors.append("snapshot entry path is not canonical project-relative")
            elif path == PROJECT_MARKER_PATH:
                errors.append("snapshot entries includes host ProjectId marker")
            else:
                paths.append(path)
            if entry.get("kind") == "file":
                if not _closed(entry, {"path", "kind", "byteLength", "contentSha256", "executable"}):
                    errors.append("snapshot file entry is not the exact closed record")
                elif not _is_uint(entry["byteLength"]) or \
                        not isinstance(entry["contentSha256"], str) or \
                        not DIGEST_RE.fullmatch(entry["contentSha256"]) or \
                        not isinstance(entry["executable"], bool):
                    errors.append("snapshot file entry has invalid length/digest/executable")
            elif entry.get("kind") == "symlink":
                if not _closed(entry, {"path", "kind", "targetBytesHex"}) or \
                        not isinstance(entry.get("targetBytesHex"), str) or \
                        not re.fullmatch(r"(?:[0-9a-f]{2})*", entry["targetBytesHex"]):
                    errors.append("snapshot symlink entry is not exact lowercase target bytes")
            else:
                errors.append("snapshot entry kind is outside {file,symlink}")
        if paths != sorted(paths, key=lambda item: item.encode("utf-8")) or \
                len(paths) != len(set(paths)):
            errors.append("snapshot entries is not sorted unique by path")
    vcs = record["vcsState"]
    if not _closed(vcs, {"adapterId", "headCommitId", "indexTreeId", "dirtyOverlayPolicy",
                         "untrackedPolicy", "sparseCheckout"}):
        errors.append("snapshot vcsState is not the exact closed record")
    else:
        if not _is_nfc_text(vcs["adapterId"]) or not IDENT_RE.fullmatch(vcs["adapterId"]):
            errors.append("snapshot vcs adapter is not canonical")
        for name in ("headCommitId", "indexTreeId"):
            if vcs[name] is not None and not _is_nfc_text(vcs[name]):
                errors.append(f"snapshot vcs {name} is neither null nor canonical text")
        if vcs["dirtyOverlayPolicy"] not in {"include", "exclude", "reject"} or \
                vcs["untrackedPolicy"] not in {"include", "exclude", "reject"}:
            errors.append("snapshot vcs overlay policy is outside the closed enum")
        sparse = vcs["sparseCheckout"]
        if not _closed(sparse, {"enabled", "patterns"}) or \
                not isinstance(sparse.get("enabled"), bool) or \
                not _sorted_unique_text(sparse.get("patterns", [])) or \
                (not sparse.get("enabled") and sparse.get("patterns") != []):
            errors.append("snapshot sparseCheckout is not the exact canonical record")
    errors += _configuration_errors(record["resolvedConfiguration"], "ci")
    scope = record["scope"]
    if not _closed(scope, {"workspaceUnitIds", "requestedPaths", "changeSpec"}):
        errors.append("snapshot scope is not the exact closed record")
    else:
        if not _sorted_unique_text(scope["workspaceUnitIds"], nonempty=True):
            errors.append("snapshot workspaceUnitIds is not sorted unique")
        if not _sorted_unique_text(scope["requestedPaths"], path_values=True):
            errors.append("snapshot requestedPaths is not sorted unique canonical paths")
        errors += _change_spec_errors(scope["changeSpec"])
    capture = record["capture"]
    expected_capture = {
        "validationMethod": "double-read-stat-and-content",
        "readSetPaths": paths,
        "symlinkPolicy": "record-link-no-follow",
        "pathComparison": "case-sensitive",
        "unicodeNormalization": "NFC-reject-noncanonical",
        "pathSeparator": "/",
    }
    if capture != expected_capture:
        errors.append("snapshot capture policy/read-set is not the exact closed canonical record")
    try:
        _cve1(record)
    except ValueError as exc:
        errors.append(f"SnapshotDescriptor CVE1-invalid value: {exc}")
    return errors


def _snapshot_preimage(record: dict) -> bytes:
    errors = _snapshot_record_errors(record)
    if errors:
        raise ValueError(errors[0])
    return SNAPSHOT_DOMAIN_BYTES + struct.pack(">H", 1) + _cve1(record)


def _snapshot_id(record: dict) -> tuple[bytes, str]:
    preimage = _snapshot_preimage(record)
    return preimage, "snap1:sha256:" + hashlib.sha256(preimage).hexdigest()


def _project_marker_bytes(project_id: str) -> bytes:
    if not PROJECT_ID_RE.fullmatch(project_id):
        raise ValueError("noncanonical PROJECT-ID-V1")
    return PROJECT_MARKER_PREFIX + project_id.encode("ascii") + b"\n"


def _canonical_json(value) -> bytes:
    def validate(item):
        if item is None or isinstance(item, bool):
            return
        if isinstance(item, int) and not isinstance(item, bool):
            if not -(1 << 63) <= item < (1 << 63):
                raise ValueError("integer outside signed-64")
            return
        if isinstance(item, str):
            if unicodedata.normalize("NFC", item) != item:
                raise ValueError("non-NFC string")
            return
        if isinstance(item, list):
            for child in item:
                validate(child)
            return
        if isinstance(item, dict) and all(isinstance(key, str) for key in item):
            for key, child in item.items():
                validate(key)
                validate(child)
            return
        raise ValueError("value is outside opensip-canonical-json-v1")
    validate(value)
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":")).encode("utf-8")


def _plan_intent_commitment(intent: dict) -> str:
    preimage = b"opensip.plan-intent.v1\0" + _canonical_json(intent)
    return "sha256:" + hashlib.sha256(preimage).hexdigest()


def _admission_descriptor_from_intent(intent: dict, c2: dict | None) -> tuple[dict | None, list[str]]:
    errors: list[str] = []
    if not _closed(intent, {"schemaVersion", "intentKind", "analysis"}) or \
            intent.get("schemaVersion") != 1 or intent.get("intentKind") != "analysis":
        return None, ["sourcePlanIntent is not the exact analysis tagged-union arm"]
    analysis = intent["analysis"]
    analysis_fields = {"executionTopology", "workflowIntent", "networkIntent",
                       "remoteComputation", "repositoryExecution", "admissionDescriptor"}
    if not _closed(analysis, analysis_fields):
        return None, ["sourcePlanIntent.analysis is not the exact closed record"]
    plan_intent_schema = (c2 or {}).get("planIntent") or {}
    analysis_schema = plan_intent_schema.get("analysisIntentV1") or {}
    if analysis_schema.get("closed") is not True or \
            set(analysis_schema.get("required", [])) != analysis_fields:
        errors.append("live C-2 AnalysisIntentV1 is not the exact closed record")
    for name, fallback in (
            ("executionTopology", {"one-shot", "resident-single-project", "resident-multi-project"}),
            ("workflowIntent", {"analysis", "repair", "mutation"}),
            ("networkIntent", {"denied", "granted"}),
            ("remoteComputation", {"local-only", "cloud-service", "model-service"})):
        live = set(analysis_schema.get(name, [])) or fallback
        if analysis[name] not in live:
            errors.append(f"sourcePlanIntent.analysis.{name} is outside live C-2")
    repo = analysis["repositoryExecution"]
    repo_schema = analysis_schema.get("repositoryExecution") or {}
    repo_fields = {"buildScripts", "proceduralMacros", "compilerPlugins", "projectHooks"}
    if repo_schema.get("closed") is not True or \
            set(repo_schema.get("required", [])) != repo_fields or \
            set(repo_schema.get("values", [])) != {"disabled", "granted"}:
        errors.append("live C-2 repositoryExecution schema is not exact")
    if not _closed(repo, repo_fields) or \
            any(value not in {"disabled", "granted"} for value in repo.values()):
        errors.append("sourcePlanIntent repositoryExecution is not exact")
    descriptor = analysis["admissionDescriptor"]
    descriptor_fields = {"schemaVersion", "release", "invocationProfile",
                         "resolvedConfiguration", "scope", "changeSpec", "contributions",
                         "capabilityGrants", "workflow", "budgets"}
    admission_schema = plan_intent_schema.get("admissionDescriptorV1") or {}
    if admission_schema.get("closed") is not True or \
            set(admission_schema.get("required", [])) != descriptor_fields or \
            admission_schema.get("schemaVersion") != 1:
        errors.append("live C-2 AdmissionDescriptorV1 is not the exact closed record")
    if not _closed(descriptor, descriptor_fields) or descriptor.get("schemaVersion") != 1:
        errors.append("AdmissionDescriptorV1 is not the exact closed record")
        return None, errors
    return descriptor, errors


def _plan_admission_join_errors(vector: dict, c2: dict | None) -> list[str]:
    intent = vector.get("sourcePlanIntent")
    fixture_id = vector.get("sourcePlanIntentFixtureId")
    if intent is None and fixture_id and c2:
        fixture = next((item for item in c2.get("planIntentFixtures", [])
                        if item.get("id") == fixture_id and item.get("valid") is True), None)
        intent = (fixture or {}).get("intent")
    if not isinstance(intent, dict):
        return ["positive PlanId vector lacks sourcePlanIntent"]
    descriptor, errors = _admission_descriptor_from_intent(intent, c2)
    if descriptor is None:
        return errors
    try:
        plan = _materialize_plan_vector(vector, c2)
    except ValueError as exc:
        return errors + [str(exc)]
    for name in ("release", "invocationProfile", "resolvedConfiguration", "scope", "changeSpec",
                 "contributions", "capabilityGrants", "workflow", "budgets"):
        if plan.get(name) != descriptor.get(name):
            errors.append(f"PlanDescriptor.{name} is not byte-structurally equal to admitted {name}")
    computed = _plan_intent_commitment(intent)
    if vector.get("expectedPlanIntentCommitment") != computed or \
            plan.get("planIntentCommitment") != computed:
        errors.append("PlanDescriptor field 13 is not the recomputed admitted PlanIntent commitment")
    return errors


def _materialize_plan_vector(vector: dict, c2: dict | None) -> dict:
    if isinstance(vector.get("input"), dict):
        return vector["input"]
    construction = vector.get("planInputConstruction")
    fixture_id = vector.get("sourcePlanIntentFixtureId")
    if not isinstance(construction, dict) or not c2 or not fixture_id:
        raise ValueError("positive vector has neither input nor exact fixture construction")
    fixture = next((item for item in c2.get("planIntentFixtures", [])
                    if item.get("id") == fixture_id and item.get("valid") is True), None)
    if fixture is None:
        raise ValueError("positive vector source PlanIntent fixture is absent")
    descriptor, errors = _admission_descriptor_from_intent(fixture.get("intent"), c2)
    if errors or descriptor is None:
        raise ValueError(errors[0] if errors else "source AdmissionDescriptor unavailable")
    required_construction = {"snapshotId", "planSchemaMajor", "semanticUniverses",
                             "planIntentCommitment"}
    if set(construction) != required_construction:
        raise ValueError("planInputConstruction is not the exact four post-admission fields")
    return {
        "snapshotId": construction["snapshotId"],
        "planSchemaMajor": construction["planSchemaMajor"],
        "release": copy.deepcopy(descriptor["release"]),
        "invocationProfile": descriptor["invocationProfile"],
        "resolvedConfiguration": copy.deepcopy(descriptor["resolvedConfiguration"]),
        "scope": copy.deepcopy(descriptor["scope"]),
        "changeSpec": copy.deepcopy(descriptor["changeSpec"]),
        "contributions": copy.deepcopy(descriptor["contributions"]),
        "semanticUniverses": copy.deepcopy(construction["semanticUniverses"]),
        "capabilityGrants": copy.deepcopy(descriptor["capabilityGrants"]),
        "workflow": copy.deepcopy(descriptor["workflow"]),
        "budgets": copy.deepcopy(descriptor["budgets"]),
        "planIntentCommitment": construction["planIntentCommitment"],
    }


def _d9_golden_context_errors(mapping: dict, d9: dict | None,
                              expected_contexts: dict[str, str], label: str) -> list[str]:
    if d9 is None:
        return [f"could not load {D9} for identity termination join"]
    errors: list[str] = []
    contexts = mapping.get("contexts") or {}
    if set(contexts) != set(expected_contexts):
        errors.append(f"{label} D9 context set is not exact")
    goldens = {item.get("id"): item for item in d9.get("goldenCases", [])}
    exit_codes = {item.get("class"): item.get("code") for item in d9.get("exitClasses", [])}
    for context, golden_id in expected_contexts.items():
        row = contexts.get(context) or {}
        golden = goldens.get(golden_id) or {}
        if row.get("referenceGoldenId") != golden_id or \
                row.get("scenarioAxes") != golden.get("scenarioAxes") or \
                row.get("expectedTermination") != golden.get("expectedTermination"):
            errors.append(f"{label} D9 context {context} drifted from live golden {golden_id}")
        expected = row.get("expectedTermination") or {}
        if row.get("exitCode") != exit_codes.get(expected.get("class")):
            errors.append(f"{label} D9 context {context} has wrong numeric exit code")
    return errors


def _d9_context_errors(mapping: dict, d9: dict | None, outcomes: set[str]) -> list[str]:
    expected_contexts = {
        "request-invalid": "pre-admission-invalid-config",
        "request-mismatch": "repair-snapshot-conflict",
        "persisted-corruption": "query-ledger-corrupt",
        "provider-echo": "analysis-provider-protocol-prevents-seal",
    }
    errors = _d9_golden_context_errors(mapping, d9, expected_contexts, "PlanId")
    outcome_map = mapping.get("outcomeContexts") or {}
    if set(outcome_map) != outcomes:
        errors.append("identity D9 outcome set is not total over typed PlanId failures")
    invalid = {
        "PLAN_ID_INVALID_REPRESENTATION", "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION",
        "PLAN_ID_PROFILE_VIOLATION", "PLAN_ID_INPUT_CLASS_VIOLATION",
    }
    for outcome in outcomes:
        expected = {
            "requestInput": "request-invalid" if outcome in invalid else "request-mismatch",
            "persistedOrCache": "persisted-corruption",
            "providerEcho": "provider-echo",
        }
        if outcome_map.get(outcome) != expected:
            errors.append(f"identity D9 mapping for {outcome} is not exact by provenance context")
    if set((mapping.get("provenanceContexts") or {}).get("closedValues", [])) != {
            "requestInput", "persistedOrCache", "providerEcho"}:
        errors.append("identity D9 provenance context vocabulary is not closed")
    return errors


def _project_d9_errors(mapping: dict, d9: dict | None) -> list[str]:
    expected_contexts = {
        "request-invalid": "pre-admission-invalid-config",
        "persisted-corruption": "query-ledger-corrupt",
        "host-io": "pre-admission-host-io-failure",
    }
    errors = _d9_golden_context_errors(mapping, d9, expected_contexts, "ProjectId")
    if mapping.get("outcomeContexts") != PROJECT_D9_OUTCOME_CONTEXTS or \
            set(mapping.get("outcomeContexts") or {}) != PROJECT_OUTCOMES:
        errors.append("ProjectId D9 outcome mapping is not exact and total by provenance")
    provenance = (mapping.get("provenanceContexts") or {}).get("closedValues", [])
    if set(provenance) != {
            "callerOrConfig", "persistedMarkerOrRegistry", "allocationInfrastructure"} or \
            len(provenance) != 3:
        errors.append("ProjectId D9 provenance vocabulary is not exact and closed")
    triggers = mapping.get("allocationTriggers") or {}
    if triggers != {
            "CSPRNG_FAILURE": "allocationInfrastructure",
            "REGISTRY_RESERVATION_IO_FAILURE": "allocationInfrastructure",
            "MARKER_PUBLICATION_IO_FAILURE": "allocationInfrastructure",
            "COLLISION_EXHAUSTION": "allocationInfrastructure"}:
        errors.append("ProjectId allocation failures are not all mapped to host I/O")
    return errors


def _snapshot_d9_errors(mapping: dict, d9: dict | None) -> list[str]:
    expected_contexts = {
        "request-invalid": "pre-admission-invalid-config",
        "request-mismatch": "repair-snapshot-conflict",
        "persisted-corruption": "query-ledger-corrupt",
        "provider-echo": "analysis-provider-protocol-prevents-seal",
    }
    errors = _d9_golden_context_errors(mapping, d9, expected_contexts, "SnapshotId")
    if mapping.get("outcomeContexts") != SNAPSHOT_D9_OUTCOME_CONTEXTS or \
            set(mapping.get("outcomeContexts") or {}) != SNAPSHOT_OUTCOMES:
        errors.append("SnapshotId D9 outcome mapping is not exact and total by provenance")
    provenance = (mapping.get("provenanceContexts") or {}).get("closedValues", [])
    if set(provenance) != {
            "requestOrMutationInput", "persistedLedgerCasOrCache", "providerEcho"} or \
            len(provenance) != 3:
        errors.append("SnapshotId D9 provenance vocabulary is not exact and closed")
    host_io = mapping.get("hostIoBoundary") or {}
    goldens = {item.get("id"): item for item in (d9 or {}).get("goldenCases", [])}
    golden = goldens.get("pre-admission-host-io-failure") or {}
    termination = golden.get("expectedTermination") or {}
    exit_codes = {item.get("class"): item.get("code")
                  for item in (d9 or {}).get("exitClasses", [])}
    if host_io.get("typedHostOutcome") != "SNAPSHOT_INPUT_IO_FAILED" or \
            host_io.get("referenceGoldenId") != "pre-admission-host-io-failure" or \
            host_io.get("faultCause") != golden.get("scenarioAxes", {}).get("faultCause") or \
            host_io.get("terminationClass") != termination.get("class") or \
            host_io.get("errorCode") != termination.get("errorCode") or \
            host_io.get("exitCode") != exit_codes.get(termination.get("class")) or \
            "successful read" not in host_io.get("rule", ""):
        errors.append("Snapshot input I/O is conflated with persisted content corruption")
    return errors


def _plan_preimage(record: dict, c2: dict | None = None,
                   delivery: dict | None = None) -> bytes:
    errors = _plan_record_errors(record, c2, delivery)
    if errors:
        raise ValueError(errors[0])
    result = PLAN_DOMAIN_BYTES + struct.pack(">H", 1) + struct.pack(">H", len(PLAN_FIELDS))
    for tag, name in PLAN_FIELDS:
        encoded = _cve1(record[name])
        result += bytes([tag]) + struct.pack(">I", len(encoded)) + encoded
    return result


def _plan_id(record: dict, c2: dict | None = None,
             delivery: dict | None = None) -> tuple[bytes, str]:
    preimage = _plan_preimage(record, c2, delivery)
    return preimage, "plan1:sha256:" + hashlib.sha256(preimage).hexdigest()


def _replace(record: dict, path: str, value) -> None:
    parts = path.split(".")
    target = record
    for part in parts[:-1]:
        target = target[part]
    target[parts[-1]] = value


def _mutate_pointer(value, mutation: dict) -> None:
    parts = [part.replace("~1", "/").replace("~0", "~")
             for part in mutation.get("path", "").split("/")[1:]]
    target = value
    for part in parts[:-1]:
        target = target[int(part)] if isinstance(target, list) else target[part]
    leaf = parts[-1]
    if mutation["op"] in {"set", "add"}:
        if isinstance(target, list):
            target[int(leaf)] = mutation["value"]
        else:
            target[leaf] = mutation["value"]
    elif mutation["op"] == "reverse":
        selected = target[int(leaf)] if isinstance(target, list) else target[leaf]
        selected.reverse()
    elif mutation["op"] == "duplicate-first":
        selected = target[int(leaf)] if isinstance(target, list) else target[leaf]
        selected.insert(1, copy.deepcopy(selected[0]))
    else:
        raise ValueError("unknown negative mutation operation")


def tm_ids(tm: dict) -> set[str]:
    ids: set[str] = set()
    for k in ("assets", "primaryRisks", "findings", "requiredProperties",
              "conditionalAdversaries", "nonGoals", "trustBoundaries", "residualRisks"):
        v = tm.get(k)
        if isinstance(v, list):
            ids |= {x["id"] for x in v if isinstance(x, dict) and "id" in x}
    return ids


def classify(c: dict) -> dict[str, list[str]]:
    """input name -> [classes it appears in]. A name in two lists is RI-CL-2."""
    out: dict[str, list[str]] = {}
    for cls, block in c["ambientInputClosure"]["classes"].items():
        for item in block["inputs"]:
            name = item["input"] if isinstance(item, dict) else item
            out.setdefault(name, []).append(cls)
    return out


def _check(c: dict, tm: dict | None, c2: dict | None = None,
           delivery: dict | None = None, product: dict | None = None) -> list[str]:
    f: list[str] = []
    c2 = c2 if c2 is not None else load(C2)
    delivery = delivery if delivery is not None else load(DELIVERY)
    product = product if product is not None else load(PRODUCT)
    d9 = load(D9)
    closure = c["ambientInputClosure"]
    members = classify(c)

    # ---- RI-CL-2: exactly one class each ----
    for name, classes in members.items():
        if len(classes) > 1:
            f.append(f"RI-CL-2: ambient input '{name}' is classified {classes} — an input "
                     f"belongs to exactly one class")

    # ---- RI-CL-1: the closure must be total over what it declares ----
    if not all(closure["classes"].get(k, {}).get("inputs")
               for k in ("neutralised", "keyed", "forbidden")):
        f.append("RI-CL-1: the closure is missing a class or a class is empty — "
                 "'neutralise, key, or forbid' must be exhaustive")
    if "totality" not in closure:
        f.append("RI-CL-1: no totality rule is stated, so an unclassified input has no "
                 "declared status")

    # ---- RI-CL-3/4/5 via the fixtures ----
    inplanid_expected = {"neutralised": False, "keyed": True, "forbidden": False}
    rule_for = {"neutralised": "RI-CL-3", "keyed": "RI-CL-4", "forbidden": "RI-CL-5"}
    for fx in c["closureFixtures"]:
        name, cls, in_pid = fx["input"], fx["class"], fx["inPlanId"]
        actual = members.get(name)
        if actual is None:
            f.append(f"{fx['id']}: input '{name}' is not in the declared closure")
            continue
        if cls not in actual:
            f.append(f"{fx['id']}: fixture says '{cls}' but the closure classifies it "
                     f"{actual}")
            continue
        want_rule = rule_for[cls]
        conforms = (in_pid == inplanid_expected[cls])
        if fx["valid"] and not conforms:
            f.append(f"{fx['id']}: expected valid but a '{cls}' input with "
                     f"inPlanId={in_pid} violates {want_rule}")
        elif not fx["valid"]:
            if conforms:
                f.append(f"{fx['id']}: expected REJECTION by {fx.get('violates')} but the "
                         f"assignment conforms")
            elif fx.get("violates") != want_rule:
                f.append(f"{fx['id']}: expected rejection by {fx.get('violates')} but the "
                         f"violated rule is {want_rule} — the fixture proves a different "
                         f"property than it claims")

    # every class must have at least one positive and the set must have a negative
    for cls in ("neutralised", "keyed", "forbidden"):
        if not any(fx["valid"] and fx["class"] == cls for fx in c["closureFixtures"]):
            f.append(f"RI-CL-1: class '{cls}' has no positive fixture — unexercised rule")
        if not any(not fx["valid"] and fx["class"] == cls for fx in c["closureFixtures"]):
            f.append(f"{rule_for[cls]}: class '{cls}' has no negative fixture — the rule "
                     f"is never shown to bite")

    # ---- RI-TM: citations resolve in the LIVE threat model ----
    if tm is None:
        f.append(f"RI-TM: could not load {TM} — citations unverified")
    else:
        live = tm_ids(tm)
        refs = [(d.get("claim", "?"), r) for d in c["decisionDependencies"]
                for r in d.get("refs", [])]
        refs += [(r["id"], r["threatModelRef"]) for r in c["configuration"]["rules"]
                 if "threatModelRef" in r]
        for where, ref in refs:
            if ref not in live:
                f.append(f"RI-TM: {where} cites threat-model id '{ref}', which does not "
                         f"exist in the live model — paper compliance")

    # ---- RI-PR: precedence is a total order with declared PlanId participation ----
    layers = [p["layer"] for p in c["configuration"]["precedence"]]
    if layers != sorted(layers) or len(set(layers)) != len(layers):
        f.append(f"RI-PR: precedence layers {layers} are not a strict total order")
    for p in c["configuration"]["precedence"]:
        if "affectsPlanId" not in p:
            f.append(f"RI-PR: layer {p['layer']} does not declare PlanId participation")

    # ---- RI-SU: both P-4 providers keyed, with the unsound-if-omitted dimensions ----
    per = c["projectModel"]["semanticUniverse"]["perProvider"]
    for prov, dims in REQUIRED_UNIVERSE_DIMS.items():
        if prov not in per:
            f.append(f"RI-SU: P-4 commits a '{prov}' semantic provider with no universe key")
            continue
        blob = " ".join(per[prov]["keyComponents"]).lower()
        for d in dims:
            if d.lower() not in blob:
                f.append(f"RI-SU: {prov} universe key omits '{d}' — two semantically "
                         f"different fact sets could share one identity")
        if "ifIncomplete" not in per[prov]:
            f.append(f"RI-SU: {prov} does not say what happens when the key is incomplete; "
                     f"silence means silently resolving")

    # ---- RI-CT: an unimplementable test must name its blocker ----
    for t in c["conformanceTests"]:
        if not t.get("implementable") and not (t.get("requiresHarness")
                                               or t.get("requiresMechanism")):
            f.append(f"RI-CT: {t['id']} is not implementable and names no blocker")

    # ---- A1-RI-04 final CI/layer-4 product rule ----
    posture = (c.get("configuration") or {}).get("untrackedOverridePosture") or {}
    decision = ((product or {}).get("decisions") or {}).get("A1-RI-04") or {}
    binding = posture.get("bindingProductDecision") or {}
    if decision.get("choice") != "CI_IGNORES_LAYER_4" or \
            "does not load or resolve layer-4" not in decision.get("rule", "").lower():
        f.append("RI-L4: live product disposition does not bind CI_IGNORES_LAYER_4")
    if posture.get("status") != "PRODUCT_DECIDED" or \
            binding.get("choice") != "CI_IGNORES_LAYER_4" or \
            posture.get("productDecisionStillOpen") is not False:
        f.append("RI-L4: resolved-inputs does not carry the final A1-RI-04 product choice")
    layer4 = next((item for item in c["configuration"]["precedence"]
                   if item.get("layer") == 4), {})
    if layer4.get("affectsPlanId") != "local-interactive only" or \
            layer4.get("productDecision") != "CI_IGNORES_LAYER_4":
        f.append("RI-L4: layer 4 is not PlanId-keyed only for local-interactive resolution")
    if not any(t.get("id") == "RI-LAYER4-CI" for t in c.get("conformanceTests", [])):
        f.append("RI-L4: conformanceTests lacks RI-LAYER4-CI covering the product decision")

    # ---- R1-RI-03 analysis vs presentation locale ----
    amb = c.get("ambientInputClosure") or {}
    avp = amb.get("analysisVersusPresentation") or {}
    if not avp:
        f.append("RI-LOCALE: analysisVersusPresentation split missing (R1-RI-03) — "
                 "locale neutralisation must not be over-read as a UX ban")
    else:
        ablob = json.dumps(avp).lower()
        if "presentation" not in ablob and "display" not in ablob and "tty" not in ablob:
            f.append("RI-LOCALE: analysisVersusPresentation does not permit presentation localization")
        if "planid" not in ablob.replace(" ", ""):
            f.append("RI-LOCALE: analysisVersusPresentation does not keep presentation out of PlanId")

    # ---- RI-PRJ: exact persisted PROJECT-ID-V1 lifecycle ----
    project = c.get("projectIdContract") or {}
    project_assurance = project.get("assurance") or {}
    if project.get("id") != "PROJECT-ID-V1" or project.get("status") != "IMPLEMENTABLE":
        f.append("RI-PRJ: PROJECT-ID-V1 is absent or not honestly IMPLEMENTABLE")
    if project_assurance.get("evidenceGrade") != "IMPLEMENTABLE_UNEXECUTED" or \
            project_assurance.get("qualificationEvidenceIds") != [] or \
            project_assurance.get("releaseEvidenceIds") != []:
        f.append("RI-PRJ: ProjectId assurance is greenwashed")
    project_rep = project.get("representation") or {}
    if project_rep.get("raw") != "32 uniformly random bytes from the OS CSPRNG" or \
            project_rep.get("text") != "prj1-<64 lowercase hexadecimal characters>" or \
            project_rep.get("regex") != r"^prj1-[0-9a-f]{64}$":
        f.append("RI-PRJ: ProjectId representation drifted")
    lifecycle = project.get("authorityAndLifecycle") or {}
    if lifecycle.get("allocationOwner") != "orchestration host project resolver" or \
            lifecycle.get("markerPath") != PROJECT_MARKER_PATH or \
            "MUST NOT supply" not in lifecycle.get("callerRule", ""):
        f.append("RI-PRJ: ProjectId owner, marker, or caller boundary is not exact")
    allocation = project.get("allocationAndReservation") or {}
    if allocation.get("maximumCandidates") != 8 or \
            "create-new" not in allocation.get("markerPublication", "").lower() or \
            "atomically reserve" not in allocation.get("registryReservation", "").lower():
        f.append("RI-PRJ: ProjectId allocation/reservation protocol is incomplete")
    movement = project.get("moveCloneAndCollision") or {}
    for term, field in (("preserves ProjectId", "rootMove"),
                        ("new ProjectId", "ordinaryClone"),
                        ("PROJECT_ID_COLLISION", "copiedMarker"),
                        ("explicit fork", "collisionResolution")):
        if term not in movement.get(field, ""):
            f.append(f"RI-PRJ: ProjectId {field} rule omits {term!r}")
    pvectors = project.get("goldenVectors") or {}
    ppositives = {item.get("id"): item for item in pvectors.get("positive", [])}
    allocation_vector = ppositives.get("project-id-v1-allocation") or {}
    try:
        raw = bytes.fromhex(allocation_vector.get("rawBytesHex", ""))
        expected_project = "prj1-" + raw.hex()
        marker = _project_marker_bytes(expected_project)
        if len(raw) != 32 or allocation_vector.get("expectedProjectId") != expected_project or \
                allocation_vector.get("expectedMarkerBytesHex") != marker.hex() or \
                allocation_vector.get("expectedMarkerSha256") != hashlib.sha256(marker).hexdigest():
            f.append("RI-PRJ: allocation/marker positive vector is wrong")
    except (ValueError, TypeError):
        f.append("RI-PRJ: allocation vector is not decodable")
    move_vector = ppositives.get("project-id-v1-root-move") or {}
    if move_vector.get("beforeProjectId") != move_vector.get("afterProjectId") or \
            move_vector.get("registryTransition") != "OLD_ROOT_ABSENT_TO_NEW_ROOT_ATOMIC_REBIND":
        f.append("RI-PRJ: root-move fixture does not preserve identity with exact rebind")
    clone_vector = ppositives.get("project-id-v1-ordinary-clone") or {}
    if clone_vector.get("sourceProjectId") == clone_vector.get("cloneProjectId") or \
            clone_vector.get("cloneMarkerInitiallyPresent") is not False:
        f.append("RI-PRJ: ordinary-clone fixture aliases the source ProjectId")
    project_negatives = {item.get("id"): item.get("expected")
                         for item in pvectors.get("negative", [])}
    expected_project_negatives = {
        "reject-project-id-caller-supplied": "PROJECT_ID_CALLER_SUPPLIED",
        "reject-project-id-uppercase": "PROJECT_ID_INVALID_REPRESENTATION",
        "reject-project-id-copied-marker": "PROJECT_ID_COLLISION",
        "reject-project-id-tracked-marker": "PROJECT_ID_MARKER_TRACKED",
        "reject-project-id-symlink-marker": "PROJECT_ID_MARKER_UNSAFE",
        "reject-project-id-allocation-exhaustion": "PROJECT_ID_ALLOCATION_FAILED",
    }
    if project_negatives != expected_project_negatives:
        f.append("RI-PRJ: ProjectId negative vector set/outcomes are not exact")
    project_verify = project.get("suppliedVersusPersisted") or {}
    expected_project_outcomes = {
        "match": "VERIFIED_PROJECT_ID",
        "malformed": "PROJECT_ID_INVALID_REPRESENTATION",
        "callerSupplied": "PROJECT_ID_CALLER_SUPPLIED",
        "liveRootCollision": "PROJECT_ID_COLLISION",
        "trackedMarker": "PROJECT_ID_MARKER_TRACKED",
        "unsafeMarkerPath": "PROJECT_ID_MARKER_UNSAFE",
        "allocationFailed": "PROJECT_ID_ALLOCATION_FAILED",
    }
    if project_verify.get("suppliedAuthority") is not False or \
            project_verify.get("outcomes") != expected_project_outcomes:
        f.append("RI-PRJ: ProjectId verification outcome vocabulary is not exact")
    f += ["RI-D9: " + item for item in _project_d9_errors(
        project.get("identityOutcomeD9Mapping") or {}, d9)]

    # ---- RI-SNAPSHOT: exact SNAPSHOT-ID-V1 derivation and verification ----
    snapshot = c.get("snapshotIdContract") or {}
    snapshot_assurance = snapshot.get("assurance") or {}
    if snapshot.get("id") != "SNAPSHOT-ID-V1" or snapshot.get("status") != "IMPLEMENTABLE":
        f.append("RI-SNAPSHOT: SNAPSHOT-ID-V1 is absent or not honestly IMPLEMENTABLE")
    if snapshot_assurance.get("evidenceGrade") != "IMPLEMENTABLE_UNEXECUTED" or \
            snapshot_assurance.get("qualificationEvidenceIds") != [] or \
            snapshot_assurance.get("releaseEvidenceIds") != []:
        f.append("RI-SNAPSHOT: SnapshotId assurance is greenwashed")
    snapshot_rep = snapshot.get("identityRepresentation") or {}
    if snapshot_rep.get("digestAlgorithm") != "SHA-256" or \
            snapshot_rep.get("text") != "snap1:sha256:<64 lowercase hexadecimal characters>" or \
            snapshot_rep.get("regex") != r"^snap1:sha256:[0-9a-f]{64}$":
        f.append("RI-SNAPSHOT: SnapshotId representation drifted")
    snapshot_framing = snapshot.get("preimageFraming") or {}
    if snapshot_framing.get("domainBytes") != SNAPSHOT_DOMAIN_DESCRIPTION or \
            snapshot_framing.get("recipeVersion") != 1 or \
            snapshot_framing.get("preimage") != \
            "domainBytes || u16be(recipeVersion=1) || CVE1(SnapshotDescriptorV1)":
        f.append("RI-SNAPSHOT: SnapshotId domain/version/preimage drifted")
    snapshot_schema = snapshot.get("descriptorSchema") or {}
    if snapshot_schema.get("closed") is not True or set(snapshot_schema.get("required", [])) != {
            "schemaVersion", "projectId", "entries", "vcsState", "resolvedConfiguration",
            "scope", "capture"}:
        f.append("RI-SNAPSHOT: SnapshotDescriptorV1 top-level schema is not closed")
    svectors = snapshot.get("goldenVectors") or {}
    snapshot_vector_ids = {item.get("id"): item.get("expectedSnapshotId")
                           for item in svectors.get("positive", [])}
    snapshot_vector_ids.update({item.get("id"): item.get("expectedSnapshotId")
                                for item in svectors.get("transformations", [])})
    spositive = {item.get("id"): item for item in svectors.get("positive", [])}.get(
        "snapshot-id-v1-minimal")
    if not spositive:
        f.append("RI-SNAPSHOT: minimal positive vector is absent")
    else:
        try:
            descriptor = spositive["descriptor"]
            body_map = spositive.get("fileBodiesHex") or {}
            entries = {entry["path"]: entry for entry in descriptor["entries"]}
            for path, body_hex in body_map.items():
                body = bytes.fromhex(body_hex)
                entry = entries[path]
                if entry.get("kind") != "file" or entry.get("byteLength") != len(body) or \
                        entry.get("contentSha256") != hashlib.sha256(body).hexdigest():
                    raise ValueError("file body does not match descriptor")
            preimage, computed = _snapshot_id(descriptor)
            if len(preimage) != spositive.get("expectedPreimageByteLength") or \
                    computed != spositive.get("expectedSnapshotId"):
                f.append("RI-SNAPSHOT: minimal vector byte length or SnapshotId is wrong")
        except (KeyError, TypeError, ValueError, struct.error) as exc:
            f.append(f"RI-SNAPSHOT: minimal vector is invalid: {exc}")
    for transform in svectors.get("transformations", []):
        if not spositive:
            break
        candidate = copy.deepcopy(spositive["descriptor"])
        try:
            for change in transform.get("replaceMany", []):
                _replace(candidate, change["path"], change["value"])
            _, computed = _snapshot_id(candidate)
            if computed != transform.get("expectedSnapshotId") or \
                    (transform.get("mustDifferFromBase") and
                     computed == spositive.get("expectedSnapshotId")):
                f.append(f"RI-SNAPSHOT {transform.get('id')}: transformation oracle is wrong")
        except (KeyError, TypeError, ValueError, struct.error) as exc:
            f.append(f"RI-SNAPSHOT {transform.get('id')}: invalid transformation: {exc}")
    snapshot_negatives = {item.get("id"): item.get("expected")
                          for item in svectors.get("negative", [])}
    expected_snapshot_negatives = {
        "reject-snapshot-unknown-field": "SNAPSHOT_ID_PREIMAGE_SCHEMA_VIOLATION",
        "reject-snapshot-path-traversal": "SNAPSHOT_ID_PREIMAGE_SCHEMA_VIOLATION",
        "reject-snapshot-unsorted-entries": "SNAPSHOT_ID_PREIMAGE_SCHEMA_VIOLATION",
        "reject-snapshot-symlink-follow-shape": "SNAPSHOT_ID_PREIMAGE_SCHEMA_VIOLATION",
        "reject-snapshot-request-id": "SNAPSHOT_ID_PREIMAGE_SCHEMA_VIOLATION",
        "reject-snapshot-supplied-mismatch": "SNAPSHOT_ID_MISMATCH",
    }
    if snapshot_negatives != expected_snapshot_negatives:
        f.append("RI-SNAPSHOT: exact negative vector set/outcomes are incomplete")
    snapshot_verify = snapshot.get("suppliedVersusRecomputed") or {}
    if snapshot_verify.get("suppliedAuthority") is not False or \
            "before PlanId" not in snapshot_verify.get("rule", ""):
        f.append("RI-SNAPSHOT: supplied SnapshotId can become authority without recomputation")
    expected_snapshot_outcomes = {
        "match": "VERIFIED_SNAPSHOT_ID",
        "malformedRepresentation": "SNAPSHOT_ID_INVALID_REPRESENTATION",
        "schemaOrCanonicalizationViolation": "SNAPSHOT_ID_PREIMAGE_SCHEMA_VIOLATION",
        "wellFormedMismatch": "SNAPSHOT_ID_MISMATCH",
    }
    if snapshot_verify.get("outcomes") != expected_snapshot_outcomes:
        f.append("RI-SNAPSHOT: SnapshotId verification outcome vocabulary is not exact")
    f += ["RI-D9: " + item for item in _snapshot_d9_errors(
        snapshot.get("identityOutcomeD9Mapping") or {}, d9)]

    # ---- RI-PID: exact PLAN-ID-V1 derivation and verification contract ----
    pid = c.get("planIdContract") or {}
    assurance = pid.get("assurance") or {}
    if pid.get("id") != "PLAN-ID-V1" or pid.get("status") != "IMPLEMENTABLE":
        f.append("RI-PID: PLAN-ID-V1 is absent or not honestly IMPLEMENTABLE")
    if assurance.get("state") != "IMPLEMENTABLE" or \
            assurance.get("evidenceGrade") != "IMPLEMENTABLE_UNEXECUTED" or \
            assurance.get("qualificationEvidenceIds") != [] or \
            assurance.get("releaseEvidenceIds") != []:
        f.append("RI-PID: PlanId assurance is greenwashed beyond IMPLEMENTABLE_UNEXECUTED")
    rep = pid.get("identityRepresentation") or {}
    if rep.get("digestAlgorithm") != "SHA-256" or \
            rep.get("regex") != r"^plan1:sha256:[0-9a-f]{64}$" or \
            rep.get("text") != "plan1:sha256:<64 lowercase hexadecimal characters>":
        f.append("RI-PID: PlanId digest algorithm or canonical text representation drifted")
    framing = pid.get("preimageFraming") or {}
    if framing.get("domainBytes") != PLAN_DOMAIN_DESCRIPTION or \
            framing.get("recipeVersion") != 1:
        f.append("RI-PID: domain separator or recipe version drifted")
    fields = [(item.get("tag"), item.get("name"))
              for item in pid.get("preimageFields", [])]
    if fields != PLAN_FIELDS:
        f.append(f"RI-PID: preimage fields/tags are {fields}, expected {PLAN_FIELDS}")
    intent_field = next((item for item in pid.get("preimageFields", [])
                         if item.get("name") == "planIntentCommitment"), {})
    exact_intent_recipe = (
        "SHA-256(UTF8(\"opensip.plan-intent.v1\") || 0x00 || "
        "opensip-canonical-json-v1(PlanIntent)); textual form is "
        "sha256:<64 lowercase hex>"
    )
    if intent_field.get("tag") != 13 or intent_field.get("recipe") != exact_intent_recipe:
        f.append("RI-PID: PlanIntent commitment field/recipe drifted from the admission join")
    if "fieldCount=13" not in framing.get("preimage", "") or \
            "thirteen field frames" not in framing.get("preimage", ""):
        f.append("RI-PID: field-count framing is not exactly thirteen")
    encodings = (pid.get("canonicalValueEncoding") or {}).get("encodings") or {}
    expected_encodings = {
        "null": "00",
        "false": "01",
        "true": "02",
        "unsigned-64": "03 || u64be(value)",
        "NFC-UTF8-string": "04 || u32be(byteLength) || UTF8(value)",
        "array": "05 || u32be(elementCount) || CVE1(element[0]) ... CVE1(element[n-1])",
        "string-keyed-map": "06 || u32be(entryCount) || CVE1(key) || CVE1(value), entries sorted by unsigned lexicographic order of NFC UTF-8 key bytes",
        "negative-signed-64": "07 || i64be(value in two's-complement)",
    }
    if encodings != expected_encodings:
        f.append("RI-PID: CVE1 byte grammar drifted from the executable oracle")
    excluded = pid.get("excludedIdentitiesAndInputs") or {}
    if set(excluded.get("identities", [])) != {
            "RequestId", "ExecutionId", "RunId", "FactViewId", "EvidenceDigest", "PlanId"}:
        f.append("RI-PID: correlation/attempt/seal/evidence identities are not exactly excluded")
    if set(excluded.get("inputClasses", [])) != {"neutralised", "forbidden"}:
        f.append("RI-PID: NEUTRALISED/FORBIDDEN ambient classes are not excluded")
    bindings = pid.get("keyedInputBindings", [])
    keyed_names = {
        item["input"] if isinstance(item, dict) else item
        for item in closure["classes"]["keyed"]["inputs"]
    }
    bound_names = {item.get("input") for item in bindings}
    plan_field_names = {name for _, name in PLAN_FIELDS}
    if keyed_names != bound_names or any(item.get("field") not in plan_field_names
                                         for item in bindings):
        f.append("RI-PID: declared KEYED inputs do not map exactly to closed PlanId fields")
    relative = (pid.get("fieldCanonicalization") or {}).get("predicateRelativeFacts", "")
    if "No global fact tier" not in relative or any("tier" in name.lower()
                                                    for _, name in PLAN_FIELDS):
        f.append("RI-PID: PlanId invents or fails to reject a global fact tier")
    descriptor_schema = pid.get("planDescriptorSchema") or {}
    if descriptor_schema.get("closed") is not True or \
            descriptor_schema.get("requiredInTagOrder") != [name for _, name in PLAN_FIELDS] or \
            set((descriptor_schema.get("admissionDescriptorEquality") or {}).get(
                "exactFields", [])) != {
                    "release", "invocationProfile", "resolvedConfiguration", "scope",
                    "changeSpec", "contributions", "capabilityGrants", "workflow", "budgets"} or \
            descriptor_schema.get("budgetKeyPattern") != BUDGET_ID_RE.pattern:
        f.append("RI-PID: recursive PlanDescriptorV1 schema/equality binding is not exact")
    ts_universe = (pid.get("semanticUniverseSchemas") or {}).get("typescript-v1") or {}
    if ts_universe.get("closed") is not True or \
            set(ts_universe.get("required", [])) != TS_PLAN_UNIVERSE_REQUIRED or \
            ts_universe.get("constants") != {
                "schemaVersion": 1,
                "runtimeArtifactId": "typescript-runtime",
                "providerArtifactId": "typescript-provider",
            }:
        f.append("RI-PID: TypeScript PlanId universe identity closure is not exact")
    ts_resolved = ts_universe.get("resolvedInputs") or {}
    if ts_resolved.get("closed") is not True or \
            set(ts_resolved.get("required", [])) != TS_RESOLVED_UNIVERSE_REQUIRED:
        f.append("RI-PID: TypeScript resolved-input universe subobject is not closed")
    expected_ts_digests = {
        "manifestId", "capabilityManifestId", "runtimeArtifactSha256",
        "providerArtifactSha256", "runtimeDescriptorSha256",
        "providerDescriptorSha256", "typescriptCompilerSha256",
        "typescriptStdlibMerkleRoot",
    }
    if set(ts_universe.get("digestFields", [])) != expected_ts_digests or \
            "64 lowercase hexadecimal" not in ts_universe.get("digestRepresentation", ""):
        f.append("RI-PID: TypeScript universe digest fields/representation are not exact")
    rust_universe = (pid.get("semanticUniverseSchemas") or {}).get("rust-v1") or {}
    if rust_universe.get("closed") is not True or \
            set(rust_universe.get("required", [])) != RUST_PLAN_UNIVERSE_REQUIRED or \
            rust_universe.get("constants") != {
                "schemaVersion": 1,
                "providerArtifactId": "rust-provider",
                "toolchainArtifactId": "rust-toolchain-bundle",
            }:
        f.append("RI-PID: Rust PlanId universe identity closure is not exact")
    rust_resolved = rust_universe.get("resolvedInputs") or {}
    if rust_resolved.get("closed") is not True or \
            set(rust_resolved.get("required", [])) != RUST_RESOLVED_UNIVERSE_REQUIRED:
        f.append("RI-PID: Rust resolved-input universe subobject is not closed")
    expected_rust_digests = {
        "manifestId", "capabilityManifestId", "providerArtifactSha256",
        "toolchainArtifactSha256", "rustCommitHash", "sysrootDigest",
        "rustcDevLlvmDigest", "providerBinarySha256", "licenseNoticeBundleSha256",
    }
    if set(rust_universe.get("digestFields", [])) != expected_rust_digests or \
            "64 lowercase hexadecimal" not in rust_universe.get("digestRepresentation", ""):
        f.append("RI-PID: Rust universe digest fields/representation are not exact")
    supplied = pid.get("suppliedVersusRecomputed") or {}
    if supplied.get("suppliedAuthority") is not False or \
            "before cache lookup" not in supplied.get("rule", "") or \
            "planIntentCommitment" not in supplied.get("rule", ""):
        f.append("RI-PID: supplied PlanId can become authority without full recomputation")
    expected_outcomes = {
        "match": "VERIFIED_PLAN_ID",
        "malformedRepresentation": "PLAN_ID_INVALID_REPRESENTATION",
        "schemaOrCanonicalizationViolation": "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION",
        "wellFormedMismatch": "PLAN_ID_MISMATCH",
        "profileViolation": "PLAN_ID_PROFILE_VIOLATION",
        "planIntentMismatch": "PLAN_INTENT_COMMITMENT_MISMATCH",
    }
    if supplied.get("outcomes") != expected_outcomes:
        f.append("RI-PID: supplied-vs-recomputed outcome vocabulary drifted")

    f += ["RI-D9: " + item for item in _d9_context_errors(
        pid.get("identityOutcomeD9Mapping") or {}, d9, PLAN_OUTCOMES)]

    vectors = pid.get("goldenVectors") or {}
    positives = {item.get("id"): item for item in vectors.get("positive", [])}
    base = positives.get("planid-v1-ci-minimal")
    if base is None:
        f.append("RI-PID: exact positive vector planid-v1-ci-minimal is absent")
    else:
        try:
            preimage, computed = _plan_id(base.get("input"), c2, delivery)
            if len(preimage) != base.get("expectedPreimageByteLength") or \
                    computed != base.get("expectedPlanId"):
                f.append("RI-PID: positive vector byte length or expected PlanId is wrong")
            for error in _plan_admission_join_errors(base, c2):
                f.append("RI-JOIN: " + error)
            if base.get("input", {}).get("snapshotId") != \
                    snapshot_vector_ids.get(base.get("snapshotVectorId")):
                f.append("RI-JOIN: minimal PlanId vector does not consume derived SnapshotId")
        except (KeyError, TypeError, ValueError, struct.error) as exc:
            f.append(f"RI-PID: positive vector is not encodable: {exc}")
    full = positives.get("planid-v1-ci-full-providers")
    if full is None:
        f.append("RI-PID: shipping full-profile provider-bearing PlanId vector is absent")
    else:
        try:
            full_input = _materialize_plan_vector(full, c2)
            preimage, computed = _plan_id(full_input, c2, delivery)
            providers = {item.get("providerId") for item in
                         full_input.get("semanticUniverses", [])}
            if providers != {"rust-semantic", "typescript-semantic"} or \
                    full_input.get("release", {}).get("profileId") != "full":
                f.append("RI-PID: provider-bearing vector is not the shipping full profile")
            if len(preimage) != full.get("expectedPreimageByteLength") or \
                    computed != full.get("expectedPlanId"):
                f.append("RI-PID: full-provider vector byte length or PlanId is wrong")
            for error in _plan_admission_join_errors(full, c2):
                f.append("RI-JOIN: full-provider " + error)
            if full_input.get("snapshotId") != \
                    snapshot_vector_ids.get(full.get("snapshotVectorId")):
                f.append("RI-JOIN: full-provider PlanId vector does not consume derived SnapshotId")
        except (KeyError, TypeError, ValueError, struct.error) as exc:
            f.append(f"RI-PID: full-provider vector is not encodable: {exc}")
    if base is not None:
        for vector in vectors.get("transformations", []):
            candidate = copy.deepcopy(base["input"])
            changes = vector.get("replaceMany") or [vector.get("replace")]
            try:
                for change in changes:
                    _replace(candidate, change["path"], change["value"])
                _, computed = _plan_id(candidate, c2, delivery)
                if computed != vector.get("expectedPlanId") or \
                        (vector.get("mustDifferFromBase") and
                         computed == base.get("expectedPlanId")):
                    f.append(f"RI-PID {vector.get('id')}: transformation oracle is wrong")
            except (KeyError, TypeError, ValueError, struct.error) as exc:
                f.append(f"RI-PID {vector.get('id')}: transformation is invalid: {exc}")
    negatives = {item.get("id"): item for item in vectors.get("negative", [])}
    if {item: negatives.get(item, {}).get("expected") for item in REQUIRED_PLAN_NEGATIVES} \
            != REQUIRED_PLAN_NEGATIVES:
        f.append("RI-PID: exact negative-vector set/outcomes are incomplete or drifted")
    mismatch = negatives.get("reject-supplied-planid-mismatch", {})
    if mismatch.get("suppliedPlanId") == mismatch.get("recomputedPlanId") or \
            (base and mismatch.get("recomputedPlanId") != base.get("expectedPlanId")):
        f.append("RI-PID: supplied-mismatch vector does not exercise a real mismatch")
    uppercase = negatives.get("reject-uppercase-planid", {}).get("suppliedPlanId", "")
    if PLAN_ID_RE.fullmatch(uppercase):
        f.append("RI-PID: malformed-representation vector is actually canonical")
    intent_negative = negatives.get("reject-plan-intent-substitution", {})
    if intent_negative.get("attemptRecordPlanIntentCommitment") == \
            intent_negative.get("executionPlanPlanIntentCommitment"):
        f.append("RI-PID: PlanIntent substitution vector does not substitute anything")
    for negative in vectors.get("negative", []):
        mutation = negative.get("mutation")
        if not mutation:
            continue
        source = positives.get(negative.get("base"))
        if not source:
            f.append(f"RI-PID {negative.get('id')}: negative references unknown base")
            continue
        candidate_vector = copy.deepcopy(source)
        try:
            candidate_input = _materialize_plan_vector(candidate_vector, c2)
            candidate_vector["input"] = candidate_input
            _mutate_pointer(candidate_input, mutation)
            schema_errors = _plan_record_errors(candidate_input, c2, delivery)
            join_errors = _plan_admission_join_errors(candidate_vector, c2)
            expected = negative.get("expected")
            if expected == "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION" and not schema_errors:
                f.append(f"RI-PID {negative.get('id')}: malformed nested descriptor was accepted")
            if expected == "PLAN_INTENT_COMMITMENT_MISMATCH" and not join_errors:
                f.append(f"RI-JOIN {negative.get('id')}: admitted descriptor substitution was accepted")
        except (KeyError, IndexError, TypeError, ValueError) as exc:
            f.append(f"RI-PID {negative.get('id')}: negative mutation itself is invalid: {exc}")

    # ---- RI-JOIN: live lifecycle, delivery and product contracts ----
    if c2 is None:
        f.append(f"RI-JOIN: could not load {C2}")
    else:
        levels = {item.get("level"): item
                  for item in c2.get("theAdmissionBoundary", {}).get("levels", [])}
        allocated = set(levels.get("snapshot-binding", {}).get("allocates", []))
        if not {"SnapshotId", "PlanId"} <= allocated or \
                "SnapshotId" not in c2.get("executionPlan", {}).get("boundTo", "") or \
                "PlanId" not in c2.get("executionPlan", {}).get("boundTo", ""):
            f.append("RI-JOIN: live C-2 no longer allocates/binds SnapshotId and PlanId together")
        project_pattern = (((c2.get("planIntent") or {}).get("schema") or {})
                           .get("projectId") or {}).get("canonicalTextPattern")
        c2_blob = json.dumps(c2, sort_keys=True)
        if project_pattern not in {None, r"^prj1-[0-9a-f]{64}$"} or \
                "PROJECT-ID-V1" not in c2_blob:
            f.append("RI-JOIN: live C-2 does not consume canonical PROJECT-ID-V1")
        if not all(term in c2_blob for term in (
                "planIntentCommitment", "opensip.plan-intent.v1", "AttemptRecord", "ExecutionPlan")):
            f.append("RI-JOIN: live C-2 lacks the canonical PlanIntent commitment lifecycle join")
        intent_vectors = {item.get("id"): item for item in c2.get("planIntentFixtures", [])}
        minimal_intent = intent_vectors.get("valid-minimal-analysis-intent", {})
        exact_minimal_commitment = minimal_intent.get("expectedCommitment")
        try:
            computed_minimal_commitment = _plan_intent_commitment(minimal_intent.get("intent"))
        except (TypeError, ValueError):
            computed_minimal_commitment = None
        if not COMMITMENT_RE.fullmatch(exact_minimal_commitment or "") or \
                exact_minimal_commitment != computed_minimal_commitment:
            f.append("RI-JOIN: C-2 minimal PlanIntent commitment oracle drifted")
        if base:
            plan_input = base.get("input", {})
            intent = minimal_intent.get("intent", {})
            descriptor, descriptor_errors = _admission_descriptor_from_intent(intent, c2)
            equality_fields = ("release", "invocationProfile", "resolvedConfiguration", "scope",
                               "changeSpec", "contributions", "capabilityGrants", "workflow", "budgets")
            if descriptor_errors or descriptor is None or \
                    plan_input.get("planIntentCommitment") != exact_minimal_commitment or \
                    any(plan_input.get(name) != descriptor.get(name) for name in equality_fields):
                f.append("RI-JOIN: PLAN-ID-V1 positive vector is not the frozen C-2 minimal intent")
            if base.get("sourcePlanIntentFixtureId") != "valid-minimal-analysis-intent":
                f.append("RI-JOIN: base PlanId sourcePlanIntent is not the live C-2 minimal fixture")
    if delivery is None:
        f.append(f"RI-JOIN: could not load {DELIVERY}")
    else:
        release_schema = delivery.get("releaseManifestSchema", {})
        manifest_required = set(release_schema.get("ReleaseManifestV1", {}).get("required", []))
        profile_required = set(release_schema.get("ProfileEntry", {}).get("required", []))
        if "manifestId" not in manifest_required or \
                not {"profileId", "capabilityManifestId"} <= profile_required:
            f.append("RI-JOIN: DELIVERY no longer supplies the three release identity fields")
        grants = delivery.get("provenancePolicy", {}).get("grants", [])
        if not grants or any(item.get("planIdVisible") is not True for item in grants):
            f.append("RI-JOIN: a DELIVERY contribution grant is not PlanId-visible")
        ts_delivery = delivery.get("typescriptSemanticSubstrate") or {}
        packaging = ts_delivery.get("packaging") or {}
        identity = ts_delivery.get("identity") or {}
        if packaging.get("runtimeArtifactId") != "typescript-runtime" or \
                packaging.get("providerArtifactId") != "typescript-provider" or \
                set(identity.get("handshakeRequired", [])) != TS_DELIVERY_HANDSHAKE_REQUIRED:
            f.append("RI-JOIN: DELIVERY TypeScript artifacts/handshake drifted from PlanId closure")
        plan_rule = identity.get("planIdRule", "")
        for term in ("manifestId", "capabilityManifestId", "artifact IDs and sha256",
                     "protocolMajor", "Node/V8/modules ABI", "stdlib Merkle root",
                     "resolved-inputs TypeScript semantic-universe"):
            if term not in plan_rule:
                f.append(f"RI-JOIN: DELIVERY TypeScript PlanId rule omits {term}")
        rust_delivery = delivery.get("rustSemanticSubstrate") or {}
        rust_protocol = rust_delivery.get("providerProtocol") or {}
        if rust_delivery.get("decision") != "bundled-pinned-rustc-driver-sidecar" or \
                rust_protocol.get("major") != 1 or \
                set(rust_protocol.get("handshakeRequired", [])) != RUST_DELIVERY_HANDSHAKE_REQUIRED:
            f.append("RI-JOIN: DELIVERY Rust sidecar/protocol drifted from rust-v1 universe")
        toolchain_blob = " ".join(rust_delivery.get("toolchainIdentity", [])).lower()
        for term in ("rust source commit", "rustc verbose version", "cargo version",
                     "rustc-dev and llvm", "target triple and sysroot", "standard-library",
                     "provider binary", "license/notice"):
            if term not in toolchain_blob:
                f.append(f"RI-JOIN: DELIVERY Rust toolchain identity omits {term}")

    if tm is not None:
        storage_project = (tm.get("storageNamespace") or {}).get("projectId") or {}
        if storage_project.get("canonicalTextPattern") != r"^prj1-[0-9a-f]{64}$" or \
                "PROJECT-ID-V1" not in storage_project.get("logicalIdentityOwner", "") or \
                "projectIdContract" not in storage_project.get("admissionJoin", ""):
            f.append("RI-JOIN: live storage namespace does not consume PROJECT-ID-V1")

    for test_id in {"RI-PROJECTID-01", "RI-SNAPSHOTID-01", "RI-SNAPSHOTID-02",
                    "RI-PLANID-01", "RI-PLANID-02", "RI-PLANID-03", "RI-PLANID-04"}:
        if not any(item.get("id") == test_id and item.get("implementable") is True
                   for item in c.get("conformanceTests", [])):
            f.append(f"RI-PID: conformance test {test_id} is absent or not implementable")

    return f


def check(c: object, tm: dict | None, c2: dict | None = None,
          delivery: dict | None = None, product: dict | None = None) -> list[str]:
    """Total contract boundary for malformed but parsed JSON input."""
    if not isinstance(c, dict) or not c:
        return ["RI-TOTALITY-ROOT: contract root must be a non-empty object"]
    closure = c.get("ambientInputClosure")
    if not isinstance(closure, dict) or not isinstance(closure.get("classes"), dict):
        return ["RI-TOTALITY-SHAPE: ambientInputClosure.classes must be an object"]
    try:
        return _check(c, tm, c2, delivery, product)
    except MALFORMED_SHAPE_EXCEPTIONS as exc:
        return [f"RI-TOTALITY-EXCEPTION: malformed contract shape "
                f"({type(exc).__name__})"]


# --------------------------------------------------------------------------
def _m_key_a_constant(c):
    for fx in c["closureFixtures"]:
        if fx["id"] == "reject-neutralised-in-planid":
            fx["valid"] = True

def _m_unkeyed_analysis_input(c):
    for fx in c["closureFixtures"]:
        if fx["id"] == "reject-keyed-absent-from-planid":
            fx["valid"] = True

def _m_record_the_forbidden(c):
    for fx in c["closureFixtures"]:
        if fx["id"] == "reject-forbidden-in-planid":
            fx["valid"] = True

def _m_double_classify(c):
    c["ambientInputClosure"]["classes"]["keyed"]["inputs"].append("wall clock")

def _m_drop_totality(c):
    del c["ambientInputClosure"]["totality"]

def _m_stale_tm_citation(c):
    c["configuration"]["rules"][0]["threatModelRef"] = "F2"

def _m_drop_rust_cfg(c):
    per = c["projectModel"]["semanticUniverse"]["perProvider"]["rust"]
    per["keyComponents"] = [k for k in per["keyComponents"] if "cfg" not in k.lower()]

def _m_drop_ts_provider(c):
    del c["projectModel"]["semanticUniverse"]["perProvider"]["typescript"]

def _m_silent_incomplete_universe(c):
    del c["projectModel"]["semanticUniverse"]["perProvider"]["rust"]["ifIncomplete"]

def _m_unblocked_unimplementable(c):
    for t in c["conformanceTests"]:
        if t["id"] == "RI-18":
            del t["requiresHarness"]

def _m_drop_layer4_provisional(c):
    cfg = c.get("configuration") or {}
    if "untrackedOverridePosture" in cfg:
        del cfg["untrackedOverridePosture"]
    c["conformanceTests"] = [t for t in c.get("conformanceTests", []) if t.get("id") != "RI-LAYER4-CI"]

def _m_drop_locale_split(c):
    amb = c.get("ambientInputClosure") or {}
    amb.pop("analysisVersusPresentation", None)

def _m_change_plan_domain(c):
    c["planIdContract"]["preimageFraming"]["domainBytes"] = \
        "UTF-8 bytes for opensip.plan-id.v2 followed by NUL"

def _m_change_plan_recipe_version(c):
    c["planIdContract"]["preimageFraming"]["recipeVersion"] = 2

def _m_drop_plan_intent_field(c):
    c["planIdContract"]["preimageFields"] = [
        item for item in c["planIdContract"]["preimageFields"]
        if item["name"] != "planIntentCommitment"
    ]

def _m_swap_plan_field_tags(c):
    fields = c["planIdContract"]["preimageFields"]
    fields[0]["tag"], fields[1]["tag"] = fields[1]["tag"], fields[0]["tag"]

def _m_change_plan_digest(c):
    c["planIdContract"]["identityRepresentation"]["digestAlgorithm"] = "BLAKE3"

def _m_change_cve_map_order(c):
    c["planIdContract"]["canonicalValueEncoding"]["encodings"]["string-keyed-map"] = \
        "06 || insertion-order entries"

def _m_corrupt_plan_vector(c):
    c["planIdContract"]["goldenVectors"]["positive"][0]["expectedPlanId"] = \
        "plan1:sha256:" + "0" * 64

def _m_trust_supplied_plan_id(c):
    c["planIdContract"]["suppliedVersusRecomputed"]["suppliedAuthority"] = True

def _m_drop_keyed_binding(c):
    c["planIdContract"]["keyedInputBindings"].pop()

def _m_allow_execution_id(c):
    c["planIdContract"]["excludedIdentitiesAndInputs"]["identities"].remove("ExecutionId")

def _m_drift_plan_intent_recipe(c):
    for field in c["planIdContract"]["preimageFields"]:
        if field["name"] == "planIntentCommitment":
            field["recipe"] = "SHA-256 of implementation-defined PlanIntent bytes"

def _m_greenwash_plan_id(c):
    assurance = c["planIdContract"]["assurance"]
    assurance["state"] = "DEMONSTRATED"
    assurance["evidenceGrade"] = "DEMONSTRATED"

def _m_drop_ts_runtime_identity(c):
    required = c["planIdContract"]["semanticUniverseSchemas"]["typescript-v1"]["required"]
    required.remove("modulesAbi")

def _m_arbitrary_rust_universe(c):
    full = next(item for item in c["planIdContract"]["goldenVectors"]["positive"]
                if item["id"] == "planid-v1-ci-full-providers")
    full["planInputConstruction"]["semanticUniverses"][0]["universe"] = {"arbitrary": True}

def _m_unsorted_plan_scope(c):
    base = c["planIdContract"]["goldenVectors"]["positive"][0]
    base["input"]["scope"]["workspaceUnitIds"] = ["unit:z", "unit:a"]

def _m_substitute_admitted_artifact(c):
    base = c["planIdContract"]["goldenVectors"]["positive"][0]
    base["input"]["contributions"][0]["artifactDigest"] = "a" * 64

def _m_drift_plan_d9(c):
    row = c["planIdContract"]["identityOutcomeD9Mapping"]["contexts"]["request-invalid"]
    row["scenarioAxes"]["rejectionCause"] = "precondition-failed"
    row["expectedTermination"]["errorCode"] = "REQUEST.PRECONDITION_FAILED"

def _m_drop_rust_schema_field(c):
    required = c["planIdContract"]["semanticUniverseSchemas"]["rust-v1"] \
        ["resolvedInputs"]["required"]
    required.remove("cfg")

def _m_change_snapshot_domain(c):
    c["snapshotIdContract"]["preimageFraming"]["domainBytes"] = "opensip.snapshot-id.v2"

def _m_corrupt_snapshot_vector(c):
    c["snapshotIdContract"]["goldenVectors"]["positive"][0]["expectedSnapshotId"] = \
        "snap1:sha256:" + "0" * 64

def _m_allow_snapshot_marker(c):
    vector = c["snapshotIdContract"]["goldenVectors"]["positive"][0]
    vector["descriptor"]["entries"][0]["path"] = PROJECT_MARKER_PATH
    vector["descriptor"]["scope"]["requestedPaths"] = [PROJECT_MARKER_PATH]
    vector["descriptor"]["capture"]["readSetPaths"] = [PROJECT_MARKER_PATH]
    body = vector["fileBodiesHex"].pop("src/lib.rs")
    vector["fileBodiesHex"][PROJECT_MARKER_PATH] = body

def _m_path_derived_project_id(c):
    c["projectIdContract"]["representation"]["raw"] = "SHA-256 of canonical root path"

def _m_clone_aliases_project(c):
    vector = next(item for item in c["projectIdContract"]["goldenVectors"]["positive"]
                  if item["id"] == "project-id-v1-ordinary-clone")
    vector["cloneProjectId"] = vector["sourceProjectId"]

def _m_drop_project_move_rule(c):
    c["projectIdContract"]["moveCloneAndCollision"]["rootMove"] = "Implementation-defined."

def _m_accept_invalid_budget(c):
    full = next(item for item in c["planIdContract"]["goldenVectors"]["positive"]
                if item["id"] == "planid-v1-ci-full-providers")
    full["planInputConstruction"]["planIntentCommitment"] = full["expectedPlanIntentCommitment"]
    # The base vector is independently stored, so exercise recursive validation directly.
    base = c["planIdContract"]["goldenVectors"]["positive"][0]
    base["input"]["budgets"] = {"analysis.seconds": 1}


def _m_treat_project_marker_corruption_as_config(c):
    mapping = c["projectIdContract"]["identityOutcomeD9Mapping"]["outcomeContexts"]
    mapping["PROJECT_ID_COLLISION"]["persistedMarkerOrRegistry"] = "request-invalid"


def _m_invent_project_allocation_error(c):
    row = c["projectIdContract"]["identityOutcomeD9Mapping"]["contexts"]["host-io"]
    row["expectedTermination"]["errorCode"] = "PROJECT.ALLOCATION_FAILED"


def _m_treat_snapshot_cas_corruption_as_config(c):
    mapping = c["snapshotIdContract"]["identityOutcomeD9Mapping"]["outcomeContexts"]
    mapping["SNAPSHOT_ID_MISMATCH"]["persistedLedgerCasOrCache"] = "request-invalid"


def _m_treat_snapshot_io_as_corruption(c):
    boundary = c["snapshotIdContract"]["identityOutcomeD9Mapping"]["hostIoBoundary"]
    boundary["faultCause"] = "ledger-corrupt"
    boundary["errorCode"] = "LEDGER.CORRUPT"


def _m_prefix_semantic_provider_id(c):
    full = next(item for item in c["planIdContract"]["goldenVectors"]["positive"]
                if item["id"] == "planid-v1-ci-full-providers")
    full["planInputConstruction"]["semanticUniverses"][0]["providerId"] = \
        "provider.rust-semantic"


MUTATIONS = [
    ("key a neutralised constant (RI-CL-3)", _m_key_a_constant),
    ("leave an analysis-affecting input out of PlanId (RI-CL-4)", _m_unkeyed_analysis_input),
    ("record a forbidden input instead of refusing it (RI-CL-5)", _m_record_the_forbidden),
    ("classify one input twice (RI-CL-2)", _m_double_classify),
    ("drop the totality rule (RI-CL-1)", _m_drop_totality),
    ("cite a superseded threat-model id (A1-RI-02 / RI-TM)", _m_stale_tm_citation),
    ("drop cfg from the Rust universe key (A1-RI-01 / RI-SU)", _m_drop_rust_cfg),
    ("drop the TypeScript universe entirely (A1-RI-05 / RI-SU)", _m_drop_ts_provider),
    ("let an incomplete universe resolve silently (RI-SU)", _m_silent_incomplete_universe),
    ("mark a test unimplementable with no blocker (RI-CT)", _m_unblocked_unimplementable),
    ("drop final layer-4 product binding (A1-RI-04)", _m_drop_layer4_provisional),
    ("drop analysis-vs-presentation locale split (R1-RI-03)", _m_drop_locale_split),
    ("change PlanId domain separator (IP-R4-01)", _m_change_plan_domain),
    ("change PlanId recipe version without a new recipe (IP-R4-01)",
     _m_change_plan_recipe_version),
    ("drop PlanIntent commitment from PlanId (IP-R4-01 / admission join)",
     _m_drop_plan_intent_field),
    ("swap PlanId field tags (IP-R4-01)", _m_swap_plan_field_tags),
    ("change PlanId digest algorithm (IP-R4-01)", _m_change_plan_digest),
    ("make CVE1 maps insertion-ordered (IP-R4-01)", _m_change_cve_map_order),
    ("corrupt the exact PlanId golden (IP-R4-01)", _m_corrupt_plan_vector),
    ("trust a caller-supplied PlanId (IP-R4-01)", _m_trust_supplied_plan_id),
    ("leave one KEYED input unmapped (IP-R4-01)", _m_drop_keyed_binding),
    ("allow ExecutionId into PlanId (IP-R4-01)", _m_allow_execution_id),
    ("make PlanIntent commitment bytes implementation-defined (IP-R4-01)",
     _m_drift_plan_intent_recipe),
    ("claim PlanId demonstrated without product evidence (FINAL-02)", _m_greenwash_plan_id),
    ("drop Node modules ABI from the TypeScript PlanId universe (IP-R4-03 join)",
     _m_drop_ts_runtime_identity),
    ("accept an arbitrary Rust universe (R6-IP01-01)", _m_arbitrary_rust_universe),
    ("accept noncanonical nested Plan scope order (R6-IP01-03)", _m_unsorted_plan_scope),
    ("substitute a fully admitted artifact record (R7-C2-04)", _m_substitute_admitted_artifact),
    ("map identity outcomes to a different D9 cause/code (R6-XID-04)", _m_drift_plan_d9),
    ("drop a Rust resolved-universe field (R6-IP01-01)", _m_drop_rust_schema_field),
    ("change SnapshotId domain separator (R6-IP01-02)", _m_change_snapshot_domain),
    ("corrupt exact SnapshotId vector (R6-IP01-02)", _m_corrupt_snapshot_vector),
    ("allow ProjectId marker into SnapshotId (R6-IP01-02/R7-SN-01)", _m_allow_snapshot_marker),
    ("make ProjectId path-derived (R7-SN-01)", _m_path_derived_project_id),
    ("let an ordinary clone alias ProjectId (R7-SN-01)", _m_clone_aliases_project),
    ("drop ProjectId root-move semantics (R7-SN-01)", _m_drop_project_move_rule),
    ("accept a unitless Plan budget (R6-IP01-03)", _m_accept_invalid_budget),
    ("treat persisted ProjectId collision as caller config (R6-XID-04)",
     _m_treat_project_marker_corruption_as_config),
    ("invent a ProjectId allocation error code (R6-XID-04)",
     _m_invent_project_allocation_error),
    ("treat persisted Snapshot/CAS corruption as caller config (R6-XID-04)",
     _m_treat_snapshot_cas_corruption_as_config),
    ("treat Snapshot read I/O as content corruption (R6-XID-04)",
     _m_treat_snapshot_io_as_corruption),
    ("alias a canonical semantic provider with provider.* (R5R-DLTS-05)",
     _m_prefix_semantic_provider_id),
]


def selftest(base: dict, tm) -> int:
    pre = check(base, tm)
    if pre:
        print(f"REFUSING to self-test: the base contract has {len(pre)} finding(s), so "
              f"every mutation would be masked by them.")
        for x in pre[:5]:
            print("  -", x)
        return 1
    print("mutation self-test — each row must be REJECTED\n")
    escaped = 0
    for name, root in TOTALITY_ROOT_CASES:
        findings = check(copy.deepcopy(root), tm)
        if not findings:
            escaped += 1
        print(f"  {'reject' if findings else 'ESCAPE':>6}  parsed-JSON root {name}")
        print(f"          {findings[0] if findings else 'NO FINDING — root survived'}")
    for name, mut in MUTATIONS:
        c = copy.deepcopy(base)
        mut(c)
        findings = check(c, tm)
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
    tmp = HERE / TM
    tm = json.loads(tmp.read_text()) if tmp.exists() else None
    if "--selftest" in sys.argv:
        return selftest(c, tm)
    f = check(c, tm)
    if not f:
        n = sum(len(b["inputs"]) for b in c["ambientInputClosure"]["classes"].values())
        impl = sum(1 for t in c["conformanceTests"] if t.get("implementable"))
        print(f"resolved-inputs OK — {p.name}, {n} ambient inputs classified, "
              f"{len(c['closureFixtures'])} closure fixtures, RI-CL-1..5 / RI-TM / RI-PR / "
              f"RI-SU / RI-CT / RI-PRJ / RI-SNAPSHOT / RI-PID / RI-D9 / RI-JOIN clean")
        print(f"  citations/joins cross-checked against {TM}, {C2}, {DELIVERY}, {PRODUCT}, {D9}")
        print("  PROJECT-ID-V1 and SNAPSHOT-ID-V1: exact custody/recipe vectors, "
              "provenance-sensitive D9 mapping, IMPLEMENTABLE_UNEXECUTED")
        print(f"  PLAN-ID-V1: {len(c['planIdContract']['preimageFields'])} framed fields, "
              f"{len(c['planIdContract']['goldenVectors']['negative'])} negative vectors, "
              f"IMPLEMENTABLE_UNEXECUTED")
        print(f"  {impl}/{len(c['conformanceTests'])} conformance tests implementable")
        return 0
    print(f"{len(f)} finding(s) in {p.name}:")
    for x in f:
        print("  -", x)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
