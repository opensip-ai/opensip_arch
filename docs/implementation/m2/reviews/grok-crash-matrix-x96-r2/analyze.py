#!/usr/bin/env python3
"""Read-only X9-6 r2 checks and digest comparison. Writes only under this directory."""
import hashlib
import json
import subprocess
from pathlib import Path

PY = "/opt/homebrew/Cellar/python@3.14/3.14.6/bin/python3.14"
REPO = Path("/Users/sb/code/opensip-ai/opensip-x9-6")
COMMIT = "3d2d5b5a5e5cabd1768b02e29eb3c0928264fb4f"
EVID = Path("/Users/sb/code/opensip-ai/opensip_arch/docs/implementation/m2/crash-matrix-x9/evidence") / COMMIT
SETS = REPO / "target/opensip-x9"
OUT = Path("/tmp/opensip-implementation/reviews/grok-crash-matrix-x96-r2")
CHECKER = REPO / "tools/check_crash_matrix.py"
REQ = {
    "storage": REPO / "crates/storage/tests/fixtures/crash-matrix/required-runs.v1.json",
    "host": REPO / "crates/host/tests/fixtures/crash-matrix/required-runs.v1.json",
}


def run_check(label, pairs):
    cmd = [PY, str(CHECKER), "check", "--repository", str(REPO), "--commit", COMMIT]
    for name, run_set, repeat in pairs:
        cmd += ["--target", name, str(REQ[name]), str(run_set), str(repeat)]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    path = OUT / f"check-{label}.json"
    path.write_text(proc.stdout)
    err = OUT / f"check-{label}.err"
    err.write_text(proc.stderr)
    if proc.returncode != 0:
        raise SystemExit(f"{label} check exit {proc.returncode}: {proc.stderr[-500:]}")
    return json.loads(proc.stdout)


def load_runs(directory: Path):
    runs = {}
    for path in sorted((directory / "runs").iterdir()):
        if path.suffix != ".json":
            continue
        run = json.loads(path.read_text())
        key = f"{run['case']}-{run['variant']}"
        runs[key] = {
            "normalizedSha256": run["postState"]["normalizedSha256"],
            "traces": [child["trace"] for child in run["children"]],
        }
    return runs


def compare(left, right):
    only_left = sorted(set(left) - set(right))
    only_right = sorted(set(right) - set(left))
    equal = differing = 0
    diffs = []
    for key in sorted(set(left) & set(right)):
        norm = left[key]["normalizedSha256"] == right[key]["normalizedSha256"]
        trace = left[key]["traces"] == right[key]["traces"]
        if norm and trace:
            equal += 1
        else:
            differing += 1
            diffs.append({
                "run": key,
                "normalizedSha256Equal": norm,
                "childTraceEqual": trace,
                "childCounts": [len(left[key]["traces"]), len(right[key]["traces"])],
            })
    return {"equal": equal, "differing": differing, "onlyLeft": only_left, "onlyRight": only_right, "diffs": diffs}


def dir_bytes(path: Path):
    files = [p for p in path.rglob("*") if p.is_file()]
    return len(files), sum(p.stat().st_size for p in files)


def pin_mismatches(matrix_path: Path, directory: Path):
    matrix = json.loads(matrix_path.read_text())
    bad = []
    for entry in matrix["runs"]:
        data = (directory / entry["path"]).read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if digest != entry["sha256"] or len(data) != entry["bytes"]:
            bad.append(entry["path"])
    return len(matrix["runs"]), bad


def main():
    grok1 = {"storage": SETS / "x96-grok-r2-1-storage", "host": SETS / "x96-grok-r2-1-host"}
    grok2 = {"storage": SETS / "x96-grok-r2-2-storage", "host": SETS / "x96-grok-r2-2-host"}
    lead1 = {"storage": EVID / "storage", "host": EVID / "host"}
    lead2 = {"storage": SETS / "x96-final-2-storage", "host": SETS / "x96-final-2-host"}
    final1 = {"storage": SETS / "x96-final-1-storage", "host": SETS / "x96-final-1-host"}

    reviewer = run_check("reviewer-pair", [("storage", grok1["storage"], grok2["storage"]), ("host", grok1["host"], grok2["host"])])
    mixed = run_check("mixed-pair", [("storage", lead1["storage"], grok1["storage"]), ("host", lead1["host"], grok1["host"])])
    lead = run_check("lead-pair", [("storage", lead1["storage"], lead2["storage"]), ("host", lead1["host"], lead2["host"])])
    committed = json.loads((EVID / "check.json").read_text())

    def brief(doc):
        targets = {}
        for name, body in doc["targets"].items():
            targets[name] = {k: body[k] for k in ("runs", "censusPoints", "killSet", "killedPoints", "censusTrace")}
        return {k: doc[k] for k in (
            "passed", "commit", "runs", "unionCensusPoints", "killSet", "killedPoints",
            "killedOutsideKillSet", "limits", "repetitionsAgree", "matrixPass", "productQualification",
        )} | {"targets": targets}

    runs = {}
    for label, mapping in (
        ("grok1", grok1), ("grok2", grok2), ("lead1", lead1), ("lead2", lead2), ("final1", final1),
    ):
        runs[label] = {}
        for target, directory in mapping.items():
            runs[label][target] = load_runs(directory)

    pairs = {}
    for left_name, right_name in (
        ("grok1", "lead1"), ("grok2", "lead1"), ("grok1", "grok2"),
        ("grok1", "lead2"), ("grok2", "lead2"), ("final1", "lead1"),
    ):
        combined = {"equal": 0, "differing": 0, "onlyLeft": [], "onlyRight": [], "diffs": [], "byTarget": {}}
        for target in ("storage", "host"):
            result = compare(runs[left_name][target], runs[right_name][target])
            combined["byTarget"][target] = {
                "equal": result["equal"], "differing": result["differing"],
                "onlyLeft": result["onlyLeft"], "onlyRight": result["onlyRight"],
            }
            combined["equal"] += result["equal"]
            combined["differing"] += result["differing"]
            combined["diffs"].extend({**item, "target": target} for item in result["diffs"])
            combined["onlyLeft"].extend(f"{target}:{name}" for name in result["onlyLeft"])
            combined["onlyRight"].extend(f"{target}:{name}" for name in result["onlyRight"])
        pairs[f"{left_name}_vs_{right_name}"] = combined

    # hashes.txt
    text = (EVID / "hashes.txt").read_text()
    file_lines = 0
    bad_hash = []
    footer = None
    for line in text.splitlines():
        if line.startswith("product commit "):
            footer = line
            continue
        digest, nbytes, rel = line.split(" ", 2)
        file_lines += 1
        path = EVID / rel
        if not path.is_file():
            bad_hash.append(rel + " missing")
            continue
        data = path.read_bytes()
        if hashlib.sha256(data).hexdigest() != digest or len(data) != int(nbytes):
            bad_hash.append(rel)
    hashes_sha = hashlib.sha256((EVID / "hashes.txt").read_bytes()).hexdigest()

    storage_n, storage_b = dir_bytes(EVID / "storage/runs")
    host_n, host_b = dir_bytes(EVID / "host/runs")
    archives = [p.name for p in EVID.rglob("*") if p.suffix in {".xz", ".gz", ".tar"} or p.name.endswith(".tar.xz")]
    layout_names = sorted(str(p.relative_to(EVID)) for p in EVID.rglob("*") if p.is_file() and "runs/" not in str(p.relative_to(EVID)))

    pins = {}
    for label, matrix, directory in (
        ("lead1-storage", EVID / "storage/matrix.json", EVID / "storage"),
        ("lead1-host", EVID / "host/matrix.json", EVID / "host"),
        ("lead2-storage", EVID / "lead-2/storage/matrix.json", lead2["storage"]),
        ("lead2-host", EVID / "lead-2/host/matrix.json", lead2["host"]),
        ("final1-storage", SETS / "x96-final-1-storage/matrix.json", final1["storage"]),
        ("final1-host", SETS / "x96-final-1-host/matrix.json", final1["host"]),
    ):
        count, bad = pin_mismatches(matrix, directory)
        pins[label] = {"runs": count, "mismatches": bad}

    # live final-1 matrix pins against the committed lead-1 files
    pins["final1-matrix-vs-evidence-storage"] = {
        "runs": pins["final1-storage"]["runs"],
        "mismatches": pin_mismatches(SETS / "x96-final-1-storage/matrix.json", EVID / "storage")[1],
    }
    pins["final1-matrix-vs-evidence-host"] = {
        "runs": pins["final1-host"]["runs"],
        "mismatches": pin_mismatches(SETS / "x96-final-1-host/matrix.json", EVID / "host")[1],
    }

    evidence_runs = pairs["grok1_vs_lead1"]["equal"] + pairs["grok2_vs_lead1"]["equal"] + pairs["grok1_vs_lead2"]["equal"] + pairs["grok2_vs_lead2"]["equal"]
    evidence_diff = pairs["grok1_vs_lead1"]["differing"] + pairs["grok2_vs_lead1"]["differing"] + pairs["grok1_vs_lead2"]["differing"] + pairs["grok2_vs_lead2"]["differing"]

    summary = {
        "reviewerPair": brief(reviewer),
        "mixedPair": brief(mixed),
        "leadPair": brief(lead),
        "leadCheckEqualsCommitted": lead == committed,
        "hashes": {"fileLines": file_lines, "bad": bad_hash, "footer": footer, "sha256": hashes_sha, "bytes": (EVID / "hashes.txt").stat().st_size},
        "layout": {
            "nonRunFiles": layout_names,
            "storageRuns": storage_n,
            "storageRunBytes": storage_b,
            "hostRuns": host_n,
            "hostRunBytes": host_b,
            "archives": archives,
        },
        "pins": pins,
        "normalizedAgreement": {
            "equal": evidence_runs,
            "differing": evidence_diff,
            "runsPerSet": pairs["grok1_vs_lead1"]["equal"] + pairs["grok1_vs_lead1"]["differing"],
            "pairs": {name: {k: value[k] for k in ("equal", "differing", "onlyLeft", "onlyRight", "diffs", "byTarget")} for name, value in pairs.items()},
        },
    }
    (OUT / "agreement.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({
        "reviewerMatrixPass": reviewer["matrixPass"],
        "mixedMatrixPass": mixed["matrixPass"],
        "leadMatrixPass": lead["matrixPass"],
        "leadCheckEqualsCommitted": lead == committed,
        "equal": evidence_runs,
        "differing": evidence_diff,
        "hashesBad": len(bad_hash),
        "hashesSha": hashes_sha,
        "fileLines": file_lines,
        "storageRuns": storage_n,
        "hostRuns": host_n,
        "archives": archives,
        "pairDiffs": {name: value["differing"] for name, value in pairs.items()},
        "pinMismatches": {name: len(value["mismatches"]) for name, value in pins.items()},
    }, indent=2))


if __name__ == "__main__":
    main()
