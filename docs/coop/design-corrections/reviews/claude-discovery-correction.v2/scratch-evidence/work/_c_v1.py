v1prov=copy.deepcopy(ox["provenance"]); v1prov["schemaVersion"]=1
v1provEmpty=copy.deepcopy(v1prov); v1provEmpty["prunedTrees"]=[]
def attempt(fn):
    try: return ("accepted", fn())
    except Exception as e: return ("refused", type(e).__name__+":"+str(e)[:110])
o,d=attempt(lambda: S.validate_discovery_provenance(v1provEmpty) and "valid")
rec("V1 read: V1 provenance with NO pruned rows stays readable", "accepted", d, o=="accepted", "historical read support is preserved")
o,d=attempt(lambda: S.validate_discovery_provenance(v1prov) and "valid")
rec("V2 read: V1 provenance WITH legacy pruned rows stays readable", "accepted", d, o=="accepted")
o,d=attempt(lambda: DD.boundary_inventory_from_provenance(v1provEmpty)["schemaVersion"])
rec("V3 convert: V1 provenance with no pruned rows is refused, never relabelled V2", "PROVENANCE_VERSION_UNSUPPORTED:1", d, o=="refused" and "PROVENANCE_VERSION_UNSUPPORTED:1" in d, "root probe 1")
o,d=attempt(lambda: DD.boundary_inventory_from_provenance(v1prov)["schemaVersion"])
rec("V4 convert: V1 provenance with pruned rows is refused", "PROVENANCE_VERSION_UNSUPPORTED:1", d, o=="refused" and "PROVENANCE_VERSION_UNSUPPORTED:1" in d)
o,d=attempt(lambda: DD.boundary_inventory_from_provenance(ox["provenance"])["schemaVersion"])
rec("V5 convert: current V2 provenance still converts to a V2 inventory", 2, d, o=="accepted" and d==2)
o,d=attempt(lambda: S.boundary_inventory(dict(ox, provenance=v1prov)))
rec("V6 convert: the security wrapper maps it onto the existing BOUNDARY_INVENTORY Reject", "Reject BOUNDARY_INVENTORY:PROVENANCE_VERSION_UNSUPPORTED:1", d, o=="refused" and "BOUNDARY_INVENTORY:PROVENANCE_VERSION_UNSUPPORTED:1" in d, "no new public code")
