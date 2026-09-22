from pathlib import Path
import hashlib,importlib.util,json,shutil,subprocess
T=Path('/tmp/opensip-implementation');A=Path('/Users/sb/code/opensip-ai/opensip_arch');L=A.parent/'opensip';D=T/'initial-diagnostics-generation404';P=D/'product'
def dig(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def save(p,v):p.write_text(json.dumps(v,indent=2)+'\n')
assert not(D/'preparation.json').exists()
assert subprocess.check_output(['git','status','--porcelain'],cwd=L)==b''
for r in json.loads((D/'baseline.json').read_text())['files']:
 assert dig((L/r['path']).read_bytes())=={k:r[k]for k in ('bytes','sha256')}
candidate=(P/'schemas/sources/common-v4.schema.json').read_bytes()
build=json.loads((T/'contracts-generator-rebuild-403/receipt.json').read_text());old_build=json.loads((L/'tools/contracts/build-receipt.json').read_text());toolchain=json.loads((P/'tools/contracts/toolchain.json').read_text())
closure_original=json.loads((L/'tools/contracts/generator-closure.json').read_text());materialized=[]
for r in closure_original['files']:
 p=P/r['path']
 if p.exists():continue
 b=(L/r['path']).read_bytes();assert dig(b)=={k:r[k]for k in ('bytes','sha256')}
 p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b);shutil.copymode(L/r['path'],p);materialized.append(r)
save(D/'ignored-generator-dependencies.json',{'standing':'Exact selected build dependencies are materialized ignored files, not tracked product source. First preparation copied tracked files only and stopped before generation when these were absent; nothing live changed.','files':materialized})
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
