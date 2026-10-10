from pathlib import Path
B=Path(__file__).resolve().parent;s=(B/'rebuild_pooled.py').read_text();s=s.replace("out=B/'pooled-candidates'","out=B/'native-context-candidate'")
a=s.index("for name in [");b=s.index(':\n p=P/',a);s=s[:a]+"for name in ['native-context']"+s[b:]
a=s.index(' # Pool names are local');b=s.index(' data=json.dumps(new',a)
s=s[:a]+''' # Preserve the exact indexed selection population using the original witness.
 def aggregate(v):
  common={r['id']:r for packet in v['bodyIdentity'].values()for r in packet['objects']};bs={d:v['bodyIdentityBlobs'][d]for packet in v['bodyIdentity'].values()for d in packet['blobDigests']}
  for key in ['capabilitySupport','coverageProducer']:
   for case in v[key].values():
    for row in case['request']['objects']:common[row['id']]=row
  for key in ['capabilitySupportBlobs','coverageProducerBlobs']:bs.update(v[key])
  view=dict(common);view.update(v['viewJoinObjects']);vb=dict(bs);vb.update(v['viewJoinBlobs']);run=dict(view);run.update(v['runLinkObjects']);rb=dict(vb);rb.update(v['runLinkBlobs']);return {'viewJoins':(view,vb),'runLinks':(run,rb)}
 oldpools=aggregate(f);newpools=aggregate(new);indexed=0
 for group in oldpools:
  oo,ob=map(sorted,oldpools[group]);no,nb=map(sorted,newpools[group]);assert len(oo)==len(no)and len(ob)==len(nb)
  oi={k:i for i,k in enumerate(no)};bi={k:i for i,k in enumerate(nb)}
  for label,case in f[group].items():
   request=case['request'];target=new[group][label]['request'];objects=[g.mapping.get(oo[i],oo[i])for i in request['objectIndices']];blobs=[g.mapping.get(ob[i],ob[i])for i in request['blobIndices']]
   target['objectIndices']=[oi[k]for k in objects];target['blobIndices']=[bi[k]for k in blobs];assert [no[i]for i in target['objectIndices']]==objects and [nb[i]for i in target['blobIndices']]==blobs;indexed+=2
 assert indexed==116
''' +s[b:]
s=s.replace("cases=len(f['cases'])","indexedSelectionsPreserved=indexed")
(B/'rebuild_native_context.py').write_text(s);compile(s,'native-builder','exec')
