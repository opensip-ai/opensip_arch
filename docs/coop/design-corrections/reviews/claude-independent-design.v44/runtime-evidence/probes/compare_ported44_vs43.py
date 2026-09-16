"""Compare every ported scope-preservation probe receipt on source44 with this origin's own source43 receipt of the same probe
(read-only history): per case ok and observed equality, cases added/removed. Evidence of preserved behavior only.
Writes only receipts/ported44-vs43.json."""
import json
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v44')
R43 = Path('/tmp/opensip-design-corrections/claude-independent-design.v43/receipts/probes')
PAIRS = [('policy-v40-on44.json', 'policy-v40-on43.json'), ('native-v40-on44.json', 'native-v40-on43.json'),
         ('runterm-adv-v40-on44.json', 'runterm-adv-v40-on43.json'), ('query-carriers.json', 'query-carriers.json'),
         ('carrier-readonly.json', 'carrier-readonly.json'), ('comparison-knowledge.json', 'comparison-knowledge.json'),
         ('repair2.json', 'repair2.json'), ('run-termination-s7.json', 'run-termination-s7.json'),
         ('native-custody-fallback.json', 'native-custody-fallback.json'), ('capture-joins-on44.json', 'capture-joins-on43.json')]


def cases(doc):
    if isinstance(doc, dict):
        for k in ('rows', 'cases', 'results'):
            if isinstance(doc.get(k), list):
                return {(r.get('case') or r.get('name') or json.dumps(r, sort_keys=True)[:80]) if isinstance(r, dict) else json.dumps(r)[:80]: r for r in doc[k]}
    if isinstance(doc, list):
        return {(r[0] if isinstance(r, list) else json.dumps(r, sort_keys=True)[:80]): r for r in doc}
    return {}


out = {}
for new, old in PAIRS:
    p44, p43 = RT / 'receipts/probes' / new, R43 / old
    rec = {'receipt44': str(p44), 'receipt43': str(p43), 'exists44': p44.exists(), 'exists43': p43.exists()}
    if p44.exists() and p43.exists():
        d44, d43 = json.loads(p44.read_text()), json.loads(p43.read_text())
        c44, c43 = cases(d44), cases(d43)
        rec['wholeReceiptEqual'] = d44 == d43
        rec['cases44'], rec['cases43'] = len(c44), len(c43)
        rec['added'], rec['removed'] = sorted(set(c44) - set(c43)), sorted(set(c43) - set(c44))
        rec['failed44'] = sorted(k for k, v in c44.items() if isinstance(v, dict) and v.get('ok') is False)
        rec['okChanged'] = sorted(k for k in set(c44) & set(c43) if isinstance(c44[k], dict) and c44[k].get('ok') != c43[k].get('ok'))
        rec['observedChanged'] = sorted(k for k in set(c44) & set(c43) if c44[k] != c43[k])
        if not c44:
            rec['topKeysDiffering'] = sorted(k for k in set(d44) | set(d43) if d44.get(k) != d43.get(k)) if isinstance(d44, dict) else None
    out[new] = rec
out['allPresent'] = all(v['exists44'] and v['exists43'] for v in out.values() if isinstance(v, dict) and 'exists44' in v)
out['noFailures44'] = all(not v.get('failed44') for v in out.values() if isinstance(v, dict) and 'failed44' in v)
(RT / 'receipts/ported44-vs43.json').write_text(json.dumps(out, indent=1))
print(json.dumps({k: ({kk: vv for kk, vv in v.items() if kk not in ('receipt44', 'receipt43')} if isinstance(v, dict) else v) for k, v in out.items()}, indent=1)[:9000])
