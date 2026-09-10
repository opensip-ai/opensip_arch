"""From-scratch independent replay of the four exported Runs.

Command:
  /tmp/opensip-architecture-review-env/bin/python -I -B \\
    /tmp/opensip-design-corrections/consumer-b.v12-fresh-other-runs-full-review.v1/output/checker/main.py
"""
from __future__ import annotations

import json
import sys
import traceback
from pathlib import Path

# allow running as a script
HERE = Path(__file__).resolve().parent
if str(HERE.parent) not in sys.path:
    sys.path.insert(0, str(HERE.parent))

from checker.kit_owners import KitOwners, EXPORTS, EXPORT_MANIFEST
from checker.schema_validate import build_registry
from checker.store import load_store
from checker.replay import IndependentReplay

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-kit-other-runs-producing-law-selfaudit.v1/output")


def main() -> int:
    owners = KitOwners()
    registry = build_registry(owners)
    results = []
    for rec in owners.export_manifest["files"]:
        path = str(Path("/tmp/opensip-design-corrections/consumer-b.v12-fresh-other-runs-full-review.v1") / rec["path"])
        store = load_store(path, rec["name"], rec["sha256"], rec["bytes"])
        replay = IndependentReplay(owners, store, registry)
        try:
            result = replay.run()
        except Exception as e:
            result = {
                "exportName": rec["name"],
                "exportPath": path,
                "exportSha256": rec["sha256"],
                "runId": rec.get("runId"),
                "scopedRunVerdict": "FOUR_RUN_REFUSED",
                "firstRefusal": {"code": "CHECKER_EXCEPTION", "message": f"{type(e).__name__}: {e}"},
                "layers": {
                    "raw": {"status": "REFUSED", "firstRefusal": {"code": "CHECKER_EXCEPTION", "message": str(e)}},
                    "structural": {"status": "notReached"},
                    "fullsemantic": {"status": "notReached"},
                },
                "traceback": traceback.format_exc(),
            }
        results.append(result)
        (OUT / "measured" / f"{rec['name']}.replay.json").write_text(json.dumps(result, indent=2, sort_keys=True) + "\n")
        print("===", rec["name"], result.get("scopedRunVerdict"), "first", result.get("firstRefusal"))
        for layer, body in (result.get("layers") or {}).items():
            print("   ", layer, body.get("status"), "faults", body.get("faultCount"), "first", body.get("firstRefusal"))
    (OUT / "measured" / "four-runs-replay.json").write_text(json.dumps(results, indent=2, sort_keys=True) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
