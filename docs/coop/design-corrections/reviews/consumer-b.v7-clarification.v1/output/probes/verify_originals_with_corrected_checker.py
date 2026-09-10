"""Run the CORRECTED closure over the ORIGINAL v7 exported bytes.
This is the discriminating check: a corrected validator must refuse the
original graphs that violate the two laws it previously did not enforce."""
import base64, json, os, sys
WORK = "/tmp/opensip-design-corrections/consumer-b.v7-clarification.v1/output/work"
ORIG = "/tmp/opensip-design-corrections/consumer-b.v7/output/vectors"
sys.path.insert(0, WORK)
import oslib as O, graph as G
from oslib import H, sha256hex

out = {}
for name in sorted(f[:-len(".objects.json")] for f in os.listdir(ORIG)
                   if f.endswith(".objects.json")):
    objs = json.load(open("%s/%s.objects.json" % (ORIG, name)))
    blobs = json.load(open("%s/%s.blobs.json" % (ORIG, name)))["blobs"]
    w = G.World(objs["projectId"])
    for d, b64 in blobs.items():
        w.cas[d] = base64.b64decode(b64)
    for key, row in objs["objects"].items():
        dom, desc = row["domain"], row["descriptor"]
        w.objects[key] = desc
        w.frames[H(dom, desc)] = (dom, desc)
    w.inventory = list(w.objects[objs["runId"]]["sourceInventory"]) \
        if "sourceInventory" in w.objects[objs["runId"]] else \
        list(w.objects[w.objects[objs["runId"]]["snapshotId"]]["sourceInventory"])
    c = G.Closure(w)
    errs = c.close_run(objs["runId"])
    out[name] = {"checks": c.checks, "admitted": not errs, "errors": errs,
                 "objectAdmissionCoverage":
                     getattr(c, "objectAdmissionCoverage", None)}
    print("%-40s checks=%4d %s" % (name, c.checks,
                                   "ADMITTED" if not errs else
                                   "REFUSED (%d): %s" % (len(errs), errs[0][:110])))
    for e in errs[1:]:
        print("%44s %s" % ("", e[:110]))
json.dump(out, open(os.path.dirname(os.path.abspath(__file__))
                    + "/corrected-checker-vs-original-exports.json", "w"),
          indent=1, sort_keys=True)
ref = sorted(k for k, v in out.items() if not v["admitted"])
adm = sorted(k for k, v in out.items() if v["admitted"])
print("\nREFUSED %d: %s" % (len(ref), ref))
print("ADMITTED %d: %s" % (len(adm), adm))
