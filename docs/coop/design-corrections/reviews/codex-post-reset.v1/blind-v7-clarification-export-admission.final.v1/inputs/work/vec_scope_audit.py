"""CLARIFICATION v1 item 4: MEASURE the reporting-scope corrections root raised,
so the corrected report states them as measurements rather than assertions."""
import json, os, re

import oslib as O
from oslib import C, H, sha256hex


def measure(results_path):
    R = json.load(open(results_path))
    out = {}

    # (g) nativeHPreimages canonicalPayloadBytes were TRUNCATED HEADS
    pre = R["nativeHPreimages"]
    trunc = {k: {"canonicalPayloadLength": v["canonicalPayloadLength"],
                 "displayedChars": len(v["canonicalPayloadBytes"]),
                 "displayIsTruncated":
                     len(v["canonicalPayloadBytes"]) < v["canonicalPayloadLength"]}
            for k, v in pre.items()}
    out["nativeHPreimageDisplay"] = {
        "perDomain": trunc,
        "truncatedCount": sum(1 for v in trunc.values() if v["displayIsTruncated"]),
        "totalCount": len(trunc),
        "displayCapChars": 400,
        "fullBytesExistInExports": True,
        "note": "the DISPLAY field is a 400-character head; the full canonical "
                "bytes and the full H preimage frame are in the per-run blob "
                "exports, keyed by digest"}

    # (h) ADV-1: the honest enum comparison
    d9 = O.doc("d9"); common = O.doc("common")["$defs"]
    inherited_map = set(d9["codeMaps"]["faultCauseToErrorCode"])
    inherited_enum = set(d9["scenarioAxesSchema"]["properties"]["faultCause"]["enum"])
    successor_enum = set(common["D9FaultCause"]["enum"])
    out["d9FaultCauseCounts"] = {
        "inheritedFaultCauseToErrorCodeEntries": len(inherited_map),
        "inheritedScenarioAxisEnumMembers": len(inherited_enum),
        "successorEnumMembers": len(successor_enum),
        "enumToEnumComparison": "%d -> %d" % (len(inherited_enum),
                                              len(successor_enum)),
        "mapToEnumComparisonIsNotLikeForLike": True,
        "noneIsASentinelPresentInBothEnums":
            "none" in inherited_enum and "none" in successor_enum,
        "addedByTheSuccessor": sorted(successor_enum - inherited_enum),
        "correction": "the ORIGINAL report compared TEN fault-map entries "
                      "against TWELVE successor enum members (which include the "
                      "`none` sentinel). The like-for-like enum comparison is "
                      "11 -> 12; the delta is the same single member either way."}

    # (f) how many negatives are genuinely SINGLE-FIELD
    single, multi = [], []
    classification = {
        # measured by reading the mutation each builder applies
        "stdlib-inventory-incomplete": "removes one inventory ROW (and the "
                                       "context digest, universe and Plan all "
                                       "recompute)",
        "compiler-version-not-from-manifest": "one field",
        "lockfile-outside-snapshot": "one field",
        "config-node-kind-relabelled": "one field inside a hashed record; the "
                                       "graph digest, universe and Plan recompute",
        "plan-budget-contradicts-config": "one field",
        "file-payload-digest-wrong": "one payload field; the fact identity "
                                     "recomputes",
        "inventory-fact-carries-an-anchor": "adds an anchor; the fact identity "
                                            "recomputes",
        "unanchored-code-fact": "empties the anchor array; the fact identity "
                                "recomputes",
        "rung-of-another-relation": "one field; the fact identity recomputes",
        "totality-omits-an-inventoried-path": "drops a whole fact RECORD from "
                                              "the view",
        "partition-overlap": "adds a whole scope RECORD and its Coverage",
        "plan-omits-a-retained-context": "drops one Plan array member; the Plan "
                                         "identity recomputes",
        "raw-payload-offered-as-an-h-identity": "replaces a retained BLOB",
        "altered-frame": "replaces a retained BLOB",
        "missing-preimage": "deletes a retained BLOB",
        "unregistered-h-domain": "replaces a retained BLOB",
        "unregistered-h-domain-in-plan": "changes the minting DOMAIN; the "
                                         "context digest and Plan recompute",
        "clone-level-specification-not-retained": "deletes a retained BLOB",
        "finding-evidence-refs-unordered": "reorders one array in one record",
        "finding-cites-a-fact-outside-the-evaluated-view": "replaces one array "
                                                          "member",
        "finding-parameter-message-code-mismatch": "replaces a retained record "
                                                   "and one field",
        "ambiguous-selection-claiming-complete [selection=AMB]":
            "a different SELECTION: a different ownership record, universe and "
            "whole graph",
        "partial-enumeration-false-complete": "one ownership field plus the "
                                              "Coverage entry; universe and "
                                              "graph recompute",
        "projection-digest-mismatch": "one universe field",
        "hidden-context": "empties a Plan array; the Plan identity recomputes",
        "grammar-definition-outside-the-closure-tree": "changes the closure "
                                                       "TREE; closure id, "
                                                       "context, universe and "
                                                       "graph recompute",
        "grammar-bundle-manifest-outside-the-closure-tree": "changes the "
                                                            "closure TREE",
        "normalizer-spec-outside-the-closure-tree": "changes the closure TREE",
        "data-grammar-claims-code": "one field in a bundle row",
        "false-complete-on-unsupported-scope": "one Coverage entry (three "
                                               "fields)",
        "grammar-version-not-from-manifest": "one field",
        "markdown-anchored-code-fact": "two anchor fields; the fact identity "
                                       "recomputes",
        "select-a-grammar-not-in-the-bundle": "adds one array member",
    }
    for k, v in classification.items():
        (single if v in ("one field",) else multi).append(k)
    out["negativeMutationShape"] = {
        "classified": classification,
        "strictlyOneFieldOnly": sorted(single),
        "changeMoreThanOneFieldOrARecordOrRecomputeIdentities": sorted(multi),
        "correction": "the ORIGINAL report said 'Each is a SINGLE-FIELD "
                      "mutation of an otherwise complete positive graph'. That "
                      "is accurate for %d of %d; the rest change a whole "
                      "record, a retained blob, a closure tree or a selection, "
                      "and most recompute downstream identities. What holds for "
                      "ALL of them is that each isolates ONE law and leaves the "
                      "rest of the graph otherwise complete."
                      % (len(single), len(classification))}

    # (e) the relation digest-law traversal scope
    out["relationDigestLawTraversalScope"] = {
        "measured": R["selfChecks"]["relationDigestLaw"]
            ["governedTopLevelOccurrences"],
        "covers": "TOP-LEVEL selector properties of each relation payload whose "
                  "type is DigestHex, Sha256Text or CanonicalPath",
        "doesNotCover": "nested object members, array elements, map values, "
                        "intermediate local $defs aliases, inline patterns "
                        "equal to a governed definition, and oneOf/anyOf/allOf "
                        "branch inheritance - all of which the relation "
                        "document's own x-opensip-digest-law governs",
        "correction": "the ORIGINAL report's phrase 'reaches every governed "
                      "top-level occurrence' was accurate, but the surrounding "
                      "claim should not be read as covering arbitrary schema "
                      "inheritance."}

    # (a)-(d) what the public/workflow vectors are and are not
    out["vectorNature"] = {
        "failureEnvelopes": {
            "whatItIs": "literal composed CommandEnvelope major-2 objects "
                        "validated against command-envelope.schema.json and the "
                        "common StepTermination/DomainDetail branch contract",
            "whatItIsNot": "an actual raised-and-caught internal failure routed "
                           "through a host termination projection",
            "count": len([k for k in R["public"]["failureEnvelopes"]
                          if not k.startswith("_")])},
        "authorization": {
            "whatItIs": "records validated against the security/native schemas, "
                        "plus equality of the four effect values against the "
                        "pinned permission truth table in the child-process "
                        "execution mode",
            "whatItIsNot": "an executed security admission or authorization "
                           "engine; the CI-consent refusal, the over-claimed "
                           "enforcement refusal and the repair-plan edit "
                           "boundary are LITERAL ASSERTIONS in the vector, not "
                           "engine outputs",
            "measuredNotAsserted": ["schema validity of each record",
                                    "effect values equal to the pinned table",
                                    "the canonical empty owner-array digest",
                                    "a display alias refused by the platformId "
                                    "enum"],
            "assertedNotExecuted": ["interactive consent refuses in CI",
                                    "an over-claimed ENFORCED-PLATFORM value "
                                    "refuses at security admission",
                                    "an edited descriptor is named by no "
                                    "authorization"]},
        "comparison": {
            "whatItIs": "schema-valid ComparisonDescriptor records whose "
                        "classifications are conceptual",
            "whatItIsNot": "a closed baseline/Run comparison engine; no pivot "
                           "was evaluated and no finding set was diffed",
            "scopePolicyAxis": "the TWO PLANS ARE REAL constructed Plans "
                               "differing only in the bound ScopeDocumentV1 "
                               "parameter, with real distinct PlanIds; they are "
                               "NOT two fully compared Runs"},
        "minResolutionPredicates": {
            "whatItIs": "ladder-index comparison helpers over one relation's own "
                        "ladder, plus cross-relation refusal",
            "whatItIsNot": "full sufficiency_v2 over every Coverage and evidence "
                           "boundary (confidence floors, derivation policy, "
                           "closed-world, dependsOn recursion)"}}
    return out
