import pathlib

P = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v1/work/'
                 'docs/coop/design-corrections/workflows/workflows_model.v1.py')
s = P.read_text(encoding='utf-8')

# --- 1. the authority, READ not restated, beside the other read authorities -----------------
ANCHOR = """    return have_i >= need_i


SEV_ORDER = {'note': 0, 'warning': 1, 'error': 2}
"""
NEW = '''    return have_i >= need_i


# The per-requirement sufficiency OUTCOME vocabulary, READ from its owning authority rather than
# restated here: native/native-evidence.schemas.v2.json#/$defs/DeficiencyV2, whose only defined
# producer is native-evidence.md section 4.6 `sufficiency_v2`. It is NOT D9Deficiency: four of these
# nine members (derivation-policy-unmet, external-consumers-unknown, input-closure-incomplete,
# resolution-incomplete) have no D9Deficiency member at all, and the D9-mapped value for all four is
# the same `verdict-indeterminate`, so a D9-typed per-requirement field could only be schema-invalid
# for four of nine outcomes, collapse them into one, or drop the disclosure. The workflows schema
# bundle mirrors this enum as common#/$defs/NativeSufficiencyDeficiency because that bundle resolves
# only workflows URNs; check-integration.py holds the two equal.
NATIVE_SUFFICIENCY_DEFICIENCIES = list(canonical.parse(
    (Path(__file__).resolve().parent.parent / 'native' / 'native-evidence.schemas.v2.json').read_bytes()
)['$defs']['DeficiencyV2']['enum'])


def admit_evidence_requirement(req):
    """Close ONE repair EvidenceRequirement's (satisfied, deficiency) pair at the producer/consumer
    boundary, and return the exact native cause or None.

    `sufficiency_v2` is total and its result shape is closed: {satisfied: true, disclosures} with no
    deficiency, or {satisfied: false, deficiency} carrying exactly one DeficiencyV2 member. Repair
    CONSUMES that result and mints no sufficiency verdict of its own, so the record has no lawful
    third shape and the schema presence law is re-decided here rather than trusted:

      * a deficiency on a SATISFIED requirement contradicts its own producer;
      * an UNSATISFIED requirement with no deficiency drops the only disclosure of why the repair is
        inapplicable, which was previously schema-valid and left three conforming readings open;
      * a value outside the native vocabulary - notably the D9 spellings `verdict-indeterminate` and
        `none`, which the field's former D9Deficiency type admitted - is not a native outcome and is
        refused rather than silently read as one.

    This is a DISCLOSURE admission, never an authorization: the sealed Run named by `evidenceRunId`
    remains the evidence authority, `applicable` is still false whenever any requirement is
    unsatisfied, and apply still requires a security authorization bound to the exact repairPlanId.
    No boolean derived here substitutes for either."""
    deficiency = req.get('deficiency')
    if req['satisfied']:
        if deficiency is not None:
            raise Refusal('REQUEST.PRECONDITION_FAILED', None,
                          'native.sufficiency-outcome-on-satisfied-requirement: a satisfied '
                          'requirement carries no deficiency; sufficiency_v2 returns disclosures, '
                          'not a deficiency, when it is satisfied', req['relation'])
        return None
    if deficiency is None:
        raise Refusal('REQUEST.PRECONDITION_FAILED', None,
                      'native.sufficiency-outcome-missing: an unsatisfied requirement must carry '
                      'the sufficiency_v2 outcome that made it unsatisfied', req['relation'])
    if deficiency not in NATIVE_SUFFICIENCY_DEFICIENCIES:
        raise Refusal('REQUEST.PRECONDITION_FAILED', None,
                      'native.sufficiency-outcome-not-a-native-outcome: ' + str(deficiency) +
                      ' is not a member of the native per-requirement sufficiency vocabulary ' +
                      str(NATIVE_SUFFICIENCY_DEFICIENCIES), req['relation'])
    return deficiency


SEV_ORDER = {'note': 0, 'warning': 1, 'error': 2}
'''
assert s.count(ANCHOR) == 1
s = s.replace(ANCHOR, NEW)

# --- 2. repair_preview consumes the exact cause ---------------------------------------------
OLD = """        admit_atom({'relation': req['relation'], 'minResolution': req['minResolution'],
                    'evidence': EVIDENCE_RELATIONS.get(req['relation'], {}).get('evidenceKind')})
        if not req['satisfied']:
            unmet.append({'code': 'REPAIR.EVIDENCE_RUN_UNAVAILABLE', 'remedy': 'evidence requirement unsatisfied: ' + req['relation']})
"""
NEW2 = """        admit_atom({'relation': req['relation'], 'minResolution': req['minResolution'],
                    'evidence': EVIDENCE_RELATIONS.get(req['relation'], {}).get('evidenceKind')})
        # The (satisfied, deficiency) pair is admitted against the NATIVE sufficiency vocabulary
        # that produced it, and the exact cause is carried into the unmet precondition rather than
        # discarded: `resolution-incomplete` and `external-consumers-unknown` are different remedies
        # for the same false `satisfied`, and a caller that cannot tell them apart cannot act.
        deficiency = admit_evidence_requirement(req)
        if not req['satisfied']:
            unmet.append({'code': 'REPAIR.EVIDENCE_RUN_UNAVAILABLE',
                          'remedy': 'evidence requirement unsatisfied: ' + req['relation'] + '@'
                                    + req['minResolution'] + ' (' + deficiency + ')'})
"""
assert s.count(OLD) == 1
s = s.replace(OLD, NEW2)

P.write_text(s, encoding='utf-8')
print('ok')
