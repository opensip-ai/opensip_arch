import json, sys
sys.path.insert(0, "/tmp/opensip-design-corrections/consumer-b.v8/output/work")
import closure as CL, osip, schemas, run_ts_config
from osip import C

F = json.load(open("/tmp/opensip-design-corrections/consumer-b.v8/output/vectors-gaps.json"))

# --- G4: stage-spec.operation / outputDomains carry no named vocabulary -----
D = schemas.LOADED["identity"]["$defs"]
op = D["stage-spec"]["properties"]["operation"]
od = D["stage-spec"]["properties"]["outputDomains"]["items"]
epod = D["execution-plan"]["properties"]["stages"]["items"]["properties"][
    "outputDomains"]["items"]
print("stage-spec.operation        :", json.dumps(op))
print("stage-spec.outputDomains[]  :", json.dumps(od))
print("execution-plan .outputDomains[]:", json.dumps(epod))
cap = D["analysis-spec"]["properties"]["requestedCapabilities"]["items"][
    "properties"]["capabilityId"]
print("compare: analysis-spec.capabilityId carries x-opensip-vocabulary:",
      "x-opensip-vocabulary" in cap)
has_vocab = any("x-opensip-vocabulary" in x for x in (op, od, epod))
F.append({
    "id": "CB-GAP-4", "severity": "SHOULD",
    "title": "stage-spec.operation and both outputDomains arrays are unbounded "
             "Text with NO named vocabulary, while stageSpecDigest enters "
             "exec-plan2 -> proof2 -> seal2 -> RunId",
    "observedResult":
        "stage-spec.operation is %r; stage-spec.outputDomains items are %r; "
        "execution-plan stage outputDomains items are %r. None carries an "
        "x-opensip-vocabulary annotation, while the SIBLING field "
        "analysis-spec.requestedCapabilities[].capabilityId does (%s)."
        % (op, od, epod, "x-opensip-vocabulary" in cap),
    "whatAClosedContractWouldHaveDone":
        "exactly what CB4-SHOULD-2 did for capabilityId and what "
        "x-opensip-config-node-kind-law did for TypeScriptConfigGraphV1.kind: "
        "name the authority beside the field",
    "detail": {
        "selectors": ["foundation/identity-schemas.v2.json#/$defs/stage-spec/"
                      "properties/operation",
                      "foundation/identity-schemas.v2.json#/$defs/stage-spec/"
                      "properties/outputDomains/items",
                      "foundation/identity-schemas.v2.json#/$defs/execution-plan/"
                      "properties/stages/items/properties/outputDomains/items"],
        "consequence": "Two conforming hosts describing ONE stage of one analysis "
                       "may write `native.analyze` and `analyze`, or "
                       "`subject-scope` and `scope2`, and mint different "
                       "stageSpecDigests, different exec-plan2, different proof2, "
                       "different seal2 and different RunIds. That is the exact "
                       "independent-replay-across-machines property "
                       "identity-and-evidence section 6 requires.",
        "notMitigatedBy": "identity section 3 requires only that a stage spec's "
                          "outputDomains EQUAL the stage's - an internal "
                          "consistency rule between two places that may both be "
                          "spelled the same wrong way."},
    "measuredBy": "schema inspection of the three selectors above and of the "
                  "sibling field that DOES carry the annotation"})
print("\nCB-GAP-4 recorded (has any vocabulary annotation:", has_vocab, ")")

# --- G5: plan.semanticClosures membership is stated for ONE field only ------
fx, A, run_id = run_ts_config.build_run("synthesized", seed="closures")
plan = osip.parse_frame(fx.s.blobs[A.plan_id.split(":")[1]])[1]
print("\nplan.semanticClosures as I built it:", len(plan["semanticClosures"]))
narrow = dict(plan)
# drop the toolchain and stdlib closures: nothing in the kit requires them
keep = []
for cid in plan["semanticClosures"]:
    dom, cl = osip.parse_frame(fx.s.blobs[cid.split(":")[1]])
    if cl["kind"] in ("provider", "evaluator", "detector"):
        keep.append(cid)
narrow["semanticClosures"] = sorted(keep, key=lambda x: C(x))
nh = fx.s.put_h("plan", narrow)


def rekey(fx, A, plan_hex):
    pid = "plan2:" + plan_hex
    seal = osip.parse_frame(fx.s.blobs[A.run["evaluationSealId"].split(":")[1]])[1]
    ev = osip.parse_frame(fx.s.blobs[seal["evidenceId"].split(":")[1]])[1]
    proof = osip.parse_frame(fx.s.blobs[seal["proofBundleId"].split(":")[1]])[1]
    ep = osip.parse_frame(fx.s.blobs[proof["executionPlanId"].split(":")[1]])[1]
    ep = dict(ep); ep["planId"] = pid
    eph = fx.s.put_h("execution-plan", ep)
    proof = dict(proof); proof["planId"] = pid
    proof["executionPlanId"] = "exec-plan2:" + eph
    ph = fx.s.put_h("proof-bundle", proof)
    ev = dict(ev); ev["planId"] = pid; ev["proofBundleId"] = "proof2:" + ph
    eh = fx.s.put_h("semantic-evidence", ev)
    seal = dict(seal); seal["planId"] = pid; seal["evidenceId"] = "evidence2:" + eh
    seal["proofBundleId"] = "proof2:" + ph; seal["executionPlanId"] = "exec-plan2:" + eph
    sh = fx.s.put_h("evaluation-seal", seal)
    run = dict(A.run); run["planId"] = pid; run["evidenceId"] = "evidence2:" + eh
    run["evaluationSealId"] = "seal2:" + sh
    return "run2:" + fx.s.put_h("run", run)


# the views/facts/scopes still name the ORIGINAL plan2, so re-mint them too is
# out of scope; instead assert the SCHEMA and MEMBERSHIP question directly.
scope_desc = schemas.LOADED["identity"]["$defs"]["subject-scope"]["properties"][
    "enumeratorClosure"].get("description", "")
fact_desc = schemas.LOADED["identity"]["$defs"]["fact"]["properties"][
    "producerClosure"].get("description", "")
print("subject-scope.enumeratorClosure states membership:",
      "plan.semanticClosures" in scope_desc)
print("fact.producerClosure states membership:",
      "plan.semanticClosures" in fact_desc, "(description present:",
      bool(fact_desc), ")")
F.append({
    "id": "CB-GAP-5", "severity": "SHOULD",
    "title": "the membership rule for plan.semanticClosures is published for "
             "EXACTLY ONE field and for no other closure the graph names",
    "observedResult":
        "subject-scope.enumeratorClosure's own description states `The closure "
        "must also be a member of plan.semanticClosures`; fact.producerClosure, "
        "view.producerClosure, stage-spec.producerClosure, cache-key."
        "producerClosure, proof-bundle.evaluatorClosure, evaluation-seal."
        "evaluatorClosure, finding.ruleClosure, import.producerClosure, "
        "import.adapterClosure and the native context's toolchain / stdlib / "
        "rust-dev-llvm / grammar closures carry NO such statement (measured: "
        "fact.producerClosure description present = %s)" % bool(fact_desc),
    "whatAClosedContractWouldHaveDone":
        "state the membership set once - which closure kinds a Plan must select "
        "and which it must not - the way x-opensip-digest-domains.closureKinds "
        "already states which KIND each closure-bearing field admits",
    "detail": {
        "selectors": ["foundation/identity-schemas.v2.json#/$defs/plan/properties/"
                      "semanticClosures",
                      "foundation/identity-schemas.v2.json#/$defs/subject-scope/"
                      "properties/enumeratorClosure (the one field that states it)",
                      "foundation/identity-schemas.v2.json#/x-opensip-digest-"
                      "domains/closureKinds/byField (states KIND, not membership)"],
        "consequence": "plan.semanticClosures is a canonical SET inside the Plan "
                       "descriptor, so it is a PlanId input. Two conforming hosts "
                       "analysing one repository with one toolchain can list "
                       "{provider, evaluator} or {provider, evaluator, toolchain, "
                       "stdlib} and mint different PlanIds and RunIds for the same "
                       "analysis. My own reconstruction had to CHOOSE, and I chose "
                       "to include the toolchain and stdlib closures.",
        "whatIDidNotClaim": "I did not construct a closing Run with the narrower "
                            "set, because every retained view, scope and fact "
                            "names the original plan2 and re-minting all of them "
                            "would be a second complete graph rather than a "
                            "discriminating control. The finding is about the "
                            "ABSENCE of a published membership rule, which is "
                            "established by the selectors above."},
    "measuredBy": "schema description inspection across every closure-bearing "
                  "field of identity-schemas.v2, plus the reconstruction choice "
                  "this absence forced on me"})
print("\nCB-GAP-5 recorded")

with open("/tmp/opensip-design-corrections/consumer-b.v8/output/vectors-gaps.json",
          "w") as f:
    json.dump(F, f, indent=1, sort_keys=True, default=str)
print("\ntotal findings:", len(F),
      [(g["id"], g["severity"]) for g in F])
