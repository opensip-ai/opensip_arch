"""Re-run of ROOT's executed partial-clone-Coverage counterexample against the CORRECTED source.

Provenance: the construction is Codex/root's, from
docs/coop/design-corrections/reviews/codex-post-reset.v1/partial-clone-coverage-counterexample.v9/probe.py,
which ran against captured in-progress v6 source and showed BOTH vectors close, replay and COMMIT:
the honest `unknown`/indeterminate control AND a contradictory `complete` Coverage with no
deficiency and a determinate `fail` seal, over the same partial ownership and the same empty view.
That evidence is root's and is not rewritten here.

Only the two mechanical adaptations root's own construction needs against the current tree are made:
the probe reads the workspace shape out of the built universe's retained ownership record (which now
carries `units` and `selectedUnitIds`), and it runs against the working tree rather than a copied
v8 base. The two vectors, their assertions and their reporting are otherwise root's.

Expected now: the honest control still closes, replays and commits; the contradictory claim refuses
with its exact cause at the owning Run's Coverage admission.
"""
import ast,copy,hashlib,json,sys
from pathlib import Path

ROOT=Path('/Users/sb/code/opensip-ai/opensip_arch')
fixture=ROOT/'docs/coop/design-corrections/foundation/check-identity.py'
source=fixture.read_text();tree=ast.parse(source)
last=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='graph_with_import').end_lineno
ns={'__file__':str(fixture),'__name__':'claude_partial_clone_rerun'};sys.argv=[str(fixture)]
exec(compile('\n'.join(source.split('\n')[:last]),str(fixture),'exec'),ns)
M,C,build,replay=ns['M'],ns['C'],ns['build'],ns['replay']

initial=build(relation='clones',universe_language='rust',has_match=False,resolved=False)
scope=next(v for d,v in initial[1].values() if d=='subject-scope')
_,universe,_=M.parse_h_frame(initial[2][scope['sourceUniverse']],'native-semantic-universe')
_,ownership,_=M.parse_h_frame(initial[2][universe['sourceUnitOwnershipId'].removeprefix('sha256:')],'native-nested')
workspace={'edition':universe['edition'],
           **{k:copy.deepcopy(v) for k,v in ownership.items() if k!='schemaVersion'}}
workspace['enumeration']='partial'

vectors=[]
for name,resolved in [('honest-unknown-control',False),('contradictory-complete-claim',True)]:
    run,objects,blobs=build(relation='clones',universe_language='rust',has_match=False,
                            resolved=resolved,workspace=workspace)
    cov=next(v for d,v in objects.values() if d=='coverage')
    payload=C.parse(blobs[cov['payloadDigest']]);seal=objects[run['evaluationSealId']][1]
    result={'id':name,'ownershipEnumeration':workspace['enumeration'],
            'coverageState':payload['entry']['coverage'],'deficiency':payload['entry']['deficiency'],
            'sealVerdict':seal['verdict'],'factCount':sum(d=='fact' for d,v in objects.values()),
            'closure':{},'store':{}}
    try:
        result['closure']={'admitted':True,'runId':M.close_run(run,objects,blobs)}
        store=M.EvidenceStore();eid='exec1_'+('a' if not resolved else 'b')*32
        result['store']={'preparedRunId':store.prepare(run,objects,blobs,eid,replay),
                         'commit':store.commit(eid)}
    except Exception as exc:
        result['closure']={'admitted':False,'cause':type(exc).__name__+':'+str(exc)}
    vectors.append(result)

honest,contradictory=vectors
print(json.dumps({
 'standing':'actual Claude coauthor re-run of a ROOT-authored construction against the CURRENT tree; '
            'design/reference evidence only, no product qualification',
 'rootEvidence':'docs/coop/design-corrections/reviews/codex-post-reset.v1/partial-clone-coverage-counterexample.v9/result.json',
 'currentFixtureSha256':hashlib.sha256(fixture.read_bytes()).hexdigest(),
 'currentModelSha256':hashlib.sha256((ROOT/'docs/coop/design-corrections/foundation/identity-model.py').read_bytes()).hexdigest(),
 'vectors':vectors,
 'honestControlStillCommits':honest['store'].get('commit')=='committed'
                             and honest['sealVerdict']=='indeterminate',
 'contradictoryClaimRefused':not contradictory['closure']['admitted'],
 'contradictoryCause':contradictory['closure'].get('cause')},indent=1))
