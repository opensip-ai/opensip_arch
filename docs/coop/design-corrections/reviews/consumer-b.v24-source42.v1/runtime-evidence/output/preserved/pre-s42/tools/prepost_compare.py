"""Pre/post matrix for HC-33..HC-36 over every claimed complete positive and the designed negative (source39.v2).

For each Run:
  bytes  - v1 store (preserved/source39-v1/runs) vs rebuilt v2 store (runs/): runId equality, proof/evidence/seal identity equality, and the
           exact blob delta (added/removed digests with their frame domain or 'raw/record');
  code x bytes, each in a fresh reference-interpreter process:
           pre code  x v1 bytes  -> selfcheck/pre/<run>.replay.json (already recorded by tools/selfcheck_prior.py; re-read, not re-run)
           post code x v1 bytes  -> selfcheck/post/<run>.v1-bytes.replay.json
           pre code  x v2 bytes  -> selfcheck/post/<run>.pre-code.replay.json
           post code x v2 bytes  -> runs/<run>.replay.fromscratch.json (tools/from_scratch.py; re-read)
Writes selfcheck/prepost-matrix.json.  Usage: python3 tools/prepost_compare.py
"""
import base64
import json
import os
import subprocess
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source42.v1/output/preserved/pre-s42"
REF = ["/tmp/opensip-architecture-review-env/bin/python", "-I", "-B"]
sys.path.insert(0, OUT + "/ref")
import retained_graph as RG  # noqa: E402

POST = OUT + "/selfcheck/post"


def first(rep):
    if not rep:
        return None
    if rep.get("firstRefusal"):
        return rep["firstRefusal"]
    faults = rep.get("graphAdmission", {}).get("faults", []) + (rep.get("semanticReplay", {}).get("faults") or [])
    return {"stage": "graph-admission" if rep.get("graphAdmission", {}).get("faults") else ("semantic-replay" if faults else None),
            "fault": faults[0] if faults else None}


def run_ref(script, store, dst):
    p = subprocess.run(REF + [script, store, dst], capture_output=True, text=True)
    return json.load(open(dst)) if os.path.exists(dst) else {"error": p.stderr[-500:]}


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


def main():
    os.makedirs(POST, exist_ok=True)
    fs = json.load(open(OUT + "/runs/from-scratch.summary.json"))
    rows = []
    for r in fs["runs"]:
        name = r["run"]
        v1_path = f"{OUT}/preserved/source39-v1/runs/{name}.store.json"
        v2_path = f"{OUT}/runs/{name}.store.json"
        v1, v2 = json.load(open(v1_path)), json.load(open(v2_path))
        added, removed = sorted(set(v2["blobs"]) - set(v1["blobs"])), sorted(set(v1["blobs"]) - set(v2["blobs"]))
        i1, i2 = ids(v1), ids(v2)
        pre_v1 = json.load(open(f"{OUT}/selfcheck/pre/{name}.replay.json"))
        post_v1 = run_ref(f"{OUT}/tools/replay_run.py", v1_path, f"{POST}/{name}.v1-bytes.replay.json")
        pre_v2 = run_ref(f"{OUT}/preserved/pre-hc33/tools/replay_run.py", v2_path, f"{POST}/{name}.pre-code.replay.json")
        post_v2 = json.load(open(f"{OUT}/runs/{name}.replay.fromscratch.json"))
        row = {"run": name, "role": r["role"],
               "identitiesUnchanged": i1 == i2, "v1Identities": i1, "v2Identities": i2,
               "blobDelta": {"added": len(added), "addedByDomain": domains(v2["blobs"], added), "removed": len(removed),
                             "removedByDomain": domains(v1["blobs"], removed)},
               "matrix": {"preCode_v1Bytes": {"result": pre_v1.get("result"), "first": first(pre_v1)},
                          "postCode_v1Bytes": {"result": post_v1.get("result"), "first": first(post_v1)},
                          "preCode_v2Bytes": {"result": pre_v2.get("result"), "first": first(pre_v2)},
                          "postCode_v2Bytes": {"result": post_v2.get("result"), "first": first(post_v2),
                                               "retainedClosure": (post_v2.get("retainedClosure") or {}).get("result"),
                                               "reachableOutputSet": (post_v2.get("semanticReplay") or {}).get("reachableOutputSet")}}}
        rows.append(row)
        m = row["matrix"]
        print(name, "ids-equal", row["identitiesUnchanged"], "delta", row["blobDelta"]["addedByDomain"], row["blobDelta"]["removedByDomain"],
              "| pre/v1", m["preCode_v1Bytes"]["result"], "| post/v1", m["postCode_v1Bytes"]["result"], (m["postCode_v1Bytes"]["first"] or {}).get("stage"),
              "| pre/v2", m["preCode_v2Bytes"]["result"], "| post/v2", m["postCode_v2Bytes"]["result"])
    positives = [x for x in rows if x["role"] == "claimed-positive"]
    doc = {"standing": "pre/post helper-correction matrix; every cell is a fresh-process closure over exact exported bytes",
           "rows": rows,
           "allPositiveIdentitiesUnchanged": all(x["identitiesUnchanged"] for x in positives),
           "onlySubjectDescriptorsAdded": all(set(x["blobDelta"]["addedByDomain"]) <= {"evaluation-subject"} and not x["blobDelta"]["removed"] for x in positives),
           "positivesPreCodeV1BytesAdmit": sum(1 for x in positives if x["matrix"]["preCode_v1Bytes"]["result"] == "ADMIT"),
           "positivesPostCodeV1BytesRefuse": sum(1 for x in positives if x["matrix"]["postCode_v1Bytes"]["result"] == "REFUSE"),
           "positivesPreCodeV2BytesAdmit": sum(1 for x in positives if x["matrix"]["preCode_v2Bytes"]["result"] == "ADMIT"),
           "positivesPostCodeV2BytesAdmit": sum(1 for x in positives if x["matrix"]["postCode_v2Bytes"]["result"] == "ADMIT"),
           "positives": len(positives)}
    json.dump(doc, open(OUT + "/selfcheck/prepost-matrix.json", "w"), indent=1, sort_keys=True)
    print(json.dumps({k: v for k, v in doc.items() if k != "rows"}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
