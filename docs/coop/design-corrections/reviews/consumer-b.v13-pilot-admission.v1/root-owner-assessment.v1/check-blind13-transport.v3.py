"""Transport controls only; toy descriptors are not schema-admitted Runs."""
from pathlib import Path
import base64,copy,hashlib,importlib.util,json
B=Path('/tmp/opensip-design-corrections')
def module(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
M=module('transport_owner3',B/'candidate-subject.v25/docs/coop/design-corrections/foundation/identity-model.v3.py')
P=module('transport_parser3',B/'check-blind13-exported-graphs.v3.py')
sha=lambda x:hashlib.sha256(x).hexdigest()
def fixture(domain='canonical-record',aux=False,frame=False):
 d={'value':1};cx=M.C.canonical(d);dg=sha(cx) if domain=='canonical-record' else M.C.identity(domain,d);ident=dg if domain=='canonical-record' else (M.PREFIX.get(domain,'sha256')+':'+dg)
 meta={'domain':domain,'identity':ident,'canonicalBytesHex':cx.hex(),'canonicalSha256':sha(cx)};blobs={sha(cx):base64.b64encode(cx).decode()};cache=copy.deepcopy(d)
 if aux:cache['_digest']=ident
 if frame:
  raw=b'opensip.product.v1\0'+domain.encode()+b'\0'+len(cx).to_bytes(8,'big')+cx;assert sha(raw)==dg;blobs[dg]=base64.b64encode(raw).decode()
 return {'objectTable':{ident:cache},'frames':{dg:meta},'blobs':blobs},ident,dg
rows=[]
def test(name,j,accept,check=None):
 try:
  notes=[];objects,blobs=P.decode_store(json.dumps(j).encode(),M,notes)
 except Exception as e:
  assert not accept,(name,type(e).__name__,str(e));rows.append({'name':name,'passed':True,'observed':'REFUSE','reason':str(e)});return
 assert accept,name
 if check:check(objects,blobs,notes)
 rows.append({'name':name,'passed':True,'observed':'DECODE','notes':notes})
def exact_blobs(j):
 def check(objects,blobs,notes):assert blobs=={k:base64.b64decode(v) for k,v in j['blobs'].items()}
 return check
j,i,d=fixture();test('raw-exact',j,True,exact_blobs(j))
j,i,d=fixture(aux=True);test('raw-cache-bookkeeping-exact-source-unchanged',j,True,exact_blobs(j))
k=copy.deepcopy(j);k['objectTable'][i]['_digest']='0'*64;test('wrong-bookkeeping-digest',k,False)
k=copy.deepcopy(j);k['objectTable'][i]['value']=2;test('semantic-cache-mismatch-not-repaired',k,False)
k=copy.deepcopy(j);k['blobs']={};test('bookkeeping-does-not-supply-missing-bytes',k,False)
k,i,d=fixture(domain='run',aux=True,frame=True);test('typed-record-extra-field-not-stripped',k,False)
k,i,d=fixture(domain='native.context.typescript.v2');test('no-native-h-frame-manufactured',k,True,exact_blobs(k))
k,i,d=fixture(domain='native.context.typescript.v2',frame=True);test('present-native-frame-preserved-exactly',k,True,exact_blobs(k))
k=copy.deepcopy(j);key=next(iter(k['blobs']));k['blobs'][key]=base64.b64encode(b'wrong').decode();test('corrupt-source-blob-refused',k,False)
r={'standing':'Root raw transport adapter controls only. No toy descriptor is claimed to be an admitted Run. Frozen owner admission remains unchanged.','parserSha256':sha(Path(P.__file__).read_bytes()),'controls':rows,'passed':all(x['passed'] for x in rows)}
p=B/'blind13-transport-controls.v3.json';p.open('x').write(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2))
