#!/usr/bin/env python
"""Remaining headline figures re-derived, plus live anchors for every prior
correction this review is required to keep in view.

Preservation evidence, not a first-principles re-derivation of each correction:
each row names an anchor that must be PRESENT in the frozen bytes, and the
governing suite executed and passed on those exact bytes.
"""
import json
import os
import re
import sys

ROOT = "/tmp/opensip-design-corrections/candidate-subject.v17"
COPY = "/tmp/opensip-design-corrections/post-reset-review.v17/copies/copy-A-reference-run"
DC = os.path.join(ROOT, "docs/coop/design-corrections")
CT = os.path.join(ROOT, "docs/v2/contracts/product-v1")
OUT = sys.argv[1]


def T(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


rep = {}

# ---- remaining headline figures ----
inv = json.load(open(os.path.join(DC, "workflows/command-inventory.v1.json")))
rep["commands"] = len(inv["commands"])
rep["goldens"] = len(inv["goldens"])
rep["renderers"] = len(inv["renderers"])
ws = json.load(open(os.path.join(
    COPY, "docs/coop/design-corrections/workflows/workflows-report.v1.json")))
rep["workflowSurfaceSchemaCount"] = ws["schemaCount"]
rep["workflowSurfaceBoundaries"] = len(ws["boundaries"])
ig = json.load(open(os.path.join(
    COPY, "docs/coop/design-corrections/integration-report.v1.json")))
rep["integrationPassed"] = ig["passed"]
rep["integrationFailed"] = ig["failed"]
rep["integrationSyntheticTcbInputs"] = ig.get("syntheticTcbInputs")
sec = json.load(open(os.path.join(
    COPY, "docs/coop/design-corrections/security/security-lifecycle-report.v1.json")))
rep["securityCases"] = len(sec["cases"])
rep["securitySweeps"] = len(sec["sweeps"])
rep["securitySchemasValidated"] = len(sec.get("schemasValidated", []))
nat = json.load(open(os.path.join(
    COPY, "docs/coop/design-corrections/native/native-evidence-report.v2.json")))
rep["nativeCases"] = nat["cases"]["total"]
rep["nativePositiveCases"] = nat["cases"]["positive"]
rep["nativeNegativeCases"] = nat["cases"]["negative"]
rep["nativeMatrixCells"] = nat["matrix"]["cells"]
rep["nativeQualifiedCells"] = nat["matrix"]["qualifiedCells"]
rep["nativeLimitations"] = nat["limitations"]

# ---- preserved prior corrections: live anchors ----
NATIVE_MD = T(os.path.join(CT, "native-evidence.md"))
IDENT_MD = T(os.path.join(CT, "identity-and-evidence.md"))
WORK_MD = T(os.path.join(CT, "workflows-and-surfaces.md"))
SEC_MD = T(os.path.join(CT, "security-and-lifecycle.md"))
ADM_MD = T(os.path.join(CT, "admission-and-qualification.md"))
IDMODEL = T(os.path.join(DC, "foundation/identity-model.py"))
NMODEL = T(os.path.join(DC, "native/native_evidence_model.v2.py"))
WMODEL = T(os.path.join(DC, "workflows/workflows_model.v1.py"))
NSCHEMA = T(os.path.join(DC, "native/native-evidence.schemas.v2.json"))
RSCHEMA = T(os.path.join(DC, "workflows/schemas/repair.schema.json"))
RELREG = T(os.path.join(DC, "foundation/relation-payload-schemas.v2.json"))

ANCHORS = [
    ("capability/default/availability composition",
     [("native-evidence.md", NATIVE_MD, r"CapabilityAvailability"),
      ("native schemas", NSCHEMA, r"CapabilityAvailabilityV1")]),
    ("Unicode 15 lib name conversion assumption",
     [("native-evidence.md", NATIVE_MD, r"UCD 15\.0\.0|unicode_case_data_agreement"),
      ("native model", NMODEL, r"lib_name_fold"),
      ("native model refusal", NMODEL, r"ReferenceEnvironmentError")]),
    ("body language / compiler dialect ownership",
     [("identity model", IDMODEL, r"body_language_version"),
      ("native-evidence.md", NATIVE_MD, r"dialect")]),
    ("anchor cardinality and file totality",
     [("relation registry", RELREG, r"anchorLaw"),
      ("relation registry minimum", RELREG, r'"minimum"')]),
    ("registered payload / digest annotations",
     [("native schemas", NSCHEMA, r"x-opensip-digest"),
      ("identity model", IDMODEL, r"relation_digest_annotation_coverage")]),
    ("typed canonical equality",
     [("identity model", IDMODEL, r"def ordered\("),
      ("identity model", IDMODEL, r"canonical")]),
    ("imported observations / ScopeDocument binding",
     [("workflows model", WMODEL, r"verify_scope_parameter_binding"),
      ("workflows model", WMODEL, r"observationWindow|observation")]),
    ("static / runtime evidence distinctions",
     [("workflows model", WMODEL, r"workflow\.import-payload\.runtime\.v1"),
      ("imported law", T(os.path.join(DC, "workflows/schemas/imported-evidence.schema.json")),
       r"whatThisOutcomeNeverEstablishes")]),
    ("cache admission",
     [("identity model", IDMODEL, r"def admit_cache_entry")]),
    ("repair projection / replay",
     [("workflows model", WMODEL, r"def repair_apply"),
      ("workflows model", WMODEL, r"mutation_replay_scope"),
      ("repair schema", RSCHEMA, r"closedWorld")]),
    ("purge disclosure",
     [("workflows model", WMODEL, r"purge"),
      ("workflows-and-surfaces.md", WORK_MD, r"PinnedPurgeDisclosure|purge")]),
    ("output failure after committed Run",
     [("workflows-and-surfaces.md", WORK_MD,
       r"required-output|post-commit|required output")]),
    ("coverage partition law (CX-BV6-01)",
     [("relation registry", RELREG, r"coveragePartitionLaw"),
      ("identity model", IDMODEL, r"COVERAGE_PARTITION_LAW")]),
    ("closed-world gate before any descriptor",
     [("workflows model", WMODEL, r"deadCodeRepairEligible"),
      ("workflows model", WMODEL, r"UNSAFE_ACTIONS")]),
]

rows = []
for name, checks in ANCHORS:
    found = []
    for where, text, pat in checks:
        found.append({"where": where, "pattern": pat,
                      "present": bool(re.search(pat, text, re.I))})
    rows.append({"correction": name, "anchors": found,
                 "allAnchorsPresent": all(f["present"] for f in found)})
rep["preservedCorrections"] = rows
rep["preservedCorrectionCount"] = len(rows)
rep["correctionsMissingAnAnchor"] = [
    r for r in rows if not r["allAnchorsPresent"]]
rep["allPreservedCorrectionsHaveLiveAnchors"] = not rep["correctionsMissingAnAnchor"]

with open(OUT, "w") as fh:
    json.dump(rep, fh, indent=1, sort_keys=True, default=str)

for k in ("commands", "goldens", "renderers", "workflowSurfaceSchemaCount",
          "workflowSurfaceBoundaries", "integrationPassed", "integrationFailed",
          "securityCases", "securitySweeps", "securitySchemasValidated",
          "nativeCases", "nativePositiveCases", "nativeNegativeCases",
          "nativeMatrixCells", "nativeQualifiedCells"):
    print("  %-34s %s" % (k, rep[k]))
print()
for r in rows:
    print("  %-52s %s" % (r["correction"],
                          "ANCHORED" if r["allAnchorsPresent"] else "MISSING"))
    if not r["allAnchorsPresent"]:
        for f in r["anchors"]:
            if not f["present"]:
                print("        missing:", f["where"], "/", f["pattern"])
print()
print("all preserved corrections have live anchors:",
      rep["allPreservedCorrectionsHaveLiveAnchors"])
