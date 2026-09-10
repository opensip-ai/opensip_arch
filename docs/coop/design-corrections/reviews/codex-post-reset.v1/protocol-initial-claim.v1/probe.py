"""Root bounded extraction of actual proposed protocol3_run to assess a coauthor claim.
No host enforcement claim: exact function AST executed with its captured normative constants.
"""
from pathlib import Path
import ast,copy,json,hashlib
b=Path('/tmp/opensip-design-corrections');src=b/'v19-protocol-initial-coauthor.v1';out=b/'codex-post-reset.v1/protocol-initial-claim.v1';out.mkdir(exist_ok=False)
p=src/'native_evidence_model.v2.py';tree=ast.parse(p.read_text());fn=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='protocol3_run');tokens=next(ast.literal_eval(x.value) for x in tree.body if isinstance(x,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='IDENTITY_TOKENS' for t in x.targets));d=json.loads((src/'protocol3-transitions.v1.json').read_text());ns={'PROTOCOL3_RULES':d['rules'],'_PRE_COMPLETE':d['wildcards']['*PRE_COMPLETE']['phases'],'_PROCESS_FAULTS':set(d['wildcards']['*PROCESS_FAULT']['frames']),'_SOURCE_FRAMES':{f for row in d['stateUpdates'] for f in row.get('onFrames',[])},'IDENTITY_TOKENS':tokens}; funcs=[]
for initial in [False,True]:
 f=copy.deepcopy(fn);assign=next(x for x in f.body if isinstance(x,ast.Assign) and getattr(x.targets[0],'id',None)=='state');idx=next(i for i,k in enumerate(assign.value.keys) if k.value=='identityNegotiated');assert assign.value.values[idx].value is False;assign.value.values[idx]=ast.Constant(initial);module=ast.fix_missing_locations(ast.Module(body=[f],type_ignores=[]));local=dict(ns);exec(compile(module,str(p),'exec'),local);funcs.append(local['protocol3_run'])
traces={'skip-ack':[{'frame':'Hello'},{'frame':'OpenUniverse'}],'missing-tokens':[{'frame':'Hello'},{'frame':'HelloAck','capabilities':[]},{'frame':'OpenUniverse'}],'valid-tokens':[{'frame':'Hello'},{'frame':'HelloAck','capabilities':tokens},{'frame':'OpenUniverse'}]};rows={name:{str(v):fn(events) for v,fn in zip([False,True],funcs)} for name,events in traces.items()}
for name in ['skip-ack','missing-tokens']:
 assert all(r['finalPhase']=='FAULT' and r['sourceBytesSent'] is False for r in rows[name].values())
assert rows['missing-tokens']['False']==rows['missing-tokens']['True']
assert rows['valid-tokens']['False']==rows['valid-tokens']['True']
result={'standing':__doc__,'modelSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'traces':traces,'results':rows,'conclusion':'The initial-true change alone does NOT permit OpenUniverse before negotiation. Phase gating requires HelloAck, which overwrites identityNegotiated before READY_OPEN_UNIVERSE. Publishing initialState remains useful for complete deterministic state reconstruction; coauthor security-bypass example is not supported by the actual transition function.','publicationCorrectionStillAccepted':True,'hostQualification':False};(out/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
