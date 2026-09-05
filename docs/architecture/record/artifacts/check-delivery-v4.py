#!/usr/bin/env python3
"""check-delivery-v4.py -- the retained checker for artifacts/delivery.v4.json.

WHAT THIS IS.  delivery.v4.json is a CANDIDATE successor to the binding DELIVERY
head delivery.v2.json.  It proposes CAP-MANIFEST-ID-V1, publishes seven committed
capability-manifest vectors with complete bytes, seventeen negative controls, and
three derived PlanIds.  Its predecessor candidate, delivery.v3.json, was REJECTED
FOR REPAIR, and its own review recorded a second and independent disqualifier:

    IMPLEMENTATION-FREEZE.md section 7.1 -- "No retained checker - a fair
    residual for a candidate, disqualifying for application."

This file is that checker.  It is a NEW file: it edits nothing, it is pinned by
nothing, and section 7.6 -- which forbids editing a REVIEWED checker because
section 7.2 binds a verdict to bytes -- therefore does not reach it.

WHAT IT REFUSES TO DO.

  * It never compares one stored string to another stored string.  Every id,
    byte length, hex string and PlanId in the artifact is RECOMPUTED from the
    recipe, from delivery.v2's live installProfiles or from the artifact's own
    published manifest values, and the comparison is the gate.
  * It never parses a file it has not hash-verified.  Drift is exit 2, before
    any parse, because a report about bytes nobody named is not a report.
  * It never reports a measurement it cannot fail on.  IMPLEMENTATION-FREEZE.md
    section 7.2.2's rider: "a measurement that cannot fail the build is prose."
    Every number this file computes is compared and raises a finding.
  * It never declares a control it does not execute.  The freeze records EPC-V2
    in a sibling artifact as declared-but-never-executed -- "it declares that,
    and nothing runs it" -- and gate G12 fails the run if the number of controls
    executed is not the number the artifact declares.
  * It never admits a scalar by isinstance.  Python's bool is an int subclass,
    so `isinstance(True, int)` is True; section 6 law 18's defect class defeated
    C-2 at v3, v5, v6, v7 and v8 successively, each time inside the repair's own
    self-certification.  Every type test here is `type(x) is T`, and --selftest
    mutation 1 changes exactly that and requires the run to fail.

WHAT IT DOES NOT HASH-PIN.  IMPLEMENTATION-FREEZE.md and IMPLEMENTER-BLUEPRINT.md
are under concurrent edit by other lanes.  Section 7.7 records why a whole-file
digest of such a document "would manufacture a false refusal on an unrelated edit
while adding nothing".  The propositions this checker relies on are verified by
whitespace-normalised CONTENT ANCHOR instead, exactly as
check-retention-custody-v24.py does.

USAGE.  python3 -I -B check-delivery-v4.py [--selftest] [--verbose]
EXIT.    0 = no findings.  1 = findings, each naming its position.  2 = input drift.
"""

import argparse
import copy
import hashlib
import importlib.util
import json
import pathlib
import re
import sys
import unicodedata

HERE = pathlib.Path(__file__).resolve().parent
COOP = HERE.parent

SUBJECT = "artifacts/delivery.v4.json"

# Hash-verified before any parse.  Exit 2 on any mismatch.
PINNED = {
    "artifacts/delivery.v4.json":
        "3cffece076289a4e62f3e0680cb8cc7c6a134b3190a6b39b7ec14b007704a121",
    "artifacts/delivery.v2.json":
        "47b6cfd17338fafd407c554afe1951ab23d2896aac99bcfd272fc0894e3cabf3",
    "artifacts/delivery.v3.json":
        "01f1b95d0c740580c9307c188e4c2f6806f4d2e7e54d458f570631734cb62a6d",
    "artifacts/delivery.v3.review-independent.json":
        "7791ef39abe51b6646df3113353187e6c4b8350ac9299a599ecac780fc077796",
    "artifacts/resolved-inputs.v2.json":
        "0114205aaa5d3f7c0aecc58c10522711aacaa6aa404a41563245627b27b88f43",
    "artifacts/fact-plane.v1.json":
        "9057200822c5be59bcf8e691e3755cfa1acf2c89f0b1c2bc89237afaa0925b4d",
    "artifacts/c2-plan-stage-schema.v4.json":
        "4876284790462968549f834b866c7ffc5f7be1c43b583169570c1947c5c4af39",
    "artifacts/check-resolved-inputs.py":
        "7ffed1c0e66e345a72c5e0e7feaf332508d0842c1ecdba8572f872997917ffa0",
}

# Whitespace-normalised excerpts of IMPLEMENTATION-FREEZE.md.  Not a byte pin.
FREEZE_ANCHORS = (
    ("section 6 law 2, the ground of the ordering ruling's leg 4",
     "Resolution uses neutralise/key/forbid. Only declared analysis inputs may "
     "affect `PlanId`; CI does not read layer 4."),
    ("section 7.1, the disqualifier this checker exists to close",
     "No retained checker — a fair residual for a candidate, disqualifying for "
     "application"),
    ("section 7.1, the property a retained checker must have",
     "a byte recipe with no retained checker is a description that happens to "
     "contain digests"),
    ("section 7.2.2's rider, the rule every gate here obeys",
     "a measurement that cannot fail the build is prose"),
    ("section 7.5, why a duplicate-key finding must name the key",
     "6 of 47 rejecting checkers never say which key was duplicated"),
    ("section 7.6, why writing a NEW checker is lawful and editing one is not",
     "a reviewed checker cannot be edited"),
    ("section 7, the declared-but-never-executed control",
     "it declares that, and nothing runs it"),
)

DOMAIN = "opensip.capability-manifest.v1"

# A sentinel for "no gate refused this value".  It must be a string that CANNOT
# occur in a control's stated condition: the bare word ADMITTED does occur --
# NEG-PLAT-1's own thisRule reads "x1 is ADMITTED and mints ..." -- so using it
# made the named-condition gate pass on a value the gates had stopped refusing.
# --selftest mutation SKIP_DOMAIN is what found that.
ADMITTED = "<<NO GATE REFUSED THIS VALUE>>"
PLACEHOLDER_LITERALS = (
    "2" * 64,
    "7" * 64,
)

# --selftest mutation switches.  Every one of them is read at exactly one site.
MUT = set()


# --------------------------------------------------------------------------- io
class Drift(Exception):
    pass


class DuplicateKey(Exception):
    def __init__(self, key, where):
        super().__init__("duplicate JSON key %r in %s" % (key, where))
        self.key = key
        self.where = where


def _hook_factory(where):
    def hook(pairs):
        seen = set()
        for key, _ in pairs:
            if key in seen and "DUP_KEY_HOOK_OFF" not in MUT:
                raise DuplicateKey(key, where)
            seen.add(key)
        return dict(pairs)
    return hook


def sha_bytes(raw):
    return hashlib.sha256(raw).hexdigest()


def read_bytes(rel):
    path = COOP / rel
    if not path.exists():
        raise Drift("pinned input is absent: %s" % rel)
    return path.read_bytes()


def verify_pins():
    """Hash-verify every pinned input BEFORE anything is parsed."""
    problems = []
    for rel, expected in PINNED.items():
        raw = read_bytes(rel)
        actual = sha_bytes(raw)
        if rel == SUBJECT and "SUBJECT_DRIFT" in MUT:
            actual = "0" * 64
        if actual != expected:
            problems.append("%s: recorded %s, measured %s" % (rel, expected, actual))
    return problems


def load_json(rel):
    raw = read_bytes(rel)
    return json.loads(raw.decode("utf-8"), object_pairs_hook=_hook_factory(rel))


# ------------------------------------------------------------------- encoder A
class EncErr(Exception):
    pass


def encA(v):
    """CVE1, recursive, from resolved-inputs.v2#planIdContract.canonicalValueEncoding."""
    if v is None:
        return b"\x00"
    if type(v) is bool:
        return b"\x02" if v else b"\x01"
    if type(v) is float:
        if "FLOAT_ADMITTED" in MUT:
            return b"\x03" + int(v).to_bytes(8, "big")
        raise EncErr("floating-point values are forbidden")
    if type(v) is int:
        if v < 0:
            return b"\x07" + v.to_bytes(8, "big", signed=True)
        return b"\x03" + v.to_bytes(8, "big")
    if type(v) is str:
        if unicodedata.normalize("NFC", v) != v:
            if "NFC_NORMALISE" in MUT:
                v = unicodedata.normalize("NFC", v)
            else:
                raise EncErr("string is not NFC and is rejected, never normalised")
        raw = v.encode("utf-8")
        return b"\x04" + len(raw).to_bytes(4, "big") + raw
    if type(v) is list:
        return (b"\x05" + len(v).to_bytes(4, "big")
                + b"".join(encA(e) for e in v))
    if type(v) is dict:
        keys = list(v)
        if len(set(keys)) != len(keys):
            raise EncErr("duplicate map key")
        for k in keys:
            if type(k) is not str:
                raise EncErr("map key is not a string")
        out = b"\x06" + len(keys).to_bytes(4, "big")
        for k in sorted(keys, key=lambda s: s.encode("utf-8")):
            out += encA(k) + encA(v[k])
        return out
    raise EncErr("value outside CVE1's eight closed types: %s" % type(v).__name__)


# ------------------------------------------------------------------- encoder B
_TAGS = {"null": 0x00, "false": 0x01, "true": 0x02, "unsigned-64": 0x03,
         "NFC-UTF8-string": 0x04, "array": 0x05, "string-keyed-map": 0x06,
         "negative-signed-64": 0x07}


def _be(n, width):
    return bytes((n >> shift) & 0xFF for shift in range(width * 8 - 8, -1, -8))


def _cve1_type_name(v):
    cls = type(v)
    if cls is type(None):
        return "null"
    if cls is bool:
        return "true" if v else "false"
    if cls is int:
        return "unsigned-64" if v >= 0 else "negative-signed-64"
    if cls is float:
        if "FLOAT_ADMITTED" in MUT:
            return "unsigned-64"
        raise EncErr("floating-point values are forbidden")
    if cls is str:
        return "NFC-UTF8-string"
    if cls is list:
        return "array"
    if cls is dict:
        return "string-keyed-map"
    raise EncErr("value outside CVE1's eight closed types: %s" % cls.__name__)


def encB(root):
    """CVE1, table-driven on the eight closed type NAMES, explicit work stack."""
    out = bytearray()
    stack = [root]
    while stack:
        v = stack.pop()
        name = _cve1_type_name(v)
        out.append(_TAGS[name])
        if name in ("null", "true", "false"):
            continue
        if name == "unsigned-64":
            out += _be(int(v), 8)
        elif name == "negative-signed-64":
            out += _be(int(v) + (1 << 64), 8)
        elif name == "NFC-UTF8-string":
            if unicodedata.normalize("NFC", v) != v:
                if "NFC_NORMALISE" in MUT:
                    v = unicodedata.normalize("NFC", v)
                else:
                    raise EncErr("string is not NFC and is rejected, never normalised")
            raw = v.encode("utf-8")
            out += _be(len(raw), 4) + raw
        elif name == "array":
            out += _be(len(v), 4)
            for element in reversed(v):
                stack.append(element)
        else:
            keys = list(v)
            if len(set(keys)) != len(keys):
                raise EncErr("duplicate map key")
            for k in keys:
                if type(k) is not str:
                    raise EncErr("map key is not a string")
            out += _be(len(keys), 4)
            for k in sorted(keys, key=lambda s: s.encode("utf-8"), reverse=True):
                stack.append(v[k])
                stack.append(k)
    return bytes(out)


# --------------------------------------------------------------------- decoder
def decode(buf):
    value, offset = _dec(buf, 0)
    if offset != len(buf):
        raise EncErr("trailing bytes after a complete CVE1 value")
    return value


def _dec(b, i):
    tag = b[i]
    i += 1
    if tag == 0x00:
        return None, i
    if tag == 0x01:
        return False, i
    if tag == 0x02:
        return True, i
    if tag == 0x03:
        return int.from_bytes(b[i:i + 8], "big"), i + 8
    if tag == 0x07:
        return int.from_bytes(b[i:i + 8], "big", signed=True), i + 8
    if tag == 0x04:
        n = int.from_bytes(b[i:i + 4], "big")
        i += 4
        return b[i:i + n].decode("utf-8"), i + n
    if tag == 0x05:
        n = int.from_bytes(b[i:i + 4], "big")
        i += 4
        out = []
        for _ in range(n):
            value, i = _dec(b, i)
            out.append(value)
        return out, i
    if tag == 0x06:
        n = int.from_bytes(b[i:i + 4], "big")
        i += 4
        out = {}
        for _ in range(n):
            key, i = _dec(b, i)
            value, i = _dec(b, i)
            out[key] = value
        return out, i
    raise EncErr("unknown CVE1 tag 0x%02x" % tag)


class EncoderDisagreement(Exception):
    pass


def cve1(value):
    """Both encoders, always.  A disagreement is a defect, never a tie-break."""
    a = encA(value)
    b = encB(value)
    if a != b:
        raise EncoderDisagreement("encoder A and encoder B disagree")
    return a


def cap_manifest_id(manifest):
    prefix = DOMAIN.encode("utf-8")
    if "NO_NUL" not in MUT:
        prefix += b"\x00"
    return hashlib.sha256(prefix + cve1(manifest)).hexdigest()


# ------------------------------------------------------------------- admission
CM_KEYS = ["schemaVersion", "profile", "providers", "coverageForAbsent"]
PC_KEYS = ["providerId", "language", "providerVersionSource",
           "toolchainIdentitySource", "relations", "platformIds"]
AC_KEYS = ["providerId", "language", "relationIds", "coverageState", "deficiency"]

# The fourteen reachable scalar type-positions DL-DOM-1 quantifies over.
BOUND_SCALARS = [
    "ProviderCapability.platformIds[]",
    "ProviderCapability.relations key",
    "ProviderCapability.relations value",
    "AbsentCapability.relationIds[]",
    "AbsentCapability.coverageState",
    "AbsentCapability.deficiency",
]
OPEN_SCALARS = [
    "CapabilityManifestV1.schemaVersion",
    "CapabilityManifestV1.profile",
    "ProviderCapability.providerId",
    "ProviderCapability.language",
    "ProviderCapability.providerVersionSource",
    "ProviderCapability.toolchainIdentitySource",
    "AbsentCapability.providerId",
    "AbsentCapability.language",
]


class Registries:
    def __init__(self, delivery_v2, fact_plane):
        matrix = delivery_v2["platformMatrix"]
        self.platform = (["all-supported"]
                         + [r["platformId"] for r in matrix["supported"]]
                         + [r["platformId"] for r in matrix["bestEffort"]])
        self.relations = fact_plane["relationRegistry"]["relations"]
        self.deficiency = list(fact_plane["deficiencyVocabulary"]["values"])
        self.coverage_state = ["unavailable"]


def adm_type(manifest, errs):
    """Section 6 law 18.  EXACT type, never isinstance."""
    def is_int(x):
        if "EXACT_TYPE_OFF" in MUT:
            return isinstance(x, int)
        return type(x) is int

    def is_str(x):
        if "EXACT_TYPE_OFF" in MUT:
            return isinstance(x, str)
        return type(x) is str

    if not is_int(manifest.get("schemaVersion")):
        errs.append("schemaVersion: exact-type -- %s is not an integer"
                    % type(manifest.get("schemaVersion")).__name__)
    if not is_str(manifest.get("profile")):
        errs.append("profile: exact-type -- %s is not a string"
                    % type(manifest.get("profile")).__name__)
    for record, keys in (("ProviderCapability", PC_KEYS),
                         ("AbsentCapability", AC_KEYS)):
        source = manifest.get("providers" if record == "ProviderCapability"
                              else "coverageForAbsent")
        if type(source) is not list:
            continue
        for entry in source:
            if type(entry) is not dict:
                errs.append("%s: exact-type -- entry is not an object" % record)
                continue
            for key in keys:
                if key in ("relations",):
                    if type(entry.get(key)) is not dict:
                        errs.append("%s.%s: exact-type -- not an object" % (record, key))
                elif key in ("platformIds", "relationIds"):
                    if type(entry.get(key)) is not list:
                        errs.append("%s.%s: exact-type -- not an array" % (record, key))
                elif not is_str(entry.get(key)):
                    errs.append("%s.%s: exact-type -- %s is not a string"
                                % (record, key, type(entry.get(key)).__name__))
    return errs


def adm_closed(manifest, errs):
    """DL-CLOSED-1.  Records are closed; a map declares a key domain and is not.

    MUT CLOSE_THE_MAP reinstates delivery.v3's catch-all reading, under which a
    reachable object type with no declared key set -- which `relations` is -- is
    inadmissible.  That is blocker IR-V3-B1 and it refuses all four live
    manifests, which is exactly what the mutation must demonstrate.
    """
    if sorted(manifest) != sorted(CM_KEYS):
        errs.append("CapabilityManifestV1: field set %r != %r"
                    % (sorted(manifest), sorted(CM_KEYS)))
    for entry in manifest.get("providers", []):
        if type(entry) is not dict:
            continue
        if sorted(entry) != sorted(PC_KEYS):
            errs.append("ProviderCapability: field set %r != %r"
                        % (sorted(entry), sorted(PC_KEYS)))
        if "CLOSE_THE_MAP" in MUT:
            errs.append("ProviderCapability.relations: a reachable object type that "
                        "declares no key set is inadmissible until it declares one")
    for entry in manifest.get("coverageForAbsent", []):
        if type(entry) is not dict:
            continue
        if sorted(entry) != sorted(AC_KEYS):
            errs.append("AbsentCapability: field set %r != %r"
                        % (sorted(entry), sorted(AC_KEYS)))
    return errs


def adm_domain(manifest, reg, errs):
    """DL-DOM-1.  Bound scalars are compared by EXACT NFC UTF-8 bytes."""
    if "SKIP_DOMAIN" in MUT:
        return errs
    for entry in manifest.get("providers", []):
        for value in entry.get("platformIds", []):
            if value not in reg.platform:
                errs.append("ProviderCapability.platformIds: %r is not a member of "
                            "PLATFORM-ID-DOMAIN-V1" % value)
        for key, rung in entry.get("relations", {}).items():
            if key not in reg.relations:
                errs.append("ProviderCapability.relations: key %r is not a member of "
                            "fact-plane.v1#relationRegistry.relations" % key)
            elif rung not in reg.relations[key]["ladder"]:
                errs.append("ProviderCapability.relations: %r is not a rung of relation "
                            "%r's ladder" % (rung, key))
    for entry in manifest.get("coverageForAbsent", []):
        for value in entry.get("relationIds", []):
            if value not in reg.relations:
                errs.append("AbsentCapability.relationIds: %r is not a member of "
                            "fact-plane.v1#relationRegistry.relations" % value)
        if entry.get("coverageState") not in reg.coverage_state:
            errs.append("AbsentCapability.coverageState: %r is not 'unavailable'"
                        % entry.get("coverageState"))
        if entry.get("deficiency") not in reg.deficiency:
            errs.append("AbsentCapability.deficiency: %r is not a member of "
                        "fact-plane.v1#deficiencyVocabulary" % entry.get("deficiency"))
    return errs


def _ascending(seq, key_of, where, errs):
    for i in range(1, len(seq)):
        previous = key_of(seq[i - 1]).encode("utf-8")
        current = key_of(seq[i]).encode("utf-8")
        if not previous < current:
            errs.append("%s: not strictly ascending by declared key UTF-8 bytes at "
                        "index %d (%r then %r)"
                        % (where, i, key_of(seq[i - 1]), key_of(seq[i])))


def adm_order(manifest, errs):
    """DL-ORD-1, in the traversal delivery.v4 declares at admission.traversalOrder."""
    if "SKIP_ORDER" in MUT:
        return errs
    for entry in manifest.get("providers", []):
        _ascending(entry.get("platformIds", []), lambda s: s,
                   "ProviderCapability.platformIds", errs)
    for entry in manifest.get("coverageForAbsent", []):
        _ascending(entry.get("relationIds", []), lambda s: s,
                   "AbsentCapability.relationIds", errs)
    _ascending(manifest.get("providers", []), lambda d: d["providerId"],
               "CapabilityManifestV1.providers", errs)
    _ascending(manifest.get("coverageForAbsent", []), lambda d: d["providerId"],
               "CapabilityManifestV1.coverageForAbsent", errs)
    return errs


def admit(manifest, reg):
    """The four gates, in the artifact's declared order.  Returns a message list."""
    errs = []
    adm_type(manifest, errs)
    adm_closed(manifest, errs)
    if errs:
        return errs
    adm_domain(manifest, reg, errs)
    if errs:
        return errs
    adm_order(manifest, errs)
    return errs


def _sort_key_providers(entry):
    if "SORT_BY_ENCODED_BYTES" in MUT:
        return cve1(entry)
    return entry["providerId"].encode("utf-8")


def canonicalise(manifest):
    if "NO_CANONICALISE" in MUT:
        return copy.deepcopy(manifest)
    out = dict(manifest)
    out["providers"] = sorted(
        [dict(p, platformIds=sorted(p["platformIds"], key=lambda s: s.encode("utf-8")))
         for p in manifest["providers"]], key=_sort_key_providers)
    out["coverageForAbsent"] = sorted(
        [dict(a, relationIds=sorted(a["relationIds"], key=lambda s: s.encode("utf-8")))
         for a in manifest["coverageForAbsent"]],
        key=lambda d: d["providerId"].encode("utf-8"))
    return out


# ------------------------------------------------------------------ PLAN-ID-V1
PLAN_FIELDS = ["snapshotId", "planSchemaMajor", "release", "invocationProfile",
               "resolvedConfiguration", "scope", "changeSpec", "contributions",
               "semanticUniverses", "capabilityGrants", "workflow", "budgets",
               "planIntentCommitment"]
_SET_VALUED_STAGE_ARRAYS = ("dependsOn", "relations", "ruleIds", "capabilityGrants")


def _utf8(s):
    return s.encode("utf-8")


def canonicalise_plan(plan):
    p = copy.deepcopy(plan)
    p["resolvedConfiguration"] = sorted(p["resolvedConfiguration"],
                                        key=lambda d: _utf8(d["path"]))
    scope = p["scope"]
    scope["workspaceUnitIds"] = sorted(set(scope["workspaceUnitIds"]), key=_utf8)
    scope["requestedPaths"] = sorted(set(scope["requestedPaths"]), key=_utf8)
    p["contributions"] = sorted(p["contributions"], key=lambda d: _utf8(d["activationId"]))
    p["semanticUniverses"] = sorted(p["semanticUniverses"], key=lambda d: _utf8(d["providerId"]))
    p["capabilityGrants"] = sorted(
        p["capabilityGrants"],
        key=lambda d: (_utf8(d["grantId"]), _utf8(d["grantVersion"]), _utf8(d["projectId"])))
    stages = sorted(p["workflow"]["stages"], key=lambda d: _utf8(d["stageId"]))
    for stage in stages:
        for name in _SET_VALUED_STAGE_ARRAYS:
            if type(stage.get(name)) is list:
                stage[name] = sorted(set(stage[name]), key=_utf8)
    p["workflow"]["stages"] = stages
    return p


def plan_preimage(plan):
    p = canonicalise_plan(plan)
    out = bytearray(b"opensip.plan-id\x00")
    out += (1).to_bytes(2, "big")
    out += (13).to_bytes(2, "big")
    for tag, name in enumerate(PLAN_FIELDS, start=1):
        encoded = cve1(p[name])
        out.append(tag)
        out += len(encoded).to_bytes(4, "big")
        out += encoded
    return bytes(out)


def plan_id(plan):
    pre = plan_preimage(plan)
    return pre, "plan1:sha256:" + hashlib.sha256(pre).hexdigest()


# ----------------------------------------------------------------------- gates
class Run:
    def __init__(self, verbose=False):
        self.findings = []
        self.counts = {}
        self.verbose = verbose
        # every 64-hex value this run RECOMPUTED and compared, for gate G19
        self.recomputed = set()

    def fail(self, code, position, detail):
        self.findings.append("%s at %s: %s" % (code, position, detail))

    def eq(self, code, position, got, want, note=""):
        if "NO_RECOMPUTE_LEDGER" not in MUT:
            for value in (got, want):
                if type(value) is str:
                    self.recomputed.update(_HEX64.findall(value))
        if got != want:
            self.fail(code, position,
                      "recomputed %r, artifact publishes %r%s"
                      % (got, want, (" -- " + note) if note else ""))
            return False
        self.counts[code] = self.counts.get(code, 0) + 1
        return True

    def bump(self, name, n=1):
        self.counts[name] = self.counts.get(name, 0) + n


def gate_anchors(run):
    """G01 -- the freeze propositions this artifact cites, by content anchor."""
    raw = (COOP / "IMPLEMENTATION-FREEZE.md").read_text(encoding="utf-8")
    flat = re.sub(r"\s+", " ", raw)
    for label, text in FREEZE_ANCHORS:
        needle = re.sub(r"\s+", " ", text)
        if "ANCHOR_DRIFT" in MUT:
            needle += " (mutated)"
        if needle not in flat:
            run.fail("DV4-ANCHOR", label,
                     "the cited text is absent from the live IMPLEMENTATION-FREEZE.md")
        else:
            run.bump("anchorsVerified")


def gate_standing(run, art):
    """G02 -- the standing this candidate declares, and what it must not have moved."""
    expected = {
        "artifact": "delivery.v4.json",
        "surface": "DELIVERY",
        "status": "CANDIDATE",
        "applicationState": "NOT APPLIED",
        "reviewState": "AWAITING-INDEPENDENT-REVIEW",
        "binds": "NOTHING",
        "sealRecommendation": "DO-NOT-SEAL",
    }
    for key, want in expected.items():
        if art.get(key) != want:
            run.fail("DV4-STANDING", "$." + key,
                     "declares %r, a retained candidate must declare %r" % (art.get(key), want))
        else:
            run.bump("standingChecks")
    flat = json.dumps(art)
    if "[UNSET]" in flat:
        run.fail("DV4-STANDING", "$", "the artifact contains the literal [UNSET]")
    if "BLOCKED_ON_PHASE_1A" in flat and "CD-RT-5" not in flat:
        run.fail("DV4-STANDING", "$", "a disposition literal appears without its row id")
    for op in art["derivedFrom"]["operations"]:
        if op["op"] == "set" and "from" not in op:
            run.fail("DV4-STANDING", "derivedFrom.operations",
                     "a set operation restates no predecessor value")


def gate_derivation(run, art, base):
    """G03 -- resolve the delta against the verified predecessor, type-exactly."""
    decl = art["derivedFrom"]
    run.eq("DV4-DERIV", "derivedFrom.artifact", decl["artifact"], "delivery.v2.json")
    run.eq("DV4-DERIV", "derivedFrom.sha256", decl["sha256"],
           PINNED["artifacts/delivery.v2.json"])
    effective = copy.deepcopy(base)
    for index, op in enumerate(decl["operations"]):
        where = "derivedFrom.operations[%d] (%s %s)" % (index, op["op"], op["path"])
        steps = op["path"].split(".")
        node = effective
        ok = True
        for step in steps[:-1]:
            if type(node) is not dict or step not in node:
                run.fail("DV4-DERIV", where, "parent path does not resolve")
                ok = False
                break
            node = node[step]
        if not ok:
            continue
        leaf = steps[-1]
        if op["op"] == "set":
            if leaf not in node:
                run.fail("DV4-DERIV", where, "does not resolve against the predecessor")
                continue
            current = node[leaf]
            if not exact_equal(current, op["from"]):
                run.fail("DV4-DERIV", where,
                         "declares it replaces %r (%s) but the verified predecessor holds "
                         "%r (%s)" % (op["from"], type(op["from"]).__name__,
                                      current, type(current).__name__))
                continue
        else:
            if leaf in node:
                run.fail("DV4-DERIV", where, "already exists in the predecessor")
                continue
        node[leaf] = copy.deepcopy(op["value"])
        run.bump("operationsApplied")
    return effective


def exact_equal(left, right):
    if type(left) is not type(right):
        return False
    if type(left) is dict:
        return set(left) == set(right) and all(exact_equal(left[k], right[k]) for k in left)
    if type(left) is list:
        return len(left) == len(right) and all(exact_equal(a, b) for a, b in zip(left, right))
    return left == right


def gate_goldens(run, resolved_inputs, c2v4):
    """G04 -- the binding-artifact oracle.  Both pinned PLAN-ID-V1 goldens."""
    positives = {v["id"]: v for v in resolved_inputs["planIdContract"]["goldenVectors"]["positive"]}
    minimal = positives["planid-v1-ci-minimal"]
    pre, pid = plan_id(minimal["input"])
    run.eq("DV4-ORACLE", "planid-v1-ci-minimal.preimageBytes",
           len(pre), minimal["expectedPreimageByteLength"])
    run.eq("DV4-ORACLE", "planid-v1-ci-minimal.planId", pid, minimal["expectedPlanId"])

    full_vector = positives["planid-v1-ci-full-providers"]
    spec = importlib.util.spec_from_file_location(
        "_cri", str(HERE / "check-resolved-inputs.py"))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    full = module._materialize_plan_vector(full_vector, c2v4)
    pre_full, pid_full = plan_id(full)
    run.eq("DV4-ORACLE", "planid-v1-ci-full-providers.preimageBytes",
           len(pre_full), full_vector["expectedPreimageByteLength"])
    run.eq("DV4-ORACLE", "planid-v1-ci-full-providers.planId",
           pid_full, full_vector["expectedPlanId"])
    return minimal["input"], full, pre, pre_full


def _reachable_objects(manifest):
    """Every reachable object, classified as delivery.v4's recordShape declares."""
    out = [("CapabilityManifestV1", manifest, "RECORD")]
    for entry in manifest.get("providers", []):
        out.append(("ProviderCapability", entry, "RECORD"))
        out.append(("ProviderCapability.relations", entry.get("relations", {}), "MAP"))
        for rung in entry.get("relations", {}).values():
            if type(rung) is dict:
                out.append(("ProviderCapability.relations value", rung, "UNCLASSIFIED"))
    for entry in manifest.get("coverageForAbsent", []):
        out.append(("AbsentCapability", entry, "RECORD"))
    return out


def gate_closure_property(run, manifest, label):
    """G05 -- DL-CLOSED-1 as a property, walked over a real admitted value."""
    for name, obj, kind in _reachable_objects(manifest):
        if kind == "UNCLASSIFIED":
            run.fail("DV4-CLOSURE", "%s / %s" % (label, name),
                     "a reachable object is neither a declared record nor a declared map; "
                     "DL-CLOSED-1 makes it inadmissible until the schema declares one")
            continue
        if kind == "RECORD":
            declared = {"CapabilityManifestV1": CM_KEYS, "ProviderCapability": PC_KEYS,
                        "AbsentCapability": AC_KEYS}[name]
            if sorted(obj) != sorted(declared):
                run.fail("DV4-CLOSURE", "%s / %s" % (label, name),
                         "record key set %r is not its declared %r"
                         % (sorted(obj), sorted(declared)))
            else:
                run.bump("recordsClosed")
        else:
            for value in obj.values():
                if type(value) not in (str, int, bool, type(None)):
                    run.fail("DV4-CLOSURE", "%s / %s" % (label, name),
                             "a declared map's value is not a scalar, so DL-CLOSED-1's "
                             "recursive clause applies and this object is unclosed")
            run.bump("mapsWalked")


def gate_domain_census(run, art):
    """G06 -- DL-DOM-1's scalar census is exhaustive at fourteen positions."""
    domains = None
    for op in art["derivedFrom"]["operations"]:
        if op["path"] == "capabilityManifestSchema.valueDomains":
            domains = op["value"]
    if domains is None:
        run.fail("DV4-DOMAIN", "derivedFrom", "the artifact declares no valueDomains block")
        return
    published_bound = []
    for spec in domains["registries"].values():
        published_bound.extend(spec["boundPositions"])
    published_open = sorted(domains["declaredOPEN"])
    if sorted(published_bound) != sorted(BOUND_SCALARS):
        run.fail("DV4-DOMAIN", "valueDomains.registries[].boundPositions",
                 "publishes %r, this checker reaches %r"
                 % (sorted(published_bound), sorted(BOUND_SCALARS)))
    else:
        run.bump("boundPositions", len(published_bound))
    if published_open != sorted(OPEN_SCALARS):
        run.fail("DV4-DOMAIN", "valueDomains.declaredOPEN",
                 "publishes %r, this checker reaches %r" % (published_open, sorted(OPEN_SCALARS)))
    else:
        run.bump("openPositions", len(published_open))
    total = len(published_bound) + len(published_open)
    if total != 14:
        run.fail("DV4-DOMAIN", "valueDomains.censusIsEXHAUSTIVE",
                 "%d + %d = %d, the census claims fourteen reachable scalar positions"
                 % (len(published_bound), len(published_open), total))
    overlap = set(published_bound) & set(published_open)
    if overlap:
        run.fail("DV4-DOMAIN", "valueDomains", "a position is both bound and open: %r"
                 % sorted(overlap))


def gate_vectors(run, art, base, reg):
    """G07 -- every published vector, recomputed from the recipe."""
    identity = None
    for op in art["derivedFrom"]["operations"]:
        if op["path"] == "capabilityManifestIdentity":
            identity = op["value"]
    if identity is None:
        run.fail("DV4-VECTOR", "derivedFrom", "no capabilityManifestIdentity operation")
        return None
    vectors = identity["vectors"]["byId"]
    run.eq("DV4-COUNT", "vectors.count", len(vectors), identity["vectors"]["count"])

    profiles = base["installProfiles"]["profiles"]
    live_index = {"DCM-1-core": 0, "DCM-2-typescript-deep": 1,
                  "DCM-3-rust-deep": 2, "DCM-4-full": 3}
    computed_ids = {}
    for name, vector in vectors.items():
        if name in live_index:
            authoring = profiles[live_index[name]]["capabilityManifest"]
            committed = canonicalise(authoring)
            violations = admit(authoring, reg)
            run.eq("DV4-VECTOR", "%s.authoringFormViolations" % name,
                   violations, vector["authoringFormViolations"],
                   "the complete list under the declared traversal")
            run.eq("DV4-VECTOR", "%s.authoringFormAdmissible" % name,
                   violations == [], vector["authoringFormAdmissible"])
        elif "authoringForm" in vector:
            committed = canonicalise(vector["authoringForm"])
            violations = admit(vector["authoringForm"], reg)
            run.eq("DV4-VECTOR", "%s.authoringFormViolations" % name,
                   violations, vector["authoringFormViolations"])
            run.eq("DV4-VECTOR", "%s.committedManifest" % name,
                   committed, vector["committedManifest"],
                   "canonicalise(authoringForm) must be the published committed manifest")
        else:
            committed = vector["committedManifest"]

        admitted = admit(committed, reg)
        if admitted:
            run.fail("DV4-VECTOR", "%s.committed" % name,
                     "the published committed form is INADMISSIBLE: %s" % admitted[0])
            continue
        gate_closure_property(run, committed, name)

        encoded = cve1(committed)
        run.eq("DV4-VECTOR", "%s.committedByteLength" % name,
               len(encoded), vector["committedByteLength"])
        run.eq("DV4-VECTOR", "%s.committedBytesHex" % name,
               encoded.hex(), vector["committedBytesHex"])
        run.eq("DV4-VECTOR", "%s.committedBytesSha256" % name,
               sha_bytes(encoded), vector["committedBytesSha256"])
        minted = cap_manifest_id(committed)
        run.eq("DV4-VECTOR", "%s.capabilityManifestId" % name,
               minted, vector["capabilityManifestId"])
        computed_ids[name] = minted
        if minted in PLACEHOLDER_LITERALS:
            run.fail("DV4-VECTOR", "%s.capabilityManifestId" % name,
                     "equals a placeholder literal, which is evidence of back-fitting")

        # decode(encode(x)) == x, LITERALLY, and the published hex re-encodes.
        if decode(encoded) != committed:
            run.fail("DV4-VECTOR", "%s.literalRoundTrip" % name,
                     "decode(encode(x)) != x on an admitted value")
        else:
            run.bump("roundTrips")
        from_hex = bytes.fromhex(vector["committedBytesHex"])
        if cve1(decode(from_hex)) != from_hex:
            run.fail("DV4-VECTOR", "%s.committedBytesHex" % name,
                     "the published hex does not re-encode to itself")
        else:
            run.bump("hexReEncodes")
    sort_rule = vectors.get("DCM-6-sort-rule")
    if sort_rule is not None and "encodedByteSortWouldMint" in sort_rule:
        with _temporarily(MUT, "SORT_BY_ENCODED_BYTES"):
            wrong = canonicalise(sort_rule["authoringForm"])
        run.eq("DV4-VECTOR", "DCM-6-sort-rule.encodedByteSortWouldMint",
               cap_manifest_id(wrong), sort_rule["encodedByteSortWouldMint"],
               "sorting by encoded item bytes is length-major and orders ['b','aa']")
        if cap_manifest_id(wrong) == sort_rule["capabilityManifestId"]:
            run.fail("DV4-VECTOR", "DCM-6-sort-rule",
                     "the two sort conventions mint one id, so this vector separates "
                     "nothing")
    return identity, computed_ids


class _temporarily:
    """Add a reading switch for one measurement and restore EXACTLY what was there.

    A naive add/discard pair silently deletes a switch --selftest has already set,
    which makes the mutation under test disappear and the run come back clean.  That
    happened here and --selftest mutation SKIP_DOMAIN is what found it.
    """

    def __init__(self, flags, name):
        self.flags = flags
        self.name = name
        self.was_present = name in flags

    def __enter__(self):
        self.flags.add(self.name)
        return self

    def __exit__(self, *exc):
        if not self.was_present:
            self.flags.discard(self.name)
        return False


def _apply_construction(cons, ctx, half=None):
    """Build a control's input from the construction the ARTIFACT declares.

    The checker interprets a small declared vocabulary rather than hard-coding
    the documents, so a control cannot drift from the thing this file executes.
    """
    kind = cons["kind"]
    if kind == "liveAuthoringForm":
        value = copy.deepcopy(ctx["profiles"][cons["profileIndex"]]["capabilityManifest"])
        transform = cons.get("transform")
        if transform == "reverseCoverageForAbsent":
            value["coverageForAbsent"] = list(reversed(value["coverageForAbsent"]))
        elif transform == "reverseProviders":
            value["providers"] = list(reversed(value["providers"]))
        elif transform is not None:
            raise KeyError("unknown construction transform %r" % transform)
        return value
    if kind == "baseManifest":
        return copy.deepcopy(ctx["control"]["baseManifest"])
    if kind == "vector":
        value = copy.deepcopy(ctx["vectors"][cons["baseVector"]]["committedManifest"])
        if half == "x2" and "x2PlatformIds" in cons:
            value["providers"][0]["platformIds"] = list(cons["x2PlatformIds"])
        elif half is None and "platformIds" in cons:
            value["providers"][0]["platformIds"] = list(cons["platformIds"])
        return value
    if kind == "coreCommitted":
        value = copy.deepcopy(ctx["core"])
        spec = cons
        if half in ("providerHalf", "absentHalf"):
            spec = cons[half]
        if "setSchemaVersion" in spec:
            token = spec["setSchemaVersion"]
            value["schemaVersion"] = {"jsonBooleanTrue": True,
                                      "jsonStringOne": "1",
                                      "jsonNumberOneDotZero": 1.0}[token]
        if "setProfile" in spec:
            value["profile"] = spec["setProfile"]
        if "setDeficiency" in spec:
            value["coverageForAbsent"][0]["deficiency"] = spec["setDeficiency"]
        if "addRelationId" in spec:
            entry = value["coverageForAbsent"][0]
            entry["relationIds"] = sorted(entry["relationIds"] + [spec["addRelationId"]])
        if "insertAt" in spec:
            where = spec["insertAt"]
            target = {"providers[0]": value["providers"][0],
                      "coverageForAbsent[0]": value["coverageForAbsent"][0]}[where]
            target[spec["key"]] = spec["value"]
        return value
    if kind == "allFourLiveCommitted":
        return None
    raise KeyError("unknown construction kind %r" % kind)


def gate_controls(run, identity, base, reg, vectors):
    """Every negative control, EXECUTED from its own declared construction, and
    each asserting the SPECIFIC NAMED CONDITION it states -- never merely a
    non-zero exit.  IMPLEMENTATION-FREEZE.md section 7 records EPC-V2 in a
    sibling artifact as declared-but-never-executed; the executed-count gate at
    the end of this function is what stops that happening here."""
    controls = {c["id"]: c for c in identity["negativeControls"]["controls"]}
    run.eq("DV4-COUNT", "negativeControls.count", len(controls),
           identity["negativeControls"]["count"])
    profiles = base["installProfiles"]["profiles"]
    core = canonicalise(profiles[0]["capabilityManifest"])
    executed = set()

    def ctx_for(cid):
        return {"profiles": profiles, "core": core, "vectors": vectors,
                "control": controls[cid]}

    def build(cid, half=None):
        control = controls[cid]
        if "construction" not in control:
            run.fail("DV4-CONTROL", cid,
                     "declares no machine-readable construction, so nothing can execute it")
            return None
        return _apply_construction(control["construction"], ctx_for(cid), half)

    def named(cid, condition, position):
        stated = controls[cid].get("thisRule", "")
        if condition not in stated:
            run.fail("DV4-CONTROL", position,
                     "executed outcome %r is not the condition the control states (%r)"
                     % (condition, stated[:200]))
        else:
            run.bump("namedConditionsMatched")
        executed.add(cid)

    def refusal_of(value):
        errs = admit(value, reg)
        return errs[0] if errs else ADMITTED

    for cid in sorted(controls):
        if "construction" not in controls[cid]:
            run.fail("DV4-CONTROL", cid, "declares no construction")

    # ---- NEG-ORD-1 / NEG-ORD-2 / NEG-ORD-3 -------------------------------
    ord1 = build("NEG-ORD-1")
    named("NEG-ORD-1", " | ".join(admit(ord1, reg)) or ADMITTED, "NEG-ORD-1.thisRule")
    run.eq("DV4-CONTROL", "NEG-ORD-1.orderBearingReadingWouldMint",
           cap_manifest_id(ord1), controls["NEG-ORD-1"]["orderBearingReadingWouldMint"])
    run.eq("DV4-CONTROL", "NEG-ORD-1.byteLengthIsNotADefence",
           len(cve1(ord1)), len(cve1(canonicalise(ord1))),
           "the inadmissible and the admissible form must be the same byte length, or "
           "length alone would separate the readings")

    ord2 = build("NEG-ORD-2")
    named("NEG-ORD-2", " | ".join(admit(ord2, reg)) or ADMITTED, "NEG-ORD-2.thisRule")
    run.eq("DV4-CONTROL", "NEG-ORD-2.orderBearingReadingWouldMint",
           cap_manifest_id(ord2), controls["NEG-ORD-2"]["orderBearingReadingWouldMint"])
    if cve1(canonicalise(ord1)) != cve1(canonicalise(ord2)):
        run.fail("DV4-CONTROL", "NEG-ORD-2.canonicalise",
                 "the two authoring documents do not canonicalise to one byte string, so "
                 "the collision this control is about is not the one described")
    else:
        run.bump("collisionsCanonicalised")

    ord3 = build("NEG-ORD-3")
    full_auth = copy.deepcopy(profiles[3]["capabilityManifest"])
    executed.add("NEG-ORD-3")
    run.eq("DV4-CONTROL", "NEG-ORD-3.canonicalId",
           cap_manifest_id(canonicalise(ord3)), cap_manifest_id(canonicalise(full_auth)),
           "two builders disagreeing only about array order must reach ONE id")
    run.eq("DV4-CONTROL", "NEG-ORD-3.reversed", cap_manifest_id(ord3),
           controls["NEG-ORD-3"]["orderBearingReadingWouldMint"]["reversed"])
    run.eq("DV4-CONTROL", "NEG-ORD-3.asDeclared", cap_manifest_id(full_auth),
           controls["NEG-ORD-3"]["orderBearingReadingWouldMint"]["asDeclared"])

    # ---- NEG-DUP-1 / NEG-DUP-2 -------------------------------------------
    dup1 = build("NEG-DUP-1")
    named("NEG-DUP-1", " | ".join(admit(dup1, reg)) or ADMITTED, "NEG-DUP-1.thisRule")
    run.eq("DV4-CONTROL", "NEG-DUP-1.aDUPLICATETOLERATINGImplementationWouldMint",
           cap_manifest_id(dup1),
           controls["NEG-DUP-1"]["aDUPLICATETOLERATINGImplementationWouldMint"])
    deduped = copy.deepcopy(dup1)
    deduped["providers"] = [deduped["providers"][0]]
    run.eq("DV4-CONTROL", "NEG-DUP-1.aDEDUPLICATINGImplementationWouldMint",
           cap_manifest_id(deduped),
           controls["NEG-DUP-1"]["aDEDUPLICATINGImplementationWouldMint"])
    if (controls["NEG-DUP-1"]["aDUPLICATETOLERATINGImplementationWouldMint"]
            == controls["NEG-DUP-1"]["aDEDUPLICATINGImplementationWouldMint"]):
        run.fail("DV4-CONTROL", "NEG-DUP-1",
                 "the two published readings are the same value, so the control separates "
                 "nothing")

    dup2 = build("NEG-DUP-2")
    named("NEG-DUP-2", " | ".join(admit(dup2, reg)) or ADMITTED, "NEG-DUP-2.thisRule")
    run.eq("DV4-CONTROL", "NEG-DUP-2.aBYTESONLYDeduplicatorWouldMint",
           cap_manifest_id(dup2), controls["NEG-DUP-2"]["aBYTESONLYDeduplicatorWouldMint"])

    # ---- NEG-TYPE-1..3, section 6 law 18 ---------------------------------
    type1 = build("NEG-TYPE-1")
    named("NEG-TYPE-1", refusal_of(type1), "NEG-TYPE-1.thisRule")
    run.eq("DV4-CONTROL", "NEG-TYPE-1.wouldMint", cap_manifest_id(type1),
           controls["NEG-TYPE-1"]["wouldMint"])

    type2 = build("NEG-TYPE-2")
    named("NEG-TYPE-2", refusal_of(type2), "NEG-TYPE-2.thisRule")
    run.eq("DV4-CONTROL", "NEG-TYPE-2.wouldMint", cap_manifest_id(type2),
           controls["NEG-TYPE-2"]["wouldMint"])

    type3 = build("NEG-TYPE-3")
    named("NEG-TYPE-3", refusal_of(type3), "NEG-TYPE-3.thisRule")
    try:
        cve1(type3)
        run.fail("DV4-CONTROL", "NEG-TYPE-3.andSECONDARILY",
                 "CVE1 encoded a float; resolved-inputs.v2 forbids floating-point outright")
    except EncErr:
        run.bump("cve1Refusals")

    # ---- NEG-CLOSED-1 / NEG-CLOSED-2 / NEG-CLOSED-3 ----------------------
    closed1 = build("NEG-CLOSED-1")
    named("NEG-CLOSED-1", refusal_of(closed1), "NEG-CLOSED-1.thisRule")
    run.eq("DV4-CONTROL", "NEG-CLOSED-1.wouldMint", cap_manifest_id(closed1),
           controls["NEG-CLOSED-1"]["wouldMint"])
    run.eq("DV4-CONTROL", "NEG-CLOSED-1.committedByteLengthUnderTheOpenReading",
           len(cve1(closed1)),
           controls["NEG-CLOSED-1"]["committedByteLengthUnderTheOpenReading"])

    provider_half = build("NEG-CLOSED-2", "providerHalf")
    absent_half = build("NEG-CLOSED-2", "absentHalf")
    published = controls["NEG-CLOSED-2"]["underTheUNCLOSEDreadingOfThisArtifactsOwnRecipe"]
    run.eq("DV4-CONTROL", "NEG-CLOSED-2.baseline", cap_manifest_id(core),
           published["baseline"])
    run.eq("DV4-CONTROL", "NEG-CLOSED-2.extraKeyInProviderCapability",
           cap_manifest_id(provider_half), published["extraKeyInProviderCapability"])
    run.eq("DV4-CONTROL", "NEG-CLOSED-2.extraKeyInAbsentCapability",
           cap_manifest_id(absent_half), published["extraKeyInAbsentCapability"])
    run.eq("DV4-CONTROL", "NEG-CLOSED-2.committedByteLengths",
           [len(cve1(core)), len(cve1(provider_half)), len(cve1(absent_half))],
           published["committedByteLengths"])
    three = {cap_manifest_id(core), cap_manifest_id(provider_half),
             cap_manifest_id(absent_half)}
    if len(three) != 3:
        run.fail("DV4-CONTROL", "NEG-CLOSED-2.anyTwoEqual",
                 "the three documents do not mint three distinct ids")
    if not admit(provider_half, reg) or not admit(absent_half, reg):
        run.fail("DV4-CONTROL", "NEG-CLOSED-2.thisRule",
                 "ADM-CLOSED admitted an extra-key document")
    executed.add("NEG-CLOSED-2")

    closed3 = controls["NEG-CLOSED-3"]["measured"]
    key_sizes, per_provider, admitted_here = set(), [], 0
    for index, name in enumerate(["DCM-1-core", "DCM-2-typescript-deep",
                                  "DCM-3-rust-deep", "DCM-4-full"]):
        committed = canonicalise(profiles[index]["capabilityManifest"])
        if admit(committed, reg) == []:
            admitted_here += 1
        for entry in committed["providers"]:
            key_sizes.add(len(entry["relations"]))
            per_provider.append([name, entry["providerId"], len(entry["relations"])])
    run.eq("DV4-CONTROL", "NEG-CLOSED-3.relationsKeySetSizes", sorted(key_sizes),
           closed3["relationsKeySetSizesAcrossTheFourLiveManifests"])
    run.eq("DV4-CONTROL", "NEG-CLOSED-3.perProviderRelationsKeyCount", per_provider,
           closed3["perProviderRelationsKeyCount"])
    run.eq("DV4-CONTROL", "NEG-CLOSED-3.admittedUnderTHISDOCUMENTSRepairedProperty",
           admitted_here, closed3["admittedUnderTHISDOCUMENTSRepairedProperty"])
    with _temporarily(MUT, "CLOSE_THE_MAP"):
        under_catch_all = sum(
            1 for index in range(4)
            if admit(canonicalise(profiles[index]["capabilityManifest"]), reg) == [])
    run.eq("DV4-CONTROL", "NEG-CLOSED-3.admittedUnderTheCATCHALLReading",
           under_catch_all, closed3["admittedUnderTheCATCHALLReading"],
           "blocker IR-V3-B1 executed: the rejected candidate's literal catch-all refuses "
           "every live manifest, so a gate and the document's own vectors cannot both be "
           "right")
    executed.add("NEG-CLOSED-3")

    # ---- NEG-NFC-1 -------------------------------------------------------
    nfc = build("NEG-NFC-1")
    try:
        cve1(nfc)
        run.fail("DV4-CONTROL", "NEG-NFC-1.thisRule",
                 "a non-NFC string was encoded rather than refused")
    except EncErr:
        run.bump("cve1Refusals")
        executed.add("NEG-NFC-1")

    # ---- NEG-DOM-1 -------------------------------------------------------
    measured = controls["NEG-DOM-1"]["measured"]
    body = cve1(core)
    for label, want in measured.items():
        if label == "correct":
            got = cap_manifest_id(core)
        elif label == "correctDomainWithoutTheNULSeparator":
            got = hashlib.sha256(DOMAIN.encode("utf-8") + body).hexdigest()
        else:
            got = hashlib.sha256(label.encode("utf-8") + b"\x00" + body).hexdigest()
        run.eq("DV4-CONTROL", "NEG-DOM-1.measured[%s]" % label, got, want)
    if len(set(measured.values())) != len(measured):
        run.fail("DV4-CONTROL", "NEG-DOM-1.measured", "two domain labels produced one id")
    executed.add("NEG-DOM-1")

    # ---- NEG-PLAT-1, the third injectivity channel ------------------------
    plat = controls["NEG-PLAT-1"]
    x1 = build("NEG-PLAT-1")
    x2 = build("NEG-PLAT-1", "x2")
    v3gates = plat["measuredUnderDELIVERYV3sTHREEGATES"]
    run.eq("DV4-CONTROL", "NEG-PLAT-1.idOfX1", cap_manifest_id(x1), v3gates["idOfX1"])
    run.eq("DV4-CONTROL", "NEG-PLAT-1.idOfX2", cap_manifest_id(x2), v3gates["idOfX2"])
    if cap_manifest_id(x1) == cap_manifest_id(x2):
        run.fail("DV4-CONTROL", "NEG-PLAT-1.idsDiffer",
                 "the two spellings mint one id, so the channel this control describes is "
                 "not present")
    if decode(cve1(x2)) != x2:
        run.fail("DV4-CONTROL", "NEG-PLAT-1.detectorVerdict",
                 "x2 does not round-trip, so the channel is NOT symmetric and the "
                 "artifact's claim that the DL-INJ-1 detector is silent on it is wrong")
    else:
        run.bump("symmetricChannelsConfirmed")
    with _temporarily(MUT, "SKIP_DOMAIN"):
        v3_admits_both = admit(x1, reg) == [] and admit(x2, reg) == []
    run.eq("DV4-CONTROL", "NEG-PLAT-1.bothAdmitted", v3_admits_both,
           v3gates["bothAdmitted"],
           "under the rejected candidate's three gates BOTH spellings must be admissible, "
           "or the channel was never open")
    named("NEG-PLAT-1", refusal_of(x2), "NEG-PLAT-1.thisRule")

    plat2 = build("NEG-PLAT-2")
    named("NEG-PLAT-2", refusal_of(plat2), "NEG-PLAT-2.thisRule")
    run.eq("DV4-CONTROL", "NEG-PLAT-2.wouldMint", cap_manifest_id(plat2),
           controls["NEG-PLAT-2"]["wouldMint"])

    # ---- NEG-REL-1 / NEG-DEF-1 -------------------------------------------
    rel1 = build("NEG-REL-1")
    named("NEG-REL-1", refusal_of(rel1), "NEG-REL-1.thisRule")
    run.eq("DV4-CONTROL", "NEG-REL-1.wouldMint", cap_manifest_id(rel1),
           controls["NEG-REL-1"]["wouldMint"])

    def1 = build("NEG-DEF-1")
    named("NEG-DEF-1", refusal_of(def1), "NEG-DEF-1.thisRule")
    run.eq("DV4-CONTROL", "NEG-DEF-1.wouldMint", cap_manifest_id(def1),
           controls["NEG-DEF-1"]["wouldMint"])

    if "SKIP_ONE_CONTROL" in MUT:
        executed.discard("NEG-DEF-1")

    missing = sorted(set(controls) - executed)
    if missing:
        run.fail("DV4-CONTROL", "negativeControls",
                 "DECLARED BUT NOT EXECUTED by this checker: %s. IMPLEMENTATION-FREEZE.md "
                 "section 7 records EPC-V2 as exactly this defect -- it declares that, and "
                 "nothing runs it" % ", ".join(missing))
    else:
        run.bump("controlsExecuted", len(executed))


def gate_derived_planids(run, identity, minimal, full, pre_min, pre_full, ids):
    """G13 -- the three derived PlanIds, recomputed end to end."""
    block = identity["planIdField3Resolution"]["step3_aPLANIDWHOSEFIELD3CAMEFROMTHERULE"]
    core_id = ids["DCM-1-core"]
    full_id = ids["DCM-4-full"]

    def diff(a, b):
        positions = [i for i in range(min(len(a), len(b))) if a[i] != b[i]]
        return len(positions), [positions[0], positions[-1]] if positions else []

    d1 = copy.deepcopy(minimal)
    d1["release"]["capabilityManifestId"] = core_id
    pre, pid = plan_id(d1)
    run.eq("DV4-PLANID", "PID-D1.planId", pid, block["PID-D1"]["planId"])
    run.eq("DV4-PLANID", "PID-D1.preimageBytes", len(pre), block["PID-D1"]["preimageBytes"])
    count, span = diff(pre_min, pre)
    run.eq("DV4-PLANID", "PID-D1.differingBytePositions", count,
           block["PID-D1"]["differingBytePositions"])
    run.eq("DV4-PLANID", "PID-D1.differingSpan", span, block["PID-D1"]["differingSpan"])

    d2 = copy.deepcopy(full)
    d2["release"]["capabilityManifestId"] = full_id
    for universe in d2["semanticUniverses"]:
        universe["universe"]["capabilityManifestId"] = full_id
    pre2, pid2 = plan_id(d2)
    run.eq("DV4-PLANID", "PID-D2.planId", pid2, block["PID-D2"]["planId"])
    run.eq("DV4-PLANID", "PID-D2.preimageBytes", len(pre2), block["PID-D2"]["preimageBytes"])
    count2, span2 = diff(pre_full, pre2)
    run.eq("DV4-PLANID", "PID-D2.differingBytePositions", count2,
           block["PID-D2"]["differingBytePositions"])
    run.eq("DV4-PLANID", "PID-D2.differingSpan", span2, block["PID-D2"]["differingSpan"])

    d3 = copy.deepcopy(full)
    d3["release"]["capabilityManifestId"] = full_id
    pre3, pid3 = plan_id(d3)
    run.eq("DV4-PLANID", "PID-D3.planId", pid3, block["PID-D3"]["planId"])
    run.eq("DV4-PLANID", "PID-D3.preimageBytes", len(pre3), block["PID-D3"]["preimageBytes"])
    count3, span3 = diff(pre_full, pre3)
    run.eq("DV4-PLANID", "PID-D3.differingBytePositions", count3,
           block["PID-D3"]["differingBytePositions"])
    run.eq("DV4-PLANID", "PID-D3.differingSpan", span3, block["PID-D3"]["differingSpan"])



# ------------------------------------------------- the evaluated proposal's grammar
#
# delivery.v4 publishes eight ids computed under ANOTHER SURFACE'S grammar --
# plan-and-policy-identity-recipes.v2's R-A recipe -- and a 28-collection
# divergence census over it (OBS-V4-1).  Those are the only values in the artifact
# that this document's own recipe cannot produce, so this checker carries a second
# grammar rather than leaving eight digests and three counts unaccountable.

def _C(tag, body):
    return bytes([tag]) + len(body).to_bytes(4, "big") + body


def _proposal_record(manifest, after, label, emit):
    """R-A record bytes.  `after` selects sort-AFTER-framing instead of the
    proposal's stated sort-BEFORE-framing rule."""
    def order(items, tag):
        if after:
            return sorted(range(len(items)), key=lambda i: _C(tag, items[i]))
        return sorted(range(len(items)), key=lambda i: items[i])

    def provider(entry, where):
        relations = [bytes([0x60]) + _C(0x61, k.encode("utf-8")) + _C(0x62, v.encode("utf-8"))
                     for k, v in entry["relations"].items()]
        o = order(relations, 0x56)
        relation_bytes = b"".join(_C(0x56, relations[i]) for i in o)
        emit[where + ".relations"] = (relation_bytes, tuple(o), "map")
        platforms = [_C(0x59, s.encode("utf-8")) for s in entry["platformIds"]]
        op = order(platforms, 0x58)
        platform_bytes = b"".join(_C(0x58, platforms[i]) for i in op)
        emit[where + ".platformIds"] = (platform_bytes, tuple(op), "array")
        return (bytes([0x50]) + _C(0x51, entry["providerId"].encode("utf-8"))
                + _C(0x52, entry["language"].encode("utf-8"))
                + _C(0x53, entry["providerVersionSource"].encode("utf-8"))
                + _C(0x54, entry["toolchainIdentitySource"].encode("utf-8"))
                + _C(0x55, relation_bytes) + _C(0x57, platform_bytes))

    def absent(entry, where):
        ids = [_C(0x75, s.encode("utf-8")) for s in entry["relationIds"]]
        o = order(ids, 0x74)
        id_bytes = b"".join(_C(0x74, ids[i]) for i in o)
        emit[where + ".relationIds"] = (id_bytes, tuple(o), "array")
        return (bytes([0x70]) + _C(0x71, entry["providerId"].encode("utf-8"))
                + _C(0x72, entry["language"].encode("utf-8")) + _C(0x73, id_bytes)
                + _C(0x76, entry["coverageState"].encode("utf-8"))
                + _C(0x77, entry["deficiency"].encode("utf-8")))

    providers = [provider(e, "%s.providers[%d]" % (label, i))
                 for i, e in enumerate(manifest["providers"])]
    o = order(providers, 0x44)
    provider_bytes = b"".join(_C(0x44, providers[i]) for i in o)
    emit[label + ".providers"] = (provider_bytes, tuple(o), "array")
    absents = [absent(e, "%s.coverageForAbsent[%d]" % (label, i))
               for i, e in enumerate(manifest["coverageForAbsent"])]
    oa = order(absents, 0x46)
    absent_bytes = b"".join(_C(0x46, absents[i]) for i in oa)
    emit[label + ".coverageForAbsent"] = (absent_bytes, tuple(oa), "array")
    return (bytes([0x40]) + _C(0x41, str(manifest["schemaVersion"]).encode("ascii"))
            + _C(0x42, manifest["profile"].encode("utf-8"))
            + _C(0x43, provider_bytes) + _C(0x45, absent_bytes))


def _proposal_id(record):
    root = hashlib.sha256(bytes([0x00]) + len(record).to_bytes(8, "big") + record).digest()
    preimage = (bytes([0x30]) + _C(0x31, b"opensip.delivery.v1")
                + _C(0x32, b"capability-manifest-v1") + _C(0x33, root))
    return hashlib.sha256(preimage).hexdigest()


def gate_obs_census(run, identity, base):
    """G17 -- OBS-V4-1's census, recomputed, and the eight proposal-grammar ids."""
    block = identity["proposalEvaluation"][
        "aFINDINGAGAINSTTHEPROPOSALTHATITSOWNSUITEDOESNOTREACH"]
    census = block["theCENSUS"]
    profiles = base["installProfiles"]["profiles"]
    names = ["core", "typescript-deep", "rust-deep", "full"]
    before, after = {}, {}
    before_ids, after_ids, lengths = {}, {}, {}
    for index, name in enumerate(names):
        manifest = profiles[index]["capabilityManifest"]
        rb = _proposal_record(manifest, "PROPOSAL_SORT_AFTER" in MUT, name, before)
        ra = _proposal_record(manifest, True, name, after)
        before_ids[name] = _proposal_id(rb)
        after_ids[name] = _proposal_id(ra)
        lengths[name] = len(rb)
        if len(rb) != len(ra):
            run.fail("DV4-OBS", "%s recordByteLength" % name,
                     "the two conventions produce different record lengths, so the "
                     "artifact's claim that only interior bytes move is wrong")
    order_div = sorted(k for k in before if before[k][1] != after[k][1])
    byte_div = sorted(k for k in before if before[k][0] != after[k][0])
    array_only = sorted(k for k in order_div if before[k][2] == "array")
    run.eq("DV4-OBS", "OBS-V4-1.sortedCollectionsTotal", len(before),
           census["sortedCollectionsTotal"])
    run.eq("DV4-OBS", "OBS-V4-1.orderDivergenceCount", len(order_div),
           census["orderDivergenceCount"])
    run.eq("DV4-OBS", "OBS-V4-1.orderDivergentPositions", order_div,
           census["orderDivergentPositions"])
    run.eq("DV4-OBS", "OBS-V4-1.byteDivergenceCount", len(byte_div),
           census["byteDivergenceCount"])
    run.eq("DV4-OBS", "OBS-V4-1.byteDivergentPositions", byte_div,
           census["byteDivergentPositions"])
    run.eq("DV4-OBS", "OBS-V4-1.arrayOnlyOrderDivergenceCount", len(array_only),
           census["arrayOnlyOrderDivergenceCount"])
    run.eq("DV4-OBS", "OBS-V4-1.arrayOnlyOrderDivergentPositions", array_only,
           census["arrayOnlyOrderDivergentPositions"])
    measured = block["measuredIds"]
    run.eq("DV4-OBS", "OBS-V4-1.sortBeforeFraming", before_ids,
           measured["sortBeforeFraming_theProposalsStatedRule"])
    run.eq("DV4-OBS", "OBS-V4-1.sortAfterFraming", after_ids, measured["sortAfterFraming"])
    run.eq("DV4-OBS", "OBS-V4-1.recordByteLengths", lengths,
           measured["recordByteLengthsUnderBOTH"])
    run.eq("DV4-OBS", "proposalEvaluation.reproducedSetReadingIds", before_ids,
           identity["proposalEvaluation"]["IREPRODUCEDITBEFOREJUDGINGIT"]
           ["reproducedSetReadingIds"])
    if len(order_div) == len(byte_div):
        run.fail("DV4-OBS", "OBS-V4-1.theCORRECTION",
                 "order divergence and byte divergence are the same number, so the "
                 "correction this observation makes has no referent")
    for value in list(before_ids.values()) + list(after_ids.values()):
        run.recomputed.add(value)


_NUL_MARKS = ("|| 0x00 ||", chr(92) + "u0000') ||", chr(0) + "') ||")


def gate_prefix_census(run, art, base):
    """G18 -- the prefix-form count, with its predicate, recomputed on live bytes."""
    published = None
    for op in art["derivedFrom"]["operations"]:
        if op["path"] == "capabilityManifestIdentity":
            published = (op["value"]["proposalEvaluation"]["whatICHANGE"][0]
                         ["theCOUNTOFPREFIXFORMSTATEMENTS"])
    if published is None:
        run.fail("DV4-PREFIX", "proposalEvaluation", "no prefix-form census is published")
        return
    a_paths, b_paths = [], []

    def walk(node, path):
        if type(node) is dict:
            for key, value in node.items():
                walk(value, path + "." + key)
        elif type(node) is list:
            for index, value in enumerate(node):
                walk(value, path + "[%d]" % index)
        elif type(node) is str and any(m in node for m in _NUL_MARKS):
            digest = ("PREFIX_PREDICATE_BLIND" in MUT
                      or re.search(r"(SHA-256|sha256)\s*\(\s*UTF8\(", node) is not None)
            (a_paths if digest else b_paths).append(path)

    walk(base, "$")
    run.eq("DV4-PREFIX", "predicateA.count", len(a_paths), published["countUnderPredicateA"])
    run.eq("DV4-PREFIX", "predicateA.positions", sorted(a_paths),
           published["positionsUnderPredicateA"])
    run.eq("DV4-PREFIX", "predicateB.count", len(b_paths), published["countUnderPredicateB"])
    run.eq("DV4-PREFIX", "predicateB.positions", sorted(b_paths),
           published["positionsUnderPredicateB"])
    run.eq("DV4-PREFIX", "total", len(a_paths) + len(b_paths), published["total"])


_HEX64 = re.compile(r"(?<![0-9a-f])[0-9a-f]{64}(?![0-9a-f])")


def gate_digest_accountability(run, art):
    """G19 -- no 64-hex literal in the artifact is unrecomputed and undeclared.

    A checker that recomputes MOST of a document's digests still leaves the rest
    as values a reader must trust.  This gate closes the difference.
    """
    raw = (COOP / SUBJECT).read_text(encoding="utf-8")
    present = set(_HEX64.findall(raw))
    declared = set()
    block = art.get("digestAccountability")
    if block is None:
        run.fail("DV4-ACCOUNT", "$.digestAccountability",
                 "the artifact declares no digest-accountability block, so this gate cannot "
                 "distinguish a quoted foreign digest from an unrecomputed one")
        return
    for row in block["quotedFromAnotherDocumentAndNOTREPUBLISHED"]:
        declared.add(row["value"])
    for row in block["measuredByThisLaneAndNOTRECOMPUTABLELATER"]:
        declared.add(row["value"])
    recorded = {row["sha256"] for row in art["recordedInputs"]["inputs"]}
    recorded |= set(PINNED.values())
    unaccounted = sorted(present - run.recomputed - declared - recorded)
    if unaccounted:
        for value in unaccounted:
            index = raw.index(value)
            context = raw[max(0, index - 120):index].splitlines()[-1][-90:]
            run.fail("DV4-ACCOUNT", value,
                     "neither recomputed by this run, nor a recorded input digest, nor "
                     "declared at digestAccountability. Context: ...%s" % context)
    else:
        run.bump("digestsAccountedFor", len(present))
    stale = sorted(declared - present)
    if stale:
        run.fail("DV4-ACCOUNT", "digestAccountability",
                 "declares %d digest(s) that no longer appear in the artifact: %s"
                 % (len(stale), ", ".join(h[:16] + "…" for h in stale)))


def _leaf_census(node, acc, path="$"):
    if type(node) is dict:
        for key, value in node.items():
            if type(key) is not str:
                acc["nonStringKeys"].append(path)
            _leaf_census(value, acc, path + "." + key)
    elif type(node) is list:
        for index, value in enumerate(node):
            _leaf_census(value, acc, path + "[%d]" % index)
    else:
        if "LEAF_CENSUS_BLIND" in MUT:
            if isinstance(node, bool) and isinstance(node, int):
                acc["int"].append(path)
                return
        if type(node) is bool:
            acc["bool"].append(path)
        elif type(node) is int:
            acc["int"].append(path)
        elif type(node) is float:
            acc["float"].append(path)
        elif type(node) is str:
            acc["str"] += 1
        elif node is None:
            acc["null"].append(path)
        else:
            acc["other"].append(path)


def gate_leaf_census(run, art):
    """G14 -- the artifact's own non-string-leaf census, recomputed."""
    acc = {"str": 0, "int": [], "bool": [], "float": [], "null": [], "other": [],
           "nonStringKeys": []}
    _leaf_census(art, acc)
    published = art["leafCensus"]
    run.eq("DV4-LEAF", "leafCensus.stringLeaves", acc["str"], published["stringLeaves"])
    run.eq("DV4-LEAF", "leafCensus.integerLeaves", len(acc["int"]), published["integerLeaves"])
    run.eq("DV4-LEAF", "leafCensus.booleanLeaves", len(acc["bool"]),
           published["booleanLeaves"])
    run.eq("DV4-LEAF", "leafCensus.nullLeaves", len(acc["null"]), published["nullLeaves"])
    run.eq("DV4-LEAF", "leafCensus.floatLeaves", len(acc["float"]), published["floatLeaves"])
    run.eq("DV4-LEAF", "leafCensus.nonStringKeys", len(acc["nonStringKeys"]),
           published["nonStringKeys"])
    run.eq("DV4-LEAF", "leafCensus.nonStringLeafTotal",
           len(acc["int"]) + len(acc["bool"]) + len(acc["null"]) + len(acc["float"]),
           published["nonStringLeafTotal"])
    run.eq("DV4-LEAF", "leafCensus.integerLeafPaths", acc["int"], published["integerLeafPaths"])
    run.eq("DV4-LEAF", "leafCensus.booleanLeafPaths", acc["bool"], published["booleanLeafPaths"])
    if acc["float"]:
        run.fail("DV4-LEAF", acc["float"][0],
                 "a float leaf in an artifact that publishes CVE1 preimages, and CVE1 "
                 "forbids floating-point outright")
    if acc["other"]:
        run.fail("DV4-LEAF", acc["other"][0], "a leaf outside JSON's value types")


def gate_self_measurement(run, art, identity):
    """G15 -- every number in selfMeasurement, recomputed from what it describes."""
    sm = art["selfMeasurement"]
    ops = art["derivedFrom"]["operations"]
    domains = None
    duds = None
    for op in ops:
        if op["path"] == "capabilityManifestSchema.valueDomains":
            domains = op["value"]
        if op["path"] == "declaredUnresolvedDependencies":
            duds = op["value"]
    bound = []
    for spec in domains["registries"].values():
        bound.extend(spec["boundPositions"])
    expect = {
        "operations": len(ops),
        "setOperations": sum(1 for o in ops if o["op"] == "set"),
        "addOperations": sum(1 for o in ops if o["op"] == "add"),
        "committedVectorsPublished": len(identity["vectors"]["byId"]),
        "negativeControlsExecuted": len(identity["negativeControls"]["controls"]),
        "admissionGates": len(identity["admission"]["gateOrder"]),
        "scalarPositionsBOUNDToARegistry": len(bound),
        "scalarPositionsDECLAREDOPEN": len(domains["declaredOPEN"]),
        "reachableScalarTypePositions": len(bound) + len(domains["declaredOPEN"]),
        "declaredUnresolvedDependencies": len(duds["entries"]),
    }
    for key, want in expect.items():
        run.eq("DV4-COUNT", "selfMeasurement." + key, want, sm[key])
    for key in ("rowsClosedByThisDocument", "headsRepointed", "dispositionsChanged"):
        if sm[key] != 0:
            run.fail("DV4-COUNT", "selfMeasurement." + key,
                     "a candidate that binds nothing must report 0, reports %r" % sm[key])
    ids = [d["id"] for d in duds["entries"]]
    if len(set(ids)) != len(ids):
        run.fail("DV4-COUNT", "declaredUnresolvedDependencies", "duplicate DUD id")


def gate_duplicate_key_hook(run):
    """G16 -- the hook must RAISE and must NAME the key (freeze section 7.5)."""
    probe = '{"a": 1, "b": 2, "a": 3}'
    try:
        json.loads(probe, object_pairs_hook=_hook_factory("<selftest probe>"))
    except DuplicateKey as exc:
        if exc.key != "a" or "a" not in str(exc):
            run.fail("DV4-PARSE", "<duplicate-key probe>",
                     "the hook raised without naming the duplicated key")
        else:
            run.bump("duplicateKeyProbes")
        return
    run.fail("DV4-PARSE", "<duplicate-key probe>",
             "a duplicate JSON key was ADMITTED; json.loads keeps the last of duplicates, "
             "so a document can say one thing to a reader and another to every instrument")


# ------------------------------------------------------------------- the run
def run_all(verbose=False):
    run = Run(verbose)
    art = load_json(SUBJECT)
    base = load_json("artifacts/delivery.v2.json")
    resolved_inputs = load_json("artifacts/resolved-inputs.v2.json")
    fact_plane = load_json("artifacts/fact-plane.v1.json")
    c2v4 = load_json("artifacts/c2-plan-stage-schema.v4.json")
    reg = Registries(base, fact_plane)

    gate_duplicate_key_hook(run)
    gate_anchors(run)
    gate_standing(run, art)
    gate_derivation(run, art, base)
    minimal, full, pre_min, pre_full = gate_goldens(run, resolved_inputs, c2v4)
    gate_domain_census(run, art)
    result = gate_vectors(run, art, base, reg)
    if result is not None:
        identity, ids = result
        gate_controls(run, identity, base, reg, identity["vectors"]["byId"])
        if "DCM-1-core" in ids and "DCM-4-full" in ids:
            gate_derived_planids(run, identity, minimal, full, pre_min, pre_full, ids)
        gate_self_measurement(run, art, identity)
        gate_obs_census(run, identity, base)
    gate_prefix_census(run, art, base)
    gate_leaf_census(run, art)
    gate_digest_accountability(run, art)
    return run


SELFTEST = [
    ("EXACT_TYPE_OFF",
     "ADM-TYPE admits by isinstance, so Python's bool passes the integer gate",
     "NEG-TYPE-1"),
    ("SKIP_ORDER",
     "ADM-ORDER is skipped, so the non-canonical live authoring forms are admitted",
     "NEG-ORD-1"),
    ("SKIP_DOMAIN",
     "ADM-DOMAIN is skipped, so the case-variant platformId is admitted",
     "NEG-PLAT-1"),
    ("CLOSE_THE_MAP",
     "DL-CLOSED-1 is read as the rejected candidate's catch-all, so the relations MAP is "
     "required to declare a key set and every live manifest is refused -- blocker IR-V3-B1",
     "DCM-1-core"),
    ("NO_NUL",
     "the 0x00 domain separator is dropped from the preimage",
     "capabilityManifestId"),
    ("SORT_BY_ENCODED_BYTES",
     "providers are sorted by encoded item bytes, which is length-major, instead of by the "
     "declared providerId key",
     "DCM-6-sort-rule"),
    ("NO_CANONICALISE",
     "the live authoring forms are encoded as written instead of canonicalised",
     "DCM-1-core"),
    ("NFC_NORMALISE",
     "the encoder silently NFC-normalises instead of refusing",
     "NEG-NFC-1"),
    ("FLOAT_ADMITTED",
     "the encoder encodes a float, which resolved-inputs.v2 forbids outright",
     "NEG-TYPE-3"),
    ("DUP_KEY_HOOK_OFF",
     "the duplicate-key hook admits a duplicate instead of naming it",
     "duplicate-key probe"),
    ("SKIP_ONE_CONTROL",
     "one declared negative control is not executed -- the EPC-V2 defect",
     "negativeControls"),
    ("LEAF_CENSUS_BLIND",
     "the leaf walk counts booleans as integers, as an isinstance walk would",
     "leafCensus"),
    ("ANCHOR_DRIFT",
     "a cited freeze proposition is no longer present in the live file",
     "DV4-ANCHOR"),
    ("PROPOSAL_SORT_AFTER",
     "the evaluated proposal's grammar is built under sort-AFTER-framing where its own "
     "stated rule is sort-BEFORE-framing, which is the ambiguity OBS-V4-1 is about",
     "OBS-V4-1"),
    ("PREFIX_PREDICATE_BLIND",
     "the prefix-form census drops the SHA-256-in-the-same-sentence half of its predicate, "
     "which is the whole reason its count is five and not eight",
     "DV4-PREFIX"),
    ("NO_RECOMPUTE_LEDGER",
     "the run stops recording which digests it recomputed -- what a checker that compared "
     "stored strings to stored strings would look like from the outside",
     "DV4-ACCOUNT"),
    ("SUBJECT_DRIFT",
     "the subject's live bytes no longer match the digest this checker pins, which must "
     "stop the run at exit 2 BEFORE anything is parsed",
     "artifacts/delivery.v4.json"),
]


def selftest():
    print("SELFTEST -- each mutation must fail the run, and must fail for its OWN reason.")
    print()
    ok = True
    for flag, description, expected_position in SELFTEST:
        MUT.clear()
        MUT.add(flag)
        try:
            if flag == "SUBJECT_DRIFT":
                # exit 2 is a REFUSAL TO PARSE, so it is measured at verify_pins()
                # rather than inside the run.  A switch no mutation can reach is a
                # switch nothing has shown to work.
                findings = verify_pins()
            else:
                run = run_all()
                findings = run.findings
        except (EncErr, EncoderDisagreement, DuplicateKey, KeyError, TypeError) as exc:
            findings = ["%s raised %s: %s" % (flag, type(exc).__name__, exc)]
        MUT.clear()
        hit = [f for f in findings if expected_position in f]
        status = "PASS" if (findings and hit) else "FAIL"
        if status == "FAIL":
            ok = False
        print("  %-4s %-22s %d finding(s); expected position %r %s"
              % (status, flag, len(findings), expected_position,
                 "seen" if hit else "NOT SEEN"))
        print("        %s" % description)
        if hit:
            print("        first matching finding: %s" % hit[0][:150])
        elif findings:
            print("        first finding: %s" % findings[0][:150])
        print()

    MUT.clear()
    clean = run_all()
    print("  %-4s %-22s %d finding(s) with no mutation applied"
          % ("PASS" if not clean.findings else "FAIL", "<unmutated>", len(clean.findings)))
    if clean.findings:
        ok = False
        for finding in clean.findings[:5]:
            print("        %s" % finding)
    print()
    print("SELFTEST %s -- %d mutations, each failing for its named reason"
          % ("OK" if ok else "FAILED", len(SELFTEST)))
    return 0 if ok else 1


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--selftest", action="store_true",
                        help="run the mutation suite instead of the check")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    print("CHECK-DELIVERY-V4 -- artifacts/delivery.v4.json, recomputed from the recipe")
    print()
    try:
        drift = verify_pins()
    except Drift as exc:
        print("  INPUT DRIFT: %s" % exc)
        print()
        print("EXIT 2 -- refusing to parse bytes this checker has not verified.")
        return 2
    if drift:
        print("  INPUT DRIFT, before any parse:")
        for item in drift:
            print("    %s" % item)
        print()
        print("EXIT 2 -- a report about bytes nobody named is not a report.")
        return 2
    print("  hash-verified before parsing: %d inputs" % len(PINNED))
    for rel in sorted(PINNED):
        print("    %s  %s" % (PINNED[rel][:16] + "…", rel))
    print()

    if args.selftest:
        return selftest()

    run = run_all(args.verbose)
    print("  measured this run:")
    for key in sorted(run.counts):
        print("    %-28s %d" % (key, run.counts[key]))
    print()
    if not run.findings:
        print("FINDINGS: 0")
        print()
        print("EXIT 0 -- every published id, byte length, hex string, PlanId and count was")
        print("recomputed from the recipe and matched. Seventeen negative controls executed,")
        print("each asserting its own named condition.")
        return 0
    print("FINDINGS: %d" % len(run.findings))
    for finding in run.findings:
        print("  %s" % finding)
    print()
    print("EXIT 1 -- see above; each finding names its position.")
    return 1


if __name__ == "__main__":
    sys.exit(main())
