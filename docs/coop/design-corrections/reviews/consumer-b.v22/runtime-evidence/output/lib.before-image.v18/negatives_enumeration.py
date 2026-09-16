"""Distinguishing controls for the ENUMERATION contract (audit areas 2 and 3).

Every control is a lawful-LOOKING enumeration record that one published clause refuses, applied
at BUILD time so the whole graph is reminted and reclosed, with the ACTUAL first refusal
reported. These exist because the v16 checker validated the enumeration plan not at all: it
read the plan only to index cells. A passing emitter plus a passing replay proved nothing about
a clause both omitted.

The unavailable-binding controls are the direct test of the v16 advisory V16-A2, which claimed
the unavailable case was NOT STATED and that no inventory exists for it. The clauses say the
opposite, and these controls show the difference between a MISSING record and a retained
`unavailable` record.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_closure as CL
import run_syntax_code as RSC
import run_syntax_code_full as RSCF

OUT = '/tmp/opensip-design-corrections/consumer-b.v18/output'

CASES = [
    ('file-extent-narrowed-to-the-compiler-or-grammar-readable-paths',
     {'file-extent-compiler-filtered': True},
     'ENUMERATION_FILE_EXTENT_IS_FIRST_PARTY_SCOPED_SNAPSHOT_MEMBERSHIP',
     'enumeration-contract section 5 + x-opensip-file-membership-extent-law.fileKind: '
     '"Every remaining inventoried first-party snapshot path ... REGARDLESS of compiler-mode '
     'program-member. Inventory is not grammar-gated."'),
    ('inventory-cell-kinds-narrowed-to-a-consumer-chosen-subset',
     {'inventory-cell-kinds-consumer-subset': True},
     'ENUMERATION_CELL_KINDS_DERIVED_FROM_THE_REGISTRY',
     'section 1: `kinds` is the stored enum set from x-opensip-kind-derivation -- "an '
     '`inventory` cell stores `file` and `package`; it is not two cells"'),
    ('package-extent-includes-a-manifest-that-mints-no-named-subject',
     {'package-extent-includes-a-nameless-manifest': True},
     'ENUMERATION_EXTENT_PATH_IS_A_SNAPSHOT_MEMBER',
     'section 4/8: the package candidate extent is NAMED first-party manifests union '
     'parse/classification failures; a nameless or workspace-only manifest is not a subject '
     'and is not in the candidate extent. (This mutation also names a non-member path, which '
     'is the earlier guard and is reported as the actual first refusal.)'),
    ('file-inventory-drops-one-extent-path',
     {'file-inventory-drops-an-extent-path': True},
     'ENUMERATION_INVENTORY_FILE_TOTALITY',
     'section 4: complete + kind=file means the parsed rows[].path set EQUALS that binding\'s '
     'file extent; omission is ENUMERATION_INVENTORY_FILE_TOTALITY'),
    ('unavailable-binding-drops-its-host-extents',
     {'unavailable-binding-drops-extents': True},
     'ENUMERATION_BINDING_EXTENT_KINDS_EQUAL_THE_CELL_KINDS',
     'section 1, unavailable binding: "`extents` still populated from host membership so '
     'expected file/package paths are not lost"'),
    ('the-unavailable-cells-retained-inventory-is-missing-entirely',
     {'drop-the-unavailable-inventory': True},
     'ENUMERATION_INVENTORY_MISSING_RECORD',
     'section 4 + execution-inputs section 6: exactly one SubjectInventoryV1 per '
     '(cellOrdinal, programOrdinal, kind) with NO available-only qualifier; "Unselected or '
     '`universe=null` does not discard same-cell inventory items." A missing record is not a '
     'retained unavailable record -- this is the control that refutes V16-A2.'),
    ('two-inventories-for-one-cell-program-kind',
     {'two-inventories-for-one-cell-program-kind': True},
     'ENUMERATION_EXACTLY_ONE_INVENTORY_PER_CELL_PROGRAM_KIND',
     'section 4: EXACTLY one per (cellOrdinal, programOrdinal, kind)'),
    ('membership-row-missing-for-a-snapshot-path',
     {'membership-row-missing-for-a-snapshot-path': True},
     'ENUMERATION_MEMBERSHIP_ROWS_EXACTLY_COVER_THE_SNAPSHOT',
     'section 8: "Membership rows must exactly cover snapshot paths (host TCB); a missing row '
     'is not a silent exclude."'),
    # ---- v18: binding provenance / default selection and the U-1..U-4 unit law
    ('default-unit-binding-names-a-program-entry',
     {'default-unit-names-a-program-entry': True},
     'ENUMERATION_BINDING_PROGRAM_ENTRY',
     'enumeration-plan.schema.v1.json #/$defs/AvailableProgramBindingV1/properties/'
     'programEntry: "U-1 DEFAULT USES NULL". A filename that happens to exist is not the '
     'derivation, and a default unit is not a Plan-selected extra program.'),
    ('a-unit-no-U1-marker-derives',
     {'invent-a-unit-no-marker-derives': True},
     'ENUMERATION_U1_UNIT_COUNT_DERIVED_FROM_THE_SNAPSHOT',
     'native-evidence section 1.4 U-1: a `tsjs` unit exists ONLY where a directory holds '
     'tsconfig.json | jsconfig.json | package.json, and U-4 adds that a file with no unit is '
     '"NOT a member of an invented unit"'),
    ('membership-row-family-not-fixed-by-extension',
     {'row-family-not-fixed-by-extension': True},
     'ENUMERATION_U3_FAMILY_IS_FIXED_BY_EXTENSION',
     'native-evidence section 1.4 U-3: "A file\'s family is fixed by extension ... Units of '
     'another family never claim it." package.json is not a tsjs-extension file.'),
    ('two-bindings-in-one-cell-sharing-one-universe',
     {'duplicate-universe-inside-one-cell': True},
     'ENUMERATION_BINDING_DUPLICATE_UNIVERSE',
     'enumeration-plan.schema.v1.json #/$defs/CellObligationV1/properties/programBindings: '
     '"Duplicate available universe H inside one cell refuses '
     'ENUMERATION_BINDING_DUPLICATE_UNIVERSE"'),
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
                   'runId': g['out']['runId'],
                   'closureChecksPassed': rep['checksPassed'],
                   'refused': not rep['admitted'],
                   'firstRefusal': rep['refusals'][0] if rep['refusals'] else None,
                   'orderedRefusalChecks': ordered,
                   'masksLater': ordered[1:]}
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
        rows.append(row)
        print('%-58s refused=%-5s intended=%-5s first=%s'
              % (label[:58], row['refused'], row['firstRefusalIsTheIntendedJoin'],
                 (row['firstRefusal'] or {}).get('check')))
    doc = {'standing': __doc__, 'classification': 'invalid', 'controls': rows}
    with open(OUT + '/vectors/enumeration-negative-controls.json', 'w') as f:
        json.dump(doc, f, indent=1, default=str)
    bad = [r['case'] for r in rows if not r['refused']]
    off = [r['case'] for r in rows if not r['firstRefusalIsTheIntendedJoin']]
    if off:
        print()
        for r in rows:
            if r['case'] in off:
                print('NOT THE INTENDED JOIN: %s\n  expected ~%s\n  ordered %s'
                      % (r['case'], r['expectedOwnerJoin'],
                         r['orderedRefusalChecks'][:5]))
    assert not bad, bad
    print('\nall %d enumeration controls refused; %d reached the intended law'
          % (len(rows), len(rows) - len(off)))


main()
