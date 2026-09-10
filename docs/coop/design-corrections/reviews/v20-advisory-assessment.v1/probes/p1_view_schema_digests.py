"""CB-ADV-1 probe: what does the accepted closure actually enforce about view.schemaDigests?

Runs entirely inside the COPY of the frozen tree at ../probe-tree (reviews/ excluded), against a
truncated fixture harness (_probe_fixtures.py = first 1020 lines of check-identity.py, i.e. its
constructors only, no suite execution and no report writing). The frozen tree is never imported
from and never written to.

Every mutation is re-minted through the harness's own `rekey`, which propagates the new view
identity up through proof-bundle, semantic-evidence, evaluation-seal and the Run, so a refusal is
evidence about the schemaDigests law and never about a stale identity.
"""
import copy, hashlib, importlib.util, json
from pathlib import Path

HERE = Path(__file__).resolve().parent
FOUND = HERE.parent / 'probe-tree/docs/coop/design-corrections/foundation'


def load(name, path):
    s = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m


F = load('probe_fixtures', FOUND / '_probe_fixtures.py')
M, C = F.M, F.C

results = []


def outcome(name, fn):
    try:
        value = fn()
    except BaseException as exc:                     # noqa: BLE001 - the fault name IS the result
        results.append({'probe': name, 'admitted': False,
                        'fault': type(exc).__name__ + ':' + str(exc)[:220]})
    else:
        results.append({'probe': name, 'admitted': True, 'runId': value})
    print(json.dumps(results[-1]))


def case(name, mutate, **build_kw):
    run, objects, blobs = F.build(**build_kw)
    view_id = objects[objects[run['evidenceId']][1]['viewIds'][0]][1] and \
        objects[run['evidenceId']][1]['viewIds'][0]
    view = copy.deepcopy(objects[view_id][1])
    mutate(view, objects, blobs)
    F.rekey(objects, view_id, view, run)
    outcome(name, lambda: M.close_run(run, objects, blobs))


REGISTRY = json.loads((FOUND / 'identity-schemas.v2.json').read_text())['x-opensip-payload-registry']
DOCS = {}
for cls, body in REGISTRY['classes'].items():
    if 'document' in body:
        DOCS[body['document']] = hashlib.sha256((FOUND.parent / body['document']).read_bytes()).hexdigest()
    for row in body.get('rows', {}).values():
        DOCS[row['document']] = hashlib.sha256((FOUND.parent / row['document']).read_bytes()).hexdigest()
BY_DIGEST = {v: k for k, v in DOCS.items()}


def describe(tag, **build_kw):
    run, objects, blobs = F.build(**build_kw)
    view = objects[objects[run['evidenceId']][1]['viewIds'][0]][1]
    facts = [objects[f][1] for f in view['facts']]
    covs = [objects[c][1] for c in view['coverageIds']]
    union = sorted({f['payloadSchemaDigest'] for f in facts} |
                   {c['payloadSchemaDigest'] for c in covs})
    row = {'probe': 'context:' + tag,
           'buildKwargs': {k: str(v) for k, v in build_kw.items()},
           'factCount': len(facts), 'coverageCount': len(covs),
           'viewSchemaDigests': [BY_DIGEST.get(d, d) for d in sorted(view['schemaDigests'])],
           'unionOfAdmittedPayloadSchemas': [BY_DIGEST.get(d, d) for d in union],
           'viewSetEqualsMechanicalUnion': union == sorted(view['schemaDigests'])}
    results.append(row)
    print(json.dumps(row))
    return run, objects, blobs


print(json.dumps({'probe': 'registered-documents', 'documents': DOCS}, indent=1))

# ---------------------------------------------- is the committed set the mechanical union at all?
run0, objects0, blobs0 = describe('no-facts', has_match=False)
outcome('P1-a-baseline-admits', lambda: M.close_run(run0, objects0, blobs0))
describe('with-a-relation-fact', has_match=True, source_path='a.ts')

# ------------------------------------------------------------------------------------- mutations
case('P1-b-empty-set', lambda v, o, b: v.update(schemaDigests=[]))
case('P1-c-drop-one-listed-schema',
     lambda v, o, b: v.update(schemaDigests=sorted(v['schemaDigests'])[:1]))
case('P1-c2-drop-the-schema-a-coverage-was-actually-admitted-under',
     lambda v, o, b: v.update(schemaDigests=sorted(
         set(v['schemaDigests']) - {o[v['coverageIds'][0]][1]['payloadSchemaDigest']})))


def add_registered_but_unused(v, o, b):
    """A REGISTERED document this view admitted nothing under: import-source-context."""
    raw = (FOUND / 'import-source-context.schema.json').read_bytes()
    d = hashlib.sha256(raw).hexdigest()
    b[d] = raw
    v['schemaDigests'] = sorted(set(v['schemaDigests']) | {d})


case('P1-d-add-registered-document-this-view-did-not-admit', add_registered_but_unused)


def add_unregistered_blob(v, o, b):
    """Arbitrary retained bytes that are NOT any registered schema document."""
    raw = b'{"not":"a registered schema document"}\n'
    d = hashlib.sha256(raw).hexdigest()
    b[d] = raw
    v['schemaDigests'] = sorted(set(v['schemaDigests']) | {d})


case('P1-e-add-unregistered-retained-blob', add_unregistered_blob)
case('P1-f-add-unretained-digest',
     lambda v, o, b: v.update(schemaDigests=sorted(set(v['schemaDigests']) | {'a' * 64})))


def only_unregistered(v, o, b):
    raw = b'totally unrelated bytes\n'
    d = hashlib.sha256(raw).hexdigest()
    b[d] = raw
    v['schemaDigests'] = [d]


case('P1-g-only-an-unregistered-retained-blob', only_unregistered)

(HERE / 'p1_view_schema_digests.results.json').write_text(
    json.dumps({'registeredDocuments': DOCS, 'results': results}, indent=1) + '\n')
