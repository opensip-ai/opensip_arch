"""Pinned reference composition checks; no native observers or product activation."""
import argparse
import ast
import copy
import hashlib
import importlib.util
import json
from pathlib import Path

from jsonschema import Draft202012Validator
from referencing import Registry, Resource


def digest(raw):
    return {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--architecture', required=True, type=Path)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    unit = Path(__file__).resolve().parent.parent
    bindings = json.loads((unit / 'reference/input-pins.json').read_bytes())
    inputs = {}
    for row in bindings['inputs']:
        path = args.architecture / row['path']
        raw = path.read_bytes()
        if digest(raw) != {key: row[key] for key in ('bytes', 'sha256')}:
            raise ValueError('reference input changed: ' + row['path'])
        inputs[row['role']] = (path, raw)
    assert not args.output.exists(), 'output must be fresh'

    def load_module(role, name):
        spec = importlib.util.spec_from_file_location(name, inputs[role][0])
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    canonical = load_module('canonical', 'doctor_reference_canonical')
    projection = load_module('projection', 'doctor_reference_projection')

    def workflow(role):
        tree = ast.parse(inputs[role][1])
        names = {'doctor', 'terminate', 'exit_code', 'render', 'parity_holds'}
        selected = [node for node in tree.body
                    if isinstance(node, ast.FunctionDef) and node.name in names]
        assert {node.name for node in selected} == names
        ns = {'canonical': canonical, 'EXIT': {
            'success': 0, 'policy-failed': 1, 'request-rejected': 2,
            'indeterminate': 3, 'operational-failed': 4, 'interrupted': 130}}
        exec(compile(ast.Module(body=selected, type_ignores=[]), str(inputs[role][0]), 'exec'), ns)
        return tree, ns

    before, old = workflow('baseline')
    after, new = workflow('workflow')
    others = lambda tree: [ast.dump(node) for node in tree.body
                          if not (isinstance(node, ast.FunctionDef) and node.name in {'doctor', 'terminate'})]
    assert others(before) == others(after)
    assert len(others(before)) == 116
    schemas = [json.loads(raw) for role, (_, raw) in inputs.items() if role.startswith('schema:')]
    assert len(schemas) == 40 and len({schema['$id'] for schema in schemas}) == 40
    registry = Registry().with_resources((schema['$id'], Resource.from_contents(schema)) for schema in schemas)
    common = json.loads(inputs['schema:common-v4.schema.json'][1])
    old_common = json.loads(inputs['old-common'][1])
    old_defs, new_defs = copy.deepcopy(old_common), copy.deepcopy(common)
    old_codes = old_defs['$defs']['DomainDetailCode'].pop('enum')
    new_codes = new_defs['$defs']['DomainDetailCode'].pop('enum')
    assert old_defs == new_defs and new_codes[:317] == old_codes
    assert new_codes[317:] == ['INSTALLATION.DURABILITY_NOT_CHECKED', 'INSTALLATION.NOT_INITIALIZED']
    assert len(new_codes) == len(set(new_codes)) == 319
    vocabulary = json.loads(inputs['public-registry'][1])
    assert {row['code'] for row in vocabulary['records']} == set(new_codes)
    detail = Draft202012Validator({'$ref': common['$id'] + '#/$defs/DomainDetail'}, registry=registry)
    envelope_schema = json.loads(inputs['schema:command-envelope-v7.schema.json'][1])
    envelope_validator = Draft202012Validator(envelope_schema, registry=registry)
    inventory = json.loads(inputs['commands'][1])
    commands = {row['name']: row for row in inventory['commands']}
    unproducible_golden = next(row for row in inventory['goldens']
                              if row['id'] == 'doctor-report-not-producible')
    cases = json.loads(inputs['cases'][1])
    results = []
    request_id = 'req1_00000000000000000000000000000001'
    for case in cases['cases']:
        codes = cases['inheritedTwoDefectCodes'] if case['id'] == 'inherited-two-defects-no-notice' else ['DELIVERY.CLOSURE_BYTES_CORRUPT'] * case['actual']
        actual = [{'code': code, 'remedy': 'Inspect the reported defect.'} for code in codes]
        for item in actual:
            detail.validate(item)
        session = projection.DoctorSession(new)
        try:
            report, termination = session.assemble(case['complete'], actual,
                report_producible=case.get('reportProducible', True))
            assert case['produced'] and not session.failed
        except projection.ReportUnavailable:
            assert not case['produced'] and session.failed
            report, termination = session.unavailable_projection()
            try:
                session.assemble(False, [])
            except projection.ReportUnavailable:
                pass
            else:
                raise AssertionError('failed report session resumed')
        assert report['reportProduced'] == case['produced']
        assert type(report['defectsFound']) is int and report['defectsFound'] == case['count']
        assert len(report['defects']) == case['entries']
        assert new['exit_code'](termination) == case['exit']
        notice = [item for item in report['defects'] if item['code'] == projection.INFO]
        assert len(notice) == int(case['notice'])
        if notice:
            assert notice[0]['remedy'] == cases['expectedInformationalRemedy']
        if case['produced']:
            assert ('domainDetail' in termination) == (case['count'] > 0)
            if case['count']:
                assert termination['domainDetail']['code'] == 'DOCTOR.DEFECTS_FOUND'
        else:
            assert termination['domainDetail']['code'] == 'DOCTOR.REPORT_NOT_PRODUCIBLE'
            assert termination['class'] == unproducible_golden['class']
            assert termination['errorCode'] == unproducible_golden['errorCode']
            assert termination['domainDetail']['code'] == unproducible_golden['domainDetail']
            assert new['exit_code'](termination) == unproducible_golden['exitCode']
        envelope, renderings = projection.project_doctor(new, commands['doctor'], report,
            termination, request_id, {'standing': 'synthetic caller-supplied security projection'})
        envelope_validator.validate(envelope)
        assert new['parity_holds'](renderings)
        for rendered in renderings:
            assert rendered['parity']['defects-found'] == case['count']
            assert rendered['parity']['defects'] == report['defects']
            assert set(rendered['parity']) == set(commands['doctor']['parityFields'])
            if rendered['format'] in ('json', 'agent'):
                assert rendered['envelope'] == envelope
            else:
                assert rendered['lines'].count(cases['expectedInformationalLabel']) == int(case['notice'])
        if case['id'] == 'inherited-two-defects-no-notice':
            assert old['doctor'](True, actual) == (report, termination)
        results.append({'id': case['id'], 'envelope': envelope, 'renderings': renderings})

    malformed = {'code': 'INSTALLATION.UNREGISTERED', 'remedy': 'Unknown.'}
    assert not detail.is_valid(malformed)
    assert new['doctor'](True, [malformed])[0]['defectsFound'] == 1
    duplicate = projection.DoctorSession(new)
    try:
        duplicate.assemble(True, [projection.NOTICE])
    except projection.ReportUnavailable:
        assert duplicate.failed
    else:
        raise AssertionError('informational notice admitted as an actual defect')
    good = results[0]['envelope']
    mutations = []
    for name in ['boolean-count', 'detail-severity', 'doctor-field', 'unknown-code', 'oversized-array']:
        bad = copy.deepcopy(good)
        if name == 'boolean-count': bad['doctor']['defectsFound'] = False
        if name == 'detail-severity': bad['doctor']['defects'][0]['severity'] = 'info'
        if name == 'doctor-field': bad['doctor']['severity'] = 'info'
        if name == 'unknown-code': bad['doctor']['defects'][0]['code'] = malformed['code']
        if name == 'oversized-array': bad['doctor']['defects'] *= 257
        assert not envelope_validator.is_valid(bad), name
        mutations.append(name)
    for code in ['INSTALLATION.NOT_INITIALIZED', 'storage.backup-choice-required']:
        failure_detail = {'code': code, 'remedy': 'Follow the disclosed initialization prerequisites.'}
        failure = {'schemaFamily': 'opensip.product.envelope', 'schemaMajor': 7,
                   'kind': 'failure', 'requestId': request_id, 'exitCode': 2,
                   'termination': {'class': 'request-rejected', 'errorCode': 'REQUEST.PRECONDITION_FAILED',
                                   'domainDetail': failure_detail}, 'errors': [failure_detail]}
        envelope_validator.validate(failure)
        results.append({'id': code, 'envelope': failure, 'nativeRoutingClaimed': False})
    # Use each existing field set; never add doctor defects or a new note channel.
    for command_name in ('trust-doctor', 'store-status'):
        command = commands[command_name]
        assert 'defects' not in command['parityFields']
        parity = {field: {'syntheticExistingField': field} for field in command['parityFields']}
        rendered = [new['render']({'parity': parity, 'envelope': {'syntheticExistingEnvelope': True}}, fmt, command)
                    for fmt in command['formats']]
        assert new['parity_holds'](rendered)
        assert projection.INFO not in json.dumps(rendered)
        results.append({'id': command_name, 'renderings': rendered,
                        'standing': 'Existing field-set projection only; not schema-valid native trust/store report.'})
    old_failed, old_termination = old['doctor'](False, [])
    new_failed, new_termination = new['doctor'](False, [])
    assert old_failed == new_failed
    assert {key: value for key, value in new_termination.items() if key != 'domainDetail'} == old_termination
    assert new_termination['domainDetail']['code'] == 'DOCTOR.REPORT_NOT_PRODUCIBLE'
    old_term_ast = next(node for node in before.body if isinstance(node, ast.FunctionDef) and node.name == 'terminate')
    new_term_ast = copy.deepcopy(next(node for node in after.body if isinstance(node, ast.FunctionDef) and node.name == 'terminate'))
    # Strip exactly the one newly registered existing-law detail, then compare
    # the entire terminate AST; every other branch must remain byte-meaning identical.
    changed = 0
    for node in ast.walk(new_term_ast):
        if isinstance(node, ast.Dict):
            for index, (key, value) in enumerate(zip(node.keys, node.values)):
                if (isinstance(key, ast.Constant) and key.value == 'domainDetail'
                        and isinstance(value, ast.Dict)
                        and any(isinstance(v, ast.Constant) and v.value == 'DOCTOR.REPORT_NOT_PRODUCIBLE' for v in value.values)):
                    node.keys.pop(index); node.values.pop(index); changed += 1; break
    assert changed == 1 and ast.dump(old_term_ast) == ast.dump(new_term_ast)
    result = {'passed': True, 'doctorCases': len(cases['cases']), 'schemaMutationsRefused': mutations,
              'nonDoctorOrTerminateTopLevelStatementsUnchanged': 116,
              'terminateChangedOnlyByExistingUnproducibleDetail': True, 'currentCodes': 319,
              'checkedInputFiles': len(inputs), 'results': results,
              'standing': 'Pinned trusted reference composition; no native observation, source selection, product renderer or qualification.'}
    args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'results'}))


if __name__ == '__main__':
    main()
