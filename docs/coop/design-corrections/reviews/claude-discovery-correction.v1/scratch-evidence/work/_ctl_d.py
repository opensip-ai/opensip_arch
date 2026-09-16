def custody_case(total, bad_dir, bad_marker):
    ctx=K._synthetic_repo(total,0); RR=ctx["cwd"]
    names=sorted(k for k in ctx["fs"] if k.startswith(RR+"/pkg") and k.endswith("/package.json"))
    for i in range(bad_dir): ctx["fs"][names[i].rsplit("/",1)[0]]["mode"]="0757"
    for i in range(bad_dir,bad_dir+bad_marker): ctx["fs"][names[i]]["nlink"]=2
    sec=S.discovery(ctx)
    if not (sec["status"]=="ACCEPT"): return sec, None, None
    iv=S.boundary_inventory(sec)
    mkx={k[len(RR)+1:]:{"sha256":"a"*64} for k,e in ctx["fs"].items() if k.startswith(RR+"/") and e["kind"]=="file" and k.rpartition("/")[2] in DD.WORKSPACE_MARKERS}
    return sec, iv, N.discover_units(mkx, None, iv)
s1,i1,n1=custody_case(4200,150,0)
ok10a = s1["status"]=="ACCEPT" and len(s1["provenance"]["units"])==4051 and n1["refused"] is None and len(n1["units"])==4051
rec("C10a 4200 first-party with 150 directory-custody failures still admits 4051 in BOTH instruments", 4051, {"security":len(s1["provenance"]["units"]),"native":len(n1["units"]) if n1 else None}, ok10a, "preserves the corrected cap/custody behaviour verified in review pass 2")
s2,i2,n2=custody_case(4200,0,150)
ok10b = s2["status"]=="ACCEPT" and len(s2["provenance"]["units"])==4051 and n2["refused"] is None and len(n2["units"])==4051
rec("C10b same for 150 marker-custody failures", 4051, {"security":len(s2["provenance"]["units"]),"native":len(n2["units"]) if n2 else None}, ok10b)
s3,_,_=custody_case(4096,0,0)
ok10c = s3["status"]=="REFUSE" and s3["detail"]=="WORKSPACE_UNIT_LIMIT:4097>4096"
rec("C10c 4096 pkg dirs plus the root is 4097 selected directories and refuses", "WORKSPACE_UNIT_LIMIT:4097>4096", s3.get("detail"), ok10c)
s4,i4,n4=custody_case(4095,0,0)
ok10d = s4["status"]=="ACCEPT" and len(s4["provenance"]["units"])==4096 and n4["refused"] is None and len(n4["units"])==4096
rec("C10d exactly 4096 selected directories admit in both instruments", 4096, {"security":len(s4["provenance"]["units"]),"native":len(n4["units"]) if n4 else None}, ok10d)
