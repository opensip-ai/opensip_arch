"""Custody standing for reuse in runtime source45.v1. It records:
  - the kit delta against my own source44 custody rows (three changed members);
  - an AST census of the helpers that READ each changed member. A helper reads a member when an open/doc/admit/digest/... call receives a string
    literal naming it, or a name bound to one (transitively, across import aliases); a helper that only cites it in label text is not a reader;
  - generic readers that walk every kit document, and whether any unchanged kit document $refs a changed document's $id;
  - helper bytes after the runtime rebind and the source45 edits and new files;
  - byte identity of the stores with the source44.v1 copy (preserved/s44-final/results-manifest.json);
  - which measurements were executed fresh in source45, which were reused as exact prior measurements (and why each is unaffected), and which were
    superseded.
Writes selfcheck/s45-provenance.json and exits 1 if a reuse precondition fails. The census method is unchanged from tools/provenance_s44.py.
Usage: python3 tools/seq.py <label> tools/provenance_s45.py
"""
import ast
import glob
import hashlib
import json
import os
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source45.v1/output/"
KIT = OUT.replace("/output/", "/subject/docs/")


def sha(rel):
    return hashlib.sha256(open(OUT + rel, "rb").read()).hexdigest()


delta_doc = json.load(open(OUT + "s45-kit-delta.json"))
delta = delta_doc["deltaVsOwnSource44Rows"]
members = delta["changed"] + delta["added"]
code = sorted(f"{sub}/{n}" for sub in ("ref", "tools", "builders", "vectors") for n in os.listdir(OUT + sub) if n.endswith(".py"))
RECORDS = {"tools/hc_source39.py", "tools/hc_source41.py", "tools/hc_source42.py", "tools/hc_source43.py", "tools/hc_source44.py", "tools/hc_source45.py",
           "tools/provenance_s44.py", "tools/provenance_s45.py", "tools/finalize_review.py", "tools/checkpoint_p123.py", "tools/result_diffs_s44.py",
           "tools/result_diffs_s45.py"}
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
file_of_stem = {}
for f in code:
    file_of_stem.setdefault(os.path.splitext(os.path.basename(f))[0], f)
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
          "tools/run_preserved_s43.py", "tools/run_unchanged_s44.py", "tools/smoke_s44.py"}
GENERIC_EXPECTED = {"ref/schemas.py": "loads every kit JSON document into the validation registry; results depend only on the selectors resolved",
                    "tools/reference_census.py": "walks every kit JSON document; re-executed fresh in source45",
                    "vectors/phase3_payload_vectors.py": "HC-51 token census over every kit document; re-executed fresh (phase 3)",
                    "vectors/phase3_startup_vectors.py": "pin-document presence check over every kit document; re-executed fresh (phase 3)",
                    "vectors/phase0_custody.py": "custody of every member; re-executed fresh", "tools/final_custody.py": "custody of every member; re-executed fresh",
                    "tools/smoke_schemas.py": "development probe (prints document count); not a measurement"}
non_phase3_readers = {m: [f for f in r if f not in PHASE3] for m, r in readers.items()}
rebind = json.load(open(OUT + "rebind-s45-manifest.json"))
after = {r["file"]: r["afterSha256"] for r in rebind["files"]}
EDITED = {"ref/provider_wire.py": "HC-60", "vectors/phase3_startup_vectors.py": "HC-60", "vectors/phase3_traces.py": "HC-60",
          "tools/checkpoint_p123.py": "HC-60 gating", "tools/checkpoint_p9.py": "source45 records", "tools/final_custody.py": "HC-59",
          "vectors/phase0_custody.py": "HC-59", "tools/finalize_review.py": "source45 standing"}
NEW = {"tools/hc_source45.py", "tools/provenance_s45.py", "tools/result_diffs_s45.py", "tools/run_unchanged_s44.py"}
rows = []
for f in code:
    s = sha(f)
    if f in NEW:
        status = "new in source45"
    elif f in EDITED:
        status = f"edited in source45 ({EDITED[f]})"
    elif f in after:
        status = "rebound only" if s == after[f] else "CHANGED AFTER REBIND"
    else:
        status = "untouched by the rebind and not edited in source45"
    rows.append({"file": f, "sha256": s, "status": status})
unexpected = [r["file"] for r in rows if r["status"] == "CHANGED AFTER REBIND"]
results = json.load(open(OUT + "preserved/s44-final/results-manifest.json"))["files"]
stores = {r["path"]: r["sha256"] for r in results if r["path"].endswith(".store.json")}
store_diffs = [p for p, s in stores.items() if not os.path.exists(OUT + p) or sha(p) != s]
fs = json.load(open(OUT + "runs/from-scratch.summary.json"))
fresh_logs = sorted(os.path.basename(p) for p in glob.glob(OUT + "logs/s45*"))
REUSED = [
    ("phase 1 canonical/CVE1/lexical vectors", "vectors/phase1-canonical.json, vectors/cve1-eight-types.json", "logs/s42v2-cp.1.phase1_canonical.log"),
    ("phase 2 capability-manifest admission", "vectors/capability-manifests.json", "logs/s42v2-cp.2.phase2_capmanifest.log"),
    ("phase 4 tables and phases 5-8 vectors, discovery and mode vectors, run termination", "vectors/*.json (other than reference-census, retention-negatives, graph-query), envelopes/*.json",
     "logs/s42-fin-p4to9.0-.5, .8; logs/s42-fin-disc.0/.1"),
    ("complete positive builds and controls (stores)", "runs/*.store.json", "logs/s42-fin-build.0-.3, logs/s42v2-fin2.0.syntax_runs.log"),
    ("mutation replay of all stores", "runs/replay-all.summary.json", "logs/s42v2-fin2.1.replay_all.log"),
    ("semantic tamper controls", "runs/*.tamper-outputs.json", "logs/s42-fin-tamper.0-.2"),
    ("unchanged-vs-corrected source42 matrix and provenance", "selfcheck/s42-prepost-matrix.json, selfcheck/s42-provenance.json", "logs/s42v2-fin2.5, logs/s42v2-fin2.6"),
    ("process-id nondeterminism of replay outputs (two executions)", "selfcheck/s44-determinism-before.json, selfcheck/s44-determinism-after.json", "logs/s44-det.0-.4")]
reason = ("the helpers behind these measurements read no changed kit member (non-phase-3 AST readers: none). The only generic kit readers are the "
          "validation registry (every unchanged selector resolves as before, because no unchanged kit document references a changed $id) and the fresh "
          "census/custody tools. Helper bytes are the source44 bytes after the runtime-root rebind only, and stores are byte-identical to the source44.v1 copy")
FRESH = [("provider traces and payload/startup vectors (phase 3, corrected HC-60)", "traces/*.json", "logs/s45-p3.0-.2"),
         ("unchanged source44 phase-3 scripts on the source45 kit", "preserved/s45-original/traces/*.json", "logs/s45-original.0-.2"),
         ("from-scratch closure and complete replay of every claimed positive; export replay; admission log; graph query; reference census; retention negatives",
          "runs/from-scratch.summary.json, runs/replay-export.summary.json, runs/phase9-admission-summary.json, vectors/graph-query.json, "
          "vectors/reference-census.json, vectors/retention-negatives.json", "logs/s45-fin.0-.5"),
         ("source44 result-comparison arithmetic reconciliation", "selfcheck/s45-s44-arithmetic-reconciliation.json", "output/reconcile_s44_arithmetic.py (run with python3)"),
         ("classification of every result byte difference from the source44 copy", "selfcheck/s45-result-diffs.json", "logs/s45-fin10.*"),
         ("custody, checkpoints 0-11, provenance, final custody, phases 10-11", "vectors/phase0-custody.json, checkpoints/, selfcheck/s45-provenance.json, runs/final-custody.json",
          "logs/s45-cp.*, logs/s45-fin10.*, logs/s45-fin11.*")]
out = {"kitDelta": delta, "kitManifestSha256": delta_doc["manifestSha256"], "parentSubjectSha256": delta_doc["parentSubjectSha256"],
       "memberReaders": readers, "nonPhase3Readers": non_phase3_readers, "genericKitReaders": {f: GENERIC_EXPECTED.get(f, "UNEXPECTED") for f in generic},
       "changedDocumentIds": changed_ids, "changedIdsReferencedByUnchangedKitDocuments": ref_from_unchanged,
       "helperBytes": rows, "helperChangedAfterRebindUnexpectedly": unexpected,
       "storesComparedToSource44": len(stores), "storeByteDifferences": store_diffs,
       "freshInSource45": {"logs": fresh_logs, "measurements": [{"measurement": m, "artifacts": a, "logs": l} for m, a, l in FRESH],
                           "fromScratchEveryResultMatchesOriginal": fs.get("everyResultMatchesOriginal")},
       "reusedExactPriorMeasurements": [{"measurement": m, "artifacts": a, "logs": l,
                                         "standing": "reused exact prior measurement (source42, or source44 for the determinism probe); not re-executed in source45",
                                         "whyUnaffected": reason} for m, a, l in REUSED],
       "supersededInSource45": [{"measurement": "pre-Analyze host conversion closedWorld (startup-vectors conversion measurement and the unavailable-before-analyze trace conversions)",
                                 "source44": "M-s44-1 determinacy measurement and reading A (logs/s44-p3b.0, logs/s44-p3.2; preserved/s44-final/traces/)",
                                 "source45": "HC-60; logs/s45-original.1/.2 (unchanged), logs/s45-p3.1/.2 (corrected)"}]}
ok = (all(not v for v in non_phase3_readers.values()) and not ref_from_unchanged and all(v != "UNEXPECTED" for v in out["genericKitReaders"].values())
      and not unexpected and not store_diffs)
out["reusePreconditionsHold"] = ok
with open(OUT + "selfcheck/s45-provenance.json", "w") as fh:
    json.dump(out, fh, indent=1, sort_keys=True)
print(json.dumps({k: out[k] for k in ("memberReaders", "nonPhase3Readers", "genericKitReaders", "changedIdsReferencedByUnchangedKitDocuments",
                                      "helperChangedAfterRebindUnexpectedly", "storesComparedToSource44", "storeByteDifferences", "reusePreconditionsHold")}, indent=1))
sys.exit(0 if ok else 1)
