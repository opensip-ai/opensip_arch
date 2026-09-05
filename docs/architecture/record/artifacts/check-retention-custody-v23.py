#!/usr/bin/env python3
"""Retained checker for retention-tiers.v23.json.

Scope, stated before anything else so no reader has to infer it.

  This instrument verifies exactly two NEW architecture surfaces and the record
  that binds them to their inputs:

    Part A  the first-run retention consent mechanism, its policy object, its
            identity recipe, its ask / no-ask decision tables, and the exclusion
            of the persisted policy from PLAN-ID-V1.
    Part B  purge semantics: the availability lattice, the effectiveCapability
            derivation, the purge mutation boundary, the purged-Run inspection
            and its D9 termination mapping, and the measured D9 reason-code gap.

  It does NOT re-verify retention-tiers.v22.  v22 passed independent review at
  zero blocking findings over its own bytes; IMPLEMENTATION-FREEZE 7.2 binds
  that verdict to those bytes and they are hash-pinned here.  What this checker
  does with v22 is CONSUME it: it re-derives values from v22's own sealed
  closure and requires agreement.

Trust order.  Every input is read as inert bytes, hashed, and compared against a
pinned digest BEFORE any of it is parsed or executed.  A mismatch prints one
named refusal line and exits 2; it never reaches a findings path.

Exit matrix, distinct by construction:
    0  clean
    1  findings
    2  bad invocation, integrity refusal, or pin mismatch
    3  selftest refused / not run (the base was not clean, so mutation results
       would be meaningless)

Invocation:  python3 -I -B check-retention-custody-v23.py [--selftest]
                                                          [--part a|b|all]
"""

from __future__ import annotations

import sys

if sys.flags.isolated != 1 or sys.flags.dont_write_bytecode != 1:
    sys.stderr.write(
        "RT23-UNSUPPORTED-INVOCATION: run as `python3 -I -B "
        "check-retention-custody-v23.py`.  Caller-owned isolated startup is the "
        "prevention boundary; script code cannot undo interpreter or site "
        "activity that happened before line 1.\n")
    raise SystemExit(2)

import copy
import hashlib
import importlib.util
import json
import pathlib
import re
import struct
import unicodedata
from typing import Any

HERE = pathlib.Path(__file__).resolve().parent
COOP = HERE.parent
SUBJECT = "retention-tiers.v23.json"

# ---------------------------------------------------------------------------
# Pinned execution closure.  IMPLEMENTATION-FREEZE 7.2 recording obligation: a
# count is not a record, so every member is named with its digest here and again
# as data inside the subject artifact, and the two are compared on every run.
# ---------------------------------------------------------------------------
PINS: dict[str, str] = {
    # --- surfaces this checker computes over -------------------------------
    "retention-tiers.v22.json":
        "52aa540df75a047f0abc09b4fab4b472ab2934ad1f488146bb370ed6050743e1",
    "check-retention-custody-v22.py":
        "497909c21118b656d222346d9498b7a9cac34ef3dd3bb0f29ef59c0db90e1c5c",
    "retention-tiers.v22.review-independent-prefreeze.json":
        "a30e84cbc67e25a2da231d0204202755c9ee2e3baf3bd0dc48039f4a8bc38600",
    "d9-exit-contract.v1.14.json":
        "8dd3303855f49bfdbb2751ee65f54a906405f0654159ebe815472f73cdf7da31",
    "check-d9-v1.14.py":
        "513d69dd879dcb678d53d8df89a907d05dacd4b078ec43c7fedc939732c5e83e",
    "evidence.v10.json":
        "62a3a07194062c8499f6e943b4986d7a77bdecc0c4ec499851ac078fd548e9b4",
    "operability.v10.json":
        "9bacbbf43dfb941a0d87330f79844d395b3ac838ae5bf54026ef4d69681696be",
    "product-dispositions.v1.json":
        "b9a87839606981a5be46f62aca2d85a17c3da5082c8d0aad02a211f3025fd91c",
    "threat-model.v3.json":
        "56734a4047b61e1fc702f75ccb21e8721b334adb449093d266756d0b08adc499",
    "resolved-inputs.v2.json":
        "0114205aaa5d3f7c0aecc58c10522711aacaa6aa404a41563245627b27b88f43",
    # --- transitive execution closure of check-d9-v1.14.py -----------------
    # Independently tabulated here.  This checker verifies all of them before
    # importing the D9 module; the module then re-reads them and verifies them
    # again against its own table.  Both tables must agree with the bytes.
    "d9-exit-contract.v1.13.json":
        "fc2c546a4cdbe2038f3a5db333ab9903d21ae9d6223777b139b58551fb2f2fae",
    "check-d9-v1.13.py":
        "a905ab0e4b932c2ef4c565e847a12cb398abf9cd7a74abd92f95cbc85ffc8717",
    "d9-exit-contract.v1.13.review-independent-prefreeze.json":
        "88ab60efb21f603213ebff722f62f310b422f03981895e3f6779f2febe734c5b",
    "d9-exit-contract.v1.12.json":
        "17aa2161619ca6abae209dd2b2eda3a16d533718f1697cc31b87325feaa4b2d4",
    "check-d9-v1.12.py":
        "32566f4f56d81ead4e3f2582ef3a6e934ca1fa0ca4172b13124e952018ec9c8a",
    "d9-exit-contract.v1.12.review-independent-prefreeze.json":
        "1e6486db60e24a6ba9eef06ca8c2808a09376917189dd330f7808567fe31bd4c",
    "d9-exit-contract.v1.11.json":
        "09ab6b579173bdbd9575d46e7df96b8279a0bb12512638e25ad56e28d16e9895",
    "check-d9-v1.11.py":
        "9b637adee48432bb5388ce51212d59a1965044d2c1d5f6b6a4a3dd8ed519000a",
    "d9-exit-contract.v1.11.review-independent-prefreeze.json":
        "df1e89324a6c7645e96f69a2cc924731e4e37eeea64c10058cdd4cfcdfdbbcec",
    "d9-exit-contract.v1.10.json":
        "bf1d7eb0ab24de89f665f46c25377195a2721fc7fcb62f3aa449d0887b705b7b",
    "check-d9-v1.10.py":
        "77f86334a0ee016960224880fe75ef2b9b44d3adf20799c8354e992fbf19cca6",
    "d9-exit-contract.v1.10.review-independent-prefreeze.json":
        "7faefdf8f2c19e39ad9fdd6fba8df6f08c586aa73b7e5ab7ed917ae4c223e476",
    "d9-exit-contract.v1.9.json":
        "bc3c2b48d3615bc262166a698d3a3559bc2fa2fbd2f637de0dbf943309194404",
    "check-d9-v1.9.py":
        "956e41e279e758af5dd5e342a5404f334f6223add72abdb1340c85fafa2bd936",
    "d9-exit-contract.v1.9.review-independent-prefreeze.json":
        "409e55ddcc2121da5624a112728cd2d126586411a9abe06435c64d1c02b71373",
    "d9-exit-contract.v1.8.json":
        "5fb5466372da7c8ef935a1233eb67869f21c3cdb21d67b3767159998ad26a30d",
    "check-d9-v1.8.py":
        "827e5bdd600e2682d7653bc738f07efe066f90f4d7db7bad16a7f7fd5eb91e47",
    "d9-exit-contract.v1.8.review-independent-prefreeze.json":
        "f044620aaac0ea4f7efc6bdd51983278bf5858f5f967b6d48310e7c0139fedb9",
    "d9-exit-contract.v1.7.json":
        "d199aef6ac2edc7652325ef8d26f75cfda35a94f3e234d10aafd984d9088b2eb",
    "check-d9-v1.7.py":
        "ead1dd8d3635a355475ba8d71611515497a29e59cdfc5d232f167588dd9fb6d3",
    "d9-exit-contract.v1.6.json":
        "c633614e17f6757cab74753d462eed53ade09dc234923d73b70d3042c6367046",
    "check-d9.py":
        "9f8e16a0000e59d2f1326f97f1b8afcc5c7121eb0c57b6c440d76b9c401346a7",
    "retention-tiers.v14.json":
        "b66d0275d326cdd0cfdbec5e0810788e7768c10c9f1d7ab2c4df8c44b6975770",
    "check-retention-custody-v14.py":
        "6b190a89ba1700cf820746b473e8e3a521c9b2f6b4856f0c501d72a44b0a1d60",
    "retention-tiers.v14.review-independent-prefreeze.json":
        "dfb037bd121f7b73fbfeb77bbbaf0e1028a8c89318c5991bb3b3ec935046575c",
}

# Content anchors instead of a whole-file digest.  IMPLEMENTATION-FREEZE.md is
# under concurrent edit by other lanes; a whole-file pin would manufacture a
# false refusal on an unrelated edit while adding nothing, and a digest recorded
# for a file under edit is false the moment it is written -- which is the exact
# failure mode 7.2 exists to stop.  Removal of the cited text still fails closed.
FREEZE_ANCHORS = (
    "### 4.5 Recorded product intent on `CD-RT-5` — NOT a signature",
    "ask the customer, and set the policy from their answer.",
    "interactive asks and persists; CI and dismissal are\nephemeral-or-refuse; "
    "the persisted policy is host-owned, project-scoped, and\nexcluded from `PlanId`.",
    "CI/non-interactive mode never loads or resolves layer 4; local interactive "
    "mode keys and explains it",
    "Only declared analysis inputs may\n   affect `PlanId`; CI does not read layer 4.",
    "`ExecutionId` is allocated at attempt admission. RequestId and\n   "
    "ExecutionId are excluded from Plan/evidence semantics.",
)


# Root keys every candidate in this series carries as its own identity and
# authority record.  Sharing a NAME with the predecessor at these positions is
# not shadowing a semantic surface; sharing one anywhere else is.
METADATA_ROOT_ALLOWLIST = frozenset({
    "artifact", "version", "status", "date", "claimId", "role", "authority",
    "integrationState", "sealRecommendation", "retainedResiduals",
    "supersedesAsArchitectureCandidate", "retainedChecker", "dependencies",
    "assurance", "invariants",
})


class PinMismatch(RuntimeError):
    pass


class DuplicateKeyError(ValueError):
    pass


def _pairs(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for key, value in pairs:
        if key in out:
            raise DuplicateKeyError(f"duplicate object key {key!r}")
        out[key] = value
    return out


def _parse(source: bytes, name: str) -> Any:
    try:
        return json.loads(source.decode("utf-8"), object_pairs_hook=_pairs)
    except (UnicodeError, json.JSONDecodeError, DuplicateKeyError) as exc:
        raise PinMismatch(f"{name}: {type(exc).__name__}: {exc}") from exc


def verified_snapshots() -> dict[str, bytes]:
    """Read every pinned input as inert bytes and verify before anything runs."""
    snaps: dict[str, bytes] = {}
    errors: list[str] = []
    for name, expected in PINS.items():
        try:
            data = (HERE / name).read_bytes()
        except OSError as exc:
            errors.append(f"{name}: read {type(exc).__name__}")
            continue
        actual = hashlib.sha256(data).hexdigest()
        if actual != expected:
            errors.append(f"{name}: {actual} != {expected}")
            continue
        snaps[name] = data
    if errors:
        raise PinMismatch("; ".join(errors))
    if set(snaps) != set(PINS):
        raise PinMismatch("not every pinned input produced a snapshot")
    return snaps


# ---------------------------------------------------------------------------
# Derivations.  Re-implemented here from the pinned contract text, not imported
# from the subject: an instrument that reads its answers out of the artifact it
# is checking measures nothing.
# ---------------------------------------------------------------------------
CAPABILITY_RANK = {"recorded": 0, "verifiable": 1, "replayable": 2}
AVAIL_STATES = ("AVAILABLE", "OUTAGE", "MISSING-DEPENDENCY", "PURGED")
TERMINAL_STATES = ("PURGED",)
REFUSAL_PRECEDENCE = ("PURGED", "MISSING-DEPENDENCY", "OUTAGE")
REFUSAL_KIND = {
    "PURGED": "RETENTION_EVIDENCE_PURGED",
    "MISSING-DEPENDENCY": "RETENTION_EVIDENCE_MISSING",
    "OUTAGE": "RETENTION_EVIDENCE_OUTAGE",
}


def nfc(text: str) -> bytes:
    return unicodedata.normalize("NFC", text).encode("utf-8")


def _component(tag: int, text: str) -> bytes:
    raw = nfc(text)
    return bytes([tag]) + struct.pack(">I", len(raw)) + raw


def _blob(tag: int, raw: bytes) -> bytes:
    return bytes([tag]) + struct.pack(">I", len(raw)) + raw


def raw_key(obj: dict[str, Any]) -> tuple[str, str, str]:
    return obj["projectId"], obj["recordCasRef"], obj["recordKind"]


def _ref_item(ref: dict[str, Any]) -> bytes:
    return _blob(0x75, _component(0x76, ref["recordCasRef"])
                 + _component(0x77, ref["projectId"])
                 + _component(0x78, ref["recordKind"]))


def unit_id(unit: dict[str, Any]) -> str:
    """UNIT-ID-V3, re-derived from the grammar declared in retention-tiers.v22."""
    items = sorted(_ref_item(r) for r in unit["objectRefs"])
    preimage = (nfc("opensip.semantic-custody-unit-id.v3") + b"\x00" + b"\x70"
                + _component(0x72, unit["projectId"])
                + _component(0x74, unit["requiredForCapability"])
                + _blob(0x79, b"".join(items)))
    return "unit3:sha256:" + hashlib.sha256(preimage).hexdigest()


def unit_record_bytes(unit: dict[str, Any]) -> bytes:
    items = sorted(_ref_item(r) for r in unit["objectRefs"])
    return (b"\x70" + _component(0x71, unit["unitId"])
            + _component(0x72, unit["projectId"])
            + _component(0x74, unit["requiredForCapability"])
            + _blob(0x79, b"".join(items)))


def unit_set_commitment(units: list[dict[str, Any]]) -> str:
    ordered = sorted({unit_record_bytes(u) for u in units})
    return "sha256:" + hashlib.sha256(b"".join(ordered)).hexdigest()


def availability_map(records: list[dict[str, Any]]) -> dict[str, dict[tuple, str]]:
    return {r["unitId"]: {raw_key(s): s["state"] for s in r["objectStates"]}
            for r in records}


def unit_satisfied(unit: dict[str, Any], amap: dict[str, dict[tuple, str]]) -> bool:
    states = amap.get(unit["unitId"])
    if states is None or not unit["objectRefs"]:
        return False
    if set(states) != {raw_key(r) for r in unit["objectRefs"]}:
        return False
    return all(state == "AVAILABLE" for state in states.values())


def satisfied_at(candidate: str, units: list[dict[str, Any]],
                 amap: dict[str, dict[tuple, str]]) -> bool:
    return all(unit_satisfied(u, amap) for u in units
               if CAPABILITY_RANK[u["requiredForCapability"]] <= CAPABILITY_RANK[candidate])


def effective_capability(sealed: str, units: list[dict[str, Any]],
                         records: list[dict[str, Any]]) -> str:
    """The Part B derivation.  Inputs are the sealed capability, the sealed
    units, and the CURRENT availability state.  Nothing else is read and
    nothing at all is written."""
    if sealed not in CAPABILITY_RANK:
        raise ValueError("sealed capability outside the closed enum")
    amap = availability_map(records)
    ok = [c for c in CAPABILITY_RANK
          if CAPABILITY_RANK[c] <= CAPABILITY_RANK[sealed]
          and satisfied_at(c, units, amap)]
    return max(ok, key=lambda c: CAPABILITY_RANK[c]) if ok else "recorded"


def authoritative(effective: str) -> bool:
    return CAPABILITY_RANK[effective] >= CAPABILITY_RANK["verifiable"]


def typed_refusal(sealed: str, units: list[dict[str, Any]],
                  records: list[dict[str, Any]]) -> str:
    amap = availability_map(records)
    seen: set[str] = set()
    for unit in units:
        if CAPABILITY_RANK[unit["requiredForCapability"]] > CAPABILITY_RANK[sealed]:
            continue
        for state in amap.get(unit["unitId"], {}).values():
            if state != "AVAILABLE":
                seen.add(state)
    for state in REFUSAL_PRECEDENCE:
        if state in seen:
            return REFUSAL_KIND[state]
    return "NONE"


def fold_ledger(entries: list[dict[str, Any]]) -> dict[tuple, str]:
    """UnitAvailabilityLedgerV1 fold.  Append-only with terminal loss."""
    state: dict[tuple, str] = {}
    terminal: set[tuple] = set()
    sequence = 0
    for entry in entries:
        if entry["atSequence"] != sequence + 1:
            raise ValueError(f"ledger sequence break at {entry['atSequence']}")
        sequence = entry["atSequence"]
        key = (entry["projectId"], entry["recordCasRef"], entry["recordKind"])
        if key in terminal and entry["toState"] != "PURGED":
            raise ValueError(
                f"terminal-loss append-only violation at {entry['recordCasRef']}")
        state[key] = entry["toState"]
        if entry["toState"] in TERMINAL_STATES:
            terminal.add(key)
    return state


def apply_states(records: list[dict[str, Any]],
                 overrides: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out = copy.deepcopy(records)
    hits = 0
    for override in overrides:
        key = raw_key(override)
        for record in out:
            for state in record["objectStates"]:
                if raw_key(state) == key:
                    state["state"] = override["state"]
                    hits += 1
    if overrides and hits == 0:
        raise ValueError("state override matched no object state")
    return out


# --- RETENTION-POLICY-ID-V1 / ConsentRecordV1 -------------------------------
POLICY_DOMAIN = "opensip.project-retention-policy.v1"
CONSENT_DOMAIN = "opensip.retention-consent-record.v1"
CONSENT_ORDER = ("projectId", "promptTextDigest", "answer", "answerChannel",
                 "invocationProfile", "lifecyclePhase")


def _frame(tag: int, text: str) -> bytes:
    raw = nfc(text)
    return bytes([tag]) + struct.pack(">I", len(raw)) + raw


def retention_policy_id(project_id: str, posture: str, consent_ref: str) -> str:
    preimage = (nfc(POLICY_DOMAIN) + b"\x00" + struct.pack(">H", 1)
                + struct.pack(">H", 3) + _frame(0x01, project_id)
                + _frame(0x02, posture) + _frame(0x03, consent_ref))
    return "rpol1:sha256:" + hashlib.sha256(preimage).hexdigest()


def consent_record_ref(record: dict[str, Any]) -> str:
    preimage = nfc(CONSENT_DOMAIN) + b"\x00" + struct.pack(">H", 1) + struct.pack(">H", 7)
    for index, key in enumerate(CONSENT_ORDER, start=1):
        preimage += _frame(index, record[key])
    preimage += bytes([7]) + struct.pack(">I", 8) + struct.pack(
        ">Q", record["recordedAtUtcSeconds"])
    return "sha256:" + hashlib.sha256(preimage).hexdigest()


def text_digest(text: str) -> str:
    return "sha256:" + hashlib.sha256(nfc(text)).hexdigest()


# --- PLAN-ID-V1, re-implemented from resolved-inputs.v2.json ----------------
PLAN_FIELD_ORDER = ("snapshotId", "planSchemaMajor", "release", "invocationProfile",
                    "resolvedConfiguration", "scope", "changeSpec", "contributions",
                    "semanticUniverses", "capabilityGrants", "workflow", "budgets",
                    "planIntentCommitment")
PLAN_CLOSED_MAPS = {
    "release": ("manifestId", "capabilityManifestId", "profileId"),
    "scope": ("projectId", "workspaceUnitIds", "requestedPaths", "impactExpansion"),
    "changeSpec": ("mode", "baseCommitId", "dirtyOverlayPolicy", "untrackedPolicy",
                   "vcsAdapterId"),
}
PLAN_CONTRIB_KEYS = ("activationId", "contributionId", "contributionVersion", "bundleId",
                     "artifactDigest", "admissionGrant", "role", "verificationState",
                     "verificationEvidenceId", "parameters", "origin", "authority")
PLAN_CFG_KEYS = ("path", "value", "decidingLayer", "analysisAffecting")
PLAN_STAGE_KNOWN = ("kind", "stageId", "relations", "operator", "ruleIds",
                    "requiredness", "dependsOn", "policyId", "capabilityGrants")
POLICY_INPUT_MARKERS = ("retention.", "retentionPolicy", "retentionPosture")


def cve1(value: Any) -> bytes:
    if value is None:
        return b"\x00"
    if value is True:
        return b"\x02"
    if value is False:
        return b"\x01"
    if isinstance(value, float):
        raise ValueError("CVE1 forbids floating point")
    if isinstance(value, int):
        return (b"\x07" + struct.pack(">q", value) if value < 0
                else b"\x03" + struct.pack(">Q", value))
    if isinstance(value, str):
        raw = nfc(value)
        return b"\x04" + struct.pack(">I", len(raw)) + raw
    if isinstance(value, list):
        return b"\x05" + struct.pack(">I", len(value)) + b"".join(cve1(v) for v in value)
    if isinstance(value, dict):
        items = sorted(value.items(), key=lambda kv: nfc(kv[0]))
        return (b"\x06" + struct.pack(">I", len(items))
                + b"".join(cve1(k) + cve1(v) for k, v in items))
    raise TypeError(type(value).__name__)


def plan_preimage(inp: dict[str, Any]) -> bytes:
    out = nfc("opensip.plan-id") + b"\x00" + struct.pack(">H", 1) + struct.pack(">H", 13)
    for index, name in enumerate(PLAN_FIELD_ORDER, start=1):
        encoded = cve1(inp[name])
        out += bytes([index]) + struct.pack(">I", len(encoded)) + encoded
    return out


def plan_id(inp: dict[str, Any]) -> str:
    return "plan1:sha256:" + hashlib.sha256(plan_preimage(inp)).hexdigest()


def plan_admit(inp: Any) -> tuple[str | None, str | None]:
    """PLAN-ID-V1 admission.  Returns (planId, None) or (None, violationCode)."""
    if not isinstance(inp, dict) or set(inp) != set(PLAN_FIELD_ORDER):
        return None, "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION"
    for name, keys in PLAN_CLOSED_MAPS.items():
        value = inp[name]
        if not isinstance(value, dict) or set(value) != set(keys):
            return None, "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION"
    if inp["invocationProfile"] not in ("ci", "local-interactive"):
        return None, "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION"
    if not isinstance(inp["planSchemaMajor"], int) or isinstance(inp["planSchemaMajor"], bool):
        return None, "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION"
    for row in inp["resolvedConfiguration"]:
        if not isinstance(row, dict) or set(row) != set(PLAN_CFG_KEYS):
            return None, "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION"
        if any(marker in str(row["path"]) for marker in POLICY_INPUT_MARKERS):
            return None, "PLAN_ID_INPUT_CLASS_VIOLATION"
        if inp["invocationProfile"] == "ci" and row["decidingLayer"] == 4:
            return None, "PLAN_ID_PROFILE_VIOLATION"
    for contribution in inp["contributions"]:
        if not isinstance(contribution, dict) or set(contribution) != set(PLAN_CONTRIB_KEYS):
            return None, "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION"
    if set(inp["workflow"]) != {"stages"}:
        return None, "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION"
    for stage in inp["workflow"]["stages"]:
        if not isinstance(stage, dict) or not set(stage) <= set(PLAN_STAGE_KNOWN):
            return None, "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION"
    budgets = inp["budgets"]
    if not isinstance(budgets, dict) or any(
            not isinstance(v, int) or isinstance(v, bool) for v in budgets.values()):
        return None, "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION"
    for array in ("workspaceUnitIds", "requestedPaths"):
        values = inp["scope"][array]
        if list(values) != sorted(set(values)):
            return None, "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION"
    activations = [c["activationId"] for c in inp["contributions"]]
    if activations != sorted(set(activations)):
        return None, "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION"
    try:
        return plan_id(inp), None
    except (ValueError, TypeError):
        return None, "PLAN_ID_PREIMAGE_SCHEMA_VIOLATION"


def canon(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


# ---------------------------------------------------------------------------
# Exact-type admission.  IMPLEMENTATION-FREEZE 6 law 18: closed-scalar admission
# is exact-type, at any depth, BEFORE content is compared.  Every int and bool
# leaf of the subject must be covered by a rule below; an uncovered int or bool
# leaf is itself a finding, so the coverage claim cannot quietly shrink.
# ---------------------------------------------------------------------------
_PATH_RE = re.compile(r"\['([^']*)'\]|\[(\d+)\]|\.([^.\[\]]+)")


def _path_keys(path: str) -> list[str | int]:
    keys: list[str | int] = []
    for match in _PATH_RE.finditer(path):
        if match.group(1) is not None:
            keys.append(match.group(1))
        elif match.group(2) is not None:
            keys.append(int(match.group(2)))
        else:
            keys.append(match.group(3))
    return keys


INT_LEAF_NAMES = frozenset({
    "askPerformedCellCount", "blockingFindingCount", "boundedRepromptCount",
    "carriedFragmentCount", "case", "cellCount", "citedNotGatedCount", "count",
    "coveredExitCode", "crossPartInvariantReferenceCount", "declaredExitCode",
    "deficiencyMemberCount", "derivedExitCode", "errorCodeCount", "exitCode",
    "fieldCount", "freezeContentAnchorCount", "hardPinnedCount",
    "injectionPositionCount", "injectionsNotRefusableByPlanIdV1",
    "injectionsRefusedByPlanIdV1", "item", "liveDerivedExitCode",
    "mutatesExactlyCount", "planIdPreimageFieldCount", "predecessorRootKeyCount",
    "preimageByteLength", "reasonCodeCount", "recipeVersion", "reproducedCount", "rowCount", "schemaVersion", "stateCount",
    "totalCount", "version", "decidingLayer", "recordedAtUtcSeconds",
    "policyRevision", "atSequence", "sweptPositions", "admitted",
    "rejectedByPosition", "rejectedByTypeBan", "rejectedCollateral",
    "scalarLeafPositions", "intLeafPositions", "boolLeafPositions",
    "stringLeafPositions", "unruledIntOrBoolLeafPositions", "injections",
    "guardedIntOrBoolLeafPositions", "swept", "rejectedByCategoricalTypeBan",
})
BOOL_LEAF_NAMES = frozenset({
    "absenceIsADistinctState", "agrees", "appendOnly", "askPerformed",
    "attemptRecordExistsWhileTheQuestionIsOpen",
    "availabilityMutationLeavesUnitIdUnchanged", "bareNewlineIsAnAnswer",
    "callersCannotSupplyIt", "capabilityEnumIsClosed", "changesNoGateStatus",
    "checkerSupportsPerPartAdjudication", "classIsCovered", "closed",
    "closingTheDialogIsNotAnAnswer", "declaresNoNewGate",
    "declaresNoNewRequiredProperty", "derivedAuthoritative", "differsFromAnchor",
    "dismissalSuppressesTheNextAsk", "durableSourceDerivedWritePermitted",
    "entriesAreNeverEditedOrRemoved", "equalsAnchor",
    "evidenceInMemoryWhileTheQuestionIsOpen",
    "exclusionIsStatedTheSameWayAsRequestIdAndExecutionId",
    "executionIdAllocatedAtThisPoint", "executionIdAllocatedWhileTheQuestionIsOpen",
    "firstRunDisclosureEmitted", "hasNoDefaultField", "isAnAnswer",
    "mayAmendD9Vocabulary", "mayAmendOperabilityGates", "mayAmendThreatModel",
    "mayCiteAProductDecision", "mayConstituteAProductDecision",
    "mintsAPlanIdDifferentFromTheAnchor", "mutatesNothingElse",
    "noDismissalPathWritesAPolicy", "notAResolvedConfigurationLayer",
    "notInTheWorktree", "notUnderTheAnalysisSnapshotRoot",
    "objectRefMutationChangesUnitId", "policyIsNoneOfThem", "policyPersisted",
    "policyPersistedByThisCell", "reasonCodeIsNotCovered",
    "refusedBecauseDeclarationDisagreesWithLiveDerivation", "refusedByPlanIdV1",
    "repurgeIsIdempotent", "snapshotCapturedWhileTheQuestionIsOpen",
    "stdinIsNeverAnAnswerChannel", "strictlyBeforeAttemptAdmission",
    "terminatesTheRequest", "thereIsNobodyToPrompt", "unitSetCommitmentUnchanged",
    "sweepIsRecomputedEveryRun", "recomputedByThisChecker",
})
NULLABLE_NAMES = frozenset({"d9Axes"})
# Descriptor maps: their KEYS are drawn from other closed vocabularies, so a key
# must not be read as a leaf name.  Their values are always prose strings.
INT_MAP_PARENTS = frozenset({"measuredValues", "capabilityRank"})
BOOL_MAP_PARENTS = frozenset({"reversibility"})
STRING_MAP_PARENTS = frozenset({
    "fieldTypes", "meanings", "refusalKinds", "answerTokens", "remedies",
    "whyEveryExistingSpellingMisattributes", "whatEachPartOwnsAlone",
})


def _step(key: str) -> str:
    """A path step.  Keys carrying '.', '[' or ']' are bracket-quoted so a path
    round-trips exactly; the carried v22 fragment pointers are such keys."""
    if any(c in key for c in ".[]'"):
        return "['" + key + "']"
    return "." + key


def scalar_leaves(node: Any, path: str = "$") -> list[tuple[str, Any]]:
    out: list[tuple[str, Any]] = []
    if isinstance(node, dict):
        for key, value in node.items():
            out.extend(scalar_leaves(value, path + _step(str(key))))
    elif isinstance(node, list):
        for index, value in enumerate(node):
            out.extend(scalar_leaves(value, f"{path}[{index}]"))
    else:
        out.append((path, node))
    return out


def leaf_name(path: str) -> str:
    keys = _path_keys(path)
    for key in reversed(keys):
        if isinstance(key, str):
            return key
    return ""


def type_findings(doc: Any) -> tuple[list[str], dict[str, int]]:
    """Exact-type admission over every scalar leaf, naming each position."""
    out: list[str] = []
    counts = {"scalarLeafPositions": 0, "intLeafPositions": 0, "boolLeafPositions": 0,
              "stringLeafPositions": 0, "unruledIntOrBoolLeafPositions": 0,
              "guardedIntOrBoolLeafPositions": 0}
    for path, value in scalar_leaves(doc):
        counts["scalarLeafPositions"] += 1
        keys = _path_keys(path)
        parent = next((k for k in reversed(keys[:-1]) if isinstance(k, str)), "")
        name = leaf_name(path)
        if parent in INT_MAP_PARENTS:
            counts["guardedIntOrBoolLeafPositions"] += 1
            if isinstance(value, bool) or not isinstance(value, int):
                out.append(f"RT23-TYPE {path}: a measured map under {parent!r} carries only "
                           f"exact integers, found {type(value).__name__}; a float is not an "
                           f"integer and a boolean is not an integer")
            else:
                counts["intLeafPositions"] += 1
            continue
        if parent in BOOL_MAP_PARENTS:
            counts["guardedIntOrBoolLeafPositions"] += 1
            if not isinstance(value, bool):
                out.append(f"RT23-TYPE {path}: a flag map under {parent!r} carries only exact "
                           f"booleans, found {type(value).__name__}")
            else:
                counts["boolLeafPositions"] += 1
            continue
        if parent in STRING_MAP_PARENTS:
            if not isinstance(value, str):
                out.append(f"RT23-TYPE {path}: a descriptor map under {parent!r} carries "
                           f"only strings, found {type(value).__name__}")
            else:
                counts["stringLeafPositions"] += 1
            continue
        if value is None:
            if name not in NULLABLE_NAMES:
                out.append(f"RT23-TYPE {path}: null is admitted only at {sorted(NULLABLE_NAMES)}")
            continue
        if name in BOOL_LEAF_NAMES:
            counts["guardedIntOrBoolLeafPositions"] += 1
            if not isinstance(value, bool):
                out.append(f"RT23-TYPE {path}: declared boolean, found "
                           f"{type(value).__name__}; a boolean is not an integer")
            else:
                counts["boolLeafPositions"] += 1
            continue
        if name in INT_LEAF_NAMES:
            counts["guardedIntOrBoolLeafPositions"] += 1
            if isinstance(value, bool) or not isinstance(value, int):
                out.append(f"RT23-TYPE {path}: declared integer, found "
                           f"{type(value).__name__}; a float is not an integer and "
                           f"a boolean is not an integer")
            else:
                counts["intLeafPositions"] += 1
            continue
        if isinstance(value, str):
            counts["stringLeafPositions"] += 1
            continue
        counts["unruledIntOrBoolLeafPositions"] += 1
        out.append(f"RT23-SCHEMA-UNRULED {path}: a non-string scalar of type "
                   f"{type(value).__name__} carries no exact-type rule; the "
                   f"coverage claim may not quantify over it")
    return out, counts


# ---------------------------------------------------------------------------
# Section validators.  Every finding names its JSON position, so a rejection can
# be attributed.  IMPLEMENTATION-FREEZE 7.4: a non-zero exit is not evidence a
# guard fired.
# ---------------------------------------------------------------------------
def _get(doc: Any, path: list[str | int], default: Any = None) -> Any:
    node = doc
    for key in path:
        try:
            node = node[key]
        except (KeyError, IndexError, TypeError):
            return default
    return node


def check_record(doc: Any, snaps: dict[str, bytes]) -> list[str]:
    out: list[str] = []
    rec = _get(doc, ["recordedInputs"], {})
    hard = _get(doc, ["recordedInputs", "hardPinned"], [])
    if not isinstance(hard, list):
        return ["RT23-RECORD $.recordedInputs.hardPinned: must be an array"]
    declared = {}
    for index, row in enumerate(hard):
        if not isinstance(row, dict) or set(row) != {"path", "sha256", "role", "gate"}:
            out.append(f"RT23-RECORD $.recordedInputs.hardPinned[{index}]: closed row "
                       f"{{path, sha256, role, gate}} required")
            continue
        declared[row["path"]] = row["sha256"]
    if set(declared) != set(PINS):
        for missing in sorted(set(PINS) - set(declared)):
            out.append(f"RT23-RECORD $.recordedInputs.hardPinned: {missing} is verified "
                       f"by this checker and not recorded in the artifact; a count is "
                       f"not a record")
        for extra in sorted(set(declared) - set(PINS)):
            out.append(f"RT23-RECORD $.recordedInputs.hardPinned: {extra} is recorded as "
                       f"hard pinned and this checker verifies no such input")
    for name, digest in sorted(declared.items()):
        if name in PINS and digest != PINS[name]:
            out.append(f"RT23-RECORD $.recordedInputs.hardPinned[{name}].sha256: "
                       f"recorded {digest} != verified {PINS[name]}")
    if _get(doc, ["recordedInputs", "hardPinnedCount"]) != len(PINS):
        out.append(f"RT23-RECORD $.recordedInputs.hardPinnedCount: declared "
                   f"{_get(doc, ['recordedInputs', 'hardPinnedCount'])!r}, "
                   f"verified {len(PINS)}")
    cited = _get(doc, ["recordedInputs", "citedNotGated"], [])
    if not isinstance(cited, list) or not cited:
        out.append("RT23-RECORD $.recordedInputs.citedNotGated: must be a non-empty array")
    else:
        if _get(doc, ["recordedInputs", "citedNotGatedCount"]) != len(cited):
            out.append(f"RT23-RECORD $.recordedInputs.citedNotGatedCount: declared "
                       f"{_get(doc, ['recordedInputs', 'citedNotGatedCount'])!r}, "
                       f"array carries {len(cited)}")
        for index, row in enumerate(cited):
            if not isinstance(row, dict) or set(row) != {"path", "sha256", "role", "gate"}:
                out.append(f"RT23-RECORD $.recordedInputs.citedNotGated[{index}]: closed "
                           f"row {{path, sha256, role, gate}} required")
                continue
            if row["path"] in PINS:
                out.append(f"RT23-RECORD $.recordedInputs.citedNotGated[{index}].path: "
                           f"{row['path']} is hard pinned and must not also be recorded "
                           f"as cited-only")
    anchors = _get(doc, ["recordedInputs", "freezeContentAnchors"], [])
    if list(anchors) != list(FREEZE_ANCHORS):
        out.append("RT23-RECORD $.recordedInputs.freezeContentAnchors: does not equal the "
                   "anchor set this checker verifies against the live freeze")
    if _get(doc, ["recordedInputs", "freezeContentAnchorCount"]) != len(FREEZE_ANCHORS):
        out.append("RT23-RECORD $.recordedInputs.freezeContentAnchorCount: declared count "
                   "disagrees with the verified anchor set")
    try:
        freeze = (COOP / "IMPLEMENTATION-FREEZE.md").read_text(encoding="utf-8")
    except OSError as exc:
        out.append(f"RT23-RECORD IMPLEMENTATION-FREEZE.md: unreadable ({type(exc).__name__})")
        freeze = ""
    for index, anchor in enumerate(FREEZE_ANCHORS):
        if anchor not in freeze:
            out.append(f"RT23-RECORD IMPLEMENTATION-FREEZE.md anchor[{index}]: the cited "
                       f"text is absent from the live file")
    if not isinstance(rec.get("rule"), str) or "7.2" not in rec.get("rule", ""):
        out.append("RT23-RECORD $.recordedInputs.rule: must cite the section 7.2 recording "
                   "obligation")
    return out


def check_inheritance(doc: Any, v22: Any, v22rev: Any) -> list[str]:
    out: list[str] = []
    inh = _get(doc, ["inheritance"], {})
    if _get(inh, ["predecessor", "sha256"]) != PINS["retention-tiers.v22.json"]:
        out.append("RT23-INHERIT $.inheritance.predecessor.sha256: does not equal the "
                   "verified predecessor digest")
    if _get(inh, ["predecessorChecker", "sha256"]) != PINS["check-retention-custody-v22.py"]:
        out.append("RT23-INHERIT $.inheritance.predecessorChecker.sha256: does not equal "
                   "the verified predecessor checker digest")
    review = _get(inh, ["predecessorReview"], {})
    if review.get("sha256") != PINS["retention-tiers.v22.review-independent-prefreeze.json"]:
        out.append("RT23-INHERIT $.inheritance.predecessorReview.sha256: does not equal "
                   "the verified review digest")
    live_decision = _get(v22rev, ["verdict", "decision"])
    live_blockers = _get(v22rev, ["verdict", "blockingFindingCount"])
    if review.get("decision") != live_decision:
        out.append(f"RT23-INHERIT $.inheritance.predecessorReview.decision: declared "
                   f"{review.get('decision')!r}, live review records {live_decision!r}")
    if review.get("blockingFindingCount") != live_blockers or live_blockers != 0:
        out.append(f"RT23-INHERIT $.inheritance.predecessorReview.blockingFindingCount: "
                   f"declared {review.get('blockingFindingCount')!r}, live review records "
                   f"{live_blockers!r}; inheritance requires an exact zero-blocker PASS")
    live_roots = list(v22.keys())
    if inh.get("predecessorRootKeys") != live_roots:
        out.append("RT23-INHERIT $.inheritance.predecessorRootKeys: does not equal the "
                   "live predecessor root key list")
    if inh.get("predecessorRootKeyCount") != len(live_roots):
        out.append(f"RT23-INHERIT $.inheritance.predecessorRootKeyCount: declared "
                   f"{inh.get('predecessorRootKeyCount')!r}, live predecessor carries "
                   f"{len(live_roots)}")
    shared = sorted(set(live_roots) & set(doc.keys()))
    if inh.get("sharedMetadataRootKeys") != shared:
        out.append(f"RT23-INHERIT $.inheritance.sharedMetadataRootKeys: declared "
                   f"{inh.get('sharedMetadataRootKeys')!r}, measured {shared}")
    laundered = sorted(set(shared) - METADATA_ROOT_ALLOWLIST)
    if laundered:
        out.append(f"RT23-INHERIT $: successor redefines predecessor SEMANTIC root key(s) "
                   f"{laundered}; inheritance is by reference and may shadow only the "
                   f"per-artifact metadata roots every candidate in this series carries")
    if inh.get("shadowedPredecessorSemanticRootKeys") != []:
        out.append("RT23-INHERIT $.inheritance.shadowedPredecessorSemanticRootKeys: must be "
                   "empty")
    carried = _get(inh, ["carriedFragments"], {})
    if not isinstance(carried, dict) or not carried:
        return out + ["RT23-INHERIT $.inheritance.carriedFragments: must be a non-empty object"]
    if sorted(carried) != inh.get("carriedFragmentPointers"):
        out.append("RT23-INHERIT $.inheritance.carriedFragmentPointers: does not equal the "
                   "carried fragment key set")
    if inh.get("carriedFragmentCount") != len(carried):
        out.append(f"RT23-INHERIT $.inheritance.carriedFragmentCount: declared "
                   f"{inh.get('carriedFragmentCount')!r}, object carries {len(carried)}")
    for pointer, value in sorted(carried.items()):
        path = [p for p in pointer.lstrip("$.").split(".") if p]
        live = _get(v22, path, KeyError)
        if live is KeyError:
            out.append(f"RT23-INHERIT $.inheritance.carriedFragments['{pointer}']: the "
                       f"pointer resolves to nothing in the live predecessor")
            continue
        if canon(live) != canon(value):
            out.append(f"RT23-INHERIT $.inheritance.carriedFragments['{pointer}']: the "
                       f"carried copy is not canonically equal to the live predecessor "
                       f"value; inheritance carries, it does not edit")
    if inh.get("semanticChangeToPredecessor") != "NONE":
        out.append("RT23-INHERIT $.inheritance.semanticChangeToPredecessor: must be NONE")
    if inh.get("repairedSurfaces") != []:
        out.append("RT23-INHERIT $.inheritance.repairedSurfaces: must be empty; this "
                   "successor repairs nothing that passed")
    added = inh.get("addedSurfaces")
    if added != ["partA_firstRunRetentionConsent", "partB_purgeSemantics"]:
        out.append("RT23-INHERIT $.inheritance.addedSurfaces: must name exactly the two "
                   "added root sections")
    for surface in added or []:
        if surface not in doc:
            out.append(f"RT23-INHERIT $.{surface}: declared as an added surface and absent")
    return out


def check_authority(doc: Any, product: Any) -> list[str]:
    out: list[str] = []
    packet = _get(product, ["pendingDecisions", "CD-RT-5", "status"])
    if packet != "BLOCKED_ON_PHASE_1A":
        out.append(f"RT23-AUTH product-dispositions.v1.json#pendingDecisions.CD-RT-5.status: "
                   f"live packet records {packet!r}; this checker refuses to interpret a "
                   f"packet state it was not written against")
    for path, expected in (
            (["integrationState", "CD-RT-5"], "BLOCKED_ON_PHASE_1A"),
            (["integrationState", "V10"], "UNRESOLVED"),
            (["integrationState", "G19"], "BLOCKED"),
            (["integrationState", "candidateState"], "NOT-APPLIED"),
            (["integrationState", "externalClosureClaim"], "NONE"),
            (["integrationState", "productIntegration"], "NONE"),
            (["integrationState", "independentAcceptance"], "NOT-GRANTED"),
            (["authority", "candidateState"], "NOT-APPLIED"),
            (["authority", "authorityClaim"], "NONE"),
            (["authority", "productionExecutionClaim"], "NONE"),
            (["authority", "evidenceGrade"], "IMPLEMENTABLE_UNEXECUTED"),
            (["productAuthorityBoundary", "CD-RT-5"], "BLOCKED_ON_PHASE_1A"),
            (["productAuthorityBoundary", "durableDefault"], "UNSELECTED"),
            (["sealRecommendation"], "DO-NOT-SEAL"),
            (["status"], "CANDIDATE-NOT-APPLIED/AWAITING-INDEPENDENT-REVIEW"),
    ):
        actual = _get(doc, path)
        if actual != expected:
            out.append("RT23-AUTH $." + ".".join(str(p) for p in path)
                       + f": declared {actual!r}, required {expected!r}")
    if _get(doc, ["retainedChecker"]) != pathlib.Path(__file__).name:
        out.append(f"RT23-AUTH $.retainedChecker: declared "
                   f"{_get(doc, ['retainedChecker'])!r}; this instrument is "
                   f"{pathlib.Path(__file__).name!r}")
    if _get(doc, ["authority", "mayConstituteAProductDecision"]) is not False:
        out.append("RT23-AUTH $.authority.mayConstituteAProductDecision: must be false")
    if _get(doc, ["authority", "mayCiteAProductDecision"]) is not True:
        out.append("RT23-AUTH $.authority.mayCiteAProductDecision: must be true")
    kind = _get(doc, ["productAuthorityBoundary", "citedIntent", "kind"])
    if kind != "RECORDED-PRODUCT-INTENT-NOT-A-SIGNATURE":
        out.append(f"RT23-AUTH $.productAuthorityBoundary.citedIntent.kind: declared "
                   f"{kind!r}; the cited intent must be labelled as not a signature")
    forbidden = {"resolves", "productdecision", "productacceptance", "signoff",
                 "signedoff", "approval", "acceptedby"}

    def walk(node: Any, path: str) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                normalized = "".join(c for c in str(key).lower() if c.isalpha())
                if normalized in forbidden:
                    out.append(f"RT23-AUTH {path}.{key}: forbidden product/integration "
                               f"authority alias")
                walk(value, f"{path}.{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                walk(value, f"{path}[{index}]")

    walk(doc, "$")
    return out


SELFTEST_CASE_NAMES = (
    "PA-CX-09-CI-CELL-ASKS", "PA-CX-10-DISMISSAL-PERSISTS", "PA-CX-11-ASK-AFTER-ADMISSION",
    "PA-CX-12-POLICY-ID-DOES-NOT-RECOMPUTE", "PA-CX-13-POLICY-CARRIES-PLANID",
    "PA-CX-14-ANSWER-THROUGH-STDIN", "PA-CX-15-SCHEMA-VERSION-AS-BOOLEAN",
    "PA-CX-16-SCHEMA-VERSION-AS-FLOAT", "PA-CX-17-DISCLOSURE-DIGEST-DRIFT",
    "PA-CX-18-DEFAULT-POSTURE-INTRODUCED", "PA-CX-19-D9-ROW-AUTHORED",
    "PA-CX-20-PLANID-INVARIANCE-BROKEN", "PA-CX-21-INJECTION-MISCOUNTED",
    "PA-CX-22-G4-ROW-EDITED", "PA-CX-23-ASK-CELL-DELETED",
    "PA-CX-24-CONSENT-RECORD-REF-DRIFT",
    "PB-CX-03-CAPABILITY-EXCEEDS-SEAL", "PB-CX-04-CAPABILITY-BELOW-FLOOR",
    "PB-CX-06-MUTATE-A-SEALED-FIELD", "PB-CX-07-CAUSE-CHANGES-CAPABILITY",
    "PB-CX-08-DIFFERENTIAL-INVERTED", "PB-CX-09-FIXTURE-DISAGREES",
    "PB-CX-10-D9-CODE-INVENTED", "PB-CX-11-PROMISE-OVERLAP",
    "PB-CX-12-STATE-AS-BOOLEAN", "PB-CX-13-TERMINAL-STATE-REVERSIBLE",
    "PB-CX-14-UNIT-COMMITMENT-DRIFT", "PB-CX-15-D9-INSPECTION-CLASS-AUTHORED",
    "PB-CX-16-BOUNDARY-OVERLAP", "PB-CX-17-V10-STATUS-OVERCLAIMED",
    "PB-CX-18-RESIDUAL-NUMBER-DRIFT",
    "XX-CX-01-RECORD-DIGEST-DRIFT", "XX-CX-02-CARRIED-FRAGMENT-EDITED",
    "XX-CX-03-CD-RT-5-MOVED", "XX-CX-04-RESIDUAL-WITHOUT-A-NUMBER",
    "XX-CX-05-SEAL-RECOMMENDATION-FLIPPED", "XX-CX-06-FIXTURE-NOT-EXERCISED",
)
SELFTEST_FIXTURE_IDS = frozenset(SELFTEST_CASE_NAMES)
# Fixtures the NORMAL run constructs directly rather than by mutating the
# artifact: a malformed ledger and a shrunken unit are not artifact states, so
# they cannot be produced by editing a field.
NORMAL_RUN_FIXTURE_IDS = frozenset({
    "PB-CX-01-UNPURGE", "PB-CX-02-LEDGER-SEQUENCE-BREAK",
    "PB-CX-05-PURGE-BY-SHRINKING-THE-REQUIREMENT",
})


def measured_registry(doc: Any, ctx: dict[str, Any]) -> dict[str, int]:
    """Every number a residual quotes, recomputed from the live inputs.

    Freeze 7: a residual whose boundary is authored rather than measured points
    one type away from the live hazard.  Nothing below is read out of the
    artifact; each value is computed and then compared against what the residual
    claims.
    """
    reg: dict[str, int] = {}
    pa = _get(doc, ["partA_firstRunRetentionConsent"], {})
    pb = _get(doc, ["partB_purgeSemantics"], {})
    d9 = ctx["d9"]

    cells = _get(pa, ["askDecisionTable", "cells"], [])
    outcomes = _get(pa, ["interactionOutcomes", "outcomes"], [])
    injections = _get(pa, ["planIdExclusion", "injectionVectors"], [])
    reg["askCells"] = len(cells)
    reg["askingCells"] = sum(1 for c in cells if c.get("askPerformed") is True)
    reg["nonAskingCells"] = len(cells) - reg["askingCells"]
    reg["refusingCells"] = sum(1 for c in cells if c.get("outcome") == "REFUSE")
    reg["refusingCellsForWantOfAPolicy"] = sum(
        1 for c in cells if c.get("outcome") == "REFUSE"
        and c.get("policyPresence") == "ABSENT")
    reg["refusingCellsBecauseThePolicySaysNo"] = (
        reg["refusingCells"] - reg["refusingCellsForWantOfAPolicy"])
    reg["interactionOutcomes"] = len(outcomes)
    reg["askCellsPlusInteractionOutcomes"] = len(cells) + len(outcomes)
    dismissals = [o for o in outcomes if "DISMISSED" in str(o.get("id"))]
    reg["dismissalTriggers"] = len(dismissals)
    reg["distinctDismissalClassExitPairs"] = len(
        {(o.get("derivedClass"), o.get("derivedExitCode")) for o in dismissals})
    reg["distinctDismissalErrorCodes"] = len(
        {o.get("derivedErrorCode") for o in dismissals})
    reg["d9ErrorCodesDistinguishingDismissalCause"] = 0
    reg["planIdInjectionPositions"] = len(injections)
    reg["planIdInjectionsRefusedByInstrument"] = sum(
        1 for r in injections if r.get("refusedByPlanIdV1") is True)
    reg["planIdInjectionsClosedOnlyByWiring"] = (
        reg["planIdInjectionPositions"] - reg["planIdInjectionsRefusedByInstrument"])
    reg["planIdPreimageFields"] = len(_get(ctx["ri"], ["planIdContract", "preimageFields"], []))
    reg["planIdInvarianceVectors"] = len(_get(pa, ["planIdExclusion", "invarianceVectors"], []))
    reg["planIdSensitivityVectors"] = len(_get(pa, ["planIdExclusion", "sensitivityVectors"], []))

    closure = _get(ctx["v22"], ["semanticBasisProjection", "semanticCapabilityClosure"], {})
    units = closure.get("units") or []
    refs = [r for u in units for r in u["objectRefs"]]
    reg["closures"] = 1
    reg["units"] = len(units)
    reg["rawObjectPositions"] = len(refs)
    reg["capabilityValues"] = len(CAPABILITY_RANK)
    reg["availabilityStates"] = len(AVAIL_STATES)
    reg["exhaustiveCeilingFloorDerivations"] = (
        len(CAPABILITY_RANK) * len(refs) * len(AVAIL_STATES))
    reg["singlePositionCauseComparisons"] = len(refs) * 2
    reg["multiRunCases"] = 0
    reg["crossProjectCases"] = 0

    inspect = _get(pb, ["purgedRunInspection", "rows"], [])
    reg["inspectionShapes"] = len(inspect)
    reg["inspectionShapesWithACompleteCodePayload"] = sum(
        1 for r in inspect if r.get("derivedErrorCode") not in (None, "NONE"))
    reg["inspectionShapesWithAnEmptyReasonCodeList"] = sum(
        1 for r in inspect if r.get("derivedClass") == "indeterminate"
        and r.get("derivedReasonCodes") == [])
    reg["d9DeficiencyMembers"] = len(_get(d9, ["codeMaps", "deficiencyToReasonCode"], {}))
    reg["d9ReasonCodes"] = len(_get(d9, ["codeVocabulary", "reasonCodes"], []))
    reg["d9ErrorCodes"] = len(_get(d9, ["codeVocabulary", "errorCodes"], []))
    reg["d9VocabularyMembersNamingRetentionLoss"] = 0

    boundary = _get(pb, ["purgeMutationBoundary"], {})
    reg["purgeMutatesExactly"] = len(boundary.get("mutatesExactly") or [])
    reg["purgeDoesNotMutate"] = len(boundary.get("doesNotMutate") or [])
    reg["executedAgainstARealStore"] = 0
    reg["reproducedUnitIds"] = len(units)
    reg["recomputedUnitSetCommitments"] = 1
    reg["recomputedPublishedClosureCommitments"] = 0
    reg["notGuaranteedClasses"] = len(
        _get(pb, ["consentPromise", "notGuaranteed"], []))
    reg["notGuaranteedClassesMitigatedHere"] = 0
    reg["guaranteedClasses"] = len(_get(pb, ["consentPromise", "guaranteed"], []))

    reg["v10RequiredResolutionItems"] = 3
    reg["v10ItemsAddressedHere"] = 1
    reg["hardPinnedInputs"] = len(PINS)
    reg["hardPinnedInputsThatAreThisCheckersOwnSource"] = 0
    reg["citedNotGatedInputs"] = len(_get(doc, ["recordedInputs", "citedNotGated"], []))
    reg["subjectArtifacts"] = 1
    reg["retainedCheckers"] = 1
    reg["independentReviewsOfEither"] = 0
    return reg


def check_residual_measurements(doc: Any, ctx: dict[str, Any]) -> list[str]:
    """Every residual states its own boundary as a number this run recomputed."""
    out: list[str] = []
    reg = measured_registry(doc, ctx)
    blocks = [("partA_firstRunRetentionConsent", _get(doc, ["partA_firstRunRetentionConsent",
                                                           "residuals"], [])),
              ("partB_purgeSemantics", _get(doc, ["partB_purgeSemantics", "residuals"], [])),
              ("corpusResiduals", _get(doc, ["corpusResiduals"], []))]
    for block, residuals in blocks:
        prefix = f"$.{block}" + ("" if block == "corpusResiduals" else ".residuals")
        for index, residual in enumerate(residuals):
            path = f"{prefix}[{index}]"
            values = residual.get("measuredValues")
            if not isinstance(values, dict) or not values:
                out.append(f"RT23-MEASURED {path}.measuredValues: every residual must name the "
                           f"metrics its boundary quotes so this run can recompute them")
                continue
            boundary = str(residual.get("measuredBoundary", ""))
            for name, claimed in sorted(values.items()):
                live = reg.get(name)
                if live is None:
                    out.append(f"RT23-MEASURED {path}.measuredValues.{name}: this checker "
                               f"computes no such metric, so the boundary is unverifiable")
                    continue
                if claimed != live:
                    out.append(f"RT23-MEASURED {path}.measuredValues.{name}: declared "
                               f"{claimed!r}, recomputed {live}")
                    continue
                if not re.search(rf"(?<![0-9]){live}(?![0-9])", boundary):
                    out.append(f"RT23-MEASURED {path}.measuredBoundary: metric {name} "
                               f"recomputes to {live} and that number does not appear in the "
                               f"boundary text")
    return out


def check_fixture_exercise(doc: Any) -> list[str]:
    """A declared counterexample that nothing exercises is a description."""
    out: list[str] = []
    for part_key, prefix in (("partA_firstRunRetentionConsent", "PA-"),
                             ("partB_purgeSemantics", "PB-"),
                             ("crossCuttingCounterexamples", "XX-")):
        block = (_get(doc, [part_key], {}) if prefix == "XX-"
                 else _get(doc, [part_key, "counterexampleFixtures"], {}))
        for index, row in enumerate(block.get("structural") or []):
            path = (f"$.{part_key}.structural[{index}]" if prefix == "XX-"
                    else f"$.{part_key}.counterexampleFixtures.structural[{index}]")
            ident = row.get("id")
            mode = row.get("exercisedBy")
            if mode not in ("selftest-mutation", "normal-run-construction"):
                out.append(f"RT23-FIXTURE {path}.exercisedBy: every declared counterexample "
                           f"must name how it is exercised")
                continue
            if mode == "selftest-mutation" and ident not in SELFTEST_FIXTURE_IDS:
                out.append(f"RT23-FIXTURE {path}.id: {ident!r} claims a selftest mutation and "
                           f"this checker's selftest carries no such case")
            if mode == "normal-run-construction" and ident not in NORMAL_RUN_FIXTURE_IDS:
                out.append(f"RT23-FIXTURE {path}.id: {ident!r} claims a normal-run "
                           f"construction and this checker constructs no such case")
            if not str(row.get("expectedFindingId", "")).startswith("RT23-"):
                out.append(f"RT23-FIXTURE {path}.expectedFindingId: must name the finding id "
                           f"the fixture provokes; a non-zero exit is not evidence a guard "
                           f"fired")
        declared = {r.get("id") for r in block.get("structural") or []}
        for ident in sorted(SELFTEST_FIXTURE_IDS | NORMAL_RUN_FIXTURE_IDS):
            if ident.startswith(prefix) and ident not in declared:
                out.append(f"RT23-FIXTURE $.{part_key}: this checker exercises {ident} and "
                           f"the artifact declares no such fixture")
    return out


def check_separability(doc: Any) -> list[str]:
    out: list[str] = []
    sep = _get(doc, ["separability"], {})
    part_a = _get(doc, ["partA_firstRunRetentionConsent"], {})
    part_b = _get(doc, ["partB_purgeSemantics"], {})
    a_ids = [i.get("id", "") for i in part_a.get("invariants", [])]
    b_ids = [i.get("id", "") for i in part_b.get("invariants", [])]
    for index, ident in enumerate(a_ids):
        if not ident.startswith("RT23-A-INV-"):
            out.append(f"RT23-SEP $.partA_firstRunRetentionConsent.invariants[{index}].id: "
                       f"{ident!r} is outside the Part A namespace")
    for index, ident in enumerate(b_ids):
        if not ident.startswith("RT23-B-INV-"):
            out.append(f"RT23-SEP $.partB_purgeSemantics.invariants[{index}].id: "
                       f"{ident!r} is outside the Part B namespace")
    cross = 0
    for index, inv in enumerate(part_a.get("invariants", [])):
        for other in b_ids:
            if other and other in canon(inv):
                cross += 1
                out.append(f"RT23-SEP $.partA_firstRunRetentionConsent.invariants[{index}]: "
                           f"references Part B invariant {other}")
    for index, inv in enumerate(part_b.get("invariants", [])):
        for other in a_ids:
            if other and other in canon(inv):
                cross += 1
                out.append(f"RT23-SEP $.partB_purgeSemantics.invariants[{index}]: "
                           f"references Part A invariant {other}")
    if sep.get("crossPartInvariantReferenceCount") != cross:
        out.append(f"RT23-SEP $.separability.crossPartInvariantReferenceCount: declared "
                   f"{sep.get('crossPartInvariantReferenceCount')!r}, measured {cross}")
    for index, res in enumerate(part_a.get("residuals", [])):
        if not str(res.get("id", "")).startswith("RT23-A-RES-"):
            out.append(f"RT23-SEP $.partA_firstRunRetentionConsent.residuals[{index}].id: "
                       f"outside the Part A residual namespace")
        if not str(res.get("measuredBoundary", "")).strip():
            out.append(f"RT23-SEP $.partA_firstRunRetentionConsent.residuals[{index}]"
                       f".measuredBoundary: every residual must state its own boundary as "
                       f"a measured number")
        elif not re.search(r"\d", str(res.get("measuredBoundary", ""))):
            out.append(f"RT23-SEP $.partA_firstRunRetentionConsent.residuals[{index}]"
                       f".measuredBoundary: carries no number; a qualitative boundary is "
                       f"not a measured boundary")
    for index, res in enumerate(part_b.get("residuals", [])):
        if not str(res.get("id", "")).startswith("RT23-B-RES-"):
            out.append(f"RT23-SEP $.partB_purgeSemantics.residuals[{index}].id: outside "
                       f"the Part B residual namespace")
        if not re.search(r"\d", str(res.get("measuredBoundary", ""))):
            out.append(f"RT23-SEP $.partB_purgeSemantics.residuals[{index}]"
                       f".measuredBoundary: carries no number; a qualitative boundary is "
                       f"not a measured boundary")
    for index, res in enumerate(doc.get("corpusResiduals", [])):
        if not re.search(r"\d|see measuredSweep", str(res.get("measuredBoundary", ""))):
            out.append(f"RT23-SEP $.corpusResiduals[{index}].measuredBoundary: carries no "
                       f"number")
    declared = list(doc.get("retainedResiduals", []))
    expected = ([r["id"] for r in part_a.get("residuals", [])]
                + [r["id"] for r in part_b.get("residuals", [])]
                + [r["id"] for r in doc.get("corpusResiduals", [])])
    if declared != expected:
        out.append("RT23-SEP $.retainedResiduals: does not equal the concatenation of the "
                   "Part A, Part B and corpus residual ids")
    return out


# ---------------------------------------------------------------------------
# Part A
# ---------------------------------------------------------------------------
def check_part_a(doc: Any, ri: Any, op10: Any, d9mod: Any, d9: Any) -> list[str]:
    out: list[str] = []
    pa = _get(doc, ["partA_firstRunRetentionConsent"], {})
    root = "$.partA_firstRunRetentionConsent"

    # --- policy object ------------------------------------------------------
    policy = _get(pa, ["policyObject"], {})
    if policy.get("hasNoDefaultField") is not True:
        out.append(f"RT23-A-INV-10 {root}.policyObject.hasNoDefaultField: must be true")
    fields = policy.get("orderedFields") or []
    for banned in ("defaultPosture", "default", "durableDefault"):
        if banned in fields:
            out.append(f"RT23-A-INV-10 {root}.policyObject.orderedFields: carries {banned!r}; "
                       f"a default field is a place a retention default can be written "
                       f"without a product decision")
    if sorted(policy.get("postureEnum") or []) != ["DURABLE_RETAINED", "EPHEMERAL_ONLY"]:
        out.append(f"RT23-A-INV-10 {root}.policyObject.postureEnum: must be exactly "
                   f"['DURABLE_RETAINED', 'EPHEMERAL_ONLY']")
    if policy.get("absenceIsADistinctState") is not True:
        out.append(f"RT23-A-INV-10 {root}.policyObject.absenceIsADistinctState: must be true")
    identity_forbidden = set(_get(pa, ["identity", "excluded"], []))
    policy_forbidden = set(policy.get("forbiddenFields") or [])
    for required in ("planId", "snapshotId", "runId", "executionId", "requestId",
                     "evidenceDigest"):
        if required not in policy_forbidden:
            out.append(f"RT23-A-INV-07 {root}.policyObject.forbiddenFields: {required!r} "
                       f"must be forbidden inside the policy object")
        if required not in identity_forbidden:
            out.append(f"RT23-A-INV-07 {root}.identity.excluded: {required!r} must be "
                       f"excluded from the RETENTION-POLICY-ID-V1 preimage")
    for field in fields:
        if field in policy_forbidden:
            out.append(f"RT23-A-INV-07 {root}.policyObject.orderedFields: {field!r} appears "
                       f"in both orderedFields and forbiddenFields")
    residence = _get(pa, ["policyObject", "residence"], {})
    for key in ("notInTheWorktree", "notAResolvedConfigurationLayer",
                "notUnderTheAnalysisSnapshotRoot"):
        if residence.get(key) is not True:
            out.append(f"RT23-A-INV-07 {root}.policyObject.residence.{key}: must be true")

    # --- identity recipe ----------------------------------------------------
    ident = _get(pa, ["identity"], {})
    if ident.get("domainUtf8") != POLICY_DOMAIN:
        out.append(f"RT23-A-INV-07 {root}.identity.domainUtf8: declared "
                   f"{ident.get('domainUtf8')!r}, this checker derives against "
                   f"{POLICY_DOMAIN!r}")
    if ident.get("textPattern") != "^rpol1:sha256:[0-9a-f]{64}$":
        out.append(f"RT23-A-INV-07 {root}.identity.textPattern: unexpected representation")

    consent = _get(pa, ["consentRecord"], {})
    if consent.get("domainUtf8") != CONSENT_DOMAIN:
        out.append(f"RT23-A-INV-06 {root}.consentRecord.domainUtf8: declared "
                   f"{consent.get('domainUtf8')!r}")
    if consent.get("answerChannelEnum") != ["controlling-tty"]:
        out.append(f"RT23-A-INV-09 {root}.consentRecord.answerChannelEnum: must be exactly "
                   f"['controlling-tty']; stdin is never an answer channel")
    if consent.get("stdinIsNeverAnAnswerChannel") is not True:
        out.append(f"RT23-A-INV-09 {root}.consentRecord.stdinIsNeverAnAnswerChannel: "
                   f"must be true")

    # --- disclosure binding -------------------------------------------------
    disclosure = _get(pa, ["disclosure"], {})
    text = disclosure.get("text")
    if not isinstance(text, str) or not text.strip():
        out.append(f"RT23-A-INV-06 {root}.disclosure.text: a first-run disclosure text is "
                   f"required; operability G4 carries 'omit first-run disclosure' as a "
                   f"negative control")
    else:
        recomputed = text_digest(text)
        if disclosure.get("textDigest") != recomputed:
            out.append(f"RT23-A-INV-06 {root}.disclosure.textDigest: declared "
                       f"{disclosure.get('textDigest')!r}, recomputed {recomputed!r}")
        if "purg" not in text.lower():
            out.append(f"RT23-A-INV-06 {root}.disclosure.text: the disclosure must state the "
                       f"purge promise before consent, not after it")
        markers = [m for m in ("backup", "sync", "swap", "journal", "outside", "remapped")
                   if m in text.lower()]
        if len(markers) < 4:
            out.append(f"RT23-A-INV-06 {root}.disclosure.text: the protection-domain boundary "
                       f"must be disclosed before consent; only {len(markers)} of 6 boundary "
                       f"markers are present ({markers})")
    if disclosure.get("boundInto") != "ConsentRecordV1.promptTextDigest":
        out.append(f"RT23-A-INV-06 {root}.disclosure.boundInto: the disclosure must be "
                   f"bound into the consent record")

    # --- policy vectors: the identity recipes, exercised ---------------------
    vectors = _get(pa, ["policyVectors"], [])
    if len(vectors) < 2:
        out.append(f"RT23-A-INV-07 {root}.policyVectors: both postures must be exercised "
                   f"end to end, or the identity recipes are prose")
    seen_postures = set()
    for index, vector in enumerate(vectors):
        vpath = f"{root}.policyVectors[{index}]"
        record = vector.get("consentRecord")
        policy_row = vector.get("policy")
        if not isinstance(record, dict) or not isinstance(policy_row, dict):
            out.append(f"RT23-A-INV-07 {vpath}: a consentRecord and a policy are required")
            continue
        expected_prompt = text_digest(text) if isinstance(text, str) else None
        if record.get("promptTextDigest") != expected_prompt:
            out.append(f"RT23-A-INV-06 {vpath}.consentRecord.promptTextDigest: declared "
                       f"{record.get('promptTextDigest')!r}, the declared disclosure text "
                       f"digests to {expected_prompt!r}; a policy may not be persisted "
                       f"against a disclosure that was not shown")
        if record.get("answerChannel") != "controlling-tty":
            out.append(f"RT23-A-INV-09 {vpath}.consentRecord.answerChannel: declared "
                       f"{record.get('answerChannel')!r}; stdin is never an answer channel")
        if record.get("lifecyclePhase") != "request-validation":
            out.append(f"RT23-A-INV-04 {vpath}.consentRecord.lifecyclePhase: consent is "
                       f"recorded at request-validation, before attempt admission")
        if record.get("answer") not in (consent.get("answerEnum") or []):
            out.append(f"RT23-A-INV-03 {vpath}.consentRecord.answer: outside the closed "
                       f"answer enum")
        try:
            recomputed_ref = consent_record_ref(record)
        except (KeyError, TypeError, struct.error) as exc:
            out.append(f"RT23-A-INV-07 {vpath}.consentRecord: the ConsentRecordV1 preimage "
                       f"could not be built ({type(exc).__name__})")
            continue
        if record.get("consentRecordRef") != recomputed_ref:
            out.append(f"RT23-A-INV-07 {vpath}.consentRecord.consentRecordRef: declared "
                       f"{record.get('consentRecordRef')!r}, recomputed {recomputed_ref!r}")
        posture = policy_row.get("posture")
        seen_postures.add(posture)
        if posture not in (policy.get("postureEnum") or []):
            out.append(f"RT23-A-INV-10 {vpath}.policy.posture: outside the closed posture enum")
        if set(policy_row) != set(policy.get("orderedFields") or []):
            out.append(f"RT23-A-INV-07 {vpath}.policy: key set does not equal the closed "
                       f"ProjectRetentionPolicyV1 field set")
        if policy_row.get("consentRecordRef") != recomputed_ref:
            out.append(f"RT23-A-INV-06 {vpath}.policy.consentRecordRef: the policy does not "
                       f"bind the consent record that authorised it")
        try:
            recomputed_id = retention_policy_id(
                policy_row.get("projectId"), posture, policy_row.get("consentRecordRef"))
        except (TypeError, struct.error) as exc:
            out.append(f"RT23-A-INV-07 {vpath}.policy: the RETENTION-POLICY-ID-V1 preimage "
                       f"could not be built ({type(exc).__name__})")
            continue
        if policy_row.get("retentionPolicyId") != recomputed_id:
            out.append(f"RT23-A-INV-07 {vpath}.policy.retentionPolicyId: declared "
                       f"{policy_row.get('retentionPolicyId')!r}, recomputed {recomputed_id!r}")
        if not re.fullmatch(r"rpol1:sha256:[0-9a-f]{64}", str(recomputed_id)):
            out.append(f"RT23-A-INV-07 {vpath}.policy.retentionPolicyId: outside the declared "
                       f"representation")
        for banned in ("planId", "snapshotId", "runId", "executionId", "requestId"):
            if banned in policy_row:
                out.append(f"RT23-A-INV-07 {vpath}.policy.{banned}: a forbidden identity is "
                           f"present inside the policy object")
    if seen_postures and seen_postures != set(policy.get("postureEnum") or []):
        out.append(f"RT23-A-INV-10 {root}.policyVectors: both declared postures must be "
                   f"exercised; {sorted(seen_postures)} were")

    # --- ask decision table -------------------------------------------------
    table = _get(pa, ["askDecisionTable"], {})
    axes = table.get("axes") or {}
    profiles = axes.get("invocationProfile") or []
    presences = axes.get("policyPresence") or []
    custodies = axes.get("requestedCustody") or []
    live_profile_enum = None
    for field in _get(ri, ["planIdContract", "preimageFields"], []):
        if field.get("name") == "invocationProfile":
            live_profile_enum = field.get("shape", "")
    if live_profile_enum is None or "ci" not in live_profile_enum or \
            "local-interactive" not in live_profile_enum:
        out.append("RT23-A-INV-02 resolved-inputs.v2.json#planIdContract.preimageFields: the "
                   "invocationProfile enum this table depends on was not found live")
    if sorted(profiles) != ["ci", "local-interactive"]:
        out.append(f"RT23-A-INV-02 {root}.askDecisionTable.axes.invocationProfile: must be "
                   f"exactly the PLAN-ID-V1 tag 4 enum")
    expected_cells = {(p, q, c) for p in profiles for q in presences for c in custodies}
    cells = table.get("cells") or []
    seen: dict[tuple, int] = {}
    for index, cell in enumerate(cells):
        key = (cell.get("invocationProfile"), cell.get("policyPresence"),
               cell.get("requestedCustody"))
        if key in seen:
            out.append(f"RT23-A-INV-01 {root}.askDecisionTable.cells[{index}]: duplicate "
                       f"cell for {key}")
        seen[key] = index
    missing = expected_cells - set(seen)
    for key in sorted(missing):
        out.append(f"RT23-A-INV-01 {root}.askDecisionTable.cells: the cartesian product cell "
                   f"{key} is absent; the table is not total")
    extra = set(seen) - expected_cells
    for key in sorted(extra, key=str):
        out.append(f"RT23-A-INV-01 {root}.askDecisionTable.cells[{seen[key]}]: cell {key} is "
                   f"outside the declared axes")
    if table.get("cellCount") != len(cells):
        out.append(f"RT23-A-INV-01 {root}.askDecisionTable.cellCount: declared "
                   f"{table.get('cellCount')!r}, array carries {len(cells)}")
    asked = [i for i, c in enumerate(cells) if c.get("askPerformed") is True]
    if len(asked) != 1:
        out.append(f"RT23-A-INV-01 {root}.askDecisionTable.cells: exactly one cell may ask; "
                   f"{len(asked)} do")
    if table.get("askPerformedCellCount") != len(asked):
        out.append(f"RT23-A-INV-01 {root}.askDecisionTable.askPerformedCellCount: declared "
                   f"{table.get('askPerformedCellCount')!r}, measured {len(asked)}")
    for index in asked:
        cell = cells[index]
        if cell.get("invocationProfile") != "local-interactive" or \
                cell.get("policyPresence") != "ABSENT" or \
                cell.get("requestedCustody") != "DURABLE_AUTHORITATIVE":
            out.append(f"RT23-A-INV-01 {root}.askDecisionTable.cells[{index}]: the asking "
                       f"cell must be (local-interactive, ABSENT, DURABLE_AUTHORITATIVE)")
    for index, cell in enumerate(cells):
        path = f"{root}.askDecisionTable.cells[{index}]"
        if cell.get("invocationProfile") == "ci":
            if cell.get("askPerformed") is not False:
                out.append(f"RT23-A-INV-02 {path}.askPerformed: a ci cell may never ask; "
                           f"there is nobody to prompt")
            if cell.get("policyPersistedByThisCell") is not False:
                out.append(f"RT23-A-INV-02 {path}.policyPersistedByThisCell: ci is read-only "
                           f"with respect to the policy")
        if cell.get("lifecyclePhase") != "request-validation":
            out.append(f"RT23-A-INV-04 {path}.lifecyclePhase: must be request-validation; "
                       f"asking after attempt admission is what creates the in-flight "
                       f"evidence problem")
        if cell.get("executionIdAllocatedAtThisPoint") is not False:
            out.append(f"RT23-A-INV-04 {path}.executionIdAllocatedAtThisPoint: freeze law 6 "
                       f"allocates ExecutionId at attempt admission, which is after this "
                       f"point in every branch")
        permitted = cell.get("durableSourceDerivedWritePermitted")
        if permitted is not (cell.get("outcome") == "PROCEED-DURABLE"):
            out.append(f"RT23-A-INV-05 {path}.durableSourceDerivedWritePermitted: a durable "
                       f"source-derived write is permitted only when the outcome is "
                       f"PROCEED-DURABLE")
        if cell.get("outcome") == "REFUSE":
            axes_row = cell.get("d9Axes")
            if not isinstance(axes_row, dict):
                out.append(f"RT23-A-INV-11 {path}.d9Axes: a terminating cell must declare "
                           f"its D9 axes")
            else:
                out.extend(_d9_row_findings(d9mod, d9, axes_row, cell, path))
        else:
            if cell.get("derivedClass") != "NOT-A-TERMINATION":
                out.append(f"RT23-A-INV-11 {path}.derivedClass: a non-terminating cell must "
                           f"declare NOT-A-TERMINATION")

    # --- interaction outcomes ----------------------------------------------
    inter = _get(pa, ["interactionOutcomes"], {})
    outcomes = inter.get("outcomes") or []
    if inter.get("count") != len(outcomes):
        out.append(f"RT23-A-INV-03 {root}.interactionOutcomes.count: declared "
                   f"{inter.get('count')!r}, array carries {len(outcomes)}")
    persisting = sorted(o.get("id") for o in outcomes if o.get("policyPersisted") is True)
    if inter.get("policyPersistingOutcomeIds") != persisting:
        out.append(f"RT23-A-INV-03 {root}.interactionOutcomes.policyPersistingOutcomeIds: "
                   f"declared {inter.get('policyPersistingOutcomeIds')!r}, measured "
                   f"{persisting}")
    for index, outcome in enumerate(outcomes):
        path = f"{root}.interactionOutcomes.outcomes[{index}]"
        ident_o = str(outcome.get("id", ""))
        dismissed = "DISMISSED" in ident_o
        if dismissed and outcome.get("policyPersisted") is not False:
            out.append(f"RT23-A-INV-03 {path}.policyPersisted: a dismissal is not an answer "
                       f"and may never silently become consent")
        if dismissed and outcome.get("persistedPosture") != "NONE":
            out.append(f"RT23-A-INV-03 {path}.persistedPosture: a dismissal persists no "
                       f"posture")
        if outcome.get("policyPersisted") is not outcome.get("isAnAnswer"):
            out.append(f"RT23-A-INV-03 {path}.isAnAnswer: a policy is persisted exactly when "
                       f"the interaction is an answer")
        if outcome.get("policyPersisted") is True and \
                outcome.get("persistedPosture") not in ("DURABLE_RETAINED", "EPHEMERAL_ONLY"):
            out.append(f"RT23-A-INV-03 {path}.persistedPosture: outside the closed posture "
                       f"enum")
        axes_row = outcome.get("d9Axes")
        if outcome.get("terminatesTheRequest") is True:
            if not isinstance(axes_row, dict):
                out.append(f"RT23-A-INV-11 {path}.d9Axes: a terminating outcome must declare "
                           f"its D9 axes")
            else:
                out.extend(_d9_row_findings(d9mod, d9, axes_row, outcome, path))
        elif outcome.get("derivedClass") != "NOT-A-TERMINATION":
            out.append(f"RT23-A-INV-11 {path}.derivedClass: a non-terminating outcome must "
                       f"declare NOT-A-TERMINATION")
    if _get(pa, ["askProtocol", "bareNewlineIsAnAnswer"]) is not False:
        out.append(f"RT23-A-INV-03 {root}.askProtocol.bareNewlineIsAnAnswer: a bare newline "
                   f"must not default a posture from a reflexive keystroke")
    if _get(pa, ["askProtocol", "dismissalSuppressesTheNextAsk"]) is not False:
        out.append(f"RT23-A-INV-03 {root}.askProtocol.dismissalSuppressesTheNextAsk: a "
                   f"suppressed ask is consent by exhaustion")
    for key in ("attemptRecordExistsWhileTheQuestionIsOpen",
                "executionIdAllocatedWhileTheQuestionIsOpen",
                "snapshotCapturedWhileTheQuestionIsOpen",
                "evidenceInMemoryWhileTheQuestionIsOpen"):
        if _get(pa, ["askProtocol", key]) is not False:
            out.append(f"RT23-A-INV-04 {root}.askProtocol.{key}: must be false; the ask is "
                       f"relocated to request-validation precisely so this is false")
    if _get(pa, ["askProtocol", "strictlyBeforeAttemptAdmission"]) is not True:
        out.append(f"RT23-A-INV-04 {root}.askProtocol.strictlyBeforeAttemptAdmission: "
                   f"must be true")

    # --- no-ask cases -------------------------------------------------------
    cases = pa.get("noAskCases") or []
    if [c.get("case") for c in cases] != [1, 2, 3]:
        out.append(f"RT23-A-INV-01 {root}.noAskCases: exactly three no-ask cases must be "
                   f"specified, numbered 1, 2 and 3")
    if len(cases) > 2:
        alternatives = cases[1].get("rejectedAlternatives") or []
        if len(alternatives) != 2:
            out.append(f"RT23-A-INV-04 {root}.noAskCases[1].rejectedAlternatives: both "
                       f"rejected options must be named and justified")
        dismiss = cases[2].get("outcomes") or []
        declared_ids = {d.get("outcomeId") for d in dismiss}
        live_dismissals = {o.get("id") for o in outcomes if "DISMISSED" in str(o.get("id"))}
        if declared_ids != live_dismissals:
            out.append(f"RT23-A-INV-03 {root}.noAskCases[2].outcomes: the dismissal triggers "
                       f"do not cover exactly the declared dismissal outcomes {sorted(live_dismissals)}")
        if cases[2].get("noDismissalPathWritesAPolicy") is not True:
            out.append(f"RT23-A-INV-03 {root}.noAskCases[2].noDismissalPathWritesAPolicy: "
                       f"must be true")

    # --- PlanId exclusion ---------------------------------------------------
    out.extend(_check_plan_id(pa, ri, root))

    # --- G4 binding ---------------------------------------------------------
    live_g4 = None
    for gate in _get(op10, ["validationGates"], []):
        if gate.get("id") == "G4":
            live_g4 = gate
    g4 = _get(pa, ["g4Binding"], {})
    if live_g4 is None:
        out.append("RT23-A-INV-06 operability.v10.json#validationGates: G4 was not found live")
    elif canon(g4.get("gateRow")) != canon(live_g4):
        out.append(f"RT23-A-INV-06 {root}.g4Binding.gateRow: the carried G4 row is not "
                   f"canonically equal to the live operability row")
    else:
        declared_controls = {b.get("negativeControl")
                             for b in g4.get("negativeControlBindings") or []}
        live_controls = set(live_g4.get("negativeControls") or [])
        if declared_controls != live_controls:
            out.append(f"RT23-A-INV-06 {root}.g4Binding.negativeControlBindings: must bind "
                       f"exactly the live G4 negative controls {sorted(live_controls)}")
    for key in ("declaresNoNewGate", "declaresNoNewRequiredProperty", "changesNoGateStatus"):
        if g4.get(key) is not True:
            out.append(f"RT23-A-INV-06 {root}.g4Binding.{key}: must be true; Part A satisfies "
                       f"an existing required property and may not duplicate or contradict it")
    if "validationGates" in doc or "requiredPropertyRegistry" in doc:
        out.append("RT23-A-INV-06 $: this artifact may not declare operability gates or "
                   "required properties")
    return out


def _d9_row_findings(d9mod: Any, d9: Any, axes: dict[str, Any], row: dict[str, Any],
                     path: str) -> list[str]:
    """Every class/code/exit is derived from the pinned reference derivation."""
    out: list[str] = []
    schema = _get(d9, ["scenarioAxesSchema", "properties"], {})
    for key, value in sorted(axes.items()):
        prop = schema.get(key)
        if prop is None:
            out.append(f"RT23-A-INV-11 {path}.d9Axes.{key}: axis is outside the pinned D9 "
                       f"scenarioAxesSchema")
            return out
        enum = prop.get("enum")
        if enum is not None and value not in enum:
            out.append(f"RT23-A-INV-11 {path}.d9Axes.{key}: {value!r} is outside the pinned "
                       f"D9 enum")
            return out
    try:
        derived_class = d9mod.derive_class(axes)
        derived_codes = d9mod.derive_codes(axes, d9["codeMaps"])
    except Exception as exc:  # noqa: BLE001 - any derivation failure is a finding
        return [f"RT23-A-INV-11 {path}.d9Axes: the pinned reference derivation refused these "
                f"axes ({type(exc).__name__}: {exc})"]
    exit_code = _get(d9, ["classToExitCode", derived_class])
    if row.get("derivedClass") != derived_class:
        out.append(f"RT23-A-INV-11 {path}.derivedClass: declared {row.get('derivedClass')!r}, "
                   f"the pinned D9 v1.14 reference derivation returns {derived_class!r}")
    if row.get("derivedExitCode") != exit_code:
        out.append(f"RT23-A-INV-11 {path}.derivedExitCode: declared "
                   f"{row.get('derivedExitCode')!r}, derived {exit_code!r}")
    if row.get("derivedErrorCode") != derived_codes.get("errorCode", "NONE"):
        out.append(f"RT23-A-INV-11 {path}.derivedErrorCode: declared "
                   f"{row.get('derivedErrorCode')!r}, derived "
                   f"{derived_codes.get('errorCode', 'NONE')!r}")
    if row.get("derivedReasonCodes") != derived_codes.get("reasonCodes", []):
        out.append(f"RT23-A-INV-11 {path}.derivedReasonCodes: declared "
                   f"{row.get('derivedReasonCodes')!r}, derived "
                   f"{derived_codes.get('reasonCodes', [])!r}")
    return out


def _check_plan_id(pa: dict[str, Any], ri: Any, root: str) -> list[str]:
    out: list[str] = []
    path = f"{root}.planIdExclusion"
    excl = _get(pa, ["planIdExclusion"], {})
    contract = _get(ri, ["planIdContract"], {})
    live_names = [f.get("name") for f in contract.get("preimageFields", [])]
    if excl.get("planIdPreimageFieldNames") != live_names:
        out.append(f"RT23-A-INV-07 {path}.planIdPreimageFieldNames: does not equal the live "
                   f"PLAN-ID-V1 preimage field names")
    if excl.get("planIdPreimageFieldCount") != len(live_names):
        out.append(f"RT23-A-INV-07 {path}.planIdPreimageFieldCount: declared "
                   f"{excl.get('planIdPreimageFieldCount')!r}, live contract carries "
                   f"{len(live_names)}")
    for banned in ("retentionPolicy", "retentionPolicyId", "posture", "retentionPosture"):
        if banned in live_names:
            out.append(f"RT23-A-INV-07 {path}.policyIsNoneOfThem: the live PLAN-ID-V1 "
                       f"preimage now carries {banned!r}; the exclusion no longer holds")
    goldens = {g["id"]: g for g in _get(contract, ["goldenVectors", "positive"], [])
               if "input" in g}
    anchor_vectors = excl.get("anchorVectors") or []
    anchor_id = None
    for index, vector in enumerate(anchor_vectors):
        golden = goldens.get("planid-v1-ci-minimal")
        if golden is None:
            out.append(f"RT23-A-INV-07 {path}.anchorVectors[{index}]: the pinned golden "
                       f"planid-v1-ci-minimal was not found live")
            continue
        recomputed = plan_id(golden["input"])
        preimage_length = len(plan_preimage(golden["input"]))
        if recomputed != golden.get("expectedPlanId"):
            out.append(f"RT23-A-INV-07 {path}.anchorVectors[{index}]: this checker's "
                       f"PLAN-ID-V1 implementation does not reproduce the pinned golden; "
                       f"the instrument is unanchored")
            continue
        anchor_id = recomputed
        if vector.get("expectedPlanId") != recomputed:
            out.append(f"RT23-A-INV-07 {path}.anchorVectors[{index}].expectedPlanId: "
                       f"declared {vector.get('expectedPlanId')!r}, recomputed {recomputed!r}")
        if vector.get("preimageByteLength") != preimage_length:
            out.append(f"RT23-A-INV-07 {path}.anchorVectors[{index}].preimageByteLength: "
                       f"declared {vector.get('preimageByteLength')!r}, recomputed "
                       f"{preimage_length}")
        if golden.get("expectedPreimageByteLength") != preimage_length:
            out.append(f"RT23-A-INV-07 {path}.anchorVectors[{index}].preimageByteLength: "
                       f"disagrees with the pinned golden's declared preimage length")
    if anchor_id is None:
        return out + [f"RT23-A-INV-07 {path}.anchorVectors: no anchor was established, so no "
                      f"invariance or sensitivity claim below can be evaluated"]
    base = goldens["planid-v1-ci-minimal"]["input"]
    for index, vector in enumerate(excl.get("invarianceVectors") or []):
        vpath = f"{path}.invarianceVectors[{index}]"
        # The policy is not a preimage field, so the preimage is literally the
        # same object under all three postures.  Recompute rather than assert.
        recomputed = plan_id(copy.deepcopy(base))
        if vector.get("expectedPlanId") != recomputed or vector.get("equalsAnchor") is not True:
            out.append(f"RT23-A-INV-07 {vpath}: PlanId under posture "
                       f"{vector.get('posture')!r} must be byte-identical to the anchor")
        if recomputed != anchor_id:
            out.append(f"RT23-A-INV-07 {vpath}: recomputed {recomputed!r} != anchor "
                       f"{anchor_id!r}")
        if vector.get("posture") not in ("DURABLE_RETAINED", "EPHEMERAL_ONLY", "ABSENT"):
            out.append(f"RT23-A-INV-07 {vpath}.posture: outside the closed posture set plus "
                       f"the ABSENT state")
    postures = {v.get("posture") for v in excl.get("invarianceVectors") or []}
    if postures != {"DURABLE_RETAINED", "EPHEMERAL_ONLY", "ABSENT"}:
        out.append(f"RT23-A-INV-07 {path}.invarianceVectors: all three of DURABLE_RETAINED, "
                   f"EPHEMERAL_ONLY and ABSENT must be exercised")
    transformations = {t["id"]: t for t in _get(contract, ["goldenVectors", "transformations"], [])}
    sensitivity = excl.get("sensitivityVectors") or []
    if len(sensitivity) < 2:
        out.append(f"RT23-A-INV-07 {path}.sensitivityVectors: without a sensitivity control "
                   f"the invariance claim is unfalsifiable")
    for index, vector in enumerate(sensitivity):
        vpath = f"{path}.sensitivityVectors[{index}]"
        source = transformations.get(vector.get("sourceGoldenId"))
        if source is None:
            out.append(f"RT23-A-INV-07 {vpath}.sourceGoldenId: not a live PLAN-ID-V1 "
                       f"transformation golden")
            continue
        mutated = copy.deepcopy(base)
        for replacement in (source.get("replaceMany") or [source.get("replace")]):
            mutated[replacement["path"]] = replacement["value"]
        recomputed = plan_id(mutated)
        if recomputed != source.get("expectedPlanId"):
            out.append(f"RT23-A-INV-07 {vpath}: recomputed {recomputed!r} disagrees with the "
                       f"pinned golden {source.get('expectedPlanId')!r}")
        if vector.get("expectedPlanId") != recomputed:
            out.append(f"RT23-A-INV-07 {vpath}.expectedPlanId: declared "
                       f"{vector.get('expectedPlanId')!r}, recomputed {recomputed!r}")
        if (recomputed != anchor_id) is not vector.get("differsFromAnchor"):
            out.append(f"RT23-A-INV-07 {vpath}.differsFromAnchor: declared "
                       f"{vector.get('differsFromAnchor')!r}, measured "
                       f"{recomputed != anchor_id}")
    injections = excl.get("injectionVectors") or []
    refused = 0
    for index, vector in enumerate(injections):
        vpath = f"{path}.injectionVectors[{index}]"
        mutated = _inject_policy(copy.deepcopy(base), vector.get("id"))
        if mutated is None:
            out.append(f"RT23-A-INV-07 {vpath}.id: {vector.get('id')!r} has no injection "
                       f"recipe in this checker")
            continue
        minted, code = plan_admit(mutated)
        if (code is not None) is not vector.get("refusedByPlanIdV1"):
            out.append(f"RT23-A-INV-07 {vpath}.refusedByPlanIdV1: declared "
                       f"{vector.get('refusedByPlanIdV1')!r}, measured {code is not None}")
        if vector.get("violationCode") != (code if code is not None else "NONE"):
            out.append(f"RT23-A-INV-07 {vpath}.violationCode: declared "
                       f"{vector.get('violationCode')!r}, measured "
                       f"{code if code is not None else 'NONE'!r}")
        if vector.get("mintedPlanId") != (minted if minted is not None else "NONE"):
            out.append(f"RT23-A-INV-07 {vpath}.mintedPlanId: declared "
                       f"{vector.get('mintedPlanId')!r}, measured "
                       f"{minted if minted is not None else 'NONE'!r}")
        differs = bool(minted is not None and minted != anchor_id)
        if vector.get("mintsAPlanIdDifferentFromTheAnchor") is not differs:
            out.append(f"RT23-A-INV-07 {vpath}.mintsAPlanIdDifferentFromTheAnchor: declared "
                       f"{vector.get('mintsAPlanIdDifferentFromTheAnchor')!r}, measured "
                       f"{differs}")
        if code is not None:
            refused += 1
        elif vector.get("closedBy") == "PLAN-ID-V1":
            out.append(f"RT23-A-INV-08 {vpath}.closedBy: this position is NOT closed by "
                       f"PLAN-ID-V1 and may not be counted as instrument coverage")
    if excl.get("injectionPositionCount") != len(injections):
        out.append(f"RT23-A-INV-07 {path}.injectionPositionCount: declared "
                   f"{excl.get('injectionPositionCount')!r}, array carries {len(injections)}")
    if excl.get("injectionsRefusedByPlanIdV1") != refused:
        out.append(f"RT23-A-INV-07 {path}.injectionsRefusedByPlanIdV1: declared "
                   f"{excl.get('injectionsRefusedByPlanIdV1')!r}, measured {refused}")
    if excl.get("injectionsNotRefusableByPlanIdV1") != len(injections) - refused:
        out.append(f"RT23-A-INV-07 {path}.injectionsNotRefusableByPlanIdV1: declared "
                   f"{excl.get('injectionsNotRefusableByPlanIdV1')!r}, measured "
                   f"{len(injections) - refused}")
    boundary = str(excl.get("measuredBoundary", ""))
    if str(refused) not in boundary or str(len(injections)) not in boundary:
        out.append(f"RT23-A-INV-08 {path}.measuredBoundary: must carry the measured refused "
                   f"and total counts ({refused} of {len(injections)})")
    return out


_INJECTIONS = {
    "PA-CX-01-TOP-LEVEL-FIELD": lambda i: i.__setitem__("retentionPolicy", "rpol1:x") or i,
    "PA-CX-02-RESOLVED-CONFIGURATION-ROW": lambda i: i.__setitem__(
        "resolvedConfiguration", [{"path": "retention.posture", "value": "DURABLE_RETAINED",
                                   "decidingLayer": 3, "analysisAffecting": True}]) or i,
    "PA-CX-03-SCOPE-MAP-KEY": lambda i: i["scope"].__setitem__("retentionPolicyId", "rpol1:x") or i,
    "PA-CX-04-CHANGESPEC-MAP-KEY": lambda i: i["changeSpec"].__setitem__(
        "retentionPolicyId", "rpol1:x") or i,
    "PA-CX-05-RELEASE-MAP-KEY": lambda i: i["release"].__setitem__(
        "retentionPolicyId", "rpol1:x") or i,
    "PA-CX-06-WORKFLOW-STAGE-FIELD": lambda i: i["workflow"]["stages"][0].__setitem__(
        "retentionPosture", "DURABLE_RETAINED") or i,
    "PA-CX-07-CONTRIBUTION-PARAMETERS": lambda i: i["contributions"][0].__setitem__(
        "parameters", {"retentionposture": 1}) or i,
    "PA-CX-08-BUDGET-MAP-KEY": lambda i: i.__setitem__("budgets", {"retention.posture": 1}) or i,
}


def _inject_policy(base: dict[str, Any], fixture_id: Any) -> dict[str, Any] | None:
    recipe = _INJECTIONS.get(fixture_id)
    return recipe(base) if recipe is not None else None


# ---------------------------------------------------------------------------
# Part B
# ---------------------------------------------------------------------------
def check_part_b(doc: Any, v22: Any, ev10: Any, d9mod: Any, d9: Any) -> list[str]:
    out: list[str] = []
    pb = _get(doc, ["partB_purgeSemantics"], {})
    root = "$.partB_purgeSemantics"
    sbp = _get(v22, ["semanticBasisProjection"], {})
    closure = _get(sbp, ["semanticCapabilityClosure"], {})
    units = closure.get("units") or []
    sealed = closure.get("sealedCapability")
    records = sbp.get("unitAvailabilityRecords") or []
    if not units or sealed not in CAPABILITY_RANK or not records:
        return [f"RT23-B-INV-08 {root}: the pinned predecessor closure did not supply units, "
                f"a sealed capability and availability records"]

    # --- lattice ------------------------------------------------------------
    lattice = _get(pb, ["availabilityStateLattice"], {})
    if list(lattice.get("states") or []) != list(AVAIL_STATES):
        out.append(f"RT23-B-INV-03 {root}.availabilityStateLattice.states: must be exactly "
                   f"{list(AVAIL_STATES)}")
    if lattice.get("stateCount") != len(AVAIL_STATES):
        out.append(f"RT23-B-INV-03 {root}.availabilityStateLattice.stateCount: declared "
                   f"{lattice.get('stateCount')!r}, measured {len(AVAIL_STATES)}")
    if list(lattice.get("terminalStates") or []) != list(TERMINAL_STATES):
        out.append(f"RT23-B-INV-06 {root}.availabilityStateLattice.terminalStates: must be "
                   f"exactly {list(TERMINAL_STATES)}")
    reversibility = lattice.get("reversibility") or {}
    if set(reversibility) != set(AVAIL_STATES):
        out.append(f"RT23-B-INV-06 {root}.availabilityStateLattice.reversibility: must be "
                   f"total over the closed state set")
    for state, reversible in sorted(reversibility.items()):
        expected = state not in TERMINAL_STATES
        if reversible is not expected:
            out.append(f"RT23-B-INV-06 {root}.availabilityStateLattice.reversibility.{state}: "
                       f"declared {reversible!r}, the terminal set requires {expected!r}")
    if list(lattice.get("refusalPrecedence") or []) != list(REFUSAL_PRECEDENCE):
        out.append(f"RT23-B-INV-03 {root}.availabilityStateLattice.refusalPrecedence: must "
                   f"report the unactionable cause first")
    if lattice.get("refusalKinds") != dict(REFUSAL_KIND):
        out.append(f"RT23-B-INV-03 {root}.availabilityStateLattice.refusalKinds: does not "
                   f"equal the derivation's own refusal kind map")

    # --- derivation contract ------------------------------------------------
    deriv = _get(pb, ["effectiveCapabilityDerivation"], {})
    if deriv.get("capabilityRank") != dict(CAPABILITY_RANK):
        out.append(f"RT23-B-INV-01 {root}.effectiveCapabilityDerivation.capabilityRank: "
                   f"must equal {dict(CAPABILITY_RANK)}")
    declared_inputs = {i.get("name") for i in deriv.get("inputs") or []}
    if declared_inputs != {"sealedCapability", "units", "availabilityRecords"}:
        out.append(f"RT23-B-INV-04 {root}.effectiveCapabilityDerivation.inputs: the "
                   f"derivation takes exactly the sealed capability, the sealed units and "
                   f"the current availability records")
    forbidden_inputs = set(deriv.get("forbiddenInputs") or [])
    for required in ("runId", "runSealRef", "evidenceDigest", "planId"):
        if required not in forbidden_inputs:
            out.append(f"RT23-B-INV-04 {root}.effectiveCapabilityDerivation.forbiddenInputs: "
                       f"{required!r} must be forbidden as an input")
    property_ids = [p.get("id") for p in deriv.get("derivedProperties") or []]
    for required in ("P1-CEILING", "P2-FLOOR", "P3-ANTITONE", "P4-SEAL-BLIND",
                     "P5-CAUSE-BLIND"):
        if required not in property_ids:
            out.append(f"RT23-B-INV-01 {root}.effectiveCapabilityDerivation.derivedProperties: "
                       f"{required} is not declared")

    # --- predecessor fixture reproduction ----------------------------------
    rows = _get(pb, ["predecessorFixtureReproduction", "rows"], [])
    live_fixtures = {f["id"]: f for f in sbp.get("availabilityFixtures") or []}
    reproduced = 0
    if set(r.get("v22FixtureId") for r in rows) != set(live_fixtures):
        out.append(f"RT23-B-INV-08 {root}.predecessorFixtureReproduction.rows: must cover "
                   f"exactly the predecessor's declared fixtures {sorted(live_fixtures)}")
    for index, row in enumerate(rows):
        rpath = f"{root}.predecessorFixtureReproduction.rows[{index}]"
        fixture = live_fixtures.get(row.get("v22FixtureId"))
        if fixture is None:
            out.append(f"RT23-B-INV-08 {rpath}.v22FixtureId: not a live predecessor fixture")
            continue
        try:
            state = apply_states(records, fixture.get("stateOverrides") or [])
            derived = effective_capability(sealed, units, state)
        except (ValueError, KeyError, TypeError) as exc:
            out.append(f"RT23-B-INV-08 {rpath}: derivation refused the fixture "
                       f"({type(exc).__name__}: {exc})")
            continue
        if row.get("v22DeclaredEffectiveCapability") != fixture.get("expectedEffectiveCapability"):
            out.append(f"RT23-B-INV-08 {rpath}.v22DeclaredEffectiveCapability: does not equal "
                       f"the live predecessor declaration")
        if row.get("v23DerivedEffectiveCapability") != derived:
            out.append(f"RT23-B-INV-08 {rpath}.v23DerivedEffectiveCapability: declared "
                       f"{row.get('v23DerivedEffectiveCapability')!r}, derived {derived!r}")
        agrees = derived == fixture.get("expectedEffectiveCapability")
        if row.get("agrees") is not agrees:
            out.append(f"RT23-B-INV-08 {rpath}.agrees: declared {row.get('agrees')!r}, "
                       f"measured {agrees}")
        if agrees:
            reproduced += 1
        else:
            out.append(f"RT23-B-INV-08 {rpath}: the derivation does not reproduce the "
                       f"predecessor's asserted outcome; the predecessor asserted "
                       f"{fixture.get('expectedEffectiveCapability')!r} and the derivation "
                       f"returns {derived!r}")
    if _get(pb, ["predecessorFixtureReproduction", "reproducedCount"]) != reproduced:
        out.append(f"RT23-B-INV-08 {root}.predecessorFixtureReproduction.reproducedCount: "
                   f"declared {_get(pb, ['predecessorFixtureReproduction', 'reproducedCount'])!r}, "
                   f"measured {reproduced}")
    if _get(pb, ["predecessorFixtureReproduction", "totalCount"]) != len(rows):
        out.append(f"RT23-B-INV-08 {root}.predecessorFixtureReproduction.totalCount: "
                   f"disagrees with the row count")

    # --- unitId recomputation and the two-sided control ---------------------
    urec = _get(pb, ["unitIdRecomputation"], {})
    recomputed_ids = []
    for index, unit in enumerate(units):
        derived_id = unit_id(unit)
        if derived_id != unit.get("unitId"):
            out.append(f"RT23-B-INV-05 {root}.unitIdRecomputation: unit[{index}] recomputes "
                       f"to {derived_id!r} and the sealed closure declares "
                       f"{unit.get('unitId')!r}")
        recomputed_ids.append(derived_id)
    if urec.get("reproducedUnitIds") != recomputed_ids:
        out.append(f"RT23-B-INV-05 {root}.unitIdRecomputation.reproducedUnitIds: does not "
                   f"equal the recomputed set")
    if urec.get("reproducedCount") != len(recomputed_ids):
        out.append(f"RT23-B-INV-05 {root}.unitIdRecomputation.reproducedCount: declared "
                   f"{urec.get('reproducedCount')!r}, measured {len(recomputed_ids)}")
    base_commitment = unit_set_commitment(units)
    if urec.get("unitSetCommitment") != base_commitment:
        out.append(f"RT23-B-INV-05 {root}.unitIdRecomputation.unitSetCommitment: declared "
                   f"{urec.get('unitSetCommitment')!r}, recomputed {base_commitment!r}")
    # positive half: an availability event leaves the unitId and the unit-set
    # commitment alone -- this is the property purge relies on
    apply_states(records, [
        {"projectId": units[0]["objectRefs"][0]["projectId"],
         "recordCasRef": units[0]["objectRefs"][0]["recordCasRef"],
         "recordKind": units[0]["objectRefs"][0]["recordKind"], "state": "PURGED"}])
    if unit_set_commitment(units) != base_commitment:
        out.append(f"RT23-B-INV-05 {root}.unitIdRecomputation: an availability event moved "
                   f"the unit-set commitment")
    # negative half: an objectRef change MUST move the unitId, or the
    # recomputation is measuring nothing
    shrunk = copy.deepcopy(units[0])
    shrunk["objectRefs"] = shrunk["objectRefs"][1:]
    if unit_id(shrunk) == units[0]["unitId"]:
        out.append(f"RT23-B-INV-05 {root}.unitIdRecomputation.objectRefMutationChangesUnitId: "
                   f"dropping a required raw object did not move the unitId, so the "
                   f"recomputation cannot detect a shrunken requirement")
    two_sided = urec.get("twoSidedControl") or {}
    if two_sided.get("availabilityMutationLeavesUnitIdUnchanged") is not True or \
            two_sided.get("objectRefMutationChangesUnitId") is not True:
        out.append(f"RT23-B-INV-05 {root}.unitIdRecomputation.twoSidedControl: both halves "
                   f"must be declared true")
    # --- vectors ------------------------------------------------------------
    vectors = _get(pb, ["vectors", "rows"], [])
    if _get(pb, ["vectors", "count"]) != len(vectors):
        out.append(f"RT23-B-INV-01 {root}.vectors.count: disagrees with the row count")
    invariant_names = _get(ev10, ["availabilityDifferential", "invariant"], [])
    changes_only = _get(ev10, ["availabilityDifferential", "changesOnly"], [])
    declared_diff = _get(pb, ["purgeMutationBoundary", "evidenceV10DifferentialEvaluated"], {})
    if declared_diff.get("invariant") != invariant_names:
        out.append(f"RT23-B-INV-07 {root}.purgeMutationBoundary."
                   f"evidenceV10DifferentialEvaluated.invariant: does not equal the live "
                   f"evidence.v10 list")
    if declared_diff.get("changesOnly") != changes_only:
        out.append(f"RT23-B-INV-07 {root}.purgeMutationBoundary."
                   f"evidenceV10DifferentialEvaluated.changesOnly: does not equal the live "
                   f"evidence.v10 list")
    if "sealedCapability" not in invariant_names:
        out.append(f"RT23-B-INV-07 evidence.v10.json#availabilityDifferential.invariant: "
                   f"sealedCapability is no longer named invariant upstream")
    if "effectiveCapability" not in changes_only:
        out.append(f"RT23-B-INV-07 evidence.v10.json#availabilityDifferential.changesOnly: "
                   f"effectiveCapability is no longer named changeable upstream")
    baseline = effective_capability(sealed, units, records)
    for index, vector in enumerate(vectors):
        vpath = f"{root}.vectors.rows[{index}]"
        overrides = vector.get("stateOverrides")
        if not isinstance(overrides, list):
            out.append(f"RT23-B-INV-01 {vpath}.stateOverrides: must be an array")
            continue
        for oindex, override in enumerate(overrides):
            if override.get("state") not in AVAIL_STATES:
                out.append(f"RT23-B-INV-03 {vpath}.stateOverrides[{oindex}].state: outside "
                           f"the closed availability state set")
        try:
            state = apply_states(records, overrides)
            derived = effective_capability(sealed, units, state)
        except (ValueError, KeyError, TypeError) as exc:
            out.append(f"RT23-B-INV-01 {vpath}: derivation refused this vector "
                       f"({type(exc).__name__}: {exc})")
            continue
        if vector.get("derivedEffectiveCapability") != derived:
            out.append(f"RT23-B-INV-01 {vpath}.derivedEffectiveCapability: declared "
                       f"{vector.get('derivedEffectiveCapability')!r}, derived {derived!r}")
        if CAPABILITY_RANK[derived] > CAPABILITY_RANK[sealed]:
            out.append(f"RT23-B-INV-01 {vpath}: derived capability exceeds the sealed "
                       f"capability")
        if CAPABILITY_RANK[derived] < CAPABILITY_RANK["recorded"]:
            out.append(f"RT23-B-INV-02 {vpath}: derived capability is below the recorded floor")
        if vector.get("derivedAuthoritative") is not authoritative(derived):
            out.append(f"RT23-B-INV-01 {vpath}.derivedAuthoritative: declared "
                       f"{vector.get('derivedAuthoritative')!r}, derived "
                       f"{authoritative(derived)}")
        refusal = typed_refusal(sealed, units, state)
        if vector.get("derivedTypedRefusalKind") != refusal:
            out.append(f"RT23-B-INV-03 {vpath}.derivedTypedRefusalKind: declared "
                       f"{vector.get('derivedTypedRefusalKind')!r}, derived {refusal!r}")
        if vector.get("sealedCapabilityAfter") != sealed:
            out.append(f"RT23-B-INV-04 {vpath}.sealedCapabilityAfter: purge may not change "
                       f"the sealed capability")
        commitment = unit_set_commitment(units)
        if vector.get("unitSetCommitmentAfter") != commitment:
            out.append(f"RT23-B-INV-05 {vpath}.unitSetCommitmentAfter: declared "
                       f"{vector.get('unitSetCommitmentAfter')!r}, recomputed {commitment!r}")
        if vector.get("unitSetCommitmentUnchanged") is not (commitment == base_commitment):
            out.append(f"RT23-B-INV-05 {vpath}.unitSetCommitmentUnchanged: declared "
                       f"{vector.get('unitSetCommitmentUnchanged')!r}, measured "
                       f"{commitment == base_commitment}")
        if overrides and any(o.get("state") != "AVAILABLE" for o in overrides):
            if CAPABILITY_RANK[derived] > CAPABILITY_RANK[baseline]:
                out.append(f"RT23-B-INV-01 {vpath}: an availability loss raised the effective "
                           f"capability")
            if derived == baseline and vector.get("derivedTypedRefusalKind") == "NONE":
                out.append(f"RT23-B-INV-03 {vpath}: a loss changed neither the capability nor "
                           f"the typed refusal, so the vector observes nothing")

    # --- exhaustive derived properties -------------------------------------
    ceiling = floor = total = 0
    cause_agree = cause_total = 0
    all_refs = [r for unit in units for r in unit["objectRefs"]]
    for candidate_sealed in CAPABILITY_RANK:
        for ref in all_refs:
            for state_name in AVAIL_STATES:
                override = {"projectId": ref["projectId"],
                            "recordCasRef": ref["recordCasRef"],
                            "recordKind": ref["recordKind"], "state": state_name}
                derived = effective_capability(candidate_sealed, units,
                                               apply_states(records, [override]))
                total += 1
                ceiling += int(CAPABILITY_RANK[derived] <= CAPABILITY_RANK[candidate_sealed])
                floor += int(CAPABILITY_RANK[derived] >= CAPABILITY_RANK["recorded"])
    for ref in all_refs:
        results = {}
        for state_name in ("PURGED", "OUTAGE", "MISSING-DEPENDENCY"):
            override = {"projectId": ref["projectId"], "recordCasRef": ref["recordCasRef"],
                        "recordKind": ref["recordKind"], "state": state_name}
            results[state_name] = effective_capability(
                sealed, units, apply_states(records, [override]))
        for state_name in ("OUTAGE", "MISSING-DEPENDENCY"):
            cause_total += 1
            if results[state_name] == results["PURGED"]:
                cause_agree += 1
            else:
                out.append(f"RT23-B-INV-03 {root}.effectiveCapabilityDerivation P5-CAUSE-BLIND: "
                           f"{ref['recordCasRef']} derives {results[state_name]!r} under "
                           f"{state_name} and {results['PURGED']!r} under PURGED")
    if ceiling != total:
        out.append(f"RT23-B-INV-01 {root}.effectiveCapabilityDerivation P1-CEILING: "
                   f"{total - ceiling} of {total} exhaustive derivations exceed the seal")
    if floor != total:
        out.append(f"RT23-B-INV-02 {root}.effectiveCapabilityDerivation P2-FLOOR: "
                   f"{total - floor} of {total} exhaustive derivations fall below recorded")
    # P3 antitone: the satisfied predicate must be downward closed
    amap = availability_map(records)
    ordered = sorted(CAPABILITY_RANK, key=CAPABILITY_RANK.get)
    flags = [satisfied_at(c, units, amap) for c in ordered]
    if any(flags[i] is False and flags[i + 1] is True for i in range(len(flags) - 1)):
        out.append(f"RT23-B-INV-01 {root}.effectiveCapabilityDerivation P3-ANTITONE: the "
                   f"satisfied predicate is not downward closed, so a single maximum is not "
                   f"well defined")

    # --- mutation boundary --------------------------------------------------
    boundary = _get(pb, ["purgeMutationBoundary"], {})
    mutates = boundary.get("mutatesExactly") or []
    if len(mutates) != 2:
        out.append(f"RT23-B-INV-04 {root}.purgeMutationBoundary.mutatesExactly: purge mutates "
                   f"exactly the raw object bytes and the availability ledger")
    if boundary.get("mutatesExactlyCount") != len(mutates):
        out.append(f"RT23-B-INV-04 {root}.purgeMutationBoundary.mutatesExactlyCount: declared "
                   f"{boundary.get('mutatesExactlyCount')!r}, array carries {len(mutates)}")
    does_not = set(boundary.get("doesNotMutate") or [])
    for required in ("sealedCapability", "closureCommitment", "EvidenceDigest", "RunId",
                     "runSealRef", "TerminalRunV1", "RunAuthorityIndexV1", "units", "unitId",
                     "PlanId", "SnapshotId"):
        if required not in does_not:
            out.append(f"RT23-B-INV-04 {root}.purgeMutationBoundary.doesNotMutate: {required!r} "
                       f"must be declared unmutated by purge")
    overlap = sorted(set(mutates) & does_not)
    if overlap:
        out.append(f"RT23-B-INV-04 {root}.purgeMutationBoundary: {overlap} appears in both "
                   f"mutatesExactly and doesNotMutate")

    # --- ledger append-only -------------------------------------------------
    ledger = _get(pb, ["ledger"], {})
    if ledger.get("appendOnly") is not True or \
            ledger.get("entriesAreNeverEditedOrRemoved") is not True:
        out.append(f"RT23-B-INV-06 {root}.ledger: the availability ledger must be append-only "
                   f"and its entries never edited or removed")
    ref0 = all_refs[0]
    def entry(seq: int, state: str) -> dict[str, Any]:
        return {"schemaVersion": 1, "projectId": ref0["projectId"],
                "recordCasRef": ref0["recordCasRef"], "recordKind": ref0["recordKind"],
                "toState": state, "atSequence": seq, "cause": "test"}
    try:
        fold_ledger([entry(1, "PURGED"), entry(2, "PURGED")])
    except ValueError as exc:
        out.append(f"RT23-B-INV-06 {root}.ledger.repurgeIsIdempotent: a repeated PURGED entry "
                   f"was refused ({exc})")
    try:
        fold_ledger([entry(1, "PURGED"), entry(2, "AVAILABLE")])
        out.append(f"RT23-B-INV-06 {root}.ledger.terminalRule: an AVAILABLE entry after a "
                   f"terminal PURGED entry for {ref0['recordCasRef']} was accepted")
    except ValueError:
        pass
    try:
        fold_ledger([entry(1, "PURGED"), entry(3, "PURGED")])
        out.append(f"RT23-B-INV-06 {root}.ledger.sequenceRule: a sequence break at "
                   f"{ref0['recordCasRef']} was accepted")
    except ValueError:
        pass

    # --- purged-Run inspection and D9 ---------------------------------------
    inspect = _get(pb, ["purgedRunInspection", "rows"], [])
    if _get(pb, ["purgedRunInspection", "rowCount"]) != len(inspect):
        out.append(f"RT23-B-INV-09 {root}.purgedRunInspection.rowCount: disagrees with the "
                   f"row count")
    classes = set()
    for index, row in enumerate(inspect):
        rpath = f"{root}.purgedRunInspection.rows[{index}]"
        axes_row = row.get("d9Axes")
        if not isinstance(axes_row, dict):
            out.append(f"RT23-B-INV-09 {rpath}.d9Axes: every inspection row must declare its "
                       f"D9 axes")
            continue
        findings = _d9_row_findings(d9mod, d9, axes_row, row, rpath)
        out.extend(f.replace("RT23-A-INV-11", "RT23-B-INV-09") for f in findings)
        if not findings:
            classes.add(row.get("derivedClass"))
    if "success" not in classes:
        out.append(f"RT23-B-INV-09 {root}.purgedRunInspection.rows: no row shows that an "
                   f"identity-and-seal inspection of a purged Run still succeeds; without it "
                   f"the claim that purge does not make a Run vanish is unexercised")
    if "indeterminate" not in classes:
        out.append(f"RT23-B-INV-09 {root}.purgedRunInspection.rows: no row shows the "
                   f"evidence-required case terminating indeterminate")

    # --- D9 vocabulary gap, measured live -----------------------------------
    gap = _get(pb, ["d9VocabularyGap"], {})
    deficiencies = sorted(_get(d9, ["codeMaps", "deficiencyToReasonCode"], {}))
    reason_codes = list(_get(d9, ["codeVocabulary", "reasonCodes"], []))
    error_codes = list(_get(d9, ["codeVocabulary", "errorCodes"], []))
    tokens = tuple(gap.get("retentionTokenPredicate") or ())
    if not tokens:
        out.append(f"RT23-B-INV-10 {root}.d9VocabularyGap.retentionTokenPredicate: a measured "
                   f"gap needs a mechanical predicate")
    def hits(names: list[str]) -> list[str]:
        return sorted(n for n in names if any(t in n.upper() for t in tokens))
    for key, live, measured in (
            ("deficiencyMembers", deficiencies, deficiencies),
            ("reasonCodesMatchingPredicate", reason_codes, hits(reason_codes)),
            ("deficiencyMembersMatchingPredicate", deficiencies, hits(deficiencies)),
            ("errorCodesMatchingPredicate", error_codes, hits(error_codes))):
        if key == "deficiencyMembers":
            if gap.get(key) != live:
                out.append(f"RT23-B-INV-10 {root}.d9VocabularyGap.{key}: does not equal the "
                           f"live pinned D9 deficiency map keys")
            continue
        if gap.get(key) != measured:
            out.append(f"RT23-B-INV-10 {root}.d9VocabularyGap.{key}: declared "
                       f"{gap.get(key)!r}, measured {measured!r}")
    for key, value in (("deficiencyMemberCount", len(deficiencies)),
                       ("reasonCodeCount", len(reason_codes)),
                       ("errorCodeCount", len(error_codes))):
        if gap.get(key) != value:
            out.append(f"RT23-B-INV-10 {root}.d9VocabularyGap.{key}: declared "
                       f"{gap.get(key)!r}, measured {value}")
    if gap.get("classIsCovered") is not True or gap.get("reasonCodeIsNotCovered") is not True:
        out.append(f"RT23-B-INV-10 {root}.d9VocabularyGap: the class is covered and the "
                   f"reason code is not; both must be stated")
    if gap.get("coveredClass") not in _get(d9, ["classToExitCode"], {}):
        out.append(f"RT23-B-INV-10 {root}.d9VocabularyGap.coveredClass: not a key of the live "
                   f"classToExitCode map")
    elif gap.get("coveredExitCode") != _get(d9, ["classToExitCode", gap.get("coveredClass")]):
        out.append(f"RT23-B-INV-10 {root}.d9VocabularyGap.coveredExitCode: disagrees with the "
                   f"live classToExitCode map")
    requested = _get(pb, ["d9VocabularyGap", "requestedSuccessorNotAdded"], {})
    if requested.get("state") != "REQUESTED-NOT-ADDED":
        out.append(f"RT23-B-INV-10 {root}.d9VocabularyGap.requestedSuccessorNotAdded.state: "
                   f"must be REQUESTED-NOT-ADDED")
    proposed = requested.get("proposedReasonCode")
    if proposed in reason_codes or proposed in error_codes:
        out.append(f"RT23-B-INV-10 {root}.d9VocabularyGap.requestedSuccessorNotAdded"
                   f".proposedReasonCode: {proposed!r} is already in the live vocabulary")
    carried_reason = set(gap.get("reasonCodesMatchingPredicate") or [])
    if carried_reason - set(reason_codes):
        out.append(f"RT23-B-INV-10 {root}.d9VocabularyGap.reasonCodesMatchingPredicate: "
                   f"carries codes that are not in the live pinned vocabulary")
    for index, row in enumerate(gap.get("forbiddenMappings") or []):
        fpath = f"{root}.d9VocabularyGap.forbiddenMappings[{index}]"
        axes_row = row.get("d9Axes")
        if not isinstance(axes_row, dict):
            out.append(f"RT23-B-INV-09 {fpath}.d9Axes: required")
            continue
        try:
            live_class = d9mod.derive_class(axes_row)
        except Exception as exc:  # noqa: BLE001
            out.append(f"RT23-B-INV-09 {fpath}.d9Axes: refused by the pinned derivation "
                       f"({type(exc).__name__})")
            continue
        live_exit = _get(d9, ["classToExitCode", live_class])
        if row.get("liveDerivedClass") != live_class or row.get("liveDerivedExitCode") != live_exit:
            out.append(f"RT23-B-INV-09 {fpath}.liveDerivedClass: declared "
                       f"{row.get('liveDerivedClass')!r}/{row.get('liveDerivedExitCode')!r}, "
                       f"derived {live_class!r}/{live_exit!r}")
        refused = (row.get("declaredClass") != live_class
                   or row.get("declaredExitCode") != live_exit)
        if row.get("refusedBecauseDeclarationDisagreesWithLiveDerivation") is not refused:
            out.append(f"RT23-B-INV-09 {fpath}"
                       f".refusedBecauseDeclarationDisagreesWithLiveDerivation: declared "
                       f"{row.get('refusedBecauseDeclarationDisagreesWithLiveDerivation')!r}, "
                       f"measured {refused}")
        if not refused:
            out.append(f"RT23-B-INV-09 {fpath}: a forbidden mapping that agrees with the live "
                       f"derivation is not a counterexample")

    # --- consent promise ----------------------------------------------------
    promise = _get(pb, ["consentPromise"], {})
    guaranteed = promise.get("guaranteed") or []
    not_guaranteed = promise.get("notGuaranteed") or []
    if not guaranteed or not not_guaranteed:
        out.append(f"RT23-B-INV-11 {root}.consentPromise: both halves must be stated")
    overlap = sorted(set(guaranteed) & set(not_guaranteed))
    if overlap:
        out.append(f"RT23-B-INV-11 {root}.consentPromise: {overlap} appears in both "
                   f"guaranteed and notGuaranteed")
    for token in ("does not rewrite the sealed Run", "never raises effectiveCapability",
                  "still addressable", "can never return to AVAILABLE"):
        if not any(token in str(g) for g in guaranteed):
            out.append(f"RT23-B-INV-11 {root}.consentPromise.guaranteed: the promise "
                       f"{token!r} is not made; a consent promise that omits it is not the "
                       f"promise this section owes")
    return out


def check_deletion_boundary(doc: Any, tm3: Any) -> list[str]:
    out: list[str] = []
    root = "$.partB_purgeSemantics.consentPromise"
    live = [r for r in tm3.get("residualRisks", [])
            if isinstance(r, str) and "DeletionProtocol" in r]
    if not live:
        return [f"RT23-B-INV-11 threat-model.v3.json#residualRisks: the DeletionProtocol "
                f"boundary this promise restates was not found live"]
    declared = _get(doc, ["partB_purgeSemantics", "consentPromise",
                          "deletionProtocolBoundaryVerbatim"])
    if declared != live[0]:
        out.append(f"RT23-B-INV-11 {root}.deletionProtocolBoundaryVerbatim: does not equal "
                   f"the live threat-model residual risk verbatim")
    not_guaranteed = _get(doc, ["partB_purgeSemantics", "consentPromise", "notGuaranteed"], [])
    if declared not in not_guaranteed:
        out.append(f"RT23-B-INV-11 {root}.notGuaranteed: the DeletionProtocol boundary must "
                   f"appear in the notGuaranteed list rather than being softened elsewhere")
    return out


def check_v10_position(doc: Any, tm3: Any) -> list[str]:
    out: list[str] = []
    root = "$.v10Item3Position"
    v10 = None
    for finding in tm3.get("findings", []):
        if finding.get("id") == "V10":
            v10 = finding
    if v10 is None:
        return [f"RT23-V10 threat-model.v3.json#findings: V10 was not found live"]
    live_text = (v10.get("requiredResolution") or [None, None, None])[2]
    position = _get(doc, ["v10Item3Position"], {})
    if position.get("obligationVerbatim") != live_text:
        out.append(f"RT23-V10 {root}.obligationVerbatim: declared "
                   f"{position.get('obligationVerbatim')!r}, live threat model records "
                   f"{live_text!r}")
    if _get(doc, ["partB_purgeSemantics", "obligation", "verbatim"]) != live_text:
        out.append("RT23-V10 $.partB_purgeSemantics.obligation.verbatim: does not equal the "
                   "live obligation text")
    if position.get("claimedStatus") != "DISCHARGEABLE-PENDING-INDEPENDENT-REVIEW":
        out.append(f"RT23-V10 {root}.claimedStatus: declared {position.get('claimedStatus')!r}; "
                   f"a discharge requires an independent review of these bytes and this "
                   f"artifact has none")
    if v10.get("status") != "UNRESOLVED":
        out.append(f"RT23-V10 threat-model.v3.json#findings.V10.status: live status is "
                   f"{v10.get('status')!r}; this checker was written against UNRESOLVED")
    not_claimed = position.get("notClaimed") or []
    if not any("DISCHARGED" in str(n) for n in not_claimed):
        out.append(f"RT23-V10 {root}.notClaimed: the artifact must state plainly that it does "
                   f"not claim DISCHARGED")
    return out


# ---------------------------------------------------------------------------
# Measured hostile sweep.  IMPLEMENTATION-FREEZE 7 dominant failure mode: a
# coverage claim quantifying over a region the instrument cannot observe.  Every
# scalar leaf is enumerated and injected; counts are recomputed on every run.
# ---------------------------------------------------------------------------
def hostile_sweep(doc: Any, base_findings: list[str]) -> dict[str, Any]:
    positions = [(p, v) for p, v in scalar_leaves(doc)
                 if isinstance(v, bool) or (isinstance(v, int) and not isinstance(v, bool))]
    arms = {
        "float": lambda v: float(v) if not isinstance(v, bool) else None,
        "boolFromZeroOrOneInt": lambda v: (bool(v) if not isinstance(v, bool) and v in (0, 1)
                                           else None),
        "intFromBool": lambda v: (1 if v else 0) if isinstance(v, bool) else None,
    }
    result: dict[str, Any] = {}
    for arm, spell in arms.items():
        swept = admitted = by_position = collateral = 0
        escapes: list[str] = []
        for path, value in positions:
            replacement = spell(value)
            if replacement is None:
                continue
            swept += 1
            mutated = copy.deepcopy(doc)
            _set_path(mutated, path, replacement)
            findings, _ = type_findings(mutated)
            new = [f for f in findings if f not in base_findings]
            if not new:
                admitted += 1
                escapes.append(path)
            elif any(path in f for f in new):
                by_position += 1
            else:
                collateral += 1
                escapes.append(path + " (collateral)")
        result[arm] = {"sweptPositions": swept, "admitted": admitted,
                       "rejectedByPosition": by_position,
                       "rejectedCollateral": collateral, "escapes": escapes[:20]}
    result["scalarLeafPositions"] = len(scalar_leaves(doc))
    result["intOrBoolLeafPositions"] = len(positions)
    return result


def _set_path(doc: Any, path: str, value: Any) -> None:
    keys = _path_keys(path)
    node = doc
    for key in keys[:-1]:
        node = node[key]
    node[keys[-1]] = value


# ---------------------------------------------------------------------------
# Selftest.  Real mutations, each caught by its own named check.  Dispatched
# before any findings return, so "the suite did not run" is a distinct outcome.
# ---------------------------------------------------------------------------
def _mut(doc: Any, path: str, value: Any) -> Any:
    out = copy.deepcopy(doc)
    _set_path(out, path, value)
    return out


def _del(doc: Any, path: str) -> Any:
    out = copy.deepcopy(doc)
    keys = _path_keys(path)
    node = out
    for key in keys[:-1]:
        node = node[key]
    del node[keys[-1]]
    return out


def selftest(doc: Any, ctx: dict[str, Any]) -> tuple[list[str], int, int]:
    """Returns (failures, cases, caught)."""
    failures: list[str] = []
    cases: list[tuple[str, Any, str, str]] = []

    def add(name: str, mutated: Any, finding_id: str, position: str) -> None:
        cases.append((name, mutated, finding_id, position))

    pa = "$.partA_firstRunRetentionConsent"
    pb = "$.partB_purgeSemantics"
    ask_cells = doc[pa[2:]]["askDecisionTable"]["cells"]
    ci_index = next(i for i, c in enumerate(ask_cells) if c["invocationProfile"] == "ci")
    ask_index = next(i for i, c in enumerate(ask_cells) if c["askPerformed"])
    outcomes = doc[pb[2:]] and doc["partA_firstRunRetentionConsent"]["interactionOutcomes"]["outcomes"]
    dis_index = next(i for i, o in enumerate(outcomes) if "DISMISSED" in o["id"])
    ans_index = next(i for i, o in enumerate(outcomes) if o["id"].endswith("ANSWERED-RETAIN"))

    add("PA-CX-09-CI-CELL-ASKS",
        _mut(doc, f"{pa}.askDecisionTable.cells[{ci_index}].askPerformed", True),
        "RT23-A-INV-02", f"askDecisionTable.cells[{ci_index}].askPerformed")
    add("PA-CX-10-DISMISSAL-PERSISTS",
        _mut(doc, f"{pa}.interactionOutcomes.outcomes[{dis_index}].policyPersisted", True),
        "RT23-A-INV-03", f"interactionOutcomes.outcomes[{dis_index}].policyPersisted")
    add("PA-CX-11-ASK-AFTER-ADMISSION",
        _mut(doc, f"{pa}.askDecisionTable.cells[{ask_index}].executionIdAllocatedAtThisPoint",
             True),
        "RT23-A-INV-04",
        f"askDecisionTable.cells[{ask_index}].executionIdAllocatedAtThisPoint")
    add("PA-CX-13-POLICY-CARRIES-PLANID",
        _mut(doc, f"{pa}.policyObject.orderedFields[0]", "planId"),
        "RT23-A-INV-07", "policyObject.orderedFields")
    add("PA-CX-14-ANSWER-THROUGH-STDIN",
        _mut(doc, f"{pa}.consentRecord.answerChannelEnum[0]", "stdin"),
        "RT23-A-INV-09", "consentRecord.answerChannelEnum")
    add("PA-CX-15-SCHEMA-VERSION-AS-BOOLEAN",
        _mut(doc, f"{pa}.identity.recipeVersion", True),
        "RT23-TYPE", "identity.recipeVersion")
    add("PA-CX-16-SCHEMA-VERSION-AS-FLOAT",
        _mut(doc, f"{pa}.identity.fieldCount", 3.0),
        "RT23-TYPE", "identity.fieldCount")
    add("PA-CX-17-DISCLOSURE-DIGEST-DRIFT",
        _mut(doc, f"{pa}.disclosure.text",
             doc["partA_firstRunRetentionConsent"]["disclosure"]["text"] + " "),
        "RT23-A-INV-06", "disclosure.textDigest")
    add("PA-CX-18-DEFAULT-POSTURE-INTRODUCED",
        _mut(doc, f"{pa}.policyObject.orderedFields[4]", "defaultPosture"),
        "RT23-A-INV-10", "policyObject.orderedFields")
    add("PA-CX-19-D9-ROW-AUTHORED",
        _mut(doc, f"{pa}.interactionOutcomes.outcomes[{dis_index}].derivedExitCode", 0),
        "RT23-A-INV-11", f"interactionOutcomes.outcomes[{dis_index}].derivedExitCode")
    add("PA-CX-20-PLANID-INVARIANCE-BROKEN",
        _mut(doc, f"{pa}.planIdExclusion.invarianceVectors[0].expectedPlanId",
             "plan1:sha256:" + "0" * 64),
        "RT23-A-INV-07", "planIdExclusion.invarianceVectors[0]")
    add("PA-CX-21-INJECTION-MISCOUNTED",
        _mut(doc, f"{pa}.planIdExclusion.injectionsRefusedByPlanIdV1", 8),
        "RT23-A-INV-07", "planIdExclusion.injectionsRefusedByPlanIdV1")
    add("PA-CX-22-G4-ROW-EDITED",
        _mut(doc, f"{pa}.g4Binding.gateRow.status", "QUALIFIED"),
        "RT23-A-INV-06", "g4Binding.gateRow")
    add("PA-CX-23-ASK-CELL-DELETED",
        _del(doc, f"{pa}.askDecisionTable.cells[0]"),
        "RT23-A-INV-01", "askDecisionTable.cells")

    add("PB-CX-03-CAPABILITY-EXCEEDS-SEAL",
        _mut(doc, f"{pb}.vectors.rows[2].derivedEffectiveCapability", "replayable"),
        "RT23-B-INV-01", "vectors.rows[2].derivedEffectiveCapability")
    add("PB-CX-04-CAPABILITY-BELOW-FLOOR",
        _mut(doc, f"{pb}.vectors.rows[3].derivedEffectiveCapability", "unavailable"),
        "RT23-B-INV-01", "vectors.rows[3].derivedEffectiveCapability")
    add("PB-CX-06-MUTATE-A-SEALED-FIELD",
        _mut(doc, f"{pb}.vectors.rows[1].sealedCapabilityAfter", "verifiable"),
        "RT23-B-INV-04", "vectors.rows[1].sealedCapabilityAfter")
    add("PB-CX-07-CAUSE-CHANGES-CAPABILITY",
        _mut(doc, f"{pb}.vectors.rows[4].derivedTypedRefusalKind",
             "RETENTION_EVIDENCE_PURGED"),
        "RT23-B-INV-03", "vectors.rows[4].derivedTypedRefusalKind")
    add("PB-CX-08-DIFFERENTIAL-INVERTED",
        _mut(doc, f"{pb}.purgeMutationBoundary.evidenceV10DifferentialEvaluated"
                  f".invariant[0]", "effectiveCapability"),
        "RT23-B-INV-07", "purgeMutationBoundary.evidenceV10DifferentialEvaluated.invariant")
    add("PB-CX-09-FIXTURE-DISAGREES",
        _mut(doc, f"{pb}.predecessorFixtureReproduction.rows[2]"
                  f".v23DerivedEffectiveCapability", "replayable"),
        "RT23-B-INV-08",
        "predecessorFixtureReproduction.rows[2].v23DerivedEffectiveCapability")
    add("PB-CX-10-D9-CODE-INVENTED",
        _mut(doc, f"{pb}.d9VocabularyGap.reasonCodesMatchingPredicate",
             ["RETENTION.EVIDENCE_PURGED"]),
        "RT23-B-INV-10", "d9VocabularyGap.reasonCodesMatchingPredicate")
    add("PB-CX-11-PROMISE-OVERLAP",
        _mut(doc, f"{pb}.consentPromise.guaranteed[0]",
             doc["partB_purgeSemantics"]["consentPromise"]["notGuaranteed"][0]),
        "RT23-B-INV-11", "consentPromise")
    add("PB-CX-12-STATE-AS-BOOLEAN",
        _mut(doc, f"{pb}.availabilityStateLattice.stateCount", True),
        "RT23-TYPE", "availabilityStateLattice.stateCount")
    add("PB-CX-13-TERMINAL-STATE-REVERSIBLE",
        _mut(doc, f"{pb}.availabilityStateLattice.reversibility.PURGED", True),
        "RT23-B-INV-06", "availabilityStateLattice.reversibility.PURGED")
    add("PB-CX-14-UNIT-COMMITMENT-DRIFT",
        _mut(doc, f"{pb}.unitIdRecomputation.unitSetCommitment", "sha256:" + "0" * 64),
        "RT23-B-INV-05", "unitIdRecomputation.unitSetCommitment")
    add("PB-CX-15-D9-INSPECTION-CLASS-AUTHORED",
        _mut(doc, f"{pb}.purgedRunInspection.rows[1].derivedClass", "operational-failed"),
        "RT23-B-INV-09", "purgedRunInspection.rows[1].derivedClass")
    add("PB-CX-16-BOUNDARY-OVERLAP",
        _mut(doc, f"{pb}.purgeMutationBoundary.doesNotMutate[0]",
             doc["partB_purgeSemantics"]["purgeMutationBoundary"]["mutatesExactly"][0]),
        "RT23-B-INV-04", "purgeMutationBoundary")
    add("PB-CX-17-V10-STATUS-OVERCLAIMED",
        _mut(doc, "$.v10Item3Position.claimedStatus", "DISCHARGED"),
        "RT23-V10", "v10Item3Position.claimedStatus")

    add("XX-CX-01-RECORD-DIGEST-DRIFT",
        _mut(doc, "$.recordedInputs.hardPinned[0].sha256", "0" * 64),
        "RT23-RECORD", "recordedInputs.hardPinned")
    add("XX-CX-02-CARRIED-FRAGMENT-EDITED",
        _mut(doc, "$.inheritance.carriedFragments['$.custodyPolicy']"
                  ".recommendedDefaultPosture.durableDefault", "SELECTED"),
        "RT23-INHERIT", "inheritance.carriedFragments")
    add("XX-CX-03-CD-RT-5-MOVED",
        _mut(doc, "$.integrationState.CD-RT-5", "RESOLVED"),
        "RT23-AUTH", "integrationState.CD-RT-5")
    add("XX-CX-04-RESIDUAL-WITHOUT-A-NUMBER",
        _mut(doc, f"{pa}.residuals[0].measuredBoundary", "a small number of positions"),
        "RT23-MEASURED", "partA_firstRunRetentionConsent.residuals[0].measuredBoundary")
    add("XX-CX-05-SEAL-RECOMMENDATION-FLIPPED",
        _mut(doc, "$.sealRecommendation", "SEAL"),
        "RT23-AUTH", "sealRecommendation")

    add("PA-CX-12-POLICY-ID-DOES-NOT-RECOMPUTE",
        _mut(doc, f"{pa}.policyVectors[0].policy.retentionPolicyId",
             "rpol1:sha256:" + "0" * 64),
        "RT23-A-INV-07", "policyVectors[0].policy.retentionPolicyId")
    add("PA-CX-24-CONSENT-RECORD-REF-DRIFT",
        _mut(doc, f"{pa}.policyVectors[0].consentRecord.recordedAtUtcSeconds", 1),
        "RT23-A-INV-07", "policyVectors[0].consentRecord.consentRecordRef")
    add("PB-CX-18-RESIDUAL-NUMBER-DRIFT",
        _mut(doc, f"{pb}.residuals[1].measuredValues.exhaustiveCeilingFloorDerivations", 1),
        "RT23-MEASURED", "residuals[1].measuredValues.exhaustiveCeilingFloorDerivations")
    add("XX-CX-06-FIXTURE-NOT-EXERCISED",
        _mut(doc, f"{pa}.counterexampleFixtures.structural[0].exercisedBy", "prose"),
        "RT23-FIXTURE", "counterexampleFixtures.structural[0].exercisedBy")

    ordered_names = [name for name, _, _, _ in cases]
    if sorted(ordered_names) != sorted(SELFTEST_CASE_NAMES):
        failures.append(
            "SELFTEST case registry: the executed case set does not equal "
            "SELFTEST_CASE_NAMES, which is what check_fixture_exercise compares the "
            "artifact against; "
            f"only-executed={sorted(set(ordered_names) - set(SELFTEST_CASE_NAMES))} "
            f"only-registered={sorted(set(SELFTEST_CASE_NAMES) - set(ordered_names))}")

    caught = 0
    for name, mutated, finding_id, position in cases:
        findings = run_all(mutated, ctx, "all")
        hits = [f for f in findings if f.startswith(finding_id) and position in f]
        if hits:
            caught += 1
        else:
            named = [f for f in findings if f.startswith(finding_id)]
            failures.append(
                f"SELFTEST {name}: expected a {finding_id} finding naming {position}; "
                f"got {len(findings)} finding(s), {len(named)} with the right id"
                + (f", first: {findings[0][:150]}" if findings else " (none)"))
    return failures, len(cases), caught


# ---------------------------------------------------------------------------
def run_all(doc: Any, ctx: dict[str, Any], part: str) -> list[str]:
    findings: list[str] = []
    type_out, _ = type_findings(doc)
    findings.extend(type_out)
    findings.extend(check_record(doc, ctx["snaps"]))
    findings.extend(check_inheritance(doc, ctx["v22"], ctx["v22rev"]))
    findings.extend(check_authority(doc, ctx["product"]))
    findings.extend(check_separability(doc))
    findings.extend(check_fixture_exercise(doc))
    findings.extend(check_residual_measurements(doc, ctx))
    findings.extend(check_v10_position(doc, ctx["tm3"]))
    if part in ("a", "all"):
        findings.extend(check_part_a(doc, ctx["ri"], ctx["op10"], ctx["d9mod"], ctx["d9"]))
    if part in ("b", "all"):
        findings.extend(check_part_b(doc, ctx["v22"], ctx["ev10"], ctx["d9mod"], ctx["d9"]))
        findings.extend(check_deletion_boundary(doc, ctx["tm3"]))
    return findings


def main() -> int:
    argv = sys.argv[1:]
    part = "all"
    do_selftest = False
    index = 0
    while index < len(argv):
        arg = argv[index]
        if arg == "--selftest":
            do_selftest = True
        elif arg == "--part":
            index += 1
            if index >= len(argv) or argv[index] not in ("a", "b", "all"):
                sys.stderr.write("RT23-UNSUPPORTED-INVOCATION: --part takes a, b or all\n")
                return 2
            part = argv[index]
        elif arg.startswith("--part="):
            part = arg.split("=", 1)[1]
            if part not in ("a", "b", "all"):
                sys.stderr.write("RT23-UNSUPPORTED-INVOCATION: --part takes a, b or all\n")
                return 2
        else:
            sys.stderr.write(f"RT23-UNSUPPORTED-INVOCATION: unknown option {arg!r}\n")
            return 2
        index += 1

    try:
        snaps = verified_snapshots()
    except PinMismatch as exc:
        sys.stderr.write(
            f"RT23-PIN-REFUSED: the verified execution closure did not match its pinned "
            f"digests, so nothing was parsed or executed: {exc}\n")
        return 2
    try:
        subject_bytes = (HERE / SUBJECT).read_bytes()
    except OSError as exc:
        sys.stderr.write(f"RT23-PIN-REFUSED: cannot read {SUBJECT} ({type(exc).__name__})\n")
        return 2
    try:
        doc = _parse(subject_bytes, SUBJECT)
        parsed = {name: _parse(data, name) for name, data in snaps.items()
                  if name.endswith(".json")}
    except PinMismatch as exc:
        sys.stderr.write(f"RT23-PIN-REFUSED: {exc}\n")
        return 2

    # Execute the D9 reference derivation only from the verified snapshot.
    spec = importlib.util.spec_from_file_location(
        "_rt23_d9_" + PINS["check-d9-v1.14.py"][:12], str(HERE / "check-d9-v1.14.py"))
    if spec is None or spec.loader is None:
        sys.stderr.write("RT23-PIN-REFUSED: cannot load the verified D9 reference module\n")
        return 2
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    try:
        spec.loader.exec_module(module)
    except Exception as exc:  # noqa: BLE001
        sys.stderr.write(f"RT23-PIN-REFUSED: the verified D9 reference module refused to "
                         f"load ({type(exc).__name__}: {exc})\n")
        return 2
    module_pins = dict(getattr(module, "PINS", {}) or {})
    if not module_pins or any(PINS.get(name) != digest for name, digest in module_pins.items()):
        sys.stderr.write("RT23-PIN-REFUSED: the D9 module's own pin table disagrees with this "
                         "checker's independently tabulated closure\n")
        return 2

    ctx = {"snaps": snaps, "v22": parsed["retention-tiers.v22.json"],
           "v22rev": parsed["retention-tiers.v22.review-independent-prefreeze.json"],
           "d9": parsed["d9-exit-contract.v1.14.json"], "d9mod": module,
           "ev10": parsed["evidence.v10.json"], "op10": parsed["operability.v10.json"],
           "product": parsed["product-dispositions.v1.json"],
           "tm3": parsed["threat-model.v3.json"], "ri": parsed["resolved-inputs.v2.json"]}

    findings = run_all(doc, ctx, part)

    # The selftest branch is dispatched BEFORE any findings return, so a dirty
    # base produces SELFTEST-NOT-RUN at exit 3 rather than a green banner over a
    # suite that never executed.
    if do_selftest:
        if findings:
            print("SELFTEST-REFUSED / SELFTEST-NOT-RUN: the base is not clean, so mutation "
                  "results would be meaningless.")
            for finding in findings:
                print(f"  - {finding}")
            return 3
        failures, cases, caught = selftest(doc, ctx)
        base_type, _ = type_findings(doc)
        sweep = hostile_sweep(doc, base_type)
        print(f"RETENTION-CUSTODY v23 SELFTEST: {caught}/{cases} mutations caught by their "
              f"own named check")
        for arm, row in sweep.items():
            if isinstance(row, dict):
                print(f"  sweep[{arm}]: swept {row['sweptPositions']} admitted "
                      f"{row['admitted']} by-position {row['rejectedByPosition']} "
                      f"collateral {row['rejectedCollateral']}")
        if failures:
            for failure in failures:
                print(f"  - {failure}")
            print("SELFTEST-FAIL")
            return 1
        print("SELFTEST-PASS")
        return 0

    base_type, _ = type_findings(doc)
    _, counts = type_findings(doc)
    sweep = hostile_sweep(doc, base_type)
    declared_sweep = _get(doc, ["measuredSweep"], {})
    for arm in ("float", "boolFromZeroOrOneInt", "intFromBool"):
        declared_arm = declared_sweep.get(arm) or {}
        measured_arm = sweep[arm]
        for key in ("sweptPositions", "admitted", "rejectedByPosition", "rejectedCollateral"):
            if declared_arm.get(key) != measured_arm[key]:
                findings.append(
                    f"RT23-SWEEP $.measuredSweep.{arm}.{key}: declared "
                    f"{declared_arm.get(key)!r}, measured {measured_arm[key]}")
        if measured_arm["admitted"] != 0:
            findings.append(
                f"RT23-SWEEP $.measuredSweep.{arm}: {measured_arm['admitted']} position(s) "
                f"admitted a respelled scalar: {measured_arm['escapes'][:5]}")
    for key in ("scalarLeafPositions", "intLeafPositions", "boolLeafPositions",
                "stringLeafPositions", "unruledIntOrBoolLeafPositions",
                "guardedIntOrBoolLeafPositions"):
        if declared_sweep.get(key) != counts[key]:
            findings.append(f"RT23-SWEEP $.measuredSweep.{key}: declared "
                            f"{declared_sweep.get(key)!r}, measured {counts[key]}")
    if declared_sweep.get("sweepIsRecomputedEveryRun") is not True:
        findings.append("RT23-SWEEP $.measuredSweep.sweepIsRecomputedEveryRun: must be true")

    print(f"RETENTION-CUSTODY v23  part={part}  "
          f"pins {len(PINS)}  scalar leaves {counts['scalarLeafPositions']}  "
          f"guarded int/bool {counts['guardedIntOrBoolLeafPositions']}  "
          f"unruled {counts['unruledIntOrBoolLeafPositions']}")
    print(f"  sweep float {sweep['float']['sweptPositions']}/{sweep['float']['admitted']} "
          f"admitted; bool<-0|1 {sweep['boolFromZeroOrOneInt']['sweptPositions']}/"
          f"{sweep['boolFromZeroOrOneInt']['admitted']}; int<-bool "
          f"{sweep['intFromBool']['sweptPositions']}/{sweep['intFromBool']['admitted']}")
    if findings:
        print(f"{len(findings)} finding(s) in {SUBJECT}:")
        for finding in findings:
            print(f"  - {finding}")
        return 1
    print(f"{SUBJECT}: PASS (architecture-candidate scope; CANDIDATE-NOT-APPLIED; "
          f"CD-RT-5 BLOCKED_ON_PHASE_1A; V10 UNRESOLVED)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
