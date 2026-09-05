#!/usr/bin/env python3
"""Replay host foundation design evidence, with an optional external report path."""
import argparse,hashlib,importlib.util,json
from pathlib import Path
from jsonschema import Draft202012Validator
B=Path(__file__).resolve().parent;ROOT=B.parents[2]
spec=importlib.util.spec_from_file_location('host_foundation',B/'host-foundation-model.v1.py');MODEL=importlib.util.module_from_spec(spec);spec.loader.exec_module(MODEL)
def sha(raw):return hashlib.sha256(raw).hexdigest()
def select(value,path):
 if path=='semanticHasUi':return any(k=='ui' or k.startswith('ui.') for k in value['semantic'])
 # Config leaf names intentionally retain their dotted contract names.
 if isinstance(value,dict):
  if path in value:return value[path]
  for key in sorted(value,key=len,reverse=True):
   if path.startswith(key+'.'):return select(value[key],path[len(key)+1:])
 if isinstance(value,list):
  key,sep,rest=path.partition('.');v=value[int(key)];return select(v,rest) if sep else v
 raise KeyError(path)
def main():
 parser=argparse.ArgumentParser();parser.add_argument('--report',type=Path,default=B/'host-foundation-report.v1.json');args=parser.parse_args()
 data=json.loads((B/'host-foundation-cases.v1.json').read_text());rows=[]
 for case in data['cases']:
  try:
   actual=MODEL.evaluate(case['kind'],case['input']);fail=[]
   for p,expected in case['expected'].items():
    try:got=select(actual,p)
    except (KeyError,IndexError,ValueError):got={'missingSelector':p}
    if got!=expected:fail.append({'selector':p,'expected':expected,'actual':got})
   rows.append({'id':case['id'],'kind':case['kind'],'classes':case['classes'],'pass':not fail,'actual':actual,**({'failures':fail} if fail else {})})
  except Exception as e:rows.append({'id':case['id'],'kind':case['kind'],'classes':case['classes'],'pass':False,'uncaught':type(e).__name__+': '+str(e)})
 pinrows=[]
 for p in data['sourcePins']:
  actual=sha((ROOT/p['path']).read_bytes());pinrows.append({'id':'source:'+p['path'],'pass':actual==p['sha256'],'sha256':actual})
 lock=json.loads((B/'component-lock-schema.completed.v3.json').read_text())['properties']['resolutionInputs']['properties'];schema=MODEL.SCHEMA
 Draft202012Validator.check_schema(schema)
 joins=[]
 def objects(v):
  if isinstance(v,dict):
   if v.get('type')=='object':yield v
   for x in v.values():yield from objects(x)
  elif isinstance(v,list):
   for x in v:yield from objects(x)
 closed=list(objects(schema));joins.append({'id':'all-object-paths-closed','objectCount':len(closed),'pass':all(v.get('additionalProperties') is False for v in closed)})
 for layer in ['defaults','global','project','local','environment','flags']:joins.append({'id':'closed-carrier-'+layer,'pass':schema['$defs'][layer].get('additionalProperties') is False})
 for layer in ['defaults','project','local']:
  for field in ['request','pins','holds']:
   a=schema['$defs'][layer]['properties']['components']['properties'][field]
   joins.append({'id':'exact-lock-item-'+layer+'-'+field,'pass':a['items']==lock[field]['items'] and a['maxItems']==128})
 for layer in ['project','local']:
  joins.append({'id':'exact-lock-scopes-'+layer,'pass':schema['$defs'][layer]['properties']['components']['properties']['allowedScopes']==lock['scopeContext']['properties']['allowedScopes']})
 allchecks=rows+pinrows+joins
 report={'status':'PASS' if all(v['pass'] for v in allchecks) else 'FAIL','evidenceClass':'EXECUTABLE REFERENCE DESIGN; NOT PRODUCT QUALIFICATION','total':len(allchecks),'passed':sum(v['pass'] for v in allchecks),'caseCount':len(rows),'sourcePins':pinrows,'schemaJoins':joins,'cases':rows,'subjects':[{'path':str((B/n).relative_to(ROOT)),'sha256':sha((B/n).read_bytes())} for n in ['preview-configuration.schema.v1.json','host-foundation-model.v1.py','host-foundation-cases.v1.json','host-foundation-check.v1.py']],'limitations':data['limitations']}
 args.report.write_text(json.dumps(report,indent=2,ensure_ascii=True)+'\n')
 print(f"{report['status']} {report['passed']}/{report['total']} ({report['caseCount']} cases): {args.report}")
 for row in allchecks:
  if not row['pass']:print(json.dumps(row))
 return 0 if report['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
