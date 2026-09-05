#!/usr/bin/env python3
"""Proposed SDK courier reference checks using actual local temporary files."""
import argparse,copy,hashlib,importlib.util,json,os,stat,tempfile
from pathlib import Path
P=Path(__file__).resolve().parent
def module(name,path):
 s=importlib.util.spec_from_file_location(name,P/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
M=module('sdk_courier','broker-sdk-courier.model.v1.py');SECJOIN=module('sdk_security_join','broker-host-security-join.v1.py');C=module('courier_control','control-completion.check.v5.py')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--report',default=str(P/'broker-sdk-courier.report.v1.json'));args=ap.parse_args();checks=[];traces=[]
 def check(id,value):checks.append({'id':id,'passed':bool(value)})
 def raised(fn):
  try:return {'returned':fn()}
  except (M.CourierFailure,M.B.StartupFailure) as e:return {'error':str(e)}
 for effect in ['HE-1','HE-2']:
  variants=['positive','refused','failed','indeterminate','wrong-request','wrong-commit','outcome-order','bad-ref','digest-mismatch','wrong-handle','foreign-handle','unknown-result-member','fractional-decision','invalid-refusal','security-context-missing','security-broker-scope-empty','security-underlying-revoked','security-binding-empty','security-binding-partial','security-binding-unknown','security-members-object','security-members-duplicate','security-connection-malformed','security-journal-malformed','string-request','boolean-request']
  variants+=['receipt-only','host-narrow-bytecap','reversible-write','stage-mutated-after-read','single-use','caller-mutable-array','existing-stage'] if effect=='HE-1' else ['security-members-missing','security-members-empty','security-snapshot-missing','security-traversal','missing','symlink','hardlink','directory','fifo','wrong-size','replayed-result','root-mode-changed','held-root-after-rename','empty-result','aggregate-over-limit']
  for variant in variants:
   with tempfile.TemporaryDirectory(prefix='opensip-sdk-courier-') as td:
    root=Path(td).resolve()
    for part in ['operational','projects','11111111-1111-4111-8111-111111111111','spawns','22222222-2222-4222-8222-222222222222']:
     root=root/part;root.mkdir(mode=0o700)
    (root/'stage').mkdir(mode=0o700);state=Path(td)/'host-state';state.mkdir(mode=0o700)
    body={'effectClass':effect,'authorizationRef':'ah:'+'1'*32,'operationRef':'op-'+'2'*32,'commitClass':'IRREVERSIBLE' if effect=='HE-1' and variant!='reversible-write' else 'REVERSIBLE'}
    descriptor={'bootstrapVersion':1,'handles':[body],'resultScratchRoot':str(root)};env={**M.B.FIXED,M.B.KEY:M.B.encode(descriptor)};events=[];hostfd=os.open(root,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW);publisher=M.ReferenceResultPublisher(hostfd);counter=[0];committed=[];security_decisions=[];caller=bytearray(b'caller original bytes')
    source=b'' if variant=='empty-result' else b'export const fixture = 1;\n';sealed={'snapshotDigest':'a'*64,'members':{'src/member.ts':source}}
    def send(seq,request):
     counter[0]+=1
     assert request=={k:body[k] for k in ['effectClass','authorizationRef','operationRef']}
     if variant=='invalid-refusal':return {'type':'refusal','body':{'family':'RF-6','decisionClass':'PR-99'}}
     if variant=='refused':return {'type':'refusal','body':{'family':'RF-6','decisionClass':'PR-2'}}
     ctx=SECJOIN.context(request,sealed,5 if variant=='host-narrow-bytecap' else M.MAX_RESULT)
     entry=ctx['connectionMap'][request['authorizationRef']]
     if variant=='security-context-missing':ctx.pop('currentBinding')
     if variant=='security-binding-empty':ctx['currentBinding']={}
     if variant=='security-binding-partial':ctx['currentBinding'].pop('manifestDigest')
     if variant=='security-binding-unknown':ctx['currentBinding']['callerOverride']='forged'
     if variant=='security-members-object':ctx['snapshotMembers']=[{}]
     if variant=='security-members-duplicate':ctx['snapshotMembers']=['src/member.ts','src/member.ts']
     if variant=='security-connection-malformed':ctx['connectionMap'][request['authorizationRef']]={}
     if variant=='security-journal-malformed':ctx['journalState'][entry['underlyingLocator']]={}
     if variant=='security-broker-scope-empty':ctx['journalState'][entry['brokerLocator']]['scope']={}
     if variant=='security-underlying-revoked':ctx['journalState'][entry['underlyingLocator']]['status']='REVOKED'
     if variant=='security-members-missing':ctx.pop('snapshotMembers')
     if variant=='security-members-empty':ctx['snapshotMembers']=[]
     if variant=='security-snapshot-missing':ctx['journalState'][entry['underlyingLocator']]['scope'].pop('snapshotDigest')
     if variant=='security-traversal':entry['target']['memberPath']='src/../private'
     denied=SECJOIN.evaluate(request,ctx);security_decisions.append({'context':ctx,'decision':denied})
     if denied is not None:return {'type':'refusal','body':{k:denied[k] for k in ['family','decisionClass']}}
     events.append('security-request-admitted:' + SECJOIN.RECEIPT['securityLibrary'])
     # These are reference journal ordering observations, not SQLite/witness
     # durability proof. Physical file operations below are actually executed.
     outcome='FAILED' if variant=='failed' else 'INDETERMINATE' if variant=='indeterminate' else 'COMPLETED'
     response={'type':'effectResult','body':{'requestSeq':seq,'decisionSeq':40+counter[0]*2,'outcomeSeq':41+counter[0]*2,'commitClass':body['commitClass'],'effectOutcome':outcome}}
     if outcome!='COMPLETED':
      events.append('injected-host-outcome:'+outcome);return response
     intent='ICI' if body['commitClass']=='IRREVERSIBLE' else 'RCI';done='ICO' if intent=='ICI' else 'RCO'
     if effect=='HE-1':
      if variant=='caller-mutable-array':caller[:]=b'changed after SDK copy'
      fd=os.open('stage/'+body['authorizationRef'][3:]+'.bin',os.O_RDONLY|os.O_NOFOLLOW|os.O_CLOEXEC|os.O_NONBLOCK,dir_fd=hostfd)
      try:
       st=os.fstat(fd);admission=SECJOIN.SEC.stage_file_admission({'type':'regular' if stat.S_ISREG(st.st_mode) else 'other','nlink':st.st_nlink,'uid':st.st_uid,'size':st.st_size},os.geteuid(),entry['target']['byteCap'])
       if admission is not None:
        events.append('stage-refused-before-buffer-allocation:'+admission);response['body']['effectOutcome']='FAILED';return response
       data=M.file_read(fd,st.st_size)
      finally:os.close(fd)
      if variant=='stage-mutated-after-read':(root/'stage'/('1'*32+'.bin')).write_bytes(b'attacker mutation after immutable host read')
      events.append('RA');events.append(intent);temp=state/'pending';fd=os.open(temp,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
      try:M.exact_write(fd,data);os.fsync(fd)
      finally:os.close(fd)
      os.replace(temp,state/'committed');events.append('physical-commit');committed.append((state/'committed').read_bytes())
     else:
      # Exact sealed member lookup; no repository filesystem path is consulted.
      target={'snapshotDigest':'a'*64,'memberPath':'src/member.ts'};assert target['snapshotDigest']==sealed['snapshotDigest'] and target['memberPath'] in sealed['members'];data=sealed['members'][target['memberPath']]
      events.append('RA');events.append(intent)
     rid=f'{counter[0]:032x}';ref='rr:'+rid+':'+M.sha(data)+':'+str(len(data))
     if effect=='HE-2':
      name=rid+'.bin';temp=rid+'.pending'
      if variant not in ['security-members-missing','security-members-empty','security-snapshot-missing','security-traversal','missing','symlink','hardlink','directory','fifo','replayed-result']:
       published=publisher.publish(rid,data if variant!='wrong-size' else data+b'x');assert published['effectOutcome']=='COMPLETED'
      elif variant=='symlink':os.symlink('/dev/null',name,dir_fd=hostfd)
      elif variant=='hardlink':
       (root/'backing').write_bytes(data);os.link(root/'backing',root/name)
      elif variant=='directory':os.mkdir(name,dir_fd=hostfd)
      elif variant=='fifo':os.mkfifo(root/name)
      elif variant=='replayed-result':
       if counter[0]==1:(root/name).write_bytes(data)
       else:ref='rr:'+('0'*31+'1')+':'+M.sha(data)+':'+str(len(data))
      events.append('result-publication')
     events.append(done)
     if effect=='HE-1':os.unlink('stage/'+body['authorizationRef'][3:]+'.bin',dir_fd=hostfd);events.append('UNLINK-STAGE')
     response['body']['resultRef']=ref;events.append('effectResult')
     if variant=='wrong-request':response['body']['requestSeq']=seq+1
     if variant=='string-request':response['body']['requestSeq']=str(seq)
     if variant=='boolean-request':response['body']['requestSeq']=True
     if variant=='wrong-commit':response['body']['commitClass']='REVERSIBLE' if body['commitClass']=='IRREVERSIBLE' else 'IRREVERSIBLE'
     if variant=='outcome-order':response['body']['outcomeSeq']=response['body']['decisionSeq']
     if variant=='bad-ref':response['body']['resultRef']='../outside'
     if variant=='digest-mismatch':response['body']['resultRef']='rr:'+rid+':'+'0'*64+':'+str(len(data))
     if variant=='unknown-result-member':response['body']['providerOverride']='forged'
     if variant=='fractional-decision':response['body']['decisionSeq']=1.5
     if variant=='root-mode-changed':os.chmod(root,0o755)
     if variant=='held-root-after-rename':
      root.rename(root.with_name('renamed'));root.mkdir(mode=0o700);(root/name).write_bytes(b'forged replacement path')
     # Actual existing closed body schema admission; SDK has separate pending
     # request and commit-class validation above these structural checks.
     wire={'type':'effectResult','seq':counter[0],'controlMajor':1,'body':response['body']}
     if variant not in ['unknown-result-member','fractional-decision','string-request','boolean-request']:assert C.VALIDATORS['effectResult'].is_valid(wire)
     return response
    sdk=M.BrokerSDK(env,send);handle=(sdk.hostStateWriteHandles if effect=='HE-1' else sdk.projectReadHandles)[0]
    if variant=='existing-stage':(root/'stage'/('1'*32+'.bin')).write_bytes(b'old bytes')
    if variant=='aggregate-over-limit':sdk._received=M.MAX_SPAWN-len(source)+1
    if variant=='wrong-handle':handle=M.ReadHandle() if effect=='HE-1' else M.WriteHandle()
    if variant=='foreign-handle':handle=M.WriteHandle() if effect=='HE-1' else M.ReadHandle()
    request=lambda:sdk.writeHostState(handle,caller) if effect=='HE-1' else sdk.readProject(handle)
    actual=raised(request)
    if variant in ['single-use','replayed-result']:actual=raised(request)
    if variant in ['positive','receipt-only','reversible-write','stage-mutated-after-read','caller-mutable-array','held-root-after-rename','empty-result']:
     expected={'kind':'COMPLETED','commitClass':body['commitClass']} if effect=='HE-1' else {'kind':'COMPLETED','bytes':source};check(effect+'/'+variant,actual=={'returned':expected})
    elif variant.startswith('security-'):
     expected='PR-5' if variant=='security-underlying-revoked' else 'PR-4';check(effect+'/'+variant,actual=={'returned':{'kind':'REFUSED','decisionClass':expected}} and 'RA' not in events and 'result-open' not in sdk.trace)
    elif variant=='host-narrow-bytecap':check(effect+'/'+variant,actual=={'returned':{'kind':'FAILED','commitClass':body['commitClass']}} and committed==[] and any(e.startswith('stage-refused-before-buffer-allocation:') for e in events))
    elif variant in ['refused','failed','indeterminate']:
     expected={'kind':'REFUSED','decisionClass':'PR-2'} if variant=='refused' else {'kind':variant.upper(),'commitClass':body['commitClass']};check(effect+'/'+variant,actual=={'returned':expected} and 'result-open' not in sdk.trace)
    else:check(effect+'/'+variant,'error' in actual)
    if effect=='HE-1' and committed:
     check(effect+'/'+variant+'/immutable-commit',committed==[b'caller original bytes'])
     check(effect+'/'+variant+'/no-receipt-file',not any(p.suffix=='.bin' for p in root.iterdir()))
     check(effect+'/'+variant+'/stage-before-request',sdk.trace.index('stage-close')<sdk.trace.index('request:1'))
    if 'physical-commit' in events:check(effect+'/'+variant+'/journal-intent-before-effect',events.index('RA')<events.index('ICI' if body['commitClass']=='IRREVERSIBLE' else 'RCI')<events.index('physical-commit')<events.index('ICO' if body['commitClass']=='IRREVERSIBLE' else 'RCO')<events.index('UNLINK-STAGE')<events.index('effectResult'))
    if effect=='HE-2' and 'effectResult' in events:check(effect+'/'+variant+'/publication-before-result',events.index('RA')<events.index('RCI')<events.index('result-publication')<events.index('RCO')<events.index('effectResult'))
    normalized=copy.deepcopy(actual)
    if 'returned' in normalized and isinstance(normalized['returned'].get('bytes'),bytes):normalized['returned']['bytesHex']=normalized['returned'].pop('bytes').hex()
    traces.append({'id':effect+'/'+variant,'result':normalized,'hostEvents':events,'sdkEvents':sdk.trace,'wireRequests':counter[0],'securityDecisions':security_decisions});sdk.close();os.close(hostfd)
   check(effect+'/'+variant+'/spawn-scratch-removed',not Path(td).exists())
 empty_env={**M.B.FIXED,M.B.KEY:M.B.encode({'bootstrapVersion':1,'handles':[]}),'__CF_USER_TEXT_ENCODING':'runtime-added'};empty=M.BrokerSDK(empty_env,lambda seq,body:None)
 check('shipped-empty/no-courier-open',empty.trace==[] and not empty.hostStateWriteHandles and not empty.projectReadHandles and empty_env==M.B.FIXED);empty.close()
 with tempfile.TemporaryDirectory(prefix='opensip-courier-boundary-') as td:
  os.chmod(td,0o700);fd=os.open(td,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW);publisher=M.ReferenceResultPublisher(fd)
  try:
   block=b'x'*M.MAX_RESULT
   for i in range(4):
    reply=publisher.publish(f'{i:032x}',block);check('caps/result-exact-16MiB/'+str(i),reply['effectOutcome']=='COMPLETED' and (Path(td)/(f'{i:032x}'+'.bin')).stat().st_size==M.MAX_RESULT)
   before=sorted(p.name for p in Path(td).iterdir());reply=publisher.publish('f'*32,b'x')
   check('caps/spawn-exact-64MiB',publisher.charged_bytes==M.MAX_SPAWN)
   check('caps/spawn-one-over-no-publication',reply=={'effectOutcome':'FAILED'} and sorted(p.name for p in Path(td).iterdir())==before)
   oversize=M.ReferenceResultPublisher(fd);reply=oversize.publish('e'*32,block+b'x')
   check('caps/result-one-over-no-publication',reply=={'effectOutcome':'FAILED'} and oversize.charged_bytes==0 and sorted(p.name for p in Path(td).iterdir())==before)
  finally:os.close(fd)
 with tempfile.TemporaryDirectory(prefix='opensip-stage-boundary-') as td:
  os.chmod(td,0o700);root=Path(td).resolve();(root/'stage').mkdir(mode=0o700);calls=[]
  handles=[{'effectClass':'HE-1','authorizationRef':'ah:'+str(i)*32,'operationRef':'op-'+'2'*32,'commitClass':'REVERSIBLE'} for i in [1,3]]
  def stage_host(seq,body):
   path=root/'stage'/(body['authorizationRef'][3:]+'.bin');fd=os.open(path,os.O_RDONLY|os.O_NOFOLLOW|os.O_NONBLOCK)
   try:st=os.fstat(fd);data=M.file_read(fd,st.st_size)
   finally:os.close(fd)
   calls.append(len(data));path.unlink()
   return {'type':'effectResult','body':{'requestSeq':seq,'decisionSeq':1,'outcomeSeq':2,'commitClass':'REVERSIBLE','effectOutcome':'COMPLETED','resultRef':'rr:'+'f'*32+':'+M.sha(data)+':'+str(len(data))}}
  sdk=M.BrokerSDK({M.B.KEY:M.B.encode({'bootstrapVersion':1,'handles':handles,'resultScratchRoot':str(root)})},stage_host)
  try:
   result=sdk.writeHostState(sdk.hostStateWriteHandles[0],b'z'*M.MAX_RESULT)
   check('caps/stage-exact-16MiB-native',result=={'kind':'COMPLETED','commitClass':'REVERSIBLE'} and calls==[M.MAX_RESULT])
   failed=raised(lambda:sdk.writeHostState(sdk.hostStateWriteHandles[1],b'z'*(M.MAX_RESULT+1)))
   check('caps/stage-one-over-before-file-or-request',failed=={'error':'STAGE.OVER_CAP'} and calls==[M.MAX_RESULT] and list((root/'stage').iterdir())==[])
  finally:sdk.close()
 report={'standing':'REFERENCE-PHYSICAL-COURIER-EVIDENCE-NOT-PRODUCT-QUALIFICATION','passed':sum(c['passed'] for c in checks),'total':len(checks),'checks':checks,'traces':traces,'limits':['Host permission/journal prerequisites are explicit test bindings; journal events are ordering observations, not SQLite/witness execution.','Native temporary operations execute on this host only; no OS support-matrix qualification.','Request admission executes the exact receipt-pinned security library through its required context. Independent security acceptance and lifecycle gate integration remain separate adoption requirements.']}
 Path(args.report).write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(report['passed'],report['total']);print([c['id'] for c in checks if not c['passed']]);return 0 if report['passed']==report['total'] else 1
if __name__=='__main__':raise SystemExit(main())
