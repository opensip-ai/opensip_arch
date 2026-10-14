from pathlib import Path
import subprocess,json,hashlib,struct,os,time
# Untimed functional smoke of receiver_ne_fields.py before the r3 series (lane held briefly; nothing measured).
W=Path(__file__).resolve().parent;PY='/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14';os.setpriority(os.PRIO_PROCESS,0,10)
D=Path('/var/folders/rq/jfj79dls03s0zb6d839wcqlh0000gn/T');lane=D/'opensip-lanes.lock';owned=False
def can(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
fr=lambda b:struct.pack('>I',len(b))+b;empty=fr(can([]));sid0='sha256:'+'0'*64
e1=[dict(packageKey='k',path='a',byteLength=3,contentSha256=hashlib.sha256(b'xyz').hexdigest())]
def man(entries,sid=sid0,digest=None):d=hashlib.sha256(can(dict(dependencySourceSetId=sid,entries=entries))).hexdigest();return can(dict(dependencySourceSetId=sid,manifestSha256=digest or d,entries=entries)),d
def ch(data,sid=sid0,pk='k',path='a',index=0,offset=0):h=can(dict(dependencySourceSetId=sid,packageKey=pk,path=path,chunkIndex=index,byteOffset=offset));return fr(struct.pack('>I',len(h))+h+data)
m1,d1=man(e1);s1=dict(dependencySourceSetId=sid0,manifestSha256=d1,entryCount=1,totalBytes=3,totalChunkCount=2);good=ch(b'xy')+ch(b'z',index=1,offset=2)
snap=[dict(path='f',bytes=2,sha256=hashlib.sha256(b'hi').hexdigest())]
cases=dict(valid=empty+fr(m1)+good+fr(can(s1)),validWithSnapshot=fr(can(snap))+fr(b'hi')+fr(m1)+good+fr(can(s1)),
 depDigest=empty+fr(m1)+ch(b'xy')+ch(b'q',index=1,offset=2)+fr(can(s1)),manDigest=empty+fr(man(e1,digest='0'*64)[0])+good+fr(can(s1)),manMissing=empty+fr(can(dict(dependencySourceSetId=sid0,entries=e1)))+good+fr(can(s1)),
 sidWrong=empty+fr(m1)+ch(b'xy',sid='sha256:'+'1'*64)+ch(b'z',index=1,offset=2)+fr(can(s1)),pk=empty+fr(m1)+ch(b'xy',pk='j')+ch(b'z',index=1,offset=2)+fr(can(s1)),path=empty+fr(m1)+ch(b'xy',path='b')+ch(b'z',index=1,offset=2)+fr(can(s1)),
 gap=empty+fr(m1)+ch(b'xy')+ch(b'z',index=2,offset=2)+fr(can(s1)),offset=empty+fr(m1)+ch(b'xy')+ch(b'z',index=1,offset=1)+fr(can(s1)),emptyChunk=empty+fr(m1)+ch(b'')+good+fr(can(s1)),overrun=empty+fr(m1)+ch(b'xyzw')+fr(can(s1)),
 big=empty+fr(man([dict(e1[0],byteLength=1048577)])[0])+ch(b'x'*1048577),sealCount=empty+fr(m1)+good+fr(can(dict(s1,entryCount=2))),sealChunks=empty+fr(m1)+good+fr(can(dict(s1,totalChunkCount=1))),
 sealDigest=empty+fr(m1)+good+fr(can(dict(s1,manifestSha256='0'*64))),dup=empty+fr(man(e1+e1)[0]),grouping=empty+fr(man([dict(e1[0],path='a'),dict(e1[0],packageKey='j',path='b'),dict(e1[0],path='c')])[0]),trailing=empty+fr(m1)+good+fr(can(s1))+b'z')
while True:
 try:lane.mkdir();owned=True;break
 except FileExistsError:time.sleep(2)
try:
 out={}
 for k,data in cases.items():
  r=subprocess.run([PY,'-I','-B',str(W/'receiver_ne_fields.py')],input=data,capture_output=True);out[k]=(r.returncode,r.stderr.decode().strip().splitlines()[-1] if r.stderr else json.loads(r.stdout.splitlines()[1])['accepted']==s1)
finally:
 if owned:lane.rmdir()
for k,v in out.items():print(k,v)
assert out['valid'][0]==0 and out['validWithSnapshot'][0]==0 and all(v[0]!=0 for k,v in out.items() if not k.startswith('valid'))
print('SMOKE OK')
