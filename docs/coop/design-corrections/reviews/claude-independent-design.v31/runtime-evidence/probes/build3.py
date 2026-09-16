"""review.json part 3 — 14 F rows, and the 16 AR / 15 FW / 27 inherited / 5 scoped maps re-decided
for source31 with CURRENT scope text and real file-path change accounting (RR27-02 and RR27-03)."""
import json, os

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v31'
REC = os.path.join(BASE, 'receipts')
V27 = json.load(open('/tmp/opensip-design-corrections/claude-independent-design.v27/review.json'))
p01 = json.load(open(os.path.join(REC, 'p01-delta.json')))
CHANGED = {c['path'] for c in p01['cumulative']['changed']} | {a['path'] for a in p01['cumulative']['added']}
p12 = json.load(open(os.path.join(REC, 'p12-enumcontrols.json')))
p14 = json.load(open(os.path.join(REC, 'p14-exports.json')))
p15 = json.load(open(os.path.join(REC, 'p15-portable31.json')))
p16 = json.load(open(os.path.join(REC, 'p16-verifypkg.json')))
p17 = json.load(open(os.path.join(REC, 'p17-propmixed.json')))
p18b = json.load(open(os.path.join(REC, 'p18b-f09enclosure.json')))
O = {}

# ---------------- owner file maps, by ACTUAL path ----------------
CONTRACT = 'docs/v2/contracts/product-v1/'
FOUND = 'docs/coop/design-corrections/foundation/'
NAT = 'docs/coop/design-corrections/native/'
SEC = 'docs/coop/design-corrections/security/'
WF = 'docs/coop/design-corrections/workflows/'
ARCH = 'docs/v2/architecture/'

OWNERS = {
    'AR-01': [CONTRACT + 'admission-and-qualification.md', FOUND + 'canonical.py',
              CONTRACT + 'identity-and-evidence.md'],
    'AR-02': [CONTRACT + 'admission-and-qualification.md'],
    'AR-03': [CONTRACT + 'security-and-lifecycle.md'],
    'AR-04': [CONTRACT + 'security-and-lifecycle.md'],
    'AR-05': [CONTRACT + 'security-and-lifecycle.md'],
    'AR-06': [CONTRACT + 'security-and-lifecycle.md', SEC + 'carrier-format.v3.md'],
    'AR-07': [CONTRACT + 'native-evidence.md'],
    'AR-08': [CONTRACT + 'workflows-and-surfaces.md'],
    'AR-09': [CONTRACT + 'identity-and-evidence.md', FOUND + 'identity-schemas.v3.json'],
    'AR-10': [CONTRACT + 'workflows-and-surfaces.md', CONTRACT + 'security-and-lifecycle.md'],
    'AR-11': [CONTRACT + 'workflows-and-surfaces.md'],
    'AR-12': [CONTRACT + 'native-evidence.md', NAT + 'native-evidence.schemas.v2.json'],
    'AR-13': [CONTRACT + 'native-evidence.md', CONTRACT + 'workflows-and-surfaces.md'],
    'AR-14': [CONTRACT + 'security-and-lifecycle.md', SEC + 'carrier-format.v3.md',
              SEC + 'carrier-migration.v1.md', SEC + 'carrier-dispatch.v3.json'],
    'AR-15': [CONTRACT + 'README.md', 'docs/coop/design-corrections/current-source-map.proposed.md',
              ARCH + 'report-asset-binding.v1.json'],
    'AR-16': [CONTRACT + 'workflows-and-surfaces.md', CONTRACT + 'native-evidence.md'],
    'FW-01': [CONTRACT + 'security-and-lifecycle.md', CONTRACT + 'native-evidence.md',
              CONTRACT + 'admission-and-qualification.md', CONTRACT + 'workflows-and-surfaces.md'],
    'FW-02': [CONTRACT + 'native-evidence.md', CONTRACT + 'identity-and-evidence.md'],
    'FW-03': [CONTRACT + 'native-evidence.md'],
    'FW-04': [CONTRACT + 'workflows-and-surfaces.md', CONTRACT + 'native-evidence.md'],
    'FW-05': [CONTRACT + 'workflows-and-surfaces.md'],
    'FW-06': [CONTRACT + 'identity-and-evidence.md', FOUND + 'evaluator-composition-contract.v3.md',
              FOUND + 'identity-model.v3.py', FOUND + 'identity-schemas.v3.json'],
    'FW-07': [CONTRACT + 'workflows-and-surfaces.md'],
    'FW-08': [CONTRACT + 'native-evidence.md', CONTRACT + 'workflows-and-surfaces.md'],
    'FW-09': [CONTRACT + 'workflows-and-surfaces.md'],
    'FW-10': [CONTRACT + 'workflows-and-surfaces.md', CONTRACT + 'native-evidence.md',
              CONTRACT + 'security-and-lifecycle.md'],
    'FW-11': [CONTRACT + 'workflows-and-surfaces.md'],
    'FW-12': [CONTRACT + 'workflows-and-surfaces.md'],
    'FW-13': [CONTRACT + 'workflows-and-surfaces.md', WF + 'command-inventory.v3.json'],
    'FW-14': ['docs/coop/design-corrections/current-source-map.proposed.md'],
    'FW-15': [CONTRACT + 'workflows-and-surfaces.md'],
}
DEFAULT_OWNERS = {
    'DR-001': ['docs/coop/design-corrections/current-source-map.proposed.md',
               CONTRACT + 'README.md', ARCH + 'report-asset-binding.v1.json'],
    'DR-002': [CONTRACT + 'identity-and-evidence.md'],
    'DR-003': [CONTRACT + 'security-and-lifecycle.md', CONTRACT + 'identity-and-evidence.md'],
    'DR-004': [CONTRACT + 'identity-and-evidence.md', CONTRACT + 'native-evidence.md'],
    'DR-005': [CONTRACT + 'identity-and-evidence.md', ARCH + 'commit-recovery-plan.v1.json'],
    'DR-006': [CONTRACT + 'identity-and-evidence.md', FOUND + 'identity-schemas.v3.json'],
    'DR-007': [CONTRACT + 'workflows-and-surfaces.md', CONTRACT + 'native-evidence.md'],
    'DR-008': [CONTRACT + 'identity-and-evidence.md', CONTRACT + 'admission-and-qualification.md'],
    'DR-009': [CONTRACT + 'identity-and-evidence.md'],
    'DR-010': [CONTRACT + 'admission-and-qualification.md'],
    'DR-011': ['docs/coop/design-corrections/inherited-residuals.proposed.md',
               'docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json'],
}

# ---------------- F rows ----------------
F27 = V27['fDispositions']
FNOW = {}


def f(fid, status, current, limits=None):
    FNOW[fid] = {'severity': F27[fid]['severity'], 'area': F27[fid]['area'],
                 'v27Disposition': F27[fid]['disposition'],
                 'dispositionOn31': status, 'currentBasisOn31': current,
                 'appliedByThisReview': False, 'finalApplicationOutcomeGranted': False}
    if limits:
        FNOW[fid]['limits'] = limits


f('F-01', 'RESOLVED-AND-STILL-HOLDS',
  'historical-consumer-custody/original-requirements.json is a member of package7 and I verified all '
  '270 members hash-match. The 123/8/3 charter handoff is carried forward unchanged with '
  'independentAcceptance false.',
  'Charter custody only; the blind charter itself remains a separate uninfluenced requirement.')
f('F-02', 'RESOLVED-AND-STILL-HOLDS',
  'The consumer-b.v13 v6/v7 assessment artifacts remain frozen in package7 under '
  'historical-consumer-custody with their attachment manifest; all package members verified 270/270.',
  'Preserved historical files still contain live working-path strings as provenance, not as authority.')
f('F-03', 'RESOLVED-AND-STRENGTHENED',
  'The query checks are not merely regenerable now, they are part of package verification: '
  'verify-package.py runs check-author-query.py and assess-author-query.py after the 13 Run outcomes '
  'and asserts all seven. I executed it against frozen source31 and regenerated all eight query '
  'outputs byte-identical to the retained copies.')
f('F-04', 'RESOLVED-AND-NOW-CONTROLLED',
  'The internal-root law is unchanged on 31 and is now exercised by check-enumeration.v1.py. My own '
  'guard-omission mutation reproduces the ORIGINAL F-04 defect exactly: the two project-root cases '
  'refuse with ENUMERATION_BINDING_PROGRAM_ENTRY and the two member-root cases silently ADMIT.',
  'The controls are JOIN controls, not a whole Run; that is the correct shape for this boundary.')
f('F-05', 'RESOLVED-AND-STILL-HOLDS',
  'ts-invalid-default-entry replays on 31 as structural ADMIT then semantic REFUSE '
  'EVALUATOR_ENUMERATION_JOIN:ENUMERATION_BINDING_PROGRAM_ENTRY, verified by my own decoder against '
  'the snapshot31 owner.')
f('F-06', 'PARTIALLY-RESOLVED-REMAINDER-STILL-AN-EVIDENCE-LIMIT',
  'The dead parameter is gone and ts-lawful-explicit-selection admits on 31 with a distinct runId. '
  'The second binding is still not constructed.',
  'The two-binding construction remains incomplete and the shipped control is single-explicit only. '
  'I accept that as an evidence limit, not a demonstrated owner defect, so AR-01 Q3 still cannot be '
  'answered from this package.')
f('F-07', 'RESOLVED-BY-DISCLOSURE-STILL-ACCURATE',
  'Re-measured on 31: the seven positives exercise exists and none only; and/or/not appear nowhere '
  'and count-at-most/all-covered remain NotImplementedError in the partial helper. The README states '
  'this plainly.',
  'The predicate algebra is exercised for 2 of 4 atom ops and 0 of 3 combinators, which bounds what '
  'the seven Runs evidence.')
f('F-08', 'RESOLVED-AND-STILL-HOLDS',
  'check-author-properties.py passes on source31 with six checks including both effective-edition '
  'assertions - body identity changes under different selected editions, and is preserved when a '
  'selection change keeps the effective edition.')
f('F-09', 'RESOLVED-WITH-MY-EVIDENCE-CLAIM-CORRECTED',
  'The citation itself was and remains right: execution-inputs-contract.v1.md section 5 is "Native '
  'Coverage accounts (derived)" and I reproduced the refusal on 31 (unmerged view ADMIT/ADMIT, merged '
  'view structural ADMIT then REFUSE EVALUATOR_EXECUTION_INPUTS_JOIN:EXECUTION_INPUTS_COVERAGE_DERIVE). '
  'My v27 EVIDENCE sentence was wrong and is corrected here: by AST enclosure, 1 of the 7 raise sites '
  'is inside load_coverage, 6 are directly in the coverage-account loop of admit_execution_inputs, and '
  'partitions_in_cell contains none.',
  'See correctionsToMyOwnV27Record RR27-01.')
f('F-10', 'RESOLVED-AND-STRENGTHENED',
  'I rebuilt all five constructor groups from scratch against frozen source31 in a fresh arbitrary '
  'directory with only --source/--package/--out (plus --positive), no helper overlay, and ALL 13 '
  'store files came out byte-identical to the preserved package exports with identical runIds.',
  'The v27 "one differing unreferenced blob per store" limitation is gone; I measured current equality '
  'rather than assuming it. construction-provenance.json differs by design because it records my paths.')
f('F-11', 'RESOLVED-AND-STILL-HOLDS',
  'runs.py still carries constructionProofSource in place of the vacuous self-comparison; no '
  'compare_proof(proof, proof) pattern remains in the shipped helper.')
f('F-12', 'RESOLVED-AND-STILL-ACCURATE',
  'The per-group weighting is restated in the package README and holds on my own replay: only TS '
  'checkpoint3 is helper-versus-owner agreement; the other six are owner-derived and owner-replayed '
  'self-consistency, and the three negatives derive from checkpoint3.',
  'I weight the six owner-derived Runs as determinism and self-consistency, never as '
  'two-implementation agreement.')
f('F-13', 'RESOLVED-AND-REVERIFIED',
  'sharedReviewDependencies still declares TCB-SCOPE-01 with its assumption, consequence and exactly '
  '13 dependent ids. I re-decided the set on current bytes by reading each row and the declared 13 is '
  'exactly right.')
f('F-14', 'ACKNOWLEDGED-INFORMATIONAL-NO-CHANGE-DEMANDED',
  'All 30 rows again carry the identical self-assessment verdict with distinct rationales and limits. '
  'F-14 asked for no correction, only that uniformity not be read as corroboration, and I demand no '
  'forced uniform-verdict fix.',
  'I grade no row from that self-assessment; every one of my 30 dispositions rests on frozen31 bytes.')
O['fDispositions'] = FNOW

# ---------------- the four carried maps ----------------
CUR = {
    'AR-01': ('Exact integer admission is unchanged on 31. Lexical admission precedes JSON decoding, '
              '1.0/1e0/-0/booleans/numeric strings refuse an integer field, and closed identifier and '
              'digest patterns use the portable end-of-input assertion.'),
    'AR-02': ('Authenticated qualification subject and independent verification are unchanged on 31 '
              'and remain measurement obligations no design document can discharge.'),
    'AR-03': ('Repository/config custody and discovery are unchanged on 31. The v27-era count '
              'sentences in S13 remain derived from the measured report rather than transcribed.'),
    'AR-04': 'Forward clock excursion and poisoned-floor rules are unchanged on 31.',
    'AR-05': 'Expired root continuity and live revocation are unchanged on 31.',
    'AR-06': ('Support population and multiple platform provenance are unchanged on 31, including the '
              'carrierFormat 3 correction and the evidence-custody/diagnosis-vocabulary paragraph.'),
    'AR-07': 'Sealed Rust dependencies and authorized preparation are unchanged on 31.',
    'AR-08': 'Invocation/attempt/step/Run and action lifecycle are unchanged on 31.',
    'AR-09': ('Identity/proof/custody/retention closure is specified and, on 31, the closing digest '
              'law is scoped to bare 64-hex digest fields with machine-readable selectors. No '
              'precision defect from my earlier reviews is open against this owner.'),
    'AR-10': 'Runnable prior detector and portable baseline are unchanged on 31.',
    'AR-11': 'Typed delta attribution and admitted imported evidence are unchanged on 31.',
    'AR-12': ('Resolution-complete authoritative negative provenance is unchanged in prose on 31; its '
              'native schema owner changed at 29 only to define the `derived` retention, add the '
              'measured siteCountLaw and re-indent, which I verified does not alter this obligation.'),
    'AR-13': 'TS/JS/Rust native cells, monorepos and output handling are unchanged on 31.',
    'AR-14': ('Core/state/trust migration and concurrent operation are specified on 31, with the '
              'inherited-migration scoping and the read-only recovery diagnosis vocabulary in place. '
              'No precision defect from my earlier reviews is open against this owner.'),
    'AR-15': ('One effective current narrative and obligation map. On 31 the report-asset anchors are '
              'unambiguous (14 anchors, no duplicate id) and the current source map is present. No '
              'precision defect from my earlier reviews is open against this owner.'),
    'AR-16': ('Provenance-specific remedies and exact outcomes are unchanged on 31; the case and sweep '
              'counts remain derived from the measured report.'),
    'FW-01': 'zero-config/recommend is unchanged on 31.',
    'FW-02': 'clones is unchanged on 31.',
    'FW-03': 'native semantics is unchanged in prose on 31; see AR-12 on the schema owner.',
    'FW-04': 'richer evidence is unchanged on 31.',
    'FW-05': 'delta gate is unchanged on 31.',
    'FW-06': ('Determinism. On 31 this obligation is stronger than at 27: the reference ordered() now '
              'implements the explicit ruleResults key order, so the reference and the published '
              'schema/composition law agree, and I verified that BOTH explicit key orders in the '
              'bundle are implemented with none left to the generic order. No determinacy defect from '
              'my earlier reviews is open against this owner.'),
    'FW-07': 'coherent workflow is unchanged on 31.',
    'FW-08': 'omissions is unchanged on 31.',
    'FW-09': 'candidate -> inspect -> review is unchanged on 31.',
    'FW-10': 'repair evidence is unchanged on 31.',
    'FW-11': 'weakened safeguards / metric redistribution is unchanged on 31.',
    'FW-12': 'bounded review is unchanged on 31.',
    'FW-13': 'common registry is unchanged on 31.',
    'FW-14': 'real configuration corpus remains an implementation-qualification obligation on 31.',
    'FW-15': 'policy authoring/test is unchanged on 31.',
}
INH = {
    'DR-001': ('A current source/selector/claim map exists on 31 and each historical misleading '
               'selector has a prospective account. No precision defect from my earlier reviews is '
               'open against this obligation.'),
    'DR-002': 'Identity sections 2-5 are unchanged on 31.',
    'DR-003': 'Unperformed by design on 31 and correctly not claimed.',
    'DR-004': 'Provider truth remains trusted extraction evidence on 31.',
    'DR-005': 'All 54 commit-recovery cases are unexecuted on 31; native carrier qualification is separately required.',
    'DR-006': ('The closure law and its digest-domain registry are unchanged on 31, with the scope '
               'statement carrying machine-readable selectors. No precision defect from my earlier '
               'reviews is open against this obligation.'),
    'DR-007': ('Exact D9 branch/cause/result behaviour is unchanged on 31. The successor D9 artifact '
               'carrying host-invariant remains a disclosed, attributed implementation obligation of '
               'the D9 unit, carried forward by this review and not closed.'),
    'DR-008': 'No store exists on 31; the retention obligation is design law only.',
    'DR-009': ('Reproducibility across machines. On 31 the reference ordering law is aligned with the '
               'published schema/composition order, which removes the divergence class this row is '
               'about; see FW-06. No defect from my earlier reviews is open here.'),
    'DR-010': 'The seven boundary items of admission section 5 are unchanged on 31.',
    'DR-011': ('inherited-residuals.proposed.md and evaluation-residual-dispositions.proposed.json are '
               'both unchanged on 31; all 30 nested residuals are disposed individually below.'),
}
for i in range(1, 17):
    INH.setdefault('DR-011-R%02d' % i, None)
SPECIFIC_R = {
    'DR-011-R01': 'FACT-PLANE joins are unchanged on 31; no provider is measured.',
    'DR-011-R06': 'Applied v15 stays applied on 31 and its rejected validator is not elevated.',
    'DR-011-R08': ('D9. Closed host-owned termination with its observation-to-faultCause mapping is '
                   'unchanged on 31. The successor D9 artifact carrying host-invariant remains a '
                   'disclosed, attributed implementation obligation, carried forward not closed.'),
    'DR-011-R10': ('Blind consumer-B. Closable only by an actual fresh implementer litmus, which this '
                   'review is explicitly not. The separate blind original 123/8/3 charter remains '
                   'required and uninfluenced: I did not read or touch any blind runtime, report or '
                   'output, and I claim no blind acceptance.'),
    'DR-011-R11': 'Remains an implementation-qualification obligation on 31.',
    'DR-011-R12': ('EVALUATION PROOF. Product proof/evidence/seal plus authenticated trusted evaluator '
                   'replay replace the v8/v13 lineages. All 30 nested residuals carry individual '
                   'dispositions below, with TCB-SCOPE-01 assessed once over 13 of them.'),
}

O['arDispositions'] = {}
O['fwDispositions'] = {}
O['inheritedResidualDispositions'] = {}
O['scopedReviewOwnerDispositions'] = {}


def carry(mapname, target, curmap, ownermap):
    for rid, old in V27[mapname].items():
        owners = ownermap.get(rid) or OWNERS.get(rid) or DEFAULT_OWNERS.get(rid) or []
        changed = sorted(p for p in owners if p in CHANGED)
        row = {k: old[k] for k in ('unit', 'obligation', 'constraint', 'topic', 'review',
                                   'inheritedFinding', 'owner') if k in old}
        row['disposition'] = old['disposition']
        row['currentOwnerFiles'] = owners
        row['ownerFilesChangedIn27to31'] = changed
        row['ownerFilesUnchangedIn27to31'] = [p for p in owners if p not in CHANGED]
        row['currentScopeOn31'] = curmap.get(rid) or SPECIFIC_R.get(rid) or (
            'Unchanged on 31: none of this row\'s owner files is in my 27->31 delta, so my v27 reading '
            'of the same bytes stands and is inherited here rather than re-read.')
        row['historicalNote'] = (
            'My source26 review raised issues against some of these owners; every one of them was '
            'resolved in source27 and none is an open condition of source31. That history is recorded '
            'here and deliberately kept out of the current scope field.'
            if old.get('v26IssuesNowResolved') else None)
        row['v26IssuesResolvedInSource27'] = old.get('v26IssuesNowResolved')
        row['readingStanding'] = ('inherited from my v27 complete reading, after exact-byte '
                                  'verification that these owner files are unchanged'
                                  if not changed else
                                  'changed owner files read in this session')
        row['appliedByThisReview'] = False
        row['finalApplicationOutcomeGranted'] = False
        target[rid] = row


carry('arDispositions', O['arDispositions'], CUR, OWNERS)
carry('fwDispositions', O['fwDispositions'], CUR, OWNERS)
carry('inheritedResidualDispositions', O['inheritedResidualDispositions'], INH, DEFAULT_OWNERS)

SCOPED = {
    'DR-201': ([  'docs/v2/contracts/product-v1/workflows-and-surfaces.md',
                  'docs/v2/contracts/product-v1/identity-and-evidence.md'],
               'Branch separation between the step DAG and the derivation DAG, Run-versus-command '
               'finalization, post-commit output failure and parked recipes is unchanged on 31.'),
    'DR-202': (['docs/v2/architecture/commit-recovery-plan.v1.json',
                'docs/v2/architecture/commit-recovery-readonly.v3.md',
                'docs/coop/design-corrections/security/carrier-format.v3.md',
                'docs/coop/design-corrections/security/carrier-dispatch.v3.json'],
               'Delivery/operations. None of these owner files is in my 27->31 delta, so they are '
               'unchanged across THIS delta. All 54 recovery cases remain unexecuted and every '
               'qualification gate remains unperformed.'),
    'DR-203': (['docs/v2/contracts/product-v1/workflows-and-surfaces.md'],
               'Prototype lessons routing is unchanged on 31.'),
    'DR-204': (['docs/v2/architecture/repository-file-inventory.v1.json',
                'docs/v2/architecture/implementation-coverage.v1.json',
                'docs/v2/architecture/implementation-normative-inputs.v2.json',
                'docs/v2/architecture/implementation-planning-sources.v1.json'],
               'V1/coop invariant coverage. Measured on frozen31: 12895 files and 736,536,507 bytes; '
               '198 planned paths across 20 packages in 46 directories with 9 pending decisions; 320 '
               'coverage mappings across 11 groups; M0-M6 milestone order; 54 recovery cases, 0 '
               'executed. The current architecture input layer is implementation-normative-inputs.v2 '
               'with 28 pins, every one resolving against frozen31, and the original v1 layer is '
               'preserved in the snapshot and named as previousArchitectureInputLayer. I read layer 2 '
               'completely via the Read tool in this session.'),
    'DR-205': (['docs/v2/architecture/repository-file-inventory.v1.json'],
               'Small-core/components routing is unchanged on 31.'),
}
for rid, old in V27['scopedReviewOwnerDispositions'].items():
    owners, cur = SCOPED[rid]
    changed = sorted(p for p in owners if p in CHANGED)
    O['scopedReviewOwnerDispositions'][rid] = {
        'review': old.get('review'), 'inheritedFinding': old.get('inheritedFinding'),
        'owner': old.get('owner'),
        'disposition': 'ROUTING-ASSESSED-ONLY-NOT-APPLIED',
        'currentOwnerFiles': owners,
        'ownerFilesChangedIn27to31': changed,
        'currentScopeOn31': cur,
        'readingStanding': ('inherited from my v27 complete reading, after exact-byte verification '
                            'that these owner files are unchanged' if not changed
                            else 'changed owner files read in this session'),
        'appliedByThisReview': False, 'finalApplicationOutcomeGranted': False}

json.dump(O, open(os.path.join(BASE, 'part3.json'), 'w'), indent=1)
for k in ('fDispositions', 'arDispositions', 'fwDispositions', 'inheritedResidualDispositions',
          'scopedReviewOwnerDispositions'):
    print('%-34s %d' % (k, len(O[k])))
chg = {k: v['ownerFilesChangedIn27to31'] for k, v in O['arDispositions'].items()
       if v['ownerFilesChangedIn27to31']}
print('AR rows with changed owner files:', chg)
print('FW rows with changed owner files:',
      {k: v['ownerFilesChangedIn27to31'] for k, v in O['fwDispositions'].items()
       if v['ownerFilesChangedIn27to31']})
