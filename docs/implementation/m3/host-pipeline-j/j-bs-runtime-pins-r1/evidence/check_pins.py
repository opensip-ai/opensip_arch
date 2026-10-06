"""Read-only exact source-pin/policy join; no compiler or product execution."""
import argparse,pathlib,re,json,hashlib
q=argparse.ArgumentParser();q.add_argument('--product',required=True);q.add_argument('--candidate',required=True);q.add_argument('--architecture',required=True);args=q.parse_args();p=pathlib.Path(args.product);c=pathlib.Path(args.candidate);a=pathlib.Path(args.architecture)
def pin(root,rel):
 b=(root/rel).read_bytes();return dict(path=rel,bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def table(root):
 s=(root/'crates/identity/src/schema_registry.rs').read_text();rows=[]
 for id,path,n,digest in re.findall(r'SourcePin \{\s*id: "([^"]+)",\s*path: "([^"]+)",\s*bytes: (\d+),\s*sha256: \[([^\]]+)\]',s):
  raw=bytes(int(n.strip()) for n in digest.split(',') if n.strip());assert len(raw)==32;rows.append(dict(schemaId=id,sourcePath=path,bytes=int(n),sha256=raw.hex()))
 assert len(rows)==48;return rows
before=table(p);after=table(c);registry=json.loads((p/'schemas/admission-registry.json').read_bytes());assert after==registry['sources']
inv='schemas/sources/invocation-v5.schema.json';changed=[i for i in range(48) if before[i]!=after[i]];assert len(changed)==1;i=changed[0];assert before[i]['sourcePath']==after[i]['sourcePath']==inv;assert before[i]['schemaId']==after[i]['schemaId'];assert before[i]['bytes']==71161 and before[i]['sha256']=='28aa0c42b05fa3ad13ae4d9aed1bac17983453577306b8e15678dc74af63f4fb';assert after[i]['bytes']==71837 and after[i]['sha256']=='63f97dfcb77d3065c4a5f4af3194fbe0e874cc89a8b9e2533728da2a4af28ec0'
for row in after:
 assert {k:pin(c,row['sourcePath'])[k] for k in ('bytes','sha256')}=={k:row[k] for k in ('bytes','sha256')}
# Only the one SourcePin block may change in the Rust file (format included).
pattern=r'SourcePin \{\s*id: "urn:opensip:product-v1:workflows:evaluator3:invocation:5",\s*path: "schemas/sources/invocation-v5.schema.json",\s*bytes: \d+,\s*sha256: \[[^\]]+\],\s*\}'
s=(p/'crates/identity/src/schema_registry.rs').read_text();t=(c/'crates/identity/src/schema_registry.rs').read_text();assert re.sub(pattern,'INVOCATION_PIN',s)==re.sub(pattern,'INVOCATION_PIN',t)
rel='tools/identity/dependency-policy.json';old=json.loads((p/rel).read_text());new=json.loads((c/rel).read_text());r=next(x for x in new['localSources'] if x['path']=='src/schema_registry.rs');assert {k:r[k] for k in ('bytes','sha256')}=={k:pin(c,'crates/identity/src/schema_registry.rs')[k] for k in ('bytes','sha256')};r.update(next(x for x in old['localSources'] if x['path']==r['path']));assert new==old
for rel in ['schemas/admission-registry.json','schemas/admission-source-map.json','schemas/sources/invocation-v5.schema.json','crates/host/src/schema_sources.rs','tools/contracts/generator-closure.json','tools/verify_design.py']:
 assert pin(p,rel)==pin(c,rel)
print(json.dumps(dict(compiledSources=48,unchangedSourcePins=47,unchangedAliases=len(registry['aliases']),allActualSourcePinsMatch=True,onlyInvocationPinChanged=True,policyOnlyOneLocalSourcePinChanged=True,selectedSchemaUnchanged=True,hostLoaderUnchanged=True,generatorClosureUnchanged=True,consumerAdmissionNotClaimed=True,qualification=False),indent=2))
