"""Reviewer v10 harness.

Loads the FINAL v10 identity model from the reviewer's own disposable copy, after proving the
copy is byte-identical to the frozen subject. Never touches the frozen tree.

The model is loaded as a module (not by running the authored suite), so the reviewer drives the
pure law functions directly. Passing authored checks is not acceptance.
"""
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

COPY = Path('/tmp/opensip-design-corrections/post-reset-review.v10/work/copy')
SUBJECT = Path('/tmp/opensip-design-corrections/candidate-subject.v10')
FOUND = COPY / 'coop/design-corrections/foundation'
SUBJ_FOUND = SUBJECT / 'docs/coop/design-corrections/foundation'


def _sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def load_model():
    for name in ('identity-model.py', 'canonical.py', 'relation-payload-schemas.v2.json',
                 'identity-schemas.v2.json'):
        a, b = _sha(FOUND / name), _sha(SUBJ_FOUND / name)
        assert a == b, ('copy drifted', name, a, b)
    spec = importlib.util.spec_from_file_location('rev10_identity_model',
                                                  FOUND / 'identity-model.py')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod._sha256 = _sha(FOUND / 'identity-model.py')
    return mod


def base_document(model):
    """A deep copy of the shipped relation document, safe to mutate in a probe."""
    return copy.deepcopy(model.RELATION_DOCUMENT)


def try_closure(model, name, document):
    """Run the law for one relation; return ('ADMIT', None) or ('REFUSE', cause)."""
    try:
        model.relation_annotation_closure(name, document)
        return 'ADMIT', None
    except Exception as exc:  # AdmissionError or anything else - report faithfully
        return 'REFUSE', type(exc).__name__ + ':' + str(exc)


def custody(paths):
    out = {}
    for p in paths:
        b = (SUBJECT / p).read_bytes()
        out[p] = {'sha256': hashlib.sha256(b).hexdigest(), 'bytes': len(b)}
    return out


def emit(obj, path):
    Path(path).write_text(json.dumps(obj, indent=2, sort_keys=True, default=str) + '\n')
