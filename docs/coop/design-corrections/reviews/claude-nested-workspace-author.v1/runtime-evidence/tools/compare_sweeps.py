"""Compare pre-fix and post-fix discrimination sweep digests.

Usage: compare_sweeps.py PRE_DIGESTS POST_DIGESTS OUT_JSON

Claim checked: the correction changes nothing on inputs that returned before (byte-identical canonical output) and
turns every input that raised into a returned output. Non-zero exit otherwise.
"""
import json
import sys
from pathlib import Path

pre = json.loads(Path(sys.argv[1]).read_text())
post = json.loads(Path(sys.argv[2]).read_text())
out = {"preInputs": len(pre), "postInputs": len(post), "sameInputSet": set(pre) == set(post),
       "preReturnedPostIdentical": 0, "preReturnedPostDiffers": [], "preRaisedPostReturned": 0, "preRaisedByType": {},
       "postRaised": []}
for key in sorted(set(pre) & set(post)):
    a, b = pre[key], post[key]
    if a.startswith("raise:"):
        out["preRaisedByType"][a] = out["preRaisedByType"].get(a, 0) + 1
        if b.startswith("raise:"):
            out["postRaised"].append(key)
        else:
            out["preRaisedPostReturned"] += 1
    elif b.startswith("raise:"):
        out["postRaised"].append(key)
    elif a == b:
        out["preReturnedPostIdentical"] += 1
    else:
        out["preReturnedPostDiffers"].append(key)
out["holds"] = out["sameInputSet"] and not out["preReturnedPostDiffers"] and not out["postRaised"]
Path(sys.argv[3]).write_text(json.dumps(out, indent=1) + "\n")
print(json.dumps({k: (v if not isinstance(v, list) else len(v)) for k, v in out.items()}, indent=1))
raise SystemExit(0 if out["holds"] else 1)
