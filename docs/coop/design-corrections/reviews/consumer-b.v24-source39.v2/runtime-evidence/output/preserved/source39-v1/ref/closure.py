"""Complete Run closure and independent semantic replay over an exported store.

identity-and-evidence s3 (identities, closing digest law, closure membership), s4 (evaluation), composition s7
(complete replay criterion). Reported separately: graph admission (owner records, joins, digest law) and semantic
replay (every evaluator output recomputed from admitted inputs only, then compared byte-for-byte with retained claims).
Replay is attempted only after graph admission succeeds ("input admission precedes replay").
"""
import json

import canonical as K
import cve1
import digestlaw
import enumeration as EN
import evaluator as EV
import execinputs as XI
import imports as IM
import membership as M
import native_ctx as NC
import native_facts as NF
import schemas
import source39 as S39

KIT = schemas.kit()
ID = "foundation/identity-schemas.v3.json"
NE = "native/native-evidence.schemas.v2.json"
PDOC1 = "workflows/schemas/policy-document.schema.json"
PDOC2 = "workflows/schemas/policy-document.v2.schema.json"
XI_DOC = "foundation/execution-inputs.schema.v1.json"
INV_DOC = "foundation/subject-inventory.schema.v1.json"
PARAM_ROWS = KIT.doc(ID)["x-opensip-payload-registry"]["classes"]["parameter"]["rows"]
MATRIX_IDS = {c["id"] for c in EN.MATRIX["capabilities"]}
ENUM_KEY = "foundation/enumeration-plan.schema.v1.json"
EMIT_KEY = "foundation/evaluator-emission-plan.schema.v1.json"
SCOPE_KEY = "workflows/schemas/policy-document.schema.json#/$defs/ScopeDocumentV1"


class Fault(Exception):
    def __init__(self, key, detail=""):
        super().__init__(f"{key}:{detail}" if detail else key)
        self.key = key
        self.detail = detail


def first_diff(a, b, path="$"):
    if type(a) is not type(b):
        return path
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a or k not in b:
                return f"{path}.{k}"
            d = first_diff(a[k], b[k], f"{path}.{k}")
            if d:
                return d
        return None
    if isinstance(a, list):
        if len(a) != len(b):
            return f"{path}[len {len(a)}!={len(b)}]"
        for i, (x, y) in enumerate(zip(a, b)):
            d = first_diff(x, y, f"{path}[{i}]")
            if d:
                return d
        return None
    return None if a == b else path


class Closure:
    def __init__(self, store):
        self.store = store
        self.faults = []
        self.admitted = []

    def fault(self, key, detail=""):
        self.faults.append(f"{key}:{detail}" if detail else key)

    def obj(self, ident, domain):
        if not isinstance(ident, str) or not ident.startswith(K.PREFIX[domain] + ":"):
            raise Fault("IDENTITY_PREFIX", f"{domain}:{ident}")
        hx = ident.split(":", 1)[1]
        if hx not in self.store.blobs:
            raise Fault("EVIDENCE_UNAVAILABLE", ident)
        try:
            d, v = self.store.get_frame(hx, {domain})
        except K.AdmissionError as exc:
            raise Fault("IDENTITY_FRAME_REFUSED", f"{ident}:{exc.boundary}")
        if K.identifier(domain, v) != ident:
            raise Fault("IDENTITY_MISMATCH", ident)
        r = KIT.admit(v, ID, f"#/$defs/{domain}")
        if not r["ok"]:
            raise Fault("SCHEMA_REFUSED", f"{domain}:{r['typed']}{r['stock'][:1]}{r['order'][:1]}")
        self.admitted.append((ident, v, ID, f"#/$defs/{domain}"))
        return v

    def rec(self, hx, doc, sel, label):
        if not isinstance(hx, str) or hx not in self.store.blobs:
            raise Fault("EVIDENCE_UNAVAILABLE", label)
        try:
            v = self.store.get_record(hx)
        except K.AdmissionError as exc:
            raise Fault("RECORD_NOT_CANONICAL", f"{label}:{exc.boundary}")
        r = KIT.admit(v, doc, sel)
        if not r["ok"]:
            raise Fault("SCHEMA_REFUSED", f"{label}:{r['typed']}{r['stock'][:1]}{r['order'][:1]}")
        self.admitted.append((label, v, doc, sel))
        return v


def close_run(store, run_id):
    C = Closure(store)
    report = {"runId": run_id, "result": None, "graphAdmission": {}, "semanticReplay": {"performed": False}}
    g = {}
    try:
        g = admit_graph(C, run_id)
    except (Fault, NC.Refusal, K.AdmissionError, EV.EvalRefusal) as exc:
        key = getattr(exc, "key", None) or getattr(exc, "boundary", None) or str(exc)
        C.fault(key, getattr(exc, "detail", ""))
    except Exception as exc:  # checker defect: reported explicitly, never an ADMIT
        C.fault("cb24.CLOSURE_INTERNAL_ERROR", f"{type(exc).__name__}:{exc}")
    report["graphAdmission"] = {"faults": C.faults, "admittedRecords": len(C.admitted),
                                "digestLaw": g.get("digestLaw"), "summary": g.get("summary")}
    if C.faults:
        report["result"] = "REFUSE"
        return report
    rep = replay(C, g)
    report["semanticReplay"] = rep
    report["result"] = "ADMIT" if not rep["faults"] else "REFUSE"
    return report


def admit_graph(C, run_id):
    store = C.store
    run = C.obj(run_id, "run")
    plan_id = run["planId"]
    plan = C.obj(plan_id, "plan")
    seal = C.obj(run["evaluationSealId"], "evaluation-seal")
    evidence = C.obj(run["evidenceId"], "semantic-evidence")
    proof = C.obj(seal["proofBundleId"], "proof-bundle")
    snapshot = C.obj(plan["snapshotId"], "snapshot")
    for a, b, name in ((seal["planId"], plan_id, "seal.planId"), (evidence["planId"], plan_id, "evidence.planId"),
                       (proof["planId"], plan_id, "proof.planId"), (evidence["proofBundleId"], seal["proofBundleId"], "evidence.proofBundleId"),
                       (seal["executionPlanId"], proof["executionPlanId"], "seal.executionPlanId"),
                       (seal["evaluatorClosure"], proof["evaluatorClosure"], "seal.evaluatorClosure"),
                       (seal["policyDigest"], plan["policyDigest"], "seal.policyDigest"), (run["snapshotId"], plan["snapshotId"], "run.snapshotId"),
                       (run["projectId"], snapshot["projectId"], "run.projectId"),
                       (run["capabilityManifestId"], plan["capabilityManifestId"], "run.capabilityManifestId"),
                       (seal["verdict"], proof["verdict"], "seal.verdict")):
        if a != b:
            C.fault("RUN_JOIN", name)
    # capability manifest (CAP-MANIFEST-ID-V1 over the committed CVE1 bytes)
    mb = store.blobs.get(plan["capabilityManifestBytesDigest"])
    if mb is None:
        C.fault("EVIDENCE_UNAVAILABLE", "plan.capabilityManifestBytesDigest")
    else:
        try:
            adm = cve1.CapabilityAdmission().admit(cve1.decode(mb))
            if adm["result"] != "ADMIT" or adm["committedBytesHex"] != mb.hex():
                C.fault("RELEASE.CAPABILITY_MANIFEST_NOT_CANONICAL", str(adm.get("firstRefusal")))
            if cve1.capability_manifest_id(mb) != plan["capabilityManifestId"]:
                C.fault("CAPABILITY_MANIFEST_ID_MISMATCH")
        except cve1.CVE1Error as exc:
            C.fault("RELEASE.CAPABILITY_MANIFEST_NOT_CANONICAL", exc.code)
    # snapshot
    inv_rows = snapshot["sourceInventory"]
    inv_bytes = {}
    for row in inv_rows:
        b = store.blobs.get(row["sha256"])
        if b is None:
            C.fault("EVIDENCE_UNAVAILABLE", f"source:{row['path']}")
        elif len(b) != row["bytes"]:
            C.fault("BLOB_LENGTH", row["path"])
        else:
            inv_bytes[row["path"]] = b
    config = C.rec(snapshot["resolvedConfigDigest"], ID, "#/$defs/semantic-configuration", "configuration")
    scope = C.rec(snapshot["scopeDigest"], ID, "#/$defs/scope-descriptor", "scope-descriptor")
    vcs = C.rec(snapshot["vcsDigest"], ID, "#/$defs/vcs-observation", "vcs-observation")
    if vcs["sourceInventoryDigest"] != K.raw_digest(inv_rows):
        C.fault("VCS_SOURCE_INVENTORY_JOIN")
    if plan["resolvedConfigDigest"] != snapshot["resolvedConfigDigest"]:
        C.fault("PLAN_SNAPSHOT_JOIN", "resolvedConfigDigest")
    if plan["scopeDigest"] != snapshot["scopeDigest"]:
        C.fault("PLAN_SNAPSHOT_JOIN", "scopeDigest")
    if plan["budget"] != config["analysis"]["budget"]:
        C.fault("PLAN_CONFIG_JOIN", "budget")
    # HC-19: native Config2 join - explicit workspaceRoots are exact roots ("." is the project root ""); absent roots are zero-config
    # discovery, the only case with the U-9 syntax-only fallback.
    cfg_discovery = config.get("discovery", {})
    explicit_roots = [("" if r == "." else r) for r in cfg_discovery.get("workspaceRoots", [])] or None
    try:
        discovery = M.discover_units(inv_bytes, None, explicit_roots)
    except K.AdmissionError as exc:
        raise Fault(exc.boundary, getattr(exc, "detail", ""))
    derived_scope = M.unit_scope_descriptor(discovery, cfg_discovery.get("ignorePaths", []), cfg_discovery.get("workspaceRoots") or None)
    if derived_scope != scope:
        C.fault("cb24.SCOPE_DESCRIPTOR_DERIVATION", first_diff(derived_scope, scope))
    # analysis spec and parameters
    spec = C.rec(plan["analysisSpecDigest"], ID, "#/$defs/analysis-spec", "analysis-spec")
    tuples = set()
    for rc in spec["requestedCapabilities"]:
        t = (rc["capabilityId"], rc["languageMode"], rc["workspaceRoot"])
        if t in tuples:
            C.fault("native.requested-capability-duplicate-ownership-tuple", str(t))
        tuples.add(t)
        if rc["capabilityId"] not in MATRIX_IDS:
            C.fault("native.requested-capability-unregistered", rc["capabilityId"])
        elif rc["languageMode"] not in EN.LANGUAGE_MODES:
            C.fault("ANALYSIS_SPEC_LANGUAGE_MODE_UNREGISTERED", rc["languageMode"])
        elif EN.cell_state(rc["capabilityId"], rc["languageMode"])["state"] == "NOT-SELECTED":
            C.fault("native.requested-capability-mode-not-selected", str(t))
    params = {}
    for p in spec["parameters"]:
        key = next((k for k, row in PARAM_ROWS.items() if KIT.digest(row["document"]) == p["schemaDigest"]), None)
        if key is None:
            C.fault("PARAMETER_SCHEMA_UNREGISTERED", p["schemaDigest"])
            continue
        row = PARAM_ROWS[key]
        if store.blobs.get(p["schemaDigest"]) != KIT.raw[schemas.norm_rel(row["document"])]:
            C.fault("EVIDENCE_UNAVAILABLE", f"parameter-schema:{row['document']}")
        params.setdefault(key, []).append(C.rec(p["payloadDigest"], row["document"], row["selector"], f"parameter:{key}"))
    # HC-23: x-opensip-payload-registry.classes.parameter.selectionCardinality - at most one parameter per registered row
    for key, rows in sorted(params.items()):
        if len(rows) > 1:
            C.fault("ANALYSIS_SPEC_PARAMETER_SELECTION_AMBIGUOUS", key)
    for key in (ENUM_KEY, EMIT_KEY):
        if not params.get(key):
            C.fault("EVALUATOR_PARAMETER_CARDINALITY", key)
    if not params.get(ENUM_KEY) or not params.get(EMIT_KEY):
        raise Fault("EVALUATOR_PARAMETER_CARDINALITY", "required-evaluator3-parameter-absent")
    enum = params[ENUM_KEY][0]
    emission = params[EMIT_KEY][0]
    scope_document = (params.get(SCOPE_KEY) or [None])[0]
    grant = C.rec(plan["semanticGrantDigest"], ID, "#/$defs/semantic-grant", "semantic-grant")
    if grant["projectId"] != snapshot["projectId"] or grant["scopeDigest"] != plan["scopeDigest"]:
        C.fault("SEMANTIC_GRANT_JOIN")
    if bool(plan["importIds"]) != ("read-import" in grant["analysisOperations"]):
        C.fault("SEMANTIC_GRANT_READ_IMPORT_JOIN")
    if ("prepare-code" in grant["analysisOperations"]) != any(pr["kind"] == "trusted-repository-code" for pr in grant["principals"]):
        C.fault("SEMANTIC_GRANT_PREPARE_CODE_JOIN")
    policy = C.rec(plan["policyDigest"], PDOC2, "#/$defs/PolicyDocumentV2", "policy")
    waivers = C.rec(plan["waiverDigest"], PDOC1, "#/$defs/WaiverSetV1", "waivers")
    # closures (direct members)
    closures = {}
    for cid in plan["semanticClosures"]:
        try:
            closures[cid] = NC.admit_closure(store, cid, None, refusal_prefix="cb24.semantic-closure")
        except NC.Refusal as exc:
            C.fault(exc.key, exc.detail)
    # emission plan joins (composition s1)
    if emission["policyDigest"] != plan["policyDigest"]:
        C.fault("EMISSION_PLAN_POLICY_JOIN")
    prules = {r["ruleId"]: r for r in policy["rules"]}
    if sorted(r["ruleId"] for r in emission["rules"]) != sorted(prules):
        C.fault("EMISSION_PLAN_RULE_TOTALITY")
    ns = set()
    for er in emission["rules"]:
        pr = prules.get(er["ruleId"])
        if pr is not None:
            ref = pr["ruleProgramRef"]
            if (er["contributionId"], er["ruleStableId"], er["semanticsMajor"]) != (ref["contributionId"], ref["ruleStableId"], ref["semanticsMajor"]):
                C.fault("EMISSION_PLAN_RULE_REF_JOIN", er["ruleId"])
        dc = closures.get(er["detectorClosure"])
        if dc is None or dc["kind"] != "detector":
            C.fault("EMISSION_PLAN_DETECTOR_CLOSURE", er["ruleId"])
        k = (er["ruleStableId"], er["semanticsMajor"])
        if k in ns:
            C.fault("EMISSION_PLAN_FINGERPRINT_NAMESPACE_DUPLICATE", str(k))
        ns.add(k)
    for r in policy["rules"]:
        if r["subjectEnumeration"]["universe"] not in EV.PROFILE["policyUniverseMap"]:
            C.fault("EVALUATOR_POLICY_UNIVERSE_TOKEN_UNKNOWN", r["subjectEnumeration"]["universe"])
    # native contexts and universes
    admissions = {}
    for hx in plan["nativeContextDigests"]:
        try:
            a = NC.admit_native_context(store, hx, inv_rows)
            for rf in a["refusals"]:
                C.fault(rf)
            admissions[hx] = a
        except NC.Refusal as exc:
            C.fault(exc.key, exc.detail)
    bound = {}
    for cell in enum["cells"]:
        for b in cell["programBindings"]:
            if b["universe"] is not None and b["universe"] not in bound:
                try:
                    bu = NC.bind_universe(store, b["universe"], admissions, inv_rows)
                    for f in bu.get("faults", []):
                        C.fault(f)
                    bound[b["universe"]] = bu
                except NC.Refusal as exc:
                    C.fault(exc.key, exc.detail)
    membership_rec = C.rec(enum["membershipDigest"], NE, "#/$defs/UnitMembershipV1", "unit-membership")
    # HC-18: native U-4b.5 enforces order and row derivation over the RETAINED record (EN.admit_enumeration). The original
    # cb24.UNIT_MEMBERSHIP_DERIVATION re-derivation from snapshot bytes is withdrawn: closure cannot see the security boundary
    # inventory, which the Plan does not retain.
    # HC-21: identity s3 "What sourceInventory contains" - a row inside a pruned tree must be a read of a Plan-selected TypeScript
    # context's committed node_modules layout; VCS-tree and Cargo build-output rows never are.
    layouts = [a["detail"]["layout"] for a in admissions.values()
               if a["domain"] == "native.context.typescript.v2" and a["detail"].get("layout") is not None]
    for f in S39.pruned_read_faults(inv_rows, M.retained_cargo_roots(membership_rec["units"]), layouts):
        C.fault(f)
    # execution inputs (located by the proof; admitted as an INPUT, re-derived below)
    xi = C.rec(proof["executionInputsDigest"], XI_DOC, "#", "execution-inputs")
    inventories = []
    candidates = {}
    for ref in xi["hostCapture"]["hostDerivedRefs"]:
        if ref["domain"] == "subject-inventory":
            inventories.append((ref["digest"], C.rec(ref["digest"], INV_DOC, "#", f"subject-inventory:{ref['digest'][:12]}")))
        elif ref["domain"] == "candidate-producer-result":
            candidates[ref["digest"]] = C.rec(ref["digest"], XI_DOC, "#/$defs/CandidateProducerResultV1", "candidate")
        else:
            C.fault("cb24.SIDECAR_NOT_RECONSTRUCTED", ref["domain"])
    efaults, index = EN.admit_enumeration(plan, plan_id, spec, scope, membership_rec, enum, inventories, bound, closures, inv_bytes)
    for f in efaults:
        C.fault(f)
    if index is None:
        raise Fault("ENUMERATION_REFUSED")
    exec_plan_id = xi["executionPlanId"]
    exec_plan = C.obj(exec_plan_id, "execution-plan")
    if exec_plan["planId"] != plan_id:
        C.fault("EXECUTION_PLAN_JOIN")
    stage_specs = {}
    for st in exec_plan["stages"]:
        spec_rec = C.rec(st["stageSpecDigest"], ID, "#/$defs/stage-spec", f"stage-spec:{st['ordinal']}")
        stage_specs[st["stageSpecDigest"]] = spec_rec
        if spec_rec["planId"] != plan_id:
            C.fault("STAGE_SPEC_PLAN_JOIN", str(st["ordinal"]))
        pc = closures.get(spec_rec["producerClosure"])
        if pc is None or pc["kind"] != "provider":
            C.fault("STAGE_SPEC_PRODUCER_CLOSURE", str(st["ordinal"]))
        if sorted(spec_rec["outputDomains"]) != sorted(st["outputDomains"]):
            C.fault("STAGE_SPEC_OUTPUT_DOMAINS", str(st["ordinal"]))
        # HC-15: identity s3 - the stage output schema is registered by the producer closure's tree
        if pc is not None:
            for f in S39.stage_output_faults(store, spec_rec, pc):
                C.fault(f, str(st["ordinal"]))
        # HC-22: identity s3 / $defs/stage-spec parameters - a stage takes no hidden input
        spec_rows = {K.C(p) for p in spec["parameters"]}
        if any(K.C(p) not in spec_rows for p in spec_rec["parameters"]):
            C.fault("STAGE_SPEC_HIDDEN_PARAMETER", str(st["ordinal"]))
        if any(q >= st["ordinal"] for q in st["requires"]):
            C.fault("EXECUTION_PLAN_REQUIRES_ORDER", str(st["ordinal"]))
    # selected views and their members (closure membership + native producer admission re-run)
    views, scopes, coverages, facts, payloads = {}, {}, {}, {}, {}
    for rec in xi["hostCapture"]["stageReceipts"]:
        if rec["state"] != "complete":
            continue
        for o in rec["outputRefs"]:
            if o["domain"] != "view":
                continue
            vid = "view2:" + o["digest"]
            v = C.obj(vid, "view")
            views[vid] = v
            pc = closures.get(v["producerClosure"])
            if pc is None or pc["kind"] != "provider":
                C.fault("VIEW_PRODUCER_CLOSURE_NOT_SELECTED", vid)
            for sid in v["scopeIds"]:
                if sid not in scopes:
                    scopes[sid] = C.obj(sid, "subject-scope")
                    for f in NF.scope_faults(scopes[sid], plan["snapshotId"], bound, closures):
                        C.fault(f, sid)
            for fid in v["facts"]:
                if fid not in facts:
                    facts[fid] = C.obj(fid, "fact")
                    if facts[fid]["producerClosure"] != v["producerClosure"]:
                        C.fault("FACT_PRODUCER_VIEW_JOIN", fid)
                    ff, payload = NF.fact_faults(store, facts[fid], plan["snapshotId"], inv_rows, bound)
                    for f in ff:
                        C.fault(f, fid)
                    payloads[fid] = payload
            for cid in v["coverageIds"]:
                if cid not in coverages:
                    cov = C.obj(cid, "coverage")
                    sc = scopes.get(cov["scopeId"])
                    if sc is None:
                        C.fault("native.coverage-subject-scope-outside-view", cid)
                        continue
                    if bound.get(sc["sourceUniverse"]) is None:
                        C.fault("cb24.COVERAGE_UNIVERSE_UNBOUND", cid)
                        continue
                    vfp = [(facts[f], payloads[f]) for f in v["facts"] if payloads.get(f) is not None]
                    cf, cpay = NF.coverage_faults(store, cov, sc, cov["scopeId"], vfp, bound.get(sc["sourceUniverse"]), inv_rows)
                    for f in cf:
                        C.fault(f, cid)
                    coverages[cid] = (cov, cpay)
                    C.admitted.append((f"coverage-payload:{cid}", cpay, NE, "#/$defs/CoverageResultV3"))
            for f in NF.view_faults(v, plan_id, scopes, {c: coverages[c][0] for c in v["coverageIds"] if c in coverages}, facts,
                                    set(digestlaw.REGISTERED_DOCS)):
                C.fault(f, vid)
            for f in NF.totality_faults(v, scopes, {c: coverages[c][0] for c in v["coverageIds"]}, facts, payloads, inv_rows,
                                        {c: coverages[c][1] for c in v["coverageIds"]}):
                C.fault(f, vid)
    for fid, f in facts.items():
        if payloads.get(fid) is not None:
            C.admitted.append((f"fact-payload:{fid}", payloads[fid], "foundation/relation-payload-schemas.v2.json",
                               NF.RELS[f["relation"]]["selector"]))
    imports_adm = {}
    for iid in plan["importIds"]:
        w = C.obj(iid, "import")
        res = IM.admit_import(store, iid, w, plan)
        for f in res["faults"]:
            C.fault(f, iid)
        C.admitted += res["admitted"]
        imports_adm[iid] = res
    ctx = {"enum_index": index, "views": views, "scopes": scopes, "coverages": coverages, "candidates": candidates,
           "vcs_kind": vcs["kind"], "sidecar_refs": []}
    xfaults, derived = XI.admit(xi, plan, plan_id, exec_plan, exec_plan_id, enum, closures, stage_specs, ctx)
    for f in xfaults:
        C.fault(f)
    # digest law over every admitted record
    law = {"records": 0, "annotatedFields": 0, "unannotatedOutsideLaw": {}}
    for label, inst, doc, sel in C.admitted:
        res = digestlaw.check_instance(store, inst, doc, sel, {"plan": plan})
        law["records"] += 1
        law["annotatedFields"] += res["annotated"]
        for f in res["faults"]:
            C.fault(f, label)
        if res["unannotatedOutsideLaw"]:
            law["unannotatedOutsideLaw"][f"{doc}{sel}"] = res["unannotatedOutsideLaw"]
    summary = {"closures": len(closures), "contexts": len(admissions), "universes": len(bound), "inventories": len(inventories),
               "views": len(views), "scopes": len(scopes), "coverages": len(coverages), "facts": len(facts),
               "cellOutcomes": [(o["capabilityId"], o["state"], o["deficiency"], o["nativeCause"]) for o in (derived or {}).get("outcomes", [])],
               "requiredRows": len((derived or {}).get("requiredRows", []))}
    return {"run": run, "plan": plan, "plan_id": plan_id, "seal": seal, "evidence": evidence, "proof": proof, "snapshot": snapshot,
            "policy": policy, "waivers": waivers, "emission": emission, "enum": enum, "index": index, "views": views, "scopes": scopes,
            "coverages": coverages, "facts": facts, "payloads": payloads, "bound": bound, "xi": xi, "derived": derived,
            "exec_plan_id": exec_plan_id, "scope_document": scope_document, "digestLaw": law, "summary": summary,
            "imports": imports_adm}


def replay(C, g):
    store = C.store
    faults = []
    inp = EV.Inputs(plan=g["plan"], plan_id=g["plan_id"], exec_plan_id=g["exec_plan_id"], evaluator_closure=g["xi"]["evaluatorClosure"],
                    policy=g["policy"], waivers=g["waivers"], emission=g["emission"], enum_plan=g["enum"],
                    inventories=g["index"]["inventories"], views=g["views"], scopes=g["scopes"], coverages=g["coverages"],
                    facts=g["facts"], fact_payloads=g["payloads"], bound=g["bound"],
                    imports={i: r["wrapper"] for i, r in g["imports"].items()},
                    import_payloads={i: r["payload"] for i, r in g["imports"].items()},
                    import_observations={i: r["observation"] for i, r in g["imports"].items()},
                    import_scopes={i: r["scope"] for i, r in g["imports"].items()},
                    import_flags={i: r["flags"] for i, r in g["imports"].items()}, exec_inputs=g["xi"],
                    exec_inputs_digest=g["proof"]["executionInputsDigest"], required_rows=g["derived"]["requiredRows"],
                    scope_document=g["scope_document"], project_id=g["snapshot"]["projectId"])
    try:
        out = EV.evaluate(inp)
    except EV.EvalRefusal as exc:
        return {"performed": True, "faults": [f"EVALUATION_REFUSED:{exc.key}"]}
    if K.C(out["proof"]) != K.C(g["proof"]):
        faults.append(f"SEMANTIC_REPLAY_PROOF_MISMATCH:{first_diff(out['proof'], g['proof'])}")
    checks = ((out["proofId"], g["seal"]["proofBundleId"], "proofBundleId"), (out["evidenceId"], g["run"]["evidenceId"], "evidenceId"),
              (out["sealId"], g["run"]["evaluationSealId"], "evaluationSealId"), (out["runId"], C.admitted[0][0], "runId"))
    for a, b, name in checks:
        if a != b:
            faults.append(f"SEMANTIC_REPLAY_IDENTITY_MISMATCH:{name}")
    for ident, (dom, desc) in out["objects"].items():
        hx = ident.split(":", 1)[1]
        if hx not in store.blobs:
            if dom != "policy-derivation":
                faults.append(f"SEMANTIC_REPLAY_OUTPUT_OBJECT_MISSING:{ident}")
            continue
        try:
            d, v = store.get_frame(hx, {dom})
        except K.AdmissionError as exc:
            faults.append(f"SEMANTIC_REPLAY_OUTPUT_OBJECT_REFUSED:{ident}:{exc.boundary}")
            continue
        if K.C(v) != K.C(desc):
            faults.append(f"SEMANTIC_REPLAY_OUTPUT_OBJECT_MISMATCH:{ident}:{first_diff(desc, v)}")
    for d, b in out["blobs"].items():
        if store.blobs.get(d) != b:
            faults.append(f"SEMANTIC_REPLAY_OUTPUT_PREIMAGE_MISSING:{d}")
    # every output preimage of the recomputed graph obeys the digest law too
    for ident, (dom, desc) in out["objects"].items():
        for f in digestlaw.check_instance(store, desc, ID, f"#/$defs/{dom}", {"plan": g["plan"]})["faults"]:
            if dom != "policy-derivation" or "MISSING" not in f:
                faults.append(f"{f}:{ident}")
    proof = out["proof"]
    return {"performed": True, "faults": faults,
            "recomputed": {"proofId": out["proofId"], "evidenceId": out["evidenceId"], "sealId": out["sealId"], "runId": out["runId"],
                           "policyDerivationId": out["policyDerivationId"], "verdict": proof["verdict"],
                           "evaluationState": proof["evaluationState"], "findingIds": proof["findingIds"],
                           "waivedFindingIds": proof["waivedFindingIds"], "predicateProofCount": len(proof["predicateProofs"]),
                           "ruleOutcomes": {r["ruleId"]: r["outcome"] for r in proof["ruleResults"]},
                           "executionDeficiencies": [(d["cause"], d["nativeCause"]) for d in proof["executionDeficiencies"]],
                           "budget": out["budget"]}}
