# Executed by build_review45.py in its own globals (exec) after the findings and rows parts. Assembles review.json, checks
# gaps, decides the verdict, renders review.md. Writes only RT/review.json and RT/review.md.

ALL_ROWS = F_ROWS + RES_ROWS + AR_ROWS + FW_ROWS + DR_ROWS + SCOPED_ROWS
ids = [r['id'] for r in ALL_ROWS]
if len(ALL_ROWS) != 107 or len(set(ids)) != 107 or set(ids) != set(V44ROWS):
    GAPS.append('disposition rows: %d (unique %d); id set equals source44: %s' % (len(ALL_ROWS), len(set(ids)), set(ids) == set(V44ROWS)))
for r in ALL_ROWS:
    if r['appliedByThisReview'] is not False or r['finalApplicationOutcomeGranted'] is not False:
        GAPS.append('row flag not false: ' + r['id'])
    if r['assessmentBasis'] not in (N, I) or not r['currentAssessment'] or not r['currentOwner'] or not r['consequence']:
        GAPS.append('row incomplete: ' + r['id'])
    if r['assessmentBasis'] == I and not r['unchanged44Basis']:
        GAPS.append('unchanged basis without quoted source44 basis: ' + r['id'])
if len(TCB['dependentRows']) != 13 or TCB['dependentRowCount'] != 13:
    GAPS.append('TCB dependent count is not 13')
nonF = [r['currentAssessment'] for r in ALL_ROWS if not r['id'].startswith('F-')]
if len(set(nonF)) != len(nonF):
    GAPS.append('duplicate current assessment texts among non-F rows')
prior_same = [r['id'] for r in ALL_ROWS if not r['id'].startswith('F-') and r['currentAssessment'] == V44ROWS[r['id']]['currentAssessment']]
if prior_same:
    GAPS.append('rows whose text is copied verbatim from source44: %s' % prior_same)

scope_complete = (not GAPS and groups_ok and children_ok and planning_ok and pkg_ok and verified_manifest and parent44_ok and pins_ok and reference_ok
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
              'Source45 closes a real under-specification. Source44 section 9.7 named closed_world_v2 for the pre-analysis host-conversion closedWorld without publishing its output. Source45 publishes the complete record in section 9.7 and as the startup-law member hostConversionClosedWorld, and scopes it to this conversion and both languages, disclaiming any proof of absent dynamic loading or dispatch. '
              'Derived independently from section 4.5 and the registered ClosedWorldV2 schema, exportsClosed unknown, entryPointsRecognized none and deadCodeRepairEligible false are forced; the remaining members are lawful published choices that cannot enable closed exports or repair. '
              'For TypeScript and Rust, every minted entry carries exactly the published record and admits, and the entries and coverage2 identities are byte-identical to the source44 exchange, so no identity changes. '
              'The model now copies the published law. The two changed cases pin every field, and a law mutation is detected where the source44 cases could not detect a helper mutation. The checker refuses each of the three mutated sources with its exact binding fault. '
              'The repair consumer stays refused for conversion-only selections; a non-authoritative display artifact is observed. The native-cases change is a reindent plus two expectation additions, and the generic historical-batch prose is clarified per language with registered shapes unchanged. '
              'Planning v13 binds the two changed normative inputs and preserves v8-v12. ADV42-01 and ADV44-01 are retained as non-blocking advisories, and S40-01 and ADV40-01 remain resolved. The source44 reference-scope limits stay material (OBS45-10). '
              'Also completed on verified copies: subject, archive, all 12,920 members, parent44, the 14/1/0 delta, all 6,264 pins, six pinned groups, 17 children, planning and inventory, package v22 with RunIds measured unchanged, ten scope-preservation probes, startup re-execution and final copy re-verification. '
              'Source-level acceptance only: no blind reconstruction, application, readiness, implementation authorization or product qualification is granted.')
review = {
    'schema': 'opensip.independent-design-review.source45.v1',
    'reviewer': 'Claude (independent design review origin %s, continuing after the completed source44 review; source45 charter; authored none of the reviewed bytes)' % ORIGIN,
    'standing': 'Source45 whole-design successor review. Not fresh-origin independence, blind reconstruction, final application acceptance, implementation authorization or product qualification.',
    'verdict': verdict, 'verdictBasis': basis_text,
    'subjectManifestPath': LIVE45, 'subjectManifestSha256': EXPECT['manifest45'], 'liveManifestSha256Measured': live45, 'verifiedManifest': verified_manifest,
    'subjectSnapshot': S45, 'subjectFileCount': SV['counts45']['fileCount'], 'subjectTotalBytes': SV['counts45']['totalBytes'],
    'subjectArchivePath': ARCHIVE45, 'subjectArchiveSha256': EXPECT['archive45'], 'archiveSha256Measured': archive45, 'archiveVerification': {k: summ(v) for k, v in ARCH.items()},
    'parent44': {'manifestSha256': SV['manifest44']['sha256'], 'declaredBy45': SV['parentChain']['45declares44'], 'snapshotVerified': SV['snapshot44']['verified'],
                 'members': SV['snapshot44']['members'], 'archiveSha256': EXPECT['archive44'], 'unchangedAndVerified': parent44_ok},
    'delta44to45': dict(DCOUNTS, changedPaths=[r['path'] for r in DELTA['changed']], addedPaths=[r['path'] for r in DELTA['added']], removedPaths=[r['path'] for r in DELTA['removed']],
                        diffs=DIFFSUM['44to45']),
    'ownedSourcePins': {'receipt': 'receipts/source-pins45.json', 'sha256': sha(REC + '/source-pins45.json'), 'totalPinEntries': PINS['totalPinEntries'], 'allPinsMatch': PINS['allPinsMatch'],
                        'changedPinUnion': PINS['changedPinUnion'], 'addedPinUnion': PINS['addedPinUnion'], 'deltaFilesPinnedByNoLedger': PINS['deltaFilesPinnedByNoLedger'],
                        'ledgers': {k: {x: v[x] for x in ('ledgerSha256', 'entries', 'mismatchedAgainstManifest', 'changedPinsVs44', 'addedVs44', 'removedVs44')} for k, v in PINS['ledgers'].items()}, 'verified': pins_ok},
    'planningInputLayer': {'path': ARCHD + 'implementation-normative-inputs.v13.json', 'sha256': PC['layerSha256']['13'], 'expected': EXPECT['v13'], 'inputs': PC['layerInputs']['13'],
                           'changedVsV12': PC['v13ChangedVsV12'], 'addedVsV12': PC['v13AddedVsV12'], 'removedVsV12': PC['v13RemovedVsV12'],
                           'predecessorLayersByteIdenticalToSource44': PC['priorLayersByteEqualToSource44'], 'changedNormativeDeltaDocumentsNotBound': UNBOUND_NORMATIVE,
                           'adv4401BindingState': PC['adv4401']},
    'predecessorsPreserved': {'source44Review': {'path': V44PATH, 'sha256': sha(V44PATH), 'expected': EXPECT['review44'], 'verdict': V44['verdict'], 'modifiedByThisReview': False, 'conclusionInherited': False}},
    'readScope': {
        'rule': 'Whole-file claims only for fresh45Read (every line read this charter) and inheritedUnchanged44Read (counted as completely read by this origin\'s completed source44 review and byte-identical now; not re-read). complete44ReadPlusComplete45Diff is a complete predecessor read plus the exact diff. Delta reads, range reads, structural comparisons, evidence reads and search-only sightings are not whole-file reads of source45 bytes. Hashes recomputed at build time.',
        'fresh45Read': fresh, 'fresh45RangeRead': ranged, 'deltaReads': delta_reads, 'deltaFilesStructurallyCompared': structural_delta, 'complete44ReadPlusComplete45Diff': via_diff,
        'inheritedUnchanged44Read': inherited, 'changedPriorReadNotReread': changed_not, 'prior44RangeReadOnly': prior_ranges, 'searchOnlySightings': SEARCH_ONLY,
        'evidenceReads': evidence_reads, 'deltaFilesWithoutReadEntry': uncovered,
        'counts': {'fresh45Read': len(fresh), 'fresh45RangeRead': len(ranged), 'deltaReads': len(delta_reads), 'deltaFilesStructurallyCompared': len(structural_delta),
                   'complete44ReadPlusComplete45Diff': len(via_diff), 'inheritedUnchanged44Read': len(inherited), 'changedPriorReadNotReread': len(changed_not),
                   'evidenceReads': len(evidence_reads), 'searchOnlySightings': len(SEARCH_ONLY)},
        'ledger': {'path': 'receipts/read-ledger.jsonl', 'sha256': sha(LEDGER), 'rows': len(ledger)},
    },
    'newMustIssues': MUST, 'newShouldIssues': SHOULD, 'advisories': ADVISORIES, 'observations': OBSERVATIONS,
    'priorFindingDispositions': PRIOR_DISPOSITIONS, 'itemDispositions': ITEMS,
    'probes': PROBES,
    'commandReceipts': {'referenceGroups': group_rows, 'referenceGroupsPassed': groups_ok, 'evaluator3Children': children, 'evaluator3ChildrenAllExit0': children_ok,
                        'foundationChecks': foundation_checks, 'nativeStdout': NATIVE_STDOUT, 'planning': {k: P[k]['exitCode'] for k in ('check_implementation_planning', 'check_repository_file_inventory')},
                        'planningStdout': {k: P[k]['stdout'].strip() for k in ('check_implementation_planning', 'check_repository_file_inventory')},
                        'planningCounts': {k: v for k, v in PC.items() if k != 'planningSourcesHistory'}, 'planningOk': planning_ok,
                        'referenceComparison': {'receipt': 'receipts/reference-comparison.json', 'sha256': sha(REC + '/reference-comparison.json'),
                                                'groups': {k: {kk: vv for kk, vv in v.items() if not kk.startswith('stdout') or kk.startswith('stdoutFile') or kk.startswith('stdoutSha') or kk == 'stdoutEqualHistoricalMine44'} for k, v in RC['groups'].items()},
                                                'childrenEqualRoot': RC['childrenEqualRoot'], 'childrenNotEqualRoot': RC['childrenNotEqualRoot'], 'childrenDifferingFromHistoricalMine44': RC['childrenDifferingFromHistoricalMine44'], 'ok': reference_ok},
                        'copyVerificationFinal': {'receipt': 'receipts/copy-verification-final.json', 'sha256': sha(REC + '/copy-verification-final.json'), 'result': {k: v['verified'] for k, v in COPYVER.items()}}},
    'childCompletion': {'referenceGroups': [(r['name'], r['exitCode'], r['timedOut']) for r in group_rows], 'evaluator3Children': len(children),
                        'probeRuns': {p['id']: p['execution']['exitCode'] for p in PROBES if p.get('execution')}, 'packageToolRuns': {k: v and v['exitCode'] for k, v in PKG_RUNS.items()},
                        'backgroundProcessesOutstanding': 0},
    'packageAssessment': PACKAGE, 'rootAndPackageEvidence': EVIDENCE, 'mapSources': MAP,
    'planningLayer': {'normativeInputsV13Sha256': PC['layerSha256']['13'], 'inputs': PC['layerInputs']['13'], 'paths': PC['inventoryPaths'], 'packages': PC['inventoryPackages'],
                      'mappings': PC['coverageMappings'], 'mappingsSource44': PC['coverageMappingsSource44'], 'reportFeatures': PC['coverageGroups']['reportFeatures'],
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


def cell(v):
    return str(v).replace('|', '\\|').replace('\n', ' ')


L = []
A = L.append
A('# Independent design review — source45 (whole-design successor)\n')
A('**Reviewer:** %s  ' % review['reviewer'])
A('**Standing:** %s\n' % review['standing'])
A('## Verdict: %s\n' % verdict)
A(basis_text + '\n')
A('## Subject\n')
A('| Item | Value |\n|---|---|')
for k in ('subjectManifestSha256', 'liveManifestSha256Measured', 'verifiedManifest', 'subjectFileCount', 'subjectTotalBytes', 'subjectArchiveSha256', 'archiveSha256Measured'):
    A('| %s | `%s` |' % (k, review[k]))
A('| parent44 | `%s` declared by 45: %s; snapshot verified: %s (%s members); archive `%s` |' % (review['parent44']['manifestSha256'], review['parent44']['declaredBy45'], review['parent44']['snapshotVerified'], review['parent44']['members'], EXPECT['archive44']))
A('| delta 44to45 | %s changed, %s added, %s removed |' % (DCOUNTS['changed'], DCOUNTS['added'], DCOUNTS['removed']))
A('| owned source pins | %d entries; all match: %s; %d changed pins |' % (PINS['totalPinEntries'], PINS['allPinsMatch'], len(PINS['changedPinUnion'])))
A('| planning input layer v13 | `%s` (%d inputs; v8-v12 byte-identical to source44) |' % (PC['layerSha256']['13'], PC['layerInputs']['13']))
A('')
A('Changed files: ' + ', '.join('`%s`' % p for p in review['delta44to45']['changedPaths']) + '\n')
A('Added files: ' + ', '.join('`%s`' % p for p in review['delta44to45']['addedPaths']) + '\n')
A('## Issues\n')
A('No MUST issue. No SHOULD issue. No new advisory. ADV42-01 and ADV44-01 are retained as non-blocking advisories.\n')
for a in ADVISORIES:
    A('### %s (%s, %s): %s\n' % (a['id'], a['severity'], a['origin'], a['title']))
    A('**Current standing.** ' + a['currentStanding'] + '\n')
    A('**Standing assessment.** ' + a['standingAssessment'] + '\n')
    A(md_list(a['selectors']) + '\n')
    A('**Detail.** ' + a['detail'] + '\n')
    A('**Consequence.** ' + a['consequence'] + '\n')
    A('**Disposition.** ' + a['disposition'] + '\n')
    A('**Measured on source45**\n\n```json\n' + json.dumps(a['measuredOnSource45'], indent=1, default=str)[:4000] + '\n```\n')
A('## Observations (not defects)\n')
for o in OBSERVATIONS:
    A('- **%s** %s (%s)' % (o['id'], o['text'], o['receipt']))
A('')
A('## Current dispositions of prior findings, advisories and observations\n')
A('| id | current disposition | basis | reasoning |\n|---|---|---|---|')
for d in PRIOR_DISPOSITIONS:
    A('| %s | %s | %s | %s |' % (d['id'], cell(d['currentDisposition']), d.get('basis', '-'), cell(d['reasoning'])))
A('')
A('## Item dispositions\n')
for it in ITEMS:
    A('### %s: %s\n' % (it['id'], it['disposition']))
    A(it['assessment'] + '\n')
    if it.get('unchanged44Items'):
        A('| source44 item | source44 disposition | unchanged basis on source45 |\n|---|---|---|')
        for u in it['unchanged44Items']:
            A('| %s | %s | %s |' % (u['id'], cell(u['source44Disposition']), cell(u['basis'])))
        A('')
    if it.get('scopeBasis'):
        A('| scope | basis | current source45 evidence | unchanged-44 basis |\n|---|---|---|---|')
        for sb in it['scopeBasis']:
            A('| %s | %s | %s | %s |' % (cell(sb['scope']), cell(sb['basis']), cell(sb['current45']), cell(sb['unchanged44'] or '-')))
        A('')
        A('| ported probe | rows | same case set as source44 | observations differing from source44 |\n|---|---|---|---|')
        for k, v in it['portedProbes'].items():
            A('| %s | %d | %s | %s |' % (k, v['rows'], v['sameCaseSetAsSource44'], v['observedDifferFromSource44'] or 'none'))
        A('')
A('## Package v22\n')
A(PACKAGE['result'] + '\n')
A('Measured RunIds (17): ' + ', '.join('`%s`' % r for r in PACKAGE['measuredRunIds']) + '\n')
A(md_list(PACKAGE['limits']) + '\n')
A('| control | owner admission | semantic admission | reason |\n|---|---|---|---|')
for c in PACKAGE['normalizationMapControls']:
    A('| %s | %s | %s | %s |' % (c['name'], c['ownerAdmission'], c['semanticAdmission'], cell(c['reason'])))
A('')
A('## Commands and probes\n')
A('| group | exit | seconds | stdout sha256 | equal root | equal codex | equal own source44 |\n|---|---|---|---|---|---|---|')
for r in group_rows:
    g = RC['groups'][r['name']]
    A('| %s | %s | %s | `%s` | %s | %s | %s |' % (r['name'], r['exitCode'], r['seconds'], r['stdoutSha256'], g['stdoutFileEqualRoot'], g['stdoutFileEqualCodex'], g['stdoutEqualHistoricalMine44']))
A('\nevaluator3 children: %d, all exit 0: %s; query-projection checks %s (failed %s); execution-inputs cases %s; enumeration cases %s. Native: %s. Planning: %s. Planning counts ok: %s.\n'
  % (len(children), children_ok, children['query-projection'].get('checksCount'), children['query-projection'].get('failedCount'), children['execution-inputs'].get('casesCount'),
     children['enumeration'].get('casesCount'), NATIVE_STDOUT, review['commandReceipts']['planningStdout'], planning_ok))
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
A('Delta files compared structurally: %s.\n' % '; '.join('%s (%s)' % (e['path'], e['standing']) for e in structural_delta))
A('Fresh whole-file reads:\n\n' + (md_list('%s (%s lines, sha256 `%s`)' % (e['path'], e['lines'], e['sha256']) for e in fresh) or '- none') + '\n')
A('Range reads:\n\n' + md_list('%s: %s (sha256 `%s`)' % (e['path'], ', '.join(e['ranges']), e['sha256']) for e in ranged) + '\n')
A('Complete diff reads:\n\n' + md_list('%s (%s; diff `%s`)' % (e['path'], e['readClass'], e['diffSha256']) for e in delta_reads) + '\n')
A('Evidence reads:\n\n' + md_list('%s: %s' % (e['path'], ', '.join(e['ranges'])) for e in evidence_reads) + '\n')
A('Search-only sightings (not reads):\n\n' + md_list('%s: %s — %s' % (x['path'], x['lines'], x['standing']) for x in SEARCH_ONLY) + '\n')
A('Inherited unchanged source44 whole-file reads (not re-read): %d files; complete source44 read plus complete 44->45 diff: %d (%s); listed in review.json.\n' % (len(inherited), len(via_diff), ', '.join(e['path'] for e in via_diff)))
A('## TCB-SCOPE-01 (assessed once)\n')
A('**Assumption.** %s\n\n**Consequence.** %s\n\n**Dependent rows (%d).** %s\n' % (TCB['assumption'], TCB['consequence'], TCB['dependentRowCount'], ', '.join(TCB['dependentRows'])))
A('**Current assessment.** ' + TCB['currentAssessment'] + '\n')
A(md_list(TCB['substantiveCurrentAssessment']) + '\n')
A('**Position:** %s. **Standing:** %s. **Adjudication owner:** %s\n' % (TCB['reviewerPosition'], TCB['standing'], TCB['adjudicationOwner']))
A('## Disposition rows (%d)\n' % len(ALL_ROWS))
A('All rows: appliedByThisReview=false, finalApplicationOutcomeGranted=false. No grade is assigned; scoped owner rows are routing only.\n')
A('**Basis rule.** %s Counts: %s.\n' % (BASIS_RULE, json.dumps(review['dispositionRowBasisCounts'])))
A('| id | prior44 | disposition | basis | current assessment | owner | consequence |\n|---|---|---|---|---|---|---|')
for r in ALL_ROWS:
    A('| %s | %s | %s | %s | %s | %s | %s |' % (r['id'], cell(r['prior44Disposition']), cell(r['disposition']), r['assessmentBasis'], cell(r['currentAssessment']), cell(r['currentOwner']), cell(r['consequence'])))
A('\nThe quoted source44 basis and governing owners of every unchanged-44-basis row are in review.json (`unchanged44Basis`, `unchanged44GoverningOwners`).\n')
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
