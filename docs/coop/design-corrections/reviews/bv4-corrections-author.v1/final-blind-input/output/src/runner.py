"""Assemble Plan -> derivation plan -> proof -> evidence -> seal -> Run and close it."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import fixtures as F  # noqa: E402
import graph as G  # noqa: E402
import kit  # noqa: E402
import osip  # noqa: E402

# A real, minimal PolicyDocumentV1 in the product DSL and its compiled program.
POLICY_RULE_ID = "no-clone-of-add"


def policy_and_program(rule_closure_hex, relation, min_resolution, subject_kind="file"):
    """A real PolicyDocumentV1 in the product DSL and its exact compiled projection."""
    predicate = {"op": "none", "relation": relation, "minResolution": min_resolution,
                 "filters": []}
    ref = {"contributionId": "first-party", "ruleStableId": POLICY_RULE_ID,
           "semanticsMajor": 2, "programDigest": rule_closure_hex}
    rule = {"ruleId": POLICY_RULE_ID, "ruleProgramRef": ref, "enabled": True,
            "severity": "warning", "gate": True,
            "subjectEnumeration": {"universe": "native", "subjectKind": subject_kind,
                                   "include": ["**"], "exclude": []},
            "emitWhen": predicate, "evidenceUse": []}
    policy = {"schemaFamily": "opensip.product.policy", "schemaMajor": 1,
              "gateSeverityAtLeast": "warning", "rules": [rule]}
    kit.validate("policy", "#/$defs/PolicyDocumentV1", policy)
    policy_digest = osip.canonical_record_digest(policy)
    program = {"schemaVersion": 1, "policyDigest": policy_digest,
               "rules": [{"ruleId": POLICY_RULE_ID, "ruleProgramRef": ref,
                          "emitWhen": predicate}]}
    kit.validate("policy", "#/$defs/RuleProgramV1", program)
    # Membership of THIS atom relation ladder is the SUFFICIENT condition and is
    # enforced at Run closure over both the policy and the compiled program.
    ladder = kit.doc("relation")["x-opensip-relation-registry"]["relations"]
    row = ladder.get(relation)
    if row is None or min_resolution not in row["ladder"]:
        raise G.Refusal("atom-minResolution-not-a-rung-of-this-relations-ladder",
                        "%s@%s" % (relation, min_resolution))
    return policy, program, predicate


def assemble(scn, verdict="pass", predicate_value="false", relation="clones",
             min_resolution="normalized-body-hash", extra_contexts=(),
             extra_universes=(), imports=(), analysis_parameters=(),
             semantic_operations=("native-analysis", "read-source")):
    store = scn["store"]
    snap = scn["snapshot"]
    uni = scn["universe"]
    ctx = scn["context"]
    prov, ev, rc = scn["provider"], scn["evaluator"], scn["rule"]

    contexts = [ctx] + list(extra_contexts)
    universes = [uni] + list(extra_universes)

    cap = G.make_capability_manifest(store, F.capability_manifest([{
        "providerId": prov["id"], "language": scn.get("language", "typescript"),
        "providerVersionSource": "signed-closure-manifest",
        "toolchainIdentitySource": "native-context",
        "relations": scn.get("declaredRelations",
                             {"file": "enumerated", "package": "manifest-declared",
                              "clones": "normalized-body-hash",
                              "references": "resolved-binding",
                              "unresolved-edge": "observed"}),
        "platformIds": [F.PLATFORM]}]))

    policy, program, predicate = policy_and_program(
        rc["hex"], relation, min_resolution)
    store.put_record(policy)
    program_digest = store.put_record(program)

    spec = {"schemaVersion": 2,
            "requestedCapabilities": sorted(
                [{"capabilityId": "%s@%s" % (relation, min_resolution),
                  "languageMode": scn.get("languageMode", "js-allowjs"),
                  "workspaceRoot": ".", "required": True}],
                key=lambda x: osip.c_encode(x)),
            "policyPackIds": ["blind.consumer.b"],
            "parameters": sorted(analysis_parameters, key=lambda p: osip.c_encode(p))}

    grant = {"schemaVersion": 2, "projectId": G.PROJECT_ID,
             "principals": [{"kind": "first-party", "closureId": prov["id"],
                             "ownerSourceDigest": None}],
             "analysisOperations": sorted(set(semantic_operations)),
             "scopeDigest": snap["scopeDigest"]}

    closures = sorted({c["id"] for c in (prov, ev, rc)}
                      | {c["id"] for c in scn.get("extraSemanticClosures", [])})

    waivers = {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1,
               "waivers": []}
    kit.validate("policy", "#/$defs/WaiverSetV1", waivers)
    plan = G.make_plan(store, snap, cap, closures, spec, contexts,
                       [i["id"] for i in imports], policy, waivers,
                       snap["scope"], dict(F.BUDGET), grant)

    exec_plan = G.make_execution_plan(store, plan, [{
        "producerClosure": prov["id"], "operation": "native.analyze",
        "parameters": spec["parameters"],
        "outputDomains": ["coverage", "fact", "subject-scope"],
        "outputSchemaDigest": kit.doc_digest("native"), "requires": []}])

    view = G.make_view(store, plan["id"], scn["scopes"], scn["facts"], scn["coverages"],
                       prov["id"], [kit.doc_digest("relation"), kit.doc_digest("native")])

    pp_digest, _ = G.make_program_predicate(store, program_digest, POLICY_RULE_ID,
                                            "p", predicate)
    matching = [f["id"] for f in scn["facts"]
                if f["descriptor"]["relation"] == relation]
    cov_ids = [c["id"] for c in scn["coverages"]
               if c["payload"]["entry"]["relation"] == relation]
    witness_digest, _ = G.make_witness(store, pp_digest,
                                       matching if predicate_value == "false" else [],
                                       cov_ids)

    input_refs = [{"domain": "view", "digest": view["hex"]},
                  {"domain": "rule-program", "digest": program_digest},
                  {"domain": "policy", "digest": plan["descriptor"]["policyDigest"]},
                  {"domain": "capability-manifest",
                   "digest": cap["capabilityManifestId"]},
                  {"domain": "analysis-spec",
                   "digest": plan["descriptor"]["analysisSpecDigest"]}]
    input_refs += [{"domain": "coverage", "digest": c["hex"]} for c in scn["coverages"]]
    input_refs += [{"domain": "native-context", "digest": c["hex"]} for c in contexts]
    input_refs += [{"domain": "import", "digest": i["hex"]} for i in imports]

    scope_ids = sorted({s["id"] for s in scn["scopes"]})
    proofs = [{"ruleId": POLICY_RULE_ID, "subjectId": "src", "predicateId": "p",
               "operation": predicate["op"],
               "inputRefs": sorted(input_refs, key=lambda r: osip.c_encode(r)),
               "scopeIds": scope_ids, "value": predicate_value,
               "witnessDigest": witness_digest}]

    findings = []
    if predicate_value == "true":
        findings.append(G.make_finding(
            store, POLICY_RULE_ID, 2,
            {"language": "typescript", "kind": "function", "logicalPath": "src/app.ts",
             "qualifiedName": "add",
             "discriminator": osip.raw_sha256(osip.c_encode(
                 ["function", "add", "(", "a", ",", "b", ")"]))},
            [], rc["id"], "CLONE.FOUND", {"count": 2}, "warning",
            [{"domain": "fact", "digest": scn["facts"][0]["hex"]}]))

    proof = G.make_proof(store, plan, exec_plan, ev["id"], program_digest,
                         input_refs, proofs, [f["id"] for f in findings], verdict)
    evidence = G.make_evidence(store, plan, [view], scn["coverages"],
                               [i["id"] for i in imports],
                               [f["id"] for f in findings], proof)
    seal = G.make_seal(store, plan, exec_plan, evidence, ev["id"], proof, verdict)
    run = G.make_run(store, snap, plan, evidence, seal, cap)

    all_closures = dict(scn["closures"])
    result = G.close_run(store, run, plan, snap, seal, evidence, proof, [view],
                         scn["facts"], scn["coverages"], scn["scopes"], contexts,
                         universes, all_closures, scn["retained"], cap, imports)
    return {"run": run, "plan": plan, "seal": seal, "evidence": evidence,
            "proof": proof, "view": view, "execPlan": exec_plan, "cap": cap,
            "closure": result, "policy": policy, "program": program,
            "analysisSpec": spec, "semanticGrant": grant}
