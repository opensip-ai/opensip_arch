from pathlib import Path
import sys,json,hashlib
from referencing import Registry,Resource
from referencing.jsonschema import DRAFT202012
B=Path("/tmp/opensip-design-corrections")
sys.path.insert(0,str(B/"candidate-subject.v37/docs/coop/design-corrections/foundation"))
import canonical
from jsonschema import ValidationError,Draft202012Validator
P=B/"termination-exclusivity-successor.v1/source"
V=json.loads((P/"docs/coop/design-corrections/workflows/workflow-cases.v1.json").read_text())["terminationVectors"]
rows=[]
for label,S in [("baseline37",B/"candidate-subject.v37"),("successor-working",P)]:
 W=S/"docs/coop/design-corrections/workflows/schemas";schemas={}
 for p in [*W.glob("*.schema.json"),*(W/"evaluator3").glob("*.schema.json")]:
  d=json.loads(p.read_text());Draft202012Validator.check_schema(d);schemas[d["$id"]]=d
 reg=Registry().with_resources((u,Resource(contents=d,specification=DRAFT202012)) for u,d in schemas.items())
 def admit(ref,value):
  try:canonical.typed(value);canonical.ExactValidator({"$ref":ref},registry=reg).validate(value);return True
  except ValidationError:return False
 for profile in ("legacy","current3"):
  u="urn:opensip:product-v1:workflows:"+("evaluator3:" if profile=="current3" else "")+"common"+(":3" if profile=="current3" else "")
  for kind in ("accept","reject"):
   for i,t in enumerate(V[kind]):
    t=dict(t)
    if t.get("runId")=="$RUN1":t["runId"]=("run3:" if profile=="current3" else "run2:")+"a"*64
    rows.append({"source":label,"profile":profile,"vector":kind+"-"+str(i),"expectedLawful":kind=="accept","actualAdmit":admit(u+"#/$defs/StepTermination",t)})
 legacy=schemas["urn:opensip:product-v1:workflows:common"]["$defs"]["StepTermination"]
 current=schemas["urn:opensip:product-v1:workflows:evaluator3:common:3"]["$defs"]["StepTermination"]
 assert legacy==current
checks={"allSuccessorVectors":all(r["actualAdmit"]==r["expectedLawful"] for r in rows if r["source"]=="successor-working"),"newTwelveRejectsAdmittedAtBaselineBothProfiles":all(r["actualAdmit"] for r in rows if r["source"]=="baseline37" and r["vector"].startswith("reject-") and int(r["vector"].split("-")[1])>=12),"bothDefinitionsEqual":True}
result={"standing":"Typed carrier admission only; no Run replay or host qualification", "checks":checks,"rows":rows,"passed":all(checks.values())}
p=B/"root-source38-focused.v1/carrier-discrimination.json";p.write_text(json.dumps(result,indent=2)+"\n");print(json.dumps({"checks":checks,"rows":len(rows),"passed":result["passed"]}));sys.exit(0 if result["passed"] else 1)
