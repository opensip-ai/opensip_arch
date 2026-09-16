"""S01 — R33-REC2-03: what cause does a REQUIRED selected-U matrix-unsupported cell actually emit,
and where does `required-cell-unsatisfied` actually apply? Read the frozen33 owners directly.
"""
import json, os, re

V1 = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v1'
SRC = '/tmp/opensip-design-corrections/candidate-subject.v33'
OUT = '/tmp/opensip-design-corrections/claude-independent33-reconciliation.v2/receipts'
CHK = os.path.join(SRC, 'docs/coop/design-corrections/foundation/check-execution-inputs.v1.py')
CON = os.path.join(SRC, 'docs/coop/design-corrections/foundation/execution-inputs-contract.v1.md')
MOD = os.path.join(SRC, 'docs/coop/design-corrections/foundation/execution_inputs_model.v1.py')
R = {}

V = json.load(open(os.path.join(V1, 'review.json')))
# 1. what my own v1 JSON actually recorded for this fixture
blob = json.dumps(V, indent=1, default=str).splitlines()
hits = []
for i, l in enumerate(blob):
    if 'required-unsupported-matrix-pair-bridge' in l or 'language-tier-unsupported' in l:
        hits.append('\n'.join(blob[max(0, i - 6):i + 7]))
R['myV1RecordContext'] = hits
print('=== what my v1 JSON records for this fixture ===')
for h in hits:
    print(h[:1400]); print('  ...')

# 2. the control in the frozen checker
L = open(CHK, encoding='utf-8').read().splitlines()
idx = [i + 1 for i, l in enumerate(L) if 'required-unsupported-matrix-pair-bridge' in l]
R['controlLines'] = idx
print('\n=== check-execution-inputs.v1.py: the retained control ===')
for n in idx:
    lo, hi = max(1, n - 30), min(len(L), n + 14)
    for k in range(lo, hi + 1):
        print('%5d  %s' % (k, L[k - 1][:150]))
    R['controlRegion'] = [L[k - 1] for k in range(lo, hi + 1)]

# 3. where required-cell-unsatisfied is produced, and under what guard
print('\n=== where `required-cell-unsatisfied` is produced in the model ===')
ML = open(MOD, encoding='utf-8').read().splitlines()
mi = [i + 1 for i, l in enumerate(ML) if 'required-cell-unsatisfied' in l or 'required_cell_unsatisfied' in l]
R['modelLines'] = mi
for n in mi:
    lo, hi = max(1, n - 12), min(len(ML), n + 8)
    print('--- model %d ---' % n)
    for k in range(lo, hi + 1):
        print('%5d  %s' % (k, ML[k - 1][:150]))
R['modelRegions'] = {str(n): [ML[k - 1] for k in range(max(1, n - 12), min(len(ML), n + 8) + 1)] for n in mi}

# 4. the contract's own wording
C = open(CON, encoding='utf-8').read()
R['contractMentionsRequiredCellUnsatisfied'] = C.count('required-cell-unsatisfied')
paras = [p for p in re.split(r'\n\n+', C) if 'required-cell-unsatisfied' in p or
         ('language-tier-unsupported' in p and 'required' in p.lower())]
R['contractParagraphs'] = paras
print('\n=== execution-inputs-contract.v1.md paragraphs ===')
for p in paras:
    print('---'); print(p[:1500])
json.dump(R, open(os.path.join(OUT, 's01-bridgecause.json'), 'w'), indent=1, default=str)
print('\nwrote s01-bridgecause.json')
