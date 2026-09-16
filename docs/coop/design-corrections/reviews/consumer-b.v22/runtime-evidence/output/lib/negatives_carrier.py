"""Discriminating controls for the enumeration CARRIER PAIR (audit area 2).

Each control replaces exactly ONE record's own (state, deficiency, nativeCause) triple and
leaves everything else lawful, so the refusal that appears is the carrier law rather than a
prerequisite. The three distinctions the audit demands each get their own control:

  copied native deficiency   -> the owner carrier law decides the nativeCause
                                (must-be-null / required+allowedCauses / optional)
  local source-syntax-invalid -> nativeCause MUST be null
  complete / absent          -> no pair at all, in either direction

The carrier is checked on the RECORD THAT CARRIES IT: one control targets the
UnavailableProgramBindingV1 and the others target the SubjectInventoryV1, because an inventory's
own pair is not validated by its binding's.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_closure as CL
import run_syntax_code as RSC
import run_syntax_code_full as RSCF

OUT = '/tmp/opensip-design-corrections/consumer-b.v22/output'

CASES = [
    ('inventory-copied-deficiency-whose-required-cause-is-null',
     {'carrier-required-cause-is-null': True},
     'ENUMERATION_CARRIER_INVENTORY:NATIVE_CAUSE_REQUIRED_AND_A_MEMBER_OF_ALLOWED_CAUSES',
     'native x-opensip-deficiency-cause-registry row for language-tier-unsupported: carrier '
     'entry.nativeCause, nativeCause REQUIRED, allowedCauses ["capability-missing"]. '
     'nullIsNotAnEscape: a null there "no longer records an unmade disclosure".'),
    ('inventory-copied-deficiency-with-a-cause-outside-its-allowed-set',
     {'carrier-cause-not-in-allowed-set': True},
     'ENUMERATION_CARRIER_INVENTORY:NATIVE_CAUSE_REQUIRED_AND_A_MEMBER_OF_ALLOWED_CAUSES',
     'the same row: a schema-valid NativeCause that is not in allowedCauses is the '
     '"relabelled cause" the registry exists to refuse'),
    ('inventory-must-be-null-deficiency-carrying-a-cause',
     {'carrier-must-be-null-cause-present': True},
     'ENUMERATION_CARRIER_INVENTORY:NATIVE_CAUSE_MUST_BE_NULL_FOR_THIS_DEFICIENCY',
     'registry row for budget-exhausted: carrier entry.resolutionCompleteness.stageTerminal, '
     'nativeCause must-be-null'),
    # The next three are refused by the OWNING SCHEMA's own allOf branches, BEFORE retained
    # closure. That is the stronger boundary and is reported as observed rather than relabelled
    # to the closure check that would also have caught them.
    ('inventory-local-source-syntax-invalid-carrying-a-native-cause',
     {'carrier-local-member-with-a-cause': True},
     'allOf/6/then/not',
     'subject-inventory.schema.v1.json: the local-member branch itself refuses a non-null '
     'nativeCause ("nativeCause MUST be null for the local member"). Refused at the owning '
     'schema, before closure.'),
    ('complete-inventory-carrying-a-deficiency',
     {'carrier-complete-inventory-with-a-deficiency': True},
     'allOf/1/then/properties/deficiency/type',
     'subject-inventory.schema.v1.json allOf[state=complete] pins deficiency to type null '
     '("null iff state=complete"). Refused at the owning schema.'),
    ('native-cause-without-any-deficiency',
     {'carrier-cause-without-a-deficiency': True},
     'allOf/1/then/properties/nativeCause/type',
     'the same complete branch pins nativeCause to type null; registry.noDeficiencyNoCause '
     'states the reason ("A cause without a deficiency names why nothing went wrong"). '
     'Refused at the owning schema.'),
    ('unavailable-BINDING-whose-required-cause-is-null',
     {'binding-carrier-required-cause-null': True},
     'ENUMERATION_CARRIER_BINDING:NATIVE_CAUSE_REQUIRED_AND_A_MEMBER_OF_ALLOWED_CAUSES',
     'enumeration-contract section 1: the unavailable binding carries "`nativeCause` a '
     'NativeCause member or null AS THAT DEFICIENCY\'S CARRIER LAW REQUIRES"'),
]


def main():
    rows = []
    for label, mut, expect, law in CASES:
        RSC.MUTATE = dict(mut)
        try:
            g = RSCF.complete(RSC.build())
            c = CL.Closure(g['st'])
            rep = c.close_run(g['out']['runId'], label)
            ordered = [r['check'] for r in rep['refusals']]
            row = {'case': label, 'classification': 'invalid', 'mutation': mut,
                   'owningLaw': law, 'builtAndReminted': True,
                   'refused': not rep['admitted'],
                   'firstRefusal': rep['refusals'][0] if rep['refusals'] else None,
                   'orderedRefusalChecks': ordered, 'masksLater': ordered[1:]}
        except Exception as e:
            row = {'case': label, 'classification': 'invalid', 'mutation': mut,
                   'owningLaw': law, 'builtAndReminted': False, 'refused': True,
                   'firstRefusal': {'check': 'BUILD_TIME_ADMISSION_REFUSAL',
                                    'detail': '%s: %s' % (type(e).__name__, str(e)[:400])},
                   'orderedRefusalChecks': ['BUILD_TIME_ADMISSION_REFUSAL'],
                   'masksLater': []}
        finally:
            RSC.MUTATE = {}
        got = json.dumps(row['firstRefusal'] or {})
        row['expectedOwnerJoin'] = expect
        row['firstRefusalIsTheIntendedJoin'] = expect in got
        row['refusalBoundary'] = (
            'owning-schema-admission'
            if (row['firstRefusal'] or {}).get('check') == 'BUILD_TIME_ADMISSION_REFUSAL'
            else 'retained-closure')
        rows.append(row)
        print('%-56s refused=%-5s intended=%-5s boundary=%-24s first=%s'
              % (label[:56], row['refused'], row['firstRefusalIsTheIntendedJoin'],
                 row['refusalBoundary'],
                 (row['firstRefusal'] or {}).get('check', '')[:46]))
    with open(OUT + '/vectors/carrier-negative-controls.json', 'w') as f:
        json.dump({'standing': __doc__, 'controls': rows}, f, indent=1, default=str)
    bad = [r['case'] for r in rows if not r['refused']]
    off = [r['case'] for r in rows if not r['firstRefusalIsTheIntendedJoin']]
    if off:
        print()
        for r in rows:
            if r['case'] in off:
                print('NOT THE INTENDED JOIN: %s\n  expected ~%s\n  ordered %s'
                      % (r['case'], r['expectedOwnerJoin'], r['orderedRefusalChecks'][:4]))
    assert not bad, bad
    print('\nall %d carrier controls refused; %d reached the intended law'
          % (len(rows), len(rows) - len(off)))


main()
