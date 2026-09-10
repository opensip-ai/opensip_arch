from pathlib import Path
import importlib.util,json,hashlib,sys
root=Path(sys.argv[1]).resolve();dc=root/'docs/coop/design-corrections'
def load(name,path):
 sp=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m);return m
W=load('bv6_import_workflow',dc/'workflows/workflows_model.v1.py');N=load('bv6_import_native',dc/'native/native_evidence_model.v2.py');rows=[]
for relation,kind in [('runtime-observation','runtime'),('history-change','history')]:
 atom={'op':'exists','relation':relation,'minResolution':'observed','filters':[],'evidence':kind};W.admit_atom(atom)
 facts=[{'relation':relation,'subject':'synthetic-subject','resolution':'observed'}]
 observed=W.eval_pred(atom,'synthetic-subject',facts,True,{kind},{kind})
 req={'relation':relation,'minResolution':'observed','completeness':'complete'}
 native=N.sufficiency_v2(req,{relation:{'resolution':'observed','coverage':'complete'}})
 requirement={**req,'satisfied':True};W.validate_import_record('workflows/schemas/repair.schema.json','#/$defs/EvidenceRequirement',requirement)
 rows.append({'relation':relation,'admitAtom':'ADMIT','owningImportedPredicateValue':observed,'nativeSufficiencyOnSameNamedRelation':native,'satisfiedRequirementSchema':'ADMIT','repairBoundaryHelper':W.admit_evidence_requirement(requirement)})
print(json.dumps({'standing':'Draft root owner-boundary demonstration with synthetic helper inputs, not full imported Run/repair execution. These functions have DIFFERENT domains/purposes and are not required to give equal outputs. The contrast establishes why claiming native sufficiency_v2 is the only producer for both supported repair relation planes needs correction and a separate owning imported-outcome mapping.','sources':[{'path':str(p.relative_to(root)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in [dc/'workflows/workflows_model.v1.py',dc/'native/native_evidence_model.v2.py',dc/'workflows/schemas/repair.schema.json']],'cases':rows},indent=2))
