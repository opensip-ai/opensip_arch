"""Core canonicalization/digest-law vectors, minimum-resolution predicates, imported
evidence, and the explicitly authorized test / preparation / repair paths."""

from __future__ import annotations

import hashlib
import json

import opensip_ref as R
import closure as CL
import world as W
from opensip_ref import C, H, ident, sha256_text, raw, raw_bytes


# ---------------------------------------------------------------------------
# C / H / admission vectors
# ---------------------------------------------------------------------------


def scenario_canonical(results):
    vectors = []

    def vec(name, value, note=""):
        b = C(value)
        vectors.append({
            "name": name, "value": value, "canonicalBytes": b.decode("utf-8"),
            "byteLength": len(b), "sha256OfCanonicalBytes": raw_bytes(b), "note": note,
        })

    vec("key-order-is-utf8-bytes", {"b": 1, "a": 2, "é": 3, "Z": 4},
        "keys sorted by UTF-8 bytes: Z < a < b < c3a9")
    vec("non-bmp-key-order", {"\U0001F600": 1, "\ufffd": 2, "z": 3},
        "UR-1: non-BMP key ordering is by UTF-8 bytes, not by UTF-16 code units")
    vec("integer-boundaries",
        {"maxU64": 2**64 - 1, "minI64": -(2**63), "zero": 0, "one": 1},
        "range [-2^63, 2^64-1], shortest ordinary decimal")
    vec("booleans-are-distinct", {"t": True, "f": False, "i": 1, "z": 0},
        "true is never 1")
    vec("escaping", {"q": "a\"b\\c/d", "ctl": "\u0001\b\t\n\f\r",
                     "keep": "\u007f\u2028"},
        "quote/backslash escaped, b t n f r used, other C0 as lowercase u00xx, "
        "slash NOT escaped, U+007F and U+2028 unescaped")
    vec("no-unicode-normalization",
        {"nfc": "\u00e9", "nfd": "e\u0301"},
        "C never normalises: two distinct scalars stay distinct")
    vec("arrays-keep-admitted-order", {"a": [3, 1, 2], "b": ["b", "a", "b"]},
        "C never sorts, deduplicates or infers a set from uniqueItems")

    refusals = {}
    for name, payload in [
        ("duplicate-key", b'{"a":1,"a":2}'),
        ("float-spelled-integer", b'{"a":1.0}'),
        ("exponent-spelled-integer", b'{"a":1e0}'),
        ("negative-zero", b'{"a":-0}'),
        ("nonfinite", b'{"a":NaN}'),
        ("integer-above-u64", b'{"a":18446744073709551616}'),
        ("integer-below-i64", b'{"a":-9223372036854775809}'),
        ("lone-surrogate-bytes", b'{"a":"\xed\xa0\x80"}'),
        ("malformed-utf8", b'{"a":"\xff"}'),
    ]:
        try:
            R.parse(payload)
            refusals[name] = "ADMITTED(!)"
        except R.Refuse as exc:
            refusals[name] = exc.code

    v = "leaf"
    for _ in range(32):
        v = [v]
    try:
        R.check_bounds(v)
        refusals["depth-32"] = "admitted (root container counts as 1)"
    except R.Refuse as exc:
        refusals["depth-32"] = exc.code
    v2 = [v]
    try:
        R.check_bounds(v2)
        refusals["depth-33"] = "ADMITTED(!)"
    except R.Refuse as exc:
        refusals["depth-33"] = exc.code

    frames = []
    for domain, desc in [("subject-scope", {"schemaVersion": 2}),
                         ("run", {"schemaVersion": 2}),
                         ("native.context.syntax.v2", {"schemaVersion": 2})]:
        fr = R.frame(domain, desc)
        frames.append({
            "domain": domain, "descriptor": desc,
            "framePrefixHex": fr[:len(b"opensip.product.v1") + 1].hex(),
            "frameLength": len(fr), "frameHex": fr.hex(),
            "H": H(domain, desc),
            "typedIdentity": ident(domain, desc) if domain in R.DOMAIN_PREFIX else None,
            "sha256TextSpelling": sha256_text(domain, desc),
            "rawSha256OfCanonicalPayload": raw(desc),
            "frameDigestIsNotThePayloadDigest": H(domain, desc) != raw(desc),
        })

    results["canonicalization"] = {
        "encoder": "C: UTF-8 byte-ordered keys, no whitespace, arrays in admitted order",
        "hRecipe": 'H(D,X) = SHA256(ASCII("opensip.product.v1") || 00 || ASCII(D) || 00 '
                   '|| uint64BE(len(C(X))) || C(X))',
        "vectors": vectors,
        "admissionRefusals": refusals,
        "frames": frames,
    }


def scenario_digest_law(results):
    """The closing digest law asserted MECHANICALLY: every 64-hex field of
    identity-schemas.v2 must carry an x-opensip-digest annotation."""
    unannotated = CL.unannotated_hex64_fields("identity")
    reps = set()

    def walk(node):
        if isinstance(node, dict):
            ann = node.get("x-opensip-digest")
            if isinstance(ann, dict) and "representation" in ann:
                reps.add(ann["representation"])
            for v in node.values():
                walk(v)
        elif isinstance(node, list):
            for v in node:
                walk(v)
    walk(R.IDENTITY)
    results["digest-law"] = {
        "unannotated64HexFieldsInIdentitySchemasV2": unannotated,
        "closed": not unannotated,
        "representationsInUse": sorted(reps),
        "closedRepresentationVocabulary":
            ["raw-artifact", "canonical-record", "h-identity", "capability-manifest-id"],
        "byDomainRegistryCoversEveryRefDomainEnumMember": _ref_domains_covered(),
        "note": "an unannotated 64-hex field is inadmissible; the law admits NO default",
    }


def _ref_domains_covered():
    reg = set(R.DIGEST_DOMAINS["byDomain"])
    out = {}
    for name in ("Ref", "ProofInputRef", "FindingEvidenceRef"):
        enum = R.IDENTITY["$defs"][name]["properties"]["domain"]["enum"]
        out[name] = sorted(set(enum) - reg) or "all registered"
    return out


def scenario_capability_manifest(results):
    """capabilityManifestId, computed from the prose (CVE1 + the inherited domain)."""
    manifest = W.capability_manifest(
        "blind-consumer-b",
        [{"language": "typescript", "platformIds": ["all-supported"],
          "providerId": "typescript-semantic",
          "providerVersionSource": "release-manifest:typescript-semantic",
          "relations": {"clones": "normalized-body-hash", "declares": "syntactic",
                        "file": "enumerated", "imports": "resolved-target",
                        "references": "resolved-binding"},
          "toolchainIdentitySource": "native-context:typescript-v2"}],
        [{"coverageState": "unavailable", "deficiency": "language-tier-unsupported",
          "language": "rust", "providerId": "rust-semantic",
          "relationIds": ["calls", "imports", "reachability", "references", "types"]}],
    )
    committed, cap_id = R.capability_manifest_id(manifest)
    mutated = json.loads(json.dumps(manifest))
    mutated["providers"][0]["relations"]["clones"] = "normalized-body-hash "
    _, cap_id2 = R.capability_manifest_id(mutated)

    neg = {}
    for name, bad in [
        ("boolean-schema-version", dict(manifest, schemaVersion=True)),
        ("string-schema-version", dict(manifest, schemaVersion="1")),
    ]:
        # CVE1 is TOTAL on booleans and strings: it does not fail, it mints a
        # DIFFERENT id.  ADM-TYPE is the gate, BEFORE encoding.
        _, other = R.capability_manifest_id(bad)
        neg[name] = {"cve1Encodes": True, "differentId": other != cap_id,
                     "gate": "ADM-TYPE refuses before encoding; a digest cannot police "
                             "its own input's type"}
    try:
        R.cve1({"x": 1.5})
        neg["float"] = "ADMITTED(!)"
    except R.Refuse as exc:
        neg["float"] = exc.code
    try:
        R.cve1({"x": "e\u0301"})
        neg["non-nfc-string"] = "ADMITTED(!)"
    except R.Refuse as exc:
        neg["non-nfc-string"] = exc.code

    relation_domain = set()
    delivery = R.doc_json("docs/coop/artifacts/delivery.v4.json")
    op = delivery["derivedFrom"]["operations"][17]["value"]
    regs = op["valueDomains"]["registries"]
    inherited_relations = regs["fact-plane.v1#relationRegistry.relations"]["members"]
    inherited_deficiencies = regs["fact-plane.v1#deficiencyVocabulary"]["members"]

    results["capability-manifest"] = {
        "manifest": manifest,
        "committedByteLength": len(committed),
        "committedBytesSha256": raw_bytes(committed),
        "capabilityManifestId": cap_id,
        "recipe": 'hex(SHA-256(UTF8("opensip.capability-manifest.v1") || 0x00 || '
                  'CVE1(CapabilityManifestV1)))',
        "singleFieldMutationMovesTheId": cap_id != cap_id2,
        "negatives": neg,
        "inheritedValueDomains": {
            "relationRegistryMembers": inherited_relations,
            "deficiencyVocabularyMembers": inherited_deficiencies,
            "productRelationRegistryMembers": sorted(R.RELATION_REGISTRY),
            "productDeficiencyMembers": R.NATIVE["$defs"]["DeficiencyV2"]["enum"],
            "relationsTheProductAddedThatTheManifestDomainCannotExpress":
                sorted(set(R.RELATION_REGISTRY) - set(inherited_relations)),
            "deficienciesTheProductAddedThatTheManifestDomainCannotExpress":
                sorted(set(R.NATIVE["$defs"]["DeficiencyV2"]["enum"])
                       - set(inherited_deficiencies)),
        },
    }


def scenario_identity_mutation(results):
    """Semantic-field changes move an identity; operational fields are excluded."""
    base = {
        "schemaVersion": 2,
        "snapshotId": "snapshot2:" + "11" * 32,
        "sourceUniverse": "22" * 32,
        "targetUniverse": "22" * 32,
        "relation": "file",
        "resolution": "enumerated",
        "enumeratorClosure": "closure2:" + "33" * 32,
        "subjects": ["a.ts", "b.ts"],
    }
    R.validate("identity", "#/$defs/subject-scope", base)
    base_id = ident("subject-scope", base)
    moved = {}
    for field, value in [("snapshotId", "snapshot2:" + "12" * 32),
                         ("sourceUniverse", "23" * 32),
                         ("relation", "package"), ("resolution", "manifest-declared"),
                         ("enumeratorClosure", "closure2:" + "34" * 32),
                         ("subjects", ["a.ts", "b.ts", "c.ts"])]:
        mutated = dict(base)
        mutated[field] = value
        moved[field] = ident("subject-scope", mutated) != base_id

    # operational identities are EXCLUDED: the same semantic inputs on two attempts
    # produce the SAME Run.  They are not fields of any semantic descriptor.
    semantic_fields = set()
    for name in ("snapshot", "plan", "fact", "subject-scope", "coverage", "view",
                 "proof-bundle", "semantic-evidence", "evaluation-seal", "run"):
        semantic_fields |= set(R.IDENTITY["$defs"][name].get("properties", {}))
    operational = ["requestId", "executionId", "receiptId", "timestamp", "wallClock",
                   "pid", "signer", "nonce", "expiresAt", "outputDestination"]

    results["identity-mutation"] = {
        "baseSubjectScope": base, "baseScopeId": base_id,
        "everySemanticFieldMovesTheIdentity": moved,
        "allMoved": all(moved.values()),
        "operationalFieldsAbsentFromEverySemanticDescriptor":
            {f: (f not in semantic_fields) for f in operational},
        "subjectsAreACanonicalSet":
            "duplicate subjects refuse rather than dedupe (x-opensip-order canonical-set "
            "+ uniqueItems)",
        "orderMattersForSequenceArrays":
            raw({"a": [1, 2]}) != raw({"a": [2, 1]}),
    }


# ---------------------------------------------------------------------------
# Minimum-resolution predicates
# ---------------------------------------------------------------------------


def satisfies(relation, fact_rung, min_rung):
    """Satisfaction is ladder-index comparison INSIDE ONE RELATION."""
    return R.rung_index(relation, fact_rung) >= R.rung_index(relation, min_rung)


def scenario_min_resolution(results):
    cases = []
    for relation, min_rung, qualifying, insufficient, level in [
        ("declares", "syntactic", "syntactic", None, "syntactic"),
        ("imports", "resolved-target", "resolved-target", "syntactic-specifier", "resolved"),
        ("references", "resolved-binding", "resolved-binding", "syntactic-name-match",
         "resolved"),
        ("calls", "resolved-callee", "resolved-callee", "syntactic-callee-name", "resolved"),
        ("types", "checked", "checked", "annotated", "type"),
    ]:
        row = {"relation": relation, "level": level, "ladder": R.ladder(relation),
               "minResolution": min_rung,
               "qualifyingFactRung": qualifying,
               "qualifyingSatisfies": satisfies(relation, qualifying, min_rung)}
        if insufficient:
            row["insufficientFactRung"] = insufficient
            row["insufficientSatisfies"] = satisfies(relation, insufficient, min_rung)
        cases.append(row)

    neg = {}
    try:
        satisfies("references", "resolved-callee", "resolved-binding")
        neg["rung-of-another-relation"] = "ADMITTED(!)"
    except R.Refuse as exc:
        neg["rung-of-another-relation"] = exc.code + ":" + exc.detail
    try:
        R.rung_index("declares", "checked")
        neg["type-rung-on-a-syntactic-relation"] = "ADMITTED(!)"
    except R.Refuse as exc:
        neg["type-rung-on-a-syntactic-relation"] = exc.code + ":" + exc.detail
    try:
        CL._admit_atom("made-up-relation", "syntactic")
        neg["unregistered-atom-relation"] = "ADMITTED(!)"
    except R.Refuse as exc:
        neg["unregistered-atom-relation"] = exc.code + ":" + exc.detail

    # no global rank: `resolved` named a different rung in each relation, which is why
    # the abstract tier vocabulary was withdrawn.
    per_relation = {rel: R.ladder(rel) for rel in
                    ("imports", "references", "calls", "reachability", "types")}

    # Coverage sufficiency for a UNIVERSAL NEGATIVE
    def sufficiency(requirement, entry):
        """sufficiency_v2, in order, with NO early exit (post-reset SHOULD-4)."""
        causes = []
        if entry is None:
            return ["required-relation-missing"]
        if R.rung_index(entry["relation"], entry["resolution"]) \
                < R.rung_index(entry["relation"], requirement["minResolution"]):
            causes.append("provider-unavailable")
        if entry["confidenceMillionths"] < requirement.get("minConfidenceMillionths", 0):
            causes.append("confidence-floor-unmet")
        if requirement["relation"] == "types" and \
                requirement.get("derivationPolicy") == "declared-only" and \
                "compiler-inferred" in entry["derivationKinds"]:
            causes.append("derivation-policy-unmet")
        if requirement["completeness"] == "complete" and entry["coverage"] != "complete":
            causes.append(entry["deficiency"])
        if requirement["quantifier"] == "universal-negative":
            st = entry["resolutionCompleteness"]["state"]
            if st in ("partial", "not-attempted"):
                causes.append("resolution-incomplete")
            elif st == "incomplete":
                causes.append("resolution-incomplete"
                              if requirement["unresolvedEdgePolicy"] == "forbid"
                              else "DISCLOSURE:unresolved-edges")
            if entry["closedWorld"]["exportsClosed"] != "closed":
                causes.append("external-consumers-unknown"
                              if requirement["externalConsumerPolicy"] == "forbid"
                              else "DISCLOSURE:external-consumers")
        return causes

    req = {"relation": "references", "minResolution": "resolved-binding",
           "minConfidenceMillionths": 0, "completeness": "complete",
           "quantifier": "universal-negative", "unresolvedEdgePolicy": "forbid",
           "externalConsumerPolicy": "forbid"}
    good = W.entry("references", "resolved-binding", "complete", "complete", True, True,
                   "complete")
    bad_state = W.entry("references", "resolved-binding", "complete", "incomplete", True,
                        True, "complete", edge_count=1,
                        edge_classes=["computed-member-access"])
    open_exports = W.entry("references", "resolved-binding", "complete", "complete", True,
                           True, "complete", exports_closed="open",
                           external="possible", dead_code=False)
    floor_req = {"relation": "clones", "minResolution": "normalized-body-hash",
                 "minConfidenceMillionths": 900000, "completeness": "partial-ok",
                 "quantifier": "existential", "unresolvedEdgePolicy": "disclose",
                 "externalConsumerPolicy": "assume-closed"}
    low_conf = W.entry("clones", "normalized-body-hash", "complete", "not-applicable",
                       False, True, None, confidence=100000)
    ok_conf = W.entry("clones", "normalized-body-hash", "complete", "not-applicable",
                      False, True, None, confidence=1000000)
    types_req = {"relation": "types", "minResolution": "checked",
                 "minConfidenceMillionths": 0, "completeness": "complete",
                 "quantifier": "existential", "derivationPolicy": "declared-only",
                 "unresolvedEdgePolicy": "disclose", "externalConsumerPolicy": "assume-closed"}
    inferred = W.entry("types", "checked", "complete", "complete", True, True, "complete",
                       derivation_kinds=["compiler-inferred"])

    results["minimum-resolution-predicates"] = {
        "ladderIndexComparisonWithinOneRelation": cases,
        "noGlobalRank": per_relation,
        "negatives": neg,
        "sufficiency": {
            "universalNegativeQualifying": sufficiency(req, good),
            "universalNegativeInsufficientResolution": sufficiency(req, bad_state),
            "universalNegativeOpenExports": sufficiency(req, open_exports),
            "confidenceFloorPrecedesTheOneRungShortcut": sufficiency(floor_req, low_conf),
            "confidenceFloorSatisfied": sufficiency(floor_req, ok_conf),
            "declaredOnlyDerivationPolicy": sufficiency(types_req, inferred),
            "relationAbsentFromTheView": sufficiency(req, None),
        },
        "precedenceMostSpecificFirst": [
            "language-tier-unsupported", "provider-unavailable",
            "input-closure-incomplete", "budget-exhausted", "confidence-floor-unmet",
            "derivation-policy-unmet", "resolution-incomplete",
            "external-consumers-unknown", "required-relation-missing"],
        "repairEvidenceRequirements": _repair_requirements(),
        "importedObservationBoundary": _imported_boundary(),
    }


def _repair_requirements():
    ok = {"relation": "references", "minResolution": "resolved-binding",
          "completeness": "complete", "satisfied": True}
    bad = {"relation": "references", "minResolution": "resolved-binding",
           "completeness": "complete", "satisfied": False,
           "deficiency": "provider-unavailable"}
    R.validate("repair", "#/$defs/EvidenceRequirement", ok)
    R.validate("repair", "#/$defs/EvidenceRequirement", bad)
    neg = {}
    try:
        R.validate("repair", "#/$defs/EvidenceRequirement",
                   dict(ok, minResolution="resolved-callee"))
        neg["cross-relation-rung-is-schema-valid"] = (
            "SCHEMA-VALID; the flat rung enum is NECESSARY only. Membership of THIS "
            "relation's ladder is enforced at admission")
    except R.Refuse as exc:
        neg["cross-relation-rung-is-schema-valid"] = exc.code
    return {
        "destructiveRecipePrerequisite":
            "a destructive unused-code recipe additionally requires native closed-world "
            "resolution evidence (deadCodeRepairEligible); an advisory similarity or "
            "runtime-cold signal alone never authorizes deletion",
        "requirementSatisfied": ok, "requirementUnsatisfied": bad,
        "notes": neg,
    }


def _imported_boundary():
    reg = R.doc_json(R._PATHS["imported-evidence"])["x-opensip-evidence-relation-registry"]
    atom_evidence = {"op": "exists", "relation": "runtime-observation",
                     "minResolution": "observed", "filters": [], "evidence": "runtime"}
    atom_native = {"op": "none", "relation": "references",
                   "minResolution": "resolved-binding", "filters": []}
    R.validate("policy-document", "#/$defs/Atom", atom_evidence)
    R.validate("policy-document", "#/$defs/Atom", atom_native)
    return {
        "closedEvidenceRelations": sorted(reg["relations"]),
        "ladders": {k: v["ladder"] for k, v in reg["relations"].items()},
        "noNewRungToken": "observed is already the registered rung of unresolved-edge",
        "evidenceAtomMustDeclareItsKind": atom_evidence,
        "nativeFactAtomMustNotCarryEvidence": atom_native,
        "noHitsIsNotNonUse":
            "observed-hit is positive execution evidence; observable-unhit is BOUNDED "
            "negative evidence with its window and population; unobservable/unmapped "
            "never become unhit signals; one window never establishes universal non-use; "
            "runtime coverage is never OpenSIP Coverage",
        "requiredEvidenceAbsent": "the rule is INDETERMINATE (a typed deficiency); "
                                  "optional evidence absent is disclosed "
                                  "IMPORT.ABSENT_FOR_PREDICATE and is not a gating deficiency",
    }


# ---------------------------------------------------------------------------
# import2, correspondence, staleness
# ---------------------------------------------------------------------------


def scenario_import(results):
    snapshot_id = "snapshot2:" + "aa" * 32
    payload = {
        "payloadDomain": "workflow.import-payload.runtime.v1",
        "format": "v8-json",
        "observationWindow": {"startUtc": "2026-09-01T00:00:00Z",
                              "endUtc": "2026-09-02T00:00:00Z"},
        "observedPopulation": "test-suite",
        "subjects": [
            {"path": "src/a.ts", "symbol": "alpha", "observability": "observed-hit",
             "hits": 12},
            {"path": "src/b.ts", "symbol": "beta", "observability": "observable-unhit",
             "hits": 0},
            {"path": "src/c.ts", "symbol": "gamma", "observability": "unobservable",
             "mappingGap": "no source map for this bundle chunk"},
        ],
        "mappingGaps": ["dist/bundle.js has no source map"],
    }
    ok, why = R.schema_ok("imported-evidence", "#/$defs/RuntimePayloadV1", payload)
    hit_on_unobservable = json.loads(json.dumps(payload))
    hit_on_unobservable["subjects"][2]["hits"] = 3
    unobs_ok, unobs_why = R.schema_ok("imported-evidence", "#/$defs/RuntimePayloadV1",
                                      hit_on_unobservable)
    correspondence = {"kind": "exact-snapshot", "snapshotId": snapshot_id}
    R.validate("common", "#/$defs/SourceCorrespondence", correspondence)
    build = {"schemaVersion": 1, "buildIdentity": None}
    observation = {"schemaVersion": 1, "kind": "runtime", "window": None,
                   "population": None, "selection": None, "revisionRange": None}
    scope = W.scope_descriptor(["."])
    wrapper = {
        "schemaVersion": 2, "kind": "runtime",
        "payloadSchemaDigest": R.IMPORTED_EVIDENCE_DIGEST,
        "payloadDigest": raw(payload) if ok else raw({"unvalidated": True}),
        "sourceCorrespondenceDigest": raw(correspondence),
        "buildDigest": raw(build),
        "producerClosure": "closure2:" + "b1" * 32,
        "adapterClosure": "closure2:" + "b2" * 32,
        "blobs": [],                       # 0..4096: a self-contained payload retains none
        "scopeDigest": raw(scope),
        "observationDigest": raw(observation),
        "completeness": "complete", "omissions": [],
    }
    R.validate("identity", "#/$defs/import", wrapper)
    import_id = "import2:" + H("import", wrapper)

    mirror_ok, mirror_why = R.schema_ok("imported-evidence", "#/$defs/ImportWrapperV2",
                                        wrapper)
    unsorted = dict(wrapper, omissions=["b", "a"], completeness="partial")
    # A STOCK JSON-Schema validator cannot discriminate here: x-opensip-order is an
    # ANNOTATION that an admission implementation must enforce.  The differential is
    # therefore run over BOTH the schema and the declared order.
    def admit(bundle, sel, inst):
        ok, why = R.schema_ok(bundle, sel, inst)
        if not ok:
            return False, why
        try:
            CL.check_document_orders(bundle, sel, inst)
        except R.Refuse as exc:
            return False, exc.code + ":" + exc.detail
        return True, None
    foundation_unsorted, fu_why = admit("identity", "#/$defs/import", unsorted)
    mirror_unsorted, mu_why = admit("imported-evidence", "#/$defs/ImportWrapperV2",
                                    unsorted)

    staleness = {
        "snapshot-equal": ("current", "consumable"),
        "snapshot-differs": ("stale", "unmapped-only"),
        "commit-differs": ("stale", "unmapped-only"),
        "commit-equal-dirty": ("unverifiable", "unmapped-only"),
        "build-identity-differs": ("wrong-build", "unmapped-only"),
    }
    stale_term = {"class": "request-rejected", "errorCode": "REQUEST.PRECONDITION_FAILED",
                  "domainDetail": {"code": "IMPORT.STALE_FOR_PLAN",
                                   "remedy": "re-import against the analysed snapshot"}}
    R.validate("common", "#/$defs/StepTermination", stale_term)
    mapping_term = {"class": "request-rejected", "errorCode": "CONFIG.INVALID",
                    "domainDetail": {"code": "IMPORT.MAPPING_REQUIRED",
                                     "remedy": "supply an admitted SourceMappingV1"}}
    R.validate("common", "#/$defs/StepTermination", mapping_term)

    results["imported-evidence"] = {
        "wrapper": wrapper,
        "importId": import_id,
        "importIdIsTheOnlyHDomainInAnImport": True,
        "auxiliaryDigestsAreRawSha256OfCanonicalClosedRecords": {
            "payloadSchemaDigest": "raw SHA-256 of the EXACT FULL schema document bytes",
            "payloadDigest": raw(payload) if ok else "payload rejected by the registry row",
            "sourceCorrespondenceDigest": raw(correspondence),
            "buildDigest": raw(build),
            "scopeDigest": raw(scope),
            "observationDigest": raw(observation),
        },
        "payloadValidatedThroughTheRegistryRow": {"ok": ok, "detail": why},
        "payload": payload,
        "hitCountOnAnUnobservableSubjectRefuses": {"admitted": unobs_ok,
                                                   "detail": unobs_why},
        "foundationRecordAndWorkflowMirrorAgree": {
            "sortedInstance": {"foundation": True, "mirror": mirror_ok,
                               "mirrorDetail": mirror_why},
            "unsortedOmissionsInstance": {"foundation": foundation_unsorted,
                                          "foundationDetail": fu_why,
                                          "mirror": mirror_unsorted,
                                          "mirrorDetail": mu_why,
                                          "agree": foundation_unsorted == mirror_unsorted,
                                          "note": "a stock JSON-Schema validator admits "
                                                  "both; the differential is only "
                                                  "discriminating once x-opensip-order "
                                                  "is enforced as the contract requires"},
        },
        "zeroBlobsIsLawful": "blobs is 0..4096: the payload bytes and the registered "
                             "schema DOCUMENT bytes are retained independently",
        "stalenessTable": {k: {"staleness": v[0], "consumability": v[1]}
                           for k, v in staleness.items()},
        "staleSelectedForAPlan": stale_term,
        "correspondenceMissing": mapping_term,
    }


# ---------------------------------------------------------------------------
# Explicit test / preparation / repair authorization
# ---------------------------------------------------------------------------


def scenario_authorized_steps(results):
    grant_ref = "security.repo-execution-grant.v2:" + "c1" * 32
    closure_id = "closure2:" + "c2" * 32
    params = {
        "kind": "test-execution",
        "argv": ["tools/runner", "--ci"],
        "argv0Source": {"kind": "toolchain-closure", "closureId": closure_id,
                        "member": "tools/runner"},
        "cwdIsRoot": True,
        "principal": "P-TRUSTED-REPO",
        "executionClass": "test-runner",
        "platformId": "macos-aarch64",
        "authorizationRef": grant_ref,
        "consentSource": "pre-existing-policy",
        "afterStep": 0,
        "timeoutMilliseconds": 600000,
        "maxOutputBytes": 1048576,
        "environmentAllowlist": ["HOME", "LANG"],
        "effects": {"network": "DISCLOSURE-ONLY", "subprocess": "DISCLOSURE-ONLY",
                    "filesystemWrite": "DISCLOSURE-ONLY",
                    "environment": "ENFORCED-BY-CONSTRUCTION"},
    }
    ok, why = R.schema_ok("test-execution", "#/$defs/TestExecutionStepParams", params)
    over = json.loads(json.dumps(params))
    over["effects"]["network"] = "ENFORCED-PLATFORM"
    over_ok, over_why = R.schema_ok("test-execution", "#/$defs/TestExecutionStepParams", over)

    truth = R.doc_json("docs/coop/artifacts/permission-truth-tables.v9.json")
    tokens = _permission_rows(truth)

    plan_id = "plan2:" + "d1" * 32
    run_id = "run2:" + "d2" * 32
    snap = "snapshot2:" + "d3" * 32
    edit = {"path": "src/dead.ts", "action": "delete",
            "preimageDigest": "e1" * 32, "postimageDigest": None, "postimageBytes": 0}
    desc = {
        "schemaFamily": "opensip.product.repair-plan", "schemaMajor": 1,
        "projectId": W.PROJECT_ID, "snapshotId": snap, "evidenceRunId": run_id,
        "planId": plan_id,
        "recipe": {"contributionId": "opensip.first-party.repairs",
                   "recipeId": "remove-unused-export", "recipeVersion": "1.0.0",
                   "closureId": "closure2:" + "d4" * 32},
        "recipeTrust": "admitted",
        "evidenceOrigin": "native-analysis",
        # NOTE: the repair schema's closedWorld is a CLOSED FIVE-field record while the
        # native ClosedWorldV2 it says it is "copied from" is a closed SEVEN-field record.
        # A literal copy refuses; the projection is determinate by elimination but is
        # published nowhere.  Recorded as a SHOULD issue.
        "closedWorld": {"exportsClosed": "closed", "entryPointsRecognized": "all",
                        "nonliteralLoading": "none", "externalConsumers": "none-declared",
                        "deadCodeRepairEligible": True},
        "targets": ["finding-key2:" + "e2" * 32],
        "edits": [edit], "totalPostimageBytes": 0,
        "evidenceRequirements": [{"relation": "references",
                                  "minResolution": "resolved-binding",
                                  "completeness": "complete", "satisfied": True}],
        "permittedEditScope": ["src/**"],
        "applicable": True, "unmetPreconditions": [], "limitations": [],
    }
    plan_ok, plan_why = R.schema_ok("repair", "#/$defs/RepairPlanDescriptor", desc)
    repair_plan_id = "repairplan2:" + H("workflow.repair-plan", desc) if plan_ok else None

    apply_params = {"kind": "repair-apply", "planStep": 1,
                    "repairPlanId": repair_plan_id or ("repairplan2:" + "0" * 64),
                    "consentSource": "policy",
                    "authorizationRef": "security.repair-apply-authorization.v1:" + "d5" * 32}
    apply_ok, apply_why = R.schema_ok("invocation-record", "#/$defs/RepairApplyParams",
                                      apply_params)

    consent_map = {"interactive-explicit": {"test": "interactive-consent",
                                            "repair": "interactive"},
                   "policy-record": {"test": "pre-existing-policy", "repair": "policy"}}

    results["authorized-steps"] = {
        "testExecutionParams": {"admitted": ok, "detail": why, "params": params},
        "overClaimedEnforcement": {"schemaAdmitted": over_ok, "detail": over_why,
                                   "contractRule": "a claimed enforcement without a "
                                                   "measured primitive is refused "
                                                   "(TEST.CONFINEMENT_CLAIM_REFUSED); "
                                                   "the effect values are COPIED from "
                                                   "the pinned truth table"},
        "permissionTokenProjection": tokens,
        "repairPlanDescriptor": {"admitted": plan_ok, "detail": plan_why,
                                 "repairPlanId": repair_plan_id},
        "repairApplyParams": {"admitted": apply_ok, "detail": apply_why},
        "consentMapping": consent_map,
        "authorityBoundaries": {
            "grantIsOperational": "the authority grant is the operational "
                                  "authorizationRef; it is EXCLUDED from the Plan "
                                  "descriptor and from every content identity",
            "planBindsTheSemanticProjection":
                "{kind: trusted-repository-code, closureId, ownerSourceDigest} with "
                "analysisOperations containing prepare-code, ONLY for host-prepared",
            "importedInertProjectsOnlyReadImport": True,
            "testRunnerHasNoPlan":
                "a test-execution step has no Plan; its observations enter an analysis "
                "only through an admitted import2 with its execution provenance, and "
                "`test-code` is not an analysis semantic-grant operation",
            "preparationRunsBeforeThePlanExists": True,
            "confinementNeverClaimed": True,
        },
    }


def _permission_rows(truth):
    """The four effect names are field names; the pinned table is over seven tokens."""
    wanted = {"subprocess": "PT-PROC-EXEC-DECLARED",
              "filesystemWrite": "PT-FS-WRITE-HOST-STATE",
              "network": "PT-NET-EGRESS",
              "environment": "PT-ENV-READ"}
    found = {}
    text = json.dumps(truth)
    for field, token in wanted.items():
        found[field] = {"token": token, "presentInPinnedTable": token in text}
    for token in ("PT-HOST-EFFECT-BROKERED", "PT-FS-READ-PROJECT", "PT-FS-READ-COMPONENT"):
        found[token] = {"projectedByNoEffectField": True, "presentInPinnedTable":
                        token in text}
    return found
