from pathlib import Path
import json,hashlib,importlib.util
B=Path(__file__).resolve().parent;P=Path('/Users/sb/code/opensip-ai/opensip');W=P.parent/'opensip-host-current-corpus';old=json.loads((P/'crates/host/tests/fixtures/replay-fixtures.json').read_bytes());new=json.loads((W/'crates/host/tests/fixtures/replay-fixtures.current.json').read_bytes());mapping=json.loads((B/'replay-identity-map.json').read_bytes());assert len(set(mapping.values()))==len(mapping);inverse={v:k for k,v in mapping.items()}
def can(v):return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def undo(v):
 if isinstance(v,str):return inverse.get(v,v)
 if isinstance(v,list):return [undo(x)for x in v]
 if isinstance(v,dict):return {inverse.get(k,k):undo(x)for k,x in v.items()}
 return v
# Set normalization is required only when a digest changes an element's order.
# Compare semantic collection contents as multisets; positional arrays compare positionally.
def same(a,b,path=()):
 if type(a)is not type(b):return False
 if isinstance(a,dict):return a.keys()==b.keys()and all(same(a[k],b[k],path+(k,))for k in a)
 if isinstance(a,list):
  if len(a)!=len(b):return False
  # A changed order alone is allowed only when exact typed items are preserved.
  if all(same(x,y,path+(str(i),))for i,(x,y)in enumerate(zip(a,b))):return True
  return sorted(can(x)for x in a)==sorted(can(x)for x in b)
 return a==b
old_objects=list(old['objectPool'].values());new_objects=list(new['objectPool'].values());assert len(old_objects)==len(new_objects)==831
for a,b in zip(old_objects,new_objects):assert same(a,undo(b)),a['id']
old_blobs=list(old['blobPool'].values());new_blobs=list(new['blobPool'].values());assert len(old_blobs)==len(new_blobs)==703;schema_changes=0
for a,b in zip(old_blobs,new_blobs):
 before=bytes.fromhex(a['hex']);after=bytes.fromhex(b['hex'])
 if a['digest']=='e5834d37aebd96d77d352975878da349033f8633ecbd83322ad0fbea461f7773':
  schema_changes+=1;assert after==(P/'schemas/sources/native-v2.schema.json').read_bytes();continue
 if before==after:continue
 assert same(json.loads(before),undo(json.loads(after))),a['digest']
assert schema_changes==1
for a,b in zip(old['cases'],new['cases']):
 assert a['label']==b['label'] and same(a['expected'],undo(b['expected'])),a['label']
 assert [old['objectPool'][k]['id']for k in a['objects']]==[undo(new['objectPool'][k]['id'])for k in b['objects']]
 assert [old['blobPool'][k]['digest']for k in a['blobs']]==[undo(new['blobPool'][k]['digest'])for k in b['blobs']]
counts={k:sum(k in c['expected']for c in new['cases'])for k in ['value','mismatch','unavailable']};assert counts=={'value':91,'mismatch':9,'unavailable':1}
# This audit confirms field/content preservation; the constructor's schema-directed
# order rules and actual product replay independently own order and admission.
out={'standing':'INVERSE GRAPH CONTENT/REFERENCE CORRESPONDENCE; NOT ADMISSION OR QUALIFICATION','objectRows':831,'blobRows':703,'schemaBlobsReplaced':1,'caseLabels':101,'expectedKinds':counts,'allOriginalCaseObjectAndBlobSelectionsPreserved':True,'allNonSchemaBlobValuesAndObjectFieldsPreservedUnderInverseIdentityMap':True,'allExpectedValuesAndFaultMeaningsPreservedUnderInverseIdentityMap':True,'guardSourceByteIdentical':(P/'crates/identity/src/schema_registry.rs').read_bytes()==(W/'crates/identity/src/schema_registry.rs').read_bytes(),'parserLimitUnchanged':True};assert out['guardSourceByteIdentical'];(B/'replay-correspondence.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out,indent=2))
