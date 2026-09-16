"""Bind an application summary to actual final-source reference receipts.

Pure record construction and read-only verification. Does not grant acceptance,
write an application, or change the frozen historical validation summary.
"""
from pathlib import Path
import copy
import hashlib
import json


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load(path):
    return json.loads(Path(path).read_bytes())


def current_reference_summary(root, subject, command_ref, count_ref, previous):
    root = Path(root)
    dc = 'docs/coop/design-corrections/'
    assert sha(root / subject['path']) == subject['sha256']
    manifest = load(root / subject['path'])
    snapshot = Path(manifest['snapshotRoot'])
    members = {r['path']: r for r in manifest['files']}
    assert sha(root / command_ref['path']) == command_ref['sha256']
    commands = load(root / command_ref['path'])
    assert commands['passed'] is True
    assert commands['subjectManifestSha256'] == subject['sha256']
    directory = (root / command_ref['path']).parent
    suite = load(directory / 'report.json')
    assert suite['passed'] is True and len(suite['checks']) == 6
    assert len(commands['commands']) == 7
    evidence = []

    def measured(name):
        path = directory / name
        evidence.append({'path': path.relative_to(root).as_posix(), 'sha256': sha(path)})
        return load(path)

    for row in commands['commands']:
        assert row['sourceSha256'] == members[row['source']]['sha256'] == sha(snapshot / row['source'])
        assert row['exitCode'] == 0 and row['timedOut'] is False
    for row in suite['checks']:
        assert row['exitCode'] == 0 and row['timedOut'] is False
        assert sha(directory / (row['name'] + '.stdout')) == row['stdoutSha256']
        assert sha(directory / (row['name'] + '.stderr')) == row['stderrSha256']
        matches = [c for c in commands['commands'] if c['name'] == row['name']]
        assert len(matches) == 1 and matches[0]['command'] == row['command']
        assert matches[0]['stdoutSha256'] == row['stdoutSha256']
        assert matches[0]['stderrSha256'] == row['stderrSha256']
    foundation = measured('foundation.json')
    evaluator = measured('evaluator3/report.json')
    assert foundation['passed'] is True and evaluator['passed'] is True
    pins = load(snapshot / (dc + 'foundation/evaluator3-source-pins.v1.json'))
    ordinary = load(snapshot / (dc + 'foundation/source-pins.v1.json'))
    assert foundation['sourceFileCount'] == len(ordinary['files'])
    assert commands['currentProfilePinsSha256'] == sha(snapshot / (dc + 'foundation/evaluator3-source-pins.v1.json'))
    assert len(evaluator['checks']) == suite['evaluatorChildren'] == commands['evaluatorBudget']['children']
    for row in evaluator['checks']:
        assert row['exitCode'] == 0 and row['timedOut'] is False
        assert sha(directory / 'evaluator3' / (row['name'] + '.stdout')) == row['stdoutSha256']
        assert sha(directory / 'evaluator3' / (row['name'] + '.stderr')) == row['stderrSha256']
    assert sha(root / count_ref['path']) == count_ref['sha256']
    counts = load(root / count_ref['path'])
    identity = measured('foundation/identity-report.json')
    assert counts['reportSha256'] == sha(root / counts['report'])
    assert (root / counts['report']).resolve() == (directory / 'foundation/identity-report.json').resolve()
    assert identity['failed'] == 0 and identity['passed'] == counts['passingCalls']
    assert counts['passingCalls'] == counts['distinctIds'] + counts['duplicateExtraInstances']
    components = {}
    for key, name in [('foundation', 'foundation-report.json'), ('identity', 'identity-report.json'),
                      ('product-quality', 'product-quality-report.json'),
                      ('product-configuration', 'product-configuration-report.json')]:
        components[key] = measured('foundation/' + name)['passed']
    array = measured('foundation/array-order-report.json')
    components['array-order'] = array.get('arrayCount', array.get('count', len(array['checks'])))
    native = measured('native-report.json')
    security = measured('security.json')
    workflow = measured('workflow-surface-report.json')
    integration = measured('integration.json')
    matrix = load(snapshot / (dc + 'native/native-capability-matrix.v2.json'))
    assert native['matrix']['cells'] == len(matrix['cells']) and native['matrix']['qualifiedCells'] == 0
    current = copy.deepcopy(previous)

    def report(name):
        return (directory / name).relative_to(root / dc).as_posix()

    current['foundation'] = {
        'checksPassed': sum(components.values()), 'sourcePinsVerified': foundation['sourceFileCount'],
        'report': report('foundation.json'), 'components': components,
        'identityCountAccount': {'path': str(Path(count_ref['path']).relative_to(dc)),
                                'sha256': count_ref['sha256'],
                                **{k: counts[k] for k in ('passingCalls', 'distinctIds', 'duplicateExtraInstances')}},
    }
    current['security'] = {'casesPassed': security['counts']['pass'],
                           'invariantSweepsPassed': len(security['sweeps']), 'report': report('security.json')}
    current['native'] = {'casesPassed': native['cases']['passed'], 'matrixCells': len(matrix['cells']),
                         'qualifiedCells': 0, 'report': report('native-report.json')}
    current['workflows'].update(checksPassed=workflow['passed'], report=report('workflows.json'))
    current['integration'] = {'checksPassed': integration['passed'], 'report': report('integration.json')}
    current['evaluator3'] = {'suiteCount': len(evaluator['checks']), 'allPassed': True,
                            'sourcePinsVerified': len(pins['files']), 'report': report('evaluator3/report.json'),
                            'standing': 'Actual final-source synthetic reference replay; no product qualification.'}
    current['currentExecutedReference'] = {
        'standing': 'Actual recorded final-source commands and reports; not a new execution or product qualification.',
        'subject': subject, 'commands': command_ref, 'identityCounts': count_ref,
        'reports': evidence,
    }
    return current
