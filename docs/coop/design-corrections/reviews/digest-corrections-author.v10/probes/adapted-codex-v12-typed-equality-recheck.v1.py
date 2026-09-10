"""ADAPTED copy of root's prepared final-source recheck. Not root's run, and not run in root's place.

Original: /tmp/opensip-design-corrections/codex-post-reset.v1/recheck-annotation-typed-equality-final-v12.py
          4193 bytes, sha256 47e2cfe70dc76228cd943e641a8b04d1e075efed3d9bdd4489c500719111e1e0
The original is preserved unmodified and was NOT executed here: it writes into a repository path
(docs/coop/design-corrections/reviews/codex-post-reset.v1/...), asserts `not out.exists()`, and reads
a handoff.json/custody.json that only exist once root has retained this delta. Running it as written
would have written outside my ownership and would have burned root's one-shot output directory.

Adaptations, all labelled, none touching the vectors or the verdict logic:
  * `r` is my disposable work root instead of Path.cwd() of the repository.
  * the handoff.json / custody.json / ownedFilesChanged pre-assertions are dropped (those artefacts
    are root's retention record; this run happens before the handoff exists). The equivalent hashes
    are printed instead so root can compare them with the shipped handoff rows.
  * `out` is a probe result file under my own outputs; no source-delta copy, no probe.py copy, no
    mkdir of a repository reviews directory.
  * the final asserts are kept (passed, discriminatingRefusals > 0).
The pair table, the five document shapes, the annotation builder, the metaschema check, the
before/final two-image comparison and the pass rule are byte-for-byte root's.
"""
import copy, hashlib, importlib.util, json
from pathlib import Path

from jsonschema import Draft202012Validator

# ADAPTED: work root, not the repository working directory.
r = Path('/tmp/opensip-design-corrections/digest-corrections-author.v10/work')
dc = r / 'docs/coop/design-corrections'
out = Path('/tmp/opensip-design-corrections/digest-corrections-author.v10/probes'
           '/result-adapted-codex-v12-typed-equality-recheck.v1.json')
sha = lambda p: hashlib.sha256(p.read_bytes()).hexdigest()

def load(path, name):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

M = load(dc / 'foundation/identity-model.py', 'codex_v12_typed_final')
P = load(Path('/tmp/opensip-design-corrections/candidate-subject.v11/docs/coop/design-corrections'
              '/foundation/identity-model.py'), 'codex_v11_typed_before')

pairs = [('integer-vs-boolean', 1, True, False), ('boolean-vs-integer', True, 1, False),
         ('nested-integer-vs-boolean', {'v': [1]}, {'v': [True]}, False),
         ('same-integer', 1, 1, True), ('same-boolean', True, True, True),
         ('same-nested', {'v': [True]}, {'v': [True]}, True),
         ('ordinary-string-conflict', 'one', 'two', False)]

def annotation(value):
    return {'representation': 'raw-artifact', 'retention': 'not-joined',
            'authority': 'Codex schema-only probe', 'ordinal': copy.deepcopy(value)}

def leaf(ann):
    return {'$ref': '#/$defs/DigestHex', 'x-opensip-digest': ann}

def document(shape, a, b):
    d = copy.deepcopy(M.RELATION_DOCUMENT)
    props = d['$defs']['FilePayloadV1']['properties']
    if shape == 'property-alias':
        d['$defs']['ProbeAlias'] = leaf(b)
        props['probe'] = {'$ref': '#/$defs/ProbeAlias', 'x-opensip-digest': a}
    elif shape == 'parent-nullable-branch':
        props['probe'] = {'x-opensip-digest': a, 'oneOf': [leaf(b), {'type': 'null'}]}
    elif shape == 'alias-chain':
        d['$defs']['ProbeA'] = {'$ref': '#/$defs/ProbeB', 'x-opensip-digest': a}
        d['$defs']['ProbeB'] = leaf(b)
        props['probe'] = {'$ref': '#/$defs/ProbeA'}
    elif shape == 'enclosing-container':
        props['probe'] = {'type': 'object', 'x-opensip-digest': a, 'properties': {'leaf': leaf(b)}}
    elif shape == 'same-path-merge':
        d['$defs']['ProbeContainer'] = {'type': 'object', 'properties': {'leaf': leaf(a)}}
        props['probe'] = {'$ref': '#/$defs/ProbeContainer', 'properties': {'leaf': leaf(b)}}
    else:
        raise AssertionError(shape)
    Draft202012Validator.check_schema(d)
    return d

def run(model, d):
    try:
        model.relation_annotation_closure('file', copy.deepcopy(d))
        return {'admitted': True}
    except Exception as e:
        return {'admitted': False, 'cause': str(e), 'exception': type(e).__name__}

rows = []
for shape in ['property-alias', 'parent-nullable-branch', 'alias-chain', 'enclosing-container',
              'same-path-merge']:
    for label, a, b, equal in pairs:
        d = document(shape, annotation(a), annotation(b))
        before = run(P, d)
        final = run(M, d)
        passed = final['admitted'] if equal else \
            'RELATION_DIGEST_ANNOTATION_CONFLICT' in final.get('cause', '')
        rows.append({'id': shape + '/' + label, 'expectedAdmit': equal, 'pythonValuesEqual': a == b,
                     'before': before, 'final': final, 'passed': passed})

result = {
    'standing': 'ADAPTED coauthor run of root\'s prepared v12 recheck against my final work-root '
                'source. Schema/reference evidence only. Not root\'s run, not the independent '
                'reviewer\'s verdict, no acceptance, readiness or product qualification.',
    'originalScript': {
        'path': '/tmp/opensip-design-corrections/codex-post-reset.v1/'
                'recheck-annotation-typed-equality-final-v12.py',
        'bytes': 4193,
        'sha256': '47e2cfe70dc76228cd943e641a8b04d1e075efed3d9bdd4489c500719111e1e0',
        'executedAsWritten': False},
    'baseManifestSha256': 'a03b7fe987ee886101a6d5b85bf4b0760f59b06a5a9e9c5f627accb9a7263bdf',
    'allVectorsMetaschemaValid': True,
    # ADAPTED: printed instead of asserted against a handoff that does not exist yet.
    'ownedFileHashesAtRunTime': [
        {'path': 'docs/coop/design-corrections/foundation/identity-model.py',
         'sha256': sha(dc / 'foundation/identity-model.py')},
        {'path': 'docs/coop/design-corrections/foundation/check-identity.py',
         'sha256': sha(dc / 'foundation/check-identity.py')}],
    'vectors': rows,
    'discriminatingRefusals': sum(x['before']['admitted'] and not x['final']['admitted']
                                  and not x['expectedAdmit'] for x in rows),
    'shapesThatDiscriminate': sorted({x['id'].split('/')[0] for x in rows
                                      if x['before']['admitted'] and not x['final']['admitted']}),
    'shapesAlreadyCorrectOnFrozenV11': sorted(
        {x['id'].split('/')[0] for x in rows} -
        {x['id'].split('/')[0] for x in rows
         if x['before']['admitted'] and not x['final']['admitted']}),
    'passed': all(x['passed'] for x in rows),
}
out.write_text(json.dumps(result, indent=2) + '\n')
assert result['passed'], 'Exact failed result/source retained; do not overwrite'
assert result['discriminatingRefusals'] > 0
print(len(rows), 'typed annotation cases pass across five collection/inheritance/merge locations;',
      result['discriminatingRefusals'], 'refusals discriminate frozen v11 from final source.')
print('discriminating shapes  :', result['shapesThatDiscriminate'])
print('already correct on v11 :', result['shapesAlreadyCorrectOnFrozenV11'])
