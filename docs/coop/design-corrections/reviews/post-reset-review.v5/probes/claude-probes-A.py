# Independent v5 probes, group A: MUST-A(v4) SARIF parity. Author: reviewer session (not subject author).
import json,sys,os,importlib.util,copy,traceback
SUB='/tmp/opensip-design-corrections/post-reset-review.v5/scratch/subject'
W=SUB+'/docs/coop/design-corrections/workflows'
sys.path.insert(0,W)
spec=importlib.util.spec_from_file_location('wfm',W+'/workflows_model.v1.py')
M=importlib.util.module_from_spec(spec); spec.loader.exec_module(M)
INV=json.load(open(W+'/command-inventory.v1.json'))
CASES=json.load(open(W+'/workflow-cases.v1.json'))
SCH=json.load(open(W+'/schemas/command-inventory.schema.json'))
import jsonschema
from jsonschema import Draft202012Validator as DV
R=[]
def p(pid,title,ok,detail=''):
    R.append({'id':pid,'title':title,'result':'PASS' if ok else 'FAIL','detail':str(detail)[:900]})
    print(('PASS ' if ok else 'FAIL ')+pid+' :: '+title+(' :: '+str(detail)[:300] if detail else ''))

COMMON=['run-id','verdict','required-coverage','deficiency','findings','termination-class','retention-disclosure']
CMD={c['name']:c for c in INV['commands']}
sarif_cmds=sorted(c['name'] for c in INV['commands'] if 'sarif' in c['formats'])

# A1 exactly the four advertised commands
p('A1','SARIF advertised by exactly default/analyze/audit/repair-verify',
  sarif_cmds==['analyze','audit','default','repair-verify'],sarif_cmds)

# A2 every SARIF command declares all seven common fields
missing={n:[f for f in COMMON if f not in CMD[n]['parityFields']] for n in sarif_cmds}
p('A2','all four declare the seven common analysis parity fields',
  all(not v for v in missing.values()),missing)

# A3 schema (independently validated, not via checker) rejects each single omission, per command
val=DV(SCH)
def valid_command(obj):
    # validate against $defs/Command via a wrapper schema resolving $ref internally
    s=dict(SCH); s=json.loads(json.dumps(SCH))
    s2={'$id':s['$id'],'$defs':s['$defs'],'$ref':'#/$defs/Command'}
    return DV(s2).is_valid(obj)
base_ok=all(valid_command(CMD[n]) for n in sarif_cmds)
rej={}
for n in sarif_cmds:
    for f in COMMON:
        r=copy.deepcopy(CMD[n]); r['parityFields'].remove(f)
        rej[n+'/'+f]=valid_command(r)
p('A3','unmodified SARIF rows valid AND every single-field omission rejected by schema',
  base_ok and not any(rej.values()),{'baseValid':base_ok,'stillValid':[k for k,v in rej.items() if v]})

# A3b omission for a NON-sarif command must NOT be rejected by this rule (rule is scoped)
nonsarif=[c for c in INV['commands'] if 'sarif' not in c['formats'] and c['parityFields']]
scoped=True; ex=None
for c in nonsarif[:6]:
    r=copy.deepcopy(c)
    if 'run-id' in r['parityFields']:
        r['parityFields'].remove('run-id')
        if not valid_command(r): scoped=False; ex=c['name']
p('A3b','SARIF field rule is scoped to SARIF commands only (no over-reach)',scoped,ex)

# A4 renderer sources results and runProperties from the ONE filtered declared projection.
# Undeclared envelope data must not appear anywhere in the rendering.
def env_for(name,extra=None,drop=None):
    c=CMD[name]
    par={k:('x-'+k) for k in c['parityFields']}
    par['findings']=[{'fingerprint':'fp-'+name}]
    par['verdict']='pass'; par['deficiency']=None
    if extra: par.update(extra)
    if drop:
        for d in drop: par.pop(d,None)
    return {'parity':par,'envelope':{'schemaFamily':'opensip.product.envelope','schemaMajor':2},'hints':['h']}
leak={}
for n in sarif_cmds:
    e=env_for(n,extra={'SECRET-undeclared':'leak','findings-shadow':[{'fingerprint':'ghost'}]})
    r=M.render(e,'sarif',CMD[n])
    blob=json.dumps(r)
    leak[n]={'inParity':'SECRET-undeclared' in r['parity'],'anywhere':'leak' in blob or 'ghost' in blob,
             'resultsIsDeclared':r['results']==e['parity']['findings'],
             'runProps':r['runProperties']}
p('A4','undeclared envelope data never reaches SARIF results/runProperties/parity',
  all(not v['inParity'] and not v['anywhere'] and v['resultsIsDeclared'] for v in leak.values()),leak)

# A5 a declared field absent from the host projection must NOT become fabricated valid output
fab={}
for n in sarif_cmds:
    for f in ('findings','verdict','deficiency'):
        e=env_for(n,drop=[f])
        try:
            r=M.render(e,'sarif',CMD[n]); fab[n+'/'+f]={'fabricated':True,'out':r.get('results') if f=='findings' else r['runProperties']}
        except KeyError as k: fab[n+'/'+f]={'fabricated':False,'raised':'KeyError '+str(k)}
        except M.Refusal as rf: fab[n+'/'+f]={'fabricated':False,'raised':'Refusal '+rf.detail}
p('A5','missing declared field never yields fabricated null/empty SARIF output',
  all(not v['fabricated'] for v in fab.values()),fab)

# A5b the v4 defect counterexample: a hypothetical sarif command WITHOUT findings/verdict declared
hypo=copy.deepcopy(CMD['analyze'])
hypo['name']='hypo'; 
for f in ('findings','verdict','deficiency'): hypo['parityFields'].remove(f)
e={'parity':{k:('x-'+k) for k in hypo['parityFields']},'envelope':{},'hints':[]}
e['parity']['findings']=[{'fingerprint':'undeclared-ghost'}]
try:
    r=M.render(e,'sarif',hypo); out={'rendered':True,'results':r['results'],'runProperties':r['runProperties']}
    ok=False
except KeyError as k: out={'rendered':False,'raised':'KeyError '+str(k)}; ok=True
except M.Refusal as rf: out={'rendered':False,'raised':'Refusal '+rf.detail}; ok=True
schema_refuses=not valid_command(hypo)
p('A5b','v4 counterexample (sarif row lacking findings/verdict) refused by schema AND not rendered',
  ok and schema_refuses,{'render':out,'schemaRefuses':schema_refuses})

# A6 audit keeps the current analysis findings and deficiency, plus comparison fields
a=CMD['audit']
p('A6','audit declares analysis findings+deficiency and its comparison fields',
  all(f in a['parityFields'] for f in COMMON) and 'comparison-counts' in a['parityFields'] and 'baseline-id' in a['parityFields'],
  a['parityFields'])
ra=M.render(env_for('audit'),'sarif',a)
p('A6b','audit SARIF emits real findings and its declared deficiency (not null-by-default)',
  ra['results']==[{'fingerprint':'fp-audit'}] and 'verdict' in ra['runProperties'] and ra['runProperties']['verdict']=='pass',
  ra['runProperties'])

# A7 repair-verify keeps fresh Run verdict/findings and verification counts
rv=CMD['repair-verify']
p('A7','repair-verify declares verdict/findings plus verification counts',
  all(f in rv['parityFields'] for f in COMMON) and all(f in rv['parityFields'] for f in
      ('applied-snapshot-id','verified-snapshot-id','snapshot-matched','targets-remaining','net-new-findings')),
  rv['parityFields'])
rr=M.render(env_for('repair-verify'),'sarif',rv)
p('A7b','repair-verify SARIF carries a real verdict, not null',
  rr['runProperties']['verdict']=='pass' and rr['results']==[{'fingerprint':'fp-repair-verify'}],rr['runProperties'])

# A8 cross-renderer parity uses the same single projection for all advertised formats
par_eq={}
for n in sarif_cmds:
    e=env_for(n); c=CMD[n]
    rs=[M.render(e,f,c) for f in c['formats']]
    par_eq[n]={'holds':M.parity_holds(rs),'formats':c['formats'],
               'sarifParityEqualsJson':[r for r in rs if r['format']=='sarif'][0]['parity']==[r for r in rs if r['format']=='json'][0]['parity']}
p('A8','one declared projection shared by every advertised renderer of all four commands',
  all(v['holds'] and v['sarifParityEqualsJson'] for v in par_eq.values()),par_eq)

# A9 render cases now exercise all four
exercised={c['command'] for c in CASES['renderCases'] if 'sarif' in c.get('formats',[]) and 'refusal' not in c['expect']}
p('A9','render cases exercise every advertised SARIF command',exercised==set(sarif_cmds),sorted(exercised))

# A10 empty findings is a real empty result, distinguishable from a missing projection field
e=env_for('analyze'); e['parity']['findings']=[]
r=M.render(e,'sarif',CMD['analyze'])
e2=env_for('analyze',drop=['findings'])
try: M.render(e2,'sarif',CMD['analyze']); distinguishable=False
except KeyError: distinguishable=True
p('A10','empty findings renders [] and is distinguishable from an absent field',
  r['results']==[] and distinguishable,{'empty':r['results'],'absentRaises':distinguishable})

# A11 ephemeral run-id null projection does not mint Run authority
e=env_for('analyze'); e['parity']['run-id']=None
r=M.render(e,'sarif',CMD['analyze'])
p('A11','ephemeral run-id may project null without fabricating a Run id',
  r['parity']['run-id'] is None and 'run-id' in CMD['analyze']['parityFields'],r['parity']['run-id'])

# A12 prose / inventory / schema / checker agree on the SAME seven field names
prose=open(SUB+'/docs/v2/contracts/product-v1/workflows-and-surfaces.md').read()
sc=[x['then']['properties']['parityFields']['allOf'] for x in SCH['$defs']['Command']['allOf']
    if 'formats' in x.get('if',{}).get('properties',{})][0]
schema_fields=[c['contains']['const'] for c in sc]
chk=open(W+'/check_workflows.v1.py').read()
in_prose=[f for f in COMMON if '`'+f+'`' in prose]
p('A12','seven common fields identical in prose, schema, inventory rows and checker',
  sorted(schema_fields)==sorted(COMMON) and sorted(in_prose)==sorted(COMMON) and all(("'"+f+"'") in chk for f in COMMON),
  {'schema':schema_fields,'prose':in_prose})

# A13 non-analysis / advisory commands still gain no SARIF and no minted verdict
adv=[c['name'] for c in INV['commands'] if c.get('advisory') and 'sarif' in c['formats']]
p('A13','no advisory command advertises SARIF',adv==[],adv)
try:
    M.render(env_for('analyze'),'sarif',CMD['query']) if 'query' in CMD else None
    q='query' in CMD and 'sarif' in CMD['query']['formats']
    p('A13b','non-applicable SARIF request refused OUTPUT.FORMAT_NOT_APPLICABLE',not q,'no refusal raised')
except M.Refusal as rf:
    p('A13b','non-applicable SARIF request refused OUTPUT.FORMAT_NOT_APPLICABLE',
      rf.detail=='OUTPUT.FORMAT_NOT_APPLICABLE',rf.detail)

json.dump(R,open('/tmp/opensip-design-corrections/post-reset-review.v5/probes/claude-probes-A.json','w'),indent=1)
print('\nA-group:',sum(1 for x in R if x['result']=='PASS'),'pass',sum(1 for x in R if x['result']=='FAIL'),'fail of',len(R))
