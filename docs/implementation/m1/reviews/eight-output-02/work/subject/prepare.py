"""Stable names and inert carrier projection for the explicitly selected trial refs."""
from pathlib import Path
import json
import re

HERE = Path(__file__).parent
BASE = HERE.parent / 'm1-full-generator-trial-01'
source = json.loads((BASE / 'source-map.json').read_bytes())
original = json.loads((BASE / 'flattened-trial.json').read_bytes())
owners = {r['schemaId']: r for r in json.loads((HERE / 'owners.json').read_bytes())}

def name(ref):
    owner, fragment = ref.split('#')
    parts = fragment.split('/')[1:]
    if parts[:1] == ['$defs']:
        parts = parts[1:]
    suffix = ''.join(x[:1].upper() + x[1:] for x in re.findall('[A-Za-z0-9]+', '_'.join(parts))) or 'Root'
    return owners[owner]['namespace'] + suffix

names = {old: name(ref) for ref, old in source['selectedTargets'].items()}
assert len(set(names.values())) == len(names), 'identifier collision'
target_names = {ref: names[old] for ref, old in source['selectedTargets'].items()}
(HERE / 'targets.json').write_text(json.dumps(target_names, indent=2) + '\n')

def schema_map(value, leaf):
    if type(value) is bool:
        return leaf(value)
    result = dict(value)
    for key in ('properties', 'patternProperties', 'definitions', '$defs'):
        if key in result:
            result[key] = {k: schema_map(v, leaf) for k, v in result[key].items()}
    for key in ('additionalProperties', 'propertyNames', 'items', 'not', 'contains', 'if', 'then', 'else'):
        if key in result:
            result[key] = schema_map(result[key], leaf)
    for key in ('allOf', 'anyOf', 'oneOf'):
        if key in result:
            result[key] = [schema_map(v, leaf) for v in result[key]]
    return leaf(result)

def rename(value):
    if type(value) is bool:
        return value
    if '$ref' in value:
        ref = value['$ref']
        assert ref.startswith('#/definitions/')
        value['$ref'] = '#/definitions/' + names[ref[len('#/definitions/'):]]
    return value

flat = {'$schema': original['$schema'], 'definitions': {
    names[k]: schema_map(v, rename) for k, v in original['definitions'].items()}}
flat['definitions'] = dict(sorted(flat['definitions'].items()))
(HERE / 'named-schemas.json').write_text(json.dumps(flat, indent=2) + '\n')

def rust(value):
    if type(value) is bool:
        return value
    for key in [*('if', 'then', 'else', 'pattern', 'default', 'contains'), *(k for k in value if k.startswith('x-'))]:
        value.pop(key, None)
    if value.get('not') == {}:
        value.pop('not')
    if 'allOf' in value:
        value['allOf'] = [v for v in value['allOf'] if v != {}]
        if not value['allOf']:
            value.pop('allOf')
    if value.get('minLength') == 0:
        value.pop('minLength')
    enum = value.get('enum', [value['const']] if 'const' in value else [])
    if enum and all(type(v) is int for v in enum):
        value['type'] = 'integer'
    if value.get('type') == 'integer':
        low = value.get('minimum', -(2**63))
        high = value.get('maximum', 2**64 - 1)
        if low < 0 and high > 2**63 - 1:
            # Inert exact-domain carrier. Full range/enum/const constraints stay
            # in the original schema, not in the native storage type.
            return {'type': 'integer'}
    if 'patternProperties' in value:
        # Exactly the one selected SARIF message map; any other pattern-map
        # shape refuses instead of silently widening another carrier.
        assert set(value['patternProperties']) == {'^.+$'}
        assert not value.get('properties') and value['additionalProperties'] is False
        value['additionalProperties'] = value.pop('patternProperties')['^.+$']
    return value

def literal(value):
    if type(value) is int:
        return str(value) + 'n'
    if type(value) is dict:
        return '{' + ';'.join(json.dumps(k) + ':' + literal(v) for k, v in value.items()) + '}'
    if type(value) is list:
        return '[' + ','.join(literal(v) for v in value) + ']'
    return json.dumps(value, ensure_ascii=False)

def typescript(value):
    if value is True:
        return {'tsType': 'Json'}
    if value is False:
        return value
    for key in [*('if', 'then', 'else'), *(k for k in value if k.startswith('x-'))]:
        value.pop(key, None)
    if 'const' in value:
        value['tsType'] = literal(value['const'])
    elif 'enum' in value and any(type(x) is int for x in value['enum']):
        value['tsType'] = ' | '.join(literal(x) for x in value['enum'])
    elif value.get('type') == 'integer':
        value['tsType'] = 'bigint'
    elif type(value.get('type')) is list and 'integer' in value['type']:
        mapping = {'integer': 'bigint', 'null': 'null', 'boolean': 'boolean', 'string': 'string',
                   'object': '{[key:string]:Json}', 'array': 'Json[]'}
        value['tsType'] = ' | '.join(mapping[x] for x in value['type'])
    return value

for label, leaf in [('rust', rust), ('ts', typescript)]:
    (HERE / (label + '-projection.json')).write_text(json.dumps(schema_map(flat, leaf), indent=2) + '\n')
print(json.dumps(dict(targets=len(names), namespaces=len(owners), standing='partial corpus trial; protocol translation audit pending')))
