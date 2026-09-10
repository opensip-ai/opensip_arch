"""Run every reconstruction scenario and write the machine-readable vector outputs."""

from __future__ import annotations

import hashlib
import json
import os
import sys
import traceback

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import opensip_ref as R
import closure as CL
import world as W
import build_ts as TS
import build_rust as RS
import build_syntax as SY
import build_workflow as WF
import build_extra as EX

OUT = "/tmp/opensip-design-corrections/consumer-b.v5/output"


def verify_manifest():
    base = R.KIT
    m = json.load(open(os.path.join(base, "consumer-input-manifest.json")))
    rows, ok, bad = [], 0, 0
    listed = set()
    for f in m["files"]:
        p = os.path.join(base, f["path"])
        listed.add(f["path"])
        if not os.path.exists(p):
            rows.append({"path": f["path"], "status": "MISSING"})
            bad += 1
            continue
        b = open(p, "rb").read()
        d = hashlib.sha256(b).hexdigest()
        good = d == f["sha256"] and len(b) == f["bytes"]
        rows.append({"path": f["path"], "status": "OK" if good else "MISMATCH",
                     "sha256": d, "bytes": len(b)})
        ok += good
        bad += (not good)
    on_disk = set()
    for root, _d, fs in os.walk(base):
        for x in fs:
            rp = os.path.relpath(os.path.join(root, x), base)
            if rp != "consumer-input-manifest.json":
                on_disk.add(rp)
    return {
        "parentSubjectSha256": m["parentSubjectSha256"],
        "declaredFileCount": len(m["files"]),
        "verifiedOk": ok, "failed": bad,
        "extraFilesOnDisk": sorted(on_disk - listed),
        "manifestEntriesMissingOnDisk": sorted(listed - on_disk),
        "allVerified": bad == 0 and not (on_disk - listed) and not (listed - on_disk),
        "rows": rows,
    }


def rc1_unresolved_edge_gap():
    """RC-1's `not-applicable` list names seven relations and the syntactic rungs.
    `unresolved-edge@observed` is in NEITHER list and is not a RESOLVED rung, so more
    than one state is defensible for an ordinary (available) entry."""
    g = CL.Graph("rc1-gap")
    scope = {"relation": "unresolved-edge", "resolution": "observed", "subjects": [],
             "sourceUniverse": "0" * 64, "targetUniverse": "0" * 64}
    out = {}
    for state, attempted, exhaustive, terminal in (
            ("not-applicable", False, True, None),
            ("complete", True, True, "complete"),
            ("not-attempted", False, True, None)):
        ent = W.entry("unresolved-edge", "observed", "complete" if state != "not-attempted"
                      else "unknown", state, attempted, exhaustive, terminal)
        if state == "not-attempted":
            ent["deficiency"] = None
        try:
            CL.check_rc2(g, scope, ent)
            CL.check_cause_registry(ent)
            ent2 = dict(ent)
            ent2["examinedUniverse"] = {"subjectScopeCommitment": "sha256:" + "0" * 64,
                                        "subjectCount": 0}
            payload = {"schemaVersion": 3,
                       "key": {"relation": "unresolved-edge", "resolution": "observed",
                               "sourceUniverse": "0" * 64, "targetUniverse": "0" * 64,
                               "subjectScopeCommitment": "sha256:" + "0" * 64},
                       "entry": ent2}
            R.validate("native", "#/$defs/CoverageResultV3", payload)
            out[state] = {"admitted": True, "coveragePayloadDigest": R.raw(payload)}
        except R.Refuse as exc:
            out[state] = {"admitted": False, "refusal": exc.code}
    distinct = {v.get("coveragePayloadDigest") for v in out.values()
                if v.get("coveragePayloadDigest")}
    return {
        "rc1NotApplicableRelations": ["file", "package", "vcs-change", "declares",
                                      "literal", "control-flow", "clones"],
        "rc1AlsoCoversSyntacticRungs": True,
        "unresolvedEdgeIsInNeitherList": True,
        "observedIsNotAResolvedRung": True,
        "statesTried": out,
        "distinctCoveragePayloadDigests": len(distinct),
        "consequence": "two conforming producers mint DIFFERENT coverage2 identities for "
                       "the same observation of the same universe",
    }


def main():
    results = {}
    errors = {}

    def run(name, fn, *a):
        try:
            return fn(*a)
        except Exception as exc:            # noqa: BLE001
            errors[name] = traceback.format_exc(limit=6)
            return None

    run("ts-ordinary", TS.scenario_ordinary, results)
    run("ts-synthesized", TS.scenario_synthesized, results)
    run("ts-custom-named", TS.scenario_custom_named_multi_base, results)
    run("ts-jsconfig", TS.scenario_jsconfig_shared_base, results)
    run("ts-two-contexts", TS.scenario_two_typescript_contexts, results)
    run("ts-negatives", TS.scenario_negatives, results)
    run("cache-key", TS.scenario_cache_key, results)

    run("rust-mixed", RS.scenario_mixed_edition, results)
    run("rust-two-selections", RS.scenario_two_selections, results)
    run("rust-ownership", RS.scenario_ownership_deficiencies, results)
    run("rust-negatives", RS.scenario_rust_negatives, results)

    bid = run("syntax-code", SY.scenario_code_grammar, results)
    run("syntax-data", SY.scenario_data_only, results, bid)
    run("syntax-vs-compiler", SY.scenario_grammar_vs_compiler_identity, results, bid)

    av = run("zero-config", WF.scenario_zero_config, results)
    run("public-terminations", WF.scenario_public_terminations, results)
    sc = run("scope-parameter", WF.scenario_scope_parameter, results)
    if sc:
        run("comparison", WF.scenario_comparison, results, sc[0], sc[1], sc[2])
    run("mutation-purge", WF.scenario_mutation_and_purge, results)
    if av:
        run("invocations", WF.scenario_invocations, results, av[0], av[1])

    run("canonicalization", EX.scenario_canonical, results)
    run("digest-law", EX.scenario_digest_law, results)
    run("capability-manifest", EX.scenario_capability_manifest, results)
    run("identity-mutation", EX.scenario_identity_mutation, results)
    run("min-resolution", EX.scenario_min_resolution, results)
    run("imported-evidence", EX.scenario_import, results)
    run("authorized-steps", EX.scenario_authorized_steps, results)

    results["rc1-unresolved-edge-state-gap"] = run("rc1", rc1_unresolved_edge_gap) or {}

    manifest = verify_manifest()
    os.makedirs(os.path.join(OUT, "vectors"), exist_ok=True)
    with open(os.path.join(OUT, "vectors", "input-verification.json"), "w") as fh:
        json.dump(manifest, fh, indent=1, sort_keys=True)
    for name, value in results.items():
        with open(os.path.join(OUT, "vectors", name + ".json"), "w") as fh:
            json.dump(value, fh, indent=1, sort_keys=True, ensure_ascii=False)
    summary = {
        "inputVerification": {k: v for k, v in manifest.items() if k != "rows"},
        "scenarios": sorted(results),
        "scenarioCount": len(results),
        "errors": errors,
    }
    with open(os.path.join(OUT, "vectors", "_summary.json"), "w") as fh:
        json.dump(summary, fh, indent=1, sort_keys=True)
    print(json.dumps(summary, indent=1))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
