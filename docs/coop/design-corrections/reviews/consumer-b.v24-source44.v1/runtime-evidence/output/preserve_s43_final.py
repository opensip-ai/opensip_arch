"""source44.v1 setup: before any source44 edit or execution that rewrites them, copy the exact source43.v1 final bytes of the output files this runtime may
change into output/preserved/s43-final/ and record the sha256 of every copied runs/selfcheck/negatives/traces/vectors/envelopes file in
output/preserved/s43-final/results-manifest.json. The complete source43.v1 output also remains in place in the preserved source43.v1 runtime (not read or
written by this runtime). Executable copies are the post-rebind bytes; their pre-rebind hashes are in output/rebind-s44-manifest.json. Refuses to run twice.
Usage: python3 output/preserve_s43_final.py
"""
import hashlib
import json
import os
import shutil
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source44.v1/output/"
DEST = OUT + "preserved/s43-final/"
FILES = (["ref/factbatch.py", "ref/protocol3.py", "vectors/payload_fixtures.py", "vectors/phase3_payload_vectors.py", "vectors/phase3_traces.py",
          "traces/complete.json", "traces/unavailable.json", "traces/cancel.json", "traces/fault.json", "traces/terminal.json", "traces/controls.json",
          "traces/payload-vectors.json", "tools/checkpoint_p123.py", "tools/checkpoint_p9.py", "tools/finalize_review.py", "tools/hc_source43.py",
          "tools/final_custody.py", "tools/provenance_s43.py", "vectors/phase0_custody.py", "vectors/phase0-custody.json", "requirement-status.json",
          "blind-review.md", "blind-review.json", "runs/final-custody.json", "selfcheck/s43-provenance.json", "notes/00-session-standing.md",
          "notes/10-gaps.md", "notes/11-provider-trace-payload-law.md", "notes/12-source43-query-contract.md"]
         + [f"checkpoints/phase-{n}.json" for n in range(12)])


def main():
    if os.path.exists(DEST):
        print("already preserved; refusing to run twice")
        return 1
    rows = []
    for rel in FILES:
        b = open(OUT + rel, "rb").read()
        os.makedirs(os.path.dirname(DEST + rel), exist_ok=True)
        shutil.copyfile(OUT + rel, DEST + rel)
        rows.append({"path": rel, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
    rebind = json.load(open(OUT + "rebind-s44-manifest.json"))
    pre = {r["file"]: r["beforeSha256"] for r in rebind["files"]}
    for r in rows:
        if r["path"] in pre:
            r["preRebindSha256"] = pre[r["path"]]
    results = []
    for sub in ("runs", "selfcheck", "negatives", "traces", "vectors", "envelopes"):
        for name in sorted(os.listdir(OUT + sub)):
            p = f"{OUT}{sub}/{name}"
            if os.path.isfile(p):
                b = open(p, "rb").read()
                results.append({"path": f"{sub}/{name}", "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
    with open(DEST + "manifest.json", "w") as fh:
        json.dump({"standing": "exact source43.v1 final bytes (as copied by the root into source44.v1) of files that source44.v1 may change; "
                               "executable files after the runtime-root rebind only (preRebindSha256 recorded)", "files": rows}, fh, indent=1)
    with open(DEST + "results-manifest.json", "w") as fh:
        json.dump({"standing": "sha256 of every copied source43.v1 result file before any source44 execution", "files": results}, fh, indent=1)
    print(json.dumps({"preserved": len(rows), "resultsHashed": len(results), "stores": sum(1 for r in results if r["path"].endswith(".store.json"))}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
