"""Assemble author-review.json from the actual probe artifacts."""
import json, os

RT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.join(RT, 'probes')


def load(name, root=HERE):
    return json.load(open(os.path.join(root, name)))


handoff = load('changed-file-handoff.json', RT)
lanes = load('lane-results.json', RT)
baseline = load('v2-source-baseline.json')
checker = load('checker-report.json')
native = load('native-lane-detail.json')
admission = load('symbol-only-admission.json')
schema_patch = load('schema-annotation-patch.json')

cw = [c for c in checker['results'] if c['id'].startswith('repair-cw')]
standing = checker.get('repairClosedWorldStanding', {})

doc = {
    "sessionId": "919c766d-f2d0-4cfa-abaa-9d7425d9395f",
    "turn": "source coauthor v2",
    "standing": "AUTHOR_PENDING_REVIEW",
    "authorAcceptanceClaimed": False,
    "rootAgreementClaimedForNewBytes": False,
    "finalDesignBlindOrApplicationAcceptance": "never from this origin",
    "consumerOutputsUsed": False,
    "productImplementation": False,
    "gitOperations": False,
    "nativeProducerQualificationClaimed": False,
    "fullProductRepairClaimed": False,

    "inputCustody": {
        "v2Root": baseline['v2Root'],
        "custodyDeclared": baseline['custodyDeclared'],
        "v2FileCount": baseline['v2FileCount'],
        "custodyMismatches": baseline['custodyMismatches'],
        "extra": baseline['extra'], "missing": baseline['missing'],
        "differsFromV1Source": baseline['v1Differ'],
        "v1HandoffCarriedIntoV2": all(r['match'] for r in baseline['v1HandoffCarried']),
        "verifiedBeforeAuthoring": True,
    },

    "RRS_A1": {
        "correction": "path ownership is the RETAINED SELECTED-PROGRAM CENSUS of this Run's EnumerationPlanV1, not source-path Coverage scopes",
        "retainedJoin": "run3 -> plan2 -> analysisSpecDigest -> analysis-spec parameters -> the entry resolving through identity-model.v3.parameter_row_of to foundation/enumeration-plan.schema.v1.json",
        "guaranteed": "REQUIRED evaluator3 parameter; evaluator_input_model.v3.required_parameters refuses EVALUATOR_REQUIRED_PARAMETER_MISSING without it and full replay re-admits it",
        "notUsed": ["caller-selected map", "optional unsigned sidecar", "filename parsing",
                    "path reconstruction from an opaque native symbol ID"],
        "applicablePathCensus": "each selected binding's own extents[] per kind plus candidateSourcePaths",
        "availableBinding": "non-null universe contributes that universe",
        "unavailableSelectedBinding": "universe=null with a retained extent containing an unsafe path is TYPED unresolved ownership; it does not vanish behind a closed owner",
        "unselectedBinding": "never inferred as an owner",
        "extentKindPrecision": "file/package are host membership extents; symbol is the selected program's code scope; all snapshot files are not every compiler's programRootFiles",
        "unrelatedProgramsStayUnrelated": True,
        "multipleOwnershipPreserved": True,
        "sourcePathScopes": "ADDITIONAL retained witness; redundancy measured via witnessOnlyUniverses, never a completeness certificate",
        "coverageSelectionUniverse": "sourceUniverse ALONE decides relevance; independent of evidenceRequirements",
        "reachabilityAtEnumerationOwner": {
            "standing": admission['standing'],
            "symbolOnlySelectedAvailableUniverse": admission['caseB_symbolOnlySelectedAvailableUniverse']['result'],
            "unavailableSelectedBinding": admission['caseC_unavailableSelectedBinding']['result'],
            "candidateOnlyCell": admission['caseD_candidateOnlyCell']['result'],
            "conclusion": "admission does NOT prevent the omission; the hypothesised case is reachable and was not refuted",
        },
    },

    "RRS_A2": {
        "emptyDisplaySentinel": {"deadCodeRepairEligible": False, "exportsClosed": "unknown",
                                 "entryPointsRecognized": "none", "nonliteralLoading": "present",
                                 "externalConsumers": "unknown"},
        "sentinelDescription": "five-field LEAST-CLOSED display sentinel; NOT an all-unknown record; exactly two members are unknown and THREE are not, the false boolean included",
        "noMemberAuthoritative": True,
        "absenceFoldedIntoDisplay": "a relevant universe with no Coverage, or an unresolved ownership, folds the sentinel into the reduction so the display cannot read closed while eligibility is refused",
        "orderingPublished": {"encoding": "UTF-8 bytes",
                              "members": ["relation", "resolution", "sourceUniverse",
                                          "targetUniverse", "subjectScopeCommitment", "coverageId"]},
        "remedyNamesExactRecord": "all six ordering members unabbreviated, including the retained coverage2 identity",
        "dynamicDispatch": "not read by the gate; keeps its target-relative affected_targets and per-requirement sufficiency roles",
        "separateRequirements": ["recipe trust", "policy consent", "current-snapshot equality",
                                 "authorization bound to the exact repairPlanId"],
        "previewIsNotAuthorization": True,
        "noRepairPlanIdEqualityAcrossDifferentEvidenceRunIds": True,
    },

    "fullAdmittedAsymmetricControl": {
        "runId": "run3:896bef61cbe9969d20ccd93d7948ffbee2cedb747eb0ebf633584f96aaf1e63d",
        "admittedBy": "identity-model.v3.close_run (complete evaluator3 semantic replay)",
        "shape": "universe A binds only the inventory cell (file extent, file@enumerated scope); universe B binds only the symbol-kind syntax cell (symbol extent) and has NO source-path scope; B's declares Coverage dissents",
        "sourcePathOnlyOwners": "the file-extent universe only",
        "censusOwners": "both",
        "oldLawOutcome": "would admit the delete",
        "correctedLawOutcome": "refuses, naming the declares record",
        "alsoDrivenThroughCurrentPreview": True,
        "rootHadNotClaimedSuchAReproduction": True,
    },

    "changedFiles": handoff['changedFiles'],
    "changedFileIntegrity": {
        "baselineFileCount": handoff['baselineFileCount'],
        "currentFileCount": handoff['currentFileCount'],
        "undeclaredChanges": handoff['undeclaredChanges'],
        "unexpectedNewFiles": handoff['unexpectedNewFiles'],
        "missingFiles": handoff['missingFiles'],
    },
    "authorizedFixtureExtension": {
        "path": "docs/coop/design-corrections/foundation/evaluator_graph_fixture.v3.py",
        "category": "authorized-bounded-fixture-extension (separate handoff entry)",
        "option": "symbol_only_second_program (default OFF)",
        "alsoChanged": "required-native pair split that the option needs so each view binds to its own cell outcome",
        "defaultsAltered": False,
        "baselineRunUnchanged": "run3:fbc6cee45b8d9c8060320eece887ea6667a6e794706ec2783a285582ab60fe9c",
        "identityOrNativeAdmissionChangedToPass": False,
    },
    "schemaAnnotationPatch": {
        "rows": schema_patch,
        "onlyChangedNode": "$defs/RepairPlanDescriptor/properties/closedWorld/description",
        "shapeProof": "both documents re-parsed, that annotation blanked, remainder required byte-identical",
        "annotationBytesDidChange": True,
        "fieldShapeMemberSetKeyOrderOrMajorChanged": False,
    },

    "lanesExecuted": lanes['lanes'],
    "generatedSourceReportsPreservedAndRestored": lanes['generatedSourceReportsPreservedAndRestored'],
    "workflowProjectionLane": {
        "passed": checker['passed'], "count": checker['count'], "failed": checker['failed'],
        "repairCwCheckCount": len(cw), "repairCwAllOk": all(c['ok'] for c in cw),
        "repairCwCheckIds": [c['id'] for c in cw],
    },
    "nativeLanePrecision": {
        "exitCode": native['exitCode'],
        "stoppedAt": native['stoppedAt'],
        "reported": native['reported'],
        "distinctFaultKinds": native['distinctFaultKinds'],
        "faultPaths": native['faultPaths'],
        "semanticChecksExecuted": native['semanticChecksExecuted'],
        "precision": native['precision'],
    },
    "pinLedgersInvalidatedNotEditedByAuthor": handoff['pinLedgersInvalidatedNotEditedByAuthor'],
    "controlStanding": standing,

    "independentReviewScopeCorrections": [
        "its RRS-A2 remedy demonstration used file@enumerated with sourceUniverse != targetUniverse; file is universeRule same-only, so those are NOT two lawfully admitted native records, and abbreviated pseudo-IDs are not retained identities. That claim is not repeated.",
        "the structural fact it reports -- the old remedy omitted coverageId, targetUniverse and the scope commitment -- is real and is fixed.",
        "the conforming discriminating controls keep file source==target and separate records by subjectScopeCommitment and coverage2 identity, and use imports (universeRule admitted-target) for the cross-universe key.",
        "the display sentinel has THREE non-unknown members, not two: the false boolean as well as the two enums.",
        "no full-Run remedy counterexample is claimed by root, by the reviewer, or by this author.",
        "its RRS-A1 evidence is static normative plus a unit-scoped probe with no full-Run counterexample, by its own statement; the full-Run asymmetric control reported here is this author's, executed this turn.",
    ],

    "unexecutedBoundaries": [
        "real native producer qualification: all ClosedWorldV2 values are synthetic owner-minted observations",
        "repair apply, recover and verify; the security authorization path",
        "any Rust or TypeScript universe; Rust sourceUnitOwnership multi-target ownership is covered by rule, not by execution",
        "unavailable, unselected and candidate-only bindings inside a full Run (UNIT controls plus a separate enumeration-owner admission probe)",
        "vcs-change or clones acting as an actual retained witness",
        "the imported evidence plane; its exclusion is structural, not tested",
        "pin ledger updates, deliberately left to root",
        "the native lane's semantic checks, which did not run because it stopped at pin admission",
        "any identity/native schema field shape, native model, security, unrelated contract, planning inventory, readiness or application record",
        "root's separate glob source, which was neither read nor overwritten",
    ],

    "openQuestionsForRoot": [
        "whether the asymmetric graph belongs in evaluator_graph_fixture.v3.py or in a workflows-local fixture",
        "whether the four UNIT binding controls should become full-Run controls, which needs fixture support for unavailable/candidate-only bindings",
        "pin sealing for the nine changed files plus adding repair_closed_world_selection.v1.py to the three populated ledgers",
    ],
}

out = os.path.join(RT, 'author-review.json')
json.dump(doc, open(out, 'w'), indent=2)
print('WROTE', out)
print('changed', len(doc['changedFiles']), '| undeclared', len(doc['changedFileIntegrity']['undeclaredChanges']))
print('repair-cw', doc['workflowProjectionLane']['repairCwCheckCount'],
      'allOk', doc['workflowProjectionLane']['repairCwAllOk'])
print('lanes', [(l['lane'].split(' (')[0], l['exitCode']) for l in doc['lanesExecuted']])
