"""Provider wire deterministic CBOR (source44): the inherited canonicalCbor of delivery.v2 (typescriptSemanticSubstrate.providerProtocol.wireSchema.
canonicalCbor) and rust-provider-protocol.v2 (canonicalCbor), used for handshake limit byte equality and the typescript-semantic FactBatchV1
batchCommitment over the wire FactCandidateV1 array.

Data model (both artifacts): null, false, true, uint64, NFC UTF-8 text, byte string, definite array, definite text-keyed map. delivery.v2 also lists
negative-int64; rust-provider-protocol.v2 forbids negative integers (the `allow_negative` switch). Floats, tags, indefinite lengths, non-shortest arguments,
duplicate and non-text keys and non-NFC text refuse.

Map order:
  - delivery.v2: ascending lexicographic order of each key's deterministic-CBOR encoded bytes;
  - rust-provider-protocol.v2: byte length of the encoded key first, then lexicographic.
For text keys the two coincide (native/provider-handshake.schemas.v1.json#/x-opensip-wire-law/candidateCborProjection). `encode` implements the delivery
rule; `same_order_both_rules` measures the coincidence on every map it encodes.

The relation payload profile (fact-plane canonicalPayloadEncoding, which forbids byte strings) stays in ref/factbatch.py.
"""
import unicodedata


class WireCborError(Exception):
    def __init__(self, cls):
        super().__init__(cls)
        self.cls = cls


def _head(major, n, out):
    if n < 24:
        out.append((major << 5) | n)
    elif n < 0x100:
        out += bytes([(major << 5) | 24, n])
    elif n < 0x10000:
        out.append((major << 5) | 25)
        out += n.to_bytes(2, "big")
    elif n < 0x100000000:
        out.append((major << 5) | 26)
        out += n.to_bytes(4, "big")
    elif n < 0x10000000000000000:
        out.append((major << 5) | 27)
        out += n.to_bytes(8, "big")
    else:
        raise WireCborError("uint64-range")


ORDER_CHECKS = {"maps": 0, "rulesDisagreed": 0}


def encode(value, allow_negative=False):
    out = bytearray()
    _enc(value, out, allow_negative)
    return bytes(out)


def _enc(v, out, allow_negative):
    if v is None:
        out.append(0xf6)
    elif v is False:
        out.append(0xf4)
    elif v is True:
        out.append(0xf5)
    elif type(v) is int:
        if v < 0:
            if not allow_negative or v < -(2 ** 63):
                raise WireCborError("negative-integer")
            _head(1, -1 - v, out)
        else:
            _head(0, v, out)
    elif type(v) is float:
        raise WireCborError("float")
    elif type(v) in (bytes, bytearray):
        _head(2, len(v), out)
        out += bytes(v)
    elif type(v) is str:
        try:
            b = v.encode("utf-8")
        except UnicodeEncodeError:
            raise WireCborError("invalid-utf8")
        if not unicodedata.is_normalized("NFC", v):
            raise WireCborError("non-nfc-text")
        _head(3, len(b), out)
        out += b
    elif type(v) is list:
        _head(4, len(v), out)
        for x in v:
            _enc(x, out, allow_negative)
    elif type(v) is dict:
        items = []
        for k, x in v.items():
            if type(k) is not str:
                raise WireCborError("non-text-key")
            items.append((encode(k), x))
        bytewise = sorted(items, key=lambda t: t[0])
        length_first = sorted(items, key=lambda t: (len(t[0]), t[0]))
        ORDER_CHECKS["maps"] += 1
        if [k for k, _ in bytewise] != [k for k, _ in length_first]:
            ORDER_CHECKS["rulesDisagreed"] += 1
        _head(5, len(items), out)
        for kb, x in bytewise:
            out += kb
            _enc(x, out, allow_negative)
    else:
        raise WireCborError("unsupported-type:" + type(v).__name__)


def same_order_both_rules():
    return dict(ORDER_CHECKS, coincide=ORDER_CHECKS["rulesDisagreed"] == 0)
