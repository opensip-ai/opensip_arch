"""Construct independently authored complete Run graphs from published schemas.

Synthetic trusted observations: we invent repository bytes and compiler/context
descriptors as a reconstruction host would after native admission. This is not
native compiler execution (future qualification).
"""
from __future__ import annotations

import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from . import canonical, cap_admit, clone_body, h, order, store

KIT = Path("/tmp/opensip-design-corrections/consumer-b.v13/subject")
REL_BYTES = (KIT / "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json").read_bytes()
REL_DIGEST = hashlib.sha256(REL_BYTES).hexdigest()
NAT_BYTES = (KIT / "docs/coop/design-corrections/native/native-evidence.schemas.v2.json").read_bytes()
NAT_DIGEST = hashlib.sha256(NAT_BYTES).hexdigest()
POL_V2_BYTES = (KIT / "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json").read_bytes()
POL_V2_DIGEST = hashlib.sha256(POL_V2_BYTES).hexdigest()
POL_V1_BYTES = (KIT / "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json").read_bytes()
POL_V1_DIGEST = hashlib.sha256(POL_V1_BYTES).hexdigest()
IMP_BYTES = (KIT / "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json").read_bytes()
IMP_DIGEST = hashlib.sha256(IMP_BYTES).hexdigest()
COMMON_BYTES = (KIT / "docs/coop/design-corrections/workflows/schemas/common.schema.json").read_bytes()
COMMON_DIGEST = hashlib.sha256(COMMON_BYTES).hexdigest()


def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def blob_row(path: str, data: bytes) -> dict:
    return {"path": path, "sha256": sha(data), "bytes": len(data)}


def project_id() -> str:
    return "prj1-" + sha(b"consumer-b.v13.synthetic.project")


def hex64(label: str) -> str:
    return sha(label.encode("utf-8"))


def closed_world_inapplicable() -> dict:
    return {
        "exportsClosed": "unknown",
        "entryPointsRecognized": "none",
        "nonliteralLoading": "none",
        "externalConsumers": "unknown",
        "dynamicDispatch": "not-applicable",
        "reasons": ["inventory-rung"],
        "deadCodeRepairEligible": False,
    }


def resolution_not_applicable() -> dict:
    return {
        "state": "not-applicable",
        "attempted": False,
        "examinedExhaustive": True,
        "stageTerminal": "complete",
        "unresolvedEdgeCount": 0,
        "unresolvedEdgeClasses": [],
    }


def coverage_entry(relation: str, resolution: str, scope_commit: str, subject_count: int, *, coverage="complete", deficiency=None, native_cause=None, exhaustive=True, state="not-applicable", attempted=False) -> dict:
    return {
        "schemaVersion": 3,
        "key": {
            "relation": relation,
            "resolution": resolution,
            "sourceUniverse": None,  # filled by caller
            "targetUniverse": None,
            "subjectScopeCommitment": scope_commit,
        },
        "entry": {
            "relation": relation,
            "resolution": resolution,
            "coverage": coverage,
            "examinedUniverse": {
                "subjectScopeCommitment": scope_commit,
                "subjectCount": subject_count,
            },
            "resolutionCompleteness": {
                "state": state,
                "attempted": attempted,
                "examinedExhaustive": exhaustive,
                "stageTerminal": "complete" if coverage == "complete" else "unavailable",
                "unresolvedEdgeCount": 0,
                "unresolvedEdgeClasses": [],
            },
            "closedWorld": closed_world_inapplicable(),
            "derivationKinds": [],
            "confidenceMillionths": 1000000,
            "deficiency": deficiency,
            "nativeCause": native_cause,
        },
    }


def make_closure(kind: str, platform: str, files: dict[str, bytes], version: str = "1.0.0", protocol_major: int = 3) -> tuple[dict, str, dict[str, bytes]]:
    tree = [blob_row(p, b) for p, b in sorted(files.items())]
    # manifest body (security metadata profile, excluding signature envelope)
    manifest_body = canonical.encode(
        {
            "kind": kind,
            "semanticVersion": version,
            "platform": platform,
            "files": [{"path": p, "sha256": sha(b), "bytes": len(b)} for p, b in sorted(files.items())],
        }
    )
    rec = {
        "schemaVersion": 2,
        "kind": kind,
        "manifestDigest": sha(manifest_body),
        "tree": tree,
        "semanticVersion": version,
        "protocolMajor": protocol_major,
        "platform": platform,
    }
    ident = h.h_id("closure", rec)
    blobs = dict(files)
    blobs["_manifest:" + kind] = manifest_body
    return rec, ident, blobs


def minimal_cap_manifest(profile: str, providers: list[dict], absent: list[dict] | None = None) -> dict:
    doc = {
        "schemaVersion": 1,
        "profile": profile,
        "providers": providers,
        "coverageForAbsent": absent or [],
    }
    return doc


def ts_provider_cap() -> dict:
    return {
        "providerId": "typescript-semantic",
        "language": "typescript",
        "providerVersionSource": "release.typescript-provider",
        "toolchainIdentitySource": "release.typescript-runtime",
        "relations": {
            "calls": "resolved-callee",
            "clones": "normalized-body-hash",
            "control-flow": "syntactic",
            "declares": "syntactic",
            "file": "enumerated",
            "imports": "resolved-target",
            "literal": "syntactic",
            "package": "manifest-declared",
            "reachability": "from-resolved-calls",
            "references": "resolved-binding",
            "types": "checked",
            "unresolved-edge": "observed",
            "vcs-change": "vcs-reported",
        },
        "platformIds": [
            "linux-aarch64-gnu",
            "linux-x86_64-gnu",
            "macos-aarch64",
            "macos-x86_64",
        ],
    }


def rust_provider_cap() -> dict:
    p = copy.deepcopy(ts_provider_cap())
    p["providerId"] = "rust-semantic"
    p["language"] = "rust"
    p["providerVersionSource"] = "release.rust-provider"
    p["toolchainIdentitySource"] = "release.rust-toolchain"
    return p


def syntax_provider_cap() -> dict:
    return {
        "providerId": "syntax-only",
        "language": "*",
        "providerVersionSource": "release.syntax-bundle",
        "toolchainIdentitySource": "release.syntax-bundle",
        "relations": {
            "clones": "normalized-body-hash",
            "control-flow": "syntactic",
            "declares": "syntactic",
            "file": "enumerated",
            "literal": "syntactic",
            "package": "manifest-declared",
            "vcs-change": "vcs-reported",
        },
        "platformIds": ["all-supported"],
    }


class Graph:
    def __init__(self, name: str):
        self.name = name
        self.store = store.Store()
        self.store.meta["runName"] = name
        self.files: dict[str, bytes] = {}
        self.ids: dict[str, str] = {}
        self.objects: dict[str, Any] = {}
        self.notes: list[str] = []

    def add_file(self, path: str, data: bytes | str) -> dict:
        if isinstance(data, str):
            data = data.encode("utf-8")
        self.files[path] = data
        self.store.put_blob(data, path)
        return blob_row(path, data)

    def retain_schema_docs(self) -> None:
        for label, raw in [
            ("relation-payload", REL_BYTES),
            ("native-evidence", NAT_BYTES),
            ("policy-v2", POL_V2_BYTES),
            ("policy-v1", POL_V1_BYTES),
            ("imported-evidence", IMP_BYTES),
        ]:
            self.store.put_blob(raw)

    def put_h(self, domain: str, obj: Any) -> str:
        ident = self.store.put_canonical_record(domain, obj)
        self.objects[domain if domain not in self.objects else domain + ":" + ident] = obj
        return ident

    def put_c(self, obj: Any) -> str:
        return self.store.put_raw_digest_record(obj)


def _honored_ts() -> dict:
    return {
        "allowJs": False,
        "checkJs": False,
        "module": "nodenext",
        "moduleResolution": "nodenext",
        "target": "es2022",
        "strict": True,
        "skipLibCheck": True,
        "noEmit": True,
        "types": None,
        "lib": ["es2022"],
        "baseUrl": None,
        "paths": [],
        "rootDirs": [],
        "resolveJsonModule": True,
        "allowSyntheticDefaultImports": True,
        "esModuleInterop": True,
        "customConditions": [],
        "jsx": None,
    }


def build_policy(rule_id: str, universe: str, subject_kind: str, emit_when: dict) -> dict:
    return {
        "schemaFamily": "opensip.product.policy",
        "schemaMajor": 2,
        "gateSeverityAtLeast": "error",
        "rules": [
            {
                "ruleId": rule_id,
                "ruleProgramRef": {
                    "contributionId": "contrib.file-exists.v1",
                    "ruleStableId": rule_id,
                    "semanticsMajor": 1,
                    "programDigest": hex64("rule-program-" + rule_id),
                },
                "enabled": True,
                "severity": "error",
                "gate": True,
                "subjectEnumeration": {
                    "universe": universe,
                    "subjectKind": subject_kind,
                    "include": [],
                    "exclude": [],
                },
                "emitWhen": emit_when,
                "evidenceUse": [],
                "messageCode": rule_id,
            }
        ],
    }


def file_exists_atom() -> dict:
    return {
        "op": "exists",
        "relation": "file",
        "minResolution": "enumerated",
        "filters": [],
    }


def none_clones_atom() -> dict:
    return {
        "op": "none",
        "relation": "clones",
        "minResolution": "normalized-body-hash",
        "filters": [],
    }


def build_scope_document() -> dict:
    return {
        "schemaFamily": "opensip.product.scope",
        "schemaMajor": 1,
        "include": ["**/*"],
        "exclude": ["node_modules/**"],
    }


def build_waivers() -> dict:
    return {
        "schemaFamily": "opensip.product.waiver",
        "schemaMajor": 1,
        "waivers": [],
    }


def semantic_config(caps: list[str]) -> dict:
    return {
        "analysis": {
            "profileId": "default",
            "capabilities": sorted(caps),
            "budget": {"unit": "work-units", "limit": 1000000},
        },
        "components": {},
        "discovery": {"entryPoints": [], "workspaceRoots": ["."], "ignorePaths": []},
        "policy": {"packIds": [], "waiverIds": []},
        "evidence": {"importIds": []},
    }


def scope_desc(roots: list[str] | None = None) -> dict:
    return {
        "schemaVersion": 2,
        "workspaceRoots": roots or ["."],
        "pathPrefixes": [],
        "excludedPathPrefixes": [],
    }


def grant(pid: str, scope_digest: str, closures: list[str], ops: list[str]) -> dict:
    principals = []
    for c in closures:
        principals.append({"kind": "first-party", "closureId": c, "ownerSourceDigest": None})
    return {
        "schemaVersion": 2,
        "projectId": pid,
        "principals": order.cset(principals),
        "analysisOperations": order.cset(ops),
        "scopeDigest": scope_digest,
    }
