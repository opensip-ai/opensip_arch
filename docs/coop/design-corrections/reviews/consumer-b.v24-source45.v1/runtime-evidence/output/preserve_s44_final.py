"""source45.v1 setup: preserve the exact source44.v1 final bytes before any source45 rebind, edit or execution.

Copies to output/preserved/s44-final/ (same relative paths):
  - every executable *.py under output/{ref,builders,tools,vectors} (exact copied bytes, before the runtime-root rebind);
  - the source44 review and standing: blind-review.md, blind-review.json, requirement-status.json, checkpoints/*.json, notes/*.md;
  - the source44 phase-3 outputs (traces/*.json), custody reports (vectors/phase0-custody.json, runs/final-custody.json) and selfcheck/*.json.
It also writes preserved/s44-final/results-manifest.json with the sha256 and length of every file under output/{runs,negatives,traces,vectors,envelopes,selfcheck},
and preserved/s44-final/manifest.json for the copied files. Refuses to run twice. Usage: python3 output/preserve_s44_final.py
"""
import glob
import hashlib
import json
import os
import shutil
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source45.v1/output/"
DEST = OUT + "preserved/s44-final/"


def main():
    if os.path.exists(DEST + "manifest.json"):
        print("already preserved; refusing to run twice")
        return 1
    rels = []
    for sub in ("ref", "builders", "tools", "vectors"):
        rels += sorted(os.path.relpath(p, OUT) for p in glob.glob(OUT + sub + "/*.py"))
    rels += ["blind-review.md", "blind-review.json", "requirement-status.json", "vectors/phase0-custody.json", "runs/final-custody.json"]
    for pattern in ("checkpoints/*.json", "notes/*.md", "traces/*.json", "selfcheck/*.json"):
        rels += sorted(os.path.relpath(p, OUT) for p in glob.glob(OUT + pattern))
    rows = []
    for rel in rels:
        src = OUT + rel
        b = open(src, "rb").read()
        os.makedirs(os.path.dirname(DEST + rel), exist_ok=True)
        shutil.copyfile(src, DEST + rel)
        rows.append({"path": rel, "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
    results = []
    for sub in ("runs", "negatives", "traces", "vectors", "envelopes", "selfcheck"):
        for d, _, fs in os.walk(OUT + sub):
            for x in sorted(fs):
                p = os.path.join(d, x)
                b = open(p, "rb").read()
                results.append({"path": os.path.relpath(p, OUT), "sha256": hashlib.sha256(b).hexdigest(), "bytes": len(b)})
    results.sort(key=lambda r: r["path"])
    json.dump({"standing": "exact source44.v1 final bytes as copied by the root into source45.v1, captured before any source45 rebind, edit or execution",
               "files": rows}, open(DEST + "manifest.json", "w"), indent=1)
    json.dump({"standing": "sha256 of every copied source44.v1 result file before any source45 execution", "files": results},
              open(DEST + "results-manifest.json", "w"), indent=1)
    print(json.dumps({"preserved": len(rows), "resultFilesHashed": len(results), "stores": sum(1 for r in results if r["path"].endswith(".store.json"))}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
