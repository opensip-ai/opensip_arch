"""Mechanical substantiation of every gap this blind consumer reports.

Each probe reads only the kit's own normative bytes and reports what it
observed; nothing here is an opinion about intent.
"""

import json
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import osref as O
import graph as G

SUBJECT = G.SUBJECT
FINDINGS = []


def load(rel):
    return json.load(open(os.path.join(SUBJECT, rel)))


def probe(gid, severity, selectors, statement, observation, invention):
    FINDINGS.append({"id": gid, "severity": severity, "selectors": selectors,
                     "statement": statement, "observed": observation,
                     "whatAnImplementerMustInvent": invention})


# ---- G1: a registered payload schema DOCUMENT cannot constrain its payload --
def g1():
    import jsonschema
    from jsonschema import Draft202012Validator
    docs = {
        "native/native-evidence.schemas.v2.json (coverage, fact-adjacent, "
        "dependency + prepared import payloads)":
            "docs/coop/design-corrections/native/native-evidence.schemas.v2.json",
        "workflows/schemas/imported-evidence.schema.json (runtime + history payloads)":
            "docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json",
        "workflows/schemas/test-execution.schema.json (test payload)":
            "docs/coop/design-corrections/workflows/schemas/test-execution.schema.json",
    }
    obs = {}
    junk = {"this": "is not any registered payload", "n": 1}
    for label, rel in docs.items():
        doc = load(rel)
        root_keys = [k for k in doc if k not in ("$schema", "$id", "title",
                                                 "description", "$defs", "$comment")]
        vacuous = Draft202012Validator(doc).is_valid(junk)
        obs[label] = {"rootConstraintKeys": root_keys,
                      "arbitraryObjectValidatesAgainstTheWholeDocument": vacuous}
    ctl = load("docs/coop/design-corrections/foundation/import-source-context.schema.json")
    obs["control: foundation/import-source-context.schema.json"] = {
        "rootConstraintKeys": [k for k in ctl if k not in
                               ("$schema", "$id", "title", "description", "$defs")],
        "arbitraryObjectValidatesAgainstTheWholeDocument":
            Draft202012Validator(ctl).is_valid(junk)}
    probe(
        "G1", "MUST",
        ["identity-and-evidence.md section 3 (`a document offered as a *payload* "
         "schema must constrain the payload directly, so a multi-record bundle "
         "cannot pass vacuously`)",
         "native-evidence.md section 7.1 registry (kind -> schema DOCUMENT + `#/$defs/...` selector)",
         "native-evidence.md section 4.1a step 6 / section 7.2 (`the exact full schema DOCUMENT file bytes`)",
         "workflows-and-surfaces.md section 4 (`payloadSchemaDigest is raw SHA-256 of the entire schema document's bytes`)",
         "identity-schemas.v2.json #/$defs/coverage.payloadSchemaDigest, #/$defs/fact.payloadSchemaDigest, #/$defs/import.payloadSchemaDigest"],
        "identity section 3 forbids admitting a payload schema document that does "
        "not constrain the payload directly, while the native and workflow "
        "registries require exactly that document's digest for every registered "
        "payload kind, and every one of those documents is a multi-record bundle "
        "with an unconstrained root.",
        obs,
        "Which of the two rules governs. Either (a) `payloadSchemaDigest` names "
        "the document while validation uses the registry row's `#/$defs` selector "
        "-- in which case identity section 3's sentence is false as written and "
        "the selector, not the digest, is what constrains -- or (b) each payload "
        "needs its own single-record document, which no registry row names. The "
        "choice changes which bytes are hashed, so it changes coverage2, import2 "
        "and every fact2 identity.")


# ---- G2: two different canonical encoders for one fact payload -------------
def g2():
    fp = load("docs/coop/artifacts/fact-plane.v1.json")
    reg = fp["factRecordContractV1"]["relationPayloadSchemaRegistryV1"]
    ident = load("docs/coop/design-corrections/foundation/identity-schemas.v2.json")
    fact_payload = ident["$defs"]["fact"]["properties"]["payloadDigest"]["x-opensip-digest"]
    fact_schema = ident["$defs"]["fact"]["properties"]["payloadSchemaDigest"]["x-opensip-digest"]
    probe(
        "G2", "MUST",
        ["identity-schemas.v2.json #/$defs/fact.payloadDigest (x-opensip-digest = canonical-record)",
         "identity-and-evidence.md section 3 closing digest law, `canonical-record` row "
         "(`raw SHA256 of C(record)`)",
         "fact-plane.v1.json $.factRecordContractV1.relationPayloadSchemaRegistryV1.canonicalPayloadEncoding",
         "native-evidence.md section 0 (`Existing relation payload grammars are reused by "
         "exact payloadSchemaDigest inside fact2`) and section 4.4"],
        "The digest law makes fact2.payloadDigest the raw SHA-256 of the FOUNDATION "
        "canonical JSON bytes C(payload); the owning relation-payload registry, "
        "which native section 0 retains and extends rather than supersedes, "
        "declares a deterministic-CBOR canonical payload encoding with a "
        "different type profile and a different admission rule.",
        {"registryCanonicalPayloadEncoding": reg["canonicalPayloadEncoding"],
         "identityFactPayloadDigestAnnotation": fact_payload,
         "identityFactPayloadSchemaDigestAnnotation": fact_schema,
         "registryIsNotJsonSchemaDocuments": {
             "shape": sorted(reg["schemas"]["declares"].keys()),
             "note": "the registry rows are a bespoke required/optional/fields/enums "
                     "grammar inside a 59 KiB artifact, not schema documents"},
         "typeProfileDisagreement": {
             "foundationC": "integers [-2^63, 2^64-1], negatives allowed, NO Unicode normalization",
             "relationRegistryCBOR": "uint64 only, negative integers FORBIDDEN, non-NFC text FORBIDDEN"}},
        "Which encoder produces the bytes whose raw SHA-256 is fact2.payloadDigest, "
        "and which exact bytes are the `complete registered relation payload schema "
        "document` that fact2.payloadSchemaDigest names. No per-relation document "
        "exists anywhere in the kit, and a payload carrying a negative integer is "
        "admissible under one profile and inadmissible under the other. Two "
        "conforming implementations therefore mint different fact2 identities for "
        "one provider output.")


# ---- G3: the nodeModulesInReadSet=true branch has no preimage record -------
def g3():
    native = load("docs/coop/design-corrections/native/native-evidence.schemas.v2.json")
    defs = sorted(native["$defs"].keys())
    probe(
        "G3", "MUST",
        ["native-evidence.md section 2.4 table row `nodeModulesLayoutDigest` "
         "(`raw SHA-256 of the canonical resolvedNodeModulesLayout record`)",
         "native-evidence.schemas.v2.json #/$defs/TypeScriptNativeContextV2.nodeModulesLayoutDigest",
         "native-evidence.md section 2.2 (`resolvedNodeModulesLayout` listed as retained)"],
        "`nodeModulesLayoutDigest` is defined as the raw SHA-256 of the canonical "
        "`resolvedNodeModulesLayout` record, and no schema in the kit defines that "
        "record. The digest is null exactly when nodeModulesInReadSet=false, so the "
        "ONLY TypeScript universe an implementer can actually construct is one that "
        "does not read node_modules -- i.e. one in which every bare specifier is an "
        "`unresolved-module-specifier` unresolved edge.",
        {"definitionsMatchingNodeModules": [d for d in defs if "odeModules" in d],
         "definitionCount": len(defs),
         "consequence": "This blind consumer's positive TypeScript vector is forced "
                        "to nodeModulesInReadSet=false; the true branch is not "
                        "constructible from these inputs."},
        "The closed shape of `resolvedNodeModulesLayout` (which paths, which "
        "digests, which order annotation). Without it the ordinary "
        "bare-specifier-resolving TypeScript project has no admissible native "
        "context, which is the mainstream case the contract exists to serve.")


# ---- G4: native 2.2 names three fields the closed universe cannot carry ----
def g4():
    native = load("docs/coop/design-corrections/native/native-evidence.schemas.v2.json")
    uni = native["$defs"]["TypeScriptUniverseV2ResolvedInputs"]
    claimed = ["tsconfigGraphHash", "compilerOptions", "programRootFiles",
               "packageLockIdentity", "resolvedNodeModulesLayout",
               "executionCapableResolution"]
    present = sorted(uni["properties"].keys())
    probe(
        "G4", "SHOULD",
        ["native-evidence.md section 2.2 (`Retained: tsconfigGraphHash, "
         "compilerOptions (closed subset), programRootFiles, packageLockIdentity, "
         "resolvedNodeModulesLayout, executionCapableResolution`)",
         "native-evidence.schemas.v2.json #/$defs/TypeScriptUniverseV2ResolvedInputs "
         "(additionalProperties: false)",
         "resolved-inputs.v2.json $.planIdContract.semanticUniverseSchemas.typescript-v1.resolvedInputs.required"],
        "Section 2.2's `Retained:` list names three fields the closed successor "
        "record does not carry. An implementer building the record from the prose "
        "produces one that fails admission.",
        {"proseClaimsRetained": claimed,
         "closedRecordProperties": present,
         "namedButAbsent": [f for f in claimed if f not in present],
         "additionalProperties": uni.get("additionalProperties")},
        "Nothing semantic -- the closed schema is unambiguous and the three values "
        "moved into TypeScriptNativeContextV2 (honoredOptions, lockfileIdentity, "
        "nodeModulesLayoutDigest). But the prose is a normative-looking list that "
        "an implementer will build from, so it should say `relocated to the "
        "context` rather than `retained`.")


# ---- G5: tsconfigGraphHash has no producing recipe -------------------------
def g5():
    native = load("docs/coop/design-corrections/native/native-evidence.schemas.v2.json")
    field = native["$defs"]["TypeScriptUniverseV2ResolvedInputs"]["properties"]["tsconfigGraphHash"]
    ri = load("docs/coop/artifacts/resolved-inputs.v2.json")
    ts1 = ri["planIdContract"]["semanticUniverseSchemas"]["typescript-v1"]["resolvedInputs"]
    probe(
        "G5", "MUST",
        ["native-evidence.schemas.v2.json #/$defs/TypeScriptUniverseV2ResolvedInputs.tsconfigGraphHash",
         "native-evidence.md section 2.2 (`Retained: tsconfigGraphHash`)",
         "resolved-inputs.v2.json $.planIdContract.semanticUniverseSchemas.typescript-v1.resolvedInputs.canonicalization",
         "identity-and-evidence.md section 3 closing digest law (scoped to identity-schemas.v2 only)"],
        "`tsconfigGraphHash` is a 64-hex universe key -- any universe field change "
        "changes PlanId -- with no producing recipe anywhere in the kit. The "
        "closing digest law that would have forbidden an unannotated 64-hex field "
        "is scoped to identity-schemas.v2 and does not reach the native bundle, so "
        "this field is admissible with no declared meaning.",
        {"schemaEntry": field,
         "retainedFromV1Canonicalization": ts1.get("canonicalization"),
         "nativeBundleHas_x_opensip_digest_annotations":
             _count_annotation(native, "x-opensip-digest"),
         "identityBundleHas_x_opensip_digest_annotations":
             _count_annotation(load("docs/coop/design-corrections/foundation/"
                                    "identity-schemas.v2.json"), "x-opensip-digest")},
        "The exact preimage: which files, in which order, hashed with which "
        "encoder. Two conforming hosts analysing one repository will mint "
        "different typescript-v2 universe identities and therefore different "
        "PlanIds and RunIds, which defeats independent replay (FW-06). This "
        "reference had to invent one to build its vector.")


def _count_annotation(doc, key):
    n = 0
    stack = [doc]
    while stack:
        cur = stack.pop()
        if isinstance(cur, dict):
            if key in cur:
                n += 1
            stack.extend(cur.values())
        elif isinstance(cur, list):
            stack.extend(cur)
    return n


# ---- G6: unresolved-edge is not expressible in a capability manifest -------
def g6():
    fp = load("docs/coop/artifacts/fact-plane.v1.json")
    dl = load("docs/coop/artifacts/delivery.v4.json")
    doms = dl["derivedFrom"]["operations"][17]["value"]["valueDomains"]["registries"]
    rel_dom = doms["fact-plane.v1#relationRegistry.relations"]
    native = load("docs/coop/design-corrections/native/native-evidence.schemas.v2.json")
    probe(
        "G6", "SHOULD",
        ["delivery.v4.json $.derivedFrom.operations[17].value.valueDomains.registries"
         "['fact-plane.v1#relationRegistry.relations'] (12 members, ADM-DOMAIN bound)",
         "native-evidence.md section 0 (fact-plane $.relationRegistry.relations "
         "**Extended** with relation `unresolved-edge`)",
         "native-evidence.schemas.v2.json #/$defs/Relation (13 members)",
         "identity-and-evidence.md section 3 (capabilityManifestId uses the "
         "inherited applied producing recipe)"],
        "Native extends the relation registry with `unresolved-edge`, but "
        "CAP-MANIFEST-ID-V1's ADM-DOMAIN gate binds ProviderCapability.relations "
        "keys and AbsentCapability.relationIds to the twelve members it measured "
        "on the live fact-plane bytes. A provider that declares the new relation "
        "as a capability cannot be expressed in a capability manifest, and the "
        "manifest is a PlanId input.",
        {"capabilityManifestRelationDomainMembers": rel_dom["members"],
         "capabilityManifestRelationDomainCount": rel_dom["memberCount"],
         "nativeRelationEnum": native["$defs"]["Relation"]["enum"],
         "factPlaneRegistryRelations": sorted(fp["relationRegistry"]["relations"].keys()),
         "extraInNative": sorted(set(native["$defs"]["Relation"]["enum"])
                                 - set(fp["relationRegistry"]["relations"]))},
        "Whether the extension propagates into the capability manifest domain "
        "(and if so, what the `unresolved-edge` ladder rung `observed` means for "
        "ProviderCapability.relations, since delivery binds values to the "
        "relation's own ladder). Executed as vector V-CM-05.")


# ---- G7: ExecutionId end-anchor conflict -----------------------------------
def g7():
    c2 = load("docs/coop/artifacts/c2-plan-stage-schema.v4.json")
    ex = c2["planIntent"]["wireTypes"]["executionId"]
    common = load("docs/coop/design-corrections/workflows/schemas/common.schema.json")
    probe(
        "G7", "SHOULD",
        ["identity-and-evidence.md section 2 (`The grammar is the C-2 owner selector "
         "c2-plan-stage-schema.v4.json planIntent.wireTypes.executionId`)",
         "c2-plan-stage-schema.v4.json $.planIntent.wireTypes.executionId.pattern",
         "admission-and-qualification.md section 1 (`The product schemas use the "
         "portable ECMAScript assertion (?![\\s\\S]) where an end anchor is "
         "intended, because $ can also match before a final newline. A "
         "newline-suffixed identifier or digest is malformed`)",
         "common.schema.json #/$defs/ExecutionId.pattern",
         "security-and-lifecycle.md S9.1 (the same discipline, stated explicitly "
         "as an intended successor difference for RootV1)"],
        "Identity section 2 makes the C-2 selector THE normative ExecutionId "
        "grammar. That selector's pattern ends with a bare `$`, which admits a "
        "newline-suffixed value; admission section 1 declares such a value "
        "malformed and the workflow successor pattern refuses it. Security S9.1 "
        "handles exactly this situation for RootV1 by saying in terms that the "
        "successor is deliberately not byte-equivalent; identity section 2 makes "
        "no such statement while naming the older selector as the grammar.",
        {"c2Pattern": ex["pattern"],
         "workflowSuccessorPattern": common["$defs"]["ExecutionId"]["pattern"],
         "c2AdmitsTrailingNewline": bool(re.match(ex["pattern"], "exec1_" + "0" * 32 + "\n")),
         "successorAdmitsTrailingNewline": False,
         "c2OwnershipHonesty": ex["ownershipHonesty"][:200]},
        "Whether the normative grammar is the C-2 bytes (which admit a trailing "
        "newline) or the end-anchored successor. Identity section 2 should say, as "
        "S9.1 does, that the successor pattern is the admission boundary and the "
        "C-2 selector is the grammar's provenance.")


# ---- G8: plan.budget is the one unconstrained object in a closed record ----
def g8():
    ident = load("docs/coop/design-corrections/foundation/identity-schemas.v2.json")
    budget = ident["$defs"]["plan"]["properties"]["budget"]
    cfg_budget = (ident["$defs"]["semantic-configuration"]["properties"]["analysis"]
                  ["properties"]["budget"])
    probe(
        "G8", "SHOULD",
        ["identity-schemas.v2.json #/$defs/plan.properties.budget",
         "identity-and-evidence.md section 3 domain table (`plan ... deterministic budget`)",
         "admission-and-qualification.md section 1.1 (`analysis always contains "
         "profileId, capabilities and the complete {unit,limit} budget`)",
         "identity-schemas.v2.json #/$defs/semantic-configuration...analysis.budget (closed)"],
        "Every other field of the `plan` record is closed and every 64-hex field "
        "carries an x-opensip-digest annotation, but `plan.budget` is a bare "
        "`{\"type\": \"object\"}` with no additionalProperties, no required keys "
        "and no order annotation, inside a record whose bytes ARE the PlanId. The "
        "resolved semantic configuration's budget IS closed, so the shape exists; "
        "the Plan just does not reference it.",
        {"planBudgetSchema": budget,
         "semanticConfigurationBudgetSchema": cfg_budget,
         "planRecordAdditionalProperties": ident["$defs"]["plan"].get("additionalProperties")},
        "Whether plan.budget is the same closed {unit, limit} record. Until it is "
        "constrained, two hosts can put different key sets there and mint "
        "different PlanIds for one analysis, and the digest law's own reasoning "
        "(`a new field added without an annotation refuses at admission instead of "
        "silently inheriting a plausible rule`) does not reach it.")


# ---- G9: no registered public detail for the pinned-purge refusal ---------
def g9():
    common = load("docs/coop/design-corrections/workflows/schemas/common.schema.json")
    codes = common["$defs"]["DomainDetailCode"]["enum"]
    probe(
        "G9", "SHOULD",
        ["identity-and-evidence.md section 5 (`A direct purge of a pinned Run "
         "refuses unless the explicit destructive purge also revokes the named "
         "pins after disclosing consequences`)",
         "workflows-and-surfaces.md section 12 (`Owners register stable details "
         "before emitting them; an unknown detail refuses admission`)",
         "public-detail-registry.v1.json / common.schema.json #/$defs/DomainDetailCode",
         "command-envelope.schema.json (kind=failure requires a non-empty `errors` "
         "array of DomainDetail)"],
        "Identity section 5 requires a purge refusal that names the active pins "
        "and discloses consequences, and the closed public detail registry has no "
        "member for it. A kind=failure envelope requires at least one DomainDetail "
        "whose code is a registry member, so no admissible public envelope exists "
        "for this normatively required refusal.",
        {"retentionOrPinRelatedCodes": [c for c in codes
                                        if "PIN" in c.upper() or "RETENT" in c.upper()
                                        or "PURGE" in c.upper()],
         "evidenceLifecycleCodes": [c for c in codes if c.startswith("evidence.")],
         "registrySize": len(codes),
         "demonstratedBy": "terminations.json TERM-11 (envelopeConstructible=false)"},
        "The registry member (and its owner) for the pinned-purge refusal. This is "
        "the same class of defect the previous blind consumer's M-5 raised against "
        "the security unit, which was closed by registering the eleven missing "
        "codes; the identity unit's retention refusals were not swept the same way.")


# ---- G10: configOrigin tsconfig-vs-jsconfig is not derivable ---------------
def g10():
    native = load("docs/coop/design-corrections/native/native-evidence.schemas.v2.json")
    ctx = native["$defs"]["TypeScriptNativeContextV2"]
    uni = native["$defs"]["TypeScriptUniverseV2ResolvedInputs"]
    probe(
        "G10", "SHOULD",
        ["native-evidence.md section 2.4 (`languageMode, packageModuleType, "
         "allowJs, checkJs, lockfileKind, nodeModulesInReadSet, "
         "jsDiagnosticsEnabled, jsAdmittedToProgram, configOrigin, the "
         "extends-graph emptiness and the synthesized-options presence are each "
         "checked against the context`)",
         "native-evidence.schemas.v2.json #/$defs/TypeScriptNativeContextV2 (no configOrigin property)",
         "native-evidence.schemas.v2.json #/$defs/TypeScriptUniverseV2ResolvedInputs.configOrigin "
         "(enum tsconfig | jsconfig | synthesized)"],
        "`bind_typescript_universe` is required to check `configOrigin` against "
        "the retained context, and the context has no configOrigin field. Only "
        "the synthesized/non-synthesized distinction is derivable (an empty "
        "configGraphPaths); nothing in the context distinguishes `tsconfig` from "
        "`jsconfig`, so a caller may spell either.",
        {"contextProperties": sorted(ctx["properties"].keys()),
         "universeConfigOriginEnum": uni["properties"]["configOrigin"]["enum"],
         "onlyDerivableSignal": "configProjection.configGraphPaths == [] <-> synthesized",
         "thisReferenceImplemented": "synthesized-only agreement; the tsconfig/"
                                     "jsconfig spelling is unchecked and was invented"},
        "The rule that decides configOrigin from the retained context. Because "
        "configOrigin is a universe field, an unchecked spelling mints two "
        "different universe identities -- and therefore two PlanIds -- for one "
        "admitted context.")


# ---- G11: subject-scope.enumeratorClosure kind is unconstrained ------------
def g11():
    ident = load("docs/coop/design-corrections/foundation/identity-schemas.v2.json")
    kinds = ident["$defs"]["closure"]["properties"]["kind"]["enum"]
    probe(
        "G11", "advisory",
        ["identity-schemas.v2.json #/$defs/subject-scope.enumeratorClosure",
         "identity-schemas.v2.json #/$defs/closure.properties.kind.enum",
         "native-evidence.md section 4.1a (`enumeratorClosure is the closure2 of "
         "the Plan-bound enumerator that produced the partition`)"],
        "`enumeratorClosure` must be a closure2, and the closed `closure.kind` "
        "enum has no `enumerator` member, while nothing states which kind is "
        "lawful there. Contrast `toolClosure.closureId` (kind=toolchain), "
        "`typescriptStdlibMerkleRoot` (kind=stdlib) and `rustcDevLlvmDigest` "
        "(kind=rust-dev-llvm), each of which the digest-domain registry pins by "
        "kind.",
        {"closureKindEnum": kinds,
         "closureJoinsThatPinAKind":
             list(ident["x-opensip-digest-domains"]["domainSets"]["native-context"]
                  ["native.context.typescript.v2"]["closureJoins"]),
         "thisReferenceUsed": "kind=provider (the native provider enumerates)"},
        "Which closure kind an enumerator must be. Low risk -- the Plan-selection "
        "join already constrains it -- but it is the one closure reference in the "
        "identity graph with no kind rule.")


# ---- G12: readiness/governance records are correctly OUT of scope ----------
def g12():
    readme = open(os.path.join(SUBJECT, "docs/v2/contracts/product-v1/README.md")).read()
    probe(
        "G12", "confirmation",
        ["docs/v2/contracts/product-v1/README.md (final paragraph)",
         "docs/coop/design-corrections/current-source-map.proposed.md"],
        "The index draws the distinction the reconstruction needs: the five "
        "contracts' retained/superseded selector tables are the normative recipe "
        "source, while the correction record and the central readiness register "
        "`grant standing; they are not additional semantic recipes`. Their absence "
        "from this kit is deliberate and never blocked a semantic reconstruction.",
        {"indexStatement": readme[readme.find("The normative retained/superseded"):
                                  readme.find("Passing design reference checks")].strip(),
         "everySelectorNeededWasResolvableInsideTheKit": True,
         "governanceRecordsNeededForAnyVector": False},
        "Nothing. Recorded so the verdict is not read as an input-custody "
        "complaint about the excluded governance records.")


def main():
    for fn in (g1, g2, g3, g4, g5, g6, g7, g8, g9, g10, g11, g12):
        fn()
    path = "/tmp/opensip-design-corrections/consumer-b.v2/output/gaps.json"
    with open(path, "w") as fh:
        json.dump({"findings": FINDINGS}, fh, indent=1, sort_keys=True)
        fh.write("\n")
    for f in FINDINGS:
        print("%-4s %-12s %s" % (f["id"], f["severity"], f["statement"].split(".")[0][:110]))


if __name__ == "__main__":
    main()
