import json
import sys

sys.path.insert(0, "/tmp/opensip-design-corrections/consumer-b.v8/output/work")
import closure as CL
import run_ts

fx, A, run_id = run_ts.build_run()
c = CL.Closure(fx.s)
rep = c.close_run(run_id)
print("RUN", run_id)
print("checks", rep["checks"], "ok", rep["ok"])
for f in rep["faults"][:40]:
    print("  FAULT", f["code"], f["detail"][:160])
print()
print("ts bodyIdentity ", A.extra["tsBodyIdentity"])
print("js bodyIdentity ", A.extra["jsBodyIdentity"])
print("l1 bodyIdentity ", A.extra["l1BodyIdentity"])
print("blv ts", json.dumps(A.extra["tsBodyLanguageVersion"], sort_keys=True))
print("blv js", json.dumps(A.extra["jsBodyLanguageVersion"], sort_keys=True))
