#!/usr/bin/env python3
"""P07: is the cross-language universe/context binding actually enforced?
Tested three ways: (a) the native binding API directly, (b) the identity
model's frame parser via the domain-set registry, (c) a complete re-minted Run
whose Rust universe names the TypeScript context."""
import contextlib, copy, hashlib, importlib.util, io, json, sys
from pathlib import Path
SUBJ=Path("/tmp/opensip-design-corrections/candidate-subject.v8")
F=SUBJ/"docs/coop/design-corrections/foundation"; NATD=SUBJ/"docs/coop/design-corrections/native"
def load(n,p,iso=False):
    s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s)
    if not iso: s.loader.exec_module(m); return m
    a,b=sys.argv,io.StringIO(); sys.argv=[str(p)]
    try:
        with contextlib.redirect_stdout(b):
            try: s.loader.exec_module(m)
            except SystemExit: pass
    finally: sys.argv=a
    return m
M=load("idmodel",F/"identity-model.py"); C=M.C
N=load("nat",NATD/"native_evidence_model.v2.py")
CHK=load("idcheck",F/"check-identity.py",True)
R={"checks":[]}
def rec(n,ok,d=None): R["checks"].append({"id":n,"passed":bool(ok),"detail":d})

run,objects,blobs=CHK.build(has_match=True,universe_language="rust")
M.close_run(run,objects,blobs)
plan=objects[run['planId']][1]
ctx={}
for d in plan['nativeContextDigests']:
    dom,val,_=M.parse_h_frame(blobs[d],'native-context'); ctx[dom]=(d,val)
ts_d,ts_ctx=ctx['native.context.typescript.v2']; ru_d,ru_ctx=ctx['native.context.rust.v2']
runiv=tsuniv=None
for d,raw in list(blobs.items()):
    try: dom,val,_=M.parse_h_frame(raw,'native-semantic-universe')
    except Exception: continue
    if dom=='native.semantic-universe.rust.v2': runiv=val
    if dom=='native.semantic-universe.typescript.v2': tsuniv=val

# (a) direct binding API: a Rust universe pointed at the TypeScript context
ts_adm=N.admit_native_context('typescript',ts_ctx,{})
bad=dict(runiv, nativeContextId='sha256:'+ts_d)
try:
    res=N.bind_rust_universe(bad, ts_adm, ts_ctx, None, None)
    rec("XL-1-bind_rust_universe-against-a-typescript-admission",
        res['result']=='REFUSE', {"result":res['result'],"refusals":res['refusals'][:6]})
except Exception as e:
    rec("XL-1-bind_rust_universe-against-a-typescript-admission", True, {"raised":str(e)[:250]})

# and the mirror: a TypeScript universe against a Rust admission
ru_adm=N.admit_native_context('rust',ru_ctx,{})
bad_ts=dict(tsuniv or {}, nativeContextId='sha256:'+ru_d) if tsuniv else None
if bad_ts:
    try:
        res=N.bind_typescript_universe(bad_ts, ru_adm, ru_ctx, None, None)
        rec("XL-2-bind_typescript_universe-against-a-rust-admission",
            res['result']=='REFUSE', {"result":res['result'],"refusals":res['refusals'][:6]})
    except Exception as e:
        rec("XL-2-bind_typescript_universe-against-a-rust-admission", True, {"raised":str(e)[:250]})

# (b) the identity registry: which record does each universe domain register?
ids=json.loads((F/"identity-schemas.v2.json").read_bytes())
dsets=ids['x-opensip-digest-domains']['domainSets']
R["universeDomainSetRows"]=dsets.get('native-semantic-universe')
R["contextDomainSetRows"]=dsets.get('native-context')

# a frame of the rust universe domain carrying TypeScript universe BYTES
if tsuniv:
    frame=M.h_preimage_frame('native.semantic-universe.rust.v2', tsuniv)
    try:
        M.parse_h_frame(frame,'native-semantic-universe')
        rec("XL-3-ts-universe-bytes-under-the-rust-universe-domain", False, {"got":"parsed"})
    except Exception as e:
        rec("XL-3-ts-universe-bytes-under-the-rust-universe-domain", True, {"got":str(e)[:250]})

# (c) complete Run: re-mint the RUST universe to name the TS context, re-frame,
#     and repoint every reference so the Run is self-consistent.
def complete_cross():
    r,o,b=CHK.build(has_match=True,universe_language="rust")
    plan=o[r['planId']][1]
    tsd=None
    for d in plan['nativeContextDigests']:
        dom,_,_=M.parse_h_frame(b[d],'native-context')
        if dom=='native.context.typescript.v2': tsd=d
    # locate the retained rust universe frame and its digest
    old=None; oldval=None
    for d,raw in list(b.items()):
        try: dom,val,_=M.parse_h_frame(raw,'native-semantic-universe')
        except Exception: continue
        if dom=='native.semantic-universe.rust.v2': old,oldval=d,val
    new=dict(oldval, nativeContextId='sha256:'+tsd)
    newd=M.native_universe_frame('native.semantic-universe.rust.v2',new,b)
    # repoint every object that named the old universe
    def repoint(x):
        if isinstance(x,str): return newd if x==old else x
        if isinstance(x,list): return [repoint(y) for y in x]
        if isinstance(x,dict): return {k:repoint(v) for k,v in x.items()}
        return x
    while True:
        moved=next(((k,repoint(v)) for k,(d,v) in o.items() if repoint(v)!=v),None)
        if moved is None: break
        CHK.rekey(o,moved[0],moved[1],r)
    CHK.resync_coverage(o,b,r); CHK.resync_witness(o,b,r); CHK.resync_proof_refs(o,b,r)
    M.close_run(r,o,b)
try:
    complete_cross()
    rec("XL-4-complete-Run-with-rust-universe-on-ts-context", False, {"got":"ADMITTED"})
except Exception as e:
    rec("XL-4-complete-Run-with-rust-universe-on-ts-context", True, {"got":str(e)[:300]})

R["summary"]={"total":len(R["checks"]),"passed":sum(c["passed"] for c in R["checks"]),
              "failed":[c for c in R["checks"] if not c["passed"]]}
json.dump(R,sys.stdout,indent=1,default=str); print()
