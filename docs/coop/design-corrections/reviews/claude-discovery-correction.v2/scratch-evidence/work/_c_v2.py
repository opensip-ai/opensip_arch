v1inv=copy.deepcopy(inv); v1inv["schemaVersion"]=1
v1inv["prunedTrees"]=[{"path":t["path"],"reason":t["reason"],"markerCount":t["markerCount"]} for t in inv["prunedTrees"] if t["markerCount"] is not None]
v1invEmpty=copy.deepcopy(v1inv); v1invEmpty["prunedTrees"]=[]
o,d=attempt(lambda: N.validate_boundary_inventory(v1invEmpty) and "valid")
rec("V7 read: V1 boundary inventory with no pruned rows stays readable", "accepted", d, o=="accepted")
o,d=attempt(lambda: N.validate_boundary_inventory(v1inv) and "valid")
rec("V8 read: V1 boundary inventory with legacy pruned rows stays readable", "accepted", d, o=="accepted", "root probe 2 input; the READ lane is unchanged")
EXP="native.boundary-inventory-version-unsupported:1"
for nm,fn in [("discover_units", lambda b: N.discover_units(markers_of(fsx), None, b)),
              ("assign_membership", lambda b: N.assign_membership(nd["units"], files_of(fsx), b)),
              ("unit_scope_descriptor", lambda b: N.unit_scope_descriptor(nd["units"], [], None, b["prunedTrees"], b)),
              ("require_admitted_boundaries", lambda b: N.require_admitted_boundaries(b)),
              ("admit_current_boundary_inventory", lambda b: N.admit_current_boundary_inventory(b))]:
    o,d=attempt((lambda g: (lambda: g(v1inv)))(fn))
    rec("V9 current: "+nm+" refuses a V1 inventory at its own boundary", EXP, d, o=="refused" and EXP in d, "labelled input refusal, not an incidental UnitDiscoveryV2 output shape error")
    o,d=attempt((lambda g: (lambda: g(v1invEmpty)))(fn))
    rec("V10 current: "+nm+" refuses an EMPTY V1 inventory too", EXP, d, o=="refused" and EXP in d, "emptiness is not a version")
o,d=attempt(lambda: N.admit_current_boundary_inventory(inv)["schemaVersion"])
rec("V11 current: a V2 inventory is admitted unchanged", 2, d, o=="accepted" and d==2)
rec("V12 label: NativeRefusal is a shared AdmissionError so existing handlers catch it", True, issubclass(N.NativeRefusal, N.AdmissionError), issubclass(N.NativeRefusal, N.AdmissionError), "v1 subclassed ValueError and escaped every admitted-input except site")
