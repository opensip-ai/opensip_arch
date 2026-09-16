# Executed by build_review43.py in its own globals (exec) after the findings and rows parts. Assembles review.json, checks
# gaps, decides the verdict, renders review.md. Writes only RT/review.json and RT/review.md.

ALL_ROWS = F_ROWS + RES_ROWS + AR_ROWS + FW_ROWS + DR_ROWS + SCOPED_ROWS
ids = [r['id'] for r in ALL_ROWS]
if len(ALL_ROWS) != 107 or len(set(ids)) != 107 or set(ids) != set(V42ROWS):
    GAPS.append('disposition rows: %d (unique %d); id set equals source42: %s' % (len(ALL_ROWS), len(set(ids)), set(ids) == set(V42ROWS)))
for r in ALL_ROWS:
    if r['appliedByThisReview'] is not False or r['finalApplicationOutcomeGranted'] is not False:
        GAPS.append('row flag not false: ' + r['id'])
    if r['assessmentBasis'] not in (N, I) or not r['currentAssessment'] or not r['currentOwner'] or not r['consequence']:
        GAPS.append('row incomplete: ' + r['id'])
    if r['assessmentBasis'] == I and not r['unchanged42Basis']:
        GAPS.append('unchanged basis without quoted source42 basis: ' + r['id'])
if len(TCB['dependentRows']) != 13 or TCB['dependentRowCount'] != 13:
    GAPS.append('TCB dependent count is not 13')
nonF = [r['currentAssessment'] for r in ALL_ROWS if not r['id'].startswith('F-')]
if len(set(nonF)) != len(nonF):
    GAPS.append('duplicate current assessment texts among non-F rows')
prior_same = [r['id'] for r in ALL_ROWS if not r['id'].startswith('F-') and r['currentAssessment'] == V42ROWS[r['id']]['currentAssessment']]
if prior_same:
    GAPS.append('rows whose text is copied verbatim from source42: %s' % prior_same)

scope_complete = (not GAPS and groups_ok and children_ok and planning_ok and pkg_ok and verified_manifest and parent42_ok and pins_ok and reference_ok
                  and all(p.get('execution') is None or p['execution']['exitCode'] == 0 for p in PROBES))
if MUST:
    verdict = 'BLOCKER'
elif SHOULD:
    verdict = 'CHANGES_REQUIRED'
elif scope_complete:
    verdict = 'ACCEPT'
else:
    verdict = 'INCOMPLETE'
basis_text = ('No MUST, no SHOULD, no blocker. '
              'Availability: source43 corrects a source42 under-disclosure. A successful graph response now reports an observed partial or retained state in context.availability exactly, as identity-and-evidence ("A query reports both") and the query parity field require. '
              'Independently discriminated on one lawful closed Run with each tree\'s own modules: partial reports retained on source42 and partial on source43, with identical items and context. The same holds through the reference adapter record path, a trusted-latest join, a cursor continuation, and parity/renderers. '
              'A host observation grants nothing: every refusing state, precondition, public route, missing-byte and corrupt-byte case is unchanged and identical on both trees. '
              'Path orientation: section 4 selects the walk representation for a previously unspecified field and preserves the model behaviour, with byte-identical responses across trees and goldens for tie, order, depth and zero-hop. '
              'The cursor stays an opaque host token with same-host continuation, cache-loss and bound laws confirmed. Limitation and diagnostic prose obey schema, parity and route laws without canonical wording. No new public identity, error code or schema major exists, and RunIds are unchanged. '
              'ADV42-01 is retained as a non-blocking advisory; its root routing as a crates/host/src/analysis.rs implementation verification obligation is correctly scoped and is not a containment proof. S40-01 and ADV40-01 remain resolved. '
              'Also completed on verified copies: subject, archive, all members, parent42, the 9/0/0 delta, all pins, six pinned groups, 17 children, planning and inventory, package v20, the scope-preservation probes and final copy re-verification. '
              'Source-level acceptance only: no blind reconstruction, application, readiness, implementation authorization or product qualification is granted.')
review = {
    'schema': 'opensip.independent-design-review.source43.v1',
    'reviewer': 'Claude (independent design review origin %s, continuing after the completed source42 review; source43 charter; authored none of the reviewed bytes)' % ORIGIN,
    'standing': 'Source43 whole-design successor review. Not fresh-origin independence, blind reconstruction, final application acceptance, implementation authorization or product qualification.',
    'verdict': verdict, 'verdictBasis': basis_text,
    'subjectManifestPath': LIVE43, 'subjectManifestSha256': EXPECT['manifest43'], 'liveManifestSha256Measured': live43, 'verifiedManifest': verified_manifest,
    'subjectSnapshot': S43, 'subjectFileCount': SV['counts43']['fileCount'], 'subjectTotalBytes': SV['counts43']['totalBytes'],
    'subjectArchivePath': ARCHIVE43, 'subjectArchiveSha256': EXPECT['archive43'], 'archiveSha256Measured': archive43, 'archiveVerification': {k: summ(v) for k, v in ARCH.items()},
    'parent42': {'manifestSha256': SV['manifest42']['sha256'], 'declaredBy43': SV['parentChain']['43declares42'], 'snapshotVerified': SV['snapshot42']['verified'],
                 'members': SV['snapshot42']['members'], 'archiveSha256': EXPECT['archive42'], 'unchangedAndVerified': parent42_ok},
    'delta42to43': dict(DCOUNTS, changedPaths=[r['path'] for r in DELTA['changed']], addedPaths=[r['path'] for r in DELTA['added']], removedPaths=[r['path'] for r in DELTA['removed']],
                        diffs=DIFFSUM['42to43']),
    'ownedSourcePins': {'receipt': 'receipts/source-pins43.json', 'sha256': sha(REC + '/source-pins43.json'), 'allPinsMatch': PINS['allPinsMatch'], 'changedPinUnion': PINS['changedPinUnion'],
                        'ledgers': {k: {x: v[x] for x in ('ledgerSha256', 'entries', 'mismatchedAgainstManifest', 'changedPinsVs42', 'addedVs42', 'removedVs42')} for k, v in PINS['ledgers'].items()}, 'verified': pins_ok},
    'planningInputLayer': {'path': 'docs/v2/architecture/implementation-normative-inputs.v11.json', 'sha256': PC['layerSha256']['11'], 'expected': EXPECT['v11'], 'inputs': PC['layerInputs']['11'],
                           'retainedBecauseInputsUnchanged': PC['v11InputsIntersectingThe9ChangedFiles'] == [] and not PC['layerMismatchedAgainstSource43']['11']},
    'predecessorsPreserved': {'source42Review': {'path': V42PATH, 'sha256': sha(V42PATH), 'expected': EXPECT['review42'], 'verdict': V42['verdict'], 'modifiedByThisReview': False, 'conclusionInherited': False}},
    'readScope': {
        'rule': 'Whole-file claims only for fresh43Read (every line read this charter) and inheritedUnchanged42Read (counted as completely read by this origin\'s completed source42 review and byte-identical now; not re-read). complete42ReadPlusComplete43Diff is a complete predecessor read plus the exact diff. Delta reads, range reads, evidence reads and search-only sightings are not whole-file reads of source43 bytes. Hashes recomputed at build time.',
        'fresh43Read': fresh, 'fresh43RangeRead': ranged, 'deltaReads': delta_reads, 'complete42ReadPlusComplete43Diff': via_diff, 'inheritedUnchanged42Read': inherited,
        'changedPriorReadNotReread': changed_not, 'prior42RangeReadOnly': prior_ranges, 'searchOnlySightings': SEARCH_ONLY,
        'evidenceReads': evidence_reads, 'deltaFilesWithoutReadEntry': uncovered,
        'counts': {'fresh43Read': len(fresh), 'fresh43RangeRead': len(ranged), 'deltaReads': len(delta_reads), 'complete42ReadPlusComplete43Diff': len(via_diff),
                   'inheritedUnchanged42Read': len(inherited), 'changedPriorReadNotReread': len(changed_not), 'evidenceReads': len(evidence_reads), 'searchOnlySightings': len(SEARCH_ONLY)},
        'ledger': {'path': 'receipts/read-ledger.jsonl', 'sha256': sha(LEDGER), 'rows': len(ledger)},
    },
    'newMustIssues': MUST, 'newShouldIssues': SHOULD, 'advisories': ADVISORIES, 'observations': OBSERVATIONS,
    'priorFindingDispositions': PRIOR_DISPOSITIONS, 'itemDispositions': ITEMS,
    'probes': PROBES,
    'commandReceipts': {'referenceGroups': group_rows, 'referenceGroupsPassed': groups_ok, 'evaluator3Children': children, 'evaluator3ChildrenAllExit0': children_ok,
                        'foundationChecks': foundation_checks, 'planning': {k: P[k]['exitCode'] for k in ('check_implementation_planning', 'check_repository_file_inventory')},
                        'planningStdout': {k: P[k]['stdout'].strip() for k in ('check_implementation_planning', 'check_repository_file_inventory')},
                        'planningCounts': PC, 'planningOk': planning_ok,
                        'referenceComparison': {'receipt': 'receipts/reference-comparison.json', 'sha256': sha(REC + '/reference-comparison.json'), 'groups': RC['groups'],
                                                'childrenEqualRoot': RC['childrenEqualRoot'], 'childrenDifferingFromHistoricalMine42': RC['childrenDifferingFromHistoricalMine42'], 'ok': reference_ok},
                        'referenceChildrenStripped': {'receipt': 'receipts/reference-children-stripped.json', 'sha256': sha(REC + '/reference-children-stripped.json')},
                        'copyVerificationFinal': {'receipt': 'receipts/copy-verification-final.json', 'sha256': sha(REC + '/copy-verification-final.json'), 'result': {k: v['verified'] for k, v in COPYVER.items()}}},
    'childCompletion': {'referenceGroups': [(r['name'], r['exitCode'], r['timedOut']) for r in group_rows], 'evaluator3Children': len(children),
                        'probeRuns': {p['id']: p['execution']['exitCode'] for p in PROBES if p.get('execution')}, 'packageToolRuns': {k: v and v['exitCode'] for k, v in PKG_RUNS.items()},
                        'backgroundProcessesOutstanding': 0},
    'packageAssessment': PACKAGE, 'rootAndPackageEvidence': EVIDENCE, 'mapSources': MAP, 'graphQueryCoverageRows': GRAPH_COVERAGE_ROWS,
    'planningLayer': {'normativeInputsV11Sha256': PC['layerSha256']['11'], 'inputs': PC['layerInputs']['11'], 'paths': PC['inventoryPaths'], 'packages': PC['inventoryPackages'],
                      'mappings': PC['coverageMappings'], 'mappingsSource42': PC['coverageMappingsSource42'], 'reportFeatures': PC['coverageGroups']['reportFeatures'],
                      'plannedRecoveryCasesUnexecuted': PC['recoveryCasesNotExecuted'], 'milestones': 'M0-M6'},
    'fDispositions': F_ROWS, 'evaluationResidualDispositions': RES_ROWS, 'arDispositions': AR_ROWS, 'fwDispositions': FW_ROWS,
    'inheritedResidualDispositions': DR_ROWS, 'scopedReviewOwnerDispositions': SCOPED_ROWS, 'dispositionRowCount': len(ALL_ROWS),
    'assessmentBasisRule': BASIS_RULE, 'dispositionRowBasisCounts': {b: sum(1 for r in ALL_ROWS if r['assessmentBasis'] == b) for b in (N, I)},
    'sharedAssumptionTCBSCOPE01': TCB, 'retained': RETAINED, 'authority': AUTHORITY, 'limitations': LIMITATIONS,
}
receipt_files = sorted(p for p in glob.glob(REC + '/**/*', recursive=True) if os.path.isfile(p))
review['receiptInventory'] = [{'path': rel(p), 'sha256': sha(p)} for p in receipt_files] + [{'path': rel(p), 'sha256': sha(p)} for p in sorted(glob.glob(RT + '/probes/*.py'))]
review['buildGaps'] = GAPS
with open(RT + '/review.json', 'w', encoding='utf-8') as fh:
    json.dump(review, fh, indent=1, ensure_ascii=False, default=str)
    fh.write('\n')


def md_list(items):
    return '\n'.join('- ' + str(x) for x in items)


def cell(s):
    return str(s).replace('|', '\\|').replace('\n', ' ')


L = []
A = L.append
A('# Independent design review — source43 (whole-design successor)\n')
A('**Reviewer:** %s  ' % review['reviewer'])
A('**Standing:** %s\n' % review['standing'])
A('## Verdict: %s\n' % verdict)
A(basis_text + '\n')
A('## Subject\n')
A('| Item | Value |\n|---|---|')
for k in ('subjectManifestSha256', 'liveManifestSha256Measured', 'verifiedManifest', 'subjectFileCount', 'subjectTotalBytes', 'subjectArchiveSha256', 'archiveSha256Measured'):
    A('| %s | `%s` |' % (k, review[k]))
A('| parent42 | `%s` declared by 43: %s; snapshot verified: %s (%s members); archive `%s` |' % (review['parent42']['manifestSha256'], review['parent42']['declaredBy43'], review['parent42']['snapshotVerified'], review['parent42']['members'], EXPECT['archive42']))
A('| delta 42to43 | %s changed, %s added, %s removed |' % (DCOUNTS['changed'], DCOUNTS['added'], DCOUNTS['removed']))
A('| owned source pins | all match: %s; changed pins: %s |' % (PINS['allPinsMatch'], ', '.join('`%s`' % p.replace('docs/coop/design-corrections/', '') for p in PINS['changedPinUnion'])))
A('| planning input layer v11 | `%s` (%d inputs, retained: unchanged inputs) |' % (PC['layerSha256']['11'], PC['layerInputs']['11']))
A('')
A('Changed files: ' + ', '.join('`%s`' % p for p in review['delta42to43']['changedPaths']) + '\n')
A('## Issues\n')
A('No MUST issue. No SHOULD issue. No new advisory.\n')
for a in ADVISORIES:
    A('### %s (%s, %s): %s\n' % (a['id'], a['severity'], a['origin'], a['title']))
    A('**Current standing.** ' + a['currentStanding'] + '\n')
    A('**Standing assessment.** ' + a['standingAssessment'] + '\n')
    A(md_list(a['selectors']) + '\n')
    A('**Detail (source42, unchanged bytes).** ' + a['detail'] + '\n')
    A('**Consequence.** ' + a['consequence'] + '\n')
    A('**Disposition.** ' + a['disposition'] + '\n')
    A('**Measured on source43**\n\n```json\n' + json.dumps(a['measuredOnSource43'], indent=1, default=str)[:4000] + '\n```\n')
A('## Observations (not defects)\n')
for o in OBSERVATIONS:
    A('- **%s** %s (%s)' % (o['id'], o['text'], o['receipt']))
A('')
A('## Current dispositions of prior findings, advisories and observations\n')
A('| id | current disposition | basis |\n|---|---|---|')
for d in PRIOR_DISPOSITIONS:
    A('| %s | %s | %s |' % (d['id'], cell(d['currentDisposition']), cell(d['basis'])))
A('')
A('## Item dispositions\n')
for it in ITEMS:
    A('### %s: %s\n' % (it['id'], it['disposition']))
    A(it['assessment'] + '\n')
    if it.get('scopeBasis'):
        A('| scope | basis | current source43 evidence | unchanged-42 basis |\n|---|---|---|---|')
        for s in it['scopeBasis']:
            A('| %s | %s | %s | %s |' % (cell(s['scope']), cell(s['basis']), cell(s['current43']), cell(s['unchanged42'] or '-')))
        A('')
        A('Unchanged-42 items standing on byte-identical owners: ' + ', '.join('%s (%s)' % (u['id'], u['source42Disposition']) for u in it['unchanged42Items']) + '\n')
        A('| ported probe | rows | same case set as source42 | observations differing from source42 |\n|---|---|---|---|')
        for k, v in it['portedProbes'].items():
            A('| %s | %d | %s | %s |' % (k, v['rows'], v['sameCaseSetAsSource42'], len(v['observedDifferFromSource42'])))
        A('')
A('## Package v20\n')
A(PACKAGE['result'] + '\n')
A(md_list(PACKAGE['limits']) + '\n')
A('| control | owner admission | semantic admission | reason |\n|---|---|---|---|')
for c in PACKAGE['normalizationMapControls']:
    A('| %s | %s | %s | %s |' % (c['name'], c['ownerAdmission'], c['semanticAdmission'], cell(c['reason'])))
A('')
A('## Commands and probes\n')
A('| group | exit | seconds | stdout sha256 | equal root | equal codex | equal own source42 |\n|---|---|---|---|---|---|---|')
for r in group_rows:
    g = RC['groups'][r['name']]
    A('| %s | %s | %s | `%s` | %s | %s | %s |' % (r['name'], r['exitCode'], r['seconds'], r['stdoutSha256'], g['stdoutFileEqualRoot'], g['stdoutFileEqualCodex'], g['stdoutEqualHistoricalMine42']))
A('\nevaluator3 children: %d, all exit 0: %s; query-projection checks %s (failed %s); execution-inputs cases %s; enumeration cases %s. Planning: %s. Planning counts ok: %s.\n'
  % (len(children), children_ok, children['query-projection'].get('checksCount'), children['query-projection'].get('failedCount'), children['execution-inputs'].get('casesCount'),
     children['enumeration'].get('casesCount'), review['commandReceipts']['planningStdout'], planning_ok))
A('| probe | rows | failed | run receipt | earlier attempts |\n|---|---|---|---|---|')
for p in PROBES:
    if p.get('execution'):
        A('| %s | %s | %s | %s | %s |' % (p['id'], (p.get('result') or {}).get('rows', '-'), len((p.get('result') or {}).get('failedRows', [])), p['execution']['runReceipt'], len(p['execution']['earlierAttempts'])))
    else:
        A('| %s | (command receipt) | - | %s | - |' % (p['id'], ', '.join(p['receipts'])))
A('')
A('## Read coverage\n')
A(review['readScope']['rule'] + '\n')
A('```json\n' + json.dumps(review['readScope']['counts'], indent=1) + '\n```\n')
A('Delta files without a read entry: %s.\n' % (uncovered or 'none'))
A('Fresh whole-file reads:\n\n' + md_list('%s (%s lines, sha256 `%s`)' % (e['path'], e['lines'], e['sha256']) for e in fresh) + '\n')
A('Range reads:\n\n' + md_list('%s: %s (sha256 `%s`)' % (e['path'], ', '.join(e['ranges']), e['sha256']) for e in ranged) + '\n')
A('Complete diff reads:\n\n' + md_list('%s (%s; diff `%s`)' % (e['path'], e['readClass'], e['diffSha256']) for e in delta_reads) + '\n')
A('Evidence reads:\n\n' + md_list('%s: %s' % (e['path'], ', '.join(e['ranges'])) for e in evidence_reads) + '\n')
A('Search-only sightings (not reads):\n\n' + md_list('%s: %s — %s' % (s['path'], s['lines'], s['standing']) for s in SEARCH_ONLY) + '\n')
A('Inherited unchanged source42 whole-file reads (not re-read): %d files; complete source42 read plus complete 42->43 diff: %d; listed in review.json.\n' % (len(inherited), len(via_diff)))
A('## TCB-SCOPE-01 (assessed once)\n')
A('**Assumption.** %s\n\n**Consequence.** %s\n\n**Dependent rows (%d).** %s\n' % (TCB['assumption'], TCB['consequence'], TCB['dependentRowCount'], ', '.join(TCB['dependentRows'])))
A('**Current assessment.** ' + TCB['currentAssessment'] + '\n')
A(md_list(TCB['substantiveCurrentAssessment']) + '\n')
A('**Position:** %s. **Standing:** %s. **Adjudication owner:** %s\n' % (TCB['reviewerPosition'], TCB['standing'], TCB['adjudicationOwner']))
A('## Disposition rows (%d)\n' % len(ALL_ROWS))
A('All rows: appliedByThisReview=false, finalApplicationOutcomeGranted=false. No grade is assigned; scoped owner rows are routing only.\n')
A('**Basis rule.** %s Counts: %s.\n' % (BASIS_RULE, json.dumps(review['dispositionRowBasisCounts'])))
A('| id | prior42 | disposition | basis | current assessment | owner | consequence |\n|---|---|---|---|---|---|---|')
for r in ALL_ROWS:
    A('| %s | %s | %s | %s | %s | %s | %s |' % (r['id'], cell(r['prior42Disposition']), cell(r['disposition']), r['assessmentBasis'], cell(r['currentAssessment']), cell(r['currentOwner']), cell(r['consequence'])))
A('\nThe quoted source42 basis of every unchanged-42-basis row is in review.json (`unchanged42Basis`).\n')
A('## Retained obligations\n')
A('```json\n' + json.dumps(RETAINED, indent=1) + '\n```\n')
A('## Authority\n')
A('```json\n' + json.dumps(AUTHORITY, indent=1) + '\n```\n')
A('## Limitations\n')
A(md_list(LIMITATIONS) + '\n')
A('## Build gaps\n')
A(md_list(GAPS) if GAPS else 'none')
with open(RT + '/review.md', 'w', encoding='utf-8') as fh:
    fh.write('\n'.join(L) + '\n')
print(json.dumps({'verdict': verdict, 'verifiedManifest': verified_manifest, 'rows': len(ALL_ROWS), 'gaps': GAPS, 'readCounts': review['readScope']['counts'],
                  'basisCounts': review['dispositionRowBasisCounts'], 'reviewJsonSha256': sha(RT + '/review.json'), 'reviewMdSha256': sha(RT + '/review.md')}, indent=1))
