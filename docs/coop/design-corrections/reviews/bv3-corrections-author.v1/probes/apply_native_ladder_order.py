#!/usr/bin/env python3
"""Reorder RELATION-LADDER-DOMAIN-V2.ladders to weakest-first, matching the
foundation ladder authority exactly.

The arrays were alphabetised while still declaring
`fact-plane.v1#relationRegistry.relations[].ladder` as their source, which
reverses calls, imports and references relative to the ladder they name. Only
the ITEM ORDER inside each array changes; membership, keys, formatting and every
other byte of the document are preserved.
"""
import json
import os
import re
import sys

WORK = "/tmp/opensip-design-corrections/bv3-corrections-author.v1/work"
DC = os.path.join(WORK, "docs/coop/design-corrections")
DOM = os.path.join(DC, "native/capability-manifest-domains.v2.json")
AUTH = os.path.join(DC, "foundation/relation-payload-schemas.v2.json")

authority = {
    name: row["ladder"]
    for name, row in json.load(open(AUTH))["x-opensip-relation-registry"]["relations"].items()
}

text = open(DOM, encoding="utf-8").read()
before = json.loads(text)["registries"]["RELATION-LADDER-DOMAIN-V2"]["ladders"]

start = text.index('"RELATION-LADDER-DOMAIN-V2"')
lad_at = text.index('"ladders": {', start)
end = text.index('\n      "rule":', lad_at)
segment = text[lad_at:end]

new_segment = segment
for name, ladder in before.items():
    if sorted(ladder) != sorted(authority[name]):
        sys.exit("membership differs for %s: %r vs %r" % (name, ladder, authority[name]))
    if ladder == authority[name]:
        continue
    old_block = '"%s": [\n%s\n        ]' % (
        name, ",\n".join('          "%s"' % r for r in ladder))
    new_block = '"%s": [\n%s\n        ]' % (
        name, ",\n".join('          "%s"' % r for r in authority[name]))
    if old_block not in new_segment:
        sys.exit("could not locate block for " + name)
    new_segment = new_segment.replace(old_block, new_block, 1)

text = text[:lad_at] + new_segment + text[end:]
open(DOM, "w", encoding="utf-8").write(text)

after = json.load(open(DOM))["registries"]["RELATION-LADDER-DOMAIN-V2"]["ladders"]
mismatch = [n for n in after if after[n] != authority[n]]
print(json.dumps({
    "reordered": [n for n in before if before[n] != after[n]],
    "membershipUnchanged": all(sorted(before[n]) == sorted(after[n]) for n in before),
    "mismatchVsAuthority": mismatch,
}, indent=2))
sys.exit(1 if mismatch else 0)
