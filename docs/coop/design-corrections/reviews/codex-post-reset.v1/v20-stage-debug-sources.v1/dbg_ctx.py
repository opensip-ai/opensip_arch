import importlib.util, pathlib, sys, hashlib, json, copy
FOUND=pathlib.Path("/tmp/opensip-design-corrections/candidate-subject.v19/docs/coop/design-corrections/foundation")
sys.path.insert(0,str(FOUND))
spec=importlib.util.spec_from_file_location("ci",FOUND/"check-identity.py");ci=importlib.util.module_from_spec(spec)
try: spec.loader.exec_module(ci)
except SystemExit: pass
M,C=ci.M,ci.C
r0,o0,b0=ci.build(); p0=o0[r0["planId"]][1]
rr,orr,brr=ci.build(universe_language="rust"); pr=orr[rr["planId"]][1]
print("ts contexts:",p0["nativeContextDigests"])
print("rs contexts:",pr["nativeContextDigests"])
print("diff:",[d for d in pr["nativeContextDigests"] if d not in p0["nativeContextDigests"]])
