#!/usr/bin/env python
"""Points 3, 4, 5: an honest audit of what my own probes actually covered.

I re-read my retained probe SOURCES and RESULTS and state their true scope.
"""
import json
import os
import re
import sys
import collections

OLD = "/tmp/opensip-design-corrections/post-reset-review.v17"
SUBJ = "/tmp/opensip-design-corrections/candidate-subject.v17"
REV = "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews"
OUT = sys.argv[1]


def L(n):
    return json.load(open(os.path.join(OLD, "logs", n)))


def S(n):
    return open(os.path.join(OLD, "probes", n)).read()


rep = {}

# ---------------- Point 3: p03 composition ----------------
p03 = L("p03-must1-executable.json")
ids = [c["id"] for c in p03["cases"]]
buckets = collections.Counter(i.split("/")[0].split("-")[0] if "/" in i
                              else i.split("-")[0] for i in ids)
groups = collections.Counter()
for i in ids:
    if i.startswith("N-admit"):
        groups["native relation x native cause (ADMIT)"] += 1
    elif i.startswith("N-crossplane"):
        groups["native relation x imported cause (cross-plane REFUSE)"] += 1
    elif i.startswith("I-perkind"):
        groups["imported relation x imported cause (per-kind)"] += 1
    elif i.startswith("I-crossplane"):
        groups["imported relation x native cause (cross-plane REFUSE)"] += 1
    elif i.startswith("P-"):
        groups["presence/typing law"] += 1
    elif i.startswith("ROUNDTRIP"):
        groups["carryability of a produced token"] += 1
rep["p03Composition"] = dict(groups)
rep["p03TotalCases"] = len(ids)
nat_rel = p03["nativeRelations"]
imp_rel = p03["importedRelations"]
rep["p03NativeRelationCount"] = len(nat_rel)
rep["p03ImportedRelationCount"] = len(imp_rel)
cross_rels = sorted({i.split("/")[1] for i in ids if i.startswith("N-crossplane")})
rep["p03CrossPlaneCoveredNativeRelations"] = cross_rels
rep["p03CrossPlaneCoversAllNativeRelations"] = (
    sorted(cross_rels) == sorted(nat_rel))
rep["p03IsFullCrossProduct"] = rep["p03CrossPlaneCoversAllNativeRelations"]
rep["p03FullCrossProductWouldBe"] = (
    len(nat_rel) * 9 + len(nat_rel) * 7 + len(imp_rel) * 7 + len(imp_rel) * 9)
rep["p03Arithmetic"] = (
    "%d native x 9 native causes = %d ; cross-plane for only the FIRST %d native "
    "relations x 7 = %d ; %d imported x 7 = %d ; %d imported x 9 native = %d ; "
    "%d presence ; %d carryability = %d"
    % (len(nat_rel), len(nat_rel) * 9, len(cross_rels), len(cross_rels) * 7,
       len(imp_rel), len(imp_rel) * 7, len(imp_rel), len(imp_rel) * 9,
       groups["presence/typing law"], groups["carryability of a produced token"],
       len(ids)))

# ROUNDTRIP construction: does it forward the produced record?
src3 = S("p03_must1_executable.py")
rt = re.search(r'for pc in producer_cases:.*?\n\n', src3, re.S)
rep["p03RoundtripSource"] = rt.group(0).strip() if rt else None
rep["p03RoundtripUsesFixedRelation"] = bool(
    rt and '"references"' in rt.group(0))
rep["p03RoundtripForwardsProducedRecord"] = False
rep["p03ProducerResults"] = [
    {"target": pc.get("target"),
     "producedDeficiency": (pc.get("result") or {}).get("deficiency"),
     "sameToken": (pc.get("result") or {}).get("deficiency") == pc.get("target"),
     "producedFromRelation": None}
    for pc in p03["producerCases"]]
rep["allFourProducersEmittedTheSameSoleToken"] = all(
    r["sameToken"] for r in rep["p03ProducerResults"])
# which relation each producer case actually used
for pc, row in zip(p03["producerCases"], rep["p03ProducerResults"]):
    row["producedFromRelation"] = (
        "types" if row["target"] == "derivation-policy-unmet" else "references")
rep["p03RoundtripRelationMismatch"] = [
    r for r in rep["p03ProducerResults"] if r["producedFromRelation"] != "references"]

# sufficiency inputs were partial helper dicts
ve = re.search(r"def view_entry\(\*\*kw\):.*?return e\n", src3, re.S)
rep["p03ViewEntryHelper"] = ve.group(0).strip() if ve else None
rep["p03SufficiencyInputsAreValidatedRecords"] = False
rep["p03SufficiencyInputNote"] = (
    "view_entry builds a partial dict with resolution/coverage/"
    "confidenceMillionths/resolutionCompleteness/closedWorld only. It is NOT a "
    "schema-validated ViewEntryV3 and carries no full ClosedWorldV2 (seven "
    "members) or complete ResolutionCompletenessV2 record.")

# the wrong cross-reference in my own note
rep["p03CopiedBooleanNoteText"] = p03["copiedBooleanAloneNote"]["butThisIsNotAuthorization"]
rep["p03CopiedBooleanNotePointsTo"] = "p06"
rep["p06IsActually"] = "the coverage-partition probe, not an authorization probe"
rep["noExecutedAuthorizationControlWasRun"] = True

# ---------------- Point 4: p04 / p05 / p06 scope ----------------
src4 = S("p04_must2_config_kind.py")
rep["p04ControlBoundary"] = "native_evidence_model.typescript_config_graph_faults"
rep["p04UsesFillerDigests"] = "hashlib.sha256(path.encode()).hexdigest()" in src4
rep["p04CallsFullNativeContextAdmission"] = "admit_native_context" in src4
rep["p04ConstructedRuns"] = 0
p04 = L("p04-must2-config-kind.json")
rep["p04IdentityConsequenceMeasured"] = {
    "twoGraphDigestsComputedAndDiffer":
        p04["identityConsequence"]["twoReadingsMintTwoHashes"],
    "exactReadingHash": p04["identityConsequence"]["exactReadingHash"],
    "prefixReadingHash": p04["identityConsequence"]["prefixReadingHash"],
    "runIdsConstructed": 0,
    "runIdConsequenceIs": "the PUBLISHED derivation chain read from the law and "
                          "the contract (inspection), not two constructed Runs",
}
rep["p04ConfigOriginClaimSource"] = (
    "normative inspection of x-opensip-config-node-kind-law/derivedValueScope "
    "and native-evidence.md 2.2; NOT emitted by the 13 controls")

src5 = S("p05_should1_command_operation_map.py")
rep["p05UsesAuthorKeyFunctions"] = bool(
    re.search(r"M\.mutation_replay_scope", src5)
    and re.search(r"M\.mutation_replay_key", src5))
rep["p05IndependentlyReimplementedH"] = False
rep["p05WhatItActuallyEstablished"] = (
    "the preimage FIELD SET equals the published recipe, and the author's own "
    "key function is deterministic and sensitive to operation and requestId. "
    "The H encoding itself was NOT independently reimplemented.")

p06 = L("p06-should2-partition.json")
rep["p06FullRunControls"] = p06["caseCount"]
rep["p06Positives"] = len(p06["positiveRunIdentities"])
rep["p06TypedRefusals"] = p06["caseCount"] - len(p06["positiveRunIdentities"])
rep["p06OtherRelationChosen"] = p06["otherRelationChosen"]
rep["p06DifferentRelationBranchExecuted"] = p06["otherRelationChosen"] is not None
rep["p06UsesSharedAuthorFixture"] = "check-identity.py build()"
rep["p06TotalityEvidence"] = (
    "STATIC read of the relation registry: 13 relations, exactly one "
    "(`file`) carries a coverageTotality row. Not an executed totality control.")
overlap_case = next((c for c in p06["cases"]
                     if c["id"] == "NEG-two-no-coverage-scopes-overlap"), None)
rep["p06OverlapSubjectCount"] = 1
rep["p06TestsUtf8TieBreaking"] = False
rep["p06TieBreakNote"] = (
    "each overlap control has exactly ONE overlapping subject, so min() by UTF-8 "
    "bytes is trivial; the byte-order tie-break rule is NOT discriminated.")

# ---------------- Point 4b: admission vs prose classification ----------------
ADMISSION_ENFORCED = [
    "CB6-MUST-1", "CB6-MUST-2", "CB6-SHOULD-2", "CX-BV6-01", "CX-BV6-02",
    "CX-BV6-03", "BV6-V3-IMPORT-CAUSE", "CB6-NEW-3",
]
PARTLY_ENFORCED_PARTLY_PUBLISHED = [
    "CB6-SHOULD-1", "CX-BV6-04", "BV6-V3-RECEIPT", "BV6-V3-IMPORT-BINDING",
    "BV6-V3-IMPORT-SEMANTICS",
]
PROSE_OR_EVIDENCE = [
    "CB6-ADV-1", "CB6-ADV-2", "CB6-ADV-3", "CX-BV6-05", "CX-BV6-06",
    "CX-BV6-07", "CX-BV6-08", "CB6-NEW-1", "CB6-NEW-2", "CB6-NEW-4",
    "BV6-V3-PRECISION", "BV6-V4-CR-1", "BV6-V5-CR-1",
]
rep["findingRemedyClassification"] = {
    "admissionEnforced": ADMISSION_ENFORCED,
    "publishedLawPlusPartialEnforcement": PARTLY_ENFORCED_PARTLY_PUBLISHED,
    "proseOrEvidenceCorrection": PROSE_OR_EVIDENCE,
    "counts": {"admissionEnforced": len(ADMISSION_ENFORCED),
               "publishedLawPlusPartialEnforcement":
                   len(PARTLY_ENFORCED_PARTLY_PUBLISHED),
               "proseOrEvidenceCorrection": len(PROSE_OR_EVIDENCE)},
    "total": len(ADMISSION_ENFORCED) + len(PARTLY_ENFORCED_PARTLY_PUBLISHED)
             + len(PROSE_OR_EVIDENCE),
    "originalClaimWas": "all corrected 'in the admission, not merely in prose'",
    "correctedClaim": "8 are enforced at an executable boundary; 5 publish law "
                      "with partial executable enforcement; 13 are prose or "
                      "evidence-record corrections and are correctly so.",
}

# ---------------- Point 5: p10 scope + advisory lineage ----------------
p10 = L("p10-xref-corrected.json")
rep["p10RecordsScanned"] = len([r for r in p10["records"] if r.get("present")])
rep["p10IsWholeCorpusProof"] = False
rep["p10RawCounts"] = {
    "currentPinsResolved": p10["currentPinsResolved"],
    "historicalAsOfPins": p10["historicalAsOfPins"],
    "rawProblemsBeforeTriage": len(p10["problems"]),
}
rep["p10HistoricalClassificationNote"] = (
    "classifying a pin as as-of-then records that it does NOT match current "
    "bytes and sits under a historical key. It does NOT verify the old bytes.")

# advisory account lineage
import subprocess
V16X = "/tmp/opensip-design-corrections/post-reset-review.v17-clarification.v1/v16x"
acct = {}
for name in ("advisory-application-account.v16.proposed.json",
             "advisory-application-account.v16.json",
             "advisory-application-account.v17.proposed.json"):
    rel = "docs/coop/design-corrections/reviews/codex-post-reset.v1/" + name
    subprocess.run(["tar", "xzf", os.path.join(REV, "candidate-source.v16.tar.gz"), rel],
                   cwd=V16X, capture_output=True)
    p16 = os.path.join(V16X, rel)
    p17 = os.path.join(SUBJ, rel)
    acct[name] = {
        "inV16Tarball": os.path.isfile(p16),
        "inV17Subject": os.path.isfile(p17),
        "v16Items": len(json.load(open(p16))["items"]) if os.path.isfile(p16) else None,
        "v17Items": len(json.load(open(p17))["items"]) if os.path.isfile(p17) else None,
    }
# any other account files in the v17 subject
d = os.path.join(SUBJ, "docs/coop/design-corrections/reviews/codex-post-reset.v1")
acct["accountFilesPresentInV17Subject"] = sorted(
    f for f in os.listdir(d) if f.startswith("advisory-application-account"))
rep["advisoryAccountLineage"] = acct

# qualification gate flags
qg = json.load(open(os.path.join(
    SUBJ, "docs/coop/design-corrections/qualification-gates.proposed.json")))
items = qg["items"]
flagnames = sorted({k for it in items for k in it
                    if isinstance(it.get(k), bool)})
rep["qualificationGateBooleanFlags"] = {
    fn: {"true": sum(1 for it in items if it.get(fn) is True),
         "false": sum(1 for it in items if it.get(fn) is False)}
    for fn in flagnames}
rep["qualificationGateCount"] = len(items)
rep["allGateBooleanFlagsFalse"] = all(
    v["true"] == 0 for v in rep["qualificationGateBooleanFlags"].values())

with open(OUT, "w") as fh:
    json.dump(rep, fh, indent=1, sort_keys=True, default=str)

print("=== P3: p03 composition ===")
for k, v in rep["p03Composition"].items():
    print("   %-56s %d" % (k, v))
print("   total:", rep["p03TotalCases"])
print("   arithmetic:", rep["p03Arithmetic"])
print("   cross-plane covered native relations:",
      len(rep["p03CrossPlaneCoveredNativeRelations"]), "of",
      rep["p03NativeRelationCount"], "->", rep["p03CrossPlaneCoveredNativeRelations"])
print("   IS a full cross-product:", rep["p03IsFullCrossProduct"])
print("   full cross-product would be:", rep["p03FullCrossProductWouldBe"], "cases")
print("   roundtrip uses fixed relation 'references':",
      rep["p03RoundtripUsesFixedRelation"])
print("   roundtrip relation mismatch rows:",
      [r["target"] for r in rep["p03RoundtripRelationMismatch"]])
print("   all four producers emitted the same sole token:",
      rep["allFourProducersEmittedTheSameSoleToken"])
print()
print("=== P4: p04/p05/p06 ===")
print("   p04 boundary          :", rep["p04ControlBoundary"])
print("   p04 filler digests    :", rep["p04UsesFillerDigests"],
      "| full context admission:", rep["p04CallsFullNativeContextAdmission"],
      "| Runs constructed:", rep["p04ConstructedRuns"])
print("   p05 used author key fn:", rep["p05UsesAuthorKeyFunctions"],
      "| independently reimplemented H:", rep["p05IndependentlyReimplementedH"])
print("   p06 full-Run controls :", rep["p06FullRunControls"],
      "(%d positive, %d typed refusals)" % (rep["p06Positives"], rep["p06TypedRefusals"]))
print("   p06 different-relation branch executed:",
      rep["p06DifferentRelationBranchExecuted"],
      "(otherRelationChosen=%s)" % rep["p06OtherRelationChosen"])
print("   p06 tests UTF-8 tie-break:", rep["p06TestsUtf8TieBreaking"])
print()
print("   remedy classification:", json.dumps(
    rep["findingRemedyClassification"]["counts"]))
print()
print("=== P5 ===")
print("   p10 records scanned:", rep["p10RecordsScanned"], "| whole-corpus proof:",
      rep["p10IsWholeCorpusProof"])
print("   advisory account files in v17 subject:",
      rep["advisoryAccountLineage"]["accountFilesPresentInV17Subject"])
for k, v in rep["advisoryAccountLineage"].items():
    if isinstance(v, dict) and "v16Items" in v:
        print("     %-46s v16=%s v17=%s" % (k, v["v16Items"], v["v17Items"]))
print("   gate boolean flags:", json.dumps(rep["qualificationGateBooleanFlags"]))
print("   all gate flags false:", rep["allGateBooleanFlagsFalse"])
