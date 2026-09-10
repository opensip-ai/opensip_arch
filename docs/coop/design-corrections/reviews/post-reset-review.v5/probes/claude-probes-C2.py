# Corrected C2 / C8 (prior failures were probe defects: crude string search; bad normalisation).
import json,sys,os,importlib.util,copy
from pathlib import Path
SUB='/tmp/opensip-design-corrections/post-reset-review.v5/scratch/subject'
DC=SUB+'/docs/coop/design-corrections'
R=[]
def p(pid,title,ok,detail=''):
    R.append({'id':pid,'title':title,'result':'PASS' if ok else 'FAIL','detail':str(detail)[:900]})
    print(('PASS ' if ok else 'FAIL ')+pid+' :: '+title+((' :: '+str(detail)[:300]) if detail else ''))
sys.path.insert(0,DC+'/foundation'); os.chdir(DC+'/foundation')
s=importlib.util.spec_from_file_location('idm',DC+'/foundation/identity-model.py')
ID=importlib.util.module_from_spec(s); s.loader.exec_module(ID)

# C2 (executable): a semantic identifier is a pure function of its declared semantic value.
# Adding output/operational fields to the *value* must change it; that is why such fields are
# excluded from identity domains by construction. Test the actual identifier function.
base={'projectId':'p','kind':'finding','key':'k'}
a=ID.identifier('workflow.candidate',base)
b=ID.identifier('workflow.candidate',dict(base))
p('C2','semantic identifier is deterministic over its semantic value',a==b and isinstance(a,str),a[:48])
c=ID.identifier('workflow.candidate',dict(base,key='k2'))
p('C2b','a different semantic input yields a different identifier',c!=a,'')
d=ID.identifier('workflow.evidence',base)
p('C2c','domain separation: same value in a different domain yields a different identifier',d!=a,'')

# The only 'verdict' occurrence in the identity model is a cross-record JOIN assertion,
# not an identity input. Prove it: it appears solely in close_run's join guard.
src=Path(DC+'/foundation/identity-model.py').read_text()
lines=[l for l in src.splitlines() if 'verdict' in l]
p('C2d','identity model mentions verdict only in the VERDICT_JOIN consistency guard',
  len(lines)==1 and 'VERDICT_JOIN' in lines[0] and 'def identifier' not in lines[0],
  lines[0].strip()[:200] if lines else 'none')
import inspect
idsrc=inspect.getsource(ID.identifier)+inspect.getsource(ID.ordered)
p('C2e','the identifier/ordered derivation reads no output or operational field name',
  not any(t in idsrc for t in ('verdict','deficiency','parityFields','runProperties','exitCode','findings')),
  idsrc.replace('\n',' ')[:180])

# C8 (corrected normalisation): outside parityFields and the SARIF parityRule prose,
# the command inventory is unchanged from v4.
prev=json.load(open('/tmp/opensip-design-corrections/candidate-subject.v4/docs/coop/design-corrections/workflows/command-inventory.v1.json'))
cur=json.load(open(DC+'/workflows/command-inventory.v1.json'))
def norm(inv):
    x=copy.deepcopy(inv)
    for c in x['commands']: c.pop('parityFields',None)
    for r in x['renderers']:
        if r['format']=='sarif': r.pop('parityRule',None)
    return json.dumps(x,sort_keys=True)
p('C8','with parityFields and the SARIF parityRule text removed, the inventory is identical to v4',
  norm(prev)==norm(cur),'exact equality of the normalised inventories')
# and the ONLY renderer row that changed is sarif
ch=[r['format'] for r in cur['renderers'] if r!=[q for q in prev['renderers'] if q['format']==r['format']][0]]
p('C8b','sarif is the only renderer row changed in the delta',ch==['sarif'],ch)
# top-level keys unchanged
p('C8c','inventory top-level structure unchanged',sorted(prev)==sorted(cur),set(prev)^set(cur))

json.dump(R,open('/tmp/opensip-design-corrections/post-reset-review.v5/probes/claude-probes-C2.json','w'),indent=1)
print('\nC2-group:',sum(1 for x in R if x['result']=='PASS'),'PASS',sum(1 for x in R if x['result']=='FAIL'),'FAIL of',len(R))
