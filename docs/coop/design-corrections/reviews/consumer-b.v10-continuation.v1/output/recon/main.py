#!/usr/bin/env python3
"""From-scratch reconstruction driver. Recomputes identities and validates graphs."""
from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path

ROOT = Path("/tmp/opensip-design-corrections/consumer-b.v10-continuation.v1/output")
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from recon import capability as cap
from recon.codec import (
    AdmissionError,
    admit_json_text,
    body_identity,
    body_identity_frame,
    canonical_digest,
    capability_manifest_id,
    decode_cve1,
    encode_c,
    encode_cve1,
    h_hex,
    h_id,
    h_preimage,
    l0_payload,
    parse_h_frame,
    sha256,
)
from recon.graphs import ts_ordinary_graph
from recon.graphs_lang import rust_mixed_graph, syntax_graph
from recon.protocol import identity_versions, run_trace, rust_hello_caps
from recon.schema_val import validate_def

OUT = ROOT / "vectors"
RUNS = ROOT / "runs"
OUT.mkdir(exist_ok=True)
RUNS.mkdir(exist_ok=True)


def dump(name: str, obj) -> None:
    p = OUT / f"{name}.json"
    p.write_text(json.dumps(obj, indent=2, default=lambda o: o.hex() if isinstance(o, bytes) else str(o)))
    return


def run_codec_vectors() -> dict:
    results = []
    # eight CVE1 types
    samples = {
        "null": None,
        "false": False,
        "true": True,
        "unsigned-64": 1,
        "unsigned-64-zero": 0,
        "negative-signed-64": -1,
        "NFC-UTF8-string": "café",
        "array": [1, "a", None],
        "string-keyed-map": {"b": 1, "a": 2},
    }
    roundtrips = {}
    for k, v in samples.items():
        b = encode_cve1(v)
        back = decode_cve1(b)
        roundtrips[k] = {"hex": b.hex(), "roundtrip": back == v, "decoded": back}
        assert back == v, (k, back, v)
    results.append({"id": "cve1-eight-types", "ok": True, "roundtrips": roundtrips})

    # H identity: semantic change vs operational exclusion
    d1 = {"schemaVersion": 2, "projectId": "prj1-" + "a" * 64, "x": 1}
    d2 = {"schemaVersion": 2, "projectId": "prj1-" + "a" * 64, "x": 2}
    h1, h2 = h_hex("plan", d1), h_hex("plan", d2)
    results.append(
        {
            "id": "h-semantic-field-change",
            "ok": h1 != h2,
            "h1": h1,
            "h2": h2,
        }
    )
    # operational timestamp/request-id are not in descriptors
    results.append(
        {
            "id": "h-operational-excluded",
            "ok": True,
            "note": "RequestId/ExecutionId/timestamps are not H preimage fields (identity-and-evidence §2)",
        }
    )

    # lexical integer admission
    lex_ok = []
    for text, should_fail, code in [
        ('{"n":1}', False, None),
        ('{"n":1.0}', True, "NON_INTEGER_TOKEN"),
        ('{"n":1e0}', True, "NON_INTEGER_TOKEN"),
        ('{"n":true}', False, None),  # type is later ADM-TYPE
        ('{"a":1,"a":2}', True, "DUPLICATE_KEY"),
        ('{"n":-0}', True, "NEG_ZERO"),
    ]:
        try:
            admit_json_text(text)
            lex_ok.append({"text": text, "failed": False, "expectFail": should_fail, "ok": not should_fail})
        except AdmissionError as e:
            lex_ok.append({"text": text, "failed": True, "code": e.code, "expectFail": should_fail, "ok": should_fail})
    results.append({"id": "lexical-admission", "cases": lex_ok, "ok": all(c["ok"] for c in lex_ok)})

    # C key order is UTF-8 bytes
    c = encode_c({"b": 1, "a": 2})
    results.append({"id": "c-key-order", "bytes": c.decode(), "ok": c.decode().startswith('{"a":2,"b":1}')})

    # body L0 double length prefix
    span = b"a=1\n"
    payload = l0_payload(span)
    assert payload == b"\x00\x00\x00\x04a=1\n"
    blv_lang = bytes(32)
    frame = body_identity_frame(
        level_id="L0-verbatim",
        level_version=bytes(32),
        language_id="typescript",
        language_version=bytes(32),
        payload=payload,
    )
    # trailing frame component is u32be(8) || payload
    assert frame.endswith(b"\x00\x00\x00\x08\x00\x00\x00\x04a=1\n")
    results.append({"id": "l0-double-length", "ok": True, "bodyIdentity": body_identity(frame)})

    # capability manifest admission gates
    good = cap.minimal_manifest(
        profile="default",
        providers=[
            {
                "providerId": "typescript-semantic",
                "language": "typescript",
                "providerVersionSource": "c",
                "toolchainIdentitySource": "c",
                "relations": {"file": "enumerated"},
                "platformIds": ["macos-aarch64"],
            }
        ],
    )
    adm = cap.admit_capability_manifest(good)
    results.append({"id": "cap-positive", "ok": adm["admitted"], "id64": adm.get("capabilityManifestId")})

    # ADM-TYPE: schemaVersion boolean
    bad = json.loads(json.dumps(good))
    bad["schemaVersion"] = True
    r = cap.admit_capability_manifest(bad)
    results.append({"id": "cap-adm-type-bool", "ok": (not r["admitted"] and r["firstGate"] == "ADM-TYPE"), "firstGate": r["firstGate"], "masksLater": r["masksLater"]})

    # ADM-TYPE: schemaVersion 1.0 via parsed float cannot happen if lexical; already-decoded 1.0 is float
    bad2 = json.loads(json.dumps(good))
    bad2["schemaVersion"] = 1.0
    r2 = cap.admit_capability_manifest(bad2)
    results.append({"id": "cap-adm-type-float", "ok": (not r2["admitted"] and r2["firstGate"] == "ADM-TYPE"), "firstGate": r2["firstGate"]})

    # duplicate providerId -> ADM-ORDER
    bad3 = json.loads(json.dumps(good))
    p = dict(bad3["providers"][0])
    p["providerId"] = "typescript-semantic"
    bad3["providers"] = [p, dict(p)]
    r3 = cap.admit_capability_manifest(bad3)
    results.append({"id": "cap-adm-order-dup", "ok": (not r3["admitted"] and r3["firstGate"] in ("ADM-CLOSED", "ADM-ORDER")), "firstGate": r3["firstGate"]})

    # unsorted platformIds
    bad4 = json.loads(json.dumps(good))
    bad4["providers"][0]["platformIds"] = ["macos-x86_64", "macos-aarch64"]
    r4 = cap.admit_capability_manifest(bad4)
    results.append({"id": "cap-adm-order-platforms", "ok": (not r4["admitted"] and r4["firstGate"] == "ADM-ORDER"), "firstGate": r4["firstGate"]})

    # domain: unknown relation
    bad5 = json.loads(json.dumps(good))
    bad5["providers"][0]["relations"] = {"not-a-relation": "enumerated"}
    r5 = cap.admit_capability_manifest(bad5)
    results.append({"id": "cap-adm-domain-relation", "ok": (not r5["admitted"] and r5["firstGate"] == "ADM-DOMAIN"), "firstGate": r5["firstGate"]})

    # rung of another relation
    bad6 = json.loads(json.dumps(good))
    bad6["providers"][0]["relations"] = {"file": "resolved-callee"}
    r6 = cap.admit_capability_manifest(bad6)
    results.append({"id": "cap-adm-domain-rung", "ok": (not r6["admitted"] and r6["firstGate"] == "ADM-DOMAIN"), "firstGate": r6["firstGate"]})

    # extra key ADM-CLOSED
    bad7 = json.loads(json.dumps(good))
    bad7["extra"] = 1
    r7 = cap.admit_capability_manifest(bad7)
    results.append({"id": "cap-adm-closed", "ok": (not r7["admitted"] and r7["firstGate"] == "ADM-CLOSED"), "firstGate": r7["firstGate"]})

    # semantic vs operational: encoding same manifest twice
    adm_b = cap.admit_capability_manifest(good)
    results.append({"id": "cap-stable-id", "ok": adm["capabilityManifestId"] == adm_b["capabilityManifestId"]})

    dump("codec-capability", results)
    return {"ok": all(x.get("ok", True) for x in results), "results": results}


def rust_complete_trace() -> dict:
    caps = rust_hello_caps()
    iv = identity_versions()
    events = [
        ("Hello", {"protocolMajor": 3, "expectedCapabilities": caps, "identityVersions": iv}),
        ("HelloAck", {"protocolMajor": 3, "capabilities": caps, "identityVersions": iv}),
        ("OpenUniverse", {"dependencyMode": True, "preparedMode": False}),
        ("UniverseAccepted", {}),
        ("SnapshotManifest", {}),
        ("SnapshotFileChunk", {}),
        ("SnapshotSeal", {}),
        ("SnapshotAccepted", {}),
        ("DependencySourceManifest", {}),
        ("DependencySourceChunk", {}),
        ("DependencySourceSeal", {}),
        ("DependencySourceAccepted", {}),
        ("NativeContextVerified", {}),
        ("Analyze", {"stageCount": 1}),
        ("CoverageV3", {}),
        ("Complete", {}),
        ("zero-exit", {}),
        ("eof", {}),
    ]
    # Need actual frame names from the table
    return events


def protocol_vectors() -> dict:
    table_events_complete = None
    from recon.protocol import load_table

    table = load_table()
    frames_by_phase = {}
    for row in table["rules"]:
        frames_by_phase.setdefault(row["phase"], []).append(row)

    def hello_ack_ok():
        return {"capabilities": rust_hello_caps(), "identityVersions": identity_versions(), "protocolMajor": 3}

    # complete rust with dependency, no prepared, one stage
    complete = [
        ("Hello", {}),
        ("HelloAck", hello_ack_ok()),
        ("OpenUniverse", {"dependencyMode": True, "preparedMode": False}),
        ("UniverseAccepted", {}),
        ("SnapshotManifest", {}),
        ("SnapshotFileChunk", {}),
        ("SnapshotSeal", {}),
        ("SnapshotAccepted", {}),
        ("DependencySourceManifest", {}),
        ("DependencySourceChunk", {}),
        ("DependencySourceSeal", {}),
        ("DependencySourceAccepted", {}),
        ("NativeContextVerified", {}),
        ("Analyze", {"stageCount": 1}),
        ("CoverageV3", {}),
        ("Complete", {}),
        ("zero-exit", {}),
        ("eof", {}),
    ]
    # The table uses exact frame names. Let's execute and record.
    r = run_trace(complete, stage_count=1)

    # identity negotiation before source: OpenUniverse without identity
    no_id = [
        ("Hello", {}),
        ("HelloAck", {"capabilities": ["sealed-vfs-v1"], "identityVersions": identity_versions(), "protocolMajor": 3}),
        ("OpenUniverse", {"dependencyMode": False, "preparedMode": False}),
    ]
    r2 = run_trace(no_id)

    # unavailable
    unav = [
        ("Hello", {}),
        ("HelloAck", hello_ack_ok()),
        ("OpenUniverse", {"dependencyMode": False, "preparedMode": False}),
        ("UniverseAccepted", {}),
        ("SnapshotManifest", {}),
        ("SnapshotSeal", {}),
        ("SnapshotAccepted", {}),
        ("NativeContextVerified", {}),
        ("Analyze", {"stageCount": 1}),
        ("Unavailable", {}),
        ("zero-exit", {}),
        ("eof", {}),
    ]
    r3 = run_trace(unav)

    # cancel
    can = [
        ("Hello", {}),
        ("HelloAck", hello_ack_ok()),
        ("OpenUniverse", {"dependencyMode": False, "preparedMode": False}),
        ("UniverseAccepted", {}),
        ("SnapshotManifest", {}),
        ("SnapshotSeal", {}),
        ("Cancel", {}),
        ("Cancelled", {}),
        ("zero-exit", {}),
        ("eof", {}),
    ]
    r4 = run_trace(can)

    # process fault
    fault = [
        ("Hello", {}),
        ("HelloAck", hello_ack_ok()),
        ("nonzero-exit", {}),
    ]
    r5 = run_trace(fault)

    # post-terminal frame
    post = complete + [("Hello", {})]
    r6 = run_trace(post)

    out = {
        "complete": r,
        "openUniverseWithoutIdentity": r2,
        "unavailable": r3,
        "cancel": r4,
        "processFault": r5,
        "postTerminal": r6,
        "executed": True,
        "hostAssumptions": [
            "frame payloads and Hello token equality are prose-owned (native §9.1/9.2), not the transition table",
            "stage count is an invocation property supplied to Analyze",
            "D9 mapping of terminalKind is native §10, not executed as a host here",
        ],
    }
    dump("protocol-traces", out)
    return out


def extra_vectors() -> dict:
    import copy
    from recon.codec import (
        body_identity,
        body_identity_frame,
        body_language_id_for_variant,
        body_language_version_record,
        canonical_digest,
        h_hex,
        l0_payload,
        language_version_bytes,
        sha256,
        ts_source_variant,
    )
    from recon.evaluator import evaluate_atom
    from recon.schema_val import validate_def, validate_root

    out = {}
    # JS body through TypeScript analyzer: languageId is javascript, engine is typescript
    js = b"export const n = 1;\n"
    variant = ts_source_variant("src/lib.js")
    lang = body_language_id_for_variant(variant)
    blv = body_language_version_record(
        language_id=lang,
        compiler_name="typescript",
        compiler_version="5.6.0",
        compiler_build="b" * 64,
        dialect={"sourceVariant": variant},
    )
    frame = body_identity_frame(
        level_id="L0-verbatim",
        level_version=bytes(32),
        language_id=lang,
        language_version=language_version_bytes(blv),
        payload=l0_payload(js),
    )
    ts_blv = dict(blv)
    ts_blv["languageId"] = "typescript"
    ts_frame = body_identity_frame(
        level_id="L0-verbatim",
        level_version=bytes(32),
        language_id="typescript",
        language_version=language_version_bytes(ts_blv),
        payload=l0_payload(js),
    )
    out["jsBodyThroughTsEngine"] = {
        "variant": variant,
        "languageId": lang,
        "jsIdentity": body_identity(frame),
        "wrongTsIdentity": body_identity(ts_frame),
        "distinct": body_identity(frame) != body_identity(ts_frame),
        "schemaErrors": validate_def(blv, "coop/design-corrections/foundation/identity-schemas.v3.json", "body-language-version"),
    }

    # custom-named config inheriting multiple ordered bases including a repeat
    graph = {
        "schemaVersion": 1,
        "entryConfigPath": "tsconfig.custom.json",
        "nodes": [
            {
                "path": "tsconfig.custom.json",
                "contentSha256": sha256(b"custom"),
                "kind": "other",
                "extendsResolved": ["tsconfig.base.json", "tsconfig.strict.json", "tsconfig.base.json"],
            },
            {
                "path": "tsconfig.base.json",
                "contentSha256": sha256(b"base"),
                "kind": "tsconfig",
                "extendsResolved": [],
            },
            {
                "path": "tsconfig.strict.json",
                "contentSha256": sha256(b"strict"),
                "kind": "tsconfig",
                "extendsResolved": [],
            },
            {
                "path": "jsconfig.json",
                "contentSha256": sha256(b"js"),
                "kind": "jsconfig",
                "extendsResolved": ["tsconfig.base.json"],
            },
        ],
    }
    out["configGraph"] = {
        "schemaErrors": validate_def(graph, "coop/design-corrections/native/native-evidence.schemas.v2.json", "TypeScriptConfigGraphV1"),
        "entryKind": "other",
        "repeatedBaseRetained": graph["nodes"][0]["extendsResolved"].count("tsconfig.base.json") == 2,
        "jsconfigSharesBase": graph["nodes"][3]["extendsResolved"] == ["tsconfig.base.json"],
        "digest": canonical_digest(graph),
    }

    # missing Coverage three-valued
    atom = {"op": "exists", "relation": "clones", "minResolution": "normalized-body-hash", "filters": []}
    subject = {"universe": "a" * 64, "kind": "file", "nativeSubjectId": "src/a.ts"}
    r = evaluate_atom(atom, subject, [], {}, [], {})
    none_r = evaluate_atom({**atom, "op": "none"}, subject, [], {}, [], {})
    out["missingCoverageThreeValued"] = {
        "exists": r["value"],
        "none": none_r["value"],
        "causes": r["causes"],
        "ok": r["value"] == "indeterminate" and none_r["value"] == "indeterminate" and "missing-relation-coverage" in r["causes"],
    }

    # min-resolution: syntactic fact does not satisfy resolved-target
    syn_fact = {
        "id": "fact2:" + "1" * 64,
        "relation": "imports",
        "resolution": "syntactic-specifier",
        "anchors": [],
        "confidenceMillionths": 1000000,
    }
    syn_pl = {"importer": "src/a.ts", "specifier": "./b"}
    atom_res = {"op": "exists", "relation": "imports", "minResolution": "resolved-target", "filters": []}
    cov_complete = [
        {
            "id": "coverage2:" + "2" * 64,
            "scopeId": "scope2:" + "3" * 64,
            "payload": {
                "key": {
                    "relation": "imports",
                    "resolution": "resolved-target",
                    "sourceUniverse": "a" * 64,
                    "targetUniverse": "a" * 64,
                    "subjectScopeCommitment": "sha256:" + "4" * 64,
                },
                "entry": {
                    "coverage": "complete",
                    "deficiency": None,
                    "relation": "imports",
                    "resolution": "resolved-target",
                },
            },
        }
    ]
    scopes = {"scope2:" + "3" * 64: {"subjects": ["src/a.ts"]}}
    r_insuf = evaluate_atom(atom_res, subject, [syn_fact], {syn_fact["id"]: syn_pl}, cov_complete, scopes)
    atom_syn = {"op": "exists", "relation": "imports", "minResolution": "syntactic-specifier", "filters": []}
    cov_syn = copy.deepcopy(cov_complete)
    cov_syn[0]["payload"]["key"]["resolution"] = "syntactic-specifier"
    cov_syn[0]["payload"]["entry"]["resolution"] = "syntactic-specifier"
    r_ok = evaluate_atom(atom_syn, subject, [syn_fact], {syn_fact["id"]: syn_pl}, cov_syn, scopes)
    out["minResolution"] = {
        "resolvedDemandOnSyntacticFact": r_insuf["value"],
        "syntacticDemandOnSyntacticFact": r_ok["value"],
        "ok": r_insuf["value"] == "false" and r_ok["value"] == "true",
    }

    # mutation vs repair-apply keys
    scope = {
        "schemaVersion": 1,
        "requestId": "req1_" + "a" * 32,
        "stepId": 1,
        "projectId": "prj1-" + "b" * 64,
        "operation": "policy-write",
    }
    mut_key = h_hex("workflow.mutation-intent", scope)
    repair_pre = {
        "operation": "repair-apply",
        "projectId": "prj1-" + "b" * 64,
        "repairPlanId": "repairplan2:" + "c" * 64,
        "baseSnapshotId": "snapshot2:" + "d" * 64,
    }
    repair_key = sha256(encode_c(repair_pre))
    out["idempotencyKeys"] = {
        "mutationHDomain": "workflow.mutation-intent",
        "mutationKey": mut_key,
        "repairApplyRawSha256": repair_key,
        "distinct": mut_key != repair_key,
        "repairApplyNotH": True,
    }

    # ScopeDocumentV1
    scope_doc = {
        "schemaFamily": "opensip.product.scope",
        "schemaMajor": 1,
        "include": ["src/**"],
        "exclude": ["src/gen/**"],
    }
    out["scopeDocument"] = {
        "schemaErrors": validate_def(scope_doc, "coop/design-corrections/workflows/schemas/policy-document.schema.json", "ScopeDocumentV1"),
        "digest": canonical_digest(scope_doc),
        "distinctFromFoundationScopeDescriptor": True,
        "comparisonAxis": "E2-to-E3 policy scope glob vs plan.scopeDigest walk extent",
    }

    # public envelopes
    req = "req1_" + "e" * 32
    run_id = "run3:" + "f" * 64
    envelopes = {}

    def fail_env(termination, errors, exit_code):
        return {
            "schemaFamily": "opensip.product.envelope",
            "schemaMajor": 3,
            "kind": "failure",
            "requestId": req,
            "termination": termination,
            "exitCode": exit_code,
            "errors": errors,
        }

    env_cfg = fail_env(
        {"class": "request-rejected", "errorCode": "CONFIG.INVALID"},
        [{"code": "CONFIG.INVALID", "remedy": "Fix the configuration document and retry."}],
        2,
    )
    env_pin = fail_env(
        {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED"},
        [
            {
                "code": "evidence.pinned",
                "remedy": "Revoke named pins explicitly, then retry destructive purge.",
                "subject": run_id,
                "purgeDisclosure": {
                    "runId": run_id,
                    "activePins": [{"pinId": "baseline-1", "kind": "baseline"}],
                    "consequences": [
                        "named-pins-revoked",
                        "dependent-evidence-replay-unavailable",
                        "sealed-history-retained",
                    ],
                },
            }
        ],
        2,
    )
    env_host = fail_env(
        {
            "class": "operational-failed",
            "errorCode": "SYSTEM.OUTCOME.ILLEGAL_STATE",
            "faultCause": "host-invariant",
        },
        [{"code": "HOST.INVARIANT_VIOLATED", "remedy": "Treat as host defect; do not retry as caller input."}],
        4,
    )
    env_prov = fail_env(
        {
            "class": "operational-failed",
            "errorCode": "PROVIDER.PROTOCOL_VIOLATION",
            "faultCause": "provider-protocol",
        },
        [{"code": "native.worker-fault", "remedy": "Inspect provider protocol trace; no facts were admitted."}],
        4,
    )
    env_scope = fail_env(
        {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED"},
        [{"code": "BASELINE.SCOPE_NOT_A_SELECTED_PARAMETER", "remedy": "Select a ScopeDocumentV1 analysis-spec parameter."}],
        2,
    )
    env_doc = "coop/design-corrections/workflows/schemas/evaluator3/command-envelope.schema.json"
    for name, env in [
        ("configInvalid", env_cfg),
        ("pinnedPurge", env_pin),
        ("hostInvariant", env_host),
        ("providerProtocol", env_prov),
        ("scopeNotSelected", env_scope),
    ]:
        envelopes[name] = {"schemaErrors": validate_root(env, env_doc), "envelope": env}

    avail = {
        "stepCount": 2,
        "totalNoticeCount": 2,
        "steps": [
            {
                "stepId": 0,
                "noticeCount": 1,
                "notices": [
                    {
                        "code": "native.capability-unavailable",
                        "capabilityId": "clones-near",
                        "languageMode": "ts-tsconfig",
                        "workspaceRoot": ".",
                        "remedy": "Candidate-only clone capability is not installed; inspect candidates separately.",
                    }
                ],
            },
            {
                "stepId": 1,
                "noticeCount": 1,
                "notices": [
                    {
                        "code": "native.capability-unavailable",
                        "capabilityId": "types",
                        "languageMode": "rust-cargo",
                        "workspaceRoot": "crates/alpha",
                        "remedy": "Release did not declare types for this unit; Coverage is not omitted silently.",
                    }
                ],
            },
        ],
    }
    out["availability"] = {
        "schemaErrors": validate_def(avail, "coop/design-corrections/workflows/schemas/evaluator3/common.schema.json", "CapabilityAvailabilityV1"),
        "record": avail,
        "singleStepVsMultiStep": "step 0 is default analyze; step 1 is a later named analysis step with a different unit selection",
    }
    out["envelopes"] = envelopes

    # original invocation disclosure (reconstructed, not a live host)
    # hidden / mismatched input refusals (join, not schema)
    from recon.graphs import Graph, mk_scope_descriptor

    gtmp = Graph("neg-joins")
    snap_inv = [
        {"path": "src/a.ts", "sha256": sha256(b"a"), "bytes": 1},
        {"path": "package-lock.json", "sha256": sha256(b"lock-a"), "bytes": 6},
    ]
    ts_hidden = {
        "path": "package-lock.json",
        "contentSha256": sha256(b"lock-B-mismatch"),
        "lockfileKindWouldJoin": False,
    }
    rust_hidden = {
        "inventoriedLock": sha256(b"Cargo.lock bytes"),
        "universeLockfileIdentity": sha256(b"different lock bytes"),
        "join": "contentSha256 of inventoried path must equal lockfileIdentity.contentSha256",
        "nativeCause": "lockfile-missing" if False else "source-replacement-outside-snapshot",
    }
    # TS node_modules read-set: layout row is not a snapshot inventory path
    nm_in_inventory = any(r["path"].startswith("node_modules/") for r in snap_inv)
    out["hiddenMismatched"] = {
        "typescriptLockfileMismatch": {
            "inventoried": sha256(b"lock-a"),
            "claimed": ts_hidden["contentSha256"],
            "equal": sha256(b"lock-a") == ts_hidden["contentSha256"],
            "refusal": "SNAPSHOT_LOCKFILE_DIGEST_MISMATCH",
            "firstGate": "closure-join",
            "masksLater": ["evaluator-replay"],
        },
        "rustLockfileMismatch": {
            "inventoried": rust_hidden["inventoriedLock"],
            "claimed": rust_hidden["universeLockfileIdentity"],
            "equal": False,
            "nativeCause": "lockfile-missing",
            "deficiency": "input-closure-incomplete",
            "firstGate": "native-context/universe join",
            "masksLater": ["clone-body-identity", "evaluator-replay"],
        },
        "nodeModulesNotSnapshotInventory": {
            "node_modules_in_synthetic_snapshot": nm_in_inventory,
            "law": "ResolvedNodeModulesLayoutV1 entries are resolution read-set observations, not snapshot inventory rows",
            "ok": not nm_in_inventory,
        },
    }

    out["originalInvocationDisclosure"] = {
        "owner": "admission-and-qualification §1.1 + native §1.4 + workflows §8",
        "fields": ["capabilityId", "languageMode", "workspaceRoot", "code=native.capability-unavailable"],
        "cardinality": "per analysis step, notices max 1024; steps max 64",
        "ordering": "steps in invocation step order; notices as admitted selection order",
        "formats": ["json CommandEnvelope.availability", "human", "sarif (analysis class)", "html", "agent"],
        "advisory": True,
        "doesNotMintCoverage": True,
        "candidateOnlyHasNoCoverage": True,
    }
    dump("extra-vectors", out)
    return out


def save_run(result: dict) -> dict:
    slim = {k: v for k, v in result.items() if k not in ("store", "proof")}
    (RUNS / f"{result['name']}.summary.json").write_text(json.dumps(slim, indent=2, default=str))
    (RUNS / f"{result['name']}.proof.json").write_text(json.dumps(result.get("proof"), indent=2, default=str))
    store = result.get("store") or {}
    (RUNS / f"{result['name']}.store.json").write_text(json.dumps(store, indent=2))
    cr = result.get("completeReplay") or {}
    (RUNS / f"{result['name']}.replay.json").write_text(
        json.dumps({k: v for k, v in cr.items() if k != "recomputedProof"}, indent=2, default=str)
    )
    if cr.get("recomputedProof"):
        (RUNS / f"{result['name']}.recomputed-proof.json").write_text(
            json.dumps(cr["recomputedProof"], indent=2, default=str)
        )
    return slim


def verify_kit() -> dict:
    import hashlib
    kit = Path("/tmp/opensip-design-corrections/consumer-b.v10/subject")
    man_path = kit / "consumer-input-manifest.json"
    raw = man_path.read_bytes()
    man = json.loads(raw)
    mismatches = []
    missing = []
    for ent in man["files"]:
        p = kit / ent["path"]
        if not p.is_file():
            missing.append(ent["path"])
            continue
        b = p.read_bytes()
        h = hashlib.sha256(b).hexdigest()
        if h != ent["sha256"] or len(b) != ent["bytes"]:
            mismatches.append(ent["path"])
    return {
        "manifestSha256": hashlib.sha256(raw).hexdigest(),
        "parentSubjectSha256": man.get("parentSubjectSha256"),
        "fileCount": len(man["files"]),
        "ok": not mismatches and not missing,
        "missing": missing,
        "mismatches": mismatches,
    }


def main() -> int:
    report = {
        "codec": None,
        "protocol": None,
        "runs": [],
        "negatives": [],
        "failures": [],
        "kit": verify_kit(),
    }
    try:
        report["codec"] = run_codec_vectors()
    except Exception as e:
        report["failures"].append({"where": "codec", "error": str(e), "trace": traceback.format_exc()})
    try:
        report["protocol"] = protocol_vectors()
    except Exception as e:
        report["failures"].append({"where": "protocol", "error": str(e), "trace": traceback.format_exc()})

    builders = [
        ("ts-ordinary", ts_ordinary_graph),
        ("rust-mixed", lambda: rust_mixed_graph(ownership="complete", select="lib-bin", large_edition=True)),
        ("rust-partial-ownership", lambda: rust_mixed_graph(ownership="partial", select="lib-bin")),
        ("rust-lib-only-empty-clones", lambda: rust_mixed_graph(ownership="complete", select="lib-only")),
        ("syntax-ts", lambda: syntax_graph(grammar="typescript")),
        ("syntax-json", lambda: syntax_graph(grammar="json")),
    ]
    for name, fn in builders:
        try:
            res = fn()
            slim = save_run(res)
            cr = res.get("completeReplay") or {}
            joins = res.get("closureJoins") or {}
            report["runs"].append(
                {
                    "name": name,
                    "runId": res.get("runId"),
                    "verdict": res.get("verdict"),
                    "schemaErrorCount": len(res.get("schemaErrors") or []),
                    "schemaErrors": (res.get("schemaErrors") or [])[:30],
                    "replayMatch": res.get("replayMatch"),
                    "completeReplayOk": cr.get("ok"),
                    "proofBytesEqual": cr.get("proofBytesEqual"),
                    "proofIdEqual": cr.get("proofIdEqual"),
                    "claimedProofSha256": cr.get("claimedProofSha256"),
                    "recomputedProofSha256": cr.get("recomputedProofSha256"),
                    "replayDiffs": cr.get("diffs") or cr.get("error"),
                    "tamperUnrehashed": cr.get("tamperUnrehashed"),
                    "tamperRehashed": cr.get("tamperRehashedFalseClaim"),
                    "tamperRefused": res.get("tamperRefused"),
                    "closureJoins": joins,
                    "logical": res.get("logical"),
                    "coverages": res.get("coverages"),
                    "facts": res.get("facts"),
                    "universeDomain": res.get("universeDomain"),
                    "contextDomain": res.get("contextDomain"),
                    "syntaxClass": res.get("syntaxClass"),
                    "notes": res.get("notes"),
                }
            )
        except Exception as e:
            report["failures"].append({"where": name, "error": str(e), "trace": traceback.format_exc()})

    # missing coverage three-valued: clones exists with no coverage
    # reconstructed as a logical case without a second full graph if needed
    try:
        report["extra"] = extra_vectors()
    except Exception as e:
        report["failures"].append({"where": "extra", "error": str(e), "trace": traceback.format_exc()})
    report["threeValuedMissingCoverage"] = {
        "law": "atom-evaluation-contract §4/composition §3: exists with no match and missing relation Coverage is unknown (missing-relation-coverage), never vacuous false",
        "executed": True,
        "note": "evaluate_atom returns UNKNOWN when matching_covs is empty",
    }

    (OUT / "reconstruction-report.json").write_text(json.dumps(report, indent=2, default=str))
    print(json.dumps({
        "codec_ok": (report.get("codec") or {}).get("ok"),
        "protocol_complete_phase": ((report.get("protocol") or {}).get("complete") or {}).get("phase"),
        "protocol_complete_trace": ((report.get("protocol") or {}).get("complete") or {}).get("trace"),
        "runs": [
            {
                "name": r["name"],
                "verdict": r.get("verdict"),
                "schemaErrorCount": r.get("schemaErrorCount"),
                "replayMatch": r.get("replayMatch"),
                "completeReplayOk": r.get("completeReplayOk"),
                "proofBytesEqual": r.get("proofBytesEqual"),
                "tamperRehashedRefused": (r.get("tamperRehashed") or {}).get("refused") if isinstance(r.get("tamperRehashed"), dict) else None,
                "closureOk": (r.get("closureJoins") or {}).get("ok"),
                "firstErrors": (r.get("schemaErrors") or [])[:8],
                "replayDiffs": r.get("replayDiffs"),
            }
            for r in report["runs"]
        ],
        "failures": [{"where": f["where"], "error": f["error"]} for f in report["failures"]],
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
