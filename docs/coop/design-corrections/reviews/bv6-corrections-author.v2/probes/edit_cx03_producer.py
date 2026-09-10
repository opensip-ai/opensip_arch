"""Rewrite imported_requirement_outcome per the Codex coherence points."""
import pathlib

P = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v2/work/'
                 'docs/coop/design-corrections/workflows/workflows_model.v1.py')
s = P.read_text(encoding='utf-8')
start = s.index('def imported_requirement_outcome(req, evidence, required=True):')
end = s.index("SEV_ORDER = {'note': 0,")
NEW = '''def imported_requirement_outcome(req, targets, evidence, required=True):
    """The IMPORTED plane's per-requirement reference projection, implementing the published
    per-kind applicability and precedence of the imported-requirement law.

    PRECONDITIONS - this is a PURE projection over inputs that have ALREADY been admitted elsewhere.
    It does not validate an opaque Run, re-derive source correspondence, or admit payload,
    observation scope or polarity: an authenticated importer and the retained Run closure own those.
    Passing it an unadmitted payload produces a meaningless answer, not a refusal.

    INPUT BINDING - every value it reads is named by an owning field, so no untyped caller boolean
    stands in for a measured Run:
      req            a repair EvidenceRequirement. Its `completeness` decides ALL versus ANY over
                     targets: `complete` requires EVERY target supported, `partial-acceptable` at
                     least one. Nothing is added to that record.
      targets        RepairPlanDescriptor.targets - the plan's own targets. They are NOT a field of
                     EvidenceRequirement; the projection is evaluated against the plan being built.
      evidence       the admitted import context for this relation's evidenceKind:
                       available    an admitted import of the kind reached this Run
                       consumable   False for the unmapped-only staleness states
                       runtime:  observability {target: observed-hit|observable-unhit|unobservable|
                                 unmapped}, observationWindow, observedPopulation,
                                 windowSatisfiesRequirement (the recipe's declared demand, an INPUT)
                       history:  covered {target: bool} from collectionScope, present {target: bool}
                                 from subjects, revisionRange, rangeSatisfiesRequirement
      required       the rule's evidenceUse declaration. NEVER defaulted to optional: an unknown or
                     unsupplied declaration is REQUIRED, so an unresolved condition is never silently
                     satisfied.

    History is NOT projected through the runtime fields. HistoryPayloadV1 carries revisionRange and
    collectionScope and has no observationWindow, observedPopulation or observability, so a history
    requirement reports only its own outcomes and a runtime one only its own.

    A satisfied result does NOT mean the evidence is positive: `observed-hit` is positive execution
    evidence and `observable-unhit` is BOUNDED NEGATIVE evidence, and the disclosure says which. An
    optional absence is satisfied by ABSENCE and says so. Nothing here establishes a universal
    negative, and no result changes `deadCodeRepairEligible`, which is decided against the evidence
    Run's own native ClosedWorldV2 before any descriptor exists."""
    plane = requirement_plane(req['relation'])
    if plane != 'imported':
        raise Refusal('CONFIG.INVALID', None,
                      'native.imported-outcome-for-native-relation: ' + str(req['relation'])
                      + ' is a native fact relation; its producer is native section 4.6 '
                      'sufficiency_v2', req['relation'])
    kind = EVIDENCE_RELATIONS[req['relation']]['evidenceKind']
    applicable = IMPORTED_REQUIREMENT_LAW['perKindApplicability'][req['relation']]
    targets = list(targets)
    if not targets:
        raise Refusal('CONFIG.INVALID', None,
                      'native.imported-outcome-without-targets: the projection is per target and the '
                      'plan supplied none', req['relation'])
    every = req['completeness'] == 'complete'
    causes, disclosures = [], []

    def note(cause):
        # A relation may only report an outcome its OWN payload can ground.
        if cause not in applicable:
            raise Refusal('CONFIG.INVALID', None,
                          'native.imported-outcome-not-applicable-to-kind: ' + cause + ' is not an '
                          'outcome of the ' + kind + ' projection', req['relation'])
        causes.append(cause)

    if not evidence.get('available'):
        if not required:
            # The EXISTING optional route, stated rather than re-invented: satisfied BY ABSENCE.
            return {'satisfied': True, 'satisfiedBy': 'declared-optional-absence',
                    'disclosures': [{'kind': 'import-absent', 'code': 'IMPORT.ABSENT_FOR_PREDICATE',
                                     'evidenceKind': kind}]}
        note('evidence-kind-unavailable')
    elif not evidence.get('consumable'):
        note('import-unmapped-only')
    elif kind == 'runtime':
        observability = evidence.get('observability') or {}
        supported = {t for t in targets
                     if observability.get(t) in ('observed-hit', 'observable-unhit')}
        if any(observability.get(t) in ('unobservable', 'unmapped') for t in targets):
            note('subject-not-observable')
        if not evidence.get('windowSatisfiesRequirement', False):
            note('observation-window-insufficient')
        if not (supported >= set(targets) if every else supported):
            note('import-absent-for-requirement')
        if supported and not causes:
            disclosures.append({'kind': 'observation-bounds', 'evidenceKind': kind,
                                'observationWindow': evidence.get('observationWindow'),
                                'observedPopulation': evidence.get('observedPopulation'),
                                'polarity': sorted({observability[t] for t in supported})})
    else:
        covered, present = evidence.get('covered') or {}, evidence.get('present') or {}
        supported = {t for t in targets if present.get(t)}
        if not all(covered.get(t) for t in targets):
            note('history-outside-collection-scope')
        if not evidence.get('rangeSatisfiesRequirement', False):
            note('history-range-insufficient')
        if not (supported >= set(targets) if every else supported):
            note('import-absent-for-requirement')
        if supported and not causes:
            disclosures.append({'kind': 'history-bounds', 'evidenceKind': kind,
                                'revisionRange': evidence.get('revisionRange')})
    if not causes:
        return {'satisfied': True, 'satisfiedBy': 'bounded-observation',
                'disclosures': disclosures}
    order = IMPORTED_REQUIREMENT_LAW['precedence']
    return {'satisfied': False, 'deficiency': min(causes, key=order.index),
            'disclosures': disclosures}


'''
P.write_text(s[:start] + NEW + s[end:], encoding='utf-8')
print('ok')
