"""Compare every ported scope-preservation probe receipt on source45 with this origin's own source44 receipt of the same probe
(read-only history): per case ok and observed equality, cases added/removed. Evidence of preserved behavior only.
Writes only receipts/ported45-vs44.json."""
import json
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v45')
R44 = Path('/tmp/opensip-design-corrections/claude-independent-design.v44/receipts/probes')
PAIRS = [('policy-v40-on45.json', 'policy-v40-on44.json'), ('native-v40-on45.json', 'native-v40-on44.json'),
         ('runterm-adv-v40-on45.json', 'runterm-adv-v40-on44.json'), ('query-carriers.json', 'query-carriers.json'),
         ('carrier-readonly.json', 'carrier-readonly.json'), ('comparison-knowledge.json', 'comparison-knowledge.json'),
         ('repair2.json', 'repair2.json'), ('run-termination-s7.json', 'run-termination-s7.json'),
         ('native-custody-fallback.json', 'native-custody-fallback.json'), ('capture-joins-on45.json', 'capture-joins-on44.json')]


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
    p45, p44 = RT / 'receipts/probes' / new, R44 / old
    rec = {'receipt45': str(p45), 'receipt44': str(p44), 'exists45': p45.exists(), 'exists44': p44.exists()}
    if p45.exists() and p44.exists():
        d45, d44 = json.loads(p45.read_text()), json.loads(p44.read_text())
        c45, c44 = cases(d45), cases(d44)
        rec['wholeReceiptEqual'] = d45 == d44
        rec['cases45'], rec['cases44'] = len(c45), len(c44)
        rec['added'], rec['removed'] = sorted(set(c45) - set(c44)), sorted(set(c44) - set(c45))
        rec['failed45'] = sorted(k for k, v in c45.items() if isinstance(v, dict) and v.get('ok') is False)
        rec['okChanged'] = sorted(k for k in set(c45) & set(c44) if isinstance(c45[k], dict) and c45[k].get('ok') != c44[k].get('ok'))
        rec['observedChanged'] = sorted(k for k in set(c45) & set(c44) if c45[k] != c44[k])
    out[new] = rec
out['allPresent'] = all(v['exists45'] and v['exists44'] for v in out.values() if isinstance(v, dict) and 'exists45' in v)
out['noFailures45'] = all(not v.get('failed45') for v in out.values() if isinstance(v, dict) and 'failed45' in v)
(RT / 'receipts/ported45-vs44.json').write_text(json.dumps(out, indent=1))
print(json.dumps({k: ({kk: vv for kk, vv in v.items() if kk not in ('receipt45', 'receipt44')} if isinstance(v, dict) else v) for k, v in out.items()}, indent=1)[:9000])
