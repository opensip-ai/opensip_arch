"""INDEPENDENT derivation #3 -- ExecutionInputsV1 receipts, accounts, outcomes, typed causes.

Written from the published clauses first, and deliberately BLIND to two things the instruction
forbids using as the answer:

  * the evaluation seal / Run verdict (never read by this module), and
  * any general "this capability is available" notion.

Its inputs are only: the retained Plan and execution-plan, the EnumerationPlanV1 parameter, the
retained SubjectInventoryV1 set, the captured stage receipts and stage specs, the returned views /
subject-scopes / Coverage payloads, the admitted vcs-observation, and the published registries +
capability matrix. Everything else is derived here and then compared with the host's asserted row.

CLAUSE -> CODE MAP  (contract = execution-inputs-contract.v1.md, schema =
execution-inputs.schema.v1.json)

 X1 schema #/$defs/NativeCoverageAccountV1.applicability -- the LITERAL closed set
    {supported-available, unsupported-typed, unavailable-unselected, unavailable-null-universe,
    inapplicable-vcs}; its allOf pins coverageIds.maxItems=0 for the four non-supported kinds,
    and contract section 5 spells the same as "none" / "do not fabricate Coverage at null U".
      -> derive_account()
 X2 schema #/$defs/CellProgramOutcomeV1.allOf -- state=complete => deficiency null, nativeCause
    null, stageOrdinal INTEGER, stageOrdinalNullReason null; stageOrdinal null =>
    stageOrdinalNullReason a non-null string (enum unavailable-binding|optional-unselected).
      -> outcome_cross_field()
 X3 contract section 3 -- selected producer outputs (enumerator=selected, non-null U, derived
    state complete or partial): stageOrdinal NON-NULL matching a receipt; check enumerator
    closure (Plan-selected PROVIDER), stage-spec producerClosure, view planId, each named scope
    sourceUniverse vs binding U, and receipt outputDomains vs the stage. "Selected U cannot
    become complete by omitting the stage and views."
      -> stage_joins()
 X4 contract section 4 outcome table, row by row, plus the primary-pair law:
      enumerator unselected, or universe null                         -> unavailable
      selected U, typed provider-unavailable candidate/inventory,
        no returned work                                              -> unavailable
      any inventory partial, or any supported-available account
        not complete                                                  -> partial
      all inventories complete, every account complete/inapplicable/
        unsupported, candidate complete if owed                       -> complete
    "`complete` + partial inventory is EXECUTION_INPUTS_OUTCOME_DERIVE"; the row's
    deficiency/nativeCause EQUALS the derived primary pair (first retained source) and that pair
    must actually occur on a source record; "Host join requires the outcome pair to be a MEMBER
    of those source pairs"; "Unselected or universe=null DOES NOT DISCARD same-cell inventory
    items"; "Empty `kinds` is not complete-empty work".
      -> derive_outcome_state(), outcome_pair()
 X5 contract section 5 per-applicability envelopes and the per-universe attribution clause:
      supported-available  coverageIds EQUALS every matching returned partition for
                           (cell, program, relation, resolution, U, producer); empty ->
                           native-work-incomplete; mixed complete+unknown -> not complete;
                           EVERY resolved Coverage envelope's subject-scope sourceUniverse AND
                           every resolved payload key.sourceUniverse MUST equal U; and
                           independently every expected source subject of the relation's
                           subject-kind from this cell's inventory must be a member of some
                           returned partition -- "Missing expected subjects -> incomplete even
                           if the remaining Coverage is complete".
      unsupported-typed    none; the MATRIX cell deficiency and the cause-registry cause for
                           THAT deficiency (not a hardcoded capability-missing).
      unavailable-*        none.
      inapplicable-vcs     none; "admitted VCS observation kind=none is the basis".
    Section 5 also says explicitly that it does NOT constrain targetUniverse, so this module
    asserts nothing about it and records that silence.
      -> derive_account()
 X6 contract section 4/6 -- one outcome per (cellOrdinal, programOrdinal); inventory digests
    exactly one per kind, kinds set-equal to the cell with NO available-only qualifier;
    candidateResultRefs EQUALS the set of outcomes' non-null candidateResultDigest, each bound
    once; section 6 candidate custody (ids/paths/universe/contentSha256/byteLength/examinedPaths).
      -> outcome_inventories(), candidate_refs()
 X7 schema CellProgramOutcomeV1.viewDigests DESC -- "view2 H suffixes, never sha256(C(view)).
    Must equal captured receipt views attributed to this cell/program/U/producer."
      -> stage_joins()
 X8 contract section 1 -- receipts rooted in admitted execution-plan producer obligations: one
    receipt per stage, ordinals unique and TOTAL, outputDomains EQUAL the stage, outputRefs
    domains subset of those domains; optional unavailable stages carry typed state and a reason,
    never silent missing. selectedRefs is EXACT TOTALITY: stage-produced = union of COMPLETE
    receipt outputRefs; coverage = every coverageIds member of those captured returned views;
    inventories/candidate envelopes = exactly the digests named by cell outcomes; imports = Plan
    importIds. Forbidden domains: proof-bundle, finding, evaluation-seal, run, semantic-evidence.
    Section 6: "selectedRefs blob-domain members equal this set [hostDerivedRefs]."
      -> receipt_totality(), selected_totality()
 X9 contract section 7 -- evaluationInputRefs = selectedRefs + {domain:execution-inputs,digest};
    "`execution-inputs` itself is NOT a selectedRefs member (circular)";
    proof.executionInputsDigest is required.
      -> proof_wiring()
 X10 enumeration-plan.schema.v1.json #/$defs/UnselectedEnumeratorRef ("reason" const
    optional-unselected, "Lawful only on UnavailableProgramBindingV1 when the cell
    required=false") vs #/$defs/SelectedEnumeratorRef ("Executable unavailability with this
    selected closure is UnavailableProgramBindingV1, not an unselected enumerator"), joined to
    the CellProgramOutcomeV1.stageOrdinalNullReason enum {unavailable-binding,
    optional-unselected}: the typed null reason is DERIVED from which unavailable shape the
    binding actually is, not asserted.
      -> stage_joins()

DECLARED INTERPRETATIONS (stated because the text admits more than one reading, and this module
must not silently pick one):

 I-1  section 4 row 2 says "selected U, typed provider-unavailable candidate/inventory, no
      returned work". Later in the same section: "A selected unavailable binding may be
      `budget-exhausted` or `input-closure-incomplete` rather than generic
      `provider-unavailable`; the original typed pair is kept". This module therefore reads row 2
      as *any* typed unavailable inventory/candidate with no returned complete work, keeping the
      original pair -- not only the literal token provider-unavailable.
 I-2  section 5 requires the expected-subject membership join per account, and then closes with
      "Global missing expected subjects still needs a reconstruct join; this unit does not invent
      that census." This module reads the TABLE ROW as the binding obligation for the subjects
      this cell actually retains (the inventory rows of the relation's subject-kind), and reads
      the closing sentence as withholding a GLOBAL snapshot-wide census. It therefore joins
      retained inventory rows against the returned partitions and does not invent any census
      beyond them. The alternative reading -- that the closing sentence suspends the table row
      entirely -- is recorded, not assumed.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_schema as S
import opensip_build as B
import opensip_store as ST

OUT = '/tmp/opensip-design-corrections/consumer-b.v19/output'
KIT = S.KIT
RUNS = ['syntax-code', 'typescript', 'rust', 'rust-partial', 'syntax-data']

APPLICABILITY = ('supported-available', 'unsupported-typed', 'unavailable-unselected',
                 'unavailable-null-universe', 'inapplicable-vcs')
NON_SUPPORTED = APPLICABILITY[1:]
BLOB_DOMAINS = ('subject-inventory', 'candidate-producer-result', 'target-attribution',
                'incoming-search')
FORBIDDEN_REF_DOMAINS = ('proof-bundle', 'finding', 'evaluation-seal', 'run',
                         'semantic-evidence')
NULL_REASONS = ('unavailable-binding', 'optional-unselected')


def kitdoc(rel):
    return json.load(open(KIT + '/' + S.doc_path(rel)))


class F:
    def __init__(self):
        self.rows = []

    def need(self, cond, clause, check, detail=None):
        self.rows.append({'clause': clause, 'check': check,
                          'result': 'PASS' if cond else 'REFUSE', 'detail': detail})
        return bool(cond)

    def ok(self, clause, check, detail=None):
        self.rows.append({'clause': clause, 'check': check, 'result': 'PASS',
                          'detail': detail})

    def na(self, clause, check, detail=None):
        self.rows.append({'clause': clause, 'check': check, 'result': 'NOT-APPLICABLE',
                          'detail': detail})

    @property
    def refusals(self):
        return [r for r in self.rows if r['result'] == 'REFUSE']


class Run:
    """Everything this module is allowed to read, resolved once from the exported store."""

    def __init__(self, label):
        self.label = label
        self.st, _ = ST.Store.load(OUT + '/runs/%s.store.json' % label)
        st = self.st
        self.ei = json.loads(st.get_blob(st.labels['execution-inputs']).decode())
        self.ep = json.loads(st.get_blob(st.labels['enumeration-plan']).decode())
        self.plan_id = next(t for t in st.objects if t.startswith('plan2:'))
        self.plan = st.objects[self.plan_id]
        self.xp_id = next(t for t in st.objects if t.startswith('exec-plan2:'))
        self.xp = st.objects[self.xp_id]
        self.proof = next(r for t, r in st.objects.items() if t.startswith('proof3:'))
        self.snap = next(r for t, r in st.objects.items() if t.startswith('snapshot2:'))
        self.vcs = (json.loads(st.get_blob(self.snap['vcsDigest']).decode())
                    if self.snap.get('vcsDigest') else None)
        self.closures = {t: r for t, r in st.objects.items() if t.startswith('closure2:')}
        self.views = {t: r for t, r in st.objects.items() if t.startswith('view2:')}
        self.scopes = {t: r for t, r in st.objects.items() if t.startswith('scope2:')}
        self.covs = {t: r for t, r in st.objects.items() if t.startswith('coverage2:')}
        self.inv_by = {}
        for r in self.ei['selectedRefs']:
            if r['domain'] != 'subject-inventory':
                continue
            iv = json.loads(st.get_blob(r['digest']).decode())
            self.inv_by.setdefault((iv['cellOrdinal'], iv['programOrdinal']), []).append(
                (r['digest'], iv))
        self.cands = {}
        for d in self.ei['candidateResultRefs']:
            by = st.get_blob(d)
            if by is not None:
                self.cands[d] = json.loads(by.decode())
        self.projreg = kitdoc('foundation/evaluator-projection-registry.v1.json')
        self.matrix = kitdoc('native/native-capability-matrix.v2.json')
        self.defreg = kitdoc(B.NATIVE_DOC)[
            'x-opensip-deficiency-cause-registry']['deficiencies']
        self.outcome_of = {(c['cellOrdinal'], c['programOrdinal']): c
                           for c in self.ei['cellOutcomes']}

    # -------- resolution helpers (a typed id resolves only through the retained table)
    def cov_payload(self, tid):
        c = self.covs.get(tid)
        if c is None:
            return None
        by = self.st.get_blob(c['payloadDigest'])
        return json.loads(by.decode()) if by is not None else None

    def cov_scope(self, tid):
        c = self.covs.get(tid)
        return self.scopes.get(c['scopeId']) if c else None

    def binding(self, ck):
        cell = self.ep['cells'][ck[0]]
        return cell, cell['programBindings'][ck[1]]

    def stage_of(self, ordinal):
        rows = [s for s in self.xp['stages'] if s['ordinal'] == ordinal]
        return rows[0] if len(rows) == 1 else None

    def receipt_of(self, ordinal):
        rows = [r for r in self.ei['hostCapture']['stageReceipts']
                if r['ordinal'] == ordinal]
        return rows[0] if len(rows) == 1 else None


# ---------------------------------------------------------------------- X8 receipts
def receipt_totality(f, R):
    rcs = R.ei['hostCapture']['stageReceipts']
    ords = [r['ordinal'] for r in rcs]
    stage_ords = [s['ordinal'] for s in R.xp['stages']]
    f.need(len(set(ords)) == len(ords),
           'X8 section 1 "ordinals unique and total"', 'RECEIPT_ORDINALS_UNIQUE', ords)
    f.need(sorted(ords) == sorted(stage_ords),
           'X8 section 1 "one receipt per stage, ordinals unique and total" over '
           'execution-plan.stages (a silently missing stage is not an unavailable stage)',
           'ONE_RECEIPT_PER_EXECUTION_PLAN_STAGE',
           {'receipts': sorted(ords), 'stages': sorted(stage_ords)})
    f.need(R.ei['hostCapture']['custody'] == 'host-tcb-evidence-store'
           and R.ei['hostCapture']['observation'] == 'stage-return',
           'X8 schema HostCaptureV1 custody/observation consts ("TCB trust boundary, not a '
           'mathematically independent second witness")',
           'HOST_CAPTURE_DECLARES_ITS_OWN_TCB_CUSTODY',
           {'custody': R.ei['hostCapture']['custody'],
            'observation': R.ei['hostCapture']['observation'],
            'disclosure': ('this origin supplies that host observation synthetically; equality '
                           'to it proves selection, never a non-malicious host')})
    for rc in rcs:
        stg = R.stage_of(rc['ordinal'])
        where = {'ordinal': rc['ordinal'], 'state': rc['state']}
        if not f.need(stg is not None, 'X8 receipt names an admitted stage',
                      'RECEIPT_ORDINAL_IS_AN_ADMITTED_STAGE', where):
            continue
        f.need(rc['stageSpecDigest'] == stg['stageSpecDigest'],
               'X8 "rooted in admitted execution-plan producer obligations"',
               'RECEIPT_STAGE_SPEC_DIGEST_IS_THE_STAGES_OWN',
               dict(where, receipt=rc['stageSpecDigest'], stage=stg['stageSpecDigest']))
        f.need(K.C(K.cset_strings(rc['outputDomains']))
               == K.C(K.cset_strings(stg['outputDomains'])),
               'X8 "outputDomains equal that stage\'s admitted outputDomains"',
               'RECEIPT_OUTPUT_DOMAINS_EQUAL_THE_STAGE',
               dict(where, receipt=rc['outputDomains'], stage=stg['outputDomains']))
        f.need({r['domain'] for r in rc['outputRefs']} <= set(rc['outputDomains']),
               'X8 "outputRefs domains are a subset of those domains"',
               'RECEIPT_OUTPUT_REF_DOMAINS_SUBSET_OF_OUTPUT_DOMAINS',
               dict(where, refDomains=sorted({r['domain'] for r in rc['outputRefs']})))
        ss = R.st.get_blob(rc['stageSpecDigest'])
        if ss is not None:
            spec = json.loads(ss.decode())
            f.need(spec['producerClosure'] == rc['producerClosure'],
                   'X3 section 3 "stage-spec producerClosure"',
                   'RECEIPT_PRODUCER_IS_THE_STAGE_SPEC_PRODUCER',
                   dict(where, receipt=rc['producerClosure'],
                        stageSpec=spec['producerClosure']))
        if rc['state'] == 'unavailable':
            f.need(rc['unavailableReason'] is not None and not rc['outputRefs'],
                   'X8 schema StageReceiptV1.allOf[state=unavailable] + "Optional unavailable '
                   'stages carry typed state and a reason -- never silent missing"',
                   'UNAVAILABLE_RECEIPT_CARRIES_A_TYPED_REASON_AND_NO_OUTPUT_REFS',
                   dict(where, reason=rc['unavailableReason'],
                        outputRefs=len(rc['outputRefs'])))
        else:
            f.need(rc['unavailableReason'] is None,
                   'X8 schema StageReceiptV1.allOf[state=complete]',
                   'COMPLETE_RECEIPT_CARRIES_NO_UNAVAILABLE_REASON',
                   dict(where, reason=rc['unavailableReason']))


# ---------------------------------------------------------------------- X8 selectedRefs
def selected_totality(f, R):
    sel = R.ei['selectedRefs']
    f.need(not [r for r in sel if r['domain'] in FORBIDDEN_REF_DOMAINS],
           'X8 section 1 "Forbidden on selectedRefs: proof-bundle, finding, evaluation-seal, '
           'run, semantic-evidence"', 'NO_FORBIDDEN_SELECTED_REF_DOMAIN',
           sorted({r['domain'] for r in sel}))
    stage_out = []
    captured_views = set()
    for rc in R.ei['hostCapture']['stageReceipts']:
        if rc['state'] != 'complete':
            continue
        stage_out += rc['outputRefs']
        captured_views |= {r['digest'] for r in rc['outputRefs'] if r['domain'] == 'view'}
    produced = K.cset([r for r in sel if r['domain'] in ('view', 'coverage')])
    f.need(K.C(K.cset(stage_out)) == K.C(produced),
           'X8 section 1 selectedRefs table: stage-produced equals the "union of complete '
           'receipt outputRefs" (exact totality, not a subset)',
           'STAGE_PRODUCED_SELECTED_REFS_EQUAL_THE_COMPLETE_RECEIPT_UNION',
           {'declared': sorted((r['domain'], r['digest']) for r in produced),
            'receiptUnion': sorted((r['domain'], r['digest']) for r in K.cset(stage_out))})
    owed_cov = set()
    seen_cov = {r['digest'] for r in sel if r['domain'] == 'coverage'}
    for vd in sorted(captured_views):
        v = R.views.get('view2:' + vd)
        if v is None:
            continue
        owed_cov |= {R.st.suffix(c) for c in v['coverageIds']}
    f.need(owed_cov <= seen_cov,
           'X8 section 1 selectedRefs table: coverage equals "every coverageIds member of those '
           'captured returned views" (EXECUTION_INPUTS_SELECTED_COVER)',
           'EVERY_RETURNED_VIEW_COVERAGE_IS_A_SELECTED_REF',
           {'missing': sorted(owed_cov - seen_cov)})
    f.need(seen_cov <= owed_cov,
           'X8 the same table read the other way: a selected coverage ref that no captured '
           'returned view names is not stage-produced evidence',
           'NO_SELECTED_COVERAGE_OUTSIDE_THE_CAPTURED_VIEWS',
           {'extra': sorted(seen_cov - owed_cov)})
    hd = K.cset([r for r in sel if r['domain'] in BLOB_DOMAINS])
    f.need(K.C(hd) == K.C(R.ei['hostCapture']['hostDerivedRefs']),
           'X8 section 6 "selectedRefs blob-domain members equal this set"',
           'SELECTED_BLOB_DOMAIN_MEMBERS_EQUAL_HOST_DERIVED_REFS',
           {'selected': sorted((r['domain'], r['digest']) for r in hd),
            'hostDerived': sorted((r['domain'], r['digest'])
                                  for r in R.ei['hostCapture']['hostDerivedRefs'])})
    named_inv = {d for co in R.ei['cellOutcomes'] for d in co['inventoryDigests']}
    f.need({r['digest'] for r in sel if r['domain'] == 'subject-inventory'} == named_inv,
           'X8 section 1 selectedRefs table: inventories are "exactly the digests named by cell '
           'outcomes"', 'SELECTED_INVENTORIES_ARE_EXACTLY_THE_OUTCOME_NAMED_SET',
           {'selected': sorted({r['digest'] for r in sel
                                if r['domain'] == 'subject-inventory'}),
            'named': sorted(named_inv)})
    named_cand = {co['candidateResultDigest'] for co in R.ei['cellOutcomes']
                  if co['candidateResultDigest']}
    f.need({r['digest'] for r in sel
            if r['domain'] == 'candidate-producer-result'} == named_cand,
           'X8 the same row for candidate envelopes',
           'SELECTED_CANDIDATE_ENVELOPES_ARE_EXACTLY_THE_OUTCOME_NAMED_SET',
           {'named': sorted(named_cand)})
    f.need({'import2:' + r['digest'] for r in sel if r['domain'] == 'import'}
           == set(R.plan['importIds']),
           'X8 section 1 selectedRefs table: imports are "Plan importIds -- preselected Plan '
           'INPUT, not a view-only stage product"',
           'SELECTED_IMPORTS_EQUAL_THE_PLAN_IMPORT_IDS',
           {'selected': sorted('import2:' + r['digest'] for r in sel
                               if r['domain'] == 'import'),
            'plan': sorted(R.plan['importIds'])})


# ---------------------------------------------------------------------- X9 proof wiring
def proof_wiring(f, R):
    xi = [r for r in R.proof['evaluationInputRefs'] if r['domain'] == 'execution-inputs']
    f.need(len(xi) == 1, 'X9 section 7 required evaluationInputRefs shape',
           'EXACTLY_ONE_EXECUTION_INPUTS_REF_IN_THE_PROOF', len(xi))
    f.need(not [r for r in R.ei['selectedRefs'] if r['domain'] == 'execution-inputs'],
           'X9 section 7 "`execution-inputs` itself is NOT a selectedRefs member (circular)"',
           'EXECUTION_INPUTS_IS_NOT_ITS_OWN_SELECTED_REF', None)
    f.need(R.proof.get('executionInputsDigest') is not None,
           'X9 section 7 "proof.executionInputsDigest is required"',
           'PROOF_CARRIES_THE_EXECUTION_INPUTS_DIGEST', None)
    if xi:
        f.need(xi[0]['digest'] == R.proof.get('executionInputsDigest'),
               'X9 the XI member is that digest', 'XI_MEMBER_IS_THE_PROOF_DIGEST', None)
        want = K.cset(list(R.ei['selectedRefs']) + [xi[0]])
        f.need(K.C(want) == K.C(R.proof['evaluationInputRefs']),
               'X9 section 7 "require evaluationInputRefs = selectedRefs + '
               '{domain:execution-inputs,digest}"',
               'EVALUATION_INPUT_REFS_EQUAL_SELECTED_REFS_PLUS_XI', None)
        f.need(K.rec_digest(R.ei) == xi[0]['digest'],
               'X9 schema title: identity is the raw SHA-256 of C(this record)',
               'EXECUTION_INPUTS_DIGEST_IS_THE_RECORD_IDENTITY', None)


# ---------------------------------------------------------------------- X1/X5 accounts
def derive_account(f, R, acc):
    """Returns (state, deficiency, nativeCause) derived from the owner records alone."""
    ck = (acc['cellOrdinal'], acc['programOrdinal'])
    cell, binding = R.binding(ck)
    U = binding.get('universe')
    appl = acc['applicability']
    co = R.outcome_of.get(ck) or {}
    where = {'cell': cell['capabilityId'], 'program': ck[1], 'relation': acc['relation'],
             'resolution': acc['resolution'], 'applicability': appl}

    f.need(appl in APPLICABILITY, 'X1 applicability enum',
           'APPLICABILITY_IS_A_LITERAL_MEMBER', where)
    if appl in NON_SUPPORTED:
        f.need(not acc['coverageIds'],
               'X1 schema allOf (coverageIds maxItems 0) + section 5 table "none" / "do not '
               'fabricate Coverage at null U"',
               'NO_COVERAGE_ENVELOPE_WHERE_THE_BRANCH_FORBIDS_ONE',
               dict(where, coverageIds=len(acc['coverageIds'])))
    f.na('X5 "This clause ... does NOT constrain `targetUniverse`: a Coverage or a fact may name '
         'a target in another universe"',
         'TARGET_UNIVERSE_IS_DELIBERATELY_UNCONSTRAINED_HERE',
         dict(where, targetUniverse=acc['targetUniverse']))

    if appl == 'supported-available':
        f.need(acc['sourceUniverse'] == U,
               'X5 "A selected (cellOrdinal, programOrdinal) binding carries exactly ONE '
               'universe U"', 'SUPPORTED_ACCOUNT_SOURCE_UNIVERSE_IS_THE_BINDING_UNIVERSE',
               dict(where, account=acc['sourceUniverse'], binding=U))
        returned, foreign = set(), []
        for vd in co.get('viewDigests', []):
            v = R.views.get('view2:' + vd)
            if v is None:
                continue
            if v.get('producerClosure') != co.get('enumeratorClosure'):
                # section 5: the resolution is "restricted to the binding's own
                # enumerator/provider closure"
                continue
            for cid in v['coverageIds']:
                pay = R.cov_payload(cid)
                sc = R.cov_scope(cid)
                if pay is None or sc is None:
                    continue
                k = pay['key']
                if (k['relation'], k['resolution']) != (acc['relation'], acc['resolution']):
                    continue
                if k['sourceUniverse'] != U or sc['sourceUniverse'] != U:
                    foreign.append({'coverage': cid, 'payloadU': k['sourceUniverse'],
                                    'scopeU': sc['sourceUniverse'], 'bindingU': U})
                    continue
                returned.add(R.st.suffix(cid))
        f.need(not foreign,
               'X5 "every resolved Coverage envelope\'s subject-scope sourceUniverse and every '
               'resolved Coverage payload key.sourceUniverse MUST equal U -- a foreign-universe '
               'Coverage reached this way is EXECUTION_INPUTS_COVERAGE_DERIVE, not a silently '
               'skipped row"',
               'NO_FOREIGN_UNIVERSE_COVERAGE_REACHED_THROUGH_THIS_BINDING',
               dict(where, foreign=foreign))
        f.need(set(acc['coverageIds']) == returned,
               'X5 "the account\'s declared coverageIds MUST equal the complete matching '
               'returned partition set for (cell, program, relation, resolution, U, producer)"',
               'COVERAGE_IDS_EQUAL_EVERY_MATCHING_RETURNED_PARTITION',
               dict(where, declared=sorted(acc['coverageIds']), derived=sorted(returned)))
        if not returned:
            f.ok('X5 "Empty -> semantic native-work-incomplete"',
                 'SUPPORTED_AVAILABLE_WITH_NO_RETURNED_PARTITION_IS_NATIVE_WORK_INCOMPLETE',
                 where)
            return ('native-work-incomplete', None, None)
        entries = []
        for hx in sorted(returned):
            pay = R.cov_payload('coverage2:' + hx)
            entries.append((hx, pay['entry']))
        if not all(e['coverage'] == 'complete' for _h, e in entries):
            pair = next(((e['deficiency'], e['nativeCause']) for _h, e in entries
                         if e['coverage'] != 'complete'), (None, None))
            f.ok('X5 "Mixed complete+unknown -> not complete"; "Each coverage record keeps '
                 'deficiency+nativeCause+inputRef together. No branch may unzip deficiencies '
                 'and nativeCauses and re-pair the first of each."',
                 'MIXED_COVERAGE_IS_NOT_A_COMPLETE_ACCOUNT',
                 dict(where, coverages=[(h, e['coverage']) for h, e in entries],
                      keptPair=list(pair)))
            return ('incomplete',) + pair
        # I-2: expected source subjects of the relation's subject-kind
        row = (R.projreg['relations'].get(acc['relation']) or {})
        kind = row.get('sourceSubjectKind')
        expect, from_inv = set(), []
        for d, iv in R.inv_by.get(ck, []):
            if iv['kind'] != kind:
                continue
            from_inv.append(d)
            expect |= {r['nativeSubjectId'] for r in iv['rows']}
        covered = set()
        for hx in sorted(returned):
            sc = R.cov_scope('coverage2:' + hx)
            if sc:
                covered |= set(sc['subjects'])
        if not from_inv:
            f.na('X5 expected-subject membership (interpretation I-2)',
                 'THIS_CELL_RETAINS_NO_INVENTORY_OF_THE_RELATIONS_SUBJECT_KIND',
                 dict(where, subjectKind=kind))
            return ('complete', None, None)
        missing = sorted(expect - covered)
        # The clause makes a shortfall a DERIVED STATE, not a defect in the record: "Missing
        # expected subjects -> incomplete even if the remaining Coverage is complete". So the
        # shortfall is measured and reported here and folded into the derived account state; the
        # only refusable thing is a HOST ROW that disagrees with the derivation, which the outcome
        # checks below decide. (The generation-18 draft of this module refused on the shortfall
        # itself, which would have reported lawful evidence as a defect.)
        f.ok('X5 "every expected source subject from this cell\'s inventory/extent of the '
             'relation\'s subject-kind must be a member of some returned partition '
             '(source-path / package-name / symbol) ... Missing expected subjects -> incomplete '
             'even if the remaining Coverage is complete"',
             'EXPECTED_SOURCE_SUBJECT_MEMBERSHIP_MEASURED',
             dict(where, subjectKind=kind, inventories=sorted(from_inv),
                  expected=len(expect), covered=len(expect & covered), missing=missing,
                  derivedAccountState=('complete' if not missing else 'incomplete'),
                  interpretation='I-2'))
        return ('complete', None, None) if not missing else ('incomplete', None, None)

    if appl == 'unsupported-typed':
        cap = R.projreg['capabilityForRelation'].get(acc['relation'])
        rows = [c for c in R.matrix['cells']
                if c['capability'] == cap and c['mode'] == cell['languageMode']]
        mdef = rows[0]['deficiency'] if rows else None
        f.need(bool(rows) and mdef is not None,
               'X5 unsupported-typed carries the "matrix cell deficiency"',
               'UNSUPPORTED_TYPED_HAS_A_MATRIX_CELL_WITH_A_DEFICIENCY',
               dict(where, capability=cap, mode=cell['languageMode'], matrixRows=len(rows),
                    matrixDeficiency=mdef))
        reg = R.defreg.get(mdef) or {}
        allowed = reg.get('allowedCauses') or []
        cause = allowed[0] if (reg.get('nativeCause') == 'required'
                               and len(allowed) == 1) else None
        f.ok('X5 "the cause-registry cause for THAT deficiency (not a hardcoded '
             'capability-missing for every cell)"',
             'UNSUPPORTED_TYPED_CAUSE_COMES_FROM_THE_REGISTRY_ROW_FOR_THAT_DEFICIENCY',
             dict(where, matrixDeficiency=mdef, registryVerdict=reg.get('nativeCause'),
                  allowedCauses=allowed, derivedCause=cause))
        return ('unsupported-typed', mdef, cause)

    if appl == 'inapplicable-vcs':
        f.need(R.vcs is not None and R.vcs.get('kind') == 'none',
               'X5 inapplicable-vcs: "admitted VCS observation kind=none is the basis"',
               'INAPPLICABLE_VCS_REQUIRES_AN_ADMITTED_VCS_KIND_NONE',
               dict(where, admittedVcsKind=(R.vcs or {}).get('kind')))
        return ('inapplicable', None, None)

    # unavailable-unselected / unavailable-null-universe
    f.need(acc['sourceUniverse'] is None,
           'X5 the null-U branches carry no universe and no Coverage',
           'UNAVAILABLE_ACCOUNT_CARRIES_A_NULL_SOURCE_UNIVERSE',
           dict(where, sourceUniverse=acc['sourceUniverse']))
    if appl == 'unavailable-unselected':
        f.need(binding['enumerator'].get('status') == 'unselected',
               'X5 applicability is "joined to binding+matrix+VCS"',
               'UNAVAILABLE_UNSELECTED_MATCHES_AN_UNSELECTED_ENUMERATOR',
               dict(where, enumerator=binding['enumerator']))
    else:
        f.need(U is None,
               'X5 unavailable-null-universe is the null-U binding',
               'UNAVAILABLE_NULL_UNIVERSE_MATCHES_A_NULL_BINDING_UNIVERSE',
               dict(where, bindingUniverse=U))
    return ('unavailable', None, None)


# ---------------------------------------------------------------------- X3/X7/X10 stage joins
def stage_joins(f, R, co, derived_state):
    ck = (co['cellOrdinal'], co['programOrdinal'])
    cell, binding = R.binding(ck)
    U = binding.get('universe')
    selected = (binding['enumerator'].get('status') == 'selected' and U is not None)
    where = {'cell': cell['capabilityId'], 'program': ck[1], 'declaredState': co['state'],
             'derivedState': derived_state}
    for fld, val in (('capabilityId', cell['capabilityId']),
                     ('languageMode', cell['languageMode']),
                     ('workspaceRoot', cell['workspaceRoot']),
                     ('required', cell['required'])):
        f.need(co[fld] == val, 'X4 "One row per enumeration binding"',
               'OUTCOME_FIELD_EQUALS_THE_CELL:' + fld,
               dict(where, field=fld, row=co[fld], cell=val))
    f.need(K.C(K.cset_strings(co['kinds'])) == K.C(K.cset_strings(cell['kinds'])),
           'X4 "kinds set-equal to the cell"', 'OUTCOME_KINDS_EQUAL_THE_CELL_KINDS',
           dict(where, row=co['kinds'], cell=cell['kinds']))
    f.need(co['universe'] == U, 'X3 the row names the binding universe',
           'OUTCOME_UNIVERSE_IS_THE_BINDING_UNIVERSE',
           dict(where, row=co['universe'], binding=U))
    f.need(co['enumeratorStatus'] == binding['enumerator'].get('status'),
           'X3 enumerator status comes from the binding',
           'OUTCOME_ENUMERATOR_STATUS_IS_THE_BINDING_STATUS',
           dict(where, row=co['enumeratorStatus'],
                binding=binding['enumerator'].get('status')))
    if selected:
        f.need(co['enumeratorClosure'] == binding['enumerator'].get('closureId'),
               'X3 "Check enumerator closure"',
               'OUTCOME_ENUMERATOR_CLOSURE_IS_THE_BINDING_CLOSURE',
               dict(where, row=co['enumeratorClosure'],
                    binding=binding['enumerator'].get('closureId')))
        f.need(co['enumeratorClosure'] in R.plan['semanticClosures'],
               'X3 "(Plan-selected PROVIDER)"', 'ENUMERATOR_CLOSURE_IS_PLAN_SELECTED',
               dict(where, closure=co['enumeratorClosure']))
        kind = (R.closures.get(co['enumeratorClosure']) or {}).get('kind')
        f.need(kind == 'provider', 'X3 "(Plan-selected PROVIDER)"',
               'ENUMERATOR_CLOSURE_KIND_IS_PROVIDER', dict(where, closureKind=kind))

    if selected and derived_state in ('complete', 'partial'):
        if f.need(isinstance(co['stageOrdinal'], int),
                  'X3 "Selected producer outputs ... stageOrdinal non-null, matching a receipt"',
                  'SELECTED_PRODUCER_OUTPUT_HAS_A_STAGE_ORDINAL',
                  dict(where, stageOrdinal=co['stageOrdinal'])):
            rc = R.receipt_of(co['stageOrdinal'])
            stg = R.stage_of(co['stageOrdinal'])
            if f.need(rc is not None and stg is not None,
                      'X3 "matching a receipt"',
                      'STAGE_ORDINAL_MATCHES_ONE_RECEIPT_AND_ONE_STAGE',
                      dict(where, ordinal=co['stageOrdinal'])):
                f.need(rc['producerClosure'] == co['enumeratorClosure'],
                       'X3 "Check enumerator closure ..., stage-spec producerClosure"',
                       'RECEIPT_PRODUCER_IS_THE_CELL_ENUMERATOR',
                       dict(where, receipt=rc['producerClosure'],
                            cell=co['enumeratorClosure']))
                f.need(K.C(K.cset_strings(rc['outputDomains']))
                       == K.C(K.cset_strings(stg['outputDomains'])),
                       'X3 "and receipt outputDomains vs the stage"',
                       'RECEIPT_OUTPUT_DOMAINS_VS_THE_STAGE',
                       dict(where, receipt=rc['outputDomains'], stage=stg['outputDomains']))
                rv = {r['digest'] for r in rc['outputRefs'] if r['domain'] == 'view'}
                f.need(set(co['viewDigests']) <= rv,
                       'X7 viewDigests DESC "Must equal captured receipt views attributed to '
                       'this cell/program/U/producer"',
                       'OUTCOME_VIEWS_COME_FROM_THE_CAPTURED_RECEIPT',
                       dict(where, declared=sorted(co['viewDigests']),
                            receiptViews=sorted(rv)))
        for vd in co['viewDigests']:
            v = R.views.get('view2:' + vd)
            if not f.need(v is not None,
                          'X7 "view2 H suffixes, never sha256(C(view))"',
                          'VIEW_DIGEST_RESOLVES_AS_A_VIEW2_H_SUFFIX', dict(where, view=vd)):
                continue
            f.need(v['planId'] == R.plan_id, 'X3 "view planId"',
                   'ATTRIBUTED_VIEW_NAMES_THIS_PLAN',
                   dict(where, view=vd, viewPlan=v['planId']))
            f.need(v['producerClosure'] == co['enumeratorClosure'],
                   'X3 the attributed view is this cell\'s own producer output',
                   'ATTRIBUTED_VIEW_PRODUCER_IS_THE_CELL_ENUMERATOR',
                   dict(where, view=vd, viewProducer=v['producerClosure']))
            for sid in v['scopeIds']:
                sc = R.scopes.get(sid)
                if sc is None:
                    continue
                f.need(sc['sourceUniverse'] == U,
                       'X3 "each named scope `sourceUniverse` vs binding U"',
                       'NAMED_SCOPE_SOURCE_UNIVERSE_IS_THE_BINDING_UNIVERSE',
                       dict(where, scope=sid, scopeU=sc['sourceUniverse'], bindingU=U))
        if co['state'] == 'complete':
            f.need(bool(co['viewDigests']),
                   'X3 "Selected U cannot become complete by omitting the stage and views"',
                   'COMPLETE_SELECTED_CELL_NAMES_ITS_VIEWS', where)
    else:
        if co['stageOrdinal'] is None:
            if binding['enumerator'].get('status') == 'unselected':
                want = 'optional-unselected'
                basis = ('UnselectedEnumeratorRef.reason is the const optional-unselected and is '
                         '"Lawful only on UnavailableProgramBindingV1 when the cell '
                         'required=false"')
                f.need(binding['enumerator'].get('reason') == 'optional-unselected'
                       and cell['required'] is False,
                       'X10 UnselectedEnumeratorRef DESC',
                       'UNSELECTED_ENUMERATOR_IS_THE_OPTIONAL_CELL_SHAPE',
                       dict(where, enumerator=binding['enumerator'],
                            required=cell['required']))
            else:
                want = 'unavailable-binding'
                basis = ('SelectedEnumeratorRef DESC: "Executable unavailability with this '
                         'selected closure is UnavailableProgramBindingV1, not an unselected '
                         'enumerator"')
            f.need(co['stageOrdinalNullReason'] == want,
                   'X10 + X2 stageOrdinalNullReason enum {unavailable-binding, '
                   'optional-unselected}',
                   'NULL_STAGE_REASON_IS_DERIVED_FROM_THE_BINDING_SHAPE',
                   dict(where, declared=co['stageOrdinalNullReason'], derived=want,
                        basis=basis))
        else:
            rc = R.receipt_of(co['stageOrdinal'])
            f.need(rc is not None and rc['state'] == 'unavailable'
                   and rc['unavailableReason'] == 'provider-unavailable',
                   'X3 "Unavailable / optional-unselected: stageOrdinal may be null with typed '
                   'reason, OR may name an `unavailable` receipt (provider-unavailable)"',
                   'UNAVAILABLE_CELL_NAMING_A_RECEIPT_NAMES_AN_UNAVAILABLE_ONE',
                   dict(where, ordinal=co['stageOrdinal'],
                        receiptState=(rc or {}).get('state'),
                        receiptReason=(rc or {}).get('unavailableReason')))
        f.need(not co['viewDigests'],
               'X3 an unavailable / unselected binding returned no attributed view',
               'UNAVAILABLE_CELL_ATTRIBUTES_NO_VIEW',
               dict(where, viewDigests=co['viewDigests']))


# ---------------------------------------------------------------------- X2 cross-field
def outcome_cross_field(f, R, co):
    where = {'cell': co['cellOrdinal'], 'program': co['programOrdinal'],
             'state': co['state']}
    if co['state'] == 'complete':
        f.need(co['deficiency'] is None and co['nativeCause'] is None
               and isinstance(co['stageOrdinal'], int)
               and co['stageOrdinalNullReason'] is None,
               'X2 schema CellProgramOutcomeV1.allOf[state=complete]',
               'COMPLETE_OUTCOME_CROSS_FIELD_SHAPE',
               dict(where, deficiency=co['deficiency'], nativeCause=co['nativeCause'],
                    stageOrdinal=co['stageOrdinal'],
                    stageOrdinalNullReason=co['stageOrdinalNullReason']))
    if co['stageOrdinal'] is None:
        f.need(isinstance(co['stageOrdinalNullReason'], str)
               and co['stageOrdinalNullReason'] in NULL_REASONS,
               'X2 schema allOf[stageOrdinal null] + the reason enum',
               'NULL_STAGE_ORDINAL_CARRIES_A_TYPED_REASON',
               dict(where, reason=co['stageOrdinalNullReason']))


# ---------------------------------------------------------------------- X6 inventories
def outcome_inventories(f, R, co):
    ck = (co['cellOrdinal'], co['programOrdinal'])
    cell, binding = R.binding(ck)
    invs = R.inv_by.get(ck, [])
    kinds = sorted(iv['kind'] for _d, iv in invs)
    where = {'cell': cell['capabilityId'], 'program': ck[1],
             'enumeratorStatus': binding['enumerator'].get('status'),
             'bindingUniverse': binding.get('universe')}
    f.need(kinds == sorted(set(kinds)), 'X6 section 4 "exactly one per kind"',
           'EXACTLY_ONE_INVENTORY_PER_KIND', dict(where, kinds=kinds))
    f.need(sorted(set(kinds)) == sorted(set(cell['kinds'])),
           'X6 section 4 "kinds set-equal to the cell" read with section 6 "Unselected or '
           '`universe=null` does not discard same-cell inventory items" -- the clause carries no '
           'available-only qualifier',
           'INVENTORY_KINDS_SET_EQUAL_TO_THE_CELL',
           dict(where, cellKinds=sorted(set(cell['kinds'])), inventoryKinds=kinds))
    f.need(sorted(co['inventoryDigests']) == sorted(d for d, _ in invs),
           'X6 the row names the retained inventory set',
           'OUTCOME_INVENTORY_DIGESTS_ARE_THE_RETAINED_SET',
           dict(where, declared=sorted(co['inventoryDigests']),
                retained=sorted(d for d, _ in invs)))
    for _d, iv in invs:
        f.need(iv['parameterDigest'] == R.ei['enumerationPlanDigest'],
               'X6 section 7 "Their retained cell records and exact selected references bind '
               'them to this Plan"',
               'INVENTORY_PARAMETER_DIGEST_IS_THE_ENUMERATION_PLAN',
               dict(where, kind=iv['kind'], parameterDigest=iv['parameterDigest']))
    return invs


# ---------------------------------------------------------------------- X4 outcome
def derive_outcome_state(R, co, invs, my_accounts):
    """The section 4 table, row by row. Reads no seal and no capability-availability notion."""
    ck = (co['cellOrdinal'], co['programOrdinal'])
    _cell, binding = R.binding(ck)
    if (binding['enumerator'].get('status') == 'unselected'
            or binding.get('universe') is None):
        return ('unavailable', (binding.get('deficiency'), binding.get('nativeCause')),
                'row1: enumerator unselected, or universe null')
    states = [v[0] for v in my_accounts.values()]
    inv_states = [iv['state'] for _d, iv in invs]
    returned_work = any(s == 'complete' for s in states)
    cand = R.cands.get(co['candidateResultDigest']) if co['candidateResultDigest'] else None
    typed_unavailable = ('unavailable' in inv_states
                         or (cand is not None and cand['state'] == 'unavailable'))
    if typed_unavailable and not returned_work:
        pair = (None, None)
        for _d, iv in sorted(invs, key=lambda t: t[0]):
            if iv['state'] == 'unavailable':
                pair = (iv.get('deficiency'), iv.get('nativeCause'))
                break
        else:
            if cand is not None:
                pair = (cand.get('deficiency'), cand.get('nativeCause'))
        return ('unavailable', pair,
                'row2: typed unavailable candidate/inventory, no returned work '
                '(interpretation I-1)')
    not_complete_supported = [k for k, v in my_accounts.items()
                              if v[0] in ('incomplete', 'native-work-incomplete')]
    if 'partial' in inv_states or not_complete_supported:
        pair = (None, None)
        for _d, iv in sorted(invs, key=lambda t: t[0]):
            if iv['state'] != 'complete':
                pair = (iv.get('deficiency'), iv.get('nativeCause'))
                break
        else:
            for k in sorted(not_complete_supported):
                pair = my_accounts[k][1:]
                break
        return ('partial', pair,
                'row3: any inventory partial, or any supported-available account not complete')
    if cand is not None and cand['state'] != 'complete':
        return ('partial', (cand.get('deficiency'), cand.get('nativeCause')),
                'row4: candidate owed but not complete')
    return ('complete', (None, None),
            'row4: all inventories complete, every account complete/inapplicable/unsupported, '
            'candidate complete if owed')


def outcome_pair(f, R, co, invs, my_accounts, derived_pair, derived_state, basis):
    ck = (co['cellOrdinal'], co['programOrdinal'])
    cell, binding = R.binding(ck)
    where = {'cell': cell['capabilityId'], 'program': ck[1],
             'declaredState': co['state'], 'derivedState': derived_state,
             'tableRow': basis}
    f.need(co['state'] == derived_state, 'X4 section 4 derived-state table',
           'CELL_OUTCOME_STATE_IS_DERIVED_FROM_THE_TABLE',
           dict(where, inventoryStates=[iv['state'] for _d, iv in invs],
                accountStates={'%s@%s' % k[2:]: v[0] for k, v in my_accounts.items()},
                note=('derived WITHOUT reading the evaluation seal, the Run verdict, or any '
                      'general "capability is available" notion')))
    if co['state'] == 'complete':
        f.need(not any(iv['state'] == 'partial' for _d, iv in invs),
               'X4 "`complete` + partial inventory is EXECUTION_INPUTS_OUTCOME_DERIVE"',
               'COMPLETE_ROW_HAS_NO_PARTIAL_INVENTORY',
               dict(where, inventoryStates=[iv['state'] for _d, iv in invs]))
    declared = (co['deficiency'], co['nativeCause'])
    f.need(declared == derived_pair,
           'X4 "The row\'s deficiency/nativeCause equals the derived primary pair (first '
           'retained source)"', 'CELL_OUTCOME_PRIMARY_PAIR_IS_DERIVED',
           dict(where, declared=list(declared), derived=list(derived_pair)))
    source_pairs = [(iv.get('deficiency'), iv.get('nativeCause'))
                    for _d, iv in invs if iv['state'] != 'complete']
    source_pairs += [(v[1], v[2]) for v in my_accounts.values() if v[0] != 'complete']
    if (binding['enumerator'].get('status') == 'unselected'
            or binding.get('universe') is None):
        source_pairs.append((binding.get('deficiency'), binding.get('nativeCause')))
    if co['candidateResultDigest']:
        c = R.cands.get(co['candidateResultDigest'])
        if c is not None and c['state'] != 'complete':
            source_pairs.append((c.get('deficiency'), c.get('nativeCause')))
    if declared != (None, None):
        f.need(declared in source_pairs,
               'X4 "that pair must actually occur on a source record ... Host join requires the '
               'outcome pair to be a MEMBER of those source pairs, not equal only to a first '
               'unzipped cause"',
               'CELL_OUTCOME_PAIR_IS_A_MEMBER_OF_THE_OWNED_SOURCE_PAIRS',
               dict(where, declared=list(declared),
                    ownedPairs=[list(p) for p in source_pairs]))
    else:
        f.ok('X4 no carrier claimed', 'CELL_OUTCOME_CLAIMS_NO_CARRIER_PAIR', where)
    if not cell['kinds']:
        f.need(co['state'] != 'complete' or co['candidateResultDigest'] is not None,
               'X4 "Empty `kinds` is not complete-empty work"',
               'EMPTY_KINDS_IS_NOT_COMPLETE_EMPTY_WORK',
               dict(where, candidateResultDigest=co['candidateResultDigest']))


# ---------------------------------------------------------------------- X6 candidates
def candidate_refs(f, R):
    want = sorted({co['candidateResultDigest'] for co in R.ei['cellOutcomes']
                   if co['candidateResultDigest']})
    f.need(sorted(R.ei['candidateResultRefs']) == want,
           'X6 section 6 "candidateResultRefs EQUALS the set of outcomes\' non-null '
           'candidateResultDigest, each bound once"',
           'CANDIDATE_RESULT_REFS_EQUAL_THE_OUTCOME_SET',
           {'declared': sorted(R.ei['candidateResultRefs']), 'derived': want})
    names = [co['candidateResultDigest'] for co in R.ei['cellOutcomes']
             if co['candidateResultDigest']]
    f.need(len(names) == len(set(names)), 'X6 "each bound once"',
           'EACH_CANDIDATE_ENVELOPE_IS_BOUND_ONCE', names)
    if not want:
        owed = [c['capabilityId'] for c in R.ep['cells']
                if c['capabilityId'] in ('clones-near', 'clones-cross-tsjs')]
        f.need(not owed,
               'X6 schema CandidateProducerResultV1.capabilityId enum {clones-near, '
               'clones-cross-tsjs}: such a cell owes the envelope '
               '(EXECUTION_INPUTS_CANDIDATE_REQUIRED)',
               'NO_CELL_OWES_A_CANDIDATE_ENVELOPE_IN_THIS_RUN', {'owedBy': owed})
        f.na('X6 section 6 candidate custody (sourceBodies ids/paths/universe/contentSha256/'
             'byteLength, examinedPaths = this binding\'s Plan candidateSourcePaths, '
             'complete-empty envelope shape)',
             'SECTION_6_CANDIDATE_CUSTODY_IS_UNEXERCISED_BY_THIS_RUN',
             {'candidateResultRefs': 0,
              'standing': ('this Run declares no clones-near / clones-cross-tsjs cell, so no '
                           'CandidateProducerResultV1 is owed and none is retained; the '
                           'section 6 custody laws are therefore NOT exercised here, which is '
                           'recorded as an exercise gap rather than as a pass')})
        return
    snap_rows = {r['path']: r for r in R.snap['sourceInventory']}
    for d, c in sorted(R.cands.items()):
        ck = (c['cellOrdinal'], c['programOrdinal'])
        cell, binding = R.binding(ck)
        census = binding.get('candidateSourcePaths')
        where = {'candidate': d[:12], 'cell': cell['capabilityId'], 'program': ck[1]}
        f.need(c['planId'] == R.plan_id and c['executionPlanId'] == R.xp_id,
               'X6 the envelope is bound to this Plan', 'CANDIDATE_PLAN_JOIN', where)
        f.need(c['universe'] == binding.get('universe'),
               'X6 "`universe` must equal the envelope U"',
               'CANDIDATE_UNIVERSE_IS_THE_BINDING_UNIVERSE',
               dict(where, envelope=c['universe'], binding=binding.get('universe')))
        f.need(census is not None,
               'X6 "the Plan field must be present (explicit [] is a selected zero-path '
               'census)"', 'BINDING_DECLARES_A_CANDIDATE_SOURCE_PATH_CENSUS', where)
        if c['state'] == 'complete':
            f.need(sorted(c['examinedPaths']) == sorted(census or []),
                   'X6 "Complete examinedPaths equals the Plan candidateSourcePaths of THIS '
                   'program binding, not the whole snapshot and not the union of sibling '
                   'programs"', 'COMPLETE_EXAMINED_PATHS_EQUAL_THIS_BINDINGS_PLAN_CENSUS',
                   dict(where, examined=sorted(c['examinedPaths']),
                        census=sorted(census or [])))
            if not c['sourceBodies']:
                f.need(c['groupDigests'] == [],
                       'X6 "Complete-empty candidate still requires the retained envelope with '
                       'sourceBodies=[], groupDigests=[], and examinedPaths equal that Plan '
                       'census"', 'COMPLETE_EMPTY_CANDIDATE_ENVELOPE_SHAPE', where)
        groups = {}
        for gd in c['groupDigests']:
            by = R.st.get_blob(gd)
            if f.need(by is not None,
                      'X6 "Every group digest is read from retained exact bytes, hashed, '
                      'schema-validated as CloneCandidateGroupV2"',
                      'CANDIDATE_GROUP_BYTES_ARE_RETAINED', dict(where, group=gd[:12])):
                groups[gd] = json.loads(by.decode())
        members = {m for g in groups.values() for m in g['members']}
        for sb in c['sourceBodies']:
            w2 = dict(where, body=sb['id'], path=sb['path'])
            f.need(sb['id'] in members, 'X6 "Each `id` must match a group member"',
                   'CANDIDATE_SOURCE_BODY_ID_IS_A_GROUP_MEMBER', w2)
            f.need(sb['path'] in (census or []),
                   'X6 "each `path` must be in THIS binding\'s Plan candidateSourcePaths"',
                   'CANDIDATE_SOURCE_BODY_PATH_IS_IN_THE_PLAN_CENSUS',
                   dict(w2, census=sorted(census or [])))
            f.need(sb['universe'] == c['universe'],
                   'X6 "`universe` must equal the envelope U"',
                   'CANDIDATE_SOURCE_BODY_UNIVERSE_IS_THE_ENVELOPE_U', w2)
            row = snap_rows.get(sb['path'])
            f.need(row is not None and sb['contentSha256'] == row['sha256']
                   and sb['byteLength'] == row['bytes'],
                   'X6 "contentSha256/byteLength must equal the admitted snapshot '
                   'source-inventory row ... that file\'s snapshot length, not a body-span"',
                   'CANDIDATE_SOURCE_BODY_JOINS_THE_SNAPSHOT_ROW',
                   dict(w2, declared=[sb['contentSha256'], sb['byteLength']],
                        snapshot=[(row or {}).get('sha256'), (row or {}).get('bytes')]))


# ---------------------------------------------------------------------- per-run driver
def check(label):
    f = F()
    R = Run(label)
    receipt_totality(f, R)
    selected_totality(f, R)
    proof_wiring(f, R)

    keys = [(c['cellOrdinal'], c['programOrdinal']) for c in R.ei['cellOutcomes']]
    f.need(len(set(keys)) == len(keys),
           'X6 section 4 "One outcome per enumeration (cellOrdinal, programOrdinal)"',
           'ONE_OUTCOME_PER_CELL_PROGRAM', keys)
    planned = {(ci, b['ordinal']) for ci, c in enumerate(R.ep['cells'])
               for b in c['programBindings']}
    f.need(set(keys) == planned,
           'X6 EXECUTION_INPUTS_CELL_TOTALITY: an outcome for every planned binding',
           'AN_OUTCOME_FOR_EVERY_PLANNED_CELL_PROGRAM',
           {'declared': sorted(keys), 'planned': sorted(planned)})
    f.need(R.ei['enumerationPlanDigest'] == K.rec_digest(R.ep),
           'X6 the parameter digest is the retained EnumerationPlanV1',
           'ENUMERATION_PLAN_DIGEST_IS_THE_RETAINED_PARAMETER', None)

    acc_keys = [(a['cellOrdinal'], a['programOrdinal'], a['relation'], a['resolution'])
                for a in R.ei['nativeCoverageAccounts']]
    f.need(len(set(acc_keys)) == len(acc_keys),
           'X5 "References plus explicit applicability for ONE matrix relation@rung on one '
           'binding" (EXECUTION_INPUTS_NATIVE_COVERAGE_TOTALITY)',
           'ONE_ACCOUNT_PER_CELL_PROGRAM_RELATION_RUNG', None)

    derived_accounts = {}
    for acc in R.ei['nativeCoverageAccounts']:
        k = (acc['cellOrdinal'], acc['programOrdinal'], acc['relation'], acc['resolution'])
        derived_accounts[k] = derive_account(f, R, acc)

    for co in R.ei['cellOutcomes']:
        ck = (co['cellOrdinal'], co['programOrdinal'])
        outcome_cross_field(f, R, co)
        invs = outcome_inventories(f, R, co)
        mine = {k: v for k, v in derived_accounts.items() if k[:2] == ck}
        state, pair, basis = derive_outcome_state(R, co, invs, mine)
        stage_joins(f, R, co, state)
        outcome_pair(f, R, co, invs, mine, pair, state, basis)
    candidate_refs(f, R)
    return f


def main():
    out, total = {}, 0
    for label in RUNS:
        f = check(label)
        out[label] = {'checks': f.rows,
                      'passed': sum(1 for r in f.rows if r['result'] == 'PASS'),
                      'notApplicable': sum(1 for r in f.rows
                                           if r['result'] == 'NOT-APPLICABLE'),
                      'refused': len(f.refusals), 'refusals': f.refusals}
        total += len(f.refusals)
        print('%-13s passed=%-4d n/a=%-3d refused=%d'
              % (label, out[label]['passed'], out[label]['notApplicable'],
                 out[label]['refused']))
        for r in f.refusals:
            print('    REFUSE %-54s %s'
                  % (r['check'][:54], json.dumps(r['detail'], default=str)[:150]))
    with open(OUT + '/vectors/indep-execution-inputs.json', 'w') as fh:
        json.dump({'standing': __doc__,
                   'derivationInputs': ['retained Plan and execution-plan',
                                        'EnumerationPlanV1 parameter',
                                        'retained SubjectInventoryV1 set',
                                        'captured stage receipts and stage specs',
                                        'returned views / subject-scopes / Coverage payloads',
                                        'admitted vcs-observation',
                                        'published registries and the capability matrix'],
                   'deliberatelyNotRead': ['the evaluation seal and the Run verdict',
                                           'any general "capability is available" notion',
                                           'the retained closure helper\'s own conclusions'],
                   'runs': out, 'totalRefusals': total}, fh, indent=1, default=str)
    print('total refusals:', total)


main()
