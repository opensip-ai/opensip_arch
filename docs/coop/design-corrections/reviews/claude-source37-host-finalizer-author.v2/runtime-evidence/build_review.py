"""Assemble v2 review.json from retained receipts, manifests, v1 history and root's probe. Every number is read back."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = HERE / "receipts"
SRC = HERE / "source"
V1 = Path("/tmp/opensip-design-corrections/claude-source37-host-finalizer-author.v1")
ROOT_PROBE = Path("/tmp/opensip-design-corrections/root-host-finalizer-scope.v1")


def js(path):
    return json.loads(Path(path).read_text())


def out(label, base=R):
    return js(base / label / "stdout.txt")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def receipt(label):
    d = R / label
    return {"label": label, **js(d / "command.json"), "exit": int((d / "exit.txt").read_text()), **js(d / "digests.json")}


def digest(label, base=R):
    return js(base / label / "digests.json")["stdoutSha256"]


after, before = js(HERE / "after-manifest.json"), js(HERE / "before-manifest.json")
sem = out("semantic-replay-v2")
v1_sem = out("semantic-replay-assembly.2", V1 / "receipts")
p2, p3, p1 = out("p2-termination-mutants-v2"), out("p3-root-variants-v2"), out("p1-combined-runs")
term_rows = [r for r in sem["checks"] if r["case"].startswith("run-termination")]
v1_ids = {r["case"] for r in v1_sem["checks"]}
v1_rows = {r["case"]: r for r in v1_sem["checks"] if r["case"].startswith("run-termination")}

frozen_changed = {r["frozen37Sha256"]: r["path"] for r in after["files"] if r["frozen37Sha256"] and not r["equalsFrozen37"]}
v1_changed = {r["v1Sha256"]: r["path"] for r in after["files"] if not r["equalsV1"]}
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
    hits = {path: text.count(h) for h, path in frozen_changed.items() if text.count(h)}
    if hits:
        stale[rel] = hits

controls = {
    "semanticReplay": {
        "v2": {"passed": sem["passed"], "count": sem["count"], "blocked": sem["blocked"]},
        "v1": {"passed": v1_sem["passed"], "count": v1_sem["count"]},
        "newRows": sorted(r["case"] for r in term_rows if r["case"] not in v1_ids),
        "v1RowsUnchangedResult": {c: (next(r for r in term_rows if r["case"] == c).get("termination") == v1_rows[c].get("termination")
                                      and next(r for r in term_rows if r["case"] == c).get("faults") == [])
                                  for c in v1_rows},
        "terminationRows": [{k: r.get(k) for k in ("case", "faults", "termination", "refusedSchemaValidAlternatives", "permutation",
                                                    "admittedProjectionWithDelegatedMembers", "refused", "drift")} for r in term_rows],
    },
    "mutants": {"referencePasses": p2["referencePasses"], "discriminating": p2["discriminating"],
                "failingRowsPerMutant": {k: v["failingRows"] for k, v in p2.items() if isinstance(v, dict) and "failingRows" in v}},
    "rootVariants": {"rootReportSha256": p3["rootReportSha256"], "rows": p3["rows"]},
    "regressionVsV1": {
        "workflowProjection": {"passed": out("workflow-projection-v2")["passed"], "count": out("workflow-projection-v2")["count"],
                               "identicalStdoutToV1": digest("workflow-projection-v2") == digest("workflow-projection-assembly.2", V1 / "receipts")},
        "queryProjection": {"count": out("query-projection-v2")["count"],
                            "identicalStdoutToV1": digest("query-projection-v2") == digest("query-projection-assembly", V1 / "receipts")},
        "checkWorkflows": {**out("check-workflows-v2"),
                           "identicalStdoutToV1": digest("check-workflows-v2") == digest("check-workflows-assembly.2", V1 / "receipts")},
        "identity": {**out("identity-v2"), "identicalStdoutToV1": digest("identity-v2") == digest("identity-assembly", V1 / "receipts")},
        "integration": {"passed": out("integration-v2")["passed"],
                        "identicalStdoutToV1": digest("integration-v2") == digest("integration-assembly", V1 / "receipts")},
    },
}

doc = {
    "review": "S37-01 host finalizer v2 scope follow-up: coverageId omission wording, combined closed-Run goldens, analysis projection versus delegated StepTermination members",
    "authorOrigin": "823bf66b-e92a-4789-ab81-63a1a9dc371d",
    "standing": "COAUTHOR SCOPE CONTINUATION ONLY. Not acceptance, not blind reconstruction, not application or readiness, not product qualification. No pins, global suites, planning, freeze, activation, commit or push. v1 is retained history and was not modified.",
    "inputs": {
        "v1Runtime": str(V1), "v1AfterManifestSha256": after["v1AfterManifestSha256"],
        "v1CopyExact": out("copy-v1-source")["copy"]["exact"],
        "v1SourceStillExactAtEnd": out("v1-source-integrity")["copy"]["exact"],
        "frozen37ManifestSha256": after["manifestSha256"],
        "rootProbe": {"probe.py": sha(ROOT_PROBE / "probe.py"), "report.json": sha(ROOT_PROBE / "report.json")},
    },
    "decisions": {
        "section5": "omission only when no condition at the primary rank has a declared or stage carrier; carrier-less conditions (evaluator-only, work budget, requirement-relative) do not suppress another condition's carrier; the v1 reduction law is unchanged",
        "projectionScope": "the owner derives an ANALYSIS PROJECTION: class, runId, reasonCodes and order, coverageId presence and value, and absence of errorCode/faultCause/signal. executionId (W section 1 / identity section 2), domainDetail (W sections 8-9, detail registry, composition section 8) and authority (W section 9) are delegated: shape-checked against StepTermination, returned owner-validation-required, never labelled lawful. Any other member refuses.",
        "whyNotBan": "executionId is a fresh host-CSPRNG attempt identity (W section 1, identity section 2) and domainDetail is host-attached explanation (W sections 8-9, composition section 8); exact whole-termination equality would forbid members other owners define and would make full terminations of two attempts unequal by design.",
        "apiChange": "check_candidate/admit_termination (v1) replaced by check_projection/admit_projection with a fixed refusal order; the maintained checker uses check_projection",
        "unchanged": ["condition population, cause bridge, total order, carrier choice", "fixture", "native-evidence.md",
                      "workflow-projection-contract.v3.md", "common schemas and StepTermination", "D9 v1.14 artifact", "identities"],
    },
    "files": {"before": before["files"], "after": after["files"], "tree": after["tree"],
              "v1ToV2Diff": after["v1-to-v2.diff"], "frozen37ToFinalDiff": after["frozen37-to-final.diff"]},
    "controls": controls,
    "exploration": {"p1CombinedRuns": {k: v.get("finalize", {}).get("termination") for k, v in p1.items()}},
    "coordination": {
        "queryFaultAuthor": "no overlap: v2 edits only foundation run-termination files, check-semantic-replay.v3.py and one W section 9 paragraph; the semantic fixture is unchanged in v2",
        "root": "W section 9 base is root-owned; merge the added paragraph (v1 +11 lines, v2 +4/-2 wording) later. R1/R2 common schemas untouched.",
        "staleFrozen37HashOccurrences": stale,
        "v1ToV2ChangedFiles": sorted(v1_changed.values()),
        "pinAdditionsStillNeeded": [r["path"] for r in after["files"] if r["frozen37Sha256"] is None],
    },
    "limitations": [
        "Mixed-owner goldens cover evaluator work budget with required-execution native accounts carrying stage terminals, and native atom causes with stage terminals and evaluator diagnostics; not requirement-relative sufficiency (required-relation-missing, confidence-floor-unmet), language-tier-unsupported, input-closure-incomplete, enumeration or import obligations.",
        "Delegated-member controls use shape fixtures; they prove the projection boundary and refusals, not that any executionId, domainDetail or authority value is a lawful host attribution or remedy.",
        "Delegated member lawfulness (attempt correlation, detail-to-observation agreement, authority standing) is not validated anywhere in this owner; their owners' host validation is outside these reference controls.",
        "The final section 5 wording edit (prose only) came after the checks; no checker or model reads the contract text.",
        "Synthetic native-admitted Runs; same author for contract, model and goldens; no blind reconstruction.",
        "TCB-SCOPE-01 (one assumption, 13 dependent accounts), 32 product gates and 54 planned recovery cases remain unperformed; nothing is granted.",
    ],
    "commands": [receipt(d.name) for d in sorted(R.iterdir()) if (d / "command.json").exists() and (d / "exit.txt").exists()],
    "commandsNote": "every finished receipt; the running build-review receipt is retained on disk",
    "grantsNothing": True,
}
text = json.dumps(doc, indent=1) + "\n"
(HERE / "review.json").write_text(text)
print(json.dumps({"sha256": hashlib.sha256(text.encode()).hexdigest(), "commands": len(doc["commands"]),
                  "newRows": controls["semanticReplay"]["newRows"], "v1RowsUnchanged": controls["semanticReplay"]["v1RowsUnchangedResult"],
                  "mutants": controls["mutants"]["discriminating"], "regression": controls["regressionVsV1"],
                  "stale": stale, "tree": after["tree"]}, indent=1))
