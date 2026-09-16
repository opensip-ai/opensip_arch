fs,d,f=base_fs()
fs[R+"/node_modules"]=d(); fs[R+"/node_modules/pkg"]=d()
o=disc(fs); pr=anchors(o["provenance"])
rec("C1 no-marker node_modules anchor is reported", [(R+"/node_modules","dependency-tree",0,"observed-inventory")], pr, pr==[(R+"/node_modules","dependency-tree",0,"observed-inventory")], "CR-25: version 1 reported nothing here")
fs2,d2,f2=base_fs()
fs2[R+"/node_modules"]=d2(); fs2[R+"/node_modules/pkg"]=d2(); fs2[R+"/node_modules/pkg/index.js"]=f2()
o2=disc(fs2); pr2=anchors(o2["provenance"])
rec("C2 pruned tree with only non-marker files", [(R+"/node_modules","dependency-tree",0,"observed-inventory")], pr2, pr2==[(R+"/node_modules","dependency-tree",0,"observed-inventory")])
fs3,d3,f3=base_fs()
fs3[R+"/node_modules"]=dict(d3(), aclUnreadable=True); fs3[R+"/node_modules/p/package.json"]=f3()
o3=disc(fs3); pr3=anchors(o3["provenance"])
rec("C3 unreadable pruned directory keeps the anchor and nulls the count", [(R+"/node_modules","dependency-tree",None,"not-enumerated")], pr3, pr3==[(R+"/node_modules","dependency-tree",None,"not-enumerated")], "per-row basis; a global basis could not express this")
z=disc(base_fs()[0]); rec("C4a zero supplied marker observations beyond the root", [], anchors(z["provenance"]), anchors(z["provenance"])==[] and z["status"]=="ACCEPT")
big=K._synthetic_repo(0,4200); ob=disc(big["fs"])
exp=[("/home/alice/big/node_modules","dependency-tree",4200,"observed-inventory")]
rec("C4b 4200 supplied installed markers stay one anchor with an exact supplied count", exp, anchors(ob["provenance"]), anchors(ob["provenance"])==exp and len(ob["provenance"]["units"])==1)
ne=disc(fs2, prunedTreeMarkerInventory="not-enumerated")
exp=[(R+"/node_modules","dependency-tree",None,"not-enumerated")]
rec("C4c declared not-enumerated inventory yields a null count, never zero", exp, anchors(ne["provenance"]), anchors(ne["provenance"])==exp, "zero observed is not zero hidden")
try:
    S.discovery({"invokingUid":1000,"accountHome":"/home/alice","cwd":R,"fs":fs2,"prunedTreeMarkerInventory":"guessed"}); bad="ACCEPTED"
except Exception as e: bad=type(e).__name__+":"+str(e)
rec("C4d unknown basis declaration is an instrument shape error", "Reject:DISCOVERY_OBSERVATION_SHAPE", bad, "DISCOVERY_OBSERVATION_SHAPE" in bad)
