"""Author-02 mutation run (authoring evidence, not part of the claimed reference closure).
Each mutant copies the candidate into work/mutants/<id>, applies one exact once-only source replacement, and runs check.py in trace mode
(the subject manifest is intentionally not consulted there). A mutant is KILLED when the check exits non-zero.
Run: cd work && TMPDIR=$PWD PY -I -B mutants.py [ids...]
"""
import json
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
CAND = HERE.parent / "candidate"
PY = "/tmp/opensip-implementation/metadata-reference-env/bin/python"
ARCH = "/Users/sb/code/opensip-ai/opensip_arch"
MUTANTS = [
    {"id": "M4-test-reach-hits-subject-universe-only", "review": "M4/F2", "file": "reference_model.py",
     "old": "hits = sorted((i for i in items if i[\"endpoint\"][\"kind\"] == \"symbol\" and i[\"endpoint\"][\"universe\"] in embedded",
     "new": "hits = sorted((i for i in items if i[\"endpoint\"][\"kind\"] == \"symbol\" and i[\"endpoint\"][\"universe\"] == target[\"universe\"] and i[\"endpoint\"][\"universe\"] in embedded"},
    {"id": "M7-whole-view-count-basis-always-exact", "review": "M7/F7", "file": "reference_model.py",
     "old": "\"countBasis\": \"lower-bound\" if len(ordered) > max_items else \"exact\"", "new": "\"countBasis\": \"exact\""},
    {"id": "M8-metric-zero-absence-ignores-limitations", "review": "M8/F7", "file": "reference_model.py",
     "old": "context[\"totalItems\"] == 0 and not has_limitations(context)}", "new": "context[\"totalItems\"] == 0}"},
    {"id": "M9-test-origin-set-partial-blocker-dropped", "review": "F3", "file": "reference_model.py",
     "old": "    blockers = {\"test-origin-set-partial\"}\n", "new": "    blockers = set()\n"},
    {"id": "M10-cargo-member-targets-ignored", "review": "F4", "file": "reference_model.py",
     "old": "        if unit[\"unitId\"] not in selected or unit[\"targetKind\"] not in ENTRY_TARGET_KINDS:",
     "new": "        if unit[\"unitId\"] not in selected or unit[\"targetKind\"] not in ENTRY_TARGET_KINDS or unit[\"markerPath\"] != \"Cargo.toml\":"},
    {"id": "M11-importer-owner-by-symbol-path", "review": "F9", "file": "reference_model.py",
     "old": "        from_keys, cause = (key_resolver or importer_owner_keys)(world, row)",
     "new": "        from_keys, cause = (key_resolver or (lambda w, r: w.path_owner_keys(r[\"source\"][\"universe\"], w.symbol_attribution(r[\"source\"][\"universe\"], r[\"source\"][\"nativeSubjectId\"])[0]) if w.symbol_attribution(r[\"source\"][\"universe\"], r[\"source\"][\"nativeSubjectId\"])[0] else (None, \"importer-anchor-missing\")))(world, row)"},
    {"id": "M12-cells-omitted-blocker-dropped", "review": "F6", "file": "reference_model.py",
     "old": "    if kc < len(full[\"cells\"]):\n        blockers.add(\"cells-omitted\")\n", "new": ""},
    {"id": "M13-jest-selection-not-read", "review": "F3", "file": "reference_model.py",
     "old": "            if isinstance(jest, dict) and any(k in jest for k in TEST_SELECTION_KEYS)", "new": "            if False and isinstance(jest, dict)"},
    {"id": "M14-reached-universe-identity-blocker-dropped", "review": "F2", "file": "reference_model.py",
     "old": "            blockers.add(\"reached-universe-without-test-origin-identity\")", "new": "            pass"},
    {"id": "M15-source-dependencies-per-universe", "review": "F8", "file": "reference_model.py",
     "old": "cell[\"deps\"].add((tuple(row[\"anchorPaths\"]), target_identity))", "new": "cell[\"deps\"].add((tuple(row[\"anchorPaths\"]), target_identity, importer[\"universe\"]))"},
    {"id": "M16-registry-row-required-again", "review": "F1", "file": "identity_bridge.py",
     "old": "REGISTRY_ROW = {\"document\": PARAMETER_DOCUMENT, \"selector\": \"#\", \"owner\": \"foundation\",",
     "new": "REGISTRY_ROW = {\"requiredForEvaluatorMajors\": [3], \"document\": PARAMETER_DOCUMENT, \"selector\": \"#\", \"owner\": \"foundation\","},
    {"id": "M16b-overlay-row-required-published-row-unchanged", "review": "F1", "file": "identity_bridge.py",
     "old": "    rows[PARAMETER_DOCUMENT] = copy.deepcopy(REGISTRY_ROW)\n", "new": "    rows[PARAMETER_DOCUMENT] = dict(copy.deepcopy(REGISTRY_ROW), requiredForEvaluatorMajors=[3])\n"},
    {"id": "M17-coupling-budget-ignored", "review": "F6", "file": "reference_model.py",
     "old": "    kc, deltas[\"cells\"] = largest(ncells, lambda k: coupling_panel(world, full, k, 0, 0, placeholder))",
     "new": "    kc, deltas[\"cells\"] = ncells, None"},
]


def run(mutant):
    target = HERE / "mutants" / mutant["id"]
    if target.exists():
        shutil.rmtree(target)
    shutil.copytree(CAND, target, ignore=shutil.ignore_patterns("__pycache__"))
    path = target / mutant["file"]
    text = path.read_text()
    assert text.count(mutant["old"]) == 1, "mutant precondition " + mutant["id"]
    path.write_text(text.replace(mutant["old"], mutant["new"]))
    scratch = target / "tmp"
    scratch.mkdir()
    started = time.time()
    proc = subprocess.run([PY, "-I", "-B", str(target / "check.py"), "--architecture", ARCH, "--trace-closure"], capture_output=True, text=True,
                          env={"PATH": "/usr/bin:/bin", "TMPDIR": str(scratch), "HOME": os.environ.get("HOME", "/tmp")}, timeout=900)
    tail = [line for line in proc.stderr.strip().splitlines() if line.strip()][-1:] if proc.returncode else proc.stdout.strip().splitlines()[-1:]
    (HERE / "mutants" / (mutant["id"] + ".stderr.txt")).write_text(proc.stderr)
    shutil.rmtree(target)
    return {"id": mutant["id"], "review": mutant["review"], "exitCode": proc.returncode, "killed": proc.returncode != 0, "evidence": tail, "seconds": round(time.time() - started, 1)}


def main():
    wanted = set(sys.argv[1:])
    (HERE / "mutants").mkdir(exist_ok=True)
    results_path = HERE / "mutation-results.json"
    results = json.loads(results_path.read_text()) if results_path.exists() else {}
    for mutant in MUTANTS:
        if wanted and mutant["id"] not in wanted:
            continue
        results[mutant["id"]] = run(mutant)
        print(json.dumps(results[mutant["id"]]), flush=True)
    results_path.write_text(json.dumps(results, indent=1) + "\n")


if __name__ == "__main__":
    main()
