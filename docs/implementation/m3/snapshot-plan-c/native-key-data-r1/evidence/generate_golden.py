from pathlib import Path
import json,hashlib
B=Path(__file__).resolve().parent
def canonical(v):return json.dumps(v,ensure_ascii=False,separators=(',',':')).encode('utf-8')
def key(prefix,v):return prefix+hashlib.sha256(canonical(v)).hexdigest()
cases=[('a','1','', 'snapshot-member','path','Cargo.toml'),('a','1','', 'dependency-closure-member','path','nested/Cargo.toml'),('pkg','1.2.3','registry+https://example.invalid/index','dependency-closure-member','registry',None),('λ\n"','arbitrary version','git+https://example.invalid/r?branch=m#raw','dependency-closure-member','git',None),('e\u0301','é','原'*4,'dependency-closure-member','vendored',None)]
rows=[]
for n,v,s,c,k,p in cases:
 pkg=[n,v,s];pk=key('pkg1-',pkg);own=[c,pk,p]
 rows.append(dict(name=n,version=v,sourceId=s,source=c,sourceKind=k,snapshotManifestPath=p,packagePreimage=canonical(pkg).decode(),packageKey=pk,ownerPreimage=canonical(own).decode(),ownerKey=key('own2-',own)))
b=(json.dumps(dict(schemaVersion=1,vectors=rows),ensure_ascii=False,indent=2)+'\n').encode();p=B/'fixtures/golden.json'
if p.exists():assert p.read_bytes()==b
else:p.write_bytes(b)
print('Five independent Python raw canonical package/owner recipes verified')
