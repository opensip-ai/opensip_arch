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
    selected = copy.deepcopy(identity_schema)
    selected['$ref'] = '#/$defs/semantic-configuration'
    reference.validate(selected, configuration)
    digest = hashlib.sha256(reference.canonical(configuration)).hexdigest()
    if digest != admitted_plan['resolvedConfigDigest']:
        raise DisclosureRefusal('CONFIG-DISCLOSURE.SOURCE-DIGEST')
    output = {'schemaFamily': 'opensip.report.configuration-disclosure', 'schemaMajor': 1,
              'policy': 'semantic-configuration-public-fields-v1',
              'source': {'kind': 'retained-plan-resolved-configuration', 'planId': plan_id,
                         'resolvedConfigDigest': digest},
              'fields': {}, 'limitations': list(disclosure_schema['properties']['limitations']['const'])}
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
