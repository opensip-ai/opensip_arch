import importlib.util,json
from pathlib import Path
root=Path("/tmp/opensip-design-corrections/candidate-subject.v1/docs/coop/design-corrections/foundation")
s=importlib.util.spec_from_file_location("c",root/"canonical.py");C=importlib.util.module_from_spec(s);s.loader.exec_module(C)
schema=json.loads((root/"identity-schemas.v2.json").read_text())
results=[]
for name,value in [("Hash","a"*64+"\n"),("ProjectId","prj1-"+"a"*64+"\n")]:
 sub=dict(schema,**{"$ref":"#/$defs/"+name})
 try:C.validate(sub,value);outcome="ADMITTED"
 except Exception:outcome="REFUSED"
 results.append({"definition":name,"input":value,"outcome":outcome,"expected":"REFUSED"})
print(json.dumps(results,indent=2))
