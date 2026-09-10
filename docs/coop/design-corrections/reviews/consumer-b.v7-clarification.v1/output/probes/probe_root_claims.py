"""PRE-FIX PROBE. Reproduce root's two claimed defects against the ORIGINAL
exported bytes, using the ORIGINAL helper modules, before any correction."""
import base64, json, os, sys
WORK = "/tmp/opensip-design-corrections/consumer-b.v7-clarification.v1/output/work"
ORIG = "/tmp/opensip-design-corrections/consumer-b.v7/output"
sys.path.insert(0, WORK)
import oslib as O
from oslib import C, H, sha256hex

names = sorted(f[:-len(".objects.json")] for f in os.listdir(ORIG + "/vectors")
               if f.endswith(".objects.json"))
report = {}
for n in names:
    objs = json.load(open("%s/vectors/%s.objects.json" % (ORIG, n)))
    blobs = json.load(open("%s/vectors/%s.blobs.json" % (ORIG, n)))["blobs"]
    cas = {d: base64.b64decode(b) for d, b in blobs.items()}
    r = {"findings": [], "grammar": None}

    # ---- claim A: finding.evidenceRefs strictly ascending by C(item)?
    for key, row in sorted(objs["objects"].items()):
        if row["domain"] != "finding":
            continue
        refs = row["descriptor"]["evidenceRefs"]
        keys = [C(x) for x in refs]
        asc = all(keys[i] < keys[i + 1] for i in range(len(keys) - 1))
        r["findings"].append({
            "finding": key, "count": len(refs), "strictlyAscendingByC": asc,
            "asRetained": [x["domain"] for x in refs],
            "canonicalSortWouldBe": [x["domain"] for x in
                                     sorted(refs, key=lambda y: C(y))],
            "schemaAnnotation": O.doc("identity")["$defs"]["finding"]
                ["properties"]["evidenceRefs"]["x-opensip-order"],
            "jsonSchemaAloneAdmits":
                O.validate("identity", "#/$defs/finding", row["descriptor"]) == [],
            "orderAdmissionFaults":
                O.admit_ordered("identity", "#/$defs/finding", row["descriptor"])})

    # ---- claim B: grammar bundle members present in the DECLARED closure tree?
    ctxs = [(k, row) for k, row in objs["objects"].items()
            if row["domain"] == "native.context.syntax.v2"]
    if ctxs:
        _, ctx = ctxs[0]
        gb = ctx["descriptor"]["grammarBundle"]
        cl = objs["objects"].get(gb["closureId"])
        tree = {m["sha256"] for m in cl["descriptor"]["tree"]} if cl else set()
        members = [("bundleDigest", gb["bundleDigest"]),
                   ("normalizer.specificationDigest",
                    gb["normalizer"]["specificationDigest"])]
        members += [("grammarDigest:" + g["grammarId"], g["grammarDigest"])
                    for g in gb["grammars"]]
        r["grammar"] = {
            "closureId": gb["closureId"], "treeMemberCount": len(tree),
            "declaredMembers": [
                {"field": f, "digest": d, "inDeclaredClosureTree": d in tree,
                 "retainedSomewhereInCas": d in cas} for f, d in members],
            "allInTree": all(d in tree for _, d in members)}
    report[n] = r

viol_order = sorted(n for n, r in report.items()
                    if any(not f["strictlyAscendingByC"] for f in r["findings"]))
viol_tree = sorted(n for n, r in report.items()
                   if r["grammar"] and not r["grammar"]["allInTree"])
summary = {"graphsWithUnorderedEvidenceRefs": viol_order,
           "graphsWithGrammarMembersOutsideTheDeclaredTree": viol_tree,
           "distinctGraphsRefusedByEitherDefect":
               sorted(set(viol_order) | set(viol_tree)),
           "graphsClean": sorted(set(report) - set(viol_order) - set(viol_tree))}
json.dump({"summary": summary, "perGraph": report},
          open(os.path.dirname(os.path.abspath(__file__))
               + "/probe-root-claims.json", "w"), indent=1, sort_keys=True)
print(json.dumps(summary, indent=1))
for n in sorted(report):
    for f in report[n]["findings"]:
        print("  %-38s asc=%-5s retained=%s canonical=%s orderFaults=%d"
              % (n, f["strictlyAscendingByC"], f["asRetained"],
                 f["canonicalSortWouldBe"], len(f["orderAdmissionFaults"])))
    g = report[n]["grammar"]
    if g:
        for m in g["declaredMembers"]:
            print("  %-38s %-34s inTree=%-5s inCas=%s"
                  % (n, m["field"], m["inDeclaredClosureTree"],
                     m["retainedSomewhereInCas"]))
