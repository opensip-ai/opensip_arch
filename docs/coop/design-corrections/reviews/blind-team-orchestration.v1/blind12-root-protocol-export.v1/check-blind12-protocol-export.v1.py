from pathlib import Path
import importlib.util,json,hashlib,shutil
B=Path('/tmp/opensip-design-corrections');F=B/'candidate-subject.v24/docs/coop/design-corrections/foundation/identity-model.v3.py'
s=importlib.util.spec_from_file_location('root_protocol_owner',F);M=importlib.util.module_from_spec(s);s.loader.exec_module(M);N=M.native_admission()
o=B/'blind12-root-protocol-export.v1';o.mkdir();src=B/'consumer-b.v12-team-corrections.v2/output/traces';docs={n:json.loads((src/(n+'.json')).read_text()) for n in ['complete','unavailable','cancel','fault','terminal']}
for n in docs:shutil.copy2(src/(n+'.json'),o/(n+'.json'))
cases=[(n,docs[n]) for n in ['complete','unavailable','cancel','fault']]+[('postTerminal',docs['terminal']['postTerminal']),('missingIdentity',docs['fault']['openUniverseWithoutIdentity']['trace'])];rows=[]
for name,case in cases:
 events=[r['event'] for r in case['trace']];prefixes=[]
 for i,row in enumerate(case['trace'],1):
  got=N.protocol3_run(events[:i],stage_count=case['final']['stageCount']);expected={'finalPhase':row['phaseAfter'],'terminalKind':row['terminalKind'],'sourceBytesSent':row['sourceBytesSent'],'identityNegotiated':row['identityNegotiated'],'trace':[r['traceId'] for r in case['trace'][:i]]};ok=all(got[k]==v for k,v in expected.items());prefixes.append({'length':i,'passed':ok,'traceId':got['trace'][-1]})
 last=N.protocol3_run(events,stage_count=case['final']['stageCount']);ok=all(r['passed'] for r in prefixes) and last['stagesCompleted']==case['final']['stagesCompleted'];rows.append({'name':name,'passed':ok,'prefixes':prefixes,'final':last})
r={'standing':'Actual frozen protocol3 state interpreter applied to every prefix of six exact exported standalone traces. Frame payload schema/VFS/native-host/OS enforcement are outside this trace boundary. No root outputs supplied to blind team.','ownerSha256':hashlib.sha256(F.read_bytes()).hexdigest(),'nativeOwnerSha256':hashlib.sha256(Path(N.__file__).read_bytes()).hexdigest(),'checks':rows,'passed':all(x['passed'] for x in rows)}
(o/'report.json').write_text(json.dumps(r,indent=2)+'\n');shutil.copy2(Path(__file__),o/Path(__file__).name);print(json.dumps({'traces':len(rows),'prefixes':sum(len(x['prefixes']) for x in rows),'passed':r['passed']}));assert r['passed']
