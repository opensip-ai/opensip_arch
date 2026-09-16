import json,copy,hashlib
from pathlib import Path
from jsonschema import Draft202012Validator,validators,ValidationError
W=Path(__file__).parent; arch=Path('/Users/sb/code/opensip-ai/opensip_arch/docs/coop/completion')
schema=json.loads(Path('/tmp/opensip-implementation/m1-control-generation-subject-01/schemas/sources/control.v3.schema.json').read_bytes())
assert hashlib.sha256(json.dumps(schema).encode()).hexdigest() # parsed
# independent reviewer extension: count strict UTF-8 bytes; lone surrogates are invalid instances
def utf8(v,limit,inst,s):
    if isinstance(inst,str):
        try: n=len(inst.encode('utf-8'))
        except UnicodeEncodeError: yield ValidationError('surrogate'); return
        if n>limit: yield ValidationError('utf8')
V=validators.extend(Draft202012Validator,{'x-maxUtf8Bytes':utf8})(schema)
pos=json.loads(Path(W.parent/'corpus/positive.json').read_text()); bases={}
for p in pos: bases.setdefault(p['type'],p)
types=[b['properties']['type']['const'] for b in schema['oneOf']]
cases=[]
def add(cid,value,kind,raw=None):
    if raw is None: raw=json.dumps(value,ensure_ascii=False,separators=(',',':'))
    cases.append({'id':cid,'kind':kind,'raw':raw,'valid':V.is_valid(value) if value is not None else False})
def setp(obj,path,val):
    o=obj
    for k in path[:-1]:
        if isinstance(o,list):
            if len(o)<=k: return False
            o=o[k]
        elif isinstance(o,dict) and k in o: o=o[k]
        else: return False
    if isinstance(o,dict) or (isinstance(o,list) and len(o)>path[-1]): o[path[-1]]=val; return True
    return False
def walk(node,ipath,out):
    if not isinstance(node,dict): return
    if 'x-maxUtf8Bytes' in node or node.get('type')=='integer': out.append((ipath,node))
    for k,c in node.get('properties',{}).items(): walk(c,ipath+[k],out)
    if isinstance(node.get('items'),dict): walk(node['items'],ipath+[0],out)
    for k in ('allOf','anyOf','oneOf'):
        for c in node.get(k,[]): walk(c,ipath,out)
    for k in ('then','else'): walk(node.get(k),ipath,out)
skipped=0;informative=[]
for vi,branch in enumerate(schema['oneOf']):
    t=types[vi]; leaves=[]; walk(branch,[],leaves)
    for ipath,node in leaves:
        pid='/'.join(map(str,ipath))
        if 'x-maxUtf8Bytes' in node:
            L=node['x-maxUtf8Bytes']; res={}
            for w,ch in ((1,'a'),(2,'é'),(3,'界'),(4,'🦀')):
                for label,s in (('exact',ch*(L//w)+'a'*(L%w)),('over',ch*(L//w)+'a'*(L%w)+'a'),('tail-exact','a'*(L-w)+ch),('tail-over','a'*(L-w+1)+ch),('scalars-over',ch*(L//w+1))):
                    v=copy.deepcopy(bases[t])
                    if not setp(v,ipath,s): skipped+=1; continue
                    add(f'utf8/{t}/{pid}/w{w}/{label}',v,'utf8'); res[(w,label)]=cases[-1]['valid']
            if res.get((1,'exact')) and not res.get((1,'over')): informative.append(f'{t}/{pid}')
        else:
            lo=node.get('minimum',-(2**63)); hi=node.get('maximum',2**64-1)
            for label,n in (('min',lo),('max',hi),('below',lo-1),('above',hi+1)):
                v=copy.deepcopy(bases[t])
                if not setp(v,ipath,n): skipped+=1; continue
                add(f'int/{t}/{pid}/{label}',v,'integer')
for i,a in enumerate(types):
    for j,b in enumerate(types):
        if i!=j:
            v=copy.deepcopy(bases[a]); v['body']=copy.deepcopy(bases[b]['body']); add(f'swap/{a}<-{b}',v,'swap')
src=json.loads((arch/'control-completion.cases.v5.json').read_bytes())
for c in src['cases']:
    if 'frameHex' not in c: continue
    f=bytes.fromhex(c['frameHex'])
    if len(f)>=4 and int.from_bytes(f[:4],'big')==len(f)-4:
        body=f[4:]
        try: json.loads(body.decode('utf-8'),parse_float=lambda _:(_ for _ in ()).throw(ValueError()),object_pairs_hook=lambda r: (_ for _ in ()).throw(ValueError()) if len({k for k,_ in r})!=len(r) else dict(r)); continue
        except Exception: pass
        try: add('lexical/'+c['id'],None,'lexical',body.decode('utf-8'))
        except UnicodeDecodeError: cases.append({'id':'lexical/'+c['id'],'kind':'lexical','rawHex':body.hex(),'valid':False})
(W/'cases.json').write_text(json.dumps(cases,ensure_ascii=False,indent=1))
import collections
print('cases',len(cases),collections.Counter((c['kind'],c['valid']) for c in cases),'skipped',skipped,'utf8 boundary-informative fields',len(informative))
print(informative)
