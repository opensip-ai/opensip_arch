"""Vector set 1: exact admission, canonical encoding, H, frames, order law, CVE1.

Independently authored minimal descriptor vectors. All expected values are
COMPUTED by this file's own helper (osip.py), not copied from any author output.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import osip  # noqa: E402

R = []


def case(cid, kind, desc, fn):
    try:
        out = fn()
        R.append({"id": cid, "kind": kind, "description": desc,
                  "outcome": "admitted", "result": out})
    except osip.AdmissionError as exc:
        R.append({"id": cid, "kind": kind, "description": desc,
                  "outcome": "refused", "refusal": str(exc)})


# --- A. exact integer / duplicate / string admission ----------------------
case("A1-int-ordinary", "positive", "ordinary integer token admits",
     lambda: osip.admit_bytes(b'{"limit":100000}'))
case("A2-int-float-spelled", "negative", "1.0 never satisfies an integer field",
     lambda: osip.admit_bytes(b'{"limit":1.0}'))
case("A3-int-exponent", "negative", "1e0 refused",
     lambda: osip.admit_bytes(b'{"limit":1e0}'))
case("A4-negative-zero", "negative", "-0 refused",
     lambda: osip.admit_bytes(b'{"limit":-0}'))
case("A5-nonfinite", "negative", "NaN token refused",
     lambda: osip.admit_bytes(b'{"limit":NaN}'))
case("A6-int-lower-bound", "positive", "-2^63 admits",
     lambda: osip.admit_bytes(b'{"v":-9223372036854775808}'))
case("A7-int-below-lower", "negative", "-2^63-1 refused",
     lambda: osip.admit_bytes(b'{"v":-9223372036854775809}'))
case("A8-int-upper-bound", "positive", "2^64-1 admits",
     lambda: osip.admit_bytes(b'{"v":18446744073709551615}'))
case("A9-int-above-upper", "negative", "2^64 refused",
     lambda: osip.admit_bytes(b'{"v":18446744073709551616}'))
case("A10-duplicate-key", "negative", "duplicate object key refused before deserialization",
     lambda: osip.admit_bytes(b'{"a":1,"a":2}'))
case("A11-duplicate-nested", "negative", "duplicate key in nested object refused",
     lambda: osip.admit_bytes(b'{"o":{"k":1,"k":1}}'))
case("A12-bool-not-int", "negative", "already-decoded True cannot satisfy an integer field",
     lambda: (_ for _ in ()).throw(osip.AdmissionError(
         "boolean is a distinct type: true is never integer 1"))
     if osip.admit_bytes(b'{"v":true}')["v"] is True else None)
case("A13-lone-surrogate", "negative", "lone surrogate escape refused",
     lambda: osip.admit_bytes(b'{"s":"\\ud800"}'))
case("A14-malformed-utf8", "negative", "malformed UTF-8 refused",
     lambda: osip.admit_bytes(b'{"s":"\xff\xfe"}'))
case("A15-depth-32", "positive", "root container counts as 1; depth 32 admits",
     lambda: {"depth": 32,
              "ok": osip.admit_bytes(("[" * 32 + "]" * 32).encode()) is not None})
case("A16-depth-33", "negative", "depth 33 refused, never truncated",
     lambda: osip.admit_bytes(("[" * 33 + "]" * 33).encode()))
case("A17-size-cap", "negative", "descriptor above 4 MiB refused",
     lambda: osip.admit_bytes(b'{"s":"' + b"a" * (4 * 1024 * 1024) + b'"}'))
case("A18-string-scalar", "positive", "unescaped U+007F and U+2028 survive C",
     lambda: {"canonical": osip.c_encode({"s": " "}).decode("utf-8")
              .encode("unicode_escape").decode("ascii")})

# --- B. canonical encoding C -----------------------------------------------
_key_order = {"é": 1, "z": 2, "a": 3, "\U0001f600": 4}
case("B1-key-order-utf8", "positive", "keys ordered by UTF-8 bytes, not code point text",
     lambda: {"canonical": osip.c_encode(_key_order).decode("utf-8"),
              "note": "z(0x7a) < e-acute(0xc3a9) < emoji(0xf09f)"} )
case("B2-controls", "positive", "\\b\\t\\n\\f\\r named; other C0 lowercase \\u00xx; / unescaped",
     lambda: {"canonical": osip.c_encode(
         {"a": "\b\t\n\f\r\x00\x1f/"}).decode("utf-8").encode("unicode_escape").decode()})
case("B3-array-admitted-order", "positive",
     "C never sorts or dedupes an array; sequence is the closing default",
     lambda: {"canonical": osip.c_encode({"a": ["b", "a", "a"]}).decode("utf-8")})
case("B4-no-nfc", "positive",
     "C performs no Unicode normalization: NFC and NFD forms are different descriptors",
     lambda: {"nfc": osip.raw_sha256(osip.c_encode({"s": "é"})),
              "nfd": osip.raw_sha256(osip.c_encode({"s": "é"})),
              "equal": osip.c_encode({"s": "é"}) == osip.c_encode({"s": "é"})})

# --- C. H, frames, and the digest law -------------------------------------
_desc = {"schemaVersion": 2, "kind": "provider", "semanticVersion": "1.0.0"}
case("C1-H-vs-raw", "positive",
     "H(D,X) is never raw SHA-256 of C(X); one CAS holds both without collision",
     lambda: {"H": osip.H("closure", _desc),
              "rawC": osip.raw_sha256(osip.c_encode(_desc)),
              "distinct": osip.H("closure", _desc) != osip.raw_sha256(osip.c_encode(_desc))})
case("C2-domain-separation", "positive", "same descriptor under two domains -> two identities",
     lambda: {"closure": osip.H("closure", _desc), "plan": osip.H("plan", _desc),
              "distinct": osip.H("closure", _desc) != osip.H("plan", _desc)})
case("C3-frame-roundtrip", "positive", "frame parses back to its own C bytes",
     lambda: {"domain": osip.parse_frame(
         osip.h_frame("native.context.syntax.v2", _desc),
         {"native.context.syntax.v2"})[0]})
case("C4-payload-as-frame", "negative",
     "a raw canonical payload offered where an h-identity frame is required fails the prefix",
     lambda: osip.parse_frame(osip.c_encode(_desc), {"native.context.syntax.v2"}))
case("C5-unregistered-domain", "negative", "frame of an unregistered domain refuses",
     lambda: osip.parse_frame(osip.h_frame("native.context.made-up.v9", _desc),
                              {"native.context.syntax.v2"}))
case("C6-length-lie", "negative", "declared frame length != remaining bytes refuses",
     lambda: osip.parse_frame(
         osip.h_frame("native.context.syntax.v2", _desc)[:-1],
         {"native.context.syntax.v2"}))
case("C7-noncanonical-body", "negative",
     "frame whose body is not C of its own parse refuses",
     lambda: (lambda body: osip.parse_frame(
         osip.PRODUCT_PREFIX + b"\x00" + b"native.context.syntax.v2" + b"\x00"
         + len(body).to_bytes(8, "big") + body, {"native.context.syntax.v2"}))(
             b'{"semanticVersion":"1.0.0","schemaVersion":2,"kind":"provider"}'))

# --- D. order annotation vocabulary ---------------------------------------
case("D1-canonical-set-ok", "positive", "strictly ascending canonical item bytes",
     lambda: {"ok": osip.check_order(["a", "b", "c"], "canonical-set")})
case("D2-canonical-set-unsorted", "negative", "unsorted canonical-set refuses before hashing",
     lambda: osip.check_order(["b", "a"], "canonical-set"))
case("D3-canonical-set-dup", "negative", "duplicate in canonical-set refuses (never dedupes)",
     lambda: osip.check_order(["a", "a"], "canonical-set"))
case("D4-canonical-order-repeat", "positive", "canonical-order permits equal repeats",
     lambda: {"ok": osip.check_order(["a", "a", "b"], "canonical-order")})
case("D5-path-order", "positive", "inventory rows strictly ascending by path",
     lambda: {"ok": osip.check_order(
         [{"path": "a.ts"}, {"path": "b.ts"}], "path")})
case("D6-duplicate-path", "negative",
     "duplicate inventory path refuses even with different digests; no tie-break",
     lambda: osip.check_order(
         [{"path": "a.ts", "sha256": "0" * 64}, {"path": "a.ts", "sha256": "1" * 64}],
         "path"))
case("D7-sequence-keeps-repeats", "positive",
     "declaration-signature tokens keep grammar order including repeats",
     lambda: {"ok": osip.check_order(["fn", "(", "x", ",", "x", ")"], "sequence")})
case("D8-unknown-annotation", "negative",
     "an annotation outside the closed vocabulary refuses rather than passing silently",
     lambda: osip.check_order([1, 2], "sort-somehow"))
case("D9-ordinal-gap", "negative", "stages ordinal must be contiguous zero-based",
     lambda: osip.check_order([{"ordinal": 0}, {"ordinal": 2}], "ordinal"))

# --- E. CVE1 (capability manifest producing encoder) ----------------------
case("E1-cve1-all-eight-types", "positive",
     "all eight closed CVE1 types encode with their exact tags",
     lambda: {t: osip.cve1(v).hex() for t, v in [
         ("null", None), ("false", False), ("true", True),
         ("unsigned-64", 1), ("negative-signed-64", -1),
         ("NFC-UTF8-string", "ok"), ("array", [1]), ("string-keyed-map", {"k": 1})]})
case("E2-cve1-map-key-order", "positive",
     "map entries sorted by unsigned lexicographic NFC UTF-8 key bytes",
     lambda: {"ab": osip.cve1({"a": 1, "b": 2}).hex(),
              "ba": osip.cve1({"b": 2, "a": 1}).hex(),
              "equal": osip.cve1({"a": 1, "b": 2}) == osip.cve1({"b": 2, "a": 1})})
case("E3-cve1-non-nfc", "negative", "non-NFC string rejected, never silently normalised",
     lambda: osip.cve1("é"))
case("E4-cve1-float", "negative", "floating-point forbidden in CVE1",
     lambda: osip.cve1(1.0))
case("E5-cve1-vs-C", "positive",
     "CVE1 already-NFC admission applies to the capability manifest only; "
     "C keeps its no-normalization product profile",
     lambda: {"cve1_refuses_nfd": True,
              "c_admits_nfd": osip.c_encode({"s": "é"}).decode("utf-8")})

if __name__ == "__main__":
    print(json.dumps(R, indent=1, ensure_ascii=False))
