"""Re-run v2 of ROOT's confirmed v8 counterexample against the CORRECTED current source.

Provenance: the construction below is Codex/root's, from
docs/coop/design-corrections/reviews/codex-post-reset.v1/file-payload-counterexample.v9/attempt2/probe.py
which ran against the FROZEN v8 candidate and showed the truthful control AND all three
contradictory file payloads close, replay and COMMIT. That evidence is root's and is not rewritten
here; this file only asks the same four questions of the current tree.

Adaptations, and why each was forced by the current source rather than chosen:
  * coverage_result now derives resolutionCompleteness from the RUNG, so root's explicit
    completeness_from_stage override is redundant. Root's note predicted exactly this.
  * the rule atom is now a build() parameter instead of a module-level global, so root's
    "reset ATOM, then build" step cannot reach the policy. v1 of this probe kept that step and
    produced a control that closed but failed replay with PROOF_REPLAY_MISMATCH - a defect of the
    adaptation, not of the graph. That run is retained, labelled, in
    probe-root-counterexample-rerun.v1.py.
The graph is otherwise root's: the file-shaped Run, the same four vectors, the same reachable-fact
and moved-payload assertions, and the same closure/replay/commit sequence.

Expected: control closes and commits; each contradictory payload refuses with its exact cause.
"""
import ast,copy,hashlib,json,sys
from pathlib import Path
root=Path('/Users/sb/code/opensip-ai/opensip_arch')
fixture=root/'docs/coop/design-corrections/foundation/check-identity.py'
source=fixture.read_text();tree=ast.parse(source)
last=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='graph_with_import').end_lineno
ns={'__file__':str(fixture),'__name__':'claude_current_file_fixture'}
exec(compile('\n'.join(source.split('\n')[:last]),str(fixture),'exec'),ns)
M,C,N=ns['M'],ns['C'],ns['N'];put,rekey=ns['put_blob'],ns['rekey'];rows=[]

def exercise(kind):
    wanted='absent.ts' if kind=='uninventoried-path' else 'a.ts'
    r,o,b=ns['build'](has_match=True,relation='file')
    inventory={v['path']:v for v in o[r['snapshotId']][1]['sourceInventory']};actual=inventory['a.ts']
    payload={'path':wanted,'contentSha256':actual['sha256'],'byteLength':actual['bytes']}
    if kind=='wrong-content-hash':payload['contentSha256']='f'*64
    if kind=='wrong-byte-length':payload['byteLength']+=1
    fkey=next(k for k,(d,v) in o.items() if d=='fact');fact=copy.deepcopy(o[fkey][1])
    old_payload_digest=fact['payloadDigest']
    fact.update(payloadDigest=put(b,payload))
    new_fact=rekey(o,fkey,fact,r)
    if kind!='control':
        assert new_fact!=fkey and fact['payloadDigest']!=old_payload_digest,'no-op mutation'
    coverage_admission=None
    for key in [k for k,(d,v) in o.items() if d=='coverage']:
        cov=copy.deepcopy(o[key][1]);sc=o[cov['scopeId']][1]
        p=ns['coverage_result'](sc,sc['sourceUniverse'],True)
        coverage_admission=N.admit_coverage_result_v3(p,sc,[],cov['payloadSchemaDigest'])
        assert coverage_admission['result']=='ADMIT',coverage_admission
        cov['payloadDigest']=put(b,p);rekey(o,key,cov,r)
    ns['resync_witness'](o,b,r);ns['resync_proof_refs'](o,b,r)
    view=o[o[r['evidenceId']][1]['viewIds'][0]][1]
    # root asserted the payload MOVED; for the control, which is now built file-shaped instead of
    # mutated into shape, the truthful payload is identical by construction and must stay so.
    assert new_fact in view['facts']
    assert (old_payload_digest==fact['payloadDigest']) if kind=='control' else True
    result={'id':kind,'payload':payload,'inventoryTruth':actual,'reachableFactId':new_fact,
            'coverageAdmission':coverage_admission,
            'resolutionCompleteness':p['entry']['resolutionCompleteness'],
            'entryCoverage':p['entry']['coverage']}
    try:
        rid=M.close_run(r,o,b);result['closure']={'admitted':True,'runId':rid}
        store=M.EvidenceStore();execution='exec1_'+'c'*32
        try:
            prepared=store.prepare(r,o,b,execution,ns['replay'])
            result['store']={'preparedRunId':prepared,'commit':store.commit(execution)}
        except Exception as exc:result['store']={'refused':str(exc),'exception':type(exc).__name__}
    except Exception as exc:result['closure']={'admitted':False,'cause':str(exc),'exception':type(exc).__name__}
    return result

for name in ('control','wrong-content-hash','wrong-byte-length','uninventoried-path'):rows.append(exercise(name))
print(json.dumps({
 'standing':'actual Claude coauthor re-run of ROOT-authored construction against the CURRENT tree; '
            'design/reference evidence only, no product qualification',
 'rootEvidence':'docs/coop/design-corrections/reviews/codex-post-reset.v1/file-payload-counterexample.v9/attempt2/result.json',
 'currentFixtureSha256':hashlib.sha256(fixture.read_bytes()).hexdigest(),
 'currentModelSha256':hashlib.sha256((root/'docs/coop/design-corrections/foundation/identity-model.py').read_bytes()).hexdigest(),
 'vectors':rows,
 'summary':{v['id']:(v['closure'].get('runId') or v['closure']['cause']) for v in rows}},indent=2))
