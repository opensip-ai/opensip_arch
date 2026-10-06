import hashlib,importlib.util,json,pathlib,shutil,socket,threading
base=pathlib.Path('/tmp/opensip-implementation/jbs-product-authoring');root=base/'product';trial=base/'confinement-probe'
if trial.exists():shutil.rmtree(trial)
trial.mkdir()
def module(name):
 spec=importlib.util.spec_from_file_location('probe_'+name,root/('tools/contracts/'+name+'.py'));m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
admission=module('admission');confine=module('confine');admission.verify_confinement(json.loads((root/'tools/contracts/confinement-profile.json').read_bytes()))
node=pathlib.Path('/Users/sb/opensip-deps/native-repin-01/runs/check-1/tool-node');generator=pathlib.Path('/Users/sb/opensip-deps/contracts-generator-rebuild-02/opensip-contract-generator')
script=trial/'probe.cjs';script.write_bytes(pathlib.Path('/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/native-repin-selection-v1/evidence/reprobe/scripts/probe.cjs').read_bytes())
canary_dir=trial/'canary';canary_dir.mkdir();canary=canary_dir/'secret.txt';canary.write_text('synthetic outside canary\n');inputs=trial/'inputs';inputs.mkdir();(inputs/'options.json').write_text('{}\n')
records=[]
def capture(label,command,exe,reads,writes,cwd,confined=True):
 if confined:
  profile=trial/(label+'.sb');profile.write_text(admission.child_profile(exe,reads,writes));command=['/usr/bin/sandbox-exec','-f',str(profile),*map(str,command)]
 status,out,err,failure=confine.capture_child(list(map(str,command)),cwd=cwd,env={'PATH':'/usr/bin:/bin','LANG':'C','LC_ALL':'C','TZ':'UTC'},timeout=30)
 (trial/(label+'.stdout')).write_bytes(out);(trial/(label+'.stderr')).write_bytes(err);assert not failure,(label,failure)
 record={'label':label,'confined':confined,'exitCode':status};records.append(record);return status,out
results={}
for confined in [True,False]:
 label='confined' if confined else 'control';run=trial/label;run.mkdir();scratch=run/'scratch';output=run/'output';scratch.mkdir();output.mkdir()
 tcp=socket.socket();tcp.bind(('127.0.0.1',0));tcp.listen();tcp.settimeout(5);udp=socket.socket(socket.AF_INET,socket.SOCK_DGRAM);udp.bind(('127.0.0.1',0));udp.settimeout(5);seen={}
 def listen(sock,key):
  try:
   if key=='tcp':sock.accept()[0].close()
   else:sock.recvfrom(64)
   seen[key]=True
  except OSError:seen[key]=False
 threads=[threading.Thread(target=listen,args=(tcp,'tcp')),threading.Thread(target=listen,args=(udp,'udp'))]
 for thread in threads:thread.start()
 cfg={'scratch':str(scratch),'output':str(output),'input':str(inputs/'options.json'),'tcpPort':tcp.getsockname()[1],'udpPort':udp.getsockname()[1],'outsideReads':{'canary':str(canary)},'outsideStats':{'canary':str(canary)},'outsideLists':{'canaryDir':str(canary_dir)},'outsideWrites':{'canaryDir':str(canary_dir/(label+'-write'))}}
 status,out=capture(label,[node,script,json.dumps(cfg)],node,[script,inputs],[scratch,output],scratch,confined);assert status==0;values=json.loads(out)
 for thread in threads:thread.join()
 tcp.close();udp.close();results[label]={'values':values,'listenerObserved':seen}
 assert values['allowedScratchWrite']=='ALLOWED' and values['allowedOutputWrite']=='ALLOWED' and 'ALLOWED' in values['allowedInputRead']
 if confined:
  for key in ['outsideRead:canary','outsideStat:canary','outsideList:canaryDir','outsideWrite:canaryDir','symlinkEscapeRead','hardlinkEscape','writeRootRename','syslogUnixConnect','loopbackTcp','loopbackUdp','listen','etcPasswdRead','tmpdirList']:assert values[key] in ['EPERM','EACCES'],(key,values[key])
  assert values['spawnShell']=={'ALLOWED':'EPERM'}
  assert seen=={'tcp':False,'udp':False};assert output.is_dir();assert not (canary_dir/'confined-write').exists()
 else:
  for key in ['outsideRead:canary','outsideStat:canary','outsideList:canaryDir','symlinkEscapeRead']:assert 'ALLOWED' in values[key],(key,values[key])
  assert values['outsideWrite:canaryDir']=='ALLOWED' and values['spawnShell']=={'ALLOWED':'RAN'} and values['loopbackUdp']=='SENT' and values['listen']=='ALLOWED';assert seen=={'tcp':True,'udp':True}
assert canary.read_text()=='synthetic outside canary\n'
prepared=base/'generate-candidate-1/prepared';granted=trial/'generator-granted';granted.mkdir();outside=trial/'generator-outside';outside.mkdir()
for label,read,write,expected,confined in [('generator-positive',prepared,granted/'yes',0,True),('generator-outside-read',prepared,outside/'no-read',None,True),('generator-outside-write',prepared,outside/'no-write',None,True),('generator-control',prepared,outside/'control',0,False)]:
 reads=[inputs] if label=='generator-outside-read' else [prepared]
 status,_=capture(label,[generator,read,write],generator,reads,[granted],trial,confined)
 assert status==0 if expected==0 else status!=0,(label,status)
 if expected is None:assert not write.exists()
status,_=capture('undeclared-exec',['/bin/sh','-c','echo synthetic'],node,[inputs],[granted],trial);assert status!=0
assert not pathlib.Path('/Users/sb/Library/Application Support/OpenSIP').exists()
result={'passed':True,'standing':'macOS 27.0.1 development runtime-pin maintenance controls; same child renderer and confinement policies; not release qualification','probeSha256':hashlib.sha256(script.read_bytes()).hexdigest(),'records':records,'results':results,'canaryUnchanged':True,'installationAbsent':True,'productQualification':False}
(base/'confinement-checks.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'passed':True,'childRuns':len(records),'confinedNodeChecks':len(results['confined']['values']),'productQualification':False}))
