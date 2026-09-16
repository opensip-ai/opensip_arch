import json, hashlib, difflib, os, sys
SUCC=sys.argv[1]+chr(47); OUT=sys.argv[2]
os.makedirs(OUT, exist_ok=True)
D=chr(36)+"defs"; R=chr(36)+"ref"
rows=[]
BASIS={"type":"string","enum":["not-enumerated","observed-inventory"],"description":"Whether the SUPPLIED marker inventory enumerated inside this pruned tree. not-enumerated means discovery did not descend, or the anchor own directory observation could not be established, and markerCount is null. observed-inventory means markerCount is exact OVER THE SUPPLIED INVENTORY ONLY; zero observed never means zero hidden. Provenance only: never a comparison key, never a unit-selection, work-bound, Coverage or scope input."}
NN={"oneOf":[{"type":"null"},{R:"#/"+D+"/I64NonNegative"}]}
REASON=["dependency-tree","vcs-tree","cargo-build-output"]
REQ=["path","reason","markerCount","markerCountBasis"]
ROWDESC="Pruned-tree row VERSION 2 (XA-02 / CR-25). Closed four-member row. The anchor is known from the admitted directory observation and is recorded even when no descendant marker was observed; discovery never descends into the tree to obtain a count or to find a nested anchor. markerCount is null if and only if markerCountBasis is not-enumerated. Version-1 rows keep their bytes under the version-1 records and are read as version 1, never re-read as version 2."
PTDESC="anchors of dependency (node_modules), VCS (.git/.hg/.svn/.jj) and Cargo build-output (target directly under a Cargo.toml directory) trees observed under the selected root; pruned by exact path segment per ../discovery-defaults.py; one record per tree, never per package. VERSION 2 (CR-25): an anchor observed as a directory entry is recorded even with zero observed descendant markers, and the count carries an explicit basis."
CNTDESC="Exact count of distinct supplied marker paths under this anchor when markerCountBasis is observed-inventory; null when not-enumerated. Common i64 nonnegative domain, shared byte-for-byte with the native mirror."
INVDESC="TRUSTED ADMITTED INPUT (P3), VERSION 2 (XA-02 / CR-25): the security discovery instrument authority boundaries for the selected root, converted once by discovery-defaults.boundary_inventory_from_provenance from the ACCEPTed DiscoveryProvenanceV2. Its prunedTrees may name an anchor the marker inventory alone cannot derive; the native instrument accepts those as additional known anchors and never re-derives a boundary from caller input. Never authored by a caller."
UDDESC="Unit discovery output VERSION 2 (XA-02 / CR-25): version-2 pruned rows. Under an admitted boundary inventory the prunedTrees carried here are the ADMITTED anchors, which may include anchors the marker inventory alone cannot derive. Version 1 remains the historical record and the standalone-lane output."
I64DESC="Common i64 nonnegative domain, equal to the security bundle I64NonNegative. Introduced by XA-02 so the pruned-tree markerCount domain is ONE domain in both mirrors; the version-1 native row allowed an unsigned 64-bit upper bound that was never the security mirror domain."
def write(rel, mut, indent, ea):
    p=SUCC+rel; original=open(p).read(); d=json.loads(original); mut(d)
    updated=json.dumps(d, indent=indent, ensure_ascii=ea)+chr(10)
    open(p,"w").write(updated)
    patch="".join(difflib.unified_diff(original.splitlines(True), updated.splitlines(True), fromfile=rel, tofile=rel))
    open(OUT+chr(47)+os.path.basename(rel)+".patch","w").write(patch)
    rows.append({"path":rel,"beforeSha256":hashlib.sha256(original.encode()).hexdigest(),"afterSha256":hashlib.sha256(updated.encode()).hexdigest(),"beforeBytes":len(original.encode()),"afterBytes":len(updated.encode()),"patchLines":patch.count(chr(10))})
    print("OK %-52s %s to %s patchLines=%d" % (rel.split(chr(47))[-1], rows[-1]["beforeSha256"][:12], rows[-1]["afterSha256"][:12], rows[-1]["patchLines"]))
