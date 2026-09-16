"""Read-only redaction of the selected Plan's admitted semantic configuration.

No raw file/layer text, environment, native provider configuration or current
project settings are accepted here. The host supplies the exact retained Plan.
"""
import copy
import hashlib


class DisclosureRefusal(ValueError):
    pass


def project(plan_id, admitted_plan, configuration, policy, reference, identity_schema,
            disclosure_schema):
    # Full Plan/Run association and custody precede this function. Re-check the
    # precise configuration schema and its already-owned digest before reading
    # fields; never pass unknown future fields into a generic renderer.
    plan_schema = copy.deepcopy(identity_schema)
    plan_schema['$ref'] = '#/$defs/plan'
    reference.validate(plan_schema, admitted_plan)
    if type(plan_id) is not str or plan_id != 'plan2:' + reference.identity('plan', admitted_plan):
        raise DisclosureRefusal('CONFIG-DISCLOSURE.PLAN-ID')
    selected = copy.deepcopy(identity_schema)
    selected['$ref'] = '#/$defs/semantic-configuration'
    reference.validate(selected, configuration)
    digest = hashlib.sha256(reference.canonical(configuration)).hexdigest()
    if digest != admitted_plan['resolvedConfigDigest']:
        raise DisclosureRefusal('CONFIG-DISCLOSURE.SOURCE-DIGEST')
    if not reference.equal_typed(admitted_plan['budget'], configuration['analysis']['budget']):
        raise DisclosureRefusal('CONFIG-DISCLOSURE.BUDGET-JOIN')
    output = {'schemaFamily': 'opensip.report.configuration-disclosure', 'schemaMajor': 1,
              'policy': 'semantic-configuration-public-fields-v1',
              'source': {'kind': 'retained-plan-resolved-configuration', 'planId': plan_id,
                         'resolvedConfigDigest': digest},
              'fields': {}, 'provenance': copy.deepcopy(disclosure_schema['properties']['provenance']['const']), 'limitations': list(disclosure_schema['properties']['limitations']['const'])}
    owner_fields = {group+'.'+field for group, spec in identity_schema['$defs']['semantic-configuration']['properties'].items()
                    for field in spec['properties']}
    if {r['field'] for r in policy['fields']} != owner_fields or len(policy['fields']) != len(owner_fields):
        raise DisclosureRefusal('CONFIG-DISCLOSURE.POLICY-COVERAGE')
    for rule in policy['fields']:
        key = rule['field']; group, field = key.split('.')
        if field not in configuration[group]:
            row = {'field': key, 'state': 'not-present'}
        elif rule['policy'] == 'public-closed-value':
            row = {'field': key, 'state': 'disclosed', 'value': copy.deepcopy(configuration[group][field])}
        else:
            row = {'field': key, 'state': 'redacted', 'reason': 'configuration-value-not-public'}
            if rule['policy'] == 'redact-with-count':
                row['itemCount'] = len(configuration[group][field])
            elif rule['policy'] != 'redact-value':
                raise DisclosureRefusal('CONFIG-DISCLOSURE.POLICY-KIND')
        output['fields'][key] = row
    # The closed output schema also owns the allowlist; changing the supplied
    # private policy to expose a string does not make the resulting row lawful.
    reference.validate(disclosure_schema, output)
    reference.canonical(output)
    return output


SOURCE_FAILURES = {
    'missing': {'state': 'unavailable', 'reason': 'evidence-missing'},
    'purged': {'state': 'unavailable', 'reason': 'evidence-purged'},
    'expired': {'state': 'unavailable', 'reason': 'evidence-expired'},
    'corrupt': {'state': 'corrupt', 'reason': 'retained-bytes-corrupt'},
    'digest-mismatch': {'state': 'corrupt', 'reason': 'retained-bytes-corrupt'},
    'plan-id-mismatch': {'state': 'corrupt', 'reason': 'retained-bytes-corrupt'},
    'budget-join-mismatch': {'state': 'corrupt', 'reason': 'retained-bytes-corrupt'},
    'invalid-retained-shape': {'state': 'corrupt', 'reason': 'retained-bytes-corrupt'},
    'unsupported-schema': {'state': 'incompatible', 'reason': 'retained-schema-major-unsupported'},
}


def unavailable_source(reason):
    """Host classifies retained-source failures before calling the projection.

    No arbitrary exception messages or current settings enter the report.
    Invalid compiled policy and programmer faults are not retained-source loss.
    """
    if type(reason) is not str or reason not in SOURCE_FAILURES:
        raise DisclosureRefusal('CONFIG-DISCLOSURE.UNKNOWN-SOURCE-FAILURE')
    return dict(SOURCE_FAILURES[reason])
