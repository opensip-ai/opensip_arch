"""Assemble author-review.json from the actual probe artifacts, not from prose."""
import json, os

RT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.join(RT, 'probes')


def load(name):
    with open(os.path.join(HERE, name)) as fh:
        return json.load(fh)


handoff = json.load(open(os.path.join(RT, 'changed-file-handoff.json')))
lanes = json.load(open(os.path.join(RT, 'lane-results.json')))
baseline = load('author-source-baseline.json')
impact = load('impact-scan.json')
native = load('native-lane-detail.json')
checker = load('checker-stdout.json')
schema_patch = load('schema-annotation-patch.json')

cw = [c for c in checker['results'] if c['id'].startswith('repair-cw')]
standing = checker.get('repairClosedWorldStanding', {})

doc = {
    "sessionId": "919c766d-f2d0-4cfa-abaa-9d7425d9395f",
    "role": "SOURCE COAUTHOR on this turn; not an independent acceptor",
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
        "authorRoot": baseline['authorRoot'],
        "frozenRoot": baseline['frozenRoot'],
        "custodyClaimedFiles": 1353,
        "filesHashed": baseline['fileCount'],
        "exactFrozen31Matches": baseline['exactMatches'],
        "notInFrozen31": baseline['notInFrozen31'],
        "differFromFrozen31": baseline['differFromFrozen31'],
        "parentManifestSha256": "ca713db549f9337ae52a4bccc2ebbb84b136b8dc5d0545003bb3b2a24dfc95b5",
        "verifiedBeforeAuthoring": True,
    },

    "law": {
        "module": "docs/coop/design-corrections/workflows/repair_closed_world_selection.v1.py",
        "RS-1-unsafeSet": "every delete and every replace, unqualified; any one activates the gate; targets and edits are separate arrays with no published correspondence and no pointer is invented",
        "RS-2-relevantUniverses": "union of (a) all matching occurrences of every target fingerprint via finding3.subjectId -> subject3.universe, and (b) every universe owning an unsafe edited path via retained source-path subject scopes (file, clones, vcs-change; all universeRule same-only). A universe in neither does not veto. An unowned unsafe path is REPAIR.CLOSED_WORLD_NOT_ESTABLISHED, not guessed and not vacuous. Multiple ownership preserved.",
        "RS-3-selectedRecords": "every retained native coverage2 whose scope sourceUniverse is relevant; sourceUniverse ALONE decides relevance; independent of evidenceRequirements; dedupe by retained coverage2 identity; order by full partition key then identity",
        "RS-4-gate": "non-vacuous conjunction of deadCodeRepairEligible; a relevant universe with no native Coverage is not established; dynamicDispatch not read; imported observations contribute nothing",
        "RS-5-displaySummary": "five fields unchanged; conjunction plus per-field least-closed reduction; a DISPLAY SUMMARY, not a native producer record, never an input to the gate",
        "RS-6-createOnly": "no gate and no unmet from ineligibility alone, but the same reduction still runs so descriptor and repairPlanId stay deterministic including with zero native Coverage",
        "RS-7-identity": "descriptor shape and repairPlanId recipe unchanged; VALUES and Run identity are what move; no repairPlanId equality claimed across different Runs",
        "newPublicDetailCodes": [],
        "disclosedEnumLimit": "ClosedWorldV2.nonliteralLoading has no `unknown` member (none|present), so the empty-summary value is the least-closed pole `present`; a display convention, not an observation. Widening that enum is a native field-shape change this unit does not own and did not make.",
    },

    "changedFiles": handoff['changedFiles'],
    "changedFileIntegrity": {
        "baselineFileCount": handoff['baselineFileCount'],
        "currentFileCount": handoff['currentFileCount'],
        "undeclaredChanges": handoff['undeclaredChanges'],
        "missingFiles": handoff['missingFiles'],
        "beforeImageVerification": handoff['beforeImageVerification'],
    },
    "schemaAnnotationPatch": {
        "rows": schema_patch,
        "onlyChangedNode": "$defs/RepairPlanDescriptor/properties/closedWorld/description",
        "shapeProof": "both documents re-parsed, that one annotation blanked in each, remainder required byte-identical",
        "annotationBytesDidChange": True,
        "fieldShapeMemberSetOrMajorChanged": False,
    },

    "lanesExecuted": lanes['lanes'],
    "generatedReportsRestoredAfterRun": lanes['restoredAfterRun'],
    "workflowProjectionLane": {
        "passed": checker['passed'], "count": checker['count'],
        "failed": checker['failed'],
        "repairCwCheckCount": len(cw),
        "repairCwAllOk": all(c['ok'] for c in cw),
        "repairCwCheckIds": [c['id'] for c in cw],
    },
    "nativeLane": {
        "exitCode": native['exitCode'],
        "pinOnly": native['pinOnly'],
        "distinctFaultKinds": native['distinctFaultKinds'],
        "faultPaths": [f['path'] for f in native['faults']],
        "frozen31ExitCode": 0,
        "note": "exit 2 is entirely sha256 pin mismatch on exactly the seven edited files; zero semantic faults",
    },
    "pinLedgersInvalidatedNotEditedByAuthor": [
        {"ledger": row['ledger'], "brokenPaths": [b['pinnedPath'] for b in row.get('brokenByThisAuthor', [])]}
        for row in impact['pinLedgers'] if row.get('brokenByThisAuthor')
    ],

    "controlStanding": standing,

    "rootPointsAddressed": {
        "1-createOnlyStillBuildsDescriptor": "corrected; create-only summary defined and covered by two full-Run controls",
        "2-probeBScopeAndMajor": "corrected; new positive and conflicting negative derive from full admitted Runs and both schema majors are named; preview is not authorization",
        "3-probeEViolatedInputAssumption": "withdrawn as a defect claim; evaluator3 refuses a caller-selected record instead, and the historic adapter is not made a native validator",
        "4-conservativeEntryInvalidInput": "withdrawn; every record used is owner-minted and a control asserts native 4.5 true-only holds; no adjacent atom-model correction inferred",
        "5-fixtureScopeOverstated": "narrowed to the two fixtures actually measured",
        "6-equalIdClaim": "withdrawn; recipe/shape vs values/Run identity separated; annotation bytes acknowledged as changing",
        "7-underspecifiedPlusSibling": "target/edit mapping, zero-entry record, mixed case and full tie-breaking all defined; unsigned optional sibling withdrawn",
        "8-recipeScopedEvidence": "removed; selection is independent of evidenceRequirements, held by two full-Run controls",
    },

    "unexecutedBoundaries": [
        "real native producer qualification: all ClosedWorldV2 values are synthetic owner-minted observations",
        "repair apply, recover and verify; the security authorization path",
        "any Rust or TypeScript universe; only the fixture's two syntax universes",
        "a full admitted Run with an uncovered relevant universe or asymmetric ownership (fixture cannot produce one; UNIT controls only)",
        "vcs-change or clones acting as an actual path owner",
        "the imported evidence plane; its exclusion is structural, not tested",
        "pin ledger updates, deliberately left to root",
        "any native/identity schema field shape, native model, security, unrelated contracts, planning inventories, readiness or application records",
    ],

    "openQuestionsForRoot": [
        "the nonliteralLoading empty-summary convention; the alternative needs a native enum change that is not the author's",
        "whether the five UNIT controls should become full-Run controls, which needs a fixture with asymmetric extents",
        "whether repair_closed_world_selection.v1.py belongs in the three pin ledgers and any other lane's OWNED list",
    ],
}

out = os.path.join(RT, 'author-review.json')
json.dump(doc, open(out, 'w'), indent=2)
print('WROTE', out)
print('changed files', len(doc['changedFiles']), '| undeclared', len(doc['changedFileIntegrity']['undeclaredChanges']))
print('repair-cw checks', doc['workflowProjectionLane']['repairCwCheckCount'],
      'allOk', doc['workflowProjectionLane']['repairCwAllOk'])
print('lanes', [(l['lane'], l['exitCode']) for l in doc['lanesExecuted']])
