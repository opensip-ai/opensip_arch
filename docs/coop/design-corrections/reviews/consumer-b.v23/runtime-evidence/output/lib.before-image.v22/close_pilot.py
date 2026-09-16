import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import opensip_closure as CL
import run_syntax_code as RSC, run_syntax_code_full as F

g = F.complete(RSC.build())
c = CL.Closure(g['st'])
rep = c.close_run(g['out']['runId'], 'syntax-code')
print('admitted        :', rep['admitted'])
print('checks passed   :', rep['checksPassed'])
print('checks n/a      :', rep['checksNotApplicable'])
print('checks refused  :', rep['checksRefused'])
print('digests visited :', rep['retainedDigestsVisited'], 'of', rep['storeBlobCount'])
for r in rep['refusals'][:30]:
    print('  REFUSE', r['check'], '|', json.dumps(r['detail'])[:260])
