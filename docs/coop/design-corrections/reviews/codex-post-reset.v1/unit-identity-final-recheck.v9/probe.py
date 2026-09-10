from pathlib import Path
import hashlib,importlib.util,json,shutil
from jsonschema import Draft202012Validator
root=Path.cwd();dc=root/'docs/coop/design-corrections';out=dc/'reviews/codex-post-reset.v1/unit-identity-final-recheck.v9'
assert not out.exists();handoff=json.loads((dc/'reviews/digest-corrections-author.v6/handoff.json').read_text())
owned={r['path']:r['sha256'] for r in handoff['ownedFilesChanged']}
for name in ('native/native_evidence_model.v2.py','native/native-evidence.schemas.v2.json'):
 p=dc/name;assert hashlib.sha256(p.read_bytes()).hexdigest()==owned[str(p.relative_to(root))]
p=dc/'native/native_evidence_model.v2.py';spec=importlib.util.spec_from_file_location('final_unit_probe',p);N=importlib.util.module_from_spec(spec);spec.loader.exec_module(N)
schema=json.loads((dc/'native/native-evidence.schemas.v2.json').read_text());defs=schema['$defs']
v=Draft202012Validator({'$ref':'#/$defs/SourceUnitOwnershipV1','$defs':defs})
rows=[]
for label,marker in [('ordinary','crates/c-interop/Cargo.toml'),('hash-in-path','crates/c#interop/Cargo.toml'),('maximum-path','a'*(4096-len('/Cargo.toml'))+'/Cargo.toml')]:
 unit={'markerPath':marker,'crateName':'interop','targetKind':'lib','targetName':'interop','targetEdition':None};unit['unitId']=N.source_unit_id(unit)
 value={'schemaVersion':1,'enumeration':'complete','units':[unit],'selectedUnitIds':[unit['unitId']],'ownership':[{'path':'src/lib.rs','unitId':unit['unitId']}]}
 errors=[e.message for e in v.iter_errors(value)];faults=N.source_unit_ownership_faults(value,{'edition':{'interop':2021}},{marker:{},'src/lib.rs':{}})
 assert not errors and not faults,(label,errors,faults)
 assert len(unit['unitId'])==71
 rows.append({'id':label,'markerPathLength':len(marker),'record':value,'identityProjection':N.unit_identity_projection(unit),'schemaErrors':errors,'ownershipJoinFaults':faults})
assert len({r['record']['units'][0]['unitId'] for r in rows})==3
out.mkdir();sources=[]
for name in ('native/native_evidence_model.v2.py','native/native-evidence.schemas.v2.json'):
 p=dc/name;q=out/'source'/name;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(p,q);sources.append({'path':str(p.relative_to(root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'capturedPath':str(q.relative_to(out))})
shutil.copyfile(__file__,out/'probe.py')
(out/'result.json').write_text(json.dumps({'standing':'Codex final-source schema/identity/ownership-join probe, not a complete Run, independent acceptance or product qualification','vectors':rows,'sources':sources,'allPassed':True},indent=2)+'\n')
print('Three admitted path controls pass final unit schema and ownership joins with bounded derived identities.')
