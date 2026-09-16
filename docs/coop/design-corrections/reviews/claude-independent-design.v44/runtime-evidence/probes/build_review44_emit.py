# Executed by build_review44.py in its own globals (exec) after the findings and rows parts. Assembles review.json, checks
# gaps, decides the verdict, renders review.md. Writes only RT/review.json and RT/review.md.

ALL_ROWS = F_ROWS + RES_ROWS + AR_ROWS + FW_ROWS + DR_ROWS + SCOPED_ROWS
ids = [r['id'] for r in ALL_ROWS]
if len(ALL_ROWS) != 107 or len(set(ids)) != 107 or set(ids) != set(V43ROWS):
    GAPS.append('disposition rows: %d (unique %d); id set equals source43: %s' % (len(ALL_ROWS), len(set(ids)), set(ids) == set(V43ROWS)))
for r in ALL_ROWS:
    if r['appliedByThisReview'] is not False or r['finalApplicationOutcomeGranted'] is not False:
        GAPS.append('row flag not false: ' + r['id'])
    if r['assessmentBasis'] not in (N, I) or not r['currentAssessment'] or not r['currentOwner'] or not r['consequence']:
        GAPS.append('row incomplete: ' + r['id'])
    if r['assessmentBasis'] == I and not r['unchanged43Basis']:
        GAPS.append('unchanged basis without quoted source43 basis: ' + r['id'])
if len(TCB['dependentRows']) != 13 or TCB['dependentRowCount'] != 13:
    GAPS.append('TCB dependent count is not 13')
nonF = [r['currentAssessment'] for r in ALL_ROWS if not r['id'].startswith('F-')]
if len(set(nonF)) != len(nonF):
    GAPS.append('duplicate current assessment texts among non-F rows')
prior_same = [r['id'] for r in ALL_ROWS if not r['id'].startswith('F-') and r['currentAssessment'] == V43ROWS[r['id']]['currentAssessment']]
if prior_same:
    GAPS.append('rows whose text is copied verbatim from source43: %s' % prior_same)

scope_complete = (not GAPS and groups_ok and children_ok and planning_ok and pkg_ok and verified_manifest and parent43_ok and pins_ok and reference_ok
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
              'Provider wire: TypeScriptHelloV2/TypeScriptHelloAckV2 keep every delivery.v2 HelloV1/HelloAckV1 member, and Rust HelloV3/HelloAckV3 keep every rust v2 HelloV2/HelloAckV2 member and every registered member. The exact 10- and 32-member limit maps, the raw-byte contract digest, the descriptor and Plan identity joins, the sorted signed-row tokens and the identityVersions echoes are source-bound and were discriminated field by field. Supersession of the registered definitions is narrow and named. '
              'Historical TS FactBatchV1 (commitment recomputed independently) and Rust FactBatchV2 share one candidate CBOR projection with negotiated V3, and a scoped occupancy omission validates no historical batch. '
              'Provider startup: the OpenUniverse/UniverseAccepted identity fields, per-language native-context and repository-resolution applicability, host-derived modes including empty custody, NativeContextVerified, and the pre-Analyze native-context-mismatch payload (phase, correlation, clean zero-exit/EOF versus faults) are consistent across owners, as are its host-derived provider-unavailable coverage, the Coverage/CoverageV3 frame selectors with their entry and wrapper schemas, and the inserted cancellation interval. rustCommitHash needs no join beyond its 64-hex chain. '
              'The reference scope is disclosed: trusted host inputs, abstract custody/Analyze events and unrecomputed stream commitments (OBS44-05..07). New advisory ADV44-01 is non-blocking: layer v12 binds the TS order table but not the changed P3 table. ADV42-01 is retained on re-measured values, and S40-01 and ADV40-01 remain resolved. '
              'Also completed on verified copies: subject, archive, all 12,919 members, parent43, the 24/6/0 delta, all pins, six pinned groups, 17 children, planning and inventory, package v21 with RunIds measured unchanged, the ten scope-preservation probes and final copy re-verification. '
              'Source-level acceptance only: no blind reconstruction, application, readiness, implementation authorization or product qualification is granted.')
review = {
    'schema': 'opensip.independent-design-review.source44.v1',
    'reviewer': 'Claude (independent design review origin %s, continuing after the completed source43 review; source44 charter; authored none of the reviewed bytes)' % ORIGIN,
    'standing': 'Source44 whole-design successor review. Not fresh-origin independence, blind reconstruction, final application acceptance, implementation authorization or product qualification.',
    'verdict': verdict, 'verdictBasis': basis_text,
    'subjectManifestPath': LIVE44, 'subjectManifestSha256': EXPECT['manifest44'], 'liveManifestSha256Measured': live44, 'verifiedManifest': verified_manifest,
    'subjectSnapshot': S44, 'subjectFileCount': SV['counts44']['fileCount'], 'subjectTotalBytes': SV['counts44']['totalBytes'],
    'subjectArchivePath': ARCHIVE44, 'subjectArchiveSha256': EXPECT['archive44'], 'archiveSha256Measured': archive44, 'archiveVerification': {k: summ(v) for k, v in ARCH.items()},
    'parent43': {'manifestSha256': SV['manifest43']['sha256'], 'declaredBy44': SV['parentChain']['44declares43'], 'snapshotVerified': SV['snapshot43']['verified'],
                 'members': SV['snapshot43']['members'], 'archiveSha256': EXPECT['archive43'], 'unchangedAndVerified': parent43_ok},
    'delta43to44': dict(DCOUNTS, changedPaths=[r['path'] for r in DELTA['changed']], addedPaths=[r['path'] for r in DELTA['added']], removedPaths=[r['path'] for r in DELTA['removed']],
                        diffs=DIFFSUM['43to44']),
    'ownedSourcePins': {'receipt': 'receipts/source-pins44.json', 'sha256': sha(REC + '/source-pins44.json'), 'allPinsMatch': PINS['allPinsMatch'], 'changedPinUnion': PINS['changedPinUnion'],
                        'addedPinUnion': PINS['addedPinUnion'], 'deltaFilesPinnedByNoLedger': PINS['deltaFilesPinnedByNoLedger'],
                        'ledgers': {k: {x: v[x] for x in ('ledgerSha256', 'entries', 'mismatchedAgainstManifest', 'changedPinsVs43', 'addedVs43', 'removedVs43')} for k, v in PINS['ledgers'].items()}, 'verified': pins_ok},
    'planningInputLayer': {'path': ARCHD + 'implementation-normative-inputs.v12.json', 'sha256': PC['layerSha256']['12'], 'expected': EXPECT['v12'], 'inputs': PC['layerInputs']['12'],
                           'addedVsV11': PC['v12AddedVsV11'], 'changedVsV11': PC['v12ChangedVsV11'], 'removedVsV11': PC['v12RemovedVsV11'],
                           'predecessorLayersByteIdenticalToSource43': PC['priorLayersByteEqualToSource43'], 'changedNormativeDeltaDocumentsNotBound': UNBOUND_NORMATIVE, 'advisory': 'ADV44-01'},
    'predecessorsPreserved': {'source43Review': {'path': V43PATH, 'sha256': sha(V43PATH), 'expected': EXPECT['review43'], 'verdict': V43['verdict'], 'modifiedByThisReview': False, 'conclusionInherited': False}},
    'readScope': {
        'rule': 'Whole-file claims only for fresh44Read (every line read this charter) and inheritedUnchanged43Read (counted as completely read by this origin\'s completed source43 review and byte-identical now; not re-read). complete43ReadPlusComplete44Diff is a complete predecessor read plus the exact diff. Delta reads, range reads, evidence reads and search-only sightings are not whole-file reads of source44 bytes. Hashes recomputed at build time.',
        'fresh44Read': fresh, 'fresh44RangeRead': ranged, 'deltaReads': delta_reads, 'complete43ReadPlusComplete44Diff': via_diff, 'inheritedUnchanged43Read': inherited,
        'changedPriorReadNotReread': changed_not, 'prior43RangeReadOnly': prior_ranges, 'searchOnlySightings': SEARCH_ONLY,
        'evidenceReads': evidence_reads, 'deltaFilesWithoutReadEntry': uncovered, 'deltaFilesRangeReadOnly': range_only_delta,
        'counts': {'fresh44Read': len(fresh), 'fresh44RangeRead': len(ranged), 'deltaReads': len(delta_reads), 'deltaFilesRangeReadOnly': len(range_only_delta),
                   'complete43ReadPlusComplete44Diff': len(via_diff),
                   'inheritedUnchanged43Read': len(inherited), 'changedPriorReadNotReread': len(changed_not), 'evidenceReads': len(evidence_reads), 'searchOnlySightings': len(SEARCH_ONLY)},
        'ledger': {'path': 'receipts/read-ledger.jsonl', 'sha256': sha(LEDGER), 'rows': len(ledger)},
    },
    'newMustIssues': MUST, 'newShouldIssues': SHOULD, 'advisories': ADVISORIES, 'observations': OBSERVATIONS,
    'priorFindingDispositions': PRIOR_DISPOSITIONS, 'itemDispositions': ITEMS,
    'probes': PROBES,
    'commandReceipts': {'referenceGroups': group_rows, 'referenceGroupsPassed': groups_ok, 'evaluator3Children': children, 'evaluator3ChildrenAllExit0': children_ok,
                        'foundationChecks': foundation_checks, 'nativeStdout': NATIVE_STDOUT, 'planning': {k: P[k]['exitCode'] for k in ('check_implementation_planning', 'check_repository_file_inventory')},
                        'planningStdout': {k: P[k]['stdout'].strip() for k in ('check_implementation_planning', 'check_repository_file_inventory')},
                        'planningCounts': PC, 'planningOk': planning_ok,
                        'referenceComparison': {'receipt': 'receipts/reference-comparison.json', 'sha256': sha(REC + '/reference-comparison.json'), 'groups': RC['groups'],
                                                'childrenEqualRoot': RC['childrenEqualRoot'], 'childrenDifferingFromHistoricalMine43': RC['childrenDifferingFromHistoricalMine43'],
                                                'groupDifferencesFromOwnSource43': GROUP_DIFF_43, 'ok': reference_ok},
                        'copyVerificationFinal': {'receipt': 'receipts/copy-verification-final.json', 'sha256': sha(REC + '/copy-verification-final.json'), 'result': {k: v['verified'] for k, v in COPYVER.items()}}},
    'childCompletion': {'referenceGroups': [(r['name'], r['exitCode'], r['timedOut']) for r in group_rows], 'evaluator3Children': len(children),
                        'probeRuns': {p['id']: p['execution']['exitCode'] for p in PROBES if p.get('execution')}, 'packageToolRuns': {k: v and v['exitCode'] for k, v in PKG_RUNS.items()},
                        'backgroundProcessesOutstanding': 0},
    'packageAssessment': PACKAGE, 'rootAndAuthorEvidence': EVIDENCE, 'mapSources': MAP,
    'planningLayer': {'normativeInputsV12Sha256': PC['layerSha256']['12'], 'inputs': PC['layerInputs']['12'], 'paths': PC['inventoryPaths'], 'packages': PC['inventoryPackages'],
                      'mappings': PC['coverageMappings'], 'mappingsSource43': PC['coverageMappingsSource43'], 'reportFeatures': PC['coverageGroups']['reportFeatures'],
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
A('# Independent design review — source44 (whole-design successor)\n')
A('**Reviewer:** %s  ' % review['reviewer'])
A('**Standing:** %s\n' % review['standing'])
A('## Verdict: %s\n' % verdict)
A(basis_text + '\n')
A('## Subject\n')
A('| Item | Value |\n|---|---|')
for k in ('subjectManifestSha256', 'liveManifestSha256Measured', 'verifiedManifest', 'subjectFileCount', 'subjectTotalBytes', 'subjectArchiveSha256', 'archiveSha256Measured'):
    A('| %s | `%s` |' % (k, review[k]))
A('| parent43 | `%s` declared by 44: %s; snapshot verified: %s (%s members); archive `%s` |' % (review['parent43']['manifestSha256'], review['parent43']['declaredBy44'], review['parent43']['snapshotVerified'], review['parent43']['members'], EXPECT['archive43']))
A('| delta 43to44 | %s changed, %s added, %s removed |' % (DCOUNTS['changed'], DCOUNTS['added'], DCOUNTS['removed']))
A('| owned source pins | all match: %s; %d changed and %d added pins |' % (PINS['allPinsMatch'], len(PINS['changedPinUnion']), len(PINS['addedPinUnion'])))
A('| planning input layer v12 | `%s` (%d inputs; v8-v11 byte-identical to source43) |' % (PC['layerSha256']['12'], PC['layerInputs']['12']))
A('')
A('Changed files: ' + ', '.join('`%s`' % p for p in review['delta43to44']['changedPaths']) + '\n')
A('Added files: ' + ', '.join('`%s`' % p for p in review['delta43to44']['addedPaths']) + '\n')
A('## Issues\n')
A('No MUST issue. No SHOULD issue. One new non-blocking advisory (ADV44-01); ADV42-01 retained.\n')
for a in ADVISORIES:
    A('### %s (%s, %s): %s\n' % (a['id'], a['severity'], a['origin'], a['title']))
    if a.get('currentStanding'):
        A('**Current standing.** ' + a['currentStanding'] + '\n')
    if a.get('standingAssessment'):
        A('**Standing assessment.** ' + a['standingAssessment'] + '\n')
    A(md_list(a['selectors']) + '\n')
    A('**Detail.** ' + a['detail'] + '\n')
    A('**Consequence.** ' + a['consequence'] + '\n')
    A('**Disposition.** ' + a['disposition'] + '\n')
    meas = a.get('measuredOnSource44') or a.get('measured')
    A('**Measured on source44**\n\n```json\n' + json.dumps(meas, indent=1, default=str)[:4000] + '\n```\n')
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
    if it.get('scopeBasis'):
        A('| scope | basis | current source44 evidence | unchanged-43 basis |\n|---|---|---|---|')
        for sb in it['scopeBasis']:
            A('| %s | %s | %s | %s |' % (cell(sb['scope']), cell(sb['basis']), cell(sb['current44']), cell(sb['unchanged43'] or '-')))
        A('')
        A('Unchanged-43 items standing on byte-identical owners: ' + ', '.join('%s (%s)' % (u['id'], u['source43Disposition']) for u in it['unchanged43Items']) + '\n')
        A('| ported probe | rows | same case set as source43 | observations differing from source43 |\n|---|---|---|---|')
        for k, v in it['portedProbes'].items():
            A('| %s | %d | %s | %s |' % (k, v['rows'], v['sameCaseSetAsSource43'], v['observedDifferFromSource43'] or 'none'))
        A('')
A('## Package v21\n')
A(PACKAGE['result'] + '\n')
A('Measured RunIds (17): ' + ', '.join('`%s`' % r for r in PACKAGE['measuredRunIds']) + '\n')
A(md_list(PACKAGE['limits']) + '\n')
A('| control | owner admission | semantic admission | reason |\n|---|---|---|---|')
for c in PACKAGE['normalizationMapControls']:
    A('| %s | %s | %s | %s |' % (c['name'], c['ownerAdmission'], c['semanticAdmission'], cell(c['reason'])))
A('')
A('## Commands and probes\n')
A('| group | exit | seconds | stdout sha256 | equal root | equal codex | equal own source43 |\n|---|---|---|---|---|---|---|')
for r in group_rows:
    g = RC['groups'][r['name']]
    A('| %s | %s | %s | `%s` | %s | %s | %s |' % (r['name'], r['exitCode'], r['seconds'], r['stdoutSha256'], g['stdoutFileEqualRoot'], g['stdoutFileEqualCodex'],
                                                g['stdoutEqualHistoricalMine43'] or GROUP_DIFF_43.get(r['name'])))
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
A('Delta files read by named ranges only (complete diff not read): %s.\n' % ('; '.join('%s (%s)' % (e['path'], e['standing']) for e in range_only_delta) or 'none'))
A('Fresh whole-file reads:\n\n' + md_list('%s (%s lines, sha256 `%s`)' % (e['path'], e['lines'], e['sha256']) for e in fresh) + '\n')
A('Range reads:\n\n' + md_list('%s: %s (sha256 `%s`)' % (e['path'], ', '.join(e['ranges']), e['sha256']) for e in ranged) + '\n')
A('Complete diff reads:\n\n' + md_list('%s (%s; diff `%s`)' % (e['path'], e['readClass'], e['diffSha256']) for e in delta_reads) + '\n')
A('Evidence reads:\n\n' + md_list('%s: %s' % (e['path'], ', '.join(e['ranges'])) for e in evidence_reads) + '\n')
A('Search-only sightings (not reads):\n\n' + md_list('%s: %s — %s' % (x['path'], x['lines'], x['standing']) for x in SEARCH_ONLY) + '\n')
A('Inherited unchanged source43 whole-file reads (not re-read): %d files; complete source43 read plus complete 43->44 diff: %d; listed in review.json.\n' % (len(inherited), len(via_diff)))
A('## TCB-SCOPE-01 (assessed once)\n')
A('**Assumption.** %s\n\n**Consequence.** %s\n\n**Dependent rows (%d).** %s\n' % (TCB['assumption'], TCB['consequence'], TCB['dependentRowCount'], ', '.join(TCB['dependentRows'])))
A('**Current assessment.** ' + TCB['currentAssessment'] + '\n')
A(md_list(TCB['substantiveCurrentAssessment']) + '\n')
A('**Position:** %s. **Standing:** %s. **Adjudication owner:** %s\n' % (TCB['reviewerPosition'], TCB['standing'], TCB['adjudicationOwner']))
A('## Disposition rows (%d)\n' % len(ALL_ROWS))
A('All rows: appliedByThisReview=false, finalApplicationOutcomeGranted=false. No grade is assigned; scoped owner rows are routing only.\n')
A('**Basis rule.** %s Counts: %s.\n' % (BASIS_RULE, json.dumps(review['dispositionRowBasisCounts'])))
A('| id | prior43 | disposition | basis | current assessment | owner | consequence |\n|---|---|---|---|---|---|---|')
for r in ALL_ROWS:
    A('| %s | %s | %s | %s | %s | %s | %s |' % (r['id'], cell(r['prior43Disposition']), cell(r['disposition']), r['assessmentBasis'], cell(r['currentAssessment']), cell(r['currentOwner']), cell(r['consequence'])))
A('\nThe quoted source43 basis and governing owners of every unchanged-43-basis row are in review.json (`unchanged43Basis`, `unchanged43GoverningOwners`).\n')
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
