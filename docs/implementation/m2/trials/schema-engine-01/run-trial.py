from pathlib import Path
import json,subprocess,importlib.util,hashlib,random,itertools
from referencing import Registry,Resource
A=Path('/Users/sb/code/opensip-ai/opensip_arch');P=A.parent/'opensip';B=Path('/tmp/opensip-implementation/m2-schema-engine-trial-01');F=A/'docs/coop/design-corrections/foundation/canonical.py'
spec=importlib.util.spec_from_file_location('reference_canonical',F);ref=importlib.util.module_from_spec(spec);spec.loader.exec_module(ref)
rows=json.loads((P/'schemas/registry.json').read_bytes())['sources'];documents=[];pins=[]
for row in rows:
 raw=(P/row['sourcePath']).read_bytes();assert hashlib.sha256(raw).hexdigest()==row['sourceSha256'];documents.append(ref.parse(raw));pins.append({'path':row['sourcePath'],'bytes':len(raw),'sha256':row['sourceSha256']})
(B/'schema-source-pins.json').write_text(json.dumps(pins,indent=2)+'\n')
byid={d['$id']:d for d in documents};entries=[];schemas={}
for d in documents:
 for pointer,node in [('',d)]+[('/$defs/'+k,v) for k,v in d.get('$defs',{}).items()]:
  entry=d['$id']+'#'+pointer;entries.append(entry);schemas[entry]=(node,d['$id'])
# Synthetic focused keyword cross-products, each a closed local document.
def add(name,s):
 d={'$id':'urn:trial:'+name,'$schema':'https://json-schema.org/draft/2020-12/schema',**s};documents.append(d);byid[d['$id']]=d;entry=d['$id']+'#';entries.append(entry);schemas[entry]=(d,d['$id']);return entry
synthetic={
'exact-const':{'const':1},'exact-enum':{'enum':[False,1,{'a':1},[True]]},'scalar-length':{'type':'string','minLength':2,'maxLength':3},
'array-prefix':{'type':'array','prefixItems':[{'const':0},{'type':'boolean'}],'items':{'type':'string'}},
'array-tail-refusal':{'prefixItems':[True],'items':False},'contains':{'contains':{'const':0}},'unique':{'uniqueItems':True},
'allof':{'allOf':[{'type':'integer'},{'minimum':0},{'maximum':2}]},'anyof':{'anyOf':[{'type':'integer'},{'type':'boolean'}]},
'oneof-overlap':{'oneOf':[{'type':'integer'},{'minimum':0}]},'negation':{'not':{'type':'integer'}},
'conditional':{'if':{'type':'integer'},'then':{'minimum':0},'else':{'type':'string'}},
'ignored-then':{'then':False,'else':False},'object':{'type':'object','required':['a'],'properties':{'a':{'type':'integer'}},'additionalProperties':False},
'propertynames':{'propertyNames':{'minLength':2}},'object-count':{'minProperties':1,'maxProperties':2},
'array-count':{'minItems':1,'maxItems':2},'integer-bounds':{'minimum':-9223372036854775808,'maximum':18446744073709551615},
'annotation-byte-limit':{'type':'string','x-maxUtf8Bytes':1},
'pattern-props':{'properties':{'a':{'const':1}},'patternProperties':{'^[a-z][a-zA-Z0-9]*(?![\\s\\S])':{'type':'boolean'}},'additionalProperties':False},
'recursive':{'anyOf':[{'type':'null'},{'type':'array','items':{'$ref':'#'}}]},
}
for name,s in synthetic.items():add(name,s)
patterns=[r['pattern'] for r in json.loads((B.with_name('m2-schema-pattern-trial-03')/'pattern-census.json').read_bytes())['patterns']]
patterns.append('^.+$')
for i,p in enumerate(patterns):
 add('pattern-'+str(i),{'pattern':p});add('not-pattern-'+str(i),{'not':{'pattern':p}});add('property-pattern-'+str(i),{'patternProperties':{p:{'type':'integer'}},'additionalProperties':False})
reg=Registry().with_resources((d['$id'],Resource.from_contents(d)) for d in documents)
validators={e:ref.ExactValidator({'$ref':e},registry=reg) for e in entries}
# A bounded witness synthesizer broadens root/definition coverage; the oracle,
# not the synthesizer, determines validity. It is not a fixture authority.
def resolve(r,owner):
 ident,_,frag=r.partition('#');ident=ident or owner;v=byid[ident]
 for part in frag.split('/')[1:]:v=v[part.replace('~1','/').replace('~0','~')]
 return v,ident
pattern_examples={}
for line in (B.with_name('m2-schema-pattern-trial-03')/'cases.jsonl').read_bytes().splitlines():
 c=json.loads(line)
 if c['pattern'] not in pattern_examples and __import__('re').search(c['pattern'],c['text']):pattern_examples[c['pattern']]=c['text']
def synth(s,owner,depth=0):
 if depth>12:return None
 if type(s) is bool:return None
 if 'const' in s:return s['const']
 if 'enum' in s:return s['enum'][0]
 if '$ref' in s:return synth(*resolve(s['$ref'],owner),depth+1)
 for k in ['oneOf','anyOf']:
  if k in s:return synth(s[k][0],owner,depth+1)
 t=s.get('type');t=t[0] if isinstance(t,list) else t
 if t=='object' or 'required' in s:
  v={k:synth(s.get('properties',{}).get(k,{}),owner,depth+1) for k in s.get('required',[])}
 elif t=='array':v=[synth(s.get('prefixItems',[])[i] if i<len(s.get('prefixItems',[])) else s.get('items',{}),owner,depth+1) for i in range(min(s.get('minItems',0),10))]
 elif t=='integer':v=s.get('minimum',0)
 elif t=='boolean':v=False
 elif t=='string':v=pattern_examples.get(s.get('pattern'),'a'*min(s.get('minLength',0),256))
 else:v=None
 for rule in s.get('allOf',[]):
  extra=synth(rule,owner,depth+1)
  if isinstance(v,dict) and isinstance(extra,dict):v.update(extra)
  elif v is None:v=extra
 return v
values=[None,False,True,-9223372036854775808,-1,0,1,2,18446744073709551615,'','a','ab','a\n','😀','😀é','a\u0000',[],[0],[False],[True,1],[1,True],[1,1],[0,False,'a'],{}, {'a':0},{'a':True},{'aa':1},{'a':1,'b':2},{'a':1,'b':2,'c':3}]
rng=random.Random(20260915)
for _ in range(150):
 v=rng.choice(values[:18]);values.append([v,rng.choice(values[:18])]);values.append({'a':v,'b':rng.choice(values[:18])})
cases=[]
for entry,(schema,owner) in schemas.items():
 local=values[:29]+[synth(schema,owner)]
 if entry.startswith('urn:trial:'):local=values
 for value in local:cases.append({'ref':entry,'value':value})
# Full selected pattern corpus through direct schema and not-schema contexts.
for line in (B.with_name('m2-schema-pattern-trial-03')/'cases.jsonl').read_bytes().splitlines():
 c=json.loads(line);i=patterns.index(c['pattern'])
 if len(c['text'])<=300:
  cases.append({'ref':'urn:trial:pattern-'+str(i)+'#','value':c['text']})
  cases.append({'ref':'urn:trial:not-pattern-'+str(i)+'#','value':c['text']})
for value in ['', '\n','\n\n','a','a\n','a\n\n','a\r','a\u2028','a\nb','😀\n']:
 for form in ['pattern-','not-pattern-']:
  cases.append({'ref':'urn:trial:'+form+str(len(patterns)-1)+'#','value':value})
# Distinct pointer escapes and booleans verified in standalone later controls.
initial={'documents':documents,'entries':entries};initialraw=json.dumps(initial,ensure_ascii=True,separators=(',',':')).encode();assert len(initialraw)<ref.MAX_BYTES
(B/'initial.json').write_bytes(initialraw+b'\n')
raw=b''.join(json.dumps(c,ensure_ascii=True,separators=(',',':')).encode()+b'\n' for c in cases);(B/'cases.jsonl').write_bytes(raw)
exe=B/'probe/target/debug/opensip-schema-engine-trial'
r=subprocess.run([str(exe)],input=initialraw+b'\n'+raw,capture_output=True,timeout=300);(B/'probe.stdout').write_bytes(r.stdout);(B/'probe.stderr').write_bytes(r.stderr);assert r.returncode==0,r.stderr.decode();lines=r.stdout.splitlines();assert lines[0]==b'READY',lines[:4];assert len(lines)==len(cases)+1
mismatches=[];positives=set();valid=0
for c,a in zip(cases,lines[1:]):
 expected=validators[c['ref']].is_valid(c['value'])
 if expected:valid+=1;positives.add(c['ref'])
 if a not in [b'0',b'1'] or (a==b'1')!=expected:mismatches.append({**c,'reference':expected,'actual':a.decode()})
(B/'mismatches.json').write_text(json.dumps(mismatches,indent=2)+'\n')
result={'standing':'Exploratory exact schema interpreter; no registered descriptor admission or product selection','sources':len(rows),'selectedEntries':len(entries)-len(synthetic)-3*len(patterns),'syntheticEntries':len(synthetic)+3*len(patterns),'cases':len(cases),'referenceValidCases':valid,'positiveEntries':len(positives),'mismatches':len(mismatches),'patternSemantics':'Closed69 Python re.search equivalent predicates; finite corpus only','xMaxUtf8Bytes':'annotation at ExactValidator shape boundary; additional owner law not implemented','productChanged':False};(B/'result.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2));assert not mismatches,mismatches[:8]
