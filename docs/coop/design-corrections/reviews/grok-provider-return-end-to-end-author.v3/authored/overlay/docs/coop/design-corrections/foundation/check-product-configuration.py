import argparse,copy,importlib.util,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('cfg2',H/'product-configuration-model.py');M=importlib.util.module_from_spec(s);s.loader.exec_module(M);C=M.C
rows=[]
def check(k,v):rows.append({'id':k,'passed':bool(v)})
def reject(k,f):
    try:f()
    except (ValueError,C.ValidationError):check(k,True)
    else:check(k,False)
registry={'profiles':['default'],'capabilities':['typescript.imports','rust.imports'],'packs':['architecture']}
default={'schemaVersion':2,'analysis':{'profileId':'default','capabilities':['typescript.imports','rust.imports'],'budget':{'unit':'work-units','limit':1000}},'components':{'request':[],'pins':[],'holds':[],'allowedScopes':['project','global']},'discovery':{'entryPoints':['src/main.rs'],'workspaceRoots':['src'],'ignorePaths':['target']},'policy':{'packIds':['architecture'],'waiverIds':[]},'evidence':{'importIds':[]},'retention':{'maxBytes':None,'maxRuns':None,'maxAgeSeconds':None},'ui':{'color':'auto'}}
# request's inherited schema requires nonempty if specified; defaults omit an empty request.
default['components'].pop('request')
base={'defaults':C.canonical(default)}
a=M.resolve(base,registry);check('zero-project-config-mixed-native-default',set(a['semantic']['analysis']['capabilities'])==set(registry['capabilities']))
b={**base,'project':C.canonical({'schemaVersion':2,'discovery':{'entryPoints':['app/main.rs']}})}
result=M.resolve(b,registry);check('explicit-entry-points-override-discovery',result['semantic']['discovery']['entryPoints']==['app/main.rs'] and result['provenance']['discovery.entryPoints']=='project')
root_result=M.resolve({**base,'project':C.canonical({'schemaVersion':2,'discovery':{'workspaceRoots':['.']}})},registry)
check('workspace-project-root-sentinel',root_result['semantic']['discovery']['workspaceRoots']==['.'])
reject('entry-point-root-sentinel-is-not-a-source',lambda:M.resolve({**base,'project':C.canonical({'schemaVersion':2,'discovery':{'entryPoints':['.']}})},registry))
reject('explicit-empty-workspace-roots-refused',lambda:M.resolve({**base,'project':C.canonical({'schemaVersion':2,'discovery':{'workspaceRoots':[]}})},registry))
for k,raw in [('fractional',b'{"schemaVersion":2.0}'),('exponent',b'{"schemaVersion":2e0}'),('boolean',b'{"schemaVersion":true}'),('unknown-key',b'{"schemaVersion":2,"shell":"run"}'),('unknown-capability',b'{"schemaVersion":2,"analysis":{"capabilities":["other.magic"]}}'),('path-escape',b'{"schemaVersion":2,"discovery":{"entryPoints":["../a.ts"]}}')]:reject(k,lambda raw=raw:M.resolve({**base,'project':raw},registry))
check('ci-does-not-consume-invalid-local',M.resolve({**base,'local':b'invalid'},registry,True)['resolvedConfigDigest']==a['resolvedConfigDigest'])
reject('interactive-consumes-invalid-local',lambda:M.resolve({**base,'local':b'invalid'},registry,False))
for k,record in [('ui',{'color':'never'}),('retention',{'maxBytes':1})]:check(k+'-excluded-from-semantic-config',M.resolve({**base,'flags':C.canonical({'schemaVersion':2,k:record})},registry)['resolvedConfigDigest']==a['resolvedConfigDigest'])
check('semantic-budget-changes-config',M.resolve({**base,'flags':b'{"schemaVersion":2,"analysis":{"budget":{"unit":"work-units","limit":999}}}'},registry)['resolvedConfigDigest']!=a['resolvedConfigDigest'])
check('set-order-not-semantic',M.resolve({**base,'project':b'{"schemaVersion":2,"analysis":{"capabilities":["rust.imports","typescript.imports"]}}'},registry)['resolvedConfigDigest']==a['resolvedConfigDigest'])
reject('waiver-unregistered',lambda:M.resolve({**base,'project':b'{"schemaVersion":2,"policy":{"waiverIds":["unknown"]}}'},registry))
# Blind consumer M4: optional input sections have one exact resolved spelling.
minimal={'schemaVersion':2,'analysis':default['analysis']}
minimal_result=M.resolve({'defaults':C.canonical(minimal)},registry)
check('resolved-empty-sections-always-present',set(minimal_result['semantic'])=={'analysis','components','discovery','policy','evidence'} and all(minimal_result['semantic'][k]=={} for k in ['components','discovery','policy','evidence']))
explicit=dict(minimal,components={},discovery={},policy={},evidence={})
check('explicit-empty-input-sections-same-digest',M.resolve({'defaults':C.canonical(explicit)},registry)['resolvedConfigDigest']==minimal_result['resolvedConfigDigest'])
for missing in ['profileId','capabilities','budget']:
    broken=copy.deepcopy(minimal);broken['analysis'].pop(missing)
    reject('resolved-required-'+missing,lambda broken=broken:M.resolve({'defaults':C.canonical(broken)},registry))
sem_schema=json.loads((H/'identity-schemas.v2.json').read_text());sem_schema['$ref']='#/$defs/semantic-configuration'
for missing in ['analysis','components','discovery','policy','evidence']:
    broken=copy.deepcopy(minimal_result['semantic']);broken.pop(missing)
    reject('semantic-schema-required-'+missing,lambda broken=broken:C.validate(sem_schema,broken))
out={'standing':'design-reference-only','productQualification':False,'checks':rows,'passed':sum(v['passed'] for v in rows),'failed':sum(not v['passed'] for v in rows)}
p=argparse.ArgumentParser();p.add_argument('--report');x=p.parse_args()
if x.report:Path(x.report).write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:out[k] for k in ['passed','failed']}));sys.exit(bool(out['failed']))
