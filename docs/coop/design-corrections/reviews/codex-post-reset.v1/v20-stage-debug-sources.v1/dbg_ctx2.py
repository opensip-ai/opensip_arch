import importlib.util, pathlib, sys, hashlib, copy, json
FOUND=pathlib.Path("/tmp/opensip-design-corrections/candidate-subject.v19/docs/coop/design-corrections/foundation")
sys.path.insert(0,str(FOUND))
spec=importlib.util.spec_from_file_location("ci",FOUND/"check-identity.py");ci=importlib.util.module_from_spec(spec)
try: spec.loader.exec_module(ci)
except SystemExit: pass
M,C=ci.M,ci.C
exec(open("/private/tmp/opensip-design-corrections/v20-stage-membership-assessment.v1/_remint.py").read())
r0,o0,b0=ci.build()
# SUBSET direction: drop one retained+reached context from the Plan
r,o,b=remint_plan(M,C,r0,o0,b0,lambda p:p.update(nativeContextDigests=p["nativeContextDigests"][:-1]))
try: print("CTX-SUBSET -> ACCEPT",M.close_run(r,o,b))
except Exception as e: print("CTX-SUBSET -> REFUSE %s:%s"%(type(e).__name__,e))
# and the closure subset direction for an UNUSED-but-selected closure removed: n/a (none unused)
