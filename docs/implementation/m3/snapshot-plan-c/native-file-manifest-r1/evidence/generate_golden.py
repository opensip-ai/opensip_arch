from pathlib import Path
import json,hashlib
r=Path(__file__).parent;vectors=[]
for files in [[],[{'path':'src/a.rs','digestByte':7,'byteLength':3}],[{'path':'é/quote"','digestByte':255,'byteLength':18446744073709551615},{'path':'a\nfile','digestByte':0,'byteLength':0}]]:
 rows=[dict(path=f['path'],contentSha256=(bytes([f['digestByte']])*32).hex(),byteLength=f['byteLength'])for f in sorted(files,key=lambda f:f['path'].encode())];c=json.dumps(rows,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode();frame=b'opensip.product.v1\0native.dependency-file-manifest.v1\0'+len(c).to_bytes(8,'big')+c;vectors.append(dict(files=files,canonical=c.decode(),rawArraySha256=hashlib.sha256(c).hexdigest(),nativeManifestSha256=hashlib.sha256(frame).hexdigest()))
expected=(json.dumps(vectors,indent=2,ensure_ascii=False)+'\n').encode();assert(r/'golden.json').read_bytes()==expected;print('Three independent exact complete canonical-array/raw-SHA/native-frame-H vectors match retained fixture bytes.')
