#!/usr/bin/env python3
"""Independent syntax-code Run closure/replay probes.

Normative-only. Does not import consumer helper builders or evaluator as an
expected-output oracle. C/H/lexical algorithms are taken from
identity-and-evidence.md §3. Transport is exact base64 blob bytes + SHA-256
rehash. Stock JSON Schema uses installed jsonschema; x-opensip-order is
implemented from the closed vocabulary in identity-and-evidence §3.

Usage:
  /tmp/opensip-architecture-review-env/bin/python -I -B \\
    /tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v1/output/diagnostics/syntax_code_pilot_probes.py
"""
from __future__ import annotations

import base64
import hashlib
import json
import sys
import unicodedata
from pathlib import Path
from typing import Any

KIT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v1/subject")
SNAP = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v1/consumer-snapshot")
OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-validator.v1/output")
STORE_PATH = SNAP / "runs" / "syntax-code.store.json"
META_PATH = SNAP / "runs" / "syntax-code.meta.json"
CLOSURE_PATH = SNAP / "runs" / "syntax-code.closure.json"
REPLAY_PATH = SNAP / "runs" / "syntax-code.replay.json"
REPLAY_SCRIPT = SNAP / "scripts" / "replay_from_export.py"
PILOT_SCRIPT = SNAP / "scripts" / "pilot_syntax_run.py"

IDENT = KIT / "docs/coop/design-corrections/foundation/identity-schemas.v3.json"
NATIVE = KIT / "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"
REL = KIT / "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json"
ENUM = KIT / "docs/coop/design-corrections/foundation/enumeration-plan.schema.v1.json"
EXEC = KIT / "docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json"
SINV = KIT / "docs/coop/design-corrections/foundation/subject-inventory.schema.v1.json"
POL2 = KIT / "docs/coop/design-corrections/workflows/schemas/policy-document.v2.schema.json"
EMIS = KIT / "docs/coop/design-corrections/foundation/evaluator-emission-plan.schema.v1.json"
CAP_REG = KIT / "docs/coop/design-corrections/native/capability-manifest-domains.v2.json"
MATRIX = KIT / "docs/coop/design-corrections/native/native-capability-matrix.v2.json"
FACT_ID = KIT / "docs/coop/artifacts/fact-identity-policy.v2.json"

I64_MIN = -9223372036854775808
U64_MAX = 18446744073709551615
MAX_BYTES = 4 * 1024 * 1024
MAX_DEPTH = 32
PRODUCT_PREFIX = b"opensip.product.v1"

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

NATIVE_DOMAINS = {
    "native.context.syntax.v2",
    "native.semantic-universe.syntax.v2",
    "native.context.typescript.v2",
    "native.semantic-universe.typescript.v2",
    "native.context.rust.v2",
    "native.semantic-universe.rust.v2",
    "native.dependency-source-set.v1",
    "native.unified-features.rust.v1",
    "native.prepared-output-set.v3",
    "native.cargo-config-projection.v2",
    "native.dependency-file-manifest.v1",
}

PROBES: list[dict[str, Any]] = []
FIRST_REFUSAL: dict[str, Any] | None = None


def record(name: str, ok: bool, *, selector: str, detail: Any = None, class_: str = "check") -> None:
    global FIRST_REFUSAL
    rec = {
        "name": name,
        "ok": bool(ok),
        "selector": selector,
        "class": class_,
        "detail": detail,
    }
    PROBES.append(rec)
    if (not ok) and FIRST_REFUSAL is None and class_ in ("closure", "frame", "schema", "replay"):
        FIRST_REFUSAL = rec


# --- C / lexical / H from identity-and-evidence §3 (independent of helper) ---


class AdmitError(Exception):
    def __init__(self, code: str, msg: str):
        super().__init__(msg)
        self.code = code
        self.msg = msg


def _enc_str(s: str) -> str:
    out = ['"']
    for ch in s:
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
        elif 0xD800 <= o <= 0xDFFF:
            raise AdmitError("NON_SCALAR_UNICODE", f"surrogate U+{o:04X}")
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def _encode(value: Any, depth: int) -> str:
    if depth > MAX_DEPTH:
        raise AdmitError("NESTING_TOO_DEEP", str(depth))
    if value is None:
        return "null"
    if type(value) is bool:
        return "true" if value else "false"
    if type(value) is int:
        if value < I64_MIN or value > U64_MAX:
            raise AdmitError("INTEGER_OUT_OF_RANGE", str(value))
        return str(value)
    if type(value) is str:
        return _enc_str(value)
    if type(value) is list:
        return "[" + ",".join(_encode(v, depth + 1) for v in value) + "]"
    if type(value) is dict:
        keys = list(value.keys())
        for k in keys:
            if type(k) is not str:
                raise AdmitError("OBJECT_KEY_NOT_STRING", repr(k))
        keys.sort(key=lambda k: k.encode("utf-8"))
        return "{" + ",".join(_enc_str(k) + ":" + _encode(value[k], depth + 1) for k in keys) + "}"
    raise AdmitError("UNSUPPORTED_TYPE", type(value).__name__)


def C(value: Any) -> bytes:
    raw = _encode(value, 1).encode("utf-8")
    if len(raw) > MAX_BYTES:
        raise AdmitError("DESCRIPTOR_TOO_LARGE", str(len(raw)))
    return raw


class RawAdmit:
    def __init__(self, raw: bytes):
        if len(raw) > MAX_BYTES:
            raise AdmitError("DESCRIPTOR_TOO_LARGE", str(len(raw)))
        try:
            self.s = raw.decode("utf-8")
        except UnicodeDecodeError as e:
            raise AdmitError("MALFORMED_UTF8", str(e)) from e
        if self.s.startswith("\ufeff"):
            raise AdmitError("BOM_FORBIDDEN", "BOM")
        self.n = len(self.s)
        self.i = 0

    def peek(self) -> str:
        return self.s[self.i] if self.i < self.n else ""

    def skip_ws(self) -> None:
        while self.i < self.n and self.s[self.i] in " \t\n\r":
            self.i += 1

    def parse(self) -> Any:
        v = self._value(1)
        self.skip_ws()
        if self.i != self.n:
            raise AdmitError("TRAILING_JUNK", str(self.i))
        return v

    def _value(self, depth: int) -> Any:
        if depth > MAX_DEPTH:
            raise AdmitError("NESTING_TOO_DEEP", str(depth))
        self.skip_ws()
        if self.i >= self.n:
            raise AdmitError("UNEXPECTED_EOF", "eof")
        c = self.s[self.i]
        if c == "{":
            return self._object(depth)
        if c == "[":
            return self._array(depth)
        if c == '"':
            return self._string()
        if c == "t":
            return self._lit("true", True)
        if c == "f":
            return self._lit("false", False)
        if c == "n":
            return self._lit("null", None)
        if c == "-" or c.isdigit():
            return self._number()
        raise AdmitError("UNEXPECTED_TOKEN", c)

    def _lit(self, lit: str, value: Any) -> Any:
        if self.s.startswith(lit, self.i):
            self.i += len(lit)
            return value
        raise AdmitError("UNEXPECTED_TOKEN", lit)

    def _object(self, depth: int) -> dict:
        self.i += 1
        self.skip_ws()
        out: dict[str, Any] = {}
        seen: set[str] = set()
        if self.peek() == "}":
            self.i += 1
            return out
        while True:
            self.skip_ws()
            key = self._string()
            if key in seen:
                raise AdmitError("DUPLICATE_KEY", key)
            seen.add(key)
            self.skip_ws()
            if self.peek() != ":":
                raise AdmitError("EXPECTED_COLON", str(self.i))
            self.i += 1
            out[key] = self._value(depth + 1)
            self.skip_ws()
            c = self.peek()
            if c == ",":
                self.i += 1
                continue
            if c == "}":
                self.i += 1
                return out
            raise AdmitError("EXPECTED_COMMA_OR_END", c)

    def _array(self, depth: int) -> list:
        self.i += 1
        self.skip_ws()
        out: list[Any] = []
        if self.peek() == "]":
            self.i += 1
            return out
        while True:
            out.append(self._value(depth + 1))
            self.skip_ws()
            c = self.peek()
            if c == ",":
                self.i += 1
                continue
            if c == "]":
                self.i += 1
                return out
            raise AdmitError("EXPECTED_COMMA_OR_END", c)

    def _string(self) -> str:
        if self.peek() != '"':
            raise AdmitError("EXPECTED_STRING", str(self.i))
        self.i += 1
        chars: list[str] = []
        while self.i < self.n:
            c = self.s[self.i]
            if c == '"':
                self.i += 1
                return "".join(chars)
            if c == "\\":
                self.i += 1
                chars.append(self._escape())
                continue
            o = ord(c)
            if o < 0x20:
                raise AdmitError("UNESCAPED_CONTROL", hex(o))
            chars.append(c)
            self.i += 1
        raise AdmitError("UNTERMINATED_STRING", "eof")

    def _escape(self) -> str:
        c = self.s[self.i]
        self.i += 1
        table = {'"': '"', "\\": "\\", "/": "/", "b": "\b", "f": "\f", "n": "\n", "r": "\r", "t": "\t"}
        if c in table:
            return table[c]
        if c == "u":
            h = self.s[self.i : self.i + 4]
            self.i += 4
            return chr(int(h, 16))
        raise AdmitError("BAD_ESCAPE", c)

    def _number(self) -> int:
        start = self.i
        if self.peek() == "-":
            self.i += 1
        if self.s[self.i] == "0":
            self.i += 1
            if self.i < self.n and self.s[self.i].isdigit():
                raise AdmitError("LEADING_ZERO", "leading zero")
        else:
            while self.i < self.n and self.s[self.i].isdigit():
                self.i += 1
        if self.i < self.n and self.s[self.i] == ".":
            raise AdmitError("FLOAT_FORBIDDEN", "float")
        if self.i < self.n and self.s[self.i] in "eE":
            raise AdmitError("EXPONENT_FORBIDDEN", "exp")
        token = self.s[start : self.i]
        if token == "-0":
            raise AdmitError("NEG_ZERO_FORBIDDEN", "-0")
        value = int(token, 10)
        if value < I64_MIN or value > U64_MAX:
            raise AdmitError("INTEGER_OUT_OF_RANGE", str(value))
        return value


def admit_raw(raw: bytes) -> Any:
    return RawAdmit(raw).parse()


def h_preimage(domain: str, canonical: bytes) -> bytes:
    return PRODUCT_PREFIX + b"\x00" + domain.encode("ascii") + b"\x00" + len(canonical).to_bytes(8, "big") + canonical


def H(domain: str, value: Any) -> str:
    return hashlib.sha256(h_preimage(domain, C(value))).hexdigest()


def parse_h_frame(frame: bytes) -> dict:
    prefix = PRODUCT_PREFIX + b"\x00"
    if not frame.startswith(prefix):
        raise AdmitError("H_FRAME_PREFIX", "missing prefix")
    rest = frame[len(prefix) :]
    nul = rest.find(b"\x00")
    if nul < 0:
        raise AdmitError("H_FRAME_DOMAIN", "no domain")
    domain = rest[:nul].decode("ascii")
    after = rest[nul + 1 :]
    declared = int.from_bytes(after[:8], "big")
    payload = after[8:]
    if declared != len(payload):
        raise AdmitError("H_FRAME_LENGTH_MISMATCH", f"{declared} vs {len(payload)}")
    parsed = admit_raw(payload)
    if C(parsed) != payload:
        raise AdmitError("H_FRAME_NOT_CANONICAL", "remainder != C(parse)")
    digest = hashlib.sha256(frame).hexdigest()
    return {"domain": domain, "value": parsed, "digest": digest, "canonicalBytes": payload}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


# --- CVE1 (resolved-inputs.v2 canonicalValueEncoding; used only for cap-manifest) ---


def cve1_encode(value: Any, depth: int = 0) -> bytes:
    if depth > 64:
        raise AdmitError("CVE1_NESTING", str(depth))
    if value is None:
        return b"\x00"
    if type(value) is bool:
        return b"\x02" if value else b"\x01"
    if type(value) is int:
        if value >= 0:
            return b"\x03" + value.to_bytes(8, "big", signed=False)
        return b"\x07" + value.to_bytes(8, "big", signed=True)
    if type(value) is str:
        if unicodedata.normalize("NFC", value) != value:
            raise AdmitError("NON_NFC_STRING", value)
        raw = value.encode("utf-8")
        return b"\x04" + len(raw).to_bytes(4, "big") + raw
    if type(value) is list:
        parts = [b"\x05", len(value).to_bytes(4, "big")]
        for el in value:
            parts.append(cve1_encode(el, depth + 1))
        return b"".join(parts)
    if type(value) is dict:
        keys = sorted(value.keys(), key=lambda k: k.encode("utf-8"))
        parts = [b"\x06", len(keys).to_bytes(4, "big")]
        for k in keys:
            parts.append(cve1_encode(k, depth + 1))
            parts.append(cve1_encode(value[k], depth + 1))
        return b"".join(parts)
    raise AdmitError("CVE1_UNSUPPORTED", type(value).__name__)


# --- order ---


def check_order(arr: list, annotation, *, path: str) -> list[str]:
    errs: list[str] = []
    if annotation is None or annotation == "sequence":
        return errs
    if annotation == "canonical-set":
        keys = [C(x) for x in arr]
        if len(keys) != len(set(keys)):
            errs.append(f"{path}: canonical-set duplicate")
        if keys != sorted(keys):
            errs.append(f"{path}: canonical-set not strictly ascending C")
        return errs
    if annotation == "canonical-order":
        keys = [C(x) for x in arr]
        if keys != sorted(keys):
            errs.append(f"{path}: canonical-order not nondecreasing")
        return errs
    if annotation == "utf8":
        if any(type(x) is not str for x in arr):
            errs.append(f"{path}: utf8 requires strings")
            return errs
        b = [x.encode("utf-8") for x in arr]
        if len(b) != len(set(b)):
            errs.append(f"{path}: utf8 duplicate")
        if b != sorted(b):
            errs.append(f"{path}: utf8 not ascending")
        return errs
    if annotation == "path":
        paths = []
        for x in arr:
            if type(x) is dict and "path" in x:
                paths.append(x["path"])
            elif type(x) is str:
                paths.append(x)
            else:
                errs.append(f"{path}: path order needs path")
                return errs
        if len(paths) != len(set(paths)):
            errs.append(f"{path}: duplicate paths")
        b = [p.encode("utf-8") for p in paths]
        if b != sorted(b):
            errs.append(f"{path}: path not ascending UTF-8")
        return errs
    if annotation == "numeric":
        if arr != sorted(arr) or len(arr) != len(set(arr)):
            errs.append(f"{path}: numeric")
        return errs
    if annotation == "ordinal":
        for i, x in enumerate(arr):
            if not isinstance(x, dict) or x.get("ordinal") != i:
                errs.append(f"{path}: ordinal not contiguous 0-based")
                break
        return errs
    if annotation == "predicate":
        keys = [("\0".join((x["ruleId"], x["subjectId"], x["predicateId"]))).encode() for x in arr]
        if keys != sorted(keys) or len(keys) != len(set(keys)):
            errs.append(f"{path}: predicate order")
        return errs
    if annotation in ("ruleId", "waiverId"):
        vals = [x[annotation] for x in arr]
        b = [v.encode("utf-8") for v in vals]
        if len(vals) != len(set(vals)) or b != sorted(b):
            errs.append(f"{path}: {annotation} order")
        return errs
    if isinstance(annotation, dict) and "by" in annotation:
        by = annotation["by"]
        keys = [("\0".join(str(x[k]) for k in by)).encode() for x in arr]
        if keys != sorted(keys) or len(keys) != len(set(keys)):
            errs.append(f"{path}: by {by}")
        return errs
    errs.append(f"{path}: annotation {annotation!r} outside closed vocabulary")
    return errs


def walk_order(instance: Any, schema: dict, defs: dict, *, path: str) -> list[str]:
    errs: list[str] = []
    if not isinstance(schema, dict):
        return errs
    if "$ref" in schema:
        ref = schema["$ref"]
        if ref.startswith("#/$defs/"):
            return walk_order(instance, defs.get(ref.split("/")[-1], {}), defs, path=path)
        return errs
    if "allOf" in schema:
        for sub in schema["allOf"]:
            errs.extend(walk_order(instance, sub, defs, path=path))
    t = schema.get("type")
    if t == "array" and isinstance(instance, list):
        errs.extend(check_order(instance, schema.get("x-opensip-order"), path=path))
        items = schema.get("items") or {}
        for i, el in enumerate(instance):
            errs.extend(walk_order(el, items, defs, path=f"{path}[{i}]"))
    if t == "object" and isinstance(instance, dict):
        props = schema.get("properties") or {}
        for k, v in instance.items():
            if k in props:
                errs.extend(walk_order(v, props[k], defs, path=f"{path}.{k}"))
    return errs


def load_json(p: Path) -> Any:
    return json.loads(p.read_text())


def validate_stock(instance: Any, schema_doc: dict, selector: str) -> list[dict]:
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource

    if selector.startswith("#/$defs/"):
        name = selector.split("/")[-1]
        schema = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": (schema_doc.get("$id") or "urn:local") + "/inline-" + name,
            "$defs": schema_doc.get("$defs", {}),
            **schema_doc["$defs"][name],
        }
        order_schema = schema_doc["$defs"][name]
        defs = schema_doc.get("$defs", {})
    else:
        schema = schema_doc
        order_schema = schema_doc
        defs = schema_doc.get("$defs", {})
    errors = []
    try:
        v = Draft202012Validator(schema)
        for e in v.iter_errors(instance):
            errors.append({"path": list(e.absolute_path), "message": e.message, "validator": e.validator})
    except Exception as ex:
        errors.append({"path": [], "message": str(ex), "validator": "setup"})
    for msg in walk_order(instance, order_schema, defs, path="$"):
        errors.append({"path": [], "message": msg, "validator": "x-opensip-order"})
    return errors


# --- store ---


def load_store(path: Path) -> dict:
    doc = load_json(path)
    blobs = {k: base64.b64decode(v) for k, v in doc["blobs"].items()}
    return {"objectTable": doc["objectTable"], "blobs": blobs, "blobCount": doc.get("blobCount")}


def main() -> int:
    results: dict[str, Any] = {
        "pilot": "syntax-code-complete-run-closure-replay",
        "storePath": str(STORE_PATH),
        "python": sys.version,
    }

    store_bytes = STORE_PATH.read_bytes()
    results["storeFile"] = {"sha256": sha256(store_bytes), "bytes": len(store_bytes)}
    meta_bytes = META_PATH.read_bytes()
    results["metaFile"] = {"sha256": sha256(meta_bytes), "bytes": len(meta_bytes)}
    closure_claim = load_json(CLOSURE_PATH)
    replay_claim = load_json(REPLAY_PATH)
    meta = load_json(META_PATH)
    results["claimedMeta"] = {
        "runId": meta.get("runId"),
        "verdict": meta.get("verdict"),
        "atomValue": meta.get("atomValue"),
        "blobCount": meta.get("blobCount"),
        "schemaChecksAllStockOk": all(c.get("stockOk") for c in meta.get("schemaChecks") or []),
    }
    results["claimedClosureOk"] = closure_claim.get("ok")
    results["claimedReplay"] = replay_claim

    store = load_store(STORE_PATH)
    blobs: dict[str, bytes] = store["blobs"]
    table = store["objectTable"]

    # blob rehash
    rehash_fail = []
    for d, b in blobs.items():
        if sha256(b) != d:
            rehash_fail.append(d)
    record(
        "blob-rehash-all",
        not rehash_fail,
        selector="identity-and-evidence.md §3 raw blob SHA256 of exact bytes",
        detail={"n": len(blobs), "failCount": len(rehash_fail), "fails": rehash_fail[:5]},
        class_="frame",
    )
    record(
        "blobCount-matches",
        store["blobCount"] == len(blobs) == meta.get("blobCount"),
        selector="consumer-snapshot/runs/syntax-code.meta.json blobCount; store.blobCount",
        detail={"store": store["blobCount"], "len": len(blobs), "meta": meta.get("blobCount")},
        class_="check",
    )

    # parse every H-looking blob
    frames: dict[str, dict] = {}
    frame_errors = []
    for d, b in blobs.items():
        if b.startswith(PRODUCT_PREFIX + b"\x00"):
            try:
                frames[d] = parse_h_frame(b)
            except AdmitError as e:
                frame_errors.append({"digest": d, "code": e.code, "msg": e.msg})
    record(
        "h-frames-parse",
        not frame_errors,
        selector="identity-and-evidence.md §3 H preimage frame admission",
        detail={"nFrames": len(frames), "errors": frame_errors[:8]},
        class_="frame",
    )

    by_domain: dict[str, list[dict]] = {}
    for d, fr in frames.items():
        by_domain.setdefault(fr["domain"], []).append({"digest": d, **fr})

    def one(domain: str) -> dict | None:
        xs = by_domain.get(domain) or []
        return xs[0] if len(xs) == 1 else None

    run_fr = None
    run_ids = [k for k in table if str(k).startswith("run3:")]
    record(
        "exactly-one-run3",
        len(run_ids) == 1,
        selector="identity-and-evidence.md §3 domain run / run3",
        detail=run_ids,
        class_="frame",
    )
    if run_ids:
        rec = table[run_ids[0]]
        run_fr = frames.get(rec["digest"])
        record(
            "run-frame-present",
            run_fr is not None and run_fr["domain"] == "run",
            selector="identity-and-evidence.md §3 Run includes seal; frame under H digest",
            detail={"digest": rec.get("digest"), "domain": None if run_fr is None else run_fr["domain"]},
            class_="frame",
        )

    ident_doc = load_json(IDENT)
    native_doc = load_json(NATIVE)
    rel_doc = load_json(REL)
    enum_doc = load_json(ENUM)
    exec_doc = load_json(EXEC)
    sinv_doc = load_json(SINV)
    pol2_doc = load_json(POL2)

    def schema_check(label: str, inst: Any, doc: dict, sel: str, path: str) -> None:
        errs = validate_stock(inst, doc, sel)
        record(
            f"schema-{label}",
            not errs,
            selector=path + sel,
            detail=errs[:6],
            class_="schema",
        )

    run = run_fr["value"] if run_fr else None
    if run:
        schema_check("run", run, ident_doc, "#/$defs/run", "identity-schemas.v3.json")
        recomputed_run = DOMAIN_PREFIX["run"] + ":" + H("run", run)
        record(
            "run-H-recompute",
            recomputed_run == run_ids[0],
            selector="identity-and-evidence.md §3 H(D,X); identifier prefix:lowercase hex",
            detail={"recomputed": recomputed_run, "claimed": run_ids[0]},
            class_="frame",
        )

    # walk graph from run
    def get_typed(tid: str) -> dict | None:
        meta_rec = table.get(tid)
        if not meta_rec:
            return None
        return frames.get(meta_rec["digest"])

    def get_canon(digest: str) -> Any:
        raw = blobs[digest]
        parsed = admit_raw(raw)
        if C(parsed) != raw:
            raise AdmitError("CANON_NOT_C", digest)
        return parsed

    seal_fr = get_typed(run["evaluationSealId"]) if run else None
    record(
        "run-seal-retained",
        seal_fr is not None and seal_fr["domain"] == "evaluation-seal",
        selector="identity-and-evidence.md §3 run includes evaluationSealId; graph acyclic seal includes evidence+proof",
        detail=None if seal_fr is None else seal_fr["domain"],
        class_="closure",
    )
    seal = seal_fr["value"] if seal_fr else None
    if seal:
        schema_check("seal", seal, ident_doc, "#/$defs/evaluation-seal", "identity-schemas.v3.json")

    ev_fr = get_typed(seal["evidenceId"]) if seal else None
    proof_fr = get_typed(seal["proofBundleId"]) if seal else None
    record(
        "seal-evidence-and-proof-retained",
        ev_fr is not None and proof_fr is not None,
        selector="identity-and-evidence.md §3 evaluation-seal includes evidence, evaluator, policy, proof and verdict",
        class_="closure",
    )
    evidence = ev_fr["value"] if ev_fr else None
    proof = proof_fr["value"] if proof_fr else None
    if evidence:
        schema_check("evidence", evidence, ident_doc, "#/$defs/semantic-evidence", "identity-schemas.v3.json")
    if proof:
        schema_check("proof", proof, ident_doc, "#/$defs/proof-bundle", "identity-schemas.v3.json")
        record(
            "proof-no-evidence-or-run",
            "evidenceId" not in proof and "runId" not in proof,
            selector="identity-and-evidence.md §3 The graph is acyclic: proof does not include EvidenceId or RunId",
            class_="closure",
        )
        recomputed_proof = DOMAIN_PREFIX["proof-bundle"] + ":" + H("proof-bundle", proof)
        claimed_proof = seal["proofBundleId"] if seal else None
        record(
            "proof-H-recompute",
            recomputed_proof == claimed_proof,
            selector="identity-and-evidence.md §3 H(proof-bundle, X)",
            detail={"recomputed": recomputed_proof, "claimed": claimed_proof},
            class_="frame",
        )

    plan_fr = get_typed(run["planId"]) if run else None
    snap_fr = get_typed(run["snapshotId"]) if run else None
    record(
        "plan-and-snapshot-retained",
        plan_fr is not None and snap_fr is not None,
        selector="identity-and-evidence.md §3 run3 ProjectId, snapshot, Plan, evidence, seal, capability manifest",
        class_="closure",
    )
    plan = plan_fr["value"] if plan_fr else None
    snapshot = snap_fr["value"] if snap_fr else None
    if plan:
        schema_check("plan", plan, ident_doc, "#/$defs/plan", "identity-schemas.v3.json")
    if snapshot:
        schema_check("snapshot", snapshot, ident_doc, "#/$defs/snapshot", "identity-schemas.v3.json")

    # source inventory is inlined on snapshot; also vcsDigest join
    src_inv = snapshot["sourceInventory"] if snapshot else []
    record(
        "snapshot-inventory-path-order",
        [r["path"].encode() for r in src_inv] == sorted(r["path"].encode() for r in src_inv)
        and len({r["path"] for r in src_inv}) == len(src_inv),
        selector="identity-and-evidence.md §3 inventories use path order; duplicate paths refuse",
        detail=[r["path"] for r in src_inv],
        class_="schema",
    )

    # vcs sourceInventoryDigest equals digest of snapshot inventory
    if snapshot and snapshot.get("vcsDigest") in blobs:
        try:
            vcs = get_canon(snapshot["vcsDigest"])
            inv_c = C(src_inv)
            record(
                "vcs-sourceInventoryDigest-equals-snapshot-inventory",
                vcs.get("sourceInventoryDigest") == sha256(inv_c),
                selector="identity-and-evidence.md §3 vcs-observation.sourceInventoryDigest must equal the digest of the snapshot's own inventory",
                detail={"vcs": vcs.get("sourceInventoryDigest"), "inventoryC": sha256(inv_c)},
                class_="closure",
            )
        except AdmitError as e:
            record("vcs-parse", False, selector="identity-and-evidence.md §3 vcsDigest canonical-record", detail=e.code, class_="closure")

    # native contexts: plan.nativeContextDigests exact set of retained context frames
    ctx_frames = by_domain.get("native.context.syntax.v2") or []
    uni_frames = by_domain.get("native.semantic-universe.syntax.v2") or []
    record(
        "syntax-context-present",
        len(ctx_frames) >= 1,
        selector="identity-and-evidence.md §3 native.context.syntax.v2; native-evidence.md §1.2",
        detail=len(ctx_frames),
        class_="closure",
    )
    record(
        "syntax-universe-present",
        len(uni_frames) >= 1,
        selector="identity-and-evidence.md §3 native.semantic-universe.syntax.v2; native-evidence.md §1.2",
        detail=len(uni_frames),
        class_="closure",
    )
    if plan:
        claimed_ctx = list(plan.get("nativeContextDigests") or [])
        retained_ctx = sorted({fr["digest"] for fr in ctx_frames})
        record(
            "plan-nativeContextDigests-equals-retained-syntax-context-frames",
            sorted(claimed_ctx) == retained_ctx,
            selector="identity-and-evidence.md §3 the set of retained context frames must equal plan.nativeContextDigests exactly",
            detail={"plan": claimed_ctx, "retained": retained_ctx},
            class_="closure",
        )
        # other language contexts should be absent for this syntax-only pilot
        extra_native = [d for d in by_domain if d.startswith("native.context.") and d != "native.context.syntax.v2"]
        extra_uni = [d for d in by_domain if d.startswith("native.semantic-universe.") and d != "native.semantic-universe.syntax.v2"]
        record(
            "no-compiler-universe-or-context",
            not extra_native and not extra_uni,
            selector="native-evidence.md §1.2 syntax-only; R-RUN-NO-COMPILER-UNIT",
            detail={"extraContext": extra_native, "extraUniverse": extra_uni},
            class_="closure",
        )

    syn_ctx = ctx_frames[0]["value"] if ctx_frames else None
    syn_uni = uni_frames[0]["value"] if uni_frames else None
    if syn_ctx:
        schema_check("syn_ctx", syn_ctx, native_doc, "#/$defs/SyntaxNativeContextV2", "native-evidence.schemas.v2.json")
    if syn_uni:
        schema_check("syn_uni", syn_uni, native_doc, "#/$defs/SyntaxUniverseV2ResolvedInputs", "native-evidence.schemas.v2.json")
        record(
            "universe-resolutionAttempted-false",
            syn_uni.get("resolutionAttempted") is False,
            selector="native-evidence.md §1.2 constant resolutionAttempted=false",
            class_="closure",
        )
        if plan:
            record(
                "universe-binds-plan-selected-context",
                syn_uni.get("nativeContextId") == "sha256:" + (plan.get("nativeContextDigests") or [""])[0],
                selector="identity-and-evidence.md §3 every retained universe frame's nativeContextId must be sha256: plus a member of plan.nativeContextDigests",
                detail=syn_uni.get("nativeContextId"),
                class_="closure",
            )
            record(
                "universe-context-domain-is-syntax",
                True,  # domain of the frame already selected
                selector="identity-schemas.v3.json#/x-opensip-digest-domains/domainSets/native-semantic-universe/native.semantic-universe.syntax.v2 contextDomain native.context.syntax.v2",
                class_="closure",
            )

    # grammar closure join
    gb = (syn_ctx or {}).get("grammarBundle") if syn_ctx else None
    g_closure = None
    if gb:
        g_fr = get_typed(gb.get("closureId"))
        record(
            "grammarBundle.closureId-retained-kind-grammar",
            g_fr is not None and g_fr["value"].get("kind") == "grammar",
            selector="identity-schemas.v3.json domainSets native.context.syntax.v2 closureJoins grammarBundle.closureId kind=grammar; native-evidence.md §1.2",
            detail=None if g_fr is None else g_fr["value"].get("kind"),
            class_="closure",
        )
        g_closure = g_fr["value"] if g_fr else None
        if g_closure:
            schema_check("grammar-closure", g_closure, ident_doc, "#/$defs/closure", "identity-schemas.v3.json")
            man = blobs.get(g_closure["manifestDigest"])
            record(
                "grammar-closure-manifest-bytes-retained",
                man is not None and sha256(man) == g_closure["manifestDigest"],
                selector="identity-and-evidence.md §3 closure.manifestDigest raw SHA256 of admitted component manifest body under the security metadata profile",
                detail={"digest": g_closure["manifestDigest"], "bytes": None if man is None else len(man), "head": None if man is None else man[:80].decode("utf-8", "replace")},
                class_="closure",
            )
            record(
                "parserVersion-equals-grammar-closure-semanticVersion",
                gb.get("parserVersion") == g_closure.get("semanticVersion"),
                selector="native-evidence.md §1.2 parserVersion must equal that closure manifest's semanticVersion (native.syntax-grammar-version-not-from-manifest)",
                detail={"parserVersion": gb.get("parserVersion"), "semanticVersion": g_closure.get("semanticVersion")},
                class_="closure",
            )
        # bundleDigest / grammarDigest / specificationDigest preimages
        for field, digest, art in [
            ("bundleDigest", gb.get("bundleDigest"), "exact retained bytes of the admitted grammar bundle manifest"),
            ("normalizer.specificationDigest", gb.get("normalizer", {}).get("specificationDigest"), "exact retained normalisation level specification bytes"),
        ]:
            raw = blobs.get(digest)
            record(
                f"grammarBundle-{field}-retained",
                raw is not None and digest is not None and sha256(raw) == digest,
                selector="native-evidence.schemas.v2.json#/$defs/SyntaxGrammarBundleV1 x-opensip-digest raw-artifact " + art,
                detail={"digest": digest, "present": raw is not None, "n": None if raw is None else len(raw)},
                class_="closure",
            )
        for i, g in enumerate(gb.get("grammars") or []):
            gd = g.get("grammarDigest")
            raw = blobs.get(gd)
            record(
                f"grammarDigest[{i}]-retained",
                raw is not None and sha256(raw) == gd,
                selector="native-evidence.schemas.v2.json#/$defs/SyntaxGrammarBundleV1 grammars[].grammarDigest raw-artifact",
                class_="closure",
            )
        # selected grammar in bundle
        if syn_uni:
            ids = set(g.get("grammarId") for g in gb.get("grammars") or [])
            missing_sel = [x for x in syn_uni.get("selectedGrammarIds") or [] if x not in ids]
            record(
                "selectedGrammarIds-subset-of-bundle",
                not missing_sel,
                selector="native-evidence.md §1.2 A selection naming a grammar the bundle does not contain refuses (native.syntax-grammar-not-in-bundle)",
                detail={"selected": syn_uni.get("selectedGrammarIds"), "bundle": sorted(ids), "missing": missing_sel},
                class_="closure",
            )
        langs = [g.get("languageId") for g in gb.get("grammars") or []]
        record(
            "installed-bundle-seven-languages",
            set(langs) == {"rust", "typescript", "javascript", "json", "toml", "markdown", "yaml"},
            selector="native-evidence.md §1.2 The bundled grammar set is closed, and it has SEVEN languages; native-capability-matrix.v2.json syntaxOnlyGrammarClass; SyntaxGrammarBundleV1 grammars is the CLOSED bundled-grammar set",
            detail=langs,
            class_="closure",
        )
        # closure tree must include grammar definition, bundle, normalizer spec
        if g_closure:
            tree_digests = {row["sha256"] for row in g_closure.get("tree") or []}
            needed = {gb.get("bundleDigest"), gb.get("normalizer", {}).get("specificationDigest")}
            needed.update(g.get("grammarDigest") for g in gb.get("grammars") or [])
            missing_tree = [d for d in needed if d not in tree_digests]
            record(
                "grammar-artifacts-in-closure-tree",
                not missing_tree,
                selector="native-evidence.md §1.2 every grammar definition, the bundle manifest and the normalizer specification present in the retained tree",
                detail={"missingFromTree": missing_tree, "tree": sorted(tree_digests)},
                class_="closure",
            )

    # capability manifest
    if plan:
        cap_bytes_d = plan.get("capabilityManifestBytesDigest")
        cap_bytes = blobs.get(cap_bytes_d)
        record(
            "capabilityManifestBytesDigest-retained",
            cap_bytes is not None,
            selector="identity-and-evidence.md §3 Plan carries capabilityManifestBytesDigest (raw SHA256) as well as capabilityManifestId",
            class_="closure",
        )
        if cap_bytes is not None:
            derived = sha256(b"opensip.capability-manifest.v1\x00" + cap_bytes)
            record(
                "capabilityManifestId-derived-from-retained-CVE1",
                derived == plan.get("capabilityManifestId") == (run or {}).get("capabilityManifestId"),
                selector="identity-and-evidence.md §3 SHA256(UTF8(opensip.capability-manifest.v1) || 00 || committedBytes); capability-manifest-id derived from capabilityManifestBytesDigest",
                detail={"derived": derived, "plan": plan.get("capabilityManifestId")},
                class_="closure",
            )

    # facts / scopes / coverage / view
    fact_frames = by_domain.get("fact") or []
    scope_frames = by_domain.get("subject-scope") or []
    cov_frames = by_domain.get("coverage") or []
    view_frames = by_domain.get("view") or []
    record(
        "view-present",
        len(view_frames) >= 1,
        selector="identity-and-evidence.md §3 view2 Plan, scopes, facts, Coverage",
        detail=len(view_frames),
        class_="closure",
    )
    view = view_frames[0]["value"] if view_frames else None
    if view:
        schema_check("view", view, ident_doc, "#/$defs/view", "identity-schemas.v3.json")
        if plan:
            record(
                "view-planId-join",
                view.get("planId") == (DOMAIN_PREFIX["plan"] + ":" + plan_fr["digest"] if plan_fr else None) or view.get("planId") == run["planId"],
                selector="identity-and-evidence.md §3 Every visited fact/scope and view/proof joins the current source or Plan",
                detail={"view.planId": view.get("planId"), "run.planId": None if run is None else run["planId"]},
                class_="closure",
            )

    rel_reg = rel_doc["x-opensip-relation-registry"]["relations"]
    rel_bytes = REL.read_bytes()
    rel_file_digest = sha256(rel_bytes)
    native_bytes = NATIVE.read_bytes()
    native_file_digest = sha256(native_bytes)

    facts = []
    for fr in fact_frames:
        rec = fr["value"]
        schema_check(f"fact-{rec.get('relation')}-{fr['digest'][:8]}", rec, ident_doc, "#/$defs/fact", "identity-schemas.v3.json")
        payload_raw = blobs.get(rec["payloadDigest"])
        payload = admit_raw(payload_raw) if payload_raw is not None else None
        facts.append({"digest": fr["digest"], "typedId": DOMAIN_PREFIX["fact"] + ":" + fr["digest"], "record": rec, "payload": payload})
        record(
            f"fact-payloadSchemaDigest-full-relation-document-{rec.get('relation')}",
            rec.get("payloadSchemaDigest") == rel_file_digest,
            selector="identity-and-evidence.md §3 payload registry: payloadSchemaDigest is the raw SHA-256 of the exact full bytes of relation-payload-schemas.v2.json",
            detail={"got": rec.get("payloadSchemaDigest"), "want": rel_file_digest},
            class_="closure",
        )
        if payload is not None:
            sel = rel_reg[rec["relation"]]["selector"]
            schema_check(f"payload-{rec['relation']}-{fr['digest'][:8]}", payload, rel_doc, sel, "relation-payload-schemas.v2.json")
        # universe same-only
        if rel_reg[rec["relation"]].get("universeRule") == "same-only":
            record(
                f"universeRule-same-only-{rec['relation']}-{fr['digest'][:8]}",
                rec["sourceUniverse"] == rec["targetUniverse"],
                selector="relation-payload-schemas.v2.json#/x-opensip-relation-registry/relations/" + rec["relation"] + "/universeRule",
                class_="closure",
            )
        # ladder membership
        ladder = rel_reg[rec["relation"]]["ladder"]
        record(
            f"rung-in-relation-ladder-{rec['relation']}-{rec['resolution']}-{fr['digest'][:8]}",
            rec["resolution"] in ladder,
            selector="relation-payload-schemas.v2.json#/x-opensip-relation-registry membershipRule ladder",
            detail={"resolution": rec["resolution"], "ladder": ladder},
            class_="closure",
        )
        # snapshot join
        record(
            f"fact-snapshotId-is-run-snapshot-{fr['digest'][:8]}",
            rec.get("snapshotId") == run["snapshotId"],
            selector="identity-and-evidence.md §3 every visited fact joins the current source",
            class_="closure",
        )

    # anchor laws then snapshotJoins (order required by registry)
    inv_by_path = {r["path"]: r for r in src_inv}

    for f in facts:
        rec, payload = f["record"], f["payload"]
        rel = rec["relation"]
        alaw = rel_reg[rel]["anchorLaw"]
        n_anc = len(rec.get("anchors") or [])
        if alaw.get("cardinality") == 0:
            ok = n_anc == 0
            want = "exactly 0"
        elif alaw.get("cardinality") == 1:
            ok = n_anc == 1
            want = "exactly 1"
        else:
            ok = n_anc >= int(alaw.get("minimum") or 1)
            want = f">= {alaw.get('minimum', 1)}"
        record(
            f"anchorLaw-{rel}-{f['digest'][:8]}",
            ok,
            selector="relation-payload-schemas.v2.json#/x-opensip-relation-registry/anchorLaw class=" + str(alaw.get("class")),
            detail={"n": n_anc, "want": want, "class": alaw.get("class")},
            class_="closure",
        )

    for f in facts:
        rec, payload = f["record"], f["payload"]
        if rec["relation"] != "file" or payload is None:
            continue
        row = inv_by_path.get(payload.get("path"))
        blob = blobs.get(payload.get("contentSha256")) if payload.get("contentSha256") else None
        joins = {
            "pathInInventory": row is not None,
            "digestEquals": row is not None and row["sha256"] == payload.get("contentSha256"),
            "lengthEquals": row is not None and row["bytes"] == payload.get("byteLength"),
            "blobRetained": blob is not None,
            "blobRehash": blob is not None and sha256(blob) == payload.get("contentSha256"),
            "blobLength": blob is not None and len(blob) == payload.get("byteLength"),
        }
        record(
            f"file-snapshotJoins-inventoried-file-{f['digest'][:8]}",
            all(joins.values()),
            selector="relation-payload-schemas.v2.json#/x-opensip-relation-registry/relations/file/snapshotJoins inventoried-file; identity-and-evidence.md §3 file join table",
            detail=joins,
            class_="closure",
        )

    # clones bodyIdentityJoin
    BODY_TAG = b"opensip.fact-identity.v1"
    dialect_table = {
        ".rs": "rs",
        ".d.ts": "ts-declaration",
        ".ts": "ts",
        ".tsx": "tsx",
        ".mts": "mts",
        ".cts": "cts",
        ".js": "js",
        ".jsx": "jsx",
        ".mjs": "mjs",
        ".cjs": "cjs",
    }
    body_lang = {
        "rs": "rust",
        "ts": "typescript",
        "tsx": "typescript",
        "ts-declaration": "typescript",
        "mts": "typescript",
        "cts": "typescript",
        "js": "javascript",
        "jsx": "javascript",
        "mjs": "javascript",
        "cjs": "javascript",
    }

    def longest_suffix(path: str) -> str | None:
        hits = [s for s in dialect_table if path.endswith(s)]
        if not hits:
            return None
        return max(hits, key=len)

    def u8pref(b: bytes) -> bytes:
        return bytes([len(b)]) + b

    def parse_body_frame(frame: bytes) -> dict:
        i = 0

        def take_u8() -> bytes:
            nonlocal i
            n = frame[i]
            i += 1
            b = frame[i : i + n]
            i += n
            return b

        tag = take_u8()
        level_id = take_u8()
        level_version = take_u8()
        language_id = take_u8()
        language_version = take_u8()
        plen = int.from_bytes(frame[i : i + 4], "big")
        i += 4
        payload = frame[i : i + plen]
        return {
            "tag": tag,
            "levelId": level_id.decode("ascii"),
            "levelVersion": level_version,
            "languageId": language_id.decode("ascii"),
            "languageVersion": language_version,
            "payload": payload,
            "rest": i + plen == len(frame),
        }

    # derived body-language-version from context
    derived_blv = None
    if syn_ctx and gb:
        derived_blv_fields = {
            "schemaVersion": 1,
            "compilerName": gb.get("parserName"),
            "compilerVersion": gb.get("parserVersion"),
            "compilerBuild": gb.get("bundleDigest"),
        }

    for f in facts:
        rec, payload = f["record"], f["payload"]
        if rec["relation"] != "clones" or payload is None:
            continue
        bid = payload.get("bodyIdentity")
        if not (isinstance(bid, str) and bid.startswith("sha256:") and len(bid) == 71):
            record(
                f"clones-bodyIdentity-form-{f['digest'][:8]}",
                False,
                selector="identity-and-evidence.md §3 clones bodyIdentity is sha256: + SHA-256 of framed preimage",
                detail=bid,
                class_="closure",
            )
            continue
        hex_id = bid[7:]
        frame = blobs.get(hex_id)
        record(
            f"clones-bodyIdentity-frame-retained-{payload.get('normalisationLevel')}-{f['digest'][:8]}",
            frame is not None,
            selector="identity-and-evidence.md §3 The frame itself is retained under that 64-hex suffix, so closure fetches it, re-hashes it, parses it; relation-payload-schemas.v2.json bodyIdentityJoin; L1-L3 exact retained preimage custody",
            detail={"bodyIdentity": bid, "retained": frame is not None},
            class_="closure",
        )
        anchors = rec.get("anchors") or []
        if len(anchors) != 1:
            continue
        anc = anchors[0]
        src = blobs.get(anc.get("blobDigest"))
        record(
            f"clones-anchor-blob-retained-{f['digest'][:8]}",
            src is not None and sha256(src) == anc.get("blobDigest") and anc.get("path") in inv_by_path,
            selector="identity-and-evidence.md §3 clones framed body-identity join; anchor is the body span",
            class_="closure",
        )
        # L0 recompute
        if payload.get("normalisationLevel") == "L0-verbatim" and src is not None and frame is not None:
            start, end = anc["startByte"], anc["endByte"]
            span = src[start:end]
            l0_payload = len(span).to_bytes(4, "big") + span
            parsed = parse_body_frame(frame)
            record(
                f"clones-L0-payload-double-length-prefix-{f['digest'][:8]}",
                parsed["payload"] == l0_payload and len(parsed["payload"]) == len(span) + 4,
                selector="identity-and-evidence.md §3 At L0-verbatim payload_len == raw_byte_len + 4; worked example law",
                detail={"payloadLen": len(parsed["payload"]), "span": len(span)},
                class_="closure",
            )
            # recompute identity from derived languageVersion + retained level spec
            level_spec = None
            if gb:
                level_spec = blobs.get(gb.get("normalizer", {}).get("specificationDigest"))
            if level_spec is not None and syn_ctx is not None:
                variant = dialect_table[longest_suffix(anc["path"])]
                blv = {
                    "schemaVersion": 1,
                    "languageId": body_lang[variant],
                    "compilerName": gb["parserName"],
                    "compilerVersion": gb["parserVersion"],
                    "compilerBuild": gb["bundleDigest"],
                    "dialect": {"grammarVariant": variant},
                }
                lv = hashlib.sha256(C(blv)).digest()
                pre = (
                    u8pref(BODY_TAG)
                    + u8pref(b"L0-verbatim")
                    + u8pref(hashlib.sha256(level_spec).digest())
                    + u8pref(blv["languageId"].encode("ascii"))
                    + u8pref(lv)
                    + len(l0_payload).to_bytes(4, "big")
                    + l0_payload
                )
                recomputed = "sha256:" + sha256(pre)
                record(
                    f"clones-L0-recomputed-from-derived-languageVersionBinding-{f['digest'][:8]}",
                    recomputed == bid,
                    selector="identity-schemas.v3.json domainSets native.semantic-universe.syntax.v2 languageVersionBinding; identity-and-evidence.md §3 body-language-version retention derived; relation-payload-schemas.v2.json bodyIdentityJoin recomputableAt L0-verbatim",
                    detail={"recomputed": recomputed, "claimed": bid, "derivedBlv": blv},
                    class_="closure",
                )
                record(
                    f"clones-normalisationVersion-is-sha256-of-retained-level-spec-{f['digest'][:8]}",
                    payload.get("normalisationVersion") == sha256(level_spec),
                    selector="identity-and-evidence.md §3 normalisationVersion is the raw SHA-256 of the exact retained canonical level-specification bytes",
                    class_="closure",
                )
        elif payload.get("normalisationLevel") != "L0-verbatim":
            record(
                f"clones-non-L0-requires-retained-frame-{payload.get('normalisationLevel')}-{f['digest'][:8]}",
                frame is not None,
                selector="relation-payload-schemas.v2.json bodyIdentityJoin note: At L1-L3 the requirement is exact retained preimage custody plus the framed-identity check",
                class_="closure",
            )

    # coverage
    for fr in cov_frames:
        rec = fr["value"]
        schema_check(f"coverage-{fr['digest'][:8]}", rec, ident_doc, "#/$defs/coverage", "identity-schemas.v3.json")
        record(
            f"coverage-payloadSchemaDigest-full-native-document-{fr['digest'][:8]}",
            rec.get("payloadSchemaDigest") == native_file_digest,
            selector="identity-and-evidence.md §3 payloadSchemaDigest raw SHA-256 of exact full native-evidence.schemas.v2.json bytes",
            detail={"got": rec.get("payloadSchemaDigest"), "want": native_file_digest},
            class_="closure",
        )
        payload = admit_raw(blobs[rec["payloadDigest"]]) if rec.get("payloadDigest") in blobs else None
        if payload is not None:
            schema_check(f"CoverageResultV3-{fr['digest'][:8]}", payload, native_doc, "#/$defs/CoverageResultV3", "native-evidence.schemas.v2.json")
            entry = payload.get("entry") or {}
            if entry.get("coverage") == "complete":
                record(
                    f"coverage-complete-implies-examinedExhaustive-{fr['digest'][:8]}",
                    entry.get("resolutionCompleteness", {}).get("examinedExhaustive") is True,
                    selector="relation-payload-schemas.v2.json coverageTotalityLaw; native-evidence.md §4 complete examined partition",
                    class_="closure",
                )
        # subjectScopeCommitment is sha256: + scope2 H suffix
        scope_id = rec.get("scopeId")
        scope_fr = get_typed(scope_id) if scope_id else None
        if scope_fr and payload is not None:
            commit = payload.get("key", {}).get("subjectScopeCommitment")
            want = "sha256:" + scope_fr["digest"]
            record(
                f"subjectScopeCommitment-is-H-of-scope-{fr['digest'][:8]}",
                commit == want,
                selector="identity-and-evidence.md §3 subjectScopeCommitment is sha256: plus the 64-hex suffix of the exact admitted scope2 identity, using H(subject-scope, descriptor)",
                detail={"got": commit, "want": want},
                class_="closure",
            )
            scope = scope_fr["value"]
            schema_check(f"scope-{scope.get('relation')}", scope, ident_doc, "#/$defs/subject-scope", "identity-schemas.v3.json")
            record(
                f"coverage-key-matches-scope-{fr['digest'][:8]}",
                payload.get("key", {}).get("relation") == scope.get("relation")
                and payload.get("key", {}).get("resolution") == scope.get("resolution")
                and payload.get("key", {}).get("sourceUniverse") == scope.get("sourceUniverse")
                and payload.get("key", {}).get("targetUniverse") == scope.get("targetUniverse")
                and payload.get("entry", {}).get("examinedUniverse", {}).get("subjectCount") == len(scope.get("subjects") or []),
                selector="identity-and-evidence.md §3 native Coverage admission joins key/entry commitments and count to this host-owned scope descriptor",
                class_="closure",
            )

    # coverage totality for file@enumerated
    if view:
        view_facts = []
        for tid in view.get("facts") or []:
            fr = get_typed(tid)
            if fr:
                pl = admit_raw(blobs[fr["value"]["payloadDigest"]])
                view_facts.append((tid, fr["value"], pl))
        view_scopes = []
        for tid in view.get("scopeIds") or []:
            fr = get_typed(tid)
            if fr:
                view_scopes.append((tid, fr["value"]))
        # partition law
        from collections import defaultdict

        parts: dict[tuple, list] = defaultdict(list)
        for tid, sc in view_scopes:
            key = (sc["snapshotId"], sc["relation"], sc["resolution"], sc["sourceUniverse"], sc["targetUniverse"])
            parts[key].append(set(sc.get("subjects") or []))
        overlap = False
        for key, sets in parts.items():
            acc: set = set()
            for s in sets:
                if acc & s:
                    overlap = True
                acc |= s
        record(
            "coveragePartitionLaw-per-view-disjoint-subjects",
            not overlap,
            selector="relation-payload-schemas.v2.json#/x-opensip-relation-registry/coveragePartitionLaw SUBJECT_SCOPE_PARTITION_OVERLAP",
            class_="closure",
        )
        # totality
        omitted = []
        for tid, sc in view_scopes:
            if sc.get("relation") != "file" or sc.get("resolution") != "enumerated":
                continue
            # find coverage for this scope
            cov_complete = False
            for cfr in cov_frames:
                if cfr["value"].get("scopeId") == tid:
                    pl = admit_raw(blobs[cfr["value"]["payloadDigest"]])
                    if pl.get("entry", {}).get("coverage") == "complete":
                        cov_complete = True
            if not cov_complete:
                continue
            for subj in sc.get("subjects") or []:
                if subj not in inv_by_path:
                    continue
                found = False
                for _, frec, pl in view_facts:
                    if (
                        frec.get("relation") == "file"
                        and frec.get("resolution") == "enumerated"
                        and frec.get("snapshotId") == sc["snapshotId"]
                        and frec.get("sourceUniverse") == sc["sourceUniverse"]
                        and frec.get("targetUniverse") == sc["targetUniverse"]
                        and pl.get("path") == subj
                    ):
                        found = True
                        break
                if not found:
                    omitted.append(subj)
        record(
            "coverageTotalityLaw-file-enumerated",
            not omitted,
            selector="relation-payload-schemas.v2.json#/x-opensip-relation-registry/relations/file/coverageTotality COVERAGE_INVENTORY_TOTALITY_OMITS_PATH",
            detail={"omitted": omitted},
            class_="closure",
        )

    # enumeration inventories
    enum_d = None
    enum_plan = None
    if plan:
        aspec = get_canon(plan["analysisSpecDigest"])
        schema_check("analysis-spec", aspec, ident_doc, "#/$defs/analysis-spec", "identity-schemas.v3.json")
        # find enumeration parameter
        for p in aspec.get("parameters") or []:
            if p.get("schemaDigest") == sha256(ENUM.read_bytes()):
                enum_d = p["payloadDigest"]
                enum_plan = get_canon(enum_d)
        record(
            "enumeration-plan-parameter-retained",
            enum_plan is not None,
            selector="identity-and-evidence.md §4 Plan commits EnumerationPlanV1; enumeration-contract.v1.md §1",
            class_="closure",
        )
        if enum_plan:
            schema_check("enum", enum_plan, enum_doc, "#", "enumeration-plan.schema.v1.json")
            record(
                "enum-snapshot-and-scope-join",
                enum_plan.get("snapshotId") == plan.get("snapshotId") == run.get("snapshotId")
                and enum_plan.get("scopeDigest") == plan.get("scopeDigest"),
                selector="enumeration-contract.v1.md §3 snapshotId equals plan.snapshotId; scopeDigest equals plan.scopeDigest",
                class_="closure",
            )
            memb = get_canon(enum_plan["membershipDigest"])
            schema_check("UnitMembershipV1", memb, native_doc, "#/$defs/UnitMembershipV1", "native-evidence.schemas.v2.json")
            # U-4: syntax-only files in a repo with no TS/Rust unit have unitOrdinal null
            rows = memb.get("rows") or []
            units = memb.get("units") or []
            null_ordinal = all(r.get("unitOrdinal") is None for r in rows)
            invented = any(u.get("unitKind") == "syntax-only" for u in units)
            record(
                "syntax-only-membership-unitOrdinal-null-no-invented-unit",
                null_ordinal and not invented and rows and all(r.get("membership") == "syntax-only" for r in rows),
                selector="native-evidence.md §1.2 A file reached that way is syntax-only membership with unitOrdinal: null under U-4, not a member of an invented unit",
                detail={"rows": rows, "units": [{"unitKind": u.get("unitKind"), "unitOrdinal": u.get("unitOrdinal"), "markerPath": u.get("markerPath")} for u in units]},
                class_="closure",
            )
            # expected inventories
            kind_map = enum_doc["x-opensip-kind-derivation"]
            expected = []
            for i, cell in enumerate(enum_plan.get("cells") or []):
                kinds = cell.get("kinds") or []
                nprog = len(cell.get("programBindings") or [])
                for po in range(nprog):
                    for k in kinds:
                        expected.append((i, po, k))
            # find retained SubjectInventoryV1 records
            sinv_records = []
            for d, rec in table.items():
                if rec.get("kind") == "canonical-record" and rec.get("label", "").startswith("SubjectInventory"):
                    obj = get_canon(d) if d in blobs else None
                    if obj and obj.get("schemaVersion") == 1 and "cellOrdinal" in obj:
                        sinv_records.append(obj)
            # also scan all canonical records
            if not sinv_records:
                for d, b in blobs.items():
                    if b.startswith(PRODUCT_PREFIX):
                        continue
                    try:
                        obj = admit_raw(b)
                    except AdmitError:
                        continue
                    if isinstance(obj, dict) and obj.get("schemaVersion") == 1 and "cellOrdinal" in obj and "rows" in obj and "kind" in obj and "planId" in obj:
                        sinv_records.append(obj)
            present = {(s["cellOrdinal"], s["programOrdinal"], s["kind"]) for s in sinv_records}
            missing = [e for e in expected if e not in present]
            record(
                "enumeration-exactly-one-inventory-per-cell-program-kind",
                not missing,
                selector="enumeration-contract.v1.md §4 Exactly one SubjectInventoryV1 per (cellOrdinal, programOrdinal, kind) in cell.kinds; ENUMERATION_INVENTORY_MISSING_RECORD",
                detail={"expected": expected, "present": sorted(present), "missing": missing, "nSinv": len(sinv_records)},
                class_="closure",
            )
            # cells match requestedCapabilities
            req = [(c["capabilityId"], c["languageMode"], c["workspaceRoot"], c["required"]) for c in aspec.get("requestedCapabilities") or []]
            cells = [(c["capabilityId"], c["languageMode"], c["workspaceRoot"], c["required"]) for c in enum_plan.get("cells") or []]
            record(
                "enum-cells-equal-requestedCapabilities",
                req == cells or sorted(req) == sorted(cells),
                selector="enumeration-contract.v1.md §3 cells ↔ requestedCapabilities same tuples including required",
                detail={"req": req, "cells": cells},
                class_="closure",
            )

    # execution inputs
    ei = None
    if proof and proof.get("executionInputsDigest") in blobs:
        ei = get_canon(proof["executionInputsDigest"])
        schema_check("exec_inputs", ei, exec_doc, "#", "execution-inputs.schema.v1.json")
        record(
            "proof.executionInputsDigest-retained",
            True,
            selector="identity-schemas.v3.json proof-bundle executionInputsDigest required on schemaVersion 3",
            class_="closure",
        )
        # selectedRefs must include views/coverages/inventories; forbidden domains
        forbidden = {"proof-bundle", "finding", "evaluation-seal", "run", "semantic-evidence"}
        bad = [r for r in ei.get("selectedRefs") or [] if r.get("domain") in forbidden]
        record(
            "execution-inputs-selectedRefs-forbid-proof-outputs",
            not bad,
            selector="execution-inputs-contract.v1.md §1 Forbidden on selectedRefs: proof-bundle, finding, evaluation-seal, run, semantic-evidence",
            detail=bad,
            class_="closure",
        )
        # cell outcomes inventoryDigests exactly one per kind
        if enum_plan:
            for oc in ei.get("cellOutcomes") or []:
                cell = (enum_plan.get("cells") or [])[oc["cellOrdinal"]]
                kinds = set(cell.get("kinds") or [])
                invs = oc.get("inventoryDigests") or []
                record(
                    f"cellOutcome[{oc['cellOrdinal']}]-inventoryDigests-exactly-one-per-kind",
                    len(invs) == len(kinds),
                    selector="execution-inputs-contract.v1.md §4 Inventory digests: exactly one per kind, kinds set-equal to the cell",
                    detail={"kinds": sorted(kinds), "nInv": len(invs), "state": oc.get("state")},
                    class_="closure",
                )

    # no TS/Rust compilation unit in snapshot inventory
    if snapshot:
        paths = [r["path"] for r in src_inv]
        record(
            "snapshot-has-no-tsconfig-or-cargo-toml",
            "tsconfig.json" not in paths and "jsconfig.json" not in paths and "Cargo.toml" not in paths and "package.json" not in paths,
            selector="native-evidence.md §1.2 syntax-only repository with no TypeScript or Rust compilation unit; R-RUN-NO-COMPILER-UNIT",
            detail=paths,
            class_="closure",
        )

    # --- independent atom + composition from retained selected inputs ---
    # Load policy / rule program / subject / facts for the file-present rule.
    policy = None
    rule_program = None
    if plan and plan.get("policyDigest") in blobs:
        policy = get_canon(plan["policyDigest"])
        schema_check("policy", policy, pol2_doc, "#/$defs/PolicyDocumentV2", "policy-document.v2.schema.json")
    if proof and proof.get("ruleProgramDigest") in blobs:
        rule_program = get_canon(proof["ruleProgramDigest"])
        # RuleProgramV2 is the projection of policy
        if policy:
            expected_rp = {
                "schemaVersion": 2,
                "policyDigest": plan["policyDigest"],
                "rules": [
                    {
                        "ruleId": r["ruleId"],
                        "ruleProgramRef": r["ruleProgramRef"],
                        "emitWhen": r["emitWhen"],
                    }
                    for r in policy.get("rules") or []
                ],
            }
            record(
                "ruleProgram-is-projection-of-plan-policy",
                C(rule_program) == C(expected_rp) and rule_program.get("policyDigest") == plan["policyDigest"],
                selector="identity-and-evidence.md §3 compiled program is not a free artifact: its policyDigest must equal the Plan's, and it must be exactly the projection of the Plan-selected policy's rules in the policy's own ruleId order",
                class_="closure",
            )

    # Independent atom: none of file where subject eq hello.rs
    # Occupancy for file is payload.path (atom-evaluation-contract.v1.md §3).
    file_facts = [f for f in facts if f["record"]["relation"] == "file" and f["record"]["resolution"] == "enumerated"]
    matching = []
    subject_native = "hello.rs"
    for f in file_facts:
        if (f["payload"] or {}).get("path") == subject_native:
            matching.append(f["typedId"])
    # Coverage at exact requested rung file@enumerated
    file_cov_ids = []
    file_cov_complete = False
    for fr in cov_frames:
        rec = fr["value"]
        sc = get_typed(rec["scopeId"])
        if not sc:
            continue
        if sc["value"].get("relation") == "file" and sc["value"].get("resolution") == "enumerated":
            file_cov_ids.append(DOMAIN_PREFIX["coverage"] + ":" + fr["digest"])
            pl = admit_raw(blobs[rec["payloadDigest"]])
            if pl.get("entry", {}).get("coverage") == "complete":
                file_cov_complete = True
    # none: false on known match; true on complete absence; else indeterminate
    if matching:
        atom_value = "false"
    elif not file_cov_ids:
        atom_value = "indeterminate"
    else:
        atom_value = "true" if file_cov_complete else "indeterminate"
    record(
        "independent-atom-none-file-hello.rs",
        atom_value == "false" and bool(matching),
        selector="atom-evaluation-contract.v1.md §3 source occupancy file path; identity-and-evidence.md §4 none: false on a known match; true on complete absence; otherwise indeterminate",
        detail={"value": atom_value, "matchingFactIds": matching, "coverageIds": file_cov_ids, "claimedAtom": meta.get("atomValue")},
        class_="replay",
    )

    # composition: emitWhen false => no finding; gating rule with no finding => pass
    emit = atom_value == "true"
    derived_findings = []  # none
    # gate: enabled AND gate=true AND severity >= gateSeverityAtLeast
    rule_outcome = "fail" if emit else "pass"
    if atom_value == "indeterminate":
        rule_outcome = "indeterminate"
    derived_verdict = rule_outcome  # single rule
    record(
        "independent-composition-verdict",
        derived_verdict == "pass" and not emit,
        selector="evaluator-composition-contract.v3.md §4-5 emitWhen=true emits finding; live unwaived gating finding => fail; otherwise pass. Among admitted semantic results any gating fail wins else indeterminate else pass",
        detail={"emitWhen": emit, "ruleOutcome": rule_outcome, "verdict": derived_verdict, "claimedVerdict": None if proof is None else proof.get("verdict")},
        class_="replay",
    )

    # Complete proof comparison: reconstruct a complete proof from retained inputs
    # and compare C to the claimed proof. This MUST refuse if the consumer's
    # claimed proof cannot be rebuilt without trusting saved verdicts.
    if proof is not None:
        # The independent reconstruction of the COMPLETE proof bundle requires
        # predicateProofs, witnesses, program-predicates, ruleResults, evaluationInputRefs.
        # We rebuild verdict/findings/ruleResults from retained selected inputs, then
        # compare the FULL claimed C(proof) to a reconstruction that copies only
        # structural citations the evaluator is allowed to read (not claimed verdict).
        rebuilt_core = {
            "schemaVersion": proof["schemaVersion"],
            "planId": proof["planId"],
            "executionPlanId": proof["executionPlanId"],
            "evaluatorClosure": proof["evaluatorClosure"],
            "ruleProgramDigest": proof["ruleProgramDigest"],
            "findingIds": derived_findings,
            "verdict": derived_verdict,
            "evaluationState": "evaluated",
            "waivedFindingIds": [],
            "executionDeficiencies": [],
            "executionInputsDigest": proof.get("executionInputsDigest"),
        }
        claimed_core = {k: proof[k] for k in rebuilt_core}
        record(
            "independent-proof-core-fields-equal-retained",
            C(rebuilt_core) == C(claimed_core),
            selector="evaluator-composition-contract.v3.md §7 Compare C of the COMPLETE recomputed proof; identity-and-evidence.md §4 Before sealing, independently reconstruct ... Compare the complete canonical proof. Equal finding counts or equal verdicts are insufficient — this probe first checks the composition-derived core, then the complete bundle.",
            detail={"rebuilt": rebuilt_core, "claimedSubset": claimed_core},
            class_="replay",
        )
        # Complete bundle equality cannot be established by reminting the saved object.
        # Fresh-process requirement: replay_from_export.py must recompute the proof.
        replay_src = REPLAY_SCRIPT.read_text()
        pilot_src = PILOT_SCRIPT.read_text()
        record(
            "fresh-process-replay-script-recomputes-complete-proof",
            "walk_predicate" in replay_src or "eval_atom" in replay_src or "derivedVerdict" in replay_src,
            selector="evaluator-composition-contract.v3.md §7 An independent evaluator receives admitted input closure and constructs every output from scratch; R-REPLAY-AFTER-ADMISSION; R-REPLAY-NO-CALLER-TRUTH; R-FROM-SCRATCH-COMMAND",
            detail={
                "script": str(REPLAY_SCRIPT),
                "containsWalkPredicate": "walk_predicate" in replay_src,
                "printsSavedVerdict": 'proof["verdict"]' in replay_src,
                "note": "script reloads run/seal/proof frames and prints the saved proof verdict; it does not reconstruct predicate proofs, findings, or compare C of a recomputed complete proof",
            },
            class_="replay",
        )
        record(
            "in-process-replay-uses-builder-memory-not-export",
            "facts_for_eval" in pilot_src and "tree2 = walk_predicate" in pilot_src,
            selector="R-REPLAY-NO-CALLER-TRUTH; evaluator-composition-contract.v3.md §7 It may not read claimed findings/witnesses to select subjects; replay must use retained export",
            detail="pilot_syntax_run.py recomputes walk_predicate on in-memory builder objects, then proofCompareEqual is C(parsed_frame)==C(builder proof)",
            class_="replay",
        )
        record(
            "claimed-proofCompareEqual-is-frame-self-equality",
            replay_claim.get("proofCompareEqual") is True
            and "C(pf[\"value\"]) == C(proof)" in pilot_src,
            selector="requirements.json R-REPLAY-COMPARE-BUNDLE; stopCondition helper self-consistency (reminted C-byte equality) is not admission",
            class_="replay",
        )
        record(
            "claimed-derivedVerdict-is-caller-mapping-from-atom-value",
            '"derivedVerdict": "pass" if tree2["value"] == "false" else "fail"' in pilot_src,
            selector="R-REPLAY-NO-CALLER-TRUTH No caller-authored truth / empty-match flags / literal pass-fail substitutes; composition-contract.v3.md §5 verdict from findings/gates/deficiencies",
            class_="replay",
        )
        tautology = 'or True)' in pilot_src and "proof-canonical-retained" in pilot_src
        record(
            "pilot-proof-canonical-retained-join-is-tautology",
            tautology,
            selector="pilot_syntax_run.py join('proof-canonical-retained', ... or True) — a join predicate that is unconditionally true is not a closure check",
            detail="observed source contains `or True` on proof-canonical-retained",
            class_="check",
        )

        # Tamper via ACTUAL comparison path: change claimed verdict, keep citations,
        # independently recompute composition verdict from retained inputs, refuse mismatch.
        tampered = json.loads(C(proof).decode())  # round-trip via our C then admit
        tampered = admit_raw(C(proof))
        tampered = json.loads(json.dumps(tampered))
        tampered["verdict"] = "fail"
        identities_ok = (
            tampered.get("planId") == proof.get("planId")
            and tampered.get("predicateProofs") == proof.get("predicateProofs")
            and tampered.get("findingIds") == proof.get("findingIds")
            and tampered.get("ruleProgramDigest") == proof.get("ruleProgramDigest")
        )
        comparison_refuses = C(tampered) != C(proof) and derived_verdict != tampered["verdict"]
        consumer_tamper = replay_claim.get("tamper") or {}
        record(
            "tamper-verdict-comparison-path-refuses",
            comparison_refuses and identities_ok,
            selector="identity-and-evidence.md §4 Compare the complete canonical proof; R-REPLAY-TAMPER preserve valid record identities and citation membership, change claimed logical result, replay refuses",
            detail={
                "identitiesPreserved": identities_ok,
                "C_equal": C(tampered) == C(proof),
                "independentVerdict": derived_verdict,
                "tamperedVerdict": tampered["verdict"],
                "comparisonRefuses": comparison_refuses,
                "consumerClaimedRefused": consumer_tamper.get("refused"),
                "consumerMethod": "C(tampered)!=C(proof) AND predicateProofs equal; does not re-evaluate or compare a recomputed complete proof against the tampered claim",
            },
            class_="replay",
        )
        record(
            "consumer-tamper-is-not-complete-proof-replay",
            True,  # observational: their path is C inequality only
            selector="R-REPLAY-TAMPER via the actual comparison path; evaluator-composition-contract.v3.md §7 Discriminating controls must ... show semantic replay refusal rather than merely a stale hash",
            detail={
                "consumerJoin": "tamper-verdict-changes-C-without-touching-citations",
                "consumerRefused": consumer_tamper.get("refused"),
                "independentNote": "C inequality of a mutated verdict field is necessary but not the published replay comparison of a freshly recomputed complete proof bundle against the tampered claim",
            },
            class_="check",
        )

        # complete proof C equality as a whole object — only if we reconstructed everything.
        # We did not reconstruct witnesses/predicateProofs from scratch beyond the atom,
        # so we MUST NOT claim complete-bundle equality. Record as notReached.
        record(
            "complete-proof-bundle-C-compare",
            False,
            selector="evaluator-composition-contract.v3.md §7 Compare C of the COMPLETE recomputed proof and every referenced output preimage and H identity. Counts, selected predicate fields, final verdict, or existence of a recomputed digest alone are insufficient.",
            detail={
                "reason": "Validator independently derived atom value, findings, rule outcome and verdict from retained selected inputs. Reconstructing byte-identical predicateProofs/witnesses/program-predicates requires walking the compiled program nodeDigest recipe over retained RuleProgramV2; the consumer export does not provide a fresh-process reconstruction of those nodes from the store, and the validator does not treat the saved proof as an oracle. Complete-bundle C compare is therefore not reached as a passing admission, and is recorded as a consumer replay omission.",
                "derivedAtom": atom_value,
                "derivedVerdict": derived_verdict,
                "claimedVerdict": proof.get("verdict"),
                "predicateProofCount": len(proof.get("predicateProofs") or []),
                "findingCount": len(proof.get("findingIds") or []),
            },
            class_="replay",
        )

    # consumer evaluator occupancy bug (static inspection of helper, not used as oracle)
    ev_src = (SNAP / "helper" / "evaluator.py").read_text()
    record(
        "consumer-eval_atom-does-not-skip-non-occupying-file-facts",
        "if subject[\"kind\"] == \"file\" and pl.get(\"path\") != subject[\"nativeSubjectId\"]:" in ev_src
        and "pass" in ev_src.split("if subject[\"kind\"] == \"file\" and pl.get(\"path\") != subject[\"nativeSubjectId\"]:")[1][:200],
        selector="atom-evaluation-contract.v1.md §3 Source occupancy uses the registered payload field (file path). A fact whose path ≠ current subject is a non-match, not a filter-only pass-through.",
        detail="eval_atom hits `pass` instead of continuing; this Run's filter on subject eq hello.rs happens to hide the hole for the single-file case",
        class_="check",
    )

    # schemaChecks are stock-only
    record(
        "consumer-schemaChecks-are-stockOk-only",
        all(c.get("stockOk") is True for c in meta.get("schemaChecks") or [])
        and all("x-opensip-digest" not in json.dumps(c) for c in meta.get("schemaChecks") or []),
        selector="requirements.json R-VALIDATE-OWNING-SCHEMA including published kit keywords stock JSON Schema ignores; identity-and-evidence.md §3 JSON Schema alone does not establish exact numeric admission; x-opensip-digest is the closing digest law",
        class_="check",
    )

    # three-valued note vs this Run
    record(
        "three-valued-law-exists-missing-coverage-is-indeterminate",
        True,
        selector="identity-and-evidence.md §4 exists true on known match; false on complete absence; otherwise indeterminate. This Run's atom is `none` with complete file Coverage and a known match, so value is false (not vacuous true).",
        detail={"thisRunAtom": atom_value, "consumerNote": replay_claim.get("threeValuedNote")},
        class_="check",
    )

    # output majors
    record(
        "output-majors-profile3",
        (run or {}).get("schemaVersion") == 3
        and (proof or {}).get("schemaVersion") == 3
        and (evidence or {}).get("schemaVersion") == 3
        and (seal or {}).get("schemaVersion") == 3
        and (snapshot or {}).get("schemaVersion") == 2
        and (plan or {}).get("schemaVersion") == 2,
        selector="current-source-map.proposed.md Current evaluator profile selection; identity-and-evidence.md §4 selected evaluator output profile is 3; unchanged native/input identities retain major two",
        class_="check",
    )

    results["firstRefusal"] = FIRST_REFUSAL
    results["probeCount"] = len(PROBES)
    results["failCount"] = sum(1 for p in PROBES if not p["ok"])
    results["passCount"] = sum(1 for p in PROBES if p["ok"])
    results["probes"] = PROBES
    results["limitations"] = [
        "Real compiler/crypto/OS/SQLite/host authentication not executed (F-OS-COMPILER-CRYPTO-SQLITE).",
        "Synthetic trusted observations in the consumer graph are treated as claimed descriptors, not native enforcement proof (F-SYNTHETIC-TCB).",
        "Component-manifest security-metadata-profile admission of closure.manifestDigest bytes was checked for retention/rehash only; full delivery.v4/component-manifest-schemas.v11 envelope admission is a further static omission if those bytes are not that profile.",
        "TS/Rust Runs in the same snapshot were not graded.",
        "jsonschema Draft 2020-12 stock validation used for type/required/enum; x-opensip-order independently implemented; x-opensip-digest enforced by explicit join probes rather than a generic schema-keyword engine.",
    ]

    outp = OUT / "diagnostics" / "syntax_code_pilot_probes.json"
    outp.write_text(json.dumps(results, indent=2) + "\n")
    print(json.dumps({
        "probeCount": results["probeCount"],
        "passCount": results["passCount"],
        "failCount": results["failCount"],
        "firstRefusal": None if FIRST_REFUSAL is None else {"name": FIRST_REFUSAL["name"], "selector": FIRST_REFUSAL["selector"], "detail": FIRST_REFUSAL.get("detail")},
        "written": str(outp),
    }, indent=2, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
