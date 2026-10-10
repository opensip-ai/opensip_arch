from pathlib import Path
import struct,json,hashlib,subprocess,tempfile,os
B=Path('/tmp/opensip-implementation');V=B/'sm-dependency-map-transfer-2026-10-10';dest=V/'controls-r1.json';assert not dest.exists();os.setpriority(os.PRIO_PROCESS,0,10);root=Path(tempfile.mkdtemp(prefix='opensip-sm-map-transfer-controls-',dir='/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T'));root.chmod(0o700)
def u64(n):return struct.pack('>Q',n)
def frame(b):return struct.pack('>I',len(b))+b
def source_map(rows):return b'OPSMRUST1\0'+u64(len(rows))+b''.join(u64(len(name))+name+u64(len(content))+content for name,content in rows)
def wire(raw,pin=None,chunk=1048576):
 h=dict(format='OPSMRUST1',bytes=len(raw),sha256=pin or hashlib.sha256(raw).hexdigest());return frame(json.dumps(h).encode())+b''.join(frame(raw[i:i+chunk]) for i in range(0,len(raw),chunk))
rows=[(b'/synthetic/empty.rs',b''),(b'/synthetic/large.rs',b'x'*(1048576+19))];raw=source_map(rows);cases=[('split-content-and-empty-file',wire(raw),True),('one-byte-frames',wire(source_map([(b'/x.rs',b'abc')]),chunk=1),True),('whole-map-corruption',wire(raw,pin='0'*64),False),('oversized-frame',struct.pack('>I',1048577),False),('truncated-payload',wire(raw)[:-1],False),('trailing-input',wire(raw)+b'x',False),('duplicate-map-path',wire(source_map([(b'/x.rs',b'a'),(b'/x.rs',b'b')])),False),('unsorted-map-path',wire(source_map([(b'/z.rs',b'a'),(b'/a.rs',b'b')])),False),('row-bound',wire(b'OPSMRUST1\0'+u64(100001)),False)]
records=[];home=os.environ.get('HOME')
for name,data,success in cases:
 env={'TMPDIR':str(root)};p=subprocess.run(['/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14','-I','-B',str(V/'receiver.py')],input=data,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env,timeout=30);(root/(name+'.stdout')).write_bytes(p.stdout);(root/(name+'.stderr')).write_bytes(p.stderr);assert (p.returncode==0)==success,(name,p.stderr)
 result=json.loads(p.stdout) if success else None
 if name=='split-content-and-empty-file':assert result['rows']==2 and result['contentBytes']==1048576+19 and result['contentFrames']==2
 if name=='one-byte-frames':assert result['contentFrames']==len(source_map([(b'/x.rs',b'abc')]))
 records.append(dict(name=name,returncode=p.returncode,successExpected=success,result=result,inputBytes=len(data),inputSha256=hashlib.sha256(data).hexdigest()))
assert os.environ.get('HOME')==home and not Path('/Users/sb/Library/Application Support/OpenSIP').exists();dest.write_text(json.dumps(dict(standing='NEW FIRSTPARTY FRAMED SOURCE MAP TRANSFER CONTROLS; UNREVIEWED; NO CORPUS',root=str(root),controlsPassed=len(records),childProcesses=len(records),records=records,sourceAuthentication=False,nativeAdmission=False,repositoryCodeExecuted=False,SMComplete=False),indent=2)+'\n');print('Nine new framed map transfer controls pass; no corpus/compiler/application execution.')
