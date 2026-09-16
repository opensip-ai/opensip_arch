"""Disposable checks of actual draft row admission; no application or acceptance."""
import argparse
import copy
import hashlib
import importlib.util
import json
import shutil
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('application_rows', HERE / 'application_rows.py')
M = importlib.util.module_from_spec(spec)
spec.loader.exec_module(M)
parser = argparse.ArgumentParser()
parser.add_argument('--row-map', type=Path, required=True)
parser.add_argument('--register', type=Path, required=True)
parser.add_argument('--report', type=Path, required=True)
args = parser.parse_args()
assert not args.report.exists(), 'Preserve prior reports; choose a new output'
original = json.loads(args.row_map.read_text())
ids = [row['id'] for row in original['rows']]
observations = []
for case in ('valid-current-draft', 'stale-disposition', 'missing-row', 'duplicate-row', 'qualification-claim', 'acceptance-claim'):
    with tempfile.TemporaryDirectory(prefix='opensip-row-admission-') as temp:
        draft = Path(temp)
        reg = Path('files/docs/v2/architecture/08-decision-and-readiness-register.md')
        (draft / reg).parent.mkdir(parents=True)
        shutil.copyfile(args.register, draft / reg)
        document = copy.deepcopy(original)
        if case == 'stale-disposition':
            document['rows'][3]['disposition'] = 'major2 identity names'
        elif case == 'missing-row':
            document['rows'].pop()
        elif case == 'duplicate-row':
            document['rows'].append(copy.deepcopy(document['rows'][0]))
        elif case == 'qualification-claim':
            document['rows'][0]['productQualified'] = True
        elif case == 'acceptance-claim':
            document['rows'][0]['independentGrade'] = 'ACCEPT-DESIGN'
        (draft / 'readiness-row-map.proposed.json').write_text(json.dumps(document))
        try:
            rows = M.load_rows(draft, ids)
            observed, reason = 'ADMIT', None
        except AssertionError as error:
            observed, reason = 'REFUSE', str(error)
        expected = 'ADMIT' if case == 'valid-current-draft' else 'REFUSE'
        observations.append(dict(case=case, expected=expected, observed=observed, reason=reason, passed=observed == expected))
report = {'standing': 'Synthetic/disposable draft admission controls only; no real assembly or acceptance.', 'sourceSha256': hashlib.sha256((HERE / 'application_rows.py').read_bytes()).hexdigest(), 'checks': observations, 'passed': all(row['passed'] for row in observations)}
report['inputs'] = {'rowMapSha256': hashlib.sha256(args.row_map.read_bytes()).hexdigest(), 'registerSha256': hashlib.sha256(args.register.read_bytes()).hexdigest()}
args.report.parent.mkdir(parents=True, exist_ok=True)
args.report.write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps(report, indent=2))
raise SystemExit(not report['passed'])
