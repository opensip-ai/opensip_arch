"""Independent x-opensip-order coverage sweep across EVERY schema document in
the subject, including the foundation import-source-context and product-quality
report schemas the v6 finding did not enumerate. Counts arrays by walking the
raw schema bytes, not by trusting check-array-orders.py."""
import json, sys
from pathlib import Path

SUB = Path('/tmp/opensip-design-corrections/candidate-subject.v7/docs/coop/design-corrections')
VOCAB = {'sequence', 'canonical-set', 'canonical-order', 'utf8', 'path', 'numeric',
         'ordinal', 'predicate', 'ruleId', 'waiverId'}

docs = sorted(set(list(SUB.rglob('*.schema.json')) + list(SUB.rglob('*schemas*.json'))
                  + list(SUB.rglob('*.schema.v*.json')) + list(SUB.rglob('*schema.v*.json'))))
docs = [d for d in docs if 'reviews/' not in str(d.relative_to(SUB))]

def arrays(node, path, out):
    if isinstance(node, dict):
        if node.get('type') == 'array' or 'items' in node or 'prefixItems' in node:
            out.append((path, node))
        for k, v in node.items():
            arrays(v, path + '/' + k, out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            arrays(v, path + '/' + str(i), out)

report = {}
grand = {'arrays': 0, 'annotated': 0}
badvocab = []
for d in docs:
    try:
        j = json.loads(d.read_text())
    except Exception:
        continue
    out = []
    arrays(j, '', out)
    ann = [(p, n['x-opensip-order']) for p, n in out if 'x-opensip-order' in n]
    un = [p for p, n in out if 'x-opensip-order' not in n]
    for p, a in ann:
        ok = (isinstance(a, str) and a in VOCAB) or (isinstance(a, dict) and set(a) == {'by'} and isinstance(a['by'], list))
        if not ok:
            badvocab.append((str(d.relative_to(SUB)), p, a))
    kinds = {}
    for _, a in ann:
        kinds[a if isinstance(a, str) else 'by:' + ','.join(a['by'])] = \
            kinds.get(a if isinstance(a, str) else 'by:' + ','.join(a['by']), 0) + 1
    report[str(d.relative_to(SUB))] = {'arrays': len(out), 'annotated': len(ann),
                                       'unannotated': len(un), 'unannotatedPaths': un[:8],
                                       'kinds': kinds}
    grand['arrays'] += len(out); grand['annotated'] += len(ann)

print(json.dumps({'grandTotal': grand,
                  'documentsScanned': len(report),
                  'vocabularyViolations': badvocab,
                  'perDocument': report}, indent=1))
json.dump({'grandTotal': grand, 'perDocument': report, 'vocabularyViolations': badvocab},
          open(sys.argv[1], 'w'), indent=1)
