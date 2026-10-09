"""First-party independent throwaway scope encoder. No source/profile/admission authority."""
import hashlib,io

def encode(value):
 out=io.BytesIO()
 def uint(tag,n):
  if type(n)is not int or not 0<=n<2**64:raise ValueError('uint64')
  if n<24:out.write(bytes([(tag<<5)|n]));return
  for width,additional in [(1,24),(2,25),(4,26),(8,27)]:
   if n<1<<(width*8):out.write(bytes([(tag<<5)|additional]));out.write(n.to_bytes(width,'big'));return
 def write(v):
  if v is None:out.write(b'\xf6')
  elif type(v)is bool:out.write(b'\xf5'if v else b'\xf4')
  elif type(v)is int:uint(0,v)
  elif type(v)is str:
   raw=v.encode('utf8');uint(3,len(raw));out.write(raw)
  elif type(v)is list:
   uint(4,len(v))
   for item in v:write(item)
  elif type(v)is dict:
   pairs=[]
   for key in v:
    if type(key)is not str:raise ValueError('map key must be text')
    encoded=encode(key);pairs.append((len(encoded),encoded,key))
   uint(5,len(pairs))
   for _,raw,key in sorted(pairs):out.write(raw);write(v[key])
  else:raise ValueError('unsupported value')
 write(value);return out.getvalue()

def commitment(domain,value):return 'sha256:'+hashlib.sha256(domain.encode('ascii')+b'\0'+encode(value)).hexdigest()

def derive(snapshot_id,entries):
 selected=[];paths=set()
 for entry in entries:
  if entry['kind']!='file'or not entry['path'].endswith('.rs')or entry['byteLength']==0:continue
  if entry['path']in paths:raise ValueError('duplicate path')
  paths.add(entry['path']);selected.append(entry)
 if not selected:raise ValueError('empty scope')
 selected.sort(key=lambda e:e['path'].encode('utf8'));result=[]
 for ordinal,entry in enumerate(selected):
  preimage={'snapshotId':snapshot_id,'path':entry['path'],'contentSha256':entry['contentSha256'],'byteLength':entry['byteLength']}
  subject='rust-file:'+commitment('opensip.rust-provider.subject.v2',preimage)
  result.append({'subjectOrdinal':ordinal,'subjectId':subject,'path':entry['path'],'startByte':0,'endByte':entry['byteLength']})
 return result
