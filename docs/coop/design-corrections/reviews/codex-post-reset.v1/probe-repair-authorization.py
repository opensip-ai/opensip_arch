import importlib.util, json, copy
from pathlib import Path
root=Path("/tmp/opensip-design-corrections/candidate-subject.v1/docs/coop/design-corrections")
spec=importlib.util.spec_from_file_location("security_probe",root/"security/security_lifecycle_model_v1.py")
s=importlib.util.module_from_spec(spec);spec.loader.exec_module(s)
f=json.loads((root/"security/repair-authorization-cases.v1.json").read_text())
a=copy.deepcopy(f["authorizationBase"]);c=copy.deepcopy(f["ctxBase"])
c["recipeClosureId"]=a["recipeClosureId"]
a["recipeClosureId"]="closure2:"+"7"*64
s.validate_input("RepairApplyAuthorizationV1",a)
r=s.admit_repair_authorization(a,c)
print(json.dumps({"observation":"Foreign recipe closure admitted by security primitive despite host expected recipe; workflow separately checks actual recipe trust, so no end-to-end bypass is claimed", "expectedRecipe":c["recipeClosureId"],"authorizationRecipe":a["recipeClosureId"],"result":r},indent=2))
