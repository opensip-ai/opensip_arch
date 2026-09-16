cnt=copy.deepcopy(inv)
for t in cnt["prunedTrees"]:
    t["markerCount"]=None; t["markerCountBasis"]="not-enumerated"
nc=N.discover_units(markers_of(fsx), None, cnt)
rec("C5a count and basis are not equality keys", "no refusal", (nc["refused"] or {}).get("detail"), nc["refused"] is None)
sb=N.unit_scope_descriptor(nd["units"], [], None, nd["prunedTrees"], inv)
sc=N.unit_scope_descriptor(nc["units"], [], None, nc["prunedTrees"], cnt)
ok5b = sb["scopeDescriptor"]==sc["scopeDescriptor"] and sb["scopeDigest"]==sc["scopeDigest"]
rec("C5b count or basis change leaves scopeDescriptor and scopeDigest bit-identical", sb["scopeDigest"], sc["scopeDigest"], ok5b, "only the path member reaches excludedPathPrefixes")
ub=sorted(u["rootPath"] for u in nd["units"]); uc=sorted(u["rootPath"] for u in nc["units"])
rec("C11a count or basis change leaves the selected unit set identical", ub, uc, ub==uc)
ob=hashlib.sha256(C.canonical(inv)).hexdigest(); oc=hashlib.sha256(C.canonical(cnt)).hexdigest()
rec("C5c count or basis change DOES change the operational provenance digest", "differs", {"base":ob[:16],"changed":oc[:16]}, not (ob==oc), "exact bytes changed; a truthful provenance change, not a semantic one")
fl=list(sb["scopeDescriptor"]["excludedPathPrefixes"])
rec("C11b a directory-only anchor DOES reach excludedPathPrefixes", "vendorish/.hg present", fl, "vendorish/.hg" in fl, "disclosed identity consequence of CR-25; the segment rule already pruned the tree so the analysed byte set is unchanged")
