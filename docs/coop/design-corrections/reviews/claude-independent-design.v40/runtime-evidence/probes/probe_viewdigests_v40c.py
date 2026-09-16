"""viewDigests attribution, third probe: the other reading of a genuinely returned but unattributed view.

probe_viewdigests_v40b showed that the reference attributes V_decl (a producer- and universe-matched view whose only scope
relation is not an inventory relation) to no cell row and omits it from receipt outputRefs and selectedRefs, and that naming it
on the row refuses. Contract section 1 defines the record as a host observation of stage returns, with selectedRefs
stage-produced = union of complete receipt outputRefs. This probe asks the reference about the host that records V_decl as
returned: V_decl in the stage receipt outputRefs and in selectedRefs, on no cell row. Same minted graph as v40b.
Writes only receipts/probes/viewdigests-v40c.json."""
import contextlib, copy, importlib.util, io, json, sys, traceback
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v40')
DC = RT / 'work/source40-pkg/docs/coop/design-corrections'
OUT = RT / 'receipts/probes/viewdigests-v40c.json'
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
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    with contextlib.redirect_stdout(io.StringIO()):
        spec.loader.exec_module(module)
    return module


def receipts_of(ei):
    hc = ei.get('hostCapture') or {}
    return hc.get('stageReceipts') or []


def main():
    K = load('vd40c_checker', DC / 'foundation/check-execution-inputs.v1.py')
    owner = K.manifest_from_owner(K.F.build_file_inputs())
    objects, blobs = dict(owner['objects']), dict(owner['blobs'])
    binding = owner['enumeration_plan']['cells'][0]['programBindings'][0]
    uni, provider = binding['universe'], binding['enumerator']['closureId']
    snapshot_id = owner['plan']['snapshotId']
    existing = next(v for k, (d, v) in objects.items() if d == 'view')
    path = next(r['path'] for r in objects[snapshot_id][1]['sourceInventory'])
    minted = {}
    for label, relation, resolution in (('V_file', 'file', 'enumerated'), ('V_decl', 'declares', 'syntactic')):
        scope = K._mint(objects, 'subject-scope', {'snapshotId': snapshot_id, 'sourceUniverse': uni, 'targetUniverse': uni, 'relation': relation,
                                                     'resolution': resolution, 'enumeratorClosure': provider, 'subjects': [path]})
        minted[label] = K._mint(objects, 'view', {'planId': owner['plan_id'], 'scopeIds': [scope], 'facts': [], 'coverageIds': [],
                                                  'producerClosure': provider, 'schemaDigests': existing['schemaDigests']})
    rebuilt = K.rebuild_after_object_mutation(owner, objects, blobs, extra_view_ids=list(minted.values()))
    ei = rebuilt['execution_inputs']
    hexes = {label: K.hx(v) for label, v in minted.items()}
    base = K.admit(rebuilt)
    row('control-reference-rebuild-admits', base.get('result') == 'ADMIT', {'result': base.get('result'), 'refusals': base.get('refusals')})
    recs = receipts_of(ei)
    carrying = [i for i, r in enumerate(recs) if any(x.get('domain') == 'view' and x.get('digest') == hexes['V_file'] for x in r.get('outputRefs') or [])]
    row('control-V_file-is-in-exactly-one-stage-receipt', len(carrying) == 1,
        {'receipts': len(recs), 'carrying': carrying, 'V_declInAnyReceipt': any(x.get('digest') == hexes['V_decl'] for r in recs for x in r.get('outputRefs') or [])})
    if len(carrying) != 1:
        return
    returned = copy.deepcopy(rebuilt)
    rei = returned['execution_inputs']
    rrec = receipts_of(rei)[carrying[0]]
    ref = {'domain': 'view', 'digest': hexes['V_decl']}
    rrec['outputRefs'] = K.canon_refs(list(rrec['outputRefs']) + [ref])
    rei['selectedRefs'] = K.canon_refs(list(rei['selectedRefs']) + [ref])
    # Attempt 1 refused EXECUTION_INPUTS_REF_POINTER because the harness kept the pre-mutation pointer set. Section 2 requires
    # store_pointers = promised_pointers(...) of the manifest under test, so recompute it (checker idiom pointers_of as fallback).
    try:
        returned['store_pointers'] = K.M.promised_pointers(rei, returned['plan'], returned['execution_plan'], returned['enumeration_plan'],
                                                           objects=returned['objects'], blobs=returned['blobs'])['store_pointers']
        pointer_source = 'promised_pointers'
    except Exception as exc:  # noqa: BLE001
        returned['store_pointers'] = K.pointers_of(returned['objects'], returned['blobs'])
        pointer_source = 'pointers_of (promised_pointers raised %s: %s)' % (type(exc).__name__, str(exc)[:200])
    control = copy.deepcopy(rebuilt)
    control['store_pointers'] = returned['store_pointers'] if pointer_source == 'pointers_of' else control['store_pointers']
    got = K.admit(returned)
    row('host-records-V_decl-as-returned-in-receipt-and-selectedRefs-on-no-row', True,
        {'result': got.get('result'), 'refusals': got.get('refusals'), 'storePointers': pointer_source,
         'V_declPointerPresent': hexes['V_decl'] in json.dumps(returned['store_pointers']),
         'differsFromReferenceEncoding': K.M.raw_digest(rei) != K.M.raw_digest(ei)}, None, 'observation')


try:
    main()
except Exception:  # noqa: BLE001
    row('probe-crashed', False, traceback.format_exc()[-2500:])
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps({'standing': 'independent reviewer probe over the maintained owner graph and reference admission; extra views minted by the reviewer',
                           'rows': ROWS, 'failed': [r for r in ROWS if not r['ok']]}, indent=1, default=str))
print(json.dumps({'rows': ROWS}, indent=1, default=str)[:8000])
