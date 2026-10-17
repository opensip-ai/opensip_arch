"""Build (or, with --check, verify) D2b-1's CBOR differential corpus (LD-D2B-14).

Every input is decoded by native wire owner trial 07's reference decoder (`tools/wirecodec.py`, read in place) under
each profile, and its outcome recorded: "OK" or the reference's refusal code. The product test replays every case
through `provider_protocol::cbor::decode` and requires the same outcome, so the Rust reader's refusal order and
codes are the reference's, and the NFC predicate agrees with the reference's `unicodedata` over every text here.

The inputs are deterministic: the reference's own decoder probes (`check_reference.py` `wire_examples`), every
initial byte with a few suffixes, a set of seed values at every integer and length boundary, every non-shortest
re-encoding of each boundary, and for each seed its every truncation, three single-bit flips at each of its first 24
and last 4 bytes, and one trailing byte.

Usage: build_cbor_differential.py <arch root> <output json> [--check]
"""
import hashlib
import json
import sys
import unicodedata
from pathlib import Path

TRIAL = "docs/implementation/m1/trials/native-wire-owner-07/subject"
PROFILES = ("ts2-cbor", "rust3-cbor")


def load_reference(arch):
    path = arch / TRIAL / "tools" / "wirecodec.py"
    raw = path.read_bytes()
    namespace = {"__name__": "wirecodec"}
    exec(compile(raw, str(path), "exec"), namespace)
    return namespace, hashlib.sha256(raw).hexdigest()


def seeds():
    texts = [
        "", "a", "b", "aa", "ab", "é", "é", "Å", "Å", "Å", "ﬁ", "가",
        "가", "क़", "ẛ̣", "x" * 23, "y" * 24, "z" * 255, "w" * 256,
    ]
    ints = [0, 1, 23, 24, 255, 256, 65535, 65536, (1 << 32) - 1, 1 << 32, (1 << 64) - 1]
    negs = [-1, -24, -25, -256, -257, -(1 << 32), -(1 << 63)]
    out = [None, True, False, b"", b"\x00", b"abc", bytes(24), [], {}]
    out += texts + ints + negs
    out += [
        [1, [2, [3, [4, [5]]]]],
        {"a": 1, "b": [True, None], "aa": {"x": b"\x01"}},
        {"executionId": None, "analysisOrdinal": 0, "reason": "user-interrupt"},
        {"protocolMajor": 3, "direction": "host-to-worker", "sequence": 0, "frameType": "SnapshotFileChunk",
         "payload": {"snapshotId": "s", "path": "src/a.ts", "chunkIndex": 0, "byteOffset": 0, "bytes": b"abc"}},
        [-1, {"k": -(1 << 63)}],
        {"é": 1, "e": 2},
        list(range(24)),
    ]
    return out


def non_shortest(n, major):
    """Every wider head for argument n, which the reference refuses."""
    out = []
    for ai, size in ((24, 1), (25, 2), (26, 4), (27, 8)):
        if n < 1 << (8 * size):
            out.append(bytes([major << 5 | ai]) + n.to_bytes(size, "big"))
    return out[1:] if n >= 24 else out


def inputs(W, probes):
    seen, ordered = set(), []

    def add(label, data):
        data = bytes(data)
        if data not in seen:
            seen.add(data)
            ordered.append((label, data))

    for label, data in probes:
        add(label, data)
    for ib in range(256):
        for suffix in (b"", b"\x00", b"\x01" * 9, b"\xff", b"\x61\x61", b"\x80\x00"):
            add("initial-byte", bytes([ib]) + suffix)
    for n in (0, 1, 23, 24, 255, 256, 65535, 65536, (1 << 32) - 1, 1 << 32, (1 << 64) - 1):
        for major in (0, 1, 2, 3, 4, 5):
            for head in non_shortest(n, major):
                add("non-shortest", head)
    for value in seeds():
        enc = W["encode"](value)
        add("seed", enc)
        add("seed-trailing", enc + b"\x00")
        for cut in range(len(enc)):
            add("seed-truncated", enc[:cut])
        for i in [i for i in range(len(enc)) if i < 24 or i >= len(enc) - 4]:
            for bit in (0x01, 0x20, 0x80):
                flipped = bytearray(enc)
                flipped[i] ^= bit
                add("seed-bit-flip", flipped)
    return ordered


def probes(W):
    enc = W["encode"]
    neg = enc({"snapshotId": "s", "path": "src/a.ts", "chunkIndex": -1, "byteOffset": 0, "bytes": b"abc"})
    return [
        ("wire-rust3-negative-int-forbidden", neg),
        ("wire-non-shortest", b"\x18\x05"),
        ("wire-map-order", b"\xa2" + enc("b") + enc(1) + enc("a") + enc(1)),
        ("wire-length-first-map-order", b"\xa2" + enc("aa") + enc(1) + enc("b") + enc(1)),
        ("wire-duplicate-key", b"\xa2" + enc("a") + enc(1) + enc("a") + enc(1)),
        ("wire-float", b"\xf9\x00\x00"),
        ("wire-tag", b"\xc0\x60"),
        ("wire-indefinite", b"\x5f\xff"),
        ("wire-non-nfc", enc("é")),
        ("non-text-key", b"\xa1\x01\x01"),
        ("int-range", b"\x3b\x80\x00\x00\x00\x00\x00\x00\x00"),
        ("invalid-utf8", b"\x62\xc3\x28"),
        ("empty", b""),
    ]


def build(arch):
    W, digest = load_reference(arch)
    cases = []
    for label, data in inputs(W, probes(W)):
        for profile in PROFILES:
            try:
                W["decode"](data, profile)
                outcome = "OK"
            except W["Refuse"] as exc:
                outcome = exc.code
            cases.append({"label": label, "profile": profile, "input": data.hex(), "outcome": outcome})
    corpus = {
        "artifact": "opensip.d2b.cbor-differential",
        "version": 1,
        "reference": {"path": TRIAL + "/tools/wirecodec.py", "sha256": digest},
        "unicodeVersion": unicodedata.unidata_version,
        "cases": cases,
    }
    rows = ",\n".join(json.dumps(c, sort_keys=True, ensure_ascii=True, separators=(",", ":")) for c in cases)
    head = json.dumps(dict(corpus, cases=[]), sort_keys=True, ensure_ascii=True, separators=(",", ":"))
    return (head.replace('"cases":[]', '"cases":[\n' + rows + "\n]") + "\n").encode()


def main(argv):
    arch, out = Path(argv[1]), Path(argv[2])
    data = build(arch)
    if "--check" in argv[3:]:
        if out.read_bytes() != data:
            print("cbor differential corpus is stale")
            return 1
        print("cbor differential corpus current")
        return 0
    out.write_bytes(data)
    print(out, len(data), hashlib.sha256(data).hexdigest())
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
