# Executed by build_review40.py in its own globals (exec) after build_review40_rows.py. Assembles review.json, checks gaps,
# renders review.md. Writes only RT/review.json and RT/review.md.

ALL_ROWS = F_ROWS + RES_ROWS + AR_ROWS + FW_ROWS + DR_ROWS + SCOPED_ROWS
ids = [r['id'] for r in ALL_ROWS]
if len(ALL_ROWS) != 107 or len(set(ids)) != 107:
    GAPS.append('disposition rows: %d (unique %d), expected 107' % (len(ALL_ROWS), len(set(ids))))
if set(ids) != set(V39ROWS):
    GAPS.append('row ids differ from source39: missing %s extra %s' % (sorted(set(V39ROWS) - set(ids)), sorted(set(ids) - set(V39ROWS))))
for r in ALL_ROWS:
    if r['appliedByThisReview'] is not False or r['finalApplicationOutcomeGranted'] is not False:
        GAPS.append('row flag not false: ' + r['id'])
    if r['assessmentBasis'] not in (N, I) or not r['assessment']:
        GAPS.append('row basis or assessment missing: ' + r['id'])
texts = [r['assessment'] for r in ALL_ROWS if not r['id'].startswith('F-')]
if len(set(texts)) != len(texts):
    GAPS.append('duplicate assessment texts among non-F rows')

verdict = 'CHANGES_REQUIRED' if SHOULD else 'ACCEPT'
basis_text = ('One SHOULD issue is unresolved (S40-01). CellProgramOutcomeV1.viewDigests attribution, and through it stage-receipt outputRefs and selectedRefs, has no published recipe. The reference decides it with an unpublished capability-relation criterion, the literal schema reading is refused, and two conforming encodings of the same stage returns both admit with different ExecutionInputsV1 digests, so different Run identities. '
              'It is pre-existing (owner bytes unchanged 39->40) and was demonstrated by reviewer-minted graphs through the maintained builder and reference admission. There is no MUST issue and no blocker. '
              'S39-01 and S39-02 are closed at source level with discriminating probes against source39 bytes; ADV39-01 is closed by an exact, truthful account; ADV38-01/02/03 remain closed; ADV40-01 is editorial. '
              'Subject, archive, all members, parent39, the delta, six pinned groups (all pass), 17 evaluator3 children, planning and inventory checks, package v17 content agreement and every reviewer probe ran to completion. Source-level result only.')

review = {
    'schema': 'opensip.independent-design-review.source40.v1',
    'reviewer': 'Claude (independent design review origin %s; source40 charter; authored none of the reviewed bytes)' % ORIGIN,
    'standing': 'Independent whole-design successor review of frozen source40. Not final application review, not inheritance of the source39 review, not blind reconstruction, not readiness, implementation authorization or product qualification.',
    'verdict': verdict, 'verdictBasis': basis_text,
    'subjectManifestPath': LIVE40, 'subjectManifestSha256': EXPECT['manifest40'], 'liveManifestSha256Measured': live40, 'verifiedManifest': verified_manifest,
    'subjectSnapshot': S40, 'subjectFileCount': SV['fileCount40'], 'subjectTotalBytes': SV['totalBytes40'],
    'subjectArchivePath': ARCHIVE40, 'subjectArchiveSha256': EXPECT['archive40'], 'archiveSha256Measured': archive40, 'archiveVerification': archives,
    'parentManifestSha256': EXPECT['manifest39'], 'parentManifestSha256Measured': live39, 'parentUnchangedAndVerified': parent_ok,
    'delta39to40': dict(delta_counts, changedPaths=[r['path'] for r in delta['changed']], addedPaths=sorted(added_paths)),
    'planningInputLayer': {'path': 'docs/v2/architecture/implementation-normative-inputs.v9.json', 'sha256': PC['v9Sha256'], 'expected': EXPECT['v9']},
    'predecessorsPreserved': {'source39Review': {'path': V39PATH, 'sha256': sha(V39PATH), 'verdict': v39['verdict'], 'modifiedByThisReview': False, 'conclusionInherited': False}},
    'readScope': {
        'rule': 'Whole-file claims are made only for fresh40Read (every line read this charter) and inheritedUnchanged39Read (counted as completely read by this origin\'s source39 review and byte-identical now; not re-read). complete39ReadPlusComplete40Diff is a complete predecessor read plus the exact complete diff. delta40Read, fresh40RangeRead, prior39RangeReadOnly and searchOnlySightings are not whole-file reads. Hashes were recomputed at build time.',
        'fresh40Read': fresh, 'fresh40RangeRead': ranged, 'delta40Read': delta_reads, 'complete39ReadPlusComplete40Diff': via_diff,
        'inheritedUnchanged39Read': inherited, 'changedPriorReadNotReread': changed_not, 'prior39RangeReadOnly': prior_ranges, 'searchOnlySightings': SEARCH_ONLY,
        'deltaFilesWithoutReadEntry': uncovered_delta,
        'counts': {'fresh40Read': len(fresh), 'fresh40RangeRead': len(ranged), 'delta40Read': len(delta_reads), 'complete39ReadPlusComplete40Diff': len(via_diff),
                   'inheritedUnchanged39Read': len(inherited), 'changedPriorReadNotReread': len(changed_not)},
        'ledger': {'path': 'receipts/read-ledger.jsonl', 'sha256': sha(LEDGER), 'rows': len(ledger)},
    },
    'newMustIssues': [], 'newShouldIssues': SHOULD, 'advisories': ADVISORIES, 'observations': OBSERVATIONS,
    'findingDispositions': [{'id': 'S40-01', 'disposition': 'OPEN-SHOULD; route to the foundation execution-inputs owner'},
                            {'id': 'ADV40-01', 'disposition': 'EDITORIAL; route to the architecture planning-layer owner; non-blocking'}],
    'itemDispositions': ITEMS,
    'probes': PROBES,
    'commandReceipts': {'referenceGroups': group_rows, 'referenceGroupsPassed': groups_ok, 'evaluator3Children': children, 'evaluator3ChildrenAllExit0': children_ok,
                        'foundationChecks': foundation_checks, 'planning': {k: P[k]['exitCode'] for k in ('check_implementation_planning', 'check_repository_file_inventory')},
                        'planningCounts': PC, 'planningOk': planning_ok, 'referenceComparison': {'receipt': 'receipts/reference-comparison.json', 'sha256': sha(REC + '/reference-comparison.json'),
                                                                                                  'groups': RC['groups'], 'childrenEqual': RC['childrenEqual']}},
    'childCompletion': {'referenceGroups': [(r['name'], r['exitCode'], r['timedOut']) for r in group_rows], 'evaluator3Children': len(children),
                        'planning': {k: P[k]['exitCode'] for k in ('check_implementation_planning', 'check_repository_file_inventory')},
                        'probeRuns': {p['id']: p['execution']['exitCode'] for p in PROBES if p.get('execution')}, 'packageToolRuns': {k: v and v['exitCode'] for k, v in PKG_RUNS.items()},
                        'backgroundProcessesOutstanding': 0},
    'packageAssessment': PACKAGE,
    'rootAndAuthorEvidence': EVIDENCE,
    'planningLayer': {'normativeInputsV9Sha256': PC['v9Sha256'], 'inputs': PC['v9Inputs'], 'paths': PC['inventoryPaths'], 'packages': PC['inventoryPackages'],
                      'mappings': PC['coverageMappings'], 'mappingsSource39': PC['coverageMappingsSource39'], 'mappingsSource38': v39['planningLayer']['mappingsSource38'],
                      'reportFeatures': PC['coverageGroups']['reportFeatures'], 'plannedRecoveryCasesUnexecuted': PC['recoveryCasesNotExecuted'], 'milestones': 'M0-M6'},
    'mapSources': MAP,
    'fDispositions': F_ROWS, 'evaluationResidualDispositions': RES_ROWS, 'arDispositions': AR_ROWS, 'fwDispositions': FW_ROWS,
    'inheritedResidualDispositions': DR_ROWS, 'scopedReviewOwnerDispositions': SCOPED_ROWS, 'dispositionRowCount': len(ALL_ROWS),
    'assessmentBasisRule': BASIS_RULE,
    'dispositionRowBasisCounts': {b: sum(1 for r in ALL_ROWS if r['assessmentBasis'] == b) for b in (N, I)},
    'sharedAssumptionTCBSCOPE01': TCB, 'retained': RETAINED, 'authority': AUTHORITY, 'limitations': LIMITATIONS,
}
receipt_files = sorted(p for p in glob.glob(REC + '/**/*', recursive=True) if os.path.isfile(p))
review['receiptInventory'] = [{'path': rel(p), 'sha256': sha(p)} for p in receipt_files] + \
                             [{'path': rel(p), 'sha256': sha(p)} for p in sorted(glob.glob(RT + '/probes/*.py'))]
review['buildGaps'] = GAPS

with open(RT + '/review.json', 'w', encoding='utf-8') as fh:
    json.dump(review, fh, indent=1, ensure_ascii=False)
    fh.write('\n')


def md_list(items):
    return '\n'.join('- ' + str(x) for x in items)


def cell(s):
    return str(s).replace('|', '\\|').replace('\n', ' ')


L = []
A = L.append
A('# Independent design review — source40 (whole-design successor)\n')
A('**Reviewer:** %s  ' % review['reviewer'])
A('**Standing:** %s\n' % review['standing'])
A('## Verdict: %s\n' % verdict)
A(basis_text + '\n')
A('## Subject\n')
A('| Item | Value |\n|---|---|')
for k in ('subjectManifestSha256', 'liveManifestSha256Measured', 'verifiedManifest', 'subjectFileCount', 'subjectTotalBytes', 'subjectArchiveSha256', 'archiveSha256Measured',
          'parentManifestSha256', 'parentUnchangedAndVerified'):
    A('| %s | `%s` |' % (k, review[k]))
A('| delta 39->40 | %d changed, %d added, %d removed |' % (delta_counts['changed'], delta_counts['added'], delta_counts['removed']))
A('| planning input layer v9 | `%s` |' % PC['v9Sha256'])
A('')
A('## New issues\n')
A('No MUST issue.\n')
for f in SHOULD:
    A('### %s (%s): %s\n' % (f['id'], f['severity'], f['title']))
    A('**Selectors**\n\n' + md_list(f['selectors']) + '\n')
    A('**Measured**\n\n```json\n' + json.dumps(f['measured'], indent=1) + '\n```\n')
    A('**Detail.** ' + f['detail'] + '\n')
    A('**Consequence.** ' + f['consequence'] + '\n')
    A('**Required change.** ' + f['requiredChange'] + '\n')
    A('**Owner.** ' + f['owner'] + '  \n**Receipts.** ' + ', '.join(f['receipts']) + '\n')
for a in ADVISORIES:
    A('### %s (%s): %s\n' % (a['id'], a['severity'], a['title']))
    A(md_list(a['selectors']) + '\n\n' + a['detail'] + '\n\n**Disposition.** ' + a['disposition'] + '\n')
A('## Observations (not defects)\n')
for o in OBSERVATIONS:
    A('- **%s** %s (%s)' % (o['id'], o['text'], o['receipt']))
A('')
A('## Item dispositions\n')
for it in ITEMS:
    A('### %s: %s\n' % (it['id'], it['disposition']))
    A('*Origin:* %s%s\n' % (it['origin'], ('; prior39: ' + it['prior39Disposition']) if it.get('prior39Disposition') else ''))
    A(md_list(it['selectors']) + '\n')
    A(it['assessment'] + '\n')
A('## Package v17\n')
A(PACKAGE['result'] + '\n')
A(md_list(PACKAGE['limits']) + '\n')
A('Normalization-map negatives (exact, not generalized):\n')
A('| control | owner admission | semantic admission | reason |\n|---|---|---|---|')
for c in PACKAGE['normalizationMapControls']:
    A('| %s | %s | %s | %s |' % (c['name'], c['ownerAdmission'], c['semanticAdmission'], cell(c['reason'])))
A('')
A('## Commands and probes\n')
A('| group | exit | seconds | stdout sha256 |\n|---|---|---|---|')
for r in group_rows:
    A('| %s | %s | %s | `%s` |' % (r['name'], r['exitCode'], r['seconds'], r['stdoutSha256']))
A('\nevaluator3 children: %d, all exit 0: %s. Planning: %s. Planning counts ok: %s.\n' % (len(children), children_ok, review['commandReceipts']['planning'], planning_ok))
A('| probe | rows | failed | run receipt | earlier attempts |\n|---|---|---|---|---|')
for p in PROBES:
    if p.get('execution'):
        A('| %s | %s | %s | %s | %s |' % (p['id'], p['result']['rows'], len(p['result']['failedRows']), p['execution']['runReceipt'], len(p['execution']['earlierAttempts'])))
    else:
        A('| %s | (command receipt) | - | %s | - |' % (p['id'], ', '.join(p['receipts'])))
A('')
A('## Read coverage\n')
A(review['readScope']['rule'] + '\n')
A('```json\n' + json.dumps(review['readScope']['counts'], indent=1) + '\n```\n')
A('Delta files without a read entry: %s\n' % (uncovered_delta or 'none'))
A('Fresh whole-file reads this charter:\n\n' + md_list('%s (%s lines)' % (e['path'], e['lines']) for e in fresh) + '\n')
A('Range reads this charter:\n\n' + md_list('%s: %s' % (e['path'], ', '.join(e['ranges'])) for e in ranged) + '\n')
A('Complete source39 read plus complete 39->40 diff: %s\n' % (', '.join(e['path'] for e in via_diff) or 'none'))
A('Inherited unchanged source39 whole-file reads (not re-read): %d files, listed in review.json.\n' % len(inherited))
A('## TCB-SCOPE-01 (assessed once)\n')
A('**Assumption.** %s\n\n**Consequence.** %s\n\n**Dependent rows (%d).** %s\n' % (TCB['assumption'], TCB['consequence'], TCB['dependentRowCount'], ', '.join(TCB['dependentRows'])))
A(md_list(TCB['substantiveCurrentAssessment']) + '\n')
A('**Position:** %s. **Standing:** %s. **Adjudication owner:** %s\n' % (TCB['reviewerPosition'], TCB['standing'], TCB['adjudicationOwner']))
A('## Disposition rows (%d)\n' % len(ALL_ROWS))
A('All rows: appliedByThisReview=false, finalApplicationOutcomeGranted=false. Author grades are not assigned.\n')
A('**Basis rule.** %s Counts: %s.\n' % (BASIS_RULE, json.dumps(review['dispositionRowBasisCounts'])))
A('| id | prior39 | disposition | basis | assessment |\n|---|---|---|---|---|')
for r in ALL_ROWS:
    A('| %s | %s | %s | %s | %s |' % (r['id'], cell(r['prior39Disposition']), cell(r['disposition']), r['assessmentBasis'], cell(r['assessment'])))
A('')
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
                  'reviewJsonSha256': sha(RT + '/review.json'), 'reviewMdSha256': sha(RT + '/review.md')}, indent=1))
