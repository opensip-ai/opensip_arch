"""Foundation CAN bytes for harness records (Q0 r13, ground rules)."""
import hashlib
import json

MAX_BYTES = 4 * 1024 * 1024


class Refusal(ValueError):
    """An input failed a named harness admission check."""


def typed(value, depth=0):
    if type(value) in (dict, list) and depth >= 32:
        raise Refusal("DEPTH_LIMIT")
    if value is None or type(value) is bool:
        return
    if type(value) is int:
        if not -(2**63) <= value <= 2**64 - 1:
            raise Refusal("INTEGER_RANGE")
    elif type(value) is str:
        try:
            value.encode("utf-8", "strict")
        except UnicodeError as exc:
            raise Refusal("UNICODE_SCALAR_REQUIRED") from exc
    elif type(value) is list:
        for child in value:
            typed(child, depth + 1)
    elif type(value) is dict:
        for key, child in value.items():
            if type(key) is not str:
                raise Refusal("STRING_KEY_REQUIRED")
            typed(key, depth + 1)
            typed(child, depth + 1)
    else:
        raise Refusal("EXACT_JSON_TYPE_REQUIRED")


def canonical(value):
    typed(value)
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(",", ":"), allow_nan=False).encode("utf-8")
    if len(raw) > MAX_BYTES:
        raise Refusal("BYTE_LIMIT")
    return raw


def parse(raw):
    if type(raw) is not bytes or len(raw) > MAX_BYTES:
        raise Refusal("BYTE_LIMIT_OR_TYPE")

    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise Refusal("DUPLICATE_KEY")
            out[key] = value
        return out

    def integer(text):
        if text == "-0":
            raise Refusal("NEGATIVE_ZERO")
        return int(text)

    def forbidden(_):
        raise Refusal("FLOAT_OR_NONFINITE_FORBIDDEN")

    try:
        value = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=pairs,
                           parse_int=integer, parse_float=forbidden,
                           parse_constant=forbidden)
        typed(value)
        return value
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise Refusal(str(exc)) from exc


def digest(value):
    return hashlib.sha256(canonical(value)).hexdigest()


def sha256(raw):
    return hashlib.sha256(raw).hexdigest()


def pin(value):
    return type(value) is str and len(value) == 64 and all(c in "0123456789abcdef" for c in value)
