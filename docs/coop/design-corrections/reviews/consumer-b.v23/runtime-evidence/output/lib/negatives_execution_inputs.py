"""Discriminating controls for the ExecutionInputsV1 laws (audit area 3).

Each control replaces exactly ONE element of the HOST record -- one account, one outcome row, one
receipt set, one selected reference -- and leaves every other record lawful. The whole graph is
then REMINTED and re-closed, so the tampered graph is hash-consistent and linkage-valid and only
semantic re-derivation can refuse it. Every row below reports the ACTUAL first refusal and the
checks it masked; where the first refusal is a different (earlier) law than the one under test,
that boundary is reported as measured rather than relabelled.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_closure as CL
import run_syntax_code as RSC
import run_syntax_code_full as RSCF

OUT = '/tmp/opensip-design-corrections/consumer-b.v23/output'

CASES = [
    ('applicability-not-the-derived-first-match',
     'EXECUTION_INPUTS_COVERAGE_DERIVE:APPLICABILITY_IS_THE_DERIVED_FIRST_MATCH',
     'generation 20: NativeCoverageAccountV1 x-opensip-applicability-precedence is a NORMATIVE '
     'FIRST-MATCH order in which `unsupported-typed` outranks both unavailable tokens. The mutation '
     'sets the value generation 19 would have produced for this account '
     '(`unavailable-unselected` on an UNSUPPORTED-TYPED cell with an unselected enumerator), so '
     'this control measures the clause that changed this origin\'s own answer.'),
    ('source-universe-nulled-on-a-non-supported-account',
     'EXECUTION_INPUTS_COVERAGE_DERIVE:SOURCE_UNIVERSE_IS_THE_BINDING_COORDINATE_FOR_EVERY_'
     'APPLICABILITY',
     'x-opensip-external-joins: sourceUniverse IS the binding universe for EVERY applicability, '
     'and the mutation applies the rule the kit names and rejects -- "NOT null whenever '
     'coverageIds is empty"'),
    ('carrier-manufactured-for-pure-missing-work',
     'EXECUTION_INPUTS_OUTCOME_DERIVE:PRIMARY_PAIR',
     'x-opensip-derived-carrier-law pureMissingWork: a census-driven incomplete account carries '
     '(null, null) and "It is NOT provider-unavailable: that would assert a provider observation '
     'occurring on no source record"'),
    ('owed-matrix-account-dropped',
     'EXECUTION_INPUTS_NATIVE_COVERAGE_TOTALITY:ONE_ACCOUNT_PER_OWED_MATRIX_PAIR',
     'the owed account set is programBindings ordinal x the matrix capabilities[id].relations '
     'array; dropping one owed pair is not a host choice'),
    ('account-relabelled-unsupported-on-a-supported-matrix-cell',
     'EXECUTION_INPUTS_COVERAGE_DERIVE:APPLICABILITY_IS_THE_DERIVED_FIRST_MATCH',
     'section 5: `unsupported-typed` carries "the matrix cell deficiency"; the matrix row for '
     '(syntax, syntax-only) is SUPPORTED-DESIGN with deficiency null, so a relation whose '
     'partition WAS returned cannot be relabelled unsupported. This is the V19-D3 defect class '
     'turned into a control, and on the first measured run the retained closure did NOT refuse '
     'it -- the law was ported because this control exposed the omission.'),
    ('coverage-ids-narrowed-to-a-subset',
     'EXECUTION_INPUTS_COVERAGE_DERIVE:COVERAGE_IDS_EQUAL_EVERY_MATCHING_RETURNED_PARTITION',
     'section 5: coverageIds "EQUALS every matching returned partition (not a complete subset)"'),
    ('fabricated-coverage-at-a-null-universe',
     'allOf/0/then/properties/coverageIds/maxItems',
     'section 5 "none -- do not fabricate Coverage at null U" is ALSO pinned by the owning '
     'schema: NativeCoverageAccountV1.allOf[0] sets coverageIds.maxItems 0 for the four '
     'non-supported kinds, so this refuses at owning-schema admission BEFORE retained closure. '
     'Measured and reported as the stronger boundary rather than relabelled to the closure '
     'check that would also have caught it.'),
    ('complete-row-over-an-incomplete-account',
     'EXECUTION_INPUTS_OUTCOME_DERIVE:STATE',
     'section 4: "any supported-available account not complete -> partial"; the host cannot mint '
     'a complete semantic by asserting the row'),
    ('unzipped-carrier-pair',
     'EXECUTION_INPUTS_OUTCOME_DERIVE:PRIMARY_PAIR',
     'section 4: the row pair EQUALS the derived primary pair and must be a MEMBER of the owned '
     'source pairs -- "not an unzipped first-deficiency plus a later unrelated nativeCause"'),
    ('view-attributed-without-a-receipt',
     'EXECUTION_INPUTS_OUTPUT_BACKLINK:OUTCOME_VIEWS_COME_FROM_THE_CAPTURED_RECEIPT',
     'viewDigests DESC: "Must equal captured receipt views attributed to this '
     'cell/program/U/producer"'),
    ('null-stage-reason-swapped',
     'EXECUTION_INPUTS_STAGE_ORDINAL:NULL_REASON_IS_DERIVED_FROM_THE_BINDING_SHAPE',
     'section 3 + enumeration-plan UnselectedEnumeratorRef: an optional-unselected binding\'s '
     'typed null reason is derived from the binding shape, not asserted'),
    ('receipt-set-not-total-over-the-stages',
     'ORDER_ORDINAL_NOT_CONTIGUOUS_ZERO_BASED',
     'moving the only receipt to ordinal 1 is refused EARLIER than the totality law, by the '
     'published `x-opensip-order: ordinal` keyword on hostCapture.stageReceipts. Measured and '
     'reported as the stronger boundary; the totality law itself is reached by the next control.'),
    ('execution-plan-stage-without-a-receipt',
     'EXECUTION_INPUTS_RECEIPT_TOTALITY:ONE_RECEIPT_PER_ADMITTED_STAGE',
     'section 1: "one receipt per stage, ordinals unique and total" over the admitted '
     'execution-plan stages -- a silently unreported producer obligation is not an absent one'),
    ('captured-view-coverage-left-unselected',
     'EXECUTION_INPUTS_SELECTED_COVER:EVERY_RETURNED_VIEW_COVERAGE_IS_SELECTED',
     'section 1 selectedRefs table: coverage equals "every coverageIds member of those captured '
     'returned views"'),
    ('inventory-kind-dropped-from-the-outcome',
     'EXECUTION_INPUTS:OUTCOME_INVENTORY_DIGESTS_ARE_THE_RETAINED_SET',
     'section 4: inventory digests are "exactly one per kind, kinds set-equal to the cell"'),
]


def main():
    rows = []
    for label, expect, law in CASES:
        RSCF.MUTATE = {label: True}
        try:
            g = RSCF.complete(RSC.build())
            c = CL.Closure(g['st'])
            rep = c.close_run(g['out']['runId'], label)
            ordered = [r['check'] for r in rep['refusals']]
            row = {'case': label, 'classification': 'invalid', 'owningLaw': law,
                   'builtAndReminted': True, 'refused': not rep['admitted'],
                   'firstRefusal': rep['refusals'][0] if rep['refusals'] else None,
                   'orderedRefusalChecks': ordered, 'masksLater': ordered[1:],
                   'checksPassedBeforeRefusal': rep['checksPassed']}
        except Exception as e:
            row = {'case': label, 'classification': 'invalid', 'owningLaw': law,
                   'builtAndReminted': False, 'refused': True,
                   'firstRefusal': {'check': 'BUILD_TIME_ADMISSION_REFUSAL',
                                    'detail': '%s: %s' % (type(e).__name__, str(e)[:400])},
                   'orderedRefusalChecks': ['BUILD_TIME_ADMISSION_REFUSAL'], 'masksLater': []}
        finally:
            RSCF.MUTATE = {}
        first = (row['firstRefusal'] or {}).get('check', '')
        row['expectedOwnerJoin'] = expect
        row['firstRefusalIsTheIntendedJoin'] = expect in json.dumps(row['firstRefusal'] or {})
        row['refusalBoundary'] = ('owning-schema-admission'
                                  if first == 'BUILD_TIME_ADMISSION_REFUSAL'
                                  else 'retained-closure')
        # where an earlier law fires first, record WHERE the intended law appeared in the ordered
        # refusal list instead of relabelling the boundary
        hits = [i for i, ch in enumerate(row['orderedRefusalChecks']) if expect in ch]
        row['intendedLawPositionInOrderedRefusals'] = (hits[0] if hits else None)
        row['maskedByEarlierLaws'] = (row['orderedRefusalChecks'][:hits[0]] if hits else
                                      row['orderedRefusalChecks'][:1])
        rows.append(row)
        print('%-54s refused=%-5s intended=%-5s first=%s'
              % (label[:54], row['refused'], row['firstRefusalIsTheIntendedJoin'], first[:58]))
    with open(OUT + '/vectors/execution-inputs-negative-controls.json', 'w') as f:
        json.dump({'standing': __doc__, 'controls': rows}, f, indent=1, default=str)
    bad = [r['case'] for r in rows if not r['refused']]
    off = [r['case'] for r in rows if not r['firstRefusalIsTheIntendedJoin']]
    for r in rows:
        if r['case'] in off:
            print('\nNOT THE INTENDED JOIN: %s\n  expected ~%s\n  ordered  %s'
                  % (r['case'], r['expectedOwnerJoin'], r['orderedRefusalChecks'][:5]))
    assert not bad, bad
    print('\nall %d execution-inputs controls refused; %d reached the intended law'
          % (len(rows), len(rows) - len(off)))


main()
