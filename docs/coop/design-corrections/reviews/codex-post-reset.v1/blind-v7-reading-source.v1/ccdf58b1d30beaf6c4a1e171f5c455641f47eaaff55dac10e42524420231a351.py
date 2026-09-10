"""Independently authored minimal descriptor vectors (blind consumer B, v7).

Every repository shape, every byte and every expected outcome below is chosen by
this session.  Nothing is copied from an author fixture; the kit contains no
author fixtures, models or checkers.
"""

import hashlib

import oslib as O
import graph as G
from oslib import C, H, sha256hex, raw_digest

PROJECT = "prj1-" + "a1" * 32


# ---------------------------------------------------------------------------
# generic constructors over a World
# ---------------------------------------------------------------------------
class Kit(object):
    def __init__(self, project=PROJECT):
        self.w = G.World(project)
        # every registered schema document the graph names is part of closure
        self.w.raw(O.doc_bytes("relation"))
        self.w.raw(O.doc_bytes("native"))
        self.w.raw(O.doc_bytes("identity"))
        self.w.raw(O.doc_bytes("policy-document"))

    # ---- raw repository -------------------------------------------------
    def file(self, path, text):
        return self.w.blob(path, text.encode("utf-8") if isinstance(text, str)
                           else text)

    def closure(self, kind, tree, semver, platform="macos-aarch64",
                protocol_major=3):
        rows = []
        for p, data in sorted(tree.items()):
            d = self.w.raw(data if isinstance(data, bytes) else data.encode())
            rows.append({"path": p, "sha256": d,
                         "bytes": len(data if isinstance(data, bytes)
                                      else data.encode())})
        rows.sort(key=lambda r: r["path"].encode("utf-8"))
        manifest = ("manifest:" + kind + ":" + semver + ":" + platform).encode()
        desc = {"schemaVersion": 2, "kind": kind,
                "manifestDigest": self.w.raw(manifest),
                "tree": rows, "semanticVersion": semver,
                "protocolMajor": protocol_major, "platform": platform}
        cid, _ = self.w.mint("closure", desc)
        return cid, desc

    def mint_native(self, domain, descriptor):
        _, hx = self.w.mint(domain, descriptor)
        return "sha256:" + hx, hx

    # ---- semantic objects ----------------------------------------------
    def snapshot(self, config, scope, vcs_kind="git", commit="c" * 40,
                 dirty=False):
        inv = sorted(self.w.inventory, key=lambda r: r["path"].encode("utf-8"))
        self.w.record(inv)
        vcs = {"schemaVersion": 2, "kind": vcs_kind,
               "commitId": commit if vcs_kind != "none" else None,
               "dirty": dirty, "sourceInventoryDigest": raw_digest(inv)}
        desc = {"schemaVersion": 2, "projectId": self.w.projectId,
                "sourceInventory": inv,
                "resolvedConfigDigest": self.w.record(config),
                "scopeDigest": self.w.record(scope),
                "vcsDigest": self.w.record(vcs)}
        sid, _ = self.w.mint("snapshot", desc)
        return sid, desc

    def scope(self, snapshot_id, source_u, target_u, relation, rung,
              enumerator, subjects):
        desc = {"schemaVersion": 2, "snapshotId": snapshot_id,
                "sourceUniverse": source_u, "targetUniverse": target_u,
                "relation": relation, "resolution": rung,
                "enumeratorClosure": enumerator,
                "subjects": sorted(set(subjects), key=lambda s: C(s))}
        sid, hx = self.w.mint("subject-scope", desc)
        return sid, hx, desc

    def fact(self, snapshot_id, relation, rung, source_u, target_u, producer,
             payload, anchors, confidence=1000000):
        desc = {"schemaVersion": 2, "snapshotId": snapshot_id,
                "relation": relation, "resolution": rung,
                "sourceUniverse": source_u, "targetUniverse": target_u,
                "producerClosure": producer,
                "payloadSchemaDigest": G.REL_DOC_DIGEST,
                "payloadDigest": self.w.record(payload),
                "anchors": sorted(anchors, key=lambda a: C(a)),
                "confidenceMillionths": confidence}
        fid, _ = self.w.mint("fact", desc)
        return fid, desc

    def coverage(self, scope_id, scope_hx, scope_desc, entry_over):
        commit = "sha256:" + scope_hx
        entry = dict(entry_over)
        entry.setdefault("relation", scope_desc["relation"])
        entry.setdefault("resolution", scope_desc["resolution"])
        entry["examinedUniverse"] = {"subjectScopeCommitment": commit,
                                     "subjectCount": len(scope_desc["subjects"])}
        payload = {"schemaVersion": 3,
                   "key": {"relation": scope_desc["relation"],
                           "resolution": scope_desc["resolution"],
                           "sourceUniverse": scope_desc["sourceUniverse"],
                           "targetUniverse": scope_desc["targetUniverse"],
                           "subjectScopeCommitment": commit},
                   "entry": entry}
        desc = {"schemaVersion": 2, "scopeId": scope_id,
                "payloadSchemaDigest": G.NATIVE_DOC_DIGEST,
                "payloadDigest": self.w.record(payload)}
        cid, _ = self.w.mint("coverage", desc)
        return cid, desc, payload

    def view(self, plan_id, scope_ids, fact_ids, coverage_ids, producer,
             schema_digests):
        desc = {"schemaVersion": 2, "planId": plan_id,
                "scopeIds": sorted(set(scope_ids), key=lambda s: C(s)),
                "facts": sorted(set(fact_ids), key=lambda s: C(s)),
                "coverageIds": sorted(set(coverage_ids), key=lambda s: C(s)),
                "producerClosure": producer,
                "schemaDigests": sorted(set(schema_digests), key=lambda s: C(s))}
        vid, _ = self.w.mint("view", desc)
        return vid, desc


NOT_APPLICABLE_RC = {"state": "not-applicable", "attempted": False,
                     "examinedExhaustive": True, "stageTerminal": "complete",
                     "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []}

CLOSED_WORLD_OPEN = {"exportsClosed": "unknown", "entryPointsRecognized": "none",
                     "nonliteralLoading": "none", "externalConsumers": "unknown",
                     "dynamicDispatch": "not-applicable", "reasons": [],
                     "deadCodeRepairEligible": False}


def entry_complete(**over):
    e = {"coverage": "complete", "resolutionCompleteness": dict(NOT_APPLICABLE_RC),
         "closedWorld": dict(CLOSED_WORLD_OPEN), "derivationKinds": [],
         "confidenceMillionths": 1000000, "deficiency": None, "nativeCause": None}
    e.update(over)
    return e


def entry_unavailable(**over):
    e = entry_complete(coverage="unknown",
                       deficiency="language-tier-unsupported",
                       nativeCause="capability-missing")
    e.update(over)
    return e


# ---------------------------------------------------------------------------
# level specifications (synthetic, retained, re-hashed at closure)
# ---------------------------------------------------------------------------
LEVEL_SPECS = {
    "L0-verbatim": b"opensip level specification L0-verbatim v1\n"
                   b"no tokenisation; the canonical payload is the raw body span\n",
    "L1-lexical": b"opensip level specification L1-lexical v1\n"
                  b"token kinds: kw ident punct str num ws-elided\n"
                  b"transform order: strip insignificant whitespace, normalise line endings\n"
                  b"replacement bytes: none\n",
}


def retain_level_specs(kit):
    out = {}
    for level, data in LEVEL_SPECS.items():
        out[level] = kit.w.raw(data)
    return out


# ---------------------------------------------------------------------------
# body identity minting
# ---------------------------------------------------------------------------
def mint_body_identity(kit, universe_domain, universe, context, retained,
                       anchor_path, span_bytes, level, level_version_hex,
                       tokens=None):
    blv, language_id = G.body_language_version(
        kit.w, universe_domain, universe, context, anchor_path, retained)
    kit.w.record(blv)                                    # derived, retained
    lv_raw = hashlib.sha256(C(blv)).digest()
    if level == "L0-verbatim":
        payload = O.body_payload_L0(span_bytes)
    else:
        payload = O.body_payload_tokens(tokens)
    ident, frame = O.body_identity(level, bytes.fromhex(level_version_hex),
                                   language_id, lv_raw, payload)
    kit.w.raw(frame)
    return ident, blv, language_id


# ---------------------------------------------------------------------------
# policy / proof scaffolding (one non-gating rule, verdict pass)
# ---------------------------------------------------------------------------
def policy_and_program(kit, relation="file", rung="enumerated"):
    rule = {
        "ruleId": "inventory-present",
        "ruleProgramRef": {"contributionId": "opensip.first-party",
                           "ruleStableId": "inventory-present",
                           "semanticsMajor": 1,
                           "programDigest": sha256hex(b"inventory-present.v1")},
        "enabled": True, "severity": "note", "gate": False,
        "subjectEnumeration": {"universe": "primary", "subjectKind": "file"},
        "emitWhen": {"op": "exists", "relation": relation,
                     "minResolution": rung, "filters": []},
        "evidenceUse": [], "messageCode": "inventory.present"}
    policy = {"schemaFamily": "opensip.product.policy", "schemaMajor": 1,
              "gateSeverityAtLeast": "error", "rules": [rule]}
    waivers = {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1,
               "waivers": []}
    pd = kit.w.record(policy)
    wd = kit.w.record(waivers)
    program = {"schemaVersion": 1, "policyDigest": pd,
               "rules": [{"ruleId": rule["ruleId"],
                          "ruleProgramRef": rule["ruleProgramRef"],
                          "emitWhen": rule["emitWhen"]}]}
    rpd = kit.w.record(program)
    return policy, pd, waivers, wd, program, rpd, rule


def build_proof(kit, plan_id, exec_plan_id, evaluator, detector, rule, rpd,
                view_id, fact_id, coverage_id, extra_inputs):
    node = rule["emitWhen"]
    ppd_rec = {"schemaVersion": 2, "ruleProgramDigest": rpd,
               "ruleId": rule["ruleId"], "predicateId": "p",
               "operation": node["op"], "nodeDigest": raw_digest(node)}
    ppd = kit.w.record(ppd_rec)
    witness = {"schemaVersion": 2, "programPredicateDigest": ppd,
               "matchingFactIds": [fact_id], "coverageIds": [coverage_id],
               "countLimit": None, "childPredicateIds": []}
    wd = kit.w.record(witness)

    tokens = ["ts", "declaration", "function", "inventoryProbe", "()", "void"]
    discriminator = sha256hex(C(tokens))
    fp = {"schemaVersion": 2, "ruleStableId": rule["ruleProgramRef"]["ruleStableId"],
          "detectorSemanticsMajor": 1,
          "subjectKey": {"language": "typescript", "kind": "file",
                         "logicalPath": "src/a.ts", "qualifiedName": "src/a.ts",
                         "discriminator": discriminator},
          "relatedSubjectKeys": []}
    fpid, _ = kit.w.mint("finding-fingerprint", fp)
    params = {"schemaVersion": 2, "messageCode": "inventory.present",
              "parameters": {"path": "src/a.ts"}}
    pdg = kit.w.record(params)
    finding = {"schemaVersion": 2, "fingerprint": fpid, "ruleClosure": detector,
               "subjectId": "file:src/a.ts", "messageCode": "inventory.present",
               "parameterDigest": pdg, "severity": "note",
               "evidenceRefs": [{"domain": "fact",
                                 "digest": fact_id.split(":", 1)[1]},
                                {"domain": "coverage",
                                 "digest": coverage_id.split(":", 1)[1]}]}
    find_id, _ = kit.w.mint("finding", finding)

    inputs = [{"domain": "view", "digest": view_id.split(":", 1)[1]},
              {"domain": "coverage", "digest": coverage_id.split(":", 1)[1]},
              {"domain": "rule-program", "digest": rpd}] + extra_inputs
    inputs = sorted({C(i): i for i in inputs}.values(), key=lambda i: C(i))
    proof = {"schemaVersion": 2, "planId": plan_id,
             "executionPlanId": exec_plan_id, "evaluatorClosure": evaluator,
             "ruleProgramDigest": rpd,
             "evaluationInputRefs": inputs,
             "predicateProofs": [{"ruleId": rule["ruleId"],
                                  "subjectId": "file:src/a.ts",
                                  "predicateId": "p", "operation": node["op"],
                                  "inputRefs": inputs,
                                  "scopeIds": [],
                                  "value": "true", "witnessDigest": wd}],
             "findingIds": [find_id], "verdict": "pass"}
    pid, _ = kit.w.mint("proof-bundle", proof)
    return pid, [find_id]


def build_exec_plan(kit, plan_id, producer):
    spec = {"schemaVersion": 2, "planId": plan_id, "producerClosure": producer,
            "operation": "native.analyze", "parameters": [],
            "outputDomains": ["coverage", "fact"],
            "outputSchemaDigest": G.NATIVE_DOC_DIGEST}
    sd = kit.w.record(spec)
    ep = {"schemaVersion": 2, "planId": plan_id,
          "stages": [{"ordinal": 0, "stageSpecDigest": sd, "requires": [],
                      "outputDomains": ["coverage", "fact"]}]}
    epid, _ = kit.w.mint("execution-plan", ep)
    return epid


def seal_and_run(kit, plan_id, exec_plan_id, evidence_id, evaluator, policy_digest,
                 proof_id, snapshot_id, cap_id, verdict="pass"):
    seal = {"schemaVersion": 2, "planId": plan_id,
            "executionPlanId": exec_plan_id, "evidenceId": evidence_id,
            "evaluatorClosure": evaluator, "policyDigest": policy_digest,
            "proofBundleId": proof_id, "verdict": verdict}
    sid, _ = kit.w.mint("evaluation-seal", seal)
    run = {"schemaVersion": 2, "projectId": kit.w.projectId,
           "snapshotId": snapshot_id, "planId": plan_id,
           "evidenceId": evidence_id, "evaluationSealId": sid,
           "capabilityManifestId": cap_id}
    rid, _ = kit.w.mint("run", run)
    return sid, rid


def evidence(kit, plan_id, view_ids, coverage_ids, import_ids, finding_ids,
             proof_id):
    ev = {"schemaVersion": 2, "planId": plan_id,
          "viewIds": sorted(set(view_ids), key=lambda s: C(s)),
          "coverageIds": sorted(set(coverage_ids), key=lambda s: C(s)),
          "importIds": sorted(set(import_ids), key=lambda s: C(s)),
          "findingIds": sorted(set(finding_ids), key=lambda s: C(s)),
          "proofBundleId": proof_id}
    eid, _ = kit.w.mint("semantic-evidence", ev)
    return eid


# ---------------------------------------------------------------------------
# capability manifest for a Run
# ---------------------------------------------------------------------------
def capability_manifest(kit, providers, absent=()):
    m = {"schemaVersion": 1, "profile": "default",
         "providers": sorted(providers, key=lambda p: p["providerId"].encode()),
         "coverageForAbsent": sorted(absent,
                                     key=lambda a: a["providerId"].encode())}
    v = O.admit_capability_manifest(m)
    if v:
        raise AssertionError("capability manifest not admissible: %r" % v)
    b = O.cve1(m)
    kit.w.raw(b)
    return m, b, sha256hex(b), O.capability_manifest_id(b)


def plan(kit, snapshot_id, cap_bytes_digest, cap_id, closures, spec_digest,
         config_digest, context_hexes, import_ids, policy_digest, waiver_digest,
         scope_digest, budget, grant_digest):
    p = {"schemaVersion": 2, "snapshotId": snapshot_id,
         "capabilityManifestId": cap_id,
         "semanticClosures": sorted(set(closures), key=lambda s: C(s)),
         "analysisSpecDigest": spec_digest,
         "resolvedConfigDigest": config_digest,
         "nativeContextDigests": sorted(set(context_hexes), key=lambda s: C(s)),
         "importIds": sorted(set(import_ids), key=lambda s: C(s)),
         "policyDigest": policy_digest, "waiverDigest": waiver_digest,
         "scopeDigest": scope_digest, "budget": budget,
         "semanticGrantDigest": grant_digest,
         "capabilityManifestBytesDigest": cap_bytes_digest}
    pid, _ = kit.w.mint("plan", p)
    return pid, p
