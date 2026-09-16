for bad,label in [(7,"unknown-int"),(True,"bool"),("2","string"),(None,"null"),(2.0,"float")]:
    p=copy.deepcopy(ox["provenance"]); p["schemaVersion"]=bad
    b=copy.deepcopy(inv); b["schemaVersion"]=bad
    o1,d1=attempt((lambda pp: (lambda: S.validate_discovery_provenance(pp) and "valid"))(p))
    o2,d2=attempt((lambda pp: (lambda: DD.boundary_inventory_from_provenance(pp)["schemaVersion"]))(p))
    o3,d3=attempt((lambda bb: (lambda: N.validate_boundary_inventory(bb) and "valid"))(b))
    o4,d4=attempt((lambda bb: (lambda: N.admit_current_boundary_inventory(bb)["schemaVersion"]))(b))
    want="UNKNOWN" if label=="unknown-int" else "SHAPE"
    ok = o1=="refused" and o2=="refused" and o3=="refused" and o4=="refused"
    ok = ok and (want.lower() in d2.lower()) and (want.lower() in d1.lower())
    rec("V13 all four version paths refuse schemaVersion "+label, "refused on read, convert and current admission", {"provRead":d1,"convert":d2,"invRead":d3,"currentAdmit":d4}, ok)
