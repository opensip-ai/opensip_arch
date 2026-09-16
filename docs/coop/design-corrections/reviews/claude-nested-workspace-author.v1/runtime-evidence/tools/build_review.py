"""Build review.json and review.md from this runtime's receipts and result files, and publish the delta.

Usage: build_review.py

Every number in the review is read here from a receipt (receipts/<label>/{command.json,exit.txt,stdout.txt,stderr.txt})
or a result file; consistency checks are evaluated and listed, and the build exits non-zero if any fails. The delta in
deltas/v1 is copied to the runtime root as correction.patch / delta-manifest.json after its sha256 is re-verified.
This builder's own receipt cannot be listed inside the review it writes.
"""
import hashlib
import json
import re
from pathlib import Path

R = Path(__file__).resolve().parents[1]
sha = lambda b: hashlib.sha256(b).hexdigest()
load = lambda p: json.loads((R / p).read_text())
CHECKS = []


def check(name, ok, detail=None):
    CHECKS.append({"check": name, "holds": bool(ok), **({"detail": detail} if detail is not None else {})})
    return ok


def receipt(label):
    d = R / "receipts" / label
    return {"label": label, "argv": json.loads((d / "command.json").read_text())["argv"], "cwd": json.loads((d / "command.json").read_text())["cwd"],
            "exit": int((d / "exit.txt").read_text()), "stdout": (d / "stdout.txt").read_text(errors="replace"),
            "stderr": (d / "stderr.txt").read_text(errors="replace")}


def last_line(text):
    lines = [x for x in text.splitlines() if x.strip()]
    return lines[-1] if lines else ""


def walk(obj):
    yield obj
    if isinstance(obj, dict):
        for v in obj.values():
            yield from walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from walk(v)


def suite(label):
    r = receipt(label)
    name = label.split("suite-")[-1].split(".")[0]
    s = {"label": label, "exit": r["exit"]}
    if r["exit"] != 0 and not r["stdout"].strip().startswith(("{", "[", "PASS", "FAIL")) or (r["stderr"].strip() and "Traceback" in r["stderr"]):
        s["aborted"] = last_line(r["stderr"])
        return s
    if name == "native":
        if r["stdout"].lstrip().startswith("["):
            s["pinFaults"] = [f["path"] for f in json.loads(r["stdout"])]
        else:
            s["summary"] = last_line(r["stdout"])
    elif name in ("consumer24",):
        doc = json.loads(r["stdout"])
        s.update(total=doc["total"], passed=doc["passed"], failed=[(f["item"], f["case"], f.get("detail")) for f in doc["failed"]])
    elif name == "enumeration":
        s["stdoutSummary"] = json.loads(r["stdout"][:r["stdout"].index("\n}\n") + 3])
    elif name in ("integration", "identity"):
        doc = json.loads(r["stdout"])
        s.update(passed=doc["passed"], failed=doc["failed"])
    elif name == "security":
        doc = json.loads(r["stdout"])
        s.update({k: doc[k] for k in doc if k in ("passed", "counts", "sourcePinsValid", "changedOrMissing")})
        if "sweeps" in doc:
            s["sweepsHolding"] = "%d/%d" % (sum(1 for _, h in doc["sweeps"] if h), len(doc["sweeps"]))
    elif name == "workflow-projection":
        doc = json.loads(r["stdout"])
        summary = next(x for x in walk(doc) if isinstance(x, dict) and "passed" in x and "failed" in x)
        oks = [x["ok"] for x in walk(doc) if isinstance(x, dict) and "ok" in x]
        s.update(passed=summary["passed"], failed=summary["failed"], okTrue=oks.count(True), okFalse=oks.count(False))
    return s


# ------------------------------------------------------------------ custody
capture = load("custody/frozen39-capture.json")
final = load("results/final-recheck.json")
delta = load("deltas/v1/delta-manifest.json")
patch_bytes = (R / "deltas/v1/correction.patch").read_bytes()
check("capture-verified-all-members", capture["memberCount"] == 12909 and not capture["verifyBefore"]["faults"] and not capture["verifyAfter"]["faults"]
      and not capture["copyFaults"] and not capture["verifyBefore"]["unlisted"], capture["memberCount"])
check("final-recheck-holds", final["holds"])
check("final-recheck-frozen39-no-pycache", not final["frozen39Snapshot"]["pycacheDirs"], final["frozen39Snapshot"]["pycacheDirs"][:5])
check("delta-patch-sha-matches-manifest", sha(patch_bytes) == delta["patch"]["sha256"] and len(patch_bytes) == delta["patch"]["bytes"])
check("delta-no-additions-removals-faults", not delta["addedFiles"] and not delta["removedFiles"] and not delta["faults"] and not delta["pycacheDirs"])
patch_apply = load("results/postfix/patch-apply-check.json")
check("system-patch-reproduces-after-bytes", patch_apply["holds"] and receipt("patch-apply-system-patch")["exit"] == 0)

# ------------------------------------------------------------------ reproduction and probes
root_pre, root_post = load("results/prefix/root-adapted.json"), load("results/postfix/root-adapted.json")
raised = lambda rows: {r["name"]: (r.get("exceptionType") if r["raised"] else None) for r in rows}
check("root-observation-reproduced", raised(root_pre["rows"]) == {"ordinary-workspace": None, "nested-workspace-leaf": None,
                                                                   "nested-workspace-with-package": "StopIteration", "explicit-inner-workspace": None})
check("root-report-rows-equal-adapted-prefix-rows", final["rootReportRowsEqualAdaptedPrefixRows"])
check("root-adapted-postfix-nothing-raises", all(v is None for v in raised(root_post["rows"]).values()))
disc_pre, disc_post = load("results/prefix/discriminate.json"), load("results/postfix/discriminate.json")
comparison = load("results/postfix/sweep-comparison.json")
check("probe-prefix-escapes-recorded", disc_pre["sweep"]["raised"] == {"StopIteration": 918} and len(disc_pre["namedRaised"]) == 12
      and disc_pre["enumeration"]["nested-markers-standalone-fixture-derivation"].get("exceptionType") == "StopIteration")
check("probe-postfix-all-named-hold", disc_post["namedHolds"] == disc_post["namedTotal"] == 24 and disc_post["membership"]["holds"])
check("probe-postfix-sweep-clean", disc_post["sweep"]["raised"] == {} and disc_post["sweep"]["oracleMismatch"] == 0 and disc_post["sweep"]["ordinalFaults"] == 0
      and disc_post["sweep"]["refusedUnexpectedly"] == 0 and disc_post["sweep"]["p22Mismatch"] == 0
      and set(disc_post["sweep"]["oracleEnclosingUnitCounts"]) == {"1"})
check("probe-postfix-enumeration-typed", disc_post["enumeration"]["nested-markers-standalone-fixture-derivation"] ==
      {"raised": False, "result": "REFUSE", "refusals": ["ENUMERATION_ADMISSION_MEMBERSHIP_DERIVATION"]})
check("sweep-prefix-returning-inputs-unchanged", comparison["holds"] and comparison["preReturnedPostIdentical"] + comparison["preRaisedPostReturned"] == comparison["preInputs"])

# ------------------------------------------------------------------ suites
NAMES = ["native", "consumer24", "enumeration", "integration", "security", "identity", "workflow-projection"]
pre = {n: suite("prefix-suite-" + n) for n in NAMES}
post = {n: suite("postfix-suite-" + n) for n in NAMES}
controls = {n: suite("controls-prefix-model-suite-" + n) for n in ("native", "consumer24", "enumeration")}
unpinned = {"native": suite("postfix-unpinned-suite-native"), "security-attempt-1": {"label": "postfix-unpinned-suite-security", "exit": receipt("postfix-unpinned-suite-security")["exit"],
            "aborted": last_line(receipt("postfix-unpinned-suite-security")["stderr"])}, "security": suite("postfix-unpinned-suite-security.2")}
enum_pre, enum_post = load("results/prefix/enumeration-receipt.json"), load("results/postfix/enumeration-receipt.json")
new_enum = {c["case"]: [c["result"], c["refusals"]] for c in enum_post["cases"] if c["case"].startswith("nested-cargo-workspace")}
native_report = json.loads((R / "work/run-postfix/docs/coop/design-corrections/native/native-evidence-report.v2.json").read_text())
new_native = next(x for x in native_report["cases"]["results"] if x["id"] == "units-nested-cargo-workspace-folds-into-the-deepest-surviving-workspace-unit")
check("all-prefix-suites-exit-0", all(s["exit"] == 0 for s in pre.values()), {n: s["exit"] for n, s in pre.items()})
check("all-postfix-suites-exit-0", all(s["exit"] == 0 for s in post.values()), {n: s["exit"] for n, s in post.items()})
check("native-380-to-381-all-pass", pre["native"]["summary"].startswith("PASS: 380/380") and post["native"]["summary"].startswith("PASS: 381/381") and new_native["passed"])
check("consumer24-183-to-187-all-pass", (pre["consumer24"]["total"], pre["consumer24"]["passed"], post["consumer24"]["total"], post["consumer24"]["passed"]) == (183, 183, 187, 187))
check("enumeration-cases-plus-two-no-mismatch", len(enum_post["cases"]) == len(enum_pre["cases"]) + 2 and enum_pre["mismatches"] == [] == enum_post["mismatches"]
      and new_enum == {"nested-cargo-workspace-derivation-differs-refused": ["REFUSE", ["ENUMERATION_ADMISSION_MEMBERSHIP_DERIVATION"]],
                       "nested-cargo-workspace-derivation-folds-into-surviving-unit": ["ADMIT", []]}, new_enum)
check("unchanged-suites-equal", all(pre[n][k] == post[n][k] for n, keys in (("integration", ("passed", "failed")), ("identity", ("passed", "failed")),
                                                                            ("security", ("passed", "counts", "sweepsHolding")),
                                                                            ("workflow-projection", ("passed", "failed", "okTrue", "okFalse"))) for k in keys))
delta_paths = sorted(f["path"] for f in delta["files"])
check("unpinned-postfix-refuses-exactly-on-delta-files", sorted(unpinned["native"]["pinFaults"]) == delta_paths
      and unpinned["security"].get("sourcePinsValid") is False and sorted(unpinned["security"]["changedOrMissing"]) == delta_paths)
overlay = load("results/postfix/run-copy-pin-overlay.json")
check("pin-overlay-only-delta-entries", not overlay["pinOverlay"]["entriesNotAtBefore"] and {x["path"] for x in overlay["pinOverlay"]["replaced"]} == set(delta_paths))
control_state = load("results/controls/control-copy-state.json")
diag_pre, diag_post = load("results/controls/native-case-diagnosis-prefix-model.json"), load("results/controls/native-case-diagnosis-corrected-model.json")
check("control-copy-state-holds", control_state["holds"])
check("controls-fail-against-frozen39-model",
      controls["native"]["exit"] == 1 and "TypeError" in controls["native"].get("aborted", "")
      and diag_pre["discovery"]["faults"].count("step discover_units: StopIteration: ") == 4
      and controls["consumer24"]["failed"] == [("M3", "section-crashed", controls["consumer24"]["failed"][0][2])] and "StopIteration" in controls["consumer24"]["failed"][0][2]
      and controls["consumer24"]["passed"] == 183
      and controls["enumeration"]["exit"] == 1 and controls["enumeration"].get("aborted") == "StopIteration")
check("native-case-passes-against-corrected-model", diag_post["full"].get("passed") is True and diag_post["discovery"]["passed"] is True)
failed_attempts = [
    {"label": "edit-native-cases", "exit": receipt("edit-native-cases")["exit"], "what": last_line(receipt("edit-native-cases")["stderr"]),
     "followUp": "edit-native-cases-textual: textual insertion keeping every original byte; the dumps round-trip first differs at the offsets it records"},
    {"label": "postfix-unpinned-suite-security", "exit": receipt("postfix-unpinned-suite-security")["exit"], "what": last_line(receipt("postfix-unpinned-suite-security")["stderr"]),
     "followUp": "postfix-unpinned-suite-security.2 with an existing report directory (harness error, not a suite result)"},
    {"label": "control-copy-mutate", "exit": receipt("control-copy-mutate")["exit"], "what": last_line(receipt("control-copy-mutate")["stderr"]),
     "followUp": "the copy had already been mutated before the record write failed; control-copy-verify-state reads and records the actual state instead of re-running"},
    {"label": "build-review", "exit": receipt("build-review")["exit"], "what": last_line(receipt("build-review")["stderr"]),
     "followUp": "the builder listed its own in-progress receipt (no exit.txt yet); it now skips receipts without exit.txt and names them"},
]
check("failed-attempts-preserved", [f["exit"] for f in failed_attempts] == [1, 1, 1, 1])

receipts, in_progress = [], []
for d in sorted((R / "receipts").iterdir(), key=lambda p: p.stat().st_mtime):
    if not (d / "exit.txt").exists():
        in_progress.append(d.name)
        continue
    r = receipt(d.name)
    receipts.append({"label": d.name, "exit": r["exit"], "cwd": r["cwd"], "argv": r["argv"], "stdoutSha256": sha(r["stdout"].encode()),
                     "stderrSha256": sha(r["stderr"].encode())})

# ------------------------------------------------------------------ publish delta
published = {}
for name in ("correction.patch", "delta-manifest.json"):
    data = (R / "deltas/v1" / name).read_bytes()
    (R / name).write_bytes(data)
    published[name] = {"sha256": sha((R / name).read_bytes()), "bytes": len((R / name).read_bytes()), "equalsDeltasV1": (R / name).read_bytes() == data}
check("published-delta-equals-deltas-v1", all(v["equalsDeltasV1"] for v in published.values()))

holds = all(c["holds"] for c in CHECKS)
review = {
    "artifact": "nested-workspace-author.review", "version": 1,
    "author": "AUTHOR 823bf66b-e92a-4789-ab81-63a1a9dc371d (Claude)",
    "standing": ("Bounded architecture/design/reference correction of nested Cargo workspace folding over a fresh regular-file capture of frozen39. "
                 "Not independent acceptance, not readiness, not frozen40, not a repin. No product code, commit, push, activation, agents, web or private/session logs; "
                 "no LIVE, frozen or other-runtime writes; no blind consumer artifact or root replay diagnosis read; the TS/JS unitKind coauthor's work was not read."),
    "acceptanceClaimed": False, "readinessClaimed": False, "frozen40Claimed": False,
    "custody": {"manifestSha256": capture["manifestSha256"], "memberCount": capture["memberCount"], "totalBytes": capture["totalBytes"],
                "capture": capture["capture"], "finalRecheck": {"holds": final["holds"], "frozen39Faults": len(final["frozen39Snapshot"]["faults"]),
                                                                "frozen39Unlisted": final["frozen39Snapshot"]["unlisted"], "rootProbeFiles": final["rootProbeDirectory"]["files"]}},
    "defect": {
        "location": "docs/coop/design-corrections/native/native_evidence_model.v2.py discover_units, frozen39 lines 3925-3958",
        "mechanism": ("two passes disagreed on what a fold target is: pass 1 folded a Cargo.toml directory when ANY enclosing kept workspace MANIFEST existed; "
                      "pass 2 chose the deepest enclosing workspace MANIFEST and looked it up among units with next(); a workspace manifest below a workspace unit "
                      "is itself folded, so the lookup found no unit and StopIteration escaped"),
        "escapes": ["native discover_units (no typed refusal)", "enumeration admit_enumeration derivation witness (handler catches AdmissionError/ValidationError only)",
                    "consumer and checker call sites"],
        "measured": {"sweepInputs": disc_pre["sweep"]["inputs"], "sweepRaised": disc_pre["sweep"]["raised"], "namedRaised": disc_pre["namedRaised"],
                     "enumeration": disc_pre["enumeration"]["nested-markers-standalone-fixture-derivation"]},
    },
    "decision": {
        "chosen": "select the fold target among SURVIVING cargo-workspace units (U-4b.2 read as unit), in one depth-ordered pass; clarify U-4b.2 prose; no new code",
        "totality": ("for a kept Cargo.toml directory with an enclosing kept workspace manifest, the shallowest such manifest has no enclosing workspace manifest and is "
                     "therefore a unit; workspace units are pairwise non-nested, so exactly one encloses (sweep: every folded directory had exactly one)"),
        "typedRefusalRejected": ("no published law makes a workspace manifest below a workspace unit an error; U-4b.2 prescribes folding; a refusal would need a new "
                                 "code (out of scope) and would refuse representable trusted observations the contract already decides"),
    },
    "delta": {"files": delta["files"], "patch": delta["patch"], "published": published},
    "results": {"prefix": pre, "postfix": post, "postfixUnpinned": unpinned, "controlsAgainstFrozen39Model": controls,
                "nativeNewCase": new_native, "enumerationNewCases": new_enum, "nativeCaseDiagnosis": {"frozen39Model": diag_pre, "correctedModel": diag_post},
                "probes": {"rootAdapted": {"prefix": raised(root_pre["rows"]), "postfix": raised(root_post["rows"])},
                           "discriminate": {"prefix": {k: disc_pre[k] for k in ("namedHolds", "namedTotal", "namedRaised", "sweep", "enumeration")},
                                            "postfix": {k: disc_post[k] for k in ("namedHolds", "namedTotal", "namedRaised", "sweep", "enumeration")}},
                           "sweepComparison": {k: (v if not isinstance(v, list) else len(v)) for k, v in comparison.items()}},
                "pinOverlay": {"replacedEntries": len(overlay["pinOverlay"]["replaced"]), "pinFiles": sorted({x["pinFile"] for x in overlay["pinOverlay"]["replaced"]})},
                "controlCopyState": {"holds": control_state["holds"], "pinEntryCount": control_state["pinEntryCount"]},
                "patchApply": {"holds": patch_apply["holds"]}},
    "failedAttempts": failed_attempts,
    "directEdits": ["native_evidence_model.v2.py: fold loop + removed second pass (Edit x2) and docstring sentence (Edit x1)",
                    "native-evidence.md: U-4b.2 clarification (Edit x1)", "check-native-consumer24-corrections.v1.py: M3 tail rows (Edit x1)",
                    "check-enumeration.v1.py: two cases (Edit x1) and expectations/assertion (Edit x1)",
                    "native-cases.v2.json: fixture + case via receipt edit-native-cases-textual"],
    "checks": CHECKS, "holds": holds, "receipts": receipts, "receiptsInProgressAtBuild": in_progress,
}
(R / "review.json").write_text(json.dumps(review, indent=1) + "\n")

# ------------------------------------------------------------------ markdown
def row(cells):
    return "| " + " | ".join(str(c).replace("|", "\\|") for c in cells) + " |"


def brief(s):
    if "aborted" in s:
        return "aborted: " + s["aborted"]
    if "summary" in s:
        return s["summary"]
    if "pinFaults" in s:
        return "PIN-MISMATCH on %d files" % len(s["pinFaults"])
    if "total" in s:
        return "%d/%d passed; failed %s" % (s["passed"], s["total"], [f[1] for f in s["failed"]])
    if "stdoutSummary" in s:
        return "mismatches %s" % s["stdoutSummary"]["mismatches"]
    if "counts" in s:
        return "passed %s, cases %s, sweeps %s" % (s["passed"], s["counts"], s.get("sweepsHolding"))
    if "sourcePinsValid" in s:
        return "sourcePinsValid %s on %d files" % (s["sourcePinsValid"], len(s["changedOrMissing"]))
    if "okTrue" in s:
        return "passed %s, failed %s, ok rows %d/%d" % (s["passed"], s["failed"], s["okTrue"], s["okTrue"] + s["okFalse"])
    return "passed %s, failed %s" % (s.get("passed"), s.get("failed"))


sw_pre, sw_post = disc_pre["sweep"], disc_post["sweep"]
md = []
md.append("# Nested Cargo workspace folding — bounded author correction\n")
md.append("**Standing.** " + review["standing"] + " Root integration, full references and independent review follow. "
          "Every number below is recomputed by `tools/build_review.py` from receipts and result files; `review.json` carries the same values and %d consistency checks (all hold: **%s**).\n" % (len(CHECKS), holds))
md.append("## 1. Custody\n")
md.append("- LIVE manifest39 `%s`, sha256 verified; all %d members (%d bytes) verified, then captured as fresh regular files into `work/source` (`custody/frozen39-capture.json`: no faults, no unlisted, no copy faults)." % (capture["manifest"], capture["memberCount"], capture["totalBytes"]))
md.append("- End-of-work recheck (`results/final-recheck.json`, receipt `final-recheck`): manifest sha holds, frozen39 snapshot %d faults / %d unlisted; `work/source` differs from frozen39 in exactly the 5 delta files at their after-bytes; root's probe directory unchanged in use (hashes recorded) and root's `report.json` rows equal this runtime's pre-fix path-only adaptation rows: **%s**.\n"
          % (len(final["frozen39Snapshot"]["faults"]), len(final["frozen39Snapshot"]["unlisted"]), final["rootReportRowsEqualAdaptedPrefixRows"]))
md.append("## 2. Defect, reproduced\n")
md.append("Root's observation reproduces in the capture (`probes/root_adapted.py`, a path-only adaptation: model and report paths are arguments; cases and calls are root's): ordinary workspace, nested workspace leaf and explicit inner workspace return; `nested-workspace-with-package` raises `StopIteration`.\n")
md.append("Mechanism in frozen39 `discover_units` (lines 3925–3958): two passes disagreed on what a fold target is. Pass 1 marked a `Cargo.toml` directory folded when **any enclosing kept workspace manifest** existed. Pass 2 chose the **deepest enclosing workspace manifest** and looked it up among units with `next(...)`. A workspace manifest below a workspace unit is itself folded by pass 1, so for any `Cargo.toml` directory below such a nested workspace the lookup finds no unit and `StopIteration` escapes. It is not a typed refusal, and it also escapes enumeration admission: the derivation witness (`enumeration_model.v1.py:667`) catches only `AdmissionError`/`ValidationError`.\n")
md.append("Measured extent before the correction (`results/prefix/discriminate.json`):\n")
md.append("- exhaustive sweep over six directories (`\"\"`, `a`, `a/b`, `a/b/c`, `a-b`, `ab/c`) × {absent, package, workspace}, automatic and every explicit selection of one or two present directories: **%d of %d inputs raised `StopIteration`**; every input that returned already matched the law oracle (%d mismatches) and P22 (%d mismatches);" % (sw_pre["raised"].get("StopIteration", 0), sw_pre["inputs"], sw_pre["oracleMismatch"], sw_pre["p22Mismatch"]))
md.append("- %d of %d named scenarios raised: %s;" % (len(disc_pre["namedRaised"]), disc_pre["namedTotal"], ", ".join("`%s`" % x for x in disc_pre["namedRaised"])))
md.append("- enumeration admission with nested markers in the derivation witness: `%s` escaped at `%s`.\n" % (disc_pre["enumeration"]["nested-markers-standalone-fixture-derivation"]["exceptionType"], disc_pre["enumeration"]["nested-markers-standalone-fixture-derivation"]["at"]))
md.append("## 3. Assessment under published law\n")
md.append("U-4b.2 folds \"a `Cargo.toml` directory strictly below the root of a `cargo-workspace` **unit** … into the DEEPEST such workspace\". \"Such workspace\" can be read as a unit or as any workspace manifest. Only the unit reading is implementable. `memberPackageRoots` exists only on a `WorkspaceUnitV2`, and a workspace manifest below a workspace unit is not a unit by the same sentence. The manifest reading therefore has no record to receive members and forces either a contradiction or a refusal.\n")
md.append("The unit reading is total, so no refusal is needed. Take a kept `Cargo.toml` directory *d* with at least one enclosing kept workspace manifest, and let *w₀* be the shallowest. *w₀* has no enclosing kept workspace manifest (one would also enclose *d* and be shallower), so *w₀* is a unit. A workspace manifest below another kept workspace manifest is folded, so workspace units are pairwise non-nested. Exactly one workspace unit therefore encloses *d*, and \"DEEPEST (the longest enclosing `rootPath`)\" selects it. The sweep observed this: every one of %d folded directories after the correction had exactly one enclosing workspace unit (`oracleEnclosingUnitCounts`).\n" % sum(sw_post["oracleEnclosingUnitCounts"].values()))
md.append("Consistency with the neighbouring law:\n")
md.append("- **P22 / U-2** (explicit roots are unit selection): selection happens before folding and is unchanged. Explicit `.` equals the automatic unit. `.`+`nested` folds `nested` into the root unit, just as frozen39 already folds an explicitly named member package under a named workspace root. `nested` alone is its own workspace unit with `nested/pkg`, and `nested/pkg` alone is a `cargo-package`. Over all %d single-workspace explicit selections in the sweep, the explicit unit equals automatic discovery of its own subtree (%d mismatches)." % (sw_post["p22Checked"], sw_post["p22Mismatch"]))
md.append("- **U-8** boundaries: marker directories at or below a boundary are removed before folding (item 1); unchanged. A boundary below a nested workspace used to crash; it now folds the rest.")
md.append("- **U-4a / U-4b.4** pruning: Cargo roots for rows are unit roots plus member roots. With the correction every folded nested root is a member, so `nested/target` and `nested/pkg/target` stay `host-ignore-convention` and `nested/src/target` stays source.")
md.append("- **U-4b.3** ordering: unchanged (strict UTF-8 member roots; `nested-x` sorts before `nested/pkg`), enforced by the M3 law control.\n")
md.append("**A typed refusal was considered and rejected.** No published law makes a workspace manifest below a workspace unit an error. U-4b.2 prescribes folding, and the observations are representable trusted markers. A refusal would need a new code, which is out of scope, and would refuse inputs the contract already decides. No claim is made that Cargo accepts such a layout: this is a standalone reference over marker observations, and applicability is assessed under the published law only.\n")
md.append("## 4. Correction (smallest coherent)\n")
md.append(row(["file", "before sha256 / bytes", "after sha256 / bytes"]))
md.append(row(["---", "---", "---"]))
for f in delta["files"]:
    md.append(row(["`%s`" % f["path"], "`%s` / %d" % (f["before"]["sha256"], f["before"]["bytes"]), "`%s` / %d" % (f["after"]["sha256"], f["after"]["bytes"])]))
md.append("\n`correction.patch` sha256 `%s` (%d bytes), unified diff against frozen39 (a/ b/ repo-relative, 3 lines of context); `delta-manifest.json` sha256 `%s`. The system `patch -p1` applied to the frozen39 before-bytes reproduces all five after-images exactly (`results/postfix/patch-apply-check.json`).\n"
          % (delta["patch"]["sha256"], delta["patch"]["bytes"], published["delta-manifest.json"]["sha256"]))
md.append("- **Model.** One depth-ordered pass. A `Cargo.toml` directory is folded into the deepest already-emitted `rust` `cargo-workspace` unit that strictly encloses it, or else becomes a unit. The former second pass (the `next(...)` lookup) and `cargo_ws_roots` are removed, plus one docstring sentence. There is no new code, schema, registered-schema byte, pin or planning change, and no TS/JS line changed.")
md.append("- **Behaviour preserved elsewhere.** Every sweep input that returned before the correction returns byte-identical output after it (%d inputs); every one of the %d inputs that raised now returns (`results/postfix/sweep-comparison.json`)." % (comparison["preReturnedPostIdentical"], comparison["preRaisedPostReturned"]))
md.append("- **Contract.** U-4b.2 now says the fold target is a surviving **unit**, that directories left after item 1 and explicit selection are decided shallowest first, that a nested workspace manifest below a workspace unit is a member and receives none, and why a target always exists. It cites the new native case.")
md.append("- **Checker controls.**")
md.append("  - `native-cases.v2.json`: fixture `markersCargoNestedWorkspace` and case `units-nested-cargo-workspace-folds-into-the-deepest-surviving-workspace-unit`, placed after the existing P22 Cargo case rather than at the array end. The case covers automatic folding, explicit `.`, `.`+`nested`, `nested` and `nested/pkg`, a nested-project boundary, pruned trees, membership rows and scope prefixes.")
md.append("  - consumer24 M3: 4 rows — the fold, the law passing, member roots in segment rather than UTF-8 order giving `ENUMERATION_MEMBERSHIP_ORDER`, and a dropped folded member un-pruning its `target` giving `ENUMERATION_MEMBERSHIP_ROW_DERIVATION`.")
md.append("  - enumeration: the derivation witness over nested markers now decides a typed `REFUSE` [`ENUMERATION_ADMISSION_MEMBERSHIP_DERIVATION`] where memberships differ, and a coherent nested-workspace admission `ADMIT`s. The exact refusal and the folded rust unit are asserted.\n")
md.append("## 5. Suites (all children finished)\n")
md.append("Suites ran in run copies, never in `work/source` (checkers write reports beside themselves). `work/run-prefix` is a copy of the unedited capture. `work/run-postfix` is a copy of the corrected capture with the %d registered pin entries of the 5 delta files rewritten from before to after sha256, **in the copy only**, across %d pin files (`results/postfix/run-copy-pin-overlay.json`; no entry was at an unexpected value). The delta itself changes no pin file.\n"
          % (len(overlay["pinOverlay"]["replaced"]), len({x["pinFile"] for x in overlay["pinOverlay"]["replaced"]})))
md.append(row(["suite", "pre-fix (frozen39 bytes)", "post-fix (corrected, pin overlay)"]))
md.append(row(["---", "---", "---"]))
for n in NAMES:
    md.append(row([n, "exit %d — %s" % (pre[n]["exit"], brief(pre[n])), "exit %d — %s" % (post[n]["exit"], brief(post[n]))]))
md.append("\nThe new native case passed in the post-fix report, and the enumeration receipt records %s. Without the pin overlay, the corrected bytes are refused by pin verification exactly on the 5 delta files: native `PIN-MISMATCH` exit %d (receipt `postfix-unpinned-suite-native`), security `sourcePinsValid: false` exit %d (`postfix-unpinned-suite-security.2`). **Root must repin at integration; this delta deliberately does not.**\n"
          % (json.dumps(new_enum), unpinned["native"]["exit"], unpinned["security"]["exit"]))
md.append("### Controls discriminate: corrected checkers and cases against the frozen39 model\n")
md.append("The used unpinned copy was changed to hold the frozen39 model, with pins for the other 4 delta files overlaid (`results/controls/control-copy-state.json`, %d pin entries, holds: %s).\n" % (control_state["pinEntryCount"], control_state["holds"]))
md.append("- native: exit %d, the checker aborts (`%s`). Its step resolver dereferences `$auto.units` after the faulted step, which is the existing harness behaviour for any failed bound step. `probes/native_case_diagnosis.py` runs the case's discovery steps through the checker's own `run_case`: %d `discover_units` steps fault with `StopIteration` (automatic, `.`, `.`+`nested`, boundary), the explicit `nested` and `nested/pkg` steps return, and %d expectations are unreachable. Against the corrected model the full case passes." % (controls["native"]["exit"], controls["native"].get("aborted"), diag_pre["discovery"]["faults"].count("step discover_units: StopIteration: "), sum(1 for f in diag_pre["discovery"]["faults"] if "unreachable" in f)))
md.append("- consumer24: %d/%d; the only failure is M3 `section-crashed` (`StopIteration` at the `next(...)` lookup), and every pre-existing row still passes." % (controls["consumer24"]["passed"], controls["consumer24"]["total"]))
md.append("- enumeration: exit %d, `%s` escapes admission from `admit_enumeration` → `discover_units`.\n" % (controls["enumeration"]["exit"], controls["enumeration"].get("aborted")))
md.append("## 6. Failed attempts, preserved\n")
for f in failed_attempts:
    md.append("- `%s` (exit %d): %s → %s" % (f["label"], f["exit"], f["what"], f["followUp"]))
md.append("- Pre-fix probe, control and checker failures above are intended evidence and are kept as receipts.\n")
md.append("## 7. Integration notes for root\n")
md.append("- **Model hunks** are near, but do not change, the TS/JS unit block. The third hunk's context includes the tsjs `recognizerId` / `provenance` / `break` lines (frozen39 3950–3952). If the TS/JS unitKind coauthor changed those exact lines, that hunk needs a 3-way merge. That author's work was not read.")
md.append("- **Checker insertions:** `native-cases.v2.json` after `markersCargoWorkspaceTwoMembers` and after case index 105 (380→381 cases); consumer24 at the end of `m3()`; enumeration after `invalid-boundaries-native-admission-error`, plus 2 `want` entries and one assertion after the internal-root mismatches.")
md.append("- **Pins, reports, receipts:** registered pins (native, security, foundation, evaluator3, workflows pin files) still name the before-bytes. The frozen `native-evidence-report.v2.json` was not regenerated (post-fix reports live only in the run copies), and enumeration receipts were written to this runtime.\n")
md.append("## 8. Scope limitations\n")
md.append("- Standalone reference evidence over trusted marker observations. No Cargo, compiler or repository code ran, and no claim is made about Cargo's treatment of nested or `exclude`d workspaces. Markers carry no `exclude` information; whether a product should treat an excluded nested workspace as its own unit is a separate product/Cargo-semantics question that published law does not decide, and it is not decided here.")
md.append("- The sweep universe is 6 directories, explicit selections of at most 2, rust markers only, no boundaries, custody exclusions or cap interplay; those are covered only by named scenarios. The oracle was written by the same author as the fix, from the contract text, so it is not independent.")
md.append("- Suites ran on run copies with a pin overlay, not on LIVE or the frozen tree. Identity, workflow projection, integration and security are breadth re-runs whose results are unchanged.")
md.append("- No acceptance, readiness, frozen40 or repin is claimed. Root full references and independent review follow integration.\n")
md.append("## 9. Commands (receipts)\n")
md.append(row(["label", "exit", "argv (after interpreter flags)"]))
md.append(row(["---", "---", "---"]))
for r in receipts:
    argv = r["argv"][3:] if r["argv"][:3] == ["/tmp/opensip-architecture-review-env/bin/python", "-I", "-B"] else r["argv"]
    md.append(row([r["label"], r["exit"], "`%s`" % " ".join(argv).replace(str(R) + "/", "")]))
md.append("\nInterpreter for every Python receipt: `/tmp/opensip-architecture-review-env/bin/python -I -B`, with `PYTHONDONTWRITEBYTECODE=1`; each receipt directory holds command, cwd, stdout, stderr, exit and digests. Direct edits made without a receipt: " + "; ".join(review["directEdits"]) + ".\n")
(R / "review.md").write_text("\n".join(md))
print(json.dumps({"holds": holds, "failedChecks": [c for c in CHECKS if not c["holds"]], "checks": len(CHECKS), "receipts": len(receipts), "published": published}, indent=1))
raise SystemExit(0 if holds else 1)
