"""Independent (Claude v12) probe, corrected: source-level identity tap in a DISPOSABLE copy."""
import os,sys,json,hashlib,subprocess,shutil
BASE='/tmp/opensip-design-corrections/post-reset-review.v12/copies/identity2'
os.makedirs(BASE,exist_ok=True)
TAP='''
def identifier(domain,value):
    if domain not in PREFIX:raise C.AdmissionError('IDENTITY_DOMAIN')
    schema=copy.deepcopy(SCHEMA);schema['$ref']='#/$defs/'+domain
    C.validate(schema,value);ordered(value)
    _r=PREFIX[domain]+':'+C.identity(domain,value)
    import os as _os
    with open(_os.environ['CLAUDE_ID_TAP'],'a') as _f:_f.write(domain+'|'+_r+'\\n')
    return _r
'''
ORIG='''def identifier(domain,value):
    if domain not in PREFIX:raise C.AdmissionError('IDENTITY_DOMAIN')
    schema=copy.deepcopy(SCHEMA);schema['$ref']='#/$defs/'+domain
    C.validate(schema,value);ordered(value)
    return PREFIX[domain]+':'+C.identity(domain,value)
'''
res={}
for tag,root in [('v11','/tmp/opensip-design-corrections/candidate-subject.v11'),
                 ('v12','/tmp/opensip-design-corrections/candidate-subject.v12')]:
    work=os.path.join(BASE,tag)
    if os.path.exists(work):shutil.rmtree(work)
    shutil.copytree(root,work)
    f=os.path.join(work,'docs/coop/design-corrections/foundation/identity-model.py')
    s=open(f).read()
    assert ORIG in s,'anchor not found in '+tag
    open(f,'w').write(s.replace(ORIG,TAP.strip()+'\n',1))
    tap=os.path.join(BASE,'tap-%s.txt'%tag)
    open(tap,'w').close()
    env=dict(os.environ,CLAUDE_ID_TAP=tap)
    p=subprocess.run(['/tmp/opensip-architecture-review-env/bin/python','-I','-B',
        os.path.join(work,'docs/coop/design-corrections/foundation/check-identity.py')],
        capture_output=True,text=True,timeout=1200,env=env,
        cwd=os.path.join(work,'docs/coop/design-corrections/foundation'))
    lines=[l for l in open(tap).read().split('\n') if l]
    res[tag]={'suiteStdout':p.stdout.strip()[-120:],'suiteExit':p.returncode,
              'identityCalls':len(lines),'distinctIdentities':len(set(lines)),
              'multisetDigest':hashlib.sha256('\n'.join(sorted(lines)).encode()).hexdigest(),
              'domains':len(set(l.split('|')[0] for l in lines))}
print(json.dumps(res,indent=1))
a=set(open(os.path.join(BASE,'tap-v11.txt')).read().split('\n'))-{''}
b=set(open(os.path.join(BASE,'tap-v12.txt')).read().split('\n'))-{''}
print('v11 distinct',len(a),'v12 distinct',len(b))
print('v11 identities MISSING from v12 (instability):',len(a-b))
for x in sorted(a-b)[:10]:print('   -',x[:110])
print('v12-only identities (new cases):',len(b-a))
for x in sorted(b-a)[:5]:print('   +',x[:110])
print('SHARED-SET STABLE:',len(a-b)==0)
json.dump({'summary':res,'missingFromV12':sorted(a-b)[:50],'newInV12':sorted(b-a)[:50]},
          open('/tmp/opensip-design-corrections/post-reset-review.v12/probes/body-identity-result.json','w'),indent=1)
