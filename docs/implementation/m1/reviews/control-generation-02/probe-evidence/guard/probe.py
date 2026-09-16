import json,copy,importlib.util
from pathlib import Path
R=Path(__file__).parent
spec=importlib.util.spec_from_file_location('p',R/'code/prepare.py');P=importlib.util.module_from_spec(spec);spec.loader.exec_module(P)
def run(label,schema,expect):
    try: P.name_variant_objects(copy.deepcopy(schema)); got='pass'
    except ValueError as e: got='refuse: '+str(e)
    ok=(got=='pass')==(expect=='pass')
    rows.append({'probe':label,'expected':expect,'got':got,'ok':ok})
rows=[]
U=lambda comb,a,b:{comb:[{'properties':{'v':a}},{'properties':{'v':b}}]}
arr=({'type':'array','items':{'type':'string'}},{'type':'array','items':{'type':'integer'}})
for comb in ('oneOf','anyOf'):
  for pos,wrap in [('root',lambda n:n),('properties',lambda n:{'type':'object','properties':{'x':n}}),('items',lambda n:{'type':'array','items':n}),('additionalProperties',lambda n:{'type':'object','additionalProperties':n}),('not',lambda n:{'not':n}),('then',lambda n:{'if':{},'then':n}),('else',lambda n:{'if':{},'else':n}),('allOf-branch',lambda n:{'allOf':[n]}),('nested-union-branch',lambda n:{'oneOf':[n,{'type':'null'}]}),('patternProperties',lambda n:{'patternProperties':{'^.+$':n}})]:
    run(f'{comb}/{pos}/array',{'definitions':{'Root':wrap(U(comb,*arr))}},'refuse')
run('object diff under definition oneOf gets named',{'definitions':{'Root':U('oneOf',{'type':'object','required':['a']},{'type':'object','required':['b']})}},'pass')
run('object diff under anyOf (namer does not title) refuses',{'definitions':{'Root':U('anyOf',{'type':'object','required':['a']},{'type':'object','required':['b']})}},'refuse')
run('object diff under nested oneOf (namer only top-level) refuses',{'definitions':{'Root':{'properties':{'x':U('oneOf',{'type':'object','required':['a']},{'type':'object','required':['b']})}}}},'refuse')
run('const string diff',{'definitions':{'Root':U('oneOf',{'type':'string','const':'a'},{'type':'string','const':'b'})}},'refuse')
run('plain string diff description only (no name needed)',{'definitions':{'Root':U('oneOf',{'type':'string','description':'a'},{'type':'string'})}},'pass')
run('integer range diff (no name needed)',{'definitions':{'Root':U('oneOf',{'type':'integer','maximum':3},{'type':'integer','maximum':4})}},'pass')
run('same title different shapes',{'definitions':{'Root':U('oneOf',dict(arr[0],title='T'),dict(arr[1],title='T'))}},'refuse')
run('one titled one untitled',{'definitions':{'Root':U('oneOf',dict(arr[0],title='T'),arr[1])}},'refuse')
run('empty title',{'definitions':{'Root':U('oneOf',dict(arr[0],title=''),dict(arr[1],title='X'))}},'refuse')
run('distinct titles',{'definitions':{'Root':U('oneOf',dict(arr[0],title='L'),dict(arr[1],title='R'))}},'pass')
run('three branches two identical one different',{'definitions':{'Root':{'oneOf':[{'properties':{'v':arr[0]}},{'properties':{'v':arr[0]}},{'properties':{'v':arr[1]}}]}}},'refuse')
run('ref children differ (named by ref)',{'definitions':{'Root':U('oneOf',{'$ref':'#/definitions/A'},{'$ref':'#/definitions/B'})}},'pass')
body=lambda r:{'type':'object','required':[r]}
run('title collides with definition',{'definitions':{'Root':U('oneOf',body('a'),body('b')),'RootVariant0Property0':{'type':'integer'}}},'refuse')
run('title collides with existing inline title',{'definitions':{'Root':U('oneOf',body('a'),body('b')),'Other':{'type':'object','properties':{'q':{'type':'object','title':'RootVariant1Property0'}}}}},'refuse')
run('title collides with generated title of another definition',{'definitions':{'Root':{'oneOf':[{'properties':{'v':body('a')}},{'properties':{'v':body('b')}}]},'RootVariant0':{'oneOf':[{'properties':{'Property0':body('a')}}]}}},'pass')
# residual gaps (finite-claim limits, informational): case-normalized collision, derived-name collision
run('INFO normalized title collision (rootVariant0Property0 def)',{'definitions':{'Root':U('oneOf',body('a'),body('b')),'rootVariant0Property0':{'type':'integer'}}},'info')
run('INFO derived Typify name RootV (untitled prop) not reserved',{'definitions':{'Root':U('oneOf',body('a'),body('b')),'Root2':{'type':'object','properties':{'variant0Property0':{'type':'object'}}}}},'info')
run('INFO allOf sibling differing',{'definitions':{'Root':U('allOf',*arr)}},'info')
run('INFO branch properties inside branch allOf',{'definitions':{'Root':{'oneOf':[{'allOf':[{'properties':{'v':arr[0]}}]},{'allOf':[{'properties':{'v':arr[1]}}]}]}}},'info')
for r in rows: print(('OK  ' if r['ok'] or r['expected']=='info' else 'BAD ')+r['probe']+' -> '+r['got'][:90])
json.dump(rows,open(R/'guard-probe-result.json','w'),indent=1)
