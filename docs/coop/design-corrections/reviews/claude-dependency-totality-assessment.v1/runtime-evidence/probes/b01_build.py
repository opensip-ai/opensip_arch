"""B01 — build review.json for the bounded dependency-totality + text-consistency assessment from receipts.
Asserts the claims it writes against the receipts that measured them."""
import hashlib, json, os, time

BASE = '/tmp/opensip-design-corrections/claude-dependency-totality-assessment.v1'
RC = os.path.join(BASE, 'receipts')
S35 = '/tmp/opensip-design-corrections/candidate-subject.v35'
FSU = '/tmp/opensip-design-corrections/dependency-scope-successor.v1/source/docs/coop/design-corrections/foundation'
MAN = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v35.json'
AUTH = '/tmp/opensip-design-corrections/claude-dependency-scope-author.v1'
V35 = '/tmp/opensip-design-corrections/claude-independent-design.v35'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
rc = lambda n: json.load(open(os.path.join(RC, n)))
p01, p02, p04 = rc('p01-dependency-totality.json'), rc('p02-history-runtime.json'), rc('p04-attestation-variant.json')
p03 = rc('p03-consumer-regression.json')
p05 = rc('p05-execution-inputs-diff.json')
assert all(v['bothExitZero'] for v in p03['comparison'].values())
nonidentical = [k for k, v in p03['comparison'].items() if not v['stdoutIdentical']]
assert nonidentical == ['check-execution-inputs.v1.py']
assert p05['p03DiffCount'] == 5 and all(d['path'].startswith('$.ownedHashes[') and d['path'].endswith('].path') for d in p05['p03JsonPathDiffs'])
assert p05['successorRunToRunIdentical'] and p05['remedyRunToRunIdentical']
assert all('/kit-successor/' in d['successor'] and '/kit-remedy/' in d['remedy'] for d in p05['p03JsonPathDiffs'])
man = json.load(open(MAN))
rows = {f['path']: f['sha256'] for f in man['files']}
CITED = ['docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md', 'docs/coop/design-corrections/foundation/atom_model.v1.py',
         'docs/coop/design-corrections/foundation/check-atoms.v1.py', 'docs/coop/design-corrections/foundation/evaluator-projection-registry.v1.json',
         'docs/coop/design-corrections/foundation/identity-model.v3.py', 'docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json',
         'docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md', 'docs/coop/design-corrections/workflows/schemas/imported-evidence.schema.json',
         'docs/coop/design-corrections/native/native_evidence_model.v2.py', 'docs/v2/contracts/product-v1/native-evidence.md',
         'docs/v2/contracts/product-v1/identity-and-evidence.md', 'docs/v2/contracts/product-v1/workflows-and-surfaces.md',
         'docs/coop/design-corrections/workflows/workflows_model.v1.py']
cited = {p: {'sha256': sha(os.path.join(S35, p)), 'equalsFrozen35Manifest': sha(os.path.join(S35, p)) == rows[p]} for p in CITED}
assert all(v['equalsFrozen35Manifest'] for v in cited.values())
assert sha(MAN) == 'eb45c22b88a428887672d729be6645abf7d4d175474313d0909c8307d7966c85'

deriv = {}
for fn, probe_dir in (('law-derivation-dependency.json', 'p01_dependency_totality'), ('law-derivation-history-runtime.json', 'p02_history_runtime')):
    started = json.load(open(os.path.join(RC, probe_dir, 'command.json')))['startedUtc']
    written = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime(os.path.getmtime(os.path.join(BASE, fn))))
    deriv[fn] = {'sha256': sha(os.path.join(BASE, fn)), 'writtenUtc': written, 'probeStartedUtc': started, 'writtenBeforeProbeRan': written <= started}
assert all(v['writtenBeforeProbeRan'] for v in deriv.values())

T1 = p01['T1-incomingTwoSubjectPrimary']
val = lambda case, m: T1[case][m].get('value')
assert p01['defectCases']['frozen35'] == p01['defectCases']['successor'] == ['partial-f-only', 'partial-g-scope-wrong-universe', 'partial-g-scope-without-coverage']
assert p01['defectCases']['remedy'] == [] and p01['remedyPartialEqualsNoDependencyAnswer'] and p01['outgoingUnchangedByRemedy']
assert all(v == 1 for v in p01['permutationsDistinct'].values())
assert p04['mismatchesByModel']['remedyA+B'] == [] and p04['emptyProgramUnchangedByB']
assert not p01['checkAtomsRegression']['remedy-on-successor-model']['failed'] and not p04['checkAtomsWithRemedyAplusB']['failed']
assert all(p02['R-checks'].values()) and p02['H2-pass'] and p02['H1-schemaAdmitsDuplicateAndNonUtf8OrderedPaths']['admitted']
dom = p01['T3-knownMatchDominance']['partial-f-only']

J = {
    'review': 'Bounded independent assessment: dependency totality in incoming/dependency views, plus two proposed text consistency corrections',
    'standing': ('Independent design-review origin ce3dec3b-0620-44ec-86e6-129b0e25cb1b after its completed source35 ACCEPT. Not source36 '
                 'acceptance, not application review. Grants no acceptance, readiness, qualification or application outcome.'),
    'inputs': {
        'frozen35Manifest': {'sha256': sha(MAN), 'citedOwnerFilesVerifiedAgainstManifest': cited},
        'myCompleteSource35Review': {'reviewJson': sha(V35 + '/review.json'), 'reviewMd': sha(V35 + '/review.md')},
        'authorRuntime': {'path': AUTH, 'reviewMd': sha(AUTH + '/review.md'), 'q3Probe': sha(AUTH + '/probes/q3_dependency_shapes.py'),
                          'standing': 'evidence read, not adopted; no author bytes edited'},
        'successorSource': {'path': FSU, 'atomModelSha256': p01['hashesBefore']['successorAtomModel'],
                            'matchesAuthorReportedDigest': p01['successorMatchesAuthorReport'], 'checkAtomsSha256': p01['hashesBefore']['successorCheckAtoms'],
                            'unchangedDuringMyProbes': p01['noTreeChanged'] and p04['successorUnchanged']},
        'notRead': 'no consumer material, root-blind record, or consumer-specific input/result'},
    'lawDerivedBeforeTesting': deriv,
}

J['dependencyTotality'] = {
    'decision': 'REQUIRED BY CURRENT LAW; the source35 answer is a REFERENCE DEFECT, with textual under-specification at the atom dependency sentence',
    'answer': ('Yes: for a same-kind DEPENDS_ON relation, dependency evidence must cover EVERY current source subject of the evaluated '
               'primary claim. Native RC-4 ties reachability to calls edges "over the same examined set"; atom section 4 forbids '
               '"fictional complete entries"; native sufficiency_v2 step 1 answers an absent relation required-relation-missing; '
               'identity section 3 makes complete "a claim about the examined partition". A folded complete calls entry backed by a '
               'strict subset of the primary scope\'s subjects is a complete claim for subjects nobody examined.'),
    'whyNotMerelyUnderSpecified': ('The one sentence that could be read loosely ("pair dep Coverage to current-source scopes containing '
                                   'those native ids") does not say "every", but no owner permits the loose reading and four owners '
                                   'exclude it. Outgoing already evaluates per subject; only whole-scope incoming and attestation views '
                                   'lose the per-subject obligation.'),
    'ownerCitations': json.load(open(os.path.join(BASE, 'law-derivation-dependency.json')))['ownerCitations'],
    'measured': {
        'standing': 'atom-api synthetic inputs (global atom-input admission + evaluate_atom); remedy candidates applied in-process only',
        'incomingTwoSubjectPrimary': {case: {m: T1[case][m].get('value') for m in ('frozen35', 'successor', 'remedy')} for case in T1},
        'defectCasesFrozen35AndSuccessor': p01['defectCases']['frozen35'],
        'remedyPartialEqualsNoDependencyAnswer': p01['remedyPartialEqualsNoDependencyAnswer'],
        'outgoingPerSubject': {l: {m: v.get('value') for m, v in p01['T2-outgoingPerSubject'][l].items()} for l in p01['T2-outgoingPerSubject']},
        'orderIndependence': p01['permutationsDistinct'],
        'knownMatchCountDominanceUnderPartial': {m: {k: v.get('value') for k, v in dom[m].items()} for m in dom},
        'knownFactMatched': p01['knownFactMatched'],
        'attestationView': {k: {m: v.get('value') for m, v in p04['cases'][k].items()} for k in p04['cases']},
        'emptySourceProgramCoverageRoute': {d: {m: v.get('value') for m, v in p01['T4-emptySourceProgram'][d].items()} for d in p01['T4-emptySourceProgram']},
        'differentKindWholeSourceClonesDeclares': {d: {m: v.get('value') for m, v in p01['T5-differentKindWholeSource'][d].items()} for d in p01['T5-differentKindWholeSource']},
        'checkAtomsRegression': {'successor95WithRemedyA': p01['checkAtomsRegression']['remedy-on-successor-model'],
                                 'successor95WithRemedyAplusB': p04['checkAtomsWithRemedyAplusB']},
        'authorObservationReproducedIndependently': val('partial-f-only', 'frozen35') == 'true' and val('partial-f-only', 'successor') == 'true'},
    'boundaries': {
        'lawfulDisjointPartitions': 'dependency partitions {f} and {g} satisfy totality: true on every model including both remedies, one result for every insertion order',
        'unlawfulOverlap': ('overlapping same-partitionKey dependency scopes {f},{f,g} are refused at close_run '
                            '(SUBJECT_SCOPE_PARTITION_OVERLAP; identity-and-evidence.md:1320-1332); at the atom API they answer true on every '
                            'model and carry no law'),
        'knownMatchCountDominance': ('unchanged: under the remedy a known incoming fact still makes exists true, none false, count<=0 false; '
                                     'only completeness-dependent count<=1 and all-covered become unknown'),
        'causeAndCitationSemantics': ('an uncovered subject makes the dependency occupy NO position (existing rule "a dependency contributing '
                                      'no selected Coverage occupies no position"): coverage-unknown at S plus required-relation-missing in '
                                      'nativeDeficiencies, and the partial dependency partitions are NOT folded or cited - the answer equals '
                                      'the no-dependency answer exactly (value, causes, nativeDeficiencies, coverageIds). No new cause token.'),
        'outgoing': 'already per subject (current subjects = the atom subject); unchanged by the remedy',
        'emptySource': ('CONSERVATIVE, UNDER-SPECIFIED: an empty primary partition closed by complete Coverage cannot satisfy a dependency on '
                        'any model, even with an explicit empty calls partition (containment pairs nothing); the attestation route with an '
                        'explicit empty calls partition does close (whole-source). Never unsound; the two routes disagree for empty programs.'),
        'differentKindWholeSource': ('GENUINELY UNDER-SPECIFIED: clones->declares takes every declares partition of (S, T); a declares '
                                     'partition for f only satisfies a clones claim over a file that also declares g, on every model. No owner '
                                     'states a population rule for different-kind dependencies, and RC-4 names reachability/calls only. Not '
                                     'claimed as a defect.'),
        'attestationWholeSourceSameKind': ('SAME DEFECT CLASS: a qualifying reachability attestation naming {f, g} plus calls for f only '
                                           'answers true on frozen35, the successor and same-kind remedy A; variant B (totality over the '
                                           'named scopes\' subjects, whole-source kept when that set is empty) answers unknown and leaves the '
                                           'empty-program attestation closure unchanged.')},
    'reachabilityByStanding': {
        'atomApi': 'DEMONSTRATED (p01, p04)',
        'nativeProducer': ('NOT EXCLUDED: admit_coverage_result_v3 admits one scope and one entry and cannot see a second relation '
                           '(relation-payload-schemas.v2.json coveragePartitionLaw.producerCannotDecideThis); a calls scope over {f} and a '
                           'reachability scope over {f, g} each admit on their own. RC-4 is a stated producer obligation, not a between-relation admission check.'),
        'closedRun': ('NOT EXCLUDED by close_run coverage laws: disjointness is per partitionKey, so different relations never overlap; the '
                      'omission half is owed only by file@enumerated (identity-model.v3.py:1027-1055 reads the coverageTotality row; '
                      'relation-payload-schemas.v2.json coverageTotalityLaw.whichRelationsHaveOne).'),
        'executionInputsCensus': ('PARTIALLY NEUTRALIZED: the calls cell\'s expected symbol census leaves g uncovered, so that account is '
                                  'incomplete and the cell partial (execution-inputs-contract.v1.md:188-201). A REQUIRED calls cell (the default '
                                  'profile requests every capability as required) emits requiredCellDeficiencies -> required-cell-unsatisfied -> '
                                  'Run indeterminate; the atom value inside proof is still wrong. An OPTIONAL calls cell carries no required deficiency.'),
        'closedEnumerationOrRetainedRun': 'NOT CONSTRUCTED; no full-Run counterexample is claimed'},
    'smallestRemedy': {
        'required': 'A (same-kind scope-paired totality) is the smallest correction that closes the reported defect.',
        'recommendedForCoherence': 'A + B (the attestation view applies the same principle over its named scopes\' subjects).',
        'modelA': p01['remedyFunctionSource'],
        'modelB': p04['variantBSource'],
        'contractText': ('Section 4 dependency paragraph: "Same sourceSubjectKind: pair dependency Coverage only to exact (relation, rung, S) '
                         'scopes that contain a current source subject, and those paired scopes must jointly contain EVERY current source '
                         'subject - the atom subject (outgoing), the evaluated source scope\'s subjects (incoming), or the subjects of the '
                         'scopes a qualifying attestation names (attestation view, when non-empty). Otherwise the dependency contributes no '
                         'position and sufficiency_v2 answers required-relation-missing (native RC-4: a derived relation is claimed over the '
                         'same examined set as its dependency)." Add section 9 cases: partial, partial-with-unpaired-scope, disjoint, attestation partial.'),
        'checker': ('check-atoms controls: partial dependency census unknown and equal to the no-dependency answer; lawful disjoint partitions '
                    'true; attestation partial unknown; known-match dominance under partial; outgoing unchanged.'),
        'crossOwnerEffects': {
            'changedOwnersIfAdopted': ['foundation/atom-evaluation-contract.v1.md', 'foundation/atom_model.v1.py', 'foundation/check-atoms.v1.py',
                                       'five pin ledgers (re-digest only)'],
            'unchangedOwners': 'no schema, registry, identity, native or execution-inputs change; no new cause token',
            'consumerCheckers': {
                'result': ('all 8 atom-model consumers exit 0 on the successor kit and on the remedy kit; 7 give byte-identical stdout; '
                           'check-execution-inputs.v1.py differs in exactly 5 JSON paths, all $.ownedHashes[*].path, which embed the absolute '
                           'disposable kit directory (kit-successor vs kit-remedy); the hash values are equal and each kit is identical run '
                           'to run. No consumer result changes.'),
                'comparison': p03['comparison'], 'executionInputsDiffPaths': [d['path'] for d in p05['p03JsonPathDiffs']],
                'runToRun': p05['reruns'], 'receipts': ['receipts/p03-consumer-regression.json', 'receipts/p05-execution-inputs-diff.json']},
            'retainedPackageRuns': 'package12 retained Runs contain only exists/file/source and none/clones/source atoms (my source35 review r05), so no reachability dependency view is replayed there',
            'composesWithAuthorSuccessor': 'applied on top of the successor _select_dep_coverages (mapped fallback already removed); 95/95 successor check-atoms still pass'},
        'optionalFollowUps': ['state an empty-examined-set rule so the Coverage route and the attestation route agree for empty programs',
                              'decide a population rule for different-kind whole-source dependencies (clones->declares)']},
}

H = p02
J['textConsistency'] = {
    'historySubjectOrder': {
        'decision': 'ROOT PROPOSAL ALIGNS EVERY OWNER; one precision owed',
        'contradiction': {'registryRow': H['registryHistorySubjectOrder'], 'sameRegistryOrdinalRow': H['registryOrdinalRow'],
                          'payloadSchema': H['schemaSubjects']},
        'measured': {'stockSchemaAdmitsDuplicatePathsInNonSortedProducerOrder': H['H1-schemaAdmitsDuplicateAndNonUtf8OrderedPaths']['admitted'],
                     'atomRetainsEveryOrdinal': {k: [v.get('value'), v.get('known')] for k, v in H['H2-atomRetainsEveryDuplicateOrdinalInProducerOrder'].items()},
                     'runtimeContrast': H['H3-runtimeContrastDuplicateKeyRefusal']},
        'correction': {'order': 'existing sequence (producer order)', 'uniqueKey': 'none (duplicate paths allowed)',
                       'duplicatePaths': 'every matching row is retained at its original ordinal (HISTORY_SUBJECT_SEQUENCE_ORDINALS)'},
        'precisionOwed': ('duplicates stay lawful payload rows for atom evaluation, but the repair targetSubjectProjection refuses when more than '
                          'one payload subject matches one target (imported-evidence.schema.json:970 step 5); the corrected row should say it '
                          'confers no merge or pick rule on any consumer. The "HistorySubject keyed by {path}" phrasing '
                          '(workflows-and-surfaces.md:469, imported-evidence.schema.json:963, workflows_model.v1.py:1094) names the match key, not uniqueness.'),
        'nativeProducerNote': 'native normalize_history emits unique UTF-8-sorted paths: one lawful producer order, consistent with "sequence"'},
    'importQuantifiersRuntimeProse': {
        'decision': 'ROOT PROPOSAL ALIGNS EXISTING OWNERS; one precision owed',
        'measured': H['R-checks'],
        'matrix': {obs: {f: {op: x.get('value') for op, x in d.items()} for f, d in H['R-runtimeMatrix'][obs].items()} for obs in H['R-runtimeMatrix']},
        'correction': ('atom section 6 Runtime: unfiltered exists is true on a consumable mapped row of EITHER polarity (observed-hit or '
                       'observable-unhit) - it asserts that an observed row exists, not that the subject executed; an observability filter '
                       'restricts polarity; unobservable and unmapped rows never enter R and never make exists true.'),
        'precisionOwed': ('a filter naming unobservable or unmapped is ADMITTED by the comparator enum (registry:970-984) but can never match, '
                          'because those rows become uncertain addresses with causes before filtering; their disclosure happens with or without '
                          'the filter, so registry observabilityFilter "may select disclosure" should read "cannot select them into R; their '
                          'disclosure is unconditional".')}}
J['limitations'] = [
    'All dependency and runtime/history measurements are atom-api synthetic inputs or stock schema; no native producer run, closed enumeration admission or retained Run was constructed.',
    'Remedies A and B are in-process candidates applied to loaded modules and, for p03, to disposable copies in this runtime; no source, author or frozen byte was written.',
    'The successor tree is mutable author work; its digests are recorded at probe time and were unchanged across my probes.',
    'This assessment does not repeat the 107 rows or integrated suites; the final frozen successor review carries that scope.']
J['probeErrorsPreserved'] = ['My first p01 run was issued through a shell pipeline with redirection that the permission mode refused; no probe ran. All probes were then run through probes/run.py, which retains command, stdout, stderr, exit and digests.',
                             'p02 contained a syntax slip on one record line and an assumed registry key path; both were fixed before p02 ever ran.',
                             'p05 framed the p03 stdout difference as either a remedy effect or run-to-run nondeterminism; it was neither. The checker embeds the absolute kit path in ownedHashes[*].path, so its "explained by nondeterminism" flag is null by construction; the JSON-path diff is the evidence relied on.']
J['grantsNothing'] = {'sourceAcceptance': False, 'applicationOutcome': False, 'readiness': False, 'qualification': False, 'commitOrPush': False}
J['receipts'] = {os.path.relpath(os.path.join(d, f), BASE): sha(os.path.join(d, f)) for d, _, fs in os.walk(RC) for f in sorted(fs)}
out = os.path.join(BASE, 'review.json')
json.dump(J, open(out, 'w'), indent=1, default=str)
print('p03 included:', bool(p03), '| review.json', sha(out))
