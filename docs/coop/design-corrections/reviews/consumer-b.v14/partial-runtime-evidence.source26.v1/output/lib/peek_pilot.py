import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import run_syntax_code as RSC, run_syntax_code_full as F
g = F.complete(RSC.build())
out = g['out']
for pp in out['proof']['predicateProofs']:
    w = out['witnesses'][pp['witnessDigest']]
    print('%-32s %-14s %-20s %-14s kind=%-12s facts=%d cov=%d defs=%s'
          % (pp['ruleId'], pp['predicateId'], pp['subjectId'][:22], pp['value'],
             w['kind'], len(w['matchingFactIds']), len(w['coverageIds']),
             [d['cause'] for d in w['deficiencies']]))
print()
for fid, fr in out['findings'].items():
    print(fid)
    print('  ', json.dumps(fr, indent=1)[:900])
    print('   params', json.dumps(out['findingAux'][fid]['parameters']))
