"""Pre-edit grounding: which EXISTING public records can actually carry these two things?
Schema admission only; no host runtime, no Run closure, no D9 execution."""
import importlib.util,json,pathlib,sys
DC=pathlib.Path(sys.argv[1])
s=importlib.util.spec_from_file_location('f',DC/'integration-fixtures.py');f=importlib.util.module_from_spec(s);s.loader.exec_module(f)
W=f.W
out={}
def adm(label,doc,sel,value):
    try:W.validate_import_record(doc,sel,value);out[label]='ADMIT'
    except Exception as e:out[label]='REFUSE:'+type(e).__name__+':'+str(e)[:110]
CM='workflows/schemas/common.schema.json';IR='workflows/schemas/invocation-record.schema.json'
detail={'code':'native.capability-unavailable','subject':'clones-near @ ts-tsconfig',
        'remedy':'install or enable the provider'}
adm('A DomainDetail with an EXISTING native.capability-unavailable code',CM,'#/$defs/DomainDetail',detail)
adm('B DoctorResult carrying a list of those details',IR,'#/$defs/DoctorResult',
    {'kind':'doctor','reportProduced':True,'defectsFound':2,'defects':[detail,dict(detail,subject='clones-cross-tsjs @ ts-tsconfig')]})
adm('C StepTermination success carrying an advisory domainDetail',CM,'#/$defs/StepTermination',
    {'class':'success','domainDetail':detail})
adm('D StepTermination request-rejected + CONFIG.INVALID',CM,'#/$defs/StepTermination',
    {'class':'request-rejected','errorCode':'CONFIG.INVALID'})
adm('E StepTermination request-rejected + REQUEST.PRECONDITION_FAILED',CM,'#/$defs/StepTermination',
    {'class':'request-rejected','errorCode':'REQUEST.PRECONDITION_FAILED'})
adm('F StepTermination operational-failed + PROVIDER.PROTOCOL_VIOLATION + provider-protocol',CM,'#/$defs/StepTermination',
    {'class':'operational-failed','errorCode':'PROVIDER.PROTOCOL_VIOLATION','faultCause':'provider-protocol'})
# the host-invariant question: is the orphan code emittable at all today?
adm('G host fault: operational-failed + SYSTEM.OUTCOME.ILLEGAL_STATE + faultCause host-invariant',CM,'#/$defs/StepTermination',
    {'class':'operational-failed','errorCode':'SYSTEM.OUTCOME.ILLEGAL_STATE','faultCause':'host-invariant'})
adm('H host fault with NO faultCause (operational-failed requires one)',CM,'#/$defs/StepTermination',
    {'class':'operational-failed','errorCode':'SYSTEM.OUTCOME.ILLEGAL_STATE'})
adm('I host fault borrowing the unrelated host-io cause',CM,'#/$defs/StepTermination',
    {'class':'operational-failed','errorCode':'SYSTEM.OUTCOME.ILLEGAL_STATE','faultCause':'host-io'})
# the prose placeholders my v2 published
adm('J the v2 prose placeholder as a DomainDetail code',CM,'#/$defs/DomainDetail',
    {'code':'request detail (capability, mode)','remedy':'x'})
c=json.loads((DC/'workflows/schemas/common.schema.json').read_text())['$defs']
out['orphanErrorCodes']=sorted(set(c['D9ErrorCode']['enum'])-
  set(json.loads((DC.parent/'artifacts/d9-exit-contract.v1.14.json').read_text())['codeMaps']['faultCauseToErrorCode'].values())-
  set(json.loads((DC.parent/'artifacts/d9-exit-contract.v1.14.json').read_text())['codeMaps']['rejectionCauseToErrorCode'].values()))
print(json.dumps(out,indent=1))
