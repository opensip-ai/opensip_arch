import importlib.util,json,sys,os,re,glob,hashlib
R='/tmp/opensip-design-corrections/candidate-subject.v21/docs/coop/design-corrections'
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);sys.modules[n]=m;s.loader.exec_module(m);return m
W=load('wfm',os.path.join(R,'workflows/workflows_model.v1.py'))
out={}

# (1) Refusal with detail=None: does termination() emit an explicitly-null domainDetail
#     (schema-invalid per workflows section 0) or omit the optional field?
r=W.Refusal('CONFIG.INVALID',None,'a refusal that carries no domain detail')
t=r.termination()
out['refusal_detail_none']={'terminationKeys':sorted(t.keys()),
  'domainDetailPresent':'domainDetail' in t,
  'domainDetailValue':t.get('domainDetail'),
  'explicitlyNull':('domainDetail' in t and t['domainDetail'] is None)}
import jsonschema
common=json.load(open(os.path.join(R,'workflows/schemas/common.schema.json')))
store={common.get('$id','common.schema.json'):common}
def admits(inst):
    try:
        res=jsonschema.RefResolver(base_uri=common.get('$id',''),referrer=common,store=store)
        jsonschema.validate(inst,{'$ref':(common.get('$id','')+'#/$defs/StepTermination')},resolver=res)
        return True,None
    except Exception as e: return False,str(e)[:200]
ok,err=admits(t)
out['refusal_detail_none']['stepTerminationAdmits']=ok
out['refusal_detail_none']['error']=err

# does adopt_baseline's duplicate-entry guard really raise detail=None?
src=open(os.path.join(R,'workflows/workflows_model.v1.py')).read()
i=src.find('def adopt_baseline')
seg=src[i:i+4000]
out['adopt_baseline_detail_none_guards']=[l.strip() for l in seg.splitlines() if 'Refusal(' in l and "None" in l][:6]

# (2) Who reads the per-script reference reports independently of the launcher report?
consumers={}
for p in glob.glob(os.path.join(R,'**/*.py'),recursive=True):
    if '/reviews/' in p: continue
    t2=open(p,errors='replace').read()
    hits=[n for n in ['identity-report.json','foundation-report.json','product-quality-report.json',
                      'product-configuration-report.json','array-order-report.json'] if n in t2]
    if hits: consumers[os.path.relpath(p,R)]=hits
out['perScriptReportConsumers']=consumers
# does the launcher unlink/quarantine the target report before spawning?
lau=open(os.path.join(R,'foundation/run-reference-checks.py')).read()
out['launcherClearsStaleReport']={'unlink':'unlink' in lau,'remove':'os.remove' in lau,
  'missing_ok':'missing_ok' in lau,
  'note':'A timed-out child leaves the PREVIOUS run report on disk under the same name.'}
print(json.dumps(out,indent=1))
json.dump(out,open('/tmp/opensip-design-corrections/post-reset-review.v21/results/adversarial.json','w'),indent=1)
