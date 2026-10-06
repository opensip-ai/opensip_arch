"""Execute explicit reference fixtures and span controls; no product qualification."""
import argparse
import copy
import importlib.util
import json
import sys
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--deps', type=Path, required=True)
args = parser.parse_args()
sys.path.insert(0, str(args.deps))
here = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('component_reference', here / 'reference.py')
reference = importlib.util.module_from_spec(spec)
spec.loader.exec_module(reference)
from jsonschema import Draft202012Validator
Draft202012Validator.check_schema(json.loads((here / 'component-source-model.schema.json').read_bytes()))
fixtures = json.loads((here / 'fixtures.json').read_bytes())
ids, passed = set(), []
for case in fixtures.get('canonicalCases', []):
    value = 0
    for _ in range(case['containers']):
        value = [value]
    try:
        reference.exact_json(value)
    except reference.ModelError as error:
        assert not case['admissible'] and str(error) == case['error'], case['id']
    else:
        assert case['admissible'], case['id']
    passed.append(case['id'])
for case in fixtures['cases']:
    assert case['id'] not in ids
    ids.add(case['id'])
    original = bytes.fromhex(case['sourceHex'])
    snapshot = {'snapshotId': 'snapshot2:' + 'a' * 64, 'files': {'source': original}}
    closure = 'closure2:' + 'b' * 64
    regions, blobs = copy.deepcopy(case['regions']), {}
    for row in regions:
        if row['derived'] is not None:
            derived = row['derived']
            content = bytes.fromhex(derived.pop('contentHex'))
            derived['sha256'] = reference.digest(content)
            derived['byteLength'] = len(content)
            blobs[derived['sha256']] = content
    record = {'schemaVersion': 1, 'snapshotId': snapshot['snapshotId'],
              'source': {'path': 'source', 'contentSha256': reference.digest(original), 'byteLength': len(original)},
              'producerClosureId': closure, 'format': case['format'],
              'state': 'complete' if all(row['state'] == 'complete' for row in regions) else 'partial',
              'regions': regions}
    for change in case['changes']:
        target = record
        for part in change['path'][:-1]:
            target = target[part]
        target[change['path'][-1]] = change['value']
    if case.get('omitDerivedRetention'):
        blobs.clear()
    expected = case['expected']
    try:
        result = reference.validate(record, snapshot, {closure}, blobs)
    except reference.ModelError as error:
        assert not expected['admissible'] and str(error) == expected['error'], (case['id'], str(error))
    else:
        assert expected['admissible'], case['id']
        assert result['semanticCompleteness'] == 'not-established' and result['repairAuthority'] is False
        for span in expected['spans']:
            try:
                translated = reference.exact_original_span(record['regions'][span['regionId']], span['start'], span['end'], original, blobs)
            except reference.ModelError as error:
                assert span.get('error') == str(error), (case['id'], str(error))
            else:
                assert 'error' not in span
                actual = None if translated is None else list(translated)
                assert actual == span['original'], (case['id'], actual)
    passed.append(case['id'])
print(json.dumps({'referenceCases': len(passed), 'passed': passed, 'productQualification': False}))
