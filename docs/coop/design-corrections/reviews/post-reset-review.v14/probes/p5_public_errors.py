"""Item 5: the ACTUAL public error surface - guard refusal, key/subject normalization,
host-known origin, D9 derivation, complete failure envelope, and the Unicode boundary."""
import hashlib, json, sys
sys.path.insert(0, "/tmp/opensip-design-corrections/post-reset-review.v14/probes")
from harness import CI, M, C, N, probe, emit

ROOT = "/tmp/opensip-design-corrections/post-reset-review.v14/work"
NDOC = json.load(open(ROOT + "/docs/coop/design-corrections/native/native-evidence.schemas.v2.json"))
REG = NDOC["x-opensip-public-route-registry"]
PUB = json.load(open(ROOT + "/docs/coop/design-corrections/public-detail-registry.v1.json"))
PUBCODES = {r["code"] for r in PUB["records"]} if isinstance(PUB["records"], list) \
           else set(PUB["records"])
WF = json.load(open(ROOT + "/docs/coop/design-corrections/workflows/schemas/common.schema.json"))

def term(k, o=None): return N.public_termination_for(k, o)
def errs(k, o=None): return N.failure_envelope_errors(k, o)

# --- 1. A colon-suffixed internal key is NOT a standalone public code. ---------------------
probe("F0-the-guards-emit-colon-suffixed-internal-keys", "check",
      lambda: N.normalize_internal_key(
          "native.requested-capability-unregistered:made-up")
          == ("native.requested-capability-unregistered", "made-up"))
probe("F1-a-colon-suffixed-internal-key-is-not-itself-a-public-DomainDetailCode", "check",
      lambda: "native.requested-capability-unregistered:made-up" not in PUBCODES
              and "native.requested-capability-unregistered" not in PUBCODES)
probe("F2-negative-an-unregistered-internal-key-refuses-rather-than-passing-through",
      "negative", lambda: term("totally.made.up.key"),
      "native.public-route-key-unregistered")

# --- 2. Origin cannot be laundered. --------------------------------------------------------
probe("F3-negative-an-origin-the-key-cannot-have-refuses", "negative",
      lambda: term("native.release-capability-duplicate", "external-configuration"),
      "native.public-route-origin-not-possible")
probe("F4-negative-an-origin-dependent-key-with-no-origin-refuses", "negative",
      lambda: term("native.requested-capability-unregistered"),
      "native.public-route-origin-required")

# --- 3. The four distinct conditions get four distinct D9 answers. ------------------------
CASES = {
    "user configuration": ("native.requested-capability-unregistered", "external-configuration",
                           "request-rejected", "CONFIG.INVALID"),
    "external/retained bad input": ("native.requested-capability-unregistered",
                                    "externally-supplied-spec", "request-rejected",
                                    "REQUEST.PRECONDITION_FAILED"),
    "impossible requested cell": ("native.requested-capability-mode-not-selected", None,
                                  "request-rejected", "REQUEST.UNSATISFIABLE"),
    "bad authenticated release": ("native.release-capability-duplicate", None,
                                  "request-rejected", "REQUEST.PRECONDITION_FAILED"),
    "producer protocol fault": ("native.coverage-cause-not-for-deficiency", None,
                                "operational-failed", "PROVIDER.PROTOCOL_VIOLATION"),
}
def case_holds(key, origin, cls, code):
    t = term(key, origin)
    return t["class"] == cls and (code is None or t["errorCode"] == code)
for label, (k, o, cls, code) in CASES.items():
    probe("F5-%s-routes-to-%s" % (label.replace(" ", "-").replace("/", "-"), cls), "check",
          lambda k=k, o=o, c=cls, cd=code: case_holds(k, o, c, cd))

probe("F6-the-five-conditions-are-not-collapsed-into-one-code", "check",
      lambda: len({term("native.requested-capability-unregistered",
                        "external-configuration")["errorCode"],
                   term("native.requested-capability-unregistered",
                        "externally-supplied-spec")["errorCode"],
                   term("native.requested-capability-mode-not-selected")["errorCode"],
                   term("native.coverage-cause-not-for-deficiency")["errorCode"],
                   term("native.requested-capability-unregistered",
                        "host-generated-internal-layer")["errorCode"]}) == 5)

# The same key under three different origins must NOT produce one answer - this is the
# origin-dependence the context-free alias map deliberately cannot express.
probe("F6b-one-key-under-three-origins-yields-three-different-classes-or-codes", "check",
      lambda: len({(term("native.requested-capability-unregistered", o)["class"],
                    term("native.requested-capability-unregistered", o)["errorCode"])
                   for o in ("external-configuration", "externally-supplied-spec",
                             "host-generated-internal-layer")}) == 3)

# --- 4. The failure envelope requires NONEMPTY schema-admitted errors, even where
#        StepTermination.domainDetail is lawfully absent.
probe("F7-domainDetail-is-optional-on-StepTermination", "check",
      lambda: "domainDetail" not in WF["$defs"]["StepTermination"].get("required", []))
def every_route_has_nonempty_errors():
    bad = []
    for key, row in REG["keys"].items():
        if row.get("notATermination"): continue
        origins = row["possibleOrigins"] if row["originDependent"] else [None]
        for o in origins:
            e = errs(key, o)
            if not e or not all(d.get("code") in PUBCODES and d.get("subject")
                                and d.get("remedy") for d in e):
                bad.append((key, o, e))
    return not bad, bad
probe("F8-every-registered-route-yields-nonempty-registered-envelope-errors", "check",
      lambda: every_route_has_nonempty_errors()[0])
def route_absent_detail_still_has_errors():
    for key, row in REG["keys"].items():
        if row.get("notATermination"): continue
        origins = row["possibleOrigins"] if row["originDependent"] else [None]
        for o in origins:
            t = term(key, o)
            if "domainDetail" not in t:
                return len(errs(key, o)) >= 1
    return False
probe("F9-a-route-with-NO-termination-detail-still-owes-the-envelope-a-detail", "check",
      route_absent_detail_still_has_errors)
probe("F10-where-a-detail-exists-the-two-surfaces-are-the-SAME-record", "check",
      lambda: (lambda t, e: t["domainDetail"] == e[0])(
          term("native.requested-capability-unregistered", "external-configuration"),
          errs("native.requested-capability-unregistered", "external-configuration")))

# --- 5. The advisory account terminates nothing. -------------------------------------------
probe("F11-the-release-absence-account-is-not-a-termination", "check",
      lambda: term("native.release-capability-undeclared") is None)
probe("F12-negative-and-it-cannot-be-forced-into-a-failure-envelope", "negative",
      lambda: errs("native.release-capability-undeclared"),
      "native.public-route-not-a-failure")

# --- 6. THE UNICODE BOUNDARY: code points for length/slice, raw UTF-8 bytes for SHA-256. --
ASCII_FITS = "a" * 900
NONASCII_FITS = "é" * 900          # 900 code points, 1800 UTF-8 bytes
NONASCII_LONG = "é" * 2000         # 2000 code points, 4000 UTF-8 bytes
COMPOSED = "é" * 600              # 1200 code points, decomposed; NFC would be 600

probe("F13-a-fitting-ascii-subject-is-returned-verbatim", "check",
      lambda: N.bounded_subject(ASCII_FITS) == ASCII_FITS)
probe("F14-a-fitting-NON-ASCII-subject-is-RETAINED-even-though-its-utf8-exceeds-1024",
      "check",
      lambda: len(NONASCII_FITS) <= 1024 < len(NONASCII_FITS.encode("utf-8"))
              and N.bounded_subject(NONASCII_FITS) == NONASCII_FITS)
def elision_shape(raw):
    out = N.bounded_subject(raw)
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    marker = "...#sha256:"
    return (len(out) == 1024 and out.endswith(marker + digest)
            and out.startswith(raw[:1024 - len(marker) - 64]))
probe("F15-an-over-length-non-ascii-subject-elides-to-exactly-1024-CODE-POINTS", "check",
      lambda: elision_shape(NONASCII_LONG))
probe("F16-the-digest-is-over-raw-UTF8-bytes-with-no-added-normalization", "check",
      lambda: N.bounded_subject(COMPOSED).endswith(
          hashlib.sha256(COMPOSED.encode("utf-8")).hexdigest())
          if len(COMPOSED) > 1024 else True)
def nfc_would_differ():
    import unicodedata
    nfc = unicodedata.normalize("NFC", COMPOSED)
    return (nfc != COMPOSED
            and hashlib.sha256(nfc.encode("utf-8")).hexdigest()
                != hashlib.sha256(COMPOSED.encode("utf-8")).hexdigest()
            and N.bounded_subject(COMPOSED).endswith(
                hashlib.sha256(COMPOSED.encode("utf-8")).hexdigest()))
probe("F17-a-COMPOSED-vs-DECOMPOSED-string-is-not-silently-normalized", "check",
      nfc_would_differ)
probe("F18-two-distinct-over-length-values-elide-to-distinct-subjects", "check",
      lambda: N.bounded_subject("é" * 2000 + "A")
              != N.bounded_subject("é" * 2000 + "B"))
probe("F19-the-registered-key-survives-elision-verbatim", "check",
      lambda: N.bounded_subject("native.requested-capability-unregistered:" + "é" * 3000)
              .startswith("native.requested-capability-unregistered:"))

emit("/tmp/opensip-design-corrections/post-reset-review.v14/evidence/probe-public-errors.json",
     {"registeredRouteKeys": sorted(REG["keys"]),
      "envelopeErrorScan": every_route_has_nonempty_errors()[1]})
