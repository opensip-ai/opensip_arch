#!/usr/bin/env python3
"""Publish, per relation, whether `subject-scope.subjects` are SOURCE PATHS.

Guard A must judge a scope on its own extent where the record supplies one. For `clones` the
subjects ARE source paths, so a README.md-scoped clone request must not be served by an unrelated
`src/plain.rs` elsewhere in the snapshot. For `declares` and the other symbol relations the subjects
are opaque symbol identifiers and the record carries no path association at all, so no per-subject
path law is possible and the coarse extent is the honest fallback.

The values are read from the existing published law, not invented:
  * a relation whose registry `snapshotJoins` names a `pathField` binds its subject to a snapshot
    path (`file`, `vcs-change`);
  * `clones` binds its subject to the body span's source path through `bodyIdentityJoin`
    (`anchorCardinality: 1`, "the body span the identity is over");
  * `package` names a package, not a path;
  * every remaining relation carries `SubjectIdV1` symbol identifiers in its payload.
"""
import json
import sys

WORK = sys.argv[1]
REL = WORK + "/docs/coop/design-corrections/foundation/relation-payload-schemas.v2.json"

# relation -> the kind of identifier its subject-scope subjects carry
SUBJECT_KIND = {
    "file": "source-path",
    "vcs-change": "source-path",
    "clones": "source-path",
    "package": "package-name",
    "declares": "symbol",
    "literal": "symbol",
    "control-flow": "symbol",
    "references": "symbol",
    "imports": "symbol",
    "calls": "symbol",
    "types": "symbol",
    "reachability": "symbol",
    "unresolved-edge": "symbol",
}

raw = open(REL, encoding="utf-8").read()
doc = json.loads(raw)
relations = doc["x-opensip-relation-registry"]["relations"]
missing = sorted(set(relations) - set(SUBJECT_KIND))
if missing:
    sys.exit("no subjectKind for: " + ", ".join(missing))

text = raw
for name in relations:
    kind = SUBJECT_KIND[name]
    anchor = '      "%s": {' % name
    start = text.index(anchor)
    ladder_at = text.index('        "ladder":', start)
    block = '        "subjectKind": %s,\n' % json.dumps(kind)
    text = text[:ladder_at] + block + text[ladder_at:]

doc2 = json.loads(text)
registry = doc2["x-opensip-relation-registry"]
registry["subjectKindLaw"] = (
    "What a subject-scope's `subjects` entries IDENTIFY, per relation. `source-path`: each subject is "
    "a path in the snapshot this scope names, so the scope's own extent is exactly those paths - "
    "`file` and `vcs-change` bind it through their registry snapshotJoins pathField, and `clones` "
    "binds it through bodyIdentityJoin, whose single anchor IS the body span the identity is over. "
    "`package-name`: a package identifier, not a path. `symbol`: an opaque SubjectIdV1 that the "
    "record associates with no path; the enumerator's attribution of symbols to files is trusted and "
    "is NOT re-derivable from the retained Run, so no per-subject path law is possible for these "
    "relations and any capability question about them can only be answered at the coarser retained "
    "extent. That limit is stated rather than worked around: inventing symbol-to-path parsing would "
    "be fabricated evidence."
)
# reorder so the law sits next to the other registry-level laws
out = json.dumps(doc2, indent=2)
open(REL, "w", encoding="utf-8").write(text[: text.index('    "relations": {')]
                                       + '    "subjectKindLaw": %s,\n' % json.dumps(registry["subjectKindLaw"])
                                       + text[text.index('    "relations": {"'.replace('"', '')) if False else text.index('    "relations": {'):])
after = json.load(open(REL))["x-opensip-relation-registry"]
bad = [n for n, r in after["relations"].items() if r.get("subjectKind") != SUBJECT_KIND[n]]
print(json.dumps({"relationsUpdated": len(after["relations"]),
                  "subjectKinds": {n: r["subjectKind"] for n, r in sorted(after["relations"].items())},
                  "mismatches": bad}, indent=2))
sys.exit(1 if bad else 0)
