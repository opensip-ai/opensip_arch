from pathlib import Path
import json,importlib.util,copy,hashlib
R=Path.cwd();D=R/'docs/coop/design-corrections/security';s=importlib.util.spec_from_file_location('S',D/'security_lifecycle_model_v1.py');M=importlib.util.module_from_spec(s);s.loader.exec_module(M)
cases=json.loads((D/'root-schema-cases.v1.json').read_text());root=cases['roots']['root2'];out=[]
for field,value in [('indexOrigin',False),('keys-publicKey',1),('role-namespaces',[False])]:
 b=copy.deepcopy(root)
 if field=='keys-publicKey':b['keys'][0]['publicKey']=value
 elif field=='role-namespaces':b['roles']['TR-PROFILE']['namespaces']=value
 else:b[field]=value
 out.append({'id':field,'result':M.admit_root_document(b,(1,2))})
b={'profileSetSchema':1,'arbitrary':'not a profile set'};env={'envelopeSchema':2,'kind':'platform-profile-set','body':b,'bodyDigest':M.metadata_sha('opensip.metadata.platform-profile-set.1',b)}
out.append({'id':'non-schema-profile-set','result':M.admit_profile_set_envelope(env,root,root['roles']['TR-PROFILE']['keys'])})
out.append({'id':'unknown-backup-disagrees-with-foundation','result':M.storage_write_admission('UNKNOWN',False,None,False,False)})
print(json.dumps(out,indent=2))
