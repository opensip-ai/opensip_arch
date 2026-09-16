import copy
import json
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from common import ROOT, DC, ARCH, load, jload, Recorder

S = ROOT / 'm1-history-selection-subject-01'
h = load(S / 'history.py', 'history_subject')
pins = {p['role']: Path(p['path']) for p in jload(S / 'input-pins.json')['files']}
common = jload(pins['common']); report = jload(pins['report-schema']); inv = jload(pins['command-inventory'])
R = Recorder('m1-history-selection-subject-01')


def rid(n):
    return 'run3:' + format(n, '064x')


# Controls
for i, bad in enumerate((['latest'], [rid(1)[:20]], [rid(1) + ',' + rid(2)], [rid(i) for i in range(5)], [rid(1), rid(1)])):
    o = R.outcome(lambda: h.admit_request(bad, 'html'))
    R.record('HIS-C1.%d' % i, 'control-invalid', 'latest/prefix/comma/5 IDs/duplicate refuse before lookup', o, o.get('raised') == 'HistoryRefusal')
calls = []
sel = h.plan_selection(h.admit_request([rid(9), rid(3)], 'html'), rid(3))
out = h.resolve_slots(sel, lambda r: calls.append(r) or {'state': 'unavailable', 'runId': r, 'availability': 'purged'})
R.record('HIS-C2', 'control-valid', 'current-run equality after analysis uses no lookup; order preserved; no fallback', {'slots': out, 'lookups': calls},
         out[1] == {'state': 'current-run', 'runId': rid(3)} and calls == [rid(9)])
auto = {}
exec(compile('\n'.join([l for l in []]), 'x', 'exec'), auto)
R.record('HIS-C3', 'control-valid', 'explicit selection contains no baseline or recent Run it was not given', sel['requestedRunIds'], sel['requestedRunIds'] == [rid(9), rid(3)])

# F: non-HTML format route contradicts owner route
dd = common['$defs']['DomainDetailCode']['enum']
o = R.outcome(lambda: h.admit_request([rid(1)], 'json'))
wf = (ARCH / 'docs/v2/contracts/product-v1/workflows-and-surfaces.md').read_text().splitlines()
R.record('HIS-F1', 'finding', 'flag used without an HTML format follows owner route REQUEST.UNKNOWN_OPTION / OUTPUT.FORMAT_NOT_APPLICABLE (2)',
         {'reference': o, 'ownerLine1141_1142': ' '.join(wf[1140:1142]), 'existingDetails': [c for c in dd if c in ('OUTPUT.FORMAT_NOT_APPLICABLE', 'EVALUATION.SELECTION_LIMIT')],
          'proposedDetailRegistered': 'REPORT.HISTORY_SELECTION_INVALID' in dd},
         o.get('raised') == 'HistoryRefusal' and 'OUTPUT.FORMAT_NOT_APPLICABLE' in dd,
         'proposal routes format misuse and over-limit selections to one new detail under REQUEST.UNSATISFIABLE; existing format-applicability and selection-limit details are not analysed')

# F: host fault misclassified as user request rejection
o = R.outcome(lambda: h.plan_selection(h.admit_request([rid(1)], 'html'), 'run3:not-a-run'))
R.record('HIS-F2', 'finding', 'an invalid host-supplied currentRunId is an internal source fault, not REPORT.HISTORY_SELECTION_INVALID', o, o.get('raised') == 'HistoryRefusal')

# F: other Runs minted by this invocation (pivot analysis) are ordinary snapshot lookups
ledger = report['$defs']['InvocationLedgerV1']['properties']['planVariant']['enum']
roles = report['$defs']['LedgerStepV1']['properties']['planRole']['enum']
variants = [v for v in ledger if 'pivot' in v] + [r for r in roles if 'pivot' in r]
sel = h.plan_selection(h.admit_request([rid(7)], 'html'), rid(3))  # rid(7) = pivot Run minted earlier in this invocation
R.record('HIS-F3', 'finding', 'contract defines the read-snapshot point and treatment of a requested pivot/baseline Run minted by the same invocation',
         {'slots': sel['slots'], 'planningTokensMentioningPivot': variants[:8]}, sel['slots'][0]['source'] == 'exact-retained-lookup',
         'only equality with the primary current Run is special-cased; snapshot timing relative to this invocation\'s own commits is undefined')

# F: lookup result shape not the owner HistoryRunV1 and no project binding
hr = report['$defs']['HistoryRunV1']['oneOf'][0]['required']
o = R.outcome(lambda: h.resolve_slots(h.plan_selection(h.admit_request([rid(1)], 'html'), None), lambda r: {'state': 'present', 'runId': r, 'projectId': 'other-project'}))
R.record('HIS-F4', 'finding', 'present slot is checked against owner HistoryRunV1 and bound to the admitted project', {'ownerPresentRequired': hr, 'accepted': o},
         'returned' in o, 'synthetic callback; reference cannot and does not claim namespace custody, but no carrier-side binding is specified either')

# F: owning query unit named by RP-DO-12 is not pinned
obl = [x for x in jload(ROOT / 'm1-report-projection-subject-07/owner/design-obligations.v1.json')['obligations'] if x['id'] == 'RP-DO-12'][0]
R.record('HIS-F5', 'finding', 'proposal pins/types the RP-DO-12 owning unit (query-projection-contract.v3 section 1 run.show item)',
         {'owningDesignUnit': obl['owningDesignUnit'], 'closureCriterion': obl['closureCriterion'], 'subjectPins': sorted(str(p) for p in pins.values())},
         not any('query-projection' in str(p) for p in pins.values()))

# F: flag record not specified; inventory shape requires owner/class/join
R.record('HIS-F6', 'finding', 'exact flag record {flag, owner, class, join} supplied for the eight HTML rows',
         {'inventoryFlagShape': sorted(inv['commands'][0]['flags'][0]), 'htmlCommands': [c['name'] for c in inv['commands'] if 'html' in c['formats']]},
         'owner' in inv['commands'][0]['flags'][0], 'contract prose gives spelling only; no owner/class/join text or value grammar is frozen')

# Derivation: fixed disclosure overhead
worst = {'policy': 'explicit-run-ids.1', 'requestedRunIds': [rid(2**255 + i) for i in range(4)], 'currentRunId': rid(2**255 + 9),
         'slots': [{'runId': rid(2**255 + i), 'source': 'exact-retained-lookup'} for i in range(4)]}
unavail = [{'state': 'unavailable', 'runId': rid(2**255 + i), 'availability': 'unavailable'} for i in range(4)]
canon = load(DC / 'foundation/canonical.py', 'canon')
R.record('HIS-D1', 'derivation', 'canonical bytes of maximal selection record and four minimal unavailable rows (detail excluded)',
         {'selectionBytes': len(canon.canonical(worst)), 'unavailableRowsBytes': len(canon.canonical(unavail)),
          'budgetProfileRootMemberMaxBytes': report['$defs']['BudgetProfileV1']['properties']['rootMemberMaxBytes']}, True)
R.dump(Path(__file__).resolve().parent / 'history-results.json')
