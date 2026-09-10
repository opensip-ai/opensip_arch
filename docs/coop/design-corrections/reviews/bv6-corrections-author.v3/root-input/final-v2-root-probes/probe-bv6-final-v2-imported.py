"""Root-selected final-v2 helper boundary controls, not full Run or host qualification."""
from pathlib import Path
import hashlib,importlib.util,json,sys
w=Path(sys.argv[1]);p=w/'docs/coop/design-corrections/workflows/workflows_model.v1.py'
s=importlib.util.spec_from_file_location('root_final_v2_imported',p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
rows=[]
for relation,cause in [('runtime-observation','history-range-insufficient'),('history-change','subject-not-observable'),('runtime-observation','subject-not-observable'),('history-change','history-range-insufficient')]:
 req={'relation':relation,'minResolution':'observed','completeness':'complete','satisfied':False,'deficiency':cause}
 row={'kind':'consumer-cause','requirement':req,'allowedByPublishedPerKindLaw':cause in m.IMPORTED_REQUIREMENT_LAW['perKindApplicability'][relation]}
 try:row.update(result='ADMIT',value=m.admit_evidence_requirement(req))
 except Exception as e:row.update(result='REFUSE',error=type(e).__name__+':'+str(e))
 rows.append(row)
req={'relation':'runtime-observation','minResolution':'observed','completeness':'complete'}
for flag in [True,False,None,0]:
 row={'kind':'optional-absence','requiredArgument':flag,'limit':'Nonboolean arguments test the stated unknown-default claim; no assertion they pass an owning prior typed declaration boundary.'}
 try:row['value']=m.imported_requirement_outcome(req,['synthetic-fingerprint'],{'available':False},required=flag)
 except Exception as e:row['error']=type(e).__name__+':'+str(e)
 rows.append(row)
for kind in ['runtime','history']:
 req={'relation':'runtime-observation' if kind=='runtime' else 'history-change','minResolution':'observed','completeness':'partial-acceptable'}
 evidence={'available':True,'consumable':True}
 if kind=='runtime':evidence.update(observability={'seen':'observed-hit','other':'unobservable'},windowSatisfiesRequirement=True,observationWindow={'startUtc':'2026-09-01T00:00:00Z','endUtc':'2026-09-02T00:00:00Z'},observedPopulation='synthetic')
 else:evidence.update(covered={'seen':True,'other':False},present={'seen':True},rangeSatisfiesRequirement=True,revisionRange={'from':None,'to':'a'*40,'commitCount':1,'truncated':False})
 rows.append({'kind':'partial-has-one-supported-'+kind,'requirement':req,'input':evidence,'value':m.imported_requirement_outcome(req,['seen','other'],evidence),'limit':'Synthetic already-projected helper inputs, not proof of source/target binding; tests whether the stated at-least-one rule also has other vetoes.'})
print(json.dumps({'sourceRoot':str(w),'sourceSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'standing':__doc__,'cases':rows},indent=2))
