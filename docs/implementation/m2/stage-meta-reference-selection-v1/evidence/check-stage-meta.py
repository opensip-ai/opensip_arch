from pathlib import Path
import argparse,ast,hashlib,importlib.util,json,re,copy
from jsonschema import Draft202012Validator as V
p=argparse.ArgumentParser();p.add_argument('--architecture',type=Path,required=True);args=p.parse_args();A=args.architecture;M=A/'docs/implementation/m2';U=M/'stage-meta-reference-selection-v1';R=U/'reference'
def load(path,name):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
C=load(M/'exact-schema-profile-selection-v1/reference/canonical.py','stage_canonical');new=load(R/'stage_schema_model.v1.py','stage_profile');oldpath=M/'predicate-matching-reference-selection-v1/reference/identity_model.py';newpath=R/'identity_model.py'
def stage(path):
 tree=ast.parse(path.read_bytes());functions=[n for n in tree.body if isinstance(n,ast.FunctionDef)and n.name in ['stage_output_schema_member_path','admit_stage_output_schema']];env={'C':C,'hashlib':hashlib,'importlib':__import__('importlib'),'HERE':R,'STAGE_OUTPUT_INTERFACE_DIRECTORY':'opensip-interface/stage-output/','STAGE_OUTPUT_DECLARATION':'x-opensip-stage-output','_STAGE_OPERATION_SEGMENT':re.compile(r'[a-z0-9][a-z0-9._-]{0,127}')};exec(compile(ast.Module(body=functions,type_ignores=[]),str(path),'exec'),env);return env['admit_stage_output_schema']
def without_stage(path):
 t=ast.parse(path.read_bytes());t.body=[n for n in t.body if not(isinstance(n,ast.FunctionDef)and n.name=='admit_stage_output_schema')];return ast.dump(t,include_attributes=False)
assert without_stage(oldpath)==without_stage(newpath)
corpus=json.loads((U/'evidence/projection-corpus.json').read_bytes());mismatches=[];changed=0
for i,row in enumerate(corpus):
 try:V.check_schema(row['document'],format_checker=None);expected=True
 except Exception:expected=False
 assert expected==row['annotationReference'],i
 try:V.check_schema(row['document']);former=True
 except Exception:former=False
 assert former==row['selectedAmbient'],i
 try:new.admit_document(row['document']);actual=True
 except new.StageSchemaInvalid:actual=False
 if actual!=row['annotationReference']:mismatches.append(i)
 changed+=actual!=row['selectedAmbient']
assert not mismatches
oldstage=stage(oldpath);newstage=stage(newpath)
def packet(doc=None,pretty=False):
 doc=copy.deepcopy(doc)if doc is not None else {'$schema':'https://json-schema.org/draft/2020-12/schema','type':'object','x-opensip-stage-output':{'schemaVersion':1,'operation':'analyze','outputDomains':['fact']}}
 raw=(json.dumps(doc,indent=2).encode()if pretty else C.canonical(doc));sha=hashlib.sha256(raw).hexdigest();spec={'operation':'analyze','outputDomains':['fact'],'outputSchemaDigest':sha};closure={'tree':[{'path':'opensip-interface/stage-output/analyze.schema.json','sha256':sha,'bytes':len(raw)}]};return spec,closure,raw
def outcome(fn,args):
 try:fn(*args);return 'checked'
 except C.AdmissionError as e:return str(e)
rows=[]
def check(label,args,expected_change=False):
 a=outcome(oldstage,args);b=outcome(newstage,args);assert(a!=b)==expected_change,(label,a,b);rows.append({'label':label,'old':a,'candidate':b})
check('canonical',packet());check('pretty',packet(pretty=True))
base=json.loads(packet()[2])
for label,change,delta in [('invalid-pattern',{'pattern':'('},True),('invalid-pattern-property',{'patternProperties':{'(':True}},True),('remote-ref',{'$ref':'https://example.invalid/schema'},False),('nested-bool',{'properties':{'a':False}},False),('unknown-keyword',{'custom':{'pattern':'('}},False),('wrong-schema',{'$schema':'draft07'},False),('wrong-declaration',{'x-opensip-stage-output':{}},False),('anchor-lf',{'$anchor':'a\n'},False),('anchor-cr',{'$anchor':'a\r'},False),('id-fragment',{'$id':'a#bad'},False),('bad-type',{'type':'unknown'},False)]:
 check(label,packet({**base,**change}),delta)
for label,edit in [('unregistered',lambda s,c:c.update(tree=[])),('registration-mismatch',lambda s,c:c['tree'][0].update(sha256='0'*64)),('operation-invalid',lambda s,c:s.update(operation='../escape'))]:
 s,c,raw=packet();edit(s,c);check(label,(s,c,raw))
s,c,raw=packet();check('digest-mismatch',(s,c,b'{}'))
for label,raw in [('float',b'{"x":1.0}'),('duplicate',b'{"x":1,"x":2}'),('invalid-json',b'{')]:
 s,c,_=packet();s['outputSchemaDigest']=hashlib.sha256(raw).hexdigest();c['tree'][0]['sha256']=s['outputSchemaDigest'];check(label,(s,c,raw))
# Adversarial ambient format registrations cannot affect explicit None.
checker=V.FORMAT_CHECKER;prior=checker.checkers.copy();ambient=[]
try:
 for name in ['uri','uri-reference','regex']:checker.checkers[name]=(lambda _:False,())
 for d in [base,{**base,'pattern':'a'},{**base,'$ref':'not a URI'},{**base,'patternProperties':{'a':True}}]:
  new.admit_document(d);ambient.append(True)
finally:checker.checkers.clear();checker.checkers.update(prior)
result={'corpusCases':len(corpus),'candidateMismatches':mismatches,'intentionalCompatibilityChanges':changed,'stageCases':rows,'ambientFormatMutationControls':len(ambient),'otherIdentityASTUnchanged':True,'scope':'Proposed portable structural meta-schema profile only. Not instance execution, regex compilation, full Run or replay.'};print(json.dumps(result,ensure_ascii=False,indent=2))
