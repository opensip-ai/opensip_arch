"""Supplied-observation conjunction, not descriptor/profile or OS qualification."""
from copy import deepcopy
from pathlib import Path
import json
import registry_model as m
root=dict(platform='macos',canonicalPathBytesHex=b'/repo'.hex(),volumeIdentity=dict(kind='macos-apfs-volume-uuid-v1',value='1'*32),inodeId='42',birthSeconds=0,birthNanoseconds=123)
row=dict(projectId='prj1-'+'1'*64,namespaceId='00000001-0000-4000-8000-000000000000',root=root,status='ACTIVE',allocationKind='random')
doc=dict(schemaVersion=2,entries=[row]);v=dict(deviceId='2049',filesystemId=[1,2])
base=dict(document=doc,root=root,marker_observation=m.marker(row['projectId']),old_carrier='absent',current_carrier='present',profile_observation='qualified-macos-apfs-uuid-v1',volatile_before=v,volatile_after=v)
cases=[]
def case(name,changes,expected):
 inputs={**deepcopy(base),**changes}
 try:observed=m.conditional_native_reuse(**inputs)
 except m.Refused as e:observed={'refused':str(e)}
 ok=isinstance(observed,dict)and 'refused'in observed if expected=='REFUSE' else observed==expected
 cases.append(dict(name=name,expected=expected,observed=observed,passed=ok));assert ok,(name,expected,observed)
case('complete-conditional-join',{},'MATCHED_ACTIVE')
for field,value in [('old_carrier','present'),('old_carrier','unavailable'),('current_carrier','absent'),('current_carrier','unavailable'),('profile_observation','unsupported'),('profile_observation','unavailable'),('root',None),('volatile_before',None),('volatile_after',None)]:
 case('missing-or-unavailable-'+field+'-'+str(value),{field:value},'UNAVAILABLE')
case('durable-agreement-does-not-bypass-live-device-change',dict(volatile_after=dict(v,deviceId='2050')),'UNAVAILABLE')
case('durable-agreement-does-not-bypass-live-fsid-change',dict(volatile_after=dict(v,filesystemId=[1,3])),'UNAVAILABLE')
newv=dict(deviceId='2050',filesystemId=[3,4]);case('changed-between-operations-only',dict(volatile_before=newv,volatile_after=newv),'MATCHED_ACTIVE')
wrong=deepcopy(root);wrong['volumeIdentity']['value']='2'*32;case('volatile-agreement-does-not-bypass-durable-change',dict(root=wrong),'CONTRADICTION')
case('volatile-and-durable-do-not-bypass-marker',dict(marker_observation=m.marker('prj1-'+'2'*64)),'CONTRADICTION')
case('tracking-still-required',dict(tracking='unknown'),'TRACKING_REFUSAL')
case('later-invalid-row-cannot-be-skipped',dict(document=dict(schemaVersion=2,entries=[row,dict(row,extra=0)])),'REFUSE')
case('no-context-from-caller-profile-label',dict(profile_observation='caller-approved'),'REFUSE')
case('reserved-not-active',dict(document=dict(schemaVersion=2,entries=[dict(row,status='RESERVED')])),'RECOVERY_REQUIRED')
out=Path(__file__).with_name('native-join-results.381.json');assert not out.exists();out.write_text(json.dumps(dict(standing='Pure model labels, no native capability or platform qualification',count=len(cases),failed=0,cases=cases),indent=2)+'\n');print(len(cases),'native join conditional cases passed')
