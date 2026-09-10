"""Root counterexample; producer-boundary reference admission, not a full Run or product test."""
from pathlib import Path
import copy, hashlib, importlib.util, json, sys, unicodedata
root=Path(sys.argv[1]).resolve()
native=root/'docs/coop/design-corrections/native'
spec=importlib.util.spec_from_file_location('native_bv5_root',native/'native_evidence_model.v2.py')
n=importlib.util.module_from_spec(spec);spec.loader.exec_module(n)
f=json.loads((native/'native-cases.v2.json').read_text())['fixtures']
scope=copy.deepcopy(f['scopeDescriptor']);scope.update(relation='unresolved-edge',resolution='observed')
commitment=n.subject_scope_commitment(scope)
payload=copy.deepcopy(f['coveragePayload'])
for record in (payload['key'],payload['entry']):record.update(relation='unresolved-edge',resolution='observed')
payload['key']['subjectScopeCommitment']=commitment['subjectScopeCommitment']
payload['entry']['examinedUniverse']['subjectScopeCommitment']=commitment['subjectScopeCommitment']
payload['entry']['resolutionCompleteness']={'state':'not-applicable','attempted':False,'examinedExhaustive':True,'stageTerminal':None,'unresolvedEdgeCount':0,'unresolvedEdgeClasses':[]}
rows=[]
for name,delta in [('control',{}),('attempted-true',{'attempted':True}),('nonempty-classes',{'unresolvedEdgeClasses':['dynamic-dispatch']}),('attempted-and-classes',{'attempted':True,'unresolvedEdgeClasses':['dynamic-dispatch']})]:
 p=copy.deepcopy(payload);p['entry']['resolutionCompleteness'].update(delta)
 try:result=n.admit_coverage_result_v3(p,scope,[])
 except Exception as e:result={'raised':type(e).__name__,'message':str(e)[:300]}
 rows.append({'name':name,'resolutionCompleteness':p['entry']['resolutionCompleteness'],'result':result})
out={'subjectRoot':str(root),'nativeModelSha256':hashlib.sha256((native/'native_evidence_model.v2.py').read_bytes()).hexdigest(),'scope':'Reference producer-boundary admission with fixture commitments; no full retained Run closure, product host, compiler or execution qualification.','rows':rows,'lowercaseEvidence':{'unicodeVersion':unicodedata.unidata_version,'values':[{'input':s,'lower':s.lower(),'casefold':s.casefold()} for s in ['ES2022','\u0130','\u039f\u03a3','\u00df']]}}
print(json.dumps(out,indent=2,ensure_ascii=True))
