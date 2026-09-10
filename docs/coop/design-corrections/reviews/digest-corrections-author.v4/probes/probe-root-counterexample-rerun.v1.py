"""Re-run of ROOT's confirmed v8 counterexample against the CORRECTED current source.

Provenance: the construction below is Codex/root's, from
docs/coop/design-corrections/reviews/codex-post-reset.v1/file-payload-counterexample.v9/attempt2/probe.py
which ran against the FROZEN v8 candidate and showed the truthful control AND all three
contradictory file payloads close, replay and COMMIT. That evidence is root's and is not rewritten
here; this file only asks the same four questions of the current tree.

Adaptations, all mechanical: the current fixture's FILTER_FIELD_OF is relation-keyed rather than
flat, and coverage_result now derives resolutionCompleteness from the rung itself, so the explicit
completeness_from_stage override root had to write is no longer needed. The graph is still built as
root built it - a references-shaped Run mutated into a file-shaped one - rather than through the new
build(relation='file') path, so the result is not an artifact of my own fixture shape.

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
    ns['ATOM']={'op':'none','relation':'file','minResolution':'syntax','filters':[{'field':'subject','cmp':'eq','value':wanted}]}
    r,o,b=ns['build'](has_match=True)
    inventory={v['path']:v for v in o[r['snapshotId']][1]['sourceInventory']};actual=inventory['a.ts']
    payload={'path':wanted,'contentSha256':actual['sha256'],'byteLength':actual['bytes']}
    if kind=='wrong-content-hash':payload['contentSha256']='f'*64
    if kind=='wrong-byte-length':payload['byteLength']+=1
    skey=next(k for k,(d,v) in o.items() if d=='subject-scope');scope=copy.deepcopy(o[skey][1])
    scope.update(relation='file',resolution='enumerated');rekey(o,skey,scope,r)
    fkey=next(k for k,(d,v) in o.items() if d=='fact');fact=copy.deepcopy(o[fkey][1])
    old_payload_digest=fact['payloadDigest']
    fact.update(relation='file',resolution='enumerated',payloadDigest=put(b,payload))
    new_fact=rekey(o,fkey,fact,r)
    coverage_admission=None
    for key in [k for k,(d,v) in o.items() if d=='coverage']:
        cov=copy.deepcopy(o[key][1]);sc=o[cov['scopeId']][1]
        p=ns['coverage_result'](sc,sc['sourceUniverse'],True)
        coverage_admission=N.admit_coverage_result_v3(p,sc,[],cov['payloadSchemaDigest'])
        assert coverage_admission['result']=='ADMIT',coverage_admission
        cov['payloadDigest']=put(b,p);rekey(o,key,cov,r)
    ns['resync_witness'](o,b,r);ns['resync_proof_refs'](o,b,r)
    view=o[o[r['evidenceId']][1]['viewIds'][0]][1]
    assert new_fact in view['facts'];assert old_payload_digest!=fact['payloadDigest']
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

# TRUTHFUL LABEL, added after execution: this version reproduced root's construction literally, and
# its three REFUSAL rows are valid (they are reached at Run closure, before replay). Its CONTROL row
# is not: the control closed but its store.prepare refused PROOF_REPLAY_MISMATCH, because root's
# frozen-source construction reset the module-level ATOM before calling build(), and the current
# build() takes the rule atom as a parameter derived from the relation instead of reading that
# global. So the control's policy stayed references-shaped while its fact became file-shaped, and
# the independent replay correctly disagreed with the committed proof. That is a probe-adaptation
# defect, not a finding about the graph. Superseded by probe-root-counterexample-rerun.v2.py, which
# builds the same file-shaped graph through the parameter. Retained unaltered above this line.
