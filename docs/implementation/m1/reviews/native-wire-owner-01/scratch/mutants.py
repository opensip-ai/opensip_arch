"""Reviewer mutations of author choices and handwritten rules, run against copies of the frozen 18 files.
Each mutant edits wire-carriers.v1.json only and records which checks fail."""
import json, os, shutil, subprocess, sys
S = "/tmp/opensip-implementation/m1-native-wire-owner-review-01/scratch"
PY = "/tmp/opensip-implementation/metadata-reference-env/bin/python"


def rule(d, rid):
    return next(a for a in d["admission"] if a["id"] == rid)


def member(d, rec, name):
    return next(m for m in d["records"][rec]["members"] if m["name"] == name)


def m_prepared_total_256(d):
    member(d, "Rust3PreparedOutputManifestV3", "entries")["type"]["maxItems"] = "256"
    member(d, "Rust3PreparedOutputEntryV3", "outputOrdinal")["type"]["max"] = "255"


def m_canonical_path_native(d):
    d["scalars"]["Rust3CanonicalPath"]["type"]["pattern"] = "^(?!/)(?!.*(^|/)\\.\\.?(/|$))[^\\u0000\\\\]+(?![\\s\\S])"


def m_exec_minlength1(d):
    d["scalars"]["Ts2ExecutionIdText"]["type"] = {"t": "text", "nfc": True, "minScalars": "1"}


def m_anchor_4096(d):
    member(d, "Rust3FactCandidateV1", "anchors")["type"]["maxItems"] = "4096"
    member(d, "Ts2FactCandidateV1", "anchors")["type"]["maxItems"] = "4096"


def m_ts_path_bytes(d):
    t = d["scalars"]["Ts2ProjectPath"]["type"]
    t.pop("maxScalars"); t["maxUtf8Bytes"] = "4096"


def m_fault_phase_worker_view(d):
    r = rule(d, "RUST3-FAULT-CANCEL-TYPES")
    r["rule"] = r["rule"].replace("host phase in which the Cancel was sent or the fault received", "worker phase at send")


def m_cancel_in_start_allowed(d):
    d["protocols"]["rust-semantic"]["transitions"]["cancelInStart"] = "Host may send Cancel in START (rust2 T023)."


def m_depsrc_order_sequence(d):
    r = rule(d, "DEPSRC-CUSTODY")
    r["rule"] = r["rule"].replace("ordered package-then-path", "ordered by sequence")


def m_scope2_drop_closure(d):
    r = rule(d, "PER-KEY-SCOPE2")
    r["rule"] = r["rule"].replace("enumeratorClosure (Plan-selected provider closure2 of the stage), ", "")


def m_identitytext_no_bytes(d):
    d["scalars"]["Rust3IdentityText"]["type"].pop("maxUtf8Bytes")


def m_package_key_min4(d):
    d["scalars"]["Rust3PackageKey"]["type"]["minScalars"] = "4"


def m_outputseen_not_reset(d):
    d["protocols"]["rust-semantic"]["transitions"]["stateUpdateAdditions"] = [{"onFrames": ["FactBatch", "CoverageV3"], "sets": "outputSeen = true"}]


def m_prepared_limit_rule_text(d):
    r = rule(d, "PREPARED-V3-SET-JOIN")
    r["rule"] = r["rule"].replace("build-script-directives rows <= maxPreparedOutputEntries", "all rows <= maxPreparedOutputEntries")


def m_commit_unavailable_stagecoverage(d):
    for row in d["commitmentMap"]["rows"]:
        if row["field"] == "Startup1UnavailableV3.coverageCommitment":
            row["domain"] = "opensip.rust-provider.stage-coverage.v2"


MUTANTS = [m_prepared_total_256, m_canonical_path_native, m_exec_minlength1, m_anchor_4096, m_ts_path_bytes,
           m_fault_phase_worker_view, m_cancel_in_start_allowed, m_depsrc_order_sequence, m_scope2_drop_closure,
           m_identitytext_no_bytes, m_package_key_min4, m_outputseen_not_reset, m_prepared_limit_rule_text,
           m_commit_unavailable_stagecoverage]


def run(m):
    work = os.path.join(S, "mut", m.__name__)
    shutil.rmtree(work, ignore_errors=True)
    shutil.copytree(os.path.join(S, "run1"), work, ignore=shutil.ignore_patterns("check-result.rerun.json"))
    p = os.path.join(work, "wire-carriers.v1.json")
    d = json.load(open(p))
    m(d)
    open(p, "w").write(json.dumps(d, indent=1, ensure_ascii=False) + "\n")
    env = dict(os.environ, TMPDIR=os.path.join(S, "tmp"))
    subprocess.run([PY, "-I", "-B", "check.py", "--out", os.path.join(work, "out.json")], cwd=work, env=env,
                   capture_output=True, timeout=1200)
    try:
        o = json.load(open(os.path.join(work, "out.json")))
        return {"mutant": m.__name__, "failed": o["failed"], "failedChecks": [f["id"] for f in o["failures"]]}
    except Exception as e:
        return {"mutant": m.__name__, "error": repr(e)}


if __name__ == "__main__":
    from concurrent.futures import ThreadPoolExecutor
    with ThreadPoolExecutor(4) as ex:
        results = list(ex.map(run, MUTANTS))
    json.dump(results, open(os.path.join(S, "mutants-result.json"), "w"), indent=1)
    print(json.dumps(results, indent=1))
