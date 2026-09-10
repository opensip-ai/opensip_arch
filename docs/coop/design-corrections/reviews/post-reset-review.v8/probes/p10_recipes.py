#!/usr/bin/env python3
"""P10: the two closed workflow recipes, attacked for their precise operational scope.
  R1 policy-test-suite H identity vs raw policy digests
  R2 generic mutation idempotency H over MutationReplayScopeV1
Question: can either dedup across requests, permit caller-chosen receipt lookup,
accept mutable effect inputs, or confer authority?
"""
import contextlib,copy,hashlib,importlib.util,io,json,sys
from pathlib import Path
SUBJ=Path("/tmp/opensip-design-corrections/candidate-subject.v8"); DC=SUBJ/"docs/coop/design-corrections"
def load(n,p):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
W=load("wf",DC/"workflows/workflows_model.v1.py"); CN=W.canonical
R={"checks":[],"observations":{}}
def rec(n,ok,d=None): R["checks"].append({"id":n,"passed":bool(ok),"detail":d})
def refuses(n,fn,token=""):
    try: fn()
    except Exception as e: rec(n, token in str(e), {"expect":token,"got":str(e)[:250]})
    else: rec(n, False, {"got":"ADMITTED"})

RID="req1_"+"a"*32; RID2="req1_"+"b"*32; PID="prj1-"+"c"*64

# ---- R2 mutation replay scope -------------------------------------------
s1=W.mutation_replay_scope(RID,0,PID,"core-update")
k1=W.mutation_replay_key(s1)
R["observations"]["scope"]=s1; R["observations"]["key"]=k1
rec("R2-01-key-is-an-H-identity-not-a-raw-sha",
    k1 != hashlib.sha256(CN.canonical(s1)).hexdigest(),
    {"H":k1,"rawSha":hashlib.sha256(CN.canonical(s1)).hexdigest()})
# independent H reconstruction over the declared domain
c=CN.canonical(s1)
mine=hashlib.sha256(b"opensip.product.v1\x00workflow.mutation-intent\x00"+len(c).to_bytes(8,"big")+c).hexdigest()
rec("R2-02-H-domain-and-preimage-reproduced-independently", mine==k1.split(":")[-1],
    {"mine":mine,"model":k1})

# a DIFFERENT request must not dedup to the same key
k2=W.mutation_replay_key(W.mutation_replay_scope(RID2,0,PID,"core-update"))
rec("R2-03-different-request-does-not-dedup", k1!=k2, {"k1":k1,"k2":k2})
k3=W.mutation_replay_key(W.mutation_replay_scope(RID,1,PID,"core-update"))
rec("R2-04-different-step-does-not-dedup", k1!=k3)
k4=W.mutation_replay_key(W.mutation_replay_scope(RID,0,"prj1-"+"d"*64,"core-update"))
rec("R2-05-different-project-does-not-dedup", k1!=k4)
k5=W.mutation_replay_key(W.mutation_replay_scope(RID,0,PID,"core-rollback"))
rec("R2-06-different-operation-does-not-dedup", k1!=k5)
# the SAME request/step/project/operation IS idempotent
rec("R2-07-same-scope-is-idempotent", k1==W.mutation_replay_key(W.mutation_replay_scope(RID,0,PID,"core-update")))

# the scope is closed: no mutable effect input may enter
refuses("R2-08-extra-effect-input-refused",
        lambda: W.mutation_replay_key(dict(s1, payloadDigest="e"*64)))
refuses("R2-09-caller-invented-scope-field-refused",
        lambda: W.mutation_replay_key(dict(s1, receiptId="whatever")))

# the admission join: a caller cannot present a key for a different operation
refuses("R2-10-mutationClass-must-equal-scope-operation",
        lambda: W.admit_mutation_replay_key({'kind':'mutation','mutationClass':'core-rollback','idempotencyKey':k1.split(':')[-1],'inputDescriptorDigest':'a'*64}, s1),
        "MUTATION_REPLAY_SCOPE_JOIN")
refuses("R2-11-caller-chosen-idempotency-key-refused",
        lambda: W.admit_mutation_replay_key({'kind':'mutation','mutationClass':'core-update','idempotencyKey':'f'*64,'inputDescriptorDigest':'a'*64}, s1),
        "MUTATION_REPLAY_SCOPE_JOIN")
try:
    W.admit_mutation_replay_key({'kind':'mutation','mutationClass':'core-update','idempotencyKey':k1.split(':')[-1],'inputDescriptorDigest':'a'*64}, s1)
    rec("R2-12-legitimate-join-admits", True)
except Exception as e:
    rec("R2-12-legitimate-join-admits", False, {"got":str(e)[:250]})
# a key derived from ANOTHER request cannot be presented against this scope
refuses("R2-13-cross-request-receipt-lookup-refused",
        lambda: W.admit_mutation_replay_key({'kind':'mutation','mutationClass':'core-update','idempotencyKey':k2.split(':')[-1],'inputDescriptorDigest':'a'*64}, s1),
        "MUTATION_REPLAY_SCOPE_JOIN")

# the pure helper is not a ledger or an authorization
src=(DC/"workflows/workflows_model.v1.py").read_text()
seg=src[src.index("def mutation_replay_scope"):src.index("# ----------------------------------------------------------------------------- evidence retention")]
R["observations"]["mutationSegment"]=seg
for tok in ("open(","write","commit","ledger.","authorize","grant","execute","subprocess"):
    rec("R2-14-no-"+tok.strip("(.")+"-in-the-pure-helper", tok not in seg, {"token":tok})

# the generic scope must REFUSE repair-apply, preserving its separate recipe
refuses("R2-15-repair-apply-excluded-from-the-generic-scope",
        lambda: W.mutation_replay_scope(RID,0,PID,"repair-apply"))
refuses("R2-16-repair-apply-excluded-from-MutationParams",
        lambda: W.admit_mutation_replay_key({'kind':'mutation','mutationClass':'repair-apply','idempotencyKey':'a'*64}, s1))

# ---- R1 policy test suite ------------------------------------------------
suite={'schemaFamily':'opensip.product.policy-test-suite','schemaMajor':1,'cases':[]}
try:
    d1=CN.identity('workflow.policy-test-suite', suite)
    R["observations"]["suiteDigest"]=d1
    c=CN.canonical(suite)
    mine=hashlib.sha256(b"opensip.product.v1\x00workflow.policy-test-suite\x00"+len(c).to_bytes(8,"big")+c).hexdigest()
    rec("R1-01-suite-identity-is-H-over-its-own-domain", mine==d1.split(":")[-1], {"mine":mine,"model":d1})
    rec("R1-02-suite-digest-is-not-a-raw-policy-digest",
        d1.split(":")[-1] != hashlib.sha256(CN.canonical(suite)).hexdigest())
    # a policy document hashed raw must never equal the suite H identity
    policy={'schemaFamily':'opensip.product.policy','schemaMajor':1,'gateSeverityAtLeast':'error','rules':[]}
    rec("R1-03-policy-raw-digest-distinct-from-suite-H",
        hashlib.sha256(CN.canonical(policy)).hexdigest() != d1.split(":")[-1])
    # the same bytes under a different domain give a different identity
    rec("R1-04-domain-separation-holds",
        CN.identity('workflow.policy-test-result', suite) != d1)
except Exception as e:
    rec("R1-00-suite-identity-available", False, {"got":str(e)[:250]})

# repair-apply keeps its SEPARATE content-derived recipe
R["observations"]["repairApplyRecipeMentions"]=[l.strip() for l in src.splitlines()
    if "repair" in l.lower() and ("digest" in l.lower() or "idempot" in l.lower())][:12]

R["summary"]={"total":len(R["checks"]),"passed":sum(c["passed"] for c in R["checks"]),
              "failed":[c for c in R["checks"] if not c["passed"]]}
json.dump(R,sys.stdout,indent=1,default=str); print()
