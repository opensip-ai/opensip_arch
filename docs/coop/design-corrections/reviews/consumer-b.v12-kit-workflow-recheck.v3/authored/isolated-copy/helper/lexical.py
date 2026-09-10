"""Raw-input lexical admission from identity-and-evidence §3.

Refuse before deserialization loses lexical information:
duplicate keys, floating/exponent tokens, -0, nonfinite tokens,
malformed UTF-8, non-scalar Unicode. Integer range [-2^63, 2^64-1].
Booleans distinct. Descriptor max 4 MiB. Nesting depth 32 (root=1).
"""
from __future__ import annotations

from typing import Any

from helper.errors import AdmissionError

I64_MIN = -9223372036854775808
U64_MAX = 18446744073709551615
MAX_BYTES = 4 * 1024 * 1024
MAX_DEPTH = 32


class RawAdmit:
    def __init__(self, raw: bytes):
        if not isinstance(raw, (bytes, bytearray)):
            raise AdmissionError("LEXICAL_NOT_BYTES", "raw input must be exact bytes")
        if len(raw) > MAX_BYTES:
            raise AdmissionError("DESCRIPTOR_TOO_LARGE", f"descriptor {len(raw)} exceeds 4 MiB")
        try:
            self.text = raw.decode("utf-8")
        except UnicodeDecodeError as e:
            raise AdmissionError("MALFORMED_UTF8", str(e)) from e
        if self.text.startswith("\ufeff"):
            raise AdmissionError("BOM_FORBIDDEN", "UTF-8 BOM is not admitted")
        self.s = self.text
        self.n = len(self.s)
        self.i = 0

    def peek(self) -> str:
        return self.s[self.i] if self.i < self.n else ""

    def skip_ws(self) -> None:
        while self.i < self.n and self.s[self.i] in " \t\n\r":
            self.i += 1

    def parse(self) -> Any:
        value = self._value(depth=1)
        self.skip_ws()
        if self.i != self.n:
            raise AdmissionError("TRAILING_JUNK", f"trailing bytes at {self.i}")
        return value

    def _value(self, depth: int) -> Any:
        if depth > MAX_DEPTH:
            raise AdmissionError("NESTING_TOO_DEEP", f"nesting depth {depth} exceeds {MAX_DEPTH}")
        self.skip_ws()
        if self.i >= self.n:
            raise AdmissionError("UNEXPECTED_EOF", "unexpected end of input")
        c = self.s[self.i]
        if c == "{":
            return self._object(depth)
        if c == "[":
            return self._array(depth)
        if c == '"':
            return self._string()
        if c == "t":
            return self._literal("true", True)
        if c == "f":
            return self._literal("false", False)
        if c == "n":
            return self._literal("null", None)
        if c == "-" or c.isdigit():
            return self._number()
        raise AdmissionError("UNEXPECTED_TOKEN", f"unexpected {c!r} at {self.i}")

    def _literal(self, lit: str, value: Any) -> Any:
        if self.s.startswith(lit, self.i):
            self.i += len(lit)
            return value
        raise AdmissionError("UNEXPECTED_TOKEN", f"expected {lit} at {self.i}")

    def _object(self, depth: int) -> dict:
        self.i += 1  # {
        self.skip_ws()
        out: dict[str, Any] = {}
        seen: set[str] = set()
        if self.peek() == "}":
            self.i += 1
            return out
        while True:
            self.skip_ws()
            if self.peek() != '"':
                raise AdmissionError("OBJECT_KEY_NOT_STRING", f"object key must be string at {self.i}")
            key = self._string()
            if key in seen:
                raise AdmissionError("DUPLICATE_KEY", f"duplicate key {key!r}", extra={"key": key})
            seen.add(key)
            self.skip_ws()
            if self.peek() != ":":
                raise AdmissionError("EXPECTED_COLON", f"expected ':' at {self.i}")
            self.i += 1
            val = self._value(depth + 1)
            out[key] = val
            self.skip_ws()
            c = self.peek()
            if c == ",":
                self.i += 1
                continue
            if c == "}":
                self.i += 1
                return out
            raise AdmissionError("EXPECTED_COMMA_OR_END", f"expected ',' or '}}' at {self.i}")

    def _array(self, depth: int) -> list:
        self.i += 1  # [
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
            raise AdmissionError("EXPECTED_COMMA_OR_END", f"expected ',' or ']' at {self.i}")

    def _string(self) -> str:
        if self.peek() != '"':
            raise AdmissionError("EXPECTED_STRING", f"expected string at {self.i}")
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
                raise AdmissionError("UNESCAPED_CONTROL", f"unescaped control U+{o:04X} at {self.i}")
            if 0xD800 <= o <= 0xDFFF:
                raise AdmissionError("NON_SCALAR_UNICODE", f"surrogate U+{o:04X} in UTF-8 text")
            chars.append(c)
            self.i += 1
        raise AdmissionError("UNTERMINATED_STRING", "unterminated string")

    def _escape(self) -> str:
        if self.i >= self.n:
            raise AdmissionError("UNTERMINATED_STRING", "unterminated escape")
        c = self.s[self.i]
        self.i += 1
        table = {
            '"': '"',
            "\\": "\\",
            "/": "/",
            "b": "\b",
            "f": "\f",
            "n": "\n",
            "r": "\r",
            "t": "\t",
        }
        if c in table:
            return table[c]
        if c == "u":
            return self._u_escape()
        raise AdmissionError("BAD_ESCAPE", f"invalid escape \\{c}")

    def _hex4(self) -> int:
        if self.i + 4 > self.n:
            raise AdmissionError("BAD_UNICODE_ESCAPE", "truncated \\u escape")
        h = self.s[self.i : self.i + 4]
        self.i += 4
        try:
            return int(h, 16)
        except ValueError as e:
            raise AdmissionError("BAD_UNICODE_ESCAPE", f"non-hex \\u{h}") from e

    def _u_escape(self) -> str:
        cp = self._hex4()
        if 0xD800 <= cp <= 0xDBFF:
            # high surrogate; require a following \u low surrogate
            if self.i + 6 <= self.n and self.s[self.i : self.i + 2] == "\\u":
                self.i += 2
                low = self._hex4()
                if 0xDC00 <= low <= 0xDFFF:
                    scalar = 0x10000 + ((cp - 0xD800) << 10) + (low - 0xDC00)
                    return chr(scalar)
                raise AdmissionError("NON_SCALAR_UNICODE", f"high surrogate U+{cp:04X} not followed by low")
            raise AdmissionError("NON_SCALAR_UNICODE", f"unpaired high surrogate U+{cp:04X}")
        if 0xDC00 <= cp <= 0xDFFF:
            raise AdmissionError("NON_SCALAR_UNICODE", f"unpaired low surrogate U+{cp:04X}")
        return chr(cp)

    def _number(self) -> int:
        start = self.i
        neg = False
        if self.peek() == "-":
            neg = True
            self.i += 1
            if self.i >= self.n or not self.s[self.i].isdigit():
                raise AdmissionError("BAD_NUMBER", f"lone minus at {start}")
        if self.i >= self.n or not self.s[self.i].isdigit():
            raise AdmissionError("BAD_NUMBER", f"expected digit at {self.i}")
        # integer part: 0 or [1-9][0-9]*
        if self.s[self.i] == "0":
            self.i += 1
            if self.i < self.n and self.s[self.i].isdigit():
                raise AdmissionError("LEADING_ZERO", "leading zeros forbidden", extra={"token": self.s[start : self.i + 1]})
        else:
            while self.i < self.n and self.s[self.i].isdigit():
                self.i += 1
        # fraction / exponent refuse
        if self.i < self.n and self.s[self.i] == ".":
            raise AdmissionError("FLOAT_FORBIDDEN", "floating-point tokens refused", extra={"at": start})
        if self.i < self.n and self.s[self.i] in "eE":
            raise AdmissionError("EXPONENT_FORBIDDEN", "exponent tokens refused", extra={"at": start})
        token = self.s[start : self.i]
        if token in ("-0",):
            raise AdmissionError("NEG_ZERO_FORBIDDEN", "-0 is refused")
        # nonfinite names are not numbers; Infinity/NaN would fail token rules
        try:
            value = int(token, 10)
        except ValueError as e:
            raise AdmissionError("BAD_NUMBER", f"cannot parse {token}") from e
        if value < I64_MIN or value > U64_MAX:
            raise AdmissionError(
                "INTEGER_OUT_OF_RANGE",
                f"{value} outside [-2^63, 2^64-1]",
                extra={"value": str(value)},
            )
        return value


def admit_raw(raw: bytes) -> Any:
    return RawAdmit(raw).parse()


def first_refusal(raw: bytes) -> dict:
    try:
        value = admit_raw(raw)
        return {"ok": True, "value": value}
    except AdmissionError as e:
        return {"ok": False, "firstRefusal": e.as_dict()}
