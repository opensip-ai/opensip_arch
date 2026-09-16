"""Offline reference-document custody check, not fragment/dynamic/schema admission."""
import json
import posixpath


def validate_schema_references(parsed):
    ids = {}
    refs = []

    def visit(value, path):
        if isinstance(value, dict):
            if '$id' in value:
                key = value['$id']
                canonical = json.dumps(value, sort_keys=True, separators=(',', ':'))
                if key in ids:
                    assert ids[key][1] == canonical, ('Ambiguous schema URI', key, ids[key][0], path)
                else:
                    ids[key] = (path, canonical)
            for key in ('$ref', '$dynamicRef'):
                if key in value:
                    refs.append((path, value[key]))
            for child in value.values():
                visit(child, path)
        elif isinstance(value, list):
            for child in value:
                visit(child, path)

    for path, document in parsed.items():
        visit(document, path)
    for path, ref in refs:
        base = ref.split('#')[0]
        if not base or base in ids:
            continue
        assert not base.startswith(('urn:', 'https:', 'http:')), ('Unretained absolute schema reference', path, ref)
        target = posixpath.normpath(posixpath.join(posixpath.dirname(path), base))
        assert target in parsed, ('Unretained relative schema reference', path, ref, target)
    return {'schemaIds': len(ids), 'references': len(refs), 'unresolvedAbsolute': 0, 'ambiguousSchemaIds': 0}
