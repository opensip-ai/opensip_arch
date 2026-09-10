#!/usr/bin/env python3
"""Initialize requirement-status.json from requirements.json. Kit-scope file, not design authority."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path("/tmp/opensip-design-corrections/consumer-b.v12")
OUT = ROOT / "output"
req = json.loads((ROOT / "requirements.json").read_text())

rows = []
for s in req["standing"]:
    rows.append(
        {
            "id": s["id"],
            "kind": s["kind"],
            "acceptBlocking": s["acceptBlocking"],
            "status": "unexecuted",
            "artifact": None,
            "firstRefusal": None,
            "notes": "",
        }
    )
for r in req["requirements"]:
    rows.append(
        {
            "id": r["id"],
            "kind": r["kind"],
            "acceptBlocking": r.get("acceptBlocking", True),
            "status": "unexecuted",
            "artifact": None,
            "firstRefusal": None,
            "notes": "",
        }
    )
for f in req["futureQualification"]:
    rows.append(
        {
            "id": f["id"],
            "kind": f["kind"],
            "acceptBlocking": False,
            "status": "futureQualification",
            "artifact": None,
            "firstRefusal": None,
            "notes": "Not demanded; not claimed as proof.",
        }
    )

(OUT / "requirement-status.json").write_text(json.dumps(rows, indent=2) + "\n")
print("rows", len(rows))
print("standing", len(req["standing"]), "requirements", len(req["requirements"]), "future", len(req["futureQualification"]))
