#!/usr/bin/env python3
"""Reference design checks. Does not qualify a product or a supported OS matrix."""
import argparse,copy,hashlib,importlib.util,json,os,shutil,subprocess,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
def load(name,file):
 s=importlib.util.spec_from_file_location(name,HERE/file);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
M=load('broker_bootstrap','broker-bootstrap.model.v1.py')
CONTROL=load('broker_control','control-completion.check.v5.py')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--report',default=str(HERE/'broker-bootstrap.report.v1.json'));ap.add_argument('--node',default=shutil.which('node'));args=ap.parse_args()
 results=[]
 def check(id,value):results.append({'id':id,'passed':bool(value)})
 def raises(fn,typ):
  try:fn()
  except typ:return True
  return False
 corpus=json.loads((HERE/'broker-bootstrap.cases.v1.json').read_text())
 for c in corpus['cases']:
  try:M.parse(c['encoded']);actual='ACCEPT'
  except M.StartupFailure:actual='STARTUP-FAILURE'
  check('parse/'+c['id'],actual==c['expected'])
 base={'spawn':'spawn-1','component':'component-1','installGeneration':1,'manifest':'a'*64,'platform':'macos-arm64','policy':'b'*64,'projectKey':'PRIVATE-PROJECT-KEY','grantGeneration':1,'pid':1234,'bootUUID':'boot-1','declared':['PT-HOST-EFFECT-BROKERED'],'denied':[]}
 def broker():
  h=M.HostBroker(base,entropy=lambda:'1'*32);h.register('HE-1','op-'+'2'*32,'gj:UFJJVkFURQ:1:1','host-owned-target',{'host-approved':'parameter'});return h
 h=broker();env=M.launch_environment({'HOME':'dummy-home','PATH':'dummy-path','NODE_OPTIONS':'--require=ambient','OPENSSL_CONF':'ambient','OPENSIP_BROKER_CONTEXT':'forged','HTTP_PROXY':'dummy'},h.bootstrap());dispatch=[lambda b:None];sdk=M.SDK(lambda b:dispatch[0](b));handles=sdk.consume(env)
 check('sdk/consume-once-and-remove',M.KEY not in env and len(handles)==1)
 check('sdk/repeated-consume',raises(lambda:sdk.consume(env),M.StartupFailure))
 env2={M.KEY:h.bootstrap()};check('sdk/reinsert-still-rejected',raises(lambda:sdk.consume(env2),M.StartupFailure) and M.KEY not in env2)
 for label,environment in [('missing',{}),('malformed',{M.KEY:'='})]:
  check('sdk/'+label,raises(lambda:M.SDK().consume(environment),M.StartupFailure) and M.KEY not in environment)
 check('sdk/empty-shipped',M.SDK().consume({M.KEY:M.encode({'bootstrapVersion':1,'handles':[]})})==())
 calls=[];dispatch[0]=lambda b:calls.append(b)
 for name,obj in [('unknown',object()),('forged-constructor',M.Handle()),('copied',copy.copy(handles[0])),('cross-sdk',M.SDK().consume({M.KEY:h.bootstrap()})[0]),('dict',{'authorizationRef':'ah:'+'1'*32})]:
  check('sdk/reject-'+name,raises(lambda:sdk.requestEffect(obj),M.LocalHandleFailure) and not calls)
 captured=[];dispatch[0]=lambda b:captured.append(b);sdk.requestEffect(handles[0]);captured[0]['operationRef']='mutated';captured2=[];dispatch[0]=lambda b:captured2.append(b);sdk.requestEffect(handles[0]);body=captured2[0]
 check('sdk/courier-fields-immutable',body==M.parse(h.bootstrap())['handles'][0])
 check('sdk/no-provider-params',raises(lambda:sdk.requestEffect(handles[0],{'target':'attacker'}),TypeError))
 check('sdk/subprocess-strip',M.KEY not in sdk.child_environment({**env,M.KEY:'reinserted'}))
 check('host/courier-hides-authority',all(x not in json.dumps(body)+h.bootstrap() for x in ('PRIVATE-PROJECT-KEY','gj:','host-owned-target','host-approved')))
 dispatch[0]=lambda b:h.dispatch(b,base);decision=sdk.requestEffect(handles[0])
 check('host/exact-registered-admission',decision=={'wire':None,'decision':'GRANTED','initiated':[],'registeredTarget':'host-owned-target','registeredParameters':{'host-approved':'parameter'}})
 check('host/grant-durable-before-launch',h.schedule==[{'op':'WRITE','type':'GRANT','request':body['authorizationRef']},{'op':'SYNC'}])
 check('host/no-dynamic-registration',raises(lambda:h.register('HE-2','op-'+'3'*32,'gj:internal:1:2','target',{}),ValueError))
 for key in M.HostBroker.BINDINGS:
  wrong=copy.deepcopy(base);wrong[key]='wrong'
  check('host/context-'+key,h.dispatch(body,wrong)=={'wire':'RF-6','decision':'PR-4','initiated':[]})
  b=broker();b.bootstrap();b.current[key]='changed';check('host/current-'+key,b.dispatch(body,base)['decision']=='PR-4')
 for key in body:
  wrong={**body,key:'forged'};check('host/request-'+key,h.dispatch(wrong,base)['decision']=='PR-4')
 b=broker();b.schedule.pop();b.bootstrap();check('host/undurable-grant',b.dispatch(body,base)['decision']=='PR-4')
 b=broker();b.bootstrap();b.revoke();check('host/revoked',b.dispatch(body,base)=={'wire':'RF-6','decision':'PR-5','initiated':[]})
 b=broker();b.bootstrap();b.current['denied']=['PT-HOST-EFFECT-BROKERED'];check('host/current-policy-denial',b.dispatch(body,base)['decision']=='PR-2')
 b=broker();b.bootstrap();b.current['declared']=[];check('host/current-manifest-undeclared',b.dispatch(body,base)['decision']=='PR-1')
 b=broker();b.bootstrap();b.close();check('host/spawn-closed-handle',b.dispatch(body,base)['decision']=='PR-4')
 b=broker();check('host/duplicate-grant',raises(lambda:b.register('HE-1','op-'+'2'*32,'gj:UFJJVkFURQ:1:1','target',{}),ValueError))
 sequence=iter(['1'*32,'1'*32,'3'*32,'4'*32,'5'*32])
 b=M.HostBroker(base,entropy=lambda:next(sequence));one=b.register('HE-1','op-'+'2'*32,'gj:internal:1:1','one',{});two=b.register('HE-2','op-'+'2'*32,'gj:internal:1:2','two',{})
 check('host/two-grants-one-operation',one['operationRef']==two['operationRef'] and one['authorizationRef']!=two['authorizationRef'])
 check('host/collision-regenerated',two['authorizationRef']=='ah:'+'3'*32)
 b.register('HE-1','op-'+'4'*32,'gj:internal:1:3','three',{});b.register('HE-2','op-'+'5'*32,'gj:internal:1:4','four',{})
 check('host/four-grants',len(b._entries)==4)
 check('host/fifth-grant-refuses-before-truncation',raises(lambda:b.register('HE-1','op-'+'6'*32,'gj:internal:1:5','five',{}),ValueError) and len(b._entries)==4)
 dirty={**M.FIXED,M.KEY:h.bootstrap(),'__CF_USER_TEXT_ENCODING':'runtime-added','PATH':'mutated'};M.SDK().consume(dirty)
 check('sdk/sanitize-before-provider',dirty==M.FIXED)
 b=M.HostBroker(base);fresh=b.register('HE-1','op-'+'3'*32,'gj:internal:1:1','target',{});check('host/csprng-format',len(fresh['authorizationRef'])==35 and fresh['authorizationRef'].startswith('ah:'))
 # Existing control schema remains broad and opaque. Host-derived authorization
 # result is joined to its RF6 route; local SDK never fabricates RF evidence.
 old=json.loads((HERE/'control-completion.cases.v5.json').read_text())
 context=copy.deepcopy(next(c['context'] for c in old['cases'] if c.get('expected',{}).get('type')=='effectRequest'))
 for allow in (True,False):
  context['authorizationEvidence']={'authorized':allow,**body,'decisionClass':None if allow else 'PR-4','bindingMismatchDecisionClass':'PR-4'}
  raw=json.dumps({'type':'effectRequest','seq':1,'controlMajor':1,'body':body},separators=(',',':')).encode();wire=len(raw).to_bytes(4,'big')+raw
  try:verdict=CONTROL.parse(wire,context)['verdict']
  except CONTROL.Refusal as e:verdict=e.family+'/'+str(e.decision)
  check('control/opaque-handle-'+str(allow),verdict==('ACCEPT' if allow else 'RF-6/PR-4'))
 # Retain a byte-exact actual frame, not a schema-only example.
 frame={'context':context,'frameHex':wire.hex(),'expectedRefusal':'RF-6/PR-4'}
 # Replay all previously reviewed framing/transition cases to an external report.
 with tempfile.TemporaryDirectory(prefix='opensip-broker-control-') as td:
  r=Path(td)/'report.json';p=subprocess.run([str(Path(os.sys.executable)),str(HERE/'control-completion.check.v5.py'),'--report',str(r)],capture_output=True,text=True)
  check('control/484-regressions-byte-identical',p.returncode==0 and r.read_bytes()==(HERE/'control-completion.report.v5.json').read_bytes())
 # Actual reference runtime launch, with exact verified empty config asset.
 node=Path(args.node).resolve();config=(HERE/'broker-bootstrap.openssl-empty.v1.cnf').resolve();entry=(HERE/'broker-bootstrap.node-probe.v1.cjs').resolve()
 check('runtime/empty-config-digest',config.read_bytes()==b'' and hashlib.sha256(config.read_bytes()).hexdigest()=='e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855')
 with tempfile.TemporaryDirectory(prefix='opensip-broker-scratch-') as td:
  os.chmod(td,0o700);launchenv=M.launch_environment({'HOME':'ambient','PATH':'ambient','OPENSIP_BROKER_CONTEXT':'ambient'},M.encode({'bootstrapVersion':1,'handles':[]}));argv=M.launch_argv(str(node),str(config),str(entry))
  p=subprocess.run(argv,cwd=td,env=launchenv,shell=False,capture_output=True,text=True,timeout=20);out=json.loads(p.stdout) if p.returncode==0 else {}
  check('runtime/node24',out.get('version','').startswith('v24.'))
  check('runtime/full-icu',out.get('fullICU'))
  check('runtime/exact-flags',out.get('execArgv')==argv[1:-1])
  check('runtime/exec-five-keys',set(launchenv)==set(M.FIXED)|{M.KEY})
  check('runtime/sanitized-five-keys',out.get('sanitized')==launchenv)
  check('runtime/no-forbidden-ambient',not (set(out.get('env',{})) & {'HOME','PATH','NODE_OPTIONS','NODE_PATH','OPENSSL_CONF','SSL_CERT_FILE','HTTP_PROXY','HTTPS_PROXY'}))
  check('runtime/scratch-cwd-0700',out.get('cwd')==str(Path(td).resolve()) and out.get('mode')==0o700)
  check('runtime/bootstrap-removed',out.get('bootstrapConsumed'))
  check('runtime/subprocess-exclusion',out.get('childExit')==0 and out.get('child',{}).get('keys')==sorted(M.FIXED) and out.get('child',{}).get('brokerPresent') is False)
 check('runtime/scratch-destroyed',not Path(td).exists())
 report={'standing':'REFERENCE-DESIGN-EVIDENCE-NOT-PRODUCT-QUALIFICATION','passed':sum(r['passed'] for r in results),'total':len(results),'results':results,'controlFrame':frame,'sourcePins':{p:hashlib.sha256((ROOT/p).read_bytes()).hexdigest() for p in ['docs/coop/artifacts/delivery.v2.json','docs/coop/completion/security-completion.v2.md','docs/coop/completion/security-behavior-model.v2.py','docs/coop/completion/control-completion.schema.v3.json','docs/coop/completion/control-completion.check.v5.py','docs/coop/completion/control-completion.cases.v5.json','docs/coop/completion/control-completion.report.v5.json']},'runtime':{'version':out.get('version'),'nodeSha256':hashlib.sha256(node.read_bytes()).hexdigest(),'platform':os.sys.platform,'nodePath':str(node),'fullICU':out.get('fullICU'),'rawEnvironmentKeys':sorted(out.get('env',{})),'sanitizedEnvironmentKeys':sorted(out.get('sanitized',{})),'descendantRawEnvironmentKeys':out.get('child',{}).get('rawKeys')},'limitations':['One native host probe; not four-platform qualification.','SDK identity checks are API misuse guards, not an in-process sandbox.','Host model stops at request admission; journal carrier, witness durability, and effect execution retain their separate security contracts.','Shipped TypeScript has zero broker handles; nonempty cases are synthetic host-registered operations.']}
 Path(args.report).write_text(json.dumps(report,indent=2,sort_keys=True)+'\n');print(f"{report['passed']}/{report['total']} passed")
 if report['passed']!=report['total']:raise SystemExit(1)
if __name__=='__main__':main()
