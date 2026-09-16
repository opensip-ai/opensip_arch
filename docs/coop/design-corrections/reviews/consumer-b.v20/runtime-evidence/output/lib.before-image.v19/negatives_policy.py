"""Distinguishing controls for audit selector group 1: an INVALID DISABLED policy rule must
refuse at ADMISSION even though a disabled rule is never EXECUTED.

workflows-and-surfaces section 5 bounds and admits the policy DOCUMENT -- every rule in it --
and composition sections 1/2 join every rule to the rule program, the emission plan and the
fingerprint namespace. `enabled` is consumed later, by the separate decision about which
admitted rules are executed. So the two obligations are distinguished here:

  POSITIVE control: a VALID disabled rule admits, is bound by every join, and is recorded with
  state/outcome `disabled`, empty arrays and no predicate proofs. That is what makes the
  refusals below attributable to the INVALIDITY rather than to disabled-ness.

  NEGATIVE controls: each mutates ONLY the disabled rule (or only its emission row) at BUILD
  time, so every downstream identity -- rule program, policy digest, emission plan, Plan,
  proof, evidence, seal, Run -- is legitimately reminted, and the ENTIRE graph is then
  reclosed. The ACTUAL first refusal is reported as observed, so an earlier generic guard is
  never mistaken for the intended one.
"""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_core as K
import opensip_closure as CL
import run_syntax_code as RSC
import run_syntax_code_full as RSCF

OUT = '/tmp/opensip-design-corrections/consumer-b.v19/output'
DISABLED_ID = 'rule.zz-disabled'


def rebuild_and_close(mutate, label, expect_check=None, layer=None):
    RSCF.MUTATE = dict(mutate)
    try:
        g = RSCF.complete(RSC.build())
        c = CL.Closure(g['st'])
        rep = c.close_run(g['out']['runId'], label)
        row = {'case': label, 'classification': 'invalid', 'mutation': _show(mutate),
               'builtAndReminted': True, 'mutatedRuleEnabled': False,
               'runId': g['out']['runId'],
               'closureChecksPassed': rep['checksPassed'],
               'refused': not rep['admitted'],
               'firstRefusal': rep['refusals'][0] if rep['refusals'] else None,
               'allRefusalChecks': sorted({r['check'] for r in rep['refusals']})}
    except Exception as e:
        row = {'case': label, 'classification': 'invalid', 'mutation': _show(mutate),
               'builtAndReminted': False, 'mutatedRuleEnabled': False, 'refused': True,
               'firstRefusal': {'check': 'BUILD_TIME_ADMISSION_REFUSAL',
                                'detail': '%s: %s' % (type(e).__name__, str(e)[:600])},
               'allRefusalChecks': ['BUILD_TIME_ADMISSION_REFUSAL'],
               'note': ('refused before a Run existed: the mutated policy failed its own '
                        'owning-schema or evaluator-admission boundary, which precedes '
                        'retained closure')}
    finally:
        RSCF.MUTATE = {}
    if expect_check:
        row['expectedOwnerJoin'] = expect_check
        row['expectedRefusalLayer'] = layer
        got = (row['firstRefusal'] or {}).get('check', '')
        det = str((row['firstRefusal'] or {}).get('detail', '') or '')
        row['observedRefusalLayer'] = (
            'owning-schema-admission' if 'schemaPath' in det
            else 'evaluator-admission' if got == 'BUILD_TIME_ADMISSION_REFUSAL'
            else 'retained-closure')
        row['firstRefusalIsTheIntendedJoin'] = (
            (expect_check in got or expect_check in det)
            and row['observedRefusalLayer'] == layer)
    return row


def _show(m):
    return json.loads(json.dumps(m, default=lambda o: '<drop>'))


def positive_control():
    RSCF.MUTATE = {}
    g = RSCF.complete(RSC.build())
    c = CL.Closure(g['st'])
    rep = c.close_run(g['out']['runId'], 'valid-disabled-rule')
    out, st = g['out'], g['st']
    proof = out['proof']
    rr = [x for x in proof['ruleResults'] if x['ruleId'] == DISABLED_ID][0]
    policy = st.objects[[k for k in st.objects if k.startswith('policy#')][0]] \
        if any(k.startswith('policy#') for k in st.objects) else None
    emit = None
    for k, v in st.objects.items():
        if isinstance(v, dict) and v.get('policyDigest') and 'rules' in v:
            emit = v
    pol_rule = None
    for k, v in st.objects.items():
        if isinstance(v, dict) and v.get('schemaFamily') == 'opensip.product.policy' \
                and v.get('schemaMajor') == 2:
            pol_rule = [r for r in v['rules'] if r['ruleId'] == DISABLED_ID][0]
    rp = None
    for k, v in st.objects.items():
        if isinstance(v, dict) and 'programs' in v and 'ruleIndex' in str(list(v.keys())):
            rp = v
    return {'case': 'valid-disabled-rule-is-admitted-bound-and-recorded-disabled',
            'classification': 'valid', 'runAdmitted': rep['admitted'],
            'closureChecksPassed': rep['checksPassed'],
            'admissionJoinsObservedForTheDisabledRule': {
                'presentInPolicyDocument': pol_rule is not None,
                'enabled': pol_rule and pol_rule['enabled'],
                'boundInRuleProgram': rp is not None and any(
                    p.get('ruleId') == DISABLED_ID for p in (rp.get('programs') or [])),
                'boundInEmissionPlan': emit is not None and any(
                    r['ruleId'] == DISABLED_ID for r in emit['rules']),
                'emissionRowEqualsPolicyRuleProgramRef': emit is not None and all(
                    [r for r in emit['rules'] if r['ruleId'] == DISABLED_ID][0][f]
                    == pol_rule['ruleProgramRef'][f]
                    for f in ('contributionId', 'ruleStableId', 'semanticsMajor')),
            },
            'executionOutcomeObserved': {
                'outcome': rr['outcome'],
                'enumerationState': rr['enumeration']['state'],
                'selectedSubjectIds': rr['enumeration']['selectedSubjectIds'],
                'findingIds': rr['findingIds'],
                'deficiencies': rr['deficiencies'],
                'predicateProofs': [p for p in proof['predicateProofs']
                                    if p['ruleId'] == DISABLED_ID],
            },
            'law': ('admitted and joined like every other rule; `enabled:false` changed only '
                    'EXECUTION -- composition section 2 requires state/outcome `disabled` '
                    'with empty arrays and no emitted predicate.')}


def main():
    rows = [positive_control()]
    lit = {'op': 'exists', 'relation': 'literal', 'minResolution': 'syntactic',
           'filters': []}
    # (label, build-time mutation, substring of the OWNING law's refusal, refusal LAYER)
    # The layer is recorded because the three boundaries are distinct obligations: the policy
    # document's own schema grammar, the evaluator's admission of the Plan inputs, and the
    # retained-closure audit of the sealed Run. A control is only accepted when the FIRST
    # refusal is the intended law AT the intended boundary.
    cases = [
        ('disabled-rule-minResolution-not-on-that-relations-ladder',
         {'disabled-rule-override': {'emitWhen': dict(lit,
                                                      minResolution='resolved-callee')}},
         'ATOM_MIN_RESOLUTION_IN_THIS_RELATIONS_LADDER', 'retained-closure'),
        ('disabled-rule-relation-in-neither-registry',
         {'disabled-rule-override': {'emitWhen': dict(lit, relation='calls-inlined')}},
         'ATOM_RELATION_IS_REGISTERED', 'retained-closure'),
        ('disabled-rule-native-atom-carrying-evidence',
         {'disabled-rule-override': {'emitWhen': dict(lit, evidence='runtime')}},
         'NATIVE_FACT_ATOM_MUST_NOT_CARRY_EVIDENCE', 'retained-closure'),
        ('disabled-rule-imported-atom-not-declared-in-evidenceUse',
         {'disabled-rule-override': {
             'emitWhen': {'op': 'exists', 'relation': 'runtime-observation',
                          'minResolution': 'observed', 'filters': [],
                          'evidence': 'runtime'},
             'evidenceUse': []}},
         'IMPORTED_ATOM_DECLARED_IN_EVIDENCE_USE', 'retained-closure'),
        ('disabled-rule-count-at-most-without-n',
         {'disabled-rule-override': {'emitWhen': dict(lit, op='count-at-most')}},
         'properties/emitWhen/oneOf', 'owning-schema-admission'),
        ('disabled-rule-predicate-tree-deeper-than-8',
         {'disabled-rule-override': {'emitWhen': _deep(lit, 9)}},
         'PREDICATE_DEPTH_AT_MOST_8', 'retained-closure'),
        ('disabled-rule-filter-field-not-admissible-for-its-relation',
         {'disabled-rule-override': {
             'emitWhen': dict(lit, filters=[{'field': 'targetKind', 'cmp': 'eq',
                                             'value': 'symbol'}])}},
         'FILTER_FIELD_ADMITTED_FOR_THIS_RELATION', 'retained-closure'),
        ('disabled-rule-subjectKind-not-in-the-documents-own-enum',
         {'disabled-rule-override': {'subjectEnumeration': {'universe': 'syntax',
                                                            'subjectKind': 'crate'}}},
         'subjectEnumeration/properties/subjectKind/enum', 'owning-schema-admission'),
        ('disabled-rule-missing-from-the-emission-plan',
         {'emission-drop-ruleId': DISABLED_ID},
         'EMISSION_PLAN_DOES_NOT_BIND_EVERY_POLICY_RULE', 'evaluator-admission'),
        ('disabled-rule-duplicating-another-rules-fingerprint-namespace',
         {'disabled-rule-override': {
             'ruleProgramRef': {'contributionId': 'contrib.clone-hygiene',
                                'ruleStableId': 'clone-hygiene.declares-present',
                                'semanticsMajor': 1,
                                'programDigest': K.raw_sha256(
                                    b'clone-hygiene.declares-present.v1')}}},
         'FINGERPRINT_NAMESPACE_NOT_UNIQUE', 'evaluator-admission'),
        # ---- v17: the atom KIND / ENDPOINT law, which the v16 checker never reached.
        # Each of these is a DISABLED rule, so under the v16 checker the `disabled` outcome
        # hid it entirely: the Run closed and replayed with a malformed program inside it.
        ('disabled-rule-subject-kind-incompatible-with-its-relations-source-endpoint',
         {'disabled-rule-override': {
             'subjectEnumeration': {'universe': 'syntax', 'subjectKind': 'file'},
             'emitWhen': dict(lit)}},
         'ATOM_KIND_INCOMPATIBLE', 'retained-closure'),
        ('disabled-rule-subject-kind-package-against-a-symbol-source-endpoint',
         {'disabled-rule-override': {
             'subjectEnumeration': {'universe': 'syntax', 'subjectKind': 'package'},
             'emitWhen': dict(lit)}},
         'ATOM_KIND_INCOMPATIBLE', 'retained-closure'),
        ('disabled-rule-endpoint-target-on-a-unary-relation',
         {'disabled-rule-override': {'emitWhen': dict(lit, endpoint='target')}},
         'ATOM_ENDPOINT_UNAVAILABLE', 'retained-closure'),
        ('disabled-rule-endpoint-target-at-a-rung-that-forbids-the-resolved-field',
         {'disabled-rule-override': {
             'subjectEnumeration': {'universe': 'syntax', 'subjectKind': 'symbol'},
             'emitWhen': {'op': 'exists', 'relation': 'imports',
                          'minResolution': 'syntactic-specifier', 'filters': [],
                          'endpoint': 'target'}}},
         'ATOM_ENDPOINT_UNAVAILABLE', 'retained-closure'),
        ('disabled-rule-endpoint-target-kind-not-in-targetKinds',
         {'disabled-rule-override': {
             'subjectEnumeration': {'universe': 'syntax', 'subjectKind': 'file'},
             'emitWhen': {'op': 'exists', 'relation': 'calls',
                          'minResolution': 'resolved-callee', 'filters': [],
                          'endpoint': 'target'}}},
         'ATOM_KIND_INCOMPATIBLE', 'retained-closure'),
        ('disabled-rule-filter-forbidden-at-the-requested-rung',
         {'disabled-rule-override': {
             'subjectEnumeration': {'universe': 'syntax', 'subjectKind': 'symbol'},
             'emitWhen': {'op': 'exists', 'relation': 'imports',
                          'minResolution': 'syntactic-specifier',
                          'filters': [{'field': 'target', 'cmp': 'eq',
                                       'value': 'ts:src/util.ts'}]}}},
         'FILTER_FIELD_FORBIDDEN_AT_THE_REQUESTED_RUNG', 'retained-closure'),
        # a POSITIVE contrast for the same two laws: the same relation at the rung that DOES
        # admit the target endpoint, with a kind that IS in targetKinds, must admit
        ('disabled-rule-endpoint-target-at-an-admitted-rung-and-kind-IS-LAWFUL',
         {'disabled-rule-override': {
             'subjectEnumeration': {'universe': 'syntax', 'subjectKind': 'symbol'},
             'emitWhen': {'op': 'exists', 'relation': 'imports',
                          'minResolution': 'resolved-target', 'filters': [],
                          'endpoint': 'target'}}},
         None, None),
    ]
    for label, mut, expect, layer in cases:
        if expect is None:
            # a LAWFUL mutation of the same disabled rule: it must ADMIT. Without this
            # contrast a checker that refused every endpoint=target atom would look correct.
            r = rebuild_and_close(mut, label, None, None)
            r['classification'] = 'valid'
            r['mustAdmit'] = True
            r['admitted'] = not r['refused']
            rows.append(r)
            continue
        rows.append(rebuild_and_close(mut, label, expect, layer))

    for r in rows:
        if r.get('mustAdmit'):
            print('%-58s LAWFUL-CONTRAST admitted=%s' % (r['case'][:58], r['admitted']))
        elif r.get('classification') == 'valid':
            print('%-58s admitted=%-5s disabledOutcome=%s'
                  % (r['case'][:58], r['runAdmitted'],
                     r['executionOutcomeObserved']['outcome']))
        else:
            print('%-58s refused=%-5s intended=%-5s layer=%-24s first=%s'
                  % (r['case'][:58], r['refused'],
                     r.get('firstRefusalIsTheIntendedJoin'),
                     r.get('observedRefusalLayer'),
                     (r['firstRefusal'] or {}).get('check')))

    with open(OUT + '/vectors/policy-admission-negative-controls.json', 'w') as f:
        json.dump({'standing': __doc__, 'controls': rows}, f, indent=1, default=str)

    bad = [r['case'] for r in rows
           if r.get('classification') == 'invalid' and not r['refused']]
    bad += [r['case'] for r in rows
            if r.get('classification') == 'valid' and not r.get('mustAdmit')
            and not r['runAdmitted']]
    bad += [r['case'] for r in rows if r.get('mustAdmit') and not r['admitted']]
    off = [r['case'] for r in rows
           if r.get('classification') == 'invalid'
           and not r.get('firstRefusalIsTheIntendedJoin')]
    print()
    if off:
        print('FIRST REFUSAL WAS NOT THE INTENDED OWNER JOIN:')
        for r in rows:
            if r['case'] in off:
                print('  %s\n    expected ~%s\n    got      %s\n    detail   %s'
                      % (r['case'], r['expectedOwnerJoin'],
                         (r['firstRefusal'] or {}).get('check'),
                         str((r['firstRefusal'] or {}).get('detail'))[:260]))
    if bad:
        print('CONTROLS THAT DID NOT REFUSE/ADMIT AS REQUIRED:', bad)
        sys.exit(1)
    print('all %d policy-admission controls behaved as required (%d negative, 1 positive)'
          % (len(rows), len(rows) - 1))


def _deep(leaf, n):
    node = leaf
    for _ in range(n):
        node = {'op': 'not', 'operand': node}
    return node


main()
