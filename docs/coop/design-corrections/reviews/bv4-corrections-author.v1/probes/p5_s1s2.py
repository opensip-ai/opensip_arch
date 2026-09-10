"""S1 and S2 before/after."""
import json,sys,pathlib,copy
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from kitload import load_kit
K=load_kit(sys.argv[1]);M=K.M;C=K.C;N=K.N
out={}
# ---- S1: what a LITERAL implementer of the registry sentence produces, per universe.
src=M.RELATIONS['clones']['bodyIdentityJoin']['languageIdSource']
out['languageIdSource']=src
enum=set(M.SCHEMA['$defs']['body-language-version']['properties']['languageId']['enum'])
rows=M.DIGESTS['domainSets']['native-semantic-universe']
def literal_engine_reading(domain):
    return rows[domain]['language']
def derived_body_reading(domain,path):
    b=rows[domain]['languageVersionBinding'];d=b['dialect']
    if d['form']!='closed-suffix-table':return b['bodyLanguage']
    m=[s for s in d['table'] if path.endswith(s)]
    return b['bodyLanguageByVariant'][d['table'][max(m,key=len)]]
out['readings']={}
for domain,path in (('native.semantic-universe.typescript.v2','a.js'),
                    ('native.semantic-universe.typescript.v2','a.ts'),
                    ('native.semantic-universe.syntax.v2','src/lib.rs'),
                    ('native.semantic-universe.syntax.v2','a.ts'),
                    ('native.semantic-universe.rust.v2','src/lib.rs')):
    eng=literal_engine_reading(domain);der=derived_body_reading(domain,path)
    out['readings'][domain.split('.')[-2]+' '+path]={
        'engineReading':eng,'engineReadingRepresentable':eng in enum,
        'derivedBodyReading':der,'agree':eng==der}
out['registrySentenceNamesTheBodySelector']=('bodyLanguageByVariant' in src)
# The actual frame value produced by a full Run, per universe.
def frame_language(**kw):
    run,objects,blobs=K.build(resolved=True,has_match=True,relation='clones',**kw)
    M.close_run(run,objects,blobs)
    fact=next(v for k,(d,v) in objects.items() if d=='fact')
    payload=C.parse(blobs[fact['payloadDigest']])
    return M.parse_body_frame(blobs[payload['bodyIdentity'].removeprefix('sha256:')])[3].decode()
for label,kw in (('ts-hosted .js body',dict(universe_language='typescript',source_path='a.js')),
                 ('compiler-free .rs body',dict(universe_language='syntax',pure_syntax=True)),
                 ('rust .rs body',dict(universe_language='rust'))):
    try:out.setdefault('runFrameLanguageId',{})[label]=frame_language(**kw)
    except Exception as exc:out.setdefault('runFrameLanguageId',{})[label]='ERROR:'+str(exc)[:100]
# ---- S2: is the capabilityId vocabulary closed at retained Run admission?
def request(capability,mode='ts-tsconfig'):
    r,o,b=K.build(resolved=True,has_match=True)
    plan=copy.deepcopy(o[r['planId']][1]);spec=C.parse(b[plan['analysisSpecDigest']])
    spec['requestedCapabilities'][0].update(capabilityId=capability,languageMode=mode)
    plan['analysisSpecDigest']=K.put_blob(b,spec);K.rekey_plan(o,b,r,plan)
    return M.close_run(r,o,b)
out['capabilityRequests']={}
for label,cap,mode in (('matrix id inventory','inventory','ts-tsconfig'),
                       ('matrix id clones-fact','clones-fact','ts-tsconfig'),
                       ('relation@rung spelling','clones@normalized-body-hash','ts-tsconfig'),
                       ('bare relation name','declares','ts-tsconfig'),
                       ('made-up id','made-up-capability','ts-tsconfig'),
                       ('case variant','Inventory','ts-tsconfig'),
                       ('preview constant','preview-typescript','ts-tsconfig'),
                       ('NOT-SELECTED cell','clones-cross-tsjs','rust-cargo'),
                       ('UNSUPPORTED-TYPED cell','references','syntax-only')):
    try:request(cap,mode);out['capabilityRequests'][label]={'admitted':True}
    except Exception as exc:out['capabilityRequests'][label]={'admitted':False,'error':str(exc)[:130]}
out['releaseRegistryAdmissionExists']=hasattr(N,'admit_release_capability_registry')
out['requestedCapabilityAdmissionExists']=hasattr(N,'admit_requested_capabilities')
print(json.dumps(out,indent=1,sort_keys=True))
