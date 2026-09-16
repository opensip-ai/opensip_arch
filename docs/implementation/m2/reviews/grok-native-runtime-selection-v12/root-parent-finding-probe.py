from pathlib import Path
import json,importlib.util,hashlib
A=Path('/Users/sb/code/opensip-ai/opensip_arch');L=A.parent/'opensip';p=L/'tools/verify_design.py';s=importlib.util.spec_from_file_location('actual_verifier',p);v=importlib.util.module_from_spec(s);s.loader.exec_module(v);seen={};original=v.contract_successor
# Observe the exact accepted map actually passed by the unmodified verifier.
def capture(architecture,binding,accepted):
 seen['map']=accepted
 return original(architecture,binding,accepted)
v.contract_successor=capture
result=v.verify(A,json.loads((L/'design-lock.json').read_bytes()),L);assert result['passed'];record=json.loads((A/'docs/implementation/m2/native-runtime-selection-v12/successor.json').read_bytes());rows=[]
for row in record['parents']:
 selected=seen['map'].get(row['path']);ok=selected is not None and all(selected[k]==row[k]for k in ['bytes','sha256']);rows.append({'parent':row,'selected':selected,'passesActualParentPredicate':ok});assert ok,row
out={'liveVerifierPassed':True,'actualAcceptedMapCapturedNotLockInputsOnly':True,'allThreeParentsPassActualPredicate':True,'rows':rows,'scope':'No candidate review/assent fabricated or activation attempted. Instrumentation only observes accepted map while preserving every original live verification call.'};Path('/tmp/opensip-implementation/runtime12-parent-finding-probe.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
