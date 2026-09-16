miss=copy.deepcopy(inv)
miss["prunedTrees"]=[t for t in miss["prunedTrees"] if not (t["path"]=="packages/web/node_modules")]
nm=N.discover_units(markers_of(fsx), None, miss)
d7=(nm["refused"] or {}).get("detail")
rec("C7 missing marker-implied anchor still refuses", "native.boundary-inventory-mismatch", d7, d7=="native.boundary-inventory-mismatch")
wrong=copy.deepcopy(inv)
for t in wrong["prunedTrees"]:
    if t["path"]=="packages/web/node_modules": t["reason"]="vcs-tree"
nw=N.discover_units(markers_of(fsx), None, wrong)
d8=(nw["refused"] or {}).get("detail")
rec("C8 mismatched reason refuses", "native.boundary-inventory-mismatch", d8, d8=="native.boundary-inventory-mismatch")
