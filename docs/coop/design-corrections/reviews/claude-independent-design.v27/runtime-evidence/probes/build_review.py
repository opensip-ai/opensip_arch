"""Assemble review.json for the v27 successor delta + focused evidence review.

Every disposition row carries its own reason. The v26 maps are re-decided against the measured
26->27 delta rather than copied: rows whose owner bytes did not change say so explicitly and name
what I inherited; rows whose owner bytes DID change carry the change I measured and read.
"""
import json, os

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v27'
REC = os.path.join(BASE, 'receipts')
SRC = '/tmp/opensip-design-corrections/candidate-subject.v27'


def rec(n):
    return json.load(open(os.path.join(REC, n)))


v26 = json.load(open('/tmp/opensip-design-corrections/claude-independent-design.v26/review.json'))
p00, p01 = rec('p00-verify27.json'), rec('p01-delta.json')
p06, pE = rec('p06-package-verify.json'), rec('pE-exports.json')
pF, pF3 = rec('pF-portable.json'), rec('pF3-blobdelta.json')
pH, pS = rec('pH-groups27.json'), rec('pS-reassess.json')
pJ, pK4 = rec('pJ-fremedies.json'), rec('pK4-rootctl.json')
pK2, pM = rec('pK2-rootexec.json'), rec('pM-f09tcb.json')
pN, pO = rec('pN-residualbind.json'), rec('pO-axcustody.json')
pL, pP = rec('pL-pkgprobes.json'), rec('pP-handoff.json')
prop = json.load(open(os.path.join(
    SRC, 'docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json')))

CHANGED = {c['path'] for c in p01['changed']} | {a['path'] for a in p01['added']}

R = {}
R['review'] = ('Independent design review of consolidated product source27 — successor delta and '
               'focused evidence review, continuing the same reviewer origin that produced the '
               'source26 CHANGES_REQUIRED review.')
R['origin'] = v26['origin']
R['ancestry'] = {
    'sameOriginAsSource26Review': True,
    'predecessorReview': 'claude-independent-design.v26 (verdict CHANGES_REQUIRED)',
    'predecessorSubjectManifestSha256': p00['parentManifestSha256'],
    'source27DeclaredParentManifestSha256': p00['parentManifestSha256'],
    'parentIsExactlyTheSource26IReviewed': p00['parentIsTheSource26IReviewed'],
    'basis': ('source27 manifest declares parentManifestSha256 c9a6c26a..., which is byte-identical '
              'to the manifest of the subject my v26 review verified and graded. Ancestry is proven '
              'by measurement, not by narrative.')}
R['subjectManifestSha256'] = p00['manifestSha256']
R['verifiedManifest'] = True
R['manifestVerification'] = {
    'manifestPath': p00['manifestPath'],
    'manifestSha256': p00['manifestSha256'],
    'manifestSha256MatchesDeclared': p00['manifestSha256Matches'],
    'archiveSha256Expected': 'adb78633c890eb99e3eb001d050c1fec0b77be870d18201aa732947fde827603',
    'archiveSha256Verified': p00.get('archiveSha256Matches', p00.get('archiveMatches')),
    'declaredFileCount': p00['fileCountDeclared'],
    'filesChecked': p00['filesChecked'],
    'everyFileShaAndByteCountVerified': True,
    'declaredTotalBytes': p00['totalBytesDeclared'],
    'measuredTotalBytes': p00['bytesMeasured'],
    'extrasOnDisk': p00.get('extraOnDisk', p00.get('extrasOnDisk', 0)),
    'snapshotUnchangedAfterAllRuns': pH['frozenDeviationsAfterRuns'] == 0,
    'authoritativeSource': 'frozen snapshot27 only; no mutable tree was ever read as authority'}

R['delta26to27'] = {
    'derivedByThisReview': True,
    'method': 'set difference over the two frozen manifests, then line-level diff with both sides manifest-authenticated',
    'added': p01['addedCount'], 'removed': p01['removedCount'], 'changed': p01['changedCount'],
    'netBytes': p01['netBytes'],
    'touchesReviewsTree': p01['deltaTouchesReviewsTree'],
    'addedPaths': [a['path'] for a in p01['added']],
    'changedPaths': [c['path'] for c in p01['changed']],
    'pureDigestOnlyEdits': ['docs/v2/architecture/report-asset-binding.v1.json',
                            'docs/v2/architecture/implementation-coverage.v1.json',
                            'docs/coop/design-corrections/foundation/source-pins.v1.json',
                            'docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json',
                            'docs/coop/design-corrections/native/source-pins.v2.json',
                            'docs/coop/design-corrections/security/source-pins.v1.json',
                            'docs/coop/design-corrections/workflows/source-pins.v1.json',
                            'docs/coop/design-corrections/workflows/workflows-report.v1.json'],
    'note': ('report-asset-binding.v1.json and implementation-coverage.v1.json have identical byte '
             'counts in 26 and 27 with different digests; I diffed both and confirmed the edits are '
             'the B11->B14 anchor disambiguation and its three citations, and pin-digest refreshes.')}

# ---------------- reading ----------------
R['readingStanding'] = (
    'A programmatic traversal is distinct from complete tool-delivered prose reading, and the two are '
    'reported apart. "Completed this review" means the bytes were delivered to me as prose in this '
    'session. "Inherited" means I read the file completely in the v26 session and the 26->27 delta '
    'shows its bytes unchanged; I do not re-badge that as a fresh read.')
R['completedReadingThisReview'] = [
    {'path': 'docs/coop/design-corrections/foundation/provider-target-attribution-return.schema.v2.json',
     'lines': 253, 'sha256': '2d5719b57dc65095', 'why': 'REQUIRED CORRECTION of the v26 scope overclaim',
     'changedIn27': False,
     'coverage': 'complete file read in bounded chunks via the Read tool, all 13 schemaKeys and ~40 joinKeys'},
    {'path': 'docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json',
     'lines': 242, 'changedIn27': False,
     'coverage': 'complete file read; all 30 rows and the standing line'},
    {'path': 'docs/coop/design-corrections/foundation/target-attribution.schema.v2.json',
     'changedIn27': True, 'coverage': 'changed region read in full context plus the whole allOf chain'},
    {'path': 'docs/coop/design-corrections/native/occupancy-companion.schema.v1.json',
     'changedIn27': True, 'coverage': 'changed region read in full context'},
    {'path': 'docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md',
     'changedIn27': True, 'coverage': 'changed sentence read in its full section'},
    {'path': 'docs/coop/design-corrections/foundation/identity-schemas.v3.json',
     'changedIn27': True, 'coverage': 'changed standing + new scope block read in full; whole bundle traversed programmatically'},
    {'path': 'docs/v2/contracts/product-v1/identity-and-evidence.md',
     'changedIn27': True, 'coverage': 'changed section 3 paragraphs read in full context'},
    {'path': 'docs/coop/design-corrections/security/carrier-migration.v1.md',
     'changedIn27': True, 'coverage': 'changed intent scoping read in full section'},
    {'path': 'docs/coop/design-corrections/security/carrier-dispatch.v3.json',
     'changedIn27': True, 'coverage': 'changed openDispatch/freshInstallPath rows read in full'},
    {'path': 'docs/coop/design-corrections/security/carrier-format.v3.md',
     'changedIn27': True, 'coverage': 'new evidence-custody/diagnosis-vocabulary paragraph read in full'},
    {'path': 'docs/v2/contracts/product-v1/security-and-lifecycle.md',
     'changedIn27': True, 'coverage': 'changed S13 count sentences read in full'},
    {'path': 'docs/v2/architecture/report-asset-binding.v1.json',
     'changedIn27': True, 'coverage': 'all 14 anchors and every citation traversed and diffed'},
    {'path': 'docs/v2/architecture/implementation-normative-inputs.v2.json',
     'changedIn27': 'ADDED', 'coverage': 'complete new file read'},
    {'path': 'docs/v2/architecture/implementation-planning-sources.v1.json',
     'changedIn27': True, 'coverage': 'new previousArchitectureInputLayer block read in full'},
    {'path': 'docs/coop/design-corrections/foundation/check-provider-attribution-return.v2.py',
     'changedIn27': True, 'coverage': 'four new test functions (10 cells) read and executed'},
    {'path': 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json#/$defs/InternalUnitRootV1',
     'changedIn27': False, 'coverage': 'definition read in full for the F-04 assessment'},
    {'path': 'docs/v2/contracts/product-v1/native-evidence.md U-0',
     'changedIn27': False, 'coverage': 'U-0 clause and all 21 root-bearing lines read'},
    {'path': 'claude-author-package-successor.v4/README.md', 'coverage': 'complete'},
    {'path': 'claude-author-package-successor.v4/claude-author-remint-review.md', 'coverage': 'complete'},
    {'path': 'claude-author-package-successor.v4/author-delivery-commands.md', 'coverage': 'complete'},
    {'path': 'claude-author-package-successor.v4/check-author-query.py', 'coverage': 'complete'},
    {'path': 'claude-author-package-review.v1/review.md (F-01..F-14)', 'coverage': 'all 14 finding records read in full'},
]
R['inheritedReadingFromV26'] = {
    'standing': ('Read completely in the v26 session; the delta I derived shows these bytes unchanged '
                 'in 27. Not claimed as freshly read here.'),
    'contractsReadCompletelyInV26': len(v26['contractsReadCompletely']),
    'readCompletelyLinesInV26': v26['readCompletelyLines'],
    'unchangedIn27': True}

# ---------------- corrections to my own prior work ----------------
R['correctionsToMyOwnPriorReview'] = [
    {'id': 'C-1', 'kind': 'scope overclaim',
     'what': ("v26 requiredReviewActions.targetAttributionV2AndProviderReturnSchemasReadCompletely was "
              "true while v26 contractsReadCompletely carried no entry for "
              "foundation/provider-target-attribution-return.schema.v2.json. The flag overstated what "
              "the reading record supported."),
     'correctedHow': ("I read that entire file this session (253 lines, all 13 schemaKeys and ~40 "
                      "joinKeys), together with the incorporated provider-return laws, the registered "
                      "definitions and the affected joins, and record measured full coverage above."),
     'v26ReportAltered': False,
     'note': 'The v26 report is left exactly as issued; this correction lives only in the v27 report.'},
    {'id': 'C-2', 'kind': 'evidence mislabelling',
     'what': ("v26 probe pB2 was described as exercising the buffer/bind/capture/atom boundaries. It "
              "used inspect.getsource and jsonschema validation — it read and validated source, it did "
              "not execute those boundaries."),
     'correctedHow': ("This session executed buffer_fact_batch_occupancy, bind_worker_occupancy, "
                      "capture_occupancy, project_companion_to_v2 and AM._admit_target_attributions "
                      "for real, on frozen snapshot27 bytes, and the receipts carry the raw outcomes."),
     'v26ReportAltered': False},
    {'id': 'C-3', 'kind': 'evidence over-weighting',
     'what': ("v26 framed a two-record differing-digest pair as defeating independent replay. Supplying "
              "different optional hints intentionally is expected to change descriptor digests; a pair "
              "is neither a complete reminted Run demonstration nor a general nondeterminism proof."),
     'correctedHow': ("pM1_weighting re-measured every position. The positions that still admit several "
                      "digests are exactly the ones the contract declares meaningful (the fact.anchors "
                      "precedent); the real defect was the eight positions where the contract declares "
                      "the hint meaningless yet two spellings were admissible. 27 closes those eight."),
     'v26ReportAltered': False},
    {'id': 'C-4', 'kind': 'citation undercount',
     'what': 'v26 S-3 said "the two (B11/B12) citations"; there are three.',
     'correctedHow': ('I re-counted on 27: 0 B11/B12 citations remain and 3 B14/B12 citations are '
                      'present, so root updated all three, one more than my v26 text described.'),
     'v26ReportAltered': False},
    {'id': 'C-5', 'kind': 'probe defects in THIS session (preserved, not design faults)',
     'what': ['pM1_boundaries.py called buffer_fact_batch_occupancy with wrong kwargs and '
              'public_observation without diagnostic_bytes (TypeError both times)',
              'my target-attribution fixture omitted packageManifestPath, so package/external '
              'hint=null refused for my fixture\'s reason, not the design\'s',
              'pK2 first run passed the membership wrapper where admit_unit_roots takes the unit list, '
              'so all nine cases refused units:not-a-list',
              'pK3 computed guardPrecedesBindingJoin against the DEFINITION line of _unit_for_cell '
              'rather than its call site, giving a wrong False',
              'pP_handoff picked the 185-char `standing` string over the 8-row `standingRules` list',
              'my first assess-author-query.py invocation passed --source/--package instead of --input'],
     'correctedHow': 'each was re-run correctly; every failed run is preserved in the receipts and labelled mine',
     'v26ReportAltered': False}]

# ---------------- delta assessment ----------------
R['deltaAssessment'] = {
    'M-1': {'v26Severity': 'MUST', 'status': 'RESOLVED', 'basis': (
        'Both logicalPath schemas and the prose now exclude the hint at kind=unknown, and the '
        'atom contract sentence reads "null when kind=package or kind=unknown". My exhaustive '
        '4x3x2 = 24-cell audit finds 24/24 cells conforming to the declared meaning: the eight '
        'positions the contract calls meaningless now admit exactly one encoding, and the four it '
        'calls meaningful still admit the lawful hint, so the correction is not over-narrowed. '
        'Executed at all three host entries (buffer/bind/capture) plus the retained-atom admission; '
        'every meaningless-position hint refuses.')},
    'M-1-routeSufficiency': {'status': 'ROOT DECLINATION CORRECT', 'basis': (
        'I suggested a new internal fault key in v26. Root instead routed through the existing '
        'PROVIDER_RETURN_SCHEMA / TARGET_ATTRIBUTION_SCHEMA keys and added no new fault. I executed '
        'the public derivation: the two pre-existing sibling keys '
        'TARGET_ATTRIBUTION_LOGICAL_PATH_ON_FIRST_PARTY and _ON_PACKAGE are themselves '
        'input-schema-invalid and reach the identical public termination — operational-failed, '
        'PROVIDER.PROTOCOL_VIOLATION, provider-protocol, EVALUATION.INPUT_REFUSED. A new key would '
        'be publicly indistinguishable from the ones already there. I do not demand a new key merely '
        'because I suggested one; the existing route suffices.')},
    'S-1': {'v26Severity': 'SHOULD', 'status': 'RESOLVED', 'basis': (
        'The standing is narrowed to "Every bare 64-hex digest field", the three prose sentences are '
        'narrowed the same way, and a new x-opensip-digest-domains.scope block publishes machine-'
        'readable selectors (pattern ^[0-9a-f]{64}(?![\\s\\S]) and $ref #/$defs/Hash) plus explicit '
        'rules for nullable branches and typed-prefix identities. Measured: 64 bare occurrences, 0 '
        'unannotated even counting branches; 63 typed-prefix occurrences, all outside the scope the '
        'annotation now claims. The universal quantifier is now true of what it quantifies over.')},
    'S-2': {'v26Severity': 'SHOULD', 'status': 'RESOLVED', 'basis': (
        'Intent validation is scoped to the inherited-carrier migration path (acts A-B-C) including a '
        'resumed migration, and the fresh-install path in openDispatch step 8 — including its '
        'interrupted-install act-C resume — is stated to take no CarrierMigrationIntentV1, with '
        'first_generation 1 and null migration fields. The intent domains (observedFormat 1|2, '
        'firstGeneration >= 2) are unchanged and no longer need a satisfying value on a path that '
        'never constructs one.')},
    'S-3': {'v26Severity': 'SHOULD', 'status': 'RESOLVED', 'basis': (
        '14 anchors, 0 duplicate ids. security-completion.v1.md is now B14 and workflows-and-surfaces.md '
        'keeps B11. I re-counted the citations: 0 B11/B12 remain and 3 B14/B12 are present — three '
        'updated, one more than my v26 text claimed. No cited id is undeclared.')},
    'A-1': {'status': 'RESOLVED', 'basis': (
        'carrier-format.v3.md now states witnessMalformed is a read-only recovery diagnosis only and '
        '"deliberately is not a durable carrier_quarantine.reason". The DDL enum is unchanged from 26, '
        'which is now the documented intent rather than an unexplained gap.')},
    'A-2': {'status': 'RESOLVED', 'basis': (
        'The literals 456 and "ten invariant sweeps" are gone, replaced by "the current case fixtures" '
        'and "the current invariant sweeps" with the measured report named as the authority for both '
        'counts. This is the derive-don\'t-transcribe rule native section 1.1 already argues for.')},
    'A-3': {'status': 'RESOLVED', 'basis': (
        'A new evidence-custody and diagnosis-vocabulary paragraph declares the scratch citations '
        'relative to the original author review runtime, states they add no law, and distinguishes a '
        'check-integrated-carrier rerun from reproduction of the original C1-C18 measurements.')}}

# ---------------- F rows ----------------
F = {}


def f(fid, sev, area, status, basis, limits=None):
    F[fid] = {'severity': sev, 'area': area, 'disposition': status, 'basis': basis}
    if limits:
        F[fid]['limits'] = limits


f('F-01', 'major', 'charter custody / AR-03 / AR-05', 'RESOLVED',
  'The pinned charter now resolves inside the frozen package. I computed sha256 of '
  'historical-consumer-custody/original-requirements.json and it equals the F-01 pin '
  '08dffd7f...5196e exactly, and original-requirement-handoff.json names that path. I counted the '
  'rows myself in the charter bytes: requirements 123, standing 8, futureQualification 3.')
f('F-02', 'major', 'custody / AR-03', 'RESOLVED',
  'historical-consumer-custody carries the consumer-b.v13 v6 root-owner-assessment.v1 and v7 '
  'root-partial-assessment.v1 artifacts with an attachment-manifest. I verified all 16 rows: 16 '
  'hash-match, 0 mismatch, 0 missing. The evidence AR-03 rests on is now deliverable and pinned.',
  'Preserved historical files still contain 10 mentions of live /tmp working paths. Those are '
  'provenance strings inside artifacts frozen unchanged, not authority pointers; the '
  'attachment-manifest SHAs are the authority and they resolve.')
f('F-03', 'major', 'reproducibility of the seven query checks', 'RESOLVED',
  'The absent check-blind13-exported-graphs.v4.py import is gone; check-author-query.py now takes '
  '--source/--package/--out and loads the query owner from snapshot27 '
  '(workflows/check-query-projection.v3.py) and the transport from the bundled check-export.v4.py. '
  'I ran it myself against source27 and regenerated all eight outputs BYTE-IDENTICAL to the shipped '
  'query-checks1 copies, then ran assess-author-query.py: PASS 7 author query checks. The '
  '"retained-only, not regenerable" impact is eliminated by my own execution.',
  'verify-package.py still does not re-execute the query checks, so regeneration is a reviewer '
  'action rather than an automatic one. That does not restore the original impact.')
f('F-04', 'major', 'normative under-specification: internal root spelling', 'RESOLVED',
  'The remedy is real, named and executable on snapshot27. rootPath is now '
  '$ref #/$defs/InternalUnitRootV1, a per-segment pattern admitting the empty string or a canonical '
  'relative dir and never "."; native-evidence.md carries a normative U-0 clause and documents the '
  'workspaceRoot-vs-rootPath asymmetry on both edges; and a dedicated admission fault '
  'NATIVE_UNIT_ROOT_REPRESENTATION names the offending root and its schema selector. I executed it: '
  '"." and "./" refuse with NATIVE_UNIT_ROOT_REPRESENTATION:units[0].rootPath:#/$defs/'
  'InternalUnitRootV1, "" and "packages/a" still admit, member roots "." and "" refuse against '
  'CanonicalRelativeDirV1. The misattribution is closed: _admit_membership_unit_roots is wired at '
  'enumeration_model.v1.py:581 and short-circuits before the only _unit_for_cell call (747) and '
  'before every ENUMERATION_BINDING_PROGRAM_ENTRY raise (738/740/750/757), translating to the '
  'internal-only ENUMERATION_MEMBERSHIP_UNIT_ROOT with no new public D9 route.',
  'The remedy predates 27 — native-evidence.schemas.v2.json, native_evidence_model.v2.py and '
  'enumeration_model.v1.py are all unchanged in my 26->27 delta. Its control coverage is advisory A-4.')
f('F-05', 'minor', 'control coverage / AR-01 default-unit programEntry', 'RESOLVED',
  'binding-controls ships ts-invalid-default-entry (provenance default-unit with programEntry '
  '"tsconfig.json"). I replayed it through the snapshot27 owner myself: structural custody ADMIT, '
  'then complete semantic replay REFUSE with EVALUATOR_ENUMERATION_JOIN:'
  'ENUMERATION_BINDING_PROGRAM_ENTRY — exactly the admit-then-refuse shape F-05 asked for, and the '
  'refusal the AR-01 correction relies on.')
f('F-06', 'minor', 'fixture hygiene / AR-01 Q3', 'PARTIALLY-RESOLVED-REMAINDER-DISCLOSED',
  'The dead parameter is gone: ts_pilot.py.patch replaces programEntry=program_entry with an '
  'explicit None carrying the U-1 reason, and the helper is renamed _default_unit_binding. A '
  'non-default binding now exists and replays: ts-lawful-explicit-selection, structural ADMIT and '
  'semantic ADMIT with a distinct runId.',
  'The second half — an additional-program binding distinct from the default-unit one — is NOT '
  'delivered. The author attempted it at construction time and recorded the ordered owner refusals '
  '(ENUMERATION_BINDING_DUPLICATE_UNIVERSE + ENUMERATION_INVENTORY_MISSING_RECORD, then '
  'NATIVE_UNIVERSE_BINDING:native.universe-path-not-inventoried). I accept that account as an '
  'evidence limit, not as a demonstrated owner defect: every refusal is a published obligation '
  'enforced against an incomplete construction. AR-01 Q3 therefore still cannot be answered from '
  'this package, and the shipped control is correctly never described as two bindings.')
f('F-07', 'minor', 'control coverage / AR-02 predicate algebra', 'RESOLVED-BY-DISCLOSURE',
  'F-07 permitted either new combinator Runs or a plain statement that the paths are unexercised. '
  'README:9 states it directly and the remint review re-measures it on the new exports. I confirmed '
  'independently: evaluator.py still raises NotImplementedError at both atom ops, and no and/or/not '
  'node occurs in the shipped evidence.',
  'The predicate algebra remains exercised for 2 of 4 atom ops and 0 of 3 combinators. '
  'count-at-most and all-covered are unimplemented in the partial helper. This bounds what the '
  'seven Runs evidence, and I weight them accordingly.')
f('F-08', 'minor', 'property evidence under-determines its claim', 'RESOLVED',
  'author-properties.json now publishes selectedUnitIds, selectedUnits, sourceUnitOwnershipId and '
  'measuredBodyOwner with effectiveEdition and an explicit editionBasis; the pre-remedy file is '
  'retained beside it as author-properties.before-f8.json and carries none of them. '
  'check-author-properties.py now asserts the effective-edition change and stability, and I ran it '
  'myself: passed, with the checks naming "same physical body under different selected target '
  'editions changes body identity" and "selection change preserving effective edition changes '
  'universe but preserves body identity". The claim is now establishable from the published file.')
f('F-09', 'minor', 'citation accuracy / AR-06', 'RESOLVED',
  'I verified the clause myself rather than accepting the correction. '
  'EXECUTION_INPUTS_COVERAGE_DERIVE is raised only inside load_coverage and partitions_in_cell — '
  'coverage-account derivation — and execution-inputs-contract.v1.md §5 is "Native Coverage accounts '
  '(derived)" while §3 is "Stage ordinal and receipts". The corrected §5 citation is right and the '
  'original §3 citation was wrong. I also reproduced the refusal: unmerged view ADMIT/ADMIT, merged '
  'view structural ADMIT then REFUSE EVALUATOR_EXECUTION_INPUTS_JOIN:EXECUTION_INPUTS_COVERAGE_DERIVE.')
f('F-10', 'minor', 'reproducibility / helper portability', 'RESOLVED',
  'author_portable.py replaces all three historical dependencies with declared arguments and bundles '
  'the helpers and the transport. I proved it by execution rather than by reading: I ran all five '
  'builders from scratch in a fresh arbitrary directory (/tmp/indep27-arbitrary-*/deep/nested/'
  'elsewhere) with only --source, --package, --out and --positive, and all five succeeded with runIds '
  'identical to the shipped claims everywhere. Notably I passed NO --helpers overlay, which retires '
  'the remint review\'s own caveat that the README limitation could only be retired if the overlay '
  'were merged with the entry points: in this successor it is merged.',
  'Fresh builds differ from the shipped exports by exactly one unreferenced retained blob per store '
  '(the target-attribution.schema.v2.json document itself, which changed in 27). I proved that blob '
  'inert by mutual replay — each build passes close_run while lacking the other\'s copy — and '
  'objectTable, frames, meta and every RunId are identical. I repaired no export.')
f('F-11', 'info', 'fixture hygiene: vacuous self-comparison', 'RESOLVED',
  'runs.py.patch replaces compare_proof(proof, proof) with constructionProofSource. I measured the '
  'shipped helper: zero occurrences of the self-comparison pattern remain.')
f('F-12', 'info', 'evidential weighting / AR-04', 'RESOLVED',
  'README:9 now states the per-group weighting explicitly — checkpoint3 compares the author helper '
  'with the reference owner, and the other six have the owner both derive and replay the proof, '
  'establishing self-consistency. The remint review §3 repeats it and adds that the three negatives '
  'derive from checkpoint3. My own replay agrees with that division, and I weight the six '
  'owner-derived Runs as determinism and self-consistency evidence, never as two-implementation '
  'agreement.')
f('F-13', 'minor', 'AR-07 residual concentration', 'RESOLVED',
  'evaluation-residual-author-assessment.json now carries sharedReviewDependencies with TCB-SCOPE-01, '
  'its assumption, its consequence ("rejecting or changing this one assumption reopens all thirteen '
  'named residual accounts together") and the explicit list of 13 dependent ids. I did not take that '
  'list on trust: I classified all 30 rows myself. My keyword pass flagged 14 and disagreed on three '
  'rows, so I read those three in full. RES-EP13-13 does depend on the move (its disposition is '
  '"fixture isolation only, no process isolation against hostile Python"); IR-EP13-NB-02 and '
  'IR-EP13-NB-06 do not — their dispositions ("a grep is not a security guarantee", "a parity rule '
  'imposes cost without closing the class") hold wherever the TCB line is drawn, and my classifier '
  'had matched a shared evidence-scope label rather than their reasoning. Read row by row, the '
  'declared 13 is exactly right.')
f('F-14', 'info', 'AR-07 self-assessment signal', 'ACKNOWLEDGED-NO-CORRECTION-REQUIRED',
  'I re-measured: all 30 rows still carry the identical verdict '
  'proposed-account-supported-with-stated-limits, with 30 distinct rationales and 30 distinct limits. '
  'F-14 asked for no correction, only that uniformity not be read as corroboration. I grade no row '
  'from that self-assessment; every one of my 30 dispositions below rests on frozen bytes I read or '
  'executed.')
R['fDispositions'] = F
R['fDispositionSource'] = {
    'requestedPath': '/tmp/opensip-design-corrections/claude-author-package-review.v1/review.json',
    'pathExists': False,
    'actualSource': 'claude-author-package-review.v1/review.md, embedded JSON block at $.report.findings',
    'reviewMdSha256': rec('pI3-findingsF.json')['reviewMdSha256'],
    'idSpelling': 'F-01..F-14 (hyphenated), not F01..F14',
    'note': ('The named review.json is absent from that directory; it holds review.md plus session '
             'metadata (result.json), input-manifest.json, public-events.jsonl, prompt.md, '
             'verification.json, process.json and scratch/. The instruction authorised authored prose '
             'as a fallback, and all 14 rows were recovered complete with severity, area, path, '
             'selector, claim, evidence, impact and requestedCorrection.'),
    'rowsRecovered': 14}

json.dump(R, open(os.path.join(BASE, 'review.part1.json'), 'w'), indent=1)
print('part1 keys:', list(R))
print('F rows:', len(F))
