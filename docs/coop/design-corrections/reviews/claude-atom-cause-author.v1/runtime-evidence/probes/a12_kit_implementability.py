"""Is every token the amendment relies on reachable from the NORMATIVE-ONLY kit?

Kit = .md and .json under docs/v2/contracts/ and docs/coop/design-corrections/ of the successor
source; every .py is excluded. For each token the amended section 4 cites, report the kit files
that carry it. A token found only in .py files would not be implementable by a normative-only
consumer and must not appear in applied design prose.
"""
import json
import re
from pathlib import Path

S = Path("/tmp/opensip-design-corrections/atom-cause-successor.v1/source")
ROOTS = [S / "docs/v2/contracts", S / "docs/coop/design-corrections"]
CONTRACT = "docs/coop/design-corrections/foundation/atom-evaluation-contract.v1.md"
# Same kit boundary the prior publication assessment used: current published contracts and
# schemas only, so historical review folders and build residue cannot supply a clause.
EXCLUDE_DIR = re.compile(r"/(reviews|__pycache__|disposable|before-image|quarantine)/")

TOKENS = [
    "capabilityForRelation",
    "UnavailableProgramBindingV1",
    "engineFamilies",
    "languageModes",
    "universeDomain",
    "sourceUniverse",
    "coverage2",
    "scope2",
    "missing-relation-coverage",
    "selector-unbound",
    "uncovered-expected-source-subject",
    "scope-without-coverage",
    "cross-family-edge-not-owed",
    "coverage-unknown",
    "unavailable-program-binding",
    "population-unknown",
    "source-target-search-unattested",
    "confidenceMillionths",
    "exportsClosed",
    "derivationKinds",
    "resolutionCompleteness",
    "not-attempted",
    "count-at-most",
]

kit = []
for r in ROOTS:
    kit.extend(p for p in r.rglob("*")
               if p.is_file() and p.suffix in (".md", ".json")
               and not EXCLUDE_DIR.search(str(p) + "/"))
kit = sorted(kit)
texts = {}
for p in kit:
    try:
        texts[str(p.relative_to(S))] = p.read_text()
    except Exception:  # noqa: BLE001
        continue

rows = []
for tok in TOKENS:
    hits = [rel for rel, t in texts.items() if tok in t]
    outside = [h for h in hits if h != CONTRACT]
    rows.append({
        "token": tok,
        "kitFiles": len(hits),
        "inKitBesidesThisContract": bool(outside),
        "examples": sorted(outside)[:3],
    })

print(json.dumps({
    "kitFileCount": len(texts),
    "kitRoots": [str(r.relative_to(S)) for r in ROOTS],
    "pythonExcluded": True,
    "tokens": rows,
    "tokensOnlyInThisContract": [r["token"] for r in rows if not r["inKitBesidesThisContract"]],
}, indent=2))
