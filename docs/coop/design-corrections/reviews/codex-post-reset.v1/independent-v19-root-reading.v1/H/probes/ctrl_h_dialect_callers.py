"""Concrete counterexample for the producer-context docstring advisory. Disposable copy only."""
import json,re
from pathlib import Path
ROOT=Path('/tmp/opensip-design-corrections/post-reset-review.v19/copies/repro-v19')
DC=ROOT/'docs/coop/design-corrections'
R=[]
def ck(i,d,g,w): R.append({'id':i,'desc':d,'pass':g==w,'observed':g,'expected':w})
CALL=re.compile(r'N\.admit_coverage_result_v3\(([^)]*)\)')
sites=[]
for rel in ('integration-fixtures.py','foundation/check-identity.py','check-integration.py'):
    t=(DC/rel).read_text()
    for m in CALL.finditer(t):
        sites.append({'file':rel,'line':t[:m.start()].count('\n')+1,
                      'args':len([a for a in m.group(1).split(',') if a.strip()])})
ck('H1:fixture-path-omits-dialect',
   'the FIXTURE assembly producer calls omit the dialect (4 args); the owning units producer-boundary '
   'control at check-identity.py:2677 DOES supply it (5 args)',
   [sorted({s['args'] for s in sites}),
    [s['args'] for s in sites if s['file']=='foundation/check-identity.py' and s['line']==2677],
    sorted({s['args'] for s in sites if s['file']=='integration-fixtures.py'})],
   [[3,4,5],[5],[4]])
ck('H2:only-closure-supplies',
   'the ONLY call site supplying the dialect is retained Run closure in identity-model',
   (DC/'foundation/identity-model.py').read_text().count('_scope_dialect)'),1)
ck('H3:docstring-phrase',
   'the docstring phrase \'the reference producer\' is best read as that control, not the fixture path',
   'the reference producer and Run closure both do' in (DC/'native/native_evidence_model.v2.py').read_text(),True)
ck('H4:published-law-is-accurate',
   'the PUBLISHED normative law names only Run closure, so no published law is wrong',
   'as Run closure does' in json.dumps(json.loads((DC/'foundation/identity-schemas.v2.json').read_text())
       ['x-opensip-digest-domains']['scopeCapabilityLaw']),True)
ck('H5:authority-unaffected',
   'the closure guard is unconditional, so final authority does not depend on the parameter',
   'coverage_source_variant_prerequisite(scope,coverage_payload)' in
   (DC/'foundation/identity-model.py').read_text(),True)
f=[r for r in R if not r['pass']]
Path('/tmp/opensip-design-corrections/post-reset-review.v19/results/ctrl-h.json').write_text(
  json.dumps({'controls':len(R),'failed':len(f),'callSites':sites,'failures':f,'results':R},indent=1))
print('CTRL-H controls=%d failed=%d'%(len(R),len(f)));print(json.dumps(sites,indent=1))
for x in f: print('  FAIL',x['id'],x['desc'],x['observed'],x['expected'])
