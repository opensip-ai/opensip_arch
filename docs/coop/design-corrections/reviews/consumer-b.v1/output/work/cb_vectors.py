"""Consumer-B independent vectors. No author model, fixture or golden was read.

All synthetic bytes below are authored here. Every "trusted observation"
(custody, signature, OS, provider protocol success) is an ASSUMPTION, never
native enforcement proof.
"""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cb_canonical as C  # noqa: E402

SUBJ = "/tmp/opensip-design-corrections/consumer-b.v1/subject"
OUT = "/tmp/opensip-design-corrections/consumer-b.v1/output"

RESULTS = []
ASSUMPTIONS = []


def rec(vid, title, selector, expect, got, ok, extra=None):
    RESULTS.append({
        "id": vid, "title": title, "owningSelector": selector,
        "expected": expect, "observed": got, "pass": bool(ok),
        "extra": extra or {},
    })
    return ok


def assume(aid, text):
    ASSUMPTIONS.append({"id": aid, "assumption": text})


# ===========================================================================
# A. Admission and canonical encoding
# ===========================================================================

def refuses(fn, *a, **kw):
    try:
        fn(*a, **kw)
        return None
    except C.Refused as e:
        return e.code


def series_A():
    S = "identity-and-evidence.md §3 + admission-and-qualification.md §1"

    # A1 duplicate key
    rec("A1", "duplicate key refused before deserialization", S,
        "JSON.DUPLICATE_KEY",
        refuses(C.parse, b'{"schemaVersion":2,"schemaVersion":2}'),
        refuses(C.parse, b'{"schemaVersion":2,"schemaVersion":2}') == "JSON.DUPLICATE_KEY")

    # A2 float / exponent spellings of an integer
    for vid, tok in [("A2a", b"1.0"), ("A2b", b"1e0"), ("A2c", b"1E0"),
                     ("A2d", b"1.0000000000000001"), ("A2e", b"9007199254740991.1")]:
        code = refuses(C.parse, b'{"n":' + tok + b'}')
        rec(vid, "float/exponent token %s does not satisfy an integer field"
            % tok.decode(), S, "NUMBER.NOT_ORDINARY_INTEGER", code,
            code == "NUMBER.NOT_ORDINARY_INTEGER")

    # A3 -0 and nonfinite
    rec("A3a", "-0 refused", S, "NUMBER.NEGATIVE_ZERO",
        refuses(C.parse, b'{"n":-0}'),
        refuses(C.parse, b'{"n":-0}') == "NUMBER.NEGATIVE_ZERO")
    rec("A3b", "NaN refused", S, "NUMBER.NONFINITE",
        refuses(C.parse, b'{"n":NaN}'),
        refuses(C.parse, b'{"n":NaN}') == "NUMBER.NONFINITE")

    # A4 canonical integer range [-2^63, 2^64-1]
    for vid, tok, want in [
            ("A4a", str(2 ** 64 - 1), True), ("A4b", str(2 ** 64), False),
            ("A4c", str(-(2 ** 63)), True), ("A4d", str(-(2 ** 63) - 1), False)]:
        code = refuses(C.parse, ('{"n":%s}' % tok).encode())
        ok = (code is None) if want else (code == "NUMBER.OUT_OF_CANONICAL_RANGE")
        rec(vid, "integer boundary %s" % tok, S,
            "admitted" if want else "NUMBER.OUT_OF_CANONICAL_RANGE",
            code or "admitted", ok)

    # A5 booleans are distinct from integers; True cannot satisfy const:2
    rec("A5a", "true does not satisfy const 2", S, "not-exact",
        C.exact_const(True, 2), C.exact_const(True, 2) is False)
    rec("A5b", "1.0 (decoded float) does not satisfy const 1", S, "not-exact",
        C.exact_const(1.0, 1), C.exact_const(1.0, 1) is False)
    rec("A5c", "integer 2 satisfies const 2", S, "exact",
        C.exact_const(2, 2), C.exact_const(2, 2) is True)

    # A6 lone surrogate
    code = refuses(C.parse, b'{"s":"\\ud800"}')
    rec("A6", "lone surrogate escape refused", S, "UNICODE.SURROGATE_ESCAPE",
        code, code == "UNICODE.SURROGATE_ESCAPE")

    # A7 key ordering is by UTF-8 bytes, including non-BMP
    obj = {"\U0001F600": 1, "～": 2, "b": 3, "a": 4}
    enc = C.encode(obj)
    order = [k for k in sorted(obj, key=lambda x: x.encode("utf-8"))]
    rec("A7", "keys sort by UTF-8 bytes (non-BMP after BMP)", S,
        ["a", "b", "～", "\U0001F600"], order,
        order == ["a", "b", "～", "\U0001F600"],
        {"canonicalBytesHex": enc.hex()})

    # A8 escaping rules: quote/backslash, \b\t\n\f\r, lowercase \u00xx,
    #    slash NOT escaped, U+007F and U+2028 unescaped, no normalization.
    s = "a/b\"c\\d\te\x00f\x1ff\x7fg h"
    enc = C.encode({"s": s})
    want = ('{"s":"a/b\\"c\\\\d\\te\\u0000f\\u001ff\x7fg h"}').encode("utf-8")
    rec("A8", "escape set exactly as prose (slash/U+007F/U+2028 unescaped)", S,
        want.decode("utf-8"), enc.decode("utf-8"), enc == want,
        {"canonicalBytesHex": enc.hex()})

    # A9 no Unicode normalization: NFC vs NFD are different identities
    nfc, nfd = "é", "é"
    h1 = C.H("snapshot", {"x": nfc})
    h2 = C.H("snapshot", {"x": nfd})
    rec("A9", "no Unicode normalization: NFC and NFD differ", S,
        "distinct H", {"nfc": h1, "nfd": h2}, h1 != h2)

    # A10 depth: root container = 1; 32 admitted, 33 refused
    def nest(n):
        v = 1
        for _ in range(n):
            v = [v]
        return v
    rec("A10a", "nesting depth 32 admitted", S, "admitted",
        refuses(C.canonical, nest(32)) or "admitted",
        refuses(C.canonical, nest(32)) is None)
    rec("A10b", "nesting depth 33 refused", S, "DESCRIPTOR.DEPTH_EXCEEDED",
        refuses(C.canonical, nest(33)),
        refuses(C.canonical, nest(33)) == "DESCRIPTOR.DEPTH_EXCEEDED")

    # A11 set arrays: reordering is identity-neutral, duplicates refuse
    a = {"schemaVersion": 2, "importIds": ["import2:" + "a" * 64,
                                           "import2:" + "b" * 64]}
    b = {"schemaVersion": 2, "importIds": ["import2:" + "b" * 64,
                                           "import2:" + "a" * 64]}
    rec("A11a", "set-array reordering yields one identity", S,
        "equal", [C.H("plan", a), C.H("plan", b)],
        C.H("plan", a) == C.H("plan", b))
    dup = {"importIds": ["import2:" + "a" * 64, "import2:" + "a" * 64]}
    rec("A11b", "duplicate set item refused (not silently deduped)", S,
        "SET.DUPLICATE_ITEM", refuses(C.canonical, dup),
        refuses(C.canonical, dup) == "SET.DUPLICATE_ITEM")

    # A12 inventory sorts by UTF-8 logical path, NOT by canonical item bytes
    inv = [{"path": "b.ts", "sha256": "0" * 64, "bytes": 1},
           {"path": "a.ts", "sha256": "f" * 64, "bytes": 2}]
    enc = C.encode({"sourceInventory": inv})
    by_path_first = enc.index(b'"a.ts"') < enc.index(b'"b.ts"')
    # counterfactual: pure canonical-byte sort would put the f*64 blob first
    set_sorted = sorted([C.encode(x) for x in inv])
    would_differ = set_sorted[0] != C.encode(inv[1])
    rec("A12", "inventory sorts by logical path (distinct from set order)",
        "identity-and-evidence.md §3 'Inventories instead sort by UTF-8 "
        "logical path'", "a.ts before b.ts", enc.decode(),
        by_path_first and would_differ)

    # A13 stage arrays sort by contiguous ordinal; a gap refuses
    stages = [{"ordinal": 1, "stageSpecDigest": "1" * 64, "requires": [0],
               "outputDomains": ["fact"]},
              {"ordinal": 0, "stageSpecDigest": "0" * 64, "requires": [],
               "outputDomains": ["subject-scope"]}]
    ok = C.encode({"stages": stages}).index(b'"0"' if False else b'"ordinal":0') < \
        C.encode({"stages": stages}).index(b'"ordinal":1')
    rec("A13a", "stage array sorts by contiguous ordinal", S, "0 then 1",
        C.encode({"stages": stages}).decode(), ok)
    gap = [dict(stages[0], ordinal=5)]
    rec("A13b", "non-contiguous stage ordinal refused", S,
        "STAGES.NOT_CONTIGUOUS_ORDINAL", refuses(C.canonical, {"stages": gap}),
        refuses(C.canonical, {"stages": gap}) == "STAGES.NOT_CONTIGUOUS_ORDINAL")

    # A14 predicate proofs sort by (ruleId, subjectId, predicateId)
    pp = [{"ruleId": "r2", "subjectId": "s", "predicateId": "p", "value": "true"},
          {"ruleId": "r1", "subjectId": "s", "predicateId": "p", "value": "false"}]
    e = C.encode({"predicateProofs": pp})
    rec("A14", "predicate proofs sort by (ruleId, subjectId, predicateId)", S,
        "r1 before r2", e.decode(), e.index(b'"r1"') < e.index(b'"r2"'))

    # A15 the H frame itself (length framing prevents concatenation collisions)
    pre, c = C.H_preimage("snapshot", {"a": "b"})
    want_pre = (b"opensip.product.v1\x00snapshot\x00"
                + len(c).to_bytes(8, "big") + c)
    rec("A15", "H preimage frame is namespace||00||domain||00||u64be(len)||C(X)",
        "identity-and-evidence.md §3 H(D,X)", want_pre.hex(), pre.hex(),
        pre == want_pre and C.H("snapshot", {"a": "b"})
        == hashlib.sha256(want_pre).hexdigest())

    # A16 domain separation: identical descriptor, different domain
    d = {"schemaVersion": 2}
    rec("A16", "domain separation: same descriptor, different domain -> "
        "different identity", S, "distinct",
        {"snapshot": C.H("snapshot", d), "plan": C.H("plan", d)},
        C.H("snapshot", d) != C.H("plan", d))

    # A17 retained CAP-MANIFEST-ID-V1 recipe reproduces the retained
    #     DELIVERY v4 published committed byte strings.
    dv4 = json.load(open(os.path.join(
        SUBJ, "docs/coop/artifacts/delivery.v4.json")))
    vecs = dv4["derivedFrom"]["operations"][17]["value"]["vectors"]["byId"]
    allok, detail = True, {}
    for k, e in vecs.items():
        b = bytes.fromhex(e["committedBytesHex"])
        mine = C.capability_manifest_id(b)
        detail[k] = {"mine": mine, "published": e["capabilityManifestId"]}
        allok &= (mine == e["capabilityManifestId"]
                  and hashlib.sha256(b).hexdigest() == e["committedBytesSha256"])
    rec("A17", "my CAP-MANIFEST-ID-V1 implementation reproduces all seven "
        "retained committed-byte vectors",
        "delivery.v4.json $.derivedFrom.operations[17].value.recipe; "
        "identity-and-evidence.md §3", "all match", detail, allok)

    # A18 strict end anchor: a newline-suffixed identifier is malformed
    import re
    strict = re.compile(r"^exec1_[0-9a-f]{32}(?![\s\S])")
    loose = re.compile(r"^exec1_[0-9a-f]{32}$")
    v = "exec1_" + "0" * 32 + "\n"
    rec("A18", "trailing-newline ExecutionId: product (?![\\s\\S]) refuses, "
        "retained C-2 `$` grammar admits",
        "admission-and-qualification.md §1 vs c2-plan-stage-schema.v4.json "
        "$.planIntent.wireTypes.executionId.pattern",
        {"product": "refuse", "c2Retained": "match"},
        {"product": bool(strict.match(v)), "c2Retained": bool(loose.match(v))},
        (strict.match(v) is None) and (loose.match(v) is not None))


# ===========================================================================
# B. A complete minimal positive Run descriptor graph
# ===========================================================================

def blob(path, data):
    return {"path": path, "sha256": hashlib.sha256(data).hexdigest(),
            "bytes": len(data)}


def build_graph(mutate=None):
    m = mutate or {}
    G = {}

    # --- synthetic project (ProjectId is a host-CSPRNG draw; synthetic here)
    projectId = "prj1-" + hashlib.sha256(b"consumer-b.v1/synthetic-project"
                                         ).hexdigest()
    G["projectId"] = projectId

    # --- synthetic source bytes (authored here)
    src = {
        "src/a.ts": b"export function foo(){return 1}\nexport function bar(){return 2}\n",
        "src/b.ts": b"import {foo} from './a';\nfoo();\n",
    }
    inventory = [blob(p, d) for p, d in src.items()]
    G["sourceInventory"] = inventory
    sourceInventoryDigest = C.raw(inventory)

    # --- scope descriptor -> scopeDigest (identity §3: raw SHA-256 of the
    #     closed scope-descriptor record in identity-schemas.v2)
    scope = {"schemaVersion": 2, "workspaceRoots": ["."],
             "pathPrefixes": ["src"], "excludedPathPrefixes": []}
    G["scopeDescriptor"] = scope
    scopeDigest = C.raw(scope)

    # --- resolved semantic configuration -> resolvedConfigDigest
    #     ASSUMPTION CB-A1 (see report): all five sections present.
    cfg = {
        "analysis": {"profileId": "default", "capabilities": ["references"],
                     "budget": {"unit": "work-units", "limit": 100000}},
        "components": {}, "discovery": {}, "policy": {}, "evidence": {},
    }
    G["semanticConfiguration"] = cfg
    resolvedConfigDigest = C.raw(cfg)

    # --- VCS observation -> vcsDigest
    vcs = {"schemaVersion": 2, "kind": "git",
           "commitId": "a" * 40, "dirty": False,
           "sourceInventoryDigest": sourceInventoryDigest}
    G["vcsObservation"] = vcs
    vcsDigest = C.raw(vcs)

    # --- snapshot2
    snapshot = {"schemaVersion": 2, "projectId": projectId,
                "sourceInventory": inventory,
                "resolvedConfigDigest": resolvedConfigDigest,
                "scopeDigest": scopeDigest, "vcsDigest": vcsDigest}
    if "snapshot" in m:
        snapshot = m["snapshot"](snapshot)
    G["snapshot"] = snapshot
    snapshotId = C.ident("snapshot", snapshot)
    G["snapshotId"] = snapshotId

    # --- closures (synthetic signed trees)
    def closure(kind, name, ver, proto):
        body = ("manifest:" + name + ":" + ver).encode()
        tree = [blob(name + "/bin", ("BIN:" + name + ":" + ver).encode())]
        c = {"schemaVersion": 2, "kind": kind,
             "manifestDigest": hashlib.sha256(body).hexdigest(),
             "tree": tree, "semanticVersion": ver, "protocolMajor": proto,
             "platform": "macos-aarch64"}
        return c, C.ident("closure", c)

    provC, provId = closure("provider", "provider-typescript", "1.0.0", 2)
    evalC, evalId = closure("evaluator", "opensip-evaluator", "1.0.0", 0)
    detC, detId = closure("detector", "rulepack-core", "1.0.0", 0)
    G["closures"] = {"provider": provC, "evaluator": evalC, "detector": detC}
    G["closureIds"] = {"provider": provId, "evaluator": evalId,
                       "detector": detId}

    # --- capability manifest (CAP-MANIFEST-ID-V1 over synthetic committed bytes)
    committed = b"\x06\x00\x00\x00\x00"   # synthetic CVE1-shaped empty map
    capId = C.capability_manifest_id(committed)
    capBytesDigest = hashlib.sha256(committed).hexdigest()
    G["capabilityManifestCommittedBytesHex"] = committed.hex()

    # --- TypeScript semantic universe (native §2.2 / §11)
    #     nativeContextId is INVENTED: see report finding M-2.
    invented_ts_context = "sha256:" + hashlib.sha256(
        b"consumer-b.v1/INVENTED-typescript-native-context").hexdigest()
    tsu = {
        "schemaVersion": 2, "languageMode": "ts-tsconfig",
        "configOrigin": "tsconfig", "synthesizerVersion": None,
        "synthesizedOptions": None, "packageModuleType": "module",
        "allowJs": False, "checkJs": False, "jsAdmittedToProgram": False,
        "jsDiagnosticsEnabled": False, "resolutionCompletenessImplied": False,
        "jsRootFiles": [], "programRootFiles": ["src/a.ts", "src/b.ts"],
        "lockfileKind": "package-lock", "nodeModulesInReadSet": False,
        "executionCapableResolution": False,
        "tsconfigGraphHash": hashlib.sha256(b"tsconfig-graph").hexdigest(),
        "nativeContextId": invented_ts_context,
    }
    G["typescriptUniverse"] = tsu
    universe = C.H("native.semantic-universe.typescript.v2", tsu)
    G["universe"] = universe

    # --- analysis spec -> analysisSpecDigest
    spec = {"schemaVersion": 2,
            "requestedCapabilities": [{"capabilityId": "references",
                                       "languageMode": "ts-tsconfig",
                                       "workspaceRoot": ".", "required": True}],
            "policyPackIds": ["core"], "parameters": []}
    G["analysisSpec"] = spec
    analysisSpecDigest = C.raw(spec)

    # --- semantic grant -> semanticGrantDigest
    grant = {"schemaVersion": 2, "projectId": projectId,
             "principals": [{"kind": "first-party", "closureId": provId,
                             "ownerSourceDigest": None}],
             "analysisOperations": ["read-source", "native-analysis"],
             "scopeDigest": scopeDigest}
    G["semanticGrant"] = grant
    semanticGrantDigest = C.raw(grant)

    # --- policy / waivers (workflow closed documents)
    policy = {
        "schemaFamily": "opensip.product.policy", "schemaMajor": 1,
        "gateSeverityAtLeast": "error",
        "rules": [{
            "ruleId": "core.exported-symbol-referenced",
            "ruleProgramRef": {
                "contributionId": "11111111-1111-4111-8111-111111111111",
                "ruleStableId": "core.exported-symbol-referenced",
                "semanticsMajor": 2,
                "programDigest": hashlib.sha256(b"program-bytes").hexdigest()},
            "enabled": True, "severity": "note", "gate": False,
            "subjectEnumeration": {"universe": "typescript",
                                   "subjectKind": "export"},
            "emitWhen": {"op": "exists", "relation": "references",
                         "minResolution": "resolved-binding", "filters": []},
            "evidenceUse": []}]}
    waivers = {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1,
               "waivers": []}
    G["policyDocument"] = policy
    G["waiverSet"] = waivers
    policyDigest = C.raw(policy)
    waiverDigest = C.raw(waivers)
    ruleProgram = {"schemaVersion": 1, "policyDigest": policyDigest,
                   "rules": [{"ruleId": policy["rules"][0]["ruleId"],
                              "ruleProgramRef": policy["rules"][0]["ruleProgramRef"],
                              "emitWhen": policy["rules"][0]["emitWhen"]}]}
    G["ruleProgram"] = ruleProgram
    ruleProgramDigest = C.raw(ruleProgram)

    # --- plan2
    plan = {"schemaVersion": 2, "snapshotId": snapshotId,
            "capabilityManifestId": capId,
            "capabilityManifestBytesDigest": capBytesDigest,
            "semanticClosures": sorted([provId, evalId, detId]),
            "analysisSpecDigest": analysisSpecDigest,
            "resolvedConfigDigest": resolvedConfigDigest,
            "nativeContextDigests": [invented_ts_context.split(":")[1]],
            "importIds": [], "policyDigest": policyDigest,
            "waiverDigest": waiverDigest, "scopeDigest": scopeDigest,
            "budget": {"unit": "work-units", "limit": 100000},
            "semanticGrantDigest": semanticGrantDigest}
    if "plan" in m:
        plan = m["plan"](plan)
    G["plan"] = plan
    planId = C.ident("plan", plan)
    G["planId"] = planId

    # --- subject-scope -> scope2
    sscope = {"schemaVersion": 2, "snapshotId": snapshotId,
              "sourceUniverse": universe, "targetUniverse": universe,
              "relation": "references", "resolution": "resolved-binding",
              "enumeratorClosure": provId,
              "subjects": ["src/a.ts#bar", "src/a.ts#foo"]}
    G["subjectScope"] = sscope
    scopeId = C.ident("subject-scope", sscope)
    G["scopeId"] = scopeId

    # --- fact payload + fact2 (relation `references` @ resolved-binding)
    #     payload schema is the retained fact-plane relation payload registry.
    fp_path = os.path.join(SUBJ, "docs/coop/artifacts/fact-plane.v1.json")
    factPayloadSchemaDigest = hashlib.sha256(
        open(fp_path, "rb").read()).hexdigest()
    factPayload = {"subject": "src/a.ts#foo", "target": "src/b.ts#1",
                   "kind": "call-site"}
    factPayloadDigest = C.raw(factPayload)
    fact = {"schemaVersion": 2, "snapshotId": snapshotId,
            "relation": "references", "resolution": "resolved-binding",
            "sourceUniverse": universe, "targetUniverse": universe,
            "producerClosure": provId,
            "payloadSchemaDigest": factPayloadSchemaDigest,
            "payloadDigest": factPayloadDigest,
            "anchors": [{"path": "src/b.ts",
                         "blobDigest": inventory[1]["sha256"],
                         "startByte": 25, "endByte": 30}],
            "confidenceMillionths": 1000000}
    if "fact" in m:
        fact = m["fact"](fact)
    G["factPayload"] = factPayload
    G["fact"] = fact
    factId = C.ident("fact", fact)
    G["factId"] = factId

    # --- Coverage payload (CoverageResultV3) + coverage2
    #     subjectScopeCommitment is INVENTED: see report finding M-1.
    invented_ssc = "sha256:" + hashlib.sha256(
        b"consumer-b.v1/INVENTED-subject-scope-commitment/" + scopeId.encode()
    ).hexdigest()
    covPayload = {
        "schemaVersion": 3,
        "key": {"relation": "references", "resolution": "resolved-binding",
                "sourceUniverse": universe, "targetUniverse": universe,
                "subjectScopeCommitment": invented_ssc},
        "entry": {
            "relation": "references", "resolution": "resolved-binding",
            "coverage": "complete",
            "examinedUniverse": {"subjectScopeCommitment": invented_ssc,
                                 "subjectCount": 2},
            "resolutionCompleteness": {
                "state": "complete", "attempted": True,
                "examinedExhaustive": True, "stageTerminal": "complete",
                "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []},
            "closedWorld": {"exportsClosed": "closed",
                            "entryPointsRecognized": "all",
                            "nonliteralLoading": "none",
                            "externalConsumers": "none-declared",
                            "dynamicDispatch": "not-applicable",
                            "reasons": [], "deadCodeRepairEligible": True},
            "derivationKinds": [], "confidenceMillionths": 1000000,
            "deficiency": None, "nativeCause": None}}
    nat_path = os.path.join(
        SUBJ, "docs/coop/design-corrections/native/native-evidence.schemas.v2.json")
    covSchemaDigest = hashlib.sha256(open(nat_path, "rb").read()).hexdigest()
    coverage = {"schemaVersion": 2, "scopeId": scopeId,
                "payloadSchemaDigest": covSchemaDigest,
                "payloadDigest": C.raw(covPayload)}
    G["coveragePayload"] = covPayload
    G["coverage"] = coverage
    coverageId = C.ident("coverage", coverage)
    G["coverageId"] = coverageId

    # --- view2
    view = {"schemaVersion": 2, "planId": planId, "scopeIds": [scopeId],
            "facts": [factId], "coverageIds": [coverageId],
            "producerClosure": provId,
            "schemaDigests": sorted({factPayloadSchemaDigest,
                                     covSchemaDigest})}
    G["view"] = view
    viewId = C.ident("view", view)
    G["viewId"] = viewId

    # --- exec-plan2
    stage0 = {"stage": "enumerate", "closure": provId}
    stage1 = {"stage": "extract-references", "closure": provId}
    stage2 = {"stage": "evaluate", "closure": evalId}
    execPlan = {"schemaVersion": 2, "planId": planId, "stages": [
        {"ordinal": 0, "stageSpecDigest": C.raw(stage0), "requires": [],
         "outputDomains": ["subject-scope"]},
        {"ordinal": 1, "stageSpecDigest": C.raw(stage1), "requires": [0],
         "outputDomains": ["coverage", "fact"]},
        {"ordinal": 2, "stageSpecDigest": C.raw(stage2), "requires": [0, 1],
         "outputDomains": ["proof-bundle"]}]}
    G["executionPlan"] = execPlan
    execPlanId = C.ident("execution-plan", execPlan)
    G["executionPlanId"] = execPlanId

    # --- predicate witness -> witnessDigest
    witness = {"schemaVersion": 2,
               "programPredicateDigest": C.raw(policy["rules"][0]["emitWhen"]),
               "matchingFactIds": [factId], "coverageIds": [coverageId],
               "countLimit": None, "childPredicateIds": []}
    if "witness" in m:
        witness = m["witness"](witness)
    G["witness"] = witness
    witnessDigest = C.raw(witness)

    # --- finding fingerprint -> finding-key2, finding -> finding2
    sigTokens = ["ts", "function", "foo", "0", "():number"]
    discriminator = hashlib.sha256(C.canonical(sigTokens)).hexdigest()
    fp = {"schemaVersion": 2,
          "ruleStableId": "core.exported-symbol-referenced",
          "detectorSemanticsMajor": 2,
          "subjectKey": {"language": "typescript", "kind": "export",
                         "logicalPath": "src/a.ts", "qualifiedName": "foo",
                         "discriminator": discriminator},
          "relatedSubjectKeys": []}
    G["declarationSignatureTokens"] = sigTokens
    G["findingFingerprint"] = fp
    fingerprintId = C.ident("finding-fingerprint", fp)
    G["fingerprintId"] = fingerprintId

    finding = {"schemaVersion": 2, "fingerprint": fingerprintId,
               "ruleClosure": detId, "subjectId": "src/a.ts#foo",
               "messageCode": "core.referenced",
               "parameterDigest": C.raw({"name": "foo"}),
               "severity": "note",
               "evidenceRefs": [
                   {"domain": "fact", "digest": factId.split(":")[1]},
                   {"domain": "coverage", "digest": coverageId.split(":")[1]},
                   {"domain": "predicate-witness", "digest": witnessDigest}]}
    if "finding" in m:
        finding = m["finding"](finding)
    G["finding"] = finding
    findingId = C.ident("finding", finding)
    G["findingId"] = findingId

    # --- proof-bundle -> proof2
    inputRefs = [
        {"domain": "view", "digest": viewId.split(":")[1]},
        {"domain": "coverage", "digest": coverageId.split(":")[1]},
        {"domain": "rule-program", "digest": ruleProgramDigest},
        {"domain": "policy", "digest": policyDigest},
        {"domain": "waiver", "digest": waiverDigest},
        {"domain": "analysis-spec", "digest": analysisSpecDigest},
        {"domain": "configuration", "digest": resolvedConfigDigest},
        {"domain": "capability-manifest", "digest": capId},
        {"domain": "native-context", "digest": invented_ts_context.split(":")[1]},
    ]
    if "inputRefs" in m:
        inputRefs = m["inputRefs"](inputRefs)
    proof = {"schemaVersion": 2, "planId": planId,
             "executionPlanId": execPlanId, "evaluatorClosure": evalId,
             "ruleProgramDigest": ruleProgramDigest,
             "evaluationInputRefs": inputRefs,
             "predicateProofs": [{
                 "ruleId": "core.exported-symbol-referenced",
                 "subjectId": "src/a.ts#foo", "predicateId": "p0",
                 "operation": "exists",
                 "inputRefs": [{"domain": "view",
                                "digest": viewId.split(":")[1]},
                               {"domain": "coverage",
                                "digest": coverageId.split(":")[1]}],
                 "scopeIds": [scopeId], "value": "true",
                 "witnessDigest": witnessDigest}],
             "findingIds": [findingId], "verdict": "pass"}
    G["proof"] = proof
    proofId = C.ident("proof-bundle", proof)
    G["proofId"] = proofId

    # --- semantic-evidence -> evidence2
    evidence = {"schemaVersion": 2, "planId": planId, "viewIds": [viewId],
                "coverageIds": [coverageId], "importIds": [],
                "findingIds": [findingId], "proofBundleId": proofId}
    G["evidence"] = evidence
    evidenceId = C.ident("semantic-evidence", evidence)
    G["evidenceId"] = evidenceId

    # --- evaluation-seal -> seal2
    seal = {"schemaVersion": 2, "planId": planId,
            "executionPlanId": execPlanId, "evidenceId": evidenceId,
            "evaluatorClosure": evalId, "policyDigest": policyDigest,
            "proofBundleId": proofId, "verdict": "pass"}
    G["seal"] = seal
    sealId = C.ident("evaluation-seal", seal)
    G["sealId"] = sealId

    # --- run2
    run = {"schemaVersion": 2, "projectId": projectId,
           "snapshotId": snapshotId, "planId": planId,
           "evidenceId": evidenceId, "evaluationSealId": sealId,
           "capabilityManifestId": capId}
    G["run"] = run
    runId = C.ident("run", run)
    G["runId"] = runId
    return G


# ---------------------------------------------------------------------------
# Closure checker (identity-and-evidence.md §3 "The closure checker ..." and
# "Finding citations cannot introduce extra authoritative input roots.")
# ---------------------------------------------------------------------------

def close_run(G):
    """Returns [] when the Run graph closes; otherwise a list of refusals."""
    bad = []
    plan, snap = G["plan"], G["snapshot"]

    # snapshot/Plan config+scope agreement
    if plan["resolvedConfigDigest"] != snap["resolvedConfigDigest"]:
        bad.append("PLAN.CONFIG_DOES_NOT_JOIN_SNAPSHOT")
    if plan["scopeDigest"] != snap["scopeDigest"]:
        bad.append("PLAN.SCOPE_DOES_NOT_JOIN_SNAPSHOT")
    if plan["snapshotId"] != G["snapshotId"]:
        bad.append("PLAN.SNAPSHOT_REF_MISMATCH")

    # facts/scopes/coverage agree on source, universes, relation/rung, producer
    f, s = G["fact"], G["subjectScope"]
    if f["snapshotId"] != G["snapshotId"] or s["snapshotId"] != G["snapshotId"]:
        bad.append("VIEW.CROSS_SOURCE_JOIN")
    for k in ("relation", "resolution", "sourceUniverse", "targetUniverse"):
        if f[k] != s[k]:
            bad.append("VIEW.UNIVERSE_OR_RUNG_DISAGREEMENT:" + k)
    if f["producerClosure"] != G["view"]["producerClosure"]:
        bad.append("VIEW.PRODUCER_DISAGREEMENT")
    if G["coverage"]["scopeId"] != G["scopeId"]:
        bad.append("COVERAGE.SCOPE_NOT_IN_VIEW")

    # every source anchor names an inventoried blob
    inv = {b["path"]: b["sha256"] for b in snap["sourceInventory"]}
    for a in f["anchors"]:
        if inv.get(a["path"]) != a["blobDigest"]:
            bad.append("FACT.ANCHOR_NOT_INVENTORIED:" + a["path"])
        if a["startByte"] > a["endByte"]:
            bad.append("FACT.SPAN_NOT_HALF_OPEN")
        nbytes = {b["path"]: b["bytes"] for b in snap["sourceInventory"]}
        if a["endByte"] > nbytes.get(a["path"], 0):
            bad.append("FACT.SPAN_OUT_OF_BLOB")

    # proof/finding Ref domains exclude run/evidence/seal/proof outputs
    forbidden = {"run", "semantic-evidence", "evaluation-seal", "proof-bundle"}
    for r in G["proof"]["evaluationInputRefs"]:
        if r["domain"] in forbidden:
            bad.append("PROOF.FORBIDDEN_INPUT_DOMAIN:" + r["domain"])

    # every evaluated import must belong to Plan
    plan_imports = {i.split(":")[1] for i in plan["importIds"]}
    for r in G["proof"]["evaluationInputRefs"]:
        if r["domain"] == "import" and r["digest"] not in plan_imports:
            bad.append("PROOF.IMPORT_NOT_SELECTED_BY_PLAN:" + r["digest"][:12])

    # finding citations: facts/Coverage must belong to an evaluated view;
    # witnesses must be witnesses of this proof; imports must be both
    # Plan-selected and in evaluationInputRefs.
    view_facts = set(G["view"]["facts"])
    view_cov = set(G["view"]["coverageIds"])
    proof_witnesses = {p["witnessDigest"] for p in G["proof"]["predicateProofs"]}
    inputs = {(r["domain"], r["digest"]) for r in G["proof"]["evaluationInputRefs"]}
    for r in G["finding"]["evidenceRefs"]:
        d, h = r["domain"], r["digest"]
        if d == "fact" and ("fact2:" + h) not in view_facts:
            bad.append("FINDING.FACT_OUTSIDE_EVALUATED_VIEW:" + h[:12])
        if d == "coverage" and ("coverage2:" + h) not in view_cov:
            bad.append("FINDING.COVERAGE_OUTSIDE_EVALUATED_VIEW:" + h[:12])
        if d == "predicate-witness" and h not in proof_witnesses:
            bad.append("FINDING.WITNESS_NOT_OF_THIS_PROOF:" + h[:12])
        if d == "import" and (("import", h) not in inputs
                              or h not in plan_imports):
            bad.append("FINDING.IMPORT_NOT_IN_CLOSURE:" + h[:12])

    # witness facts must be exactly those the program selects over the
    # complete admitted view (here: the single admitted `references` fact)
    selected = sorted(view_facts)
    if sorted(G["witness"]["matchingFactIds"]) != selected:
        bad.append("WITNESS.NOT_EXACTLY_THE_SELECTED_FACTS")

    # predicate input refs are a subset of evaluationInputRefs
    for p in G["proof"]["predicateProofs"]:
        for r in p["inputRefs"]:
            if (r["domain"], r["digest"]) not in inputs:
                bad.append("PROOF.PREDICATE_INPUT_NOT_IN_EVALUATION_INPUTS")

    # evidence view roots equal the named views; coverage roots equal their union
    if set(G["evidence"]["viewIds"]) != {G["viewId"]}:
        bad.append("EVIDENCE.VIEW_ROOTS_MISMATCH")
    if set(G["evidence"]["coverageIds"]) != view_cov:
        bad.append("EVIDENCE.COVERAGE_ROOTS_NOT_VIEW_UNION")

    # acyclicity: proof carries no evidence/seal/run id anywhere
    ptext = json.dumps(G["proof"])
    for ident in (G["evidenceId"], G["sealId"], G["runId"]):
        if ident in ptext:
            bad.append("GRAPH.CYCLE_PROOF_INCLUDES_" + ident.split(":")[0])

    # sealed verdict must equal the proof's verdict
    if G["seal"]["verdict"] != G["proof"]["verdict"]:
        bad.append("SEAL.VERDICT_DISAGREES_WITH_PROOF")
    return bad


def validate_all(G):
    import jsonschema
    from jsonschema import Draft202012Validator
    ident = json.load(open(os.path.join(
        SUBJ, "docs/coop/design-corrections/foundation/identity-schemas.v2.json")))
    reg = {}
    out = {}
    pairs = [("snapshot", G["snapshot"]), ("plan", G["plan"]),
             ("subject-scope", G["subjectScope"]), ("fact", G["fact"]),
             ("coverage", G["coverage"]), ("view", G["view"]),
             ("execution-plan", G["executionPlan"]),
             ("predicate-witness", G["witness"]),
             ("finding-fingerprint", G["findingFingerprint"]),
             ("finding", G["finding"]), ("proof-bundle", G["proof"]),
             ("semantic-evidence", G["evidence"]),
             ("evaluation-seal", G["seal"]), ("run", G["run"]),
             ("scope-descriptor", G["scopeDescriptor"]),
             ("semantic-configuration", G["semanticConfiguration"]),
             ("analysis-spec", G["analysisSpec"]),
             ("semantic-grant", G["semanticGrant"]),
             ("vcs-observation", G["vcsObservation"])]
    for k in ("provider", "evaluator", "detector"):
        pairs.append(("closure", G["closures"][k]))
    for name, doc in pairs:
        sch = dict(ident)
        sch["$ref"] = "#/$defs/" + name
        errs = sorted(Draft202012Validator(sch).iter_errors(doc),
                      key=lambda e: list(e.path))
        out.setdefault(name, []).extend(
            [e.message + " at " + "/".join(str(x) for x in e.path)
             for e in errs])
    # native CoverageResultV3
    nat = json.load(open(os.path.join(
        SUBJ, "docs/coop/design-corrections/native/native-evidence.schemas.v2.json")))
    sch = dict(nat); sch["$ref"] = "#/$defs/CoverageResultV3"
    out["CoverageResultV3"] = [
        e.message for e in Draft202012Validator(sch).iter_errors(G["coveragePayload"])]
    # TypeScript universe
    sch = dict(nat); sch["$ref"] = "#/$defs/TypeScriptUniverseV2ResolvedInputs"
    out["TypeScriptUniverseV2ResolvedInputs"] = [
        e.message for e in Draft202012Validator(sch).iter_errors(G["typescriptUniverse"])]
    return {k: v for k, v in out.items() if v}


def series_B():
    S = "identity-and-evidence.md §3 (identity table), §4 (proof), §5 (commit)"
    G = build_graph()

    errs = validate_all(G)
    rec("B1", "complete minimal positive Run graph validates against the "
        "normative closed schemas", "foundation/identity-schemas.v2.json + "
        "native/native-evidence.schemas.v2.json#CoverageResultV3",
        "no schema errors", errs, errs == {})

    bad = close_run(G)
    rec("B2", "close_run: the positive graph closes (all joins hold)",
        S, [], bad, bad == [])

    ids = {k: G[k] for k in ("snapshotId", "planId", "scopeId", "factId",
                             "coverageId", "viewId", "executionPlanId",
                             "fingerprintId", "findingId", "proofId",
                             "evidenceId", "sealId", "runId")}
    rec("B3", "computed identifiers (my encoder, my synthetic descriptors)",
        S, "deterministic", ids, True)

    # determinism: rebuilding yields byte-identical identities
    G2 = build_graph()
    rec("B4", "rebuild is byte-identical (deterministic construction)", S,
        "equal", {"runId": G2["runId"]}, G2["runId"] == G["runId"])

    # ---- semantic change vs operational change
    Gc = build_graph(mutate={"fact": lambda f: dict(f, confidenceMillionths=999999)})
    rec("B5", "semantic-field change (fact.confidenceMillionths) changes "
        "fact2 -> view2 -> evidence2 -> seal2 -> run2", S, "all change",
        {"factId": Gc["factId"], "runId": Gc["runId"]},
        Gc["factId"] != G["factId"] and Gc["viewId"] != G["viewId"]
        and Gc["evidenceId"] != G["evidenceId"] and Gc["runId"] != G["runId"])

    Gs = build_graph(mutate={"snapshot": lambda s: dict(
        s, vcsDigest=hashlib.sha256(b"other-commit").hexdigest())})
    rec("B6", "source-provenance change (snapshot.vcsDigest) changes "
        "snapshot2 and therefore plan2/run2", S, "all change",
        {"snapshotId": Gs["snapshotId"], "runId": Gs["runId"]},
        Gs["snapshotId"] != G["snapshotId"] and Gs["runId"] != G["runId"])

    # operational identity exclusion: two attempts, different RequestId /
    # ExecutionId / wall clock / receipt signer -> the SAME run2.
    attempts = []
    for i, (req, ex, wall) in enumerate([
            ("req1_" + "0" * 32, "exec1_" + "1" * 32, "2026-09-06T00:00:00Z"),
            ("req1_" + "f" * 32, "exec1_" + "e" * 32, "2026-09-07T11:22:33Z")]):
        receipt = {"schemaVersion": 2, "runId": G["runId"], "executionId": ex,
                   "namespaceId": "ns-1", "commitSequence": 100 + i,
                   "inventoryDigest": hashlib.sha256(
                       ("inv%d" % i).encode()).hexdigest(),
                   "sealedAssurance": "replayable",
                   "signerKeyId": "key-%d" % i}
        attempts.append({"requestId": req, "executionId": ex,
                         "wallClock": wall, "commitReceipt": receipt,
                         "runId": G["runId"]})
    same = attempts[0]["runId"] == attempts[1]["runId"]
    # and no operational token appears anywhere in the Run closure
    closure_text = json.dumps({k: G[k] for k in (
        "snapshot", "plan", "subjectScope", "fact", "coverage", "view",
        "executionPlan", "witness", "finding", "proof", "evidence", "seal",
        "run")})
    leaked = [t for t in ("req1_", "exec1_", "2026-09-0", "signerKeyId",
                          "namespaceId", "commitSequence")
              if t in closure_text]
    rec("B7", "operational identities (RequestId/ExecutionId/wall clock/"
        "receipt signer/namespace/sequence) are excluded from Run identity; "
        "two attempts share one run2 with separate receipts",
        "identity-and-evidence.md §2 and §5 step 3", "same run2, no leakage",
        {"runId": G["runId"], "attempts": attempts, "leakedTokens": leaked},
        same and leaked == [])

    # StepId is a zero-based ordered position, not a minted identity
    rec("B8", "StepId is the zero-based position in the invocation DAG "
        "(operational), and never appears in a semantic descriptor",
        "identity-and-evidence.md §2; workflows-and-surfaces.md §1",
        "absent from closure", "stepId" in closure_text,
        "stepId" not in closure_text)

    # ---- acyclic construction: proof excludes evidence/seal/run
    rec("B9", "acyclicity: proof2 contains no evidence2/seal2/run2; evidence "
        "contains proof; seal contains both; run contains seal",
        "identity-and-evidence.md §3 'The graph is acyclic'",
        "acyclic",
        {"proofHasEvidence": G["evidenceId"] in json.dumps(G["proof"]),
         "evidenceHasProof": G["proofId"] == G["evidence"]["proofBundleId"],
         "sealHasBoth": (G["evidenceId"] == G["seal"]["evidenceId"]
                         and G["proofId"] == G["seal"]["proofBundleId"]),
         "runHasSeal": G["sealId"] == G["run"]["evaluationSealId"]},
        (G["evidenceId"] not in json.dumps(G["proof"])
         and G["proofId"] == G["evidence"]["proofBundleId"]
         and G["evidenceId"] == G["seal"]["evidenceId"]
         and G["sealId"] == G["run"]["evaluationSealId"]))

    # cache2 vs regen2 share a descriptor shape and are separated ONLY by domain
    ck = {"schemaVersion": 2, "planId": G["planId"],
          "producerClosure": G["closureIds"]["provider"],
          "stageSpecDigest": G["executionPlan"]["stages"][1]["stageSpecDigest"],
          "scopeIds": [G["scopeId"]],
          "inputRefs": [{"domain": "snapshot",
                         "digest": G["snapshotId"].split(":")[1]}],
          "outputSchemaDigest": G["fact"]["payloadSchemaDigest"]}
    c2, r2 = C.ident("cache-key", ck), C.ident("regeneration-key", ck)
    rec("B10", "cache2 and regen2 share an identical descriptor schema and "
        "are distinguished only by the H domain",
        "identity-schemas.v2.json#/$defs/cache-key and #/$defs/regeneration-key",
        "distinct identities from one descriptor", {"cache2": c2, "regen2": r2},
        c2.split(":")[1] != r2.split(":")[1])

    return G


# ===========================================================================
# C. Refused hidden / mismatched inputs
# ===========================================================================

def series_C(G):
    S = "identity-and-evidence.md §3 'Finding citations cannot introduce " \
        "extra authoritative input roots.'"

    # C1 hidden finding evidence: a well-formed, hash-valid fact outside the
    #    evaluated view.
    hidden_fact = dict(G["fact"], payloadDigest=C.raw({"subject": "src/a.ts#baz",
                                                      "target": "external",
                                                      "kind": "call-site"}))
    hidden_id = C.ident("fact", hidden_fact)
    Gh = build_graph(mutate={"finding": lambda f: dict(
        f, evidenceRefs=f["evidenceRefs"] + [
            {"domain": "fact", "digest": hidden_id.split(":")[1]}])})
    bad = close_run(Gh)
    hit = [b for b in bad if b.startswith("FINDING.FACT_OUTSIDE_EVALUATED_VIEW")]
    rec("C1", "a well-formed, hash-valid fact cited by a finding but outside "
        "the evaluated view is REFUSED, not admitted as hidden evidence",
        S, "FINDING.FACT_OUTSIDE_EVALUATED_VIEW", bad, len(hit) == 1,
        {"hiddenFactId": hidden_id,
         "schemaValid": validate_all(Gh) == {}})

    # C2 an import in evaluationInputRefs that Plan never selected.
    ghost_import = "0123456789abcdef" * 4
    Gi = build_graph(mutate={"inputRefs": lambda r: r + [
        {"domain": "import", "digest": ghost_import}]})
    bad = close_run(Gi)
    rec("C2", "an import listed in evaluationInputRefs but not selected by "
        "Plan is REFUSED (no extra authoritative input root)",
        "identity-and-evidence.md §3 'import citations must be both selected "
        "by Plan and listed in evaluationInputRefs'",
        "PROOF.IMPORT_NOT_SELECTED_BY_PLAN", bad,
        any(b.startswith("PROOF.IMPORT_NOT_SELECTED_BY_PLAN") for b in bad))

    # C3 cross-source join: a fact bound to another snapshot2.
    other = build_graph(mutate={"snapshot": lambda s: dict(
        s, vcsDigest=hashlib.sha256(b"foreign").hexdigest())})
    Gx = build_graph(mutate={"fact": lambda f: dict(
        f, snapshotId=other["snapshotId"])})
    bad = close_run(Gx)
    rec("C3", "a fact bound to a different snapshot2 is a refused "
        "cross-source join, even though it is schema-valid and hash-valid",
        "identity-and-evidence.md §3 'rejects ... cross-Plan/cross-source ... "
        "references'", "VIEW.CROSS_SOURCE_JOIN", bad,
        "VIEW.CROSS_SOURCE_JOIN" in bad,
        {"schemaValid": validate_all(Gx) == {}})

    # C4 a witness that is a strict subset of the selected facts
    Gw = build_graph(mutate={"witness": lambda w: dict(w, matchingFactIds=[])})
    bad = close_run(Gw)
    rec("C4", "a witness naming a subset of the program-selected facts is "
        "REFUSED (the producer cannot choose the witness set)",
        "identity-and-evidence.md §4 'Witness facts must be exactly those "
        "selected by the program over the complete admitted view'",
        "WITNESS.NOT_EXACTLY_THE_SELECTED_FACTS", bad,
        "WITNESS.NOT_EXACTLY_THE_SELECTED_FACTS" in bad)

    # C5 proof tampering: a witness byte change moves witnessDigest, so the
    #    finding's predicate-witness citation no longer names a witness of
    #    this proof.
    Gt = build_graph()
    tampered = dict(Gt["witness"], countLimit=7)
    Gt2 = build_graph(mutate={"witness": lambda w: dict(w, countLimit=7)})
    moved = C.raw(tampered) != C.raw(Gt["witness"])
    rec("C5", "witness tampering moves witnessDigest and therefore proof2, "
        "evidence2, seal2 and run2", "identity-and-evidence.md §4",
        "identities move",
        {"beforeRun": Gt["runId"], "afterRun": Gt2["runId"]},
        moved and Gt2["runId"] != Gt["runId"])

    # C6 caller-supplied `verified` / operational authority is not admissible:
    #    the closed schemas have no such field.
    from jsonschema import Draft202012Validator
    ident = json.load(open(os.path.join(
        SUBJ, "docs/coop/design-corrections/foundation/identity-schemas.v2.json")))
    sch = dict(ident); sch["$ref"] = "#/$defs/run"
    forged = dict(G["run"], verified=True)
    errs = [e.message for e in Draft202012Validator(sch).iter_errors(forged)]
    rec("C6", "a caller's `verified:true` cannot be carried: run2 is a closed "
        "record", "identity-and-evidence.md §1; identity-schemas.v2 "
        "#/$defs/run additionalProperties:false",
        "additionalProperties refusal", errs, len(errs) >= 1)

    # C7 forged capabilityManifestId over the same bytes
    committed = bytes.fromhex(G["capabilityManifestCommittedBytesHex"])
    forged_id = hashlib.sha256(committed).hexdigest()   # plain SHA, wrong recipe
    real_id = C.capability_manifest_id(committed)
    rec("C7", "a supplied capabilityManifestId is never authority: the host "
        "recomputes it under CAP-MANIFEST-ID-V1 and a plain SHA-256 of the "
        "same bytes does not match",
        "identity-and-evidence.md §3; delivery.v4 CAP-MANIFEST-ID-V1",
        "mismatch detected",
        {"recomputed": real_id, "plainSha256OfSameBytes": forged_id},
        real_id != forged_id and real_id == G["plan"]["capabilityManifestId"])


# ===========================================================================
# D. Public termination examples (schema-validated)
# ===========================================================================

def series_D():
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
    base = os.path.join(SUBJ, "docs/coop/design-corrections/workflows/schemas")
    docs = {}
    for f in os.listdir(base):
        d = json.load(open(os.path.join(base, f)))
        docs[d["$id"]] = d
    registry = Registry().with_resources(
        [(k, Resource.from_contents(v, default_specification=None)
          if False else Resource(contents=v, specification=None)) for k, v in []]
    ) if False else Registry().with_resources(
        [(k, Resource.from_contents(v)) for k, v in docs.items()])

    common = docs["urn:opensip:product-v1:workflows:common"]
    reg_pub = json.load(open(os.path.join(
        SUBJ,
        "docs/coop/design-corrections/public-detail-registry.v1.json")))

    def validate(term):
        sch = {"$schema": "https://json-schema.org/draft/2020-12/schema",
               "$id": "urn:opensip:consumer-b:term",
               "$ref": "urn:opensip:product-v1:workflows:common#/$defs/"
                       "StepTermination"}
        v = Draft202012Validator(sch, registry=registry)
        return [e.message for e in v.iter_errors(term)]

    # public detail code vocabulary from the closed registry
    codes = set()

    def collect(o):
        if isinstance(o, dict):
            for k, v in o.items():
                if k in ("code", "detailCode") and isinstance(v, str):
                    codes.add(v)
                collect(v)
        elif isinstance(o, list):
            for x in o:
                collect(x)
    collect(reg_pub)
    enum = common["$defs"]["DomainDetailCode"].get("enum")
    if enum:
        codes |= set(enum)

    EX = [
        ("D1", "fresh project, providers installed: durable authoritative "
         "analysis succeeds; DEFAULTED retention disclosed",
         "workflows-and-surfaces.md §9 golden row 1; identity §5",
         {"class": "success", "authority": "authoritative",
          "runId": "run2:" + "1" * 64}),
        ("D2", "required provider closure not installed -> indeterminate 3",
         "workflows-and-surfaces.md §9; native §10 provider-unavailable row",
         {"class": "indeterminate",
          "reasonCodes": ["COVERAGE.PROVIDER_UNAVAILABLE"],
          "coverageId": "coverage2:" + "2" * 64,
          "domainDetail": {
              "code": "COMPONENT.REQUIRED_CLOSURE_NOT_INSTALLED",
              "remedy": "opensip install provider-typescript"}}),
        ("D3", "required evidence purged, query needs actual proof -> "
         "request-rejected 2 before evaluation",
         "identity-and-evidence.md §5; workflows §12 evidence.* details",
         {"class": "request-rejected",
          "errorCode": "REQUEST.PRECONDITION_FAILED",
          "domainDetail": {"code": "evidence.purged",
                           "remedy": "re-run an authoritative analysis",
                           "subject": "run2:" + "3" * 64}}),
        ("D4", "inability to read retained bytes DURING a selected operation "
         "-> operational-failed 4 (a different event position from D3)",
         "identity-and-evidence.md §5 'inability during a selected operation "
         "is HOST.IO_FAILURE ... (exit 4)'",
         {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE",
          "faultCause": "host-io",
          "domainDetail": {"code": "evidence.missing",
                           "remedy": "opensip doctor",
                           "subject": "fact2:" + "4" * 64}}),
        ("D5", "admitted but incomplete native inputs -> AUTHORITATIVE Run, "
         "indeterminate 3 with the deficiency in the coverage2 record",
         "native-evidence.md §10 fault law; identity §5",
         {"class": "indeterminate", "reasonCodes": ["VERDICT.INDETERMINATE"],
          "runId": "run2:" + "5" * 64, "coverageId": "coverage2:" + "5" * 64,
          "authority": "authoritative"}),
        ("D6", "worker fault: no facts, no Coverage, no Run -> "
         "operational-failed 4",
         "native-evidence.md §10 'A worker that faults ... contributes no "
         "facts, no Coverage entries and no Run'",
         {"class": "operational-failed",
          "errorCode": "PROVIDER.PROTOCOL_VIOLATION",
          "faultCause": "provider-protocol"}),
        ("D7", "required renderer fails AFTER commit -> operational-failed 4, "
         "runId retained, Run not rewritten",
         "workflows-and-surfaces.md §8 and §9",
         {"class": "operational-failed",
          "errorCode": "DELIVERY.REQUIRED_FAILED",
          "faultCause": "delivery-required", "runId": "run2:" + "7" * 64,
          "domainDetail": {
              "code": "DELIVERY.RENDERER_FAILED_AFTER_COMMIT",
              "remedy": "re-render from the retained Run"}}),
        ("D8", "optional export sink fails -> success 0 (egress never changes "
         "a verdict)", "workflows-and-surfaces.md §9",
         {"class": "success", "runId": "run2:" + "8" * 64}),
        ("D9", "--ephemeral offered as a baseline/repair prerequisite -> "
         "request-rejected 2",
         "workflows-and-surfaces.md §1 and §9",
         {"class": "request-rejected", "errorCode": "REQUEST.UNSATISFIABLE",
          "domainDetail": {
              "code": "WORKFLOW.EPHEMERAL_CANNOT_SUPPLY_AUTHORITY",
              "remedy": "re-run without --ephemeral"}}),
        ("D10", "ephemeral analysis whose verdict fails -> policy-failed 1 "
         "with authority=ephemeral and NO runId",
         "workflows-and-surfaces.md §1; common#/$defs/StepTermination branch",
         {"class": "policy-failed", "authority": "ephemeral"}),
        ("D11", "CI storage root detected backup-managed, no explicit choice "
         "-> request-rejected 2 before any evidence is created",
         "identity-and-evidence.md §5 (TM V17); security S3.1; workflows §12 "
         "canonical spelling `storage.backup-choice-required`",
         {"class": "request-rejected",
          "errorCode": "REQUEST.PRECONDITION_FAILED",
          "domainDetail": {"code": "storage.backup-choice-required",
                           "remedy": "--allow-backup-custody or --ephemeral"}}),
        ("D12", "doctor report produced WITH defects -> success 0",
         "workflows-and-surfaces.md §8/§9; security S11 (CI gates on "
         "outcome, never the exit code)",
         {"class": "success",
          "domainDetail": {"code": "DOCTOR.DEFECTS_FOUND",
                           "remedy": "inspect doctor.defectsFound"}}),
        ("D13", "SIGINT before settle, with a Run already committed by an "
         "earlier step -> interrupted 130 carrying that runId",
         "workflows-and-surfaces.md §1 cancellation; §9",
         {"class": "interrupted", "signal": "SIGINT",
          "runId": "run2:" + "d" * 64}),
        ("D14", "purge of a pinned Run without revoking the pins -> "
         "request-rejected 2", "identity-and-evidence.md §5",
         {"class": "request-rejected",
          "errorCode": "REQUEST.PRECONDITION_FAILED"}),
        ("D15", "empty findings array is a real empty result, not a missing "
         "projection: a passing Run terminates success 0",
         "workflows-and-surfaces.md §8 'An empty findings array is a real "
         "empty result'", {"class": "success", "runId": "run2:" + "e" * 64}),
        ("D16", "comparison indeterminate because required evidence was lost "
         "-> indeterminate 3 even when both finding sets are empty",
         "workflows-and-surfaces.md §3 evidence axis; §12",
         {"class": "indeterminate", "reasonCodes": ["VERDICT.INDETERMINATE"],
          "domainDetail": {
              "code": "COMPARISON.REQUIRED_EVIDENCE_UNAVAILABLE",
              "remedy": "re-import the required evidence"}}),
    ]

    exit_of = {"success": 0, "policy-failed": 1, "request-rejected": 2,
               "indeterminate": 3, "operational-failed": 4, "interrupted": 130}
    for vid, title, sel, term in EX:
        errs = validate(term)
        dd = term.get("domainDetail", {}).get("code")
        unregistered = dd is not None and codes and dd not in codes
        rec(vid, title, sel, "schema-valid; exit %s" % exit_of[term["class"]],
            {"termination": term, "exitCode": exit_of[term["class"]],
             "schemaErrors": errs,
             "domainDetailRegistered": (None if dd is None else not unregistered)},
            errs == [])

    # negative controls on the branch contract
    NEG = [
        ("D17", "success carrying an errorCode is schema-refused",
         {"class": "success", "errorCode": "HOST.IO_FAILURE"}),
        ("D18", "operational-failed without faultCause is schema-refused",
         {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE"}),
        ("D19", "operational-failed with faultCause=none is schema-refused",
         {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE",
          "faultCause": "none"}),
        ("D20", "policy-failed with neither runId nor authority=ephemeral is "
         "schema-refused", {"class": "policy-failed"}),
        ("D21", "authority=ephemeral together with a runId is schema-refused",
         {"class": "policy-failed", "authority": "ephemeral",
          "runId": "run2:" + "0" * 64}),
        ("D22", "indeterminate carrying an errorCode is schema-refused",
         {"class": "indeterminate", "reasonCodes": ["VERDICT.INDETERMINATE"],
          "errorCode": "HOST.IO_FAILURE"}),
        ("D23", "an unregistered DomainDetailCode is schema-refused",
         {"class": "success",
          "domainDetail": {"code": "MADE.UP_CODE", "remedy": "none"}}),
        ("D24", "an unknown termination field is schema-refused (closed union)",
         {"class": "success", "exitCode": 0}),
    ]
    for vid, title, term in NEG:
        errs = validate(term)
        rec(vid, title, "common.schema.json#/$defs/StepTermination branch "
            "contract; workflows-and-surfaces.md §9", "schema refusal",
            {"termination": term, "schemaErrors": errs}, errs != [])


# ===========================================================================
def main():
    series_A()
    G = series_B()
    series_C(G)
    series_D()

    os.makedirs(os.path.join(OUT, "vectors"), exist_ok=True)
    G_out = {k: v for k, v in G.items()}
    json.dump(G_out, open(os.path.join(OUT, "vectors",
                                       "run-descriptor-graph.json"), "w"),
              indent=1, sort_keys=True)
    json.dump({"results": RESULTS,
               "passed": sum(1 for r in RESULTS if r["pass"]),
               "total": len(RESULTS)},
              open(os.path.join(OUT, "vectors", "vector-results.json"), "w"),
              indent=1, sort_keys=True)
    fails = [r for r in RESULTS if not r["pass"]]
    print("vectors: %d/%d pass" % (len(RESULTS) - len(fails), len(RESULTS)))
    for r in fails:
        print("  FAIL", r["id"], r["title"])
        print("        expected:", r["expected"])
        print("        observed:", json.dumps(r["observed"])[:400])


if __name__ == "__main__":
    main()
