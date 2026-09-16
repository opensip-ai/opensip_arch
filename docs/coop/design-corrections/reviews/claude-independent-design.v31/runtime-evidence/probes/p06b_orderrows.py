"""PROBE 06b (v31) — capture the FULL frozen check-replay.v3.py report and extract the
rule-result ordering rows, so the admit/refuse triple is evidenced rather than inferred from a tail."""
import json, os, subprocess

SRC = '/tmp/opensip-design-corrections/candidate-subject.v31'
OUT = '/tmp/opensip-design-corrections/claude-independent-design.v31/receipts'
PY = '/tmp/opensip-architecture-review-env/bin/python'
p = os.path.join(SRC, 'docs/coop/design-corrections/foundation/check-replay.v3.py')
r = subprocess.run([PY, '-I', '-B', p], capture_output=True, text=True,
                   cwd=os.path.dirname(p), timeout=3600)
print('rc=%d  stdout bytes=%d' % (r.returncode, len(r.stdout)))
rep = json.loads(r.stdout)
R = {'returncode': r.returncode, 'reportTopKeys': sorted(rep) if isinstance(rep, dict) else '<list>'}
# The report keys are standing/passed/count/checks; my first pass looked for 'rows' and found 0.
rows = rep['checks']
R['reportPassed'] = rep.get('passed')
R['reportCount'] = rep.get('count')
R['totalRows'] = len(rows)
sel = [x for x in rows if 'rule-result' in json.dumps(x)]
R['ruleResultRows'] = sel
print('\ntotal rows: %d | rule-result rows: %d\n' % (len(rows), len(sel)))
for x in sel:
    print(json.dumps(x, indent=1)[:900])
    print()
R['positiveAdmits'] = any(x.get('case') == 'rule-result-id-order-differs-from-canonical'
                          and x.get('ownerAdmission') == 'ADMIT' for x in sel)
R['canonicalOrderRefuses'] = any(x.get('case') == 'rule-result-refuses-canonical-order'
                                 and x.get('ownerAdmission') == 'REFUSE' for x in sel)
R['duplicateRuleIdRefuses'] = any(x.get('case') == 'rule-result-refuses-duplicate-rule-id'
                                  and x.get('ownerAdmission') == 'REFUSE' for x in sel)
print('correct-order wholeRun ADMITS      :', R['positiveAdmits'])
print('canonical-member order REFUSES     :', R['canonicalOrderRefuses'])
print('duplicate ruleId REFUSES           :', R['duplicateRuleIdRefuses'])
json.dump(R, open(os.path.join(OUT, 'p06b-orderrows.json'), 'w'), indent=1)
print('\nwrote p06b-orderrows.json')
