"""Independent owned-source-pin verification on the formal source44 manifest index: every entry of every source-pins ledger
(foundation, evaluator3, native v2, security, workflows) must name a manifest member with the pinned SHA-256; changed, added and
removed pins versus source43 are recorded, and every 43->44 delta file that any ledger pins must be repinned.
Writes only receipts/source-pins44.json."""
import json
from pathlib import Path

RT = Path('/private/tmp/opensip-design-corrections/claude-independent-design.v44')
IDX = json.loads((RT / 'receipts/manifest44-index.json').read_text())
SV = json.loads((RT / 'receipts/subject-verification.json').read_text())
BASE = RT / 'work/base43'
DC = 'docs/coop/design-corrections/'
LEDGERS = [DC + 'foundation/source-pins.v1.json', DC + 'foundation/evaluator3-source-pins.v1.json', DC + 'native/source-pins.v2.json',
           DC + 'security/source-pins.v1.json', DC + 'workflows/source-pins.v1.json']
delta = {r['path'] for k in ('changed', 'added') for r in SV['delta']['43to44'][k]}


def pin_list(doc):
    keys = [k for k, v in doc.items() if isinstance(v, list) and v and all(isinstance(x, dict) and set(x) >= {'path', 'sha256'} for x in v)]
    if len(keys) != 1:
        raise SystemExit('ambiguous or missing pin list: %s' % keys)
    return keys[0], doc[keys[0]]


out = {'ledgers': {}}
for led in LEDGERS:
    doc = json.loads((RT / 'work/source44-pkg' / led).read_text())
    key, files = pin_list(doc)
    bad = [f['path'] for f in files if IDX.get(f['path']) != f['sha256']]
    old = {f['path']: f['sha256'] for f in pin_list(json.loads((BASE / led).read_text()))[1]}
    new = {f['path']: f['sha256'] for f in files}
    out['ledgers'][led] = {'ledgerSha256': IDX.get(led), 'entries': len(files), 'mismatchedAgainstManifest': bad, 'duplicatePaths': len(files) - len(new),
                           'changedPinsVs43': sorted(p for p in new if p in old and old[p] != new[p]), 'addedVs43': sorted(set(new) - set(old)),
                           'removedVs43': sorted(set(old) - set(new)), 'selfPinned': led in new,
                           'deltaFilesPinnedButNotCurrent': sorted(p for p in delta if p in new and new[p] != IDX.get(p))}
out['allPinsMatch'] = all(not v['mismatchedAgainstManifest'] for v in out['ledgers'].values())
out['changedPinUnion'] = sorted({p for v in out['ledgers'].values() for p in v['changedPinsVs43']})
out['addedPinUnion'] = sorted({p for v in out['ledgers'].values() for p in v['addedVs43']})
out['deltaFilesPinnedByNoLedger'] = sorted(p for p in delta if not any(p in {f['path'] for f in pin_list(json.loads((RT / 'work/source44-pkg' / led).read_text()))[1]} for led in LEDGERS))
print(json.dumps(out, indent=1))
(RT / 'receipts/source-pins44.json').write_text(json.dumps(out, indent=1))
