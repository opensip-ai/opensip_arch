#!/usr/bin/env python3
"""Independent adversarial broker integration probes; reference execution only."""
import argparse, copy, hashlib, importlib.util, json, os, tempfile
from pathlib import Path
P=Path(__file__).resolve().parent
ROOT=P.parents[2]
def load(name,path):
 s=importlib.util.spec_from_file_location(name,P/path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
M=load('independent_courier','broker-sdk-courier.model.v1.py')
J=load('independent_security_join','broker-host-security-join.v2.py')
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--report',default=str(P/'broker-integration-independent-probes.v1.json'));args=ap.parse_args()
 checks=[]
 def check(name,value,observed=None):checks.append({'id':name,'passed':bool(value),'observed':observed})
 freeze=P/'broker-bootstrap.freeze.v4.json';f=json.loads(freeze.read_text())
 check('exact-review-subject',digest(freeze)=='ab83b12f1de37ac36788d4ddc01c5f47760af6e8058a53ce1d944989124dc3c9')
 pins=f['subjects']+f['dependencies'];before={x['path']:digest(ROOT/x['path']) for x in pins}
 check('all-frozen-subjects-and-dependencies-match',all(before[x['path']]==x['sha256'] for x in pins))
 response_variants={
 'success':lambda r:None,'missing-request':lambda r:r['body'].pop('requestSeq'),
 'null-body':lambda r:r.update(body=None),'array-body':lambda r:r.update(body=[]),
 'extra-envelope-key':lambda r:r.update(seq=1),'extra-body-key':lambda r:r['body'].update(extra=True),
 'boolean-decision':lambda r:r['body'].update(decisionSeq=True),
 'boolean-outcome':lambda r:r['body'].update(outcomeSeq=True),
 'zero-decision':lambda r:r['body'].update(decisionSeq=0),
 'over-js-outcome':lambda r:r['body'].update(outcomeSeq=9007199254740992),
 'wrong-commit':lambda r:r['body'].update(commitClass='IRREVERSIBLE'),
 'reversed-journal-pair':lambda r:r['body'].update(decisionSeq=12,outcomeSeq=11),
 'wrong-request':lambda r:r['body'].update(requestSeq=2),
 'ref-nul-tail':lambda r:r['body'].update(resultRef=r['body']['resultRef']+'\u0000'),
 'ref-leading-zero-length':lambda r:r['body'].update(resultRef=r['body']['resultRef'][:-1]+'01'),
 'ref-uppercase-id':lambda r:r['body'].update(resultRef=r['body']['resultRef'].replace('a'*32,'A'*32)),
 'ref-over-file-cap':lambda r:r['body'].update(resultRef='rr:'+'a'*32+':'+'b'*64+':16777217'),
 'non-completed-failed':lambda r:r['body'].update(effectOutcome='FAILED'),
 'non-completed-indeterminate':lambda r:r['body'].update(effectOutcome='INDETERMINATE'),
 'terminal-refusal':lambda r:r.update(type='refusal',body={'family':'RF-6','decisionClass':'PR-5'}),
 }
 for variant,mutate in response_variants.items():
  with tempfile.TemporaryDirectory(prefix='independent-broker-') as td:
   root=Path(td);os.chmod(root,0o700);(root/'stage').mkdir(mode=0o700)
   raw=b'x';(root/('a'*32+'.bin')).write_bytes(raw)
   entry={'effectClass':'HE-2','authorizationRef':'ah:'+'1'*32,'operationRef':'op-'+'2'*32,'commitClass':'REVERSIBLE'}
   descriptor={'bootstrapVersion':1,'handles':[entry],'resultScratchRoot':str(root)}
   calls=[]
   def send(seq,body):
    calls.append((seq,body));r={'type':'effectResult','body':{'requestSeq':seq,'decisionSeq':10,'outcomeSeq':11,'commitClass':'REVERSIBLE','effectOutcome':'COMPLETED','resultRef':'rr:'+'a'*32+':'+M.sha(raw)+':1'}};mutate(r);return r
   env={**M.B.FIXED,M.B.KEY:M.B.encode(descriptor),'NODE_OPTIONS':'hostile'}
   sdk=M.BrokerSDK(env,send)
   try:
    try:result=sdk.readProject(sdk.projectReadHandles[0]);observed=result['kind']
    except M.CourierFailure as e:result=None;observed=str(e)
    expected='COMPLETED' if variant=='success' else 'FAILED' if variant.endswith('-failed') else 'INDETERMINATE' if variant.endswith('-indeterminate') else 'REFUSED' if variant=='terminal-refusal' else None
    check('response:'+variant,(result is None if expected is None else result['kind']==expected),observed)
    check('wire-and-no-unadmitted-read:'+variant,len(calls)==1 and calls[0][1]=={k:entry[k] for k in ['effectClass','authorizationRef','operationRef']} and (variant=='success' or 'result-open' not in sdk.trace))
    if variant=='terminal-refusal':check('terminal-refusal-clears-all-local-authority',not sdk._registry and sdk._root is None and sdk._stage is None)
    if variant=='success':check('bootstrap-not-visible-after-admission',M.B.KEY not in env and 'NODE_OPTIONS' not in env)
   finally:sdk.close()
 with tempfile.TemporaryDirectory(prefix='independent-cross-spawn-') as td:
  root=Path(td);os.chmod(root,0o700);(root/'stage').mkdir(mode=0o700);calls=[]
  entries=[{'effectClass':e,'authorizationRef':'ah:'+str(i)*32,'operationRef':'op-'+str(i)*32,'commitClass':'REVERSIBLE'} for i,e in [(1,'HE-1'),(2,'HE-2')]]
  desc={'bootstrapVersion':1,'handles':entries,'resultScratchRoot':str(root)}
  make=lambda:M.BrokerSDK({**M.B.FIXED,M.B.KEY:M.B.encode(desc)},lambda *x:calls.append(x))
  a=make();b=make()
  try:
   for name,method,h in [('foreign-write',a.writeHostState,b.hostStateWriteHandles[0]),('foreign-read',a.readProject,b.projectReadHandles[0]),('forged-write',a.writeHostState,M.WriteHandle()),('forged-read',a.readProject,M.ReadHandle()),('wrong-class-write',a.writeHostState,a.projectReadHandles[0]),('wrong-class-read',a.readProject,a.hostStateWriteHandles[0])]:
    try:method(h,b'x') if 'write' in name else method(h);error='RETURNED'
    except M.CourierFailure as e:error=str(e)
    check(name,error=='SDK.UNKNOWN_LOCAL_HANDLE' and not calls and list((root/'stage').iterdir())==[],error)
   try:a.writeHostState(a.hostStateWriteHandles[0],b'x'*(M.MAX_RESULT+1));error='RETURNED'
   except M.CourierFailure as e:error=str(e)
   check('oversized-stage-before-file-or-request',error=='STAGE.OVER_CAP' and not calls and list((root/'stage').iterdir())==[],error)
   h=a.projectReadHandles[0];a.close()
   try:a.readProject(h);error='RETURNED'
   except M.CourierFailure as e:error=str(e)
   check('closed-instance-cannot-dispatch',error=='SDK.UNKNOWN_LOCAL_HANDLE' and not calls,error)
  finally:a.close();b.close()
 # Exercise actual pinned security request admission with independent context mutations.
 for effect in ['HE-1','HE-2']:
  body={'effectClass':effect,'authorizationRef':'ah:'+'1'*32,'operationRef':'op-'+'2'*32}
  base=J.context(body,{'snapshotDigest':'a'*64,'members':{'src/member.ts':b'x'}},16)
  def entry(c):return c['connectionMap'][body['authorizationRef']]
  def grant(c,role):return c['journalState'][entry(c)[role+'Locator']]
  mutants={
   'valid':lambda c:None,'foreign-operation':lambda c:entry(c).update(operationRef='op-'+'9'*32),
   'foreign-generation':lambda c:entry(c).update(grantGeneration=2),
   'broker-token-swap':lambda c:grant(c,'broker').update(token=J.SEC.EFFECT_UNDERLYING_TOKEN[effect]),
   'underlying-token-swap':lambda c:grant(c,'underlying').update(token='PT-HOST-EFFECT-BROKERED'),
   'broker-revoked':lambda c:grant(c,'broker').update(status='REVOKED'),
   'underlying-closed':lambda c:grant(c,'underlying').update(status='CLOSED'),
   'broker-platform-rebind':lambda c:grant(c,'broker')['binding'].update(platform='linux-arm64'),
   'underlying-empty-scope':lambda c:grant(c,'underlying').update(scope={}),
   'extra-context':lambda c:c.update(callerAuthority=True),
  }
  if effect=='HE-2':mutants.update({'prefix-boundary':lambda c:grant(c,'broker')['scope'].update(pathPrefixes=['sr']), 'wrong-snapshot':lambda c:grant(c,'underlying')['scope'].update(snapshotDigest='c'*64),'missing-exact-member':lambda c:c.update(snapshotMembers=['src/other.ts'])})
  else:mutants.update({'bool-byte-cap':lambda c:entry(c)['target'].update(byteCap=True),'state-class-mismatch':lambda c:grant(c,'underlying')['scope'].update(stateClass='SC-CACHE')})
  for name,mutate in mutants.items():
   ctx=copy.deepcopy(base);mutate(ctx);got=J.evaluate(body,ctx)
   check('security-request:'+effect+':'+name,(got is None) if name=='valid' else isinstance(got,dict) and got['family']=='RF-6' and got['decisionClass'] in ['PR-4','PR-5'],got)
 check('all-subjects-and-dependencies-unchanged',before=={x['path']:digest(ROOT/x['path']) for x in pins})
 report={'documentClass':'independent-broker-integration-probes','subject':{'path':str(freeze.relative_to(ROOT)),'sha256':digest(freeze)},'securityAcceptance':'SEPARATE-NOT-CERTIFIED','checks':checks,'counts':{'passed':sum(c['passed'] for c in checks),'failed':sum(not c['passed'] for c in checks),'total':len(checks)},'limitations':['One-host physical reference execution; no native platform qualification.','Security request join is checked against exact v6; security unit acceptance is separate.','No real transport concurrency, durable journal, operation lease or GC qualification.']}
 Path(args.report).write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(report['counts']);return bool(report['counts']['failed'])
if __name__=='__main__':raise SystemExit(main())
