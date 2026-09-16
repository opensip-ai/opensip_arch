"""Validate the one-key coverage correction with the unchanged owned validator.

Run with Python -I -B. All external application source is hash checked and
compiled directly from those bytes; no imported application pyc is used.
This is design bookkeeping, not executed product qualification.
"""
import copy
import hashlib
import json
from pathlib import Path
import types

HERE = Path(__file__).resolve().parent


def main():
    pins = json.loads((HERE / 'input-pins.json').read_bytes())
    content = {}
    for pin in pins['files']:
        raw = Path(pin['path']).read_bytes()
        assert len(raw) == pin['bytes'] and hashlib.sha256(raw).hexdigest() == pin['sha256'], pin['path']
        content[pin['path']] = raw
    def read(path):
        return json.loads(content[path])
    correction = json.loads((HERE / 'successor.json').read_bytes())
    parent_raw = content[correction['parent']['path']]
    assert hashlib.sha256(parent_raw).hexdigest() == correction['parent']['sha256']
    assert len(parent_raw) == correction['parent']['bytes']
    base = read(correction['parent']['path'])
    corrected = json.loads((HERE / 'implementation-coverage.v3.json').read_bytes())
    expected = copy.deepcopy(base)
    asset = 'crates/reporting/src/assets.rs'
    assert asset not in expected['moduleFirstMilestone']
    expected['moduleFirstMilestone'][asset] = 'M1'
    assert corrected == expected, 'successor has changes outside the exact one-key scope'
    p = pins['roles']['validator']
    validator = types.ModuleType('owned_planning_validator')
    validator.__file__ = p
    exec(compile(content[p], p, 'exec'), validator.__dict__)
    inventory = read(pins['roles']['inventory'])
    root = Path(pins['architectureRoot'])
    for pin in base['sources'].values():
        assert hashlib.sha256(content[str(root / pin['path'])]).hexdigest() == pin['sha256'], pin['path']
    sources = {k: (json.loads(content[str(root / v['path'])]) if v['path'].endswith('.json') else content[str(root / v['path'])].decode()) for k, v in base['sources'].items()}
    def outcome(data, inputs):
        try:
            validator.validate_coverage(data, inputs, inventory)
            return 'valid'
        except ValueError as exc:
            return str(exc)
    assert outcome(base, sources) == 'Missing/extra module milestone prerequisite'
    assert outcome(corrected, sources) == 'valid'
    delivery_groups = ('commands', 'queryOperations', 'renderers', 'capabilityCells', 'workflowGoldens')
    asset_rows = [(g, row['id'], row['milestone']) for g in delivery_groups for row in corrected['groups'][g] if asset in row['owners']]
    assert asset_rows == [('commands', 'version', 'M1')]
    # The independently pending report overlay is checked for composition,
    # without selecting its semantics or invoking its workaround branch.
    overlay = read(pins['roles']['reportOverlay'])
    applied = copy.deepcopy(corrected)
    for change in overlay['rowChanges']:
        row = applied['groups'][change['group']][change['index']]
        assert row['id'] == change['id']
        row['source'] = change['source']
        row.update(change.get('fields', {}))
        for key in ('owners', 'reviewIssues'):
            if key in change:
                row[key] = change[key]
        if 'verificationMethod' in change:
            row['verification']['method'] = change['verificationMethod']
    for addition in overlay['rowAdditions']:
        applied['groups'][addition['group']].append(addition['row'])
    applied['reviewIssues'] += overlay['reviewIssueAdditions']
    next_sources = dict(sources, commands=read(pins['roles']['reportInventory']))
    workflow_path = base['sources']['workflows-and-surfaces']['path']
    lines = next_sources['workflows-and-surfaces'].splitlines(keepends=True)
    for row in read(pins['roles']['reportPassages'])['overrides']:
        if row['path'] == workflow_path:
            assert lines[row['line'] - 1].rstrip('\n') == row['before']
            lines[row['line'] - 1] = row['after'] + '\n'
    next_sources['workflows-and-surfaces'] = ''.join(lines)
    assert outcome(applied, next_sources) == 'valid'
    controls = {}
    for value in ('M0', 'M6', 'unknown'):
        trial = copy.deepcopy(corrected)
        trial['moduleFirstMilestone'][asset] = value
        controls[value] = outcome(trial, sources)
    assert controls['M0'] == 'valid'  # Ordering alone cannot select the owner value.
    assert controls['M6'].startswith('Delivery precedes module prerequisite:')
    assert controls['unknown'] == 'Missing/extra module milestone prerequisite'
    # Independently preserve the validator's metadata-drift detection.
    drift = copy.deepcopy(applied)
    fit = next(r for r in drift['groups']['commands'] if r['id'] == 'fit')
    fit['parityFields'] = next(r for r in base['groups']['commands'] if r['id'] == 'fit')['parityFields']
    assert outcome(drift, next_sources) == 'Command metadata drift'
    print(json.dumps({'passed': True, 'selected': False, 'productQualification': False,
                      'externalPins': len(content), 'baseRows': sum(map(len, corrected['groups'].values())),
                      'overlayRows': sum(map(len, applied['groups'].values())), 'assetDeliveryRows': asset_rows,
                      'correctedBase': 'valid', 'pendingReportOverlayComposition': 'valid',
                      'validatorWorkaroundUsed': False, 'milestoneControls': controls}, indent=2))


if __name__ == '__main__':
    main()
