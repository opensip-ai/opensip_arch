"""ExecutionInputsV1 derivation and admission (execution-inputs-contract.v1 s1-s7; composition s9.6 bridge).

One derivation function is used twice: by the synthetic host capture that authors the claimed record, and by
closure/replay, which re-derives every derived field from retained owner records plus the host OBSERVATION fields
(stage receipts, per-binding returned viewDigests, stageOrdinal, candidateResultDigest) and compares. Neither path
reads a claimed state/deficiency/account/selectedRefs value.
"""
import canonical as K
import schemas
import source39 as S39
from enumeration import cell_state, MATRIX

KIT = schemas.kit()
ID = "foundation/identity-schemas.v3.json"
XI_DOC = "foundation/execution-inputs.schema.v1.json"
EXEC_REGISTRY = set(KIT.doc(ID)["x-opensip-evaluator-deficiency-registry"]["sources"]["execution"])
CAUSES = KIT.doc("native/native-evidence.schemas.v2.json")["x-opensip-deficiency-cause-registry"]["deficiencies"]
RELREG = KIT.doc("foundation/relation-payload-schemas.v2.json")["x-opensip-relation-registry"]["relations"]
CAPS = {c["id"]: c for c in MATRIX["capabilities"]}
CANDIDATE_CAPS = {"clones-near", "clones-cross-tsjs"}
FORBIDDEN_SELECTED = {"proof-bundle", "finding", "evaluation-seal", "run", "semantic-evidence"}


def cset(items):
    uniq = {K.C(x): x for x in items}
    return [uniq[k] for k in sorted(uniq)]


def sfx(ident):
    return ident.split(":", 1)[1]


def matrix_pair(capability, mode):
    """Matrix cell deficiency plus THAT deficiency's registered cause (execution-inputs s5 unsupported-typed row)."""
    d = cell_state(capability, mode)["deficiency"]
    if d is None:
        return None, None
    row = CAUSES[d]
    if row.get("nativeCause") == "required":
        allowed = row.get("allowedCauses", [])
        if len(allowed) != 1:
            raise K.AdmissionError("cb24.MATRIX_CAUSE_UNDETERMINED", d)
        return d, allowed[0]
    return d, None


def expected_subjects(relation, extents, invs_by_kind, language_mode):
    kind = RELREG[relation]["subjectKind"]
    if kind == "source-path":
        paths = set(extents.get("file", []))
        if "bodyIdentityJoin" in RELREG[relation]:
            # HC-14: bodyEligibilityLaw.census / contract s5 - a body-identity relation is owed only the eligible file-inventory
            # paths under the universe domain of the cell's languageMode.
            domain = S39.universe_domain_of_mode(language_mode)
            paths = {p for p in paths if S39.body_eligible(domain, p)}
        return paths
    inv = invs_by_kind.get("package" if kind == "package-name" else "symbol")
    return {r["nativeSubjectId"] for r in inv["rows"]} if inv else set()


def derive_accounts(ci, cell, b, returned, views, scopes, coverages, extents, invs_by_kind, vcs_kind, faults):
    """Accounts in owed order (matrix relations array as authored). Returns [(NativeCoverageAccountV1, internal)]."""
    U = b["universe"]
    state = cell_state(cell["capabilityId"], cell["languageMode"])["state"]
    out = []
    for rel, rung in CAPS[cell["capabilityId"]]["relations"]:
        if rel == "vcs-change" and vcs_kind == "none":
            app = "inapplicable-vcs"
        elif state == "UNSUPPORTED-TYPED":
            app = "unsupported-typed"
        elif b["enumerator"]["status"] == "unselected":
            app = "unavailable-unselected"
        elif U is None:
            app = "unavailable-null-universe"
        else:
            app = "supported-available"
        # HC-14: contract s5 - targetUniverse has one canonical value, null (schema-typed); sourceUniverse is the binding U.
        acc = {"cellOrdinal": ci, "programOrdinal": b["ordinal"], "relation": rel, "resolution": rung,
               "sourceUniverse": U, "targetUniverse": None, "applicability": app, "coverageIds": []}
        internal = {"accountState": None, "deficiency": None, "nativeCause": None, "coverageRecords": [],
                    "censusMissing": [], "scopeIds": []}
        if app == "supported-available":
            cids = set()
            for vid in returned:
                for cid in views[vid]["coverageIds"]:
                    cov, payload = coverages[cid]
                    k = payload["key"]
                    if k["relation"] != rel or k["resolution"] != rung:
                        continue
                    if k["sourceUniverse"] != U or scopes[cov["scopeId"]]["sourceUniverse"] != U:
                        faults.append(f"EXECUTION_INPUTS_COVERAGE_DERIVE:foreign-universe:{cid}")
                        continue
                    cids.add(cid)
            cids = sorted(cids, key=lambda x: K.C(x))
            acc["coverageIds"] = [sfx(c) for c in cids]
            covered = set()
            for cid in cids:
                cov, payload = coverages[cid]
                e = payload["entry"]
                internal["coverageRecords"].append({"coverage": sfx(cid), "deficiency": e["deficiency"],
                                                    "nativeCause": e["nativeCause"], "coverage_state": e["coverage"]})
                covered |= set(scopes[cov["scopeId"]]["subjects"])
                internal["scopeIds"].append(cov["scopeId"])
            missing = expected_subjects(rel, extents, invs_by_kind, cell["languageMode"]) - covered
            internal["censusMissing"] = sorted(missing, key=lambda x: x.encode())
            complete = bool(cids) and all(r["coverage_state"] == "complete" for r in internal["coverageRecords"]) and not missing
            internal["accountState"] = "complete" if complete else "incomplete"
            if not complete:
                carrier = next(((r["deficiency"], r["nativeCause"]) for r in internal["coverageRecords"] if r["deficiency"] is not None), (None, None))
                internal["deficiency"], internal["nativeCause"] = carrier
        elif app == "unsupported-typed":
            internal["accountState"] = "unsupported"
            internal["deficiency"], internal["nativeCause"] = matrix_pair(cell["capabilityId"], cell["languageMode"])
        elif app in ("unavailable-unselected", "unavailable-null-universe"):
            internal["accountState"] = "unavailable"
            internal["deficiency"], internal["nativeCause"] = b.get("deficiency"), b.get("nativeCause")
        else:
            internal["accountState"] = "inapplicable"
        out.append((acc, internal))
    return out


def candidate_views(ctx):
    """s3 candidate views: the view outputRefs of complete receipts, restricted to admitted views, in canonical order.
    HC-48 (source42 execution-inputs-contract.v1.md s3 line 53): the candidate views are exactly those receipt outputRefs; a view that is
    on selectedRefs but on no complete receipt is refused EXECUTION_INPUTS_SELECTED_COVER (admit), never a candidate. The source41 version
    also drew candidates from the claimed selectedRefs."""
    cand = {"view2:" + r["digest"] for rec in ctx.get("receipts", []) if rec["state"] == "complete" for r in rec["outputRefs"] if r["domain"] == "view"}
    return sorted((v for v in cand if v in ctx["views"]), key=lambda x: K.C(x))


def attributed_views(cell, b, ctx):
    """HC-42 (source41 execution-inputs s3 "View attribution", line 53): a candidate view V is attributed to a row whose enumerator is
    selected with closure P and whose universe U is non-null iff V.producerClosure = P and ONE AND THE SAME named subject-scope S has
    S.sourceUniverse = U and S.relation in the capability's matrix relations (a candidate-only capability: U alone). The matrix cell
    state plays no part; an unselected enumerator or a null U attributes nothing."""
    U = b["universe"]
    if b["enumerator"]["status"] != "selected" or U is None:
        return []
    candidate_only = cell["capabilityId"] in CANDIDATE_CAPS
    rels = {rel for rel, _ in CAPS[cell["capabilityId"]]["relations"]}
    out = []
    # HC-42 follow-on (logs/s41-post-p4to9.0.phase4_tables.log, .5.phase8_envelopes.log): direct derive_outcome callers carry no
    # precomputed candidate set, so it is derived here by the same function derive() uses
    for vid in (ctx["candidate_views"] if "candidate_views" in ctx else candidate_views(ctx)):
        v = ctx["views"][vid]
        if v["producerClosure"] != b["enumerator"]["closureId"]:
            continue
        if any(sid in ctx["scopes"] and ctx["scopes"][sid]["sourceUniverse"] == U and (candidate_only or ctx["scopes"][sid]["relation"] in rels)
               for sid in v["scopeIds"]):
            out.append(vid)
    return out


def attribution_map(enum_plan, receipts, views, scopes, selected_refs=()):
    """HC-42 for the synthetic host capture: {(cellOrdinal, programOrdinal): attributed view2 ids} under s3, over the view outputRefs of
    complete receipts (plus view refs on selectedRefs when supplied)."""
    cand = {"view2:" + r["digest"] for rec in receipts if rec["state"] == "complete" for r in rec["outputRefs"] if r["domain"] == "view"}
    ctx = {"views": views, "scopes": scopes, "candidate_views": sorted((v for v in cand if v in views), key=lambda x: K.C(x))}
    return {(ci, b["ordinal"]): attributed_views(cell, b, ctx) for ci, cell in enumerate(enum_plan["cells"]) for b in cell["programBindings"]}


def derive_outcome(ci, cell, b, obs, ctx, faults):
    """obs: host observation for this binding {viewDigests:[view2 ids], stageOrdinal, candidateResultDigest}.
    ctx: owner records. Returns (CellProgramOutcomeV1 without ordinal, accounts, requiredRows, sources)."""
    U = b["universe"]
    po = b["ordinal"]
    key = (ci, po)
    invs = {k: ctx["enum_index"]["inventories"][(ci, po, k)] for k in cell["kinds"] if (ci, po, k) in ctx["enum_index"]["inventories"]}
    invs_by_kind = {k: v[1] for k, v in invs.items()}
    inv_digests = sorted({v[0] for v in invs.values()}, key=lambda h: K.C(h))
    extents = ctx["enum_index"]["extents"].get(key, {})
    unavailable_binding = b["enumerator"]["status"] == "unselected" or U is None
    # HC-42: the row's views are DERIVED by s3 attribution; the observed viewDigests must equal that canonical set. The source39 helper
    # took the observed list as the returned views (with view-plan / view-producer checks under STAGE_ORDINAL / STAGE_PRODUCER keys).
    observed = list(obs["viewDigests"])
    for vid in observed:
        if vid not in ctx["views"]:
            faults.append(f"EXECUTION_INPUTS_REF_POINTER:{vid}")
    returned = attributed_views(cell, b, ctx)
    if len(set(observed)) != len(observed) or sorted(set(observed), key=lambda x: K.C(x)) != sorted(returned, key=lambda x: K.C(x)):
        faults.append(f"EXECUTION_INPUTS_VIEW_TOTALITY:{ci}:{po}")
    # s3: every scope named by an attributed view has sourceUniverse = U, for every account applicability
    for vid in returned:
        for sid in ctx["views"][vid]["scopeIds"]:
            if ctx["scopes"][sid]["sourceUniverse"] != U:
                faults.append(f"EXECUTION_INPUTS_COVERAGE_DERIVE:scope-universe:{sid}")
    accounts = derive_accounts(ci, cell, b, returned, ctx["views"], ctx["scopes"], ctx["coverages"], extents, invs_by_kind,
                               ctx["vcs_kind"], faults)
    sources = []
    if unavailable_binding:
        sources.append({"source": "binding", "relation": None, "resolution": None, "deficiency": b.get("deficiency"),
                        "nativeCause": b.get("nativeCause"), "inputRefs": []})
    for h in inv_digests:
        inv = next(i for d, i in invs.values() if d == h)
        if inv["state"] != "complete":
            sources.append({"source": "inventory", "relation": None, "resolution": None, "deficiency": inv["deficiency"],
                            "nativeCause": inv["nativeCause"], "inputRefs": [{"domain": "subject-inventory", "digest": h}]})
    candidate_owed = cell["capabilityId"] in CANDIDATE_CAPS and not unavailable_binding
    cand_digest = obs.get("candidateResultDigest") if candidate_owed else None
    env = None
    if candidate_owed:
        if cand_digest is None:
            if cell["required"]:
                faults.append(f"EXECUTION_INPUTS_CANDIDATE_REQUIRED:{ci}:{po}")
            sources.append({"source": "candidate", "relation": None, "resolution": None, "deficiency": None,
                            "nativeCause": None, "inputRefs": []})
        else:
            env = ctx["candidates"].get(cand_digest)
            if env is None:
                faults.append(f"EXECUTION_INPUTS_REF_LOST_BYTES:candidate:{cand_digest}")
            elif env["state"] != "complete":
                sources.append({"source": "candidate", "relation": None, "resolution": None, "deficiency": env["deficiency"],
                                "nativeCause": env["nativeCause"],
                                "inputRefs": [{"domain": "candidate-producer-result", "digest": cand_digest}]})
    for acc, internal in accounts:
        st = internal["accountState"]
        if st == "incomplete":
            if internal["coverageRecords"]:
                for r in internal["coverageRecords"]:
                    sources.append({"source": "coverage", "relation": acc["relation"], "resolution": acc["resolution"],
                                    "deficiency": r["deficiency"], "nativeCause": r["nativeCause"],
                                    "inputRefs": [{"domain": "coverage", "digest": r["coverage"]}]})
            else:
                sources.append({"source": "account", "relation": acc["relation"], "resolution": acc["resolution"],
                                "deficiency": None, "nativeCause": None,
                                "inputRefs": [{"domain": "coverage", "digest": c} for c in acc["coverageIds"]]})
        elif st in ("unsupported", "unavailable"):
            sources.append({"source": "account-" + st, "relation": acc["relation"], "resolution": acc["resolution"],
                            "deficiency": internal["deficiency"], "nativeCause": internal["nativeCause"], "inputRefs": []})
    inv_states = [i["state"] for i in invs_by_kind.values()]
    if unavailable_binding:
        state = "unavailable"
    elif candidate_owed and (cand_digest is None or (env is not None and env["state"] == "unavailable")):
        state = "unavailable"
    elif inv_states and all(s == "unavailable" for s in inv_states) and not returned and (env is None or env["state"] == "unavailable"):
        state = "unavailable"
    elif any(s != "complete" for s in inv_states) or any(i["accountState"] == "incomplete" for _, i in accounts) or \
            (env is not None and env["state"] == "partial"):
        state = "partial"
    else:
        state = "complete"
    carrier = (None, None)
    if state != "complete":
        carrier = next(((s["deficiency"], s["nativeCause"]) for s in sources if s["deficiency"] is not None), (None, None))
    stage_ord = None if unavailable_binding else obs.get("stageOrdinal")
    null_reason = None
    if stage_ord is None:
        null_reason = "optional-unselected" if b["enumerator"]["status"] == "unselected" else "unavailable-binding"
    if not unavailable_binding and state in ("complete", "partial"):
        rec = next((r for r in ctx["receipts"] if r["ordinal"] == stage_ord), None)
        if rec is None or rec["state"] != "complete":
            faults.append(f"EXECUTION_INPUTS_STAGE_ORDINAL:{ci}:{po}")
        else:
            if rec["producerClosure"] != b["enumerator"]["closureId"]:
                faults.append(f"EXECUTION_INPUTS_STAGE_PRODUCER:{ci}:{po}")
            outs = {("view2:" + r["digest"]) for r in rec["outputRefs"] if r["domain"] == "view"}
            if not set(returned) <= outs:
                faults.append(f"EXECUTION_INPUTS_STAGE_ORDINAL:views-not-on-receipt:{ci}:{po}")
    outcome = {"cellOrdinal": ci, "programOrdinal": po, "capabilityId": cell["capabilityId"],
               "languageMode": cell["languageMode"], "workspaceRoot": cell["workspaceRoot"], "required": cell["required"],
               "kinds": sorted(cell["kinds"], key=lambda k: K.C(k)), "universe": U,
               "enumeratorStatus": b["enumerator"]["status"], "enumeratorClosure": b["enumerator"].get("closureId"),
               "state": state, "deficiency": carrier[0], "nativeCause": carrier[1],
               "stageOrdinal": stage_ord, "stageOrdinalNullReason": null_reason,
               "inventoryDigests": inv_digests, "viewDigests": sorted([sfx(v) for v in returned], key=lambda h: K.C(h)),
               "candidateResultDigest": cand_digest}
    required_rows = []
    if cell["required"]:
        for s in sources:
            if s["source"] == "candidate" and not s["inputRefs"] and cand_digest is None:
                continue
            required_rows.append({"cellOrdinal": ci, "programOrdinal": po, "capabilityId": cell["capabilityId"],
                                  "relation": s["relation"], "resolution": s["resolution"], "source": s["source"],
                                  "deficiency": s["deficiency"], "nativeCause": s["nativeCause"], "universe": U,
                                  "inputRefs": cset(s["inputRefs"])})
    return outcome, accounts, cset(required_rows), sources


def derive(enum_plan, observations, ctx, faults):
    """observations: {(ci, po): {viewDigests, stageOrdinal, candidateResultDigest}} (host observation fields)."""
    outcomes, accounts, required, internal_accounts = [], [], [], []
    # HC-42 (s3): candidate views are the view refs on selectedRefs and the view outputRefs of complete receipts; a candidate view whose
    # planId is not the Plan's refuses EXECUTION_INPUTS_PLAN_JOIN
    ctx = dict(ctx, candidate_views=candidate_views(ctx))
    for vid in ctx["candidate_views"]:
        if ctx["views"][vid]["planId"] != ctx["plan_id"]:
            faults.append(f"EXECUTION_INPUTS_PLAN_JOIN:view:{vid}")
    for ci, cell in enumerate(enum_plan["cells"]):
        for b in cell["programBindings"]:
            obs = observations.get((ci, b["ordinal"]), {"viewDigests": [], "stageOrdinal": None, "candidateResultDigest": None})
            o, accs, rows, _ = derive_outcome(ci, cell, b, obs, ctx, faults)
            outcomes.append(dict({"ordinal": len(outcomes)}, **o))
            accounts += [a for a, _ in accs]
            internal_accounts += [dict(i, cellOrdinal=ci, programOrdinal=b["ordinal"], relation=a["relation"],
                                       resolution=a["resolution"], applicability=a["applicability"]) for a, i in accs]
            required += rows
    host_derived = []
    for o in outcomes:
        host_derived += [{"domain": "subject-inventory", "digest": d} for d in o["inventoryDigests"]]
        if o["candidateResultDigest"]:
            host_derived.append({"domain": "candidate-producer-result", "digest": o["candidateResultDigest"]})
    host_derived = cset(host_derived + ctx.get("sidecar_refs", []))
    stage_refs = [r for rec in ctx["receipts"] if rec["state"] == "complete" for r in rec["outputRefs"]]
    cov_refs = [{"domain": "coverage", "digest": sfx(c)} for r in stage_refs if r["domain"] == "view"
                for c in ctx["views"]["view2:" + r["digest"]]["coverageIds"]]
    imports = [{"domain": "import", "digest": sfx(i)} for i in ctx["plan"]["importIds"]]
    selected = cset(stage_refs + cov_refs + host_derived + imports)
    return {"outcomes": outcomes, "accounts": accounts, "internalAccounts": internal_accounts,
            "requiredRows": cset(required), "hostDerivedRefs": host_derived, "selectedRefs": selected,
            "candidateResultRefs": sorted({o["candidateResultDigest"] for o in outcomes if o["candidateResultDigest"]}, key=lambda h: K.C(h))}


def bridge(required_rows, xi_ref):
    """composition s9.6 steps 1-7."""
    items = []
    for row in required_rows:
        d = row["deficiency"]
        if d in EXEC_REGISTRY:
            cause = d
        elif d is None or d == "source-syntax-invalid":
            cause = "required-cell-unsatisfied"
        else:
            raise K.AdmissionError("EVALUATOR_EXECUTION_CAUSE_UNREGISTERED", str(d))
        items.append({"source": "execution", "cause": cause, "subjectId": None, "predicateId": None,
                      "inputRefs": cset([xi_ref] + row["inputRefs"]), "evidenceKind": None,
                      "nativeCause": row["nativeCause"], "universe": row["universe"]})
    return cset(items)


def build_record(plan, plan_id, exec_plan_id, evaluator_closure, enum_plan, receipts, observations, ctx):
    """Synthetic host capture (s8 intent): derive claim states from owner records; never invents Coverage."""
    faults = []
    ctx = dict(ctx, receipts=receipts, plan=plan, plan_id=plan_id)
    d = derive(enum_plan, observations, ctx, faults)
    rec = {"schemaVersion": 1, "planId": plan_id, "executionPlanId": exec_plan_id, "evaluatorClosure": evaluator_closure,
           "enumerationPlanDigest": K.raw_digest(enum_plan), "analysisSpecDigest": plan["analysisSpecDigest"],
           "hostCapture": {"custody": "host-tcb-evidence-store", "observation": "stage-return", "stageReceipts": receipts,
                           "hostDerivedRefs": d["hostDerivedRefs"]},
           "selectedRefs": d["selectedRefs"], "cellOutcomes": d["outcomes"], "nativeCoverageAccounts": d["accounts"],
           "candidateResultRefs": d["candidateResultRefs"]}
    return rec, d, faults


def admit(claimed, plan, plan_id, exec_plan, exec_plan_id, enum_plan, closures, stage_specs, ctx):
    """Re-derives from owner records + claimed OBSERVATION fields; returns (faults, derived)."""
    faults = []
    r = KIT.admit(claimed, XI_DOC, "#")
    if not r["ok"]:
        return [f"EXECUTION_INPUTS_SCHEMA:{r['typed']}{r['stock'][:1]}{r['order'][:1]}"], None
    if claimed["planId"] != plan_id:
        faults.append("EXECUTION_INPUTS_PLAN_JOIN")
    if claimed["executionPlanId"] != exec_plan_id:
        faults.append("EXECUTION_INPUTS_EXECUTION_PLAN_JOIN")
    if claimed["enumerationPlanDigest"] != K.raw_digest(enum_plan):
        faults.append("EXECUTION_INPUTS_ENUMERATION_DIGEST")
    if claimed["analysisSpecDigest"] != plan["analysisSpecDigest"]:
        faults.append("EXECUTION_INPUTS_PLAN_JOIN:analysisSpecDigest")
    ev = closures.get(claimed["evaluatorClosure"])
    if claimed["evaluatorClosure"] not in plan["semanticClosures"] or ev is None or ev["kind"] != "evaluator":
        faults.append("EXECUTION_INPUTS_EVALUATOR_CLOSURE")
    receipts = claimed["hostCapture"]["stageReceipts"]
    if [x["ordinal"] for x in receipts] != [s["ordinal"] for s in exec_plan["stages"]]:
        faults.append("EXECUTION_INPUTS_RECEIPT_TOTALITY")
    for rec, stage in zip(receipts, exec_plan["stages"]):
        spec = stage_specs.get(stage["stageSpecDigest"])
        if rec["stageSpecDigest"] != stage["stageSpecDigest"] or spec is None:
            faults.append("EXECUTION_INPUTS_STAGE_ORDINAL:spec")
            continue
        if rec["producerClosure"] != spec["producerClosure"]:
            faults.append("EXECUTION_INPUTS_STAGE_PRODUCER")
        if sorted(rec["outputDomains"]) != sorted(stage["outputDomains"]):
            faults.append("EXECUTION_INPUTS_STAGE_ORDINAL:outputDomains")
        if any(o["domain"] not in rec["outputDomains"] for o in rec["outputRefs"]):
            faults.append("EXECUTION_INPUTS_STAGE_ORDINAL:outputRefs")
        for o in rec["outputRefs"]:
            if o["domain"] == "view" and "view2:" + o["digest"] not in ctx["views"]:
                faults.append("EXECUTION_INPUTS_REF_LOST_BYTES:view")
    # HC-48 (source42 execution-inputs s3 line 53): a view on selectedRefs but on no complete receipt refuses EXECUTION_INPUTS_SELECTED_COVER
    receipt_views = {r["digest"] for rec in receipts if rec["state"] == "complete" for r in rec["outputRefs"] if r["domain"] == "view"}
    for ref in claimed["selectedRefs"]:
        if ref["domain"] == "view" and ref["digest"] not in receipt_views:
            faults.append(f"EXECUTION_INPUTS_SELECTED_COVER:view-not-on-receipt:{ref['digest']}")
    observations = {}
    bindings = [(ci, b["ordinal"]) for ci, c in enumerate(enum_plan["cells"]) for b in c["programBindings"]]
    if len(claimed["cellOutcomes"]) != len(bindings):
        faults.append("EXECUTION_INPUTS_OUTCOME_TOTALITY")
    for row in claimed["cellOutcomes"]:
        observations[(row["cellOrdinal"], row["programOrdinal"])] = {
            "viewDigests": ["view2:" + h for h in row["viewDigests"]], "stageOrdinal": row["stageOrdinal"],
            "candidateResultDigest": row["candidateResultDigest"]}
    dctx = dict(ctx, receipts=receipts, plan=plan, plan_id=plan_id, claimed_selected_refs=claimed["selectedRefs"])
    derived = derive(enum_plan, observations, dctx, faults)
    if claimed["cellOutcomes"] != derived["outcomes"]:
        faults.append("EXECUTION_INPUTS_OUTCOME_DERIVE")
    if sorted(map(K.C, claimed["nativeCoverageAccounts"])) != sorted(map(K.C, derived["accounts"])):
        faults.append("EXECUTION_INPUTS_COVERAGE_DERIVE")
    if claimed["selectedRefs"] != derived["selectedRefs"]:
        faults.append("EXECUTION_INPUTS_SELECTED_COVER")
    if any(x["domain"] in FORBIDDEN_SELECTED for x in claimed["selectedRefs"]):
        faults.append("EXECUTION_INPUTS_SELECTED_FORBIDDEN")
    if claimed["hostCapture"]["hostDerivedRefs"] != derived["hostDerivedRefs"]:
        faults.append("EXECUTION_INPUTS_HOST_DERIVED")
    if claimed["candidateResultRefs"] != derived["candidateResultRefs"]:
        faults.append("EXECUTION_INPUTS_CANDIDATE_BIND")
    for d in derived["candidateResultRefs"]:
        env = ctx["candidates"].get(d)
        if env is None:
            continue
        o = next(o for o in derived["outcomes"] if o["candidateResultDigest"] == d)
        if env["planId"] != plan_id or env["executionPlanId"] != exec_plan_id or env["cellOrdinal"] != o["cellOrdinal"] or \
                env["programOrdinal"] != o["programOrdinal"] or env["capabilityId"] != o["capabilityId"] or \
                env["languageMode"] != o["languageMode"] or env["universe"] != o["universe"] or \
                env["producerClosure"] != o["enumeratorClosure"]:
            faults.append("EXECUTION_INPUTS_CANDIDATE_BIND:join")
    try:
        bridge(derived["requiredRows"], {"domain": "execution-inputs", "digest": K.raw_digest(claimed)})
    except K.AdmissionError as exc:
        faults.append(exc.boundary)
    return faults, derived
