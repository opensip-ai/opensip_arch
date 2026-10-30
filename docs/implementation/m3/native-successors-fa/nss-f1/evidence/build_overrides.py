"""NSS-F1: build the exact passage overrides and the handshake successor copies, and check them.

Usage: python3 -I -B build_overrides.py --arch <opensip_arch checkout> --product <opensip checkout>
       [--record-root <another arch worktree holding newly locked successor records>]... [--check]

Every override is insert-only: `after` is `before` with one contiguous insertion. Every `before` is read from the
parent at its pinned bytes. No selector may already be bound by the product design lock. The handshake copies are
the current parent's bytes with exactly the listed textual edits, and must parse to the parent plus exactly the
listed structural edits. Writes overrides.json and the two handshake copies under ../design and ../product, or with
--check compares instead. Reads arch and product files; writes nothing outside nss-f1/.
"""
import argparse
import copy
import hashlib
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
NE = "docs/v2/contracts/product-v1/native-evidence.md"
RCA = "docs/implementation/m3/native-successors-fa/rust-commit-alignment-r2"
ST = RCA + "/design/native/provider-startup.schemas.v1.json"
PST = RCA + "/product/schemas/sources/startup-v1.schema.json"
HS = RCA + "/design/native/provider-handshake.schemas.v1.json"
PHS = RCA + "/product/schemas/sources/handshake-v1.schema.json"
ORDER = "docs/coop/design-corrections/native/typescript-protocol2-order.v1.json"
PINS = {
    NE: (329013, "83b99783893bec4bcca76bc043310e1d33305fc41ef85e012fbcb19e5b222ca0"),
    ST: (34838, "e8b2aae594c9914eda5b9aae9b6bc6e9d85f8d172312ada3f2ca3b0458262b55"),
    PST: (34838, "e8b2aae594c9914eda5b9aae9b6bc6e9d85f8d172312ada3f2ca3b0458262b55"),
    HS: (38182, "1fc57cbc8d71dfae9ec6ce9534415c60e810de5aa39134d95a37209ce2694edb"),
    PHS: (38182, "1fc57cbc8d71dfae9ec6ce9534415c60e810de5aa39134d95a37209ce2694edb"),
    ORDER: (11341, "007ef7affce224c7bac6af3bb7897e86691085e2dd788f4a613e45c1fa5b8bbb"),
}
TOKEN = "native-context-inputs-v1"
SCHEMA_DOC = "native-context-inputs.schemas.v1.json"

# NE line overrides: line -> (anchor inside `before` after which the text is inserted, inserted text).
# anchor None means "at the end of the line".
NE_INSERTS = {
    125: ("is the native semantic-universe identity.",
          " Under the `typescript-semantic` token `native-context-inputs-v1` the payload is `TypeScriptOpenUniverseV3`, "
          "`TypeScriptOpenUniverseV2` plus the native-context inputs carrier (§9.5a)."),
    127: ("No enum member or terminal route is added.",
          " Under the `typescript-semantic` token `native-context-inputs-v1`, `Unavailable` is also lawful in that "
          "interval with `TypeScriptPreAnalyzeInputMismatchV1` (§9.5a), converted identically."),
    1620: (None,
           " On `typescript-semantic` the host's selection reaches the worker on the negotiated `OpenUniverse` carrier of "
           "§9.5a: the entry configuration and the retained layout are digest-bound to the universe and to this context; "
           "the unit root is bound by no digest and is admissible only as the start of TSR-1 R-6's ancestor walks, whose successfully derived "
           "results are context members compared before Analyze (a walk that fails ends in a closed-key refusal), with every other use prohibited (§9.5a). The worker "
           "takes only that selection and re-derives every other member."),
    2853: (None,
           " For `typescript-semantic`, `native-context-inputs-v1` (§9.5a) is a token the Plan needs for every worker."),
    2862: (None,
           " Under `native-context-inputs-v1` the `typescript-semantic` OpenUniverse also carries the native-context "
           "inputs carrier, and the worker checks its digest joins before `UniverseAccepted` (§9.5a)."),
    2953: (None,
           " Under the negotiated token `native-context-inputs-v1` (§9.5a) the inputs of that recomputation arrive on "
           "`OpenUniverse`, and the pre-Analyze `TypeScriptPreAnalyzeInputMismatchV1` carries two cases: (a) a "
           "configuration-graph disagreement after a completed recomputation whose context id equals the Plan-bound one; "
           "(b) a closed-key refusal of the graph or context recomputation, for which no context is completed and no "
           "equality or recomputed id is asserted. A completed recomputation with a differing id remains "
           "`native-context-mismatch`, first in §9.5a's order."),
    3007: (None, "SECTION"),
    3192: (None,
           " Under the `typescript-semantic` token `native-context-inputs-v1` the context's retained preimage bytes also "
           "travel in `nativeContextInputs.context` (§9.5a): digest-bound to this identity, never a second identity."),
    3215: (None,
           " Under the `typescript-semantic` token `native-context-inputs-v1`, `TypeScriptPreAnalyzeInputMismatchV1` "
           "(`native-input-mismatch`, §9.5a) is also admitted in this phase; it is a separate payload with its own "
           "correlation, not another reason of this one."),
}

# JSON Pointer string overrides on both startup copies, and on the order table.
ST_INSERTS = {
    "/x-opensip-startup-law/typescriptOpenUniverse/payload": (
        None, "; under native-context-inputs-v1, TypeScriptOpenUniverseV3 of " + SCHEMA_DOC + " (native-evidence "
        "9.5a; contract successor NSS-F1): TypeScriptOpenUniverseV2 with every member unchanged plus nativeContextInputs"),
    "/x-opensip-startup-law/typescriptOpenUniverse/nativeContext": (
        None, "; under native-context-inputs-v1 the context's retained preimage bytes also travel in "
        "nativeContextInputs.context, digest-bound to that identity and never a second identity (native-evidence 9.5a)"),
    "/x-opensip-startup-law/nativeContextVerified": (
        None, " Under native-context-inputs-v1 (typescript-semantic), equal: true also asserts that the worker's "
        "re-derived configuration graph equals the carried one and that neither recomputation step refused "
        "(native-evidence 9.5a)."),
    "/x-opensip-startup-law/preAnalyzeUnavailable/reason": (
        None, " Under native-context-inputs-v1 (typescript-semantic), the token-gated TypeScriptPreAnalyzeInputMismatchV1 "
        "of " + SCHEMA_DOC + " (reason native-input-mismatch; native-evidence 9.5a) is also admitted in this phase; it "
        "is a separate payload with its own correlation, not another reason of this one, and its host conversion is "
        "this payload's."),
}
ORDER_INSERTS = {
    "/eventObservations/unavailablePayload": (
        "pre-analyze (PreAnalyzeUnavailableV1",
        ", or, under native-context-inputs-v1, TypeScriptPreAnalyzeInputMismatchV1 of " + SCHEMA_DOC +
        "; contract successor NSS-F1"),
}

WIRE_LAW_BLOCK = (
    '    "nativeContextInputs": {\n'
    '      "negotiated": "typescript-semantic only. TypeScriptOpenUniverseV3, and the pre-Analyze payloads '
    'PreAnalyzeUnavailableV1 and TypeScriptPreAnalyzeInputMismatchV1, as published in NSS-F1\'s '
    + SCHEMA_DOC + ', iff native-context-inputs-v1 is in both the Hello and the HelloAck token arrays. '
    'TypeScriptOpenUniverseV3 is TypeScriptOpenUniverseV2 with every member unchanged plus nativeContextInputs.",\n'
    '      "notNegotiated": "provider-startup TypeScriptOpenUniverseV2 and PreAnalyzeUnavailableV1, unchanged.",\n'
    '      "violation": "TypeScriptOpenUniverseV3 or TypeScriptPreAnalyzeInputMismatchV1 without the token, or '
    'TypeScriptOpenUniverseV2 with it, is PROVIDER.PROTOCOL_VIOLATION.",\n'
    '      "planNeed": "native-context-inputs-v1 is not an identity token and does not enlarge the identity token set. '
    'It is a token the Plan needs (native-evidence section 9.1, step 1) for every typescript-semantic worker, because '
    'every such worker owes the native-context recomputation of native-evidence sections 2.4 and 9.5a.",\n'
    '      "majors": "TypeScript major stays 2. The token adds no frame, phase, terminal, limit member or identity '
    'version, and it is independent of target-attribution-v2 and symbol-census-v1. rust-semantic is unaffected."\n'
    '    },\n'
)

HS_TEXT_EDITS = [
    ('        "symbol-census-v1"\n      ],\n      "description": "The typescript-semantic members',
     '        "symbol-census-v1",\n        "' + TOKEN + '"\n      ],\n      "description": "The typescript-semantic members'),
    ('symbol-census-v1 (section 9.8; contract successor FA-2) is also a member, although the registered '
     'native-evidence.schemas.v2.json CapabilityToken does not list it."\n    },\n    "RustCapabilityToken"',
     'symbol-census-v1 (section 9.8; contract successor FA-2) is also a member, although the registered '
     'native-evidence.schemas.v2.json CapabilityToken does not list it. ' + TOKEN + ' (section 9.5a; contract '
     'successor NSS-F1) is also a member, although the registered native-evidence.schemas.v2.json CapabilityToken '
     'does not list it."\n    },\n    "RustCapabilityToken"'),
    ('"TypeScriptCapabilitiesV2": {\n      "type": "array",\n      "minItems": 4,\n      "maxItems": 12,',
     '"TypeScriptCapabilitiesV2": {\n      "type": "array",\n      "minItems": 4,\n      "maxItems": 13,'),
    ('RustCapabilityToken also adds subject-scope-reference-v1, native-evidence section 9.3a)',
     'RustCapabilityToken also adds subject-scope-reference-v1, native-evidence section 9.3a; TypeScriptCapabilityToken '
     'also adds ' + TOKEN + ', native-evidence section 9.5a)'),
    ('    "commitments": {\n', WIRE_LAW_BLOCK + '    "commitments": {\n'),
    ('and of the rust-semantic subject-scope-reference-v1 token of section 9.3a.',
     'and of the rust-semantic subject-scope-reference-v1 token of section 9.3a, and of the typescript-semantic '
     + TOKEN + ' token of section 9.5a.'),
]


def sha(b):
    return hashlib.sha256(b).hexdigest()


def read_pinned(arch, path):
    b = open(os.path.join(arch, path), "rb").read()
    n, h = PINS[path]
    if len(b) != n or sha(b) != h:
        sys.exit(f"parent {path} is not at its pin")
    return b


def insert(before, anchor, text):
    if anchor is None:
        return before + text
    if before.count(anchor) != 1:
        sys.exit("anchor not unique: " + anchor)
    i = before.index(anchor) + len(anchor)
    return before[:i] + text + before[i:]


def insert_only(before, after):
    for i in range(len(before) + 1):
        p, s = before[:i], before[i:]
        if after.startswith(p) and after.endswith(s) and len(after) > len(before):
            return True
    return False


def pointer_get(doc, ptr):
    cur = doc
    for part in ptr.split("/")[1:]:
        cur = cur[part.replace("~1", "/").replace("~0", "~")]
    return cur


def pointer_set(doc, ptr, value):
    parts = ptr.split("/")[1:]
    cur = doc
    for part in parts[:-1]:
        cur = cur[part]
    cur[parts[-1]] = value


def bound_selectors(arch, product, extra_roots=()):
    """Every selector the product lock binds. A record absent from --arch is read from an --record-root, and every
    record must have the bytes the lock pins."""
    lock = json.load(open(os.path.join(product, "design-lock.json")))
    out = set()
    for c in lock["contractSuccessors"]:
        rec = c["record"]
        for root in (arch,) + tuple(extra_roots):
            path = os.path.join(root, rec["path"])
            if os.path.exists(path):
                break
        else:
            sys.exit("successor record not found: " + rec["path"])
        raw = open(path, "rb").read()
        if len(raw) != rec["bytes"] or sha(raw) != rec["sha256"]:
            sys.exit("successor record is not at its locked bytes: " + path)
        s = json.loads(raw)
        for o in s.get("passageOverrides", []):
            out.add((o["parent"]["path"], json.dumps(o["selector"], sort_keys=True)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--arch", required=True)
    ap.add_argument("--product", required=True)
    ap.add_argument("--record-root", action="append", default=[])
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args()
    bound = bound_selectors(a.arch, a.product, a.record_root)
    print("lock successors:", len(json.load(open(os.path.join(a.product, "design-lock.json")))["contractSuccessors"]),
          file=sys.stderr)
    section = open(os.path.join(ROOT, "section-9-5a.md")).read().rstrip("\n")
    overrides = []

    ne_bytes = read_pinned(a.arch, NE)
    ne_lines = ne_bytes.decode("utf-8").splitlines()
    for line, (anchor, text) in sorted(NE_INSERTS.items()):
        before = ne_lines[line - 1]
        after = before + "\n\n" + section if text == "SECTION" else insert(before, anchor, text)
        overrides.append({"parent": {"path": NE, "bytes": PINS[NE][0], "sha256": PINS[NE][1]},
                          "selector": {"line": line}, "before": before, "after": after})

    for path in (ST, PST):
        doc = json.loads(read_pinned(a.arch, path))
        for ptr, (anchor, text) in ST_INSERTS.items():
            before = pointer_get(doc, ptr)
            overrides.append({"parent": {"path": path, "bytes": PINS[path][0], "sha256": PINS[path][1]},
                              "selector": {"jsonPointer": ptr}, "before": before,
                              "after": insert(before, anchor, text)})
    order = json.loads(read_pinned(a.arch, ORDER))
    for ptr, (anchor, text) in ORDER_INSERTS.items():
        before = pointer_get(order, ptr)
        overrides.append({"parent": {"path": ORDER, "bytes": PINS[ORDER][0], "sha256": PINS[ORDER][1]},
                          "selector": {"jsonPointer": ptr}, "before": before, "after": insert(before, anchor, text)})

    for o in overrides:
        key = (o["parent"]["path"], json.dumps(o["selector"], sort_keys=True))
        if key in bound:
            sys.exit(f"selector already bound: {key}")
        if not insert_only(o["before"], o["after"]):
            sys.exit(f"not insert-only: {key}")

    hs = read_pinned(a.arch, HS)
    if read_pinned(a.arch, PHS) != hs:
        sys.exit("handshake parents differ")
    text = hs.decode("utf-8")
    for old, new in HS_TEXT_EDITS:
        if text.count(old) != 1:
            sys.exit("handshake edit anchor not unique: " + old[:60])
        text = text.replace(old, new)
    copy_bytes = text.encode("utf-8")
    parent, child = json.loads(hs), json.loads(copy_bytes)
    want = copy.deepcopy(parent)
    D = want["$defs"]
    D["TypeScriptCapabilityToken"]["enum"].append(TOKEN)
    D["TypeScriptCapabilityToken"]["description"] = child["$defs"]["TypeScriptCapabilityToken"]["description"]
    D["TypeScriptCapabilitiesV2"]["maxItems"] = 13
    want["x-opensip-wire-law"]["supersedes"][3] = child["x-opensip-wire-law"]["supersedes"][3]
    law = {}
    for k, v in want["x-opensip-wire-law"].items():
        if k == "commitments":
            law["nativeContextInputs"] = child["x-opensip-wire-law"]["nativeContextInputs"]
        law[k] = v
    want["x-opensip-wire-law"] = law
    want["description"] = child["description"]
    if want != child or list(child["x-opensip-wire-law"]) != list(law):
        sys.exit("handshake copy is not the parent plus exactly the listed edits")
    for f in ("description",):
        if not insert_only(parent[f], child[f]):
            sys.exit("handshake description edit is not insert-only")
    if D["RustCapabilityToken"] != parent["$defs"]["RustCapabilityToken"]:
        sys.exit("rust token changed")

    out_overrides = json.dumps({"schemaVersion": 1, "standing": "NSS-F1 r1 passage overrides (insert-only), for "
                                "the binding's successor.json. Generated by evidence/build_overrides.py.",
                                "passageOverrides": overrides}, indent=2, ensure_ascii=False) + "\n"
    targets = {
        os.path.join(ROOT, "overrides.json"): out_overrides.encode("utf-8"),
        os.path.join(ROOT, "design/native/provider-handshake.schemas.v1.json"): copy_bytes,
        os.path.join(ROOT, "product/schemas/sources/handshake-v1.schema.json"): copy_bytes,
    }
    report = {"overrides": len(overrides), "neLines": sorted(NE_INSERTS),
              "handshakeCopy": {"bytes": len(copy_bytes), "sha256": sha(copy_bytes)}}
    if a.check:
        bad = [p for p, b in targets.items() if not os.path.exists(p) or open(p, "rb").read() != b]
        print("MATCHES" if not bad else "DIFFERS: " + ", ".join(bad))
        sys.exit(1 if bad else 0)
    for p, b in targets.items():
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "wb").write(b)
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main()
