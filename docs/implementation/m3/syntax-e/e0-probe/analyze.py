#!/usr/bin/env python3
"""E0 analysis: applies the predeclared P1-P6 rules (E1 item 3) to phase 2's outputs.

The rules are fixed here, in phase 1, before any measurement exists:

P1  The four modules of build root A and build root B are byte-identical (sha256).
P2  Every module has zero imports, by both witnesses (independent reader and engine);
    recorded alongside: exports (A10 shape), start function, memories, target features.
P3  Over every regular selected T2a file (the 10 dialect selectors, cap 20,000, all <= 4 MiB):
    the wasm status equals the native status, and where both produced a tree the two
    SyntaxTreeV1 byte strings are equal (sha256). Any difference fails P3.
P4  Runs A (sorted, 1 thread), B (shuffle seed 1, 1 thread), C (shuffle seed 2, 8 threads)
    and D (reverse, 4 threads, the modules of build root B), every file in a fresh instance:
    per file, (status, tree sha256, fuel, peak pages) identical across all four.
    Discrimination controls (not gated): lazy translation and instance reuse are expected to
    change fuel; if neither does, P4's sensitivity is undemonstrated and the report says so.
P5  Timing run T (wasm only, sorted, 1 thread, after a warm-up run). Per file, time is the
    whole per-file cost the product pays: fresh store and instance, input copy, parse, result
    copy and host validation. Throughput = bytes / time in MiB/s (MiB = 1,048,576 bytes).
    P5a: the median over files with bytes > 0 is >= 1.0 MiB/s.
    P5b: every file (all are <= 4 MiB) takes <= 10 s.
    Also reported, not gated: aggregate throughput, parse-only median, native times.
P6  From run A's fuel and peak pages, one constant set for the bundle:
      B = 4 * max fuel over zero-byte files (if none, over the smallest file), rounded up to
          2 significant figures;
      K = ceil(max over files with bytes > 0 of (4 * fuel - B) / bytes), rounded up to 2 s.f.;
      M = 4 * max peak pages, rounded up to a multiple of 16 pages.
    Every file then uses <= 25% of B + K * bytes by construction. P6 passes iff M <= 65,536
    (the engine's wasm32 ceiling) and the verification run under (B, K, M) ends with no
    truncation. Boundary controls (not gated): exact measured fuel and pages give no
    truncation; one less fuel gives truncated:fuel and one less page gives truncated:memory,
    for every sampled file.
"""
import csv, hashlib, json, math, os, statistics, sys
from collections import Counter, defaultdict

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
MiB = 1048576.0

def rows(name):
    p = os.path.join(OUT, name)
    if not os.path.exists(p):
        return None
    with open(p) as f:
        lines = [l for l in f if not l.startswith("#")]
    return list(csv.DictReader(lines, delimiter="\t"))

def regular(rs):
    return [r for r in rs if r["w_status"] != "not-regular"]

def up2(x):
    """Round up to 2 significant figures."""
    if x <= 0:
        return 0
    e = int(math.floor(math.log10(x))) - 1
    return int(math.ceil(x / 10 ** e) * 10 ** e)

res = {}

# P1
def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()
mods = ["javascript", "rust", "tsx", "typescript"]
ba, bb = os.path.join(OUT, "..", "build-a", "out"), os.path.join(OUT, "..", "build-b", "out")
if os.path.isdir(ba) and os.path.isdir(bb):
    p1 = {m: (sha(f"{ba}/{m}.wasm"), sha(f"{bb}/{m}.wasm")) for m in mods}
    res["P1"] = {"pass": all(a == b for a, b in p1.values()), "modules": {m: {"a": a, "b": b} for m, (a, b) in p1.items()}}

# P2
insp = rows("p2-inspect.tsv")
if insp:
    res["P2"] = {
        "pass": all(r["imports(reader)"] == "0" and r["imports(engine)"] == "0" for r in insp),
        "modules": {os.path.basename(r["module"]): {k: r[k] for k in ("imports(reader)", "imports(engine)", "exports", "start", "memories", "target_features", "engine_shape", "bytes", "data_bytes")} for r in insp},
    }

# Admission (recorded, not gated)
adm = rows("admit.tsv")
if adm:
    res["admission"] = adm

# P3
A = rows("run-a.tsv")
if A:
    reg = regular(A)
    bad = [r for r in reg if r["w_status"] != r["n_status"] or (r["w_status"] == "ok" and r["eq"] != "1")]
    out = Counter((r["grammar"], r["w_outcome"]) for r in reg)
    res["P3"] = {
        "pass": not bad,
        "files": len(reg),
        "compared_trees": sum(1 for r in reg if r["eq"] == "1"),
        "mismatches": [{k: r[k] for k in ("idx", "repo", "path", "grammar", "w_status", "n_status", "first_diff")} for r in bad[:50]],
        "mismatch_count": len(bad),
        "outcomes": {f"{g}:{o}": n for (g, o), n in sorted(out.items())},
        "validation_failures_wasm": Counter(r["w_valid"] for r in reg if r["w_valid"] != "ok").most_common(10),
        "validation_failures_native": Counter(r["n_valid"] for r in reg if r["n_valid"] != "ok").most_common(10),
        "symlinks_skipped": len(A) - len(reg),
    }

# P4
key = lambda r: (r["w_status"], r["w_tree_sha256"], r["w_fuel_total"], r["w_pages_peak"])
runs = {n: rows(f"run-{n}.tsv") for n in ("a", "b", "c", "d")}
if all(runs.values()):
    base = {r["idx"]: key(r) for r in regular(runs["a"])}
    diffs = {}
    for n in ("b", "c", "d"):
        other = {r["idx"]: key(r) for r in regular(runs[n])}
        diffs[n] = sorted(i for i in base if other.get(i) != base[i])
    seq_moved = {n: sum(1 for r in runs[n] if r["seq"] != r["idx"]) for n in ("b", "c", "d")}
    res["P4"] = {"pass": all(not d for d in diffs.values()), "differing_files": {n: len(d) for n, d in diffs.items()},
                 "examples": {n: d[:10] for n, d in diffs.items()}, "files_processed_out_of_list_order": seq_moved}
    ctl = {}
    for n in ("lazy", "reuse"):
        c = rows(f"run-{n}.tsv")
        if c:
            cm = {r["idx"]: r for r in regular(c)}
            fuel_diff = sum(1 for i, r in cm.items() if r["w_fuel_total"] != base[i][2])
            tree_diff = sum(1 for i, r in cm.items() if r["w_tree_sha256"] != base[i][1])
            ctl[n] = {"files": len(cm), "fuel_differs": fuel_diff, "tree_differs": tree_diff}
    res["P4"]["controls"] = ctl

# P5
T = rows("run-t.tsv")
if T:
    reg = [r for r in regular(T) if r["w_status"] not in ("trunc-size",)]
    thr = [int(r["bytes"]) / MiB / (int(r["w_t_total_ns"]) / 1e9) for r in reg if int(r["bytes"]) > 0]
    thr_parse = [int(r["bytes"]) / MiB / (int(r["w_t_parse_ns"]) / 1e9) for r in reg if int(r["bytes"]) > 0]
    tmax = max(reg, key=lambda r: int(r["w_t_total_ns"]))
    tot_b = sum(int(r["bytes"]) for r in reg)
    tot_t = sum(int(r["w_t_total_ns"]) for r in reg) / 1e9
    per_g = defaultdict(list)
    for r in reg:
        if int(r["bytes"]) > 0:
            per_g[r["grammar"]].append(int(r["bytes"]) / MiB / (int(r["w_t_total_ns"]) / 1e9))
    q = lambda v, p: sorted(v)[min(len(v) - 1, int(p * len(v)))]
    res["P5"] = {
        "pass": statistics.median(thr) >= 1.0 and int(tmax["w_t_total_ns"]) <= 10e9,
        "P5a_median_MiBps": statistics.median(thr),
        "P5b_max_seconds": int(tmax["w_t_total_ns"]) / 1e9,
        "P5b_max_file": f'{tmax["repo"]}/{tmax["path"]} ({tmax["bytes"]} bytes)',
        "files_in_median": len(thr),
        "p10_p90_MiBps": [q(thr, 0.10), q(thr, 0.90)],
        "aggregate_MiBps": tot_b / MiB / tot_t,
        "median_parse_only_MiBps": statistics.median(thr_parse),
        "median_instantiate_us": statistics.median(int(r["w_t_inst_ns"]) / 1e3 for r in reg),
        "median_by_grammar_MiBps": {g: statistics.median(v) for g, v in sorted(per_g.items())},
        "sweep_seconds": tot_t,
    }
    if A:
        na = [r for r in regular(A) if int(r["bytes"]) > 0 and r["n_t_total_ns"] not in ("-", "")]
        res["P5"]["native_median_MiBps_context"] = statistics.median(int(r["bytes"]) / MiB / (int(r["n_t_total_ns"]) / 1e9) for r in na)

# P6
if A:
    reg = [r for r in regular(A) if r["w_status"] == "ok"]
    fuel = [(int(r["bytes"]), int(r["w_fuel_total"]), int(r["w_pages_peak"]), r) for r in reg]
    zero = [f for b, f, p, r in fuel if b == 0]
    if not zero:
        smallest = min(b for b, f, p, r in fuel)
        zero = [f for b, f, p, r in fuel if b == smallest]
    B = up2(4 * max(zero))
    K = up2(max((4 * f - B) / b for b, f, p, r in fuel if b > 0))
    peak = max(p for b, f, p, r in fuel)
    M = int(math.ceil(4 * peak / 16.0) * 16)
    worst = max(fuel, key=lambda x: x[1] / (B + K * x[0]))
    rate = None
    if T:
        tr = [r for r in regular(T) if r["w_status"] == "ok"]
        rate = sum(int(r["w_fuel_parse"]) for r in tr) / (sum(int(r["w_t_parse_ns"]) for r in tr) / 1e9)
    budget4 = B + K * 4 * 1024 * 1024
    res["P6"] = {
        "constants": {"fuelBase": B, "fuelPerByte": K, "maxMemoryPages": M},
        "max_peak_pages": peak,
        "max_budget_fraction": worst[1] / (B + K * worst[0]),
        "max_budget_fraction_file": f'{worst[3]["repo"]}/{worst[3]["path"]}',
        "per_grammar_max_fuel_per_byte": {g: max(f / b for b, f, p, r in fuel if b > 0 and r["grammar"] == g) for g in sorted({r["grammar"] for r in reg})},
        "budget_at_4MiB": budget4,
        "fuel_per_second": rate,
        "seconds_to_exhaust_4MiB_budget": (budget4 / rate) if rate else None,
        "memory_pass": M <= 65536,
    }
    L = rows("run-limits.tsv")
    if L:
        lr = regular(L)
        trunc = [r for r in lr if r["w_outcome"].startswith("truncated") or r["w_outcome"] == "backend-fault"]
        res["P6"]["verification"] = {"files": len(lr), "truncated_or_fault": len(trunc), "outcomes": Counter(r["w_outcome"] for r in lr)}
        res["P6"]["pass"] = res["P6"]["memory_pass"] and not trunc
    for n, want in (("exact", None), ("fuel-minus1", "truncated:fuel"), ("pages-minus1", "truncated:memory")):
        c = rows(f"run-{n}.tsv")
        if c:
            cr = regular(c)
            got = Counter(r["w_outcome"] for r in cr)
            ok = all((r["w_outcome"] == want) if want else (not r["w_outcome"].startswith("truncated") and r["w_outcome"] != "backend-fault") for r in cr)
            res["P6"].setdefault("boundary_controls", {})[n] = {"files": len(cr), "as_expected": ok, "outcomes": got}

json.dump(res, open(os.path.join(OUT, "summary.json"), "w"), indent=1, default=str)
for k in ("P1", "P2", "P3", "P4", "P5", "P6"):
    if k in res:
        print(k, "PASS" if res[k].get("pass") else "FAIL" if "pass" in res[k] else "n/a")
print("summary:", os.path.join(OUT, "summary.json"))
