"""Controls for the application summary boundary over the actual frozen39 receipts and exact historical summary.

usage: python -I -B boundary_controls.py
Reads the repo, frozen39 snapshot and retained v13 archive READ ONLY. Mutation worlds are built only under
controls/<id>/ in this runtime. The gated whole application script is NOT run (no bound receipt, assembled
application or accepted peer verdict exists); its boundary segments are extracted verbatim from the before and after
script bytes and executed with the application fields assemble-records.successor.v1.py records for v39.
"""
import ast, builtins, copy, hashlib, importlib.util, json, shutil, sys, tarfile, traceback
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-application39-summary-author.v1')
APP = RT / 'work/application-successor-root.v2'
BEFORE = RT / 'work/before'
CTL = RT / 'controls'
REPO = Path('/Users/sb/code/opensip-ai/opensip_arch')
DC = 'docs/coop/design-corrections/'
SNAP = '/tmp/opensip-design-corrections/candidate-subject.v39'
SCRIPT = 'apply-advisory-records.successor.v1.py'
HELPER = 'current_reference_summary.py'
FR = DC + 'reviews/codex-post-reset.v1/final-reference.v39/'
SUBJECT = {'path': DC + 'reviews/candidate-subject.v39.json', 'sha256': 'f71a59928d1b6aa84eed81b8cb49fd1fba91c65dd6599c58f99efcdc42569009'}
CMD = {'path': FR + 'reference-checks.json', 'sha256': 'cf31e1315ad63b2a4f20869a67944ac4c6444ecb2a80a6d3d79bf65ee6ba06b1'}
CNT = {'path': DC + 'reviews/codex-post-reset.v1/identity-check-counts.v39.json', 'sha256': '466a064d826c0e6661168f910d2ae5815d9da49a850babfdefe6c89cb28d9745'}
RESULTS = []


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


def bsha(b):
    return hashlib.sha256(b).hexdigest()


def load(p):
    return json.loads(Path(p).read_bytes())


def module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


sys.path.insert(0, str(APP))
C = module('coverage_contract_ctl', APP / 'coverage_contract.py')
OLD_H = module('crs_before', BEFORE / HELPER)
NEW_H = module('crs_after', APP / HELPER)


def app_fields(subject=SUBJECT, snapshot=SNAP, cmd=CMD, cnt=CNT):
    """Exactly the application fields the boundary segments read (assemble-records.successor.v1.py lines 565-674)."""
    return {'designSubject': subject, 'designSnapshotRoot': snapshot,
            'acceptedDesignReproduction': {'originalExecutedCommandRecord': cmd},
            'referenceEvidenceSummary': {'identityCountMeasurement': cnt}}


def outcome(fn):
    try:
        return {'result': 'pass', 'value': fn()}
    except Exception as exc:  # every refusal is recorded with its type, message head and raising frame
        tb = traceback.extract_tb(exc.__traceback__)
        frame = next((f for f in reversed(tb) if f.filename.endswith((HELPER, SCRIPT)) or '#segment' in f.filename), tb[-1])
        line = frame.line or ''
        if frame.filename.endswith('#segment'):
            # exec'd verbatim segments keep their real line numbers; read the raising line from the real script bytes
            line = Path(frame.filename[:-len('#segment')]).read_text().splitlines()[frame.lineno - 1].strip()
        return {'result': 'refuse', 'error': type(exc).__name__, 'message': str(exc).splitlines()[0][:200] if str(exc) else '',
                'at': '%s:%s' % (Path(frame.filename).name, frame.lineno), 'line': line[:200]}


# A refusal counts only at the guard under test: the raising error, message or line must contain this text.
EXPECTED_REFUSAL_SITE = {
    'actual-old-boundary-fails-on-frozen39': {'old': "old['native']['casesPassed'] == native['cases']['passed']"},
    'actual-historical-v13-guard-unchanged-and-scope-verified-from-retained-archive': {'v13SegmentOnHost': 'FileNotFoundError'},
    'receipt-missing-executed-native-report': {'before': 'FileNotFoundError', 'after': 'FileNotFoundError'},
    'receipt-forged-executed-native-count': {'after': 'not the executed copy: native'},
    'receipt-forged-workflow-surface-count': {'after': "parent['check']['reportSha256']"},
    'receipt-forged-integration-count': {'after': 'not the executed copy: integration'},
    'receipt-forged-security-count': {'after': "security['counts']['pass'] == security['counts']['total']"},
    'receipt-command-source-sha-mismatch': {'before': "row['sourceSha256']", 'after': "row['sourceSha256']"},
    'receipt-current-profile-pins-mismatch': {'before': 'currentProfilePinsSha256', 'after': 'currentProfilePinsSha256'},
    'receipt-command-ref-sha-mismatch': {'before': "command_ref['sha256']", 'after': "command_ref['sha256']"},
    'receipt-identity-counts-inconsistent': {'before': "counts['passingCalls']", 'after': "counts['passingCalls']"},
    'receipt-original-runner-receipt-altered': {'after': 'originalRunnerReceiptSha256'},
    'receipt-workflows-parent-report-hash-mismatch': {'after': "parent['check']['reportSha256']"},
    'receipt-evaluator-child-stdout-altered': {'before': "'.stdout'))", 'after': "'.stdout'))"},
    'snapshot-lawful-historical-summary-vintage-differs': {'oldScriptBoundary': "old['native']['casesPassed'] == native['cases']['passed']"},
    'snapshot-unpinned-historical-summary-change': {'boundary': 'accepted subject pin'},
    'snapshot-historical-summary-internally-inconsistent': {'boundary': "sum(old['foundation']['components'].values())"},
    'snapshot-historical-summary-matrix-cells-60': {'boundary': "old['native']['matrixCells'] == cells"},
    'snapshot-frozen-native-report-not-executed-copy': {'after': 'not the executed copy: native', 'boundary': 'not the executed copy: native'},
    'snapshot-frozen-integration-report-not-executed-copy': {'after': 'not the executed copy: integration', 'boundary': 'not the executed copy: integration'},
    'snapshot-and-receipt-consistent-qualified-cell': {'before': "qualifiedCells'] == 0", 'after': "native['matrix']['qualifiedCells'] == 0",
                                                       'boundary': "accepted['native']['matrix']['qualifiedCells'] == 0"},
    'snapshot-matrix-cell-removed': {'before': "len(matrix['cells'])", 'after': "native['matrix']['cells'] == len(matrix['cells'])",
                                     'boundary': "cells == accepted['native']['matrix']['cells']"},
    'snapshot-matrix-platform-qualified': {'after': 'platformQualified', 'boundary': 'platformQualified'},
    'snapshot-frozen-security-report-counts-differ': {'boundary': "accepted['security']['counts']['pass']"},
    'snapshot-command-source-bytes-unpinned': {'before': "row['sourceSha256']", 'after': "row['sourceSha256']", 'boundary': "row['sourceSha256']"},
}


def record(cid, world, expected, observed, facts=None):
    ok = all(observed[k]['result'] == v for k, v in expected.items())
    sites = EXPECTED_REFUSAL_SITE.get(cid, {})
    for k, text in sites.items():
        seen = ' '.join(str(observed[k].get(x, '')) for x in ('error', 'message', 'line'))
        ok = ok and observed[k]['result'] == 'refuse' and text in seen
    row = {'id': cid, 'world': world, 'expected': expected, 'expectedRefusalSite': sites,
           'observed': {k: {x: y for x, y in v.items() if x != 'value'} for k, v in observed.items()}, 'ok': ok}
    if facts is not None:
        row['facts'] = facts
    RESULTS.append(row)
    return row


# ------------------------------------------------------------------ verbatim script segments
def lines_of(path):
    return path.read_text().splitlines(keepends=True)


def segment(path, start_prefix, stop_prefix=None, stop_inclusive_prefix=None):
    text = lines_of(path)
    start = next(i for i, l in enumerate(text) if l.startswith(start_prefix))
    if stop_prefix is not None:
        stop = next(i for i in range(start + 1, len(text)) if text[i].startswith(stop_prefix))
    else:
        stop = next(i for i in range(start, len(text)) if text[i].startswith(stop_inclusive_prefix)) + 1
    return start + 1, stop, ''.join(text[start:stop])


def exec_segment(path, first_line, src, ns):
    code = compile('\n' * (first_line - 1) + src, str(path) + '#segment', 'exec')
    exec(code, ns)
    return ns


def namespace(helper, root=REPO, fields=None):
    return {'root': Path(root), 'app': fields or app_fields(), 'sha': lambda p: hashlib.sha256(p.read_bytes()).hexdigest(),
            'load': lambda p: json.loads(p.read_text()), 'Path': Path, 'dc': DC, 'C': C,
            'current_reference_summary': getattr(helper, 'current_reference_summary'),
            'accepted_summary_boundary': getattr(helper, 'accepted_summary_boundary', None)}


OLD_A = segment(BEFORE / SCRIPT, "manifest = load(root / app['designSubject']['path'])", "historical_manifest_path = ")
NEW_A = segment(APP / SCRIPT, "snapshot = Path(app['designSnapshotRoot'])", "historical_manifest_path = ")
OLD_B = segment(BEFORE / SCRIPT, "historical_manifest_path = ", "current = current_reference_summary(")
NEW_B = segment(APP / SCRIPT, "historical_manifest_path = ", "current = boundary['current']")
OLD_C = segment(BEFORE / SCRIPT, "current = current_reference_summary(", stop_inclusive_prefix="current['native']['qualifiedCells'] = ")
NEW_C = segment(APP / SCRIPT, "current = boundary['current']", stop_inclusive_prefix="assert current['native']['matrixCells'] == measured_cells")


def run_old_boundary(root=REPO, fields=None):
    ns = namespace(OLD_H, root, fields)
    exec_segment(BEFORE / SCRIPT, OLD_A[0], OLD_A[2], ns)
    exec_segment(BEFORE / SCRIPT, OLD_C[0], OLD_C[2], dict(ns, old=ns['old']))
    return ns


def run_new_boundary(root=REPO, fields=None):
    ns = namespace(NEW_H, root, fields)
    exec_segment(APP / SCRIPT, NEW_A[0], NEW_A[2], ns)
    exec_segment(APP / SCRIPT, NEW_C[0], NEW_C[2], ns)
    return ns


# ------------------------------------------------------------------ actual frozen39
old_run = outcome(lambda: run_old_boundary())
old_loads = namespace(OLD_H)
# Evaluate each original count assertion separately over the same verbatim loads (lines kept at their numbers).
seg_lines = OLD_A[2].splitlines(keepends=True)
loads_src = ''.join(l if not l.startswith(('assert ', 'measured_cells')) else '\n' for l in seg_lines)
exec_segment(BEFORE / SCRIPT, OLD_A[0], loads_src, old_loads)
old_loads['measured_cells'] = len(old_loads['matrix']['cells'])
per_assert = []
for offset, l in enumerate(seg_lines):
    if l.startswith('assert '):
        per_assert.append({'line': OLD_A[0] + offset, 'source': l.strip(), 'holds': bool(eval(l.strip()[len('assert '):], old_loads))})
record('actual-old-boundary-fails-on-frozen39', 'actual', {'old': 'refuse'}, {'old': old_run},
       {'firstFailure': old_run.get('at'), 'eachOriginalAssertion': per_assert,
        'historicalSummaryVersusFrozenGeneratedReports': {
            'native.casesPassed': [old_loads['old']['native']['casesPassed'], old_loads['native']['cases']['passed']],
            'workflows.checksPassed': [old_loads['old']['workflows']['checksPassed'], old_loads['workflow']['passed']]}})

before_helper = outcome(lambda: OLD_H.current_reference_summary(REPO, SUBJECT, CMD, CNT, load(Path(SNAP) / (DC + 'validation-summary.v1.json'))))
bh = before_helper.get('value') or {}
record('actual-before-helper-passes-as-root-observed', 'actual', {'before': 'pass'}, {'before': before_helper},
       {'foundation': bh.get('foundation', {}).get('checksPassed'), 'native': bh.get('native', {}).get('casesPassed'),
        'workflow': bh.get('workflows', {}).get('checksPassed'), 'evaluatorChildren': bh.get('evaluator3', {}).get('suiteCount'),
        'workflowsCommandsGoldensCarriedFromHistoricalSummary': [bh.get('workflows', {}).get('commands'), bh.get('workflows', {}).get('goldens')]})

new_run = outcome(lambda: run_new_boundary())
ns = new_run.get('value') or {}
cur = ns.get('current', {})
facts = {}
if new_run['result'] == 'pass':
    facts = {
        'current': {'foundation': cur['foundation']['checksPassed'], 'sourcePins': cur['foundation']['sourcePinsVerified'],
                    'identity': cur['foundation']['components']['identity'], 'security': [cur['security']['casesPassed'], cur['security']['invariantSweepsPassed']],
                    'native': cur['native']['casesPassed'], 'matrixCells': cur['native']['matrixCells'], 'qualifiedCells': cur['native']['qualifiedCells'],
                    'workflows': [cur['workflows']['checksPassed'], cur['workflows']['commands'], cur['workflows']['goldens']],
                    'integration': cur['integration']['checksPassed'], 'evaluator3': [cur['evaluator3']['suiteCount'], cur['evaluator3']['sourcePinsVerified']]},
        'acceptedSummaryCountsDiffering': [r for r in ns['boundary']['acceptedSummaryCounts'] if not r['equal']],
        'custody': [(r['group'], r['relation']) for r in cur['currentExecutedReference']['generatedReportCustody']],
        'sourceRoles': [(r['path'].split('/')[-1], r['role']) for r in ns['sources']],
    }
record('actual-corrected-boundary-passes-on-frozen39-with-differing-historical-counts', 'actual', {'new': 'pass'}, {'new': new_run}, facts)

if new_run['result'] == 'pass':
    rebound = outcome(lambda: NEW_H.current_reference_summary(REPO, SUBJECT, CMD, CNT, copy.deepcopy(cur)))
    same = rebound['result'] == 'pass' and all(cur[k] == rebound['value'][k] for k in ('foundation', 'security', 'native', 'workflows', 'integration', 'evaluator3', 'currentExecutedReference'))
    record('actual-verify-applied-rebound-reproduces-current-groups', 'actual', {'rebound': 'pass'}, {'rebound': rebound}, {'equalForVerifyAppliedKeys': same})
    if not same:
        RESULTS[-1]['ok'] = False
    prospective = load(Path('/tmp/opensip-design-corrections/root-application39-summary-guard-probe.v1/current-summary.prospective.json'))
    diff = {k: sorted(set(cur[k]) ^ set(prospective[k])) if isinstance(cur[k], dict) else None
            for k in ('foundation', 'security', 'native', 'workflows', 'integration', 'evaluator3', 'currentExecutedReference')}
    equal_values = {k: all(cur[k].get(x) == prospective[k].get(x) for x in prospective[k]) for k in ('foundation', 'security', 'native', 'workflows', 'integration', 'evaluator3')}
    record('actual-corrected-current-counts-equal-root-prospective-helper-output', 'actual', {}, {}, {'keyAdditions': diff, 'prospectiveValuesPreserved': equal_values})
    if not all(equal_values.values()):
        RESULTS[-1]['ok'] = False

# v13 guard: byte-identical segment; the historical snapshot is not materialised on this host; archive proves its scope.
b_same = OLD_B[2] == NEW_B[2]
v13 = outcome(lambda: exec_segment(APP / SCRIPT, NEW_B[0], NEW_B[2], namespace(NEW_H)))
hm = load(REPO / (DC + 'reviews/candidate-subject.v13.json'))
row = next(r for r in hm['files'] if r['path'] == DC + 'validation-summary.v1.json')
with tarfile.open(REPO / (DC + 'reviews/candidate-source.v13.tar.gz'), 'r:gz') as t:
    member = t.extractfile(DC + 'validation-summary.v1.json').read()
record('actual-historical-v13-guard-unchanged-and-scope-verified-from-retained-archive', 'actual', {'v13SegmentOnHost': 'refuse'}, {'v13SegmentOnHost': v13},
       {'segmentBytesIdenticalBeforeAfter': b_same, 'manifestSha256': sha(REPO / (DC + 'reviews/candidate-subject.v13.json')),
        'manifestShaEqualsHistoricalConstant': sha(REPO / (DC + 'reviews/candidate-subject.v13.json')) == C.HISTORICAL_V13_MANIFEST_SHA256,
        'snapshotMembersPresentOnHost': sum(1 for r in hm['files'] if (Path(hm['snapshotRoot']) / r['path']).exists()), 'snapshotMembers': len(hm['files']),
        'archiveSummarySha256EqualsManifestRow': bsha(member) == row['sha256'], 'archiveSummaryMatrixCells': json.loads(member)['native']['matrixCells'],
        'historicalConstant': C.HISTORICAL_V13_MATRIX_CELLS})
if not (b_same and bsha(member) == row['sha256'] and json.loads(member)['native']['matrixCells'] == C.HISTORICAL_V13_MATRIX_CELLS):
    RESULTS[-1]['ok'] = False


def undefined_names(path):
    tree = ast.parse(path.read_text())
    bound, used = set(dir(builtins)) | {'__file__'}, set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Name):
            (bound if isinstance(node.ctx, (ast.Store, ast.Del)) else used).add(node.id)
        elif isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            bound.add(node.name)
        elif isinstance(node, ast.arg):
            bound.add(node.arg)
        elif isinstance(node, (ast.Import, ast.ImportFrom)):
            bound |= {(a.asname or a.name).split('.')[0] for a in node.names}
        elif isinstance(node, ast.ExceptHandler) and node.name:
            bound.add(node.name)
    return sorted(used - bound)


record('static-after-script-and-helper-have-no-unbound-names', 'static', {}, {},
       {'afterScript': undefined_names(APP / SCRIPT), 'afterHelper': undefined_names(APP / HELPER), 'beforeScript': undefined_names(BEFORE / SCRIPT)})
if undefined_names(APP / SCRIPT) or undefined_names(APP / HELPER):
    RESULTS[-1]['ok'] = False


# ------------------------------------------------------------------ mutation worlds (runtime only)
def receipt_world(cid):
    root = CTL / cid / 'root'
    if root.exists():
        shutil.rmtree(root)
    (root / SUBJECT['path']).parent.mkdir(parents=True)
    shutil.copyfile(REPO / SUBJECT['path'], root / SUBJECT['path'])
    shutil.copytree(REPO / FR, root / FR)
    shutil.copyfile(REPO / CNT['path'], root / CNT['path'])
    return root


def rewrite(path, fn):
    doc = load(path)
    fn(doc)
    path.write_text(json.dumps(doc, indent=1) + '\n')


def snapshot_world(cid, mutate_snapshot=None, keep_manifest_rows=False, mutate_receipts=None):
    root = receipt_world(cid)
    overlay = CTL / cid / 'snapshot'
    manifest = load(REPO / SUBJECT['path'])
    commands = load(REPO / CMD['path'])
    needed = {r['source'] for r in commands['commands']} | {DC + p for p in (
        'foundation/source-pins.v1.json', 'foundation/evaluator3-source-pins.v1.json', 'workflows/command-inventory.v1.json',
        'validation-summary.v1.json', 'native/native-capability-matrix.v2.json', 'native/native-evidence-report.v2.json',
        'workflows/workflows-report.v1.json', 'integration-report.v1.json', 'foundation/identity-report.json',
        'security/security-lifecycle-report.v1.json', 'foundation/validation-report.json')}
    for rel in needed:
        (overlay / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(Path(SNAP) / rel, overlay / rel)
    if mutate_snapshot:
        mutate_snapshot(overlay)
    if mutate_receipts:
        mutate_receipts(root)
    manifest['snapshotRoot'] = str(overlay)
    if not keep_manifest_rows:
        for r in manifest['files']:
            if r['path'] in needed:
                r['sha256'] = sha(overlay / r['path'])
    (root / SUBJECT['path']).write_text(json.dumps(manifest, indent=1) + '\n')
    subject = {'path': SUBJECT['path'], 'sha256': sha(root / SUBJECT['path'])}
    rewrite(root / CMD['path'], lambda d: d.__setitem__('subjectManifestSha256', subject['sha256']))
    cmd = {'path': CMD['path'], 'sha256': sha(root / CMD['path'])}
    return root, subject, str(overlay), cmd


def helpers_both(root, subject=SUBJECT, cmd=CMD, cnt=CNT, snapshot=SNAP):
    prev = load(Path(snapshot) / (DC + 'validation-summary.v1.json'))
    return {'before': outcome(lambda: OLD_H.current_reference_summary(root, subject, cmd, cnt, copy.deepcopy(prev))),
            'after': outcome(lambda: NEW_H.current_reference_summary(root, subject, cmd, cnt, copy.deepcopy(prev)))}


def boundary_new(root, subject, snapshot, cmd, cnt=CNT):
    return outcome(lambda: NEW_H.accepted_summary_boundary(root, subject, snapshot, cmd, cnt))


def value(o, *path):
    node = o.get('value')
    for k in path:
        if not isinstance(node, dict):
            return None
        node = node.get(k)
    return node


# receipt-side controls
def receipt_control(cid, mutate, expected, facts_fn=None, cmd_rehash=False, cnt_rehash=False):
    root = receipt_world(cid)
    mutate(root)
    cmd = {'path': CMD['path'], 'sha256': sha(root / CMD['path'])} if cmd_rehash else CMD
    cnt = {'path': CNT['path'], 'sha256': sha(root / CNT['path'])} if cnt_rehash else CNT
    obs = helpers_both(root, SUBJECT, cmd, cnt)
    record(cid, 'receipt-mutation', expected, obs, facts_fn(obs) if facts_fn else None)


receipt_control('receipt-missing-executed-native-report', lambda r: (r / FR / 'native-report.json').unlink(), {'before': 'refuse', 'after': 'refuse'})
receipt_control('receipt-forged-executed-native-count', lambda r: rewrite(r / FR / 'native-report.json', lambda d: d['cases'].update(passed=999, total=999)),
                {'before': 'pass', 'after': 'refuse'}, lambda o: {'beforeClaimsNative': value(o['before'], 'native', 'casesPassed')})
receipt_control('receipt-forged-workflow-surface-count', lambda r: rewrite(r / FR / 'workflow-surface-report.json', lambda d: d.update(passed=1817)),
                {'before': 'pass', 'after': 'refuse'}, lambda o: {'beforeClaimsWorkflows': value(o['before'], 'workflows', 'checksPassed')})
# A consistent forgery: one more check entry and a matching passed count, so only report custody can catch it.
receipt_control('receipt-forged-integration-count',
                lambda r: rewrite(r / FR / 'integration.json', lambda d: (d['checks'].append(copy.deepcopy(d['checks'][-1])), d.update(passed=len(d['checks'])))),
                {'before': 'pass', 'after': 'refuse'}, lambda o: {'beforeClaimsIntegration': value(o['before'], 'integration', 'checksPassed')})
receipt_control('receipt-forged-security-count', lambda r: rewrite(r / FR / 'security.json', lambda d: d['counts'].update({'pass': 463})),
                {'before': 'pass', 'after': 'refuse'}, lambda o: {'beforeClaimsSecurity': value(o['before'], 'security', 'casesPassed')})


def _forge_command_source(r):
    """The same forged source digest in the bound and the original runner receipts, with the derived view re-pointed,
    so the runner-receipt guard is satisfied and only the source pin guard can refuse."""
    rewrite(r / CMD['path'], lambda d: d['commands'][3].update(sourceSha256='0' * 64))
    rewrite(r / FR / 'runner-original-reference-checks.json', lambda d: d['commands'][3].update(sourceSha256='0' * 64))
    rewrite(r / FR / 'report.json', lambda d: d.update(originalRunnerReceiptSha256=sha(r / FR / 'runner-original-reference-checks.json')))


receipt_control('receipt-command-source-sha-mismatch', _forge_command_source, {'before': 'refuse', 'after': 'refuse'}, cmd_rehash=True)
receipt_control('receipt-current-profile-pins-mismatch', lambda r: rewrite(r / CMD['path'], lambda d: d.update(currentProfilePinsSha256='0' * 64)),
                {'before': 'refuse', 'after': 'refuse'}, cmd_rehash=True)
root_ref = receipt_world('receipt-command-ref-sha-mismatch')
obs = {'before': outcome(lambda: OLD_H.current_reference_summary(root_ref, SUBJECT, dict(CMD, sha256='0' * 64), CNT, {})),
       'after': outcome(lambda: NEW_H.current_reference_summary(root_ref, SUBJECT, dict(CMD, sha256='0' * 64), CNT, {}))}
record('receipt-command-ref-sha-mismatch', 'receipt-mutation', {'before': 'refuse', 'after': 'refuse'}, obs)
receipt_control('receipt-identity-counts-inconsistent', lambda r: rewrite(r / CNT['path'], lambda d: d.update(passingCalls=1597)),
                {'before': 'refuse', 'after': 'refuse'}, cnt_rehash=True)
receipt_control('receipt-original-runner-receipt-altered', lambda r: rewrite(r / FR / 'runner-original-reference-checks.json', lambda d: d.update(passed=True, note='altered')),
                {'before': 'pass', 'after': 'refuse'})
receipt_control('receipt-workflows-parent-report-hash-mismatch', lambda r: rewrite(r / FR / 'workflows.json', lambda d: d['check'].update(reportSha256='0' * 64)),
                {'before': 'pass', 'after': 'refuse'})
receipt_control('receipt-evaluator-child-stdout-altered',
                lambda r: (lambda p: p.write_bytes(p.read_bytes() + b' '))(sorted((r / FR / 'evaluator3').glob('*.stdout'))[0]),
                {'before': 'refuse', 'after': 'refuse'})


# snapshot-side controls (manifest and receipt subject binding re-derived so the targeted guard is reached)
def snap_control(cid, mutate_snapshot, expected, keep_rows=False, mutate_receipts=None, facts_fn=None, with_boundary=True, old_boundary=False):
    root, subject, overlay, cmd = snapshot_world(cid, mutate_snapshot, keep_rows, mutate_receipts)
    obs = helpers_both(root, subject, cmd, CNT, overlay)
    if with_boundary:
        obs['boundary'] = boundary_new(root, subject, overlay, cmd)
    if old_boundary:
        obs['oldScriptBoundary'] = outcome(lambda: run_old_boundary(root, app_fields(subject, overlay, cmd)))
        obs['newScriptBoundary'] = outcome(lambda: run_new_boundary(root, app_fields(subject, overlay, cmd)))
    record(cid, 'snapshot-mutation', expected, obs, facts_fn(obs) if facts_fn else None)


def edit_snap(rel, fn):
    return lambda overlay: rewrite(overlay / (DC + rel), fn)


snap_control('snapshot-lawful-historical-summary-vintage-differs',
             edit_snap('validation-summary.v1.json', lambda d: (d['native'].update(casesPassed=111), d['workflows'].update(checksPassed=222))),
             {'before': 'pass', 'after': 'pass', 'boundary': 'pass', 'oldScriptBoundary': 'refuse', 'newScriptBoundary': 'pass'}, old_boundary=True,
             facts_fn=lambda o: {'recorded': [r for r in (value(o['boundary'], 'acceptedSummaryCounts') or []) if r['field'] in ('native.casesPassed', 'workflows.checksPassed')]})
snap_control('snapshot-unpinned-historical-summary-change', edit_snap('validation-summary.v1.json', lambda d: d['native'].update(casesPassed=111)),
             {'boundary': 'refuse'}, keep_rows=True)
snap_control('snapshot-historical-summary-internally-inconsistent', edit_snap('validation-summary.v1.json', lambda d: d['foundation'].update(checksPassed=1999)),
             {'boundary': 'refuse'})
snap_control('snapshot-historical-summary-matrix-cells-60', edit_snap('validation-summary.v1.json', lambda d: d['native'].update(matrixCells=60)),
             {'boundary': 'refuse'})
snap_control('snapshot-frozen-native-report-not-executed-copy', edit_snap('native/native-evidence-report.v2.json', lambda d: d.update(standing=d.get('standing', '') + ' altered')),
             {'before': 'pass', 'after': 'refuse', 'boundary': 'refuse'})
snap_control('snapshot-frozen-integration-report-not-executed-copy', edit_snap('integration-report.v1.json', lambda d: d.update(standing='altered')),
             {'before': 'pass', 'after': 'refuse', 'boundary': 'refuse'})
snap_control('snapshot-and-receipt-consistent-qualified-cell',
             edit_snap('native/native-evidence-report.v2.json', lambda d: d['matrix'].update(qualifiedCells=1)),
             {'before': 'refuse', 'after': 'refuse', 'boundary': 'refuse'},
             mutate_receipts=lambda r: rewrite(r / FR / 'native-report.json', lambda d: d['matrix'].update(qualifiedCells=1)))
snap_control('snapshot-matrix-cell-removed', edit_snap('native/native-capability-matrix.v2.json', lambda d: d['cells'].pop()),
             {'before': 'refuse', 'after': 'refuse', 'boundary': 'refuse'})
snap_control('snapshot-matrix-platform-qualified', edit_snap('native/native-capability-matrix.v2.json', lambda d: d.update(platformQualified=True)),
             {'before': 'pass', 'after': 'refuse', 'boundary': 'refuse'})
snap_control('snapshot-frozen-security-report-counts-differ', edit_snap('security/security-lifecycle-report.v1.json', lambda d: d['counts'].update({'pass': 463})),
             {'before': 'pass', 'after': 'pass', 'boundary': 'refuse'})
snap_control('snapshot-inventory-golden-removed-is-measured', edit_snap('workflows/command-inventory.v1.json', lambda d: d['goldens'].pop()),
             {'before': 'pass', 'after': 'pass', 'boundary': 'pass'},
             facts_fn=lambda o: {'beforeGoldens': value(o['before'], 'workflows', 'goldens'), 'afterGoldens': value(o['after'], 'workflows', 'goldens')})
snap_control('snapshot-command-source-bytes-unpinned', lambda overlay: (lambda p: p.write_bytes(p.read_bytes() + b'\n# altered\n'))(overlay / load(REPO / CMD['path'])['commands'][3]['source']),
             {'before': 'refuse', 'after': 'refuse', 'boundary': 'refuse'}, keep_rows=True)

last = RESULTS[-2]
if last['id'] == 'snapshot-inventory-golden-removed-is-measured' and not (last['facts']['beforeGoldens'] == 43 and last['facts']['afterGoldens'] == 42):
    last['ok'] = False
lawful = next(r for r in RESULTS if r['id'] == 'snapshot-lawful-historical-summary-vintage-differs')
if [(x['acceptedSummary'], x['current']) for x in lawful['facts']['recorded']] != [(111, 380), (222, 1816)]:
    lawful['ok'] = False

report = {
    'standing': 'Boundary controls over actual frozen39 receipts and exact historical summary; mutation worlds are runtime-only copies. The gated whole application script was not run; no accepted peer verdict or application stage is fabricated.',
    'inputs': {'subject': SUBJECT, 'commands': CMD, 'identityCounts': CNT, 'snapshotRoot': SNAP,
               'beforeScriptSha256': sha(BEFORE / SCRIPT), 'afterScriptSha256': sha(APP / SCRIPT),
               'beforeHelperSha256': sha(BEFORE / HELPER), 'afterHelperSha256': sha(APP / HELPER),
               'segments': {'oldA': OLD_A[:2], 'newA': NEW_A[:2], 'oldB': OLD_B[:2], 'newB': NEW_B[:2], 'oldC': OLD_C[:2], 'newC': NEW_C[:2]}},
    'count': len(RESULTS), 'failed': [r['id'] for r in RESULTS if not r['ok']], 'passed': all(r['ok'] for r in RESULTS), 'results': RESULTS,
}
(RT / 'receipts').mkdir(exist_ok=True)
(RT / 'receipts/boundary-controls.json').write_text(json.dumps(report, indent=1, default=str) + '\n')
print(json.dumps({'count': report['count'], 'passed': report['passed'], 'failed': report['failed'],
                  'rows': [(r['id'], r['ok'], {k: v['result'] + ('' if v['result'] == 'pass' else ' ' + v.get('at', '')) for k, v in r['observed'].items()}) for r in RESULTS]}, indent=1))
sys.exit(0 if report['passed'] else 1)
