from pathlib import Path
import importlib.util,json,hashlib,sys
root=Path(sys.argv[1]).resolve();source=root/'docs/coop/design-corrections/workflows/workflows_model.v1.py';sp=importlib.util.spec_from_file_location('bv6_req',source);W=importlib.util.module_from_spec(sp);sp.loader.exec_module(W)
rows=[]
for label,delta in [('valid-satisfied',{'satisfied':True}),('satisfied-explicit-null',{'satisfied':True,'deficiency':None}),('nonboolean-one',{'satisfied':1}),('valid-unsatisfied',{'satisfied':False,'deficiency':'resolution-incomplete'}),('missing-cause',{'satisfied':False})]:
 req={'relation':'references','minResolution':'resolved-binding','completeness':'complete',**delta};row={'case':label,'requirement':req}
 for name,fn in [('owningSchema',lambda:W.validate_import_record('workflows/schemas/repair.schema.json','#/$defs/EvidenceRequirement',req)),('boundaryHelper',lambda:W.admit_evidence_requirement(req))]:
  try:result=fn();row[name]={'result':'ADMIT','return':result}
  except Exception as e:row[name]={'result':'REFUSE','type':type(e).__name__,'detail':str(e)}
 rows.append(row)
print(json.dumps({'standing':'Provisional root draft-boundary comparison; no final finding or acceptance. Whole repair/retained Run not exercised. Invalid schema inputs may be excluded by an earlier boundary: final contract/helper preconditions must state that explicitly.','sourceRoot':str(root),'sourceSha256':hashlib.sha256(source.read_bytes()).hexdigest(),'cases':rows},indent=2))
