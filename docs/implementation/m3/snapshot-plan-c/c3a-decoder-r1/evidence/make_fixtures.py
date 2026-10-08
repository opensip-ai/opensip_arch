from pathlib import Path
import gzip,hashlib,io,tarfile,json,shutil
P=Path('/Users/sb/code/opensip-ai/opensip-c3a-decoder/crates/host/src/archive_decoder/fixtures');P.mkdir(exist_ok=True)

def header(name,kind,size):
 h=bytearray(512);b=name.encode();h[:min(len(b),100)]=b[:100];h[124:136]=f'{size:011o}\0'.encode();h[156]=kind;h[257:265]=b'ustar  \0';h[148:156]=b' '*8;h[148:156]=f'{sum(h):06o}\0 '.encode();return bytes(h)
def archive(files,end=1024):
 out=b''
 for name,content in files:
  if len(name.encode())>100:
   payload=name.encode()+b'\0';out+=header('././@LongLink',ord('L'),len(payload))+payload+b'\0'*((-len(payload))%512)
  out+=header(name,ord('0'),len(content))+content+b'\0'*((-len(content))%512)
 return out+b'\0'*end
fixtures={}
for n,files in [('base',[('unit-1.0.0/z.txt',b'hello\n'),('unit-1.0.0/src/a.rs',b'fn main(){}'),('unit-1.0.0/empty',b'')]),('long',[('unit-1.0.0/'+('a'*110)+'/\u00e9.rs',b'long\n')]),('empty',[])]:
 raw=archive(files);b=gzip.compress(raw,mtime=0);(P/(n+'.tar.gz')).write_bytes(b);fixtures[n]=dict(packageName='unit',packageVersion='1.0.0',compressedSha256=hashlib.sha256(b).hexdigest(),compressedBytes=len(b),inflatedBytes=len(raw),contentBytes=sum(len(v)for _,v in files),files=sorted([dict(path=k[len('unit-1.0.0/'):],byteLength=len(v),contentSha256=hashlib.sha256(v).hexdigest())for k,v in files],key=lambda r:r['path'].encode()))
A=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m3/snapshot-plan-c/c3-r6-producer-evidence-r1');b=(A/'producer.crate').read_bytes();(P/'producer.crate').write_bytes(b);rows=[]
with tarfile.open(fileobj=io.BytesIO(b),mode='r:gz')as t:
 for entry in t:
  assert entry.isfile();content=t.extractfile(entry).read();rows.append(dict(path=entry.name,byteLength=len(content),contentSha256=hashlib.sha256(content).hexdigest()))
root=rows[0]['path'].split('/')[0];name,version=root.rsplit('-',1)
for row in rows:row['path']=row['path'][len(root)+1:]
fixtures['producer']=dict(packageName=name,packageVersion=version,compressedSha256=hashlib.sha256(b).hexdigest(),compressedBytes=len(b),inflatedBytes=len(gzip.decompress(b)),contentBytes=sum(r['byteLength']for r in rows),files=sorted(rows,key=lambda r:r['path'].encode()),standing='Exact original accepted pinned Cargo package producer bytes; re-used as actual decoder input, not producer/profile re-review or qualification')
(P/'expected.json').write_text(json.dumps(fixtures,indent=2)+'\n');print({k:len(v['files'])for k,v in fixtures.items()})
