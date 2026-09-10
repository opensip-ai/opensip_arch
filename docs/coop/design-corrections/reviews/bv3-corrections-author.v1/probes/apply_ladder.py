#!/usr/bin/env python3
"""Insert the explicit ordered `ladder` array into every foundation relation
registry row, immediately before that row's `rungs` field-rule table.

The ladder VALUES are not authored here: they are read from the inherited
docs/coop/artifacts/fact-plane.v1.json#/relationRegistry/relations[].ladder,
plus native-evidence section 4.4's `unresolved-edge: [observed]`, which is the
one relation the successor registry adds. Nothing is invented; the drift checks
added alongside prove the inherited value and every mirror still agree in order.

Edits the text with exact indentation rather than re-serialising, so the rest of
the document's bytes are untouched.
"""
import json
import os
import re
import sys

WORK = "/tmp/opensip-design-corrections/bv3-corrections-author.v1/work"
DC = os.path.join(WORK, "docs/coop/design-corrections")
REL = os.path.join(DC, "foundation/relation-payload-schemas.v2.json")
FACT_PLANE = os.path.join(WORK, "docs/coop/artifacts/fact-plane.v1.json")

inherited = {
    name: row["ladder"]
    for name, row in json.load(open(FACT_PLANE))["relationRegistry"]["relations"].items()
}
inherited["unresolved-edge"] = ["observed"]

text = open(REL, encoding="utf-8").read()
doc = json.loads(text)
relations = doc["x-opensip-relation-registry"]["relations"]

missing = sorted(set(relations) - set(inherited))
if missing:
    sys.exit("no inherited ladder for: " + ", ".join(missing))

inserted = []
for name in relations:
    ladder = inherited[name]
    # Anchor on this relation's own block so the right `rungs` line is matched.
    anchor = '      "%s": {' % name
    start = text.index(anchor)
    rungs_at = text.index('        "rungs":', start)
    body = ",\n".join('          %s' % json.dumps(r) for r in ladder)
    block = '        "ladder": [\n%s\n        ],\n' % body
    text = text[:rungs_at] + block + text[rungs_at:]
    inserted.append({"relation": name, "ladder": ladder})

open(REL, "w", encoding="utf-8").write(text)

# Re-parse and prove the insertion is exactly the inherited ladder, in order.
after = json.load(open(REL))["x-opensip-relation-registry"]["relations"]
bad = [n for n in after if after[n].get("ladder") != inherited[n]]
print(json.dumps({
    "relationsUpdated": len(inserted),
    "ladders": {n: after[n]["ladder"] for n in sorted(after)},
    "orderMismatchesVsInherited": bad,
}, indent=2))
sys.exit(1 if bad else 0)
