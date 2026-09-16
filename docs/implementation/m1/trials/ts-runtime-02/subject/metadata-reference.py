from pathlib import Path
import importlib.util
import json

arch = Path('/Users/sb/code/opensip-ai/opensip_arch')
path = arch / 'docs/implementation/m1/metadata-v2/check_metadata.py'
spec = importlib.util.spec_from_file_location('metadata', path)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
reference, registry, documents = module.load(arch)
fixtures = json.loads((path.parent / 'fixtures.json').read_bytes())
validator = reference.ExactValidator(documents['urn:opensip:product-v1:workflows:evaluator3:command-envelope:4'], registry=registry)
print(json.dumps([dict(id=case['id'], shape=validator.is_valid(case['value'])) for case in fixtures['cases']]))
