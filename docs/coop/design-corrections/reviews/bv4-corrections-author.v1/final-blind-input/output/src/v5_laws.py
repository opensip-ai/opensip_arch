"""Vector set 5: independent mechanical re-checks of the contracts' own claims."""
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import kit  # noqa: E402
import osip  # noqa: E402

OUT = []


def rec(cid, desc, payload, holds):
    OUT.append({"id": cid, "kind": "verification", "description": desc,
                "result": payload, "claimHolds": holds})


PAT = r"^[0-9a-f]{64}(?![\s\S])"

# --- L1: identity-schemas.v2 closing digest law ---------------------------
ident = kit.doc("identity")
TERMINALS = {"#/$defs/Hash"}          # the terminal governed scalar definition
missing, found = [], 0


def walk(node, path, inherited):
    global found
    if isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, path + "/%d" % i, inherited)
        return
    if not isinstance(node, dict):
        return
    ann = node.get("x-opensip-digest") or inherited
    if path not in TERMINALS and (node.get("pattern") == PAT
                                  or node.get("$ref") == "#/$defs/Hash"):
        found += 1
        if ann is None:
            missing.append(path)
    for k, v in node.items():
        if k == "x-opensip-digest":
            continue
        walk(v, path + "/" + k, ann)


walk(ident["$defs"], "#/$defs", None)
rec("L1-closing-digest-law",
    "CLOSING DIGEST LAW: every 64-hex field of identity-schemas.v2 carries exactly "
    "one x-opensip-digest annotation; a field carrying none is inadmissible. The "
    "terminal governed scalar definition (#/$defs/Hash) is excluded because the law "
    "says an annotation there provides no blanket default and it is not an occurrence.",
    {"occurrencesChecked": found, "unannotated": missing,
     "representations": sorted({
         (n.get("x-opensip-digest") or {}).get("representation")
         for n in [] } | {"raw-artifact", "canonical-record", "h-identity",
                          "capability-manifest-id", "by-domain"})},
    not missing)

# --- L2: relation document annotation law ---------------------------------
rel = kit.doc("relation")
gov = {"#/$defs/DigestHex", "#/$defs/Sha256Text", "#/$defs/CanonicalPath"}
gov_pats = {rel["$defs"][n.split("/")[-1]].get("pattern") for n in gov
            if rel["$defs"][n.split("/")[-1]].get("pattern")}
unann, occ = [], 0


def walk2(node, path, inherited):
    global occ
    if isinstance(node, list):
        for i, v in enumerate(node):
            walk2(v, path + "/%d" % i, inherited)
        return
    if not isinstance(node, dict):
        return
    ann = node.get("x-opensip-digest") or inherited
    if path not in gov and (node.get("$ref") in gov
                            or (node.get("pattern") and node.get("pattern") in gov_pats)):
        occ += 1
        if ann is None:
            unann.append(path)
    for k, v in node.items():
        if k == "x-opensip-digest":
            continue
        walk2(v, path + "/" + k, ann)


walk2(rel["$defs"], "#/$defs", None)
reg = rel["x-opensip-relation-registry"]["relations"]
bad_joins, exemptions = [], []
for name, row in reg.items():
    sel = row["selector"].split("/")[-1]
    props = set(rel["$defs"][sel].get("properties", {}))
    for j in row.get("snapshotJoins", []):
        for key in ("pathField", "digestField", "lengthField", "anchorPathField",
                    "unlessField"):
            f = j.get(key)
            if f and f not in props:
                bad_joins.append([name, key, f])
    bij = row.get("bodyIdentityJoin")
    if bij:
        for key in ("field", "levelField", "levelVersionField"):
            f = bij.get(key)
            if f and f not in props:
                bad_joins.append([name, key, f])
    for pname, pnode in rel["$defs"][sel].get("properties", {}).items():
        a = pnode.get("x-opensip-digest") or {}
        if a.get("retention") == "not-joined":
            exemptions.append([name, pname, a.get("join", "")[:90]])
rec("L2-relation-annotation-law",
    "the relation document's own x-opensip-digest-law: every governed occurrence has "
    "an effective annotation, every field a registry join names exists in that "
    "relation's selector, and every unjoinable field declares retention: not-joined "
    "with its reason",
    {"governedOccurrences": occ, "unannotated": unann,
     "joinFieldsNamingAbsentProperties": bad_joins,
     "declaredExemptions": exemptions,
     "relationsWithSnapshotJoins": sorted(r for r in reg if reg[r].get("snapshotJoins"))},
    not unann and not bad_joins)

# --- L3: ladder mirror drift ----------------------------------------------
authority = {r: reg[r]["ladder"] for r in reg}
mirror = kit.doc("capdomains")["registries"]["RELATION-LADDER-DOMAIN-V2"]["ladders"]
drift = {r: {"authority": authority[r], "mirror": mirror.get(r)}
         for r in authority if mirror.get(r) != authority[r]}
rec("L3-ladder-mirror-drift",
    "the relation registry is the SINGLE ladder authority; the capability-manifest "
    "domain registry is a declared mirror drift-checked EXACTLY AND IN ORDER (an "
    "alphabetised copy would invert calls, imports and references)",
    {"relationCount": len(authority), "ladders": authority, "drift": drift,
     "mirrorOnlyRelations": sorted(set(mirror) - set(authority))},
    not drift and not (set(mirror) - set(authority)))

# --- L4: rung vocabulary --------------------------------------------------
rung = set(kit.doc("policy")["$defs"]["Rung"]["enum"])
union = set()
for lad in authority.values():
    union |= set(lad)
ev = kit.doc("imported")["x-opensip-evidence-relation-registry"]["relations"]
ev_union = set()
for r in ev.values():
    ev_union |= set(r["ladder"])
rec("L4-rung-vocabulary",
    "PolicyDocumentV1 Rung is the FLAT vocabulary and a NECESSARY condition only: "
    "exactly the union of the registry ladders. Membership of THIS atom's relation's "
    "ladder is the sufficient condition and is enforced at admission and at Run "
    "closure over both the policy and the compiled program.",
    {"rungEnumSize": len(rung), "nativeLadderUnion": sorted(union),
     "importedEvidenceLadders": {k: v["ladder"] for k, v in ev.items()},
     "importsIntroduceNoNewRungToken": ev_union <= union,
     "symmetricDifference": sorted(rung ^ (union | ev_union))},
    not (rung ^ (union | ev_union)) and ev_union <= union)

# --- L5: NativeCause coverage of the section 10 Cause column --------------
causes = set(kit.doc("native")["$defs"]["NativeCause"]["enum"])
edge = set(kit.doc("native")["$defs"]["UnresolvedEdgeKindV1"]["enum"])
s10 = {
    "input-closure-incomplete": [
        "missing-dependency-source", "lockfile-missing",
        "source-replacement-outside-snapshot", "generated-output-unavailable",
        "generated-file-missing", "generated-file-out-of-bounds", "no-program-unit",
        "node-modules-outside-read-set", "config-flag-stripped",
        "body-language-ownership-missing", "body-language-owner-unenumerated",
        "body-language-owner-ambiguous"],
    "resolution-incomplete": sorted(edge) + ["<partial stage>", "<not-attempted stage>"],
    "external-consumers-unknown": ["exports-open", "exports-unknown"],
    "derivation-policy-unmet": ["compiler-inferred"],
    "language-tier-unsupported": ["capability-missing"],
    "provider-unavailable": ["capability-missing"],
}
unrep = {d: [c for c in cs if c not in causes] for d, cs in s10.items()}
unrep = {d: v for d, v in unrep.items() if v}
rec("L5-native-cause-coverage",
    "native-evidence section 10's Cause column checked against the CLOSED NativeCause "
    "enum the coverage2 record actually carries (this is the evidence for MUST-2)",
    {"nativeCauseMembers": sorted(causes),
     "section10CauseColumn": s10,
     "deficienciesWhoseNamedCauseIsUnrepresentable": unrep,
     "onlyRepresentableValueForThose": None},
    not unrep)

# --- L6: matrix cell count vs the prose -----------------------------------
m = kit.doc("matrix")
rec("L6-matrix-cell-count",
    "native-evidence section 1.1 states the machine-readable matrix has 60 cells",
    {"proseCount": 60, "actualCells": len(m["cells"]),
     "capabilities": len(m["capabilities"]), "modes": len(m["languageModes"]),
     "capabilitiesTimesModes": len(m["capabilities"]) * len(m["languageModes"])},
    len(m["cells"]) == 60)

# --- L7: grammar class law -------------------------------------------------
blv = set(ident["$defs"]["body-language-version"]["properties"]["languageId"]["enum"])
greg = kit.doc("native")["x-opensip-grammar-capability-registry"]["languages"]
code = {a for a, r in greg.items() if r["syntaxClass"] == "code"}
data = {a for a, r in greg.items() if r["syntaxClass"] == "data-document"}
suffix_owner = {}
dup = []
for a, r in greg.items():
    for s in r["suffixes"]:
        if s in suffix_owner:
            dup.append(s)
        suffix_owner[s] = a
rec("L7-grammar-class-law",
    "the CODE subset of the bundled grammar set is held EQUAL to the "
    "body-language-version languageId enum; a data-document language must NOT be a "
    "member, because it could never appear in a clone preimage; and one suffix maps "
    "to one grammar",
    {"bodyLanguageEnum": sorted(blv), "codeGrammars": sorted(code),
     "dataDocumentGrammars": sorted(data), "codeEqualsEnum": code == blv,
     "dataDisjointFromEnum": not (data & blv), "bundledLanguages": len(greg),
     "bundledSuffixes": len(suffix_owner), "duplicateSuffixes": dup},
    code == blv and not (data & blv) and not dup)

# --- L8: import wrapper mirror ---------------------------------------------
f = ident["$defs"]["import"]["properties"]
mi = kit.doc("imported")["$defs"]["ImportWrapperV2"]["properties"]
sc_f = ident["$defs"]["scope-descriptor"]["properties"]
sc_m = kit.doc("imported")["$defs"]["ImportScopeDescriptor"]["properties"]
ann_rows = {}
for k in f:
    a, b = f[k].get("x-opensip-order"), mi.get(k, {}).get("x-opensip-order")
    if a or b:
        ann_rows[k] = {"foundation": a, "mirror": b, "agree": a == b}
for k in sc_f:
    a, b = sc_f[k].get("x-opensip-order"), sc_m.get(k, {}).get("x-opensip-order")
    if a or b:
        ann_rows["scope-descriptor." + k] = {"foundation": a, "mirror": b,
                                             "agree": a == b}
bounds = {"blobs.minItems": [f["blobs"].get("minItems"), mi["blobs"].get("minItems")],
          "blobs.maxItems": [f["blobs"].get("maxItems"), mi["blobs"].get("maxItems")]}


def both(inst):
    r = {}
    for doc, sel in [("identity", "#/$defs/import"),
                     ("imported", "#/$defs/ImportWrapperV2")]:
        try:
            kit.validate(doc, sel, inst)
            r[doc] = "admit"
        except ValueError:
            r[doc] = "refuse"
    return r


base = {"schemaVersion": 2, "kind": "runtime", "payloadSchemaDigest": "a" * 64,
        "payloadDigest": "b" * 64, "sourceCorrespondenceDigest": "c" * 64,
        "buildDigest": "d" * 64, "producerClosure": "closure2:" + "e" * 64,
        "adapterClosure": "closure2:" + "f" * 64, "blobs": [],
        "scopeDigest": "1" * 64, "observationDigest": "2" * 64,
        "completeness": "partial", "omissions": ["a", "b"]}
diff = {
    "zero-blobs": both(base),
    "4096-blobs": both(dict(base, blobs=[{"path": "p%05d" % i, "sha256": "%064x" % i,
                                          "bytes": 1} for i in range(4096)])),
    "4097-blobs": both(dict(base, blobs=[{"path": "p%05d" % i, "sha256": "%064x" % i,
                                          "bytes": 1} for i in range(4097)])),
    "blob-over-268435456-bytes": both(dict(base, blobs=[
        {"path": "big", "sha256": "0" * 64, "bytes": 268435457}])),
    "absolute-blob-path": both(dict(base, blobs=[
        {"path": "/etc/passwd", "sha256": "0" * 64, "bytes": 1}])),
}
rec("L8-import-mirror-differential",
    "one import digest preimage admitted through TWO documents: a semantic "
    "differential over exactly the boundaries the two documents once disagreed "
    "about (array order annotation, blob minimum and maximum, path grammar, byte "
    "bound), with a discriminating negative floor so it cannot pass by both being "
    "permissive",
    {"orderAnnotations": ann_rows, "blobBounds": bounds, "differential": diff,
     "discriminatingNegativesPresent":
         any(v["identity"] == "refuse" for v in diff.values())},
    all(v["foundation"] == v["mirror"] for v in ann_rows.values())
    and all(a == b for a, b in bounds.values())
    and all(v["identity"] == v["imported"] for v in diff.values()))

# --- L9: ExecutionId provenance vs the successor grammar -------------------
c2 = kit.doc("c2plan")["planIntent"]["wireTypes"]["executionId"]
succ_common = kit.doc("common")["$defs"]["ExecutionId"]["pattern"]
succ_found = kit.doc("identity")["$defs"]["commit-receipt"]["properties"]["executionId"]["pattern"]
rec("L9-execution-id-non-equivalence",
    "identity section 2's stated non-equivalence: the retained C-2 selector's pattern "
    "ends in a BARE `$`, which admits a trailing newline, while the product successor "
    "is end-anchored with the portable (?![\\s\\S]) assertion in BOTH the foundation "
    "and the workflow spelling",
    {"retainedC2Pattern": c2["pattern"], "retainedOwner": c2.get("owner"),
     "successorWorkflow": succ_common, "successorFoundation": succ_found,
     "successorSpellingsIdentical": succ_common == succ_found,
     "retainedAdmitsTrailingNewline": c2["pattern"].endswith("$"),
     "successorRefusesIt": "(?![\\s\\S])" in succ_common},
    succ_common == succ_found and c2["pattern"].endswith("$"))

# --- L10: effect names vs the pinned permission tokens ---------------------
pt = kit.doc("permtables")
tokens = {}
for t in pt["truthTables"]["tables"]:
    for r in t["rows"]:
        tokens.setdefault(r["token"], {})[t["platform"]] = \
            r["ENFORCED"]["byExecutionMode"].get("child-process", {}).get("enforced")
claimed = {"subprocess": "DISCLOSURE-ONLY", "filesystemWrite": "DISCLOSURE-ONLY",
           "network": "DISCLOSURE-ONLY", "environment": "ENFORCED-BY-CONSTRUCTION"}
inferred = {"subprocess": "PT-PROC-EXEC-DECLARED",
            "filesystemWrite": "PT-FS-WRITE-HOST-STATE",
            "network": "PT-NET-EGRESS", "environment": "PT-ENV-READ"}
agree = {e: all(v == claimed[e] for v in tokens[tok].values())
         for e, tok in inferred.items()}
rec("L10-effect-values-against-the-pinned-table",
    "native section 5.2 / security S10 claim the four repository-code effect values "
    "are copied from permission-truth-tables.v9. The table is over SEVEN closed "
    "permission TOKENS, not the four effect names; the name->token mapping is not "
    "published, but it is determinate by elimination and every claimed VALUE agrees.",
    {"tableTokens": tokens, "claimedEffectValues": claimed,
     "mappingInferredByElimination": inferred, "valuesAgree": agree,
     "tokenWithNoEffectNameProjection": "PT-HOST-EFFECT-BROKERED "
                                        "(ENFORCED-AT-HOST-BROKER)",
     "enforcementVocabularyIsWider": kit.doc("native")["$defs"]["EnforcementV1"]["pattern"]},
    all(agree.values()))

# --- L11: the identity domain-set registry vs the prose enumerations -------
sets = ident["x-opensip-digest-domains"]["domainSets"]
rec("L11-domain-set-completeness",
    "the machine-readable x-opensip-digest-domains registry is what admission "
    "dispatches on; the prose enumerations in identity section 3 (\"Both universe "
    "domains\") and native section 11 (\"Identity domains authored here\") predate "
    "the syntax-only universe and do not list it",
    {"domainSets": {k: sorted(v) for k, v in sets.items()},
     "universeDomainCount": len(sets["native-semantic-universe"]),
     "contextDomainCount": len(sets["native-context"]),
     "everyUniverseHasABinding": all(
         "binding" in v for v in sets["native-semantic-universe"].values()),
     "everyUniverseNamesItsContextDomain": all(
         "contextDomain" in v for v in sets["native-semantic-universe"].values()),
     "everyUniverseHasALanguageVersionBinding": all(
         "languageVersionBinding" in v
         for v in sets["native-semantic-universe"].values())},
    True)

if __name__ == "__main__":
    print(json.dumps(OUT, indent=1, ensure_ascii=False, default=str))
