"""Phase 3 (source44, HC-58): handshake, startup, coverage, terminal, cancellation and pre-Analyze host-conversion vectors.

Owners (source44 kit bytes only):
  native/provider-handshake.schemas.v1.json (whole document)
  native/provider-startup.schemas.v1.json (whole document)
  native-evidence.md s9.1, s9.3, s9.4, s9.7 (lines 3151-3294), s4.5 (lines 2208-2258), s0 rows 119-129
  native/native-evidence.schemas.v2.json CoverageResultV3, ViewEntryV3, ClosedWorldV2, StageAuthorityV1
  artifacts/delivery.v2.json typescriptSemanticSubstrate.providerProtocol.wireSchema (limits, canonicalCbor, commitments, CancelledV1)
  artifacts/rust-provider-protocol.v2.json (limits, canonicalCbor, CancelledV2 and the raw bytes)

Every expectation below is my own derivation from the cited selector, written before execution and asserted. Admission is executed by ref/provider_wire.py.
No author output is compared.

source45 (HC-60): the kit now publishes the conversion closedWorld. The conversion section therefore measures three things: that the two owners agree
and the published value admits; that conversion identities are stable; and that each of my source44 M-s44-1 candidates now refuses. The source44
determinacy measurement is preserved at preserved/s44-final/traces/startup-vectors.json#/conversion and preserved/s44-final/vectors/phase3_startup_vectors.py.
Writes traces/startup-vectors.json; exits 1 on any assertion failure.
"""
import copy
import hashlib
import inspect
import json
import sys

OUTP = '/private/tmp/opensip-design-corrections/consumer-b.v24-source45.v1/output/'
sys.path.insert(0, OUTP + 'ref')
sys.path.insert(0, OUTP + 'tools')
sys.path.insert(0, OUTP + 'vectors')
import canonical as K  # noqa: E402
import factbatch as FB  # noqa: E402
import native_facts as NF  # noqa: E402
import payload_fixtures as PF  # noqa: E402
import protocol3 as P  # noqa: E402
import provider_exchange as X  # noqa: E402
import provider_wire as W  # noqa: E402
import status as S  # noqa: E402
import wirecbor as WC  # noqa: E402

KIT = FB.K
failures = []
VECTORS = []


def check(cond, label):
    if not cond:
        failures.append(label)


def with_(value, *edits):
    v = copy.deepcopy(value)
    for path, new in edits:
        cur = v
        for k in path[:-1]:
            cur = cur[k]
        if new is DELETE:
            del cur[path[-1]]
        else:
            cur[path[-1]] = new
    return v


DELETE = object()


def vec(vid, group, cls, lang, law, faults, expected_keys, note="", subject=None, extra=()):
    keys = [f["key"] for f in faults]
    exp = list(expected_keys)
    observed = {"result": "REFUSE" if keys else "ADMIT", "firstRefusal": keys[0] if keys else None, "faultKeys": keys}
    expected = {"result": "REFUSE" if exp else "ADMIT", "firstRefusal": exp[0] if exp else None, "faultKeys": exp}
    ok = observed == expected
    check(ok, f"{vid}: expected {expected} observed {observed} {faults[:3]}")
    rec = {"id": vid, "group": group, "class": cls, "provider": lang, "law": law, "note": note, "expected": expected, "observed": observed,
           "faults": faults, "matches": ok, "subject": subject}
    for label, cond, value in extra:
        check(cond, f"{vid}: {label}")
        rec.setdefault("extraChecks", []).append({"label": label, "ok": bool(cond), "value": value})
    VECTORS.append(rec)


WL = "native/provider-handshake.schemas.v1.json#/x-opensip-wire-law"
SL = "native/provider-startup.schemas.v1.json#/x-opensip-startup-law"
L_HS = {"ts": f"native/provider-handshake.schemas.v1.json#/$defs/TypeScriptHelloV2,TypeScriptHelloAckV2,TypeScriptProtocolLimitsV1; {WL}/capabilityArrays,limits,typescriptDescriptorBinding; native-evidence.md s9.1, s9.4",
        "rust": f"native/provider-handshake.schemas.v1.json#/$defs/HelloV3,HelloAckV3,ProtocolLimitsV3; {WL}/capabilityArrays,limits,rustIdentityBinding,expectedProtocolContractSha256; native-evidence.md s9.1, s9.3"}
L_OU = {"ts": f"native/provider-startup.schemas.v1.json#/$defs/TypeScriptOpenUniverseV2; {SL}/identityMembers,universeIdentity,typescriptOpenUniverse; native-evidence.md s9.7",
        "rust": f"native/provider-startup.schemas.v1.json#/$defs/OpenUniverseV3; {SL}/identityMembers,rustOpenUniverse (handshakeJoin, repositoryResolution, derivedModes); protocol3-transitions.v1.json#/derivedObservations"}
L_UA = f"native/provider-startup.schemas.v1.json#/$defs/TypeScriptUniverseAcceptedV2,UniverseAcceptedV3; {SL}/typescriptOpenUniverse/accepted,rustOpenUniverse/accepted"
L_NCV = f"native/provider-startup.schemas.v1.json#/$defs/NativeContextVerifiedV1; {SL}/nativeContextVerified"
L_UN = f"native/provider-startup.schemas.v1.json#/$defs/PreAnalyzeUnavailableV1,TypeScriptUnavailableV2,UnavailableV3; {SL}/preAnalyzeUnavailable,postAnalyzeReasons,coverageFrames/terminals"
L_CV = f"native/provider-startup.schemas.v1.json#/$defs/TypeScriptCoverageV2,CoverageV3; {SL}/coverageFrames/entries; native-evidence.md s9.7 lines 3251-3263"
L_BE = f"native/provider-startup.schemas.v1.json#/$defs/TypeScriptBudgetExhaustedV2,BudgetExhaustedV3; {SL}/coverageFrames/terminals"
L_CA = f"{SL}/cancellation; native/typescript-protocol2-order.v1.json#/cancellationObservedPhase; delivery.v2.json CancelledV1; rust-provider-protocol.v2.json CancelledV2"
L_CONV = (f"{SL}/preAnalyzeUnavailable/hostConversion; native-evidence.md s9.7 lines 3227-3249; s4.5 lines 2208-2242; "
          "native/native-evidence.schemas.v2.json#/$defs/CoverageResultV3,ViewEntryV3,ClosedWorldV2,ResolutionCompletenessV2")
H, HA, OUK, UAK, NCVK, UNK, CVK, BEK, CAK = ("cb24.HELLO_", "cb24.HELLOACK_", "cb24.OPEN_UNIVERSE_", "cb24.UNIVERSE_ACCEPTED_", "cb24.NATIVE_CONTEXT_VERIFIED_",
                                            "cb24.UNAVAILABLE_", "cb24.COVERAGE_", "cb24.BUDGET_", "cb24.CANCELLED_")
TC = "cb24.TERMINAL_COVERAGE"

# ================================================================================================ handshake
for lang in ("ts", "rust"):
    tr, hp, ap = PF.trusted(lang), PF.hello_payload(lang), PF.ack_payload(lang)
    vec(f"HS-{lang}-hello-admit", "handshake", "valid", lang, L_HS[lang], W.admit_hello(lang, hp, tr), [], subject=hp)
    vec(f"HS-{lang}-helloack-admit", "handshake", "valid", lang, L_HS[lang], W.admit_hello_ack(lang, ap, hp, tr), [], subject=ap)
    rev = list(reversed(hp["expectedCapabilities"]))
    vec(f"HS-{lang}-hello-capabilities-descending", "handshake", "invalid", lang, L_HS[lang] + " (x-opensip-order utf8)",
        W.admit_hello(lang, with_(hp, (("expectedCapabilities",), rev)), tr), [H + "SCHEMA", H + "TOKENS_NOT_SIGNED_ROW"])
    vec(f"HS-{lang}-hello-lawful-tokens-not-signed-row", "handshake", "invalid", lang, L_HS[lang] + " ('Hello carries exactly the selected signed capability row's tokens')",
        W.admit_hello(lang, with_(hp, (("expectedCapabilities",), PF.caps(lang, False))), tr), [H + "TOKENS_NOT_SIGNED_ROW"])
    vec(f"HS-{lang}-hello-hostBuildId-other", "handshake", "invalid", lang, L_HS[lang], W.admit_hello(lang, with_(hp, (("hostBuildId",), "opensip-host:other")), tr),
        [H + "HOST_BUILD_ID"])
    vec(f"HS-{lang}-helloack-omits-optional-token", "handshake", "invalid", lang, L_HS[lang] + " ('HelloAck echoes the Hello array exactly')",
        W.admit_hello_ack(lang, with_(ap, (("capabilities",), PF.caps(lang, False))), hp, tr), [HA + "TOKEN_ECHO"],
        note="target-attribution-v2 is not an identity token, but the echo is exact")
    vec(f"HS-{lang}-helloack-capabilities-descending", "handshake", "invalid", lang, L_HS[lang],
        W.admit_hello_ack(lang, with_(ap, (("capabilities",), rev)), hp, tr), [HA + "SCHEMA", HA + "TOKEN_ECHO"])
    no_fact = [c for c in ap["capabilities"] if c != "fact-identity-fact2"]
    vec(f"HS-{lang}-helloack-identity-token-missing", "handshake", "invalid", lang, L_HS[lang] + " (allOf contains)",
        W.admit_hello_ack(lang, with_(ap, (("capabilities",), no_fact)), hp, tr), [HA + "SCHEMA", HA + "TOKEN_ECHO"])
    vec(f"HS-{lang}-helloack-identityVersions-coverage-2", "handshake", "invalid", lang, L_HS[lang] + " #/$defs/IdentityVersionsV1",
        W.admit_hello_ack(lang, with_(ap, (("identityVersions", "coverage"), 2)), hp, tr), [HA + "SCHEMA", HA + "IDENTITY_VERSIONS_ECHO"])
    vec(f"HS-{lang}-helloack-before-admitted-hello", "handshake", "invalid", lang, L_HS[lang], W.admit_hello_ack(lang, ap, None, tr), [H + "NOT_ADMITTED"])

tr, hp, ap = PF.trusted("ts"), PF.hello_payload("ts"), PF.ack_payload("ts")
first_limit = sorted(W.TS_LIMITS)[0]
vec("HS-ts-hello-limits-carry-limitRule", "handshake", "invalid", "ts", L_HS["ts"] + " ('limitRule is policy text, never a member')",
    W.admit_hello("ts", with_(hp, (("limits", "limitRule"), "policy")), tr), [H + "SCHEMA", H + "LIMITS"])
vec("HS-ts-hello-limit-value-changed", "handshake", "invalid", "ts", L_HS["ts"], W.admit_hello("ts", with_(hp, (("limits", first_limit), W.TS_LIMITS[first_limit] + 1)), tr),
    [H + "SCHEMA", H + "LIMITS"])
vec("HS-ts-hello-limits-are-ProtocolLimitsV3", "handshake", "invalid", "ts", L_HS["ts"] + " ('No ProtocolLimitsV3 member applies')",
    W.admit_hello("ts", with_(hp, (("limits",), dict(W.LIMITS_V3))), tr), [H + "SCHEMA", H + "LIMITS"])
with_rust_token = sorted(PF.caps("ts", False) + ["dependency-source-v1"], key=lambda t: t.encode())
vec("HS-ts-hello-rust-only-token", "handshake", "invalid", "ts", L_HS["ts"] + " #/$defs/TypeScriptCapabilityToken",
    W.admit_hello("ts", with_(hp, (("expectedCapabilities",), with_rust_token)), tr), [H + "SCHEMA", H + "TOKENS_NOT_SIGNED_ROW"])
pretty = hashlib.sha256(json.dumps(PF.TS_PROVIDER_DESCRIPTOR, indent=2, sort_keys=True).encode()).hexdigest()
vec("HS-ts-hello-provider-descriptor-digest-of-pretty-json", "handshake", "invalid", "ts", L_HS["ts"] + " typescriptDescriptorBinding.digests (RFC 8785 bytes)",
    W.admit_hello("ts", with_(hp, (("expectedProviderDescriptorSha256",), pretty)), tr), [H + "DESCRIPTOR_DIGEST"],
    extra=[("pretty-JSON digest differs from the RFC 8785 digest", pretty != hp["expectedProviderDescriptorSha256"], pretty)])
vec("HS-ts-hello-carries-payload-protocolMajor", "handshake", "invalid", "ts", L_HS["ts"] + " ('TypeScriptHelloV2 carries no payload protocolMajor')",
    W.admit_hello("ts", with_(hp, (("protocolMajor",), 2)), tr), [H + "SCHEMA"])
vec("HS-ts-helloack-nodeVersion-not-runtime-descriptor", "handshake", "invalid", "ts", L_HS["ts"] + " typescriptDescriptorBinding.rule",
    W.admit_hello_ack("ts", with_(ap, (("nodeVersion",), "18.20.0")), hp, tr), [HA + "DESCRIPTOR_FIELD"])
vec("HS-ts-helloack-provider-digest-not-echo", "handshake", "invalid", "ts", L_HS["ts"],
    W.admit_hello_ack("ts", with_(ap, (("providerDescriptorSha256",), PF.h("other-descriptor"))), hp, tr), [HA + "DESCRIPTOR_DIGEST_ECHO"])
vec("HS-ts-helloack-protocolMajor-1", "handshake", "invalid", "ts", L_HS["ts"] + " (protocolMajor const 2, equals the provider descriptor)",
    W.admit_hello_ack("ts", with_(ap, (("protocolMajor",), 1)), hp, tr), [HA + "SCHEMA", HA + "DESCRIPTOR_FIELD"])

tr, hp, ap = PF.trusted("rust"), PF.hello_payload("rust"), PF.ack_payload("rust")
vec("HS-rust-hello-limits-v2-only", "handshake", "invalid", "rust", L_HS["rust"] + " (32 members)", W.admit_hello("rust", with_(hp, (("limits",), dict(W.RUST_LIMITS_V2))), tr),
    [H + "SCHEMA", H + "LIMITS"])
parsed = hashlib.sha256(json.dumps(KIT.doc(W.RUST), sort_keys=True, separators=(",", ":")).encode()).hexdigest()
vec("HS-rust-hello-contract-digest-of-reserialized-json", "handshake", "invalid", "rust", L_HS["rust"] + " ('exact bytes')",
    W.admit_hello("rust", with_(hp, (("expectedProtocolContractSha256",), parsed)), tr), [H + "CONTRACT_DIGEST"],
    extra=[("reserialized digest differs from the raw-byte digest", parsed != W.CONTRACT_SHA256, parsed)])
vec("HS-rust-hello-expected-identity-protocolMajor-2", "handshake", "invalid", "rust", L_HS["rust"] + " #/$defs/ExpectedRustIdentityV3",
    W.admit_hello("rust", with_(hp, (("expectedIdentity", "protocolMajor"), 2)), tr), [H + "SCHEMA", H + "EXPECTED_IDENTITY"])
vec("HS-rust-hello-expected-identity-not-plan-row", "handshake", "invalid", "rust", L_HS["rust"] + " rustIdentityBinding.source",
    W.admit_hello("rust", with_(hp, (("expectedIdentity", "sysrootDigest"), PF.h("other-sysroot"))), tr), [H + "EXPECTED_IDENTITY"])
vec("HS-rust-helloack-sysroot-not-echo", "handshake", "invalid", "rust", L_HS["rust"] + " rustIdentityBinding.rule",
    W.admit_hello_ack("rust", with_(ap, (("sysrootDigest",), PF.h("other-sysroot"))), hp, tr), [HA + "IDENTITY_ECHO"])

# The first s44-p3 run asserted that native/source-pins.v2.json (cited by the wire law's expectedProtocolContractSha256.rule) is readable. It is not a
# member of the frozen subject (logs/s44-p3.1.phase3_startup_vectors.log). Its absence is recorded as a kit observation. The digest itself stays fully
# determined: the raw SHA-256 of the rust-provider-protocol.v2.json bytes equals the value the wire law pins.
pin_doc = [rel for rel in KIT.docs if rel.endswith("source-pins.v2.json")]
wire_controls = {"limitCrossCheck": W.LIMIT_CROSS_CHECK, "contractSha256": W.CONTRACT_SHA256, "pinnedInWireLaw": W.CONTRACT_PINNED,
                 "citedPinDocumentInSubject": pin_doc or "absent: native/source-pins.v2.json is not a subject member"}
check(all(W.LIMIT_CROSS_CHECK.values()), f"limit cross-check {W.LIMIT_CROSS_CHECK}")

# ================================================================================================ wire deterministic CBOR (provider-handshake candidateCborProjection)
cbor = {}
cbor["limitsInsertionOrderInvariant"] = WC.encode(W.LIMITS_V3) == WC.encode(dict(reversed(list(W.LIMITS_V3.items()))))
cbor["encodedKeyOrderShorterFirst"] = WC.encode({"aa": 0, "b": 1}).hex()
check(cbor["encodedKeyOrderShorterFirst"] == "a261620162616100", f"encoded-key order {cbor['encodedKeyOrderShorterFirst']}")
check(cbor["limitsInsertionOrderInvariant"], "limits CBOR bytes do not depend on insertion order")
for label, value, kw in (("negative-without-allowance", -1, {}), ("float", 1.5, {"allow_negative": True})):
    try:
        WC.encode(value, **kw)
        cbor[label] = "encoded"
    except WC.WireCborError as exc:
        cbor[label] = f"refused {exc.cls}"
    check(cbor[label].startswith("refused"), f"wire CBOR {label}: {cbor[label]}")
cbor["negativeAllowedDeliveryDataModel"] = WC.encode(-1, allow_negative=True).hex()
cbor["byteString"] = WC.encode(b"\x01\x02").hex()
check(cbor["negativeAllowedDeliveryDataModel"] == "20" and cbor["byteString"] == "420102", f"wire CBOR scalars {cbor}")
TSB = PF.v3("ts-calls", 0, PF.calls_b0())
wire_c = FB.ts_batch_commitment(TSB["candidates"])
json_vec_c = "sha256:" + hashlib.sha256(FB.FACT_BATCH_DOMAIN.encode() + b"\x00" + WC.encode(TSB["candidates"], allow_negative=True)).hexdigest()
undomained = "sha256:" + hashlib.sha256(WC.encode([FB.wire_candidate(c) for c in TSB["candidates"]], allow_negative=True)).hexdigest()
reordered = [dict(reversed(list(c.items()))) for c in TSB["candidates"]]
cbor["tsBatchCommitment"] = {"wireProjection": wire_c, "overJsonVectors": json_vec_c, "withoutDomain": undomained,
                             "jsonMemberOrderInvariant": FB.ts_batch_commitment(reordered) == wire_c}
check(len({wire_c, json_vec_c, undomained}) == 3 and cbor["tsBatchCommitment"]["jsonMemberOrderInvariant"], f"TS batch commitment controls {cbor['tsBatchCommitment']}")
cbor["mapOrderRules"] = WC.same_order_both_rules()
check(cbor["mapOrderRules"]["coincide"] and cbor["mapOrderRules"]["maps"] > 0, f"bytewise and length-first map orders coincide for text keys {cbor['mapOrderRules']}")
cbor["inheritedRules"] = {"delivery.v2": FB.TS_WIRE["canonicalCbor"], "rust-provider-protocol.v2": KIT.doc(W.RUST)["canonicalCbor"]}

# ================================================================================================ OpenUniverse
for lang in ("ts", "rust"):
    ou, evs = PF.startup_events(lang)
    ctx = dict(PF.exchange_ctx(lang)["startup"], hello=PF.hello_payload(lang), helloAck=PF.ack_payload(lang))
    f, obs = W.admit_open_universe(lang, ou, ctx)
    vec(f"OU-{lang}-admit", "open-universe", "valid", lang, L_OU[lang], f, [], subject=ou,
        extra=[("derived observations", obs == (None if lang == "ts" else {"dependencyMode": True, "preparedMode": False, "law": obs and obs["law"]}), obs),
               ("universe identity equals the retained Run's native universe frame key", W.universe_identity(lang, ou["universe"]["resolvedInputs"]) == PF.UNIV[lang],
                PF.RET[lang]["store"])])
    f = W.admit_open_universe(lang, with_(ou, (("executionId",), "exec-other")), ctx)[0]
    vec(f"OU-{lang}-executionId-not-attempt", "open-universe", "invalid", lang, L_OU[lang] + " identityMembers", f, [OUK + "EXECUTION_ID"])
    f = W.admit_open_universe(lang, with_(ou, (("snapshotId",), "snap1:sha256:" + PF.RET[lang]["plan"]["snapshotId"][10:])), ctx)[0]
    vec(f"OU-{lang}-snapshotId-v1-text", "open-universe", "invalid", lang, L_OU[lang] + " (^snapshot2:)", f, [OUK + "SCHEMA", OUK + "SNAPSHOT_ID"])
    f = W.admit_open_universe(lang, with_(ou, (("planId",), PF.RET[lang]["plan"]["planId"])), ctx)[0]
    vec(f"OU-{lang}-planId-other-plan2", "open-universe", "invalid", lang, L_OU[lang], f, [OUK + "PLAN_ID"])

ou, _ = PF.startup_events("ts")
ctx = dict(PF.exchange_ctx("ts")["startup"], hello=PF.hello_payload("ts"), helloAck=PF.ack_payload("ts"))
ri = ou["universe"]["resolvedInputs"]
vec("OU-ts-universeKey-raw-sha256-of-resolvedInputs", "open-universe", "invalid", "ts", L_OU["ts"] + " universeIdentity",
    W.admit_open_universe("ts", with_(ou, (("universeKey",), "sha256:" + K.raw_digest(ri))), ctx)[0], [OUK + "UNIVERSE_KEY"])
vec("OU-ts-universeKey-bare-hex", "open-universe", "invalid", "ts", L_OU["ts"] + " (Sha256Text)",
    W.admit_open_universe("ts", with_(ou, (("universeKey",), PF.RET["ts"]["universeHex"])), ctx)[0], [OUK + "SCHEMA", OUK + "UNIVERSE_KEY"])
vec("OU-ts-carries-repositoryResolution", "open-universe", "invalid", "ts", L_OU["ts"] + " typescriptOpenUniverse.absent",
    W.admit_open_universe("ts", with_(ou, (("repositoryResolution",), None)), ctx)[0], [OUK + "SCHEMA"])
vec("OU-ts-handshake-join-nodeVersion", "open-universe", "invalid", "ts", L_OU["ts"] + " typescriptOpenUniverse.handshakeJoin",
    W.admit_open_universe("ts", with_(ou, (("universe", "nodeVersion"), "18.20.0")), ctx)[0], [OUK + "HANDSHAKE_JOIN"])
vec("OU-ts-native-context-not-in-plan", "open-universe", "invalid", "ts", L_OU["ts"] + " typescriptOpenUniverse.nativeContext",
    W.admit_open_universe("ts", with_(ou, (("universe", "resolvedInputs", "nativeContextId"), "sha256:" + PF.h("other-context"))), ctx)[0],
    [OUK + "NATIVE_CONTEXT_NOT_PLAN", OUK + "UNIVERSE_KEY"], note="the universe identity covers resolvedInputs, so the unchanged universeKey also fails")

ou, _ = PF.startup_events("rust")
ctx = dict(PF.exchange_ctx("rust")["startup"], hello=PF.hello_payload("rust"), helloAck=PF.ack_payload("rust"))
vec("OU-rust-carries-mode-boolean", "open-universe", "invalid", "rust", L_OU["rust"] + " ('no mode booleans')",
    W.admit_open_universe("rust", with_(ou, (("dependencyMode",), False)), ctx)[0], [OUK + "SCHEMA"])
f, obs = W.admit_open_universe("rust", with_(ou, (("repositoryResolution", "dependencySourceSetId"), None)), ctx)
vec("OU-rust-dependency-set-null", "open-universe", "invalid", "rust", L_OU["rust"] + " derivedModes ('dependencySourceSetId is required and non-null')", f,
    [OUK + "SCHEMA", OUK + "REPOSITORY_RESOLUTION"], extra=[("the would-be dependencyMode=false observation never reaches the table", obs["dependencyMode"] is False, obs)])
vec("OU-rust-prepared-id-without-universe-prepared", "open-universe", "invalid", "rust", L_OU["rust"] + " rustOpenUniverse.repositoryResolution",
    W.admit_open_universe("rust", with_(ou, (("repositoryResolution", "preparedOutputSetId"), PF.PREPARED_OUTPUT_SET_ID)), ctx)[0],
    [OUK + "REPOSITORY_RESOLUTION", OUK + "REPOSITORY_RESOLUTION"])
vec("OU-rust-authorization-without-prepared", "open-universe", "invalid", "rust", L_OU["rust"] + " ('authorizationId and effects are both null when preparedOutputSetId is null')",
    W.admit_open_universe("rust", with_(ou, (("repositoryResolution", "authorizationId"), "sha256:" + PF.h("authorization"))), ctx)[0], [OUK + "REPOSITORY_RESOLUTION"])
vec("OU-rust-handshake-join-sysroot", "open-universe", "invalid", "rust", L_OU["rust"] + " rustOpenUniverse.handshakeJoin",
    W.admit_open_universe("rust", with_(ou, (("universe", "sysrootDigest"), PF.h("other-sysroot"))), ctx)[0], [OUK + "HANDSHAKE_JOIN"])
vec("OU-rust-universe-protocolMajor-2", "open-universe", "invalid", "rust", L_OU["rust"],
    W.admit_open_universe("rust", with_(ou, (("universe", "protocolMajor"), 2)), ctx)[0], [OUK + "SCHEMA", OUK + "HANDSHAKE_JOIN"])
oup, _ = PF.startup_events("rust", prepared=True)
ctxp = dict(PF.exchange_ctx("rust", prepared=True)["startup"], hello=PF.hello_payload("rust"), helloAck=PF.ack_payload("rust"))
f, obs = W.admit_open_universe("rust", oup, ctxp)
vec("OU-rust-prepared-imported-descriptor-admit", "open-universe", "valid", "rust", L_OU["rust"] + " ('null for an imported-descriptor preparation')", f, [], subject=oup,
    note="fixture: retained rust-mixed resolvedInputs with a synthetic preparedOutputSetId, preparedResolution imported-inert and the recomputed native context id",
    extra=[("derived observations dependencyMode and preparedMode true", obs["dependencyMode"] is True and obs["preparedMode"] is True, obs)])

# ================================================================================================ UniverseAccepted, NativeContextVerified
for lang in ("ts", "rust"):
    ou, evs = PF.startup_events(lang)
    ua = evs["UniverseAccepted"]["payload"]
    vec(f"UA-{lang}-admit", "universe-accepted", "valid", lang, L_UA, W.admit_universe_accepted(lang, ua, ou), [], subject=ua)
    vec(f"UA-{lang}-before-open-universe", "universe-accepted", "invalid", lang, L_UA, W.admit_universe_accepted(lang, ua, None), [UAK + "BEFORE_OPEN"])
    ncv = evs["NativeContextVerified"]["payload"]
    vec(f"NCV-{lang}-admit", "native-context-verified", "valid", lang, L_NCV, W.admit_native_context_verified(ncv, ou), [], subject=ncv)
    vec(f"NCV-{lang}-recomputed-differs-equal-true", "native-context-verified", "invalid", lang, L_NCV,
        W.admit_native_context_verified(with_(ncv, (("recomputedNativeContextId",), "sha256:" + PF.h("worker-context"))), ou), [NCVK + "JOIN"])
    vec(f"NCV-{lang}-equal-false", "native-context-verified", "invalid", lang, L_NCV + " (equal const true)",
        W.admit_native_context_verified(with_(ncv, (("equal",), False)), ou), [NCVK + "SCHEMA"])
ou, evs = PF.startup_events("ts")
vec("UA-ts-universeKey-not-echo", "universe-accepted", "invalid", "ts", L_UA,
    W.admit_universe_accepted("ts", with_(evs["UniverseAccepted"]["payload"], (("universeKey",), "sha256:" + PF.h("worker-key"))), ou), [UAK + "ECHO"])
ou, evs = PF.startup_events("rust")
vec("UA-rust-carries-planIntentCommitment", "universe-accepted", "invalid", "rust", L_UA,
    W.admit_universe_accepted("rust", with_(evs["UniverseAccepted"]["payload"], (("planIntentCommitment",), ou["planIntentCommitment"])), ou), [UAK + "SCHEMA"])
vec("UA-rust-universe-not-recursive-echo", "universe-accepted", "invalid", "rust", L_UA,
    W.admit_universe_accepted("rust", with_(evs["UniverseAccepted"]["payload"], (("universe", "rustcVersion"), "1.80.0")), ou), [UAK + "ECHO"])

# ================================================================================================ Unavailable
for lang in ("ts", "rust"):
    ou, evs = PF.startup_events(lang)
    reqs = X.requests_of(PF.analyze_event(lang), lang)
    pre = evs["PreAnalyzeUnavailable"]["payload"]
    post = PF.post_unavailable(lang)["payload"]
    f, kind = W.admit_unavailable(lang, pre, "WAIT_NATIVE_CONTEXT_VERIFIED", ou, None)
    vec(f"UN-{lang}-pre-analyze-admit", "unavailable", "valid", lang, L_UN, f, [], subject=pre, extra=[("classified pre-analyze", kind == "pre-analyze", kind)])
    f, kind = W.admit_unavailable(lang, post, "ANALYZING", ou, reqs)
    vec(f"UN-{lang}-post-analyze-admit", "unavailable", "valid", lang, L_UN, f, [], extra=[("classified post-analyze", kind == "post-analyze", kind)])
    vec(f"UN-{lang}-pre-analyze-in-ANALYZING", "unavailable", "invalid", lang, L_UN + " preAnalyzeUnavailable.phase",
        W.admit_unavailable(lang, pre, "ANALYZING", ou, reqs)[0], [UNK + "PHASE"])
    f, kind = W.admit_unavailable(lang, post, "WAIT_NATIVE_CONTEXT_VERIFIED", ou, None)
    vec(f"UN-{lang}-post-analyze-in-native-context-interval", "unavailable", "invalid", lang, L_UN + " ('inside it the post-Analyze payloads ... are PROVIDER.PROTOCOL_VIOLATION')",
        f, [UNK + "PHASE"])
    vec(f"UN-{lang}-post-analyze-reason-native-context-mismatch", "unavailable", "invalid", lang, L_UN + " postAnalyzeReasons",
        W.admit_unavailable(lang, with_(post, (("reason",), "native-context-mismatch")), "ANALYZING", ou, reqs)[0], [UNK + "SCHEMA", UNK + "SCHEMA"])
    vec(f"UN-{lang}-pre-analyze-reason-capability-missing", "unavailable", "invalid", lang, L_UN + " preAnalyzeUnavailable.reason",
        W.admit_unavailable(lang, with_(pre, (("reason",), "capability-missing")), "WAIT_NATIVE_CONTEXT_VERIFIED", ou, None)[0], [UNK + "SCHEMA", UNK + "SCHEMA"])
    vec(f"UN-{lang}-pre-analyze-equal-contexts", "unavailable", "invalid", lang, L_UN + " preAnalyzeUnavailable.correlation",
        W.admit_unavailable(lang, with_(pre, (("recomputedNativeContextId",), pre["nativeContextId"])), "WAIT_NATIVE_CONTEXT_VERIFIED", ou, None)[0],
        [UNK + "CONTEXTS_EQUAL"])
ou, evs = PF.startup_events("ts")
pre, post = evs["PreAnalyzeUnavailable"]["payload"], PF.post_unavailable("ts")["payload"]
reqs = X.requests_of(PF.analyze_event("ts"), "ts")
vec("UN-ts-pre-analyze-in-READY_ANALYZE", "unavailable", "invalid", "ts", L_UN + " preAnalyzeUnavailable.phase",
    W.admit_unavailable("ts", pre, "READY_ANALYZE", ou, None)[0], [UNK + "PHASE"], note="after NativeContextVerified the interval is over")
vec("UN-ts-pre-analyze-snapshot-not-open-universe", "unavailable", "invalid", "ts", L_UN + " correlation",
    W.admit_unavailable("ts", with_(pre, (("snapshotId",), PF.RET["rust"]["plan"]["snapshotId"])), "WAIT_NATIVE_CONTEXT_VERIFIED", ou, None)[0], [UNK + "CORRELATION"])
vec("UN-ts-pre-analyze-carries-analysisOrdinal", "unavailable", "invalid", "ts", L_UN + " ('No analysisOrdinal, affectedStageIds, coverage or coverageCommitment')",
    W.admit_unavailable("ts", with_(pre, (("analysisOrdinal",), 0)), "WAIT_NATIVE_CONTEXT_VERIFIED", ou, None)[0], [UNK + "SCHEMA", UNK + "SCHEMA"])
vec("UN-ts-post-analyze-affected-stage-subset", "unavailable", "invalid", "ts", L_UN + " ('all requested stageIds in request order')",
    W.admit_unavailable("ts", with_(post, (("affectedStageIds",), ["ts-imports"])), "ANALYZING", ou, reqs)[0], [UNK + "AFFECTED_STAGES"])
n_ts = len(post["coverage"])
bad_def = with_(post, (("coverage",), [with_(e, (("entry", "deficiency"), "budget-exhausted")) for e in post["coverage"]]))
vec("UN-ts-post-analyze-entries-budget-exhausted", "unavailable", "invalid", "ts", L_UN + " coverageFrames.terminals",
    W.admit_unavailable("ts", bad_def, "ANALYZING", ou, reqs)[0], [TC] * n_ts)
swapped = with_(post, (("coverage", 0), post["coverage"][1]), (("coverage", 1), post["coverage"][0]))
vec("UN-ts-post-analyze-entries-swapped", "unavailable", "invalid", "ts", L_UN + " ('stage-major/key order')",
    W.admit_unavailable("ts", swapped, "ANALYZING", ou, reqs)[0], [TC] * 4, note="each swapped entry fails its key and its relation/resolution")

# ================================================================================================ Coverage wrappers
for lang in ("ts", "rust"):
    reqs = X.requests_of(PF.analyze_event(lang), lang)
    for i, r in enumerate(reqs):
        p = PF.coverage_payload(lang, i)
        vec(f"CV-{lang}-stage{i}-admit", "coverage", "valid", lang, L_CV, W.admit_coverage(lang, p, r, 0), [], subject=p,
            note="entries are my retained CoverageResultV3 for the retained rung; the coverageCommitment is a placeholder (s9.7 reference scope: not recomputed)")
reqs = X.requests_of(PF.analyze_event("ts"), "ts")
p0 = PF.coverage_payload("ts", 0)
vec("CV-ts-entries-reversed", "coverage", "invalid", "ts", L_CV, W.admit_coverage("ts", with_(p0, (("entries",), list(reversed(p0["entries"])))), reqs[0], 0),
    [CVK + "KEY_CORRESPONDENCE"] * 4)
vec("CV-ts-entry-missing", "coverage", "invalid", "ts", L_CV + " ('The entry count equals the requested key count')",
    W.admit_coverage("ts", with_(p0, (("entries",), p0["entries"][:-1])), reqs[0], 0), [CVK + "KEY_CORRESPONDENCE"])
vec("CV-ts-entry-key-carries-full-universe-text", "coverage", "invalid", "ts", L_CV + " ('64-hex suffixes')",
    W.admit_coverage("ts", with_(p0, (("entries", 0, "key", "sourceUniverse"), "sha256:" + p0["entries"][0]["key"]["sourceUniverse"])), reqs[0], 0),
    [CVK + "SCHEMA", CVK + "KEY_CORRESPONDENCE"])
vec("CV-ts-analysisOrdinal-1", "coverage", "invalid", "ts", L_CV + " (analysisOrdinal exactly 0)", W.admit_coverage("ts", with_(p0, (("analysisOrdinal",), 1)), reqs[0], 0),
    [CVK + "SCHEMA", CVK + "ANALYSIS_ORDINAL"])
vec("CV-ts-stageId-other-requested-stage", "coverage", "invalid", "ts", L_CV + " ('the wrapper stageId attributes every entry')",
    W.admit_coverage("ts", with_(p0, (("stageId",), "ts-calls")), reqs[0], 0), [CVK + "STAGE_ID"])
vec("CV-ts-frame-payload-is-CoverageResultV3", "coverage", "invalid", "ts", L_CV + " ('the ENTRY type, never a frame')",
    W.admit_coverage("ts", p0["entries"][0], reqs[0], 0), [CVK + "SCHEMA", CVK + "STAGE_ID", CVK + "ANALYSIS_ORDINAL", CVK + "KEY_CORRESPONDENCE"])
vec("CV-ts-entry-carries-stageId", "coverage", "invalid", "ts", L_CV + " ('carries no stageId and no entryOrdinal')",
    W.admit_coverage("ts", with_(p0, (("entries", 0, "stageId"), "ts-imports")), reqs[0], 0), [CVK + "SCHEMA"])
rreqs = X.requests_of(PF.analyze_event("rust"), "rust")
vec("CV-rust-analysisOrdinal-other", "coverage", "invalid", "rust", L_CV, W.admit_coverage("rust", with_(PF.coverage_payload("rust", 0), (("analysisOrdinal",), 1)), rreqs[0], 0),
    [CVK + "ANALYSIS_ORDINAL"])

# ================================================================================================ BudgetExhausted
for lang, trig in (("ts", "ts-imports"), ("rust", "rust-calls")):
    reqs = X.requests_of(PF.analyze_event(lang), lang)
    p = PF.budget_exhausted(lang, trig)["payload"]
    vec(f"BE-{lang}-admit", "budget-exhausted", "valid", lang, L_BE, W.admit_budget_exhausted(lang, p, reqs, 0), [], subject=p)
    vec(f"BE-{lang}-trigger-not-requested", "budget-exhausted", "invalid", lang, L_BE, W.admit_budget_exhausted(lang, with_(p, (("triggerStageId",), "syntax-declares")), reqs, 0),
        [BEK + "TRIGGER_STAGE"])
    vec(f"BE-{lang}-before-analyze", "budget-exhausted", "invalid", lang, L_BE, W.admit_budget_exhausted(lang, p, None, 0), [BEK + "PHASE"])
p = PF.budget_exhausted("ts", "ts-imports")["payload"]
vec("BE-ts-unit-instead-of-dimension", "budget-exhausted", "invalid", "ts", L_BE + " (BudgetExhaustedV1 members kept)",
    W.admit_budget_exhausted("ts", with_(p, (("dimension",), DELETE), (("unit",), "items")), X.requests_of(PF.analyze_event("ts"), "ts"), 0), [BEK + "SCHEMA"])
pr = PF.budget_exhausted("rust", "rust-calls")["payload"]
vec("BE-rust-entries-provider-unavailable", "budget-exhausted", "invalid", "rust", L_BE + " coverageFrames.terminals",
    W.admit_budget_exhausted("rust", with_(pr, (("coverage",), [with_(e, (("entry", "deficiency"), "provider-unavailable")) for e in pr["coverage"]])),
                             X.requests_of(PF.analyze_event("rust"), "rust"), 0), [TC] * len(pr["coverage"]))

# ================================================================================================ Cancelled
cp = PF.cancel("ts")["payload"]
for vid, phase, word, keys, cls, note in (
        ("CA-ts-native-context-interval-snapshot", "WAIT_NATIVE_CONTEXT_VERIFIED", "snapshot", [], "valid", ""),
        ("CA-ts-ready-analyze-snapshot", "READY_ANALYZE", "snapshot", [], "valid", "including after NativeContextVerified emission"),
        ("CA-ts-native-context-interval-universe", "WAIT_NATIVE_CONTEXT_VERIFIED", "universe", [CAK + "OBSERVED_PHASE"], "invalid", ""),
        ("CA-ts-ready-analyze-analysis", "READY_ANALYZE", "analysis", [CAK + "OBSERVED_PHASE"], "invalid", "no Analyze was received"),
        ("CA-ts-analyzing-analysis", "ANALYZING", "analysis", [], "explanatory", "inherited interval; s9.7 does not restate it and it is not validated here"),
        ("CA-ts-native-context-phase-word", "WAIT_NATIVE_CONTEXT_VERIFIED", "native-context", [CAK + "SCHEMA"], "invalid", "'No enum member ... is added'")):
    vec(vid, "cancelled", cls, "ts", L_CA, W.admit_cancelled("ts", PF.cancelled("ts", word)["payload"], phase, cp), keys, note=note)
vec("CA-ts-executionId-not-cancel", "cancelled", "invalid", "ts", L_CA + " ('exact Cancel value')",
    W.admit_cancelled("ts", with_(PF.cancelled("ts", "snapshot")["payload"], (("executionId",), "exec-other")), "WAIT_NATIVE_CONTEXT_VERIFIED", cp), [CAK + "CORRELATION"])
vec("CA-ts-extra-member", "cancelled", "invalid", "ts", L_CA + " (closed)",
    W.admit_cancelled("ts", with_(PF.cancelled("ts", "snapshot")["payload"], (("reason",), "user-interrupt")), "WAIT_NATIVE_CONTEXT_VERIFIED", cp), [CAK + "SCHEMA"])
vec("CA-rust-observedPhase-not-validated", "cancelled", "explanatory", "rust", L_CA + " ('CancelledV2.observedPhase remains the exact concrete phase ... unchanged')",
    W.admit_cancelled("rust", PF.cancelled("rust", "any-worker-phase")["payload"], "ANALYZING", PF.cancel("rust")["payload"]), [],
    note="no owner I can read publishes the worker phase vocabulary; unchanged by source44 and outside the s9.7 reference scope")
vec("CA-rust-analysisOrdinal-not-cancel", "cancelled", "invalid", "rust", L_CA,
    W.admit_cancelled("rust", PF.cancelled("rust", "analysis", 1)["payload"], "ANALYZING", PF.cancel("rust")["payload"]), [CAK + "CORRELATION"])

# ================================================================================================ pre-Analyze host conversion (source45: published closedWorld)
PUBLISHED = W.HOST_CONVERSION_CLOSED_WORLD
DETERMINED = {"entryPointsRecognized": "none", "nonliteralLoading": "none", "externalConsumers": "unknown", "deadCodeRepairEligible": False}
# my source44 M-s44-1 candidates, unchanged (preserved/s44-final/traces/startup-vectors.json#/conversion/candidates)
S44_CANDIDATES = {
    "A-exports-unknown-dispatch-not-applicable-no-reasons": dict(DETERMINED, exportsClosed="unknown", dynamicDispatch="not-applicable", reasons=[]),
    "B-exports-unknown-dispatch-resolved-no-reasons": dict(DETERMINED, exportsClosed="unknown", dynamicDispatch="resolved", reasons=[]),
    "C-exports-open-dispatch-not-applicable-no-reasons": dict(DETERMINED, exportsClosed="open", dynamicDispatch="not-applicable", reasons=[]),
    "D-exports-unknown-dispatch-not-applicable-with-reason": dict(DETERMINED, exportsClosed="unknown", dynamicDispatch="not-applicable", reasons=["provider-unavailable"])}
L_CW = ("native-evidence.md s9.7 closedWorld bullet (lines 3241-3261); "
        "native/provider-startup.schemas.v1.json#/x-opensip-startup-law/preAnalyzeUnavailable/hostConversion,hostConversionClosedWorld")
cw_schema = KIT.admit(PUBLISHED, W.NE, "#/$defs/ClosedWorldV2")
conversion = {"law": L_CONV + "; " + L_CW, "publishedClosedWorld": PUBLISHED, "markdownBlockClosedWorld": W.MD_HOST_CONVERSION_CLOSED_WORLD,
              "ownersAgree": W.HOST_CONVERSION_CLOSED_WORLD_OWNERS_AGREE, "publishedAdmitsClosedWorldV2": cw_schema["ok"], "languages": {}}
check(W.HOST_CONVERSION_CLOSED_WORLD_OWNERS_AGREE, "the s9.7 JSON block equals provider-startup hostConversionClosedWorld")
check(cw_schema["ok"], f"published closedWorld admits ClosedWorldV2 {cw_schema['stock'][:2]} {cw_schema['order']}")
check(all(PUBLISHED[k] == v for k, v in DETERMINED.items()), "the published value keeps every member my source44 reading found determined")
check(list(inspect.signature(W.pre_analyze_conversion).parameters) == ["requests"], "conversion takes no worker input and no closedWorld choice")
check(all(cw != PUBLISHED for cw in S44_CANDIDATES.values()), "none of my source44 candidates equals the published value")


def coverage2_ids(conv, scope_of):
    return [K.identifier("coverage", {"schemaVersion": 2, "scopeId": scope_of[e["key"]["resolution"] + "|" + e["key"]["relation"]],
                                      "payloadSchemaDigest": KIT.digest(W.NE), "payloadDigest": K.sha256_hex(K.C(e))}) for e in conv["entries"]]


for lang in ("ts", "rust"):
    aev = PF.analyze_event(lang)
    reqs = X.requests_of(aev, lang)
    scope_of = {k["resolution"] + "|" + d["relation"]: d["scopeId"] for d in aev["hostDomains"] for k in d["keys"]}
    conv, again = W.pre_analyze_conversion(reqs), W.pre_analyze_conversion(reqs)
    sa = KIT.admit(conv["stageAuthority"], W.NE, "#/$defs/StageAuthorityV1")
    ids, ids_again = coverage2_ids(conv, scope_of), coverage2_ids(again, scope_of)
    rc = [(e["key"]["resolution"], e["entry"]["resolutionCompleteness"]["state"]) for e in conv["entries"]]
    check(conv["faults"] == [] and sa["ok"], f"conversion {lang}: {conv['faults'][:3]} {sa['stock'][:2]}")
    check(len(conv["entries"]) == sum(len(r["keys"]) for r in reqs), f"conversion {lang}: one entry per requested key")
    check(all(state == ("not-attempted" if res in NF.RESOLVED else "not-applicable") for res, state in rc), f"conversion {lang}: rc states {rc}")
    check(conv["stageAuthority"]["d9"] == {"class": "indeterminate", "exitCode": 3, "code": "COVERAGE.PROVIDER_UNAVAILABLE"}, f"conversion {lang} authority")
    check(all(e["entry"]["closedWorld"] == PUBLISHED for e in conv["entries"]), f"conversion {lang}: every entry carries the published closedWorld")
    check(ids == ids_again, f"conversion {lang}: two mintings give the same coverage2 identities")
    candidates = {}
    for name, cw in S44_CANDIDATES.items():
        faults = [f for r in reqs for k, n in zip(r["keys"], r["subjectCounts"]) for f in W.admit_minted_entry(W.mint_conversion_entry(k, n, cw))]
        got = sorted({f["key"] for f in faults})
        candidates[name] = {"closedWorld": cw, "faultKeys": got, "faultCount": len(faults)}
        check(got == ["cb24.CONVERSION_CLOSED_WORLD_NOT_PUBLISHED"] and len(faults) == len(conv["entries"]),
              f"conversion {lang}: source44 candidate {name} refuses only as not the published value {got}")
    controls = {}
    for name, cw, key in (("exports-closed", dict(PUBLISHED, exportsClosed="closed"), "cb24.CLOSED_WORLD_EXPORTS_CLOSED_INGREDIENTS"),
                          ("repair-eligible", dict(PUBLISHED, deadCodeRepairEligible=True), "cb24.CLOSED_WORLD_REPAIR_ELIGIBILITY")):
        got = sorted({f["key"] for r in reqs for k, n in zip(r["keys"], r["subjectCounts"]) for f in W.admit_minted_entry(W.mint_conversion_entry(k, n, cw))})
        controls[name] = {"closedWorld": cw, "faultKeys": got}
        check(key in got and "cb24.CONVERSION_CLOSED_WORLD_NOT_PUBLISHED" in got, f"conversion control {lang} {name}: {got}")
    minted = W.mint_conversion_entry(reqs[0]["keys"][-1], reqs[0]["subjectCounts"][-1], PUBLISHED)
    rc6 = W.admit_minted_entry(with_(minted, (("entry", "coverage"), "complete")))
    rc2 = W.admit_minted_entry(with_(minted, (("entry", "resolutionCompleteness", "state"), "complete" if minted["key"]["resolution"] in NF.RESOLVED else "not-attempted")))
    controls["coverage-complete-over-unexamined"] = [f["detail"] for f in rc6]
    controls["resolution-state-wrong"] = [f["detail"] for f in rc2]
    check("RC-6" in controls["coverage-complete-over-unexamined"], f"RC-6 control {lang} {rc6}")
    check(any(d.startswith("RC-") for d in controls["resolution-state-wrong"]), f"RC-1/RC-2 control {lang} {rc2}")
    conversion["languages"][lang] = {"requests": reqs,
                                     "published": {"faults": conv["faults"], "entries": len(conv["entries"]), "coverage2": ids, "resolutionCompleteness": rc,
                                                   "stageAuthority": conv["stageAuthority"], "stageAuthoritySchemaOk": sa["ok"],
                                                   "identitiesStableAcrossTwoMintings": ids == ids_again},
                                     "source44Candidates": candidates, "controls": controls}
conversion["determinacyResolution"] = {
    "issue": "M-s44-1 (source44)",
    "status": "resolved by the source45 bytes",
    "finding": ("native-evidence s9.7 now gives the conversion closedWorld as one complete value for both languages, and "
                "provider-startup#/x-opensip-startup-law/preAnalyzeUnavailable/hostConversionClosedWorld publishes the same value machine-readably; hostConversion "
                "references it. The value keeps every member my source44 reading found determined, fixes dynamicDispatch not-applicable and reasons "
                "['no-manifest'], and admits as ClosedWorldV2. None of my four source44 candidates equals it: A differs only in reasons ([] versus ['no-manifest']). "
                "Every candidate now refuses as not the published value, and the published conversion mints stable coverage2 identities."),
    "selectors": ["docs/v2/contracts/product-v1/native-evidence.md s9.7 lines 3241-3261",
                  "docs/coop/design-corrections/native/provider-startup.schemas.v1.json#/x-opensip-startup-law/preAnalyzeUnavailable/hostConversion (line 58)",
                  "docs/coop/design-corrections/native/provider-startup.schemas.v1.json#/x-opensip-startup-law/preAnalyzeUnavailable/hostConversionClosedWorld (lines 59-69)"],
    "measured": {lang: (conversion["ownersAgree"] and conversion["publishedAdmitsClosedWorldV2"] and conversion["languages"][lang]["published"]["faults"] == []
                        and conversion["languages"][lang]["published"]["identitiesStableAcrossTwoMintings"]
                        and all(c["faultKeys"] == ["cb24.CONVERSION_CLOSED_WORLD_NOT_PUBLISHED"] for c in conversion["languages"][lang]["source44Candidates"].values()))
                 for lang in ("ts", "rust")}}

# ================================================================================================ summary
groups = {}
for v in VECTORS:
    g = groups.setdefault(v["group"], {"valid": 0, "invalid": 0, "explanatory": 0, "matched": 0})
    g[v["class"]] += 1
    g["matched"] += v["matches"]
keys = sorted({k for v in VECTORS for k in v["observed"]["faultKeys"]})
out = {"standing": ("source44 executed reference reconstruction of the handshake and startup payload law (provider-handshake.schemas.v1.json, provider-startup.schemas.v1.json, "
                    "native-evidence s9.1/9.3/9.4/9.7) on constructed payloads joined to my retained Run values. These are schema, join, phase and host-conversion checks; "
                    "they are not OS/provider/compiler qualification."),
       "vectors": VECTORS, "groups": groups, "faultKeysExercised": keys, "wireControls": wire_controls, "wireCbor": cbor, "conversion": conversion,
       "fixtureSources": {lang: {"store": PF.RET[lang]["store"], "runId": PF.RET[lang]["runId"], "plan": PF.RET[lang]["plan"], "universeHex": PF.RET[lang]["universeHex"],
                                 "contextHex": PF.RET[lang]["contextHex"]} for lang in ("ts", "rust")},
       "executedVsHost": {"executed": ["TypeScriptHelloV2/HelloAckV2 and HelloV3/HelloAckV3 schemas; delivery.v2 and ProtocolLimitsV3 limit equality with deterministic-CBOR bytes; "
                                       "RFC 8785 descriptor digests and descriptor-field joins; contract raw-byte digest; rust-v1 identity row; exact token and identityVersions echoes",
                                       "OpenUniverse/UniverseAccepted/NativeContextVerified schemas, identity members, native semantic-universe identity recomputation, handshake joins, "
                                       "plan native context membership, RepositoryResolutionV3 joins and derived modes",
                                       "pre-Analyze and post-Analyze Unavailable classification, phase law, correlation and reason partition",
                                       "Coverage wrapper shape and requested-key correspondence; terminal coverage deficiency and order",
                                       "TypeScript CancelledV1 inserted observedPhase interval and Cancel echo",
                                       "pre-Analyze host conversion minted through CoverageResultV3 schema, RC-1/RC-2/RC-6, cause registry and s4.5 ingredient rules; coverage2 identities"],
                          "notExecuted": ["commitment recomputation of coverageCommitment and stream commitments (s9.7 reference scope)", "framing bytes, processes, compilers",
                                          "snapshot, dependency-source and prepared custody payloads", "Rust CancelledV2 observedPhase vocabulary",
                                          "signature verification of the descriptors (synthetic trusted host inputs)"]},
       "assertionFailures": failures}
S.dump("traces/startup-vectors.json", out)
print(json.dumps({"vectors": len(VECTORS), "groups": groups, "faultKeysExercised": keys, "conversionResolutionMeasured": conversion["determinacyResolution"]["measured"],
                  "failures": failures}, indent=1))
sys.exit(1 if failures else 0)
