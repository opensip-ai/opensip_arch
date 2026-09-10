import importlib.util, pathlib, sys, itertools
FOUND=pathlib.Path("/tmp/opensip-design-corrections/candidate-subject.v19/docs/coop/design-corrections/foundation")
sys.path.insert(0,str(FOUND))
spec=importlib.util.spec_from_file_location("ci",FOUND/"check-identity.py");ci=importlib.util.module_from_spec(spec)
try: spec.loader.exec_module(ci)
except SystemExit: pass
M,C=ci.M,ci.C
exec(open("/private/tmp/opensip-design-corrections/v20-stage-membership-assessment.v1/_remint.py").read())
r0,o0,b0=ci.build();p0=o0[r0["planId"]][1]
ctx=list(p0["nativeContextDigests"])
print("plan declares",len(ctx),"contexts")
for i,d in enumerate(ctx):
    keep=[x for x in ctx if x!=d]
    r,o,b=remint_plan(M,C,r0,o0,b0,lambda p,k=keep:p.update(nativeContextDigests=k))
    try: M.close_run(r,o,b);print("  drop %s -> ACCEPT (context was NOT load-bearing)"%d[:12])
    except Exception as e: print("  drop %s -> REFUSE %s"%(d[:12],str(e)[:60]))
# minimal set
for n in range(0,4):
    for keep in itertools.combinations(ctx,n):
        r,o,b=remint_plan(M,C,r0,o0,b0,lambda p,k=list(keep):p.update(nativeContextDigests=k))
        try:
            M.close_run(r,o,b);print("MINIMAL closing context set size %d: %s"%(n,[x[:12] for x in keep]));raise SystemExit
        except SystemExit: raise
        except Exception: pass
