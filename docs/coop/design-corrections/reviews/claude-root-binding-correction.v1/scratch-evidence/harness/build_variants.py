import sys,json,hashlib,os
S='/private/tmp/opensip-design-corrections/claude-root-binding-correction.v1/scratch'
OUT=S+'/output/evidence/fcontrols'
os.makedirs(OUT,exist_ok=True)
sys.path.insert(0,S+'/helpers_pkg')
import importlib
def build(tag, entry, provenance):
    for m in list(sys.modules):
        if m=='helpers' or m.startswith('helpers.'): del sys.modules[m]
    from helpers import ts_pilot
    orig=ts_pilot._binding
    def patched(provider_id, ctx_hex, uhex, program_entry, extents, candidate_paths=None):
        b=orig(provider_id, ctx_hex, uhex, program_entry, extents, candidate_paths)
        b['programEntry']=entry
        b['provenance']=provenance
        return b
    ts_pilot._binding=patched
    g=ts_pilot.build_ts_run()
    exp=g['store'].export()
    raw=json.dumps(exp,indent=2,sort_keys=True)+chr(10)
    fn=OUT+'/'+tag+'.store.json'
    open(fn,'w').write(raw)
    claim=[{'name':tag,'path':tag+'.store.json','runId':g['runId']}]
    open(OUT+'/'+tag+'.claims.json','w').write(json.dumps(claim,indent=2)+chr(10))
    print(tag,'runId',g['runId'])
    print('   export sha',hashlib.sha256(raw.encode()).hexdigest(),'objects',len(exp['objectTable']))
    return g['runId']
r1=build('ts-lawful-default', None, 'default-unit')
r2=build('ts-negative-default-unit-nonnull-entry', 'tsconfig.json', 'default-unit')
r3=build('ts-lawful-explicit-plan-selection', 'tsconfig.json', 'explicit-plan-selection')
json.dump({'lawfulDefault':r1,'negativeDefaultUnitNonNullEntry':r2,'lawfulExplicitPlanSelection':r3,
           'distinctRunIds':len({r1,r2,r3})==3},open(OUT+'/variant-runids.json','w'),indent=1)
print('distinct runIds:',len({r1,r2,r3})==3)
