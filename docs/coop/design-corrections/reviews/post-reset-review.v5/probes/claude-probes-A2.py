# Independent v5 probes, group A (revised registry): MUST-A(v4) SARIF parity.
import json,sys,os,importlib.util,copy,glob
from pathlib import Path
SUB='/tmp/opensip-design-corrections/post-reset-review.v5/scratch/subject'
W=SUB+'/docs/coop/design-corrections/workflows'
sys.path.insert(0,W)
spec=importlib.util.spec_from_file_location('wfm',W+'/workflows_model.v1.py')
M=importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
from jsonschema import Draft202012Validator as DV
from jsonschema.validators import Draft202012Validator
from referencing import Registry,Resource
from referencing.jsonschema import DRAFT202012
SCHEMAS={}
for p in sorted(glob.glob(W+'/schemas/*.schema.json')):
    s=json.loads(Path(p).read_text()); SCHEMAS[s['$id']]=s
FOUND=json.loads(Path(SUB+'/docs/coop/design-corrections/foundation/identity-schemas.v2.json').read_text())
REG=Registry().with_resources([(k,Resource(contents=v,specification=DRAFT202012)) for k,v in SCHEMAS.items()]
                              +[(FOUND['$id'],Resource(contents=FOUND,specification=DRAFT202012))])
U='urn:opensip:product-v1:workflows:'
def valid_command(obj):
    return DV({'$ref':U+'command-inventory#/$defs/Command'},registry=REG).is_valid(obj)
INV=json.load(open(W+'/command-inventory.v1.json'))
CASES=json.load(open(W+'/workflow-cases.v1.json'))
SCH=SCHEMAS[U+'command-inventory']
R=[]
def p(pid,title,ok,detail=''):
    R.append({'id':pid,'title':title,'result':'PASS' if ok else 'FAIL','detail':str(detail)[:900]})
    print(('PASS ' if ok else 'FAIL ')+pid+' :: '+title+((' :: '+str(detail)[:260]) if detail else ''))

COMMON=['run-id','verdict','required-coverage','deficiency','findings','termination-class','retention-disclosure']
CMD={c['name']:c for c in INV['commands']}
sarif_cmds=sorted(c['name'] for c in INV['commands'] if 'sarif' in c['formats'])

p('A1','SARIF advertised by exactly default/analyze/audit/repair-verify',
  sarif_cmds==['analyze','audit','default','repair-verify'],sarif_cmds)
missing={n:[f for f in COMMON if f not in CMD[n]['parityFields']] for n in sarif_cmds}
p('A2','all four declare the seven common analysis parity fields',all(not v for v in missing.values()),missing)

base_ok=all(valid_command(CMD[n]) for n in sarif_cmds)
rej={}
for n in sarif_cmds:
    for f in COMMON:
        r=copy.deepcopy(CMD[n]); r['parityFields'].remove(f); rej[n+'/'+f]=valid_command(r)
p('A3','unmodified rows valid AND every single omission rejected (4x7=28 negatives)',
  base_ok and not any(rej.values()),{'baseValid':base_ok,'stillValid':[k for k,v in rej.items() if v],'negatives':len(rej)})

scoped=True;ex=[]
for c in [c for c in INV['commands'] if 'sarif' not in c['formats']]:
    if 'run-id' in c['parityFields']:
        r=copy.deepcopy(c); r['parityFields'].remove('run-id')
        if not valid_command(r): scoped=False; ex.append(c['name'])
p('A3b','rule scoped to SARIF commands only (non-SARIF rows unaffected)',scoped,ex[:5])

def env_for(name,extra=None,drop=None):
    c=CMD[name]; par={k:('x-'+k) for k in c['parityFields']}
    par['findings']=[{'fingerprint':'fp-'+name}]; par['verdict']='pass'; par['deficiency']=None
    if extra: par.update(extra)
    for d in (drop or []): par.pop(d,None)
    return {'parity':par,'envelope':{'schemaFamily':'opensip.product.envelope','schemaMajor':2},'hints':['h']}

leak={}
for n in sarif_cmds:
    e=env_for(n,extra={'SECRET-undeclared':'leak','findings-shadow':[{'fingerprint':'ghost'}]})
    r=M.render(e,'sarif',CMD[n]); blob=json.dumps(r)
    leak[n]={'inParity':'SECRET-undeclared' in r['parity'],'anywhere':('leak' in blob or 'ghost' in blob),
             'resultsIsDeclared':r['results']==e['parity']['findings']}
p('A4','undeclared envelope data never reaches SARIF results/runProperties/parity',
  all(not v['inParity'] and not v['anywhere'] and v['resultsIsDeclared'] for v in leak.values()),leak)

fab={}
for n in sarif_cmds:
    for f in ('findings','verdict','deficiency'):
        e=env_for(n,drop=[f])
        try:
            r=M.render(e,'sarif',CMD[n]); fab[n+'/'+f]={'fabricated':True}
        except KeyError as k: fab[n+'/'+f]={'fabricated':False,'raised':'KeyError '+str(k)}
        except M.Refusal as rf: fab[n+'/'+f]={'fabricated':False,'raised':'Refusal '+rf.detail}
p('A5','missing declared field never yields fabricated null/empty SARIF output (12 cases)',
  all(not v['fabricated'] for v in fab.values()),{'fabricated':[k for k,v in fab.items() if v['fabricated']],'cases':len(fab)})

hypo=copy.deepcopy(CMD['analyze']); hypo['name']='hypo'
for f in ('findings','verdict','deficiency'): hypo['parityFields'].remove(f)
e={'parity':{k:('x-'+k) for k in hypo['parityFields']},'envelope':{},'hints':[]}
e['parity']['findings']=[{'fingerprint':'undeclared-ghost'}]
try:
    r=M.render(e,'sarif',hypo); out={'rendered':True,'results':r['results'],'runProperties':r['runProperties']}; ok=False
except KeyError as k: out={'raised':'KeyError '+str(k)}; ok=True
except M.Refusal as rf: out={'raised':'Refusal '+rf.detail}; ok=True
sr=not valid_command(hypo)
p('A5b','exact v4 counterexample refused by schema AND not silently rendered',ok and sr,{'render':out,'schemaRefuses':sr})

a=CMD['audit']
p('A6','audit declares analysis findings+deficiency plus comparison fields',
  all(f in a['parityFields'] for f in COMMON) and {'comparison-counts','baseline-id','comparison-id'}<=set(a['parityFields']),a['parityFields'])
ra=M.render(env_for('audit'),'sarif',a)
p('A6b','audit SARIF emits real findings and declared verdict (v4 showed x-verdict/null/1-result)',
  ra['results']==[{'fingerprint':'fp-audit'}] and ra['runProperties']['verdict']=='pass' and 'deficiency' in ra['runProperties'],ra['runProperties'])

rv=CMD['repair-verify']
p('A7','repair-verify declares common fields plus verification counts',
  all(f in rv['parityFields'] for f in COMMON) and {'applied-snapshot-id','verified-snapshot-id','snapshot-matched','targets-remaining','net-new-findings'}<=set(rv['parityFields']),rv['parityFields'])
rr=M.render(env_for('repair-verify'),'sarif',rv)
p('A7b','repair-verify SARIF carries a real fresh-Run verdict, not v4 null',
  rr['runProperties']['verdict']=='pass' and rr['results']==[{'fingerprint':'fp-repair-verify'}],rr['runProperties'])

par_eq={}
for n in sarif_cmds:
    e=env_for(n); c=CMD[n]; rs=[M.render(e,f,c) for f in c['formats']]
    par_eq[n]={'holds':M.parity_holds(rs),
               'sarifEqJson':[r for r in rs if r['format']=='sarif'][0]['parity']==[r for r in rs if r['format']=='json'][0]['parity']}
p('A8','one declared projection shared by every advertised renderer of all four',
  all(v['holds'] and v['sarifEqJson'] for v in par_eq.values()),par_eq)

exercised={c['command'] for c in CASES['renderCases'] if 'sarif' in c.get('formats',[]) and 'refusal' not in c['expect']}
p('A9','render cases exercise every advertised SARIF command',exercised==set(sarif_cmds),sorted(exercised))

e=env_for('analyze'); e['parity']['findings']=[]
r=M.render(e,'sarif',CMD['analyze'])
try: M.render(env_for('analyze',drop=['findings']),'sarif',CMD['analyze']); dist=False
except KeyError: dist=True
p('A10','empty findings renders [] and is distinguishable from an absent field',r['results']==[] and dist,{'empty':r['results']})

e=env_for('analyze'); e['parity']['run-id']=None
r=M.render(e,'sarif',CMD['analyze'])
p('A11','ephemeral run-id projects null without minting Run authority',
  r['parity']['run-id'] is None and 'run-id' in CMD['analyze']['parityFields'],r['parity']['run-id'])

prose=open(SUB+'/docs/v2/contracts/product-v1/workflows-and-surfaces.md').read()
sc=[x['then']['properties']['parityFields']['allOf'] for x in SCH['$defs']['Command']['allOf'] if 'formats' in x.get('if',{}).get('properties',{})][0]
schema_fields=[c['contains']['const'] for c in sc]
chk=open(W+'/check_workflows.v1.py').read()
in_prose=[f for f in COMMON if '`'+f+'`' in prose]
p('A12','seven common fields identical across prose, schema, inventory, checker',
  sorted(schema_fields)==sorted(COMMON) and sorted(in_prose)==sorted(COMMON) and all(("'"+f+"'") in chk for f in COMMON),
  {'schema':sorted(schema_fields),'prose':sorted(in_prose)})

adv=[c['name'] for c in INV['commands'] if c.get('advisory') and 'sarif' in c['formats']]
p('A13','no advisory command advertises SARIF',adv==[],adv)
nonsarif=[c for c in INV['commands'] if 'sarif' not in c['formats']][0]
try:
    M.render(env_for(nonsarif['name']) if nonsarif['name'] in CMD else env_for('analyze'),'sarif',nonsarif)
    p('A13b','non-applicable SARIF refused OUTPUT.FORMAT_NOT_APPLICABLE',False,'no refusal')
except M.Refusal as rf:
    p('A13b','non-applicable SARIF refused OUTPUT.FORMAT_NOT_APPLICABLE ('+nonsarif['name']+')',rf.detail=='OUTPUT.FORMAT_NOT_APPLICABLE',rf.detail)

# A14: the checker's own negative construction is genuinely discriminating (does the reference
# case distinguish filtered vs unfiltered sourcing?) - test-strength observation, not a product law
e=env_for('analyze',extra={})
unfiltered=e['parity'].get('findings',[])
filtered={k:e['parity'][k] for k in CMD['analyze']['parityFields']}['findings']
p('A14','reference render case cannot itself distinguish filtered vs unfiltered sourcing (probe A4 does)',
  unfiltered==filtered,'checker feeds parity == declared set exactly; A4 supplies the discriminating extra keys')

json.dump(R,open('/tmp/opensip-design-corrections/post-reset-review.v5/probes/claude-probes-A2.json','w'),indent=1)
print('\nA-group:',sum(1 for x in R if x['result']=='PASS'),'PASS',sum(1 for x in R if x['result']=='FAIL'),'FAIL of',len(R))
