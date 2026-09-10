"""Independent four-Run admission from the frozen kit.

Implements published C/H/CVE1, owning-schema registry, digest/order annotations,
domainSet nestedIdentities/nestedRecords/snapshotJoins/blobJoins/closureJoins,
relation registry laws, execution-inputs totality/derive_outcome, and complete
proof reconstruction. Consumer helper PASS is not used as an oracle.
"""
from __future__ import annotations

import base64
import copy
import hashlib
import json
from pathlib import Path
from typing import Any

from independent.kit_core import (
    AdmissionError,
    C,
    DOMAIN_PREFIX,
    H,
    NATIVE_DOMAINS,
    admit_raw,
    capability_manifest_id_from_bytes,
    cve1_decode,
    cve1_encode,
    h_frame,
    hex_of,
    parse_h_frame,
    sort_c,
    typed_id,
)
from independent.schema_and_order import (
    DOCS,
    KIT,
    file_sha256,
    kit_rel,
    load_json,
    validate_against,
    walk_order,
    _resolve_ref,
)

IDENT_REL = "foundation/identity-schemas.v3.json"
NATIVE_REL = "native/native-evidence.schemas.v2.json"
REL_REL = "foundation/relation-payload-schemas.v2.json"
EXEC_REL = "foundation/execution-inputs.schema.v1.json"
ENUM_REL = "foundation/enumeration-plan.schema.v1.json"
EMIS_REL = "foundation/evaluator-emission-plan.schema.v1.json"
SINV_REL = "foundation/subject-inventory.schema.v1.json"
POL2_REL = "workflows/schemas/policy-document.v2.schema.json"
POL1_REL = "workflows/schemas/policy-document.schema.json"
MATRIX_REL = "native/native-capability-matrix.v2.json"
IMP_REL = "workflows/schemas/imported-evidence.schema.json"

OWNING = {
    "plan": (IDENT_REL, "#/$defs/plan"),
    "run": (IDENT_REL, "#/$defs/run"),
    "snapshot": (IDENT_REL, "#/$defs/snapshot"),
    "proof-bundle": (IDENT_REL, "#/$defs/proof-bundle"),
    "evaluation-seal": (IDENT_REL, "#/$defs/evaluation-seal"),
    "semantic-evidence": (IDENT_REL, "#/$defs/semantic-evidence"),
    "view": (IDENT_REL, "#/$defs/view"),
    "fact": (IDENT_REL, "#/$defs/fact"),
    "coverage": (IDENT_REL, "#/$defs/coverage"),
    "execution-plan": (IDENT_REL, "#/$defs/execution-plan"),
    "stage-spec": (IDENT_REL, "#/$defs/stage-spec"),
    "closure": (IDENT_REL, "#/$defs/closure"),
    "subject-scope": (IDENT_REL, "#/$defs/subject-scope"),
    "evaluation-subject": (IDENT_REL, "#/$defs/evaluation-subject"),
    "import": (IDENT_REL, "#/$defs/import"),
    "analysis-spec": (IDENT_REL, "#/$defs/analysis-spec"),
}

CTX_OWNING = {
    "native.context.typescript.v2": (NATIVE_REL, "#/$defs/TypeScriptNativeContextV2"),
    "native.context.rust.v2": (NATIVE_REL, "#/$defs/NativeContextV2"),
    "native.context.syntax.v2": (NATIVE_REL, "#/$defs/SyntaxNativeContextV2"),
}
UNI_OWNING = {
    "native.semantic-universe.typescript.v2": (NATIVE_REL, "#/$defs/TypeScriptUniverseV2ResolvedInputs"),
    "native.semantic-universe.rust.v2": (NATIVE_REL, "#/$defs/RustUniverseV2ResolvedInputs"),
    "native.semantic-universe.syntax.v2": (NATIVE_REL, "#/$defs/SyntaxUniverseV2ResolvedInputs"),
}

SEV_RANK = {"note": 0, "warning": 1, "error": 2}
T, F, U = "true", "false", "indeterminate"
UNIVERSE_TOKEN = {
    "typescript": "native.semantic-universe.typescript.v2",
    "rust": "native.semantic-universe.rust.v2",
    "syntax": "native.semantic-universe.syntax.v2",
}
FORBIDDEN_SELECTED = {
    "proof-bundle",
    "finding",
    "evaluation-seal",
    "run",
    "semantic-evidence",
    "execution-inputs",
}
BLOB_INPUT_DOMAINS = {
    "subject-inventory",
    "candidate-producer-result",
    "target-attribution",
    "incoming-search",
}
INAPPLICABLE = {
    "inapplicable-vcs",
    "unsupported-typed",
    "unavailable-unselected",
    "unavailable-null-universe",
}
FACT_ID_TAG = b"opensip.fact-identity.v1"


class JoinLog:
    def __init__(self):
        self.joins = []
        self.first_refusal = None
        self.not_reached = []

    def rec(self, layer: str, name: str, ok: bool, detail: str = "", *, refuse: bool = True, diagnostic: bool = False):
        item = {"layer": layer, "name": name, "ok": bool(ok), "detail": detail}
        after = self.first_refusal is not None
        if diagnostic or (after and refuse):
            item["diagnostic"] = True
            item["acceptance"] = "notReached"
        self.joins.append(item)
        if not ok and self.first_refusal is None and refuse and not diagnostic:
            self.first_refusal = {"layer": layer, "name": name, "detail": detail}
        elif not ok and after and refuse:
            self.not_reached.append({"name": name, "reason": f"diagnostic after first refusal {self.first_refusal['layer']}:{self.first_refusal['name']}"})
        return ok

    def mark_not_reached(self, name: str, reason: str):
        self.not_reached.append({"name": name, "reason": reason})


class Store:
    def __init__(self, blobs: dict[str, bytes], object_table: dict):
        self.blobs = blobs
        self.object_table = object_table

    @classmethod
    def load(cls, path: Path) -> "Store":
        doc = json.loads(path.read_text())
        blobs = {k: base64.b64decode(v) for k, v in doc["blobs"].items()}
        return cls(blobs, doc["objectTable"])

    def rehash(self, digest: str) -> bytes:
        if digest not in self.blobs:
            raise AdmissionError("DIGEST_PREIMAGE_MISSING", digest)
        raw = self.blobs[digest]
        got = hashlib.sha256(raw).hexdigest()
        if got != digest:
            raise AdmissionError("BLOB_REHASH", f"{digest}->{got}")
        return raw

    def parse_canonical(self, digest: str) -> Any:
        raw = self.rehash(digest)
        obj = admit_raw(raw)
        if C(obj) != raw:
            raise AdmissionError("CANONICAL_REMAINDER", digest)
        return obj

    def parse_typed(self, typed: str, domain: str) -> dict:
        rec = self.object_table.get(typed)
        if rec is None:
            # maybe typed is missing from table; try hex
            hx = typed.split(":", 1)[1] if ":" in typed else typed
            frame = self.rehash(hx)
        else:
            frame = self.rehash(rec["digest"])
        parsed = parse_h_frame(frame, allowed_domains={domain})
        return parsed["value"]

    def parse_native(self, hex_or_sha: str) -> dict:
        hx = hex_of(hex_or_sha)
        if hx is None:
            raise AdmissionError("NATIVE_HEX", str(hex_or_sha))
        frame = self.rehash(hx)
        return parse_h_frame(frame)


def get_path(obj: Any, parts: list) -> Any:
    cur = obj
    for p in parts:
        if p == "[]":
            return cur if isinstance(cur, list) else None
        if not isinstance(cur, dict) or p not in cur:
            return None
        cur = cur[p]
    return cur


def collect_paths(obj: Any, parts: list) -> list[tuple[list, Any]]:
    """Walk a path that may contain [] array wildcards."""
    if not parts:
        return [([], obj)]
    p = parts[0]
    rest = parts[1:]
    if p == "[]":
        if not isinstance(obj, list):
            return []
        out = []
        for i, el in enumerate(obj):
            for path, val in collect_paths(el, rest):
                out.append(([i] + path, val))
        return out
    if not isinstance(obj, dict) or p not in obj:
        return []
    return collect_paths(obj[p], rest)


def load_kit_docs():
    return {
        "ident": load_json(IDENT_REL),
        "native": load_json(NATIVE_REL),
        "rel": load_json(REL_REL),
        "exec": load_json(EXEC_REL),
        "enum": load_json(ENUM_REL),
        "emis": load_json(EMIS_REL),
        "sinv": load_json(SINV_REL),
        "pol2": load_json(POL2_REL),
        "pol1": load_json(POL1_REL),
        "matrix": load_json(MATRIX_REL),
    }


def matrix_pairs(matrix: dict, cap_id: str) -> list[tuple[str, str]]:
    for cap in matrix.get("capabilities") or []:
        if cap["id"] == cap_id:
            return [(r[0], r[1]) for r in cap.get("relations") or []]
    raise AdmissionError("EXECUTION_INPUTS_KIND_MAP", cap_id)


def matrix_cell(matrix: dict, cap_id: str, mode: str) -> dict | None:
    for cell in matrix.get("cells") or []:
        if cell.get("capability") == cap_id and cell.get("mode") == mode:
            return cell
    return None


def dialect_table(ident: dict, uni_domain: str) -> dict | None:
    row = ident["x-opensip-digest-domains"]["domainSets"]["native-semantic-universe"].get(uni_domain)
    if not row:
        return None
    d = (row.get("languageVersionBinding") or {}).get("dialect") or {}
    if d.get("form") != "closed-suffix-table":
        return None
    return d.get("table") or {}


def suffix_variant(path: str, table: dict) -> str | None:
    best = None
    for suf in table:
        if path.endswith(suf) and (best is None or len(suf) > len(best)):
            best = suf
    return table.get(best) if best else None


def parse_u8pref(buf: bytes, i: int) -> tuple[bytes, int]:
    if i >= len(buf):
        raise AdmissionError("FACT_IDENTITY_FRAME", "trunc u8")
    n = buf[i]
    i += 1
    if i + n > len(buf):
        raise AdmissionError("FACT_IDENTITY_FRAME", "trunc payload")
    return buf[i : i + n], i + n


def parse_body_identity_frame(frame: bytes) -> dict:
    tag, i = parse_u8pref(frame, 0)
    if tag != FACT_ID_TAG:
        raise AdmissionError("FACT_IDENTITY_TAG", repr(tag))
    level_id_b, i = parse_u8pref(frame, i)
    level_version, i = parse_u8pref(frame, i)
    language_id_b, i = parse_u8pref(frame, i)
    language_version, i = parse_u8pref(frame, i)
    if i + 4 > len(frame):
        raise AdmissionError("FACT_IDENTITY_FRAME", "trunc len")
    payload_len = int.from_bytes(frame[i : i + 4], "big")
    i += 4
    if i + payload_len != len(frame):
        raise AdmissionError("FACT_IDENTITY_FRAME", "len")
    payload = frame[i:]
    rec = {
        "levelId": level_id_b.decode("ascii"),
        "levelVersion": level_version,
        "languageId": language_id_b.decode("ascii"),
        "languageVersion": language_version,
        "payload": payload,
    }
    if rec["levelId"] == "L0-verbatim":
        raw_len = int.from_bytes(payload[:4], "big")
        span = payload[4:]
        if raw_len != len(span) or payload_len != raw_len + 4:
            raise AdmissionError("L0_PAYLOAD", "")
        rec["l0Span"] = span
    return rec


def admit_digest_field(store: Store, value: Any, ann: dict, *, path: str, log: JoinLog) -> dict:
    representation = ann.get("representation")
    retention = ann.get("retention")
    if representation == "capability-manifest-id" or retention == "derived":
        return {"path": path, "ok": True, "kind": "derived"}
    if representation == "snapshot-path":
        return {"path": path, "ok": True, "kind": "snapshot-path"}
    if representation == "by-domain":
        hx = hex_of(value)
        if hx is None:
            raise AdmissionError("DIGEST_FIELD_SHAPE", f"{path}={value!r}")
        if hx not in store.blobs:
            raise AdmissionError("DIGEST_PREIMAGE_MISSING", f"{path} {hx}")
        store.rehash(hx)
        return {"path": path, "ok": True, "kind": "by-domain", "digest": hx}
    hx = hex_of(value)
    if hx is None:
        raise AdmissionError("DIGEST_FIELD_SHAPE", f"{path}={value!r}")
    raw = store.rehash(hx)
    if representation == "raw-artifact":
        return {"path": path, "ok": True, "kind": "raw-artifact", "digest": hx, "bytes": len(raw)}
    if representation == "canonical-record":
        parsed = admit_raw(raw)
        if C(parsed) != raw:
            raise AdmissionError("CANONICAL_REMAINDER", path)
        rec = ann.get("record") or {}
        document = rec.get("document")
        selector = rec.get("selector")
        stock = None
        if document and rec.get("payloadClass") is None:
            stock = validate_against(parsed, document, selector=selector or "#", label=path)
            if not stock["stockOk"]:
                raise AdmissionError("DIGEST_RECORD_SCHEMA", f"{path}: {stock['errors'][:3]}")
        return {"path": path, "ok": True, "kind": "canonical-record", "digest": hx, "stock": stock}
    if representation == "h-identity":
        domain = ann.get("domain")
        allowed = {domain} if domain else None
        if ann.get("domainSet"):
            allowed = None
        parsed = parse_h_frame(raw, allowed_domains=allowed)
        return {"path": path, "ok": True, "kind": "h-identity", "digest": hx, "domain": parsed["domain"]}
    return {"path": path, "ok": True, "kind": representation or "retained", "digest": hx}


def walk_digest_anns(store, instance, schema, doc, *, path, log) -> list:
    out = []
    schema = _resolve_ref(schema, doc)
    if not isinstance(schema, dict):
        return out
    if "x-opensip-digest" in schema and instance is not None:
        rec = admit_digest_field(store, instance, schema["x-opensip-digest"], path=path, log=log)
        out.append(rec)
    if "allOf" in schema:
        for sub in schema["allOf"]:
            out.extend(walk_digest_anns(store, instance, sub, doc, path=path, log=log))
    if schema.get("type") == "array" and isinstance(instance, list):
        items = schema.get("items") or {}
        for i, el in enumerate(instance):
            out.extend(walk_digest_anns(store, el, items, doc, path=f"{path}[{i}]", log=log))
    if schema.get("type") == "object" and isinstance(instance, dict):
        props = schema.get("properties") or {}
        addl = schema.get("additionalProperties")
        for k, v in instance.items():
            if k in props:
                out.extend(walk_digest_anns(store, v, props[k], doc, path=f"{path}.{k}", log=log))
            elif isinstance(addl, dict):
                out.extend(walk_digest_anns(store, v, addl, doc, path=f"{path}.{k}", log=log))
    return out


def snapshot_index(snapshot: dict) -> dict[str, dict]:
    idx = {}
    for row in snapshot.get("sourceInventory") or []:
        idx[row["path"]] = row
    return idx


def join_snapshot_form(store, snapshot, value, join, *, path, log):
    form = join.get("form")
    idx = snapshot_index(snapshot)
    if form == "inventoried-paths":
        seq = value if isinstance(value, list) else []
        path_field = join.get("pathField")
        for item in seq:
            pth = item[path_field] if path_field and isinstance(item, dict) else item
            if pth not in idx:
                raise AdmissionError("SNAPSHOT_JOIN_PATH", f"{path} {pth}")
        log.rec("structural", f"snapshotJoin:{path}:inventoried-paths", True, str(len(seq)))
        return
    if form == "inventoried-path":
        pth = value if isinstance(value, str) else value.get(join.get("pathField", "path"))
        if pth not in idx:
            raise AdmissionError("SNAPSHOT_JOIN_PATH", f"{path} {pth}")
        log.rec("structural", f"snapshotJoin:{path}:inventoried-path", True, pth)
        return
    if form == "inventoried-path-and-digest":
        if value is None and join.get("nullable"):
            log.rec("structural", f"snapshotJoin:{path}:nullable", True, "")
            return
        pth = value[join.get("pathField", "path")]
        dig = value[join.get("digestField", "contentSha256")]
        row = idx.get(pth)
        if row is None:
            raise AdmissionError("SNAPSHOT_JOIN_PATH", f"{path} {pth}")
        if row["sha256"] != dig:
            raise AdmissionError("SNAPSHOT_JOIN_DIGEST", f"{path} {pth}")
        log.rec("structural", f"snapshotJoin:{path}:path-and-digest", True, pth)
        return
    if form == "inventoried-file":
        pth = value[join["pathField"]]
        dig = value[join["digestField"]]
        length = value[join["lengthField"]]
        row = idx.get(pth)
        if row is None:
            raise AdmissionError("SNAPSHOT_JOIN_PATH", pth)
        if row["sha256"] != dig or row["bytes"] != length:
            raise AdmissionError("FILE_INVENTORY_JOIN", pth)
        if join.get("retainedBlob"):
            blob = store.rehash(dig)
            if len(blob) != length:
                raise AdmissionError("FILE_BLOB_LENGTH", pth)
        log.rec("structural", f"snapshotJoin:{path}:inventoried-file", True, pth)
        return
    log.rec("structural", f"snapshotJoin:{path}:{form}", True, "form-recorded")


def join_blob_form(store, obj, join, *, path, log):
    parts = list(join.get("path") or [])
    digest_field = join.get("digestField")
    length_field = join.get("lengthField")
    if not digest_field:
        return
    if parts == []:
        targets = [([], obj)]
    else:
        targets = collect_paths(obj, parts)
    for loc, node in targets:
        if not isinstance(node, dict):
            continue
        dig = node.get(digest_field)
        hx = hex_of(dig) if isinstance(dig, str) else (dig if isinstance(dig, str) else None)
        if hx is None and isinstance(dig, str) and len(dig) == 64:
            hx = dig
        if hx is None:
            continue
        raw = store.rehash(hx)
        if length_field and node.get(length_field) is not None and len(raw) != node[length_field]:
            raise AdmissionError("BLOB_JOIN_LENGTH", f"{path} {loc}")
        log.rec("structural", f"blobJoin:{path}.{digest_field}", True, hx[:12])


def _admit_one_nested_identity(store, val, spec, *, ident, log, path_label: str, snapshot=None):
    domain_sets = ident["x-opensip-digest-domains"]["domainSets"]
    ds = spec.get("domainSet")
    allowed = set((domain_sets.get(ds) or {}).keys()) if ds else None
    hx = hex_of(val)
    if hx is None:
        raise AdmissionError("NESTED_IDENTITY_SHAPE", f"{path_label}={val!r}")
    frame = store.rehash(hx)
    parsed = parse_h_frame(frame, allowed_domains=allowed)
    nested_row = (domain_sets.get(ds) or {}).get(parsed["domain"])
    if nested_row:
        document = nested_row.get("document")
        selector = nested_row.get("selector")
        if document and selector:
            stock = validate_against(parsed["value"], document, selector=selector, label=parsed["domain"])
            if not stock["stockOk"]:
                raise AdmissionError("NESTED_IDENTITY_SCHEMA", f"{parsed['domain']}: {stock['errors'][:2]}")
        join_nested_identities(
            store,
            parsed["value"],
            nested_row.get("nestedIdentities"),
            path=parsed["domain"],
            ident=ident,
            log=log,
            snapshot=snapshot,
        )
        join_nested_records(store, parsed["value"], nested_row.get("nestedRecords"), path=parsed["domain"], log=log)
        for sj in nested_row.get("snapshotJoins") or []:
            if snapshot is None:
                raise AdmissionError("SNAPSHOT_JOIN_NO_SNAPSHOT", path_label)
            sval = get_path(parsed["value"], sj["path"])
            join_snapshot_form(
                store,
                snapshot,
                sval,
                sj,
                path=parsed["domain"] + "." + ".".join(sj["path"]),
                log=log,
            )
        for bj in nested_row.get("blobJoins") or []:
            join_blob_form(store, parsed["value"], bj, path=parsed["domain"], log=log)
    log.rec("structural", f"nestedIdentity:{path_label}", True, parsed["domain"])
    return parsed


def join_nested_identities(store, obj, nested, *, path, ident, log, snapshot=None):
    for spec in nested or []:
        parts = list(spec["path"])
        if "[]" in parts:
            targets = collect_paths(obj, parts)
            if not targets:
                log.rec("structural", f"nestedIdentity:{'.'.join(parts)}:empty", True, "zero array members")
                continue
            for loc, val in targets:
                _admit_one_nested_identity(
                    store, val, spec, ident=ident, log=log, path_label=".".join(parts), snapshot=snapshot
                )
            continue
        val = get_path(obj, parts)
        if val is None:
            if spec.get("nullable"):
                log.rec("structural", f"nestedIdentity:{'.'.join(parts)}:null", True, "")
                continue
            raise AdmissionError("NESTED_IDENTITY_MISSING", str(parts))
        _admit_one_nested_identity(
            store, val, spec, ident=ident, log=log, path_label=".".join(parts), snapshot=snapshot
        )


def join_nested_records(store, obj, nested, *, path, log):
    for spec in nested or []:
        val = get_path(obj, spec["path"])
        if val is None:
            if spec.get("nullable"):
                log.rec("structural", f"nestedRecord:{'.'.join(spec['path'])}:null", True, "")
                continue
            raise AdmissionError("NESTED_RECORD_MISSING", str(spec["path"]))
        hx = hex_of(val) or (val if isinstance(val, str) and len(val) == 64 else None)
        if hx is None:
            raise AdmissionError("NESTED_RECORD_SHAPE", str(spec["path"]))
        rec = store.parse_canonical(hx)
        stock = validate_against(rec, spec["document"], selector=spec.get("selector") or "#", label=spec.get("retainedAs") or path)
        if not stock["stockOk"]:
            raise AdmissionError("NESTED_RECORD_SCHEMA", f"{spec.get('retainedAs')}: {stock['errors'][:3]}")
        for bj in spec.get("blobJoins") or []:
            join_blob_form(store, rec, bj, path=spec.get("retainedAs") or path, log=log)
        log.rec("structural", f"nestedRecord:{spec.get('retainedAs') or '.'.join(spec['path'])}", True, hx[:12])
        spec["_record"] = rec
        spec["_digest"] = hx


def join_closure_joins(store, obj, joins, *, plan_selected: set[str], closures: dict, log):
    for spec in joins or []:
        val = get_path(obj, spec["path"])
        form = spec["form"]
        kind = spec.get("kind")
        if form == "closure2-identity":
            if val not in closures:
                raise AdmissionError("CLOSURE_NOT_RETAINED", str(val))
            if kind and closures[val]["kind"] != kind:
                raise AdmissionError("CLOSURE_KIND", f"{val} {closures[val]['kind']} != {kind}")
            # selectedThroughOtherInput: need not be in plan.semanticClosures
            log.rec("structural", f"closureJoin:{'.'.join(spec['path'])}", True, f"{kind}:{val[:20]}")
        elif form == "closure2-suffix":
            hx = hex_of(val) if isinstance(val, str) else None
            if hx is None and isinstance(val, str) and len(val) == 64:
                hx = val
            typed = f"closure2:{hx}"
            if typed not in closures and hx not in {c.split(':')[1] for c in closures}:
                # may still be retained as h-identity
                rec = store.parse_native(hx)
                if rec["domain"] != "closure":
                    raise AdmissionError("CLOSURE_SUFFIX_DOMAIN", rec["domain"])
                if kind and rec["value"]["kind"] != kind:
                    raise AdmissionError("CLOSURE_KIND", f"suffix {kind}")
                closures[typed] = rec["value"]
            else:
                rec = closures.get(typed)
                if rec and kind and rec["kind"] != kind:
                    raise AdmissionError("CLOSURE_KIND", f"{typed} != {kind}")
            log.rec("structural", f"closureJoin-suffix:{'.'.join(spec['path'])}", True, kind or "")
        else:
            log.rec("structural", f"closureJoin:{form}", True, str(spec["path"]))


def admit_component_manifest(store, closure: dict, log: JoinLog):
    digest = closure["manifestDigest"]
    raw = store.rehash(digest)
    body = admit_raw(raw)
    if C(body) != raw:
        raise AdmissionError("COMPONENT_MANIFEST_NOT_C", digest)
    if set(body.keys()) <= {"schemaFamily", "schemaMajor", "compatibleClosures"}:
        raise AdmissionError("COMPONENT_MANIFEST_IS_DETECTOR_LISTING", digest)
    if body.get("kind") != "component":
        raise AdmissionError("COMPONENT_MANIFEST_KIND", str(body.get("kind")))
    if body.get("version") != closure["semanticVersion"]:
        raise AdmissionError("COMPONENT_MANIFEST_VERSION", "")
    if body.get("selectedClosureKind") != closure["kind"]:
        raise AdmissionError("COMPONENT_MANIFEST_SELECTED_KIND", "")
    expected_name = f"opensip-{closure['kind']}"
    if body.get("name") != expected_name:
        raise AdmissionError("COMPONENT_MANIFEST_NAME", "")
    plat = closure["platform"]
    split = {
        "macos-aarch64": ("macos", "arm64"),
        "macos-x86_64": ("macos", "x86_64"),
        "linux-aarch64-gnu": ("linux", "arm64"),
        "linux-x86_64-gnu": ("linux", "x86_64"),
    }
    os_name, arch = split[plat]
    chosen = next(p for p in body["platforms"] if p["os"] == os_name and p["arch"] == arch)
    projected = []
    for e in (chosen.get("tree") or {}).get("entries") or []:
        if e.get("type") != "file":
            continue
        projected.append({"path": e["path"], "sha256": e["sha256"], "bytes": e["length"]})
    projected = sorted(projected, key=lambda r: r["path"].encode())
    closure_tree = sorted(list(closure["tree"]), key=lambda r: r["path"].encode())
    if projected != closure_tree:
        raise AdmissionError("COMPONENT_MANIFEST_TREE", "")
    for row in closure["tree"]:
        blob = store.rehash(row["sha256"])
        if len(blob) != row["bytes"]:
            raise AdmissionError("TREE_MEMBER_LENGTH", row["path"])
    log.rec("structural", f"component-manifest[{closure['kind']}]", True, digest[:12])
    return {"v11Standing": "CANDIDATE-NOT-APPLIED", "stockInhabitanceClaimed": False, "signatureEnvelopeVerified": False}


def derive_account(account, matching):
    applicability = account["applicability"]
    named = sort_c(list(account.get("coverageIds") or []))
    matching_ids = sort_c([e["digest"] for e in matching])
    derived = {
        "applicability": applicability,
        "namedCoverageIds": named,
        "matchingCoverageIds": matching_ids,
        "derivedCoverage": None,
        "accountComplete": False,
        "nativeWorkIncomplete": False,
        "deficiency": None,
        "nativeCause": None,
    }
    if applicability in INAPPLICABLE:
        if named:
            raise AdmissionError("EXECUTION_INPUTS_COVERAGE_DERIVE", f"{applicability} nonempty coverageIds")
        derived["accountComplete"] = True
        return derived
    if applicability != "supported-available":
        raise AdmissionError("EXECUTION_INPUTS_COVERAGE_DERIVE", applicability)
    if named != matching_ids:
        raise AdmissionError(
            "EXECUTION_INPUTS_NATIVE_COVERAGE_TOTALITY",
            f"coverageIds {named} != matching {matching_ids}",
        )
    if not named:
        derived["nativeWorkIncomplete"] = True
        derived["accountComplete"] = False
        return derived
    states = [e["entry"]["coverage"] for e in matching]
    if any(s != "complete" for s in states):
        derived["accountComplete"] = False
        derived["derivedCoverage"] = "unknown" if "unknown" in states else "partial"
        # pick a source pair
        src = next(e for e in matching if e["entry"]["coverage"] != "complete")
        derived["deficiency"] = src["entry"].get("deficiency")
        derived["nativeCause"] = src["entry"].get("nativeCause")
        return derived
    derived["accountComplete"] = True
    derived["derivedCoverage"] = "complete"
    return derived


def derive_outcome(*, enumerator_status, universe, inventories, derived_accounts):
    if enumerator_status == "unselected" or universe is None:
        return {"state": "unavailable", "deficiency": "provider-unavailable", "nativeCause": None, "reason": "unselected"}
    inv_states = [i["state"] for i in inventories]
    if any(s == "unavailable" for s in inv_states) and not any(s in ("complete", "partial") for s in inv_states):
        src = inventories[0] if inventories else {}
        return {
            "state": "unavailable",
            "deficiency": src.get("deficiency") or "provider-unavailable",
            "nativeCause": src.get("nativeCause"),
            "reason": "provider-unavailable",
        }
    if any(s == "partial" for s in inv_states):
        src = next(i for i in inventories if i["state"] == "partial")
        return {
            "state": "partial",
            "deficiency": src.get("deficiency"),
            "nativeCause": src.get("nativeCause"),
            "reason": "inventory-partial",
        }
    for acc in derived_accounts:
        if acc["applicability"] == "supported-available" and not acc["accountComplete"]:
            return {
                "state": "partial",
                "deficiency": "required-relation-missing" if acc.get("nativeWorkIncomplete") else (acc.get("deficiency") or "resolution-incomplete"),
                "nativeCause": acc.get("nativeCause"),
                "reason": "supported-available-account-not-complete",
            }
    if any(s != "complete" for s in inv_states):
        raise AdmissionError("EXECUTION_INPUTS_OUTCOME_DERIVE", str(inv_states))
    return {"state": "complete", "deficiency": None, "nativeCause": None, "reason": "all-complete"}


def kleene_not(v):
    return F if v == T else T if v == F else U


def kleene_and(vals):
    if any(v == F for v in vals):
        return F
    if all(v == T for v in vals):
        return T
    return U


def kleene_or(vals):
    if any(v == T for v in vals):
        return T
    if all(v == F for v in vals):
        return F
    return U


def ladders_from_rel(relreg):
    return {name: row["ladder"] for name, row in relreg["relations"].items()}


def rung_ge(ladders, relation, fact_rung, min_rung):
    ladder = ladders[relation]
    if fact_rung not in ladder or min_rung not in ladder:
        return False
    return ladder.index(fact_rung) >= ladder.index(min_rung)


def occupancy_id(kind, payload, native_id):
    if kind == "file":
        return payload.get("path", native_id)
    if kind == "package":
        return payload.get("packageName", native_id)
    if kind == "symbol":
        return payload.get("declared", native_id)
    return native_id


def eval_atom(atom, *, subject, facts, coverages, payloads, ladders):
    rel = atom["relation"]
    minr = atom["minResolution"]
    op = atom["op"]
    matching = []
    for f in facts:
        if f["record"]["relation"] != rel:
            continue
        if not rung_ge(ladders, rel, f["record"]["resolution"], minr):
            continue
        pl = payloads[f["id"]]
        occ = occupancy_id(subject["kind"], pl, subject["nativeSubjectId"])
        if occ != subject["nativeSubjectId"]:
            continue
        ok = True
        for filt in atom.get("filters") or []:
            field, cmp_, val = filt["field"], filt["cmp"], filt["value"]
            if field == "subject":
                got = subject["nativeSubjectId"]
            elif field == "resolution":
                got = f["record"]["resolution"]
            else:
                got = pl.get(field)
            if cmp_ == "eq" and got != val:
                ok = False
                break
            if cmp_ == "neq" and got == val:
                ok = False
                break
        if ok:
            matching.append(f["id"])
    covs = [c for c in coverages if c["record"]["relation"] == rel and c["record"]["resolution"] == minr]
    cov_ids = [c["id"] for c in covs]
    has_cov = bool(cov_ids)
    cov_complete = any(c["entry"].get("coverage") == "complete" for c in covs)
    known = matching
    if op == "exists":
        if known:
            value = T
        elif not has_cov:
            value = U
        else:
            value = F if cov_complete else U
    elif op == "none":
        if known:
            value = F
        elif not has_cov:
            value = U
        else:
            value = T if cov_complete else U
    elif op == "count-at-most":
        n = atom["n"]
        if len(set(known)) > n:
            value = F
        elif not has_cov:
            value = U
        else:
            value = T if cov_complete and len(set(known)) <= n else U
    elif op == "all-covered":
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


def walk_predicate(node, *, prefix, **kw):
    op = node["op"]
    if op in ("exists", "none", "count-at-most", "all-covered"):
        r = eval_atom(node, **kw)
        r["predicateId"] = prefix
        r["operation"] = op
        r["children"] = []
        r["node"] = node
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


def flatten(node):
    out = [node]
    for ch in node.get("children") or []:
        out.extend(flatten(ch))
    return out


def digest_of(obj):
    return hashlib.sha256(C(obj)).hexdigest()


def compose_proof(g, *, ladders, file_subjects, complete_file_invs, execution_deficiencies):
    pred_proofs = []
    all_finding_ids = []
    rule_results = []
    policy = g["policy"]
    policy_rules = {r["ruleId"]: r for r in policy["rules"]}
    for rp_rule in g["rule_program"]["rules"]:
        rule_id = rp_rule["ruleId"]
        pol_rule = policy_rules[rule_id]
        atom = rp_rule["emitWhen"]
        inventory_refs = sort_c([{"domain": "subject-inventory", "digest": digest_of(inv)} for inv in complete_file_invs])
        selected_ids = sort_c([s["id"] for s in file_subjects])
        enum_state = "complete"
        if not pol_rule.get("enabled", True):
            rule_results.append(
                {
                    "ruleId": rule_id,
                    "enumeration": {
                        "state": "disabled",
                        "inventoryRefs": [],
                        "selectedSubjectIds": [],
                        "unresolvedSubjectIds": [],
                        "incompleteInventoryRefs": [],
                    },
                    "outcome": "disabled",
                    "findingIds": [],
                    "deficiencies": [],
                }
            )
            continue
        root_values = []
        live_findings = []
        for subj in file_subjects:
            tree = walk_predicate(
                atom,
                prefix="p",
                subject=subj["record"],
                facts=g["facts"],
                coverages=g["coverages"],
                payloads=g["payloads"],
                ladders=ladders,
            )
            root_values.append(tree["value"])
            for n in flatten(tree):
                prog_pred = {
                    "schemaVersion": 2,
                    "ruleProgramDigest": g["rule_program_digest"],
                    "ruleId": rule_id,
                    "predicateId": n["predicateId"],
                    "operation": n["operation"],
                    "nodeDigest": hashlib.sha256(C(n["node"])).hexdigest(),
                }
                pp_d = digest_of(prog_pred)
                w = {
                    "schemaVersion": 3,
                    "programPredicateDigest": pp_d,
                    "matchingFactIds": sort_c(list(n.get("matchingFactIds") or [])),
                    "coverageIds": sort_c(list(n.get("coverageIds") or [])),
                    "countLimit": None,
                    "childPredicateIds": sort_c([c["predicateId"] for c in n.get("children") or []]),
                    "matchingImportRows": [],
                    "uncertainFactIds": [],
                    "uncertainImportRows": [],
                    "deficiencies": list(n.get("deficiencies") or []),
                    "kind": n["kind"],
                }
                wd = digest_of(w)
                used_cov = []
                for cid in n.get("coverageIds") or []:
                    hex_d = cid.split(":", 1)[1] if ":" in cid else cid
                    used_cov.append({"domain": "coverage", "digest": hex_d})
                pred_proofs.append(
                    {
                        "ruleId": rule_id,
                        "subjectId": subj["id"],
                        "predicateId": n["predicateId"],
                        "operation": n["operation"],
                        "inputRefs": sort_c(
                            [
                                {"domain": "view", "digest": g["view_digest"]},
                                {"domain": "rule-program", "digest": g["rule_program_digest"]},
                            ]
                            + used_cov
                        ),
                        "scopeIds": sort_c([g["file_scope_id"]]),
                        "value": n["value"],
                        "witnessDigest": wd,
                    }
                )
        pred_proofs = sorted(
            pred_proofs,
            key=lambda x: (x["ruleId"].encode(), x["subjectId"].encode(), x["predicateId"].encode()),
        )
        gating = pol_rule.get("enabled", True) and pol_rule.get("gate", False) and SEV_RANK[pol_rule["severity"]] >= SEV_RANK[policy["gateSeverityAtLeast"]]
        if live_findings and gating:
            outcome = "fail"
        elif enum_state != "complete" or any(v == "indeterminate" for v in root_values):
            outcome = "indeterminate" if gating else "pass"
        else:
            outcome = "pass"
        rule_results.append(
            {
                "ruleId": rule_id,
                "enumeration": {
                    "state": enum_state,
                    "inventoryRefs": inventory_refs,
                    "selectedSubjectIds": selected_ids,
                    "unresolvedSubjectIds": [],
                    "incompleteInventoryRefs": [],
                },
                "outcome": outcome,
                "findingIds": sort_c(live_findings),
                "deficiencies": [],
            }
        )
    rule_results = sorted(rule_results, key=lambda r: r["ruleId"].encode())
    if any(r["outcome"] == "fail" for r in rule_results):
        verdict = "fail"
    elif any(r["outcome"] == "indeterminate" for r in rule_results) or execution_deficiencies:
        verdict = "indeterminate"
    else:
        verdict = "pass"
    eval_input_refs = sort_c(
        list(g["execution_inputs"]["selectedRefs"])
        + [{"domain": "execution-inputs", "digest": g["execution_inputs_digest"]}]
    )
    eval_input_refs_with_policy = sort_c(
        list(eval_input_refs)
        + [
            {"domain": "rule-program", "digest": g["rule_program_digest"]},
            {"domain": "policy", "digest": g["policy_digest"]},
        ]
    )
    return {
        "schemaVersion": 3,
        "planId": g["plan_id"],
        "executionPlanId": g["execution_plan_id"],
        "evaluatorClosure": g["evaluator_closure"],
        "ruleProgramDigest": g["rule_program_digest"],
        "evaluationInputRefs": eval_input_refs,
        "predicateProofs": pred_proofs,
        "findingIds": sort_c(all_finding_ids),
        "verdict": verdict,
        "evaluationState": "evaluated",
        "ruleResults": rule_results,
        "waivedFindingIds": [],
        "executionDeficiencies": sort_c(execution_deficiencies),
        "executionInputsDigest": g["execution_inputs_digest"],
        "_eval_input_refs_with_policy": eval_input_refs_with_policy,
    }


def load_graph(store: Store) -> dict:
    run_ids = sorted(k for k in store.object_table if str(k).startswith("run3:"))
    if not run_ids:
        raise AdmissionError("NO_RUN", "")
    run_id = run_ids[0]
    run = store.parse_typed(run_id, "run")
    if typed_id("run", run) != run_id:
        raise AdmissionError("RUN_H_MISMATCH", typed_id("run", run))
    seal = store.parse_typed(run["evaluationSealId"], "evaluation-seal")
    claimed_proof_id = seal["proofBundleId"]
    claimed_proof = store.parse_typed(claimed_proof_id, "proof-bundle")
    ei = store.parse_canonical(claimed_proof["executionInputsDigest"])
    plan = store.parse_typed(run["planId"], "plan")
    snapshot = store.parse_typed(run["snapshotId"], "snapshot")
    policy = store.parse_canonical(plan["policyDigest"])
    rp = {
        "schemaVersion": 2,
        "policyDigest": plan["policyDigest"],
        "rules": [
            {"ruleId": r["ruleId"], "ruleProgramRef": r["ruleProgramRef"], "emitWhen": r["emitWhen"]}
            for r in sorted(policy["rules"], key=lambda x: x["ruleId"].encode())
        ],
    }
    rp_d = digest_of(rp)
    retained_rp = store.parse_canonical(rp_d)
    enum_plan = store.parse_canonical(ei["enumerationPlanDigest"])
    view_refs = [r for r in ei["selectedRefs"] if r["domain"] == "view"]
    if len(view_refs) != 1:
        raise AdmissionError("VIEW_COUNT", str(len(view_refs)))
    view_digest = view_refs[0]["digest"]
    view = store.parse_typed(f"view2:{view_digest}", "view")
    facts = []
    payloads = {}
    for fid in view["facts"]:
        frec = store.parse_typed(fid, "fact")
        pl = store.parse_canonical(frec["payloadDigest"])
        facts.append({"id": fid, "record": frec})
        payloads[fid] = pl
    coverages = []
    file_scope_id = None
    coverages_h = []
    view_coverages_full = []
    for cid in view["coverageIds"]:
        crec = store.parse_typed(cid, "coverage")
        payload = store.parse_canonical(crec["payloadDigest"])
        coverages_h.append(crec)
        coverages.append(
            {
                "id": cid,
                "record": {"relation": payload["key"]["relation"], "resolution": payload["key"]["resolution"]},
                "entry": payload["entry"],
                "payload": payload,
                "h": crec,
            }
        )
        view_coverages_full.append(
            {"id": cid, "digest": cid.split(":", 1)[1], "record": crec, "payload": payload, "entry": payload["entry"]}
        )
        if payload["key"]["relation"] == "file":
            file_scope_id = crec["scopeId"]
    if file_scope_id is None:
        raise AdmissionError("NO_FILE_SCOPE", "")
    inv_digests = []
    for outcome in ei["cellOutcomes"]:
        inv_digests.extend(outcome["inventoryDigests"])
    for r in ei["selectedRefs"]:
        if r["domain"] == "subject-inventory":
            inv_digests.append(r["digest"])
    inventories = []
    seen = set()
    for d in inv_digests:
        if d in seen:
            continue
        seen.add(d)
        inventories.append(store.parse_canonical(d))
    ctx_hex = plan["nativeContextDigests"][0]
    ctx_parsed = store.parse_native(ctx_hex)
    ctx, ctx_domain = ctx_parsed["value"], ctx_parsed["domain"]
    uni_hex = facts[0]["record"]["sourceUniverse"]
    uni_parsed = store.parse_native(uni_hex)
    uni, uni_domain = uni_parsed["value"], uni_parsed["domain"]
    exec_plan = store.parse_typed(ei["executionPlanId"], "execution-plan")
    stage_spec = store.parse_canonical(exec_plan["stages"][0]["stageSpecDigest"])
    analysis_spec = store.parse_canonical(plan["analysisSpecDigest"])
    emission_plan = None
    scope_doc = None
    enum_from_param = None
    for p in analysis_spec["parameters"]:
        rec = store.parse_canonical(p["payloadDigest"])
        if rec.get("schemaVersion") == 1 and "rules" in rec and rec["rules"] and "detectorClosure" in rec["rules"][0]:
            emission_plan = rec
        if rec.get("schemaFamily") == "opensip.product.scope":
            scope_doc = rec
        if rec.get("schemaVersion") == 1 and "cells" in rec:
            enum_from_param = rec
    if emission_plan is None:
        raise AdmissionError("NO_EMISSION_PLAN", "")
    evidence = store.parse_typed(run["evidenceId"], "semantic-evidence")
    vcs = store.parse_canonical(snapshot["vcsDigest"])
    closures = {}
    for cid in plan["semanticClosures"]:
        closures[cid] = store.parse_typed(cid, "closure")
    extra = []
    gb = ctx.get("grammarBundle") or {}
    if isinstance(gb, dict) and gb.get("closureId"):
        extra.append(gb["closureId"])
    tc = ctx.get("toolClosure") or {}
    if isinstance(tc, dict) and tc.get("closureId"):
        extra.append(tc["closureId"])
    extra.append(emission_plan["rules"][0]["detectorClosure"])
    extra.append(ei["evaluatorClosure"])
    for cid in extra:
        if cid and cid not in closures:
            closures[cid] = store.parse_typed(cid, "closure")
    scopes_list = [store.parse_typed(sid, "subject-scope") for sid in view["scopeIds"]]
    return {
        "run_id": run_id,
        "run": run,
        "seal": seal,
        "claimed_proof_id": claimed_proof_id,
        "claimed_proof": claimed_proof,
        "execution_inputs": ei,
        "execution_inputs_digest": claimed_proof["executionInputsDigest"],
        "plan": plan,
        "plan_id": run["planId"],
        "snapshot": snapshot,
        "policy": policy,
        "policy_digest": plan["policyDigest"],
        "rule_program": retained_rp,
        "rule_program_digest": rp_d,
        "enum_plan": enum_plan,
        "view": view,
        "view_digest": view_digest,
        "facts": facts,
        "payloads": payloads,
        "coverages": coverages,
        "file_scope_id": file_scope_id,
        "inventories": inventories,
        "ctx": ctx,
        "ctx_hex": ctx_hex,
        "ctx_domain": ctx_domain,
        "uni": uni,
        "uni_hex": hex_of(uni_hex),
        "uni_domain": uni_domain,
        "evaluator_closure": ei["evaluatorClosure"],
        "execution_plan_id": ei["executionPlanId"],
        "execution_plan": exec_plan,
        "stage_spec": stage_spec,
        "analysis_spec": analysis_spec,
        "emission_plan": emission_plan,
        "scope_doc": scope_doc,
        "evidence": evidence,
        "vcs": vcs,
        "closures": closures,
        "coverages_h": coverages_h,
        "views_full": [view],
        "view_coverages_full": view_coverages_full,
        "scopes": scopes_list,
    }


def expected_applicability(matrix, cap_id, language_mode, relation, vcs):
    if relation == "vcs-change":
        return "inapplicable-vcs" if vcs.get("kind") == "none" else "supported-available"
    cell = matrix_cell(matrix, cap_id, language_mode)
    if cell is None:
        raise AdmissionError("MATRIX_CELL_MISSING", f"{cap_id}@{language_mode}")
    st = cell.get("state")
    if st == "UNSUPPORTED-TYPED":
        return "unsupported-typed"
    if st == "NOT-SELECTED":
        raise AdmissionError("REQUESTED_CAPABILITY_MODE_NOT_SELECTED", f"{cap_id}@{language_mode}")
    return "supported-available"


def _universe_hex(value) -> str | None:
    if value is None:
        return None
    hx = hex_of(value)
    if hx:
        return hx
    if isinstance(value, str) and len(value) == 64:
        return value
    return value if isinstance(value, str) else None


def execution_deficiencies_from_outcomes(ei, derived_by_outcome):
    """Retain originating typed causes. Do not rewrite native Coverage incompleteness as execution/required-cell-unsatisfied.

    execution-inputs-contract: originating deficiency/nativeCause pair is kept.
    required-cell-unsatisfied is for required *inventory* partial with otherwise complete native accounts.
    evaluator-deficiency-registry: language-tier-unsupported and input-closure-incomplete are native causes.
    universe is bare 64-hex (identity-schemas evaluation-deficiency).
    """
    defs = []
    native_causes = {
        "budget-exhausted",
        "confidence-floor-unmet",
        "coverage-unknown",
        "cross-family-edge-not-owed",
        "derivation-policy-unmet",
        "enumeration-unknown",
        "external-consumers-unknown",
        "input-closure-incomplete",
        "language-tier-unsupported",
        "missing-relation-coverage",
        "population-unknown",
        "provider-unavailable",
        "required-relation-missing",
        "resolution-incomplete",
        "scope-without-coverage",
        "selector-unbound",
        "source-target-search-unattested",
        "target-export-unknown",
        "target-kind-unknown",
        "target-metadata-unknown",
        "unavailable-program-binding",
        "uncovered-expected-source-subject",
        "unresolved-edge-target-unattributed",
    }
    for outcome, derived in zip(ei["cellOutcomes"], derived_by_outcome):
        if not outcome.get("required"):
            continue
        if derived.get("state") == "complete":
            continue
        refs = sort_c([{"domain": "subject-inventory", "digest": d} for d in outcome.get("inventoryDigests") or []])
        defic = derived.get("deficiency") or outcome.get("deficiency")
        ncause = derived.get("nativeCause") if derived.get("nativeCause") is not None else outcome.get("nativeCause")
        reason = derived.get("reason")
        if defic in native_causes:
            # Retain the originating native pair. required-cell-unsatisfied is only
            # for required inventory-partial with otherwise complete native accounts.
            source, cause = "native", defic
        elif reason == "inventory-partial":
            source, cause = "execution", "required-cell-unsatisfied"
        elif reason == "supported-available-account-not-complete":
            source, cause = "native", defic or "required-relation-missing"
        else:
            source, cause = "execution", defic or "required-cell-unsatisfied"
        defs.append(
            {
                "source": source,
                "cause": cause,
                "subjectId": None,
                "predicateId": None,
                "inputRefs": refs,
                "evidenceKind": None,
                "nativeCause": ncause,
                "universe": _universe_hex(outcome.get("universe")),
            }
        )
    return defs


def admit_one(store_path: Path, *, skip_tamper: bool = False) -> dict:
    log = JoinLog()
    kit = load_kit_docs()
    ident = kit["ident"]
    relreg = kit["rel"]["x-opensip-relation-registry"]
    matrix = kit["matrix"]
    domain_sets = ident["x-opensip-digest-domains"]["domainSets"]
    payload_reg = ident["x-opensip-payload-registry"]
    store = Store.load(store_path)
    raw_ok = True
    # RAW: every blob rehashes
    for k, raw in store.blobs.items():
        got = hashlib.sha256(raw).hexdigest()
        if got != k:
            raw_ok = False
            log.rec("raw", "blob-rehash", False, f"{k}->{got}")
            break
    else:
        log.rec("raw", "blob-rehash-all", True, str(len(store.blobs)))
    schema_ok = True
    structural_ok = True
    semantic_ok = True
    g = None
    try:
        g = load_graph(store)
        log.rec("raw", "h-frame-run-plan-proof", True, g["run_id"])
    except AdmissionError as e:
        log.rec("raw", "graph-load", False, f"{e.code}: {e}")
        raw_ok = False
        return finish(store_path, store, g, log, raw_ok, False, False, False, None)

    # schema owning records
    schema_jobs = [
        ("plan", g["plan"], *OWNING["plan"]),
        ("run", g["run"], *OWNING["run"]),
        ("snapshot", g["snapshot"], *OWNING["snapshot"]),
        ("proof", g["claimed_proof"], *OWNING["proof-bundle"]),
        ("seal", g["seal"], *OWNING["evaluation-seal"]),
        ("evidence", g["evidence"], *OWNING["semantic-evidence"]),
        ("view", g["view"], *OWNING["view"]),
        ("execution-plan", g["execution_plan"], *OWNING["execution-plan"]),
        ("stage-spec", g["stage_spec"], *OWNING["stage-spec"]),
        ("execution-inputs", g["execution_inputs"], EXEC_REL, "#"),
        ("enumeration-plan", g["enum_plan"], ENUM_REL, "#"),
        ("emission-plan", g["emission_plan"], EMIS_REL, "#"),
        ("analysis-spec", g["analysis_spec"], IDENT_REL, "#/$defs/analysis-spec"),
        ("policy", g["policy"], POL2_REL, "#/$defs/PolicyDocumentV2"),
        ("rule-program", g["rule_program"], POL2_REL, "#/$defs/RuleProgramV2"),
    ]
    for i, inv in enumerate(g["inventories"]):
        schema_jobs.append((f"inventory[{i}]", inv, SINV_REL, "#"))
    for i, f in enumerate(g["facts"]):
        schema_jobs.append((f"fact[{i}]", f["record"], *OWNING["fact"]))
    for i, c in enumerate(g["coverages_h"]):
        schema_jobs.append((f"coverage[{i}]", c, *OWNING["coverage"]))
    for i, sc in enumerate(g["scopes"]):
        schema_jobs.append((f"scope[{i}]", sc, *OWNING["subject-scope"]))
    for cid, crec in g["closures"].items():
        schema_jobs.append((f"closure[{crec['kind']}]", crec, *OWNING["closure"]))
    if g["ctx_domain"] in CTX_OWNING:
        schema_jobs.append(("native-context", g["ctx"], *CTX_OWNING[g["ctx_domain"]]))
    if g["uni_domain"] in UNI_OWNING:
        schema_jobs.append(("native-universe", g["uni"], *UNI_OWNING[g["uni_domain"]]))
    if g.get("scope_doc") is not None:
        schema_jobs.append(("scope-document", g["scope_doc"], POL1_REL, "#/$defs/ScopeDocumentV1"))
    for label, inst, rel, sel in schema_jobs:
        r = validate_against(inst, rel, selector=sel, label=label)
        ok = r["stockOk"]
        if not ok:
            schema_ok = False
        log.rec("schema", f"owning-schema:{label}", ok, "" if ok else str(r["errors"][:2]))
        if not ok and log.first_refusal and log.first_refusal["layer"] == "schema":
            pass

    # payload registry for facts
    rel_bytes_sha = file_sha256(REL_REL)
    native_bytes_sha = file_sha256(NATIVE_REL)
    for f in g["facts"]:
        rel = f["record"]["relation"]
        row = relreg["relations"][rel]
        payload = g["payloads"][f["id"]]
        r = validate_against(payload, REL_REL, selector=row["selector"], label=f"payload-{rel}")
        if not r["stockOk"]:
            schema_ok = False
            log.rec("schema", f"payload-registry:{rel}", False, str(r["errors"][:2]))
        else:
            log.rec("schema", f"payload-registry:{rel}", True, row["selector"])
        if f["record"]["resolution"] not in row["ladder"]:
            structural_ok = False
            log.rec("structural", f"relation-ladder:{rel}", False, f["record"]["resolution"])
        else:
            log.rec("structural", f"relation-ladder:{rel}", True, f["record"]["resolution"])
        if row["universeRule"] == "same-only" and f["record"]["sourceUniverse"] != f["record"]["targetUniverse"]:
            structural_ok = False
            log.rec("structural", f"universe-rule:{rel}", False, "")
        else:
            log.rec("structural", f"universe-rule:{rel}", True, row["universeRule"])
        if digest_of(payload) != f["record"]["payloadDigest"]:
            structural_ok = False
            log.rec("structural", f"payload-C:{rel}", False, "")
        else:
            log.rec("structural", f"payload-C:{rel}", True, "")
        if f["record"]["payloadSchemaDigest"] != rel_bytes_sha:
            structural_ok = False
            log.rec("structural", "payloadSchemaDigest", False, f["record"]["payloadSchemaDigest"][:16])
        else:
            log.rec("structural", "payloadSchemaDigest", True, "relation-payload.v2")
        # rungs required/forbidden
        rung_rules = (row.get("rungs") or {}).get(f["record"]["resolution"]) or {}
        for req in rung_rules.get("required") or []:
            if req not in payload or payload[req] is None:
                structural_ok = False
                log.rec("structural", f"rung-required:{rel}.{req}", False, "")
        for forb in rung_rules.get("forbidden") or []:
            if forb in payload and payload[forb] is not None:
                structural_ok = False
                log.rec("structural", f"rung-forbidden:{rel}.{forb}", False, "")
        # anchor law
        al = row["anchorLaw"]
        nanc = len(f["record"].get("anchors") or [])
        if al.get("cardinality") == 0 and nanc != 0:
            structural_ok = False
            log.rec("structural", f"anchor-cardinality:{rel}", False, str(nanc))
        elif al.get("cardinality") == 1 and nanc != 1:
            structural_ok = False
            log.rec("structural", f"anchor-cardinality:{rel}", False, str(nanc))
        elif al.get("minimum") is not None and nanc < al["minimum"]:
            structural_ok = False
            log.rec("structural", f"anchor-cardinality:{rel}", False, str(nanc))
        else:
            log.rec("structural", f"anchor-cardinality:{rel}", True, str(nanc))
        # snapshot joins
        try:
            for sj in row.get("snapshotJoins") or []:
                join_snapshot_form(store, g["snapshot"], payload, sj, path=f"fact.{rel}", log=log)
        except AdmissionError as e:
            structural_ok = False
            log.rec("structural", f"fact-snapshotJoin:{rel}", False, f"{e.code}: {e}")

    # coverage payload registry
    for c in g["coverages"]:
        pl = c["payload"]
        r = validate_against(pl, NATIVE_REL, selector="#/$defs/CoverageResultV3", label="CoverageResultV3")
        ok = r["stockOk"]
        if not ok:
            schema_ok = False
        log.rec("schema", "coverage-payload-v3", ok, "" if ok else str(r["errors"][:2]))
        if c["h"]["payloadSchemaDigest"] != native_bytes_sha:
            structural_ok = False
            log.rec("structural", "coverage-payloadSchemaDigest", False, "")
        else:
            log.rec("structural", "coverage-payloadSchemaDigest", True, "")

    # annotated digest owners
    try:
        digest_hits = []
        ident_doc = ident
        for label, inst, defn in [
            ("plan", g["plan"], "plan"),
            ("run", g["run"], "run"),
            ("snapshot", g["snapshot"], "snapshot"),
            ("proof", g["claimed_proof"], "proof-bundle"),
            ("seal", g["seal"], "evaluation-seal"),
            ("evidence", g["evidence"], "semantic-evidence"),
            ("view", g["view"], "view"),
            ("execution-plan", g["execution_plan"], "execution-plan"),
            ("stage-spec", g["stage_spec"], "stage-spec"),
        ]:
            digest_hits.extend(walk_digest_anns(store, inst, ident_doc["$defs"][defn], ident_doc, path=label, log=log))
        digest_hits.extend(walk_digest_anns(store, g["execution_inputs"], kit["exec"], kit["exec"], path="execution-inputs", log=log))
        digest_hits.extend(walk_digest_anns(store, g["enum_plan"], kit["enum"], kit["enum"], path="enum", log=log))
        digest_hits.extend(walk_digest_anns(store, g["emission_plan"], kit["emis"], kit["emis"], path="emis", log=log))
        for i, inv in enumerate(g["inventories"]):
            digest_hits.extend(walk_digest_anns(store, inv, kit["sinv"], kit["sinv"], path=f"inv[{i}]", log=log))
        for cid, crec in g["closures"].items():
            digest_hits.extend(walk_digest_anns(store, crec, ident_doc["$defs"]["closure"], ident_doc, path=f"closure[{crec['kind']}]", log=log))
        ctx_row = domain_sets["native-context"][g["ctx_domain"]]
        uni_row = domain_sets["native-semantic-universe"][g["uni_domain"]]
        digest_hits.extend(
            walk_digest_anns(store, g["ctx"], kit["native"]["$defs"][ctx_row["selector"].split("/")[-1]], kit["native"], path="ctx", log=log)
        )
        digest_hits.extend(
            walk_digest_anns(store, g["uni"], kit["native"]["$defs"][uni_row["selector"].split("/")[-1]], kit["native"], path="uni", log=log)
        )
        log.rec("structural", "annotated-digest-owners", True, f"n={len(digest_hits)}")
    except AdmissionError as e:
        structural_ok = False
        log.rec("structural", "annotated-digest-owners", False, f"{e.code}: {e}")

    # domainSet joins
    ctx_row = domain_sets["native-context"][g["ctx_domain"]]
    uni_row = domain_sets["native-semantic-universe"][g["uni_domain"]]
    selected = set(g["plan"]["semanticClosures"])
    try:
        join_closure_joins(store, g["ctx"], ctx_row.get("closureJoins"), plan_selected=selected, closures=g["closures"], log=log)
        join_nested_identities(
            store, g["ctx"], ctx_row.get("nestedIdentities"), path="ctx", ident=ident, log=log, snapshot=g["snapshot"]
        )
        join_nested_records(store, g["ctx"], ctx_row.get("nestedRecords"), path="ctx", log=log)
        for sj in ctx_row.get("snapshotJoins") or []:
            val = get_path(g["ctx"], sj["path"])
            join_snapshot_form(store, g["snapshot"], val, sj, path="ctx." + ".".join(sj["path"]), log=log)
        for bj in ctx_row.get("blobJoins") or []:
            join_blob_form(store, g["ctx"], bj, path="ctx", log=log)
        join_nested_identities(
            store, g["uni"], uni_row.get("nestedIdentities"), path="uni", ident=ident, log=log, snapshot=g["snapshot"]
        )
        join_nested_records(store, g["uni"], uni_row.get("nestedRecords"), path="uni", log=log)
        for sj in uni_row.get("snapshotJoins") or []:
            val = get_path(g["uni"], sj["path"])
            join_snapshot_form(store, g["snapshot"], val, sj, path="uni." + ".".join(sj["path"]), log=log)
        if g["uni"].get("nativeContextId") != "sha256:" + g["ctx_hex"]:
            raise AdmissionError("UNIVERSE_BINDS_CONTEXT", str(g["uni"].get("nativeContextId")))
        log.rec("structural", "universe-binds-context", True, g["ctx_domain"])
        for field in uni_row.get("contextAgreementFields") or []:
            if g["uni"].get(field) != g["ctx"].get(field):
                raise AdmissionError("CONTEXT_AGREEMENT", field)
            log.rec("structural", f"contextAgreement:{field}", True, "")
    except AdmissionError as e:
        structural_ok = False
        log.rec("structural", "domainSet-joins", False, f"{e.code}: {e}")

    # syntax grammar tree
    if g["ctx_domain"] == "native.context.syntax.v2":
        try:
            bundle = g["ctx"]["grammarBundle"]
            closure = g["closures"][bundle["closureId"]]
            if closure["kind"] != "grammar":
                raise AdmissionError("GRAMMAR_CLOSURE_KIND", closure["kind"])
            tree = {row["sha256"] for row in closure["tree"]}
            required = {"bundle": bundle["bundleDigest"], "spec": bundle["normalizer"]["specificationDigest"]}
            for gr in bundle["grammars"]:
                required[gr["grammarId"]] = gr["grammarDigest"]
            missing = [n for n, d in required.items() if d not in tree]
            if missing:
                raise AdmissionError("GRAMMAR_TREE_RETENTION", str(missing))
            if bundle["parserVersion"] != closure["semanticVersion"]:
                raise AdmissionError("PARSER_VERSION", "")
            sel = set(g["uni"].get("selectedGrammarIds") or [])
            have = {x["grammarId"] for x in bundle["grammars"]}
            if not sel <= have:
                raise AdmissionError("SELECTED_GRAMMAR_SUBSET", str(sel))
            if g["uni"].get("resolutionAttempted") is not False:
                raise AdmissionError("RESOLUTION_ATTEMPTED", str(g["uni"].get("resolutionAttempted")))
            log.rec("structural", "grammar-tree-and-selection", True, str(sorted(sel)))
        except AdmissionError as e:
            structural_ok = False
            log.rec("structural", "grammar-tree-and-selection", False, f"{e.code}: {e}")

    # closure membership
    try:
        law = ident["x-opensip-digest-domains"]["closureMembership"]
        kinds = ident["x-opensip-digest-domains"]["closureKinds"]["byField"]
        directs = {
            "view.producerClosure": [g["view"]["producerClosure"]],
            "stage-spec.producerClosure": [g["stage_spec"]["producerClosure"]],
            "subject-scope.enumeratorClosure": [sc["enumeratorClosure"] for sc in g["scopes"]],
            "evaluation-seal.evaluatorClosure": [g["seal"]["evaluatorClosure"]],
            "finding.ruleClosure": [],
            "cache-key.producerClosure": [],
        }
        for field, values in directs.items():
            expected_kind = kinds.get(field)
            for cid in values:
                if cid not in selected:
                    raise AdmissionError("UNSELECTED_DIRECT_CLOSURE", f"{field} {cid}")
                if g["closures"][cid]["kind"] != expected_kind:
                    raise AdmissionError("CLOSURE_KIND", f"{field}")
        if g["claimed_proof"]["evaluatorClosure"] != g["seal"]["evaluatorClosure"]:
            raise AdmissionError("EQUAL_TO_DIRECT_MISMATCH", "proof.evaluatorClosure")
        for f in g["facts"]:
            if f["record"]["producerClosure"] != g["view"]["producerClosure"]:
                raise AdmissionError("EQUAL_TO_DIRECT_MISMATCH", "fact.producerClosure")
        det = g["emission_plan"]["rules"][0]["detectorClosure"]
        if det not in selected:
            raise AdmissionError("UNSELECTED_DETECTOR_CLOSURE", det)
        if g["closures"][det]["kind"] != "detector":
            raise AdmissionError("CLOSURE_KIND", "detector")
        log.rec("structural", "closure-membership", True, f"selected={len(selected)}")
    except AdmissionError as e:
        structural_ok = False
        log.rec("structural", "closure-membership", False, f"{e.code}: {e}")

    # component manifests
    try:
        for cid in sorted(selected):
            admit_component_manifest(store, g["closures"][cid], log)
    except AdmissionError as e:
        structural_ok = False
        log.rec("structural", "component-manifest", False, f"{e.code}: {e}")

    # capability manifest identity
    try:
        committed = store.rehash(g["plan"]["capabilityManifestBytesDigest"])
        # CVE1 round-trip of decoded bytes
        try:
            decoded = cve1_decode(committed)
            reenc = cve1_encode(decoded)
            log.rec("raw", "cve1-roundtrip-capability-manifest", reenc == committed, str(len(committed)))
        except AdmissionError as e:
            log.rec("raw", "cve1-roundtrip-capability-manifest", False, f"{e.code}: {e}")
        cid = capability_manifest_id_from_bytes(committed)
        if cid != g["plan"]["capabilityManifestId"] or cid != g["run"]["capabilityManifestId"]:
            raise AdmissionError("CAPABILITY_MANIFEST_ID", cid)
        log.rec("structural", "capabilityManifestId-derived", True, cid[:16])
    except AdmissionError as e:
        structural_ok = False
        log.rec("structural", "capabilityManifestId-derived", False, f"{e.code}: {e}")

    # unit membership
    try:
        memb = store.parse_canonical(g["enum_plan"]["membershipDigest"])
        r = validate_against(memb, NATIVE_REL, selector="#/$defs/UnitMembershipV1", label="membership")
        if not r["stockOk"]:
            raise AdmissionError("MEMBERSHIP_SCHEMA", str(r["errors"][:3]))
        if g["ctx_domain"] == "native.context.syntax.v2":
            invented = [u for u in memb.get("units") or [] if u.get("unitKind") == "syntax-only"]
            invented += [row for row in memb.get("rows") or [] if row.get("membership") == "syntax-only" and row.get("unitOrdinal") is not None]
            if invented:
                raise AdmissionError("SYNTAX_ONLY_INVENTED_UNIT", str(invented))
            log.rec("structural", "syntax-only-membership-unitOrdinal-null", True, "")
        else:
            log.rec("structural", "unit-membership-schema", True, f"nUnits={len(memb.get('units') or [])}")
        g["membership"] = memb
    except AdmissionError as e:
        structural_ok = False
        log.rec("structural", "unit-membership", False, f"{e.code}: {e}")

    # enumeration inventories
    try:
        expected = []
        for ci, cell in enumerate(g["enum_plan"]["cells"]):
            for pb in cell["programBindings"]:
                for kind in cell["kinds"]:
                    expected.append((ci, pb["ordinal"], kind))
        present = {(inv["cellOrdinal"], inv["programOrdinal"], inv["kind"]): inv for inv in g["inventories"]}
        missing = [loc for loc in expected if loc not in present]
        extra = [k for k in present if k not in set(expected)]
        if missing or extra:
            raise AdmissionError("ENUMERATION_INVENTORY_MISSING_RECORD", f"missing={missing} extra={extra}")
        log.rec("structural", "enumeration-inventory-totality", True, str(expected))
    except AdmissionError as e:
        structural_ok = False
        log.rec("structural", "enumeration-inventory-totality", False, f"{e.code}: {e}")

    # execution inputs laws
    derived_by_outcome = []
    language_mode = None
    reqs = g["analysis_spec"].get("requestedCapabilities") or []
    if reqs:
        language_mode = reqs[0]["languageMode"]
    try:
        ei = g["execution_inputs"]
        stages = g["execution_plan"]["stages"]
        receipts = ei["hostCapture"]["stageReceipts"]
        if len(stages) != len(receipts):
            raise AdmissionError("EXECUTION_INPUTS_RECEIPT_TOTALITY", "")
        for st, rec in zip(stages, receipts):
            if rec["ordinal"] != st["ordinal"] or rec["outputDomains"] != st["outputDomains"] or rec["stageSpecDigest"] != st["stageSpecDigest"]:
                raise AdmissionError("EXECUTION_INPUTS_STAGE_PRODUCER", "")
            for r in rec["outputRefs"]:
                if r["domain"] not in rec["outputDomains"]:
                    raise AdmissionError("EXECUTION_INPUTS_OUTPUT_BACKLINK", r["domain"])
        log.rec("structural", "receipt-totality", True, str(len(receipts)))
        for st in stages:
            if set(st["outputDomains"]) != {"view"}:
                raise AdmissionError("EXECUTION_INPUTS_HOST_DERIVED", str(st["outputDomains"]))
        log.rec("structural", "stage-outputDomains-view-only", True, "view")
        complete_output_refs = []
        for rec in receipts:
            if rec["state"] == "complete":
                complete_output_refs.extend(rec["outputRefs"])
        expected_selected = []
        seen = set()

        def add(domain, digest):
            key = (domain, digest)
            if key in seen:
                return
            seen.add(key)
            expected_selected.append({"domain": domain, "digest": digest})

        for r in complete_output_refs:
            if r["domain"] in FORBIDDEN_SELECTED:
                raise AdmissionError("EXECUTION_INPUTS_SELECTED_COVER", r["domain"])
            add(r["domain"], r["digest"])
        for view in g["views_full"]:
            for cid in view.get("coverageIds") or []:
                add("coverage", cid.split(":", 1)[1] if ":" in cid else cid)
        for outcome in ei["cellOutcomes"]:
            for d in outcome.get("inventoryDigests") or []:
                add("subject-inventory", d)
        for iid in g["plan"].get("importIds") or []:
            add("import", iid.split(":", 1)[1] if ":" in iid else iid)
        for r in ei["hostCapture"]["hostDerivedRefs"]:
            if r["domain"] in BLOB_INPUT_DOMAINS:
                add(r["domain"], r["digest"])
        expected_selected = sort_c(expected_selected)
        if sort_c(ei["selectedRefs"]) != expected_selected:
            raise AdmissionError("EXECUTION_INPUTS_SELECTED_COVER", "selectedRefs != totality")
        log.rec("structural", "selectedRefs-exact-totality", True, str(len(expected_selected)))
        blob_sel = sort_c([r for r in ei["selectedRefs"] if r["domain"] in BLOB_INPUT_DOMAINS])
        blob_host = sort_c([r for r in ei["hostCapture"]["hostDerivedRefs"] if r["domain"] in BLOB_INPUT_DOMAINS])
        if blob_sel != blob_host:
            raise AdmissionError("EXECUTION_INPUTS_HOST_DERIVED", "blob")
        log.rec("structural", "hostDerivedRefs-equals-blob-selected", True, "")

        expected_pairs = {}
        present_pairs = {}
        derived_by_cell = {}
        inventories_by_digest = {digest_of(inv): inv for inv in g["inventories"]}
        for outcome in ei["cellOutcomes"]:
            loc = (outcome["cellOrdinal"], outcome["programOrdinal"])
            expected_pairs[loc] = set(matrix_pairs(matrix, outcome["capabilityId"]))
            derived_by_cell[loc] = []
        for acc in ei["nativeCoverageAccounts"]:
            loc = (acc["cellOrdinal"], acc["programOrdinal"])
            present_pairs.setdefault(loc, set()).add((acc["relation"], acc["resolution"]))
            outcome = next(
                o
                for o in ei["cellOutcomes"]
                if o["cellOrdinal"] == acc["cellOrdinal"] and o["programOrdinal"] == acc["programOrdinal"]
            )
            exp_app = expected_applicability(matrix, outcome["capabilityId"], language_mode, acc["relation"], g["vcs"])
            if acc["applicability"] != exp_app:
                raise AdmissionError(
                    "EXECUTION_INPUTS_APPLICABILITY",
                    f"{outcome['capabilityId']}/{acc['relation']}: host {acc['applicability']} != derived {exp_app} (matrix {language_mode})",
                )
            matching = []
            for c in g["view_coverages_full"]:
                key = c["payload"]["key"]
                if key["relation"] != acc["relation"] or key["resolution"] != acc["resolution"]:
                    continue
                if key["sourceUniverse"] != outcome["universe"] or key["targetUniverse"] != outcome["universe"]:
                    continue
                matching.append({"digest": c["digest"], "id": c.get("id"), "entry": c["payload"]["entry"], "key": key})
            derived_acc = derive_account(acc, matching)
            derived_by_cell[loc].append(derived_acc)
        for loc, expected in expected_pairs.items():
            present = present_pairs.get(loc, set())
            if present != expected:
                raise AdmissionError(
                    "EXECUTION_INPUTS_NATIVE_COVERAGE_TOTALITY",
                    f"cell {loc} present {sorted(present)} expected {sorted(expected)}",
                )
        log.rec("structural", "native-coverage-account-totality", True, str({str(k): sorted(v) for k, v in present_pairs.items()}))
        log.rec("structural", "native-account-applicability-from-matrix", True, language_mode or "")
        for outcome in ei["cellOutcomes"]:
            loc = (outcome["cellOrdinal"], outcome["programOrdinal"])
            invs = [inventories_by_digest[d] for d in outcome["inventoryDigests"]]
            derived = derive_outcome(
                enumerator_status=outcome["enumeratorStatus"],
                universe=outcome["universe"],
                inventories=invs,
                derived_accounts=derived_by_cell[loc],
            )
            derived_by_outcome.append(derived)
            if outcome["state"] != derived["state"]:
                raise AdmissionError(
                    "EXECUTION_INPUTS_OUTCOME_DERIVE",
                    f"host state {outcome['state']} != derived {derived['state']} ({derived['reason']})",
                )
            if outcome["deficiency"] != derived["deficiency"] or outcome["nativeCause"] != derived["nativeCause"]:
                # host pair must equal derived primary pair
                raise AdmissionError(
                    "EXECUTION_INPUTS_CAUSE_CARRIER",
                    f"host {(outcome['deficiency'], outcome['nativeCause'])} != derived {(derived['deficiency'], derived['nativeCause'])}",
                )
            log.rec("structural", f"derive_outcome[{outcome['ordinal']}]", True, derived["reason"] + ":" + derived["state"])
    except AdmissionError as e:
        structural_ok = False
        log.rec("structural", "execution-inputs-laws", False, f"{e.code}: {e}")
        derived_by_outcome = derived_by_outcome or [{}] * len(g["execution_inputs"]["cellOutcomes"])

    # coverage totality + partition
    try:
        file_row = relreg["relations"]["file"]
        ct = file_row["coverageTotality"]
        inv_paths = {r["path"] for r in g["snapshot"]["sourceInventory"]}
        for sc, cov in zip(
            # pair scopes to coverages by scopeId
            g["scopes"],
            g["coverages"],
        ):
            pass
        # map coverage by scope
        cov_by_scope = {}
        for c in g["coverages"]:
            cov_by_scope[c["h"]["scopeId"]] = c
        for sc in g["scopes"]:
            c = cov_by_scope.get(sc and typed_id("subject-scope", sc) if False else None)
        # better: match by recomputing scope ids
        scope_ids = {typed_id("subject-scope", sc): sc for sc in g["scopes"]}
        # use view.scopeIds order
        scope_by_id = {}
        for sid, sc in zip(g["view"]["scopeIds"], g["scopes"]):
            scope_by_id[sid] = sc
        for c in g["coverages"]:
            if c["record"]["relation"] != "file" or c["record"]["resolution"] != "enumerated":
                continue
            if c["entry"].get("coverage") != "complete":
                continue
            sc = scope_by_id[c["h"]["scopeId"]]
            subjects = sc.get("subjects") or []
            fact_paths = set()
            for f in g["facts"]:
                if f["record"]["relation"] != "file":
                    continue
                if f["record"]["sourceUniverse"] != sc["sourceUniverse"]:
                    continue
                fact_paths.add(g["payloads"][f["id"]]["path"])
            for subj in subjects:
                if subj in inv_paths and subj not in fact_paths:
                    raise AdmissionError("COVERAGE_INVENTORY_TOTALITY_OMITS_PATH", subj)
        log.rec("structural", "file-coverage-totality", True, "")
        # partition
        parts = {}
        for sid, sc in scope_by_id.items():
            key = (sc["snapshotId"], sc["relation"], sc["resolution"], sc["sourceUniverse"], sc["targetUniverse"])
            parts.setdefault(key, []).append(set(sc.get("subjects") or []))
        for key, sets in parts.items():
            acc = set()
            for s in sets:
                if acc & s:
                    raise AdmissionError("SUBJECT_SCOPE_PARTITION_OVERLAP", str(key))
                acc |= s
        log.rec("structural", "coverage-partition-disjoint", True, str(len(parts)))
    except AdmissionError as e:
        structural_ok = False
        log.rec("structural", "coverage-totality-partition", False, f"{e.code}: {e}")

    # clones body identity + languageVersion + scopeCapabilityLaw
    try:
        table = dialect_table(ident, g["uni_domain"])
        for f in g["facts"]:
            if f["record"]["relation"] != "clones":
                continue
            pl = g["payloads"][f["id"]]
            suffix = hex_of(pl["bodyIdentity"])
            frame = store.rehash(suffix)
            parsed = parse_body_identity_frame(frame)
            log.rec("structural", f"clones-bodyIdentity-frame-{pl['normalisationLevel']}", True, parsed["levelId"])
            if parsed["levelId"] == "L0-verbatim":
                a = f["record"]["anchors"][0]
                span = store.rehash(a["blobDigest"])[a["startByte"] : a["endByte"]]
                if parsed.get("l0Span") != span:
                    raise AdmissionError("L0_SPAN_JOIN", "")
                log.rec("structural", "L0-span-join", True, str(len(span)))
            # languageVersion derived
            blv_fields = uni_row["languageVersionBinding"]["fields"]
            compiler_name = blv_fields["compilerName"].get("const")
            if compiler_name is None:
                compiler_name = get_path(g["ctx"], blv_fields["compilerName"]["path"])
            compiler_version = get_path(g["ctx"], blv_fields["compilerVersion"]["path"])
            compiler_build = get_path(g["ctx"], blv_fields["compilerBuild"]["path"])
            dialect_spec = uni_row["languageVersionBinding"]["dialect"]
            dialect_obj = None
            if dialect_spec.get("form") == "closed-suffix-table":
                a = f["record"]["anchors"][0]
                # path from snapshot via blob? use occupancy of enclosing file
                # body language from anchor path suffix: need path. File facts use payload path; clones use anchor on a snapshot blob.
                # Find inventory path whose sha256 == blobDigest
                blob = a["blobDigest"]
                path = next((row["path"] for row in g["snapshot"]["sourceInventory"] if row["sha256"] == blob), None)
                var = suffix_variant(path or "", dialect_spec["table"]) if path else None
                if var is None:
                    raise AdmissionError("BODY_LANGUAGE_SOURCE_VARIANT_UNKNOWN", str(path))
                dialect_obj = {dialect_spec["key"]: var}
                body_lang = (uni_row["languageVersionBinding"].get("bodyLanguageByVariant") or {}).get(var)
            elif dialect_spec.get("form") == "selected-compilation-target-edition":
                own_id = hex_of(g["uni"].get("sourceUnitOwnershipId"))
                if own_id is None:
                    raise AdmissionError("BODY_LANGUAGE_OWNERSHIP_REQUIRED", "")
                own = parse_h_frame(store.rehash(own_id))["value"]
                if own.get("enumeration") == "partial":
                    raise AdmissionError("BODY_LANGUAGE_OWNER_UNENUMERATED", "")
                a = f["record"]["anchors"][0]
                blob = a["blobDigest"]
                path = next((row["path"] for row in g["snapshot"]["sourceInventory"] if row["sha256"] == blob), None)
                rows = [r for r in own.get("ownership") or [] if r.get("path") == path]
                selected_ids = set(own.get("selectedUnitIds") or [])
                selected_rows = [r for r in rows if r.get("unitId") in selected_ids]
                if not selected_rows:
                    raise AdmissionError("BODY_LANGUAGE_OWNER_NOT_COMPILED", str(path))
                editions = set()
                units_by_id = {u["unitId"]: u for u in own.get("units") or []}
                for r in selected_rows:
                    u = units_by_id[r["unitId"]]
                    ed = u.get("targetEdition")
                    if ed is None:
                        ed = (g["uni"].get("edition") or {}).get(u.get("crateName"))
                    editions.add(ed)
                if len(editions) != 1:
                    raise AdmissionError("BODY_LANGUAGE_OWNER_AMBIGUOUS", str(editions))
                dialect_obj = {"edition": next(iter(editions))}
                body_lang = "rust"
            else:
                body_lang = uni_row["languageVersionBinding"].get("bodyLanguage")
            blv = {
                "schemaVersion": 1,
                "languageId": body_lang,
                "compilerName": compiler_name,
                "compilerVersion": compiler_version,
                "compilerBuild": compiler_build,
                "dialect": dialect_obj,
            }
            lv = hashlib.sha256(C(blv)).digest()
            if parsed["languageVersion"] != lv:
                raise AdmissionError("LANGUAGE_VERSION_DERIVE", parsed["languageVersion"].hex())
            if parsed["languageId"] != body_lang:
                raise AdmissionError("BODY_LANGUAGE_ID", parsed["languageId"])
            log.rec("structural", "languageVersion-derived", True, body_lang)
        # scopeCapabilityLaw for clones coverages
        if table is not None:
            scope_by_id = {sid: sc for sid, sc in zip(g["view"]["scopeIds"], g["scopes"])}
            for c in g["coverages"]:
                if c["record"]["relation"] != "clones":
                    continue
                sc = scope_by_id[c["h"]["scopeId"]]
                subjects = sc.get("subjects") or []
                unsupported = False
                if not subjects:
                    unsupported = True
                for pth in subjects:
                    if suffix_variant(pth, table) is None:
                        unsupported = True
                if unsupported:
                    entry = c["entry"]
                    if entry.get("coverage") == "complete":
                        raise AdmissionError("COVERAGE_SOURCE_VARIANT_FALSE_COMPLETE", "")
                    if entry.get("coverage") != "unknown" or entry.get("deficiency") != "language-tier-unsupported" or entry.get("nativeCause") != "capability-missing":
                        raise AdmissionError(
                            "COVERAGE_SOURCE_VARIANT_PAIR",
                            f"{entry.get('coverage')}/{entry.get('deficiency')}/{entry.get('nativeCause')}",
                        )
                    log.rec("structural", "scopeCapabilityLaw-unsupported-clones", True, "unknown+language-tier-unsupported/capability-missing")
                else:
                    log.rec("structural", "scopeCapabilityLaw-supported-clones", True, str(subjects))
    except AdmissionError as e:
        structural_ok = False
        log.rec("structural", "clones-body-and-scope-capability", False, f"{e.code}: {e}")

    # acyclic: proof has no evidenceId/runId
    if "evidenceId" in g["claimed_proof"] or "runId" in g["claimed_proof"]:
        structural_ok = False
        log.rec("structural", "acyclic-proof", False, "")
    else:
        log.rec("structural", "acyclic-proof", True, "")

    # import payload if present
    if g["plan"].get("importIds"):
        try:
            for iid in g["plan"]["importIds"]:
                rec = store.parse_typed(iid, "import")
                r = validate_against(rec, IDENT_REL, selector="#/$defs/import", label="import")
                if not r["stockOk"]:
                    raise AdmissionError("IMPORT_SCHEMA", str(r["errors"][:2]))
                pl = store.parse_canonical(rec["payloadDigest"])
                kind = rec.get("kind")
                domain = pl.get("payloadDomain")
                key = f"{kind}|{domain}"
                rows = payload_reg["classes"]["import"]["rows"]
                if key not in rows:
                    raise AdmissionError("IMPORT_UNREGISTERED", key)
                row = rows[key]
                r2 = validate_against(pl, row["document"], selector=row["selector"], label="import-payload")
                if not r2["stockOk"]:
                    raise AdmissionError("IMPORT_PAYLOAD_SCHEMA", str(r2["errors"][:2]))
                log.rec("schema", f"import-payload:{key}", True, row["selector"])
                log.rec("structural", "imported-payload-in-graph", True, iid)
        except AdmissionError as e:
            structural_ok = False
            log.rec("structural", "import-payload", False, f"{e.code}: {e}")
    else:
        log.mark_not_reached("imported-payload-in-graph", "this Run has empty plan.importIds")

    # semantic replay
    expected_proof = None
    try:
        file_invs = [inv for inv in g["inventories"] if inv["kind"] == "file"]
        complete_file_invs = [inv for inv in file_invs if inv.get("state") == "complete"]
        seen_subj = {}
        universe = g["uni_hex"]
        for inv in complete_file_invs:
            for row in inv["rows"]:
                key = (universe, "file", row["nativeSubjectId"])
                subj = {"schemaVersion": 3, "universe": universe, "kind": "file", "nativeSubjectId": row["nativeSubjectId"]}
                sid = typed_id("evaluation-subject", subj)
                rec = store.object_table.get(sid)
                if rec is None:
                    raise AdmissionError("SUBJECT_NOT_RETAINED", sid)
                frame = store.rehash(rec["digest"])
                parsed = parse_h_frame(frame, allowed_domains={"evaluation-subject"})
                if parsed["value"] != subj:
                    raise AdmissionError("SUBJECT_RECORD_MISMATCH", sid)
                seen_subj[key] = {"id": sid, "record": subj, "row": row}
        subjects = [seen_subj[k] for k in sorted(seen_subj, key=lambda t: C(list(t)))]
        if derived_by_outcome:
            exec_defs = execution_deficiencies_from_outcomes(g["execution_inputs"], derived_by_outcome)
        else:
            exec_defs = execution_deficiencies_from_outcomes(
                g["execution_inputs"],
                [
                    {"state": o["state"], "deficiency": o.get("deficiency"), "nativeCause": o.get("nativeCause")}
                    for o in g["execution_inputs"]["cellOutcomes"]
                ],
            )
        ladders = ladders_from_rel(relreg)
        expected_proof = compose_proof(
            g,
            ladders=ladders,
            file_subjects=subjects,
            complete_file_invs=complete_file_invs,
            execution_deficiencies=exec_defs,
        )
        kit_proof = {k: v for k, v in expected_proof.items() if not str(k).startswith("_")}
        expected_c = C(kit_proof)
        claimed_c = C(g["claimed_proof"])
        expected_id = typed_id("proof-bundle", kit_proof)
        equal = expected_c == claimed_c
        reached = schema_ok and structural_ok
        if not reached:
            log.mark_not_reached(
                "complete-semantic-replay",
                "positive graph admission did not complete; later proof-C-compare is diagnostic/notReached for acceptance",
            )
        log.rec(
            "fullsemantic",
            "proof-C-compare-kit-evaluationInputRefs",
            equal,
            f"expected {expected_id} claimed {g['claimed_proof_id']}",
            refuse=reached,
            diagnostic=not reached,
        )
        alt = dict(kit_proof)
        alt["evaluationInputRefs"] = expected_proof["_eval_input_refs_with_policy"]
        alt_c = C(alt)
        alt_equal = alt_c == claimed_c
        log.rec(
            "fullsemantic",
            "proof-C-compare-if-policy-and-rule-program-added-to-evaluationInputRefs",
            True,
            (
                "enumeration-contract.v1.md §7 names selectedRefs + execution-inputs only; "
                f"adding policy/rule-program would {'match' if alt_equal else 'not match'} claimed C "
                "(recorded, not used to waive the kit field)"
            ),
            refuse=False,
            diagnostic=True,
        )
        log.rec(
            "fullsemantic",
            "proof-C-compare",
            equal,
            f"expected {expected_id} claimed {g['claimed_proof_id']}",
            refuse=reached,
            diagnostic=not reached,
        )
        log.rec(
            "fullsemantic",
            "proof-identity-compare",
            expected_id == g["claimed_proof_id"],
            expected_id,
            refuse=reached,
            diagnostic=not reached,
        )
        if not equal:
            if reached:
                semantic_ok = False
            diffs = []
            for k in sorted(set(kit_proof) | set(g["claimed_proof"])):
                if kit_proof.get(k) != g["claimed_proof"].get(k):
                    diffs.append(k)
            log.rec("fullsemantic", "proof-field-diffs", False, ",".join(diffs), refuse=False, diagnostic=True)
        expected_proof = kit_proof
        g["expected_proof"] = expected_proof
        g["expected_proof_id"] = expected_id
        g["expected_c_sha"] = hashlib.sha256(expected_c).hexdigest()
        g["claimed_c_sha"] = hashlib.sha256(claimed_c).hexdigest()
        g["execution_deficiencies_derived"] = exec_defs
        g["derived_verdict"] = expected_proof["verdict"]
        g["subjects"] = subjects
        if not reached:
            semantic_ok = False
    except AdmissionError as e:
        semantic_ok = False
        log.rec(
            "fullsemantic",
            "proof-reconstruct",
            False,
            f"{e.code}: {e}",
            refuse=schema_ok and structural_ok,
            diagnostic=not (schema_ok and structural_ok),
        )

    g["tamper"] = execute_tamper(store, store_path, g, log, schema_ok, structural_ok, skip_tamper=skip_tamper)

    return finish(store_path, store, g, log, raw_ok, schema_ok, structural_ok, semantic_ok, language_mode)


def _ot_h_entry(domain: str, typed: str, digest: str, label: str) -> dict:
    return {
        "kind": "h-identity",
        "domain": domain,
        "digest": digest,
        "typedId": typed,
        "sha256Text": f"sha256:{digest}",
        "label": label,
    }


def execute_tamper(store: Store, store_path: Path, g: dict, log: JoinLog, schema_ok: bool, structural_ok: bool, *, skip_tamper: bool) -> dict:
    out = {
        "staleHashControl": None,
        "semanticRefuse": None,
        "tamperedProofId": None,
        "wholeRun": {"executed": False, "reason": "not-run"},
    }
    if skip_tamper:
        out["wholeRun"] = {"executed": False, "reason": "skip_tamper_on_replacement_admit"}
        return out
    if not g.get("expected_proof") or not g.get("claimed_proof"):
        log.mark_not_reached("tamper", "expected/claimed proof unavailable")
        out["wholeRun"] = {"executed": False, "reason": "no-proof"}
        return out
    claimed = g["claimed_proof"]
    expected = g["expected_proof"]
    tampered = copy.deepcopy(claimed)
    if tampered.get("verdict") == "pass":
        tampered["verdict"] = "fail"
    elif tampered.get("verdict") == "indeterminate":
        tampered["verdict"] = "pass"
    else:
        tampered["verdict"] = "pass"
    for rr in tampered.get("ruleResults") or []:
        if rr.get("outcome") in ("pass", "indeterminate"):
            rr["outcome"] = "fail"
            break
    tampered_c = C(tampered)
    claimed_c = C(claimed)
    expected_c = C(expected)
    stale = tampered_c != claimed_c
    tampered_id = typed_id("proof-bundle", tampered)
    semantic_refuse = expected_c != tampered_c
    citations_preserved = [p.get("witnessDigest") for p in tampered.get("predicateProofs") or []] == [
        p.get("witnessDigest") for p in claimed.get("predicateProofs") or []
    ]
    reached = schema_ok and structural_ok
    log.rec(
        "fullsemantic",
        "logical-result-tamper-stale-hash-control",
        stale,
        tampered_id,
        refuse=False,
        diagnostic=True,
    )
    log.rec(
        "fullsemantic",
        "logical-result-tamper-semantic-C-differs-from-expected",
        bool(semantic_refuse and citations_preserved),
        tampered_id,
        refuse=False,
        diagnostic=True,
    )
    out["staleHashControl"] = stale
    out["semanticRefuse"] = bool(semantic_refuse and citations_preserved)
    out["tamperedProofId"] = tampered_id
    if not reached:
        log.mark_not_reached(
            "whole-run-tamper-admit",
            "positive graph admission did not complete; reminted replacement is not this execution",
        )
        out["wholeRun"] = {
            "executed": False,
            "reason": "original-graph-not-admitted",
            "note": "distinct foreign proof IDs or proof-only remint is not whole-Run tamper",
        }
        return out
    try:
        tampered_frame = h_frame("proof-bundle", tampered)
        tampered_digest = hashlib.sha256(tampered_frame).hexdigest()
        new_ev = copy.deepcopy(g["evidence"])
        new_ev["proofBundleId"] = tampered_id
        new_ev_id = typed_id("semantic-evidence", new_ev)
        new_ev_frame = h_frame("semantic-evidence", new_ev)
        new_ev_digest = hashlib.sha256(new_ev_frame).hexdigest()
        new_seal = copy.deepcopy(g["seal"])
        new_seal["proofBundleId"] = tampered_id
        new_seal["evidenceId"] = new_ev_id
        new_seal["verdict"] = tampered["verdict"]
        new_seal_id = typed_id("evaluation-seal", new_seal)
        new_seal_frame = h_frame("evaluation-seal", new_seal)
        new_seal_digest = hashlib.sha256(new_seal_frame).hexdigest()
        new_run = copy.deepcopy(g["run"])
        new_run["evidenceId"] = new_ev_id
        new_run["evaluationSealId"] = new_seal_id
        new_run_id = typed_id("run", new_run)
        new_run_frame = h_frame("run", new_run)
        new_run_digest = hashlib.sha256(new_run_frame).hexdigest()
        blobs = dict(store.blobs)
        ot = copy.deepcopy(store.object_table)
        blobs[tampered_digest] = tampered_frame
        blobs[new_ev_digest] = new_ev_frame
        blobs[new_seal_digest] = new_seal_frame
        blobs[new_run_digest] = new_run_frame
        for old_k in [k for k in list(ot) if str(k).startswith("run3:")]:
            del ot[old_k]
        ot[tampered_id] = _ot_h_entry("proof-bundle", tampered_id, tampered_digest, "tampered-proof")
        ot[new_ev_id] = _ot_h_entry("semantic-evidence", new_ev_id, new_ev_digest, "reminted-evidence")
        ot[new_seal_id] = _ot_h_entry("evaluation-seal", new_seal_id, new_seal_digest, "reminted-seal")
        ot[new_run_id] = _ot_h_entry("run", new_run_id, new_run_digest, "reminted-run")
        repl_doc = {
            "objectTable": ot,
            "blobs": {k: base64.b64encode(v).decode("ascii") for k, v in blobs.items()},
            "blobCount": len(blobs),
        }
        probes = store_path.resolve().parents[2] / "output" / "probes"
        # store lives at SNAP/runs/<name>.store.json; origin output is sibling of snapshot
        # Write under this validator's output/probes regardless of store location.
        out_dir = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-law-interaction-review.v1/output/probes")
        out_dir.mkdir(parents=True, exist_ok=True)
        repl_path = out_dir / f"{store_path.stem}.whole-run-tamper.store.json"
        repl_path.write_text(json.dumps(repl_doc, separators=(",", ":")) + "\n")
        repl = admit_one(repl_path, skip_tamper=True)
        repl_layers = repl.get("layers") or {}
        repl_admitted_structurally = repl_layers.get("raw") == "PASS" and repl_layers.get("schema") == "PASS" and repl_layers.get("structural") == "PASS"
        repl_semantic = repl_layers.get("fullsemantic")
        # Whole-Run tamper succeeds only if replacement admits, then semantic refuses.
        ok_admit = bool(repl_admitted_structurally)
        ok_refuse = repl_semantic == "REFUSED" and (repl.get("expectedProofId") != repl.get("proofId"))
        log.rec(
            "fullsemantic",
            "whole-run-tamper-replacement-admitted",
            ok_admit,
            f"replacement run {new_run_id} layers={repl_layers} first={repl.get('firstRefusal')}",
        )
        log.rec(
            "fullsemantic",
            "whole-run-tamper-semantic-refuse-after-admit",
            bool(ok_admit and ok_refuse),
            f"expected {repl.get('expectedProofId')} claimed {repl.get('proofId')} semantic={repl_semantic}",
        )
        out["wholeRun"] = {
            "executed": True,
            "reason": "reminted-proof-evidence-seal-run-then-admitted",
            "replacementStore": str(repl_path),
            "replacementStoreSha256": hashlib.sha256(repl_path.read_bytes()).hexdigest(),
            "replacementRunId": new_run_id,
            "replacementProofId": tampered_id,
            "replacementEvidenceId": new_ev_id,
            "replacementSealId": new_seal_id,
            "replacementLayers": repl_layers,
            "replacementFirstRefusal": repl.get("firstRefusal"),
            "replacementOverall": repl.get("overall"),
            "replacementAdmittedStructurally": ok_admit,
            "semanticRefuseAfterAdmit": bool(ok_admit and ok_refuse),
            "foreignProofIdControl": "not-used; reminted enclosing run/seal/evidence identities",
        }
        g["tamper_replacement"] = out["wholeRun"]
    except Exception as e:
        log.rec("fullsemantic", "whole-run-tamper", False, f"{type(e).__name__}: {e}")
        out["wholeRun"] = {"executed": False, "reason": f"exception:{type(e).__name__}: {e}"}
    return out


def finish(store_path, store, g, log, raw_ok, schema_ok, structural_ok, semantic_ok, language_mode):
    layers = {}
    earlier_refused = False
    for layer in ("raw", "schema", "structural", "fullsemantic"):
        acc = [j for j in log.joins if j["layer"] == layer and not j.get("diagnostic")]
        fails = [j for j in acc if not j["ok"]]
        if earlier_refused:
            layers[layer] = "NOT_REACHED"
        elif fails:
            layers[layer] = "REFUSED"
            earlier_refused = True
        elif acc:
            layers[layer] = "PASS"
        else:
            layers[layer] = "NOT_REACHED"
            earlier_refused = True
    overall = "ADMIT" if all(v == "PASS" for v in layers.values()) else "REFUSED"
    out = {
        "store": str(store_path),
        "storeSha256": hashlib.sha256(store_path.read_bytes()).hexdigest(),
        "bytes": store_path.stat().st_size,
        "blobCount": len(store.blobs),
        "layers": layers,
        "overall": overall,
        "firstRefusal": log.first_refusal,
        "notReached": log.not_reached,
        "joins": log.joins,
        "languageMode": language_mode,
    }
    if g:
        out.update(
            {
                "runId": g.get("run_id"),
                "planId": g.get("plan_id"),
                "proofId": g.get("claimed_proof_id"),
                "expectedProofId": g.get("expected_proof_id"),
                "derivedVerdict": g.get("derived_verdict"),
                "claimedVerdict": (g.get("claimed_proof") or {}).get("verdict"),
                "proofCExpectedSha256": g.get("expected_c_sha"),
                "proofCClaimedSha256": g.get("claimed_c_sha"),
                "tamper": g.get("tamper"),
                "ctxDomain": g.get("ctx_domain"),
                "uniDomain": g.get("uni_domain"),
                "requestedCapabilities": (g.get("analysis_spec") or {}).get("requestedCapabilities"),
                "cellOutcomes": [
                    {k: o.get(k) for k in ["ordinal", "capabilityId", "state", "deficiency", "nativeCause", "required"]}
                    for o in (g.get("execution_inputs") or {}).get("cellOutcomes") or []
                ],
                "nativeCoverageAccounts": [
                    {
                        "relation": a.get("relation"),
                        "resolution": a.get("resolution"),
                        "applicability": a.get("applicability"),
                        "coverageIds": a.get("coverageIds"),
                    }
                    for a in (g.get("execution_inputs") or {}).get("nativeCoverageAccounts") or []
                ],
                "snapshotPaths": [r["path"] for r in (g.get("snapshot") or {}).get("sourceInventory") or []],
                "factRelations": [f["record"]["relation"] for f in g.get("facts") or []],
                "coverages": [
                    {
                        "relation": c["record"]["relation"],
                        "resolution": c["record"]["resolution"],
                        "coverage": c["entry"].get("coverage"),
                        "deficiency": c["entry"].get("deficiency"),
                        "nativeCause": c["entry"].get("nativeCause"),
                    }
                    for c in g.get("coverages") or []
                ],
                "importIds": (g.get("plan") or {}).get("importIds"),
                "scopeDocPresent": g.get("scope_doc") is not None,
                "executionDeficienciesDerived": g.get("execution_deficiencies_derived"),
                "graph": g,  # for property checks
            }
        )
    return out
