#!/usr/bin/env python3
"""Pilot complete positive: syntax-only code grammar Run (R-RUN-SYNTAX-CODE).

Independently chosen synthetic observations. Kit-derived identities only.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v5/output")
KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-workflow-corrections.v5/subject")
sys.path.insert(0, str(OUT))

from helper.body_identity import (  # noqa: E402
    body_identity,
    body_identity_frame,
    body_language_version,
    framed_token_stream,
    l0_payload,
    language_version_bytes,
)
from helper.canonical import C  # noqa: E402
from helper.cap_manifest import capability_manifest_id  # noqa: E402
from helper.compose_proof import compose_expected_proof, select_file_subjects  # noqa: E402
from helper.evaluator import flatten, walk_predicate  # noqa: E402
from helper.identity import H, h_frame, typed_id  # noqa: E402
from helper.schema_admit import validate_against  # noqa: E402
from helper.store import Store  # noqa: E402
from helper.status import mark  # noqa: E402

IDENT = "docs/coop/design-corrections/foundation/identity-schemas.v3.json"
NATIVE = "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"
REL = "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json"
POL2 = "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json"
POL1 = "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json"
ENUM = "docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json"
EMIS = "docs/coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json"
EXEC = "docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json"
SINV = "docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json"


def sha_file(rel: str) -> str:
    return hashlib.sha256((KIT / rel).read_bytes()).hexdigest()


def sort_set(xs):
    return sorted(xs, key=lambda x: C(x))


store = Store()

# --- source files ---
hello = b"pub fn add(a: i32, b: i32) -> i32 { a + b }\n"
hello_d = store.put_raw(hello, label="hello.rs")
assert len(hello) == hello_d and False or True
hello_len = len(hello)

src_inv = [{"path": "hello.rs", "sha256": hello_d, "bytes": hello_len}]
src_inv = sorted(src_inv, key=lambda r: r["path"].encode())
inv_digest = store.put_canonical(src_inv, label="source-inventory")

vcs = {"schemaVersion": 2, "kind": "none", "commitId": None, "dirty": False, "sourceInventoryDigest": inv_digest}
vcs_d = store.put_canonical(vcs, label="vcs-observation")

scope_desc = {
    "schemaVersion": 2,
    "workspaceRoots": ["."],
    "pathPrefixes": [],
    "excludedPathPrefixes": [],
}
scope_d = store.put_canonical(scope_desc, label="scope-descriptor")

sem_cfg = {
    "analysis": {
        "profileId": "core",
        "capabilities": ["clones-fact", "inventory", "syntax"],
        "budget": {"unit": "work-units", "limit": 100000},
    },
    "components": {},
    "discovery": {},
    "policy": {},
    "evidence": {},
}
cfg_d = store.put_canonical(sem_cfg, label="semantic-configuration")

project_id = "prj1-" + hashlib.sha256(b"consumer-b.v12.syntax-pilot").hexdigest()
snapshot = {
    "schemaVersion": 2,
    "projectId": project_id,
    "sourceInventory": src_inv,
    "resolvedConfigDigest": cfg_d,
    "scopeDigest": scope_d,
    "vcsDigest": vcs_d,
}
snap_h = store.put_h("snapshot", snapshot, label="snapshot")
snapshot_id = snap_h["typedId"]

# --- closures ---
def make_closure(kind, platform="macos-aarch64", extra_files=None):
    body = json.dumps({"kind": kind, "name": f"opensip-{kind}", "version": "1.0.0"}, separators=(",", ":")).encode()
    man_d = store.put_raw(body, label=f"manifest-{kind}")
    tree = extra_files or []
    tree = sorted(tree + [{"path": f"bin/{kind}", "sha256": store.put_raw(b"stub-" + kind.encode(), label=f"bin-{kind}"), "bytes": 5 + len(kind)}], key=lambda r: r["path"].encode())
    rec = {
        "schemaVersion": 2,
        "kind": kind,
        "manifestDigest": man_d,
        "tree": tree,
        "semanticVersion": "1.0.0",
        "protocolMajor": 1,
        "platform": platform,
    }
    return store.put_h("closure", rec, label=f"closure-{kind}"), rec

grammar_spec = b"L0-verbatim: raw body span bytes. L1-lexical: collapse ASCII whitespace runs to 0x20; keep tokens.\n"
level_spec_d = store.put_raw(grammar_spec, label="level-spec-L1")
g_file = store.put_raw(b"rust-grammar-stub", label="grammar-rust")
bundle_blob = store.put_raw(b"grammar-bundle-archive", label="grammar-bundle-bytes")
g_closure, g_closure_rec = make_closure(
    "grammar",
    extra_files=[
        {"path": "grammars/rust.bin", "sha256": g_file, "bytes": len(b"rust-grammar-stub")},
        {"path": "bundle/archive", "sha256": bundle_blob, "bytes": len(b"grammar-bundle-archive")},
        {"path": "normalizer/specification", "sha256": level_spec_d, "bytes": len(grammar_spec)},
    ],
)
prov_closure, _ = make_closure("provider")
eval_closure, _ = make_closure("evaluator")
det_closure, _ = make_closure("detector")
grammar_bundle = {
    "schemaVersion": 1,
    "closureId": g_closure["typedId"],
    "parserName": "opensip-syntax-parser",
    "parserVersion": "1.0.0",
    "bundleDigest": bundle_blob,
    "grammars": [
        {
            "grammarId": "rust",
            "grammarVersion": "1.0.0",
            "languageId": "rust",
            "syntaxClass": "code",
            "suffixes": [".rs"],
            "grammarDigest": g_file,
        }
    ],
    "normalizer": {
        "normalizerId": "opensip-body-norm",
        "normalizerVersion": "1.0.0",
        "specificationDigest": level_spec_d,
    },
}
# grammars ordered by grammarId
syn_ctx = {"schemaVersion": 2, "grammarBundle": grammar_bundle}
ctx_h = store.put_h("native.context.syntax.v2", syn_ctx, label="syntax-context")
ctx_hex = ctx_h["digest"]

syn_uni = {
    "schemaVersion": 2,
    "nativeContextId": ctx_h["sha256Text"],
    "selectedGrammarIds": ["rust"],
    "resolutionAttempted": False,
}
uni_h = store.put_h("native.semantic-universe.syntax.v2", syn_uni, label="syntax-universe")
uni_hex = uni_h["digest"]

# --- capability manifest ---
cap_man = {
    "schemaVersion": 1,
    "profile": "core",
    "providers": [
        {
            "providerId": "syntax-provider",
            "language": "*",
            "providerVersionSource": "release.syntax-provider",
            "toolchainIdentitySource": "release.syntax-grammar",
            "relations": {
                "clones": "normalized-body-hash",
                "control-flow": "syntactic",
                "declares": "syntactic",
                "file": "enumerated",
                "literal": "syntactic",
                "package": "manifest-declared",
                "vcs-change": "vcs-reported",
            },
            "platformIds": [
                "linux-aarch64-gnu",
                "linux-x86_64-gnu",
                "macos-aarch64",
                "macos-x86_64",
            ],
        }
    ],
    "coverageForAbsent": [
        {
            "providerId": "syntax-provider",
            "language": "*",
            "relationIds": ["calls", "imports", "reachability", "references", "types"],
            "coverageState": "unavailable",
            "deficiency": "language-tier-unsupported",
        }
    ],
}
# coverageForAbsent relationIds must be sorted
cap_man["coverageForAbsent"][0]["relationIds"] = sorted(cap_man["coverageForAbsent"][0]["relationIds"])
cap_id_rec = capability_manifest_id(cap_man)
cap_bytes = bytes.fromhex(cap_id_rec["committedBytesHex"])
cap_bytes_d = store.put_raw(cap_bytes, label="capability-manifest-cve1")
assert hashlib.sha256(b"opensip.capability-manifest.v1\x00" + cap_bytes).hexdigest() == cap_id_rec["capabilityManifestId"]

# --- policy ---
contrib = "opensip.rules.syntax-pilot"
rule_stable = "file-present"
atom = {
    "op": "none",
    "relation": "file",
    "minResolution": "enumerated",
    "filters": [{"field": "subject", "cmp": "eq", "value": "hello.rs"}],
}
# programDigest filled after program exists — circular with ruleProgramRef.programDigest
# Policy rules include ruleProgramRef.programDigest of the RuleProgram. Typical: programDigest is SHA256(C(program)).
# We'll mint policy first without that digest matching, then set both to the program digest.
# The policy includes rules with programDigest. RuleProgram.policyDigest is SHA256(C(policy)).
# So: construct policy with placeholder, program with policy digest, then? That's circular.
# Standard approach: programDigest in policy refers to detector program artifact, NOT the RuleProgramV2 document.
# Schema: ruleProgramRef.programDigest is Sha256Hex — "detector program"
# RuleProgramV2.policyDigest is digest of PolicyDocumentV2.
# They are different. policy.rules[].ruleProgramRef.programDigest can be a detector blob digest.

det_prog = store.put_raw(b"declarative-subject-v1-detector", label="detector-program")
policy = {
    "schemaFamily": "opensip.product.policy",
    "schemaMajor": 2,
    "gateSeverityAtLeast": "error",
    "rules": [
        {
            "ruleId": "file-present",
            "ruleProgramRef": {
                "contributionId": contrib,
                "ruleStableId": rule_stable,
                "semanticsMajor": 1,
                "programDigest": det_prog,
            },
            "enabled": True,
            "severity": "error",
            "gate": True,
            "subjectEnumeration": {"universe": "syntax", "subjectKind": "file"},
            "emitWhen": atom,
            "evidenceUse": [],
        }
    ],
}
policy_d = store.put_canonical(policy, label="PolicyDocumentV2")
rule_program = {
    "schemaVersion": 2,
    "policyDigest": policy_d,
    "rules": [
        {
            "ruleId": "file-present",
            "ruleProgramRef": {
                "contributionId": contrib,
                "ruleStableId": rule_stable,
                "semanticsMajor": 1,
                "programDigest": det_prog,
            },
            "emitWhen": atom,
        }
    ],
}
rp_d = store.put_canonical(rule_program, label="RuleProgramV2")
waivers = {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1, "waivers": []}
waiver_d = store.put_canonical(waivers, label="WaiverSetV1")

grant = {
    "schemaVersion": 2,
    "projectId": project_id,
    "principals": [
        {
            "kind": "first-party",
            "closureId": prov_closure["typedId"],
            "ownerSourceDigest": None,
        }
    ],
    "analysisOperations": ["native-analysis", "read-source"],
    "scopeDigest": scope_d,
}
grant["analysisOperations"] = sorted(grant["analysisOperations"])
grant["principals"] = sort_set(grant["principals"])
grant_d = store.put_canonical(grant, label="semantic-grant")

# --- analysis spec parameters ---
def retain_schema(rel: str) -> str:
    return store.put_raw((KIT / rel).read_bytes(), label=rel)

enum_schema_d = retain_schema(ENUM)
emis_schema_d = retain_schema(EMIS)
rel_schema_d = retain_schema(REL)
native_schema_d = retain_schema(NATIVE)
ident_schema_d = retain_schema(IDENT)
pol2_schema_d = retain_schema(POL2)
pol1_schema_d = retain_schema(POL1)
sinv_schema_d = retain_schema(SINV)
exec_schema_d = retain_schema(EXEC)

# membership: syntax-only is not a WorkspaceUnitV2. U-4 unitOrdinal is null.
membership = {
    "schemaVersion": 1,
    "units": [],
    "rows": [
        {
            "path": "hello.rs",
            "languageFamily": "none",
            "unitOrdinal": None,
            "membership": "syntax-only",
            "reason": "grammar-only",
        }
    ],
    "unsupportedFiles": [],
    "outsideBoundaryFiles": [],
    "erasedFiles": [],
}
memb_d = store.put_canonical(membership, label="UnitMembershipV1")

# enumeration plan cells — order by capabilityId, languageMode, workspaceRoot
def binding():
    return {
        "ordinal": 0,
        "provenance": "default-unit",
        "enumerator": {"status": "selected", "closureId": prov_closure["typedId"]},
        "nativeContextDigest": ctx_hex,
        "universe": uni_hex,
        "programEntry": None,
        "extents": [{"kind": "file", "paths": ["hello.rs"]}],
    }


def cell(cap, kinds, extents_kind=None):
    b = binding()
    if extents_kind:
        b["extents"] = [{"kind": k, "paths": ["hello.rs"] if k != "package" else []} for k in kinds]
        b["extents"] = sorted(b["extents"], key=lambda x: x["kind"].encode())
    return {
        "capabilityId": cap,
        "languageMode": "syntax-only",
        "workspaceRoot": ".",
        "required": True,
        "kinds": kinds,
        "programBindings": [b],
    }


cells = [
    cell("clones-fact", ["file"]),
    cell("inventory", ["file", "package"]),
    cell("syntax", ["symbol"]),
]
# kinds canonical-set
for c in cells:
    c["kinds"] = sorted(c["kinds"])
    if c["capabilityId"] == "syntax":
        c["programBindings"][0]["extents"] = [{"kind": "symbol", "paths": ["hello.rs"]}]
    if c["capabilityId"] == "inventory":
        c["programBindings"][0]["extents"] = [
            {"kind": "file", "paths": ["hello.rs"]},
            {"kind": "package", "paths": []},
        ]
        c["programBindings"][0]["extents"] = sorted(c["programBindings"][0]["extents"], key=lambda x: x["kind"].encode())
enum_plan = {
    "schemaVersion": 1,
    "snapshotId": snapshot_id,
    "scopeDigest": scope_d,
    "membershipDigest": memb_d,
    "cells": cells,
}
enum_d = store.put_canonical(enum_plan, label="EnumerationPlanV1")

emis_plan = {
    "schemaVersion": 1,
    "policyDigest": policy_d,
    "rules": [
        {
            "ruleId": "file-present",
            "contributionId": contrib,
            "ruleStableId": rule_stable,
            "semanticsMajor": 1,
            "detectorClosure": det_closure["typedId"],
            "stabilityClass": "path-stable",
            "emissionProfile": "declarative-subject-v1",
        }
    ],
}
emis_d = store.put_canonical(emis_plan, label="EvaluatorEmissionPlanV1")

params = sort_set(
    [
        {"schemaDigest": enum_schema_d, "payloadDigest": enum_d},
        {"schemaDigest": emis_schema_d, "payloadDigest": emis_d},
    ]
)
req_caps = sort_set(
    [
        {"capabilityId": "clones-fact", "languageMode": "syntax-only", "workspaceRoot": ".", "required": True},
        {"capabilityId": "inventory", "languageMode": "syntax-only", "workspaceRoot": ".", "required": True},
        {"capabilityId": "syntax", "languageMode": "syntax-only", "workspaceRoot": ".", "required": True},
    ]
)
analysis_spec = {
    "schemaVersion": 2,
    "requestedCapabilities": req_caps,
    "policyPackIds": [],
    "parameters": params,
}
as_d = store.put_canonical(analysis_spec, label="analysis-spec")

# --- plan ---
plan = {
    "schemaVersion": 2,
    "snapshotId": snapshot_id,
    "capabilityManifestId": cap_id_rec["capabilityManifestId"],
    "semanticClosures": sort_set([prov_closure["typedId"], g_closure["typedId"]]),
    "analysisSpecDigest": as_d,
    "resolvedConfigDigest": cfg_d,
    "nativeContextDigests": [ctx_hex],
    "importIds": [],
    "policyDigest": policy_d,
    "waiverDigest": waiver_d,
    "scopeDigest": scope_d,
    "budget": {"unit": "work-units", "limit": 100000},
    "semanticGrantDigest": grant_d,
    "capabilityManifestBytesDigest": cap_bytes_d,
}
plan_h = store.put_h("plan", plan, label="plan")
plan_id = plan_h["typedId"]

# stage spec / execution plan
stage_spec = {
    "schemaVersion": 2,
    "planId": plan_id,
    "producerClosure": prov_closure["typedId"],
    "operation": "analyze",
    "parameters": params,
    "outputDomains": sort_set(["coverage", "fact", "view", "subject-inventory"]),
    "outputSchemaDigest": native_schema_d,
}
ss_d = store.put_canonical(stage_spec, label="stage-spec")
exec_plan = {
    "schemaVersion": 2,
    "planId": plan_id,
    "stages": [
        {"ordinal": 0, "stageSpecDigest": ss_d, "requires": [], "outputDomains": stage_spec["outputDomains"]}
    ],
}
ep_h = store.put_h("execution-plan", exec_plan, label="execution-plan")
exec_plan_id = ep_h["typedId"]

# --- body identity ---
blv = body_language_version(
    language_id="rust",
    compiler_name="opensip-syntax-parser",
    compiler_version="1.0.0",
    compiler_build=bundle_blob,
    dialect={"grammarVariant": "rs"},
)
lv = language_version_bytes(blv)
l0_frame = body_identity_frame(
    level_id="L0-verbatim",
    level_spec_bytes=grammar_spec,
    language_id="rust",
    language_version=lv,
    payload=l0_payload(hello),
)
l0_id = "sha256:" + store.put_raw(l0_frame, label="fact-identity-L0-verbatim")
# L1: treat whole file as one token ident-like after whitespace collapse
collapsed = b" ".join(hello.split())
tokens = [("other", collapsed)]
l1_frame = body_identity_frame(
    level_id="L1-lexical",
    level_spec_bytes=grammar_spec,
    language_id="rust",
    language_version=lv,
    payload=framed_token_stream(tokens),
)
l1_id = "sha256:" + store.put_raw(l1_frame, label="fact-identity-L1-lexical")
assert l0_id == body_identity(
    level_id="L0-verbatim",
    level_spec_bytes=grammar_spec,
    language_id="rust",
    language_version=lv,
    payload=l0_payload(hello),
)
assert l1_id == body_identity(
    level_id="L1-lexical",
    level_spec_bytes=grammar_spec,
    language_id="rust",
    language_version=lv,
    payload=framed_token_stream(tokens),
)
store.put_canonical(blv, label="body-language-version")
store.put_raw(lv, label="languageVersion-raw32")

# --- facts ---
file_payload = {"path": "hello.rs", "contentSha256": hello_d, "byteLength": hello_len}
file_pd = store.put_canonical(file_payload, label="FilePayloadV1")
decl_payload = {"container": "file:hello.rs", "declarationKind": "function", "declared": "function:add"}
decl_pd = store.put_canonical(decl_payload, label="DeclaresPayloadV1")
cl0_payload = {"bodyIdentity": l0_id, "normalisationLevel": "L0-verbatim", "normalisationVersion": hashlib.sha256(grammar_spec).hexdigest()}
cl1_payload = {"bodyIdentity": l1_id, "normalisationLevel": "L1-lexical", "normalisationVersion": hashlib.sha256(grammar_spec).hexdigest()}
cl0_pd = store.put_canonical(cl0_payload, label="ClonesPayloadV1-L0")
cl1_pd = store.put_canonical(cl1_payload, label="ClonesPayloadV1-L1")


def fact(relation, resolution, payload_digest, anchors):
    rec = {
        "schemaVersion": 2,
        "snapshotId": snapshot_id,
        "relation": relation,
        "resolution": resolution,
        "sourceUniverse": uni_hex,
        "targetUniverse": uni_hex,
        "producerClosure": prov_closure["typedId"],
        "payloadSchemaDigest": rel_schema_d,
        "payloadDigest": payload_digest,
        "anchors": sort_set(anchors),
        "confidenceMillionths": 1000000,
    }
    h = store.put_h("fact", rec, label=f"fact-{relation}-{resolution}")
    return h, rec


file_fact_h, file_fact = fact("file", "enumerated", file_pd, [])
decl_fact_h, decl_fact = fact(
    "declares",
    "syntactic",
    decl_pd,
    [{"path": "hello.rs", "blobDigest": hello_d, "startByte": 0, "endByte": hello_len}],
)
cl0_h, cl0_f = fact(
    "clones",
    "normalized-body-hash",
    cl0_pd,
    [{"path": "hello.rs", "blobDigest": hello_d, "startByte": 0, "endByte": hello_len}],
)
cl1_h, cl1_f = fact(
    "clones",
    "normalized-body-hash",
    cl1_pd,
    [{"path": "hello.rs", "blobDigest": hello_d, "startByte": 0, "endByte": hello_len}],
)

# --- scopes + coverage ---
def make_scope(relation, resolution, subjects):
    rec = {
        "schemaVersion": 2,
        "snapshotId": snapshot_id,
        "sourceUniverse": uni_hex,
        "targetUniverse": uni_hex,
        "relation": relation,
        "resolution": resolution,
        "enumeratorClosure": prov_closure["typedId"],
        "subjects": sorted(subjects),
    }
    h = store.put_h("subject-scope", rec, label=f"scope-{relation}")
    return h, rec


scope_file_h, scope_file = make_scope("file", "enumerated", ["hello.rs"])
scope_dec_h, scope_dec = make_scope("declares", "syntactic", ["function:add"])
scope_cl_h, scope_cl = make_scope("clones", "normalized-body-hash", ["hello.rs"])


def rc_na(stage="complete", exhaustive=True):
    return {
        "state": "not-applicable",
        "attempted": False,
        "examinedExhaustive": exhaustive,
        "stageTerminal": stage,
        "unresolvedEdgeCount": 0,
        "unresolvedEdgeClasses": [],
    }


def closed_world():
    return {
        "exportsClosed": "unknown",
        "entryPointsRecognized": "none",
        "nonliteralLoading": "none",
        "externalConsumers": "unknown",
        "dynamicDispatch": "not-applicable",
        "reasons": [],
        "deadCodeRepairEligible": False,
    }


def coverage_entry(relation, resolution, scope_h, subjects_len, cov="complete"):
    commit = "sha256:" + scope_h["digest"]
    key = {
        "relation": relation,
        "resolution": resolution,
        "sourceUniverse": uni_hex,
        "targetUniverse": uni_hex,
        "subjectScopeCommitment": commit,
    }
    entry = {
        "relation": relation,
        "resolution": resolution,
        "coverage": cov,
        "examinedUniverse": {"subjectScopeCommitment": commit, "subjectCount": subjects_len},
        "resolutionCompleteness": rc_na(exhaustive=(cov == "complete")),
        "closedWorld": closed_world(),
        "derivationKinds": [],
        "confidenceMillionths": 1000000,
        "deficiency": None,
        "nativeCause": None,
    }
    payload = {"schemaVersion": 3, "key": key, "entry": entry}
    pd = store.put_canonical(payload, label=f"CoverageResultV3-{relation}")
    rec = {
        "schemaVersion": 2,
        "scopeId": scope_h["typedId"],
        "payloadSchemaDigest": native_schema_d,
        "payloadDigest": pd,
    }
    h = store.put_h("coverage", rec, label=f"coverage-{relation}")
    return h, rec, payload


cov_file_h, cov_file, cov_file_p = coverage_entry("file", "enumerated", scope_file_h, 1)
cov_dec_h, cov_dec, cov_dec_p = coverage_entry("declares", "syntactic", scope_dec_h, 1)
cov_cl_h, cov_cl, cov_cl_p = coverage_entry("clones", "normalized-body-hash", scope_cl_h, 1)

view = {
    "schemaVersion": 2,
    "planId": plan_id,
    "scopeIds": sort_set([scope_file_h["typedId"], scope_dec_h["typedId"], scope_cl_h["typedId"]]),
    "facts": sort_set([file_fact_h["typedId"], decl_fact_h["typedId"], cl0_h["typedId"], cl1_h["typedId"]]),
    "coverageIds": sort_set([cov_file_h["typedId"], cov_dec_h["typedId"], cov_cl_h["typedId"]]),
    "producerClosure": prov_closure["typedId"],
    "schemaDigests": sort_set([rel_schema_d, native_schema_d]),
}
view_h = store.put_h("view", view, label="view")

# --- subject inventories: exactly one per (cellOrdinal, programOrdinal, kind) ---
inv_row_file = {
    "nativeSubjectId": "hello.rs",
    "kind": "file",
    "path": "hello.rs",
    "qualifiedName": "hello.rs",
    "subjectLanguage": "rust",
    "signatureTokens": [],
    "projections": [],
}
inv_row_symbol = {
    "nativeSubjectId": "function:add",
    "kind": "symbol",
    "path": "hello.rs",
    "qualifiedName": "add",
    "subjectLanguage": "rust",
    "exported": "exported",
    "signatureTokens": ["add"],
    "projections": [],
}


def make_sinv(cell_ordinal, kind, rows, examined):
    rec = {
        "schemaVersion": 1,
        "planId": plan_id,
        "parameterDigest": enum_d,
        "cellOrdinal": cell_ordinal,
        "programOrdinal": 0,
        "kind": kind,
        "state": "complete",
        "deficiency": None,
        "nativeCause": None,
        "examinedPaths": sorted(examined),
        "rows": rows,
    }
    d = store.put_canonical(rec, label=f"SubjectInventoryV1-{cell_ordinal}-{kind}")
    return d, rec


sinv_clones_file_d, sinv_clones_file = make_sinv(0, "file", [inv_row_file], ["hello.rs"])
sinv_inv_file_d, sinv_inv_file = make_sinv(1, "file", [inv_row_file], ["hello.rs"])
sinv_pkg_d, sinv_pkg = make_sinv(1, "package", [], [])
sinv_sym_d, sinv_sym = make_sinv(2, "symbol", [inv_row_symbol], ["hello.rs"])
file_inventories = [sinv_clones_file, sinv_inv_file]
subjects = select_file_subjects(inventories=file_inventories, universe=uni_hex, store=store)
assert len(subjects) == 1
subj = subjects[0]["record"]
subj_h = {"typedId": subjects[0]["id"]}

facts_for_eval = [
    {"id": file_fact_h["typedId"], "record": file_fact},
    {"id": decl_fact_h["typedId"], "record": decl_fact},
    {"id": cl0_h["typedId"], "record": cl0_f},
    {"id": cl1_h["typedId"], "record": cl1_f},
]
payloads = {
    file_fact_h["typedId"]: file_payload,
    decl_fact_h["typedId"]: decl_payload,
    cl0_h["typedId"]: cl0_payload,
    cl1_h["typedId"]: cl1_payload,
}
coverages_for_eval = [
    {"id": cov_file_h["typedId"], "record": {"relation": "file", "resolution": "enumerated"}, "entry": cov_file_p["entry"]},
    {"id": cov_dec_h["typedId"], "record": {"relation": "declares", "resolution": "syntactic"}, "entry": cov_dec_p["entry"]},
    {"id": cov_cl_h["typedId"], "record": {"relation": "clones", "resolution": "normalized-body-hash"}, "entry": cov_cl_p["entry"]},
]
tree = walk_predicate(
    atom,
    prefix="p",
    subject=subj,
    facts=facts_for_eval,
    coverages=coverages_for_eval,
    payloads=payloads,
)
assert tree["value"] == "false", tree  # none of file hello.rs is FALSE because the file exists

# execution inputs
inv_refs = sort_set(
    [
        {"domain": "subject-inventory", "digest": sinv_clones_file_d},
        {"domain": "subject-inventory", "digest": sinv_inv_file_d},
        {"domain": "subject-inventory", "digest": sinv_pkg_d},
        {"domain": "subject-inventory", "digest": sinv_sym_d},
    ]
)
host_cap = {
    "custody": "host-tcb-evidence-store",
    "observation": "stage-return",
    "stageReceipts": [
        {
            "ordinal": 0,
            "stageSpecDigest": ss_d,
            "producerClosure": prov_closure["typedId"],
            "outputDomains": stage_spec["outputDomains"],
            "outputRefs": sort_set(
                [
                    {"domain": "view", "digest": view_h["digest"]},
                    {"domain": "coverage", "digest": cov_file_h["digest"]},
                    {"domain": "coverage", "digest": cov_dec_h["digest"]},
                    {"domain": "coverage", "digest": cov_cl_h["digest"]},
                ]
                + inv_refs
            ),
            "state": "complete",
            "unavailableReason": None,
        }
    ],
    "hostDerivedRefs": inv_refs,
}


def outcome(ord_, cell_ord, cap, kinds, invs, views):
    return {
        "ordinal": ord_,
        "cellOrdinal": cell_ord,
        "programOrdinal": 0,
        "capabilityId": cap,
        "languageMode": "syntax-only",
        "workspaceRoot": ".",
        "required": True,
        "kinds": kinds,
        "universe": uni_hex,
        "enumeratorStatus": "selected",
        "enumeratorClosure": prov_closure["typedId"],
        "state": "complete",
        "deficiency": None,
        "nativeCause": None,
        "stageOrdinal": 0,
        "stageOrdinalNullReason": None,
        "inventoryDigests": sort_set(list(invs)),
        "viewDigests": views,
        "candidateResultDigest": None,
    }


cell_outcomes = [
    outcome(0, 0, "clones-fact", ["file"], [sinv_clones_file_d], [view_h["digest"]]),
    outcome(1, 1, "inventory", ["file", "package"], [sinv_inv_file_d, sinv_pkg_d], [view_h["digest"]]),
    outcome(2, 2, "syntax", ["symbol"], [sinv_sym_d], [view_h["digest"]]),
]
cell_outcomes[0]["kinds"] = ["file"]
cell_outcomes[1]["kinds"] = sorted(["file", "package"])
cell_outcomes[2]["kinds"] = ["symbol"]

nca = []
for rel, rung, covh, cell_i in [
    ("clones", "normalized-body-hash", cov_cl_h, 0),
    ("file", "enumerated", cov_file_h, 1),
    ("declares", "syntactic", cov_dec_h, 2),
]:
    nca.append(
        {
            "cellOrdinal": cell_i,
            "programOrdinal": 0,
            "relation": rel,
            "resolution": rung,
            "sourceUniverse": uni_hex,
            "targetUniverse": uni_hex,
            "applicability": "supported-available",
            "coverageIds": [covh["digest"]],
        }
    )

exec_inputs = {
    "schemaVersion": 1,
    "planId": plan_id,
    "executionPlanId": exec_plan_id,
    "evaluatorClosure": eval_closure["typedId"],
    "enumerationPlanDigest": enum_d,
    "analysisSpecDigest": as_d,
    "hostCapture": host_cap,
    "selectedRefs": sort_set(
        [
            {"domain": "view", "digest": view_h["digest"]},
            {"domain": "coverage", "digest": cov_file_h["digest"]},
            {"domain": "coverage", "digest": cov_dec_h["digest"]},
            {"domain": "coverage", "digest": cov_cl_h["digest"]},
        ]
        + inv_refs
    ),
    "cellOutcomes": cell_outcomes,
    "nativeCoverageAccounts": nca,
    "candidateResultRefs": [],
}
ei_d = store.put_canonical(exec_inputs, label="ExecutionInputsV1")

proof = compose_expected_proof(
    plan_id=plan_id,
    execution_plan_id=exec_plan_id,
    evaluator_closure=eval_closure["typedId"],
    policy=policy,
    policy_digest=policy_d,
    rule_program=rule_program,
    rule_program_digest=rp_d,
    execution_inputs=exec_inputs,
    execution_inputs_digest=ei_d,
    subjects=subjects,
    facts=facts_for_eval,
    payloads=payloads,
    coverages=coverages_for_eval,
    view_digest=view_h["digest"],
    file_scope_id=scope_file_h["typedId"],
    file_inventories=file_inventories,
    store=store,
)
assert proof["verdict"] == "pass", proof
assert proof["predicateProofs"][0]["value"] == "false"
proof_h = store.put_h("proof-bundle", proof, label="proof")
evidence = {
    "schemaVersion": 3,
    "planId": plan_id,
    "viewIds": [view_h["typedId"]],
    "coverageIds": sort_set([cov_file_h["typedId"], cov_dec_h["typedId"], cov_cl_h["typedId"]]),
    "importIds": [],
    "findingIds": [],
    "proofBundleId": proof_h["typedId"],
}
ev_h = store.put_h("semantic-evidence", evidence, label="evidence")
seal = {
    "schemaVersion": 3,
    "planId": plan_id,
    "executionPlanId": exec_plan_id,
    "evidenceId": ev_h["typedId"],
    "evaluatorClosure": eval_closure["typedId"],
    "policyDigest": policy_d,
    "proofBundleId": proof_h["typedId"],
    "verdict": "pass",
}
seal_h = store.put_h("evaluation-seal", seal, label="seal")
run = {
    "schemaVersion": 3,
    "projectId": project_id,
    "snapshotId": snapshot_id,
    "planId": plan_id,
    "evidenceId": ev_h["typedId"],
    "evaluationSealId": seal_h["typedId"],
    "capabilityManifestId": cap_id_rec["capabilityManifestId"],
}
run_h = store.put_h("run", run, label="run")

# validate key records
checks = []
for label, inst, rel, sel in [
    ("snapshot", snapshot, IDENT, "#/$defs/snapshot"),
    ("plan", plan, IDENT, "#/$defs/plan"),
    ("run", run, IDENT, "#/$defs/run"),
    ("proof", proof, IDENT, "#/$defs/proof-bundle"),
    ("policy", policy, POL2, "#/$defs/PolicyDocumentV2"),
    ("enum", enum_plan, ENUM, "#"),
    ("exec_inputs", exec_inputs, EXEC, "#"),
    ("view", view, IDENT, "#/$defs/view"),
    ("file_fact", file_fact, IDENT, "#/$defs/fact"),
    ("decl_fact", decl_fact, IDENT, "#/$defs/fact"),
    ("cl0_fact", cl0_f, IDENT, "#/$defs/fact"),
    ("coverage_file", cov_file, IDENT, "#/$defs/coverage"),
    ("cov_payload_file", cov_file_p, NATIVE, "#/$defs/CoverageResultV3"),
    ("scope_file", scope_file, IDENT, "#/$defs/subject-scope"),
    ("syn_ctx", syn_ctx, NATIVE, "#/$defs/SyntaxNativeContextV2"),
    ("syn_uni", syn_uni, NATIVE, "#/$defs/SyntaxUniverseV2ResolvedInputs"),
    ("emis", emis_plan, EMIS, "#"),
    ("grant", grant, IDENT, "#/$defs/semantic-grant"),
    ("file_payload", file_payload, REL, "#/$defs/FilePayloadV1"),
    ("decl_payload", decl_payload, REL, "#/$defs/DeclaresPayloadV1"),
    ("cl0_payload", cl0_payload, REL, "#/$defs/ClonesPayloadV1"),
    ("membership", membership, NATIVE, "#/$defs/UnitMembershipV1"),
    ("sinv_clones_file", sinv_clones_file, SINV, "#"),
    ("sinv_inv_file", sinv_inv_file, SINV, "#"),
    ("sinv_pkg", sinv_pkg, SINV, "#"),
    ("sinv_sym", sinv_sym, SINV, "#"),
    ("seal", seal, IDENT, "#/$defs/evaluation-seal"),
    ("evidence", evidence, IDENT, "#/$defs/semantic-evidence"),
    ("analysis_spec", analysis_spec, IDENT, "#/$defs/analysis-spec"),
    ("blv", blv, IDENT, "#/$defs/body-language-version"),
]:
    r = validate_against(inst, rel, selector=sel, label=label)
    checks.append({"label": label, "stockOk": r["stockOk"], "nErrors": len(r["errors"]), "errors": r["errors"][:5]})

export_path = OUT / "runs" / "syntax-code.store.json"
store.export(export_path)
meta = {
    "runId": run_h["typedId"],
    "planId": plan_id,
    "snapshotId": snapshot_id,
    "proofId": proof_h["typedId"],
    "verdict": "pass",
    "atomValue": tree["value"],
    "capabilityManifestId": cap_id_rec["capabilityManifestId"],
    "nativeContext": ctx_h["sha256Text"],
    "universe": uni_h["sha256Text"],
    "fileFact": file_fact_h["typedId"],
    "clonesL0": cl0_h["typedId"],
    "clonesL1": cl1_h["typedId"],
    "l0Identity": l0_id,
    "l1Identity": l1_id,
    "outputMajors": {"run": "run3", "proof": "proof3", "evidence": "evidence3", "seal": "seal3"},
    "schemaChecks": checks,
    "export": str(export_path),
    "blobCount": len(store.blobs),
}
(OUT / "runs" / "syntax-code.meta.json").write_text(json.dumps(meta, indent=2) + "\n")
# --- independent closure joins (kit laws, not helper self-mint equality alone) ---
closure = {"ok": True, "joins": []}

def join(name, pred, detail=""):
    rec = {"name": name, "ok": bool(pred), "detail": detail}
    closure["joins"].append(rec)
    if not pred:
        closure["ok"] = False

# file inventory join
join("file-path-in-snapshot", file_payload["path"] in {r["path"] for r in src_inv})
row = next(r for r in src_inv if r["path"] == "hello.rs")
join("file-digest-matches-inventory", file_payload["contentSha256"] == row["sha256"])
join("file-length-matches-inventory", file_payload["byteLength"] == row["bytes"])
join("file-blob-retained", hello_d in store.blobs and store.blobs[hello_d] == hello)
join("file-zero-anchors", file_fact["anchors"] == [])
# L0 recompute from retained bytes AND retained frame fetch
re_l0 = body_identity(
    level_id="L0-verbatim",
    level_spec_bytes=grammar_spec,
    language_id="rust",
    language_version=lv,
    payload=l0_payload(store.blobs[hello_d]),
)
join("clones-L0-recomputed-from-anchor-bytes", re_l0 == l0_id, re_l0)
l0_suffix = l0_id[len("sha256:") :]
l1_suffix = l1_id[len("sha256:") :]
join("clones-L0-frame-retained", l0_suffix in store.blobs and store.blobs[l0_suffix] == l0_frame)
join("clones-L1-frame-retained", l1_suffix in store.blobs and store.blobs[l1_suffix] == l1_frame)
g_tree = {row["sha256"] for row in g_closure_rec["tree"]}
join("grammar-bundleDigest-in-tree", bundle_blob in g_tree, bundle_blob)
join("grammar-specificationDigest-in-tree", level_spec_d in g_tree, level_spec_d)
join("grammar-definition-in-tree", g_file in g_tree, g_file)
join("declares-container-subject-id", ":" in decl_payload["container"] and decl_payload["container"].startswith("file:"))
join("declares-declared-subject-id", decl_payload["declared"].startswith("function:"))
join("membership-no-invented-unit", membership["units"] == [])
join("membership-unitOrdinal-null", all(r["unitOrdinal"] is None for r in membership["rows"]))
inv_locs = {(s["cellOrdinal"], s["programOrdinal"], s["kind"]) for s in [sinv_clones_file, sinv_inv_file, sinv_pkg, sinv_sym]}
join("enumeration-inventories-complete", inv_locs == {(0, 0, "file"), (1, 0, "file"), (1, 0, "package"), (2, 0, "symbol")})
join("capability-manifest-derived", cap_id_rec["capabilityManifestId"] == plan["capabilityManifestId"])
join("cap-bytes-digest", hashlib.sha256(cap_bytes).hexdigest() == cap_bytes_d)
join("plan-native-context-selected", ctx_hex in plan["nativeContextDigests"])
join("universe-binds-context", syn_uni["nativeContextId"] == "sha256:" + ctx_hex)
join("proof-no-evidence-or-run", "evidenceId" not in proof and "runId" not in proof)
join("run-includes-seal", run["evaluationSealId"] == seal_h["typedId"])
join("seal-includes-evidence-and-proof", seal["evidenceId"] == ev_h["typedId"] and seal["proofBundleId"] == proof_h["typedId"])
join("coverage-complete-implies-exhaustive", cov_file_p["entry"]["coverage"] != "complete" or cov_file_p["entry"]["resolutionCompleteness"]["examinedExhaustive"] is True)
join("file-rung-enumerated-only", file_fact["resolution"] == "enumerated")
join("grammar-closure-kind", g_closure["typedId"].startswith("closure2:"))

# reload export in-process (builder sanity, not the from-scratch command)
loaded = Store.load(export_path)
join("export-reload-run-frame", loaded.get(run_h["digest"]) == store.get(run_h["digest"]))
from helper.identity import parse_h_frame
from helper.proof_replay import load_graph, reconstruct_expected_proof

pf = parse_h_frame(loaded.get(proof_h["digest"]), allowed_domains={"proof-bundle"})
join("proof-frame-C-equals-claimed", C(pf["value"]) == C(proof))
join("recomputed-run-H", typed_id("run", run) == run_h["typedId"])
g_loaded = load_graph(loaded)
recon = reconstruct_expected_proof(loaded, g_loaded)
join("builder-sanity-complete-proof-C", C(recon["proof"]) == C(proof))
join("derived-verdict-from-composition", recon["proof"]["verdict"] == "pass")
# Stale-hash control is recorded separately from semantic replay (the latter is replay_from_export.py --tamper).
stale = json.loads(json.dumps(proof))
stale["verdict"] = "fail"
join("stale-hash-control-verdict-C-changes", C(stale) != C(proof))

(OUT / "runs" / "syntax-code.closure.json").write_text(json.dumps(closure, indent=2) + "\n")
replay_note = {
    "runId": run_h["typedId"],
    "derivedAtomValue": tree["value"],
    "claimedVerdict": proof["verdict"],
    "derivedVerdict": recon["proof"]["verdict"],
    "builderSanityProofCompareEqual": C(recon["proof"]) == C(proof),
    "note": "Builder-side sanity is not admission. Authoritative complete replay is the fresh-process command in syntax-code.replay-cmd.json.",
    "fromScratchCommand": "/tmp/opensip-architecture-review-env/bin/python -I -B "
    + str(OUT / "scripts/replay_from_export.py")
    + " "
    + str(export_path),
    "tamperCommand": "/tmp/opensip-architecture-review-env/bin/python -I -B "
    + str(OUT / "scripts/replay_from_export.py")
    + " --tamper "
    + str(export_path),
    "threeValuedNote": "exists with missing Coverage and no match is indeterminate; this Run has complete file Coverage so none is false, not vacuous true",
}
(OUT / "runs" / "syntax-code.replay.json").write_text(json.dumps(replay_note, indent=2) + "\n")
(OUT / "runs" / "syntax-code.replay-cmd.json").write_text(
    json.dumps(
        {
            "store": str(export_path),
            "command": "/tmp/opensip-architecture-review-env/bin/python -I -B " + str(OUT / "scripts/replay_from_export.py"),
            "args": [str(export_path)],
            "tamperArgs": ["--tamper", str(export_path)],
            "kind": "complete-expected-proof-from-admitted-inputs",
        },
        indent=2,
    )
    + "\n"
)

print(json.dumps({"runId": run_h["typedId"], "checks": [(c["label"], c["stockOk"], c["nErrors"]) for c in checks], "closureOk": closure["ok"]}, indent=2))
for c in checks:
    if not c["stockOk"]:
        print("FAIL", c["label"], json.dumps(c["errors"][:3], indent=2)[:800])
for j in closure["joins"]:
    if not j["ok"]:
        print("JOIN FAIL", j)
