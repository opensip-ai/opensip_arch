"""p01: read-only measurement over the v2 working copy (no writes to the tree; interpreter -B).

For actually closed Runs (the declares Run root probed, and the golden work-budget-with-native-stage fixture):
- the Run's admitted execution plan (objects[run.evaluationSealId].executionPlanId), its stage count and ordinals;
- whether the plan record's planId is the Run's planId;
- the actual reference commit path: identity-model.v3 EvidenceStore.prepare + commit with a replay adapter over
  evaluator_replay_model.v3.derive, and whether its receipt inventoryDigest equals commit_inventory(runId, objects,
  blobs) over the same maps;
- root's three probe cases re-run against the unchanged v1 model bytes in this copy (expected RETURNED).
Output: receipts/p01-measure.json.
"""
import copy, hashlib, importlib.util, json, sys, traceback
from pathlib import Path

BASE = Path('/tmp/opensip-design-corrections/claude-source38-advisory-author.v2')
F = BASE / 'work/edited/docs/coop/design-corrections/foundation'


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


K = load('v2_measure_semantic', F / 'check-semantic-replay.v3.py')
T = load('v2_measure_termination', F / 'run_termination_model.v1.py')
Q = load('v2_measure_query', F.parent / 'workflows/query_projection_model.v3.py')
M, R = K.M, K.R
doc = json.loads((F / 'run-termination-goldens.v1.json').read_text())
out = {'standing': 'read-only measurement; reference evidence only', 'modelSha256': hashlib.sha256((F / 'run_termination_model.v1.py').read_bytes()).hexdigest()}


def facts(label, run, objects, blobs):
    rid = M.close_run(run, objects, blobs)
    seal = objects[run['evaluationSealId']][1]
    xp = seal['executionPlanId']
    plan = objects[xp][1]
    row = {'runId': rid, 'runHasExecutionPlanId': 'executionPlanId' in run, 'sealExecutionPlanId': xp,
           'executionPlanDomain': objects[xp][0], 'planIdJoin': plan['planId'] == run['planId'],
           'stageCount': len(plan['stages']), 'ordinals': [s['ordinal'] for s in plan['stages']],
           'proofExecutionPlanId': objects[seal['proofBundleId']][1]['executionPlanId'] == xp}
    _, inventory = M.commit_inventory(rid, objects, blobs)
    row['commitInventoryDigest'] = inventory
    try:
        _, owner = M.open_run_closure(run, objects, blobs)
        proof = objects[seal['proofBundleId']][1]

        def replay(plan_descriptor, objs, bl, refs):
            return R.derive(run['planId'], xp, seal['evaluatorClosure'], refs, objs, bl, owner)['proof']

        store = M.EvidenceStore()
        eid = 'exec1_' + 'd' * 32
        prepared = store.prepare(run, objects, blobs, eid, replay)
        committed = store.commit(eid)
        receipt = store.receipts[0]
        row['referenceCommit'] = {'prepared': prepared, 'commit': committed, 'receipt': receipt,
                                  'inventoryEqualsCommitInventory': receipt['inventoryDigest'] == inventory,
                                  'storeInventoryObjectsEqual': set(store.inventories[rid]['objects']) == set(objects)}
    except Exception as exc:
        row['referenceCommit'] = {'error': type(exc).__name__ + ': ' + str(exc)[:300], 'tb': traceback.format_exc()[-1200:]}
    out[label] = row
    return rid, xp, len(plan['stages'])


g, (run, objects, blobs), actual = K.case_declares_exists()
rid, xp, n = facts('declares', run, objects, blobs)
fixture = doc['fixtures']['incoming-incomplete']
params = dict(fixture['params'], budget_limit=1, references_stage_terminals={'foo': 'budget-exhausted'}, atom=K.REFS_NONE_TGT)
run2, objects2, blobs2, _ = K.close_positive(K.S.build_ts_semantic_graph(**params))
facts('work-budget-with-native-stage-budget-carrier', run2, objects2, blobs2)

# root's three cases, unchanged v1 model in this copy
derived = T.finalize(run, objects, blobs)['termination']
eid = 'exec1_' + 'a' * 32
_, inventory = M.commit_inventory(rid, objects, blobs)
receipt = {'schemaVersion': 2, 'runId': rid, 'executionId': eid, 'namespaceId': 'root-reference', 'commitSequence': 1,
           'inventoryDigest': inventory, 'sealedAssurance': 'replayable', 'signerKeyId': 'reference-host'}
attempt = {'executionId': eid, 'outcome': 'completed', 'derivation': {'planId': run['planId'], 'executionPlanId': xp,
                                                                        'stageCount': n, 'stagesCompleted': n}}
obs = {'stepId': 0, 'durability': 'authoritative', 'attempts': [attempt], 'commitReceipt': receipt, 'requiredClosureNotInstalled': False}
rs = copy.deepcopy(M.SCHEMA)
rs['$ref'] = '#/$defs/commit-receipt'
rows = []
for name in ('baseline', 'wrong-execution-plan', 'wrong-inventory-digest'):
    o = copy.deepcopy(obs)
    if name == 'wrong-execution-plan':
        o['attempts'][0]['derivation']['executionPlanId'] = 'exec-plan2:' + 'e' * 64
    if name == 'wrong-inventory-digest':
        o['commitReceipt']['inventoryDigest'] = 'f' * 64
    try:
        got = T.admit_analysis_step_termination(
            derived, run, objects, blobs, o,
            lambda v: Q.validate_schema(Q.COMMON_ID + '#/$defs/StepTermination', v),
            lambda v: Q.validate_schema('urn:opensip:product-v1:workflows:evaluator3:invocation:3#/$defs/Attempt', v),
            lambda v: M.C.validate(rs, v))
        rows.append({'case': name, 'outcome': 'RETURNED', 'standing': got['standing']})
    except Exception as exc:
        rows.append({'case': name, 'outcome': 'REFUSE', 'reason': str(exc)[:160]})
out['rootCasesOnV1Model'] = rows
(BASE / 'receipts' / 'p01-measure.json').write_text(json.dumps(out, indent=1, default=str) + '\n')
print(json.dumps(out, indent=1, default=str)[:12000])
