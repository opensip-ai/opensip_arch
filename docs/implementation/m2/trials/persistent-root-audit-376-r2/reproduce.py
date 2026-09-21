"""Conditional model test; never reboots, remounts, or mutates a real registry."""
from pathlib import Path
import hashlib, importlib.util, json, sys
A=Path(sys.argv[1])
p=A/'docs/implementation/m2/project-registry-owner-selection-v1/reference/registry_model.py'
raw=p.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='b9c1a19a27d899aaf0a35b7a23709e6e6541f38903bdd9741c5603b38bdd6e19'
spec=importlib.util.spec_from_file_location('registry_model',p);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
root=dict(platform='linux',canonicalPathBytesHex=b'/repo'.hex(),deviceId='2049',inodeId='42',birthSeconds=1700000000,birthNanoseconds=123)
pid='prj1-'+'1'*64
row=dict(projectId=pid,namespaceId='00000001-0000-4000-8000-000000000000',root=root,status='ACTIVE',allocationKind='random')
doc=dict(schemaVersion=1,entries=[row]);changed=dict(root,deviceId='2050')
assert m.classify(doc,root,m.marker(pid))=='MATCHED_ACTIVE'
assert m.classify(doc,changed,m.marker(pid))=='CONTRADICTION'
assert m.locator_key(root)==m.locator_key(changed)
print(json.dumps(dict(scope='pure conditional model; not executed OS reboot/remount',document=doc,changedObservation=changed,baseline='MATCHED_ACTIVE',afterDeviceNumberChange='CONTRADICTION',sameLocator=True),indent=2))
