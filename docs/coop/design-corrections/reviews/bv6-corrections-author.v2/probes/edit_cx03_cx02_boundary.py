"""CX-BV6-03 plane-tagged field + CX-BV6-02 typed presence law and owning error routing."""
import json, pathlib, collections

W = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v2/work')

# --------------------------------------------------------------- 1. repair.schema.json field
P = W / 'docs/coop/design-corrections/workflows/schemas/repair.schema.json'
d = json.loads(P.read_text(encoding='utf-8'), object_pairs_hook=collections.OrderedDict)
er = d['$defs']['EvidenceRequirement']
dv = er['properties']['deficiency']
assert dv['$ref'] == 'urn:opensip:product-v1:workflows:common#/$defs/NativeSufficiencyDeficiency'

new = collections.OrderedDict()
new['oneOf'] = [
    {'$ref': 'urn:opensip:product-v1:workflows:common#/$defs/NativeSufficiencyDeficiency'},
    {'$ref': 'urn:opensip:product-v1:workflows:common#/$defs/ImportedRequirementDeficiency'},
]
new['description'] = (
    "The reason THIS requirement is unsatisfied, in the vocabulary of THIS requirement's evidence "
    "PLANE. Repair admits a requirement over either plane, so the field carries either vocabulary "
    "and the plane is decided AT ADMISSION from the relation's registry membership - never guessed "
    "from the value and never left to the reader. NATIVE plane (the thirteen relations of "
    "foundation/relation-payload-schemas.v2.json): the value is a DeficiencyV2 member produced by "
    "native-evidence.md section 4.6 `sufficiency_v2` for this requirement against the evidence Run "
    "named by evidenceRunId. IMPORTED plane (`runtime-observation`, `history-change`): the value is "
    "an ImportedRequirementDeficiency produced under "
    "imported-evidence.schema.json#/x-opensip-imported-requirement-law, because those relations mint "
    "no fact2 and have no Coverage entry, so sufficiency_v2 has nothing to range over and is not "
    "asked. A cross-plane value is REFUSED at admission: the two vocabularies are disjoint in "
    "meaning as well as in membership. "
    "WHAT THIS FIELD CARRIES: it is the satisfaction/deficiency PROJECTION of its producer's full "
    "result, not that result. `sufficiency_v2` also returns `causes` on both branches and may return "
    "`disclosures` on a failing branch; those stay with the producer and the retained Coverage and "
    "are deliberately not copied here. "
    "PRESENCE IS TYPED, NOT OPTIONAL: `deficiency` is REQUIRED exactly when `satisfied` is false and "
    "FORBIDDEN when it is true, enforced by the allOf below. `additionalProperties: false` plus that "
    "law means an explicit `null` is refused in BOTH branches - a present key with a null value is "
    "not an absent key - and `satisfied` must be an actual boolean. "
    "WHY NOT D9Deficiency, which this field named before: four of the nine native outcomes are not "
    "members of it, so the field could not express its own producer's result, and its D9-mapped "
    "value is the same `verdict-indeterminate` for all four - conflating `resolution-incomplete`, "
    "the outcome that decides a destructive unused-code repair, with three unrelated causes. "
    "D9Deficiency is unchanged and still carries every whole-Run and comparison-step termination. "
    "THIS FIELD IS NOT AN AUTHORIZATION: the sealed Run named by evidenceRunId remains the authority, "
    "`applicable` is false whenever any requirement is unsatisfied, EVERY delete and EVERY replace is "
    "decided against that Run's own native ClosedWorldV2 before any descriptor exists - which no "
    "imported requirement can change - and apply requires a security authorization bound to the exact "
    "repairPlanId, which every edit to this value moves."
)
new['x-opensip-vocabulary'] = collections.OrderedDict([
    ('nativePlaneAuthority', 'native/native-evidence.schemas.v2.json#/$defs/DeficiencyV2'),
    ('importedPlaneAuthority',
     'workflows/schemas/imported-evidence.schema.json#/x-opensip-imported-requirement-law/outcomes'),
    ('planeDecidedBy',
     'the relation registry the relation belongs to, read at admission by '
     'workflows_model.admit_evidence_requirement; the same separation the imported-evidence '
     'evidenceDeclarationRule already makes'),
    ('producers', ['native-evidence.md section 4.6 sufficiency_v2 (native plane)',
                   'workflows_model.imported_requirement_outcome (imported plane)']),
])
er['properties']['deficiency'] = new
P.write_text(json.dumps(d, indent=2, ensure_ascii=True) + '\n', encoding='utf-8')

# --------------------------------------------------------------- 2. the boundary
Q = W / 'docs/coop/design-corrections/workflows/workflows_model.v1.py'
s = Q.read_text(encoding='utf-8')

OLD = s[s.index("NATIVE_SUFFICIENCY_DEFICIENCIES = list(canonical.parse("):s.index("SEV_ORDER = {'note': 0,")]
NEW = '''NATIVE_SUFFICIENCY_DEFICIENCIES = list(canonical.parse(
    (Path(__file__).resolve().parent.parent / 'native' / 'native-evidence.schemas.v2.json').read_bytes()
)['$defs']['DeficiencyV2']['enum'])
# The IMPORTED plane's own outcome vocabulary and precedence, read from the law that owns those two
# relations. It is a DIFFERENT set from the native one and the two never mix: DeficiencyV2 speaks of
# Coverage states, rungs, universes and resolution completeness, none of which an imported
# observation has, and these members speak of evidence-kind availability, unmapped-only staleness,
# subject observability and observation window/population, none of which a native view has.
IMPORTED_REQUIREMENT_LAW = canonical.parse(
    (Path(__file__).resolve().parent / 'schemas' / 'imported-evidence.schema.json').read_bytes()
)['x-opensip-imported-requirement-law']
IMPORTED_REQUIREMENT_DEFICIENCIES = list(IMPORTED_REQUIREMENT_LAW['precedence'])


def requirement_plane(relation):
    """Which evidence plane a repair EvidenceRequirement's relation belongs to.

    Read from registry MEMBERSHIP, never from the deficiency value and never from a naming
    convention: EVIDENCE_RELATIONS is the imported-evidence registry and RELATION_LADDERS carries
    both, so a relation in neither is not a requirement relation at all and `admit_atom` has already
    refused it before this is asked."""
    return 'imported' if relation in EVIDENCE_RELATIONS else 'native'


def admit_evidence_requirement(req):
    """Close ONE repair EvidenceRequirement at the producer/consumer boundary and return
    (plane, exact cause or None).

    Repair CONSUMES a per-requirement outcome and mints none of its own. Two producers own the two
    planes - native section 4.6 `sufficiency_v2` for the thirteen native fact relations, and
    `imported_requirement_outcome` under the imported-evidence requirement law for the two imported
    relations - and this boundary decides which vocabulary the record may carry.

    The presence law is TYPED, and it is re-decided here rather than trusted because two boundaries
    that both claim to decide one law must agree:

      * `satisfied` must be an actual boolean. `1` is not `True` here: isinstance(1, bool) is False,
        and the owning schema's `type: boolean` refuses it too. An earlier revision used truthiness
        and admitted it.
      * PRESENCE is distinguished from VALUE. A present `deficiency` key whose value is null is NOT
        an absent key, and the owning schema refuses it in both branches - `additionalProperties:
        false` plus the presence law. An earlier revision used `req.get('deficiency')`, which
        conflated the two and admitted `{satisfied: true, deficiency: null}`.
      * REQUIRED exactly when satisfied is false, FORBIDDEN when true.
      * the value must belong to THIS requirement's plane. A native requirement carrying an imported
        outcome, or the reverse, is a category error and refuses.

    ROUTING: every violation here is a malformed repair REQUEST, so it refuses CONFIG.INVALID -
    the same class `validate_import_record` and `admit_atom` use for a malformed input - and not
    REQUEST.PRECONDITION_FAILED, which is for a well-formed request whose preconditions are unmet.
    No public DomainDetailCode is added; the internal decision key travels in the remedy.

    This is a DISCLOSURE admission, never an authorization: the sealed Run named by `evidenceRunId`
    remains the evidence authority, `applicable` is still false whenever any requirement is
    unsatisfied, EVERY delete and EVERY replace is decided against that Run's own native
    ClosedWorldV2 before any descriptor exists, and apply still requires a security authorization
    bound to the exact repairPlanId. No value returned here substitutes for any of that."""
    plane = requirement_plane(req['relation'])
    vocabulary = (IMPORTED_REQUIREMENT_DEFICIENCIES if plane == 'imported'
                  else NATIVE_SUFFICIENCY_DEFICIENCIES)
    other = (NATIVE_SUFFICIENCY_DEFICIENCIES if plane == 'imported'
             else IMPORTED_REQUIREMENT_DEFICIENCIES)

    def refuse(key, why):
        raise Refusal('CONFIG.INVALID', None, key + ': ' + why, req['relation'])

    if not isinstance(req['satisfied'], bool):
        refuse('native.sufficiency-outcome-satisfied-not-boolean',
               'satisfied must be a boolean; ' + repr(req['satisfied']) + ' is not')
    present = 'deficiency' in req
    if req['satisfied']:
        if present:
            refuse('native.sufficiency-outcome-on-satisfied-requirement',
                   'a satisfied requirement carries no deficiency key at all, not even a null; its '
                   'producer returns disclosures rather than a deficiency when it is satisfied')
        return plane, None
    if not present:
        refuse('native.sufficiency-outcome-missing',
               'an unsatisfied requirement must carry the outcome that made it unsatisfied')
    value = req['deficiency']
    if value is None:
        refuse('native.sufficiency-outcome-null',
               'an explicit null is not an outcome; a present key with a null value is not an '
               'absent key and the owning schema refuses it')
    if value in other:
        refuse('native.sufficiency-outcome-wrong-plane',
               str(value) + ' belongs to the ' + ('native' if plane == 'imported' else 'imported')
               + ' plane, but relation ' + str(req['relation']) + ' is on the ' + plane + ' plane')
    if value not in vocabulary:
        refuse('native.sufficiency-outcome-not-a-native-outcome' if plane == 'native'
               else 'native.sufficiency-outcome-not-an-imported-outcome',
               str(value) + ' is not a member of the ' + plane + ' per-requirement vocabulary '
               + str(vocabulary))
    return plane, value


def imported_requirement_outcome(req, evidence, required=True):
    """The IMPORTED plane's per-requirement producer, implementing the published precedence.

    `evidence` is the admitted imported-evidence context for THIS requirement's evidenceKind, a
    trusted model input exactly as the native view is for sufficiency_v2:
      available            bool   - an import of this kind reached this Run at all
      consumable           bool   - False for the unmapped-only staleness states, which never feed
                                    a predicate and therefore never support a requirement either
      observability        {target: observed-hit|observable-unhit|unobservable|unmapped}
      windowSatisfiesRequirement  bool - the payload's observationWindow/observedPopulation meet
                                    what the requirement asks; carried, never inferred
    `req['targets']` are the subjects the requirement is about, so the decision is PER TARGET and
    never a statement about the payload as a whole.

    Returns {satisfied, deficiency?, disclosures}. What it never returns is a universal negative:
    `observable-unhit` is bounded negative evidence about ONE window, not `unused`, and no result of
    this function changes `deadCodeRepairEligible`, which is decided against the evidence Run's own
    native ClosedWorldV2 before any descriptor exists."""
    if requirement_plane(req['relation']) != 'imported':
        raise Refusal('CONFIG.INVALID', None,
                      'native.imported-outcome-for-native-relation: ' + str(req['relation'])
                      + ' is a native fact relation; its producer is native section 4.6 '
                      'sufficiency_v2', req['relation'])
    targets = list(req.get('targets') or [])
    disclosures = []
    causes = []
    if not evidence.get('available'):
        if not required:
            # The EXISTING optional-evidence route, unchanged and not re-invented here.
            return {'satisfied': True,
                    'disclosures': [{'kind': 'import-absent', 'code': 'IMPORT.ABSENT_FOR_PREDICATE'}]}
        causes.append('evidence-kind-unavailable')
    elif not evidence.get('consumable'):
        causes.append('import-unmapped-only')
    else:
        observability = evidence.get('observability') or {}
        if any(observability.get(t) in ('unobservable', 'unmapped') for t in targets):
            causes.append('subject-not-observable')
        if not evidence.get('windowSatisfiesRequirement', False):
            causes.append('observation-window-insufficient')
        if not any(observability.get(t) in ('observed-hit', 'observable-unhit') for t in targets):
            causes.append('import-absent-for-requirement')
    if not causes:
        # Positive, BOUNDED evidence: the window and population travel with it, and it is never a
        # universal negative about anything outside them.
        disclosures.append({'kind': 'observation-bounds',
                            'observationWindow': evidence.get('observationWindow'),
                            'observedPopulation': evidence.get('observedPopulation')})
        return {'satisfied': True, 'disclosures': disclosures}
    order = IMPORTED_REQUIREMENT_LAW['precedence']
    return {'satisfied': False, 'deficiency': min(causes, key=order.index),
            'disclosures': disclosures}


'''
s = s.replace(OLD, NEW)

# repair_preview consumes the (plane, cause) pair
OLD2 = """        deficiency = admit_evidence_requirement(req)
        if not req['satisfied']:
            unmet.append({'code': 'REPAIR.EVIDENCE_RUN_UNAVAILABLE',
                          'remedy': 'evidence requirement unsatisfied: ' + req['relation'] + '@'
                                    + req['minResolution'] + ' (' + deficiency + ')'})
"""
NEW2 = """        plane, deficiency = admit_evidence_requirement(req)
        if not req['satisfied']:
            unmet.append({'code': 'REPAIR.EVIDENCE_RUN_UNAVAILABLE',
                          'remedy': 'evidence requirement unsatisfied: ' + req['relation'] + '@'
                                    + req['minResolution'] + ' (' + plane + ': ' + deficiency + ')'})
"""
assert s.count(OLD2) == 1
s = s.replace(OLD2, NEW2)
Q.write_text(s, encoding='utf-8')
print('ok')
