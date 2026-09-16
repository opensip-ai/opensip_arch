"""Portable local reference checks; no full graph/replay claim."""
import argparse, ast, functools, itertools, json, sys, types, unicodedata
from pathlib import Path
ap=argparse.ArgumentParser();ap.add_argument('--architecture',type=Path,required=True);args=ap.parse_args();A=args.architecture;U=Path(__file__).resolve().parents[1]
old_i=A/'docs/implementation/m2/recognition-derived-reference-selection-v1/reference/identity_model.py'
old_w=A/'docs/coop/design-corrections/workflows/workflows_model.v1.py'
class AdmissionError(ValueError):pass

def functions(path,names):
    module=ast.parse(path.read_bytes());nodes=[n for n in module.body if isinstance(n,ast.FunctionDef) and n.name in names]
    assert {n.name for n in nodes}==set(names)
    env={'C':types.SimpleNamespace(AdmissionError=AdmissionError)}
    exec(compile(ast.Module(body=nodes,type_ignores=[]),str(path),'exec'),env)
    return env

def remainder(path,name):
    raw=path.read_text()
    if path==old_w:
        record=json.loads((A/'docs/implementation/m1/source-selection-v2/successor.json').read_bytes())
        override=next(o for o in record['passageOverrides'] if 'workflows_model.v1.py' in o['parent']['path'])
        assert raw.splitlines()[override['selector']['line']-1]==override['before']
        assert raw.count(override['before'])==1
        raw=raw.replace(override['before'],override['after'])
    m=ast.parse(raw);m.body=[n for n in m.body if not(isinstance(n,ast.FunctionDef) and n.name==name)]
    return ast.dump(m,include_attributes=False)
assert remainder(old_i,'predicate_node_at')==remainder(U/'reference/identity_model.py','predicate_node_at')
assert remainder(old_w,'glob_match')==remainder(U/'reference/workflows_model.v1.py','glob_match')
old_glob=functions(old_w,['glob_match'])['glob_match'];new_glob=functions(U/'reference/workflows_model.v1.py',['glob_match'])['glob_match']
# Deliberately declarative/exhaustive, sharing no greedy/backtracking implementation.
@functools.lru_cache(None)
def ordinary(pattern,candidate):
    if not pattern:return not candidate
    if pattern[0]=='*':return any(ordinary(pattern[1:],candidate[k:]) for k in range(len(candidate)+1))
    return bool(candidate) and (pattern[0]=='?' or pattern[0]==candidate[0]) and ordinary(pattern[1:],candidate[1:])
def normative(pattern,candidate):
    p,s=pattern.split('/'),candidate.split('/')
    @functools.lru_cache(None)
    def walk(i,j):
        if i==len(p):return j==len(s)
        if p[i]=='**':return any(walk(i+1,k) for k in range(j,len(s)+1))
        return j<len(s) and ordinary(p[i],s[j]) and walk(i+1,j+1)
    return walk(0,0)
strings=[''.join(p)for n in range(5)for p in itertools.product('ab*?/',repeat=n)]
pairs=itertools.product(strings,strings)
extra=[('*a','*ba'),('a*b','a*xb'),('**a','**ba'),('*?','*ab'),('**/*.ts','a.ts'),('**/*.ts','src/a.ts'),('?.ts','é.ts'),('?.ts','e\u0301.ts'),('?', '💠'),('[ab]','a'),('[ab]','[ab]'),('{a,b}','a'),('{a,b}','{a,b}'),('src/**','src'),('src/','src'),('a/**/b','a/x/y/b'),('a/*/b','a//b')]
count=0;changes=0;examples=[]
for p,s in itertools.chain(pairs,extra):
    before,after,want=old_glob(p,s),new_glob(p,s),normative(p,s);count+=1
    assert after==want,(p,s,before,after,want)
    if before!=after:
        changes+=1
        if len(examples)<12:examples.append({'pattern':p,'candidate':s,'before':before,'after':after})
old_env=functions(old_i,['predicate_node_at','predicate_child_addresses']);new_env=functions(U/'reference/identity_model.py',['predicate_node_at','predicate_child_addresses'])
leaf={'op':'exists'};tree={'op':'and','operands':[leaf,{'op':'not','operand':leaf},{'op':'or','operands':[leaf,leaf]}]}
def result(fn,address):
    try:return {'node':fn(tree,address)}
    except AdmissionError as e:return {'refusal':str(e)}
    except Exception as e:return {'exception':type(e).__name__}
addresses=['p','p.0','p.1','p.1.0','p.2','p.2.0','p.2.1','p.3','p.0.0','p.1.1','p.00','p.01','p.','p..0','q','P','p.-1','p.+0','p. 0','p.0 ','p.0\n','p.1_0','p.'+'9'*4094]
for address in addresses:
    assert result(old_env['predicate_node_at'],address)==result(new_env['predicate_node_at'],address),address
numeric=[]
for n in range(128,0x110000):
    c=chr(n)
    if c.isdigit():numeric.append(c)
changes_address=[];unicode_count=0
for part in numeric+['٠١','０１','٠1','0١','１0','²0','𝟘1']:
    address='p.'+part;before=result(old_env['predicate_node_at'],address);after=result(new_env['predicate_node_at'],address);unicode_count+=1
    assert after=={'refusal':'PREDICATE_ADDRESS'},(address,after)
    if before!=after:changes_address.append({'address':address,'before':before,'after':after})
# Exhaustive reachable address traversal independently checks emitted spelling.
stack=[(tree,'p')];emitted=0
while stack:
    node,address=stack.pop();emitted+=1
    assert new_env['predicate_node_at'](tree,address)==node
    assert new_env['predicate_child_addresses'](node,address)==old_env['predicate_child_addresses'](node,address)
    children=node.get('operands',[node['operand']] if 'operand'in node else [])
    stack.extend((child,address+'.'+str(i))for i,child in enumerate(children))
print(json.dumps({'python':sys.version.split()[0],'unicode':unicodedata.unidata_version,'unchangedAstOutsideTwoFunctionsAgainstSelectedEffectivePredecessor':True,'inheritedInterruptionOverridePreserved':True,'globCases':count,'globChangedResults':changes,'globMismatches':0,'globChangeExamples':examples,'asciiAddressControls':len(addresses),'unicodeAddressControls':unicode_count,'unicodeChangedResults':len(changes_address),'unicodeChangeExamples':changes_address[:12],'emittedAddressRoundTrips':emitted,'scope':'Local actual reference function/AST checks, independent declarative glob law; no complete Run or replay.'},ensure_ascii=False,indent=2))
