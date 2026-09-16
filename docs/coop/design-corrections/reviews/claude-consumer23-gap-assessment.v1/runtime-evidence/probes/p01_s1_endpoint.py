"""P01 — V23-S1 on frozen candidate36 (read-only). A graph endpoint of kind=package without packageManifestPath, and every
other section-2 step-1 shape, measured on: raw schema (GraphEndpoint and GraphQueryRequestV1), the public execute_graph_query
wrapper (with CommandEnvelope validity), the parse helpers (effective_params / parse_endpoint_syntax) and the internal
traverse_projected_graph helper. Plus: can inventory_vertices ever populate its ambiguous set (the other ENDPOINT_AMBIGUOUS
clause)? Model behaviour is evidence, not normative input. No source byte is written."""
import copy, hashlib, importlib.util, json, os, sys, traceback

S36 = '/tmp/opensip-design-corrections/candidate-subject.v36'
WF = S36 + '/docs/coop/design-corrections/workflows'
OUT = '/tmp/opensip-design-corrections/claude-consumer23-gap-assessment.v1/receipts'
os.makedirs(OUT, exist_ok=True)
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
spec = importlib.util.spec_from_file_location('ckq36', WF + '/check-query-projection.v3.py')
CK = importlib.util.module_from_spec(spec)
spec.loader.exec_module(CK)
Q = CK.Q
R = {'owners': {p: sha(WF + '/' + p) for p in ('query_projection_model.v3.py', 'check-query-projection.v3.py', 'query-projection-contract.v3.md',
                                              'schemas/evaluator3/graph-query.schema.json')}}
U1 = 'a' * 64
SHAPES = {
    'package-without-packageManifestPath': {'universe': U1, 'kind': 'package', 'nativeSubjectId': 'app'},
    'package-with-empty-packageManifestPath': {'universe': U1, 'kind': 'package', 'nativeSubjectId': 'app', 'packageManifestPath': ''},
    'package-with-packageManifestPath (well-formed control)': {'universe': U1, 'kind': 'package', 'nativeSubjectId': 'app', 'packageManifestPath': 'app/package.json'},
    'symbol (well-formed control)': {'universe': U1, 'kind': 'symbol', 'nativeSubjectId': 'ts-symbol:src/a.ts#f'},
    'step1-packageManifestPath-on-file': {'universe': U1, 'kind': 'file', 'nativeSubjectId': 'src/a.ts', 'packageManifestPath': 'package.json'},
    'step1-kind-outside-set': {'universe': U1, 'kind': 'module', 'nativeSubjectId': 'x'},
    'step1-universe-not-64-hex': {'universe': 'abc', 'kind': 'symbol', 'nativeSubjectId': 'x'},
    'step1-empty-native-id': {'universe': U1, 'kind': 'symbol', 'nativeSubjectId': ''},
    'step1-extra-property': {'universe': U1, 'kind': 'symbol', 'nativeSubjectId': 'x', 'extra': 1},
}
S2_PREDICTION = {'package-without-packageManifestPath': 'QUERY.ENDPOINT_AMBIGUOUS', 'package-with-empty-packageManifestPath': 'QUERY.PARAMS_MALFORMED or QUERY.ENDPOINT_AMBIGUOUS (text silent on an empty coordinate)'}


def schema_verdict(selector, value):
    try:
        Q.validate_schema(Q.SCHEMA_ID + selector, value)
        return {'admit': True}
    except Exception as exc:  # noqa: BLE001
        return {'admit': False, 'error': str(exc).splitlines()[0][:220]}


def refusal(fn):
    try:
        out = fn()
        return {'refused': False, 'result': (str(type(out).__name__) + ':' + json.dumps(out, default=str)[:160]) if out is not None else None}
    except Q.QueryRefusal as exc:
        rec = {'refused': True, 'errorCode': exc.error_code, 'detail': exc.detail, 'subject': (str(exc.subject)[:200] if exc.subject is not None else None)}
        try:
            term = exc.termination()
            rec['terminationValid'] = CK.valid(CK.U + 'common:3#/$defs/StepTermination', term)[0]
            if getattr(exc, 'request', None) is not None or getattr(exc, 'host', None) is not None:
                env = exc.envelope()
                ok, why = CK.valid(CK.U + 'command-envelope:3', env)
                rec['envelopeValid'] = ok and env.get('kind') == 'failure' and 'run' not in env
                rec['envelopeErrors'] = [e.get('code') for e in env.get('errors', [])]
        except Exception as exc2:  # noqa: BLE001
            rec['envelopeError'] = '%s: %s' % (type(exc2).__name__, str(exc2)[:160])
        return rec
    except Exception as exc:  # noqa: BLE001
        return {'refused': 'untyped', 'exception': '%s: %s' % (type(exc).__name__, str(exc)[:200])}


rows = {}
for label, ep in SHAPES.items():
    params = {'relation': 'references', 'minResolution': 'resolved-binding', 'direction': 'outgoing', 'endpoint': copy.deepcopy(ep)}
    req = CK.request('graph.neighbors', CK.project_id(), {'runId': CK.run_id()}, params)
    row = {
        'rawSchemaGraphEndpoint': schema_verdict('#/$defs/GraphEndpoint', ep),
        'rawSchemaGraphQueryRequestV1': schema_verdict('#/$defs/GraphQueryRequestV1', req),
        'publicWrapper': refusal(lambda: Q.execute_graph_query(req, host=CK.host_obs())),
        'effectiveParamsHelper': refusal(lambda: Q.effective_params('graph.neighbors', params)),
        'parseEndpointSyntaxHelper': refusal(lambda: Q.parse_endpoint_syntax(ep, 'endpoint')),
        'internalTraverseHelper': refusal(lambda: Q.traverse_projected_graph('graph.neighbors', params, [], project_id=CK.project_id(), run_id=CK.run_id())),
        'section2Prediction': S2_PREDICTION.get(label, 'QUERY.PARAMS_MALFORMED' if label.startswith('step1') else 'admitted by section 2 (then view/vertex steps)')}
    rows[label] = row
    print('%-52s schemaEP=%-5s schemaReq=%-5s wrapper=%-26s helper=%-26s traverse=%s' % (
        label, row['rawSchemaGraphEndpoint']['admit'], row['rawSchemaGraphQueryRequestV1']['admit'],
        row['publicWrapper'].get('detail') or row['publicWrapper'].get('exception', 'not refused'),
        row['parseEndpointSyntaxHelper'].get('detail') or 'not refused', row['internalTraverseHelper'].get('detail') or row['internalTraverseHelper'].get('exception', 'not refused')), flush=True)
R['shapes'] = rows
pkg = rows['package-without-packageManifestPath']
R['observations'] = {
    'publicWrapperForMissingCoordinate': [pkg['publicWrapper'].get('errorCode'), pkg['publicWrapper'].get('detail')],
    'helperForMissingCoordinate': [pkg['parseEndpointSyntaxHelper'].get('errorCode'), pkg['parseEndpointSyntaxHelper'].get('detail')],
    'section2Predicts': 'QUERY.ENDPOINT_AMBIGUOUS',
    'wrapperEnvelopeValid': pkg['publicWrapper'].get('envelopeValid'),
    'wrapperDisagreesWithSection2': pkg['publicWrapper'].get('detail') != 'QUERY.ENDPOINT_AMBIGUOUS',
    'wrapperDisagreesWithHelper': pkg['publicWrapper'].get('detail') != pkg['parseEndpointSyntaxHelper'].get('detail'),
    'step1ShapesAgreeEverywhere': all(r['publicWrapper'].get('detail') == 'QUERY.PARAMS_MALFORMED' and r['parseEndpointSyntaxHelper'].get('detail') == 'QUERY.PARAMS_MALFORMED'
                                      and not r['rawSchemaGraphEndpoint']['admit'] for k, r in rows.items() if k.startswith('step1')),
    'wellFormedControlsPassSchemaAndReachRunCheck': all(rows[k]['rawSchemaGraphQueryRequestV1']['admit'] and rows[k]['publicWrapper'].get('detail') == 'QUERY.VIEW_UNKNOWN'
                                                        for k in rows if 'well-formed control' in k)}
print('\nobservations:', json.dumps(R['observations'], indent=1), flush=True)

# ---- the other ENDPOINT_AMBIGUOUS clause: can inventory_vertices ever mark a tuple ambiguous?
saved = (Q.load_enumeration_plan, Q.inventory_universe, Q._blob_payload)
amb = {}
try:
    Q.load_enumeration_plan = lambda plan, blobs: None
    Q.inventory_universe = lambda enum_plan, inv: U1
    Q._blob_payload = lambda blobs, digest, subject: blobs[digest]
    CASES = {
        'duplicate-symbol-rows-same-id': [{'kind': 'symbol', 'rows': [{'nativeSubjectId': 'ts-symbol:a#f'}]}, {'kind': 'symbol', 'rows': [{'nativeSubjectId': 'ts-symbol:a#f'}]}],
        'same-package-name-two-manifests': [{'kind': 'package', 'rows': [{'nativeSubjectId': 'app', 'path': 'a/package.json'}]}, {'kind': 'package', 'rows': [{'nativeSubjectId': 'app', 'path': 'b/package.json'}]}],
        'same-package-name-same-manifest-twice': [{'kind': 'package', 'rows': [{'nativeSubjectId': 'app', 'path': 'a/package.json'}, {'nativeSubjectId': 'app', 'path': 'a/package.json'}]}],
        'package-row-without-path': [{'kind': 'package', 'rows': [{'nativeSubjectId': 'app'}]}]}
    for label, invs in CASES.items():
        blobs = {'inv%d' % i: inv for i, inv in enumerate(invs)}
        proof = {'evaluationInputRefs': [{'domain': 'subject-inventory', 'digest': d} for d in blobs]}
        vertices, ambiguous = Q.inventory_vertices(proof, {}, blobs)
        amb[label] = {'vertices': sorted('|'.join(k) for k in vertices), 'ambiguous': sorted('|'.join(k) for k in ambiguous)}
    amb['_codeReading'] = 'key = endpoint_tuple(named); ambiguous.add(key) only if vertices[key] != named, but named = canonical_endpoint(ep) is a function of exactly the key fields'
except Exception:  # noqa: BLE001
    amb['error'] = traceback.format_exc()[-1200:]
finally:
    Q.load_enumeration_plan, Q.inventory_universe, Q._blob_payload = saved
R['inventoryVerticesAmbiguity'] = amb
R['multiVertexClauseEverPopulated'] = any(v.get('ambiguous') for k, v in amb.items() if isinstance(v, dict))
print('inventory_vertices ambiguity:', json.dumps(amb, indent=1), '\never populated:', R['multiVertexClauseEverPopulated'])
R['ownersUnchangedAfter'] = R['owners'] == {p: sha(WF + '/' + p) for p in R['owners']}
json.dump(R, open(os.path.join(OUT, 'p01-s1-endpoint.json'), 'w'), indent=1, default=str)
print('owners unchanged:', R['ownersUnchangedAfter'], '\nwrote p01-s1-endpoint.json')
