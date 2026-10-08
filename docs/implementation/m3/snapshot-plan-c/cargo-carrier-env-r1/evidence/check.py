"""Read-only existing symbolic native carrier controls; no Cargo or OS observation."""
from pathlib import Path
import argparse, importlib.util, json, sys

parser = argparse.ArgumentParser()
parser.add_argument('--architecture', type=Path, required=True)
parser.add_argument('--deps', type=Path, required=True)
args = parser.parse_args()
sys.path.insert(0, str(args.deps))
spec = importlib.util.spec_from_file_location('native_model', args.architecture / 'docs/coop/design-corrections/native/native_evidence_model.v2.py')
model = importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)
cases = []
environments = [('private-empty', {'CARGO_HOME':'<private-empty>'}), ('missing', {}), ('ambient-home', {'CARGO_HOME':'/ambient/not-read'}), ('cargo-override', {'CARGO_HOME':'<private-empty>', 'CARGO_TARGET_DIR':'/ambient/not-read'}), ('path', {'CARGO_HOME':'<private-empty>', 'PATH':'/ambient/not-read'}), ('rustflags', {'CARGO_HOME':'<private-empty>', 'RUSTFLAGS':'-Zunsafe'}), ('fake-private-literal', {'CARGO_HOME':'private-empty'})]
for label, environment in environments:
    result = model.cargo_config_admission([], [], environment, {'cargo':'a'*64, 'rustc':'b'*64}, {'cargo':'a'*64, 'rustc':'b'*64})
    assert result['admitted'] == (label == 'private-empty')
    cases.append({'id':label, 'symbolicEnvironment':environment, 'result':result})
report = {'standing':'Existing native reference function, symbolic values only; no environment mutation, Cargo launch, filesystem observation, custody proof or product qualification', 'positive':1, 'negative':6, 'cases':cases, 'productImplemented':False, 'productQualification':False}
assert json.loads((Path(__file__).parent / 'reference-controls.json').read_text()) == report
print('Existing symbolic private-home exception admits once and refuses six malformed environments; no OS/product controls asserted.')
