from pathlib import Path
import os,subprocess,tempfile,time,json,hashlib,statistics,sys
# U-2c SM-5 two-part series r2 (PLAN-r3 D-2 one timed span; D-3 R8 per entry). The accepted typed sealing run_set.py recipe
# with probe_two_part.py: 3 warmups + 7 measured fresh children per Rust entry, parent setpriority/readback 10, each direct
# child read back at 10, lane held for the whole set, private 0700 TMPDIR. Each R8 entry's repository part is the accepted
# overlay union (each entry's map carries the whole overlay, D-3). Control: every child's repository part must reproduce the
# accepted typed sealing shape (rows, inventory, snapshot2/plan2-equivalent digests, descriptor bytes) for its workload.
os.setpriority(os.PRIO_PROCESS,0,10);parent_nice=os.getpriority(os.PRIO_PROCESS,0);assert parent_nice==10
W=Path(__file__).resolve().parent;A=Path('/Users/sb/code/opensip-ai/opensip_arch');P=A.parent/'opensip';C=Path('/Users/sb/code/.opensip-implementation-cache');sys.path.insert(0,str(P/'tools/quality'));from corpus import manifest_document;from store import verify
raw=(A/'docs/implementation/m3/corpus/t2-corpus-manifest.draft.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='c8cc48e1549a05e9d563728fcac776ceca6c2ba63fa2004779385bd2fa4b7578';m=manifest_document(raw);entries={r['id']:r for r in m['repositories']};overlay=next(w for w in m['workspaces']if w['id']=='mr-rs-medium-serde-json')
typed={w['id']:w for w in json.loads((A/'docs/implementation/m3/spikes/s-m-sealing-typed-2026-10-09/results.json').read_text())['workloads']}
inputs=json.loads((W/'u2c-inputs.json').read_text())['entries'];dest=W/'sm5-two-part-results-r2.json';assert not dest.exists();E=W/'sm5-two-part-evidence';E.mkdir()
def members(eid):
 if eid.startswith('mr-rs-medium-serde-json/'):return 'mr-rs-medium-serde-json',[dict(root=str(C/'t2-corpus-c8cc48e1/store'/entries[r['entry']]['treeDigest']['value']),prefix=r['mount']+'/',entry=r['entry'])for r in overlay['overlay']['members']]
 assert entries[eid]['heldOut']is False;return eid,[dict(root=str(C/'t2-corpus-c8cc48e1/store'/entries[eid]['treeDigest']['value']),prefix='',entry=eid)]
D=Path(subprocess.check_output(['/usr/bin/getconf','DARWIN_USER_TEMP_DIR']).decode().strip());lock=D/'opensip-lanes.lock';owned=False
while True:
 try:lock.mkdir();owned=True;break
 except FileExistsError:print('waiting for lane',flush=True);time.sleep(5)
try:
 T=Path(tempfile.mkdtemp(prefix='opensip-u2c-sm5tp-',dir=D)).resolve();T.chmod(0o700);env=dict(PATH='/opt/homebrew/bin:/usr/bin:/bin',TMPDIR=str(T))
 for key in ['HOME','LANG','LC_ALL','TZ']:
  if key in os.environ:env[key]=os.environ[key]
 result=[]
 for e in inputs:
  wid,mem=members(e['entry']);proofs=[dict(entry=x['entry'],treeVerified=verify(Path(x['root']),entries[x['entry']]))for x in mem];acc=typed[wid]['shape']
  w=dict(id=e['slug'],entry=e['entry'],repositoryWorkload=wid,members=mem,dependency=dict(descriptor=e['descriptor'],dependencySourceSetId=e['dependencySourceSetId'],packages=e['packages']))
  inp=E/(e['slug']+'-input.json');inp.write_text(json.dumps(w,indent=1)+'\n');runs=[];shape=None
  for n in range(10):
   out=E/f"{e['slug']}-{n}.stdout";err=E/f"{e['slug']}-{n}.stderr"
   with out.open('wb')as o,err.open('wb')as x:
    child=subprocess.Popen(['/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14','-I','-B',str(W/'probe_two_part.py'),str(inp)],cwd=T,env=env,stdout=o,stderr=x);child_nice=os.getpriority(os.PRIO_PROCESS,child.pid);assert child_nice==10;_,status,usage=os.wait4(child.pid,0);code=os.waitstatus_to_exitcode(status)
   assert code==0,(e['slug'],n,err.read_text());r=json.loads(out.read_text());assert err.read_bytes()==b''
   current={k:v for k,v in r.items()if not k.endswith('Nanos')};shape=current if shape is None else shape;assert shape==current
   rp=r['repository'];assert rp['rows']==acc['rows'] and rp['bytes']==acc['bytes'] and rp['snapshotEquivalentDigest']==acc['snapshotEquivalentDigest'] and rp['planEquivalentDigest']==acc['planEquivalentDigest'] and rp['snapshotEquivalentDescriptorBytes']==acc['snapshotEquivalentDescriptorBytes'] and rp['nonregularExcluded']==acc['nonregularExcluded'] and rp['inventoryCanonicalBytes']==acc['inventoryCanonicalBytes'] and rp['inventorySha256']==hashlib.sha256(json.dumps(acc['regularRows'],ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
   dp=r['dependency'];assert dp['entries']==e['files'] and dp['bytes']==e['bytes'] and dp['dependencySourceSetId']==e['dependencySourceSetId']
   rss=int(usage.ru_maxrss);runs.append(dict(ordinal=n,observedChildNiceness=child_nice,warmup=n<3,elapsedNanos=r['elapsedNanos'],repositoryPartNanos=r['repositoryPartNanos'],dependencyPartNanos=r['dependencyPartNanos'],exitCode=0,rssNative=rss,rssUnit='bytes'))
  meas=[x for x in runs if not x['warmup']];stat=lambda k:dict(median=statistics.median(x[k]for x in meas),max=max(x[k]for x in meas))
  rp=shape['repository'];dp=shape['dependency']
  bounds=dict(repository=dict(rows=[rp['rows'],100000,rp['rows']<=100000],snapshotDescriptorBytes=[rp['snapshotEquivalentDescriptorBytes'],4194304,rp['snapshotEquivalentDescriptorBytes']<=4194304],bytes=[rp['bytes'],8589934592,rp['bytes']<=8589934592],source='PROPOSAL-r6:559 via PLAN-r3 D-9'),
   dependency=dict(packages=[dp['packages'],4096,dp['packages']<=4096],entries=[dp['entries'],1000000,dp['entries']<=1000000],bytes=[dp['bytes'],8589934592,dp['bytes']<=8589934592],descriptorBytes=[dp['descriptorCanonicalBytes'],None,'no contract bound on descriptor bytes found; reported only'],source='NE:2931-2932 ProtocolLimitsV3; DependencySourceSetV1 packages maxItems 4096'))
  result.append(dict(id=e['slug'],entry=e['entry'],repositoryWorkload=wid,acceptedTypedRepositoryShapeReproduced=True,shape=shape,bounds=bounds,verifiedMembers=proofs,runs=runs,elapsed=stat('elapsedNanos'),repositoryPart=stat('repositoryPartNanos'),dependencyPart=stat('dependencyPartNanos')))
  dest.write_text(json.dumps(dict(standing='UNREVIEWED U-2c SM-5 TWO-PART SERIES r2 (PLAN-r3 D-2 ONE SPAN, D-3 PER ENTRY); LEAD macOS PRELIMINARY; GENERATED-LOCK SETS ARE SIZING STAND-INS',workloads=result,ownedTMPDIR=str(T),TMPDIRMode='0700',laneHeldForEntireSet=True,nice=10,observedParentNiceness=parent_nice,supersedes='sm5-ds-results-r1.json (dependency part alone, separate span; retained as history)',SM5PlaceholderFilled=False,SMComplete=False,LG1Met=False,effectiveL=False,productQualification=False),indent=1)+'\n')
  print(e['entry'],round(statistics.median(x['elapsedNanos']for x in meas)/1e6,3),round(statistics.median(x['repositoryPartNanos']for x in meas)/1e6,3),round(statistics.median(x['dependencyPartNanos']for x in meas)/1e6,3),flush=True)
finally:
 if owned:lock.rmdir()
 assert not Path('/Users/sb/Library/Application Support/OpenSIP').exists()
