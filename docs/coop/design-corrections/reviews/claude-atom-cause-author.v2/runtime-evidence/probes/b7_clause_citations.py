"""Resolve each LOAD-BEARING citation of the amendment to an exact published location.

v1 reported a token census over a 169-file current-contract set. Root is right that this is not the
102-file blind kit and that token presence is not implementability. This probe is narrower and
stronger for the clauses that actually carry the amendment: it resolves each citation to a file and
JSON pointer / line and prints what is there, so a reader can check the rule is derivable rather
than merely that the word occurs. It still proves nothing about any other kit boundary.
"""
import json
from pathlib import Path

S = Path("/tmp/opensip-design-corrections/atom-cause-successor.v1/source/docs/coop/design-corrections")

JSON_CITES = [
    ("capabilityForRelation[relation]",
     "foundation/evaluator-projection-registry.v1.json", ["capabilityForRelation"]),
    ("engineFamilies.families[*].languageModes / universeDomain",
     "foundation/evaluator-projection-registry.v1.json", ["engineFamilies", "families"]),
    ("AtomCauseV1.universe (optional, nullable)",
     "foundation/evaluator-projection-registry.v1.json", ["$defs", "AtomCauseV1"]),
    ("evaluation-deficiency.universe (required, nullable)",
     "foundation/identity-schemas.v3.json", ["$defs", "evaluation-deficiency"]),
    ("ViewEntryV3.coverage enum",
     "native/native-evidence.schemas.v2.json", ["$defs", "ViewEntryV3", "properties", "coverage"]),
    ("ResolutionCompletenessState enum",
     "native/native-evidence.schemas.v2.json", ["$defs", "ResolutionCompletenessState"]),
    ("ClosedWorldV2.exportsClosed enum",
     "native/native-evidence.schemas.v2.json",
     ["$defs", "ClosedWorldV2", "properties", "exportsClosed"]),
    ("UnavailableProgramBindingV1",
     "foundation/enumeration-plan.schema.v1.json", ["$defs", "UnavailableProgramBindingV1"]),
]

MD_CITES = [
    ("DEPENDS_ON graph is published in prose",
     "foundation/atom-evaluation-contract.v1.md", "reachability→`calls@resolved-callee`"),
    ("incoming accounting obligation",
     "foundation/atom-evaluation-contract.v1.md", "account **every** represented Coverage"),
]

rows = []
for label, rel, pointer in JSON_CITES:
    doc = json.loads((S / rel).read_text())
    node, missing = doc, None
    for key in pointer:
        if isinstance(node, dict) and key in node:
            node = node[key]
        else:
            missing = key
            break
    rows.append({
        "citation": label, "file": rel, "pointer": "/".join(pointer),
        "resolved": missing is None,
        "missingKey": missing,
        "requiredList": node.get("required") if missing is None and isinstance(node, dict) else None,
        "enum": node.get("enum") if missing is None and isinstance(node, dict) else None,
        "universeIsOptional": (missing is None and isinstance(node, dict)
                               and "universe" in (node.get("properties") or {})
                               and "universe" not in (node.get("required") or [])) or None,
        "excerpt": json.dumps(node, sort_keys=True)[:260] if missing is None else None,
    })

for label, rel, needle in MD_CITES:
    lines = (S / rel).read_text().splitlines()
    hit = next((i + 1 for i, line in enumerate(lines) if needle in line), None)
    rows.append({"citation": label, "file": rel, "line": hit, "resolved": hit is not None})

print(json.dumps({
    "standing": "Clause-location evidence for the amendment's load-bearing citations only. NOT a "
                "kit census, NOT the 102-file blind kit, and not a claim that any other consumer "
                "boundary is implementable.",
    "citations": rows,
    "allResolved": all(r["resolved"] for r in rows),
    "unresolved": [r["citation"] for r in rows if not r["resolved"]],
}, indent=2, default=str))
