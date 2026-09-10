#!/usr/bin/env python
"""Governance-record cross-reference resolution + register preservation.

A. Scan every {path, sha256} pair in the v17 governance records and check that
   the named file exists in the frozen subject and hashes to the named digest.
   Records that describe a DISPOSABLE COPY against a different base manifest are
   scoped out explicitly (that mis-scoping caused a false positive in v16).
B. Registers: 16 AR, 15 FW, 27 inherited residuals, 30 evaluation subresiduals,
   5 DR-201..205 scoped review owners, 32 qualification gates - counted from the
   owning documents, and their preservation checked against the v16 bytes.
"""
import hashlib
import json
import os
import re
import sys

ROOT = "/tmp/opensip-design-corrections/candidate-subject.v17"
V16 = "/tmp/opensip-design-corrections/post-reset-review.v17/copies/v16-extract"
DC = os.path.join(ROOT, "docs/coop/design-corrections")
OUT = sys.argv[1]

# Governance records to scan (v17 generation only)
RECORDS = [
    "docs/coop/design-corrections/post-reset-dispositions.v17.proposed.json",
    "docs/coop/design-corrections/reviews/codex-post-reset.v1/successor-source-assessment.v17.json",
    "docs/coop/design-corrections/reviews/codex-post-reset.v1/blind-assessment.v6.json",
    "docs/coop/design-corrections/reviews/codex-post-reset.v1/final-reference.v17/reference-checks.json",
    "docs/coop/design-corrections/historical-preservation-report.v17.json",
    "docs/coop/design-corrections/correction-crosswalk.proposed.json",
    "docs/coop/design-corrections/reviews/bv6-corrections-author.v6/handoff.json",
    "docs/coop/design-corrections/reviews/bv6-corrections-author.v6/custody.json",
]


def sha_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for b in iter(lambda: fh.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()


HEX64 = re.compile(r"^[0-9a-f]{64}$")
rep = {"crossReferences": []}
resolved = unresolved = scoped_out = 0
problems = []


def scan(obj, record, ptr=""):
    """Find dicts carrying both a path-ish key and a sha256-ish key."""
    global resolved, unresolved, scoped_out
    if isinstance(obj, dict):
        pk = next((k for k in ("path", "file", "source") if k in obj
                   and isinstance(obj[k], str)), None)
        sk = next((k for k in ("sha256", "fileSha256", "sourceSha256",
                               "afterSha256", "digest")
                   if k in obj and isinstance(obj[k], str)
                   and HEX64.match(obj[k])), None)
        if pk and sk:
            path, sha = obj[pk], obj[sk]
            # Scope-out: rows that describe a disposable copy or a prior version
            scope_note = None
            if obj.get("baseManifestSha256") and \
               obj["baseManifestSha256"] != \
               "8cfe6d20a7d49b819f7c2eb2578afcaa5037048ed290ff1867fdcd6789cf3a9c":
                scope_note = "describes a copy against a different base manifest"
            if "beforeSha256" in obj and sk == "afterSha256":
                pass  # after must resolve
            for cand in (path, os.path.join("docs/coop/design-corrections", path)):
                full = os.path.join(ROOT, cand)
                if os.path.isfile(full):
                    actual = sha_file(full)
                    ok = actual == sha
                    if scope_note and not ok:
                        scoped_out += 1
                        return
                    if ok:
                        resolved += 1
                    else:
                        unresolved += 1
                        problems.append({
                            "record": record, "pointer": ptr,
                            "path": cand, "declared": sha, "actual": actual,
                            "key": sk, "scopeNote": scope_note})
                    break
            else:
                # file not found under either root
                if scope_note:
                    scoped_out += 1
                else:
                    unresolved += 1
                    problems.append({"record": record, "pointer": ptr,
                                     "path": path, "declared": sha,
                                     "actual": None, "key": sk,
                                     "problem": "path not found in subject"})
        for k, v in obj.items():
            scan(v, record, ptr + "/" + str(k))
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            scan(v, record, ptr + "/" + str(i))


for rel in RECORDS:
    p = os.path.join(ROOT, rel)
    if not os.path.isfile(p):
        rep["crossReferences"].append({"record": rel, "present": False})
        continue
    with open(p) as fh:
        doc = json.load(fh)
    scan(doc, rel)

rep["xrefResolved"] = resolved
rep["xrefUnresolved"] = unresolved
rep["xrefScopedOut"] = scoped_out
rep["xrefProblems"] = problems
rep["allGovernanceXrefsResolve"] = unresolved == 0

# ---------------- registers ----------------
def T(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


reg = {}

# qualification gates
qg = json.load(open(os.path.join(DC, "qualification-gates.proposed.json")))
gates = None
for k, v in qg.items():
    if isinstance(v, list) and v and isinstance(v[0], dict):
        gates = v
        reg["qualificationGatesKey"] = k
        break
if gates is not None:
    reg["qualificationGateCount"] = len(gates)
    reg["gatesDemonstratedTrue"] = [g for g in gates if g.get("demonstrated")]
    reg["gatesQualifiedTrue"] = [g for g in gates if g.get("qualified")]
    reg["allGatesUnperformed"] = (
        not reg["gatesDemonstratedTrue"] and not reg["gatesQualifiedTrue"])

# inherited residuals
ir = T(os.path.join(DC, "inherited-residuals.proposed.md"))
reg["inheritedResidualDRRows"] = sorted(set(re.findall(r"DR-0\d{2}(?:-R\d{2})?", ir)))
reg["inheritedResidualRowCount"] = len(reg["inheritedResidualDRRows"])
reg["dr011RRows"] = sorted(set(re.findall(r"DR-011-R\d{2}", ir)))
reg["dr011RRowCount"] = len(reg["dr011RRows"])

# evaluation subresiduals
ev = json.load(open(os.path.join(DC, "evaluation-residual-dispositions.proposed.json")))
evl = None
for k, v in ev.items():
    if isinstance(v, list) and v and isinstance(v[0], dict):
        evl = v
        reg["evaluationSubresidualKey"] = k
        break
reg["evaluationSubresidualCount"] = len(evl) if evl is not None else None

# scoped review owners DR-201..205
allsrc = {}
for base, sub in ((DC, ""),):
    for dp, dn, fns in os.walk(base):
        if "reviews" in dp.split(os.sep):
            continue
        for fn in fns:
            if fn.endswith((".md", ".json")):
                try:
                    allsrc[os.path.join(dp, fn)] = T(os.path.join(dp, fn))
                except Exception:
                    pass
dr2 = {}
for f, t in allsrc.items():
    for m in set(re.findall(r"DR-20[1-5]", t)):
        dr2.setdefault(m, []).append(os.path.relpath(f, ROOT))
reg["dr201to205Found"] = sorted(dr2)
reg["dr201to205Count"] = len(dr2)
reg["dr201to205Files"] = {k: v[:4] for k, v in sorted(dr2.items())}

# AR / FW rows: count and check the owning documents' preservation vs v16
cw = json.load(open(os.path.join(DC, "correction-crosswalk.proposed.json")))
items = cw.get("items", [])
reg["crosswalkItemCount"] = len(items)
ar_ids = sorted({i.get("id") for i in items
                 if isinstance(i.get("id"), str) and i["id"].startswith("AR-")})
fw_ids = sorted({i.get("id") for i in items
                 if isinstance(i.get("id"), str) and i["id"].startswith("FW-")})
reg["arIdsInCrosswalk"] = ar_ids
reg["fwIdsInCrosswalk"] = fw_ids

# FW rows live in current-source-map.proposed.md; AR rows in the depth review
csm_p = os.path.join(DC, "current-source-map.proposed.md")
csm = T(csm_p)
reg["fwRowsInSourceMap"] = sorted(set(re.findall(r"FW-\d+", csm)))
reg["fwRowCount"] = len(reg["fwRowsInSourceMap"])
csm_v16 = os.path.join(V16, "docs/coop/design-corrections/current-source-map.proposed.md")
reg["sourceMapByteIdenticalToV16"] = (
    os.path.isfile(csm_v16)
    and sha_file(csm_v16) == sha_file(csm_p))

ar_doc_p = os.path.join(ROOT, "docs/coop/architecture-depth-review/REVIEW.md")
if os.path.isfile(ar_doc_p):
    ar_doc = T(ar_doc_p)
    reg["arRowsInDepthReview"] = sorted(set(re.findall(r"AR-\d+", ar_doc)))
    reg["arRowCount"] = len(reg["arRowsInDepthReview"])

# inherited residual owning doc preservation
for rel in ("inherited-residuals.proposed.md",
            "evaluation-residual-dispositions.proposed.json",
            "qualification-gates.proposed.json",
            "inherited-row-sources.proposed.json"):
    a = os.path.join(V16, "docs/coop/design-corrections", rel)
    b = os.path.join(DC, rel)
    if os.path.isfile(a) and os.path.isfile(b):
        reg["byteIdenticalToV16:" + rel] = sha_file(a) == sha_file(b)

# D-372 / condition 5
readme = T(os.path.join(DC, "README.md"))
reg["readmeMentionsD372Unapplied"] = bool(
    re.search(r"D-372 has not been applied", readme))
m = re.search(r"[^\n]*D-372[^\n]*", readme)
reg["d372Sentence"] = m.group(0)[:400] if m else None
cond = re.findall(r"[^\n]*condition 5[^\n]*", readme, re.I)
reg["condition5Sentences"] = cond[:4]

rep["registers"] = reg
with open(OUT, "w") as fh:
    json.dump(rep, fh, indent=1, sort_keys=True, default=str)

print("xref resolved:", resolved, "unresolved:", unresolved,
      "scopedOut:", scoped_out)
for p in problems[:20]:
    print("   PROBLEM:", json.dumps(p)[:300])
print()
for k in sorted(reg):
    if k in ("dr201to205Files", "gatesDemonstratedTrue", "gatesQualifiedTrue"):
        continue
    print("  %-46s %s" % (k, json.dumps(reg[k])[:190]))
