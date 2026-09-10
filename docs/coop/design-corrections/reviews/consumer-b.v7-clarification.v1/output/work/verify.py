"""From-scratch verifier for the retained blind-consumer-B v7 Run graphs.

It reads ONLY the exported object table and the exported blob/frame bytes.  It
rebuilds the content-addressed store, recomputes every semantic identity from
the retained descriptors, re-parses every retained H preimage frame, and re-runs
the complete retained closure (schema admission, native context/universe
admission, relation registry joins, Coverage laws, body-identity joins and the
proof/witness joins).

    /tmp/opensip-architecture-review-env/bin/python -I -B verify.py
"""

import base64
import glob
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import oslib as O          # noqa: E402
import graph as G          # noqa: E402
from oslib import C, H, sha256hex   # noqa: E402

VEC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "vectors")


def load(name):
    with open(os.path.join(VEC, name + ".objects.json")) as f:
        objs = json.load(f)
    with open(os.path.join(VEC, name + ".blobs.json")) as f:
        blobs = json.load(f)

    w = G.World(objs["projectId"])
    # 1. rebuild the CAS from the exported bytes, re-hashing every one
    bad_blobs = []
    for digest, b64 in blobs["blobs"].items():
        raw = base64.b64decode(b64)
        if sha256hex(raw) != digest:
            bad_blobs.append(digest)
        w.cas[digest] = raw
    # 2. rebuild the object table, RECOMPUTING every identity from the
    #    descriptor rather than trusting the exported key
    bad_ids = []
    for key, row in objs["objects"].items():
        dom, desc = row["domain"], row["descriptor"]
        hx = H(dom, desc)
        prefix = O.IDENTITY_PREFIX.get(dom)
        expect = (prefix + ":" + hx) if prefix else ("sha256:" + hx)
        if expect != key:
            bad_ids.append((key, expect))
        w.objects[key] = desc
        w.frames[hx] = (dom, desc)
        # the H preimage FRAME must be the retained object under that digest
        if w.cas.get(hx) != O.h_frame(dom, desc):
            bad_ids.append((key, "frame-not-retained"))
    # 3. snapshot inventory comes from the retained snapshot descriptor
    run = w.objects[objs["runId"]]
    w.inventory = list(w.objects[run["snapshotId"]]["sourceInventory"])
    return w, objs["runId"], bad_blobs, bad_ids


def main():
    names = sorted(os.path.basename(p)[:-len(".objects.json")]
                   for p in glob.glob(os.path.join(VEC, "*.objects.json")))
    total_checks = 0
    failures = 0
    report = {}
    for name in names:
        w, run_id, bad_blobs, bad_ids = load(name)
        c = G.Closure(w)
        errs = c.close_run(run_id)
        errs = (["BLOB_DIGEST_MISMATCH:" + d for d in bad_blobs]
                + ["IDENTITY_NOT_RECOMPUTABLE:%s" % (x,) for x in bad_ids]
                + errs)
        total_checks += c.checks
        ok = not errs
        failures += 0 if ok else 1
        report[name] = {"runId": run_id, "checks": c.checks,
                        "objects": len(w.objects), "blobs": len(w.cas),
                        "admitted": ok, "errors": errs}
        print("%-40s objects=%3d blobs=%3d checks=%4d  %s"
              % (name, len(w.objects), len(w.cas), c.checks,
                 "ADMITTED" if ok else "REFUSED: " + "; ".join(errs[:3])))
    print("\n%d graphs, %d closure checks, %d failures"
          % (len(names), total_checks, failures))
    out = os.path.join(VEC, "..", "verify-report.json")
    with open(out, "w") as f:
        json.dump({"graphs": report, "totalChecks": total_checks,
                   "failures": failures}, f, indent=1, sort_keys=True)
    print("report:", os.path.abspath(out))
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
