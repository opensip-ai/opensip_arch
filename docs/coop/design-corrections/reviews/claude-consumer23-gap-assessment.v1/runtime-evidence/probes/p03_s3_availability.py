"""P03 — V23-S3 on frozen candidate36 (read-only). Every identity availability state (plus omitted and two non-states) through
the PUBLIC execute_graph_query wrapper over a REAL admitted Run built with the query checker's own semantic fixture
(close_positive), with StepTermination and CommandEnvelope validity. Plus: identity availability enum, registry evidence.*
records, the query s7 paragraph and table, the identity model's own unavailability termination, and which states existing
controls exercise. Model behaviour is evidence, not normative input. No source byte is written."""
import hashlib, importlib.util, json, os, re

S36 = '/tmp/opensip-design-corrections/candidate-subject.v36'
DC = S36 + '/docs/coop/design-corrections'
WF = DC + '/workflows'
OUT = '/tmp/opensip-design-corrections/claude-consumer23-gap-assessment.v1/receipts'
sha = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()
OWN = [WF + '/query_projection_model.v3.py', WF + '/check-query-projection.v3.py', WF + '/query-projection-contract.v3.md', DC + '/foundation/identity-schemas.v3.json',
       DC + '/foundation/identity-model.v3.py', DC + '/public-detail-registry.v1.json', S36 + '/docs/v2/contracts/product-v1/identity-and-evidence.md']
R = {'owners': {os.path.relpath(p, S36): sha(p) for p in OWN}}
spec = importlib.util.spec_from_file_location('ckq36b', WF + '/check-query-projection.v3.py')
CK = importlib.util.module_from_spec(spec)
spec.loader.exec_module(CK)
Q = CK.Q
ids = json.load(open(DC + '/foundation/identity-schemas.v3.json'))


def find_def(o, key):
    if isinstance(o, dict):
        if key in o and isinstance(o[key], dict) and 'properties' in o[key]:
            return o[key]
        for v in o.values():
            hit = find_def(v, key)
            if hit is not None:
                return hit
    return None


STATES = find_def(ids, 'availability')['properties']['state']['enum']
R['identityAvailabilityStates'] = STATES
reg = json.load(open(DC + '/public-detail-registry.v1.json'))
R['registryEvidenceRecords'] = [r for r in reg['records'] if r['code'].startswith('evidence.')]
R['registryHasEvidenceUnavailable'] = any(r['code'] == 'evidence.unavailable' for r in reg['records'])
contract = open(WF + '/query-projection-contract.v3.md', encoding='utf-8').read()
para = next(l for l in contract.splitlines() if l.startswith('Identity **availability**'))
table_rows = [l for l in contract.splitlines() if l.startswith('|') and 'HOST.IO_FAILURE' in l]
R['contractAvailabilityParagraph'] = para
R['contractHostIoRows'] = table_rows
R['contractNamesDetailForUnavailable'] = bool(re.search(r'unavailable[^.|]{0,60}evidence\.(missing|[a-z-]+)', para)) or any('unavailable' in r for r in table_rows)
R['identityModelUnavailabilityTermination'] = Q.identity3().EvidenceUnavailable('ref').termination
R['modelAvailRefuse'] = Q.AVAIL_REFUSE
src = open(WF + '/check-query-projection.v3.py', encoding='utf-8').read()
R['existingControlsByState'] = {s: bool(re.search(r'availability="%s"' % s, src)) for s in STATES + ['missing']}
print('states:', STATES, '| registry evidence.unavailable:', R['registryHasEvidenceUnavailable'], '| contract names unavailable detail:', R['contractNamesDetailForUnavailable'])
print('controls by state:', R['existingControlsByState'])
print('identity EvidenceUnavailable termination:', R['identityModelUnavailabilityTermination'])

foundation = WF.rsplit('/', 1)[0] + '/foundation'
S = CK.load('p03_semantic_fixture3', CK.HERE.parent / 'foundation' / 'evaluator_semantic_fixture.v3.py')
replay = CK.load('p03_semantic_replay_check3', CK.HERE.parent / 'foundation' / 'check-semantic-replay.v3.py')
atom = {'op': 'none', 'relation': 'references', 'minResolution': 'resolved-binding', 'endpoint': 'target', 'filters': []}
g = S.build_ts_semantic_graph(atom=atom, has_declares=False, has_references_fact=True, second_partition=True, references_resolved=False, incoming_search=True,
                              incoming_complete=False, target_sidecar=True, second_universe=True)
run, objects, blobs, actual = replay.close_positive(g)
run_key = actual['runId']
req = CK.request('graph.neighbors', run['projectId'], {'runId': run_key},
                 {'relation': 'references', 'minResolution': 'resolved-binding', 'direction': 'outgoing', 'endpoint': CK.ep(g['u1'], 'symbol', g['foo'])})
results = {}
for state in [None] + STATES + ['missing', 'not-a-state']:
    host = CK.host_obs(latestRunId=run_key) if state is None else CK.host_obs(latestRunId=run_key, availability=state)
    try:
        out = Q.execute_graph_query(req, run, objects, blobs, host=host)
        results[str(state)] = {'refused': False, 'items': len(out['items']), 'termination': out['termination']}
    except Q.QueryRefusal as exc:
        term = exc.termination()
        env = exc.envelope()
        results[str(state)] = {'refused': True, 'class': term['class'], 'errorCode': term.get('errorCode'), 'faultCause': term.get('faultCause'),
                               'detail': exc.detail, 'subject': exc.subject, 'terminationValid': CK.valid(CK.U + 'common:3#/$defs/StepTermination', term)[0],
                               'envelopeValid': CK.valid(CK.U + 'command-envelope:3', env)[0] and env.get('kind') == 'failure' and 'run' not in env,
                               'envelopeErrors': [e.get('code') for e in env.get('errors', [])]}
    print('%-14s %s' % (state, json.dumps(results[str(state)], default=str)[:220]), flush=True)
R['publicWrapperByAvailability'] = results
R['observedMapping'] = {s: results[s].get('detail') if results[s]['refused'] else 'not refused by the observation' for s in results}
R['ownersUnchangedAfter'] = R['owners'] == {os.path.relpath(p, S36): sha(p) for p in OWN}
json.dump(R, open(os.path.join(OUT, 'p03-s3-availability.json'), 'w'), indent=1, default=str)
print('observed mapping:', R['observedMapping'], '\nowners unchanged:', R['ownersUnchangedAfter'], '\nwrote p03-s3-availability.json')
