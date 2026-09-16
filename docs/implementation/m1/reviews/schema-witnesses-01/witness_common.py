"""Shared read-only loading and exact witness checks for the schema-witness corpus.

Reads only: metadata-v2 check_metadata.load() (which verifies the 28 schema pins and
the lexical canonical reference pin), the full-generator trial selectedTargets refs,
and optionally the TS-runtime harvest corpus. No generated carrier source is read.
"""
import hashlib
import importlib.util
import json
from pathlib import Path

ARCH = Path('/Users/sb/code/opensip-ai/opensip_arch')
IMPL = Path('/tmp/opensip-implementation')
OUT = IMPL / 'm1-schema-witnesses-01'
METADATA_DIR = ARCH / 'docs/implementation/m1/metadata-v2'
CHECK_METADATA = METADATA_DIR / 'check_metadata.py'
SOURCES = METADATA_DIR / 'sources.json'
SOURCE_MAP = IMPL / 'm1-full-generator-trial-01/source-map.json'
HARVEST = IMPL / 'm1-ts-runtime-review-01/work/probes/harvest-cases.json'


def pin(path):
    raw = Path(path).read_bytes()
    return {'path': str(path), 'sha256': hashlib.sha256(raw).hexdigest(), 'bytes': len(raw)}


def load():
    spec = importlib.util.spec_from_file_location('check_metadata_v2', CHECK_METADATA)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    reference, registry, documents = module.load(ARCH)
    return reference, registry, documents


def targets():
    return json.loads(SOURCE_MAP.read_bytes())['selectedTargets']


def check(reference, registry, ref, value):
    """None when value is exact-codec valid and valid for ref; else a precise error string."""
    try:
        reference.typed(value)
        raw = reference.canonical(value)
        back = reference.parse(raw)
        if not reference.equal_typed(back, value):
            return 'CANONICAL_ROUNDTRIP_MISMATCH'
        reference.validate({'$ref': ref}, back, registry)
        if not reference.ExactValidator({'$ref': ref}, registry=registry).is_valid(back):
            return 'EXACT_VALIDATOR_IS_VALID_FALSE'
    except Exception as exc:  # report, never count as covered
        message = getattr(exc, 'message', None) or str(exc)
        path = getattr(exc, 'json_path', None)
        schema_path = list(getattr(exc, 'absolute_schema_path', []) or [])
        return json.dumps({'error': type(exc).__name__, 'message': message[:600],
                           'instancePath': path, 'schemaPath': schema_path}, default=str)
    return None


def no_float(_):
    raise ValueError('float forbidden in witness corpus')
