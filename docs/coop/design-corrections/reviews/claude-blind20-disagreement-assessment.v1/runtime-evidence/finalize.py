#!/usr/bin/env python3
"""Final integrity record for this diagnosis runtime. READ-ONLY outside; writes only here."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

H = Path(__file__).resolve().parent


def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()


deliverables = [{"file": n, "bytes": (H / n).stat().st_size, "sha256": sha(H / n)}
                for n in ("diagnosis.md", "diagnosis.json") if (H / n).is_file()]
files = sorted(str(p.relative_to(H)) for p in H.rglob("*") if p.is_file())
d = json.loads((H / "diagnosis.json").read_text())
out = {
    "standing": "Final integrity record. READ-ONLY diagnosis; no acceptance.",
    "deliverables": deliverables,
    "runtimeFileCount": len(files),
    "rootCauseIds": [r["id"] for r in d["rootCauses"]],
    "rootCauseClassifications": {r["id"]: r["classification"] for r in d["rootCauses"]},
    "surfaceClassifications": {k: v["classification"] for k, v in d["surfaceClaims"].items()},
    "frozenVerified": d["frozenSource"]["everyManifestRowVerifiedByteExact"],
    "designChangeNeeded": d["doesSource33NeedADesignChange"]["answer"],
    "receiptCount": len(d["receipts"]),
    "nonZeroExitReceipts": d["nonZeroExitReceipts"],
    "limitationCount": len(d["limitations"]),
    "acceptance": None,
}
(H / "finalize-report.json").write_text(json.dumps(out, indent=2) + "\n")
print(json.dumps(out, indent=2))
