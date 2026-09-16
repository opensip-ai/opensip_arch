from pathlib import Path
import importlib.util,json,hashlib,sys
S=Path(sys.argv[1]);O=Path(sys.argv[2]);O.mkdir();f=S/'docs/coop/design-corrections/native/native_evidence_model.v2.py';s=importlib.util.spec_from_file_location('root_jsconfig_modes',f);N=importlib.util.module_from_spec(s);s.loader.exec_module(N)
markers=[('jsconfig-default',{'jsconfig.json':{}},'js-allowjs','js-program'),('jsconfig-false',{'jsconfig.json':{'allowJs':False}},'ts-tsconfig','ts-program'),('jsconfig-true',{'jsconfig.json':{'allowJs':True}},'js-allowjs','js-program'),('tsconfig-false',{'tsconfig.json':{'allowJs':False}},'ts-tsconfig','ts-program'),('tsconfig-true',{'tsconfig.json':{'allowJs':True}},'js-allowjs','js-program'),('package-only',{'package.json':{}},'js-synthesized','js-program'),('tsconfig-before-jsconfig',{'tsconfig.json':{'allowJs':False},'jsconfig.json':{'allowJs':True}},'ts-tsconfig','ts-program')]
rows=[]
for name,inputs,mode,kind in markers:
 m={k:dict(v,sha256='b'*64)for k,v in inputs.items()};out=N.discover_units(m);u=out['units'][0];rows.append({'name':name,'markers':m,'expected':[mode,kind],'observed':[u['languageMode'],u['unitKind']],'passed':[u['languageMode'],u['unitKind']]==[mode,kind]})
r={'standing':'Root standalone trusted-marker reference probe of explicit native mode-table contract, no compiler/host qualification.','source':str(S),'modelSha256':hashlib.sha256(f.read_bytes()).hexdigest(),'rows':rows,'passed':all(x['passed']for x in rows)};(O/'report.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r));raise SystemExit(not r['passed'])
