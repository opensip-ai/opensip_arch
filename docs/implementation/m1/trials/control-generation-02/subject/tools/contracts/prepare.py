"""Prepare explicit schema entrypoints for the selected inert carrier generators."""
import json
import re
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


def selected_keywords():
    runtime=(Path(__file__).parent/'runtime/schema.ts').read_text()
    result=set()
    for name in ('known','annotations'):
        match=re.search(r'const '+name+r' = new Set\((\[[^\n]*\])\);',runtime)
        if not match:
            raise ValueError('selected runtime keyword declaration changed')
        values=json.loads(match.group(1))
        if not all(type(value) is str for value in values):
            raise ValueError('invalid selected runtime keyword declaration')
        result.update(values)
    return result


def flatten(documents, options):
    keywords=selected_keywords()
    names = {row['ref']: row['typeName'] for row in options['entryPoints']}
    denied = set(options['deniedRefs'])
    if any(ref == base or ref.startswith(base + '/') for ref in names for base in denied):
        raise ValueError('selected entrypoint is superseded')
    references = set()

    def convert(value, owner):
        if type(value) is bool:
            return value
        if not isinstance(value, dict):
            raise ValueError('invalid schema node')
        if '$id' in value and value['$id'] != owner:
            raise ValueError('nested schema identity differs from owner')
        if '$schema' in value and value['$schema'] != 'https://json-schema.org/draft/2020-12/schema':
            raise ValueError('nested schema dialect differs from selection')
        unknown=set(value)-keywords
        if unknown:
            raise ValueError('unsupported schema keyword: '+', '.join(sorted(unknown)))
        # Declaration tables are addressed through exact refs, never discovered
        # as implicit extra outputs. References in annotation/instance data are
        # not schema references and are never dereferenced here.
        result = {k: v for k, v in value.items() if k not in ('$id', '$schema', '$defs', 'definitions')}
        if '$ref' in result:
            target = reference(result['$ref'], owner)
            if any(target == base or target.startswith(base + '/') for base in denied):
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
        if set(value['patternProperties']) != {'^.+$'} or value.get('properties') or value.get('additionalProperties') is not False:
            raise ValueError('unselected Rust pattern-map projection')
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
    elif 'enum' in value:
        value['tsType'] = ' | '.join(literal(x) for x in value['enum'])
    elif value.get('type') == 'integer':
        value['tsType'] = 'bigint'
    elif type(value.get('type')) is list and 'integer' in value['type']:
        mapping = {'integer': 'bigint', 'null': 'null', 'boolean': 'boolean', 'string': 'string',
                   'object': '{[key:string]:Json}', 'array': 'Json[]'}
        value['tsType'] = ' | '.join(mapping[x] for x in value['type'])
    return value


def name_variant_objects(schema):
    """Prevent Typify reusing one inline object name for different union bodies.

    These are private carrier names, not source schema IDs or wire fields.
    Only conflicting direct object properties in a named oneOf are affected.
    Stable variant/property positions keep names distinct even when field names
    would normalize to the same Rust identifier. Original schemas are unchanged.
    """
    reserved = set(schema['definitions'])
    def collect_titles(value):
        if isinstance(value, dict) and isinstance(value.get('title'), str):
            reserved.add(value['title'])
        return value
    schema_map(schema, collect_titles)
    for name, definition in schema['definitions'].items():
        if not isinstance(definition, dict):
            continue
        fields = {}
        for variant, branch in enumerate(definition.get('oneOf', [])):
            if not isinstance(branch, dict):
                continue
            for index, (key, child) in enumerate(sorted(branch.get('properties', {}).items())):
                if isinstance(child, dict) and child.get('type') == 'object':
                    fields.setdefault(key, []).append((variant, index, child))
        for entries in fields.values():
            if len({json.dumps(child, sort_keys=True) for _, _, child in entries}) > 1:
                for variant, index, child in entries:
                    title = f'{name}Variant{variant}Property{index}'
                    if title in reserved:
                        raise ValueError('private variant title collides with an existing type: ' + title)
                    reserved.add(title)
                    child['title'] = title
    refuse_ambiguous_union_properties(schema)
    return schema


def refuse_ambiguous_union_properties(schema):
    """Refuse the residual sibling-property alias class before calling Typify.

    The finite selected definitions have independent roundtrip evidence. This
    conservative guard is not a proof of arbitrary Typify name allocation.
    """
    def needs_name(child):
        return (isinstance(child, dict) and '$ref' not in child and (
            child.get('type') in ('object', 'array') or 'enum' in child or
            any(k in child for k in ('oneOf', 'anyOf', 'allOf')) or
            (child.get('type') == 'string' and
             any(k in child for k in ('minLength', 'maxLength', 'const')))))

    def inspect(value):
        if not isinstance(value, dict):
            return value
        for combiner in ('oneOf', 'anyOf'):
            fields = {}
            for branch in value.get(combiner, []):
                if isinstance(branch, dict):
                    for key, child in branch.get('properties', {}).items():
                        if needs_name(child):
                            fields.setdefault(key, []).append(child)
            for key, children in fields.items():
                shapes = {json.dumps(child, sort_keys=True) for child in children}
                if len(shapes) <= 1:
                    continue
                titles = {}
                for child in children:
                    title = child.get('title')
                    shape = json.dumps(child, sort_keys=True)
                    if not isinstance(title, str) or not title or (title in titles and titles[title] != shape):
                        raise ValueError('ambiguous inline union property type: ' + key)
                    titles[title] = shape
        return value

    schema_map(schema, inspect)


def prepare(documents, options, destination: Path):
    flat = flatten(documents, options)
    for label, leaf in [('rust', rust), ('ts', typescript)]:
        projection = schema_map(flat, leaf)
        if label == 'rust':
            projection = name_variant_objects(projection)
        (destination / (label + '-projection.json')).write_text(json.dumps(projection, indent=2) + '\n')
    (destination / 'owners.json').write_text(json.dumps(options['owners'], indent=2) + '\n')
    (destination / 'targets.json').write_text(json.dumps({r['ref']: r['typeName'] for r in options['entryPoints']}, indent=2) + '\n')
