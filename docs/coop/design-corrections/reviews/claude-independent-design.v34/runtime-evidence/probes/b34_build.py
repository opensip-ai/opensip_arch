"""B34 — build the COMPLETE source34 review.json from the corrected 107-row baseline and my own receipts.

Rules: baseline row fields are never edited (they are history); every source34 fact is added in new
*On34 / *33to34 fields; owner arrays are derived from the two manifests; every current claim points at
a receipt produced in this runtime."""
import hashlib, json, os, re

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v34'
RC = os.path.join(BASE, 'receipts')
B2 = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v2'
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'


def sha(p):
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def rc(n):
    return json.load(open(os.path.join(RC, n)))


q00, q01, q02, q04 = rc('q00-custody.json'), rc('q01-diffs.json'), rc('q02-baseline.json'), rc('q04-rows.json')
q05, q06, q07, q08 = rc('q05-atomlaw.json'), rc('q06-followups.json'), rc('q07-suites.json'), rc('q08-package11.json')
q09, q10, q11, q12 = rc('q09-subject-universe.json'), rc('q10-reach-and-rows.json'), rc('q11-default-reach.json'), rc('q12-package-delta.json')
BL = json.load(open(os.path.join(B2, 'review.json')))
m34 = {f['path']: f['sha256'] for f in json.load(open(os.path.join(REV, 'candidate-subject.v34.json')))['files']}
m33 = {f['path']: f['sha256'] for f in json.load(open(os.path.join(REV, 'candidate-subject.v33.json')))['files']}
DELTA = sorted(c['path'] for c in q00['delta']['changed'])
MAPS = ('fDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions',
        'inheritedResidualDispositions', 'scopedReviewOwnerDispositions')
case05 = {c['id']: c for c in q05['cases']}
case06 = {c['id']: c for c in q06['cases']}
J = {}

# ------------------------------------------------------------------ identity, subject, custody
J['review'] = 'Independent design review of exact frozen consolidated product source34'
J['verdict'] = 'CHANGES_REQUIRED'
J['subjectManifestSha256'] = q00['manifestSha256']
J['verifiedManifest'] = bool(q00['manifestShaMatchesDeclared'] and q00['archiveEqualsManifest'] and q00['missing'] == 0
                             and q00['hashMismatches'] == 0 and q00['sizeMismatches'] == 0 and q00['extras'] == 0)
J['sessionIdentity'] = {
    'origin': 'ce3dec3b-0620-44ec-86e6-129b0e25cb1b',
    'role': 'independent reviewer; I have authored no source in this lineage',
    'notAForbiddenAcceptor': ['eaa8276c-dc65-4d26-8ca2-703b345698f9', '36a89be8-3442-4edb-90d8-a6fd959a437c',
                              '0aa529b3-0da1-44b1-b2b9-dbcd9f1bd206', '329a5132-ee66-4303-97a9-b9ebd1b7ffc0',
                              '919c766d-f2d0-4cfa-abaa-9d7425d9395f', '823bf66b-e92a-4789-ab81-63a1a9dc371d'],
    'notAForbiddenAcceptorStatement': 'I am none of the six excluded source-author origins.',
    'priorReviewsHistoricalUnchanged': [
        {'path': 'claude-independent-design.v33/review.json', 'sha256': sha('/tmp/opensip-design-corrections/claude-independent-design.v33/review.json'),
         'mdSha256': sha('/tmp/opensip-design-corrections/claude-independent-design.v33/review.md'), 'standing': 'ACCEPT on source33; historical'},
        {'path': 'claude-independent33-reconciliation.v1/review.json', 'sha256': sha('/tmp/opensip-design-corrections/claude-independent33-reconciliation.v1/review.json'),
         'mdSha256': sha('/tmp/opensip-design-corrections/claude-independent33-reconciliation.v1/review.md'), 'standing': 'record reconciliation; historical'},
        {'path': 'claude-independent33-reconciliation.v2/review.json', 'sha256': q02['baselineJsonSha256'],
         'mdSha256': q02['baselineMdSha256'], 'standing': 'record reconciliation; the corrected 107-row baseline of this review'}],
    'neitherAcceptsTheseBytes': True,
    'blindPolicy': ('No consumer output, runtime, report or root blind replay file was opened. No blind result or oracle is '
                    'an input to this review, and I claim no blind acceptance.')}
J['baselineRecord'] = {'path': 'claude-independent33-reconciliation.v2/review.json', 'sha256': q02['baselineJsonSha256'],
                       'expected': '89f4bd73ea4168286102c90d02020f2ee514a52e81280d186d05b78a3b6c4533',
                       'matches': q02['baselineMatches'], 'mdSha256': q02['baselineMdSha256'],
                       'standing': ('complete corrected 107-row baseline; every baseline row field is preserved verbatim as '
                                    'history, and every source34 fact is added in new fields')}
J['manifestVerification'] = {k: q00[k] for k in (
    'manifestSha256', 'manifestShaMatchesDeclared', 'archiveSha256', 'archiveShaMatchesDeclared', 'declaredFiles',
    'filesChecked', 'measuredTotalBytes', 'missing', 'hashMismatches', 'sizeMismatches', 'extras', 'archiveMemberRows',
    'archiveHashMismatches', 'archiveEqualsManifest', 'matchesDeclared12899', 'matchesDeclaredBytes736798408')}
J['manifestVerification']['parentManifestSha256'] = '1cf3db70d4b73b0c42f1393331e6a874ee26f7ddf67aa05c6ac15a5753069299'
J['manifestVerification']['parentIsMyReviewedSource33'] = q00['manifest33IsMyReviewedSource33'] and q00['parentNamesSource33ManifestDigest']
J['manifestVerification']['receipt'] = 'receipts/q00-custody.json'

sub = ['docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md',
       'docs/coop/design-corrections/foundation/atom_model.v1.py',
       'docs/coop/design-corrections/foundation/check-atoms.v1.py']
J['delta33to34'] = {
    'derivedByThisReview': True, 'derivedFrom': 'the frozen33 and frozen34 manifests (not prose, not root inventory)',
    'added': 0, 'removed': 0, 'changed': 9, 'touched': 9, 'netBytes': q00['delta']['netBytes'],
    'changedFiles': q00['delta']['changed'],
    'substantive': {p: {'plusLines': q01['files'][p]['plus'], 'minusLines': q01['files'][p]['minus'],
                        'lines33': q01['files'][p]['lines33'], 'lines34': q01['files'][p]['lines34']} for p in sub},
    'digestRebindingOnly': {p: {'plusLines': q01['files'][p]['plus'], 'minusLines': q01['files'][p]['minus'],
                                'nature': 'sha256 values of the three atom owners re-pinned; no other line changed'}
                            for p in DELTA if p not in sub},
    'contractSections': q01['contractSections'],
    'modelTopLevelChanged': q01['files']['docs/coop/design-corrections/foundation/atom_model.v1.py']['topLevel'],
    'checkerTopLevelChanged': q01['files']['docs/coop/design-corrections/foundation/check-atoms.v1.py']['topLevel'],
    'rootInventoryAgreement': q00['rootInventory'],
    'diffs': 'receipts/diffs/*.diff', 'receipt': 'receipts/q00-custody.json, receipts/q01-diffs.json'}

# ------------------------------------------------------------------ the changed atom law
g_admitted = [r for r in q05['G-table'] if r['admission'] == 'ADMIT']
g_refused = [(r['pairing'], r['attestation'], r['refusal']) for r in q05['G-table'] if r['admission'] != 'ADMIT']
qm = q05['G-qualificationMatrix']
J['sourceChangeAssessment'] = {'atomCompletenessLaw': {
    'status': ('Correct and well-controlled on every changed branch I tested, with ONE pre-existing design defect at the '
               'incoming boundary the change publishes (MUST-34-01) and one prose-precision advisory (A-12).'),
    'whatChanged': ('Only atom-evaluation-contract.v1.md section 4 changed (11 sections on both sides). It publishes: the '
                    'completeness-result/truth independence; ascending scope2/coverage2 selection order with dedup and '
                    'sort AFTER pairing; the optional atom universe projected to the required nullable deficiency '
                    'universe; the shared prelude P1/P2; outgoing steps 1-4; incoming no-further-early-return '
                    'accumulation with both cross-family routes; the three-case incoming search-accounting table; and '
                    'the deterministic dependency view with its field-by-field fold. The reference change is four '
                    'selection functions now returning ascending id order, with _coverages_for_current_source '
                    'deduplicating and sorting the combined paired list.'),
    'rootLaterBytes': {
        'record': 'reviews/root-final-atom-cause-source-completion.v1/change.json',
        'beforeSha256': '2d7c25948856bdfe6d21cebb1818b7c09461667173532257cf0f7d6267a2463c',
        'afterSha256': 'd7ef1336874fb1a70316cad3069725a6178c16c9bd9e39913516fc5c930c3417',
        'afterEqualsFrozen34Contract': m34['docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md'] == 'd7ef1336874fb1a70316cad3069725a6178c16c9bd9e39913516fc5c930c3417',
        'content': ('the search-accounting table and its surrounding sentences, the absent/admitted-nonqualifying '
                    'versus global-refusal sentence, the owed unknown-family wording and the fold tie wording'),
        'standing': ('root-authored; the author-v2 run did not review these bytes. I reviewed them as part of the frozen '
                     'contract and tested each against the branches (G1-G4, A5, E5b).')},
    'evidenceStanding': {
        'atom-api': q05['standingKey']['atom-api'], 'helper-unit': q05['standingKey']['helper-unit'],
        'retainedRuns': ('package11 retained Runs contain no incoming-endpoint atom and no IncomingSearchV1 record '
                         '(receipts/q08-package11.json anyRunReachesChangedAtomBranches), so NO retained Run exercises the '
                         'changed incoming or attestation branches. Nothing below is upgraded to a full-Run '
                         'counterexample or to qualification.'),
        'authorAndRootEvidence': ('The 81 check-atoms cases and root\'s five-case draft-review probe are author/root '
                                  'evidence. I read the root probe to learn the API and did not reuse its cases; every '
                                  'control below is my own.')},
    'branches': {
        'sharedPrelude': {'assessment': ('P1 then P2 run before the endpoint split exactly as published '
                                         '(atom_model.v1.py:1454-1465). P2 is shared and projects a null universe as an '
                                         'absent key; an owed unavailable binding of unknown family blocks incoming only.'),
                          'controls': {k: case05[k]['passed'] for k in ('A1-no-owed-binding-both-endpoints', 'A3-only-unavailable-same-family-binding',
                                                                         'A5-unknown-family-unavailable-blocks-incoming-only')}},
        'noOwedBindingVersusNoBindingAtSubjectUniverse': {
            'outgoing': 'correct: bindings exist but none at U -> selector-unbound, unknown (A2).',
            'incoming': 'DEFECT, see MUST-34-01: no analogue exists, so an unbound subject program can yield a proven negative.',
            'controls': {'A2': case05['A2-binding-only-at-other-same-family-universe']['passed'],
                         'A4 (measured)': q05['monotonicityObservation'], 'q09': q09['finding']}},
        'outgoingEarlyReturns': {'assessment': ('Each return ends completeness only. With two known facts at every stop: '
                                                'exists true, none false, count<=1 false, count<=2 UNKNOWN, all-covered '
                                                'unknown, completeness cause retained; without the stop count<=2 is true.'),
                                 'controls': {'B1': case05['B1-known-matches-dominate-each-early-stop-including-count-bound']['passed'],
                                              'B2': case05['B2-count-bound-discriminator-without-early-stop']['passed']}},
        'incomingAccumulation': {'assessment': ('No further early return; per (U, provider) accounting; a selected provider '
                                                'that emitted no scope cannot disappear; one failing universe hides nothing.'),
                                 'controls': {'F1': case05['F1-provider-B-owes-its-own-scope-account']['passed'],
                                              'F2': case05['F2-selected-provider-with-no-scope-cannot-disappear']['passed'],
                                              'F3': case05['F3-typed-source-universe-attribution-across-universes']['passed'],
                                              'H1': case05['H1-incoming-two-providers-attestation-list-and-map-orders']['passed']}},
        'causeChannelsAndTypedSourceUniverse': {
            'assessment': ('Three channels stay separate: AtomCauseV1 causes (endpoint causes carry the partition source '
                           'universe, prelude causes carry none), nativeDeficiencies (sufficiency strings), and the typed '
                           'nativeCause carrier on coverage-unknown. Observation, not a defect: target-export-unknown carries '
                           'the TARGET subject universe, while every search/population cause carries S.'),
            'controls': {'F3': case05['F3-typed-source-universe-attribution-across-universes']['passed'],
                         'E4': case05['E4-position-order-primary-before-dependency']['passed'],
                         'I1': case05['I1-nullable-universe-projection-claim']['passed']}},
        'dependencyTraversal': {'assessment': ('Only a calls partition paired to the current subject at the same (S,T) '
                                               'heals reachability; no partition, an unrelated-subject partition, an unpaired '
                                               'containing scope and an other-target partition all leave the dependency '
                                               'position empty, which native sufficiency_v2 answers required-relation-missing. '
                                               'Unchanged from source33 on every case.'),
                                'controls': {'D': case05['D-dependency-traversal-outgoing']['passed'],
                                             'unchangedFrom33': case05['D-dependency-traversal-outgoing'].get('unchangedFrom33')},
                                'relationKinds': q05['relationKinds']},
        'partitionFoldOrdering': {
            'assessment': ('Selection order is now a function of the evidence. The carrier is the first partition WITH a '
                           'non-null deficiency in ascending coverage2 order, a Coverage paired by two scopes is folded and '
                           'cited once, and an unrelated-scope Coverage is not cited. Each control discriminates the change: '
                           'the same harness on frozen33 is order-dependent.'),
            'E1': q05['cases'][[c['id'] for c in q05['cases']].index('E1-dep-fold-invariant-under-every-map-insertion-order')]['observed'],
            'E2': case05['E2-multi-scope-same-kind-dedup-and-first-carrier-with-deficiency']['observed'],
            'E2pairing': q05['E2-pairing'],
            'H3processBoundary': q06['H3']['summary'],
            'controls': {'E1': case05['E1-dep-fold-invariant-under-every-map-insertion-order']['passed'],
                         'E2': case05['E2-multi-scope-same-kind-dedup-and-first-carrier-with-deficiency']['passed'],
                         'H3': case06['H3-process-boundary-hash-seeded-order']['passed']}},
        'wholeRecordFoldsAndTies': {
            'assessment': ('RC and closedWorld are replaced whole only on a strictly worse rank, ties (including '
                           'complete/not-applicable) keep the incumbent whole, confidence is an independent minimum, '
                           'derivationKinds is an ordered union, unfolded fields keep the first partition, and every '
                           'partition is cited.'),
            'standing': 'helper-unit over natively validated RC/CW records (E5b); my first attempt E5 used two invalid records and is kept as a probe error',
            'controls': {'E5b': case06['E5b-fold-semantics-over-natively-valid-records']['passed']}},
        'searchAccountingTable': {
            'assessment': ('The published three-case table agrees with the branches on every admitted cell. A present '
                           'admitted non-qualifying attestation behaves exactly like an absent one; schema-invalid or '
                           'misjoined attestations are global admission refusals even when they do not match the current '
                           'atom; and sufficiency fails independently of qualification. Prose precision: see A-12.'),
            'G1': {'passed': case05['G1-table-agrees-with-branches-on-every-admitted-cell']['passed'],
                   'cells': len(q05['G-table']), 'admitted': len(g_admitted), 'refused': g_refused,
                   'disagreements': case05['G1-table-agrees-with-branches-on-every-admitted-cell']['observed']['disagreements']},
            'G2sufficiencyIndependentOfQualification': case05['G2-sufficiency-fails-independently-of-search-qualification']['passed'],
            'G3qualificationMatrix': {'passed': case05['G3-admitted-nonqualifying-equals-absent-and-refusals-are-global']['passed'],
                                      'combinations': len(qm), 'admitted': sum(1 for r in qm if r['admission'] == 'ADMIT'),
                                      'refusedKeys': sorted({r['refusal'] for r in qm if r['admission'] != 'ADMIT'})},
            'G4globalAdmission': case05['G4-attestations-are-admitted-globally-before-matching']['observed'],
            'R1emptyProgram': q06['R1']},
        'causeRepresentationUniverse': q05['I-projection']['AtomCauseV1']},
    'controlsRun': {'q05': {'passed': q05['passed'], 'failed': q05['failed']},
                    'q06': {c['id']: c['passed'] for c in q06['cases']}, 'q09': q09['finding']},
    'receipts': ['receipts/q05-atomlaw.json', 'receipts/q06-followups.json', 'receipts/q09-subject-universe.json',
                 'receipts/q10-reach-and-rows.json', 'receipts/q11-default-reach.json']},
    'pinLedgersAndReport': {'assessment': ('The five pin ledgers and workflows-report change only by re-digesting the three '
                                           'atom owners (line diffs in receipts/diffs); the launcher re-establishes source '
                                           'pin validity on frozen34 and the regenerated workflows report is byte-equal.'),
                            'launcherSourcePinsValid': q07['launcherReport']['sourcePinsValid'],
                            'regeneratedWorkflowsReportEqualsFrozen34': q07['regeneratedWorkflowsReportEqualsFrozen34']},
    'planning': {'layer4Retained': True,
                 'why': ('implementation-normative-inputs.v4.json is byte-identical 33->34, all 29 pins resolve against '
                         'frozen34 and none of the pinned paths is in the delta, so a new source version requires no new '
                         'planning layer; layer3, layer2 and the original source25 layer remain preserved history'),
                 'layer4': q01['layer4'],
                 'checks': q07['planningGroups'],
                 'populations': {'paths': 198, 'packages': 20, 'coverageMappings': 320, 'plannedRecoveryCases': 54,
                                 'recoveryCasesExecuted': 0, 'milestones': 'M0-M6'},
                 'moduleLayoutAndInventoryOwnersUnchanged33to34': all(m33.get(p) == m34.get(p) for p in (
                     'docs/v2/architecture/14-repository-and-module-layout.md',
                     'docs/v2/architecture/repository-file-inventory.v1.json',
                     'docs/v2/architecture/implementation-coverage.v1.json',
                     'docs/v2/architecture/implementation-planning-sources.v1.json'))}}

# ------------------------------------------------------------------ issues and advisories
rows09 = q09['cases']
J['newMustIssues'] = [{
    'id': 'MUST-34-01',
    'title': ('Incoming completeness can answer a proven negative although the subject\'s own program was never bound '
              'for the relation'),
    'selectors': [
        'docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md section 4: "Shared prelude" P2 ("no owed binding at all, neither available nor unavailable")',
        'docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md section 4: "Incoming cause derivation" ("incoming makes no further early return") and "Incoming owed programs = EnumerationPlan bindings for capabilityForRelation[relation]"',
        'docs/coop/design-corrections/foundation/atom_model.v1.py:1462-1465 (P2) and 1525-1601 (incoming accumulation over available bindings only)',
        'compare atom-evaluation-contract.v1.md section 4 outgoing step 1 and atom_model.v1.py:1496-1500 (selector-unbound)'],
    'measured': {label: {k: {'value': v.get('value'), 'causes': v.get('causes')} for k, v in row.items()}
                 for label, row in rows09.items()},
    'finding': q09['finding'],
    'discrimination': ('On identical inputs, the ONLY change from a proven negative to unknown is adding an owed binding '
                       'for the subject\'s own universe: bound-but-unevidenced gives unknown with '
                       'source-target-search-unattested and uncovered-expected-source-subject at U; bound-unavailable gives '
                       'unavailable-program-binding; no references binding anywhere gives missing-relation-coverage. The '
                       'same inputs answered on the outgoing endpoint are unknown via selector-unbound. With only a '
                       'foreign-family program bound, incoming is again a negative with only a non-blocking disclosure.'),
    'whyThisIsAMust': ('A negative atom value is the strongest claim the evaluator makes, and section 4 itself holds the '
                       'rule that an unbound program yields unknown: P2 for no binding at all and outgoing step 1 for no '
                       'binding at U. Incoming applies neither. So requesting LESS analysis (removing the subject\'s own '
                       'unit from the relation) turns an unknown into a certain none=true / exists=false carrying no cause, '
                       'and the result cites only the other program\'s Coverage. The defect is in the normative prose, not '
                       'only in the reference: the published owed-program definition plus "no further early return" '
                       'produce exactly this answer.'),
    'reachability': {
        'defaultProfile': ('NOT reachable: requiredDefault requests every capability whose cell is not NOT-SELECTED, and '
                           'no engine family mixes NOT-SELECTED with requested modes for calls, control-flow, imports, '
                           'reachability or references; syntax-only is UNSUPPORTED-TYPED, which is requested and blocking '
                           '(receipts/q11-default-reach.json).'),
        'explicitNarrowing': ('Reachable by a lawful request: native-capability-matrix.v2.json explicitOverride and '
                              'admission-and-qualification.md let product-configuration analysis.capabilities override the '
                              'request with its own provenance, and cells are exactly the requested ownership tuples '
                              '(enumeration-contract.v1.md section 1). My narrowed plan passes enumeration-plan.schema.v1.json '
                              '(no errors).'),
        'notDemonstrated': ('I did NOT run enumeration closed-world admission for that plan and did NOT build a retained '
                            'Run; the evidence is the published law, atom-api controls and a schema check.')},
    'preExisting': ('Present unchanged in source33: identical results on the frozen33 atom_model '
                    '(receipts/q10-reach-and-rows.json identicalOn33 = %s). It is not a source34 regression, and my own '
                    'source32/source33 ACCEPT records did not find it.' % q10['identicalOn33']),
    'requiredResolution': ('The normative incoming law must make the subject universe\'s own absence visible and blocking '
                           'when the relation has owed bindings but none available at the subject universe and no '
                           'lawful rule makes that program not owed; or it must explicitly and normatively define why '
                           'such a program is not owed and require a typed disclosure in the atom result. Either choice '
                           'must also say what the foreign-family-only case answers. I do not author the wording.'),
    'affectsRows': ['arDispositions/AR-12', 'fwDispositions/FW-08'],
    'standing': 'atom-api controls + published law + enumeration-plan schema; no retained Run; no qualification'}]
J['newShouldIssues'] = []

adv = {a['id']: a for a in BL['advisories']}
a9 = dict(adv['A-9']); a9['statusOn34'] = ('Carried with limits intact: repair_closed_world_selection.v1.py and '
                                           'workflows-and-surfaces.md are byte-identical 33->34; the A-9 admitted-versus-unit '
                                           'limitations are retained exactly.')
a10 = dict(adv['A-10']); a10['selectors'] = list(a10['selectors']) + ['claude-author-package-successor.v11 (current, exports byte-identical to package10)']
a10['statusOn34'] = ('Carried with limits unchanged and now measured on package11: all 13 exports are byte-identical to the '
                     'package10 exports (exportsChanged false), so the construction evidence did NOT change 33->34 while '
                     'the verification is current on 34. Limits retained exactly: TS checkpoint helper-versus-owner only; '
                     'six owner-derived self-consistency; exists/none only with and/or/not unexercised and count-at-most / '
                     'all-covered unimplemented in the partial helper; two-binding construction incomplete with a single '
                     'explicit binding; no compiler, provider or OS qualification.')
a11 = dict(adv['A-11']); a11['statusOn34'] = 'Historical; resolved during the source33 review and not reopened.'
a12 = {
    'id': 'A-12',
    'title': 'Two published incoming alternatives are unreachable under the owning schemas',
    'selectors': ['atom-evaluation-contract.v1.md section 4 search-accounting table row 1',
                  'incoming-search.schema.v1.json scopeRefs minItems 1 and its joins text "untagged scopes fall back to all S scopes"',
                  'atom_model.v1.py:953-975 (_incoming_groups untagged branches) and 1395-1400'],
    'measured': ('(1) Table row 1 reads "no source scopes and no qualifying attestation", but IncomingSearchV1 scopeRefs has '
                 'minItems 1 while admission requires scopeRefs to equal the provider\'s owned scopes, which are empty: no '
                 'admissible attestation can exist for a scope-less provider group, and an attempt refuses the WHOLE atom '
                 'globally (INCOMING_SEARCH_SCHEMA) instead of leaving it unknown. The lawful way an empty selected program '
                 'closes incoming is an explicit empty-subject scope with complete S->U Coverage, which the native scope '
                 'carrier admits and which does close it (R1). (2) A subject scope without enumeratorClosure is refused by '
                 'the native scope carrier as soon as it is paired (ATOM_NATIVE_CARRIER), so the "untagged scope" fallback '
                 'described by the attestation schema and implemented in _incoming_groups is not reachable with admitted '
                 'scope records.'),
    'why_not_a_should': ('Every reachable outcome is correct: row 1 always yields source-target-search-unattested as '
                         'predicted, and the owning schema is itself normative, so a careful consumer is not misled into '
                         'a wrong value. The cost is a consumer who follows the table literally and builds an empty '
                         'attestation, turning a lawful unknown into a global refusal, and a dead branch described as law.'),
    'receipts': ['receipts/q05-atomlaw.json (G-table no-scope rows, F2b, F4)', 'receipts/q06-followups.json (R1)'],
    'statusOn34': 'NEW on source34 (the table is new; the untagged fallback text predates it).'}
J['advisories'] = [a9, a10, a11, a12]

# ------------------------------------------------------------------ package, suites, receipts
J['authorPackageReview'] = {
    'status': 'COMPLETE - INDEPENDENTLY VERIFIED ON SOURCE34 (package11)',
    'package': 'claude-author-package-successor.v11',
    'artifactManifestSha256': q08['artifactManifestSha256'], 'matchesRootVerifiedPackageManifest': q08['matchesRootVerifiedPackageManifest'],
    'members': {'declared': q08['declaredMembers'], 'verified': q08['verified'], 'mismatched': q08['mismatched'],
                'missing': q08['missing'], 'onDiskNotListed': q08['filesOnDiskNotInManifest']},
    'sourceManifestEqualsFrozen34': q08['sourceManifestEqualsFrozen34'],
    'sourceBinding': q08['sourceBinding'], 'parentIsMyVerifiedPackage10': q08['parentIsMyVerifiedPackage10'],
    'constructionProvenance': ('mixed and UNCHANGED from package10: TypeScript-derived groups constructed on source33, '
                               'normalized and Rust groups exact source30 bytes; both construction accounts are '
                               'byte-identical to package10\'s. No historical construction is relabelled as a source34 '
                               'execution; only the verification is current.'),
    'allExportsByteEqualPackage10': q08['allExportsEqualPackage10'],
    'package10To11': {k: q12[k] for k in ('members', 'added', 'removed', 'changedCommon', 'identicalCommon')},
    'residualAuthorAssessment': q12['residualAssessment'],
    'thirteenCases': {'counts': q08['counts'], 'positivesAdmitBoth': q08['positivesAdmitBoth'],
                      'negativesAdmitThenRefuse': q08['negativesAdmitThenRefuse'],
                      'bindingInvalidRefused': q08['bindingInvalidRefused'], 'bindingLawfulAdmitted': q08['bindingLawfulAdmitted'],
                      'allThirteenAsExpected': q08['allThirteenAsExpected'],
                      'rows': [{k: r.get(k) for k in ('group', 'name', 'structural', 'semantic', 'semanticIdMatches', 'semanticReason', 'exportEqualsPackage10')} for r in q08['rows']]},
    'owner': {'path': 'foundation/identity-model.v3.py', 'sha256': q08['ownerSha256'], 'equalsFrozen34Row': q08['ownerEqualsFrozen34Row']},
    'verifier': {'command': q08['verifier']['command'], 'returncode': q08['verifier']['returncode'],
                 'sourceFilesVerified': q08['verification']['sourceFilesVerified'], 'packageFilesVerified': q08['verification']['packageFilesVerified'],
                 'queryChecks': q08['queryChecks'], 'queryAssessment': q08.get('queryAssessment'),
                 'myGroupsIncludingReportDigestsMatchRoot': q08['myGroupsIncludingReportDigestsMatchRoot']},
    'retainedRunsReachChangedAtomBranches': q08['anyRunReachesChangedAtomBranches'],
    'rootVerification': {'path': 'reviews/author-package-final34-verification.v1/verification.json',
                         'sha256': sha(os.path.join(REV, 'author-package-final34-verification.v1/verification.json')),
                         'standing': 'evidence I compared against my own execution, not my acceptance'},
    'grantsNoPackageAcceptance': True, 'receipts': ['receipts/q08-package11.json', 'receipts/q12-package-delta.json']}
J['suites'] = {'standing': 'each job justified by a delta file or a direct consumer of one; root suite receipts are evidence, not authority',
               'disposableCopy': {'copied': q07['disposableCopied'], 'verified': q07['disposableVerified']},
               'jobs': q07['jobs'], 'launcherReport': q07['launcherReport'], 'planningGroups': q07['planningGroups'],
               'disposableFilesRewrittenByCheckers': q07['disposableFilesRewrittenByCheckers'],
               'regeneratedWorkflowsReportEqualsFrozen34': q07['regeneratedWorkflowsReportEqualsFrozen34'],
               'frozen34DeviationsAfterRuns': q07['frozen34DeviationsAfterRuns'], 'allJobsExitZero': q07['allJobsExitZero'],
               'checkAtoms': json.load(open(os.path.join(RC, 'suite34-check-atoms.stdout'))),
               'receipt': 'receipts/q07-suites.json'}
J['suites']['checkAtoms'] = {k: J['suites']['checkAtoms'][k] for k in ('standing', 'ok', 'passed', 'failed')}

# ------------------------------------------------------------------ rows
stale = {s['row']: s for s in q04['staleReadingStanding']}
CONSEQ = {
    'arDispositions/AR-12': ('PARTIALLY-REOPENED-BY-MUST-34-01',
        'PARTIALLY REOPENED ON 34 AT THE ATOM-LAW BOUNDARY. This row\'s own owners are byte-identical 33->34 and its '
        'native negative-provenance account is inherited. But an authoritative negative is only as strong as the atom law '
        'that consumes provenance, and the source34 incoming law answers none=true / exists=false with no cause when the '
        'subject\'s own program has no owed binding and another same-family program is fully evidenced (MUST-34-01; '
        'receipts/q09-subject-universe.json; identical on frozen33, receipts/q10). The baseline disposition is not '
        'rewritten; its atom-level consequence stays open until MUST-34-01 is resolved.'),
    'fwDispositions/FW-08': ('PARTIALLY-REOPENED-BY-MUST-34-01',
        'PARTIALLY REOPENED ON 34. The omissions this row covers still hold and are now better controlled: census-driven '
        'missing partitions and subjects stay unknown, and every outgoing early return keeps its completeness cause while '
        'known matches still decide the value (B1/B2). One omission is not disclosed at all: under lawful explicit '
        'capability narrowing an incoming atom leaves the subject\'s own unbound program out of accounting without any '
        'cause (MUST-34-01).'),
    'fwDispositions/FW-06': ('STRENGTHENED-ON-34',
        'STRENGTHENED ON 34 AND MEASURED. Section 4 now publishes ascending scope2/coverage2 selection order, with the '
        'combined Coverage list deduplicated and sorted after pairing. Every coverages x scopes x coverageScopes insertion '
        'order gives one result (E1: 24 orderings; E2: 480 orderings), and six fresh interpreters with six different '
        'hash-seeded insertion orders give one digest (H3). The same harness on frozen33 yields two results with different '
        'carriers, so the controls discriminate the change.'),
    'inheritedResidualDispositions/DR-009': ('STRENGTHENED-ON-34',
        'STRENGTHENED ON 34. Reproducibility across machines now also covers the atom carriers: the typed coverage-unknown '
        'nativeCause no longer depends on process hash seeding (H3: six processes, one digest on frozen34; two on frozen33). '
        'Owners byte-identical 33->34; the rest is inherited.'),
    'arDispositions/AR-16': ('STRENGTHENED-ON-34',
        'STRENGTHENED ON 34. Exact outcomes now include a deterministic atom carrier: coverage-unknown\'s nativeCause is the '
        'first non-null over published positions (primary before dependency, E4) and, within a position, taken whole from '
        'the first partition in ascending coverage2 order that carries a deficiency (E2). Owners byte-identical 33->34.'),
}
F_TEXT = {
    'F-01': 'the charter custody artifacts carried from package10 are among the 301 members byte-identical in package11.',
    'F-02': 'the consumer-b.v13 v6/v7 assessment artifacts are among the 301 members byte-identical in package11.',
    'F-03': 'verify-package.py ran against frozen34 in this runtime: rc 0, 12,899 source files, 311 package files, 7/7 queries, group and report digests equal to root\'s receipt.',
    'F-05': 'ts-invalid-default-entry structurally ADMITS then semantically REFUSES EVALUATOR_ENUMERATION_JOIN:ENUMERATION_BINDING_PROGRAM_ENTRY through the frozen34 identity-model.v3.py owner.',
    'F-06': 'ts-lawful-explicit-selection admits through both boundaries with its runId; the two-binding construction remains incomplete with a single explicit binding, an evidence limit.',
    'F-08': 'the property probe remains a separate command (author-properties.json and check-author-properties.py byte-identical to package10); README.md changed only to describe the source34 binding.',
    'F-10': 'mixed provenance is unchanged: exportsChanged false, all 13 exports byte-identical to package10, constructionSourceVersion {typescriptDerivedGroups: 33, normalizedAndRustGroups: 30}, currentVerificationSourceVersion 34.',
    'F-11': 'the helper files carrying this row (author_portable.py, evaluator.py.patch) are byte-identical to package10.',
    'F-12': 'the weighting holds on the same exports: only checkpoint3/author-ts is helper-versus-owner agreement; six positives are owner-derived self-consistency; three negatives derive from checkpoint3.',
    'F-13': 'package11\'s evaluation-residual-author-assessment.json binds the frozen34 manifest bd00c07d..., carries 30 rows with independentGrade PENDING and TCB-SCOPE-01 over 13 dependents; its evidence resolves against frozen candidate34.',
    'F-14': 'all 30 rows still carry proposed-account-supported-with-stated-limits; informational, no grade awarded.',
}
F_SOURCE = {
    'F-04': ['docs/coop/design-corrections/foundation/enumeration-contract.v1.md', 'docs/coop/design-corrections/foundation/check-enumeration.v1.py'],
    'F-07': [],
    'F-09': ['docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md', 'docs/coop/design-corrections/foundation/execution-inputs.schema.v1.json',
             'docs/coop/design-corrections/foundation/execution_inputs_model.v1.py', 'docs/coop/design-corrections/foundation/check-execution-inputs.v1.py',
             'docs/coop/design-corrections/foundation/execution_inputs_fixture.v3.py'],
}
PKG = ('Verified on the source34-bound package11 (artifact manifest 38f7ce94..., 311/311 members, source-manifest '
       'byte-equal to frozen34, all 13 Run/control cases through open_run_closure AND close_run with my own decoder).')
tcb = set(BL['sharedAssumptionTCBSCOPE01']['dependentRows'])
counts = {'inherited': 0, 'consequence': 0, 'package': 0, 'sourceLawF': 0}
for mp in MAPS:
    for rid, row in BL[mp].items():
        key = mp + '/' + rid
        qr = q04['rows'][key]
        owners = qr['owners']
        row['ownerFilesChangedIn33to34'] = sorted(p for p in owners if p in DELTA)
        row['ownerFilesUnchangedIn33to34'] = sorted(p for p in owners if p not in DELTA)
        row['ownerPathsResolveInFrozen34'] = all(p in m34 for p in owners) if owners else None
        row['ownerArraysDerivedFromManifests33and34'] = bool(owners)
        if rid in F_SOURCE:
            paths = F_SOURCE[rid]
            row['subjectOwnerFilesOn34'] = paths
            row['subjectOwnerBytesEqual33and34'] = all(m33.get(p) == m34.get(p) and p in m34 for p in paths)
        if key in stale:
            ch = row.get('ownerFilesChangedIn32to33') or row.get('ownerSelectorsChangedIn32to33') or []
            row['readingStandingLegacyCorrectionOn34'] = {
                'legacyString': row.get('readingStanding'), 'whyStale': stale[key]['why'],
                'accurateHistoricalStanding': ('source33: owner(s) %s CHANGED 32->33 and the changed region was read in '
                                               'the source33 session' % ch) if ch else
                                              'source33: no owner of this row changed 32->33; the reading was inherited on exact bytes',
                'legacyStringKept': 'the legacy string is not edited; this field qualifies it'}
        row['appliedByThisReview'] = False
        row['finalApplicationOutcomeGranted'] = False
        n = len(owners)
        if key in CONSEQ:
            st, txt = CONSEQ[key]
            row['statusChangeOn34'] = st
            row['currentStatusOn34'] = txt
            row['readingStandingOn34'] = ('INHERITED ON EXACT BYTES for this row\'s %d owner file(s) (identical sha256 in the '
                                          'frozen33 and frozen34 manifests), PLUS a fresh source34 assessment of the changed '
                                          'atom law\'s consequence for this subject (receipts/q05, q06, q09).' % n)
            counts['consequence'] += 1
        elif mp == 'fDispositions' and rid in F_TEXT:
            row['statusChangeOn34'] = 'RE-VERIFIED-ON-PACKAGE11'
            row['currentStatusOn34'] = PKG + ' Row-specific on 34: ' + F_TEXT[rid]
            row['readingStandingOn34'] = ('PACKAGE-BORNE: re-measured on package11 in this runtime (receipts/q08-package11.json, '
                                          'q12-package-delta.json); historical package10 and package8 readings stay in the '
                                          'baseline fields.')
            counts['package'] += 1
        elif mp == 'fDispositions':
            row['statusChangeOn34'] = 'INHERITED'
            if rid == 'F-07':
                row['currentStatusOn34'] = ('Inherited on 34: package11 carries the package10 exports byte-identically, so the '
                                            'measured predicate coverage (exists/none only; and/or/not unexercised; '
                                            'count-at-most / all-covered unimplemented in the partial helper) is unchanged, and '
                                            'the disclosure remains accurate.')
                row['readingStandingOn34'] = 'INHERITED ON EXACT EXPORT BYTES (receipts/q08-package11.json exportEqualsPackage10 on all 13).'
            else:
                row['currentStatusOn34'] = ('Inherited on 34: every subject owner of this row (%s) is byte-identical 33->34, '
                                            'so the source33 account in currentBasisOn33 is inherited, not re-derived.%s'
                                            % (', '.join(p.split('/')[-1] for p in F_SOURCE[rid]),
                                               ' The owning suites still pass on frozen34 (evaluator3 launcher, 16/16 children).'))
                row['readingStandingOn34'] = 'INHERITED ON EXACT BYTES (receipts/q04-rows.json; manifests 33/34).'
            counts['sourceLawF'] += 1
        else:
            row['statusChangeOn34'] = 'INHERITED'
            extra = ''
            if mp == 'evaluationResidualDispositions':
                extra = (' The author proposal remains PENDING independent grading and no grade is awarded here.' +
                         (' This row is one of the 13 TCB-SCOPE-01 dependents; that assumption is not closed.' if rid in tcb else ''))
            row['currentStatusOn34'] = ('Inherited on 34: all %d owner path(s) are byte-identical in the frozen33 and frozen34 '
                                        'manifests, none is in the 9-file delta, and the changed atom completeness law does not '
                                        'bear on this row\'s subject. The source33 current account is retained verbatim in '
                                        'currentStatusOn33 and is inherited with explicit standing, not re-derived.%s' % (n, extra))
            row['readingStandingOn34'] = ('INHERITED ON EXACT BYTES: %d owner file(s) with identical sha256 in the frozen33 and '
                                          'frozen34 manifests (receipts/q04-rows.json). The substantive reading is the one '
                                          'recorded for source33.' % n)
            counts['inherited'] += 1
        row['currentFieldStandingOn34'] = ('currentStatusOn34 and readingStandingOn34 are the source34 account; every baseline '
                                           'field of this row is preserved verbatim as history.')
    J[mp] = BL[mp]
J['rowCarryForwardCounts'] = counts
J['readingStandingAudit'] = {
    'rule': ('stale = the legacy string claims unchanged owners while the row\'s own 32->33 changed-owner array is non-empty, '
             'or claims a changed/re-read owner while that array is empty'),
    'staleRows': sorted(stale), 'count': len(stale),
    'rootCount': 8,
    'reconciliationWithRoot': ('Root reported eight. Eight rows are the "unchanged" class; the ninth, DR-011-R12, is the '
                               'inverse class (claims a changed owner region although none of its owners changed 32->33). '
                               'All nine carry readingStandingLegacyCorrectionOn34; no legacy string is edited.'),
    'receipt': 'receipts/q04-rows.json'}
J['sharedAssumptionTCBSCOPE01'] = dict(BL['sharedAssumptionTCBSCOPE01'])
J['sharedAssumptionTCBSCOPE01']['statusOn34'] = ('One joint consequence over the same 13 dependent rows; not closed, not '
                                                 'regraded; every dependent row\'s owners are byte-identical 33->34.')
J['dispositionCounts'] = {mp: len(BL[mp]) for mp in MAPS}
J['dispositionCounts']['total'] = sum(J['dispositionCounts'].values())
J['dispositionStandingForEveryRow'] = dict(BL['dispositionStandingForEveryRow'])
J['crossUnitStanding'] = dict(BL['crossUnitStanding'])
J['crossUnitStanding']['statusOn34'] = ('All obligations carried forward unchanged: 28 condition-2 obligations retained, 32 '
                                        'product qualification gates unperformed with condition 5 NOT MET, 54 recovery cases '
                                        'unexecuted, TCB-SCOPE-01 one joint consequence over 13 rows, and the D9 implementation '
                                        'obligation on DR-007 / DR-011-R08 persists.')
J['grantsNothing'] = dict(BL['grantsNothing'])
J['verdictBasis'] = (
    'SOURCE34 DESIGN: CHANGES_REQUIRED. Full custody verified: manifest bd00c07d... and archive 5c9768de... match, all '
    '12,899 rows (736,798,408 bytes) verify with no missing, mismatched or extra file, the archive equals the manifest, and '
    'the parent is exactly the source33 I reviewed. My manifest-derived delta is 9 changed files (0 added, 0 removed) and '
    'agrees with root\'s inventory; three carry substance (the atom contract section 4, four reference selection functions, '
    'the checker) and six only re-pin those digests. The changed atom completeness law is correct on every changed branch '
    'I tested with my own controls, including the root-authored final table: shared prelude, outgoing early returns that '
    'never stop known matches, incoming accumulation per (U, provider), typed source-universe attribution, dependency '
    'traversal, ascending selection order with dedup after pairing, whole-record folds and ties, and the search-accounting '
    'table on all 21 admitted cells, all discriminating against source33 where the change is behavioural. Suites (check-atoms '
    '81/81, the evaluator3 launcher 16/16 with pins valid, foundation, integration, native 375/375, security, workflows) and '
    'planning checks pass on frozen34 with zero drift; layer4 is retained; package11 verifies 311/311 with all 13 cases and '
    '7 queries. Changes are nonetheless required for MUST-34-01: the published incoming law answers a proven negative when '
    'the subject\'s own program was never bound for the relation, reachable by lawful explicit capability narrowing and '
    'present unchanged since source33, where my own ACCEPT missed it.')
J['correctionsToMyOwnPriorRecords'] = [{
    'id': 'C34-01', 'records': ['claude-independent-design.v33', 'claude-independent33-reconciliation.v1', 'claude-independent33-reconciliation.v2'],
    'correction': ('Those records accepted an atom law that already produced the MUST-34-01 negative; the frozen33 '
                   'atom_model gives identical results on the same inputs. They are preserved unchanged; this record '
                   'qualifies them.'), 'evidence': 'receipts/q10-reach-and-rows.json'}]
J['limitations'] = [
    'Design and reference layers only. No product implementation exists and none is demanded.',
    'Atom-law controls are atom-api (global atom-input admission and evaluate_atom over synthetic inputs) or helper-unit; none is native producer admission, a retained Run, blind reconstruction or qualification.',
    'No retained package11 Run reaches the changed incoming or attestation branches; retained-Run evidence therefore says nothing about them.',
    'MUST-34-01 reachability under lawful explicit narrowing rests on published request law plus an enumeration-plan schema check; enumeration closed-world admission and a retained Run were not executed.',
    'The author package is author-assisted reference evidence verified on source34; its construction provenance is mixed and unchanged from package10, and verifying it grants no package acceptance.',
    'A-10 limits retained: TS checkpoint helper-versus-owner only, six owner-derived self-consistency, exists/none with other operator limitations, incomplete two-binding construction with a single explicit binding, no compiler/provider/OS qualification.',
    'A-9 repair controls retain their exact admitted-versus-unit limitations.',
    'All 30 author residual proposals remain PENDING independent grading; none is substantively graded here.',
    'Unchanged readings are inherited only on exact manifest-byte equality and are labelled INHERITED; they are not fresh re-reads.',
    'Root and author receipts (including root\'s five-case probe and the 81 check-atoms cases) were treated as evidence to assess, never as authority.',
    'No consumer output, runtime, report or blind replay file was read; no blind oracle is an input.']
J['probeErrorsPreserved'] = [
    'q00: first run assumed a manifest "size" key; the manifest uses "bytes". Fixed in place before any result was used.',
    'q05 F4: my untagged-scope fixture was refused by the native scope carrier (ATOM_NATIVE_CARRIER), so F4 tested nothing about groups; the refusal itself became the A-12 observation.',
    'q05 H3: child interpreters failed on my own import path (-I drops the script directory); the control never ran. Rerun correctly in q06.',
    'q05 E5: two ResolutionCompletenessV2 records used an unresolvedEdgeClasses value outside the native enum; E5b repeats the fold with valid records.',
    'q05 G4: the "scope misjoin" mutation also emptied scopeRefs, so it refused at schema before any join; the other mutations refuse as labelled.',
    'q08: the atom-reach scanner also counted schema-shaped objects as atoms; only the string-valued atoms (exists/file/source, none/clones/source) and the zero incoming-endpoint / zero IncomingSearchV1 counts are relied on.',
    'q10 part 2: the matrix parser read the wrong shape and returned null for every cell, measuring nothing; q11 is the correct measurement.']
recs = sorted(f for f in os.listdir(RC) if f.endswith('.json'))
J['evidenceReceipts'] = {
    'interpreter': '/tmp/opensip-architecture-review-env/bin/python -I -B',
    'receipts': {f: sha(os.path.join(RC, f)) for f in recs},
    'probes': sorted(f for f in os.listdir(os.path.join(BASE, 'probes')) if f.endswith('.py')),
    'frozen34DriftAfterEveryProbe': {'q05': [q05['frozen34DriftBefore'], q05['frozen34DriftAfter']],
                                     'q06': [q06['frozen34DriftBefore'], q06['frozen34DriftAfter']],
                                     'q07': q07['frozen34DeviationsAfterRuns'], 'q08': q08['frozen34DeviationsAfter'],
                                     'q09': [q09['frozen34DriftBefore'], q09['frozen34DriftAfter']]}}
J['historyPointers'] = {'source33RecordBlocks': ('source33-specific top-level blocks (delta32to33, the source33 execution-law '
                                                 'assessment, correction ledgers R33-REC and R33-REC2, audits) are retained in '
                                                 'the baseline and earlier records by reference, not copied as current'),
                        'records': J['sessionIdentity']['priorReviewsHistoricalUnchanged']}
out = os.path.join(BASE, 'review.json')
json.dump(J, open(out, 'w'), indent=1, default=str)
print('rows:', J['dispositionCounts'], '| carry:', counts)
print('verdict:', J['verdict'], '| MUST:', [m['id'] for m in J['newMustIssues']], '| advisories:', [a['id'] for a in J['advisories']])
print('bytes', os.path.getsize(out), 'sha256', sha(out))
