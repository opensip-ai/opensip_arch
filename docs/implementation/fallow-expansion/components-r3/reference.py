"""Pure reference for extraction intermediates, never authoritative admission.

Inputs are explicit already-admitted snapshot/closure descriptors and retained
byte blobs. Fixtures provide synthetic inputs and grant no product authority.
"""
import hashlib
import json
from pathlib import Path


class ModelError(ValueError):
    pass


def require(condition, code):
    if not condition:
        raise ModelError(code)


def exact_json(value, depth=0):
    if type(value) in (dict, list):
        require(depth < 32, 'depth-bound')
    if value is None or type(value) in (bool, str):
        if type(value) is str:
            try:
                value.encode('utf-8', 'strict')
            except UnicodeError:
                raise ModelError('unicode-scalar') from None
        return
    if type(value) is int:
        require(-(2**63) <= value <= 2**64 - 1, 'integer-range')
        return
    require(type(value) in (dict, list), 'exact-json-type')
    if type(value) is dict:
        for key, child in value.items():
            require(type(key) is str, 'object-key')
            exact_json(key, depth + 1)
            exact_json(child, depth + 1)
    else:
        for child in value:
            exact_json(child, depth + 1)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def boundary(raw, offset):
    return (0 <= offset <= len(raw) and
            (offset == len(raw) or raw[offset] & 0xC0 != 0x80))


def text_valid(raw):
    try:
        raw.decode('utf-8', 'strict')
        return True
    except UnicodeError:
        return False


def partition(rows, length, start_key, end_key):
    position = 0
    for row in rows:
        require(row[start_key] == position and position < row[end_key] <= length, 'partition')
        position = row[end_key]
    require(position == length and (bool(rows) == bool(length)), 'partition')


def validate(record, admitted_snapshot, admitted_closures, retained_blobs):
    from jsonschema import Draft202012Validator
    exact_json(record)
    encoded = json.dumps(record, ensure_ascii=False, sort_keys=True,
                         separators=(',', ':'), allow_nan=False).encode()
    require(len(encoded) <= 4 * 1024 * 1024, 'record-byte-bound')
    schema = json.loads(Path(__file__).with_name('component-source-model.schema.json').read_bytes())
    require(Draft202012Validator(schema).is_valid(record), 'schema')
    require(record['snapshotId'] == admitted_snapshot['snapshotId'], 'snapshot-join')
    source = record['source']
    require(source['path'] in admitted_snapshot['files'], 'source-membership')
    original = admitted_snapshot['files'][source['path']]
    require(type(original) is bytes and source['contentSha256'] == digest(original) and
            source['byteLength'] == len(original), 'source-content')
    require(record['producerClosureId'] in admitted_closures, 'producer-closure')
    rows = record['regions']
    partition(rows, len(original), 'startByte', 'endByte')
    valid_original = text_valid(original)
    if not valid_original:
        require(len(rows) == 1 and rows[0]['kind'] == 'unmapped' and
                rows[0]['language'] == 'unknown' and rows[0]['state'] == 'malformed' and
                'malformed-source' in rows[0]['blockers'] and rows[0]['derived'] is None,
                'malformed-source-account')
    component = record['format'] in ('vue', 'svelte', 'astro')
    complete = True
    for ordinal, region in enumerate(rows):
        require(region['regionId'] == ordinal, 'region-ordinal')
        if valid_original:
            require(boundary(original, region['startByte']) and boundary(original, region['endByte']), 'utf8-boundary')
        require((region['state'] == 'complete') == (not region['blockers']), 'state-blockers')
        complete = complete and region['state'] == 'complete'
        if region['kind'] == 'unmapped':
            require(region['language'] == 'unknown' and region['state'] in ('unsupported', 'malformed') and
                    (('unmapped-region' in region['blockers']) if valid_original else True), 'unmapped-state')
        elif component:
            permitted = {'container': ['component-markup'], 'script': ['typescript', 'javascript'],
                         'template': [record['format'] + '-template'], 'style': ['css']}
            require(region['kind'] in permitted and region['language'] in permitted[region['kind']], 'region-language')
        else:
            require(region['kind'] == 'whole' and region['language'] == record['format'] and len(rows) == 1, 'whole-language')
        derived = region['derived']
        if derived is None:
            continue
        require(derived['sha256'] in retained_blobs, 'derived-retention')
        generated = retained_blobs[derived['sha256']]
        require(type(generated) is bytes and derived['sha256'] == digest(generated) and
                derived['byteLength'] == len(generated), 'derived-content')
        require(text_valid(generated) and valid_original, 'derived-utf8')
        partition(derived['segments'], len(generated), 'derivedStart', 'derivedEnd')
        for segment in derived['segments']:
            a, b = segment['derivedStart'], segment['derivedEnd']
            require(boundary(generated, a) and boundary(generated, b), 'utf8-boundary')
            c, d = segment['sourceStart'], segment['sourceEnd']
            if segment['kind'] == 'generated':
                require(c is None and d is None, 'generated-source')
            else:
                require(type(c) is int and type(d) is int and
                        region['startByte'] <= c <= d <= region['endByte'], 'source-range')
                require(boundary(original, c) and boundary(original, d), 'utf8-boundary')
                if segment['kind'] == 'exact':
                    require(b - a == d - c and generated[a:b] == original[c:d], 'exact-bytes')
    require(record['state'] == ('complete' if complete else 'partial'), 'model-state')
    return {'extractionComplete': complete, 'semanticCompleteness': 'not-established', 'repairAuthority': False}


def exact_original_span(validated_region, start, end, original, retained_blobs):
    """Call only after validate. None means no exact original citation or edit span."""
    require(text_valid(original), 'span-source-utf8')
    require(type(start) is int and type(end) is int and 0 <= start < end, 'span-shape')
    derived = validated_region['derived']
    if derived is None:
        require(end <= validated_region['endByte'] - validated_region['startByte'], 'span-range')
        result = (validated_region['startByte'] + start, validated_region['startByte'] + end)
        require(boundary(original, result[0]) and boundary(original, result[1]), 'utf8-boundary')
        return result
    require(end <= derived['byteLength'], 'span-range')
    generated = retained_blobs[derived['sha256']]
    require(boundary(generated, start) and boundary(generated, end), 'utf8-boundary')
    source_start = source_end = None
    for segment in derived['segments']:
        a, b = max(start, segment['derivedStart']), min(end, segment['derivedEnd'])
        if a >= b:
            continue
        if segment['kind'] != 'exact':
            return None
        c = segment['sourceStart'] + a - segment['derivedStart']
        d = segment['sourceStart'] + b - segment['derivedStart']
        if source_end is not None and c != source_end:
            return None
        if source_start is None:
            source_start = c
        source_end = d
    return None if source_start is None else (source_start, source_end)
