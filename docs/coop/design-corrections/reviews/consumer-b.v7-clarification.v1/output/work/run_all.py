"""Execute every blind-consumer-B v7 vector and emit machine-readable results.

Outputs (under output/):
  vectors/<run>.objects.json   typed identity -> {domain, descriptor}
  vectors/<run>.blobs.json     digest -> base64 of the EXACT retained bytes
  vector-results.json          every vector, its measured result and its checks
"""

import base64
import hashlib
import json
import os
import sys
import unicodedata

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import oslib as O                      # noqa: E402
import graph as G                      # noqa: E402
import build as B                      # noqa: E402
import vec_ts, vec_rust, vec_syntax    # noqa: E402
import vec_public as V                 # noqa: E402
import vec_authz as A                  # noqa: E402
import vec_selfcheck as SC             # noqa: E402
import vec_repair_clarify as RC        # noqa: E402
import vec_bounds_clarify as BC        # noqa: E402
import vec_scope_audit as SA           # noqa: E402
from oslib import C, H, sha256hex, raw_digest, Refused   # noqa: E402

OUT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
VEC = os.path.join(OUT, "vectors")
os.makedirs(VEC, exist_ok=True)

RESULTS = {"tool": "blind-consumer-b.v7 independent reference",
           "pass": "CLARIFICATION v1 (post-review, after root feedback)",
           "subjectSha256Manifest": "consumer-input-manifest.json (verified)"}


# ---------------------------------------------------------------------------
def export(name, kit, run_id):
    objects = {}
    for key, desc in sorted(kit.w.objects.items()):
        if key.startswith("sha256:"):
            hx = key.split(":", 1)[1]
            dom = kit.w.frames[hx][0]
        else:
            dom = {v: k for k, v in O.IDENTITY_PREFIX.items()}[key.split(":", 1)[0]]
        objects[key] = {"domain": dom, "descriptor": desc,
                        "hDigest": H(dom, desc)}
    blobs = {d: base64.b64encode(b).decode("ascii")
             for d, b in sorted(kit.w.cas.items())}
    with open(os.path.join(VEC, name + ".objects.json"), "w") as f:
        json.dump({"runId": run_id, "projectId": kit.w.projectId,
                   "objects": objects}, f, indent=1, sort_keys=True)
    with open(os.path.join(VEC, name + ".blobs.json"), "w") as f:
        json.dump({"runId": run_id, "blobs": blobs}, f, indent=1, sort_keys=True)
    return {"objectCount": len(objects), "blobCount": len(blobs),
            "totalBlobBytes": sum(len(b) for b in kit.w.cas.values())}


def run_closure(kit, run_id):
    c = G.Closure(kit.w)
    errs = c.close_run(run_id)
    return {"checks": c.checks, "errors": errs, "admitted": not errs,
            "objectAdmissionCoverage": getattr(c, "objectAdmissionCoverage", None)}


# ---------------------------------------------------------------------------
# A. canonical / lexical / identity helper vectors
# ---------------------------------------------------------------------------
def helper_vectors():
    out = {}
    # A1 canonical encoder, independently chosen
    cases = [
        ("empty-object", {}, b"{}"),
        ("key-byte-order", {"b": 1, "a": 2, "é": 3, "Z": 4},
         '{"Z":4,"a":2,"b":1,"é":3}'.encode("utf-8")),
        ("non-bmp-key-order", {"\U0001F600": 1, "�": 2},
         '{"�":2,"\U0001F600":1}'.encode("utf-8")),
        ("arrays-keep-admitted-order", {"a": [3, 1, 2]}, b'{"a":[3,1,2]}'),
        ("control-escapes", {"s": "a\u0000b\u0007c\td\ne"},
         b'{"s":"a\\u0000b\\u0007c\\td\\ne"}'),
        ("u007f-and-u2028-unescaped", {"s": "\u007f\u2028"},
         '{"s":"\u007f\u2028"}'.encode("utf-8")),
        ("slash-not-escaped", {"p": "a/b"}, b'{"p":"a/b"}'),
        ("no-unicode-normalization",
         {"nfc": "é", "nfd": "é"},
         '{"nfc":"é","nfd":"é"}'.encode("utf-8")),
        ("integer-bounds", {"lo": -(2 ** 63), "hi": 2 ** 64 - 1},
         b'{"hi":18446744073709551615,"lo":-9223372036854775808}'),
    ]
    out["canonicalEncoder"] = []
    for label, value, expect in cases:
        got = C(value)
        out["canonicalEncoder"].append(
            {"case": label, "canonicalBytes": got.decode("utf-8"),
             "matchesIndependentlyHandSpelledBytes": got == expect,
             "sha256": sha256hex(got)})
    # NFC vs NFD are DIFFERENT canonical bytes and therefore different digests
    out["nfcNfdDistinct"] = (raw_digest({"s": "é"})
                             != raw_digest({"s": "é"}))

    # A2 H identity, hand-spelled frame
    d, x = "subject-scope", {"schemaVersion": 2}
    frame = O.h_frame(d, x)
    manual = (b"opensip.product.v1\x00" + d.encode() + b"\x00"
              + len(C(x)).to_bytes(8, "big") + C(x))
    out["hIdentity"] = {"domain": d, "canonicalBytes": C(x).decode(),
                        "frameHex": frame.hex(),
                        "frameEqualsHandSpelled": frame == manual,
                        "H": H(d, x),
                        "HIsNotRawSha256OfPayload": H(d, x) != sha256hex(C(x)),
                        "identity": O.identity(d, x)}

    # A3 raw-input LEXICAL admission, exercised on BYTES (not parsed objects)
    lex = []
    for label, raw in [
            ("duplicate-key", b'{"a":1,"a":2}'),
            ("float-spelled-integer", b'{"schemaVersion":1.0}'),
            ("exponent-spelled-integer", b'{"schemaVersion":1e0}'),
            ("uppercase-exponent", b'{"schemaVersion":1E0}'),
            ("high-precision-float", b'{"n":1.0000000000000001}'),
            ("nine-quadrillion-point-one", b'{"n":9007199254740991.1}'),
            ("negative-zero", b'{"n":-0}'),
            ("nonfinite-nan", b'{"n":NaN}'),
            ("nonfinite-infinity", b'{"n":Infinity}'),
            ("integer-above-u64", b'{"n":18446744073709551616}'),
            ("integer-below-i64", b'{"n":-9223372036854775809}'),
            ("lone-surrogate", b'{"s":"\\ud800"}'),
            ("malformed-utf8", b'{"s":"\xff\xfe"}'),
            ("raw-control-in-string", b'{"s":"a\nb"}'),
            ("trailing-bytes", b'{}{}'),
            ("depth-33", b"[" * 33 + b"]" * 33),
    ]:
        try:
            parse = O.parse_exact(raw)
            lex.append({"case": label, "admitted": True, "value": repr(parse)})
        except Refused as r:
            lex.append({"case": label, "admitted": False, "refusal": r.code,
                        "detail": r.detail})
    for label, raw in [("ordinary-integer", b'{"schemaVersion":2}'),
                       ("escaped-newline-in-text", b'{"s":"a\\nb"}'),
                       ("depth-32", b"[" * 32 + b"]" * 32),
                       ("surrogate-pair", b'{"s":"\\ud83d\\ude00"}')]:
        try:
            v = O.parse_exact(raw)
            lex.append({"case": label, "admitted": True, "value": repr(v)})
        except Refused as r:
            lex.append({"case": label, "admitted": False, "refusal": r.code})
    out["rawInputLexicalAdmission"] = lex

    # A4 already-DECODED values: an integer field cannot be satisfied by a bool
    #     or a float, and a numeric string is not a number.  This is the
    #     SEPARATE gate; the schema layer alone does not decide it.
    decoded = []
    for label, value, ok_int in [("python-bool-true", True, False),
                                 ("python-float-1.0", 1.0, False),
                                 ("numeric-string", "1", False),
                                 ("python-int-1", 1, True)]:
        exact = (type(value) is int and type(value) is not bool)
        try:
            enc = C({"schemaVersion": value})
            enc_ok = True
        except Refused as r:
            enc, enc_ok = r.code, False
        # what a JSON Schema `const: 1` alone would say
        schema_says = O.validate("identity", "#/$defs/snapshot",
                                 {"schemaVersion": value}) == [] or None
        decoded.append({"case": label,
                        "exactIntegerGateAdmits": exact,
                        "expectedAdmit": ok_int,
                        "gateAgrees": exact == ok_int,
                        "canonicalEncoderResult":
                            enc.decode() if enc_ok else enc})
    out["decodedValueExactTypeGate"] = decoded

    # A5 end-anchored identifier grammars: a trailing newline is malformed
    import re
    exec_pat = re.compile(r"^exec1_[0-9a-f]{32}(?![\s\S])")
    bare_pat = re.compile(r"^exec1_[0-9a-f]{32}$")
    val = "exec1_" + "0" * 32 + "\n"
    out["endAnchor"] = {
        "value": repr(val),
        "productSuccessorGrammarAdmits": bool(exec_pat.match(val)),
        "inheritedBareDollarAdmits": bool(bare_pat.match(val)),
        "schemaRefuses": O.validate("common", "#/$defs/ExecutionId", val) != []}
    return out


# ---------------------------------------------------------------------------
# B. capability manifest admission (independently chosen descriptors)
# ---------------------------------------------------------------------------
def capability_manifest_vectors():
    out = {}
    base = {"schemaVersion": 1, "profile": "default",
            "providers": [
                {"providerId": "rust-semantic", "language": "rust",
                 "providerVersionSource": "signed-closure-manifest",
                 "toolchainIdentitySource": "native-context-v2",
                 "relations": {"clones": "normalized-body-hash",
                               "unresolved-edge": "observed"},
                 "platformIds": ["linux-aarch64-gnu", "macos-aarch64"]},
                {"providerId": "typescript-semantic", "language": "typescript",
                 "providerVersionSource": "signed-closure-manifest",
                 "toolchainIdentitySource": "native-context-v2",
                 "relations": {"file": "enumerated", "imports": "resolved-target"},
                 "platformIds": ["macos-aarch64"]}],
            "coverageForAbsent": [
                {"providerId": "syntax-all", "language": "*",
                 "relationIds": ["references", "types"],
                 "coverageState": "unavailable",
                 "deficiency": "language-tier-unsupported"}]}
    b = O.cve1(base)
    out["positive"] = {
        "descriptor": base,
        "violations": O.admit_capability_manifest(base),
        "committedByteLength": len(b),
        "committedBytesSha256": sha256hex(b),
        "capabilityManifestId": O.capability_manifest_id(b),
        "decodeEncodeRoundTripsLiterally": O.cve1(O.cve1_decode(b)) == b,
        "committedBytesHexHead": b.hex()[:96]}

    negatives = {}

    def neg(label, mutate):
        m = json.loads(json.dumps(base))
        mutate(m)
        try:
            enc = O.cve1(m)
            enc_id = O.capability_manifest_id(enc)
            enc_err = None
        except Refused as r:
            enc, enc_id, enc_err = None, None, r.code
        negatives[label] = {
            "gateViolations": O.admit_capability_manifest(m),
            "cve1Refusal": enc_err,
            "wouldMintIfGatesSkipped": enc_id,
            "differsFromPositive": enc_id != out["positive"]["capabilityManifestId"]}

    # ADM-TYPE: CVE1 is TOTAL on booleans and strings; only the gate refuses.
    neg("ADM-TYPE:schemaVersion-true",
        lambda m: m.__setitem__("schemaVersion", True))
    neg("ADM-TYPE:schemaVersion-string",
        lambda m: m.__setitem__("schemaVersion", "1"))
    # ADM-CLOSED
    neg("ADM-CLOSED:undeclared-key",
        lambda m: m["providers"][0].__setitem__("extra", "x"))
    neg("ADM-CLOSED:missing-key",
        lambda m: m["providers"][0].pop("language"))
    # ADM-DOMAIN
    neg("ADM-DOMAIN:platform-case-variant",
        lambda m: m["providers"][1].__setitem__("platformIds", ["MACOS-AARCH64"]))
    neg("ADM-DOMAIN:relation-not-registered",
        lambda m: m["providers"][0]["relations"].__setitem__("made-up", "observed"))
    neg("ADM-DOMAIN:rung-of-another-relation",
        lambda m: m["providers"][0]["relations"].__setitem__("clones",
                                                             "resolved-callee"))
    neg("ADM-DOMAIN:deficiency-not-registered",
        lambda m: m["coverageForAbsent"][0].__setitem__("deficiency",
                                                        "resolution-incomplete"))
    # ADM-ORDER
    neg("ADM-ORDER:providers-unsorted",
        lambda m: m.__setitem__("providers", list(reversed(m["providers"]))))
    neg("ADM-ORDER:platformIds-unsorted",
        lambda m: m["providers"][0].__setitem__(
            "platformIds", ["macos-aarch64", "linux-aarch64-gnu"]))
    neg("ADM-ORDER:duplicate-platformId",
        lambda m: m["providers"][1].__setitem__("platformIds",
                                                ["macos-aarch64", "macos-aarch64"]))
    out["negatives"] = negatives

    # the thirteenth relation IS expressible under the successor registry and
    # was NOT under the inherited twelve-member domain
    inherited12 = set(O.doc("delivery")["derivedFrom"]["operations"][17]["value"]
                      ["valueDomains"]["registries"]
                      ["fact-plane.v1#relationRegistry.relations"]["members"])
    successor13 = set(O.cm_domains()["registries"]["RELATION-DOMAIN-V2"]["members"])
    out["relationDomainSuccessor"] = {
        "inheritedMemberCount": len(inherited12),
        "successorMemberCount": len(successor13),
        "added": sorted(successor13 - inherited12),
        "unresolvedEdgeWasInexpressibleBefore":
            "unresolved-edge" not in inherited12}
    # the ladder mirror is drift-checked EXACTLY AND IN ORDER
    mirror = O.cm_domains()["registries"]["RELATION-LADDER-DOMAIN-V2"]["ladders"]
    authority = {r: G.RELATIONS[r]["ladder"] for r in G.RELATIONS}
    out["ladderMirrorDriftCheck"] = {
        "equalAndInOrder": mirror == authority,
        "differences": {k: (mirror.get(k), authority.get(k))
                        for k in set(mirror) | set(authority)
                        if mirror.get(k) != authority.get(k)}}

    # A CROSS-CHECK ONLY, clearly separated from my own chosen vectors: my
    # independently written CVE1/id/gates reproduce the retained normative
    # vectors of delivery.v4 exactly.
    cross = {}
    for vid, vec in O.doc("delivery")["derivedFrom"]["operations"][17][
            "value"]["vectors"]["byId"].items():
        cb = bytes.fromhex(vec["committedBytesHex"])
        dec = O.cve1_decode(cb)
        cross[vid] = {"idReproduced":
                          O.capability_manifest_id(cb) == vec["capabilityManifestId"],
                      "reEncodesLiterally": O.cve1(dec) == cb,
                      "gatesAdmit": O.admit_capability_manifest(dec) == []}
    out["_implementationCrossCheckAgainstRetainedNormativeVectors"] = cross
    return out


# ---------------------------------------------------------------------------
def main():
    R = RESULTS
    R["helpers"] = helper_vectors()
    R["capabilityManifest"] = capability_manifest_vectors()

    runs = {}
    # ---- RUN-TS -----------------------------------------------------------
    ts = vec_ts.build()
    runs["RUN-TS"] = dict(run_closure(ts["kit"], ts["run"]),
                          runId=ts["run"], planId=ts["plan"],
                          snapshotId=ts["snapshot"],
                          contexts=ts["contexts"], universes=ts["universes"],
                          bodyIdentities=ts["bodyIdentities"],
                          bodyLanguages=ts["bodyLanguages"],
                          capabilityManifestId=ts["capabilityManifestId"],
                          export=export("RUN-TS", ts["kit"], ts["run"]))
    runs["RUN-TS"]["bodyLanguageVersions"] = {
        k: v for k, v in ts["bodyLanguageVersions"].items()}

    ts_negs = {}
    for m in ["stdlib-inventory-incomplete", "compiler-version-not-from-manifest",
              "lockfile-outside-snapshot", "config-node-kind-relabelled",
              "plan-budget-contradicts-config", "file-payload-digest-wrong",
              "inventory-fact-carries-an-anchor", "unanchored-code-fact",
              "rung-of-another-relation", "totality-omits-an-inventoried-path",
              "partition-overlap", "plan-omits-a-retained-context",
              "raw-payload-offered-as-an-h-identity", "altered-frame",
              "missing-preimage", "unregistered-h-domain",
              "unregistered-h-domain-in-plan",
              "clone-level-specification-not-retained",
              # CLARIFICATION v1 discriminating negatives for the two laws the
              # ORIGINAL closure did not enforce
              "finding-evidence-refs-unordered",
              "finding-cites-a-fact-outside-the-evaluated-view",
              "finding-parameter-message-code-mismatch"]:
        r = vec_ts.build(m)
        res = run_closure(r["kit"], r["run"])
        ts_negs[m] = {"refused": bool(res["errors"]),
                      "firstObservedRefusal": res["errors"][0] if res["errors"] else None,
                      "allRefusals": res["errors"], "checks": res["checks"]}
    runs["RUN-TS"]["negatives"] = ts_negs

    # ---- RUN-RS -----------------------------------------------------------
    for sel in ("A", "A2", "B"):
        rs = vec_rust.build(sel)
        name = "RUN-RS-" + sel
        runs[name] = dict(run_closure(rs["kit"], rs["run"]),
                          runId=rs["run"], universe=rs["universe"],
                          context=rs["context"], selection=sel,
                          ownershipId=rs["ownership"],
                          dialects=rs["dialects"],
                          bodyIdentities=rs["bodyIdentities"],
                          units=rs["units"],
                          capabilityManifestId=rs["capabilityManifestId"],
                          export=export(name, rs["kit"], rs["run"]))
    # POSITIVE controls: a scope that cannot determine a body dialect and
    # DISCLOSES it correctly closes an authoritative indeterminate Run.
    for sel, m, label in [("A", "partial-enumeration",
                           "RUN-RS-PARTIAL-ENUMERATION-DISCLOSED"),
                          ("A", "no-ownership",
                           "RUN-RS-NO-OWNERSHIP-DISCLOSED")]:
        rs = vec_rust.build(sel, m)
        runs[label] = dict(run_closure(rs["kit"], rs["run"]),
                           runId=rs["run"], universe=rs["universe"],
                           selection=sel, dialects=rs["dialects"],
                           bodyIdentities=rs["bodyIdentities"],
                           note="empty clones view; Coverage carries the "
                                "incompleteness; predicate and seal indeterminate",
                           export=export(label, rs["kit"], rs["run"]))
    rs_negs = {}
    for sel, m in [("AMB", ""),
                   ("A", "partial-enumeration-false-complete"),
                   ("A", "projection-digest-mismatch"), ("A", "hidden-context")]:
        r = vec_rust.build(sel, m)
        res = run_closure(r["kit"], r["run"])
        rs_negs[(m or "ambiguous-selection-claiming-complete") +
                ("" if m else " [selection=AMB]")] = {
                    "refused": bool(res["errors"]),
                      "firstObservedRefusal":
                          res["errors"][0] if res["errors"] else None,
                      "allRefusals": res["errors"], "checks": res["checks"],
                      "dialects": r["dialects"],
                      "bodyIdentities": r["bodyIdentities"]}
    runs["RUN-RS-A"]["negatives"] = rs_negs
    # the two required identity properties
    runs["_rustIdentityProperties"] = {
        "sameFileTwoSelectedEditionsTwoBodyIdentities":
            runs["RUN-RS-A"]["bodyIdentities"]["shared/dual.rs"]
            != runs["RUN-RS-B"]["bodyIdentities"]["shared/dual.rs"],
        "selectionChangeWithoutDialectChangeKeepsBodyIdentity":
            runs["RUN-RS-A"]["bodyIdentities"] == runs["RUN-RS-A2"]["bodyIdentities"],
        "selectionChangeChangesTheUniverse":
            runs["RUN-RS-A"]["universe"] != runs["RUN-RS-A2"]["universe"],
        "mixedEditionBodiesCloseInOneUniverse":
            sorted({json.dumps(d) for d in runs["RUN-RS-A"]["dialects"].values()})}

    # ---- SYNTAX -----------------------------------------------------------
    for kind in ("code", "data"):
        sy = vec_syntax.build(kind)
        name = "RUN-SYN-" + kind.upper()
        runs[name] = dict(run_closure(sy["kit"], sy["run"]),
                          runId=sy["run"], universe=sy["universe"],
                          context=sy["context"],
                          bodyIdentities=sy["bodyIdentities"],
                          inventory=sy["inventory"],
                          capabilityManifestId=sy["capabilityManifestId"],
                          export=export(name, sy["kit"], sy["run"]))
    syn_negs = {}
    for kind, m in [("code", "markdown-anchored-code-fact"),
                    ("code", "false-complete-on-unsupported-scope"),
                    ("data", "false-complete-on-unsupported-scope"),
                    ("code", "data-grammar-claims-code"),
                    ("code", "select-a-grammar-not-in-the-bundle"),
                    ("code", "grammar-version-not-from-manifest"),
                    ("code", "hidden-context"),
                    # CLARIFICATION v1 discriminating negatives for native S1.2
                    # tree MEMBERSHIP (not mere CAS retention)
                    ("code", "grammar-definition-outside-the-closure-tree"),
                    ("code", "grammar-bundle-manifest-outside-the-closure-tree"),
                    ("code", "normalizer-spec-outside-the-closure-tree"),
                    ("data", "grammar-definition-outside-the-closure-tree")]:
        r = vec_syntax.build(kind, m)
        res = run_closure(r["kit"], r["run"])
        syn_negs[kind + "/" + m] = {
            "refused": bool(res["errors"]),
            "firstObservedRefusal": res["errors"][0] if res["errors"] else None,
            "allRefusals": res["errors"], "checks": res["checks"]}
    runs["RUN-SYN-CODE"]["negatives"] = syn_negs
    runs["_grammarVersusCompilerBodyIdentity"] = {
        "sameBytes": True,
        "typescriptEngineJavascriptBody":
            runs["RUN-TS"]["bodyIdentities"]["js-b.js@L0"],
        "grammarOnlyJavascriptBody":
            runs["RUN-SYN-CODE"]["bodyIdentities"]["lib/util.js@L0"],
        "identitiesDiffer":
            runs["RUN-TS"]["bodyIdentities"]["js-b.js@L0"]
            != runs["RUN-SYN-CODE"]["bodyIdentities"]["lib/util.js@L0"],
        "bothCarryLanguageIdJavascript":
            runs["RUN-TS"]["bodyLanguages"]["src/b.js"] == "javascript"
            and runs["RUN-SYN-CODE"]["bodyIdentities"]["_languageId"] == "javascript"}
    R["runs"] = runs

    # ---- public / workflow ------------------------------------------------
    pub = {}
    pub["capabilityAvailability"] = V.build_availability_vectors()
    for k in ("singleStep", "multiStep", "emptyEntry", "noSelection"):
        pub["capabilityAvailability"][k + "SchemaErrors"] = O.validate(
            "common", "#/$defs/CapabilityAvailabilityV1",
            pub["capabilityAvailability"][k])
    fe = V.failure_envelopes()
    pub["failureEnvelopes"] = {}
    for k, v in fe.items():
        if k.startswith("_"):
            pub["failureEnvelopes"][k] = v
            continue
        pub["failureEnvelopes"][k] = {
            "envelope": v,
            "schemaErrors": O.validate("command-envelope", "#", v)}
    pp = V.pinned_purge_refusal(
        runs["RUN-TS"]["runId"],
        [{"pinId": "baseline.main", "kind": "baseline"},
         {"pinId": "repair.plan-7", "kind": "repair-prerequisite"},
         {"pinId": "export.q3", "kind": "backup-export"}])
    pub["pinnedPurgeRefusal"] = {"envelope": pp,
                                 "schemaErrors": O.validate("command-envelope",
                                                            "#", pp)}
    pub["mutationKeys"] = V.mutation_keys()
    cmp_ = V.comparison_scope_axis()
    pub["scopePolicyAxis"] = {
        "planA": cmp_["planA"], "planB": cmp_["planB"],
        "plansDiffer": cmp_["plansDiffer"],
        "scopeDocumentA": cmp_["scopeDocumentA"],
        "scopeDocumentB": cmp_["scopeDocumentB"],
        "parameterA": cmp_["parameterA"], "parameterB": cmp_["parameterB"],
        "registeredParameterDocumentDigest": V.SCOPE_DOC_SCHEMA_DIGEST,
        "foundationScopeDescriptorDigestUnchanged":
            cmp_["foundationScopeDescriptorDigest"],
        "comparisonSchemaErrors": O.validate("comparison-result", "#",
                                             cmp_["comparison"]),
        "comparisonResultId": cmp_["comparison"]["comparisonResultId"]}
    pub["repair"] = V.build_repair_vectors()
    pub["relationRungTable"] = V.min_resolution_table()
    pub["minResolutionPredicates"] = V.min_resolution_predicates()
    pub["d9Extension"] = V.d9_extension_check()
    pub["authorization"] = A.build_authorization_vectors()
    pub["comparisonCases"] = A.build_comparison_vectors()
    pub["purgeAndReplay"] = A.purge_and_replay()
    pub["commandInventoryProjection"] = {
        name: {"requestClass": COM["requestClass"], "steps": COM["steps"],
               "formats": COM["formats"], "parityFields": COM["parityFields"],
               "carriesCapabilityAvailability":
                   "capability-availability" in COM["parityFields"]}
        for name, COM in sorted(V.COMMANDS.items())
        if COM.get("requestClass") == "analysis"
        or name in ("purge", "import", "doctor")}
    R["public"] = pub

    # native dependency / configuration H PREIMAGES, reconstructed from the
    # normative recipes and shown as exact bytes.
    rs = vec_rust.build("A")
    w = rs["kit"].w
    preimages = {}
    for hx, (dom, desc) in sorted(w.frames.items()):
        if dom.startswith("native.") and dom not in (
                "native.semantic-universe.rust.v2",):
            preimages[dom] = {
                "identityBareHex": hx,
                "sha256TextForm": "sha256:" + hx,
                "canonicalPayloadBytes": C(desc).decode("utf-8")[:400],
                "canonicalPayloadLength": len(C(desc)),
                "framePrefixHex": O.h_frame(dom, desc)[:64].hex(),
                "frameLength": len(O.h_frame(dom, desc)),
                "recomputes": H(dom, desc) == hx,
                "rawSha256OfPayloadDiffers": sha256hex(C(desc)) != hx}
    R["nativeHPreimages"] = preimages

    # ---- self-checks of laws the contracts state about their own documents
    sc = SC.build()
    sc["cardinalityBoundaries"] = SC.cardinality_boundaries()
    # the declared-order admission layer is LOAD-BEARING: JSON Schema alone
    # admits a reversed canonical-set.
    tsx = vec_ts.build()
    any_scope = max((k for k in tsx["kit"].w.objects if k.startswith("scope2:")),
                    key=lambda k: len(tsx["kit"].w.objects[k]["subjects"]))
    reversed_scope = dict(tsx["kit"].w.objects[any_scope])
    reversed_scope["subjects"] = list(reversed(reversed_scope["subjects"]))
    sc["orderAdmissionIsLoadBearing"] = {
        "jsonSchemaAlone": O.validate("identity", "#/$defs/subject-scope",
                                      reversed_scope),
        "declaredOrderAdmission": O.admit_ordered(
            "identity", "#/$defs/subject-scope", reversed_scope)[:2]}
    R["selfChecks"] = sc
    # ---- CLARIFICATION v1 additions ---------------------------------------
    R["clarificationV1"] = {
        "item2_repairCauseCarrier": RC.build(),
        "item3_planBoundReachability": BC.build()}

    # ---- the TypeScript body-dialect classification probe -----------------
    # CLARIFICATION v1: exported as a COMPLETE graph so its claimed closure is
    # independently inspectable, now that the unrelated helper errors
    # (evidenceRefs ordering, grammar-tree membership) are corrected.
    probe = vec_ts.build("ts-clones-scope-over-an-unlisted-suffix")
    pres = run_closure(probe["kit"], probe["run"])
    pres_export = export("RUN-TS-MUST1-PROBE", probe["kit"], probe["run"])
    runs["RUN-TS-MUST1-PROBE"] = dict(
        pres, runId=probe["run"], planId=probe["plan"],
        universes=probe["universes"], contexts=probe["contexts"],
        capabilityManifestId=probe["capabilityManifestId"],
        export=pres_export,
        note="CB7-MUST-1 probe: a clones@normalized-body-hash scope over the "
             "inventoried path package.json under a TypeScript universe, "
             "coverage complete, deficiency null, no fact for that subject")
    R["typescriptVariantUnknownProbe"] = {
        "exportedAs": "RUN-TS-MUST1-PROBE",
        "export": pres_export,
        "scopeSubject": "package.json",
        "runClosesWithCompleteAndNoFact": pres["admitted"],
        "checks": pres["checks"], "errors": pres["errors"],
        "dialectSelectorRefusal": "BODY_LANGUAGE_SOURCE_VARIANT_UNKNOWN",
        "nativeCauseMembersForBodyLanguage":
            [x for x in O.doc("native")["$defs"]["NativeCause"]["enum"]
             if x.startswith("body-language")],
        "note": "no published law decides whether this scope owes a disclosure"}

    # item 4 scope audit needs the results it audits, so write once, measure,
    # then write the final file including the audit.
    tmp = os.path.join(OUT, "vector-results.json")
    with open(tmp, "w") as f:
        json.dump(R, f, indent=1, sort_keys=True)
    R["clarificationV1"]["item4_reportingScopeAudit"] = SA.measure(tmp)
    with open(tmp, "w") as f:
        json.dump(R, f, indent=1, sort_keys=True)

    # console summary
    print("== positive Runs")
    for k in sorted(runs):
        if k.startswith("_"):
            continue
        v = runs[k]
        print("  %-14s checks=%4d errors=%d" % (k, v["checks"], len(v["errors"])))
    print("== negatives")
    tot = 0
    for k in sorted(runs):
        if k.startswith("_"):
            continue
        for n, r in sorted(runs[k].get("negatives", {}).items()):
            tot += 1
            print("  %-14s %-44s refused=%s" % (k, n, r["refused"]))
    print("  total negatives:", tot)
    print("== results written to", os.path.join(OUT, "vector-results.json"))


if __name__ == "__main__":
    main()
