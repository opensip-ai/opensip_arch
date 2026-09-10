"""CB-ADV-2, part 2: does SELECTION alone ever grant an import evidence authority?

`graph_with_import` builds its base graph with `with_finding=False`, so the p2 run skipped this
case. Here the harness's own `build` is bound to the finding-carrying variant for the duration of
the graph construction only; nothing in the model is patched.
"""
import copy, importlib.util, json
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


def outcome(name, fn, expect_token=None):
    try:
        value = fn()
    except BaseException as exc:                     # noqa: BLE001
        text = type(exc).__name__ + ':' + str(exc)[:220]
        row = {'probe': name, 'admitted': False, 'fault': text}
    else:
        row = {'probe': name, 'admitted': True, 'runId': value}
    if expect_token is not None:
        row['expectedToken'] = expect_token
        row['tokenMatched'] = (not row['admitted']) and expect_token in row.get('fault', '')
    results.append(row)
    print(json.dumps(row))
    return row


_base = F.build
F.build = lambda *a, **k: _base(resolved=True, has_match=True, with_finding=True)


def graph():
    return F.graph_with_import()


def proof_of(objects, run):
    pk = objects[run['evaluationSealId']][1]['proofBundleId']
    return pk, copy.deepcopy(objects[pk][1])


def cite_import_from_finding(unevaluate):
    run, objects, blobs = graph()
    pk, proof = proof_of(objects, run)
    import_hex = next(r['digest'] for r in proof['evaluationInputRefs'] if r['domain'] == 'import')
    if unevaluate:
        proof['evaluationInputRefs'] = [r for r in proof['evaluationInputRefs']
                                        if r['domain'] != 'import']
        for p in proof['predicateProofs']:
            p['inputRefs'] = [r for r in p['inputRefs'] if r['domain'] != 'import']
        F.rekey(objects, pk, proof, run)
    fid = objects[run['evidenceId']][1]['findingIds'][0]
    finding = copy.deepcopy(objects[fid][1])
    finding['evidenceRefs'] = sorted(finding['evidenceRefs'] +
                                     [{'domain': 'import', 'digest': import_hex}],
                                     key=C.canonical)
    F.rekey(objects, fid, finding, run)
    return run, objects, blobs


run, objects, blobs = graph()
print(json.dumps({'probe': 'context',
                  'findingIds': objects[run['evidenceId']][1]['findingIds'],
                  'planImportIds': objects[run['planId']][1]['importIds'],
                  'evidenceImportIds': objects[run['evidenceId']][1]['importIds']}))
outcome('P2-g0-finding-graph-baseline-admits', lambda: M.close_run(run, objects, blobs))

g = cite_import_from_finding(unevaluate=False)
outcome('P2-g1-finding-cites-an-EVALUATED-selected-import',
        lambda: M.close_run(*g))

g = cite_import_from_finding(unevaluate=True)
outcome('P2-g2-finding-cites-a-SELECTED-BUT-UNEVALUATED-import',
        lambda: M.close_run(*g), 'HIDDEN_FINDING_EVIDENCE')

(HERE / 'p2g_finding_import_authority.results.json').write_text(
    json.dumps({'results': results}, indent=1) + '\n')
