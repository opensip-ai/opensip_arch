#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

OUT = Path("/tmp/opensip-design-corrections/consumer-b.v12-team-corrections.v2/output")
sys.path.insert(0, str(OUT))

from helper.status import mark, write_checkpoint  # noqa: E402

p0 = [
    "S-FRESH-ORIGIN",
    "S-NOT-PRODUCT",
    "S-KIT-ONLY",
    "S-MANIFEST-VERIFY",
    "S-NO-ORACLE",
    "S-MISSING-DEP-IS-CUSTODY",
    "S-PROFILE-CURRENT",
    "S-CONTINUATION",
    "R-FIVE-CONTRACTS-INDEX",
    "R-SOURCE-MAP-SCOPE",
    "R-CVE1-TYPES-AVAILABLE",
]
mark(
    p0,
    status="executed",
    artifact="kit-standing.json",
    notes="Phase 0 input custody. 80/80 hashes PASS. Eight CVE1 types present. Governance standing not used as recipe.",
)
ck0 = write_checkpoint(
    0,
    notes="Manifest SHA-256 ea2fa750ff863ef0bbfffb8bd2748dc4b776a7cbf4e43ddd4c8e6998214e6bf8 matches. 80 files PASS. Five contracts indexed. Successor-over-inherited recorded. Eight CVE1 types listed from resolved-inputs.v2 canonicalValueEncoding. Readiness/review records excluded.",
    artifacts=["hash-verification.json", "kit-standing.json", "requirement-status.json"],
)
print("phase0", len(ck0["requirementIdsExecuted"]), "executed", len(ck0["requirementIdsUnexecuted"]), "unexec")

p1 = [
    "R-H-HELPER",
    "R-CVE1-EIGHT-TYPES",
    "R-LEXICAL-ADMISSION",
    "R-SEMANTIC-VS-OPERATIONAL",
    "R-RAW-VS-PARSED",
    "R-ACYCLIC-JOINS",
]
mark(["R-H-HELPER"], status="executed", artifact="vectors/h-helper.json")
mark(["R-CVE1-EIGHT-TYPES"], status="executed", artifact="vectors/cve1-eight-types.json")
mark(["R-LEXICAL-ADMISSION"], status="executed", artifact="vectors/lexical-admission.json")
mark(["R-SEMANTIC-VS-OPERATIONAL"], status="executed", artifact="vectors/semantic-vs-operational.json")
mark(["R-RAW-VS-PARSED"], status="executed", artifact="vectors/raw-vs-parsed.json")
mark(["R-ACYCLIC-JOINS"], status="executed", artifact="vectors/acyclic-joins.json")
ck1 = write_checkpoint(
    1,
    notes="Independent C/H/CVE1 helpers from prose. Eight CVE1 types round-tripped. Raw lexical negatives distinct from parsed encode. Semantic vcsDigest change moves snapshot2; requestId/executionId/wallClock do not. Acyclic snapshot→plan→view→proof→evidence→seal→run; proof naming evidenceId/runId refused.",
    artifacts=[
        "helper/canonical.py",
        "helper/cve1.py",
        "helper/identity.py",
        "helper/lexical.py",
        "vectors/cve1-eight-types.json",
        "vectors/h-helper.json",
        "vectors/lexical-admission.json",
        "vectors/raw-vs-parsed.json",
        "vectors/semantic-vs-operational.json",
        "vectors/acyclic-joins.json",
    ],
)
print("phase1", len(ck1["requirementIdsExecuted"]), "executed", len(ck1["requirementIdsUnexecuted"]), "unexec")
print("p1 ids in executed", [i for i in p1 if i in ck1["requirementIdsExecuted"]])
