"""Custody standing for reuse in runtime source44.v1. Records:
  - the kit delta against my own source43 custody rows (six changed and three added members);
  - an AST census of the helpers that READ each changed or added member. A helper reads a member when an open/doc/admit/digest/... call receives a string
    literal naming it, or a name bound to one (transitively, across import aliases). A helper that only cites the member in label text is not a reader;
  - generic readers that walk every kit document, and whether any unchanged kit document $refs a changed document's $id;
  - helper bytes after the runtime rebind and the source44 edits and new files;
  - byte identity of stores and every retained result with the source43.v1 copy (preserved/s43-final/results-manifest.json);
  - which measurements were executed fresh in source44, which were reused as exact prior measurements (and why each is unaffected), and which were
    superseded.
Writes selfcheck/s44-provenance.json and exits 1 if a reuse precondition fails.
Usage: python3 tools/seq.py <label> tools/provenance_s44.py
"""
import ast
import glob
import hashlib
import json
import os
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source44.v1/output/"
KIT = OUT.replace("/output/", "/subject/docs/")


def sha(rel):
    return hashlib.sha256(open(OUT + rel, "rb").read()).hexdigest()


delta_doc = json.load(open(OUT + "s44-kit-delta.json"))
delta = delta_doc["deltaVsOwnSource43Rows"]
members = delta["changed"] + delta["added"]
code = sorted(f"{sub}/{n}" for sub in ("ref", "tools", "builders", "vectors") for n in os.listdir(OUT + sub) if n.endswith(".py"))
RECORDS = {"tools/hc_source39.py", "tools/hc_source41.py", "tools/hc_source42.py", "tools/hc_source43.py", "tools/hc_source44.py", "tools/provenance_s44.py",
           "tools/finalize_review.py", "tools/checkpoint_p123.py"}
READ_CALLS = {"open", "doc", "admit", "digest", "resolve_pointer", "validator_for", "stock_errors", "order_violations", "base_uri"}


def forms(member):
    rel = member[len("docs/"):]
    out = {rel}
    if rel.startswith("coop/design-corrections/"):
        out.add(rel[len("coop/design-corrections/"):])
    return out


trees = {f: ast.parse(open(OUT + f, encoding="utf-8").read(), filename=f) for f in code}
aliases = {}
for f, tree in trees.items():
    a = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for al in node.names:
                a[al.asname or al.name] = al.name
    aliases[f] = a
stem_of = {f: os.path.splitext(os.path.basename(f))[0] for f in code}
file_of_stem = {}
for f, s in stem_of.items():
    file_of_stem.setdefault(s, f)
binds = {f: {} for f in code}


def mentions(f, node):
    found = set()
    for sub in ast.walk(node):
        if isinstance(sub, ast.Constant) and isinstance(sub.value, str):
            found |= {m for m in members if any(x in sub.value for x in forms(m))}
        elif isinstance(sub, ast.Name):
            found |= binds[f].get(sub.id, set())
        elif isinstance(sub, ast.Attribute) and isinstance(sub.value, ast.Name) and sub.value.id in aliases[f]:
            target = file_of_stem.get(aliases[f][sub.value.id])
            if target:
                found |= binds[target].get(sub.attr, set())
    return found


grew = True
while grew:
    grew = False
    for f, tree in trees.items():
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                ms = mentions(f, node.value)
                for t in node.targets:
                    if isinstance(t, ast.Name) and not ms <= binds[f].get(t.id, set()):
                        binds[f][t.id] = binds[f].get(t.id, set()) | ms
                        grew = True
readers = {m: [] for m in members}
for f, tree in trees.items():
    if f in RECORDS:
        continue
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            fn = node.func.id if isinstance(node.func, ast.Name) else (node.func.attr if isinstance(node.func, ast.Attribute) else None)
            if fn in READ_CALLS:
                for arg in list(node.args) + [k.value for k in node.keywords]:
                    for m in mentions(f, arg):
                        if f not in readers[m]:
                            readers[m].append(f)
readers = {m: sorted(v) for m, v in readers.items()}
text = {f: open(OUT + f, encoding="utf-8").read() for f in code}
generic = sorted(f for f in code if f not in RECORDS and (("os.walk(" in text[f] and any(k in text[f] for k in ("KIT_DOCS", "os.walk(KIT", "os.walk(SUBJ")))
                                                          or ".docs.items()" in text[f] or "K.docs" in text[f] or "KIT.docs" in text[f]))
changed_ids = {}
# Own tool error in the first run (logs/s44-cp.7.provenance_s44.log): this loop parsed the two changed .md members as JSON. Only JSON members carry $id.
for m in [x for x in members if x.endswith(".json")]:
    doc = json.load(open(KIT + m[len("docs/"):]))
    if isinstance(doc, dict) and isinstance(doc.get("$id"), str):
        changed_ids[m] = doc["$id"]
ref_from_unchanged = []
for d, _, fs in os.walk(KIT):
    for x in fs:
        if x.endswith(".json"):
            rel = "docs/" + os.path.relpath(os.path.join(d, x), KIT)
            if rel in members:
                continue
            raw = open(os.path.join(d, x), encoding="utf-8").read()
            ref_from_unchanged += [(rel, i) for i in changed_ids.values() if i in raw]
PHASE3 = {"ref/factbatch.py", "ref/protocol3.py", "ref/protocol_ts2.py", "ref/provider_wire.py", "ref/provider_exchange.py", "ref/wirecbor.py",
          "vectors/payload_fixtures.py", "vectors/phase3_payload_vectors.py", "vectors/phase3_startup_vectors.py", "vectors/phase3_traces.py",
          "tools/run_preserved_s43.py", "tools/smoke_s44.py"}
GENERIC_EXPECTED = {"ref/schemas.py": "loads every kit JSON document into the validation registry; results depend only on the selectors resolved",
                    "tools/reference_census.py": "walks every kit JSON document; re-executed fresh in source44",
                    "vectors/phase3_payload_vectors.py": "HC-51 token census over every kit document; re-executed fresh (phase 3)",
                    "vectors/phase3_startup_vectors.py": "pin-document presence check over every kit document; re-executed fresh (phase 3)",
                    "vectors/phase0_custody.py": "custody of every member; re-executed fresh", "tools/final_custody.py": "custody of every member; re-executed fresh",
                    "tools/smoke_schemas.py": "development probe (prints document count); not a measurement"}
non_phase3_readers = {m: [f for f in r if f not in PHASE3] for m, r in readers.items()}
rebind = json.load(open(OUT + "rebind-s44-manifest.json"))
after = {r["file"]: r["afterSha256"] for r in rebind["files"]}
EDITED = {"ref/factbatch.py": "HC-57", "ref/protocol3.py": "HC-58", "vectors/payload_fixtures.py": "HC-58", "vectors/phase3_payload_vectors.py": "HC-57",
          "vectors/phase3_traces.py": "HC-58", "tools/checkpoint_p123.py": "HC-57/HC-58 gating", "tools/checkpoint_p9.py": "source44 records",
          "tools/final_custody.py": "HC-56", "vectors/phase0_custody.py": "HC-56", "tools/finalize_review.py": "source44 standing"}
NEW = {"ref/wirecbor.py", "ref/protocol_ts2.py", "ref/provider_wire.py", "ref/provider_exchange.py", "vectors/phase3_startup_vectors.py", "tools/hc_source44.py",
       "tools/provenance_s44.py", "tools/run_preserved_s43.py", "tools/smoke_s44.py", "tools/probe_s44_records.py", "tools/probe_s44_records2.py",
       "tools/determinism_probe_s44.py", "tools/result_diffs_s44.py"}
rows = []
for f in code:
    s = sha(f)
    if f in NEW:
        status = "new in source44"
    elif f in EDITED:
        status = f"edited in source44 ({EDITED[f]})"
    elif f in after:
        status = "rebound only" if s == after[f] else "CHANGED AFTER REBIND"
    else:
        status = "untouched by the rebind and not edited in source44"
    rows.append({"file": f, "sha256": s, "status": status})
unexpected = [r["file"] for r in rows if r["status"] == "CHANGED AFTER REBIND"]
results = json.load(open(OUT + "preserved/s43-final/results-manifest.json"))
res_rows = results["files"]
stores = {r["path"]: r["sha256"] for r in res_rows if r["path"].endswith(".store.json")}
store_diffs = [p for p, s in stores.items() if not os.path.exists(OUT + p) or sha(p) != s]
result_changes = sorted(r["path"] for r in res_rows if not r["path"].endswith(".store.json") and (not os.path.exists(OUT + r["path"]) or sha(r["path"]) != r["sha256"]))
fs = json.load(open(OUT + "runs/from-scratch.summary.json"))
fresh_logs = sorted(os.path.basename(p) for p in glob.glob(OUT + "logs/s44*"))
REUSED = [
    ("phase 1 canonical/CVE1/lexical vectors", "vectors/phase1-canonical.json, vectors/cve1-eight-types.json", "logs/s42v2-cp.1.phase1_canonical.log"),
    ("phase 2 capability-manifest admission", "vectors/capability-manifests.json", "logs/s42v2-cp.2.phase2_capmanifest.log"),
    ("phase 4 tables and phases 5-8 vectors, discovery and mode vectors, run termination", "vectors/*.json (other than reference-census, retention-negatives, graph-query), envelopes/*.json",
     "logs/s42-fin-p4to9.0-.5, .8; logs/s42-fin-disc.0/.1"),
    ("complete positive builds and controls (stores)", "runs/*.store.json", "logs/s42-fin-build.0-.3, logs/s42v2-fin2.0.syntax_runs.log"),
    ("mutation replay of all stores", "runs/replay-all.summary.json", "logs/s42v2-fin2.1.replay_all.log"),
    ("semantic tamper controls", "runs/*.tamper-outputs.json", "logs/s42-fin-tamper.0-.2"),
    ("unchanged-vs-corrected source42 matrix and provenance", "selfcheck/s42-prepost-matrix.json, selfcheck/s42-provenance.json", "logs/s42v2-fin2.5, logs/s42v2-fin2.6")]
reason = ("the helpers behind these measurements read no changed or added kit member (non-phase-3 AST readers: none). The only generic kit readers are the "
          "validation registry (every unchanged selector resolves as before, because no unchanged kit document references a changed $id) and the fresh "
          "census/custody tools. Helper bytes are the source43 bytes after the runtime-root rebind only, and stores are byte-identical to the source43.v1 copy")
FRESH = [("provider traces and payload/startup vectors (phase 3, corrected HC-57/HC-58)", "traces/*.json", "logs/s44-p3.0, logs/s44-p3.2, logs/s44-p3b.0"),
         ("unchanged source43 phase-3 scripts on the source44 kit", "preserved/s44-original/traces/*.json", "logs/s44-original.0/.1"),
         ("from-scratch closure and complete replay of every claimed positive; export replay; admission log", "runs/from-scratch.summary.json, runs/replay-export.summary.json, runs/phase9-admission-summary.json",
          "logs/s44-fin.0-.2"),
         ("graph query (unchanged helper; query owner unchanged)", "vectors/graph-query.json", "logs/s44-fin.3"),
         ("reference census (walks every kit document) and retention/reference-class negatives (consume the census)", "vectors/reference-census.json, vectors/retention-negatives.json",
          "logs/s44-fin.4, logs/s44-fin.5"),
         ("second execution of from-scratch closure, export replay and retention negatives (determinism), and classification of every result byte "
          "difference from the source43 copy", "selfcheck/s44-determinism-before.json, selfcheck/s44-determinism-after.json, selfcheck/s44-result-diffs.json",
          "logs/s44-det.*, logs/s44-diff.*"),
         ("custody, checkpoints 0-11, provenance, final custody, phases 10-11", "vectors/phase0-custody.json, checkpoints/, selfcheck/s44-provenance.json, runs/final-custody.json",
          "logs/s44-cp.*, logs/s44-prov.*, logs/s44-fin10.*, logs/s44-fin11.*")]
out = {"kitDelta": delta, "kitManifestSha256": delta_doc["manifestSha256"], "parentSubjectSha256": delta_doc["parentSubjectSha256"],
       "memberReaders": readers, "nonPhase3Readers": non_phase3_readers, "genericKitReaders": {f: GENERIC_EXPECTED.get(f, "UNEXPECTED") for f in generic},
       "changedDocumentIds": changed_ids, "changedIdsReferencedByUnchangedKitDocuments": ref_from_unchanged,
       "helperBytes": rows, "helperChangedAfterRebindUnexpectedly": unexpected,
       "storesComparedToSource43": len(stores), "storeByteDifferences": store_diffs,
       "retainedResultsChangedSinceSource43Copy": result_changes,
       "freshInSource44": {"logs": fresh_logs, "measurements": [{"measurement": m, "artifacts": a, "logs": l} for m, a, l in FRESH],
                           "fromScratchEveryResultMatchesOriginal": fs.get("everyResultMatchesOriginal")},
       "reusedExactPriorMeasurements": [{"measurement": m, "artifacts": a, "logs": l, "standing": "reused exact source42 measurement (reused in source43.v1); not re-executed in source44",
                                         "whyUnaffected": reason} for m, a, l in REUSED],
       "supersededInSource44": [{"measurement": "provider traces and FactBatch payload vectors (R-TRACE-*)", "source42v3/source43": "logs/s42v3-p3b.0/.1 (reused in source43.v1)",
                                 "source44": "HC-57/HC-58; logs/s44-original.0/.1 (unchanged), logs/s44-p3.*/s44-p3b.0 (corrected)"}]}
ok = (all(not v for v in non_phase3_readers.values()) and not ref_from_unchanged and all(v != "UNEXPECTED" for v in out["genericKitReaders"].values())
      and not unexpected and not store_diffs)
out["reusePreconditionsHold"] = ok
with open(OUT + "selfcheck/s44-provenance.json", "w") as fh:
    json.dump(out, fh, indent=1, sort_keys=True)
print(json.dumps({k: out[k] for k in ("memberReaders", "nonPhase3Readers", "genericKitReaders", "changedIdsReferencedByUnchangedKitDocuments",
                                      "helperChangedAfterRebindUnexpectedly", "storesComparedToSource43", "storeByteDifferences",
                                      "retainedResultsChangedSinceSource43Copy", "reusePreconditionsHold")}, indent=1))
sys.exit(0 if ok else 1)
