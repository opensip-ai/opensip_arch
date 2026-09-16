"""Assemble review.json from retained receipts, manifests and reviewer inputs. Every number is read back."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = HERE / "receipts"
SRC = HERE / "source"
REVIEWER = Path("/tmp/opensip-design-corrections/claude-independent-design.v37")


def js(path):
    return json.loads(Path(path).read_text())


def out(label):
    return js(R / label / "stdout.txt")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def receipt(label):
    d = R / label
    return {"label": label, **js(d / "command.json"), "exit": int((d / "exit.txt").read_text()), **js(d / "digests.json")}


after, before = js(HERE / "after-manifest.json"), js(HERE / "before-manifest.json")
sem, sem_f37 = out("semantic-replay-assembly.2"), out("semantic-replay-frozen37")
term_rows = [r for r in sem["checks"] if r["case"].startswith("run-termination")]
p1, p2 = out("p1-explore-termination"), out("p2-termination-mutants")
wp, wp_f37 = out("workflow-projection-assembly.2"), out("workflow-projection-frozen37")
changed = [r for r in after["files"] if r["inFrozen37"] and not r["equalsFrozen37"]]
new = [r for r in after["files"] if not r["inFrozen37"]]
frozen_hashes = {r["frozen37Sha256"]: r["path"] for r in changed}
hash_bearing = ["docs/coop/design-corrections/foundation/evaluator3-source-pins.v1.json",
                "docs/coop/design-corrections/foundation/source-pins.v1.json",
                "docs/coop/design-corrections/native/source-pins.v2.json",
                "docs/coop/design-corrections/security/source-pins.v1.json",
                "docs/coop/design-corrections/workflows/source-pins.v1.json",
                "docs/v2/architecture/implementation-normative-inputs.v5.json",
                "docs/v2/architecture/implementation-planning-sources.v1.json",
                "docs/v2/architecture/implementation-coverage.v1.json",
                "docs/v2/architecture/implementation-normative-inputs.v4.json",
                "docs/v2/architecture/implementation-normative-inputs.v3.json"]
stale = {}
for rel in hash_bearing:
    text = (SRC / rel).read_text()
    hits = {path: text.count(h) for h, path in frozen_hashes.items() if text.count(h)}
    if hits:
        stale[rel] = hits


def same_stdout(a, b):
    return receipt(a)["stdoutSha256"] == receipt(b)["stdoutSha256"]


controls = {
    "semanticReplay": {"assembly": {"passed": sem["passed"], "count": sem["count"], "blocked": sem["blocked"]},
                       "frozen37": {"passed": sem_f37["passed"], "count": sem_f37["count"]},
                       "newRows": len(term_rows),
                       "terminationRows": [{"case": r["case"], "faults": r["faults"], "termination": r.get("termination"),
                                            "refusedSchemaValidAlternatives": r.get("refusedSchemaValidAlternatives"),
                                            "permutation": r.get("permutation"), "drift": r.get("drift")} for r in term_rows]},
    "mutants": {"referencePasses": p2["referencePasses"], "discriminating": p2["discriminating"],
                "failingRowsPerMutant": {k: v["failingRows"] for k, v in p2.items() if isinstance(v, dict) and "failingRows" in v}},
    "identity": {"assembly": out("identity-assembly"), "frozen37": out("identity-frozen37"),
                 "identicalStdout": same_stdout("identity-assembly", "identity-frozen37")},
    "integration": {"assembly": {"passed": out("integration-assembly")["passed"], "failed": out("integration-assembly")["failed"]},
                    "frozen37": {"passed": out("integration-frozen37")["passed"]},
                    "identicalStdout": same_stdout("integration-assembly", "integration-frozen37")},
    "queryProjection": {"assembly": {k: out("query-projection-assembly")[k] for k in ("passed", "count", "failedCount")},
                        "identicalStdout": same_stdout("query-projection-assembly", "query-projection-frozen37")},
    "workflowProjection": {"assembly": {"passed": wp["passed"], "count": wp["count"]}, "frozen37": {"passed": wp_f37["passed"], "count": wp_f37["count"]},
                           "onlyDifferingSourceHashes": sorted(k for k in wp["sourceHashes"] if wp["sourceHashes"][k] != wp_f37["sourceHashes"].get(k)),
                           "restIdentical": {k: v for k, v in wp.items() if k != "sourceHashes"} == {k: v for k, v in wp_f37.items() if k != "sourceHashes"}},
    "checkWorkflows": {"assembly": out("check-workflows-assembly.2"), "pristine37": out("check-workflows-pristine37"),
                       "identicalStdout": same_stdout("check-workflows-assembly.2", "check-workflows-pristine37")},
    "fixtureConsumers": {name: {"identicalStdout": same_stdout(f"{name}-assembly", f"{name}-pristine37")}
                         for name in ("execution-replay", "candidate-replay", "provider-attribution", "execution-inputs")},
    "nativeCases": {"assembly": out("native-cases-assembly"), "pristine37": out("native-cases-pristine37")},
}
ei_a, ei_p = out("execution-inputs-assembly"), out("execution-inputs-pristine37")
controls["fixtureConsumers"]["execution-inputs"]["onlyOwnedHashPathsDiffer"] = (
    {k: v for k, v in ei_a.items() if k != "ownedHashes"} == {k: v for k, v in ei_p.items() if k != "ownedHashes"}
    and [x["sha256"] for x in ei_a["ownedHashes"]] == [x["sha256"] for x in ei_p["ownedHashes"]])

doc = {
    "review": "S37-01 host finalizer correction: whole-Run indeterminate reasonCodes order, cause bridge and coverageId",
    "authorOrigin": "823bf66b-e92a-4789-ab81-63a1a9dc371d",
    "standing": "COAUTHOR CORRECTION ONLY. Not independent acceptance, not blind reconstruction, not successor, application or readiness agreement, not product qualification. No commit, push, freeze or activation.",
    "inputs": {
        "frozen37": "/tmp/opensip-design-corrections/candidate-subject.v37",
        "manifest": "/Users/sb/code/opensip-ai/opensip_arch/docs/coop/design-corrections/reviews/candidate-subject.v37.json",
        "manifestSha256": after["manifestSha256"],
        "copyVerified": out("copy-source")["copy"]["exact"],
        "frozen37StillExactAfterBaselines": out("frozen37-integrity-after-baselines")["copy"]["exact"],
        "pristineCopyExactAfterBaselines": out("pristine37-integrity-after-baselines")["copy"]["exact"],
        "reviewerInputs": {str(p): sha(p) for p in (REVIEWER / "review.md", REVIEWER / "receipts/probe-cause-attribution.json",
                                                    REVIEWER / "receipts/probe-semantic-boundaries.json",
                                                    REVIEWER / "probes/probe_cause_attribution.py")},
    },
    "finding": "S37-01",
    "decisions": {
        "owner": "docs/coop/design-corrections/foundation/run-termination-contract.v1.md (new; pointed to by workflows-and-surfaces section 9 and native-evidence section 10)",
        "population": "proof.executionDeficiencies plus, for each sealed-indeterminate gating rule, rule-level records and root-blocking witness deficiencies recomputed from the retained witness tree (composition sections 3 and 5)",
        "order": "native section 10 precedence rank per DeficiencyV2 cause; work-budget-exhausted ranks as budget-exhausted; every other registered cause rank 9 -> verdict-indeterminate; distinct D9 deficiencies by least rank",
        "stageTerminal": "originating coverage2 stageTerminal budget-exhausted/unavailable adds a stage-implied condition; the entry is never rewritten; coverageId prefers a declared carrier, then a stage carrier",
        "coverageId": "least declared carrier of the primary cause, else least stage carrier, else omitted",
        "workBudget": "MUST contribute D9 deficiency budget-exhausted (replaces 'may reuse'); positioned by the section 4 order",
        "classPrecedence": "unchanged; fault/rejection/interrupt/durability decided first from trusted host observation; sealed verdict decides pass/fail/indeterminate",
        "notChanged": ["D9 v1.14 artifact", "common schemas and StepTermination", "registered payload schema bytes", "identities",
                       "public code vocabulary", "native run_termination helper", "source-pins ledgers", "planning layers", "generated reports"],
    },
    "reviewerReproducers": {
        "A": "same Run, two carriers: derived coverageId is the least declared carrier; the other and omission are refused (golden same-run-two-coverage-carriers)",
        "B": "stage/entry disagreement on an actually closed Run: reasonCodes[0] COVERAGE.BUDGET_EXHAUSTED, coverageId the stage carrier whose entry keeps resolution-incomplete (golden stage-entry-disagreement)",
        "C": "discovery order is not an input: 16 tested orders derive one termination while the verbatim D9 reducer gives 2 primaries (golden permuted-condition-discovery). The reviewer's three-owner mix is not a retained Run golden; see limitations",
    },
    "files": {"before": before["files"], "after": after["files"], "tree": after["tree"], "proposedEditsDiff": after["proposedEditsDiff"],
              "changedExisting": [{k: r[k] for k in ("path", "frozen37Sha256", "sha256", "bytes", "added", "removed", "diffSha256")} for r in changed],
              "new": [{k: r[k] for k in ("path", "sha256", "bytes", "added", "diffSha256")} for r in new]},
    "controls": controls,
    "exploration": {"p1Cases": {k: v.get("finalize", {}).get("termination") for k, v in p1.items() if isinstance(v, dict) and "finalize" in v},
                    "p1RouteDrift": p1["routeDrift"]},
    "forRoot": {
        "staleFrozen37HashOccurrences": stale,
        "pinAdditionsNeeded": [r["path"] for r in new],
        "workflowsAndSurfacesSection9Delta": "one added paragraph (+11/-0) after 'No new D9 family is introduced.'; exact bytes in diffs/",
        "rootOwnedFilesTouched": [],
        "rootOwnedFilesReadOnlyDependencies": ["workflows/query_projection_model.v3.py (StepTermination schema validation in the new checker rows)"],
        "notRun": ["run-evaluator3-checks.py, run-reference-checks.py launchers and native check_native_evidence main (pin-gated; native and workflows launchers write into the tree)",
                   "planning checks", "six integrated groups"],
        "optionalFollowUps": ["StepTermination.coverageId / D9Deficiency descriptions could cite the owner in a root schema successor",
                              "a D9 successor artifact could restate the pre-reduction order"],
    },
    "limitations": [
        "Goldens are synthetic native-admitted Runs closed by close_run; not compiler or provider qualification.",
        "No retained golden combines several COVERAGE.* causes from different owners (e.g. requirement required-relation-missing plus a stage terminal); that order rests on the section 4 table and route drift.",
        "Derivation, contract and goldens share one author; no blind reconstruction was performed.",
        "Stage-implied conditions come only from Coverage records that a population record originates from; a host-observed stage terminal that no retained record carries contributes nothing by design.",
        "The fixture gained two knobs (budget_limit, references_stage_terminals); defaults are byte-preserving, as the identical consumer-checker outputs show.",
        "Comparison-step d9Deficiency (workflow_projection_model) is unchanged and outside this owner.",
        "TCB-SCOPE-01 (one assumption, 13 dependent accounts), 32 product gates and 54 planned recovery cases remain unperformed; nothing is granted here.",
    ],
    "commands": [receipt(d.name) for d in sorted(R.iterdir()) if (d / "command.json").exists() and (d / "exit.txt").exists()],
    "commandsNote": "every receipt that has finished; the build-review receipts of this builder are still running when it reads the directory and are retained on disk",
    "grantsNothing": True,
}
text = json.dumps(doc, indent=1) + "\n"
(HERE / "review.json").write_text(text)
print(json.dumps({"sha256": hashlib.sha256(text.encode()).hexdigest(), "commands": len(doc["commands"]),
                  "stale": stale, "mutants": controls["mutants"]["discriminating"],
                  "fixtureConsumers": controls["fixtureConsumers"], "semantic": controls["semanticReplay"]["assembly"]}, indent=1))
