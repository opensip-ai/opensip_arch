"""Lexical admission on RAW UTF-8 JSON before decode (admission-and-qualification §1,
identity-and-evidence §3). Duplicate keys, floats, exponents, -0, nonfinite,
malformed UTF-8, and integer-range faults refuse here — not after json.loads.
"""
from __future__ import annotations

from typing import Any, Optional

I64_MIN = -(2**63)
U64_MAX = 2**64 - 1
MAX_BYTES = 4 * 1024 * 1024
MAX_DEPTH = 32


class LexicalError(Exception):
    def __init__(self, code: str, message: str, position: int = -1):
        super().__init__(f"{code}: {message}")
        self.code = code
        self.message = message
        self.position = position
        self.firstRefusal = code


def admit_raw(raw: bytes) -> Any:
    if len(raw) > MAX_BYTES:
        raise LexicalError("LEX_SIZE", "descriptor exceeds 4 MiB")
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError as e:
        raise LexicalError("LEX_UTF8", "malformed UTF-8") from e
    # Reject non-scalar Unicode (surrogates cannot appear in valid UTF-8
    # decoded Python str; still refuse U+FFFE/FFFF? contract: non-scalar).
    for i, ch in enumerate(text):
        o = ord(ch)
        if 0xD800 <= o <= 0xDFFF:
            raise LexicalError("LEX_SURROGATE", "non-scalar Unicode", i)
    p = _Parser(text)
    value = p.parse_value(depth=0 if _is_container_start(p) else 0)
    p.skip_ws()
    if p.i < len(p.s):
        raise LexicalError("LEX_TRAILING", "trailing content after value", p.i)
    return value


def _is_container_start(p: "_Parser") -> bool:
    p.skip_ws()
    return p.i < len(p.s) and p.s[p.i] in "{["


class _Parser:
    def __init__(self, s: str):
        self.s = s
        self.i = 0

    def skip_ws(self) -> None:
        while self.i < len(self.s) and self.s[self.i] in " \t\r\n":
            self.i += 1

    def peek(self) -> str:
        if self.i >= len(self.s):
            raise LexicalError("LEX_EOF", "unexpected end", self.i)
        return self.s[self.i]

    def parse_value(self, depth: int) -> Any:
        self.skip_ws()
        ch = self.peek()
        if ch == "{":
            return self.parse_object(depth + 1)
        if ch == "[":
            return self.parse_array(depth + 1)
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
        raise LexicalError("LEX_TOKEN", f"unexpected {ch!r}", self.i)

    def parse_lit(self, lit: str, value: Any) -> Any:
        if self.s[self.i : self.i + len(lit)] != lit:
            raise LexicalError("LEX_TOKEN", f"expected {lit}", self.i)
        self.i += len(lit)
        return value

    def parse_object(self, depth: int) -> dict:
        if depth > MAX_DEPTH:
            raise LexicalError("LEX_DEPTH", "nesting depth exceeds 32", self.i)
        assert self.s[self.i] == "{"
        self.i += 1
        self.skip_ws()
        out: dict[str, Any] = {}
        seen: set[str] = set()
        if self.peek() == "}":
            self.i += 1
            return out
        while True:
            self.skip_ws()
            if self.peek() != '"':
                raise LexicalError("LEX_KEY", "object key must be string", self.i)
            key = self.parse_string()
            if key in seen:
                raise LexicalError("LEX_DUP_KEY", f"duplicate key {key!r}", self.i)
            seen.add(key)
            self.skip_ws()
            if self.peek() != ":":
                raise LexicalError("LEX_COLON", "expected colon", self.i)
            self.i += 1
            val = self.parse_value(depth)
            out[key] = val
            self.skip_ws()
            ch = self.peek()
            if ch == ",":
                self.i += 1
                continue
            if ch == "}":
                self.i += 1
                return out
            raise LexicalError("LEX_OBJECT", "expected comma or }", self.i)

    def parse_array(self, depth: int) -> list:
        if depth > MAX_DEPTH:
            raise LexicalError("LEX_DEPTH", "nesting depth exceeds 32", self.i)
        assert self.s[self.i] == "["
        self.i += 1
        self.skip_ws()
        out: list[Any] = []
        if self.peek() == "]":
            self.i += 1
            return out
        while True:
            out.append(self.parse_value(depth))
            self.skip_ws()
            ch = self.peek()
            if ch == ",":
                self.i += 1
                continue
            if ch == "]":
                self.i += 1
                return out
            raise LexicalError("LEX_ARRAY", "expected comma or ]", self.i)

    def parse_string(self) -> str:
        assert self.s[self.i] == '"'
        self.i += 1
        out = []
        s = self.s
        n = len(s)
        while self.i < n:
            ch = s[self.i]
            if ch == '"':
                self.i += 1
                return "".join(out)
            if ch == "\\":
                self.i += 1
                if self.i >= n:
                    raise LexicalError("LEX_STRING", "truncated escape", self.i)
                e = s[self.i]
                self.i += 1
                mapping = {
                    '"': '"',
                    "\\": "\\",
                    "/": "/",
                    "b": "\b",
                    "f": "\f",
                    "n": "\n",
                    "r": "\r",
                    "t": "\t",
                }
                if e in mapping:
                    out.append(mapping[e])
                    continue
                if e == "u":
                    hexpart = s[self.i : self.i + 4]
                    if len(hexpart) < 4 or any(c not in "0123456789abcdefABCDEF" for c in hexpart):
                        raise LexicalError("LEX_UNICODE", "invalid \\u escape", self.i)
                    cp = int(hexpart, 16)
                    self.i += 4
                    if 0xD800 <= cp <= 0xDBFF:
                        # surrogate pair required
                        if s[self.i : self.i + 2] != "\\u":
                            raise LexicalError("LEX_SURROGATE", "unpaired high surrogate", self.i)
                        self.i += 2
                        hex2 = s[self.i : self.i + 4]
                        if len(hex2) < 4:
                            raise LexicalError("LEX_SURROGATE", "truncated low surrogate", self.i)
                        cp2 = int(hex2, 16)
                        self.i += 4
                        if not (0xDC00 <= cp2 <= 0xDFFF):
                            raise LexicalError("LEX_SURROGATE", "invalid low surrogate", self.i)
                        cp = 0x10000 + ((cp - 0xD800) << 10) + (cp2 - 0xDC00)
                    elif 0xDC00 <= cp <= 0xDFFF:
                        raise LexicalError("LEX_SURROGATE", "unpaired low surrogate", self.i)
                    out.append(chr(cp))
                    continue
                raise LexicalError("LEX_ESCAPE", f"invalid escape \\{e}", self.i)
            if ord(ch) < 0x20:
                raise LexicalError("LEX_CONTROL", "unescaped control in string", self.i)
            out.append(ch)
            self.i += 1
        raise LexicalError("LEX_STRING", "unterminated string", self.i)

    def parse_number(self) -> int:
        start = self.i
        s = self.s
        if s[self.i] == "-":
            self.i += 1
        if self.i >= len(s) or not s[self.i].isdigit():
            raise LexicalError("LEX_NUMBER", "invalid number", start)
        if s[self.i] == "0":
            self.i += 1
            if self.i < len(s) and s[self.i].isdigit():
                raise LexicalError("LEX_LEADING_ZERO", "leading zero", start)
        else:
            while self.i < len(s) and s[self.i].isdigit():
                self.i += 1
        token = s[start : self.i]
        if self.i < len(s) and s[self.i] in ".eE":
            raise LexicalError(
                "LEX_NON_INTEGER",
                f"integer field refuses float/exponent token {s[start:self.i+1]!r}",
                start,
            )
        if token == "-0":
            raise LexicalError("LEX_NEG_ZERO", "-0 is rejected", start)
        if token.startswith("-"):
            n = int(token)
            if n < I64_MIN:
                raise LexicalError("LEX_INT_RANGE", "integer below -2^63", start)
            return n
        n = int(token)
        if n > U64_MAX:
            raise LexicalError("LEX_INT_RANGE", "integer above 2^64-1", start)
        return n
