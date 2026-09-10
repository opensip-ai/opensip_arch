"""Construction helpers for complete minimal positive Run descriptor graphs.

Everything here is MY OWN synthetic trusted observation.  A synthetic TCB
observation is an assumption, never native enforcement proof.
"""
from __future__ import annotations

import hashlib
import json

import capman
import closure as CL
import osip
import schemas
from closure import Store, suffix
from osip import C, H, ident, raw_sha256, record_digest

RELATION_DOC_DIGEST = CL.RELATION_DOC_DIGEST
NATIVE_DOC_DIGEST = CL.NATIVE_DOC_DIGEST
POLICY_DOC_DIGEST = CL.POLICY_DOC_DIGEST


class Fixture:
    def __init__(self, project_seed: str):
        self.s = Store()
        self.project_id = "prj1-" + hashlib.sha256(project_seed.encode()).hexdigest()
        self.files = {}          # snapshot source inventory: path -> bytes
        self.closures = {}       # label -> closure2:<hex>
        self.objects = []        # machine-readable object table
        # identity section 3: the complete closure includes the bytes of every
        # REGISTERED SCHEMA DOCUMENT referenced anywhere in the graph.
        for rel in (CL.RELATION_DOC, CL.NATIVE_DOC, CL.POLICY_DOC):
            self.s.put_raw(osip.doc_bytes(rel), "schema-document:" + rel)

    # -- object table ------------------------------------------------------
    def note(self, typed_identity, domain, descriptor, label):
        self.objects.append({"identity": typed_identity, "domain": domain,
                             "label": label, "descriptor": descriptor})

    # -- raw repository ----------------------------------------------------
    def add_file(self, path, data: bytes):
        self.files[path] = data
        self.s.put_raw(data, "source:" + path)
        return path

    def inventory(self):
        rows = [{"path": p, "sha256": raw_sha256(b), "bytes": len(b)}
                for p, b in self.files.items()]
        rows.sort(key=lambda r: r["path"].encode("utf-8"))
        return rows

    # -- closures ----------------------------------------------------------
    def closure(self, label, kind, members, semantic_version, platform,
                protocol_major=3):
        """members: dict relpath -> bytes"""
        tree = []
        for p in sorted(members, key=lambda x: x.encode("utf-8")):
            b = members[p]
            self.s.put_raw(b, "closure-member:%s:%s" % (label, p))
            tree.append({"path": p, "sha256": raw_sha256(b), "bytes": len(b)})
        manifest_body = C({"component": label, "semanticVersion": semantic_version,
                           "platform": platform})
        self.s.put_raw(manifest_body, "closure-manifest:" + label)
        desc = {"schemaVersion": 2, "kind": kind,
                "manifestDigest": raw_sha256(manifest_body), "tree": tree,
                "semanticVersion": semantic_version, "protocolMajor": protocol_major,
                "platform": platform}
        errs = schemas.validate(desc, "identity", "#/$defs/closure")
        assert not errs, errs
        h = self.s.put_h("closure", desc, "closure:" + label)
        cid = "closure2:" + h
        self.closures[label] = cid
        self.note(cid, "closure", desc, label)
        return cid, desc, {r["path"]: r["sha256"] for r in tree}

    # -- generic retention -------------------------------------------------
    def rec(self, record, doc, selector, label):
        errs = schemas.validate(record, doc, selector)
        assert not errs, (label, errs)
        d = self.s.put_record(record, label)
        return d

    def hid(self, domain, descriptor, doc, selector, label):
        errs = schemas.validate(descriptor, doc, selector)
        assert not errs, (label, errs)
        h = self.s.put_h(domain, descriptor, label)
        self.note(osip.PREFIXES.get(domain, domain) + ":" + h, domain, descriptor, label)
        return h


# ---------------------------------------------------------------------------
def default_semantic_config(capabilities, budget_limit=100000):
    return {
        "analysis": {"profileId": "default",
                     "capabilities": sorted(set(capabilities)),
                     "budget": {"unit": "work-units", "limit": budget_limit}},
        "components": {}, "discovery": {}, "policy": {}, "evidence": {},
    }


def scope_descriptor(roots, prefixes, excluded):
    return {"schemaVersion": 2,
            "workspaceRoots": sorted(set(roots), key=lambda x: C(x)),
            "pathPrefixes": sorted(set(prefixes), key=lambda x: C(x)),
            "excludedPathPrefixes": sorted(set(excluded), key=lambda x: C(x))}


def analysis_spec(rows, parameters=None):
    rows = sorted(rows, key=lambda r: C(r))
    return {"schemaVersion": 2, "requestedCapabilities": rows,
            "policyPackIds": [], "parameters": sorted(parameters or [], key=lambda r: C(r))}


def semantic_grant(project_id, closure_ids, operations, scope_digest):
    principals = [{"kind": "first-party", "closureId": c, "ownerSourceDigest": None}
                  for c in closure_ids]
    principals.sort(key=lambda p: C(p))
    return {"schemaVersion": 2, "projectId": project_id, "principals": principals,
            "analysisOperations": sorted(set(operations), key=lambda x: C(x)),
            "scopeDigest": scope_digest}


MINIMAL_POLICY = {
    "schemaFamily": "opensip.product.policy",
    "schemaMajor": 1,
    "gateSeverityAtLeast": "error",
    "rules": [{
        "ruleId": "no-unresolved-edges",
        "ruleProgramRef": {"contributionId": "opensip.first-party.detectors",
                           "ruleStableId": "no-unresolved-edges",
                           "semanticsMajor": 1,
                           "programDigest": "0" * 64},
        "enabled": True, "severity": "error", "gate": True,
        "subjectEnumeration": {"universe": "repository", "subjectKind": "file"},
        "emitWhen": {"op": "exists", "relation": "unresolved-edge",
                     "minResolution": "observed", "filters": []},
        "evidenceUse": [],
    }],
}

EMPTY_WAIVERS = {"schemaFamily": "opensip.product.waivers", "schemaMajor": 1,
                 "waivers": []}


def rule_program(policy, policy_digest):
    return {"schemaVersion": 1, "policyDigest": policy_digest,
            "rules": [{"ruleId": r["ruleId"], "ruleProgramRef": r["ruleProgramRef"],
                       "emitWhen": r["emitWhen"]} for r in policy["rules"]]}


# ---------------------------------------------------------------------------
def coverage_entry(relation, rung, commitment, subject_count, coverage,
                   deficiency=None, cause=None, closed_world=None,
                   derivation_kinds=None, confidence=1000000,
                   rc=None, stage_terminal="complete", examined_exhaustive=True):
    """A ViewEntryV3 built to RC-0/RC-1/RC-2 by construction."""
    if rc is None:
        if rung in CL.RESOLVED_RUNGS:
            rc = {"state": "complete", "attempted": True,
                  "examinedExhaustive": examined_exhaustive,
                  "stageTerminal": stage_terminal,
                  "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []}
        else:
            rc = {"state": "not-applicable", "attempted": False,
                  "examinedExhaustive": examined_exhaustive,
                  "stageTerminal": stage_terminal,
                  "unresolvedEdgeCount": 0, "unresolvedEdgeClasses": []}
    cw = closed_world or {"exportsClosed": "unknown", "entryPointsRecognized": "none",
                          "nonliteralLoading": "none", "externalConsumers": "unknown",
                          "dynamicDispatch": "not-applicable", "reasons": [],
                          "deadCodeRepairEligible": False}
    return {"relation": relation, "resolution": rung, "coverage": coverage,
            "examinedUniverse": {"subjectScopeCommitment": commitment,
                                 "subjectCount": subject_count},
            "resolutionCompleteness": rc, "closedWorld": cw,
            "derivationKinds": sorted(derivation_kinds or []),
            "confidenceMillionths": confidence,
            "deficiency": deficiency, "nativeCause": cause}
