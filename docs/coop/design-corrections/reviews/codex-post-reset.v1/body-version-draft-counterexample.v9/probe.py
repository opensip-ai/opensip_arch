"""Codex draft-binding representation counterexample; schema/projection only, not a full Run bypass."""
from pathlib import Path
import ast,copy,hashlib,json
root=Path.cwd();dc=root/'docs/coop/design-corrections';out=dc/'reviews/codex-post-reset.v1/body-version-draft-counterexample.v9';out.mkdir(exist_ok=False);sha=lambda p:hashlib.sha256(p.read_bytes()).hexdigest()
paths=['docs/coop/design-corrections/foundation/identity-schemas.v2.json','docs/coop/design-corrections/foundation/identity-model.py','docs/coop/design-corrections/native/native-evidence.schemas.v2.json','docs/v2/contracts/product-v1/native-evidence.md','docs/coop/artifacts/fact-identity-policy.v2.json'];captured=[]
for rel in paths:
 p=root/rel;q=out/'source-images'/rel;q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(p.read_bytes());captured.append({'path':rel,'sha256':sha(q),'bytes':q.stat().st_size})
ids=json.loads((out/'source-images'/paths[0]).read_text());native=json.loads((out/'source-images'/paths[2]).read_text());row=ids['x-opensip-digest-domains']['domainSets']['native-semantic-universe']['native.semantic-universe.rust.v2'];assert row['languageVersionBinding']==['edition'],'Draft already changed: inspect new law before using this probe'
mp=dc/'reviews/candidate-subject.v8.json';m=json.loads(mp.read_text());base=Path(m['snapshotRoot']);f=base/'docs/coop/design-corrections/foundation/check-identity.py';source=f.read_text();tree=ast.parse(source);last=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='graph_with_import').end_lineno;ns={'__file__':str(f),'__name__':'frozen_control'};exec(compile('\n'.join(source.split('\n')[:last]),str(f),'exec'),ns);M,C=ns['M'],ns['C'];r,o,b=ns['build'](has_match=True,universe_language='rust');M.close_run(r,o,b)
universe=None
for raw in b.values():
 try:domain,value,_=M.parse_h_frame(raw,'native-semantic-universe')
 except Exception:continue
 if domain=='native.semantic-universe.rust.v2':universe=value;break
assert universe is not None
large=copy.deepcopy(universe);large['edition']={**large['edition'],**{'ordinary_workspace_crate_'+str(i):2021 for i in range(20)}}
C.validate({'$defs':native['$defs'],'$ref':'#/$defs/RustUniverseV2ResolvedInputs'},large)
component=C.canonical({field:large[field] for field in row['languageVersionBinding']});assert len(component)>255
result={'standing':'Codex coauthor draft representation check, NOT a completed Run bypass or independent review','baselineFrozenV8RunCloses':True,'expandedRustUniverseSchemaAdmitted':True,'editionEntries':len(large['edition']),'languageVersionComponentBytes':len(component),'inheritedComponentMaximumBytes':255,'fitsInheritedFrame':False,'observedDraftBinding':row['languageVersionBinding'],'largeUniverse':large,'versionComponentHex':component.hex(),'limitation':'The expanded universe is validated against the captured native schema; no whole expanded native admission/Run/clone commit is claimed. This demonstrates that the declared raw-C component recipe cannot encode a schema-admitted input in the inherited u8 frame.'}
(out/'result.json').write_text(json.dumps(result,indent=2)+'\n');(out/'probe.py').write_bytes(Path(__file__).read_bytes());(out/'custody.json').write_text(json.dumps({'standing':'Exact in-progress source images captured for the draft concern; no final-source claim','files':captured,'allLiveSourcesUnchangedDuringProbe':all(sha(root/v['path'])==v['sha256'] for v in captured),'frozenBaseManifestSha256':sha(mp),'productQualification':False},indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ('largeUniverse','versionComponentHex')}))
