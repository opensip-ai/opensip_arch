try:
    N.require_admitted_boundaries(None); hb="ACCEPTED"
except Exception as e: hb=type(e).__name__+":"+str(e)
rec("C12a authoritative lane refuses a missing admitted inventory", "NativeRefusal:native.admitted-boundaries-required", hb, "admitted-boundaries-required" in hb)
alone=N.discover_units(markers_of(fsx), None, None)
rec("C12b standalone/algorithm lane still accepts no inventory", "no refusal", (alone["refused"] or {}).get("detail"), alone["refused"] is None and alone["boundaries"]["source"]=="none")
try:
    N.validate_boundary_inventory(dict(inv, schemaVersion=7)); vb="ACCEPTED"
except Exception as e: vb=type(e).__name__+":"+str(e)
rec("C12c unknown inventory version refuses rather than falling back to V1", "native.boundary-inventory-version-unknown:7", vb, "version-unknown:7" in vb)
try:
    S.validate_discovery_provenance(dict(ox["provenance"], schemaVersion=9)); pv="ACCEPTED"
except Exception as e: pv=type(e).__name__+":"+str(e)
rec("C12d unknown provenance version refuses", "DISCOVERY_PROVENANCE_VERSION_UNKNOWN:9", pv, "DISCOVERY_PROVENANCE_VERSION_UNKNOWN:9" in pv)
S.validate_input("DiscoveryProvenanceV2", ox["provenance"]); N.validate_native("AdmittedBoundaryInventoryV2", inv); N.validate_native("UnitDiscoveryV2", nd)
rec("C12e version-2 records validate under their own named definitions", "valid", "valid", True, "a changed record is never named V1")
hostres=H.admit_repository_discovery({"invokingUid":1000,"accountHome":"/home/alice","cwd":R,"fs":fsx}, markers_of(fsx), files_of(fsx))
okh = hostres["native"]["refused"] is None and hostres["boundaries"]["schemaVersion"]==2
rec("C13 full security to boundary to native host composition runs on version 2", "schemaVersion 2, no refusal", {"schemaVersion":hostres["boundaries"]["schemaVersion"],"units":len(hostres["native"]["units"])}, okh)
args.out.write_text(json.dumps({"standing":"CLAUDE reference controls for the XA-02 / CR-25 correction; synthetic trusted observations; NOT product qualification","source":str(args.source),"controls":rows,"passed":sum(1 for r in rows if r["holds"]),"failed":[r["control"] for r in rows if not r["holds"]]}, indent=2)+chr(10))
print("controls", sum(1 for r in rows if r["holds"]), "of", len(rows))
sys.exit(0 if all(r["holds"] for r in rows) else 1)
