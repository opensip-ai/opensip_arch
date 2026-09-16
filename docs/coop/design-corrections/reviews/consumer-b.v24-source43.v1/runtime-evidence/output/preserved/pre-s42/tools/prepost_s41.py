"""Pre/post matrix for the source41 helper corrections (HC-39 onward) over every claimed complete positive, the designed negative and the
closure controls introduced in source41. Every computed cell is a fresh reference-interpreter closure over exact exported bytes.

  original bytes = preserved/pre-s41/runs/<run>.store.json   (built by the unchanged ported helpers against the source41 kit)
  current bytes  = runs/<run>.store.json                     (rebuilt after the corrections)
  pre code       = preserved/pre-s41/tools/replay_run.py     (unchanged ported helpers, rebound copy)
  post code      = tools/replay_run.py

  pre  x original -> preserved/pre-s41/runs/<run>.replay.fromscratch.json (logs/s41-original.7.from_scratch; re-read, not re-run)
  post x original -> selfcheck/s41/<run>.original-bytes.replay.json
  pre  x current  -> selfcheck/s41/<run>.pre-code.replay.json
  post x current  -> runs/<run>.replay.fromscratch.json (tools/from_scratch.py; re-read)
Controls (source41 mutation stores): pre x current -> selfcheck/s41/<name>.pre-code.replay.json; post x current -> runs/<name>.replay.json.
Writes selfcheck/s41-prepost-matrix.json.  Usage: python3 tools/seq.py <label> tools/prepost_s41.py
"""
import base64
import json
import os
import subprocess
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source43.v1/output/preserved/pre-s42"
PRE = OUT + "/preserved/pre-s41"
REF = ["/tmp/opensip-architecture-review-env/bin/python", "-I", "-B"]
sys.path.insert(0, OUT + "/ref")
import retained_graph as RG  # noqa: E402

DST = OUT + "/selfcheck/s41"
CONTROLS = ["syntax-code~unit-kind-other-family", "syntax-code~unit-root-external-sentinel", "syntax-code~row-view-omitted",
            "ts-pass~unit-kind-not-mode-projection"]


def first(rep):
    if not rep:
        return None
    if rep.get("firstRefusal"):
        return rep["firstRefusal"]
    faults = rep.get("faultsInStageOrder") or (rep.get("graphAdmission", {}).get("faults", []) + (rep.get("semanticReplay", {}).get("faults") or []))
    return {"fault": faults[0]} if faults else None


def run_ref(script, store, dst):
    if os.path.exists(dst):
        os.remove(dst)
    p = subprocess.run(REF + [script, store, dst], capture_output=True, text=True)
    return json.load(open(dst)) if os.path.exists(dst) else {"error": p.stderr[-800:]}


def load(path):
    return json.load(open(path)) if os.path.exists(path) else None


def domains(blobs, keys):
    out = {}
    for h in keys:
        dom, _, err = RG.parse_frame(base64.b64decode(blobs[h]))
        k = dom if err is None else "raw/record"
        out[k] = out.get(k, 0) + 1
    return out


def ids(ex):
    blobs = {h: base64.b64decode(b) for h, b in ex["blobs"].items()}
    _, run, _ = RG.parse_frame(blobs[ex["runId"].split(":", 1)[1]])
    _, seal, _ = RG.parse_frame(blobs[run["evaluationSealId"].split(":", 1)[1]])
    return {"runId": ex["runId"], "evidenceId": run["evidenceId"], "evaluationSealId": run["evaluationSealId"], "proofBundleId": seal["proofBundleId"]}


def cell(rep):
    return {"result": (rep or {}).get("result"), "first": first(rep), "error": (rep or {}).get("error")}


def main():
    os.makedirs(DST, exist_ok=True)
    fs = json.load(open(OUT + "/runs/from-scratch.summary.json"))
    rows = []
    for r in fs["runs"]:
        name = r["run"]
        orig_path, cur_path = f"{PRE}/runs/{name}.store.json", f"{OUT}/runs/{name}.store.json"
        orig, cur = load(orig_path), load(cur_path)
        row = {"run": name, "role": r["role"], "originalStorePresent": orig is not None}
        if orig is not None:
            added, removed = sorted(set(cur["blobs"]) - set(orig["blobs"])), sorted(set(orig["blobs"]) - set(cur["blobs"]))
            i0, i1 = ids(orig), ids(cur)
            row.update({"identitiesUnchanged": i0 == i1, "originalIdentities": i0, "currentIdentities": i1,
                        "blobDelta": {"added": len(added), "addedByDomain": domains(cur["blobs"], added), "removed": len(removed),
                                      "removedByDomain": domains(orig["blobs"], removed)}})
            pre_orig = load(f"{PRE}/runs/{name}.replay.fromscratch.json")
            post_orig = run_ref(f"{OUT}/tools/replay_run.py", orig_path, f"{DST}/{name}.original-bytes.replay.json")
        else:
            pre_orig = post_orig = None
        pre_cur = run_ref(f"{PRE}/tools/replay_run.py", cur_path, f"{DST}/{name}.pre-code.replay.json")
        post_cur = load(f"{OUT}/runs/{name}.replay.fromscratch.json")
        row["matrix"] = {"preCode_originalBytes": cell(pre_orig), "postCode_originalBytes": cell(post_orig),
                         "preCode_currentBytes": cell(pre_cur), "postCode_currentBytes": dict(cell(post_cur),
                                                                                             retainedClosure=((post_cur or {}).get("retainedClosure") or {}).get("result"))}
        rows.append(row)
        m = row["matrix"]
        print(name, "ids-equal", row.get("identitiesUnchanged"), "| pre/orig", m["preCode_originalBytes"]["result"], "| post/orig",
              m["postCode_originalBytes"]["result"], (m["postCode_originalBytes"]["first"] or {}).get("fault"), "| pre/cur", m["preCode_currentBytes"]["result"],
              "| post/cur", m["postCode_currentBytes"]["result"])
    controls = []
    for name in CONTROLS:
        store = f"{OUT}/runs/{name}.store.json"
        if not os.path.exists(store):
            controls.append({"control": name, "storePresent": False})
            continue
        pre = run_ref(f"{PRE}/tools/replay_run.py", store, f"{DST}/{name}.pre-code.replay.json")
        post = load(f"{OUT}/runs/{name}.replay.json")
        controls.append({"control": name, "storePresent": True, "preCode": cell(pre), "postCode": cell(post)})
        print("control", name, "| pre", cell(pre)["result"], (cell(pre)["first"] or {}).get("fault"), "| post", cell(post)["result"], (cell(post)["first"] or {}).get("fault"))
    positives = [x for x in rows if x["role"] == "claimed-positive"]
    doc = {"standing": "pre/post matrix for the source41 helper corrections; every computed cell is a fresh-process closure over exact exported bytes; "
                       "orientation for what the corrections changed, never an oracle",
           "rows": rows, "controls": controls, "positives": len(positives),
           "positiveIdentitiesUnchanged": sum(1 for x in positives if x.get("identitiesUnchanged")),
           "positivesPreCodeOriginalBytesAdmit": sum(1 for x in positives if x["matrix"]["preCode_originalBytes"]["result"] == "ADMIT"),
           "positivesPostCodeOriginalBytesAdmit": sum(1 for x in positives if x["matrix"]["postCode_originalBytes"]["result"] == "ADMIT"),
           "positivesPreCodeCurrentBytesAdmit": sum(1 for x in positives if x["matrix"]["preCode_currentBytes"]["result"] == "ADMIT"),
           "positivesPostCodeCurrentBytesAdmit": sum(1 for x in positives if x["matrix"]["postCode_currentBytes"]["result"] == "ADMIT"),
           "controlsPreCodeAdmit": [c["control"] for c in controls if c.get("preCode", {}).get("result") == "ADMIT"],
           "controlsPostCodeRefuse": [c["control"] for c in controls if c.get("postCode", {}).get("result") == "REFUSE"]}
    json.dump(doc, open(OUT + "/selfcheck/s41-prepost-matrix.json", "w"), indent=1, sort_keys=True)
    print(json.dumps({k: v for k, v in doc.items() if k not in ("rows", "controls")}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
