"""Self-check of own prior exported bytes BEFORE any v2 helper correction (source39.v2 self-audit step 1).

For every Run store seeded from source39.v1 (runs/*.store.json listed in runs/seeded-from-v1.json):
  1. byte custody: SHA-256 equals the preserved v1 manifest row (preserved/source39-v1/manifest.json);
  2. fresh-process closure+replay with the UNCHANGED ported v1 helper code (port-manifest.json; tools/replay_run.py), written to
     selfcheck/pre/<name>.replay.json, compared field-by-field with v1's own recorded runs/<name>.replay.json (result, graph
     faults, replay performed/faults, recomputed identities/verdict) - receipts (pid, time, paths) excluded;
  3. fresh-process independent retained-closure walk (tools/walk_run.py, ref/retained_graph.py - NEW in v2, not v1 code), written
     to selfcheck/pre/<name>.walk.json.
Writes selfcheck/pre-summary.json. It asserts nothing about correctness; it records what the unchanged code and the new walker say.
Usage: python3 tools/selfcheck_prior.py
"""
import hashlib
import json
import os
import subprocess
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source42.v3/output/preserved/pre-s42"
REF = ["/tmp/opensip-architecture-review-env/bin/python", "-I", "-B"]
PRE = OUT + "/selfcheck/pre"


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


def comparable(rep):
    sr = rep.get("semanticReplay", {})
    rc = sr.get("recomputed") or {}
    return {"result": rep.get("result"), "graphFaults": rep.get("graphAdmission", {}).get("faults"),
            "admittedRecords": rep.get("graphAdmission", {}).get("admittedRecords"),
            "replayPerformed": sr.get("performed"), "replayFaults": sr.get("faults"),
            "recomputed": {k: rc.get(k) for k in ("proofId", "evidenceId", "sealId", "runId", "policyDerivationId", "verdict",
                                                  "evaluationState", "findingIds", "waivedFindingIds", "ruleOutcomes")}}


def main():
    os.makedirs(PRE, exist_ok=True)
    manifest = {r["path"]: r["sha256"] for r in json.load(open(OUT + "/preserved/source39-v1/manifest.json"))["files"]}
    port = json.load(open(OUT + "/port-manifest.json"))
    code_now = {f["destination"]: sha(OUT + "/" + f["destination"][len("output/"):]) == f["destinationSha256"] for f in port["files"]}
    rows = []
    for s in json.load(open(OUT + "/runs/seeded-from-v1.json"))["stores"]:
        name = s["store"][:-len(".store.json")]
        store = f"{OUT}/runs/{s['store']}"
        row = {"run": name, "storeSha256": sha(store), "custodyEqualsV1Manifest": sha(store) == manifest.get(f"runs/{s['store']}")}
        dst = f"{PRE}/{name}.replay.json"
        p = subprocess.run(REF + [f"{OUT}/tools/replay_run.py", store, dst], capture_output=True, text=True)
        now = json.load(open(dst)) if os.path.exists(dst) else {}
        row["replayExit"] = p.returncode
        row["stderrTail"] = p.stderr[-400:] if not now else None
        prior_path = f"{OUT}/preserved/source39-v1/runs/{name}.replay.json"
        if os.path.exists(prior_path):
            a, b = comparable(json.load(open(prior_path))), comparable(now)
            row["v1Recorded"] = {"result": a["result"], "firstGraphFault": (a["graphFaults"] or [None])[0], "firstReplayFault": (a["replayFaults"] or [None])[0]}
            row["preResult"] = {"result": b["result"], "firstGraphFault": (b["graphFaults"] or [None])[0], "firstReplayFault": (b["replayFaults"] or [None])[0]}
            row["equalToV1Recorded"] = a == b
            row["differingFields"] = sorted(k for k in a if a[k] != b[k])
        else:
            row["v1Recorded"] = None
            row["preResult"] = {"result": now.get("result")}
            row["equalToV1Recorded"] = None
        wdst = f"{PRE}/{name}.walk.json"
        wp = subprocess.run(REF + [f"{OUT}/tools/walk_run.py", store, wdst], capture_output=True, text=True)
        w = json.load(open(wdst)) if os.path.exists(wdst) else {}
        row["walk"] = {"exit": wp.returncode, "result": w.get("result"), "firstRefusal": w.get("firstRefusal"),
                       "faultCount": len(w.get("faults", [])),
                       "faultCodes": sorted({f"{f['obligation']}:{f['code']}:{f['detail'].split(':')[0]}" for f in w.get("faults", [])}),
                       "stderrTail": wp.stderr[-400:] if not w else None}
        rows.append(row)
        print(name, row["custodyEqualsV1Manifest"], row["preResult"]["result"], row["equalToV1Recorded"], row["walk"]["result"],
              (row["walk"]["firstRefusal"] or {}).get("code"))
    doc = {"standing": "pre-correction self-check of own source39.v1 exported bytes with unchanged ported code; the walker is new v2 code",
           "portedCodeUnchangedSincePort": all(code_now.values()), "portedFilesChangedSincePort": sorted(k for k, v in code_now.items() if not v),
           "stores": len(rows), "allCustodyEqual": all(r["custodyEqualsV1Manifest"] for r in rows),
           "allReplayResultsEqualV1Recorded": all(r["equalToV1Recorded"] in (True, None) for r in rows),
           "withoutV1Recorded": [r["run"] for r in rows if r["equalToV1Recorded"] is None],
           "notEqual": [r["run"] for r in rows if r["equalToV1Recorded"] is False],
           "walkResults": {r["run"]: r["walk"]["result"] for r in rows}, "rows": rows}
    json.dump(doc, open(OUT + "/selfcheck/pre-summary.json", "w"), indent=1, sort_keys=True)
    print(json.dumps({k: doc[k] for k in ("portedCodeUnchangedSincePort", "stores", "allCustodyEqual", "allReplayResultsEqualV1Recorded",
                                          "withoutV1Recorded", "notEqual")}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
