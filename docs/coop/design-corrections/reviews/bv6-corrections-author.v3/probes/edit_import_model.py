"""BV6-V3-IMPORT-BINDING + IMPORT-CAUSE + IMPORT-SEMANTICS in the reference model."""
import pathlib

P = pathlib.Path('/private/tmp/opensip-design-corrections/bv6-corrections-author.v3/work/'
                 'docs/coop/design-corrections/workflows/workflows_model.v1.py')
s = P.read_text(encoding='utf-8')

# ---------------------------------------------------------------- 1. per-kind consumer check
OLD = """    if value in other:
        refuse('native.sufficiency-outcome-wrong-plane',
               str(value) + ' belongs to the ' + ('native' if plane == 'imported' else 'imported')
               + ' plane, but relation ' + str(req['relation']) + ' is on the ' + plane + ' plane')
    if value not in vocabulary:
        refuse('native.sufficiency-outcome-not-a-native-outcome' if plane == 'native'
               else 'native.sufficiency-outcome-not-an-imported-outcome',
               str(value) + ' is not a member of the ' + plane + ' per-requirement vocabulary '
               + str(vocabulary))
    return plane, value
"""
NEW = """    if value in other:
        refuse('native.sufficiency-outcome-wrong-plane',
               str(value) + ' belongs to the ' + ('native' if plane == 'imported' else 'imported')
               + ' plane, but relation ' + str(req['relation']) + ' is on the ' + plane + ' plane')
    if value not in vocabulary:
        refuse('native.sufficiency-outcome-not-a-native-outcome' if plane == 'native'
               else 'native.sufficiency-outcome-not-an-imported-outcome',
               str(value) + ' is not a member of the ' + plane + ' per-requirement vocabulary '
               + str(vocabulary))
    if plane == 'imported':
        # PER-KIND, not merely per plane. The producer already refuses an outcome a relation's own
        # payload cannot ground; the consumer must decide the SAME law, or a record can carry a
        # history range outcome on a runtime relation - which the published perKindApplicability
        # excludes and which an earlier revision of this boundary admitted.
        applicable = IMPORTED_REQUIREMENT_LAW['perKindApplicability'][req['relation']]
        if value not in applicable:
            refuse('native.sufficiency-outcome-not-applicable-to-kind',
                   str(value) + ' is not an outcome of the '
                   + EVIDENCE_RELATIONS[req['relation']]['evidenceKind'] + ' projection that owns '
                   + str(req['relation']) + '; its applicable outcomes are ' + str(applicable))
    return plane, value
"""
assert s.count(OLD) == 1
s = s.replace(OLD, NEW)

# ---------------------------------------------------------------- 2. the projection + producer
start = s.index('def imported_requirement_outcome(')
end = s.index("SEV_ORDER = {'note': 0,")
NEW2 = '''def project_targets_to_imported_subjects(targets, kind, findings, fingerprint_descriptors,
                                         payload_subjects):
    """The DETERMINISTIC target -> imported-subject projection published at
    imported-evidence.schema.json#/x-opensip-imported-requirement-law/targetSubjectProjection.

    RepairPlanDescriptor.targets are FINGERPRINTS (`finding-key2:<64 hex>`), while RuntimeSubject is
    keyed by {path, symbol?} and HistorySubject by {path}. They are different vocabularies and this
    is the join between them. An earlier revision read the payload maps directly by the target
    string, which silently equated a finding-key identity with a LogicalPath.

    INPUTS, all already admitted elsewhere - this function READS, it does not admit:
      findings                {fingerprint: finding record} of the EVIDENCE RUN named by
                              RepairPlanDescriptor.evidenceRunId. repair_preview already refuses a
                              target absent from that Run, so this is the same binding.
      fingerprint_descriptors {fingerprint: foundation `finding-fingerprint` descriptor}. That
                              descriptor's retention is `preimage`, so its bytes are retained under
                              the finding-key2 digest and re-hashed at Run closure; this reads a
                              RETAINED record, never a caller assertion.
      payload_subjects        the admitted RuntimeSubject or HistorySubject rows of the import.

    GRANULARITY is preserved, not flattened. Runtime matches on logicalPath and, where the row
    carries `symbol`, on qualifiedName. History has NO symbol field, so a symbol-granularity target
    projects to its FILE and that widening is DISCLOSED per target rather than hidden.

    Ambiguity REFUSES: two matching rows for one target is not a deterministic projection and this
    function will not choose. An unmatched target is `matched: False` - unsupported, never satisfied
    and never read as evidence of non-use."""
    projection = {}
    for target in targets:
        if target not in findings:
            raise Refusal('CONFIG.INVALID', None,
                          'native.imported-projection-target-not-in-evidence-run: ' + str(target)
                          + ' is not a finding of the evidence Run named by evidenceRunId', target)
        descriptor = fingerprint_descriptors.get(target)
        if descriptor is None:
            raise Refusal('CONFIG.INVALID', None,
                          'native.imported-projection-fingerprint-preimage-missing: the retained '
                          'finding-fingerprint descriptor for ' + str(target) + ' is required to '
                          'project it to a payload subject', target)
        key = descriptor['subjectKey']
        symbol_granularity = bool(key.get('qualifiedName'))
        matches = []
        for row in payload_subjects:
            if row['path'] != key['logicalPath']:
                continue
            if kind == 'runtime' and 'symbol' in row and row['symbol'] != key['qualifiedName']:
                continue
            matches.append(row)
        if len(matches) > 1:
            raise Refusal('CONFIG.INVALID', None,
                          'native.imported-projection-ambiguous-target: ' + str(len(matches))
                          + ' payload subjects match ' + str(target) + '; the projection is not '
                          'deterministic and is not resolved by choosing one', target)
        row = matches[0] if matches else None
        projection[target] = {
            'matched': row is not None,
            'logicalPath': key['logicalPath'],
            'symbolGranularity': symbol_granularity,
            # HistorySubject carries no symbol, so a symbol target is answered at file granularity.
            'granularityWidenedToFile': bool(symbol_granularity and kind == 'history'),
            'observability': row.get('observability') if row and kind == 'runtime' else None,
        }
    return projection


def imported_requirement_outcome(req, projection, evidence, required):
    """The IMPORTED plane's per-requirement reference projection, implementing the published
    per-kind applicability and precedence of the imported-requirement law.

    PRECONDITIONS - a PURE projection over already-admitted inputs. It does not validate an opaque
    Run, re-derive source correspondence, or admit payload, observation scope or polarity: an
    authenticated importer and the retained Run closure own those.

    INPUT BINDING, each named by the field that owns it:
      req         a repair EvidenceRequirement. Its `completeness` decides ALL versus ANY over the
                  plan's targets. That reading of the existing enum is a SELECTED CLARIFICATION
                  chosen here for imported requirements, not a meaning the enum already published.
      projection  the output of project_targets_to_imported_subjects - the deterministic
                  fingerprint -> subject join, keyed by TARGET FINGERPRINT. Targets are never read
                  as paths.
      evidence    the admitted import context for this relation's evidenceKind:
                    available/consumable, and for runtime windowSatisfiesRequirement plus the
                    observationWindow/observedPopulation bounds; for history
                    rangeSatisfiesRequirement plus revisionRange, and `covered` keyed by target
                    fingerprint from collectionScope. The window/range DEMAND is owned by the
                    admitted recipe CLOSURE named by recipe.closureId - not a RecipeRef wire field,
                    which does not exist - and is projected here as a typed input.
      required    the owning evidenceUse declaration, as a TYPED BOOLEAN. A non-boolean REFUSES:
                  there is no `unknown` state at this boundary and no default is applied to one.

    SUPPORT depends on completeness; BOUNDS do not. A target that is unobservable or outside the
    history collection scope only names the cause more precisely WHEN the support test fails, so a
    lawful partial-acceptable requirement with one supported target is satisfied even though another
    target is unobservable. An earlier revision vetoed on any such target before the ANY test.

    Satisfied does NOT mean positive: `observed-hit` is positive execution evidence and
    `observable-unhit` is BOUNDED NEGATIVE evidence, and the disclosure says which. Nothing here
    establishes a universal negative, and no result changes `deadCodeRepairEligible`."""
    plane = requirement_plane(req['relation'])
    if plane != 'imported':
        raise Refusal('CONFIG.INVALID', None,
                      'native.imported-outcome-for-native-relation: ' + str(req['relation'])
                      + ' is a native fact relation; its producer is native section 4.6 '
                      'sufficiency_v2', req['relation'])
    if not isinstance(required, bool):
        raise Refusal('CONFIG.INVALID', None,
                      'native.imported-required-declaration-not-boolean: the evidenceUse '
                      'declaration must reach this boundary as a typed boolean; '
                      + repr(required) + ' is not, and a falsy value is not `optional`',
                      req['relation'])
    kind = EVIDENCE_RELATIONS[req['relation']]['evidenceKind']
    applicable = IMPORTED_REQUIREMENT_LAW['perKindApplicability'][req['relation']]
    targets = list(projection)
    if not targets:
        raise Refusal('CONFIG.INVALID', None,
                      'native.imported-outcome-without-targets: the projection is per target and '
                      'the plan supplied none', req['relation'])
    causes, disclosures = [], []

    def note(cause):
        if cause not in applicable:
            raise Refusal('CONFIG.INVALID', None,
                          'native.imported-outcome-not-applicable-to-kind: ' + cause + ' is not an '
                          'outcome of the ' + kind + ' projection', req['relation'])
        causes.append(cause)

    if not evidence.get('available'):
        if not required:
            # The OWNING evidenceUse route, related to that declaration and not equated with the
            # policy evaluator's own optional-absence handling: satisfied BY ABSENCE.
            return {'satisfied': True, 'satisfiedBy': 'declared-optional-absence',
                    'disclosures': [{'kind': 'import-absent', 'code': 'IMPORT.ABSENT_FOR_PREDICATE',
                                     'evidenceKind': kind}]}
        note('evidence-kind-unavailable')
    elif not evidence.get('consumable'):
        note('import-unmapped-only')
    else:
        covered = evidence.get('covered') or {}
        supported, unobservable, uncovered = set(), set(), set()
        for target, row in projection.items():
            if kind == 'runtime':
                if row['observability'] in ('observed-hit', 'observable-unhit'):
                    supported.add(target)
                elif row['observability'] in ('unobservable', 'unmapped'):
                    unobservable.add(target)
            else:
                if not covered.get(target):
                    uncovered.add(target)
                elif row['matched']:
                    supported.add(target)
        every = req['completeness'] == 'complete'
        satisfied_support = supported >= set(targets) if every else bool(supported)
        # BOUNDS are a property of the observation, not of the target count, so they apply to both
        # completeness values.
        if not evidence.get('rangeSatisfiesRequirement' if kind == 'history'
                            else 'windowSatisfiesRequirement', False):
            note('history-range-insufficient' if kind == 'history'
                 else 'observation-window-insufficient')
        if not satisfied_support:
            # Name the most actionable reason among the targets that are NOT supported.
            if kind == 'runtime' and unobservable:
                note('subject-not-observable')
            elif kind == 'history' and uncovered:
                note('history-outside-collection-scope')
            else:
                note('import-absent-for-requirement')
        if satisfied_support and not causes:
            bounds = {'kind': 'observation-bounds' if kind == 'runtime' else 'history-bounds',
                      'evidenceKind': kind, 'supportedTargets': sorted(supported)}
            if kind == 'runtime':
                bounds.update(observationWindow=evidence.get('observationWindow'),
                              observedPopulation=evidence.get('observedPopulation'),
                              polarity=sorted({projection[t]['observability'] for t in supported}))
            else:
                bounds.update(revisionRange=evidence.get('revisionRange'))
            disclosures.append(bounds)
            widened = sorted(t for t in supported if projection[t]['granularityWidenedToFile'])
            if widened:
                # A symbol target answered by file-level history is coarser than the recipe named.
                disclosures.append({'kind': 'granularity-widened-to-file',
                                    'evidenceKind': kind, 'targets': widened})
    if not causes:
        return {'satisfied': True, 'satisfiedBy': 'bounded-observation',
                'disclosures': disclosures}
    order = IMPORTED_REQUIREMENT_LAW['precedence']
    return {'satisfied': False, 'deficiency': min(causes, key=order.index),
            'disclosures': disclosures}


'''
P.write_text(s[:start] + NEW2 + s[end:], encoding='utf-8')
print('ok')
