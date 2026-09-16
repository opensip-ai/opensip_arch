"""viewDigests attribution, second probe: does the reference attribution depend on a criterion the normative text does not state?

Mints two extra views into the maintained one-universe owner graph, both returned by the binding's own producer at the binding's
own universe and Plan: V_file (one subject-scope of relation `file`, a relation of the row's `inventory` capability) and V_decl
(one subject-scope of relation `declares`, not an inventory relation). Neither view names Coverage. The graph is rebuilt through
the maintained host-capture builder (rebuild_after_object_mutation). Then the reference admission is asked about:
  1. the rebuilt manifest (the reference's own attribution),
  2. a manifest whose only cell row names BOTH extra views, i.e. every view of this cell/program/U/producer (the four coordinates
     the schema description names).
Writes only receipts/probes/viewdigests-v40b.json."""
import contextlib, copy, importlib.util, io, json, sys, traceback
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v40')
DC = RT / 'work/source40-pkg/docs/coop/design-corrections'
OUT = RT / 'receipts/probes/viewdigests-v40b.json'
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


def main():
    K = load('vd40b_checker', DC / 'foundation/check-execution-inputs.v1.py')
    owner = K.manifest_from_owner(K.F.build_file_inputs())
    base = K.admit(owner)
    row('control-owner-admits', base.get('result') == 'ADMIT', {'result': base.get('result'), 'refusals': base.get('refusals')})
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
        view = K._mint(objects, 'view', {'planId': owner['plan_id'], 'scopeIds': [scope], 'facts': [], 'coverageIds': [], 'producerClosure': provider,
                                          'schemaDigests': existing['schemaDigests']})
        minted[label] = view
    try:
        rebuilt = K.rebuild_after_object_mutation(owner, objects, blobs, extra_view_ids=list(minted.values()))
    except Exception as exc:  # noqa: BLE001
        row('rebuild-through-the-maintained-builder', False, type(exc).__name__ + ':' + str(exc)[:400])
        return
    rows = rebuilt['execution_inputs']['cellOutcomes']
    hexes = {label: K.hx(v) for label, v in minted.items()}
    attributed = {label: [(r['cellOrdinal'], r['capabilityId']) for r in rows if h in r['viewDigests']] for label, h in hexes.items()}
    selected = {label: any(ref['domain'] == 'view' and ref['digest'] == h for ref in rebuilt['execution_inputs']['selectedRefs']) for label, h in hexes.items()}
    got = K.admit(rebuilt)
    row('reference-rebuild-admits', got.get('result') == 'ADMIT', {'result': got.get('result'), 'refusals': got.get('refusals')})
    row('reference-attribution-of-the-two-producer-and-universe-matched-views', True,
        {'attributedRows': attributed, 'inSelectedRefs': selected}, None, 'observation')
    four = copy.deepcopy(rebuilt)
    for r in four['execution_inputs']['cellOutcomes']:
        r['viewDigests'] = K.M.canon_str_list(list(dict.fromkeys(r['viewDigests'] + list(hexes.values()))))
    got4 = K.admit(four)
    row('a-manifest-attributing-every-view-of-this-cell-program-U-producer', True, {'result': got4.get('result'), 'refusals': got4.get('refusals')},
        None, 'observation')


try:
    main()
except Exception:  # noqa: BLE001
    row('probe-crashed', False, traceback.format_exc()[-2500:])
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps({'standing': 'independent reviewer probe over the maintained owner graph and reference admission; extra views minted by the reviewer',
                           'rows': ROWS, 'failed': [r for r in ROWS if not r['ok']]}, indent=1, default=str))
print(json.dumps({'rows': ROWS}, indent=1, default=str)[:8000])
