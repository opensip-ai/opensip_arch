"""Reference controls for the four nonblocking advisories and the accepted V15-ADV-1 wording.

ADV-1  the four representations are TERMINAL; `by-domain` is a selector that resolves through
       x-opensip-digest-domains.byDomain into exactly one of them, and no byDomain row names it.
ADV-2  LogicalPath is $ref-enforced at exactly two fields; the description now says so without
       changing the accepted path set.
ADV-3  the L0 body payload is length-prefixed TWICE (payload_len == raw_byte_len + 4), checked
       against the foundation reference implementation `framed_body_preimage`, and the alternative
       single-prefix reading yields a different bodyIdentity.
ADV-4  covered in probe_capability_manifest_domain_selection.py (platform accounting).
V15-ADV-1  cardinality-first is exact: schema faults still refuse at the schema step for every
       request that reaches it, and an oversized-and-malformed spec refuses on cardinality.

Usage: /tmp/opensip-architecture-review-env/bin/python -I -B probe_advisories.py <work-root>
"""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
import re
import sys
from pathlib import Path

WORK = Path(sys.argv[1]).resolve()
FOUNDATION_DIR = WORK / "docs/coop/design-corrections/foundation"
NATIVE = WORK / "docs/coop/design-corrections/native"
CONTRACTS = WORK / "docs/v2/contracts/product-v1"

spec = importlib.util.spec_from_file_location("nm", NATIVE / "native_evidence_model.v2.py")
N = importlib.util.module_from_spec(spec)
spec.loader.exec_module(N)

IDENTITY_SCHEMAS = json.loads((FOUNDATION_DIR / "identity-schemas.v2.json").read_text(encoding="utf-8"))
IDENTITY_MD = (CONTRACTS / "identity-and-evidence.md").read_text(encoding="utf-8")
NATIVE_MD = (CONTRACTS / "native-evidence.md").read_text(encoding="utf-8")
POLICY = json.loads((WORK / "docs/coop/artifacts/fact-identity-policy.v2.json").read_text(encoding="utf-8"))

# the accepted v15 manifest digest of the inherited historical artifact, as a literal control
ACCEPTED_V15_POLICY_DIGEST = "10055004e6919a55b29c38d9c474857280fbbb6f561dfff6ed88b7e54efbd110"

out = {"probe": "advisory-controls", "checks": [], "failures": []}


def check(name, condition, **detail):
    out["checks"].append({"check": name, "ok": bool(condition), **detail})
    if not condition:
        out["failures"].append(name)


# ============================== ADV-1 =======================================================
TERMINAL = {"raw-artifact", "canonical-record", "h-identity", "capability-manifest-id"}
byDomain = IDENTITY_SCHEMAS["x-opensip-digest-domains"]["byDomain"]
used = {}


def walk(node, path=""):
    if isinstance(node, dict):
        ann = node.get("x-opensip-digest")
        if isinstance(ann, dict) and "representation" in ann:
            used.setdefault(ann["representation"], []).append(path)
        for k, v in node.items():
            walk(v, path + "/" + k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, path + "/" + str(i))


walk(IDENTITY_SCHEMAS)
check("exactly five representation tokens are in use: the four terminal ones plus `by-domain`",
      set(used) == TERMINAL | {"by-domain"}, counts={k: len(v) for k, v in used.items()})
check("`by-domain` appears on exactly the three reference digest fields",
      sorted(p.rsplit("/properties/", 1)[0].rsplit("/", 1)[-1] for p in used.get("by-domain", []))
      == ["FindingEvidenceRef", "ProofInputRef", "Ref"], sites=used.get("by-domain"))
check("every byDomain row resolves to one of the four TERMINAL representations, and none is by-domain",
      all(row["representation"] in TERMINAL for row in byDomain.values()),
      domains=len(byDomain),
      byRepresentation={r: sum(1 for v in byDomain.values() if v["representation"] == r)
                        for r in sorted(TERMINAL)})
check("identity §3 now states that the four are TERMINAL and that by-domain is a selector",
      "closed set of **terminal**" in IDENTITY_MD and "selector, not a fifth terminal" in IDENTITY_MD)

# ============================== ADV-2 =======================================================
refs = []


def walk2(node, path=""):
    if isinstance(node, dict):
        if node.get("$ref", "").endswith("/LogicalPath"):
            refs.append(path)
        for k, v in node.items():
            walk2(v, path + "/" + k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk2(v, path + "/" + str(i))


walk2(IDENTITY_SCHEMAS)
lp = IDENTITY_SCHEMAS["$defs"]["LogicalPath"]
check("LogicalPath is $ref-enforced at exactly the two fields the description now names",
      sorted(refs) == ["/$defs/Blob/properties/path", "/$defs/import-blob/properties/path"],
      refs=sorted(refs))
check("the description no longer claims every identity-bearing path field carries it",
      "every identity-bearing path field now carries it" not in lp["description"]
      and "exactly two fields" in lp["description"])
check("the accepted path set is UNCHANGED: pattern, not, and bounds are byte-identical",
      lp["pattern"] == "^[^/\\\\\\u0000]{1,255}(/[^/\\\\\\u0000]{1,255})*(?![\\s\\S])"
      and lp["not"] == {"pattern": "(^|/)\\.\\.?(/|$)"}
      and lp["minLength"] == 1 and lp["maxLength"] == 4096,
      pattern=lp["pattern"], not_=lp["not"], minLength=lp["minLength"], maxLength=lp["maxLength"])
anchor = IDENTITY_SCHEMAS["$defs"]["fact"]["properties"]["anchors"]["items"]["properties"]["path"]
check("the two join-only path fields are still plain bounded strings (nothing widened or narrowed)",
      "$ref" not in anchor and anchor["type"] == "string" and anchor["maxLength"] == 4096)

# ============================== ADV-3 =======================================================
CHECK_IDENTITY = (FOUNDATION_DIR / "check-identity.py").read_text(encoding="utf-8")
match = re.search(r"def framed_body_preimage\(.*?\n(?:.*?\n)*?            \+len\(payload\)"
                  r"\.to_bytes\(4, ?'big'\)\+payload\)", CHECK_IDENTITY)
check("the foundation reference frame ends with the outer u32be payload length", bool(match))

span = b"a=1\n"
l0_payload = len(span).to_bytes(4, "big") + span
outer_component = len(l0_payload).to_bytes(4, "big") + l0_payload
check("the worked byte example in identity §3 matches the computed bytes",
      "00 00 00 04 61 3d 31 0a" in IDENTITY_MD
      and "00 00 00 08 00 00 00 04 61 3d 31 0a" in IDENTITY_MD
      and l0_payload.hex() == "00000004613d310a"
      and outer_component.hex() == "0000000800000004613d310a",
      l0Payload=l0_payload.hex(), outerComponent=outer_component.hex())
check("payload_len == raw_byte_len + 4 at L0, as the corrected prose states",
      len(l0_payload) == len(span) + 4 and "payload_len == raw_byte_len + 4" in IDENTITY_MD)


def frame(payload, level=b"L0-verbatim", level_version=b"\x11" * 32,
          language_id=b"typescript", language_version=b"\x22" * 32):
    def prefixed(raw):
        assert len(raw) <= 255
        return bytes([len(raw)]) + raw
    return (prefixed(b"opensip.fact-identity.v1") + prefixed(level) + prefixed(level_version)
            + prefixed(language_id) + prefixed(language_version)
            + len(payload).to_bytes(4, "big") + payload)


double = hashlib.sha256(frame(l0_payload)).hexdigest()
single = hashlib.sha256(frame(span)).hexdigest()
check("the two grammatically available readings really do yield different bodyIdentity values",
      double != single, doublePrefixed=double, singlePrefixed=single)
policy_bytes = (WORK / "docs/coop/artifacts/fact-identity-policy.v2.json").read_bytes()
check("the inherited fact-identity-policy.v2 BYTES are untouched by this correction",
      hashlib.sha256(policy_bytes).hexdigest() == ACCEPTED_V15_POLICY_DIGEST,
      digest=hashlib.sha256(policy_bytes).hexdigest(),
      acceptedV15Digest=ACCEPTED_V15_POLICY_DIGEST,
      inheritedL0=POLICY["canonicalisationSchema"]["byteGrammar"]["payloadEncodingByLevel"]["L0-verbatim"])
check("the inherited L0 grammar still says exactly what it always said (quoted, not rewritten)",
      POLICY["canonicalisationSchema"]["byteGrammar"]["payloadEncodingByLevel"]["L0-verbatim"]
      .startswith("u32be raw_byte_len ||"))

# ============================== V15-ADV-1 ===================================================
MATRIX = json.loads((NATIVE / "native-capability-matrix.v2.json").read_text(encoding="utf-8"))
cell = next(c for c in MATRIX["cells"] if c["state"] != "NOT-SELECTED")
row = {"capabilityId": cell["capability"], "languageMode": cell["mode"],
       "workspaceRoot": ".", "required": False}


def spec_of(count, break_schema):
    s = {"schemaVersion": 2,
         "requestedCapabilities": [dict(row, workspaceRoot="u%04d" % i) for i in range(count)],
         "policyPackIds": [], "parameters": []}
    if break_schema:
        del s["schemaVersion"]
    return s


def admit(s):
    try:
        N.admit_analysis_spec(s)
        return {"outcome": "ADMIT"}
    except Exception as exc:
        return {"outcome": type(exc).__name__, "detail": str(exc).splitlines()[0][:160],
                "domainDetail": getattr(exc, "detail", None)}


small_bad = admit(spec_of(10, True))
big_bad = admit(spec_of(1034, True))
big_ok_shape = admit(spec_of(1034, False))
check("control: a small malformed spec refuses at the SCHEMA step",
      small_bad["outcome"] not in ("ADMIT",) and "ScopeRefusal" not in small_bad["outcome"],
      result=small_bad)
check("an oversized AND malformed spec refuses on CARDINALITY (the order is exact, not a claim "
      "that the schema fault is lost)",
      "Scope" in big_bad["outcome"] or "count>limit" in json.dumps(big_bad), result=big_bad)
check("an oversized but well-formed spec refuses the same way",
      "Scope" in big_ok_shape["outcome"] or "count>limit" in json.dumps(big_ok_shape),
      result=big_ok_shape)
check("the two routes differ, which is exactly what the corrected sentence now scopes",
      big_bad["outcome"] != small_bad["outcome"])
check("native §10's sentence is now scoped to requests that reach the schema step",
      "for every request that reaches that step" in NATIVE_MD
      and "cardinality-first" in NATIVE_MD)
check("no bounded-array limit or order statement was changed",
      "`requestedCapabilities` has limit1024" in NATIVE_MD
      and "**Four** fields are bounded this way" in NATIVE_MD
      and "it is never truncated" in NATIVE_MD)
check("retained-record corruption handling is unchanged in the same paragraph",
      "an oversized array there means corruption rather than an oversized request" in NATIVE_MD)

out["ok"] = not out["failures"]
print(json.dumps(out, indent=1))
sys.exit(0 if out["ok"] else 1)
