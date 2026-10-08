from pathlib import Path
import os,json,subprocess,tempfile,hashlib
B=Path('/tmp/opensip-implementation/o1b-authoring-r1');root=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());private=Path(tempfile.mkdtemp(prefix='opensip-o1b-phases-',dir=root));private.chmod(0o700);env=dict(os.environ,PATH='/opt/homebrew/bin:/opt/homebrew/Cellar/rust/1.95.0/bin',TMPDIR=str(private));rows=[]
def invoke(exe,argv,name):
 raw=private/(name+'.stream');out=private/(name+'.stdout');err=private/(name+'.stderr')
 with raw.open('wb') as stream,out.open('wb') as stdout,err.open('wb') as stderr:
  channel=os.dup(stream.fileno())
  pid=os.posix_spawn(str(exe),[str(exe),*argv],env,file_actions=[(os.POSIX_SPAWN_DUP2,stdout.fileno(),1),(os.POSIX_SPAWN_DUP2,stderr.fileno(),2),(os.POSIX_SPAWN_DUP2,channel,3)]);_,status=os.waitpid(pid,0);os.close(channel)
 assert os.waitstatus_to_exitcode(status)==0,(name,status,err.read_bytes());assert not err.read_bytes()
 data=raw.read_bytes();records=[json.loads(x) for x in data.splitlines()];assert records[0]['event']=='log.stream.opened' and records[0]['fields']['sink']=='harness'
 (B/(name+'.stream')).write_bytes(data);(B/(name+'.stdout')).write_bytes(out.read_bytes());return records,data
records,data=invoke(B/'stream-probe',['phase-api'],'actual-phase-api')
starts={x['fields']['phase']:x['fields'] for x in records if x['event']=='host.phase.started'};ends={x['fields']['phase']:x['fields'] for x in records if x['event']=='host.phase.completed'}
assert set(starts)=={'request','delivery'} and set(ends)=={'request','delivery','reuse'}
assert starts['request']['at']==0 and 'parent' not in starts['request'];assert starts['delivery']['parent']=='request'
for phase in starts:assert ends[phase]['wall']==ends[phase]['at']-starts[phase]['at'] and ends[phase]['cpu']>=0
assert ends['delivery']['outcome']=='failed' and ends['request']['outcome']=='cancelled'
assert ends['reuse']['outcome']=='not-applicable' and ends['reuse']['wall']==ends['reuse']['cpu']==0
assert starts['delivery']['at']<=ends['delivery']['at']<=ends['reuse']['at']<=ends['request']['at']
rows.append({'name':'actual-phase-api-pair-not-applicable-outcomes','passed':True,'recordCount':len(records)})
records,data=invoke(B/'product/target/harness/opensip',['version','--format','json'],'optimized-harness-profile')
assert len(records)==6 and records[0]['fields']['build']=='debug-assertions-on';rows.append({'name':'optimized-harness-actual-stream','passed':True,'recordCount':len(records)})
# Q0's per-record parent semantic validation is separate from grammatical read-back.
parents={'request':None,'delivery':'request','reuse':'request'}
def parents_valid(records):
 return all(row['fields'].get('parent')==parents[row['fields']['phase']] for row in records if row['event']=='host.phase.started')
assert parents_valid(records);bad=json.loads(json.dumps(records));next(x for x in bad if x['event']=='host.phase.started' and x['fields']['phase']=='delivery')['fields']['parent']='reuse';assert not parents_valid(bad);rows.append({'name':'harness-parent-semantic-control','passed':True,'wrongRegisteredParentRejected':True,'Q0EnvelopeAccepted':False})
for name in ['inheritance-probe','driver-torn']:
 path=B/(name+'.stream');digest=hashlib.sha256(path.read_bytes()).hexdigest();independent=subprocess.check_output(['/usr/bin/openssl','dgst','-sha256',str(path)]).decode().strip().rsplit(' ',1)[1];assert digest==independent
 fragment={'operationalRecords':[{'recordSha256':digest}]};assert fragment['operationalRecords'][0]['recordSha256']==independent
 tampered=json.loads(json.dumps(fragment));tampered['operationalRecords'][0]['recordSha256']='0'*64;assert tampered['operationalRecords'][0]['recordSha256']!=independent
 (B/(name+'-driver-fragment.json')).write_text(json.dumps(fragment,indent=2)+'\n');rows.append({'name':name+'-driver-digest-field','passed':True,'bytes':path.stat().st_size,'sha256':digest,'Q0EnvelopeAccepted':False})
(B/'phase-stream-controls.json').write_text(json.dumps({'standing':'Unreviewed actual phase/optimized-profile/driver-fragment controls; no Q0 envelope acceptance or M6 qualification','passed':True,'checks':rows,'productQualification':False,'inventoryAuthored':False},indent=2)+'\n');print('phase/profile/digest controls passed',len(rows))
