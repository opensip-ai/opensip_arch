"""review.json part 2 — carry all 107 baseline rows forward with current33 status, owner arrays
derived from the v32/v33 manifests, and the changed-owner rows individually reassessed."""
import json, os

BASE = '/tmp/opensip-design-corrections/claude-independent-design.v33'
REC = os.path.join(BASE, 'receipts')
REV = '/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews'
B = json.load(open('/tmp/opensip-design-corrections/claude-independent32-reconciliation.v2/review.json'))
m32 = {f['path']: f['sha256'] for f in json.load(open(os.path.join(REV, 'candidate-subject.v32.json')))['files']}
m33 = {f['path']: f['sha256'] for f in json.load(open(os.path.join(REV, 'candidate-subject.v33.json')))['files']}
O = {}

C = 'docs/v2/contracts/product-v1/'
F = 'docs/coop/design-corrections/foundation/'
EXECC, EXECS, EXECM = F + 'execution-inputs-contract.v1.md', F + 'execution-inputs.schema.v1.json', F + 'execution_inputs_model.v1.py'
COMP, ENUMC = F + 'evaluator-composition-contract.v3.md', F + 'enumeration-contract.v1.md'
NATIVE = C + 'native-evidence.md'

# rows whose owner set gains a changed-in-33 owner, with an individually reasoned current status
REASSESSED = {
    'AR-07': ([C + 'native-evidence.md'],
              'Sealed Rust dependencies and authorized preparation unchanged in substance; the native '
              'chapter changed +1175 bytes and is the one repin in layer4. I read the changed region: '
              'it aligns the native text with the execution-inputs account law and adds no new native '
              'obligation. check_native_evidence.v2.py passes 375/375 on 33.'),
    'AR-12': ([C + 'native-evidence.md', 'docs/coop/design-corrections/native/native-evidence.schemas.v2.json'],
              'Resolution-complete authoritative negative provenance is strengthened on 33: the native '
              'chapter now agrees with execution-inputs §5 that a selected-U UNSUPPORTED-TYPED cell is '
              'answered with its own matrix deficiency and cause rather than a hardcoded '
              'capability-missing, and that account completeness is EXTRACTION completeness, so RC-1 '
              'not-applicable and RC-3 complete-with-unresolved stay lawful. The native schema file '
              'itself is unchanged in my 32->33 delta.'),
    'AR-16': ([C + 'workflows-and-surfaces.md', C + 'native-evidence.md', COMP],
              'Provenance-specific remedies and exact outcomes are strengthened on 33 by the '
              'required-execution bridge: a required cell whose incompleteness is pure missing work now '
              'bridges to required-cell-unsatisfied carrying {XI} plus each originating Coverage, '
              'inventory or candidate ref, so a remedy names the actual originating record instead of '
              'a manufactured provider observation.'),
    'FW-03': ([C + 'native-evidence.md'],
              'Native semantics unchanged in substance on 33; the native chapter edit is the '
              'execution-account alignment described under AR-12, and no provider is measured.'),
    'FW-06': ([C + 'identity-and-evidence.md', COMP, F + 'identity-model.v3.py', F + 'identity-schemas.v3.json'],
              'Determinism is strengthened on 33. The composition contract changed to remove a '
              'prescribed provider-unavailable fallback that contradicted execution-inputs, and the '
              'derived carrier is now a published deterministic selection: returned partitions in '
              'canonical H order, then named-but-not-returned Coverage, pair taken WHOLE from the first '
              'record that carries one. check-identity passes 1596/1596 and check-replay passes on 33.'),
    'FW-08': ([C + 'native-evidence.md', C + 'workflows-and-surfaces.md', EXECC],
              'Omissions are handled more precisely on 33: a missing partition or a missing expected '
              'subject is census-driven incompleteness that mints NO new vocabulary member and carries '
              '(null, null), while the account stays incomplete and the cell stays partial. Both the '
              'missing-partition and missing-subject cases are governed by one paragraph.'),
    'FW-10': ([C + 'workflows-and-surfaces.md', 'docs/coop/design-corrections/workflows/repair_closed_world_selection.v1.py'],
              'Repair evidence is unchanged on 33; neither the repair module nor the workflows chapter '
              'is in my 32->33 delta. The A-9 admitted-versus-unit limitations are retained exactly.'),
}
INH_REASSESSED = {
    'DR-004': ([C + 'identity-and-evidence.md', C + 'native-evidence.md'],
               'Provider truth remains trusted extraction evidence on 33, and the new law makes that '
               'sharper: no host may manufacture a provider observation that occurs on no source record.'),
    'DR-007': ([C + 'workflows-and-surfaces.md', C + 'native-evidence.md', F + 'evaluator-fault-contract.v3.md'],
               'Exact D9 branch/cause/result behaviour is unchanged on 33. The owning fault contract '
               'evaluator-fault-contract.v3.md is not in my 32->33 delta; the native chapter is. The '
               'published D9 successor carrying host-invariant remains an ASSIGNED implementation '
               'obligation, carried forward and not closed by this review.'),
    'DR-011-R01': (['docs/coop/design-corrections/native/native-evidence.schemas.v2.json',
                    C + 'native-evidence.md', F + 'identity-schemas.v3.json'],
                   'FACT-PLANE. CoverageResultV3 with RC-0..RC-6 is unchanged on 33, and the execution '
                   'law now states explicitly that account complete is EXTRACTION completeness so RC-1 '
                   'and RC-3 stay lawful rather than being forced to complete.'),
    'DR-011-R12': ([C + 'admission-and-qualification.md',
                    'docs/coop/design-corrections/evaluation-residual-dispositions.proposed.json'],
                   'EVALUATION PROOF. Unchanged on 33. All 30 nested residuals carry individual '
                   'dispositions below and remain author proposals PENDING independent grading, with '
                   'TCB-SCOPE-01 assessed once over 13 of them.'),
}

MAPS = ('arDispositions', 'fwDispositions', 'inheritedResidualDispositions',
        'scopedReviewOwnerDispositions')
audit = {'rows': 0, 'rowsWithChangedOwner': [], 'unresolved': []}
for mp in MAPS:
    out = {}
    for rid, row in B[mp].items():
        r = dict(row)
        owners = list(r.get('currentOwnerFiles', []))
        spec = REASSESSED.get(rid) or INH_REASSESSED.get(rid)
        if spec:
            for p in spec[0]:
                if p not in owners:
                    owners.append(p)
        r['currentOwnerFiles'] = owners
        ch = sorted(p for p in owners if m32.get(p) != m33.get(p))
        un = sorted(p for p in owners if m32.get(p) == m33.get(p))
        miss = [p for p in owners if p not in m33]
        r['ownerFilesChangedIn32to33'] = ch
        r['ownerFilesUnchangedIn32to33'] = un
        r['ownerPathsResolveInFrozen33'] = not miss
        r['ownerArraysDerivedFromManifestHashes'] = True
        for k in ('ownerFilesChangedIn31to32', 'ownerFilesUnchangedIn31to32',
                  'ownerPathsResolveInFrozen32'):
            r.pop(k, None)
        prior = r.pop('currentStatusOn32', None)
        if spec:
            r['currentStatusOn33'] = spec[1]
            r['readingStanding'] = 'changed owner regions read in this source33 session'
            audit['rowsWithChangedOwner'].append(mp + '/' + rid)
        else:
            r['currentStatusOn33'] = (
                'Unchanged on 33: none of this row\'s owner files is in my derived 32->33 delta, so my '
                'source32 assessment stands on the reading I completed then. ' + (prior or ''))
            r['readingStanding'] = ('inherited from my source32 review after exact-byte verification '
                                    'that these owner files are unchanged in the 32->33 delta')
        r['priorStatusOn32'] = prior
        r['appliedByThisReview'] = False
        r['finalApplicationOutcomeGranted'] = False
        if miss:
            audit['unresolved'].append({'row': mp + '/' + rid, 'missing': miss})
        audit['rows'] += 1
        out[rid] = r
    O[mp] = out

# evaluation residuals
ev = {}
for rid, row in B['evaluationResidualDispositions'].items():
    r = dict(row)
    sel = r.get('currentOwnerSelectors', [])
    miss = [p for p in sel if p not in m33]
    ch = sorted(p for p in sel if m32.get(p) != m33.get(p))
    r['ownerSelectorsResolveInFrozen33'] = not miss
    r['ownerSelectorsChangedIn32to33'] = ch
    prior = r.pop('currentStatusOn32', None)
    r['currentStatusOn33'] = (('Cited owner bytes CHANGED in 32->33 (%s); re-read this session. ' % ch)
                              if ch else 'Cited owner bytes unchanged in 32->33. ') + (prior or '')
    r['priorStatusOn32'] = prior
    r['readingStanding'] = ('changed cited owner re-read this session' if ch else
                            'inherited after exact-byte verification that the cited owner is unchanged')
    r['reviewStatus'] = 'PENDING'
    r['independentGradeAwardedHere'] = None
    r['appliedByThisReview'] = False
    r['finalApplicationOutcomeGranted'] = False
    audit['rows'] += 1
    if miss:
        audit['unresolved'].append({'row': 'evaluationResidualDispositions/' + rid, 'missing': miss})
    ev[rid] = r
O['evaluationResidualDispositions'] = ev

# F rows
fd = {}
for rid, row in B['fDispositions'].items():
    r = dict(row)
    prior = r.pop('dispositionOn32', None)
    prior_basis = r.pop('currentBasisOn32', None)
    r['dispositionOn33'] = prior
    r['currentBasisOn33'] = (
        'Unchanged on 33: nothing in my derived 32->33 delta touches this row\'s subject. ' +
        (prior_basis or ''))
    r['priorBasisOn32'] = prior_basis
    r['appliedByThisReview'] = False
    r['finalApplicationOutcomeGranted'] = False
    audit['rows'] += 1
    fd[rid] = r
# the package-dependent F rows must record the incomplete package review
p11 = json.load(open(os.path.join(REC, 'p11-package.json')))
for rid in ('F-01', 'F-02', 'F-03', 'F-05', 'F-06', 'F-08', 'F-10', 'F-11', 'F-12'):
    fd[rid]['dispositionOn33'] = 'PACKAGE-EVIDENCE-REVIEW-INCOMPLETE-ON-33'
    fd[rid]['currentBasisOn33'] = (
        'This row rests on author package evidence. The root-owned author-package-update.json is still '
        'PENDING and names no package10 manifest or root verification, so I have NOT verified a '
        'source33-bound package and record this row INCOMPLETE rather than carrying the source32 '
        'result forward as if current. Package9 was rebound rather than constructed on 33 and its '
        'actual current verification FAILED on three positive cases; I assessed those preserved '
        'receipts and did not rerun them. ' + (fd[rid].get('priorBasisOn32') or ''))
O['fDispositions'] = fd
O['rowAudit'] = audit
json.dump(O, open(os.path.join(BASE, 'part2.json'), 'w'), indent=1, default=str)
for k in ('fDispositions', 'evaluationResidualDispositions', 'arDispositions', 'fwDispositions',
          'inheritedResidualDispositions', 'scopedReviewOwnerDispositions'):
    print('%-34s %d' % (k, len(O[k])))
print('rows processed:', audit['rows'])
print('rows with a changed owner:', audit['rowsWithChangedOwner'])
print('unresolved owner paths:', audit['unresolved'])
