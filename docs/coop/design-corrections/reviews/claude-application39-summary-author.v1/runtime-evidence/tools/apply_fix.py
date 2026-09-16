"""Correct the application summary boundary in this runtime's capture only.

usage: python -I -B apply_fix.py [--dry]
Files: work/application-successor-root.v2/{apply-advisory-records.successor.v1.py, current_reference_summary.py}.
Before-images are copied to work/before/ first; every replacement must occur exactly once; receipts append to
receipts/edits.jsonl. Nothing outside this runtime is written.
"""
import hashlib, json, shutil, sys
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-application39-summary-author.v1')
APP = RT / 'work/application-successor-root.v2'
BEFORE = RT / 'work/before'
DRY = '--dry' in sys.argv
SCRIPT = 'apply-advisory-records.successor.v1.py'
HELPER = 'current_reference_summary.py'


def sha(b):
    return hashlib.sha256(b).hexdigest()


HELPER_EDITS = [
    ('''Pure record construction and read-only verification. Does not grant acceptance,
write an application, or change the frozen historical validation summary.
"""''', '''Pure record construction and read-only verification. Does not grant acceptance,
write an application, or change the frozen historical validation summary.

Two evidence vintages meet at the application boundary. An accepted subject may retain an older validation summary
byte-for-byte while its generated reports and the bound reference receipts are current. Current counts come only from
the source-bound receipts; every frozen generated report the application presents as current must be the executed
copy; the accepted summary is checked only as itself (accepted_summary_boundary) and its counts are recorded, never
equated with current execution.
"""'''),
    ('''    assert len(commands['commands']) == 7
''', '''    assert len(commands['commands']) == 7
    # The derived six-group view names the original runner receipt; the bound receipt adds only the subject binding.
    original = load(directory / 'runner-original-reference-checks.json')
    assert sha(directory / 'runner-original-reference-checks.json') == suite['originalRunnerReceiptSha256']
    assert original['passed'] is True and original['commands'] == commands['commands']
'''),
    ('''    native = measured('native-report.json')
    security = measured('security.json')
    workflow = measured('workflow-surface-report.json')
    integration = measured('integration.json')
    matrix = load(snapshot / (dc + 'native/native-capability-matrix.v2.json'))
    assert native['matrix']['cells'] == len(matrix['cells']) and native['matrix']['qualifiedCells'] == 0
''', '''    native = measured('native-report.json')
    security = measured('security.json')
    workflow = measured('workflow-surface-report.json')
    integration = measured('integration.json')
    parent = measured('workflows.json')
    assert parent['passed'] is True and parent['sourcePinsValid'] is True and parent['check']['exitCode'] == 0
    assert parent['check']['reportSha256'] == sha(directory / 'workflow-surface-report.json')
    assert json.loads(parent['check']['stdout']) == {'checks': workflow['passed'], 'passed': workflow['passed'], 'failed': 0}
    assert native['cases']['failed'] == 0 and native['cases']['passed'] == native['cases']['total']
    assert workflow['failed'] == [] and integration['failed'] == [] and integration['checks'] == integration['passed']
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
'''),
    ('''    current['workflows'].update(checksPassed=workflow['passed'], report=report('workflows.json'))
''', '''    current['workflows'] = {'checksPassed': workflow['passed'], 'commands': len(inventory['commands']),
                            'goldens': len(inventory['goldens']), 'report': report('workflows.json'),
                            'inventory': {'path': inventory_rel, 'sha256': sha(snapshot / inventory_rel),
                                          'resolveAgainst': subject}}
'''),
    ('''        'subject': subject, 'commands': command_ref, 'identityCounts': count_ref,
        'reports': evidence,
    }
    return current
''', '''        'subject': subject, 'commands': command_ref, 'identityCounts': count_ref,
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
'''),
]

SCRIPT_EDITS = [
    ('''Current matrix cell count is measured from the accepted snapshot.
"""''', '''Current matrix cell count is measured from the accepted snapshot.
The accepted frozen validation summary keeps its own evidence vintage; current counts come only from the
source-bound reference receipts (current_reference_summary.accepted_summary_boundary).
"""'''),
    ('''from current_reference_summary import current_reference_summary
''', '''from current_reference_summary import accepted_summary_boundary
'''),
    ('''manifest = load(root / app['designSubject']['path'])
snapshot = Path(app['designSnapshotRoot'])
expected = {r['path']: r for r in manifest['files']}
sources = []


def accepted(rel):
    p = snapshot / rel
    assert sha(p) == expected[rel]['sha256']
    sources.append({'path': rel, 'sha256': sha(p), 'resolveAgainst': app['designSubject']})
    return load(p)


old = accepted(dc + 'validation-summary.v1.json')
matrix = accepted(dc + 'native/native-capability-matrix.v2.json')
native = accepted(dc + 'native/native-evidence-report.v2.json')
identity = accepted(dc + 'foundation/identity-report.json')
security = accepted(dc + 'security/security-lifecycle-report.v1.json')
workflow = accepted(dc + 'workflows/workflows-report.v1.json')
integration = accepted(dc + 'integration-report.v1.json')
assert old['foundation']['checksPassed'] == sum(old['foundation']['components'].values())
assert old['foundation']['components']['identity'] == identity['passed']
assert old['security']['casesPassed'] == security['counts']['pass'] and old['security']['invariantSweepsPassed'] == len(security['sweeps'])
assert old['native']['casesPassed'] == native['cases']['passed']
assert old['workflows']['checksPassed'] == workflow['passed'] and old['integration']['checksPassed'] == integration['passed']
measured_cells = len(matrix['cells'])
assert measured_cells == native['matrix']['cells'] and native['matrix']['qualifiedCells'] == 0
assert old['native']['matrixCells'] == measured_cells
''', '''snapshot = Path(app['designSnapshotRoot'])
# Two evidence vintages meet here. The accepted subject may retain an older validation summary byte-for-byte while
# its generated reports and the bound reference receipts are current. The summary is checked only as itself; every
# current count and every presented generated report is bound to the source-bound receipts. Historical counts are
# recorded beside current ones, never equated with them.
boundary = accepted_summary_boundary(root, app['designSubject'], app['designSnapshotRoot'],
    app['acceptedDesignReproduction']['originalExecutedCommandRecord'],
    app['referenceEvidenceSummary']['identityCountMeasurement'])
old = boundary['acceptedSummary']
measured_cells = boundary['measuredCells']
sources = boundary['sources']
'''),
    ('''current = current_reference_summary(root, app['designSubject'],
    app['acceptedDesignReproduction']['originalExecutedCommandRecord'],
    app['referenceEvidenceSummary']['identityCountMeasurement'], old)
current['native']['matrixCells'] = measured_cells
current['native']['qualifiedCells'] = native['matrix']['qualifiedCells']
''', '''current = boundary['current']
assert current['native']['matrixCells'] == measured_cells and current['native']['qualifiedCells'] == 0
'''),
    ('''    'sha256': sha(snapshot / (dc + 'validation-summary.v1.json')),
    'resolveAgainst': app['designSubject'],
}
''', '''    'sha256': sha(snapshot / (dc + 'validation-summary.v1.json')),
    'resolveAgainst': app['designSubject'],
    'meaning': (
        'The accepted frozen summary as recorded by its own evidence vintage; not current execution. Its counts '
        'are listed beside the receipt-bound current counts; a difference is not a correction of it.'
    ),
    'recordedCountsVersusCurrent': boundary['acceptedSummaryCounts'],
}
'''),
    ('''app['referenceEvidenceSummary']['acceptedFrozenValidationSummary'] = app['referenceEvidenceSummary']['validationSummary']
app['referenceEvidenceSummary']['acceptedFrozenValidationSummary']['resolveAgainst'] = app['designSubject']
app['referenceEvidenceSummary']['validationSummary'] = current_ref
''', '''frozen_ref = app['referenceEvidenceSummary']['validationSummary']
assert sha(root / frozen_ref['path']) == frozen_ref['sha256']
assert app['referenceEvidenceSummary']['foundationPassingCalls'] == load(root / frozen_ref['path'])['foundation']['checksPassed']
app['referenceEvidenceSummary']['acceptedFrozenValidationSummary'] = app['referenceEvidenceSummary']['validationSummary']
app['referenceEvidenceSummary']['acceptedFrozenValidationSummary']['resolveAgainst'] = app['designSubject']
app['referenceEvidenceSummary']['validationSummary'] = current_ref
# The assembled foundation count came from the frozen summary; keep it under that name and state the current count.
app['referenceEvidenceSummary']['acceptedFrozenFoundationPassingCalls'] = app['referenceEvidenceSummary']['foundationPassingCalls']
app['referenceEvidenceSummary']['foundationPassingCalls'] = current['foundation']['checksPassed']
'''),
    ('''    + f"Current reference evidence records {native['cases']['passed']} native cases, {workflow['passed']} workflow controls and {current['evaluator3']['suiteCount']} current evaluator suites.''',
     '''    + f"Current reference evidence records {current['native']['casesPassed']} native cases, {current['workflows']['checksPassed']} workflow controls and {current['evaluator3']['suiteCount']} current evaluator suites.'''),
    ('''            'measuredMatrixCells': measured_cells,
''', '''            'measuredMatrixCells': measured_cells,
            'acceptedSummaryCountsVersusCurrent': boundary['acceptedSummaryCounts'],
'''),
]


def run(name, edits):
    path = APP / name
    raw = path.read_bytes()
    text = raw.decode('utf-8')
    for i, (old, new) in enumerate(edits):
        n = text.count(old)
        if n != 1:
            raise SystemExit('%s replacement %d expected exactly one match, found %d: %r' % (name, i, n, old[:120]))
        text = text.replace(old, new)
    compile(text, name, 'exec')
    row = {'path': name, 'replacements': len(edits), 'beforeSha256': sha(raw), 'afterSha256': sha(text.encode()), 'dry': DRY}
    if not DRY:
        BEFORE.mkdir(parents=True, exist_ok=True)
        if not (BEFORE / name).exists():
            shutil.copyfile(path, BEFORE / name)
        path.write_bytes(text.encode())
        with open(RT / 'receipts/edits.jsonl', 'a') as f:
            f.write(json.dumps(row) + '\n')
    return row


rows = [run(HELPER, HELPER_EDITS), run(SCRIPT, SCRIPT_EDITS)]
print(json.dumps(rows, indent=1))
