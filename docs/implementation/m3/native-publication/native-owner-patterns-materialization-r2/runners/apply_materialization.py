from pathlib import Path
import os, json, hashlib, subprocess, re
assert os.environ.get('OPENSIP_LEAD_HOLDS_LANE_LOCK') == '1'
F=Path(__file__).parent
P=Path('/Users/sb/code/opensip-ai/opensip'); A=P.parent/'opensip_arch'; W=P.parent/'opensip-native-owner-patterns-takeover'
B=F/'source-design-r1'; integration=json.loads((B/'integration.json').read_text())
def git(root,*args): return subprocess.check_output(['/usr/bin/git','-C',str(root),*args],text=True).strip()
def check(path,pin):
 raw=path.read_bytes(); assert len(raw)==pin['bytes'] and hashlib.sha256(raw).hexdigest()==pin['sha256'],str(path)
 return raw
assert git(P,'rev-parse','HEAD')==integration['productLock']
assert git(A,'rev-parse','HEAD')==integration['architecture']
assert not git(P,'status','--porcelain')
assert git(W,'rev-parse','HEAD')=='21306d28b4c0508d9219d53b428dd84163c7567d'
rows=json.loads((F/'preflight-r3/product-map.json').read_text())['rows']
assert sorted(git(W,'diff','--name-only').splitlines())==sorted(r['path'] for r in rows)
for row in rows: check(W/row['path'],row['candidate'])
assert git(P,'diff','--name-only','HEAD^','HEAD')=='design-lock.json'
subprocess.run(['/usr/bin/git','-C',str(W),'checkout','-q','--detach',integration['productLock']],check=True)
prefix='docs/implementation/m3/native-publication/native-owner-patterns-source-r1'
audit=json.loads((A/prefix/'audit.json').read_text())
for row in audit['sourceChanges']:
 assert (W/row['productPath']).read_bytes()==check(A/row['source']['path'],row['source'])
for row in audit['metadataProductMap']:
 (W/row['productPath']).write_bytes(check(A/row['candidate']['path'],row['candidate']))
path=W/'crates/identity/src/schema_registry.rs'; text=path.read_text()
for pin in audit['compiledPinUpdatesStillRequired']:
 pattern=r'(SourcePin \{\s*id: "'+re.escape(pin['schemaId'])+r'",\s*path: "'+re.escape(pin['productPath'])+r'",\s*bytes: )(\d+)(,\s*sha256: \[)([\s\S]*?)(\],\s*\})'
 matches=list(re.finditer(pattern,text)); assert len(matches)==1
 m=matches[0]; before=next(r['before'] for r in audit['sourceChanges'] if r['productPath']==pin['productPath'])
 assert int(m[2])==before['bytes']
 assert bytes(map(int,re.findall(r'\d+',m[4]))).hex()==before['sha256']
 replacement=m[1]+str(pin['bytes'])+m[3]+'\n            '+', '.join(str(b) for b in bytes.fromhex(pin['sha256']))+',\n        '+m[5]
 text=text[:m.start()]+replacement+text[m.end():]
path.write_text(text)
subprocess.run(['/opt/homebrew/Cellar/rust/1.95.0/bin/rustfmt','--edition','2024',str(path)],check=True)
changed=git(W,'diff','--name-only').splitlines()
report=dict(productBase=integration['productLock'],architecture=integration['architecture'],paths=changed,
 pins={p:dict(bytes=(W/p).stat().st_size,sha256=hashlib.sha256((W/p).read_bytes()).hexdigest()) for p in changed},
 selectedDesignBound=True,compiledPinsUpdated=2,metadataFilesCopied=5,generatorExecuted=False,unitAccepted=False)
(F/'materialization-applied.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
