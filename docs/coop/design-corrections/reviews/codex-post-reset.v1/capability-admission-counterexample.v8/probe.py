from pathlib import Path
import json,hashlib,importlib.util,copy,shutil
root=Path.cwd();dc=root/'docs/coop/design-corrections';out=dc/'reviews/codex-post-reset.v1/capability-admission-counterexample.v8';out.mkdir(exist_ok=False)
sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest();paths=[dc/'native/native_evidence_model.v2.py',dc/'native/capability-manifest-domains.v2.json',dc/'native/native-evidence.schemas.v2.json',dc/'foundation/identity-model.py',dc/'foundation/identity-schemas.v2.json',dc/'foundation/relation-payload-schemas.v2.json',dc/'foundation/canonical.py'];rows=[]
for p in paths:
 q=out/'source'/p.relative_to(root);q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);rows.append({'path':str(p.relative_to(root)),'sha256':sha(p),'bytes':p.stat().st_size})
p=dc/'native/native_evidence_model.v2.py';s=importlib.util.spec_from_file_location('capability_probe',p);N=importlib.util.module_from_spec(s);s.loader.exec_module(N)
v=json.loads((root/'docs/coop/artifacts/delivery.v4.json').read_text());recipe=next(r['value'] for r in v['derivedFrom']['operations'] if r['path']=='capabilityManifestIdentity');raw=bytes.fromhex(recipe['vectors']['byId']['DCM-1-core']['committedBytesHex']);value=N.cve1_decode(raw);results=[]
for name,change in [('boolean-schema-version',lambda v:v.update(schemaVersion=True)),('duplicate-platform-id',lambda v:v['providers'][0]['platformIds'].append(v['providers'][0]['platformIds'][0])),('duplicate-provider',lambda v:v['providers'].append(copy.deepcopy(v['providers'][0])))]:
 bad=copy.deepcopy(value);change(bad);res=N.admit_capability_manifest(N.cve1_encode(bad));results.append({'id':name,'input':bad,'outcome':res,'expected':'REFUSE under inherited ADM-TYPE / strict unique ADM-ORDER'})
for row in rows:assert sha(root/row['path'])==row['sha256'],'Concurrent source changed; do not claim exact source capture'
(out/'result.json').write_text(json.dumps({'standing':'Codex in-progress coauthor admission counterexamples, not independent acceptance. Same current module before/after source hashes verified.','sources':rows,'inheritedRecipe':'docs/coop/artifacts/delivery.v4.json#derivedFrom.operations[17].value.admission / orderingRuling','positive':N.admit_capability_manifest(raw),'vectors':results,'productQualification':False},indent=2)+'\n');(out/'probe.py').write_bytes(Path(__file__).read_bytes());print(json.dumps(results))
