"""Provider handshake and startup payload admission (source44, HC-58): typescript-semantic major 2 and rust-semantic major 3.

Normative sources (kit bytes only; no author code consulted):
  native-evidence.md s9.1 lines 2783-2866 (both handshakes, token-array order, reject-before-disclosure), s9.2 lines 2872-2904 (frame table, derived
    modes), s9.3 lines 2929-2942 (ProtocolLimitsV3), s9.4 lines 2944-3001 (TypeScript major 2), s9.7 lines 3151-3294 (startup payloads, pre-Analyze
    Unavailable and host conversion, Coverage wrappers, TypeScript cancellation), s0 rows 119-129 (superseded selectors)
  native/provider-handshake.schemas.v1.json (whole document including #/x-opensip-wire-law)
  native/provider-startup.schemas.v1.json (whole document including #/x-opensip-startup-law)
  native/native-evidence.schemas.v2.json #/$defs/CoverageResultV3, RepositoryResolutionV3, TypeScriptUniverseV2ResolvedInputs, RustUniverseV2ResolvedInputs
  artifacts/delivery.v2.json typescriptSemanticSubstrate.providerProtocol.wireSchema.limits / canonicalCbor / payloadSchemas.CancelledV1
  artifacts/rust-provider-protocol.v2.json limits, limitsHandshake, canonicalCbor (and its raw bytes for expectedProtocolContractSha256)
  foundation identity H recipe (native semantic-universe identity, native-evidence s11; ref/canonical.H)

Internal refusal keys are the reconstruction's own and carry the cb24. prefix (advisory A-c1). A worker payload refusal is PROVIDER.PROTOCOL_VIOLATION
(stage_authority fault law); a host-authored payload refusal is a host invariant.

Scope follows the kit's own reference scope for s9.7:
  - executed: schemas, handshake joins, startup cross-record joins, Coverage wrapper shape and requested-key correspondence, the TypeScript
    observedPhase interval, the pre-Analyze host conversion through CoverageResultV3 admission;
  - not executed: commitment recomputation for Coverage wrappers, the complete inherited Cancel/Cancelled record, correlation, Rust Cancelled
    phase law beyond exact concrete phase equality, framing bytes, processes or compilers.

source45 (HC-60): the host conversion's closedWorld is now published as one exact value. It appears in native-evidence s9.7 (the JSON block under the
closedWorld bullet) and in provider-startup #/x-opensip-startup-law/preAnalyzeUnavailable/hostConversionClosedWorld. Both owners are read and must
agree. pre_analyze_conversion takes no closedWorld argument, and a minted conversion entry whose closedWorld differs from the published value refuses
cb24.CONVERSION_CLOSED_WORLD_NOT_PUBLISHED. The source44 bytes of this file are preserved at preserved/s44-final/ref/provider_wire.py.
"""
import hashlib
import json
import re

import canonical as K
import factbatch as FB
import native_facts as NF
import protocol3 as P
import wirecbor as WC

KIT = FB.K
HS = "native/provider-handshake.schemas.v1.json"
ST = "native/provider-startup.schemas.v1.json"
NE = "native/native-evidence.schemas.v2.json"
DELIVERY = "coop/artifacts/delivery.v2.json"
RUST = "coop/artifacts/rust-provider-protocol.v2.json"
NATIVE_MD = FB.schemas.KIT_DOCS + "v2/contracts/product-v1/native-evidence.md"
IDENTITY_TOKENS = ["source-identity-snapshot2", "plan-identity-plan2", "fact-identity-fact2", "coverage-v3"]
IDENTITY_VERSIONS = {"snapshot": 2, "plan": 2, "fact": 2, "coverage": 3}
WIRE_LAW = KIT.doc(HS)["x-opensip-wire-law"]
STARTUP_LAW = KIT.doc(ST)["x-opensip-startup-law"]

# ---------------------------------------------------------------- limits, derived from the inherited artifacts and native s9.3 prose
TS_LIMITS = {k: v for k, v in KIT.doc(DELIVERY)["typescriptSemanticSubstrate"]["providerProtocol"]["wireSchema"]["limits"].items() if k != "limitRule"}
RUST_LIMITS_V2 = dict(KIT.doc(RUST)["limits"])
_md = open(NATIVE_MD, encoding="utf-8").read()
_s93 = _md[_md.index("### 9.3 Limits"):_md.index("### 9.4 TypeScript major 2")]
_s93_members = dict((m, int(v)) for m, v in re.findall(r"`(max[A-Za-z]+) (\d+)`", _s93.split("All 24 v2 limits")[0]))
LIMITS_V3 = dict(RUST_LIMITS_V2, **_s93_members)
assert len(TS_LIMITS) == 10 and len(RUST_LIMITS_V2) == 24 and len(_s93_members) == 8 and len(LIMITS_V3) == 32
HOST_CONVERSION_CLOSED_WORLD = STARTUP_LAW["preAnalyzeUnavailable"]["hostConversionClosedWorld"]
_s97 = _md[_md.index("### 9.7 Startup frames"):_md.index("## 10. Deficiencies")]
_cw_bullet = _s97[_s97.index("`closedWorld`: exactly the complete value below"):]
_cw_json = _cw_bullet[_cw_bullet.index("```json") + len("```json"):]
MD_HOST_CONVERSION_CLOSED_WORLD = json.loads(_cw_json[:_cw_json.index("```")])
HOST_CONVERSION_CLOSED_WORLD_OWNERS_AGREE = MD_HOST_CONVERSION_CLOSED_WORLD == HOST_CONVERSION_CLOSED_WORLD
CONTRACT_SHA256 = KIT.digest(RUST)
CONTRACT_PINNED = WIRE_LAW["expectedProtocolContractSha256"]["sha256"]
TS_DESCRIPTOR = WIRE_LAW["typescriptDescriptorBinding"]
RUST_IDENTITY = WIRE_LAW["rustIdentityBinding"]


def schema_limits_consts(selector):
    return {k: v["const"] for k, v in KIT.doc(HS)["$defs"][selector]["properties"].items()}


LIMIT_CROSS_CHECK = {"TypeScriptProtocolLimitsV1 consts == delivery.v2 limits": schema_limits_consts("TypeScriptProtocolLimitsV1") == TS_LIMITS,
                     "ProtocolLimitsV3 consts == rust-provider-protocol.v2 limits + native s9.3": schema_limits_consts("ProtocolLimitsV3") == LIMITS_V3,
                     "pinned contract digest == raw SHA-256 of rust-provider-protocol.v2.json": CONTRACT_PINNED == CONTRACT_SHA256}


def fault(key, detail=""):
    return {"key": key, "detail": str(detail)[:400]}


def schema_faults(value, doc, selector, key):
    r = KIT.admit(value, doc, selector)
    if r["ok"]:
        return []
    return [fault(key, FB._summary(r))]


def jcs(value):
    """RFC 8785 bytes for the synthetic descriptors used here: every key and string is ASCII and every number an integer, for which RFC 8785 equals
    sorted-key compact JSON. Anything else raises instead of being approximated."""
    def check(v):
        if isinstance(v, dict):
            for k, x in v.items():
                assert isinstance(k, str) and k.isascii()
                check(x)
        elif isinstance(v, list):
            for x in v:
                check(x)
        else:
            assert v is None or type(v) in (bool, int) or (isinstance(v, str) and v.isascii()), v
    check(value)
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("ascii")


def descriptor_digest(descriptor):
    return hashlib.sha256(jcs(descriptor)).hexdigest()


# ---------------------------------------------------------------- handshake
def admit_hello(lang, hello, trusted):
    if lang == "ts":
        out = schema_faults(hello, HS, "#/$defs/TypeScriptHelloV2", "cb24.HELLO_SCHEMA")
        if not isinstance(hello, dict):
            return out
        limits = hello.get("limits")
        if not FB.same(limits, TS_LIMITS):
            out.append(fault("cb24.HELLO_LIMITS", "limits are not exactly delivery.v2 wireSchema.limits numeric members"))
        if hello.get("hostBuildId") != trusted["hostBuildId"]:
            out.append(fault("cb24.HELLO_HOST_BUILD_ID"))
        if hello.get("expectedProviderDescriptorSha256") != descriptor_digest(trusted["providerDescriptor"]):
            out.append(fault("cb24.HELLO_DESCRIPTOR_DIGEST", "provider descriptor"))
        if hello.get("expectedRuntimeDescriptorSha256") != descriptor_digest(trusted["runtimeDescriptor"]):
            out.append(fault("cb24.HELLO_DESCRIPTOR_DIGEST", "runtime descriptor"))
    else:
        out = schema_faults(hello, HS, "#/$defs/HelloV3", "cb24.HELLO_SCHEMA")
        if not isinstance(hello, dict):
            return out
        limits = hello.get("limits")
        if not FB.same(limits, LIMITS_V3):
            out.append(fault("cb24.HELLO_LIMITS", "limits are not exactly ProtocolLimitsV3 (24 inherited + 8 native s9.3 members)"))
        else:
            try:
                if WC.encode(limits) != WC.encode(LIMITS_V3):
                    out.append(fault("cb24.HELLO_LIMITS_CBOR"))
            except WC.WireCborError as exc:
                out.append(fault("cb24.HELLO_LIMITS_CBOR", exc.cls))
        if hello.get("hostBuildId") != trusted["hostBuildId"]:
            out.append(fault("cb24.HELLO_HOST_BUILD_ID"))
        if hello.get("expectedProtocolContractSha256") != CONTRACT_SHA256:
            out.append(fault("cb24.HELLO_CONTRACT_DIGEST", "not the raw SHA-256 of rust-provider-protocol.v2.json"))
        expected_identity = dict({"protocolMajor": 3}, **{f: trusted["rustV1Row"][f] for f in RUST_IDENTITY["echoFields"]})
        if not FB.same(hello.get("expectedIdentity"), expected_identity):
            out.append(fault("cb24.HELLO_EXPECTED_IDENTITY", "not the selected Plan rust-v1 row identity with protocolMajor 3"))
    if hello.get("expectedCapabilities") != trusted["signedRowTokens"]:
        out.append(fault("cb24.HELLO_TOKENS_NOT_SIGNED_ROW", "expectedCapabilities are not exactly the selected signed capability row's tokens"))
    return out


def admit_hello_ack(lang, ack, hello, trusted):
    if hello is None:
        return [fault("cb24.HELLO_NOT_ADMITTED")]
    if lang == "ts":
        out = schema_faults(ack, HS, "#/$defs/TypeScriptHelloAckV2", "cb24.HELLOACK_SCHEMA")
        if not isinstance(ack, dict):
            return out
        if ack.get("providerDescriptorSha256") != hello.get("expectedProviderDescriptorSha256") or \
                ack.get("runtimeDescriptorSha256") != hello.get("expectedRuntimeDescriptorSha256"):
            out.append(fault("cb24.HELLOACK_DESCRIPTOR_DIGEST_ECHO"))
        for f in TS_DESCRIPTOR["providerDescriptorFields"]:
            if not FB.same(ack.get(f), trusted["providerDescriptor"].get(f)):
                out.append(fault("cb24.HELLOACK_DESCRIPTOR_FIELD", f"provider descriptor {f}"))
        for f in TS_DESCRIPTOR["runtimeDescriptorFields"]:
            if not FB.same(ack.get(f), trusted["runtimeDescriptor"].get(f)):
                out.append(fault("cb24.HELLOACK_DESCRIPTOR_FIELD", f"runtime descriptor {f}"))
    else:
        out = schema_faults(ack, HS, "#/$defs/HelloAckV3", "cb24.HELLOACK_SCHEMA")
        if not isinstance(ack, dict):
            return out
        ident = hello.get("expectedIdentity") or {}
        for f in RUST_IDENTITY["echoFields"]:
            if not FB.same(ack.get(f), ident.get(f)):
                out.append(fault("cb24.HELLOACK_IDENTITY_ECHO", f))
        if not FB.same(ack.get("protocolMajor"), ident.get("protocolMajor")):
            out.append(fault("cb24.HELLOACK_PROTOCOL_MAJOR"))
    if ack.get("capabilities") != hello.get("expectedCapabilities"):
        out.append(fault("cb24.HELLOACK_TOKEN_ECHO", "capabilities are not the exact echo of Hello expectedCapabilities"))
    if not FB.same(ack.get("identityVersions"), hello.get("identityVersions")):
        out.append(fault("cb24.HELLOACK_IDENTITY_VERSIONS_ECHO"))
    return out


# ---------------------------------------------------------------- startup
def universe_identity(lang, resolved_inputs):
    return "sha256:" + K.H(f"native.semantic-universe.{'typescript' if lang == 'ts' else 'rust'}.v2", resolved_inputs)


def admit_open_universe(lang, ou, ctx):
    sel = "#/$defs/TypeScriptOpenUniverseV2" if lang == "ts" else "#/$defs/OpenUniverseV3"
    out = schema_faults(ou, ST, sel, "cb24.OPEN_UNIVERSE_SCHEMA")
    if not isinstance(ou, dict) or not isinstance(ou.get("universe"), dict):
        return out, None
    plan = ctx["plan"]
    if ou.get("executionId") != ctx["executionId"]:
        out.append(fault("cb24.OPEN_UNIVERSE_EXECUTION_ID"))
    if ou.get("planIntentCommitment") != ctx["planIntentCommitment"]:
        out.append(fault("cb24.OPEN_UNIVERSE_PLAN_INTENT"))
    if ou.get("snapshotId") != plan["snapshotId"]:
        out.append(fault("cb24.OPEN_UNIVERSE_SNAPSHOT_ID", "snapshotId is not the verified Plan snapshot2 text"))
    if ou.get("planId") != plan["planId"]:
        out.append(fault("cb24.OPEN_UNIVERSE_PLAN_ID", "planId is not the verified plan2 text"))
    ri = ou["universe"].get("resolvedInputs") or {}
    ctx_id = ri.get("nativeContextId")
    if not (isinstance(ctx_id, str) and ctx_id[7:] in plan["nativeContextDigests"]):
        out.append(fault("cb24.OPEN_UNIVERSE_NATIVE_CONTEXT_NOT_PLAN", "resolvedInputs.nativeContextId suffix is not in plan.nativeContextDigests"))
    law = STARTUP_LAW["typescriptOpenUniverse" if lang == "ts" else "rustOpenUniverse"]
    if lang == "ts":
        ack = ctx["helloAck"] or {}
        for f in law["handshakeJoin"]:
            if not FB.same(ou["universe"].get(f), ack.get(f)):
                out.append(fault("cb24.OPEN_UNIVERSE_HANDSHAKE_JOIN", f"universe.{f} != TypeScriptHelloAckV2.{f}"))
        try:
            if ou.get("universeKey") != universe_identity("ts", ri):
                out.append(fault("cb24.OPEN_UNIVERSE_UNIVERSE_KEY", "universeKey is not sha256:H(native.semantic-universe.typescript.v2, resolvedInputs)"))
        except Exception as exc:  # an unencodable resolvedInputs is already a schema fault
            out.append(fault("cb24.OPEN_UNIVERSE_UNIVERSE_KEY", f"{type(exc).__name__}"))
        return out, None
    ident = (ctx["hello"] or {}).get("expectedIdentity") or {}
    for f in law["handshakeJoin"]:
        if not FB.same(ou["universe"].get(f), ident.get(f)):
            out.append(fault("cb24.OPEN_UNIVERSE_HANDSHAKE_JOIN", f"universe.{f} != HelloV3.expectedIdentity.{f}"))
    rr = ou.get("repositoryResolution") or {}
    for f in ("dependencySourceSetId", "preparedOutputSetId"):
        if not FB.same(rr.get(f), ri.get(f)):
            out.append(fault("cb24.OPEN_UNIVERSE_REPOSITORY_RESOLUTION", f"repositoryResolution.{f} != universe.resolvedInputs.{f}"))
    prep = ctx.get("preparation")
    if rr.get("preparedOutputSetId") is None:
        if rr.get("authorizationId") is not None or rr.get("effects") is not None:
            out.append(fault("cb24.OPEN_UNIVERSE_REPOSITORY_RESOLUTION", "authorizationId and effects must be null when preparedOutputSetId is null"))
    else:
        if prep is None or rr.get("authorizationId") != prep["authorizationId"] or not FB.same(rr.get("effects"), prep["effects"]):
            out.append(fault("cb24.OPEN_UNIVERSE_REPOSITORY_RESOLUTION", "authorizationId/effects are not the selected preparation's"))
        if (rr.get("authorizationId") is None) != (rr.get("effects") is None):
            out.append(fault("cb24.OPEN_UNIVERSE_REPOSITORY_RESOLUTION", "effects must be null exactly when authorizationId is null"))
    observations = {"dependencyMode": rr.get("dependencySourceSetId") is not None, "preparedMode": rr.get("preparedOutputSetId") is not None,
                    "law": "protocol3-transitions.v1.json#/derivedObservations; provider-startup.schemas.v1.json#/x-opensip-startup-law/rustOpenUniverse/derivedModes"}
    return out, observations


def admit_universe_accepted(lang, ua, ou):
    if ou is None:
        return [fault("cb24.UNIVERSE_ACCEPTED_BEFORE_OPEN")]
    if lang == "ts":
        out = schema_faults(ua, ST, "#/$defs/TypeScriptUniverseAcceptedV2", "cb24.UNIVERSE_ACCEPTED_SCHEMA")
        members = ("executionId", "snapshotId", "planId", "universeKey")
    else:
        out = schema_faults(ua, ST, "#/$defs/UniverseAcceptedV3", "cb24.UNIVERSE_ACCEPTED_SCHEMA")
        members = ("executionId", "snapshotId", "planId", "providerId", "universe", "repositoryResolution")
    for f in members:
        if not isinstance(ua, dict) or not FB.same(ua.get(f), ou.get(f)):
            out.append(fault("cb24.UNIVERSE_ACCEPTED_ECHO", f))
    return out


def admit_native_context_verified(ncv, ou):
    out = schema_faults(ncv, ST, "#/$defs/NativeContextVerifiedV1", "cb24.NATIVE_CONTEXT_VERIFIED_SCHEMA")
    want = ((ou or {}).get("universe") or {}).get("resolvedInputs", {}).get("nativeContextId")
    if not isinstance(ncv, dict) or ncv.get("nativeContextId") != want or ncv.get("recomputedNativeContextId") != want:
        out.append(fault("cb24.NATIVE_CONTEXT_VERIFIED_JOIN", "both ids must equal OpenUniverse universe.resolvedInputs.nativeContextId"))
    return out


def classify_unavailable(lang, payload):
    if KIT.admit(payload, ST, "#/$defs/PreAnalyzeUnavailableV1")["ok"]:
        return "pre-analyze"
    if KIT.admit(payload, ST, "#/$defs/TypeScriptUnavailableV2" if lang == "ts" else "#/$defs/UnavailableV3")["ok"]:
        return "post-analyze"
    return None


def requested_keys(requests):
    return [k for r in requests for k in r["keys"]]


def key_correspondence_faults(entries, keys, key_name):
    out = []
    if not isinstance(entries, list) or len(entries) != len(keys):
        return [fault(key_name, f"{len(entries) if isinstance(entries, list) else None} entries for {len(keys)} requested keys")]
    for i, (e, k) in enumerate(zip(entries, keys)):
        ek = (e or {}).get("key") or {}
        want = {"relation": k["relation"], "resolution": k["resolution"], "subjectScopeCommitment": k["subjectScopeCommitment"],
                "sourceUniverse": k["sourceUniverseId"][7:], "targetUniverse": k["targetUniverseId"][7:]}
        if not FB.same(ek, want):
            out.append(fault(key_name, f"entries[{i}].key does not answer requested key {i}"))
        entry = (e or {}).get("entry") or {}
        if entry.get("relation") != k["relation"] or entry.get("resolution") != k["resolution"]:
            out.append(fault(key_name, f"entries[{i}].entry relation/resolution"))
    return out


def admit_unavailable(lang, payload, host_phase, ou, requests):
    kind = classify_unavailable(lang, payload)
    if kind is None:
        sel = "#/$defs/TypeScriptUnavailableV2" if lang == "ts" else "#/$defs/UnavailableV3"
        return (schema_faults(payload, ST, "#/$defs/PreAnalyzeUnavailableV1", "cb24.UNAVAILABLE_SCHEMA")[:1] +
                schema_faults(payload, ST, sel, "cb24.UNAVAILABLE_SCHEMA")[:1]), None
    out = []
    if kind == "pre-analyze":
        if host_phase != "WAIT_NATIVE_CONTEXT_VERIFIED":
            out.append(fault("cb24.UNAVAILABLE_PHASE", f"PreAnalyzeUnavailableV1 in host phase {host_phase}"))
        for f in ("executionId", "snapshotId", "planId"):
            if ou is None or payload.get(f) != ou.get(f):
                out.append(fault("cb24.UNAVAILABLE_CORRELATION", f))
        want = ((ou or {}).get("universe") or {}).get("resolvedInputs", {}).get("nativeContextId")
        if payload.get("nativeContextId") != want:
            out.append(fault("cb24.UNAVAILABLE_CORRELATION", "nativeContextId"))
        if payload.get("recomputedNativeContextId") == payload.get("nativeContextId"):
            out.append(fault("cb24.UNAVAILABLE_CONTEXTS_EQUAL", "recomputedNativeContextId must differ from nativeContextId"))
    else:
        if host_phase == "WAIT_NATIVE_CONTEXT_VERIFIED" or requests is None:
            out.append(fault("cb24.UNAVAILABLE_PHASE", f"post-Analyze Unavailable payload in host phase {host_phase}"))
        else:
            if payload.get("affectedStageIds") != [r["stageId"] for r in requests]:
                out.append(fault("cb24.UNAVAILABLE_AFFECTED_STAGES", "affectedStageIds are not every requested stageId in request order"))
            out += key_correspondence_faults(payload.get("coverage"), requested_keys(requests), "cb24.TERMINAL_COVERAGE")
            for i, e in enumerate(payload.get("coverage") or []):
                ent = (e or {}).get("entry") or {}
                if ent.get("coverage") != "unknown" or ent.get("deficiency") != "provider-unavailable":
                    out.append(fault("cb24.TERMINAL_COVERAGE", f"coverage[{i}] is not unknown/provider-unavailable"))
    return out, kind


def admit_coverage(lang, payload, request, analysis_ordinal):
    out = schema_faults(payload, ST, "#/$defs/TypeScriptCoverageV2" if lang == "ts" else "#/$defs/CoverageV3", "cb24.COVERAGE_SCHEMA")
    if not isinstance(payload, dict):
        return out
    if payload.get("stageId") != request["stageId"]:
        out.append(fault("cb24.COVERAGE_STAGE_ID", "wrapper stageId is not the current requested stage"))
    if not FB.same(payload.get("analysisOrdinal"), analysis_ordinal):
        out.append(fault("cb24.COVERAGE_ANALYSIS_ORDINAL"))
    out += key_correspondence_faults(payload.get("entries"), request["keys"], "cb24.COVERAGE_KEY_CORRESPONDENCE")
    return out


def admit_budget_exhausted(lang, payload, requests, analysis_ordinal):
    out = schema_faults(payload, ST, "#/$defs/TypeScriptBudgetExhaustedV2" if lang == "ts" else "#/$defs/BudgetExhaustedV3", "cb24.BUDGET_SCHEMA")
    if not isinstance(payload, dict) or requests is None:
        return out + ([fault("cb24.BUDGET_PHASE")] if requests is None else [])
    if payload.get("triggerStageId") not in [r["stageId"] for r in requests]:
        out.append(fault("cb24.BUDGET_TRIGGER_STAGE"))
    if not FB.same(payload.get("analysisOrdinal"), analysis_ordinal):
        out.append(fault("cb24.BUDGET_ANALYSIS_ORDINAL"))
    out += key_correspondence_faults(payload.get("coverage"), requested_keys(requests), "cb24.TERMINAL_COVERAGE")
    for i, e in enumerate(payload.get("coverage") or []):
        ent = (e or {}).get("entry") or {}
        if ent.get("coverage") != "unknown" or ent.get("deficiency") != "budget-exhausted":
            out.append(fault("cb24.TERMINAL_COVERAGE", f"coverage[{i}] is not unknown/budget-exhausted"))
    return out


TS_CANCELLED_PHASES = {"handshake", "universe", "snapshot", "analysis"}


def admit_cancelled(lang, payload, cancel_phase, cancel_payload):
    """Closed members and the inherited echo of the host's Cancel (delivery.v2 CancelledV1 'exact Cancel value'; rust-provider-protocol.v2 CancelledV2
    'execution/analysis echo Cancel'). TypeScript: observedPhase enum plus the s9.7 inserted interval (snapshot for a Cancel at
    WAIT_NATIVE_CONTEXT_VERIFIED/READY_ANALYZE); other intervals are inherited and not restated. Rust: CancelledV2.observedPhase is 'the exact concrete
    phase at Cancel receipt', a worker phase whose vocabulary no owner I can read publishes, so it is not validated here (unchanged by source44)."""
    out = []
    if not isinstance(payload, dict) or set(payload) != {"executionId", "analysisOrdinal", "observedPhase"}:
        return [fault("cb24.CANCELLED_SCHEMA", "closed members executionId, analysisOrdinal, observedPhase")]
    if cancel_payload is None or payload["executionId"] != cancel_payload.get("executionId") or \
            not FB.same(payload["analysisOrdinal"], cancel_payload.get("analysisOrdinal")):
        out.append(fault("cb24.CANCELLED_CORRELATION", "executionId/analysisOrdinal are not the exact Cancel values"))
    if lang == "ts":
        law = STARTUP_LAW["cancellation"]
        if payload["observedPhase"] not in TS_CANCELLED_PHASES:
            out.append(fault("cb24.CANCELLED_SCHEMA", "observedPhase enum handshake|universe|snapshot|analysis"))
        elif cancel_phase in law["hostPhasesAtCancel"] and payload["observedPhase"] != law["observedPhase"]:
            out.append(fault("cb24.CANCELLED_OBSERVED_PHASE", f"Cancel at {cancel_phase} requires observedPhase {law['observedPhase']}"))
    return out


# ---------------------------------------------------------------- pre-Analyze host conversion (native s9.7)
def completeness_from_stage(resolution):
    """attempted=false, stageTerminal=unavailable, examinedExhaustive=false: not-attempted on a resolved rung, not-applicable otherwise (s9.7 lines 3238-3240)."""
    resolved = resolution in NF.RESOLVED
    return {"state": "not-attempted" if resolved else "not-applicable", "attempted": False, "examinedExhaustive": False, "stageTerminal": "unavailable",
            "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []}


def mint_conversion_entry(key, subject_count, closed_world):
    entry = {"relation": key["relation"], "resolution": key["resolution"], "coverage": "unknown",
             "examinedUniverse": {"subjectScopeCommitment": key["subjectScopeCommitment"], "subjectCount": subject_count},
             "resolutionCompleteness": completeness_from_stage(key["resolution"]), "closedWorld": closed_world, "derivationKinds": [],
             "confidenceMillionths": 0, "deficiency": "provider-unavailable", "nativeCause": None}
    return {"schemaVersion": 3, "key": {"relation": key["relation"], "resolution": key["resolution"], "sourceUniverse": key["sourceUniverseId"][7:],
                                        "subjectScopeCommitment": key["subjectScopeCommitment"], "targetUniverse": key["targetUniverseId"][7:]}, "entry": entry}


def admit_minted_entry(result):
    """CoverageResultV3 schema plus the RC-1/RC-2/RC-6 relations and the cause registry that apply to a host-minted, fact-free entry."""
    out = schema_faults(result, NE, "#/$defs/CoverageResultV3", "cb24.CONVERSION_ENTRY_SCHEMA")
    entry, key = result["entry"], result["key"]
    rc = entry["resolutionCompleteness"]
    if key["resolution"] in NF.RESOLVED:
        if rc["state"] != "not-attempted" or rc["attempted"] or rc["unresolvedEdgeCount"] != 0:
            out.append(fault("native.coverage-bijection-mismatch", "RC-2-not-attempted"))
    elif rc["state"] != "not-applicable" or rc["attempted"] or rc["unresolvedEdgeCount"] != 0 or rc["unresolvedEdgeClasses"]:
        out.append(fault("native.coverage-bijection-mismatch", "RC-1-non-resolved"))
    if entry["coverage"] == "complete" and not rc["examinedExhaustive"]:
        out.append(fault("native.coverage-bijection-mismatch", "RC-6"))
    out += [fault(k) for k in NF.cause_registry_faults(entry, key["relation"])]
    cw = entry["closedWorld"]
    if cw["exportsClosed"] == "closed" and not (cw["entryPointsRecognized"] == "all" and cw["nonliteralLoading"] == "none" and
                                                cw["externalConsumers"] == "none-declared"):
        out.append(fault("cb24.CLOSED_WORLD_EXPORTS_CLOSED_INGREDIENTS", "native s4.5 lines 2213-2224: exportsClosed=closed requires every ingredient"))
    if cw["deadCodeRepairEligible"] and not (cw["exportsClosed"] == "closed" and cw["entryPointsRecognized"] == "all" and cw["nonliteralLoading"] == "none"):
        out.append(fault("cb24.CLOSED_WORLD_REPAIR_ELIGIBILITY", "native s4.5 lines 2237-2239 deadCodeRepairEligible ingredients"))
    if cw != HOST_CONVERSION_CLOSED_WORLD:
        out.append(fault("cb24.CONVERSION_CLOSED_WORLD_NOT_PUBLISHED",
                         "native s9.7 closedWorld bullet (lines 3241-3261); provider-startup #/x-opensip-startup-law/preAnalyzeUnavailable/hostConversionClosedWorld"))
    return out


def pre_analyze_conversion(requests):
    """Host conversion after a clean pre-Analyze Unavailable (native s9.7). Every member is fixed by the kit; the closedWorld is the published value."""
    entries, faults = [], []
    for r in requests:
        for k, n in zip(r["keys"], r["subjectCounts"]):
            e = mint_conversion_entry(k, n, json.loads(json.dumps(HOST_CONVERSION_CLOSED_WORLD)))
            faults += admit_minted_entry(e)
            entries.append(e)
    return {"entries": entries, "faults": faults, "stageAuthority": P.stage_authority("unavailable", False),
            "payloadDigests": [K.raw_digest(e) for e in entries]}
