"""Item 2: the typed pre-Plan refusal, its exact observed fields, and the ACTUAL public envelope.
Reference model plus real schema admission; no host, renderer or Run execution."""
import importlib.util,json,pathlib,sys
DC=pathlib.Path(sys.argv[1])
s=importlib.util.spec_from_file_location('f',DC/'integration-fixtures.py');f=importlib.util.module_from_spec(s);s.loader.exec_module(f)
N,W=f.N,f.W
CM='workflows/schemas/common.schema.json';ENV='workflows/schemas/command-envelope.schema.json'
def adm(doc,sel,v):
    try:W.validate_import_record(doc,sel,v);return 'ADMIT'
    except Exception as e:
        c=e.__cause__;return 'REFUSE:'+(str(c).split('\n')[0] if c else str(e))[:80]
def units(n):return [{'rootPath':'apps/u%03d'%i,'languageMode':'ts-tsconfig','languageFamily':'tsjs'} for i in range(n)]
out={'bound':N.requested_capability_bound(),'perTsUnit':len(N.required_default_capabilities('ts-tsconfig'))}
rows=[]
for n in (1,93,94,1024):
    try:
        r=N.default_capability_selection(units(n),[])
        rows.append({'units':n,'outcome':'ADMIT','requests':len(r['analysisSpec']['requestedCapabilities']),
                     'notices':len(r['undeclaredCapabilities'])})
    except N.ScopeRefusal as e:
        t=N.scope_refusal_termination(e)
        env={'schemaFamily':'opensip.product.envelope','schemaMajor':2,'kind':'failure',
             'requestId':'req1_'+'a'*32,'termination':t,'exitCode':W.EXIT[t['class']],
             'errors':[t['domainDetail']]}
        rows.append({'units':n,'outcome':'REFUSE','typed':True,'message':str(e),
                     'field':e.subject['field'],'count':e.subject['count'],'limit':e.subject['limit'],
                     'class':t['class'],'errorCode':t['errorCode'],'detail':t['domainDetail']['code'],
                     'subject':t['domainDetail']['subject'],
                     'terminationAdmission':adm(CM,'#/$defs/StepTermination',t),
                     'envelopeAdmission':adm(ENV,'',env),
                     'planMinted':False,'runMinted':False})
    except Exception as e:
        rows.append({'units':n,'outcome':'REFUSE','typed':False,'exception':type(e).__name__,
                     'rawScalars':len(str(e))})
out['defaultSelection']=rows
# The EXPLICIT path (not the default helper) must get the same typed refusal.
explicit=[{'capabilityId':'inventory','languageMode':'ts-tsconfig','workspaceRoot':'apps/u%04d'%i,'required':True}
          for i in range(1025)]
try:
    N.admit_requested_capabilities(explicit);out['explicitOverflow']={'outcome':'ADMIT'}
except N.ScopeRefusal as e:
    t=N.scope_refusal_termination(e)
    out['explicitOverflow']={'outcome':'REFUSE','typed':True,'subject':t['domainDetail']['subject'],
      'errorCode':t['errorCode'],'envelopeAdmission':adm(ENV,'',
        {'schemaFamily':'opensip.product.envelope','schemaMajor':2,'kind':'failure','requestId':'req1_'+'b'*32,
         'termination':t,'exitCode':W.EXIT[t['class']],'errors':[t['domainDetail']]})}
except Exception as e:
    out['explicitOverflow']={'outcome':'REFUSE','typed':False,'exception':type(e).__name__}
# A fitting explicit selection at exactly the bound still admits.
try:
    N.admit_requested_capabilities(explicit[:1024]);out['explicitAtExactBound']='ADMIT'
except Exception as e:out['explicitAtExactBound']='REFUSE:'+type(e).__name__
# The existing scope-array refusal is unchanged and shares the code.
try:
    N.unit_scope_descriptor([{'rootPath':'r%05d'%i,'languageMode':'ts-tsconfig','languageFamily':'tsjs'}
                             for i in range(1025)],[])
    out['scopeArrayRefusalUnchanged']='ADMIT (unexpected)'
except N.ScopeRefusal as e:
    out['scopeArrayRefusalUnchanged']={'subject':N.scope_refusal_termination(e)['domainDetail']['subject'],
      'detail':e.detail,'sharesTheCode':e.detail=='PROJECT.SCOPE_LIMIT'}
out['detailCodeIsAnExistingPublicMember']='PROJECT.SCOPE_LIMIT' in {
  r['code'] for r in json.loads((DC/'public-detail-registry.v1.json').read_text())['records']}
print(json.dumps(out,indent=1))
