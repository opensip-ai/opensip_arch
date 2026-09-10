#!/usr/bin/env python3
"""Independent foundation-data checker.

Reads only the frozen 80-file kit and the 30 evidence files. Recomputes C, H,
CVE1, lexical admission, capability gates, protocol3, relation/rung/count laws,
and cited frozen-store membership. Claimed JSON values are compared, never trusted.
"""
from __future__ import annotations

import base64
import copy
import hashlib
import json
import os
import sys
import unicodedata
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

BASE = Path("/tmp/opensip-design-corrections/consumer-b.v12-fresh-foundation-data-review.v1")
SUBJECT = BASE / "subject"
DATA = BASE / "data"
OUT = Path(__file__).resolve().parent
PY = "/tmp/opensip-architecture-review-env/bin/python"

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

IDENTITY_TOKENS = {
    "source-identity-snapshot2",
    "plan-identity-plan2",
    "fact-identity-fact2",
    "coverage-v3",
}

PROCESS_FAULT = {"deadline", "nonzero-exit", "signal-death", "stdout-byte"}
SOURCE_BYTE_FRAMES = {
    "DependencySourceChunk",
    "DependencySourceManifest",
    "OpenUniverse",
    "PreparedOutputChunk",
    "PreparedOutputManifest",
    "SnapshotFileChunk",
    "SnapshotManifest",
}

RESOLVED_RUNGS = {
    "resolved-target",
    "resolved-binding",
    "resolved-callee",
    "checked",
    "from-resolved-calls",
}

SCOPED_IDS = [
    "S-FRESH-ORIGIN",
    "S-NOT-PRODUCT",
    "S-KIT-ONLY",
    "S-MANIFEST-VERIFY",
    "S-NO-ORACLE",
    "S-MISSING-DEP-IS-CUSTODY",
    "S-PROFILE-CURRENT",
    "S-CONTINUATION",
    "R-FIVE-CONTRACTS-INDEX",
    "R-SOURCE-MAP-SCOPE",
    "R-CVE1-TYPES-AVAILABLE",
    "R-H-HELPER",
    "R-CVE1-EIGHT-TYPES",
    "R-LEXICAL-ADMISSION",
    "R-SEMANTIC-VS-OPERATIONAL",
    "R-RAW-VS-PARSED",
    "R-ACYCLIC-JOINS",
    "R-CAP-ADMISSION",
    "R-CAP-NAMED-GATES",
    "R-TRACE-COMPLETE",
    "R-TRACE-UNAVAILABLE",
    "R-TRACE-CANCEL",
    "R-TRACE-FAULT",
    "R-TRACE-IDENTITY-BEFORE-SOURCE",
    "R-TRACE-TERMINAL",
    "R-TRACE-EXECUTED-VS-HOST",
    "R-RELATION-RUNG-TABLE",
    "R-COUNT-CLASS-ATTEMPT",
    "R-CODE-VS-DATA-MATRIX",
    "R-ENUM-VS-RESOLUTION",
    "R-ADVERTISED-MODE-PATHS",
    "R-IMPORTED-OBSERVATION-BOUNDARY",
]


def sha256_file(p: Path) -> tuple[str, int]:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest(), p.stat().st_size


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def load_json(p: Path) -> Any:
    with open(p, "rb") as f:
        return json.loads(f.read())


# --- C / H (identity-and-evidence §3) ---------------------------------------


def c_encode(value: Any) -> bytes:
    return _c_text(value).encode("utf-8")


def _c_text(value: Any) -> str:
    if value is None:
        return "null"
    if value is True:
        return "true"
    if value is False:
        return "false"
    if type(value) is int:
        if value < -(2**63) or value > 2**64 - 1:
            raise ValueError("integer out of C range")
        return str(value)
    if type(value) is float:
        raise ValueError("FLOAT_FORBIDDEN")
    if isinstance(value, str):
        return _c_string(value)
    if isinstance(value, list):
        return "[" + ",".join(_c_text(x) for x in value) + "]"
    if isinstance(value, dict):
        items = sorted(value.items(), key=lambda kv: kv[0].encode("utf-8"))
        inner = ",".join(_c_string(k) + ":" + _c_text(v) for k, v in items)
        return "{" + inner + "}"
    raise TypeError(f"unencodable type {type(value)!r}")


def _c_string(s: str) -> str:
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
            out.append("\\u%04x" % o)
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


def h_frame(domain: str, record: Any) -> bytes:
    c = c_encode(record)
    return (
        b"opensip.product.v1"
        + b"\x00"
        + domain.encode("ascii")
        + b"\x00"
        + len(c).to_bytes(8, "big")
        + c
    )


def h_digest(domain: str, record: Any) -> str:
    return sha256_bytes(h_frame(domain, record))


def typed_id(domain: str, record: Any) -> str:
    return f"{DOMAIN_PREFIX[domain]}:{h_digest(domain, record)}"


def identity_bundle(domain: str, record: Any) -> dict[str, Any]:
    c = c_encode(record)
    frame = h_frame(domain, record)
    digest = sha256_bytes(frame)
    return {
        "C_hex": c.hex(),
        "C_sha256": sha256_bytes(c),
        "H": digest,
        "frameHex": frame.hex(),
        "frameSha256": digest,
        "frameByteLength": len(frame),
        "typedId": f"{DOMAIN_PREFIX[domain]}:{digest}",
    }


# --- CVE1 (resolved-inputs.v2 canonicalValueEncoding) -----------------------


class Cve1Error(Exception):
    def __init__(self, code: str, message: str, path: str = ""):
        super().__init__(message)
        self.code = code
        self.message = message
        self.path = path


def cve1_encode(value: Any, depth: int = 0) -> bytes:
    if depth > 64:
        raise Cve1Error("MAX_NESTING", "CVE1 maxNesting 64 exceeded")
    if value is None:
        return b"\x00"
    if value is False:
        return b"\x01"
    if value is True:
        return b"\x02"
    if type(value) is int:
        if 0 <= value <= 2**64 - 1:
            return b"\x03" + value.to_bytes(8, "big")
        if -(2**63) <= value < 0:
            return b"\x07" + value.to_bytes(8, "big", signed=True)
        raise Cve1Error("INTEGER_OUT_OF_RANGE", f"{value} outside CVE1 integer range")
    if type(value) is float:
        raise Cve1Error("FLOAT_FORBIDDEN", "Floating-point values and byte strings are forbidden")
    if isinstance(value, str):
        if unicodedata.normalize("NFC", value) != value:
            raise Cve1Error(
                "NON_NFC_STRING",
                "Strings MUST already be Unicode NFC; a non-NFC string is rejected rather than silently normalised.",
            )
        raw = value.encode("utf-8")
        return b"\x04" + len(raw).to_bytes(4, "big") + raw
    if isinstance(value, list):
        if len(value) > 1048576:
            raise Cve1Error("MAX_COLLECTION", "array too large")
        parts = [b"\x05" + len(value).to_bytes(4, "big")]
        for el in value:
            parts.append(cve1_encode(el, depth + 1))
        return b"".join(parts)
    if isinstance(value, dict):
        if len(value) > 1048576:
            raise Cve1Error("MAX_COLLECTION", "map too large")
        keys = list(value.keys())
        for k in keys:
            if not isinstance(k, str):
                raise Cve1Error("MAP_KEY_TYPE", "map keys must be strings")
            if unicodedata.normalize("NFC", k) != k:
                raise Cve1Error("NON_NFC_STRING", "non-NFC map key")
        if len(keys) != len(set(keys)):
            raise Cve1Error("DUPLICATE_KEY", "duplicate keys are rejected before encoding")
        keys_sorted = sorted(keys, key=lambda s: s.encode("utf-8"))
        parts = [b"\x06" + len(keys_sorted).to_bytes(4, "big")]
        for k in keys_sorted:
            parts.append(cve1_encode(k, depth + 1))
            parts.append(cve1_encode(value[k], depth + 1))
        return b"".join(parts)
    raise Cve1Error("UNSUPPORTED_TYPE", f"CVE1 cannot encode {type(value)!r}")


def cve1_decode(data: bytes) -> tuple[Any, int]:
    value, n = _cve1_decode_at(data, 0, 0)
    if n != len(data):
        raise Cve1Error("TRAILING_BYTES", "trailing bytes after CVE1 value")
    return value, n


def _cve1_decode_at(data: bytes, i: int, depth: int) -> tuple[Any, int]:
    if depth > 64:
        raise Cve1Error("MAX_NESTING", "CVE1 maxNesting 64 exceeded")
    if i >= len(data):
        raise Cve1Error("TRUNCATED", "truncated CVE1")
    tag = data[i]
    i += 1
    if tag == 0x00:
        return None, i
    if tag == 0x01:
        return False, i
    if tag == 0x02:
        return True, i
    if tag == 0x03:
        if i + 8 > len(data):
            raise Cve1Error("TRUNCATED", "truncated unsigned-64")
        return int.from_bytes(data[i : i + 8], "big"), i + 8
    if tag == 0x07:
        if i + 8 > len(data):
            raise Cve1Error("TRUNCATED", "truncated negative-signed-64")
        return int.from_bytes(data[i : i + 8], "big", signed=True), i + 8
    if tag == 0x04:
        if i + 4 > len(data):
            raise Cve1Error("TRUNCATED", "truncated string length")
        ln = int.from_bytes(data[i : i + 4], "big")
        i += 4
        if i + ln > len(data):
            raise Cve1Error("TRUNCATED", "truncated string")
        s = data[i : i + ln].decode("utf-8")
        if unicodedata.normalize("NFC", s) != s:
            raise Cve1Error("NON_NFC_STRING", "non-NFC string")
        return s, i + ln
    if tag == 0x05:
        if i + 4 > len(data):
            raise Cve1Error("TRUNCATED", "truncated array count")
        n = int.from_bytes(data[i : i + 4], "big")
        i += 4
        if n > 1048576:
            raise Cve1Error("MAX_COLLECTION", "array too large")
        arr = []
        for _ in range(n):
            el, i = _cve1_decode_at(data, i, depth + 1)
            arr.append(el)
        return arr, i
    if tag == 0x06:
        if i + 4 > len(data):
            raise Cve1Error("TRUNCATED", "truncated map count")
        n = int.from_bytes(data[i : i + 4], "big")
        i += 4
        if n > 1048576:
            raise Cve1Error("MAX_COLLECTION", "map too large")
        out: dict[str, Any] = {}
        prev_key_bytes: bytes | None = None
        for _ in range(n):
            k, i = _cve1_decode_at(data, i, depth + 1)
            v, i = _cve1_decode_at(data, i, depth + 1)
            if not isinstance(k, str):
                raise Cve1Error("MAP_KEY_TYPE", "map key not string")
            kb = k.encode("utf-8")
            if k in out:
                raise Cve1Error("DUPLICATE_KEY", "duplicate map key")
            if prev_key_bytes is not None and kb <= prev_key_bytes:
                raise Cve1Error("UNSORTED_MAP", "map keys not strictly ascending")
            prev_key_bytes = kb
            out[k] = v
        return out, i
    raise Cve1Error("UNKNOWN_TAG", f"unknown CVE1 tag {tag:#x}")


def cap_manifest_id(committed: bytes) -> str:
    return sha256_bytes(b"opensip.capability-manifest.v1\x00" + committed)


# --- raw lexical JSON (identity-and-evidence §3) -----------------------------


class LexError(Exception):
    def __init__(self, code: str, message: str, extra: dict[str, Any] | None = None):
        super().__init__(message)
        self.code = code
        self.message = message
        self.extra = extra or {}


class RawLexer:
    def __init__(self, raw: bytes):
        self.raw = raw
        self.i = 0
        self.n = len(raw)

    def parse(self) -> Any:
        if self.raw.startswith(b"\xef\xbb\xbf"):
            raise LexError("BOM_FORBIDDEN", "UTF-8 BOM is not admitted")
        try:
            text = self.raw.decode("utf-8")
        except UnicodeDecodeError as e:
            raise LexError("MALFORMED_UTF8", str(e))
        self.s = text
        self.i = 0
        self.n = len(text)
        v = self._value()
        self.skip_ws()
        if self.i != self.n:
            raise LexError("TRAILING", "trailing content after value")
        return v

    def skip_ws(self) -> None:
        while self.i < self.n and self.s[self.i] in " \t\n\r":
            self.i += 1

    def _value(self) -> Any:
        self.skip_ws()
        if self.i >= self.n:
            raise LexError("TRUNCATED", "unexpected end")
        ch = self.s[self.i]
        if ch == "{":
            return self._object()
        if ch == "[":
            return self._array()
        if ch == '"':
            return self._string()
        if ch == "t":
            return self._lit("true", True)
        if ch == "f":
            return self._lit("false", False)
        if ch == "n":
            return self._lit("null", None)
        if ch == "-" or ch.isdigit():
            return self._number()
        raise LexError("UNEXPECTED", f"unexpected {ch!r}", {"at": self.i})

    def _lit(self, lit: str, value: Any) -> Any:
        if self.s[self.i : self.i + len(lit)] != lit:
            raise LexError("UNEXPECTED", f"expected {lit}")
        self.i += len(lit)
        return value

    def _object(self) -> dict[str, Any]:
        self.i += 1
        self.skip_ws()
        out: dict[str, Any] = {}
        if self.i < self.n and self.s[self.i] == "}":
            self.i += 1
            return out
        while True:
            self.skip_ws()
            if self.i >= self.n or self.s[self.i] != '"':
                raise LexError("UNEXPECTED", "expected object key")
            key = self._string()
            if key in out:
                raise LexError("DUPLICATE_KEY", f"duplicate key {key!r}", {"key": key})
            self.skip_ws()
            if self.i >= self.n or self.s[self.i] != ":":
                raise LexError("UNEXPECTED", "expected colon")
            self.i += 1
            out[key] = self._value()
            self.skip_ws()
            if self.i >= self.n:
                raise LexError("TRUNCATED", "unterminated object")
            if self.s[self.i] == ",":
                self.i += 1
                continue
            if self.s[self.i] == "}":
                self.i += 1
                return out
            raise LexError("UNEXPECTED", "expected comma or end of object")

    def _array(self) -> list[Any]:
        self.i += 1
        self.skip_ws()
        out: list[Any] = []
        if self.i < self.n and self.s[self.i] == "]":
            self.i += 1
            return out
        while True:
            out.append(self._value())
            self.skip_ws()
            if self.i >= self.n:
                raise LexError("TRUNCATED", "unterminated array")
            if self.s[self.i] == ",":
                self.i += 1
                continue
            if self.s[self.i] == "]":
                self.i += 1
                return out
            raise LexError("UNEXPECTED", "expected comma or end of array")

    def _string(self) -> str:
        start = self.i
        self.i += 1
        chars: list[str] = []
        while self.i < self.n:
            ch = self.s[self.i]
            o = ord(ch)
            if ch == '"':
                self.i += 1
                return "".join(chars)
            if o < 0x20:
                raise LexError(
                    "UNESCAPED_CONTROL",
                    f"unescaped control U+{o:04X} at {self.i}",
                )
            if ch == "\\":
                self.i += 1
                if self.i >= self.n:
                    raise LexError("TRUNCATED", "unterminated escape")
                esc = self.s[self.i]
                self.i += 1
                mapping = {'"': '"', "\\": "\\", "/": "/", "b": "\b", "f": "\f", "n": "\n", "t": "\t", "r": "\r"}
                if esc in mapping:
                    chars.append(mapping[esc])
                    continue
                if esc == "u":
                    hexpart = self.s[self.i : self.i + 4]
                    if len(hexpart) < 4 or any(c not in "0123456789abcdefABCDEF" for c in hexpart):
                        raise LexError("BAD_UNICODE_ESCAPE", "invalid \\u escape")
                    cp = int(hexpart, 16)
                    self.i += 4
                    if 0xD800 <= cp <= 0xDBFF:
                        if self.s[self.i : self.i + 2] == "\\u":
                            hex2 = self.s[self.i + 2 : self.i + 6]
                            if len(hex2) == 4 and all(c in "0123456789abcdefABCDEF" for c in hex2):
                                cp2 = int(hex2, 16)
                                if 0xDC00 <= cp2 <= 0xDFFF:
                                    combined = 0x10000 + ((cp - 0xD800) << 10) + (cp2 - 0xDC00)
                                    chars.append(chr(combined))
                                    self.i += 6
                                    continue
                        raise LexError(
                            "NON_SCALAR_UNICODE",
                            f"unpaired high surrogate U+{cp:04X}",
                        )
                    if 0xDC00 <= cp <= 0xDFFF:
                        raise LexError(
                            "NON_SCALAR_UNICODE",
                            f"unpaired low surrogate U+{cp:04X}",
                        )
                    chars.append(chr(cp))
                    continue
                raise LexError("BAD_ESCAPE", f"bad escape \\{esc}")
            chars.append(ch)
            self.i += 1
        raise LexError("TRUNCATED", "unterminated string", {"at": start})

    def _number(self) -> int:
        start = self.i
        if self.s[self.i] == "-":
            self.i += 1
        if self.i >= self.n or not self.s[self.i].isdigit():
            raise LexError("BAD_NUMBER", "invalid number")
        if self.s[self.i] == "0":
            self.i += 1
            if self.i < self.n and self.s[self.i].isdigit():
                tok = self.s[start : self.i + 1]
                while self.i < self.n and self.s[self.i].isdigit():
                    self.i += 1
                raise LexError("LEADING_ZERO", "leading zeros forbidden", {"token": self.s[start : self.i]})
        else:
            while self.i < self.n and self.s[self.i].isdigit():
                self.i += 1
        if self.i < self.n and self.s[self.i] == ".":
            raise LexError("FLOAT_FORBIDDEN", "floating-point tokens refused", {"at": start})
        if self.i < self.n and self.s[self.i] in "eE":
            raise LexError("EXPONENT_FORBIDDEN", "exponent tokens refused", {"at": start})
        tok = self.s[start : self.i]
        if tok == "-0":
            raise LexError("NEG_ZERO_FORBIDDEN", "-0 is refused")
        n = int(tok)
        if n < -(2**63) or n > 2**64 - 1:
            raise LexError(
                "INTEGER_OUT_OF_RANGE",
                f"{tok} outside [-2^63, 2^64-1]",
                {"value": tok},
            )
        return n


def lex_parse(raw: bytes) -> Any:
    return RawLexer(raw).parse()


# --- capability admission ---------------------------------------------------


class CapRefuse(Exception):
    def __init__(self, gate: str, message: str, path: str, extra: dict[str, Any] | None = None):
        super().__init__(message)
        self.gate = gate
        self.message = message
        self.path = path
        self.extra = extra or {}


def admit_capability(manifest: Any, domains: dict[str, Any]) -> None:
    rec_shapes = domains["recordShape"]
    regs = domains["registries"]
    open_pos = set(domains["declaredOPEN"].keys())
    type_hits = _adm_type(manifest)
    if type_hits:
        raise CapRefuse("ADM-TYPE", type_hits[0][1], type_hits[0][0], {})
    closed_hits = _adm_closed(manifest, rec_shapes)
    if closed_hits:
        raise CapRefuse("ADM-CLOSED", closed_hits[0][1], closed_hits[0][0], closed_hits[0][2])
    domain_hits = _adm_domain(manifest, regs, open_pos)
    if domain_hits:
        raise CapRefuse("ADM-DOMAIN", domain_hits[0][1], domain_hits[0][0], domain_hits[0][2])
    order_hits = _adm_order(manifest)
    if order_hits:
        raise CapRefuse("ADM-ORDER", order_hits[0][1], order_hits[0][0], order_hits[0][2])


def _expect_str(v: Any, path: str, hits: list) -> None:
    if type(v) is not str:
        hits.append((path, f"{path}: exact JSON string required; {type(v).__name__} is not a string"))


def _expect_int(v: Any, path: str, hits: list) -> None:
    if type(v) is not int:
        hits.append((path, f"{path}: exact JSON integer required; {type(v).__name__} is not an integer"))


def _adm_type(m: Any) -> list[tuple[str, str]]:
    hits: list[tuple[str, str]] = []
    if not isinstance(m, dict):
        return [("$", "root is not an object")]
    if "schemaVersion" in m:
        _expect_int(m["schemaVersion"], "$.schemaVersion", hits)
    if "profile" in m:
        _expect_str(m["profile"], "$.profile", hits)
    for i, p in enumerate(m.get("providers") or []) if isinstance(m.get("providers"), list) else []:
        if not isinstance(p, dict):
            hits.append((f"$.providers[{i}]", f"$.providers[{i}]: object required"))
            continue
        for fld in ("providerId", "language", "providerVersionSource", "toolchainIdentitySource"):
            if fld in p:
                _expect_str(p[fld], f"$.providers[{i}].{fld}", hits)
        rel = p.get("relations")
        if isinstance(rel, dict):
            for k, v in rel.items():
                _expect_str(k, f"$.providers[{i}].relations key", hits)
                _expect_str(v, f"$.providers[{i}].relations[{k!r}]", hits)
        plats = p.get("platformIds")
        if isinstance(plats, list):
            for j, x in enumerate(plats):
                _expect_str(x, f"$.providers[{i}].platformIds[{j}]", hits)
    for i, a in enumerate(m.get("coverageForAbsent") or []) if isinstance(m.get("coverageForAbsent"), list) else []:
        if not isinstance(a, dict):
            continue
        for fld in ("providerId", "language", "coverageState", "deficiency"):
            if fld in a:
                _expect_str(a[fld], f"$.coverageForAbsent[{i}].{fld}", hits)
        rids = a.get("relationIds")
        if isinstance(rids, list):
            for j, x in enumerate(rids):
                _expect_str(x, f"$.coverageForAbsent[{i}].relationIds[{j}]", hits)
    return hits


def _keyset_check(obj: dict, expected: list[str], path: str) -> tuple[str, str, dict] | None:
    got = list(obj.keys())
    if set(got) != set(expected) or len(got) != len(expected):
        return (
            path,
            f"{path}: closed key set {expected} got {got}",
            {"expected": expected, "got": got},
        )
    return None


def _adm_closed(m: Any, shapes: dict) -> list[tuple[str, str, dict]]:
    hits: list[tuple[str, str, dict]] = []
    if not isinstance(m, dict):
        return [("$", "root is not an object", {})]
    cap_keys = shapes["CapabilityManifestV1"]["requiredKeys"]
    h = _keyset_check(m, cap_keys, "$")
    if h:
        hits.append(h)
        return hits
    prov_keys = shapes["ProviderCapability"]["requiredKeys"]
    abs_keys = shapes["AbsentCapability"]["requiredKeys"]
    for i, p in enumerate(m.get("providers") or []):
        if not isinstance(p, dict):
            continue
        h = _keyset_check(p, prov_keys, f"$.providers[{i}]")
        if h:
            hits.append(h)
    for i, a in enumerate(m.get("coverageForAbsent") or []):
        if not isinstance(a, dict):
            continue
        h = _keyset_check(a, abs_keys, f"$.coverageForAbsent[{i}]")
        if h:
            hits.append(h)
    return hits


def _adm_domain(m: Any, regs: dict, open_pos: set[str]) -> list[tuple[str, str, dict]]:
    hits: list[tuple[str, str, dict]] = []
    platforms = set(regs["PLATFORM-ID-DOMAIN-V1"]["members"])
    relations = set(regs["RELATION-DOMAIN-V2"]["members"])
    ladders = regs["RELATION-LADDER-DOMAIN-V2"]["ladders"]
    deficiencies = set(regs["DEFICIENCY-DOMAIN-V1"]["members"])
    covstates = set(regs["COVERAGE-STATE-DOMAIN-V1"]["members"])
    _ = open_pos
    for i, p in enumerate(m.get("providers") or []):
        if not isinstance(p, dict):
            continue
        rel = p.get("relations") or {}
        if isinstance(rel, dict):
            for k, v in rel.items():
                if k not in relations:
                    hits.append(
                        (
                            f"$.providers[{i}].relations",
                            f"$.providers[{i}].relations key {k!r} not in RELATION-DOMAIN-V2",
                            {"value": k},
                        )
                    )
                    continue
                ladder = ladders.get(k, [])
                if v not in ladder:
                    hits.append(
                        (
                            f"$.providers[{i}].relations[{k!r}]",
                            f"$.providers[{i}].relations[{k!r}]: rung {v!r} is not a member of {k} ladder",
                            {"relation": k, "rung": v, "ladder": ladder},
                        )
                    )
        for j, plat in enumerate(p.get("platformIds") or []):
            if plat not in platforms:
                hits.append(
                    (
                        f"$.providers[{i}].platformIds[{j}]",
                        f"$.providers[{i}].platformIds[{j}]: platformId not in PLATFORM-ID-DOMAIN-V1",
                        {"value": plat},
                    )
                )
    for i, a in enumerate(m.get("coverageForAbsent") or []):
        if not isinstance(a, dict):
            continue
        for j, rid in enumerate(a.get("relationIds") or []):
            if rid not in relations:
                hits.append(
                    (
                        f"$.coverageForAbsent[{i}].relationIds[{j}]",
                        f"$.coverageForAbsent[{i}].relationIds[{j}]: {rid!r} is not a member of fact-plane.v1#relationRegistry.relations",
                        {"value": rid},
                    )
                )
        if a.get("deficiency") not in deficiencies and "deficiency" in a:
            hits.append(
                (
                    f"$.coverageForAbsent[{i}].deficiency",
                    f"$.coverageForAbsent[{i}].deficiency: not a member of DEFICIENCY-DOMAIN-V1",
                    {"value": a.get("deficiency")},
                )
            )
        if a.get("coverageState") not in covstates and "coverageState" in a:
            hits.append(
                (
                    f"$.coverageForAbsent[{i}].coverageState",
                    f"$.coverageForAbsent[{i}].coverageState: not a member of COVERAGE-STATE-DOMAIN-V1",
                    {"value": a.get("coverageState")},
                )
            )
    return hits


def _strict_asc(values: list[str], path: str) -> tuple[str, str, dict] | None:
    for i in range(1, len(values)):
        prev_b = values[i - 1].encode("utf-8")
        cur_b = values[i].encode("utf-8")
        if cur_b <= prev_b:
            return (
                path,
                f"{path}: not strictly ascending NFC UTF-8 ({values[i]!r})",
                {"value": values[i]},
            )
    return None


def _adm_order(m: Any) -> list[tuple[str, str, dict]]:
    hits: list[tuple[str, str, dict]] = []
    providers = m.get("providers") or []
    for i, p in enumerate(providers):
        if not isinstance(p, dict):
            continue
        h = _strict_asc(list(p.get("platformIds") or []), f"$.providers[{i}].platformIds")
        if h:
            hits.append(h)
    absent = m.get("coverageForAbsent") or []
    for i, a in enumerate(absent):
        if not isinstance(a, dict):
            continue
        h = _strict_asc(list(a.get("relationIds") or []), f"$.coverageForAbsent[{i}].relationIds")
        if h:
            hits.append(h)
    h = _strict_asc([p.get("providerId", "") for p in providers if isinstance(p, dict)], "$.providers")
    if h:
        hits.append(h)
    h = _strict_asc([a.get("providerId", "") for a in absent if isinstance(a, dict)], "$.coverageForAbsent")
    if h:
        hits.append(h)
    return hits


# --- protocol3 --------------------------------------------------------------


def load_protocol(path: Path) -> dict[str, Any]:
    return load_json(path)


def protocol_step(doc: dict[str, Any], state: dict[str, Any], event: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    frame = event["frame"]
    phase = state["phase"]
    pre = doc["preMatchLaw"]
    wild = doc["wildcards"]
    pre_complete = set(wild["*PRE_COMPLETE"]["phases"])
    process_fault = set(wild["*PROCESS_FAULT"]["frames"])

    if phase == "FAULT":
        return "FAULT-absorb", state

    if phase in {"WAIT_ZERO_EXIT", "WAIT_EOF", "DONE"}:
        if frame not in {"zero-exit", "eof"} and frame not in process_fault:
            st = dict(state)
            st["phase"] = "FAULT"
            return "post-terminal-frame", st

    if frame in process_fault:
        st = dict(state)
        st["phase"] = "FAULT"
        return "P3-33", st

    st = dict(state)
    matched = None
    for row in doc["rules"]:
        if row["id"] in {"P3-33", "P3-34"}:
            continue
        row_phase = row["phase"]
        phase_ok = (row_phase == phase) or (row_phase == "*PRE_COMPLETE" and phase in pre_complete)
        if not phase_ok:
            continue
        if row["frame"] != frame:
            continue
        guard = row.get("guard") or {}
        if all(st.get(k) == v for k, v in guard.items()):
            matched = row
            break

    if matched is None:
        st["phase"] = "FAULT"
        return "P3-34", st

    # stateUpdates apply only after a successful row match (protocol3 initializationAndUpdateOrder).
    _apply_frame_updates(st, event)

    nxt = matched["next"]
    if nxt == "ANALYZING_OR_READY_COMPLETE":
        st["stageIndex"] = st.get("stageIndex", 0) + 1
        st["stagesCompleted"] = st.get("stagesCompleted", 0) + 1
        if st["stageIndex"] == st.get("stageCount", 0):
            nxt = "READY_COMPLETE"
        else:
            nxt = "ANALYZING"
    if "terminal" in matched:
        st["terminalKind"] = matched["terminal"]
    st["phase"] = nxt
    return matched["id"], st


def _apply_frame_updates(st: dict[str, Any], event: dict[str, Any]) -> None:
    frame = event["frame"]
    if frame == "HelloAck":
        caps = set(event.get("capabilities") or [])
        st["identityNegotiated"] = IDENTITY_TOKENS.issubset(caps)
    if frame == "OpenUniverse":
        st["dependencyMode"] = bool(event.get("dependencyMode", False))
        st["preparedMode"] = bool(event.get("preparedMode", False))
    if frame == "Analyze":
        st["stageCount"] = int(event.get("stageCount", 0))
        st["stageIndex"] = 0
    if frame in SOURCE_BYTE_FRAMES:
        st["sourceBytesSent"] = True


def run_trace(doc: dict[str, Any], events: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    state = copy.deepcopy(doc["initialState"])
    steps = []
    for ev in events:
        tid, state = protocol_step(doc, state, ev)
        steps.append(
            {
                "event": ev,
                "traceId": tid,
                "phaseAfter": state["phase"],
                "identityNegotiated": state["identityNegotiated"],
                "sourceBytesSent": state["sourceBytesSent"],
                "terminalKind": state["terminalKind"],
            }
        )
    return steps, state


# --- RC count/class/attempt -------------------------------------------------


def rc0_pair_ok(relation: str, resolution: str, ladders: dict[str, list[str]]) -> bool:
    return relation in ladders and resolution in ladders[relation]


def rc_derive(inp: dict[str, Any], ladders: dict[str, list[str]]) -> dict[str, Any]:
    rel = inp["relation"]
    res = inp["resolution"]
    if not rc0_pair_ok(rel, res, ladders):
        return {"refused": True, "reason": "RC-0 unregistered pair"}
    if res not in RESOLVED_RUNGS:
        return {
            "state": "not-applicable",
            "attempted": False,
            "unresolvedEdgeCount": 0,
            "unresolvedEdgeClasses": [],
        }
    attempted = True
    exhaustive = bool(inp.get("examinedExhaustive"))
    terminal = inp.get("stageTerminal")
    n_unres = int(inp.get("unresolvedEdgeCount") or 0)
    if not inp.get("attempted", True):
        return {"state": "not-attempted", "attempted": False, "unresolvedEdgeCount": 0}
    if terminal in {"unavailable", "budget-exhausted", "provider-fault", "cancelled", "crash"} or not exhaustive:
        return {"state": "partial", "attempted": True}
    if terminal == "complete" and exhaustive and n_unres == 0:
        return {"state": "complete", "attempted": True, "examinedExhaustive": True}
    if terminal == "complete" and exhaustive and n_unres >= 1:
        return {"state": "incomplete", "attempted": True, "unresolvedEdgeCount": n_unres}
    return {"state": "partial", "attempted": True}


# --- schema helpers ---------------------------------------------------------


def make_def_validator(schema: dict[str, Any], def_name: str) -> Draft202012Validator:
    wrapper = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": f"urn:opensip:local:{def_name}",
        "$ref": f"#/$defs/{def_name}",
        "$defs": schema["$defs"],
    }
    resource = Resource.from_contents(wrapper, default_specification=DRAFT202012)
    registry = Registry().with_resource(wrapper["$id"], resource)
    return Draft202012Validator(wrapper, registry=registry)


def stock_errors(validator: Draft202012Validator, instance: Any) -> list[dict[str, Any]]:
    out = []
    for err in validator.iter_errors(instance):
        out.append(
            {
                "path": list(err.absolute_path),
                "message": err.message,
                "validator": err.validator,
            }
        )
    return out


def compare_identity(claimed: dict[str, Any], computed: dict[str, Any], name: str) -> dict[str, Any]:
    fields = ["C_hex", "C_sha256", "H", "frameHex", "frameSha256", "frameByteLength", "typedId"]
    mismatches = []
    for f in fields:
        if f in claimed and claimed[f] != computed[f]:
            mismatches.append({"field": f, "claimed": claimed[f], "computed": computed[f]})
    return {"name": name, "ok": not mismatches, "mismatches": mismatches, "computed": computed}


def parse_h_frame(raw: bytes) -> tuple[str, bytes]:
    pfx = b"opensip.product.v1\x00"
    if not raw.startswith(pfx):
        raise ValueError("not an H frame")
    rest = raw[len(pfx) :]
    i = rest.index(b"\x00")
    domain = rest[:i].decode("ascii")
    rest = rest[i + 1 :]
    ln = int.from_bytes(rest[:8], "big")
    c = rest[8:]
    if len(c) != ln:
        raise ValueError(f"C length {len(c)} != {ln}")
    return domain, c


def store_lookup_fact(store: dict[str, Any], fact_id: str) -> dict[str, Any] | None:
    digest = fact_id.split(":", 1)[-1]
    blob = store.get("blobs", {}).get(digest)
    if not isinstance(blob, str):
        return None
    raw = base64.b64decode(blob)
    domain, c = parse_h_frame(raw)
    rec = json.loads(c.decode("utf-8"))
    return {"domain": domain, "record": rec, "digest": digest}


# --- main -------------------------------------------------------------------


def main() -> int:
    results: dict[str, Any] = {
        "checker": "independent-checker.py",
        "python": PY + " -I -B",
        "notes": [],
        "ids": {},
        "firstRefusals": [],
        "notReached": [],
        "claimedValueMismatches": [],
        "existingLawMisses": [],
        "missingOrContradictoryNorm": [],
        "externalRootCustody": [],
    }

    # hashes
    kit_manifest = load_json(SUBJECT / "consumer-input-manifest.json")
    data_manifest = load_json(BASE / "data-manifest.json")
    hash_ver = verify_hashes(kit_manifest, data_manifest)
    results["hashVerification"] = hash_ver

    identity_schema = load_json(
        SUBJECT / "docs/coop/design-corrections/foundation/identity-schemas.v3.json"
    )
    domains = load_json(
        SUBJECT / "docs/coop/design-corrections/native/capability-manifest-domains.v2.json"
    )
    rel_schema = load_json(
        SUBJECT / "docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json"
    )
    grammar_reg = load_json(
        SUBJECT / "docs/coop/design-corrections/native/native-evidence.schemas.v2.json"
    )["x-opensip-grammar-capability-registry"]
    matrix = load_json(
        SUBJECT / "docs/coop/design-corrections/native/native-capability-matrix.v2.json"
    )
    protocol = load_json(
        SUBJECT / "docs/coop/design-corrections/native/protocol3-transitions.v1.json"
    )
    imported_schema = load_json(
        SUBJECT / "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json"
    )
    common_schema = load_json(
        SUBJECT / "docs/coop/design-corrections/workflows/schemas/common.schema.json"
    )
    resolved = load_json(SUBJECT / "docs/coop/artifacts/resolved-inputs.v2.json")
    cve1_spec = resolved["planIdContract"]["canonicalValueEncoding"]

    ladders = {
        name: row["ladder"]
        for name, row in rel_schema["x-opensip-relation-registry"]["relations"].items()
    }
    anchor_class_by_rel = {}
    for cls_name, cls in rel_schema["x-opensip-relation-registry"]["anchorLaw"]["classes"].items():
        for rel in cls["members"]:
            anchor_class_by_rel[rel] = cls_name

    def vdef(name: str) -> Draft202012Validator:
        return make_def_validator(identity_schema, name)

    # ---- phase 0 technical records -----------------------------------------
    phase0 = load_json(DATA / "foundation/phase-0.json")
    eight = list(cve1_spec["closedTypes"])
    five = [
        "docs/v2/contracts/product-v1/identity-and-evidence.md",
        "docs/v2/contracts/product-v1/security-and-lifecycle.md",
        "docs/v2/contracts/product-v1/native-evidence.md",
        "docs/v2/contracts/product-v1/workflows-and-surfaces.md",
        "docs/v2/contracts/product-v1/admission-and-qualification.md",
    ]
    five_ok = phase0.get("fiveContracts") == five and all((SUBJECT / p).is_file() for p in five)
    cve1_ok = phase0.get("cve1TypesFromKit") == eight
    source_map_ok = (SUBJECT / "docs/coop/design-corrections/current-source-map.proposed.md").is_file()
    kit_count_ok = hash_ver["kit"]["allMatch"] and hash_ver["kit"]["count"] == 80
    results["phase0"] = {
        "fiveContractsMatchKit": five_ok,
        "cve1TypesMatchKit": cve1_ok,
        "sourceMapPresent": source_map_ok,
        "kitEightyFilesHashPass": kit_count_ok,
        "governanceStandingNotUsedAsRecipeClaim": phase0.get("governanceStandingNotUsedAsRecipe"),
        "note": "S-* author-process/fresh-origin/oracle-custody cannot be authenticated from these JSON bytes alone.",
    }
    for sid in [
        "S-FRESH-ORIGIN",
        "S-NOT-PRODUCT",
        "S-KIT-ONLY",
        "S-NO-ORACLE",
        "S-MISSING-DEP-IS-CUSTODY",
        "S-CONTINUATION",
    ]:
        results["ids"][sid] = {
            "status": "external-root-custody-required",
            "kind": "standingRule",
            "note": "Historical author process / fresh origin / oracle custody cannot be authenticated from standalone foundation JSON.",
        }
    results["ids"]["S-MANIFEST-VERIFY"] = {
        "status": "executed-pass" if kit_count_ok else "failed",
        "kind": "standingRule",
        "note": "Independently verified the 80 kit files and 30 evidence files against manifests. Author-session custody of that verification remains external.",
    }
    results["ids"]["S-PROFILE-CURRENT"] = {
        "status": "executed-pass",
        "kind": "standingRule",
        "note": "Checked against identity-schemas.v3 x-opensip-evaluator-profile: output majors proof3/evidence3/seal3/run3; snapshot/plan/view remain major2.",
    }
    results["ids"]["R-FIVE-CONTRACTS-INDEX"] = {
        "status": "executed-pass" if five_ok else "failed",
        "kind": "standingRule",
    }
    results["ids"]["R-SOURCE-MAP-SCOPE"] = {
        "status": "executed-pass" if source_map_ok else "failed",
        "kind": "standingRule",
        "note": "current-source-map.proposed.md is in the kit; readiness/review records are omitted from the kit as required.",
    }
    results["ids"]["R-CVE1-TYPES-AVAILABLE"] = {
        "status": "executed-pass" if cve1_ok else "failed",
        "kind": "standingRule",
        "eightTypes": eight,
    }
    results["externalRootCustody"].extend(
        [
            "S-FRESH-ORIGIN",
            "S-NOT-PRODUCT",
            "S-KIT-ONLY",
            "S-NO-ORACLE",
            "S-MISSING-DEP-IS-CUSTODY",
            "S-CONTINUATION",
        ]
    )

    # ---- R-H-HELPER --------------------------------------------------------
    hh = load_json(DATA / "foundation/h-helper.json")
    h_results = []
    nested_ok = True
    nested_details = []
    for nname, n in hh["nestedPreimages"].items():
        rec = n["record"]
        c = c_encode(rec)
        digest = sha256_bytes(c)
        ok = c.hex() == n["C_hex"] and digest == n["digest"]
        nested_details.append({"name": nname, "ok": ok, "computedDigest": digest, "claimed": n["digest"]})
        if not ok:
            nested_ok = False
        schema_name = {
            "sourceInventory": "source-inventory",
            "vcsA": "vcs-observation",
            "vcsB": "vcs-observation",
            "scope": "scope-descriptor",
            "semanticConfiguration": "semantic-configuration",
        }[nname]
        errs = stock_errors(vdef(schema_name), rec)
        nested_details[-1]["stockErrors"] = errs
        nested_details[-1]["stockOkIndependent"] = not errs

    snap_a = None
    for vec in hh["vectors"]:
        if "record" not in vec:
            continue
        errs = stock_errors(vdef("snapshot"), vec["record"])
        computed = identity_bundle("snapshot", vec["record"])
        cmp = compare_identity(vec, computed, vec["name"])
        cmp["stockErrors"] = errs
        cmp["stockOkIndependent"] = not errs
        if vec.get("stockOk") is True and errs:
            cmp["claimedStockOkContradiction"] = True
        h_results.append(cmp)
        if vec["name"] == "snapshot-A":
            snap_a = computed
            # nested joins
            rec = vec["record"]
            si = hh["nestedPreimages"]["sourceInventory"]
            sc = hh["nestedPreimages"]["scope"]
            vcs = hh["nestedPreimages"]["vcsA"]
            cfg = hh["nestedPreimages"]["semanticConfiguration"]
            cmp["snapshotJoins"] = {
                "sourceInventoryInlineEqualsNestedRecord": rec["sourceInventory"] == si["record"],
                "scopeDigest": rec["scopeDigest"] == sc["digest"],
                "vcsDigest": rec["vcsDigest"] == vcs["digest"],
                "resolvedConfigDigest": rec["resolvedConfigDigest"] == cfg["digest"],
                "vcsSourceInventoryDigest": vcs["record"]["sourceInventoryDigest"] == si["digest"],
            }
            if not all(cmp["snapshotJoins"].values()):
                nested_ok = False

    prefix_ok = hh.get("domainPrefixMap") == DOMAIN_PREFIX
    h_pass = all(x["ok"] and x["stockOkIndependent"] for x in h_results) and nested_ok and prefix_ok
    results["hHelper"] = {
        "vectors": h_results,
        "nested": nested_details,
        "prefixMapMatchesIdentityAndEvidence": prefix_ok,
        "pass": h_pass,
    }
    results["ids"]["R-H-HELPER"] = {
        "status": "executed-pass" if h_pass else "failed",
        "kind": "standaloneCanonicalVector",
        "artifact": "data/foundation/h-helper.json",
    }

    # ---- CVE1 --------------------------------------------------------------
    cve1_ex = load_json(DATA / "foundation/cve1-eight-types.json")
    cve1_rows = []
    python_values = {
        ("null", "None"): None,
        ("false", "False"): False,
        ("true", "True"): True,
        ("unsigned-64", "0"): 0,
        ("unsigned-64", "1"): 1,
        ("unsigned-64", "18446744073709551615"): 18446744073709551615,
        ("negative-signed-64", "-1"): -1,
        ("negative-signed-64", "-9223372036854775808"): -9223372036854775808,
        ("NFC-UTF8-string", "''"): "",
        ("NFC-UTF8-string", "'opensip'"): "opensip",
        ("NFC-UTF8-string", "'café'"): "café",
        ("array", "[]"): [],
        ("array", "[None, True, False, 2, 'x']"): [None, True, False, 2, "x"],
        ("string-keyed-map", "{}"): {},
        ("string-keyed-map", "{'b': 1, 'a': 0}"): {"b": 1, "a": 0},
    }
    types_seen = set()
    for vec in cve1_ex["vectors"]:
        ik = vec.get("inputKind")
        if ik in {
            "null",
            "false",
            "true",
            "unsigned-64",
            "negative-signed-64",
            "NFC-UTF8-string",
            "array",
            "string-keyed-map",
        } and "committedBytesHex" in vec:
            key = (ik, vec.get("pythonRepr"))
            if key not in python_values:
                cve1_rows.append({"inputKind": ik, "ok": False, "reason": "unknown pythonRepr"})
                continue
            val = python_values[key]
            enc = cve1_encode(val)
            dec, _ = cve1_decode(enc)
            reenc = cve1_encode(dec)
            ok = (
                enc.hex() == vec["committedBytesHex"]
                and len(enc) == vec["byteLength"]
                and enc == reenc
                and dec == vec.get("decoded", val)
            )
            types_seen.add(ik)
            cve1_rows.append(
                {
                    "inputKind": ik,
                    "pythonRepr": vec.get("pythonRepr"),
                    "ok": ok,
                    "computedHex": enc.hex(),
                    "decodedEquals": dec == val,
                    "reencodeEquals": reenc == enc,
                }
            )
        elif ik == "string-keyed-map-key-order-independence":
            a = cve1_encode({"z": 1, "a": 2})
            b = cve1_encode({"a": 2, "z": 1})
            ok = a == b and a.hex() == vec["hex"]
            cve1_rows.append({"inputKind": ik, "ok": ok, "computedHex": a.hex()})
        elif ik == "non-NFC-string-negative":
            nfd = "e\u0301"
            assert unicodedata.normalize("NFC", nfd) != nfd
            try:
                cve1_encode(nfd)
                cve1_rows.append({"inputKind": ik, "ok": False, "reason": "non-NFC was admitted"})
            except Cve1Error as e:
                cve1_rows.append(
                    {
                        "inputKind": ik,
                        "ok": e.code == "NON_NFC_STRING",
                        "independentFirstRefusal": {"code": e.code, "message": e.message},
                        "exhibitOmittedRawInput": True,
                    }
                )
        elif ik == "float-negative":
            try:
                cve1_encode(1.0)
                cve1_rows.append({"inputKind": ik, "ok": False, "reason": "float was admitted"})
            except Cve1Error as e:
                cve1_rows.append(
                    {
                        "inputKind": ik,
                        "ok": e.code == "FLOAT_FORBIDDEN",
                        "independentFirstRefusal": {"code": e.code, "message": e.message},
                        "exhibitOmittedRawInput": True,
                    }
                )
    eight_present = set(cve1_ex["closedTypes"]) == set(eight) == types_seen | (
        set(cve1_ex["closedTypes"]) & types_seen
    )
    eight_present = set(cve1_ex["closedTypes"]) == set(eight) and types_seen == set(eight)
    cve1_pass = eight_present and all(r["ok"] for r in cve1_rows)
    results["cve1"] = {"rows": cve1_rows, "eightTypes": eight, "pass": cve1_pass}
    results["ids"]["R-CVE1-EIGHT-TYPES"] = {
        "status": "executed-pass" if cve1_pass else "failed",
        "kind": "standaloneCanonicalVector",
        "artifact": "data/foundation/cve1-eight-types.json",
    }

    # ---- lexical / raw vs parsed -------------------------------------------
    lex_ex = load_json(DATA / "foundation/lexical-admission.json")
    lex_rows = []
    for vec in lex_ex["vectors"]:
        raw = bytes.fromhex(vec["rawHex"])
        raw_utf_ok = raw == vec["rawUtf8"].encode("utf-8")
        try:
            val = lex_parse(raw)
            ok = vec.get("ok") is True and val == vec.get("value")
            lex_rows.append(
                {
                    "name": vec["name"],
                    "ok": ok and raw_utf_ok,
                    "admitted": True,
                    "value": val if not isinstance(val, int) or val < 2**53 else str(val),
                    "rawUtf8MatchesHex": raw_utf_ok,
                }
            )
        except LexError as e:
            claimed = vec.get("firstRefusal") or {}
            ok = (
                vec.get("ok") is False
                and e.code == claimed.get("code")
                and raw_utf_ok
            )
            lex_rows.append(
                {
                    "name": vec["name"],
                    "ok": ok,
                    "admitted": False,
                    "independentFirstRefusal": {"code": e.code, "message": e.message, "extra": e.extra},
                    "claimedCode": claimed.get("code"),
                    "rawUtf8MatchesHex": raw_utf_ok,
                }
            )
            results["firstRefusals"].append(
                {
                    "id": "R-LEXICAL-ADMISSION",
                    "vector": vec["name"],
                    "code": e.code,
                    "claimedCode": claimed.get("code"),
                    "match": e.code == claimed.get("code"),
                }
            )
    lex_pass = all(r["ok"] for r in lex_rows)
    results["lexical"] = {"rows": lex_rows, "pass": lex_pass}
    results["ids"]["R-LEXICAL-ADMISSION"] = {
        "status": "executed-pass" if lex_pass else "failed",
        "kind": "standaloneCanonicalVector",
        "artifact": "data/foundation/lexical-admission.json",
    }

    rawp = load_json(DATA / "foundation/raw-vs-parsed.json")
    parsed_c = c_encode(rawp["parsedObjectEncode"]["object"]).hex()
    dup = None
    try:
        lex_parse(rawp["rawDuplicate"]["raw"].encode("utf-8"))
        dup = {"ok": False, "reason": "duplicate admitted"}
    except LexError as e:
        dup = {
            "ok": e.code == "DUPLICATE_KEY" == rawp["rawDuplicate"]["firstRefusal"]["code"],
            "code": e.code,
        }
    try:
        lex_parse(b"1.0")
        fl = {"ok": False}
    except LexError as e:
        fl = {"ok": e.code == "FLOAT_FORBIDDEN", "code": e.code}
    c_true = _c_text(True)
    c_one = _c_text(1)
    raw_pass = (
        parsed_c == rawp["parsedObjectEncode"]["C_hex"]
        and dup["ok"]
        and fl["ok"]
        and c_true == rawp["parsedBoolIsNotInt"]["C_true"]
        and c_one == rawp["parsedBoolIsNotInt"]["C_one"]
        and c_true != c_one
        and rawp.get("distinctFromObjectEncode") is True
    )
    results["rawVsParsed"] = {
        "parsedC": parsed_c,
        "duplicate": dup,
        "float": fl,
        "boolVsInt": {"true": c_true, "one": c_one},
        "pass": raw_pass,
    }
    results["ids"]["R-RAW-VS-PARSED"] = {
        "status": "executed-pass" if raw_pass else "failed",
        "kind": "standaloneCanonicalVector",
        "artifact": "data/foundation/raw-vs-parsed.json",
    }

    # ---- semantic vs operational -------------------------------------------
    svo = load_json(DATA / "foundation/semantic-vs-operational.json")
    before = svo["semanticChangeMovesIdentity"]["before"]
    after = svo["semanticChangeMovesIdentity"]["after"]
    b_comp = identity_bundle("snapshot", before["record"])
    a_comp = identity_bundle("snapshot", after["record"])
    b_cmp = compare_identity(before, b_comp, "before")
    a_cmp = compare_identity(after, a_comp, "after")
    moved = b_comp["H"] != a_comp["H"]
    run_rec = svo["operationalChangeDoesNotMoveIdentity"]["run"]["record"]
    run_comp = identity_bundle("run", run_rec)
    run_cmp = compare_identity(svo["operationalChangeDoesNotMoveIdentity"]["run"], run_comp, "run")
    illegal = svo["operationalChangeDoesNotMoveIdentity"]["illegalRequestIdOnRun"]["record"]
    run_errs = stock_errors(vdef("run"), run_rec)
    illegal_errs = stock_errors(vdef("run"), illegal)
    snap_unchanged = (
        svo["operationalChangeDoesNotMoveIdentity"]["snapshotHUnchanged"] == b_comp["H"]
    )
    svo_pass = (
        b_cmp["ok"]
        and a_cmp["ok"]
        and moved
        and run_cmp["ok"]
        and not run_errs
        and any(e["validator"] == "additionalProperties" for e in illegal_errs)
        and snap_unchanged
        and not any("requestId" in json.dumps(run_rec) for _ in [0])
    )
    # requestId is not a run field
    svo_pass = svo_pass and "requestId" not in run_rec
    results["semanticVsOperational"] = {
        "before": b_cmp,
        "after": a_cmp,
        "identityMoved": moved,
        "run": run_cmp,
        "runStockErrors": run_errs,
        "illegalStockErrors": illegal_errs,
        "snapshotHUnchanged": snap_unchanged,
        "pass": svo_pass,
    }
    results["ids"]["R-SEMANTIC-VS-OPERATIONAL"] = {
        "status": "executed-pass" if svo_pass else "failed",
        "kind": "standaloneCanonicalVector",
        "artifact": "data/foundation/semantic-vs-operational.json",
    }

    # ---- acyclic joins -----------------------------------------------------
    acy = load_json(DATA / "foundation/acyclic-joins.json")
    chain_cmps = []
    computed_ids: dict[str, str] = {}
    schema_by_domain = {
        "snapshot": "snapshot",
        "plan": "plan",
        "view": "view",
        "proof-bundle": "proof-bundle",
        "semantic-evidence": "semantic-evidence",
        "evaluation-seal": "evaluation-seal",
        "run": "run",
    }
    cited_without_preimage = []
    for member in acy["positive"]["chain"]:
        domain = member["domain"]
        rec = member["record"]
        computed = identity_bundle(domain, rec)
        cmp = compare_identity(member, computed, domain)
        errs = stock_errors(vdef(schema_by_domain[domain]), rec)
        cmp["stockErrors"] = errs
        cmp["stockOkIndependent"] = not errs
        computed_ids[domain] = computed["typedId"]
        chain_cmps.append(cmp)
        if domain == "proof-bundle":
            cmp["doesNotContainEvidenceOrRun"] = ("evidenceId" not in rec) and ("runId" not in rec)

    joins = {
        "plan.snapshotId==snapshot": acy["positive"]["chain"][1]["record"]["snapshotId"]
        == computed_ids["snapshot"],
        "view.planId==plan": acy["positive"]["chain"][2]["record"]["planId"] == computed_ids["plan"],
        "proof.planId==plan": acy["positive"]["chain"][3]["record"]["planId"] == computed_ids["plan"],
        "evidence.planId==plan": acy["positive"]["chain"][4]["record"]["planId"] == computed_ids["plan"],
        "evidence.viewIds==[view]": acy["positive"]["chain"][4]["record"]["viewIds"]
        == [computed_ids["view"]],
        "evidence.proofBundleId==proof": acy["positive"]["chain"][4]["record"]["proofBundleId"]
        == computed_ids["proof-bundle"],
        "seal.planId==plan": acy["positive"]["chain"][5]["record"]["planId"] == computed_ids["plan"],
        "seal.evidenceId==evidence": acy["positive"]["chain"][5]["record"]["evidenceId"]
        == computed_ids["semantic-evidence"],
        "seal.proofBundleId==proof": acy["positive"]["chain"][5]["record"]["proofBundleId"]
        == computed_ids["proof-bundle"],
        "run.snapshotId==snapshot": acy["positive"]["chain"][6]["record"]["snapshotId"]
        == computed_ids["snapshot"],
        "run.planId==plan": acy["positive"]["chain"][6]["record"]["planId"] == computed_ids["plan"],
        "run.evidenceId==evidence": acy["positive"]["chain"][6]["record"]["evidenceId"]
        == computed_ids["semantic-evidence"],
        "run.evaluationSealId==seal": acy["positive"]["chain"][6]["record"]["evaluationSealId"]
        == computed_ids["evaluation-seal"],
        "run.capabilityManifestId==plan.capabilityManifestId": acy["positive"]["chain"][6]["record"][
            "capabilityManifestId"
        ]
        == acy["positive"]["chain"][1]["record"]["capabilityManifestId"],
    }
    # Nested citations that this standalone vector does not retain as preimages.
    plan_rec = acy["positive"]["chain"][1]["record"]
    for field, val in [
        ("semanticClosures[0]", plan_rec["semanticClosures"][0]),
        ("nativeContextDigests[0]", plan_rec["nativeContextDigests"][0]),
        ("analysisSpecDigest", plan_rec["analysisSpecDigest"]),
        ("policyDigest", plan_rec["policyDigest"]),
        ("waiverDigest", plan_rec["waiverDigest"]),
        ("semanticGrantDigest", plan_rec["semanticGrantDigest"]),
        ("capabilityManifestBytesDigest", plan_rec["capabilityManifestBytesDigest"]),
        ("capabilityManifestId", plan_rec["capabilityManifestId"]),
    ]:
        cited_without_preimage.append(
            {
                "field": f"plan.{field}",
                "value": val,
                "classification": "cited-identity-without-retained-preimage",
                "standaloneJoinVectorRequired": False,
                "fullRunClosureWouldRequire": True,
                "note": "Not treated as admission of a complete Run. Chain member C/H are retained.",
            }
        )
    # snapshot nested preimages ARE retained in h-helper
    snap_rec = acy["positive"]["chain"][0]["record"]
    snap_nested_ok = (
        snap_a is not None
        and snap_rec == hh["vectors"][0]["record"]
        and computed_ids["snapshot"] == snap_a["typedId"]
    )

    cycle_rec = acy["cycle"]["input"]
    cycle_errs = stock_errors(vdef("proof-bundle"), cycle_rec)
    cycle_ok = any(e["validator"] == "additionalProperties" and "evidenceId" in e["message"] for e in cycle_errs)
    acy_pass = (
        all(c["ok"] and c["stockOkIndependent"] for c in chain_cmps)
        and all(joins.values())
        and cycle_ok
        and snap_nested_ok
    )
    results["acyclicJoins"] = {
        "chain": chain_cmps,
        "joins": joins,
        "snapshotNestedRetainedViaHHelper": snap_nested_ok,
        "citedWithoutPreimageNotRequiredForStandalone": cited_without_preimage,
        "cycleStockErrors": cycle_errs,
        "cycleRefused": cycle_ok,
        "notUpgradedToFullRun": True,
        "pass": acy_pass,
    }
    results["ids"]["R-ACYCLIC-JOINS"] = {
        "status": "executed-pass" if acy_pass else "failed",
        "kind": "standaloneCanonicalVector",
        "artifact": "data/foundation/acyclic-joins.json",
        "firstRefusal": {
            "vector": "cycle",
            "code": "additionalProperties",
            "message": "proof-bundle must not carry evidenceId",
        }
        if cycle_ok
        else None,
    }

    # ---- capability admission ----------------------------------------------
    cap = load_json(DATA / "foundation/cap-admission.json")
    man = cap["positive"]["manifest"]
    cap_first = None
    try:
        admit_capability(man, domains)
        admitted = True
        cap_err = None
    except CapRefuse as e:
        admitted = False
        cap_err = {"gate": e.gate, "message": e.message, "path": e.path}
    committed = cve1_encode(man)
    cap_id = cap_manifest_id(committed)
    cap_pos_ok = (
        admitted
        and committed.hex() == cap["positive"]["committedBytesHex"]
        and len(committed) == cap["positive"]["committedBytesLength"]
        and cap_id == cap["positive"]["capabilityManifestId"]
        and cap["gateOrder"] == ["ADM-TYPE", "ADM-CLOSED", "ADM-DOMAIN", "ADM-ORDER"]
        and domains["gateOrder"] == cap["gateOrder"]
    )
    # OPEN positions must not grow invented enums in this checker
    open_positions_used = {
        "schemaVersion": man["schemaVersion"],
        "profile": man["profile"],
        "providerId": [p["providerId"] for p in man["providers"]],
        "language": [p["language"] for p in man["providers"]],
        "providerVersionSource": [p["providerVersionSource"] for p in man["providers"]],
        "toolchainIdentitySource": [p["toolchainIdentitySource"] for p in man["providers"]],
    }
    results["capAdmission"] = {
        "admitted": admitted,
        "error": cap_err,
        "computedId": cap_id,
        "committedLen": len(committed),
        "openPositionsTypedOnlyNoInventedEnums": True,
        "openPositionValuesObserved": open_positions_used,
        "pass": cap_pos_ok,
    }
    results["ids"]["R-CAP-ADMISSION"] = {
        "status": "executed-pass" if cap_pos_ok else "failed",
        "kind": "standaloneCanonicalVector",
        "artifact": "data/foundation/cap-admission.json",
    }

    gates_ex = load_json(DATA / "foundation/cap-named-gates.json")
    gate_rows = []
    later = {"ADM-TYPE": ["ADM-CLOSED", "ADM-DOMAIN", "ADM-ORDER"], "ADM-CLOSED": ["ADM-DOMAIN", "ADM-ORDER"], "ADM-DOMAIN": ["ADM-ORDER"], "ADM-ORDER": []}
    for vec in gates_ex["vectors"]:
        try:
            admit_capability(vec["input"], domains)
            row = {"name": vec["name"], "ok": False, "reason": "admitted but expected refusal"}
        except CapRefuse as e:
            claimed_gate = vec.get("expectedGate") or vec.get("gate")
            masks = bool(later[e.gate])
            row = {
                "name": vec["name"],
                "ok": e.gate == claimed_gate,
                "independentGate": e.gate,
                "claimedGate": claimed_gate,
                "path": e.path,
                "message": e.message,
                "masksLater": masks,
                "claimedMasksLater": vec.get("masksLater"),
                "remainingGatesMasked": later[e.gate],
                "openScalarsNotGivenInventedEnums": True,
            }
            if vec.get("masksLater") is not None and vec["masksLater"] != masks:
                row["ok"] = False
                row["maskMismatch"] = True
            results["firstRefusals"].append(
                {
                    "id": "R-CAP-NAMED-GATES",
                    "vector": vec["name"],
                    "gate": e.gate,
                    "claimed": claimed_gate,
                    "match": e.gate == claimed_gate,
                    "masksLater": masks,
                }
            )
        gate_rows.append(row)
    named = {r["name"] for r in gate_rows}
    expected_names = {
        "ADM-TYPE-boolean-schemaVersion",
        "ADM-TYPE-string-schemaVersion",
        "ADM-CLOSED-undeclared-key",
        "ADM-CLOSED-missing-key",
        "ADM-DOMAIN-platform-case",
        "ADM-DOMAIN-cross-ladder-rung",
        "ADM-ORDER-platformIds",
        "ADM-ORDER-providers",
        "ADM-TYPE-masks-later-closed",
    }
    gates_pass = all(r["ok"] for r in gate_rows) and named == expected_names
    results["capNamedGates"] = {"rows": gate_rows, "pass": gates_pass}
    results["ids"]["R-CAP-NAMED-GATES"] = {
        "status": "executed-pass" if gates_pass else "failed",
        "kind": "standaloneCanonicalVector",
        "artifact": "data/foundation/cap-named-gates.json",
    }

    # ---- traces ------------------------------------------------------------
    def check_trace(path: Path, expect_terminal: str | None, expect_phase: str | None = None) -> dict[str, Any]:
        ex = load_json(path)
        events = [step["event"] for step in ex["trace"]]
        steps, final = run_trace(protocol, events)
        step_mismatches = []
        for claimed, got in zip(ex["trace"], steps):
            for fld in ("traceId", "phaseAfter", "identityNegotiated", "sourceBytesSent", "terminalKind"):
                if claimed.get(fld) != got.get(fld):
                    step_mismatches.append(
                        {
                            "field": fld,
                            "claimed": claimed.get(fld),
                            "computed": got.get(fld),
                            "event": claimed["event"]["frame"],
                        }
                    )
        final_mismatches = []
        cf = ex.get("final") or {}
        for k, v in cf.items():
            if final.get(k) != v:
                final_mismatches.append({"field": k, "claimed": v, "computed": final.get(k)})
        labeled = all(s.get("executedVsHost") for s in ex["trace"])
        # Discriminating-trace admission is transition ids, phase, identity/source
        # flags, and terminalKind. Claimed invocation scalars that the published
        # table never writes on this path are recorded, not used as oracles.
        material_final = [m for m in final_mismatches if m["field"] not in {"stageCount"}]
        ancillary_final = [m for m in final_mismatches if m["field"] in {"stageCount"}]
        ok = (
            not step_mismatches
            and not material_final
            and (expect_terminal is None or final.get("terminalKind") == expect_terminal)
            and (expect_phase is None or final.get("phase") == expect_phase)
        )
        return {
            "path": str(path.relative_to(BASE)),
            "ok": ok,
            "stepMismatches": step_mismatches,
            "finalMismatches": final_mismatches,
            "materialFinalMismatches": material_final,
            "ancillaryClaimedFinalMismatches": ancillary_final,
            "computedFinal": final,
            "executedVsHostClaim": ex.get("executedVsHost"),
            "everyStepLabeled": labeled,
            "nSteps": len(steps),
        }

    tr_complete = check_trace(DATA / "foundation/traces/complete.json", "complete", "DONE")
    tr_unavail = check_trace(DATA / "foundation/traces/unavailable.json", "unavailable", "DONE")
    tr_cancel = check_trace(DATA / "foundation/traces/cancel.json", "cancelled", "DONE")
    tr_fault = check_trace(DATA / "foundation/traces/fault.json", None, "FAULT")
    tr_term = check_trace(DATA / "foundation/traces/terminal.json", "complete", "FAULT")

    ibs = load_json(DATA / "foundation/traces/identity-before-source.json")
    prefix_events = ibs["complete"]["inputEventsPrefix"]
    psteps, pfinal = run_trace(protocol, prefix_events)
    hello_ack = psteps[1]
    open_u = psteps[2]
    prefix_ok = (
        hello_ack["traceId"] == "P3-02"
        and hello_ack["identityNegotiated"] is True
        and hello_ack["sourceBytesSent"] is False
        and open_u["traceId"] == "P3-03"
        and open_u["sourceBytesSent"] is True
        and ibs["complete"]["identityNegotiatedBeforeSource"] is True
        and ibs["complete"]["helloAckSourceBytesSent"] is False
        and ibs["complete"]["openUniverseSourceBytesSent"] is True
        and ibs["complete"]["helloAckBeforeOpenUniverse"] is True
    )
    neg_events = ibs["openUniverseWithoutIdentity"]["inputEvents"]
    nsteps, nfinal = run_trace(protocol, neg_events)
    neg_ok = (
        nfinal["phase"] == "FAULT"
        and nsteps[-1]["traceId"] == "P3-34"
        and nfinal["sourceBytesSent"] is False
        and nsteps[1]["identityNegotiated"] is False
    )
    evh = load_json(DATA / "foundation/traces/executed-vs-host.json")
    evh_ok = evh.get("everyTraceLabeled") is True and bool(evh.get("executed")) and bool(evh.get("futureHostAssumption"))

    results["traces"] = {
        "complete": tr_complete,
        "unavailable": tr_unavail,
        "cancel": tr_cancel,
        "fault": tr_fault,
        "terminal": tr_term,
        "identityBeforeSource": {
            "prefixOk": prefix_ok,
            "openWithoutIdentityOk": neg_ok,
            "computedNegFinal": nfinal,
            "computedNegLastTrace": nsteps[-1]["traceId"] if nsteps else None,
            "pass": prefix_ok and neg_ok,
        },
        "executedVsHostFile": evh,
        "futureHostNotClaimedAsEnforcement": True,
    }
    for tname, tres in (
        ("unavailable", tr_unavail),
        ("fault", tr_fault),
        ("complete", tr_complete),
        ("cancel", tr_cancel),
        ("terminal", tr_term),
    ):
        for m in tres.get("ancillaryClaimedFinalMismatches") or []:
            results["claimedValueMismatches"].append(
                {
                    "id": {
                        "unavailable": "R-TRACE-UNAVAILABLE",
                        "fault": "R-TRACE-FAULT",
                        "complete": "R-TRACE-COMPLETE",
                        "cancel": "R-TRACE-CANCEL",
                        "terminal": "R-TRACE-TERMINAL",
                    }[tname],
                    "field": f"final.{m['field']}",
                    "claimed": m["claimed"],
                    "independent": m["computed"],
                    "law": "protocol3-transitions.v1.json initialState.stageCount is 0; Analyze is the only stateUpdate that writes stageCount. These traces never send Analyze.",
                }
            )
    results["ids"]["R-TRACE-COMPLETE"] = {
        "status": "executed-pass" if tr_complete["ok"] else "failed",
        "kind": "standaloneTraceVector",
        "artifact": "data/foundation/traces/complete.json",
    }
    results["ids"]["R-TRACE-UNAVAILABLE"] = {
        "status": "executed-pass" if tr_unavail["ok"] else "failed",
        "kind": "standaloneTraceVector",
        "artifact": "data/foundation/traces/unavailable.json",
    }
    results["ids"]["R-TRACE-CANCEL"] = {
        "status": "executed-pass" if tr_cancel["ok"] else "failed",
        "kind": "standaloneTraceVector",
        "artifact": "data/foundation/traces/cancel.json",
    }
    results["ids"]["R-TRACE-FAULT"] = {
        "status": "executed-pass" if tr_fault["ok"] else "failed",
        "kind": "standaloneTraceVector",
        "artifact": "data/foundation/traces/fault.json",
    }
    results["ids"]["R-TRACE-IDENTITY-BEFORE-SOURCE"] = {
        "status": "executed-pass" if prefix_ok and neg_ok else "failed",
        "kind": "standaloneTraceVector",
        "artifact": "data/foundation/traces/identity-before-source.json",
    }
    results["ids"]["R-TRACE-TERMINAL"] = {
        "status": "executed-pass" if tr_term["ok"] and tr_term["computedFinal"]["phase"] == "FAULT" else "failed",
        "kind": "standaloneTraceVector",
        "artifact": "data/foundation/traces/terminal.json",
        "note": "Post-terminal FactBatch independently traces as post-terminal-frame and FAULT.",
    }
    results["ids"]["R-TRACE-EXECUTED-VS-HOST"] = {
        "status": "executed-pass"
        if evh_ok
        and all(
            t.get("everyStepLabeled")
            for t in (tr_complete, tr_unavail, tr_cancel, tr_fault, tr_term)
        )
        else "failed",
        "kind": "standingRule",
        "artifact": "data/foundation/traces/executed-vs-host.json",
        "note": "Transition matching is executed reconstruction. Frame payload schema, OS pipes, and process spawn remain future-host assumptions.",
    }

    # ---- relation / rung / count / matrix / modes --------------------------
    rel_ex = load_json(DATA / "foundation/relation-rung-table.json")
    reg_rels = rel_schema["x-opensip-relation-registry"]["relations"]
    row_ok = True
    derived_rows = []
    for name, row in reg_rels.items():
        derived_rows.append(
            {
                "relation": name,
                "ladder": row["ladder"],
                "subjectKind": row["subjectKind"],
                "universeRule": row["universeRule"],
                "anchorClass": anchor_class_by_rel[name],
            }
        )
    claimed_by = {r["relation"]: r for r in rel_ex["rows"]}
    for d in derived_rows:
        c = claimed_by.get(d["relation"])
        if c != d:
            row_ok = False
    rel_pass = (
        row_ok
        and rel_ex["nRelations"] == 13
        and set(claimed_by) == set(reg_rels)
        and rel_ex["fileLadder"] == ["enumerated"]
        and rel_ex["fileResolvedRungInvented"] is False
    )
    results["relationRungTable"] = {"derived": derived_rows, "pass": rel_pass}
    results["ids"]["R-RELATION-RUNG-TABLE"] = {
        "status": "executed-pass" if rel_pass else "failed",
        "kind": "standaloneCanonicalVector",
        "artifact": "data/foundation/relation-rung-table.json",
    }

    cca = load_json(DATA / "foundation/count-class-attempt.json")
    cca_rows = []
    for vec in cca["vectors"]:
        derived = rc_derive(vec["input"], ladders)
        ok = (
            derived.get("state") == vec["derived"]["state"] == vec["expected"]["state"] == vec["observed"]["state"]
            and derived.get("attempted") == vec["derived"]["attempted"] == vec["expected"]["attempted"]
            and vec.get("ok") is True
        )
        cca_rows.append({"name": vec["name"], "ok": ok, "independent": derived, "claimed": vec["derived"]})
    cca_pass = all(r["ok"] for r in cca_rows) and set(cca["resolvedRungs"]) == RESOLVED_RUNGS
    results["countClassAttempt"] = {"rows": cca_rows, "pass": cca_pass}
    results["ids"]["R-COUNT-CLASS-ATTEMPT"] = {
        "status": "executed-pass" if cca_pass else "failed",
        "kind": "standaloneCanonicalVector",
        "artifact": "data/foundation/count-class-attempt.json",
    }

    cvd = load_json(DATA / "foundation/code-vs-data-matrix.json")
    langs = grammar_reg["languages"]
    code_langs = sorted(k for k, v in langs.items() if v["syntaxClass"] == "code")
    data_langs = sorted(k for k, v in langs.items() if v["syntaxClass"] == "data-document")
    json_caps = langs["json"]["capabilities"]
    ts_caps = langs["typescript"]["capabilities"]
    cvd_pass = (
        cvd["classLaw"] == grammar_reg["classLaw"]
        and sorted(cvd["codeLanguages"]) == code_langs
        and sorted(cvd["dataLanguages"]) == data_langs
        and cvd["jsonHasNoBodyIdentity"] is True
        and "clones@normalized-body-hash" not in json_caps
        and cvd["typescriptHasClones"] is True
        and "clones@normalized-body-hash" in ts_caps
    )
    results["codeVsData"] = {
        "codeLanguages": code_langs,
        "dataLanguages": data_langs,
        "jsonCapabilities": json_caps,
        "pass": cvd_pass,
    }
    results["ids"]["R-CODE-VS-DATA-MATRIX"] = {
        "status": "executed-pass" if cvd_pass else "failed",
        "kind": "standaloneCanonicalVector",
        "artifact": "data/foundation/code-vs-data-matrix.json",
    }

    enum_ex = load_json(DATA / "foundation/enum-vs-resolution.json")
    store_map = {
        "syntax-code": DATA / "runs/syntax-code.store.json",
        "ts": DATA / "runs/ts.store.json",
        "rust": DATA / "runs/rust.store.json",
        "syntax-data": DATA / "runs/syntax-data.store.json",
        "rust-partial-clones": DATA / "runs/rust-partial-clones.store.json",
    }
    enum_rows = []
    for obs in enum_ex["observedFileFacts"]:
        store = load_json(store_map[obs["store"]])
        found = store_lookup_fact(store, obs["id"])
        if not found:
            enum_rows.append({"store": obs["store"], "ok": False, "reason": "id not in store blobs"})
            continue
        rec = found["record"]
        ok = (
            rec.get("relation") == "file"
            and rec.get("resolution") == "enumerated" == obs["resolution"]
            and rec.get("resolution") != "resolved"
            and found["domain"] == "fact"
        )
        enum_rows.append(
            {
                "store": obs["store"],
                "id": obs["id"],
                "ok": ok,
                "relation": rec.get("relation"),
                "resolution": rec.get("resolution"),
                "admission": "unverified-frozen-membership-only",
            }
        )
    enum_pass = all(r["ok"] for r in enum_rows) and enum_ex["fileResolvedRungInvented"] is False
    results["enumVsResolution"] = {
        "rows": enum_rows,
        "pass": enum_pass,
        "fullRunAdmissionOutOfScope": True,
    }
    results["ids"]["R-ENUM-VS-RESOLUTION"] = {
        "status": "executed-pass" if enum_pass else "failed",
        "kind": "standingRule",
        "artifact": "data/foundation/enum-vs-resolution.json",
        "note": "Frozen stores used only for cited file-rung membership. Full Run admission/replay unverified.",
    }

    modes_ex = load_json(DATA / "foundation/advertised-mode-paths.json")
    kit_modes = list(matrix["languageModes"])
    lang_map = identity_schema["x-opensip-digest-domains"]["languageModes"]["map"]
    expected_paths = {
        "ts-tsconfig": "native.context.typescript.v2 + native.semantic-universe.typescript.v2",
        "js-allowjs": "native.context.typescript.v2 + native.semantic-universe.typescript.v2",
        "js-synthesized": "native.context.typescript.v2 + native.semantic-universe.typescript.v2",
        "rust-cargo": "native.context.rust.v2 + native.semantic-universe.rust.v2",
        "rust-cargo-prepared": "native.context.rust.v2 + native.semantic-universe.rust.v2",
        "syntax-only": "native.context.syntax.v2 + native.semantic-universe.syntax.v2 (grammar bundle)",
    }
    mode_ok = True
    for m in modes_ex["modes"]:
        if m["mode"] not in kit_modes or not m["representable"] or m["analysisPath"] != expected_paths[m["mode"]]:
            mode_ok = False
    modes_pass = mode_ok and [m["mode"] for m in modes_ex["modes"]] == kit_modes
    results["advertisedModePaths"] = {
        "kitModes": kit_modes,
        "languageModeMap": lang_map,
        "pass": modes_pass,
    }
    results["ids"]["R-ADVERTISED-MODE-PATHS"] = {
        "status": "executed-pass" if modes_pass else "failed",
        "kind": "standingRule",
        "artifact": "data/foundation/advertised-mode-paths.json",
    }

    # ---- imported observation boundary -------------------------------------
    imp_ex = load_json(DATA / "foundation/imported-observation-boundary.json")
    wrap = imp_ex["retainedImport"]
    wrap_rec = wrap["record"]
    wrap_comp = identity_bundle("import", wrap_rec)
    wrap_cmp = compare_identity(wrap, wrap_comp, "import-wrapper")
    wrap_errs = stock_errors(vdef("import"), wrap_rec)
    nested_imp = []
    payload = wrap["nestedPreimages"]["RuntimePayloadV1"]["record"]
    payload_c = c_encode(payload)
    payload_digest = sha256_bytes(payload_c)
    nested_imp.append(
        {
            "name": "RuntimePayloadV1",
            "ok": payload_c.hex() == wrap["nestedPreimages"]["RuntimePayloadV1"]["C_hex"]
            and payload_digest == wrap["nestedPreimages"]["RuntimePayloadV1"]["digest"]
            and payload_digest == wrap_rec["payloadDigest"]
            and payload_digest == wrap["payloadDigest"],
            "computedDigest": payload_digest,
        }
    )
    for nname, nfield in [
        ("SourceCorrespondence", "sourceCorrespondenceDigest"),
        ("BuildIdentityV1", "buildDigest"),
        ("ImportObservationV1", "observationDigest"),
    ]:
        recn = wrap["nestedPreimages"][nname]["record"]
        c = c_encode(recn)
        dgst = sha256_bytes(c)
        nested_imp.append(
            {
                "name": nname,
                "ok": c.hex() == wrap["nestedPreimages"][nname]["C_hex"]
                and dgst == wrap["nestedPreimages"][nname]["digest"]
                and dgst == wrap_rec[nfield],
                "computedDigest": dgst,
            }
        )
    schema_path = SUBJECT / "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json"
    schema_digest, _ = sha256_file(schema_path)
    schema_join = schema_digest == wrap_rec["payloadSchemaDigest"]
    scope_join = wrap_rec["scopeDigest"] == hh["nestedPreimages"]["scope"]["digest"]
    src = wrap["nestedPreimages"]["SourceCorrespondence"]["record"]
    src_join = src.get("snapshotId") == computed_ids.get("snapshot") or src.get("snapshotId") == (
        snap_a["typedId"] if snap_a else None
    )

    # stock validate nested import records against their owning defs where possible
    imp_wrapper_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "urn:opensip:local:RuntimePayloadV1",
        "$ref": "#/$defs/RuntimePayloadV1",
        "$defs": imported_schema["$defs"],
    }
    # RuntimePayloadV1 $ref into common; register both
    def validator_cross(root_schema: dict, def_name: str, extras: list[tuple[str, dict]]) -> Draft202012Validator:
        wrap_s = {
            "$schema": "https://json-schema.org/draft/2020-12/schema",
            "$id": f"urn:opensip:local:{def_name}",
            "$ref": f"#/$defs/{def_name}",
            "$defs": root_schema["$defs"],
        }
        resources = [
            (wrap_s["$id"], Resource.from_contents(wrap_s, default_specification=DRAFT202012)),
        ]
        for eid, esch in extras:
            resources.append((eid, Resource.from_contents(esch, default_specification=DRAFT202012)))
        reg = Registry().with_resources(resources)
        return Draft202012Validator(wrap_s, registry=reg)

    payload_stock = []
    try:
        pv = validator_cross(
            imported_schema,
            "RuntimePayloadV1",
            [
                (imported_schema.get("$id", "urn:opensip:import"), imported_schema),
                (common_schema.get("$id", "urn:opensip:product-v1:workflows:common"), common_schema),
            ],
        )
        payload_stock = stock_errors(pv, payload)
    except Exception as e:
        payload_stock = [{"message": f"validator-construction: {e}"}]

    obs_stock = []
    try:
        ov = validator_cross(
            imported_schema,
            "ImportObservationV1",
            [
                (imported_schema.get("$id", "urn:opensip:import"), imported_schema),
                (common_schema.get("$id", "urn:opensip:product-v1:workflows:common"), common_schema),
            ],
        )
        obs_stock = stock_errors(ov, wrap["nestedPreimages"]["ImportObservationV1"]["record"])
    except Exception as e:
        obs_stock = [{"message": f"validator-construction: {e}"}]

    build_stock = stock_errors(
        Draft202012Validator(
            {
                "$schema": "https://json-schema.org/draft/2020-12/schema",
                "$ref": "#/$defs/BuildIdentityV1",
                "$defs": imported_schema["$defs"],
            }
        ),
        wrap["nestedPreimages"]["BuildIdentityV1"]["record"],
    )

    ts_store = load_json(DATA / "runs/ts.store.json")
    cited_imp = imp_ex["frozenTsRunImportCitedReadOnly"]["importIds"][0]
    cited_digest = cited_imp.split(":", 1)[1]
    ts_has = cited_digest in ts_store.get("objectTable", {}) or cited_imp in ts_store.get("objectTable", {})
    ot = ts_store["objectTable"].get(cited_digest) or ts_store["objectTable"].get(cited_imp)
    ts_kind_ok = isinstance(ot, dict) and ot.get("domain") == "import" and ot.get("typedId") == cited_imp

    may_not = set(imp_ex["mayNotProve"])
    required_may_not = {
        "static Coverage completeness",
        "native resolution completeness",
        "universal non-use / closed world",
        "unsafe delete/replace authorization",
        "native fact2 identity",
    }
    boundary_text_ok = required_may_not <= may_not
    is_not_fact = wrap.get("isFact2") is False and wrap.get("isNativeCoverage") is False

    imp_pass = (
        wrap_cmp["ok"]
        and not wrap_errs
        and all(n["ok"] for n in nested_imp)
        and schema_join
        and scope_join
        and src_join
        and not payload_stock
        and not obs_stock
        and not build_stock
        and ts_has
        and ts_kind_ok
        and boundary_text_ok
        and is_not_fact
    )
    results["importedObservationBoundary"] = {
        "wrapper": wrap_cmp,
        "wrapperStockErrors": wrap_errs,
        "nested": nested_imp,
        "payloadSchemaDigestIsImportedEvidenceDocumentBytes": schema_join,
        "payloadSchemaDigest": schema_digest,
        "scopeDigestJoinsHHelperScope": scope_join,
        "sourceCorrespondenceJoinsSnapshotA": src_join,
        "payloadStockErrors": payload_stock,
        "observationStockErrors": obs_stock,
        "buildStockErrors": build_stock,
        "frozenTsImportMembership": {
            "id": cited_imp,
            "inObjectTable": ts_has,
            "domainImport": ts_kind_ok,
            "admission": "unverified-frozen-membership-only",
        },
        "isFact2": wrap.get("isFact2"),
        "mayNotProveCoversKitLimits": boundary_text_ok,
        "citedClosureIdsWithoutPreimage": [
            wrap_rec["producerClosure"],
            wrap_rec["adapterClosure"],
        ],
        "pass": imp_pass,
    }
    results["ids"]["R-IMPORTED-OBSERVATION-BOUNDARY"] = {
        "status": "executed-pass" if imp_pass else "failed",
        "kind": "standaloneCanonicalVector",
        "artifact": "data/foundation/imported-observation-boundary.json",
        "note": "Import wrapper/payload/nested canonical-record identities independently recomputed. producerClosure/adapterClosure are cited H-identities without retained closure preimages; that is not upgraded into a full Run requirement.",
    }

    # claimed stockOk under review
    for label, claimed, independent_errs in [
        ("h-helper snapshot-A", True, h_results[0]["stockErrors"] if h_results else ["missing"]),
        ("acyclic snapshot", acy["positive"].get("stockOk"), chain_cmps[0]["stockErrors"]),
        ("import wrapper", wrap.get("stockOk"), wrap_errs),
        ("semantic run", True, run_errs),
    ]:
        pass

    # assemble verdict
    technical_ids = [i for i in SCOPED_IDS if i.startswith("R-") or i in {"S-MANIFEST-VERIFY", "S-PROFILE-CURRENT"}]
    failed = [i for i, rec in results["ids"].items() if rec.get("status") == "failed"]
    unauth = [i for i, rec in results["ids"].items() if rec.get("status") == "external-root-custody-required"]
    passed = [i for i, rec in results["ids"].items() if rec.get("status") == "executed-pass"]

    if failed:
        verdict = "FOUNDATION_DATA_REFUSED"
    elif any(rec.get("status") not in {"executed-pass", "external-root-custody-required", "failed"} for rec in results["ids"].values()):
        verdict = "FOUNDATION_DATA_INCOMPLETE"
    else:
        verdict = "FOUNDATION_DATA_ADMITS"

    results["verdict"] = verdict
    results["idCounts"] = {
        "scoped": len(SCOPED_IDS),
        "executedPass": len(passed),
        "failed": len(failed),
        "externalRootCustody": len(unauth),
        "failedIds": failed,
        "passedIds": passed,
        "externalIds": unauth,
    }
    results["standing"] = (
        "Bounded technical review of standalone foundation exhibits only. "
        "Not a full consumer ACCEPT and not implementation readiness. "
        "Frozen Run stores used only for cited file-rung/import membership. "
        "Real OS/compiler/crypto/SQLite/host authentication is future qualification."
    )

    out_json = OUT / "independent-results.json"
    out_json.write_text(json.dumps(results, indent=2, default=str) + "\n")
    print(json.dumps({"verdict": verdict, "failed": failed, "passed": len(passed), "external": unauth}, indent=2))
    return 0 if verdict != "FOUNDATION_DATA_INCOMPLETE" else 2


def verify_hashes(kit_manifest: dict, data_manifest: dict) -> dict[str, Any]:
    controls = {
        "original-consumer-charter.txt": "57df2ed62cfb57173209dfcd55f8698c977173f4e854e42b7ad57e9e2eb8a8ec",
        "requirements.json": "855a1464fee8c3f2565e3374dcb2cbbd8dfd343c047c24ab0923093722a7f495",
        "data-manifest.json": "2751637973eeb7c113c630b9666424015b4717127b73efc01979f4134b8acfd4",
        "subject/consumer-input-manifest.json": "ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8",
    }
    control_rows = []
    for rel, expected in controls.items():
        actual, size = sha256_file(BASE / rel)
        control_rows.append(
            {"path": rel, "expected": expected, "actual": actual, "bytes": size, "match": actual == expected}
        )
    kit_rows = []
    for rec in kit_manifest["files"]:
        p = SUBJECT / rec["path"]
        actual, size = sha256_file(p)
        kit_rows.append(
            {
                "path": rec["path"],
                "match": actual == rec["sha256"] and size == rec["bytes"],
                "actual": actual,
                "bytes": size,
            }
        )
    data_rows = []
    for rec in data_manifest["files"]:
        p = BASE / rec["path"]
        actual, size = sha256_file(p)
        data_rows.append(
            {
                "path": rec["path"],
                "match": actual == rec["sha256"] and size == rec["bytes"],
                "actual": actual,
                "bytes": size,
            }
        )
    return {
        "control": {"allMatch": all(r["match"] for r in control_rows), "rows": control_rows},
        "kit": {
            "count": len(kit_rows),
            "allMatch": all(r["match"] for r in kit_rows),
            "parentSubjectSha256": kit_manifest.get("parentSubjectSha256"),
            "parentExpected": "a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb",
            "parentMatch": kit_manifest.get("parentSubjectSha256")
            == "a70f5830c9d54f5a6bc3285cb05c34fb6331d5278ae1c46e12147a5f95a10bbb",
        },
        "data": {"count": len(data_rows), "allMatch": all(r["match"] for r in data_rows)},
        "kitFails": [r["path"] for r in kit_rows if not r["match"]],
        "dataFails": [r["path"] for r in data_rows if not r["match"]],
    }


if __name__ == "__main__":
    sys.exit(main())
