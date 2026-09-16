"""Resumed independent review: coverage prerequisite correction probes.

Run: python -I -B -X pycache_prefix=<empty> coverage_probes.py SUBJECT_COPY RESULTS_JSON
Independent of the subject's check.py except where a control runs it as a subprocess.
"""
import copy
import hashlib
import inspect
import json
import shutil
import subprocess
import sys
import types
from pathlib import Path

COPY, RESULTS = Path(sys.argv[1]), Path(sys.argv[2])
REVIEW = RESULTS.parent
SUBJECT05 = Path('/tmp/opensip-implementation/m1-report-projection-subject-05')
ASSET = 'crates/reporting/src/assets.rs'
DELIVERY = ('commands', 'queryOperations', 'renderers', 'capabilityCells', 'workflowGoldens')
out = {}


def sha(data):
    return hashlib.sha256(data).hexdigest()


pins = json.loads((COPY / 'input-pins.json').read_bytes())
content = {}
for pin in pins['files']:
    raw = Path(pin['path']).read_bytes()
    assert (len(raw), sha(raw)) == (pin['bytes'], pin['sha256']), pin['path']
    content[pin['path']] = raw
out['externalPins'] = {'count': len(content), 'allMatch': True,
                       'reportOverlayFromFrozenSubject05': all(p.startswith(str(SUBJECT05) + '/owner/') for p in (
                           pins['roles']['reportOverlay'], pins['roles']['reportInventory'], pins['roles']['reportPassages']))}
m05 = json.loads(Path(str(SUBJECT05) + '.json').read_bytes())
for f in m05['files']:
    assert sha((SUBJECT05 / f['path']).read_bytes()) == f['sha256'], f['path']
    if str(SUBJECT05 / f['path']) in content:
        assert f['sha256'] == sha(content[str(SUBJECT05 / f['path'])])
out['subject05'] = {'manifestSha256': sha(Path(str(SUBJECT05) + '.json').read_bytes()),
                    'standing': m05['standing'], 'allFilesMatch': True}

successor = json.loads((COPY / 'successor.json').read_bytes())
parent_raw = content[successor['parent']['path']]
assert (sha(parent_raw), len(parent_raw)) == (successor['parent']['sha256'], successor['parent']['bytes'])
v3_raw = (COPY / 'implementation-coverage.v3.json').read_bytes()
v2, v3 = json.loads(parent_raw), json.loads(v3_raw)


def diff(a, b, path=''):
    if type(a) is not type(b):
        return [(path, 'type')]
    if isinstance(a, dict):
        found = []
        for key in list(a) + [k for k in b if k not in a]:
            if key not in b:
                found.append((path + '/' + key, 'removed'))
            elif key not in a:
                found.append((path + '/' + key, 'added', b[key]))
            else:
                found += diff(a[key], b[key], path + '/' + key)
        if not found and list(a) != list(b):
            found.append((path, 'key-order'))
        return found
    if isinstance(a, list):
        if len(a) != len(b):
            return [(path, 'length')]
        return [d for i, (x, y) in enumerate(zip(a, b)) for d in diff(x, y, f'{path}/{i}')]
    return [] if a == b else [(path, 'changed', a, b)]


delta = diff(v2, v3)
module_order = list(v3['moduleFirstMilestone'])
assert delta == [('/moduleFirstMilestone/' + ASSET, 'added', 'M1')], delta
expected_bytes = json.dumps(dict(v2, moduleFirstMilestone=dict(v2['moduleFirstMilestone'], **{ASSET: 'M1'})),
                            indent=2, ensure_ascii=False) + '\n'
out['semanticDelta'] = {'changes': [list(d) for d in delta], 'appendedLast': module_order[-1] == ASSET,
                        'v2SerializationIsIndent2': json.dumps(v2, indent=2, ensure_ascii=False) + '\n' == parent_raw.decode(),
                        'v3BytesEqualIndent2WithOneKeyAppended': expected_bytes == v3_raw.decode(),
                        'byteGrowth': len(v3_raw) - len(parent_raw),
                        'standingTextUnchanged': v2['standing'] == v3['standing'],
                        'subjectManifestFieldsUnchanged': (v2['subjectManifest'], v2['subjectManifestSha256']) == (
                            v3['subjectManifest'], v3['subjectManifestSha256'])}
assert out['semanticDelta']['v3BytesEqualIndent2WithOneKeyAppended']

order = v3['milestoneOrder']
owners_min = {}
for group in DELIVERY:
    for row in v3['groups'][group]:
        for owner in row['owners']:
            owners_min[owner] = min(owners_min.get(owner, row['milestone']), row['milestone'], key=order.index)
mismatch = {k: (v, owners_min.get(k)) for k, v in v3['moduleFirstMilestone'].items() if owners_min.get(k) != v}
out['valueSelection'] = {
    'assetDeliveryRows': [(g, r['id'], r['milestone']) for g in DELIVERY for r in v3['groups'][g] if ASSET in r['owners']],
    'assetNonDeliveryRows': [(g, r['id'], r['milestone']) for g, rows in v3['groups'].items() if g not in DELIVERY
                             for r in rows if ASSET in r['owners']],
    'modulesWhoseValueEqualsEarliestOwningDeliveryRow': len(v3['moduleFirstMilestone']) - len(mismatch),
    'modulesTotal': len(v3['moduleFirstMilestone']),
    'conventionExceptions': mismatch,
    'milestoneStanding': {k: v3['milestoneStanding'][k] for k in ('M0', 'M1')} if isinstance(v3.get('milestoneStanding'), dict) else v3.get('milestoneStanding'),
}
assert owners_min[ASSET] == 'M1'

validator = types.ModuleType('review_owned_validator')
validator.__file__ = pins['roles']['validator']
exec(compile(content[pins['roles']['validator']], pins['roles']['validator'], 'exec'), validator.__dict__)
inventory = json.loads(content[pins['roles']['inventory']])
root = Path(pins['architectureRoot'])
sources = {k: (json.loads(content[str(root / v['path'])]) if v['path'].endswith('.json')
               else content[str(root / v['path'])].decode()) for k, v in v3['sources'].items()}
for v in v3['sources'].values():
    assert sha(content[str(root / v['path'])]) == v['sha256'], v['path']


def outcome(data, src):
    try:
        validator.validate_coverage(data, src, inventory)
        return 'valid'
    except ValueError as exc:
        return str(exc)


def with_value(data, value):
    trial = copy.deepcopy(data)
    if value is None:
        trial['moduleFirstMilestone'].pop(ASSET, None)
    else:
        trial['moduleFirstMilestone'][ASSET] = value
    return trial


values = [None, 'M0', 'M1', 'M2', 'M3', 'M4', 'M5', 'M6', 'M7', 'm1', 1]
out['validatorBase'] = {'parentV2': outcome(v2, sources), 'successorV3': outcome(v3, sources),
                        'assetValueMatrix': {str(v): outcome(with_value(v3, v), sources) for v in values}}
assert out['validatorBase']['successorV3'] == 'valid'

owner_files = [p for p in SUBJECT05.glob('*.py') if 'def apply_overlay' in p.read_text()]
assert len(owner_files) == 1, owner_files
owner = types.ModuleType('review_report05_owner')
owner.__file__ = str(owner_files[0])
sys.path_hooks  # no import-path mutation; compile from bytes only
exec(compile(owner_files[0].read_bytes(), str(owner_files[0]), 'exec'), owner.__dict__)
overlay = json.loads(content[pins['roles']['reportOverlay']])
signature = inspect.signature(owner.apply_overlay)
composed = owner.apply_overlay(copy.deepcopy(v3), overlay, with_workaround=False)
workaround = overlay.get('scopedValidatorWorkaround', {}).get('moduleFirstMilestone', {}).get('add')
next_sources = dict(sources, commands=json.loads(content[pins['roles']['reportInventory']]))
workflow_path = v3['sources']['workflows-and-surfaces']['path']
lines = next_sources['workflows-and-surfaces'].splitlines(keepends=True)
for row in json.loads(content[pins['roles']['reportPassages']])['overrides']:
    if row['path'] == workflow_path:
        assert lines[row['line'] - 1].rstrip('\n') == row['before']
        lines[row['line'] - 1] = row['after'] + '\n'
next_sources['workflows-and-surfaces'] = ''.join(lines)
out['pendingOverlay'] = {
    'composedBy': f'{owner_files[0].name}:apply_overlay{signature} with_workaround=False (subject05 own code, hash-verified)',
    'rowCount': sum(map(len, composed['groups'].values())),
    'composedValid': outcome(composed, next_sources),
    'assetRowsAfterComposition': [(g, r['id'], r['milestone']) for g in DELIVERY for r in composed['groups'][g] if ASSET in r['owners']],
    'overlayWorkaroundAdds': workaround,
    'assetValueMatrix': {str(v): outcome(with_value(composed, v), next_sources) for v in values},
    'withoutCorrectionUsingParentV2': outcome(owner.apply_overlay(copy.deepcopy(v2), overlay, with_workaround=False), next_sources),
}
assert out['pendingOverlay']['composedValid'] == 'valid'
drift = copy.deepcopy(composed)
fit = next(r for r in drift['groups']['commands'] if r['id'] == 'fit')
fit['parityFields'] = next(r for r in v2['groups']['commands'] if r['id'] == 'fit')['parityFields']
out['pendingOverlay']['commandMetadataDriftControl'] = outcome(drift, next_sources)

controls = {}
base_dir = REVIEW / 'work' / 'coverage-controls'
shutil.rmtree(base_dir, ignore_errors=True)


def control(label, mutate_v3=None, mutate_pins=None):
    work = base_dir / label
    shutil.copytree(COPY, work)
    if mutate_v3:
        data = json.loads((work / 'implementation-coverage.v3.json').read_bytes())
        mutate_v3(data)
        (work / 'implementation-coverage.v3.json').write_text(json.dumps(data, indent=1) + '\n')
    if mutate_pins:
        data = json.loads((work / 'input-pins.json').read_bytes())
        mutate_pins(data)
        (work / 'input-pins.json').write_text(json.dumps(data, indent=2) + '\n')
    p = subprocess.run([sys.executable, '-I', '-B', '-X', 'pycache_prefix=' + sys.pycache_prefix, str(work / 'check.py')],
                       capture_output=True, text=True, timeout=300)
    last = (p.stderr.strip().splitlines() or [''])[-1]
    controls[label] = {'exit': p.returncode, 'lastStderrLine': last[:200]}


control('unchanged-reformatted-semantic-equal', lambda d: None)
control('value-M0', lambda d: d['moduleFirstMilestone'].__setitem__(ASSET, 'M0'))
control('key-removed', lambda d: d['moduleFirstMilestone'].pop(ASSET))
control('extra-standing-edit', lambda d: d.__setitem__('standing', d['standing'] + ' edited'))
control('extra-row-milestone-edit', lambda d: d['groups']['commands'][0].__setitem__('milestone', 'M2'))
control('input-pin-digest-edit', mutate_pins=lambda d: d['files'][0].__setitem__('sha256', '0' * 64))
shutil.rmtree(base_dir)
out['checkPyControls'] = controls
assert controls['unchanged-reformatted-semantic-equal']['exit'] == 0
assert all(v['exit'] != 0 for k, v in controls.items() if k != 'unchanged-reformatted-semantic-equal'), controls

RESULTS.write_text(json.dumps(out, indent=2, default=list) + '\n')
print(json.dumps({'passed': True, 'semanticDelta': out['semanticDelta']['changes'],
                  'base': out['validatorBase']['assetValueMatrix'], 'overlay': out['pendingOverlay']['composedValid'],
                  'controls': {k: v['exit'] for k, v in controls.items()}}, default=list))
