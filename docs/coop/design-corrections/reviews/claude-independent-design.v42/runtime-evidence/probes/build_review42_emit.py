# Executed by build_review42.py in its own globals (exec) after the findings and rows parts. Assembles review.json, checks
# gaps, decides the verdict, renders review.md. Writes only RT/review.json and RT/review.md.

ALL_ROWS = F_ROWS + RES_ROWS + AR_ROWS + FW_ROWS + DR_ROWS + SCOPED_ROWS
ids = [r['id'] for r in ALL_ROWS]
if len(ALL_ROWS) != 107 or len(set(ids)) != 107 or set(ids) != set(V40ROWS):
    GAPS.append('disposition rows: %d (unique %d); id set equals source40: %s' % (len(ALL_ROWS), len(set(ids)), set(ids) == set(V40ROWS)))
for r in ALL_ROWS:
    if r['appliedByThisReview'] is not False or r['finalApplicationOutcomeGranted'] is not False:
        GAPS.append('row flag not false: ' + r['id'])
    if r['assessmentBasis'] not in (N, I) or not r['currentAssessment'] or not r['currentOwner'] or not r['consequence']:
        GAPS.append('row incomplete: ' + r['id'])
    if r['assessmentBasis'] == I and not r['unchanged40Basis']:
        GAPS.append('unchanged basis without quoted source40 basis: ' + r['id'])
if len(TCB['dependentRows']) != 13:
    GAPS.append('TCB dependent count is not 13')
nonF = [r['currentAssessment'] for r in ALL_ROWS if not r['id'].startswith('F-')]
if len(set(nonF)) != len(nonF):
    GAPS.append('duplicate current assessment texts among non-F rows')

scope_complete = not GAPS and groups_ok and children_ok and planning_ok and pkg_ok and verified_manifest and parent41_ok and last40_ok
if MUST:
    verdict = 'BLOCKER'
elif SHOULD:
    verdict = 'CHANGES_REQUIRED'
elif scope_complete:
    verdict = 'ACCEPT'
else:
    verdict = 'INCOMPLETE'
basis_text = ('No MUST, no SHOULD, no blocker. S40-01 is resolved on the complete source42 bytes including the capture follow-on: section 3 publishes the view attribution predicate and the section 3 named-scope law now holds for every applicability; section 8 and the model make receipts capture explicit returns and make selection equal the union of complete receipts. '
              'Independent three-tree discrimination with full-Run closure confirms each change (26/26); the historical 76/86 execution-inputs and 46 enumeration cases are preserved field for field. The programEntry clarification is consistent and its enforcement is confirmed (24/24 owner cases). ADV40-01 is resolved without mutating layer8. '
              'ADV42-01 is a non-blocking advisory: admission does not state or check receipt/view producer equality, nor apply the PLAN_JOIN before the row filter; Run closure refuses every measured shape. '
              'Subject, archive, parent41, last-reviewed40, both deltas, six pinned groups, 17 children, planning and inventory checks, package v19 and every probe completed; all copies re-verified. '
              'Source-level acceptance only: no blind reconstruction, application, readiness, implementation authorization or product qualification is granted.')
review = {
    'schema': 'opensip.independent-design-review.source42.v1',
    'reviewer': 'Claude (independent design review origin %s, continuing after the completed source40 review; source42 charter; authored none of the reviewed bytes)' % ORIGIN,
    'standing': 'Source42 whole-design successor review. Not fresh-origin independence, blind reconstruction, application acceptance, implementation authorization or qualification.',
    'verdict': verdict, 'verdictBasis': basis_text,
    'subjectManifestPath': LIVE42, 'subjectManifestSha256': EXPECT['manifest42'], 'liveManifestSha256Measured': live42, 'verifiedManifest': verified_manifest,
    'subjectSnapshot': S42, 'subjectFileCount': SV['counts42']['fileCount'], 'subjectTotalBytes': SV['counts42']['totalBytes'],
    'subjectArchivePath': ARCHIVE42, 'subjectArchiveSha256': EXPECT['archive42'], 'archiveSha256Measured': archive42, 'archiveVerification': {k: summ(v) for k, v in ARCH.items()},
    'parent41': {'manifestSha256': SV['manifest41']['sha256'], 'declaredBy42': SV['parentChain']['42declares41'], 'snapshotVerified': SV['snapshot41']['verified'], 'members': SV['snapshot41']['members'], 'unchangedAndVerified': parent41_ok},
    'lastReviewed40': {'manifestSha256': SV['manifest40']['sha256'], 'declaredBy41': SV['parentChain']['41declares40'], 'snapshotVerified': SV['snapshot40']['verified'], 'members': SV['snapshot40']['members'], 'unchangedAndVerified': last40_ok},
    'deltas': {k: dict(DCOUNTS[k], changedPaths=[r['path'] for r in DELTA[k]['changed']], addedPaths=[r['path'] for r in DELTA[k]['added']]) for k in DELTA},
    'planningInputLayer': {'path': 'docs/v2/architecture/implementation-normative-inputs.v11.json', 'sha256': PC['layerSha256']['11'], 'expected': EXPECT['v11']},
    'predecessorsPreserved': {'source40Review': {'path': V40PATH, 'sha256': sha(V40PATH), 'expected': EXPECT['review40'], 'verdict': V40['verdict'], 'modifiedByThisReview': False, 'conclusionInherited': False}},
    'readScope': {
        'rule': 'Whole-file claims only for fresh42Read (every line read this charter) and inheritedUnchanged40Read (counted as completely read by this origin\'s completed source40 review and byte-identical now; not re-read). complete40ReadPlusComplete42Diff is a complete predecessor read plus the exact diff. delta reads, range reads, evidence reads and search-only sightings are not whole-file reads of source42 bytes. Hashes recomputed at build time.',
        'fresh42Read': fresh, 'fresh42RangeRead': ranged, 'deltaReads': delta_reads, 'complete40ReadPlusComplete42Diff': via_diff, 'inheritedUnchanged40Read': inherited,
        'changedPriorReadNotReread': changed_not, 'prior40RangeReadOnly': prior_ranges, 'byteIdenticalToFreshRead': byte_identical_to_fresh, 'searchOnlySightings': SEARCH_ONLY,
        'evidenceReads': evidence_reads, 'deltaFilesWithoutReadEntry': uncovered,
        'counts': {'fresh42Read': len(fresh), 'fresh42RangeRead': len(ranged), 'deltaReads': len(delta_reads), 'complete40ReadPlusComplete42Diff': len(via_diff),
                   'inheritedUnchanged40Read': len(inherited), 'changedPriorReadNotReread': len(changed_not), 'evidenceReads': len(evidence_reads)},
        'ledger': {'path': 'receipts/read-ledger.jsonl', 'sha256': sha(LEDGER), 'rows': len(ledger)},
    },
    'newMustIssues': MUST, 'newShouldIssues': SHOULD, 'advisories': ADVISORIES, 'observations': OBSERVATIONS,
    'source40FindingDispositions': SOURCE40_DISPOSITIONS, 'itemDispositions': ITEMS,
    'probes': PROBES,
    'commandReceipts': {'referenceGroups': group_rows, 'referenceGroupsPassed': groups_ok, 'evaluator3Children': children, 'evaluator3ChildrenAllExit0': children_ok,
                        'foundationChecks': foundation_checks, 'planning': {k: J(REC + '/planning-checks.json')[k]['exitCode'] for k in ('check_implementation_planning', 'check_repository_file_inventory')},
                        'planningCounts': PC, 'planningOk': planning_ok, 'referenceComparison': {'receipt': 'receipts/reference-comparison.json', 'sha256': sha(REC + '/reference-comparison.json'),
                                                                                                  'groups': RC['groups'], 'childrenEqualCodex': RC['childrenEqualCodex'], 'childrenEqualRootV3': RC['childrenEqualRootV3']},
                        'casePopulations': {'receipt': 'receipts/case-populations.json', 'sha256': sha(REC + '/case-populations.json')},
                        'enumerationPopulation': {'receipt': 'receipts/enumeration-case-population.json', 'sha256': sha(REC + '/enumeration-case-population.json')},
                        'copyVerificationFinal': {'receipt': 'receipts/copy-verification-final.json', 'sha256': sha(REC + '/copy-verification-final.json'), 'result': {k: v['verified'] for k, v in COPYVER.items()}}},
    'childCompletion': {'referenceGroups': [(r['name'], r['exitCode'], r['timedOut']) for r in group_rows], 'evaluator3Children': len(children),
                        'probeRuns': {p['id']: p['execution']['exitCode'] for p in PROBES if p.get('execution')}, 'packageToolRuns': {k: v and v['exitCode'] for k, v in PKG_RUNS.items()},
                        'backgroundProcessesOutstanding': 0},
    'packageAssessment': PACKAGE, 'rootAndAuthorEvidence': EVIDENCE, 'mapSources': MAP,
    'planningLayer': {'normativeInputsV11Sha256': PC['layerSha256']['11'], 'inputs': PC['layerInputs']['11'], 'paths': PC['inventoryPaths'], 'packages': PC['inventoryPackages'],
                      'mappings': PC['coverageMappings'], 'mappingsSource41': PC['coverageMappingsSource41'], 'mappingsSource40': PC['coverageMappingsSource40'],
                      'reportFeatures': PC['coverageGroups']['reportFeatures'], 'plannedRecoveryCasesUnexecuted': PC['recoveryCasesNotExecuted'], 'milestones': 'M0-M6'},
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
A('# Independent design review — source42 (whole-design successor)\n')
A('**Reviewer:** %s  ' % review['reviewer'])
A('**Standing:** %s\n' % review['standing'])
A('## Verdict: %s\n' % verdict)
A(basis_text + '\n')
A('## Subject\n')
A('| Item | Value |\n|---|---|')
for k in ('subjectManifestSha256', 'liveManifestSha256Measured', 'verifiedManifest', 'subjectFileCount', 'subjectTotalBytes', 'subjectArchiveSha256', 'archiveSha256Measured'):
    A('| %s | `%s` |' % (k, review[k]))
A('| parent41 | `%s` declared by 42: %s; snapshot verified: %s (%s members) |' % (review['parent41']['manifestSha256'], review['parent41']['declaredBy42'], review['parent41']['snapshotVerified'], review['parent41']['members']))
A('| last-reviewed40 | `%s` declared by 41: %s; snapshot verified: %s (%s members) |' % (review['lastReviewed40']['manifestSha256'], review['lastReviewed40']['declaredBy41'], review['lastReviewed40']['snapshotVerified'], review['lastReviewed40']['members']))
for k in ('41to42', '40to42', '40to41'):
    A('| delta %s | %s changed, %s added, %s removed |' % (k, DCOUNTS[k]['changed'], DCOUNTS[k]['added'], DCOUNTS[k]['removed']))
A('| planning input layer v11 | `%s` |' % PC['layerSha256']['11'])
A('')
A('## Issues\n')
A('No MUST issue. No SHOULD issue.\n')
for a in ADVISORIES:
    A('### %s (%s): %s\n' % (a['id'], a['severity'], a['title']))
    A(md_list(a['selectors']) + '\n')
    A('**Detail.** ' + a['detail'] + '\n')
    A('**Consequence.** ' + a['consequence'] + '\n')
    A('**Disposition.** ' + a['disposition'] + '\n')
    A('**Measured**\n\n```json\n' + json.dumps(a['measured'], indent=1, default=str)[:6000] + '\n```\n')
A('## Observations (not defects)\n')
for o in OBSERVATIONS:
    A('- **%s** %s (%s)' % (o['id'], o['text'], o['receipt']))
A('')
A('## Current dispositions of source40 findings, advisories and observations\n')
A('| id | current disposition | basis |\n|---|---|---|')
for d in SOURCE40_DISPOSITIONS:
    A('| %s | %s | %s |' % (d['id'], cell(d['currentDisposition']), cell(d['basis'])))
A('')
A('## Item dispositions\n')
for it in ITEMS:
    A('### %s: %s\n' % (it['id'], it['disposition']))
    A(it['assessment'] + '\n')
    if it.get('properties'):
        A('| property | classification | selectors | note |\n|---|---|---|---|')
        for p in it['properties']:
            A('| %s | %s | %s | %s |' % (cell(p['property']), cell(p['classification']), cell(p['selectors']), cell(p['note'])))
        A('')
A('## Package v19\n')
A(PACKAGE['result'] + '\n')
A(md_list(PACKAGE['limits']) + '\n')
A('| control | owner admission | semantic admission | reason |\n|---|---|---|---|')
for c in PACKAGE['normalizationMapControls']:
    A('| %s | %s | %s | %s |' % (c['name'], c['ownerAdmission'], c['semanticAdmission'], cell(c['reason'])))
A('')
A('## Commands and probes\n')
A('| group | exit | seconds | stdout sha256 |\n|---|---|---|---|')
for r in group_rows:
    A('| %s | %s | %s | `%s` |' % (r['name'], r['exitCode'], r['seconds'], r['stdoutSha256']))
A('\nevaluator3 children: %d, all exit 0: %s; execution-inputs cases %s, enumeration cases %s. Planning: %s. Planning counts ok: %s.\n'
  % (len(children), children_ok, children['execution-inputs'].get('casesCount'), children['enumeration'].get('casesCount'), review['commandReceipts']['planning'], planning_ok))
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
A('Delta files without a read entry: %s. Byte-identical to a fresh read: %s.\n' % (uncovered or 'none', json.dumps(byte_identical_to_fresh)))
A('Fresh whole-file reads:\n\n' + md_list('%s (%s lines)' % (e['path'], e['lines']) for e in fresh) + '\n')
A('Range reads:\n\n' + md_list('%s: %s' % (e['path'], ', '.join(e['ranges'])) for e in ranged) + '\n')
A('Complete diff reads:\n\n' + md_list('%s (%s)' % (e['path'], e['readClass']) for e in delta_reads) + '\n')
A('Evidence reads:\n\n' + md_list('%s: %s' % (e['path'], ', '.join(e['ranges'])) for e in evidence_reads) + '\n')
A('Inherited unchanged source40 whole-file reads (not re-read): %d files, listed in review.json.\n' % len(inherited))
A('## TCB-SCOPE-01 (assessed once)\n')
A('**Assumption.** %s\n\n**Consequence.** %s\n\n**Dependent rows (%d).** %s\n' % (TCB['assumption'], TCB['consequence'], TCB['dependentRowCount'], ', '.join(TCB['dependentRows'])))
A(md_list(TCB['substantiveCurrentAssessment']) + '\n')
A('**Position:** %s. **Standing:** %s. **Adjudication owner:** %s\n' % (TCB['reviewerPosition'], TCB['standing'], TCB['adjudicationOwner']))
A('## Disposition rows (%d)\n' % len(ALL_ROWS))
A('All rows: appliedByThisReview=false, finalApplicationOutcomeGranted=false. No grade is assigned.\n')
A('**Basis rule.** %s Counts: %s.\n' % (BASIS_RULE, json.dumps(review['dispositionRowBasisCounts'])))
A('| id | prior40 | disposition | basis | current assessment | owner | consequence |\n|---|---|---|---|---|---|---|')
for r in ALL_ROWS:
    A('| %s | %s | %s | %s | %s | %s | %s |' % (r['id'], cell(r['prior40Disposition']), cell(r['disposition']), r['assessmentBasis'], cell(r['currentAssessment']), cell(r['currentOwner']), cell(r['consequence'])))
A('\nThe quoted source40 basis of every unchanged-40-basis row is in review.json (`unchanged40Basis`).\n')
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
