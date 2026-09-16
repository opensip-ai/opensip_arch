"""Phase 8: authorization records, purge/replay/output failures, public termination goldens, host-captured vs candidate,
four evidence states and the detector compatibility listing.

Writes vectors/test-prep-repair-authorization.json, envelopes/purge-replay-output-failure.json, envelopes/public-termination.json,
vectors/host-captured-vs-candidate.json, vectors/empty-partial-unavailable-missing.json, vectors/detector-compat-file.json.
These are authorization RECORDS and admission joins reconstructed from the contracts; no repository code is executed, no
security signature/truth-table measurement or lease is performed (future qualification).
Usage: python3 tools/runref.py tools/phase8_envelopes.py
"""
import copy
import hashlib
import json
import sys

OUT = "/private/tmp/opensip-design-corrections/consumer-b.v24-source41.v1/output"
sys.path.insert(0, OUT + "/ref")
sys.path.insert(0, OUT + "/tools")
sys.path.insert(0, OUT + "/builders")

import canonical as K  # noqa: E402
import closure as CL  # noqa: E402
import detector_compat as DC  # noqa: E402
import enumeration as EN  # noqa: E402
import execinputs as XI  # noqa: E402
import schemas  # noqa: E402
from store import Store  # noqa: E402
import phase7_vectors as P7  # noqa: E402
from syntax_runs import closure as mk_closure  # noqa: E402
from ts_runs import DEFAULT_PACK  # noqa: E402

KIT = schemas.kit()
SEC = "security/security-lifecycle.schemas.v1.json"
TEST = "workflows/schemas/test-execution.schema.json"
NE = P7.NE
INVOC3, COMMON3, ID = P7.INVOC3, P7.COMMON3, P7.ID
EXEC_DOC = "foundation/execution-inputs.schema.v1.json"
DDC = set(KIT.doc(COMMON3)["$defs"]["DomainDetailCode"]["enum"])
# security-and-lifecycle.md lines 1079-1083: the platform truth-table row, identical on all four platforms
TRUTH_ROW = {"subprocess": "DISCLOSURE-ONLY", "filesystemWrite": "DISCLOSURE-ONLY", "network": "DISCLOSURE-ONLY", "environment": "ENFORCED-BY-CONSTRUCTION"}
# workflows-and-surfaces.md lines 1436-1441
CONSENT_MAP = {"interactive-explicit": ("interactive-consent", "interactive"), "policy-record": ("pre-existing-policy", "policy")}
POLICY_RECORD = hashlib.sha256(b"cb24 synthetic admitted policy record").hexdigest()
failures = []


def must(name, cond, detail=None):
    if not cond:
        failures.append({"vector": name, "detail": detail})
    return bool(cond)


def dump(rel, obj):
    with open(f"{OUT}/{rel}", "w") as fh:
        json.dump(obj, fh, indent=1, sort_keys=True)


def loaded(name):
    exported = json.load(open(f"{OUT}/runs/{name}.store.json"))
    store = Store.load(exported)
    C = CL.Closure(store)
    g = CL.admit_graph(C, exported["runId"])
    must(f"{name}-admits", not C.faults, C.faults[:2])
    g.update(runId=exported["runId"], store=store, exported=exported)
    return g


def closures_by_name(g):
    out = {}
    for row in g["exported"]["objectTable"]:
        if row["domain"] == "closure":
            label = g["exported"]["blobLabels"].get(row["frameSha256"], "")
            out[label.split(":", 1)[-1]] = (row["id"], g["store"].get_object(row["id"]))
    return out


def label_digest(g, label):
    return next(h for h, v in g["exported"]["blobLabels"].items() if v == label)


# ------------------------------------------------------------------ authorization records
def grant_ref(grant):
    return "security.repo-execution-grant.v2:" + K.H("security.repo-execution-grant.v2", grant)


def admit_test_step(params, grant, ctx):
    ok, errs = P7.admit(params, TEST, "#/$defs/TestExecutionStepParams")
    if not ok:
        return f"SCHEMA:TestExecutionStepParams:{(errs or [''])[:2]}"
    gok, gerrs = P7.admit(grant, SEC, "#/schemas/RepoExecutionGrantV2")
    if not gok:
        return f"SECURITY_SCHEMA:RepoExecutionGrantV2:{(gerrs or [''])[:2]}"
    mode = grant["authorization"]["mode"]
    if grant["authorization"]["ci"] != ctx["ci"]:
        return "TEST.PRINCIPAL_NOT_ADMITTED:ci-flag"
    if ctx["ci"] and (mode == "interactive-explicit" or params["consentSource"] == "interactive-consent"):
        return "TEST.INTERACTIVE_CONSENT_IN_CI"
    if CONSENT_MAP[mode][0] != params["consentSource"]:
        return "cb24.TEST_CONSENT_SOURCE_RELABELLED"
    if params["authorizationRef"] != grant_ref(grant):
        return "TEST.PRINCIPAL_NOT_ADMITTED:authorization-ref"
    for f, v in (("projectId", ctx["projectId"]), ("snapshotId", ctx["snapshotId"]), ("argvDigest", K.raw_digest(params["argv"])),
                 ("executionClass", params["executionClass"]), ("platformId", params["platformId"])):
        if grant[f] != v:
            return f"TEST.PRINCIPAL_NOT_ADMITTED:{f}"
    if grant["owners"] != [] or grant["ownerSourceDigest"] != K.raw_digest([]):
        return "TEST.PRINCIPAL_NOT_ADMITTED:owners"
    src = params["argv0Source"]
    if src["kind"] == "toolchain-closure":
        desc = ctx["closures"].get(src["closureId"])
        members = {r["path"] for r in desc["tree"]} if desc else set()
        if src["closureId"] != grant["toolClosureId"] or src["member"] not in members or params["argv"][0] != src["member"] or \
                grant["runner"] != {"kind": "toolchain-closure", "member": src["member"]}:
            return "TEST.ARGV_NOT_IN_CLOSURE"
    elif src["path"] not in ctx["snapshotPaths"] or params["argv"][0] != src["path"] or grant["runner"] != {"kind": "snapshot-member", "member": src["path"]}:
        return "TEST.ARGV_NOT_IN_CLOSURE"
    if "PATH" in params["environmentAllowlist"]:
        return "TEST.ENV_NOT_ALLOWLISTED"
    if params["effects"] != TRUTH_ROW:
        return "TEST.CONFINEMENT_CLAIM_REFUSED"
    if grant["effects"] != TRUTH_ROW:
        return "TEST.CONFINEMENT_CLAIM_REFUSED:grant"
    return None


def repair_ref(auth):
    return "security.repair-apply-authorization.v1:" + K.H("security.repair-apply-authorization.v1", auth)


def admit_repair(params, auth, plan_desc, repair_plan_id, ci):
    ok, errs = P7.admit(params, INVOC3, "#/$defs/RepairApplyParams")
    if not ok:
        return f"SCHEMA:RepairApplyParams:{(errs or [''])[:2]}"
    aok, aerrs = P7.admit(auth, SEC, "#/schemas/RepairApplyAuthorizationV1")
    if not aok:
        return f"SECURITY_SCHEMA:RepairApplyAuthorizationV1:{(aerrs or [''])[:2]}"
    if "repairplan2:" + K.H("workflow.repair-plan", plan_desc) != repair_plan_id:
        return "cb24.REPAIR_PLAN_ID_NOT_RECOMPUTED"
    mode = auth["consent"]["mode"]
    if auth["consent"]["ci"] != ci:
        return "REPAIR.CONSENT_NOT_BOUND:ci-flag"
    if ci and mode == "interactive-explicit":
        return "REPAIR.CONSENT_NOT_BOUND:interactive-in-ci"
    if CONSENT_MAP[mode][1] != params["consentSource"]:
        return "cb24.REPAIR_CONSENT_SOURCE_RELABELLED"
    if params["authorizationRef"] != repair_ref(auth):
        return "REPAIR.CONSENT_NOT_BOUND:authorization-ref"
    # security S10.1: projectId, repairPlanId and baseSnapshotId equal the invocation's; recipeClosureId equals the rehashed plan's recipe.
    # The retained plan descriptor carries its base snapshot as snapshotId.
    for key, a, b in (("cb24.AUTHZ_REPAIR_PLAN_ID_MISMATCH", auth["repairPlanId"], params["repairPlanId"]),
                      ("cb24.AUTHZ_REPAIR_PLAN_ID_MISMATCH", auth["repairPlanId"], repair_plan_id),
                      ("cb24.AUTHZ_PROJECT_ID_MISMATCH", auth["projectId"], plan_desc["projectId"]),
                      ("cb24.AUTHZ_BASE_SNAPSHOT_ID_MISMATCH", auth["baseSnapshotId"], plan_desc["snapshotId"]),
                      ("AUTHZ.RECIPE_CLOSURE_MISMATCH", auth["recipeClosureId"], plan_desc["recipe"]["closureId"])):
        if a != b:
            return f"REPAIR.CONSENT_NOT_BOUND:{key}"
    return None


def grant_set_ref(refs):
    return "security.repo-execution-grants.v2:" + K.H("security.repo-execution-grants.v2", {"schemaVersion": 2, "grantRefs": sorted(set(refs), key=str.encode)})


def admit_preparation(params, ae, grants):
    ok, errs = P7.admit(params, INVOC3, "#/$defs/NativePreparationParams")
    if not ok:
        return f"SCHEMA:NativePreparationParams:{(errs or [''])[:2]}"
    aok, aerrs = P7.admit(ae, NE, "#/$defs/AuthorizedExecutionV2")
    if not aok:
        return f"SCHEMA:AuthorizedExecutionV2:{(aerrs or [''])[:2]}"
    for gr in grants:
        gok, gerrs = P7.admit(gr, SEC, "#/schemas/RepoExecutionGrantV2")
        if not gok:
            return f"SECURITY_SCHEMA:RepoExecutionGrantV2:{(gerrs or [''])[:2]}"
    if params["authorizationDescriptorDigest"] != K.raw_digest(ae):
        return "cb24.PREPARATION_DESCRIPTOR_DIGEST"
    if not (params["securityGrantSetRef"] == ae["authorizationRef"] == grant_set_ref([grant_ref(gr) for gr in grants])):
        return "cb24.PREPARATION_GRANT_SET_REF"
    by_owner = {}
    for gr in grants:
        if gr["executionClass"] == "test-runner":
            return "cb24.PREPARATION_TEST_RUNNER_GRANT"
        for o in gr["owners"]:
            by_owner.setdefault(o["ownerKey"], []).append(gr)
    for o in ae["owners"]:
        row = {"ownerKey": o["ownerKey"], "source": o["source"], "ownerFileManifestSha256": o["ownerFileManifestSha256"]}
        gs = by_owner.get(o["ownerKey"], [])
        if len(gs) != 1 or gs[0]["owners"] != [row] or gs[0]["executionClass"] != o["kind"] or gs[0]["ownerSourceDigest"] != K.raw_digest([row]):
            return f"cb24.PREPARATION_OWNER_GRANT:{o['ownerKey']}"
        gr = gs[0]
        if gr["effects"] != TRUTH_ROW or {k: v["enforcement"] for k, v in ae["effects"].items()} != TRUTH_ROW:
            return "cb24.PREPARATION_EFFECTS_NOT_TRUTH_TABLE"
        if gr["authorization"]["mode"] != ae["authorization"]["mode"] or gr["authorization"]["ci"] != ae["authorization"]["ci"]:
            return "cb24.PREPARATION_CONSENT_JOIN"
        if gr["toolClosureId"] != ae["toolClosure"]["closureId"] or gr["projectId"] != ae["projectId"] or gr["snapshotId"] != ae["snapshotId"] or \
                gr["dependencySourceSetId"] != ae["dependencySourceSetId"].split(":", 1)[1]:
            return "cb24.PREPARATION_GRANT_BINDING"
    return None


def authorization():
    g = loaded("ts-pass")
    cl = closures_by_name(g)
    T_id, T_desc = cl["cb24-typescript"]
    ctx = {"ci": True, "projectId": g["snapshot"]["projectId"], "snapshotId": g["plan"]["snapshotId"], "closures": {T_id: T_desc},
           "snapshotPaths": {r["path"] for r in g["snapshot"]["sourceInventory"]}}
    argv = ["bin/node", "--test", "src/util.ts"]

    def base_grant():
        return {"grantSchema": 2, "principalClass": "repository-code", "semanticPrincipalKind": "trusted-repository-code", "projectId": ctx["projectId"],
                "snapshotId": ctx["snapshotId"], "argvDigest": K.raw_digest(argv), "executionClass": "test-runner", "owners": [],
                "ownerSourceDigest": K.raw_digest([]), "runner": {"kind": "toolchain-closure", "member": "bin/node"}, "dependencySourceSetId": None,
                "toolClosureId": T_id, "platformId": "macos-aarch64", "effects": dict(TRUTH_ROW),
                "authorization": {"mode": "policy-record", "policyRecordId": POLICY_RECORD, "ci": True}, "expiry": "operation-end", "inherited": False}

    def base_params(grant):
        return {"kind": "test-execution", "argv": list(argv), "argv0Source": {"kind": "toolchain-closure", "closureId": T_id, "member": "bin/node"},
                "cwdIsRoot": True, "principal": "P-TRUSTED-REPO", "executionClass": "test-runner", "platformId": "macos-aarch64",
                "authorizationRef": grant_ref(grant), "consentSource": "pre-existing-policy", "afterStep": 0, "timeoutMilliseconds": 600000,
                "maxOutputBytes": 1048576, "environmentAllowlist": ["CI"], "effects": dict(TRUTH_ROW)}
    grant = base_grant()
    params = base_params(grant)
    first = admit_test_step(params, grant, ctx)
    must("test-step-admits", first is None, first)
    empty_owner_digest = K.raw_digest([])
    must("empty-owner-digest-matches-security-text", empty_owner_digest.startswith("4f53cda1") and empty_owner_digest.endswith("2b945"), empty_owner_digest)
    test_negatives = []

    def neg(label, mutate, expect, c=None):
        gr, pa = base_grant(), None
        cc = dict(ctx, **(c or {}))
        pa = mutate(gr)
        fl = admit_test_step(pa, gr, cc)
        ok = fl is not None and fl.startswith(expect)
        must(f"test-negative:{label}", ok, fl)
        test_negatives.append({"vector": label, "classification": "invalid", "firstRefusal": fl, "expected": expect, "pass": ok,
                               "keySpelledInKit": fl.split(":")[0] in DDC if fl else None})

    def m_ci_interactive(gr):
        gr["authorization"] = {"mode": "interactive-explicit", "policyRecordId": None, "ci": True}
        return dict(base_params(gr), consentSource="interactive-consent")

    def m_relabel(gr):
        gr["authorization"] = {"mode": "interactive-explicit", "policyRecordId": None, "ci": False}
        return base_params(gr)

    def m_argv0(gr):
        gr["argvDigest"] = K.raw_digest(["bin/sh", "-c", "npm test"])
        gr["runner"] = {"kind": "toolchain-closure", "member": "bin/sh"}
        return dict(base_params(gr), argv=["bin/sh", "-c", "npm test"], argv0Source={"kind": "toolchain-closure", "closureId": T_id, "member": "bin/sh"})

    def m_path(gr):
        return dict(base_params(gr), environmentAllowlist=["CI", "PATH"])

    def m_confine(gr):
        return dict(base_params(gr), effects=dict(TRUTH_ROW, network="ENFORCED-BY-CONSTRUCTION"))

    def m_platform_primitive(gr):
        return dict(base_params(gr), effects=dict(TRUTH_ROW, network="ENFORCED-PLATFORM:seatbelt"))

    def m_snapshot(gr):
        gr["snapshotId"] = "snapshot2:" + "0" * 64
        return base_params(gr)

    def m_stale_ref(gr):
        pa = base_params(gr)
        gr["platformId"] = "linux-x86_64-gnu"
        return pa

    neg("ci-interactive-consent", m_ci_interactive, "TEST.INTERACTIVE_CONSENT_IN_CI")
    neg("consent-source-relabelled", m_relabel, "cb24.TEST_CONSENT_SOURCE_RELABELLED", {"ci": False})
    neg("argv0-not-in-tool-closure", m_argv0, "TEST.ARGV_NOT_IN_CLOSURE")
    neg("path-copied-from-environment", m_path, "TEST.ENV_NOT_ALLOWLISTED")
    neg("stronger-network-confinement-claim", m_confine, "TEST.CONFINEMENT_CLAIM_REFUSED")
    neg("platform-primitive-claim-not-in-workflow-enum", m_platform_primitive, "SCHEMA:TestExecutionStepParams")
    neg("grant-bound-to-other-snapshot", m_snapshot, "TEST.PRINCIPAL_NOT_ADMITTED:snapshotId")
    neg("grant-changed-after-reference", m_stale_ref, "TEST.PRINCIPAL_NOT_ADMITTED:authorization-ref")
    goldens = {x["id"]: x for x in KIT.doc("workflows/command-inventory.v3.json")["goldens"]}
    test_envelopes = []
    for gid in ("test-run-ci-interactive", "test-run-confinement-claim"):
        gd = goldens[gid]
        det = {"code": gd["domainDetail"], "remedy": gd["remedy"]}
        env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 3, "kind": "failure", "requestId": P7.req_id(1000 + len(test_envelopes)),
               "projectId": ctx["projectId"], "termination": {"class": gd["class"], "errorCode": gd["errorCode"], "domainDetail": det},
               "exitCode": gd["exitCode"], "errors": [det]}
        f = P7.check_envelope(env)
        must(f"test-envelope:{gid}", not f, f)
        test_envelopes.append({"golden": gid, "envelope": env, "faults": f})

    # repair apply
    rd = json.load(open(OUT + "/vectors/repair-descriptor.json"))
    plan = rd["plan"]
    pdesc, rpid = plan["descriptor"], plan["repairPlanId"]
    must("repair-descriptor-has-snapshot", "snapshotId" in pdesc, sorted(pdesc))

    def base_auth():
        return {"authorizationSchema": 1, "kind": "repair-apply", "projectId": pdesc["projectId"], "repairPlanId": rpid, "baseSnapshotId": pdesc["snapshotId"],
                "recipeClosureId": pdesc["recipe"]["closureId"], "consent": {"mode": "policy-record", "policyRecordId": POLICY_RECORD, "ci": True},
                "expiry": "operation-end", "leaseMode": "EXCLUSIVE", "repositoryExecution": False}
    auth = base_auth()
    rparams = {"kind": "repair-apply", "planStep": 0, "repairPlanId": rpid, "consentSource": "policy", "authorizationRef": repair_ref(auth)}
    rfirst = admit_repair(rparams, auth, pdesc, rpid, True)
    must("repair-authorization-admits", rfirst is None, rfirst)
    repair_negatives = []
    other = next(c for c in rd["authorityControls"] if c.get("repairPlanId") and c["repairPlanId"] != rpid)
    for label, mut, expect in (
            ("authorization-for-other-plan", lambda a, p: (a.update(repairPlanId=other["repairPlanId"]), p.update(authorizationRef=repair_ref(a))), "REPAIR.CONSENT_NOT_BOUND:cb24.AUTHZ_REPAIR_PLAN_ID_MISMATCH"),
            ("interactive-consent-in-ci", lambda a, p: (a.update(consent={"mode": "interactive-explicit", "policyRecordId": None, "ci": True}),
                                                       p.update(consentSource="interactive", authorizationRef=repair_ref(a))), "REPAIR.CONSENT_NOT_BOUND:interactive-in-ci"),
            ("policy-consent-relabelled-interactive", lambda a, p: p.update(consentSource="interactive"), "cb24.REPAIR_CONSENT_SOURCE_RELABELLED"),
            ("authorization-grants-repository-execution", lambda a, p: (a.update(repositoryExecution=True), p.update(authorizationRef=repair_ref(a))), "SECURITY_SCHEMA"),
            ("base-snapshot-moved", lambda a, p: (a.update(baseSnapshotId="snapshot2:" + "1" * 64), p.update(authorizationRef=repair_ref(a))), "REPAIR.CONSENT_NOT_BOUND:cb24.AUTHZ_BASE_SNAPSHOT_ID_MISMATCH")):
        a, p = base_auth(), dict(rparams)
        mut(a, p)
        fl = admit_repair(p, a, pdesc, rpid, True)
        ok = fl is not None and fl.startswith(expect)
        must(f"repair-negative:{label}", ok, fl)
        repair_negatives.append({"vector": label, "classification": "invalid", "firstRefusal": fl, "expected": expect, "pass": ok})
    apply_key = K.raw_digest({"operation": "repair-apply", "projectId": pdesc["projectId"], "repairPlanId": rpid, "baseSnapshotId": pdesc["snapshotId"]})

    # native preparation
    gr_run = loaded("rust-mixed")
    ctx_hex = label_digest(gr_run, "native-context:rust")
    nctx = gr_run["store"].get_frame(ctx_hex, {"native.context.rust.v2"})[1]
    owner_manifest = K.raw_digest(["crates/a/build.rs", "crates/a/Cargo.toml"])
    row = {"ownerKey": "lib_a build-script", "source": "snapshot-member", "ownerFileManifestSha256": owner_manifest}
    prep_argv = ["bin/cargo", "build-script-run", "lib_a"]

    def prep_grant(r=row, cls="build-script"):
        return {"grantSchema": 2, "principalClass": "repository-code", "semanticPrincipalKind": "trusted-repository-code",
                "projectId": gr_run["snapshot"]["projectId"], "snapshotId": gr_run["plan"]["snapshotId"], "argvDigest": K.raw_digest(prep_argv),
                "executionClass": cls, "owners": [r] if cls != "test-runner" else [], "ownerSourceDigest": K.raw_digest([r] if cls != "test-runner" else []),
                "runner": {"kind": "toolchain-closure", "member": "bin/cargo"}, "dependencySourceSetId": nctx["dependencySourceSetId"].split(":", 1)[1],
                "toolClosureId": nctx["toolClosure"]["closureId"], "platformId": "macos-aarch64", "effects": dict(TRUTH_ROW),
                "authorization": {"mode": "policy-record", "policyRecordId": POLICY_RECORD, "ci": True}, "expiry": "operation-end", "inherited": False}

    def prep_ae(grants, owners=(row,)):
        return {"schemaVersion": 2, "operation": "native.prepare", "principalClass": "repository-code", "projectId": gr_run["snapshot"]["projectId"],
                "snapshotId": gr_run["plan"]["snapshotId"], "dependencySourceSetId": nctx["dependencySourceSetId"], "toolchain": nctx["toolchain"],
                "toolClosure": nctx["toolClosure"], "cfgSetId": "default",
                "owners": [{"ownerKey": o["ownerKey"], "kind": "build-script", "ownerFileManifestSha256": o["ownerFileManifestSha256"],
                            "provenanceAssurance": "in-snapshot", "source": o["source"]} for o in owners],
                "authorization": {"mode": "policy-record", "policyRecordId": "sha256:" + POLICY_RECORD, "ci": True},
                "authorizationRef": grant_set_ref([grant_ref(x) for x in grants]),
                "bounds": {"maxOwners": 4096, "maxWallMilliseconds": 3600000, "maxOutDirBytes": 4294967296, "maxOutputBytesPerOwner": 268435456},
                "effects": {k: {"requested": f"{k} with the invoking user's authority", "enforcement": v} for k, v in TRUTH_ROW.items()},
                "liveBoundaries": {"revocationCheck": "before-each-owner", "cancellation": "process-group-kill", "trustClockRequired": True},
                "semanticGrantPrincipalKind": "trusted-repository-code", "workflowPrincipalSpelling": "P-TRUSTED-REPO"}
    pg = prep_grant()
    ae = prep_ae([pg])
    pparams = {"kind": "native-preparation", "authorizationDescriptorDigest": K.raw_digest(ae), "securityGrantSetRef": ae["authorizationRef"]}
    pfirst = admit_preparation(pparams, ae, [pg])
    must("preparation-authorization-admits", pfirst is None, pfirst)
    prep_negatives = []
    row2 = {"ownerKey": "lib_b build-script", "source": "snapshot-member", "ownerFileManifestSha256": K.raw_digest(["crates/#b/build.rs"])}
    for label, build, expect in (
            ("descriptor-edited-after-digest", lambda: (lambda a: (a, dict(pparams), [pg], a.update(cfgSetId="other")))(copy.deepcopy(ae))[:3], "cb24.PREPARATION_DESCRIPTOR_DIGEST"),
            ("owner-without-its-own-grant", lambda: (lambda a: (a, {"kind": "native-preparation", "authorizationDescriptorDigest": K.raw_digest(a), "securityGrantSetRef": a["authorizationRef"]}, [pg]))(prep_ae([pg], (row, row2))), "cb24.PREPARATION_OWNER_GRANT:lib_b"),
            ("test-runner-grant-offered", lambda: (lambda t: (lambda a: (a, {"kind": "native-preparation", "authorizationDescriptorDigest": K.raw_digest(a), "securityGrantSetRef": a["authorizationRef"]}, [t]))(prep_ae([t])))(prep_grant(cls="test-runner")), "cb24.PREPARATION_TEST_RUNNER_GRANT"),
            ("grant-set-ref-from-unsorted-list", lambda: (lambda a: (dict(a, authorizationRef="security.repo-execution-grants.v2:" + K.H("security.repo-execution-grants.v2", {"schemaVersion": 2, "grantRefs": sorted([grant_ref(prep_grant(row2)), grant_ref(pg)], key=str.encode, reverse=True)})),
                                                                     None, None))(prep_ae([pg, prep_grant(row2)], (row, row2))), "cb24.PREPARATION_GRANT_SET_REF")):
        a, p, grants = build()
        if p is None:
            grants = [pg, prep_grant(row2)]
            p = {"kind": "native-preparation", "authorizationDescriptorDigest": K.raw_digest(a), "securityGrantSetRef": a["authorizationRef"]}
        fl = admit_preparation(p, a, grants)
        ok = fl is not None and fl.startswith(expect)
        must(f"preparation-negative:{label}", ok, fl)
        prep_negatives.append({"vector": label, "classification": "invalid", "firstRefusal": fl, "expected": expect, "pass": ok})
    scope = {"schemaVersion": 1, "requestId": P7.req_id(1100), "stepId": 0, "projectId": gr_run["snapshot"]["projectId"], "operation": "native-preparation"}
    sok, serrs = P7.admit(scope, INVOC3, "#/$defs/MutationReplayScopeV1")
    must("preparation-receipt-scope-admits", sok, serrs)
    dump("vectors/test-prep-repair-authorization.json", {
        "classification": "valid",
        "testExecution": {"grant": grant, "grantRef": grant_ref(grant), "params": params, "firstRefusal": first, "emptyOwnerDigest": empty_owner_digest,
                          "negatives": test_negatives, "publicEnvelopes": test_envelopes, "consentMap": CONSENT_MAP, "truthTableRow": TRUTH_ROW,
                          "argvDigestRecipe": "cb24: raw SHA-256 of C(argv); security binds 'argv digest' but no recipe was found in the selected kit"},
        "repairApply": {"authorization": auth, "authorizationRef": repair_ref(auth), "params": rparams, "firstRefusal": rfirst, "negatives": repair_negatives,
                        "idempotencyKey": apply_key, "applyPreconditionAfterAuthorization": {"planApplicable": pdesc["applicable"],
                                                                                              "note": "authorization admission does not make a non-applicable plan applicable; apply still refuses its unmet preconditions"}},
        "nativePreparation": {"grant": pg, "grantRef": grant_ref(pg), "grantSetRef": ae["authorizationRef"], "authorizedExecution": ae, "params": pparams,
                              "firstRefusal": pfirst, "negatives": prep_negatives, "receiptIdempotencyKey": K.H("workflow.mutation-intent", scope),
                              "receiptLookupMeaning": "not replay: identifies the step receipt and authorizes nothing (workflows s1 line 160)"},
        "notPerformed": ["security signature/TCB admission of grants", "platform truth-table measurement", "policy-record admission", "spawning any process", "EXCLUSIVE lease"],
        "selectors": ["workflows-and-surfaces.md s7 lines 928-952; lines 1421, 1436-1443", "security-and-lifecycle.md lines 1062-1124",
                      "native-evidence.md lines 3728-3745", "test-execution.schema.json#/$defs/TestExecutionStepParams",
                      "security-lifecycle.schemas.v1.json#/schemas/RepoExecutionGrantV2, #/schemas/RepairApplyAuthorizationV1",
                      "native-evidence.schemas.v2.json#/$defs/AuthorizedExecutionV2", "invocation-record.schema.json#/$defs/RepairApplyParams, NativePreparationParams"]})


# ------------------------------------------------------------------ purge / replay / required output
def envelopes_in(obj):
    if isinstance(obj, dict):
        if obj.get("schemaFamily") == "opensip.product.envelope":
            yield obj
        for v in obj.values():
            yield from envelopes_in(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from envelopes_in(v)


def failure_env(n, term, project_id=None):
    env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 3, "kind": "failure", "requestId": P7.req_id(n), "termination": term,
           "exitCode": P7.EXIT[term["class"]], "errors": [term["domainDetail"]]}
    if project_id:
        env["projectId"] = project_id
    return env


def purge_replay_output():
    g = loaded("ts-pass")
    pid, rid = g["snapshot"]["projectId"], g["runId"]
    goldens = {x["id"]: x for x in KIT.doc("workflows/command-inventory.v3.json")["goldens"]}
    out = {"classification": "valid"}
    pinned = json.load(open(OUT + "/envelopes/pinned-purge.json"))
    pinned_envs = list(envelopes_in(pinned))
    out["pinnedPurgeRefusal"] = {"source": "envelopes/pinned-purge.json", "envelopes": len(pinned_envs),
                                 "faults": [P7.check_envelope(e) for e in pinned_envs],
                                 "classes": [e["termination"]["class"] for e in pinned_envs]}
    must("pinned-purge-envelopes-valid", pinned_envs and all(not f for f in out["pinnedPurgeRefusal"]["faults"]), out["pinnedPurgeRefusal"])
    ra = json.load(open(OUT + "/envelopes/receipt-availability.json"))
    out["purgeCompleted"] = {"source": "envelopes/receipt-availability.json", "mutationReceipt": ra["mutationReceipt"]["receiptId"],
                             "availabilityAfter": ra["availability"][1]}
    exported = g["exported"]
    for label, domain_or_label in (("proof-bundle-purged", "proof-bundle"), ("fact-payload-bytes-lost", "fact-payload:calls")):
        ex = copy.deepcopy(exported)
        if domain_or_label == "proof-bundle":
            victim = next(r["frameSha256"] for r in ex["objectTable"] if r["domain"] == "proof-bundle")
        else:
            victim = next(h for h, v in ex["blobLabels"].items() if v == domain_or_label)
        del ex["blobs"][victim]
        rep = CL.close_run(Store.load(ex), ex["runId"])
        out[label] = {"removedBlob": victim, "closeRun": rep["result"], "firstRefusal": (rep.get("faultsInStageOrder") or [None])[0],
                      "firstRefusalStage": (rep.get("firstRefusal") or {}).get("stage"),
                      "semanticReplayPerformed": rep["semanticReplay"].get("performed")}
        must(f"replay-refuses:{label}", rep["result"] == "REFUSE" and not rep["semanticReplay"].get("performed"), out[label])
    gq = goldens["query-evidence-purged"]
    purged = failure_env(1200, {"class": gq["class"], "errorCode": gq["errorCode"],
                                "domainDetail": {"code": gq["domainDetail"], "remedy": gq["remedy"], "subject": rid}}, pid)
    missing = failure_env(1201, {"class": "operational-failed", "errorCode": "HOST.IO_FAILURE", "faultCause": "host-io",
                                 "domainDetail": {"code": "evidence.missing", "remedy": "restore the retained bytes from custody or re-run the analysis", "subject": rid}}, pid)
    ga = goldens["analyze-renderer-failed-after-commit"]
    after = failure_env(1202, {"class": ga["class"], "errorCode": ga["errorCode"], "faultCause": "delivery-required", "runId": rid,
                               "domainDetail": {"code": ga["domainDetail"], "remedy": ga["remedy"]}}, pid)
    bound = failure_env(1203, {"class": "operational-failed", "errorCode": "OUTPUT.SERIALIZATION_FAILED", "faultCause": "output-serialization",
                               "domainDetail": {"code": "EVALUATION.OUTPUT_BOUND_EXCEEDED", "remedy": "narrow the request; the materialized output exceeds its bound"}}, pid)
    pre_commit_term = {"class": "operational-failed", "errorCode": "DELIVERY.REQUIRED_FAILED", "faultCause": "delivery-required"}
    t_ok, t_errs = P7.admit(pre_commit_term, COMMON3, "#/$defs/StepTermination")
    go = goldens["analyze-optional-export-failed"]
    optional = {"class": go["class"], "runId": rid}
    o_ok, o_errs = P7.admit(optional, COMMON3, "#/$defs/StepTermination")
    rows = {}
    for label, env in (("replay-after-purge", purged), ("retained-bytes-missing", missing), ("required-renderer-after-commit", after), ("output-bound-exceeded", bound)):
        f = P7.check_envelope(env)
        must(f"output-envelope:{label}", not f, f)
        rows[label] = {"envelope": env, "faults": f}
    out["envelopes"] = rows
    out["requiredProjectionFailureBeforeCommit"] = {
        "termination": pre_commit_term, "terminationAdmitted": t_ok, "terminationErrors": t_errs, "runIdInvented": False,
        "failureEnvelopeDetail": None,
        "measured": "A kind=failure envelope requires errors[]; DomainDetailCode has DELIVERY.RENDERER_FAILED_AFTER_COMMIT (after commit) but no member naming a pre-commit required-projection failure, so this termination is carried without inventing a detail (advisory candidate)",
        "deliveryCodes": sorted(c for c in DDC if c.startswith("DELIVERY."))}
    out["optionalExportFailure"] = {"termination": optional, "admitted": o_ok, "errors": o_errs, "golden": go["id"]}
    out["selectors"] = ["workflows-and-surfaces.md s8 lines 995-1010, s9 goldens lines 1155-1156, s12 lines 1348-1384", "workflow-projection-contract.v3 s0 (lost bytes are custody, not correspondence), s6",
                        "command-inventory.v3 goldens query-evidence-purged, analyze-renderer-failed-after-commit, analyze-optional-export-failed"]
    dump("envelopes/purge-replay-output-failure.json", out)


# ------------------------------------------------------------------ public termination goldens
def public_termination():
    inherited = KIT.doc("coop/artifacts/d9-exit-contract.v1.14.json")["codeMaps"]["faultCauseToErrorCode"]
    inverse = {}
    for c, e in list(inherited.items()) + [("host-invariant", "SYSTEM.OUTCOME.ILLEGAL_STATE")]:
        inverse.setdefault(e, []).append(c)
    ts_fail = json.load(open(OUT + "/runs/ts-fail.build.json"))["runId"]
    ts_pass = loaded("ts-pass")
    gfail = loaded("ts-fail")
    rows, no_detail = [], []
    for n, gd in enumerate(KIT.doc("workflows/command-inventory.v3.json")["goldens"]):
        cls = gd["class"]
        t = {"class": cls}
        cause_note = None
        if cls in ("request-rejected", "operational-failed"):
            t["errorCode"] = gd["errorCode"]
        if cls == "operational-failed":
            causes = inverse.get(gd["errorCode"], [])
            if len(causes) == 1:
                t["faultCause"] = causes[0]
            cause_note = causes
        if cls == "indeterminate":
            t["reasonCodes"] = [gd["reasonCode"]]
        if cls == "policy-failed":
            t["runId"] = ts_fail
        if cls == "interrupted":
            t["signal"] = "SIGINT"
        if gd.get("domainDetail") == "DELIVERY.RENDERER_FAILED_AFTER_COMMIT":
            # HC-29: the evaluator3 StepTermination branch for this detail requires the committed Run's runId (the golden remedy reads it
            # from the termination); the original builder omitted it (logs/s39-p89.0.phase8_envelopes.log)
            t["runId"] = ts_pass["runId"]
        if gd.get("domainDetail"):
            t["domainDetail"] = {"code": gd["domainDetail"], "remedy": gd.get("remedy") or gd["situation"][:1024]}
        tok, terrs = P7.admit(t, COMMON3, "#/$defs/StepTermination")
        row = {"golden": gd["id"], "command": gd["command"], "termination": t, "terminationAdmitted": tok, "terminationErrors": terrs,
               "exitMatches": P7.EXIT[cls] == gd["exitCode"], "faultCauseCandidates": cause_note,
               "detailRegistered": gd.get("domainDetail") in DDC if gd.get("domainDetail") else None}
        if cls in ("request-rejected", "operational-failed"):
            if "domainDetail" in t:
                env = failure_env(1300 + n, t)
                row["envelope"], row["envelopeFaults"] = env, P7.check_envelope(env)
            else:
                no_detail.append(gd["id"])
                row["envelope"], row["envelopeFaults"] = None, ["no golden detail: failure errors[] composition not published for this golden"]
        elif cls in ("success", "policy-failed") and gd["command"] in ("default", "analyze"):
            src = gfail if cls == "policy-failed" else ts_pass
            run_res = {"kind": "analysis", "authority": "authoritative", "runId": src["runId"], "planId": src["plan_id"], "verdict": src["proof"]["verdict"],
                       "requiredCoverage": "satisfied", "durability": "committed", "deficiency": "none", "secondaryDeficiencies": []}
            env = {"schemaFamily": "opensip.product.envelope", "schemaMajor": 3, "kind": "run", "requestId": P7.req_id(1300 + n),
                   "projectId": src["snapshot"]["projectId"], "termination": t, "exitCode": P7.EXIT[cls], "run": run_res}
            row["envelope"], row["envelopeFaults"] = env, P7.check_envelope(env)
        ok = tok and row["exitMatches"] and not row.get("envelopeFaults") and row["detailRegistered"] is not False
        if cls == "operational-failed" and "faultCause" not in t:
            ok = False
        row["pass"] = ok
        rows.append(row)
    bad = [r["golden"] for r in rows if not r["pass"] and r["golden"] not in no_detail]
    must("public-termination-goldens", not bad, bad)
    dump("envelopes/public-termination.json", {"classification": "valid", "goldenCount": len(rows), "passed": sum(1 for r in rows if r["pass"]),
                                              "failureGoldensWithoutDetail": no_detail, "faultCauseInverseAmbiguous": {e: c for e, c in inverse.items() if len(c) > 1},
                                              "rows": rows,
                                              "selectors": ["workflows/command-inventory.v3.json#/goldens", "evaluator3 common StepTermination, DomainDetailCode", "coop/artifacts/d9-exit-contract.v1.14.json#/codeMaps"]})


# ------------------------------------------------------------------ host-captured vs candidate
def host_captured_vs_candidate():
    g = loaded("ts-pass")
    vcs_kind = g["store"].get_record(g["snapshot"]["vcsDigest"])["kind"]
    ctx = {"enum_index": g["index"], "views": g["views"], "scopes": g["scopes"], "coverages": g["coverages"], "candidates": {}, "vcs_kind": vcs_kind,
           "receipts": g["xi"]["hostCapture"]["stageReceipts"], "plan_id": g["plan_id"], "plan": g["plan"]}
    cells = g["enum"]["cells"]
    view_id = sorted(g["views"])[0]
    obs = {"viewDigests": [view_id], "stageOrdinal": 0, "candidateResultDigest": None}
    ci_calls = next(i for i, c in enumerate(cells) if c["capabilityId"] == "calls")
    faults = []
    o_calls, accs, rows, _ = XI.derive_outcome(ci_calls, cells[ci_calls], cells[ci_calls]["programBindings"][0], obs, ctx, faults)
    stored = next(o for o in g["xi"]["cellOutcomes"] if o["cellOrdinal"] == ci_calls)
    must("host-captured-recomputes-stored-outcome", {k: v for k, v in stored.items() if k != "ordinal"} == o_calls and not faults, (stored, o_calls, faults))
    b = cells[ci_calls]["programBindings"][0]
    ci = len(cells)
    kinds = EN.KIND_DERIVATION["clones-near"]
    binding = dict(copy.deepcopy(b), extents=[])

    def cell(required):
        return {"capabilityId": "clones-near", "languageMode": "ts-tsconfig", "workspaceRoot": ".", "required": required, "kinds": kinds, "programBindings": [binding]}

    def envelope(state, deficiency=None):
        return {"schemaVersion": 1, "planId": g["plan_id"], "executionPlanId": g["exec_plan_id"], "cellOrdinal": ci, "programOrdinal": 0,
                "capabilityId": "clones-near", "languageMode": "ts-tsconfig", "universe": b["universe"], "producerClosure": b["enumerator"]["closureId"],
                "stageOrdinal": 0, "state": state, "deficiency": deficiency, "nativeCause": None, "authority": "candidate-only",
                "semanticEquivalenceClaimed": False, "automaticDeletionEligible": False, "examinedPaths": ["src/index.ts", "src/util.ts"],
                "groupDigests": [], "sourceBodies": []}
    cases = []
    for label, required, env in (("required-candidate-absent", True, None), ("optional-candidate-absent", False, None),
                                 ("required-candidate-complete", True, envelope("complete")),
                                 ("required-candidate-partial", True, envelope("partial", "provider-unavailable"))):
        cctx = dict(ctx, candidates={})
        o = dict(obs)
        env_ok = None
        if env is not None:
            env_ok, env_errs = P7.admit(env, EXEC_DOC, "#/$defs/CandidateProducerResultV1")
            must(f"candidate-envelope-admits:{label}", env_ok, env_errs)
            d = K.raw_digest(env)
            cctx["candidates"][d] = env
            o["candidateResultDigest"] = d
        fl = []
        oc, a, rr, src = XI.derive_outcome(ci, cell(required), binding, o, cctx, fl)
        cases.append({"case": label, "outcome": oc, "accounts": [x for x, _ in a], "requiredRows": rr, "faults": fl, "envelopeAdmitted": env_ok})
    exp = {"required-candidate-absent": ("unavailable", ["EXECUTION_INPUTS_CANDIDATE_REQUIRED"]), "optional-candidate-absent": ("unavailable", []),
           "required-candidate-complete": ("complete", []), "required-candidate-partial": ("partial", [])}
    for c in cases:
        st, fk = exp[c["case"]]
        must(f"candidate-case:{c['case']}", c["outcome"]["state"] == st and [f.split(":")[0] for f in c["faults"]] == fk and not c["accounts"], c)
    must("candidate-partial-required-row", any(r["source"] == "candidate" and r["inputRefs"] and r["inputRefs"][0]["domain"] == "candidate-producer-result"
                                               for r in cases[3]["requiredRows"]), cases[3]["requiredRows"])
    # source39: under the bodyEligibilityLaw census ts-clones-required's required clones account is complete, so the required-incomplete
    # host-captured example is the Run whose required clones account retains a disclosed unknown partition
    incomplete_run = "syntax-mixed-disclosed"
    gr = loaded(incomplete_run)
    cci = next(i for i, c in enumerate(gr["enum"]["cells"]) if c["capabilityId"] == "clones-fact")
    host_rows = [r for r in gr["derived"]["requiredRows"] if r["cellOrdinal"] == cci]
    must("host-captured-required-rows-from-coverage", host_rows and all(r["source"] == "coverage" and r["inputRefs"][0]["domain"] == "coverage" for r in host_rows), host_rows)
    dump("vectors/host-captured-vs-candidate.json", {
        "classification": "valid",
        "hostCapturedRequiredWork": {"run": "ts-pass", "cellOrdinal": ci_calls, "observation": obs, "recomputedOutcome": o_calls, "storedOutcome": stored,
                                     "accounts": [x for x, _ in accs], "requiredRows": rows,
                                     "requiredIncomplete": {"run": incomplete_run, "cellOrdinal": cci, "requiredRows": host_rows}},
        "candidateOnlyReturns": cases,
        "distinction": "host capture owns stage receipts, returned view digests and Coverage-derived accounts/required rows; a candidate-only return is one CandidateProducerResultV1 per binding, projected with no Coverage account, never a fact or complete-clone claim; its absence is a typed required refusal only when required",
        "selectors": ["execution-inputs.schema.v1.json#/$defs/CandidateProducerResultV1", "execution-inputs contract (candidate carrier order, no manufactured carrier)",
                      "native-capability-matrix.v2.json clones-near relations []"]})
    return cases


# ------------------------------------------------------------------ four states
def four_states(candidate_cases):
    g = loaded("ts-pass")
    empty_rules = [r for r in g["proof"]["ruleResults"] if r["outcome"] == "pass" and r["enumeration"]["state"] == "complete" and not r["findingIds"]
                   and r["enumeration"]["selectedSubjectIds"]]
    # source39: under the bodyEligibilityLaw census ts-pass owes no clones partition for its data files, so its cells are complete; the
    # partial example is syntax-mixed-disclosed, whose clones account keeps a disclosed unknown partition
    partial_run = "syntax-mixed-disclosed"
    gp = loaded(partial_run)
    partial_cells = [o for o in gp["xi"]["cellOutcomes"] if o["state"] == "partial"]
    partial_cov = [p["entry"] for c, (d, p) in sorted(gp["coverages"].items()) if p and p["entry"]["coverage"] != "complete"]
    unavailable = next(c for c in candidate_cases if c["case"] == "optional-candidate-absent")["outcome"]
    trace = json.load(open(OUT + "/traces/unavailable.json"))
    multi = json.load(open(OUT + "/vectors/multi-unit-missing-caps.json"))
    ex = copy.deepcopy(g["exported"])
    victim = next(h for h, v in ex["blobLabels"].items() if v == "fact-payload:calls")
    del ex["blobs"][victim]
    rep = CL.close_run(Store.load(ex), ex["runId"])
    avail = {"schemaVersion": 2, "runId": g["runId"], "generation": 1, "state": "partial", "missingRefs": [{"domain": "fact-payload", "digest": victim}],
             "reason": "committed fact payload bytes are missing from the store"}
    aok, aerrs = P7.admit(avail, ID, "#/$defs/availability")
    states = {
        "complete-empty": {"run": "ts-pass", "rules": [{"ruleId": r["ruleId"], "selectedSubjects": len(r["enumeration"]["selectedSubjectIds"]), "findings": 0} for r in empty_rules],
                           "meaning": "complete population, determinate roots, zero findings: a real empty result"},
        "partial": {"run": "ts-pass", "cellOutcomes": partial_cells, "coverageEntries": partial_cov,
                    "meaning": "work ran but a typed deficiency remains (clones-fact over non-code files: language-tier-unsupported / capability-missing)"},
        "unavailable": {"candidateOutcome": unavailable, "providerTrace": {"file": "traces/unavailable.json", "keys": sorted(trace)[:12]},
                        "availabilityNotices": multi["availability"]["totalNoticeCount"],
                        "meaning": "the work was not performed or the capability is not installed; typed, never an empty result"},
        "missing-committed-bytes": {"removedBlob": victim, "closeRun": rep["result"], "firstRefusal": (rep.get("faultsInStageOrder") or [None])[0],
                                    "firstRefusalStage": (rep.get("firstRefusal") or {}).get("stage"),
                                    "availabilityRecord": avail, "availabilityAdmitted": aok, "availabilityErrors": aerrs,
                                    "meaning": "a committed record's bytes are gone: custody refusal (evidence.missing), not correspondence-incomplete and not partial evidence"}}
    must("state-complete-empty", bool(empty_rules), [r["ruleId"] for r in g["proof"]["ruleResults"]])
    must("state-partial", bool(partial_cells) and bool(partial_cov))
    must("state-unavailable", unavailable["state"] == "unavailable")
    must("state-missing", rep["result"] == "REFUSE" and aok, (rep["result"], aerrs))
    dump("vectors/empty-partial-unavailable-missing.json", {"classification": "valid", "states": states, "labelsDistinct": len(states) == 4,
                                                           "selectors": ["workflow-projection-contract.v3 s0 table", "workflows-and-surfaces.md s8 line 991 (empty findings is a real empty result)",
                                                                         "identity-schemas.v3.json#/$defs/availability", "execution-inputs outcome states complete|partial|unavailable"]})


# ------------------------------------------------------------------ detector compatibility listing
def detector_compat():
    st = Store()
    base_id, base_desc = mk_closure(st, "detector", "cb24-ts-pack", {"rules/pack.json": DEFAULT_PACK})
    listing = K.C({"schemaFamily": "opensip.product.detector-manifest", "schemaMajor": 1, "compatibleClosures": [{"closureId": base_id, "semanticsMajor": 1}]})
    pack11 = b"{\"pack\":\"cb24.ts-pack\",\"semantics\":\"1.1\"}\n"
    cur_id, cur_desc = mk_closure(st, "detector", "cb24-ts-pack", {"rules/pack.json": pack11, DC.RESERVED: listing}, "1.1.0")
    adm = DC.admit_listing(st, cur_id, cur_desc, "retained-generation")
    manifest_body = st.blobs[cur_desc["manifestDigest"]]
    mok, _ = P7.admit(json.loads(manifest_body), DC.DOC, "#")
    vectors = [{"vector": "listing-names-baseline-same-major", "classification": "valid", "state": adm["state"],
                "declaredCompatible": DC.declared_compatible(adm, base_id, 1), "listing": adm["listing"],
                "componentManifestDigest": cur_desc["manifestDigest"], "listingIsNotManifestDigest": adm["listing"]["sha256"] != cur_desc["manifestDigest"],
                "manifestBodyIsNotADetectorManifest": not mok, "pass": adm["state"] == "listing" and DC.declared_compatible(adm, base_id, 1) and not mok}]
    vectors.append({"vector": "same-listing-other-major", "classification": "valid", "declaredCompatible": DC.declared_compatible(adm, base_id, 2),
                    "pass": not DC.declared_compatible(adm, base_id, 2)})
    a = DC.admit_listing(st, base_id, base_desc, "retained-generation")
    vectors.append({"vector": "reserved-path-absent-is-no-declaration", "classification": "valid", "state": a["state"], "pass": a["state"] == "absent"})

    def variant(label, files, expect_state, expect_refusal=None, origin="retained-generation", desc_edit=None):
        s2 = Store()
        cid, desc = mk_closure(s2, "detector", "cb24-ts-pack", files, "1.1.0")
        if desc_edit:
            desc = desc_edit(s2, copy.deepcopy(desc))
        r = DC.admit_listing(s2, cid, desc, origin)
        ok = r["state"] == expect_state and (expect_refusal is None or (r["firstRefusal"] or "").startswith(expect_refusal))
        vectors.append({"vector": label, "classification": "valid" if expect_state != "refused" else "invalid", "state": r["state"],
                        "firstRefusal": r["firstRefusal"], "declaredCompatible": DC.declared_compatible(r, base_id, 1), "pass": ok})

    empty = K.C({"schemaFamily": "opensip.product.detector-manifest", "schemaMajor": 1, "compatibleClosures": []})
    variant("empty-listing-is-complete-none", {"rules/pack.json": pack11, DC.RESERVED: empty}, "listing")
    variant("malformed-listing-refuses", {"rules/pack.json": pack11, DC.RESERVED: b"{not json"}, "refused", "cb24.DETECTOR_LISTING_MALFORMED")
    variant("unrecognized-listing-refuses", {"rules/pack.json": pack11, DC.RESERVED: K.C({"schemaFamily": "opensip.product.detector-manifest", "schemaMajor": 2,
                                                                                         "compatibleClosures": []})}, "refused", "cb24.DETECTOR_LISTING_UNRECOGNIZED")

    def wrong_length(s2, d):
        for r in d["tree"]:
            if r["path"] == DC.RESERVED:
                r["bytes"] += 1
        return d

    def missing_bytes(s2, d):
        for r in d["tree"]:
            if r["path"] == DC.RESERVED:
                del s2.blobs[r["sha256"]]
        return d

    def duplicate(s2, d):
        row = next(r for r in d["tree"] if r["path"] == DC.RESERVED)
        d["tree"].append(dict(row, sha256=s2.put_bytes(empty), bytes=len(empty)))
        return d

    def manifest_as_listing(s2, d):
        d["tree"] = [r for r in d["tree"] if r["path"] != DC.RESERVED]
        d["manifestDigest"] = s2.put_bytes(listing)
        return d
    variant("length-mismatch-refuses", {"rules/pack.json": pack11, DC.RESERVED: listing}, "refused", "cb24.DETECTOR_LISTING_DIGEST_OR_LENGTH_MISMATCH", desc_edit=wrong_length)
    variant("listed-bytes-missing-refuses", {"rules/pack.json": pack11, DC.RESERVED: listing}, "refused", "cb24.DETECTOR_LISTING_BYTES_MISSING", desc_edit=missing_bytes)
    variant("non-unique-reserved-path-refuses", {"rules/pack.json": pack11, DC.RESERVED: listing}, "refused", "cb24.DETECTOR_LISTING_PATH_NOT_UNIQUE", desc_edit=duplicate)
    variant("caller-supplied-trust-refuses", {"rules/pack.json": pack11, DC.RESERVED: listing}, "refused", "cb24.DETECTOR_LISTING_TRUST_ORIGIN_NOT_ADMITTED", origin="request-map")
    variant("listing-bytes-in-manifestDigest-are-not-a-declaration", {"rules/pack.json": pack11}, "absent", desc_edit=manifest_as_listing)
    gdet = loaded("cmp-code-detc")
    gbase = loaded("cmp-base")
    dcur = next((row["id"], gdet["store"].get_object(row["id"])) for row in gdet["exported"]["objectTable"]
                if row["domain"] == "closure" and gdet["store"].get_object(row["id"])["kind"] == "detector")
    dbase = next(row["id"] for row in gbase["exported"]["objectTable"] if row["domain"] == "closure" and gbase["store"].get_object(row["id"])["kind"] == "detector")
    committed = DC.admit_listing(gdet["store"], dcur[0], dcur[1], "retained-generation")
    vectors.append({"vector": "committed-run-cmp-code-detc-listing", "classification": "valid", "state": committed["state"],
                    "declaredCompatibleWithCmpBaseDetector": DC.declared_compatible(committed, dbase, 1), "projection": committed,
                    "pass": committed["state"] == "listing" and DC.declared_compatible(committed, dbase, 1)})
    for v in vectors:
        must(f"detector-compat:{v['vector']}", v["pass"], v)
    dump("vectors/detector-compat-file.json", {"classification": "valid", "reservedPath": DC.RESERVED, "vectors": vectors,
                                              "owners": {"listing admission (tree path, bytes, schema)": "workflows-and-surfaces.md s2 lines 289-296; projection contract s14",
                                                         "component manifest body / closure.manifestDigest": "identity-schemas.v3 #/$defs/closure manifestDigest (security metadata body); projection contract s13, s15",
                                                         "signature and platform tree authentication": "security TCB (not performed)"},
                                              "refusalKeysSpelledInKit": False})


def main():
    authorization()
    purge_replay_output()
    public_termination()
    cases = host_captured_vs_candidate()
    four_states(cases)
    detector_compat()
    print("failures", len(failures))
    print(json.dumps(failures, default=str)[:8000])
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
