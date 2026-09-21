"""Conditional pure379 cases, not host profile qualification or reboot evidence."""
from copy import deepcopy
from pathlib import Path
import itertools,json
import registry_model as m
root=dict(platform='macos',canonicalPathBytesHex=b'/repo'.hex(),volumeIdentity=dict(kind='macos-apfs-volume-uuid-v1',value='1'*32),inodeId='42',birthSeconds=1700000000,birthNanoseconds=123)
row=dict(projectId='prj1-'+'1'*64,namespaceId='00000001-0000-4000-8000-000000000000',root=root,status='ACTIVE',allocationKind='random')
doc=dict(schemaVersion=2,entries=[row]);cases=[]
def case(name,call,expected):
 try:result=call()
 except m.Refused as e:result={'refused':str(e)}
 ok=isinstance(result,dict) and 'refused'in result if expected=='REFUSE' else result==expected
 cases.append(dict(name=name,expected=expected,result=result,passed=ok));assert ok,(name,expected,result)
def valid(d):m.validate(d);return 'VALID'
def changed_root(**values):r=deepcopy(root);r.update(values);return r
def lookup(r):return m.classify(doc,r,m.marker(row['projectId']))
case('unchanged-qualified-values',lambda:lookup(root),'MATCHED_ACTIVE')
old=dict(deviceId='2049',filesystemId=[1,2]);new=dict(deviceId='2050',filesystemId=[3,4]);before=m.encode(doc)
for name,v in [('before-reboot-assumption',old),('after-reboot-assumption',new)]:
 case(name+'-intra-operation-consistent',lambda v=v:m.volatile_consistent(v,deepcopy(v)),True)
 case(name+'-durable-match-with-no-write',lambda:lookup(root),'MATCHED_ACTIVE')
case('cross-sample-device-fsid-change-refuses',lambda:m.volatile_consistent(old,new),False)
case('only-device-change-within-operation-refuses',lambda:m.volatile_consistent(old,dict(old,deviceId='2050')),False)
case('only-fsid-change-within-operation-refuses',lambda:m.volatile_consistent(old,dict(old,filesystemId=[1,3])),False)
assert m.encode(doc)==before
for name,value in [('none',None),('empty',{}),('zero',dict(kind='macos-apfs-volume-uuid-v1',value='0'*32)),('uppercase',dict(kind='macos-apfs-volume-uuid-v1',value='A'*32)),('unknown-kind',dict(kind='device-id',value='1'*32)),('short',dict(kind='macos-apfs-volume-uuid-v1',value='1'*31)),('extra',dict(kind='macos-apfs-volume-uuid-v1',value='1'*32,extra=0)),('nonstring',dict(kind='macos-apfs-volume-uuid-v1',value=1))]:
 case('invalid-volume-'+name,lambda value=value:lookup(changed_root(volumeIdentity=value)),'REFUSE')
case('linux-profile-not-invented',lambda:lookup(changed_root(platform='linux')),'REFUSE')
case('legacy-root-not-reinterpreted',lambda:lookup({**{k:v for k,v in root.items() if k!='volumeIdentity'},'deviceId':'2049'}),'REFUSE')
case('legacy-envelope-not-reinterpreted',lambda:valid(dict(doc,schemaVersion=1)),'REFUSE')
for name,r in [('volume',changed_root(volumeIdentity=dict(kind='macos-apfs-volume-uuid-v1',value='2'*32))),('inode',changed_root(inodeId='43')),('birth-second',changed_root(birthSeconds=1700000001)),('birth-nanos',changed_root(birthNanoseconds=124)),('path',changed_root(canonicalPathBytesHex=b'/renamed'.hex()))]:
 case('durable-change-'+name,lambda r=r:lookup(r),'CONTRADICTION')
other=deepcopy(row);other.update(projectId='prj1-'+'2'*64,namespaceId='00000002-0000-4000-8000-000000000000');other['root']['canonicalPathBytesHex']=b'/other'.hex()
case('same-incarnation-different-locator-refuses',lambda:valid(dict(schemaVersion=2,entries=[row,other])),'REFUSE')
distinct=deepcopy(other);distinct['root']['volumeIdentity']['value']='2'*32
case('same-numeric-inode-birth-distinct-volume-allowed',lambda:valid(dict(schemaVersion=2,entries=[row,distinct])),'VALID')
collision=deepcopy(distinct);collision['root']['canonicalPathBytesHex']=root['canonicalPathBytesHex']
case('locator-uniqueness-remains-separate',lambda:valid(dict(schemaVersion=2,entries=[row,collision])),'REFUSE')
case('indistinguishable-coherent-copy-limitation',lambda:lookup(deepcopy(root)),'MATCHED_ACTIVE')
for old_state,new_state,established,authorized in itertools.product(('absent','present','unavailable'),('absent','present','unavailable'),(False,True),(False,True)):
 expected='UNAVAILABLE'
 if old_state=='absent' and new_state=='present':expected='DECODE_COMPLETE_V2'
 if old_state=='absent' and new_state=='absent' and not established and authorized:expected='AUTHORIZED_PRISTINE_CREATION_CANDIDATE'
 case('carrier-'+str((old_state,new_state,established,authorized)),lambda o=old_state,n=new_state,e=established,a=authorized:m.carrier_observation(o,n,e,a),expected)
case('old-absence-unknown-label-not-absence',lambda:m.carrier_observation('unknown','present',True,False),'REFUSE')
for v in [dict(deviceId='01',filesystemId=[1,2]),dict(deviceId=str(1<<64),filesystemId=[1,2]),dict(deviceId='1',filesystemId=[True,2]),dict(deviceId='1',filesystemId=[1<<31,2])]:
 case('invalid-live-sample-'+str(v),lambda v=v:m.volatile_consistent(v,v),'REFUSE')
out=Path(__file__).with_name('persistent-results.379.json');assert not out.exists();out.write_text(json.dumps(dict(standing='Pure conditional model, no native admission/reboot/clone-detection or owner acceptance',cases=cases,count=len(cases),failed=0),indent=2)+'\n');print(len(cases),'persistent cases passed')
