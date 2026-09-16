"""Assemble review.json from the actual probe output, custody files and receipts.

Every PROVEN fact is recomputed from probes/output/policy-test-profile-probe.json and the builder refuses (exit 1) if one
does not hold, so the report cannot carry a stale or hand-typed claim. Inferences, selectors and the correction plan are
labelled as such.
"""
import hashlib
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
load = lambda p: json.loads((HERE / p).read_text())
fsha = lambda p: hashlib.sha256((HERE / p).read_bytes()).hexdigest()
probe = load("probes/output/policy-test-profile-probe.json")
B, POL, SU, OBS = probe["bindings"], probe["policies"], probe["suites"], probe["observations"]
BYPASS = "DIAGNOSTIC_BYPASS_legacy_run_policy_test_NOT_A_PRODUCT_ROUTE"
ROUTE = "publicRoute_run_admitted_policy_test"
failures = []


def fact(fid, statement, holds, evidence):
    if not holds:
        failures.append(fid)
    return {"id": fid, "statement": statement, "holds": bool(holds), "evidence": evidence}


lawful_v2 = sorted(n for n, p in POL.items() if p["schemaMajor"] == 2 and p["policyDocumentV2Schema"]["valid"]
                   and p["currentV3ResolvePolicy"]["outcome"] == "RETURNED" and p["evaluator3EffectivePolicyRecordV1"]["valid"])
suite_of = {"checker-v2-literal": "checker-v2-literal-suite", "endpoint-target-v2": "endpoint-target-v2-suite", "test-filter-v2": "test-filter-v2-suite"}
facts = [
    fact("F1-route-binds-legacy-resolver-and-evaluator",
         "run_admitted_policy_test (workflows_model.v3.py) calls the legacy workflows_model.v1 run_policy_test object, whose globals are the "
         "legacy module: it resolves the legacy resolve_policy (not the v3 atom-owner override) and the legacy evaluate/eval_pred; v3 defines no "
         "evaluate and the legacy eval_pred names no endpoint.",
         B["run_policy_test.isLegacyObject"] and B["run_policy_test.globalsAreLegacyModule"] and B["run_policy_test.resolvesLegacyResolvePolicy"]
         and not B["run_policy_test.resolvesCurrentV3ResolvePolicy"] and B["v3.resolve_policy.overridesLegacy"] and B["run_policy_test.evaluate.isLegacy"]
         and not B["v3.definesOwnEvaluate"] and not B["legacyEvalPredicateSourceMentionsEndpoint"],
         {"probe": "bindings", "values": B}),
    fact("F2-selected-admission-and-classifier-are-v1",
         "Suite admission validates PolicyTestSuiteV1 whose candidatePolicy is PolicyDocumentV1, and the grammar classifier reads "
         "urn:opensip:product-v1:workflows:policy-document rooted at PolicyDocumentV1.",
         B["suiteAdmissionRef"].endswith("PolicyTestSuiteV1") and B["grammarClassifier.document$id"] == "urn:opensip:product-v1:workflows:policy-document"
         and B["grammarClassifier.rootDefinitionConstants"] == ["PolicyDocumentV1"],
         {"probe": "bindings"}),
    fact("F3-lawful-current-v2-candidates-cannot-be-tested",
         "Every probe policy that is simultaneously PolicyDocumentV2-schema valid, admitted by the current v3 resolve_policy (atom owner) and "
         "carriable in evaluator3 EffectivePolicyRecordV1 (the policy-show carrier) is refused by the selected suite admission and by the public "
         "route, before any evaluation.",
         lawful_v2 == sorted(suite_of) and all(SU[suite_of[n]]["selectedAdmission"]["outcome"] == "REFUSED"
                                              and SU[suite_of[n]][ROUTE]["outcome"] == "REFUSED" for n in lawful_v2),
         {"lawfulCurrentV2Policies": lawful_v2,
          "routeRefusals": {n: {k: SU[suite_of[n]][ROUTE].get(k) for k in ("errorCode", "detail", "remedy", "terminationClass", "exitCode")} for n in lawful_v2}}),
    fact("F4-schema-major-is-the-sole-cause-for-the-checker-literal",
         "DISCRIMINATION ONLY (not a lawful conversion): the same checker literal with only schemaMajor 1 is admitted and returns a "
         "resolver-accepted result, so for that input the refusal is exactly the candidate major.",
         SU["checker-literal-major1-DISCRIMINATION-ONLY-suite"]["selectedAdmission"]["outcome"] == "RETURNED"
         and SU["checker-literal-major1-DISCRIMINATION-ONLY-suite"][ROUTE].get("result", {}).get("resolverAccepted") is True,
         {"suite": "checker-literal-major1-DISCRIMINATION-ONLY-suite"}),
    fact("F5-lawful-v1-controls-still-route",
         "The exact owner V1 suite (workflow-cases.v1.json policySuite) and a V1 control are admitted by the current route and the owner suite's "
         "result validates PolicyTestResultV1 and the evaluator3 PolicyTestResultRecordV1 carrier.",
         OBS["controlV1SuiteAdmittedAndCarried"] and SU["endpoint-source-v1-suite"][ROUTE]["outcome"] == "RETURNED",
         {"controlResult": {k: SU["control-v1-owner-suite"][ROUTE]["result"][k] for k in ("policyTestResultId", "summary", "resultSchema", "carrierSchema")}}),
    fact("F6-policy-show-carries-v2-not-v1",
         "The current policy-show carrier admits the V2 policies and refuses the owner V1 fixture policy, so the policy a user sees as current "
         "cannot be the candidate the current suite admits, and vice versa.",
         POL["checker-v2-literal"]["evaluator3EffectivePolicyRecordV1"]["valid"] and not POL["base-v1-owner-fixture"]["evaluator3EffectivePolicyRecordV1"]["valid"]
         and not POL["checker-v2-literal"]["policyDocumentV1Schema"]["valid"],
         {"probe": "policies.*.evaluator3EffectivePolicyRecordV1"}),
    fact("F7-route-resolver-disagrees-with-current-atom-law",
         "The route's legacy resolver accepts policies the current v3 resolver refuses (the owner fixture basePolicy: "
         "ATOM_FILTER_FIELD_FORBIDDEN history-change.confidenceMillionths, yet the public route returns resolverAccepted=true; a target endpoint "
         "on relation file: ATOM_ENDPOINT_UNAVAILABLE) and refuses a V2 test-execution atom the v3 resolver admits.",
         POL["base-v1-owner-fixture"]["currentV3ResolvePolicy"].get("remedy", "").startswith("ATOM_FILTER_FIELD_FORBIDDEN")
         and POL["base-v1-owner-fixture"]["legacyResolvePolicy"]["outcome"] == "RETURNED"
         and SU["control-v1-owner-suite"][ROUTE]["result"]["resolverAccepted"] is True
         and POL["forbidden-target-v2"]["currentV3ResolvePolicy"].get("remedy", "").startswith("ATOM_ENDPOINT_UNAVAILABLE")
         and POL["forbidden-target-v2"]["legacyResolvePolicy"]["outcome"] == "RETURNED"
         and POL["test-filter-v2"]["currentV3ResolvePolicy"]["outcome"] == "RETURNED"
         and POL["test-filter-v2"]["legacyResolvePolicy"]["outcome"] == "REFUSED",
         {"baseV1": {k: POL["base-v1-owner-fixture"][k] for k in ("currentV3ResolvePolicy", "legacyResolvePolicy")},
          "forbiddenTargetV2": OBS["forbiddenTargetEndpoint"],
          "testFilterV2Legacy": POL["test-filter-v2"]["legacyResolvePolicy"]}),
    fact("F8-legacy-evaluator-ignores-endpoint",
         "DIAGNOSTIC BYPASS (not a product route): for an admitted-by-v3 V2 atom exists imports resolved-target endpoint=target over one "
         "fixture edge src/b.ts -> src/a.ts, the legacy evaluator's findings equal those for the same atom with the default source endpoint "
         "(finding on src/b.ts; the src/a.ts expectation is unmet).",
         OBS["bypassEndpointTargetFindingsEqualEndpointSourceFindings"]
         and [f["subject"] for c in OBS["bypassEndpointTargetResults"] for f in c["findings"]] == ["src/b.ts"]
         and OBS["bypassEndpointTargetResults"][0]["expectationOutcomes"] == ["unmet"],
         {"bypassEndpointTargetResults": OBS["bypassEndpointTargetResults"]}),
    fact("F9-v2-declared-member-classified-as-imperative-key",
         "A lawful V2 candidate whose only V1-undeclared member is Atom.endpoint is refused POLICY.IMPERATIVE_KEY_REFUSED (a hook/script/include/"
         "exec-key detail) rather than a major/profile refusal, because the classifier walks the V1 grammar.",
         SU["endpoint-target-v2-suite"]["selectedAdmission"].get("detail") == "POLICY.IMPERATIVE_KEY_REFUSED"
         and POL["endpoint-target-v2"]["currentV3ResolvePolicy"]["outcome"] == "RETURNED" and POL["endpoint-target-v2"]["grammarClassifierViolation"] is True,
         {"suite": "endpoint-target-v2-suite"}),
]
if failures:
    print(json.dumps({"refused": "proven fact does not hold", "failures": failures}, indent=1))
    sys.exit(1)

receipts = []
for d in sorted((HERE / "receipts").iterdir()):
    dig = json.loads((d / "digests.json").read_text())
    receipts.append({"label": d.name, "argv": json.loads((d / "command.json").read_text())["argv"], "exit": (d / "exit.txt").read_text().strip(),
                     "seconds": dig["seconds"], "stdoutSha256": dig["stdoutSha256"], "stderrSha256": dig["stderrSha256"],
                     "sourceUnchangedBeforeAndAfter": not any(dig[k]["mismatch"] or dig[k]["unlisted"] for k in ("sourceBefore", "sourceAfter"))})

review = {
    "artifact": "claude-policy-test-profile-assessment.review", "version": 1,
    "origin": "823bf66b-e92a-4789-ab81-63a1a9dc371d",
    "standing": ("Bounded READ-ONLY coauthor owner assessment over the FIXED captured intermediate source. Not independent final source "
                 "review, not acceptance, not product qualification; no source, LIVE, frozen or other-author artifact written; no author "
                 "correction made."),
    "question": "Does the CURRENT public policy-test command lawfully test the CURRENT PolicyDocumentV2 policy, or is there a real profile/owner migration gap?",
    "disposition": "REAL-GAP",
    "dispositionSummary": ("The evaluator3 policy.test route is not an intentionally selected legacy test scope: it admits only PolicyDocumentV1 "
                           "candidates and resolves/evaluates them with the legacy workflow1 resolver and evaluator, while the current contract "
                           "names PolicyDocumentV2 as the DSL, the policy-show carrier and the candidate/effective digest preimage. No published "
                           "transformation or dispatch bridge was found. A user cannot test a lawful current policy through the public route."),
    "custody": {"source": load("custody/source-verify.json"), "citedOwnerFiles": load("custody/cited-owner-files.json")["files"],
                "probeOutput": {"path": "probes/output/policy-test-profile-probe.json", "sha256": fsha("probes/output/policy-test-profile-probe.json")},
                "probeScriptSha256": fsha("probes/policy_test_profile_probe.py"), "receiptLauncherSha256": fsha("run_with_receipt.py"),
                "builderSha256": fsha("build_review.py")},
    "selectors": [
        {"at": "docs/v2/contracts/product-v1/workflows-and-surfaces.md:35-39", "text": "Embedded policy uses policy-document.v2.schema.json (PolicyDocumentV2). Unchanged scope, waiver, import, test and operational records keep their explicitly selected owners. Historical output schemas remain retained evidence and are not an alternative parser for this profile."},
        {"at": "workflows-and-surfaces.md:590", "text": "DSL. PolicyDocumentV2 is closed data: rules with a ruleProgramRef ..."},
        {"at": "workflows-and-surfaces.md:628-649", "text": "Authoring test. opensip policy test SUITE ... supplies the candidate policy ... A candidate policy carrying a member that no closed alternative of the policy grammar declares ... is POLICY.IMPERATIVE_KEY_REFUSED"},
        {"at": "workflows-and-surfaces.md:1402-1407", "text": "PolicyTestResultV1.suiteDigest is ... H(\"workflow.policy-test-suite\", PolicyTestSuiteV1) ... Candidate/effective policy digests remain raw SHA-256 of their respective closed PolicyDocumentV2 canonical bytes."},
        {"at": "workflows-and-surfaces.md:1199-1200", "text": "policy-show EffectivePolicyRecordV1 policy (PolicyDocumentV2); policy-test PolicyTestResultRecordV1 result (PolicyTestResultV1, resolverAccepted=true only)"},
        {"at": "workflows-and-surfaces.md:1552-1557", "text": "A non-gating rule's unknown result remains unknown for policy-test finding/no-finding expectations"},
        {"at": "workflows/schemas/policy-test.schema.json:5,335-337", "text": "A suite tests a candidate PolicyDocumentV1 before enforcement; candidatePolicy $ref urn:opensip:product-v1:workflows:policy-document#/$defs/PolicyDocumentV1"},
        {"at": "workflows/workflows_model.v3.py:1-10", "text": "Evaluator3 policy owner. Historical workflow1 is a separate compatibility profile. (imports every legacy global)"},
        {"at": "workflows/workflows_model.v3.py:13-55", "text": "v3 rule_program_digest (major 2), admit_atom via foundation atom owner, admit_policy_rule, resolve_policy overrides"},
        {"at": "workflows/workflows_model.v3.py:157-220", "text": "POLICY_TEST_SUITE_REF PolicyTestSuiteV1; _policy_grammar reads schemas/policy-document.schema.json; classifier root PolicyDocumentV1 (line 191); run_admitted_policy_test returns run_policy_test(admit_policy_test_suite(suite))"},
        {"at": "workflows/workflows_model.v1.py:1326-1355,1387-1393,1422-1454,1514-1565", "text": "legacy admit_atom (ladder/evidence only, no endpoint or kind applicability), resolve_policy, eval_pred (matches f['subject']==subject), run_policy_test"},
        {"at": "workflows/schemas/policy-document.v2.schema.json:330-337,692-722,986", "text": "Atom.endpoint source|target; PolicyDocumentV2 schemaMajor const 2; x-opensip-profile-major-law: Policy1 is not silently relabelled or evaluated as policy2"},
        {"at": "workflows/schemas/evaluator3/command-envelope.schema.json:740-805", "text": "EffectivePolicyRecordV1.policy -> PolicyDocumentV2; PolicyTestResultRecordV1.result -> policy-test#PolicyTestResultV1 with resolverAccepted const true"},
        {"at": "workflows/workflow-projection-contract.v3.md:46", "text": "ScopeDocumentV1 and WaiverSetV1 remain on urn:opensip:product-v1:workflows:policy-document. Baseline embedded policy is PolicyDocumentV2"},
        {"at": "workflows/workflow_projection_model.v3.py:148-167,335-336,621-622,1529-1530", "text": "profile registry loads both policy documents and policy-test; baseline/current/admitted-run projections refuse schemaMajor != 2 'PolicyDocumentV2 required'"},
        {"at": "foundation/identity-model.v3.py:1747-1749", "text": "Plan policy foreign payload workflows/schemas/policy-document.v2.schema.json #/$defs/PolicyDocumentV2; proof RuleProgramV2"},
        {"at": "workflows/README.md:15-17", "text": "schemas/policy-document.v2.schema.json owns PolicyDocumentV2; unchanged scope, waiver, import and test documents retain their declared schemas"},
        {"at": "foundation/shared-profile-decisions.v1.md:8", "text": "PolicyDocumentV2 schemaMajor2 and RuleProgramV2 schemaVersion2 own atom endpoint/test filters; Scope/Waiver1 unchanged owner"},
        {"at": "foundation/evaluator-projection-registry.v1.json#/kindApplicability,/relations/imports,/relations/file", "text": "endpointTarget uses relation.targetKinds; imports endpointTarget admitted-at-rung resolved-target; file endpointTarget forbidden"},
        {"at": "foundation/atom_model.v1.py:743-787", "text": "_native_occupancy: endpoint target matches the fact's target native id/targetUniverse, not its source"},
        {"at": "workflows/check-workflow-projection.v3.py:3613-3646,3688-3692", "text": "current checker routes only the retained workflow-cases.v1.json V1 policySuite through run_policy_test / run_admitted_policy_test; grammar checks read the V1 policy-document schema"},
    ],
    "provenFacts": facts,
    "inferences": [
        {"id": "I1-not-intentional-legacy-scope", "statement": "The dispatch sentence 'Unchanged ... test ... records keep their explicitly selected owners' does not select a V1 candidate policy for policy.test: the same paragraph puts embedded policy on PolicyDocumentV2, section 10 defines the policy-test candidate/effective digests over PolicyDocumentV2 bytes, section 5 defines the DSL and 'the policy grammar' as PolicyDocumentV2, and 'test' is most naturally the retained test-execution document listed beside scope/waiver/import in workflows/README.md. No source text states that the current profile tests V1 candidates.", "basis": "selectors; bounded text search"},
        {"id": "I2-v1-candidate-is-not-enforceable-in-this-profile", "statement": "A V1 candidate that passes the current test cannot be the enforced current policy without a relabel the V2 profile law forbids: Plan admission, policy-show and every evaluator3 projection require PolicyDocumentV2.", "basis": "F6 plus identity-model.v3.py:1747, workflow_projection_model.v3.py:335/621/1529, policy-document.v2 x-opensip-profile-major-law"},
        {"id": "I3-fixture-target-semantics", "statement": "Under V2 atom law an endpoint=target atom over the fixture edge would be decided for the target subject (src/a.ts), not the source; the legacy evaluator's source-side result (F8) is therefore not the V2 meaning. Not executed through the atom owner here (its inputs are Run-shaped, not suite fixtures).", "basis": "atom_model.v1.py:743-787; registry kindApplicability"},
        {"id": "I4-v2-test-filters-not-expressible-in-facts-fixture", "statement": "FactRecordCandidate carries no testResult/exitStatus and a facts case supplies only evidenceAvailable kinds, so a V2 test-execution filter atom cannot be decided by the facts fixture; a successor must say whether such a rule is indeterminate, not-executable or refused.", "basis": "policy-test.schema.json FactRecordCandidate; policy-document.v2 FieldFilter"},
    ],
    "notCountedKnownDefects": [
        {"id": "oc2-owner-string-expression-case-is-policy-imperative-key-refused", "why": "the known unrelated grammar-classifier failure (root checker-stdout.json /failed/0: CONFIG.INVALID/CONFIG.INVALID); not re-reported. F9 is a different route (a V2-declared member, not a string expression) that follows from the V1 grammar selection; root should de-duplicate if the separate grammar correction changes the classifier document."},
        {"id": "repair-join-defects", "why": "being corrected separately; not touched by this assessment"},
    ],
    "correctionPlanForRootReview": {
        "standing": "PROPOSAL ONLY; nothing applied; minimal coherent owner correction; root decides selectors, majors and details.",
        "steps": [
            "1. Suite: publish an evaluator3-profile policy-test suite definition whose candidatePolicy is urn:opensip:product-v1:policy-document:2#/$defs/PolicyDocumentV2 (overrides Severity and waivers WaiverSetV1 unchanged). Because the suite schemaMajor is the published dispatch member inside H(workflow.policy-test-suite) and the admitted candidate set changes incompatibly (V1 candidates must refuse in this profile), recommend PolicyTestSuiteV2 (schemaMajor 2); retain PolicyTestSuiteV1 for the historical workflow1 profile and check_workflows.v1 unchanged.",
            "2. Result: keep PolicyTestResultV1, policytest2 identity and the PolicyTestResultRecordV1 carrier; section 10 already defines candidate/effective digests over PolicyDocumentV2 bytes, so no result major bump is required. Correct only the suite/result description text that says PolicyDocumentV1.",
            "3. Owner: in workflows_model.v3, admit the successor suite; refuse a V1 candidate typed (no coercion or relabel) with a root-selected registered detail; point the grammar classifier at policy-document.v2 rooted at PolicyDocumentV2 (coordinate with the separate string-expression classifier correction).",
            "4. Evaluator: define the evaluator3 authoring-test function in the v3 profile (do not call the imported legacy run_policy_test, whose globals bind the legacy resolver/evaluator): resolve with the v3 resolve_policy/atom owner, and evaluate V2 atoms including endpoint=target over FactRecordCandidate target paths and kind applicability; state the decision for V2 test-execution/test-result filter atoms under a facts fixture (I4).",
            "5. Contract text: section 5 authoring test names the successor suite and PolicyDocumentV2 candidate; clarify that the dispatch paragraph's 'test' records are test-execution documents; command-inventory.v3 policy-test goldens unchanged in class/code, plus a V1-candidate-refused golden.",
            "6. Checks: route an owner-admitted PolicyDocumentV2 suite through run_admitted_policy_test to a carried result; V1 candidate refused; endpoint=target discrimination; legacy-resolver-only policy (e.g. confidenceMillionths on history-change) refused; historical check_workflows.v1 V1 route retained byte-unchanged.",
        ],
    },
    "limits": [
        "Probe-authored V2 policies are admitted independently by the V2 schema, the v3 resolve_policy and EffectivePolicyRecordV1; base-v2-probe, endpoint-source-v2 and forbidden-target-v2 are NOT lawful under the v3 owner and are excluded from F3.",
        "The DIAGNOSTIC BYPASS calls legacy run_policy_test directly; it is not a product route and does not show what a corrected owner should return.",
        "The full check-workflow-projection.v3.py checker and full source were not rerun or reviewed; root's recorded checker result (1 known failure) was read only to exclude known defects.",
        "Target-endpoint V2 semantics were read from the atom owner and registry, not executed through it for suite fixtures (I3).",
        "Bridge/transformation search is a bounded text search of the fixed source (relabel/convert/bridge/upgrade/downgrade/migrate near policy, PolicyDocumentV1 selectors); absence is not proof of absence outside this capture.",
        "Sources-kind cases, host non-fixture execution, product implementation and the 30 independent grades are out of scope.",
    ],
    "receipts": receipts,
}
text = json.dumps(review, indent=1) + "\n"
(HERE / "review.json").write_text(text)
print(json.dumps({"review.json": hashlib.sha256(text.encode()).hexdigest(), "disposition": review["disposition"],
                  "provenFacts": {f["id"]: f["holds"] for f in facts}, "lawfulCurrentV2": lawful_v2,
                  "receipts": [(r["label"], r["exit"], r["sourceUnchangedBeforeAndAfter"]) for r in receipts]}, indent=1))
