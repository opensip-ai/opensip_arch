"""Prepare prospective generation; never select or modify the live product."""
from pathlib import Path
import hashlib, importlib.util, json, shutil, subprocess
T=Path('/tmp/opensip-implementation');A=Path('/Users/sb/code/opensip-ai/opensip_arch');L=A.parent/'opensip';D=T/'initial-diagnostics-generation404';P=D/'product';assert not D.exists();P.mkdir(parents=True)
def dig(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
assert subprocess.check_output(['git','status','--porcelain'],cwd=L)==b''
base=[]
for name in sorted(subprocess.check_output(['git','ls-files','-z'],cwd=L).decode().split('\0')):
 if not name:continue
 b=(L/name).read_bytes();p=P/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);shutil.copymode(L/name,p);base.append({'path':name,**dig(b)})
assert len(base)==592
save(D/'baseline.json',{'productHead':subprocess.check_output(['git','rev-parse','HEAD'],cwd=L,text=True).strip(),'files':base})
candidate=(T/'initial-root-binding402/diagnostic-draft/common.schema.json').read_bytes();old=(P/'schemas/sources/common-v4.schema.json').read_bytes();assert dig(old)['sha256']=='6af81f35c53ce74acbb0609d50524ab9d0b0ae1c2b772e9581dfb9f8535eaed9'
(P/'schemas/sources/common-v4.schema.json').write_bytes(candidate)
source_map=json.loads((P/'schemas/source-map.json').read_text());matches=[r for r in source_map['sources']if r['implementationPath']=='schemas/sources/common-v4.schema.json'];assert len(matches)==1
matches[0]['architectureSource']={'path':'docs/implementation/m2/initial-root-binding-owner-selection-v1/schemas/common.v4.schema.json',**dig(candidate)};save(P/'schemas/source-map.json',source_map)
build=json.loads((T/'contracts-generator-rebuild-403/receipt.json').read_text());old_build=json.loads((P/'tools/contracts/build-receipt.json').read_text())
assert build['sources']==old_build['sources']and build['dependencies']==old_build['dependencies']and build['builder']==old_build['builder']and build['tools']==old_build['tools'];save(P/'tools/contracts/build-receipt.json',build)
toolchain=json.loads((P/'tools/contracts/toolchain.json').read_text());toolchain['executables']['generator']=build['executable'];toolchain['standing']='Observed offline rebuild403 of identical generator sources/dependencies/compiler; development pins, no reproducible-build or release qualification';save(P/'tools/contracts/toolchain.json',toolchain)
closure=json.loads((P/'tools/contracts/generator-closure.json').read_text());closure_changes=[]
for row in closure['files']:
 current={'path':row['path'],**dig((P/row['path']).read_bytes())}
 if current!=row:closure_changes.append({'path':row['path'],'before':dict(row),'after':current});row.update(current)
closure['toolchain']=toolchain['executables'];save(P/'tools/contracts/generator-closure.json',closure)
expected={'tools/verify_design.py','tools/contracts/build-receipt.json','tools/contracts/toolchain.json','schemas/source-map.json','schemas/sources/common-v4.schema.json'}
assert {r['path']for r in closure_changes}==expected
registry=json.loads((P/'schemas/registry.json').read_text());rows=[r for r in registry['sources']if r['sourcePath']=='schemas/sources/common-v4.schema.json'];assert len(rows)==1;rows[0]['sourceSha256']=dig(candidate)['sha256']
assert len(registry['recipes'])==1;r=registry['recipes'][0];r['generatorClosureSha256']=dig((P/'tools/contracts/generator-closure.json').read_bytes())['sha256'];r['sourceSha256s']=sorted(x['sourceSha256']for x in registry['sources']);save(P/'schemas/registry.json',registry)
spec=importlib.util.spec_from_file_location('candidate_adapter',P/'tools/contracts/adapter.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module);module.validate_build_receipt(build,{r['path']:(P/r['path']).read_bytes()for r in closure['files']},toolchain['executables']['generator'])
save(D/'preparation.json',{'standing':'Mutable prospective generation input; unselected/unreviewed, no product mutation. Planned architecture source path must be created and formally reviewed before selected generation can run.','sourceSchemas':40,'candidateCodes':319,'closureFiles':len(closure['files']),'closureChanges':closure_changes,'generatorSourcesDependenciesBuilderCompilerUnchanged':True,'newGeneratorBinary':build['executable'],'oldGeneratorBinary':old_build['executable'],'buildReceiptValidationPassed':True,'liveProductUnchanged':True,'productionEntryPointNotBypassedForActivation':True})
print('Prepared404 prospective generation:40schemas,349closureinputs,5explicit closure changes, live product unchanged')
