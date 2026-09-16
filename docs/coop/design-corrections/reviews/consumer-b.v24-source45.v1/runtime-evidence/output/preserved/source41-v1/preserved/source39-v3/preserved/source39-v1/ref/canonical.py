"""Independent reconstruction of the product canonical encoder C, the framed identity H,
and raw-input lexical admission.

Normative source: docs/v2/contracts/product-v1/identity-and-evidence.md section 3 and
admission-and-qualification.md section 1 (kit bytes only). No author code consulted.
"""
import hashlib
import json

PRODUCT_TAG = b"opensip.product.v1"
MAX_DESCRIPTOR_BYTES = 4 * 1024 * 1024
MAX_DEPTH = 32
INT_MIN = -(2 ** 63)
INT_MAX = 2 ** 64 - 1


class AdmissionError(Exception):
    """A typed refusal. `boundary` names the first refusal boundary observed."""

    def __init__(self, boundary, detail=""):
        super().__init__(f"{boundary}:{detail}" if detail else boundary)
        self.boundary = boundary
        self.detail = detail


# ---------------------------------------------------------------- raw lexical admission

def _reject_float(token):
    raise AdmissionError("LEX_FLOAT_OR_EXPONENT", token)


def _reject_constant(token):
    raise AdmissionError("LEX_NONFINITE", token)


def _parse_int(token):
    if token == "-0":
        raise AdmissionError("LEX_NEGATIVE_ZERO", token)
    value = int(token)
    if value < INT_MIN or value > INT_MAX:
        raise AdmissionError("LEX_INTEGER_RANGE", token)
    return value


def _pairs(pairs):
    seen = set()
    out = {}
    for key, value in pairs:
        if key in seen:
            raise AdmissionError("LEX_DUPLICATE_KEY", key)
        seen.add(key)
        out[key] = value
    return out


def _scan_scalars(value, depth):
    """Post-parse walk: lone surrogates (non-scalar Unicode) and container depth."""
    if isinstance(value, dict):
        if depth > MAX_DEPTH:
            raise AdmissionError("LEX_DEPTH", str(depth))
        for k, v in value.items():
            _check_scalar_string(k)
            _scan_scalars(v, depth + 1)
    elif isinstance(value, list):
        if depth > MAX_DEPTH:
            raise AdmissionError("LEX_DEPTH", str(depth))
        for v in value:
            _scan_scalars(v, depth + 1)
    elif isinstance(value, str):
        _check_scalar_string(value)


def _check_scalar_string(s):
    for ch in s:
        if 0xD800 <= ord(ch) <= 0xDFFF:
            raise AdmissionError("LEX_NON_SCALAR_UNICODE", "U+%04X" % ord(ch))


def parse_raw(raw_bytes):
    """Admit raw descriptor bytes BEFORE any decoded value is used.

    Order of boundaries (first refusal wins): size, UTF-8, JSON lexical tokens
    (float/exponent, nonfinite, -0, integer range, duplicate key), scalar Unicode, depth.
    """
    if not isinstance(raw_bytes, (bytes, bytearray)):
        raise AdmissionError("LEX_NOT_BYTES")
    if len(raw_bytes) > MAX_DESCRIPTOR_BYTES:
        raise AdmissionError("LEX_DESCRIPTOR_TOO_LARGE", str(len(raw_bytes)))
    try:
        text = bytes(raw_bytes).decode("utf-8", errors="strict")
    except UnicodeDecodeError as exc:
        raise AdmissionError("LEX_MALFORMED_UTF8", str(exc.start))
    if text.startswith("﻿"):
        raise AdmissionError("LEX_BOM")
    try:
        value = json.loads(text, object_pairs_hook=_pairs, parse_float=_reject_float,
                           parse_int=_parse_int, parse_constant=_reject_constant)
    except AdmissionError:
        raise
    except (ValueError, RecursionError) as exc:
        raise AdmissionError("LEX_SYNTAX", type(exc).__name__)
    _scan_scalars(value, 1)
    return value


# ---------------------------------------------------------------- already-parsed typing

def check_typed(value, depth=1):
    """Admission of an already-decoded object (a separate boundary from raw lexical admission).
    Refuses Python float, out-of-range int, non-string keys, lone surrogates, depth."""
    if value is None or value is True or value is False:
        return
    if type(value) is int:
        if value < INT_MIN or value > INT_MAX:
            raise AdmissionError("TYPED_INTEGER_RANGE", str(value))
        return
    if type(value) is float:
        raise AdmissionError("TYPED_FLOAT", repr(value))
    if type(value) is str:
        _check_scalar_string(value)
        return
    if type(value) is list:
        if depth > MAX_DEPTH:
            raise AdmissionError("TYPED_DEPTH", str(depth))
        for v in value:
            check_typed(v, depth + 1)
        return
    if type(value) is dict:
        if depth > MAX_DEPTH:
            raise AdmissionError("TYPED_DEPTH", str(depth))
        for k, v in value.items():
            if type(k) is not str:
                raise AdmissionError("TYPED_NON_STRING_KEY", repr(k))
            _check_scalar_string(k)
            check_typed(v, depth + 1)
        return
    raise AdmissionError("TYPED_UNSUPPORTED_TYPE", type(value).__name__)


# ---------------------------------------------------------------- C

_ESC = {'"': '\\"', '\\': '\\\\', '\b': '\\b', '\t': '\\t', '\n': '\\n', '\f': '\\f', '\r': '\\r'}


def _enc_str(s):
    out = ['"']
    for ch in s:
        if ch in _ESC:
            out.append(_ESC[ch])
        elif ord(ch) < 0x20:
            out.append('\\u%04x' % ord(ch))
        else:
            out.append(ch)
    out.append('"')
    return ''.join(out)


def _enc(value, out):
    if value is None:
        out.append('null')
    elif value is True:
        out.append('true')
    elif value is False:
        out.append('false')
    elif type(value) is int:
        out.append(str(value))
    elif type(value) is str:
        out.append(_enc_str(value))
    elif type(value) is list:
        out.append('[')
        for i, v in enumerate(value):
            if i:
                out.append(',')
            _enc(v, out)
        out.append(']')
    elif type(value) is dict:
        out.append('{')
        keys = sorted(value.keys(), key=lambda k: k.encode('utf-8'))
        for i, k in enumerate(keys):
            if i:
                out.append(',')
            out.append(_enc_str(k))
            out.append(':')
            _enc(value[k], out)
        out.append('}')
    else:
        raise AdmissionError("C_UNSUPPORTED_TYPE", type(value).__name__)


def C(value):
    check_typed(value)
    out = []
    _enc(value, out)
    data = ''.join(out).encode('utf-8')
    if len(data) > MAX_DESCRIPTOR_BYTES:
        raise AdmissionError("C_DESCRIPTOR_TOO_LARGE", str(len(data)))
    return data


def sha256_hex(data):
    return hashlib.sha256(data).hexdigest()


def raw_digest(value):
    """raw SHA256(C(value)) -- canonical-record representation."""
    return sha256_hex(C(value))


# ---------------------------------------------------------------- H and frames

def frame(domain, value):
    body = C(value)
    return PRODUCT_TAG + b"\x00" + domain.encode('ascii') + b"\x00" + len(body).to_bytes(8, 'big') + body


def H(domain, value):
    return sha256_hex(frame(domain, value))


PREFIX = {
    "snapshot": "snapshot2", "closure": "closure2", "import": "import2", "plan": "plan2",
    "subject-scope": "scope2", "fact": "fact2", "coverage": "coverage2", "view": "view2",
    "execution-plan": "exec-plan2", "finding-fingerprint": "finding-key2",
    "evaluation-subject": "subject3", "finding": "finding3", "proof-bundle": "proof3",
    "semantic-evidence": "evidence3", "evaluation-seal": "seal3", "run": "run3",
    "cache-key": "cache2", "regeneration-key": "regen2", "policy-derivation": "policy-derivation3",
}


def identifier(domain, value):
    return PREFIX[domain] + ":" + H(domain, value)


def parse_frame(frame_bytes, allowed_domains):
    """Exact frame admission (identity-and-evidence section 3, closing digest law)."""
    fb = bytes(frame_bytes)
    head = PRODUCT_TAG + b"\x00"
    if not fb.startswith(head):
        raise AdmissionError("FRAME_PREFIX")
    rest = fb[len(head):]
    nul = rest.find(b"\x00")
    if nul < 0:
        raise AdmissionError("FRAME_DOMAIN_TERMINATOR")
    try:
        domain = rest[:nul].decode('ascii')
    except UnicodeDecodeError:
        raise AdmissionError("FRAME_DOMAIN_ASCII")
    if domain not in allowed_domains:
        raise AdmissionError("FRAME_DOMAIN_UNREGISTERED", domain)
    rest = rest[nul + 1:]
    if len(rest) < 8:
        raise AdmissionError("FRAME_LENGTH_FIELD")
    declared = int.from_bytes(rest[:8], 'big')
    body = rest[8:]
    if declared != len(body):
        raise AdmissionError("FRAME_LENGTH_MISMATCH", f"{declared}!={len(body)}")
    value = parse_raw(body)
    if C(value) != body:
        raise AdmissionError("FRAME_NOT_CANONICAL")
    return domain, value


def sha256_text(hexdigest):
    return "sha256:" + hexdigest


def strip_prefix(ident):
    return ident.split(":", 1)[1]
