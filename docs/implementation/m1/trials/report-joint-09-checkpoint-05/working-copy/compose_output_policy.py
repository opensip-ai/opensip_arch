"""Full unaccepted D9 contract view for required-output01's explicit succession."""
from pathlib import Path
import copy,hashlib,json,types
HERE=Path(__file__).resolve().parent
path=HERE/'check_model_carriers.py';V=types.ModuleType('v');V.__file__=str(path);exec(compile(path.read_bytes(),str(path),'exec'),V.__dict__)
raw=V.read_unit('required-output','owner/d9/d9-exit-contract.v1.14.json');parent=json.loads(raw);candidate=copy.deepcopy(parent)
row=next(r for r in candidate['invariants'] if r['id']=='invariant-envelope-parity')
assert row['text']=='For finite CLI commands, CommandEnvelope.termination equals process termination when serialization succeeds.'
before=row['text']
row['text']='For finite CLI commands, CommandEnvelope.termination equals process termination when complete envelope admission, serialization and required delivery succeed. If required output fails, the existing machine-output-serialization-failed operation governs process termination (OUTPUT.SERIALIZATION_FAILED, operational-failed, exit4), even after an interrupted invocation aggregate. The earlier invocation aggregate, step results and committed Runs are preserved. Partial or complete earlier envelope bytes may already be visible; do not append a second normal envelope or claim atomic stream delivery. Required render-step failures retain their own DELIVERY.REQUIRED_FAILED law before this final operation.'
candidate['version']='v1.15'
candidate['status']='JOINT-REPORT09-PROPOSAL / NOT-APPLIED / AWAITING-ACTUAL-INDEPENDENT-REVIEW'
candidate['supersedes']='d9-exit-contract.v1.14.json'
candidate['purpose']='Preserve all v1.14 exit classes, maps, axes, union fields, reduction laws and golden outcomes; explicitly compose the final required envelope admission/serialization/delivery operation after the settled invocation aggregate. Required-output01 is an unaccepted capacity-failure policy; this view does not close L02 or implement finalization.'
# The retained parent conformance/derivation records describe unchanged parent
# laws. Explicitly qualify them rather than assert the old exact-delta checker
# accepts this changed contract.
candidate['jointOutputSuccession']={'standing':'Unaccepted root view; inherited conformance records and reference derivation are parent-law evidence only, not v1.15 checker or independent approval',
 'parentSha256':hashlib.sha256(raw).hexdigest(),'policy':'required-output01/contract.md',
 'checker':'check_output_policy.py','integrationChecks':'check_output_integration.py',
 'capacity':'Complete required envelope remains bounded by4MiB; failure can occur after useful work commits. No truncation or selection preflight is added. L02 old stronger criterion requires explicit disposition and actual review.',
 'privateSource':'Finalizer consumes the exact admitted projection and aggregate; generic envelope shape validation alone does not enforce command parity.',
 'implementation':'Bounded encoder, private handles, actual stream/file delivery, signal arbitration and the sole process-exit site remain required product work.'}
changes=[]
for key in candidate:
 if candidate[key]!=parent.get(key):changes.append(key)
assert set(changes)=={'version','status','supersedes','purpose','invariants','jointOutputSuccession'}
out=HERE/'composed-owners/d9-exit-contract.proposed.v1.15.json';out.write_text(json.dumps(candidate,indent=2)+'\n')
result={'standing':'Full unaccepted D9 successor view; exact parent remains unchanged; no L02 or product acceptance',
 'parentSha256':hashlib.sha256(raw).hexdigest(),'changedTopLevelKeys':changes,
 'invariantChange':{'id':row['id'],'before':before,'after':row['text']},
 'output':{'path':str(out.relative_to(HERE)),'bytes':out.stat().st_size,'sha256':hashlib.sha256(out.read_bytes()).hexdigest()}}
(HERE/'output-policy-composition-result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'changedTopLevelKeys':changes,'passed':True}))
