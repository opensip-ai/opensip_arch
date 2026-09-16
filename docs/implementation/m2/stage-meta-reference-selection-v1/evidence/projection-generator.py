from pathlib import Path
import json,random,importlib.util,hashlib
from jsonschema import Draft202012Validator as V
B=Path('/tmp/opensip-implementation/m2-stage-meta-exploration-24');s=importlib.util.spec_from_file_location('projection',B/'structural_meta.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
keys=['$id','$schema','$ref','$dynamicRef','$recursiveRef','$comment','$anchor','$dynamicAnchor','$recursiveAnchor','$vocabulary','$defs','definitions','properties','patternProperties','dependentSchemas','items','contains','additionalProperties','propertyNames','if','then','else','not','unevaluatedItems','unevaluatedProperties','contentSchema','prefixItems','allOf','anyOf','oneOf','dependencies','dependentRequired','type','enum','examples','maximum','exclusiveMaximum','minimum','exclusiveMinimum','multipleOf','maxLength','minLength','maxItems','minItems','maxContains','minContains','maxProperties','minProperties','uniqueItems','deprecated','readOnly','writeOnly','required','title','description','format','contentEncoding','contentMediaType','pattern','unknown']
values=[None,True,False,0,1,-1,2**64,[],{},'','a','a\n','a\r','a\r\n','a\u2028','#','a#','a#\n','a#b','(','(?P<name>.)','https://example.invalid/schema','object','integer',['object','integer'],['object','object'],['a','a'],['a'],[1],[True],[{}],{'x':False},{'x':'a'},{'x':['a']},{'x':{'type':'string'}},{'(':{'pattern':'('}}]
rows=[True,False,None,0,[],{}]+[{k:v}for k in keys for v in values]
rows+= [{'properties':{'nested':v}}for v in list(rows)]
r=random.Random(2409)
for _ in range(2000):rows.append({k:r.choice(values)for k in r.sample(keys,r.randrange(1,8))})
miss=[];changes=[];records=[]
for i,v in enumerate(rows):
 try:V.check_schema(v,format_checker=None);actual=True
 except Exception:actual=False
 try:V.check_schema(v);old=True
 except Exception:old=False
 proposed=m.valid(v)
 if proposed!=actual:miss.append({'index':i,'document':v,'projection':proposed,'referenceFormatAnnotation':actual})
 if old!=actual:changes.append({'index':i,'document':v,'old':old,'formatAnnotation':actual})
 records.append({'document':v,'annotationReference':actual,'projection':proposed,'selectedAmbient':old})
(B/'projection-corpus.json').write_text(json.dumps(records,ensure_ascii=False,separators=(',',':'))+'\n');result={'cases':len(rows),'mismatches':miss,'ambientVersusAnnotationChanges':len(changes),'examples':changes[:8],'standing':'EXPLORATORY NOTSELECTED semanticchange explicit. Integer-onlyJSONinputs; finiteclosedmeta-schema projection, not general instance validator.'};(B/'projection-result.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n');print(json.dumps(result,ensure_ascii=False));assert not miss
