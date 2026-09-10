#!/usr/bin/env python
"""Re-derive every headline count in technical-review.v17.md from the reports
that this review actually EXECUTED in the disposable copy. Any figure I cannot
re-derive is reported as unverified rather than restated.
"""
import json
import os
import re
import sys

COPY = "/tmp/opensip-design-corrections/post-reset-review.v17/copies/copy-A-reference-run"
DC = os.path.join(COPY, "docs/coop/design-corrections")

DECLARED = {
    "foundation.checksPassed": 1694,
    "foundation.sourcePinsVerified": 1099,
    "foundation.components.foundation": 231,
    "foundation.components.identity": 1346,
    "foundation.components.product-quality": 24,
    "foundation.components.product-configuration": 28,
    "foundation.components.array-order": 65,
    "identity.passingCalls": 1346,
    "identity.distinctIds": 1334,
    "identity.duplicateExtraInstances": 12,
    "security.casesPassed": 456,
    "security.invariantSweepsPassed": 10,
    "native.casesPassed": 355,
    "native.matrixCells": 66,
    "native.qualifiedCells": 0,
    "workflows.checksPassed": 1787,
    "workflows.commands": 45,
    "workflows.goldens": 43,
    "integration.checksPassed": 392,
}


def L(p):
    with open(p) as fh:
        return json.load(fh)


def main():
    out = sys.argv[1]
    measured = {}
    notes = {}

    # ---- foundation ----
    f = L(os.path.join(DC, "foundation/validation-report.json"))
    measured["foundation.sourcePinsVerified"] = f["sourceFileCount"]
    comp = {}
    total = 0
    for c in f["checks"]:
        m = re.search(r'"passed":\s*(\d+)', c["stdout"])
        n = int(m.group(1)) if m else None
        key = c["script"].replace("check-", "").replace(".py", "")
        comp[key] = n
        if n:
            total += n
    measured["foundation.componentsMeasured"] = comp
    measured["foundation.checksPassedSum"] = total

    # ---- identity report: passing calls / distinct ids ----
    ip = os.path.join(DC, "foundation/identity-report.json")
    if os.path.isfile(ip):
        ident = L(ip)
        notes["identityReportTopKeys"] = list(ident.keys())[:20]
        # find the list of check records
        recs = None
        for k, v in ident.items():
            if isinstance(v, list) and v and isinstance(v[0], dict):
                recs = v
                notes["identityRecordsKey"] = k
                notes["identityRecordSample"] = {
                    kk: (str(vv)[:60]) for kk, vv in v[0].items()}
                break
        if recs is not None:
            passing = [r for r in recs
                       if r.get("ok", r.get("passed", True)) not in (False,)]
            measured["identity.records"] = len(recs)
            measured["identity.passingCalls"] = len(passing)
            idkeys = [r.get("id") for r in passing if r.get("id") is not None]
            measured["identity.idsPresent"] = len(idkeys)
            measured["identity.distinctIds"] = len(set(idkeys))
            measured["identity.duplicateExtraInstances"] = \
                len(idkeys) - len(set(idkeys))

    # ---- security ----
    s = L(os.path.join(DC, "security/security-lifecycle-report.v1.json"))
    notes["securityTopKeys"] = list(s.keys())
    for k, v in s.items():
        if isinstance(v, int):
            measured["security." + k] = v

    # ---- native ----
    n = L(os.path.join(DC, "native/native-evidence-report.v2.json"))
    notes["nativeTopKeys"] = list(n.keys())
    for k, v in n.items():
        if isinstance(v, int):
            measured["native." + k] = v
        elif isinstance(v, list):
            measured["native.len." + k] = len(v)

    # ---- workflows validation ----
    w = L(os.path.join(DC, "workflows/workflows-validation-report.json"))
    notes["workflowsTopKeys"] = list(w.keys())
    for k, v in w.items():
        if isinstance(v, int):
            measured["workflows." + k] = v
        elif isinstance(v, list):
            measured["workflows.len." + k] = len(v)

    # ---- workflow surface ----
    ws = L(os.path.join(DC, "workflows/workflows-report.v1.json"))
    notes["workflowSurfaceTopKeys"] = list(ws.keys())
    for k, v in ws.items():
        if isinstance(v, int):
            measured["workflowSurface." + k] = v

    # ---- integration ----
    i = L(os.path.join(DC, "integration-report.v1.json"))
    notes["integrationTopKeys"] = list(i.keys())
    for k, v in i.items():
        if isinstance(v, int):
            measured["integration." + k] = v

    rep = {"declaredHeadline": DECLARED, "measured": measured, "notes": notes}
    with open(out, "w") as fh:
        json.dump(rep, fh, indent=1, sort_keys=True, default=str)
    print(json.dumps(rep, indent=1, sort_keys=True, default=str))


if __name__ == "__main__":
    main()
