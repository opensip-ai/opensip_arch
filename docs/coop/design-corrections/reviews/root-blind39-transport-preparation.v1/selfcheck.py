"""Synthetic transport-only discrimination; no consumer inputs or semantic admission."""
import base64,copy,hashlib,importlib.util,json,types
from pathlib import Path
P=Path(__file__).parent
spec=importlib.util.spec_from_file_location('transport',P/'check-export.py');T=importlib.util.module_from_spec(spec);spec.loader.exec_module(T)
canonical=lambda v:json.dumps(v,separators=(',',':'),sort_keys=True,ensure_ascii=False).encode()
M=types.SimpleNamespace(C=types.SimpleNamespace(canonical=canonical),PREFIX={'test':'test2'})
body=canonical({'value':'retained'});frame=b'opensip.product.v1\x00test\x00'+len(body).to_bytes(8,'big')+body;h=hashlib.sha256(frame).hexdigest()
base={'objectTable':[{'domain':'test','frameSha256':h,'frameBytes':len(frame),'id':'test2:'+h}], 'blobs':{h:base64.b64encode(frame).decode()}}
rows=[]
obj,blobs,notes=T.decode(canonical(base),M);assert obj=={'test2:'+h:('test',{'value':'retained'})} and blobs[h]==frame and notes==[]
rows.append({'case':'exact-frame-positive','result':'ADMIT'})
def refusal(name,mutate):
 d=copy.deepcopy(base);mutate(d)
 try:T.decode(canonical(d),M)
 except (AssertionError,ValueError,UnicodeError):rows.append({'case':name,'result':'REFUSE'})
 else:raise AssertionError(name)
refusal('missing-frame',lambda d:d['blobs'].clear())
refusal('different-frame-bytes',lambda d:d['blobs'].update({h:base64.b64encode(frame+b'x').decode()}))
refusal('duplicate-object-id',lambda d:d['objectTable'].append(copy.deepcopy(d['objectTable'][0])))
refusal('wrong-typed-id',lambda d:d['objectTable'][0].update(id='test2:'+'0'*64))
refusal('wrong-domain',lambda d:d['objectTable'][0].update(domain='other'))
refusal('wrong-byte-count',lambda d:d['objectTable'][0].update(frameBytes=len(frame)+1))
refusal('bool-byte-count',lambda d:d['objectTable'][0].update(frameBytes=True))
refusal('embedded-record-extra',lambda d:d['objectTable'][0].update(record={'value':'invented'}))
refusal('invalid-base64',lambda d:d['blobs'].update({h:'!'}))
for name,payload in [('duplicate-json-key',b'{"objectTable":[],"objectTable":[],"blobs":{}}'),('nonjson-nan',b'{"objectTable":[],"blobs":{},"x":NaN}')]:
 try:T.decode(payload,M)
 except ValueError:rows.append({'case':name,'result':'REFUSE'})
 else:raise AssertionError(name)
print(json.dumps({'standing':'Synthetic transport checks only; no blind exports, schemas, full replay or acceptance assessed','passed':True,'count':len(rows),'checks':rows},indent=2))
