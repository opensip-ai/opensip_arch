from pathlib import Path
import ast,hashlib,json,importlib.util
B=Path(__file__).resolve().parent;A=Path('/Users/sb/code/opensip-ai/opensip_arch');p=A/'docs/implementation/m3/native-successors-fa/rust3-lim/evidence/build_rust3_lim.py';tree=ast.parse(p.read_text());ns={'hashlib':hashlib};exec(compile(ast.Module(body=[n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name in ['head','cbor','domain_hash','subjects_from']],type_ignores=[]),str(p),'exec'),ns);spec=importlib.util.spec_from_file_location('codec',B/'scope_codec.py');codec=importlib.util.module_from_spec(spec);spec.loader.exec_module(codec);v=json.loads((p.parent/'vectors.json').read_text());rows=[]
a=ns['subjects_from'](v['snapshotId'],v['manifestEntries']);b=codec.derive(v['snapshotId'],v['manifestEntries']);assert a==b==v['subjects'];assert ns['cbor'](a)==codec.encode(b);assert ns['domain_hash']('opensip.rust-provider.subject-scope.v2',a)==codec.commitment('opensip.rust-provider.subject-scope.v2',b)==v['subjectScopeCommitment'];domain={'subjects':a,'requestedCoverageDomain':v['stageRequestV3ByReference']['analysisDomain']['requestedCoverageDomain']};assert ns['domain_hash']('opensip.rust-provider.analysis-domain.v2',domain)==codec.commitment('opensip.rust-provider.analysis-domain.v2',domain)==v['domainCommitment'];rows.append(dict(case='exact closed synthetic vector identities/CBOR/domain',passed=True))
for label,entries in [('empty',[]),('duplicate',v['manifestEntries']+[v['manifestEntries'][2]])]:
 outcomes=[]
 for f in [ns['subjects_from'],codec.derive]:
  try:f(v['snapshotId'],entries)
  except (ValueError,SystemExit)as error:outcomes.append(str(error))
  else:raise AssertionError(label)
 rows.append(dict(case=label,refusals=outcomes,passed=True))
for sample in [{'é':'unicode','a':True,'long key':None},[0,23,24,255,256,65535,65536,4294967295,4294967296,2**64-1]]:assert ns['cbor'](sample)==codec.encode(sample)
rows.append(dict(case='CBOR UTF8 length-first map ordering and uint64 width edges',passed=True));(B/'controls.json').write_text(json.dumps(dict(standing='UNREVIEWED THROWAWAY RECIPE CONTROLS,NOT ADMISSION',controls=rows),indent=2)+'\n');print('4scope controls passed')
