"""P04 — extract the specific NEW-LAW control cases from the execution-inputs checker and report
their measured values compactly: the external sourceUniverse join, the precedence table, the
(null,null) carrier, selected-U unsupported retention, the required-cell bridge, and any full-Run rows."""
import json, os, subprocess

PY = '/tmp/opensip-architecture-review-env/bin/python'
KIT = '/tmp/opensip-design-corrections/claude-independent-design.v33/disposable/kit33'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v33/receipts'
p = os.path.join(KIT, 'docs/coop/design-corrections/foundation/check-execution-inputs.v1.py')
r = subprocess.run([PY, '-I', '-B', p], capture_output=True, text=True, cwd=os.path.dirname(p))
d = json.loads(r.stdout)
cases = d['cases']
R = {'returncode': r.returncode, 'totalCases': len(cases), 'mismatches': d['mismatches'],
     'causeRetentionStatement': d['causeRetention']}
print('cases=%d mismatches=%d' % (len(cases), len(d['mismatches'])))

def show(title, pred, fields):
    sel = [c for c in cases if pred(c)]
    print('\n=== %s (%d) ===' % (title, len(sel)))
    out = []
    for c in sel:
        row = {'case': c['case'], 'result': c['result']}
        for f in fields:
            if c.get(f) not in (None, [], {}):
                row[f] = c[f]
        out.append(row)
        print('   %-52s %-7s %s' % (c['case'][:52], c['result'],
                                    json.dumps({k: v for k, v in row.items()
                                                if k not in ('case', 'result')})[:170]))
    return out


R['externalUniverseJoin'] = show(
    'external sourceUniverse-to-binding join',
    lambda c: c.get('accountSourceUniverses'),
    ['accountSourceUniverses', 'refusals'])
R['precedenceControls'] = show(
    'FIRST-MATCH precedence table controls',
    lambda c: c.get('precedenceTable'),
    ['precedenceTable', 'derivedAccountStates'])
R['fullRunRows'] = show(
    'full-Run rows',
    lambda c: c.get('fullRun') is not None,
    ['fullRun', 'derivedOutcomeStates'])
R['nullNullCarrier'] = show(
    '(null,null) derived carrier for missing work',
    lambda c: any(p == [None, None] for p in (c.get('deficiencyPairs') or [])),
    ['deficiencyCauses', 'deficiencyPairs', 'derivedOutcomeStates', 'rowComplete'])
R['unsupportedTyped'] = show(
    'unsupported-typed / matrix cause',
    lambda c: 'unsupported' in c['case'] or 'unsupported' in json.dumps(c.get('derivedAccountStates') or []),
    ['deficiencyCauses', 'derivedAccountStates', 'derivedOutcomeStates', 'refusals'])
R['refusingControls'] = show(
    'controls that REFUSE (negative side)',
    lambda c: c['result'] == 'REFUSE',
    ['refusals'])

R['summary'] = {
    'casesWithExternalUniverseJoin': len(R['externalUniverseJoin']),
    'precedenceControls': len(R['precedenceControls']),
    'fullRunRows': len(R['fullRunRows']),
    'nullNullCarrierCases': len(R['nullNullCarrier']),
    'refusingControls': len(R['refusingControls']),
    'admittingControls': sum(1 for c in cases if c['result'] == 'ADMIT'),
    'zeroMismatches': d['mismatches'] == []}
print('\nsummary:', json.dumps(R['summary']))
json.dump(R, open(os.path.join(OUT, 'p04-newlawcontrols.json'), 'w'), indent=1, default=str)
print('wrote p04-newlawcontrols.json')
