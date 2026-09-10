"""Requirement 3: were older injected-complete vectors made COHERENT or merely weakened?

RC-6 now refuses coverage=complete with examinedExhaustive!=true. Any pre-existing
hostile vector that injected coverage=complete to reach a DEEPER refusal would now
stop at RC-6, silently losing its original target. The correct repair is to set
examinedExhaustive=true so the hostile claim is internally coherent and the deeper
guard is still reached; the wrong repair is to drop the complete claim.

This finds every case injecting coverage=complete, reports the refusal it targets,
and whether it carries examinedExhaustive=true.
"""
import json
import sys

ROOT = sys.argv[1]
cases = json.load(open(
    ROOT + "/docs/coop/design-corrections/native/native-cases.v2.json"))["cases"]


def walk(o):
    if isinstance(o, dict):
        yield o
        for v in o.values():
            yield from walk(v)
    elif isinstance(o, list):
        for v in o:
            yield from walk(v)


rows = []
for c in cases:
    complete_nodes = [n for n in walk(c) if n.get("coverage") == "complete"]
    if not complete_nodes:
        continue
    # does the same record carry an examined-exhaustive claim?
    states = []
    for n in complete_nodes:
        rc = n.get("resolutionCompleteness")
        if isinstance(rc, dict):
            states.append(rc.get("examinedExhaustive"))
        else:
            states.append("no-rc-sibling")
    errs = [s.get("expectError") for s in c.get("steps", [])
            if isinstance(s, dict) and s.get("expectError")]
    errs = [e for e in errs if e]
    rows.append({
        "id": c.get("id"),
        "kind": c.get("kind"),
        "completeNodes": len(complete_nodes),
        "examinedExhaustiveValues": states,
        "expectErrors": errs,
        "targetsRC6": any("RC-6" in str(e) or "rc6" in str(e).lower()
                          for e in errs),
    })

incoherent = [r for r in rows
              if r["kind"] == "negative" and not r["targetsRC6"]
              and any(v is not True for v in r["examinedExhaustiveValues"]
                      if v != "no-rc-sibling")]

print(json.dumps({
    "casesInjectingCompleteCoverage": len(rows),
    "rows": rows,
    "negativeVectorsThatWouldNowStopAtRC6": [r["id"] for r in incoherent],
    "allDeeperVectorsCoherent": not incoherent,
}, indent=2))
