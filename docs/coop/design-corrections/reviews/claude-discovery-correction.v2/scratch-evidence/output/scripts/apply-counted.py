import json,hashlib,difflib,os,sys
COPY=sys.argv[1]; STAGE=sys.argv[2]; OUT=sys.argv[3]; os.makedirs(OUT,exist_ok=True)
spec=json.load(open(STAGE)); rows=[]
for rel,reps in spec.items():
    p=os.path.join(COPY,rel); original=open(p).read(); upd=original
    for item in reps:
        before,after=item[0],item[1]
        want=item[2] if len(item)>2 else 1
        got=upd.count(before)
        if got!=want: raise SystemExit("COUNT %s want=%d got=%d :: %r"%(rel,want,got,before[:70]))
        upd=upd.replace(before,after)
    open(p,"w").write(upd)
    patch="".join(difflib.unified_diff(original.splitlines(True),upd.splitlines(True),fromfile=rel,tofile=rel))
    open(os.path.join(OUT,os.path.basename(rel)+".patch"),"w").write(patch)
    rows.append({"path":rel,"beforeSha256":hashlib.sha256(original.encode()).hexdigest(),"afterSha256":hashlib.sha256(upd.encode()).hexdigest(),"replacements":len(reps)})
    print("OK %-68s %s to %s"%(rel,rows[-1]["beforeSha256"][:12],rows[-1]["afterSha256"][:12]))
json.dump({"standing":"CLAUDE v2 version-guard stage","files":rows},open(os.path.join(OUT,"changed-source.json"),"w"),indent=2)
