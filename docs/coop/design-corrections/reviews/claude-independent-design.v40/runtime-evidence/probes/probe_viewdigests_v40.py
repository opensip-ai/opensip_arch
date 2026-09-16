"""CellProgramOutcomeV1.viewDigests attribution: what the normative text fixes versus what only the reference derives.

Builds the maintained execution-inputs owner graphs (the same builders check-execution-inputs.v1 uses: one-universe file graph,
missing-package graph, two-universe graph), records every cell row's viewDigests, finds views shared by more than one row,
and asks the reference admission (execution_inputs_model.v1.admit_execution_inputs) about host encodings a normative-only
reader could plausibly choose: attributing a shared view to only one row, and naming no view on a row. Writes only
receipts/probes/viewdigests-v40.json. Source-text facts are recorded as such."""
import contextlib, copy, importlib.util, io, json, re, sys, traceback
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v40')
DC = RT / 'work/source40-pkg/docs/coop/design-corrections'
OUT = RT / 'receipts/probes/viewdigests-v40.json'
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


def summarize(owner):
    out = []
    for r in owner['execution_inputs']['cellOutcomes']:
        out.append({'cell': r['cellOrdinal'], 'program': r['programOrdinal'], 'capability': r['capabilityId'], 'mode': r['languageMode'],
                    'universe': (r['universe'] or '')[:12], 'views': [v[:12] for v in r['viewDigests']]})
    return out


def main():
    K = load('vd40_checker', DC / 'foundation/check-execution-inputs.v1.py')
    text = (DC / 'foundation/execution-inputs-contract.v1.md').read_text()
    schema = json.loads((DC / 'foundation/execution-inputs.schema.v1.json').read_text())
    desc = schema['$defs']['CellProgramOutcomeV1']['properties']['viewDigests'].get('description')
    row('source-text-execution-inputs-contract-names-viewDigests', True, 'viewDigests' in text, None, 'source-text')
    row('source-text-schema-description-of-viewDigests', True, desc, None, 'source-text')
    graphs = {'one-universe': K.F.build_file_inputs(), 'missing-package': K.F.build_file_inputs(complete_required_native=False),
              'two-universes': K.F.build_file_inputs(multiple_universes=True)}
    for gname, graph in graphs.items():
        owner = K.manifest_from_owner(graph)
        base = K.admit(owner)
        rows = summarize(owner)
        row(gname + '-owner-admits', base.get('result') == 'ADMIT', {'result': base.get('result'), 'refusals': base.get('refusals'), 'rows': rows})
        counts = {}
        for r in owner['execution_inputs']['cellOutcomes']:
            for v in r['viewDigests']:
                counts.setdefault(v, []).append((r['cellOrdinal'], r['programOrdinal'], r['capabilityId']))
        shared = {v[:12]: owners for v, owners in counts.items() if len(owners) > 1}
        row(gname + '-views-attributed-to-more-than-one-cell-row', True, shared, None, 'observation')
        if shared:
            v_full = next(v for v, owners in counts.items() if len(owners) > 1)
            once = copy.deepcopy(owner)
            first = True
            for r in once['execution_inputs']['cellOutcomes']:
                if v_full in r['viewDigests']:
                    if first:
                        first = False
                    else:
                        r['viewDigests'] = [x for x in r['viewDigests'] if x != v_full]
            got = K.admit(once)
            row(gname + '-shared-view-named-on-only-its-first-row-refuses-view-totality', got.get('result') == 'REFUSE'
                and 'EXECUTION_INPUTS_VIEW_TOTALITY' in (got.get('refusals') or []), {'result': got.get('result'), 'refusals': got.get('refusals')})
        with_views = [i for i, r in enumerate(owner['execution_inputs']['cellOutcomes']) if r['viewDigests']]
        if with_views:
            none = copy.deepcopy(owner)
            none['execution_inputs']['cellOutcomes'][with_views[-1]]['viewDigests'] = []
            got = K.admit(none)
            row(gname + '-a-row-naming-no-view-while-its-producer-and-universe-returned-one-refuses', got.get('result') == 'REFUSE'
                and 'EXECUTION_INPUTS_VIEW_TOTALITY' in (got.get('refusals') or []), {'result': got.get('result'), 'refusals': got.get('refusals')})
    model = (DC / 'foundation/execution_inputs_model.v1.py').read_text()
    m = re.search(r"cap_rels = \{p\[0\] for p in _matrix_pairs\(cell\[\"capabilityId\"\]\)\}.*?_add\(faults, \"EXECUTION_INPUTS_VIEW_TOTALITY\"\)", model, re.S)
    row('source-text-reference-attribution-predicate', True, m.group(0) if m else None, None, 'source-text')
    if m:
        body = m.group(0)
        dead = re.search(r"matched_rel = True\n\s+if sc\[1\]\.get\(\"enumeratorClosure\"\) and producer and sc\[1\]\.get\(\"enumeratorClosure\"\) != producer:\n\s+continue\n", body)
        row('source-text-scope-enumeratorClosure-check-is-the-last-statement-of-the-scope-loop (its continue decides nothing)', True, bool(dead), None, 'source-text')


try:
    main()
except Exception:  # noqa: BLE001
    row('probe-crashed', False, traceback.format_exc()[-2500:])
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps({'standing': 'independent reviewer probe over the maintained execution-inputs owner graphs and reference admission; source-text rows record text only',
                           'rows': ROWS, 'failed': [r for r in ROWS if not r['ok']]}, indent=1, default=str))
print(json.dumps({'total': len(ROWS), 'failed': [(r['case'], r['observed']) for r in ROWS if not r['ok']],
                  'observations': [(r['case'], r['observed']) for r in ROWS if r.get('kind') in ('observation', 'source-text')]}, indent=1, default=str)[:9000])
