from pathlib import Path
import importlib.util,json,hashlib,shutil
B=Path('/tmp/opensip-design-corrections');F=B/'candidate-subject.v24/docs/coop/design-corrections/foundation/identity-model.v3.py'
s=importlib.util.spec_from_file_location('root_config_owner',F);M=importlib.util.module_from_spec(s);s.loader.exec_module(M);N=M.native_admission()
o=B/'blind12-root-config-export.v1';o.mkdir();rows=[]
for name,origin in [('config-synthesized.json','synthesized'),('config-custom-multi-base.json','tsconfig'),('config-js-shared-base.json','jsconfig')]:
 p=B/'consumer-b.v12-team-corrections.v2/output/vectors'/name;j=json.loads(p.read_text());g=j['graph'];digest=N.typescript_config_graph_digest(g);faults=N.typescript_config_graph_faults(g);got=N.typescript_config_origin(g)
 rows.append({'name':name,'inputSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'digest':digest,'matchesClaimedDigest':digest==j['graphDigestSha256'],'faults':faults,'origin':got,'expectedOrigin':origin,'passed':digest==j['graphDigestSha256'] and not faults and got==origin});shutil.copy2(p,o/name)
r={'standing':'Actual frozen owner stock schema, graph identity, node-kind/membership/reachability/acyclicity and origin checks on exact standalone exported graph records; not complete Run admission or config source-byte custody. No root feedback supplied to blind team.','ownerSha256':hashlib.sha256(F.read_bytes()).hexdigest(),'nativeOwnerSha256':hashlib.sha256(Path(N.__file__).read_bytes()).hexdigest(),'checks':rows,'passed':all(x['passed'] for x in rows)}
(o/'report.json').write_text(json.dumps(r,indent=2)+'\n');shutil.copy2(Path(__file__),o/Path(__file__).name);print(json.dumps(r,indent=2));assert r['passed']
