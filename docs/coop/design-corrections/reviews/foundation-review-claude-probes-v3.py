"""Independent Claude probes against frozen foundation subject v3. Reads snapshot only; writes /tmp only."""
import copy,hashlib,importlib.util,json,sys,traceback
from pathlib import Path
SNAP=Path('/tmp/opensip-design-corrections/foundation-subject.v3')
F=SNAP/'docs/coop/design-corrections/foundation'
def load(name,path):
    s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=load('pc',F/'canonical.py');M=load('pm',F/'identity-model.py');CFG=load('pcfg',F/'product-configuration-model.py')
G=load('pg',F/'g13-validator.v5.py');Q=load('pq',F/'product-quality-validator.py')
# reuse check-identity builder without running its main body: exec only the needed defs
src=(F/'check-identity.py').read_text().split('\nfor resolved in [True,False]:')[0]
ns={'__file__':str(F/'check-identity.py')};exec(compile(src,'check-identity-defs','exec'),ns);build=ns['build'];replay=ns['replay'];rekey=ns['rekey']
out=[]
def rec(pid,desc,observed,expectation):
    out.append({'id':pid,'probe':desc,'observed':observed,'expectation':expectation})
def outcome(fn):
    try:return ('ok',fn())
    except Exception as e:return ('raise',type(e).__name__+':'+str(e)[:120])

# ---- P1 canonical edge cases
rec('P1a','lone surrogate via JSON escape',outcome(lambda:C.parse(b'"\\udc00"')),'raise')
rec('P1b','escape of U+007F and U+2028',C.canonical({'s':'\x7f '}).decode('utf-8','backslashreplace'),'unescaped per contract (only 00-1F escaped)')
deep=lambda n:('['*n+']'*n).encode()
rec('P1c','depth 32 arrays',outcome(lambda:C.parse(deep(32))),'ok')
rec('P1d','depth 33 arrays',outcome(lambda:C.parse(deep(33))),'raise')
rec('P1e','1E400 / 01 / BOM / leading +',[outcome(lambda r=r:C.parse(r))[0] for r in [b'1E400',b'01',b'\xef\xbb\xbf1',b'+1']],'all raise')
rec('P1f','bool in integer schema / 1 in const true',[outcome(lambda:C.validate({'type':'integer'},True))[0],outcome(lambda:C.validate({'const':True},1))[0]],'both raise')
rec('P1g','nested 1.0 in list rejected at parse',outcome(lambda:C.parse(b'[1.0]'))[0],'raise')
rec('P1h','key order BMP vs supplementary vs surrogate-range-adjacent',C.canonical({'￿':0,'\U00010000':1,'':2}).decode(),'\\ue000 < \\uffff < U+10000 (UTF-8 byte order)')

# ---- P2 identity closure probes
run,objects,blobs=build()
ok_id=M.close_run(run,objects,blobs)
rec('P2-base','baseline fixture closes',ok_id[:12],'run2:...')

# P2a: foreign Run referenced from proof.evaluationInputRefs (cross-Plan / RunId inside proof)
run2,objects2,blobs2=build(resolved=False)  # a different plan/run (different coverage payload -> different ids)
rid2=M.close_run(run2,objects2,blobs2)
assert rid2!=ok_id
r,o,b=build();o.update(objects2);b.update(blobs2)
proof_id=o[r['evaluationSealId']][1]['proofBundleId'];proof=copy.deepcopy(o[proof_id][1])
proof['evaluationInputRefs']=sorted(proof['evaluationInputRefs']+[{'domain':'run','digest':rid2.split(':')[1]}],key=C.canonical)
rekey(o,proof_id,proof,r)
rec('P2a','proof.evaluationInputRefs names a FOREIGN Run (run2 domain) present in object set; close_run',outcome(lambda:M.close_run(r,o,b)),'contract §3: proof does not include RunId; cross-Plan refs rejected -> expect raise')
rec('P2a-replay','same object set through EvidenceStore.prepare with fixture replay',outcome(lambda:M.EvidenceStore().prepare(r,o,b,'x',replay)),'replay catches by proof inequality (fixture-level)')

# P2b: finding.evidenceRefs pointing to a fact bound to a FOREIGN snapshot
r,o,b=build();o.update(objects2);b.update(blobs2)
foreign_snapshot=run2['snapshotId']
# create a foreign fact (valid on its own) bound to snapshot of run2
empty=hashlib.sha256(C.canonical({})).hexdigest()
closure=next(k for k,(d,v) in o.items() if d=='closure')
src_blob=next(k for k,v in b.items() if v.startswith(b'export const'))
ffact={'schemaVersion':2,'snapshotId':foreign_snapshot,'relation':'references','resolution':'resolved-binding','sourceUniverse':empty,'targetUniverse':empty,'producerClosure':closure,'payloadSchemaDigest':empty,'payloadDigest':hashlib.sha256(C.canonical({'target':'foo'})).hexdigest(),'anchors':[],'confidenceMillionths':1}
b[ffact['payloadDigest']]=C.canonical({'target':'foo'})
fid=M.identifier('fact',ffact);o[fid]=('fact',ffact)
fp={'schemaVersion':2,'ruleStableId':'no-consumer','detectorSemanticsMajor':1,'subjectKey':{'language':'ts','kind':'export','logicalPath':'a.ts','qualifiedName':'foo','discriminator':'0'},'relatedSubjectKeys':[]}
fpid=M.identifier('finding-fingerprint',fp);o[fpid]=('finding-fingerprint',fp)
finding={'schemaVersion':2,'fingerprint':fpid,'ruleClosure':closure,'subjectId':'foo','messageCode':'X','parameterDigest':empty,'severity':'error','evidenceRefs':[{'domain':'fact','digest':fid.split(':')[1]}]}
fnid=M.identifier('finding',finding);o[fnid]=('finding',finding)
proof_id=o[r['evaluationSealId']][1]['proofBundleId'];proof=copy.deepcopy(o[proof_id][1]);proof['findingIds']=[fnid];rekey(o,proof_id,proof,r)
ev_id=r['evidenceId'];ev=copy.deepcopy(o[ev_id][1]);ev['findingIds']=[fnid];rekey(o,ev_id,ev,r)
rec('P2b','finding.evidenceRefs -> fact bound to FOREIGN snapshot; findingIds consistent in proof+evidence; close_run',outcome(lambda:M.close_run(r,o,b)),'contract: cross-source refs rejected -> expect raise')

# P2c: auxiliary typed payload admission: scopeDigest blob replaced by arbitrary non-JSON bytes
r,o,b=build();garbage=b'\x00not-json';gd=hashlib.sha256(garbage).hexdigest();b[gd]=garbage
sid=r['snapshotId'];snap=copy.deepcopy(o[sid][1]);snap['scopeDigest']=gd;rekey(o,sid,snap,r)
pid=r['planId'];plan=copy.deepcopy(o[pid][1]);plan['scopeDigest']=gd;plan['semanticGrantDigest']=gd;plan['analysisSpecDigest']=plan['analysisSpecDigest'];rekey(o,pid,plan,r)
rec('P2c','scopeDigest/semanticGrantDigest blobs are non-JSON bytes; close_run',outcome(lambda:M.close_run(r,o,b)),'contract §3: payloads validated with exact admitted schema -> expect raise')
# does the fixture's own auxiliary payload {} satisfy its declared schema?
sch=copy.deepcopy(M.SCHEMA)
for dom in ['scope-descriptor','analysis-spec','semantic-grant','predicate-witness']:
    s2=copy.deepcopy(sch);s2['$ref']='#/$defs/'+dom
    rec('P2c-'+dom,'fixture auxiliary payload {} validates against declared '+dom+' schema',outcome(lambda s2=s2:C.validate(s2,{}))[0],'raise => fixture payload is schema-invalid')
rec('P2c-identifier','identifier() reachable for scope-descriptor',outcome(lambda:M.identifier('scope-descriptor',{}))[1],'IDENTITY_DOMAIN => auxiliary schemas unreachable via identifier()')

# P2d: predicateProofs.inputRefs and scopeIds not covered by evaluationInputRefs / view scopes
r,o,b=build();proof_id=o[r['evaluationSealId']][1]['proofBundleId'];proof=copy.deepcopy(o[proof_id][1]);proof['evaluationInputRefs']=[];rekey(o,proof_id,proof,r)
rec('P2d','proof.evaluationInputRefs emptied while predicateProofs.inputRefs still name the view; close_run',outcome(lambda:M.close_run(r,o,b))[0],'contract §4: all consumed data listed -> expect raise')

# P2e: extra coverage in evidence not attached to any view (extra authoritative root)
r,o,b=build();scope=next(k for k,(d,v) in o.items() if d=='subject-scope')
cov={'schemaVersion':2,'scopeId':scope,'payloadSchemaDigest':empty,'payloadDigest':hashlib.sha256(C.canonical({'x':1})).hexdigest()};b[cov['payloadDigest']]=C.canonical({'x':1})
cid=M.identifier('coverage',cov);o[cid]=('coverage',cov)
ev_id=r['evidenceId'];ev=copy.deepcopy(o[ev_id][1]);ev['coverageIds']=sorted(ev['coverageIds']+[cid]);rekey(o,ev_id,ev,r)
rec('P2e','evidence.coverageIds carries a coverage no view references; close_run',outcome(lambda:M.close_run(r,o,b))[0],'contract: extra authoritative roots rejected -> expect raise')

# P2f: witness blob is garbage bytes with matching digest
r,o,b=build();proof_id=o[r['evaluationSealId']][1]['proofBundleId'];proof=copy.deepcopy(o[proof_id][1]);b[gd]=garbage;proof['predicateProofs'][0]['witnessDigest']=gd;rekey(o,proof_id,proof,r)
rec('P2f','witnessDigest -> non-JSON blob; close_run',outcome(lambda:M.close_run(r,o,b))[0],'closed witness record admission -> expect raise')
rec('P2f-replay','same through prepare with fixture replay',outcome(lambda:M.EvidenceStore().prepare(r,o,b,'x',replay))[0],'raise (fixture replay recomputes digest)')

# P2g: stage requires ordering by canonical bytes
r,o,b=build();ex=next(k for k,(d,v) in o.items() if d=='execution-plan')
stages=[{'ordinal':i,'stageSpecDigest':empty,'requires':([] if i<10 else [9,10]) ,'outputDomains':['fact']} for i in range(11)]
rec('P2g','execution-plan stage requires=[9,10] (numeric order)',outcome(lambda:M.identifier('execution-plan',{'schemaVersion':2,'planId':r['planId'],'stages':stages}))[1][:40],'contract sorts by canonical item bytes: b"10"<b"9" -> rejected as ORDER_OR_DUPLICATE (document)')

# P2h: EvidenceStore recovery surface
st=M.EvidenceStore();r,o,b=build();rid=st.prepare(r,o,b,'e1',replay);res=st.commit('e1','after-ledger-before-ack')
rec('P2h','after durability-undetermined: attempts record and any recovery API',{'commitReturn':res,'attempts':st.attempts,'hasRecover':hasattr(st,'recover')},'contract §5 recovery returns committed/failed read-only; no API modeled')
rec('P2i','availability / commit-receipt records ever instantiated by reference',{'availabilityType':type(st.availability[rid]).__name__,'receipt':st.receipts[0]},'schema records exist but reference uses bare strings/tuples')

# ---- P3 configuration
registry={'profiles':['default'],'capabilities':['typescript.imports'],'packs':['architecture']}
default=C.canonical({'schemaVersion':2,'analysis':{'profileId':'default','capabilities':['typescript.imports'],'budget':{'unit':'work-units','limit':10}},'components':{'pins':[],'holds':[],'allowedScopes':['project','global']},'discovery':{'entryPoints':[],'workspaceRoots':[],'ignorePaths':[]},'policy':{'packIds':['architecture'],'waiverIds':[]},'evidence':{'importIds':[]}})
rec('P3a','unregistered waiverId accepted?',outcome(lambda:CFG.resolve({'defaults':default,'project':b'{"schemaVersion":2,"policy":{"waiverIds":["ghost.waiver"]}}'},registry))[0],'contract §1.1 registered pack/waiver IDs -> expect raise')
rec('P3b','unregistered import2 id accepted? (disclosed as native/workflow join)',outcome(lambda:CFG.resolve({'defaults':default,'project':C.canonical({'schemaVersion':2,'evidence':{'importIds':['import2:'+'a'*64]}})},registry))[0],'accepted; join named')
rec('P3c','absent profileId error label',outcome(lambda:CFG.resolve({'defaults':C.canonical({'schemaVersion':2})},registry))[1],'label says UNREGISTERED for absent')
rec('P3d','valid local consumed when ci=False; digest changes',CFG.resolve({'defaults':default,'local':b'{"schemaVersion":2,"analysis":{"budget":{"unit":"work-units","limit":11}}}'},registry)['resolvedConfigDigest']!=CFG.resolve({'defaults':default},registry)['resolvedConfigDigest'],'True')
rec('P3e','path forms',[outcome(lambda p=p:CFG.resolve({'defaults':default,'project':C.canonical({'schemaVersion':2,'discovery':{'ignorePaths':[p]}})},registry))[0] for p in ['src/','./a','a//b','a\\b','C:x','..']],'first four+last raise; C:x ok')

# ---- P4 g13 v5: missing fixture in a cell
import subprocess,tempfile
sample=G.OLD.reference();sample.update(schemaMajor=2,harnessDigest='d'*64)
rows={r['id']:r for r in G.M['rows']}
for cell in sample['cells']:
    for f in cell['fixtureResults']:
        atoms=G.oracle(rows[cell['cellId']],f['fixtureId']);f.update(actualObservations=atoms,expectedCount=len(atoms),actualCount=len(atoms))
trusted={p['platform']:{k:p['runner'][k] for k in G.OLD.HARDWARE} for p in sample['performance']}
with tempfile.TemporaryDirectory() as td:
    p=Path(td);subprocess.run(['openssl','genpkey','-algorithm','ED25519','-out',str(p/'key')],check=True,capture_output=True)
    public=subprocess.check_output(['openssl','pkey','-in',str(p/'key'),'-pubout']).decode()
    ctx={k:sample[k] for k in ['hostDigest','providerClosureDigest','harnessDigest','matrixDigest','corpusDigest']};ctx.update(producerPublicKeyPem=public,baseline=None,trustedRunners=trusted)
    def sign(raw):
        (p/'m').write_bytes(G.signature_message(raw,ctx));return subprocess.check_output(['openssl','pkeyutl','-sign','-inkey',str(p/'key'),'-rawin','-in',str(p/'m')])
    def acc(v):
        raw=C.canonical(v);return G.admit(raw,sign(raw),ctx)
    rec('P4-base','authenticated sample admitted',acc(sample),'True')
    x=copy.deepcopy(sample);x['cells'][1]['fixtureResults'].pop();rec('P4a','cell omits one required fixture',acc(x),'False')
    x=copy.deepcopy(sample);x['cells'][1]['fixtureResults'].append(copy.deepcopy(x['cells'][1]['fixtureResults'][0]));rec('P4b','duplicate fixtureId in a cell',acc(x),'False')
    # self-consistent honest failing report: forged observation + recomputed counters + FAIL flags
    x=copy.deepcopy(sample);f=x['cells'][0]['fixtureResults'][0];exp=G.oracle(rows[x['cells'][0]['cellId']],f['fixtureId']);act=copy.deepcopy(exp);act[0]['value']='forged';act=sorted(act,key=C.canonical)
    ek=[C.canonical(v) for v in exp];ak=[C.canonical(v) for v in act]
    f.update(actualObservations=act,expectedCount=len(exp),actualCount=len(act),missingCount=len(set(ek)-set(ak)),extraCount=len(set(ak)-set(ek)),duplicateCount=0,expectationMatched=False,differenceArtifactDigest=C.identity('quality-difference',{'expected':exp,'actual':act}))
    x['cells'][0]['result']='FAIL';x['result']='FAIL';rec('P4c','honest self-consistent FAIL report admitted (expected: admission != promotion)',acc(x),'True')
    x2=copy.deepcopy(x);x2['cells'][0]['result']='PASS';x2['result']='PASS';rec('P4d','same with PASS flags asserted over failing counters',acc(x2),'False')
    # v3 product report: baseline None -> absolute-only pass?
    qctx={k:hashlib.sha256(k.encode()).hexdigest() for k in ['hostDigest','providerClosureDigest','harnessDigest']}
    qctx.update(producerPublicKeyPem=public,runnerId='r',profileId='p',qualificationRequestId='req1_'+'1'*32,expectedCells={})
    for k in ['matrix','corpus','environment']:
        qctx[k+'Bytes']=C.canonical({'k':k});qctx[k+'Digest']=hashlib.sha256(qctx[k+'Bytes']).hexdigest()
    atom={'kind':'coverage','subject':'f','value':'resolved'};cid='references/ts-tsconfig/macos-aarch64/p/f'
    qctx['expectedCells'][cid]={'observations':[atom],'exitStatus':0,'absoluteNanos':10**9,'absoluteRssBytes':10**9,'baselineMedianNanos':None,'baselinePeakRssBytes':None}
    rep={k:qctx[k] for k in ['hostDigest','providerClosureDigest','harnessDigest','matrixDigest','corpusDigest','runnerId','profileId','environmentDigest','qualificationRequestId']}
    rep.update(schemaMajor=3,cells=[{'cellId':cid,'warmupRuns':3,'elapsedNanos':[5]*7,'peakRssBytes':[5]*7,'observations':[atom],'exitStatus':0}])
    def qsign(raw):
        (p/'m').write_bytes(G.signature_message(raw,qctx));return subprocess.check_output(['openssl','pkeyutl','-sign','-inkey',str(p/'key'),'-rawin','-in',str(p/'m')])
    raw=C.canonical(rep);rec('P5a','v3 report with baselineMedianNanos=None: performance result',Q.admit(raw,qsign(raw),qctx),'contract §3: new cell needs reviewed initial baseline; absence not automatic pass')
    qctx2=copy.deepcopy(qctx);qctx2['expectedCells'][cid].pop('absoluteNanos');rec('P5b','absoluteNanos absent from oracle',Q.admit(raw,qsign(raw),qctx2)['admitted'],'False (invalid) - absence not a pass')

Path('/tmp/opensip-design-corrections/claude-probes-v3.json').write_text(json.dumps(out,indent=1,default=str)+'\n')
for o_ in out:print(json.dumps(o_,default=str)[:400])
