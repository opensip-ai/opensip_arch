#!/usr/bin/env python3
"""Rewrite the workflow reference fixtures from the withdrawn abstract tier
vocabulary to the actual relation rungs.

The mapping is PER RELATION, which is the whole point: `resolved` names a
different rung in each relation that has one, and names nothing at all in a
relation whose ladder does not have that strength. Nothing is mapped by a global
rule, and any (relation, tier) pair not listed here is a fixture that would have
to be re-authored rather than translated -- the script fails instead of guessing.

Every rewritten instance keeps its position in its relation's ladder, so no
expected policy verdict changes; check_workflows re-verifies that independently.
"""
import json
import os
import sys

WORK = "/tmp/opensip-design-corrections/bv3-corrections-author.v1/work"
DC = os.path.join(WORK, "docs/coop/design-corrections")
CASES = os.path.join(DC, "workflows/workflow-cases.v1.json")

# (relation, withdrawn tier) -> the rung of THAT relation's ladder it named.
MAP = {
    ("imports", "syntax"): "syntactic-specifier",
    ("imports", "resolved"): "resolved-target",
    ("references", "syntax"): "syntactic-name-match",
    ("references", "resolved"): "resolved-binding",
    ("calls", "syntax"): "syntactic-callee-name",
    ("calls", "resolved"): "resolved-callee",
    ("types", "syntax"): "annotated",
    ("types", "type"): "checked",
    ("declares", "syntax"): "syntactic",
    ("literal", "syntax"): "syntactic",
    ("control-flow", "syntax"): "syntactic",
    ("file", "syntax"): "enumerated",
    ("package", "syntax"): "manifest-declared",
    ("vcs-change", "syntax"): "vcs-reported",
    ("reachability", "resolved"): "from-resolved-calls",
    ("clones", "resolved"): "normalized-body-hash",
    # Imported-evidence relations: one rung, the observation itself.
    ("runtime-observation", "syntax"): "observed",
    ("history-change", "syntax"): "observed",
}
TIERS = {"syntax", "resolved", "type", "external"}

rewrites = []
unmapped = []


def convert(node, path=""):
    if isinstance(node, dict):
        relation = node.get("relation")
        for field in ("minResolution", "resolution"):
            value = node.get(field)
            if isinstance(value, str) and value in TIERS:
                if not isinstance(relation, str):
                    unmapped.append({"path": path, "field": field, "value": value,
                                     "why": "no sibling relation to map against"})
                    continue
                key = (relation, value)
                if key not in MAP:
                    unmapped.append({"path": path, "field": field, "relation": relation,
                                     "value": value, "why": "tier names no rung of this ladder"})
                    continue
                node[field] = MAP[key]
                rewrites.append({"path": path, "field": field, "relation": relation,
                                 "from": value, "to": MAP[key]})
        for k, v in node.items():
            convert(v, path + "/" + k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            convert(v, path + "[%d]" % i)


raw = open(CASES, encoding="utf-8").read()
doc = json.loads(raw)
# Reproduce the file's existing serialisation exactly, so the only byte changes
# in the delta are the rewritten values themselves.
if json.dumps(doc, indent=2) + "\n" != raw:
    sys.exit("serialisation does not round-trip; refusing to reformat the fixture")
convert(doc)
if unmapped:
    print(json.dumps({"unmapped": unmapped}, indent=2))
    sys.exit("refusing to guess: unmapped tier instances")

open(CASES, "w", encoding="utf-8").write(json.dumps(doc, indent=2) + "\n")
print(json.dumps({"rewrites": len(rewrites), "detail": rewrites}, indent=2))
