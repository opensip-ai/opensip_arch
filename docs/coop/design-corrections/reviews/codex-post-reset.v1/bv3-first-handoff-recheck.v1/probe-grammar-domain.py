from pathlib import Path
import importlib.util,json,copy,hashlib
root=Path(__file__).parent/'work';dc=root/'docs/coop/design-corrections';p=dc/'integration-fixtures.py';s=importlib.util.spec_from_file_location('root_grammar_fixture',p);f=importlib.util.module_from_spec(s);s.loader.exec_module(f)
run,objects,blobs=f.build(universe_language='syntax',relation='file',source_path='README.md')
control=f.M.close_run(run,objects,blobs)
plan=objects[run['planId']][1]
contexts=[f.M.parse_h_frame(blobs[x],'native-context') for x in plan['nativeContextDigests']]
context=next(v for domain,v,row in contexts if domain=='native.context.syntax.v2');bundle=context['grammarBundle'];rows=[]
for language,suffix in [('typescript','.ts'),('javascript','.js'),('rust','.rs'),('json','.json'),('toml','.toml'),('markdown','.md'),('yaml','.yaml'),('python','.py')]:
 value=copy.deepcopy(bundle);value['grammars']=[dict(bundle['grammars'][0],languageId=language,suffixes=[suffix])]
 try:f.N.validate_native('SyntaxGrammarBundleV1',value);admitted=True;detail=None
 except Exception as exc:admitted=False;detail=type(exc).__name__+':'+str(exc)[:500]
 rows.append({'language':language,'suffix':suffix,'alreadyBundled':f.N.BUNDLED_GRAMMARS.get(suffix)==language,'grammarDescriptorAdmitted':admitted,'detail':detail})
report={'standing':'Codex independent comparison of the actual existing BUNDLED_GRAMMARS table with the new grammar-bundle descriptor vocabulary. The full README file-inventory Run is a control. Grammar descriptors use synthetic construction data; shape validation only, not a claimed admitted parser/clone Run or real grammar measurement. Existing bundled languageIds must be representable; Python is an intentionally unsupported control, not a requested extension.','sourceRoot':str(root),'inventoryControlRunId':control,'sources':[{'path':str(p.relative_to(root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [dc/'integration-fixtures.py',dc/'native/native_evidence_model.v2.py',dc/'native/native-evidence.schemas.v2.json']],'cases':rows}
p=Path(__file__).with_suffix('.json');assert not p.exists();p.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(rows,indent=2))
