from pathlib import Path
import json,hashlib
B=Path('/tmp/opensip-design-corrections');R=Path(__file__).parent;P=B/'application-stage.v45.2';S=B/'application-stage.v46'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
old=json.loads((P/'application-subject.v45.json').read_text());new=json.loads((S/'application-subject.v46.json').read_text());out={}
for key in ['files','beforeImages','support']:
 a={v['path']:v for v in old[key]};b={v['path']:v for v in new[key]};assert len(a)==len(old[key]) and len(b)==len(new[key])
 same=sorted(p for p in a.keys()&b.keys() if a[p]['sha256']==b[p]['sha256'])
 changed=[{'path':p,'beforeSha256':a[p]['sha256'],'afterSha256':b[p]['sha256']} for p in sorted(a.keys()&b.keys()) if a[p]['sha256']!=b[p]['sha256']]
 out[key]={'unchanged':len(same),'changed':changed,'added':[b[p] for p in sorted(b.keys()-a.keys())],'removed':[a[p] for p in sorted(a.keys()-b.keys())]}
assert [out[k]['unchanged'] for k in ['files','beforeImages','support']]==[187,76,242]
assert len(out['support']['changed'])==1 and len(out['support']['added'])==79 and len(out['support']['removed'])==3
assert out['support']['changed'][0]['path']=='support/staged-reference-checks.v1.json'
assert {r['path'] for r in out['support']['removed']}=={'accepted-source-application-delta.json','assembly-metadata.json','bound-review-receipt.json'}
for key,base in [('files',S/'files'),('beforeImages',S/'before'),('support',S)]:
 for row in new[key]:assert sha(base/row['path'])==row['sha256'] and (base/row['path']).stat().st_size==row['bytes']
record={'standing':'Independent root complete all-layer45-to46 delta audit; extends earlier files-only record without changing either frozen package. No review grade inferred.','priorManifestSha256':sha(P/'application-subject.v45.json'),'currentManifestSha256':sha(S/'application-subject.v46.json'),'layers':out,'removedSupportPreserved':'All three removed package-root support files remain in immutable45.2 package/archive;46 bound receipt is explicitly selected in support/application46-review-binding.v1/bound-review-receipt.json.','countClarification':'Actual support:242same+1changed+79added=322;3removed from prior246. Netgrowth76 is not79added. First root ad-hoc assertion used the reviewer draft76added count and failed; this complete manifest-derived audit corrects that assumption and preserves it as a development note.','passed':True}
(R/'audit.json').write_text(json.dumps(record,indent=2)+'\n');print({k:{'unchanged':v['unchanged'],'changed':len(v['changed']),'added':len(v['added']),'removed':len(v['removed'])} for k,v in out.items()})
