"""Scoped pre-Run interruption envelope proposal; no product qualification."""
import copy
import hashlib
import types
import json
from pathlib import Path
from referencing import Registry, Resource
from referencing.jsonschema import DRAFT202012

HERE = Path(__file__).resolve().parent


def read(path):
    return json.loads(path.read_bytes())


def main():
    pins = read(HERE / 'input-pins.json')['inputs']
    pinned_bytes = {}
    for pin in pins:
        data = (HERE / pin['path']).read_bytes()
        assert len(data) == pin['bytes'] and hashlib.sha256(data).hexdigest() == pin['sha256']
        pinned_bytes[pin['path']] = data
    ref = types.ModuleType('pinned_canonical_reference')
    # Compile the verified bytes directly; -B alone would still read a matching
    # stale adjacent pyc through SourceFileLoader. No bytecode lookup occurs.
    exec(compile(pinned_bytes['inputs/canonical.py'], str(HERE / 'inputs/canonical.py'), 'exec'), ref.__dict__)
    documents = {}
    for path in sorted((HERE / 'inputs/schemas').glob('*.json')):
        doc = ref.parse(path.read_bytes())
        assert doc['$id'] not in documents
        documents[doc['$id']] = doc
    old = read(HERE / 'inputs/envelope5.json')
    current = read(HERE / 'command-envelope.v6.schema.json')
    documents[old['$id']] = old
    documents[current['$id']] = current
    registry = Registry().with_resources((key, Resource(contents={k: v for k, v in doc.items() if k != '$schema'}, specification=DRAFT202012)) for key, doc in documents.items())
    successor = read(HERE / 'successor.json')
    assert len(successor['delta']) == 1
    delta = successor['delta'][0]
    index = int(delta['selector'].split('/')[2])
    assert old['allOf'][index]['then'] == delta['before']
    assert current['allOf'][index]['then'] == delta['after']
    assert delta['after']['oneOf'][0] == delta['before']
    restored = copy.deepcopy(current)
    for key in ['$id', 'title', 'description']:
        restored[key] = old[key]
    restored['properties']['schemaMajor']['const'] = 5
    restored['allOf'][index]['then'] = delta['before']
    assert restored == old, 'unscoped old envelope change'
    results = []

    def admits(value, schema):
        try:
            ref.validate({'$ref': schema['$id']}, value, registry)
            return True
        except Exception as error:
            if type(error).__name__ not in ['ValidationError', 'AdmissionError']:
                raise
            return False

    def probe(name, value, expected=True):
        got = admits(value, current)
        assert got == expected, (name, got, expected)
        results.append({'case': name, 'accepted': got})

    base = {'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 6, 'kind': 'failure',
            'requestId': 'req1_' + 'a' * 32, 'termination': {'class': 'interrupted', 'signal': 'SIGINT'},
            'exitCode': 130, 'errors': []}
    for signal in ['SIGINT', 'SIGTERM', 'SIGHUP']:
        value = copy.deepcopy(base)
        value['termination']['signal'] = signal
        probe('before-run-' + signal, value)
        historical = copy.deepcopy(value)
        historical['schemaMajor'] = 5
        assert not admits(historical, old), 'the reported old owner gap must reproduce'
    for key in ['errors', 'requestId', 'termination', 'exitCode']:
        value = copy.deepcopy(base)
        del value[key]
        probe('missing-' + key, value, False)
    for key in ['class', 'signal']:
        value = copy.deepcopy(base)
        del value['termination'][key]
        probe('missing-termination-' + key, value, False)
    for signal in [None, '', 'SIGKILL', 'sigint', 2, True]:
        value = copy.deepcopy(base)
        value['termination']['signal'] = signal
        probe('wrong-signal-' + repr(signal), value, False)
    for code in [0, 1, 2, 3, 4, 130.0, True]:
        value = copy.deepcopy(base)
        value['exitCode'] = code
        probe('wrong-exit-' + repr(code), value, False)
    for class_name in ['success', 'policy-failed', 'request-rejected', 'operational-failed', 'indeterminate']:
        value = copy.deepcopy(base)
        value['termination'] = {'class': class_name}
        probe('empty-errors-not-interruption-' + class_name, value, False)
    for key, value in [('errorCode', 'HOST.IO_FAILURE'), ('faultCause', 'host-io'), ('reasonCodes', []), ('domainDetail', {'code': 'QUERY.VIEW_UNKNOWN'}), ('runId', 'run3:' + 'a' * 64)]:
        changed = copy.deepcopy(base)
        changed['termination'][key] = value
        probe('termination-extra-' + key, changed, False)
    for key, value in [('run', {}), ('findings', []), ('meta', {}), ('diagnostics', []), ('query', {}), ('availability', {}), ('invented', 'cancelled')]:
        changed = copy.deepcopy(base)
        changed[key] = value
        probe('new-form-no-' + key, changed, False)
    for major in [4, 5, 7]:
        changed = copy.deepcopy(base)
        changed['schemaMajor'] = major
        probe('major-' + str(major), changed, False)
    # All historical metadata fixtures retain the exact same SHAPE outcome.
    # This is not a repeat of compiled-catalog or full semantic admission checks.
    fixtures = read(HERE / 'inputs/metadata-fixtures.json')
    accepted_metadata_shapes = 0
    for case in fixtures['cases']:
        before = copy.deepcopy(case['value'])
        before['schemaMajor'] = 5
        after = copy.deepcopy(before)
        after['schemaMajor'] = 6
        before_admits = admits(before, old)
        accepted_metadata_shapes += int(before_admits)
        assert before_admits == admits(after, current), case['id']
    assert accepted_metadata_shapes > 0, 'shape compatibility needs positive controls'
    overrides = read(HERE / 'passage-overrides.json')['overrides']
    for override in overrides:
        owner = pinned_bytes['inputs/workflows-and-surfaces.md']
        assert hashlib.sha256(owner).hexdigest() == override['sourceSha256']
        lines = owner.decode().splitlines()
        span = override['selector']
        assert '\n'.join(lines[span['startLine']-1:span['endLine']]) == override['before']
    join_module = types.ModuleType('ledger_join')
    probes_module = types.ModuleType('join_probes')
    for module, name in [(join_module, 'ledger_join.py'), (probes_module, 'join_probes.py')]:
        exec(compile((HERE / name).read_bytes(), str(HERE / name), 'exec'), module.__dict__)
    join_results = probes_module.run(ref, registry, current, {
        'reportFixtures': read(HERE / 'inputs/report-fixtures04.json'),
        'inventory': read(HERE / 'inputs/inventory5.json')}, join_module)
    owner_probe_module = types.ModuleType('owner_model_probes')
    exec(compile((HERE / 'owner_model_probes.py').read_bytes(), str(HERE / 'owner_model_probes.py'), 'exec'), owner_probe_module.__dict__)
    owner_results = owner_probe_module.run(pinned_bytes['inputs/workflows_model.v1.py'], read(HERE / 'model-successor.json'),
        ref, registry, current, read(HERE / 'inputs/report-fixtures04.json'), join_module)
    print(json.dumps({'passed': True, 'pinsVerified': len(pins), 'probes': results,
                      'ledgerJoinProbes': join_results, 'exactProseOverrides': len(overrides),
                      'ownerModelProbes': owner_results,
                      'metadataShapeCompatibilityCases': len(fixtures['cases']), 'positiveMetadataShapeControls': accepted_metadata_shapes,
                      'oldConstraintsRestoredExactly': True,
                      'limits': 'schema/reference trial only; no signal handling, host cancellation/D9 semantic admission, delivery or source integration qualification'}, indent=2))


if __name__ == '__main__':
    main()
