"""Root-selected projection/consumer controls. Synthetic helper inputs, not full Run admission."""
from pathlib import Path
import hashlib,importlib.util,json,sys
root=Path(sys.argv[1]);p=root/'docs/coop/design-corrections/workflows/workflows_model.v1.py'
s=importlib.util.spec_from_file_location('root_imported_v3',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
rows=[]
a='finding-key2:'+'1'*64;b='finding-key2:'+'2'*64
findings={x:{'fingerprint':x} for x in [a,b]}
descriptors={x:{'schemaVersion':2,'ruleStableId':'r','detectorSemanticsMajor':1,'subjectKey':{'language':'typescript','kind':'function','logicalPath':path,'qualifiedName':name,'discriminator':'d'},'relatedSubjectKeys':[]} for x,path,name in [(a,'src/a.ts','seen'),(b,'src/b.ts','other')]}
def project(kind,subjects,targets=(a,b)):
 return m.project_targets_to_imported_subjects(list(targets),kind,findings,descriptors,subjects)
def record(label,fn):
 r={'case':label}
 try:r.update(result='RETURN',value=fn())
 except Exception as e:r.update(result='REFUSE',exception=type(e).__name__,detail=str(e),remedy=getattr(e,'remedy',None))
 rows.append(r)
for relation,cause in [('runtime-observation','history-range-insufficient'),('history-change','subject-not-observable'),('runtime-observation','subject-not-observable'),('history-change','history-range-insufficient')]:
 record('consumer:'+relation+':'+cause,lambda r=relation,c=cause:m.admit_evidence_requirement({'relation':r,'minResolution':'observed','completeness':'complete','satisfied':False,'deficiency':c}))
subjects=[{'path':'src/a.ts','symbol':'seen','observability':'observed-hit'},{'path':'src/b.ts','symbol':'other','observability':'unobservable'}]
for kind in ['runtime','history']:
 for completeness in ['complete','partial-acceptable']:
  req={'relation':'runtime-observation' if kind=='runtime' else 'history-change','minResolution':'observed','completeness':completeness}
  evidence={'available':True,'consumable':True,'windowSatisfiesRequirement':True,'rangeSatisfiesRequirement':True,'covered':{a:True,b:False},'observationWindow':{'startUtc':'2026-09-01T00:00:00Z','endUtc':'2026-09-02T00:00:00Z'},'observedPopulation':'synthetic','revisionRange':{'from':None,'to':'a'*40,'commitCount':1,'truncated':False}}
  proj=project(kind,subjects if kind=='runtime' else [{'path':'src/a.ts'}])
  record(kind+':'+completeness,lambda:m.imported_requirement_outcome(req,proj,evidence,True))
req={'relation':'runtime-observation','minResolution':'observed','completeness':'complete'}
for flag in [True,False,None,0]:record('absence:'+repr(flag),lambda:m.imported_requirement_outcome(req,project('runtime',subjects),{'available':False},flag))
for label,sub in [('same-symbol',[subjects[0]]),('different-symbol',[dict(subjects[0],symbol='wrong')]),('file-only',[{'path':'src/a.ts','observability':'observed-hit'}]),('ambiguous-file-and-symbol',[subjects[0],{'path':'src/a.ts','observability':'observed-hit'}])]:
 record('projection:'+label,lambda:project('runtime',sub,(a,)))
 record('outcome:'+label,lambda:m.imported_requirement_outcome(req,project('runtime',sub,(a,)),{'available':True,'consumable':True,'windowSatisfiesRequirement':True},True))
print(json.dumps({'sourceRoot':str(root),'sourceSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'standing':__doc__,'cases':rows},indent=2))
