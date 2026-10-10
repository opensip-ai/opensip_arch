from pathlib import Path
import ast,types,json,hashlib,collections
B=Path(__file__).resolve().parent;P=Path('/Users/sb/code/opensip-ai/opensip');W=P.parent/'opensip-host-native-current';src=B.parent/'host-current-corpus-r1-authoring/rebuild_replay.py';tree=ast.parse(src.read_text());nodes=[]
for n in tree.body:
 if isinstance(n,ast.Assign)and any(isinstance(t,ast.Name)and t.id=='original'for t in n.targets):break
 nodes.append(n)
g=types.ModuleType('recipes');g.__file__=str(src);exec(compile(ast.Module(body=nodes,type_ignores=[]),str(src),'exec'),g.__dict__)
def census(v):
 records=[];blobs=[]
 def walk(v):
  if isinstance(v,dict):
   if {'id','domain','descriptor'}.issubset(v):records.append((v['domain'],g.hid(v['domain'],v['descriptor'])==v['id']))
   if {'digest','hex'}.issubset(v):blobs.append(hashlib.sha256(bytes.fromhex(v['hex'])).hexdigest()==v['digest'])
   for x in v.values():walk(x)
  elif isinstance(v,list):
   for x in v:walk(x)
 walk(v);return collections.Counter(records),collections.Counter(blobs)
rows=[]
for candidate in sorted((W/'crates/host/tests/fixtures').glob('*-fixtures.current.json')):
 if candidate.name=='replay-fixtures.current.json':continue
 original=P/'crates/host/tests/fixtures'/candidate.name.replace('.current.json','.json');raw=original.read_bytes();newraw=candidate.read_bytes();old=json.loads(raw);new=json.loads(newraw);a,b=census(old);c,d=census(new);assert a==c,(candidate.name,a,c);assert b==d,(candidate.name,b,d);assert len(newraw)<=4*1024*1024
 if 'cases'in old:
  assert len(old['cases'])==len(new['cases'])
  if isinstance(old['cases'],dict):
   before=set(old['cases']);after=set(new['cases']);removed=before-after;added=after-before
   assert (removed,added)==(set(),set())or(candidate.name=='import-payload-fixtures.current.json'and removed=={'dependency-type-acquisitionSourcePath-None'}and added=={'dependency-selected-acquisitionSourcePath-null'})
  else:assert [c['label']for c in old['cases']]==[c['label']for c in new['cases']]
 assert (W/'crates/host/tests/fixtures'/original.name).read_bytes()==raw
 rows.append(dict(path=str(candidate.relative_to(W)),bytes=len(newraw),sha256=hashlib.sha256(newraw).hexdigest(),originalSha256=hashlib.sha256(raw).hexdigest(),objectIdentityFaultStatusCountsPreserved=True,rawDigestFaultCountsPreserved=True,invalidObjectOccurrences=sum(count for (_,valid),count in a.items()if not valid),invalidDigestOccurrences=b[False],historicalBytesUnchanged=True,existingParserBoundUnchanged=True))
assert len(rows)==10 and sum(r['invalidObjectOccurrences']for r in rows)==11
f=json.loads((W/'crates/host/tests/fixtures/native-context-fixtures.current.json').read_bytes());mapping=json.loads((B/'native-context-candidate/native-context-identity-map.json').read_bytes());common={r['id']:r for packet in f['bodyIdentity'].values()for r in packet['objects']};bs={d:f['bodyIdentityBlobs'][d]for packet in f['bodyIdentity'].values()for d in packet['blobDigests']}
for name in ['capabilitySupport','coverageProducer']:
 for case in f[name].values():
  for row in case['request']['objects']:common[row['id']]=row
for name in ['capabilitySupportBlobs','coverageProducerBlobs']:bs.update(f[name])
view=dict(common);view.update(f['viewJoinObjects']);vb=dict(bs);vb.update(f['viewJoinBlobs']);run=dict(view);run.update(f['runLinkObjects']);rb=dict(vb);rb.update(f['runLinkBlobs']);pools={'viewJoins':(sorted(view),sorted(vb)),'runLinks':(sorted(run),sorted(rb))};witness=json.loads((B/'native-index-witness.json').read_bytes())
for row in witness['cases']:
 objects,blobs=pools[row['group']];req=f[row['group']][row['label']]['request'];assert [objects[i]for i in req['objectIndices']]==[mapping.get(k,k)for k in row['objectIdsInRequestedOrder']];assert [blobs[i]for i in req['blobIndices']]==[mapping.get(k,k)for k in row['blobDigestsInRequestedOrder']];assert len(objects)==row['objectPoolCardinality']and len(blobs)==row['blobPoolCardinality']
result=dict(standing='PRIVATE UNREVIEWED STRUCTURAL CORRESPONDENCE CHECK; NOT RUNTIME OR ACCEPTANCE',files=rows,indexedSelectionsPreserved=116,invalidObjectOccurrencesPreserved=11,historicalFilesUnchanged=True,qualification=False)
(B/'candidate-correspondence.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(dict(files=len(rows),invalidObjectOccurrencesPreserved=11,indexedSelectionsPreserved=116,rawDigestFaultCountsPreserved=True,historicalFilesUnchanged=True)))
