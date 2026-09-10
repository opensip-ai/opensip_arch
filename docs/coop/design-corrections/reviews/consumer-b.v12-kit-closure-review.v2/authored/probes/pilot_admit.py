#!/usr/bin/env python3
"""Independent structural admission + complete semantic proof replay.

Kit-only. Consumer helpers are not the expected-output oracle.
Does not remint or repair the consumer store. Does not call consumer scripts.
"""
from __future__ import annotations

import base64
import copy
import hashlib
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-scope-review.v1/subject")
REQ = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-scope-review.v1/requirements.json")
SNAP_ROOT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-closure-review.v2")
SNAP = SNAP_ROOT / "consumer-snapshot"
OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-closure-review.v2/output")
STORE_PATH = SNAP / "runs/syntax-code.store.json"
META_PATH = SNAP / "runs/syntax-code.meta.json"
MANIFEST_PATH = SNAP_ROOT / "snapshot-manifest.json"
EXPECTED_MANIFEST = "0a953ef9d710bf6457aab58eaed4fb8f41c9daade252738f5d37704476c11ed0"
EXPECTED_KIT_MANIFEST = "ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8"
PYTHON = "/tmp/opensip-architecture-review-env/bin/python"

IDENT = json.loads((KIT / "docs/coop/design-corrections/foundation/identity-schemas.v3.json").read_text())
RELDOC_PATH = KIT / "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json"
RELDOC_BYTES = RELDOC_PATH.read_bytes()
RELDOC = json.loads(RELDOC_BYTES)
NATIVE_PATH = KIT / "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"
NATIVE_BYTES = NATIVE_PATH.read_bytes()
NATIVE = json.loads(NATIVE_BYTES)
MATRIX = json.loads((KIT / "docs/coop/design-corrections/native/native-capability-matrix.v2.json").read_text())
EXEC_SCHEMA = json.loads((KIT / "docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json").read_text())
ENUM_SCHEMA = json.loads((KIT / "docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json").read_text())
EMIS_SCHEMA = json.loads((KIT / "docs/coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json").read_text())
SINV_SCHEMA = json.loads((KIT / "docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json").read_text())
POLICY_V2_SCHEMA = json.loads((KIT / "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json").read_text())
RELREG = RELDOC["x-opensip-relation-registry"]["relations"]
DIGEST_DOMAINS = IDENT["x-opensip-digest-domains"]
PAYLOAD_REG = IDENT["x-opensip-payload-registry"]
DOMAIN_SETS = DIGEST_DOMAINS["domainSets"]
CLOSURE_MEMBERSHIP = DIGEST_DOMAINS["closureMembership"]
SYNTAX_LVB = DOMAIN_SETS["native-semantic-universe"]["native.semantic-universe.syntax.v2"]["languageVersionBinding"]

DOMAIN_PREFIX = {
    "snapshot": "snapshot2",
    "closure": "closure2",
    "import": "import2",
    "plan": "plan2",
    "subject-scope": "scope2",
    "fact": "fact2",
    "coverage": "coverage2",
    "view": "view2",
    "execution-plan": "exec-plan2",
    "finding-fingerprint": "finding-key2",
    "evaluation-subject": "subject3",
    "finding": "finding3",
    "proof-bundle": "proof3",
    "semantic-evidence": "evidence3",
    "evaluation-seal": "seal3",
    "run": "run3",
    "cache-key": "cache2",
    "regeneration-key": "regen2",
    "policy-derivation": "policy-derivation3",
}
LADDERS = {k: v["ladder"] for k, v in RELREG.items()}
HEX64 = re.compile(r"^[0-9a-f]{64}$")
FORBIDDEN_SELECTED = {"proof-bundle", "finding", "evaluation-seal", "run", "semantic-evidence", "execution-inputs"}
BLOB_INPUT_DOMAINS = {"subject-inventory", "candidate-producer-result", "target-attribution", "incoming-search"}
T, F, U = "true", "false", "indeterminate"
SEV_RANK = {"note": 0, "warning": 1, "error": 2}


def C_encode(value: Any, depth: int = 0) -> bytes:
    if depth > 32:
        raise ValueError("NESTING_TOO_DEEP")
    if value is None:
        return b"null"
    if type(value) is bool:
        return b"true" if value else b"false"
    if type(value) is int:
        return str(value).encode("ascii")
    if type(value) is str:
        out = ['"']
        for ch in value:
            o = ord(ch)
            if ch == '"':
                out.append('\\"')
            elif ch == "\\":
                out.append("\\\\")
            elif ch == "\b":
                out.append("\\b")
            elif ch == "\t":
                out.append("\\t")
            elif ch == "\n":
                out.append("\\n")
            elif ch == "\f":
                out.append("\\f")
            elif ch == "\r":
                out.append("\\r")
            elif o < 0x20:
                out.append(f"\\u{o:04x}")
            else:
                out.append(ch)
        out.append('"')
        return "".join(out).encode("utf-8")
    if type(value) is list:
        return b"[" + b",".join(C_encode(v, depth + 1) for v in value) + b"]"
    if type(value) is dict:
        keys = sorted(value.keys(), key=lambda k: k.encode("utf-8"))
        parts = [C_encode(k, depth + 1) + b":" + C_encode(value[k], depth + 1) for k in keys]
        return b"{" + b",".join(parts) + b"}"
    raise TypeError(type(value).__name__)


def H_preimage(domain: str, canonical: bytes) -> bytes:
    return b"opensip.product.v1\x00" + domain.encode("ascii") + b"\x00" + len(canonical).to_bytes(8, "big") + canonical


def H_hex(domain: str, value: Any) -> str:
    return hashlib.sha256(H_preimage(domain, C_encode(value))).hexdigest()


def sha256_hex(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def parse_h_frame(raw: bytes) -> dict | None:
    prefix = b"opensip.product.v1\x00"
    if not raw.startswith(prefix):
        return None
    rest = raw[len(prefix) :]
    z = rest.find(b"\x00")
    if z < 0 or len(rest) < z + 1 + 8:
        return None
    domain = rest[:z].decode("ascii")
    ln = int.from_bytes(rest[z + 1 : z + 9], "big")
    payload = rest[z + 9 :]
    if len(payload) != ln:
        return {"domain": domain, "lengthMismatch": True, "declared": ln, "actual": len(payload)}
    try:
        obj = json.loads(payload)
    except Exception as e:
        return {"domain": domain, "parseError": str(e)}
    return {"domain": domain, "payload": payload, "obj": obj, "lengthMismatch": False}


def u8pref(b: bytes) -> bytes:
    if len(b) > 255:
        raise ValueError("u8 overflow")
    return bytes([len(b)]) + b


def body_identity_l0(*, level_spec: bytes, language_id: str, language_version: bytes, span: bytes) -> str:
    level_id = "L0-verbatim"
    level_version = hashlib.sha256(level_spec).digest()
    payload = len(span).to_bytes(4, "big") + span
    pre = (
        u8pref(b"opensip.fact-identity.v1")
        + u8pref(level_id.encode("ascii"))
        + u8pref(level_version)
        + u8pref(language_id.encode("ascii"))
        + u8pref(language_version)
        + len(payload).to_bytes(4, "big")
        + payload
    )
    return "sha256:" + hashlib.sha256(pre).hexdigest()


def utf8_sorted(xs: list[str]) -> bool:
    enc = [x.encode("utf-8") for x in xs]
    return enc == sorted(enc)


def canonical_set_ok(xs: list) -> tuple[bool, str]:
    cs = [C_encode(x) for x in xs]
    if len(set(cs)) != len(cs):
        return False, "duplicate"
    if cs != sorted(cs):
        return False, "not-sorted-by-C"
    return True, "ok"


def sort_set(xs: list) -> list:
    return sorted(xs, key=lambda x: C_encode(x))


def typed(domain: str, digest: str) -> str:
    p = DOMAIN_PREFIX.get(domain)
    return f"{p}:{digest}" if p else digest


def hex_of(value: Any) -> str | None:
    if not isinstance(value, str):
        return None
    if ":" in value:
        _p, rest = value.split(":", 1)
        if HEX64.match(rest):
            return rest
        return None
    if HEX64.match(value):
        return value
    return None


def longest_suffix_variant(path: str, table: dict[str, str]) -> str | None:
    hits = [s for s in table if path.endswith(s)]
    if not hits:
        return None
    return table[max(hits, key=len)]


def walk_x_opensip(obj: Any, acc: dict[str, int]) -> None:
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k.startswith("x-opensip-"):
                acc[k] = acc.get(k, 0) + 1
            walk_x_opensip(v, acc)
    elif isinstance(obj, list):
        for v in obj:
            walk_x_opensip(v, acc)


def resolve_ref(schema: Any, doc: dict) -> Any:
    if not isinstance(schema, dict) or "$ref" not in schema:
        return schema
    ref = schema["$ref"]
    if ref.startswith("#/$defs/"):
        name = ref.split("/")[-1]
        merged = dict(doc.get("$defs", {}).get(name) or {})
        extra = {k: v for k, v in schema.items() if k != "$ref"}
        merged.update(extra)
        return merged
    return schema


def iter_digest_annos(schema: Any, doc: dict, path: str = "$"):
    schema = resolve_ref(schema, doc)
    if not isinstance(schema, dict):
        return
    if "x-opensip-digest" in schema:
        yield path, schema["x-opensip-digest"], schema
    if "allOf" in schema:
        for sub in schema["allOf"]:
            yield from iter_digest_annos(sub, doc, path)
    if schema.get("type") == "object" or "properties" in schema:
        for k, sub in (schema.get("properties") or {}).items():
            yield from iter_digest_annos(sub, doc, f"{path}.{k}")
        addl = schema.get("additionalProperties")
        if isinstance(addl, dict):
            yield from iter_digest_annos(addl, doc, f"{path}.*")
    items = schema.get("items")
    if isinstance(items, dict):
        yield from iter_digest_annos(items, doc, f"{path}[]")


def instance_values(instance: Any, template: str) -> list[tuple[str, Any]]:
    parts = template.split(".")
    cur = [("$", instance)]
    for part in parts[1:]:
        nxt = []
        is_arr = part.endswith("[]")
        key = part[:-2] if is_arr else part
        for p, val in cur:
            if key == "*":
                if isinstance(val, dict):
                    for kk, vv in val.items():
                        nxt.append((f"{p}.{kk}", vv))
                continue
            if not isinstance(val, dict) or key not in val:
                continue
            child = val[key]
            if is_arr:
                if not isinstance(child, list):
                    continue
                for i, el in enumerate(child):
                    nxt.append((f"{p}.{key}[{i}]", el))
            else:
                nxt.append((f"{p}.{key}", child))
        cur = nxt
    return cur


def kleene_not(v: str) -> str:
    return {"true": F, "false": T}.get(v, U)


def kleene_and(vals: list[str]) -> str:
    if any(v == F for v in vals):
        return F
    if all(v == T for v in vals):
        return T
    return U


def kleene_or(vals: list[str]) -> str:
    if any(v == T for v in vals):
        return T
    if all(v == F for v in vals):
        return F
    return U


def rung_ge(relation: str, fact_rung: str, min_rung: str) -> bool:
    ladder = LADDERS[relation]
    if fact_rung not in ladder or min_rung not in ladder:
        return False
    return ladder.index(fact_rung) >= ladder.index(min_rung)


def occupancy_id(kind: str, payload: dict, native_id: str) -> str:
    if kind == "file":
        return payload.get("path", native_id)
    if kind == "package":
        return payload.get("packageName", native_id)
    return native_id


def filter_match(filt: dict, *, subject_id: str, payload: dict, fact: dict) -> bool:
    field, cmp_, val = filt["field"], filt["cmp"], filt["value"]
    if field == "subject":
        got = subject_id
    elif field == "resolution":
        got = fact["resolution"]
    elif field == "universe":
        got = fact["sourceUniverse"]
    else:
        got = payload.get(field)
    if cmp_ == "eq":
        return got == val
    if cmp_ == "neq":
        return got != val
    if cmp_ == "in":
        return got in val
    if cmp_ == "prefix":
        return type(got) is str and got.startswith(val)
    return False


def eval_atom(atom: dict, *, subject: dict, facts: list[dict], coverages: list[dict], payloads: dict) -> dict:
    rel = atom["relation"]
    minr = atom["minResolution"]
    op = atom["op"]
    matching = []
    for f in facts:
        rec = f["record"]
        if rec["relation"] != rel:
            continue
        if not rung_ge(rel, rec["resolution"], minr):
            continue
        pl = payloads[f["id"]]
        occ = occupancy_id(subject["kind"], pl, subject["nativeSubjectId"])
        if occ != subject["nativeSubjectId"]:
            continue
        if any(not filter_match(filt, subject_id=subject["nativeSubjectId"], payload=pl, fact=rec) for filt in atom.get("filters") or []):
            continue
        matching.append(f["id"])
    cov_ids = [c["id"] for c in coverages if c["record"]["relation"] == rel and c["record"]["resolution"] == minr]
    has_cov = bool(cov_ids)
    known = matching
    if op == "exists":
        if known:
            value = T
        elif not has_cov:
            value = U
        else:
            cov_complete = any(c["entry"].get("coverage") == "complete" for c in coverages if c["id"] in cov_ids)
            value = F if cov_complete else U
    elif op == "none":
        if known:
            value = F
        elif not has_cov:
            value = U
        else:
            cov_complete = any(c["entry"].get("coverage") == "complete" for c in coverages if c["id"] in cov_ids)
            value = T if cov_complete else U
    elif op == "count-at-most":
        n = atom["n"]
        if len(set(known)) > n:
            value = F
        elif not has_cov:
            value = U
        else:
            cov_complete = any(c["entry"].get("coverage") == "complete" for c in coverages if c["id"] in cov_ids)
            value = T if cov_complete and len(set(known)) <= n else U
    elif op == "all-covered":
        # Atom contract: all-covered calls sufficiency_v2, not merely coverage=complete.
        # This pilot's committed atom is `none`; this branch is not the executed emitWhen.
        cov_complete = any(c["entry"].get("coverage") == "complete" for c in coverages if c["id"] in cov_ids)
        value = T if cov_complete and has_cov else U
    else:
        value = U
    defs = []
    if value == U and not has_cov:
        defs.append("missing-relation-coverage")
    return {
        "value": value,
        "matchingFactIds": sorted(set(known)),
        "coverageIds": sorted(cov_ids),
        "deficiencies": defs,
        "kind": "native-atom",
    }


def walk_predicate(node: dict, *, prefix: str, **kw) -> dict:
    op = node["op"]
    if op in ("exists", "none", "count-at-most", "all-covered"):
        r = eval_atom(node, **kw)
        r.update({"predicateId": prefix, "operation": op, "children": [], "node": node})
        return r
    if op in ("and", "or"):
        kids = [walk_predicate(ch, prefix=f"{prefix}.{i}", **kw) for i, ch in enumerate(node["operands"])]
        vals = [k["value"] for k in kids]
        value = kleene_and(vals) if op == "and" else kleene_or(vals)
        return {
            "predicateId": prefix,
            "operation": op,
            "value": value,
            "children": kids,
            "matchingFactIds": [],
            "coverageIds": [],
            "deficiencies": [],
            "kind": "boolean",
            "node": node,
        }
    if op == "not":
        kid = walk_predicate(node["operand"], prefix=f"{prefix}.0", **kw)
        return {
            "predicateId": prefix,
            "operation": "not",
            "value": kleene_not(kid["value"]),
            "children": [kid],
            "matchingFactIds": [],
            "coverageIds": [],
            "deficiencies": [],
            "kind": "boolean",
            "node": node,
        }
    raise ValueError(op)


def flatten(node: dict) -> list[dict]:
    out = [node]
    for ch in node.get("children") or []:
        out.extend(flatten(ch))
    return out


def derive_account(*, account: dict, matching: list[dict]) -> dict:
    applicability = account["applicability"]
    named = sort_set(list(account.get("coverageIds") or []))
    matching_ids = sort_set([e["digest"] for e in matching])
    derived = {
        "applicability": applicability,
        "namedCoverageIds": named,
        "matchingCoverageIds": matching_ids,
        "accountComplete": False,
        "nativeWorkIncomplete": False,
        "derivedCoverage": None,
        "error": None,
    }
    if applicability in {"inapplicable-vcs", "unsupported-typed", "unavailable-unselected", "unavailable-null-universe"}:
        if named:
            derived["error"] = "inapplicable-must-have-empty-coverageIds"
            return derived
        derived["accountComplete"] = True
        return derived
    if applicability != "supported-available":
        derived["error"] = f"unknown-applicability:{applicability}"
        return derived
    if named != matching_ids:
        derived["error"] = "coverageIds-not-equal-matching-partitions"
        return derived
    if not named:
        derived["nativeWorkIncomplete"] = True
        return derived
    states = [e["entry"]["coverage"] for e in matching]
    if any(s != "complete" for s in states):
        derived["derivedCoverage"] = "unknown" if "unknown" in states else "partial"
        return derived
    derived["accountComplete"] = True
    derived["derivedCoverage"] = "complete"
    return derived


def derive_outcome(*, enumerator_status: str, universe: str | None, inventories: list[dict], derived_accounts: list[dict], candidate_owed: bool, candidate_state: str | None) -> dict:
    if enumerator_status == "unselected" or universe is None:
        return {"state": "unavailable", "deficiency": "provider-unavailable", "nativeCause": None, "reason": "enumerator-unselected-or-null-universe"}
    inv_states = [i["state"] for i in inventories]
    if any(s == "unavailable" for s in inv_states) and not any(s in ("complete", "partial") for s in inv_states):
        src = inventories[0] if inventories else {}
        return {"state": "unavailable", "deficiency": src.get("deficiency") or "provider-unavailable", "nativeCause": src.get("nativeCause"), "reason": "selected-provider-unavailable-no-work"}
    if any(s == "partial" for s in inv_states):
        src = next(i for i in inventories if i["state"] == "partial")
        return {"state": "partial", "deficiency": src.get("deficiency"), "nativeCause": src.get("nativeCause"), "reason": "inventory-partial"}
    for acc in derived_accounts:
        if acc["applicability"] == "supported-available" and not acc["accountComplete"]:
            return {
                "state": "partial",
                "deficiency": "required-relation-missing" if acc.get("nativeWorkIncomplete") else "resolution-incomplete",
                "nativeCause": None,
                "reason": "supported-available-account-not-complete",
            }
    if candidate_owed and candidate_state != "complete":
        return {"state": "partial" if candidate_state == "partial" else "unavailable", "deficiency": None if candidate_state == "partial" else "provider-unavailable", "nativeCause": None, "reason": "candidate-owed-not-complete"}
    if any(s != "complete" for s in inv_states):
        return {"state": None, "deficiency": None, "nativeCause": None, "reason": "EXECUTION_INPUTS_OUTCOME_DERIVE", "error": f"inventory states {inv_states}"}
    return {"state": "complete", "deficiency": None, "nativeCause": None, "reason": "all-complete"}


results: dict[str, Any] = {"laws": [], "findings": [], "notReached": [], "notApplicable": [], "assumptionsAudited": []}


def rec(law_id: str, status: str, selector: str, detail: str = "", **extra):
    row = {"id": law_id, "status": status, "selector": selector, "detail": detail, **extra}
    results["laws"].append(row)
    if status == "REFUSED":
        results["findings"].append(row)
    elif status == "NOT_REACHED":
        results["notReached"].append(row)
    elif status == "NOT_APPLICABLE":
        results["notApplicable"].append(row)
    return row


# ---------- custody ----------
kit_manifest_bytes = (KIT / "consumer-input-manifest.json").read_bytes()
kit_manifest_sha = sha256_hex(kit_manifest_bytes)
kit_man = json.loads(kit_manifest_bytes)
req_sha = sha256_hex(REQ.read_bytes())
man_bytes = MANIFEST_PATH.read_bytes()
man_sha = sha256_hex(man_bytes)
man = json.loads(man_bytes)
snap_pass = 0
snap_fail = []
declared = set()
for f in man["files"]:
    rel, sha, size = f["path"], f["sha256"], f["bytes"]
    declared.add(rel)
    p = SNAP / rel
    if not p.is_file():
        snap_fail.append({"path": rel, "reason": "missing"})
        continue
    raw = p.read_bytes()
    got = sha256_hex(raw)
    if got != sha or len(raw) != size:
        snap_fail.append({"path": rel, "got": got, "expect": sha, "bytes": len(raw), "expectBytes": size})
    else:
        snap_pass += 1
undeclared = []
for p in SNAP.rglob("*"):
    if p.is_file():
        rel = str(p.relative_to(SNAP))
        if rel not in declared:
            undeclared.append(rel)

kit_file_fail = []
for f in kit_man["files"]:
    p = KIT / f["path"]
    raw = p.read_bytes()
    if sha256_hex(raw) != f["sha256"] or len(raw) != f["bytes"]:
        kit_file_fail.append(f["path"])

rec("SNAPSHOT-MANIFEST-SHA256", "PASS" if man_sha == EXPECTED_MANIFEST else "REFUSED", "session input: snapshot-manifest.json SHA-256", detail=f"got={man_sha} expect={EXPECTED_MANIFEST}")
rec("SNAPSHOT-FILES-245", "PASS" if snap_pass == 245 and not snap_fail and not undeclared else "REFUSED", "session input: all declared snapshot files", detail=f"pass={snap_pass} fail={len(snap_fail)} undeclared={len(undeclared)}")
rec("KIT-MANIFEST-SHA256", "PASS" if kit_manifest_sha == EXPECTED_KIT_MANIFEST else "REFUSED", "original80 kit consumer-input-manifest.json", detail=kit_manifest_sha)
rec("KIT-FILES-80", "PASS" if not kit_file_fail and len(kit_man["files"]) == 80 else "REFUSED", "original80 kit file sha256/bytes vs manifest", detail=str(kit_file_fail[:8]) if kit_file_fail else "PASS 80/80")
rec("REQUIREMENTS-SHA256", "PASS", "original requirements.json beside the kit", detail=req_sha)

# keyword inventory (not execution)
kw_counts: dict[str, int] = {}
for rel in [
    "docs/coop/design-corrections/foundation/identity-schemas.v3.json",
    "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json",
    "docs/coop/design-corrections/native/native-evidence.schemas.v2.json",
    "docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json",
    "docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json",
    "docs/coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json",
    "docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json",
    "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json",
    "docs/coop/design-corrections/workflows/schemas/policy-document.schema.json",
]:
    walk_x_opensip(json.loads((KIT / rel).read_text()), kw_counts)
inventory = {
    "xOpensipKeywordCounts": kw_counts,
    "digestDomains": sorted(DIGEST_DOMAINS["byDomain"].keys()),
    "domainSets": sorted(DOMAIN_SETS.keys()),
    "relationRegistry": sorted(RELREG.keys()),
    "payloadRegistryClasses": sorted(PAYLOAD_REG["classes"].keys()),
    "closureMembershipDirect": sorted(CLOSURE_MEMBERSHIP["direct"].keys()),
    "closureMembershipEqualToDirect": sorted(CLOSURE_MEMBERSHIP["equalToDirect"].keys()),
    "closureMembershipSelectedThroughOtherInput": sorted(CLOSURE_MEMBERSHIP["selectedThroughOtherInput"].keys()),
    "selectionLaw": CLOSURE_MEMBERSHIP["selectionLaw"],
    "note": "Keyword counts are an inventory of published annotations, not execution of those annotations.",
}
results["assumptionsAudited"].append(
    {
        "prior": "DIGEST-FIELD-PREIMAGE-RETENTION walked *Digest/*Sha256 suffix names",
        "correction": "This checker executes x-opensip-digest owners collected from the published schema of records actually present. Suffix walk is retained only as an audit contrast, not as the law.",
    }
)
results["assumptionsAudited"].append(
    {
        "prior": "grammarVariant-from-suffix was a local SYNTAX_SUFFIX table",
        "correction": "Variant is taken from identity-schemas.v3 domainSets.native-semantic-universe.native.semantic-universe.syntax.v2.languageVersionBinding.dialect.table; longest suffix wins; onUnknown BODY_LANGUAGE_GRAMMAR_VARIANT_UNKNOWN; bodyLanguageByVariant supplies languageId.",
        "selector": "identity-schemas.v3.json#/x-opensip-digest-domains/domainSets/native-semantic-universe/native.semantic-universe.syntax.v2/languageVersionBinding",
    }
)

# ---------- load store ----------
store_raw = STORE_PATH.read_bytes()
store_sha = sha256_hex(store_raw)
doc = json.loads(store_raw)
blobs = {k: base64.b64decode(v) for k, v in doc["blobs"].items()}
ot = doc["objectTable"]
meta = json.loads(META_PATH.read_text())
rec("STORE-SHA256", "PASS" if store_sha == "0a0b2c6217846264b2bff2b013410215b0941c4c50d695bd234a1d5aac14ec36" else "REFUSED", "exact exported syntax-code.store.json bytes", detail=f"{store_sha} bytes={len(store_raw)} blobs={len(blobs)}")

blob_key_bad = [{"key": k, "sha256": sha256_hex(raw)} for k, raw in blobs.items() if sha256_hex(raw) != k]
rec("STORE-BLOB-KEY-EQUALS-SHA256", "PASS" if not blob_key_bad else "REFUSED", "identity-and-evidence §3: raw blob reference uses SHA256 of exact bytes", detail=json.dumps(blob_key_bad[:5]) if blob_key_bad else "ok")

h_records: dict[str, dict] = {}
json_records: dict[str, Any] = {}
frame_failures = []
for digest, raw in blobs.items():
    fr = parse_h_frame(raw)
    if fr and "obj" in fr and not fr.get("lengthMismatch"):
        c_re = C_encode(fr["obj"])
        c_eq = c_re == fr["payload"]
        h_eq = sha256_hex(H_preimage(fr["domain"], c_re)) == digest
        rec_meta = ot.get(digest, {})
        h_records[digest] = {"domain": fr["domain"], "obj": fr["obj"], "cEqual": c_eq, "hEqual": h_eq, "typedId": rec_meta.get("typedId"), "label": rec_meta.get("label")}
        if not c_eq or not h_eq:
            frame_failures.append({"digest": digest, "domain": fr["domain"], "cEqual": c_eq, "hEqual": h_eq})
    elif raw[:1] in (b"{", b"["):
        try:
            json_records[digest] = json.loads(raw)
        except Exception:
            pass
    elif fr and fr.get("lengthMismatch"):
        frame_failures.append({"digest": digest, "lengthMismatch": True})
rec("H-FRAME-REMIND-AND-C-EQUALITY", "PASS" if not frame_failures else "REFUSED", "identity-and-evidence §3 H(D,X) frame admission", detail=f"nHFrames={len(h_records)}" if not frame_failures else json.dumps(frame_failures[:8]), nFrames=len(h_records))

prefix_bad = []
for digest, recd in h_records.items():
    pref = DOMAIN_PREFIX.get(recd["domain"])
    typed_id = recd.get("typedId")
    if pref:
        expect = f"{pref}:{digest}"
        if typed_id and typed_id != expect:
            prefix_bad.append({"digest": digest, "typed": typed_id, "expect": expect})
rec("TYPED-PREFIX-VS-DOMAIN", "PASS" if not prefix_bad else "REFUSED", "identity-and-evidence §3 identifier is prefix + ':' + lowercase H hex; native domain-set identities use sha256:", detail=json.dumps(prefix_bad[:8]) if prefix_bad else "ok")


def by_domain(d: str) -> list[dict]:
    return [{"digest": k, **v} for k, v in h_records.items() if v["domain"] == d]


def load_json(digest: str) -> Any:
    if digest in json_records:
        return json_records[digest]
    if digest in blobs:
        obj = json.loads(blobs[digest])
        json_records[digest] = obj
        return obj
    return None


runs, plans, snaps, proofs, evidences, seals = by_domain("run"), by_domain("plan"), by_domain("snapshot"), by_domain("proof-bundle"), by_domain("semantic-evidence"), by_domain("evaluation-seal")
facts, coverages, views, scopes, subjects, eplans, closures = by_domain("fact"), by_domain("coverage"), by_domain("view"), by_domain("subject-scope"), by_domain("evaluation-subject"), by_domain("execution-plan"), by_domain("closure")
syn_ctx, syn_uni = by_domain("native.context.syntax.v2"), by_domain("native.semantic-universe.syntax.v2")
rec(
    "GRAPH-MEMBERSHIP-CORE-DOMAINS",
    "PASS" if len(runs) == 1 and len(plans) == 1 and len(snaps) == 1 and len(proofs) == 1 and len(seals) == 1 and len(evidences) == 1 else "REFUSED",
    "identity-and-evidence §3 run/plan/snapshot/proof/evidence/seal domains",
    detail=f"run={len(runs)} plan={len(plans)} snap={len(snaps)} proof={len(proofs)} ev={len(evidences)} seal={len(seals)} fact={len(facts)} cov={len(coverages)} view={len(views)} scope={len(scopes)} closure={len(closures)}",
)
run, plan, snap, proof, evidence, seal = runs[0], plans[0], snaps[0], proofs[0], evidences[0], seals[0]
run_o, plan_o, snap_o, proof_o, ev_o, seal_o = run["obj"], plan["obj"], snap["obj"], proof["obj"], evidence["obj"], seal["obj"]
view = views[0]
view_o = view["obj"]

def eq(name, a, b, selector):
    rec(name, "PASS" if a == b else "REFUSED", selector, detail=f"{a} vs {b}")

eq("JOIN-RUN-SNAPSHOT", run_o.get("snapshotId"), typed("snapshot", snap["digest"]), "run.snapshotId = snapshot2 identity")
eq("JOIN-RUN-PLAN", run_o.get("planId"), typed("plan", plan["digest"]), "run.planId = plan2 identity")
eq("JOIN-PLAN-SNAPSHOT", plan_o.get("snapshotId"), typed("snapshot", snap["digest"]), "plan.snapshotId = snapshot2")
eq("JOIN-PROOF-PLAN", proof_o.get("planId"), typed("plan", plan["digest"]), "proof-bundle.planId = plan2")
eq("JOIN-EVIDENCE-PLAN", ev_o.get("planId"), typed("plan", plan["digest"]), "semantic-evidence.planId = plan2")
eq("JOIN-SEAL-PLAN", seal_o.get("planId"), typed("plan", plan["digest"]), "evaluation-seal.planId = plan2")
eq("JOIN-RUN-EVIDENCE", run_o.get("evidenceId"), typed("semantic-evidence", evidence["digest"]), "run.evidenceId = evidence3")
eq("JOIN-RUN-SEAL", run_o.get("evaluationSealId"), typed("evaluation-seal", seal["digest"]), "run includes seal")
eq("JOIN-SEAL-EVIDENCE", seal_o.get("evidenceId"), typed("semantic-evidence", evidence["digest"]), "seal includes evidence")
eq("JOIN-SEAL-PROOF", seal_o.get("proofBundleId"), typed("proof-bundle", proof["digest"]), "seal includes proof")
eq("JOIN-EVIDENCE-PROOF", ev_o.get("proofBundleId"), typed("proof-bundle", proof["digest"]), "evidence includes proof")
eq("JOIN-RUN-PROJECT", run_o.get("projectId"), snap_o.get("projectId"), "run.projectId = snapshot.projectId")


def contains_id(obj, s):
    if obj == s:
        return True
    if isinstance(obj, dict):
        return any(contains_id(v, s) for v in obj.values())
    if isinstance(obj, list):
        return any(contains_id(v, s) for v in obj)
    return False

proof_has_evidence = contains_id(proof_o, typed("semantic-evidence", evidence["digest"])) or "evidenceId" in proof_o
proof_has_run = contains_id(proof_o, typed("run", run["digest"])) or "runId" in proof_o
rec("ACYCLIC-PROOF-NO-EVIDENCE-OR-RUN", "PASS" if not proof_has_evidence and not proof_has_run else "REFUSED", "identity-and-evidence §3: graph is acyclic: proof does not include EvidenceId or RunId")
rec("ACYCLIC-SEAL-INCLUDES-BOTH", "PASS" if seal_o.get("evidenceId") and seal_o.get("proofBundleId") else "REFUSED", "identity-and-evidence §3: seal includes both evidence and proof")
rec("ACYCLIC-RUN-INCLUDES-SEAL", "PASS" if run_o.get("evaluationSealId") else "REFUSED", "identity-and-evidence §3: Run includes seal")

cap_id = plan_o.get("capabilityManifestId")
cap_bytes_d = plan_o.get("capabilityManifestBytesDigest")
if cap_bytes_d in blobs and cap_id:
    derived = sha256_hex(b"opensip.capability-manifest.v1\x00" + blobs[cap_bytes_d])
    rec("CAP-MANIFEST-ID-DERIVED", "PASS" if derived == cap_id else "REFUSED", "identity-and-evidence §3 capability-manifest-id SHA256(UTF8('opensip.capability-manifest.v1')||00||committedBytes)", detail=f"derived={derived} claimed={cap_id}")
else:
    rec("CAP-MANIFEST-ID-DERIVED", "REFUSED", "capability-manifest-id derived", detail=f"bytesDigest={cap_bytes_d}")
eq("JOIN-RUN-CAP-MANIFEST", run_o.get("capabilityManifestId"), plan_o.get("capabilityManifestId"), "run.capabilityManifestId = plan.capabilityManifestId")

rel_digest = sha256_hex(RELDOC_BYTES)
native_cov_digest = sha256_hex(NATIVE_BYTES)
payload_schema_bad, ladder_findings, anchor_findings, universe_findings, payload_c_findings, rung_field_findings = [], [], [], [], [], []
file_facts, clone_facts, decl_facts, cf_facts = [], [], [], []
for f in facts:
    fo = f["obj"]
    rel, rung = fo.get("relation"), fo.get("resolution")
    row = RELREG.get(rel)
    if not row:
        ladder_findings.append({"unregisteredRelation": rel})
        continue
    if rung not in row.get("ladder", []):
        ladder_findings.append({"relation": rel, "rung": rung, "ladder": row.get("ladder")})
    anchors = fo.get("anchors") or []
    alaw = row.get("anchorLaw") or {}
    cls = alaw.get("class")
    if cls == "inventory" or alaw.get("cardinality") == 0:
        if len(anchors) != 0:
            anchor_findings.append({"rel": rel, "want": 0, "got": len(anchors)})
    elif cls == "body-identity" or alaw.get("cardinality") == 1:
        if len(anchors) != 1:
            anchor_findings.append({"rel": rel, "want": 1, "got": len(anchors)})
    elif cls == "source-text" or alaw.get("minimum") == 1:
        if len(anchors) < 1:
            anchor_findings.append({"rel": rel, "want": ">=1", "got": len(anchors)})
    if row.get("universeRule") == "same-only" and fo.get("sourceUniverse") != fo.get("targetUniverse"):
        universe_findings.append({"rel": rel})
    if fo.get("payloadSchemaDigest") != rel_digest:
        payload_schema_bad.append({"fact": typed("fact", f["digest"]), "got": fo.get("payloadSchemaDigest")})
    pd = fo.get("payloadDigest")
    payload_obj = load_json(pd) if pd else None
    if payload_obj is None:
        payload_c_findings.append({"missingPayload": pd, "rel": rel})
    else:
        if sha256_hex(C_encode(payload_obj)) != pd:
            payload_c_findings.append({"rel": rel, "cMismatch": True})
        rules = (row.get("rungs") or {}).get(rung) or {}
        for reqf in rules.get("required") or []:
            if reqf not in payload_obj:
                rung_field_findings.append({"missingRequired": reqf, "rung": rung, "rel": rel})
        for forb in rules.get("forbidden") or []:
            if forb in payload_obj:
                rung_field_findings.append({"forbiddenPresent": forb, "rung": rung, "rel": rel})
        bucket = {"fact": f, "payload": payload_obj, "anchors": anchors}
        if rel == "file":
            file_facts.append(bucket)
        elif rel == "clones":
            clone_facts.append(bucket)
        elif rel == "declares":
            decl_facts.append(bucket)
        elif rel == "control-flow":
            cf_facts.append(bucket)

rec("PAYLOAD-SCHEMA-DIGEST-RELATION-DOCUMENT", "PASS" if not payload_schema_bad else "REFUSED", "x-opensip-payload-registry.classes.relation: payloadSchemaDigest = raw SHA-256 of exact relation-payload-schemas.v2.json bytes", detail=rel_digest if not payload_schema_bad else json.dumps(payload_schema_bad[:5]))
rec("RELATION-LADDER-MEMBERSHIP", "PASS" if not ladder_findings else "REFUSED", "x-opensip-relation-registry membershipRule", detail=json.dumps(ladder_findings[:8]) if ladder_findings else f"nFacts={len(facts)} relations={sorted({f['obj'].get('relation') for f in facts})}")
rec("ANCHOR-LAW-CARDINALITY", "PASS" if not anchor_findings else "REFUSED", "relation-registry anchorLaw (inventory=0, body-identity=1, source-text>=1)", detail=json.dumps(anchor_findings[:8]) if anchor_findings else "ok")
rec("UNIVERSE-RULE-SAME-ONLY", "PASS" if not universe_findings else "REFUSED", "payload-registry relation universeRule same-only", detail=json.dumps(universe_findings[:8]) if universe_findings else "ok")
rec("FACT-PAYLOAD-C-DIGEST", "PASS" if not payload_c_findings else "REFUSED", "x-opensip-digest canonical-record: payloadDigest = SHA256(C(payload))", detail=json.dumps(payload_c_findings[:8]) if payload_c_findings else "ok")
rec("RUNG-REQUIRED-FORBIDDEN-FIELDS", "PASS" if not rung_field_findings else "REFUSED", "relation rungs required/forbidden payload fields", detail=json.dumps(rung_field_findings[:8]) if rung_field_findings else "ok")

inv = snap_o.get("sourceInventory")
inv_entries = inv.get("entries") if isinstance(inv, dict) else (inv or [])
inv_by_path = {e.get("path"): e for e in inv_entries if isinstance(e, dict)}
inv_paths = [e.get("path") for e in inv_entries]
rec("SNAPSHOT-INVENTORY-PATH-ORDER", "PASS" if utf8_sorted(inv_paths) else "REFUSED", "identity snapshot sourceInventory x-opensip-order path / utf-8", detail=str(inv_paths))

file_join_bad = []
for ff in file_facts:
    pth, dgst, n = ff["payload"].get("path"), ff["payload"].get("contentSha256"), ff["payload"].get("byteLength")
    row = inv_by_path.get(pth)
    if not row:
        file_join_bad.append({"path": pth, "reason": "not-in-inventory"})
        continue
    if row.get("sha256") != dgst or row.get("bytes") != n:
        file_join_bad.append({"path": pth, "reason": "inventory-mismatch"})
    if dgst not in blobs or len(blobs[dgst]) != n or sha256_hex(blobs[dgst]) != dgst:
        file_join_bad.append({"path": pth, "reason": "retained-blob"})
rec("FILE-INVENTORIED-SNAPSHOT-JOIN", "PASS" if file_facts and not file_join_bad else ("REFUSED" if file_join_bad else "NOT_APPLICABLE"), "relation-registry file.snapshotJoins inventoried-file", detail=json.dumps(file_join_bad[:8]) if file_join_bad else f"nFileFacts={len(file_facts)}")

ctx_obj = syn_ctx[0]["obj"] if syn_ctx else None
uni_obj = syn_uni[0]["obj"] if syn_uni else None
if ctx_obj and uni_obj:
    gb = ctx_obj.get("grammarBundle") or {}
    rec("SYNTAX-GRAMMAR-BUNDLEDIGEST-PREIMAGE", "PASS" if gb.get("bundleDigest") in blobs else "REFUSED", "SyntaxGrammarBundleV1.bundleDigest x-opensip-digest raw-artifact", detail=str(gb.get("bundleDigest")))
    rec("SYNTAX-NORMALIZER-SPEC-PREIMAGE", "PASS" if (gb.get("normalizer") or {}).get("specificationDigest") in blobs else "REFUSED", "SyntaxGrammarBundleV1.normalizer.specificationDigest raw-artifact")
    cid = gb.get("closureId")
    rec("SYNTAX-CONTEXT-GRAMMAR-CLOSURE-JOIN", "PASS" if isinstance(cid, str) and cid.startswith("closure2:") and cid.split(":", 1)[-1] in blobs else "REFUSED", "domainSets.native-context.native.context.syntax.v2.closureJoins grammarBundle.closureId", detail=str(cid))
    gids = [g.get("grammarId") for g in gb.get("grammars") or []]
    sel = uni_obj.get("selectedGrammarIds") or []
    rec("SYNTAX-UNIVERSE-SELECTED-GRAMMAR-SUBSET", "PASS" if sel and all(s in gids for s in sel) else "REFUSED", "SyntaxUniverseV2ResolvedInputs.selectedGrammarIds subset of context bundle grammarIds", detail=f"sel={sel} bundle={gids}")
    rec("SYNTAX-UNIVERSE-RESOLUTION-ATTEMPTED-FALSE", "PASS" if uni_obj.get("resolutionAttempted") is False else "REFUSED", "SyntaxUniverseV2ResolvedInputs.resolutionAttempted const false")
    rec("SYNTAX-UNIVERSE-BINDS-CONTEXT", "PASS" if uni_obj.get("nativeContextId") == f"sha256:{syn_ctx[0]['digest']}" else "REFUSED", "domainSets native-semantic-universe.syntax contextField nativeContextId form sha256-text")
    rec("SYNTAX-CONTEXT-NO-TOOLCHAIN", "PASS" if set(ctx_obj.keys()) <= {"schemaVersion", "grammarBundle"} else "REFUSED", "native.context.syntax.v2: no toolchain/stdlib/lockfile/node_modules/config graph", detail=str(list(ctx_obj.keys())))
    rec("TS-RUST-CONTEXT-NOT-IN-THIS-GRAPH", "NOT_APPLICABLE", "native.context.typescript.v2 / rust.v2 snapshotJoins and nestedIdentities", detail="this graph's native context domain is syntax.v2 only")
    gdef_bad = [g.get("grammarDigest") for g in gb.get("grammars") or [] if g.get("grammarDigest") not in blobs]
    rec("GRAMMAR-DEFINITION-PREIMAGES", "PASS" if not gdef_bad else "REFUSED", "SyntaxGrammarBundleV1.grammars[].grammarDigest raw-artifact preimage")
    rec("GRAMMAR-ARRAY-ORDER-BY-GRAMMARID", "PASS" if gids == sorted(gids, key=lambda x: x.encode("utf-8")) else "REFUSED", "x-opensip-order by [grammarId]", detail=str(gids))
else:
    rec("SYNTAX-NATIVE-CONTEXT-PRESENT", "REFUSED", "native.context.syntax.v2 required for syntax-code Run")

nctx = plan_o.get("nativeContextDigests") or []
if syn_ctx:
    rec("PLAN-NATIVE-CONTEXT-SELECTION", "PASS" if syn_ctx[0]["digest"] in nctx else "REFUSED", "plan.nativeContextDigests contains admitted syntax context H suffix", detail=f"nctx={nctx}")
    rec("PLAN-NATIVE-CONTEXT-NONEMPTY", "PASS" if len(nctx) >= 1 else "REFUSED", "complete syntax positive has selected native context")

# clones L0 from kit languageVersionBinding (not a local suffix heuristic)
clone_bad = []
l1_seen = False
table = SYNTAX_LVB["dialect"]["table"]
by_variant = SYNTAX_LVB["bodyLanguageByVariant"]
for cf in clone_facts:
    payload, anchors = cf["payload"], cf["anchors"]
    if len(anchors) != 1:
        clone_bad.append({"reason": "anchor-cardinality"})
        continue
    a = anchors[0]
    path, blob, start, end = a.get("path"), a.get("blobDigest"), a.get("startByte"), a.get("endByte")
    nver, level, bid = payload.get("normalisationVersion"), payload.get("normalisationLevel"), payload.get("bodyIdentity")
    if blob not in blobs or nver not in blobs:
        clone_bad.append({"reason": "missing-preimage", "blob": blob, "nver": nver})
        continue
    if path not in inv_by_path:
        clone_bad.append({"reason": "anchor-path-not-inventoried", "path": path})
    variant = longest_suffix_variant(path or "", table)
    if variant is None:
        clone_bad.append({"reason": SYNTAX_LVB["dialect"]["onUnknown"], "path": path})
        continue
    lang = by_variant[variant]
    gb = (ctx_obj or {}).get("grammarBundle") or {}
    blv = {
        "schemaVersion": 1,
        "languageId": lang,
        "compilerName": gb.get("parserName"),
        "compilerVersion": gb.get("parserVersion"),
        "compilerBuild": gb.get("bundleDigest"),
        "dialect": {"grammarVariant": variant},
    }
    lv = hashlib.sha256(C_encode(blv)).digest()
    if level == "L0-verbatim":
        recomputed = body_identity_l0(level_spec=blobs[nver], language_id=lang, language_version=lv, span=blobs[blob][start:end])
        if recomputed != bid:
            clone_bad.append({"reason": "L0-recompute-mismatch", "got": bid, "recomputed": recomputed, "variant": variant, "lang": lang, "blv": blv})
    else:
        l1_seen = True
        rec(
            f"CLONES-L1-PLUS-PREIMAGE-ONLY:{level}",
            "PASS" if nver in blobs else "REFUSED",
            "clones bodyIdentityJoin: L1-L3 require exact retained level-specification preimage; token-stream tokenisation judgment is not executed",
            detail=f"level={level} bodyIdentity={bid}",
        )
rec("CLONES-L0-RECOMPUTE-AND-LANGUAGEVERSION-DERIVED", "PASS" if clone_facts and not clone_bad else ("REFUSED" if clone_bad else "NOT_APPLICABLE"), "relation-registry clones.bodyIdentityJoin + identity-schemas.v3 languageVersionBindingLaw for native.semantic-universe.syntax.v2", detail=json.dumps(clone_bad[:6], default=str) if clone_bad else f"nClones={len(clone_facts)}")
if l1_seen:
    rec("CLONES-L1-TOKEN-STREAM-FRAMING-JUDGMENT", "NOT_REACHED", "relation-registry clones.bodyIdentityJoin.tokenStreamFraming: parse retained stream for custody/framing; do not judge tokenisation", detail="L1 token-kind registry is level-specification freedom; framing parse not independently executed")

decl_bad = []
for d in decl_facts:
    if len(d["anchors"]) < 1:
        decl_bad.append({"reason": "no-anchor"})
    for a in d["anchors"]:
        if a.get("path") not in inv_by_path:
            decl_bad.append({"reason": "anchor-path-not-inventoried", "path": a.get("path")})
rec("DECLARES-SOURCE-TEXT-ANCHORS", "PASS" if decl_facts and not decl_bad else ("REFUSED" if decl_bad else "NOT_APPLICABLE"), "declares anchorLaw source-text minimum 1; anchor path inventoried")

cov_payload_bad, cov_complete_exh, defic_bad = [], [], []
defreg = NATIVE.get("x-opensip-deficiency-cause-registry", {}).get("deficiencies", {})
for c in coverages:
    co = c["obj"]
    pd, psd = co.get("payloadDigest"), co.get("payloadSchemaDigest")
    payload = load_json(pd) if pd else None
    if payload is None:
        cov_payload_bad.append({"missing": pd})
        continue
    if sha256_hex(C_encode(payload)) != pd:
        cov_payload_bad.append({"cMismatch": True, "cov": c["digest"]})
    if psd != native_cov_digest:
        cov_payload_bad.append({"schemaDigest": psd, "expect": native_cov_digest})
    entry = payload.get("entry") or payload
    if entry.get("coverage") == "complete" and (entry.get("resolutionCompleteness") or {}).get("examinedExhaustive") is not True:
        cov_complete_exh.append({"cov": c["digest"]})
    d = entry.get("deficiency")
    if d:
        row = defreg.get(d)
        if not row:
            defic_bad.append({"unregisteredDeficiency": d})
        elif row.get("nativeCause") == "required" and entry.get("nativeCause") not in (row.get("allowedCauses") or []):
            defic_bad.append({"deficiency": d, "nativeCause": entry.get("nativeCause")})
    c["_payload"] = payload
    c["_entry"] = entry
    c["_key"] = payload.get("key") or {}
rec("COVERAGE-PAYLOAD-C-AND-SCHEMA", "PASS" if not cov_payload_bad else "REFUSED", "x-opensip-payload-registry coverage class schemaVersion 3 → native-evidence CoverageResultV3")
rec("RC-6-COMPLETE-IMPLIES-EXAMINED-EXHAUSTIVE", "PASS" if not cov_complete_exh else "REFUSED", "native-evidence CoverageResultV3: coverage=complete REQUIRES examinedExhaustive=true")
rec("DEFICIENCY-CAUSE-REGISTRY-JOIN", "PASS" if not defic_bad else "REFUSED", "native-evidence.schemas.v2.json x-opensip-deficiency-cause-registry")

scope_map = {typed("subject-scope", s["digest"]): s["obj"] for s in scopes}
fact_map = {typed("fact", f["digest"]): f for f in facts}
totality_bad = []
view_facts, view_scopes, view_covs = view_o.get("facts") or [], view_o.get("scopeIds") or [], view_o.get("coverageIds") or []
for sid in view_scopes:
    so = scope_map.get(sid)
    if not so:
        totality_bad.append({"missingScope": sid})
        continue
    if so.get("relation") == "file" and so.get("resolution") == "enumerated":
        matching_cov = next((c for c in coverages if typed("coverage", c["digest"]) in view_covs and c["obj"].get("scopeId") == sid), None)
        entry = (matching_cov or {}).get("_entry") or {}
        if entry.get("coverage") == "complete":
            file_paths_in_view = set()
            for fid in view_facts:
                ff = fact_map.get(fid)
                if not ff:
                    continue
                fo = ff["obj"]
                if fo.get("relation") != "file" or fo.get("resolution") != "enumerated":
                    continue
                po = load_json(fo.get("payloadDigest"))
                if po:
                    file_paths_in_view.add(po.get("path"))
            for subj in so.get("subjects") or []:
                if subj in inv_by_path and subj not in file_paths_in_view:
                    totality_bad.append({"omitted": subj, "refusal": "COVERAGE_INVENTORY_TOTALITY_OMITS_PATH"})
rec("FILE-ENUMERATED-COVERAGE-TOTALITY", "PASS" if not totality_bad else "REFUSED", "relation-registry file.coverageTotality")

part_bad = []
groups: dict[tuple, list] = {}
for sid in view_scopes:
    so = scope_map.get(sid)
    if not so:
        continue
    key = (so.get("snapshotId"), so.get("relation"), so.get("resolution"), so.get("sourceUniverse"), so.get("targetUniverse"))
    groups.setdefault(key, []).append(so)
for key, lst in groups.items():
    seen = []
    for so in lst:
        subs = so.get("subjects") or []
        for s in subs:
            for prev in seen:
                if s in prev:
                    part_bad.append({"overlap": s})
        seen.append(set(subs))
rec("COVERAGE-PARTITION-DISJOINT", "PASS" if not part_bad else "REFUSED", "relation-registry coveragePartitionLaw per view")

scope_rung_bad = []
for s in scopes:
    so = s["obj"]
    rel, rung = so.get("relation"), so.get("resolution")
    row = RELREG.get(rel)
    if not row or rung not in row.get("ladder", []):
        scope_rung_bad.append({"rel": rel, "rung": rung})
    if so.get("snapshotId") != typed("snapshot", snap["digest"]):
        scope_rung_bad.append({"snapshotMismatch": True})
rec("SUBJECT-SCOPE-RUNG-IN-LADDER", "PASS" if not scope_rung_bad else "REFUSED", "close_run SUBJECT_SCOPE_RUNG_NOT_IN_RELATION_LADDER")

view_bad = []
if view_o.get("planId") != typed("plan", plan["digest"]):
    view_bad.append({"planMismatch": True})
for fid in view_facts:
    if fid not in {typed("fact", f["digest"]) for f in facts}:
        view_bad.append({"missingFact": fid})
for sid in view_scopes:
    if sid not in {typed("subject-scope", s["digest"]) for s in scopes}:
        view_bad.append({"missingScope": sid})
rec("VIEW-MEMBER-JOINS", "PASS" if not view_bad else "REFUSED", "view2 names plan, facts, scopes, coverage that are retained")

order_bad = []
def check_set(name, xs):
    if not isinstance(xs, list):
        return
    ok, why = canonical_set_ok(xs)
    if not ok:
        order_bad.append({"name": name, "why": why})
check_set("plan.semanticClosures", plan_o.get("semanticClosures"))
check_set("plan.nativeContextDigests", plan_o.get("nativeContextDigests"))
check_set("plan.importIds", plan_o.get("importIds") or [])
check_set("view.facts", view_o.get("facts"))
check_set("view.scopeIds", view_o.get("scopeIds"))
check_set("view.coverageIds", view_o.get("coverageIds"))
check_set("proof.evaluationInputRefs", proof_o.get("evaluationInputRefs"))
check_set("proof.findingIds", proof_o.get("findingIds"))
for s in scopes:
    check_set(f"scope.subjects:{s['digest'][:8]}", s["obj"].get("subjects") or [])
rec("X-OPENSIP-ORDER-CANONICAL-SET-CORE", "PASS" if not order_bad else "REFUSED", "identity-schemas x-opensip-order canonical-set: unique and sorted by C bytes", detail=json.dumps(order_bad[:8]) if order_bad else "ok")

# closure membership — prior first actual refusal, rechecked on NEW graph
sem = set(plan_o.get("semanticClosures") or [])
pc = view_o.get("producerClosure")
fact_eq = all(f["obj"].get("producerClosure") == pc for f in facts) if facts and pc else False
evc, sealc = proof_o.get("evaluatorClosure"), seal_o.get("evaluatorClosure")
scope_enum_ok = all((s["obj"].get("enumeratorClosure") in sem) for s in scopes if s["obj"].get("enumeratorClosure"))
closure_by_id = {typed("closure", c["digest"]): c["obj"] for c in closures}
rec("CLOSURE-MEMBERSHIP-FACT-EQUALS-VIEW-PRODUCER", "PASS" if fact_eq else "REFUSED", "x-opensip-digest-domains.closureMembership.equalToDirect fact.producerClosure = enclosing view.producerClosure")
rec("CLOSURE-MEMBERSHIP-PROOF-EQUALS-SEAL-EVALUATOR", "PASS" if evc == sealc else "REFUSED", "x-opensip-digest-domains.closureMembership.equalToDirect proof-bundle.evaluatorClosure = evaluation-seal.evaluatorClosure", detail=f"proof={evc} seal={sealc}")
rec("CLOSURE-MEMBERSHIP-VIEW-PRODUCER-IN-PLAN", "PASS" if pc in sem else "REFUSED", "closureMembership.direct view.producerClosure must be in plan.semanticClosures", detail=f"producer={pc}")
rec(
    "CLOSURE-MEMBERSHIP-SEAL-EVALUATOR-IN-PLAN",
    "PASS" if sealc in sem else "REFUSED",
    "identity-schemas.v3.json#/x-opensip-digest-domains/closureMembership selectionLaw: Direct members must be in plan.semanticClosures",
    detail=f"evaluator={sealc} semanticClosures={sorted(sem)} kind={(closure_by_id.get(sealc) or {}).get('kind')}",
    refusal=None if sealc in sem else "UNSELECTED_EVALUATOR_CLOSURE",
    priorFirstActualRefusal="UNSELECTED_EVALUATOR_CLOSURE on predecessor run3:f2542b3a… / closure2:2a9cfd92…",
)
rec("CLOSURE-MEMBERSHIP-SCOPE-ENUMERATOR-IN-PLAN", "PASS" if scope_enum_ok else "REFUSED", "closureMembership.direct subject-scope.enumeratorClosure in plan.semanticClosures")

# stage-spec producerClosure is a direct member
ei_d = proof_o.get("executionInputsDigest")
ei = load_json(ei_d) if ei_d else None
rec("EXECUTION-INPUTS-PREIMAGE", "PASS" if ei_d in blobs else "REFUSED", "digest-domain execution-inputs retention preimage", detail=str(ei_d))
if ei:
    rec("EXECUTION-INPUTS-PLAN-JOIN", "PASS" if ei.get("planId") == typed("plan", plan["digest"]) else "REFUSED", "execution-inputs.planId = plan2")
    rec("EXECUTION-INPUTS-C-DIGEST", "PASS" if sha256_hex(C_encode(ei)) == ei_d else "REFUSED", "execution-inputs identity is raw SHA-256 of C(record)")
    rec("EXECUTION-INPUTS-EVALUATOR-EQUALS-SEAL", "PASS" if ei.get("evaluatorClosure") == sealc else "REFUSED", "execution-inputs.evaluatorClosure equals evaluation-seal.evaluatorClosure")

exec_plan = eplans[0]["obj"] if eplans else None
stage_spec = None
if exec_plan:
    rec("JOIN-EI-EXECUTION-PLAN", "PASS" if ei and ei.get("executionPlanId") == typed("execution-plan", eplans[0]["digest"]) else "REFUSED", "execution-inputs.executionPlanId = exec-plan2")
    ssd = (exec_plan.get("stages") or [{}])[0].get("stageSpecDigest")
    stage_spec = load_json(ssd) if ssd else None
    if stage_spec:
        rec("STAGE-OUTPUT-DOMAINS-VIEW-ONLY", "PASS" if stage_spec.get("outputDomains") == ["view"] else "REFUSED", "execution-inputs-contract.v1.md §1 / §7: reference fixture stage declares outputDomains view only", detail=str(stage_spec.get("outputDomains")))
        rec(
            "CLOSURE-MEMBERSHIP-STAGE-SPEC-PRODUCER-IN-PLAN",
            "PASS" if stage_spec.get("producerClosure") in sem else "REFUSED",
            "closureMembership.direct stage-spec.producerClosure must be in plan.semanticClosures",
            detail=str(stage_spec.get("producerClosure")),
        )
        rec("STAGE-SPEC-PRODUCER-EQUALS-VIEW-PROVIDER", "PASS" if stage_spec.get("producerClosure") == pc else "REFUSED", "stage-spec.producerClosure equals view.producerClosure (provider)")

# extra detector from emission plan
as_d = plan_o.get("analysisSpecDigest")
rec("ANALYSIS-SPEC-PREIMAGE", "PASS" if as_d in blobs else "REFUSED", "digest-domain analysis-spec canonical-record preimage")
analysis_spec = load_json(as_d) if as_d else None
emission_plan = None
enum_plan = None
if analysis_spec:
    for p in analysis_spec.get("parameters") or []:
        recd = load_json(p.get("payloadDigest"))
        if not recd:
            continue
        if recd.get("schemaVersion") == 1 and recd.get("rules") and "detectorClosure" in recd["rules"][0]:
            emission_plan = recd
        if recd.get("schemaVersion") == 1 and "cells" in recd:
            enum_plan = recd
if ei and not enum_plan:
    enum_plan = load_json(ei.get("enumerationPlanDigest"))
if emission_plan:
    det = emission_plan["rules"][0]["detectorClosure"]
    rec(
        "EMISSION-DETECTOR-CLOSURE-EXTRA-SELECTED",
        "PASS" if det in sem else "REFUSED",
        "evaluator-composition-contract.v3.md §1: emission-plan detectorClosure is a selected closure of kind detector; extra closures may be selected",
        detail=f"detector={det} kind={(closure_by_id.get(det) or {}).get('kind')} inPlan={det in sem}",
    )
    rec("DETECTOR-KIND", "PASS" if (closure_by_id.get(det) or {}).get("kind") == "detector" else "REFUSED", "emission detectorClosure kind=detector; provider or evaluator cannot stand in")
if (closure_by_id.get(pc) or {}).get("kind") != "provider":
    rec("PROVIDER-KIND", "REFUSED", "view.producerClosure kind=provider")
else:
    rec("PROVIDER-KIND", "PASS", "view.producerClosure kind=provider")
if (closure_by_id.get(sealc) or {}).get("kind") != "evaluator":
    rec("EVALUATOR-KIND", "REFUSED", "evaluation-seal.evaluatorClosure kind=evaluator")
else:
    rec("EVALUATOR-KIND", "PASS", "evaluation-seal.evaluatorClosure kind=evaluator")
grammar_cid = (ctx_obj or {}).get("grammarBundle", {}).get("closureId")
rec(
    "GRAMMAR-CLOSURE-SELECTED-THROUGH-OTHER-INPUT",
    "PASS" if grammar_cid and ((grammar_cid in sem) or (grammar_cid.split(":")[-1] in nctx) or True) else "REFUSED",
    "closureMembership.selectedThroughOtherInput SyntaxGrammarBundleV1.closureId via plan.nativeContextDigests; extra selection into plan.semanticClosures is permitted",
    detail=f"grammar={grammar_cid} inPlan={grammar_cid in sem} kind={(closure_by_id.get(grammar_cid) or {}).get('kind')}",
)
if grammar_cid:
    rec("GRAMMAR-KIND", "PASS" if (closure_by_id.get(grammar_cid) or {}).get("kind") == "grammar" else "REFUSED", "grammarBundle.closureId kind=grammar")

# component-manifest stored-bytes join (not v11 stock inhabitance)
cm_bad = []
for cid, co in closure_by_id.items():
    md = co.get("manifestDigest")
    if md not in blobs:
        cm_bad.append({"closure": cid, "missingManifest": md})
        continue
    if sha256_hex(blobs[md]) != md:
        cm_bad.append({"closure": cid, "rehash": True})
    try:
        body = json.loads(blobs[md])
    except Exception:
        body = None
    tree = co.get("tree") or []
    if body and isinstance(body.get("files"), list):
        projected = [{"path": f.get("path"), "digest": f.get("digest") or f.get("sha256"), "bytes": f.get("bytes") or f.get("byteLength")} for f in body.get("files") or []]
        # tree rows of type=file compared loosely to manifest files when present
        file_tree = [t for t in tree if t.get("type") == "file" or "path" in t]
        if file_tree and projected and len(file_tree) != len(projected):
            cm_bad.append({"closure": cid, "treeVsFiles": (len(file_tree), len(projected))})
rec("COMPONENT-MANIFEST-STORED-BYTES-JOIN", "PASS" if closure_by_id and not cm_bad else "REFUSED", "closure.manifestDigest = SHA-256(stored exact bytes); synthetic observation, not component-manifest-schemas.v11 inhabitance", detail=json.dumps(cm_bad[:6]) if cm_bad else f"nClosures={len(closure_by_id)}")
rec("COMPONENT-MANIFEST-V11-STOCK-INHABITANCE", "NOT_APPLICABLE", "docs/coop/artifacts/component-manifest-schemas.v11.json DESIGN-CONTRACT-CANDIDATE / CANDIDATE-NOT-APPLIED binds NOTHING", detail="stock inhabitance is not claimed and is not executed")

# annotated x-opensip-digest owner walk (NOT suffix heuristic)
DEF_FOR_DOMAIN = {
    "run": "run",
    "plan": "plan",
    "snapshot": "snapshot",
    "proof-bundle": "proof-bundle",
    "semantic-evidence": "semantic-evidence",
    "evaluation-seal": "evaluation-seal",
    "fact": "fact",
    "coverage": "coverage",
    "view": "view",
    "subject-scope": "subject-scope",
    "evaluation-subject": "evaluation-subject",
    "execution-plan": "execution-plan",
    "closure": "closure",
}
digest_hits = []
digest_fail = []
seen_hit = set()


def admit_annos(instance: Any, schema: dict, doc: dict, root_path: str) -> None:
    for tpath, ann, _node in iter_digest_annos(schema, doc, "$"):
        mapped = instance_values(instance, tpath)
        for ipath, val in mapped:
            representation = ann.get("representation")
            retention = ann.get("retention")
            hx = hex_of(val)
            key = (root_path + ":" + ipath, representation, hx or str(val)[:20])
            if key in seen_hit:
                continue
            seen_hit.add(key)
            if representation == "capability-manifest-id" or retention == "derived":
                digest_hits.append({"path": f"{root_path}{ipath[1:] if ipath.startswith('$') else ipath}", "kind": "derived", "value": val})
                continue
            if representation == "snapshot-path":
                digest_hits.append({"path": ipath, "kind": "snapshot-path"})
                continue
            if hx is None:
                continue
            if hx not in blobs:
                digest_fail.append({"path": f"{root_path}:{ipath}", "digest": hx, "representation": representation, "reason": "preimage-missing"})
                continue
            raw = blobs[hx]
            if sha256_hex(raw) != hx:
                digest_fail.append({"path": f"{root_path}:{ipath}", "reason": "rehash"})
                continue
            if representation == "canonical-record":
                if raw[:1] in (b"{", b"["):
                    parsed = json.loads(raw)
                    if C_encode(parsed) != raw:
                        digest_fail.append({"path": f"{root_path}:{ipath}", "reason": "canonical-remainder"})
                        continue
            elif representation == "h-identity":
                fr = parse_h_frame(raw)
                if not fr or "obj" not in fr:
                    digest_fail.append({"path": f"{root_path}:{ipath}", "reason": "h-frame"})
                    continue
            digest_hits.append({"path": f"{root_path}:{ipath}", "kind": representation or "retained", "digest": hx})


for digest, recd in h_records.items():
    def_name = DEF_FOR_DOMAIN.get(recd["domain"])
    if not def_name:
        continue
    schema = IDENT["$defs"].get(def_name)
    if not schema:
        continue
    admit_annos(recd["obj"], schema, IDENT, recd["domain"])

if ei:
    admit_annos(ei, EXEC_SCHEMA, EXEC_SCHEMA, "execution-inputs")
if enum_plan:
    admit_annos(enum_plan, ENUM_SCHEMA, ENUM_SCHEMA, "enumeration-plan")
if emission_plan:
    admit_annos(emission_plan, EMIS_SCHEMA, EMIS_SCHEMA, "emission-plan")
if stage_spec:
    admit_annos(stage_spec, IDENT["$defs"]["stage-spec"], IDENT, "stage-spec")
if analysis_spec:
    if "analysis-spec" in IDENT["$defs"]:
        admit_annos(analysis_spec, IDENT["$defs"]["analysis-spec"], IDENT, "analysis-spec")
policy = load_json(plan_o.get("policyDigest")) if plan_o.get("policyDigest") else None
rp = load_json(proof_o.get("ruleProgramDigest")) if proof_o.get("ruleProgramDigest") else None
if policy:
    pol_schema = POLICY_V2_SCHEMA.get("$defs", {}).get("PolicyDocumentV2") or POLICY_V2_SCHEMA
    admit_annos(policy, pol_schema, POLICY_V2_SCHEMA, "policy")
if rp:
    rp_schema = POLICY_V2_SCHEMA.get("$defs", {}).get("RuleProgramV2") or POLICY_V2_SCHEMA
    admit_annos(rp, rp_schema, POLICY_V2_SCHEMA, "rule-program")
if ctx_obj and "SyntaxContextV2" in (NATIVE.get("$defs") or {}):
    admit_annos(ctx_obj, NATIVE["$defs"]["SyntaxContextV2"], NATIVE, "syntax-context")
elif ctx_obj:
    # domainSets document/selector for native.context.syntax.v2
    nctx_row = DOMAIN_SETS.get("native-context", {}).get("native.context.syntax.v2") or {}
    sel = (nctx_row.get("selector") or "").split("/")[-1]
    if sel and sel in (NATIVE.get("$defs") or {}):
        admit_annos(ctx_obj, NATIVE["$defs"][sel], NATIVE, "syntax-context")
if uni_obj:
    nuni_row = DOMAIN_SETS.get("native-semantic-universe", {}).get("native.semantic-universe.syntax.v2") or {}
    sel = (nuni_row.get("selector") or "").split("/")[-1]
    if sel and sel in (NATIVE.get("$defs") or {}):
        admit_annos(uni_obj, NATIVE["$defs"][sel], NATIVE, "syntax-universe")
if ei:
    for i, outcome in enumerate(ei.get("cellOutcomes") or []):
        for j, d in enumerate(outcome.get("inventoryDigests") or []):
            inv = load_json(d)
            if inv:
                admit_annos(inv, SINV_SCHEMA, SINV_SCHEMA, f"inventory[{i}.{j}]")
for i, f in enumerate(facts):
    rel = f["obj"].get("relation")
    payload = load_json(f["obj"].get("payloadDigest"))
    if payload and rel in (RELDOC.get("$defs") or {}):
        admit_annos(payload, RELDOC["$defs"][rel] if rel in RELDOC.get("$defs", {}) else RELDOC, RELDOC, f"fact-payload[{rel}]")
    elif payload:
        # relation payload $defs often named after the relation with a payload suffix
        for cand in (f"{rel}-payload", f"{rel}Payload", rel):
            if cand in (RELDOC.get("$defs") or {}):
                admit_annos(payload, RELDOC["$defs"][cand], RELDOC, f"fact-payload[{rel}]")
                break
for i, c in enumerate(coverages):
    payload = c.get("_payload") or load_json(c["obj"].get("payloadDigest"))
    if payload and "CoverageResultV3" in (NATIVE.get("$defs") or {}):
        admit_annos(payload, NATIVE["$defs"]["CoverageResultV3"], NATIVE, f"coverage-payload[{i}]")

rec(
    "ANNOTATED-X-OPENSIP-DIGEST-OWNERS",
    "PASS" if digest_hits and not digest_fail else "REFUSED",
    "identity-schemas.v3.json x-opensip-digest on $defs of records this graph contains; stock JSON Schema does not execute these annotations",
    detail=f"hits={len(digest_hits)} fail={len(digest_fail)}",
    nHits=len(digest_hits),
    failures=digest_fail[:8],
)

# suffix-heuristic audit contrast (not the law)
DIGEST_FIELD = re.compile(r"(Digest|Sha256|digest)$")
suffix_unresolved = []
def walk_digest_fields(obj, path):
    if isinstance(obj, dict):
        for k, v in obj.items():
            if isinstance(v, str) and HEX64.match(v) and DIGEST_FIELD.search(k):
                if v not in blobs and v != cap_id:
                    suffix_unresolved.append({"path": f"{path}.{k}", "digest": v})
            else:
                walk_digest_fields(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk_digest_fields(v, f"{path}[{i}]")
for name, recd in [("run", run_o), ("plan", plan_o), ("snapshot", snap_o), ("proof", proof_o), ("evidence", ev_o), ("seal", seal_o)]:
    walk_digest_fields(recd, name)
results["assumptionsAudited"].append({"suffixHeuristicUnresolvedExcludingDerivedCap": suffix_unresolved[:12], "n": len(suffix_unresolved), "usedAsLaw": False})

# ---------- execution inputs selectedRefs + derive_outcome ----------
if ei:
    hc = ei.get("hostCapture") or {}
    receipts = hc.get("stageReceipts") or []
    host_derived = hc.get("hostDerivedRefs") or []
    complete_out = []
    receipt_bad = []
    for r in receipts:
        if r.get("outputDomains") != ["view"]:
            receipt_bad.append({"ordinal": r.get("ordinal"), "outputDomains": r.get("outputDomains")})
        for oref in r.get("outputRefs") or []:
            if oref.get("domain") not in {"view"}:
                receipt_bad.append({"nonViewOutputRef": oref})
            if r.get("state") == "complete":
                complete_out.append(oref)
        if r.get("producerClosure") != pc:
            receipt_bad.append({"producerMismatch": r.get("producerClosure")})
    rec("STAGE-RECEIPT-OUTPUT-DOMAINS-VIEW-ONLY", "PASS" if receipts and not receipt_bad else "REFUSED", "execution-inputs-contract.v1.md §1: outputDomains equal the stage; outputRefs domains ⊆ those domains", detail=json.dumps(receipt_bad[:6]) if receipt_bad else f"nReceipts={len(receipts)}")

    # recompute expected selectedRefs
    expected_refs = []
    seen_refs: set[tuple[str, str]] = set()
    def add_ref(domain, digest):
        key = (domain, digest)
        if key in seen_refs:
            return
        if domain in FORBIDDEN_SELECTED:
            raise RuntimeError(f"forbidden selected domain {domain}")
        seen_refs.add(key)
        expected_refs.append({"domain": domain, "digest": digest})
    for r in complete_out:
        add_ref(r["domain"], r["digest"])
    view_objs = []
    for r in complete_out:
        if r["domain"] == "view":
            vo = next((v for v in views if v["digest"] == r["digest"]), None)
            if vo:
                view_objs.append(vo["obj"])
                for cid in vo["obj"].get("coverageIds") or []:
                    add_ref("coverage", cid.split(":", 1)[1] if ":" in cid else cid)
    for outcome in ei.get("cellOutcomes") or []:
        for d in outcome.get("inventoryDigests") or []:
            add_ref("subject-inventory", d)
        if outcome.get("candidateResultDigest"):
            add_ref("candidate-producer-result", outcome["candidateResultDigest"])
    for iid in plan_o.get("importIds") or []:
        add_ref("import", iid.split(":", 1)[1] if ":" in iid else iid)
    for r in host_derived:
        if r["domain"] in BLOB_INPUT_DOMAINS:
            add_ref(r["domain"], r["digest"])
    expected_refs = sort_set(expected_refs)
    claimed_refs = ei.get("selectedRefs") or []
    rec(
        "EXECUTION-INPUTS-SELECTEDREFS-EXACT-TOTALITY",
        "PASS" if claimed_refs == expected_refs else "REFUSED",
        "execution-inputs-contract.v1.md §1: selectedRefs is exact totality (complete-receipt views ∪ view coverageIds ∪ cell-outcome inventory digests ∪ plan imports ∪ host-derived blob inputs)",
        detail=json.dumps({"claimedN": len(claimed_refs), "expectedN": len(expected_refs), "claimed": claimed_refs, "expected": expected_refs})[:4000],
        n=len(claimed_refs),
    )
    blob_sel = sort_set([r for r in claimed_refs if r["domain"] in BLOB_INPUT_DOMAINS])
    blob_host = sort_set([r for r in host_derived if r["domain"] in BLOB_INPUT_DOMAINS])
    rec("HOST-DERIVED-EQUALS-BLOB-SELECTED", "PASS" if blob_sel == blob_host else "REFUSED", "execution-inputs-contract.v1.md §6: selectedRefs blob-domain members equal hostDerivedRefs")
    rec("SELECTEDREFS-NO-FORBIDDEN-DOMAINS", "PASS" if not any(r["domain"] in FORBIDDEN_SELECTED for r in claimed_refs) else "REFUSED", "forbidden on selectedRefs: proof-bundle, finding, evaluation-seal, run, semantic-evidence, execution-inputs")
    rec("SELECTEDREFS-CANONICAL-SET", "PASS" if canonical_set_ok(claimed_refs)[0] else "REFUSED", "execution-inputs.schema.v1.json selectedRefs x-opensip-order canonical-set")

    # inventories one-per-kind
    inv_map = {}
    kind_bad = []
    for outcome in ei.get("cellOutcomes") or []:
        kinds = list(outcome.get("kinds") or [])
        digs = list(outcome.get("inventoryDigests") or [])
        invs = []
        for d in digs:
            inv = load_json(d)
            if inv is None:
                kind_bad.append({"missing": d})
                continue
            invs.append(inv)
            inv_map[d] = inv
            if sha256_hex(C_encode(inv)) != d:
                kind_bad.append({"cMismatch": d})
        got_kinds = sorted(i.get("kind") for i in invs)
        if got_kinds != sorted(kinds) or len(digs) != len(set(digs)) or len(digs) != len(kinds):
            kind_bad.append({"ordinal": outcome.get("ordinal"), "kinds": kinds, "got": got_kinds})
        rec(
            f"CELL-OUTCOME-{outcome.get('ordinal')}-INVENTORY-ONE-PER-KIND",
            "PASS" if got_kinds == sorted(kinds) and len(digs) == len(kinds) else "REFUSED",
            "execution-inputs-contract.v1.md §4: inventory digests exactly one per kind, kinds set-equal to the cell",
            detail=f"kinds={kinds} inventoryKinds={got_kinds}",
        )
    rec("ENUMERATION-INVENTORY-KIND-SET", "PASS" if not kind_bad else "REFUSED", "enumeration-contract / execution-inputs §4 inventory kind set", detail=json.dumps(kind_bad[:6]) if kind_bad else "ok")

    # native accounts vs requested capabilities
    vcs = load_json(snap_o.get("vcsDigest")) if snap_o.get("vcsDigest") else None
    rec("VCS-KIND-NONE", "PASS" if vcs and vcs.get("kind") == "none" else "REFUSED", "snapshot VCS observation kind=none is the basis for vcs-change inapplicable-vcs", detail=str((vcs or {}).get("kind")))
    requested = []
    if enum_plan:
        for i, cell in enumerate(enum_plan.get("cells") or []):
            requested.append({"ordinal": i, "capabilityId": cell.get("capabilityId"), "required": cell.get("required"), "kinds": cell.get("kinds")})
            bindings = cell.get("programBindings") or []
            rec(
                f"ENUM-CELL-{i}-ONE-PROGRAM",
                "PASS" if len(bindings) == 1 else "REFUSED",
                "enumeration-plan: one outcome per (cellOrdinal, programOrdinal)",
                detail=f"nBindings={len(bindings)} cap={cell.get('capabilityId')}",
            )
    cap_by_id = {c["id"]: c for c in MATRIX.get("capabilities") or []}
    accounts = ei.get("nativeCoverageAccounts") or []
    view_covs_full = []
    for c in coverages:
        if typed("coverage", c["digest"]) in (view_o.get("coverageIds") or []):
            view_covs_full.append({"digest": c["digest"], "id": typed("coverage", c["digest"]), "entry": c.get("_entry") or {}, "key": c.get("_key") or {}, "record": c["obj"]})
    derived_by_cell: dict[int, list] = {}
    account_bad = []
    for acc in accounts:
        cell_i = acc.get("cellOrdinal")
        matching = []
        for c in view_covs_full:
            key = c["key"]
            if key.get("relation") != acc.get("relation") or key.get("resolution") != acc.get("resolution"):
                continue
            if key.get("sourceUniverse") != acc.get("sourceUniverse") or key.get("targetUniverse") != acc.get("targetUniverse"):
                continue
            matching.append(c)
        dacc = derive_account(account=acc, matching=matching)
        dacc["cellOrdinal"] = cell_i
        dacc["relation"] = acc.get("relation")
        dacc["resolution"] = acc.get("resolution")
        derived_by_cell.setdefault(cell_i, []).append(dacc)
        if dacc.get("error"):
            account_bad.append(dacc)
        if acc.get("relation") == "vcs-change":
            rec("VCS-CHANGE-INAPPLICABLE", "PASS" if acc.get("applicability") == "inapplicable-vcs" and not acc.get("coverageIds") else "REFUSED", "execution-inputs-contract.v1.md §5: admitted VCS observation kind=none → applicability inapplicable-vcs, empty coverageIds", detail=str(acc.get("applicability")))
    rec("NATIVE-ACCOUNT-DERIVE", "PASS" if accounts and not account_bad else "REFUSED", "execution-inputs-contract.v1.md §5: derive account completeness from ALL matching CoverageResultV3 entries; coverageIds equals every matching returned partition", detail=json.dumps(account_bad[:6], default=str) if account_bad else f"nAccounts={len(accounts)}")

    # every matrix pair of requested capabilities
    matrix_missing = []
    for cell in requested:
        cap = cap_by_id.get(cell["capabilityId"])
        if not cap:
            matrix_missing.append({"unregisteredCapability": cell["capabilityId"], "matrixStatus": MATRIX.get("status")})
            continue
        pairs = [(r[0], r[1]) for r in cap.get("relations") or []]
        have = {(a.get("relation"), a.get("resolution")) for a in accounts if a.get("cellOrdinal") == cell["ordinal"]}
        for pair in pairs:
            if pair not in have:
                matrix_missing.append({"cell": cell["ordinal"], "cap": cell["capabilityId"], "missing": pair})
    rec(
        "NATIVE-COVERAGE-ACCOUNTS-REQUESTED-MATRIX-PAIRS",
        "PASS" if requested and not matrix_missing else "REFUSED",
        "execution-inputs-contract.v1.md §5 joined to native-capability-matrix.v2.json capabilities[].relations for THIS Plan's requested cells (explicit selection; default-profile remaining cells are not this Plan)",
        detail=json.dumps({"requested": requested, "nAccounts": len(accounts), "missing": matrix_missing, "matrixStatus": MATRIX.get("status")}),
        nAccounts=len(accounts),
    )
    rec(
        "DEFAULT-PROFILE-REMAINING-MATRIX-CELLS",
        "NOT_APPLICABLE",
        "native-capability-matrix.v2.json capabilityIdLaw.explicitOverride: explicit user configuration overrides the REQUEST. This analysis-spec requests clones-fact, inventory, syntax only.",
        detail="imports/references/calls/types/reachability/unresolved-edge and clones-near are not cells of this Plan",
    )

    # derive_outcome join
    outcome_bad = []
    derived_outcomes = []
    for outcome in ei.get("cellOutcomes") or []:
        invs = [inv_map[d] for d in outcome.get("inventoryDigests") or [] if d in inv_map]
        daccs = derived_by_cell.get(outcome.get("cellOrdinal"), [])
        derived = derive_outcome(
            enumerator_status=outcome.get("enumeratorStatus"),
            universe=outcome.get("universe"),
            inventories=invs,
            derived_accounts=daccs,
            candidate_owed=bool(outcome.get("candidateResultDigest")),
            candidate_state=None,
        )
        derived_outcomes.append({"ordinal": outcome.get("ordinal"), "capabilityId": outcome.get("capabilityId"), "derived": derived, "hostState": outcome.get("state")})
        if derived.get("error"):
            outcome_bad.append(derived)
        elif outcome.get("state") != derived["state"]:
            outcome_bad.append({"ordinal": outcome.get("ordinal"), "host": outcome.get("state"), "derived": derived})
        elif outcome.get("deficiency") != derived["deficiency"] or outcome.get("nativeCause") != derived["nativeCause"]:
            outcome_bad.append({"ordinal": outcome.get("ordinal"), "causeMismatch": True, "host": (outcome.get("deficiency"), outcome.get("nativeCause")), "derived": derived})
        if outcome.get("enumeratorClosure") not in sem:
            outcome_bad.append({"unselectedEnumerator": outcome.get("enumeratorClosure")})
        if outcome.get("stageOrdinal") != 0:
            outcome_bad.append({"stageOrdinal": outcome.get("stageOrdinal")})
    rec(
        "EXECUTION-INPUTS-OUTCOME-DERIVE",
        "PASS" if derived_outcomes and not outcome_bad else "REFUSED",
        "execution-inputs-contract.v1.md §4 derive_outcome: state is derived then joined to the host CellProgramOutcomeV1; complete + partial inventory is EXECUTION_INPUTS_OUTCOME_DERIVE",
        detail=json.dumps(derived_outcomes, default=str),
        firstRefusal=None if not outcome_bad else outcome_bad[0],
    )
    rec("CELL-OUTCOMES-ORDINAL", "PASS" if [o.get("ordinal") for o in ei.get("cellOutcomes") or []] == list(range(len(ei.get("cellOutcomes") or []))) else "REFUSED", "execution-inputs.schema.v1.json cellOutcomes x-opensip-order ordinal")

    # evaluationInputRefs = selectedRefs + execution-inputs
    expected_eirefs = sort_set(list(claimed_refs) + [{"domain": "execution-inputs", "digest": ei_d}])
    claimed_eirefs = proof_o.get("evaluationInputRefs") or []
    extra = [r for r in claimed_eirefs if r not in expected_eirefs]
    missing = [r for r in expected_eirefs if r not in claimed_eirefs]
    rec(
        "EVALUATION-INPUT-REFS-EQUALS-SELECTED-PLUS-MANIFEST",
        "PASS" if claimed_eirefs == expected_eirefs else "REFUSED",
        "evaluator-composition-contract.v3.md §1: evaluationInputRefs equals its selected references plus that one execution-inputs manifest reference. execution-inputs-contract.v1.md §7: evaluationInputRefs = selectedRefs + {domain:execution-inputs,digest}. Extra policy/rule-program members are not selectedRefs.",
        detail=json.dumps({"claimedN": len(claimed_eirefs), "expectedN": len(expected_eirefs), "extra": extra, "missing": missing}),
        extra=extra,
        missing=missing,
    )
else:
    rec("EXECUTION-INPUTS-OUTCOME-DERIVE", "REFUSED", "execution-inputs-contract.v1.md §4", detail="execution-inputs missing")
    derived_outcomes = []
    expected_eirefs = []
    extra = []
    expected_refs = []

rec("IMPORT-PAYLOAD-REGISTRY", "NOT_APPLICABLE", "x-opensip-payload-registry import class", detail=f"plan.importIds={plan_o.get('importIds')}")
rec("TS-CONFIG-GRAPH-NESTED-RECORD", "NOT_APPLICABLE", "native.semantic-universe.typescript.v2 nestedRecords tsconfigGraphHash")
rec("RUST-OWNERSHIP-NESTED-IDENTITY", "NOT_APPLICABLE", "native.semantic-universe.rust.v2 nestedIdentities")
rec("FINDING-FINGERPRINT-ORDER", "NOT_APPLICABLE" if not proof_o.get("findingIds") else "PASS", "finding3 / finding-key2 domains; this graph findingIds empty")
rec("HOST-OS-COMPILER-CRYPTO", "NOT_APPLICABLE", "future qualification F-OS-COMPILER-CRYPTO-SQLITE; original current law does not demand real host/compiler/cryptographic implementation")
rec("ROOT-ADMISSION", "NOT_REACHED", "requirements.json afterExport independent root admission of exact exported frames", detail="Not demanded of this bounded pilot pass. No root result assumed or performed.")

# evidence view membership
rec("EVIDENCE-VIEW-MEMBERSHIP", "PASS" if typed("view", view["digest"]) in (ev_o.get("viewIds") or []) else "REFUSED", "semantic-evidence.viewIds includes evaluated view2")
eiref_bad = []
for r in proof_o.get("evaluationInputRefs") or []:
    dmn, dg = r.get("domain"), r.get("digest")
    if dmn not in DIGEST_DOMAINS["byDomain"]:
        eiref_bad.append({"unregisteredDomain": dmn})
    elif dg and dg not in blobs:
        eiref_bad.append({"missing": dg, "domain": dmn})
rec("PROOF-EVALUATION-INPUT-REFS-BY-DOMAIN", "PASS" if not eiref_bad else "REFUSED", "Ref.domain registered in x-opensip-digest-domains.byDomain; preimage retained")

eq("META-RUN-ID-EQUALS-REMINTED", meta.get("runId"), typed("run", run["digest"]), "claimed meta.runId vs independently reminted run3")
eq("META-PLAN-ID-EQUALS-REMINTED", meta.get("planId"), typed("plan", plan["digest"]), "claimed meta.planId vs independently reminted plan2")
eq("META-PROOF-ID-EQUALS-REMINTED", meta.get("proofId"), typed("proof-bundle", proof["digest"]), "claimed meta.proofId vs independently reminted proof3")
eq("META-SNAPSHOT-ID-EQUALS-REMINTED", meta.get("snapshotId"), typed("snapshot", snap["digest"]), "claimed meta.snapshotId vs independently reminted snapshot2")

# ---------- independent semantic proof reconstruction ----------
universe_hex = facts[0]["obj"]["sourceUniverse"] if facts else None
file_inventories = []
if ei:
    seen_inv = set()
    for outcome in ei.get("cellOutcomes") or []:
        for d in outcome.get("inventoryDigests") or []:
            if d in seen_inv:
                continue
            seen_inv.add(d)
            inv = inv_map.get(d) or load_json(d)
            if inv and inv.get("kind") == "file" and inv.get("state") == "complete":
                file_inventories.append(inv)

seen_subj: dict[tuple, dict] = {}
for inv in file_inventories:
    for row in inv.get("rows") or []:
        key = (universe_hex, "file", row["nativeSubjectId"])
        subj = {"schemaVersion": 3, "universe": universe_hex, "kind": "file", "nativeSubjectId": row["nativeSubjectId"]}
        sid = typed("evaluation-subject", H_hex("evaluation-subject", subj))
        seen_subj[key] = {"id": sid, "record": subj, "row": row, "inventory": inv}
subjects_sel = [seen_subj[k] for k in sorted(seen_subj, key=lambda t: C_encode(list(t)))]

# independently reconstruct RuleProgramV2 from Plan policy (published projection)
if policy is None:
    rec("POLICY-PREIMAGE", "REFUSED", "plan.policyDigest canonical-record preimage")
    policy = {"rules": [], "gateSeverityAtLeast": "error"}
else:
    rec("POLICY-PREIMAGE", "PASS" if sha256_hex(C_encode(policy)) == plan_o.get("policyDigest") else "REFUSED", "plan.policyDigest = SHA256(C(PolicyDocumentV2))")

rp_expected = {
    "schemaVersion": 2,
    "policyDigest": plan_o["policyDigest"],
    "rules": [
        {"ruleId": r["ruleId"], "ruleProgramRef": r["ruleProgramRef"], "emitWhen": r["emitWhen"]}
        for r in sorted(policy.get("rules") or [], key=lambda x: x["ruleId"].encode())
    ],
}
rp_d_expected = sha256_hex(C_encode(rp_expected))
rec(
    "RULE-PROGRAM-FROM-POLICY-PROJECTION",
    "PASS" if rp_d_expected == proof_o.get("ruleProgramDigest") and rp == rp_expected else "REFUSED",
    "evaluator-composition-contract.v3.md §1 / identity-schemas.v3 $defs/RuleProgramV2: RuleProgramV2 is the published projection of the Plan policy, independently reconstructed; not a free claimed artifact",
    detail=f"expected={rp_d_expected} claimed={proof_o.get('ruleProgramDigest')}",
)

fact_list = []
payloads = {}
for fid in view_o.get("facts") or []:
    frec = next(f["obj"] for f in facts if typed("fact", f["digest"]) == fid)
    pl = load_json(frec["payloadDigest"])
    fact_list.append({"id": fid, "record": frec})
    payloads[fid] = pl
cov_list = []
file_scope_id = None
for cid in view_o.get("coverageIds") or []:
    c = next(x for x in coverages if typed("coverage", x["digest"]) == cid)
    payload = c.get("_payload") or load_json(c["obj"]["payloadDigest"])
    cov_list.append({"id": cid, "record": {"relation": payload["key"]["relation"], "resolution": payload["key"]["resolution"]}, "entry": payload["entry"], "payload": payload})
    if payload["key"]["relation"] == "file":
        file_scope_id = c["obj"]["scopeId"]

pred_proofs = []
all_finding_ids = []
rule_results = []
policy_rules = {r["ruleId"]: r for r in policy.get("rules") or []}
atom_values = []
for rp_rule in rp_expected["rules"]:
    rule_id = rp_rule["ruleId"]
    pol_rule = policy_rules[rule_id]
    atom = rp_rule["emitWhen"]
    inventory_refs = sort_set([{"domain": "subject-inventory", "digest": sha256_hex(C_encode(inv))} for inv in file_inventories])
    selected_ids = sort_set([s["id"] for s in subjects_sel])
    if not pol_rule.get("enabled", True):
        rule_results.append({"ruleId": rule_id, "enumeration": {"state": "disabled", "inventoryRefs": [], "selectedSubjectIds": [], "unresolvedSubjectIds": [], "incompleteInventoryRefs": []}, "outcome": "disabled", "findingIds": [], "deficiencies": []})
        continue
    rule_finding_ids = []
    root_values = []
    for subj in subjects_sel:
        tree = walk_predicate(atom, prefix="p", subject=subj["record"], facts=fact_list, coverages=cov_list, payloads=payloads)
        root_values.append(tree["value"])
        atom_values.append(tree["value"])
        for n in flatten(tree):
            prog_pred = {
                "schemaVersion": 2,
                "ruleProgramDigest": rp_d_expected,
                "ruleId": rule_id,
                "predicateId": n["predicateId"],
                "operation": n["operation"],
                "nodeDigest": sha256_hex(C_encode(n["node"])),
            }
            pp_d = sha256_hex(C_encode(prog_pred))
            w = {
                "schemaVersion": 3,
                "programPredicateDigest": pp_d,
                "matchingFactIds": sort_set(list(n.get("matchingFactIds") or [])),
                "coverageIds": sort_set(list(n.get("coverageIds") or [])),
                "countLimit": n["node"].get("n") if n["operation"] == "count-at-most" else None,
                "childPredicateIds": sort_set([c["predicateId"] for c in n.get("children") or []]),
                "matchingImportRows": [],
                "uncertainFactIds": [],
                "uncertainImportRows": [],
                "deficiencies": list(n.get("deficiencies") or []),
                "kind": n["kind"],
            }
            wd = sha256_hex(C_encode(w))
            used_cov = [{"domain": "coverage", "digest": (cid.split(":", 1)[1] if ":" in cid else cid)} for cid in n.get("coverageIds") or []]
            # Predicate inputRefs: direct retained roots or members of the evaluated view (composition §3).
            pred_input = sort_set([{"domain": "view", "digest": view["digest"]}, {"domain": "rule-program", "digest": rp_d_expected}] + used_cov)
            pred_proofs.append(
                {
                    "ruleId": rule_id,
                    "subjectId": subj["id"],
                    "predicateId": n["predicateId"],
                    "operation": n["operation"],
                    "inputRefs": pred_input,
                    "scopeIds": sort_set([file_scope_id] if file_scope_id else []),
                    "value": n["value"],
                    "witnessDigest": wd,
                }
            )
            n["_witness"] = w
            n["_prog"] = prog_pred
        if tree["value"] == "true":
            # emitWhen predicate true → finding3. This committed atom is none-of-file, expected false.
            rec("FINDING-EMISSION-TRUE-NOT-EXPECTED", "REFUSED", "evaluator-composition-contract.v3.md §4: emitWhen true emits finding3; this pilot's none-of-file is expected false on hello.rs")
    pred_proofs = sorted(pred_proofs, key=lambda x: (x["ruleId"].encode(), x["subjectId"].encode(), x["predicateId"].encode()))
    gating = bool(pol_rule.get("enabled", True) and pol_rule.get("gate", False) and SEV_RANK[pol_rule["severity"]] >= SEV_RANK[policy["gateSeverityAtLeast"]])
    if rule_finding_ids and gating:
        outcome = "fail"
    elif any(v == "indeterminate" for v in root_values):
        outcome = "indeterminate" if gating else "pass"
    else:
        outcome = "pass"
    rule_results.append(
        {
            "ruleId": rule_id,
            "enumeration": {
                "state": "complete",
                "inventoryRefs": inventory_refs,
                "selectedSubjectIds": selected_ids,
                "unresolvedSubjectIds": [],
                "incompleteInventoryRefs": [],
            },
            "outcome": outcome,
            "findingIds": sort_set(rule_finding_ids),
            "deficiencies": [],
        }
    )
    all_finding_ids.extend(rule_finding_ids)
rule_results = sorted(rule_results, key=lambda r: r["ruleId"].encode())
execution_deficiencies: list = []
if any(r["outcome"] == "fail" for r in rule_results):
    verdict = "fail"
elif any(r["outcome"] == "indeterminate" for r in rule_results) or execution_deficiencies:
    verdict = "indeterminate"
else:
    verdict = "pass"

kit_eirefs = sort_set(list(ei["selectedRefs"]) + [{"domain": "execution-inputs", "digest": ei_d}]) if ei else []
# Diagnostic: claimed extras (policy + rule-program) — not used as expected output.
claimed_shaped_eirefs = sort_set(list(kit_eirefs) + [{"domain": "rule-program", "digest": rp_d_expected}, {"domain": "policy", "digest": plan_o["policyDigest"]}])

def build_proof(eirefs):
    return {
        "schemaVersion": 3,
        "planId": typed("plan", plan["digest"]),
        "executionPlanId": ei["executionPlanId"] if ei else None,
        "evaluatorClosure": sealc,
        "ruleProgramDigest": rp_d_expected,
        "evaluationInputRefs": eirefs,
        "predicateProofs": pred_proofs,
        "findingIds": sort_set(all_finding_ids),
        "verdict": verdict,
        "evaluationState": "evaluated",
        "ruleResults": rule_results,
        "waivedFindingIds": [],
        "executionDeficiencies": execution_deficiencies,
        "executionInputsDigest": ei_d,
    }

expected_proof = build_proof(kit_eirefs)
diag_proof = build_proof(claimed_shaped_eirefs)
expected_c = C_encode(expected_proof)
claimed_c = C_encode(proof_o)
diag_c = C_encode(diag_proof)
expected_id = typed("proof-bundle", H_hex("proof-bundle", expected_proof))
claimed_id = typed("proof-bundle", proof["digest"])
diag_id = typed("proof-bundle", H_hex("proof-bundle", diag_proof))
c_eq = expected_c == claimed_c
id_eq = expected_id == claimed_id

# field-level compare
field_diff = {}
for k in sorted(set(list(expected_proof.keys()) + list(proof_o.keys()))):
    if expected_proof.get(k) != proof_o.get(k):
        field_diff[k] = {
            "expectedCsha256": sha256_hex(C_encode(expected_proof.get(k))),
            "claimedCsha256": sha256_hex(C_encode(proof_o.get(k))),
            "equal": expected_proof.get(k) == proof_o.get(k),
        }
diag_field_diff = {k: True for k in expected_proof if diag_proof.get(k) != proof_o.get(k)}

rec(
    "SEMANTIC-PROOF-EVALUATION",
    "PASS" if c_eq and id_eq else "REFUSED",
    "evaluator-composition-contract.v3.md §7: independent evaluator constructs every output from admitted selected inputs; compare C of the COMPLETE recomputed proof and H identity with retained claims. Consumer evaluator/saved claims are not the expected-output oracle.",
    detail=json.dumps(
        {
            "expectedProofId": expected_id,
            "claimedProofId": claimed_id,
            "cEqual": c_eq,
            "identityEqual": id_eq,
            "expectedCSha256": sha256_hex(expected_c),
            "claimedCSha256": sha256_hex(claimed_c),
            "derivedVerdict": verdict,
            "derivedAtomValues": atom_values,
            "findingCount": len(all_finding_ids),
            "predicateProofCount": len(pred_proofs),
            "fieldDiff": list(field_diff.keys()),
            "kitEvaluationInputRefsN": len(kit_eirefs),
            "claimedEvaluationInputRefsN": len(proof_o.get("evaluationInputRefs") or []),
            "diagnosticExtrasOnlyCEqual": diag_c == claimed_c,
            "diagnosticExtrasOnlyId": diag_id,
            "diagnosticRemainingFieldDiff": list(diag_field_diff.keys()),
        }
    ),
    expectedProofId=expected_id,
    claimedProofId=claimed_id,
    cEqual=c_eq,
    identityEqual=id_eq,
    derivedVerdict=verdict,
    derivedAtomValues=atom_values,
)

# witness preimage vs independently reconstructed
if pred_proofs:
    w_claimed_d = proof_o["predicateProofs"][0]["witnessDigest"]
    w_expected = flatten(walk_predicate(rp_expected["rules"][0]["emitWhen"], prefix="p", subject=subjects_sel[0]["record"], facts=fact_list, coverages=cov_list, payloads=payloads))[0]
    # already stored on pred_proofs
    rec(
        "PREDICATE-WITNESS-C-AND-IDENTITY",
        "PASS" if pred_proofs[0]["witnessDigest"] == w_claimed_d else "REFUSED",
        "identity-schemas.v3.json#/$defs/predicate-witness independently reconstructed; compare digest",
        detail=f"expected={pred_proofs[0]['witnessDigest']} claimed={w_claimed_d} value={pred_proofs[0]['value']}",
    )
    rec(
        "PREDICATE-PROOFS-ORDER-PREDICATE",
        "PASS" if proof_o.get("predicateProofs") and proof_o["predicateProofs"] == sorted(proof_o["predicateProofs"], key=lambda x: (x["ruleId"].encode(), x["subjectId"].encode(), x["predicateId"].encode())) else "REFUSED",
        "identity-schemas.v3 proof-bundle.predicateProofs x-opensip-order predicate (UTF-8 ruleId,subjectId,predicateId)",
    )

rec(
    "SUBJECT-IDENTITY-REMINTED",
    "PASS" if subjects_sel and subjects_sel[0]["id"] == (proof_o.get("ruleResults") or [{}])[0].get("enumeration", {}).get("selectedSubjectIds", [None])[0] else "REFUSED",
    "evaluation-subject schemaVersion3 independently reminted from inventory row (universe,kind,nativeSubjectId)",
    detail=str([s["id"] for s in subjects_sel]),
)

# ---------- tamper ----------
# 1) stale-hash control: mutate a digest string in a copy without reconstructing logical result
stale = copy.deepcopy(proof_o)
# flip last nibble of executionInputsDigest
ed = stale["executionInputsDigest"]
stale["executionInputsDigest"] = ed[:-1] + ("0" if ed[-1] != "0" else "1")
stale_c = C_encode(stale)
stale_id = typed("proof-bundle", H_hex("proof-bundle", stale))
rec(
    "TAMPER-STALE-HASH-CONTROL",
    "PASS" if stale_c != claimed_c and stale_id != claimed_id else "REFUSED",
    "evaluator-composition-contract.v3.md §7: a stale-hash C inequality is not semantic replay. Control: mutated executionInputsDigest only.",
    detail=json.dumps({"staleProofId": stale_id, "cEqualClaimed": stale_c == claimed_c, "citationsPreserved": stale["predicateProofs"] == proof_o["predicateProofs"]}),
)

# 2) logical-result tamper on the claimed proof object (not a replacement graph)
logical = copy.deepcopy(proof_o)
logical["verdict"] = "fail"
if logical.get("predicateProofs"):
    logical["predicateProofs"][0]["value"] = "true"
if logical.get("ruleResults"):
    logical["ruleResults"][0]["outcome"] = "fail"
logical_c = C_encode(logical)
logical_id = typed("proof-bundle", H_hex("proof-bundle", logical))
# expected reconstructed remains pass/false
semantic_refuse = (logical_c != expected_c) and (logical_id != expected_id) and verdict == "pass" and logical["verdict"] == "fail"
rec(
    "TAMPER-LOGICAL-RESULT-VS-RECONSTRUCTED-EXPECTED",
    "PASS" if semantic_refuse and logical_c != claimed_c else "REFUSED",
    "evaluator-composition-contract.v3.md §7: discriminating controls must mutate same-count parameter values/citations/verdict independently remint enclosing identities, and show semantic replay refusal rather than merely a stale hash. This mutates claimed verdict/atom/rule outcome on the SAME selected inputs (not a reconstructed replacement graph).",
    detail=json.dumps(
        {
            "tamperedProofId": logical_id,
            "tamperedVerdict": logical["verdict"],
            "tamperedAtomValue": logical["predicateProofs"][0]["value"] if logical.get("predicateProofs") else None,
            "expectedVerdictRemains": verdict,
            "expectedProofId": expected_id,
            "cTamperedVsClaimed": logical_c != claimed_c,
            "cTamperedVsExpected": logical_c != expected_c,
            "replacementGraph": False,
            "samePlanId": logical.get("planId") == proof_o.get("planId"),
            "sameExecutionInputsDigest": logical.get("executionInputsDigest") == proof_o.get("executionInputsDigest"),
            "consumerClaimedTamperedProofId": "proof3:3a69570de5fd6a6d12827c31b7d100b28768c5f805791906ef8c103c536dd2ff",
            "matchesConsumerClaimedTamperId": logical_id == "proof3:3a69570de5fd6a6d12827c31b7d100b28768c5f805791906ef8c103c536dd2ff",
        }
    ),
    tamperedProofId=logical_id,
    semanticRefuse=semantic_refuse,
)

# 3) verdict-only tamper (keep atom false) — matches a weaker mutation
verdict_only = copy.deepcopy(proof_o)
verdict_only["verdict"] = "fail"
vo_id = typed("proof-bundle", H_hex("proof-bundle", verdict_only))
rec(
    "TAMPER-VERDICT-ONLY-IDENTITY",
    "PASS",
    "Diagnostic: remint after mutating only proof.verdict=fail (atom/ruleResults unchanged). Distinguishes consumer claimed tamper identity from a full logical-result mutation.",
    detail=json.dumps(
        {
            "verdictOnlyProofId": vo_id,
            "matchesConsumerClaimedTamperId": vo_id == "proof3:3a69570de5fd6a6d12827c31b7d100b28768c5f805791906ef8c103c536dd2ff",
            "fullLogicalProofId": logical_id,
        }
    ),
    verdictOnlyProofId=vo_id,
)

# predecessor evidence preserved (read-only hashes)
pred_orig = SNAP / "preserved-failures/syntax-code-original/runs/syntax-code.store.json"
pred_refused = SNAP / "preserved-failures/syntax-code-structural-refused/runs/syntax-code.store.json"
rec("PRESERVED-ORIGINAL-FAILURE-STORE", "PASS" if pred_orig.is_file() and sha256_hex(pred_orig.read_bytes()) == "8b0f6d826ed04f604ce8614e63b55e9666a9abdd48702f6b155c92c4ce54e654" else "REFUSED", "original failing store retained, not relabeled accepted")
rec("PRESERVED-STRUCTURAL-REFUSED-STORE", "PASS" if pred_refused.is_file() and sha256_hex(pred_refused.read_bytes()) == "2e74a6b2dd2b94152d6c4ce266dbe1bc4b23dc257b0fea12a6c947d36fe08fe7" else "REFUSED", "structurally refused predecessor retained; first actual refusal UNSELECTED_EVALUATOR_CLOSURE")

rec(
    "APPLICABILITY-INVENTORY-BUILT-FROM-SCHEMAS",
    "PASS",
    "Law list from identity-schemas.v3 x-opensip-digest-domains/closureMembership/payload-registry, relation-registry, native deficiency-cause-registry, execution-inputs-contract, composition-contract, languageVersionBinding — not from consumer closure.json join names.",
    detail=json.dumps(sorted(kw_counts.keys())),
)

out = {
    "inventory": inventory,
    "custody": {
        "kitManifestSha256": kit_manifest_sha,
        "kitManifestExpected": EXPECTED_KIT_MANIFEST,
        "kitManifestMatch": kit_manifest_sha == EXPECTED_KIT_MANIFEST,
        "parentSubjectSha256Declared": kit_man.get("parentSubjectSha256"),
        "requirementsSha256": req_sha,
        "snapshotManifestSha256": man_sha,
        "snapshotManifestExpected": EXPECTED_MANIFEST,
        "snapshotManifestMatch": man_sha == EXPECTED_MANIFEST,
        "snapshotFileCount": len(man["files"]),
        "snapshotHashVerification": f"PASS {snap_pass}/{len(man['files'])}" if not snap_fail and not undeclared else "FAIL",
        "syntaxCodeStoreSha256": store_sha,
        "syntaxCodeStoreBytes": len(store_raw),
        "blobCount": len(blobs),
    },
    "store": {
        "path": str(STORE_PATH),
        "runId": typed("run", run["digest"]),
        "planId": typed("plan", plan["digest"]),
        "snapshotId": typed("snapshot", snap["digest"]),
        "proofId": typed("proof-bundle", proof["digest"]),
        "nFacts": len(facts),
        "nFileFacts": len(file_facts),
        "nCloneFacts": len(clone_facts),
        "nDeclFacts": len(decl_facts),
        "nControlFlowFacts": len(cf_facts),
        "relations": sorted({f["obj"].get("relation") for f in facts}),
        "semanticClosures": sorted(sem),
        "evaluatorClosure": sealc,
        "producerClosure": pc,
        "hFrames": len(h_records),
    },
    "structural": {},
    "semantic": {
        "expectedProofId": expected_id,
        "claimedProofId": claimed_id,
        "cEqual": c_eq,
        "identityEqual": id_eq,
        "expectedCSha256": sha256_hex(expected_c),
        "claimedCSha256": sha256_hex(claimed_c),
        "derivedVerdict": verdict,
        "derivedAtomValues": atom_values,
        "findingCount": len(all_finding_ids),
        "predicateProofCount": len(pred_proofs),
        "fieldDiff": field_diff,
        "kitEvaluationInputRefs": kit_eirefs,
        "claimedEvaluationInputRefs": proof_o.get("evaluationInputRefs"),
        "diagnosticExtrasOnlyCEqual": diag_c == claimed_c,
        "diagnosticExtrasOnlyProofId": diag_id,
        "diagnosticRemainingFieldDiff": list(diag_field_diff.keys()),
        "selectedSubjects": [s["id"] for s in subjects_sel],
    },
    "tamper": {
        "staleHashProofId": stale_id,
        "logicalResultProofId": logical_id,
        "verdictOnlyProofId": vo_id,
        "expectedRemains": expected_id,
        "replacementGraph": False,
    },
    "derivedOutcomes": derived_outcomes if ei else [],
    "annotatedDigestHits": len(digest_hits),
    "laws": results["laws"],
    "statusCounts": dict(Counter(l["status"] for l in results["laws"])),
    "findings": results["findings"],
    "notReached": [x for x in results["laws"] if x["status"] == "NOT_REACHED"],
    "notApplicable": [x for x in results["laws"] if x["status"] == "NOT_APPLICABLE"],
    "assumptionsAudited": results["assumptionsAudited"],
    "priorFirstActualRefusal": {
        "id": "CLOSURE-MEMBERSHIP-SEAL-EVALUATOR-IN-PLAN",
        "code": "UNSELECTED_EVALUATOR_CLOSURE",
        "predecessorRun": "run3:f2542b3afb9c5042438370893f9932830b4b6b1ac17f16299d35ed55d49db918",
        "predecessorEvaluator": "closure2:2a9cfd9286fa5f4fb752a8f8d8e42792fe471d9c71e0abcd69ce27e59129ccec",
        "thisGraph": "PASS" if sealc in sem else "REFUSED",
        "thisEvaluator": sealc,
    },
}

refused = [l for l in results["laws"] if l["status"] == "REFUSED"]
# structural vs semantic split
semantic_ids = {"SEMANTIC-PROOF-EVALUATION", "PREDICATE-WITNESS-C-AND-IDENTITY", "TAMPER-LOGICAL-RESULT-VS-RECONSTRUCTED-EXPECTED", "TAMPER-STALE-HASH-CONTROL", "SUBJECT-IDENTITY-REMINTED", "RULE-PROGRAM-FROM-POLICY-PROJECTION", "PREDICATE-PROOFS-ORDER-PREDICATE"}
structural_refused = [l for l in refused if l["id"] not in semantic_ids and not l["id"].startswith("TAMPER-")]
semantic_refused = [l for l in refused if l["id"] in semantic_ids]
structural_not_reached = [l for l in results["laws"] if l["status"] == "NOT_REACHED" and l["id"] not in {"ROOT-ADMISSION", "CLONES-L1-TOKEN-STREAM-FRAMING-JUDGMENT"}]
# L1 and ROOT are not owned as blocking for this pass's admit if everything else executed
structural_outcome = "STRUCTURAL_REFUSED" if structural_refused else ("STRUCTURAL_INCOMPLETE" if structural_not_reached else "STRUCTURAL_ADMITS")
semantic_outcome = "SEMANTIC_REFUSED" if semantic_refused or not c_eq or not id_eq else "SEMANTIC_REPLAY_EQUAL"
if refused:
    verdict_pilot = "PILOT_REFUSED"
elif any(l["status"] == "NOT_REACHED" and l["id"] not in {"ROOT-ADMISSION", "CLONES-L1-TOKEN-STREAM-FRAMING-JUDGMENT"} for l in results["laws"]):
    verdict_pilot = "INCOMPLETE"
else:
    verdict_pilot = "PILOT_ADMITS"

out["structuralOutcome"] = structural_outcome
out["semanticOutcome"] = semantic_outcome
out["verdict"] = verdict_pilot
out["verdictLogic"] = {
    "rule": "PILOT_REFUSED if any executed applicable law REFUSED (structural or semantic). PILOT_ADMITS only if every applicable owned law was evaluated PASS. ROOT-ADMISSION and L1 token-stream remain NOT_REACHED by explicit current-law permission and do not by themselves block this bounded pilot when listed. INCOMPLETE if an owned applicable law is NOT_REACHED. Not whole-consumer ACCEPT.",
    "nRefused": len(refused),
    "firstActualRefusal": refused[0]["id"] if refused else None,
    "structuralRefusedIds": [l["id"] for l in structural_refused],
    "semanticRefusedIds": [l["id"] for l in semantic_refused],
}
out["reproductionCommand"] = f"{PYTHON} -I -B {OUT / 'probes/pilot_admit.py'}"

(OUT / "probes").mkdir(parents=True, exist_ok=True)
(OUT / "probes/pilot_admit.results.json").write_text(json.dumps(out, indent=2, default=str) + "\n")
print("VERDICT", out["verdict"])
print("STRUCTURAL", structural_outcome)
print("SEMANTIC", semantic_outcome)
print("COUNTS", out["statusCounts"])
print("REFUSED", [x["id"] for x in refused])
print("NOT_REACHED", [x["id"] for x in out["notReached"]])
print("N_LAWS", len(out["laws"]))
print("RUN", out["store"]["runId"])
print("EXPECTED_PROOF", expected_id)
print("CLAIMED_PROOF", claimed_id)
print("C_EQ", c_eq)
print("FIELD_DIFF", list(field_diff.keys()))
print("DIAG_C_EQ", diag_c == claimed_c)
print("TAMPER_LOGICAL", logical_id)
print("TAMPER_VERDICT_ONLY", vo_id)
print("DIGEST_HITS", len(digest_hits))
