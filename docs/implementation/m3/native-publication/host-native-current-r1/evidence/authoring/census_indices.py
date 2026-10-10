from pathlib import Path
import json,hashlib
P=Path('/Users/sb/code/opensip-ai/opensip');B=Path(__file__).resolve().parent;path=P/'crates/host/tests/fixtures/native-context-fixtures.json';f=json.loads(path.read_bytes());common={r['id']:r for packet in f['bodyIdentity'].values()for r in packet['objects']};bcommon={d:f['bodyIdentityBlobs'][d]for packet in f['bodyIdentity'].values()for d in packet['blobDigests']}
for name in ['capabilitySupport','coverageProducer']:
 for case in f[name].values():
  for row in case['request']['objects']:common[row['id']]=row
for name in ['capabilitySupportBlobs','coverageProducerBlobs']:bcommon.update(f[name])
view=dict(common);view.update(f['viewJoinObjects']);vblobs=dict(bcommon);vblobs.update(f['viewJoinBlobs']);run=dict(view);run.update(f['runLinkObjects']);rblobs=dict(vblobs);rblobs.update(f['runLinkBlobs']);rows=[]
for name,objects,blobs in [('viewJoins',view,vblobs),('runLinks',run,rblobs)]:
 object_keys=sorted(objects);blob_keys=sorted(blobs)
 for label,case in f[name].items():
  request=case['request'];selectedObjects=[object_keys[i]for i in request['objectIndices']];selectedBlobs=[blob_keys[i]for i in request['blobIndices']];rows.append({'group':name,'label':label,'objectIdsInRequestedOrder':selectedObjects,'blobDigestsInRequestedOrder':selectedBlobs,'objectPoolCardinality':len(object_keys),'blobPoolCardinality':len(blob_keys)})
output={'standing':'EXACT HISTORICAL INDEX-TO-OBJECT/BLOB WITNESS; NO FIXTURE CHANGE','nativeFixtureSha256':hashlib.sha256(path.read_bytes()).hexdigest(),'cases':rows,'indexedSelections':2*len(rows)};assert output['indexedSelections']==116;(B/'native-index-witness.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({'viewJoins':sum(r['group']=='viewJoins'for r in rows),'runLinks':sum(r['group']=='runLinks'for r in rows),'indexedSelections':output['indexedSelections'],'allIndicesInRange':True},indent=2))
