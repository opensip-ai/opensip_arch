fsn,dn,fn=base_fs()
fsn[R+"/vendor"]=dn(); fsn[R+"/vendor/lib"]=dict(dn(), vcs=True); fsn[R+"/vendor/lib/package.json"]=fn()
fsn[R+"/apps"]=dn(); fsn[R+"/apps/site"]=dn(); fsn[R+"/apps/site/opensip.json"]=fn(); fsn[R+"/apps/site/package.json"]=fn()
fsn[R+"/ws"]=dn(); fsn[R+"/ws/Cargo.toml"]=dict(fn(), isCargoWorkspace=True)
fsn[R+"/ws/m"]=dn(); fsn[R+"/ws/m/Cargo.toml"]=fn(); fsn[R+"/ws/target"]=dn()
on=disc(fsn); ivn=S.boundary_inventory(on)
mk=markers_of(fsn)
mk["ws/Cargo.toml"]["isCargoWorkspace"]=True
nn=N.discover_units(mk, None, ivn)
rootsn=sorted(u["rootPath"] for u in nn["units"])
okpar = nn["refused"] is None and "vendor/lib" not in rootsn and "apps/site" not in rootsn
rec("C9a nested repository and nested project stay excluded under the corrected rule", "vendor/lib and apps/site absent", rootsn, okpar)
ws=[u for u in nn["units"] if u["rootPath"]=="ws"]
okws = len(ws)==1 and ws[0]["memberPackageRoots"]==["ws/m"]
rec("C9b Cargo member folding parity", ["ws/m"], (ws[0]["memberPackageRoots"] if ws else None), okws)
tgt=[(t["path"],t["reason"]) for t in nn["prunedTrees"]]
rec("C9c marker-less Cargo target anchor is now reported", "ws/target cargo-build-output present", tgt, ("ws/target","cargo-build-output") in tgt)
oe=disc(fsn, configWorkspaceRoots=["."]) 
ive=S.boundary_inventory(oe)
ne=N.discover_units(mk, ["."], ive)
rootse=sorted(u["rootPath"] for u in ne["units"])
rec("C9d explicit root selection parity", [""], rootse, ne["refused"] is None and rootse==[""])
