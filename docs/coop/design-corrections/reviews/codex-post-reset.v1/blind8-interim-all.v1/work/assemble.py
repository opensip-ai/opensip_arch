"""Assembles a complete retained Run graph over a Fixture."""
from __future__ import annotations

import hashlib
import struct

import build
import capman
import closure as CL
import osip
import schemas
from build import Fixture, coverage_entry
from osip import C, H, ident, raw_sha256, record_digest


class Assembly:
    def __init__(self, fx: Fixture, capabilities, spec_rows, spec_parameters=None,
                 policy=None, waivers=None, grant_ops=("read-source", "native-analysis"),
                 budget_limit=100000, scope=None, vcs_kind="git",
                 capability_manifest=None):
        self.fx = fx
        self.capabilities = capabilities
        self.spec_rows = spec_rows
        self.spec_parameters = spec_parameters or []
        self.policy = policy or build.MINIMAL_POLICY
        self.waivers = waivers or build.EMPTY_WAIVERS
        self.grant_ops = grant_ops
        self.budget_limit = budget_limit
        self.scope = scope
        self.vcs_kind = vcs_kind
        self.capability_manifest = capability_manifest
        self.contexts = {}       # bare hex -> (domain, descriptor)
        self.universes = {}      # bare hex -> (domain, descriptor)
        self.scopes = []         # (scope2id, descriptor)
        self.facts = []          # (fact2id, descriptor)
        self.coverages = []      # (coverage2id, descriptor, payload)
        self.view_parts = []

    # -- native records ----------------------------------------------------
    def add_context(self, domain, desc, selector):
        h = self.fx.hid(domain, desc, "native", selector, domain)
        self.contexts[h] = (domain, desc)
        return h

    def add_universe(self, domain, desc, selector, label):
        h = self.fx.hid(domain, desc, "native", selector, label)
        self.universes[h] = (domain, desc)
        return h

    # -- snapshot / plan ---------------------------------------------------
    def seal_snapshot(self):
        fx = self.fx
        inv = fx.inventory()
        self.inv = {r["path"]: r for r in inv}
        fx.s.put_record(inv, "source-inventory")
        vcs = {"schemaVersion": 2, "kind": self.vcs_kind,
               "commitId": None if self.vcs_kind == "none" else "c" * 40,
               "dirty": False, "sourceInventoryDigest": record_digest(inv)}
        self.vcs_digest = fx.rec(vcs, "identity", "#/$defs/vcs-observation", "vcs")
        sc = self.scope or build.scope_descriptor(["."], [], [])
        self.scope_digest = fx.rec(sc, "identity", "#/$defs/scope-descriptor", "scope-descriptor")
        cfg = build.default_semantic_config(self.capabilities, self.budget_limit)
        self.config_digest = fx.rec(cfg, "identity", "#/$defs/semantic-configuration",
                                    "semantic-configuration")
        snap = {"schemaVersion": 2, "projectId": fx.project_id, "sourceInventory": inv,
                "resolvedConfigDigest": self.config_digest,
                "scopeDigest": self.scope_digest, "vcsDigest": self.vcs_digest}
        self.snapshot = snap
        self.snapshot_id = "snapshot2:" + fx.hid("snapshot", snap, "identity",
                                                 "#/$defs/snapshot", "snapshot")
        return self.snapshot_id

    def seal_plan(self, semantic_closures, import_ids=()):
        fx = self.fx
        spec = build.analysis_spec(self.spec_rows, self.spec_parameters)
        self.spec_digest = fx.rec(spec, "identity", "#/$defs/analysis-spec", "analysis-spec")
        grant = build.semantic_grant(fx.project_id, semantic_closures,
                                     self.grant_ops, self.scope_digest)
        self.grant_digest = fx.rec(grant, "identity", "#/$defs/semantic-grant", "semantic-grant")
        self.policy_digest = fx.rec(self.policy, "policy-document",
                                    "#/$defs/PolicyDocumentV1", "policy")
        self.waiver_digest = fx.rec(self.waivers, "policy-document",
                                    "#/$defs/WaiverSetV1", "waivers")
        cm = self.capability_manifest
        committed = capman.commit(cm)
        cm_bytes_digest = fx.s.put_raw(committed, "capability-manifest-artifact")
        plan = {"schemaVersion": 2, "snapshotId": self.snapshot_id,
                "capabilityManifestId": osip.capability_manifest_id(committed),
                "semanticClosures": sorted(set(semantic_closures), key=lambda x: C(x)),
                "analysisSpecDigest": self.spec_digest,
                "resolvedConfigDigest": self.config_digest,
                "nativeContextDigests": sorted(self.contexts, key=lambda x: C(x)),
                "importIds": sorted(import_ids, key=lambda x: C(x)),
                "policyDigest": self.policy_digest,
                "waiverDigest": self.waiver_digest,
                "scopeDigest": self.scope_digest,
                "budget": {"unit": "work-units", "limit": self.budget_limit},
                "semanticGrantDigest": self.grant_digest,
                "capabilityManifestBytesDigest": cm_bytes_digest}
        self.plan = plan
        self.plan_id = "plan2:" + fx.hid("plan", plan, "identity", "#/$defs/plan", "plan")
        self.semantic_closures = plan["semanticClosures"]
        return self.plan_id

    # -- native evidence ---------------------------------------------------
    def add_scope(self, relation, rung, source_u, target_u, enumerator, subjects,
                  label=""):
        d = {"schemaVersion": 2, "snapshotId": self.snapshot_id,
             "sourceUniverse": source_u, "targetUniverse": target_u,
             "relation": relation, "resolution": rung,
             "enumeratorClosure": enumerator,
             "subjects": sorted(set(subjects), key=lambda x: C(x))}
        h = self.fx.hid("subject-scope", d, "identity", "#/$defs/subject-scope",
                        "scope:%s@%s %s" % (relation, rung, label))
        sid = "scope2:" + h
        self.scopes.append((sid, d))
        return sid, h

    def add_fact(self, relation, rung, source_u, target_u, producer, payload, anchors,
                 confidence=1000000, label=""):
        row = CL.RELATIONS[relation]
        self.fx.rec(payload, "relation", row["selector"], "payload:" + relation)
        d = {"schemaVersion": 2, "snapshotId": self.snapshot_id,
             "relation": relation, "resolution": rung,
             "sourceUniverse": source_u, "targetUniverse": target_u,
             "producerClosure": producer,
             "payloadSchemaDigest": build.RELATION_DOC_DIGEST,
             "payloadDigest": record_digest(payload),
             "anchors": sorted(anchors, key=lambda a: C(a)),
             "confidenceMillionths": confidence}
        h = self.fx.hid("fact", d, "identity", "#/$defs/fact",
                        "fact:%s@%s %s" % (relation, rung, label))
        fid = "fact2:" + h
        self.facts.append((fid, d))
        return fid

    def add_coverage(self, scope_id, scope_hex, entry):
        payload = {"schemaVersion": 3,
                   "key": {"relation": entry["relation"],
                           "resolution": entry["resolution"],
                           "sourceUniverse": self._scope(scope_id)["sourceUniverse"],
                           "targetUniverse": self._scope(scope_id)["targetUniverse"],
                           "subjectScopeCommitment": "sha256:" + scope_hex},
                   "entry": entry}
        pd = self.fx.rec(payload, "native", "#/$defs/CoverageResultV3", "coverage-payload")
        d = {"schemaVersion": 2, "scopeId": scope_id,
             "payloadSchemaDigest": build.NATIVE_DOC_DIGEST, "payloadDigest": pd}
        h = self.fx.hid("coverage", d, "identity", "#/$defs/coverage",
                        "coverage:%s@%s" % (entry["relation"], entry["resolution"]))
        cid = "coverage2:" + h
        self.coverages.append((cid, d, payload))
        return cid

    def _scope(self, sid):
        for s, d in self.scopes:
            if s == sid:
                return d
        raise KeyError(sid)

    # -- view / proof / seal ----------------------------------------------
    def seal_view(self, producer, scope_ids, fact_ids, coverage_ids, schema_digests):
        d = {"schemaVersion": 2, "planId": self.plan_id,
             "scopeIds": sorted(set(scope_ids), key=lambda x: C(x)),
             "facts": sorted(set(fact_ids), key=lambda x: C(x)),
             "coverageIds": sorted(set(coverage_ids), key=lambda x: C(x)),
             "producerClosure": producer,
             "schemaDigests": sorted(set(schema_digests), key=lambda x: C(x))}
        h = self.fx.hid("view", d, "identity", "#/$defs/view", "view")
        vid = "view2:" + h
        self.views = getattr(self, "views", [])
        self.views.append((vid, d))
        return vid

    def seal_run(self, evaluator_closure, producer_closure, view_ids,
                 predicate_value="false", verdict="pass"):
        fx = self.fx
        stage_spec = {"schemaVersion": 2, "planId": self.plan_id,
                      "producerClosure": producer_closure,
                      "operation": "native.analyze", "parameters": [],
                      "outputDomains": sorted(["fact", "coverage", "subject-scope", "view"],
                                              key=lambda x: C(x)),
                      "outputSchemaDigest": build.NATIVE_DOC_DIGEST}
        ssd = fx.rec(stage_spec, "identity", "#/$defs/stage-spec", "stage-spec")
        execplan = {"schemaVersion": 2, "planId": self.plan_id,
                    "stages": [{"ordinal": 0, "stageSpecDigest": ssd, "requires": [],
                                "outputDomains": stage_spec["outputDomains"]}]}
        epid = "exec-plan2:" + fx.hid("execution-plan", execplan, "identity",
                                      "#/$defs/execution-plan", "execution-plan")
        prog = build.rule_program(self.policy, self.policy_digest)
        prog_digest = fx.rec(prog, "policy-document", "#/$defs/RuleProgramV1", "rule-program")
        rule = self.policy["rules"][0]
        node = rule["emitWhen"]
        gp = {"schemaVersion": 2, "ruleProgramDigest": prog_digest,
              "ruleId": rule["ruleId"], "predicateId": "p",
              "operation": node["op"], "nodeDigest": record_digest(node)}
        fx.rec(node, "policy-document", "#/$defs/Predicate", "predicate-node")
        gpd = fx.rec(gp, "identity", "#/$defs/program-predicate", "program-predicate")
        cov_ids = sorted({c for c, _, _ in self.coverages}, key=lambda x: C(x))
        witness = {"schemaVersion": 2, "programPredicateDigest": gpd,
                   "matchingFactIds": [], "coverageIds": cov_ids,
                   "countLimit": None, "childPredicateIds": []}
        wd = fx.rec(witness, "identity", "#/$defs/predicate-witness", "predicate-witness")
        input_refs = ([{"domain": "view", "digest": suffix_(v)} for v in view_ids]
                      + [{"domain": "coverage", "digest": suffix_(c)} for c in cov_ids]
                      + [{"domain": "rule-program", "digest": prog_digest},
                         {"domain": "policy", "digest": self.policy_digest},
                         {"domain": "waiver", "digest": self.waiver_digest},
                         {"domain": "analysis-spec", "digest": self.spec_digest},
                         {"domain": "configuration", "digest": self.config_digest}])
        input_refs.sort(key=lambda r: C(r))
        pp = {"ruleId": rule["ruleId"], "subjectId": "repository",
              "predicateId": "p", "operation": node["op"],
              "inputRefs": input_refs,
              "scopeIds": sorted({s for s, _ in self.scopes}, key=lambda x: C(x)),
              "value": predicate_value, "witnessDigest": wd}
        proof = {"schemaVersion": 2, "planId": self.plan_id, "executionPlanId": epid,
                 "evaluatorClosure": evaluator_closure,
                 "ruleProgramDigest": prog_digest,
                 "evaluationInputRefs": input_refs,
                 "predicateProofs": [pp], "findingIds": [], "verdict": verdict}
        pid = "proof2:" + fx.hid("proof-bundle", proof, "identity",
                                 "#/$defs/proof-bundle", "proof-bundle")
        evidence = {"schemaVersion": 2, "planId": self.plan_id,
                    "viewIds": sorted(view_ids, key=lambda x: C(x)),
                    "coverageIds": cov_ids, "importIds": self.plan["importIds"],
                    "findingIds": [], "proofBundleId": pid}
        eid = "evidence2:" + fx.hid("semantic-evidence", evidence, "identity",
                                    "#/$defs/semantic-evidence", "semantic-evidence")
        seal = {"schemaVersion": 2, "planId": self.plan_id, "executionPlanId": epid,
                "evidenceId": eid, "evaluatorClosure": evaluator_closure,
                "policyDigest": self.policy_digest, "proofBundleId": pid,
                "verdict": verdict}
        sid = "seal2:" + fx.hid("evaluation-seal", seal, "identity",
                                "#/$defs/evaluation-seal", "evaluation-seal")
        run = {"schemaVersion": 2, "projectId": fx.project_id,
               "snapshotId": self.snapshot_id, "planId": self.plan_id,
               "evidenceId": eid, "evaluationSealId": sid,
               "capabilityManifestId": self.plan["capabilityManifestId"]}
        rid = "run2:" + fx.hid("run", run, "identity", "#/$defs/run", "run")
        self.run_id = rid
        self.run = run
        return rid


def suffix_(x):
    return x.split(":", 1)[1]
