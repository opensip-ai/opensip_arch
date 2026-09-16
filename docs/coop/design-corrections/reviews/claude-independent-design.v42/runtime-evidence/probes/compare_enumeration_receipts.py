"""Compare the check-enumeration receipts this review produced on source41 and source42 (work/enumeration-receipt.*.json):
case populations, shared-case field identity (path-bearing fields excluded) and the new cases. Writes
receipts/enumeration-case-population.json."""
import hashlib, json
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v42')
PATHY = {'ownedHashes', 'receiptPath', 'hashes', 'report', 'receipt', 'v8ReceiptMisplaced', 'v10ReceiptPreserved'}


def strip(x):
    if isinstance(x, dict):
        return {k: strip(v) for k, v in x.items() if k not in PATHY}
    if isinstance(x, list):
        return [strip(v) for v in x]
    return x


docs = {}
out = {}
for label in ('source41', 'source42'):
    p = RT / ('work/enumeration-receipt.' + label + '.json')
    raw = p.read_bytes()
    d = json.loads(raw)
    docs[label] = d
    cases = {c['case']: c for c in d.get('cases') or []}
    out[label] = {'receipt': str(p), 'sha256': hashlib.sha256(raw).hexdigest(), 'cases': len(cases), 'mismatches': len(d.get('mismatches') or []),
                  'topKeys': sorted(d)}
c41 = {c['case']: c for c in docs['source41'].get('cases') or []}
c42 = {c['case']: c for c in docs['source42'].get('cases') or []}
shared = sorted(set(c41) & set(c42))
out['compare41to42'] = {'shared': len(shared), 'onlyA': sorted(set(c41) - set(c42)), 'onlyB': sorted(set(c42) - set(c41)),
                        'differingSharedCases': {n: sorted(k for k in set(strip(c41[n])) | set(strip(c42[n])) if strip(c41[n]).get(k) != strip(c42[n]).get(k))
                                                 for n in shared if strip(c41[n]) != strip(c42[n])},
                        'newCaseResults': {n: {'result': c42[n].get('result'), 'refusals': c42[n].get('refusals')} for n in sorted(set(c42) - set(c41))}}
for key in ('unit_root_cases', 'unitRootCases', 'tsjsUnitKindControls', 'internalUnitRootControls'):
    if key in docs['source41'] or key in docs['source42']:
        out['compare41to42'][key + 'Equal'] = strip(docs['source41'].get(key)) == strip(docs['source42'].get(key))
(RT / 'receipts/enumeration-case-population.json').write_text(json.dumps(out, indent=1))
print(json.dumps(out, indent=1))
