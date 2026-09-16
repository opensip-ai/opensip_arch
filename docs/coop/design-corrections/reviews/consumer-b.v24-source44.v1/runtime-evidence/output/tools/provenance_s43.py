"""Custody standing for reuse in runtime source43.v1. Records:
  - the kit delta against my own source42 custody rows and every helper that names the changed member;
  - which helpers read kit prose (.md) at all;
  - helper bytes after the runtime rebind, the source43 edits and the new files;
  - byte identity of the exported stores with the source42.v3 copy;
  - the table of measurements executed fresh in source43 versus reused as exact source42 measurements, with the reason each reuse is
    unaffected.
Writes selfcheck/s43-provenance.json and exits 1 if a reuse precondition fails.
Usage: python3 tools/runref.py tools/provenance_s43.py
"""
import glob
import hashlib
import json
import os
import re
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source44.v1/output/"


def sha(rel):
    return hashlib.sha256(open(OUT + rel, "rb").read()).hexdigest()


delta = json.load(open(OUT + "s43-kit-delta.json"))
changed = delta["deltaVsOwnSource42Rows"]["changed"]
code = sorted(f"{sub}/{n}" for sub in ("ref", "tools", "builders", "vectors") for n in os.listdir(OUT + sub) if n.endswith(".py"))
text = {f: open(OUT + f, encoding="utf-8").read() for f in code}
kit_rows = json.load(open(OUT.replace("/output/", "/subject/") + "consumer-input-manifest.json"))["files"]


def readers_of(member):
    """Files that READ the bytes of a kit member: a line calling open() names the member's docs-relative path, or names a variable bound (transitively,
    by assignment lines) to it. A file that only cites the path in text (records, notes, labels) names it but does not read it.
    Own tool error in the first s43-prov run (logs/s43-prov.0.provenance_s43.log): the census counted every textual mention as a reader and every
    .md open, including charter.md which is not a kit member."""
    rel = member[len("docs/"):] if member.startswith("docs/") else member
    out = {"reads": [], "namesOnly": []}
    for f in code:
        if f == "tools/provenance_s43.py" or rel not in text[f]:
            continue
        lines = text[f].split("\n")
        names = set()
        grew = True
        while grew:
            grew = False
            for line in lines:
                m = re.match(r"\s*([A-Za-z_][A-Za-z0-9_]*)\s*=[^=]", line)
                if m and m.group(1) not in names and (rel in line or any(re.search(rf"\b{re.escape(n)}\b", line.split("=", 1)[1]) for n in names)):
                    names.add(m.group(1))
                    grew = True
        reads = any("open(" in line and (rel in line or any(re.search(rf"\b{re.escape(n)}\b", line) for n in names)) for line in lines)
        out["reads" if reads else "namesOnly"].append(f)
    return out


consumer_census = {p: readers_of(p) for p in changed}
consumers = {p: c["reads"] for p, c in consumer_census.items()}
md_census = {r["path"]: readers_of(r["path"]) for r in kit_rows if r["path"].endswith(".md")}
md_readers = sorted({f for c in md_census.values() for f in c["reads"]})
md_read_members = {p: c["reads"] for p, c in md_census.items() if c["reads"]}
kit_loader_json_only = "if not f.endswith('.json')" in text["ref/schemas.py"]
rebind = json.load(open(OUT + "rebind-s43-manifest.json"))
after = {r["file"]: r["afterSha256"] for r in rebind["files"]}
EDITED = {"tools/phase9_graph_query.py": "HC-54", "tools/final_custody.py": "HC-55", "vectors/phase0_custody.py": "HC-55",
          "tools/checkpoint_p9.py": "HC-54 gating", "tools/finalize_review.py": "source43 standing"}
NEW = {"tools/hc_source43.py", "tools/provenance_s43.py", "tools/summarize_s43_query.py"}
rows = []
for f in code:
    s = sha(f)
    if f in NEW:
        status = "new in source43"
    elif f in EDITED:
        status = f"edited in source43 ({EDITED[f]})"
    elif f in after:
        status = "rebound only" if s == after[f] else "CHANGED AFTER REBIND"
    else:
        status = "untouched by the rebind and not edited in source43"
    rows.append({"file": f, "sha256": s, "status": status})
unexpected = [r["file"] for r in rows if r["status"] == "CHANGED AFTER REBIND"]
runs_manifest = json.load(open(OUT + "preserved/s42-v3-final/runs-manifest.json"))
stores = {r["path"]: r["sha256"] for r in runs_manifest["files"] if r["path"].endswith(".store.json")}
store_diffs = [p for p, s in stores.items() if not os.path.exists(OUT + p) or sha(p) != s]
fs = json.load(open(OUT + "runs/from-scratch.summary.json"))
fresh_logs = sorted(os.path.basename(p) for p in glob.glob(OUT + "logs/s43*"))
REUSED = [
    ("phase 1 canonical/CVE1/lexical vectors", "vectors/phase1-canonical.json, vectors/cve1-eight-types.json", "logs/s42v2-cp.1.phase1_canonical.log"),
    ("phase 2 capability-manifest admission", "vectors/capability-manifests.json", "logs/s42v2-cp.2.phase2_capmanifest.log"),
    ("phase 3 traces and FactBatch payload vectors", "traces/*.json", "logs/s42v3-p3b.0.phase3_payload_vectors.log, logs/s42v3-p3b.1.phase3_traces.log"),
    ("phase 4 tables and phases 5-8 vectors, discovery and mode vectors, run termination", "vectors/*.json, envelopes/*.json",
     "logs/s42-fin-p4to9.0-.5, .8, .10; logs/s42-fin-disc.0/.1"),
    ("complete positive builds and controls (stores)", "runs/*.store.json", "logs/s42-fin-build.0-.3, logs/s42v2-fin2.0.syntax_runs.log"),
    ("mutation replay of all stores", "runs/replay-all.summary.json", "logs/s42v2-fin2.1.replay_all.log"),
    ("semantic tamper controls", "runs/*.tamper-outputs.json", "logs/s42-fin-tamper.0-.2"),
    ("retention/reference-class negatives and census", "vectors/retention-negatives.json, vectors/reference-census.json", "logs/s42-fin-neg.0, logs/s42-fin-p4to9.10"),
    ("unchanged-vs-corrected source42 matrix and provenance", "selfcheck/s42-prepost-matrix.json, selfcheck/s42-provenance.json", "logs/s42v2-fin2.5, logs/s42v2-fin2.6")]
reason = ("these helpers read only kit JSON documents (ref/schemas.py loads *.json) and my retained stores; every changed kit member is prose "
          f"({changed}), whose only helper consumer is {consumers}; helper bytes are the source42 bytes after the runtime-root rebind only; stores are "
          "byte-identical to the source42.v3 copy")
out = {"kitDelta": delta["deltaVsOwnSource42Rows"], "kitManifestSha256": delta["manifestSha256"], "parentSubjectSha256": delta["parentSubjectSha256"],
       "changedMembersAllProse": all(p.endswith(".md") for p in changed), "changedMemberConsumers": consumers, "changedMemberCensus": consumer_census,
       "kitProseReaders": md_readers, "kitProseMembersRead": md_read_members,
       "kitProseMembersReadUnchanged": all(p not in changed or readers == ["tools/phase9_graph_query.py"] for p, readers in md_read_members.items()),
       "kitLoaderJsonOnly": kit_loader_json_only, "helperBytes": rows, "helperChangedAfterRebindUnexpectedly": unexpected,
       "storesComparedToSource42v3": len(stores), "storeByteDifferences": store_diffs,
       "freshInSource43": {"logs": fresh_logs, "fromScratchEveryResultMatchesSource42": fs.get("everyResultMatchesOriginal")},
       "reusedExactSource42Measurements": [{"measurement": m, "artifacts": a, "logs": l, "standing": "reused exact source42 measurement; not re-executed in source43",
                                            "whyUnaffected": reason} for m, a, l in REUSED],
       "supersededInSource43": [{"measurement": "graph query (R-GRAPH-QUERY-OPERATION-DISCLOSURE-CURSOR)", "source42": "logs/s42-fin-p4to9.6.phase9_graph_query.log",
                                 "source43": "logs/s43-original.0 (unchanged helper), logs/s43-hc54.0 (own control error), logs/s43-hc54b.0 (corrected)"}]}
ok = (out["changedMembersAllProse"] and kit_loader_json_only and consumers == {p: ["tools/phase9_graph_query.py"] for p in changed}
      and set(md_readers) <= {"vectors/phase0_custody.py", "tools/phase9_graph_query.py"} and out["kitProseMembersReadUnchanged"]
      and not unexpected and not store_diffs)
out["reusePreconditionsHold"] = ok
with open(OUT + "selfcheck/s43-provenance.json", "w") as fh:
    json.dump(out, fh, indent=1, sort_keys=True)
print(json.dumps({k: out[k] for k in ("changedMembersAllProse", "changedMemberConsumers", "kitProseReaders", "kitLoaderJsonOnly",
                                      "helperChangedAfterRebindUnexpectedly", "storesComparedToSource42v3", "storeByteDifferences", "reusePreconditionsHold")}, indent=1))
sys.exit(0 if ok else 1)
