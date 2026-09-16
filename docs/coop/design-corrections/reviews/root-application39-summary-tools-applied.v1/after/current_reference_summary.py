"""Bind an application summary to actual final-source reference receipts.

Pure record construction and read-only verification. Does not grant acceptance,
write an application, or change the frozen historical validation summary.

Two evidence vintages meet at the application boundary. An accepted subject may retain an older validation summary
byte-for-byte while its generated reports and the bound reference receipts are current. Current counts come only from
the source-bound receipts; every frozen generated report the application presents as current must be the executed
copy; the accepted summary is checked only as itself (accepted_summary_boundary) and its counts are recorded, never
equated with current execution.
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
    # The derived six-group view names the original runner receipt; the bound receipt adds only the subject binding.
    original = load(directory / 'runner-original-reference-checks.json')
    assert sha(directory / 'runner-original-reference-checks.json') == suite['originalRunnerReceiptSha256']
    assert original['passed'] is True and original['commands'] == commands['commands']
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
    parent = measured('workflows.json')
    assert parent['passed'] is True and parent['sourcePinsValid'] is True and parent['check']['exitCode'] == 0
    assert parent['check']['reportSha256'] == sha(directory / 'workflow-surface-report.json')
    assert json.loads(parent['check']['stdout']) == {'checks': workflow['passed'], 'passed': workflow['passed'], 'failed': 0}
    assert native['cases']['failed'] == 0 and native['cases']['passed'] == native['cases']['total']
    assert workflow['failed'] == [] and integration['failed'] == [] and len(integration['checks']) == integration['passed']
    assert security['passed'] is True and security['counts']['fail'] == 0
    assert security['counts']['pass'] == security['counts']['total'] and all(row['holds'] is True for row in security['sweeps'])
    matrix_rel = dc + 'native/native-capability-matrix.v2.json'
    assert sha(snapshot / matrix_rel) == members[matrix_rel]['sha256']
    matrix = load(snapshot / matrix_rel)
    assert native['matrix']['cells'] == len(matrix['cells']) and native['matrix']['qualifiedCells'] == 0
    assert matrix['platformQualified'] is False
    custody = []
    for group, executed, frozen in GENERATED_REPORTS:
        frozen_rel = dc + frozen
        assert sha(snapshot / frozen_rel) == members[frozen_rel]['sha256']
        same = sha(directory / executed) == sha(snapshot / frozen_rel)
        assert same or group not in EXECUTED_COPY_GROUPS, 'frozen generated report is not the executed copy: ' + group
        custody.append({'group': group,
                        'executedReport': {'path': (directory / executed).relative_to(root).as_posix(),
                                           'sha256': sha(directory / executed)},
                        'frozenGeneratedReport': {'path': frozen_rel, 'sha256': sha(snapshot / frozen_rel),
                                                  'resolveAgainst': subject},
                        'relation': EXECUTED_COPY if same else NOT_EXECUTED_COPY})
    # The workflow checker validates the v1 command inventory; its commands and goldens are measured, not carried.
    checker = next(row for row in commands['commands'] if row['name'] == 'workflow-surface')
    inventory_rel = dc + 'workflows/command-inventory.v1.json'
    assert inventory_rel.rsplit('/', 1)[1].encode() in (snapshot / checker['source']).read_bytes()
    assert sha(snapshot / inventory_rel) == members[inventory_rel]['sha256']
    inventory = load(snapshot / inventory_rel)
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
    current['workflows'] = {'checksPassed': workflow['passed'], 'commands': len(inventory['commands']),
                            'goldens': len(inventory['goldens']), 'report': report('workflows.json'),
                            'inventory': {'path': inventory_rel, 'sha256': sha(snapshot / inventory_rel),
                                          'resolveAgainst': subject}}
    current['integration'] = {'checksPassed': integration['passed'], 'report': report('integration.json')}
    current['evaluator3'] = {'suiteCount': len(evaluator['checks']), 'allPassed': True,
                            'sourcePinsVerified': len(pins['files']), 'report': report('evaluator3/report.json'),
                            'standing': 'Actual final-source synthetic reference replay; no product qualification.'}
    current['currentExecutedReference'] = {
        'standing': 'Actual recorded final-source commands and reports; not a new execution or product qualification.',
        'subject': subject, 'commands': command_ref, 'identityCounts': count_ref,
        'reports': evidence,
        'originalRunnerReceipt': {'path': (directory / 'runner-original-reference-checks.json').relative_to(root).as_posix(),
                                  'sha256': suite['originalRunnerReceiptSha256']},
        'generatedReportCustody': custody,
    }
    return current


EXECUTED_COPY = 'byte-identical-executed-copy'
NOT_EXECUTED_COPY = 'frozen-generated-report-differs; not current execution evidence'
# (group, executed report under the receipt directory, frozen generated report in the accepted subject)
GENERATED_REPORTS = (
    ('native', 'native-report.json', 'native/native-evidence-report.v2.json'),
    ('workflows', 'workflow-surface-report.json', 'workflows/workflows-report.v1.json'),
    ('integration', 'integration.json', 'integration-report.v1.json'),
    ('identity', 'foundation/identity-report.json', 'foundation/identity-report.json'),
    ('security', 'security.json', 'security/security-lifecycle-report.v1.json'),
    ('foundation', 'foundation.json', 'foundation/validation-report.json'),
)
# Groups whose frozen generated report the application presents as current: they must be the executed copy.
EXECUTED_COPY_GROUPS = ('native', 'workflows', 'integration', 'identity')
ACCEPTED_SUMMARY_INPUTS = (
    ('summary', 'validation-summary.v1.json'),
    ('matrix', 'native/native-capability-matrix.v2.json'),
    ('native', 'native/native-evidence-report.v2.json'),
    ('identity', 'foundation/identity-report.json'),
    ('security', 'security/security-lifecycle-report.v1.json'),
    ('workflows', 'workflows/workflows-report.v1.json'),
    ('integration', 'integration-report.v1.json'),
)
SUMMARY_COUNT_FIELDS = (
    'foundation.checksPassed', 'foundation.sourcePinsVerified', 'foundation.components.identity',
    'security.casesPassed', 'security.invariantSweepsPassed', 'native.casesPassed', 'native.matrixCells',
    'native.qualifiedCells', 'workflows.checksPassed', 'workflows.commands', 'workflows.goldens',
    'integration.checksPassed', 'evaluator3.suiteCount', 'evaluator3.sourcePinsVerified',
)


def _field(record, dotted):
    node = record
    for key in dotted.split('.'):
        if not isinstance(node, dict) or key not in node:
            return None
        node = node[key]
    return node


def accepted_summary_boundary(root, subject, snapshot_root, command_ref, count_ref):
    """The application boundary between the accepted frozen summary and current execution.

    The accepted summary is checked only as itself: pinned bytes, internal foundation consistency and the already
    corrected v13 matrix equality (summary == matrix == generated report). It is never compared with current execution
    counts. Current counts come from current_reference_summary over the source-bound receipts; the frozen generated
    reports read here are pinned by the subject, the presented ones are the executed copies (verified there), and the
    frozen security report must agree in counts only. Both vintages' counts are returned side by side; a difference
    is data, not a failure."""
    root = Path(root)
    dc = 'docs/coop/design-corrections/'
    assert sha(root / subject['path']) == subject['sha256']
    manifest = load(root / subject['path'])
    assert str(snapshot_root) == manifest['snapshotRoot']
    snapshot = Path(snapshot_root)
    members = {r['path']: r for r in manifest['files']}
    accepted, sources = {}, []
    for key, rel in ACCEPTED_SUMMARY_INPUTS:
        path = snapshot / (dc + rel)
        assert sha(path) == members[dc + rel]['sha256'], 'accepted subject pin: ' + rel
        accepted[key] = load(path)
        sources.append({'path': dc + rel, 'sha256': sha(path), 'resolveAgainst': subject})
    old = accepted['summary']
    assert old['foundation']['checksPassed'] == sum(old['foundation']['components'].values())
    cells = len(accepted['matrix']['cells'])
    assert cells == accepted['native']['matrix']['cells'] and accepted['native']['matrix']['qualifiedCells'] == 0
    assert old['native']['matrixCells'] == cells
    current = current_reference_summary(root, subject, command_ref, count_ref, old)
    custody = {row['group']: row for row in current['currentExecutedReference']['generatedReportCustody']}
    assert current['native']['casesPassed'] == accepted['native']['cases']['passed'] and current['native']['matrixCells'] == cells
    assert current['workflows']['checksPassed'] == accepted['workflows']['passed']
    assert current['integration']['checksPassed'] == accepted['integration']['passed']
    assert current['foundation']['components']['identity'] == accepted['identity']['passed']
    assert current['security']['casesPassed'] == accepted['security']['counts']['pass']
    assert current['security']['invariantSweepsPassed'] == len(accepted['security']['sweeps'])
    for (key, _), row in zip(ACCEPTED_SUMMARY_INPUTS, sources):
        if key == 'summary':
            row['role'] = 'accepted frozen summary: its own evidence vintage; not a current count source'
        elif key == 'matrix':
            row['role'] = 'accepted matrix: current cell count and zero qualification'
        elif custody[key]['relation'] == EXECUTED_COPY:
            row['role'] = 'frozen generated report: byte-identical copy of the bound execution'
        else:
            row['role'] = 'frozen generated report: counts agree with the bound execution; not an executed copy'
    counts = [{'field': f, 'acceptedSummary': _field(old, f), 'current': _field(current, f),
               'equal': _field(old, f) == _field(current, f)} for f in SUMMARY_COUNT_FIELDS]
    return {'acceptedSummary': old, 'accepted': accepted, 'sources': sources, 'measuredCells': cells,
            'current': current, 'acceptedSummaryCounts': counts}
