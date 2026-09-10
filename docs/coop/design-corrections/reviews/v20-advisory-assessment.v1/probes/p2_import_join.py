"""CB-ADV-2 probe: is semantic-evidence.importIds <-> plan.importIds already an enforced law?

Same sandbox and harness discipline as p1. Each mutation is re-minted through the harness's own
`rekey`, so refusals are about the import join and never about a stale identity. Every negative
asserts its EXACT refusal token, so a refusal at a different join is never counted as coverage of
the intended one.
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
    except BaseException as exc:                     # noqa: BLE001 - the fault name IS the result
        text = type(exc).__name__ + ':' + str(exc)[:220]
        row = {'probe': name, 'admitted': False, 'fault': text}
        if expect_token is not None:
            row['expectedToken'] = expect_token
            row['tokenMatched'] = expect_token in text
    else:
        row = {'probe': name, 'admitted': True, 'runId': value}
        if expect_token is not None:
            row['expectedToken'] = expect_token
            row['tokenMatched'] = False
    results.append(row)
    print(json.dumps(row))
    return row


def graph():
    return F.graph_with_import()


def evidence_of(objects, run):
    return copy.deepcopy(objects[run['evidenceId']][1])


def proof_of(objects, run):
    pk = objects[run['evaluationSealId']][1]['proofBundleId']
    return pk, copy.deepcopy(objects[pk][1])


# ------------------------------------------------------------------------------------ P2-a base
run, objects, blobs = graph()
plan_imports = objects[run['planId']][1]['importIds']
ev_imports = objects[run['evidenceId']][1]['importIds']
pk, proof = proof_of(objects, run)
ref_imports = sorted('import2:' + r['digest'] for r in proof['evaluationInputRefs']
                     if r['domain'] == 'import')
print(json.dumps({'probe': 'context', 'planImportIds': plan_imports,
                  'evidenceImportIds': ev_imports, 'evaluatedImportRefs': ref_imports,
                  'planEqualsEvidence': plan_imports == ev_imports}))
outcome('P2-a-baseline-admits', lambda: M.close_run(run, objects, blobs))

# -------------------------------- P2-b evidence drops a Plan-selected import (the claimed law)
run, objects, blobs = graph()
ev = evidence_of(objects, run)
ev['importIds'] = []
F.rekey(objects, run['evidenceId'], ev, run)
outcome('P2-b-evidence-omits-a-selected-import', lambda: M.close_run(run, objects, blobs),
        'IMPORT_JOIN')

# ---------------------------- P2-c evidence names an import the Plan did not select (both ways)
run, objects, blobs = graph()
plan = copy.deepcopy(objects[run['planId']][1])
plan['importIds'] = []
F.rekey_plan(objects, blobs, run, plan)
outcome('P2-c-plan-omits-an-import-the-evidence-names', lambda: M.close_run(run, objects, blobs),
        'IMPORT_JOIN')

# ------- P2-d selected but NOT evaluated: import stays in plan+evidence, leaves the proof refs
run, objects, blobs = graph()
pk, proof = proof_of(objects, run)
proof['evaluationInputRefs'] = [r for r in proof['evaluationInputRefs'] if r['domain'] != 'import']
for p in proof['predicateProofs']:
    p['inputRefs'] = [r for r in p['inputRefs'] if r['domain'] != 'import']
F.rekey(objects, pk, proof, run)
outcome('P2-d-selected-but-not-evaluated-still-admits', lambda: M.close_run(run, objects, blobs))

# ------------- P2-e the same graph with the non-evaluated selected import object withheld
run, objects, blobs = graph()
pk, proof = proof_of(objects, run)
proof['evaluationInputRefs'] = [r for r in proof['evaluationInputRefs'] if r['domain'] != 'import']
for p in proof['predicateProofs']:
    p['inputRefs'] = [r for r in p['inputRefs'] if r['domain'] != 'import']
F.rekey(objects, pk, proof, run)
withheld = {k: v for k, v in objects.items() if v[0] != 'import'}
outcome('P2-e-non-evaluated-selected-import-must-still-be-retained',
        lambda: M.close_run(run, withheld, blobs), 'EVIDENCE_UNAVAILABLE')

# ------------- P2-f evaluated but unselected: proof cites an import neither plan nor evidence has
run, objects, blobs = graph()
plan = copy.deepcopy(objects[run['planId']][1])
selected = plan['importIds'][0]
plan['importIds'] = []
F.rekey_plan(objects, blobs, run, plan)
ev = evidence_of(objects, run)
ev['importIds'] = []
F.rekey(objects, run['evidenceId'], ev, run)
outcome('P2-f-evaluated-but-unselected-import', lambda: M.close_run(run, objects, blobs),
        'UNSELECTED_EVALUATION_IMPORT')

# ------------- P2-g a finding may cite only an EVALUATED import, not merely a selected one
run, objects, blobs = F.graph_with_import()
pk, proof = proof_of(objects, run)
import_hex = next(r['digest'] for r in proof['evaluationInputRefs'] if r['domain'] == 'import')
proof['evaluationInputRefs'] = [r for r in proof['evaluationInputRefs'] if r['domain'] != 'import']
for p in proof['predicateProofs']:
    p['inputRefs'] = [r for r in p['inputRefs'] if r['domain'] != 'import']
F.rekey(objects, pk, proof, run)
finding_ids = objects[run['evidenceId']][1]['findingIds']
if finding_ids:
    fid = finding_ids[0]
    finding = copy.deepcopy(objects[fid][1])
    finding['evidenceRefs'] = sorted(finding['evidenceRefs'] +
                                     [{'domain': 'import', 'digest': import_hex}],
                                     key=C.canonical)
    F.rekey(objects, fid, finding, run)
    outcome('P2-g-finding-cites-a-selected-but-unevaluated-import',
            lambda: M.close_run(run, objects, blobs), 'HIDDEN_FINDING_EVIDENCE')
else:
    results.append({'probe': 'P2-g-finding-cites-a-selected-but-unevaluated-import',
                    'skipped': 'harness graph carries no finding'})
    print(json.dumps(results[-1]))

(HERE / 'p2_import_join.results.json').write_text(json.dumps({'results': results}, indent=1) + '\n')
