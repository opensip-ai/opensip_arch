#!/usr/bin/env python3
"""P3: measure the impact of tightening foundation Blob.path to the logical-path
grammar the identity contract already states, before deciding to do it.

Foundation `Blob` is referenced by exactly three descriptors: closure `tree`,
`import.blobs` and `source-inventory`. The contract says logical paths carry the
grammar; the schema does not enforce it anywhere, and the closure checker patches
it imperatively for scope-descriptor only. This probe collects every path value
that would flow through those three descriptors in the live corpora and reports
which would newly refuse.
"""
import json
import os
import re
import sys

WORK = os.environ.get(
    "OPENSIP_WORK",
    "/tmp/opensip-design-corrections/bv3-corrections-author.v1/work",
)
DC = os.path.join(WORK, "docs/coop/design-corrections")

# Exactly the workflow common#/$defs/LogicalPath constraints.
SEGMENT = re.compile(r"^[^/\\\x00]{1,255}(/[^/\\\x00]{1,255})*\Z")
DOTSEG = re.compile(r"(^|/)\.\.?(/|$)")


def lawful(path):
    return (
        isinstance(path, str)
        and 1 <= len(path) <= 4096
        and bool(SEGMENT.match(path))
        and not DOTSEG.search(path)
    )


def collect(node, out, path=""):
    """Any object shaped exactly like a Blob row is a candidate."""
    if isinstance(node, dict):
        if set(node) == {"path", "sha256", "bytes"}:
            out.append((path, node["path"]))
        for k, v in node.items():
            collect(v, out, path + "/" + k)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            collect(v, out, path + "[%d]" % i)


def main():
    rows = []
    for rel in ("native/native-cases.v2.json", "workflows/workflow-cases.v1.json",
                "native/native-evidence-report.v2.json",
                "foundation/identity-report.json", "integration-fixtures.py"):
        full = os.path.join(DC, rel)
        if not os.path.exists(full) or not rel.endswith(".json"):
            continue
        collect(json.load(open(full)), rows, rel)
    unlawful = [(p, v) for p, v in rows if not lawful(v)]
    report = {
        "blobRowsFound": len(rows),
        "distinctPaths": sorted({v for _, v in rows})[:40],
        "wouldNewlyRefuse": unlawful,
        "verdict": "SAFE" if not unlawful else "BREAKS-EXISTING",
    }
    print(json.dumps(report, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
