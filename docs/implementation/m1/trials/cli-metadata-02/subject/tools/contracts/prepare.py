"""Prepare explicit schema entrypoints for the selected inert carrier generators."""
import json
from pathlib import Path

MAPS = ('properties', 'patternProperties', '$defs', 'definitions')
SINGLES = ('additionalProperties', 'propertyNames', 'items', 'not', 'contains', 'if', 'then', 'else')
ARRAYS = ('allOf', 'anyOf', 'oneOf')


def schema_map(value, leaf):
    if type(value) is bool:
        return leaf(value)
    if not isinstance(value, dict):
        raise ValueError('schema node is not an object or boolean')
    result = dict(value)
    for key in MAPS:
        if key in result:
            result[key] = {k: schema_map(v, leaf) for k, v in result[key].items()}
    for key in SINGLES:
        if key in result:
            result[key] = schema_map(result[key], leaf)
    for key in ARRAYS:
        if key in result:
            result[key] = [schema_map(v, leaf) for v in result[key]]
    return leaf(result)


def reference(value, owner):
    if not isinstance(value, str) or value.count('#') > 1 or '%' in value:
        raise ValueError('unsupported schema reference spelling')
    document, _, pointer = value.partition('#')
    document = document or owner
    if pointer and not pointer.startswith('/'):
        raise ValueError('named schema anchors are not selected')
    return document + '#' + pointer


def resolve(documents, ref):
    document, pointer = ref.split('#')
    if document not in documents:
        raise ValueError('unregistered schema reference: ' + ref)
    node = documents[document]
    for token in pointer.split('/')[1:]:
        for i, char in enumerate(token):
            if char == '~' and (i + 1 == len(token) or token[i + 1] not in '01'):
                raise ValueError('malformed reference pointer')
        key = token.replace('~1', '/').replace('~0', '~')
        if not isinstance(node, dict) or key not in node:
            raise ValueError('unresolved schema pointer: ' + ref)
        node = node[key]
    if type(node) is not bool and not isinstance(node, dict):
        raise ValueError('reference does not address a schema')
    return node


def flatten(documents, options):
    names = {row['ref']: row['typeName'] for row in options['entryPoints']}
    denied = set(options['deniedRefs'])
    if set(names) & denied:
        raise ValueError('selected entrypoint is superseded')
    references = set()

    def convert(value, owner):
        if type(value) is bool:
            return value
        if not isinstance(value, dict):
            raise ValueError('invalid schema node')
        # Declaration tables are addressed through exact refs, never discovered
        # as implicit extra outputs. References in annotation/instance data are
        # not schema references and are never dereferenced here.
        result = {k: v for k, v in value.items() if k not in ('$id', '$schema', '$defs', 'definitions')}
        if '$ref' in result:
            target = reference(result['$ref'], owner)
            if target in denied:
                raise ValueError('reference reaches superseded entrypoint: ' + target)
            if target not in names:
                raise ValueError('reference missing explicit type owner: ' + target)
            resolve(documents, target)
            references.add(target)
            result['$ref'] = '#/definitions/' + names[target]
        for key in ('properties', 'patternProperties'):
            if key in result:
                result[key] = {k: convert(v, owner) for k, v in result[key].items()}
        for key in SINGLES:
            if key in result:
                result[key] = convert(result[key], owner)
        for key in ARRAYS:
            if key in result:
                result[key] = [convert(v, owner) for v in result[key]]
        return result

    definitions = {name: convert(resolve(documents, ref), ref.split('#')[0]) for ref, name in names.items()}
    return {'$schema': 'http://json-schema.org/draft-07/schema#', 'definitions': dict(sorted(definitions.items()))}


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


def prepare(documents, options, destination: Path):
    flat = flatten(documents, options)
    for label, leaf in [('rust', rust), ('ts', typescript)]:
        (destination / (label + '-projection.json')).write_text(json.dumps(schema_map(flat, leaf), indent=2) + '\n')
    (destination / 'owners.json').write_text(json.dumps(options['owners'], indent=2) + '\n')
    (destination / 'targets.json').write_text(json.dumps({r['ref']: r['typeName'] for r in options['entryPoints']}, indent=2) + '\n')
