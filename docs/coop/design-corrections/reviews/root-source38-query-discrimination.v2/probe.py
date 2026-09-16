from pathlib import Path
import json,sys,importlib.util,hashlib
B=Path('/tmp/opensip-design-corrections');rows=[]
for label,S in [('baseline37',B/'candidate-subject.v37'),('successor-working',B/'termination-exclusivity-successor.v1/source')]:
 p=S/'docs/coop/design-corrections/workflows/query_projection_model.v3.py';spec=importlib.util.spec_from_file_location('query_advisory_'+label,p);Q=importlib.util.module_from_spec(spec);spec.loader.exec_module(Q)
 ctx={'advisory':False,'availability':'retained','coverage':'complete','projectId':'prj1-'+'a'*64,'resolvedView':{'runId':'run3:'+'a'*64},'totalItems':0,'truncated':False}
 for op in ('run.show','finding.list','availability.show','comparison.diff','candidate.list','inspection.show','review.brief'):
  for value in (False,True):
   response={'schemaFamily':'opensip.product.query','schemaMajor':3,'operation':op,'context':dict(ctx,advisory=value)}
   try:Q.canonical.ExactValidator({'$ref':Q.SCHEMA_ID+'#/$defs/GraphQueryResponseV1'},registry=Q.schema_registry()).validate(response);admit=True
   except Q.ValidationError as e:admit=False
   rows.append({'source':label,'operation':op,'advisory':value,'actualAdmit':admit,'shouldAdmit':value==(op in ('comparison.diff','candidate.list','inspection.show','review.brief'))})
checks={'allCurrent':all(r['actualAdmit']==r['shouldAdmit'] for r in rows if r['source']=='successor-working'),'threeCounterexamplesDiscriminate':all(r['actualAdmit'] for r in rows if r['source']=='baseline37' and r['advisory'] and r['operation'] in ('run.show','finding.list','availability.show'))}
O=B/'root-source38-query-discrimination.v2';O.mkdir();record={'standing':'Response schema admission only; no arbitrary response promoted to a retained query result','checks':checks,'rows':rows,'passed':all(checks.values())};(O/'report.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps({'checks':checks,'rows':len(rows)}));sys.exit(0 if record['passed'] else 1)
