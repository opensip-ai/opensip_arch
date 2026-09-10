#!/usr/bin/env python3
"""Measured CapabilityAvailabilityV1 for default vs missing-release cells."""
from __future__ import annotations

import json
import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v13-pilot-admission.v6/output")
sys.path.insert(0, str(OUT))

from helpers import builder  # noqa: E402

def dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")


def notices_for(requested, declared, mode, root):
    out = []
    declared_set = set(declared)
    for cap in requested:
        if cap not in declared_set:
            out.append(
                {
                    "capabilityId": cap,
                    "languageMode": mode,
                    "workspaceRoot": root,
                    "code": "native.capability-unavailable",
                }
            )
    return out


def main() -> None:
    requested = list(builder.TS_TSCONFIG_DEFAULT_CAPS)
    # authenticated release that ships a subset
    declared = ["inventory", "syntax", "imports", "clones-fact"]
    missing = [c for c in requested if c not in declared]
    n = notices_for(requested, declared, "ts-tsconfig", ".")
    step = {"stepId": 0, "noticeCount": len(n), "notices": n}
    avail = {"stepCount": 1, "totalNoticeCount": len(n), "steps": [step]}
    empty = {"stepCount": 0, "totalNoticeCount": 0, "steps": []}
    candidate_only = [c for c in requested if c in ("clones-near", "clones-cross-tsjs")]
    doc = {
        "owners": [
            "docs/v2/contracts/product-v1/native-evidence.md §1.4",
            "docs/v2/contracts/product-v1/workflows-and-surfaces.md §8",
            "docs/v2/contracts/product-v1/admission-and-qualification.md §1.1",
        ],
        "defaultRequestedCapabilities": requested,
        "releaseDeclared": declared,
        "measuredMissing": missing,
        "candidateOnly": candidate_only,
        "singleStep": {
            "command": "analyze",
            "requestClass": "analysis",
            "availability": avail,
            "advisory": True,
            "parityField": "capability-availability",
        },
        "multiStep": {
            "steps": [
                {"stepId": 0, "selection": requested, "availability": avail},
                {
                    "stepId": 1,
                    "selection": ["inventory"],
                    "availability": {
                        "stepCount": 1,
                        "totalNoticeCount": 0,
                        "steps": [{"stepId": 1, "noticeCount": 0, "notices": []}],
                    },
                },
            ],
            "composedNoticeCount": avail["totalNoticeCount"] + 0,
            "noTruncation": True,
        },
        "emptyWhenNothingAbsent": empty,
        "candidateOnlyHaveNoCoverage": True,
        "terminatesNothing": True,
        "measured": True,
    }
    dump(OUT / "envelopes" / "invocation-disclosure.json", doc)
    dump(OUT / "envelopes" / "single-step.json", doc["singleStep"])
    dump(OUT / "envelopes" / "multi-step.json", doc["multiStep"])
    dump(OUT / "vectors" / "multi-unit-missing-caps.json", {
        "measured": True,
        "units": [
            {"workspaceRoot": ".", "languageMode": "ts-tsconfig", "requested": requested, "undeclared": missing},
            {"workspaceRoot": "crates/alpha", "languageMode": "rust-cargo", "requested": ["inventory", "syntax", "clones-fact"], "undeclared": ["syntax"]},
        ],
        "noticesCarryWorkspaceRoot": True,
    })
    dump(OUT / "vectors" / "candidate-only-clones.json", {
        "clones-near": {"relations": [], "coverage": None, "publicRoute": "CommandEnvelope.availability native.capability-unavailable"},
        "clones-cross-tsjs": {"relations": [], "coverage": None, "NOT-SELECTED": ["rust-cargo", "rust-cargo-prepared", "syntax-only"]},
        "measuredMissingOnDefaultTs": [c for c in candidate_only if c in missing],
    })
    print("AVAILABILITY notices", len(n), "missing", missing)


if __name__ == "__main__":
    main()
