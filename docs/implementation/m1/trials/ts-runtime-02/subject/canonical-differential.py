from pathlib import Path
import importlib.util
import hashlib
import json

here = Path(__file__).parent
arch = Path('/Users/sb/code/opensip-ai/opensip_arch')
path = arch / 'docs/coop/design-corrections/foundation/canonical.py'
assert hashlib.sha256(path.read_bytes()).hexdigest() == 'd47f25db0fb09ceb84282a89fdf74055cb81ccb9de26f85a5a70b032b9a6b442'
spec = importlib.util.spec_from_file_location('reference', path)
reference = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reference)
expected = []
for row in (arch / 'docs/implementation/m1/reviews/canonical-02/probes/corpus.hex').read_text().splitlines():
    try:
        expected.append('OK ' + reference.canonical(reference.parse(bytes.fromhex(row))).hex())
    except reference.AdmissionError:
        expected.append('REFUSE')
actual = (here / 'ts-outcomes.txt').read_text().splitlines()
mismatches = [i for i, (a, b) in enumerate(zip(actual, expected)) if a != b]
result = dict(cases=len(actual), referenceCases=len(expected), mismatches=mismatches,
              passed=len(actual)==len(expected) and not mismatches, productQualification=False)
(here / 'differential.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result))
assert result['passed']
