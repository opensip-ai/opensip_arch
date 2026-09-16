"""CVE1 encoder/decoder and CapabilityManifestV1 admission (CAP-MANIFEST-ID-V1).

Normative sources (kit bytes only):
- docs/coop/artifacts/resolved-inputs.v2.json#/planIdContract/canonicalValueEncoding (CVE1)
- docs/coop/design-corrections/native/capability-manifest-domains.v2.json (effective registry,
  gate order, closed record shapes, declared OPEN positions, traversal order, decoder bounds)
- docs/coop/artifacts/delivery.v4.json#/..../capabilityManifestIdentity (recipe; DL-ORD rulings)
- identity-and-evidence.md section 3 (selection of the successor registry by name)
"""
import hashlib
import json
import unicodedata

KIT = '/private/tmp/opensip-design-corrections/consumer-b.v24-source39.v1/subject/docs/'
REGISTRY_PATH = KIT + 'coop/design-corrections/native/capability-manifest-domains.v2.json'
DOMAIN_LABEL = b"opensip.capability-manifest.v1"
U64_MAX = 2 ** 64 - 1
I64_MIN = -(2 ** 63)


class CVE1Error(Exception):
    def __init__(self, code, detail=""):
        super().__init__(f"{code}:{detail}" if detail else code)
        self.code = code
        self.detail = detail


def _nfc(s):
    return unicodedata.is_normalized('NFC', s)


def encode(value, _depth=0, max_nesting=64):
    if _depth > max_nesting:
        raise CVE1Error("CVE1_NESTING")
    if value is None:
        return b"\x00"
    if value is False:
        return b"\x01"
    if value is True:
        return b"\x02"
    if type(value) is int:
        if 0 <= value <= U64_MAX:
            return b"\x03" + value.to_bytes(8, 'big')
        if I64_MIN <= value < 0:
            return b"\x07" + value.to_bytes(8, 'big', signed=True)
        raise CVE1Error("CVE1_INTEGER_RANGE", str(value))
    if type(value) is float:
        raise CVE1Error("CVE1_FLOAT_FORBIDDEN", repr(value))
    if type(value) in (bytes, bytearray):
        raise CVE1Error("CVE1_BYTES_FORBIDDEN")
    if type(value) is str:
        if not _nfc(value):
            raise CVE1Error("CVE1_NON_NFC", value)
        b = value.encode('utf-8')
        return b"\x04" + len(b).to_bytes(4, 'big') + b
    if type(value) is list:
        return b"\x05" + len(value).to_bytes(4, 'big') + b''.join(encode(v, _depth + 1) for v in value)
    if type(value) is dict:
        keys = list(value.keys())
        for k in keys:
            if type(k) is not str:
                raise CVE1Error("CVE1_MAP_KEY_NOT_STRING", repr(k))
            if not _nfc(k):
                raise CVE1Error("CVE1_NON_NFC", k)
        encoded_keys = [k.encode('utf-8') for k in keys]
        if len(set(encoded_keys)) != len(encoded_keys):
            raise CVE1Error("CVE1_DUPLICATE_KEY")
        order = sorted(range(len(keys)), key=lambda i: encoded_keys[i])
        parts = [b"\x06", len(keys).to_bytes(4, 'big')]
        for i in order:
            parts.append(encode(keys[i], _depth + 1))
            parts.append(encode(value[keys[i]], _depth + 1))
        return b''.join(parts)
    raise CVE1Error("CVE1_UNSUPPORTED_TYPE", type(value).__name__)


def decode(data, max_nesting=64, max_items=1048576):
    data = bytes(data)
    pos = 0

    def need(n):
        nonlocal pos
        if pos + n > len(data):
            raise CVE1Error("CVE1_TRUNCATED", str(pos))
        chunk = data[pos:pos + n]
        pos += n
        return chunk

    def item(depth):
        if depth > max_nesting:
            raise CVE1Error("CVE1_NESTING")
        tag = need(1)[0]
        if tag == 0x00:
            return None
        if tag == 0x01:
            return False
        if tag == 0x02:
            return True
        if tag == 0x03:
            return int.from_bytes(need(8), 'big')
        if tag == 0x07:
            v = int.from_bytes(need(8), 'big', signed=True)
            if v >= 0:
                raise CVE1Error("CVE1_NONCANONICAL_NEGATIVE_TAG", str(v))
            return v
        if tag == 0x04:
            n = int.from_bytes(need(4), 'big')
            raw = need(n)
            try:
                s = raw.decode('utf-8')
            except UnicodeDecodeError:
                raise CVE1Error("CVE1_MALFORMED_UTF8")
            if not _nfc(s):
                raise CVE1Error("CVE1_NON_NFC", s)
            return s
        if tag == 0x05:
            n = int.from_bytes(need(4), 'big')
            if n > max_items:
                raise CVE1Error("CVE1_TOO_MANY_ITEMS", str(n))
            return [item(depth + 1) for _ in range(n)]
        if tag == 0x06:
            n = int.from_bytes(need(4), 'big')
            if n > max_items:
                raise CVE1Error("CVE1_TOO_MANY_ITEMS", str(n))
            out = {}
            prev = None
            for _ in range(n):
                k = item(depth + 1)
                if type(k) is not str:
                    raise CVE1Error("CVE1_MAP_KEY_NOT_STRING")
                kb = k.encode('utf-8')
                if prev is not None and kb == prev:
                    raise CVE1Error("CVE1_DUPLICATE_KEY", k)
                if prev is not None and kb < prev:
                    raise CVE1Error("CVE1_UNSORTED_MAP_KEYS", k)
                prev = kb
                out[k] = item(depth + 1)
            return out
        raise CVE1Error("CVE1_UNKNOWN_TAG", "%02x" % tag)

    value = item(0)
    if pos != len(data):
        raise CVE1Error("CVE1_TRAILING_BYTES", str(len(data) - pos))
    return value


def capability_manifest_id(committed_bytes):
    return hashlib.sha256(DOMAIN_LABEL + b"\x00" + bytes(committed_bytes)).hexdigest()


# ---------------------------------------------------------------- admission gates

def load_registry():
    with open(REGISTRY_PATH, 'rb') as fh:
        return json.loads(fh.read())


def _u8(s):
    return s.encode('utf-8')


class CapabilityAdmission:
    """Runs ADM-TYPE, ADM-CLOSED, ADM-DOMAIN, ADM-ORDER in the registry's declared gateOrder.

    The first gate with any violation is the refusal boundary. Later gates are MASKED (not
    part of the decision); where structurally possible they are also run in hypothetical mode
    so a vector can record which later violations the first refusal masks.
    """

    def __init__(self, registry=None):
        self.reg = registry or load_registry()
        regs = self.reg['registries']
        self.relations = set(regs['RELATION-DOMAIN-V2']['members'])
        self.ladders = regs['RELATION-LADDER-DOMAIN-V2']['ladders']
        self.platforms = set(regs['PLATFORM-ID-DOMAIN-V1']['members'])
        self.deficiencies = set(regs['DEFICIENCY-DOMAIN-V1']['members'])
        self.coverage_states = set(regs['COVERAGE-STATE-DOMAIN-V1']['members'])
        shapes = self.reg['recordShape']
        self.keysets = {n: set(shapes[n]['requiredKeys']) for n in
                        ('CapabilityManifestV1', 'ProviderCapability', 'AbsentCapability')}
        self.gate_order = self.reg['gateOrder']

    # ADM-TYPE: exact JSON type for every declared scalar and container that is present.
    def gate_type(self, m):
        v = []

        def s(path, x):
            if type(x) is not str:
                v.append(f"{path}:expected-string:{type(x).__name__}")

        if type(m) is not dict:
            return [f"$:expected-object:{type(m).__name__}"]
        if 'schemaVersion' in m and type(m['schemaVersion']) is not int:
            v.append(f"$.schemaVersion:expected-integer:{type(m['schemaVersion']).__name__}")
        if 'profile' in m:
            s('$.profile', m['profile'])
        for coll, rec in (('providers', 'provider'), ('coverageForAbsent', 'absent')):
            if coll not in m:
                continue
            if type(m[coll]) is not list:
                v.append(f"$.{coll}:expected-array:{type(m[coll]).__name__}")
                continue
            for i, r in enumerate(m[coll]):
                p = f"$.{coll}[{i}]"
                if type(r) is not dict:
                    v.append(f"{p}:expected-object:{type(r).__name__}")
                    continue
                strs = (['providerId', 'language', 'providerVersionSource', 'toolchainIdentitySource']
                        if rec == 'provider' else ['providerId', 'language', 'coverageState', 'deficiency'])
                for k in strs:
                    if k in r:
                        s(f"{p}.{k}", r[k])
                if rec == 'provider':
                    if 'relations' in r:
                        if type(r['relations']) is not dict:
                            v.append(f"{p}.relations:expected-object:{type(r['relations']).__name__}")
                        else:
                            for rk, rv in r['relations'].items():
                                s(f"{p}.relations[{rk}]", rv)
                    if 'platformIds' in r:
                        if type(r['platformIds']) is not list:
                            v.append(f"{p}.platformIds:expected-array")
                        else:
                            for j, x in enumerate(r['platformIds']):
                                s(f"{p}.platformIds[{j}]", x)
                else:
                    if 'relationIds' in r:
                        if type(r['relationIds']) is not list:
                            v.append(f"{p}.relationIds:expected-array")
                        else:
                            for j, x in enumerate(r['relationIds']):
                                s(f"{p}.relationIds[{j}]", x)
        return v

    # ADM-CLOSED: every reachable RECORD carries exactly its key set; MAP is not a record.
    def gate_closed(self, m):
        v = []
        if type(m) is not dict:
            return ["$:not-a-record"]

        def check(path, rec, name):
            keys = set(rec.keys())
            want = self.keysets[name]
            for k in sorted(want - keys):
                v.append(f"{path}:missing-key:{k}")
            for k in sorted(keys - want):
                v.append(f"{path}:undeclared-key:{k}")

        check('$', m, 'CapabilityManifestV1')
        for i, r in enumerate(m.get('providers', []) if type(m.get('providers')) is list else []):
            if type(r) is dict:
                check(f"$.providers[{i}]", r, 'ProviderCapability')
        for i, r in enumerate(m.get('coverageForAbsent', []) if type(m.get('coverageForAbsent')) is list else []):
            if type(r) is dict:
                check(f"$.coverageForAbsent[{i}]", r, 'AbsentCapability')
        return v

    # ADM-DOMAIN: bound scalars are registry members by exact NFC UTF-8 bytes.
    def gate_domain(self, m):
        v = []
        for i, r in enumerate(m.get('providers', []) if isinstance(m, dict) and type(m.get('providers')) is list else []):
            if type(r) is not dict:
                continue
            rel = r.get('relations')
            if type(rel) is dict:
                for rk, rv in rel.items():
                    if rk not in self.relations:
                        v.append(f"$.providers[{i}].relations:key-not-in-RELATION-DOMAIN-V2:{rk}")
                    elif rv not in self.ladders.get(rk, []):
                        v.append(f"$.providers[{i}].relations[{rk}]:rung-not-in-ladder:{rv}")
            pl = r.get('platformIds')
            if type(pl) is list:
                for j, x in enumerate(pl):
                    if x not in self.platforms:
                        v.append(f"$.providers[{i}].platformIds[{j}]:not-in-PLATFORM-ID-DOMAIN-V1:{x}")
        for i, r in enumerate(m.get('coverageForAbsent', []) if isinstance(m, dict) and type(m.get('coverageForAbsent')) is list else []):
            if type(r) is not dict:
                continue
            ri = r.get('relationIds')
            if type(ri) is list:
                for j, x in enumerate(ri):
                    if x not in self.relations:
                        v.append(f"$.coverageForAbsent[{i}].relationIds[{j}]:not-in-RELATION-DOMAIN-V2:{x}")
            if 'coverageState' in r and r['coverageState'] not in self.coverage_states:
                v.append(f"$.coverageForAbsent[{i}].coverageState:not-in-COVERAGE-STATE-DOMAIN-V1:{r['coverageState']}")
            if 'deficiency' in r and r['deficiency'] not in self.deficiencies:
                v.append(f"$.coverageForAbsent[{i}].deficiency:not-in-DEFICIENCY-DOMAIN-V1:{r['deficiency']}")
        return v

    # ADM-ORDER: strict ascending unique by NFC UTF-8 bytes, declared traversal order.
    def gate_order_check(self, m):
        v = []
        if not isinstance(m, dict):
            return v

        def strict(path, keys):
            for j in range(1, len(keys)):
                a, b = _u8(keys[j - 1]), _u8(keys[j])
                if a == b:
                    v.append(f"{path}:duplicate-at-{j}:{keys[j]}")
                elif a > b:
                    v.append(f"{path}:not-ascending-at-{j}:{keys[j]}")

        provs = m.get('providers') if type(m.get('providers')) is list else []
        absent = m.get('coverageForAbsent') if type(m.get('coverageForAbsent')) is list else []
        for i, r in enumerate(provs):
            if type(r) is dict and type(r.get('platformIds')) is list:
                strict(f"$.providers[{i}].platformIds", [x for x in r['platformIds'] if type(x) is str])
        for i, r in enumerate(absent):
            if type(r) is dict and type(r.get('relationIds')) is list:
                strict(f"$.coverageForAbsent[{i}].relationIds", [x for x in r['relationIds'] if type(x) is str])
        strict("$.providers", [r.get('providerId') for r in provs if type(r) is dict and type(r.get('providerId')) is str])
        strict("$.coverageForAbsent", [r.get('providerId') for r in absent if type(r) is dict and type(r.get('providerId')) is str])
        return v

    def admit(self, manifest):
        gates = {'ADM-TYPE': self.gate_type, 'ADM-CLOSED': self.gate_closed,
                 'ADM-DOMAIN': self.gate_domain, 'ADM-ORDER': self.gate_order_check}
        results = {}
        first = None
        for g in self.gate_order:
            try:
                viol = gates[g](manifest)
            except Exception as exc:  # hypothetical evaluation of a masked gate over a malformed value
                viol = [f"not-evaluable:{type(exc).__name__}"]
            results[g] = viol
            if viol and first is None:
                first = g
        if first is None:
            try:
                committed = encode(manifest)
            except CVE1Error as exc:
                return {"result": "REFUSE", "firstRefusal": "CVE1-ENCODE", "violations": [exc.code],
                        "maskedLater": {}, "gateResults": results}
            decoded = decode(committed)
            if encode(decoded) != committed:
                raise AssertionError("CVE1 round-trip not byte-stable")
            return {"result": "ADMIT", "committedBytesHex": committed.hex(), "byteLength": len(committed),
                    "committedBytesSha256": hashlib.sha256(committed).hexdigest(),
                    "capabilityManifestId": capability_manifest_id(committed), "gateResults": results}
        idx = self.gate_order.index(first)
        masked = {g: results[g] for g in self.gate_order[idx + 1:] if results[g]}
        detail = {"result": "REFUSE", "firstRefusal": first, "violations": results[first],
                  "maskedLater": masked, "masksLaterHypothesizedCheck": bool(masked), "gateResults": results}
        if first == 'ADM-ORDER':
            detail["domainReasonCode"] = "RELEASE.CAPABILITY_MANIFEST_NOT_CANONICAL"
        return detail
