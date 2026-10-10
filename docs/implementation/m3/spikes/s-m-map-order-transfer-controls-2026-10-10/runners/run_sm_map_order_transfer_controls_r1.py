from pathlib import Path
import json,struct,hashlib,subprocess,tempfile,os
os.setpriority(os.PRIO_PROCESS,0,10)
B=Path('/tmp/opensip-implementation');V=B/'sm-map-order-transfer-2026-10-10';dest=V/'controls-r1.json';assert not dest.exists();root=Path(tempfile.mkdtemp(prefix='opensip-sm-map-order-controls-',dir='/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T'));root.chmod(0o700)
def u64(n):return struct.pack('>Q',n)
def frame(b):return struct.pack('>I',len(b))+b
def rawmap(rows):return b'OPSMRUST1\0'+u64(len(rows))+b''.join(u64(len(n.encode()))+n.encode()+u64(len(c))+c for n,c in rows)
cases=[('member-before-registry-order',[('/z-member/empty.rs',b''),('/a-registry/lib.rs',b'public')],True,False),('unicode-quoted-path-order',[('/β.rs',b'one'),('/a"line.rs',b'two')],True,False),('nonadjacent-duplicate',[('/z.rs',b'one'),('/a.rs',b'two'),('/z.rs',b'three')],False,False),('unordered-map-whole-pin-corruption',[('/z.rs',b'one'),('/a.rs',b'two')],False,True)];records=[]
for name,rows,success,corrupt in cases:
 raw=rawmap(rows);wire=frame(json.dumps(dict(format='OPSMRUST1',bytes=len(raw),sha256='0'*64 if corrupt else hashlib.sha256(raw).hexdigest())).encode())+b''.join(frame(raw[i:i+7]) for i in range(0,len(raw),7));(root/(name+'.input')).write_bytes(wire);err=(root/(name+'.stderr')).open('xb');child=subprocess.Popen(['/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14','-I','-B',str(V/'ready_receiver.py')],cwd=root,env={'TMPDIR':str(root)},stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=err);ready=child.stdout.readline();assert ready==b'ready\n';out,_=child.communicate(wire,timeout=30);err.close();(root/(name+'.stdout')).write_bytes(ready+out);assert (child.returncode==0)==success;result=json.loads(out) if success else None
 if success:
  descriptor=json.dumps(sorted([dict(path=n,bytes=len(c),sha256=hashlib.sha256(c).hexdigest()) for n,c in rows],key=lambda r:r['path'].encode()),ensure_ascii=False,sort_keys=True,separators=(',',':')).encode();assert result['descriptorBytes']==len(descriptor) and result['descriptorSha256']==hashlib.sha256(descriptor).hexdigest() and result['mapSha256']==hashlib.sha256(raw).hexdigest() and result['contentBytes']==sum(len(c) for _,c in rows)
 elif name=='nonadjacent-duplicate':assert 'source map duplicate path' in (root/(name+'.stderr')).read_text()
 else:assert 'whole map pin differs' in (root/(name+'.stderr')).read_text()
 records.append(dict(name=name,successExpected=success,returncode=child.returncode,readyObservedBeforeInput=True,result=result,inputBytes=len(wire),inputSha256=hashlib.sha256(wire).hexdigest()))
dest.write_text(json.dumps(dict(standing='NEW FIRSTPARTY ORIGINAL MAP ORDER WITH SORTED DESCRIPTOR CONTROLS; UNREVIEWED',root=str(root),controlsPassed=4,childProcesses=4,records=records,newReceiverActualCorpusUse=False,acceptedParentUnchanged=True,originalMapWholeHashPreserved=True,descriptorSortedByRawUTF8=True,sourceAuthentication=False,nativeAdmission=False,SM7Complete=False,SMComplete=False),indent=2)+'\n');print('Four new map-order/descriptor controls pass; no new receiver corpus use or parent control rerun.')
