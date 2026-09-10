"""Independent C encoder and lexical admission from identity-and-evidence §3.

Owner: docs/v2/contracts/product-v1/identity-and-evidence.md §3
and identity-schemas.v3.json x-opensip-order vocabulary.
"""
from __future__ import annotations

import re
from typing import Any


class LexicalRefusal(Exception):
    def __init__(self, code: str, message: str, offset: int | None = None):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message
        self.offset = offset


CONTROL_ESCAPES = {
    0x08: "\\b",
    0x09: "\\t",
    0x0A: "\\n",
    0x0C: "\\f",
    0x0D: "\\r",
}


def encode_c(value: Any) -> bytes:
    """Canonical JSON: UTF-8 byte-ordered keys, no whitespace, no trailing newline.

    Arrays keep admitted order. Integers are shortest ordinary decimal.
    Quote and backslash escaped; controls use \\b\\t\\n\\f\\r or lowercase \\u00xx.
    Slash is not escaped. Unicode scalars are unescaped. No Unicode normalization.
    """
    return _encode(value)


def _encode(value: Any) -> bytes:
    if value is None:
        return b"null"
    if value is True:
        return b"true"
    if value is False:
        return b"false"
    if isinstance(value, bool):
        return b"true" if value else b"false"
    if isinstance(value, int) and not isinstance(value, bool):
        if value < -(2**63) or value > (2**64 - 1):
            raise LexicalRefusal("INTEGER_RANGE", f"integer {value} outside [-2^63, 2^64-1]")
        return str(value).encode("ascii")
    if isinstance(value, float):
        raise LexicalRefusal("FLOAT_FORBIDDEN", "floating tokens are refused")
    if isinstance(value, str):
        return _encode_string(value)
    if isinstance(value, list):
        parts = [_encode(item) for item in value]
        return b"[" + b",".join(parts) + b"]"
    if isinstance(value, dict):
        keys = list(value.keys())
        for k in keys:
            if not isinstance(k, str):
                raise LexicalRefusal("NON_STRING_KEY", f"object key type {type(k).__name__}")
        encoded_keys = [(k.encode("utf-8"), k) for k in keys]
        encoded_keys.sort(key=lambda kv: kv[0])
        seen = set()
        members = []
        for kb, k in encoded_keys:
            if kb in seen:
                raise LexicalRefusal("DUPLICATE_KEY", f"duplicate key after utf-8 sort: {k!r}")
            seen.add(kb)
            members.append(_encode_string(k) + b":" + _encode(value[k]))
        return b"{" + b",".join(members) + b"}"
    raise LexicalRefusal("UNSUPPORTED_TYPE", f"cannot encode {type(value).__name__}")


def _encode_string(s: str) -> bytes:
    out = ['"']
    for ch in s:
        o = ord(ch)
        if ch == '"':
            out.append('\\"')
        elif ch == "\\":
            out.append("\\\\")
        elif o in CONTROL_ESCAPES:
            out.append(CONTROL_ESCAPES[o])
        elif o < 0x20:
            out.append(f"\\u{o:04x}")
        else:
            out.append(ch)
    out.append('"')
    return "".join(out).encode("utf-8")


def lexical_scan_raw(raw: bytes) -> Any:
    """Refuse duplicate keys, floats/exponents, -0, nonfinite, malformed UTF-8,
    non-scalar Unicode, before decode/encode of already-parsed objects.
    """
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        raise LexicalRefusal("MALFORMED_UTF8", str(e)) from e
    for i, ch in enumerate(text):
        o = ord(ch)
        if 0xD800 <= o <= 0xDFFF:
            raise LexicalRefusal("NON_SCALAR_UNICODE", f"surrogate U+{o:04X}", i)
    parser = _RawParser(text)
    value = parser.parse_value()
    parser.skip_ws()
    if parser.i != len(text):
        raise LexicalRefusal("TRAILING", "trailing bytes after one JSON value", parser.i)
    return value


class _RawParser:
    def __init__(self, text: str):
        self.text = text
        self.i = 0
        self.n = len(text)

    def skip_ws(self) -> None:
        # C forbids whitespace in canonical form, but stored blobs may be pretty
        # printed; lexical admission of *raw input* still rejects the numeric
        # faults below. Whitespace here is only used when the caller asked for
        # a parse of already-retained bytes (not as a producing encoder).
        while self.i < self.n and self.text[self.i] in " \t\r\n":
            self.i += 1

    def parse_value(self) -> Any:
        self.skip_ws()
        if self.i >= self.n:
            raise LexicalRefusal("EMPTY", "empty input")
        ch = self.text[self.i]
        if ch == "{":
            return self.parse_object()
        if ch == "[":
            return self.parse_array()
        if ch == '"':
            return self.parse_string()
        if ch == "t":
            return self.parse_lit("true", True)
        if ch == "f":
            return self.parse_lit("false", False)
        if ch == "n":
            return self.parse_lit("null", None)
        if ch == "-" or ch.isdigit():
            return self.parse_number()
        raise LexicalRefusal("UNEXPECTED", f"unexpected {ch!r}", self.i)

    def parse_lit(self, lit: str, value: Any) -> Any:
        if self.text.startswith(lit, self.i):
            self.i += len(lit)
            return value
        raise LexicalRefusal("LITERAL", f"expected {lit}", self.i)

    def parse_number(self) -> int:
        start = self.i
        if self.text[self.i] == "-":
            self.i += 1
            if self.i >= self.n or not self.text[self.i].isdigit():
                raise LexicalRefusal("NUMBER", "minus without digits", start)
        if self.i < self.n and self.text[self.i] == "0":
            self.i += 1
            if self.i < self.n and self.text[self.i].isdigit():
                raise LexicalRefusal("LEADING_ZERO", "leading zero", start)
        else:
            while self.i < self.n and self.text[self.i].isdigit():
                self.i += 1
        token = self.text[start : self.i]
        if self.i < self.n and self.text[self.i] in ".eE":
            raise LexicalRefusal("FLOAT_OR_EXPONENT", f"non-integer token {token!r}...", start)
        if token == "-0" or token == "+0":
            raise LexicalRefusal("NEGATIVE_ZERO", token, start)
        if token == "-":
            raise LexicalRefusal("NUMBER", "bare minus", start)
        value = int(token)
        if value < -(2**63) or value > (2**64 - 1):
            raise LexicalRefusal("INTEGER_RANGE", token, start)
        return value

    def parse_string(self) -> str:
        assert self.text[self.i] == '"'
        self.i += 1
        out = []
        while self.i < self.n:
            ch = self.text[self.i]
            if ch == '"':
                self.i += 1
                return "".join(out)
            if ch == "\\":
                self.i += 1
                if self.i >= self.n:
                    raise LexicalRefusal("STRING", "truncated escape")
                e = self.text[self.i]
                self.i += 1
                mapping = {'"': '"', "\\": "\\", "/": "/", "b": "\b", "t": "\t", "n": "\n", "f": "\f", "r": "\r"}
                if e in mapping:
                    out.append(mapping[e])
                    continue
                if e == "u":
                    hex4 = self.text[self.i : self.i + 4]
                    if len(hex4) < 4 or any(c not in "0123456789abcdefABCDEF" for c in hex4):
                        raise LexicalRefusal("STRING", "bad \\u escape", self.i)
                    cp = int(hex4, 16)
                    self.i += 4
                    if 0xD800 <= cp <= 0xDFFF:
                        raise LexicalRefusal("NON_SCALAR_UNICODE", f"surrogate \\u{hex4}", self.i)
                    out.append(chr(cp))
                    continue
                raise LexicalRefusal("STRING", f"unknown escape \\{e}", self.i)
            if ord(ch) < 0x20:
                raise LexicalRefusal("STRING", "unescaped control", self.i)
            out.append(ch)
            self.i += 1
        raise LexicalRefusal("STRING", "unterminated string")

    def parse_array(self) -> list[Any]:
        assert self.text[self.i] == "["
        self.i += 1
        self.skip_ws()
        items: list[Any] = []
        if self.i < self.n and self.text[self.i] == "]":
            self.i += 1
            return items
        while True:
            items.append(self.parse_value())
            self.skip_ws()
            if self.i >= self.n:
                raise LexicalRefusal("ARRAY", "unterminated array")
            if self.text[self.i] == ",":
                self.i += 1
                continue
            if self.text[self.i] == "]":
                self.i += 1
                return items
            raise LexicalRefusal("ARRAY", "expected comma or ]", self.i)

    def parse_object(self) -> dict[str, Any]:
        assert self.text[self.i] == "{"
        self.i += 1
        self.skip_ws()
        obj: dict[str, Any] = {}
        if self.i < self.n and self.text[self.i] == "}":
            self.i += 1
            return obj
        while True:
            self.skip_ws()
            if self.i >= self.n or self.text[self.i] != '"':
                raise LexicalRefusal("OBJECT", "expected string key", self.i)
            key = self.parse_string()
            if key in obj:
                raise LexicalRefusal("DUPLICATE_KEY", f"duplicate key {key!r}", self.i)
            self.skip_ws()
            if self.i >= self.n or self.text[self.i] != ":":
                raise LexicalRefusal("OBJECT", "expected colon", self.i)
            self.i += 1
            obj[key] = self.parse_value()
            self.skip_ws()
            if self.i >= self.n:
                raise LexicalRefusal("OBJECT", "unterminated object")
            if self.text[self.i] == ",":
                self.i += 1
                continue
            if self.text[self.i] == "}":
                self.i += 1
                return obj
            raise LexicalRefusal("OBJECT", "expected comma or }", self.i)


ORDER_VOCABULARY = {
    "sequence",
    "canonical-set",
    "canonical-order",
    "utf8",
    "path",
    "numeric",
    "ordinal",
    "predicate",
    "ruleId",
    "waiverId",
}


def check_order(annotation: Any, items: list[Any]) -> list[str]:
    """Enforce x-opensip-order. Unknown annotation refuses."""
    faults: list[str] = []
    if annotation is None:
        return faults
    if isinstance(annotation, dict) and "by" in annotation:
        keys = annotation["by"]
        if not isinstance(keys, list) or not keys:
            return [f"ORDER_BY_EMPTY:{annotation!r}"]
        tuples = []
        for i, item in enumerate(items):
            if not isinstance(item, dict):
                faults.append(f"ORDER_BY_NON_OBJECT:{i}")
                continue
            tup = []
            for k in keys:
                if k not in item:
                    faults.append(f"ORDER_BY_MISSING_KEY:{i}:{k}")
                    tup.append("")
                else:
                    v = item[k]
                    if not isinstance(v, str):
                        v = str(v)
                    tup.append(v.encode("utf-8"))
            tuples.append((i, tuple(tup)))
        decoded = [t[1] for t in tuples]
        if decoded != sorted(decoded):
            faults.append("ORDER_BY_NOT_ASCENDING")
        if len(set(decoded)) != len(decoded):
            faults.append("ORDER_BY_DUPLICATE_KEYS")
        return faults
    if annotation not in ORDER_VOCABULARY:
        return [f"ORDER_UNKNOWN_VOCABULARY:{annotation!r}"]
    if annotation == "sequence":
        return faults
    if annotation == "canonical-set":
        encoded = [encode_c(item) for item in items]
        if encoded != sorted(encoded):
            faults.append("ORDER_CANONICAL_SET_NOT_ASCENDING")
        if len(set(encoded)) != len(encoded):
            faults.append("ORDER_CANONICAL_SET_DUPLICATE")
        return faults
    if annotation == "canonical-order":
        encoded = [encode_c(item) for item in items]
        if encoded != sorted(encoded):
            faults.append("ORDER_CANONICAL_ORDER_NOT_NONDECREASING")
        return faults
    if annotation == "utf8":
        if any(not isinstance(x, str) for x in items):
            faults.append("ORDER_UTF8_NON_STRING")
            return faults
        encoded = [x.encode("utf-8") for x in items]
        if encoded != sorted(encoded):
            faults.append("ORDER_UTF8_NOT_ASCENDING")
        if len(set(encoded)) != len(encoded):
            faults.append("ORDER_UTF8_DUPLICATE")
        return faults
    if annotation == "path":
        paths = []
        for i, item in enumerate(items):
            if isinstance(item, str):
                paths.append(item.encode("utf-8"))
            elif isinstance(item, dict) and "path" in item and isinstance(item["path"], str):
                paths.append(item["path"].encode("utf-8"))
            else:
                faults.append(f"ORDER_PATH_MISSING:{i}")
                paths.append(b"")
        if paths != sorted(paths):
            faults.append("ORDER_PATH_NOT_ASCENDING")
        if len(set(paths)) != len(paths):
            faults.append("ORDER_PATH_DUPLICATE")
        return faults
    if annotation == "numeric":
        nums = []
        for i, item in enumerate(items):
            if isinstance(item, int) and not isinstance(item, bool):
                nums.append(item)
            else:
                faults.append(f"ORDER_NUMERIC_NON_INT:{i}")
                nums.append(0)
        if nums != sorted(nums):
            faults.append("ORDER_NUMERIC_NOT_ASCENDING")
        if len(set(nums)) != len(nums):
            faults.append("ORDER_NUMERIC_DUPLICATE")
        return faults
    if annotation == "ordinal":
        ords = []
        for i, item in enumerate(items):
            if isinstance(item, dict) and isinstance(item.get("ordinal"), int):
                ords.append(item["ordinal"])
            else:
                faults.append(f"ORDER_ORDINAL_MISSING:{i}")
                ords.append(-1)
        if ords != list(range(len(ords))):
            faults.append(f"ORDER_ORDINAL_NOT_CONTIGUOUS:{ords}")
        return faults
    if annotation == "predicate":
        tups = []
        for i, item in enumerate(items):
            if not isinstance(item, dict):
                faults.append(f"ORDER_PREDICATE_NON_OBJECT:{i}")
                tups.append((b"", b"", b""))
                continue
            tups.append(
                (
                    str(item.get("ruleId", "")).encode("utf-8"),
                    str(item.get("subjectId", "")).encode("utf-8"),
                    str(item.get("predicateId", "")).encode("utf-8"),
                )
            )
        if tups != sorted(tups):
            faults.append("ORDER_PREDICATE_NOT_ASCENDING")
        if len(set(tups)) != len(tups):
            faults.append("ORDER_PREDICATE_DUPLICATE")
        return faults
    if annotation in ("ruleId", "waiverId"):
        vals = []
        for i, item in enumerate(items):
            if isinstance(item, dict) and isinstance(item.get(annotation), str):
                vals.append(item[annotation].encode("utf-8"))
            elif isinstance(item, str):
                vals.append(item.encode("utf-8"))
            else:
                faults.append(f"ORDER_{annotation}_MISSING:{i}")
                vals.append(b"")
        if vals != sorted(vals):
            faults.append(f"ORDER_{annotation}_NOT_ASCENDING")
        if len(set(vals)) != len(vals):
            faults.append(f"ORDER_{annotation}_DUPLICATE")
        return faults
    return faults


def glob_match(pattern: str, path: str) -> bool:
    """workflows_model.v1.glob_match law: **/*.ts matches root a.ts."""
    if pattern == "**" or pattern == "**/**":
        return True
    rx = _glob_to_re(pattern)
    return re.fullmatch(rx, path) is not None


def _glob_to_re(pattern: str) -> str:
    out = []
    i = 0
    n = len(pattern)
    while i < n:
        if pattern.startswith("**/", i):
            out.append("(?:.*/)?")
            i += 3
            continue
        if pattern.startswith("**", i):
            out.append(".*")
            i += 2
            continue
        ch = pattern[i]
        if ch == "*":
            out.append("[^/]*")
        elif ch == "?":
            out.append("[^/]")
        elif ch in ".^$+{}[]|()\\":
            out.append("\\" + ch)
        else:
            out.append(ch)
        i += 1
    return "".join(out)


def path_in_scope(path: str, workspace_roots: list[str], path_prefixes: list[str], excluded: list[str]) -> bool:
    """Import/scope-descriptor law: under a workspaceRoots member AND a pathPrefixes
    member (empty prefixes admit remaining paths) and not under excludedPathPrefixes.
    Concatenating the two arrays as a single OR-prefix list is forbidden.
    """
    if not _under_any_prefix(path, workspace_roots):
        return False
    if path_prefixes and not _under_any_prefix(path, path_prefixes):
        return False
    if _under_any_prefix(path, excluded):
        return False
    return True


def _under_any_prefix(path: str, prefixes: list[str]) -> bool:
    for p in prefixes:
        if p in (".", ""):
            return True
        if path == p or path.startswith(p.rstrip("/") + "/"):
            return True
    return False
