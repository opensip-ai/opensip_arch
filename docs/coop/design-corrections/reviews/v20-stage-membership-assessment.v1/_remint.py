import hashlib, copy
def remint_plan(M,C,run,objects,blobs,mutate_plan):
    objects=dict(objects);blobs=dict(blobs)
    def put_blob(v):
        raw=C.canonical(v);d=hashlib.sha256(raw).hexdigest();blobs[d]=raw;return d
    def add(dom,v):
        k=M.identifier(dom,v);objects[k]=(dom,v);return k
    plan=copy.deepcopy(objects[run["planId"]][1]);mutate_plan(plan);npid=add("plan",plan)
    seal=copy.deepcopy(objects[run["evaluationSealId"]][1])
    evidence=copy.deepcopy(objects[seal["evidenceId"]][1])
    proof=copy.deepcopy(objects[seal["proofBundleId"]][1])
    ep=copy.deepcopy(objects[seal["executionPlanId"]][1])
    ovid=evidence["viewIds"][0];view=copy.deepcopy(objects[ovid][1]);view["planId"]=npid
    nvid=add("view",view);od,nd=ovid.split(":",1)[1],nvid.split(":",1)[1]
    s=C.parse(blobs[ep["stages"][0]["stageSpecDigest"]]);s["planId"]=npid
    ep["stages"][0]["stageSpecDigest"]=put_blob(s);ep["planId"]=npid;nep=add("execution-plan",ep)
    def rt(refs):
        for r in refs:
            if r.get("domain")=="view" and r["digest"]==od: r["digest"]=nd
    proof["planId"]=npid;proof["executionPlanId"]=nep;rt(proof["evaluationInputRefs"])
    for p in proof["predicateProofs"]: rt(p["inputRefs"])
    nproof=add("proof-bundle",proof)
    evidence["planId"]=npid;evidence["viewIds"]=[nvid];evidence["proofBundleId"]=nproof
    nev=add("semantic-evidence",evidence)
    seal["planId"]=npid;seal["executionPlanId"]=nep;seal["proofBundleId"]=nproof;seal["evidenceId"]=nev
    nseal=add("evaluation-seal",seal)
    run=dict(run);run["planId"]=npid;run["evidenceId"]=nev;run["evaluationSealId"]=nseal
    return run,objects,blobs
