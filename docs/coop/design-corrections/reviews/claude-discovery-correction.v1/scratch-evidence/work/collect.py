"""Collect the XA-01 + XA-02/CR-25 correction deliverables against frozen candidate25."""
import difflib, hashlib, json, os, shutil, sys
SRC=sys.argv[1]; DST=sys.argv[2]; OUT=sys.argv[3]
os.makedirs(OUT+"/changed-files", exist_ok=True); os.makedirs(OUT+"/patches", exist_ok=True)
rows=[]
for root, dirs, files in os.walk(DST):
    if "/.git" in root: continue
    for f in files:
        p=os.path.join(root,f); rel=os.path.relpath(p, DST)
        o=os.path.join(SRC, rel)
        if not os.path.exists(o): continue
        ob=open(o,"rb").read(); nb=open(p,"rb").read()
        if ob==nb: continue
        oh=hashlib.sha256(ob).hexdigest(); nh=hashlib.sha256(nb).hexdigest()
        tgt=OUT+"/changed-files/"+rel
        os.makedirs(os.path.dirname(tgt), exist_ok=True); shutil.copyfile(p, tgt)
        try:
            patch="".join(difflib.unified_diff(ob.decode().splitlines(True), nb.decode().splitlines(True), fromfile="a/"+rel, tofile="b/"+rel))
        except UnicodeDecodeError:
            patch=""
        pn=OUT+"/patches/"+rel.replace(os.sep,"__")+".patch"
        open(pn,"w").write(patch)
        rows.append({"path":rel,"beforeSha256":oh,"afterSha256":nh,"beforeBytes":len(ob),"afterBytes":len(nb),"patchLines":patch.count(chr(10))})
rows.sort(key=lambda r: r["path"])
json.dump({"standing":"CLAUDE AUTHORED XA-01 + XA-02/CR-25 correction against frozen candidate25; NOT accepted; fresh independent review required before integration","candidateManifestSha256":"fa8cdc796c4dbab514c8b8a91a593b740e3f8e69d19574f4be11c6e00c3a536d","files":rows}, open(OUT+"/changed-source.json","w"), indent=2)
for r in rows: print("%-72s %s to %s  +%d lines" % (r["path"], r["beforeSha256"][:10], r["afterSha256"][:10], r["patchLines"]))
print("changed files:", len(rows))
