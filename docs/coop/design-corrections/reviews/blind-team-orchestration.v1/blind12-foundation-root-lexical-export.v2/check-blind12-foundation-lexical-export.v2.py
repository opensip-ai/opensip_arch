from pathlib import Path
import importlib.util,json,hashlib,shutil
B=Path('/tmp/opensip-design-corrections');F=B/'candidate-subject.v24/docs/coop/design-corrections/foundation/identity-model.v3.py'
s=importlib.util.spec_from_file_location('root_lexical_selected_owner',F);M=importlib.util.module_from_spec(s);s.loader.exec_module(M)
p=B/'consumer-b.v12-team-foundation-corrections.v1/output/foundation/lexical-admission.json';j=json.loads(p.read_text());rows=[]
for r in j['vectors']:
    raw=bytes.fromhex(r['rawHex']);admitted=True;reason=None
    try:M.C.parse(raw)
    except Exception as exc:admitted=False;reason=type(exc).__name__+': '+str(exc)
    expected=r['classification']=='valid'
    rows.append({'name':r['name'],'classification':r['classification'],'admitted':admitted,'passed':admitted==expected,'reason':reason,'rawSha256':hashlib.sha256(raw).hexdigest()})
report={'standing':'Actual frozen raw parser on all exact exported lexical vectors; no consumer helper import or expected-output substitution. Not full graph admission.','inputSha256':hashlib.sha256(p.read_bytes()).hexdigest(),'ownerSha256':hashlib.sha256(F.read_bytes()).hexdigest(),'checks':rows,'passed':all(r['passed']for r in rows),'limitations':'Compares admitted/refused boundary, not equality of implementation-specific error code spellings. Consumer helper source assertions read separately; not reexecuted here.'}
o=B/'blind12-foundation-root-lexical-export.v2';o.mkdir();shutil.copy2(p,o/p.name);shutil.copy2(Path(__file__),o/Path(__file__).name);(o/'report.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps({'count':len(rows),'passed':report['passed'],'failures':[r for r in rows if not r['passed']]}));assert report['passed']
