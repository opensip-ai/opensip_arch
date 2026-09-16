"""Assemble author-report.json from retained manifests, receipts and reports. Every number is read back."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
R = HERE / "probes" / "receipts"
REP = HERE / "reports"
SRC = Path("/tmp/opensip-design-corrections/consumer23-source-clarifications.v1/source")


def js(path):
    return json.loads(Path(path).read_text())


def out(label):
    return js(R / label / "stdout.txt")


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


before, after = js(HERE / "before-manifest.json"), js(HERE / "after-manifest.json")
q_base, q_final = js(REP / "baseline-query-frozen36.json"), js(REP / "query-assembly.final2.json")
nc_f36, nc_final = out("native-cases-frozen36"), out("native-cases-assembly.3")
_first_text = (R / "identity-assembly" / "stdout.txt").read_text()
_first_summary, _end = json.JSONDecoder().raw_decode(_first_text)
id_first = {**_first_summary, "failedChecks": json.loads(_first_text[_end:])}
id_f36, id_final = out("identity-frozen36"), out("identity-assembly.3")
int_f36, int_final = out("integration-frozen36"), out("integration-assembly.3")
p2, p3 = out("p2-discrimination.2"), out("p3-native-case-discrimination")

base_ids = {c["id"] for c in q_base["checks"]}
new_query_controls = [c["id"] for c in q_final["checks"] if c["id"] not in base_ids]
s3_controls = [c for c in new_query_controls if c.startswith("host-availability-")]
s1_controls = [c for c in new_query_controls if c not in s3_controls]

commands = []
for d in sorted(R.iterdir()):
    if (d / "command.json").exists() and (d / "exit.txt").exists():
        row = js(d / "command.json")
        row["exit"] = int((d / "exit.txt").read_text())
        row.update(js(d / "digests.json"))
        commands.append(row)

changed = [r for r in after["files"] if not r["equalsFrozen36"]]
frozen_hashes = {r["frozen36Sha256"] for r in changed}
ledgers = ["foundation/evaluator3-source-pins.v1.json", "foundation/source-pins.v1.json", "native/source-pins.v2.json",
           "security/source-pins.v1.json", "workflows/source-pins.v1.json"]
pin_rows = {l: sum((SRC / "docs/coop/design-corrections" / l).read_text().count(h) for h in frozen_hashes) for l in ledgers}
other_hash_bearing = ["docs/v2/architecture/implementation-normative-inputs.v4.json",
                      "docs/v2/architecture/implementation-planning-sources.v1.json",
                      "docs/v2/architecture/implementation-coverage.v1.json",
                      "docs/coop/design-corrections/workflows/workflows-report.v1.json"]
other_rows = {p: sum((SRC / p).read_text().count(h) for h in frozen_hashes) for p in other_hash_bearing}
native_report = js(SRC / "docs/coop/design-corrections/native/native-evidence-report.v2.json")


def find_total(node):
    if isinstance(node, dict):
        if isinstance(node.get("total"), int):
            return {"total": node["total"], "passed": node.get("passed")}
        for value in node.values():
            found = find_total(value)
            if found:
                return found
    return None


native_report = find_total(native_report) or {}

doc = {
    "report": "consumer23 source clarifications: V23-S1, V23-S2, V23-S3 corrections and V16-A3 / V23-A1 dispositions",
    "authorOrigin": "823bf66b-e92a-4789-ab81-63a1a9dc371d",
    "standing": "AUTHORSHIP ONLY. Not independent acceptance, not blind B, not successor/final-application/readiness agreement, "
                "not product qualification. No commit or push. Root owns pins, generated reports, planning and freezing.",
    "inputs": {
        "assembly": str(SRC),
        "frozen36": "/tmp/opensip-design-corrections/candidate-subject.v36",
        "frozen36ManifestSha256Declared": "a729406b9de0d865294884f7575ea943c0935437091389e2acebe8e5aedb4235",
        "manifestFileVerified": False,
        "custodyMethod": "full-tree SHA-256 comparison of assembly against frozen36 (after-manifest.json#/assembly); the manifest file itself was not readable here",
        "findings": {"path": str(HERE / "consumer-source-findings.json"), "sha256": sha(HERE / "consumer-source-findings.json")},
    },
    "decisions": {
        "V23-S1": {
            "disposition": "CORRECTED: schema-first admission law",
            "law": "every shape GraphEndpoint refuses, including a package endpoint without a non-empty packageManifestPath, is "
                   "QUERY.PARAMS_MALFORMED before any Run, view, availability observation or vertex; QUERY.ENDPOINT_AMBIGUOUS is only "
                   "a well-formed complete tuple resolving to more than one distinct admitted vertex",
            "consumerSmallestFixNotTaken": {
                "reclassifyTheOneSchemaFault": "needs a placeholder re-admission and a field-based reclassification, and names an incomplete request ambiguous",
                "relaxGraphEndpoint": "loosens a strict public schema and admits a tuple that cannot resolve",
            },
            "publicWrapperBehaviourChanged": False,
            "helperBehaviourChanged": "parse_endpoint_syntax package-without-coordinate: QUERY.ENDPOINT_AMBIGUOUS -> QUERY.PARAMS_MALFORMED",
            "reachabilityLimit": "the reference public wrapper cannot produce QUERY.ENDPOINT_AMBIGUOUS: inventory_vertices keys vertices by the "
                                 "complete tuple; the branch is held by one helper-unit control",
        },
        "V23-S2": {
            "disposition": "CORRECTED: total native deficiency -> existing D9 whole-Run route",
            "consumerSmallestFixNotTaken": "calling section 10 the per-requirement / DomainDetail route would contradict the D9 owner; "
                                           "the per-requirement route is REPAIR.EVIDENCE_RUN_UNAVAILABLE, not these columns",
            "law": "section 10 class/code columns are the whole-Run termination route of the Run's primary deficiency under "
                   "d9-exit-contract codeMaps.deficiencyToReasonCode; native bridges DeficiencyV2 to D9Deficiency (five identity, "
                   "four verdict-indeterminate); primary = section 10 precedence over entry deficiencies and the deficiency a clean "
                   "typed stage terminal implies",
            "tableRowsCorrected": {"language-tier-unsupported": "COVERAGE.LANGUAGE_TIER_UNSUPPORTED",
                                   "confidence-floor-unmet": "COVERAGE.CONFIDENCE_FLOOR_UNMET",
                                   "required-relation-missing": "COVERAGE.REQUIRED_RELATION_MISSING"},
            "whyNotD9Map": "D9_MAP is keyed by public detail code and check-integration requires its keys to be registered DomainDetails",
            "runTerminationRows": {"total": len(p2["native"]["assembly"]), "changed": len(p2["nativeChanged"]),
                                   "changedRows": p2["nativeChanged"]},
            "scope": "run_termination returns ONE primary code; D9 ordered secondaryDeficiencies are composed by the host termination",
            "preserved": ["D9 public vocabulary, classes and exits (d9 artifact not edited)", "typed DeficiencyV2 carrier",
                          "per-unsatisfied-requirement REPAIR.EVIDENCE_RUN_UNAVAILABLE law"],
            "schemaAnnotationNotChanged": {
                "file": "docs/coop/design-corrections/native/native-evidence.schemas.v2.json",
                "annotationKey": "publicD9Termination",
                "why": "the raw SHA-256 of that document is a registered payloadSchemaDigest (part of coverage2 ids); an authored "
                       "annotation edit failed check-identity v20-native-view-fixture-declares-current-registered-schemas and was "
                       "reverted to exact frozen36 bytes",
                "currentText": "still the section 10 table columns (indeterminate (3) with VERDICT.INDETERMINATE, COVERAGE.PROVIDER_UNAVAILABLE or COVERAGE.BUDGET_EXHAUSTED)",
                "proposedTextForRoot": "still the section 10 table columns, which are the whole-Run route of the Run's primary deficiency "
                                       "under the D9 exit contract's codeMaps.deficiencyToReasonCode (indeterminate (3) with "
                                       "COVERAGE.LANGUAGE_TIER_UNSUPPORTED, COVERAGE.PROVIDER_UNAVAILABLE, COVERAGE.BUDGET_EXHAUSTED, "
                                       "COVERAGE.CONFIDENCE_FLOOR_UNMET or COVERAGE.REQUIRED_RELATION_MISSING for the five DeficiencyV2 "
                                       "members that are D9Deficiency members, and VERDICT.INDETERMINATE for the four that are not)",
                "condition": "apply only together with a deliberate re-registration of the schema document digest",
            },
        },
        "V23-S3": {
            "disposition": "CORRECTED: exact graph availability mapping published; model routing unchanged (comment only)",
            "law": "availability.state purged/expired/corrupt/unavailable -> operational-failed / HOST.IO_FAILURE / exit 4 with "
                   "evidence.purged / evidence.expired / evidence.corrupt / evidence.missing; retained, partial and omitted neither "
                   "refuse nor grant; close_run decides missing or corrupt bytes",
            "noNewEnumsOrDetails": True,
            "preserved": ["graph HOST.IO_FAILURE exit 4", "finding.show REQUEST.PRECONDITION_FAILED / exit 2", "other seventeen operations"],
        },
        "V16-A3": {"disposition": "CARRIED AS BOUNDED ADVISORY, no source change",
                   "rationale": "graph-query TraversalCoverage says `Not native CoverageResult` and the two obligations are distinct "
                                "required fields; the native schema does not mention traversal. Renaming a public field is a major "
                                "change for a wording hazard."},
        "V23-A1": {"disposition": "CARRIED AS BOUNDED ADVISORY, no source change",
                   "rationale": "workflows-and-surfaces section 1 Cancellation fixes the aggregate (interrupted 130, cancelled steps, "
                                "an aborted analysis leaves no Run) and command-inventory golden interrupted-before-settle fixes class "
                                "and exit; every parity field is identical under either lawful carrier"},
    },
    "hashes": {"before": before["files"], "after": after["files"]},
    "changedFiles": [{k: r[k] for k in ("path", "frozen36Sha256", "sha256", "bytes", "added", "removed", "diff", "diffSha256")}
                     for r in changed],
    "revertedToFrozen36": [r["path"] for r in after["files"] if r["equalsFrozen36"]],
    "assemblyCustody": after["assembly"],
    "controls": {
        "query": {"frozen36": {"count": q_base["count"], "failed": q_base["failedCount"]},
                  "assembly": {"count": q_final["count"], "failed": q_final["failedCount"]},
                  "new": {"S3": s3_controls, "S1": s1_controls},
                  "failOnlyUnderFrozen36Model": p2["queryDiscrimination"]["failOnlyUnderFrozen36Model"],
                  "note": "the other new controls also pass under the frozen36 model: they pin wrapper behaviour frozen36 had but did not publish"},
        "nativeCases": {"frozen36": {"total": nc_f36["total"], "passed": nc_f36["passed"]},
                        "assembly": {"total": nc_final["total"], "passed": nc_final["passed"]},
                        "new": p3["selected"], "failUnderFrozen36Model": p3["discriminating"],
                        "frozen36Faults": {r["id"]: r["faults"] for r in p3["frozen36"]},
                        "howRun": "native-cases.v2.json through check_native_evidence.v2.run_case; main() not run (pin verification and in-tree report write)"},
        "checkIdentity": {"frozen36": id_f36, "assembly": id_final},
        "checkIntegration": {"frozen36": {"passed": int_f36["passed"], "failed": int_f36["failed"]},
                             "assembly": {"passed": int_final["passed"], "failed": int_final["failed"]}},
        "previousExpectationsChanged": [],
    },
    "retainedFailedAttempts": [
        {"receipt": "identity-assembly", "result": id_first,
         "cause": "authored native schema annotation changed a registered schema document digest; reverted"},
        {"receipt": "p2-discrimination", "exit": 1, "cause": "same digest mismatch replaying an assembly-built fixture; rerun as p2-discrimination.2"},
    ],
    "selfReviewCorrection": "full-diff review found the new native-evidence.md fault-law sentence citing "
                            "native-deficiency-whole-run-route-is-total-and-d9-owned for stage-terminal precedence; corrected to "
                            "run-termination-code-is-the-primary-deficiency-route; native cases, query, identity and integration rerun "
                            "(.3 receipts) and snapshot-after.2 regenerated",
    "standings": {"publicWrapper": "execute_graph_query over the retained semantic fixture replayed through close_run",
                  "helperUnit": ["parse_endpoint_syntax", "admit_vertices", "native_deficiency_d9", "d9_route_drift", "run_termination"],
                  "notClaimed": ["Coverage admission of run_termination inputs", "a complete Run for S2", "closed enumeration",
                                 "product qualification"]},
    "forRoot": {
        "stalePinRows": {"total": sum(pin_rows.values()), "byLedger": pin_rows, "pinAdditionNeeded": False},
        "otherFrozen36HashOccurrences": {"counts": other_rows, "note": "planning-layer and generated-report files; not edited by this author"},
        "generatedReportCounts": {"native-evidence-report.v2.json": {"recordedTotal": native_report.get("total"), "assemblyTotal": nc_final["total"]}},
        "schemaAnnotationDecision": "see decisions.V23-S2.schemaAnnotationNotChanged",
        "remaining": ["run all six groups and planning", "freeze", "independent successor review", "blind reconstruction",
                      "fresh final application review"],
    },
    "carriedUnchanged": ["ONE TCB-SCOPE-01 assumption with 13 dependent residual accounts", "32 product gates unperformed",
                         "54 planned recovery cases unperformed", "source acceptance reopened; nothing granted here"],
    "limitations": [
        "S2 evidence is direct helper execution: no Coverage admission and no complete Run",
        "QUERY.ENDPOINT_AMBIGUOUS is unreachable through the reference public wrapper; held only at helper level",
        "native checker main(), the six integrated groups, planning checks and pin validation were not run",
        "the frozen36 manifest file itself was not readable; exact-tree comparison was used",
    ],
    "commands": commands,
    "grantsNothing": True,
}
text = json.dumps(doc, indent=1) + "\n"
(HERE / "author-report.json").write_text(text)
print(json.dumps({"sha256": hashlib.sha256(text.encode()).hexdigest(), "commands": len(commands),
                  "newQuery": {"S3": len(s3_controls), "S1": len(s1_controls)}, "changedFiles": len(changed),
                  "pinRows": pin_rows, "otherRows": other_rows, "nativeReportTotal": native_report.get("total"),
                  "runTermination": [len(p2["native"]["assembly"]), len(p2["nativeChanged"])]}, indent=1))
