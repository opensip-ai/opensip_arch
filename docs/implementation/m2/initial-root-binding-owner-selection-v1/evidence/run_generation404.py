from pathlib import Path
import importlib.util,json,hashlib
from types import SimpleNamespace
T=Path('/tmp/opensip-implementation');D=T/'initial-diagnostics-generation404';P=D/'product'
assert json.loads((D/'preparation.json').read_text())['buildReceiptValidationPassed']
spec=importlib.util.spec_from_file_location('prospective_pipeline404',P/'tools/contracts/pipeline.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
closure=json.loads((P/'tools/contracts/generator-closure.json').read_text())
args=SimpleNamespace(root=P,output=D/'generation',node=Path('/Users/sb/.nvm/versions/node/v24.16.0/bin/node'),generator=T/'contracts-generator-rebuild-403/opensip-contract-generator',python=Path('/opt/homebrew/Cellar/python@3.14/3.14.6/Frameworks/Python.framework/Versions/3.14/Resources/Python.app/Contents/MacOS/Python'))
provenance={'registrySha256':hashlib.sha256((P/'tools/contracts/registry.json').read_bytes()).hexdigest(),'generatorClosureSha256':hashlib.sha256((P/'tools/contracts/generator-closure.json').read_bytes()).hexdigest()}
result=m.run(args,selected_closure=closure['files'],provenance=provenance)
assert result['passed'] and not result['sourceApproved'] and not result['productModified']
