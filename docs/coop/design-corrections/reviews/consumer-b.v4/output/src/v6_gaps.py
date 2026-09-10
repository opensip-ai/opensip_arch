"""Vector set 6: executable demonstrations of each identified design gap.

Each entry shows the exact selectors, the two conforming readings an implementer
is left with, and what had to be INVENTED to build the promised vector.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixtures as F  # noqa: E402
import graph as G  # noqa: E402
import kit  # noqa: E402
import osip  # noqa: E402
import runner  # noqa: E402
import scen_syntax  # noqa: E402
import scen_ts  # noqa: E402

OUT = []


def gap(gid, severity, title, selectors, demo, readings, invented):
    OUT.append({"id": gid, "severity": severity, "title": title,
                "selectors": selectors, "demonstration": demo,
                "conformingReadings": readings, "whatIHadToInvent": invented})


# ==========================================================================
# MUST-1: fact anchor cardinality is undecided for every non-clones relation
# ==========================================================================
st = G.Store()
scn = scen_syntax.build(st, "unsupported")            # a .py file, no bundled grammar
inv = scn["snapshot"]["inventory"]["tool/main.py"]
payload = {"path": "tool/main.py", "contentSha256": inv["sha256"],
           "byteLength": inv["bytes"]}

anchored = G.make_fact(st, scn["snapshot"], "file", "enumerated",
                       scn["universe"]["hex"], scn["universe"]["hex"],
                       scn["provider"]["id"], payload,
                       [{"path": "tool/main.py", "blobDigest": inv["sha256"],
                         "startByte": 0, "endByte": inv["bytes"]}])
unanchored = G.make_fact(st, scn["snapshot"], "file", "enumerated",
                         scn["universe"]["hex"], scn["universe"]["hex"],
                         scn["provider"]["id"], payload, [])
rows = G.syntax_selected_rows(scn["universe"], scn["context"])
cap_ok = G.syntax_path_capability(rows, "tool/main.py", "file@enumerated")

gap("CB4-MUST-1", "MUST",
    "The number of anchors an inventory (or symbol) fact carries is not decided "
    "anywhere, and under a syntax universe the two lawful readings differ in "
    "ADMISSIBILITY, not just in spelling.",
    ["foundation/identity-schemas.v2.json#/$defs/fact/properties/anchors "
     "(maxItems 100000, uniqueItems, x-opensip-order canonical-set; NO minItems and "
     "no per-relation cardinality)",
     "foundation/relation-payload-schemas.v2.json#/x-opensip-relation-registry/"
     "relations/file/snapshotJoins[0].anchorPathField "
     "(\"every anchor of the fact must lie in the very file the payload claims\" - "
     "vacuous at zero anchors)",
     "foundation/relation-payload-schemas.v2.json#/x-opensip-relation-registry/"
     "relations/clones/bodyIdentityJoin.anchorCardinality = 1 "
     "(the ONLY relation given a cardinality)",
     "native-evidence.md section 1.2, \"Every admitted fact\" "
     "(\"every one of its anchor paths\" - vacuous at zero anchors; the carve-out "
     "sentence \"An unanchored code fact is not vacuously supported\" is scoped to "
     "CODE facts and leaves inventory facts undecided)",
     "docs/coop/design-corrections/native/native-evidence.schemas.v2.json#/"
     "x-opensip-grammar-capability-registry.enforcementBoundaries (2) and (3)"],
    {"repository": "one .py file with no bundled grammar plus one README.md",
     "scopeRule": "inventory capabilities are ALWAYS available and never "
                  "grammar-gated, so the file@enumerated Coverage over the whole "
                  "inventory is genuinely `complete`",
     "factRule": "every anchor path must be read by a selected grammar",
     "pathReadBySelectedGrammar": cap_ok,
     "readingA_wholeFileAnchor": {
         "factId": anchored["id"],
         "admissibleUnderTheSyntaxGuard": False,
         "refusal": "SYNTAX_CAPABILITY_UNSUPPORTED_FACT: file@enumerated at "
                    "tool/main.py"},
     "readingB_unanchored": {
         "factId": unanchored["id"], "admissibleUnderTheSyntaxGuard": True},
     "identitiesDiffer": anchored["id"] != unanchored["id"],
     "consequenceIfNeitherIsChosen":
         "under reading A the file is inventoried and `complete` while NO file fact "
         "for it can exist, so `exists file where path=tool/main.py` is FALSE over a "
         "COMPLETE Coverage - an authoritative claim that an inventoried file is "
         "absent. Under reading B the Run closes, but every inventory and symbol "
         "fact of EVERY language mode has two lawful spellings with different "
         "fact2/view2/evidence2/run2 identities, contradicting the stated property "
         "that identical semantic inputs produce the same Run."},
    ["reading A: anchor an inventory fact over the whole file (natural, and what a "
     "'source anchor must name an inventoried blob' reading suggests)",
     "reading B: leave inventory facts unanchored (the only reading under which an "
     "unsupported-file path is representable at all under a syntax universe)"],
    "I chose reading B for unsupported-file paths and reading A everywhere else, "
    "purely so the promised 'repository with no TypeScript or Rust compilation "
    "unit' vector could be built. Neither choice is derivable from the kit. A "
    "conformant fix is one sentence: state the anchor cardinality per relation "
    "(as the clones row already does), or exempt the three inventory capabilities "
    "from enforcementBoundary (2) as boundary (3) already exempts them.")

# ==========================================================================
# MUST-2: no NativeCause member for three of section 10's own Cause rows
# ==========================================================================
causes = set(kit.doc("native")["$defs"]["NativeCause"]["enum"])
edges = sorted(kit.doc("native")["$defs"]["UnresolvedEdgeKindV1"]["enum"])
st2 = G.Store()
scn2 = scen_ts.build(st2, "ordinary")
ref_cov = [c for c in scn2["coverages"]
           if c["payload"]["entry"]["relation"] == "references"][0]
entry = ref_cov["payload"]["entry"]

attempts = {}
for candidate in ["computed-member-access", "exports-open", "compiler-inferred"]:
    try:
        bad = json.loads(json.dumps(entry))
        bad["nativeCause"] = candidate
        kit.validate("native", "#/$defs/ViewEntryV3", bad)
        attempts[candidate] = "admitted"
    except ValueError as exc:
        attempts[candidate] = "refused: " + str(exc)[:110]

gap("CB4-MUST-2", "MUST",
    "native-evidence section 10's Cause column names causes for three deficiencies "
    "that the CLOSED NativeCause enum cannot express, so the only representable "
    "value is null - which the enum's own description says \"records that a "
    "disclosure was owed and not made\".",
    ["native-evidence.md section 10, deficiency table rows `resolution-incomplete` "
     "(Cause = \"the unresolved edge classes; partial/not-attempted stage\"), "
     "`external-consumers-unknown` (Cause = \"exports-open, exports-unknown\") and "
     "`derivation-policy-unmet` (Cause = \"compiler-inferred present\")",
     "docs/coop/design-corrections/native/native-evidence.schemas.v2.json#/$defs/"
     "NativeCause (closed, 14 members)",
     "docs/coop/design-corrections/native/native-evidence.schemas.v2.json#/$defs/"
     "ViewEntryV3/properties/nativeCause (oneOf NativeCause | null)",
     "docs/coop/design-corrections/native/native-evidence.schemas.v2.json#/$defs/"
     "UnresolvedEdgeKindV1 (closed, 16 members, DISJOINT from NativeCause)"],
    {"nativeCauseMembers": sorted(causes),
     "unresolvedEdgeKinds": edges,
     "intersection": sorted(causes & set(edges)),
     "attemptsToCarryTheNamedCause": attempts,
     "contrast": "the three body-language-* members were added precisely because "
                 "\"a nullable nativeCause does not satisfy a mandated disclosure\"; "
                 "the same argument applies verbatim to these three rows and was not "
                 "carried through",
     "publicProjectionIsUnaffectedForTheDEFICIENCY":
         "resolution-incomplete, external-consumers-unknown and "
         "derivation-policy-unmet ARE members of the closed public "
         "DomainDetailCode registry, so the deficiency is publicly nameable and only "
         "the cause is not"},
    ["reading A: emit nativeCause: null and accept that the CLI/JSON/SARIF/HTML/agent "
     "parity fields carry no cause for the most common deficiency in real "
     "JavaScript and non-prepared Rust",
     "reading B: read the unresolvedEdgeClasses array in resolutionCompleteness as "
     "the cause carrier and treat section 10's Cause column as descriptive prose - "
     "which leaves external-consumers-unknown and derivation-policy-unmet with no "
     "carrier at all"],
    "I emitted nativeCause: null for the honest RC-3 entry in the TypeScript Run "
    "(vector P-ts-ordinary, references@resolved-binding) and recorded the gap rather "
    "than inventing enum members. A conformant fix is either three to twenty new "
    "NativeCause members, or one sentence in section 10 saying these rows' causes "
    "travel in resolutionCompleteness.unresolvedEdgeClasses and closedWorld and that "
    "nativeCause is null for them by design.")

# ==========================================================================
# SHOULD-1: clones languageIdSource contradicts the derived body-language law
# ==========================================================================
sets = kit.doc("identity")["x-opensip-digest-domains"]["domainSets"][
    "native-semantic-universe"]
row_lang = {d: sets[d]["language"] for d in sets}
body_langs = {d: sets[d]["languageVersionBinding"].get("bodyLanguages") for d in sets}
enum = kit.doc("identity")["$defs"]["body-language-version"]["properties"][
    "languageId"]["enum"]
st3 = G.Store()
scn3 = scen_ts.build(st3, "ordinary")
js_blv = scn3["cloneIdentities"]["js_body_language_version"]

gap("CB4-SHOULD-1", "SHOULD",
    "The clones registry says the body languageId comes from \"the language of the "
    "fact sourceUniverse domain registry row\", which for a .js body under a "
    "TypeScript universe yields `typescript` and for ANY body under the syntax "
    "universe yields `syntax` - a value the closed languageId enum refuses.",
    ["foundation/relation-payload-schemas.v2.json#/x-opensip-relation-registry/"
     "relations/clones/bodyIdentityJoin.languageIdSource",
     "foundation/identity-schemas.v2.json#/x-opensip-digest-domains/domainSets/"
     "native-semantic-universe/*/language",
     "foundation/identity-schemas.v2.json#/x-opensip-digest-domains/domainSets/"
     "native-semantic-universe/*/languageVersionBinding.bodyLanguageByVariant "
     "and .bodyLanguageLaw",
     "identity-and-evidence.md section 3, \"The body's languageId comes from the "
     "SAME selector over the SAME anchor, and it is the language of the BODY, not "
     "of the provider\"",
     "foundation/identity-schemas.v2.json#/$defs/body-language-version/properties/"
     "languageId (enum: javascript, rust, typescript)"],
    {"domainRowLanguage": row_lang, "bodyLanguagesPerDomain": body_langs,
     "closedLanguageIdEnum": sorted(enum),
     "literalReadingForASyntaxUniverse": "syntax",
     "literalReadingIsUnrepresentable": "syntax" not in enum,
     "correctDerivedValueForAJsBodyUnderATypeScriptUniverse":
         js_blv["languageId"],
     "twoNormativeStatementsAgreeWithEachOther":
         "identity section 3 and the domain row's own bodyLanguageLaw both say "
         "DERIVED-FROM-VARIANT; only the relation registry sentence disagrees"},
    ["reading A (literal): languageId = domainSets[...].language - demonstrably "
     "wrong, and unrepresentable for the syntax universe",
     "reading B: languageId = bodyLanguageByVariant[selected variant] - agrees with "
     "identity section 3 and with the domain row's own bodyLanguageLaw"],
    "I implemented reading B. The correct answer is determinate, so this is a "
    "one-sentence wording defect in a NORMATIVE registry rather than a missing "
    "recipe - but a literal implementer following the registry sentence produces a "
    "different clone identity for every JavaScript body and no admissible identity "
    "at all under the syntax universe.")

# ==========================================================================
# SHOULD-2: analysis-spec capabilityId has no named vocabulary authority
# ==========================================================================
spec_prop = kit.doc("identity")["$defs"]["analysis-spec"]["properties"][
    "requestedCapabilities"]["items"]["properties"]["capabilityId"]
matrix_ids = [c["id"] for c in kit.doc("matrix")["capabilities"]]
gap("CB4-SHOULD-2", "SHOULD",
    "analysis-spec.requestedCapabilities[].capabilityId is free Text and enters "
    "PlanId through analysisSpecDigest, but no document names the vocabulary it "
    "must be drawn from.",
    ["foundation/identity-schemas.v2.json#/$defs/analysis-spec/properties/"
     "requestedCapabilities/items/properties/capabilityId ($ref #/$defs/Text)",
     "native-evidence.md section 1.4, \"default_capability_selection takes the "
     "authenticated release declaration registry rows (capability x applicable "
     "language modes)\"",
     "admission-and-qualification.md section 1.1, \"The authenticated release "
     "declaration registry supplies the `default` profile and exact applicable "
     "TS/JS/Rust capabilities\"",
     "docs/coop/design-corrections/native/native-capability-matrix.v2.json "
     "#/capabilities[].id"],
    {"schemaConstraint": spec_prop,
     "matrixCapabilityIds": matrix_ids,
     "relationAtRungSpellingIUsed": "clones@normalized-body-hash",
     "bothSpellingsSchemaValid": True,
     "consequence": "two conforming hosts requesting the same capability for the "
                    "same unit mint different analysisSpecDigests and therefore "
                    "different PlanIds and RunIds, which defeats independent replay "
                    "across machines",
     "theNamedAuthorityIsNotInThisKit":
         "the \"authenticated release declaration registry\" is named by two "
         "contracts but is not one of the 45 supplied files; the capability matrix "
         "is the only candidate and no contract says the two are the same"},
    ["reading A: capabilityId is the matrix capability id (inventory, syntax, "
     "clones-fact, ...)",
     "reading B: capabilityId is a relation@rung string, which is what the section "
     "1.3 table and the Coverage key actually use"],
    "I used relation@rung. Either the release declaration registry must be named as "
    "the vocabulary authority with its selector, or the field must be constrained "
    "to the matrix ids. This is a SHOULD rather than a MUST because the field is "
    "host-produced and a single implementation is self-consistent; it becomes a "
    "MUST the moment two implementations must agree on one PlanId.")

# ==========================================================================
# Advisories
# ==========================================================================
gap("CB4-ADV-1", "advisory",
    "native-evidence section 1.1 says the machine-readable matrix has 60 cells; it "
    "has 66 (11 capabilities x 6 modes). The prose count is stale, not the matrix.",
    ["native-evidence.md section 1.1",
     "docs/coop/design-corrections/native/native-capability-matrix.v2.json#/cells"],
    {"proseCount": 60, "actualCells": len(kit.doc("matrix")["cells"])},
    ["the matrix is authoritative; the count is decoration"],
    "nothing - the count does not affect any admission")

gap("CB4-ADV-2", "advisory",
    "The two prose enumerations of registered identity domains predate the "
    "syntax-only universe and do not list `native.semantic-universe.syntax.v2` or "
    "`native.context.syntax.v2`, although native section 1.2 registers them and the "
    "machine-readable domain-set registry (which is what admission dispatches on) "
    "carries them complete with bindings and languageVersionBindings.",
    ["identity-and-evidence.md section 3, \"Both universe domains native section 11 "
     "registers are registered here: ...typescript.v2 ... and ...rust.v2\"",
     "native-evidence.md section 11, \"Identity domains authored here\"",
     "foundation/identity-schemas.v2.json#/x-opensip-digest-domains/domainSets"],
    {"registeredUniverseDomains": sorted(sets),
     "registeredContextDomains": sorted(
         kit.doc("identity")["x-opensip-digest-domains"]["domainSets"]["native-context"]),
     "proseListsTwo": True, "registryListsThree": len(sets) == 3},
    ["the machine-readable registry is unambiguous and complete"],
    "nothing - I dispatched on the registry, as identity section 3 says the closure "
    "checker does")

gap("CB4-ADV-3", "advisory",
    "The four repository-code effect NAMES (subprocess, filesystemWrite, network, "
    "environment) are said to be copied from permission-truth-tables.v9, but that "
    "table is over seven closed permission TOKENS and the name-to-token mapping is "
    "published nowhere. The mapping is determinate by elimination and every claimed "
    "VALUE is correct.",
    ["native-evidence.md section 5.2 and section 13 H-2",
     "security-and-lifecycle.md S10",
     "docs/coop/artifacts/permission-truth-tables.v9.json#/truthTables/tables[*]/rows[*]/token",
     "docs/coop/design-corrections/native/native-evidence.schemas.v2.json#/$defs/EnforcementV1"],
    {"tokens": ["PT-FS-READ-PROJECT", "PT-FS-READ-COMPONENT", "PT-FS-WRITE-HOST-STATE",
                "PT-PROC-EXEC-DECLARED", "PT-NET-EGRESS", "PT-ENV-READ",
                "PT-HOST-EFFECT-BROKERED"],
     "inferredMapping": {"subprocess": "PT-PROC-EXEC-DECLARED",
                         "filesystemWrite": "PT-FS-WRITE-HOST-STATE",
                         "network": "PT-NET-EGRESS", "environment": "PT-ENV-READ"},
     "unprojectedToken": "PT-HOST-EFFECT-BROKERED (ENFORCED-AT-HOST-BROKER), which "
                         "EnforcementV1 admits but no effect name carries",
     "allClaimedValuesVerified": True},
    ["the mapping is forced by elimination"],
    "nothing for the vectors; I verified the values directly (see L10)")

gap("CB4-ADV-4", "advisory",
    "The `parameter` payload-registry class is keyed by the cited schemaDigest, and "
    "the ScopeDocumentV1 row cites the WHOLE policy-document.schema.json - the same "
    "document plan.policyDigest and plan.waiverDigest name under the "
    "`canonical-record` representation. The classes are different so there is no "
    "ambiguity today, but a second parameter row selecting another $def out of that "
    "same document would be indistinguishable, which the registry law itself calls "
    "out and forbids.",
    ["foundation/identity-schemas.v2.json#/x-opensip-payload-registry/classes/"
     "parameter (keyedBy: the cited schemaDigest; two rows)",
     "identity-and-evidence.md, \"The ScopeDocumentV1 parameter row (CB3-MUST-4)\""],
    {"parameterRows": sorted(kit.doc("identity")["x-opensip-payload-registry"]
                             ["classes"]["parameter"]["rows"]),
     "policyDocumentDigest": kit.doc_digest("policy"),
     "importSourceContextDigest": kit.doc_digest("importctx"),
     "keysDistinctToday": kit.doc_digest("policy") != kit.doc_digest("importctx"),
     "riskIsStructural": "the key is the DOCUMENT, not the (document, selector) pair"},
    ["today the two rows are distinguishable"],
    "nothing - but keying the class by (document, selector) rather than by document "
    "would make the stated ambiguity refusal unnecessary")

if __name__ == "__main__":
    print(json.dumps(OUT, indent=1, ensure_ascii=False, default=str))
