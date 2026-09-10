"""Product envelope canonicalization reference; design evidence, not a host runtime."""
import hashlib
import json
from jsonschema import Draft202012Validator, ValidationError, validators

MIN_INT, MAX_INT = -(2**63), 2**64 - 1
MAX_BYTES, MAX_DEPTH = 4 * 1024 * 1024, 32

class AdmissionError(ValueError):
    pass

def typed(value, depth=0):
    if type(value) in (dict, list) and depth >= MAX_DEPTH:
        raise AdmissionError('DEPTH_LIMIT')
    if value is None or type(value) is bool:
        return
    if type(value) is int:
        if not MIN_INT <= value <= MAX_INT:
            raise AdmissionError('INTEGER_RANGE')
        return
    if type(value) is str:
        try:
            value.encode('utf-8', 'strict')
        except UnicodeError as exc:
            raise AdmissionError('UNICODE_SCALAR_REQUIRED') from exc
        return
    if type(value) is list:
        for child in value:
            typed(child, depth + 1)
        return
    if type(value) is dict:
        for key, child in value.items():
            if type(key) is not str:
                raise AdmissionError('STRING_KEY_REQUIRED')
            typed(key, depth + 1)
            typed(child, depth + 1)
        return
    raise AdmissionError('EXACT_JSON_TYPE_REQUIRED')

def parse(raw):
    if type(raw) is not bytes or len(raw) > MAX_BYTES:
        raise AdmissionError('BYTE_LIMIT_OR_TYPE')
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise AdmissionError('DUPLICATE_KEY')
            result[key] = value
        return result
    def integer(text):
        if text == '-0':
            raise AdmissionError('NEGATIVE_ZERO')
        value = int(text)
        if not MIN_INT <= value <= MAX_INT:
            raise AdmissionError('INTEGER_RANGE')
        return value
    def forbidden(_):
        raise AdmissionError('FLOAT_OR_NONFINITE_FORBIDDEN')
    try:
        value = json.loads(raw.decode('utf-8','strict'), object_pairs_hook=pairs,
                           parse_int=integer, parse_float=forbidden, parse_constant=forbidden)
        typed(value)
        return value
    except (UnicodeError, ValueError, RecursionError) as exc:
        raise AdmissionError(str(exc)) from exc

def canonical(value):
    typed(value)
    # UTF-8 lexicographic key order equals Unicode scalar-value order for valid strings.
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True,
                     separators=(',', ':'), allow_nan=False).encode('utf-8')
    if len(raw) > MAX_BYTES:
        raise AdmissionError('BYTE_LIMIT')
    return raw

def identity(domain, value):
    if not domain or not all(c in 'abcdefghijklmnopqrstuvwxyz0123456789-.' for c in domain):
        raise AdmissionError('DOMAIN')
    raw = canonical(value)
    preimage = b'opensip.product.v1\0' + domain.encode('ascii') + b'\0' + len(raw).to_bytes(8,'big') + raw
    return hashlib.sha256(preimage).hexdigest()

def equal_typed(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return a.keys() == b.keys() and all(equal_typed(a[k], b[k]) for k in a)
    if type(a) is list:
        return len(a) == len(b) and all(equal_typed(x,y) for x,y in zip(a,b))
    return a == b

def exact_const(validator, expected, instance, schema):
    if not equal_typed(expected, instance):
        yield ValidationError('exact const type/value mismatch')

def exact_enum(validator, expected, instance, schema):
    if not any(equal_typed(x,instance) for x in expected):
        yield ValidationError('exact enum type/value mismatch')

def exact_order(validator, order, instance, schema):
    """Admission owns semantic order; canonical encoding preserves every array."""
    if type(instance) is not list or order == 'sequence':
        return
    try:
        if type(order) is dict:
            if set(order) != {'by'} or type(order['by']) is not list or not order['by'] or any(type(k) is not str or not k for k in order['by']) or len(set(order['by'])) != len(order['by']):
                raise ValueError('invalid field-order annotation')
            keys = [tuple(v[k].encode('utf-8') for k in order['by']) for v in instance]
        elif order == 'utf8':
            keys = [v.encode('utf-8') for v in instance]
        elif order in ('canonical-set', 'canonical-order'):
            keys = [canonical(v) for v in instance]
        elif order in ('path', 'ruleId', 'waiverId'):
            keys = [v[order].encode('utf-8') for v in instance]
        elif order == 'predicate':
            keys = [tuple(v[k].encode('utf-8') for k in ('ruleId','subjectId','predicateId')) for v in instance]
        elif order == 'numeric':
            if any(type(v) is not int for v in instance):
                raise ValueError('integer order required')
            keys = instance
        elif order == 'ordinal':
            keys = [v['ordinal'] for v in instance]
            if any(type(v) is not int for v in keys) or keys != list(range(len(keys))):
                raise ValueError('contiguous ordinal required')
        else:
            raise ValueError('unregistered order annotation')
        if keys != sorted(keys) or (order != 'canonical-order' and len(keys) != len(set(keys))):
            raise ValueError('canonical nondecreasing order required' if order == 'canonical-order' else 'strict unique order required')
    except (KeyError, TypeError, AttributeError, ValueError) as exc:
        yield ValidationError('array order '+str(order)+': '+str(exc))

ExactValidator = validators.extend(Draft202012Validator,
    validators={'const':exact_const, 'enum':exact_enum, 'x-opensip-order':exact_order},
    type_checker=Draft202012Validator.TYPE_CHECKER.redefine('integer',lambda checker, value:type(value) is int))

def validate(schema, value):
    typed(value)
    ExactValidator(schema).validate(value)
    return value
