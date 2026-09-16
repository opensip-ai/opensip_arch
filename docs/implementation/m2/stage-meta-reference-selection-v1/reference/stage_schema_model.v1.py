"""Proposed structural stage schema profile. Not selected until independent acceptance.
Registration does not compile producer regexes or evaluate producer instances.
"""
import hashlib,json
from pathlib import Path
from jsonschema import Draft202012Validator
from jsonschema.exceptions import ValidationError
from referencing import Registry,Resource
from referencing.jsonschema import DRAFT202012

_ROOT='https://json-schema.org/draft/2020-12/schema'
_VALIDATOR=None
class StageSchemaInvalid(ValueError):pass

def admit_document(document):
    global _VALIDATOR
    if _VALIDATOR is None:
        here=Path(__file__).resolve().parent/'stage-meta-2020-12'
        manifest=json.loads((here/'manifest.json').read_bytes());documents={}
        for row in manifest['files']:
            raw=(here/row['path']).read_bytes()
            if len(raw)!=row['bytes'] or hashlib.sha256(raw).hexdigest()!=row['sha256']:
                raise RuntimeError('STAGE_META_REFERENCE_BYTES')
            value=json.loads(raw)
            if value['$id']!=row['id'] or row['id'] in documents:raise RuntimeError('STAGE_META_REFERENCE_ID')
            documents[row['id']]=value
        registry=Registry().with_resources((key,Resource(contents=value,specification=DRAFT202012))for key,value in documents.items())
        # Explicit format-annotation profile. Optional URI/regex packages cannot
        # add assertions. References in PRODUCER documents are inert instance
        # strings here; only the closed bundled meta-schema graph is evaluated.
        _VALIDATOR=Draft202012Validator(documents[_ROOT],registry=registry,format_checker=None)
    try:_VALIDATOR.validate(document)
    except ValidationError as exc:raise StageSchemaInvalid('STAGE_META_DOCUMENT_INVALID')from exc
    return document
