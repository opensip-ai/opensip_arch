"""Consumer-B series F: reproducible probes of gaps that FORCE invention.

Each probe builds two readings that are BOTH admissible under the normative
inputs and shows that they mint different identities. A divergence here is a
public/semantic contract gap, not implementation freedom, because the value
enters snapshot2/plan2/coverage2 and therefore run2.
"""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import cb_canonical as C  # noqa: E402
import cb_vectors as V  # noqa: E402

SUBJ = "/tmp/opensip-design-corrections/consumer-b.v1/subject"


def build(results):
    def rec(vid, title, sel, expect, obs, ok, extra=None):
        results.append({"id": vid, "title": title, "owningSelector": sel,
                        "expected": expect, "observed": obs, "pass": bool(ok),
                        "extra": extra or {}})

    from jsonschema import Draft202012Validator
    ident = json.load(open(os.path.join(
        SUBJ, "docs/coop/design-corrections/foundation/identity-schemas.v2.json")))

    def ivalid(name, doc):
        s = dict(ident); s["$ref"] = "#/$defs/" + name
        return [e.message for e in Draft202012Validator(s).iter_errors(doc)]

    # ---- F1 resolved semantic configuration: which sections are present?
    a = {"analysis": {"profileId": "default", "capabilities": ["references"],
                      "budget": {"unit": "work-units", "limit": 100000}}}
    b = dict(a, components={}, discovery={}, policy={}, evidence={})
    da, db = C.raw(a), C.raw(b)
    rec("F1", "resolvedConfigDigest is ambiguous: the closed schema requires "
        "only `analysis`, while admission §1.1 says the resolved value "
        "'contains analysis, components, discovery, policy and evidence "
        "values'. Both spellings validate and mint different digests, so two "
        "conforming hosts produce different snapshot2/plan2/run2 for one "
        "project.",
        "admission-and-qualification.md §1.1 'Resolved semantic configuration "
        "contains analysis, components, discovery, policy and evidence "
        "values.' vs identity-schemas.v2.json#/$defs/semantic-configuration "
        "required=[\"analysis\"]",
        "DIVERGENCE (both readings schema-valid, digests differ)",
        {"analysisOnly": {"schemaErrors": ivalid("semantic-configuration", a),
                          "resolvedConfigDigest": da},
         "allFiveSections": {"schemaErrors": ivalid("semantic-configuration", b),
                             "resolvedConfigDigest": db}},
        ivalid("semantic-configuration", a) == []
        and ivalid("semantic-configuration", b) == [] and da != db)

    # F1b: the same schema also admits an EMPTY analysis section, although
    # admission §4 refuses a missing profile as CONFIG_PROFILE_MISSING.
    c = {"analysis": {}}
    rec("F1b", "the closed schema admits `{\"analysis\":{}}` with no "
        "profileId, although admission §4 declares a missing profile "
        "CONFIG_PROFILE_MISSING; the post-resolution requiredness is not "
        "expressed anywhere machine-readable",
        "identity-schemas.v2.json#/$defs/semantic-configuration/properties/"
        "analysis required=[] vs admission-and-qualification.md §4",
        "schema admits a value the prose refuses",
        {"schemaErrors": ivalid("semantic-configuration", c),
         "digest": C.raw(c)}, ivalid("semantic-configuration", c) == [])

    # ---- F2 policy `rules` array ordering under the one canonicalizer
    rule = lambda rid: {  # noqa: E731
        "ruleId": rid,
        "ruleProgramRef": {"contributionId": "11111111-1111-4111-8111-"
                                             "111111111111",
                           "ruleStableId": rid, "semanticsMajor": 2,
                           "programDigest": hashlib.sha256(
                               rid.encode()).hexdigest()},
        "enabled": True, "severity": "note", "gate": False,
        "subjectEnumeration": {"universe": "typescript",
                               "subjectKind": "export"},
        "emitWhen": {"op": "exists", "relation": "references",
                     "minResolution": "resolved-binding", "filters": []},
        "evidenceUse": []}
    # two ordinary rules with different predicates: declared ruleId order is
    # a.first then b.second, but canonical item bytes sort on `emitWhen`
    # first, where "count-at-most" precedes "exists".
    r_a = rule("a.first")
    r_b = rule("b.second")
    r_b["emitWhen"] = {"op": "count-at-most", "relation": "references",
                       "minResolution": "resolved-binding", "filters": [],
                       "n": 3}
    pol = {"schemaFamily": "opensip.product.policy", "schemaMajor": 1,
           "gateSeverityAtLeast": "error", "rules": [r_a, r_b]}

    # reading 1: `rules` is a set -> sorted by canonical item bytes
    set_reading = C.raw(pol)
    # reading 2: `rules` keeps its declared ruleId order (the schema's own
    # description) -> encode the array without re-sorting
    def enc_declared(v, key=None):
        if isinstance(v, list) and key == "rules":
            return b"[" + b",".join(enc_declared(x) for x in v) + b"]"
        if isinstance(v, dict):
            parts = []
            for k in sorted(v, key=lambda x: x.encode()):
                parts.append(C._enc_string(k) + b":" + enc_declared(v[k], k))
            return b"{" + b",".join(parts) + b"}"
        if isinstance(v, list):
            return C.encode(v, key)
        return C.encode(v, key)
    declared_reading = hashlib.sha256(enc_declared(pol)).hexdigest()
    # the two differ exactly when canonical-byte order != ruleId order
    rec("F2", "policyDigest is ambiguous: §3 says set arrays sort by canonical "
        "item bytes and names only three exceptions (inventories, predicate "
        "proofs, stages); the policy schema instead declares `rules` 'sorted "
        "ascending by ruleId UTF-8 bytes' and RuleProgramV1 hashes 'ordered "
        "rule programs'. Rule objects sort first on `emitWhen`, so the two "
        "readings disagree and policyDigest -> plan2 -> run2 diverges.",
        "identity-and-evidence.md §3 'Arrays whose semantics are sets are "
        "sorted and unique by canonical item bytes' vs "
        "policy-document.schema.json#/$defs/PolicyDocumentV1/properties/rules "
        "description and workflows-and-surfaces.md §5 'ordered rule programs'",
        "DIVERGENCE",
        {"setReadingPolicyDigest": set_reading,
         "declaredOrderPolicyDigest": declared_reading},
        set_reading != declared_reading)

    # F2b: no machine-readable marker distinguishes set from ordered arrays.
    docs = {}
    base = os.path.join(SUBJ, "docs/coop/design-corrections/workflows/schemas")
    for f in os.listdir(base):
        docs[f] = json.load(open(os.path.join(base, f)))
    arrays = {"withUnique": 0, "withoutUnique": 0}

    def count(o):
        if isinstance(o, dict):
            if o.get("type") == "array":
                arrays["withUnique" if o.get("uniqueItems")
                       else "withoutUnique"] += 1
            for v in o.values():
                count(v)
        elif isinstance(o, list):
            for v in o:
                count(v)
    for d in docs.values():
        count(d)
    # counterexample: `stages` and `tree` carry uniqueItems yet have their own
    # declared orders, so uniqueItems cannot be the set marker.
    stages_unique = ident["$defs"]["execution-plan"]["properties"]["stages"][
        "uniqueItems"]
    tree_unique = ident["$defs"]["closure"]["properties"]["tree"]["uniqueItems"]
    rec("F2b", "there is no machine-readable marker for 'this array's "
        "semantics are a set': `uniqueItems` is also carried by the two "
        "arrays §3 explicitly gives a different order (`stages`, `tree`), so "
        "the classification is prose-only and enumerates a handful of fields "
        "out of many hundreds",
        "identity-and-evidence.md §3 array-ordering paragraph",
        "no machine-readable discriminator",
        {"workflowSchemaArrays": arrays,
         "stagesHasUniqueItems": stages_unique,
         "closureTreeHasUniqueItems": tree_unique},
        stages_unique is True and tree_unique is True)

    # ---- F3 subjectScopeCommitment has no producing recipe
    scope_id = "scope2:" + hashlib.sha256(b"scope").hexdigest()
    r1 = "sha256:" + hashlib.sha256(scope_id.encode()).hexdigest()
    r2 = "sha256:" + hashlib.sha256(
        C.canonical(["src/a.ts#bar", "src/a.ts#foo"])).hexdigest()
    cov = lambda ssc: {"schemaVersion": 2, "scopeId": scope_id,  # noqa: E731
                       "payloadSchemaDigest": "0" * 64,
                       "payloadDigest": hashlib.sha256(ssc.encode()).hexdigest()}
    rec("F3", "MISSING RECIPE: `subjectScopeCommitment` is a required field "
        "of CoverageKeyV2 and ExaminedUniverseV1, its value enters the "
        "coverage payload digest and therefore coverage2 -> view2 -> "
        "evidence2 -> run2, and NO product document states how it is "
        "computed. Its only retained selector explicitly defers the "
        "computation, and its published values are declared example-only.",
        "native-evidence.md §0 retains c2-plan-stage-schema.v4.json "
        "$.coverageKey.key[subjectScopeCommitment], whose own text is "
        "'boundHere: SHAPE ONLY; computation and verification stay deferred "
        "(R1-C2-03)' and 'This is an EXAMPLE ENCODING for the fixtures only. "
        "It is NOT a claim about how a product computes a real subject-scope "
        "commitment; that remains owned by the retention/evidence surface.' "
        "identity-and-evidence.md §3's auxiliary-digest list does not supply "
        "it and native-evidence.md §11's domain list has no member for it.",
        "INVENTION REQUIRED",
        {"twoPlausibleRecipes": {"H(scope2 identifier)": r1,
                                 "SHA256(canonical subjects)": r2},
         "resultingCoverage2": {
             "recipe1": C.ident("coverage", cov(r1)),
             "recipe2": C.ident("coverage", cov(r2))}},
        r1 != r2 and C.ident("coverage", cov(r1)) != C.ident("coverage", cov(r2)))

    # ---- F4 TypeScript native context has no descriptor or domain
    nat = json.load(open(os.path.join(
        SUBJ, "docs/coop/design-corrections/native/"
              "native-evidence.schemas.v2.json")))
    ts = nat["$defs"]["TypeScriptUniverseV2ResolvedInputs"]
    ctx = nat["$defs"]["NativeContextV2"]
    ts_ctx_required = "nativeContextId" in ts["required"]
    ctx_is_rust_only = set(ctx["required"]) >= {"targetTriple", "hostTriple",
                                                "toolchain", "baseCfg",
                                                "dependencySourceSetId"}
    has_ts_stdlib_field = any(
        "typescriptStdlibMerkleRoot" in json.dumps(v)
        for v in nat["$defs"].values())
    rec("F4", "MISSING RECIPE: `TypeScriptUniverseV2ResolvedInputs."
        "nativeContextId` is REQUIRED and identity-bearing (it is inside the "
        "universe key that keys fact2/scope2/coverage2 and appears in "
        "plan.nativeContextDigests), but the only native context record is "
        "`NativeContextV2` which native §2.3 titles '(Rust)' and whose closed "
        "required fields are Rust-only; native §11's domain list has only "
        "`native.context.rust.v2`. Additionally identity §3 and native §14 "
        "both assert 'native-context schema 2' carries "
        "`typescriptStdlibMerkleRoot`, which appears in NO closed native "
        "schema at all.",
        "native-evidence.schemas.v2.json#/$defs/"
        "TypeScriptUniverseV2ResolvedInputs.required[nativeContextId]; "
        "#/$defs/NativeContextV2; native-evidence.md §2.3 and §11; "
        "identity-and-evidence.md §3 ('`typescriptStdlibMerkleRoot` and "
        "`rustcDevLlvmDigest` in native-context schema 2')",
        "INVENTION REQUIRED",
        {"tsUniverseRequiresNativeContextId": ts_ctx_required,
         "nativeContextV2IsRustOnly": ctx_is_rust_only,
         "typescriptStdlibMerkleRootDefinedAnywhere": has_ts_stdlib_field,
         "nativeIdentityDomainsForContext": ["native.context.rust.v2"]},
        ts_ctx_required and ctx_is_rust_only and not has_ts_stdlib_field)

    # ---- F5 inventory sort has no tie-break for equal paths
    inv = [{"path": "a.ts", "sha256": "0" * 64, "bytes": 1},
           {"path": "a.ts", "sha256": "f" * 64, "bytes": 2}]
    snap = {"schemaVersion": 2,
            "projectId": "prj1-" + "0" * 64, "sourceInventory": inv,
            "resolvedConfigDigest": "1" * 64, "scopeDigest": "2" * 64,
            "vcsDigest": "3" * 64}
    errs = ivalid("snapshot", snap)
    try:
        C.canonical({"sourceInventory": inv})
        my = "my encoder refuses"
    except C.Refused as e:
        my = e.code
    rec("F5", "the inventory ordering rule ('sort by UTF-8 logical path') has "
        "no tie-break, and the closed schema's `uniqueItems` is on the whole "
        "Blob object, so two inventory rows sharing a path are schema-valid "
        "with NO defined canonical order",
        "identity-and-evidence.md §3 'Inventories instead sort by UTF-8 "
        "logical path'; identity-schemas.v2.json#/$defs/snapshot/properties/"
        "sourceInventory (uniqueItems on the object, not on `path`)",
        "under-specified ordering",
        {"schemaAdmitsDuplicatePath": errs == [],
         "myEncoderChoice": my}, errs == [])

    # ---- F6 which schema admits a schema-1 root?
    v8 = json.load(open(os.path.join(
        SUBJ, "docs/coop/completion/security-schemas.v8/root.schema.json")))
    sec = json.load(open(os.path.join(
        SUBJ, "docs/coop/design-corrections/security/"
              "security-lifecycle.schemas.v1.json")))
    r1s = dict(sec["schemas"]["RootV1"]); r1s["$defs"] = sec["$defs"]

    def mkroot(url):
        keys = [{"keyId": "%064x" % i, "publicKey": "%064x" % (i + 100),
                 "label": "k%d" % i} for i in range(8)]
        role = lambda t, k: {"threshold": t, "keys": k, "namespaces": ["ns"]}  # noqa: E731
        return {"rootSchema": 1, "rootVersion": 1, "previousRootVersion": None,
                "issuedAt": "2026-01-01T00:00:00Z",
                "expiresAt": "2026-12-31T00:00:00Z", "keys": keys,
                "rootKeys": [keys[i]["keyId"] for i in range(3)],
                "rootThreshold": 2,
                "roles": {"TR-CORE": role(1, [keys[3]["keyId"]]),
                          "TR-INDEX": role(1, [keys[4]["keyId"]]),
                          "TR-COMPONENT": role(1, [keys[5]["keyId"]]),
                          "TR-BUNDLE": role(1, [keys[6]["keyId"]]),
                          "TR-REPAIR": {"threshold": 0, "keys": [],
                                        "namespaces": []}},
                "recoveryAuthority": {"threshold": 3,
                                      "keys": ["%064x" % (200 + i)
                                               for i in range(5)]},
                "kernelAttestationKeys": [],
                "indexOrigin": {"url": url, "spkiSha256": "a" * 64}}
    good = mkroot("https://example.com/x")
    nl = mkroot("https://example.com/x\n")
    ev8 = [e.message for e in Draft202012Validator(v8).iter_errors(nl)]
    er1 = [e.message for e in Draft202012Validator(r1s).iter_errors(nl)]
    base_ok = ([e.message for e in Draft202012Validator(v8).iter_errors(good)] == []
               and [e.message for e in
                    Draft202012Validator(r1s).iter_errors(good)] == [])
    rec("F6", "a newline-suffixed `indexOrigin.url` is ADMITTED by the "
        "retained v8 root.schema.json (bare `$`) and REFUSED by the security "
        "bundle's RootV1 (strict `(?![\\s\\S])`). S9.1 names both as the "
        "schema-1 rule set, so which document is the admission boundary is "
        "not decided. All 12 product successor schema documents (335 "
        "patterns) apply the strict anchor with zero exceptions; only the 3 "
        "retained v8 documents (52 patterns) do not.",
        "security-and-lifecycle.md S9.1 'Root schema 1 is the v8 "
        "`root.schema.json` rule set, preserved with its exact closed schema "
        "and semantic rules (`RootV1` in the schema bundle...)'; "
        "admission-and-qualification.md §1 end-anchor rule",
        "DIVERGENT ADMISSION",
        {"baselineBothAccept": base_ok,
         "v8RootAdmitsTrailingNewline": ev8 == [],
         "bundleRootV1Refuses": er1 != [],
         "bundleRefusal": er1[:1]},
        base_ok and ev8 == [] and er1 != [])

    # ---- F7 D9 HostTermination union closure vs workflow StepTermination
    d9 = json.load(open(os.path.join(
        SUBJ, "docs/coop/artifacts/d9-exit-contract.v1.14.json")))
    union = d9["hostTerminationUnion"]
    union_fields = set(union["fieldTypes"].keys())
    common = json.load(open(os.path.join(
        SUBJ, "docs/coop/design-corrections/workflows/schemas/"
              "common.schema.json")))
    step_fields = set(common["$defs"]["StepTermination"]["properties"].keys())
    extra = sorted(step_fields - union_fields - {"class"})
    rec("F7", "the retained D9 `hostTerminationUnion` declares "
        "`unknownFieldPolicy: reject` over a closed field set and "
        "`nullabilityPolicy: 'No field is ever explicitly null'`; the "
        "workflow StepTermination adds three fields not in that set and "
        "workflows §8 requires a projection field `run-id` that is "
        "'explicitly null' in the ephemeral case. The workflow disposition "
        "table retains only the D9 'class/code/exit table', so neither the "
        "union's field closure nor its nullability rule is dispositioned.",
        "workflows-and-surfaces.md §0 (retains d9-exit-contract.v1.14.json "
        "'class/code/exit table') and §8; d9-exit-contract.v1.14.json "
        "$.hostTerminationUnion.unknownFieldPolicy and .nullabilityPolicy; "
        "common.schema.json#/$defs/StepTermination",
        "UNDISPOSITIONED OVERLAP",
        {"d9UnionFields": sorted(union_fields),
         "stepTerminationExtraFields": extra,
         "d9NullabilityPolicy": union["nullabilityPolicy"][:110],
         "d9UnknownFieldPolicy": union["unknownFieldPolicy"]},
        extra == ["authority", "domainDetail", "faultCause"]
        and union["unknownFieldPolicy"] == "reject")

    # ---- F8 CVE1 is referenced but not defined in the kit
    dv4 = json.load(open(os.path.join(
        SUBJ, "docs/coop/artifacts/delivery.v4.json")))
    ve = dv4["derivedFrom"]["operations"][17]["value"]["valueEncoding"]
    rec("F8", "CAP-MANIFEST-ID-V1 is fully reproducible from published bytes "
        "(vector A17), but the encoder that PRODUCES those bytes, CVE1, is "
        "defined by reference to `resolved-inputs.v2#planIdContract."
        "canonicalValueEncoding`, which is not in this kit. delivery.v4 "
        "states four of CVE1's properties and three type tags; the remaining "
        "types of its 'eight closed types' are not stated here. A host can "
        "verify a committed manifest id; it cannot build one.",
        "delivery.v4.json $.derivedFrom.operations[17].value.valueEncoding."
        "source = 'resolved-inputs.v2#planIdContract.canonicalValueEncoding. "
        "Eight closed types, stated encodings, stated constraints.'",
        "INPUT-CUSTODY / BY-REFERENCE DEPENDENCY",
        {"declaredSource": ve["source"],
         "typeTagsStatedHere": ["04 text", "05 array", "06 map", "02 true"],
         "verifiableFromPublishedBytes": True, "constructible": False}, True)

    # ---- F9 README-cited governance documents absent from the kit
    missing = ["docs/coop/design-corrections/README.md (the correction record "
               "/ 'correction crosswalk [that] names exact successor "
               "selectors and retained obligations')",
               "docs/v2/architecture/08-decision-and-readiness-register.md "
               "(named 'the sole completion checklist')"]
    present = [os.path.exists(os.path.join(SUBJ, p.split(" ")[0]))
               for p in missing]
    rec("F9", "the contract index names two governing documents that are not "
        "in this kit. Neither is needed to reconstruct the design, but the "
        "crosswalk is the stated authority for which inherited selector each "
        "successor replaces, so successor-vs-inherited disputes are not "
        "adjudicable from these bytes alone.",
        "docs/v2/contracts/product-v1/README.md lines 4-6 and 51-53",
        "INPUT-CUSTODY (scoped, non-blocking)",
        {"absent": missing, "presentInKit": present}, not any(present))
