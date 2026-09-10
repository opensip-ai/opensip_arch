"""Instantiate and VALIDATE the real public outputs. No string comparison inside the proposal."""
import importlib.util,json,pathlib,sys
DC=pathlib.Path(sys.argv[1])
s=importlib.util.spec_from_file_location('f',DC/'integration-fixtures.py');f=importlib.util.module_from_spec(s);s.loader.exec_module(f)
N,W=f.N,f.W
CM='workflows/schemas/common.schema.json';IR='workflows/schemas/invocation-record.schema.json'
out={'terminations':[],'details':[],'negatives':[]}
def val(doc,sel,v):
    try:W.validate_import_record(doc,sel,v);return 'ADMIT'
    except Exception as e:return 'REFUSE:'+type(e).__name__+':'+str(e)[:90]
for key,row in N.PUBLIC_ROUTE_REGISTRY['keys'].items():
    origins=list(row['byOriginatingBoundary']) if row['originDependent'] else [None]
    for o in origins:
        t=N.public_termination_for(key,o)
        if t is None:out['terminations'].append({'key':key,'origin':o,'terminates':False});continue
        out['terminations'].append({'key':key,'origin':o,'class':t['class'],'errorCode':t['errorCode'],
            'faultCause':t.get('faultCause'),'domainDetail':(t.get('domainDetail') or {}).get('code'),
            'stepTerminationAdmission':val(CM,'#/$defs/StepTermination',t)})
# the release-absence public records, through the real carriers
units=[{'languageMode':'ts-tsconfig','rootPath':'.','languageFamily':'tsjs'}]
staged=json.loads(json.dumps(f.NATIVE_FIXTURES['registryStagedBuild']))
sel=N.default_capability_selection(units,staged)
details=N.release_absence_details(sel['undeclaredCapabilities'])
out['details']={'count':len(details),'sample':details[0] if details else None,
  'eachDomainDetailAdmission':sorted({val(CM,'#/$defs/DomainDetail',d) for d in details}),
  'doctorResultAdmission':val(IR,'#/$defs/DoctorResult',
     {'kind':'doctor','reportProduced':True,'defectsFound':len(details),'defects':details[:256]}),
  'successStepTerminationAdmission':val(CM,'#/$defs/StepTermination',
     {'class':'success','domainDetail':details[0]}) if details else None,
  'orderIsSelectionOrder':[d['subject'] for d in details]==
     [r['capabilityId']+' @ '+r['languageMode'] for r in sel['undeclaredCapabilities']]}
def neg(label,fn):
    try:fn();out['negatives'].append({'case':label,'outcome':'ADMIT'})
    except Exception as e:out['negatives'].append({'case':label,'outcome':'REFUSE','error':str(e)[:100]})
neg('a release-declaration key claimed as a user configuration origin',
    lambda:N.public_termination_for('native.release-capability-unregistered','external-configuration'))
neg('a configured-capability key claimed as a host-generated internal layer is LAWFUL',
    lambda:N.public_termination_for('native.requested-capability-unregistered','host-generated-internal-layer'))
neg('an origin-dependent key with no origin supplied',
    lambda:N.public_termination_for('native.requested-capability-unregistered'))
neg('an unregistered internal key',lambda:N.public_termination_for('native.made-up-key','external-configuration'))
print(json.dumps(out,indent=1))
