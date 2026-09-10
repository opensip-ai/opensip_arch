import copy,hashlib,importlib.util,json
from pathlib import Path
SNAP=Path('/tmp/opensip-design-corrections/foundation-subject.v3');F=SNAP/'docs/coop/design-corrections/foundation'
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=load('pc',F/'canonical.py');M=load('pm',F/'identity-model.py');HF=load('hf',F/'host-foundation-model.v2.py')
src=(F/'check-identity.py').read_text().split('\nfor resolved in [True,False]:')[0]
ns={'__file__':str(F/'check-identity.py')};exec(compile(src,'ci','exec'),ns);build=ns['build'];replay=ns['replay'];rekey=ns['rekey']
out=[]
def rec(i,d,o,e):out.append({'id':i,'probe':d,'observed':o,'expectation':e});print(json.dumps(out[-1],default=str)[:400])
def outcome(fn):
    try:return ('ok',fn())
    except Exception as e:return ('raise',type(e).__name__+':'+str(e)[:100])
# P2a redo: foreign run present in object set
run2,objects2,blobs2=build(resolved=False);rid2=M.close_run(run2,objects2,blobs2)
r,o,b=build();o.update(objects2);b.update(blobs2);o[rid2]=('run',run2)
proof_id=o[r['evaluationSealId']][1]['proofBundleId'];proof=copy.deepcopy(o[proof_id][1])
proof['evaluationInputRefs']=sorted(proof['evaluationInputRefs']+[{'domain':'run','digest':rid2.split(':')[1]}],key=C.canonical);rekey(o,proof_id,proof,r)
rec('P2a','proof.evaluationInputRefs names a FOREIGN committed Run present in object set; close_run',outcome(lambda:M.close_run(r,o,b)),'contract §3 proof excludes RunId / cross-Plan -> raise')
rec('P2a-replay','same via prepare with fixture replay',outcome(lambda:M.EvidenceStore().prepare(r,o,b,'x',replay))[0],'fixture replay catches')
# foreign evidence/seal via evidenceRefs on a finding
r,o,b=build();o.update(objects2);b.update(blobs2)
closure=next(k for k,(d,v) in o.items() if d=='closure');empty=hashlib.sha256(C.canonical({})).hexdigest()
fp={'schemaVersion':2,'ruleStableId':'x','detectorSemanticsMajor':1,'subjectKey':{'language':'ts','kind':'export','logicalPath':'a.ts','qualifiedName':'foo','discriminator':'0'},'relatedSubjectKeys':[]}
fpid=M.identifier('finding-fingerprint',fp);o[fpid]=('finding-fingerprint',fp)
finding={'schemaVersion':2,'fingerprint':fpid,'ruleClosure':closure,'subjectId':'foo','messageCode':'X','parameterDigest':empty,'severity':'error','evidenceRefs':[{'domain':'evaluation-seal','digest':run2['evaluationSealId'].split(':')[1]}]}
fnid=M.identifier('finding',finding);o[fnid]=('finding',finding)
proof_id=o[r['evaluationSealId']][1]['proofBundleId'];proof=copy.deepcopy(o[proof_id][1]);proof['findingIds']=[fnid];rekey(o,proof_id,proof,r)
ev_id=r['evidenceId'];ev=copy.deepcopy(o[ev_id][1]);ev['findingIds']=[fnid];rekey(o,ev_id,ev,r)
rec('P2a2','finding.evidenceRefs names a FOREIGN evaluation-seal (different Plan); close_run',outcome(lambda:M.close_run(r,o,b))[0],'raise')
# P2g redo
r,o,b=build()
stages=[{'ordinal':i,'stageSpecDigest':empty,'requires':([] if i<11 else [9,10]),'outputDomains':['fact']} for i in range(12)]
rec('P2g','stage ordinal 11 requires=[9,10] numeric order',outcome(lambda:M.identifier('execution-plan',{'schemaVersion':2,'planId':r['planId'],'stages':stages}))[1],'ORDER_OR_DUPLICATE since b"10"<b"9"')
stages[11]['requires']=[10,9]
rec('P2g2','stage ordinal 11 requires=[10,9] byte order',outcome(lambda:M.identifier('execution-plan',{'schemaVersion':2,'planId':r['planId'],'stages':stages}))[0],'ok')
# depth boundary: canonical.parse vs host-foundation strict
def nested(n):return ('{"x":'*(n-1)+'{}'+'}'*(n-1)).encode()
for n in [32,33,34]:
    rec('P1d-'+str(n),'nested object depth %d: canonical.parse vs host-foundation strict'%n,{'canonical':outcome(lambda:C.parse(nested(n)))[0],'strict':outcome(lambda:HF.strict(nested(n)))[0]},'both agree at the contract bound of 32')
# schema Text maxLength counted in code points not bytes
rec('P1i','Text maxLength 4096 code points vs bytes: 4096 x U+10000 (16 KiB) accepted?',outcome(lambda:C.validate({'type':'string','maxLength':4096},'\U00010000'*4096))[0],'ok => bound is code points (document)')
# semantic-grant scope/project joins not checked even with valid payloads
r,o,b=build();pid=r['planId'];plan=copy.deepcopy(o[pid][1])
grant={'schemaVersion':2,'projectId':'prj1-'+'b'*64,'principals':[],'analysisOperations':['read-source'],'scopeDigest':'f'*64}
graw=C.canonical(grant);gd=hashlib.sha256(graw).hexdigest();b[gd]=graw;plan['semanticGrantDigest']=gd;rekey(o,pid,plan,r)
rec('P2j','schema-valid semantic-grant with WRONG projectId and scopeDigest; close_run',outcome(lambda:M.close_run(r,o,b))[0],'contract §3 grant binds ProjectId+scope -> raise')
Path('/tmp/opensip-design-corrections/claude-probes-v3b.json').write_text(json.dumps(out,indent=1,default=str)+'\n')
