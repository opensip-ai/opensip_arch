"""Source42 capture joins outside the changed attribution loop, on the maintained file fixture (unsupported, two universes):
which owner refuses a captured, unattributed view whose planId is foreign AND whose producer is not the row/stage producer,
compared with the same-provider foreign-planId view and the foreign-producer view. Admission = admit_execution_inputs over the
host-edited builder manifest (explicit receipt + selectedRefs capture, store pointers from promised_pointers); closed-run column
= the same manifest through the maintained full_run driver. Writes only receipts/probes/capture-joins-on45.json."""
import contextlib, copy, importlib.util, io, json, sys, traceback
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v45')
DC = RT / 'work/source45-pkg/docs/coop/design-corrections'
OUT = RT / 'receipts/probes/capture-joins-on45.json'
ROWS = []


def row(case, ok, observed=None, expected=None, kind=None):
    r = {'case': case, 'ok': bool(ok), 'observed': observed}
    if expected is not None:
        r['expected'] = expected
    if kind:
        r['kind'] = kind
    ROWS.append(r)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(mod)
    return mod


def main():
    K = load('cj42_checker', DC / 'foundation/check-execution-inputs.v1.py')
    M, F, C = K.M, K.F, K.M.C
    NH = F.fixture_helpers()
    cov_schema = NH.N.schema_document_digest(NH.N.NATIVE_SCHEMA_DOC)

    def world(producer_of, plan_of):
        g = F.build_file_inputs(atom_override=K.NONE_ATOM, unsupported_cell='required', multiple_universes=True)
        o, b = g['objects'], g['blobs']
        first = o[g['viewIds'][0]][1]
        provider = first['producerClosure']
        rel_schema = next(d for d in first['schemaDigests'] if d != cov_schema)
        unis = {}
        for cell in g['enumerationPlan']['cells']:
            for bb in cell['programBindings']:
                unis.setdefault(cell['capabilityId'], []).append(bb['universe'])
        u0 = unis['references'][0]
        u1 = next(x for x in unis['inventory'] if x != u0)
        paths = [r['path'] for r in g['snapshot']['sourceInventory']]
        sid = K._mint(o, 'subject-scope', {'snapshotId': g['inputs']['plan']['snapshotId'], 'sourceUniverse': u1, 'targetUniverse': u1,
                                          'relation': 'references', 'resolution': 'resolved-binding', 'enumeratorClosure': provider, 'subjects': []})
        payload = NH.coverage_result(o[sid][1], u1, True, b, paths)
        cid = K._mint(o, 'coverage', {'scopeId': sid, 'payloadSchemaDigest': cov_schema, 'payloadDigest': K._blob(b, payload)})
        vid = K._mint(o, 'view', {'planId': plan_of(g), 'scopeIds': [sid], 'facts': [], 'coverageIds': [cid],
                                  'producerClosure': producer_of(g, provider), 'schemaDigests': M.canon_str_list([rel_schema, cov_schema])})
        g['viewIds'] = M.canon_str_list(g['viewIds'] + [vid])
        g['inputs']['evaluationInputRefs'] = K.canon_refs(g['inputs']['evaluationInputRefs'] + [{'domain': 'view', 'digest': K.hx(vid)}])
        g['coverageIds'] = M.canon_str_list(g['coverageIds'] + [cid])
        g['scopeIds'] = M.canon_str_list(g['scopeIds'] + [sid])
        g['inputs']['coverageCount'] = len(g['coverageIds'])
        return g, vid, cid

    def measure(name, producer_of, plan_of):
        g, vid, cid = world(producer_of, plan_of)
        kw = K.manifest_from_owner(copy.deepcopy(g))
        ei = kw['execution_inputs']
        ref = {'domain': 'view', 'digest': K.hx(vid)}
        for rc in ei['hostCapture']['stageReceipts']:
            if 'view' in rc['outputDomains']:
                rc['outputRefs'] = K.canon_refs(rc['outputRefs'] + [ref])
        ei['selectedRefs'] = K.canon_refs(ei['selectedRefs'] + [ref, {'domain': 'coverage', 'digest': K.hx(cid)}])
        kw['store_pointers'] = M.promised_pointers(ei, kw['plan'], kw['execution_plan'], kw['enumeration_plan'], objects=kw['objects'], blobs=kw['blobs'])['store_pointers']
        adm = K.admit(kw)
        rg = copy.deepcopy(g)
        d = M.raw_digest(ei)
        rg['blobs'][d] = C.canonical(ei)
        rg['inputs']['executionInputsDigest'] = d
        rg['inputs']['evaluationInputRefs'] = K.canon_refs(list(ei['selectedRefs']) + [{'domain': 'execution-inputs', 'digest': d}])
        rg['executionInputs'] = ei
        rg['executionInputsDigest'] = d
        try:
            result, proof = K.full_run(rg)
            run = {'closed': True, 'verdict': result['verdict'], 'sameManifest': proof['executionInputsDigest'] == d}
        except Exception as exc:  # noqa: BLE001
            run = {'closed': False, 'refused': type(exc).__name__ + ':' + str(exc)[:400]}
        return {'admission': {'result': adm.get('result'), 'refusals': adm.get('refusals')}, 'fullRun': run,
                'onRows': [r['capabilityId'] for r in ei['cellOutcomes'] if K.hx(vid) in r['viewDigests']]}

    same_plan = lambda g: g['inputs']['planId']
    foreign_plan = lambda g: 'plan2:' + '9' * 64
    provider_prod = lambda g, p: p
    evaluator_prod = lambda g, p: g['inputs']['evaluatorClosure']
    a = measure('same-provider-foreign-planId', provider_prod, foreign_plan)
    b = measure('foreign-producer-same-planId', evaluator_prod, same_plan)
    c = measure('foreign-producer-and-foreign-planId', evaluator_prod, foreign_plan)
    row('J1-same-provider-foreign-planId: admission PLAN_JOIN (the producer passes a row filter)', 'EXECUTION_INPUTS_PLAN_JOIN' in (a['admission']['refusals'] or []), a)
    row('J2-foreign-producer-same-planId (observation)', True, b, None, 'observation')
    row('J3-foreign-producer-and-foreign-planId (observation: which owner refuses)', True, c, None, 'observation')
    row('J2/J3 Run closure refuses both', b['fullRun'].get('closed') is False and c['fullRun'].get('closed') is False, {'J2': b['fullRun'], 'J3': c['fullRun']})


try:
    main()
except Exception:  # noqa: BLE001
    row('probe-crashed', False, traceback.format_exc()[-2500:])
OUT.write_text(json.dumps({'standing': 'independent reviewer probe on source42 owner modules; host-edited capture; not a multi-provider Run',
                           'rows': ROWS, 'failed': [r for r in ROWS if not r['ok']]}, indent=1, default=str))
print(json.dumps({'rows': ROWS}, indent=1, default=str)[:6000])
