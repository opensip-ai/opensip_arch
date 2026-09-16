"""Read-only probe of exact source37 output-profile schema admission; no full host claim."""
from pathlib import Path
import json,importlib.util,hashlib
S=Path('/tmp/opensip-design-corrections/candidate-subject.v37');O=Path(__file__).parent
p=S/'docs/coop/design-corrections/workflows/workflow_projection_model.v3.py';spec=importlib.util.spec_from_file_location('workflow37',p);W=importlib.util.module_from_spec(spec);spec.loader.exec_module(W)
ref='urn:opensip:product-v1:workflows:evaluator3:common:3#/$defs/StepTermination'
variants={
 'fault-only':{'class':'operational-failed','errorCode':'HOST.IO_FAILURE','faultCause':'host-io'},
 'fault-plus-deficiency':{'class':'operational-failed','errorCode':'HOST.IO_FAILURE','faultCause':'host-io','reasonCodes':['COVERAGE.PROVIDER_UNAVAILABLE']},
 'success-plus-faultCause':{'class':'success','faultCause':'host-io'},
 'policy-plus-reasonCodes':{'class':'policy-failed','authority':'ephemeral','reasonCodes':['COVERAGE.PROVIDER_UNAVAILABLE']},
 'indeterminate-plus-faultCause':{'class':'indeterminate','reasonCodes':['COVERAGE.PROVIDER_UNAVAILABLE'],'faultCause':'host-io'},
 'fault-plus-unknown-extra':{'class':'operational-failed','errorCode':'HOST.IO_FAILURE','faultCause':'host-io','unknown':True},
}
rows=[]
for name,value in variants.items():
 row={'name':name,'input':value}
 try:W.validate_profile(ref,value);row['observed']='ADMIT'
 except Exception as e:row.update(observed='REFUSE',reason=str(e),exception=type(e).__name__)
 rows.append(row)
record={'standing':'Current StepTermination shape admission observations only. Not a complete host finalizer, public renderer or retained-Run admission probe. No source defect or review outcome inferred before owning semantic boundary assessment.','source':'candidate-subject.v37','modelSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'schemaSha256':hashlib.sha256((S/'docs/coop/design-corrections/workflows/schemas/evaluator3/common.schema.json').read_bytes()).hexdigest(),'selector':ref,'cases':rows};(O/'probe.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(rows,indent=2))
