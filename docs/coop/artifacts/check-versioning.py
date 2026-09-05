#!/usr/bin/env python3
"""Retained executable checker for the contract-evolution policy (v4).

The finding that shaped this file is B-CSG-04 / CS-04: a baseline comparison had
no policy for a CHANGED DETECTOR. Exact artifact identity detects that something
moved; it cannot say whether the difference is new code, a detector that changed
its mind, or the user adopting a new level. A two-way diff compares
(code0,detector0) against (code1,detector1) — two variables moved and one
difference was measured — and attributes the whole thing to the user's code.

That is a false net-new finding presented as a regression, which is precisely the
failure the USER-CUSTODY class exists to prevent.

  VER-CMP   every comparison fixture classifies via the detector pivot, and an
            unavailable pivot yields INDETERMINATE, never CODE-NET-NEW
  VER-MIG   every USER-CUSTODY member has a SPECIFIED migrator or is excluded
            from discharge; migrators are offline (A1-VER-01 / A1-VER-02)
  VER-DEP   dependency citations resolve to live binding artifacts and declare a
            direction, so ownership cannot be circular (B-SCV2-06)
  VER-EG    no support window is sealed while its evidenceGrade is GUESSED
  VER-DIS   implementable test declarations specify properties but never
            discharge them; DISCHARGED/DEMONSTRATED requires retained evidence
  VER-CUST  every versioned identity declares a custody class
  VER-HIST  historical trusted declarative semantics bind exact canonical bytes,
            signed per-platform native Rust payloads, pinned trust-root/public-key
            bytes and mechanically verified Ed25519 signatures; missing capability
            dependencies fail closed without mutating old Runs

Usage: python3 artifacts/check-versioning.py [contract]   ·   --selftest
Exit:  0 clean · 1 findings · 2 IO error
"""
from __future__ import annotations
import base64, binascii, copy, hashlib, json, re, sys, pathlib

BINDING = "versioning-policy.v4.json"
HERE = pathlib.Path(__file__).resolve().parent
REFPAT = re.compile(r"^sha256:[0-9a-f]{64}$")

V4_BINDING_FIELDS = {
    "semanticsKind", "scope", "semanticsRef", "irFamily", "irMajor",
    "verifierAbi", "trustProfileId", "providerId", "releaseId",
    "signingKeyId", "trustRootRef", "publicKeyRef", "verifierManifestRef",
    "verifierArtifactRef", "platformId", "targetTriple", "executableAbi",
    "payloadMediaType", "entrypoint",
}
CAS_FIELDS = {"ref", "kind", "mediaType", "encoding", "target", "entrypoint", "bytes"}
NATIVE_MEDIA = "application/vnd.opensip.rust-native-executable"

# Self-contained strict Ed25519 verification (RFC 8032 equation and encodings).
# It is used only for offline design fixtures; no product execution claim follows.
_ED_Q = 2 ** 255 - 19
_ED_L = 2 ** 252 + 27742317777372353535851937790883648493


def _ed_inv(value: int) -> int:
    return pow(value, _ED_Q - 2, _ED_Q)


_ED_D = (-121665 * _ed_inv(121666)) % _ED_Q
_ED_I = pow(2, (_ED_Q - 1) // 4, _ED_Q)


def _ed_xrecover(y: int) -> int:
    xx = (y * y - 1) * _ed_inv(_ED_D * y * y + 1) % _ED_Q
    x = pow(xx, (_ED_Q + 3) // 8, _ED_Q)
    if (x * x - xx) % _ED_Q:
        x = x * _ED_I % _ED_Q
    if x & 1:
        x = _ED_Q - x
    return x


_ED_BY = 4 * _ed_inv(5) % _ED_Q
_ED_B = (_ed_xrecover(_ED_BY), _ED_BY)
_ED_IDENTITY = (0, 1)


def _ed_add(p: tuple[int, int], q: tuple[int, int]) -> tuple[int, int]:
    x1, y1 = p
    x2, y2 = q
    common = _ED_D * x1 * x2 * y1 * y2 % _ED_Q
    return ((x1 * y2 + x2 * y1) * _ed_inv(1 + common) % _ED_Q,
            (y1 * y2 + x1 * x2) * _ed_inv(1 - common) % _ED_Q)


def _ed_scalar(point: tuple[int, int], value: int) -> tuple[int, int]:
    result = _ED_IDENTITY
    current = point
    while value:
        if value & 1:
            result = _ed_add(result, current)
        current = _ed_add(current, current)
        value >>= 1
    return result


def _ed_encode(point: tuple[int, int]) -> bytes:
    x, y = point
    return (y | ((x & 1) << 255)).to_bytes(32, "little")


def _ed_decode(value: bytes) -> tuple[int, int]:
    if len(value) != 32:
        raise ValueError("Ed25519 point must be 32 bytes")
    encoded = int.from_bytes(value, "little")
    y = encoded & ((1 << 255) - 1)
    if y >= _ED_Q:
        raise ValueError("non-canonical Ed25519 y")
    x = _ed_xrecover(y)
    if (x & 1) != (encoded >> 255):
        x = _ED_Q - x
    point = (x, y)
    if ((-x * x + y * y - 1 - _ED_D * x * x * y * y) % _ED_Q
            or _ed_encode(point) != value):
        raise ValueError("invalid Ed25519 point")
    return point


def _ed25519_verify(public_key: bytes, message: bytes, signature: bytes) -> bool:
    try:
        if len(public_key) != 32 or len(signature) != 64:
            return False
        a = _ed_decode(public_key)
        r = _ed_decode(signature[:32])
        s = int.from_bytes(signature[32:], "little")
        if s >= _ED_L or a == _ED_IDENTITY or r == _ED_IDENTITY:
            return False
        # Require prime-order subgroup points, preventing small-order ambiguity.
        if _ed_scalar(a, _ED_L) != _ED_IDENTITY or _ed_scalar(r, _ED_L) != _ED_IDENTITY:
            return False
        challenge = int.from_bytes(
            hashlib.sha512(signature[:32] + public_key + message).digest(), "little") % _ED_L
        return _ed_scalar(_ED_B, s) == _ed_add(r, _ed_scalar(a, challenge))
    except (TypeError, ValueError, OverflowError):
        return False


def _sha256_ref(value: str) -> str:
    return "sha256:" + hashlib.sha256(value.encode("utf-8")).hexdigest()


def _ref_id(value, *, kind: str | None = None) -> str | None:
    if not isinstance(value, dict) or set(value) != {"kind", "id"}:
        return None
    if not isinstance(value.get("kind"), str) or not isinstance(value.get("id"), str):
        return None
    if kind is not None and value["kind"] != kind:
        return None
    return value["id"] if REFPAT.fullmatch(value["id"]) else None


def _content_ref(kind: str, rid: str) -> dict:
    """Construct the one closed content-reference shape used by v4 controls."""
    return {"kind": kind, "id": rid}


def _historical_decision_v3(policy: dict, fx: object) -> dict:
    """Pure, total decision over one cross-major fixture.

    This function deliberately returns dependency availability, not a capability
    rank. retention-tiers.v7 is the sole authority that turns object state into
    effectiveCapability.
    """
    refusal = {
        "decision": "REFUSE-AUTHORITATIVE-READ",
        "capabilityDependencyState": "UNAVAILABLE",
        "authoritativeRead": "REFUSE-VIA-EXISTING-D9",
        "reason": "historical-binding-mismatch",
        "runIdentityUnchanged": False,
        "sealedCapabilityUnchanged": False,
    }
    if not isinstance(fx, dict):
        return refusal
    refusal["runIdentityUnchanged"] = (
        isinstance(fx.get("sealedRunId"), str)
        and fx.get("sealedRunId") == fx.get("observedRunId")
    )
    refusal["sealedCapabilityUnchanged"] = (
        isinstance(fx.get("sealedCapability"), str)
        and fx.get("sealedCapability") == fx.get("observedSealedCapability")
    )
    if not refusal["runIdentityUnchanged"]:
        refusal["reason"] = "historical-run-identity-mutation"
        return refusal

    binding = fx.get("binding")
    exact_binding = {"semanticsKind", "scope", "irFamily", "irMajor", "verifierAbi",
                     "semanticsRef", "verifierArtifactRef"}
    if not isinstance(binding, dict) or set(binding) != exact_binding:
        return refusal
    if binding.get("scope") != "trusted-bundled-declarative-v1":
        refusal.update(decision="OUTSIDE-HISTORICAL-POLICY",
                       reason="historical-scope-excluded")
        return refusal
    semantic_kind = binding.get("semanticsKind")
    if semantic_kind not in {"predicate", "policy"}:
        return refusal
    if (not isinstance(binding.get("irFamily"), str)
            or not isinstance(binding.get("irMajor"), int)
            or isinstance(binding.get("irMajor"), bool)
            or binding["irMajor"] < 1
            or not isinstance(binding.get("verifierAbi"), str)):
        return refusal

    available = fx.get("availableRefs")
    if (not isinstance(available, list)
            or not all(isinstance(x, str) and REFPAT.fullmatch(x) for x in available)
            or len(available) != len(set(available))):
        return refusal
    available_set = set(available)
    oracle: dict[str, dict] = {}
    for entry in policy.get("casOracle", []) if isinstance(policy, dict) else []:
        if isinstance(entry, dict) and isinstance(entry.get("ref"), str):
            oracle.setdefault(entry["ref"], entry)

    expected_sem_kind = f"{semantic_kind}-semantics"
    sem_id = _ref_id(binding.get("semanticsRef"), kind=expected_sem_kind)
    if sem_id is None:
        return refusal
    if sem_id not in available_set or sem_id not in oracle:
        refusal["reason"] = "historical-semantics-unavailable"
        return refusal
    sem_entry = oracle[sem_id]
    try:
        semantics = json.loads(sem_entry.get("canonicalBytes"))
    except (TypeError, ValueError, json.JSONDecodeError):
        return refusal
    if (not isinstance(semantics, dict)
            or sem_entry.get("kind") != expected_sem_kind
            or semantics.get("irFamily") != binding["irFamily"]
            or semantics.get("irMajor") != binding["irMajor"]):
        return refusal

    verifier_id = _ref_id(binding.get("verifierArtifactRef"), kind="verifier-artifact")
    if verifier_id is None:
        return refusal
    if verifier_id not in available_set or verifier_id not in oracle:
        refusal["reason"] = "historical-verifier-artifact-unavailable"
        return refusal
    verifier_entry = oracle[verifier_id]
    try:
        verifier = json.loads(verifier_entry.get("canonicalBytes"))
    except (TypeError, ValueError, json.JSONDecodeError):
        return refusal
    if (not isinstance(verifier, dict)
            or verifier_entry.get("kind") != "verifier-artifact"
            or binding["irFamily"] not in verifier.get("irFamilies", [])
            or binding["irMajor"] not in verifier.get("irMajors", [])
            or verifier.get("verifierAbi") != binding["verifierAbi"]):
        return refusal

    manifests = [m for m in policy.get("trustedVerifierManifest", [])
                 if isinstance(m, dict)
                 and _ref_id(m.get("verifierArtifactRef"), kind="verifier-artifact")
                 == verifier_id]
    if len(manifests) != 1:
        refusal["reason"] = "historical-verifier-untrusted"
        return refusal
    manifest = manifests[0]
    if (manifest.get("signatureScheme") != "ed25519"
            or manifest.get("bundleMode") != "in-release-offline"
            or not isinstance(manifest.get("signingKeyId"), str)
            or not manifest.get("signingKeyId")
            or binding["irFamily"] not in manifest.get("irFamilies", [])
            or binding["irMajor"] not in manifest.get("irMajors", [])
            or manifest.get("verifierAbi") != binding["verifierAbi"]):
        refusal["reason"] = "historical-verifier-untrusted"
        return refusal
    sig_id = _ref_id(manifest.get("signatureRef"), kind="bundle-signature")
    if sig_id is None or sig_id not in available_set or sig_id not in oracle:
        refusal["reason"] = "historical-signature-material-unavailable"
        return refusal
    if oracle[sig_id].get("kind") != "bundle-signature":
        refusal["reason"] = "historical-verifier-untrusted"
        return refusal

    abis = fx.get("hostSupportedVerifierAbis")
    if not isinstance(abis, list) or binding["verifierAbi"] not in abis:
        refusal["reason"] = "historical-verifier-abi-unsupported"
        return refusal
    return {
        "decision": "VERIFY-HISTORICAL",
        "capabilityDependencyState": "AVAILABLE",
        "authoritativeRead": "ALLOW",
        "reason": None,
        "runIdentityUnchanged": refusal["runIdentityUnchanged"],
        "sealedCapabilityUnchanged": refusal["sealedCapabilityUnchanged"],
    }


def _canonical_json(value: object) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _decode_cas_entry(entry: object) -> tuple[bytes | None, object | None, str | None]:
    """Return exact payload bytes, parsed JSON when applicable, and a typed error."""
    if not isinstance(entry, dict) or set(entry) != CAS_FIELDS:
        return None, None, "entry-shape"
    rid = entry.get("ref")
    if (not isinstance(rid, str) or not REFPAT.fullmatch(rid)
            or not isinstance(entry.get("kind"), str)
            or not isinstance(entry.get("mediaType"), str)
            or entry.get("target") is not None and not isinstance(entry.get("target"), str)
            or entry.get("entrypoint") is not None
            and not isinstance(entry.get("entrypoint"), str)
            or not isinstance(entry.get("bytes"), str)):
        return None, None, "entry-type"
    try:
        if entry.get("encoding") == "utf-8":
            raw = entry["bytes"].encode("utf-8")
        elif entry.get("encoding") == "base64":
            raw = base64.b64decode(entry["bytes"], validate=True)
        else:
            return None, None, "entry-encoding"
    except (UnicodeEncodeError, ValueError, binascii.Error):
        return None, None, "entry-bytes"
    if "sha256:" + hashlib.sha256(raw).hexdigest() != rid:
        return None, None, "entry-digest"
    parsed = None
    if entry["mediaType"] == "application/json":
        if entry.get("encoding") != "utf-8" or entry.get("target") is not None \
                or entry.get("entrypoint") is not None:
            return None, None, "json-envelope"
        try:
            parsed = json.loads(raw.decode("utf-8"))
        except (UnicodeDecodeError, ValueError, json.JSONDecodeError):
            return None, None, "json-parse"
        if _canonical_json(parsed).encode("utf-8") != raw:
            return None, None, "json-canonical"
    return raw, parsed, None


def _oracle_index(policy: dict) -> dict[str, dict] | None:
    oracle = policy.get("casOracle") if isinstance(policy, dict) else None
    if not isinstance(oracle, list):
        return None
    result: dict[str, dict] = {}
    for entry in oracle:
        if not isinstance(entry, dict) or not isinstance(entry.get("ref"), str) \
                or entry["ref"] in result:
            return None
        result[entry["ref"]] = entry
    return result


def _required_dependencies(binding: dict, signature_id: str | None) -> list[dict]:
    rows = [
        (_ref_id(binding.get("semanticsRef")),
         binding.get("semanticsRef", {}).get("kind")
         if isinstance(binding.get("semanticsRef"), dict) else None),
        (_ref_id(binding.get("verifierManifestRef"), kind="verifier-manifest"),
         "verifier-manifest"),
        (_ref_id(binding.get("verifierArtifactRef")), "verifier-executable"),
        (signature_id, "bundle-signature"),
        (_ref_id(binding.get("trustRootRef"), kind="verifier-trust-root"),
         "verifier-trust-root"),
        (_ref_id(binding.get("publicKeyRef"), kind="verifier-public-key"),
         "verifier-public-key"),
    ]
    clean = [(rid, kind) for rid, kind in rows
             if rid is not None and isinstance(kind, str)]
    return [{"ref": rid, "kind": kind, "requiredForCapability": "verifiable"}
            for rid, kind in sorted(clean)]


def _historical_decision_v4(policy: dict, fx: object) -> dict:
    refusal = {
        "decision": "REFUSE-AUTHORITATIVE-READ",
        "capabilityDependencyState": "UNAVAILABLE",
        "authoritativeRead": "REFUSE-VIA-EXISTING-D9",
        "reason": "historical-binding-mismatch",
        "runIdentityUnchanged": False,
        "sealedCapabilityUnchanged": False,
        "requiredDependencies": [],
    }
    if not isinstance(policy, dict) or not isinstance(fx, dict):
        return refusal
    refusal["runIdentityUnchanged"] = (
        isinstance(fx.get("sealedRunId"), str)
        and fx.get("sealedRunId") == fx.get("observedRunId"))
    refusal["sealedCapabilityUnchanged"] = (
        isinstance(fx.get("sealedCapability"), str)
        and fx.get("sealedCapability") == fx.get("observedSealedCapability"))
    if not refusal["runIdentityUnchanged"]:
        refusal["reason"] = "historical-run-identity-mutation"
        return refusal
    if not refusal["sealedCapabilityUnchanged"]:
        refusal["reason"] = "historical-sealed-capability-mutation"
        return refusal
    binding = fx.get("binding")
    if not isinstance(binding, dict) or set(binding) != V4_BINDING_FIELDS:
        return refusal
    if binding.get("scope") != "trusted-bundled-declarative-v1":
        refusal.update(decision="OUTSIDE-HISTORICAL-POLICY",
                       reason="historical-scope-excluded")
        return refusal
    semantic_kind = binding.get("semanticsKind")
    expected_sem_kind = f"{semantic_kind}-semantics"
    if semantic_kind not in {"predicate", "policy"}:
        return refusal
    scalar_strings = {
        "irFamily", "verifierAbi", "trustProfileId", "providerId", "releaseId",
        "signingKeyId", "platformId", "targetTriple", "executableAbi",
        "payloadMediaType", "entrypoint",
    }
    if (not isinstance(binding.get("irMajor"), int)
            or isinstance(binding.get("irMajor"), bool) or binding["irMajor"] < 1
            or any(not isinstance(binding.get(key), str) or not binding[key]
                   for key in scalar_strings)):
        return refusal
    available = fx.get("availableRefs")
    if (not isinstance(available, list)
            or not all(isinstance(x, str) and REFPAT.fullmatch(x) for x in available)
            or len(available) != len(set(available))):
        return refusal
    available_set = set(available)
    oracle = _oracle_index(policy)
    if oracle is None:
        return refusal

    manifest_id = _ref_id(binding.get("verifierManifestRef"), kind="verifier-manifest")
    signed = [x for x in policy.get("signedVerifierBindings", [])
              if isinstance(x, dict)
              and _ref_id(x.get("manifestRef"), kind="verifier-manifest") == manifest_id]
    signature_id = (_ref_id(signed[0].get("signatureRef"), kind="bundle-signature")
                    if len(signed) == 1 else None)
    refusal["requiredDependencies"] = _required_dependencies(binding, signature_id)

    def resolve(ref_value: object, expected_kind: str, unavailable_reason: str):
        rid = _ref_id(ref_value, kind=expected_kind)
        if rid is None or rid not in oracle or rid not in available_set:
            refusal["reason"] = unavailable_reason
            return None
        raw, parsed, error = _decode_cas_entry(oracle[rid])
        if error is not None:
            refusal["reason"] = unavailable_reason
            return None
        if oracle[rid].get("kind") != expected_kind:
            refusal["reason"] = unavailable_reason
            return None
        return oracle[rid], raw, parsed

    semantics_resolved = resolve(binding.get("semanticsRef"), expected_sem_kind,
                                 "historical-semantics-unavailable")
    if semantics_resolved is None:
        return refusal
    _, _, semantics = semantics_resolved
    if not isinstance(semantics, dict):
        return refusal
    semantics_schema_name = ("PredicateSemantics" if semantic_kind == "predicate"
                             else "PolicySemantics")
    semantics_fields = set((policy.get("closedSchemas", {}).get(
        semantics_schema_name, {}) or {}).get("required", []))
    if not semantics_fields or set(semantics) != semantics_fields:
        return refusal
    if semantics.get("artifact") != f"opensip.{semantic_kind}-semantics":
        return refusal
    semantics_expected = {
        "irFamily": binding["irFamily"],
        "irMajor": binding["irMajor"],
        "verifierAbi": binding["verifierAbi"],
        "trustProfileId": binding["trustProfileId"],
        "verifierArtifactRef": binding["verifierArtifactRef"],
        "verifierManifestRef": binding["verifierManifestRef"],
    }
    if any(semantics.get(key) != value for key, value in semantics_expected.items()):
        return refusal

    if len(signed) != 1 or signature_id is None:
        refusal["reason"] = "historical-verifier-untrusted"
        return refusal
    manifest_resolved = resolve(binding.get("verifierManifestRef"),
                                "verifier-manifest", "historical-manifest-unavailable")
    if manifest_resolved is None:
        return refusal
    _, manifest_raw, manifest = manifest_resolved
    if not isinstance(manifest, dict):
        return refusal
    expected_manifest_fields = set((policy.get("closedSchemas", {}).get(
        "SignedVerifierManifest", {}) or {}).get("required", []))
    if not expected_manifest_fields or set(manifest) != expected_manifest_fields:
        return refusal
    manifest_equalities = {
        "providerId": binding["providerId"], "releaseId": binding["releaseId"],
        "trustProfileId": binding["trustProfileId"],
        "signingKeyId": binding["signingKeyId"],
        "trustRootRef": binding["trustRootRef"], "irFamily": binding["irFamily"],
        "irMajor": binding["irMajor"], "verifierAbi": binding["verifierAbi"],
        "signatureScheme": "ed25519", "bundleMode": "in-release-offline",
    }
    if any(manifest.get(key) != value for key, value in manifest_equalities.items()):
        return refusal
    payloads = manifest.get("payloads")
    if not isinstance(payloads, list):
        return refusal
    expected_platforms = policy.get("deliverySupportedPlatforms")
    if (not isinstance(expected_platforms, list)
            or sorted((x.get("platformId"), x.get("targetTriple"), x.get("executableAbi"))
                      for x in payloads if isinstance(x, dict))
            != sorted((x.get("platformId"), x.get("targetTriple"), x.get("executableAbi"))
                      for x in expected_platforms if isinstance(x, dict))
            or len(payloads) != len(expected_platforms)):
        return refusal
    selected = [x for x in payloads if isinstance(x, dict)
                and x.get("platformId") == binding["platformId"]]
    if len(selected) != 1:
        refusal["reason"] = "historical-verifier-platform-unsupported"
        return refusal
    selected = selected[0]
    exact_payload_fields = {"platformId", "targetTriple", "executableAbi", "mediaType",
                            "entrypoint", "payloadRef"}
    if set(selected) != exact_payload_fields:
        return refusal
    selected_equalities = {
        "platformId": binding["platformId"], "targetTriple": binding["targetTriple"],
        "executableAbi": binding["executableAbi"],
        "mediaType": binding["payloadMediaType"],
        "entrypoint": binding["entrypoint"],
        "payloadRef": binding["verifierArtifactRef"],
    }
    if any(selected.get(key) != value for key, value in selected_equalities.items()):
        return refusal

    if (fx.get("hostPlatformId") != binding["platformId"]
            or fx.get("hostTargetTriple") != binding["targetTriple"]
            or fx.get("hostExecutableAbi") != binding["executableAbi"]):
        refusal["reason"] = "historical-verifier-platform-unsupported"
        return refusal
    host_abis = fx.get("hostSupportedVerifierAbis")
    if not isinstance(host_abis, list) or binding["verifierAbi"] not in host_abis:
        refusal["reason"] = "historical-verifier-abi-unsupported"
        return refusal

    payload_id = _ref_id(binding.get("verifierArtifactRef"))
    if payload_id is None or payload_id not in oracle or payload_id not in available_set:
        refusal["reason"] = "historical-verifier-artifact-unavailable"
        return refusal
    payload_entry = oracle[payload_id]
    payload_raw, _, payload_error = _decode_cas_entry(payload_entry)
    if payload_error is not None:
        refusal["reason"] = "historical-verifier-artifact-unavailable"
        return refusal
    if (payload_entry.get("kind") != "verifier-executable"
            or payload_entry.get("mediaType") != NATIVE_MEDIA
            or binding["payloadMediaType"] != NATIVE_MEDIA
            or payload_entry.get("encoding") != "base64"
            or payload_entry.get("target") != binding["targetTriple"]
            or payload_entry.get("entrypoint") != binding["entrypoint"]
            or not isinstance(payload_raw, bytes) or len(payload_raw) < 32):
        refusal["reason"] = "historical-executable-incompatible"
        return refusal

    trust_resolved = resolve(binding.get("trustRootRef"), "verifier-trust-root",
                             "historical-trust-root-unavailable")
    if trust_resolved is None:
        return refusal
    _, _, trust_root = trust_resolved
    trust_fields = set((policy.get("closedSchemas", {}).get(
        "VerifierTrustRoot", {}) or {}).get("required", []))
    if not isinstance(trust_root, dict) or set(trust_root) != trust_fields:
        refusal["reason"] = "historical-verifier-untrusted"
        return refusal
    if (trust_root.get("providerId") != binding["providerId"]
            or trust_root.get("trustProfileId") != binding["trustProfileId"]
            or trust_root.get("keyId") != binding["signingKeyId"]
            or trust_root.get("publicKeyRef") != binding["publicKeyRef"]
            or trust_root.get("algorithm") != "ed25519"
            or trust_root.get("publicKeyEncoding") != "raw-32-byte-ed25519"
            or trust_root.get("status") != "PINNED-OFFLINE-TEST-ROOT"
            or trust_root.get("tofu") is not False
            or trust_root.get("networkLookup") is not False):
        refusal["reason"] = "historical-verifier-untrusted"
        return refusal
    key_resolved = resolve(binding.get("publicKeyRef"), "verifier-public-key",
                           "historical-trust-root-unavailable")
    if key_resolved is None:
        return refusal
    key_entry, public_key, _ = key_resolved
    if (key_entry.get("mediaType") != "application/vnd.opensip.ed25519-public-key"
            or key_entry.get("encoding") != "base64"
            or key_entry.get("target") is not None
            or key_entry.get("entrypoint") is not None
            or not isinstance(public_key, bytes) or len(public_key) != 32):
        refusal["reason"] = "historical-verifier-untrusted"
        return refusal

    signature_ref = signed[0].get("signatureRef")
    signature_resolved = resolve(signature_ref, "bundle-signature",
                                 "historical-signature-material-unavailable")
    if signature_resolved is None:
        return refusal
    signature_entry, signature, _ = signature_resolved
    if (signature_entry.get("mediaType")
            != "application/vnd.opensip.ed25519-signature"
            or signature_entry.get("encoding") != "base64"
            or signature_entry.get("target") is not None
            or signature_entry.get("entrypoint") is not None
            or not isinstance(signature, bytes) or len(signature) != 64
            or not isinstance(manifest_raw, bytes)
            or not _ed25519_verify(public_key, manifest_raw, signature)):
        refusal["reason"] = "historical-signature-invalid"
        return refusal
    return {
        "decision": "VERIFY-HISTORICAL",
        "capabilityDependencyState": "AVAILABLE",
        "authoritativeRead": "ALLOW",
        "reason": None,
        "runIdentityUnchanged": refusal["runIdentityUnchanged"],
        "sealedCapabilityUnchanged": refusal["sealedCapabilityUnchanged"],
        "requiredDependencies": refusal["requiredDependencies"],
    }


def _historical_decision(policy: dict, fx: object) -> dict:
    """Version-dispatched public decision retained for frozen Evidence v3 callers."""
    if isinstance(policy, dict) and "signedVerifierBindings" in policy:
        return _historical_decision_v4(policy, fx)
    return _historical_decision_v3(policy, fx)


def _migration_decision(fx: object) -> dict:
    if not isinstance(fx, dict):
        return {"decision": "REJECT-MIGRATION",
                "reason": "historical-run-identity-rewrite-forbidden",
                "sourceRunIdentityUnchanged": False}
    unchanged = (isinstance(fx.get("sourceRunId"), str)
                 and fx.get("sourceRunIdAfter") == fx.get("sourceRunId"))
    valid_new = (fx.get("action") == "CREATE-NEW-RUN" and unchanged
                 and isinstance(fx.get("newRunId"), str)
                 and fx.get("newRunId") != fx.get("sourceRunId")
                 and fx.get("lineageSourceRunId") == fx.get("sourceRunId"))
    if valid_new:
        return {"decision": "ACCEPT-NEW-RUN", "reason": None,
                "sourceRunIdentityUnchanged": True}
    return {"decision": "REJECT-MIGRATION",
            "reason": "historical-run-identity-rewrite-forbidden",
            "sourceRunIdentityUnchanged": unchanged}


def classify(fx: dict) -> str:
    """The detector-pivot decomposition. Pure; this IS the policy."""
    if not fx["pivotAvailable"]:
        return "INDETERMINATE"
    b, p, c = fx["inBaseline"], fx["inPivot"], fx["inCurrent"]
    if p and not b:
        return "CODE-NET-NEW"          # same detector, new code -> real regression
    if c and not p:
        return "DETECTION-DELTA"       # detector changed its mind about unchanged code
    if b and not p:
        return "CODE-FIXED"
    return "UNCHANGED"


def _cas_entry_from_json(kind: str, value: dict) -> dict:
    raw = _canonical_json(value).encode("utf-8")
    return {
        "ref": "sha256:" + hashlib.sha256(raw).hexdigest(),
        "kind": kind,
        "mediaType": "application/json",
        "encoding": "utf-8",
        "target": None,
        "entrypoint": None,
        "bytes": raw.decode("utf-8"),
    }


def _materialize_custody_control(policy: dict, base_fixture: dict,
                                 control: dict) -> tuple[dict, dict]:
    """Apply one retained R12 control without any network/private-key operation."""
    hp = copy.deepcopy(policy)
    fx = copy.deepcopy(base_fixture)
    for entry in hp.get("controlCasOracle", []):
        if isinstance(entry, dict) and not any(
                isinstance(old, dict) and old.get("ref") == entry.get("ref")
                for old in hp.get("casOracle", [])):
            hp["casOracle"].append(copy.deepcopy(entry))
    mutation = control.get("mutation")
    binding = fx["binding"]

    def add_available(ref_value: object) -> None:
        rid = _ref_id(ref_value)
        if rid is not None and rid not in fx["availableRefs"]:
            fx["availableRefs"].append(rid)

    def replace_manifest() -> None:
        manifest_ref = control.get("replacementManifestRef")
        signature_ref = control.get("replacementSignatureRef")
        manifest_id = _ref_id(manifest_ref, kind="verifier-manifest")
        signature_id = _ref_id(signature_ref, kind="bundle-signature")
        if manifest_id is None or signature_id is None:
            raise ValueError("control replacement manifest/signature missing")
        oracle = _oracle_index(hp)
        semantics_id = _ref_id(binding["semanticsRef"])
        if oracle is None or semantics_id not in oracle:
            raise ValueError("base semantics unavailable")
        _, semantics, error = _decode_cas_entry(oracle[semantics_id])
        if error is not None or not isinstance(semantics, dict):
            raise ValueError("base semantics malformed")
        semantics = copy.deepcopy(semantics)
        semantics["verifierManifestRef"] = copy.deepcopy(manifest_ref)
        if mutation == "descriptor-without-payload":
            semantics["verifierArtifactRef"] = copy.deepcopy(
                control["replacementPayloadRef"])
            binding["verifierArtifactRef"] = copy.deepcopy(
                control["replacementPayloadRef"])
            binding["payloadMediaType"] = "application/json"
            add_available(control["replacementPayloadRef"])
        semantics_entry = _cas_entry_from_json(binding["semanticsRef"]["kind"], semantics)
        hp["casOracle"].append(semantics_entry)
        binding["semanticsRef"] = _content_ref(binding["semanticsRef"]["kind"],
                                               semantics_entry["ref"])
        binding["verifierManifestRef"] = copy.deepcopy(manifest_ref)
        hp["signedVerifierBindings"].append({
            "manifestRef": copy.deepcopy(manifest_ref),
            "signatureRef": copy.deepcopy(signature_ref),
        })
        add_available(binding["semanticsRef"])
        add_available(manifest_ref)
        add_available(signature_ref)

    if mutation == "identity":
        pass
    elif mutation == "semantics-verifier-ref-substitution":
        oracle = _oracle_index(hp)
        manifest_id = _ref_id(binding["verifierManifestRef"], kind="verifier-manifest")
        _, manifest, error = _decode_cas_entry(oracle[manifest_id]) if oracle and manifest_id \
            else (None, None, "missing")
        candidates = [x for x in manifest.get("payloads", [])
                      if isinstance(x, dict) and x.get("platformId") == "macos-aarch64"] \
            if isinstance(manifest, dict) and error is None else []
        if len(candidates) != 1:
            raise ValueError("alternate platform payload unavailable")
        binding["verifierArtifactRef"] = copy.deepcopy(candidates[0]["payloadRef"])
        add_available(binding["verifierArtifactRef"])
    elif mutation == "semantics-abi-substitution":
        binding["verifierAbi"] = "opensip.offline-verifier-abi.v2"
    elif mutation == "replace-signed-manifest":
        replace_manifest()
    elif mutation == "corrupt-executable-bytes":
        rid = _ref_id(binding["verifierArtifactRef"])
        entry = next(x for x in hp["casOracle"] if x.get("ref") == rid)
        raw = base64.b64decode(entry["bytes"], validate=True)
        entry["bytes"] = base64.b64encode(raw + b"!").decode("ascii")
    elif mutation == "replace-public-key-chain":
        replace_manifest()
        binding["trustRootRef"] = copy.deepcopy(control["replacementTrustRootRef"])
        binding["publicKeyRef"] = copy.deepcopy(control["replacementPublicKeyRef"])
        add_available(binding["trustRootRef"])
        add_available(binding["publicKeyRef"])
    elif mutation == "replace-signature":
        signature_ref = control.get("replacementSignatureRef")
        manifest_id = _ref_id(binding["verifierManifestRef"], kind="verifier-manifest")
        selected = [x for x in hp["signedVerifierBindings"]
                    if _ref_id(x.get("manifestRef"), kind="verifier-manifest")
                    == manifest_id]
        if len(selected) != 1 or _ref_id(signature_ref, kind="bundle-signature") is None:
            raise ValueError("signature substitution cannot apply")
        selected[0]["signatureRef"] = copy.deepcopy(signature_ref)
        add_available(signature_ref)
    elif mutation == "descriptor-without-payload":
        replace_manifest()
    elif mutation == "missing-trust-root":
        rid = _ref_id(binding["trustRootRef"], kind="verifier-trust-root")
        fx["availableRefs"] = [x for x in fx["availableRefs"] if x != rid]
    else:
        raise ValueError(f"unknown custody control mutation {mutation!r}")
    fx["availableRefs"] = sorted(set(fx["availableRefs"]))
    return hp, fx


def _check_historical_v4(contract: dict, policy: dict) -> list[str]:
    out: list[str] = []
    scope = policy.get("scope") or {}
    if set(scope.get("included", [])) != {"trusted-bundled-declarative-v1"}:
        out.append("VER-HIST: historical scope is not the one trusted bundled declarative path")
    if not {"untrusted-imperative", "Probe"}.issubset(set(scope.get("excluded", []))):
        out.append("VER-HIST: imperative semantics or Probe entered historical authority")
    support = policy.get("supportPosture") or {}
    if (support.get("fixedSupportWindow") is not False
            or support.get("sla") is not False
            or support.get("costClaim") != "NONE"
            or support.get("consumerLabel") != "PROVISIONAL"):
        out.append("VER-HIST: support is not artifact-custody PROVISIONAL/no-SLA/no-cost")
    join = policy.get("capabilityJoin") or {}
    if join.get("authority") != "artifacts/retention-tiers.v7.json" \
            or "may not copy ranks" not in str(join.get("forbidden", "")):
        out.append("VER-HIST: retention v7 is not the sole capability authority")
    if ("Evidence v3" not in str(join.get("futureRejoin", ""))
            or "VERSIONING v3" not in str(join.get("futureRejoin", ""))
            or "Phase1A v3/v8" not in str(join.get("futureRejoin", ""))):
        out.append("VER-HIST: frozen Evidence v3 / future Phase1A v3-v8 rejoin boundary missing")

    trust = policy.get("trustModel") or {}
    if (trust.get("signatureScheme") != "ed25519"
            or trust.get("manifestEncoding") != "canonical-json-utf8"
            or trust.get("trustRootMode") != "PINNED-RETAINED-BYTES"
            or trust.get("tofu") is not False
            or trust.get("networkLookup") is not False
            or trust.get("adjacentMetadataAuthority") is not False
            or trust.get("privateKeyRetained") is not False):
        out.append("VER-HIST: trust model permits TOFU/network/adjacent authority or lacks pinned bytes")

    release = policy.get("releaseCustody") or {}
    delivery_path = HERE / "delivery.v2.json"
    expected_delivery_hash = (hashlib.sha256(delivery_path.read_bytes()).hexdigest()
                              if delivery_path.exists() else None)
    if (release.get("authority") != "artifacts/delivery.v2.json"
            or release.get("sha256") != expected_delivery_hash
            or release.get("networkLookup") is not False
            or release.get("executionClaim") != "NONE; fixture bytes are never executed by this checker"):
        out.append("VER-HIST: native payload custody is not exactly bound to DELIVERY v2")
    delivery_ids: set[str] = set()
    if delivery_path.exists():
        try:
            delivery = json.loads(delivery_path.read_text())
            # The live matrix is intentionally located by shape, not a copied count.
            def collect(value):
                if isinstance(value, list) and value and all(isinstance(x, dict)
                        and {"platformId", "os", "arch", "abi"}.issubset(x) for x in value):
                    delivery_ids.update(x["platformId"] for x in value)
                elif isinstance(value, dict):
                    for child in value.values():
                        collect(child)
                elif isinstance(value, list):
                    for child in value:
                        collect(child)
            collect(delivery)
        except (OSError, ValueError, json.JSONDecodeError):
            pass
    declared_platforms = policy.get("deliverySupportedPlatforms")
    declared_ids = {x.get("platformId") for x in declared_platforms
                    if isinstance(x, dict)} if isinstance(declared_platforms, list) else set()
    declared_map = {x.get("platformId"): x for x in declared_platforms
                    if isinstance(x, dict)} if isinstance(declared_platforms, list) else {}
    if (not delivery_ids or declared_ids != delivery_ids
            or len(declared_ids) != len(declared_platforms or [])
            or any(set(x) != {"platformId", "targetTriple", "executableAbi"}
                   or any(not isinstance(x.get(key), str) or not x[key]
                          for key in ("platformId", "targetTriple", "executableAbi"))
                   for x in declared_platforms or [] if isinstance(x, dict))):
        out.append("VER-HIST: per-platform payload map does not cover exact DELIVERY supported set")

    required_reasons = {
        "historical-scope-excluded", "historical-semantics-unavailable",
        "historical-manifest-unavailable", "historical-verifier-artifact-unavailable",
        "historical-signature-material-unavailable", "historical-trust-root-unavailable",
        "historical-signature-invalid", "historical-executable-incompatible",
        "historical-verifier-platform-unsupported", "historical-verifier-abi-unsupported",
        "historical-binding-mismatch", "historical-verifier-untrusted",
        "historical-run-identity-mutation", "historical-sealed-capability-mutation",
        "historical-run-identity-rewrite-forbidden",
    }
    reasons = policy.get("typedReasons")
    if not isinstance(reasons, list) or set(reasons) != required_reasons \
            or len(reasons) != len(set(reasons)):
        out.append("VER-HIST: historical refusal reason vocabulary is not exact")
    if set(policy.get("dependencyRoles") or []) != {
            "historical-semantics", "historical-manifest", "historical-executable",
            "historical-signature", "historical-trust-root", "historical-public-key"}:
        out.append("VER-HIST: six historical dependency roles are not exact")

    schemas = policy.get("closedSchemas")
    required_schemas = {"ContentRef", "CasEntry", "HistoricalSemanticsBinding",
                        "SignedVerifierBinding", "NativePayloadMapEntry",
                        "SignedVerifierManifest", "VerifierTrustRoot",
                        "PredicateSemantics", "PolicySemantics",
                        "HistoricalReadFixture", "HistoricalDecision",
                        "RequiredDependency", "CustodyControl"}
    if not isinstance(schemas, dict) or not required_schemas <= set(schemas):
        out.append("VER-HIST: closed custody schemas are incomplete")
        schemas = {}
    for name in required_schemas & set(schemas):
        schema = schemas[name]
        if (not isinstance(schema, dict) or set(schema) != {
                "required", "optional", "additionalProperties"}
                or not isinstance(schema.get("required"), list)
                or schema.get("optional") != []
                or schema.get("additionalProperties") is not False):
            out.append(f"VER-HIST: schema {name} is not exact and closed")
    if set((schemas.get("HistoricalSemanticsBinding") or {}).get("required", [])) \
            != V4_BINDING_FIELDS:
        out.append("VER-HIST: historical binding schema does not type every exact equality field")
    exact_schema_fields = {
        "ContentRef": {"kind", "id"},
        "CasEntry": CAS_FIELDS,
        "SignedVerifierBinding": {"manifestRef", "signatureRef"},
        "NativePayloadMapEntry": {"platformId", "targetTriple", "executableAbi",
                                  "mediaType", "entrypoint", "payloadRef"},
        "RequiredDependency": {"ref", "kind", "requiredForCapability"},
    }
    for name, expected in exact_schema_fields.items():
        if set((schemas.get(name) or {}).get("required", [])) != expected:
            out.append(f"VER-HIST: schema {name} required fields are not exact")

    base_oracle = policy.get("casOracle")
    control_oracle = policy.get("controlCasOracle")
    all_entries = ((base_oracle if isinstance(base_oracle, list) else [])
                   + (control_oracle if isinstance(control_oracle, list) else []))
    if not isinstance(base_oracle, list) or not base_oracle:
        out.append("VER-HIST: base CAS oracle missing")
    if not isinstance(control_oracle, list) or not control_oracle:
        out.append("VER-HIST: retained control CAS oracle missing")
    seen: dict[str, bytes] = {}
    combined_index: dict[str, dict] = {}
    for i, entry in enumerate(all_entries):
        raw, _, error = _decode_cas_entry(entry)
        prefix = "base" if i < len(base_oracle or []) else "control"
        if error is not None:
            out.append(f"VER-HIST: {prefix} CAS entry {i} invalid ({error})")
            continue
        rid = entry["ref"]
        if rid in seen:
            out.append(f"VER-HIST: CAS ref {rid} duplicated across base/control oracles")
        else:
            seen[rid] = raw
            combined_index[rid] = entry
    base_refs = {x.get("ref") for x in base_oracle or [] if isinstance(x, dict)}

    crypto = policy.get("cryptographicVerification") or {}
    vectors = crypto.get("testVectors")
    if (crypto.get("mechanism")
            != "self-contained RFC8032 Ed25519 verifier in check-versioning.py"
            or crypto.get("message") != "exact UTF-8 canonical verifier-manifest bytes"
            or not isinstance(vectors, list) or len(vectors) < 2):
        out.append("VER-HIST: deterministic cryptographic verification declaration missing")
        vectors = []
    for vector in vectors:
        try:
            got = _ed25519_verify(bytes.fromhex(vector["publicKeyHex"]),
                                  bytes.fromhex(vector["messageHex"]),
                                  bytes.fromhex(vector["signatureHex"]))
        except (KeyError, TypeError, ValueError):
            got = None
        if got is None or got != vector.get("expect"):
            out.append(f"VER-HIST: RFC8032 vector {vector.get('id')} derives {got}")
    if not any(x.get("expect") is True for x in vectors if isinstance(x, dict)) \
            or not any(x.get("expect") is False for x in vectors if isinstance(x, dict)):
        out.append("VER-HIST: Ed25519 vectors lack valid/invalid controls")

    signed = policy.get("signedVerifierBindings")
    if not isinstance(signed, list) or not signed:
        out.append("VER-HIST: signed verifier bindings missing")
        signed = []
    signed_manifest_ids: set[str] = set()
    signed_signature_ids: set[str] = set()
    payloads_by_major: dict[int, set[str]] = {}
    for i, record in enumerate(signed):
        path = f"VER-HIST signedVerifierBindings[{i}]"
        if not isinstance(record, dict) or set(record) != {"manifestRef", "signatureRef"}:
            out.append(f"{path}: binding is not closed")
            continue
        mid = _ref_id(record.get("manifestRef"), kind="verifier-manifest")
        sid = _ref_id(record.get("signatureRef"), kind="bundle-signature")
        if (mid is None or sid is None or mid in signed_manifest_ids
                or sid in signed_signature_ids):
            out.append(f"{path}: malformed/duplicate manifest or signature ref")
            continue
        signed_manifest_ids.add(mid)
        signed_signature_ids.add(sid)
        if mid not in base_refs or sid not in base_refs:
            out.append(f"{path}: authoritative signed binding is not retained in base custody")
        manifest_entry, signature_entry = combined_index.get(mid), combined_index.get(sid)
        if manifest_entry is None or signature_entry is None:
            out.append(f"{path}: signed manifest/signature does not resolve")
            continue
        manifest_raw, manifest, manifest_error = _decode_cas_entry(manifest_entry)
        signature_raw, _, signature_error = _decode_cas_entry(signature_entry)
        if (manifest_error or signature_error or not isinstance(manifest, dict)
                or manifest_entry.get("kind") != "verifier-manifest"
                or manifest_entry.get("mediaType") != "application/json"
                or signature_entry.get("kind") != "bundle-signature"
                or signature_entry.get("mediaType")
                != "application/vnd.opensip.ed25519-signature"
                or signature_entry.get("encoding") != "base64"
                or signature_entry.get("target") is not None
                or signature_entry.get("entrypoint") is not None):
            out.append(f"{path}: signed objects fail CAS/canonical decoding")
            continue
        expected_manifest_fields = set((schemas.get("SignedVerifierManifest") or {})
                                       .get("required", []))
        if set(manifest) != expected_manifest_fields:
            out.append(f"{path}: manifest is not exact closed SignedVerifierManifest")
            continue
        payloads = manifest.get("payloads")
        if (not isinstance(payloads, list) or len(payloads) != len(declared_ids)
                or {x.get("platformId") for x in payloads if isinstance(x, dict)}
                != declared_ids):
            out.append(f"{path}: manifest payload map is not exact DELIVERY coverage")
            continue
        for payload in payloads:
            if not isinstance(payload, dict) or set(payload) != {
                    "platformId", "targetTriple", "executableAbi", "mediaType",
                    "entrypoint", "payloadRef"}:
                out.append(f"{path}: native payload map entry is open/malformed")
                continue
            declared = declared_map.get(payload.get("platformId"))
            if (not isinstance(declared, dict)
                    or payload.get("targetTriple") != declared.get("targetTriple")
                    or payload.get("executableAbi") != declared.get("executableAbi")):
                out.append(f"{path}: platform target/executable ABI differs from DELIVERY binding")
            pid = _ref_id(payload.get("payloadRef"), kind="verifier-executable")
            entry = combined_index.get(pid) if pid else None
            raw, _, error = _decode_cas_entry(entry) if entry else (None, None, "missing")
            if (error is not None or entry.get("mediaType") != NATIVE_MEDIA
                    or entry.get("encoding") != "base64"
                    or entry.get("target") != payload.get("targetTriple")
                    or entry.get("entrypoint") != payload.get("entrypoint")
                    or payload.get("mediaType") != NATIVE_MEDIA
                    or not isinstance(raw, bytes) or len(raw) < 32):
                out.append(f"{path}: payload {payload.get('platformId')} is not exact native bytes")
            if isinstance(manifest.get("irMajor"), int) and pid:
                payloads_by_major.setdefault(manifest["irMajor"], set()).add(pid)
        trust_id = _ref_id(manifest.get("trustRootRef"), kind="verifier-trust-root")
        trust_entry = combined_index.get(trust_id) if trust_id else None
        _, trust_value, trust_error = _decode_cas_entry(trust_entry) \
            if trust_entry else (None, None, "missing")
        trust_fields = set((schemas.get("VerifierTrustRoot") or {}).get("required", []))
        if (trust_error is not None or not isinstance(trust_value, dict)
                or set(trust_value) != trust_fields):
            out.append(f"{path}: pinned trust root unavailable")
            continue
        key_id = _ref_id(trust_value.get("publicKeyRef"), kind="verifier-public-key")
        key_entry = combined_index.get(key_id) if key_id else None
        public_key, _, key_error = _decode_cas_entry(key_entry) \
            if key_entry else (None, None, "missing")
        if (key_error is not None or not isinstance(public_key, bytes)
                or len(public_key) != 32
                or trust_value.get("providerId") != manifest.get("providerId")
                or trust_value.get("trustProfileId") != manifest.get("trustProfileId")
                or trust_value.get("keyId") != manifest.get("signingKeyId")
                or trust_value.get("algorithm") != "ed25519"
                or trust_value.get("publicKeyEncoding") != "raw-32-byte-ed25519"
                or trust_value.get("status") != "PINNED-OFFLINE-TEST-ROOT"
                or key_entry.get("kind") != "verifier-public-key"
                or key_entry.get("mediaType")
                != "application/vnd.opensip.ed25519-public-key"
                or key_entry.get("encoding") != "base64"
                or key_entry.get("target") is not None
                or key_entry.get("entrypoint") is not None
                or trust_value.get("tofu") is not False
                or trust_value.get("networkLookup") is not False
                or not _ed25519_verify(public_key, manifest_raw, signature_raw)):
            out.append(f"{path}: detached signature does not verify under retained pinned key")
    major_sets = [refs for _, refs in sorted(payloads_by_major.items())]
    if len(major_sets) < 2 or any(left & right for i, left in enumerate(major_sets)
                                 for right in major_sets[i + 1:]):
        out.append("VER-HIST: IR majors do not have distinct native payload identities")

    fixtures = policy.get("crossMajorFixtures")
    if not isinstance(fixtures, list) or not fixtures:
        out.append("VER-HIST: cross-major fixtures missing")
        fixtures = []
    fixtures_by_id = {x.get("id"): x for x in fixtures if isinstance(x, dict)}
    for fixture in fixtures:
        fixture_fields = set((schemas.get("HistoricalReadFixture") or {})
                             .get("required", []))
        decision_fields = set((schemas.get("HistoricalDecision") or {})
                              .get("required", []))
        if (not isinstance(fixture, dict) or not fixture_fields
                or set(fixture) != fixture_fields):
            out.append("VER-HIST: historical fixture is not exact closed schema")
            continue
        if (not isinstance(fixture.get("expect"), dict) or not decision_fields
                or set(fixture["expect"]) != decision_fields):
            out.append(f"VER-HIST {fixture.get('id')}: decision is not exact closed schema")
            continue
        got = _historical_decision_v4(policy, fixture)
        if got != fixture.get("expect"):
            out.append(f"VER-HIST {fixture.get('id')}: derives {got}, expects {fixture.get('expect')}")
    successes = [x for x in fixtures if isinstance(x, dict)
                 and (x.get("expect") or {}).get("decision") == "VERIFY-HISTORICAL"]
    fixed_dependency_kinds = {"verifier-manifest", "verifier-executable",
                              "bundle-signature", "verifier-trust-root",
                              "verifier-public-key"}
    if (not any(x.get("hostDefaultIrMajor") == 2
                and (x.get("binding") or {}).get("irMajor") == 1 for x in successes)
            or any(len((x.get("expect") or {}).get("requiredDependencies", [])) != 6
                   for x in successes)
            or any(any(d.get("requiredForCapability") != "verifiable"
                       for d in (x.get("expect") or {}).get("requiredDependencies", []))
                   for x in successes)
            or any({d.get("kind") for d in (x.get("expect") or {})
                    .get("requiredDependencies", [])}
                   != fixed_dependency_kinds
                   | {f"{(x.get('binding') or {}).get('semanticsKind')}-semantics"}
                   for x in successes)):
        out.append("VER-HIST: valid cross-major six-object minimum-verifiable closure missing")
    expected_fixture_reasons = {
        "historical-verifier-artifact-unavailable", "historical-manifest-unavailable",
        "historical-trust-root-unavailable", "historical-signature-material-unavailable",
        "historical-verifier-abi-unsupported", "historical-verifier-platform-unsupported",
        "historical-run-identity-mutation", "historical-sealed-capability-mutation",
        "historical-scope-excluded",
    }
    got_fixture_reasons = {(x.get("expect") or {}).get("reason") for x in fixtures
                           if isinstance(x, dict)}
    if not expected_fixture_reasons <= got_fixture_reasons:
        out.append("VER-HIST: missing/incompatible fixture reason coverage incomplete")

    controls = policy.get("custodyControls")
    required_control_mutations = {
        "semantics-verifier-ref-substitution", "semantics-abi-substitution",
        "replace-signed-manifest", "corrupt-executable-bytes",
        "replace-public-key-chain", "replace-signature",
        "descriptor-without-payload", "missing-trust-root", "identity",
    }
    if not isinstance(controls, list) or not controls:
        out.append("VER-HIST: retained custody controls missing")
        controls = []
    if not required_control_mutations <= {x.get("mutation") for x in controls
                                         if isinstance(x, dict)}:
        out.append("VER-HIST: retained custody control mutation coverage incomplete")
    for control in controls:
        if not isinstance(control, dict) or set(control) != set(
                (schemas.get("CustodyControl") or {}).get("required", [])):
            out.append("VER-HIST: custody control is not exact closed schema")
            continue
        base = fixtures_by_id.get(control.get("baseId"))
        if base is None:
            out.append(f"VER-HIST {control.get('id')}: base fixture missing")
            continue
        try:
            mutated_policy, mutated_fixture = _materialize_custody_control(
                policy, base, control)
            got = _historical_decision_v4(mutated_policy, mutated_fixture)
        except Exception as exc:
            out.append(f"VER-HIST {control.get('id')}: control failed to apply ({exc})")
            continue
        if (got.get("decision") != control.get("expectedDecision")
                or got.get("reason") != control.get("expectedReason")):
            out.append(f"VER-HIST {control.get('id')}: derives {got.get('decision')}/"
                       f"{got.get('reason')}, expects {control.get('expectedDecision')}/"
                       f"{control.get('expectedReason')}")

    migrations = policy.get("proofMigrationFixtures")
    if not isinstance(migrations, list) or len(migrations) < 2:
        out.append("VER-HIST: append-only migration/rewrite controls missing")
        migrations = []
    for i, fixture in enumerate(migrations):
        got = _migration_decision(fixture)
        if not isinstance(fixture, dict) or got != fixture.get("expect"):
            out.append(f"VER-HIST migration[{i}]: derives {got}")
    return out


def check(c: dict) -> list[str]:
    f: list[str] = []

    if c.get("artifact") != "opensip.versioning-policy" or c.get("version") != 4:
        f.append("VER-V4: checker requires opensip.versioning-policy version 4")

    # ---- VER-CMP ----
    for fx in c["comparisonFixtures"]:
        got = classify(fx)
        want = fx["expect"]
        if fx["valid"]:
            if got != want:
                f.append(f"VER-CMP {fx['id']}: pivot derives '{got}', fixture expects "
                         f"'{want}'")
        else:
            if got == want:
                f.append(f"VER-CMP {fx['id']}: expected REJECTION ({fx.get('violates')}) "
                         f"but the pivot agrees with '{want}'")
    if not any(not fx["pivotAvailable"] for fx in c["comparisonFixtures"]):
        f.append("VER-CMP: no fixture exercises an unavailable pivot — the INDETERMINATE "
                 "path is untested and that is the path that protects the user")
    if not any(fx["valid"] and fx["expect"] == "DETECTION-DELTA"
               for fx in c["comparisonFixtures"]):
        f.append("VER-CMP: no fixture shows a DETECTION-DELTA — the whole point of the "
                 "three-way comparison is untested")
    dsd = c.get("detectorSemanticDelta", {})
    if "pivot" not in json.dumps(dsd).lower():
        f.append("VER-CMP: no detector pivot is specified (B-CSG-04)")
    if "INDETERMINATE" not in json.dumps(dsd.get("theFix", {}).get("ifPivotUnavailable", {})):
        f.append("VER-CMP: no INDETERMINATE fallback when the pivot is unavailable — the "
                 "delta would be attributed to the user's code")

    # ---- VER-SCHEMA: the result vocabulary must be closed, and only real
    # regressions may gate. A DETECTION-DELTA that fails CI is the whole defect.
    cs = c.get("comparisonSchema")
    if not cs:
        f.append("VER-SCHEMA: no typed comparison result vocabulary — two implementations "
                 "could emit different classifications and both claim conformance")
    else:
        cls = cs["ComparisonResult"]["classification"]
        if not cls.get("closed"):
            f.append("VER-SCHEMA: the classification vocabulary is not closed")
        declared = set(cls["values"])
        used = {fx["expect"] for fx in c["comparisonFixtures"]}
        for u in used - declared:
            f.append(f"VER-SCHEMA: fixture expects '{u}', absent from the vocabulary")
        gate = cs.get("gateRule", "")
        if "CODE-NET-NEW" not in gate or "never gate" not in gate:
            f.append("VER-SCHEMA: no rule restricting which classifications may fail a "
                     "gate — a DETECTION-DELTA failing CI is the defect B-CSG-04 named")

    # ---- VER-MIG ----
    mig = c.get("migrators")
    if not mig:
        f.append("VER-MIG: V2 forbids a USER-CUSTODY breaking change without a migrator "
                 "and none are specified — the rule is vacuous (A1-VER-01)")
    else:
        if "fetch" not in json.dumps(mig.get("airGap", {})).lower():
            f.append("VER-MIG: the air-gap posture does not say migrators fetch nothing "
                     "(A1-VER-02)")
        specified = {m["artifact"] for m in mig["members"] if m.get("status") == "SPECIFIED"}
        for m in mig["members"]:
            if m.get("status") == "SPECIFIED":
                for fld in ("migratorId", "preview", "idempotent", "witness"):
                    if not m.get(fld):
                        f.append(f"VER-MIG: '{m['artifact']}' is SPECIFIED but has no "
                                 f"{fld}")
            elif m.get("status") != "NOT-YET-ENFORCEABLE":
                f.append(f"VER-MIG: '{m['artifact']}' has an unknown status "
                         f"'{m.get('status')}'")
        # every USER-CUSTODY identity must appear in the migrator table
        # .get, not []: an unclassified identity must be REPORTED by VER-CUST, not
        # crash the checker. A traceback is not a rejection — it is an outage that
        # happens to exit non-zero, and it would mask every finding after it.
        uc = {i["identity"] for i in c["versionedIdentities"]
              if i.get("class") == "USER-CUSTODY"}
        named = " ".join(m["artifact"] for m in mig["members"]).lower()
        for ident in uc:
            key = ident.replace("Schema", "").replace("Recipe", "").lower()
            if key not in named.replace(" ", "").replace("/", "").replace("-", ""):
                if not any(key in m["artifact"].lower().replace(" ", "").replace("-", "")
                           for m in mig["members"]):
                    f.append(f"VER-MIG: USER-CUSTODY identity '{ident}' has no entry in "
                             f"the migrator table")

    # ---- VER-CUST ----
    for i in c["versionedIdentities"]:
        if "class" not in i:
            f.append(f"VER-CUST: identity '{i.get('identity')}' declares no custody class "
                     f"— V1 makes that unshippable")

    # ---- VER-DEP ----
    # Existence is NOT the test. Superseded artifacts stay on disk as the evidence
    # trail, so `d9-exit-contract.v1.4.json` still resolves — and B-SCV2-06 is about
    # citing a SUPERSEDED artifact, not a missing one. Compare against the register's
    # live binding instead.
    reg_p = HERE / "claim-register.v1.json"
    bindings = {}
    if reg_p.exists():
        for cl in json.loads(reg_p.read_text())["claims"]:
            if cl.get("bindingArtifact"):
                bindings[cl["id"]] = cl["bindingArtifact"]
    for d in c["decisionDependencies"]:
        src = d.get("source", "")
        if src.startswith("artifacts/"):
            if not (HERE.parent / src).exists():
                f.append(f"VER-DEP: dependency '{d['id']}' cites {src}, which does not "
                         f"exist")
            live = bindings.get(d["id"])
            if live and src != live:
                f.append(f"VER-DEP: dependency '{d['id']}' cites {src} but the register "
                         f"binds {live} — a superseded citation (B-SCV2-06)")
            if "direction" not in d:
                f.append(f"VER-DEP: dependency '{d['id']}' declares no direction, so "
                         f"ownership may be circular (B-SCV2-06)")

    # ---- VER-EG ----
    sw = c["supportWindows"]
    if "sealRule" not in sw:
        f.append("VER-EG: no seal rule for guessed support windows (A1-VER-05)")
    for k, v in sw.items():
        if isinstance(v, dict) and "evidenceGrade" not in v:
            f.append(f"VER-EG: support window '{k}' declares no evidenceGrade")

    # ---- VER-DIS ----
    # ``implementable`` is feasibility metadata, not proof of execution.
    impl = {t["id"]: t.get("implementable", False) for t in c["conformanceTests"]}
    for prop in c["dischargeStatus"]["properties"]:
        for tid in prop["dischargedBy"]:
            if tid not in impl:
                f.append(f"VER-DIS: '{prop['property']}' names unknown test '{tid}'")
            elif not impl[tid]:
                f.append(f"VER-DIS: '{prop['property']}' is discharged by '{tid}', which "
                         f"is not implementable — a paper seal")
        if prop["status"] == "SPECIFIED" and prop["dischargedBy"] and \
                prop.get("evidenceGrade") != "IMPLEMENTABLE_UNEXECUTED":
            f.append(f"VER-DIS: '{prop['property']}' is SPECIFIED by unexecuted tests "
                     "but does not say IMPLEMENTABLE_UNEXECUTED")
        if prop["status"] in {"DISCHARGED", "DEMONSTRATED"}:
            if not prop["dischargedBy"]:
                f.append(f"VER-DIS: '{prop['property']}' claims {prop['status']} with no tests")
            if prop.get("evidenceGrade") != "DEMONSTRATED" or not \
                    prop.get("demonstrationEvidenceIds"):
                f.append(f"VER-DIS: '{prop['property']}' claims {prop['status']} without "
                         "evidenceGrade DEMONSTRATED and retained demonstrationEvidenceIds "
                         "— implementable:true is not execution evidence")
    for t in c["conformanceTests"]:
        if not t.get("implementable") and not (t.get("requiresHarness")
                                               or t.get("requiresMechanism")):
            f.append(f"VER-DIS: {t['id']} is not implementable and names no blocker")

    # ---- R1-VER-01 pivot cost ship-gate ----
    dsd = c.get("detectorSemanticDelta") or {}
    sg = dsd.get("shipGate") or {}
    if not sg:
        f.append("VER-PIVOT: detectorSemanticDelta.shipGate missing (R1-VER-01) — "
                 "dual-emit affordability must not be a silent assumption")
    else:
        blob = json.dumps(sg).lower()
        if "cost" not in blob and "2" not in blob:
            f.append("VER-PIVOT: shipGate does not address cost")
        if "product" not in blob and "disposition" not in blob and "acceptance" not in blob:
            f.append("VER-PIVOT: shipGate lacks product acceptance / disposition path")
        if not dsd.get("costHonesty") and "unmeasured" not in blob:
            f.append("VER-PIVOT: cost honesty not stated")

    # ---- R1-VER-02 consumer-facing evidenceGrade ----
    sw = c.get("supportWindows") or {}
    if "consumerFacingRule" not in sw:
        f.append("VER-EG: supportWindows.consumerFacingRule missing (R1-VER-02) — "
                 "GUESSED windows must not look like SLAs")
    elif "evidencegrade" not in json.dumps(sw["consumerFacingRule"]).lower():
        f.append("VER-EG: consumerFacingRule does not require displaying evidenceGrade")

    # ---- VER-HIST: EVD-PATCH-04 / R10-EVD-07 ----------------------------
    hp = c.get("historicalSemanticsPolicy")
    if not isinstance(hp, dict):
        f.append("VER-HIST: historicalSemanticsPolicy missing (R10-EVD-07)")
        return f
    if c.get("version") == 4:
        f.extend(_check_historical_v4(c, hp))
        return f
    if set((hp.get("scope") or {}).get("included", [])) != {
            "trusted-bundled-declarative-v1"}:
        f.append("VER-HIST: historical policy is not narrowly limited to trusted bundled "
                 "declarative v1 semantics")
    excluded = set((hp.get("scope") or {}).get("excluded", []))
    if not {"untrusted-imperative", "Probe"}.issubset(excluded):
        f.append("VER-HIST: untrusted imperative semantics or Probe are not excluded")
    support = hp.get("supportPosture") or {}
    if (support.get("fixedSupportWindow") is not False
            or support.get("sla") is not False
            or support.get("costClaim") != "NONE"
            or support.get("consumerLabel") != "PROVISIONAL"):
        f.append("VER-HIST: historical semantics must be artifact-custody based and "
                 "PROVISIONAL, with no fixed window, SLA or cost claim")
    join = hp.get("capabilityJoin") or {}
    if join.get("authority") != "artifacts/retention-tiers.v7.json":
        f.append("VER-HIST: effective capability is not delegated exactly to "
                 "retention-tiers.v7")
    if "may not copy ranks" not in str(join.get("forbidden", "")):
        f.append("VER-HIST: no explicit prohibition on a second capability lattice")
    reasons = hp.get("typedReasons")
    required_reasons = {
        "historical-scope-excluded",
        "historical-semantics-unavailable",
        "historical-verifier-artifact-unavailable",
        "historical-signature-material-unavailable",
        "historical-verifier-abi-unsupported",
        "historical-binding-mismatch",
        "historical-verifier-untrusted",
        "historical-run-identity-mutation",
        "historical-run-identity-rewrite-forbidden",
    }
    if (not isinstance(reasons, list) or len(reasons) != len(set(reasons))
            or not required_reasons.issubset(set(reasons))):
        f.append("VER-HIST: typed historical-unavailability reason vocabulary is not "
                 "closed and complete")

    oracle = hp.get("casOracle")
    seen_cas: dict[str, str] = {}
    if not isinstance(oracle, list) or not oracle:
        f.append("VER-HIST: closed CAS oracle is absent")
        oracle = []
    for i, entry in enumerate(oracle):
        path = f"VER-HIST casOracle[{i}]"
        if not isinstance(entry, dict):
            f.append(f"{path}: expected closed object")
            continue
        if set(entry) != {"ref", "kind", "mediaType", "canonicalBytes"}:
            f.append(f"{path}: fields are not exactly ref/kind/mediaType/canonicalBytes")
            continue
        rid, value = entry.get("ref"), entry.get("canonicalBytes")
        if (not isinstance(rid, str) or not REFPAT.fullmatch(rid)
                or not isinstance(entry.get("kind"), str)
                or not isinstance(entry.get("mediaType"), str)
                or not isinstance(value, str)):
            f.append(f"{path}: malformed CAS entry")
            continue
        if _sha256_ref(value) != rid:
            f.append(f"{path}: reference does not equal SHA-256 of canonical bytes")
        if rid in seen_cas:
            suffix = "different bytes" if seen_cas[rid] != value else "duplicate entry"
            f.append(f"{path}: same CAS id appears twice ({suffix})")
        seen_cas[rid] = value
        if entry["mediaType"] == "application/json":
            try:
                parsed = json.loads(value)
                recoded = json.dumps(parsed, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False)
                if recoded != value:
                    f.append(f"{path}: JSON bytes are not canonical")
            except (TypeError, ValueError, json.JSONDecodeError):
                f.append(f"{path}: application/json bytes do not parse")

    manifests = hp.get("trustedVerifierManifest")
    seen_artifacts: set[str] = set()
    if not isinstance(manifests, list) or not manifests:
        f.append("VER-HIST: trusted verifier manifest is absent")
        manifests = []
    manifest_fields = {"verifierArtifactRef", "signatureRef", "signatureScheme",
                       "signingKeyId", "bundleMode", "irFamilies", "irMajors",
                       "verifierAbi"}
    for i, manifest in enumerate(manifests):
        path = f"VER-HIST trustedVerifierManifest[{i}]"
        if not isinstance(manifest, dict) or set(manifest) != manifest_fields:
            f.append(f"{path}: manifest entry is not closed")
            continue
        aid = _ref_id(manifest.get("verifierArtifactRef"), kind="verifier-artifact")
        sid = _ref_id(manifest.get("signatureRef"), kind="bundle-signature")
        if aid is None or sid is None:
            f.append(f"{path}: artifact/signature refs are malformed or mistyped")
        if aid in seen_artifacts:
            f.append(f"{path}: verifier artifact has more than one trust declaration")
        if aid is not None:
            seen_artifacts.add(aid)
        if aid not in seen_cas or sid not in seen_cas:
            f.append(f"{path}: artifact or signature does not resolve in CAS oracle")
        if (manifest.get("signatureScheme") != "ed25519"
                or manifest.get("bundleMode") != "in-release-offline"):
            f.append(f"{path}: verifier is not signed and bundled for offline use")
        fams, majors = manifest.get("irFamilies"), manifest.get("irMajors")
        if (not isinstance(fams, list) or not fams
                or not all(isinstance(x, str) and x for x in fams)
                or len(fams) != len(set(fams))
                or not isinstance(majors, list) or not majors
                or not all(isinstance(x, int) and not isinstance(x, bool) and x > 0
                           for x in majors)
                or len(majors) != len(set(majors))):
            f.append(f"{path}: IR family/major domains are not exact non-empty sets")

    fixtures = hp.get("crossMajorFixtures")
    if not isinstance(fixtures, list) or not fixtures:
        f.append("VER-HIST: no cross-major historical fixtures")
        fixtures = []
    fixture_ids: set[str] = set()
    for i, fx in enumerate(fixtures):
        if not isinstance(fx, dict):
            f.append(f"VER-HIST fixture[{i}]: expected object")
            continue
        fid = fx.get("id")
        if not isinstance(fid, str) or not fid or fid in fixture_ids:
            f.append(f"VER-HIST fixture[{i}]: missing or duplicate id")
        else:
            fixture_ids.add(fid)
        got = _historical_decision(hp, fx)
        if got != fx.get("expect"):
            f.append(f"VER-HIST {fid or i}: derives {got}, expects {fx.get('expect')}")
    if not any(isinstance(x, dict)
               and x.get("hostDefaultIrMajor") == 2
               and (x.get("binding") or {}).get("irMajor") == 1
               and (x.get("expect") or {}).get("decision") == "VERIFY-HISTORICAL"
               for x in fixtures):
        f.append("VER-HIST: no successful historical v1 verification on a v2 host")
    if not any(isinstance(x, dict)
               and (x.get("expect") or {}).get("reason")
               == "historical-verifier-artifact-unavailable" for x in fixtures):
        f.append("VER-HIST: missing-verifier deterministic refusal is untested")
    if not any(isinstance(x, dict)
               and (x.get("expect") or {}).get("reason")
               == "historical-verifier-abi-unsupported" for x in fixtures):
        f.append("VER-HIST: unsupported-ABI deterministic refusal is untested")

    # Every manifest major has a distinct artifact. This rejects a support-range
    # shortcut that would silently run one interpreter across changed semantics.
    artifacts_by_major: dict[int, set[str]] = {}
    majors_by_artifact: dict[str, set[int]] = {}
    for manifest in manifests:
        if not isinstance(manifest, dict):
            continue
        aid = _ref_id(manifest.get("verifierArtifactRef"), kind="verifier-artifact")
        for major in manifest.get("irMajors", []) if isinstance(manifest.get("irMajors"), list) else []:
            if isinstance(major, int) and not isinstance(major, bool) and aid is not None:
                artifacts_by_major.setdefault(major, set()).add(aid)
                majors_by_artifact.setdefault(aid, set()).add(major)
    if any(len(majors) != 1 for majors in majors_by_artifact.values()):
        f.append("VER-HIST: one verifier artifact is declared across multiple IR majors")
    if len(artifacts_by_major) >= 2:
        reps = [next(iter(v)) for _, v in sorted(artifacts_by_major.items()) if v]
        if len(reps) != len(set(reps)):
            f.append("VER-HIST: an IR major change did not create a new verifier artifact")

    migrations = hp.get("proofMigrationFixtures")
    if not isinstance(migrations, list) or len(migrations) < 2:
        f.append("VER-HIST: proof migration needs both new-Run and rewrite-rejection fixtures")
        migrations = []
    for i, fx in enumerate(migrations):
        got = _migration_decision(fx)
        if not isinstance(fx, dict) or got != fx.get("expect"):
            f.append(f"VER-HIST migration[{i}]: derives {got}, expects "
                     f"{fx.get('expect') if isinstance(fx, dict) else None}")
    if not any(isinstance(x, dict) and x.get("action") == "CREATE-NEW-RUN"
               and (x.get("expect") or {}).get("decision") == "ACCEPT-NEW-RUN"
               for x in migrations):
        f.append("VER-HIST: no accepted append-only proof migration")
    if not any(isinstance(x, dict) and x.get("action") == "REWRITE-EXISTING-RUN"
               and (x.get("expect") or {}).get("decision") == "REJECT-MIGRATION"
               for x in migrations):
        f.append("VER-HIST: old-Run rewrite rejection is untested")

    return f


# --------------------------------------------------------------------------
def _m_blame_code_without_pivot(c):
    for fx in c["comparisonFixtures"]:
        if fx["id"] == "reject-blaming-code-without-pivot":
            fx["valid"] = True

def _m_delta_as_regression(c):
    for fx in c["comparisonFixtures"]:
        if fx["id"] == "reject-detection-delta-as-regression":
            fx["valid"] = True

def _m_drop_indeterminate(c):
    c["detectorSemanticDelta"]["theFix"]["ifPivotUnavailable"] = {"outcome": "CODE-NET-NEW"}

def _m_drop_migrators(c):
    del c["migrators"]

def _m_migrator_without_preview(c):
    c["migrators"]["members"][0]["preview"] = None

def _m_online_migrator(c):
    c["migrators"]["airGap"] = {"rule": "A migrator may download what it needs."}

def _m_stale_d9_citation(c):
    for d in c["decisionDependencies"]:
        if d["id"] == "D9":
            d["source"] = "artifacts/d9-exit-contract.v1.4.json"

def _m_undirected_dependency(c):
    for d in c["decisionDependencies"]:
        if d["id"] == "D9":
            del d["direction"]

def _m_seal_a_guess(c):
    for p in c["dischargeStatus"]["properties"]:
        if p["property"].startswith("support windows"):
            p["dischargedBy"] = ["VT-12"]
            p["status"] = "DISCHARGED"

def _m_implementable_boolean_discharges(c):
    for p in c["dischargeStatus"]["properties"]:
        if p["property"] == "contract evolution is keyed by artifact custody":
            p["status"] = "DISCHARGED"
            p.pop("evidenceGrade", None)

def _m_drop_evidence_grade(c):
    del c["supportWindows"]["fingerprintRecipe"]["evidenceGrade"]

def _m_unclassified_identity(c):
    del c["versionedIdentities"][1]["class"]

def _m_drop_pivot_ship_gate(c):
    (c.get("detectorSemanticDelta") or {}).pop("shipGate", None)
    (c.get("detectorSemanticDelta") or {}).pop("costHonesty", None)

def _m_drop_consumer_facing_eg(c):
    (c.get("supportWindows") or {}).pop("consumerFacingRule", None)

def _m_drop_historical_policy(c):
    del c["historicalSemanticsPolicy"]

def _m_corrupt_historical_cas_bytes(c):
    c["historicalSemanticsPolicy"]["casOracle"][0]["bytes"] += " "

def _m_unsigned_historical_verifier(c):
    c["historicalSemanticsPolicy"]["trustModel"]["signatureScheme"] = "none"

def _m_same_verifier_across_majors(c):
    hp = c["historicalSemanticsPolicy"]
    hp["signedVerifierBindings"][1]["manifestRef"] = copy.deepcopy(
        hp["signedVerifierBindings"][0]["manifestRef"])

def _m_accept_missing_historical_verifier(c):
    fx = next(x for x in c["historicalSemanticsPolicy"]["crossMajorFixtures"]
              if x["id"] == "VER4-HIST-MISSING-PAYLOAD")
    fx["expect"] = {"decision": "VERIFY-HISTORICAL",
                    "capabilityDependencyState": "AVAILABLE",
                    "authoritativeRead": "ALLOW", "reason": None,
                    "runIdentityUnchanged": True,
                    "sealedCapabilityUnchanged": True,
                    "requiredDependencies": fx["expect"]["requiredDependencies"]}

def _m_accept_unsupported_historical_abi(c):
    fx = next(x for x in c["historicalSemanticsPolicy"]["crossMajorFixtures"]
              if x["id"] == "VER4-HIST-UNSUPPORTED-ABI")
    fx["expect"] = {"decision": "VERIFY-HISTORICAL",
                    "capabilityDependencyState": "AVAILABLE",
                    "authoritativeRead": "ALLOW", "reason": None,
                    "runIdentityUnchanged": True,
                    "sealedCapabilityUnchanged": True,
                    "requiredDependencies": fx["expect"]["requiredDependencies"]}

def _m_allow_probe_historical_verification(c):
    fx = next(x for x in c["historicalSemanticsPolicy"]["crossMajorFixtures"]
              if x["id"] == "VER4-HIST-PROBE-EXCLUDED")
    fx["binding"]["scope"] = "trusted-bundled-declarative-v1"

def _m_fixed_historical_support_window(c):
    c["historicalSemanticsPolicy"]["supportPosture"]["fixedSupportWindow"] = 2

def _m_unbind_historical_ir_major(c):
    fx = c["historicalSemanticsPolicy"]["crossMajorFixtures"][0]
    del fx["binding"]["irMajor"]

def _m_rewrite_old_run_accepted(c):
    fx = next(x for x in c["historicalSemanticsPolicy"]["proofMigrationFixtures"]
              if x["id"] == "VER4-MIGRATION-REWRITE-REJECTED")
    fx["expect"] = {"decision": "ACCEPT-NEW-RUN", "reason": None,
                    "sourceRunIdentityUnchanged": False}

def _m_drop_retention_v7_authority(c):
    c["historicalSemanticsPolicy"]["capabilityJoin"]["authority"] = \
        "artifacts/retention-tiers.v6.json"


def _m_enable_historical_tofu(c):
    c["historicalSemanticsPolicy"]["trustModel"]["tofu"] = True


def _m_enable_historical_network_lookup(c):
    c["historicalSemanticsPolicy"]["trustModel"]["networkLookup"] = True


def _m_drop_manifest_platform_payload(c):
    hp = c["historicalSemanticsPolicy"]
    entry = next(x for x in hp["casOracle"] if x.get("kind") == "verifier-manifest")
    manifest = json.loads(entry["bytes"])
    manifest["payloads"].pop()
    entry["bytes"] = _canonical_json(manifest)


def _m_accept_invalid_custody_control(c):
    control = next(x for x in c["historicalSemanticsPolicy"]["custodyControls"]
                   if x["mutation"] == "semantics-verifier-ref-substitution")
    control["expectedDecision"] = "VERIFY-HISTORICAL"
    control["expectedReason"] = None


def _m_drop_public_key_bytes(c):
    hp = c["historicalSemanticsPolicy"]
    hp["casOracle"] = [x for x in hp["casOracle"]
                       if x.get("kind") != "verifier-public-key"]


def _m_accept_descriptor_only(c):
    control = next(x for x in c["historicalSemanticsPolicy"]["custodyControls"]
                   if x["mutation"] == "descriptor-without-payload")
    control["expectedDecision"] = "VERIFY-HISTORICAL"
    control["expectedReason"] = None


def _m_accept_invalid_ed25519_vector(c):
    vector = next(x for x in c["historicalSemanticsPolicy"]
                  ["cryptographicVerification"]["testVectors"]
                  if x["expect"] is False)
    vector["expect"] = True


def _m_drop_future_evidence_rejoin(c):
    c["historicalSemanticsPolicy"]["capabilityJoin"]["futureRejoin"] = "NONE"


def _m_drop_one_minimum_dependency(c):
    fx = next(x for x in c["historicalSemanticsPolicy"]["crossMajorFixtures"]
              if x["expect"]["decision"] == "VERIFY-HISTORICAL")
    fx["expect"]["requiredDependencies"].pop()


def _m_accept_sealed_capability_mutation(c):
    fx = next(x for x in c["historicalSemanticsPolicy"]["crossMajorFixtures"]
              if x["id"] == "VER4-HIST-SEALED-CAPABILITY-MUTATION")
    fx["expect"].update(decision="VERIFY-HISTORICAL",
                        capabilityDependencyState="AVAILABLE",
                        authoritativeRead="ALLOW", reason=None)


def _m_open_historical_fixture_schema(c):
    c["historicalSemanticsPolicy"]["crossMajorFixtures"][0][
        "adjacentVerifierOverride"] = "forbidden"


MUTATIONS = [
    ("attribute a delta to code with no pivot (B-CSG-04)", _m_blame_code_without_pivot),
    ("report a detection delta as a regression (B-CSG-04)", _m_delta_as_regression),
    ("drop the INDETERMINATE fallback (VER-CMP)", _m_drop_indeterminate),
    ("remove every migrator, making V2 vacuous (A1-VER-01)", _m_drop_migrators),
    ("specify a migrator with no preview surface (VER-MIG)", _m_migrator_without_preview),
    ("let a migrator fetch from the network (A1-VER-02)", _m_online_migrator),
    ("cite the superseded D9 v1.4 (B-SCV2-06)", _m_stale_d9_citation),
    ("drop the dependency direction (B-SCV2-06)", _m_undirected_dependency),
    ("discharge support windows with an unbuilt test (A1-VER-05)", _m_seal_a_guess),
    ("treat implementable:true as retained discharge evidence (R2-FINAL-02)",
     _m_implementable_boolean_discharges),
    ("drop an evidence grade (A1-VER-05)", _m_drop_evidence_grade),
    ("leave a versioned identity unclassified (V1 / VER-CUST)", _m_unclassified_identity),
    ("drop pivot cost ship-gate (R1-VER-01)", _m_drop_pivot_ship_gate),
    ("drop consumer-facing evidenceGrade rule (R1-VER-02)", _m_drop_consumer_facing_eg),
    ("drop historical semantics policy (R10-EVD-07)", _m_drop_historical_policy),
    ("break CAS digest-to-bytes binding", _m_corrupt_historical_cas_bytes),
    ("trust an unsigned historical verifier declaration", _m_unsigned_historical_verifier),
    ("reuse one signed verifier binding across IR majors", _m_same_verifier_across_majors),
    ("accept a missing historical native payload", _m_accept_missing_historical_verifier),
    ("accept an unsupported historical verifier ABI", _m_accept_unsupported_historical_abi),
    ("admit Probe to historical verification", _m_allow_probe_historical_verification),
    ("promise a fixed historical support window", _m_fixed_historical_support_window),
    ("unbind exact historical IR major", _m_unbind_historical_ir_major),
    ("rewrite an old Run during proof migration", _m_rewrite_old_run_accepted),
    ("replace retention v7 as capability authority", _m_drop_retention_v7_authority),
    ("enable TOFU for historical trust", _m_enable_historical_tofu),
    ("enable network lookup for historical trust", _m_enable_historical_network_lookup),
    ("drop one DELIVERY platform from a signed native manifest",
     _m_drop_manifest_platform_payload),
    ("accept semantics verifier-ref substitution", _m_accept_invalid_custody_control),
    ("drop retained raw public-key bytes", _m_drop_public_key_bytes),
    ("accept a descriptor in place of native executable bytes", _m_accept_descriptor_only),
    ("accept a bit-flipped Ed25519 signature vector", _m_accept_invalid_ed25519_vector),
    ("drop the frozen Evidence v3 future rejoin boundary", _m_drop_future_evidence_rejoin),
    ("reduce the six-object minimum verifiable closure", _m_drop_one_minimum_dependency),
    ("accept mutation of a sealed capability", _m_accept_sealed_capability_mutation),
    ("admit adjacent verifier metadata to a historical fixture",
     _m_open_historical_fixture_schema),
]


def selftest(base) -> int:
    pre = check(base)
    if pre:
        print(f"REFUSING to self-test: the base contract has {len(pre)} finding(s), so "
              f"every mutation would be masked by them.")
        for x in pre[:5]:
            print("  -", x)
        return 1
    print("mutation self-test — each row must be REJECTED\n")
    escaped = 0
    for name, mut in MUTATIONS:
        c = copy.deepcopy(base)
        before = json.dumps(c, sort_keys=True, separators=(",", ":"))
        try:
            mut(c)
        except Exception as exc:
            print(f"  {'ERROR':>6}  {name}\n          mutation failed to apply: {exc}")
            escaped += 1
            continue
        after = json.dumps(c, sort_keys=True, separators=(",", ":"))
        if before == after:
            print(f"  {'ERROR':>6}  {name}\n          mutation applied no change")
            escaped += 1
            continue
        findings = check(c)
        if not findings:
            escaped += 1
        print(f"  {'reject' if findings else 'ESCAPE':>6}  {name}")
        print(f"          {findings[0] if findings else 'NO FINDING — mutation survived'}")
    print()
    if escaped:
        print(f"{escaped}/{len(MUTATIONS)} mutations ESCAPED — the proof path is optional")
        return 1
    print(f"all {len(MUTATIONS)} mutations rejected — the proof path is load-bearing")
    return 0


def main() -> int:
    args = [a for a in sys.argv[1:] if a != "--selftest"]
    p = pathlib.Path(args[0]) if args else HERE / BINDING
    if not p.exists():
        print(f"missing contract: {p}", file=sys.stderr)
        return 2
    c = json.loads(p.read_text())
    if "--selftest" in sys.argv:
        return selftest(c)
    f = check(c)
    if not f:
        impl = sum(1 for t in c["conformanceTests"] if t.get("implementable"))
        historical = c["historicalSemanticsPolicy"]
        print(f"versioning OK — {p.name}, {len(c['comparisonFixtures'])} comparison "
              f"fixtures, {len(historical['crossMajorFixtures'])} historical fixtures, "
              "VER-CMP / VER-MIG / VER-DEP / VER-EG / VER-DIS / VER-CUST / "
              "VER-HIST clean")
        print(f"  {impl}/{len(c['conformanceTests'])} conformance tests implementable; "
              f"support windows are GUESSED and that property is NOT DISCHARGED")
        return 0
    print(f"{len(f)} finding(s) in {p.name}:")
    for x in f:
        print("  -", x)
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
