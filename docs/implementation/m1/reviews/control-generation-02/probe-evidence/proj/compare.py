import json,copy,importlib.util,sys
from pathlib import Path
R=Path(__file__).parent; S=Path('/tmp/opensip-implementation/m1-control-generation-subject-02')
def load(n):
    spec=importlib.util.spec_from_file_location('p'+n,R/('s'+n)/'prepare.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
P1,P2=load('1'),load('2')
docs={}
for p in sorted((S/'schemas/sources').glob('*.json')):
    d=json.loads(p.read_text());docs[d['$id']]=d
opts=json.loads((S/'tools/contracts/options.json').read_text())
f1=P1.flatten(docs,opts);f2=P2.flatten(docs,opts);print('flat equal',f1==f2,len(f2['definitions']))
r1=P1.name_variant_objects(P1.schema_map(copy.deepcopy(f1),P1.rust))
f2c=copy.deepcopy(f2);r2=P2.name_variant_objects(P2.schema_map(f2c,P2.rust));print('flatten input unmutated',f2c==f2)
t1=P1.schema_map(copy.deepcopy(f1),P1.typescript);t2=P2.schema_map(copy.deepcopy(f2),P2.typescript)
diff=[n for n in r2['definitions'] if r1['definitions'][n]!=r2['definitions'][n]]
print('rust projection defs differing 01 vs 02',diff,'whole equal',r1==r2,'ts equal',t1==t2)
base=P2.schema_map(copy.deepcopy(f2),P2.rust)
print('defs changed by naming',[n for n in base['definitions'] if base['definitions'][n]!=r2['definitions'][n]])
# the only delta from unnamed base is title keys on the 16 control bodies
b=copy.deepcopy(r2['definitions']['Control3Root'])
for br in b['oneOf']: br['properties']['body'].pop('title')
print('control differs only by body titles',b==base['definitions']['Control3Root'])
# guard on unnamed base must refuse
try: P2.refuse_ambiguous_union_properties(copy.deepcopy(base)); print('guard on unnamed base: PASSED (unexpected)')
except ValueError as e: print('guard on unnamed base refuses:',e)
json.dump({'defs':len(r2['definitions']),'rustDiff01vs02':diff,'tsEqual':t1==t2},open(R/'projection-result.json','w'))
