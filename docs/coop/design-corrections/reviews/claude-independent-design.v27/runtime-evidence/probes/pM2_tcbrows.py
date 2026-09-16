"""PROBE M2 (v27) — read the three rows my keyword pass disagreed with, in full, plus two
declared rows for calibration. A keyword match is not a dependency determination; the question is
whether the row's DISPOSITION rests on the TCB-scope move or merely mentions same-process."""
import json, os

PKG = '/tmp/opensip-design-corrections/claude-author-package-successor.v4'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v27/receipts'
era = json.load(open(os.path.join(PKG, 'evaluation-residual-author-assessment.json')))
items = {i['id']: i for i in era['items']}
print('row keys:', sorted(items['RES-EP13-02']))
for rid in ('RES-EP13-13', 'IR-EP13-NB-02', 'IR-EP13-NB-06', 'RES-EP13-02', 'AX6'):
    it = items[rid]
    print('\n' + '=' * 98)
    print('%s   (declared TCB dependent: %s)'
          % (rid, rid in era['sharedReviewDependencies'][0]['dependentResidualIds']))
    print('=' * 98)
    for k, v in it.items():
        if k == 'id':
            continue
        s = v if isinstance(v, str) else json.dumps(v, ensure_ascii=False)
        print('\n  [%s]\n  %s' % (k, s))
json.dump({'inspected': ['RES-EP13-13', 'IR-EP13-NB-02', 'IR-EP13-NB-06', 'RES-EP13-02', 'AX6'],
           'rows': {k: items[k] for k in ('RES-EP13-13', 'IR-EP13-NB-02', 'IR-EP13-NB-06')}},
          open(os.path.join(OUT, 'pM2-tcbrows.json'), 'w'), indent=1)
